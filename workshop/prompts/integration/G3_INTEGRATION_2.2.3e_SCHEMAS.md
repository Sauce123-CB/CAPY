APPENDIX A: Schemas

A.12_INTEGRATION_TRACE Schema

json

{

\"schema_version\": \"G3_2.2.2eI\",

\"metadata\": {

\"company_name\": \"string\",

\"ticker\": \"string (EXCHANGE:SYMBOL)\",

\"valuation_date\": \"string (YYYY-MM-DD)\",

\"execution_timestamp\": \"string (ISO 8601)\",

\"integration_summary\": {

\"total_findings_reviewed\": \"integer\",

\"critical_findings\": \"integer\",

\"high_findings\": \"integer\",

\"medium_findings\": \"integer\",

\"findings_accepted\": \"integer\",

\"findings_rejected\": \"integer\",

\"findings_modified\": \"integer\",

\"scenarios_substituted\": \"boolean\",

\"recalculation_performed\": \"boolean\",

\"pipeline_fit_grade\": \"string (A\|B\|C\|D\|F)\",

\"sc_instances_synthesized\": \"integer (number of parallel SC reports processed)\"

}

},

\"audit_synthesis\": {

\"sc_instances_received\": \[

\"string (List of SC instance abbreviations: G3PTR, C45ET, O3H, etc.)\"

\],

\"pipeline_fit_grades\": {

\"per_instance\": \"object (mapping of SC instance → grade)\",

\"modal_grade\": \"string (A\|B\|C\|D\|F)\",

\"grade_range\": \"string (e.g., 'B-C' if grades varied)\"

},

\"concordance_analysis\": \[

{

\"finding_id\": \"string (F1, F2, ...)\",

\"flagged_by\": \[\"string (List of SC instances that flagged this)\"\],

\"concordance_status\": \"string (CONCORDANT\|DISCORDANT)\",

\"priority_variance\": \"string or null (e.g., 'HIGH vs MEDIUM' if disagreement)\"

}

\],

\"synthesis_notes\": \"string (Narrative explaining synthesis decisions and conflict resolutions)\"

},

\"executive_summary\": {

\"adjudication_outcome\": \"string (Narrative summary of key
adjudication decisions and their impact)\",

\"material_changes\": \[

\"string (Bullet points of most significant State 3 → State 4
modifications)\"

\],

\"confidence_assessment\": \"string (Overall confidence in State 4
reliability, incorporating Pipeline Fit considerations)\"

},

\"adjudication_log\": \[

{

\"finding_id\": \"string (F1, F2, \...)\",

\"source_reference\": \"string (A.11 section/objective reference, with SC instance attribution)\",

\"priority\": \"string (CRITICAL\|HIGH\|MEDIUM)\",

\"category\": \"string
(SOURCE_INTEGRITY\|PIPELINE_FIT\|PROBABILITY_ESTIMATION\|SCENARIO_DESIGN\|DISTRIBUTIONAL_ANALYSIS\|METHODOLOGY_COMPLIANCE\|OTHER)\",

\"claim_summary\": \"string (Concise statement of the audit finding)\",

\"evidence_consulted\": \[

{

\"source_type\": \"string
(PRIMARY_DOC\|DISCOVERY_RECORD\|VERIFICATION_SEARCH\|STATE_3_ARTIFACT)\",

\"source_reference\": \"string (Document name, search query, or artifact
ID)\",

\"relevant_content\": \"string (Brief summary of evidence found)\"

}

\],

\"disposition\": \"string (ACCEPT\|REJECT\|MODIFY)\",

\"disposition_rationale\": \"string (Detailed reasoning applying P1
hierarchy and P6 symmetric burden)\",

\"modification_specification\": {

\"affected_artifact\": \"string (e.g., A.5_GIM, A.10_SCENARIO_S2, null
if REJECT)\",

\"affected_element\": \"string (e.g., \'Revenue_Growth_Y1-Y3\',
\'S2_probability\', null if REJECT)\",

\"pre_adjudication_value\": \"string\|number\|null\",

\"post_adjudication_value\": \"string\|number\|null\",

\"cascade_triggered\": \"string
(FULL\|PARTIAL_SCENARIO\|PARTIAL_SSE\|NONE)\"

}

}

\],

\"verification_search_log\": \[

{

\"search_id\": \"string (VS1, VS2, \...)\",

\"related_finding_id\": \"string (F1, F2, \...)\",

\"search_purpose\": \"string
(CONFIRM_A10_CLAIM\|REFUTE_A10_CLAIM\|VERIFY_A9_ASSUMPTION\|RETRIEVE_UPDATED_DATA)\",

\"search_query\": \"string\",

\"search_timestamp\": \"string (ISO 8601)\",

\"results_summary\": \"string (Brief summary of findings)\",

\"evidentiary_impact\": \"string (How this affected the adjudication)\"

}

\],

\"scenario_reconciliation\": {

\"substitution_performed\": \"boolean\",

\"pre_reconciliation_scenarios\": \[

{

\"scenario_id\": \"string\",

\"scenario_name\": \"string\",

\"p_posterior\": \"float\",

\"ivps_impact\": \"float\",

\"expected_materiality\": \"float (\|P × M\|)\",

\"source\": \"string (STATE_3\|A10_PROPOSED)\"

}

\],

\"post_reconciliation_scenarios\": \[

{

\"scenario_id\": \"string\",

\"scenario_name\": \"string\",

\"p_posterior\": \"float\",

\"ivps_impact\": \"float\",

\"expected_materiality\": \"float\",

\"status\": \"string (RETAINED\|ADDED\|DISPLACED)\"

}

\],

\"displaced_scenarios\": \[

{

\"scenario_id\": \"string\",

\"displacement_rationale\": \"string\"

}

\],

\"distributional_completeness_check\": {

\"upside_coverage\": \"boolean\",

\"downside_coverage\": \"boolean\",

\"balance_assessment\": \"string\"

}

},

\"recalculation_cascade\": {

\"cascade_executed\": \"boolean\",

\"cascade_scope\": \"string
(FULL\|PARTIAL_SCENARIO\|PARTIAL_SSE\|NONE)\",

\"modifications_triggering_cascade\": \[

\"string (References to finding_ids that required recalculation)\"

\],

\"execution_log\": {

\"base_case_recalculated\": \"boolean\",

\"scenarios_recalculated\": \[\"string (scenario_ids)\"\],

\"sse_recalculated\": \"boolean\"

},

\"validation_checks\": {

\"economic_governor_satisfied\": \"boolean\",

\"probability_sum_validated\": \"boolean\",

\"limited_liability_enforced\": \"boolean\",

\"validation_notes\": \"string\|null\"

}

},

\"dr_revision\": {

\"dr_revised\": \"boolean\",

\"prior_dr\": \"float | null\",

\"posterior_dr\": \"float | null\",

\"delta_dr\": \"float | null\",

\"finding_id\": \"string | null (F1, F2, ... reference)\",

\"x_component_affected\": \"string | null (e.g., 'governance_risk', 'financial_risk')\",

\"evidence_justification\": \"string | null\"

},

\"state_bridge\": {

\"state_3_summary\": {

\"e_ivps\": \"float\",

\"p10\": \"float\",

\"p50\": \"float\",

\"p90\": \"float\",

\"std_dev\": \"float\",

\"skewness\": \"string (LEFT\|SYMMETRIC\|RIGHT)\",

\"scenario_count\": \"integer\"

},

\"state_4_summary\": {

\"e_ivps\": \"float\",

\"p10\": \"float\",

\"p50\": \"float\",

\"p90\": \"float\",

\"std_dev\": \"float\",

\"skewness\": \"string (LEFT\|SYMMETRIC\|RIGHT)\",

\"scenario_count\": \"integer\"

},

\"delta_analysis\": {

\"e_ivps_change_absolute\": \"float\",

\"e_ivps_change_percent\": \"float\",

\"distribution_shape_change\": \"string\|null\",

\"primary_drivers_of_change\": \[

\"string (Description of key modifications driving the delta)\"

\]

}

},

\"pipeline_fit_handling\": {

\"grade_received\": \"string (A\|B\|C\|D\|F)\",

\"handling_protocol_applied\": \"string
(PROCEED\|PROCEED_WITH_CAVEATS\|WARNING_EMITTED\|BLOCK_RECOMMENDATION)\",

\"confidence_discount_narrative\": \"string\|null (Required for grades
C, D, F)\",

\"material_blind_spots\": \[

{

\"blind_spot\": \"string\",

\"severity\": \"string (HIGH\|MEDIUM\|LOW)\",

\"directional_bias\": \"string (OVERSTATES\|UNDERSTATES\|UNCERTAIN)\",

\"interpretation_guidance\": \"string\"

}

\],

\"orchestrator_notes\": \"string\|null (Any recommendations for human
review)\"

},

\"investment_implications_update\": {

\"risk_reward_materially_changed\": \"boolean\",

\"updated_assessment\": \"string\|null (If materially changed, narrative
on revised implications)\",

\"position_sizing_implications\": \"string\|null\",

\"timing_considerations\": \"string\|null\",

\"risk_management_considerations\": \"string\|null\"

},

\"trace_metadata\": {

\"integration_duration_estimate\": \"string (e.g., \'Approximately X
minutes of execution\')\",

\"total_verification_searches\": \"integer\",

\"artifacts_amended\": \[\"string (List of artifact IDs modified, if
any)\"\],

\"version_control_note\": \"string (e.g., \'Original A.10 preserved;
amendments documented above\')\"

},

\"final_thesis_synthesis\": {

\"original_thesis_anchor\": \"string (1-2 sentence summary of the
original BASE investment thesis)\",

\"adjudication_impact\": \"string (Narrative explaining how audit
findings modified, validated, or challenged the original thesis)\",

\"state_4_thesis\": \"string (Synthesized investment thesis reflecting
the post-adjudication perspective. This must reconcile any tension
between the original view and accepted audit critiques.)\",

\"key_thesis_modifications\": \[

{

\"original_claim\": \"string (What the BASE thesis asserted)\",

\"modification\": \"string (How this was changed by adjudication)\",

\"supporting_finding_ids\": \[\"string (F1, F2, \... references)\"\]

}

\],

\"confidence_characterization\": \"string (Overall confidence in State 4
reliability: HIGH, MEDIUM, LOW, with brief rationale incorporating
Pipeline Fit grade and adjudication outcomes)\",

\"residual_uncertainties\": \[\"string (Key uncertainties that persist
even after adjudication)\"\]

}

}

\`\`\`

\## State 4 Specification

\*\*CVR State 4 Definition:\*\*

State 4 is not a new consolidated artifact but a logical state
comprising:

\`\`\`

CVR_STATE_4 = {

A.1_EPISTEMIC_ANCHORS, // From State 3 (amended if adjudication
required)

A.2_ANALYTIC_KG, // From State 3 (amended if adjudication required;
includes ATP metadata and accounting_translation_log)

A.3_CAUSAL_DAG, // From State 3 (amended if adjudication required)

A.5_GESTALT_IMPACT_MAP, // From State 3 (amended if adjudication
required)

A.6_DR_DERIVATION_TRACE, // From State 3 (amended if adjudication required per P7)

A.7_LIGHTWEIGHT_VALUATION_SUMMARY, // Recalculated if cascade triggered

A.8_RESEARCH_STRATEGY_MAP, // From State 3 (immutable)

A.9_ENRICHMENT_TRACE, // From State 3 (immutable)

A.10_SCENARIO_MODEL_OUTPUT, // From State 3 (amended if scenarios
modified)

A.11_AUDIT_REPORT, // From Silicon Council (immutable, for reference)

A.12_INTEGRATION_TRACE // NEW: The adjudication record

}

Amendment Protocol: When adjudication modifies a State 3 artifact:

\* The artifact\'s schema_version is updated to include an \"I\" suffix
(e.g., \"G3_2.2.2eI\" → \"G3_2.2.2eI-A\")

\* A.11 documents the pre- and post-modification values

\* The original values are preserved in A.11 for audit trail purposes

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

---

