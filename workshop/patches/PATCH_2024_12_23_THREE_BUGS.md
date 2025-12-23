# PATCH 2024-12-23: Three Critical Bugs from ZENV Smoke Test

**Date:** 2024-12-23
**Status:** APPLIED - Awaiting re-test
**Discovered During:** ZENV smoke test (ZENV_SMOKE_20251223_103051)

---

## Summary

Three critical bugs were discovered during the ZENV smoke test that caused kernel failures and incorrect IVPS calculations.

| Bug | Symptom | Root Cause | Fix |
|-----|---------|------------|-----|
| 1. Kernel Units | IVPS = 0.00787 vs Market = 1.07 (1000x off) | Kernel ignored GIM `unit` field | Read unit, apply multiplier |
| 2. Node Count | DAG truncated to 11 nodes (5 exogenous) | Validator checked "total nodes" not "exogenous nodes" | Change to ≤20 exogenous |
| 3. Repair Protocol | Orchestrator did inline repair | Pattern 5 didn't specify Opus requirement | Add "MUST use Opus" |

---

## Bug 1: Kernel Units (CRITICAL)

### Problem

GIM artifact specifies `"unit": "thousands"` but kernels never read this field. All financial values are in thousands, but IVPS calculation used raw equity value divided by shares:

```
equity_value = 1,234,567 (in thousands = $1.23B)
fdso = 156,789,000 shares
ivps = 1,234,567 / 156,789,000 = $0.00787  ← WRONG (1000x too small)
```

Should be:
```
ivps = (1,234,567 * 1000) / 156,789,000 = $7.87  ← CORRECT
```

### Fix Applied

All 5 kernels updated to:

1. Extract unit from GIM artifact (handling wrapped/unwrapped formats)
2. Compute multiplier: `{'thousands': 1000, 'millions': 1_000_000, 'billions': 1_000_000_000}`
3. Pass `unit_multiplier` through function chain
4. Apply at IVPS calculation: `ivps = (equity_value * unit_multiplier) / fdso`

### Files Modified

| File | Changes |
|------|---------|
| `BASE_CVR_KERNEL_2.2.3e.py` | Added unit extraction, updated `calculate_apv` signature |
| `CVR_KERNEL_ENRICH_2.2.3e.py` | Same pattern |
| `CVR_KERNEL_SCEN_2_2_2e.py` | Same + updated `execute_scenario_intervention` |
| `CVR_KERNEL_INT_2_2_2e.py` | Same pattern |
| `CVR_KERNEL_IRR_2.2.5e.py` | Same pattern |

### Code Pattern (in all kernels)

```python
# Handle both wrapped {"A.5_GESTALT_IMPACT_MAP": {...}} and unwrapped {...} formats
inner_a5 = gim_artifact.get('A.5_GESTALT_IMPACT_MAP', gim_artifact)
gim = inner_a5.get('GIM', {})

# PATCH 2.2.3e: Extract unit multiplier for per-share calculations
unit_str = inner_a5.get('unit', 'units').lower()
UNIT_MULTIPLIERS = {'thousands': 1000, 'millions': 1_000_000, 'billions': 1_000_000_000}
unit_multiplier = UNIT_MULTIPLIERS.get(unit_str, 1)

# ... later in calculate_apv:
ivps = (equity_value * unit_multiplier) / fdso
```

---

## Bug 2: Node Count Check (HIGH)

### Problem

Orchestration and validators checked "≤15 total nodes" or "≤20 total nodes", but the constraint should be on **exogenous nodes only**. Endogenous nodes (Revenue, EBIT, etc.) are computed, not modeled.

During ZENV smoke test, a validator triggered re-do because DAG had 11 total nodes, but only 5 were exogenous. The instruction was misinterpreted.

### Fix Applied

Changed all references from "≤15 nodes" or "≤20 nodes" to "≤20 exogenous nodes" with explicit counting instructions.

### Files Modified

| File | Changes |
|------|---------|
| `orchestration/BASE_STAGE.md` | 5 occurrences updated |
| `orchestration/ENRICH_STAGE.md` | Updated repair instruction |
| `orchestration/SCENARIO_STAGE.md` | Updated repair instruction |
| `orchestration/IRR_STAGE.md` | Updated repair instruction |
| `prompts/refine/BASE_T1_REFINE_v1_1.md` | Changed to "≤20 exogenous nodes" |
| `prompts/refine/BASE_T1_REFINE_v1_2.md` | Same |
| `prompts/refine/BASE_T1_REFINE_v1_3.md` | Same |
| `validators/BASE_T1_VALIDATOR.md` | Created with exogenous node check |
| `validators/BASE_REFINE_VALIDATOR.md` | Created with exogenous node check |

### Counting Logic

```python
# Method 1: If DAG has node_type field
exog_count = sum(1 for n in dag['nodes'] if n.get('node_type') == 'exogenous')

# Method 2: If DAG has exogenous_nodes list
exog_count = len(dag.get('exogenous_nodes', []))

# Constraint: exog_count ≤ 20
```

---

## Bug 3: Repair Protocol (MEDIUM)

### Problem

Pattern 5 (T2 JSON Repair) didn't explicitly require Opus for repair. During smoke test, orchestrator attempted inline repair instead of spawning an Opus subagent, leading to poor repair quality.

### Fix Applied

Added explicit instruction to `ORCHESTRATION_KEY_PATTERNS.md`:

```markdown
**CRITICAL: Repair MUST be done by Opus subagent.**
Haiku is NOT smart enough for JSON repair. When spawning a repair subagent,
ALWAYS use `model: "opus"`. The reasoning required to understand schema intent
and fix malformed structures exceeds Haiku's capabilities.
```

### Files Modified

| File | Changes |
|------|---------|
| `orchestration/ORCHESTRATION_KEY_PATTERNS.md` | Added Opus requirement to Pattern 5 |

---

## New Validators Created

Four validators that were referenced in orchestration but didn't exist have been created:

| File | Purpose |
|------|---------|
| `validators/BASE_T1_VALIDATOR.md` | Validates BASE T1 with ≤20 exog nodes check |
| `validators/BASE_REFINE_VALIDATOR.md` | Validates REFINE with equity bridge + exog nodes |
| `validators/SCENARIO_T1_VALIDATOR.md` | Validates scenario execution args JSON |
| `validators/A10_VALIDATOR.md` | Validates SSE output + kernel receipt |

---

## Commits

| Commit | Description |
|--------|-------------|
| `402fef0` | fix(kernels): read unit from GIM, fix node count, add Opus repair |
| `2afe8ae` | feat(validators): create missing BASE and SCENARIO validators |
| `1078104` | docs(CLAUDE.md): add new validators to Current Versions table |

---

## Verification Plan

Re-run ZENV smoke test and verify:

1. **Unit multiplier applied:** IVPS should be in correct range (not 1000x off)
2. **Validators run:** BASE_T1_VALIDATOR and BASE_REFINE_VALIDATOR should execute
3. **Exogenous node count:** Should pass if ≤20 exogenous (total nodes can be higher)
4. **Kernel receipt:** Should exist with exit_code=0

---

## Related Documents

- Plan file: `/Users/Benjamin/.claude/plans/snuggly-skipping-feigenbaum.md`
- Previous ZENV smoke test: `ZENV_SMOKE_20251223_103051` (deleted, was pre-patch)
- Mega-patch: `patches/MEGA_PATCH_2024_12_22.md`

---

*END OF PATCH DOCUMENTATION*
