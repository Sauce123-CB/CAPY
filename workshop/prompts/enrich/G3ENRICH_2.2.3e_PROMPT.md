# G3ENRICH 2.2.3e: Bayesian Causal Synthesis

> **Version:** 2.2.3e (Atomized)
> **Change from 2.2.2e:** Atomized output mandate, DR global calibration, terminal g from topline
> **Patch:** PATCH-2024-12-22-001

## I. MISSION AND OBJECTIVES

* Mission: Execute the ENRICHMENT stage (G3_2.2.3e) of the CAPY Pipeline for {Company Name} ({EXCHANGE:TICKER}) as of {DATE}.
* Primary Objective: To synthesize deep research (RQ Outputs), refine the Base Case assumptions (GIM) using a rigorous Bayesian Update protocol, and recalculate the valuation, transitioning from MRC State 1 to MRC State 2.
* Execution Paradigm: Guided Autonomy and Bayesian Synthesis. This stage requires high-level reasoning to interpret research, resolve conflicting evidence, translate insights into precise quantitative adjustments, and maintain epistemic rigor through explicit anchoring and variance justification.

## I.A EXECUTION PROTOCOL (Two-Shot Architecture)

### Turn Structure

This prompt governs a two-turn execution cycle. Each turn executes in a fresh Claude instance with clean context, maximizing reasoning depth through separation of concerns.

**Turn 1: Analytical Synthesis**

Trigger: "Do Turn 1: ENRICHMENT for {Company Name}, {EXCHANGE:TICKER}"

Attachments Required:
- G3ENRICH_2.2.3e_PROMPT.md (this file)
- G3ENRICH_2.2.3e_SCHEMAS.md
- G3ENRICH_2.2.3e_NORMDEFS.md
- BASE State 1 artifacts: All files from 03_T2/ folder with _BASE suffix
- RQ artifacts: A.8, A.9, RQ1-RQ7 from 04_RQ/ folder
- CVR_KERNEL_ENRICH_2.2.3e.py (reference context only)

Scope: Execute Phases A-D. Produce atomized narratives (N1-N5) and artifacts A.1-A.6, A.9. Write each as individual file.

Output: Atomized files per Section V. Write 12 individual files (5 narratives + 7 artifacts) using the Write tool.

Exclusion: Do NOT execute Kernel. Kernel is provided for semantic alignment only.

**Turn 2: Validation & Execution**

Trigger: "Do Turn 2"

Attachments Required:
- G3ENRICH_2.2.3e_PROMPT.md (this file)
- G3ENRICH_2.2.3e_SCHEMAS.md
- G3ENRICH_2.2.3e_NORMDEFS.md
- Turn 1 artifacts: All 12 files from 05_ENRICH/ folder
- CVR_KERNEL_ENRICH_2.2.3e.py

Scope: Validate Turn 1 artifacts for JSON integrity and internal consistency, repair if needed, execute kernel via Bash, write A.7 to disk.

Output: A.7 valuation artifact + kernel receipt. See Section V for filenames.

### Rationale

The two-shot architecture provides:
- Reasoning Depth: Turn 1 focuses purely on Bayesian synthesis without computational overhead.
- Error Correction: Turn 2 operates as a validation layer, catching JSON malformation and logical inconsistencies before kernel execution.
- Clean Context: Fresh instances prevent context pollution and attention degradation.

## II. EXECUTION ENVIRONMENT AND CONSTRAINTS

### A. Environmental Awareness and Tools

* Mandatory Inputs:
   1. MRC State 1 (BASE Output): The 6 artifacts (A.1, A.2, A.3, A.5, A.6, A.7) produced by G3BASE 2.2.2e.
   2. A.8_RESEARCH_STRATEGY_MAP: The targeted research plan from RQ_GEN 2.2.3, containing Uncertainty_Nexus_Analysis and Research_Plan.
   3. RQ Outputs (1-7): The research reports produced by the RQ execution stage, organized by Coverage_Objective (M-1/M-2/M-3a/M-3b/D-1/D-2/D-3).
* The Verification Doctrine (Externalized Schemas): The required output schemas are provided in the attached G3ENRICH_2.2.2e_SCHEMAS.md. The A.9_ENRICHMENT_TRACE schema is new to this stage.
* The CVR Kernel (Context Reference): The CVR Kernel (attached as CVR_KERNEL_ENRICH_2.2.2e.py) defines the computational logic that Turn 2 will execute. It is provided in Turn 1 for CONTEXTUAL UNDERSTANDING ONLY—to ensure your artifacts are semantically aligned with kernel expectations (DSL modes, node naming, equation syntax). Do NOT attempt to execute this code in Turn 1.
* Search Policy: Minimize search. ENRICHMENT focuses on synthesizing provided inputs. Ad-hoc search is permitted ONLY for clarifying specific data points explicitly referenced within the RQ Outputs or for validating critical factual claims where ambiguity remains high after synthesis.
* Emission Policy: The output must ONLY contain analytical narratives and artifacts. Reprinting instructions, schemas, or the CVR Kernel code is strictly forbidden.

### B. Two-Shot Execution Architecture (Critical)

This prompt operates in TWO-SHOT EXECUTION mode with strict separation of concerns:

**TURN 1 RESPONSIBILITY (Analytical Instance):**
- Synthesize RQ evidence using Bayesian Update Protocol
- Construct refined analytical artifacts (A.1–A.6, A.9) with full epistemic rigor
- Produce unified narratives (N1-N5)
- Emit artifacts as valid JSON in a single fenced code block
- Ensure structural compatibility with kernel requirements
- Do NOT execute kernel code or compute A.7

**TURN 2 RESPONSIBILITY (Validation & Execution Instance):**
- Validate JSON integrity and repair malformation if present
- Verify internal consistency (DAG coverage, GIM-KG alignment, DR consistency)
- Execute kernel using validated artifacts as input
- Generate A.7 (LightweightValuationSummary)
- Emit unified MRC State 2 report

This architecture leverages Turn 1's strengths (deep reasoning, Bayesian synthesis, evidence integration) while Turn 2 provides a validation layer and deterministic computation.

### C. The Efficiency Protocol (No State Reconstruction)

* Mandate: Do NOT execute the Kernel to reconstruct State 1. Trust the input artifacts from BASE.
* Action: Extract the State 1 baseline (IVPS, DR, Terminal g, key metrics) directly from the input A.7_LIGHTWEIGHT_VALUATION_SUMMARY. This establishes the computational baseline for comparison without redundant execution.
* Rationale: The MRC paradigm guarantees deterministic reconstruction. Re-execution would consume substantial resources without analytical benefit.

## III. CORE ANALYTICAL DIRECTIVES

### P1. Analytical Autonomy and Deep Synthesis (The Synthesis Mandate)

ENRICHMENT is fundamentally an evidence integration task. You must synthesize diverse, potentially conflicting research into a coherent analytical update.

* The Conflict Resolution Protocol:
   * Source Credibility Assessment: Evaluate the provenance, methodology, and potential biases of each RQ source. Primary data and audited figures take precedence over secondary commentary.
   * Reconciliation Before Rejection: Attempt to reconcile conflicting data through reasoning (e.g., different time periods, different definitions, different market segments) before defaulting to one source.
   * Ambiguity Handling: When ambiguity remains high after good-faith reconciliation, apply conservative judgment. Document the uncertainty explicitly in A.9.
   * The Anti-Narrative Mandate: Do not force-fit research findings into a pre-existing thesis. Allow the evidence to update your priors, even when this creates tension with the BASE narrative.
* The Holistic Integration Mandate: RQs are not independent inputs. You must identify cross-cutting themes, corroborating evidence, and contradictions across the full RQ set before making refinement decisions.

### P2. Structural Constraints (Pipeline Stability)

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

### P3. Epistemic Anchoring (The Bayesian Update Protocol)

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

### P4. Causal Chain Transparency (The Trace)

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

## IV. EXECUTION PROTOCOL (The Workflow)

Execute the workflow (Phases A-E), integrating the Core Analytical Directives throughout. Synthesize narratives internally during the respective phases for the final unified emission.

### A. Initialization and Baseline Confirmation (Phase A)

1. Ingestion: Ingest and parse MRC State 1 (A.1, A.2, A.3, A.5, A.6, A.7) and RQ Outputs (1-7).

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

### B. Research Synthesis and Interpretation (Phase B)

1. Holistic Synthesis (P1):
   * Analyze all RQs (1-7) comprehensively before making any refinement decisions.
   * Identify overarching themes, corroborating patterns, and critical tensions.
   * Execute the Conflict Resolution Protocol for any contradictory findings.

2. RQ-Specific Analysis (by Coverage Objective):
   * Integrity and Adversarial Review (M-1, M-2):
      - Synthesize findings from the Integrity Check (M-1) and Adversarial Synthesis (M-2).
      - Assess impact on the overall investment thesis and risk profile.
      - If M-1/M-2 findings reveal material risk factors: Evaluate DR revision per P2 DR Revision Protocol.
   * Scenario Boundary Check (M-3a, M-3b):
      - Review the Mainline Scenarios (M-3a) and Tail Risk Scenarios (M-3b) for discrete scenario evidence.
      - M-3a provides base case refinement evidence from historical analogues.
      - M-3b provides tail risk context that may inform DR or stress testing.
      - Apply the Scenario Exclusion Mandate and P=1.0 Certainty Exception as appropriate.
   * Dynamic Allocation Evidence (D-1, D-2, D-3):
      - Synthesize Lynchpin fact-finding and contextual evidence from dynamically allocated RQs.
      - These provide the primary evidence base for GIM refinement.
      - Cross-reference RQ_ID to Coverage_Objective via A.8_RESEARCH_STRATEGY_MAP.Research_Plan.

### C. Bayesian Refinement and Causal Tracing (Phase C — The Core Analysis)

Iterate through the assumptions, executing the Bayesian Update Protocol and documenting the Causal Chain.

1. Prioritized Iteration:
   * Begin with Lynchpins from A.8_RESEARCH_STRATEGY_MAP.Uncertainty_Nexus_Analysis (inherited from RQ stage).
   * Then systematically review remaining exogenous drivers in A.5_GESTALT_IMPACT_MAP.

2. For Each Driver, Execute the Protocol (P3/P4):
   a. State the Prior: Document the BASE assumption (DSL parameters) and the relevant A.1 Anchor (Base Rate distribution).
   b. Synthesize Evidence: Compile relevant findings from across the RQs. Apply Conflict Resolution if needed.
   c. Update the Posterior: Determine the refined assumption. Apply the Variance Mandate if deviating from the Anchor.
   d. Decision: Record MODIFY or CONFIRM.
   e. If MODIFY: Specify the updated DSL (mode and parameters). Utilize the Expanded DSL (see G3ENRICH_2.2.2e_NORMDEFS.md), including S_CURVE or MULTI_STAGE_FADE, if necessary to model the refined trajectory.
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

### D. Narrative Synthesis (Phase D)

Synthesize unified State 2 narratives for the final emission. ENRICHMENT inherits BASE narratives N1-N4 and produces updated State 2 versions, plus a new N5 synthesizing ENRICHMENT's analytical contribution.

**Narrative Unification Protocol**

For inherited narratives (N1-N4):
- If RQ evidence warrants material update: Rewrite section integrating new evidence
- If no material change: Passthrough with brief "[State 2: Confirmed, no material change from BASE]" annotation

**N1. Investment Thesis (State 2)**
Inherit BASE N1. Update where RQ evidence shifts thesis view—risks, catalysts, moat assessment, competitive position. Absorb executive synthesis framing (key RQ insights, aggregate thesis impact).

**N2. Invested Capital Modeling (State 2)**
Inherit BASE N2. Update only if DAG enrichment changed IC structure (rare).

**N3. Economic Governor & Constraints (State 2)**
Inherit BASE N3. Update if terminal constraints shifted materially due to GIM refinements. Incorporate extraordinary claims justification here if terminal assumptions exceed A.1 p90 or fall below p10.

**N4. Risk Assessment & DR Derivation (State 2)**
Inherit BASE N4. Mandatory update if DR revised per P2 DR Revision Protocol. Optional annotation if risk view shifted but DR held stable.

**N5. Enrichment Synthesis (NEW)**
ENRICHMENT's novel analytical contribution. Contains:
- Key Refinement Analysis: Detailed narratives on 2-4 most significant refinements (ordered by expected IVPS impact). Each traces full Causal Chain: Evidence → Interpretation → Anchor Reconciliation → Assumption Change → Valuation Impact.
- Valuation Bridge: Quantified State 1 → State 2 attribution. Tabular format preferred:
  | Driver | Prior Contribution | Posterior Contribution | Δ IVPS |
  |--------|-------------------|----------------------|--------|
- Cross-Cutting Themes: Patterns identified across RQ synthesis.
- DR Attribution (if applicable): Separate line item for IVPS change from DR revision vs. GIM refinements.

### E. Computational Execution and Emission (Phase E — State 2)

1. CVR Kernel Loading (P7):
   * Load the CVR Kernel G3_2.2.2e (attached as CVR_KERNEL_ENRICH_2.2.2e.py) into the execution environment.

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

## V. OUTPUT MANDATE (Atomized Artifact Emission)

*This section governs Turn 1 output. Turn 2 adds A.7 via kernel execution.*

### CRITICAL: Atomized Output (Pattern 12)

**DO NOT emit a single consolidated markdown file with embedded JSON.**

Each artifact and narrative MUST be written as an **individual file** using the Write tool. This prevents truncation and ensures downstream stages receive complete inputs.

### Turn 1 Required Outputs (12 files)

Write each file individually to the 05_ENRICH/ folder:

**Narratives (5 files):**
| File | Content |
|------|---------|
| `{TICKER}_N1_THESIS_ENRICH.md` | Updated investment thesis |
| `{TICKER}_N2_IC_ENRICH.md` | Updated IC modeling |
| `{TICKER}_N3_ECON_GOV_ENRICH.md` | Updated economic governor |
| `{TICKER}_N4_RISK_ENRICH.md` | Updated risk assessment |
| `{TICKER}_N5_ENRICHMENT_ENRICH.md` | NEW: Enrichment synthesis narrative |

**Artifacts (7 files):**
| File | Content |
|------|---------|
| `{TICKER}_A1_EPISTEMIC_ANCHORS_ENRICH.json` | Updated anchors (may be unchanged) |
| `{TICKER}_A2_ANALYTIC_KG_ENRICH.json` | Updated KG with research insights |
| `{TICKER}_A3_CAUSAL_DAG_ENRICH.json` | Updated DAG (if expanded) |
| `{TICKER}_A5_GIM_ENRICH.json` | Updated GIM with Bayesian adjustments |
| `{TICKER}_A6_DR_ENRICH.json` | Updated DR (if revised per P2) |
| `{TICKER}_A9_ENRICHMENT_TRACE_ENRICH.json` | NEW: Enrichment audit trail |

**Human Audit File (optional):**
| File | Content |
|------|---------|
| `{TICKER}_ENRICH_T1_AUDIT.md` | Summary for human review (NOT machine input) |

### Turn 2 Required Outputs (1 file + kernel receipt)

| File | Content |
|------|---------|
| `{TICKER}_A7_VALUATION_ENRICH.json` | Kernel execution output |
| `{TICKER}_KERNEL_RECEIPT_ENRICH.json` | Execution proof (Pattern 13) |

### Output Protocol

1. **Write each artifact as pure JSON** - no markdown wrapper, no code fences
2. **Write each narrative as markdown** - clear section headings
3. **Use exact filenames above** - case-sensitive, underscores required
4. **Validate JSON before writing** - must parse without errors
5. **Inherit reporting_currency from BASE A.2** - verify consistency

### Anti-Patterns (DO NOT DO)

❌ Single consolidated markdown file with embedded JSON blocks
❌ JSON wrapped in ```json code fences
❌ Multiple artifacts in one file
❌ Omitting files (all 12 T1 files required)
❌ Using old naming convention ({TICKER}_ENRICH2.2.3eO_T1.md)
