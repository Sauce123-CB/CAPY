# SCENARIO T1 Validator

> **Version:** 2.2.3e
> **Model:** Opus (REQUIRED - do NOT use Haiku)
> **Pattern:** 7 (Validators after each turn)

## Purpose

Validate SCENARIO T1 output before proceeding to T2 (kernel execution).

T1 produces Scenario Execution Arguments JSON that will be passed to the SCENARIO kernel. This JSON defines the discrete high-impact scenarios for probabilistic modeling.

---

## Inputs

Read the T1 output file:
- `{analysis_dir}/06_SCENARIO/{TICKER}_SCEN_T1.md`

The T1 output should contain embedded Scenario Execution Arguments JSON.

---

## Validation Checks

### 1. T1 Output File Exists

**Check:** T1 output file exists and is non-empty.

**Pass Criteria:**
- File exists at expected path
- File size > 1KB (not trivially empty)

**Fail:** Missing T1 output blocks T2 execution.

### 2. Scenario Execution Arguments JSON Present

**Check:** T1 contains embedded Scenario Execution Arguments JSON.

**Pass Criteria:**
- JSON block is present (search for `scenario_execution_args` or similar)
- JSON is well-formed (parseable)
- Contains required structure

**Fail:** Missing or malformed JSON blocks kernel execution.

### 3. Scenario Count (4 Maximum)

**Check:** At most 4 scenarios are defined.

**Pass Criteria:**
- `scenarios` array length ≤ 4
- Priority by |P × M| (expected materiality)

**Fail:** More than 4 scenarios violates the 4-Scenario Limit.

### 4. Scenario Type Coverage

**Check:** Scenarios cover the required type spectrum.

**Expected Types:**
- `MAINLINE` - High-probability, moderate impact
- `BLUE_SKY` - Low-probability transformative upside
- `BLACK_SWAN` - Low-probability catastrophic downside

**Pass Criteria:**
- At least one upside scenario (MAINLINE positive or BLUE_SKY)
- At least one downside scenario (MAINLINE negative or BLACK_SWAN)
- Balanced distributional coverage

**Warn:** Unbalanced scenario set without justification.

### 5. Probability Validity

**Check:** Marginal probabilities are valid.

**Pass Criteria:**
- Each scenario's `p_marginal` is between 0 and 1
- No probabilities of exactly 0 or 1 (eliminates scenario)
- Probabilities are independent (sum can exceed 1)

**Fail:** Invalid probabilities block SSE calculation.

### 6. Interventions Well-Formed

**Check:** Each scenario has properly structured interventions.

**Pass Criteria:**
- Each scenario has `interventions` array
- Each intervention specifies:
  - `target_driver` (must match GIM driver name)
  - `intervention_type` (MULTIPLY, ADD, REPLACE, etc.)
  - `value` (numeric)
  - `years_affected` (array or "all")

**Fail:** Malformed interventions cause kernel errors.

### 7. GIM Driver References Valid

**Check:** All intervention target drivers exist in GIM.

**Pass Criteria:**
- Every `target_driver` matches a driver in A.5 GIM
- No typos or mismatched names

**Fail:** Invalid driver references cause kernel lookup errors.

### 8. Constraints Present

**Check:** Mutual exclusivity or other constraints are defined if needed.

**Pass Criteria:**
- If scenarios are mutually exclusive, `constraints` array is present
- Constraints specify which scenario pairs cannot co-occur
- OR explicit note that scenarios are independent

**Warn:** Missing constraint specification may affect SSE state space.

### 9. No Kernel Execution in T1

**Check:** T1 did NOT execute the kernel.

**Pass Criteria:**
- No A.10 artifact exists yet
- No SSE state enumeration in T1 output
- No E[IVPS] calculated

**Fail:** T1 should NOT run kernel. That's T2's job.

---

## Output Format

### PASS

```
SCENARIO T1 VALIDATOR: PASS

Summary:
- Scenarios Defined: {count}/4
- Type Coverage: {types present}
- Probabilities: Valid (range 0-1)
- Interventions: {count} total
- Driver References: All valid
- Constraints: {present/absent}

T1 validated. Proceed to T2.
```

### FAIL

```
SCENARIO T1 VALIDATOR: FAIL

Critical Issues:
1. [Check N]: {Issue description}
   Location: {Where in T1 output}
   Impact: {Why this blocks T2}

Required Fixes:
- {Specific action to remediate}

Re-run T1 before proceeding to T2.
```

### WARN (Proceed with Caveats)

```
SCENARIO T1 VALIDATOR: PASS WITH WARNINGS

Warnings:
1. [Check N]: {Issue description}

Proceed to T2, but note caveats.
```

---

## Validator Execution

1. Read T1 output file
2. Parse embedded Scenario Execution Arguments JSON
3. Cross-reference driver names with A.5 GIM from ENRICH folder
4. Execute all checks above
5. Emit validation result

**Return:** Validation result only. Do NOT return the full T1 content.

---

*END OF SCENARIO T1 VALIDATOR*
