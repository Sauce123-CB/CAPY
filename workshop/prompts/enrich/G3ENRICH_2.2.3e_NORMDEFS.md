# G3ENRICH 2.2.3e: Normative Definitions & DSL (Appendix B)

> **Version:** 2.2.3e
> **Parent Document:** G3ENRICH_2.2.3e_PROMPT.md
> **Patch:** DR recalibration (global universe), terminal g from topline

This file defines the Financial Definitions, Assumption DSL, and execution specifications that the ENRICHMENT kernel requires.

---

## B.1. Financial Definitions and Formulas

The following definitions are normative for all CVR calculations. They align with G3BASE 2.2.2e.

### 1. EBIT (Earnings Before Interest and Taxes)
   * Definition: Operating income MUST include Stock-Based Compensation (SBC) as an expense.
   * Rationale: SBC is a real economic cost representing dilution of existing shareholders.

### 2. NOPAT (Net Operating Profit After Tax)
   * Formula: NOPAT = EBIT × (1 - Tax_Rate)

### 3. Invested Capital (IC)
   * Definition: The total capital deployed in operating assets.
   * Typical Calculation: Operating Assets - Operating Liabilities, or equivalently, Equity + Net Debt (adjusted for non-operating items).

### 4. ROIC (Return on Invested Capital)
   * Formula: ROIC = NOPAT / PREV(Invested_Capital)
   * Timing Mandate: MUST use Beginning-of-Period (BOP) Invested Capital via PREV() function.

### 5. Reinvestment
   * Formula: Reinvestment = Δ Invested_Capital = IC(t) - IC(t-1)

### 6. Reinvestment Rate (RR)
   * Formula: RR = Reinvestment / NOPAT
   * Constraint: Bounded [0, 1] for steady-state; can exceed 1.0 during high-growth phases.

### 7. FCF (Unlevered Free Cash Flow)
   * Formula: FCF_Unlevered = NOPAT - Reinvestment

### 8. Growth (g) — The Value Driver Formula
   * Formula: g = ROIC × RR
   * Economic Interpretation: Sustainable growth rate consistent with reinvestment and returns.
   * Terminal Constraint: Terminal g MUST be < DR. Recommended ceiling: Long-term nominal GDP growth (2-4%).

### 9. Timing Convention Mandate (DAG Compliance)
   * The PREV() Rule: Calculations dependent on prior period balances MUST use PREV('Variable_Name').
   * Mandatory Applications: ROIC (uses PREV(Invested_Capital)), any stock-variable updates.
   * The GET() Rule: Intra-timestep access to already-calculated variables uses GET('Variable_Name').

### 10. Valuation Methodology (APV, 20-Year Explicit, Static DR)
    * Approach: Adjusted Present Value (APV) is mandated.
    * Forecast Horizon: 20-year explicit forecast.
    * Discount Rate: Static DR applied to all streams.
    * Terminal Value: Gordon Growth Model: TV = FCF_Y21 / (DR - g_terminal)
    * Equity Bridge: Equity_Value = Enterprise_Value - Net_Debt_Y0
    * IVPS: Equity_Value / Shares_Out_Diluted_TSM

### 11. ATP Mandate (Accounting Translation Protocol)
    * Inherited Constraint: All financial inputs in A.2 reflect ATP-reconciled economic definitions established in BASE (per BASE P1.5).
    * ENRICHMENT Responsibility: When updating Y0_data based on RQ evidence, ensure updates maintain consistency with the accounting_translation_log. If RQ evidence reveals a superior economic interpretation, document the change in A.9 kg_changelog with explicit reference to the ATP entry being superseded.
    * Normative Primacy: The normative definitions in this section (e.g., EBIT includes SBC) take precedence over raw reported figures, regardless of how metrics are labeled in source documents.

### 12. Tax Rate Sourcing
    * Tax_Rate: Exogenous driver or static assumption in GIM.
    * Default: Marginal statutory rate unless company-specific effective rate is justified with citation.
    * Treatment: Must be defined in A.5 GIM if variable; otherwise static in DAG equation.

### 13. Y0 Basis Convention
    * Y0_data reflects the most recent completed fiscal year unless explicitly noted as LTM (Last Twelve Months).
    * If LTM is used, document in A.2 metadata with period end date.

### 14. Negative Terminal ROIC Handling
    * If terminal ROIC ≤ 0, assume g = 0 and RR = 0 (no value-creating reinvestment).
    * Terminal value calculated using zero-growth perpetuity: TV = NOPAT_T / DR.
    * Document in A.9 boundary_conditions.economic_governor_check.

---

## B.2. Assumption DSL Definitions (Expanded for ENRICHMENT)

The DSL (Domain-Specific Language) defines how an exogenous driver assumption evolves from Year 1 (Y1) to Year 20 (Y20). Y0 represents the historical starting value from A.2_ANALYTIC_KG.

The ENRICHMENT Kernel (G3_2.2.2e) supports six propagation modes:

---

### MODE: STATIC

**Behavior:** The value remains constant for all forecast years.

**Required Params:**
  - `value` (float): The constant value applied Y1-Y20.

**Example:**
```json
{
  "mode": "STATIC",
  "params": {"value": 0.21}
}
```

---

### MODE: LINEAR_FADE

**Behavior:** Linearly interpolates from start_value to end_value over fade_years. Holds end_value thereafter.

**Required Params:**
  - `start_value` (float): Initial value at Y1. If omitted, Y0 from KG is used.
  - `end_value` (float): Target value at completion of fade.
  - `fade_years` (int): Number of years for the fade (1-20).

**Mechanics:**
  - Annual step = (end_value - start_value) / fade_years
  - Value at year t (t ≤ fade_years): start_value + (step × t)
  - Value at year t (t > fade_years): end_value

**Example:**
```json
{
  "mode": "LINEAR_FADE",
  "params": {"start_value": 0.25, "end_value": 0.15, "fade_years": 10}
}
```

---

### MODE: CAGR_INTERP

**Behavior:** Compounds from start_value using a growth rate that interpolates from start_cagr to end_cagr over interp_years.

**Required Params:**
  - `start_cagr` (float): Initial annual growth rate (e.g., 0.15 for 15%).
  - `end_cagr` (float): Terminal annual growth rate.
  - `interp_years` (int): Years over which the CAGR fades (1-20).

**Mechanics:**
  - The growth rate linearly fades from start_cagr to end_cagr over interp_years.
  - Year t growth rate (t ≤ interp_years): start_cagr + ((end_cagr - start_cagr) × t / interp_years)
  - Year t growth rate (t > interp_years): end_cagr
  - Value compounds: Value(t) = Value(t-1) × (1 + growth_rate(t))
  - Y0 value sourced from KG (core_data.Y0_data).

**Example:**
```json
{
  "mode": "CAGR_INTERP",
  "params": {"start_cagr": 0.20, "end_cagr": 0.03, "interp_years": 15}
}
```

---

### MODE: S_CURVE

**Behavior:** Models logistic (S-curve) growth—slow start, acceleration, deceleration toward saturation. Useful for market penetration, adoption dynamics, or margin expansion with natural ceilings.

**Required Params:**
  - `start_value` (float): Initial value at Y0/Y1. If omitted, Y0 from KG is used.
  - `saturation_value` (float): The asymptotic ceiling (or floor) the curve approaches.
  - `inflection_year` (float): The year at which growth is fastest (midpoint of the S).
  - `steepness` (float): Controls the rate of transition (higher = sharper S). Typical range: 0.3 to 1.5.

**Mechanics:**
  - Uses logistic function centered on inflection_year.
  - Formula: Value(t) = start_value + (saturation_value - start_value) / (1 + exp(-steepness × (t - inflection_year)))
  - At t << inflection_year: Value ≈ start_value
  - At t = inflection_year: Value ≈ midpoint between start and saturation
  - At t >> inflection_year: Value ≈ saturation_value

**Example:**
```json
{
  "mode": "S_CURVE",
  "params": {"start_value": 0.05, "saturation_value": 0.35, "inflection_year": 8, "steepness": 0.6}
}
```

---

### MODE: MULTI_STAGE_FADE

**Behavior:** Allows defining distinct phases with different fade dynamics. Useful for complex trajectories (e.g., rapid expansion phase followed by gradual maturation, then terminal stability).

**Required Params:**
  - `stages` (array): Ordered list of stage definitions. Each stage:
    - `end_year` (int): Year at which this stage completes.
    - `end_value` (float): Value at completion of this stage.
    - `interpolation` (string, optional): "LINEAR" (default) or "CAGR". Method for this stage.

**Mechanics:**
  - Stages are processed sequentially.
  - Each stage starts from the end_value of the previous stage (or Y0 for the first stage).
  - Within each stage, values interpolate according to the specified method.
  - After the final stage, the last end_value is held constant through Y20.

**Example:**
```json
{
  "mode": "MULTI_STAGE_FADE",
  "params": {
    "stages": [
      {"end_year": 5, "end_value": 0.30, "interpolation": "LINEAR"},
      {"end_year": 12, "end_value": 0.22, "interpolation": "LINEAR"},
      {"end_year": 20, "end_value": 0.18, "interpolation": "LINEAR"}
    ]
  }
}
```

---

### MODE: EXPLICIT_SCHEDULE

**Behavior:** Manually specifies values for designated years. Gaps are linearly interpolated. Years after the schedule hold the last specified value.

**Required Params:**
  - `schedule` (object): Dictionary mapping year numbers (as strings) to values.

**Mechanics:**
  - Specified years take the explicit value.
  - Gaps between specified years are linearly interpolated.
  - Years after the last specified year hold that final value.

**Example:**
```json
{
  "mode": "EXPLICIT_SCHEDULE",
  "params": {
    "schedule": {
      "1": 0.25,
      "3": 0.22,
      "5": 0.20,
      "10": 0.18,
      "20": 0.15
    }
  }
}
```

---

## B.3. Discount Rate Methodology

### Discount Rate Philosophy (READ THIS FIRST)

This DR framework reflects the preferences of a concentrated portfolio
practitioner (~20 positions), NOT institutional WACC or CAPM theory.

**Why this matters:**
- We are NOT trying to calculate the "theoretically correct" discount rate
- We ARE encoding a specific utility function: lower required returns for
  stable names, higher for volatile/crisis-correlated names
- The X multiplier [0.5, 2.0] maps directly to this preference function
- Size premiums, EM premiums, illiquidity premiums are NOT added separately —
  they are already reflected in RFR (for country risk) and X (for company risk)

**DO NOT "improve" this formula.** Adding extra premia, adjusting for factors
not specified, or using institutional WACC logic will produce incorrect results.

### Currency-Matched RFR (MANDATORY)

RFR MUST match the reporting currency of the financials. Use WebSearch to
look up the current 10-year government bond yield for the reporting currency:

| Reporting Currency | RFR Benchmark |
|--------------------|---------------|
| USD | US Treasury 10Y |
| BRL | Brazil Government Bond 10Y |
| EUR | German Bund 10Y |
| GBP | UK Gilt 10Y |
| JPY | Japan Government Bond 10Y |

**Why currency-matched RFR:**
- Country/sovereign risk is already priced into local government bonds
- Adding separate EM/country premia would double-count this risk
- The formula DR = RFR + (ERP × X) only produces correct results with matched currency

### Formula

**Formula:** DR = RFR + (ERP × X)

Where ERP = 5.0% and X ∈ [0.5, 2.0].

**Components:**
  - RFR (Risk-Free Rate): 10-Year government bond yield in the REPORTING CURRENCY (see table above).
  - ERP (Equity Risk Premium): Standardized at 5.0% per the G3 ERP Convention Mandate.
  - X (Risk Multiplier): Qualitative assessment of company-specific risk relative to the **global universe of 50,000+ securities** (NOT S&P 500).

### Risk Multiplier (X) - Global Universe Calibration

**CRITICAL:** Calibrate X against the universe of **50,000+ globally traded public securities**, NOT the S&P 500 or any curated index of large-cap US stocks.

The S&P 500 represents the LOW-RISK tail of the global distribution. A typical S&P 500 company should receive X ≈ 0.8-0.9, not X ≈ 1.0.

| X Range | Risk Profile | Calibration Examples |
|---------|--------------|----------------------|
| 0.5 - 0.6 | Very low risk | Waste Management, utilities, quasi-monopolies with stable growing FCF |
| 0.6 - 0.8 | Low risk | Walmart, Microsoft, Apple - large diversified companies with moats |
| 0.8 - 1.0 | Below average | Google, typical S&P 500 industrial (Caterpillar, Honeywell) |
| 1.0 - 1.2 | Average (global) | Typical Russell 2000 company, profitable mid-cap growth |
| 1.2 - 1.5 | Above average | Small-cap with concentration risk, typical MSCI EM constituent |
| 1.5 - 1.8 | High risk | Small emerging market growth, unprofitable growth, early-stage |
| 1.8 - 2.0 | Very high risk | Speculative (quantum computing hype, poor-prospect biotech, near-fraud) |

**Derivation:** Determined in BASE stage. ENRICHMENT has revision authority per P2 DR Revision Protocol if RQ evidence reveals material risk factors not assessable from BASE source documents.

**Sanity check:** If your X > 1.5, the company should have clear pathological risk factors (unprofitable, early stage, poor unit economics, governance red flags).

---

## B.4. Execution Topology (DAG Compliance)

The CVR Kernel executes the SCM using topological sort to respect causal dependencies.

**DAG Rules:**

1. **PREV() Rule (Inter-Temporal):** Access prior year value with PREV('Variable_Name').
   * Mandatory for stock variables and calculations requiring BOP values.

2. **GET() Rule (Intra-Temporal):** Access current year value (already calculated in this timestep) with GET('Variable_Name').
   * Requires acyclic dependencies within each timestep.

3. **Cycle Prohibition:** Circular dependencies within a single timestep are forbidden and will cause execution failure.

**Equation Syntax:**
  - Standard Python arithmetic operators: +, -, *, /, **
  - Functions: PREV('Var'), GET('Var'), MAX(a, b), MIN(a, b), ABS(x)
  - Constants: Direct numeric values
  - References: Variable names (resolved from current timestep calculation order)

---

## B.5. Terminal Value and Economic Constraints

**Terminal Value Derivation:**
  - Method: Value Driver Formula (Perpetuity with reinvestment)
  - Formula: TV = NOPAT_Y21 × (1 - g/r) / (DR - g)
  - Where:
    - r = ROIC Anchor from A.1 epistemic anchors (NOT modeled Y20 ROIC)
    - g = Terminal Growth derived from **topline growth** (average of Revenue and EBIT growth)

### Terminal Growth Constraints (Patch 2.2.3e)

Terminal g is derived from topline growth (Revenue, EBIT), NOT from ROIC/NOPAT:
1. Calculate average of last 3 years' Revenue growth and EBIT growth
2. Cap at GDP × 1.4 (3.5%) - allows share-gainers while preventing excess
3. Also cap at RFR if available
4. Final sanity check: g must be < DR

**Rationale:** Revenue and EBIT growth are modeled reliably. IC (Invested Capital) is accounting-dependent, making ROIC unreliable for terminal value calculations.

**Economic Governor Constraints:**
  - g_terminal < DR: Mandatory. Violation causes Kernel failure.
  - g_terminal ≤ GDP × 1.4 (3.5%): Hard cap for terminal growth.
  - Terminal ROIC: Use ROIC_anchor from A.1 (industry median), not modeled ROIC.
  - Reinvestment Rate = g / ROIC_anchor: Must be ≤ 100%.

**Implied Constraint:**
  - The model must be internally consistent. Conflicting terminal assumptions will produce implausible results flagged in the Post-Execution Reality Check.

---

## B.6. ENRICHMENT-Specific Constraints Summary

The following constraints are specific to the ENRICHMENT stage:

| Artifact | Mutation Policy | Constraint |
|----------|-----------------|------------|
| A.1 EPISTEMIC_ANCHORS | Refinement Authorized | High burden of proof; requires superior third-party data |
| A.2 ANALYTIC_KG | Update Authorized | Document in A.9 kg_changelog |
| A.3 CAUSAL_DAG | Enrichment Authorized | Additive only; requires RQ evidence; document in A.9 dag_changelog |
| A.5 GESTALT_IMPACT_MAP | Update Required | Core refinement target |
| A.6 DR_DERIVATION_TRACE | Revision Authorized | High burden of proof; requires RQ evidence of material risk factors; document in A.9 dr_changelog |
| A.7 LIGHTWEIGHT_VALUATION_SUMMARY | Recalculated | Kernel output |
| A.9 ENRICHMENT_TRACE | Created | Full audit trail including dr_changelog |

**Scenario Exclusion Mandate:**
  - Discrete probabilistic scenarios (M-3a/M-3b) are reserved for SSE stage.
  - Exception: P=1.0 events (virtual certainty) must be incorporated into Base Case.

**Economic Governor Mandate:**
  - All refinements must maintain g < DR at terminal.
  - Implausible ROIC trajectories require explicit justification (Narrative N3).
