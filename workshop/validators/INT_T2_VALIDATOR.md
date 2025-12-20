# INTEGRATION T2 Validator

> **Version:** 2.2.2e
> **Model:** Opus (REQUIRED - do NOT use Haiku)
> **Pattern:** 7 (Validators after each turn)

## Purpose

Validate INTEGRATION T2 (Recalculation) output before proceeding to T3 (Final Output).

T2 executes the recalculation cascade (if required) and produces:
- Finalized artifacts A.1-A.12 with amendments applied
- A.12_INTEGRATION_TRACE (full adjudication record)
- state_4_active_inputs (pre-merged inputs for IRR)

---

## Inputs

Read the T2 output files:
- `{output_dir}/{TICKER}_INT_T2_{DATE}.md`
- `{output_dir}/{TICKER}_A12_INTEGRATION_TRACE.json` (if emitted separately)

Also read (for cross-validation):
- T1 output to verify cascade scope was honored

---

## Validation Checks

### 1. Artifact Completeness

**Check:** All required artifacts are present in T2 output.

**Required Artifacts:**
- A.1_EPISTEMIC_ANCHORS
- A.2_ANALYTIC_KG
- A.3_CAUSAL_DAG
- A.5_GESTALT_IMPACT_MAP
- A.6_DR_DERIVATION_TRACE
- A.7_LIGHTWEIGHT_VALUATION_SUMMARY
- A.8_RESEARCH_STRATEGY_MAP
- A.9_ENRICHMENT_TRACE
- A.10_SCENARIO_MODEL_OUTPUT
- A.12_INTEGRATION_TRACE

**Pass Criteria:**
- All 10 artifacts present (A.11 is referenced, not re-emitted)
- Each artifact has valid JSON structure
- Amended artifacts have schema_version suffix "-A" if modified

**Fail:** Missing artifacts block T3 and IRR.

### 2. A.12 Schema Compliance

**Check:** A.12_INTEGRATION_TRACE follows required schema.

**Required Top-Level Keys:**
- `schema_version` (should be "G3_2.2.2eI")
- `metadata` (company, ticker, timestamps, integration_summary)
- `executive_summary` (adjudication_outcome, material_changes, confidence_assessment)
- `adjudication_log` (array of finding adjudications)
- `scenario_reconciliation` (substitution_performed, pre/post scenarios)
- `recalculation_cascade` (cascade_executed, scope, execution_log)
- `state_bridge` (state_3_summary, state_4_summary, delta_analysis)
- `pipeline_fit_handling` (grade, handling_protocol, confidence_discount_narrative)
- `final_thesis_synthesis` (original_thesis, adjudication_impact, state_4_thesis)

**Pass Criteria:**
- All required keys present
- Nested structures follow schema
- Values are correct types (strings, numbers, booleans, arrays as specified)

**Fail:** Schema violations may cause downstream parsing failures.

### 3. Amendment Manifest Completeness

**Check:** All modifications accepted in T1 are documented.

**Pass Criteria:**
- `amendment_manifest.artifacts_amended` lists all modified artifact IDs
- `amendment_manifest.amendments_applied` includes all accepted findings
- Each amendment references its `finding_id` from adjudication_log
- `from_value` and `to_value` are populated for each amendment

**Fail:** Undocumented amendments break audit trail.

### 4. Cascade Execution Consistency

**Check:** Cascade execution matches T1's cascade_scope.

**Pass Criteria:**
- If T1 cascade_scope = `NONE`:
  - `recalculation_cascade.cascade_executed` = false
  - State 4 values = State 3 values (no change)

- If T1 cascade_scope = `FULL`:
  - `recalculation_cascade.cascade_executed` = true
  - `execution_log.base_case_recalculated` = true
  - `execution_log.sse_recalculated` = true

- If T1 cascade_scope = `PARTIAL_SCENARIO`:
  - `execution_log.scenarios_recalculated` is non-empty
  - `execution_log.sse_recalculated` = true

- If T1 cascade_scope = `PARTIAL_SSE`:
  - `execution_log.sse_recalculated` = true

**Fail:** Cascade mismatch indicates T2 didn't honor T1 decisions.

### 5. Kernel Validation Checks

**Check:** If cascade executed, kernel outputs are valid.

**Pass Criteria:**
- `validation_checks.probability_sum_validated` = true (JPD sums to 1.0)
- `validation_checks.economic_governor_satisfied` = true (Terminal_g < DR, Terminal_ROIC reasonable)
- `validation_checks.limited_liability_enforced` = true (no negative IVPS states)
- No Python stack traces or errors in execution log

**Fail:** Kernel validation failures indicate computation errors.

### 6. State Bridge Validity

**Check:** State 3 → State 4 bridge is properly documented.

**Pass Criteria:**
- `state_3_summary` populated with E[IVPS], P10, P50, P90, std_dev, skewness
- `state_4_summary` populated with same metrics
- `delta_analysis.e_ivps_change_absolute` and `_percent` calculated correctly
- `primary_drivers_of_change` explains key modifications

**Fail:** Missing state bridge prevents human verification.

### 7. state_4_active_inputs Completeness

**Check:** Pre-merged computational inputs for IRR are complete.

**Required Fields:**
- `fundamentals_trajectory` (Y0, Y1, Y2, Y3 with Revenue, EBITDA, etc.)
- `scenarios_finalized` (array of ≤4 scenarios with p_posterior, ivps_impact, fundamentals_y1_intervened)
- `valuation_anchor` (base_case_ivps_state2, e_ivps_state4, dr_static, terminal_g, terminal_roic)
- `market_data_snapshot` (current_price, shares_outstanding_fdso, net_debt_y0, market_cap)
- `constraints` (mutual_exclusivity_groups, economic_incompatibilities)
- `pipeline_fit_grade`

**Pass Criteria:**
- All required fields present and populated
- Values are numeric where expected
- No placeholder values (e.g., "TBD", "null", "0" for everything)

**Fail:** Incomplete state_4_active_inputs blocks IRR execution.

### 8. DR Revision Documentation (if applicable)

**Check:** If DR was revised, proper documentation per P7.

**Pass Criteria (if dr_revised = true):**
- `prior_dr` and `posterior_dr` populated
- `delta_dr` calculated correctly
- `finding_id` references specific A.11 finding
- `x_component_affected` specifies which risk factor
- `evidence_justification` explains the revision

**Fail:** Undocumented DR revision violates P7 protocol.

---

## Output Format

### PASS

```
INT T2 VALIDATOR: PASS

Summary:
- Artifacts Complete: All 10 present
- A.12 Schema: Valid
- Cascade Executed: {Yes/No}, Scope: {scope}
- State Bridge: E[IVPS] {State3} → {State4} ({delta}%)
- state_4_active_inputs: Complete
- Pipeline Fit Grade: {grade}

T2 validated. Proceed to T3.
```

### FAIL

```
INT T2 VALIDATOR: FAIL

Critical Issues:
1. [Check N]: {Issue description}
   Location: {Artifact or section}
   Impact: {Why this blocks T3}

Required Fixes:
- {Specific action to remediate}

Re-run T2 before proceeding to T3.
```

### WARN (Proceed with Caveats)

```
INT T2 VALIDATOR: PASS WITH WARNINGS

Warnings:
1. [Check N]: {Issue description}

Proceed to T3, but review warnings for potential issues.
```

---

## Validator Execution

1. Read T2 output file(s)
2. Parse all embedded JSON artifacts
3. Cross-reference with T1 cascade_scope
4. Execute all checks above
5. Emit validation result

**Return:** Validation result only. Do NOT return full artifact content.

---

*END OF INT T2 VALIDATOR*
