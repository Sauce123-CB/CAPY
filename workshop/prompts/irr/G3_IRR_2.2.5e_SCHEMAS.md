Appendix A: Schemas


{
  "schema_version": "G3_2.2.5eIRR",


  "metadata": {
    "company_name": "string",
    "ticker": "string (EXCHANGE:SYMBOL)",
    "analysis_date": "string (YYYY-MM-DD)",
    "horizon": "string (T+1)",
    "source_cvr_state": "string (STATE_4)"
  },


  "resolution_estimates": [
    {
      "scenario_id": "string (S1, S2, ...)",
      "scenario_name": "string",
      "full_magnitude_m": "float (from A.10/A.12, IVPS impact)",
      "resolution_percentage_rho": "float (0.0 to 1.0)",
      "effective_magnitude": "float (rho × full_m)",
      "resolution_evidence": {
        "primary_driver": "string (LEGAL_TIMELINE | PRODUCT_ROADMAP | MACRO_OBSERVABLE | EARNINGS_DISCLOSURE | OTHER)",
        "key_dates": [
          {
            "event": "string",
            "expected_date": "string (YYYY-MM or YYYY-QN)",
            "information_revealed": "string (what uncertainty resolves)"
          }
        ],
        "reference_class": "string | null (historical analogues for timing)",
        "evidence_summary": "string (brief justification for rho estimate)"
      },
      "rho_confidence": "string (HIGH | MEDIUM | LOW)"
    }
  ],


  "aggregate_diagnostics": {
    "average_rho": "float",
    "rho_above_50_flag": "boolean",
    "scenarios_with_low_confidence": ["string (scenario_ids)"],
    "dominant_resolution_driver": "string (most common primary_driver across scenarios)"
  },


  "null_case_specification": {
    "description": "The state where no scenarios resolve beyond their rho-weighted partial resolution",
    "effective_scenario_overlay": "string (summary of partial impacts embedded in null)",
    "residual_uncertainty_narrative": "string (what remains unresolved at T+1)"
  },

  "version_control": {
    "paradigm": "G3 Meta-Prompting Doctrine v2.4 (Two-Shot Guided Autonomy)",
    "pipeline_stage": "IRR G3_2.2.5e",
    "execution_model": "Two-Shot (T1=Analytical, T2=Computational)",
    "int_compatibility": "G3INT 2.2.3e"
  },

  "convergence_rate_assessment": {
    "base_rate": 0.20,
    "adjustments": [
      {
        "category": "Information | Attention | Microstructure | Narrative",
        "factor": "string",
        "condition": "string",
        "adjustment": "float (±X.XX)"
      }
    ],
    "total_adjustment": "float",
    "cr_final": "float (capped to [0.10, 0.40])",
    "deviation_rationale": "string | null (required if CR > 0.30 or CR < 0.12)"
  },

  "multiple_selection": {
    "primary_metric": "EV_Revenue | EV_EBITDA | EV_FCF",
    "secondary_metric": "string | null",
    "weighting": {"primary": "float", "secondary": "float"},
    "selection_rationale": "string (per B.10 rubric)"
  },

  "anti_narrative_check": {
    "reasons_market_may_not_rerate": [
      "string (reason 1)",
      "string (reason 2)",
      "string (reason 3)"
    ]
  },

  "validated_inputs": {
    "price_t0": "float",
    "shares_outstanding": "float",
    "net_debt_t0": "float",
    "fundamentals_y0": {
      "revenue": "float",
      "ebitda": "float",
      "fcf": "float"
    },
    "fundamentals_y1": {
      "revenue": "float",
      "ebitda": "float",
      "fcf": "float"
    },
    "valuation_anchor": {
      "e_ivps_state4": "float",
      "dr_static": "float",
      "base_case_ivps_state2": "float"
    },
    "scenarios_finalized": "array (from state_4_active_inputs)",
    "hurdle_rate": "float"
  }
}


{
  "schema_version": "G3_2.2.5eIRR",


  "metadata": {
    "company_name": "string",
    "ticker": "string (EXCHANGE:SYMBOL)",
    "analysis_date": "string (YYYY-MM-DD)",
    "current_price_p0": "float",
    "horizon": "string (T+1)",
    "source_cvr_state": "string (STATE_4)",
    "hurdle_rate": "float (e.g., 0.15 for 15%)",
    "methodology": "string (always 'TRANSITION_FACTOR')",
    "pipeline_fit_grade": "string (A | B | C | D | F)",
    "pipeline_fit_caveat": "string | null"
  },

  "version_control": {
    "paradigm": "G3 Meta-Prompting Doctrine v2.4 (Two-Shot Guided Autonomy)",
    "pipeline_stage": "IRR G3_2.2.5e",
    "execution_model": "Two-Shot (T1=Analytical, T2=Computational)",
    "int_compatibility": "G3INT 2.2.3e"
  },


  "transition_factor_analysis": {
    "_description": "Patch 2.3: Replaces cohort-based anchor_establishment",
    "market_multiple_t0": "float (current market-implied EV/Revenue or EV/EBITDA)",
    "dcf_multiple_t0": "float (DCF-implied multiple at T0)",
    "market_dcf_ratio": "float (market_multiple / dcf_multiple, 1.0 = fair value)",
    "transition_factor": "float (TF = DCF_Multiple_T1 / DCF_Multiple_T0)",
    "market_multiple_t1_null": "float (market_multiple_t0 × TF)",
    "dcf_multiple_t1": "float (DCF-implied multiple at T+1)",
    "ivps_t0": "float (DCF intrinsic value per share at T0)",
    "ivps_t1": "float (projected IVPS at T+1 = IVPS_T0 × (1 + DR))",
    "dr_static": "float (discount rate used)",
    "capital_allocation": "string (RETAIN_FCF | DISTRIBUTE_FCF)",
    "calculation_trace": "string (human-readable calculation steps)",
    "convergence_rate_applied": "float (CR from A.13, range [0.10, 0.40])",
    "gap_t1": "float (DCF_Multiple_T1 - Market_Multiple_T1_Null)",
    "cr_contribution": "float (CR × Gap_T1)",
    "adjusted_market_multiple_t1": "float (Market_Multiple_T1_Null + CR_Contribution)"
  },


  "null_case_analysis": {
    "_description": "Patch 2.3: Simplified for TF approach",
    "fundamentals_t1": {
      "revenue": "float",
      "ebitda": "float",
      "ebitda_margin": "float",
      "fcf": "float",
      "growth_rate_y0_to_y1": "float"
    },
    "market_multiple_t0": "float (current market-implied multiple)",
    "dcf_implied_multiple_t0": "float (DCF-derived multiple at T0)",
    "market_dcf_ratio_t0": "float (market / DCF, 1.0 = fair value)",
    "transition_factor": "float (TF = DCF_T1 / DCF_T0)",
    "market_multiple_t1_null": "float (market_t0 × TF)",
    "dcf_implied_multiple_t1": "float",
    "null_case_irr": "float (simple IRR from price_t0 to price_t1)",
    "expected_price_t1_null": "float",
    "interpretation": "string (human-readable explanation of null IRR vs DR)"
  },


  "fork_analysis": {
    "multiple_selection": {
      "primary_metric": "string",
      "secondary_metric": "string | null",
      "weighting": {"primary": "float", "secondary": "float"},
      "selection_rationale": "string"
    },
    "scenario_multiple_impacts": {
      "_description": "Patch 2.3: Derived from IVPS impacts, not cohort spread",
      "scenario_id": "float (multiple delta = IVPS_impact × FDSO / Metric_T1)"
    },
    "forks": [
      {
        "fork_id": "string (e.g., 'NULL', 'S1', 'S1_S2', ...)",
        "scenarios_active": ["string (scenario_ids)"],
        "fork_probability": "float (from JPD)",
        "fork_fundamentals": {
          "_description": "Patch 2.1: ρ-blended fundamentals for this fork",
          "revenue": "float",
          "ebitda": "float",
          "fcf": "float",
          "metric_used": "float (value of primary metric for this fork)",
          "is_base_case": "boolean (true if no adjustments applied)",
          "adjustments_applied": ["object (scenario adjustment details)"]
        },
        "multiple_assignment": {
          "_description": "Patch 2.3: TF-based multiple evolution",
          "market_multiple_t0": "float",
          "transition_factor": "float",
          "base_multiple_t1": "float (market_t0 × TF)",
          "scenario_adjustment": "float (Σ ρ_i × impact_i)",
          "fork_market_multiple_t1": "float (base + adjustment)",
          "calculation_trace": "string",
          "valuation_metric": "string",
          "valuation_fallback_flag": "boolean"
        },
        "valuation_t1": {
          "ev": "float",
          "net_debt": "float",
          "equity_value": "float",
          "shares_outstanding": "float",
          "price_t1": "float"
        },
        "fork_irr": "float"
      }
    ]
  },


  "irr_integration": {
    "e_irr": "float (probability-weighted expected IRR)",
    "irr_distribution": {
      "p10": "float",
      "p25": "float",
      "p50_median": "float",
      "p75": "float",
      "p90": "float",
      "standard_deviation": "float"
    },
    "probability_above_hurdle": "float (P(IRR > hurdle_rate))",
    "probability_of_loss": "float (P(IRR < 0))",
    "return_attribution": {
      "_description": "Patch 2.4: Simplified from 3-component decomposition",
      "null_case_irr": "float (IRR with no scenario resolution)",
      "scenario_resolution_contribution": "float (E[IRR] - null_case_irr)",
      "total_e_irr": "float (should equal e_irr)"
    }
  },


  "sanity_checks": {
    "null_irr_vs_dr_test": {
      "_description": "Patch 2.4: Replaces value_trap_test for TF approach",
      "null_case_irr": "float",
      "discount_rate": "float",
      "market_dcf_ratio": "float",
      "deviation_from_dr": "float (null_irr - dr)",
      "interpretation": "string (explains whether deviation is expected given market/DCF ratio)"
    },
    "fork_dispersion_check": {
      "irr_cv": "float (coefficient of variation of fork IRRs)",
      "irr_range": {"min": "float", "max": "float"},
      "fundamentals_vary": "boolean (true if fork fundamentals differ)",
      "interpretation": "string"
    },
    "diagnostic_flags": {
      "average_rho_above_50": "boolean",
      "all_fork_irrs_positive": "boolean",
      "market_significantly_overvalued": "boolean (market_dcf_ratio > 1.5)",
      "market_significantly_undervalued": "boolean (market_dcf_ratio < 0.67)",
      "flags_triggered": ["string"]
    }
  },


  "confidence_assessment": {
    "overall_confidence": "string (HIGH | MEDIUM | LOW)",
    "key_uncertainties": ["string"],
    "highest_leverage_assumptions": [
      {
        "assumption": "string",
        "current_value": "float | string",
        "sensitivity": "string (qualitative impact if wrong)"
      }
    ],
    "recommendation_summary": "string"
  }
}

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
