G3 SCENARIO 2.2.2e: Probabilistic Causal Valuation

> **Version:** 2.2.3e (Atomized)
> **Change from 2.2.1e:** Split into 3 files for improved context management. Schemas in G3_SCENARIO_2.2.2e_SCHEMAS.md, normative definitions in G3_SCENARIO_2.2.2e_NORMDEFS.md. Kernel delivered as separate file CVR_KERNEL_SCEN_2.2.2e.py.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

I. MISSION AND OBJECTIVES

\* Mission: Execute the SCENARIO stage (G3_2.2.2eS) of the CAPY Pipeline
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
ENRICHMENT 2.2.2e:

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
addressing Mainline Catalysts (RQ Coverage Objective M-3a) and Tail Risk
Parameterization (RQ Coverage Objective M-3b), though the specific RQ
structure may vary.

\* The Verification Doctrine (Externalized Schemas): The required output
schema (A.10_SCENARIO_MODEL_OUTPUT) is provided in the attached G3_SCENARIO_2.2.2e_SCHEMAS.md. Normative
definitions are provided in G3_SCENARIO_2.2.2e_NORMDEFS.md. The output will be validated
against these external references.

\* The CVR Kernel Mandate (Computational Integrity P7): The CVR Kernel
(CVR_KERNEL_SCEN_2.2.2e.py) is the sole authorized execution engine for all
forecasting, valuation, and integration calculations.

1\. Loading & Execution (Two-Shot File Delivery):

\* Turn 1: CVR_KERNEL_SCEN_2.2.2e.py is attached for contextual understanding only (DSL modes, function signatures, node naming conventions). DO NOT execute kernel code in T1.

\* Turn 2: Load CVR_KERNEL_SCEN_2.2.2e.py directly into the execution environment. The kernel file can be imported or executed as a standard Python module.

\* Action: In T2, load the kernel and call functions directly (e.g., `from CVR_KERNEL_SCEN_2_2_2e import execute_scenario_intervention, calculate_sse_jpd`).

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

\* Turn 1: {TICKER}\_SCEN2.2.2eO_T1\_{YYYYMMDD}.md

\* Turn 2: {TICKER}\_SCEN2.2.2eO_T2\_{YYYYMMDD}.md

\* Kernel: CVR_KERNEL_SCEN_2.2.2e.py

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
litigation settlement, asset sale proceeds, acquisition costs, acquisition premiums) should be
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

  **DAG Equation Format (CRITICAL - Kernel Compatibility):**

  Any new or modified equations must be executable Python expressions:

  ✅ CORRECT formats:
  - `"GET('Node_A') + GET('Node_B')"` - arithmetic on nodes
  - `"GET('Units') * GET('Price_Per_Unit')"` - multiplication
  - `"PREV('Invested_Capital') * (1 + GET('Growth_Rate'))"` - lagged reference
  - `""` - empty string for exogenous drivers

  ❌ WRONG formats (kernel will FAIL):
  - `"f(x, y, z)"` - descriptive notation
  - `"Revenue = Units × Price"` - prose description
  - `"sum of components"` - natural language

  **Validation test:** Could Python's `eval()` execute this string with GET/PREV defined? If no, rewrite.

\* For Lump Sums: Use EXPLICIT_SCHEDULE on an FCF adjustment driver.

2\. Risk Alignment Assessment (P2):

\* Assess whether the scenario fundamentally alters systematic risk.

\* If yes, define dr_overlay and prepare rigorous justification.

\* If no (the typical case), DR remains static.

**T1 Emission: Scenario Execution Arguments**

Compile scenario definitions with probabilities and intervention specifications. Structure per T1 Output Schema (G3_SCENARIO_2.2.2e_SCHEMAS.md, Appendix A.1). Embed JSON in Turn 1 markdown output. Kernel code attached for contextual reference only — DO NOT EXECUTE.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**TURN 2: KERNEL EXECUTION**

Fresh context. Load kernel, parse T1 JSON, execute deterministically.

**T2 Initialization: Artifact Ingestion**

Re-ingest MRC State 2 artifacts from ENRICHMENT outputs (A.2_ANALYTIC_KG, A.3_CAUSAL_DAG, A.5_GESTALT_IMPACT_MAP, A.6_DR_DERIVATION_TRACE, A.7_LIGHTWEIGHT_VALUATION_SUMMARY). Parse Turn 1 Scenario Execution Arguments JSON. Load CVR_KERNEL_SCEN_2.2.2e.py into execution environment.

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

\* Compile A.10_SCENARIO_MODEL_OUTPUT per the schema (G3_SCENARIO_2.2.2e_SCHEMAS.md).

\* Validate completeness against schema requirements.

5\. Emission (MRC State 3):

\* Emit the single consolidated artifact: A.10_SCENARIO_MODEL_OUTPUT

\* MRC State 3 = MRC State 2 + A.10

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

V. OUTPUT MANDATE (Atomized Artifact Emission)

**CRITICAL: Atomized Output (Pattern 12)**

Each artifact MUST be written as an **individual file**. DO NOT embed JSON in markdown.

### T1 Required Outputs

| File | Content |
|------|---------|
| `{TICKER}_SCEN_EXECUTION_ARGS_SCEN.json` | Scenario definitions, probabilities, interventions (kernel input) |
| `{TICKER}_N6_SCENARIO_SCEN.md` | Scenario synthesis narrative |

### T2 Required Outputs

| File | Content |
|------|---------|
| `{TICKER}_A10_SCENARIO_SCEN.json` | Kernel output: SSE results, distribution, E[IVPS] |
| `{TICKER}_KERNEL_RECEIPT_SCEN.json` | Kernel execution proof (Pattern 13) |

### Kernel Receipt Schema (Pattern 13)

After kernel execution, write receipt:
```json
{
  "artifact_type": "KERNEL_EXECUTION_RECEIPT",
  "ticker": "{TICKER}",
  "stage": "SCEN",
  "timestamp": "{ISO8601}",
  "kernel": {"file": "CVR_KERNEL_SCEN_2_2_2e.py", "version": "G3_2.2.3e_SCEN"},
  "inputs": ["SCEN_EXECUTION_ARGS", "A2", "A3", "A5", "A6"],
  "outputs": ["A10_SCENARIO"],
  "exit_code": 0,
  "execution_time_seconds": null
}
```

### Anti-Patterns (DO NOT DO)

- Do NOT embed JSON in markdown
- Do NOT produce "unified emission" documents
- Do NOT return file contents to orchestrator (write to disk, return filepath only)

State Transition: Upon successful emission, the CVR transitions from MRC State 2 (deterministic) to MRC State 3 (probabilistic).
