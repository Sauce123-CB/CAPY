# IRR T2 Validator

> **Version:** 2.2.5e
> **Model:** Opus (REQUIRED - do NOT use Haiku)
> **Pattern:** 7 (Validators after each turn)

## Purpose

Validate IRR T2 (Kernel Execution) output. T2 is the FINAL output of the IRR stage.

T2 executes the kernel via Bash and produces the complete IRR analysis:
- A.14_IRR_ANALYSIS (kernel output with E[IRR], distribution, sanity checks)
- Final document combining A.13 + A.14 + N7 (IRR narrative)

Upon validation, CVR transitions from State 4 (Finalized) to State 5 (Expected Return).

---

## Inputs

Read the T2 output files:
- `{output_dir}/{TICKER}_IRR_T2_{DATE}.md` (final narrative with A.13, A.14, N7)
- `{output_dir}/{TICKER}_A14_IRR_ANALYSIS.json` (kernel output)

Also read (for cross-validation):
- `{output_dir}/{TICKER}_A13_RESOLUTION_TIMELINE.json` (to verify ρ/CR were used correctly)

---

## Validation Checks

### 1. A.14 JSON Presence and Structure

**Check:** A.14_IRR_ANALYSIS JSON is present and well-formed.

**Required Top-Level Keys:**
- `schema_version` (should be "G3_2.2.5eIRR")
- `metadata` (company_name, ticker, analysis_date, current_price_p0, horizon, methodology, pipeline_fit_grade)
- `version_control`
- `transition_factor_analysis`
- `null_case_analysis`
- `fork_analysis`
- `irr_integration`
- `sanity_checks`
- `confidence_assessment`

**Fail:** Missing or malformed A.14 indicates kernel execution failure.

### 2. Kernel Execution Verification

**Check:** A.14 was produced by kernel, not fabricated.

**Pass Criteria:**
- T2 narrative contains evidence of Bash kernel execution
- Command trace shows: `python3 CVR_KERNEL_IRR_2.2.5e.py --a13 ... --inputs ... --output ...`
- No manual calculation of E[IRR], forks, or distribution
- `schema_version` matches kernel version (G3_2.2.5eIRR)

**Fail:** Evidence of fabricated results or manual calculation.

### 3. Transition Factor Analysis

**Check:** TF methodology correctly applied (Patch 2.3).

**Pass Criteria:**
- `methodology` = "TRANSITION_FACTOR"
- `market_multiple_t0` > 0
- `dcf_multiple_t0` > 0
- `market_dcf_ratio` = market_multiple_t0 / dcf_multiple_t0
- `transition_factor` calculated (TF = DCF_Multiple_T1 / DCF_Multiple_T0)
- `market_multiple_t1_null` = market_multiple_t0 × TF
- `convergence_rate_applied` matches A.13 `cr_final`
- `gap_t1`, `cr_contribution`, `adjusted_market_multiple_t1` all populated

**Fail:** Missing or invalid TF analysis indicates calculation error.

### 4. Null Case Analysis

**Check:** Null case IRR properly calculated and interpreted.

**Pass Criteria:**
- `null_case_irr` is a valid number
- `expected_price_t1_null` > 0
- `interpretation` explains null IRR vs discount rate relationship
- For fairly-valued stock (market_dcf_ratio ≈ 1.0), null_case_irr should ≈ dr_static

**Warn:** |null_case_irr - dr_static| > 0.08 without explanation (extreme mispricing or error).

### 5. Fork Analysis Completeness

**Check:** All feasible forks generated with valid valuations.

**Pass Criteria:**
- `forks` array is non-empty
- Fork count ≤ 2^N where N = scenario count (feasibility filtering applied)
- NULL fork is present (no scenarios active)
- Each fork has:
  - `fork_id`, `scenarios_active`, `fork_probability`
  - `fork_fundamentals` with revenue, ebitda, fcf, metric_used
  - `multiple_assignment` with TF-based calculation trace
  - `valuation_t1` with ev, net_debt, equity_value, price_t1
  - `fork_irr`
- Sum of `fork_probability` across all forks = 1.0 (±0.001 tolerance)

**Fail:** Missing forks or probabilities not summing to 1.0.

### 6. ρ Integration Verification

**Check:** Resolution percentages from A.13 were correctly applied.

**Pass Criteria:**
- Fork fundamentals show ρ-weighted blending (not full scenario impact)
- For each fork, `effective_magnitude` = ρ × full_magnitude
- `scenario_adjustment` in multiple_assignment reflects ρ weighting

**Fail:** ρ values ignored or incorrectly applied.

### 7. IRR Distribution Statistics

**Check:** Distribution statistics are complete and valid.

**Pass Criteria:**
- `e_irr` (expected IRR) is a valid number
- `irr_distribution` contains: p10, p25, p50_median, p75, p90, standard_deviation
- Percentiles are in ascending order (p10 < p25 < p50 < p75 < p90)
- `probability_above_hurdle` in [0, 1]
- `probability_of_loss` in [0, 1]
- `return_attribution` has: null_case_irr, scenario_resolution_contribution, total_e_irr
- `total_e_irr` ≈ `e_irr` (consistency check)

**Fail:** Missing or inconsistent distribution statistics.

### 8. Sanity Checks Execution

**Check:** All required sanity checks were run.

**Required Checks:**
- `null_irr_vs_dr_test` with: null_case_irr, discount_rate, market_dcf_ratio, deviation_from_dr, interpretation
- `fork_dispersion_check` with: irr_cv, irr_range, fundamentals_vary, interpretation
- `diagnostic_flags` with: average_rho_above_50, all_fork_irrs_positive, market_significantly_overvalued, market_significantly_undervalued, flags_triggered

**Pass Criteria:**
- All checks have results populated
- Interpretations are substantive (not placeholder)
- `flags_triggered` is an array (may be empty if no flags)

**Warn:** Any diagnostic flags triggered should be noted.

### 9. Null IRR vs DR Reasonableness

**Check:** Null case IRR relationship to DR is economically sensible.

**Pass Criteria:**
- If market_dcf_ratio < 1.0 (undervalued): null_case_irr > dr_static (expected upside)
- If market_dcf_ratio > 1.0 (overvalued): null_case_irr < dr_static (expected compression)
- If market_dcf_ratio ≈ 1.0 (fair): null_case_irr ≈ dr_static (return = cost of capital)
- Interpretation explains this relationship

**Warn:** Inverted relationship suggests calculation error.

### 10. Confidence Assessment

**Check:** Confidence assessment is complete.

**Pass Criteria:**
- `overall_confidence` is one of: HIGH, MEDIUM, LOW
- `key_uncertainties` is non-empty array
- `highest_leverage_assumptions` contains at least 1 entry with: assumption, current_value, sensitivity
- `recommendation_summary` is substantive

**Fail:** Missing confidence assessment.

### 11. N7 Narrative Presence

**Check:** Final output contains N7 (IRR Narrative).

**Pass Criteria:**
- T2 output contains identifiable N7 section (executive summary or IRR narrative)
- N7 summarizes: E[IRR], probability above hurdle, key drivers, confidence
- N7 references A.13 and A.14 findings
- N7 is coherent with A.14 quantitative results

**Fail:** Missing N7 narrative.

### 12. Final Document Completeness

**Check:** T2 output is the complete final IRR document.

**Pass Criteria:**
- A.13 is embedded or referenced (from T1)
- A.14 is embedded (from kernel execution)
- N7 narrative is present
- Document is self-contained for human review
- No placeholder sections or "TBD" content

**Fail:** Incomplete final document.

---

## Output Format

### PASS

```
IRR T2 VALIDATOR: PASS

Summary:
- A.14 Schema: Valid (G3_2.2.5eIRR)
- Kernel Execution: Verified via Bash
- E[IRR]: {value}% (P10: {p10}%, P50: {p50}%, P90: {p90}%)
- Probability Above Hurdle: {prob}%
- Null Case IRR: {null_irr}% vs DR: {dr}%
- Market/DCF Ratio: {ratio} ({interpretation})
- Forks Generated: {N} (probability sum: {sum})
- Sanity Checks: {passed/flags}
- Confidence: {level}
- N7 Narrative: Present

CVR State 5 (Expected Return) validated.
IRR stage complete.
```

### FAIL

```
IRR T2 VALIDATOR: FAIL

Critical Issues:
1. [Check N]: {Issue description}
   Location: {Artifact or section}
   Impact: {Why this fails validation}

Required Fixes:
- {Specific action to remediate}

Re-run T2 before finalizing IRR.
```

### WARN (Proceed with Caveats)

```
IRR T2 VALIDATOR: PASS WITH WARNINGS

Warnings:
1. [Check N]: {Issue description}

IRR stage complete with noted caveats.
```

---

## Validator Execution

1. Read T2 output files (narrative, A.14 JSON)
2. Parse all JSON blocks
3. Cross-reference with A.13 for ρ/CR consistency
4. Execute all checks above
5. Emit validation result

**Return:** Validation result only. Do NOT return full artifact content.

---

## State Transition

Upon PASS, the CVR transitions:
```
CVR_STATE_4 (Finalized Intrinsic Value)
    ↓
CVR_STATE_5 (Expected Return)
    = CVR_STATE_4 + A.13 + A.14
```

The IRR stage is the FINAL computational stage of the CAPY pipeline.

---

*END OF IRR T2 VALIDATOR*
