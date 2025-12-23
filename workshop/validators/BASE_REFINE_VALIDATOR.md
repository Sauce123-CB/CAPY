# BASE REFINE Validator

> **Version:** 2.2.3e
> **Model:** Opus (REQUIRED - do NOT use Haiku)
> **Pattern:** 7 (Validators after each turn)

## Purpose

Validate BASE REFINE output before proceeding to T2 (kernel execution).

REFINE expands the DAG with additional causal relationships and calibrates Y0 values. This is the SOURCE OF TRUTH for artifacts A.1-A.6.

---

## Inputs

Read the REFINE output files from `{analysis_dir}/02_REFINE/`:
- `{TICKER}_A1_EPISTEMIC_ANCHORS_BASE.json`
- `{TICKER}_A2_ANALYTIC_KG_BASE.json`
- `{TICKER}_A3_CAUSAL_DAG_BASE.json`
- `{TICKER}_A5_GIM_BASE.json`
- `{TICKER}_A6_DR_BASE.json`
- `{TICKER}_N1_THESIS_BASE.md`
- `{TICKER}_N2_IC_BASE.md`
- `{TICKER}_N3_ECON_GOV_BASE.md`
- `{TICKER}_N4_RISK_BASE.md`

Also compare with T1 versions from `{analysis_dir}/01_T1/` for change tracking.

---

## Validation Checks

### 1. All Required Files Present

**Check:** All 9 REFINE files exist in the output directory.

**Pass Criteria:**
- All 6 JSON artifacts exist and are non-empty
- All 4 narrative markdown files exist and are non-empty
- File naming follows convention: `{TICKER}_{ARTIFACT}_BASE.{ext}`

**Fail:** Missing files block T2 execution.

### 2. JSON Well-Formedness

**Check:** All JSON files parse correctly.

**Pass Criteria:**
- Each JSON file is syntactically valid
- No trailing commas, unclosed braces, or malformed strings

**Fail:** Malformed JSON requires repair (spawn Opus subagent for repair).

### 3. DAG Node Count (CRITICAL)

**Check:** A.3 Causal DAG has ≤20 exogenous nodes.

**Pass Criteria:**
- Count nodes where `node_type == "exogenous"` OR nodes in the `exogenous_nodes` array
- Total exogenous node count ≤ 20
- Note: Total nodes (exogenous + endogenous) is NOT the constraint

**Fail:** More than 20 exogenous nodes causes kernel execution errors.

**How to Count:**
```python
# Method 1: If DAG has node_type field
exog_count = sum(1 for n in dag['nodes'] if n.get('node_type') == 'exogenous')

# Method 2: If DAG has exogenous_nodes list
exog_count = len(dag.get('exogenous_nodes', []))

# Must be ≤ 20
```

### 4. DAG Expansion from T1

**Check:** REFINE added causal relationships beyond T1.

**Pass Criteria:**
- Total edges (relationships) in REFINE ≥ T1 edge count
- New edges have documented rationale
- No edges removed without justification

**Warn:** If REFINE DAG identical to T1, expansion may have been skipped.

### 5. Y0 Calibration Complete

**Check:** Y0 values are calibrated against reported financials.

**Pass Criteria:**
- Revenue_Y0 within 2% of reported
- EBIT_Y0 within 5% of reported (or documented explanation for deviation)
- IC_Y0 calibrated with documented approach

**Fail:** Uncalibrated Y0 will produce incorrect IVPS.

### 6. Equity Bridge Preserved from T1

**Check:** FDSO, Total_Debt, Excess_Cash, Minority_Interest preserved.

**Pass Criteria:**
- Values match T1 exactly (these don't change in REFINE)
- Or if changed, explicit documentation of why

**Fail:** Equity Bridge changes without justification corrupt IVPS.

### 7. GIM-DAG Alignment

**Check:** Every GIM driver has a corresponding DAG node.

**Pass Criteria:**
- All GIM driver names appear in DAG node list
- No orphan drivers (GIM without DAG)
- No orphan DAG nodes referenced by GIM

**Fail:** Misalignment causes kernel errors.

### 8. DR Sanity Bounds (v2.2.3e)

**Check:** A.6 DR derivation produces reasonable discount rate.

**Pass Criteria:**
- DR_Static is between 5% and 25%
- X (Risk Multiplier) is between 0.5 and 2.0 (NOT 2.2 - reduced cap)
- RFR is between 0% and 10%
- RFR matches reporting currency (e.g., USD uses US Treasury rate)

**Warn:** Values outside these ranges may indicate calibration issues.

### 9. No A.7 Yet

**Check:** A.7 (Valuation Summary) does NOT exist in REFINE folder.

**Pass Criteria:**
- No A.7 file exists (kernel hasn't run)
- No IVPS values in REFINE output

**Fail:** REFINE should NOT compute IVPS. That's T2's job.

### 10. Unit Field Present (v2.2.3e)

**Check:** A.5 GIM specifies the financial unit.

**Pass Criteria:**
- `unit` field present in A.5 (e.g., "thousands", "millions", "units")
- Unit matches source document conventions

**Warn:** Missing unit defaults to "units" (no scaling).

---

## Output Format

### PASS

```
BASE REFINE VALIDATOR: PASS

Summary:
- Files Present: 9/9
- Exogenous Nodes: {count}/20 (within limit)
- DAG Edges: {T1_count} → {REFINE_count} (expanded)
- Y0 Calibration: Revenue {pct}%, EBIT {pct}%
- Equity Bridge: Preserved
- DR Estimate: {DR_Static}%
- Unit: {unit}

REFINE validated. Proceed to T2.
```

### FAIL

```
BASE REFINE VALIDATOR: FAIL

Critical Issues:
1. [Check N]: {Issue description}
   Location: {Which file/field}
   Impact: {Why this blocks T2}

Required Fixes:
- {Specific action to remediate}

Re-run REFINE before proceeding to T2.
```

### WARN (Proceed with Caveats)

```
BASE REFINE VALIDATOR: PASS WITH WARNINGS

Warnings:
1. [Check N]: {Issue description}

Proceed to T2, but address warnings in future runs.
```

---

## Validator Execution

1. List files in REFINE output directory
2. Read and parse each JSON artifact
3. Compare with T1 versions where relevant
4. Execute all checks above
5. Emit validation result

**Return:** Validation result only. Do NOT return the full REFINE content.

---

*END OF BASE REFINE VALIDATOR*
