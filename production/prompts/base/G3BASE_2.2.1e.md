# G3BASE 2.2.1e: Autonomous Causal Valuation 

# I. MISSION AND OBJECTIVES

-   **Mission:** Execute the BASE stage (G3_2.2.1e) of the CAPY Pipeline
    > for {Company Name} ({EXCHANGE:TICKER}) as of {DATE}.

-   **Primary Objective:** To produce a Minimal Reproducible CVR State
    > 1.

-   **Execution Paradigm:** Guided Autonomy. Prioritizes fidelity to
    > economic reality, analytical depth, epistemic grounding,
    > computational integrity, generative efficiency, run to run
    > reproducibility, and clear artifacts for state passing to
    > subsequent CVR stages.

## I.A EXECUTION PROTOCOL (Two-Shot Architecture)

### Turn Structure

This prompt governs a two-turn execution cycle. Each turn executes in a fresh Claude instance with clean context, maximizing reasoning depth through separation of concerns.

**Turn 1: Analytical Synthesis**

- **Trigger:** "Do Turn 1: {Company Name}, {EXCHANGE:TICKER}, {As of DATE}"
- **Attachments Required:** 
  - This prompt (G3BASE_2.2.1e.md)
  - Company Documents (filings, transcripts, supplementary materials)
  - CVR_KERNEL_2.2.1e.py (reference context only)
- **Scope:** Execute Phases A-D (Sections III-IV). Produce analytical narratives (I-IV) and artifacts A.1-A.6 that logically entail A.7.
- **Output:** Unified emission per Section V. Filename: `{TICKER}_BASE2.2.1eO_T1_{YYYYMMDD}.md`
- **Exclusion:** Do NOT compute A.7. Kernel is provided for semantic alignment only.

**Turn 2: Validation & Execution**

- **Trigger:** "Do Turn 2"
- **Attachments Required:**
  - This prompt (G3BASE_2.2.1e.md)
  - Turn 1 Output ({TICKER}_BASE2.2.1eO_T1_{YYYYMMDD}.md)
  - CVR_KERNEL_2.2.1e.py
- **Scope:** Validate Turn 1 artifacts for JSON integrity and internal consistency, repair if needed, execute kernel, produce A.7, emit unified report.
- **Output:** Complete MRC State 1 with executed A.7. Filename: `{TICKER}_BASE2.2.1eO_T2_{YYYYMMDD}.md`

### Variable Substitution

Placeholders {Company Name}, {EXCHANGE:TICKER}, {DATE} in Section I are populated from the Turn 1 trigger command. These propagate to all artifacts.

### Rationale

The two-shot architecture provides:

1. **Reasoning Depth:** Turn 1 focuses purely on analytical synthesis without computational overhead.
2. **Error Correction:** Turn 2 operates as a validation layer, catching JSON malformation, hallucinated values, and logical inconsistencies before kernel execution.
3. **Reproducibility:** Canonical prompt attachment eliminates runtime prompt variation.
4. **Clean Context:** Fresh instances prevent context pollution and attention degradation.

## II. EXECUTION ENVIRONMENT AND CONSTRAINTS

### A. Environmental Awareness and Tools

-   **Source Analysis:** Analyze all provided attachments (Company
    > Documents). If documents not provided, use search. You may
    > supplement knowledge gaps with search.

-   **The Verification Doctrine (Externalized Schemas):** The required
    > output schemas are provided in the attached Appendix.

-   **The CVR Kernel (Context Reference):** The CVR Kernel (Appendix C, also attached as CVR_KERNEL_2.2.1e.py) defines the computational logic that Turn 2 will execute. It is provided in Turn 1 for CONTEXTUAL UNDERSTANDING ONLY—to ensure your artifacts are semantically aligned with kernel expectations. Do NOT attempt to execute this code in Turn 1.

### B. Two-Shot Execution Architecture (Critical)

This prompt operates in TWO-SHOT EXECUTION mode with strict separation of concerns:

**TURN 1 RESPONSIBILITY (This Prompt, Analytical Instance):**

- Construct all analytical artifacts (A.1–A.6) with full epistemic rigor
- Emit artifacts as valid JSON in a single fenced code block
- Ensure structural compatibility with kernel requirements (see Appendix C)
- Do NOT execute kernel code or compute A.7

**TURN 2 RESPONSIBILITY (Fresh Instance, Validation & Execution):**

- Validate JSON integrity and repair malformation if present
- Verify internal consistency (DAG coverage, GIM-KG alignment, DR consistency)
- Execute kernel using validated artifacts as input
- Generate A.7 (LightweightValuationSummary)
- Emit unified MRC State 1 report

This architecture leverages Turn 1's strengths (deep reasoning, causal inference, synthesis) while Turn 2 provides a validation layer and deterministic computation. Once Turn 1 artifacts are finalized and validated, kernel execution is purely mechanical—all analytical intelligence is embedded in artifact construction.

## III. CORE ANALYTICAL DIRECTIVES

**P1. Analytical Autonomy and Depth (The Operational Primitive
Doctrine)**

**The Core Mandate:** Decompose financials into their Operational
Primitives---the

foundational, real-world independent variables that generate accounting
outputs.

GAAP line items are acceptable as atomic drivers only when irreducible
given

available data and stability constraints.

**The Physics Test:** For every material line item---whether revenue,
cost, or

capital---ask: \"What physical event or contractual interaction creates
this

number?\" Follow the physics of the specific business, not a canonical
template.

**Decomposition Boundaries:**

\* Data Availability: Only enforce decomposition if the required
time-series

data exists in the filings or can be rigorously inferred without
hallucination.

\* Stability Requirement: If the bridge between Operational Primitive
and

Financials requires unstable assumptions, default to the aggregate GAAP

driver and note the limitation.

\* Causal Distinctness: Limit decomposition to structures that isolate
distinct

causal drivers. Avoid non-causal segmentation that increases
computational

load without refining understanding of business physics.

**P1.5 The Accounting Translation Protocol (ATP)**

The DAG operates on economic reality, not accounting artifacts. Before
any

financial metric becomes a DAG node input, establish its Economic
Definition

by reconciling it to the underlying GAAP basis.

Complexity Assessment: At Phase A start, assess accounting complexity:

\* LOW: Straightforward GAAP, no material adjusted metrics, simple
capital

structure → Execute ATP-Lite.

\* MODERATE/HIGH: Adjusted metrics, complex revenue recognition,
significant

non-cash charges, M&A, or non-standard capital structure → Execute Full
ATP.

Default to MODERATE if uncertain. Document assessment in A.2 metadata.

Full ATP: Identify accounting areas material to this company where
reported

figures may diverge from economic reality. Common high-risk areas
include

adjusted metrics, SBC treatment, CapEx decomposition, D&A normalization,

working capital manipulation, one-time item classification, revenue
recognition

timing, and consolidation effects---but follow the accounting complexity
of the

specific business. Statistical outliers (e.g., ROIC \> 30%, margins
exceeding peer maximum, abnormal FCF conversion) should trigger
additional scrutiny---ask whether adjusting for true economic
consumption would normalize the outlier. For each material area,
reconcile the economic input to its GAAP basis and document in the
accounting_translation_log with source citations.

ATP-Lite: Confirm GAAP metrics are used directly, document basis for key

inputs, confirm SBC treatment and share count basis. State \"ATP-Lite
applied;

no material reconciliation issues identified\" in the translation log.

The Semantic Alignment Test: For each critical DAG input, ask: \"If I
traced

this number back to audited GAAP line items and footnotes, would the
math

produce the same result?\" If NO or UNCERTAIN, document the bridge or
flag

for conservative interpretation.

Degradation Protocol (Insufficient Data):

1\. Use the most conservative economic interpretation.

2\. Flag as \"Unreconciled --- Conservative Estimate.\"

3\. Apply wider sensitivity range (±50%) in GIM for affected drivers.

4\. Note data gap for ENRICHMENT-stage resolution.

The Anti-Shortcut Mandate: Do not assume a metric conforms to normative

definitions because of its label. Do not rely on management
reconciliation

tables without verifying completeness. Do not skip the Complexity
Assessment.

**P2. Epistemic Anchoring (The Bayesian Calibration Protocol)**

-   **The Grounding Mandate:** Assumptions must be built via a rigorous
    > Bayesian process: Prior (Industry Physics) + Likelihood (Company
    > Context) = Posterior (GIM Assumption).

-   **Step 1: The \"Cheap\" Prior (Internal Knowledge):**

> \* For every exogenous driver, first access your pre-training corpus
> (do not use Search here) to establish the \"Base Rate\" physics for
> this specific metric in this specific industry.
>
> \* Optimization: Do not generate a single point estimate. Instead,
> generate a Base Rate Distribution (e.g., \"SaaS churn typically ranges
> from 5% to 15%, centering on 10%\"). This mitigates the error of false
> precision.

-   Step 2: The Posterior Update (Contextual Tuning):

> \* Modify the Base Rate using the specific context of the target
> company (The Evidence).
>
> \* High Sensitivity Trigger: For drivers identified as
> high-sensitivity (high impact), you may use Search to validate
> specific historical precedence or first-principles constraints.

**P2.1. The Anti-Narrative Mandate:**

Exogenous driver assumptions must be justified independently. Do not
build

cross-correlations between drivers to make a cohesive \"story\" (e.g.,
lowering

Cost of Capital because Revenue Growth is high). Assume your output is
being

audited for statistical independence, not narrative coherence.

**P2.2. The Adversarial De-Framing Mandate:**

Distinguish between audited data and management narrative. Management

incentives favor perception optimization.

\* Metric Selection (\"Why This?\"): When management highlights non-GAAP
or

proprietary metrics, ask what standard metric it replaces and why they

would obscure it.

\* Denominator Scrutiny: For ratio claims, verify dimensional
consistency

(flow vs. stock, adjusted vs. gross).

\* Friction Inversion (\"Why Not?\"): For claims of uncaptured
opportunity,

ask why it hasn\'t happened yet. Identify structural friction (churn,

technical debt, regulatory ceilings) as the true forecast constraint.

## IV. EXECUTION PROTOCOL (The Workflow)

Execute the workflow per Phases A-D. Synthesize narratives internally
for unified emission.

**A. Synthesis, Knowledge Graph, Accounting Translation, and Anchoring
(Phase A)**

1\. Data Ingestion: Analyze attachments; supplement with search if
needed.

2\. ATP Execution: Execute Complexity Assessment and ATP per P1.5.
Populate

accounting_translation_log and Y0_data with ATP-reconciled values.

3\. Near-Term Anchors: Ingest Management Guidance and Wall Street
Consensus

(Y1-Y3). Classify as \"External Posteriors\"---inputs to the Bayesian
update,

not outputs. Do not allow consensus to contaminate Cheap Prior
generation.

Document status and reasoning in A.1.

4\. Investment Thesis Synthesis (Narrative #1): Business Model, Moat,

Management, Risks.

5\. ANALYTIC_KG Construction (A.2): Populate Y0_data with Operational

Primitives identified in P1. ERP static at 5.0%.

**B. Causal Modeling (SCM Inference)**

1\. SCM Inference: Infer the optimal SCM structure.

2\. Invested Capital Modeling (Narrative #2): Define IC methodology and
its

impact on ROIC interpretation.

3\. Artifact Construction (A.3): Generate the consolidated CAUSAL_DAG,

including structure and equations.

**C. Assumption Definition and Anchoring (Phases B & C)**

1\. Epistemic Anchor Protocol (Phase B: Long-Term Anchors): Establish
base

rates and first principles. Document in A.1.

2\. The Economic Governor Protocol (Narrative #3): Define long-term
constraints

(TAM, Mean Reversion). Ensure outlier metrics have been scrutinized per
ATP

and that long-term assumptions distinguish between Structural Power and

Accounting/Cyclical Artifacts, converging to underlying Economic
Reality.

Reconcile with Base Rates (P2).

3\. GESTALT_IMPACT_MAP Construction (Phase C): Define 20-year
assumptions

(A.5). GIM justifications must trace the causal chain per P2. Provide

explicit Variance Justification if deviating from Anchors (A.1).

**D.Finalization and Anchoring (Phase D)**

1\. Discount Rate (DR) Derivation:

\* Calculate the Static DR.

\* DR Justification (Narrative #4): Justify the Risk Multiplier (X).

\* Artifact Construction: Prepare DR_DERIVATION_TRACE (A.6).

2\. Artifact Finalization (Pre-Emission Validation):

Before emission, validate internal consistency across artifacts:

\* DAG Coverage: Every node in A.3 (CAUSAL_DAG) with a non-empty
equation

must reference only nodes that exist in A.3. Every Exogenous_Driver in
A.3

must have a corresponding entry in A.5 (GIM).

\* KG-DAG Alignment: All Exogenous_Drivers using CAGR_INTERP mode in A.5
must

have a Y0 value in A.2 (core_data.Y0_data).

\* DR Consistency: A.6 (DR_DERIVATION_TRACE) must use RFR and ERP values
from

A.2 (market_context).

\* Sensitivity Candidates: Identify 3-5 highest-sensitivity exogenous
drivers

(those with largest expected impact on valuation). Note these in A.5
metadata

or Narrative #4 for downstream sensitivity configuration.

**Turn 1 Terminus:** Upon completing pre-emission validation, emit the unified output per Section V. This concludes Turn 1. Turn 2 will perform secondary validation, execute the kernel, and produce the final unified report inclusive of A.7.

**V. OUTPUT MANDATE (The Unified MRC State Vector)**

*This section governs Turn 1 output. Turn 2 output encompasses this structure plus executed A.7 and any validation notes.*

Emit the complete MRC State 1 in a single, unified block. Structure:
Narratives

followed immediately by JSON artifacts.

\[START OF UNIFIED EMISSION\]

Analytical Narratives (I-IV)

(Emit Narratives 1-4 with clear section headings.)

MRC State 1 Artifacts (A.1-A.6)

(Emit JSON object containing 5 artifacts, strictly adhering to Appendix
A.)

{

\"A.1_EPISTEMIC_ANCHORS\": {\...},

\"A.2_ANALYTIC_KG\": {

\"metadata\": {\"atp_complexity_assessment\": \"\...\", \"atp_mode\":
\"\...\"},

\"core_data\": {\...},

\"accounting_translation_log\": {\...},

\"market_context\": {\...},

\"share_data\": {\...}

},

\"A.3_CAUSAL_DAG\": {

\"DAG\": {\...},

\"coverage_manifest\": {\...}

},

\"A.5_GESTALT_IMPACT_MAP\": {\...},

\"A.6_DR_DERIVATION_TRACE\": {\...},

}

**---\-\-\-\-\-\-\-\-\-\-\-\--**

**APPENDIX A:** CVR_SCHEMAS_G3_2.2.1e.json

{

\"version_control\": {

\"paradigm\": \"G3 Meta-Prompting Doctrine v2.4 (Two-Shot Guided Autonomy)\",

\"pipeline_stage\": \"BASE G3_2.2.1e\",

\"date\": \"2025-12-07\"

},

\"normative_definitions\": {

\"1.1_financial_definitions_and_formulas\": {

\"EBIT\": \"MUST include Stock-Based Compensation (SBC) expense.\",

\"NOPAT\": \"EBIT \* (1 - Tax Rate).\",

\"ROIC\": \"NOPAT / Invested Capital.\",

\"FCF_Unlevered\": \"NOPAT - Reinvestment.\",

\"Growth_g\": \"ROIC \* Reinvestment Rate.\",

\"Timing_Convention_Mandate_DAG_Compliance\": \"Calculations dependent
on prior period balances MUST use the Beginning-of-Period (BOP) value
(i.e., the PREV() function). Mandatory for ROIC
(PREV(Invested_Capital)).\",

\"ATP_Mandate\": \"All financial inputs to the DAG must be reconciled to
their economic definition per P1.5. The accounting_translation_log in
A.2 documents this reconciliation. Raw reported figures that deviate
from normative definitions (e.g., Adj. EBITDA excluding SBC) must be
adjusted before becoming DAG inputs.\",

\"Valuation_Methodology_APV\": \"Adjusted Present Value (APV) approach
is mandated. 20-Year Explicit Forecast. Static DR is used.\"

},

\"1.2_assumption_dsl_definitions\": {

\"description\": \"The DSL defines how an assumption evolves from Year 1
(Y1) to Year 20 (Y20). (Definitions for STATIC, LINEAR_FADE,
CAGR_INTERP, S_CURVE, EXPLICIT_SCHEDULE remain unchanged)\"

},

\"1.3_dr_derivation_methodology\": {

\"DR_Static\": \"RFR + (ERP \* X). X (Risk Multiplier) is a qualitative
assessment (0.5 to 2.2).\"

}

},

\"schemas\": {

\"A.1_EPISTEMIC_ANCHORS\": {

\"schema_version\": \"G3_2.2.1e\",

\"description\": \"Documents the Bayesian Priors established in Phases A
and B.\",

\"near_term_anchors\": \"object (Guidance and Consensus)\",

\"long_term_anchors\": \"object (Mandatory Numeric Base Rate
Distributions: Must include {p10: float, p50: float, p90: float} for
every exogenous driver)\"

},

\"A.2_ANALYTIC_KG\": {

\"schema_version\": \"G3_2.2.1e\",

\"metadata\": {

\"atp_complexity_assessment\": \"string (LOW / MODERATE / HIGH)\",

\"atp_mode\": \"string (ATP-Lite / Full ATP)\"

},

\"core_data\": {

\"\_\_COMMENT\_\_\": \"CRITICAL: Must use the nested \'Y0_data\' key for
the Kernel to read history.\",

\"Y0_data\": \"object (Key-Value pairs of Y0 financials, e.g.,
{\'Revenue\': 100.0, \'EBIT\': 20.0})\",

\"TSM_data\": \"object (Trailing Twelve Month data)\"

},

\"accounting_translation_log\": {

\"\_\_COMMENT\_\_\": \"Documents the reconciliation of reported figures
to economic definitions per ATP (P1.5).\",

\"schema\": {

\"metric_name\": {

\"source_metric\": \"string (The metric as reported/labeled in source
documents)\",

\"source_reference\": \"string (Document and page/note reference)\",

\"adjustments_applied\": \[\"array of strings describing each adjustment
made\"\],

\"normative_alignment\": \"string (Confirms alignment with Section 1.1
definitions or documents deviation)\",

\"confidence\": \"string (High / Medium / Low)\",

\"flags\": \[\"array of strings for any issues requiring downstream
attention\"\]

}

},

\"required_entries\": \[\"EBIT\", \"CapEx\", \"D&A\", \"SBC_Treatment\",
\"Share_Count_Basis\"\],

\"optional_entries\": \[\"Working_Capital\", \"Revenue_Recognition\",
\"One_Time_Items\", \"Consolidation\"\]

},

\"market_context\": {

\"Current_Stock_Price\": \"float (REQUIRED for Implied Multiples)\",

\"RFR\": \"float\",

\"ERP\": \"float\",

\"Other_Context\": \"object\"

},

\"share_data\": \"object (FDSO, Share Count details)\"

},

\"A.3_CAUSAL_DAG\": {

\"schema_version\": \"G3_2.2.1e\",

\"description\": \"The unified DAG defining structure, dependencies, and
equations. (Consolidated A.3 structure and A.4 equations)\",

\"DAG\": {

\"\_\_COMMENT\_\_\": \"Dictionary where keys are Node Names.\",

\"Node_Definition\": {

\"type\": \"Exogenous_Driver / Endogenous_Driver /
Financial_Line_Item\",

\"parents\": \[\"list of strings (Explicit dependencies, primarily for
documentation)\"\],

\"equation\": \"string (Python-executable equation. MUST use
PREV(\'Var\') for lagged access and GET(\'Var\') for intra-timestep
access.)\"

}

}

},

\"A.5_GESTALT_IMPACT_MAP\": {

\"schema_version\": \"G3_2.2.1e\",

\"description\": \"The map of exogenous driver assumptions and their
justifications.\",

\"GIM\": {

\"\_\_COMMENT\_\_\": \"Dictionary where keys are Driver Handles (must
align with A.3).\",

\"Driver_Definition\": {

\"mode\": \"string (DSL Mode: STATIC, LINEAR_FADE, CAGR_INTERP, etc.)\",

\"params\": \"object (DSL Parameters)\",

\"qualitative_thesis\": \"string (Causal Chain Justification. MUST
include \'Variance Justification\' with percentile rankings if deviating
from A.1.)\"

}

}

},

\"A.6_DR_DERIVATION_TRACE\": {

\"schema_version\": \"G3_2.2.1e\",

\"derivation_trace\": {

\"RFR\": \"float\",

\"ERP\": \"float\",

\"X_Risk_Multiplier\": \"float\",

\"DR_Static\": \"float\"

},

\"justification\": \"string (See Mandatory Narrative #4. Justify the
Risk Multiplier X based on qualitative assessment.)\"

},

\"A.7_LIGHTWEIGHT_VALUATION_SUMMARY\": {

\"\_\_GENERATION_NOTE\_\_\": \"DOWNSTREAM-GENERATED. This artifact is
produced by kernel execution in Colab, not by G3+DT. Schema included for
reference.\",

\"schema_version\": \"G3_2.2.1e\",

\"description\": \"The Selective Emission output from kernel
execution.\",

\"ivps_summary\": {

\"IVPS\": \"float\",

\"DR\": \"float\",

\"Terminal_g\": \"float\",

\"ROIC_Terminal\": \"float\",

\"Current_Market_Price\": \"float or null\"

},

\"implied_multiples_analysis\": {

\"Implied_EV_Sales_Y1\": \"float\",

\"Implied_EV_EBIT_Y1\": \"float\",

\"Implied_P_NOPAT_Y1\": \"float\",

\"Market_EV_Sales_Y1\": \"float\",

\"Market_EV_EBIT_Y1\": \"float\",

\"Market_P_NOPAT_Y1\": \"float\"

},

\"sensitivity_analysis\": {

\"tornado_summary\": \[{

\"Driver_Handle\": \"string\",

\"IVPS_Low\": \"float\",

\"IVPS_High\": \"float\",

\"IVPS_Swing_Percent\": \"float\"

}\]

},

\"key_forecast_metrics\": {

\"Revenue_CAGR_Y1_Y5\": \"float\",

\"EBIT_Margin_Y5\": \"float\",

\"ROIC_Y5\": \"float\"

},

\"terminal_drivers\": \"object\",

\"forecast_trajectory_checkpoints\": {

\"\_\_COMMENT\_\_\": \"Nominal values of key drivers (Exogenous and
Endogenous) at specific checkpoints for auditability.\",

\"Y0\": \"object\",

\"Y5\": \"object\",

\"Y10\": \"object\",

\"Y20\": \"object\"

}

}

}

}

---\-\-\-\-\-\-\-\--

B.1. Assumption DSL Definitions (Strict Kernel Compliance)

The Kernel supports ONLY the following four propagation modes. Usage of
unsupported modes (e.g., S_CURVE) will result in a critical execution
failure.

-   **STATIC**

    -   *Behavior:* The value remains constant from Y1 through Y20.

    -   *Required Param:* value (float).

-   **LINEAR_FADE**

    -   *Behavior:* Linearly interpolates from start_value to end_value
        > over fade_years. Holds end_value thereafter.

    -   *Required Params:* start_value (float), end_value (float),
        > fade_years (int).

-   **CAGR_INTERP**

    -   *Behavior:* Compounds the Y0 value (found in core_data) by a
        > growth rate that interpolates from start_cagr to end_cagr over
        > interp_years.

    -   *Required Params:* start_cagr (float), end_cagr (float),
        > interp_years (int).

-   **EXPLICIT_SCHEDULE**

    -   *Behavior:* Manually overrides specific years using a dictionary
        > mapping.

    -   *Required Params:* schedule (Dictionary: {\'1\': val, \'2\':
        > val\...}).

    -   *Note:* Gaps are interpolated. Years after the schedule ends
        > hold the last value.

B.2. Execution Topology (DAG compliance)

The CVR Kernel executes the SCM using a topological sort. The following
rules apply to the equations in A.3_CAUSAL_DAG:

-   **The PREV() Rule (Inter-Temporal):** To access a variable from the
    > previous year (\$t-1\$), use PREV(\'Variable_Name\').

    -   *Mandatory:* All \"Stock\" variable updates (e.g., Invested
        > Capital accumulation) must use PREV.

-   **The GET() Rule (Intra-Temporal):** To access a variable from the
    > current year (\$t\$) that has already been calculated, use
    > GET(\'Variable_Name\').

    -   *Cycle Warning:* Intra-temporal dependencies must be acyclic.
        > (e.g., A cannot rely on B if B relies on A in the same
        > timestep).

B.3. Valuation Engine & Equity Bridge

The Kernel executes a simplified Adjusted Present Value (APV)
calculation.

-   **Discount Rate (DR):** \$RFR + (ERP \\times X)\$.

    -   *X (Risk Multiplier):* A qualitative assessment (0.5 to 2.2)
        > derived from the Analysis narratives.

-   **Explicit Period Value:** The sum of discounted Unlevered FCF for
    > Y1--Y20.

-   **Terminal Value (TV):** Calculated using the Value Driver Formula.

    -   \$TV = \\frac{NOPAT\_{Y21} \\times (1 - \\frac{g}{r})}{DR - g}\$

    -   *Where:* \$r\$ = Terminal ROIC (converges to Y20 ROIC), \$g\$ =
        > Terminal Growth (capped at RFR).

-   **The Equity Bridge (Y0 Static):**

    -   \$EnterpriseValue = PV(Explicit\\\_FCF) + PV(TV)\$

    -   \$EquityValue = EnterpriseValue - TotalDebt\_{Y0} +
        > ExcessCash\_{Y0} - MinorityInterest\_{Y0}\$

    -   *Note:* The Kernel uses **Static Y0 Balance Sheet** items for
        > the bridge. It does *not* model dynamic debt paydown or
        > interest tax shields.

---\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

**APPENDIX C: CVR Kernel (Reference Context)**

The kernel code below is provided for CONTEXTUAL UNDERSTANDING. It
defines

the computational logic that consumes artifacts A.1--A.6 and produces
A.7.

Do NOT execute this code---review it to ensure your artifacts are
semantically

aligned with kernel expectations (node naming, DSL modes, equation
syntax).

import numpy as np

import pandas as pd

import json

import math

from collections import deque, defaultdict

import re

import copy

import datetime

import logging

\#
==========================================================================================

\# CVR KERNEL (G3_2.2.1 Implementation - MRC Paradigm / Integrity
Update)

\#
==========================================================================================

\# Configuration

FORECAST_YEARS = 20

EPSILON = 1e-9

KERNEL_VERSION = \"G3_2.2.1e\"

SENSITIVITY_TORNADO_TOP_N = 5

TERMINAL_G_RFR_CAP = True \# If True, Terminal g is capped at RFR

\# Configure Logging (Minimal logging for production)

logging.basicConfig(level=logging.WARNING, format=\'%(levelname)s -
%(message)s\')

logger = logging.getLogger(\_\_name\_\_)

\#
==========================================================================================

\# 1. CORE ENGINES (DSL, SCM, APV)

\#
==========================================================================================

\# 1.1 Assumption DSL (Domain Specific Language) Engine

def apply_dsl(dsl, y0_value=None, forecast_years=FORECAST_YEARS):

\"\"\"Applies the DSL definition to generate a forecast array.\"\"\"

mode = dsl.get(\'mode\')

params = dsl.get(\'params\', {})

forecast = np.zeros(forecast_years)

if mode == \'STATIC\':

value = float(params.get(\'value\', 0))

forecast.fill(value)

elif mode == \'LINEAR_FADE\':

start_value = float(params.get(\'start_value\'))

end_value = float(params.get(\'end_value\'))

fade_years = int(params.get(\'fade_years\'))

if fade_years \> forecast_years:

fade_years = forecast_years

if fade_years \> 0:

fade_steps = np.linspace(start_value, end_value, fade_years)

forecast\[:fade_years\] = fade_steps

if fade_years \< forecast_years:

forecast\[fade_years:\] = end_value

elif mode == \'CAGR_INTERP\':

if y0_value is None:

raise ValueError(\"CAGR_INTERP requires a valid y0_value.\")

start_cagr = float(params.get(\'start_cagr\'))

end_cagr = float(params.get(\'end_cagr\'))

interp_years = int(params.get(\'interp_years\'))

if interp_years \> forecast_years:

interp_years = forecast_years

\# 1. Generate the CAGR time series

cagr_series = np.zeros(forecast_years)

if interp_years \> 0:

cagr_steps = np.linspace(start_cagr, end_cagr, interp_years)

cagr_series\[:interp_years\] = cagr_steps

if interp_years \< forecast_years:

cagr_series\[interp_years:\] = end_cagr

\# 2. Apply the CAGR series to the base value

current_value = y0_value

for i in range(forecast_years):

current_value \*= (1 + cagr_series\[i\])

forecast\[i\] = current_value

elif mode == \'EXPLICIT_SCHEDULE\':

\# (Implementation for EXPLICIT_SCHEDULE)

schedule = params.get(\'schedule\', {})

sorted_years = sorted(\[int(y) for y in schedule.keys()\])

if not sorted_years:

return forecast

start_year = sorted_years\[0\]

start_value = float(schedule\[str(start_year)\])

if start_year \> 1:

forecast\[:start_year-1\] = start_value

for i in range(len(sorted_years)):

year = sorted_years\[i\]

value = float(schedule\[str(year)\])

idx = year - 1

if idx \< forecast_years:

forecast\[idx\] = value

if i + 1 \< len(sorted_years):

next_year = sorted_years\[i+1\]

next_value = float(schedule\[str(next_year)\])

next_idx = next_year - 1

if next_year \> year + 1:

gap_years = next_year - year

interp_steps = np.linspace(value, next_value, gap_years + 1)

start_fill_idx = idx + 1

end_fill_idx = next_idx

if end_fill_idx \<= forecast_years:

forecast\[start_fill_idx:end_fill_idx\] = interp_steps\[1:-1\]

elif start_fill_idx \< forecast_years:

fill_len = forecast_years - start_fill_idx

forecast\[start_fill_idx:\] = interp_steps\[1:1+fill_len\]

last_defined_year = sorted_years\[-1\]

if last_defined_year \< forecast_years:

last_value = float(schedule\[str(last_defined_year)\])

forecast\[last_defined_year-1:\] = last_value

else:

raise ValueError(f\"Unknown DSL mode: {mode}\")

return forecast

\# 1.2 SCM (Structural Causal Model) Engine

def topological_sort(dag):

\"\"\"

Performs a topological sort on the DAG.

(G3_1.8 Hardening): Ensures only intra-timestep dependencies (GET calls)
are considered.

\"\"\"

in_degree = defaultdict(int)

graph = defaultdict(list)

nodes = set(dag.keys())

\# Regex to find GET(\'NodeName\') calls (intra-timestep dependencies)

get_regex = re.compile(r\"GET\\(\[\'\\\"\](.\*?)\[\'\\\"\]\\)\")

for node, definition in dag.items():

\# 1. Explicit dependencies from \'parents\' list

parents = definition.get(\'parents\', \[\])

for parent in parents:

if parent in nodes and parent != node:

if node not in graph\[parent\]:

graph\[parent\].append(node)

in_degree\[node\] += 1

\# 2. Implicit dependencies from \'equation\' string (GET calls)

equation = definition.get(\'equation\', \'\')

if equation:

matches = get_regex.findall(equation)

for dependency in matches:

if dependency in nodes and dependency != node:

\# Check if this dependency is already accounted for

if node not in graph\[dependency\]:

graph\[dependency\].append(node)

in_degree\[node\] += 1

\# 3. Perform the sort (Kahn\'s algorithm)

queue = deque(\[node for node in nodes if in_degree\[node\] == 0\])

sorted_list = \[\]

while queue:

node = queue.popleft()

sorted_list.append(node)

for neighbor in graph\[node\]:

in_degree\[neighbor\] -= 1

if in_degree\[neighbor\] == 0:

queue.append(neighbor)

if len(sorted_list) != len(nodes):

cycle_nodes = \[node for node in nodes if in_degree\[node\] \> 0\]

raise RuntimeError(f\"A cycle was detected in the DAG. Check nodes for
circular dependencies (must use PREV for lagged dependencies):
{cycle_nodes}\")

return sorted_list

def prepare_inputs(kg, gim):

\"\"\"Prepares inputs by applying the DSL to generate forecast arrays
for exogenous drivers.\"\"\"

inputs = {}

y0_data = kg.get(\'core_data\', {}).get(\'Y0_data\', {})

for handle, definition in gim.items():

y0_value = y0_data.get(handle)

if definition\[\'mode\'\] == \'CAGR_INTERP\' and y0_value is None:

logger.error(f\"Missing Y0 data for handle \'{handle}\' required by
CAGR_INTERP.\")

raise ValueError(f\"Missing Y0 data for handle \'{handle}\' in
ANALYTIC_KG.\")

try:

forecast_array = apply_dsl(definition, y0_value=y0_value)

inputs\[handle\] = forecast_array

except Exception as e:

logger.error(f\"Error applying DSL for handle \'{handle}\': {e}\")

raise RuntimeError(f\"Failed to process GIM assumption for {handle}.
Error: {e}\") from e

return inputs

def execute_scm(kg, dag, seq, gim):

\"\"\"Executes the SCM forecast over the forecast horizon.\"\"\"

\# 1. Initialize Data Structures

y0_data = kg.get(\'core_data\', {}).get(\'Y0_data\', {})

\# \'history\' stores the full time series data (Y0 + Y1\...Y20)

history = defaultdict(lambda: np.zeros(FORECAST_YEARS + 1))

\# Load Y0 data (at index 0)

for handle, value in y0_data.items():

if handle in dag:

try:

history\[handle\]\[0\] = float(value)

except (TypeError, ValueError):

history\[handle\]\[0\] = 0.0

\# 2. Prepare Exogenous Inputs (Apply DSL)

try:

exogenous_inputs = prepare_inputs(kg, gim)

except Exception as e:

logger.error(f\"Failed to prepare exogenous inputs: {e}\")

raise

\# Load exogenous inputs (Y1\...Y20)

for handle, forecast_array in exogenous_inputs.items():

if handle in dag:

history\[handle\]\[1:\] = forecast_array

\# 3. Define Helper Functions (PREV, GET) for use in equations

\# (G3_1.8 Hardening): Robust handling of data access and error
conditions.

def GET(handle, t):

if handle not in history:

raise NameError(f\"Handle \'{handle}\' not found during SCM execution
(GET).\")

return history\[handle\]\[t\]

def PREV(handle, t):

if t \<= 0:

raise IndexError(f\"Cannot access data before Y0 for handle \'{handle}\'
(PREV at t=0). Check ANALYTIC_KG Y0 data.\")

if handle not in history:

raise NameError(f\"Handle \'{handle}\' not found during SCM execution
(PREV).\")

return history\[handle\]\[t-1\]

\# 4. Execute the Forecast (Time-Step Iteration)

for t in range(1, FORECAST_YEARS + 1):

\# t represents the current year (Y1 to Y20)

for handle in seq:

definition = dag\[handle\]

equation_str = definition.get(\'equation\')

if not equation_str:

\# Node is exogenous or static, already populated.

continue

\# Execute the equation

try:

\# Prepare the execution environment

exec_env = {

\'GET\': lambda h: GET(h, t),

\'PREV\': lambda h: PREV(h, t),

\'max\': max, \'min\': min, \'math\': math, \'np\': np

}

\# Execute the equation string

result = eval(equation_str, exec_env)

\# Store the result

history\[handle\]\[t\] = float(result)

except Exception as e:

logger.error(f\"SCM Execution Error at t={t} for handle \'{handle}\'.
Equation: \'{equation_str}\'. Error: {e}\")

raise RuntimeError(f\"Failed to execute equation for {handle} at year
{t}. Error: {e}\") from e

\# 5. Format Output as DataFrame

\# Return the forecast period (Y1\...Y20)

forecast_data = {handle: data\[1:\] for handle, data in history.items()
if handle in seq}

index = \[f\"Y{i+1}\" for i in range(FORECAST_YEARS)\]

df = pd.DataFrame(forecast_data, index=index)

\# Ensure columns are in the topologically sorted order

ordered_cols = \[col for col in seq if col in df.columns\]

df = df\[ordered_cols\]

return df

\# 1.5 APV (Adjusted Present Value) Valuation Engine

def calculate_apv(forecast_df, dr, kg):

\"\"\"Calculates the Intrinsic Value Per Share (IVPS) using the APV
methodology.\"\"\"

\# 1. Extract Required Data

if \'FCF_Unlevered\' not in forecast_df.columns or \'ROIC\' not in
forecast_df.columns or \'NOPAT\' not in forecast_df.columns:

raise ValueError(\"Forecast DataFrame must contain \'FCF_Unlevered\',
\'ROIC\', and \'NOPAT\'.\")

fcf = forecast_df\[\'FCF_Unlevered\'\].values

nopat_T = forecast_df\[\'NOPAT\'\].iloc\[-1\]

market_context = kg.get(\'market_context\', {})

share_data = kg.get(\'share_data\', {})

core_data = kg.get(\'core_data\', {}).get(\'Y0_data\', {})

rfr = market_context.get(\'RFR\')

fdso = share_data.get(\'FDSO\')

total_debt_y0 = core_data.get(\'Total_Debt\', 0.0)

excess_cash_y0 = core_data.get(\'Excess_Cash\', 0.0)

minority_interest_y0 = core_data.get(\'Minority_Interest\', 0.0)

if fdso is None or fdso \<= 0:

raise ValueError(\"FDSO must be provided and positive in ANALYTIC_KG.\")

\# 2. Calculate PV of Explicit FCF

discount_factors = np.array(\[(1 + dr)\*\*-(i+1) for i in
range(FORECAST_YEARS)\])

pv_fcf = np.sum(fcf \* discount_factors)

\# 3. Determine Terminal Growth (g) and Terminal ROIC (r)

\# We use the Value Driver Formula: TV = NOPAT(T+1) \* (1 - g/r) / (DR -
g)

\# Terminal ROIC (r): We use the ROIC at Y20, assuming the GIM already
models the convergence.

roic_T = forecast_df\[\'ROIC\'\].iloc\[-1\]

terminal_roic_r = roic_T

\# Terminal Growth (g): Estimated based on NOPAT growth convergence,
subject to constraints.

nopat_growth_rates = forecast_df\[\'NOPAT\'\].pct_change().values\[1:\]

\# Use the average growth of the last 3 years to smooth volatility

terminal_g_estimate = np.mean(nopat_growth_rates\[-3:\])

terminal_g = terminal_g_estimate

\# Apply Constraints to Terminal Growth

if TERMINAL_G_RFR_CAP and rfr is not None:

if terminal_g \> rfr:

logger.info(f\"Capping terminal growth ({terminal_g:.4f}) at RFR
({rfr:.4f}).\")

terminal_g = rfr

if terminal_g \>= dr:

logger.warning(f\"Terminal growth ({terminal_g:.4f}) exceeds DR
({dr:.4f}). Adjusting g to 99% of DR.\")

terminal_g = dr \* 0.99

if terminal_g \< 0:

terminal_g = 0

\# 4. Calculate Terminal Value (TV)

nopat_T_plus_1 = nopat_T \* (1 + terminal_g)

\# Calculate Reinvestment Rate (IR) = g / r

if abs(terminal_roic_r) \> EPSILON:

reinvestment_rate_terminal = terminal_g / terminal_roic_r

else:

reinvestment_rate_terminal = 0

\# Apply constraints to Reinvestment Rate

if reinvestment_rate_terminal \< 0:

logger.warning(f\"Terminal Reinvestment Rate is negative. Assuming
rationalization (g=0).\")

terminal_g = 0

reinvestment_rate_terminal = 0

nopat_T_plus_1 = nopat_T

\# Value Driver Formula

numerator = nopat_T_plus_1 \* (1 - reinvestment_rate_terminal)

denominator = dr - terminal_g

if denominator \<= 0: \# Should be caught by constraints, but as a
safeguard

raise RuntimeError(\"APV denominator (DR - g) is non-positive.\")

terminal_value = numerator / denominator

\# 5. Calculate PV of Terminal Value

pv_terminal_value = terminal_value / ((1 + dr)\*\*FORECAST_YEARS)

\# 6. Calculate Enterprise Value (EV)

enterprise_value = pv_fcf + pv_terminal_value

\# 7. Calculate Equity Value

equity_value = enterprise_value - total_debt_y0 + excess_cash_y0 -
minority_interest_y0

\# 8. Calculate Intrinsic Value Per Share (IVPS)

ivps = equity_value / fdso

\# 9. Package Results

results = {

\"IVPS\": ivps,

\"Equity_Value\": equity_value,

\"Enterprise_Value\": enterprise_value,

\"DR\": dr,

\"Terminal_g\": terminal_g,

\"Terminal_ROIC_r\": terminal_roic_r,

\"FDSO\": fdso,

\"Net_Debt\": total_debt_y0 - excess_cash_y0

}

return results

\#
==========================================================================================

\# 2. INTERNAL ARTIFACT GENERATORS (Helpers)

\#
==========================================================================================

def validate_dag_coverage(kg, dag_artifact):

\"\"\"

Validates that all nodes in the DAG which are present in Y0_data have
corresponding entries

in the \`coverage_manifest\`

Also checks that nodes explicitly listed in \`coverage_manifest\` exist
in the DAG.

\"\"\"

y0_data = kg.get(\'core_data\', {}).get(\'Y0_data\', {})

dag_nodes = set(dag_artifact.get(\'DAG\', {}).keys())

coverage_manifest = dag_artifact.get(\'coverage_manifest\', {})

\# 1. Check DAG nodes against Y0_data for coverage manifest entry

missing_coverage = \[\]

for node in dag_nodes:

if node in y0_data and node not in coverage_manifest:

missing_coverage.append(node)

if missing_coverage:

raise RuntimeError(

f\"DAG Coverage Warning: The following DAG nodes are present in Y0_data
\"

f\"but lack an explicit entry in \`coverage_manifest\`: {\',
\'.join(missing_coverage)}\"

)

\# 2. Check coverage manifest entries against actual DAG nodes

invalid_coverage_entries = \[\]

for covered_node in coverage_manifest.keys():

if covered_node not in dag_nodes:

invalid_coverage_entries.append(covered_node)

if invalid_coverage_entries:

logger.warning(

f\"DAG Coverage Warning: The \`coverage_manifest\` lists entries for
nodes \...\"

f\"that do not exist in the DAG: {\',
\'.join(invalid_coverage_entries)}\"

)

def generate_forecast_summary(forecast_df,
schema_version=KERNEL_VERSION):

\"\"\"Generates a summary of the forecast for internal analysis.\"\"\"

summary_data = {}

key_items = \[\'Revenue\', \'EBIT\', \'NOPAT\', \'ROIC\'\]

for item in key_items:

if item in forecast_df.columns:

summary_data\[item\] = forecast_df\[item\].to_dict()

if \'Revenue\' in forecast_df.columns and \'EBIT\' in
forecast_df.columns:

summary_data\[\'EBIT_Margin\'\] = (forecast_df\[\'EBIT\'\] /
forecast_df\[\'Revenue\'\]).to_dict()

return {\"schema_version\": schema_version, \"summary_data\":
summary_data}

\#
==========================================================================================

\# 3. ANALYSIS MODULES (Multiples, Sensitivity)

\#
==========================================================================================

def calculate_implied_multiples(valuation_results, forecast_summary, kg,
schema_version=KERNEL_VERSION):

\"\"\"Calculates implied valuation multiples based on the IVPS and
market price.\"\"\"

ivps = valuation_results\[\'IVPS\'\]

ev_implied = valuation_results\[\'Enterprise_Value\'\]

fdso = valuation_results\[\'FDSO\'\]

net_debt = valuation_results\[\'Net_Debt\'\]

current_price = kg.get(\'market_context\',
{}).get(\'Current_Stock_Price\')

ev_market = None

if current_price is not None:

market_cap = current_price \* fdso

ev_market = market_cap + net_debt

fs = forecast_summary.get(\'summary_data\', {})

implied_multiples = {}

\# Focus on Y1 multiples for the summary

year = \'Y1\'

def calculate(num_implied, num_market, den_data, handle):

if den_data and abs(den_data.get(year, 0)) \> EPSILON:

implied_multiples\[f\"Implied\_{handle}\_{year}\"\] = num_implied /
den_data\[year\]

if num_market is not None:

implied_multiples\[f\"Market\_{handle}\_{year}\"\] = num_market /
den_data\[year\]

calculate(ev_implied, ev_market, fs.get(\'Revenue\'), \'EV_Sales\')

calculate(ev_implied, ev_market, fs.get(\'EBIT\'), \'EV_EBIT\')

calculate(ivps \* fdso, (current_price \* fdso) if current_price else
None, fs.get(\'NOPAT\'), \'P_NOPAT\')

return {

\"schema_version\": schema_version,

\"current_market_price\": current_price,

\"implied_multiples\": implied_multiples

}

def run_sensitivity_analysis(kg, dag, seq, gim, dr, base_results,
scenarios, schema_version=KERNEL_VERSION):

\"\"\"Runs sensitivity analysis (Tornado chart) by modifying GIM
assumptions or DR.\"\"\"

base_ivps = base_results\[\'IVPS\'\]

tornado_data = \[\]

\# Scenarios structure expected: List of dictionaries {driver, low,
high}

for scenario in scenarios:

driver = scenario\[\'driver\'\]

low_change = scenario\[\'low\'\]

high_change = scenario\[\'high\'\]

ivps_low = None

ivps_high = None

for direction, pct_change in \[(\'low\', low_change), (\'high\',
high_change)\]:

temp_gim = copy.deepcopy(gim)

temp_dr = dr

try:

\# Modify the input

if driver == \'Discount_Rate\':

\# Interpret change as absolute basis points change for DR

temp_dr += pct_change

if temp_dr \<= 0.01: raise ValueError(\"Discount Rate too low.\")

elif driver in temp_gim:

\# Modify the GIM assumption (apply percentage change to core
parameters)

mode = temp_gim\[driver\]\[\'mode\'\]

params = temp_gim\[driver\]\[\'params\'\]

def apply_change(value, change):

return value \* (1 + change)

if mode == \'STATIC\':

params\[\'value\'\] = apply_change(params\[\'value\'\], pct_change)

elif mode == \'LINEAR_FADE\':

params\[\'start_value\'\] = apply_change(params\[\'start_value\'\],
pct_change)

elif mode == \'CAGR_INTERP\':

params\[\'start_cagr\'\] = apply_change(params\[\'start_cagr\'\],
pct_change)

params\[\'end_cagr\'\] = apply_change(params\[\'end_cagr\'\],
pct_change)

else:

continue

\# Re-run the SCM and APV

forecast_df = execute_scm(kg, dag, seq, temp_gim)

valuation_results = calculate_apv(forecast_df, temp_dr, kg)

scenario_ivps = valuation_results\[\'IVPS\'\]

if direction == \'low\':

ivps_low = scenario_ivps

else:

ivps_high = scenario_ivps

except Exception as e:

logger.error(f\"Error during sensitivity analysis for {driver}
({direction}): {e}\")

\# Append to tornado data

if ivps_low is not None and ivps_high is not None:

\# Ensure ordering (low DR results in high IVPS, etc.)

if ivps_low \> ivps_high:

ivps_low, ivps_high = ivps_high, ivps_low

tornado_data.append({

\"Driver\": driver,

\"IVPS_Low\": ivps_low,

\"IVPS_High\": ivps_high,

\"Impact\": ivps_high - ivps_low

})

\# Sort by impact magnitude

tornado_data.sort(key=lambda x: abs(x\[\'Impact\'\]), reverse=True)

return {

\"schema_version\": schema_version,

\"base_case_ivps\": base_ivps,

\"Tornado_Chart_Data\": tornado_data

}

\#
==========================================================================================

\# 4. LIGHTWEIGHT SUMMARY GENERATOR (G3_1.8 - The Selective Emission
Artifact)

\#
==========================================================================================

def generate_lightweight_valuation_summary(valuation_results,
forecast_summary, implied_multiples, sensitivity_results, kg,
forecast_df, gim, schema_version=KERNEL_VERSION):

\"\"\"Generates the LIGHTWEIGHT_VALUATION_SUMMARY (A.7) artifact.\"\"\"

v = valuation_results

fs = forecast_summary.get(\'summary_data\', {})

im = implied_multiples.get(\'implied_multiples\', {})

sr = sensitivity_results

def safe_float(val):

try:

return float(val)

except (TypeError, ValueError):

return None

\# 1. IVPS Summary

ivps_summary = {

\"IVPS\": safe_float(v.get(\"IVPS\")),

\"DR\": safe_float(v.get(\"DR\")),

\"Terminal_g\": safe_float(v.get(\"Terminal_g\")),

\"ROIC_Terminal\": safe_float(v.get(\"Terminal_ROIC_r\")),

\"Current_Market_Price\":
safe_float(implied_multiples.get(\"current_market_price\"))

}

\# 2. Implied Multiples Analysis

implied_multiples_analysis = {

\"Implied_EV_Sales_Y1\": im.get(\"Implied_EV_Sales_Y1\"),

\"Implied_EV_EBIT_Y1\": im.get(\"Implied_EV_EBIT_Y1\"),

\"Implied_P_NOPAT_Y1\": im.get(\"Implied_P_NOPAT_Y1\"),

\"Market_EV_Sales_Y1\": im.get(\"Market_EV_Sales_Y1\"),

\"Market_EV_EBIT_Y1\": im.get(\"Market_EV_EBIT_Y1\"),

\"Market_P_NOPAT_Y1\": im.get(\"Market_P_NOPAT_Y1\")

}

\# 3. Sensitivity Analysis (Tornado Summary)

tornado_data = sr.get(\'Tornado_Chart_Data\', \[\])

tornado_summary = \[\]

base_ivps = safe_float(sr.get(\'base_case_ivps\')) or
ivps_summary\[\"IVPS\"\]

for item in tornado_data\[:SENSITIVITY_TORNADO_TOP_N\]:

swing_percent = None

ivps_low = safe_float(item.get(\"IVPS_Low\"))

ivps_high = safe_float(item.get(\"IVPS_High\"))

if base_ivps and abs(base_ivps) \> EPSILON and ivps_low is not None and
ivps_high is not None:

swing_percent = (ivps_high - ivps_low) / base_ivps

tornado_summary.append({

\"Driver_Handle\": item.get(\"Driver\"),

\"IVPS_Low\": ivps_low,

\"IVPS_High\": ivps_high,

\"IVPS_Swing_Percent\": swing_percent

})

tornado_summary.sort(key=lambda x: abs(x.get(\"IVPS_Swing_Percent\") or
0), reverse=True)

\# 4. Key Forecast Metrics

revenue_cagr_y1_y5 = None

if \'Revenue\' in forecast_df.columns and len(forecast_df) \>= 5:

try:

y0_revenue = kg.get(\'core_data\', {}).get(\'Y0_data\',
{}).get(\'Revenue\')

if y0_revenue is not None and y0_revenue \> 0:

y5_revenue = forecast_df\[\'Revenue\'\].iloc\[4\]

revenue_cagr_y1_y5 = (y5_revenue / y0_revenue)\*\*(1/5) - 1

except Exception as e:

logger.warning(f\"Could not calculate Revenue CAGR Y1-Y5: {e}\")

ebit_margin_y5 = None

if \'EBIT\' in forecast_df.columns and \'Revenue\' in
forecast_df.columns and len(forecast_df) \>= 5:

rev_y5 = forecast_df\[\'Revenue\'\].iloc\[4\]

if abs(rev_y5) \> EPSILON:

ebit_margin_y5 = forecast_df\[\'EBIT\'\].iloc\[4\] / rev_y5

roic_y5 = None

if \'ROIC\' in forecast_df.columns and len(forecast_df) \>= 5:

roic_y5 = forecast_df\[\'ROIC\'\].iloc\[4\]

key_forecast_metrics = {

\"Revenue_CAGR_Y1_Y5\": safe_float(revenue_cagr_y1_y5),

\"EBIT_Margin_Y5\": safe_float(ebit_margin_y5),

\"ROIC_Y5\": safe_float(roic_y5)

}

\# 5. Terminal Driver Values (NEW PATCH)

terminal_drivers = {}

if gim and not forecast_df.empty:

for driver in gim.keys():

if driver in forecast_df.columns:

\# Extract Year 20 (final) value

terminal_drivers\[driver\] =
safe_float(forecast_df\[driver\].iloc\[-1\])

\# 6. Forecast Trajectory Checkpoints (G3_1.8)

\# Capture nominal values at Y0, Y5, Y10, Y20 for key drivers (Exogenous
and select Endogenous/Financial)

trajectory_checkpoints = {\"Y0\": {}, \"Y5\": {}, \"Y10\": {}, \"Y20\":
{}}

y0_data = kg.get(\'core_data\', {}).get(\'Y0_data\', {})

\# Identify drivers to track: All GIM drivers (Exogenous) + Key
Financials/Endogenous

exogenous_drivers = list(gim.keys())

key_internal_drivers = \[\'Revenue\', \'EBIT\', \'NOPAT\',
\'Invested_Capital\', \'ROIC\', \'FCF_Unlevered\'\]

\# Robustly add key operational primitives modeled in the DAG

\# We look at columns in the forecast_df that are not exogenous and not
the standard financials

for driver in forecast_df.columns:

if driver not in exogenous_drivers and driver not in
key_internal_drivers:

\# Add the driver if it is not already included, prioritizing those
present in Y0 data

if driver in y0_data or len(key_internal_drivers) \< 15: \# Limit total
internal drivers to keep summary lightweight

if driver not in key_internal_drivers:

key_internal_drivers.append(driver)

all_drivers_to_track = exogenous_drivers + key_internal_drivers

for driver in all_drivers_to_track:

\# Y0

if driver in y0_data:

trajectory_checkpoints\[\"Y0\"\]\[driver\] =
safe_float(y0_data\[driver\])

\# Forecast Years (Y5, Y10, Y20)

if driver in forecast_df.columns:

if len(forecast_df) \>= 5:

trajectory_checkpoints\[\"Y5\"\]\[driver\] =
safe_float(forecast_df\[driver\].iloc\[4\]) \# Y5 is index 4

if len(forecast_df) \>= 10:

trajectory_checkpoints\[\"Y10\"\]\[driver\] =
safe_float(forecast_df\[driver\].iloc\[9\]) \# Y10 is index 9

if len(forecast_df) \>= 20:

\# Use index 19 (iloc\[-1\]) for Y20 assuming FORECAST_YEARS=20

trajectory_checkpoints\[\"Y20\"\]\[driver\] =
safe_float(forecast_df\[driver\].iloc\[-1\])

return {

\"schema_version\": schema_version,

\"ivps_summary\": ivps_summary,

\"implied_multiples_analysis\": implied_multiples_analysis,

\"sensitivity_analysis\": {

\"tornado_summary\": tornado_summary

},

\"key_forecast_metrics\": key_forecast_metrics,

\"terminal_drivers\": terminal_drivers,

\"forecast_trajectory_checkpoints\": trajectory_checkpoints \# G3_1.8

}

\#
==========================================================================================

\# 5. WORKFLOW ORCHESTRATOR (Main API) (Updated for G3_1.8)

\#
==========================================================================================

def execute_cvr_workflow(kg, dag_artifact, gim_artifact, dr_trace,
sensitivity_scenarios=None, valuation_date=None):

\"\"\"

The main API for the CVR Kernel (G3_2.2.1e).

Implements Selective Emission: Returns ONLY the
LightweightValuationSummary (A.7).

\"\"\"

print(f\"CVR Kernel Execution Started (Version: {KERNEL_VERSION})\...
\[MRC Mode\]\")

schema_version = KERNEL_VERSION

\# Extract structures from artifacts

dag = dag_artifact.get(\'DAG\', {})

gim = gim_artifact.get(\'GIM\', {})

\# 0.5 Validate DAG Coverage

print(\"Validating DAG coverage against Y0_data\")

try:

validate_dag_coverage(kg, dag_artifact)

except RuntimeError as e:

logger.error(f\"DAG Coverage Validation Failed: {e}\")

raise

\# 1. Derive Execution Sequence (Topological Sort)

print(\"Deriving SCM execution sequence\...\")

try:

seq = topological_sort(dag)

except Exception as e:

logger.error(f\"Topological Sort Failed: {e}\")

raise

\# 2. Extract DR

try:

dr = float(dr_trace\[\'derivation_trace\'\]\[\'DR_Static\'\])

except (KeyError, TypeError, ValueError):

raise RuntimeError(\"Failed to parse DR from DR_DERIVATION_TRACE.\")

\# 3. Execute SCM Forecast

print(f\"Executing {FORECAST_YEARS}-Year SCM Forecast\...\")

try:

forecast_df = execute_scm(kg, dag, seq, gim)

except Exception as e:

logger.error(f\"SCM Execution Failed: {e}\")

raise

\# 4. Execute APV Valuation

print(\"Executing APV Valuation\...\")

try:

valuation_results = calculate_apv(forecast_df, dr, kg)

except Exception as e:

logger.error(f\"APV Valuation Failed: {e}\")

raise

\# 5. Generate Internal Artifacts

print(\"Generating Internal Summary Artifacts\...\")

try:

forecast_summary = generate_forecast_summary(forecast_df,
schema_version)

except Exception as e:

logger.error(f\"Forecast Summary Generation Failed: {e}\")

raise

\# 6. Calculate Implied Multiples

print(\"Calculating Implied Multiples Analysis\...\")

try:

implied_multiples = calculate_implied_multiples(valuation_results,
forecast_summary, kg, schema_version)

except Exception as e:

logger.warning(f\"Implied Multiples Analysis Failed: {e}\")

implied_multiples = {}

\# 7. Execute Sensitivity Analysis

sensitivity_results = {}

if sensitivity_scenarios:

print(\"Executing Sensitivity Analysis\...\")

try:

\# Note: Sensitivity scenarios are expected to be a list of {driver,
low, high} definitions.

sensitivity_results = run_sensitivity_analysis(kg, dag, seq, gim, dr,
valuation_results, sensitivity_scenarios, schema_version)

except Exception as e:

logger.warning(f\"Sensitivity Analysis Failed: {e}\")

sensitivity_results = {}

\# 8. Generate Lightweight Summary (The Selective Emission)

print(\"Generating Lightweight Valuation Summary (A.7)\...\")

try:

lightweight_summary = generate_lightweight_valuation_summary(

valuation_results,

forecast_summary,

implied_multiples,

sensitivity_results,

kg,

forecast_df,

gim, \# PASSED HERE IN PATCH

schema_version

)

except Exception as e:

logger.error(f\"Lightweight Summary Generation Failed: {e}\")

raise

print(\"CVR Kernel Execution Completed.\")

return lightweight_summary

---

**APPENDIX D: Filesystem Naming Conventions**

### Prompt Files (Canonical Inputs)

| File | Description |
|------|-------------|
| `G3BASE_2.2.1e.md` | BASE stage prompt (this document) |
| `G3RQ_2.2.2.md` | RQ_GEN stage prompt |
| `G3ENRICH_2.2.1e.md` | ENRICHMENT stage prompt |
| `CVR_KERNEL_2.2.1e.py` | BASE kernel (reference) |
| `CVR_KERNEL_ENRICH_2.2.1e.py` | ENRICHMENT kernel (extended DSL) |

### Output Files

**Pattern:** `{TICKER}_{STAGE}{VERSION}O_T{N}_{YYYYMMDD}.md`

| Element | Description |
|---------|-------------|
| `{TICKER}` | Company identifier (uppercase) |
| `{STAGE}` | Pipeline stage: `BASE`, `RQ`, `ENRICH` |
| `{VERSION}` | Pipeline version (e.g., `2.2.1e`) |
| `O` | Output file indicator |
| `T{N}` | Turn number (T1, T2) — omit for single-turn stages |
| `{YYYYMMDD}` | Valuation as-of date |

### Examples

```
NVDA_BASE2.2.1eO_T1_20251207.md    # Turn 1: Narratives + A.1-A.6
NVDA_BASE2.2.1eO_T2_20251207.md    # Turn 2: Unified report + A.7
AAPL_BASE2.2.1eO_T1_20251215.md
AAPL_BASE2.2.1eO_T2_20251215.md
```
