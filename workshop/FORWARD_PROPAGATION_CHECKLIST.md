# Forward Propagation Checklist

> **Purpose:** Apply remaining mega-patch changes to SCENARIO, SC, INT, IRR
> **Created:** 2024-12-23
> **Status:** Working document

---

## Pre-Flight: Already Done

These items have been propagated to ALL stages - no action needed:

- [x] Kernel Execution Contract (all SCHEMAS files)
- [x] DR Philosophy + Currency-Matched RFR (all NORMDEFS files)
- [x] X Range [0.5, 2.0] (all NORMDEFS files)
- [x] DAG Equation Format GET/PREV syntax (BASE, REFINE, ENRICH, SCENARIO, INT prompts)
- [x] ROIC_anchor in A.2.Y0_data (BASE prompt line 538, ENRICH prompt line 282)

---

## 1. SCENARIO Stage

### 1.1 Prompt: G3_SCENARIO_2.2.2e_PROMPT.md → 2.2.3e

- [ ] **Version bump:** Update header to 2.2.3e
- [ ] **Section V rewrite:** Replace unified output with atomized emission
  - Remove "unified emission" language
  - Add atomized file table with exact filenames
  - Specify: `{TICKER}_{ARTIFACT}_SCEN.{ext}`
- [ ] **T2 instructions:** Add Kernel Receipt generation
  ```
  After kernel execution, write receipt:
  {TICKER}_KERNEL_RECEIPT_SCEN.json
  ```

### 1.2 Kernel: CVR_KERNEL_SCEN_2_2_2e.py → 2.2.3e

- [ ] **Version string:** Update to 2.2.3e
- [ ] **Add constants (top of file):**
  ```python
  GDP_PROXY = 0.025
  GDP_MULTIPLIER = 1.4
  DEFAULT_ROIC_ANCHOR = 0.15
  ```
- [ ] **Replace terminal g calculation (~line 413-420):**
  ```python
  # OLD (remove):
  nopat_growth_rates = forecast_df['NOPAT'].pct_change().values[1:]
  terminal_g_estimate = np.mean(nopat_growth_rates[-3:])

  # NEW (add):
  revenue_growth_rates = forecast_df['Revenue'].pct_change().values[1:]
  ebit_growth_rates = forecast_df['EBIT'].pct_change().values[1:]
  revenue_g = np.mean(revenue_growth_rates[-3:]) if len(revenue_growth_rates) >= 3 else np.mean(revenue_growth_rates)
  ebit_g = np.mean(ebit_growth_rates[-3:]) if len(ebit_growth_rates) >= 3 else np.mean(ebit_growth_rates)
  terminal_g_estimate = (revenue_g + ebit_g) / 2
  terminal_g_cap = GDP_PROXY * GDP_MULTIPLIER
  terminal_g = min(terminal_g_estimate, terminal_g_cap)
  terminal_g = max(terminal_g, 0)
  ```
- [ ] **Add ROIC_anchor lookup:**
  ```python
  roic_anchor = core_data.get('ROIC_anchor', DEFAULT_ROIC_ANCHOR)
  ```

---

## 2. SC Stage

### 2.1 Prompt: G3_SC_2.2.2e_*.md (6 files)

- [ ] **Verify:** Already atomized (6 separate audit prompts)
- [ ] **No changes needed** unless version bump required

---

## 3. INTEGRATION Stage

### 3.1 Prompt: G3_INTEGRATION_2.2.3e_PROMPT.md

- [ ] **Verify T1 atomized output:** Check Section A.y T1 Output Specification
- [ ] **Verify T3 atomized output:** Check Section V OUTPUT MANDATE
- [ ] **T2 instructions:** Add Kernel Receipt generation
  ```
  After kernel execution, write receipt:
  {TICKER}_KERNEL_RECEIPT_INT.json
  ```

### 3.2 Kernel: CVR_KERNEL_INT_2_2_2e.py → 2.2.3e

- [ ] **Version string:** Update to 2.2.3e
- [ ] **Add constants (top of file):**
  ```python
  GDP_PROXY = 0.025
  GDP_MULTIPLIER = 1.4
  DEFAULT_ROIC_ANCHOR = 0.15
  ```
- [ ] **Replace terminal g calculation (~line 413-420):**
  Same pattern as SCENARIO kernel
- [ ] **Add ROIC_anchor lookup:**
  ```python
  roic_anchor = core_data.get('ROIC_anchor', DEFAULT_ROIC_ANCHOR)
  ```

---

## 4. IRR Stage

### 4.1 Prompt: G3_IRR_2.2.5e_PROMPT.md → 2.2.6e

- [ ] **Version bump:** Update header to 2.2.6e
- [ ] **Section V rewrite:** Replace unified output with atomized emission
  - Specify: `{TICKER}_{ARTIFACT}_IRR.{ext}`
- [ ] **T2 instructions:** Add Kernel Receipt generation
  ```
  After kernel execution, write receipt:
  {TICKER}_KERNEL_RECEIPT_IRR.json
  ```

### 4.2 Kernel: CVR_KERNEL_IRR_2.2.5e.py → 2.2.6e

- [ ] **Version string:** Update to 2.2.6e
- [ ] **Add constants (top of file):**
  ```python
  GDP_PROXY = 0.025
  GDP_MULTIPLIER = 1.4
  DEFAULT_ROIC_ANCHOR = 0.15
  ```
- [ ] **Replace terminal g calculation (~line 588-595):**
  Same pattern as SCENARIO kernel
- [ ] **Add ROIC_anchor lookup:**
  ```python
  roic_anchor = core_data.get('ROIC_anchor', DEFAULT_ROIC_ANCHOR)
  ```

---

## 5. Schema Field Additions (One-Time)

### 5.1 A.1 EPISTEMIC_ANCHORS Schema

- [ ] **File:** G3BASE_2.2.3e_SCHEMAS.md
- [ ] **Add field:**
  ```json
  "ROIC_anchor": "number (industry median ROIC for terminal reinvestment calculation)"
  ```

### 5.2 A.2 ANALYTIC_KG Schema

- [ ] **File:** G3BASE_2.2.3e_SCHEMAS.md
- [ ] **Add to market_context:**
  ```json
  "reporting_currency": "string (USD, EUR, GBP, etc.)",
  "price_currency": "string (currency of market price)",
  "fx_rate_to_reporting": "number (if currencies differ)"
  ```

### 5.3 A.9 ENRICHMENT_TRACE Schema

- [ ] **File:** G3ENRICH_2.2.3e_SCHEMAS.md
- [ ] **Add field:**
  ```json
  "anchor_changelog": "array (changes to A.1 epistemic anchors)"
  ```

---

## 6. Scripts (One-Time)

### 6.1 generate_final_cvr.sh

- [ ] **Create:** workshop/scripts/generate_final_cvr.sh
- [ ] **Content:** See mega-patch Section 5

### 6.2 .claude/settings.json

- [ ] **Create:** CAPY/.claude/settings.json
- [ ] **Content:**
  ```json
  {
    "permissions": {
      "allow": [
        "Bash(*)", "Read(**)", "Edit(**)", "Write(**)",
        "WebFetch", "WebSearch", "Glob", "Grep"
      ],
      "defaultMode": "acceptEdits"
    }
  }
  ```

---

## Execution Order

1. **Schema additions first** (5.1-5.3) - affects all downstream
2. **SCENARIO** (1.1-1.2) - first stage after ENRICH
3. **SC** (2.1) - verify only
4. **INT** (3.1-3.2) - depends on SCENARIO output
5. **IRR** (4.1-4.2) - depends on INT output
6. **Scripts** (6.1-6.2) - can be done anytime

---

## Validation

After each stage propagation:
1. Run `RUN {STAGE}->{STAGE} {TICKER}` from smoke_tests/
2. Verify kernel executes (not simulated)
3. Verify atomized files created with correct naming
4. Verify kernel receipt generated

---

## Reference: Atomized Output Template

For Section V rewrites, use this pattern:

```markdown
## V. OUTPUT MANDATE (Atomized Artifact Emission)

**Core Principle:** Every artifact MUST be written as an individual file.

### T1 Output Files

| File | Content |
|------|---------|
| `{TICKER}_A10_SCENARIO_SCEN.json` | Scenario model output |
| `{TICKER}_N6_SCENARIO_SCEN.md` | Scenario synthesis narrative |

### T2 Output Files

| File | Content |
|------|---------|
| `{TICKER}_A7_VALUATION_SCEN.json` | Updated valuation (if recalculated) |
| `{TICKER}_KERNEL_RECEIPT_SCEN.json` | Kernel execution proof |

### Anti-Patterns (DO NOT)

- Do NOT embed JSON in markdown
- Do NOT produce "unified emission" documents
- Do NOT return file contents to orchestrator (write to disk, return filepath only)
```
