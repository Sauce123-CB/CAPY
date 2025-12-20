# CAPY Production - Analysis Execution Environment

> **Version:** 0.5.0
> **Last reviewed:** 2024-12-19
> **Review cadence:** Weekly during active development, monthly otherwise

This workspace is for **running production analyses** on companies.

For **prompt development and iteration**, use `../workshop/` instead.

---

## Auto-Peek Protocol

**When to automatically look at workshop (without user asking):**

| Trigger | Auto-Action |
|---------|-------------|
| Need latest orchestration patterns | Read `../workshop/orchestration/ORCHESTRATION_KEY_PATTERNS.md` |
| Checking EXPERIMENTAL prompt versions | `ls ../workshop/prompts/{stage}/` |
| Need to understand a patch or change | Read `../workshop/patches/SESSION_LOG_*.md` |
| Smoke test results for comparison | `ls ../workshop/smoke_tests/{TICKER}_*` |
| Checking pending patches | Read `../workshop/patches/PATCH_TRACKER.md` |

**When to automatically look at shared:**

| Trigger | Auto-Action |
|---------|-------------|
| Executing any pipeline stage | Read `../shared/PATTERNS.md` (pattern quick-ref) |
| Unsure how contexts connect | Read `../shared/BRIDGE.md` |

**Implementation:** Just do it. Don't ask permission to read sibling directories. Report what you found.

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

## Checkpoint Protocol (MANDATORY)

**ALWAYS checkpoint before modifying ANY file.**

This is non-negotiable. Do NOT edit, write, or modify files without explicit user approval.

**Before ANY file modification:**
1. **State** exactly which file(s) you intend to modify
2. **Show** the specific changes you plan to make (old → new)
3. **Wait** for explicit user approval ("yes", "proceed", "do it", etc.)
4. **Only then** execute the edit

**Rationale:** Unchecked edits cause catastrophic errors. Reading files is fine. Modifying files requires approval.

**No exceptions.** Even "trivial" changes require checkpoint. If you're uncertain whether something counts as a modification, checkpoint anyway.

**Violations:** If you modify a file without checkpointing, immediately revert the change and apologize.

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
│     └── Validate (Opus) → FAIL? Stop. PASS/WARN? ↓     │
│                                                         │
│  2. BASE_REFINE (Opus subagent)                         │
│     └── Validate (Opus) → FAIL? Stop. PASS/WARN? ↓     │
│                                                         │
│  3. BASE_T2 (Kernel execution + formatting)             │
│     └── Validate (Opus) → Report final status           │
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

   === OUTPUT INSTRUCTION (Direct-Write Protocol) ===
   Use the Write tool to save your complete output to: analyses/{RUN_ID}/01_T1/{TICKER}_BASE_T1.md

   Your output MUST include:
   1. Four analytical narratives (I-IV) as specified in G3BASE
   2. JSON artifacts A.1 through A.6 with EXACT schema from G3BASE
   3. All Y0 data points needed for kernel execution

   After writing the file, return ONLY: "Complete. File: analyses/{RUN_ID}/01_T1/{TICKER}_BASE_T1.md"
   DO NOT return the file contents.
   ```

3. **Wait for subagent completion** - subagent returns confirmation + filepath only

4. **Verify file exists:** `ls -la analyses/{RUN_ID}/01_T1/{TICKER}_BASE_T1.md`

5. **Run validator** (Task tool, subagent_type: "general-purpose", model: opus):
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

6. **Process validation result:**
   - Parse JSON response
   - Write to: `01_T1/{TICKER}_T1_validation.json`
   - If `"proceed": false` → **HALT pipeline**, report issues to user
   - If `"proceed": true` → Continue to Stage 2

7. **Update state:**
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

   === OUTPUT INSTRUCTION (Direct-Write Protocol) ===
   Use the Write tool to save your complete output to: analyses/{RUN_ID}/02_REFINE/{TICKER}_BASE_REFINE.md

   After writing the file, return ONLY: "Complete. File: analyses/{RUN_ID}/02_REFINE/{TICKER}_BASE_REFINE.md"
   DO NOT return the file contents.
   ```

3. **Wait for subagent completion** - subagent returns confirmation + filepath only

4. **Verify file exists:** `ls -la analyses/{RUN_ID}/02_REFINE/{TICKER}_BASE_REFINE.md`

5. **Run validator** (same pattern as Stage 1, with stage="BASE_REFINE")

6. **Process validation result:**
   - Write to: `02_REFINE/{TICKER}_REFINE_validation.json`
   - If `"proceed": false` → **HALT pipeline**, report issues
   - If `"proceed": true` → Continue to Stage 3

7. **Update state:**
   - Add "REFINE" to `completed_turns`
   - Set `current_turn: "T2"`

---

#### Stage 3: BASE_T2

**CRITICAL: Subagent executes kernel via Bash. Direct-write to disk.**

1. **Spawn Opus subagent** (Task tool, subagent_type: "general-purpose"):
   ```
   You are executing CAPY BASE Turn 2.

   YOUR JOB IS KERNEL EXECUTION, NOT ANALYSIS.

   === STEP 1: READ REFINE OUTPUT ===
   Read: analyses/{RUN_ID}/02_REFINE/{TICKER}_BASE_REFINE.md

   === STEP 2: EXTRACT AND VALIDATE ARTIFACTS ===
   Extract these JSON blocks from REFINE and save to individual files:
   - A.2_ANALYTIC_KG → analyses/{RUN_ID}/03_T2/A2_ANALYTIC_KG.json
   - A.3_CAUSAL_DAG → analyses/{RUN_ID}/03_T2/A3_CAUSAL_DAG.json
   - A.5_GESTALT_IMPACT_MAP → analyses/{RUN_ID}/03_T2/A5_GESTALT_IMPACT_MAP.json
   - A.6_DR_DERIVATION_TRACE → analyses/{RUN_ID}/03_T2/A6_DR_DERIVATION_TRACE.json

   If JSON is malformed, repair it (fix brackets, trailing commas, etc.)
   Use the Write tool to save each JSON file.

   === STEP 3: EXECUTE KERNEL VIA BASH ===
   **YOU MUST USE THE BASH TOOL. DO NOT COMPUTE IVPS YOURSELF.**

   Run this command:
   python -c "
   import json
   import sys
   sys.path.insert(0, 'kernels')
   from BASE_CVR_KERNEL_2_2_1e import execute_cvr_workflow

   kg = json.load(open('analyses/{RUN_ID}/03_T2/A2_ANALYTIC_KG.json'))
   dag = json.load(open('analyses/{RUN_ID}/03_T2/A3_CAUSAL_DAG.json'))
   gim = json.load(open('analyses/{RUN_ID}/03_T2/A5_GESTALT_IMPACT_MAP.json'))
   dr = json.load(open('analyses/{RUN_ID}/03_T2/A6_DR_DERIVATION_TRACE.json'))

   result = execute_cvr_workflow(kg, dag, gim, dr)

   json.dump(result, open('analyses/{RUN_ID}/03_T2/A7_kernel_output.json', 'w'), indent=2)
   print(json.dumps(result, indent=2))
   "

   === STEP 4: FORMAT T2 OUTPUT ===
   Read the kernel output JSON. Create T2 markdown document with:
   - Execution summary (kernel version, status)
   - A.7_LIGHTWEIGHT_VALUATION_SUMMARY (embed full JSON)
   - Sensitivity analysis results
   - Terminal driver values

   Use the Write tool to save to: analyses/{RUN_ID}/03_T2/{TICKER}_BASE_T2.md

   === STEP 5: RETURN CONFIRMATION ===
   Return ONLY: "Complete. File: analyses/{RUN_ID}/03_T2/{TICKER}_BASE_T2.md"
   DO NOT return the file contents.

   === PROHIBITED ===
   - DO NOT calculate IVPS yourself
   - DO NOT invent kernel output
   - If Bash fails, report the error - do not fabricate results
   ```

2. **Wait for subagent completion** - subagent returns confirmation + filepath only

3. **Verify output file exists:** `ls -la analyses/{RUN_ID}/03_T2/{TICKER}_BASE_T2.md`

4. **Run validator** (Task tool, subagent_type: "general-purpose", model: opus):
   - Validate output at `03_T2/{TICKER}_BASE_T2.md`
   - Write result to `03_T2/{TICKER}_T2_validation.json`

5. **Process validation result:**
   - If `"proceed": false` → HALT pipeline, report issues
   - If `"proceed": true` → Continue

6. **Update state:**
   - Add "T2" to `completed_turns`
   - Set `current_turn: null`

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
│  2. A.8 VALIDATOR (Opus subagent)                            │
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

   === OUTPUT INSTRUCTION (Direct-Write Protocol) ===
   Use the Write tool to save your complete A.8 JSON artifact to:
   analyses/{RUN_ID}/04_RQ/{TICKER}_A8_RESEARCH_PLAN.json

   After writing the file, return ONLY: "Complete. File: analyses/{RUN_ID}/04_RQ/{TICKER}_A8_RESEARCH_PLAN.json"
   DO NOT return the file contents.
   ```

3. **Wait for subagent completion**

4. **Verify output file exists:** `ls -la analyses/{RUN_ID}/04_RQ/{TICKER}_A8_RESEARCH_PLAN.json`

---

#### Stage 2: A.8 Validation

1. **Spawn Opus validator:**
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

   === OUTPUT INSTRUCTION (Direct-Write Protocol) ===
   After completing your research, use the Write tool to save your report to:
   analyses/{RUN_ID}/04_RQ/RQ{N}_{Topic}.md

   After writing the file, return ONLY: "Complete. File: analyses/{RUN_ID}/04_RQ/RQ{N}_{Topic}.md"
   DO NOT return the file contents.
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
- CAPY: RUN ENRICH_STAGE (Bayesian synthesis)
- Or manually proceed to SCENARIO stage
```

---

### CAPY: RUN ENRICH_STAGE

**Executes the full ENRICH pipeline (T1 → Validation → T2 → Validation) for Bayesian synthesis of research results.**

```
┌─────────────────────────────────────────────────────────────┐
│  CAPY: RUN ENRICH_STAGE                                      │
├─────────────────────────────────────────────────────────────┤
│  1. ENRICH_T1 (Opus subagent)                                │
│     └── Synthesize RQ evidence into GIM refinements          │
│     └── Validate (Opus) → FAIL? Stop. PASS/WARN? ↓          │
│                                                              │
│  2. ENRICH_T2 (Opus subagent with Bash kernel execution)     │
│     └── Extract artifacts, execute kernel via Bash           │
│     └── Validate (Opus) → Report final status                │
│                                                              │
│  3. Package outputs to 05_ENRICH/                            │
└─────────────────────────────────────────────────────────────┘
```

**Prerequisites:**
- BASE_PIPELINE complete (`completed_turns` includes T1, REFINE, T2)
- RQ_STAGE complete (A.8 + 7 RQ outputs exist in `04_RQ/`: RQ1, RQ2, RQ3a, RQ3b, RQ4, RQ5, RQ6)
- A.7 artifact exists with State 1 IVPS

---

#### Stage 0: Source Discovery (Pattern 10)

**For cold-start invocation (e.g., "Do ENRICH on DAVE"):**

1. **Find candidate runs:**
   ```
   find analyses/ -name "*{TICKER}*" -type d | sort -r | head -5
   ```

2. **Identify most recent COMPLETE run** (must have all required artifacts):
   - `02_REFINE/{TICKER}_BASE_REFINE.md` (A.1-A.6)
   - `03_T2/{TICKER}_BASE_T2.md` or kernel output (A.7 with IVPS)
   - `04_RQ/RQ*.md` (7 research outputs)

3. **READ and validate** (not just list):
   - Extract State 1 IVPS from A.7 or kernel output JSON
   - Log: "Source: {RUN_ID}, State 1 IVPS: ${value}, DR: {value}%"

4. **Set RUN_ID** from discovered folder, proceed to Stage 1.

**If bridge prompt specifies source folder:** Use that folder (still validate with READ).
**If no complete run found:** HALT, report to user.

---

#### Stage 1: ENRICH_T1

**CRITICAL: Orchestrator MUST embed all required artifacts. Subagent reads RQ outputs from disk.**

The T1 subagent performs Bayesian synthesis of research evidence to refine the GIM. It does NOT compute IVPS (that's kernel work in T2).

1. **Create output directory:**
   ```
   mkdir -p analyses/{RUN_ID}/05_ENRICH/
   ```

2. **Orchestrator reads and embeds these files:**
   - `prompts/enrich/G3ENRICH_2.2.2e_PROMPT.md` (core instructions)
   - `prompts/enrich/G3ENRICH_2.2.2e_SCHEMAS.md` (JSON schemas)
   - `prompts/enrich/G3ENRICH_2.2.2e_NORMDEFS.md` (DSL definitions)
   - `kernels/CVR_KERNEL_ENRICH_2.2.2e.py` (kernel - T1 uses for reference context, T2 executes via Bash)
   - `02_REFINE/{TICKER}_BASE_REFINE.md` (contains A.1-A.6 with complete GIM/DAG - THE SOURCE OF TRUTH)
   - `03_T2/{TICKER}_BASE_T2.md` (contains A.7 with State 1 IVPS)
   - `04_RQ/{TICKER}_A8_RESEARCH_PLAN.json` (research strategy map)

3. **Spawn Opus subagent** (Task tool, subagent_type: "general-purpose"):
   ```
   You are executing CAPY ENRICHMENT Turn 1.

   === G3ENRICH PROMPT (FOLLOW THIS EXACTLY) ===
   [FULL contents of G3ENRICH_2.2.2e_PROMPT.md - orchestrator embeds]

   === SCHEMAS (APPENDIX A) ===
   [FULL contents of G3ENRICH_2.2.2e_SCHEMAS.md - orchestrator embeds]

   === NORMATIVE DEFINITIONS (APPENDIX B) ===
   [FULL contents of G3ENRICH_2.2.2e_NORMDEFS.md - orchestrator embeds]

   === BASE ARTIFACTS (A.1-A.6, Complete GIM/DAG) ===
   [FULL contents of 02_REFINE/{TICKER}_BASE_REFINE.md - orchestrator embeds]
   ^^^ THIS IS THE SOURCE OF TRUTH FOR ALL DRIVERS ^^^

   === BASE A.7 (State 1 IVPS) ===
   [FULL contents of 03_T2/{TICKER}_BASE_T2.md - orchestrator embeds]
   ^^^ USE THIS FOR STATE 1 IVPS BASELINE ^^^

   === A.8 RESEARCH STRATEGY MAP ===
   [FULL contents of 04_RQ/{TICKER}_A8_RESEARCH_PLAN.json - orchestrator embeds]

   === RQ RESEARCH OUTPUTS ===
   Read ALL research output files from: analyses/{RUN_ID}/04_RQ/RQ*.md
   Use the Read tool to load each file yourself. These contain:
   - RQ1 (M-1): Integrity Check
   - RQ2 (M-2): Adversarial Synthesis
   - RQ3a (M-3a): Mainline Scenarios H.A.D.
   - RQ3b (M-3b): Tail Scenarios H.A.D.
   - RQ4 (D-1): Lynchpin L1 deep dive
   - RQ5 (D-2): Lynchpin L2 deep dive
   - RQ6 (D-3): Lynchpin L3 deep dive

   === TRIGGER ===
   Execute ENRICHMENT Turn 1 for {COMPANY_NAME} ({TICKER}).
   Synthesize research evidence into GIM refinements per the protocol.

   === OUTPUT INSTRUCTION (Direct-Write Protocol) ===
   Use the Write tool to save your complete output to:
   analyses/{RUN_ID}/05_ENRICH/{TICKER}_ENRICH_T1.md

   Your output MUST include:
   1. Narratives N1-N5 (Investment Thesis, IC Modeling, Economic Governor, Risk Assessment, Enrichment Synthesis)
   2. JSON artifacts A.1, A.2, A.3, A.5, A.6 (updated or pass-through with valid JSON)
   3. A.9_ENRICHMENT_TRACE (full audit trail of refinements)

   DO NOT compute IVPS. That happens in Turn 2 via kernel execution.
   DO NOT emit A.7 - that is T2's responsibility.

   After writing the file, return ONLY: "Complete. File: analyses/{RUN_ID}/05_ENRICH/{TICKER}_ENRICH_T1.md"
   DO NOT return the file contents.
   ```

4. **Wait for subagent completion** - subagent returns confirmation + filepath only

5. **Verify output file exists:** `ls -la analyses/{RUN_ID}/05_ENRICH/{TICKER}_ENRICH_T1.md`

6. **Run validator** (Task tool, subagent_type: "general-purpose", model: **opus**):
   ```
   You are the CAPY inter-turn validator.

   === VALIDATOR PROMPT ===
   [FULL contents of validators/CAPY_INTERTURN_VALIDATOR_CC.md]

   === STAGE ===
   ENRICH_T1

   === OUTPUT TO VALIDATE ===
   [FULL contents of 05_ENRICH/{TICKER}_ENRICH_T1.md]

   Return ONLY the JSON validation result.
   ```

7. **Process validation result:**
   - Write to: `05_ENRICH/{TICKER}_ENRICH_T1_validation.json`
   - If `"proceed": false` → **HALT pipeline**, report issues to user
   - If `"proceed": true` → Continue to Stage 2

8. **Update state:**
   - Add "ENRICH_T1" to `completed_turns`
   - Set `current_turn: "ENRICH_T2"`

---

#### Stage 2: ENRICH_T2

**CRITICAL: Subagent MUST execute kernel via Bash. DO NOT compute IVPS manually.**

The T2 subagent extracts artifacts from T1, runs the Python kernel via Bash, and formats the output. This pattern provides context isolation while ensuring deterministic kernel execution.

1. **Spawn Opus subagent** (Task tool, subagent_type: "general-purpose"):
   ```
   You are executing CAPY ENRICHMENT Turn 2.

   YOUR JOB IS KERNEL EXECUTION, NOT ANALYSIS.

   === STEP 1: READ T1 OUTPUT ===
   Read: analyses/{RUN_ID}/05_ENRICH/{TICKER}_ENRICH_T1.md

   === STEP 2: EXTRACT ARTIFACTS ===
   Extract these JSON blocks from T1 and save to individual files:
   - A.2_ANALYTIC_KG → analyses/{RUN_ID}/05_ENRICH/A2_ANALYTIC_KG.json
   - A.3_CAUSAL_DAG → analyses/{RUN_ID}/05_ENRICH/A3_CAUSAL_DAG.json
   - A.5_GESTALT_IMPACT_MAP → analyses/{RUN_ID}/05_ENRICH/A5_GESTALT_IMPACT_MAP.json
   - A.6_DR_DERIVATION_TRACE → analyses/{RUN_ID}/05_ENRICH/A6_DR_DERIVATION_TRACE.json

   Use the Write tool to save each JSON file.

   === STEP 3: EXECUTE KERNEL VIA BASH ===
   **YOU MUST USE THE BASH TOOL. DO NOT COMPUTE IVPS YOURSELF.**

   Run this command:
   python -c "
   import json
   import importlib.util

   spec = importlib.util.spec_from_file_location(
       'kernel', 'kernels/CVR_KERNEL_ENRICH_2.2.2e.py')
   kernel = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(kernel)

   kg = json.load(open('analyses/{RUN_ID}/05_ENRICH/A2_ANALYTIC_KG.json'))
   dag = json.load(open('analyses/{RUN_ID}/05_ENRICH/A3_CAUSAL_DAG.json'))
   gim = json.load(open('analyses/{RUN_ID}/05_ENRICH/A5_GESTALT_IMPACT_MAP.json'))
   dr = json.load(open('analyses/{RUN_ID}/05_ENRICH/A6_DR_DERIVATION_TRACE.json'))

   result = kernel.execute_cvr_workflow(kg, dag, gim, dr, [
       {'driver': 'MTM_Growth_Rate', 'low': -0.20, 'high': 0.20},
       {'driver': 'Gross_Profit_Margin', 'low': -0.10, 'high': 0.10},
       {'driver': 'ARPU_Growth_Rate', 'low': -0.20, 'high': 0.20},
       {'driver': 'Opex_ex_Variable_Pct', 'low': -0.10, 'high': 0.10},
       {'driver': 'Discount_Rate', 'low': -0.01, 'high': 0.01}
   ])

   json.dump(result, open('analyses/{RUN_ID}/05_ENRICH/A7_kernel_output.json', 'w'), indent=2)
   print(json.dumps(result, indent=2))
   "

   === STEP 4: FORMAT T2 OUTPUT ===
   Read the kernel output JSON. Create T2 markdown document with:
   - Execution summary (kernel version, status)
   - State 1 vs State 2 IVPS comparison table
   - Sensitivity analysis (tornado chart from kernel output)
   - Terminal driver values
   - A.7_LIGHTWEIGHT_VALUATION_SUMMARY (embed the full JSON)

   Use the Write tool to save to: analyses/{RUN_ID}/05_ENRICH/{TICKER}_ENRICH_T2.md

   === STEP 5: RETURN CONFIRMATION ===
   Return ONLY: "Complete. File: analyses/{RUN_ID}/05_ENRICH/{TICKER}_ENRICH_T2.md"

   === PROHIBITED ===
   - DO NOT calculate IVPS yourself
   - DO NOT invent kernel output
   - If Bash fails, report the error - do not fabricate results
   ```

2. **Wait for subagent completion** - subagent returns confirmation + filepath only

3. **Verify output file exists:** `ls -la analyses/{RUN_ID}/05_ENRICH/{TICKER}_ENRICH_T2.md`

4. **Run validator** (Task tool, subagent_type: "general-purpose", model: **opus**):
   ```
   You are the CAPY inter-turn validator.

   === VALIDATOR PROMPT ===
   [FULL contents of validators/CAPY_INTERTURN_VALIDATOR_CC.md]

   === STAGE ===
   ENRICH_T2

   === OUTPUT TO VALIDATE ===
   [FULL contents of 05_ENRICH/{TICKER}_ENRICH_T2.md]

   === KERNEL OUTPUT ===
   [FULL contents of 05_ENRICH/A7_kernel_output.json]

   Verify:
   1. A.7 exists with valid IVPS
   2. Terminal g < DR
   3. IVPS > 0 and reasonable
   4. Kernel output matches T2 document

   Return ONLY the JSON validation result.
   ```

5. **Process validation result:**
   - Write to: `05_ENRICH/{TICKER}_ENRICH_T2_validation.json`
   - If `"proceed": false` → **HALT pipeline**, report issues to user
   - If `"proceed": true` → Continue to completion

6. **Update state:**
   - Add "ENRICH_T2" to `completed_turns`
   - Record State 2 IVPS in pipeline_state.json:
     ```json
     {
       "enrich_results": {
         "state_1_ivps": <from BASE>,
         "state_2_ivps": <from kernel>,
         "delta_percent": <calculated>
       }
     }
     ```

---

#### ENRICH Stage Completion

Report summary to user:

```
ENRICH_STAGE complete for {TICKER}

Run ID: {RUN_ID}

Stage Results:
├── ENRICH_T1: {PASS/WARN/FAIL}
└── ENRICH_T2: {PASS/WARN/FAIL}

Valuation Summary:
├── State 1 IVPS (BASE):   ${base_ivps}
├── State 2 IVPS (ENRICH): ${enrich_ivps}
└── Delta:                 {percentage}%

Key GIM Refinements:
├── {Driver 1}: {prior} → {posterior} ({direction})
├── {Driver 2}: {prior} → {posterior} ({direction})
└── {Driver 3}: {prior} → {posterior} ({direction})

DR Status: {CONFIRMED at X% | REVISED from X% to Y%}

Outputs:
├── 05_ENRICH/{TICKER}_ENRICH_T1.md
├── 05_ENRICH/{TICKER}_ENRICH_T2.md
├── 05_ENRICH/{TICKER}_ENRICH_kernel_output.json
└── 05_ENRICH/{TICKER}_A9_ENRICHMENT_TRACE.json

Next steps:
- Review ENRICH outputs and A.9 trace
- CAPY: RUN SCENARIO_STAGE (discrete scenario modeling)
- Or proceed to Silicon Council deliberation
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

5. **RUN VALIDATOR** (subagent_type: "general-purpose", model: opus):
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

**CRITICAL: Subagent executes kernel via Bash. Direct-write to disk.**

Spawn Opus subagent with the prompt from Stage 3: BASE_T2 above.

The subagent will:
1. Read REFINE output
2. Extract and validate JSON artifacts (repair if malformed)
3. Execute kernel via Bash
4. Format and write T2 output to disk
5. Return confirmation + filepath only

Then run validator and update pipeline state.

**See Stage 3: BASE_T2 in CAPY: RUN BASE_PIPELINE for full subagent prompt.**

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
- All stages: Use **Opus** (consistency with analytical subagents; Haiku misses subtle fabrication issues)

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

> **This CLAUDE.md is v0.5.0 (DRAFT)**

Current status: BASE_PIPELINE, RQ_STAGE, and ENRICH_STAGE documented. T1 stages work via Opus subagent dispatch. T2 stages require orchestrator-direct kernel execution (subagents fabricate results). RQ_STAGE uses 7 parallel Claude Opus subagents with direct-write protocol. All validators use Opus for consistency.

Before v1.0:
- [x] Full smoke test of CC-enabled CAPY production run (2024-12-16, DAVE)
- [x] Build out complete instructions for BASE pipeline stages (T1, REFINE, T2)
- [x] Document inter-turn validator integration
- [x] Validate subagent dispatch patterns work end-to-end (T1, REFINE: yes; T2: no)
- [x] Document error handling and recovery procedures
- [x] Document RQ_STAGE with 7-slot architecture (2024-12-19)
- [x] RQ_STAGE smoke test (DAVE, 7 parallel subagents, ~220K words output)
- [x] Document ENRICH_STAGE with 4-file atomization (2024-12-19)
- [ ] ENRICH_STAGE smoke test
- [ ] Test COMPARE RUNS functionality
- [ ] Add remaining pipeline stages (SCENARIO, INT, IRR)
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
