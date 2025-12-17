# G3BASE 2.2.2e: Artifact Schemas (Appendix A)

> **Version:** 2.2.2e
> **Parent Document:** G3BASE_2.2.2e_PROMPT.md

This file defines the JSON schemas for all BASE stage artifacts.

---

## CVR_SCHEMAS_G3_2.2.2e.json

```json
{
  "version_control": {
    "paradigm": "G3 Meta-Prompting Doctrine v2.4 (Two-Shot Guided Autonomy)",
    "pipeline_stage": "BASE G3_2.2.2e",
    "date": "2024-12-17"
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
      "description": "The DSL defines how an assumption evolves from Year 1 (Y1) to Year 20 (Y20). See G3BASE_2.2.2e_NORMDEFS.md for full definitions of STATIC, LINEAR_FADE, CAGR_INTERP, EXPLICIT_SCHEDULE."
    },

    "1.3_dr_derivation_methodology": {
      "DR_Static": "RFR + (ERP * X). X (Risk Multiplier) is a qualitative assessment (0.5 to 2.2)."
    }
  },

  "schemas": {
    "A.1_EPISTEMIC_ANCHORS": {
      "schema_version": "G3_2.2.2e",
      "description": "Documents the Bayesian Priors established in Phases A and B.",
      "near_term_anchors": "object (Guidance and Consensus)",
      "long_term_anchors": "object (Mandatory Numeric Base Rate Distributions: Must include {p10: float, p50: float, p90: float} for every exogenous driver)"
    },

    "A.2_ANALYTIC_KG": {
      "schema_version": "G3_2.2.2e",
      "metadata": {
        "atp_complexity_assessment": "string (LOW / MODERATE / HIGH)",
        "atp_mode": "string (ATP-Lite / Full ATP)"
      },
      "core_data": {
        "__COMMENT__": "CRITICAL: Must use the nested 'Y0_data' key for the Kernel to read history.",
        "Y0_data": "object (Key-Value pairs of Y0 financials, e.g., {'Revenue': 100.0, 'EBIT': 20.0})",
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
- **params**: Mode-specific parameters (see G3BASE_2.2.2e_NORMDEFS.md)
- **qualitative_thesis**: Bayesian justification tracing Prior → Posterior
