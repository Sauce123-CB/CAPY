# SILICON COUNCIL Stage Orchestration

> **Version:** 1.0.0
> **Extracted from:** workshop/CLAUDE.md v0.12.1
> **Pipeline Position:** Stage 6 of 8 (SCENARIO → SILICON COUNCIL)

---

## SILICON COUNCIL Stage Orchestration (SCENARIO → SILICON COUNCIL)

The SILICON COUNCIL stage provides adversarial audit of MRC State 3 before finalization in INTEGRATION.

### Architecture (v2.2.2e)

**6-Audit Parallel Framework:**
- 6 specialized Opus subagents execute in parallel
- Each receives full Epistemic Parity Bundle (same context as upstream stages)
- Each writes JSON fragment directly to disk (Pattern 1)
- Validator consolidates into A.11_AUDIT_REPORT
- Simple consolidation only (INTEGRATION handles deconflicting)

**Audit Types:**
| Audit | Focus | A.11 Section |
|-------|-------|--------------|
| ACCOUNTING | Source integrity, ATP verification, data accuracy | source_integrity |
| FIT | Pipeline suitability, blind spots rubric | pipeline_fit_assessment |
| EPISTEMIC | Bayesian protocol compliance, Economic Governor | epistemic_integrity_assessment |
| RED_TEAM | Adversarial "what could go wrong" analysis | red_team_findings |
| DISTRIBUTIONAL | Distribution shape, investment implications | distributional_coherence |
| ECONOMIC_REALISM | Top-down plausibility, implied metrics check | economic_realism |

### Stage Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 0. AUTO-DISCOVERY: Locate Most Recent SCENARIO Output                       │
│    find smoke_tests/ -name "*SCENARIO*" -o -name "*A10*.json" | sort -r     │
│    Identify folder with complete 06_SCENARIO/ artifacts                     │
│    READ and validate: extract E[IVPS], State 3 metrics                      │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. PREPARE EPISTEMIC PARITY BUNDLE                                          │
│    Collect from {analysis_dir}:                                             │
│    - /source_docs/ (pre-processed financials)                               │
│    - /04_RQ/ (RQ1-RQ7 outputs)                                              │
│    - /05_ENRICH/ (A2-A7 + narratives)                                       │
│    - /06_SCENARIO/ (A10 + narratives)                                       │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. PARALLEL FAN-OUT: 6 Opus Subagents (Task tool, run_in_background: true)  │
│                                                                             │
│    Each subagent receives:                                                  │
│    - G3_SC_2.2.2e_PREAMBLE.md                                               │
│    - G3_SC_2.2.2e_{AUDIT_TYPE}.md                                           │
│    - G3_SC_2.2.2e_NORMDEFS.md                                               │
│    - G3_SC_2.2.2e_BLIND_SPOTS.md (FIT audit only)                           │
│    - Full Epistemic Parity Bundle                                           │
│                                                                             │
│    Instruct: "Execute {AUDIT_TYPE} audit for {TICKER}. Write JSON output    │
│    to {output_dir}/{TICKER}_SC_{AUDIT_TYPE}_SC.json. Return confirmation."  │
│                                                                             │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
│  │ACCOUNTING │ │   FIT     │ │ EPISTEMIC │ │ RED_TEAM  │ │  DISTRIB  │ │ECON_REAL  │
│  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
│        │             │             │             │             │             │
│        ▼             ▼             ▼             ▼             ▼             ▼
│    Write to      Write to      Write to      Write to      Write to      Write to
│    disk          disk          disk          disk          disk          disk
└──────────────────────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. VALIDATOR (Opus Subagent)                                                │
│    Input: 6 JSON fragments from step 2                                      │
│    Prompt: validators/SC_VALIDATOR.md                                       │
│    Task: Simple consolidation into A.11_AUDIT_REPORT                        │
│          - Stitch JSON fragments                                            │
│          - Add metadata (ticker, date, execution context)                   │
│          - Generate critical_findings_summary                               │
│          - Generate executive_synthesis                                     │
│    Output: {TICKER}_A11_AUDIT_REPORT.json                                   │
│    Note: NO deconflicting - INTEGRATION handles that                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Directory Structure

SILICON COUNCIL outputs go in the analysis folder's `07_SILICON_COUNCIL/` subdirectory:
```
{analysis_dir}/
├── 06_SCENARIO/                     ← Input: State 3 artifacts
├── 07_SILICON_COUNCIL/              ← SILICON COUNCIL outputs
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_SC.json   (copied from SCEN)
│   ├── {TICKER}_A2_ANALYTIC_KG_SC.json         (copied from SCEN)
│   ├── {TICKER}_A3_CAUSAL_DAG_SC.json          (copied from SCEN)
│   ├── {TICKER}_A5_GIM_SC.json                 (copied from SCEN)
│   ├── {TICKER}_A6_DR_SC.json                  (copied from SCEN)
│   ├── {TICKER}_A7_VALUATION_SC.json           (copied from SCEN)
│   ├── {TICKER}_A10_SCENARIO_SC.json           (copied from SCEN)
│   ├── {TICKER}_SC_ACCOUNTING_SC.json          (NEW - audit output)
│   ├── {TICKER}_SC_FIT_SC.json                 (NEW - audit output)
│   ├── {TICKER}_SC_EPISTEMIC_SC.json           (NEW - audit output)
│   ├── {TICKER}_SC_RED_TEAM_SC.json            (NEW - audit output)
│   ├── {TICKER}_SC_DISTRIBUTIONAL_SC.json      (NEW - audit output)
│   ├── {TICKER}_SC_ECONOMIC_REALISM_SC.json    (NEW - audit output)
│   └── {TICKER}_A11_AUDIT_SC.json              (NEW - consolidated audit)
├── 08_INTEGRATION/                  ← Next stage
└── PIPELINE_STATE.md
```

**Copy-Forward Protocol:** Before SC audits, orchestrator copies SCENARIO artifacts from 06_SCENARIO/ to 07_SILICON_COUNCIL/ with suffix rename (_SCEN → _SC) using `cp`.

### Execution Commands (DEV: SMOKE TEST SILICON COUNCIL {TICKER})

**Step 0: Auto-Discovery (Pattern 10 - MANDATORY)**
```
1. Search for SCENARIO outputs:
   find smoke_tests/ -name "*{TICKER}*A10*.json" | sort -r | head -5

2. If none in smoke_tests, check production:
   find production/analyses/ -name "*{TICKER}*A10*.json" | sort -r | head -5

3. Select most recent folder with complete 06_SCENARIO/
   (must contain A10_SCENARIO.json with E[IVPS])

4. READ and validate:
   - Extract E[IVPS], distribution stats
   - Verify State 2 → State 3 bridge is complete
   - Log baseline metrics

5. Set {analysis_dir} and {output_dir}
   Create 07_SILICON_COUNCIL/ if needed
```

**Step 1: Prepare Epistemic Parity Bundle**
```
Read all files from:
- {analysis_dir}/source_docs/ (or production/source_library/{TICKER}/)
- {analysis_dir}/04_RQ/
- {analysis_dir}/05_ENRICH/
- {analysis_dir}/06_SCENARIO/

Verify bundle completeness:
- 7 RQ files present
- ENRICH T1, T2, A2-A7 present
- SCENARIO T1, T2, A10 present
```

**Step 2: Execute 6 Parallel Audits**
```
Spawn 6 Opus subagents in parallel with Task tool:

For each AUDIT_TYPE in [ACCOUNTING, FIT, EPISTEMIC, RED_TEAM, DISTRIBUTIONAL, ECONOMIC_REALISM]:

Task(
  subagent_type: "general-purpose",
  model: "opus",
  run_in_background: true,
  prompt: """
    You are executing the {AUDIT_TYPE} audit for {TICKER}.

    Read the following prompt files:
    - prompts/silicon_council/G3_SC_2.2.2e_PREAMBLE.md
    - prompts/silicon_council/G3_SC_2.2.2e_{AUDIT_TYPE}.md
    - prompts/silicon_council/G3_SC_2.2.2e_NORMDEFS.md
    [For FIT only: - prompts/silicon_council/G3_SC_2.2.2e_BLIND_SPOTS.md]

    Epistemic Parity Bundle is in: {analysis_dir}

    Execute the audit per the prompt instructions.

    Write your JSON output to:
    {output_dir}/{TICKER}_SC_{AUDIT_TYPE}_SC.json

    Return ONLY: "Complete. File: {filepath}"
    Do NOT return the JSON content.
  """
)

Wait for all 6 tasks to complete via TaskOutput.
Verify all 6 JSON files exist with ls -la.
```

**Step 3: Run Validator**
```
Spawn Opus subagent:

Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
    You are the Silicon Council Validator for {TICKER}.

    Read: validators/SC_VALIDATOR.md

    Input files in {output_dir}/:
    - {TICKER}_SC_ACCOUNTING_SC.json
    - {TICKER}_SC_FIT_SC.json
    - {TICKER}_SC_EPISTEMIC_SC.json
    - {TICKER}_SC_RED_TEAM_SC.json
    - {TICKER}_SC_DISTRIBUTIONAL_SC.json
    - {TICKER}_SC_ECONOMIC_REALISM_SC.json

    Consolidate into A.11_AUDIT_REPORT per validator instructions.

    Write output to: {output_dir}/{TICKER}_A11_AUDIT_REPORT.json

    Return ONLY: "Complete. File: {filepath}"
  """
)

Verify A11 file exists.
Report summary to user.
```

**Step 4: Generate Markdown Copies (for human audit)**
```
Convert all JSON outputs to Markdown for human readability:
- {TICKER}_SC_ACCOUNTING_SC.json → {TICKER}_SC_ACCOUNTING_SC.md
- {TICKER}_SC_FIT_SC.json → {TICKER}_SC_FIT_SC.md
- {TICKER}_SC_EPISTEMIC_SC.json → {TICKER}_SC_EPISTEMIC_SC.md
- {TICKER}_SC_RED_TEAM_SC.json → {TICKER}_SC_RED_TEAM_SC.md
- {TICKER}_SC_DISTRIBUTIONAL_SC.json → {TICKER}_SC_DISTRIBUTIONAL_SC.md
- {TICKER}_SC_ECONOMIC_REALISM_SC.json → {TICKER}_SC_ECONOMIC_REALISM_SC.md
- {TICKER}_A11_AUDIT_REPORT.json → {TICKER}_A11_AUDIT_REPORT.md

Keep both JSON (for pipeline) and Markdown (for human audit).
Use simple JSON-to-Markdown conversion, do NOT transcribe/rewrite content.
```

### Critical Patterns Applied

| Pattern | Application |
|---------|-------------|
| Pattern 1: Direct-Write | Each audit subagent writes JSON to disk, returns path only |
| Pattern 7: Validators | Opus validator consolidates 6 fragments into A.11 |
| Pattern 8: Atomized Prompts | Preamble + 6 audit files + NORMDEFS + BLIND_SPOTS |
| Pattern 10: Input Validation | Auto-discover SCENARIO outputs, verify E[IVPS] before audits |
| Pattern 12: Canonical Snapshot | 07_SILICON_COUNCIL/ contains complete artifact set with _SC suffix |

### SILICON COUNCIL Stage Files

| File | Location | Purpose |
|------|----------|---------|
| G3_SC_2.2.2e_PREAMBLE.md | prompts/silicon_council/ | Mission, inputs, guiding principles |
| G3_SC_2.2.2e_ACCOUNTING.md | prompts/silicon_council/ | Source integrity audit |
| G3_SC_2.2.2e_FIT.md | prompts/silicon_council/ | Pipeline fit assessment |
| G3_SC_2.2.2e_EPISTEMIC.md | prompts/silicon_council/ | Epistemic integrity audit |
| G3_SC_2.2.2e_RED_TEAM.md | prompts/silicon_council/ | Adversarial review |
| G3_SC_2.2.2e_DISTRIBUTIONAL.md | prompts/silicon_council/ | Distribution coherence |
| G3_SC_2.2.2e_ECON_REALISM.md | prompts/silicon_council/ | Economic realism audit |
| G3_SC_2.2.2e_NORMDEFS.md | prompts/silicon_council/ | Normative definitions reference |
| G3_SC_2.2.2e_BLIND_SPOTS.md | prompts/silicon_council/ | Pipeline blind spots reference |
| SC_VALIDATOR.md | validators/ | Consolidation validator |

### SILICON COUNCIL Stage Atomized Files (EXPERIMENTAL)

The SILICON COUNCIL prompt v2.2.2e is split into 10 atomic files:

| File | Purpose |
|------|---------|
| `G3_SC_2.2.2e_PREAMBLE.md` | Shared header (mission, inputs, guiding principles) |
| `G3_SC_2.2.2e_ACCOUNTING.md` | Source integrity audit objective |
| `G3_SC_2.2.2e_FIT.md` | Pipeline fit assessment objective |
| `G3_SC_2.2.2e_EPISTEMIC.md` | Epistemic integrity audit objective |
| `G3_SC_2.2.2e_RED_TEAM.md` | Red team adversarial review objective |
| `G3_SC_2.2.2e_DISTRIBUTIONAL.md` | Distributional coherence review objective |
| `G3_SC_2.2.2e_ECON_REALISM.md` | Economic realism audit objective (NEW) |
| `G3_SC_2.2.2e_NORMDEFS.md` | Normative definitions reference |
| `G3_SC_2.2.2e_BLIND_SPOTS.md` | Pipeline blind spots reference |
| `SC_VALIDATOR.md` | Consolidation validator |

**Key updates from 2.2.1e:**
- Atomized from 1 monolithic file to 10 specialized files
- Added Economic Realism audit (6th parallel audit)
- Changed from multi-LLM parallel execution to Claude Opus parallel subagents
- Simple consolidation validator (no deconflicting - INTEGRATION handles that)
- Direct-write protocol for all audit outputs

**Status:** EXPERIMENTAL - awaiting smoke test. G3_SILICON_COUNCIL_2.2.1e.md remains CANONICAL until smoke test passes.

**Subagent loading:** Each subagent loads Preamble + its audit file + NORMDEFS (+ BLIND_SPOTS for FIT only).

---

