# G3BASE 2.2.3e: Normative Definitions & DSL (Appendix B)

> **Version:** 2.2.3e
> **Parent Document:** G3BASE_2.2.3e_PROMPT.md
> **Patch:** DR recalibration (global universe), terminal g from topline

This file defines the Assumption DSL, execution topology rules, and valuation engine specifications that the kernel requires.

---

## B.1. Assumption DSL Definitions (Strict Kernel Compliance)

The Kernel supports **ONLY** the following four propagation modes. Usage of unsupported modes (e.g., S_CURVE) will result in a critical execution failure.

### STATIC

- **Behavior:** The value remains constant from Y1 through Y20.
- **Required Param:** `value` (float)

**Example:**
```json
{
  "mode": "STATIC",
  "params": {"value": 0.35}
}
```

### LINEAR_FADE

- **Behavior:** Linearly interpolates from `start_value` to `end_value` over `fade_years`. Holds `end_value` thereafter.
- **Required Params:** `start_value` (float), `end_value` (float), `fade_years` (int)

**Example:**
```json
{
  "mode": "LINEAR_FADE",
  "params": {
    "start_value": 0.25,
    "end_value": 0.10,
    "fade_years": 10
  }
}
```

### CAGR_INTERP

- **Behavior:** Compounds the Y0 value (found in `core_data.Y0_data`) by a growth rate that interpolates from `start_cagr` to `end_cagr` over `interp_years`.
- **Required Params:** `start_cagr` (float), `end_cagr` (float), `interp_years` (int)
- **Critical:** The driver must have a corresponding Y0 value in A.2 `core_data.Y0_data`

**Example:**
```json
{
  "mode": "CAGR_INTERP",
  "params": {
    "start_cagr": 0.30,
    "end_cagr": 0.03,
    "interp_years": 15
  }
}
```

### EXPLICIT_SCHEDULE

- **Behavior:** Manually overrides specific years using a dictionary mapping.
- **Required Params:** `schedule` (Dictionary: `{'1': val, '2': val...}`)
- **Note:** Gaps are interpolated. Years after the schedule ends hold the last value.

**Example:**
```json
{
  "mode": "EXPLICIT_SCHEDULE",
  "params": {
    "schedule": {
      "1": 100,
      "2": 150,
      "5": 300,
      "10": 500
    }
  }
}
```

---

## B.2. Execution Topology (DAG Compliance)

The CVR Kernel executes the SCM using a **topological sort**. The following rules apply to the equations in A.3_CAUSAL_DAG:

### The PREV() Rule (Inter-Temporal)

To access a variable from the **previous year** ($t-1$), use `PREV('Variable_Name')`.

- **Mandatory:** All "Stock" variable updates (e.g., Invested Capital accumulation) must use PREV.

**Example:**
```python
# Invested Capital accumulates via reinvestment
"equation": "PREV('Invested_Capital') + GET('Reinvestment')"
```

### The GET() Rule (Intra-Temporal)

To access a variable from the **current year** ($t$) that has already been calculated, use `GET('Variable_Name')`.

- **Cycle Warning:** Intra-temporal dependencies must be acyclic. (e.g., A cannot rely on B if B relies on A in the same timestep).

**Example:**
```python
# NOPAT depends on current-year EBIT
"equation": "GET('EBIT') * (1 - GET('Tax_Rate'))"
```

### Equation Syntax Reference

| Function | Description | Example |
|----------|-------------|---------|
| `GET('X')` | Current year value of X | `GET('Revenue')` |
| `PREV('X')` | Previous year value of X | `PREV('Invested_Capital')` |
| Arithmetic | Standard Python operators | `GET('A') * GET('B') + 100` |
| Conditionals | If-else expressions | `GET('A') if GET('B') > 0 else 0` |

---

## B.3. Valuation Engine & Equity Bridge

The Kernel executes a simplified **Adjusted Present Value (APV)** calculation.

### Discount Rate (DR)

#### Discount Rate Philosophy (READ THIS FIRST)

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

#### Currency-Matched RFR (MANDATORY)

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

#### Formula

$$DR = RFR + (ERP \times X)$$

Where ERP = 5.0% and X ∈ [0.5, 2.0].

#### Risk Multiplier (X) - Global Universe Calibration

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

#### Calibration Anchors

| Security | X | Rationale |
|----------|---|-----------|
| Waste Management (WM) | 0.5 | Quasi-monopoly, stable FCF, defensive |
| Walmart (WMT) | 0.65 | Scale moat, but retail disruption risk |
| Microsoft (MSFT) | 0.7 | Diversified, dominant, recurring revenue |
| Alphabet (GOOGL) | 0.85 | Tech risk, but dominant, profitable |
| Caterpillar (CAT) | 0.9 | Typical S&P 500 industrial |
| Typical Russell 2000 | 1.1 | Average for global investable universe |
| Typical MSCI EM | 1.4 | Governance, currency, less transparency |
| Small EM growth | 1.7 | High execution and macro risk |
| Speculative pre-revenue | 1.9-2.0 | Near-zero margin of safety |

**Sanity check:** If your X > 1.5, the company should have clear pathological risk factors (unprofitable, early stage, poor unit economics, governance red flags).

### Explicit Period Value

The sum of discounted Unlevered FCF for Y1–Y20:

$$PV_{Explicit} = \sum_{t=1}^{20} \frac{FCF_t}{(1 + DR)^t}$$

### Terminal Value (TV)

Calculated using the **Value Driver Formula**:

$$TV = \frac{NOPAT_{Y21} \times (1 - \frac{g}{r})}{DR - g}$$

Where:
- $r$ = ROIC Anchor from A.1 epistemic anchors (industry median, NOT modeled Y20 ROIC)
- $g$ = Terminal Growth derived from **topline growth** (average of Revenue and EBIT growth rates)

#### Terminal Growth Constraints (Patch 2.2.3e)

Terminal g is derived from topline growth (Revenue, EBIT), NOT from ROIC/NOPAT:
1. Calculate average of last 3 years' Revenue growth and EBIT growth
2. Cap at GDP × 1.4 (3.5%) - allows share-gainers while preventing excess
3. Also cap at RFR if available
4. Final sanity check: g must be < DR

**Rationale:** Revenue and EBIT growth are modeled reliably. IC (Invested Capital) is accounting-dependent, making ROIC unreliable for terminal value calculations.

### The Equity Bridge (Y0 Static)

$$Enterprise\ Value = PV(Explicit\_FCF) + PV(TV)$$

$$Equity\ Value = Enterprise\ Value - Total\_Debt_{Y0} + Excess\_Cash_{Y0} - Minority\_Interest_{Y0}$$

**Note:** The Kernel uses **Static Y0 Balance Sheet** items for the bridge. It does *not* model dynamic debt paydown or interest tax shields.

### Required Y0 Balance Sheet Items

The following items **must** be present in `A.2.core_data.Y0_data` for the Equity Bridge:

| Item | Description |
|------|-------------|
| `Total_Debt` | Total debt for Equity Bridge |
| `Excess_Cash` | Cash in excess of operating needs |
| `Minority_Interest` | Non-controlling interests (if applicable) |

---

## B.4. Validation Checklist (Pre-Emission)

Before emitting artifacts, verify:

1. **DAG Coverage:** Every node with a non-empty equation references only nodes that exist in A.3
2. **GIM-DAG Alignment:** Every Exogenous_Driver in A.3 has a corresponding entry in A.5
3. **CAGR_INTERP Validity:** All drivers using CAGR_INTERP have Y0 values in A.2
4. **DR Consistency:** A.6 uses RFR and ERP values from A.2.market_context
5. **Equation Syntax:** All equations use only GET(), PREV(), and valid Python arithmetic
6. **No Cycles:** Intra-temporal dependencies are acyclic
