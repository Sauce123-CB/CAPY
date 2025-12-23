# Forward Propagation Checklist

> **Purpose:** Apply remaining mega-patch changes to SCENARIO, SC, INT, IRR
> **Created:** 2024-12-23
> **Status:** ✅ COMPLETED 2024-12-23

---

## Pre-Flight: Already Done

These items have been propagated to ALL stages - no action needed:

- [x] Kernel Execution Contract (all SCHEMAS files)
- [x] DR Philosophy + Currency-Matched RFR (all NORMDEFS files)
- [x] X Range [0.5, 2.0] (all NORMDEFS files)
- [x] DAG Equation Format GET/PREV syntax (BASE, REFINE, ENRICH, SCENARIO, INT prompts)
- [x] ROIC_anchor in A.2.Y0_data (BASE prompt line 538, ENRICH prompt line 282)

---

## 1. SCENARIO Stage ✅

### 1.1 Prompt: G3_SCENARIO_2.2.2e_PROMPT.md → 2.2.3e

- [x] **Version bump:** Updated header to 2.2.3e
- [x] **Section V rewrite:** Replaced unified output with atomized emission
  - Removed "unified emission" language
  - Added atomized file table with exact filenames
  - Specified: `{TICKER}_{ARTIFACT}_SCEN.{ext}`
- [x] **T2 instructions:** Added Kernel Receipt generation (Pattern 13)

### 1.2 Kernel: CVR_KERNEL_SCEN_2_2_2e.py → 2.2.3e

- [x] **Version string:** Updated to G3_2.2.3e_SCEN
- [x] **Added constants:** GDP_PROXY, GDP_MULTIPLIER, DEFAULT_ROIC_ANCHOR
- [x] **Replaced terminal g calculation:** From nopat_growth_rates to revenue_g + ebit_g
- [x] **Added ROIC_anchor lookup:** From core_data.Y0_data
- [x] **Syntax verified:** `python3 -c "import CVR_KERNEL_SCEN_2_2_2e"` passes

---

## 2. SC Stage ✅

### 2.1 Prompt: G3_SC_2.2.2e_*.md (6 files)

- [x] **Verified:** Already atomized (6 separate audit prompts)
- [x] **No changes needed**

---

## 3. INTEGRATION Stage ✅

### 3.1 Prompt: G3_INTEGRATION_2.2.3e_PROMPT.md

- [x] **T1 atomized output:** Already in place (Section A.y)
- [x] **T3 atomized output:** Already in place (Section V)
- [x] **T2 instructions:** Added Kernel Receipt generation (Pattern 13)
- [x] **Updated file naming:** Changed _S4 suffix to _INT for consistency

### 3.2 Kernel: CVR_KERNEL_INT_2_2_2e.py → 2.2.3e

- [x] **Version string:** Updated to G3_2.2.3e_INT
- [x] **Added constants:** GDP_PROXY, GDP_MULTIPLIER, DEFAULT_ROIC_ANCHOR
- [x] **Replaced terminal g calculation:** Same pattern as SCENARIO
- [x] **Added ROIC_anchor lookup:** From core_data.Y0_data
- [x] **Syntax verified:** `python3 -c "import CVR_KERNEL_INT_2_2_2e"` passes

---

## 4. IRR Stage ✅

### 4.1 Prompt: G3_IRR_2.2.5e_PROMPT.md → 2.2.6e

- [x] **Version bump:** Updated header to 2.2.6e
- [x] **Section V rewrite:** Replaced with atomized emission tables
  - Specified: `{TICKER}_{ARTIFACT}_IRR.{ext}`
- [x] **T2 instructions:** Added Kernel Receipt generation (Pattern 13)

### 4.2 Kernel: CVR_KERNEL_IRR_2.2.5e.py → 2.2.6e

- [x] **Version string:** Updated to G3_2.2.6e_IRR
- [x] **Added constants:** GDP_PROXY, GDP_MULTIPLIER, DEFAULT_ROIC_ANCHOR
- [x] **Replaced terminal g calculation:** Same pattern as SCENARIO
- [x] **Added ROIC_anchor lookup:** From core_data.Y0_data
- [x] **Syntax verified:** `python3 -m py_compile CVR_KERNEL_IRR_2.2.5e.py` passes

---

## 5. Schema Field Additions (Already Done in Prior Session)

### 5.1 A.1 EPISTEMIC_ANCHORS Schema

- [x] **File:** G3BASE_2.2.3e_SCHEMAS.md
- [x] **Added field:** ROIC_anchor

### 5.2 A.2 ANALYTIC_KG Schema

- [x] **File:** G3BASE_2.2.3e_SCHEMAS.md
- [x] **Added to market_context:** reporting_currency, price_currency, fx_rate_to_reporting

### 5.3 A.9 ENRICHMENT_TRACE Schema

- [ ] **File:** G3ENRICH_2.2.3e_SCHEMAS.md
- [ ] **Add field:** anchor_changelog (DEFERRED - low priority)

---

## 6. Scripts (Deferred)

### 6.1 generate_final_cvr.sh

- [ ] **Create:** workshop/scripts/generate_final_cvr.sh
- [ ] **Content:** See mega-patch Section 5
- [ ] **Note:** Not blocking for smoke test

### 6.2 .claude/settings.json

- [ ] **Create:** CAPY/.claude/settings.json
- [ ] **Note:** Not blocking - permissions already configured in session

---

## Summary

**Completed:** All kernel patches, all prompt patches for SCENARIO/INT/IRR
**Remaining:** generate_final_cvr.sh script, anchor_changelog schema (both low priority)

**Ready for smoke test:** YES
