# IRR Kernel Patch: Fix Double-Counting of Scenario Impacts

**Priority:** CRITICAL
**Kernel:** `CVR_KERNEL_IRR_2.2.5e.py`
**Date:** 2025-12-22

## Problem

The IRR kernel double-counts scenario impacts by:
1. Using **E[IVPS]** ($206.34) as the base for Transition Factor calculations
2. Then adding ρ-weighted scenario impacts on top

But E[IVPS] already includes the probability-weighted scenario impacts (+$7.09).
This causes E[IRR] to be artificially inflated (~27% instead of ~12-15%).

## Correct Semantic Logic

1. **Start with IVPS_Deterministic** (Base Case, no scenarios) = $199.25
2. **E[IVPS]** = IVPS_Deterministic + Σ(P × Impact) = $206.34 (market should price this)
3. **For IRR fork calculations:**
   - Use **IVPS_Deterministic** as the anchor
   - Fork_IVPS = IVPS_Deterministic + Σ(ρ_i × Impact_i) for active scenarios
   - This represents partial scenario resolution moving from base toward full scenario value

## Fix Location

In `execute_irr_workflow()` around line 4940-5000, the kernel extracts `e_ivps_state4` from the bundle and uses it for TF calculations.

**Current (WRONG):**
```python
e_ivps_state4 = state_4_inputs.get('valuation_anchor', {}).get('e_ivps')
# ... uses e_ivps_state4 ($206.34) for TF calculation
```

**Should be:**
```python
# Extract BOTH values
e_ivps_state4 = state_4_inputs.get('valuation_anchor', {}).get('e_ivps')  # $206.34
ivps_deterministic = state_4_inputs.get('valuation_anchor', {}).get('base_case_ivps')  # $199.25

# Use IVPS_DETERMINISTIC for TF calculations (not E[IVPS])
# E[IVPS] is what market prices; IVPS_deterministic is the no-scenario anchor
```

## Required Changes

### 1. Update CLI input mapping (~line 5465)
Add `base_case_ivps` to the `valuation_anchor` in the CLI section:
```python
'valuation_anchor': {
    'e_ivps': irr_inputs.get('valuation_anchor', {}).get('e_ivps_state4'),
    'base_case_ivps': irr_inputs.get('valuation_anchor', {}).get('base_case_ivps_state2'),  # ADD THIS
    'dr_static': ...,
}
```

### 2. Update IRR_INPUTS.json schema (T1 output)
T1 must extract and include `base_case_ivps_state2` from the INTEGRATION artifacts:
- Source: `A7_VALUATION_S4.json` or `A10_SCENARIO_MODEL_S4_FINAL.json`
- Field: `metadata.base_case_reference.state_2_ivps` = 199.25

### 3. Update execute_irr_workflow (~line 4940)
Extract `ivps_deterministic` and use it for TF base calculations:
```python
# Extract deterministic IVPS (base case, no scenarios)
ivps_deterministic = state_4_inputs.get('valuation_anchor', {}).get('base_case_ivps')
if not ivps_deterministic:
    # Fallback to A.7 or A.10
    ivps_deterministic = a7_summary.get('ivps_summary', {}).get('IVPS')
    logger.warning("Using A.7 IVPS as fallback for ivps_deterministic")

# Use ivps_deterministic for TF calculation, NOT e_ivps_state4
tf_result = calculate_transition_factor(
    ivps_t0=ivps_deterministic,  # CHANGED from e_ivps_state4
    ...
)
```

### 4. Update fork generation (~line 4240)
Ensure fork IVPS is calculated as:
```python
fork_ivps = ivps_deterministic + sum(rho[s] * impact[s] for s in active_scenarios)
```

## Test Values (DAVE Inc.)

| Value | Amount | Source |
|-------|--------|--------|
| IVPS_Deterministic | $199.25 | A10.metadata.base_case_reference.state_2_ivps |
| E[IVPS] State 4 | $206.34 | A10.sse_result.e_ivps |
| Current Price | $215.25 | WebSearch (live) |
| DR | 13.25% | A6/A7 |

**Expected E[IRR] after fix:** ~12-15% (near DR, since stock is ~4% overvalued)

## Files to Modify

1. `workshop/kernels/CVR_KERNEL_IRR_2.2.5e.py`
   - CLI section: add base_case_ivps to bundle
   - execute_irr_workflow: extract and use ivps_deterministic
   - Fork generation: use ivps_deterministic as anchor

2. `workshop/smoke_tests/DAVE_ENRICH_SMOKE_20251220_120936/09_IRR/DAVE_IRR_INPUTS.json`
   - Add: `valuation_anchor.base_case_ivps_state2: 199.25`

## Verification

After fix, re-run:
```bash
python3 kernels/CVR_KERNEL_IRR_2.2.5e.py \
  --a13 smoke_tests/.../09_IRR/DAVE_A13_RESOLUTION_TIMELINE.json \
  --inputs smoke_tests/.../09_IRR/DAVE_IRR_INPUTS.json \
  --output smoke_tests/.../09_IRR/DAVE_A14_IRR_ANALYSIS.json
```

Check:
- E[IRR] should be ~12-15%, not 27%
- Null Case IRR should be ~DR (13.25%) minus small overvaluation penalty
- Return attribution: scenario_resolution_contribution should be small (~1-3%), not 15%
