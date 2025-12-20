# **G3 SILICON COUNCIL 2.2.2e: Fit Audit**

> **Preamble:** This audit is part of the atomized Silicon Council framework.
> Read G3_SC_2.2.2e_PREAMBLE.md for mission, inputs, and guiding principles.
>
> **Additional Reference:** This audit requires G3_SC_2.2.2e_BLIND_SPOTS.md
> for detailed blind spot descriptions.

## **AUDIT OBJECTIVE: Pipeline Fit Assessment**

**Mission:** Evaluate whether this security is well-suited to the CAPY
pipeline's current analytical constraints, or whether significant
unmodeled factors limit the reliability of the valuation.

**Context:** The CAPY pipeline, in its current form, employs a 20-year
deterministic DCF augmented by discrete Structured State Enumeration
(SSE). While powerful, this methodology has known blind spots. The
"Future Simulator" vision (full Monte Carlo with dynamic macro states,
complex capital allocation, and interwoven scenarios) remains
aspirational. Your task is to explicitly flag where the gap between
current capabilities and ideal modeling creates material uncertainty.

## **The Pipeline Blind Spots Rubric**

Evaluate the target security against each of the following known
limitations. For each that applies, assess severity (HIGH / MEDIUM /
LOW) based on materiality to the valuation:

| **Blind Spot** | **Description** | **Warning Signs** |
|----------------|-----------------|-------------------|
| **Debt Dynamics** | The pipeline uses Simplified APV with static Y0 balance sheet. Companies with complex debt structures, refinancing risk, or material leverage may be poorly modeled. | Net Debt / EBITDA > 3x; Near-term debt maturities; Variable rate exposure; Covenant constraints |
| **Pre-Revenue / Early-Stage** | DCF requires forecasting cash flows from an established base. Pre-revenue companies rely heavily on speculative assumptions. | No or minimal revenue; Business model unproven; Heavy reliance on TAM-based reasoning |
| **Critical Document Gaps** | The pipeline ingests company filings and RQ outputs. Some securities require specialized documents the pipeline may not access (e.g., clinical trial data, patent filings, regulatory submissions). | Biotech with Ph3 drugs; IP-dependent businesses; Heavily regulated industries with pending decisions |
| **Balance Sheet Complexity** | Hidden asset value, cross-shareholdings, or trading below book value may not be captured by earnings-based valuation. | Price < Book Value; Significant investment securities on B/S; Real estate holdings at historical cost; Japanese corporate structure |
| **Conglomerate Structure** | Multi-segment businesses with disparate economics are difficult to model in a unified SCM. Sum-of-parts may diverge significantly from consolidated approach. | >3 distinct business segments; Segments with different risk profiles; Holding company structure |
| **Extreme Management Scenarios** | Activist situations, succession risk, fraud potential, or governance complexity may dominate value but are poorly captured in base case modeling. | Recent activist involvement; Key-person risk; Governance red flags from RQ1 |
| **Complex Share Dynamics** | Beyond SBC, complex equity structures (converts, warrants, earnouts, multi-class shares) may materially affect per-share value. | Outstanding convertible instruments; Earnout liabilities; Multi-class voting structure |
| **Macro/Industry Sensitivity** | The pipeline models company-specific scenarios but does not simulate macro cycles or rates sensitivity. Companies highly correlated with macro may be mispriced. | Commodity exposure; High operating leverage; Rate-sensitive business model; Strong beta to economic cycles |
| **Cyclicality** | Secular growth assumptions may miss cyclical dynamics (semiconductor cycles, commodity supercycles, credit cycles). | Historically cyclical industry; Current position in cycle unclear; Mean reversion timing uncertain |
| **Real Options** | Companies with significant embedded optionality (exploration assets, platform expansion potential, pivot options) may be systematically undervalued by DCF. | Early-stage platform; Multiple strategic paths; Optionality not captured in scenario design |
| **Binary Regulatory Events** | Where outcomes are genuinely binary with highly uncertain base rates, probability estimation may be poorly calibrated. | Pending FDA decisions; Antitrust review; Material litigation with uncertain outcome |
| **Interconnections and Non-Linearities** | The above factors often interact. High leverage + cyclicality creates different risk than either alone. | Multiple blind spots flagged; Factors compound in stress scenarios |

See G3_SC_2.2.2e_BLIND_SPOTS.md for detailed descriptions of each blind spot.

## **OUTPUT REQUIREMENT**

Produce a Pipeline Fit Grade (A through F) with specific flags and
interpretation guidance. This assessment is informational for human
auditors who can contextualize appropriately; it does not automatically
invalidate the analysis.

**Grade Definitions:**

- **A:** Well-suited to methodology; minimal unmodeled factors
- **B:** Some blind spots; manageable with noted caveats
- **C:** Material blind spots; interpret with significant caution
- **D:** Multiple severe blind spots; methodology may be inappropriate
- **F:** Fundamental mismatch; recommend alternative analysis approach

**Narrative (N1):** Pipeline Fit Summary --- A concise assessment of how
well this security fits the pipeline's current constraints. Highlight the
most material blind spots.

## **OUTPUT SCHEMA**

Write the following JSON to `{output_dir}/SC_FIT_AUDIT.json`:

```json
{
  "audit_type": "FIT",
  "pipeline_fit_assessment": {
    "grade": "string (A | B | C | D | F)",
    "grade_rationale": "string (Brief explanation of grade)",
    "blind_spot_flags": [
      {
        "blind_spot_id": "string (e.g., DEBT_DYNAMICS)",
        "severity": "string (HIGH | MEDIUM | LOW)",
        "description": "string (Specific concern for this security)",
        "valuation_implication": "string (How this affects interpretation of E[IVPS])"
      }
    ],
    "interpretation_guidance": "string (How the human auditor should contextualize the valuation given these flags)"
  },
  "narrative_n1": "string (Pipeline Fit Summary narrative)"
}
```

*END OF G3 SILICON COUNCIL 2.2.2e FIT AUDIT*
