# IRR Kernel Fix - Continuation Context

**Date:** 2025-12-22
**Status:** Ready to apply final fix

## Files to Read Before Proceeding

1. `workshop/patches/IRR_DOUBLE_COUNT_FIX.md` - The semantic fix specification
2. `workshop/kernels/CVR_KERNEL_IRR_2.2.5e.py` - The kernel to modify
3. `workshop/smoke_tests/DAVE_ENRICH_SMOKE_20251220_120936/09_IRR/DAVE_IRR_INPUTS.json` - Test inputs

## Summary of Problem

The IRR kernel uses E[IVPS] ($206.34) for Transition Factor calculations, but E[IVPS] already includes +$7.09 of probability-weighted scenario impacts. Then it adds ρ-weighted scenario impacts on top → **double-counting**.

**Result:** E[IRR] = 27% (wrong) instead of ~12-15% (correct)

## Fixes Already Applied (DO NOT REVERT)

These fixes were applied earlier in the session to make the CLI work:

### 1. EBITDA Derivation (~line 3777-3801)
Derives scenario EBITDA from EBIT + D&A when missing. **KEEP THIS.**

### 2. CLI state_4_active_inputs Nesting (~line 5446-5484)
`state_4_active_inputs` must be INSIDE `A.12_INTEGRATION_TRACE`, not a sibling.
The kernel extracts via: `a11_integration_trace.get('state_4_active_inputs', {})`. **KEEP THIS.**

### 3. expected_multiple_t1 Alias (~line 4308-4309)
Added `'expected_multiple_t1': fork_market_multiple_t1` for backward compatibility with sanity checks. **KEEP THIS.**

## Fix Still Needed (THE MAIN ISSUE)

### Location: `execute_irr_workflow()` around line 4940-5080

**Current (WRONG):**
```python
e_ivps_state4 = ivps_summary.get('IVPS') or ...  # Gets $206.34
# ... later uses e_ivps_state4 for TF calculation
tf_result = calculate_transition_factor(
    ivps_t0=e_ivps_state4,  # WRONG - uses $206.34
    ...
)
```

**Should be:**
```python
# Extract BOTH values
e_ivps_state4 = ivps_summary.get('IVPS')  # $206.34 (for reporting)
ivps_deterministic = state_4_inputs.get('valuation_anchor', {}).get('base_case_ivps')
if not ivps_deterministic:
    ivps_deterministic = a7_summary.get('ivps_summary', {}).get('base_case_ivps')
if not ivps_deterministic:
    # Last resort fallback - this shouldn't happen with proper inputs
    logger.error("base_case_ivps not found; falling back to e_ivps (will cause double-count)")
    ivps_deterministic = e_ivps_state4

# Use IVPS_DETERMINISTIC for TF calculation
tf_result = calculate_transition_factor(
    ivps_t0=ivps_deterministic,  # CORRECT - uses $199.25
    ...
)
```

### Also update CLI bundle (~line 5465)
Ensure `base_case_ivps` is passed through:
```python
'valuation_anchor': {
    'e_ivps': irr_inputs.get('valuation_anchor', {}).get('e_ivps_state4'),
    'base_case_ivps': irr_inputs.get('valuation_anchor', {}).get('base_case_ivps_state2'),  # ADD
    ...
}
```

## Test Data (DAVE Inc.)

| Field | Value | Source |
|-------|-------|--------|
| IVPS_Deterministic | $199.25 | base_case_ivps_state2 |
| E[IVPS] State 4 | $206.34 | e_ivps_state4 |
| Current Price | $215.25 | price_t0 |
| DR | 13.25% | dr_static |

**IRR_INPUTS.json already has both values at `valuation_anchor`.**

## Verification After Fix

```bash
cd /Users/Benjamin/Dev/CAPY/workshop
python3 kernels/CVR_KERNEL_IRR_2.2.5e.py \
  --a13 smoke_tests/DAVE_ENRICH_SMOKE_20251220_120936/09_IRR/DAVE_A13_RESOLUTION_TIMELINE.json \
  --inputs smoke_tests/DAVE_ENRICH_SMOKE_20251220_120936/09_IRR/DAVE_IRR_INPUTS.json \
  --output smoke_tests/DAVE_ENRICH_SMOKE_20251220_120936/09_IRR/DAVE_A14_IRR_ANALYSIS.json
```

**Expected after fix:**
- E[IRR] ≈ 12-15% (not 27%)
- Null Case IRR ≈ DR (13.25%) minus ~1% for 4.3% overvaluation
- Scenario resolution contribution: ~1-3% (not 15%)
