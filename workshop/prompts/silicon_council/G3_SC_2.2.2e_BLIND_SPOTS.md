# **G3 SILICON COUNCIL 2.2.2e: Pipeline Blind Spots Reference**

This appendix provides detailed context on each blind spot for the Pipeline Fit Assessment. Use this reference when evaluating whether a security is well-suited to the CAPY pipeline's current analytical constraints.

## **A.1 Debt Dynamics**

**What the pipeline does:** Simplified APV with static Y0 balance sheet. Enterprise Value is calculated, then Debt is subtracted at Y0 book value to arrive at Equity Value. No dynamic debt modeling.

**What it misses:**
- Refinancing risk (debt maturities, credit availability)
- Interest rate sensitivity on floating rate debt
- Covenant constraints that could force dilutive actions
- Debt spiral dynamics in stress scenarios
- Solvency concerns that might dominate equity value

**When this matters:** Net Debt / EBITDA > 3x; Significant near-term maturities; Variable rate exposure > 30% of debt; Tight covenant headroom.

## **A.2 Pre-Revenue / Early-Stage**

**What the pipeline does:** DCF from Y0 base, with growth assumptions in GIM.

**What it misses:**
- Optionality value of pivots and alternative paths
- Burn rate / runway dynamics
- Milestone-based value creation (not captured in smooth DCF)
- Binary success/failure dynamics

**When this matters:** Revenue < $10M; Business model unproven; Negative operating margins with no clear path to profitability; Heavy reliance on TAM penetration assumptions.

## **A.3 Critical Document Gaps**

**What the pipeline ingests:** Company filings (10-K, 10-Q, transcripts, presentations) and RQ outputs from AlphaSense/other sources.

**What it might miss:**
- Primary clinical/scientific data (for biotech, only derivative commentary)
- Patent filings and IP documentation
- Regulatory submission details
- Specialized industry data not in standard databases

**When this matters:** Biotech with material pipeline; IP-dependent businesses; Pending regulatory decisions where details matter.

## **A.4 Balance Sheet Complexity**

**What the pipeline does:** Standard Equity Bridge (EV - Debt + Cash - Minority Interest).

**What it misses:**
- Cross-shareholdings in other public companies (especially Japanese corporates)
- Real estate carried at historical cost
- Investment securities marked at different bases
- Hidden liabilities (pension, environmental, litigation reserves)
- Net-nets and asset plays where liquidation value exceeds going concern

**When this matters:** Price < Book Value; Significant "Other Assets" on B/S; Japanese/Korean corporate structure; Real estate holdings.

## **A.5 Conglomerate Structure**

**What the pipeline does:** Unified SCM for the consolidated entity.

**What it misses:**
- Segment-level economics with different risk profiles
- Internal transfer pricing distortions
- Conglomerate discount dynamics
- Sum-of-parts value that may diverge from consolidated DCF

**When this matters:** >3 distinct segments; Segments with materially different margins, growth, or risk; Holding company structures.

## **A.6 Extreme Management Scenarios**

**What the pipeline does:** Management quality is considered qualitatively; governance is flagged in RQ1.

**What it misses:**
- Activist campaign dynamics
- Key-person succession risk modeling
- Fraud scenarios beyond generic tail risk
- Capital allocation changes under new management

**When this matters:** Active or potential activist situation; Key-person risk (founder-led with no succession); Material governance concerns from RQ1.

## **A.7 Complex Share Dynamics**

**What the pipeline does:** TSM-adjusted share count with SBC as operating expense.

**What it misses:**
- Convert dilution under different price scenarios
- Warrant exercise dynamics
- Earnout share obligations
- Multi-class voting implications for M&A scenarios

**When this matters:** Material outstanding convertibles; Warrants with near-the-money strikes; Earnout structures; Dual-class shares.

## **A.8 Macro/Industry Sensitivity**

**What the pipeline does:** Company-specific scenarios via SSE; DR incorporates risk premium.

**What it misses:**
- Explicit rates sensitivity modeling
- Commodity price cycle effects
- Industry-wide demand shocks
- Beta-driven correlation with macro

**When this matters:** Commodity exposure; High operating leverage; Rate-sensitive (financials, real estate); Strong historical beta.

## **A.9 Cyclicality**

**What the pipeline does:** Linear or S-curve assumptions over 20-year horizon.

**What it misses:**
- Position in current cycle
- Cycle amplitude and timing
- Mean reversion to cycle midpoint vs. current level
- Inventory/capex cycle dynamics

**When this matters:** Semiconductor; Commodity producers; Cyclical industrials; Current metrics at cycle peak or trough.

## **A.10 Real Options**

**What the pipeline does:** DCF of expected cash flows; scenarios for discrete events.

**What it misses:**
- Option value of unexploited opportunities
- Platform optionality (ability to expand into adjacent markets)
- Abandonment option value
- Flexibility value under uncertainty

**When this matters:** Early-stage platforms; Multiple strategic paths available; Exploration/development stage assets.

## **A.11 Binary Regulatory Events**

**What the pipeline does:** Scenarios with probability estimation via Bayesian protocol.

**What it misses:**
- Calibration difficulty when base rates are genuinely uncertain
- Binary nature may not be well-captured by P × M framework
- Timing uncertainty may dominate value

**When this matters:** Pending FDA decisions; Antitrust review; Material litigation with binary outcome; Regulatory approval gates.

## **A.12 Interconnections and Non-Linearities**

**What the pipeline does:** Models scenarios independently; SSE handles co-occurrence.

**What it misses:**
- Non-linear interactions between risk factors
- Feedback loops (e.g., declining revenue → credit downgrade → higher interest → lower revenue)
- Threshold effects and tipping points
- Compounding of multiple moderate risks into severe outcomes

**When this matters:** Multiple blind spots flagged for the same security; Factors compound in stress scenarios; Company operates near critical thresholds.

*END OF G3 SILICON COUNCIL 2.2.2e BLIND SPOTS REFERENCE*
