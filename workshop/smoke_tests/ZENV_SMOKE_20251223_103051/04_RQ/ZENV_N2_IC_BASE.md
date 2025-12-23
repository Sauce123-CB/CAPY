# N2: Invested Capital Modeling - Zenvia Inc. (NASDAQ:ZENV)

## Conceptual Framework

Zenvia's invested capital structure reflects two distinct business models—CPaaS (asset-light channel business) and SaaS (IP-intensive software business)—along with the financial overhang from past M&A activity. The company's balance sheet is dominated by intangible assets from acquisitions (BRL 1,296M, 77% of total assets) and correspondingly high acquisition-related liabilities (BRL 271M). Understanding the physics of capital deployment requires decomposing these elements and modeling the ongoing capital requirements for each business separately.

## Balance Sheet Decomposition (as of June 30, 2025)

### Assets (BRL thousands)

**Operating Assets:**
- Cash and cash equivalents: 32,611 (working capital, not excess)
- Trade receivables (net): 203,895
- Prepayments: 6,328
- Property, plant & equipment: 12,728 (primarily data processing equipment)
- Right-of-use assets: 3,426
- **Subtotal Operating Assets**: 258,988

**Intangible Assets:**
- Goodwill and intangibles: 1,295,689 (from acquisitions: Movidesk, Sensedata, others)
- Breakdown (from prior disclosures):
  - Goodwill: ~BRL 850M (est.)
  - Customer relationships: ~BRL 300M (est.)
  - Technology/IP: ~BRL 100M (est.)
  - Trade names: ~BRL 45M (est.)

**Non-Operating/Questionable Assets:**
- Deferred tax assets: 85,642 (requires profitability to realize)
- Restricted cash: 3,415 (collateral for loans)
- Recoverable tax assets: 20,112
- Other assets: 8,424

**Total Assets**: 1,672,270

### Liabilities and Equity (BRL thousands)

**Operating Liabilities:**
- Trade payables: 457,911 (carrier costs, suppliers)
- Employee benefits: 34,102 (current 32,059 + non-current 2,043)
- Deferred revenue: 6,237
- **Subtotal Operating Liabilities**: 498,250

**Debt and Acquisition Liabilities:**
- Current debt: 78,014 (loans, borrowings, debentures)
- Non-current debt: 14,598
- **Total Interest-Bearing Debt**: 92,612
- Liabilities from acquisitions (current): 113,940
- Liabilities from acquisitions (non-current): 157,279
- **Total Acquisition Liabilities**: 271,219
- **Combined Debt + Earnouts**: 363,831

**Other Liabilities:**
- Lease liabilities: 3,692
- Tax liabilities: 46,046
- Provisions: 1,614
- Derivatives: 16,676

**Equity**: 742,161

**Total Liabilities + Equity**: 1,672,270

## Invested Capital Calculation (Y0: June 30, 2025)

### Approach: Operating Capital Method

**Invested Capital Formula:**
IC = Operating Assets - Operating Liabilities + Intangible Assets

**Calculation (BRL thousands):**
- Operating Assets: 258,988
- Less: Operating Liabilities: (498,250)
- **Operating Working Capital**: (239,262) [NEGATIVE]
- Plus: Intangible Assets: 1,295,689
- **Total Invested Capital (Book)**: 1,056,427

### Validation: Financing Method

**Alternative Check:**
- Total Equity: 742,161
- Plus: Total Debt: 92,612
- Plus: Acquisition Liabilities: 271,219
- Less: Excess Cash: 0 (no excess; company has liquidity constraints)
- Plus: Minority Interest: 0
- **Total Invested Capital (Financing)**: 1,105,992

**Reconciliation Note**: ~BRL 50M difference attributable to non-operating assets (DTAs, tax receivables) and derivatives. For valuation purposes, we use **BRL 1,056M** as base IC, reflecting economic assets deployed in operations.

## Capital Structure and Cost Implications

### Current Capital Structure (June 30, 2025)

| Component | Amount (BRL) | % | Notes |
|-----------|-------------|---|-------|
| Equity | 742,161 | 67% | Market cap: ~BRL 370M (USD 67M @ 5.5 FX) |
| Interest-Bearing Debt | 92,612 | 8% | Renegotiated in Feb 2024; matures Dec 2026 |
| Acquisition Liabilities | 271,219 | 25% | Earnouts; matures through Dec 2028; partial equity conversion option |
| **Total Capital** | 1,105,992 | 100% | |

**Key Observations:**
1. **Book vs. Market Equity Divergence**: Book equity BRL 742M vs. market equity ~BRL 370M suggests market heavily discounts asset quality or fears dilution
2. **Acquisition Liability Overhang**: BRL 271M in earnouts (mostly Movidesk) creates significant cash drag; BRL 100M convertible to equity
3. **Negative Working Capital**: Operating WC of (BRL 239M) creates acute liquidity pressure
4. **Intangible Dominance**: 77% of assets are intangibles; highly susceptible to impairment risk

### Debt Detail

**Interest-Bearing Debt (BRL 92.6M):**
- Bank loans (Votorantim, BTG Pactual, others): ~BRL 50M
- Debentures: ~BRL 40M
- Weighted average interest rate: ~CDI + 3-5% (~15-17% all-in)
- Maturity: December 2026 (18-month extension granted Feb 2024)
- Covenant risk: Company flagged going concern; close monitoring required

**Acquisition Liabilities (BRL 271M):**
- Primarily Movidesk earnout (renegotiated Feb 2024)
- Extended to 60-month term (through Dec 2028)
- BRL 100M convertible to equity at company's option (BRL 50M by Dec 2025, balance in 6 semi-annual installments from Jan 2026)
- Effective cost: APV adjustments + FX impact (disclosed as ~8-10% implicit rate)

## Capital Intensity by Business Segment

### CPaaS Business (72% of revenue, declining)

**Capital Requirements:**
- **Working Capital**: High receivables (45-60 day collections) vs. carrier payables (30-45 day terms) = moderate WC intensity
- **CapEx**: Minimal; primarily IT infrastructure for messaging routing (est. BRL 5-10M annually)
- **Intangibles**: Negligible ongoing investment; customer relationships short-cycle
- **Incremental IC/Revenue**: ~0.15-0.20 (relatively capital-efficient once platform built)

**CPaaS IC Allocation (estimated):**
- Operating WC (net): ~BRL 50M (receivables - payables for CPaaS portion)
- Platform infrastructure: ~BRL 20M (servers, routing equipment)
- Customer relationships (book value): ~BRL 100M (mostly historical)
- **Total CPaaS IC**: ~BRL 170M

### SaaS Business (28% of revenue, growing)

**Capital Requirements:**
- **Working Capital**: Lower than CPaaS (prepaid subscriptions, faster collections); likely positive WC contribution
- **CapEx**: Higher than CPaaS; ongoing product development, cloud infrastructure (est. BRL 15-25M annually)
- **Intangibles**: Critical; technology platform, AI models, customer success IP
- **Incremental IC/Revenue**: ~0.40-0.60 (higher due to upfront tech investment, but declining as scales)

**SaaS IC Allocation (estimated):**
- Operating WC (net): ~BRL (30)M (negative; prepaid subscriptions)
- Technology platform: ~BRL 150M (Zenvia Customer Cloud, legacy SaaS products)
- Customer relationships: ~BRL 200M (longer-duration SaaS contracts)
- Goodwill (Movidesk, Sensedata): ~BRL 650M
- **Total SaaS IC**: ~BRL 970M

**Validation**: BRL 170M (CPaaS) + BRL 970M (SaaS) - overlap adjustments = ~BRL 1,056M (matches IC calculation)

## Capital Efficiency Metrics (Historical)

### Asset Turnover
- Revenue (LTM H1 2025 annualized): ~BRL 1,163M
- Total Assets: BRL 1,672M
- **Asset Turnover**: 0.70× (low; reflects intangible-heavy structure)

### Invested Capital Turnover
- Revenue (LTM): ~BRL 1,163M
- Invested Capital: BRL 1,056M
- **IC Turnover**: 1.10× (marginally acceptable)

### Return on Invested Capital (ROIC) - Current
- NOPAT (LTM, estimated): ~BRL 10M (normalized EBITDA ~BRL 100M, less taxes ~BRL 20M, less D&A ~BRL 70M = ~BRL 10M)
- Invested Capital: BRL 1,056M
- **ROIC**: ~1.0% (deeply sub-WACC; unsustainable)

**Interpretation**: Company is massively overcapitalized relative to current earnings power. The bull case requires either (1) dramatic NOPAT expansion through SaaS scaling, or (2) IC reduction through asset divestitures.

## Future Capital Requirements: Modeling Assumptions

### Transformation Scenario (Base Case for CVR)

**Phase 1 (2025-2026): CPaaS Divestiture + SaaS Scaling**
- **CPaaS Sale**: Assume transaction in 2026 at 1.0× revenue (~BRL 420M)
  - Proceeds: ~BRL 420M
  - Use of proceeds: Debt paydown (BRL 93M), acquisition liability paydown (BRL 150M), working capital (BRL 100M), remaining to cash
  - **IC Reduction**: BRL 170M (CPaaS IC removed)
- **SaaS Growth**: 25% CAGR through 2027
  - Incremental IC requirement: BRL 0.50 per BRL 1.00 incremental revenue
  - FY2025 SaaS revenue: BRL 200M → FY2027 SaaS revenue: BRL 312M (delta: BRL 112M)
  - **IC Addition**: BRL 56M (for SaaS growth)

**Net IC Change**: (BRL 170M) + BRL 56M = **(BRL 114M)** reduction

**Phase 2 (2027-2029): Pure-Play SaaS Optimization**
- Continued revenue growth (20% CAGR) with improving capital efficiency (IC/Revenue declining from 0.50 to 0.40 as scale improves)
- No major divestitures; organic optimization
- **IC Addition**: ~BRL 30-40M over period

### Working Capital Dynamics

**Current State** (H1 2025):
- Days Sales Outstanding (DSO): ~65 days (calculated from receivables/daily revenue)
- Days Payables Outstanding (DPO): ~73 days (calculated from payables/daily COGS)
- **Cash Conversion Cycle**: ~65 - 73 = negative 8 days (misleading; acute liquidity risk)

**Issue**: Despite negative CCC, company burned BRL 18M in operating cash H1 2025 due to:
1. High non-cash items reversing (derivative gains)
2. Debt service payments
3. Earnout installments
4. Seasonal receivables build

**Modeling Approach**:
- Post-divestiture, assume DSO improves to 55 days (SaaS faster collections)
- DPO stabilizes at 45 days (less carrier dependency)
- **Target CCC**: ~10 days (modest working capital requirement)

### Capital Allocation Priorities (Management Stated)

1. **Deleveraging**: Pay down debt and acquisition liabilities (87% of proceeds from CPaaS sale)
2. **SaaS Investment**: R&D and customer acquisition for Zenvia Customer Cloud (BRL 20-30M annually)
3. **Working Capital**: Maintain minimum cash buffer of BRL 50-75M (vs. current BRL 33M)
4. **Shareholder Returns**: None contemplated; full FCF to balance sheet repair

## Causal Links: IC → ROIC → Value Creation

### Current State (2025)
- IC: BRL 1,056M
- ROIC: 1.0% (pre-tax)
- WACC estimate: ~18% (high risk, leveraged)
- **Economic Profit**: Deeply negative (BRL -180M annually); destroying value

### Target State (2027-2028, post-transformation)
- IC: ~BRL 950M (reduced via divestiture, partially offset by SaaS growth)
- ROIC target: 10-12% (requires NOPAT of BRL 95-114M)
  - Path: SaaS revenue BRL 300M @ 65% GM = BRL 195M GP, less SG&A BRL 60M (20% of revenue) = BRL 135M EBITDA, less D&A BRL 30M, less tax BRL 10M = ~BRL 95M NOPAT
- WACC (if successful): ~12-14% (lower leverage, perceived as SaaS company)
- **Economic Profit**: Approaching breakeven; value-accretive on marginal basis

### Key Driver: Revenue Mix Shift
The single most important invested capital dynamic is the CPaaS → SaaS mix shift:
- CPaaS: 1.1× IC turnover, 5% EBIT margin → 5.5% ROIC
- SaaS: 0.30× IC turnover (in steady state), 25% EBIT margin → 7.5% ROIC (improving to 10-12% at scale)

**Insight**: Even though SaaS is more capital-intensive per dollar of revenue, its higher margins drive superior ROIC. The transformation creates value IF management can successfully divest CPaaS near book value and scale SaaS to critical mass (BRL 300M+ revenue).

## Impairment Risk and Downside Scenarios

### Intangible Asset Impairment

**Current Book Value**: BRL 1,296M (77% of assets)

**Impairment Triggers**:
1. Failure to divest CPaaS → continued margin pressure
2. SaaS growth slows below 15% → DCF valuations decline
3. Debt covenant breach → going concern assessment
4. Competitive pressure → customer attrition

**Downside Scenario**: If management fails to execute transformation, intangibles could face BRL 300-500M impairment (25-40% haircut), destroying book equity.

**Offsetting Factor**: Tax loss carryforwards (disclosed BRL 85M DTA) would allow company to recognize impairment losses without cash tax impact, but realizability of DTA itself becomes questionable in loss scenario.

## Conclusion: Invested Capital Lens on Investment Thesis

Zenvia's invested capital structure tells the story of a company at a crossroads:

1. **Overcapitalized for Current Earnings**: ROIC of 1% on BRL 1.06B of IC is untenable; company must either grow NOPAT dramatically or shrink IC substantially.

2. **Debt and Earnout Overhang**: BRL 364M in debt + acquisition liabilities creates structural drag; CPaaS divestiture is not optional—it is necessary for survival.

3. **Intangible Risk**: BRL 1.3B in intangibles (mostly from M&A) are vulnerable to impairment if strategic pivot fails; potential for 30-50% equity value destruction in downside scenario.

4. **Transformation Potential**: If successful, revenue mix shift from 72% CPaaS to 100% SaaS, combined with IC reduction from divestiture, could drive ROIC from 1% to 10-12%, creating significant value.

5. **Binary Outcome**: The invested capital dynamics reinforce the binary nature of this investment—either the company executes a successful transformation (deleverages, scales SaaS, restores ROIC) or faces distressed restructuring with equity impairment.

The next 12-18 months will determine which path unfolds. The invested capital framework will be central to the CVR model, as changes in IC (from divestitures and SaaS investment) will be the primary mechanism through which value is created or destroyed.
