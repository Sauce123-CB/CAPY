# SCENARIO Stage Orchestration

> **Version:** 1.0.0
> **Extracted from:** workshop/CLAUDE.md v0.12.1
> **Pipeline Position:** Stage 5 of 8 (ENRICH → SCENARIO)

---

## SCENARIO Stage Orchestration (ENRICH → SCENARIO)

The SCENARIO stage transitions the CVR from deterministic State 2 (ENRICH output) to probabilistic State 3 by modeling discrete high-impact scenarios as causal interventions.

### Architecture (v2.2.2e)

**4-Scenario Limit:** Maximum 4 scenarios, prioritized by |P × M| (expected materiality).

**Scenario Types:**
| Type | Definition | Example |
|------|------------|---------|
| MAINLINE | High-probability, moderate impact | Expected M&A, product launch |
| BLUE_SKY | Low-probability transformative upside | Market dominance, breakthrough adoption |
| BLACK_SWAN | Low-probability catastrophic downside | Technological obsolescence, existential regulatory |

**Integration:** Structured State Enumeration (SSE) produces 2^4 = 16 states, filtered by constraints, renormalized to joint probability distribution.

### Stage Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. SCENARIO T1 (Opus Subagent)                              │
│    Input:  ENRICH T2 artifacts (A.1-A.9) +                  │
│            Scenario Research (RQ M-3a, M-3b outputs) +      │
│            G3_SCENARIO_2.2.2e_*.md (3 atomized files) +     │
│            CVR_KERNEL_SCEN_2_2_2e.py (contextual only)      │
│    Output: Scenario Execution Arguments JSON (in markdown)  │
│    Save:   06_SCENARIO/{TICKER}_SCEN_T1_{DATE}.md           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. SCENARIO T1 VALIDATOR (Opus Subagent)                    │
│    Prompt: validators/SCENARIO_T1_VALIDATOR.md              │
│    Check:  4 scenarios defined, probabilities valid,        │
│            interventions well-formed, constraints present   │
│    Output: PASS/FAIL + issues                               │
└──────────────────────┬──────────────────────────────────────┘
                       │ (proceed only if PASS)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. SCENARIO T2 (Opus Subagent)                              │
│    Input:  T1 output + ENRICH artifacts (fresh re-ingest)   │
│            + CVR_KERNEL_SCEN_2_2_2e.py (executable)         │
│    Execute: Kernel via Bash (Pattern 6)                     │
│    Output: A.10_SCENARIO_MODEL_OUTPUT (JSON) + narrative    │
│    Save:   06_SCENARIO/{TICKER}_SCEN_T2_{DATE}.md           │
│            + {TICKER}_A10_SCENARIO.json                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. A.10 VALIDATOR (Opus Subagent)                           │
│    Prompt: validators/A10_VALIDATOR.md                      │
│    Check:  Schema compliance, SSE math, distribution        │
│            metrics, Economic Governor satisfied             │
│    Output: PASS/WARN/FAIL + issues                          │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

SCENARIO outputs go in the analysis folder's `06_SCENARIO/` subdirectory:
```
{analysis_dir}/
├── 05_ENRICH/                       ← Input: State 2 artifacts
├── 06_SCENARIO/                     ← SCENARIO stage outputs
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_SCEN.json   (copied from ENRICH)
│   ├── {TICKER}_A2_ANALYTIC_KG_SCEN.json         (copied from ENRICH)
│   ├── {TICKER}_A3_CAUSAL_DAG_SCEN.json          (copied from ENRICH)
│   ├── {TICKER}_A5_GIM_SCEN.json                 (copied from ENRICH)
│   ├── {TICKER}_A6_DR_SCEN.json                  (copied from ENRICH)
│   ├── {TICKER}_A7_VALUATION_SCEN.json           (copied from ENRICH)
│   ├── {TICKER}_A8_RESEARCH_PLAN_SCEN.json       (copied from ENRICH)
│   ├── {TICKER}_A9_RESEARCH_RESULTS_SCEN.json    (copied from ENRICH)
│   ├── {TICKER}_A9_ENRICHMENT_TRACE_SCEN.json    (copied from ENRICH)
│   ├── {TICKER}_A10_SCENARIO_SCEN.json           (NEW - T2 kernel output)
│   ├── {TICKER}_SCEN_T1.md                       (NEW - T1 narrative)
│   ├── {TICKER}_SCEN_T2.md                       (NEW - T2 narrative)
│   ├── {TICKER}_N6_SCENARIO_SCEN.md              (NEW - scenario synthesis)
│   └── {TICKER}_KERNEL_RECEIPT_SCEN.json         (NEW - Pattern 13)
├── 07_SILICON_COUNCIL/              ← Next stage
└── PIPELINE_STATE.md
```

**Copy-Forward Protocol:** Before SCENARIO T1, orchestrator copies ENRICH artifacts from 05_ENRICH/ to 06_SCENARIO/ with suffix rename (_ENRICH → _SCEN) using `cp`.

### Execution Commands (DEV: SMOKE TEST SCENARIO {TICKER})

**Step 0: Locate Most Recent ENRICH Output (Auto-Discovery)**
```
1. Search for ENRICH smoke test folders:
   ls -t workshop/smoke_tests/*ENRICH*{TICKER}* | head -5

2. If none found in workshop, check production:
   ls -t production/analyses/{TICKER}_*/05_ENRICH/ | head -5

3. Select the most recent folder with complete ENRICH output
   (must contain {TICKER}_A7_VALUATION_ENRICH.json with State 2 IVPS)

4. Set {analysis_dir} to the parent of 05_ENRICH/
   Example: workshop/smoke_tests/{TICKER}_ENRICH_SMOKE_{TIMESTAMP}/
```

**Step 1: Validate Input (Pattern 10 - MANDATORY)**
```
READ files in {analysis_dir}/05_ENRICH/ to verify:
- {TICKER}_A7_VALUATION_ENRICH.json exists with State 2 IVPS
- Extract and log: base_ivps, dr_static, terminal_g, terminal_roic
- Verify IVPS consistency with A7 JSON
```

**Step 2: Execute SCENARIO T1 (Opus Subagent)**
```
Spawn Opus subagent with:
- prompts/scenario/G3_SCENARIO_2.2.2e_PROMPT.md
- prompts/scenario/G3_SCENARIO_2.2.2e_SCHEMAS.md
- prompts/scenario/G3_SCENARIO_2.2.2e_NORMDEFS.md
- {analysis_dir}/05_ENRICH/*.md (all ENRICH artifacts)
- {analysis_dir}/04_RQ/RQ*_M-3a*.md, RQ*_M-3b*.md (scenario research)
- kernels/CVR_KERNEL_SCEN_2_2_2e.py (for context only, DO NOT EXECUTE)

Instruct: "Execute SCENARIO T1 for {TICKER}. Emit Scenario Execution
Arguments JSON embedded in markdown. DO NOT execute kernel."

Subagent writes output directly to disk (Pattern 1).
```

**Step 3: Validate SCENARIO T1**
```
Spawn Opus subagent with:
- validators/SCENARIO_T1_VALIDATOR.md
- The T1 output from step 2

Instruct: "Validate this SCENARIO T1 artifact."
```

**Step 4: Execute SCENARIO T2 (Opus Subagent)**
```
Spawn Opus subagent with:
- T1 output (for embedded JSON)
- {analysis_dir}/06_SCENARIO/*.json (artifacts with _SCEN suffix)
- kernels/CVR_KERNEL_SCEN_2_2_2e.py

Instruct: "Execute SCENARIO T2 for {TICKER}.

CRITICAL: Manual calculation is PROHIBITED. You MUST use Bash kernel.

1. Validate T1 JSON is well-formed (repair if needed - Pattern 5)
2. Execute kernel via Bash (Pattern 6):

   python3 kernels/CVR_KERNEL_SCEN_2_2_2e.py \
     --args {scenario_execution_args} \
     --a5 {TICKER}_A5_GIM_SCEN.json \
     --a7 {TICKER}_A7_VALUATION_SCEN.json \
     --output {TICKER}_A10_SCENARIO_SCEN.json

3. Generate kernel receipt (Pattern 13):
   Write {TICKER}_KERNEL_RECEIPT_SCEN.json with:
   - kernel file, version, sha256
   - input filenames
   - command executed
   - exit_code, execution_time_seconds

Write output files to {analysis_dir}/06_SCENARIO/:
1. {TICKER}_A10_SCENARIO_SCEN.json (kernel output)
2. {TICKER}_N6_SCENARIO_SCEN.md (scenario synthesis narrative)
3. {TICKER}_KERNEL_RECEIPT_SCEN.json (execution proof)
4. {TICKER}_SCEN_T2_AUDIT.md (human audit only)

Return confirmation and filepaths."

Subagent executes kernel via Bash (Pattern 6).
Subagent writes output directly to disk (Pattern 1).
Subagent generates kernel receipt (Pattern 13).
```

**Step 5: Validate A.10**
```
Spawn Opus subagent with:
- validators/A10_VALIDATOR.md
- The A.10 JSON from step 4

Instruct: "Validate this A.10 artifact."
```

### Critical Patterns Applied

| Pattern | Application |
|---------|-------------|
| Pattern 1: Direct-Write | Subagent writes T1/T2 output to disk, returns path only |
| Pattern 3: Two-Shot | T1 = analytical synthesis (no kernel), T2 = kernel execution |
| Pattern 5: JSON Repair | T2 can repair malformed T1 JSON before kernel execution |
| Pattern 6: Bash Kernel | T2 executes CVR_KERNEL_SCEN via Bash, never manual calculation |
| Pattern 12: Canonical Snapshot | 06_SCENARIO/ contains complete artifact set with _SCEN suffix |
| Pattern 13: Kernel Receipts | T2 generates {TICKER}_KERNEL_RECEIPT_SCEN.json for reproducibility |
| Pattern 7: Validators | Opus validator after T1 AND after T2 |
| Pattern 8: Atomized Prompts | 3 files (PROMPT/SCHEMAS/NORMDEFS) + kernel |
| Pattern 10: Input Validation | READ ENRICH artifacts, verify State 2 IVPS before T1 |

### SCENARIO Stage Files

| File | Location | Purpose |
|------|----------|---------|
| G3_SCENARIO_2.2.2e_PROMPT.md | prompts/scenario/ | Core instructions (Sections I-V) |
| G3_SCENARIO_2.2.2e_SCHEMAS.md | prompts/scenario/ | JSON schemas (Appendix A) |
| G3_SCENARIO_2.2.2e_NORMDEFS.md | prompts/scenario/ | DSL & financial definitions (Appendix B) |
| CVR_KERNEL_SCEN_2_2_2e.py | kernels/ | Scenario/SSE kernel |
| SCENARIO_T1_VALIDATOR.md | validators/ | T1 schema/semantic validator |
| A10_VALIDATOR.md | validators/ | A.10 completeness validator |

### SCENARIO Stage Atomized Files (EXPERIMENTAL)

The SCENARIO prompt v2.2.2e is split into 3 atomic files plus kernel:

| File | Purpose | Size |
|------|---------|------|
| `G3_SCENARIO_2.2.2e_PROMPT.md` | Core instructions (Sections I-V) | ~22KB |
| `G3_SCENARIO_2.2.2e_SCHEMAS.md` | JSON schemas (Appendix A) | ~20KB |
| `G3_SCENARIO_2.2.2e_NORMDEFS.md` | DSL & financial definitions (Appendix B) | ~14KB |
| `CVR_KERNEL_SCEN_2_2_2e.py` | Scenario/SSE kernel | 82KB |

**Key updates from 2.2.1e:**
- 3-file atomization for context management
- References updated to G3ENRICH_2.2.2e (7-slot RQ architecture)
- Schema version updated to G3_2.2.2eS
- Embedded kernel (old Appendix C) removed - delivered as separate file

**Status:** CANONICAL - smoke tested 2024-12-20 (DAVE). G3_SCENARIO_2_2_1e.md is HISTORICAL.

**Subagent loading:** Load all 3 prompt files. Kernel executed via Bash in T2 (not embedded in subagent context).

---

