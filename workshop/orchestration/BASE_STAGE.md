# BASE Stage Orchestration

> **Version:** 1.0.0
> **Extracted from:** workshop/CLAUDE.md v0.12.1
> **Pipeline Position:** Stage 1 of 8 (SOURCE → BASE)

---

## BASE Stage Orchestration (SOURCE → BASE)

The BASE stage transforms raw source documents (10-Ks, 10-Qs, transcripts, presentations) into State 1: the foundational Company Valuation Report with epistemic anchors, causal structure, financial model, and initial valuation.

### Architecture (v2.2.3e - EXPERIMENTAL)

**Three-Shot Execution:**

| Turn | Name | Purpose | Key Output |
|------|------|---------|------------|
| T1 | Analytical | Extract facts, build causal structure, draft model | A.1-A.6, N1-N4 (embedded in T1.md) |
| REFINE | Calibration | Y0 calibration, DAG validation, equity bridge check | Refined A.1-A.6 (standalone JSON) |
| T2 | Computational | Kernel execution via Bash (Pattern 6) | A.7 + T2.md |

**Key Design Decisions:**
- **Three-shot not two-shot:** REFINE is interposed to calibrate model before kernel
- **Pattern 2 (Source Chain):** REFINE is source of truth for A.1-A.6, not T1
- **Equity Bridge preservation:** REFINE must preserve FDSO, Total_Debt, Excess_Cash, Minority_Interest
- **No WebSearch in BASE:** Market price fetched later in IRR stage

### Directory Structure

**Canonical Snapshot (Pattern 12):** After BASE T2, 03_T2/ contains complete State 1 artifacts.

```
{analysis_dir}/
├── 00_source/                               ← Input: preprocessed source docs
│   ├── {TICKER}_10K_2024.extracted.md
│   ├── {TICKER}_10Q_Q3_2024.extracted.md
│   ├── {TICKER}_earnings_call_Q3.extracted.md
│   └── {TICKER}_investor_deck.extracted.md
│
├── 01_T1/                                   ← BASE T1 outputs
│   ├── {TICKER}_BASE_T1_AUDIT.md                (T1 narrative - human audit only)
│   └── (artifacts embedded in T1.md, extracted by REFINE)
│
├── 02_REFINE/                               ← REFINE outputs (SOURCE OF TRUTH)
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_BASE.json  (refined)
│   ├── {TICKER}_A2_ANALYTIC_KG_BASE.json        (refined)
│   ├── {TICKER}_A3_CAUSAL_DAG_BASE.json         (refined, ≤15 nodes)
│   ├── {TICKER}_A5_GIM_BASE.json                (refined, Y0 calibrated)
│   ├── {TICKER}_A6_DR_BASE.json                 (refined)
│   ├── {TICKER}_N1_THESIS_BASE.md               (refined)
│   ├── {TICKER}_N2_IC_BASE.md                   (refined)
│   ├── {TICKER}_N3_ECON_GOV_BASE.md             (refined)
│   ├── {TICKER}_N4_RISK_BASE.md                 (refined)
│   └── {TICKER}_REFINE_AUDIT.md                 (calibration log - human audit)
│
├── 03_T2/                                   ← BASE T2 outputs (canonical State 1)
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_BASE.json  (COPIED from REFINE)
│   ├── {TICKER}_A2_ANALYTIC_KG_BASE.json        (COPIED from REFINE)
│   ├── {TICKER}_A3_CAUSAL_DAG_BASE.json         (COPIED from REFINE)
│   ├── {TICKER}_A5_GIM_BASE.json                (COPIED from REFINE)
│   ├── {TICKER}_A6_DR_BASE.json                 (COPIED from REFINE)
│   ├── {TICKER}_A7_VALUATION_BASE.json          (NEW - T2 kernel output)
│   ├── {TICKER}_N1_THESIS_BASE.md               (COPIED from REFINE)
│   ├── {TICKER}_N2_IC_BASE.md                   (COPIED from REFINE)
│   ├── {TICKER}_N3_ECON_GOV_BASE.md             (COPIED from REFINE)
│   ├── {TICKER}_N4_RISK_BASE.md                 (COPIED from REFINE)
│   ├── {TICKER}_KERNEL_RECEIPT_BASE.json        (NEW - Pattern 13)
│   └── {TICKER}_BASE_T2_AUDIT.md                (human audit only)
│
└── pipeline_state.json
```

**Copy-Forward Protocol (Orchestrator executes BEFORE RQ stage):**
```bash
mkdir -p {analysis_dir}/04_RQ

# Copy all BASE artifacts from 03_T2/ with suffix rename
for f in {analysis_dir}/03_T2/{TICKER}_*_BASE.json; do
  base=$(basename "$f" | sed 's/_BASE\.json$//')
  cp "$f" "{analysis_dir}/04_RQ/${base}_RQ.json"
done

for f in {analysis_dir}/03_T2/{TICKER}_*_BASE.md; do
  base=$(basename "$f" | sed 's/_BASE\.md$//')
  cp "$f" "{analysis_dir}/04_RQ/${base}_RQ.md"
done
```

### Stage Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 0: SOURCE VALIDATION                                                   │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Verify source documents exist and are preprocessed                    │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ Check source_library/{TICKER}/ for:                                         │
│   - *.extracted.md files (preprocessed PDFs)                                │
│   - If missing: run SOURCE: UPLOAD {TICKER} first                           │
│                                                                             │
│ Create analysis folder:                                                     │
│   mkdir -p smoke_tests/{TICKER}_SMOKE_{TIMESTAMP}/00_source                 │
│   cp source_library/{TICKER}/*.extracted.md 00_source/                      │
│                                                                             │
│ Set {analysis_dir} to the new folder.                                       │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: BASE T1 — ANALYTICAL                                                │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to extract facts and build initial model          │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/base/G3BASE_2.2.3e_PROMPT.md                                   │
│   2. prompts/base/G3BASE_2.2.3e_SCHEMAS.md                                  │
│   3. prompts/base/G3BASE_2.2.3e_NORMDEFS.md                                 │
│   4. kernels/BASE_CVR_KERNEL_2.2.3e.py (FOR CONTEXT ONLY - DO NOT EXECUTE)  │
│                                                                             │
│ INPUT FILES TO ATTACH:                                                      │
│   • All files from {analysis_dir}/00_source/*.extracted.md                  │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute BASE Turn 1 for {TICKER}.                                        │
│                                                                             │
│    Your analytical tasks:                                                   │
│    1. Extract epistemic anchors from source documents (A.1)                 │
│    2. Build Analytic Knowledge Graph with causal relationships (A.2)        │
│    3. Construct Causal DAG with ≤15 nodes (A.3)                             │
│    4. Build Gestalt Impact Map (GIM) with 5-year forecast (A.5)             │
│    5. Derive Discount Rate using B.3 rubric (A.6)                           │
│    6. Write narratives N1-N4 (Thesis, IC, Economic Governor, Risk)          │
│                                                                             │
│    DO NOT execute the kernel. It is provided for context only.              │
│                                                                             │
│    Write output to {analysis_dir}/01_T1/:                                   │
│    1. {TICKER}_BASE_T1_AUDIT.md (full reasoning + embedded artifacts)       │
│                                                                             │
│    Return confirmation and filepath written."                               │
│                                                                             │
│ OUTPUT PRODUCED:                                                            │
│   • {TICKER}_BASE_T1_AUDIT.md - Complete T1 output with embedded artifacts  │
│                                                                             │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns path   │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: BASE T1 VALIDATOR                                                   │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate T1 output                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/BASE_T1_VALIDATOR.md                                           │
│                                                                             │
│ INPUT FILES:                                                                │
│   • {analysis_dir}/01_T1/{TICKER}_BASE_T1_AUDIT.md                          │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • A.1-A.6 present and extractable                                         │
│   • A.3 DAG has ≤15 nodes                                                   │
│   • A.5 GIM has 5-year forecast with required rows                          │
│   • A.6 DR in reasonable range (8-18% typically)                            │
│   • N1-N4 narratives present                                                │
│   • Equity Bridge items present (FDSO, Total_Debt, Excess_Cash)             │
│                                                                             │
│ IF FAIL: Stop. Report issues. Do not proceed to REFINE.                     │
│ IF PASS: Proceed to Step 3.                                                 │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │ (proceed only if PASS)
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: BASE REFINE — CALIBRATION                                           │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to calibrate model and extract standalone JSONs   │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE TO ATTACH:                                                      │
│   prompts/refine/BASE_T1_REFINE_v1_3.md                                     │
│                                                                             │
│ INPUT FILES TO ATTACH:                                                      │
│   • {analysis_dir}/01_T1/{TICKER}_BASE_T1_AUDIT.md                          │
│   • {analysis_dir}/00_source/*.extracted.md (for Y0 verification)           │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute BASE REFINE for {TICKER}.                                        │
│                                                                             │
│    CRITICAL: REFINE is the SOURCE OF TRUTH for A.1-A.6 (Pattern 2).         │
│    T1 artifacts are drafts; REFINE outputs are canonical.                   │
│                                                                             │
│    Your calibration tasks:                                                  │
│    1. Extract A.1-A.6 from T1 into standalone JSON files                    │
│    2. Y0 Calibration: Verify model Y0 matches reported financials (±2%)     │
│    3. DAG Validation: Ensure ≤15 nodes, no orphans, coherent structure      │
│    4. Equity Bridge Check: Preserve FDSO, Total_Debt, Excess_Cash,          │
│       Minority_Interest unchanged from T1                                   │
│    5. Extract N1-N4 narratives into standalone markdown files               │
│                                                                             │
│    Write ALL output files to {analysis_dir}/02_REFINE/:                     │
│    1. {TICKER}_A1_EPISTEMIC_ANCHORS_BASE.json                               │
│    2. {TICKER}_A2_ANALYTIC_KG_BASE.json                                     │
│    3. {TICKER}_A3_CAUSAL_DAG_BASE.json                                      │
│    4. {TICKER}_A5_GIM_BASE.json                                             │
│    5. {TICKER}_A6_DR_BASE.json                                              │
│    6. {TICKER}_N1_THESIS_BASE.md                                            │
│    7. {TICKER}_N2_IC_BASE.md                                                │
│    8. {TICKER}_N3_ECON_GOV_BASE.md                                          │
│    9. {TICKER}_N4_RISK_BASE.md                                              │
│   10. {TICKER}_REFINE_AUDIT.md (calibration log)                            │
│                                                                             │
│    Return confirmation and list of filepaths written."                      │
│                                                                             │
│ OUTPUT PRODUCED (10 files):                                                 │
│   • {TICKER}_A1-A6_BASE.json - Standalone refined artifacts                 │
│   • {TICKER}_N1-N4_BASE.md - Standalone refined narratives                  │
│   • {TICKER}_REFINE_AUDIT.md - Calibration log (human audit)                │
│                                                                             │
│ PATTERN: Source Chain (Pattern 2) - REFINE outputs are source of truth      │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns paths  │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: BASE REFINE VALIDATOR                                               │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate REFINE output                         │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/BASE_REFINE_VALIDATOR.md                                       │
│                                                                             │
│ INPUT FILES (verify ALL 10 exist in 02_REFINE/):                            │
│   {analysis_dir}/02_REFINE/{TICKER}_A1_EPISTEMIC_ANCHORS_BASE.json          │
│   {analysis_dir}/02_REFINE/{TICKER}_A2_ANALYTIC_KG_BASE.json                │
│   {analysis_dir}/02_REFINE/{TICKER}_A3_CAUSAL_DAG_BASE.json                 │
│   {analysis_dir}/02_REFINE/{TICKER}_A5_GIM_BASE.json                        │
│   {analysis_dir}/02_REFINE/{TICKER}_A6_DR_BASE.json                         │
│   {analysis_dir}/02_REFINE/{TICKER}_N1_THESIS_BASE.md                       │
│   {analysis_dir}/02_REFINE/{TICKER}_N2_IC_BASE.md                           │
│   {analysis_dir}/02_REFINE/{TICKER}_N3_ECON_GOV_BASE.md                     │
│   {analysis_dir}/02_REFINE/{TICKER}_N4_RISK_BASE.md                         │
│   {analysis_dir}/02_REFINE/{TICKER}_REFINE_AUDIT.md                         │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • ALL 10 REFINE OUTPUT FILES EXIST (block T2 if any missing)              │
│   • Y0 calibration within ±2% for Revenue, EBIT, IC                         │
│   • DAG has ≤15 nodes                                                       │
│   • Equity Bridge preserved: FDSO, Total_Debt, Excess_Cash, Minority_Int    │
│   • JSON files are valid and contain required fields                        │
│                                                                             │
│ IF FAIL: Stop. Report issues. Do not proceed to T2.                         │
│ IF PASS: Proceed to Step 5.                                                 │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │ (proceed only if PASS)
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 5: BASE T2 — COMPUTATIONAL (KERNEL EXECUTION)                          │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to execute kernel and produce A.7                 │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/base/G3BASE_2.2.3e_PROMPT.md (T2 section only)                 │
│   2. kernels/BASE_CVR_KERNEL_2.2.3e.py (EXECUTABLE)                         │
│                                                                             │
│ INPUT FILES TO ATTACH (from 02_REFINE/):                                    │
│   • {analysis_dir}/02_REFINE/{TICKER}_A5_GIM_BASE.json                      │
│   • {analysis_dir}/02_REFINE/{TICKER}_A6_DR_BASE.json                       │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute BASE Turn 2 for {TICKER}.                                        │
│                                                                             │
│    CRITICAL: Manual calculation is PROHIBITED. You MUST use Bash kernel.    │
│    CRITICAL: T2 performs NO reasoning. All judgment is locked in REFINE.    │
│                                                                             │
│    1. Validate A.5 and A.6 are well-formed (repair if needed - Pattern 5)   │
│    2. Execute kernel via Bash (Pattern 6):                                  │
│                                                                             │
│       python3 kernels/BASE_CVR_KERNEL_2.2.3e.py \                           │
│         --a5 {TICKER}_A5_GIM_BASE.json \                                    │
│         --a6 {TICKER}_A6_DR_BASE.json \                                     │
│         --output {TICKER}_A7_VALUATION_BASE.json                            │
│                                                                             │
│    3. Generate kernel receipt (Pattern 13):                                 │
│       Write {TICKER}_KERNEL_RECEIPT_BASE.json with:                         │
│       - kernel file, version, sha256                                        │
│       - input filenames                                                     │
│       - command executed                                                    │
│       - exit_code, execution_time_seconds                                   │
│                                                                             │
│    4. Copy REFINE artifacts to 03_T2/ with _BASE suffix (already there)     │
│                                                                             │
│    Write output files to {analysis_dir}/03_T2/:                             │
│    1. {TICKER}_A7_VALUATION_BASE.json (kernel output)                       │
│    2. {TICKER}_KERNEL_RECEIPT_BASE.json (execution proof)                   │
│    3. {TICKER}_BASE_T2_AUDIT.md (human audit only)                          │
│    + Copy A.1-A.6, N1-N4 from 02_REFINE/ to 03_T2/                          │
│                                                                             │
│    Return confirmation and filepaths."                                      │
│                                                                             │
│ OUTPUT PRODUCED:                                                            │
│   • {TICKER}_A7_VALUATION_BASE.json - Kernel output (E[IVPS], terminal g)   │
│   • {TICKER}_KERNEL_RECEIPT_BASE.json - Execution proof (Pattern 13)        │
│   • {TICKER}_BASE_T2_AUDIT.md - Human audit only                            │
│   • All REFINE artifacts copied to 03_T2/ (canonical State 1 snapshot)      │
│                                                                             │
│ PATTERN: Bash Kernel (Pattern 6) - execute kernel via Bash, not manual calc │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns paths  │
│ PATTERN: Kernel Receipts (Pattern 13) - verifiable proof of execution       │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 6: BASE T2 VALIDATOR                                                   │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate T2 output                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/BASE_T2_VALIDATOR.md                                           │
│                                                                             │
│ INPUT FILES:                                                                │
│   • {analysis_dir}/03_T2/{TICKER}_A7_VALUATION_BASE.json                    │
│   • {analysis_dir}/03_T2/{TICKER}_KERNEL_RECEIPT_BASE.json                  │
│   • {analysis_dir}/03_T2/{TICKER}_A5_GIM_BASE.json (cross-validate)         │
│   • {analysis_dir}/03_T2/{TICKER}_A6_DR_BASE.json (cross-validate)          │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • A.7 schema compliance                                                   │
│   • Kernel receipt exists (Pattern 13: exit_code=0, timing present)         │
│   • Values have 4+ decimal precision (proves real execution)                │
│   • E[IVPS] is positive and economically sensible                           │
│   • Terminal g < DR (perpetuity validity)                                   │
│   • All 10 artifacts (A.1-A.7, N1-N4) present in 03_T2/                     │
│                                                                             │
│ IF FAIL: Report issues. May need T2 re-execution.                           │
│ IF PASS: BASE stage complete. CVR is now State 1.                           │
│          Proceed to RQ stage with copy-forward to 04_RQ/.                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Execution Commands (DEV: SMOKE TEST BASE {TICKER})

**Step 0: Validate Source Documents**
```bash
# Check source docs exist
ls source_library/{TICKER}/

# Create analysis folder
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p smoke_tests/{TICKER}_SMOKE_${TIMESTAMP}/00_source
cp source_library/{TICKER}/*.extracted.md smoke_tests/{TICKER}_SMOKE_${TIMESTAMP}/00_source/

# Set analysis_dir
export ANALYSIS_DIR="smoke_tests/{TICKER}_SMOKE_${TIMESTAMP}"
```

**Steps 1-6: Spawn Subagents**
Use Task tool with model="opus" for each step. See Stage Flow above for exact prompts and inputs.

### Critical Patterns Applied

| Pattern | Application |
|---------|-------------|
| Pattern 1: Direct-Write | All subagents write to disk, return filepath only |
| Pattern 2: Source Chain | REFINE is source of truth for A.1-A.6, not T1 |
| Pattern 3: Two-Shot (Extended) | T1=analytical, REFINE=calibration, T2=kernel |
| Pattern 5: JSON Repair | T2 can repair malformed REFINE JSON before kernel |
| Pattern 6: Bash Kernel | T2 executes BASE_CVR_KERNEL via Bash |
| Pattern 7: Validators | Opus validator after T1, REFINE, AND T2 |
| Pattern 8: Atomized Prompts | 3 files (PROMPT/SCHEMAS/NORMDEFS) + kernel |
| Pattern 12: Canonical Snapshot | 03_T2/ contains complete State 1 with _BASE suffix |
| Pattern 13: Kernel Receipts | T2 generates {TICKER}_KERNEL_RECEIPT_BASE.json |

### BASE Stage Atomized Files (EXPERIMENTAL)

The BASE prompt v2.2.3e is split into 3 atomic files for improved context management:

| File | Purpose | Size | Changes in 2.2.3e |
|------|---------|------|-------------------|
| `G3BASE_2.2.3e_PROMPT.md` | Core instructions (Sections I-V) | ~18KB | Currency detection, kernel receipts |
| `G3BASE_2.2.3e_SCHEMAS.md` | JSON schemas (Appendix A) | ~10KB | ROIC_anchor, currency fields |
| `G3BASE_2.2.3e_NORMDEFS.md` | DSL definitions (Appendix B) | ~6KB | DR global calibration |
| `BASE_CVR_KERNEL_2.2.3e.py` | Valuation kernel | ~33KB | Terminal g from topline growth |

**Status:** EXPERIMENTAL - pending smoke test. G3BASE_2.2.2e remains CANONICAL until smoke test passes.

**Subagent loading:** Load all 3 prompt files + kernel reference. The embedded kernel (old Appendix C) has been removed.

---

