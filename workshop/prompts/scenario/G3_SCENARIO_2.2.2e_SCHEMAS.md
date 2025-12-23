# G3 SCENARIO 2.2.2e: SCHEMAS

> **Version:** 2.2.2e (Atomized)
> **Contains:** Appendix A.1 (Turn 1 Output Schema) and Appendix A.2 (Final Output Schema)

APPENDIX A.1: Turn 1 Output Schema (Scenario Execution Arguments)

This schema defines the JSON structure emitted by Turn 1 for consumption
by Turn 2.

{

"schema_version": "G3_2.2.2eS_T1_ARGS",

"generation_timestamp": "string (ISO 8601)",

"metadata": { \... },

"scenario_definitions": \[ { scenario_id, scenario_name, scenario_type,
probability_estimation, intervention_definition } \],

"integration_constraints": { causal_dependencies,
mutual_exclusivity_groups, economic_incompatibilities },

"trace_documentation": { research_sources_analyzed,
candidate_scenarios_considered, methodology_notes }

}

Usage: Turn 2 parses this JSON to extract scenario definitions and
constraints, then executes kernel functions with these parameters.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

APPENDIX A.2: Final Output Schema (A.10_SCENARIO_MODEL_OUTPUT)

{

\"schema_version\": \"G3_2.2.2eS\",

\"version_control\": {

\"paradigm\": \"G3 Meta-Prompting Doctrine v2.4 (Two-Shot Guided
Autonomy)\",

\"pipeline_stage\": \"SCENARIO G3_2.2.2e\",

\"execution_model\": \"Two-Shot (T1=Analysis, T2=Execution)\",

\"base_compatibility\": \"G3BASE 2.2.2e\",

\"rq_compatibility\": \"G3RQ 2.2.3e\",

\"enrich_compatibility\": \"G3ENRICH 2.2.2e\"

},

\"metadata\": {

\"company_name\": \"string\",

\"ticker\": \"string (EXCHANGE:SYMBOL)\",

\"valuation_date\": \"string (YYYY-MM-DD)\",

\"currency\": \"string (e.g., USD)\",

\"execution_timestamp\": \"string (ISO 8601)\",

\"base_case_reference\": {

\"source_stage\": \"G3_ENRICHMENT_2.2.2e\",

\"state_2_ivps\": \"float (Deterministic IVPS from ENRICHMENT)\",

\"dr_static\": \"float (Discount Rate)\",

\"terminal_g\": \"float (Base Case terminal growth rate)\",

\"terminal_roic\": \"float (Base Case terminal ROIC)\",

\"shares_outstanding\": \"float (Static Diluted Shares, TSM Adjusted)\"

}

},

\"scenario_definitions\": \[

{

\"scenario_id\": \"string (Unique identifier, e.g., S1_ACQUISITION)\",

\"scenario_name\": \"string (Descriptive name)\",

\"scenario_type\": \"string (MAINLINE \| BLUE_SKY \| BLACK_SWAN)\",

\"description\": \"string (Narrative description of the event, its
trigger conditions, and expected economic impact)\",

\"probability_estimation\": {

\"methodology\": \"Bayesian Probability Protocol (P3)\",

\"prior_establishment\": {

\"reference_class\": \"string (Description of the chosen reference
class)\",

\"reference_class_justification\": \"string (Why this reference class is
appropriate)\",

\"data_sources\": \[

\"string (RQ citations or other data sources)\"

\],

\"sample_size\": \"integer \| string (Number of observations or
\'Limited\')\",

\"data_recency\": \"string (e.g., \'Last 10 years\', \'2015-2024\')\",

\"p_prior\": \"float (The Outside View base rate, 0.0 to 1.0)\"

},

\"causal_decomposition\": {

\"prerequisite_chain_description\": \"string (Narrative description of
the causal pathway)\",

\"probability_structure\": \"string (Mathematical structure, e.g.,
\'P(A) × P(B\|A) × P(C\|A,B)\')\",

\"conditional_components\": \[

{

\"condition_id\": \"string (e.g., C1, C2)\",

\"condition_description\": \"string\",

\"p_conditional\": \"float\",

\"evidence_justification\": \"string (The Inside View ---
company-specific evidence supporting this estimate)\"

}

\]

},

\"posterior_calculation\": {

\"p_posterior\": \"float (Final probability estimate, 0.0 to 1.0)\",

\"posterior_derivation\": \"string (How the posterior was calculated
from the decomposition)\",

\"calibration_check\": {

\"triggered\": \"boolean (True if P \> 0.70 for upside or P \< 0.10 for
downside)\",

\"sanity_check_narrative\": \"string \| null (Required if triggered ---
explicit reasoning on calibration)\"

}

}

},

\"intervention_definition\": {

\"intervention_type\": \"string (PARAMETRIC \| STRUCTURAL \| HYBRID)\",

\"intervention_type_rationale\": \"string (P1 judgment --- why this type
was selected)\",

\"gim_overlay\": {

\"description\": \"object \| null (Included if PARAMETRIC or HYBRID.
Contains ONLY the GIM entries that differ from Base Case. Uses standard
GIM/DSL structure.)\",

\"modified_drivers\": \[

{

\"driver_handle\": \"string (Reference to GIM driver)\",

\"base_case_value\": \"string (Summary of Base Case assumption)\",

\"scenario_value\": {

\"type\": \"string (DSL type: STATIC \| LINEAR_FADE \| CAGR_INTERP \|
S_CURVE \| EXPLICIT_SCHEDULE)\",

\"parameters\": \"object (DSL parameters per B.2)\"

},

\"modification_rationale\": \"string (Why this driver changes under this
scenario)\"

}

\]

},

\"structural_modifications\": {

\"description\": \"array \| null (Included if STRUCTURAL or HYBRID.
Defines changes to DAG/SCM structure.)\",

\"modifications\": \[

{

\"modification_id\": \"string\",

\"target_artifact\": \"string (CAUSAL_DAG \| STRUCTURAL_EQ)\",

\"modification_type\": \"string (ADD_NODE \| REMOVE_NODE \|
MODIFY_EQUATION \| ADD_EDGE)\",

\"target_node\": \"string (Node being modified or added)\",

\"details\": {

\"new_equation\": \"string \| null (If modifying equation)\",

\"new_edges\": \"array \| null (If adding edges, list of parent
nodes)\",

\"node_definition\": \"object \| null (If adding node, full node spec)\"

},

\"rationale\": \"string\"

}

\]

},

\"dr_overlay\": {

\"applied\": \"boolean\",

\"dr_scenario\": \"float \| null (Scenario-specific DR, if applied)\",

\"dr_delta\": \"float \| null (Change from base DR)\",

\"risk_realignment_justification\": \"string \| null (Required if
applied --- P2 mandate. Must explain the fundamental change in
systematic risk.)\"

}

},

\"magnitude_estimation\": {

\"execution_method\": \"CVR Kernel execute_scenario_intervention()\",

\"ivps_scenario\": \"float (Deterministic IVPS calculated under this
scenario)\",

\"ivps_impact\": \"float (IVPS_scenario - Base Case IVPS; positive =
upside, negative = downside)\",

\"ivps_impact_percent\": \"float (ivps_impact / Base Case IVPS × 100)\",

\"p2_reconciliation\": {

\"status\": \"string (PASS \| FAIL)\",

\"terminal_g_scenario\": \"float\",

\"terminal_roic_scenario\": \"float\",

\"economic_governor_check\": \"string (Narrative confirming g ≈ ROIC ×
RR and g \< DR)\",

\"reconciliation_notes\": \"string \| null (Additional notes if edge
cases encountered)\"

},

\"key_forecast_deltas\": {

\"description\": \"object (Optional --- key metrics showing scenario vs.
base case)\",

\"y5_revenue_delta_pct\": \"float \| null\",

\"y10_ebit_margin_delta_pct\": \"float \| null\",

\"y20_fcf_delta_pct\": \"float \| null\"

}

}

}

\],

\"integration_model\": {

\"methodology\": \"Structured State Enumeration (SSE) with
Initialize-Filter-Renormalize (B.8)\",

\"execution_method\": \"Kernelized SSE (calculate_sse_jpd)\",

\"constraints\": {

\"causal_dependencies\": \[

{

\"dependent_scenario\": \"string (scenario_id that is conditionally
dependent)\",

\"condition_scenario\": \"string (scenario_id that must occur)\",

\"p_conditional\": \"float (P(Dependent \| Condition))\",

\"dependency_rationale\": \"string\"

}

\],

\"mutual_exclusivity_groups\": \[

{

\"group_id\": \"string (e.g., MECE_1)\",

\"scenarios\": \[\"array of scenario_ids that are mutually
exclusive\"\],

\"root_event\": \"string (The common root event these scenarios
represent different outcomes of)\",

\"rationale\": \"string\"

}

\],

\"economic_incompatibilities\": \[

{

\"scenario_pair\": \[\"scenario_id_1\", \"scenario_id_2\"\],

\"incompatibility_rationale\": \"string (Why these cannot co-occur)\"

}

\]

},

\"sse_execution_results\": {

\"total_states_enumerated\": \"integer (2\^N where N = number of
scenarios)\",

\"feasible_states_count\": \"integer (States remaining after
filtering)\",

\"infeasible_states_count\": \"integer (States eliminated by
constraints)\",

\"renormalization_factor\": \"float (1.0 / sum of feasible initial
probabilities)\",

\"probability_sum_validation\": \"float (Should equal 1.0 within
epsilon)\"

}

},

\"state_enumeration\": \[

{

\"state_id\": \"string (e.g., \'BASE\', \'S1\', \'S2\', \'S1_S2\',
\'S1_S3_S4\')\",

\"state_description\": \"string (Human-readable description of this
state of the world)\",

\"scenarios_active\": \[\"array of scenario_ids occurring in this state
(empty array for Base Case)\"\],

\"feasibility_status\": \"string (FEASIBLE \| INFEASIBLE_MECE \|
INFEASIBLE_INCOMPATIBLE)\",

\"probability_calculation\": {

\"p_initial\": \"float (Probability before filtering/renormalization)\",

\"p_initial_derivation\": \"string (e.g., \'P(S1) × P(\~S2) × P(S3) =
0.25 × 0.90 × 0.15\')\",

\"p_final\": \"float (Probability after renormalization; 0.0 if
infeasible)\",

\"cumulative_probability\": \"float (Running sum for percentile
calculation, ordered by IVPS ascending)\"

},

\"valuation_calculation\": {

\"ivps_raw\": \"float (Base IVPS + sum of active scenario impacts)\",

\"ivps_raw_derivation\": \"string (e.g., \'45.00 + 15.00 + (-8.00) =
52.00\')\",

\"limited_liability_applied\": \"boolean (True if ivps_raw was
negative)\",

\"ivps_final\": \"float (MAX(0.0, ivps_raw))\"

}

}

\],

\"probabilistic_valuation_summary\": {

\"primary_output\": {

\"e_ivps\": \"float (Expected IVPS --- probability-weighted mean)\",

\"e_ivps_derivation\": \"string (Sum of P(State) × IVPS(State))\"

},

\"distribution_statistics\": {

\"median_p50\": \"float (IVPS at 50th percentile)\",

\"p10\": \"float (IVPS at 10th percentile --- downside)\",

\"p25\": \"float (IVPS at 25th percentile)\",

\"p75\": \"float (IVPS at 75th percentile)\",

\"p90\": \"float (IVPS at 90th percentile --- upside)\",

\"min_ivps\": \"float (Minimum IVPS across feasible states, floored at
0.0)\",

\"max_ivps\": \"float (Maximum IVPS across feasible states)\",

\"range\": \"float (max_ivps - min_ivps)\",

\"standard_deviation\": \"float\",

\"coefficient_of_variation\": \"float (std_dev / e_ivps)\"

},

\"distribution_shape\": {

\"skewness\": \"string (LEFT \| SYMMETRIC \| RIGHT)\",

\"skewness_interpretation\": \"string (What drives the asymmetry)\",

\"modality\": \"string (UNIMODAL \| BIMODAL \| MULTIMODAL)\",

\"modality_interpretation\": \"string (What creates multiple modes, if
applicable)\"

},

\"distribution_visualization\": {

\"ascii_representation\": \"string (Human-readable ASCII bar chart of
probability mass by IVPS bucket)\",

\"structured_data\": \[

{

\"ivps_bucket_label\": \"string (e.g., \'\$0-10\', \'\$40-50\')\",

\"ivps_bucket_midpoint\": \"float\",

\"probability_mass\": \"float\",

\"cumulative_probability\": \"float\"

}

\]

},

\"probability_sensitivity_analysis\": {

\"description\": \"Analysis of which scenario probabilities have the
largest marginal impact on E\[IVPS\]\",

\"sensitivities\": \[

{

\"scenario_id\": \"string\",

\"delta_p\": \"float (e.g., 0.10 for +10% probability shift)\",

\"delta_e_ivps\": \"float (Change in E\[IVPS\] for the probability
shift)\",

\"sensitivity_ratio\": \"float (delta_e_ivps / delta_p)\",

\"interpretation\": \"string\"

}

\]

}

},

\"analytical_synthesis\": {

\"executive_summary\": \"string (High-value narrative: key insights from
the probabilistic analysis, the meaning of the distribution shape,
comparison of E\[IVPS\] to deterministic Base Case, and overall
risk/reward characterization)\",

\"cvr_state_bridge\": {

\"state_2_ivps_deterministic\": \"float\",

\"state_3_e_ivps_probabilistic\": \"float\",

\"delta\": \"float\",

\"delta_percent\": \"float\",

\"delta_attribution\": \"string (Which scenarios and probability weights
drive the difference between deterministic and expected value)\"

},

\"risk_assessment\": {

\"downside_exposure\": {

\"p10_ivps\": \"float\",

\"p10_vs_base_case\": \"float (percentage)\",

\"downside_probability\": \"float (Probability of IVPS \< Base Case)\",

\"interpretation\": \"string (What the P10 outcome means for investment
risk)\"

},

\"upside_potential\": {

\"p90_ivps\": \"float\",

\"p90_vs_base_case\": \"float (percentage)\",

\"upside_probability\": \"float (Probability of IVPS \> Base Case × 1.5
or similar threshold)\",

\"interpretation\": \"string (What must materialize for upside; how
realistic)\"

},

\"tail_risk_characterization\": \"string (Assessment of extreme outcomes
--- is there meaningful probability of zero/total loss? Of 3x+
returns?)\"

},

\"investment_implications\": {

\"position_sizing_guidance\": \"string (How the distribution shape
should inform position size)\",

\"entry_timing_considerations\": \"string (Are there scenario resolution
events that suggest waiting or urgency?)\",

\"risk_management_considerations\": \"string (Hedging approaches given
tail exposures)\",

\"key_monitoring_indicators\": \[\"array of metrics/events to watch for
scenario probability updates\"\]

}

},

\"trace_documentation\": {

\"scenario_identification_log\": {

\"research_sources_analyzed\": \[\"array of RQ IDs or research document
references\"\],

\"candidate_scenarios_considered\": \[

{

\"scenario_name\": \"string\",

\"preliminary_p\": \"float\",

\"preliminary_m\": \"float\",

\"expected_impact\": \"float (\|P × M\|)\",

\"selection_status\": \"string (SELECTED \| REJECTED)\",

\"rejection_reason\": \"string \| null\"

}

\],

\"distributional_completeness_check\": \"string (Confirmation that
selected scenarios span upside/downside)\"

},

\"methodology_notes\": {

\"probability_estimation_notes\": \"string (Any challenges or judgment
calls in P estimation)\",

\"intervention_design_notes\": \"string (Any challenges in translating
scenarios to SCM interventions)\",

\"integration_notes\": \"string (Any edge cases in SSE execution)\"

},

\"limitations_and_caveats\": \"string (Explicit acknowledgment of model
limitations, data gaps, or areas of high uncertainty)\"

}

}

---

## Kernel Execution Contract (MANDATORY)

**The CVR kernel uses `eval()` on DAG equations.** This section documents the exact schema requirements for kernel compatibility. Violations cause kernel bypass or runtime errors.

### 1. DAG Equation Syntax

**Exogenous drivers MUST have empty equations:**
```json
"Revenue_Growth": {
  "type": "Exogenous_Driver",
  "parents": [],
  "equation": ""
}
```
- Exogenous drivers get their values from the GIM, not from equations
- Non-empty equations on exogenous drivers cause `eval()` errors
- Pseudo-code like `"f(x, y, z)"` will FAIL

**Derived nodes MUST use executable Python with GET()/PREV():**
```json
"Revenue": {
  "type": "Financial_Line_Item",
  "parents": ["Revenue_Prior", "Revenue_Growth"],
  "equation": "PREV('Revenue') * (1 + GET('Revenue_Growth'))"
}
```
- `GET('Var')` retrieves current-period value
- `PREV('Var')` retrieves prior-period value
- Equation must be valid Python that can be passed to `eval()`

### 2. GIM-DAG Name Matching (CRITICAL)

**GIM driver names MUST exactly match DAG node names:**
```json
// DAG
"Revenue_SaaS_Growth": {
  "type": "Exogenous_Driver",
  "parents": [],
  "equation": ""
}

// GIM - MUST use identical key
"Revenue_SaaS_Growth": {
  "mode": "LINEAR_FADE",
  "params": {...}
}
```
- Kernel loads GIM values using DAG node names as keys
- Mismatched names (e.g., `"SaaS_Growth"` vs `"Revenue_SaaS_Growth"`) cause silent failures
- Kernel code: `if handle in dag:` - names must match exactly

### 3. EXPLICIT_SCHEDULE Key Format

**Schedule keys MUST be numeric strings, not year labels:**
```json
// CORRECT
"params": {
  "schedule": {
    "1": 837,
    "2": 0,
    "3": 0
  }
}

// WRONG - will cause ValueError
"params": {
  "schedule": {
    "Y1": 837,
    "Y2": 0,
    "Y3": 0
  }
}
```
- Kernel parses keys with `int(key)`
- `"Y1"` causes `ValueError: invalid literal for int() with base 10: 'Y1'`

### 4. Coverage Manifest Requirements

**coverage_manifest MUST list ALL nodes present in Y0_data:**
```json
"coverage_manifest": {
  "Revenue": "Total revenue",
  "Revenue_SaaS": "SaaS segment revenue",
  "EBIT": "Earnings before interest and taxes",
  // ... every node in Y0_data needs an entry
}
```
- Kernel validates that all Y0_data keys have manifest entries
- Missing entries cause `RuntimeError: DAG Coverage Warning`
- Include even "obvious" items like `Revenue`, `EBIT`, `NOPAT`

### 5. A.6 DR Trace Key Path

**DR trace MUST use `derivation_trace` as top-level key:**
```json
{
  "schema_version": "G3_2.2.3e",
  "derivation_trace": {
    "DR_Static": 0.20,
    "RFR": 0.045,
    "ERP": 0.05,
    "X": 1.8
  }
}
```
- Kernel accesses: `dr_trace['derivation_trace']['DR_Static']`
- Using `"dr_derivation"` or other keys causes `KeyError`

### Kernel Contract Checklist

Before kernel execution, verify:

- [ ] All `Exogenous_Driver` nodes have `"equation": ""`
- [ ] All derived nodes have executable Python equations with `GET()`/`PREV()`
- [ ] GIM keys exactly match DAG node names
- [ ] EXPLICIT_SCHEDULE uses numeric keys (`"1"`, `"2"`, not `"Y1"`, `"Y2"`)
- [ ] coverage_manifest includes ALL Y0_data node names
- [ ] A.6 uses `derivation_trace.DR_Static` key path
