# **G3 SILICON COUNCIL 2.2.2e: Economic Realism Audit**

> **Preamble:** This audit is part of the atomized Silicon Council framework.
> Read G3_SC_2.2.2e_PREAMBLE.md for mission, inputs, and guiding principles.

## **AUDIT OBJECTIVE: Economic Realism**

**Mission:** Step back from the bottom-up mechanics and assess whether the
valuation's implied outcomes are plausible in the real economy. This is a
top-down sanity check that complements the detailed audits.

**Context:** The other audits verify internal consistency, methodological
compliance, and adversarial stress-testing. This audit asks a different
question: **"If this valuation is correct, what does that imply about the
company's future position in the economy, and is that plausible?"**

**Distinction from Red Team:** The Red Team audit adopts an adversarial
stance ("attack the valuation"). This audit adopts a calibrating stance
("is this economically sensible?"). Red Team asks "what could go wrong?"
Economic Realism asks "does this make sense?"

## **The Economic Realism Checklist**

### **E.1. Implied Market Position at Terminal**

Extract the terminal state metrics (Y20) and assess plausibility:

- **Implied Revenue Scale:** What is the Y20 revenue? Is this plausible
  given the company's current position and addressable market?

- **Implied Market Share:** If the TAM is known, what market share does
  the terminal revenue imply? Is this share achievable given competitive
  dynamics?

- **Implied Competitive Position:** Does the terminal state assume the
  company becomes a dominant player, maintains current position, or
  declines? Is this consistent with the industry's competitive structure?

### **E.2. Implied Margins vs. Industry Economics**

Assess whether the margin trajectory is economically justified:

- **Terminal EBIT Margin:** What margin does the model assume at Y20?
  How does this compare to:
  - Current company margin
  - Industry average margin
  - Best-in-class peer margins

- **Margin Premium Justification:** If the terminal margin exceeds
  industry average, what structural advantage justifies this? Is the
  advantage durable for 20 years?

- **Margin Compression Risk:** If the model assumes margin expansion,
  is there a plausible mechanism? Or is this "hope as a strategy"?

### **E.3. Implied Growth Persistence**

Assess whether the growth assumptions are economically realistic:

- **CAGR Plausibility:** What is the implied revenue CAGR from Y0 to Y20?
  How does this compare to:
  - Historical company growth
  - Industry growth rates
  - Base rate distributions for companies of similar size/stage

- **Size vs. Growth Tension:** Large companies grow slower. If Y20 revenue
  is large, does the late-period growth rate reflect this reality?

- **S-Curve Saturation:** If S_CURVE assumptions are used, is the
  saturation point aligned with realistic market size estimates?

### **E.4. Implied Multiples Sanity Check**

Calculate and assess the implied valuation multiples:

- **Current Implied Multiples:** Given E[IVPS] and current fundamentals,
  what P/E, EV/EBITDA, EV/Revenue, and P/FCF does the valuation imply?

- **Peer Comparison:** How do these multiples compare to:
  - Direct competitors
  - Industry medians
  - Historical trading ranges for this company

- **Multiple Expansion/Compression:** Does the valuation implicitly assume
  multiple expansion from current levels? Is this justified?

### **E.5. Terminal State Economic Governor**

Beyond the mechanical g ≈ ROIC × RR check, assess economic plausibility:

- **Terminal ROIC Sustainability:** Is the terminal ROIC (often 30-50%+)
  sustainable given:
  - Competitive entry dynamics
  - Technology obsolescence risk
  - Mean reversion tendencies in the industry

- **Terminal Growth Sustainability:** Is terminal g consistent with:
  - Long-run GDP growth (typically 2-3% nominal)
  - Industry maturity trajectory
  - Company lifecycle stage at Y20

- **Reinvestment Opportunity:** Does the terminal reinvestment rate imply
  plausible capital deployment opportunities?

### **E.6. Cross-Scenario Economic Coherence**

Assess whether the scenario outcomes are collectively plausible:

- **Scenario Spread:** Is the range of outcomes (P10 to P90) economically
  realistic? Neither too narrow (false precision) nor too wide (model
  instability)?

- **Scenario Independence:** Do the scenarios describe genuinely different
  economic futures, or are they variations on the same theme?

- **Extreme State Plausibility:** In the best and worst SSE states, are
  the implied company economics (revenue, margin, ROIC) plausible?

## **OUTPUT REQUIREMENT**

Provide a top-down economic plausibility assessment. This is not about
finding errors in methodology, but about stepping back and asking:
"Does this make sense as a description of a possible economic future?"

**Narrative (N5):** Economic Realism Assessment --- Summary of whether the
valuation's implied outcomes are plausible in the real economy. Highlight
any implied metrics that strain credulity.

## **OUTPUT SCHEMA**

Write the following JSON to `{output_dir}/SC_ECONOMIC_REALISM_AUDIT.json`:

```json
{
  "audit_type": "ECONOMIC_REALISM",
  "economic_realism": {
    "overall_status": "string (PLAUSIBLE | CONCERNS | IMPLAUSIBLE)",
    "implied_market_position": {
      "terminal_revenue": "float (Y20 revenue in $M)",
      "implied_market_share": "float or null (If TAM known, implied share %)",
      "plausibility": "string (PLAUSIBLE | STRETCH | IMPLAUSIBLE)",
      "findings": "string (Assessment of terminal market position)"
    },
    "implied_margins": {
      "terminal_ebit_margin": "float (Y20 EBIT margin %)",
      "industry_average_margin": "float or null (Industry benchmark if known)",
      "margin_premium_justified": "boolean",
      "findings": "string (Assessment of margin plausibility)"
    },
    "implied_growth": {
      "y0_y20_cagr": "float (Implied revenue CAGR %)",
      "base_rate_percentile": "string or null (Where this CAGR falls in base rate distribution)",
      "size_growth_coherence": "string (COHERENT | TENSION | PROBLEMATIC)",
      "findings": "string (Assessment of growth persistence plausibility)"
    },
    "implied_multiples": {
      "current_implied_pe": "float or null",
      "current_implied_ev_ebitda": "float or null",
      "current_implied_ev_revenue": "float or null",
      "peer_comparison": "string (PREMIUM | INLINE | DISCOUNT)",
      "findings": "string (Assessment of multiple plausibility)"
    },
    "terminal_economics": {
      "terminal_roic": "float (Terminal ROIC %)",
      "terminal_g": "float (Terminal growth %)",
      "roic_sustainability": "string (SUSTAINABLE | QUESTIONABLE | IMPLAUSIBLE)",
      "g_sustainability": "string (SUSTAINABLE | QUESTIONABLE | IMPLAUSIBLE)",
      "findings": "string (Assessment of terminal state sustainability)"
    },
    "cross_scenario_coherence": {
      "outcome_range_p10_p90": "string ($X to $Y IVPS)",
      "range_assessment": "string (APPROPRIATE | TOO_NARROW | TOO_WIDE)",
      "extreme_state_plausibility": "string (PLAUSIBLE | CONCERNS | IMPLAUSIBLE)",
      "findings": "string (Assessment of scenario set coherence)"
    },
    "critical_concerns": [
      {
        "concern_id": "string (e.g., ER01)",
        "metric": "string (Which implied metric is problematic)",
        "implied_value": "string (What the model implies)",
        "benchmark": "string (What would be realistic)",
        "severity": "string (HIGH | MEDIUM | LOW)",
        "interpretation_impact": "string (How this should affect confidence in E[IVPS])"
      }
    ]
  },
  "narrative_n5": "string (Economic Realism Assessment narrative)"
}
```

## **REFERENCE: Base Rate Benchmarks**

When assessing plausibility, compare implied metrics to these base rates:

| Metric | Median | 75th %ile | 90th %ile | Notes |
|--------|--------|-----------|-----------|-------|
| Revenue CAGR (10Y) | 5-7% | 12-15% | 20%+ | Size-dependent; smaller companies can sustain higher |
| EBIT Margin (S&P 500) | 12-15% | 20% | 30%+ | Industry-dependent |
| Terminal ROIC | 10-15% | 20-25% | 35%+ | Mean-reverts toward WACC long-term |
| Terminal g | 2-3% | 3-4% | 4-5% | Should not exceed long-run nominal GDP |
| P/E (S&P 500) | 18-22x | 25-30x | 40x+ | Growth expectations embedded |
| EV/EBITDA | 10-12x | 15-18x | 25x+ | Industry-dependent |

These are rough heuristics. Use WebSearch to retrieve current benchmarks
for the specific industry if available.

*END OF G3 SILICON COUNCIL 2.2.2e ECONOMIC REALISM AUDIT*
