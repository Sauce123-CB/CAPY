# CAPY 2.2.2e Remaining Patches - Detailed Context

---

## (1) T1+T2 KG Handshake - Enforce Debt, ATP, EV Items

**Problem:** Key Knowledge Graph items critical to the Equity Bridge (Total_Debt, Excess_Cash, Minority_Interest) and ATP reconciliation are defined in schemas but not enforced at handshake boundaries between T1 and T2.

**Current State:**
- G3BASE_2.2.1e.md line 382-385: Y0_data must include these for CAGR_INTERP mode
- BASE_CVR_KERNEL_2.2.1e.py lines 382-384: Equity Bridge uses these from core_data.Y0_data
- No explicit validation that T1→REFINE→T2 preserves these values

**Proposed Fix:**
- Add mandatory fields list to A.2 schema with explicit validation
- Add validation step in REFINE that checks for presence of Equity Bridge items
- Propagate to ENRICH/SCENARIO/INT prompts as surgical patch to their "Mandatory Inputs" sections

**Files to Touch:**
- G3BASE_2.2.1e.md - A.2 schema, Phase D validation
- BASE_T1_REFINE_v1_1.md - Add KG integrity check section
- Downstream G3 prompts - Inherit validation requirement

**Complexity:** Medium

---

## (2) Terminal ROIC Bug - IC Scaling Formula

**Problem:** In `calculate_apv()` at lines ~400-445 of the kernel, when terminal ROIC is unrealistic (80%+ in DAVE case vs 38% target), the reinvestment logic breaks down. The IC formula uses `ExtraCash_Receivables = Origination_Volume / 4 × 0.14` which doesn't scale properly with revenue growth.

**Evidence from Smoke Test:**
- Y5 ROIC = 116.1% (impossible to sustain)
- Y20 ROIC = 80.4% (still too high vs 38% target)
- T2 output correctly flagged this as calibration issue

**Original Bug Description (from message thread):**
> "Fix negative terminal ROIC bug; if ROIC=neg at terminal, default to g=topline/gdp"

**Proposed Fix:**
```python
if terminal_roic_r < 0:
    topline_growth_terminal = np.mean(forecast_df['Revenue'].pct_change().values[-3:])
    gdp_proxy = 0.025
    terminal_g = min(max(topline_growth_terminal, 0), rfr if rfr else gdp_proxy, gdp_proxy)
    reinvestment_rate_terminal = 0
    logger.warning(f"Terminal ROIC negative ({terminal_roic_r:.4f}). Defaulting g={terminal_g:.4f}")
```

Also need to fix IC scaling formula to properly model receivables at terminal scale.

**Files to Touch:**
- BASE_CVR_KERNEL_2.2.1e.py - lines ~400-445
- CVR_KERNEL_ENRICH_2.2.1e.py - same section
- CVR_KERNEL_SCEN_2_2_1e.py - same section
- CVR_KERNEL_INT_2_2_2e.py - same section
- CVR_KERNEL_IRR_2_2_4e.py - same section

**Complexity:** High - kernel code change affecting all downstream stages

---

## (3) REFINE DAG Enforcement - Hard Cap at 12-15 Nodes

**Problem:** Current REFINE prompt says "Target 12-15 exogenous nodes. Justify deviations in either direction." This is advisory, not enforced. Post-BASE scaling (SCENARIO, INT) complexity scales with exogenous node count.

**Evidence from Smoke Test:**
- DAVE REFINE arrived at 18 exogenous nodes
- Justification was provided and accepted
- Raises question: is 12-15 a hard cap or soft target?

**Original Spec:**
> "fix REFINE such that rich DAG is enforced. mandate (Strongly) full decomposition but cap at exogenous nodes = <=X, where X= ~12-15"

**Proposed Fix - Add to REFINE:**
```markdown
### 1.5 Exogenous Node Cap Enforcement (Hard Gate)

**Maximum:** 15 exogenous nodes in final DAG.

If T1 + expansions exceed 15:
1. Rank all exogenous nodes by expected IVPS sensitivity
2. Consolidate lowest-impact nodes until count ≤ 15
3. Document each consolidation with rationale

**Consolidation Priority (lowest → highest):**
- Cost nodes with <2% IVPS swing
- Nodes without Y0 calibration data
- Nodes with correlated trajectories (can be modeled as single driver)

**Exception:** May exceed 15 only if ALL nodes have documented Y0 calibration AND >2% individual IVPS sensitivity.
```

**Calibration Requirement:** Test on DAVE, FLL, ZENV, JET2

**Files to Touch:**
- BASE_T1_REFINE_v1_1.md - Add hard gate section
- G3BASE_2.2.1e.md - Reference cap in Phase D validation

**Complexity:** Low

---

## (4) Currency/Jurisdiction Guidance

**Problem:** Companies like ZENV (US-listed, Brazil operations) cause unit confusion when operating currency ≠ listing currency.

**Original Spec:**
> "add to readme (or as default) that if company reports in two currencies (or is listed in a dif jurisdiction than where it operates) it should use the operating currency and this should be put into the prompt window text, eg ZENV, As of Dec 12 2025, Currency=BRL"

**Proposed Fix - Extend trigger format:**

Current:
```
Do Turn 1: {Company Name}, {EXCHANGE:TICKER}, {As of DATE}
```

Proposed:
```
Do Turn 1: {Company Name}, {EXCHANGE:TICKER}, As of {DATE}[, Currency={XXX}]
```

Add guidance section:
```markdown
### Currency Convention

If the company operates primarily in a currency different from its listing jurisdiction:
- Specify operating currency in trigger: `Currency=BRL`
- All financial figures in output will be denominated in this currency
- Exchange rate assumptions should be documented in A.2 market_context

**Examples:**
- ZENV (US-listed, Brazil ops): `Currency=BRL`
- SHOP (US-listed, Canada ops): `Currency=CAD` or `Currency=USD` (analyst choice)
```

**Files to Touch:**
- CAPY_2_2e_README.md - Section 2.1, add currency guidance
- G3BASE_2.2.1e.md - Variable substitution section

**Complexity:** Low

---

## (5) Loosen ROIC/IC Narrative Language

**Problem:** Current IC methodology (Narrative #2 in G3BASE Phase B) is too rigid for cases like DAVE where ROIC can be misleading due to accounting artifacts.

**Original Spec:**
> "make the ROIC/IC narratives and language looser. basically i don't think it's doing what we want but it should still be in the kernel"

**Related Point (Chris):**
> "We also had the ROIC situation with Dave where it blew up ROIC because of the accounting mirage. Feels like it needs some ability to flag irregular scores as 'unusual but makes sense given x' or 'unusual but all the other metrics work, so continue but flag for double check later'"

**Proposed Enhancement:**
```markdown
2. Invested Capital Modeling (Narrative #2): 

Define IC methodology and assess ROIC interpretability:

**ROIC Quality Assessment:**
- HIGH: ROIC reflects true economic returns (clean balance sheet, minimal intangibles, stable capital structure)
- MODERATE: ROIC directionally useful but requires context (significant intangibles, M&A history, or SBC-heavy compensation)  
- LOW: ROIC potentially misleading (negative IC, massive goodwill, or accounting artifacts dominating)

If ROIC Quality = LOW, document:
- Why standard ROIC fails for this business
- Alternative capital efficiency metrics if applicable
- Flag for downstream SCENARIO/IRR stages to weight ROIC-based constraints loosely
```

Add to A.7 schema:
```json
"roic_quality_flag": "HIGH" | "MODERATE" | "LOW",
"roic_quality_rationale": "string"
```

**Files to Touch:**
- G3BASE_2.2.1e.md - Phase B, Narrative #2
- BASE_CVR_KERNEL_2.2.1e.py - A.7 output schema
- Propagate flag to downstream kernels

**Complexity:** Low

---

## (6) Output Requirements for Speed

**Problem:** Vague output specs cause LLM to over-generate or dump to chat instead of file.

**Original Spec:**
> "just nail down the output requirements so it's fast"

**Current Issues Identified:**
- INT T3 truncation (line 659-667 in README)
- Chat dump instead of file (line 649-655)

**Proposed Fix - Add to each stage's Output Mandate:**
```markdown
### Output Efficiency Protocol

1. **File Output Only:** Emit complete response as downloadable .md file. No chat dialogue.
2. **No Regeneration:** For T2/T3 turns, COPY upstream artifacts verbatim. Do not regenerate or rephrase.
3. **Selective Emission:** Only emit artifacts modified in this turn + the summary artifact (A.7/A.10/A.12/A.14).
4. **Truncation Prevention:** If approaching context limits, emit partial artifacts with `[TRUNCATED - continue in follow-up]` marker.
```

**Files to Touch:**
- All G3 prompts - add Output Efficiency Protocol section
- CAPY_2_2e_README.md - reinforce in failure modes section

**Complexity:** Medium

---

## (7) Streamline Prompts - Remove Embedded Code

**Problem:** Embedded kernel code in .md prompts (Appendix C sections) creates:
- P(missing middle) in long prompts
- Redundancy (code exists in .py files)
- Confusion about execute vs. reference

**Original Spec:**
> "see if i can streamline the readme and input/output requirements per stage. idea: delete the code from the .md prompt text and always attach the .py file as reference, trusting claude to use it for ref only and not code ex. the idea here is this reduces the p(missing middle) in prompt reading and streamlines the analysis"

**Current State:**
- G3BASE_2.2.1e.md: ~1400 lines of kernel code in Appendix C (lines 888-2280)
- G3ENRICH_2.2.1e.md: Similar embedded code
- G3_IRR_2_2_4e.md: Similar
- G3_INTEGRATION_2_2_2e.md: Similar

**Proposed Fix:**
Remove Appendix C (kernel code) from all G3 prompts. Replace with:
```markdown
### APPENDIX C: CVR Kernel (External Reference)

The kernel code is provided as a separate attachment: `CVR_KERNEL_{STAGE}_{VERSION}.py`

**Turn 1:** Kernel attached for CONTEXTUAL UNDERSTANDING. Review for:
- DSL mode definitions
- Node naming conventions  
- Equation syntax (GET(), PREV())
Do NOT execute.

**Turn 2:** Kernel attached for EXECUTION. Load and call functions directly.
```

Update README attachment tables to always list .py as required attachment.

**Estimated Token Savings:** ~3000-5000 tokens per prompt

**Files to Touch:**
- G3BASE_2.2.1e.md - Remove lines 888-2280, add reference stub
- G3ENRICH_2.2.1e.md - Same treatment
- G3_SCENARIO_2_2_1e.md - Same treatment
- G3_INTEGRATION_2_2_2e.md - Same treatment
- G3_IRR_2_2_4e.md - Same treatment
- CAPY_2_2e_README.md - Update attachment cheat sheet

**Complexity:** Medium

---

## (10) Schema Conformance - Exact JSON Templates

**Problem:** Claude Code smoke test produced artifacts with slightly different JSON structures than browser reference. The subagent interpreted G3BASE requirements but used different schema formats.

**Evidence from Smoke Test:**

Browser DAG uses:
```json
"Revenue": {
  "type": "Financial_Line_Item",
  "parents": ["MTMs", "ARPU"],
  "equation": "GET('MTMs') * GET('ARPU')"
}
```

Claude Code DAG uses:
```json
{
  "from": ["MTMs", "ARPU"],
  "to": "revenue",
  "equation": "revenue(t) = MTMs(t) * ARPU(t)"
}
```

The kernel expects the browser format with GET() and PREV() helper functions.

**Proposed Fix:**
Add explicit JSON schema templates to G3BASE that the LLM must copy exactly, not interpret. Include:
- A.1_EPISTEMIC_ANCHORS template
- A.2_ANALYTIC_KG template (with Y0_data structure)
- A.3_CAUSAL_DAG template (with GET()/PREV() syntax)
- A.5_GESTALT_IMPACT_MAP template (with LINEAR_FADE params)
- A.6_DR_DERIVATION_TRACE template

**Files to Touch:**
- G3BASE_2.2.1e.md - Add schema templates section

**Complexity:** Medium

---

## (11) Sensitivity Analysis Bug - IVPS Not Centered on Base

**Problem:** Kernel produces sensitivity IVPS values that are all different from base case - some higher, some lower, but none centered around base.

**Evidence from Smoke Test:**

Base Case IVPS: $294.09

| Driver | IVPS_Low | IVPS_High | Base |
|--------|----------|-----------|------|
| Gross_Monetization_Rate | $447 | $501 | $294 |
| CAC | $199 | $232 | $294 |
| MTM_Conversion_Rate | $387 | $420 | $294 |

Gross_Monetization_Rate: Both low ($447) and high ($501) scenarios produce IVPS > base ($294). This is mathematically impossible if the base case used the mid-point of the sensitivity range.

**Root Cause Hypothesis:**
The sensitivity analysis is likely using a different base configuration than the main valuation run. Possibilities:
- The sensitivity function is re-reading artifacts and getting different values
- The "low" and "high" multipliers are being applied incorrectly
- The base IVPS in sensitivity isn't the same as the main run

**Location:** `run_sensitivity_analysis()` function at line 602 of BASE_CVR_KERNEL_2.2.1e.py

**Files to Touch:**
- BASE_CVR_KERNEL_2.2.1e.py - debug and fix sensitivity function
- All downstream kernels with same function

**Complexity:** High - kernel code change

---

## (12) Market Price Lookup - Require WebSearch

**Problem:** T2 output used stale/hallucinated market price ($45) instead of actual (~$200). No WebSearch was called.

**Evidence from Smoke Test:**
```json
"Current_Market_Price": 45.0,
"Upside_Downside_Percent": 6.968
```

Actual DAVE price is ~$200, making the upside calculation completely wrong.

**Proposed Fix:**
Add to T2 protocol in CLAUDE.md and G3BASE:
```markdown
### Market Price Requirement

Before calculating upside/downside, you MUST:
1. Call WebSearch: "{TICKER} stock price"
2. Extract current market price from search results
3. Use this price in A.7 calculations
4. Document search timestamp

DO NOT use prices from source documents (stale) or from memory (potentially hallucinated).
```

**Files to Touch:**
- CLAUDE.md - Add to T2 protocol
- G3BASE_2.2.1e.md - Add to T2 requirements

**Complexity:** Low

---

## (14) Inter-Turn Validator Prompt - Opus-Powered Adversarial Review

**Status:** Architecture spec complete, prompt NOT written

**Why Opus (not Haiku):**

What Haiku would catch:
- JSON parses ✅
- Required fields present ✅
- Negative revenue ✅
- ROIC > 500% ✅

What Haiku would miss:
- FDSO 13.5M vs 14.5M (requires cross-referencing KG to source docs)
- Market price $45 vs $200 (requires world knowledge / search)
- Sensitivity IVPS not centered on base (requires understanding valuation math)
- Terminal ROIC 80% vs 38% target (requires reading REFINE intent)

**Validator Responsibilities (prompt to be written):**

1. **Data Integrity**
   - Share count (FDSO) matches source documents EXACTLY
   - Y0 financials match source within 2%
   - All KG values used consistently across artifacts

2. **Analytical Coherence**
   - DR derivation math is correct (RFR + ERP × X = DR)
   - Terminal ROIC consistent with stated assumptions
   - Sensitivity analysis centered on base case
   - IC formula produces reasonable terminal values

3. **Economic Realism** (beyond trivial bounds)
   - Revenue trajectory plausible given TAM/penetration
   - Margin evolution economically justified
   - ROIC trajectory sustainable or flagged

4. **Cross-Stage Consistency** (if validating REFINE or T2)
   - Values that should persist from prior stage do persist
   - Intentional changes are justified
   - No silent overwrites of prior-stage conclusions

**Output Format:**
```json
{
  "stage": "T1|REFINE|T2",
  "validation_model": "opus-4",
  "material_errors": [
    {
      "severity": "CRITICAL|HIGH|MEDIUM",
      "field": "FDSO",
      "expected": 14.5,
      "found": 13.5,
      "source": "10-K page 47",
      "ivps_impact_estimate": "+7%",
      "fix_required": true
    }
  ],
  "warnings": [],
  "overall": "PASS|FAIL",
  "blocking": true|false,
  "recommended_action": "Fix FDSO and re-run T2"
}
```

**Cost Tradeoff:** ~$0.50-1.00 per validation vs ~$0.01 for Haiku, but catches errors that matter

**Complexity:** Medium - prompt engineering, but no code changes
