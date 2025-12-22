G3 IRR 2.2.5e: Expected Return Analysis
________________


I. MISSION AND OBJECTIVES
Mission: Execute the IRR stage (G3_2.2.5eIRR) of the CAPY Pipeline for {Company Name} ({EXCHANGE:TICKER}) as of {DATE}.
Primary Objective: To transition the Computational Valuation Record (CVR) from State 4 (Finalized Intrinsic Value) to State 5 (Expected Return) by converting the probabilistic valuation distribution into a time-based expected rate of return at horizon T+1.
The IRR Value Proposition: The upstream stages (BASE → ENRICHMENT → SCENARIO → INTEGRATION) answer "What is it worth?" The IRR stage answers "What will I make?" This requires bridging the gap between intrinsic value (V) and market price (P) by modeling:
1. How fundamentals evolve to T+1 (fork-specific via Patch 2.1)
2. How the market prices those fundamentals using Transition Factor methodology (Patch 2.2-2.3)
3. How scenarios affect both fundamentals AND multiples (ρ-weighted blending)
4. How the market-to-DCF ratio evolves (TF preserves relative valuation)


Key Principle (Patch 2.2.3): For a fairly-valued stock (market price = DCF value), the null case IRR should approximately equal the discount rate. This is achieved via the Transition Factor approach, which eliminates the legacy cohort-based "fair multiple" anchor in favor of DCF-implied multiples.


Execution Paradigm: DCF-Anchored Market Evolution. The IRR stage derives expected returns from the relationship between current market price and DCF-implied value, rather than assuming convergence toward cohort median multiples.
________________


II. EXECUTION ENVIRONMENT AND CONSTRAINTS
A. Mandatory Inputs
The IRR stage receives the **CVR State 4 Bundle** from INTEGRATION 2.2.3e—a consolidated JSON object containing all finalized artifacts. The bundle structure (defined in INTEGRATION Section II.F) provides:

**Compatibility:** This stage consumes INT 2.2.3e T3 output. The
bundle_metadata.schema_version should be `G3_2.2.3eI_BUNDLE`.

**Audit Findings Reference:** IRR accesses Silicon Council findings via
A.12_INTEGRATION_TRACE.audit_synthesis, not raw A.11. The A.12 contains
synthesized concordance analysis and Pipeline Fit grade from parallel SC execution.


**Primary Input: CVR State 4 Bundle**


| Bundle Component | Purpose in IRR Stage |
|------------------|----------------------|
| `A.2_ANALYTIC_KG` | Current price, FDSO, Y0 fundamentals, market context, capital structure |
| `A.7_LIGHTWEIGHT_VALUATION_SUMMARY` | Base case IVPS, DR, terminal values, **Y0-Y3 trajectory checkpoints** |
| `A.10_SCENARIO_MODEL_OUTPUT` | Scenario definitions (P, M), JPD, constraints, distribution statistics |
| `A.12_INTEGRATION_TRACE` | State 4 E[IVPS], adjusted scenario values, Pipeline Fit grade, blind spots |
| `state_4_active_inputs` | **Pre-merged computational inputs** (fundamentals trajectory, finalized scenarios, valuation anchor, market data) |
| `final_thesis_synthesis` | Post-adjudication investment thesis for narrative context |


**Critical Data Paths:**
- **T+1 Fundamentals:** Extract from `state_4_active_inputs.fundamentals_trajectory.Y1` (NOT interpolated)
- **Scenarios:** Extract from `state_4_active_inputs.scenarios_finalized` (post-adjudication probabilities)
- **Valuation Anchor:** Extract from `state_4_active_inputs.valuation_anchor` (E[IVPS], DR, terminal values)
- **Market Data:** Extract from `state_4_active_inputs.market_data_snapshot` (current price, FDSO, net debt)
- **Convergence Rate (CR):** Calculated per B.13 rubric using recognition-speed factors only


A.x Two-Shot Execution Paradigm

The IRR stage executes across two turns to separate analytical judgment from deterministic computation.

**Turn 1: Analytical**

**Trigger:** "Do Turn 1: IRR for {Company Name}, {EXCHANGE:TICKER}"

**Attachments Required:**
- G3_IRR_2.2.5e_PROMPT.md (this file)
- G3_IRR_2.2.5e_SCHEMAS.md
- G3_IRR_2.2.5e_NORMDEFS.md
- INT T3 Output ({TICKER}_INT_T3_{YYYYMMDD}.md) containing CVR State 4 Bundle
- CVR_KERNEL_IRR_2.2.5e.py (context only — DO NOT EXECUTE)

**Scope:**
- Phase 0: Input extraction and validation
- Phase 2: Resolution timeline estimation (ρ for each scenario)
- CR derivation via B.13 rubric (Categories 1-4)
- Multiple selection rationale via B.10
- Anti-narrative discipline check (P5)

**Output:**
- A.13_RESOLUTION_TIMELINE artifact (extended schema with all kernel inputs)
- Filename: {TICKER}_IRR_T1_{YYYYMMDD}.md

**Exclusion:** DO NOT execute Kernel. Kernel is provided for semantic alignment only.

**Turn 2: Computational**

**Trigger:** "Do Turn 2"

**Attachments Required:**
- G3_IRR_2.2.5e_PROMPT.md (this file)
- T1 Output ({TICKER}_IRR_T1_{YYYYMMDD}.md)
- CVR State 4 Bundle (fresh context)
- CVR_KERNEL_IRR_2.2.5e.py

**Scope:**
- Load kernel
- Execute kernel via Bash (Pattern 6)
- Format A.14 output

**Output:**
- A.14_IRR_ANALYSIS artifact
- Executive summary narrative
- Filename: {TICKER}_IRR_T2_{YYYYMMDD}.md

**Critical:** T2 performs NO reasoning. All analytical judgment is locked in A.13.


B. The CVR Kernel Mandate
The CVR Kernel (G3_2.2.5e_IRR) is the sole authorized execution engine for all IRR calculations.

**Kernel Location:** `kernels/CVR_KERNEL_IRR_2.2.5e.py`

1. Loading & Execution (Two-Shot File Delivery):
   * Turn 1: CVR_KERNEL_IRR_2.2.5e.py is attached for contextual understanding
     only (function signatures, TF methodology, CR integration, fork generation logic).
     DO NOT execute kernel code in T1.
   * Turn 2: Execute kernel via Bash (Pattern 6):
     ```bash
     python3 CVR_KERNEL_IRR_2.2.5e.py \
       --a13 {TICKER}_A13_RESOLUTION_TIMELINE.json \
       --inputs {TICKER}_IRR_INPUTS.json \
       --output {TICKER}_A14_IRR_ANALYSIS.json
     ```
Required Functions:
* calculate_forward_fundamentals(): Project metrics to T+1
* select_valuation_multiples(): Apply B.10 rubric
* calculate_transition_factor(): Compute TF from DCF multiples (Patch 2.2)
* calculate_market_multiple_t0(): Current market-implied multiple (Patch 2.2)
* build_scenario_fundamentals_map(): Extract scenario fundamentals (Patch 2.1)
* calculate_fork_fundamentals(): ρ-blend fundamentals for fork (Patch 2.1)
* calculate_scenario_multiple_impacts_from_ivps(): IVPS → multiple impact (Patch 2.3)
* calculate_fork_market_multiple(): TF-based fork multiple (Patch 2.3)
* generate_irr_forks_tf(): TF-based fork generation (Patch 2.3)
* calculate_irr_distribution(): E[IRR] and percentiles
* run_sanity_checks(): Dispersion and diagnostic tests
* execute_irr_workflow(): Main orchestrator API (TF-based)
Prohibition: Implementing custom IRR, valuation, or distribution calculations outside the Kernel is strictly prohibited.
C. Search Policy
**MANDATORY - Live Price Refresh:** The CVR State 4 Bundle contains a market_data_snapshot that may be hours or days stale. Before any IRR calculation, you MUST search for the current stock price using web search. The live price overrides the bundle price. This is non-negotiable—IRR calculations using stale prices produce misleading results.

Limited Authorization: Beyond mandatory price refresh, search is authorized only for:
* Retrieving current market context (risk-on/risk-off indicators)
* Confirming macro conditions relevant to CR assessment (B.13)
Prohibited: Open-ended research, thesis generation, or scenario discovery. The analytical work is complete; IRR translates existing conclusions into returns.
D. Horizon Constraint
T+1 Only: The IRR stage models a single horizon: one year forward. This produces 17 forks (16 scenario combinations + null case) maximally, but fewer given the application of the MECE protocol removing impossible forks..
Rationale: The CAPY pipeline runs at least annually. Modeling T+2 and T+3 introduces compounding estimation error without proportionate benefit. At T+1, the pipeline will re-execute with updated information.
E. Emission Policy and Workflow Sequence


The IRR stage follows a two-phase workflow:


**Phase A: Qualitative Analysis (LLM generates)**
1. A.13_RESOLUTION_TIMELINE artifact — Bayesian estimation of resolution percentages (ρ)
   for each scenario. This artifact must be generated BEFORE kernel execution.
   Extract ρ values from A.13 to pass to the kernel.


**Phase B: Quantitative Analysis (Kernel executes)**
2. Call execute_irr_workflow() with rho_estimates extracted from A.13
3. Kernel returns A.14_IRR_ANALYSIS artifact


**Final Emission:**
- Analytical narrative (executive summary, key findings)
- A.13_RESOLUTION_TIMELINE (from Phase A)
- A.14_IRR_ANALYSIS (from Phase B)


Note: The kernel requires rho_estimates as input because ρ estimation is analytical
judgment (timing evidence, catalyst identification) that cannot be mechanized. The
LLM must perform this analysis qualitatively before invoking computational functions.


Reprinting instructions, schemas, or kernel code is prohibited.
________________


III. CORE ANALYTICAL DIRECTIVES
P1. Conservative Anchoring (The Outside View First)
All uncertain parameters must be anchored to outside-view defaults before inside-view adjustments.
Convergence Rate: Default CR = 0.20 (B.13 base rate). Departures above 0.40 require variance justification per B.13.4.
Resolution Percentage: Default ρ ≤ 0.30 absent specific timeline evidence. B.12 provides guidance for upward adjustments when timeline evidence is present. Document deviation rationale in A.13.
Rationale: LLMs exhibit narrative bias toward resolution and convergence. Conservative anchors counteract this tendency.
P3. Resolution Percentage Estimation (ρ ≠ P)
Resolution percentage measures how much uncertainty resolves by T+1, not the probability of occurrence.
The Distinction:
* P(scenario) = likelihood the scenario occurs
* ρ(scenario) = fraction of uncertainty resolved by T+1, regardless of outcome
A scenario with P=0.35 may have ρ=0.80 (we'll know soon) or ρ=0.20 (still ambiguous).
Evidence Basis: ρ estimates must cite primary driver, key dates, and reference class where available.
P4. Null Case Primacy
The null case (no scenario resolution beyond ρ-weighted partial impacts) is the analytical anchor.
Calculate First: The null case IRR must be computed and decomposed before fork generation.
Decomposition Required: Break null case IRR into:
* Fundamental Growth IRR (metric growth at constant multiple)
* Multiple Convergence IRR (re-rating at constant fundamentals)
This decomposition reveals return quality and identifies convergence dependency.
P5. Anti-Narrative Discipline
Before finalizing convergence rate, generate three reasons the market might NOT re-rate the stock.
Purpose: Forces consideration of value trap scenarios and counteracts narrative bias.
Documentation: The three reasons must appear in anti_narrative_check in A.13.
CR Consistency Check (per B.13):
- CR adjustments use only recognition factors (no fundamentals double-counting)
- Hard catalysts are in scenario structure with ρ, not CR adjustments
- CR consistent with comparable positions in portfolio
- If CR > 0.30: Is recognition environment genuinely exceptional?
- If CR < 0.12: Have we considered whether this is uninvestable?
P6. Fork Independence
Each fork's multiple estimate should derive from its fundamental profile, not from a global "thesis" about the company.
Check: After generating all forks, verify adequate dispersion. If the coefficient of variation of fork multiples falls below 0.10, flag potential correlation bias.
Rationale: If all forks cluster tightly, errors are correlated and do not diversify across the probability distribution.
P7. Sanity Check Mandate
Before emission, execute all mechanical sanity checks:
1. Value Trap Test: Calculate IRR with zero convergence. If below hurdle, position is convergence-dependent.
2. Fork Independence Check: Verify adequate dispersion in fork multiples.
3. Diagnostic Flags: Flag if average ρ > 0.50, all IRRs positive, or CR > 0.40.
These are diagnostic outputs for human review, not gates that block emission.
________________


IV. EXECUTION PROTOCOL
Execute the workflow in phases. Each phase produces intermediate outputs that feed subsequent phases.
________________


Phase 0: Input Extraction and Validation
Objective: Extract and validate all inputs from CVR State 4 Bundle.
Steps:
1. **MANDATORY - Fetch Live Market Price:**
   * BEFORE extracting bundle data, search for "{TICKER} stock price" to get current market price
   * Record: live_price_t0, price_source (exchange/provider), price_timestamp
   * This live price OVERRIDES any price in the bundle's market_data_snapshot
   * Rationale: Bundle price may be hours/days stale; IRR requires up-to-the-minute pricing
2. Extract Market Data:
   * Primary: state_4_active_inputs.market_data_snapshot
   * Fallback: A.2 market_context and share_data
   * Required: shares_outstanding, net_debt
   * **OVERRIDE: Replace current_price with live_price_t0 from Step 1**
3. Extract Valuation Anchor:
   * Primary: state_4_active_inputs.valuation_anchor
   * Contains: e_ivps_state4, dr_static, base_case_ivps_state2
   * Fallback: A.7 ivps_summary
4. Extract Fundamentals Trajectory:
   * Primary: state_4_active_inputs.fundamentals_trajectory (Y0, Y1)
   * Fallback: A.7 forecast_trajectory_checkpoints
   * Y1 is REQUIRED - no fallback to Y5 (would distort T+1 by 50-100%)
5. Extract Scenarios:
   * Primary: state_4_active_inputs.scenarios_finalized (post-adjudication)
   * Fallback: A.10 scenario_definitions (pre-adjudication)
6. Select Valuation Multiple:
   * Apply B.10 rubric based on T+1 fundamentals profile
   * Document primary metric selection rationale
7. Validate Inputs:
   * **live_price_t0 > 0** (from Step 1 search), shares_outstanding > 0, e_ivps_state4 > 0
   * Y1 revenue > 0
Output: Validated inputs ready for Transition Factor calculation
Lock Point: Validated inputs cannot be revised in subsequent phases.
________________


Phase 1: Transition Factor Calculation
Objective: Calculate TF from DCF multiples to project market multiple evolution.
Steps:
1. Calculate Market-Implied Multiple at T0:
   * Market_Multiple_T0 = EV_Market / Metric_Y0
   * Where EV_Market = Market_Cap + Net_Debt
2. Calculate DCF-Implied Multiple at T0:
   * Equity_T0 = IVPS_T0 × FDSO
   * EV_DCF_T0 = Equity_T0 + Net_Debt
   * DCF_Multiple_T0 = EV_DCF_T0 / Metric_Y0
3. Project DCF-Implied Multiple to T+1:
   * IVPS_T1 = IVPS_T0 × (1 + DR)  [intrinsic value compounds at discount rate]
   * Net_Debt_T1 = Net_Debt_T0 - FCF_Y1  [assuming FCF retained]
   * Equity_T1 = IVPS_T1 × FDSO
   * EV_DCF_T1 = Equity_T1 + Net_Debt_T1
   * DCF_Multiple_T1 = EV_DCF_T1 / Metric_T1
4. Calculate Transition Factor:
   * TF = DCF_Multiple_T1 / DCF_Multiple_T0
   * This captures how the DCF-implied multiple evolves as fundamentals grow
5. Apply TF to Market Multiple:
   * Market_Multiple_T1_Null = Market_Multiple_T0 × TF
   * This preserves the market-to-DCF ratio (relative valuation)
6. Calculate Null Case IRR:
   * EV_T1 = Metric_T1 × Market_Multiple_T1_Null
   * Equity_T1 = EV_T1 - Net_Debt_T1
   * Price_T1 = Equity_T1 / FDSO
   * Null_IRR = (Price_T1 / Price_T0) - 1
7. Apply Convergence Rate Adjustment:

   The Convergence Rate determines what fraction of the T+1 gap between market
   and DCF multiples closes during the year.

   * Gap_T1 = DCF_Multiple_T1 - Market_Multiple_T1_Null
   * CR_Contribution = CR × Gap_T1
   * Adjusted_Market_Multiple_T1 = Market_Multiple_T1_Null + CR_Contribution

   Equivalently (linear interpolation):
   * Adjusted_Market_Multiple_T1 = (1 - CR) × Market_Multiple_T1_Null + CR × DCF_Multiple_T1

   Where:
   - CR = 0: No convergence; market multiple follows pure TF evolution
   - CR = 1: Full convergence to DCF multiple by T+1 (unrealistic; capped at 0.40)
   - CR = 0.20 (default): 20% of gap closes annually (~3.5 year half-life)

   **Key Property:** For fairly-valued stocks (Market_Multiple = DCF_Multiple),
   Gap = 0, so CR has no effect and Null_IRR ≈ DR. This is correct — an asset
   priced at intrinsic value should return its cost of capital regardless of
   recognition speed.

   **Example:**
   - DCF Multiple T+1 = 18, Market Multiple T+1 (pre-CR) = 9
   - Gap = 18 - 9 = 9 multiple points
   - CR = 0.20 → CR_Contribution = 0.20 × 9 = 1.8
   - Adjusted Market Multiple = 9 + 1.8 = 10.8
   - Verification: Closed 1.8 of 9.0 gap = 20% ✓


Key Insight: For a fairly-valued stock (Market_Multiple ≈ DCF_Multiple), the
null case IRR will approximate the discount rate. This is the correct behavior—
an asset priced at intrinsic value should return its cost of capital.


Output: Transition Factor, null case market multiple T+1, null case IRR
________________


Phase 2: Resolution Timeline Estimation
Objective: Estimate ρ(S, T+1) for each scenario from A.10.
Steps:
1. Enumerate Scenarios:
   * Extract scenario list from A.10 (typically 4 scenarios)
   * Note full magnitude M for each
2. For Each Scenario, Estimate ρ:
   * Identify primary driver (legal, product, macro, competitive)
   * Identify key dates or milestones before T+1
   * Consult reference class for timing if available
   * Assign ρ ∈ [0, 1]
3. Apply Conservatism Check:
   * If no specific timeline evidence, default ρ ≤ 0.30
   * Document evidence for ρ > 0.30
4. Calculate Effective Magnitudes:
   * Effective_M = ρ × Full_M for each scenario
5. Aggregate Diagnostics:
   * Calculate average ρ across scenarios
   * Flag if average ρ > 0.50
Output: A.13_RESOLUTION_TIMELINE artifact
________________


Phase 3: Fork Generation
Objective: Generate all possible forks with valuations using TF-based approach.
Steps:
1. Enumerate States:
   * Use JPD from A.10 (via kernel calculate_sse_jpd() or extract directly)
   * Each feasible state is a fork
   * Extract P(fork) from JPD
2. Build Scenario Fundamentals Map:
   * Extract fundamentals_y1_intervened from each scenario
   * These represent scenario-specific T+1 fundamentals adjustments
3. For Each Fork, Calculate Fundamentals:
   * Calculate ρ-weighted blend of scenario fundamentals
   * Fork_Fundamentals = Base + Σ(ρ × scenario_impact × scenario_state)
4. Calculate Scenario Multiple Impacts from IVPS:
   * Derive multiple impact from scenario IVPS effects
   * Multiple_Impact = (Scenario_IVPS - Base_IVPS) / Base_Metric
5. Calculate Fork Market Multiple:
   * Start with null case market multiple (Market_Multiple_T0 × TF)
   * Apply scenario multiple impacts weighted by ρ and scenario state
   * Fork_Multiple = Null_Multiple + Σ(ρ × multiple_impact × scenario_state)
6. Calculate Fork Valuations:
   * EV = Metric_T+1 × Fork_Multiple
   * Equity = EV - Net_Debt_T1
   * Price_T+1 = Equity / Shares
7. Calculate Fork IRRs:
   * IRR(fork) = (Price_T+1 / Price_T0) - 1
   * Use kernel function generate_irr_forks_tf()
Output: All possible fork valuations with probabilities and IRRs
________________


Phase 4: IRR Integration
Objective: Calculate E[IRR] and distribution statistics.
Steps:
1. Calculate E[IRR]:
  E[IRR] = Σ P(fork) × IRR(fork)
2. Calculate Distribution Statistics:
   * Sort forks by IRR ascending
   * Calculate cumulative probabilities
   * Extract P10, P25, P50, P75, P90
   * Calculate standard deviation
3. Calculate Probability Metrics:
   * P(IRR > Hurdle Rate)
   * P(IRR < 0) — probability of loss
4. Calculate Return Attribution:
   * Null case IRR (baseline return assuming no scenario resolution)
   * Scenario resolution contribution = E[IRR] - IRR_null
   * This simplified decomposition replaces legacy CDR analysis
5. Diagnostic Assessment:
   * Compare null case IRR to discount rate
   * If |Null_IRR - DR| > 5%, investigate market-DCF divergence
   * If E[IRR] >> Null_IRR, return depends heavily on scenario resolution
Output: IRR integration results
________________


Phase 5: Sanity Checks and Emission
Objective: Run mechanical checks and compile final artifacts.
Steps:
1. Null Case Validation:
   * For fairly-valued stock, null case IRR should ≈ discount rate
   * Large divergence indicates potential calculation error or extreme mispricing
   * Interpret: PASS (within 3% of DR) / CAUTION (3-8%) / WARNING (>8%)
2. Fork Independence Check:
   * Calculate CV of fork multiples
   * Flag if CV < 0.10 (potential correlation)
3. Diagnostic Flags:
   * Average ρ > 0.50? Flag (resolution optimism)
   * All fork IRRs positive? Flag (optimism check)
   * Market-DCF ratio > 1.5 or < 0.67? Flag (extreme valuation divergence)
4. Compile Confidence Assessment:
   * Overall confidence (HIGH / MEDIUM / LOW)
   * Key uncertainties
   * Highest-leverage assumptions
5. Emit Artifacts:
   * Finalize A.13_RESOLUTION_TIMELINE
   * Finalize A.14_IRR_ANALYSIS
   * Write executive summary narrative
Output: Complete IRR stage artifacts
________________


V. ARTIFACT EMISSION CHECKLIST
The IRR stage produces two new artifacts:
Artifact
        Schema Reference
        Content
        A.13_RESOLUTION_TIMELINE
        G3_IRR_2.2.5e_SCHEMAS.md
        ρ estimates per scenario with evidence traces
        A.14_IRR_ANALYSIS
        G3_IRR_2.2.5e_SCHEMAS.md
        Full IRR analysis including anchors, null case, forks, distribution, sanity checks
        State Transition:
Upon successful emission, the CVR transitions from State 4 (Finalized) to State 5 (Expected Return).
CVR_STATE_5 = {
  CVR_STATE_4,                    // All prior artifacts (A.1-A.12)
  A.13_RESOLUTION_TIMELINE,       // NEW: Scenario timing
  A.14_IRR_ANALYSIS               // NEW: Expected return analysis
}
Validation Requirements:
Before emission, verify:
* E[IRR] calculated from all feasible forks
* Distribution statistics complete (P10 through P90)
* Null case decomposition present
* All sanity checks executed
* Convergence rate ≤ 0.40 OR variance justification provided
* Anti-narrative check completed (3 reasons documented)
Emission Format: JSON, validated against schemas in G3_IRR_2.2.5e_SCHEMAS.md.
