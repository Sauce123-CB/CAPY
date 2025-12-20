# INTEGRATION T3 Validator

> **Version:** 2.2.2e
> **Model:** Opus (REQUIRED - do NOT use Haiku)
> **Pattern:** 7 (Validators after each turn)

## Purpose

Validate INTEGRATION T3 (Final CVR Output) - the complete, finalized CVR State 4 document.

T3 produces the comprehensive unified document containing:
- All narratives N1-N9 (inherited and new)
- All artifacts A.1-A.12 embedded
- state_4_active_inputs for IRR consumption
- Complete audit trail for human review

**This is THE final output of the CAPY pipeline to date.**

---

## Inputs

Read the T3 output file:
- `{output_dir}/{TICKER}_INT_T3_{DATE}.md`

Also read (for cross-validation):
- T2 output to verify artifact fidelity

---

## Validation Checks

### 1. Document Structure

**Check:** T3 follows the required structure from Section V.D of the INTEGRATION prompt.

**Required Sections:**
- Executive Summary (N8: Final Investment Thesis)
- I. CVR Evolution Summary (N9)
- II. Investment Thesis Development (N1)
- III. Invested Capital Modeling (N2)
- IV. Economic Governor & Constraints (N3)
- V. Risk Assessment & DR Derivation (N4)
- VI. Enrichment Synthesis (N5)
- VII. Scenario Model Synthesis (N6)
- VIII. Adjudication Synthesis (N7)
- IX. Final Valuation Metrics
- X. MRC State 4 Artifacts

**Pass Criteria:**
- All required sections present with headers
- Sections appear in logical order
- No major sections missing

**Fail:** Missing sections make document incomplete for human review.

### 2. Narrative Completeness (N1-N9)

**Check:** All narratives are present and substantive.

**Narrative Inventory:**
| ID | Name | Source | Expected Content |
|----|------|--------|------------------|
| N1 | Investment Thesis | BASE→ENRICH | Multi-paragraph thesis |
| N2 | Invested Capital Modeling | BASE→ENRICH | IC structure narrative |
| N3 | Economic Governor | BASE→ENRICH | Terminal assumptions |
| N4 | Risk Assessment & DR | BASE→ENRICH | DR derivation trace |
| N5 | Enrichment Synthesis | ENRICH | Key refinements |
| N6 | Scenario Model Synthesis | SCENARIO | Scenario design, SSE |
| N7 | Adjudication Synthesis | INT T1/T2 | SC findings, dispositions |
| N8 | Final Investment Thesis | INT T3 | Synthesized post-adjudication view |
| N9 | CVR Evolution Summary | INT T3 | State 1→2→3→4 walkthrough |

**Pass Criteria:**
- Each narrative is non-empty
- Narratives are substantive (not single-sentence placeholders)
- N7-N9 reflect actual adjudication outcomes

**Fail:** Missing or placeholder narratives fail completeness requirement.

### 3. Artifact Embedment

**Check:** All artifacts A.1-A.12 are embedded in Section X.

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
- A.11_AUDIT_REPORT (or reference)
- A.12_INTEGRATION_TRACE
- state_4_active_inputs
- amendment_manifest

**Pass Criteria:**
- All artifacts present as complete JSON blocks
- JSON is well-formed (parseable)
- No truncation (arrays not cut short, all fields present)
- Artifacts match T2 output exactly (fidelity check)

**Fail:** Truncated or missing artifacts break downstream consumption.

### 4. Artifact-Narrative Consistency

**Check:** Narrative claims match embedded artifact values.

**Verification Points:**
- Executive summary E[IVPS] matches A.7/A.10 values
- State bridge metrics in N9 match A.12.state_bridge values
- Scenario descriptions in N6 match A.10 scenario definitions
- DR in N4 matches A.6 values
- Pipeline Fit grade in N7 matches A.12.pipeline_fit_handling.grade_received

**Pass Criteria:**
- Key numeric values consistent between narrative and artifacts
- No contradictions between text and JSON

**Fail:** Inconsistencies indicate regeneration drift rather than copy/paste.

### 5. No Deprecated Content

**Check:** T3 contains no stale State 3 references that should have been updated.

**Red Flags:**
- References to "State 3 E[IVPS]" when cascade changed values
- Scenario probabilities/magnitudes that differ from post-reconciliation values
- Pipeline Fit grades from individual SC instances when modal grade should be used
- Unrevised assumptions that were explicitly modified in adjudication

**Pass Criteria:**
- All values reflect post-adjudication State 4
- Clear "[State 4: Confirmed]" or "[State 4: Revised]" annotations where applicable
- No orphaned State 3 references

**Warn:** Deprecated content suggests incomplete revision.

### 6. No Duplication

**Check:** Narratives are not repeated or excessively duplicated.

**Pass Criteria:**
- Each narrative appears once in its designated section
- Artifacts appear once in Section X
- No copy-paste artifacts scattered throughout narrative sections

**Warn:** Duplication increases document size without benefit.

### 7. Executive Summary Accuracy

**Check:** Executive summary (N8) accurately summarizes the finalized valuation.

**Required Elements:**
- E[IVPS] (State 4 value)
- Key valuation metrics (DR, terminal values)
- Confidence characterization
- Pipeline Fit acknowledgment if grade C or below
- Synthesis of adjudication impact

**Pass Criteria:**
- All required elements present
- Values match embedded artifacts
- Confidence characterization reflects actual adjudication outcomes

**Fail:** Inaccurate executive summary misleads human readers.

### 8. Self-Containment

**Check:** Document is self-contained for human review.

**Pass Criteria:**
- Human analyst can understand the valuation without reading other files
- All referenced artifacts are embedded (not just referenced)
- Key concepts are explained (not assumed)
- Source citations are present where applicable

**Warn:** External dependencies reduce usability.

### 9. state_4_active_inputs Preservation

**Check:** state_4_active_inputs is copied verbatim from T2.

**Pass Criteria:**
- Exact match with T2 output
- No fields omitted
- No values changed
- Computational inputs preserved for IRR stage

**Fail:** Modified state_4_active_inputs breaks IRR execution.

### 10. File Size / Truncation Check

**Check:** Document is not truncated.

**Pass Criteria:**
- Document ends with "[END OF CVR STATE 4 FINAL VALUATION]" or equivalent
- All sections appear complete
- JSON blocks have matching braces
- No mid-sentence cutoffs

**Fail:** Truncation indicates context limits were exceeded.

---

## Output Format

### PASS

```
INT T3 VALIDATOR: PASS

Summary:
- Document Structure: Complete (all sections present)
- Narratives: N1-N9 present and substantive
- Artifacts: A.1-A.12 embedded and valid
- Artifact-Narrative Consistency: Verified
- Deprecated Content: None detected
- state_4_active_inputs: Preserved

Final Metrics:
- E[IVPS]: ${X.XX}
- Pipeline Fit Grade: {grade}
- Confidence: {characterization}

T3 validated. INTEGRATION stage complete.
CVR State 4 ready for human review and IRR stage.
```

### FAIL

```
INT T3 VALIDATOR: FAIL

Critical Issues:
1. [Check N]: {Issue description}
   Location: {Section or artifact}
   Impact: {Why this fails validation}

Required Fixes:
- {Specific action to remediate}

Re-run T3 to produce complete CVR State 4.
```

### WARN (Proceed with Caveats)

```
INT T3 VALIDATOR: PASS WITH WARNINGS

Warnings:
1. [Check N]: {Issue description}

CVR State 4 is usable but note caveats above.
```

---

## Validator Execution

1. Read T3 output file
2. Verify document structure
3. Check all narratives present
4. Parse and validate all artifacts
5. Cross-reference with T2 for consistency
6. Execute all checks above
7. Emit validation result

**Return:** Validation result only. Do NOT reproduce the full document.

---

## Post-Validation

Upon successful validation:
- INTEGRATION stage is complete
- CVR State 4 is the authoritative final valuation
- Document is ready for:
  - Human analyst review
  - IRR stage consumption
  - Audit trail purposes

---

*END OF INT T3 VALIDATOR*
