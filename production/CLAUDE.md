# CAPY Production - Analysis Execution Environment

> **Version:** 0.3.0
> **Last reviewed:** 2024-12-19
> **Review cadence:** Weekly during active development, monthly otherwise

This workspace is for **running production analyses** on companies.

For **prompt development and iteration**, use `../workshop/` instead.

---

## CRITICAL: You are an ORCHESTRATOR, not an ANALYST

When you see commands starting with `CAPY:`, you MUST follow the dispatch protocol below.

**DO NOT:**
- Read company source documents (`*.extracted.md`) - these are too large and will overflow your context
- Create your own analysis structure or format
- Write analysis files directly
- Use your own judgment about financial metrics

**DO:**
- Read ONLY prompt files (G3BASE, REFINE, etc.) - these are small enough to embed
- Tell subagents WHERE to find source documents (file paths) - subagent reads them itself
- Dispatch Task subagents with prompt files embedded + file paths for source docs
- Maintain organized folder structure per specification below
- Run inter-turn validators after each analytical turn
- Track pipeline state in the state JSON file
- Report completion status only

**KEY PATTERN:**
```
Orchestrator                              Subagent
    │                                        │
    ├─ Reads prompt file (small)             │
    ├─ Embeds prompt in Task                 │
    ├─ Tells subagent file paths ──────────► │
    │                                        ├─ Subagent reads source docs
    │                                        ├─ Subagent analyzes
    │                                        ├─ Subagent writes output
    ◄────────────────────────────────────────┤ Returns completion
```

---

## Folder Structure

```
production/
├── prompts/           # CANONICAL versions only (deployed from Workshop)
│   ├── base/
│   ├── refine/
│   ├── enrich/
│   ├── scenario/
│   ├── integration/
│   ├── irr/
│   ├── rq_gen/
│   ├── silicon_council/
│   └── hitl_audit/
├── kernels/           # CANONICAL versions only
├── validators/        # Inter-turn validation prompts
│   └── CAPY_INTERTURN_VALIDATOR_CC.md
├── source_library/    # Pre-staged company source documents
│   └── {TICKER}/      # One folder per company
│       ├── *.pdf
│       ├── *.extracted.md
│       └── *_pages/
└── analyses/          # Production analysis outputs
    └── {TICKER}_CAPY_{YYYYMMDD}_{HHMMSS}/
        ├── 00_source/          # Input documents
        ├── 01_T1/              # Turn 1 outputs
        ├── 02_REFINE/          # REFINE outputs
        ├── 03_T2/              # Turn 2 / Kernel outputs
        ├── 04_RQ/              # RQ_Gen outputs, RQ_Ask results
        ├── 05_SC/              # Silicon Council deliberation outputs
        ├── 06_HITL/            # Human audit outputs
        ├── pipeline_state.json
        └── README.md
```

**Note:** Current architecture is HYBRID - human orchestrator manages RQ/SC/HITL steps manually.
Future "AUTO CAPY" mode will add workarounds for automated full-pipeline execution.

**Folder naming:** `{TICKER}_CAPY_{YYYYMMDD}_{HHMMSS}`
- Example: `DAVE_CAPY_20241215_143022`
- Timestamp enables multiple runs per day per ticker

---

## Command Reference

### SOURCE: UPLOAD {TICKER}

Auto-find, organize, and preprocess PDF documents for a company.

**Trigger:** User says `SOURCE: UPLOAD {TICKER}` after dropping PDFs anywhere in production.

**Steps:**

1. **Scan for unprocessed PDFs** anywhere in production/:
   - Find all `*.pdf` files NOT already in `source_library/`
   - Exclude any PDFs in `analyses/` folders (those are already processed)

2. Create `source_library/{TICKER}/` if it doesn't exist

3. Move found PDFs to `source_library/{TICKER}/`

4. **Auto-preprocess each PDF:**
   - Run `/pdf-extract` to generate `{filename}.extracted.md` (text extraction)
   - Run `/pdf-visual` to generate `{filename}_pages/` directory (page images for visual analysis)
   - Both outputs saved alongside the PDF in `source_library/{TICKER}/`

5. Generate/update inventory file `source_library/{TICKER}/INVENTORY.md`:
   ```markdown
   # {TICKER} Source Documents

   Last updated: {YYYY-MM-DD HH:MM}

   ## Documents
   | PDF | Extracted Text | Page Images | Pages |
   |-----|----------------|-------------|-------|
   | filename.pdf | filename.extracted.md | filename_pages/ | N |
   ```

6. Report: "Found {N} PDFs. Processed and organized into source_library/{TICKER}/. Ready for CAPY: INIT."

**Preprocessing Details:**
- `/pdf-extract`: Converts PDF to markdown using `pdftoppm` + OCR pipeline
- `/pdf-visual`: Extracts each page as PNG for charts, diagrams, visual data
- Both are required for full CAPY analysis (text for financials, images for charts)

**Usage Notes:**
- Researchers can drop PDFs anywhere in production/ - no specific location needed
- Just run `SOURCE: UPLOAD {TICKER}` and system finds + processes them
- Documents persist in source_library until manually deleted
- CAPY: INIT copies from source_library to analysis 00_source/
- Multiple filings per company supported (10-K, 10-Q, presentations, etc.)
- If preprocessing fails, PDF is kept but flagged in INVENTORY.md
- Running `SOURCE: UPLOAD {TICKER}` again will find any new PDFs and add to existing folder

---

### CAPY: INIT {TICKER} {COMPANY_NAME} {DATE}

1. Generate timestamp: `{HHMMSS}` from current time

2. Create analysis folder structure:
```
analyses/{TICKER}_CAPY_{YYYYMMDD}_{HHMMSS}/
├── 00_source/          # Input documents
├── 01_T1/              # Turn 1 outputs
├── 02_REFINE/          # REFINE outputs
├── 03_T2/              # Turn 2 / Kernel outputs
├── pipeline_state.json
└── README.md
```

3. Copy source files from `source_library/{TICKER}/` to `00_source/`:
   - All `*.extracted.md` files
   - All `*_pages/` directories
   - Original PDFs if present

   If `source_library/{TICKER}/` doesn't exist, prompt user to upload documents first.

4. Create `pipeline_state.json`:
```json
{
  "ticker": "{TICKER}",
  "company_name": "{COMPANY_NAME}",
  "date": "{DATE}",
  "run_id": "{TICKER}_CAPY_{YYYYMMDD}_{HHMMSS}",
  "run_timestamp": "ISO8601 timestamp",
  "prompt_versions": {
    "base": "G3BASE_X.X.Xe.md",
    "refine": "BASE_T1_REFINE_vX_X.md",
    "kernel": "BASE_CVR_KERNEL_X.X.Xe.py"
  },
  "completed_turns": [],
  "current_turn": null,
  "validation_results": {},
  "outputs": {}
}
```

5. Report initialization complete. Do nothing else.

---

### CAPY: RUN BASE_PIPELINE

**Executes the full BASE analysis chain (T1 → REFINE → T2) without human checkpointing.**

This is the preferred command for production runs. Use individual stage commands only for debugging or re-runs.

```
┌─────────────────────────────────────────────────────────┐
│  CAPY: RUN BASE_PIPELINE                                │
├─────────────────────────────────────────────────────────┤
│  1. BASE_T1 (Opus subagent)                             │
│     └── Validate (Haiku) → FAIL? Stop. PASS/WARN? ↓    │
│                                                         │
│  2. BASE_REFINE (Opus subagent)                         │
│     └── Validate (Haiku) → FAIL? Stop. PASS/WARN? ↓    │
│                                                         │
│  3. BASE_T2 (Kernel execution + formatting)             │
│     └── Validate (Haiku) → Report final status          │
└─────────────────────────────────────────────────────────┘
```

**Prerequisites:**
- `CAPY: INIT {TICKER} {COMPANY_NAME} {DATE}` already run
- `pipeline_state.json` exists with `completed_turns: []`
- Source docs present in `00_source/`

---

#### Stage 1: BASE_T1

**CRITICAL: The orchestrator does NOT read source documents. The subagent reads them.**

1. **Orchestrator reads ONLY the prompt file:**
   - Read: `prompts/base/G3BASE_*.md` (this is small, ~50KB)
   - Do NOT read `00_source/*.extracted.md` files - these are too large

2. **Spawn Opus subagent** (Task tool, subagent_type: "general-purpose"):
   ```
   You are executing CAPY BASE Turn 1.

   === G3BASE PROMPT (FOLLOW THIS EXACTLY) ===
   [FULL contents of G3BASE prompt file - orchestrator embeds this]

   === COMPANY DOCUMENTS ===
   Read ALL files in: analyses/{RUN_ID}/00_source/*.extracted.md
   Use the Read tool to load each document yourself.

   === VISUAL DATA ===
   Read PNG files from: analyses/{RUN_ID}/00_source/*_pages/
   Use the Read tool to analyze visual data from investor presentations.

   === TRIGGER ===
   Do Turn 1: {COMPANY_NAME}, {EXCHANGE}:{TICKER}, As of {DATE}

   === OUTPUT INSTRUCTION ===
   Write your complete output to: analyses/{RUN_ID}/01_T1/{TICKER}_BASE_T1.md

   Your output MUST include:
   1. Four analytical narratives (I-IV) as specified in G3BASE
   2. JSON artifacts A.1 through A.6 with EXACT schema from G3BASE
   3. All Y0 data points needed for kernel execution
   ```

3. **Wait for subagent completion**

4. **Run validator** (Task tool, subagent_type: "general-purpose", model: haiku):
   ```
   You are the CAPY inter-turn validator.

   === VALIDATOR PROMPT ===
   [FULL contents of validators/CAPY_INTERTURN_VALIDATOR_CC.md]

   === STAGE ===
   BASE_T1

   === OUTPUT TO VALIDATE ===
   [FULL contents of 01_T1/{TICKER}_BASE_T1.md]

   Return ONLY the JSON validation result.
   ```

5. **Process validation result:**
   - Parse JSON response
   - Write to: `01_T1/{TICKER}_T1_validation.json`
   - If `"proceed": false` → **HALT pipeline**, report issues to user
   - If `"proceed": true` → Continue to Stage 2

6. **Update state:**
   - Add "T1" to `completed_turns`
   - Set `current_turn: "REFINE"`

---

#### Stage 2: BASE_REFINE

**CRITICAL: The orchestrator does NOT read source documents. The subagent reads them.**

1. **Orchestrator reads ONLY prompt files and T1 output:**
   - Read: `prompts/refine/BASE_T1_REFINE_*.md` (small)
   - Read: `prompts/base/G3BASE_*.md` (small)
   - Read: `01_T1/{TICKER}_BASE_T1.md` (T1 output - medium size)
   - Do NOT read `00_source/*.extracted.md` files

2. **Spawn Opus subagent:**
   ```
   You are executing CAPY BASE REFINE.

   === REFINE PROMPT (FOLLOW THIS EXACTLY) ===
   [FULL contents of REFINE prompt file - orchestrator embeds this]

   === G3BASE PROMPT (REFERENCE) ===
   [FULL contents of G3BASE prompt file - orchestrator embeds this]

   === T1 OUTPUT TO REFINE ===
   [FULL contents of T1 output - orchestrator embeds this]

   === COMPANY DOCUMENTS ===
   Read ALL files in: analyses/{RUN_ID}/00_source/*.extracted.md
   Use the Read tool to load each document yourself.

   === TRIGGER ===
   Do REFINE

   === OUTPUT INSTRUCTION ===
   Write your complete output to: analyses/{RUN_ID}/02_REFINE/{TICKER}_BASE_REFINE.md
   ```

3. **Wait for subagent completion**

4. **Run validator** (same pattern as Stage 1, with stage="BASE_REFINE")

5. **Process validation result:**
   - Write to: `02_REFINE/{TICKER}_REFINE_validation.json`
   - If `"proceed": false` → **HALT pipeline**, report issues
   - If `"proceed": true` → Continue to Stage 3

6. **Update state:**
   - Add "REFINE" to `completed_turns`
   - Set `current_turn: "T2"`

---

#### Stage 3: BASE_T2

**CRITICAL: T2 is kernel execution, NOT an LLM analysis task. DO NOT spawn a subagent.**

**WARNING (from smoke test 2024-12-16):** Subagents will fabricate kernel output instead of running Python.
T2 MUST be executed by the orchestrator directly via Bash.

1. **Extract artifacts from REFINE output:**
   - Read `02_REFINE/{TICKER}_BASE_REFINE.md`
   - Parse and extract JSON blocks:
     - A.1_EPISTEMIC_ANCHORS
     - A.2_ANALYTIC_KG (including Y0_data)
     - A.3_CAUSAL_DAG
     - A.5_GESTALT_IMPACT_MAP
     - A.6_DR_DERIVATION_TRACE
   - Write to: `03_T2/{TICKER}_kernel_input.json`

2. **Fix schema mismatches (if any):**

   The kernel expects specific key names. Common REFINE output → kernel input fixes:
   - `A.3_CAUSAL_DAG.nodes` → `A.3_CAUSAL_DAG.DAG`
   - `A.5_GESTALT_IMPACT_MAP.drivers` → `A.5_GESTALT_IMPACT_MAP.GIM`
   - Ensure `A.3_CAUSAL_DAG.coverage_manifest` is populated (not empty)
   - Collapse multi-period GIM formats (`Y1_Y3`, `Y4_Y10`) to single DSL per driver

   If fixes are needed, write corrected version to: `03_T2/{TICKER}_kernel_input_fixed.json`

3. **Execute Python kernel via Bash (NOT subagent):**
   ```bash
   cd {REPO_ROOT}
   python -c "
   import json
   import sys
   sys.path.insert(0, 'kernels')
   from BASE_CVR_KERNEL_2_2_1e import execute_cvr_workflow

   with open('analyses/{RUN_ID}/03_T2/{TICKER}_kernel_input.json', 'r') as f:
       artifacts = json.load(f)

   result = execute_cvr_workflow(
       kg=artifacts['A.2_ANALYTIC_KG'],
       dag_artifact=artifacts['A.3_CAUSAL_DAG'],
       gim_artifact=artifacts['A.5_GESTALT_IMPACT_MAP'],
       dr_trace=artifacts['A.6_DR_DERIVATION_TRACE']
   )

   with open('analyses/{RUN_ID}/03_T2/{TICKER}_kernel_output.json', 'w') as f:
       json.dump(result, f, indent=2)

   print('Kernel execution complete')
   print(json.dumps(result, indent=2))
   "
   ```

4. **Format T2 output:**
   - Read kernel output JSON
   - Format as markdown with A.7 artifact
   - Write to: `03_T2/{TICKER}_BASE_T2.md`

5. **Run validator** (stage="BASE_T2", **model: opus** - Haiku misses fabrication)

6. **Process validation result:**
   - Write to: `03_T2/{TICKER}_T2_validation.json`
   - Update state: add "T2" to `completed_turns`, set `current_turn: null`

---

#### Pipeline Completion

Report summary to user:

```
BASE_PIPELINE complete for {TICKER}

Run ID: {RUN_ID}

Stage Results:
├── T1:     {PASS/WARN/FAIL}
├── REFINE: {PASS/WARN/FAIL}
└── T2:     {PASS/WARN/FAIL}

Key Outputs:
├── 01_T1/{TICKER}_BASE_T1.md
├── 02_REFINE/{TICKER}_BASE_REFINE.md
└── 03_T2/{TICKER}_BASE_T2.md

IVPS: ${value} (from A.7)

Next steps:
- CAPY: RUN RQ_STAGE (generates and executes research questions)
- Or manually proceed to ENRICH stage
```

---

### CAPY: RUN RQ_STAGE

**Executes the full RQ pipeline (RQ_GEN → A.8 Validation → RQ_ASK) with parallel research subagents.**

```
┌─────────────────────────────────────────────────────────────┐
│  CAPY: RUN RQ_STAGE                                          │
├─────────────────────────────────────────────────────────────┤
│  1. RQ_GEN (Opus subagent)                                   │
│     └── Generate A.8_RESEARCH_STRATEGY_MAP                   │
│                                                              │
│  2. A.8 VALIDATOR (Haiku subagent)                           │
│     └── FAIL? Stop. PASS? ↓                                  │
│                                                              │
│  3. RQ_ASK (7 Parallel Opus subagents)                       │
│     └── Execute research queries with WebSearch              │
│     └── Each subagent writes directly to disk                │
│                                                              │
│  4. Generate A.9_RESEARCH_RESULTS summary                    │
└─────────────────────────────────────────────────────────────┘
```

**Prerequisites:**
- BASE_PIPELINE complete (`completed_turns` includes T1, REFINE, T2)
- A.7 artifact exists in `03_T2/{TICKER}_BASE_T2.md`

---

#### Stage 1: RQ_GEN

1. **Orchestrator reads:**
   - `prompts/rq_gen/RQ_Gen_2_2_3e.md` (7-slot RQ generation prompt)
   - `01_T1/{TICKER}_BASE_T1.md` (for A.1-A.6 artifacts)
   - `02_REFINE/{TICKER}_BASE_REFINE.md` (for refined artifacts)
   - `03_T2/{TICKER}_BASE_T2.md` (for A.7 with Tornado/Model Notes)

2. **Spawn Opus subagent:**
   ```
   You are executing CAPY RQ_GEN.

   === RQ_GEN PROMPT (FOLLOW THIS EXACTLY) ===
   [FULL contents of RQ_Gen_2_2_3e.md - orchestrator embeds this]

   === BASE ARTIFACTS ===
   [FULL contents of T1, REFINE, T2 outputs - orchestrator embeds]

   === TRIGGER ===
   Generate A.8_RESEARCH_STRATEGY_MAP for {COMPANY_NAME} ({TICKER})

   === OUTPUT INSTRUCTION ===
   Write your complete A.8 JSON artifact to:
   analyses/{RUN_ID}/04_RQ/{TICKER}_A8_RESEARCH_PLAN.json
   ```

3. **Wait for subagent completion**

---

#### Stage 2: A.8 Validation

1. **Spawn Haiku validator:**
   - Use `validators/A8_VALIDATOR.md`
   - Validate the A.8 JSON artifact

2. **Process validation:**
   - If FAIL: Stop pipeline, report issues
   - If PASS: Continue to RQ_ASK

---

#### Stage 3: RQ_ASK (7 Parallel Subagents)

**CRITICAL: Launch all 7 subagents in parallel using direct-write protocol.**

1. **Parse A.8** to extract 7 research queries:
   - M-1: Integrity Check (forensic accounting, governance)
   - M-2: Adversarial Synthesis (bull/bear arguments)
   - M-3a: Mainline Scenario H.A.D. (4 mainline scenarios)
   - M-3b: Tail Scenario H.A.D. (4 tail scenarios: 2 Blue Sky + 2 Black Swan)
   - D-1, D-2, D-3: Dynamic Lynchpin coverage

2. **Launch 7 parallel Task subagents** (one message with 7 Task tool calls):

   For each RQ (1-7):
   ```
   You are a Deep Research Agent executing {RQ_ID} for CAPY analysis.

   === RESEARCH QUESTION ===
   {Prompt_Text from A.8}

   === CITATION REQUIREMENTS ===
   - Every factual claim MUST include an inline citation
   - Use format: [Source Name, Date] or [SEC Filing Type, Date]
   - Include specific page numbers when available

   === OUTPUT STRUCTURE ===
   ## Executive Summary
   ## Detailed Findings
   ## Key Uncertainties
   ## Sources

   === OUTPUT INSTRUCTION ===
   After completing your research, use the Write tool to save your report to:
   analyses/{RUN_ID}/04_RQ/RQ{N}_{Topic}.md

   Return only a confirmation with the filepath.
   ```

3. **Wait for all 7 subagents** via TaskOutput (blocking)

4. **Verify output files exist:**
   ```
   04_RQ/
   ├── {TICKER}_A8_RESEARCH_PLAN.json
   ├── RQ1_Accounting_Governance.md       (M-1)
   ├── RQ2_Bull_Bear_Arguments.md         (M-2)
   ├── RQ3a_Mainline_Scenarios.md         (M-3a)
   ├── RQ3b_Tail_Scenarios.md             (M-3b)
   ├── RQ4_{Lynchpin_Topic}.md            (D-1)
   ├── RQ5_{Lynchpin_Topic}.md            (D-2)
   └── RQ6_{Lynchpin_Topic}.md            (D-3)
   ```

5. **Generate A.9_RESEARCH_RESULTS:**
   ```json
   {
     "ticker": "{TICKER}",
     "execution_timestamp": "ISO-8601",
     "executor": "claude",
     "total_queries": 7,
     "successful_queries": 7,
     "results": [
       {
         "rq_id": "RQ1",
         "status": "SUCCESS",
         "coverage_objective": "M-1 Integrity Check",
         "output_file": "RQ1_Accounting_Governance.md",
         "word_count": 5800
       }
     ]
   }
   ```
   Write to: `04_RQ/{TICKER}_A9_RESEARCH_RESULTS.json`

---

#### RQ Stage Completion

Report summary to user:

```
RQ_STAGE complete for {TICKER}

Run ID: {RUN_ID}

Stage Results:
├── RQ_GEN:   PASS (7 queries generated)
├── A.8:      PASS (schema valid)
└── RQ_ASK:   7/7 SUCCESS

Research Outputs:
├── 04_RQ/RQ1_Accounting_Governance.md      (M-1)
├── 04_RQ/RQ2_Bull_Bear_Arguments.md        (M-2)
├── 04_RQ/RQ3a_Mainline_Scenarios.md        (M-3a, 4 scenarios)
├── 04_RQ/RQ3b_Tail_Scenarios.md            (M-3b, 4 scenarios)
├── 04_RQ/RQ4_{Topic}.md                    (D-1)
├── 04_RQ/RQ5_{Topic}.md                    (D-2)
└── 04_RQ/RQ6_{Topic}.md                    (D-3)

Total: ~{N}K words of research across 8 scenarios

Next steps:
- Review research outputs
- CAPY: RUN ENRICH (Bayesian synthesis)
- Or manually proceed to SCENARIO stage
```

---

#### Error Handling

**If validation FAILS at any stage:**

1. Do NOT proceed to next stage
2. Report the validation JSON to user
3. Show specific issues and their locations
4. Suggest remediation:
   - For missing artifacts: "Re-run {stage} - prompt may have been truncated"
   - For JSON parse errors: "Check {artifact} formatting in output"
   - For sanity bound violations: "Review source data - {metric} out of expected range"

**If kernel execution fails:**

1. Report Python error/traceback
2. Check `kernel_input.json` for malformed data
3. Suggest: "Verify REFINE output artifacts are valid JSON"

---

### CAPY: RUN BASE_T1

**YOU MUST USE THE TASK TOOL TO SPAWN A SUBAGENT.**

**CRITICAL: Orchestrator reads ONLY the prompt. Subagent reads source documents.**

1. **Orchestrator reads:**
   - `prompts/base/G3BASE_*.md` (the FULL prompt - embed this in subagent prompt)

2. **Orchestrator does NOT read:**
   - Source documents (*.extracted.md) - too large, subagent reads these itself

3. Spawn a Task subagent (subagent_type: "general-purpose") with prompt:
   ```
   You are executing CAPY BASE Turn 1.

   === G3BASE PROMPT (FOLLOW THIS EXACTLY) ===
   [FULL contents of G3BASE prompt - orchestrator embeds this]

   === COMPANY DOCUMENTS ===
   Read ALL files in: analyses/{RUN_ID}/00_source/*.extracted.md
   Use the Read tool to load each document yourself.

   === VISUAL DATA ===
   Read PNG files from: analyses/{RUN_ID}/00_source/*_pages/
   Use the Read tool to analyze visual data from investor presentations.

   === TRIGGER ===
   Do Turn 1: {COMPANY_NAME}, {EXCHANGE}:{TICKER}, As of {DATE}

   === OUTPUT INSTRUCTION ===
   Write your complete output to: analyses/{RUN_ID}/01_T1/{TICKER}_BASE_T1.md
   ```

4. Wait for Task completion

5. **RUN VALIDATOR** (subagent_type: "general-purpose", model: haiku):
   - Validate output at `01_T1/{TICKER}_BASE_T1.md`
   - Write result to `01_T1/{TICKER}_T1_validation.json`
   - If FAIL: Stop and report errors
   - If PASS/WARN: Continue

6. Update state file, report completion

---

### CAPY: RUN BASE_REFINE

**CRITICAL: Orchestrator reads prompts and T1 output. Subagent reads source documents.**

1. **Orchestrator reads:**
   - `prompts/refine/BASE_T1_REFINE_*.md` (FULL contents - embed)
   - `prompts/base/G3BASE_*.md` (FULL contents - embed)
   - `01_T1/{TICKER}_BASE_T1.md` (T1 output - embed)

2. **Orchestrator does NOT read:**
   - Source documents (*.extracted.md) - subagent reads these itself

3. Spawn Task subagent with prompt:
   ```
   You are executing CAPY BASE REFINE.

   === REFINE PROMPT ===
   [FULL contents of REFINE prompt - orchestrator embeds]

   === G3BASE PROMPT (REFERENCE) ===
   [FULL contents of G3BASE - orchestrator embeds]

   === T1 OUTPUT TO REFINE ===
   [FULL contents of T1 output - orchestrator embeds]

   === COMPANY DOCUMENTS ===
   Read ALL files in: analyses/{RUN_ID}/00_source/*.extracted.md
   Use the Read tool to load each document yourself.

   === TRIGGER ===
   Do REFINE

   === OUTPUT ===
   Write to: analyses/{RUN_ID}/02_REFINE/{TICKER}_BASE_REFINE.md
   ```

4. **RUN VALIDATOR**:
   - Validate output
   - Write result to `02_REFINE/{TICKER}_REFINE_validation.json`
   - If FAIL: Stop and report errors

5. Update state file, report completion

---

### CAPY: RUN BASE_T2

**CRITICAL: T2 REQUIRES ACTUAL PYTHON KERNEL EXECUTION**

T2 is NOT an LLM analysis task. It is a kernel execution task.

**Step 1: Extract artifacts from REFINE output**

Read the REFINE output (or T1 if no REFINE) and extract JSON artifacts:
- A.1_EPISTEMIC_ANCHORS
- A.2_ANALYTIC_KG (including Y0_data)
- A.3_CAUSAL_DAG
- A.5_GESTALT_IMPACT_MAP
- A.6_DR_DERIVATION_TRACE

Write to: `03_T2/{TICKER}_kernel_input.json`

**Step 2: Execute the Python kernel**

```python
import json
import sys
sys.path.insert(0, 'kernels')
from BASE_CVR_KERNEL_2_2_1e import execute_cvr_workflow

with open('analyses/{TICKER}_CAPY_{YYYYMMDD}_{HHMMSS}/03_T2/{TICKER}_kernel_input.json', 'r') as f:
    artifacts = json.load(f)

result = execute_cvr_workflow(
    kg=artifacts['A.2_ANALYTIC_KG'],
    dag_artifact=artifacts['A.3_CAUSAL_DAG'],
    gim_artifact=artifacts['A.5_GESTALT_IMPACT_MAP'],
    dr_trace=artifacts['A.6_DR_DERIVATION_TRACE']
)

print(json.dumps(result, indent=2))
```

**Step 3: Write T2 output**

Output to: `03_T2/{TICKER}_BASE_T2.md`

**Step 4: RUN VALIDATOR**

**DO NOT:**
- Perform manual DCF calculations
- Invent kernel output
- Skip Python execution

---

### CAPY: STATUS

Report current pipeline state for all active analyses.

### CAPY: REPORT

Generate final README.md for completed analysis.

### CAPY: COMPARE RUNS {TICKER} [N]

Compare the N most recent production runs for a ticker (default N=2):

1. List all folders in `analyses/` matching `{TICKER}_CAPY_*`
2. Sort by timestamp (extracted from folder name YYYYMMDD_HHMMSS)
3. Load `pipeline_state.json` from each of the N most recent
4. Report:
   - Run timestamps
   - Prompt versions used in each run
   - Validation results for each stage
   - Final IVPS (if T2 completed)
   - Key differences between runs

---

## Inter-Turn Validator

After EVERY analytical turn, spawn a validation subagent using `validators/CAPY_INTERTURN_VALIDATOR_CC.md`.

**Validator prompt file:** `validators/CAPY_INTERTURN_VALIDATOR_CC.md`

**Model selection:**
- T1, REFINE: Use **Haiku** (cost-effective, sufficient for structure checks)
- T2: Use **Opus** (Haiku cannot reliably detect fabrication vs real kernel output)

**Checks performed:**
1. **Output Structure:** Non-empty, has headers, not truncated
2. **Artifacts Present:** Required artifacts for stage exist
3. **JSON Valid:** All JSON blocks parse correctly
4. **Sanity Bounds:** DR 5-16%, IVPS > 0, g < DR, etc.
5. **No Fabrication:** T1/REFINE don't contain kernel-computed values
6. **DR Derivation:** (REFINE only) X_T1, X_REFINE, X_final documented
7. **Kernel Execution Verification:** (T2 only) Confirm output came from actual Python execution

**Output:** JSON with `"proceed": true/false` and detailed check results.

**Pipeline behavior:**
- `"proceed": true` → Continue to next stage
- `"proceed": false` → HALT pipeline, report issues to user

---

## Version Info

Prompts and kernels in this folder are CANONICAL versions deployed from Workshop.

Last deployment: [Check VERSION.md]

---

## Maturity Status

> **This CLAUDE.md is v0.3.0 (DRAFT)**

Current status: BASE_PIPELINE and RQ_STAGE smoke-tested. T1 and REFINE work via subagent dispatch. T2 requires orchestrator-direct kernel execution (subagents fabricate results). RQ_STAGE uses 7 parallel Claude Opus subagents with direct-write protocol.

Before v1.0:
- [x] Full smoke test of CC-enabled CAPY production run (2024-12-16, DAVE)
- [x] Build out complete instructions for BASE pipeline stages (T1, REFINE, T2)
- [x] Document inter-turn validator integration
- [x] Validate subagent dispatch patterns work end-to-end (T1, REFINE: yes; T2: no)
- [x] Document error handling and recovery procedures
- [x] Document RQ_STAGE with 7-slot architecture (2024-12-19)
- [x] RQ_STAGE smoke test (DAVE, 7 parallel subagents, ~220K words output)
- [ ] Test COMPARE RUNS functionality
- [ ] Add remaining pipeline stages (ENRICH, SCENARIO, INT, IRR)
- [ ] Document SC, HITL pause points

**Smoke Test Findings (2024-12-16):**
- T1: Opus subagent works correctly
- REFINE: Opus subagent works correctly
- T2: **Subagent fabricates results** - must run kernel via Bash directly
- Haiku validator: **False positive on T2** - use Opus for T2 validation
- Schema mismatches: REFINE outputs `nodes`/`drivers`, kernel expects `DAG`/`GIM`
- Kernel output revealed DAG/GIM bugs (negative CAGR, 80%+ ROIC) - prompt patches needed in WORKSHOP

**Pending WORKSHOP updates (do not apply here):**
- REFINE v1_2: Add trajectory calibration, enforce kernel schema
- G3BASE 2.2.2e: Clarify unit conventions, add schema examples

**Do not rely on these instructions for production analyses until v1.0.**

---

## Git Workflow

Claude Code may create isolated worktree branches (e.g., `magical-sanderson`, `interesting-meitner`) for each session. Changes made in a worktree are NOT visible in master or other worktrees until merged.

**End of Session Protocol:**

When the user says "commit" at the end of a session:

1. Stage all changes: `git add -A`
2. Commit with descriptive message
3. If on a worktree branch (not master):
   - Checkout master: `git checkout master`
   - Merge the branch: `git merge <branch-name>`
   - Delete the branch: `git branch -d <branch-name>`
4. Confirm: "Changes committed and merged to master."

**Useful commands:**
- `git worktree list` - See all worktrees
- `git branch` - See current branch (* = current)
- `git status` - See uncommitted changes

**Rule:** All work should end up on `master`. Worktree branches are temporary workspaces, not long-lived feature branches.
