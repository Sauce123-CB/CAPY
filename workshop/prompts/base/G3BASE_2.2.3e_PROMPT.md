# G3BASE 2.2.3e: Autonomous Causal Valuation

> **Version:** 2.2.3e (Atomized)
> **Change from 2.2.2e:** Currency auto-detection, DR global calibration, terminal g from topline
> **Patch:** PATCH-2024-12-22-001 Section 13, 14

# I. MISSION AND OBJECTIVES

-   **Mission:** Execute the BASE stage (G3_2.2.3e) of the CAPY Pipeline
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
  - This prompt (G3BASE_2.2.3e_PROMPT.md)
  - G3BASE_2.2.3e_SCHEMAS.md (Appendix A)
  - G3BASE_2.2.3e_NORMDEFS.md (Appendix B)
  - Company Documents (filings, transcripts, supplementary materials)
  - BASE_CVR_KERNEL_2.2.3e.py (reference context only)

#### Currency Detection (MANDATORY - Before Analysis)

Before beginning analysis, identify the **REPORTING CURRENCY**:

1. Check 10-K/10-Q cover page for currency declaration
2. Verify revenue/EBIT/assets are denominated in this currency
3. Document in `A.2.market_context.reporting_currency`

**All GIM, DR, IVPS calculations must be in REPORTING CURRENCY.**
**Convert market price to reporting currency for final IVPS comparison.**

If the company trades on a different exchange (e.g., ADR), note both:
- `reporting_currency`: Currency of published financials (e.g., "EUR")
- `price_currency`: Currency of market price (e.g., "USD")
- `fx_rate_to_reporting`: FX rate if currencies differ

- **Scope:** Execute Phases A-D (Sections III-IV). Produce analytical narratives (N1-N4) and artifacts A.1-A.6 that logically entail A.7.
- **Output:** Atomized files per Section V. Write 9 individual files (4 narratives + 5 artifacts) using the Write tool.
- **Exclusion:** Do NOT compute A.7. Kernel is provided for semantic alignment only.

**Turn 2: Validation & Execution**

- **Trigger:** "Do Turn 2"
- **Attachments Required:**
  - This prompt (G3BASE_2.2.3e_PROMPT.md)
  - G3BASE_2.2.3e_SCHEMAS.md
  - G3BASE_2.2.3e_NORMDEFS.md
  - Turn 1 artifacts: All 9 files from 01_T1/ folder (A.1-A.6 JSON + N1-N4 markdown)
  - BASE_CVR_KERNEL_2.2.3e.py
- **Scope:** Validate Turn 1 artifacts for JSON integrity and internal consistency, repair if needed, execute kernel via Bash, write A.7 to disk.
- **Output:** A.7 valuation artifact + kernel receipt. See Section V for filenames.

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

-   **Market Price Requirement (MANDATORY):** Before populating `Current_Stock_Price` in A.2.market_context:
    1. Use WebSearch: "{TICKER} stock price"
    2. Extract the current market price from search results
    3. Document the search timestamp
    > **DO NOT** use prices from source documents (stale) or from memory (potentially hallucinated). This is required for accurate upside/downside calculations.

-   **The Verification Doctrine (Externalized Schemas):** The required
    > output schemas are provided in the attached G3BASE_2.2.2e_SCHEMAS.md.

-   **The CVR Kernel (Context Reference):** The CVR Kernel (attached as BASE_CVR_KERNEL_2.2.2e.py) defines the computational logic that Turn 2 will execute. It is provided in Turn 1 for CONTEXTUAL UNDERSTANDING ONLY—to ensure your artifacts are semantically aligned with kernel expectations. Do NOT attempt to execute this code in Turn 1.

### B. Two-Shot Execution Architecture (Critical)

This prompt operates in TWO-SHOT EXECUTION mode with strict separation of concerns:

**TURN 1 RESPONSIBILITY (This Prompt, Analytical Instance):**

- Construct all analytical artifacts (A.1–A.6) with full epistemic rigor
- Emit artifacts as valid JSON in a single fenced code block
- Ensure structural compatibility with kernel requirements (see G3BASE_2.2.2e_NORMDEFS.md)
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

**Turn 1 Terminus:** Upon completing pre-emission validation, write all 9 atomized files per Section V. This concludes Turn 1. Turn 2 will perform secondary validation, execute the kernel, and write A.7 + kernel receipt to disk.

**V. OUTPUT MANDATE (Atomized Artifact Emission)**

*This section governs Turn 1 output. Turn 2 adds A.7 via kernel execution.*

### CRITICAL: Atomized Output (Pattern 12)

**DO NOT emit a single consolidated markdown file with embedded JSON.**

Each artifact and narrative MUST be written as an **individual file** using the Write tool. This prevents truncation and ensures downstream stages receive complete inputs.

### Turn 1 Required Outputs (9 files)

Write each file individually to the analysis folder:

**Narratives (4 files):**
| File | Content |
|------|---------|
| `{TICKER}_N1_THESIS_BASE.md` | Investment thesis narrative |
| `{TICKER}_N2_IC_BASE.md` | Invested capital modeling narrative |
| `{TICKER}_N3_ECON_GOV_BASE.md` | Economic governor constraints narrative |
| `{TICKER}_N4_RISK_BASE.md` | Risk assessment narrative |

**Artifacts (5 files):**
| File | Content |
|------|---------|
| `{TICKER}_A1_EPISTEMIC_ANCHORS_BASE.json` | Bayesian priors, ROIC_anchor |
| `{TICKER}_A2_ANALYTIC_KG_BASE.json` | Knowledge graph, Y0_data, currency |
| `{TICKER}_A3_CAUSAL_DAG_BASE.json` | DAG structure, coverage manifest |
| `{TICKER}_A5_GIM_BASE.json` | Gestalt Impact Map |
| `{TICKER}_A6_DR_BASE.json` | Discount rate derivation trace |

**Human Audit File (optional):**
| File | Content |
|------|---------|
| `{TICKER}_BASE_T1_AUDIT.md` | Summary for human review (NOT machine input) |

### Turn 2 Required Outputs (1 file + kernel receipt)

| File | Content |
|------|---------|
| `{TICKER}_A7_VALUATION_BASE.json` | Kernel execution output |
| `{TICKER}_KERNEL_RECEIPT_BASE.json` | Execution proof (Pattern 13) |

### Output Protocol

1. **Write each artifact as pure JSON** - no markdown wrapper, no code fences
2. **Write each narrative as markdown** - clear section headings
3. **Use exact filenames above** - case-sensitive, underscores required
4. **Validate JSON before writing** - must parse without errors
5. **Include ROIC_anchor in A.1** - used for terminal reinvestment calculation
6. **Include currency fields in A.2.market_context** - reporting_currency required

### Anti-Patterns (DO NOT DO)

❌ Single consolidated markdown file with embedded JSON blocks
❌ JSON wrapped in ```json code fences
❌ Multiple artifacts in one file
❌ Omitting files (all 9 T1 files required)
❌ Using old naming convention ({TICKER}_BASE2.2.3eO_T1.md)

---

**APPENDIX D: Filesystem Naming Conventions**

### Prompt Files (Canonical Inputs)

| File | Description |
|------|-------------|
| `G3BASE_2.2.3e_PROMPT.md` | BASE stage prompt (this document) |
| `G3BASE_2.2.3e_SCHEMAS.md` | Artifact schemas (Appendix A) |
| `G3BASE_2.2.3e_NORMDEFS.md` | DSL and normative definitions (Appendix B) |
| `BASE_CVR_KERNEL_2.2.3e.py` | BASE kernel (execution) |

### Output Files (Canonical Snapshot Naming)

**Pattern:** `{TICKER}_{ARTIFACT}_{STAGE}.{ext}`

| Element | Description |
|---------|-------------|
| `{TICKER}` | Company identifier (uppercase) |
| `{ARTIFACT}` | Artifact ID: `A1_EPISTEMIC_ANCHORS`, `N1_THESIS`, etc. |
| `{STAGE}` | Pipeline stage suffix: `BASE`, `RQ`, `ENRICH`, `SCEN`, `SC`, `INT`, `IRR` |
| `{ext}` | Extension: `.json` for artifacts, `.md` for narratives |

### Examples

```
NVDA_A1_EPISTEMIC_ANCHORS_BASE.json   # A.1 artifact
NVDA_A2_ANALYTIC_KG_BASE.json         # A.2 artifact (includes currency)
NVDA_A5_GIM_BASE.json                 # A.5 artifact
NVDA_N1_THESIS_BASE.md                # Narrative 1
NVDA_N2_IC_BASE.md                    # Narrative 2
NVDA_A7_VALUATION_BASE.json           # Kernel output (Turn 2)
NVDA_KERNEL_RECEIPT_BASE.json         # Execution proof (Turn 2)
```
