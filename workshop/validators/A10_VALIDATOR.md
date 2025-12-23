# A.10 Validator (SCENARIO Output)

> **Version:** 2.2.3e
> **Model:** Opus (REQUIRED - do NOT use Haiku)
> **Pattern:** 7 (Validators after each turn)

## Purpose

Validate A.10 SCENARIO_MODEL_OUTPUT artifact after SCENARIO T2 (kernel execution).

A.10 contains the SSE (Structured State Enumeration) results: 2^N states (max 16), their probabilities, and the integrated E[IVPS].

---

## Inputs

Read the A.10 artifact:
- `{analysis_dir}/06_SCENARIO/{TICKER}_A10_SCENARIO_SCEN.json`

Also read for cross-validation:
- `{analysis_dir}/06_SCENARIO/{TICKER}_A7_VALUATION_SCEN.json` (base IVPS)
- `{analysis_dir}/06_SCENARIO/{TICKER}_KERNEL_RECEIPT_SCEN.json` (execution proof)

---

## Validation Checks

### 1. A.10 File Exists

**Check:** A.10 artifact exists and is non-empty.

**Pass Criteria:**
- File exists at expected path
- File is valid JSON
- File size > 500 bytes (not trivially empty)

**Fail:** Missing A.10 indicates kernel did not run.

### 2. Kernel Receipt Exists (Pattern 13)

**Check:** Kernel execution receipt exists.

**Pass Criteria:**
- `{TICKER}_KERNEL_RECEIPT_SCEN.json` exists
- Receipt contains:
  - `kernel.file` (kernel filename)
  - `kernel.sha256` (hash of kernel file)
  - `exit_code` = 0
  - `execution_time_seconds` > 0

**Fail:** Missing receipt suggests kernel was not actually executed.

### 3. SSE State Count

**Check:** SSE produced valid state enumeration.

**Pass Criteria:**
- `sse_states` array is present
- Array length = 2^N where N = number of scenarios (max 16 states)
- Each state has unique binary signature

**Fail:** Invalid state count indicates SSE calculation error.

### 4. Probability Distribution Valid

**Check:** State probabilities form valid distribution.

**Pass Criteria:**
- Each state probability is between 0 and 1
- Sum of all state probabilities ≈ 1.0 (within tolerance of 0.001)
- No NaN or Inf values

**Fail:** Invalid distribution blocks E[IVPS] calculation.

### 5. IVPS Values Present

**Check:** Each state has an IVPS value.

**Pass Criteria:**
- Every state in `sse_states` has `ivps` field
- All IVPS values are positive (or documented reason for zero/negative)
- IVPS values have 4+ decimal precision (proves real kernel execution)

**Warn:** Rounded IVPS values (e.g., exactly $100.00) may indicate simulated output.

### 6. E[IVPS] Calculated

**Check:** Expected IVPS is present and valid.

**Pass Criteria:**
- `expected_ivps` or `e_ivps` field is present
- Value equals probability-weighted sum of state IVPS values
- Value is positive and reasonable

**Verification:**
```python
e_ivps_calculated = sum(s['probability'] * s['ivps'] for s in sse_states)
assert abs(e_ivps - e_ivps_calculated) < 0.01
```

**Fail:** Missing or miscalculated E[IVPS] blocks downstream stages.

### 7. Scenario Impact Metrics

**Check:** Each scenario has documented impact on IVPS.

**Pass Criteria:**
- For each scenario, delta IVPS is calculable (with vs without)
- Impact direction matches scenario type (BLUE_SKY = positive, BLACK_SWAN = negative)
- No scenarios with zero impact (would be meaningless)

**Warn:** Zero-impact scenarios should be removed.

### 8. Economic Governor Satisfied

**Check:** E[IVPS] respects economic constraints.

**Pass Criteria:**
- E[IVPS] is not more than 10x the base IVPS (no explosive growth)
- E[IVPS] is not less than 0.1x the base IVPS (no total destruction without BLACK_SWAN)
- Relationship to base IVPS is documented

**Warn:** Extreme E[IVPS] values may indicate intervention miscalibration.

### 9. Unit Multiplier Applied (v2.2.3e)

**Check:** IVPS values are in correct units.

**Pass Criteria:**
- If A.5 GIM has `unit: thousands`, IVPS should be scaled appropriately
- IVPS should be roughly comparable to market price (within order of magnitude)
- Not off by 1000x due to missing unit scaling

**Fail:** Unit mismatch indicates kernel bug.

### 10. Variance and Risk Metrics

**Check:** Distribution metrics are present.

**Pass Criteria:**
- `variance_ivps` or `std_ivps` is present
- Percentile values (p10, p25, p50, p75, p90) are present
- Values are ordered correctly (p10 < p25 < p50 < p75 < p90)

**Warn:** Missing distribution metrics reduce report quality.

---

## Output Format

### PASS

```
A.10 VALIDATOR: PASS

Summary:
- SSE States: {count}
- Probability Sum: {sum} (should be ~1.0)
- E[IVPS]: ${value}
- Base IVPS: ${base_value}
- Impact Range: ${min_ivps} to ${max_ivps}
- Kernel Receipt: Present (exit_code=0)

A.10 validated. Proceed to Silicon Council.
```

### FAIL

```
A.10 VALIDATOR: FAIL

Critical Issues:
1. [Check N]: {Issue description}
   Location: {Which field/section}
   Impact: {Why this is critical}

Required Fixes:
- {Specific action to remediate}

Re-run SCENARIO T2 before proceeding.
```

### WARN (Proceed with Caveats)

```
A.10 VALIDATOR: PASS WITH WARNINGS

Warnings:
1. [Check N]: {Issue description}

Proceed to Silicon Council, but note caveats in A.11.
```

---

## Validator Execution

1. Read A.10 artifact
2. Read kernel receipt for execution proof
3. Read base IVPS from A.7 for comparison
4. Execute all checks above
5. Verify E[IVPS] calculation matches probability-weighted sum
6. Emit validation result

**Return:** Validation result only. Do NOT return the full A.10 content.

---

*END OF A.10 VALIDATOR*
