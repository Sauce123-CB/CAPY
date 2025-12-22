# INTEGRATION Stage Orchestration

> **Version:** 1.0.0
> **Extracted from:** workshop/CLAUDE.md v0.12.1
> **Pipeline Position:** Stage 7 of 8 (SILICON COUNCIL → INTEGRATION)

---

## INTEGRATION Stage Orchestration (SILICON COUNCIL → INTEGRATION)

### Purpose and Context

The INTEGRATION stage is the **final analytical stage** of the CAPY pipeline. It transitions the CVR from State 3 (Probabilistic) to State 4 (Finalized).

**What happened before INTEGRATION:**
1. **ENRICH** produced a deterministic intrinsic value per share (IVPS) calculation with artifacts A.1-A.9
2. **SCENARIO** added probabilistic scenario analysis on top, producing A.10 with E[IVPS] and distribution
3. **SILICON COUNCIL** audited both stages across 6 dimensions, producing A.11 audit reports

**What INTEGRATION does:**
1. **T1 (Adjudication):** Receives ALL upstream artifacts + ALL audit findings. Adjudicates each audit finding (ACCEPT/REJECT/MODIFY) against primary evidence. Determines what needs recalculation.
2. **T2 (Recalculation):** Executes kernel if any modifications were accepted. Produces finalized artifacts with amendments applied.
3. **T3 (Final Output):** Produces the **complete, clean, finalized CVR** - all narratives, all artifacts, no deprecated content. This is THE document for human review or IRR stage.

**Why Epistemic Parity matters:**
The INTEGRATION subagent must have access to the same evidence that upstream stages used. It cannot adjudicate audit findings without seeing the original source documents, RQ outputs, and analytical artifacts. This is non-negotiable.

### Architecture (v2.2.2e)

**Three-Shot Execution:**

| Turn | Name | Purpose | Key Output |
|------|------|---------|------------|
| T1 | Adjudication | Review SC findings, adjudicate against evidence | Adjudication decisions + T1 Handoff JSON |
| T2 | Recalculation | Execute kernel if cascade required | Finalized artifacts A.1-A.12 + state_4_active_inputs |
| T3 | Final Output | Produce complete CVR State 4 document | Clean, unified document with N1-N7 + A.1-A.12 |

### Directory Structure

```
{analysis_dir}/
├── 00_source/                       ← Source financials (10-K, 10-Q, transcripts)
├── 07_SILICON_COUNCIL/              ← Input: SC audit outputs + State 3 artifacts
├── 08_INTEGRATION/                  ← INTEGRATION outputs
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_INT.json   (adjudicated from SC)
│   ├── {TICKER}_A2_ANALYTIC_KG_INT.json         (adjudicated from SC)
│   ├── {TICKER}_A3_CAUSAL_DAG_INT.json          (adjudicated from SC)
│   ├── {TICKER}_A5_GIM_INT.json                 (adjudicated - kernel input)
│   ├── {TICKER}_A6_DR_INT.json                  (adjudicated - kernel input)
│   ├── {TICKER}_A7_VALUATION_INT.json           (T2 kernel output if cascade)
│   ├── {TICKER}_A10_SCENARIO_INT.json           (adjudicated - kernel input)
│   ├── {TICKER}_A11_AUDIT_INT.json              (copied from SC)
│   ├── {TICKER}_A12_CASCADE_INT.json            (NEW - cascade decision)
│   ├── {TICKER}_INT_T1_AUDIT.md                 (NEW - adjudication narrative)
│   ├── {TICKER}_INT_T2_AUDIT.md                 (NEW - recalculation narrative)
│   ├── {TICKER}_CVR_STATE4_INT.md               (NEW - final CVR State 4)
│   ├── {TICKER}_N1_THESIS_INT.md                (adjudicated if needed)
│   ├── {TICKER}_N2_IC_INT.md                    (adjudicated if needed)
│   ├── {TICKER}_N3_ECON_GOV_INT.md              (adjudicated if needed)
│   ├── {TICKER}_N4_RISK_INT.md                  (adjudicated if needed)
│   ├── {TICKER}_N5_ENRICHMENT_INT.md            (adjudicated if needed)
│   ├── {TICKER}_N6_SCENARIO_INT.md              (adjudicated if needed)
│   ├── {TICKER}_N7_ADJUDICATION_INT.md          (NEW - adjudication synthesis)
│   └── {TICKER}_KERNEL_RECEIPT_INT.json         (NEW - Pattern 13, if cascade)
├── 09_IRR/                          ← Next stage
└── PIPELINE_STATE.md
```

**Copy-Forward Protocol:** Before INTEGRATION T1, orchestrator copies SC artifacts from 07_SILICON_COUNCIL/ to 08_INTEGRATION/ with suffix rename (_SC → _INT) using `cp`. T1 then adjudicates and modifies these files in place.

### Stage Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 0: AUTO-DISCOVERY AND INPUT VALIDATION                                 │
│                                                                             │
│ Locate most recent complete pipeline run:                                   │
│   find smoke_tests/ -name "*A11*.json" | sort -r | head -5                  │
│                                                                             │
│ Verify folder contains ALL required inputs (see Step 1).                    │
│ READ key files to extract baseline metrics:                                 │
│   - E[IVPS] from A.10                                                       │
│   - Pipeline Fit grade(s) from A.11                                         │
│   - Count of CRITICAL/HIGH findings                                         │
│                                                                             │
│ Set {analysis_dir} to the pipeline run folder.                              │
│ Create 08_INTEGRATION/ if it doesn't exist.                                 │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: PREPARE EPISTEMIC PARITY BUNDLE                                     │
│                                                                             │
│ The T1 subagent MUST receive everything Silicon Council received,           │
│ PLUS the A.11 audit outputs. This is mandatory for principled adjudication. │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ SOURCE DOCUMENTS (Discovery Record)                                     │ │
│ │ Location: {analysis_dir}/00_source/ or /source_docs/                    │ │
│ │                                                                         │ │
│ │ Files:                                                                  │ │
│ │   • 10-K filing (full or extracted.md)                                  │ │
│ │   • 10-Q filings (all available quarters)                               │ │
│ │   • Earnings call transcripts                                           │ │
│ │   • Investor presentations                                              │ │
│ │   • Pre-processed financials spreadsheet                                │ │
│ │                                                                         │ │
│ │ Why needed: Primary evidence for adjudicating disputed claims.          │ │
│ │ The subagent may need to verify facts cited by SC audits.               │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ RESEARCH QUESTION OUTPUTS                                               │ │
│ │ Location: {analysis_dir}/04_RQ/                                         │ │
│ │                                                                         │ │
│ │ Files:                                                                  │ │
│ │   • RQ1_*.md through RQ7_*.md (7 research reports)                      │ │
│ │   • {TICKER}_A8_RESEARCH_PLAN.json                                      │ │
│ │   • {TICKER}_A9_RESEARCH_RESULTS.json                                   │ │
│ │                                                                         │ │
│ │ Why needed: External research that informed ENRICH/SCENARIO.            │ │
│ │ SC may have challenged assumptions based on RQ findings.                │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ ENRICH OUTPUTS (State 2 - Deterministic IVPS)                           │ │
│ │ Location: {analysis_dir}/05_ENRICH/                                     │ │
│ │                                                                         │ │
│ │ Files:                                                                  │ │
│ │   • {TICKER}_ENRICH_T1_AUDIT.md (analysis narrative)                    │ │
│ │   • {TICKER}_ENRICH_T2_AUDIT.md (kernel output narrative)               │ │
│ │   • {TICKER}_A1_EPISTEMIC_ANCHORS_ENRICH.json                           │ │
│ │   • {TICKER}_A2_ANALYTIC_KG_ENRICH.json                                 │ │
│ │   • {TICKER}_A3_CAUSAL_DAG_ENRICH.json                                  │ │
│ │   • {TICKER}_A5_GIM_ENRICH.json                                         │ │
│ │   • {TICKER}_A6_DR_ENRICH.json                                          │ │
│ │   • {TICKER}_A7_VALUATION_ENRICH.json (contains Base Case IVPS)         │ │
│ │   • {TICKER}_A9_ENRICHMENT_TRACE_ENRICH.json                            │ │
│ │                                                                         │ │
│ │ Why needed: The deterministic valuation that SCENARIO built upon.       │ │
│ │ SC may have challenged base case assumptions.                           │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ SCENARIO OUTPUTS (State 3 - Probabilistic E[IVPS])                      │ │
│ │ Location: {analysis_dir}/06_SCENARIO/                                   │ │
│ │                                                                         │ │
│ │ Files:                                                                  │ │
│ │   • {TICKER}_SCEN_T1_AUDIT.md (scenario identification narrative)       │ │
│ │   • {TICKER}_SCEN_T2_AUDIT.md (SSE execution narrative)                 │ │
│ │   • {TICKER}_A10_SCENARIO_SCEN.json (scenarios, probabilities, dist)    │ │
│ │                                                                         │ │
│ │ Why needed: The probabilistic layer that SC audited.                    │ │
│ │ SC may have challenged scenario selection, probabilities, or SSE math.  │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ SILICON COUNCIL OUTPUTS (A.11 Audit Reports)                            │ │
│ │ Location: {analysis_dir}/07_SILICON_COUNCIL/                            │ │
│ │                                                                         │ │
│ │ Files:                                                                  │ │
│ │   • {TICKER}_SC_ACCOUNTING_SC.json (source integrity findings)          │ │
│ │   • {TICKER}_SC_FIT_SC.json (pipeline fit assessment)                   │ │
│ │   • {TICKER}_SC_EPISTEMIC_SC.json (Bayesian protocol compliance)        │ │
│ │   • {TICKER}_SC_RED_TEAM_SC.json (adversarial review)                   │ │
│ │   • {TICKER}_SC_DISTRIBUTIONAL_SC.json (distribution coherence)         │ │
│ │   • {TICKER}_SC_ECONOMIC_REALISM_SC.json (top-down plausibility)        │ │
│ │   • {TICKER}_A11_AUDIT_REPORT.json (consolidated audit report)          │ │
│ │   • *.md versions of above (human-readable)                             │ │
│ │                                                                         │ │
│ │ Why needed: THE INPUT that triggers adjudication.                       │ │
│ │ Each finding must be evaluated: ACCEPT, REJECT, or MODIFY.              │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ VERIFICATION: Before proceeding, confirm ALL folders exist and contain     │
│ the expected files. Log file counts. If anything is missing, STOP.         │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: INTEGRATION T1 — ADJUDICATION                                       │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to adjudicate Silicon Council findings            │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/integration/G3_INTEGRATION_2.2.3e_PROMPT.md                    │
│   2. prompts/integration/G3_INTEGRATION_2.2.3e_SCHEMAS.md                   │
│   3. prompts/integration/G3_INTEGRATION_2.2.3e_NORMDEFS.md                  │
│   4. kernels/CVR_KERNEL_INT_2_2_2e.py (FOR CONTEXT ONLY - DO NOT EXECUTE)   │
│                                                                             │
│ INPUT FILES TO ATTACH (Full Epistemic Parity Bundle from Step 1):           │
│   • ALL source documents from 00_source/                                    │
│   • ALL RQ outputs from 04_RQ/                                              │
│   • ALL ENRICH outputs from 05_ENRICH/                                      │
│   • ALL SCENARIO outputs from 06_SCENARIO/                                  │
│   • ALL SILICON COUNCIL outputs from 07_SILICON_COUNCIL/                    │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute INTEGRATION Turn 1 for {TICKER}.                                 │
│                                                                             │
│    Your task: Adjudicate all Silicon Council findings against the           │
│    primary evidence. For each finding, determine disposition:               │
│    ACCEPT (State 3 needs modification), REJECT (State 3 stands),            │
│    or MODIFY (partial adjustment needed).                                   │
│                                                                             │
│    Execute Phases A-C per the prompt:                                       │
│    - Phase A: Initialization and Triage (dock all findings)                 │
│    - Phase B: Adjudication Loop (evaluate each finding)                     │
│    - Phase C: Scenario Reconciliation (finalize scenario set)               │
│                                                                             │
│    Then execute the SURGICAL EDIT PROTOCOL (CRITICAL):                      │
│    For each artifact (A.1, A.2, A.3, A.5, A.6, A.10):                       │
│    1. READ the State 3 version from the epistemic bundle                    │
│    2. APPLY any modifications required by your adjudication dispositions    │
│    3. WRITE the complete artifact with _S4 suffix to output_dir             │
│    If no modifications needed for an artifact, copy it unchanged.           │
│                                                                             │
│    Also extract and edit narratives N1-N6 from upstream T2 outputs.         │
│    Add [State 4: Revised per F{N}] annotations where modified.              │
│                                                                             │
│    DO NOT execute the kernel. It is provided for context only.              │
│                                                                             │
│    YOU MUST WRITE ALL OUTPUT FILES TO {analysis_dir}/08_INTEGRATION/:       │
│    1. {TICKER}_INT_T1_AUDIT.md (adjudication reasoning - human audit only)  │
│    2. {TICKER}_A1_EPISTEMIC_ANCHORS_INT.json (adjudicated)                  │
│    3. {TICKER}_A2_ANALYTIC_KG_INT.json (adjudicated)                        │
│    4. {TICKER}_A3_CAUSAL_DAG_INT.json (adjudicated)                         │
│    5. {TICKER}_A5_GIM_INT.json (adjudicated, kernel input)                  │
│    6. {TICKER}_A6_DR_INT.json (adjudicated, kernel input)                   │
│    7. {TICKER}_A10_SCENARIO_INT.json (adjudicated, kernel input)            │
│    8. {TICKER}_N1_THESIS_INT.md through {TICKER}_N7_ADJUDICATION_INT.md     │
│    9. {TICKER}_A12_CASCADE_INT.json (cascade scope + modifications)         │
│                                                                             │
│    Return confirmation and list of filepaths written."                      │
│                                                                             │
│ OUTPUT PRODUCED:                                                            │
│   • {TICKER}_INT_T1_AUDIT.md - Adjudication reasoning (human audit)         │
│   • {TICKER}_A1_EPISTEMIC_ANCHORS_INT.json - Adjudicated artifact           │
│   • {TICKER}_A2_ANALYTIC_KG_INT.json - Adjudicated artifact                 │
│   • {TICKER}_A3_CAUSAL_DAG_INT.json - Adjudicated artifact                  │
│   • {TICKER}_A5_GIM_INT.json - Adjudicated, kernel input                    │
│   • {TICKER}_A6_DR_INT.json - Adjudicated, kernel input                     │
│   • {TICKER}_A10_SCENARIO_INT.json - Adjudicated, kernel input              │
│   • {TICKER}_N1-N7_*_INT.md - Revised narratives (7 files: N1-N7)           │
│   • {TICKER}_A12_CASCADE_INT.json - Cascade scope + modifications           │
│                                                                             │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns paths │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: INTEGRATION T1 VALIDATOR                                            │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate T1 output                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/INT_T1_VALIDATOR.md                                            │
│                                                                             │
│ INPUT FILES (verify ALL exist in 08_INTEGRATION/):                          │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_INT_T1_AUDIT.md                    │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_A1_EPISTEMIC_ANCHORS_INT.json      │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_A2_ANALYTIC_KG_INT.json            │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_A3_CAUSAL_DAG_INT.json             │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_A5_GIM_INT.json                    │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_A6_DR_INT.json                     │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_A10_SCENARIO_INT.json              │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_N*_INT.md (7 narrative files)      │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_A12_CASCADE_INT.json               │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • ALL T1 OUTPUT FILES EXIST with _INT suffix (block T2 if missing)        │
│   • All CRITICAL findings have explicit disposition                         │
│   • All HIGH findings have explicit disposition                             │
│   • A12_CASCADE_INT.json is well-formed with valid cascade_scope            │
│   • If cascade_scope != NONE, modifications array is non-empty              │
│   • scenarios_finalized contains ≤4 scenarios                               │
│   • _INT.json artifacts are valid JSON and contain required fields          │
│                                                                             │
│ IF FAIL: Stop. Report issues. Do not proceed to T2.                         │
│ IF PASS: Proceed to Step 4.                                                 │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │ (proceed only if PASS)
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: INTEGRATION T2 — RECALCULATION                                      │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to execute recalculation cascade (if needed)      │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/integration/G3_INTEGRATION_2.2.3e_PROMPT.md                    │
│   2. kernels/CVR_KERNEL_INT_2_2_2e.py (EXECUTABLE)                          │
│                                                                             │
│ INPUT FILES TO ATTACH (from 08_INTEGRATION/ - T1 outputs):                  │
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_INT_T1_AUDIT.md                  │
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_A5_GIM_INT.json                  │
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_A6_DR_INT.json                   │
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_A10_SCENARIO_INT.json            │
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_A12_CASCADE_INT.json             │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute INTEGRATION Turn 2 for {TICKER}.                                 │
│                                                                             │
│    CRITICAL: You receive ONLY T1 outputs. Do NOT request epistemic bundle.  │
│    CRITICAL: Manual calculation is PROHIBITED. You MUST use Bash kernel.    │
│                                                                             │
│    Read A12_CASCADE_INT.json to determine cascade_scope.                    │
│                                                                             │
│    If cascade_scope = NONE: State 4 = State 3, copy artifacts unchanged.    │
│    If cascade_scope != NONE: Execute kernel via Bash:                       │
│                                                                             │
│    python3 CVR_KERNEL_INT_2_2_2e.py \                                       │
│      --a5 {TICKER}_A5_GIM_INT.json \                                        │
│      --a6 {TICKER}_A6_DR_INT.json \                                         │
│      --a10 {TICKER}_A10_SCENARIO_INT.json \                                 │
│      --cascade {TICKER}_A12_CASCADE_INT.json \                              │
│      --output {TICKER}_A7_VALUATION_INT.json                                │
│                                                                             │
│    If kernel executed, generate kernel receipt (Pattern 13):                │
│    Write {TICKER}_KERNEL_RECEIPT_INT.json with:                             │
│    - kernel file, version, sha256                                           │
│    - input filenames                                                        │
│    - command executed                                                       │
│    - exit_code, execution_time_seconds                                      │
│                                                                             │
│    Write outputs to {analysis_dir}/08_INTEGRATION/:                         │
│    - {TICKER}_A7_VALUATION_INT.json (kernel output if cascade)              │
│    - {TICKER}_A10_SCENARIO_INT.json (updated if SSE changed)                │
│    - {TICKER}_KERNEL_RECEIPT_INT.json (if kernel executed)                  │
│    - {TICKER}_INT_T2_AUDIT.md (human audit only)                            │
│    Return confirmation and filepaths only."                                 │
│                                                                             │
│ OUTPUT PRODUCED (if cascade):                                               │
│   • {TICKER}_A7_VALUATION_INT.json - Kernel output (recalculated valuation) │
│   • {TICKER}_A10_SCENARIO_INT.json - Updated SSE (if changed)               │
│   • {TICKER}_KERNEL_RECEIPT_INT.json - Execution proof (Pattern 13)         │
│   • {TICKER}_INT_T2_AUDIT.md - Human audit only                             │
│                                                                             │
│ PATTERN: Bash Kernel (Pattern 6) - execute kernel via Bash if cascade needed│
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns path   │
│ PATTERN: Kernel Receipts (Pattern 13) - generate if kernel was executed     │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 5: INTEGRATION T2 VALIDATOR                                            │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate T2 output                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/INT_T2_VALIDATOR.md                                            │
│                                                                             │
│ INPUT FILES:                                                                │
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_INT_T2_AUDIT.md                  │
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_A12_CASCADE_INT.json             │
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_KERNEL_RECEIPT_INT.json (if any) │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • All artifacts A.1-A.12 present with _INT suffix                         │
│   • Amendment manifest documents all changes                                │
│   • state_4_active_inputs is complete                                       │
│   • State bridge shows valid State 3 → State 4 delta                        │
│   • If cascade executed: kernel receipt exists (Pattern 13), exit_code=0    │
│   • If cascade executed: values have 4+ decimal precision (real execution)  │
│   • A.12 schema compliance                                                  │
│                                                                             │
│ IF FAIL: Stop. Report issues. Do not proceed to T3.                         │
│ IF PASS: Proceed to Step 6.                                                 │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │ (proceed only if PASS)
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 6: INTEGRATION T3 — FINAL CVR OUTPUT                                   │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to produce complete, finalized CVR State 4        │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ THIS IS THE FINAL OUTPUT. It must be:                                       │
│   • Complete (all narratives N1-N7, all artifacts A.1-A.12)                 │
│   • Clean (no deprecated content, no duplication)                           │
│   • Ready for human review or IRR stage consumption                         │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/integration/G3_INTEGRATION_2.2.3e_PROMPT.md                    │
│   2. prompts/integration/G3_INTEGRATION_2.2.3e_SCHEMAS.md                   │
│                                                                             │
│ INPUT FILES TO ATTACH:                                                      │
│   • {output_dir}/{TICKER}_INT_T1_{DATE}.md (adjudication work)              │
│   • {output_dir}/{TICKER}_INT_T2_{DATE}.md (finalized artifacts)            │
│                                                                             │
│ DO NOT ATTACH deprecated upstream narratives (BASE_T2, ENRICH_T2, SCEN_T2). │
│ The adjudicated versions from T1/T2 supersede those.                        │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute INTEGRATION Turn 3 for {TICKER}.                                 │
│                                                                             │
│    Your task: Produce the COMPLETE, FINALIZED CVR State 4 document.         │
│    This is THE output of the entire CAPY pipeline to date.                  │
│                                                                             │
│    Execute Phase F per the prompt:                                          │
│    - Compile all narratives N1-N7 (finalized versions from T1/T2)           │
│    - Embed all artifacts A.1-A.12 (finalized versions from T2)              │
│    - Include state_4_active_inputs (for IRR consumption)                    │
│                                                                             │
│    Narrative inventory:                                                     │
│    - N1: Investment Thesis (finalized)                                      │
│    - N2: Invested Capital Modeling (finalized)                              │
│    - N3: Economic Governor & Constraints (finalized)                        │
│    - N4: Risk Assessment & DR Derivation (finalized)                        │
│    - N5: Enrichment Synthesis (finalized)                                   │
│    - N6: Scenario Model Synthesis (finalized)                               │
│    - N7: Adjudication Synthesis (from T1 work)                              │
│                                                                             │
│    Artifact inventory:                                                      │
│    - A.1 through A.12 (all finalized, amendments applied)                   │
│    - state_4_active_inputs                                                  │
│                                                                             │
│    The output must contain NO deprecated content and NO duplication.        │
│    A human analyst reading only this document should have everything        │
│    they need to understand and evaluate the valuation.                      │
│                                                                             │
│    Write output to: {output_dir}/{TICKER}_INT_T3_{DATE}.md                  │
│    Return confirmation and filepath only."                                  │
│                                                                             │
│ OUTPUT PRODUCED:                                                            │
│   • {TICKER}_INT_T3_{DATE}.md — THE COMPLETE CVR STATE 4 DOCUMENT           │
│     This file contains:                                                     │
│     - Executive Summary with E[IVPS], key metrics, confidence               │
│     - N1-N7 narratives (finalized, adjudicated)                             │
│     - A.1-A.12 artifacts (finalized, amendments applied)                    │
│     - state_4_active_inputs (computational inputs for IRR)                  │
│     - Pipeline Fit assessment and confidence characterization               │
│                                                                             │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns path   │
│ PATTERN: Surgical Stitching (Pattern 11) - concatenate from T1/T2 outputs   │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 7: INTEGRATION T3 VALIDATOR                                            │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate final CVR output                      │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/INT_T3_VALIDATOR.md                                            │
│                                                                             │
│ INPUT FILE:                                                                 │
│   {output_dir}/{TICKER}_INT_T3_{DATE}.md                                    │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • All narratives N1-N7 present                                            │
│   • All artifacts A.1-A.12 present and complete                             │
│   • state_4_active_inputs present and complete                              │
│   • No deprecated content (check for stale State 3 references)              │
│   • No duplication (narratives not repeated)                                │
│   • Executive summary matches embedded artifact values                      │
│   • Document is self-contained (human can read without other files)         │
│                                                                             │
│ IF FAIL: Report issues. May need T3 re-execution.                           │
│ IF PASS: INTEGRATION stage complete. Output ready for human or IRR.         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Execution Commands (DEV: SMOKE TEST INTEGRATION {TICKER})

Execute the steps above in sequence. Key commands:

**Step 0: Auto-Discovery**
```bash
# Find most recent pipeline run with SC outputs
find smoke_tests/ -name "*{TICKER}*A11*.json" | sort -r | head -5

# Or check production
find production/analyses/ -name "*{TICKER}*A11*.json" | sort -r | head -5

# Set analysis_dir to parent folder
# Create output directory
mkdir -p {analysis_dir}/08_INTEGRATION/
```

**Step 1: Verify Bundle Completeness**
```bash
# Verify all input folders exist and have files
ls {analysis_dir}/00_source/
ls {analysis_dir}/04_RQ/
ls {analysis_dir}/05_ENRICH/
ls {analysis_dir}/06_SCENARIO/
ls {analysis_dir}/07_SILICON_COUNCIL/

# Count files in each
find {analysis_dir}/00_source/ -type f | wc -l
find {analysis_dir}/04_RQ/ -type f | wc -l
# ... etc
```

**Steps 2-7: Spawn Subagents**
Use Task tool with model="opus" for each step. See Stage Flow above for exact prompts and inputs.

### Critical Patterns Applied

| Pattern | Application |
|---------|-------------|
| Pattern 1: Direct-Write | All subagents write to disk, return filepath only |
| Pattern 3: Two-Shot (Extended) | T1=adjudication, T2=recalculation, T3=final output |
| Pattern 5: JSON Repair | T2 can repair malformed T1 JSON before kernel execution |
| Pattern 6: Bash Kernel | T2 executes CVR_KERNEL_INT via Bash if cascade required |
| Pattern 7: Validators | Opus validator after T1, T2, AND T3 |
| Pattern 8: Atomized Prompts | 3 files (PROMPT/SCHEMAS/NORMDEFS) + kernel |
| Pattern 10: Input Validation | Verify full bundle before T1; verify artifacts before T2/T3 |
| Pattern 11: Surgical Stitching | T3 concatenates from T1/T2, no regeneration |
| Pattern 12: Canonical Snapshot | 08_INTEGRATION/ contains complete artifact set with _INT suffix |
| Pattern 13: Kernel Receipts | T2 generates {TICKER}_KERNEL_RECEIPT_INT.json if cascade executed |

### INTEGRATION Stage Files

| File | Location | Purpose |
|------|----------|---------|
| G3_INTEGRATION_2.2.3e_PROMPT.md | prompts/integration/ | Core instructions (Sections I-V) |
| G3_INTEGRATION_2.2.3e_SCHEMAS.md | prompts/integration/ | JSON schemas (Appendix A) |
| G3_INTEGRATION_2.2.3e_NORMDEFS.md | prompts/integration/ | DSL & financial definitions (Appendix B) |
| CVR_KERNEL_INT_2_2_2e.py | kernels/ | Recalculation kernel |
| INT_T1_VALIDATOR.md | validators/ | T1 adjudication validator |
| INT_T2_VALIDATOR.md | validators/ | T2 recalculation validator |
| INT_T3_VALIDATOR.md | validators/ | T3 final output validator |

### INTEGRATION Stage Atomized Files (EXPERIMENTAL)

| File | Purpose | Lines |
|------|---------|-------|
| `G3_INTEGRATION_2.2.3e_PROMPT.md` | Core instructions (Sections I-V) | 1307 |
| `G3_INTEGRATION_2.2.3e_SCHEMAS.md` | JSON schemas (Appendix A) | 512 |
| `G3_INTEGRATION_2.2.3e_NORMDEFS.md` | DSL & financial definitions (Appendix B) | 567 |
| `CVR_KERNEL_INT_2_2_2e.py` | Recalculation kernel | (existing) |

**Status:** EXPERIMENTAL - awaiting smoke test.

**Subagent loading:** Load all 3 prompt files. Kernel attached for T1 context, executed via Bash in T2.

---

