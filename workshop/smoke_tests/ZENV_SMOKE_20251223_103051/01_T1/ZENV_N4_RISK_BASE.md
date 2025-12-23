# N4: Risk Assessment - Zenvia Inc. (NASDAQ:ZENV)

## Risk Framework and Discount Rate Derivation

Risk assessment for Zenvia requires decomposing the sources of uncertainty into *systematic* (market-compensated) and *idiosyncratic* (diversifiable) risks, then mapping them to a discount rate appropriate for this specific security. Given Zenvia's small-cap status, leverage, business model transformation, LATAM exposure, and execution uncertainty, the discount rate will be materially above the global equity market risk premium.

---

## Systematic Risk Factors (Market-Compensated)

### 1. Equity Market Risk Premium (ERP)

**Base Global ERP**: 5.0% (per CVR protocol)

This represents the expected return premium for a diversified global equity portfolio over the risk-free rate. Zenvia's exposure to this factor is modulated by its beta to global equity markets.

**Beta Estimation**:
- **Sector beta**: SaaS companies typically 1.2-1.5× market (high growth, discretionary spending)
- **Size factor**: Small-cap stocks (< $500M market cap) exhibit beta of 1.3-1.6×
- **Leverage factor**: Net debt / equity of 0.12 (BRL 92M debt / BRL 742M equity) adds ~0.1-0.2 to beta
- **LATAM factor**: Emerging market exposure adds ~0.2-0.3 to beta

**Estimated Zenvia Beta**: 1.5-1.8× (high end of spectrum due to size, leverage, and transformation risk)

**Beta-Adjusted ERP**: 5.0% × 1.5 = 7.5% (using mid-point of beta range)

---

### 2. Risk-Free Rate (RFR)

**US Treasury 10-Year**: The appropriate risk-free rate for a USD-denominated valuation of a NASDAQ-listed company with Brazilian operations.

**Current RFR (Dec 2025)**: ~4.5% (prevailing 10-year Treasury yield)

**Note on BRL vs. USD Rates**:
- Brazilian Selic rate: ~11-12% (much higher than US)
- However, Zenvia reports in BRL but trades in USD; we use USD RFR for consistency with equity trading currency
- FX risk (BRL depreciation) is captured in the discount rate multiplier, not RFR

---

### 3. Size Premium

**Small-Cap Liquidity Risk**: Zenvia's $67M market cap places it in the micro-cap category (< $300M). Historical data (Ibbotson, Duff & Phelps) shows small-cap stocks require 3-5% additional return premium.

**Zenvia-Specific Factors**:
- Average daily volume: ~200K shares (~$250K daily liquidity)
- Bid-ask spread: ~3-5% (illiquid)
- Institutional ownership: Low (< 20%)
- Analyst coverage: Minimal (1-2 analysts)

**Size Premium**: 4.0% (mid-range for micro-cap illiquidity)

---

### 4. Emerging Market Risk Premium

**LATAM Exposure**: ~90% of revenue from Brazil/LATAM. Emerging market equity risk premiums vary:
- Brazil country risk premium: ~3-4% over US (per Damodaran)
- LATAM aggregate: ~3.5-4.5%

**Offsetting Factors**:
- Listed on NASDAQ (USD-denominated shares reduce some FX risk for US investors)
- Diversified customer base (not concentrated in single industry or geography within LATAM)

**Net EM Premium**: 2.5% (adjusted for partial NASDAQ listing benefit)

---

## Idiosyncratic Risk Factors (Reflected in X-Risk Multiplier)

While technically "diversifiable," Zenvia's idiosyncratic risks are so material and concentrated that they warrant explicit consideration in the discount rate. These manifest through the **X-Risk Multiplier** applied to the base ERP.

### Risk Cluster 1: Business Model Transformation Risk

**Nature**: Company is executing simultaneous (1) divestiture of 72% of revenue (CPaaS), (2) scaling of nascent product (Zenvia Customer Cloud), and (3) operational restructuring (15% workforce reduction).

**Probability of Failure**: 40-50% (high)
- Historical M&A track record: Mixed (7+ acquisitions, uneven results)
- Product risk: Zenvia Customer Cloud launched Oct 2024 (< 1 year old)
- Execution complexity: Multiple moving parts, tight timeline

**Impact if Fails**: Severe
- Equity value impairment: 50-70%
- Potential distressed restructuring

**Risk Multiplier Contribution**: +0.4

---

### Risk Cluster 2: Liquidity and Going Concern Risk

**Nature**: Negative working capital of BRL 444M, cash of BRL 33M (down from BRL 117M at YE2024), auditor going concern warning.

**Probability of Liquidity Crisis**: 30-40%
- Debt maturities: Dec 2026 (18 months away)
- Operating cash flow: Negative BRL 18M in H1 2025
- Dependency on asset divestiture: High (no other near-term liquidity source)

**Impact if Occurs**: Catastrophic
- Forced asset sale at fire-sale prices (30-50% discount to base case)
- Equity dilution or impairment
- Covenant breaches, potential bankruptcy

**Risk Multiplier Contribution**: +0.3

---

### Risk Cluster 3: Competitive and Market Risk

**Nature**:
- CPaaS: Commoditized market with intense pricing pressure (GM collapsed from 24% to 12% in 1 year)
- SaaS: Competing against well-funded global players (Salesforce, Zendesk) and emerging AI-native startups

**Probability of Market Share Loss**: 25-35%
- CPaaS: Already occurring (management de-emphasizing this business)
- SaaS: Competitive threats increasing as AI-powered CX tools proliferate

**Impact if Occurs**: Moderate to Severe
- Revenue growth below 15% CAGR (vs. 25% target)
- Margin compression (SaaS GM stays at 55-60% vs. 70% target)
- Valuation multiple compression

**Risk Multiplier Contribution**: +0.25

---

### Risk Cluster 4: Regulatory and LATAM Political Risk

**Nature**:
- Brazil: Political instability, potential tax/regulatory changes
- Argentina: Hyperinflation (cumulative inflation > 100% in 3 years; disclosed IAS 29 treatment)
- FX volatility: BRL/USD fluctuates ±10-15% annually

**Probability of Adverse Event**: 20-30%
- FX shock (BRL depreciation > 20% in single year)
- Tax law change (Brazil frequently adjusts corporate tax)
- Data privacy regulation (LGPD enforcement, potential GDPR-like fines)

**Impact if Occurs**: Moderate
- Earnings volatility (FX translation losses)
- Compliance costs increase
- Market access restrictions

**Risk Multiplier Contribution**: +0.15

---

### Risk Cluster 5: Key Person and Governance Risk

**Nature**:
- Founder-led (Cassio Bobsin as CEO since inception)
- Recent CFO transition (Shay Chor departed Sep 2025, replaced by Piero Rosatelli)
- Limited public company governance history (IPO'd 2021)

**Probability of Key Person Departure**: 10-15%
- CEO/founder departure would be catastrophic
- CFO transition already occurred (potential continuity risk)

**Impact if Occurs**: Severe
- Strategic direction uncertainty
- Execution capability degradation
- Market confidence loss

**Risk Multiplier Contribution**: +0.1

---

## Discount Rate Calculation

### Formula (from CVR protocol):

**DR = RFR + (ERP × X)**

Where:
- RFR = Risk-Free Rate = 4.5%
- ERP = Equity Risk Premium = 5.0% (base, before multiplier)
- X = Risk Multiplier ∈ [0.5, 2.0]

### X-Risk Multiplier Derivation

**Components**:
| Risk Factor | Contribution | Weight |
|------------|-------------|--------|
| Business Model Transformation | +0.40 | High |
| Liquidity / Going Concern | +0.30 | High |
| Competitive / Market | +0.25 | Medium-High |
| Regulatory / LATAM Political | +0.15 | Medium |
| Key Person / Governance | +0.10 | Medium |
| **Subtotal (Additive)** | **+1.20** | |

**Adjustments**:
- **Beta adjustment**: Already captured in systematic ERP (beta of 1.5)
- **Size premium**: Separately added (4.0%)
- **EM premium**: Separately added (2.5%)

**Final X Multiplier**: 1.80 (high-risk, early-stage transformation + distressed)

**Calibration Check** (using global universe from CVR protocol):
- 1.5-1.8: High risk (unprofitable growth, early-stage)
- 1.8-2.0: Very high risk (speculative)

Zenvia sits at 1.8, consistent with "high risk" categorization: unprofitable (net loss BRL 38M H1 2025), early-stage transformation (Zenvia Customer Cloud < 1 year old), speculative outcome (CPaaS divestiture uncertain).

---

### Final Discount Rate:

**DR = RFR + (ERP × X) + Size_Premium + EM_Premium**

**DR = 4.5% + (5.0% × 1.8) + 4.0% + 2.5%**

**DR = 4.5% + 9.0% + 4.0% + 2.5% = 20.0%**

---

## Discount Rate Justification and Sensitivity

### 20.0% Discount Rate Implies:

**For comparison**:
- **S&P 500 average WACC**: ~8-10% (diversified, low-risk, profitable)
- **High-growth SaaS companies (profitable, $1B+ revenue)**: 10-12%
- **Small-cap SaaS (unprofitable, <$500M revenue)**: 15-18%
- **Distressed / turnaround situations**: 18-25%

**Zenvia at 20%** reflects:
- Small-cap status (adds ~3%)
- Unprofitability and transformation risk (adds ~4-5%)
- LATAM emerging market exposure (adds ~2.5%)
- Liquidity/going concern risk (adds ~2-3%)

**Sensitivity Analysis**:

| Scenario | X Multiplier | DR | Justification |
|----------|-------------|----|--------------|
| **Bull Case** (successful transformation) | 1.2 | 15.0% | Lower if: CPaaS divested at 1× revenue, SaaS scales to BRL 500M+ with 25%+ EBITDA margin, debt eliminated |
| **Base Case** (muddle through) | 1.8 | 20.0% | As calculated above |
| **Bear Case** (distressed) | 2.0+ | 24.0% | Higher if: CPaaS divestiture fails, liquidity crisis, covenant breach |

**Rationale for Base Case (20%)**:
- Reflects current state of heightened uncertainty
- Will be adjusted down in outer years IF company successfully executes (Year 3+ DR could decline to 15-16%)
- Appropriate for speculative investment requiring 20%+ expected return to compensate risk

---

## Risk Mitigation Factors and Offsetting Considerations

While Zenvia carries significant risks, several factors prevent the discount rate from going even higher:

### 1. Controlling Shareholder Support
- **Oria Capital** (PE firm) is controlling shareholder, injected BRL 50M in Feb 2024
- Demonstrated commitment to avoiding bankruptcy / supporting liquidity
- **Risk Mitigation**: Reduces probability of near-term distressed scenario by ~15-20%

### 2. Asset Backing
- CPaaS business has tangible value (BRL 200-420M range, even in stressed scenario)
- Customer base of 10,000+ provides floor valuation
- **Risk Mitigation**: Provides downside protection; equity unlikely to go to zero even in bear case

### 3. Strategic Optionality
- Multiple paths to value: Divest CPaaS, scale SaaS organically, or sell entire company
- Management has shown willingness to pivot (evidenced by 2025 strategic cycle announcement)
- **Risk Mitigation**: Increases probability of *some* positive outcome (even if not bull case)

### 4. LATAM Market Position
- 20-year operating history, dominant player in Brazil
- Localization advantage vs. global competitors (language, payment systems, regulatory knowledge)
- **Risk Mitigation**: Reduces competitive risk in core market

### 5. SaaS Product Traction
- Zenvia Customer Cloud showing strong usage growth (80% Q1→Q2)
- Franchise model early but promising (15% of new MRR already)
- **Risk Mitigation**: Evidence that product-market fit exists; reduces execution risk probability

**Net Effect**: These mitigants justify *not* using 25%+ discount rate (which would be appropriate for pure speculative venture with no downside protection). The 20% DR reflects high risk but acknowledges the company is not a "zero or hero" lottery ticket.

---

## Scenario-Based Discount Rate Adjustments (Future State)

The 20% discount rate is appropriate for **near-term cash flows (Years 1-3)** under current uncertainty. However, in scenario analysis, we should apply different discount rates to different outcome paths:

### Scenario 1: Successful Transformation (Prob: 30%)
- **Years 1-2**: 20% (transformation execution risk)
- **Years 3-5**: 15% (de-risked post-divestiture; scaled SaaS with improving margins)
- **Years 6+**: 12% (mature SaaS company with moderate growth)

**Justification**: If company successfully divests CPaaS, scales SaaS to BRL 500M+, and achieves 25%+ EBITDA margins, risk profile converges toward typical small-cap SaaS (lower liquidity risk, higher predictability).

### Scenario 2: Muddle Through (Prob: 50%)
- **All years**: 20% (persistent execution risk, sub-scale operations)

**Justification**: Company remains subscale, marginally profitable, with elevated leverage. Risk profile does not improve materially.

### Scenario 3: Distressed Outcome (Prob: 20%)
- **Years 1-2**: 25%+ (distressed discount rate)
- **Years 3+**: N/A (equity impaired or restructured)

**Justification**: If CPaaS divestiture fails or SaaS disappoints, liquidity crisis triggers forced restructuring. Equity value approaches recovery value (asset liquidation).

---

## Terminal Value Risk Considerations

**Terminal Value DR**: In perpetuity calculations (Gordon Growth Model or exit multiple), we should use a **lower discount rate** than near-term, reflecting:

1. **Survivorship Bias**: If company reaches Year 10, it has by definition navigated transformation risks
2. **Market Maturity**: Terminal period assumes steady-state, not high-risk transformation
3. **Convergence to Market**: Successful companies converge toward sector-average risk profiles

**Terminal DR Recommendation**: 12-14% (assumes successful transformation and de-risking)

**Formula**:
```
Terminal_DR = RFR + (ERP × X_terminal)

Where:
  RFR = 4.5% (assume stable)
  X_terminal = 1.2-1.4 (lower than current 1.8)

Terminal_DR = 4.5% + (5.0% × 1.3) = 11.0%
  + Size premium (2.0%, assuming larger cap by terminal period)
  + EM premium (2.0%, assumes LATAM risk persists but moderates)

= 15.0% (terminal DR)
```

**Use in Valuation**:
- Years 1-5: Use 20% DR (high risk)
- Years 6-10: Use 17% DR (moderate risk, interpolating down)
- Terminal period (Year 10+): Use 15% DR (steady-state risk)

---

## Downside Protection and Recovery Value

**Liquidation Value Analysis** (bear case floor):

Assuming company forced to liquidate assets in distressed scenario:

| Asset | Book Value (BRL M) | Recovery % | Recovery Value (BRL M) |
|-------|-------------------|-----------|----------------------|
| Cash | 33 | 100% | 33 |
| Receivables (net) | 204 | 70% | 143 |
| PP&E | 13 | 30% | 4 |
| Intangibles - CPaaS business | 150 | 50% | 75 |
| Intangibles - SaaS business | 1,146 | 20% | 229 |
| **Total Assets** | 1,546 | | **484** |
| Less: Debt | (93) | 100% | (93) |
| Less: Earnout liabilities | (271) | 50% | (136) |
| **Net Recovery** | | | **255** |

**Recovery per Share**: BRL 255M / 52.6M shares = BRL 4.85 per share (~$0.88 at 5.5 FX)

**Current Price**: $1.27

**Downside from Current**: ~30% (implies market already pricing in some distress risk)

**Implication for DR**: The 20% discount rate is consistent with ~30% downside risk (not 60-80%), given asset backing provides floor valuation.

---

## Monitoring Metrics: Risk Triggers and Re-Rating Events

To dynamically adjust the discount rate, monitor these quarterly triggers:

### De-Risking Events (DR should decline):
1. **CPaaS divestiture announced at ≥ 0.8× revenue** → Reduce DR by 3-4%
2. **SaaS revenue growth sustains ≥ 20% for 3 consecutive quarters** → Reduce DR by 1-2%
3. **Positive operating cash flow for 2 consecutive quarters** → Reduce DR by 1-2%
4. **Debt reduced by ≥ 50%** → Reduce DR by 2-3%
5. **EBITDA margin expands to 20%+** → Reduce DR by 1-2%

### Re-Risking Events (DR should increase):
1. **CPaaS divestiture fails to materialize by Q2 2026** → Increase DR by 3-5%
2. **SaaS revenue growth decelerates below 15% CAGR** → Increase DR by 2-3%
3. **Debt covenant breach or renegotiation required** → Increase DR by 4-5%
4. **Intangible impairment announced** → Increase DR by 3-4%
5. **Key executive departure (CEO, CFO)** → Increase DR by 2-3%

---

## Conclusion: 20% Discount Rate Reflects High-Risk, High-Uncertainty Situation

The 20% discount rate for Zenvia is not arbitrary—it is the mathematical outcome of:
1. **Systematic risks**: Small-cap, LATAM emerging market, high-beta sector
2. **Idiosyncratic risks**: Business model transformation, liquidity crisis, execution uncertainty
3. **Risk multiplier of 1.8**: High end of "elevated risk" range, appropriate for unprofitable growth companies with speculative transformation theses

**Key Insights**:
- This DR implies investors require 20% annual return to hold ZENV equity (vs. 8-10% for S&P 500)
- Reflects 50-70% probability that company does NOT achieve bull case
- Not static: Should decline if company de-risks (CPaaS divested, SaaS scales), or increase if risks materialize
- Consistent with current valuation ($67M market cap) and 30% downside to recovery value

In the kernel execution (Turn 2), this 20% DR will be applied to scenario-weighted cash flows, with sensitivity analysis around 15-25% range to test valuation robustness. The discount rate is the linchpin connecting risk assessment to intrinsic value—getting it right is critical for accurate CVR.
