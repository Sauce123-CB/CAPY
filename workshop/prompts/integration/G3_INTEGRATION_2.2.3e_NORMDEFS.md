APPENDIX B: NORMATIVE DEFINITIONS (Condensed)

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

B.1. Financial Definitions and Formulas (Simplified APV)

Inherited from G3 BASE/ENRICHMENT 2.2.

**DR Methodology:** See G3BASE_2.2.3e_NORMDEFS.md Section B.3 for complete DR specification, including:
- Discount Rate Philosophy (practitioner utility function, NOT WACC)
- Currency-Matched RFR requirement (MANDATORY)
- Global Universe X calibration [0.5, 2.0]

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

\* All A.2 inputs are ATP-reconciled per BASE P1.5, preserved through
ENRICHMENT and SCENARIO

\* The accounting_translation_log documents reconciliation to normative
definitions

\* Adjudication Responsibility: When A.11 raises Source Integrity
findings on accounting treatment, verify against ATP reconciliation in
A.2. Valid ATP gaps may warrant ACCEPT disposition.

\* Normative Primacy: Definitions in this section take precedence over
raw reported figures in all adjudication decisions

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

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

B.X. Integration-Specific Definitions

B.X.1 Verification Discovery Protocol (Evidentiary Hierarchy)

Rank

Source Type

Authority Level

1

Primary Documents

Highest --- 10-K, 10-Q, 8-K, proxy, audited financials. Ground truth for
company facts.

2

Verified External Sources

High --- Retrieved via Verification Search from authoritative third
parties. Must be explicitly verified.

3

CVR Analysis (State 3)

Medium --- Analytical judgments in A.1--A.10. Rigorous but rebuttable by
higher-authority evidence.

4

Audit Rhetoric

Lowest --- A.11 assertions lacking direct citation. May identify
concerns but don\'t override upstream analysis alone.

B.X.2 Scenario Substitution Mandate

Expected Materiality = \|P × M\|

\* P = Posterior probability (0.0--1.0)

\* M = IVPS impact (\$/share, positive or negative)

\* Absolute value ensures both high-P/moderate-M and low-P/high-M
scenarios rank appropriately

Substitution Rule: Top 4 scenarios by Expected Materiality constitute
finalized set. Displaced scenarios logged in A.11 with rationale.

B.X.3 Recalculation Cascade Scope

Cascade Type

Trigger

Scope

FULL

GIM base case modification

SCM → APV → All scenario magnitudes → SSE

PARTIAL_SCENARIO

Scenario intervention modification or new scenario

Affected scenario magnitude → SSE

PARTIAL_SSE

Probability revision or scenario removal (no intervention change)

SSE only

NONE

No accepted modifications

State 4 = State 3

B.X.4 Priority Classification (from Silicon Council)

Priority

Definition

Action

CRITICAL

Materially undermines E\[IVPS\] confidence

Blocks finalization without resolution

HIGH

Significant concern

Requires documented disposition (ACCEPT/REJECT/MODIFY)

MEDIUM

Notable but lower materiality

Discretionary adjudication

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

