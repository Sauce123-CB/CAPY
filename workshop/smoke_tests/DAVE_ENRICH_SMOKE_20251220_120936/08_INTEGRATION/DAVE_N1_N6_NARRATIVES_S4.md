# DAVE N1-N6 NARRATIVES (State 4 Finalized)
## Integration Turn 1 Output
## Valuation Date: 2025-12-21

---

## N1: INVESTMENT THESIS
**[State 4: Confirmed - No modifications from adjudication]**

Dave Inc. is an asset-light consumer fintech providing Earned Wage Access (EWA) services to underbanked Americans. The investment thesis rests on three pillars:

1. **Structural Cost Advantage:** Best-in-class unit economics with CAC of $19 and 4-month payback period, compared to industry averages of $50-100 CAC and 12-18 month payback.

2. **Proprietary Underwriting Moat:** CashAI algorithm trained on 150M+ origination decisions over 7+ years provides differentiated risk assessment for underbanked populations that traditional FICO cannot score.

3. **Multiple Expansion Vectors:**
   - Dave Banking revenue acceleration (interchange, deposits)
   - BNPL product launch (Dave BNPL, 2025)
   - Subscription model rollout ($3/month)
   - TAM expansion from 2.85M MTMs toward 10M+ terminal

**Key Risks:**
- Regulatory overhang (FTC/CFPB actions, CEO named as defendant)
- Credit cycle exposure (69% of customers live paycheck-to-paycheck)
- Terminal ROIC sustainability (model produces 40.9% vs. 18-22% anchor)

**[State 4 Interpretive Guidance: For conservative positioning, apply 15-20% mental discount to E[IVPS] for unmodeled shutdown risk and ROIC sustainability uncertainty]**

---

## N2: INVESTED CAPITAL MODELING
**[State 4: Confirmed - No modifications from adjudication]**

Dave's invested capital structure reflects its asset-light lending model:

**Y0 Invested Capital Composition ($275M):**
- Net ExtraCash Receivables: $260M (95%)
- Net PP&E/Intangibles: $15M (5%)
- Working Capital: Minimal (negative NWC ex-receivables)

**Key Dynamics:**
1. **Receivables-Driven Growth:** IC growth tracks ExtraCash origination growth. At current $8B annual originations with ~11-day average duration, receivables balance of $260M implies ~3x annual turnover.

2. **Capital-Light Operations:** CapEx of $7M (1.3% of revenue) reflects software-centric operations with minimal physical infrastructure.

3. **Funding Strategy:** Currently on-balance-sheet via debt facility ($75M) and equity. Management indicated potential off-balance-sheet funding by 2026, which would reduce IC but also transfer margin to funding partners.

**Terminal IC Trajectory:**
- Y20 Invested Capital: $2,527M
- Implied annual IC growth: 11.5% (driven by receivables scaling with originations)
- Terminal ROIC: 40.9% (reflects high margins on efficient capital base)

---

## N3: ECONOMIC GOVERNOR AND CONSTRAINTS
**[State 4: Confirmed - No modifications from adjudication]**

**Economic Governor Verification:**

The Economic Governor constraint (g_terminal <= DR_static) is satisfied:
- Terminal g: 4.25%
- DR_static: 13.25%
- Margin: 9.00pp (substantial headroom)

**Growth-ROIC-RR Coherence:**
- g = ROIC x RR = 40.9% x 10.4% = 4.25% (satisfied)
- Terminal RR = 10.4% implies 89.6% FCF conversion at terminal

**Constraint Validation:**
1. Terminal ROIC (40.9%) exceeds industry p90 (35%) - model output, not input assumption
2. Terminal revenue growth (4.25%) capped at RFR per methodology
3. Limited liability floor ($0) enforced across SSE states

**[State 4 Interpretive Guidance: Terminal ROIC of 40.9% exceeds long-term anchors (18-22% target). If ROIC mean-reverts to industry norms over perpetuity, E[IVPS] may be overstated by $20-30. Recommend 10-15% mental discount for ROIC sustainability.]**

---

## N4: RISK ASSESSMENT AND DR DERIVATION
**[State 4: Confirmed - No modifications from adjudication]**

**Discount Rate Derivation:**

DR = RFR + X * ERP = 4.25% + 1.80 * 5.0% = 13.25%

**X-Factor Components (1.80):**

| Factor | Impact | Rationale |
|--------|--------|-----------|
| Regulatory risk | +0.40 | CFPB/FTC actions, CEO defendant, state AG coordination |
| Credit cycle exposure | +0.25 | 31% YoY delinquency increase, procyclical strategy |
| Small-cap/emerging | +0.30 | Market cap $3.3B, limited trading history |
| Single product concentration | +0.10 | 87% revenue from ExtraCash advances |
| Bank partner dependency | +0.05 | Mitigated by Evolve-to-Coastal transition |
| Execution track record | -0.10 | Fee transition and bank migration executed flawlessly |
| Profitability | -0.10 | GAAP profitable, positive cash generation |
| TAM runway | -0.05 | Large conversion opportunity (11M inactive members) |
| Cash generation | -0.05 | FCF positive, deleveraging trajectory |
| **Net X-Factor** | **+0.80** | |

**Base X of 1.0 + 0.80 = 1.80**

**State 3 Revision from BASE:**
- BASE X: 1.75 (DR = 13.0%)
- State 3 X: 1.80 (DR = 13.25%)
- Delta: +0.05 (regulatory escalation offset by execution validation)

---

## N5: ENRICHMENT SYNTHESIS
**[State 4: Confirmed - No modifications from adjudication]**

**RQ Evidence Integration Summary:**

The ENRICH stage ingested 7 research questions (RQ1-RQ7) covering:
- M-1: Integrity Check (accounting forensics, governance)
- M-2: Adversarial Synthesis (bull/bear arguments)
- M-3a: Mainline Scenarios (regulatory, BNPL, bank, M&A)
- M-3b: Tail Scenarios (Blue Sky and Black Swan)
- D-1, D-2, D-3: Lynchpin coverage (competitive moat, growth runway)

**Key Evidence Updates:**
1. **Credit Loss Normalization (RQ3b, RQ5):** Through-cycle credit losses revised from 2.5% to 3.0% based on COVID-19 precedent (+2.3pp industry increase). Terminal gross margin adjusted from 62% to 60%.

2. **Regulatory Risk Confirmation (RQ3a):** DOJ lawsuit escalation, CEO named as defendant, coordinated state AG actions confirm elevated regulatory risk. Settlement precedents $10-50M.

3. **Competitive Moat Validation (D-3):** CashAI data moat confirmed (150M+ originations, 7+ years) but characterized as "narrow/validated" rather than "wide/impregnable."

4. **Operating Leverage Confirmation (RQ6):** Peer benchmarking validates Dave's 27% EBITDA margin at p60-p70 of distribution. Best-in-class unit economics confirmed.

**State 2 IVPS: $199.25**

---

## N6: SCENARIO MODEL SYNTHESIS
**[State 4: Confirmed - No modifications from adjudication]**

**4-Scenario Set:**

| ID | Scenario | P | M | |P x M| |
|----|----------|---|---|--------|
| S1 | REG_SETTLEMENT | 73% | -$52 | $38.17 |
| S3 | BANK_TRANSITION | 76% | +$43 | $32.37 |
| S4 | ACQUISITION | 20% | +$40 | $8.00 |
| S2 | BNPL_SUCCESS | 16% | +$31 | $4.89 |

**Scenario Narratives:**

**S1: Regulatory Settlement (73%, -$52)**
- CFPB/FTC lawsuit resolves with unfavorable settlement
- Required fee disclosure (APR equivalent) reduces tip revenue ~30%
- Compliance costs increase ~$10M annually
- Probability derived via Bayesian decomposition (N=6 reference class)

**S2: BNPL Success (16%, +$31)**
- Dave BNPL launches successfully in H2 2025
- Captures 1.5% of $500B TAM by Y5 ($7.5B GMV)
- Take rate ~5% contributes $375M incremental revenue
- Execution risk discounts probability significantly

**S3: Bank Transition Success (76%, +$43)**
- Coastal migration provides improved interchange economics
- Dave Banking becomes primary value driver by Y5
- Deposit growth enables lower-cost funding
- High probability reflects management's execution track record

**S4: Acquisition (20%, +$40)**
- Premium acquisition at ~$275-300/share
- Acquirer profile: Block, Chime, or regional bank
- Premium represents 22% to consensus PT of $275

**Distribution Characteristics:**
- E[IVPS]: $206.34
- P10: $147 (S1-only outcome)
- P50: $188
- P90: $239
- Skewness: RIGHT (upside optionality)
- Modality: MULTIMODAL (regulatory binary creates clustering)

**[State 4 Interpretive Guidance: Shutdown risk (5-10% probability, -100% impact) not explicitly modeled. Mental discount of ~$10-20 recommended for conservative positioning.]**

---

## State 4 Finalization Summary

All narratives N1-N6 confirmed without modification. Adjudication findings were either:
1. Rejected due to insufficient evidentiary basis to override State 3 analysis
2. Addressed through interpretive guidance rather than artifact modification

**Key Interpretive Guidance (apply to E[IVPS] of $206.34):**
- Shutdown risk mental discount: ~$10-20
- Terminal ROIC sustainability mental discount: ~$20-30
- Combined conservative range: $165-175

**Pipeline Fit Grade:** B (Proceed with caveats)

---

[END OF N1-N6 NARRATIVES - STATE 4]
