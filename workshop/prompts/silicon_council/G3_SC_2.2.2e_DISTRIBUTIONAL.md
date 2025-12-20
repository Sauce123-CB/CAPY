# **G3 SILICON COUNCIL 2.2.2e: Distributional Audit**

> **Preamble:** This audit is part of the atomized Silicon Council framework.
> Read G3_SC_2.2.2e_PREAMBLE.md for mission, inputs, and guiding principles.

## **AUDIT OBJECTIVE: Distributional Coherence Review**

**Mission:** Assess whether the probabilistic output (the IVPS
distribution from SSE) is coherent, well-characterized, and
appropriately interpreted.

### **D.1. Distribution Shape Analysis**

Review the distribution_statistics and distribution_shape in A.10:

- Is the skewness logically explained? What scenarios drive the
  asymmetry?

- If the distribution is bimodal, does this reflect genuine binary
  uncertainty or modeling artifact?

- Are the tails (P10, P90) plausible? Do they represent realistic
  extremes or arbitrary bounds?

### **D.2. Investment Implications Coherence**

Review the investment_implications in A.10:

- Does the position sizing guidance logically follow from the
  distribution shape?

- Are the risk management considerations appropriate given the tail
  exposures?

- Are the "key monitoring indicators" genuinely informative for
  updating scenario probabilities?

### **D.3. Base Case vs. E[IVPS] Attribution**

Review the cvr_state_bridge:

- Is the delta between deterministic Base Case and E[IVPS]
  well-explained?

- Does the attribution to specific scenarios make sense?

- If E[IVPS] is materially different from Base Case, is this driven
  by asymmetric scenarios or probability-weighted tail effects?

## **OUTPUT REQUIREMENT**

Assess distributional coherence and investment implications alignment.

**Narrative (N4):** Distributional Coherence --- Assessment of whether the
IVPS distribution is well-characterized and the investment implications
logically follow from the distribution shape.

## **OUTPUT SCHEMA**

Write the following JSON to `{output_dir}/SC_DISTRIBUTIONAL_AUDIT.json`:

```json
{
  "audit_type": "DISTRIBUTIONAL",
  "distributional_coherence": {
    "shape_assessment": {
      "status": "string (COHERENT | CONCERNS | PROBLEMATIC)",
      "findings": "string (Assessment of distribution shape, skewness, modality)"
    },
    "investment_implications_assessment": {
      "status": "string (SOUND | PARTIAL | WEAK)",
      "findings": "string (Assessment of whether investment implications follow from distribution)"
    },
    "base_case_attribution": {
      "status": "string (WELL_EXPLAINED | PARTIAL | UNCLEAR)",
      "findings": "string (Assessment of E[IVPS] vs Base Case delta explanation)"
    }
  },
  "narrative_n4": "string (Distributional coherence narrative)"
}
```

*END OF G3 SILICON COUNCIL 2.2.2e DISTRIBUTIONAL AUDIT*
