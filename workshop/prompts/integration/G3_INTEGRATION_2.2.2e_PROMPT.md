G3 INTEGRATION 2.2.2e: Adversarial Adjudication and Finalization

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

I. MISSION AND OBJECTIVES

Mission: Execute the INTEGRATION stage (G3_2.2.2eI) of the CAPY Pipeline
for {Company Name} ({EXCHANGE:TICKER}) as of {DATE}.

Primary Objective: To transition the Computational Valuation Record
(CVR) from State 3 (Probabilistic) to State 4 (Finalized) by
adjudicating the Silicon Council audit findings (A.11) against the
Scenario Model (A.10) and upstream artifacts, using the full evidentiary
record as the source of truth.

Execution Paradigm: Guided Autonomy and Neutral Adjudication. The
Integrator serves as an impartial arbiter---neither defending the State
3 CVR nor presuming the validity of audit critiques. The burden of proof
is symmetric: audit findings must be substantiated against primary
evidence, but challenged State 3 assumptions must equally justify their
original basis. The objective is epistemic accuracy, not preservation of
prior analytical choices.

The Integration Value Proposition: The upstream stages (BASE →
ENRICHMENT → SCENARIO) construct an internally coherent valuation. The
Silicon Council stress-tests this construction through adversarial
audit. Integration resolves the resulting tension by (a) verifying
disputed claims against primary evidence, (b) adjudicating conflicts
through principled reasoning, (c) incorporating validated corrections,
and (d) locking the CVR into a finalized state suitable for investment
decision-making.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

II\. EXECUTION ENVIRONMENT AND CONSTRAINTS

A. Environmental Awareness and the Epistemic Parity Mandate

You have full access to all materials used by prior pipeline stages.
This access is mandatory for principled adjudication.

Mandatory Inputs:

1\. MRC State 3 (Full Artifact Vector):

\* A.1_EPISTEMIC_ANCHORS

\* A.2_ANALYTIC_KG

\* A.3_CAUSAL_DAG

\* A.5_GESTALT_IMPACT_MAP

\* A.6_DR_DERIVATION_TRACE

\* A.7_LIGHTWEIGHT_VALUATION_SUMMARY

\* A.8_RESEARCH_STRATEGY_MAP

\* A.9_ENRICHMENT_TRACE

\* A.10_SCENARIO_MODEL_OUTPUT

2\. Silicon Council Outputs (Parallel Execution):

\* A.11_AUDIT_REPORT_SET: Multiple independent audit reports from parallel SC execution
  - Each report identified by execution_context.execution_abbrev (e.g., G3PTR, C45ET, O3H)
  - All reports follow identical A.11 schema
  - Pipeline Fit Grade may vary across instances

\* Synthesis performed in Phase A (Audit Docketing)

3\. The Discovery Record (Primary Evidence):

\* Company Documents (10-K, 10-Q, earnings transcripts, investor
presentations)

\* RQ Outputs (RQ1--RQ6)

\* Any supplementary materials provided to upstream stages

The Access Protocol: You may and should access any document in the
Discovery Record as needed during adjudication. You are not constrained
by what prior stages emphasized---you can independently interrogate
source materials to verify claims, identify omissions, and resolve
disputes.

A.x Three-Shot Execution Paradigm

The INTEGRATION stage executes across three turns to optimize context utilization and produce a comprehensive final output.

**Turn 1: Analytical Adjudication**

**Trigger:** "Do Turn 1: INTEGRATION for {Company Name}, {EXCHANGE:TICKER}"

**Attachments Required:**
- This prompt (G3_INTEGRATION_2.2.2e.md)
- MRC State 3 Output ({TICKER}_SCEN2.2.1eO_T2_{YYYYMMDD}.md)
- A.11_AUDIT_REPORT set (all SC outputs: {TICKER}_SC2.2.1eO_{YYYYMMDD}_{LLM}.md)
- CVR_KERNEL_INT_2.2.2e.py (reference context only)

**Scope:** Phases A-C (Initialization, Adjudication Loop, Scenario Reconciliation)

**Output:**
- Adjudication decisions with dispositions
- Scenario reconciliation results
- T1 Handoff JSON (execution arguments for T2)
- Filename: {TICKER}_INT2.2.2eO_T1_{YYYYMMDD}.md

**Exclusion:** Do NOT execute Kernel. Kernel is provided for semantic alignment only.

**Turn 2: Kernel Execution**

**Trigger:** "Do Turn 2"

**Attachments Required:**
- This prompt (G3_INTEGRATION_2.2.2e.md)
- Turn 1 Output ({TICKER}_INT2.2.2eO_T1_{YYYYMMDD}.md)
- MRC State 3 artifacts (re-ingested fresh for clean context)
- CVR_KERNEL_INT_2.2.2e.py

**Scope:** Phases D-E (Recalculation Cascade, Distributional Re-Analysis)

**Output:**
- Finalized artifacts A.1-A.12 with all amendments applied
- state_4_active_inputs (pre-merged computational inputs)
- Filename: {TICKER}_INT2.2.2eO_T2_{YYYYMMDD}.md

**Turn 3: Narrative Synthesis**

**Trigger:** "Do Turn 3"

**Attachments Required:**
- This prompt (G3_INTEGRATION_2.2.2e.md)
- Turn 2 Output ({TICKER}_INT2.2.2eO_T2_{YYYYMMDD}.md)
- Upstream narrative sources:
  - {TICKER}_BASE2.2.1eO_T2_{YYYYMMDD}.md
  - {TICKER}_ENRICH2.2.1eO_T2_{YYYYMMDD}.md
  - {TICKER}_SCEN2.2.1eO_T2_{YYYYMMDD}.md
  - {TICKER}_SC2.2.1eO_{YYYYMMDD}_{LLM}.md (all SC outputs)

**Scope:** Phase F (Comprehensive Final Output)

**Execution Mode:** CONCATENATION-PRIMARY — Copy/paste from upstream sources. Minimize generation. See Section V.A.x.

**Output:**
- CVR State 4 Final Valuation (unified document)
- Contains narratives N1-N9 + embedded artifacts
- Filename: {TICKER}_INT2.2.2eO_T3_{YYYYMMDD}.md

**Data Flow:**

```
T1 Inputs                    T1 Output
─────────────────────────────────────────
MRC State 3 artifacts   ──►  Adjudication JSON
A.11 Audit Reports      ──►  (scenario decisions,
Kernel (context)             modifications, cascade scope)
                                    │
                                    ▼
T2 Inputs                    T2 Output
─────────────────────────────────────────
T1 JSON                 ──►  Finalized Artifacts A.1-A.12
State 3 (fresh)         ──►  state_4_active_inputs
Kernel (executable)     ──►  Recalculation results
                                    │
                                    ▼
T3 Inputs                    T3 Output
─────────────────────────────────────────
T2 Artifacts            ──►  CVR State 4 Final Valuation
Upstream Narratives     ──►  (N1-N9 + embedded artifacts)
```

**Rationale:**

The three-shot architecture provides:
- **T1 Reasoning Depth:** Full context for adjudication without computational overhead
- **T2 Clean Execution:** Fresh context for deterministic kernel execution
- **T3 Comprehensive Synthesis:** Produces unified final valuation document suitable for human review and IRR stage consumption

B. The CVR Kernel Mandate (Computational Integrity)

The CVR Kernel (G3_2.2.2e_INT) is the sole authorized execution engine for all
recalculation.

1\. Loading & Execution (Three-Shot File Delivery):

\* Turn 1: CVR_KERNEL_INT_2.2.2e.py is attached for contextual understanding only (DSL modes, function signatures, node naming conventions). DO NOT execute kernel code in T1.

\* Turn 2: Load CVR_KERNEL_INT_2.2.2e.py directly into the execution environment. The kernel file can be imported or executed as a standard Python module.

\* Turn 3: No kernel execution. T3 performs narrative synthesis only.

\* Action: In T2, load the kernel and call functions directly (e.g., `from CVR_KERNEL_INT_2_2_2e import execute_cvr_workflow, calculate_sse_jpd`).

2\. Kernel Capabilities Required:

\* execute_cvr_workflow: Base case recalculation (if GIM modifications
accepted)

\* execute_scenario_intervention: Scenario magnitude recalculation (if
interventions modified)

\* calculate_sse_jpd: SSE integration (if scenarios substituted or
probabilities revised)

\* execute_full_scenario_analysis: Convenience wrapper for complete
re-execution

3\. Prohibition: Implementing custom forecasting, APV valuation, or SSE
integration code outside the Kernel is strictly PROHIBITED.

C. Search Policy (Verification Search Protocol)

Search is AUTHORIZED under the Verification Search Protocol. This is a
constrained authorization for evidentiary verification, not open-ended
research.

Authorized Search Purposes:

1\. Confirming or refuting A.11 claims: When the audit cites external
facts (e.g., \"Competitor X announced price cuts,\" \"Industry base
rates have shifted\"), verify the claim\'s accuracy and materiality.

2\. Independently verifying material A.10 assumptions not addressed by
A.11: The audit is not exhaustive. If you identify high-sensitivity
assumptions in A.10 that warrant verification, you may search.

3\. Retrieving updated primary data where staleness is flagged: If the
audit identifies that source data has been superseded (e.g., new
guidance issued post-BASE), search for the current authoritative source.

4\. Defending State 3 against audit findings: You may search for
contradictory evidence that supports the original analysis when audit
critiques appear weakly substantiated.

Prohibited Search: Do not conduct open-ended research to discover new
scenarios, generate new investment theses, or expand the analytical
scope beyond adjudication.

D. The Efficiency Protocol (No Full Reconstruction)

Mandate: Do NOT re-execute the full pipeline from State 1. Trust the
audited State 3 as the computational baseline.

Action: Apply only incremental modifications where adjudication
requires. Extract baseline metrics directly from
A.7_LIGHTWEIGHT_VALUATION_SUMMARY and A.10_SCENARIO_MODEL_OUTPUT:

\* Base Case IVPS (State 2)

\* E\[IVPS\] (State 3)

\* DR_Static

\* Terminal_g, Terminal_ROIC

\* Scenario definitions (P, M, interventions)

\* SSE results (JPD, distribution statistics)

Rationale: The MRC paradigm guarantees deterministic reconstruction.
Full re-execution would consume substantial resources without analytical
benefit. Recalculate only when adjudication modifies inputs.

E. Scenario Capacity Constraint

The 4-Scenario Limit: The finalized State 4 CVR MUST contain a maximum
of 4 discrete scenarios (2⁴ = 16 states).

Implication: If adjudication accepts a new scenario proposed by A.11,
the Scenario Substitution Mandate (P2) governs which existing scenario
is displaced.

F. Emission Policy (CVR State 4 Bundle Mandate)

The output must be a \*\*CVR State 4 Bundle\*\*---a consolidated JSON
object representing the finalized Computational Valuation Record. This
bundle serves as the single authoritative input for the IRR stage and as
the complete audit trail for human analysts.

\*\*Mandatory Bundle Structure:\*\*

\`\`\`json

{

\"bundle_metadata\": {

\"schema_version\": \"G3_2.2.2eI_BUNDLE\",

\"bundle_type\": \"CVR_STATE_4_FINALIZED\",

\"company_name\": \"string\",

\"ticker\": \"string (EXCHANGE:SYMBOL)\",

\"valuation_date\": \"string (YYYY-MM-DD)\",

\"generation_timestamp\": \"string (ISO 8601)\",

\"cascade_executed\": \"string
(FULL\|PARTIAL_SCENARIO\|PARTIAL_SSE\|NONE)\",

\"version_control\": {

\"paradigm\": \"G3 Meta-Prompting Doctrine v2.4 (Three-Shot Guided Autonomy)\",

\"pipeline_stage\": \"INTEGRATION G3_2.2.2e\",

\"schema_version\": \"G3_2.2.2eI\",

\"execution_model\": \"Three-Shot (T1=Adjudication, T2=Execution, T3=Synthesis)\",

\"scenario_compatibility\": \"G3SCENARIO 2.2.1e\",

\"sc_compatibility\": \"G3SC 2.2.1e\",

\"enrich_compatibility\": \"G3ENRICH 2.2.1e\",

\"base_compatibility\": \"G3BASE 2.2.1e\"

}

},

\"artifacts\": {

\"A.1_EPISTEMIC_ANCHORS\": \"{\...full artifact, amended if adjudication
required\...}\",

\"A.2_ANALYTIC_KG\": \"{\...full artifact, amended if adjudication
required\...}\",

\"A.3_CAUSAL_DAG\": \"{\...full artifact, amended if adjudication
required\...}\",

\"A.5_GESTALT_IMPACT_MAP\": \"{\...full artifact, amended if
adjudication required\...}\",

\"A.6_DR_DERIVATION_TRACE\": \"{\...full artifact, amended if adjudication
required per P7\...}\",

\"A.7_LIGHTWEIGHT_VALUATION_SUMMARY\": \"{\...recalculated if cascade
triggered, includes Y0-Y3 checkpoints\...}\",

\"A.8_RESEARCH_STRATEGY_MAP\": \"{\...full artifact, immutable\...}\",

\"A.9_ENRICHMENT_TRACE\": \"{\...full artifact, immutable\...}\",

\"A.10_SCENARIO_MODEL_OUTPUT\": \"{\...full artifact, amended if
scenarios modified\...}\",

\"A.12_INTEGRATION_TRACE\": \"{\...the adjudication record, per Appendix
A schema\...}\"

},

\"amendment_manifest\": {

\"artifacts_amended\": \[\"string (list of artifact IDs modified, e.g.,
\'A.5\', \'A.10\')\"\],

\"amendments_applied\": \[

{

\"artifact\": \"string (artifact ID)\",

\"element\": \"string (specific field modified)\",

\"from_value\": \"string\|number (pre-adjudication value)\",

\"to_value\": \"string\|number (post-adjudication value)\",

\"finding_id\": \"string (F1, F2, \... reference to adjudication_log)\"

}

\],

\"cascade_scope\": \"string
(FULL\|PARTIAL_SCENARIO\|PARTIAL_SSE\|NONE)\"

},

\"state_4_active_inputs\": {

\"description\": \"Pre-merged computational inputs for IRR stage.
Contains finalized values with all amendments applied.\",

\"fundamentals_trajectory\": {

\"Y0\": {\"Revenue\": \"float\", \"EBITDA\": \"float\",
\"EBITDA_Margin\": \"float\", \"NOPAT\": \"float\", \"FCF_Unlevered\":
\"float\", \"Invested_Capital\": \"float\", \"ROIC\": \"float\"},

\"Y1\": \"{\...same structure\...}\",

\"Y2\": \"{\...same structure\...}\",

\"Y3\": \"{\...same structure\...}\"

},

\"scenarios_finalized\": \[

{

\"scenario_id\": \"string\",

\"scenario_name\": \"string\",

\"p_posterior\": \"float (post-adjudication probability)\",

\"ivps_impact\": \"float (post-adjudication magnitude)\",

\"status\": \"string (RETAINED\|MODIFIED\|ADDED\|DISPLACED)\",

\"fundamentals_y1_intervened\": {

\"revenue\": \"float (\$M) - Scenario-specific Y1 revenue\",

\"ebitda\": \"float (\$M) - Scenario-specific Y1 EBITDA\",

\"ebit\": \"float (\$M) - Scenario-specific Y1 EBIT\",

\"ebit_margin\": \"float (0-1) - Scenario-specific Y1 EBIT margin\",

\"nopat\": \"float (\$M) - Scenario-specific Y1 NOPAT\",

\"fcf_unlevered\": \"float (\$M) - Scenario-specific Y1 unlevered FCF\"

}

}

\],

\"valuation_anchor\": {

\"base_case_ivps_state2\": \"float\",

\"e_ivps_state4\": \"float\",

\"dr_static\": \"float\",

\"terminal_g\": \"float\",

\"terminal_roic\": \"float\"

},

\"market_data_snapshot\": {

\"current_price\": \"float\",

\"shares_outstanding_fdso\": \"float\",

\"net_debt_y0\": \"float\",

\"market_cap\": \"float\"

},

\"constraints\": {

\"mutual_exclusivity_groups\": \[\"array of scenario ID pairs\"\],

\"economic_incompatibilities\": \[\"array of scenario ID pairs\"\]

},

\"pipeline_fit_grade\": \"string (A\|B\|C\|D\|F)\"

},

\"final_thesis_synthesis\": {

\"original_thesis_anchor\": \"string (1-2 sentence summary of original
BASE investment thesis)\",

\"adjudication_impact\": \"string (how audit findings modified or
validated the original view)\",

\"state_4_thesis\": \"string (synthesized investment thesis reflecting
post-adjudication perspective)\",

\"confidence_characterization\": \"string (overall confidence in State 4
reliability, incorporating Pipeline Fit and adjudication outcomes)\"

}

}

\`\`\`

\*\*Bundle Construction Protocol:\*\*

1\. Begin with State 3 artifacts (A.1--A.10) as the baseline.

2\. Apply all accepted amendments from adjudication, modifying artifacts
in place.

3\. If recalculation cascade was triggered, embed the recalculated A.7
with updated trajectory checkpoints.

4\. Populate \`amendment_manifest\` with a summary of all changes for
quick reference.

5\. Extract \`state_4_active_inputs\` from finalized artifacts---this
provides IRR with pre-merged computational inputs.

6\. Synthesize \`final_thesis_synthesis\` to reconcile original thesis
with adjudication outcomes.

7\. Embed A.12_INTEGRATION_TRACE as the detailed audit log.

\*\*Prohibition:\*\* Reprinting instructions, normative definitions, or
the CVR Kernel code within the bundle is strictly forbidden. The bundle
contains artifacts and metadata only.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

III\. CORE ANALYTICAL DIRECTIVES

P1. The Verification Discovery Protocol (Epistemic Hierarchy)

When adjudicating disputed claims, apply the following evidentiary
hierarchy:

1\. Primary Documents (Highest Authority): 10-K, 10-Q, audited
financials, official company filings. These are the ground truth for
factual claims about the company.

2\. Verified External Sources: Claims verified through Verification
Search (e.g., confirmed competitor actions, validated industry data).
Must be from authoritative sources (regulatory filings, major financial
news, academic studies).

3\. CVR Analysis (State 3): The analytical judgments embedded in
A.1--A.10. These represent rigorous upstream synthesis but are subject to
revision if contradicted by higher-authority evidence.

4\. Audit Rhetoric (Lowest Authority): Unsubstantiated assertions in
A.11. The audit may identify valid concerns, but assertions without
evidentiary grounding do not override upstream analysis.

The Verification Imperative: When A.11 cites new external facts not
present in the Discovery Record, you MUST use Verification Search to
confirm the claim before accepting the critique. Unverified audit claims
are logged but not actioned.

P2. The Scenario Substitution Mandate (Mathematical Integrity)

If adjudication validates a new scenario proposed by A.11 (or
invalidates an existing scenario), the scenario set must be reconciled
to maintain the 4-scenario constraint.

The Substitution Procedure:

1\. Rank All Candidates: Compute expected materiality \|P × M\| for:

\* All State 3 scenarios (from A.10)

\* All validated new scenarios (from A.11, post-adjudication)

2\. Select Top 4: The four scenarios with highest \|P × M\| constitute
the finalized set.

3\. Log Substitutions: Any scenario displaced from State 3 must be
documented in A.11 with:

\* Scenario ID and description

\* Original \|P × M\| ranking

\* Rationale for displacement (higher-impact replacement identified)

4\. Distributional Completeness Check: After substitution, verify the
final set includes at least one material UPSIDE and one material
DOWNSIDE scenario. If the top 4 by \|P × M\| are directionally skewed,
note this in the trace with explicit justification.

Prohibition: Do not simply add scenarios beyond the 4-scenario limit.
The SSE framework requires explicit enumeration of 2\^N states;
exceeding 16 states degrades analytical tractability.

P3. The Recalculation Cascade (Computational Integrity)

Any accepted adjudication that modifies State 3 inputs triggers a
recalculation cascade. The cascade scope depends on what was modified:

Modification Type

Cascade Scope

GIM assumption (base case driver)

Full cascade: SCM → APV → Scenario magnitudes → SSE

DR revision (per P7)

Full cascade: SCM → APV → All scenario magnitudes → SSE

Scenario intervention definition

Partial cascade: Affected scenario magnitude → SSE

Scenario probability estimate

Minimal cascade: SSE only

Scenario substitution (add/remove)

Partial cascade: New scenario magnitude (if added) → SSE

No modifications accepted

No cascade; State 4 = State 3 locked

Execution Protocol (T2 Only):

1\. Load Kernel (File Import in T2)

2\. If base case modified: execute_cvr_workflow with updated GIM

3\. If scenarios modified: execute_scenario_intervention for affected
scenarios

4\. If any scenario/probability change: calculate_sse_jpd with finalized
scenario set

5\. Regenerate distribution statistics (E\[IVPS\], percentiles, shape
metrics)

P4. Priority-Based Adjudication Protocol

Silicon Council findings are classified by priority. Handle each class
as follows:

CRITICAL Findings:

\* Definition: \"Materially undermines confidence in E\[IVPS\]; should
block finalization without resolution.\"

\* Mandate: CRITICAL findings trigger mandatory adjudication. State 4
CANNOT be emitted until every CRITICAL finding is explicitly resolved
(ACCEPT, REJECT, or MODIFY).

\* If a CRITICAL finding cannot be resolved due to evidentiary
limitations, escalate in A.11 with explicit notation that finalization
proceeded under acknowledged uncertainty.

HIGH Findings:

\* Definition: \"Significant concern requiring explicit address in
INTEGRATION.\"

\* Mandate: Every HIGH finding must be logged in A.11 with explicit
disposition (ACCEPT/REJECT/MODIFY) and supporting rationale.

\* HIGH findings that are rejected require substantive justification
referencing the evidentiary hierarchy (P1).

MEDIUM Findings:

\* Definition: \"Notable issue providing useful context.\"

\* Mandate: MEDIUM findings should be reviewed and logged. Formal
adjudication is discretionary based on materiality assessment.

\* May be batched in A.11 under \"Reviewed, No Action Required\" with
brief rationale.

P5. Pipeline Fit Handling Protocol

Silicon Council assigns an overall Pipeline Fit Grade (A--F) assessing
whether the security is well-suited to the CAPY methodology.

Grade-Based Protocol:

Grade

Interpretation

Required Action

A

Well-suited; minimal unmodeled factors

Proceed to finalization

B

Some blind spots; manageable with caveats

Proceed; note caveats in A.11

C

Material blind spots; interpret with caution

Proceed with explicit confidence discount narrative in A.11

D

Multiple severe blind spots

Emit WARNING in A.11. State that methodology limitations may materially
affect reliability. Recommend human orchestrator review before
investment action.

F

Fundamental mismatch

Emit BLOCK RECOMMENDATION in A.11. State that DCF+SSE methodology is
inappropriate. Recommend alternative analytical approach. Finalization
proceeds only with explicit orchestrator override notation.

The Confidence Discount Narrative (Grades C--F): When Pipeline Fit is C
or below, A.11 must include a dedicated section explaining:

\* Which blind spots are most material

\* Directional bias they may introduce (overstates/understates value?)

\* Suggested interpretation adjustments for the human reader

P6. The Symmetric Burden Principle

Adjudication must not exhibit status quo bias. Apply symmetric
evidentiary standards:

When evaluating an A.11 critique:

\* Ask: \"What evidence substantiates this critique? Does it meet the
threshold for overriding upstream analysis?\"

When the critique challenges a State 3 assumption:

\* Ask: \"What evidence substantiated the original assumption? Does it
withstand the critique?\"

Resolution Framework:

\* If A.11 provides superior evidence → ACCEPT the critique

\* If State 3 evidence remains stronger → REJECT the critique with
documented rationale

\* If evidence is balanced or ambiguous → MODIFY toward the more
conservative position (epistemic humility)

Do not default to preserving State 3 simply because it represents prior
analytical effort. Do not default to accepting A.11 simply because it
represents adversarial scrutiny. Adjudicate on evidentiary merit.

P7. DR Revision Protocol (Integration Authority)

Default: DR is presumptively stable. The State 3 risk assessment is inherited unless A.11 findings reveal material risk factors not assessable from prior stage evidence.

Revision Authority: DR modification in INTEGRATION is authorized if and only if:
- A.11 identifies material risk factors with CRITICAL or HIGH priority
- The risk factor was not assessable from BASE/ENRICH source documents
- Verification Search confirms the risk factor's validity (if externally sourced)

Burden of Proof: DR revision requires:
(a) Specific A.11 finding citation
(b) Explicit mapping to X multiplier component (e.g., "governance risk adjustment +0.15 due to [SC finding F3]")
(c) Quantified DR delta with directional justification

Trace Requirement: Any DR modification MUST be documented in A.12 via `dr_revision` field with:
- prior_dr, posterior_dr
- finding_id triggering revision
- X component affected
- Evidence justification

Cascade Implication: DR revision triggers FULL cascade (all scenario magnitudes recalculated with new DR).

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

IV\. EXECUTION PROTOCOL (The Workflow)

Execute the workflow in phases, integrating the Core Analytical
Directives throughout.

Phase A: Initialization and Triage

1\. Ingestion: Parse all mandatory inputs:

\* MRC State 3 artifacts (A.1--A.10)

\* A.11_AUDIT_REPORT_SET (all SC outputs from parallel execution)

\* Discovery Record inventory

2\. Baseline Extraction: From A.7 and A.10, extract:

\* Base Case IVPS, DR, Terminal_g, Terminal_ROIC

\* State 3 E\[IVPS\] and distribution statistics

\* Scenario definitions (IDs, P, M, intervention types)

3\. Audit Docketing: Create an internal register of all A.11 findings:

\* Assign unique Finding IDs (F1, F2, \...)

\* Record priority classification (CRITICAL/HIGH/MEDIUM)

\* Record finding category (Source Integrity, Pipeline Fit, Scenario
Critique, etc.)

4\. Audit Synthesis (Multi-SC Handling):

When multiple A.11 reports are provided:

a. **Concordance Analysis:**
   - Identify findings flagged by multiple SC instances (concordant)
   - Identify findings flagged by single SC instance (discordant)
   - Weight concordant findings higher in triage priority

b. **Conflict Resolution:**
   - If SCs disagree on priority classification: use highest priority
   - If SCs disagree on finding substance: note both perspectives in A.12
   - If Pipeline Fit grades diverge: use modal grade; note range in A.12

c. **Synthesis Documentation:**
   - Log synthesis decisions in A.12.audit_synthesis section
   - Attribute findings to source SC instances
   - Note concordance/discordance for each finding

d. **Docketing:**
   - Merge findings into unified register with Finding IDs (F1, F2, ...)
   - Preserve source attribution (e.g., "F3 [G3PTR, C45ET]" for concordant)

5\. Pipeline Fit Assessment: Extract the overall grade. If D or F, flag
for Protocol P5 handling.

6\. Triage Sequencing: Order findings for adjudication:

\* CRITICAL findings first (mandatory resolution)

\* HIGH findings second (mandatory disposition)

\* MEDIUM findings last (discretionary review)

\* Within each priority: Source Integrity findings before analytical
findings (data errors propagate)

\* Concordant findings before discordant findings (higher confidence)

Phase B: Adjudication Loop

For each finding in triage sequence:

1\. Claim Extraction: Identify the specific factual or analytical claim
being challenged.

2\. Evidence Retrieval:

\* Locate relevant primary documents in Discovery Record

\* If A.11 cites external facts not in Discovery Record → Verification
Search

\* Locate the original State 3 evidence supporting the challenged
assumption

3\. Evidentiary Comparison: Apply the P1 hierarchy. Determine which
evidence is authoritative.

4\. Disposition Determination:

\* ACCEPT: A.11 critique is substantiated; State 3 requires modification

\* REJECT: A.11 critique is not substantiated; State 3 stands

\* MODIFY: Partial validity; State 3 requires adjustment but not full
adoption of critique

5\. Modification Specification (if ACCEPT or MODIFY):

\* Specify exact artifact(s) affected (GIM driver, scenario probability,
intervention definition, etc.)

\* Specify the pre-adjudication value and post-adjudication value

\* Flag for Recalculation Cascade

6\. Trace Logging: Record in A.11:

\* Finding ID and summary

\* Evidence consulted (document references, search results if
applicable)

\* Disposition with rationale

\* Modification specification (if applicable)

7\. Iterate: Proceed to next finding until all CRITICAL and HIGH
findings are processed. Review MEDIUM findings and log dispositions.

Phase C: Scenario Reconciliation

After all adjudications are complete:

1\. Scenario Inventory: List all scenarios:

\* State 3 scenarios (from A.10) --- note any with modified P or M from
Phase B

\* New scenarios validated from A.11 (if any)

\* Scenarios invalidated/removed (if any)

2\. Compute \|P × M\| Rankings: Using post-adjudication values for all
scenarios.

3\. Execute Substitution Mandate (P2): If the scenario count exceeds 4
or if a new high-impact scenario displaces a lower-impact one:

\* Select top 4 by \|P × M\|

\* Log substitutions in A.11

4\. Distributional Completeness Check: Verify upside/downside balance.
Document in trace.

5\. Finalize Scenario Set: Lock the 4 (or fewer) scenarios for State 4.

Phase D: Recalculation Cascade

If any modifications were accepted in Phase B or substitutions occurred
in Phase C:

1\. Load Kernel: Import CVR_KERNEL_INT_2.2.2e.py in T2 execution environment
(Appendix C).

2\. Determine Cascade Scope: Per P3, identify which calculations require
re-execution.

3\. Execute Recalculations:

\* Base case (if GIM modified): execute_cvr_workflow

\* Scenario magnitudes (if interventions modified or new scenarios
added): execute_scenario_intervention

\* SSE integration (if any scenario/probability changes):
calculate_sse_jpd

4\. Validate Outputs:

\* Economic Governor check: Verify Terminal_g and Terminal_ROIC satisfy
constraints

\* Probability sum validation: Confirm JPD sums to 1.0

\* Limited liability check: No negative IVPS states

5\. Extract Finalized Metrics:

\* E\[IVPS\] (State 4)

\* Distribution statistics (P10, P50, P90, σ, skewness)

\* State-by-state enumeration

Phase E: Distributional Re-Analysis

1\. State Comparison: Document the State 3 → State 4 bridge:

\* E\[IVPS\] change (\$ and %)

\* Distribution shape change (if any)

\* Key driver(s) of change

2\. Risk Assessment Update: Based on finalized distribution:

\* P10 downside characterization

\* P90 upside characterization

\* Skewness interpretation

3\. Investment Implications Update: If the adjudication materially
altered the risk/reward profile, note implications for:

\* Position sizing

\* Entry timing

\* Risk management

Phase F: Emission (T2 and T3)

**Phase F.1: Artifact Emission (T2)**

1\. Construct A.12_INTEGRATION_TRACE: Per schema (Appendix A),
including:

\* Executive summary of adjudication outcomes

\* Full adjudication log (all findings with dispositions)

\* Verification evidence log (all searches performed)

\* Scenario substitution log (if applicable)

\* Recalculation cascade log

\* Pipeline Fit handling (confidence discount narrative if applicable)

\* State 3 → State 4 bridge

\* Audit synthesis log (multi-SC concordance analysis)

2\. Finalize State 4:

\* State 4 = State 3 artifacts (A.1--A.10), with any amendments noted in
A.12

\* If A.10 scenarios were modified, the amended A.10 is the
authoritative version (original values preserved in A.12 trace)

\* A.12 is appended as the Integration record

3\. Emit T2 Output: Output the CVR State 4 Bundle per Section II.F, containing all
finalized artifacts and the A.12_INTEGRATION_TRACE.

4\. Emit state_4_active_inputs: Pre-merged computational inputs for IRR stage.

**T2 Output Filename:** {TICKER}_INT2.2.2eO_T2_{YYYYMMDD}.md

**Phase F.2: Narrative Synthesis (T3)**

T3 produces the comprehensive CVR State 4 Final Valuation document. See Section V for complete specification.

**T3 Output Filename:** {TICKER}_INT2.2.2eO_T3_{YYYYMMDD}.md

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

V. OUTPUT MANDATE: CVR State 4 Final Valuation (T3)

T3 produces a comprehensive unified document containing the complete analytical journey and finalized valuation. This document serves as the authoritative final output for human analyst review, IRR stage consumption, and audit trail purposes.

\### V.A T3 Narrative Inventory

T3 synthesizes narratives from all pipeline stages into a coherent final document.

\| ID \| Name \| Source \| T3 Treatment \|
\|\-\-\-\-\|\-\-\-\-\-\-\|\-\-\-\-\-\-\-\-\|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\|
\| N1 \| Investment Thesis \| BASE→ENRICH \| Revise to reflect post-adjudication view. If SC critiques or adjudication materially changed thesis, rewrite affected sections. \|
\| N2 \| Invested Capital Modeling \| BASE→ENRICH \| Passthrough unless adjudication touched IC structure (rare). \|
\| N3 \| Economic Governor & Constraints \| BASE→ENRICH \| Revise if terminal assumptions changed via adjudication. \|
\| N4 \| Risk Assessment & DR Derivation \| BASE→ENRICH \| Revise if DR modified or risk view shifted. \|
\| N5 \| Enrichment Synthesis \| ENRICH \| Revise if GIM refinements were overturned/modified by adjudication. \|
\| N6 \| Scenario Model Synthesis \| SCENARIO (elevated) \| Extract from A.10 and SCEN narratives. Describes scenario identification, intervention design, probability estimation, SSE results. \|
\| N7 \| Adjudication Synthesis \| INT T1/T2 (new) \| Narrative rendering of A.12. SC findings summary, disposition rationale, material changes, Pipeline Fit handling. \|
\| N8 \| Final Investment Thesis \| INT T3 (new) \| Synthesized thesis reflecting complete post-adjudication view. Distinct from N1 — states final position cleanly. \|
\| N9 \| CVR Evolution Summary \| INT T3 (new) \| Structured walkthrough: State 1→2→3→4. Key deltas at each transition, primary IVPS drivers, confidence at each state. \|

\### V.A.x T3 Execution Mode: CONCATENATION-PRIMARY

**Critical Instruction:** T3 is a SYNTHESIS turn, not a GENERATION turn. Minimize original text generation. Maximize copy/paste from upstream sources.

**For Narratives N1-N6 (Inherited):**
1. LOCATE the narrative section in the upstream T2 output (ENRICH, SCEN)
2. COPY the narrative text verbatim — do not paraphrase or summarize
3. ADD "[State 4: Confirmed]" annotation if A.12 shows no amendments to referenced artifacts
4. ADD "[State 4: Revised]" annotation and EDIT ONLY the specific sentences affected if A.12 shows amendments
5. If cascade_executed = NONE, all inherited narratives should be near-verbatim passthrough

**For Narratives N7-N9 (New):**
- N7 (Adjudication Synthesis): Extract from A.12 and INT T1 reasoning. Light generation authorized.
- N8 (Final Investment Thesis): Synthesize from N1 + adjudication outcomes. Moderate generation authorized.
- N9 (CVR Evolution Summary): Structure from state bridge data. Light generation authorized.

**For Artifacts (A.1-A.12):**
1. COPY the complete JSON block from T2 output
2. Do NOT regenerate, summarize, or restructure
3. Do NOT omit fields or truncate arrays
4. Embed the full artifact — IRR stage requires complete data

**For state_4_active_inputs:**
1. COPY verbatim from T2 output
2. This is computational input for downstream stages — must be exact

**Rationale:** T3's value is ASSEMBLY and COHERENCE, not original analysis. The analytical work is complete. Regenerating content risks drift from validated artifacts. Copy/paste preserves fidelity.

\### V.B Revision Authority

**Level:** Moderate-High

**T3 CAN:**
- Rewrite narrative sections to integrate adjudication outcomes
- Synthesize new narratives (N6-N9) from available materials
- Update language for coherence and flow
- Ensure artifact-narrative consistency

**T3 CANNOT:**
- Re-litigate adjudication decisions made in T1
- Modify artifact values
- Change computational results from T2

\### V.C Revision Checklist

Before passthrough of any narrative (N1-N5), T3 must verify against A.12:

```
For each inherited narrative:
[ ] Check A.12.amendments_applied for modifications to referenced artifacts
[ ] If modifications exist: revise narrative to reflect changes
[ ] If no modifications: passthrough with "[State 4: Confirmed]" annotation
[ ] Verify no stale assumptions remain in narrative text
```

\### V.D T3 Output Structure

Emit a comprehensive unified document with the following structure:

```markdown
# CVR State 4 Final Valuation: {Company Name} ({TICKER})
## Valuation Date: {YYYY-MM-DD} | Generated: {ISO 8601 timestamp}

---

## EXECUTIVE SUMMARY (N8: Final Investment Thesis)
[2-3 paragraphs: synthesized post-adjudication thesis, E[IVPS], key metrics, confidence]

---

## I. CVR EVOLUTION SUMMARY (N9)
### State 1 → State 2 (BASE → ENRICHMENT)
[Key refinements, IVPS delta, primary drivers]

### State 2 → State 3 (ENRICHMENT → SCENARIO)
[Scenario integration impact, E[IVPS] derivation, distribution shape]

### State 3 → State 4 (SCENARIO → INTEGRATION)
[Adjudication outcomes, material changes, final confidence]

---

## II. INVESTMENT THESIS DEVELOPMENT (N1, revised)
[Full thesis narrative reflecting adjudication]

---

## III. INVESTED CAPITAL MODELING (N2)
[IC structure narrative]

---

## IV. ECONOMIC GOVERNOR & CONSTRAINTS (N3)
[Terminal assumptions, constraint satisfaction]

---

## V. RISK ASSESSMENT & DR DERIVATION (N4)
[Risk framework, DR derivation]

---

## VI. ENRICHMENT SYNTHESIS (N5)
[Key refinements from research integration]

---

## VII. SCENARIO MODEL SYNTHESIS (N6)
### Scenario Identification
[Selection rationale, |P×M| ranking]

### Intervention Design
[Per-scenario intervention logic]

### Probability Estimation
[HAD citations, Bayesian updating]

### SSE Integration Results
[Distribution statistics, state enumeration]

---

## VIII. ADJUDICATION SYNTHESIS (N7)
### Silicon Council Findings Summary
[Key findings by priority, concordance notes]

### Disposition Log
[ACCEPT/REJECT/MODIFY decisions with rationale]

### Material Changes Applied
[Specific modifications to State 3]

### Pipeline Fit Assessment
[Grade(s), confidence discount if applicable]

---

## IX. FINAL VALUATION METRICS

| Metric | Value |
|--------|-------|
| E[IVPS] (State 4) | ${X.XX} |
| Base Case IVPS | ${X.XX} |
| P10 | ${X.XX} |
| P50 (Median) | ${X.XX} |
| P90 | ${X.XX} |
| DR | X.X% |
| Terminal g | X.X% |
| Terminal ROIC | X.X% |
| Current Price | ${X.XX} |
| Implied Upside | X.X% |

---

## X. MRC STATE 4 ARTIFACTS

{
  "bundle_metadata": {...},
  "A.1_EPISTEMIC_ANCHORS": {...},
  "A.2_ANALYTIC_KG": {...},
  "A.3_CAUSAL_DAG": {...},
  "A.5_GESTALT_IMPACT_MAP": {...},
  "A.6_DR_DERIVATION_TRACE": {...},
  "A.7_LIGHTWEIGHT_VALUATION_SUMMARY": {...},
  "A.8_RESEARCH_STRATEGY_MAP": {...},
  "A.9_ENRICHMENT_TRACE": {...},
  "A.10_SCENARIO_MODEL_OUTPUT": {...},
  "A.11_AUDIT_REPORT": {...},
  "A.12_INTEGRATION_TRACE": {...},
  "state_4_active_inputs": {...},
  "amendment_manifest": {...}
}

[END OF CVR STATE 4 FINAL VALUATION]
```

\### V.E File Naming

**T3 Output:** {TICKER}_INT2.2.2eO_T3_{YYYYMMDD}.md

This is the authoritative final valuation document for:
- Human analyst review
- IRR stage consumption
- Audit trail purposes

\### V.F T2 Bundle Reference

T2 produces the CVR State 4 Bundle (JSON) per Section II.F schema. The T2 bundle contains:

\| Component \| Source \| Amendment Status \| Description \|
\|\-\-\-\-\-\-\-\-\-\--\|\-\-\-\-\-\-\--\|\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--\|\-\-\-\-\-\-\-\-\-\-\-\--\|
\| \`bundle_metadata\` \| Generated \| N/A \| Version, timestamps, cascade scope \|
\| \`A.1_EPISTEMIC_ANCHORS\` \| State 3 \| If adjudication required \| Core analytical constraints \|
\| \`A.2_ANALYTIC_KG\` \| State 3 \| If adjudication required \| Knowledge graph with Y0 data \|
\| \`A.3_CAUSAL_DAG\` \| State 3 \| If adjudication required \| Structural causal model \|
\| \`A.5_GESTALT_IMPACT_MAP\` \| State 3 \| If adjudication required \| GIM driver specifications \|
\| \`A.6_DR_DERIVATION_TRACE\` \| State 3 \| If adjudication required (P7) \| Discount rate derivation \|
\| \`A.7_LIGHTWEIGHT_VALUATION_SUMMARY\` \| Recalculated \| If cascade triggered \| Valuation summary with Y0-Y3 checkpoints \|
\| \`A.8_RESEARCH_STRATEGY_MAP\` \| State 3 \| Immutable \| Research methodology record \|
\| \`A.9_ENRICHMENT_TRACE\` \| State 3 \| Immutable \| Research synthesis \|
\| \`A.10_SCENARIO_MODEL_OUTPUT\` \| State 3 \| If scenarios modified \| Probabilistic scenario definitions \|
\| \`A.12_INTEGRATION_TRACE\` \| Generated \| N/A (New) \| Adjudication record per Appendix A \|
\| \`amendment_manifest\` \| Generated \| N/A \| Summary of all changes applied \|
\| \`state_4_active_inputs\` \| Extracted \| N/A \| Pre-merged computational inputs for IRR \|

\### V.G Emission Validation Checklist (T2)

Before emitting the T2 bundle, verify:

1\. \*\*Bundle Metadata\*\*
\- \[ \] \`schema_version\` is \"G3_2.2.2eI_BUNDLE\"
\- \[ \] \`generation_timestamp\` is current ISO 8601
\- \[ \] \`cascade_executed\` reflects actual recalculation scope

2\. \*\*Artifact Completeness\*\*
\- \[ \] All artifacts (A.1--A.10, A.12) are present
\- \[ \] Amended artifacts have schema_version suffix \"-A\"
\- \[ \] A.7 contains Y0, Y1, Y2, Y3, Y5, Y10, Y20 trajectory checkpoints

3\. \*\*Amendment Manifest\*\*
\- \[ \] \`artifacts_amended\` lists all modified artifact IDs
\- \[ \] \`amendments_applied\` includes all accepted finding modifications
\- \[ \] Each amendment references its \`finding_id\` from adjudication_log

4\. \*\*State 4 Active Inputs\*\*
\- \[ \] \`fundamentals_trajectory\` contains Y0-Y3 data
\- \[ \] \`scenarios_finalized\` reflects post-adjudication probabilities and magnitudes
\- \[ \] \`valuation_anchor\` contains finalized E\[IVPS\], DR, terminal values
\- \[ \] \`market_data_snapshot\` contains current price, shares, net debt

5\. \*\*A.12_INTEGRATION_TRACE\*\*
\- \[ \] All findings have dispositions (ACCEPT/REJECT/MODIFY)
\- \[ \] Verification searches are logged
\- \[ \] State bridge shows State 3 → State 4 delta
\- \[ \] Pipeline Fit handling is documented
\- \[ \] Audit synthesis (multi-SC) is documented

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

