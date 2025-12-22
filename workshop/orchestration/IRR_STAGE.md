# IRR Stage Orchestration

> **Version:** 1.0.0
> **Extracted from:** workshop/CLAUDE.md v0.12.1
> **Pipeline Position:** Stage 8 of 8 (INTEGRATION → IRR)

---

## IRR Stage Orchestration (INTEGRATION → IRR)

The IRR stage is the **final stage (8/8)** of the CAPY pipeline. It transitions the CVR from State 4 (Finalized Intrinsic Value) to State 5 (Expected Return).

### Purpose and Context

**What happened before IRR:**
1. **ENRICH** produced deterministic IVPS (State 2)
2. **SCENARIO** added probabilistic scenarios (State 3)
3. **SILICON COUNCIL** audited across 6 dimensions
4. **INTEGRATION** adjudicated findings and finalized artifacts (State 4)

**What IRR does:**
The upstream stages answer "What is it worth?" IRR answers **"What will I make?"**

This requires:
1. Fetching **live market price** (mandatory WebSearch)
2. Estimating **resolution percentage (ρ)** for each scenario - how much resolves by T+1
3. Deriving **Convergence Rate (CR)** via B.13 rubric - recognition speed factors only
4. Executing kernel to calculate **E[IRR]** and distribution via Transition Factor methodology

### Architecture (v2.2.5e)

**Two-Shot Execution:**

| Turn | Name | Purpose | Key Output |
|------|------|---------|------------|
| T1 | Analytical | ρ estimation, CR derivation, live price fetch, input extraction | A.13 + IRR_INPUTS.json + T1.md |
| T2 | Computational | Kernel execution via Bash (Pattern 6) | A.14 + T2.md (FINAL: A.13 + A.14 + N7) |

**Key Design Decisions:**
- **Two-shot not three-shot:** T2 IS the final output (no T3 needed)
- **WebSearch mandatory:** T1 MUST fetch live price - stale prices = wrong IRR
- **N8 is new narrative:** Completes the N1-N7 chain from INTEGRATION
- **ρ is LLM judgment:** Resolution percentage cannot be automated - requires timeline evidence analysis

### Directory Structure

**Canonical Snapshot (Pattern 12):** 09_IRR/ contains ALL artifacts with _IRR suffix.

```
{analysis_dir}/
├── 08_INTEGRATION/                              ← INPUT: Canonical snapshot with _INT suffix
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_INT.json       (adjudicated)
│   ├── {TICKER}_A2_ANALYTIC_KG_INT.json             (adjudicated)
│   ├── {TICKER}_A3_CAUSAL_DAG_INT.json              (adjudicated)
│   ├── {TICKER}_A5_GIM_INT.json                     (adjudicated)
│   ├── {TICKER}_A6_DR_INT.json                      (adjudicated)
│   ├── {TICKER}_A7_VALUATION_INT.json               (adjudicated, kernel if cascade)
│   ├── {TICKER}_A8_RESEARCH_PLAN_INT.json           (copied from SC)
│   ├── {TICKER}_A9_RESEARCH_RESULTS_INT.json        (copied from SC)
│   ├── {TICKER}_A9_ENRICHMENT_TRACE_INT.json        (copied from SC)
│   ├── {TICKER}_A10_SCENARIO_INT.json               (adjudicated)
│   ├── {TICKER}_A11_AUDIT_INT.json                  (copied from SC)
│   ├── {TICKER}_A12_CASCADE_INT.json                (NEW: cascade trace)
│   ├── {TICKER}_N1_THESIS_INT.md                    (revised if needed)
│   ├── {TICKER}_N2_IC_INT.md                        (revised if needed)
│   ├── {TICKER}_N3_ECON_GOV_INT.md                  (revised if needed)
│   ├── {TICKER}_N4_RISK_INT.md                      (revised if needed)
│   ├── {TICKER}_N5_ENRICHMENT_INT.md                (revised if needed)
│   ├── {TICKER}_N6_SCENARIO_INT.md                  (revised if needed)
│   ├── {TICKER}_N7_ADJUDICATION_INT.md              (NEW: adjudication narrative)
│   ├── {TICKER}_RQ1-RQ7_*_INT.md                    (copied from SC, 7 files)
│   ├── {TICKER}_SC_*_AUDIT_INT.json                 (copied from SC, 6 files)
│   ├── {TICKER}_CVR_STATE4_INT.md                   (NEW: T3 concatenation for human audit)
│   └── {TICKER}_KERNEL_RECEIPT_INT.json             (if valuation kernel was re-run)
│
├── 09_IRR/                                      ← IRR stage outputs (canonical snapshot)
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_IRR.json       (COPIED from INT by orchestrator)
│   ├── {TICKER}_A2_ANALYTIC_KG_IRR.json             (COPIED from INT by orchestrator)
│   ├── {TICKER}_A3_CAUSAL_DAG_IRR.json              (COPIED from INT by orchestrator)
│   ├── {TICKER}_A5_GIM_IRR.json                     (COPIED from INT by orchestrator)
│   ├── {TICKER}_A6_DR_IRR.json                      (COPIED from INT by orchestrator)
│   ├── {TICKER}_A7_VALUATION_IRR.json               (COPIED from INT by orchestrator)
│   ├── {TICKER}_A10_SCENARIO_IRR.json               (COPIED from INT by orchestrator)
│   ├── {TICKER}_A12_CASCADE_IRR.json                (COPIED from INT by orchestrator)
│   ├── {TICKER}_N1-N6_*_IRR.md                      (COPIED from INT by orchestrator, 6 files)
│   ├── {TICKER}_A13_RESOLUTION_IRR.json             (NEW T1: ρ estimates, CR, inputs)
│   ├── {TICKER}_IRR_INPUTS_IRR.json                 (NEW T1: extracted kernel inputs)
│   ├── {TICKER}_A14_IRR_ANALYSIS_IRR.json           (NEW T2: kernel output)
│   ├── {TICKER}_N8_IRR_IRR.md                       (NEW T2: IRR narrative)
│   ├── {TICKER}_KERNEL_RECEIPT_IRR.json             (NEW T2: kernel execution proof)
│   └── {TICKER}_IRR_T1_AUDIT.md                     (human audit only)
│
└── pipeline_state.json
```

**Copy-Forward Protocol (Orchestrator executes BEFORE IRR T1):**
```bash
mkdir -p {analysis_dir}/09_IRR

# Copy core artifacts from INTEGRATION with suffix rename
for f in {analysis_dir}/08_INTEGRATION/{TICKER}_A*_INT.json; do
  base=$(basename "$f" | sed 's/_INT\.json$//')
  cp "$f" "{analysis_dir}/09_IRR/${base}_IRR.json"
done

# Copy narratives
for f in {analysis_dir}/08_INTEGRATION/{TICKER}_N*_INT.md; do
  base=$(basename "$f" | sed 's/_INT\.md$//')
  cp "$f" "{analysis_dir}/09_IRR/${base}_IRR.md"
done
```

### Stage Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 0: COPY-FORWARD AND INPUT VALIDATION                                   │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Orchestrator (YOU) copies artifacts from INT → IRR, then validates    │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ 1. Locate most recent complete INTEGRATION run:                             │
│    find smoke_tests/ -path "*/08_INTEGRATION/*A7*_INT.json" | sort -r       │
│                                                                             │
│ 2. Execute copy-forward (Pattern 12 - see bash script above):               │
│    mkdir -p {analysis_dir}/09_IRR                                           │
│    for f in {analysis_dir}/08_INTEGRATION/{TICKER}_*_INT.*; do              │
│      # Copy with suffix rename: _INT → _IRR                                 │
│    done                                                                     │
│                                                                             │
│ 3. Verify folder contains ALL required artifact files:                      │
│    - {TICKER}_A2_ANALYTIC_KG_IRR.json    (copied from INT)                  │
│    - {TICKER}_A7_VALUATION_IRR.json      (copied from INT)                  │
│    - {TICKER}_A10_SCENARIO_IRR.json      (copied from INT)                  │
│                                                                             │
│ 4. READ key files to extract baseline metrics:                              │
│    - E[IVPS] from A7 or A10                                                 │
│    - DR from A6 or A7                                                       │
│    - Scenario count from A10                                                │
│                                                                             │
│ Set {analysis_dir} to the pipeline run folder.                              │
│ Proceed to Step 1 with 09_IRR/ folder ready.                                │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: IRR T1 — ANALYTICAL                                                 │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to perform analytical judgment                    │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/irr/G3_IRR_2.2.5e_PROMPT.md                                    │
│   2. prompts/irr/G3_IRR_2.2.5e_SCHEMAS.md                                   │
│   3. prompts/irr/G3_IRR_2.2.5e_NORMDEFS.md                                  │
│   4. kernels/CVR_KERNEL_IRR_2.2.5e.py (FOR CONTEXT ONLY - DO NOT EXECUTE)   │
│                                                                             │
│ INPUT FILES TO ATTACH (from 09_IRR/ - copied by orchestrator):              │
│   • {analysis_dir}/09_IRR/{TICKER}_A2_ANALYTIC_KG_IRR.json                  │
│   • {analysis_dir}/09_IRR/{TICKER}_A5_GIM_IRR.json                          │
│   • {analysis_dir}/09_IRR/{TICKER}_A7_VALUATION_IRR.json                    │
│   • {analysis_dir}/09_IRR/{TICKER}_A10_SCENARIO_IRR.json                    │
│   • {analysis_dir}/09_IRR/{TICKER}_N1-N6_*_IRR.md (context, 6 files)        │
│                                                                             │
│ WHY 09_IRR/ NOT 08_INTEGRATION/:                                            │
│   Pattern 12: Canonical Snapshot. Each stage folder contains COMPLETE       │
│   artifact set. Orchestrator has already copied with suffix rename.         │
│   Subagent reads from its own stage folder, writes to its own stage folder. │
│   This ensures artifact provenance is always traceable by folder.                   │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute IRR Turn 1 for {TICKER}.                                         │
│                                                                             │
│    MANDATORY FIRST STEP: WebSearch for '{TICKER} stock price' to get        │
│    current market price. Record source and timestamp. This live price       │
│    OVERRIDES any price in the State 4 bundle.                               │
│                                                                             │
│    Your analytical tasks:                                                   │
│    1. Extract and validate inputs from State 4 JSON files                   │
│    2. For each scenario in A10, estimate ρ (resolution percentage):         │
│       - Identify primary driver (legal, product, macro, earnings)           │
│       - Identify key dates/milestones before T+1                            │
│       - Default ρ ≤ 0.30 unless timeline evidence supports higher           │
│    3. Derive Convergence Rate (CR) via B.13 rubric:                         │
│       - Base rate = 0.20                                                    │
│       - Adjust ONLY for recognition factors (Categories 1-4)                │
│       - DO NOT adjust for fundamental factors (double-counting)             │
│       - Final CR in [0.10, 0.40]                                            │
│    4. Select valuation multiple per B.10 rubric                             │
│    5. Complete anti-narrative check (3 reasons market may not re-rate)      │
│                                                                             │
│    DO NOT execute the kernel. It is provided for context only.              │
│                                                                             │
│    Write 3 output files to {analysis_dir}/09_IRR/:                          │
│    1. {TICKER}_IRR_T1_AUDIT.md (reasoning narrative - human audit only)     │
│    2. {TICKER}_A13_RESOLUTION_IRR.json (kernel input - canonical artifact)  │
│    3. {TICKER}_IRR_INPUTS_IRR.json (extracted data for kernel)              │
│                                                                             │
│    Return confirmation and list of filepaths written."                      │
│                                                                             │
│ OUTPUT PRODUCED (3 files):                                                  │
│   • {TICKER}_IRR_T1_AUDIT.md - Reasoning, ρ derivation, CR derivation       │
│   • {TICKER}_A13_RESOLUTION_IRR.json - ρ per scenario, CR, inputs           │
│   • {TICKER}_IRR_INPUTS_IRR.json - Extracted market data, fundamentals,     │
│     scenarios for kernel consumption                                        │
│                                                                             │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns paths │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: IRR T1 VALIDATOR                                                    │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate T1 output                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/IRR_T1_VALIDATOR.md                                            │
│                                                                             │
│ INPUT FILES:                                                                │
│   • {analysis_dir}/09_IRR/{TICKER}_IRR_T1_AUDIT.md                          │
│   • {analysis_dir}/09_IRR/{TICKER}_A13_RESOLUTION_IRR.json                  │
│   • {analysis_dir}/09_IRR/{TICKER}_IRR_INPUTS_IRR.json                      │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • A.13 schema compliance (G3_2.2.5eIRR)                                   │
│   • All scenarios have ρ estimates                                          │
│   • ρ values in [0, 1], ρ > 0.30 has evidence                               │
│   • CR derived from recognition factors only (no double-counting)           │
│   • CR in [0.10, 0.40] or has deviation_rationale                           │
│   • Anti-narrative check has 3 substantive reasons                          │
│   • Live price documented (WebSearch evidence)                              │
│   • IRR_INPUTS.json complete and consistent with A.13                       │
│                                                                             │
│ IF FAIL: Stop. Report issues. Do not proceed to T2.                         │
│ IF PASS: Proceed to Step 3.                                                 │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │ (proceed only if PASS)
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: IRR T2 — COMPUTATIONAL (KERNEL EXECUTION)                           │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to execute kernel and produce final output        │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/irr/G3_IRR_2.2.5e_PROMPT.md                                    │
│   2. kernels/CVR_KERNEL_IRR_2.2.5e.py (EXECUTABLE)                          │
│                                                                             │
│ INPUT FILES TO ATTACH (from 09_IRR/):                                       │
│   • {analysis_dir}/09_IRR/{TICKER}_IRR_T1_AUDIT.md (T1 reasoning)           │
│   • {analysis_dir}/09_IRR/{TICKER}_A13_RESOLUTION_IRR.json                  │
│   • {analysis_dir}/09_IRR/{TICKER}_IRR_INPUTS_IRR.json                      │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute IRR Turn 2 for {TICKER}.                                         │
│                                                                             │
│    CRITICAL: Manual calculation is PROHIBITED. You MUST use Bash kernel.    │
│    CRITICAL: T2 performs NO reasoning. All judgment is locked in A.13.      │
│                                                                             │
│    1. Validate A.13 and IRR_INPUTS are well-formed (repair if needed)       │
│    2. Execute kernel via Bash (Pattern 6):                                  │
│                                                                             │
│       python3 kernels/CVR_KERNEL_IRR_2.2.5e.py \                            │
│         --a13 {TICKER}_A13_RESOLUTION_IRR.json \                            │
│         --inputs {TICKER}_IRR_INPUTS_IRR.json \                             │
│         --output {TICKER}_A14_IRR_ANALYSIS_IRR.json                         │
│                                                                             │
│    3. Generate kernel receipt (Pattern 13):                                 │
│       Write {TICKER}_KERNEL_RECEIPT_IRR.json with:                          │
│       - kernel file, version, sha256                                        │
│       - input filenames                                                     │
│       - command executed                                                    │
│       - exit_code, execution_time_seconds                                   │
│                                                                             │
│    4. Write N8 IRR Narrative (executive summary of expected return)         │
│                                                                             │
│    Write 3 output files to {analysis_dir}/09_IRR/:                          │
│    1. {TICKER}_A14_IRR_ANALYSIS_IRR.json (kernel output)                    │
│    2. {TICKER}_N8_IRR_IRR.md (IRR narrative)                                │
│    3. {TICKER}_KERNEL_RECEIPT_IRR.json (execution proof)                    │
│                                                                             │
│    Return confirmation and filepaths."                                      │
│                                                                             │
│ OUTPUT PRODUCED (3 files):                                                  │
│   • {TICKER}_A14_IRR_ANALYSIS_IRR.json - Kernel output (E[IRR], dist)       │
│   • {TICKER}_N8_IRR_IRR.md - IRR Narrative (executive summary)              │
│   • {TICKER}_KERNEL_RECEIPT_IRR.json - Execution proof (Pattern 13)         │
│                                                                             │
│ PATTERN: Bash Kernel (Pattern 6) - execute kernel via Bash, not manual calc │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns paths  │
│ PATTERN: Kernel Receipts (Pattern 13) - verifiable proof of execution       │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: IRR T2 VALIDATOR                                                    │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate final IRR output                      │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/IRR_T2_VALIDATOR.md                                            │
│                                                                             │
│ INPUT FILES:                                                                │
│   • {analysis_dir}/09_IRR/{TICKER}_A14_IRR_ANALYSIS_IRR.json                │
│   • {analysis_dir}/09_IRR/{TICKER}_N8_IRR_IRR.md                            │
│   • {analysis_dir}/09_IRR/{TICKER}_A13_RESOLUTION_IRR.json (cross-validate) │
│   • {analysis_dir}/09_IRR/{TICKER}_KERNEL_RECEIPT_IRR.json                  │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • A.14 schema compliance (G3_2.2.5eIRR)                                   │
│   • Kernel receipt exists (Pattern 13: exit_code=0, timing present)         │
│   • Transition Factor analysis complete                                     │
│   • Null case IRR vs DR relationship is economically sensible               │
│   • All forks generated, probabilities sum to 1.0                           │
│   • ρ values from A.13 correctly applied                                    │
│   • Distribution statistics complete (E[IRR], P10-P90)                      │
│   • Values have 4+ decimal precision (proves real execution)                │
│   • N8 narrative present and coherent with A.14                             │
│                                                                             │
│ IF FAIL: Report issues. May need T2 re-execution.                           │
│ IF PASS: IRR stage complete. CVR is now State 5 (Expected Return).          │
│          Proceed to final CVR generation (generate_final_cvr.sh).           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Execution Commands (DEV: SMOKE TEST IRR {TICKER})

**Step 0: Auto-Discovery**
```bash
# Find most recent INTEGRATION output
find smoke_tests/ -path "*/08_INTEGRATION/*A7*.json" | sort -r | head -5

# Or check production
find production/analyses/ -path "*/08_INTEGRATION/*A7*.json" | sort -r | head -5

# Verify required files exist (with _INT suffix)
ls {analysis_dir}/08_INTEGRATION/{TICKER}_A2_ANALYTIC_KG_INT.json
ls {analysis_dir}/08_INTEGRATION/{TICKER}_A7_VALUATION_INT.json
ls {analysis_dir}/08_INTEGRATION/{TICKER}_A10_SCENARIO_INT.json

# Execute copy-forward (Pattern 12) before IRR T1
mkdir -p {analysis_dir}/09_IRR/
for f in {analysis_dir}/08_INTEGRATION/{TICKER}_*_INT.json; do
  base=$(basename "$f" | sed 's/_INT\.json$//')
  cp "$f" "{analysis_dir}/09_IRR/${base}_IRR.json"
done
for f in {analysis_dir}/08_INTEGRATION/{TICKER}_*_INT.md; do
  base=$(basename "$f" | sed 's/_INT\.md$//')
  cp "$f" "{analysis_dir}/09_IRR/${base}_IRR.md"
done
```

**Steps 1-4: Spawn Subagents**
Use Task tool with model="opus" for each step. See Stage Flow above for exact prompts and inputs.

### Critical Patterns Applied

| Pattern | Application |
|---------|-------------|
| Pattern 1: Direct-Write | T1/T2 subagents write to disk, return paths only |
| Pattern 3: Two-Shot | T1=analytical judgment, T2=kernel execution |
| Pattern 5: JSON Repair | T2 can repair malformed A.13 before kernel |
| Pattern 6: Bash Kernel | `python3 CVR_KERNEL_IRR_2.2.5e.py --a13 ... --inputs ... --output ...` |
| Pattern 7: Validators | Opus validator after T1 AND T2 |
| Pattern 8: Atomized Prompts | PROMPT + SCHEMAS + NORMDEFS + kernel |
| Pattern 10: Input Validation | READ individual _IRR.json files (copied from INT), verify E[IVPS]/DR |
| Pattern 12: Canonical Snapshot | 09_IRR/ contains complete artifact set with _IRR suffix |
| Pattern 13: Kernel Receipts | T2 generates {TICKER}_KERNEL_RECEIPT_IRR.json for reproducibility |

### IRR Stage Files

| File | Location | Purpose |
|------|----------|---------|
| G3_IRR_2.2.5e_PROMPT.md | prompts/irr/ | Core instructions (Sections I-V) |
| G3_IRR_2.2.5e_SCHEMAS.md | prompts/irr/ | JSON schemas (A.13, A.14) |
| G3_IRR_2.2.5e_NORMDEFS.md | prompts/irr/ | DSL & financial definitions (B.10-B.14) |
| CVR_KERNEL_IRR_2.2.5e.py | kernels/ | IRR kernel with CLI interface |
| IRR_T1_VALIDATOR.md | validators/ | T1 analytical validator |
| IRR_T2_VALIDATOR.md | validators/ | T2 kernel/final output validator |

### IRR Stage Atomized Files (CANONICAL)

| File | Purpose | Size |
|------|---------|------|
| `G3_IRR_2.2.5e_PROMPT.md` | Core instructions (Sections I-V) | 22KB |
| `G3_IRR_2.2.5e_SCHEMAS.md` | JSON schemas (A.13, A.14) | 10KB |
| `G3_IRR_2.2.5e_NORMDEFS.md` | DSL & financial definitions (B.10-B.14) | 20KB |
| `CVR_KERNEL_IRR_2.2.5e.py` | IRR kernel with CLI | 179KB |

**Key updates from 2.2.4e:**
- 4-file atomization (removed embedded kernel from prompt)
- CLI interface added to kernel for Pattern 6 compliance
- Version refs updated to G3_2.2.5eIRR
- INT compatibility updated to G3INT 2.2.3e

**Status:** CANONICAL - smoke tested 2024-12-22 (DAVE_ENRICH_SMOKE_20251220). G3_IRR_2_2_4e.md is HISTORICAL.

**Subagent loading:** Load all 3 prompt files. Kernel provided for T1 context, executed via Bash in T2.
