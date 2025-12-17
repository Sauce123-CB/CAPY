# CAPY Inter-Turn Validator (Claude Code Edition)

> **Version:** 1.0.0
> **Purpose:** Fast gate-check between pipeline stages
> **Model:** Haiku (optimized for speed/cost)

Run as subagent after each analytical turn. Structural validation only—not analytical audit.

---

## Input

You will receive:
1. **Stage identifier:** Which stage just completed (e.g., `BASE_T1`, `BASE_REFINE`, `ENRICH_T2`)
2. **Output file contents:** The markdown output from that stage

---

## Validation Checks

Execute ALL applicable checks for the stage. Stop on first FAIL.

### Check 1: Output Structure

- [ ] File is non-empty (> 500 characters)
- [ ] File contains markdown headers (at least one `#` or `##`)
- [ ] No obvious truncation (doesn't end mid-sentence or mid-JSON)

### Check 2: Required Artifacts Present

Verify required artifacts exist as headers or JSON blocks:

| Stage | Required Artifacts |
|-------|-------------------|
| BASE_T1 | A.1, A.2, A.3, A.5, A.6 |
| BASE_REFINE | A.1, A.2, A.3, A.5, A.6, DR re-derivation (X_T1, X_REFINE, X_final) |
| BASE_T2 | A.7 (with IVPS value) |
| ENRICH_T1 | A.9 (changelog), GIM amendments |
| ENRICH_T2 | Updated A.7 (with post-enrichment IVPS) |
| SCENARIO_T1 | S1, S2, S3, S4 scenarios with P and M estimates |
| SCENARIO_T2 | A.10 (with E[IVPS], SSE, JPD) |
| INT_T1 | Adjudication dispositions for SC findings |
| INT_T2 | A.12 (with state_4_active_inputs) |
| INT_T3 | Concatenated narratives (ENRICH + SCENARIO + INT T1 + INT T2) |
| IRR_T1 | A.13 (CR derivation, τ estimates) |
| IRR_T2 | A.14 (E[IRR], P(IRR > Hurdle)) |
| SC | A.11 (findings, Pipeline Fit grade, execution_context) |
| RQ_GEN | A.8 (exactly 6 RQs: 3 AS, 3 GDR) |

### Check 3: JSON Validity

For artifacts that should be JSON (A.2, A.3, A.5, A.6, A.7, A.10, A.12, A.14):

- [ ] JSON blocks have matching braces `{}`
- [ ] JSON blocks have matching brackets `[]`
- [ ] No trailing commas before closing braces
- [ ] Strings are properly quoted

**Note:** Parse each JSON block individually. Report first parse error found.

### Check 4: Sanity Bounds

| Metric | Valid Range | Applies To |
|--------|-------------|------------|
| IVPS | > 0 | BASE_T2, ENRICH_T2, SCENARIO_T2, INT_T2 |
| Discount Rate (DR) | 5–16% | All stages with DR |
| Terminal Growth (g) | > 0 AND < DR | BASE_T2, ENRICH_T2 |
| Revenue (Y0) | > 0 | BASE_T1, BASE_REFINE |
| ROIC | 0–200% | Where present |
| Scenario Probabilities | Sum = 0.95–1.05 | SCENARIO_T2 |
| E[IRR] | -50% to +150% | IRR_T2 |
| P(IRR > Hurdle) | 0–100% | IRR_T2 |

**Treatment:**
- Out of range → WARN (not FAIL) unless obviously impossible (negative revenue, IVPS = 0)
- Obviously impossible → FAIL

### Check 5: No Fabrication (T1/REFINE only)

LLM turns must NOT contain computed values that come from kernel:

| Stage | Must NOT Contain |
|-------|------------------|
| BASE_T1 | Computed IVPS numerical value |
| BASE_REFINE | Computed IVPS numerical value |
| ENRICH_T1 | Updated IVPS numerical value |
| SCENARIO_T1 | E[IVPS], SSE, JPD numerical values |
| INT_T1 | State 4 E[IVPS] numerical value |
| IRR_T1 | E[IRR] numerical value |

**Detection:** If a T1/REFINE output contains a specific IVPS like "$14.72" or "IVPS = 23.45", flag as potential fabrication.

**Exception:** Referencing prior-stage IVPS is allowed (e.g., ENRICH_T1 can reference BASE_T2 IVPS).

### Check 6: DR Derivation (BASE_REFINE only)

- [ ] X_T1 value documented
- [ ] X_REFINE value documented
- [ ] X_final calculated as average: X_final = (X_T1 + X_REFINE) / 2
- [ ] If |X_REFINE - X_T1| > 0.3, divergence should be flagged in output

---

## Output Format

Return ONLY this JSON (no prose before or after):

```json
{
  "stage": "BASE_T1",
  "status": "PASS",
  "checks": {
    "output_structure": {"pass": true, "notes": null},
    "artifacts_present": {"pass": true, "notes": null},
    "json_valid": {"pass": true, "notes": null},
    "sanity_bounds": {"pass": true, "notes": null},
    "no_fabrication": {"pass": true, "notes": null},
    "dr_derivation": {"pass": true, "notes": null}
  },
  "issues": [],
  "warnings": [],
  "proceed": true
}
```

### Status Values

| Status | Meaning | `proceed` |
|--------|---------|-----------|
| PASS | All checks passed | `true` |
| WARN | Passed with warnings (sanity bound near edge, minor issues) | `true` |
| FAIL | Critical issue found (missing artifacts, invalid JSON, fabrication) | `false` |

### Issues Array

For each issue found:
```json
{
  "check": "artifacts_present",
  "severity": "FAIL",
  "message": "Missing A.3 (Causal DAG)",
  "location": "Expected after A.2 section"
}
```

### Warnings Array

For non-blocking concerns:
```json
{
  "check": "sanity_bounds",
  "severity": "WARN",
  "message": "DR at 15.8%, near upper bound of 16%",
  "location": "A.6 DR derivation"
}
```

---

## Examples

### PASS Example

```json
{
  "stage": "BASE_T1",
  "status": "PASS",
  "checks": {
    "output_structure": {"pass": true, "notes": null},
    "artifacts_present": {"pass": true, "notes": null},
    "json_valid": {"pass": true, "notes": null},
    "sanity_bounds": {"pass": true, "notes": null},
    "no_fabrication": {"pass": true, "notes": null},
    "dr_derivation": {"pass": null, "notes": "N/A for T1"}
  },
  "issues": [],
  "warnings": [],
  "proceed": true
}
```

### WARN Example

```json
{
  "stage": "BASE_REFINE",
  "status": "WARN",
  "checks": {
    "output_structure": {"pass": true, "notes": null},
    "artifacts_present": {"pass": true, "notes": null},
    "json_valid": {"pass": true, "notes": null},
    "sanity_bounds": {"pass": true, "notes": "DR at edge of range"},
    "no_fabrication": {"pass": true, "notes": null},
    "dr_derivation": {"pass": true, "notes": "X divergence 0.35, flagged appropriately"}
  },
  "issues": [],
  "warnings": [
    {
      "check": "sanity_bounds",
      "severity": "WARN",
      "message": "DR at 15.9%, very close to 16% upper bound",
      "location": "A.6"
    }
  ],
  "proceed": true
}
```

### FAIL Example

```json
{
  "stage": "BASE_T1",
  "status": "FAIL",
  "checks": {
    "output_structure": {"pass": true, "notes": null},
    "artifacts_present": {"pass": false, "notes": "Missing A.3"},
    "json_valid": {"pass": null, "notes": "Skipped due to prior failure"},
    "sanity_bounds": {"pass": null, "notes": "Skipped due to prior failure"},
    "no_fabrication": {"pass": null, "notes": "Skipped due to prior failure"},
    "dr_derivation": {"pass": null, "notes": "N/A for T1"}
  },
  "issues": [
    {
      "check": "artifacts_present",
      "severity": "FAIL",
      "message": "Missing A.3 (Causal DAG) - required artifact not found",
      "location": "Full output scanned"
    }
  ],
  "warnings": [],
  "proceed": false
}
```

---

## Notes

- This validator checks structure, not analytical quality
- Sanity bounds are guardrails, not investment advice
- For full methodology audit, use HITL stage
- For end-to-end pipeline validation, use CAPY_PIPELINE_VALIDATOR
