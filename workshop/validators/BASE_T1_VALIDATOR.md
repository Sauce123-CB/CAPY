# BASE T1 Validator

> **Version:** 2.2.3e
> **Model:** Opus (REQUIRED - do NOT use Haiku)
> **Pattern:** 7 (Validators after each turn)

## Purpose

Validate BASE T1 output before proceeding to REFINE.

T1 produces initial analytical synthesis:
- Epistemic anchors (A.1)
- Analytic Knowledge Graph (A.2)
- Causal DAG (A.3)
- Gestalt Impact Map (A.5)
- DR Derivation (A.6)
- Narratives (N1-N4)

---

## Inputs

Read the T1 output files from `{analysis_dir}/01_T1/`:
- `{TICKER}_A1_EPISTEMIC_ANCHORS_BASE.json`
- `{TICKER}_A2_ANALYTIC_KG_BASE.json`
- `{TICKER}_A3_CAUSAL_DAG_BASE.json`
- `{TICKER}_A5_GIM_BASE.json`
- `{TICKER}_A6_DR_BASE.json`
- `{TICKER}_N1_THESIS_BASE.md`
- `{TICKER}_N2_IC_BASE.md`
- `{TICKER}_N3_ECON_GOV_BASE.md`
- `{TICKER}_N4_RISK_BASE.md`

---

## Validation Checks

### 1. All Required Files Present

**Check:** All 9 T1 files exist in the output directory.

**Pass Criteria:**
- All 6 JSON artifacts exist and are non-empty
- All 4 narrative markdown files exist and are non-empty
- File naming follows convention: `{TICKER}_{ARTIFACT}_BASE.{ext}`

**Fail:** Missing files block REFINE execution.

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

### 4. GIM Driver Coverage

**Check:** All GIM drivers appear in the DAG.

**Pass Criteria:**
- Every driver in A.5 GIM has a corresponding node in A.3 DAG
- No orphan drivers (present in GIM but missing from DAG)

**Warn:** Missing DAG coverage may indicate incomplete causal modeling.

### 5. Equity Bridge Items Present

**Check:** A.2 contains Equity Bridge items for IVPS calculation.

**Required Items:**
- `FDSO` (Fully Diluted Shares Outstanding)
- `Total_Debt`
- `Excess_Cash`
- `Minority_Interest` (if applicable)

**Pass Criteria:**
- FDSO is present and > 0
- Total_Debt is present (may be 0)
- Excess_Cash is present (may be 0)

**Fail:** Missing FDSO blocks IVPS calculation.

### 6. DR Sanity Bounds

**Check:** A.6 DR derivation produces reasonable discount rate.

**Pass Criteria:**
- DR_Static is between 5% and 25%
- X (Risk Multiplier) is between 0.5 and 2.0
- RFR is between 0% and 10%
- ERP is between 3% and 8%

**Warn:** Values outside these ranges may indicate calibration issues.

### 7. No Kernel Values in T1

**Check:** T1 did NOT execute the kernel (T1 is synthesis only).

**Pass Criteria:**
- A.7 (Valuation Summary) does NOT exist yet
- No IVPS values appear in T1 output
- No `KERNEL_RECEIPT` file exists

**Fail:** T1 should NOT compute IVPS. That's T2's job.

### 8. ROIC Anchor Present (v2.2.3e)

**Check:** A.1 contains ROIC anchor for terminal value calculation.

**Pass Criteria:**
- `ROIC_p50` or `ROIC_anchor` field present in A.1
- Value is between 5% and 40%

**Warn:** Missing ROIC anchor will use kernel default (15%).

### 9. Currency Documented (v2.2.3e)

**Check:** A.2 documents the reporting currency.

**Pass Criteria:**
- `reporting_currency` field present (e.g., "USD", "EUR", "GBP")
- Consistent with source document currency

**Warn:** Missing currency may cause cross-listed security errors.

---

## Output Format

### PASS

```
BASE T1 VALIDATOR: PASS

Summary:
- Files Present: 9/9
- Exogenous Nodes: {count}/20 (within limit)
- GIM Drivers: {count}
- DR Estimate: {DR_Static}%
- ROIC Anchor: {value}%
- Currency: {reporting_currency}

T1 validated. Proceed to REFINE.
```

### FAIL

```
BASE T1 VALIDATOR: FAIL

Critical Issues:
1. [Check N]: {Issue description}
   Location: {Which file/field}
   Impact: {Why this blocks REFINE}

Required Fixes:
- {Specific action to remediate}

Re-run T1 before proceeding to REFINE.
```

### WARN (Proceed with Caveats)

```
BASE T1 VALIDATOR: PASS WITH WARNINGS

Warnings:
1. [Check N]: {Issue description}

Proceed to REFINE, but address warnings if they recur.
```

---

## Validator Execution

1. List files in T1 output directory
2. Read and parse each JSON artifact
3. Execute all checks above
4. Emit validation result

**Return:** Validation result only. Do NOT return the full T1 content.

---

*END OF BASE T1 VALIDATOR*
