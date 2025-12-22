# ENRICH Stage Orchestration

> **Version:** 1.0.0
> **Extracted from:** workshop/CLAUDE.md v0.12.1
> **Pipeline Position:** Stage 4 of 8 (RQ → ENRICH)

---

## ENRICH Stage Orchestration (RQ → ENRICH)

The ENRICH stage integrates research findings from the RQ stage into the CVR, transitioning from State 1 (BASE output) to State 2. Research insights modify the Analytic KG, Causal DAG, GIM assumptions, and DR factors. The kernel then recalculates valuation with enriched inputs.

### Architecture (v2.2.2e)

**Two-Shot Execution:**

| Turn | Name | Purpose | Key Output |
|------|------|---------|------------|
| T1 | Synthesis | Integrate RQ findings into artifacts, identify changes | Modified A.2, A.3, A.5, A.6 + A.9_ENRICHMENT_TRACE |
| T2 | Computational | Kernel execution via Bash (Pattern 6) | A.7 (recalculated) + N5 |

**Key Design Decisions:**
- **Two-shot not three-shot:** No REFINE interposed - RQ findings are already validated
- **Selective modification:** Only artifacts affected by RQ findings are modified
- **Enrichment trace (A.9):** Documents how each RQ finding maps to artifact changes
- **N5 narrative:** New narrative synthesizing research insights

### Directory Structure

**Canonical Snapshot (Pattern 12):** 05_ENRICH/ contains complete State 2 artifacts.

```
{analysis_dir}/
├── 04_RQ/                                   ← Input: RQ outputs with _RQ suffix
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_RQ.json    (copied from BASE)
│   ├── {TICKER}_A2_ANALYTIC_KG_RQ.json          (copied from BASE)
│   ├── {TICKER}_A3_CAUSAL_DAG_RQ.json           (copied from BASE)
│   ├── {TICKER}_A5_GIM_RQ.json                  (copied from BASE)
│   ├── {TICKER}_A6_DR_RQ.json                   (copied from BASE)
│   ├── {TICKER}_A7_VALUATION_RQ.json            (copied from BASE)
│   ├── {TICKER}_N1-N4_*_RQ.md                   (copied from BASE, 4 files)
│   ├── {TICKER}_A8_RESEARCH_PLAN_RQ.json        (NEW - RQ_GEN output)
│   ├── {TICKER}_A9_RESEARCH_RESULTS_RQ.json     (NEW - RQ_ASK summary)
│   └── {TICKER}_RQ1-RQ7_*_RQ.md                 (NEW - research outputs, 7 files)
│
├── 05_ENRICH/                               ← ENRICH stage outputs (canonical State 2)
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_ENRICH.json    (COPIED from RQ - unchanged)
│   ├── {TICKER}_A2_ANALYTIC_KG_ENRICH.json          (MODIFIED - new nodes from RQ)
│   ├── {TICKER}_A3_CAUSAL_DAG_ENRICH.json           (MODIFIED - new edges if needed)
│   ├── {TICKER}_A5_GIM_ENRICH.json                  (MODIFIED - updated assumptions)
│   ├── {TICKER}_A6_DR_ENRICH.json                   (MODIFIED - adjusted risk factors)
│   ├── {TICKER}_A7_VALUATION_ENRICH.json            (NEW - T2 kernel output)
│   ├── {TICKER}_A8_RESEARCH_PLAN_ENRICH.json        (COPIED from RQ)
│   ├── {TICKER}_A9_RESEARCH_RESULTS_ENRICH.json     (COPIED from RQ)
│   ├── {TICKER}_A9_ENRICHMENT_TRACE_ENRICH.json     (NEW - maps RQ→artifact changes)
│   ├── {TICKER}_N1_THESIS_ENRICH.md                 (COPIED from RQ - unchanged)
│   ├── {TICKER}_N2_IC_ENRICH.md                     (COPIED from RQ - unchanged)
│   ├── {TICKER}_N3_ECON_GOV_ENRICH.md               (COPIED from RQ - unchanged)
│   ├── {TICKER}_N4_RISK_ENRICH.md                   (COPIED from RQ - unchanged)
│   ├── {TICKER}_N5_ENRICHMENT_ENRICH.md             (NEW - research synthesis)
│   ├── {TICKER}_RQ1-RQ7_*_ENRICH.md                 (COPIED from RQ, 7 files)
│   ├── {TICKER}_KERNEL_RECEIPT_ENRICH.json          (NEW - Pattern 13)
│   ├── {TICKER}_ENRICH_T1_AUDIT.md                  (human audit only)
│   └── {TICKER}_ENRICH_T2_AUDIT.md                  (human audit only)
│
└── pipeline_state.json
```

**Copy-Forward Protocol (Orchestrator executes BEFORE ENRICH T1):**
```bash
mkdir -p {analysis_dir}/05_ENRICH

# Copy all RQ artifacts with suffix rename
for f in {analysis_dir}/04_RQ/{TICKER}_*_RQ.json; do
  base=$(basename "$f" | sed 's/_RQ\.json$//')
  cp "$f" "{analysis_dir}/05_ENRICH/${base}_ENRICH.json"
done

for f in {analysis_dir}/04_RQ/{TICKER}_*_RQ.md; do
  base=$(basename "$f" | sed 's/_RQ\.md$//')
  cp "$f" "{analysis_dir}/05_ENRICH/${base}_ENRICH.md"
done
```

### Stage Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 0: COPY-FORWARD AND INPUT VALIDATION                                   │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Orchestrator copies RQ artifacts, validates inputs                    │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ 1. Locate most recent complete RQ run:                                      │
│    find smoke_tests/ -path "*/04_RQ/*A9*.json" | sort -r | head -5          │
│                                                                             │
│ 2. Execute copy-forward (Pattern 12 - see bash script above)                │
│                                                                             │
│ 3. Verify all required input files exist in 05_ENRICH/:                     │
│    - {TICKER}_A1-A7_ENRICH.json (7 artifacts)                               │
│    - {TICKER}_A8_RESEARCH_PLAN_ENRICH.json                                  │
│    - {TICKER}_A9_RESEARCH_RESULTS_ENRICH.json                               │
│    - {TICKER}_RQ1-RQ7_*_ENRICH.md (7 research files)                        │
│                                                                             │
│ 4. READ A7 to extract baseline:                                             │
│    - E[IVPS] (State 1 value)                                                │
│    - DR (to verify changes)                                                 │
│                                                                             │
│ Set {analysis_dir} to the pipeline run folder.                              │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: ENRICH T1 — SYNTHESIS                                               │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to integrate RQ findings into artifacts           │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/enrich/G3ENRICH_2.2.2e_PROMPT.md                               │
│   2. prompts/enrich/G3ENRICH_2.2.2e_SCHEMAS.md                              │
│   3. prompts/enrich/G3ENRICH_2.2.2e_NORMDEFS.md                             │
│   4. kernels/CVR_KERNEL_ENRICH_2.2.2e.py (FOR CONTEXT ONLY - DO NOT EXECUTE)│
│                                                                             │
│ INPUT FILES TO ATTACH (from 05_ENRICH/):                                    │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A1-A7_ENRICH.json (7 artifacts)       │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A8_RESEARCH_PLAN_ENRICH.json          │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A9_RESEARCH_RESULTS_ENRICH.json       │
│   • {analysis_dir}/05_ENRICH/{TICKER}_RQ1-RQ7_*_ENRICH.md (7 research files)│
│   • {analysis_dir}/05_ENRICH/{TICKER}_N1-N4_*_ENRICH.md (4 narratives)      │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute ENRICH Turn 1 for {TICKER}.                                      │
│                                                                             │
│    Your synthesis tasks:                                                    │
│    1. For each RQ finding (RQ1-RQ7), identify artifact impact:              │
│       - Does it add new knowledge? → Update A.2 (Analytic KG)               │
│       - Does it change causal relationships? → Update A.3 (DAG)             │
│       - Does it change assumptions? → Update A.5 (GIM)                      │
│       - Does it change risk factors? → Update A.6 (DR)                      │
│    2. Document all changes in A.9_ENRICHMENT_TRACE:                         │
│       - RQ source, finding, artifact modified, field changed, rationale     │
│    3. If no changes needed for an artifact, copy unchanged                  │
│    4. Write N5 ENRICHMENT narrative synthesizing research insights          │
│                                                                             │
│    DO NOT execute the kernel. It is provided for context only.              │
│                                                                             │
│    Write output files to {analysis_dir}/05_ENRICH/:                         │
│    1. {TICKER}_A2_ANALYTIC_KG_ENRICH.json (modified if needed)              │
│    2. {TICKER}_A3_CAUSAL_DAG_ENRICH.json (modified if needed)               │
│    3. {TICKER}_A5_GIM_ENRICH.json (modified if needed)                      │
│    4. {TICKER}_A6_DR_ENRICH.json (modified if needed)                       │
│    5. {TICKER}_A9_ENRICHMENT_TRACE_ENRICH.json (NEW - required)             │
│    6. {TICKER}_N5_ENRICHMENT_ENRICH.md (NEW - required)                     │
│    7. {TICKER}_ENRICH_T1_AUDIT.md (reasoning log - human audit only)        │
│                                                                             │
│    Return confirmation and list of filepaths written."                      │
│                                                                             │
│ OUTPUT PRODUCED:                                                            │
│   • Modified A.2, A.3, A.5, A.6 (as needed based on RQ findings)            │
│   • {TICKER}_A9_ENRICHMENT_TRACE_ENRICH.json - Change manifest              │
│   • {TICKER}_N5_ENRICHMENT_ENRICH.md - Research synthesis narrative         │
│   • {TICKER}_ENRICH_T1_AUDIT.md - Human audit only                          │
│                                                                             │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns paths  │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: ENRICH T1 VALIDATOR                                                 │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate T1 output                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/ENRICH_T1_VALIDATOR.md                                         │
│                                                                             │
│ INPUT FILES:                                                                │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A9_ENRICHMENT_TRACE_ENRICH.json       │
│   • {analysis_dir}/05_ENRICH/{TICKER}_N5_ENRICHMENT_ENRICH.md               │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A2_ANALYTIC_KG_ENRICH.json            │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A5_GIM_ENRICH.json                    │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A6_DR_ENRICH.json                     │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • A9_ENRICHMENT_TRACE exists and is well-formed                           │
│   • Each RQ finding has documented disposition (applied/not applicable)     │
│   • Modified artifacts are valid JSON                                       │
│   • N5 narrative present and substantive                                    │
│   • DR changes have rationale (if DR was modified)                          │
│                                                                             │
│ IF FAIL: Stop. Report issues. Do not proceed to T2.                         │
│ IF PASS: Proceed to Step 3.                                                 │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │ (proceed only if PASS)
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: ENRICH T2 — COMPUTATIONAL (KERNEL EXECUTION)                        │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to execute kernel and produce updated A.7         │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/enrich/G3ENRICH_2.2.2e_PROMPT.md (T2 section)                  │
│   2. kernels/CVR_KERNEL_ENRICH_2.2.2e.py (EXECUTABLE)                       │
│                                                                             │
│ INPUT FILES TO ATTACH (from 05_ENRICH/):                                    │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A5_GIM_ENRICH.json                    │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A6_DR_ENRICH.json                     │
│   • {analysis_dir}/05_ENRICH/{TICKER}_ENRICH_T1_AUDIT.md (context)          │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute ENRICH Turn 2 for {TICKER}.                                      │
│                                                                             │
│    CRITICAL: Manual calculation is PROHIBITED. You MUST use Bash kernel.    │
│    CRITICAL: T2 performs NO reasoning. All judgment is locked in T1.        │
│                                                                             │
│    1. Validate A.5 and A.6 are well-formed (repair if needed - Pattern 5)   │
│    2. Execute kernel via Bash (Pattern 6):                                  │
│                                                                             │
│       python3 kernels/CVR_KERNEL_ENRICH_2.2.2e.py \                         │
│         --a5 {TICKER}_A5_GIM_ENRICH.json \                                  │
│         --a6 {TICKER}_A6_DR_ENRICH.json \                                   │
│         --output {TICKER}_A7_VALUATION_ENRICH.json                          │
│                                                                             │
│    3. Generate kernel receipt (Pattern 13):                                 │
│       Write {TICKER}_KERNEL_RECEIPT_ENRICH.json with:                       │
│       - kernel file, version, sha256                                        │
│       - input filenames                                                     │
│       - command executed                                                    │
│       - exit_code, execution_time_seconds                                   │
│                                                                             │
│    Write output files to {analysis_dir}/05_ENRICH/:                         │
│    1. {TICKER}_A7_VALUATION_ENRICH.json (kernel output)                     │
│    2. {TICKER}_KERNEL_RECEIPT_ENRICH.json (execution proof)                 │
│    3. {TICKER}_ENRICH_T2_AUDIT.md (human audit only)                        │
│                                                                             │
│    Return confirmation and filepaths."                                      │
│                                                                             │
│ OUTPUT PRODUCED:                                                            │
│   • {TICKER}_A7_VALUATION_ENRICH.json - Kernel output (E[IVPS] State 2)     │
│   • {TICKER}_KERNEL_RECEIPT_ENRICH.json - Execution proof (Pattern 13)      │
│   • {TICKER}_ENRICH_T2_AUDIT.md - Human audit only                          │
│                                                                             │
│ PATTERN: Bash Kernel (Pattern 6) - execute kernel via Bash, not manual calc │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns paths  │
│ PATTERN: Kernel Receipts (Pattern 13) - verifiable proof of execution       │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: ENRICH T2 VALIDATOR                                                 │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate T2 output                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/ENRICH_T2_VALIDATOR.md                                         │
│                                                                             │
│ INPUT FILES:                                                                │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A7_VALUATION_ENRICH.json              │
│   • {analysis_dir}/05_ENRICH/{TICKER}_KERNEL_RECEIPT_ENRICH.json            │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A5_GIM_ENRICH.json (cross-validate)   │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A6_DR_ENRICH.json (cross-validate)    │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • A.7 schema compliance                                                   │
│   • Kernel receipt exists (Pattern 13: exit_code=0, timing present)         │
│   • Values have 4+ decimal precision (proves real execution)                │
│   • E[IVPS] is positive and economically sensible                           │
│   • E[IVPS] delta from State 1 is explainable by RQ findings                │
│   • Terminal g < DR (perpetuity validity)                                   │
│   • All artifacts present in 05_ENRICH/ with _ENRICH suffix                 │
│                                                                             │
│ IF FAIL: Report issues. May need T2 re-execution.                           │
│ IF PASS: ENRICH stage complete. CVR is now State 2.                         │
│          Proceed to SCENARIO stage with copy-forward to 06_SCENARIO/.       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Execution Commands (DEV: SMOKE TEST ENRICH {TICKER})

**Step 0: Copy-Forward and Validation**
```bash
# Find most recent RQ output
find smoke_tests/ -path "*/04_RQ/*A9*.json" | sort -r | head -5

# Or check production
find production/analyses/ -path "*/04_RQ/*A9*.json" | sort -r | head -5

# Set analysis_dir to the pipeline run folder
# Execute copy-forward (Pattern 12)
mkdir -p {analysis_dir}/05_ENRICH
for f in {analysis_dir}/04_RQ/{TICKER}_*_RQ.json; do
  base=$(basename "$f" | sed 's/_RQ\.json$//')
  cp "$f" "{analysis_dir}/05_ENRICH/${base}_ENRICH.json"
done
for f in {analysis_dir}/04_RQ/{TICKER}_*_RQ.md; do
  base=$(basename "$f" | sed 's/_RQ\.md$//')
  cp "$f" "{analysis_dir}/05_ENRICH/${base}_ENRICH.md"
done

# Verify inputs
ls {analysis_dir}/05_ENRICH/{TICKER}_A7_VALUATION_ENRICH.json
ls {analysis_dir}/05_ENRICH/{TICKER}_A9_RESEARCH_RESULTS_ENRICH.json
```

**Steps 1-4: Spawn Subagents**
Use Task tool with model="opus" for each step. See Stage Flow above for exact prompts and inputs.

### Critical Patterns Applied

| Pattern | Application |
|---------|-------------|
| Pattern 1: Direct-Write | All subagents write to disk, return filepath only |
| Pattern 3: Two-Shot | T1=synthesis (integrate RQ), T2=kernel execution |
| Pattern 5: JSON Repair | T2 can repair malformed T1 JSON before kernel |
| Pattern 6: Bash Kernel | T2 executes CVR_KERNEL_ENRICH via Bash |
| Pattern 7: Validators | Opus validator after T1 AND T2 |
| Pattern 8: Atomized Prompts | 3 files (PROMPT/SCHEMAS/NORMDEFS) + kernel |
| Pattern 12: Canonical Snapshot | 05_ENRICH/ contains complete State 2 with _ENRICH suffix |
| Pattern 13: Kernel Receipts | T2 generates {TICKER}_KERNEL_RECEIPT_ENRICH.json |

### ENRICH Stage Atomized Files (CANONICAL)

The ENRICH prompt v2.2.2e is split into 3 atomic files plus kernel, mirroring the BASE pattern:

| File | Purpose | Size |
|------|---------|------|
| `G3ENRICH_2.2.2e_PROMPT.md` | Core instructions (Sections I-V) | 22KB |
| `G3ENRICH_2.2.2e_SCHEMAS.md` | JSON schemas (Appendix A) | 16KB |
| `G3ENRICH_2.2.2e_NORMDEFS.md` | DSL & financial definitions (Appendix B) | 13KB |
| `CVR_KERNEL_ENRICH_2.2.2e.py` | Valuation kernel | 39KB |

**Key updates from 2.2.1e:**
- 7-slot RQ architecture references (M-1, M-2, M-3a, M-3b, D-1, D-2, D-3)
- 4-file atomization for context management
- Version refs updated to G3_2.2.2e

**Status:** CANONICAL - smoke tested 2024-12-20. G3ENRICH_2.2.1e.md is HISTORICAL.

**Subagent loading:** Load all 3 prompt files. Kernel executed via Bash in T2 (not embedded in subagent context).

---

