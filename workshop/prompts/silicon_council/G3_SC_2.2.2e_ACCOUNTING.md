# **G3 SILICON COUNCIL 2.2.2e: Accounting Audit**

> **Preamble:** This audit is part of the atomized Silicon Council framework.
> Read G3_SC_2.2.2e_PREAMBLE.md for mission, inputs, and guiding principles.

## **AUDIT OBJECTIVE: Source Integrity (HIGHEST PRIORITY)**

Data integrity errors propagate through the entire valuation and invalidate
downstream analysis regardless of its sophistication. Errors in multi-stage
pipelines are common. Your task is to find them.

### **A.1 Input Error Identification**

Assume the upstream analysis contains at least one material input error.
Identify the highest-sensitivity inputs and hunt for discrepancies between:

- Artifact values and source documents

- Metric definitions used vs. what the methodology mathematically requires

Common failure modes include inputs that appear numerically correct but are
semantically misaligned with methodology requirements --- the right number
for the wrong concept.

### **A.2 Transcription Risk Stratification**

Not all data transcription carries equal error risk. LLM transcription of
straightforward items --- management guidance, headline KPIs, clearly stated
figures --- is generally reliable. Error concentrates in complex or
company-specific accounting where judgment and contextual interpretation
are required.

High-risk areas demanding explicit reconciliation to GAAP (non-exhaustive):

- **Adjusted metrics (Adj. EBITDA, Adj. FCF, Adj. Earnings):** Reconcile each
  adjustment; verify the adjustment set is complete and internally consistent

- **CapEx decomposition:** Confirm maintenance vs. growth CapEx split
  methodology; verify treatment aligns with terminal ROIC assumptions

- **D&A:** Verify alignment with asset base; check for impairments,
  accelerated depreciation, or acquisition-related step-ups

- **One-time items and discontinued operations:** Confirm treatment matches
  the valuation's normalization approach

- **M&A and new divisions:** Verify consolidation timing, pro forma
  adjustments, and whether acquired economics are properly isolated

- **Receivables and working capital:** Check for factoring, securitization,
  or classification changes that distort operating cash conversion

- **Stock-based compensation:** Confirm whether included in operating costs;
  verify dilution treatment in share count

- **Debt paydown and capital structure:** Verify schedule matches Simplified
  APV assumptions

The notes to the financial statements are the primary disambiguation tool.
Use them to reconcile reported figures to GAAP and verify the economic
substance of adjustments.

### **A.2.5 ATP Reconciliation Verification**

The BASE stage executes an Accounting Translation Protocol (ATP) that
reconciles reported figures to economic definitions before they become
DAG inputs. Verify that:

- The `accounting_translation_log` in A.2 documents reconciliation
  for all high-risk categories material to this company

- The complexity assessment (LOW / MODERATE / HIGH) in A.2 metadata is
  appropriate given the company's accounting profile

- ATP reconciliations are consistent with normative definitions (e.g.,
  EBIT includes SBC per Section 1.1)

- Any "flags" in the ATP log (unreconciled items, conservative
  estimates) were appropriately addressed in downstream stages

- Y0_data values reflect ATP-reconciled economic values, not raw
  reported figures

If ATP-Lite was applied, verify the justification for LOW complexity
assessment is sound. Companies with adjusted metrics, complex revenue
recognition, or M&A activity should have triggered Full ATP.

### **A.3 Artifact Consistency Verification**

Downstream artifacts (DAG, GIM, A.10 scenario interventions) must faithfully
represent the accounting structure established in source analysis. A distinct
failure mode occurs when definitional drift corrupts the pipeline --- for
example, using EBITDA in DAG construction but Adj. EBITDA in scenario
magnitude estimation, or applying inconsistent adjustment sets across A.5
and A.9 changelogs.

Verify that:

- All DAG nodes and GIM drivers reference metrics consistent with normative
  definitions established in A.2/A.3 artifacts

- The same economic concept uses the same numerical value and definitional
  basis throughout the pipeline

- Structural choices in the model reflect the actual accounting and
  operational structure of the target company, not a simplified proxy

Inconsistency between artifact structure and economic reality is a material
error even when individual numbers are transcribed correctly.

### **A.4 Definitional Alignment**

Trace from methodology mechanics back to inputs. For each critical input,
ask: what does the formula require, and is that what was actually provided?

Margin inputs that exclude real operating costs, share counts on wrong basis,
growth rates across inconsistent periods, and capital metrics misaligned with
ROIC computation are common sources of material error.

### **A.5 Citation Spot-Check**

Select material quantitative claims from upstream artifacts. Verify cited
sources contain the stated figures in the stated context.

## **OUTPUT REQUIREMENT**

Report the most material data integrity risk identified, even if uncertain.
If no errors are found after rigorous review, state the specific verification
steps taken and why confidence is high. Do not declare PASS without explicit
justification of the audit trail.

**Narrative (N0):** Source Integrity Audit --- Report the most material data
integrity risk identified. What input error, if present, would most damage
the valuation? What verification was performed? If no error was found,
justify confidence by documenting the specific checks conducted.

## **OUTPUT SCHEMA**

Write the following JSON to `{output_dir}/SC_ACCOUNTING_AUDIT.json`:

```json
{
  "audit_type": "ACCOUNTING",
  "source_integrity": {
    "highest_risk_finding": "string (Most material data integrity risk)",
    "verification_performed": [
      "string (List of specific verification steps taken)"
    ],
    "confidence_justification": "string (Why confidence is high if no errors found)",
    "atp_compliance": {
      "status": "string (COMPLIANT | PARTIAL | NON_COMPLIANT)",
      "findings": "string (Summary of ATP reconciliation review)"
    },
    "artifact_consistency": {
      "status": "string (CONSISTENT | DRIFT_DETECTED | MATERIAL_ERROR)",
      "findings": "string (Summary of cross-artifact consistency check)"
    },
    "citation_spot_check": {
      "claims_verified": "integer (Number of claims spot-checked)",
      "discrepancies_found": "integer (Number of discrepancies)",
      "details": "string (Summary of spot-check findings)"
    }
  },
  "narrative_n0": "string (Source Integrity Assessment narrative)"
}
```

*END OF G3 SILICON COUNCIL 2.2.2e ACCOUNTING AUDIT*
