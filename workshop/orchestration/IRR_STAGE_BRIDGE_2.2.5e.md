# IRR Stage Bridge Prompt: Atomization & Orchestration (2.2.5e)

> **Version:** 2.2.5e (target)
> **Source:** G3_IRR_2_2_4e.md (6576 lines, 65K tokens)
> **Date:** 2024-12-21
> **Status:** READY FOR IMPLEMENTATION

---

## Required Reading Before Implementation

**YOU MUST READ THESE FILES before executing IRR atomization:**

1. **`workshop/CLAUDE.md`** - Authoritative workshop instructions, current versions table, development commands
2. **`workshop/orchestration/ORCHESTRATION_KEY_PATTERNS.md`** - All 11 patterns that govern pipeline execution
3. **`workshop/prompts/integration/G3_INTEGRATION_2.2.3e_PROMPT.md`** - Reference for deterministic handoff architecture
4. **`workshop/meta/CAPY_2_2e_README.md`** - Pipeline execution guide

These documents define the patterns that have been validated through successful smoke tests of all prior stages.

---

## Executive Summary

The IRR stage is the final stage of the CAPY pipeline (Stage 8/8). It transitions the CVR from State 4 (Finalized Intrinsic Value) to State 5 (Expected Return). The current monolithic prompt contains a ~5300-line embedded kernel that must be atomized per **Pattern 8**.

**Key Principle:** IRR uses standard **Two-Shot Architecture (Pattern 3)**, not three-shot like INTEGRATION. T1 = Analytical synthesis, T2 = Kernel execution.

---

## 1. Current State Analysis

### File Inventory

| File | Lines | Tokens | Content |
|------|-------|--------|---------|
| `G3_IRR_2_2_4e.md` | 6576 | ~65K | Monolithic (prompt + embedded kernel) |
| `CVR_KERNEL_IRR_2_2_4e.py` | ~5300 | ~45K | Already exists as separate file |

### Prompt Structure

| Section | Lines | Purpose |
|---------|-------|---------|
| I. Mission & Objectives | 1-18 | Stage purpose, value proposition |
| II. Execution Environment | 19-166 | Inputs, two-shot paradigm, kernel mandate |
| III. Core Analytical Directives | 167-209 | P1-P7 (Conservative Anchoring, ρ, Null Case) |
| IV. Execution Protocol | 210-452 | Phases 0-5 (Input extraction → Emission) |
| Appendix A: Schemas | 453-742 | A.13 and A.14 JSON schemas |
| Appendix B: Normative Defs | 743-1251 | B.1-B.14 (Financial defs, DSL, CR framework) |
| **Embedded Kernel** | 1252-6576 | **REDUNDANT** - duplicates standalone .py file |

### Problems

1. **Pattern 8 Violation:** Kernel embedded in markdown (5300+ lines)
2. **Context Dilution:** 65K tokens when ~15K needed
3. **Pattern 1 Gap:** T1 outputs in markdown body, not written to disk
4. **Pattern 6 Risk:** No explicit Bash execution mandate

---

## 2. Atomization Plan (Pattern 8)

### Target File Structure

```
prompts/irr/
├── G3_IRR_2.2.5e_PROMPT.md      (~450 lines) - Sections I-IV
├── G3_IRR_2.2.5e_SCHEMAS.md     (~300 lines) - Appendix A
└── G3_IRR_2.2.5e_NORMDEFS.md    (~500 lines) - Appendix B

kernels/
└── CVR_KERNEL_IRR_2.2.5e.py     (rename from 2_2_4e, add CLI)
```

### Atomization Actions

1. **Extract Sections I-IV** → `G3_IRR_2.2.5e_PROMPT.md`
2. **Extract Appendix A** → `G3_IRR_2.2.5e_SCHEMAS.md`
3. **Extract Appendix B** → `G3_IRR_2.2.5e_NORMDEFS.md`
4. **Rename & Update Kernel** → `CVR_KERNEL_IRR_2.2.5e.py`

---

## 3. Pattern Forward-Propagation

### Pattern 1: Subagent Direct-Write Protocol

**T1 MUST write outputs to disk, not return in conversation:**

```
T1 Subagent:
├─ Executes analysis (CR derivation, ρ estimation)
├─ Writes {TICKER}_IRR_T1_{YYYYMMDD}.md to disk
├─ Writes {TICKER}_A13_RESOLUTION_TIMELINE.json to disk
├─ Returns: "Complete. Files: {path1}, {path2}"

Orchestrator:
├─ Verifies files exist (ls -la)
├─ Proceeds to T2
```

### Pattern 2: Source of Truth Chain

| IRR Input | Source |
|-----------|--------|
| CVR State 4 Bundle | `08_INTEGRATION/{TICKER}_INT_T3_{YYYYMMDD}.md` |
| Scenarios Finalized | `state_4_active_inputs.scenarios_finalized` |
| Valuation Anchor | `state_4_active_inputs.valuation_anchor` |
| Market Data | Live price via WebSearch (MANDATORY refresh) |

### Pattern 3: Two-Shot Architecture

**T1 (Analytical Synthesis):**
- Extract inputs from State 4 Bundle
- Fetch live market price (mandatory WebSearch)
- Derive CR via B.13 rubric
- Estimate ρ for each scenario via B.12
- Generate anti-narrative check (P5)
- **Write A.13 + T1.md to disk** (Pattern 1)
- Kernel provided for context only - DO NOT EXECUTE

**T2 (Kernel Execution):**
- Read T1 outputs from disk
- Validate JSON integrity (Pattern 5)
- Execute kernel via Bash (Pattern 6)
- Write A.14 + T2.md to disk

### Pattern 5: T2 JSON Repair

T2 has authority to repair malformed A.13 before kernel execution:
- Missing brackets, trailing commas
- Document any repairs in T2 output

### Pattern 6: Kernel Execution via Bash

**T2 MUST execute kernel via Bash tool:**

```bash
python3 CVR_KERNEL_IRR_2.2.5e.py \
  --a13 {TICKER}_A13_RESOLUTION_TIMELINE.json \
  --inputs {TICKER}_IRR_INPUTS.json \
  --output {TICKER}_A14_IRR_ANALYSIS.json
```

**Prohibited:** Manual IRR calculations, fabricating kernel output.

### Pattern 10: Input Source Validation

Before T1 execution:
1. READ INT T3 output (not just `ls`)
2. Extract E[IVPS], DR from State 4 Bundle
3. Log baseline metrics
4. Verify artifacts complete

---

## 4. T1 Output Specification

### Files Written by T1 (Pattern 1)

```
{output_dir}/
├── {TICKER}_IRR_T1_{YYYYMMDD}.md       # Reasoning + CR/ρ derivation
├── {TICKER}_A13_RESOLUTION_TIMELINE.json  # Kernel input artifact
└── {TICKER}_IRR_INPUTS.json            # Extracted values for kernel
```

### IRR_INPUTS.json Schema (NEW)

This artifact provides deterministic T1→T2 handoff:

```json
{
  "schema_version": "G3_2.2.5e_IRR_INPUTS",
  "ticker": "DAVE",
  "valuation_date": "2025-12-21",

  "market_data": {
    "live_price_t0": 225.00,
    "price_source": "NASDAQ via WebSearch",
    "price_timestamp": "2025-12-21T10:30:00Z",
    "shares_outstanding_fdso": 11800000,
    "net_debt_y0": -50000000
  },

  "valuation_anchor": {
    "e_ivps_state4": 206.34,
    "base_case_ivps_state2": 199.25,
    "dr_static": 0.1325,
    "terminal_g": 0.0425
  },

  "fundamentals_y0": { "revenue": 347000000, "ebitda": 85000000 },
  "fundamentals_y1": { "revenue": 445000000, "ebitda": 120000000 },

  "selected_multiple": {
    "metric": "EV/EBITDA",
    "rationale": "Positive EBITDA, capital-light fintech, per B.10"
  },

  "scenarios_finalized": [
    {"scenario_id": "S1", "p_posterior": 0.73, "ivps_impact": -52.29},
    {"scenario_id": "S2", "p_posterior": 0.16, "ivps_impact": 30.59},
    {"scenario_id": "S3", "p_posterior": 0.76, "ivps_impact": 42.59},
    {"scenario_id": "S4", "p_posterior": 0.20, "ivps_impact": 40.00}
  ],

  "convergence_rate": {
    "cr_final": 0.18,
    "base_rate": 0.20,
    "adjustments": [{"factor": "Analyst coverage sparse", "delta": -0.02}],
    "anti_narrative_check": [
      "Regulatory overhang may persist beyond T+1",
      "Insider selling signals information asymmetry",
      "Fintech sector multiple compression ongoing"
    ]
  }
}
```

---

## 5. Kernel CLI Interface (Add to 2.2.5e)

Current kernel uses function calls. Add CLI for Pattern 6 compliance:

```python
# Add to CVR_KERNEL_IRR_2.2.5e.py

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="IRR Kernel")
    parser.add_argument("--a13", required=True, help="Path to A.13 JSON")
    parser.add_argument("--inputs", required=True, help="Path to IRR_INPUTS JSON")
    parser.add_argument("--output", required=True, help="Output path for A.14")

    args = parser.parse_args()

    with open(args.a13) as f:
        a13 = json.load(f)
    with open(args.inputs) as f:
        inputs = json.load(f)

    result = execute_irr_workflow(a13, inputs)

    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"A.14 written to: {args.output}")
```

---

## 6. Orchestration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ Stage 0: Source Discovery (Pattern 10)                         │
├─────────────────────────────────────────────────────────────────┤
│ 1. Locate INT T3: 08_INTEGRATION/{TICKER}_INT_T3_*.md           │
│ 2. READ and validate State 4 Bundle presence                   │
│ 3. Extract E[IVPS]=$206.34, DR=13.25%                          │
│ 4. Create output: 09_IRR/                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 1: IRR T1 - Analytical (Pattern 3)                        │
├─────────────────────────────────────────────────────────────────┤
│ Spawn Task subagent (Pattern 1):                                │
│   Attachments:                                                  │
│   - G3_IRR_2.2.5e_PROMPT.md                                     │
│   - G3_IRR_2.2.5e_SCHEMAS.md                                    │
│   - G3_IRR_2.2.5e_NORMDEFS.md                                   │
│   - INT T3 output (State 4 Bundle)                              │
│   - CVR_KERNEL_IRR_2.2.5e.py (context only)                     │
│                                                                 │
│ Subagent writes to disk:                                        │
│   - {TICKER}_IRR_T1_{YYYYMMDD}.md                               │
│   - {TICKER}_A13_RESOLUTION_TIMELINE.json                       │
│   - {TICKER}_IRR_INPUTS.json                                    │
│                                                                 │
│ Returns: confirmation + filepaths only                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 2: IRR T2 - Kernel Execution (Pattern 6)                  │
├─────────────────────────────────────────────────────────────────┤
│ Spawn Task subagent:                                            │
│   Attachments:                                                  │
│   - G3_IRR_2.2.5e_PROMPT.md                                     │
│   - T1 outputs (3 files from Stage 1)                           │
│   - CVR_KERNEL_IRR_2.2.5e.py (EXECUTABLE)                       │
│                                                                 │
│ Subagent:                                                       │
│   1. Validates JSON (Pattern 5 - repair if needed)              │
│   2. Executes kernel via Bash (Pattern 6)                       │
│   3. Writes {TICKER}_A14_IRR_ANALYSIS.json                      │
│   4. Writes {TICKER}_IRR_T2_{YYYYMMDD}.md                       │
│                                                                 │
│ Returns: confirmation + filepaths only                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 3: Validation (Pattern 7)                                 │
├─────────────────────────────────────────────────────────────────┤
│ Verify:                                                         │
│   - All output files exist                                      │
│   - A.14 contains E[IRR] and fork distribution                  │
│   - Sanity checks passed or flagged                             │
│                                                                 │
│ THIS IS THE FINAL OUTPUT OF THE CAPY PIPELINE                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Smoke Test Requirements

### Prerequisites
- INTEGRATION smoke test complete: ✅ `DAVE_ENRICH_SMOKE_20251220`
- INT T3 available: `08_INTEGRATION/DAVE_INT_T3_20251221.md`

### Output Folder
```
smoke_tests/DAVE_ENRICH_SMOKE_20251220_120936/09_IRR/
├── DAVE_IRR_T1_20251221.md
├── DAVE_A13_RESOLUTION_TIMELINE.json
├── DAVE_IRR_INPUTS.json
├── DAVE_IRR_T2_20251221.md
└── DAVE_A14_IRR_ANALYSIS.json
```

### Success Criteria

| Criterion | Target |
|-----------|--------|
| T1 writes 3 files to disk | Pattern 1 compliance |
| A.13 contains valid ρ | 0 < ρ < 1 for all scenarios |
| CR derived with anti-narrative | 3 reasons documented |
| Kernel executes via Bash | Exit code 0 (Pattern 6) |
| A.14 contains E[IRR] | Reasonable value |
| Sanity checks documented | Value trap, dispersion |

---

## 8. Implementation Checklist

### Phase 1: Atomization (Pattern 8)
- [ ] Read existing `G3_IRR_2_2_4e.md` completely
- [ ] Create `G3_IRR_2.2.5e_PROMPT.md` (Sections I-IV)
- [ ] Create `G3_IRR_2.2.5e_SCHEMAS.md` (Appendix A + IRR_INPUTS schema)
- [ ] Create `G3_IRR_2.2.5e_NORMDEFS.md` (Appendix B)
- [ ] Copy kernel to `CVR_KERNEL_IRR_2.2.5e.py`
- [ ] Add CLI interface to kernel

### Phase 2: Prompt Updates
- [ ] Update Section II.A.x for Pattern 1 (T1 writes files)
- [ ] Add explicit Pattern 6 Bash template
- [ ] Add IRR_INPUTS.json schema
- [ ] Update version references to 2.2.5e

### Phase 3: Smoke Test
- [ ] Execute IRR T1 on DAVE
- [ ] Validate T1 outputs (3 files)
- [ ] Execute IRR T2 on DAVE
- [ ] Validate kernel execution
- [ ] Validate A.14 output

### Phase 4: Promotion
- [ ] Update workshop/CLAUDE.md (Current Versions table)
- [ ] Update patches/PATCH_TRACKER.md
- [ ] Update TODO.md
- [ ] Mark 2.2.5e as CANONICAL, 2.2.4e as HISTORICAL
- [ ] Commit and push

---

## 9. Pipeline Completion Status

After IRR smoke test:

| Stage | Status |
|-------|--------|
| BASE | ✅ CANONICAL |
| RQ | ✅ CANONICAL |
| ENRICH | ✅ CANONICAL |
| SCENARIO | ✅ CANONICAL |
| SILICON_COUNCIL | ✅ CANONICAL |
| INTEGRATION | ✅ CANONICAL |
| **IRR** | 🟡 PENDING |

**Goal:** 8/8 stages CANONICAL = Full Autonomous CAPY Pipeline

---

## Trigger Command

```
Do IRR atomization and smoke test on DAVE
```

Read the required files first, then execute.
