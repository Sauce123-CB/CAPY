# G3BASE 2.2.3e: Artifact Schemas (Appendix A)

> **Version:** 2.2.3e
> **Parent Document:** G3BASE_2.2.3e_PROMPT.md
> **Patch:** Added currency fields, ROIC_anchor, updated DR methodology

This file defines the JSON schemas for all BASE stage artifacts.

---

## CVR_SCHEMAS_G3_2.2.3e.json

```json
{
  "version_control": {
    "paradigm": "G3 Meta-Prompting Doctrine v2.4 (Two-Shot Guided Autonomy)",
    "pipeline_stage": "BASE G3_2.2.3e",
    "date": "2024-12-22"
  },

  "normative_definitions": {
    "1.1_financial_definitions_and_formulas": {
      "EBIT": "MUST include Stock-Based Compensation (SBC) expense.",
      "NOPAT": "EBIT * (1 - Tax Rate).",
      "ROIC": "NOPAT / Invested Capital.",
      "FCF_Unlevered": "NOPAT - Reinvestment.",
      "Growth_g": "ROIC * Reinvestment Rate.",
      "Timing_Convention_Mandate_DAG_Compliance": "Calculations dependent on prior period balances MUST use the Beginning-of-Period (BOP) value (i.e., the PREV() function). Mandatory for ROIC (PREV(Invested_Capital)).",
      "ATP_Mandate": "All financial inputs to the DAG must be reconciled to their economic definition per P1.5. The accounting_translation_log in A.2 documents this reconciliation. Raw reported figures that deviate from normative definitions (e.g., Adj. EBITDA excluding SBC) must be adjusted before becoming DAG inputs.",
      "Valuation_Methodology_APV": "Adjusted Present Value (APV) approach is mandated. 20-Year Explicit Forecast. Static DR is used."
    },

    "1.2_assumption_dsl_definitions": {
      "description": "The DSL defines how an assumption evolves from Year 1 (Y1) to Year 20 (Y20). See G3BASE_2.2.3e_NORMDEFS.md for full definitions of STATIC, LINEAR_FADE, CAGR_INTERP, EXPLICIT_SCHEDULE."
    },

    "1.3_dr_derivation_methodology": {
      "DR_Static": "RFR + (ERP * X). X (Risk Multiplier) calibrated against global universe of 50,000+ securities (NOT S&P 500). X ∈ [0.5, 2.0]. See NORMDEFS for calibration anchors."
    }
  },

  "schemas": {
    "A.1_EPISTEMIC_ANCHORS": {
      "schema_version": "G3_2.2.3e",
      "description": "Documents the Bayesian Priors established in Phases A and B.",
      "near_term_anchors": "object (Guidance and Consensus)",
      "long_term_anchors": "object (Mandatory Numeric Base Rate Distributions: Must include {p10: float, p50: float, p90: float} for every exogenous driver)",
      "ROIC_anchor": "float (Industry median ROIC from base rates, used for terminal reinvestment calculation. Kernel default: 0.15)"
    },

    "A.2_ANALYTIC_KG": {
      "schema_version": "G3_2.2.3e",
      "metadata": {
        "atp_complexity_assessment": "string (LOW / MODERATE / HIGH)",
        "atp_mode": "string (ATP-Lite / Full ATP)"
      },
      "core_data": {
        "__COMMENT__": "CRITICAL: Must use the nested 'Y0_data' key for the Kernel to read history.",
        "Y0_data": "object (Key-Value pairs of Y0 financials, e.g., {'Revenue': 100.0, 'EBIT': 20.0}). Include ROIC_anchor from A.1 for terminal reinvestment.",
        "TSM_data": "object (Trailing Twelve Month data)"
      },
      "accounting_translation_log": {
        "__COMMENT__": "Documents the reconciliation of reported figures to economic definitions per ATP (P1.5).",
        "schema": {
          "metric_name": {
            "source_metric": "string (The metric as reported/labeled in source documents)",
            "source_reference": "string (Document and page/note reference)",
            "adjustments_applied": ["array of strings describing each adjustment made"],
            "normative_alignment": "string (Confirms alignment with Section 1.1 definitions or documents deviation)",
            "confidence": "string (High / Medium / Low)",
            "flags": ["array of strings for any issues requiring downstream attention"]
          }
        },
        "required_entries": ["EBIT", "CapEx", "D&A", "SBC_Treatment", "Share_Count_Basis"],
        "optional_entries": ["Working_Capital", "Revenue_Recognition", "One_Time_Items", "Consolidation"]
      },
      "market_context": {
        "Current_Stock_Price": "float (REQUIRED for Implied Multiples)",
        "RFR": "float",
        "ERP": "float",
        "reporting_currency": "string (REQUIRED: Currency of published financials, e.g., 'USD', 'EUR', 'GBP')",
        "price_currency": "string (Currency of market price, defaults to reporting_currency if same)",
        "fx_rate_to_reporting": "float (FX rate if price_currency != reporting_currency, else 1.0)",
        "Other_Context": "object"
      },
      "share_data": "object (FDSO, Share Count details)"
    },

    "A.3_CAUSAL_DAG": {
      "schema_version": "G3_2.2.2e",
      "description": "The unified DAG defining structure, dependencies, and equations. (Consolidated A.3 structure and A.4 equations)",
      "DAG": {
        "__COMMENT__": "Dictionary where keys are Node Names.",
        "Node_Definition": {
          "type": "Exogenous_Driver / Endogenous_Driver / Financial_Line_Item",
          "parents": ["list of strings (Explicit dependencies, primarily for documentation)"],
          "equation": "string (Python-executable equation. MUST use PREV('Var') for lagged access and GET('Var') for intra-timestep access.)"
        }
      },
      "coverage_manifest": {
        "__COMMENT__": "Documents which financial line items are covered by the DAG.",
        "covered_items": ["list of strings"],
        "not_covered_items": ["list of strings with rationale"]
      }
    },

    "A.5_GESTALT_IMPACT_MAP": {
      "schema_version": "G3_2.2.2e",
      "description": "The map of exogenous driver assumptions and their justifications.",
      "GIM": {
        "__COMMENT__": "Dictionary where keys are Driver Handles (must align with A.3).",
        "Driver_Definition": {
          "mode": "string (DSL Mode: STATIC, LINEAR_FADE, CAGR_INTERP, EXPLICIT_SCHEDULE)",
          "params": "object (DSL Parameters - see G3BASE_2.2.2e_NORMDEFS.md)",
          "qualitative_thesis": "string (Causal Chain Justification. MUST include 'Variance Justification' with percentile rankings if deviating from A.1.)"
        }
      }
    },

    "A.6_DR_DERIVATION_TRACE": {
      "schema_version": "G3_2.2.2e",
      "derivation_trace": {
        "RFR": "float",
        "ERP": "float",
        "X_Risk_Multiplier": "float",
        "DR_Static": "float"
      },
      "justification": "string (See Mandatory Narrative #4. Justify the Risk Multiplier X based on qualitative assessment.)"
    },

    "A.7_LIGHTWEIGHT_VALUATION_SUMMARY": {
      "__GENERATION_NOTE__": "DOWNSTREAM-GENERATED. This artifact is produced by kernel execution, not by Turn 1. Schema included for reference.",
      "schema_version": "G3_2.2.2e",
      "description": "The Selective Emission output from kernel execution.",
      "ivps_summary": {
        "IVPS": "float",
        "DR": "float",
        "Terminal_g": "float",
        "ROIC_Terminal": "float",
        "Current_Market_Price": "float or null"
      },
      "implied_multiples_analysis": {
        "Implied_EV_Sales_Y1": "float",
        "Implied_EV_EBIT_Y1": "float",
        "Implied_P_NOPAT_Y1": "float",
        "Market_EV_Sales_Y1": "float",
        "Market_EV_EBIT_Y1": "float",
        "Market_P_NOPAT_Y1": "float"
      },
      "sensitivity_analysis": {
        "tornado_summary": [{
          "Driver_Handle": "string",
          "IVPS_Low": "float",
          "IVPS_High": "float",
          "IVPS_Swing_Percent": "float"
        }]
      },
      "key_forecast_metrics": {
        "Revenue_CAGR_Y1_Y5": "float",
        "EBIT_Margin_Y5": "float",
        "ROIC_Y5": "float"
      },
      "terminal_drivers": "object",
      "forecast_trajectory_checkpoints": {
        "__COMMENT__": "Nominal values of key drivers (Exogenous and Endogenous) at specific checkpoints for auditability.",
        "Y0": "object",
        "Y5": "object",
        "Y10": "object",
        "Y20": "object"
      }
    }
  }
}
```

---

## Schema Quick Reference

| Artifact | Purpose | Key Fields |
|----------|---------|------------|
| **A.1** | Epistemic Anchors | near_term_anchors, long_term_anchors (with p10/p50/p90) |
| **A.2** | Analytic Knowledge Graph | Y0_data, accounting_translation_log, market_context, share_data |
| **A.3** | Causal DAG | DAG (nodes with type/parents/equation), coverage_manifest |
| **A.5** | Gestalt Impact Map | GIM (drivers with mode/params/qualitative_thesis) |
| **A.6** | DR Derivation Trace | RFR, ERP, X_Risk_Multiplier, DR_Static, justification |
| **A.7** | Valuation Summary | IVPS, implied_multiples, sensitivity_analysis (kernel-generated) |

---

## Critical Schema Requirements

### DAG Node Format (A.3)

Each node in the DAG **must** follow this structure:

```json
"Revenue": {
  "type": "Financial_Line_Item",
  "parents": ["MTMs", "ARPU"],
  "equation": "GET('MTMs') * GET('ARPU')"
}
```

- **type**: One of `Exogenous_Driver`, `Endogenous_Driver`, `Financial_Line_Item`
- **parents**: List of dependency node names
- **equation**: Python-executable string using `GET('Var')` and `PREV('Var')`

### GIM Entry Format (A.5)

Each driver in the GIM **must** follow this structure:

```json
"Revenue_Growth": {
  "mode": "CAGR_INTERP",
  "params": {
    "start_cagr": 0.25,
    "end_cagr": 0.05,
    "interp_years": 10
  },
  "qualitative_thesis": "Management guides 25% near-term growth..."
}
```

- **mode**: One of `STATIC`, `LINEAR_FADE`, `CAGR_INTERP`, `EXPLICIT_SCHEDULE`
- **params**: Mode-specific parameters (see G3BASE_2.2.3e_NORMDEFS.md)
- **qualitative_thesis**: Bayesian justification tracing Prior → Posterior

---

## Kernel Execution Contract (MANDATORY)

**The CVR kernel uses `eval()` on DAG equations.** This section documents the exact schema requirements for kernel compatibility. Violations cause kernel bypass or runtime errors.

### 1. DAG Equation Syntax

**Exogenous drivers MUST have empty equations:**
```json
"Revenue_Growth": {
  "type": "Exogenous_Driver",
  "parents": [],
  "equation": ""
}
```
- Exogenous drivers get their values from the GIM, not from equations
- Non-empty equations on exogenous drivers cause `eval()` errors
- Pseudo-code like `"f(x, y, z)"` will FAIL

**Derived nodes MUST use executable Python with GET()/PREV():**
```json
"Revenue": {
  "type": "Financial_Line_Item",
  "parents": ["Revenue_Prior", "Revenue_Growth"],
  "equation": "PREV('Revenue') * (1 + GET('Revenue_Growth'))"
}
```
- `GET('Var')` retrieves current-period value
- `PREV('Var')` retrieves prior-period value
- Equation must be valid Python that can be passed to `eval()`

### 2. GIM-DAG Name Matching (CRITICAL)

**GIM driver names MUST exactly match DAG node names:**
```json
// DAG
"Revenue_SaaS_Growth": {
  "type": "Exogenous_Driver",
  "parents": [],
  "equation": ""
}

// GIM - MUST use identical key
"Revenue_SaaS_Growth": {
  "mode": "LINEAR_FADE",
  "params": {...}
}
```
- Kernel loads GIM values using DAG node names as keys
- Mismatched names (e.g., `"SaaS_Growth"` vs `"Revenue_SaaS_Growth"`) cause silent failures
- Kernel code: `if handle in dag:` - names must match exactly

### 3. EXPLICIT_SCHEDULE Key Format

**Schedule keys MUST be numeric strings, not year labels:**
```json
// CORRECT
"params": {
  "schedule": {
    "1": 837,
    "2": 0,
    "3": 0
  }
}

// WRONG - will cause ValueError
"params": {
  "schedule": {
    "Y1": 837,
    "Y2": 0,
    "Y3": 0
  }
}
```
- Kernel parses keys with `int(key)`
- `"Y1"` causes `ValueError: invalid literal for int() with base 10: 'Y1'`

### 4. Coverage Manifest Requirements

**coverage_manifest MUST list ALL nodes present in Y0_data:**
```json
"coverage_manifest": {
  "Revenue": "Total revenue",
  "Revenue_SaaS": "SaaS segment revenue",
  "EBIT": "Earnings before interest and taxes",
  // ... every node in Y0_data needs an entry
}
```
- Kernel validates that all Y0_data keys have manifest entries
- Missing entries cause `RuntimeError: DAG Coverage Warning`
- Include even "obvious" items like `Revenue`, `EBIT`, `NOPAT`

### 5. A.6 DR Trace Key Path

**DR trace MUST use `derivation_trace` as top-level key:**
```json
{
  "schema_version": "G3_2.2.3e",
  "derivation_trace": {
    "DR_Static": 0.20,
    "RFR": 0.045,
    "ERP": 0.05,
    "X": 1.8
  }
}
```
- Kernel accesses: `dr_trace['derivation_trace']['DR_Static']`
- Using `"dr_derivation"` or other keys causes `KeyError`

### Kernel Contract Checklist

Before kernel execution, verify:

- [ ] All `Exogenous_Driver` nodes have `"equation": ""`
- [ ] All derived nodes have executable Python equations with `GET()`/`PREV()`
- [ ] GIM keys exactly match DAG node names
- [ ] EXPLICIT_SCHEDULE uses numeric keys (`"1"`, `"2"`, not `"Y1"`, `"Y2"`)
- [ ] coverage_manifest includes ALL Y0_data node names
- [ ] A.6 uses `derivation_trace.DR_Static` key path
