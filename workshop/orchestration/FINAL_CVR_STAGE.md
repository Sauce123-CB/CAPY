# FINAL CVR Generation (Post-IRR)

> **Version:** 1.0.0
> **Extracted from:** Mega-patch plan Section 5
> **Pipeline Position:** Stage 9 of 9 (IRR → FINAL_CVR)

---

## Purpose

Generate the final human-readable CVR document ONCE, after the entire pipeline completes (post-IRR). This uses a Bash script, not Claude, to avoid truncation.

## What Goes In the Final CVR

**INCLUDE (in order):**
1. Header (ticker, date, E[IVPS], E[IRR], Pipeline Fit grade)
2. **N1:** Investment Thesis
3. **N2:** Invested Capital Modeling
4. **N3:** Economic Governor & Constraints
5. **N4:** Risk Assessment
6. **N5:** Enrichment Synthesis
7. **N6:** Scenario Model Synthesis
8. **N7:** Adjudication Synthesis
9. **N8:** IRR & Expected Return Analysis
10. **A.1-A.7:** Epistemic anchors through valuation
11. **A.10:** Scenario model
12. **A.12-A.14:** Integration trace, resolution timeline, IRR analysis

**EXCLUDE (remain in folder for audit trail):**
- RQ1-RQ7 (research inputs)
- A.8, A.9 (research plan/results)
- SC_* audits, A.11 (audit trail - findings already adjudicated into A.12)
- Kernel receipts (reproducibility artifacts)
- PIPELINE_STATE.md (orchestration state)

## Execution

```bash
# Run AFTER IRR stage completes
./workshop/scripts/generate_final_cvr.sh {TICKER} {analysis_dir}/09_IRR/
```

## Script Location

`workshop/scripts/generate_final_cvr.sh`

## Stage Flow

```
┌─────────────────────────────────────────────────────────────┐
│ FINAL_CVR (Bash Script - NO Claude)                         │
│    Input:  09_IRR/ folder with all _IRR artifacts           │
│    Script: workshop/scripts/generate_final_cvr.sh           │
│    Output: {TICKER}_FINAL_CVR.md (consolidated document)    │
│                                                             │
│    1. Concatenate N1-N8 narratives in order                 │
│    2. Embed A.1-A.7, A.10, A.12-A.14 as JSON blocks         │
│    3. Add header with summary metrics                       │
│    4. Write to {analysis_dir}/{TICKER}_FINAL_CVR.md         │
└─────────────────────────────────────────────────────────────┘
```

## Why Bash, Not Claude

1. **No truncation:** Bash `cat` preserves exact content
2. **Single concatenation:** No intermediate docs at each stage
3. **Curated content:** Final CVR contains analytical output, not working papers
4. **Audit trail preserved:** RQs, SC audits remain in folders for reproducibility

## Critical Patterns Applied

| Pattern | Application |
|---------|-------------|
| Pattern 11: Surgical Stitching | Concatenate from IRR outputs, no regeneration |
| Pattern 12: Canonical Snapshot | 09_IRR/ contains complete artifact set |
