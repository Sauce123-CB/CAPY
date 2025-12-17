G3 SCENARIO 2.2.1e: Probabilistic Causal Valuation

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

I. MISSION AND OBJECTIVES

\* Mission: Execute the SCENARIO stage (G3_2.2.1eS) of the CAPY Pipeline
for {Company Name} ({EXCHANGE:TICKER}) as of {DATE}.

\* Primary Objective: To transition the Computational Valuation Record
(CVR) from a deterministic Base Case (MRC State 2) to a probabilistic
valuation (MRC State 3). This involves modeling discrete, high-impact
scenarios as causal interventions on the Base Case SCM, estimating their
probabilities (P) and magnitudes (M) using rigorous Bayesian
methodology, and integrating them via Structured State Enumeration (SSE)
to determine the Expected Intrinsic Value Per Share (E\[IVPS\]) and the
full valuation distribution.

\* Execution Paradigm: Guided Autonomy, Causal Intervention, and
Structured State Enumeration (SSE). This stage requires high-level
analytical judgment to synthesize scenario research, design economically
coherent interventions, estimate probabilities with epistemic rigor, and
interpret the resulting distribution to inform investment
decision-making.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

II\. EXECUTION ENVIRONMENT AND CONSTRAINTS

A. Environmental Awareness and Tools

\* Mandatory Inputs:

1\. MRC State 2 (ENRICHMENT Output): The 8 artifacts produced by G3
ENRICHMENT 2.2.1e:

\* A.1_EPISTEMIC_ANCHORS

\* A.2_ANALYTIC_KG

\* A.3_CAUSAL_DAG

\* A.5_GESTALT_IMPACT_MAP

\* A.6_DR_DERIVATION_TRACE

\* A.7_LIGHTWEIGHT_VALUATION_SUMMARY

\* A.9_ENRICHMENT_TRACE

\* A.8_RESEARCH_STRATEGY_MAP

2\. Scenario Research: Research outputs providing Historical Analogue
Data (H.A.D.) for discrete scenarios. This typically includes outputs
addressing Mainline Catalysts (RQ Coverage Objective C) and Tail Risk
Parameterization (RQ Coverage Objective D), though the specific RQ
structure may vary.

\* The Verification Doctrine (Externalized Schemas): The required output
schema (A.10_SCENARIO_MODEL_OUTPUT) is provided in Appendix A. Normative
definitions are provided in Appendix B. The output will be validated
against these external references.

\* The CVR Kernel Mandate (Computational Integrity P7): The CVR Kernel
(Appendix C) is the sole authorized execution engine for all
forecasting, valuation, and integration calculations.

1\. Loading & Execution (Two-Shot File Delivery):

\* Turn 1: CVR_KERNEL_SCEN_2.2.1e.py is attached for contextual understanding only (DSL modes, function signatures, node naming conventions). DO NOT execute kernel code in T1.

\* Turn 2: Load CVR_KERNEL_SCEN_2.2.1e.py directly into the execution environment. The kernel file can be imported or executed as a standard Python module.

\* Action: In T2, load the kernel and call functions directly (e.g., `from CVR_KERNEL_SCEN_2_2_1e import execute_scenario_intervention, calculate_sse_jpd`).

2\. Scenario Execution: Utilize execute_scenario_intervention() for
magnitude estimation.

3\. SSE Integration: Utilize calculate_sse_jpd() for the
Initialize-Filter-Renormalize procedure. This Kernelized SSE guarantees
mathematical accuracy for Joint Probability Distribution calculation.

4\. Prohibition: Implementing custom forecasting, APV valuation, or SSE
integration code outside the Kernel is strictly PROHIBITED.

\* Search Policy: Minimize search. The SCENARIO stage focuses on
synthesizing provided research inputs. Ad-hoc search is permitted ONLY
for clarifying specific data points explicitly referenced within the
scenario research or for validating critical factual claims where
ambiguity remains high after synthesis.

\* Emission Policy: The output must ONLY contain analytical narratives
and artifacts. Reprinting instructions, schemas, or the CVR Kernel code
is strictly forbidden.

A.3. Two-Shot Execution Paradigm

The SCENARIO stage executes across two turns to optimize context
utilization:

**Turn 1 (Analytical Synthesis):**

\* Scope: Phases A through D.2 (Initialization, Scenario Identification,
Probability Estimation, Intervention Design)

\* Inputs: MRC State 2 artifacts, Scenario Research, Full Kernel
(contextual understanding only)

\* Output: Scenario Execution Arguments (structured JSON embedded in T1
markdown)

\* Prohibition: No kernel execution in Turn 1

**Turn 2 (Kernel Execution):**

\* Scope: Phases D.3 through F (Kernel Execution, SSE Integration,
Synthesis, Emission)

\* Inputs: Turn 1 JSON output, MRC State 2 artifacts (re-ingested
fresh), Full Kernel (.py file)

\* Output: A.10_SCENARIO_MODEL_OUTPUT

\* Execution: Deterministic --- T1 JSON provides all analytical inputs;
T2 executes and emits

**File Naming Convention:**

\* Turn 1: {TICKER}\_SCEN2.2.1eO_T1\_{YYYYMMDD}.md

\* Turn 2: {TICKER}\_SCEN2.2.1eO_T2\_{YYYYMMDD}.md

\* Kernel: CVR_KERNEL_SCEN_2.2.1e.py

**Data Flow:**

\* T1 JSON contains analytical outputs only (scenario definitions,
probabilities, intervention specs, constraints)

\* T2 re-ingests ENRICHMENT artifacts (KG, DAG, GIM, DR_TRACE) fresh
from source

\* Kernel delivered to both turns: contextual in T1, executable in T2

B. The Efficiency Protocol (No State Reconstruction)

\* Mandate: Do NOT execute the Kernel to reconstruct State 2. Trust the
input artifacts from ENRICHMENT.

\* Action: Extract the State 2 baseline directly from the input
A.7_LIGHTWEIGHT_VALUATION_SUMMARY:

\* IVPS (State 2 --- the deterministic base case)

\* DR (Static Discount Rate)

\* Terminal g (Base Case terminal growth)

\* Terminal ROIC (Base Case terminal return)

\* Key Forecast Checkpoints (Y5, Y10, Y20)

\* Rationale: The MRC paradigm guarantees deterministic reconstruction.
Re-execution would consume substantial resources without analytical
benefit.

C. Scenario Capacity Constraint

\* The 4-Scenario Limit: Execution MUST be limited to a maximum of 4
discrete scenarios, prioritized strictly by expected materiality (\|P ×
M\|).

\* Rationale: With 4 scenarios, SSE enumerates 2\^4 = 16 possible
states. This represents the practical limit for explicit enumeration
while maintaining analytical tractability. Scenarios beyond the top 4 by
expected impact should be noted but not modeled.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

III\. CORE ANALYTICAL DIRECTIVES

P1. Analytical Autonomy and Intervention Design

The SCENARIO stage requires substantial analytical judgment in designing
causal interventions that accurately translate discrete events into SCM
modifications.

\* Intervention Type Selection: You have full discretion to select the
most appropriate intervention type(s) for each scenario:

\* Parametric: Modifications to GIM assumptions only (e.g., altered
growth trajectory, margin compression).

\* Structural: Modifications to the DAG/SCM structure itself (e.g.,
adding a new driver node).

\* Hybrid: Combination of Parametric and Structural modifications.

\* Lump Sum Handling (Simplified): One-time cash flow events (e.g.,
litigation settlement, asset sale proceeds, acquisition costs) should be
modeled via GIM overlay using an EXPLICIT_SCHEDULE DSL on an
\"FCF_Adjustment\" or equivalent driver. Complex structural
interventions for lump sums are NOT required under the Simplified APV
methodology.

\* The Holistic Impact Mandate: Interventions must capture the complete
economic impact of the scenario. A scenario that affects revenue should
also consider the downstream effects on margins, reinvestment, and
terminal economics where material.

\* The Anti-Cherry-Picking Mandate: Do not selectively model only the
favorable or unfavorable aspects of a scenario. If an upside scenario
also introduces execution risk or requires investment, these must be
reflected in the intervention.

P2. Structural Constraints (Pipeline Stability and Economic Coherence)

The SCENARIO stage operates within guardrails that ensure pipeline
integrity and economic validity.

\* DR Stability Mandate: The Discount Rate (DR) calculated in BASE and
inherited through ENRICHMENT MUST remain static for the Base Case and
most scenarios.

\* Risk Realignment Exception: If a scenario fundamentally and
permanently alters the firm\'s systematic risk profile (e.g., entry into
a structurally different business, material change in operating
leverage), a DR Overlay may be applied. This requires rigorous
qualitative justification in the trace documentation.

\* Economic Governor Mandate (Universal Application): The constraint (g
≈ ROIC × RR) MUST hold across all modeled scenarios. If a scenario
intervention produces a terminal state where g ≥ DR, or where ROIC and
growth are economically inconsistent, the intervention definition must
be revised.

\* The Reconciliation Check: After each scenario Kernel execution,
verify that Terminal_g and Terminal_ROIC satisfy the Economic Governor.
Document the check in the trace.

\* Capital Dynamics Stability: The Static Share Count (TSM Adjusted)
established in BASE MUST NOT be modified. Scenarios involving equity
issuance or buybacks should be modeled through their cash flow impact,
not through share count changes.

P3. Epistemic Anchoring (The Bayesian Probability Protocol)

Probability estimation MUST follow a rigorous Bayesian methodology. This
formalizes the \"Nexus Approach\" as a structured protocol.

\* The Bayesian Frame:

\* Prior: The \"Outside View\" --- historical base rates from Reference
Class Forecasting (RCF).

\* Likelihood/Evidence: The \"Inside View\" --- company-specific context
and evidence from research.

\* Posterior: The final probability estimate P(Scenario).

\* The Three-Step Protocol:

\* Anchor (Establish the Prior):

\* Identify the appropriate reference class for the scenario type.

\* Extract base rate data from scenario research (H.A.D. --- frequency,
historical occurrence rates).

\* Document: \"In the reference class of \[X\], this type of event
occurs with frequency \[Y%\].\"

\* Sample Size and Recency Check: Note the sample size and recency of
the reference class data. Base rates from samples \<10 or \>10 years old
require explicit acknowledgment of increased uncertainty.

\* Deconstruct (Causal Decomposition):

\* Decompose the scenario into a chain of prerequisite conditions.

\* Structure: P(Scenario) = P(Condition₁) × P(Condition₂\|Condition₁) ×
\... × P(Final\|All Prior)

\* This decomposition forces explicit reasoning about the causal
pathway.

\* Update (Calculate the Posterior):

\* Integrate company-specific evidence to adjust conditional
probabilities.

\* Document: \"Given \[specific evidence\], the conditional probability
of \[condition\] is adjusted from \[prior\] to \[posterior\] because
\[reasoning\].\"

\* The Calibration Mandate (Overconfidence Correction):

\* Posterior probabilities \>70% for positive scenarios or \<10% for
negative scenarios require explicit \"sanity check\" narrative.

\* Ask: \"Is there a historical precedent for this level of confidence?
What base rate of corporate events would support this probability?\"

\* The Independence Mandate: Do not artificially correlate scenario
probabilities to create a narrative. Each scenario\'s probability should
be estimated based on its own evidence, with correlations handled
explicitly in the SSE integration phase.

P4. Causal Chain Transparency (The Trace Mandate)

We mandate complete, auditable documentation of all analytical
judgments.

\* Probability Trace: For each scenario, document the full Bayesian
Protocol execution:

\* Reference class selection and justification

\* Prior (base rate) with data sources

\* Causal decomposition structure

\* Conditional probability justifications

\* Final posterior

\* Intervention Trace: For each scenario, document:

\* Intervention type selection rationale

\* Specific modifications (GIM overlay, structural changes)

\* DR overlay justification (if applicable)

\* P2 Reconciliation narrative (Economic Governor check)

\* Integration Trace: Document:

\* Constraint definitions (dependencies, MECE groups, incompatibilities)

\* SSE execution results (renormalization factor, feasible state count)

\* Any anomalies or edge cases encountered

P5. Distributional Analysis Mandate (Beyond the Mean)

The true value of probabilistic modeling lies in understanding the
distribution of outcomes, not merely the expected value.

\* The Distribution Primacy Principle: E\[IVPS\] is a summary statistic,
not the primary output. The analytical focus must be on interpreting the
shape, risk characteristics, and investment implications of the full
valuation distribution.

\* Required Distributional Metrics:

\* Percentiles: P10 (downside), P50 (median), P90 (upside)

\* Dispersion: Standard deviation, Min/Max range

\* Shape: Skewness (LEFT/SYMMETRIC/RIGHT), Modality
(UNIMODAL/BIMODAL/MULTIMODAL)

\* Visualization Mandate: Generate a visual representation of the
probability distribution across IVPS outcomes. This should be emitted in
both human-readable (ASCII) and structured (data array) formats.

\* Analytical Interpretation Requirements:

\* Risk Assessment: What does the P10 outcome imply about downside
exposure? Is it survivable from a portfolio perspective?

\* Upside Characterization: What does the P90 outcome require to
materialize? How realistic is the path?

\* Modality Interpretation: If the distribution is bimodal, what does
this imply about the binary nature of key uncertainties?

\* Skewness Interpretation: Is the distribution skewed toward risk or
opportunity? What drives this asymmetry?

\* Investment Implications Mandate: The synthesis must translate
distributional insights into actionable investment guidance:

\* Position sizing implications (given the risk/reward profile)

\* Entry timing considerations (given scenario resolution timelines)

\* Hedging or risk management considerations (given tail exposures)

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

IV\. EXECUTION PROTOCOL (The Workflow)

Execute the workflow (Phases A-F), integrating the Core Analytical
Directives throughout. Synthesize narratives internally during the
respective phases for the final unified emission.

**TURN 1: ANALYTICAL SYNTHESIS**

Execute Phases A-C and D.1-D.2. Emit Scenario Execution Arguments JSON.

Phase A: Initialization and Baseline Extraction

1\. Ingestion: Parse MRC State 2 artifacts (A.1, A.2, A.3, A.5, A.6,
A.7, A.9_ENRICHMENT_TRACE, A.8_RESEARCH_STRATEGY_MAP) and scenario
research inputs.

2\. Baseline Extraction (The Efficiency Protocol):

\* Extract State 2 metrics directly from
A.7_LIGHTWEIGHT_VALUATION_SUMMARY:

\* base_ivps: The deterministic IVPS from ENRICHMENT (this is the \"Base
Case\" for SSE)

\* dr_static: The discount rate

\* terminal_g: Base Case terminal growth rate

\* terminal_roic: Base Case terminal ROIC

\* Key forecast trajectory data

\* These establish the computational baseline. Do NOT re-execute the
Kernel for State 2.

3\. Research Inventory: Catalog available scenario research, noting
coverage of:

\* Mainline catalysts (M&A, product launches, regulatory outcomes)

\* Tail risks (Blue Sky transformative upside, Black Swan catastrophic
downside)

\* Historical Analogue Data availability (frequency, magnitude)

Phase B: Scenario Identification and Prioritization

1\. Research Synthesis:

\* Analyze scenario research comprehensively.

\* Identify discrete, material events suitable for modeling as causal
interventions.

\* For each candidate scenario, form preliminary estimates of P
(probability) and M (magnitude) based on available H.A.D.

1.5. P=1.0 Certainty Exception (Base Case Boundary):

Events meeting ALL of the following criteria are incorporated in State 2
base case and MUST be EXCLUDED from probabilistic scenario modeling:

\* Contractual Consummation: The event has reached irreversible
completion:

\- Signed and closed transaction (not merely announced)

\- Regulatory ruling issued (not pending)

\- Product shipped / service launched (not planned)

\* Management Guidance Incorporation: Management has explicitly
incorporated the event into forward guidance AND analyst consensus
reflects certainty (no "conditional" or "if approved" framing)

\* Documentation Requirement: Explicit citation to public filing (8-K,
press release, regulatory filing) confirming completion

Events NOT meeting ALL THREE criteria remain scenario candidates
regardless of apparent probability. High-probability events (e.g., "90%
likely approval") that lack contractual consummation are SCENARIO
candidates, not base case.

*Rationale: This prevents double-counting of events already embedded in
ENRICHMENT's State 2 IVPS while ensuring genuine uncertainty is
modeled.*

2\. Prioritization by Expected Materiality:

\* Rank candidate scenarios by \|P × M\| (expected absolute impact on
IVPS).

\* Select the top 4 scenarios for modeling.

\* Distributional Completeness Check: Ensure the selected scenarios span
the outcome distribution:

\* At least one material UPSIDE scenario (Mainline or Blue Sky)

\* At least one material DOWNSIDE scenario (Mainline or Black Swan)

\* If the top 4 by \|P × M\| are skewed toward one direction, consider
substituting to achieve balance.

3\. Scenario Classification: Classify each selected scenario:

\* MAINLINE: High-probability discrete events with moderate impact
(e.g., likely M&A, expected product launch)

\* BLUE_SKY: Low-probability transformative upside (e.g., market
dominance, breakthrough adoption)

\* BLACK_SWAN: Low-probability catastrophic downside (e.g.,
technological obsolescence, existential regulatory action)

4\. Documentation: Record selection rationale, rejected candidates, and
completeness check in the trace.

Phase C: Probability Estimation (Bayesian Protocol)

For each selected scenario, execute the P3 Bayesian Probability
Protocol:

1\. Prior Establishment (The Outside View):

\* Identify the reference class from scenario research.

\* Extract base rate data (historical frequency of similar events).

\* Document the prior: P_prior = \[X%\] based on \[reference class\]
with sample size \[N\].

2\. Causal Decomposition:

\* Decompose the scenario into prerequisite conditions.

\* Structure the probability chain: P(Scenario) = P(A) × P(B\|A) ×
P(C\|A,B) × \...

\* This forces explicit reasoning about what must happen for the
scenario to materialize.

3\. Bayesian Update (The Inside View):

\* For each conditional probability, integrate company-specific
evidence.

\* Adjust from the base rate based on:

\* Company-specific capabilities or vulnerabilities

\* Market positioning relative to the reference class

\* Temporal factors (is the company earlier/later in the relevant
cycle?)

\* Calculate the final posterior: P_posterior = \[Y%\].

4\. Calibration Check:

\* If P_posterior \> 70% (for upside) or P_posterior \< 10% (for
downside), execute the Overconfidence Correction narrative.

\* Document the sanity check in the trace.

5\. Documentation: Complete the probability trace for each scenario.

Phase D: Magnitude Estimation (Causal Interventions via Kernel)

For each selected scenario, design and execute the causal intervention:

1\. Intervention Design (P1 Judgment):

\* Determine intervention type: PARAMETRIC / STRUCTURAL / HYBRID

\* For PARAMETRIC: Define the gim_overlay --- the specific GIM entries
that differ from the Base Case under this scenario.

\* For STRUCTURAL: Define structural_modifications --- changes to DAG
nodes or equations.

\* For Lump Sums: Use EXPLICIT_SCHEDULE on an FCF adjustment driver.

2\. Risk Alignment Assessment (P2):

\* Assess whether the scenario fundamentally alters systematic risk.

\* If yes, define dr_overlay and prepare rigorous justification.

\* If no (the typical case), DR remains static.

**T1 Emission: Scenario Execution Arguments**

Compile scenario definitions with probabilities and intervention specifications. Structure per T1 Output Schema (Appendix A.1). Embed JSON in Turn 1 markdown output. Kernel code attached for contextual reference only — DO NOT EXECUTE.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**TURN 2: KERNEL EXECUTION**

Fresh context. Load kernel, parse T1 JSON, execute deterministically.

**T2 Initialization: Artifact Ingestion**

Re-ingest MRC State 2 artifacts from ENRICHMENT outputs (A.2_ANALYTIC_KG, A.3_CAUSAL_DAG, A.5_GESTALT_IMPACT_MAP, A.6_DR_DERIVATION_TRACE, A.7_LIGHTWEIGHT_VALUATION_SUMMARY). Parse Turn 1 Scenario Execution Arguments JSON. Load CVR_KERNEL_SCEN_2.2.1e.py into execution environment.

3\. Kernel Execution:

\* Prepare modified artifacts based on intervention definition.

\* Load the CVR Kernel into the execution environment.

3.5 Execution Verification Gate:

\* Record the code output line that produced ivps_scenario for each
scenario

\* Critical: Compaction note: Inherited IVPS values are
hypotheses---re-execute before Phase E

Execute execute_scenario_intervention():

result = execute_scenario_intervention( kg=base_kg, dag=base_dag,
gim=base_gim, dr_trace=base_dr_trace,
intervention_def=scenario_intervention, dr_override=dr_overlay \# if
applicable)

\* Extract: ivps_scenario, ivps_impact, terminal_g, terminal_roic

4\. P2 Reconciliation:

\* Verify Economic Governor: Is terminal_g ≈ terminal_roic × RR?

\* Verify: terminal_g \< DR (otherwise perpetuity is undefined)

\* If FAIL: Revise intervention definition and re-execute.

\* Document reconciliation status and narrative.

5\. Documentation: Complete the intervention trace for each scenario.

Phase E: Integration and Distributional Analysis (Kernelized SSE)

1\. Constraint Definition (P4):

\* Causal Dependencies: Define any conditional relationships between
scenarios.

\* Example: P(Scenario_B \| Scenario_A) if B depends on A occurring.

\* Mutual Exclusivity (MECE): Define scenarios that are different
outcomes of the same root event.

\* Example: \"Acquisition Succeeds\" and \"Acquisition Fails\" are MECE.

\* Economic Incompatibilities: Define scenario pairs that cannot
logically co-occur.

\* Mandatory: BLUE_SKY and BLACK_SWAN scenarios MUST be defined as
incompatible.

\* Example: \"Market Dominance\" and \"Technological Obsolescence\"
cannot co-occur.

2\. SSE Execution (Kernelized):

\* Prepare the scenario and constraint inputs for the Kernel.

Execute calculate_sse_jpd():

sse_result = calculate_sse_jpd( scenarios=\[ {\'scenario_id\': \'S1\',
\'p_posterior\': 0.25, \'ivps_impact\': 15.0}, {\'scenario_id\': \'S2\',
\'p_posterior\': 0.10, \'ivps_impact\': -30.0}, \# \... \],
constraints={ \'causal_dependencies\': \[\...\],
\'mutual_exclusivity_groups\': \[\...\], \'economic_incompatibilities\':
\[\...\] }, base_ivps=base_case_ivps)

\* \* The Kernel executes the Initialize-Filter-Renormalize procedure:

\* Initialize: Enumerate all 2\^N states, calculate initial
probabilities.

\* Filter: Eliminate infeasible states (MECE/Incompatibility
violations).

\* Renormalize: Scale remaining probabilities to sum to 1.0.

\* Apply Limited Liability: Floor all IVPS values at 0.0.

\* Extract: e_ivps, distribution_stats, states, renormalization_factor

3\. Distribution Visualization:

\* Generate visualization using Kernel output.

\* Produce both ASCII representation and structured data array.

4\. Distributional Analysis (P5):

\* Analyze the distribution characteristics:

\* Percentiles (P10, P50, P90)

\* Skewness and its drivers

\* Modality (is there a bimodal \"barbell\" distribution?)

\* Compare E\[IVPS\] to Base Case IVPS --- what drives the delta?

\* Identify which scenario probabilities have the largest impact on
E\[IVPS\].

5\. Documentation: Record integration methodology, constraints, SSE
results, and analysis.

Phase F: Synthesis and Emission

1\. Executive Synthesis (P4/P5):

\* Compose a high-value analytical narrative covering:

\* The transition from deterministic (State 2) to probabilistic (State
3) valuation

\* Key drivers of the distribution shape

\* Risk assessment (downside exposure at P10)

\* Opportunity assessment (upside potential at P90)

\* Interpretation of E\[IVPS\] vs. Base Case IVPS

2\. CVR Bridge:

\* Quantify: State 2 IVPS → State 3 E\[IVPS\]

\* Attribution: Which scenarios and probabilities drive the delta?

3\. Investment Implications:

\* Translate distributional insights into actionable guidance:

\* Position sizing given risk/reward profile

\* Entry timing given scenario resolution timelines

\* Risk management given tail exposures

4\. Artifact Construction:

\* Compile A.10_SCENARIO_MODEL_OUTPUT per the schema (Appendix A).

\* Validate completeness against schema requirements.

5\. Emission (MRC State 3):

\* Emit the single consolidated artifact: A.10_SCENARIO_MODEL_OUTPUT

\* MRC State 3 = MRC State 2 + A.10

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

V. ARTIFACT EMISSION CHECKLIST

The SCENARIO stage produces a single consolidated artifact that captures
the complete probabilistic analysis:

Artifact

Schema

Description

A.10_SCENARIO_MODEL_OUTPUT

Appendix A

Consolidated artifact containing scenario definitions, probability
traces, intervention traces, SSE results, distributional analysis, and
analytical synthesis

Emission Format: JSON, validated against schema.

State Transition: Upon successful emission, the CVR transitions from MRC
State 2 (deterministic) to MRC State 3 (probabilistic).

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

APPENDIX A.1: Turn 1 Output Schema (Scenario Execution Arguments)

This schema defines the JSON structure emitted by Turn 1 for consumption
by Turn 2.

{

"schema_version": "G3_2.2.1eS_T1_ARGS",

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
constraints, then executes kernel functions with these parameters. Full
schema available in G3ENRICH_2_2_1e.md patch plan.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

APPENDIX A.2: Final Output Schema (A.10_SCENARIO_MODEL_OUTPUT)

{

\"schema_version\": \"G3_2.2.1eS\",

\"version_control\": {

\"paradigm\": \"G3 Meta-Prompting Doctrine v2.4 (Two-Shot Guided
Autonomy)\",

\"pipeline_stage\": \"SCENARIO G3_2.2.1e\",

\"execution_model\": \"Two-Shot (T1=Analysis, T2=Execution)\",

\"base_compatibility\": \"G3BASE 2.2.1e\",

\"rq_compatibility\": \"G3RQ 2.2.2\",

\"enrich_compatibility\": \"G3ENRICH 2.2.1e\"

},

\"metadata\": {

\"company_name\": \"string\",

\"ticker\": \"string (EXCHANGE:SYMBOL)\",

\"valuation_date\": \"string (YYYY-MM-DD)\",

\"currency\": \"string (e.g., USD)\",

\"execution_timestamp\": \"string (ISO 8601)\",

\"base_case_reference\": {

\"source_stage\": \"G3_ENRICHMENT_2.2\",

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

APPENDIX B: NORMATIVE DEFINITIONS

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

B.1. Financial Definitions and Formulas (Simplified APV)

Inherited from G3 BASE/ENRICHMENT 2.2.1e.

\#

Term

Definition

Formula/Notes

1

EBIT

Earnings Before Interest and Taxes

Revenue − OpEx (incl. SBC) − D&A. MUST include SBC.

2

NOPAT

Net Operating Profit After Tax

EBIT × (1 − Tax Rate)

3

Invested Capital (IC)

Capital deployed in operations

NWC + Net PP&E + Intangibles + Goodwill. Exclude excess cash.

4

ROIC

Return on Invested Capital

NOPAT / PREV(IC). MUST use BOP IC.

5

Reinvestment

Capital invested for growth

ΔIC = IC(t) − IC(t−1)

6

Reinvestment Rate (RR)

NOPAT proportion reinvested

Reinvestment / NOPAT

7

FCF (Unlevered)

Cash flow to all capital providers

NOPAT − Reinvestment = NOPAT × (1 − RR)

8

Growth (g)

Sustainable growth rate

ROIC × RR. Economic Governor: g ≈ ROIC × RR must hold at terminal.

9\. Valuation Methodology (Simplified APV, 20-Year, Static DR)

\* Discounting: End-of-year convention

\* DR: Static, derived in BASE (unless DR Overlay justified)

\* PV Explicit FCF: Σ(FCF_t / (1+DR)\^t) for t=1→20

\* Terminal Value: TV = FCF₂₁ / (DR − g_terminal), where FCF₂₁ = FCF₂₀ ×
(1 + g_terminal)

\* Enterprise Value: EV = PV_Explicit + PV_Terminal

\* Equity Value: EV − Net_Debt_Y0

\* IVPS: Equity_Value / Shares_Outstanding_Diluted_TSM

11\. Timing Convention (DAG Compliance)

\* ROIC MUST use PREV(Invested_Capital)

\* All balance sheet denominators MUST use PREV()

12\. ATP Mandate (Accounting Translation Protocol)

\* All A.2 inputs are ATP-reconciled per BASE P1.5

\* Scenario interventions must use ATP-reconciled values from
accounting_translation_log

\* Normative definitions (e.g., EBIT incl. SBC) take precedence over raw
reported figures

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

15\. Normative Inheritance (ENRICHMENT 2.2.1e)

Items 12-14 from ENRICHMENT 2.2.1e normative definitions are inherited
implicitly:

\* 12: Tax_Rate Sourcing --- Exogenous driver; marginal statutory
default unless justified

\* 13: Y0 Basis Convention --- Most recent fiscal year unless LTM noted

\* 14: Negative Terminal ROIC --- If ROIC ≤ 0: g=0, RR=0; TV = NOPAT_T /
DR

*These apply to scenario interventions that modify terminal economics.
If a scenario intervention produces Terminal ROIC ≤ 0, apply Item 14
boundary conditions.*

B.2. Assumption DSL Definitions (20-Year Horizon)

Y0 = historical starting value from ANALYTIC_KG

Mode

Behavior

Key Parameters

STATIC

Constant all 20 years

value

LINEAR_FADE

Linear interpolation Y0→end

end_value, end_year

CAGR_INTERP

Geometric interpolation

target_value, target_year (if start≤0, uses LINEAR)

S_CURVE

Logistic growth toward saturation

saturation_point, steepness_factor, inflection_point_year

EXPLICIT_SCHEDULE

Year-by-year specification

schedule\[\], post_schedule_dsl (optional). Primary method for Lump
Sums.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

B.6. Do-Intervention Types (Causal Intervention Framework)

Intervention Taxonomy

Type

Definition

Implementation

Use Cases

Parametric

GIM modification only, no SCM structure change

gim_overlay with differing entries

Growth/margin shifts, efficiency changes

Structural

SCM structure change (DAG/equations)

structural_modifications

New revenue streams, business model changes

Hybrid

Both Parametric + Structural

Both fields defined

Complex scenarios (e.g., market entry)

Lump Sum Handling (Simplified)

1\. Add \"FCF_Adjustment\" driver if needed

2\. Use EXPLICIT_SCHEDULE: {\"schedule\": \[0, 0, -50000000, 0, \...\],
\"post_schedule_dsl\": {\"type\": \"STATIC\", \"value\": 0}}

3\. Flows directly to FCF (no debt dynamics under Simplified APV)

Design Principles

\* Holistic Impact: Capture complete economic effect (investment, margin
dilution, execution risk)

\* Economic Coherence: Intervened SCM must satisfy Economic Governor at
terminal

\* Minimal Modification: Prefer simplest intervention type that captures
scenario economics

\* Reversibility: Permanent = modified terminal assumptions; Temporary =
EXPLICIT_SCHEDULE with reversion

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

B.7. Probability Estimation (Bayesian Protocol)

Framework: P(Scenario) = P(C₁) × P(C₂\|C₁) × P(C₃\|C₁,C₂) × \... ×
P(Outcome\|All Conditions)

Three-Step Protocol

Step 1: ANCHOR (Prior/Outside View)

\* Select reference class (specific enough to be relevant, broad enough
for N≥10)

\* Extract base rate from H.A.D. (frequency, time horizon, trends)

\* Assess data quality: sample size (N\<10 = high uncertainty), recency
(\>10yr = check structural changes), survivorship bias

\* Document: \"In reference class \[X\], event occurs at \[Y%\] based on
\[N\] observations over \[period\]\"

Step 2: DECONSTRUCT (Causal Decomposition)

\* Identify prerequisite chain: market conditions → company capabilities
→ triggers → execution

\* Express as conditional probability product

\* Purpose: Forces explicit reasoning, prevents story-driven estimation,
enables auditability

Step 3: UPDATE (Posterior/Inside View)

\* Integrate company-specific evidence to adjust each conditional

\* Document direction, magnitude, and evidence for each adjustment

\* Extraordinary claims require extraordinary evidence

\* Calculate final P(Scenario) by multiplying through decomposition

Calibration Mandates

Overconfidence Correction (Mandatory if P\>70% upside OR P\<10%
downside):

\* \"What is the base rate? Does my estimate exceed it, and why?\"

\* \"Am I accounting for unknown unknowns?\"

\* \"Would I bet at these odds?\"

\* Document sanity check in trace

Independence Mandate: Estimate probabilities independently per scenario;
correlations handled in SSE (B.8)

Common Errors to Avoid:

1\. Anchoring on management guidance (not base rates)

2\. Neglecting base rates (\"this company is special\")

3\. Conjunction fallacy: P(A∩B) ≤ P(A)

4\. Availability bias (recent/vivid ≠ more probable)

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

B.8. Integration Methodology (Structured State Enumeration)

Core Concepts

\* State Space: N scenarios → 2\^N states (each scenario occurs or
doesn\'t)

\* Feasibility: Infeasible states get P=0, excluded from distribution

\* State IVPS: Base + sum of active scenario impacts

\* E\[IVPS\]: Probability-weighted average across feasible states

Initialize-Filter-Renormalize Procedure

Phase

Action

Output

1\. Initialize

Calculate P_initial for all 2\^N states. Independent: ∏P(active) ×
∏(1−P(inactive)). Handle dependencies if defined.

{state_id, scenarios_active, p_initial}

2\. Filter

Eliminate infeasible states: MECE violations (P=0 if mutually exclusive
scenarios co-occur), Economic incompatibilities (P=0 if incompatible
pairs co-occur). MANDATORY: BLUE_SKY ↔ BLACK_SWAN incompatible.

Feasibility flags updated

3\. Renormalize

RF = 1.0 / Σ(P_initial for feasible). P_final = P_initial × RF
(feasible) or 0 (infeasible). Validate: Σ(P_final) = 1.0

Final JPD

State IVPS Calculation

Additive Impact: IVPS_raw(State) = IVPS_Base + Σ(IVPS_Impact for active
scenarios)

\* Assumes approximately additive impacts (tractability assumption)

\* Non-linear interactions noted as model limitations if material

Limited Liability: IVPS_final = MAX(0.0, IVPS_raw)

\* Equity cannot go negative; floor at zero

\* Flag when constraint binds; retain raw value for transparency

E\[IVPS\]: Σ(P_final × IVPS_final) --- exact calculation, not simulation

Kernelized Execution: calculate_sse_jpd() ensures computational
integrity, constraint enforcement, reproducibility

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

B.9. Distributional Analysis Protocol

Distribution Primacy: E\[IVPS\] is a summary statistic. Full
distribution reveals risk (left tail), opportunity (right tail),
uncertainty (range), and shape.

Required Metrics

Percentiles (calculated by ordering states by IVPS, accumulating
probabilities, interpolating):

Metric

Meaning

P10

Downside case (10% below)

P50

Median (more robust than mean for skewed distributions)

P90

Upside case (90% below)

Dispersion:

\* Range: Max − Min IVPS

\* Std Dev: σ = √(Σ P × (IVPS − E\[IVPS\])²)

\* Coef. of Variation: σ / E\[IVPS\] (enables cross-company comparison)

Shape:

Skewness

Condition

Interpretation

LEFT

Mean \< Median

Long left tail; downside \> upside

SYMMETRIC

Mean ≈ Median

Balanced

RIGHT

Mean \> Median

Long right tail; upside \> downside

Modality

Meaning

UNIMODAL

Single peak; outcomes cluster centrally

BIMODAL

Two peaks; binary uncertainty

MULTIMODAL

Multiple peaks; complex interactions

Visualization

ASCII Format (embed in artifact):

IVPS Distribution

\$0-10 \| ████ (12%)

\$10-20 \| ██ (6%)

\$20-30 \| ███████████ (28%) ← Base Case

\$30-40 \| ████████████████ (35%)

\$40-50 \| ███████ (15%)

E\[IVPS\]: \$31.50 \| Median: \$32.00 \| P10: \$8.50 \| P90: \$48.00

Structured Data: Array of {ivps_bucket_label, ivps_bucket_midpoint,
probability_mass, cumulative_probability}

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

APPENDIX C: CVR Kernel (G3_2.2.1e_SCEN)

\#
==========================================================================================

\# CVR KERNEL G3_2.2.1e_SCEN - CONSOLIDATED (ENRICHMENT BASE + SCENARIO
EXTENSIONS)

\#
==========================================================================================

\#

\# Consolidated kernel: ENRICHMENT 2.2.1e base functions + SCENARIO
extensions. Delivered to T1 (contextual) and T2 (executable).

\# For Two-Shot execution: T1 uses for context; T2 loads
CVR_KERNEL_SCEN_2.2.1e.py for execution.

\#

\# Dependencies: numpy, pandas, copy, math, itertools (add itertools to
imports)

\#
==========================================================================================

from itertools import product

import copy

import math

\# Update kernel version (modify existing constant)

\# KERNEL_VERSION = \"G3_2.2.1e_SCEN\"

\#
==========================================================================================

\# 1. INTERVENTION APPLICATION FUNCTIONS

\#
==========================================================================================

def apply_gim_overlay(base_gim, gim_overlay):

\"\"\"

Applies a GIM overlay to the base GIM, creating a scenario-modified GIM.

The overlay contains only the drivers that differ from the base case.

Drivers not in the overlay retain their base case values.

Parameters:

\-\-\-\-\-\-\-\-\-\--

base_gim : dict

The base case GIM artifact (A.5) with structure {\'GIM\': {\...}}

gim_overlay : dict

Dictionary of modified drivers: {driver_handle: new_assumption_dict}

Returns:

\-\-\-\-\-\-\--

dict : Modified GIM artifact

\"\"\"

\# Deep copy to avoid mutating the base

modified_gim = copy.deepcopy(base_gim)

\# Get the GIM dict (handle both {\'GIM\': {\...}} and direct dict
formats)

if \'GIM\' in modified_gim:

gim_dict = modified_gim\[\'GIM\'\]

else:

gim_dict = modified_gim

\# Apply overlay

if gim_overlay:

for driver_handle, new_assumption in gim_overlay.items():

if driver_handle in gim_dict:

\# Update existing driver

gim_dict\[driver_handle\]\[\'assumption\'\] = new_assumption

else:

\# Add new driver (for structural additions that need GIM entries)

gim_dict\[driver_handle\] = {

\'assumption\': new_assumption,

\'source\': \'SCENARIO_OVERLAY\'

}

return modified_gim

def apply_structural_modifications(base_dag, modifications):

\"\"\"

Applies structural modifications to the DAG for structural/hybrid
interventions.

Parameters:

\-\-\-\-\-\-\-\-\-\--

base_dag : dict

The base case CAUSAL_DAG artifact (A.3)

modifications : list

List of modification specifications:

\[

{

\'modification_type\': \'ADD_NODE\' \| \'REMOVE_NODE\' \|
\'MODIFY_EQUATION\' \| \'ADD_EDGE\',

\'target_node\': str,

\'details\': {

\'new_equation\': str (for MODIFY_EQUATION),

\'new_edges\': list (for ADD_EDGE),

\'node_definition\': dict (for ADD_NODE)

}

}

\]

Returns:

\-\-\-\-\-\-\--

dict : Modified DAG artifact

\"\"\"

modified_dag = copy.deepcopy(base_dag)

\# Get the DAG structure

if \'DAG\' in modified_dag:

dag_struct = modified_dag\[\'DAG\'\]

else:

dag_struct = modified_dag

\# Ensure required sub-structures exist

if \'nodes\' not in dag_struct:

dag_struct\[\'nodes\'\] = {}

if \'edges\' not in dag_struct:

dag_struct\[\'edges\'\] = {}

if \'equations\' not in dag_struct:

dag_struct\[\'equations\'\] = {}

for mod in modifications or \[\]:

mod_type = mod.get(\'modification_type\', mod.get(\'type\'))

target = mod.get(\'target_node\')

details = mod.get(\'details\', {})

if mod_type == \'ADD_NODE\':

\# Add a new node to the DAG

node_def = details.get(\'node_definition\', {})

dag_struct\[\'nodes\'\]\[target\] = node_def

\# Add edges if specified

if \'new_edges\' in details:

dag_struct\[\'edges\'\]\[target\] = details\[\'new_edges\'\]

else:

dag_struct\[\'edges\'\]\[target\] = \[\]

\# Add equation if specified

if \'new_equation\' in details:

dag_struct\[\'equations\'\]\[target\] = details\[\'new_equation\'\]

elif mod_type == \'REMOVE_NODE\':

\# Remove a node (use with caution - may break dependencies)

if target in dag_struct\[\'nodes\'\]:

del dag_struct\[\'nodes\'\]\[target\]

if target in dag_struct\[\'edges\'\]:

del dag_struct\[\'edges\'\]\[target\]

if target in dag_struct\[\'equations\'\]:

del dag_struct\[\'equations\'\]\[target\]

elif mod_type == \'MODIFY_EQUATION\':

\# Modify an existing equation

if \'new_equation\' in details:

dag_struct\[\'equations\'\]\[target\] = details\[\'new_equation\'\]

elif mod_type == \'ADD_EDGE\':

\# Add edges to an existing node

if target in dag_struct\[\'edges\'\]:

dag_struct\[\'edges\'\]\[target\].extend(details.get(\'new_edges\',
\[\]))

else:

dag_struct\[\'edges\'\]\[target\] = details.get(\'new_edges\', \[\])

return modified_dag

\#
==========================================================================================

\# 2. SCENARIO INTERVENTION EXECUTION

\#
==========================================================================================

def execute_scenario_intervention(kg, dag, gim, dr_trace,
intervention_def, dr_override=None):

\"\"\"

Executes a single scenario intervention and returns the deterministic
IVPS.

This function applies the intervention to the base case artifacts,
executes

the SCM forecast, calculates APV valuation, and validates P2
constraints.

Parameters:

\-\-\-\-\-\-\-\-\-\--

kg : dict

A.2_ANALYTIC_KG artifact (base case)

dag : dict

A.3_CAUSAL_DAG artifact (base case)

gim : dict

A.5_GESTALT_IMPACT_MAP artifact (base case)

dr_trace : dict

A.6_DR_DERIVATION_TRACE artifact

intervention_def : dict

Intervention specification:

{

\'gim_overlay\': dict \| None,

\'structural_modifications\': list \| None

}

dr_override : float, optional

Scenario-specific discount rate (overrides dr_trace if provided)

Returns:

\-\-\-\-\-\-\--

dict : {

\'ivps_scenario\': float,

\'ivps_base\': float,

\'ivps_impact\': float,

\'terminal_g\': float,

\'terminal_roic\': float,

\'terminal_rr\': float,

\'dr_used\': float,

\'p2_status\': \'PASS\' \| \'FAIL\',

\'p2_message\': str,

\'forecast_df\': DataFrame (for debugging, optional)

}

\"\"\"

\# 1. Apply GIM overlay

gim_overlay = intervention_def.get(\'gim_overlay\')

modified_gim = apply_gim_overlay(gim, gim_overlay) if gim_overlay else
copy.deepcopy(gim)

\# 2. Apply structural modifications

structural_mods = intervention_def.get(\'structural_modifications\')

modified_dag = apply_structural_modifications(dag, structural_mods) if
structural_mods else copy.deepcopy(dag)

\# 3. Determine discount rate

if dr_override is not None:

dr = float(dr_override)

else:

\# Extract from dr_trace (handle various structures)

try:

dr_data = dr_trace.get(\'derivation_trace\', dr_trace)

if isinstance(dr_data.get(\'DR_Static\'), dict):

dr = float(dr_data\[\'DR_Static\'\]\[\'value\'\])

else:

dr = float(dr_data.get(\'DR_Static\', dr_data.get(\'dr_calculation\',
{}).get(\'DR_Static\', {}).get(\'value\')))

except (KeyError, TypeError, ValueError) as e:

raise RuntimeError(f\"Failed to extract DR from dr_trace: {e}\")

\# 4. Execute topological sort on modified DAG

dag_struct = modified_dag.get(\'DAG\', modified_dag)

try:

seq = topological_sort(dag_struct)

except Exception as e:

raise RuntimeError(f\"Topological sort failed on modified DAG: {e}\")

\# 5. Execute SCM forecast

gim_struct = modified_gim.get(\'GIM\', modified_gim)

try:

forecast_df = execute_scm(kg, dag_struct, seq, gim_struct)

except Exception as e:

raise RuntimeError(f\"SCM execution failed for scenario: {e}\")

\# 6. Calculate APV valuation

try:

valuation_results = calculate_apv(forecast_df, dr, kg)

except Exception as e:

raise RuntimeError(f\"APV calculation failed for scenario: {e}\")

\# 7. Extract results

ivps_scenario = valuation_results.get(\'IVPS\', 0.0)

terminal_g = valuation_results.get(\'Terminal_g\', 0.0)

\# Get terminal ROIC from forecast

terminal_roic = 0.0

if \'ROIC\' in forecast_df.columns:

terminal_roic = float(forecast_df\[\'ROIC\'\].iloc\[-1\])

elif \'Terminal_ROIC\' in valuation_results:

terminal_roic = valuation_results\[\'Terminal_ROIC\'\]

\# Calculate terminal reinvestment rate

terminal_rr = 0.0

if \'Reinvestment_Rate\' in forecast_df.columns:

terminal_rr = float(forecast_df\[\'Reinvestment_Rate\'\].iloc\[-1\])

elif terminal_roic \> EPSILON:

terminal_rr = terminal_g / terminal_roic if terminal_roic \> EPSILON
else 0.0

\# 8. P2 Reconciliation (Economic Governor Check)

p2_status = \'PASS\'

p2_messages = \[\]

\# Check g \< DR (perpetuity validity)

if terminal_g \>= dr:

p2_status = \'FAIL\'

p2_messages.append(f\"Terminal g ({terminal_g:.4f}) \>= DR ({dr:.4f}).
Perpetuity undefined.\")

\# Check Economic Governor: g ≈ ROIC × RR

if terminal_roic \> EPSILON and terminal_rr \> EPSILON:

implied_g = terminal_roic \* terminal_rr

governor_diff = abs(terminal_g - implied_g)

\# Allow 10% tolerance

if governor_diff \> max(0.005, abs(implied_g) \* 0.10):

p2_messages.append(f\"Economic Governor deviation: g={terminal_g:.4f},
ROIC×RR={implied_g:.4f}\")

\# This is a warning, not necessarily a failure

p2_message = \"; \".join(p2_messages) if p2_messages else \"Economic
Governor satisfied.\"

\# 9. Calculate base case IVPS for comparison (need to run base case
too)

\# For efficiency, we assume base_ivps is passed separately or cached

\# Here we return components for the caller to compute impact

\# 10. Extract Y1 fundamentals from intervened forecast for IRR stage
(Patch 1.1)

\# These fundamentals reflect the scenario-specific trajectory

fundamentals_y1_intervened = {}

if forecast_df is not None and len(forecast_df) \> 0:

\# Y1 is typically index 1 (Y0=0, Y1=1, etc.) but fallback to first row
if needed

y1_idx = 1 if len(forecast_df) \> 1 else 0

\# Extract key metrics with safe column access

if \'Revenue\' in forecast_df.columns:

fundamentals_y1_intervened\[\'revenue\'\] =
float(forecast_df\[\'Revenue\'\].iloc\[y1_idx\])

if \'EBITDA\' in forecast_df.columns:

fundamentals_y1_intervened\[\'ebitda\'\] =
float(forecast_df\[\'EBITDA\'\].iloc\[y1_idx\])

if \'EBIT\' in forecast_df.columns:

fundamentals_y1_intervened\[\'ebit\'\] =
float(forecast_df\[\'EBIT\'\].iloc\[y1_idx\])

\# Calculate EBIT margin if revenue available

if \'revenue\' in fundamentals_y1_intervened and
fundamentals_y1_intervened\[\'revenue\'\] \> EPSILON:

fundamentals_y1_intervened\[\'ebit_margin\'\] = (

fundamentals_y1_intervened\[\'ebit\'\] /
fundamentals_y1_intervened\[\'revenue\'\]

)

if \'NOPAT\' in forecast_df.columns:

fundamentals_y1_intervened\[\'nopat\'\] =
float(forecast_df\[\'NOPAT\'\].iloc\[y1_idx\])

if \'FCF_Unlevered\' in forecast_df.columns:

fundamentals_y1_intervened\[\'fcf_unlevered\'\] =
float(forecast_df\[\'FCF_Unlevered\'\].iloc\[y1_idx\])

elif \'FCF\' in forecast_df.columns:

fundamentals_y1_intervened\[\'fcf_unlevered\'\] =
float(forecast_df\[\'FCF\'\].iloc\[y1_idx\])

return {

\'ivps_scenario\': ivps_scenario,

\'terminal_g\': terminal_g,

\'terminal_roic\': terminal_roic,

\'terminal_rr\': terminal_rr,

\'dr_used\': dr,

\'p2_status\': p2_status,

\'p2_message\': p2_message,

\'valuation_details\': {

\'enterprise_value\': valuation_results.get(\'Enterprise_Value\', 0.0),

\'equity_value\': valuation_results.get(\'Equity_Value\', 0.0),

\'pv_explicit_fcf\': valuation_results.get(\'PV_Explicit_FCF\', 0.0),

\'pv_terminal_fcf\': valuation_results.get(\'PV_Terminal_FCF\', 0.0)

},

\'fundamentals_y1_intervened\': fundamentals_y1_intervened \# Patch 1.1:
IRR stage input

}

\#
==========================================================================================

\# 3. STRUCTURED STATE ENUMERATION (SSE) FUNCTIONS

\#
==========================================================================================

def enumerate_states(scenario_ids):

\"\"\"

Enumerates all 2\^N possible states for N scenarios.

Parameters:

\-\-\-\-\-\-\-\-\-\--

scenario_ids : list

List of scenario identifiers \[\'S1\', \'S2\', \'S3\', \...\]

Returns:

\-\-\-\-\-\-\--

list : List of state dictionaries

\[

{\'state_id\': \'BASE\', \'scenarios_active\': \[\]},

{\'state_id\': \'S1\', \'scenarios_active\': \[\'S1\'\]},

{\'state_id\': \'S1_S2\', \'scenarios_active\': \[\'S1\', \'S2\'\]},

\...

\]

\"\"\"

n = len(scenario_ids)

states = \[\]

\# Generate all 2\^N combinations using binary representation

for i in range(2\*\*n):

active_scenarios = \[\]

for j in range(n):

if i & (1 \<\< j):

active_scenarios.append(scenario_ids\[j\])

\# Generate state ID

if not active_scenarios:

state_id = \'BASE\'

else:

state_id = \'\_\'.join(sorted(active_scenarios))

states.append({

\'state_id\': state_id,

\'scenarios_active\': active_scenarios,

\'binary_mask\': i

})

return states

def calculate_initial_probabilities(states, scenarios, constraints):

\"\"\"

Calculates initial probabilities for all states based on marginal
probabilities

and causal dependencies.

Parameters:

\-\-\-\-\-\-\-\-\-\--

states : list

Output from enumerate_states()

scenarios : list

List of scenario definitions:

\[{\'scenario_id\': \'S1\', \'p_posterior\': 0.25, \'ivps_impact\':
15.0}, \...\]

constraints : dict

Constraint definitions including causal_dependencies

Returns:

\-\-\-\-\-\-\--

list : States with p_initial added

\"\"\"

\# Build lookup for scenario probabilities

p_marginal = {s\[\'scenario_id\'\]: s\[\'p_posterior\'\] for s in
scenarios}

\# Build dependency lookup

\# dependencies\[dependent\] = {\'condition\': scenario_id,
\'p_conditional\': float}

dependencies = {}

for dep in constraints.get(\'causal_dependencies\', \[\]):

dependent = dep\[\'dependent_scenario\'\]

condition = dep\[\'condition_scenario\'\]

p_cond = dep\[\'p_conditional\'\]

dependencies\[dependent\] = {\'condition\': condition,
\'p_conditional\': p_cond}

for state in states:

active = set(state\[\'scenarios_active\'\])

p_initial = 1.0

for scenario_id, p_marg in p_marginal.items():

is_active = scenario_id in active

\# Check if this scenario has a dependency

if scenario_id in dependencies:

dep_info = dependencies\[scenario_id\]

condition_id = dep_info\[\'condition\'\]

condition_active = condition_id in active

if is_active:

if condition_active:

\# Dependent occurs and condition occurs

\# P(Dependent AND Condition) = P(Condition) × P(Dependent\|Condition)

\# We handle this by using P(Dependent\|Condition) for the dependent

p_initial \*= dep_info\[\'p_conditional\'\]

else:

\# Dependent occurs but condition doesn\'t

\# This is typically low probability or infeasible

\# P(Dependent AND NOT Condition) = P(Dependent) × P(NOT Condition \|
Dependent)

\# For simplicity, use marginal probability adjusted

\# This case often should be near-zero or handled as infeasible

p_initial \*= p_marg \* 0.1 \# Penalty for occurring without condition

else:

if condition_active:

\# Dependent doesn\'t occur but condition occurs

\# P(NOT Dependent \| Condition) = 1 - P(Dependent\|Condition)

p_initial \*= (1 - dep_info\[\'p_conditional\'\])

else:

\# Neither occurs

p_initial \*= (1 - p_marg)

else:

\# Independent scenario

if is_active:

p_initial \*= p_marg

else:

p_initial \*= (1 - p_marg)

state\[\'p_initial\'\] = p_initial

return states

def apply_constraints(states, constraints):

\"\"\"

Applies MECE and Economic Incompatibility constraints to identify
infeasible states.

Parameters:

\-\-\-\-\-\-\-\-\-\--

states : list

States with p_initial calculated

constraints : dict

{

\'mutual_exclusivity_groups\': \[{\'scenarios\': \[\'S1\', \'S2\'\],
\...}\],

\'economic_incompatibilities\': \[{\'scenario_pair\': \[\'S3\',
\'S4\'\], \...}\]

}

Returns:

\-\-\-\-\-\-\--

list : States with feasibility_status and constraint_violated fields

\"\"\"

mece_groups = constraints.get(\'mutual_exclusivity_groups\', \[\])

incompatibles = constraints.get(\'economic_incompatibilities\', \[\])

for state in states:

active = set(state\[\'scenarios_active\'\])

state\[\'feasibility_status\'\] = \'FEASIBLE\'

state\[\'constraint_violated\'\] = None

\# Check MECE constraints

for mece in mece_groups:

mece_scenarios = set(mece.get(\'scenarios\', \[\]))

\# Count how many MECE scenarios are active

active_mece = active.intersection(mece_scenarios)

if len(active_mece) \> 1:

state\[\'feasibility_status\'\] = \'INFEASIBLE_MECE\'

state\[\'constraint_violated\'\] = f\"MECE violation: {active_mece}\"

break

if state\[\'feasibility_status\'\] != \'FEASIBLE\':

continue

\# Check Economic Incompatibility constraints

for incomp in incompatibles:

pair = set(incomp.get(\'scenario_pair\', \[\]))

if pair.issubset(active):

state\[\'feasibility_status\'\] = \'INFEASIBLE_INCOMPATIBLE\'

state\[\'constraint_violated\'\] = f\"Incompatibility violation:
{pair}\"

break

return states

def renormalize_probabilities(states):

\"\"\"

Renormalizes probabilities of feasible states to sum to 1.0.

Parameters:

\-\-\-\-\-\-\-\-\-\--

states : list

States with feasibility_status applied

Returns:

\-\-\-\-\-\-\--

tuple : (states with p_final, renormalization_factor)

\"\"\"

\# Sum probabilities of feasible states

feasible_prob_sum = sum(

s\[\'p_initial\'\] for s in states

if s\[\'feasibility_status\'\] == \'FEASIBLE\'

)

if feasible_prob_sum \< EPSILON:

raise RuntimeError(\"No feasible states with positive probability. Check
constraints.\")

renormalization_factor = 1.0 / feasible_prob_sum

for state in states:

if state\[\'feasibility_status\'\] == \'FEASIBLE\':

state\[\'p_final\'\] = state\[\'p_initial\'\] \* renormalization_factor

else:

state\[\'p_final\'\] = 0.0

return states, renormalization_factor

def calculate_state_ivps(states, scenarios, base_ivps):

\"\"\"

Calculates IVPS for each state using the Additive Impact Mandate.

Parameters:

\-\-\-\-\-\-\-\-\-\--

states : list

States with probabilities calculated

scenarios : list

Scenario definitions with ivps_impact

base_ivps : float

Base case IVPS (State 2)

Returns:

\-\-\-\-\-\-\--

list : States with ivps_raw, ivps_final, limited_liability_applied

\"\"\"

\# Build impact lookup

impacts = {s\[\'scenario_id\'\]: s\[\'ivps_impact\'\] for s in
scenarios}

for state in states:

if state\[\'feasibility_status\'\] != \'FEASIBLE\':

state\[\'ivps_raw\'\] = None

state\[\'ivps_final\'\] = None

state\[\'limited_liability_applied\'\] = False

continue

\# Calculate raw IVPS using additive impact

total_impact = sum(impacts.get(sid, 0.0) for sid in
state\[\'scenarios_active\'\])

ivps_raw = base_ivps + total_impact

\# Apply Limited Liability Constraint

limited_liability_applied = ivps_raw \< 0

ivps_final = max(0.0, ivps_raw)

state\[\'ivps_raw\'\] = ivps_raw

state\[\'ivps_final\'\] = ivps_final

state\[\'limited_liability_applied\'\] = limited_liability_applied

return states

def calculate_sse_jpd(scenarios, constraints, base_ivps):

\"\"\"

Main API for Structured State Enumeration.

Implements the Initialize-Filter-Renormalize procedure.

This function guarantees computational integrity for JPD calculation.

Parameters:

\-\-\-\-\-\-\-\-\-\--

scenarios : list

List of scenario definitions:

\[

{

\'scenario_id\': \'S1\',

\'p_posterior\': 0.25,

\'ivps_impact\': 15.0

},

\...

\]

constraints : dict

{

\'causal_dependencies\': \[

{\'dependent_scenario\': \'S2\', \'condition_scenario\': \'S1\',
\'p_conditional\': 0.8}

\],

\'mutual_exclusivity_groups\': \[

{\'scenarios\': \[\'S1a\', \'S1b\'\], \'root_event\': \'Acquisition
outcome\'}

\],

\'economic_incompatibilities\': \[

{\'scenario_pair\': \[\'S_BULL\', \'S_BEAR\'\]}

\]

}

base_ivps : float

Base case IVPS from State 2

Returns:

\-\-\-\-\-\-\--

dict : {

\'states\': list of state dictionaries with full detail,

\'e_ivps\': float,

\'distribution_stats\': dict,

\'renormalization_factor\': float,

\'feasible_state_count\': int,

\'total_state_count\': int,

\'probability_sum_validation\': float

}

\"\"\"

\# Extract scenario IDs

scenario_ids = \[s\[\'scenario_id\'\] for s in scenarios\]

\# Phase 1: Initialize - Enumerate all states

states = enumerate_states(scenario_ids)

total_state_count = len(states)

\# Phase 1b: Calculate initial probabilities

states = calculate_initial_probabilities(states, scenarios, constraints)

\# Phase 2: Filter - Apply constraints

states = apply_constraints(states, constraints)

\# Phase 3: Renormalize

states, renormalization_factor = renormalize_probabilities(states)

\# Calculate state IVPS values

states = calculate_state_ivps(states, scenarios, base_ivps)

\# Validation

probability_sum = sum(s\[\'p_final\'\] for s in states)

feasible_state_count = sum(1 for s in states if
s\[\'feasibility_status\'\] == \'FEASIBLE\')

\# Calculate E\[IVPS\]

e_ivps = sum(

s\[\'p_final\'\] \* s\[\'ivps_final\'\]

for s in states

if s\[\'feasibility_status\'\] == \'FEASIBLE\'

)

\# Calculate distribution statistics

distribution_stats = calculate_distribution_statistics(states,
base_ivps)

return {

\'states\': states,

\'e_ivps\': e_ivps,

\'distribution_stats\': distribution_stats,

\'renormalization_factor\': renormalization_factor,

\'feasible_state_count\': feasible_state_count,

\'total_state_count\': total_state_count,

\'probability_sum_validation\': probability_sum

}

\#
==========================================================================================

\# 4. DISTRIBUTION ANALYSIS FUNCTIONS

\#
==========================================================================================

def calculate_percentile(sorted_states, target_percentile):

\"\"\"

Calculates the IVPS at a given percentile from sorted states.

Parameters:

\-\-\-\-\-\-\-\-\-\--

sorted_states : list

States sorted by ivps_final ascending, with cumulative_probability

target_percentile : float

Target percentile (0.0 to 1.0, e.g., 0.10 for P10)

Returns:

\-\-\-\-\-\-\--

float : IVPS at the target percentile

\"\"\"

if not sorted_states:

return 0.0

for i, state in enumerate(sorted_states):

if state\[\'cumulative_probability\'\] \>= target_percentile:

\# Linear interpolation for more accurate percentile

if i == 0:

return state\[\'ivps_final\'\]

prev_state = sorted_states\[i-1\]

prev_cum = prev_state\[\'cumulative_probability\'\]

curr_cum = state\[\'cumulative_probability\'\]

if curr_cum - prev_cum \< EPSILON:

return state\[\'ivps_final\'\]

\# Interpolate

fraction = (target_percentile - prev_cum) / (curr_cum - prev_cum)

return prev_state\[\'ivps_final\'\] + fraction \*
(state\[\'ivps_final\'\] - prev_state\[\'ivps_final\'\])

\# If we get here, return the maximum

return sorted_states\[-1\]\[\'ivps_final\'\]

def calculate_distribution_statistics(states, base_ivps):

\"\"\"

Calculates comprehensive distribution statistics from the SSE results.

Parameters:

\-\-\-\-\-\-\-\-\-\--

states : list

States with p_final and ivps_final calculated

base_ivps : float

Base case IVPS for reference

Returns:

\-\-\-\-\-\-\--

dict : Distribution statistics

\"\"\"

\# Filter to feasible states

feasible_states = \[s for s in states if s\[\'feasibility_status\'\] ==
\'FEASIBLE\' and s\[\'p_final\'\] \> EPSILON\]

if not feasible_states:

return {

\'error\': \'No feasible states with positive probability\'

}

\# Sort by IVPS for percentile calculations

sorted_states = sorted(feasible_states, key=lambda x:
x\[\'ivps_final\'\])

\# Calculate cumulative probabilities

cumulative = 0.0

for state in sorted_states:

cumulative += state\[\'p_final\'\]

state\[\'cumulative_probability\'\] = cumulative

\# Basic statistics

ivps_values = \[s\[\'ivps_final\'\] for s in feasible_states\]

probabilities = \[s\[\'p_final\'\] for s in feasible_states\]

\# E\[IVPS\] (mean)

e_ivps = sum(p \* v for p, v in zip(probabilities, ivps_values))

\# Variance and Std Dev

variance = sum(p \* (v - e_ivps)\*\*2 for p, v in zip(probabilities,
ivps_values))

std_dev = math.sqrt(variance) if variance \> 0 else 0.0

\# Min/Max

min_ivps = min(ivps_values)

max_ivps = max(ivps_values)

\# Percentiles

p10 = calculate_percentile(sorted_states, 0.10)

p25 = calculate_percentile(sorted_states, 0.25)

p50 = calculate_percentile(sorted_states, 0.50) \# Median

p75 = calculate_percentile(sorted_states, 0.75)

p90 = calculate_percentile(sorted_states, 0.90)

\# Coefficient of Variation

cv = std_dev / e_ivps if e_ivps \> EPSILON else 0.0

\# Skewness determination

if abs(e_ivps - p50) \< std_dev \* 0.1:

skewness = \'SYMMETRIC\'

elif e_ivps \> p50:

skewness = \'RIGHT\'

else:

skewness = \'LEFT\'

\# Modality detection (simplified)

\# Count \"peaks\" - states with higher probability than neighbors

\# This is a heuristic; true modality detection would require more
sophisticated analysis

peaks = 0

for i, state in enumerate(sorted_states):

is_peak = True

if i \> 0 and sorted_states\[i-1\]\[\'p_final\'\] \>=
state\[\'p_final\'\]:

is_peak = False

if i \< len(sorted_states) - 1 and sorted_states\[i+1\]\[\'p_final\'\]
\> state\[\'p_final\'\]:

is_peak = False

if is_peak and state\[\'p_final\'\] \> 0.05: \# Threshold for meaningful
peak

peaks += 1

if peaks \<= 1:

modality = \'UNIMODAL\'

elif peaks == 2:

modality = \'BIMODAL\'

else:

modality = \'MULTIMODAL\'

return {

\'e_ivps\': e_ivps,

\'median_p50\': p50,

\'p10\': p10,

\'p25\': p25,

\'p75\': p75,

\'p90\': p90,

\'min_ivps\': min_ivps,

\'max_ivps\': max_ivps,

\'range\': max_ivps - min_ivps,

\'standard_deviation\': std_dev,

\'variance\': variance,

\'coefficient_of_variation\': cv,

\'skewness\': skewness,

\'modality\': modality,

\'base_ivps_reference\': base_ivps,

\'sorted_states\': sorted_states \# For visualization

}

def generate_distribution_visualization(distribution_stats,
num_buckets=10):

\"\"\"

Generates both ASCII and structured visualizations of the IVPS
distribution.

Parameters:

\-\-\-\-\-\-\-\-\-\--

distribution_stats : dict

Output from calculate_distribution_statistics()

num_buckets : int

Number of buckets for the histogram (default 10)

Returns:

\-\-\-\-\-\-\--

dict : {

\'ascii_representation\': str,

\'structured_data\': list of bucket dicts

}

\"\"\"

sorted_states = distribution_stats.get(\'sorted_states\', \[\])

if not sorted_states:

return {

\'ascii_representation\': \'No feasible states to visualize.\',

\'structured_data\': \[\]

}

min_ivps = distribution_stats\[\'min_ivps\'\]

max_ivps = distribution_stats\[\'max_ivps\'\]

e_ivps = distribution_stats\[\'e_ivps\'\]

p10 = distribution_stats\[\'p10\'\]

p50 = distribution_stats\[\'median_p50\'\]

p90 = distribution_stats\[\'p90\'\]

\# Handle edge case where all values are the same

if max_ivps - min_ivps \< EPSILON:

bucket_width = 1.0

num_buckets = 1

else:

bucket_width = (max_ivps - min_ivps) / num_buckets

\# Initialize buckets

buckets = \[\]

for i in range(num_buckets):

bucket_start = min_ivps + i \* bucket_width

bucket_end = bucket_start + bucket_width

bucket_mid = (bucket_start + bucket_end) / 2

buckets.append({

\'bucket_index\': i,

\'ivps_bucket_label\': f\'\${bucket_start:.0f}-{bucket_end:.0f}\',

\'ivps_bucket_start\': bucket_start,

\'ivps_bucket_end\': bucket_end,

\'ivps_bucket_midpoint\': bucket_mid,

\'probability_mass\': 0.0

})

\# Assign states to buckets

for state in sorted_states:

ivps = state\[\'ivps_final\'\]

prob = state\[\'p_final\'\]

\# Find the appropriate bucket

bucket_idx = int((ivps - min_ivps) / bucket_width) if bucket_width \>
EPSILON else 0

bucket_idx = min(bucket_idx, num_buckets - 1) \# Handle edge case at max

buckets\[bucket_idx\]\[\'probability_mass\'\] += prob

\# Calculate cumulative probability

cumulative = 0.0

for bucket in buckets:

cumulative += bucket\[\'probability_mass\'\]

bucket\[\'cumulative_probability\'\] = cumulative

\# Generate ASCII representation

max_bar_width = 40

max_prob = max(b\[\'probability_mass\'\] for b in buckets) if buckets
else 0

ascii_lines = \[\]

ascii_lines.append(\"IVPS Distribution (Probability Mass)\")

ascii_lines.append(\"\")

for bucket in buckets:

label = bucket\[\'ivps_bucket_label\'\].ljust(12)

prob = bucket\[\'probability_mass\'\]

if max_prob \> EPSILON:

bar_width = int((prob / max_prob) \* max_bar_width)

else:

bar_width = 0

bar = \'█\' \* bar_width

pct_str = f\"({prob\*100:.1f}%)\"

\# Mark special buckets

markers = \[\]

mid = bucket\[\'ivps_bucket_midpoint\'\]

if bucket\[\'ivps_bucket_start\'\] \<= e_ivps \<
bucket\[\'ivps_bucket_end\'\]:

markers.append(\'← E\[IVPS\]\')

marker_str = \' \'.join(markers)

ascii_lines.append(f\"{label} \| {bar} {pct_str} {marker_str}\")

ascii_lines.append(\"\")

ascii_lines.append(f\"E\[IVPS\]: \${e_ivps:.2f} \| Median: \${p50:.2f}
\| P10: \${p10:.2f} \| P90: \${p90:.2f}\")

ascii_representation = \'\\n\'.join(ascii_lines)

\# Prepare structured data (without the internal sorted_states)

structured_data = \[

{

\'ivps_bucket_label\': b\[\'ivps_bucket_label\'\],

\'ivps_bucket_midpoint\': b\[\'ivps_bucket_midpoint\'\],

\'probability_mass\': b\[\'probability_mass\'\],

\'cumulative_probability\': b\[\'cumulative_probability\'\]

}

for b in buckets

\]

return {

\'ascii_representation\': ascii_representation,

\'structured_data\': structured_data

}

\#
==========================================================================================

\# 5. PROBABILITY SENSITIVITY ANALYSIS

\#
==========================================================================================

def calculate_probability_sensitivity(scenarios, constraints, base_ivps,
delta_p=0.10):

\"\"\"

Analyzes how changes in scenario probabilities affect E\[IVPS\].

Parameters:

\-\-\-\-\-\-\-\-\-\--

scenarios : list

Scenario definitions

constraints : dict

SSE constraints

base_ivps : float

Base case IVPS

delta_p : float

Probability shift to test (default 0.10 = 10%)

Returns:

\-\-\-\-\-\-\--

list : Sensitivity results for each scenario

\"\"\"

\# Get baseline E\[IVPS\]

baseline_result = calculate_sse_jpd(scenarios, constraints, base_ivps)

baseline_e_ivps = baseline_result\[\'e_ivps\'\]

sensitivities = \[\]

for i, scenario in enumerate(scenarios):

scenario_id = scenario\[\'scenario_id\'\]

original_p = scenario\[\'p_posterior\'\]

\# Create modified scenarios with increased probability

modified_scenarios = copy.deepcopy(scenarios)

new_p = min(1.0, original_p + delta_p)

modified_scenarios\[i\]\[\'p_posterior\'\] = new_p

\# Recalculate SSE

modified_result = calculate_sse_jpd(modified_scenarios, constraints,
base_ivps)

modified_e_ivps = modified_result\[\'e_ivps\'\]

\# Calculate sensitivity

delta_e_ivps = modified_e_ivps - baseline_e_ivps

actual_delta_p = new_p - original_p

sensitivity_ratio = delta_e_ivps / actual_delta_p if actual_delta_p \>
EPSILON else 0.0

sensitivities.append({

\'scenario_id\': scenario_id,

\'original_p\': original_p,

\'delta_p\': actual_delta_p,

\'delta_e_ivps\': delta_e_ivps,

\'sensitivity_ratio\': sensitivity_ratio,

\'interpretation\': f\"+{actual_delta_p\*100:.0f}% probability →
\${delta_e_ivps:+.2f} E\[IVPS\]\"

})

\# Sort by absolute impact

sensitivities.sort(key=lambda x: abs(x\[\'delta_e_ivps\'\]),
reverse=True)

return sensitivities

\#
==========================================================================================

\# 6. SCENARIO SUMMARY GENERATOR

\#
==========================================================================================

def generate_scenario_summary(sse_result, scenarios, base_ivps,
base_dr):

\"\"\"

Generates a comprehensive summary of the scenario analysis.

This function produces the core content for the
probabilistic_valuation_summary

section of A.10_SCENARIO_MODEL_OUTPUT.

Parameters:

\-\-\-\-\-\-\-\-\-\--

sse_result : dict

Output from calculate_sse_jpd()

scenarios : list

Scenario definitions

base_ivps : float

Base case IVPS

base_dr : float

Base case discount rate

Returns:

\-\-\-\-\-\-\--

dict : Summary suitable for A.10 artifact

\"\"\"

dist_stats = sse_result\[\'distribution_stats\'\]

\# Generate visualization

visualization = generate_distribution_visualization(dist_stats)

\# CVR State Bridge

delta = sse_result\[\'e_ivps\'\] - base_ivps

delta_percent = (delta / base_ivps \* 100) if base_ivps \> EPSILON else
0.0

\# Risk assessment

downside_prob = sum(

s\[\'p_final\'\] for s in sse_result\[\'states\'\]

if s\[\'feasibility_status\'\] == \'FEASIBLE\' and s\[\'ivps_final\'\]
\< base_ivps

)

upside_threshold = base_ivps \* 1.25 \# 25% above base

upside_prob = sum(

s\[\'p_final\'\] for s in sse_result\[\'states\'\]

if s\[\'feasibility_status\'\] == \'FEASIBLE\' and s\[\'ivps_final\'\]
\> upside_threshold

)

\# Count states with limited liability applied

ll_states = sum(

1 for s in sse_result\[\'states\'\]

if s.get(\'limited_liability_applied\', False)

)

return {

\'schema_version\': \'G3_2.2.1eS\',

\'primary_output\': {

\'e_ivps\': sse_result\[\'e_ivps\'\],

\'e_ivps_derivation\': f\"Sum of P(State) × IVPS(State) across
{sse_result\[\'feasible_state_count\'\]} feasible states\"

},

\'distribution_statistics\': {

\'median_p50\': dist_stats\[\'median_p50\'\],

\'p10\': dist_stats\[\'p10\'\],

\'p25\': dist_stats\[\'p25\'\],

\'p75\': dist_stats\[\'p75\'\],

\'p90\': dist_stats\[\'p90\'\],

\'min_ivps\': dist_stats\[\'min_ivps\'\],

\'max_ivps\': dist_stats\[\'max_ivps\'\],

\'range\': dist_stats\[\'range\'\],

\'standard_deviation\': dist_stats\[\'standard_deviation\'\],

\'coefficient_of_variation\': dist_stats\[\'coefficient_of_variation\'\]

},

\'distribution_shape\': {

\'skewness\': dist_stats\[\'skewness\'\],

\'modality\': dist_stats\[\'modality\'\]

},

\'distribution_visualization\': visualization,

\'cvr_state_bridge\': {

\'state_2_ivps_deterministic\': base_ivps,

\'state_3_e_ivps_probabilistic\': sse_result\[\'e_ivps\'\],

\'delta\': delta,

\'delta_percent\': delta_percent

},

\'risk_metrics\': {

\'downside_probability\': downside_prob,

\'upside_probability\': upside_prob,

\'limited_liability_states\': ll_states

},

\'sse_metadata\': {

\'total_states\': sse_result\[\'total_state_count\'\],

\'feasible_states\': sse_result\[\'feasible_state_count\'\],

\'renormalization_factor\': sse_result\[\'renormalization_factor\'\],

\'probability_sum_validation\':
sse_result\[\'probability_sum_validation\'\]

}

}

\#
==========================================================================================

\# 7. CONVENIENCE WRAPPER FOR FULL SCENARIO EXECUTION

\#
==========================================================================================

def execute_full_scenario_analysis(kg, dag, gim, dr_trace, base_ivps,
scenario_definitions, constraints):

\"\"\"

Convenience wrapper that executes the complete scenario analysis
pipeline.

This function:

1\. Executes each scenario intervention to get magnitude (M)

2\. Runs SSE integration to get JPD and E\[IVPS\]

3\. Calculates distribution statistics

4\. Generates summary for artifact construction

Parameters:

\-\-\-\-\-\-\-\-\-\--

kg : dict

A.2_ANALYTIC_KG artifact

dag : dict

A.3_CAUSAL_DAG artifact

gim : dict

A.5_GESTALT_IMPACT_MAP artifact

dr_trace : dict

A.6_DR_DERIVATION_TRACE artifact

base_ivps : float

Base case IVPS from State 2

scenario_definitions : list

List of scenario definitions:

\[

{

\'scenario_id\': \'S1\',

\'p_posterior\': 0.25,

\'intervention\': {

\'gim_overlay\': {\...},

\'structural_modifications\': \[\...\] (optional)

},

\'dr_override\': None (or float)

},

\...

\]

constraints : dict

SSE constraints (see calculate_sse_jpd)

Returns:

\-\-\-\-\-\-\--

dict : Complete analysis results for A.10 construction

\"\"\"

\# Extract base DR

try:

dr_data = dr_trace.get(\'derivation_trace\', dr_trace)

if isinstance(dr_data.get(\'DR_Static\'), dict):

base_dr = float(dr_data\[\'DR_Static\'\]\[\'value\'\])

else:

base_dr = float(dr_data.get(\'DR_Static\'))

except:

base_dr = 0.10 \# Fallback

\# Phase 1: Execute scenario interventions

scenario_results = \[\]

for scenario_def in scenario_definitions:

intervention_result = execute_scenario_intervention(

kg=kg,

dag=dag,

gim=gim,

dr_trace=dr_trace,

intervention_def=scenario_def.get(\'intervention\', {}),

dr_override=scenario_def.get(\'dr_override\')

)

ivps_impact = intervention_result\[\'ivps_scenario\'\] - base_ivps

scenario_results.append({

\'scenario_id\': scenario_def\[\'scenario_id\'\],

\'p_posterior\': scenario_def\[\'p_posterior\'\],

\'ivps_impact\': ivps_impact,

\'ivps_scenario\': intervention_result\[\'ivps_scenario\'\],

\'terminal_g\': intervention_result\[\'terminal_g\'\],

\'terminal_roic\': intervention_result\[\'terminal_roic\'\],

\'p2_status\': intervention_result\[\'p2_status\'\],

\'p2_message\': intervention_result\[\'p2_message\'\],

\'dr_used\': intervention_result\[\'dr_used\'\],

\'fundamentals_y1_intervened\':
intervention_result.get(\'fundamentals_y1_intervened\', {}) \# Patch 1.1

})

\# Phase 2: Execute SSE integration

sse_scenarios = \[

{

\'scenario_id\': s\[\'scenario_id\'\],

\'p_posterior\': s\[\'p_posterior\'\],

\'ivps_impact\': s\[\'ivps_impact\'\]

}

for s in scenario_results

\]

sse_result = calculate_sse_jpd(sse_scenarios, constraints, base_ivps)

\# Phase 3: Calculate probability sensitivities

prob_sensitivities = calculate_probability_sensitivity(sse_scenarios,
constraints, base_ivps)

\# Phase 4: Generate summary

summary = generate_scenario_summary(sse_result, sse_scenarios,
base_ivps, base_dr)

return {

\'scenario_results\': scenario_results,

\'sse_result\': sse_result,

\'probability_sensitivities\': prob_sensitivities,

\'summary\': summary

}

\#
==========================================================================================

\# END OF SCENARIO EXTENSION MODULE

\#
==========================================================================================
