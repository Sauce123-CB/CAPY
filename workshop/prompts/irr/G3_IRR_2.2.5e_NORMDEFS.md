APPENDIX B: NORMATIVE DEFINITIONS (Condensed)
________________


B.1. Financial Definitions and Formulas (Simplified APV)
Inherited from G3 BASE/ENRICHMENT 2.2.
#
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
        9. Valuation Methodology (Simplified APV, 20-Year, Static DR)
* Discounting: End-of-year convention
* DR: Static, derived in BASE (unless DR Overlay justified)
* PV Explicit FCF: Σ(FCF_t / (1+DR)^t) for t=1→20
* Terminal Value: TV = FCF₂₁ / (DR − g_terminal), where FCF₂₁ = FCF₂₀ × (1 + g_terminal)
* Enterprise Value: EV = PV_Explicit + PV_Terminal
* Equity Value: EV − Net_Debt_Y0
* IVPS: Equity_Value / Shares_Outstanding_Diluted_TSM
11. Timing Convention (DAG Compliance)
* ROIC MUST use PREV(Invested_Capital)
* All balance sheet denominators MUST use PREV()
12. ATP Mandate (Accounting Translation Protocol)
* All A.2 inputs are ATP-reconciled per BASE P1.5, preserved through ENRICHMENT and SCENARIO
* The accounting_translation_log documents reconciliation to normative definitions
* Adjudication Responsibility: When A.10 raises Source Integrity findings on accounting treatment, verify against ATP reconciliation in A.2. Valid ATP gaps may warrant ACCEPT disposition.
* Normative Primacy: Definitions in this section take precedence over raw reported figures in all adjudication decisions
________________


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
        schedule[], post_schedule_dsl (optional). Primary method for Lump Sums.
        ________________


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
1. Add "FCF_Adjustment" driver if needed
2. Use EXPLICIT_SCHEDULE: {"schedule": [0, 0, -50000000, 0, ...], "post_schedule_dsl": {"type": "STATIC", "value": 0}}
3. Flows directly to FCF (no debt dynamics under Simplified APV)
Design Principles
* Holistic Impact: Capture complete economic effect (investment, margin dilution, execution risk)
* Economic Coherence: Intervened SCM must satisfy Economic Governor at terminal
* Minimal Modification: Prefer simplest intervention type that captures scenario economics
* Reversibility: Permanent = modified terminal assumptions; Temporary = EXPLICIT_SCHEDULE with reversion
________________


B.7. Probability Estimation (Bayesian Protocol)
Framework: P(Scenario) = P(C₁) × P(C₂|C₁) × P(C₃|C₁,C₂) × ... × P(Outcome|All Conditions)
Three-Step Protocol
Step 1: ANCHOR (Prior/Outside View)
* Select reference class (specific enough to be relevant, broad enough for N≥10)
* Extract base rate from H.A.D. (frequency, time horizon, trends)
* Assess data quality: sample size (N<10 = high uncertainty), recency (>10yr = check structural changes), survivorship bias
* Document: "In reference class [X], event occurs at [Y%] based on [N] observations over [period]"
Step 2: DECONSTRUCT (Causal Decomposition)
* Identify prerequisite chain: market conditions → company capabilities → triggers → execution
* Express as conditional probability product
* Purpose: Forces explicit reasoning, prevents story-driven estimation, enables auditability
Step 3: UPDATE (Posterior/Inside View)
* Integrate company-specific evidence to adjust each conditional
* Document direction, magnitude, and evidence for each adjustment
* Extraordinary claims require extraordinary evidence
* Calculate final P(Scenario) by multiplying through decomposition
Calibration Mandates
Overconfidence Correction (Mandatory if P>70% upside OR P<10% downside):
* "What is the base rate? Does my estimate exceed it, and why?"
* "Am I accounting for unknown unknowns?"
* "Would I bet at these odds?"
* Document sanity check in trace
Independence Mandate: Estimate probabilities independently per scenario; correlations handled in SSE (B.8)
Common Errors to Avoid:
1. Anchoring on management guidance (not base rates)
2. Neglecting base rates ("this company is special")
3. Conjunction fallacy: P(A∩B) ≤ P(A)
4. Availability bias (recent/vivid ≠ more probable)
________________


B.8. Integration Methodology (Structured State Enumeration)
Core Concepts
* State Space: N scenarios → 2^N states (each scenario occurs or doesn't)
* Feasibility: Infeasible states get P=0, excluded from distribution
* State IVPS: Base + sum of active scenario impacts
* E[IVPS]: Probability-weighted average across feasible states
Initialize-Filter-Renormalize Procedure
Phase
        Action
        Output
        1. Initialize
        Calculate P_initial for all 2^N states. Independent: ∏P(active) × ∏(1−P(inactive)). Handle dependencies if defined.
        {state_id, scenarios_active, p_initial}
        2. Filter
        Eliminate infeasible states: MECE violations (P=0 if mutually exclusive scenarios co-occur), Economic incompatibilities (P=0 if incompatible pairs co-occur). MANDATORY: BLUE_SKY ↔ BLACK_SWAN incompatible.
        Feasibility flags updated
        3. Renormalize
        RF = 1.0 / Σ(P_initial for feasible). P_final = P_initial × RF (feasible) or 0 (infeasible). Validate: Σ(P_final) = 1.0
        Final JPD
        State IVPS Calculation
Additive Impact: IVPS_raw(State) = IVPS_Base + Σ(IVPS_Impact for active scenarios)
* Assumes approximately additive impacts (tractability assumption)
* Non-linear interactions noted as model limitations if material
Limited Liability: IVPS_final = MAX(0.0, IVPS_raw)
* Equity cannot go negative; floor at zero
* Flag when constraint binds; retain raw value for transparency
E[IVPS]: Σ(P_final × IVPS_final) — exact calculation, not simulation
Kernelized Execution: calculate_sse_jpd() ensures computational integrity, constraint enforcement, reproducibility
________________


B.9. Distributional Analysis Protocol
Distribution Primacy: E[IVPS] is a summary statistic. Full distribution reveals risk (left tail), opportunity (right tail), uncertainty (range), and shape.
Required Metrics
Percentiles (calculated by ordering states by IVPS, accumulating probabilities, interpolating):
Metric
        Meaning
        P10
        Downside case (10% below)
        P50
        Median (more robust than mean for skewed distributions)
        P90
        Upside case (90% below)
        Dispersion:
* Range: Max − Min IVPS
* Std Dev: σ = √(Σ P × (IVPS − E[IVPS])²)
* Coef. of Variation: σ / E[IVPS] (enables cross-company comparison)
Shape:
Skewness
        Condition
        Interpretation
        LEFT
        Mean < Median
        Long left tail; downside > upside
        SYMMETRIC
        Mean ≈ Median
        Balanced
        RIGHT
        Mean > Median
        Long right tail; upside > downside


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
$0-10   | ████ (12%)
$10-20  | ██ (6%)
$20-30  | ███████████ (28%)  ← Base Case
$30-40  | ████████████████ (35%)
$40-50  | ███████ (15%)
E[IVPS]: $31.50 | Median: $32.00 | P10: $8.50 | P90: $48.00


Structured Data: Array of {ivps_bucket_label, ivps_bucket_midpoint, probability_mass, cumulative_probability}
________________


B.X. Integration-Specific Definitions
B.X.1 Verification Discovery Protocol (Evidentiary Hierarchy)
Rank
        Source Type
        Authority Level
        1
        Primary Documents
        Highest — 10-K, 10-Q, 8-K, proxy, audited financials. Ground truth for company facts.
        2
        Verified External Sources
        High — Retrieved via Verification Search from authoritative third parties. Must be explicitly verified.
        3
        CVR Analysis (State 3)
        Medium — Analytical judgments in A.1–A.10. Rigorous but rebuttable by higher-authority evidence.
        4
        Audit Rhetoric
        Lowest — A.10 assertions lacking direct citation. May identify concerns but don't override upstream analysis alone.
        B.X.2 Scenario Substitution Mandate
Expected Materiality = |P × M|
* P = Posterior probability (0.0–1.0)
* M = IVPS impact ($/share, positive or negative)
* Absolute value ensures both high-P/moderate-M and low-P/high-M scenarios rank appropriately
Substitution Rule: Top 4 scenarios by Expected Materiality constitute finalized set. Displaced scenarios logged in A.11 with rationale.
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
        Materially undermines E[IVPS] confidence
        Blocks finalization without resolution
        HIGH
        Significant concern
        Requires documented disposition (ACCEPT/REJECT/MODIFY)
        MEDIUM
        Notable but lower materiality
        Discretionary adjudication


B.X.5 Convergence Rate Definitions


**CR (Convergence Rate):** The fraction of the price→intrinsic value gap that closes annually in the null case, driven by earnings announcements validating GIM projections. Base rate 0.20, range 0.10-0.40. Captures recognition speed only; fundamental factors affect E[IVPS] directly.


**Recognition factors:** Market microstructure and information environment characteristics that affect how quickly the market incorporates new information into price, independent of the information's fundamental content. Categories include: information dissemination efficiency (analyst coverage, institutional ownership, short interest), attention catalysts (investor days, conference visibility, index inclusion), market microstructure (liquidity, listing venue, borrow availability), and narrative receptivity (thesis simplicity, recent price action).


        B.10 Multiple Selection
Objective: Select the valuation multiple(s) the market uses to price companies with this profile.
Principle: The market prices growth on revenue, profitability on EBITDA/FCF. Match the multiple to the company's current stage and what investors focus on.
Guidelines:
* Pre-profit or high-growth (EBITDA margin <5%): EV/Revenue (100%)
* Transitional (EBITDA margin 5–20%): Blend EV/Revenue and EV/EBITDA
  - Weight toward Revenue at lower margins, toward EBITDA at higher margins
  - Use linear interpolation: EV/EBITDA weight = (Margin - 5%) / 15%
* Mature and cash-generative (EBITDA margin >20%, FCF conversion >50%): EV/EBITDA + EV/FCF
* Cyclical: Normalized EV/EBITDA


Avoid hard threshold discontinuities. If margin is near a boundary, blend multiples rather than switching abruptly. Document weighting rationale. Use the regime appropriate at T+1, not T0.


________________


B.12 Resolution Percentage (ρ)
Definition: ρ(S, T+1) ∈ [0, 1] represents how much of scenario S's uncertainty resolves by T+1.
Key Distinction: ρ is not probability. A high-P scenario may have low ρ (outcome still unknown) or high ρ (we'll know soon).
Effective Magnitude:
Effective_M(S, T+1) = ρ × Full_M(S)
Estimation Guidance:
Driver Type
        Typical ρ Range
        Legal/Regulatory (with timeline)
        0.3–0.8
        Product Launch
        0.2–0.5
        Macro/Credit
        0.2–0.4
        Competitive/Strategic
        0.1–0.3
        Evidence Required: Primary driver, key dates, reference class (if available).
Conservatism Default: If no specific timeline evidence, use ρ ≤ 0.30.
________________


B.13 Convergence Rate (CR) Framework


#### B.13.1 Conceptual Framework


The Convergence Rate (CR) measures what fraction of the price→value gap closes annually in the null case. This convergence occurs primarily through earnings announcements that validate GIM projections.


**Key Design Principle:** CR captures only *recognition speed* factors. All fundamental factors (management quality, competitive position, balance sheet, etc.) already affect E[IVPS] through GIM, DR, scenarios, and fair multiple adjustments. Including them in CR would double-count.


**Decomposition:**
- GIM alpha (projected fundamentals vs. consensus) → converges via earnings validation
- Scenario optionality → converges via scenario resolution (captured by ρ parameters)


CR applies to the null case. Scenario-driven convergence is handled separately through the fork structure and ρ estimates.


**Empirical Anchor:**
- Literature consensus: 3-5 year half-life for value stock convergence → ~15-23% annual CR
- Johnson & Xie (2004): Only 23% of extreme V/P stocks converge; this subset drives returns
- Base rate: CR = 0.20 (conservative, reflects that not all undervaluation converges)


#### B.13.2 Base Rate and Bounds


| Parameter | Value | Rationale |
|-----------|-------|-----------|
| CR_base | 0.20 | Conservative anchor consistent with 3-4 year half-life |
| CR_floor | 0.10 | Even severe orphan stocks exhibit some drift |
| CR_ceiling | 0.40 | Beyond this requires variance justification |


#### B.13.3 Inside-View Adjustment Rubric


Adjust CR from base rate using ONLY recognition-speed factors. Do NOT include factors that affect intrinsic value (these belong in GIM, DR, scenarios, or fair multiple).


**Category 1: Information Dissemination Efficiency**


How quickly does new information get incorporated into price?


| Factor | Condition | Adjustment |
|--------|-----------|------------|
| Analyst coverage | 0 analysts | -0.04 |
| | 1-3 analysts | -0.02 |
| | 4-8 analysts | 0 |
| | 9+ analysts | +0.02 |
| Active institutional ownership | <10% active (non-index) | -0.03 |
| | 10-40% active | 0 |
| | >40% active | +0.02 |
| Short interest (% float) | >15% | +0.02 |
| | 5-15% | +0.01 |
| | <5% | 0 |


**Category 2: Attention Catalysts (Non-Scenario)**


Events that force market engagement, independent of fundamental catalysts. Do NOT include hard catalysts (contracts, regulatory decisions, product launches) — these are scenarios with ρ estimates.


| Factor | Condition | Adjustment |
|--------|-----------|------------|
| Investor/Analyst Day | Scheduled in NTM | +0.02 |
| Conference visibility | Multiple high-profile in NTM | +0.01 |
| Index inclusion | Likely in NTM (Russell, S&P) | +0.03 |
| Lock-up expiry | >10% of float in NTM | -0.02 |


**Category 3: Market Microstructure**


Frictions that delay price adjustment even when information is available.


| Factor | Condition | Adjustment |
|--------|-----------|------------|
| Liquidity | Bid-ask >3% OR ADV <$250K | -0.04 |
| | Bid-ask 1-3% OR ADV $250K-$1M | -0.02 |
| | Bid-ask <1% AND ADV >$1M | 0 |
| Listing venue | OTC / foreign ordinary | -0.02 |
| | ADR (liquid) or primary US | 0 |
| Borrow availability | Hard to borrow (>5% fee) | +0.02 |


**Category 4: Narrative Receptivity**


Is the market mentally positioned to accept the re-rating thesis?


| Factor | Condition | Adjustment |
|--------|-----------|------------|
| Thesis simplicity | One-sentence, obvious | +0.02 |
| | Requires nuance | 0 |
| | Counter-consensus, complex | -0.02 |
| Recent price action (6M) | Up >50% | -0.02 |
| | -20% to +50% | 0 |
| | Down >30% | 0 (context-dependent) |


#### B.13.4 CR Calculation


```
CR_inside = max(0.10, min(0.40, CR_base + Σ(adjustments)))
```


If adjustments would push CR beyond 0.40, invoke variance justification and document rationale.


#### B.13.5 Factors Excluded from CR (Anti-Double-Counting)


The following factors affect E[IVPS] and must NOT be included in CR adjustments:


| Excluded Factor | Correct Location |
|-----------------|------------------|
| Management credibility/track record | GIM conservatism, DR |
| Accounting quality | DR, fair multiple (B.11) |
| Governance (dual-class, controlled) | Fair multiple (B.11) |
| Revenue trajectory | GIM |
| Competitive position / moat | GIM, scenarios |
| Balance sheet quality | Net debt, distress scenarios |
| Capital allocation history | GIM reinvestment assumptions |
| Hard catalysts with dates | Scenarios with ρ estimates |
| Sector sentiment | Cohort multiples (B.11) |
| Activist involvement (operational) | Scenario if material |


#### B.13.6 Integration with IRR Calculation


The null case Multiple Convergence IRR uses CR to determine recognition speed:


```
MC_null = CR × (Fair_Multiple / Current_Multiple - 1)
```


This flows into the probability-weighted IRR calculation alongside scenario-specific convergence driven by ρ parameters.
________________


B.14 IRR Decomposition
The Three Components:
E[IRR] = Fundamental_Growth + Multiple_Convergence + Scenario_Resolution
Component
        Definition
        Risk Profile
        Fundamental Growth
        Return from metric growth at constant multiple
        Lower risk (execution)
        Multiple Convergence
        Return from multiple re-rating
        Higher risk (sentiment)
        Scenario Resolution
        Incremental return vs. null case
        Binary risk (events)
        Convergence Dependency Ratio:
CDR = Multiple_Convergence / E[IRR]
* CDR > 0.50: "Convergence Dependent" — flag elevated sentiment risk
* CDR < 0.30: "Fundamental Floor" — returns resilient to multiple stagnation
