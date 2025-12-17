# G3BASE 2.2.2e: Normative Definitions & DSL (Appendix B)

> **Version:** 2.2.2e
> **Parent Document:** G3BASE_2.2.2e_PROMPT.md

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

$$DR = RFR + (ERP \times X)$$

- **X (Risk Multiplier):** A qualitative assessment (0.5 to 2.2) derived from the Analysis narratives.

| X Range | Risk Profile |
|---------|--------------|
| 0.5 - 0.8 | Low risk (stable, profitable, low leverage) |
| 0.9 - 1.2 | Average risk |
| 1.3 - 1.6 | Above average risk |
| 1.7 - 2.2 | High risk (unprofitable, high leverage, early stage) |

### Explicit Period Value

The sum of discounted Unlevered FCF for Y1–Y20:

$$PV_{Explicit} = \sum_{t=1}^{20} \frac{FCF_t}{(1 + DR)^t}$$

### Terminal Value (TV)

Calculated using the **Value Driver Formula**:

$$TV = \frac{NOPAT_{Y21} \times (1 - \frac{g}{r})}{DR - g}$$

Where:
- $r$ = Terminal ROIC (converges to Y20 ROIC)
- $g$ = Terminal Growth (capped at RFR)

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
