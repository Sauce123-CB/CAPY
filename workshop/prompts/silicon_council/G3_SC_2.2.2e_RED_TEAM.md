# **G3 SILICON COUNCIL 2.2.2e: Red Team Audit**

> **Preamble:** This audit is part of the atomized Silicon Council framework.
> Read G3_SC_2.2.2e_PREAMBLE.md for mission, inputs, and guiding principles.

## **AUDIT OBJECTIVE: Red Team Adversarial Review**

**Mission:** Adopt the persona of a skeptical short-seller or
adversarial analyst with access to all the same evidence. Your goal is
to identify failure modes, overlooked risks, and gaps in the analysis.

**The Red Team Mandate:** This is not a balanced review. You are
explicitly seeking weaknesses. The upstream stages were designed to
construct the best case for the valuation; your role is to stress-test
it.

### **C.1. "What Could Go Wrong" Analysis**

Assume the E[IVPS] is materially incorrect. Generate the most
compelling explanations:

- **If Overvalued:** What are the 3-5 assumptions or judgments most
  likely to be wrong on the downside? What evidence might have been
  underweighted? What risks might have been dismissed too easily?

- **If Undervalued:** What opportunities might the analysis have been
  too conservative on? Is there upside optionality not captured in
  the scenario design?

For each identified failure mode:

- Cite the specific assumption or judgment (GIM driver, scenario P,
  intervention design)

- Explain the mechanism by which it could fail

- Assess the materiality (impact on IVPS if wrong)

### **C.2. "What Was Overlooked" Analysis**

Independently review the source materials (company docs, RQs) to
identify:

- **Evidence Gaps:** What important questions were not asked in the
  RQs? What documents are missing that would be material?

- **Analytical Omissions:** What analytical frameworks or
  considerations are absent from the TRACE documentation? (e.g., Was
  competitive positioning adequately analyzed? Was management
  quality deeply assessed? Was capital allocation history examined?)

- **Scenario Completeness:** Are there plausible material scenarios
  that were not modeled? Is the scenario set skewed (all upside, or
  all downside)?

### **C.3. LLM-Specific Bias Detection**

The upstream stages were executed by LLMs, which have characteristic
failure modes:

- **Over-Narrativity:** Is the analysis suspiciously coherent? Do all
  the pieces fit together "too well"? Real companies have
  contradictions and loose ends.

- **Analytical Capture / "Hall of Mirrors":** Is the model
  internally consistent but potentially detached from reality? Are
  the implied multiples, market share, or competitive position
  plausible when compared to external benchmarks?

- **Anchoring on Management Narrative:** Did the analysis sufficiently
  apply the "Adversarial De-Framing Mandate"? Or did it accept
  management's chosen metrics and framing uncritically?

- **Conjunction Fallacy in Scenarios:** Are scenario probabilities
  reasonable, or do they require an implausible chain of events to
  all go right (or wrong)?

## **OUTPUT REQUIREMENT**

**Narrative (N3):** Red Team Synthesis --- The adversarial narrative---the
strongest case against the valuation. What could go wrong, and what was missed?

## **OUTPUT SCHEMA**

Write the following JSON to `{output_dir}/SC_RED_TEAM_AUDIT.json`:

```json
{
  "audit_type": "RED_TEAM",
  "red_team_findings": {
    "failure_modes": [
      {
        "finding_id": "string (e.g., RT01)",
        "failure_type": "string (OVERVALUATION_RISK | UNDERVALUATION_RISK | MODEL_FRAGILITY)",
        "target_assumption": "string (Specific GIM driver, scenario, or judgment)",
        "failure_mechanism": "string (How this could go wrong)",
        "materiality": "string (HIGH | MEDIUM | LOW)",
        "ivps_impact_estimate": "string (Qualitative or quantitative estimate of impact if wrong)"
      }
    ],
    "overlooked_considerations": [
      {
        "finding_id": "string (e.g., OC01)",
        "category": "string (EVIDENCE_GAP | ANALYTICAL_OMISSION | SCENARIO_GAP)",
        "description": "string (What was missed)",
        "potential_significance": "string (Why this matters)"
      }
    ],
    "llm_bias_flags": [
      {
        "bias_type": "string (OVER_NARRATIVITY | ANALYTICAL_CAPTURE | ANCHORING_ON_MANAGEMENT | CONJUNCTION_FALLACY)",
        "evidence": "string (Specific indicators of this bias)",
        "severity": "string (HIGH | MEDIUM | LOW)"
      }
    ],
    "adversarial_narrative": "string (The synthesized Red Team case against the valuation)"
  },
  "narrative_n3": "string (Red Team Synthesis narrative)"
}
```

*END OF G3 SILICON COUNCIL 2.2.2e RED TEAM AUDIT*
