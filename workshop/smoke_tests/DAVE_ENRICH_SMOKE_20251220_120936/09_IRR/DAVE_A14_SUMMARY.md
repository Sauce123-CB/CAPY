# DAVE Inc. - IRR Analysis (A.14)

## Executive Summary

| Metric | Value |
|--------|-------|
| Current Price | $215.25 |
| E[IVPS] State 4 | $206.34 |
| Premium/(Discount) | 4.3% |
| DR (Static) | 13.25% |
| **E[IRR]** | **27.1%** |
| Null Case IRR | 12.1% |
| P(IRR > 15%) | 83.9% |

## IRR Distribution

| P10 | P25 | P50 | P75 | P90 |
|-----|-----|-----|-----|-----|
| 10.0% | 27.2% | 27.2% | 31.8% | 39.9% |

## Transition Factor Analysis

| Metric | Value |
|--------|-------|
| Market Multiple T0 | 20.01x |
| DCF Multiple T0 | 19.18x |
| Market/DCF Ratio | 1.043 |
| Transition Factor | 0.716 |
| DCF Multiple T1 | 13.73x |
| Market Multiple T1 (Null) | 14.32x |

## Null Case Interpretation

> Market priced near DCF fair value (ratio=1.04). Null IRR of 12.1% appropriately approximates DR of 13.2%.

## Return Attribution

| Component | Contribution |
|-----------|-------------|
| Null Case IRR | 12.1% |
| Scenario Resolution | +15.0% |
| **Total E[IRR]** | **27.1%** |

## Fork Summary (Top 5 by Probability)

| Fork | P | Price T1 | IRR |
|------|---|----------|-----|
| S1_REG_SETTLEMENT + S3_BANK_TRANSITION | 37.3% | $273.84 | 27.2% |
| S3_BANK_TRANSITION | 13.8% | $281.51 | 30.8% |
| S1_REG_SETTLEMENT | 11.8% | $236.85 | 10.0% |
| S1+S3+S4 | 9.3% | $283.80 | 31.8% |
| S1+S2+S3 | 7.1% | $301.03 | 39.9% |

## Sanity Checks

- Value Trap Test: PASS: Returns exceed hurdle even without multiple expansion
- Fork Independence: WARNING: Fork multiples cluster tightly (CV=0.038). Possible correlation bias.
- Flags: ['All fork IRRs positive (optimism check)']

---

## Scenario Inputs (from A.13)

| Scenario | P | IVPS Impact | ρ | Effective Impact |
|----------|---|-------------|---|------------------|
| S1_REG_SETTLEMENT | 73% | -$52.29 | 0.25 | -$13.07 |
| S2_BNPL_SUCCESS | 16% | +$30.59 | 0.30 | +$9.18 |
| S3_BANK_TRANSITION | 76% | +$42.59 | 0.35 | +$14.91 |
| S4_ACQUISITION | 20% | +$40.00 | 0.15 | +$6.00 |
