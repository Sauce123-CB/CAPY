# BASE Turn 2 Kernel Execution Failure

## Summary

Kernel execution failed due to schema incompatibility between REFINE outputs and BASE_CVR_KERNEL_2.2.3e.py expectations.

## Failure Point

**Stage:** BASE Turn 2 (Kernel Execution)
**Kernel:** BASE_CVR_KERNEL_2.2.3e.py
**Date:** 2025-12-23
**Exit Code:** 1 (RuntimeError during SCM execution)

## Root Cause

The REFINE prompt (BASE_T1_REFINE_v1_3.md) produces artifact schemas that are incompatible with the kernel's input expectations. This is a **forward compatibility violation** - the REFINE prompt was updated without ensuring the kernel could consume its outputs.

## Specific Schema Mismatches

### 1. DAG Coverage Manifest Structure
**Expected by kernel:** Flat dict with node names as keys
**Produced by REFINE:** Nested dict with categories (revenue_components, margin_components, etc.)
**Impact:** validate_dag_coverage() fails immediately

### 2. DR Derivation Trace Wrapper
**Expected by kernel:** `dr_trace['derivation_trace']['DR_Static']`
**Produced by REFINE:** `dr['DR_Static_Final']` (no wrapper)
**Impact:** Kernel cannot extract discount rate

### 3. CAGR_INTERP Parameter Naming
**Expected by kernel:** `params['interp_years']`
**Produced by REFINE:** `params['fade_years']`
**Impact:** TypeError when applying DSL

### 4. EXPLICIT_SCHEDULE Year Keys
**Expected by kernel:** String keys "0", "1", "2", ...
**Produced by REFINE:** String keys "Y0", "Y1", "Y2", ...
**Impact:** KeyError when accessing schedule

### 5. DAG Equation Format (FATAL)
**Expected by kernel:** Executable Python expressions (e.g., `Revenue_CPaaS + Revenue_SaaS`)
**Produced by REFINE:** Descriptive notation (e.g., `f(market_volume, market_share, pricing_power)`)
**Impact:** NameError when eval() attempts to execute equation strings

## Attempted Workarounds

Created `run_kernel.py` with multiple patches:
1. Disabled validate_dag_coverage()
2. Transformed DR structure to add derivation_trace wrapper
3. Renamed fade_years → interp_years
4. Converted "Y0" → "0" in EXPLICIT_SCHEDULE
5. Patched prepare_inputs() to check params.Y0_value

**Result:** Patches 1-4 succeeded, but #5 (DAG equations) is unfixable without rewriting the entire DAG.

## Implications

1. **REFINE v1.3 is not production-ready** - cannot be used with current kernel
2. **Kernel 2.2.3e may have breaking changes** - needs review vs 2.2.2e
3. **No forward compatibility testing** - REFINE changes deployed without kernel validation
4. **DAG equation format is fundamentally incompatible** - descriptive vs executable

## Recommended Actions

### Immediate (Unblock ZENV smoke test)
- **Option A:** Revert to REFINE v1.2 + Kernel 2.2.2e (last known working combination)
- **Option B:** Write DAG equation translator (descriptive → executable Python)
- **Option C:** Update kernel to accept descriptive DAG format

### Long-term (Prevent recurrence)
1. **Enforce forward compatibility protocol** - no REFINE changes without kernel smoke test
2. **Add schema validation tests** - automated checks for artifact structure
3. **Document canonical schemas** - single source of truth for A.1-A.6 structure
4. **Version alignment** - REFINE v1.3 should require Kernel 2.2.3+, with compatibility matrix

## Files Affected

- `ZENV_A2_ANALYTIC_KG_BASE.json` ✓ (compatible)
- `ZENV_A3_CAUSAL_DAG_BASE.json` ✗ (equation format incompatible)
- `ZENV_A5_GIM_BASE.json` ✗ (parameter naming incompatible)
- `ZENV_A6_DR_BASE.json` ✗ (structure incompatible)
- `ZENV_A7_VALUATION_BASE.json` - NOT GENERATED

## Error Log Excerpt

```
ERROR - SCM Execution Error at t=1 for handle 'Debt_Service_Principal'.
Equation: 'f(amortization_schedule, earnout_installments)'.
Error: name 'f' is not defined

RuntimeError: Failed to execute equation for Debt_Service_Principal at year 1.
Error: name 'f' is not defined
```

## Status

**BLOCKED** - Cannot proceed with Turn 2 until schema compatibility is resolved.
