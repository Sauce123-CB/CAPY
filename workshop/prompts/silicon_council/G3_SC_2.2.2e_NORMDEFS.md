# **G3 SILICON COUNCIL 2.2.2e: Normative Definitions and Schemas Reference**

This appendix provides the normative definitions and artifact schemas
from the upstream pipeline stages. Use this reference to audit
compliance with methodological mandates.

## **B.1. Financial Definitions and Formulas (Simplified APV)**

**1. EBIT (Earnings Before Interest and Taxes)**

- MUST include Stock-Based Compensation (SBC) expense as an operating cost.
- Formula: Revenue - Operating Expenses (including SBC) - D&A

**2. NOPAT (Net Operating Profit After Tax)**

- The after-tax operating earnings available to all capital providers.
- Formula: EBIT × (1 - Tax Rate)

**3. Invested Capital (IC)**

- The total capital invested in business operations.
- Methodology: Operating Approach (Net Working Capital + Net PP&E + Capitalized Intangibles + Goodwill)
- Cash Treatment: Exclude excess cash from Invested Capital.

**4. ROIC (Return on Invested Capital)**

- The return generated on invested capital.
- Formula: NOPAT / PREV(Invested_Capital)
- Timing Convention: MUST use Beginning-of-Period (BOP) Invested Capital.

**5. Reinvestment (R)**

- Formula: Δ Invested_Capital (Current Year IC - Prior Year IC)

**6. Reinvestment Rate (RR)**

- Formula: Reinvestment / NOPAT

**7. FCF (Free Cash Flow to the Firm / Unlevered FCF)**

- Formula: NOPAT - Reinvestment = NOPAT × (1 - RR)

**8. Growth (g) --- The Economic Governor**

- Formula: ROIC × Reinvestment Rate
- **The Economic Governor Mandate**: g ≈ ROIC × RR MUST hold in terminal state across Base Case and all scenarios.

**9. Valuation Methodology (Simplified APV)**

The pipeline uses Simplified APV with 20-Year Explicit Forecast and Static DR:

- **Discounting Convention**: End-of-year
- **Discount Rate**: Static DR = RFR + (ERP × X), where X is Risk Multiplier (0.5 to 2.2)
- **ERP Convention**: Set statically to 5.0%
- **PV of Explicit FCF**: Σ(FCF_t / (1 + DR)^t) for t = 1 to 20
- **Terminal Value**: TV = FCF_21 / (DR - g_terminal), where FCF_21 = FCF_20 × (1 + g_terminal)
- **Enterprise Value**: EV = PV_Explicit_FCF + PV_Terminal
- **Equity Value**: EV - Net_Debt_Y0
- **IVPS**: Equity_Value / Shares_Outstanding_Static_Diluted_TSM

**Note on Simplified APV**: The pipeline does NOT model dynamic debt, debt paydown, or Interest Tax Shields. All balance sheet items for the equity bridge are static at Y0.

**10. ATP Mandate (Accounting Translation Protocol)**

- All financial inputs in A.2 must reflect ATP-reconciled economic definitions established in BASE (per BASE P1.5).
- The accounting_translation_log documents how reported figures were reconciled to normative definitions.
- Normative Primacy: The definitions in this section (e.g., EBIT includes SBC) take precedence over raw reported figures, regardless of how metrics are labeled in source documents.
- Audit Focus: Verify that ATP reconciliations are complete, consistent with normative definitions, and faithfully inherited through ENRICHMENT and SCENARIO stages.

## **B.2. Assumption DSL Definitions**

The Domain-Specific Language (DSL) defines how assumptions evolve from Y1 to Y20:

**STATIC**
- Value remains constant for all 20 years.
- Parameters: value

**LINEAR_FADE**
- Linearly interpolates from start to end value.
- Parameters: start_value, end_value, fade_years

**CAGR_INTERP**
- Geometric interpolation from Y0 to target.
- Parameters: target_value, target_year
- Exception: If start ≤ 0 and target > start, uses LINEAR interpolation.

**S_CURVE (Logistic Function)**
- Models growth that accelerates then decelerates toward saturation.
- Parameters: saturation_point (L), steepness_factor (k), inflection_point_year (m)
- Anchored to start at Y0 value.

**EXPLICIT_SCHEDULE**
- Year-by-year specification.
- Parameters: schedule (array), post_schedule_dsl (optional)
- Used for lump sum adjustments in SCENARIO stage.

## **B.3. Artifact Schemas Summary**

**A.1_EPISTEMIC_ANCHORS**
- Near-term anchors: Management Guidance and Wall Street Consensus (Y1-Y3)
- Long-term anchors: Industry Base Rate Distributions with MANDATORY p10, p50, p90 for every exogenous driver
- Mutation Policy: Refinement authorized in ENRICHMENT with high burden of proof

**A.2_ANALYTIC_KG**
- Metadata: atp_complexity_assessment (LOW / MODERATE / HIGH), atp_mode (ATP-Lite / Full ATP)
- Core data: Y0_data (ATP-reconciled historical starting values), TSM_data
- Accounting translation log: Documents reconciliation of reported figures to economic definitions per ATP (P1.5 in BASE)
- Market context: Current_Stock_Price, RFR, ERP
- Share data: Diluted share count details

**A.3_CAUSAL_DAG**
- Unified DAG with structure, dependencies, and equations
- Node types: Exogenous_Driver, Endogenous_Driver, Financial_Line_Item
- Equations must use PREV() for lagged access, GET() for intra-timestep
- Mutation Policy: Enrichment authorized (additive only) with RQ evidence

**A.5_GESTALT_IMPACT_MAP (GIM)**
- Map of exogenous driver assumptions
- Each driver: mode (DSL type), params, qualitative_thesis
- Qualitative thesis MUST include Variance Justification with percentile ranking if deviating from A.1 anchors

**A.6_DR_DERIVATION_TRACE**
- Derivation trace: RFR, ERP, X_Risk_Multiplier, DR_Static
- Justification narrative for Risk Multiplier
- Mutation Policy: FROZEN from BASE through entire pipeline

**A.7_LIGHTWEIGHT_VALUATION_SUMMARY**
- IVPS summary: IVPS, DR, Terminal_g, ROIC_Terminal, Current_Market_Price
- Implied multiples analysis
- Sensitivity analysis (tornado summary)
- Key forecast metrics and trajectory checkpoints (Y0, Y5, Y10, Y20)

**A.9_ENRICHMENT_TRACE**
- Executive synthesis
- Research synthesis (per-RQ summaries, cross-cutting themes, critical tensions)
- Conflict resolution log
- GIM changelog (every driver with: prior state, evidence synthesis, anchor reconciliation, decision, posterior state)
- DAG changelog (if any enrichment)
- KG changelog (if any Y0 data updates)
- Anchor changelog (if any base rate updates --- high bar)
- Boundary conditions (scenario exclusion check, economic governor check)
- CVR comparison (State 1 → State 2 bridge)

**A.10_SCENARIO_MODEL_OUTPUT**
- Metadata including base case reference
- Scenario definitions (up to 4): probability estimation, intervention definition, magnitude estimation
- Integration model: SSE constraints and execution results
- State enumeration: all 2^N states with probability and IVPS calculations
- Probabilistic valuation summary: E[IVPS], distribution statistics, distribution shape, visualization
- Analytical synthesis: executive summary, CVR state bridge, risk assessment, investment implications
- Trace documentation

## **B.4. Probability Estimation Protocol (Bayesian)**

**The Three-Step Protocol:**

**Step 1: Anchor (Establish Prior)**
- Select appropriate reference class
- Extract base rate from H.A.D. (Historical Analogue Data)
- Document: "In reference class [X], event occurs with base rate [Y%] based on [N] observations"
- Note sample size and recency; if N < 10 or data > 10 years old, acknowledge uncertainty

**Step 2: Deconstruct (Causal Decomposition)**
- Decompose scenario into prerequisite chain
- Express as: P(Scenario) = P(C₁) × P(C₂|C₁) × P(C₃|C₁,C₂) × ...
- Forces explicit reasoning about causal pathway

**Step 3: Update (Calculate Posterior)**
- Integrate company-specific evidence
- Document adjustments with citations
- Calculate final P(Scenario)

**Calibration Mandates:**
- If P > 70% (upside) or P < 10% (downside): Sanity check narrative required
- Independence Mandate: Estimate probabilities independently; handle correlations in SSE

**Common Errors to Flag:**
- Anchoring on management guidance (not base rates)
- Neglecting base rates
- Conjunction fallacy (P(A∩B) cannot exceed P(A))
- Availability bias

## **B.5. SSE Integration Methodology**

**Structured State Enumeration (SSE)** calculates the exact Joint Probability Distribution.

**Initialize-Filter-Renormalize Procedure:**

**Phase 1: Initialize**
- Calculate P_initial for all 2^N states
- Independent: P(State) = ∏P(active) × ∏(1-P(inactive))
- Handle causal dependencies if defined

**Phase 2: Filter**
- Eliminate infeasible states:
  - Mutual Exclusivity (MECE): States with multiple exclusive scenarios = infeasible
  - Economic Incompatibility: Defined pairs cannot co-occur
  - MANDATORY: BLUE_SKY and BLACK_SWAN must be incompatible

**Phase 3: Renormalize**
- RF = 1.0 / Σ(P_initial for feasible states)
- P_final = P_initial × RF for feasible; 0 for infeasible
- Validate: Σ(P_final) = 1.0

**State IVPS Calculation:**
- Additive Impact: IVPS(State) = IVPS_Base + Σ(IVPS_Impact for active scenarios)
- Limited Liability: IVPS_final = MAX(0.0, IVPS_raw)

**E[IVPS]:** Σ(P_final × IVPS_final) for all states

## **B.6. Key Methodological Mandates to Audit**

**From BASE:**
- Operational Primitive Mandate: Decompose beyond GAAP line items where data permits
- Adversarial De-Framing Mandate: Scrutinize management-selected metrics
- DAG Fidelity Doctrine: DAG granularity must inherit from Y0_data research

**From ENRICHMENT:**

- DR Revision Protocol Compliance: DR is presumptively stable from BASE, but ENRICHMENT 2.2.2e has conditional revision authority. Audit requirements:
  - If DR was modified: Verify revision was triggered by M-1/M-2 RQ findings revealing material risk factors not assessable from BASE documents
  - Verify explicit mapping to X multiplier component with quantified delta
  - Verify dr_changelog in A.9 documents prior/posterior X values with evidence justification
  - Apply adversarial calibration: DR revisions are stochastic and prone to motivated reasoning. Independently assess whether the cited evidence justifies the magnitude of revision.
  - If DR was NOT modified: Verify this was appropriate given RQ findings (no false negatives)

- SCM Stability: DAG enrichment rare, additive only
- Variance Mandate: Material deviations from anchors require explicit justification with percentile ranking
- Anti-Narrative Mandate: Don't force-fit research into pre-existing thesis
- Conflict Resolution Protocol: Reconciliation before rejection

**From SCENARIO:**
- 4-Scenario Limit: Max 4 scenarios prioritized by |P × M|
- Distributional Completeness: Must include upside and downside
- Holistic Impact: Interventions capture complete economic effect
- DR Overlay: Only for fundamental systematic risk changes (rare)

**DR Revision Audit Protocol (Checklist):**

1. **Extract DR Chain:** BASE DR → ENRICH DR (if revised) → SCENARIO DR overlays (if any)

2. **For Each Transition:**
   - Was revision justified per protocol? (RQ citation, X component mapping, quantified delta)
   - Is the magnitude calibrated? (Compare to base rate adjustments for similar risk factors)
   - Does the dr_changelog documentation meet trace requirements?

3. **Adversarial Calibration:**
   - Would a skeptical analyst accept this DR given the evidence?
   - Is there anchoring on prior DR masking legitimate revision need?
   - Is there motivated reasoning inflating/deflating DR to fit a thesis?

4. **Cross-Stage Consistency:**
   - Is the DR used in SCENARIO kernel execution consistent with ENRICH output?
   - Are any SCENARIO DR overlays (rare) properly justified as systematic risk changes?

## **B.7. Output Guidance**

**Priority Levels:**
- CRITICAL: Materially undermines confidence in E[IVPS]; should block finalization without resolution
- HIGH: Significant concern requiring explicit address in INTEGRATION
- MEDIUM: Notable issue providing useful context

**Pipeline Fit Grades:**
- A: Well-suited to methodology; minimal unmodeled factors
- B: Some blind spots; manageable with noted caveats
- C: Material blind spots; interpret with significant caution
- D: Multiple severe blind spots; methodology may be inappropriate
- F: Fundamental mismatch; recommend alternative analysis approach

*END OF G3 SILICON COUNCIL 2.2.2e NORMATIVE DEFINITIONS REFERENCE*
