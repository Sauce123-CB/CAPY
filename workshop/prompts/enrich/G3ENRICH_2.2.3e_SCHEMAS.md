# G3ENRICH 2.2.3e: Artifact Schemas (Appendix A)

> **Version:** 2.2.3e
> **Parent Document:** G3ENRICH_2.2.3e_PROMPT.md
> **Note:** Unchanged from 2.2.2e (schemas same, version bump for consistency)

This file defines the JSON schemas for all ENRICHMENT stage artifacts.

---

## CVR_SCHEMAS_G3_2.2.3e.json

```json
{
  "version_control": {
    "paradigm": "G3 Meta-Prompting Doctrine v2.4 (Two-Shot Guided Autonomy)",
    "pipeline_stage": "ENRICHMENT G3_2.2.3e",
    "date": "2024-12-23",
    "base_compatibility": "G3BASE 2.2.3e",
    "rq_compatibility": "G3RQ 2.2.3"
  },
  "schemas": {
    "A.1_EPISTEMIC_ANCHORS": {
      "schema_version": "G3_2.2",
      "description": "Documents the Bayesian Priors. Passed through from BASE with refinement authority.",
      "mutation_policy": "REFINEMENT_AUTHORIZED (High burden of proof. Requires superior third-party data.)",
      "structure": {
        "near_term_anchors": {
          "description": "Management Guidance and Wall Street Consensus (Y1-Y3)",
          "guidance": {
            "metric_name": {
              "value": "float",
              "period": "string (e.g., FY25)",
              "source": "string",
              "date": "YYYY-MM-DD"
            }
          },
          "consensus": {
            "metric_name": {
              "value": "float",
              "period": "string",
              "source": "string",
              "status": "string (utilized | stale | N/A)",
              "reasoning": "string"
            }
          }
        },
        "long_term_anchors": {
          "description": "Industry Base Rate Distributions for exogenous drivers. MANDATORY: Must include p10, p50, p90.",
          "Driver_Handle": {
            "metric": "string (e.g., Terminal EBIT Margin)",
            "base_rate_distribution": {
              "p10": "float (10th percentile)",
              "p50": "float (median)",
              "p90": "float (90th percentile)"
            },
            "source": "string (e.g., Industry study, Damodaran data, Historical analysis)",
            "sample_description": "string (e.g., 'SaaS companies >$500M revenue, 2015-2024')"
          }
        }
      }
    },
    "A.2_ANALYTIC_KG": {
      "schema_version": "G3_2.2",
      "description": "The Analytic Knowledge Graph containing source data. Updatable if RQs provide superior Y0 data.",
      "mutation_policy": "UPDATE_AUTHORIZED (Document in A.9 kg_changelog. ATP reconciliations should be preserved unless RQ evidence provides superior economic data.)",
      "structure": {
        "metadata": {
          "atp_complexity_assessment": "string (LOW / MODERATE / HIGH — inherited from BASE)",
          "atp_mode": "string (ATP-Lite / Full ATP — inherited from BASE)"
        },
        "company_info": {
          "company_name": "string",
          "ticker": "string (EXCHANGE:SYMBOL)",
          "currency": "string (e.g., USD)"
        },
        "core_data": {
          "__CRITICAL__": "Must use the nested 'Y0_data' key for Kernel compatibility. Values reflect ATP-reconciled economic definitions from BASE.",
          "Y0_data": {
            "__COMMENT__": "Key-Value pairs of Y0 financials and operational metrics (ATP-reconciled).",
            "Revenue": "float",
            "EBIT": "float",
            "Invested_Capital": "float",
            "Operational_Metric_N": "float (Any driver with Y0 history)"
          },
          "TSM_data": {
            "__COMMENT__": "Trailing Twelve Month or most recent period data.",
            "metric_name": "float"
          }
        },
        "accounting_translation_log": {
          "__COMMENT__": "Inherited from BASE. Documents reconciliation of reported figures to economic definitions per ATP (P1.5 in BASE).",
          "__MUTATION_POLICY__": "PRESERVE unless RQ evidence provides demonstrably superior economic data. Any updates must be documented in A.9 kg_changelog with explicit justification.",
          "schema": {
            "metric_name": {
              "source_metric": "string",
              "source_reference": "string",
              "adjustments_applied": ["array of strings"],
              "normative_alignment": "string",
              "confidence": "string (High / Medium / Low)",
              "flags": ["array of strings"]
            }
          }
        },
        "market_context": {
          "Current_Stock_Price": "float (REQUIRED for Implied Multiples)",
          "RFR": "float (Risk-Free Rate)",
          "ERP": "float (Equity Risk Premium, typically 5.0%)",
          "TAM_estimate": {
            "value": "float",
            "unit": "string",
            "source": "string"
          }
        },
        "share_data": {
          "shares_out_basic": "float",
          "shares_out_diluted_tsm": "float (TSM-adjusted, STATIC for forecast)",
          "tsm_calculation_trace": {
            "options_outstanding": "float",
            "avg_strike_price": "float",
            "rsu_psu_outstanding": "float"
          }
        },
        "capital_structure": {
          "net_debt_y0": {
            "gross_debt": "float",
            "cash_equivalents": "float",
            "net_debt": "float"
          }
        }
      }
    },
    "A.3_CAUSAL_DAG": {
      "schema_version": "G3_2.2",
      "description": "The unified DAG defining structure, dependencies, and equations. Consolidated format (structure + equations).",
      "mutation_policy": "ENRICHMENT_AUTHORIZED (Additive only. Requires verifiable RQ evidence. Document in A.9 dag_changelog.)",
      "structure": {
        "DAG": {
          "__COMMENT__": "Dictionary where keys are Node Names.",
          "Node_Name": {
            "type": "string (Exogenous_Driver | Endogenous_Driver | Financial_Line_Item)",
            "parents": ["list of strings (Explicit dependencies for documentation)"],
            "equation": "string (Python-executable. Use PREV('Var') for lagged, GET('Var') for intra-timestep.)"
          }
        },
        "coverage_manifest": {
          "__COMMENT__": "P5 DAG Fidelity audit trail from BASE.",
          "Y0_data_coverage": {
            "metric_name": "string (maps_to_node | derivative_of | excluded)",
            "disposition": "string (node reference or justification)"
          }
        }
      }
    },
    "A.5_GESTALT_IMPACT_MAP": {
      "schema_version": "G3_2.2E",
      "description": "The map of exogenous driver assumptions. Primary refinement target for ENRICHMENT.",
      "mutation_policy": "UPDATE_REQUIRED (Core ENRICHMENT output)",
      "structure": {
        "GIM": {
          "__COMMENT__": "Dictionary where keys are Driver Handles (must align with A.3 Exogenous nodes).",
          "Driver_Handle": {
            "mode": "string (STATIC | LINEAR_FADE | CAGR_INTERP | S_CURVE | MULTI_STAGE_FADE | EXPLICIT_SCHEDULE)",
            "params": {
              "__COMMENT__": "Mode-specific parameters. See G3ENRICH_2.2.2e_NORMDEFS.md for definitions."
            },
            "qualitative_thesis": "string (Causal Chain Justification. MUST include Variance Justification with percentile ranking if deviating from A.1 anchors.)"
          }
        }
      }
    },
    "A.6_DR_DERIVATION_TRACE": {
      "schema_version": "G3_2.2.2e",
      "description": "Discount Rate derivation. Presumptively stable with revision authority.",
      "mutation_policy": "REVISION_AUTHORIZED (High burden of proof. Requires RQ evidence of material risk factors. Document in A.9 dr_changelog.)",
      "structure": {
        "derivation_trace": {
          "RFR": "float",
          "ERP": "float",
          "X_Risk_Multiplier": "float (0.5 to 2.2)",
          "DR_Static": "float"
        },
        "justification": "string (Risk Multiplier justification narrative from BASE)"
      }
    },
    "A.7_LIGHTWEIGHT_VALUATION_SUMMARY": {
      "schema_version": "G3_2.2",
      "description": "The Selective Emission output from CVR Kernel. Recalculated in ENRICHMENT.",
      "mutation_policy": "RECALCULATED (Kernel output)",
      "structure": {
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
          "Market_EV_Sales_Y1": "float or null",
          "Market_EV_EBIT_Y1": "float or null",
          "Market_P_NOPAT_Y1": "float or null"
        },
        "sensitivity_analysis": {
          "tornado_summary": [
            {
              "Driver_Handle": "string",
              "IVPS_Low": "float",
              "IVPS_High": "float",
              "IVPS_Swing_Percent": "float"
            }
          ]
        },
        "key_forecast_metrics": {
          "Revenue_CAGR_Y1_Y5": "float",
          "EBIT_Margin_Y5": "float",
          "ROIC_Y5": "float"
        },
        "terminal_drivers": {
          "Terminal_ROIC": "float",
          "Terminal_RR": "float",
          "Terminal_g": "float"
        },
        "forecast_trajectory_checkpoints": {
          "__COMMENT__": "Nominal values at checkpoints for auditability.",
          "Y0": {"metric_name": "float"},
          "Y5": {"metric_name": "float"},
          "Y10": {"metric_name": "float"},
          "Y20": {"metric_name": "float"}
        }
      }
    },
    "A.9_ENRICHMENT_TRACE": {
      "schema_version": "G3_2.2.2e",
      "description": "The mandatory artifact documenting the Bayesian synthesis process, conflict resolution, and all modifications to State 1 artifacts.",
      "mutation_policy": "NEW (Created in ENRICHMENT)",
      "structure": {
        "inherited_lynchpins": {
          "__COMMENT__": "Passthrough from A.8_RESEARCH_STRATEGY_MAP for traceability.",
          "lynchpins": [
            {
              "ID": "string (e.g., L1)",
              "Driver_Handle": "string",
              "Tornado_Rank": "integer",
              "IVPS_Swing_Percent": "float"
            }
          ]
        },

        "research_synthesis": {
          "__COMMENT__": "Per-RQ analysis summaries using 7-slot architecture.",
          "rq_summaries": [
            {
              "RQ_ID": "string (e.g., RQ1)",
              "Coverage_Objective": "string (M-1 | M-2 | M-3a | M-3b | D-1 | D-2 | D-3)",
              "Platform": "string (AS | GDR)",
              "Key_Findings": "string"
            }
          ],
          "cross_cutting_themes": ["string"],
          "critical_tensions": ["string"]
        },

        "conflict_resolution_log": [
          {
            "conflict_id": "string",
            "description": "string",
            "sources_involved": ["string"],
            "resolution_approach": "string (reconciliation | source_priority | conservative_default)",
            "resolution_rationale": "string",
            "residual_uncertainty": "string (LOW | MEDIUM | HIGH)"
          }
        ],

        "gim_changelog": [
          {
            "driver_handle": "string",
            "lynchpin_id": "string | null (Reference to inherited_lynchpins.ID if applicable)",
            "rq_citations": ["string (e.g., RQ2/M-2, RQ5/D-1)"],
            "prior_state": {
              "mode": "string",
              "params": {},
              "thesis_summary": "string"
            },
            "evidence_synthesis": "string",
            "anchor_reconciliation": {
              "anchor_reference": "string",
              "prior_percentile": "string",
              "posterior_percentile": "string",
              "variance_justification": "string | null"
            },
            "decision": "string (MODIFY | CONFIRM)",
            "posterior_state": {
              "mode": "string",
              "params": {},
              "qualitative_thesis": "string"
            },
            "expected_valuation_impact": "string"
          }
        ],

        "dr_changelog": [
          {
            "__COMMENT__": "Empty array if DR unchanged. Documents any DR revision per P2 protocol.",
            "rq_citation": "string (e.g., RQ1/M-1)",
            "risk_factor_identified": "string",
            "x_multiplier_component_affected": "string (e.g., governance_risk, financial_risk)",
            "prior_x": "float",
            "posterior_x": "float",
            "prior_dr": "float",
            "posterior_dr": "float",
            "justification": "string"
          }
        ],

        "dag_changelog": [
          {
            "__COMMENT__": "Empty array if no DAG enrichment. Rare event.",
            "change_type": "string (NODE_ADDED | EQUATION_REFINED)",
            "node_name": "string",
            "rq_citation": "string",
            "justification": "string",
            "gim_linkage": "string"
          }
        ],

        "kg_changelog": [
          {
            "__COMMENT__": "Empty array if no KG updates.",
            "metric_name": "string",
            "data_type": "string (Y0_data | TSM_data | market_context)",
            "rq_citation": "string",
            "previous_value": "float | string",
            "updated_value": "float | string",
            "justification": "string"
          }
        ],

        "anchor_changelog": [
          {
            "__COMMENT__": "Empty array if no anchor refinements. High bar for inclusion.",
            "anchor_type": "string (near_term | long_term)",
            "driver_handle": "string",
            "rq_citation": "string",
            "previous_distribution": {
              "p10": "float",
              "p50": "float",
              "p90": "float",
              "source": "string"
            },
            "updated_distribution": {
              "p10": "float",
              "p50": "float",
              "p90": "float",
              "source": "string"
            },
            "burden_of_proof_justification": "string"
          }
        ],

        "boundary_conditions": {
          "scenario_exclusion_check": {
            "status": "string (PASS | EXCEPTION_APPLIED)",
            "p1_events_incorporated": "boolean",
            "p1_event_citations": ["string (Document references for P=1.0 events)"],
            "notes": "string"
          },
          "economic_governor_check": {
            "status": "string (PASS | RECONCILED)",
            "terminal_g": "float",
            "terminal_roic": "float",
            "notes": "string"
          }
        },

        "cvr_comparison": {
          "state_1_ivps": "float",
          "state_2_ivps": "float",
          "ivps_delta_absolute": "float",
          "ivps_delta_percent": "float",
          "dr_comparison": {
            "state_1_dr": "float",
            "state_2_dr": "float",
            "dr_revised": "boolean"
          },
          "terminal_g_comparison": {
            "state_1_g": "float",
            "state_2_g": "float"
          },
          "primary_drivers_of_change": [
            {
              "driver_handle": "string",
              "contribution_direction": "string (+ | -)",
              "contribution_estimate": "string"
            }
          ],
          "dr_contribution": {
            "__COMMENT__": "Null if DR unchanged. Separate attribution for DR revision impact.",
            "contribution_direction": "string (+ | -) | null",
            "contribution_estimate": "string | null"
          }
        },

        "error_recovery_log": [
          {
            "__COMMENT__": "Empty array if no errors.",
            "error_type": "string",
            "fix_applied": "string"
          }
        ]
      }
    }
  }
}
```

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
