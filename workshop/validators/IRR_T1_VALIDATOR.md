# IRR T1 Validator

> **Version:** 2.2.5e
> **Model:** Opus (REQUIRED - do NOT use Haiku)
> **Pattern:** 7 (Validators after each turn)

## Purpose

Validate IRR T1 (Analytical) output before proceeding to T2 (Kernel Execution).

T1 performs analytical judgment that cannot be automated:
- Resolution percentage (ρ) estimation for each scenario
- Convergence Rate (CR) derivation via B.13 rubric
- Multiple selection rationale via B.10
- Anti-narrative discipline check (P5)
- Live market price fetch
- Input extraction and validation

---

## Inputs

Read the T1 output files:
- `{output_dir}/{TICKER}_IRR_T1_{DATE}.md` (reasoning narrative)
- `{output_dir}/{TICKER}_A13_RESOLUTION_TIMELINE.json`
- `{output_dir}/{TICKER}_IRR_INPUTS.json`

Also read (for cross-validation):
- `{analysis_dir}/08_INTEGRATION/{TICKER}_INT_T3_{DATE}.md` (to verify scenario alignment)

---

## Validation Checks

### 1. A.13 JSON Presence and Structure

**Check:** A.13_RESOLUTION_TIMELINE JSON is present and well-formed.

**Required Top-Level Keys:**
- `schema_version` (should be "G3_2.2.5eIRR")
- `metadata` (company_name, ticker, analysis_date, horizon, source_cvr_state)
- `resolution_estimates` (array)
- `aggregate_diagnostics`
- `null_case_specification`
- `convergence_rate_assessment`
- `multiple_selection`
- `anti_narrative_check`
- `validated_inputs`
- `version_control`

**Fail:** Missing or malformed A.13 blocks T2 execution.

### 2. Resolution Estimates Coverage

**Check:** Every scenario from State 4 has a ρ estimate.

**Pass Criteria:**
- `resolution_estimates` array length matches scenario count from INT T3
- Each entry has: `scenario_id`, `scenario_name`, `full_magnitude_m`, `resolution_percentage_rho`, `effective_magnitude`, `resolution_evidence`
- No scenarios from INT T3 are missing

**Fail:** Missing ρ estimates prevent fork generation.

### 3. Resolution Percentage Bounds

**Check:** All ρ values are within valid range with proper justification.

**Pass Criteria:**
- All `resolution_percentage_rho` values in [0.0, 1.0]
- If ρ > 0.30 for any scenario, `resolution_evidence` must include:
  - `primary_driver` (LEGAL_TIMELINE, PRODUCT_ROADMAP, MACRO_OBSERVABLE, EARNINGS_DISCLOSURE, OTHER)
  - `key_dates` with at least one dated event
  - `evidence_summary` explaining why ρ > default
- `rho_confidence` is one of: HIGH, MEDIUM, LOW

**Warn:** ρ > 0.50 without strong timeline evidence (per P1 Conservative Anchoring).

**Fail:** ρ outside [0, 1] range.

### 4. Aggregate Diagnostics

**Check:** Aggregate metrics are calculated and flagged appropriately.

**Pass Criteria:**
- `average_rho` is calculated correctly (mean of all ρ values)
- `rho_above_50_flag` is true if average_rho > 0.50
- `scenarios_with_low_confidence` lists any scenarios with rho_confidence = LOW
- `dominant_resolution_driver` identifies most common primary_driver

**Warn:** `rho_above_50_flag` = true indicates potential resolution optimism.

### 5. Convergence Rate Derivation

**Check:** CR is derived per B.13 rubric using only recognition factors.

**Pass Criteria:**
- `base_rate` = 0.20
- `adjustments` array contains only Category 1-4 factors:
  - Category 1: Information Dissemination Efficiency (analyst coverage, institutional ownership, short interest)
  - Category 2: Attention Catalysts (investor day, conference visibility, index inclusion)
  - Category 3: Market Microstructure (liquidity, listing venue, borrow availability)
  - Category 4: Narrative Receptivity (thesis simplicity, recent price action)
- Each adjustment has: `category`, `factor`, `condition`, `adjustment` value
- `total_adjustment` = sum of individual adjustments
- `cr_final` = max(0.10, min(0.40, base_rate + total_adjustment))

**Fail:** CR outside [0.10, 0.40] without `deviation_rationale`.

### 6. Anti-Double-Counting Check

**Check:** CR adjustments do NOT include factors that affect E[IVPS].

**Prohibited Factors (per B.13.5):**
- Management credibility/track record
- Accounting quality
- Governance
- Revenue trajectory
- Competitive position / moat
- Balance sheet quality
- Capital allocation history
- Hard catalysts with dates (these should be scenarios with ρ)
- Sector sentiment
- Activist involvement (operational)

**Fail:** CR adjustments include prohibited factors (double-counting).

### 7. Multiple Selection Rationale

**Check:** Multiple selection follows B.10 rubric.

**Pass Criteria:**
- `primary_metric` is one of: EV_Revenue, EV_EBITDA, EV_FCF
- `selection_rationale` references T+1 fundamentals profile
- If transitional (EBITDA margin 5-20%), blend weights documented
- Weighting sums to 1.0 (if blended)

**Fail:** Missing or invalid multiple selection.

### 8. Anti-Narrative Discipline Check

**Check:** P5 compliance - three reasons market might NOT re-rate.

**Pass Criteria:**
- `anti_narrative_check.reasons_market_may_not_rerate` contains exactly 3 strings
- Each reason is substantive (not placeholder text)
- Reasons address distinct concerns (value trap, structural issues, market dynamics)

**Fail:** Missing or incomplete anti-narrative check.

### 9. Validated Inputs Completeness

**Check:** All kernel inputs are extracted and validated.

**Required Fields in `validated_inputs`:**
- `price_t0` > 0 (MUST be from live search, not stale bundle price)
- `shares_outstanding` > 0
- `net_debt_t0` (can be negative for net cash)
- `fundamentals_y0` with: revenue, ebitda, fcf
- `fundamentals_y1` with: revenue, ebitda, fcf
- `valuation_anchor` with: e_ivps_state4, dr_static, base_case_ivps_state2
- `scenarios_finalized` (array from State 4)
- `hurdle_rate` (typically 0.15)

**Fail:** Missing validated inputs block kernel execution.

### 10. Live Price Documentation

**Check:** Live market price was fetched per C. Search Policy.

**Pass Criteria:**
- T1 narrative documents WebSearch for current price
- Price source identified (exchange, provider)
- Price timestamp within last trading day
- Live price differs from bundle price (if bundle was stale)

**Warn:** No evidence of live price fetch - may be using stale data.

### 11. IRR_INPUTS.json Completeness

**Check:** Kernel input file is complete and consistent with A.13.

**Pass Criteria:**
- File exists and is well-formed JSON
- Contains: ticker, market_data, fundamentals_y0, fundamentals_y1, valuation_anchor, scenarios_finalized, hurdle_rate
- `market_data.live_price_t0` matches `validated_inputs.price_t0` in A.13
- Scenario count matches A.13 resolution_estimates count

**Fail:** Missing or inconsistent IRR_INPUTS.json blocks kernel execution.

---

## Output Format

### PASS

```
IRR T1 VALIDATOR: PASS

Summary:
- A.13 Schema: Valid (G3_2.2.5eIRR)
- Scenarios: {N} scenarios, all ρ estimates present
- Average ρ: {value} (flag: {yes/no})
- Convergence Rate: {cr_final} (base: 0.20, adjustment: {delta})
- Multiple Selection: {primary_metric}
- Anti-Narrative: 3 reasons documented
- Live Price: ${price} (source: {source})
- IRR_INPUTS.json: Complete

T1 validated. Proceed to T2.
```

### FAIL

```
IRR T1 VALIDATOR: FAIL

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
IRR T1 VALIDATOR: PASS WITH WARNINGS

Warnings:
1. [Check N]: {Issue description}

Proceed to T2, but note caveats in final output.
```

---

## Validator Execution

1. Read T1 output files (narrative, A.13, IRR_INPUTS.json)
2. Parse all JSON blocks
3. Cross-reference with INT T3 scenario list
4. Execute all checks above
5. Emit validation result

**Return:** Validation result only. Do NOT return full artifact content.

---

*END OF IRR T1 VALIDATOR*
