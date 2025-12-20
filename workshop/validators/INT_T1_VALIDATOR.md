# INTEGRATION T1 Validator

> **Version:** 2.2.2e
> **Model:** Opus (REQUIRED - do NOT use Haiku)
> **Pattern:** 7 (Validators after each turn)

## Purpose

Validate INTEGRATION T1 (Adjudication) output before proceeding to T2 (Recalculation).

T1 adjudicates Silicon Council findings and produces:
- Disposition decisions for all CRITICAL and HIGH findings
- Scenario reconciliation results
- T1 Handoff JSON with cascade scope and modifications

---

## Inputs

Read the T1 output file:
- `{output_dir}/{TICKER}_INT_T1_{DATE}.md`

Also read (for cross-validation):
- `{analysis_dir}/07_SILICON_COUNCIL/{TICKER}_A11_AUDIT_REPORT.json` (to verify all findings addressed)

---

## Validation Checks

### 1. T1 Handoff JSON Presence

**Check:** T1 output contains embedded T1 Handoff JSON block.

**Pass Criteria:**
- JSON block is present (search for "T1 Handoff" or similar header)
- JSON is well-formed (parseable)
- Contains required top-level keys: `cascade_scope`, `modifications_to_apply`, `scenarios_finalized`

**Fail:** Missing or malformed T1 Handoff JSON blocks T2 execution.

### 2. CRITICAL Findings Disposition

**Check:** Every CRITICAL finding from A.11 has an explicit disposition.

**Pass Criteria:**
- Each CRITICAL finding has disposition: ACCEPT, REJECT, or MODIFY
- Each disposition includes rationale referencing evidence
- No CRITICAL findings are unaddressed

**Fail:** Unaddressed CRITICAL findings violate P4 (Priority-Based Adjudication Protocol).

### 3. HIGH Findings Disposition

**Check:** Every HIGH finding from A.11 has an explicit disposition.

**Pass Criteria:**
- Each HIGH finding has disposition: ACCEPT, REJECT, or MODIFY
- Each disposition includes rationale
- REJECT dispositions include substantive justification per P1 (Evidentiary Hierarchy)

**Fail:** Unaddressed HIGH findings violate P4.

### 4. Cascade Scope Validity

**Check:** `cascade_scope` is a valid enum value.

**Valid Values:**
- `FULL` - GIM modifications require full recalculation
- `PARTIAL_SCENARIO` - Scenario interventions modified
- `PARTIAL_SSE` - Probabilities only changed
- `NONE` - No modifications accepted; State 4 = State 3

**Fail:** Invalid cascade_scope blocks T2 execution.

### 5. Modifications Consistency

**Check:** If `cascade_scope` != `NONE`, then `modifications_to_apply` must be non-empty.

**Pass Criteria:**
- `cascade_scope = NONE` → `modifications_to_apply` is empty or absent
- `cascade_scope != NONE` → `modifications_to_apply` contains at least one modification

Each modification should specify:
- `affected_artifact` (e.g., "A.5_GIM", "A.10_S2")
- `affected_element` (e.g., "Revenue_Growth_Y1")
- `from_value` (pre-adjudication)
- `to_value` (post-adjudication)
- `finding_id` (reference to adjudication decision)

**Fail:** Inconsistency between cascade_scope and modifications_to_apply.

### 6. Scenarios Constraint

**Check:** `scenarios_finalized` contains at most 4 scenarios.

**Pass Criteria:**
- Array length ≤ 4
- Each scenario has: `scenario_id`, `scenario_name`, `p_posterior`, `ivps_impact`
- Probabilities are valid (0-1 range, not obviously miscalculated)

**Fail:** More than 4 scenarios violates the 4-Scenario Limit (Section II.E).

### 7. Distributional Balance

**Check:** Finalized scenario set includes both upside and downside coverage.

**Pass Criteria:**
- At least one scenario with positive `ivps_impact` (upside)
- At least one scenario with negative `ivps_impact` (downside)
- OR explicit justification for directional skew documented

**Warn:** Unbalanced distribution without justification.

### 8. Audit Synthesis Documentation (Multi-SC)

**Check:** If multiple SC instances were processed, synthesis is documented.

**Pass Criteria:**
- Concordance analysis present (which findings flagged by multiple SCs)
- Pipeline Fit grade handling documented (modal grade if grades varied)
- Finding attribution preserved (which SC raised each finding)

**Warn:** Missing synthesis documentation for multi-SC input.

---

## Output Format

### PASS

```
INT T1 VALIDATOR: PASS

Summary:
- Findings Adjudicated: {N} CRITICAL, {M} HIGH, {K} MEDIUM
- Dispositions: {A} ACCEPT, {R} REJECT, {M} MODIFY
- Cascade Scope: {cascade_scope}
- Scenarios Finalized: {count}
- Pipeline Fit Grade: {grade}

T1 validated. Proceed to T2.
```

### FAIL

```
INT T1 VALIDATOR: FAIL

Critical Issues:
1. [Check N]: {Issue description}
   Location: {Where in T1 output}
   Impact: {Why this blocks T2}

Required Fixes:
- {Specific action to remediate}

Re-run T1 before proceeding to T2.
```

### WARN (Proceed with Caveats)

```
INT T1 VALIDATOR: PASS WITH WARNINGS

Warnings:
1. [Check N]: {Issue description}

Proceed to T2, but note caveats in A.12.
```

---

## Validator Execution

1. Read T1 output file
2. Parse embedded JSON blocks
3. Cross-reference with A.11 to verify finding coverage
4. Execute all checks above
5. Emit validation result

**Return:** Validation result only. Do NOT return the full T1 content.

---

*END OF INT T1 VALIDATOR*
