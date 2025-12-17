G3ENRICH 2.2.1e: Bayesian Causal Synthesis
I. MISSION AND OBJECTIVES
* Mission: Execute the ENRICHMENT stage (G3_2.2.1e) of the CAPY Pipeline for {Company Name} ({EXCHANGE:TICKER}) as of {DATE}.
* Primary Objective: To synthesize deep research (RQ Outputs), refine the Base Case assumptions (GIM) using a rigorous Bayesian Update protocol, and recalculate the valuation, transitioning from MRC State 1 to MRC State 2.
* Execution Paradigm: Guided Autonomy and Bayesian Synthesis. This stage requires high-level reasoning to interpret research, resolve conflicting evidence, translate insights into precise quantitative adjustments, and maintain epistemic rigor through explicit anchoring and variance justification.

I.A EXECUTION PROTOCOL (Two-Shot Architecture)

Turn Structure
This prompt governs a two-turn execution cycle. Each turn executes in a fresh Claude instance with clean context, maximizing reasoning depth through separation of concerns.

Turn 1: Analytical Synthesis
Trigger: "Do Turn 1: ENRICHMENT for {Company Name}, {EXCHANGE:TICKER}"

Attachments Required:
- This prompt (G3ENRICH_2.2.1e.md)
- MRC State 1 Output ({TICKER}_BASE2.2.1eO_T2_{YYYYMMDD}.md)
- A.8_RESEARCH_STRATEGY_MAP (from RQ output)
- RQ Outputs (1-6)
- CVR_KERNEL_ENRICH_2.2.1e.py (reference context only)

Scope: Execute Phases A-D. Produce unified narratives (N1-N5) and artifacts A.1-A.6, A.9. Artifact A.7 is NOT computed.

Output: Unified emission per Section V. Filename: {TICKER}_ENRICH2.2.1eO_T1_{YYYYMMDD}.md

Exclusion: Do NOT execute Kernel. Kernel is provided for semantic alignment only.

Turn 2: Validation & Execution
Trigger: "Do Turn 2"

Attachments Required:
- This prompt (G3ENRICH_2.2.1e.md)
- Turn 1 Output ({TICKER}_ENRICH2.2.1eO_T1_{YYYYMMDD}.md)
- CVR_KERNEL_ENRICH_2.2.1e.py

Scope: Validate Turn 1 artifacts for JSON integrity and internal consistency, repair if needed, execute kernel, produce A.7, emit unified MRC State 2 report.

Output: Complete MRC State 2. Filename: {TICKER}_ENRICH2.2.1eO_T2_{YYYYMMDD}.md

Rationale
The two-shot architecture provides:
- Reasoning Depth: Turn 1 focuses purely on Bayesian synthesis without computational overhead.
- Error Correction: Turn 2 operates as a validation layer, catching JSON malformation and logical inconsistencies before kernel execution.
- Clean Context: Fresh instances prevent context pollution and attention degradation.

II. EXECUTION ENVIRONMENT AND CONSTRAINTS
A. Environmental Awareness and Tools
* Mandatory Inputs:
   1. MRC State 1 (BASE Output): The 6 artifacts (A.1, A.2, A.3, A.5, A.6, A.7) produced by G3BASE 2.2.1e.
   2. A.8_RESEARCH_STRATEGY_MAP: The targeted research plan from RQ_GEN 2.2.2, containing Uncertainty_Nexus_Analysis and Research_Plan.
   3. RQ Outputs (1-6): The research reports produced by the RQ execution stage, organized by Coverage_Objective (M-1/M-2/M-3/D-1/D-2/D-3).
* The Verification Doctrine (Externalized Schemas): The required output schemas are provided in the attached Appendix A. The A.9_ENRICHMENT_TRACE schema is new to this stage.
* The CVR Kernel (Context Reference): The CVR Kernel (Appendix C, also attached as CVR_KERNEL_ENRICH_2.2.1e.py) defines the computational logic that Turn 2 will execute. It is provided in Turn 1 for CONTEXTUAL UNDERSTANDING ONLY—to ensure your artifacts are semantically aligned with kernel expectations (DSL modes, node naming, equation syntax). Do NOT attempt to execute this code in Turn 1.
* Search Policy: Minimize search. ENRICHMENT focuses on synthesizing provided inputs. Ad-hoc search is permitted ONLY for clarifying specific data points explicitly referenced within the RQ Outputs or for validating critical factual claims where ambiguity remains high after synthesis.
* Emission Policy: The output must ONLY contain analytical narratives and artifacts. Reprinting instructions, schemas, or the CVR Kernel code is strictly forbidden.

B. Two-Shot Execution Architecture (Critical)

This prompt operates in TWO-SHOT EXECUTION mode with strict separation of concerns:

TURN 1 RESPONSIBILITY (Analytical Instance):
- Synthesize RQ evidence using Bayesian Update Protocol
- Construct refined analytical artifacts (A.1–A.6, A.9) with full epistemic rigor
- Produce unified narratives (N1-N5)
- Emit artifacts as valid JSON in a single fenced code block
- Ensure structural compatibility with kernel requirements
- Do NOT execute kernel code or compute A.7

TURN 2 RESPONSIBILITY (Validation & Execution Instance):
- Validate JSON integrity and repair malformation if present
- Verify internal consistency (DAG coverage, GIM-KG alignment, DR consistency)
- Execute kernel using validated artifacts as input
- Generate A.7 (LightweightValuationSummary)
- Emit unified MRC State 2 report

This architecture leverages Turn 1's strengths (deep reasoning, Bayesian synthesis, evidence integration) while Turn 2 provides a validation layer and deterministic computation.

C. The Efficiency Protocol (No State Reconstruction)
* Mandate: Do NOT execute the Kernel to reconstruct State 1. Trust the input artifacts from BASE.
* Action: Extract the State 1 baseline (IVPS, DR, Terminal g, key metrics) directly from the input A.7_LIGHTWEIGHT_VALUATION_SUMMARY. This establishes the computational baseline for comparison without redundant execution.
* Rationale: The MRC paradigm guarantees deterministic reconstruction. Re-execution would consume substantial resources without analytical benefit.
III. CORE ANALYTICAL DIRECTIVES
P1. Analytical Autonomy and Deep Synthesis (The Synthesis Mandate)
ENRICHMENT is fundamentally an evidence integration task. You must synthesize diverse, potentially conflicting research into a coherent analytical update.
* The Conflict Resolution Protocol:
   * Source Credibility Assessment: Evaluate the provenance, methodology, and potential biases of each RQ source. Primary data and audited figures take precedence over secondary commentary.
   * Reconciliation Before Rejection: Attempt to reconcile conflicting data through reasoning (e.g., different time periods, different definitions, different market segments) before defaulting to one source.
   * Ambiguity Handling: When ambiguity remains high after good-faith reconciliation, apply conservative judgment. Document the uncertainty explicitly in A.9.
   * The Anti-Narrative Mandate: Do not force-fit research findings into a pre-existing thesis. Allow the evidence to update your priors, even when this creates tension with the BASE narrative.
* The Holistic Integration Mandate: RQs are not independent inputs. You must identify cross-cutting themes, corroborating evidence, and contradictions across the full RQ set before making refinement decisions.
P2. Structural Constraints (Pipeline Stability)
ENRICHMENT operates within analytical guardrails that ensure pipeline integrity and economic validity.
* DR Revision Protocol:
   - Default: DR is presumptively stable. The BASE risk assessment is inherited unless RQ evidence contradicts it.
   - Revision Authority: DR modification is authorized if and only if RQ outputs (particularly M-1 Integrity or M-2 Adversarial findings) reveal material risk factors not assessable from BASE source documents.
   - Burden of Proof: Revision requires (a) specific RQ citation, (b) explicit mapping to X multiplier component (e.g., "governance risk adjustment +0.15 due to [evidence]"), (c) quantified DR delta.
   - Trace Requirement: Any DR modification MUST be documented in A.9 via the `dr_changelog` field with prior/posterior X values and evidence justification.
   - Valuation Bridge Separation: N5 (Enrichment Synthesis) MUST separately attribute IVPS change from GIM refinements vs. DR revision.
* SCM Stability Mandate (With Enrichment Authority):
   * The Enrichment Exception: You are authorized to enrich the DAG structure ONLY if the RQs provide verifiable new evidence that enables a richer causal decomposition (e.g., revealing operational primitives that were aggregated in BASE due to data limitations).
   * The Constraint: ENRICHMENT does not have access to the primary company filings used in BASE. DAG enrichment should be rare. If triggered, document rigorously in A.9 with explicit citation to the RQ evidence.
   * Prohibition: Simplifying or collapsing the DAG structure is forbidden. Enrichment is additive only.
* The Economic Governor Mandate: Refinements to the GIM MUST maintain long-term economic consistency. The terminal state must satisfy the Value Driver constraint (g ≈ ROIC × RR). If refined assumptions produce an implausible terminal state (e.g., g ≥ DR, ROIC perpetually above cost of capital without moat justification), you must reconcile the assumptions before proceeding.
* Capital Dynamics Stability: The Static Share Count established in BASE (TSM Adjusted) MUST NOT be modified unless a clear calculation error is uncovered.
P3. Epistemic Anchoring (The Bayesian Update Protocol)
ENRICHMENT is a Bayesian process. You must explicitly frame the refinement workflow using this structure:
* The Bayesian Frame:
   * Priors: A.1_EPISTEMIC_ANCHORS (Base Rates and Long-Term Anchors) and the BASE GIM (A.5) represent your priors.
   * Evidence: The RQs provide the new evidence (likelihood function).
   * Posteriors: The refined GIM (A.5 State 2) represents your posteriors.
* The Anchor Refinement Protocol (Dynamic Anchors):
   * The Refinement Authority: You are authorized to update A.1 ONLY if the RQs provide demonstrably superior, objective, third-party data regarding the industry Base Rates (e.g., a rigorous academic study, authoritative industry report with larger sample size, or more recent data that supersedes the BASE sources).
   * The Burden of Proof: Updating an Anchor requires rigorous justification and citation in A.9, explaining precisely why the new data supersedes the BASE analysis. The bar is high.
* The Variance Mandate (Extraordinary Claims):
   * Posteriors (GIM assumptions) that deviate materially from the Anchors require explicit "Variance Justification" in A.9.
   * The justification must include: (a) the percentile ranking of the assumption relative to the Base Rate distribution, (b) the specific evidence supporting the deviation, and (c) the causal mechanism that explains why this company warrants an outlier assumption.
P4. Causal Chain Transparency (The Trace)
We mandate a complete, auditable trace of the refinement process, captured in A.9_ENRICHMENT_TRACE.
* Causal Chain Reconciliation: For every refinement (or confirmation), you must explicitly trace the linkage:
   RQ Evidence → Synthesis & Conflict Resolution (P1) → Reconciliation with Anchors (P3) → GIM/DAG/KG Modification Rationale → Valuation Impact
* The Changelog Mandate: A.9 must contain structured changelogs for:
   * GIM modifications (every driver reviewed)
   * DAG enrichment (if triggered)
   * KG updates (if Y0 data improved)
   * Anchor updates (if triggered)
* The CVR Comparison Mandate: A.9 must document the State 1 → State 2 valuation bridge, quantifying the IVPS change and attributing it to specific assumption changes.
* Lynchpin Inheritance Protocol:
   - ENRICHMENT inherits Lynchpin IDs from A.8_RESEARCH_STRATEGY_MAP.Uncertainty_Nexus_Analysis.Lynchpins[] as the primary iteration sequence.
   - The gim_changelog MUST cross-reference inherited Lynchpin IDs via the `lynchpin_id` field.
   - ENRICHMENT may elevate a non-Lynchpin driver to priority status ONLY if RQ evidence reveals uncertainty was materially underestimated in BASE (requires explicit documentation in A.9).
   - ENRICHMENT may NOT demote inherited Lynchpins—if evidence resolves uncertainty, the driver receives a "CONFIRM" decision with narrowed uncertainty bounds documented.
IV. EXECUTION PROTOCOL (The Workflow)
Execute the workflow (Phases A-E), integrating the Core Analytical Directives throughout. Synthesize narratives internally during the respective phases for the final unified emission.
A. Initialization and Baseline Confirmation (Phase A)
1. Ingestion: Ingest and parse MRC State 1 (A.1, A.2, A.3, A.5, A.6, A.7) and RQ Outputs (1-6).
2. Baseline Extraction (The Efficiency Protocol):
   * Extract State 1 metrics directly from A.7_LIGHTWEIGHT_VALUATION_SUMMARY:
      - IVPS (State 1)
      - DR
      - Terminal g
      - Terminal ROIC
      - Key Forecast Checkpoints (Y5, Y10, Y20)
      - Implied Multiples
      - Sensitivity Analysis results
   * These establish the baseline for comparison. Do NOT re-execute the Kernel.
B. Research Synthesis and Interpretation (Phase B)
1. Holistic Synthesis (P1):
   * Analyze all RQs (1-6) comprehensively before making any refinement decisions.
   * Identify overarching themes, corroborating patterns, and critical tensions.
   * Execute the Conflict Resolution Protocol for any contradictory findings.
2. RQ-Specific Analysis (by Coverage Objective):
   * Integrity and Adversarial Review (M-1, M-2):
      - Synthesize findings from the Integrity Check (M-1) and Adversarial Synthesis (M-2).
      - Assess impact on the overall investment thesis and risk profile.
      - If M-1/M-2 findings reveal material risk factors: Evaluate DR revision per P2 DR Revision Protocol.
   * Scenario Boundary Check (M-3):
      - Review the Historical Analogue Data (H.A.D.) for discrete scenarios in M-3.
      - Apply the Scenario Exclusion Mandate and P=1.0 Certainty Exception as appropriate.
   * Dynamic Allocation Evidence (D-1, D-2, D-3):
      - Synthesize Lynchpin fact-finding and contextual evidence from dynamically allocated RQs.
      - These provide the primary evidence base for GIM refinement.
      - Cross-reference RQ_ID to Coverage_Objective via A.8_RESEARCH_STRATEGY_MAP.Research_Plan.
C. Bayesian Refinement and Causal Tracing (Phase C — The Core Analysis)
Iterate through the assumptions, executing the Bayesian Update Protocol and documenting the Causal Chain.
1. Prioritized Iteration:
   * Begin with Lynchpins from A.8_RESEARCH_STRATEGY_MAP.Uncertainty_Nexus_Analysis (inherited from RQ stage).
   * Then systematically review remaining exogenous drivers in A.5_GESTALT_IMPACT_MAP.
2. For Each Driver, Execute the Protocol (P3/P4):
   a. State the Prior: Document the BASE assumption (DSL parameters) and the relevant A.1 Anchor (Base Rate distribution).
   b. Synthesize Evidence: Compile relevant findings from across the RQs. Apply Conflict Resolution if needed.
   c. Update the Posterior: Determine the refined assumption. Apply the Variance Mandate if deviating from the Anchor.
   d. Decision: Record MODIFY or CONFIRM.
   e. If MODIFY: Specify the updated DSL (mode and parameters). Utilize the Expanded DSL (Appendix B), including S_CURVE or MULTI_STAGE_FADE, if necessary to model the refined trajectory.
   f. Justification: Provide the causal rationale linking Evidence → Assumption → Expected Valuation Impact.
3. Constrained Refinement Protocols (P2/P3):
   * Anchor Refinement: If the evidence threshold is met (P3), update A.1_EPISTEMIC_ANCHORS. Document the superior data source and rationale in A.9.
   * DAG Enrichment: If the evidence threshold is met (P2), update A.3_CAUSAL_DAG. Ensure any new exogenous nodes are added to A.5 with appropriate DSL assumptions. Document in A.9.
   * KG Update: If RQs provided superior historical (Y0) data, update A.2_ANALYTIC_KG. Document in A.9. 
     * ATP Preservation Mandate: When modifying Y0_data, verify the update is consistent with the accounting_translation_log inherited from BASE. If the RQ evidence reveals a need to revise an ATP reconciliation (e.g., a different SBC treatment is more economically accurate), document both the Y0_data change AND the corresponding accounting_translation_log update in the kg_changelog.
4. Economic Governor Check:
   * Before proceeding to execution, verify that the refined GIM produces a plausible terminal state.
   * If g approaches or exceeds DR, or if terminal ROIC is economically implausible, you must revisit the assumptions and reconcile.
5. A.9 Construction (Ongoing):
   * Throughout Phase C, populate A.9_ENRICHMENT_TRACE with:
      - gim_changelog (every driver)
      - dag_changelog (if triggered)
      - kg_changelog (if triggered)
      - anchor_changelog (if triggered)
      - conflict_resolution_log (all material conflicts)
      - variance_justifications (all deviations from anchors)
D. Narrative Synthesis (Phase D)

Synthesize unified State 2 narratives for the final emission. ENRICHMENT inherits BASE narratives N1-N4 and produces updated State 2 versions, plus a new N5 synthesizing ENRICHMENT's analytical contribution.

Narrative Unification Protocol
For inherited narratives (N1-N4):
- If RQ evidence warrants material update: Rewrite section integrating new evidence
- If no material change: Passthrough with brief "[State 2: Confirmed, no material change from BASE]" annotation

N1. Investment Thesis (State 2)
Inherit BASE N1. Update where RQ evidence shifts thesis view—risks, catalysts, moat assessment, competitive position. Absorb executive synthesis framing (key RQ insights, aggregate thesis impact).

N2. Invested Capital Modeling (State 2)
Inherit BASE N2. Update only if DAG enrichment changed IC structure (rare).

N3. Economic Governor & Constraints (State 2)
Inherit BASE N3. Update if terminal constraints shifted materially due to GIM refinements. Incorporate extraordinary claims justification here if terminal assumptions exceed A.1 p90 or fall below p10.

N4. Risk Assessment & DR Derivation (State 2)
Inherit BASE N4. Mandatory update if DR revised per P2 DR Revision Protocol. Optional annotation if risk view shifted but DR held stable.

N5. Enrichment Synthesis (NEW)
ENRICHMENT's novel analytical contribution. Contains:
- Key Refinement Analysis: Detailed narratives on 2-4 most significant refinements (ordered by expected IVPS impact). Each traces full Causal Chain: Evidence → Interpretation → Anchor Reconciliation → Assumption Change → Valuation Impact.
- Valuation Bridge: Quantified State 1 → State 2 attribution. Tabular format preferred:
  | Driver | Prior Contribution | Posterior Contribution | Δ IVPS |
  |--------|-------------------|----------------------|--------|
- Cross-Cutting Themes: Patterns identified across RQ synthesis.
- DR Attribution (if applicable): Separate line item for IVPS change from DR revision vs. GIM refinements.

E. Computational Execution and Emission (Phase E — State 2)
1. CVR Kernel Loading (P7):
   * Load the CVR Kernel G3_2.2.1e (Appendix C, or attached CVR_KERNEL_ENRICH_2.2.1e.py) into the execution environment.
2. Sensitivity Scenario Definition:
   * Inherit sensitivity scenarios from BASE A.7 Tornado top-5 drivers plus Discount_Rate.
   * May add ≤2 additional scenarios if RQ evidence surfaces new high-sensitivity drivers not captured in BASE.
   * Format: [{'driver': 'Driver_Handle', 'low': pct_change, 'high': pct_change}]
   * Example: [{'driver': 'Revenue_Growth', 'low': -0.10, 'high': 0.10}, {'driver': 'Discount_Rate', 'low': -0.01, 'high': 0.01}]
3. CVR Kernel Execution (Selective Emission):
   * Execute execute_cvr_workflow.
   * Inputs:
      - kg: A.2_ANALYTIC_KG (potentially updated)
      - dag_artifact: A.3_CAUSAL_DAG (potentially enriched)
      - gim_artifact: A.5_GESTALT_IMPACT_MAP (updated)
      - dr_trace: A.6_DR_DERIVATION_TRACE (potentially revised per P2)
      - sensitivity_scenarios: The defined scenario list
   * Output: The recalculated A.7_LIGHTWEIGHT_VALUATION_SUMMARY (State 2).
4. Error Handling:
   * If execution fails (e.g., g ≥ DR, numerical instability), you must:
      a. Revisit Phase C and adjust the GIM to comply with the Economic Governor.
      b. Document the fix applied in A.9 (brief description of the constraint violation and resolution).
      c. Re-execute Phase E.
5. A.9 Finalization:
   * Update the cvr_comparison field in A.9_ENRICHMENT_TRACE with:
      - State 1 IVPS (from Phase A extraction)
      - State 2 IVPS (from Kernel output)
      - Delta (absolute and percentage)
      - Primary drivers of the change
6. Post-Execution Reality Check (P3/P5):
   * Review the updated Implied Multiples and Forecast Trajectory Checkpoints in A.7 (State 2).
   * Compare against the A.1 Anchors and historical benchmarks.
   * If results imply extraordinary outcomes: Incorporate justification into Narrative N3 (Phase D).
V. OUTPUT MANDATE (The Unified MRC State 2 Vector)
Emit the complete MRC State 2 in a single, unified block. The structure must be: Narratives followed immediately by the JSON artifacts.
[START OF UNIFIED EMISSION]
(I-IV.) Analytical Narratives
(Emit Narratives N1-N5 here. N1-N4 are State 2 versions of BASE narratives; N5 is ENRICHMENT's synthesis contribution.)
MRC State 2 Artifacts (A.1-A.9)
(Emit the JSON object containing the 7 artifacts here, strictly adhering to Appendix A schemas.)
```json
{
  "A.1_EPISTEMIC_ANCHORS": {...},
  "A.2_ANALYTIC_KG": {...},
  "A.3_CAUSAL_DAG": {...},
  "A.5_GESTALT_IMPACT_MAP": {...},
  "A.6_DR_DERIVATION_TRACE": {...},
  "A.7_LIGHTWEIGHT_VALUATION_SUMMARY": {...},
  "A.9_ENRICHMENT_TRACE": {...}
}
```
[END OF UNIFIED EMISSION]
—-------------
APPENDIX A: CVR_SCHEMAS_G3_2.2.1e.json
{
  "version_control": {
    "paradigm": "G3 Meta-Prompting Doctrine v2.4 (Two-Shot Guided Autonomy)",
    "pipeline_stage": "ENRICHMENT G3_2.2.1e",
    "date": "2025-12-07",
    "base_compatibility": "G3BASE 2.2.1e",
    "rq_compatibility": "G3RQ 2.2.2"
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
              "__COMMENT__": "Mode-specific parameters. See Appendix B.2 for definitions."
            },
            "qualitative_thesis": "string (Causal Chain Justification. MUST include Variance Justification with percentile ranking if deviating from A.1 anchors.)"
          }
        }
      }
    },
    "A.6_DR_DERIVATION_TRACE": {
      "schema_version": "G3_2.2.1e",
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
      "schema_version": "G3_2.2.1e",
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
          "__COMMENT__": "Per-RQ analysis summaries using dynamic allocation structure.",
          "rq_summaries": [
            {
              "RQ_ID": "string (e.g., RQ1)",
              "Coverage_Objective": "string (M-1 | M-2 | M-3 | D-1 | D-2 | D-3)",
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
—-------------
APPENDIX B: NORMATIVE DEFINITIONS AND DSL SPECIFICATION
B.1. Financial Definitions and Formulas
The following definitions are normative for all CVR calculations. They align with G3BASE 2.2.1e.
1. EBIT (Earnings Before Interest and Taxes)
   * Definition: Operating income MUST include Stock-Based Compensation (SBC) as an expense.
   * Rationale: SBC is a real economic cost representing dilution of existing shareholders.
2. NOPAT (Net Operating Profit After Tax)
   * Formula: NOPAT = EBIT × (1 - Tax_Rate)
3. Invested Capital (IC)
   * Definition: The total capital deployed in operating assets.
   * Typical Calculation: Operating Assets - Operating Liabilities, or equivalently, Equity + Net Debt (adjusted for non-operating items).
4. ROIC (Return on Invested Capital)
   * Formula: ROIC = NOPAT / PREV(Invested_Capital)
   * Timing Mandate: MUST use Beginning-of-Period (BOP) Invested Capital via PREV() function.
5. Reinvestment
   * Formula: Reinvestment = Δ Invested_Capital = IC(t) - IC(t-1)
6. Reinvestment Rate (RR)
   * Formula: RR = Reinvestment / NOPAT
   * Constraint: Bounded [0, 1] for steady-state; can exceed 1.0 during high-growth phases.
7. FCF (Unlevered Free Cash Flow)
   * Formula: FCF_Unlevered = NOPAT - Reinvestment
8. Growth (g) — The Value Driver Formula
   * Formula: g = ROIC × RR
   * Economic Interpretation: Sustainable growth rate consistent with reinvestment and returns.
   * Terminal Constraint: Terminal g MUST be < DR. Recommended ceiling: Long-term nominal GDP growth (2-4%).
9. Timing Convention Mandate (DAG Compliance)
   * The PREV() Rule: Calculations dependent on prior period balances MUST use PREV('Variable_Name').
   * Mandatory Applications: ROIC (uses PREV(Invested_Capital)), any stock-variable updates.
   * The GET() Rule: Intra-timestep access to already-calculated variables uses GET('Variable_Name').
10. Valuation Methodology (APV, 20-Year Explicit, Static DR)
    * Approach: Adjusted Present Value (APV) is mandated.
    * Forecast Horizon: 20-year explicit forecast.
    * Discount Rate: Static DR applied to all streams.
    * Terminal Value: Gordon Growth Model: TV = FCF_Y21 / (DR - g_terminal)
    * Equity Bridge: Equity_Value = Enterprise_Value - Net_Debt_Y0
    * IVPS: Equity_Value / Shares_Out_Diluted_TSM
11. ATP Mandate (Accounting Translation Protocol)
    * Inherited Constraint: All financial inputs in A.2 reflect ATP-reconciled economic definitions established in BASE (per BASE P1.5).
    * ENRICHMENT Responsibility: When updating Y0_data based on RQ evidence, ensure updates maintain consistency with the accounting_translation_log. If RQ evidence reveals a superior economic interpretation, document the change in A.9 kg_changelog with explicit reference to the ATP entry being superseded.
    * Normative Primacy: The normative definitions in this section (e.g., EBIT includes SBC) take precedence over raw reported figures, regardless of how metrics are labeled in source documents.
12. Tax Rate Sourcing
    * Tax_Rate: Exogenous driver or static assumption in GIM.
    * Default: Marginal statutory rate unless company-specific effective rate is justified with citation.
    * Treatment: Must be defined in A.5 GIM if variable; otherwise static in DAG equation.
13. Y0 Basis Convention
    * Y0_data reflects the most recent completed fiscal year unless explicitly noted as LTM (Last Twelve Months).
    * If LTM is used, document in A.2 metadata with period end date.
14. Negative Terminal ROIC Handling
    * If terminal ROIC ≤ 0, assume g = 0 and RR = 0 (no value-creating reinvestment).
    * Terminal value calculated using zero-growth perpetuity: TV = NOPAT_T / DR.
    * Document in A.9 boundary_conditions.economic_governor_check.
B.2. Assumption DSL Definitions (Expanded for ENRICHMENT)
The DSL (Domain-Specific Language) defines how an exogenous driver assumption evolves from Year 1 (Y1) to Year 20 (Y20). Y0 represents the historical starting value from A.2_ANALYTIC_KG.
The ENRICHMENT Kernel (G3_2.2.1e) supports six propagation modes:
—--
MODE: STATIC
Behavior: The value remains constant for all forecast years.
Required Params:
  - value (float): The constant value applied Y1-Y20.
Example:
{
  "mode": "STATIC",
  "params": {"value": 0.21}
}
—--
MODE: LINEAR_FADE
Behavior: Linearly interpolates from start_value to end_value over fade_years. Holds end_value thereafter.
Required Params:
  - start_value (float): Initial value at Y1. If omitted, Y0 from KG is used.
  - end_value (float): Target value at completion of fade.
  - fade_years (int): Number of years for the fade (1-20).
Mechanics:
  - Annual step = (end_value - start_value) / fade_years
  - Value at year t (t ≤ fade_years): start_value + (step × t)
  - Value at year t (t > fade_years): end_value
Example:
{
  "mode": "LINEAR_FADE",
  "params": {"start_value": 0.25, "end_value": 0.15, "fade_years": 10}
}
—--
MODE: CAGR_INTERP
Behavior: Compounds from start_value using a growth rate that interpolates from start_cagr to end_cagr over interp_years.
Required Params:
  - start_cagr (float): Initial annual growth rate (e.g., 0.15 for 15%).
  - end_cagr (float): Terminal annual growth rate.
  - interp_years (int): Years over which the CAGR fades (1-20).
Mechanics:
  - The growth rate linearly fades from start_cagr to end_cagr over interp_years.
  - Year t growth rate (t ≤ interp_years): start_cagr + ((end_cagr - start_cagr) × t / interp_years)
  - Year t growth rate (t > interp_years): end_cagr
  - Value compounds: Value(t) = Value(t-1) × (1 + growth_rate(t))
  - Y0 value sourced from KG (core_data.Y0_data).
Example:
{
  "mode": "CAGR_INTERP",
  "params": {"start_cagr": 0.20, "end_cagr": 0.03, "interp_years": 15}
}
—--
MODE: S_CURVE
Behavior: Models logistic (S-curve) growth—slow start, acceleration, deceleration toward saturation. Useful for market penetration, adoption dynamics, or margin expansion with natural ceilings.
Required Params:
  - start_value (float): Initial value at Y0/Y1. If omitted, Y0 from KG is used.
  - saturation_value (float): The asymptotic ceiling (or floor) the curve approaches.
  - inflection_year (float): The year at which growth is fastest (midpoint of the S).
  - steepness (float): Controls the rate of transition (higher = sharper S). Typical range: 0.3 to 1.5.
Mechanics:
  - Uses logistic function centered on inflection_year.
  - Formula: Value(t) = start_value + (saturation_value - start_value) / (1 + exp(-steepness × (t - inflection_year)))
  - At t << inflection_year: Value ≈ start_value
  - At t = inflection_year: Value ≈ midpoint between start and saturation
  - At t >> inflection_year: Value ≈ saturation_value
Example:
{
  "mode": "S_CURVE",
  "params": {"start_value": 0.05, "saturation_value": 0.35, "inflection_year": 8, "steepness": 0.6}
}
—--
MODE: MULTI_STAGE_FADE
Behavior: Allows defining distinct phases with different fade dynamics. Useful for complex trajectories (e.g., rapid expansion phase followed by gradual maturation, then terminal stability).
Required Params:
  - stages (array): Ordered list of stage definitions. Each stage:
    - end_year (int): Year at which this stage completes.
    - end_value (float): Value at completion of this stage.
    - interpolation (string, optional): "LINEAR" (default) or "CAGR". Method for this stage.
Mechanics:
  - Stages are processed sequentially.
  - Each stage starts from the end_value of the previous stage (or Y0 for the first stage).
  - Within each stage, values interpolate according to the specified method.
  - After the final stage, the last end_value is held constant through Y20.
Example:
{
  "mode": "MULTI_STAGE_FADE",
  "params": {
    "stages": [
      {"end_year": 5, "end_value": 0.30, "interpolation": "LINEAR"},
      {"end_year": 12, "end_value": 0.22, "interpolation": "LINEAR"},
      {"end_year": 20, "end_value": 0.18, "interpolation": "LINEAR"}
    ]
  }
}
—--
MODE: EXPLICIT_SCHEDULE
Behavior: Manually specifies values for designated years. Gaps are linearly interpolated. Years after the schedule hold the last specified value.
Required Params:
  - schedule (object): Dictionary mapping year numbers (as strings) to values.
Mechanics:
  - Specified years take the explicit value.
  - Gaps between specified years are linearly interpolated.
  - Years after the last specified year hold that final value.
Example:
{
  "mode": "EXPLICIT_SCHEDULE",
  "params": {
    "schedule": {
      "1": 0.25,
      "3": 0.22,
      "5": 0.20,
      "10": 0.18,
      "20": 0.15
    }
  }
}
B.3. Discount Rate Methodology
The Discount Rate is derived using a simplified model combining market parameters with a qualitative risk assessment.
Formula: DR = RFR + (ERP × X)
Components:
  - RFR (Risk-Free Rate): Proxy is the 10-Year US Treasury Yield at the valuation date.
  - ERP (Equity Risk Premium): Standardized at 5.0% per the G3 ERP Convention Mandate.
  - X (Risk Multiplier): Qualitative assessment of company-specific risk relative to market average.
Risk Multiplier (X) Specification:
  - Range: 0.5 to 2.2
  - Interpretation:
    - X = 1.0: Average market risk
    - X < 1.0: Below-average risk (stable, predictable, strong moat)
    - X > 1.0: Above-average risk (volatile, competitive, execution-dependent)
  - Derivation: Determined in BASE stage based on business model analysis, competitive position, and financial stability. ENRICHMENT has revision authority per P2 DR Revision Protocol if RQ evidence reveals material risk factors not assessable from BASE source documents.
B.4. Execution Topology (DAG Compliance)
The CVR Kernel executes the SCM using topological sort to respect causal dependencies.
DAG Rules:
1. PREV() Rule (Inter-Temporal): Access prior year value with PREV('Variable_Name').
   * Mandatory for stock variables and calculations requiring BOP values.
2. GET() Rule (Intra-Temporal): Access current year value (already calculated in this timestep) with GET('Variable_Name').
   * Requires acyclic dependencies within each timestep.
3. Cycle Prohibition: Circular dependencies within a single timestep are forbidden and will cause execution failure.
Equation Syntax:
  - Standard Python arithmetic operators: +, -, *, /, **
  - Functions: PREV('Var'), GET('Var'), MAX(a, b), MIN(a, b), ABS(x)
  - Constants: Direct numeric values
  - References: Variable names (resolved from current timestep calculation order)
B.5. Terminal Value and Economic Constraints
Terminal Value Derivation:
  - Method: Gordon Growth Model (Perpetuity with growth)
  - Formula: TV = FCF_Y21 / (DR - g_terminal)
  - Where: FCF_Y21 = FCF_Y20 × (1 + g_terminal)
Economic Governor Constraints:
  - g_terminal < DR: Mandatory. Violation causes Kernel failure.
  - g_terminal ≤ Long-term nominal GDP growth: Recommended (2-4% for developed markets).
  - Terminal ROIC: Should converge toward cost of capital unless durable competitive advantage is justified.
  - g = ROIC × RR: Must hold at terminal state.
Implied Constraint:
  - If g_terminal and RR_terminal are specified, ROIC_terminal is implied.
  - The model must be internally consistent. Conflicting terminal assumptions will produce implausible results flagged in the Post-Execution Reality Check.
B.6. ENRICHMENT-Specific Constraints Summary
The following constraints are specific to the ENRICHMENT stage:
| Artifact | Mutation Policy | Constraint |
|----------|-----------------|------------|
| A.1 EPISTEMIC_ANCHORS | Refinement Authorized | High burden of proof; requires superior third-party data |
| A.2 ANALYTIC_KG | Update Authorized | Document in A.9 kg_changelog |
| A.3 CAUSAL_DAG | Enrichment Authorized | Additive only; requires RQ evidence; document in A.9 dag_changelog |
| A.5 GESTALT_IMPACT_MAP | Update Required | Core refinement target |
| A.6 DR_DERIVATION_TRACE | Revision Authorized | High burden of proof; requires RQ evidence of material risk factors; document in A.9 dr_changelog |
| A.7 LIGHTWEIGHT_VALUATION_SUMMARY | Recalculated | Kernel output |
| A.9 ENRICHMENT_TRACE | Created | Full audit trail including dr_changelog |
Scenario Exclusion Mandate:
  - Discrete probabilistic scenarios (M-3) are reserved for SSE stage.
  - Exception: P=1.0 events (virtual certainty) must be incorporated into Base Case.
Economic Governor Mandate:
  - All refinements must maintain g < DR at terminal.
  - Implausible ROIC trajectories require explicit justification (Narrative N3).
—----------------------------
—-------------
APPENDIX C: CVR KERNEL G3_2.2.1e
# ==========================================================================================
# CVR KERNEL G3_2.2.1e_ENRICH (ENRICHMENT Implementation)
# Extended from G3_2.2.1e BASE with S_CURVE and MULTI_STAGE_FADE DSL support
# ==========================================================================================
import numpy as np
import pandas as pd
import json
import math
from collections import deque, defaultdict
import re
import copy
import logging
# ==========================================================================================
# CONFIGURATION
# ==========================================================================================
FORECAST_YEARS = 20
EPSILON = 1e-9
KERNEL_VERSION = "G3_2.2.1e_ENRICH"
SENSITIVITY_TORNADO_TOP_N = 5
TERMINAL_G_RFR_CAP = True  # If True, Terminal g is capped at RFR
# Configure Logging (Minimal for production)
logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# ==========================================================================================
# 1. CORE ENGINES (DSL, SCM, APV)
# ==========================================================================================
# ------------------------------------------------------------------------------
# 1.1 Assumption DSL (Domain Specific Language) Engine
# Extended with S_CURVE and MULTI_STAGE_FADE modes for ENRICHMENT
# ------------------------------------------------------------------------------
def apply_dsl(dsl, y0_value=None, forecast_years=FORECAST_YEARS):
    """
    Applies the DSL definition to generate a forecast array.
    
    Supported Modes:
    - STATIC: Constant value
    - LINEAR_FADE: Linear interpolation to target
    - CAGR_INTERP: Compounding growth rate that fades
    - S_CURVE: Logistic function for adoption/penetration dynamics
    - MULTI_STAGE_FADE: Multiple distinct phases with different targets
    - EXPLICIT_SCHEDULE: Manual year-by-year specification
    """
    mode = dsl.get('mode')
    params = dsl.get('params', {})
    forecast = np.zeros(forecast_years)
    # -------------------------------------------------------------------------
    # MODE: STATIC
    # -------------------------------------------------------------------------
    if mode == 'STATIC':
        value = float(params.get('value', 0))
        forecast.fill(value)
    # -------------------------------------------------------------------------
    # MODE: LINEAR_FADE
    # -------------------------------------------------------------------------
    elif mode == 'LINEAR_FADE':
        start_value = float(params.get('start_value', y0_value if y0_value is not None else 0))
        end_value = float(params.get('end_value'))
        fade_years = int(params.get('fade_years'))
        if fade_years > forecast_years:
            fade_years = forecast_years
        if fade_years > 0:
            fade_steps = np.linspace(start_value, end_value, fade_years)
            forecast[:fade_years] = fade_steps
        if fade_years < forecast_years:
            forecast[fade_years:] = end_value
    # -------------------------------------------------------------------------
    # MODE: CAGR_INTERP
    # -------------------------------------------------------------------------
    elif mode == 'CAGR_INTERP':
        if y0_value is None:
            raise ValueError("CAGR_INTERP requires a valid y0_value from ANALYTIC_KG.")
        start_cagr = float(params.get('start_cagr'))
        end_cagr = float(params.get('end_cagr'))
        interp_years = int(params.get('interp_years'))
        if interp_years > forecast_years:
            interp_years = forecast_years
        # Generate the CAGR time series (linear fade of growth rate)
        cagr_series = np.zeros(forecast_years)
        if interp_years > 0:
            cagr_steps = np.linspace(start_cagr, end_cagr, interp_years)
            cagr_series[:interp_years] = cagr_steps
        if interp_years < forecast_years:
            cagr_series[interp_years:] = end_cagr
        # Apply the CAGR series to compound from Y0
        current_value = y0_value
        for i in range(forecast_years):
            current_value *= (1 + cagr_series[i])
            forecast[i] = current_value
    # -------------------------------------------------------------------------
    # MODE: S_CURVE (Logistic Function) - NEW FOR ENRICHMENT
    # -------------------------------------------------------------------------
    elif mode == 'S_CURVE':
        start_value = float(params.get('start_value', y0_value if y0_value is not None else 0))
        saturation_value = float(params.get('saturation_value'))
        inflection_year = float(params.get('inflection_year'))
        steepness = float(params.get('steepness', 0.5))
        # Logistic function: value(t) = start + (saturation - start) / (1 + exp(-k*(t - t0)))
        # Where k = steepness, t0 = inflection_year
        
        for i in range(forecast_years):
            t = i + 1  # Year 1 to Year 20
            exponent = -steepness * (t - inflection_year)
            
            # Prevent overflow in exp
            if exponent > 700:
                logistic_factor = 0.0
            elif exponent < -700:
                logistic_factor = 1.0
            else:
                logistic_factor = 1.0 / (1.0 + math.exp(exponent))
            
            forecast[i] = start_value + (saturation_value - start_value) * logistic_factor
    # -------------------------------------------------------------------------
    # MODE: MULTI_STAGE_FADE - NEW FOR ENRICHMENT
    # -------------------------------------------------------------------------
    elif mode == 'MULTI_STAGE_FADE':
        stages = params.get('stages', [])
        
        if not stages:
            raise ValueError("MULTI_STAGE_FADE requires at least one stage definition.")
        
        # Sort stages by end_year
        stages = sorted(stages, key=lambda s: s['end_year'])
        
        # Determine starting value
        current_value = float(params.get('start_value', y0_value if y0_value is not None else 0))
        current_year = 0  # Start from Y0
        
        for stage in stages:
            end_year = int(stage['end_year'])
            end_value = float(stage['end_value'])
            interpolation = stage.get('interpolation', 'LINEAR').upper()
            
            # Clamp end_year to forecast horizon
            if end_year > forecast_years:
                end_year = forecast_years
            
            stage_years = end_year - current_year
            
            if stage_years <= 0:
                continue
            
            # Generate values for this stage
            if interpolation == 'LINEAR':
                stage_values = np.linspace(current_value, end_value, stage_years + 1)[1:]
            elif interpolation == 'CAGR':
                # Compound growth from current to end
                if current_value > 0 and end_value > 0:
                    stage_cagr = (end_value / current_value) ** (1 / stage_years) - 1
                    stage_values = np.array([
                        current_value * ((1 + stage_cagr) ** (j + 1))
                        for j in range(stage_years)
                    ])
                else:
                    # Fallback to linear if values are non-positive
                    stage_values = np.linspace(current_value, end_value, stage_years + 1)[1:]
            else:
                # Default to linear
                stage_values = np.linspace(current_value, end_value, stage_years + 1)[1:]
            
            # Fill forecast array
            start_idx = current_year
            end_idx = min(current_year + stage_years, forecast_years)
            forecast[start_idx:end_idx] = stage_values[:end_idx - start_idx]
            
            # Update for next stage
            current_value = end_value
            current_year = end_year
            
            if current_year >= forecast_years:
                break
        
        # Fill remaining years with last value
        if current_year < forecast_years:
            forecast[current_year:] = current_value
    # -------------------------------------------------------------------------
    # MODE: EXPLICIT_SCHEDULE
    # -------------------------------------------------------------------------
    elif mode == 'EXPLICIT_SCHEDULE':
        schedule = params.get('schedule', {})
        sorted_years = sorted([int(y) for y in schedule.keys()])
        if not sorted_years:
            return forecast
        # Initial fill before first specified year
        start_year = sorted_years[0]
        start_value = float(schedule[str(start_year)])
        if start_year > 1:
            forecast[:start_year - 1] = start_value
        # Process each specified year and interpolate gaps
        for i in range(len(sorted_years)):
            year = sorted_years[i]
            value = float(schedule[str(year)])
            idx = year - 1  # Convert to 0-indexed
            if idx < forecast_years:
                forecast[idx] = value
            # Interpolate to next specified year
            if i + 1 < len(sorted_years):
                next_year = sorted_years[i + 1]
                next_value = float(schedule[str(next_year)])
                next_idx = next_year - 1
                if next_year > year + 1:
                    gap_years = next_year - year
                    interp_steps = np.linspace(value, next_value, gap_years + 1)
                    start_fill_idx = idx + 1
                    end_fill_idx = min(next_idx, forecast_years)
                    if start_fill_idx < forecast_years:
                        fill_len = end_fill_idx - start_fill_idx
                        forecast[start_fill_idx:end_fill_idx] = interp_steps[1:1 + fill_len]
        # Hold last value through end of forecast
        last_defined_year = sorted_years[-1]
        if last_defined_year < forecast_years:
            last_value = float(schedule[str(last_defined_year)])
            forecast[last_defined_year:] = last_value
    # -------------------------------------------------------------------------
    # UNKNOWN MODE
    # -------------------------------------------------------------------------
    else:
        raise ValueError(f"Unknown DSL mode: {mode}. Supported: STATIC, LINEAR_FADE, CAGR_INTERP, S_CURVE, MULTI_STAGE_FADE, EXPLICIT_SCHEDULE")
    return forecast
# ------------------------------------------------------------------------------
# 1.2 SCM (Structural Causal Model) Engine
# ------------------------------------------------------------------------------
def topological_sort(dag):
    """
    Performs a topological sort on the DAG.
    Ensures only intra-timestep dependencies (GET calls) are considered for ordering.
    """
    in_degree = defaultdict(int)
    graph = defaultdict(list)
    nodes = set(dag.keys())
    # Regex to find GET('NodeName') calls (intra-timestep dependencies)
    get_regex = re.compile(r"GET\(['\"](.*?)['\"]\)")
    for node, definition in dag.items():
        # 1. Explicit dependencies from 'parents' list
        parents = definition.get('parents', [])
        for parent in parents:
            # Filter out PREV references in parent list
            if parent.startswith('PREV('):
                continue
            if parent in nodes and parent != node:
                if node not in graph[parent]:
                    graph[parent].append(node)
                    in_degree[node] += 1
        # 2. Implicit dependencies from 'equation' string (GET calls)
        equation = definition.get('equation', '')
        if equation:
            matches = get_regex.findall(equation)
            for dependency in matches:
                if dependency in nodes and dependency != node:
                    if node not in graph[dependency]:
                        graph[dependency].append(node)
                        in_degree[node] += 1
    # 3. Perform the sort (Kahn's algorithm)
    queue = deque([node for node in nodes if in_degree[node] == 0])
    sorted_list = []
    while queue:
        node = queue.popleft()
        sorted_list.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    if len(sorted_list) != len(nodes):
        cycle_nodes = [node for node in nodes if in_degree[node] > 0]
        raise RuntimeError(f"Cycle detected in DAG. Check nodes for circular dependencies (use PREV for lagged): {cycle_nodes}")
    return sorted_list
def validate_dag_coverage(kg, dag_artifact):
    """
    Validates that all Y0_data metrics are accounted for in the DAG (P5 Doctrine).
    Either they map to a node, are derivatives, or are explicitly excluded.
    """
    y0_data = kg.get('core_data', {}).get('Y0_data', {})
    dag = dag_artifact.get('DAG', {})
    coverage_manifest = dag_artifact.get('coverage_manifest', {}).get('Y0_data_coverage', {})
    
    dag_nodes = set(dag.keys())
    missing_metrics = []
    
    for metric in y0_data.keys():
        # Check if metric is in DAG
        if metric in dag_nodes:
            continue
        # Check if metric is documented in coverage manifest
        if metric in coverage_manifest:
            continue
        # Metric is unaccounted
        missing_metrics.append(metric)
    
    if missing_metrics:
        logger.warning(f"P5 Warning: Y0_data metrics not explicitly dispositioned in DAG: {missing_metrics}")
        # For ENRICHMENT, we issue a warning rather than failing
        # since DAG may have been enriched
def prepare_inputs(kg, gim):
    """Prepares inputs by applying the DSL to generate forecast arrays for exogenous drivers."""
    inputs = {}
    y0_data = kg.get('core_data', {}).get('Y0_data', {})
    for handle, definition in gim.items():
        y0_value = y0_data.get(handle)
        # CAGR_INTERP requires Y0 value
        if definition.get('mode') == 'CAGR_INTERP' and y0_value is None:
            logger.error(f"Missing Y0 data for handle '{handle}' required by CAGR_INTERP.")
            raise ValueError(f"Missing Y0 data for handle '{handle}' in ANALYTIC_KG.")
        try:
            forecast_array = apply_dsl(definition, y0_value=y0_value)
            inputs[handle] = forecast_array
        except Exception as e:
            logger.error(f"Error applying DSL for handle '{handle}': {e}")
            raise RuntimeError(f"Failed to process GIM assumption for {handle}. Error: {e}") from e
    return inputs
def execute_scm(kg, dag, seq, gim):
    """Executes the SCM forecast over the forecast horizon."""
    # 1. Initialize Data Structures
    y0_data = kg.get('core_data', {}).get('Y0_data', {})
    # 'history' stores the full time series data (Y0 + Y1...Y20)
    history = defaultdict(lambda: np.zeros(FORECAST_YEARS + 1))
    # Load Y0 data (at index 0)
    for handle, value in y0_data.items():
        if handle in dag:
            try:
                history[handle][0] = float(value)
            except (TypeError, ValueError):
                history[handle][0] = 0.0
    # 2. Prepare Exogenous Inputs (Apply DSL)
    try:
        exogenous_inputs = prepare_inputs(kg, gim)
    except Exception as e:
        logger.error(f"Failed to prepare exogenous inputs: {e}")
        raise
    # Load exogenous inputs (Y1...Y20)
    for handle, forecast_array in exogenous_inputs.items():
        if handle in dag:
            history[handle][1:] = forecast_array
    # 3. Define Helper Functions (PREV, GET) for use in equations
    def GET(handle, t):
        if handle not in history:
            raise NameError(f"Handle '{handle}' not found during SCM execution (GET).")
        return history[handle][t]
    def PREV(handle, t):
        if t <= 0:
            raise IndexError(f"Cannot access data before Y0 for handle '{handle}' (PREV at t=0).")
        if handle not in history:
            raise NameError(f"Handle '{handle}' not found during SCM execution (PREV).")
        return history[handle][t - 1]
    # 4. Execute the Forecast (Time-Step Iteration)
    for t in range(1, FORECAST_YEARS + 1):
        for handle in seq:
            definition = dag[handle]
            equation_str = definition.get('equation')
            if not equation_str:
                # Node is exogenous or static, already populated
                continue
            # Execute the equation
            try:
                exec_env = {
                    'GET': lambda h: GET(h, t),
                    'PREV': lambda h: PREV(h, t),
                    'MAX': max, 'MIN': min, 'ABS': abs,
                    'max': max, 'min': min, 'abs': abs,
                    'math': math, 'np': np
                }
                result = eval(equation_str, exec_env)
                history[handle][t] = float(result)
            except Exception as e:
                logger.error(f"SCM Execution Error at t={t} for handle '{handle}'. Equation: '{equation_str}'. Error: {e}")
                raise RuntimeError(f"Failed to execute equation for {handle} at year {t}. Error: {e}") from e
    # 5. Format Output as DataFrame (Y1...Y20)
    forecast_data = {handle: data[1:] for handle, data in history.items() if handle in seq}
    index = [f"Y{i + 1}" for i in range(FORECAST_YEARS)]
    df = pd.DataFrame(forecast_data, index=index)
    # Ensure columns are in topologically sorted order
    ordered_cols = [col for col in seq if col in df.columns]
    df = df[ordered_cols]
    return df
# ------------------------------------------------------------------------------
# 1.3 APV (Adjusted Present Value) Valuation Engine
# ------------------------------------------------------------------------------
def calculate_apv(forecast_df, dr, kg):
    """Calculates the Intrinsic Value Per Share (IVPS) using the APV methodology."""
    # 1. Validate Required Columns
    required_cols = ['FCF_Unlevered', 'ROIC', 'NOPAT']
    for col in required_cols:
        if col not in forecast_df.columns:
            raise ValueError(f"Forecast DataFrame must contain '{col}'.")
    fcf = forecast_df['FCF_Unlevered'].values
    nopat_T = forecast_df['NOPAT'].iloc[-1]
    # 2. Extract KG Data
    market_context = kg.get('market_context', {})
    share_data = kg.get('share_data', {})
    core_data = kg.get('core_data', {}).get('Y0_data', {})
    rfr = market_context.get('RFR')
    fdso = share_data.get('shares_out_diluted_tsm') or share_data.get('FDSO')
    
    # Capital structure for equity bridge
    capital_structure = kg.get('capital_structure', {}).get('net_debt_y0', {})
    if capital_structure:
        total_debt_y0 = capital_structure.get('gross_debt', 0.0)
        excess_cash_y0 = capital_structure.get('cash_equivalents', 0.0)
    else:
        total_debt_y0 = core_data.get('Total_Debt', 0.0)
        excess_cash_y0 = core_data.get('Excess_Cash', 0.0)
    
    minority_interest_y0 = core_data.get('Minority_Interest', 0.0)
    if fdso is None or fdso <= 0:
        raise ValueError("FDSO/shares_out_diluted_tsm must be provided and positive in ANALYTIC_KG.")
    # 3. Calculate PV of Explicit FCF
    discount_factors = np.array([(1 + dr) ** -(i + 1) for i in range(FORECAST_YEARS)])
    pv_fcf = np.sum(fcf * discount_factors)
    # 4. Determine Terminal Growth (g) and Terminal ROIC (r)
    roic_T = forecast_df['ROIC'].iloc[-1]
    terminal_roic_r = roic_T
    # Estimate terminal growth from NOPAT trajectory
    nopat_growth_rates = forecast_df['NOPAT'].pct_change().values[1:]
    terminal_g_estimate = np.mean(nopat_growth_rates[-3:])  # Average of last 3 years
    terminal_g = terminal_g_estimate
    # Apply Constraints
    if TERMINAL_G_RFR_CAP and rfr is not None:
        if terminal_g > rfr:
            logger.info(f"Capping terminal growth ({terminal_g:.4f}) at RFR ({rfr:.4f}).")
            terminal_g = rfr
    if terminal_g >= dr:
        logger.warning(f"Terminal growth ({terminal_g:.4f}) >= DR ({dr:.4f}). Adjusting g to 99% of DR.")
        terminal_g = dr * 0.99
    if terminal_g < 0:
        terminal_g = 0
    # 5. Calculate Terminal Value (Value Driver Formula)
    nopat_T_plus_1 = nopat_T * (1 + terminal_g)
    if abs(terminal_roic_r) > EPSILON:
        reinvestment_rate_terminal = terminal_g / terminal_roic_r
    else:
        reinvestment_rate_terminal = 0
    if reinvestment_rate_terminal < 0:
        logger.warning("Terminal Reinvestment Rate is negative. Assuming g=0.")
        terminal_g = 0
        reinvestment_rate_terminal = 0
        nopat_T_plus_1 = nopat_T
    numerator = nopat_T_plus_1 * (1 - reinvestment_rate_terminal)
    denominator = dr - terminal_g
    if denominator <= 0:
        raise RuntimeError(f"APV denominator (DR - g) is non-positive. DR={dr}, g={terminal_g}")
    terminal_value = numerator / denominator
    # 6. Calculate PV of Terminal Value
    pv_terminal_value = terminal_value / ((1 + dr) ** FORECAST_YEARS)
    # 7. Calculate Enterprise Value
    enterprise_value = pv_fcf + pv_terminal_value
    # 8. Calculate Equity Value
    net_debt = total_debt_y0 - excess_cash_y0
    equity_value = enterprise_value - net_debt - minority_interest_y0
    # 9. Calculate IVPS
    ivps = equity_value / fdso
    # 10. Package Results
    results = {
        "IVPS": ivps,
        "Equity_Value": equity_value,
        "Enterprise_Value": enterprise_value,
        "DR": dr,
        "Terminal_g": terminal_g,
        "Terminal_ROIC_r": terminal_roic_r,
        "Terminal_RR": reinvestment_rate_terminal,
        "FDSO": fdso,
        "Net_Debt": net_debt,
        "PV_Explicit_FCF": pv_fcf,
        "PV_Terminal_Value": pv_terminal_value
    }
    return results
# ==========================================================================================
# 2. INTERNAL ARTIFACT GENERATORS
# ==========================================================================================
def generate_forecast_summary(forecast_df, schema_version=KERNEL_VERSION):
    """Generates a summary of the forecast for internal analysis."""
    summary_data = {}
    key_items = ['Revenue', 'EBIT', 'NOPAT', 'ROIC', 'FCF_Unlevered', 'Invested_Capital']
    for item in key_items:
        if item in forecast_df.columns:
            summary_data[item] = forecast_df[item].to_dict()
    if 'Revenue' in forecast_df.columns and 'EBIT' in forecast_df.columns:
        summary_data['EBIT_Margin'] = (forecast_df['EBIT'] / forecast_df['Revenue']).to_dict()
    return {"schema_version": schema_version, "summary_data": summary_data}
# ==========================================================================================
# 3. ANALYSIS MODULES (Multiples, Sensitivity)
# ==========================================================================================
def calculate_implied_multiples(valuation_results, forecast_summary, kg, schema_version=KERNEL_VERSION):
    """Calculates implied valuation multiples based on the IVPS and market price."""
    ivps = valuation_results['IVPS']
    ev_implied = valuation_results['Enterprise_Value']
    fdso = valuation_results['FDSO']
    net_debt = valuation_results['Net_Debt']
    current_price = kg.get('market_context', {}).get('Current_Stock_Price')
    ev_market = None
    if current_price is not None:
        market_cap = current_price * fdso
        ev_market = market_cap + net_debt
    fs = forecast_summary.get('summary_data', {})
    implied_multiples = {}
    year = 'Y1'
    def calculate(num_implied, num_market, den_data, handle):
        if den_data and abs(den_data.get(year, 0)) > EPSILON:
            implied_multiples[f"Implied_{handle}_{year}"] = num_implied / den_data[year]
            if num_market is not None:
                implied_multiples[f"Market_{handle}_{year}"] = num_market / den_data[year]
    calculate(ev_implied, ev_market, fs.get('Revenue'), 'EV_Sales')
    calculate(ev_implied, ev_market, fs.get('EBIT'), 'EV_EBIT')
    calculate(ivps * fdso, (current_price * fdso) if current_price else None, fs.get('NOPAT'), 'P_NOPAT')
    return {
        "schema_version": schema_version,
        "current_market_price": current_price,
        "implied_multiples": implied_multiples
    }
def run_sensitivity_analysis(kg, dag, seq, gim, dr, base_results, scenarios, schema_version=KERNEL_VERSION):
    """
    Runs sensitivity analysis (Tornado chart) by modifying GIM assumptions or DR.
    Extended for S_CURVE and MULTI_STAGE_FADE modes.
    """
    base_ivps = base_results['IVPS']
    tornado_data = []
    for scenario in scenarios:
        driver = scenario['driver']
        low_change = scenario['low']
        high_change = scenario['high']
        ivps_low = None
        ivps_high = None
        for direction, pct_change in [('low', low_change), ('high', high_change)]:
            temp_gim = copy.deepcopy(gim)
            temp_dr = dr
            try:
                # Modify the input
                if driver == 'Discount_Rate':
                    temp_dr += pct_change
                    if temp_dr <= 0.01:
                        raise ValueError("Discount Rate too low.")
                elif driver in temp_gim:
                    mode = temp_gim[driver].get('mode')
                    params = temp_gim[driver].get('params', {})
                    def apply_change(value, change):
                        return value * (1 + change)
                    # Apply percentage change based on mode
                    if mode == 'STATIC':
                        params['value'] = apply_change(params['value'], pct_change)
                    
                    elif mode == 'LINEAR_FADE':
                        if 'start_value' in params:
                            params['start_value'] = apply_change(params['start_value'], pct_change)
                        params['end_value'] = apply_change(params['end_value'], pct_change)
                    
                    elif mode == 'CAGR_INTERP':
                        params['start_cagr'] = apply_change(params['start_cagr'], pct_change)
                        params['end_cagr'] = apply_change(params['end_cagr'], pct_change)
                    
                    elif mode == 'S_CURVE':
                        # Adjust the saturation value (the target ceiling/floor)
                        params['saturation_value'] = apply_change(params['saturation_value'], pct_change)
                    
                    elif mode == 'MULTI_STAGE_FADE':
                        # Adjust all stage end_values proportionally
                        if 'stages' in params:
                            for stage in params['stages']:
                                stage['end_value'] = apply_change(stage['end_value'], pct_change)
                    
                    elif mode == 'EXPLICIT_SCHEDULE':
                        # Adjust all scheduled values
                        if 'schedule' in params:
                            for year_key in params['schedule']:
                                params['schedule'][year_key] = apply_change(
                                    params['schedule'][year_key], pct_change
                                )
                    
                    temp_gim[driver]['params'] = params
                else:
                    # Driver not found in GIM
                    continue
                # Re-run the SCM and APV
                forecast_df = execute_scm(kg, dag, seq, temp_gim)
                valuation_results = calculate_apv(forecast_df, temp_dr, kg)
                scenario_ivps = valuation_results['IVPS']
                if direction == 'low':
                    ivps_low = scenario_ivps
                else:
                    ivps_high = scenario_ivps
            except Exception as e:
                logger.warning(f"Sensitivity analysis error for {driver} ({direction}): {e}")
        # Append to tornado data if both scenarios succeeded
        if ivps_low is not None and ivps_high is not None:
            # Ensure proper ordering (low input -> low IVPS for most drivers)
            if ivps_low > ivps_high:
                ivps_low, ivps_high = ivps_high, ivps_low
            tornado_data.append({
                "Driver": driver,
                "IVPS_Low": ivps_low,
                "IVPS_High": ivps_high,
                "Impact": ivps_high - ivps_low
            })
    # Sort by impact magnitude
    tornado_data.sort(key=lambda x: abs(x['Impact']), reverse=True)
    return {
        "schema_version": schema_version,
        "base_case_ivps": base_ivps,
        "Tornado_Chart_Data": tornado_data
    }
# ==========================================================================================
# 4. LIGHTWEIGHT SUMMARY GENERATOR (The Selective Emission Artifact)
# ==========================================================================================
def generate_lightweight_valuation_summary(
    valuation_results, 
    forecast_summary, 
    implied_multiples, 
    sensitivity_results, 
    kg, 
    forecast_df, 
    gim, 
    schema_version=KERNEL_VERSION
):
    """Generates the LIGHTWEIGHT_VALUATION_SUMMARY (A.7) artifact."""
    
    v = valuation_results
    fs = forecast_summary.get('summary_data', {})
    im = implied_multiples.get('implied_multiples', {})
    sr = sensitivity_results
    def safe_float(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return None
    # 1. IVPS Summary
    ivps_summary = {
        "IVPS": safe_float(v.get("IVPS")),
        "DR": safe_float(v.get("DR")),
        "Terminal_g": safe_float(v.get("Terminal_g")),
        "ROIC_Terminal": safe_float(v.get("Terminal_ROIC_r")),
        "Current_Market_Price": safe_float(implied_multiples.get("current_market_price"))
    }
    # 2. Implied Multiples Analysis
    implied_multiples_analysis = {
        "Implied_EV_Sales_Y1": im.get("Implied_EV_Sales_Y1"),
        "Implied_EV_EBIT_Y1": im.get("Implied_EV_EBIT_Y1"),
        "Implied_P_NOPAT_Y1": im.get("Implied_P_NOPAT_Y1"),
        "Market_EV_Sales_Y1": im.get("Market_EV_Sales_Y1"),
        "Market_EV_EBIT_Y1": im.get("Market_EV_EBIT_Y1"),
        "Market_P_NOPAT_Y1": im.get("Market_P_NOPAT_Y1")
    }
    # 3. Sensitivity Analysis (Tornado Summary)
    tornado_data = sr.get('Tornado_Chart_Data', []) if sr else []
    tornado_summary = []
    base_ivps = safe_float(sr.get('base_case_ivps')) if sr else ivps_summary["IVPS"]
    for item in tornado_data[:SENSITIVITY_TORNADO_TOP_N]:
        swing_percent = None
        ivps_low = safe_float(item.get("IVPS_Low"))
        ivps_high = safe_float(item.get("IVPS_High"))
        if base_ivps and abs(base_ivps) > EPSILON and ivps_low is not None and ivps_high is not None:
            swing_percent = (ivps_high - ivps_low) / base_ivps
        tornado_summary.append({
            "Driver_Handle": item.get("Driver"),
            "IVPS_Low": ivps_low,
            "IVPS_High": ivps_high,
            "IVPS_Swing_Percent": swing_percent
        })
    tornado_summary.sort(key=lambda x: abs(x.get("IVPS_Swing_Percent") or 0), reverse=True)
    # 4. Key Forecast Metrics
    revenue_cagr_y1_y5 = None
    if 'Revenue' in forecast_df.columns and len(forecast_df) >= 5:
        try:
            y0_revenue = kg.get('core_data', {}).get('Y0_data', {}).get('Revenue')
            if y0_revenue is not None and y0_revenue > 0:
                y5_revenue = forecast_df['Revenue'].iloc[4]
                revenue_cagr_y1_y5 = (y5_revenue / y0_revenue) ** (1 / 5) - 1
        except Exception as e:
            logger.warning(f"Could not calculate Revenue CAGR Y1-Y5: {e}")
    ebit_margin_y5 = None
    if 'EBIT' in forecast_df.columns and 'Revenue' in forecast_df.columns and len(forecast_df) >= 5:
        rev_y5 = forecast_df['Revenue'].iloc[4]
        if abs(rev_y5) > EPSILON:
            ebit_margin_y5 = forecast_df['EBIT'].iloc[4] / rev_y5
    roic_y5 = None
    if 'ROIC' in forecast_df.columns and len(forecast_df) >= 5:
        roic_y5 = forecast_df['ROIC'].iloc[4]
    key_forecast_metrics = {
        "Revenue_CAGR_Y1_Y5": safe_float(revenue_cagr_y1_y5),
        "EBIT_Margin_Y5": safe_float(ebit_margin_y5),
        "ROIC_Y5": safe_float(roic_y5)
    }
    # 5. Terminal Driver Values
    terminal_drivers = {
        "Terminal_ROIC": safe_float(v.get("Terminal_ROIC_r")),
        "Terminal_RR": safe_float(v.get("Terminal_RR")),
        "Terminal_g": safe_float(v.get("Terminal_g"))
    }
    
    # Add GIM driver terminal values
    if gim and not forecast_df.empty:
        for driver in gim.keys():
            if driver in forecast_df.columns:
                terminal_drivers[driver] = safe_float(forecast_df[driver].iloc[-1])
    # 6. Forecast Trajectory Checkpoints
    trajectory_checkpoints = {"Y0": {}, "Y5": {}, "Y10": {}, "Y20": {}}
    y0_data = kg.get('core_data', {}).get('Y0_data', {})
    exogenous_drivers = list(gim.keys()) if gim else []
    key_internal_drivers = ['Revenue', 'EBIT', 'NOPAT', 'Invested_Capital', 'ROIC', 'FCF_Unlevered']
    # Add additional tracked drivers from forecast
    for driver in forecast_df.columns:
        if driver not in exogenous_drivers and driver not in key_internal_drivers:
            if driver in y0_data or len(key_internal_drivers) < 15:
                if driver not in key_internal_drivers:
                    key_internal_drivers.append(driver)
    all_drivers_to_track = exogenous_drivers + key_internal_drivers
    for driver in all_drivers_to_track:
        # Y0
        if driver in y0_data:
            trajectory_checkpoints["Y0"][driver] = safe_float(y0_data[driver])
        # Forecast Years
        if driver in forecast_df.columns:
            if len(forecast_df) >= 5:
                trajectory_checkpoints["Y5"][driver] = safe_float(forecast_df[driver].iloc[4])
            if len(forecast_df) >= 10:
                trajectory_checkpoints["Y10"][driver] = safe_float(forecast_df[driver].iloc[9])
            if len(forecast_df) >= 20:
                trajectory_checkpoints["Y20"][driver] = safe_float(forecast_df[driver].iloc[-1])
    return {
        "schema_version": schema_version,
        "ivps_summary": ivps_summary,
        "implied_multiples_analysis": implied_multiples_analysis,
        "sensitivity_analysis": {
            "tornado_summary": tornado_summary
        },
        "key_forecast_metrics": key_forecast_metrics,
        "terminal_drivers": terminal_drivers,
        "forecast_trajectory_checkpoints": trajectory_checkpoints
    }
# ==========================================================================================
# 5. WORKFLOW ORCHESTRATOR (Main API)
# ==========================================================================================
def execute_cvr_workflow(kg, dag_artifact, gim_artifact, dr_trace, sensitivity_scenarios=None):
    """
    The main API for the CVR Kernel G3_2.2E (ENRICHMENT).
    Implements Selective Emission: Returns ONLY the LightweightValuationSummary (A.7).
    
    Parameters:
    -----------
    kg : dict
        A.2_ANALYTIC_KG artifact
    dag_artifact : dict
        A.3_CAUSAL_DAG artifact (with 'DAG' key containing node definitions)
    gim_artifact : dict
        A.5_GESTALT_IMPACT_MAP artifact (with 'GIM' key containing driver assumptions)
    dr_trace : dict
        A.6_DR_DERIVATION_TRACE artifact
    sensitivity_scenarios : list, optional
        List of sensitivity scenario definitions: [{'driver': str, 'low': float, 'high': float}]
    
    Returns:
    --------
    dict
        A.7_LIGHTWEIGHT_VALUATION_SUMMARY artifact
    """
    print(f"CVR Kernel Execution Started (Version: {KERNEL_VERSION})... [ENRICHMENT Mode]")
    schema_version = KERNEL_VERSION
    # Extract structures from artifacts
    dag = dag_artifact.get('DAG', {})
    gim = gim_artifact.get('GIM', {})
    # 0.5 Validate DAG Coverage (P5 - Warning only for ENRICHMENT)
    print("Validating DAG coverage against Y0_data (P5 Doctrine)...")
    try:
        validate_dag_coverage(kg, dag_artifact)
    except Exception as e:
        logger.warning(f"DAG Coverage Validation Warning: {e}")
    # 1. Derive Execution Sequence (Topological Sort)
    print("Deriving SCM execution sequence...")
    try:
        seq = topological_sort(dag)
    except Exception as e:
        logger.error(f"Topological Sort Failed: {e}")
        raise
    # 2. Extract DR from trace
    try:
        dr_data = dr_trace.get('derivation_trace', {})
        dr = float(dr_data.get('DR_Static'))
    except (KeyError, TypeError, ValueError) as e:
        raise RuntimeError(f"Failed to parse DR from DR_DERIVATION_TRACE: {e}")
    # 3. Execute SCM Forecast
    print(f"Executing {FORECAST_YEARS}-Year SCM Forecast...")
    try:
        forecast_df = execute_scm(kg, dag, seq, gim)
    except Exception as e:
        logger.error(f"SCM Execution Failed: {e}")
        raise
    # 4. Execute APV Valuation
    print("Executing APV Valuation...")
    try:
        valuation_results = calculate_apv(forecast_df, dr, kg)
    except Exception as e:
        logger.error(f"APV Valuation Failed: {e}")
        raise
    # 5. Generate Internal Artifacts
    print("Generating Internal Summary Artifacts...")
    try:
        forecast_summary = generate_forecast_summary(forecast_df, schema_version)
    except Exception as e:
        logger.error(f"Forecast Summary Generation Failed: {e}")
        raise
    # 6. Calculate Implied Multiples
    print("Calculating Implied Multiples Analysis...")
    try:
        implied_multiples = calculate_implied_multiples(
            valuation_results, forecast_summary, kg, schema_version
        )
    except Exception as e:
        logger.warning(f"Implied Multiples Analysis Failed: {e}")
        implied_multiples = {"implied_multiples": {}}
    # 7. Execute Sensitivity Analysis
    sensitivity_results = {}
    if sensitivity_scenarios:
        print("Executing Sensitivity Analysis...")
        try:
            sensitivity_results = run_sensitivity_analysis(
                kg, dag, seq, gim, dr, valuation_results, sensitivity_scenarios, schema_version
            )
        except Exception as e:
            logger.warning(f"Sensitivity Analysis Failed: {e}")
            sensitivity_results = {"Tornado_Chart_Data": []}
    # 8. Generate Lightweight Summary (The Selective Emission)
    print("Generating Lightweight Valuation Summary (A.7)...")
    try:
        lightweight_summary = generate_lightweight_valuation_summary(
            valuation_results,
            forecast_summary,
            implied_multiples,
            sensitivity_results,
            kg,
            forecast_df,
            gim,
            schema_version
        )
    except Exception as e:
        logger.error(f"Lightweight Summary Generation Failed: {e}")
        raise
    print("CVR Kernel Execution Completed.")
    return lightweight_summary
# ==========================================================================================
# END OF CVR KERNEL G3_2.2.1e_ENRICH
# ==========================================================================================