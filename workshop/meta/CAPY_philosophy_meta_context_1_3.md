# CAPY Philosophy and Meta-Context (v1.3)

**A Living Document – Updated: December 10, 2025**

This document outlines the foundational philosophy and long-term vision for the CAPY pipeline. It serves as meta-context for Large Language Models (LLMs) tasked with executing, improving, or conceptualizing the pipeline, ensuring alignment between implementation details and strategic vision.

---

# Part I: The CAPY Philosophy

## 1.0 Core Mission and Thesis

The primary objective of the CAPY pipeline is to leverage the scaling capabilities, analytical power, and extensibility of Large Language Models (LLMs) to build State-of-the-Art (SoTA) pipelines for the fundamental valuation of securities.

**The CAPY Thesis:** We believe fundamental analysis is an optimal use case for advanced AI. It is a purely analytical domain, supported by rich and diverse datasets, and requires the integration of qualitative reasoning and quantitative modeling—areas where LLMs excel. As LLM capabilities (context windows, reasoning, accuracy) improve, a well-designed LLM-based workflow can, and eventually will, surpass human analytical capabilities.

## 2.0 The North Star: The Future Simulator

The long-term vision for CAPY is evolution toward a "Future Simulator."

Current methodologies, which rely on deterministic Discounted Cash Flow (DCF) models augmented by discrete Structured State Enumeration (SSE), represent an intermediate stage in the pipeline's evolution. **The 2.2e architecture validates SSE as a tractable bridge:** by modeling 4 discrete scenarios with joint probability distributions, we capture the primary risk structure while remaining computationally feasible within current LLM constraints. SSE provides the conceptual foundation—probabilistic valuation distributions—that the Future Simulator will eventually generalize.

The Future Simulator will supplant these methods with a comprehensive, Monte Carlo-based simulation engine. This engine will model a vast distribution of possible futures for the target security, capturing complex, dynamic interactions that shape reality:

- **Dynamic Macroeconomic States:** Modeling macro environments and their feedback loops with company fundamentals
- **Complex Capital Allocation:** Full modeling of buybacks, dilution, debt dynamics, and cost of capital across economic states
- **Interwoven Scenarios:** Modeling complex event chains and cyclicality rather than isolated, discrete events
- **Sophisticated Tail Risk:** Improved modeling of extreme outcomes

The output of the Future Simulator will be a distribution of intrinsic values, allowing us to read risk and return directly from the shape of the distribution.

## 3.0 Operating Philosophy: Extensibility and Evolution

### 3.1 Embracing "The Bitter Lesson"

We adhere to the principles of "The Bitter Lesson." We anticipate that as LLM capabilities increase, the need for rigid, human-imposed structure will decrease. The CAPY pipeline is designed to be highly extensible to these future improvements.

### 3.2 The Evolving Role of Structure

Today, we use structured protocols to ensure rigor and consistency with current LLMs. These are implementation details, not permanent philosophical laws.

Over time, the architecture will transition from prescribing "the how" to defining "the what" (the objectives) and "the why" (the rationale), allowing stronger LLMs to optimally solve problems with greater autonomy. While reducing rigid structure, we emphasize providing strong LLMs with optimal context (including this Philosophy document) to ensure alignment.

### 3.3 Recursive Improvement

We utilize LLMs recursively—not only to execute the valuation pipeline but also to critique and improve the underlying financial theory, the prompting strategies, and the execution code itself.

### 3.4 The Two-Shot Architecture Rationale (New in v1.3)

The 2.2e pipeline introduces a fundamental architectural pattern: **separation of analytical synthesis from computational execution** across distinct turns (T1/T2) in fresh LLM contexts.

**The Problem Solved:** Early pipeline iterations suffered from a critical failure mode—LLMs would "fabricate" computational results rather than deferring to kernel execution. When analytical reasoning and computation occur in the same context, models conflate the tasks, hallucinating numerical outputs that appear plausible but aren't grounded in actual calculation.

**The Two-Shot Solution:**
- **Turn 1 (Analytical):** LLM performs pure reasoning—causal inference, evidence synthesis, assumption construction. Kernel code is embedded in prompt for semantic alignment only; no .py file is attached.
- **Turn 2 (Execution):** Fresh LLM instance validates T1 artifacts, repairs JSON malformation, and executes kernel. Separation ensures computation is deterministic and verifiable.

**Benefits:**
1. **Fabrication Prevention:** T1 cannot execute code it doesn't have
2. **Error Correction Layer:** T2 operates as validation gate before kernel execution
3. **Fresh Context:** Prevents attention degradation in long analytical turns
4. **Reproducibility:** Given identical T1 artifacts, T2 produces identical outputs

This architecture embodies a key insight: LLMs excel at reasoning and synthesis; Python excels at arithmetic. Forcing separation honors each system's comparative advantage.

## 4.0 Core Architectural Tenets

While the pipeline is extensible, certain tenets provide necessary anchors for rigorous analysis and computational integrity.

### 4.1 The Structural Causal Model (SCM)

The SCM is central to the CAPY methodology. It provides LLMs with a necessary framework, grounded in academic literature, to organize their world models, emphasize causality, and model unit economics explicitly rather than relying on high-level aggregation.

The LLM is responsible for dynamically inferring and generating the appropriate SCM structure for the target security. The SCM also provides the rigorous foundation required for modeling scenarios as causal "do-interventions."

### 4.2 The CVR Kernel

Computational integrity and normative consistency are paramount. The CVR Kernel (the Python execution engine) serves as the validated guarantor of mathematical execution. A standardized Kernel remains a core component of the pipeline, ensuring consistency across iterations (e.g., enforcing APV methodology, discounting conventions) and optimizing the use of LLM resources.

### 4.3 Epistemic Anchoring (The Outside View)

The power of advanced LLMs introduces the risk of "analytic capture"—the rigorous execution of an internally consistent model that is detached from external reality. To ensure the pipeline remains grounded, the methodology mandates Epistemic Anchoring. This requires the LLM to adopt a Bayesian approach: explicitly defining priors (the "outside view" based on consensus, historical base rates, and first principles) before updating them with company-specific evidence (the "inside view"). This rigor is foundational for the validity of all analytical outputs.

### 4.4 The State Vector and MRC Paradigm (New in v1.3)

The **Minimal Reproducible CVR (MRC)** paradigm treats pipeline outputs as an evolving state vector that enables deterministic reconstruction and complete auditability.

**State Vector Evolution:**
- **State 1 (BASE):** Artifacts A.1–A.7 (Epistemic Anchors, Analytic KG, Causal DAG, GIM, DR Derivation, Lightweight Valuation)
- **State 2 (ENRICH):** A.1–A.9 (refined assumptions with enrichment trace)
- **State 3 (SCENARIO):** A.1–A.10 (probabilistic valuation via SSE)
- **State 4 (INT):** A.1–A.12 (adjudicated findings, finalized distribution)
- **State 5 (IRR):** A.1–A.14 (expected return analysis)

**The Audit Infrastructure Principle:** Any downstream stage can fully reconstruct the analytical path from A.1 epistemic anchors through final E[IRR]. This isn't merely documentation—it's the foundation of trust. When the model claims E[IRR] = 7.3%, an auditor can trace precisely which assumptions drive that conclusion and whether those assumptions are epistemically grounded.

### 4.5 Parallel Adversarial Audit (New in v1.3)

Single-model analysis risks "analytical capture"—an internally consistent but externally detached model. The 2.2e architecture addresses this through **parallel adversarial audit:**

- **Silicon Council (SC):** Multiple LLM instances (e.g., Gemini, Claude, o-series) independently audit the CVR State 3 output. Each produces findings without knowledge of other auditors' conclusions.
- **Concordance Analysis:** The INTEGRATION stage synthesizes SC findings, weighing concordant critiques (multiple models flag same issue) more heavily than isolated concerns.
- **Human-in-the-Loop (HITL):** Optional dialectic audit where human analyst challenges CVR with LLM mediator adjudicating. Scoring rubric ensures rigor; human intuition surfaces issues models miss.

This multi-perspective architecture reduces the probability that systematic blind spots propagate through to final valuation.

### 4.6 Transition Factor Methodology (New in v1.3)

The IRR stage required a novel methodological contribution to translate static intrinsic value into time-based expected returns.

**The Problem:** Legacy approaches used cohort-based "fair multiple" convergence—assuming the market eventually prices stocks at sector median multiples. This is empirically weak and theoretically unsatisfying.

**The Transition Factor (TF) Solution:** TF preserves the relationship between market price and DCF-implied value while allowing fundamentals-driven multiple evolution.

**Key Property:** For a fairly-valued stock (market price ≈ DCF value), the null case IRR should approximately equal the discount rate. TF achieves this by anchoring multiple evolution to DCF-implied multiples rather than external cohort medians.

This methodology represents a genuine intellectual contribution—it solves the "what will I make?" question in a way that's theoretically grounded and empirically tractable.

## 5.0 Development Strategy: Pragmatism and Prioritization

We recognize that the Future Simulator is a long-term vision, potentially taking years to realize, gated by the evolution of LLM capabilities. Our development strategy is pragmatic, iterative, and focused on tractability.

### 5.1 Prioritization Metric

New features are prioritized based on their "analytic bang for the buck"—defined as the expected marginal contribution to the risk-adjusted IRR of the pipeline.

### 5.2 Vectors of Development

We approach the Future Simulator from three converging directions:

1. **Analytical Modules:** We continuously build increasingly powerful analytical modules (DCF, SSE, IRR analysis, adversarial auditing) and develop capabilities required for the Monte Carlo vision.

2. **Data Diversity and Synthesis:** We feed the models increasingly diverse and high-quality research—public financials, paywalled content (expert interviews, sell-side research), diverse buy-side perspectives (fund letters, specialized forums), and relevant alternative data. LLMs are responsible for integrating these sources, vetting quality, resolving conflicts, and managing biases.

3. **Modality Integration:** While the core focus is bottom-up fundamental analysis, we plan to integrate other alpha-generating modalities (top-down macro, technical analysis for timing). We rely on LLM sophistication to manage complexity and avoid overfitting.

## 6.0 Utility and Strategic Focus

CAPY is utilized by sophisticated investors focused on long-term capital appreciation with low-to-moderate risk.

**Market Niche:** The strategy focuses on generating alpha by being long-only in a concentrated portfolio (~20-30 securities). We prioritize less efficient markets (e.g., small/micro-cap), where deep fundamental analysis provides the greatest advantage.

**Future Utility:** Once the pipeline demonstrates sustained performance, we will explore other revenue streams, including licensing to institutions or selling research products.

---

# Part II: The G3 Meta-Prompting Doctrine (v1.3)

**Updated: December 10, 2025**

## 1.0 Introduction and Philosophical Shift

The CAPY pipeline was designed to be extensible to advancements in LLM capabilities. The transition from G2.5 to G3-class models (Gemini 3, Claude 4.5, o-series) necessitates a fundamental shift in prompting paradigm.

**The G2.5 paradigm** was characterized by Rigid Scaffolding. Prompts were highly prescriptive, emphasizing *how* to execute tasks through strict rules. This was necessary to mitigate reasoning limitations of earlier models.

**The G3 paradigm** embraces Guided Autonomy. Superior reasoning, synthesis, and context management allow us to adhere to "The Bitter Lesson." We transition from prescribing the process to defining the objectives (the "what") and the rationale (the "why"), empowering G3-class models to determine the optimal execution path.

## 2.0 The Core Tension: Autonomy vs. Rigor

The central challenge in the G3 paradigm is balancing increased model autonomy with non-negotiable pipeline requirements:

- **Analytical Rigor:** Adherence to core financial principles (Causality, Economic Convergence)
- **Reproducibility:** Consistent execution across runs
- **Epistemic Grounding:** Anchoring to external reality, avoiding "analytic capture"
- **Auditability:** Transparent tracing of assumptions and calculations
- **State Passing:** Reliable handoffs of structured artifacts between stages

The G3 Doctrine manages this tension by shifting from ex-ante prescription to ex-post verification. We trust G3 to execute the analysis but verify the integrity of the output.

## 3.0 The 2.2e Pipeline Topology (New in v1.3)

The validated 2.2e architecture consists of 8 stages with defined execution patterns:

```
BASE → RQ_GEN → ENRICH → SCENARIO → SC (parallel) → INT → IRR
                                     ↑
                                    HITL (optional)
```

**Execution Patterns:**

| Pattern | Stages | Structure |
|---------|--------|-----------|
| Two-Shot | BASE, ENRICH, SCENARIO, IRR | T1: Analytical synthesis → T2: Validation + kernel execution |
| Three-Shot | INT | T1: Adjudication → T2: Kernel execution → T3: Narrative synthesis |
| Single-Shot | RQ_GEN, SC, HITL | Complete execution in one turn |

**Rationale for Three-Shot INT:** Integration performs three distinct cognitive tasks—adjudicating SC findings, executing recalculation cascade, and synthesizing final narrative from all upstream sources. Separating these prevents context exhaustion and enables T3 concatenation mode (copy/paste rather than regeneration).

## 4.0 The Eight Principles of the G3 Doctrine

### P1. Objective-Oriented Architecture

We move away from prescriptive, step-by-step instructions. Prompts define the desired end state and analytical constraints, allowing G3 to determine the optimal path.

### P2. The Verification Doctrine (Trust but Verify)

We reduce cognitive overhead from upfront rigidity, shifting focus to validation.

- **Externalized Schemas:** JSON schemas defined in appendices, not inline
- **Emphasis on Validation:** Output validated against schemas; compliance burden on model's verification capabilities

### P3. Strategic Contextualization

G3's capabilities are best utilized when it understands strategic intent.

- **Meta-Context Primacy:** Execution prompts accompanied by foundational meta-context (Philosophy, Doctrine)
- **Rationale over Rules:** Explain *why* behind constraints rather than just listing rules

### P4. Analytical Depth over Information Density

We leverage G3's ability to produce coherent, high-value analytical narratives.

- **Synthesis Mandate:** Prompts demand synthesis of conflicting information, nuanced justifications, cohesive arguments
- **Optimizing for Downstream Consumption:** Narratives structured for the "Next LLM Reader," improving pipeline coherence

### P5. Epistemic Anchoring (Bayesian Priors and First Principles)

To prevent "analytic capture," the model adopts a Bayesian approach: defining priors (outside view) before updating with company-specific evidence (inside view).

**The Epistemic Anchor Protocol:**
1. Near-Term Anchors: Establishing Consensus/Guidance priors
2. Long-Term Anchors: Historical Base Rates, First Principles review
3. The Variance Mandate: Material deviations require rigorous "Variance Justification"
4. Post-Execution Reality Check: Implied multiples analyzed against benchmarks

### P6. Enhanced Causal Reconciliation

G3 must provide a complete, auditable trace of reasoning:

Qualitative Evidence → Analytical Interpretation → Reconciliation with Anchors → Quantitative Assumption (GIM) → Forecast Outcome (SCM) → Valuation Impact

### P7. Dynamic Research Orchestration

We leverage G3's ability to identify knowledge gaps, structured within pipeline constraints.

- **Constrained Allocation:** Research adheres to downstream input budget (6 RQ slots for ENRICHMENT)
- **Platform Targeting:** RQs targeted to available platforms (AlphaSense, Deep Research)
- **RQ Precision:** Self-contained prompts specifying desired output structure

### P8. Human-in-the-Loop Integration (New in v1.3)

The pipeline integrates structured human oversight without sacrificing scalability.

- **HITL Dialectic:** Human analyst challenges CVR via structured protocol with LLM mediator ("Final Boss")
- **Scoring Rubric:** Contributions scored (-1 to +5) based on evidentiary rigor and novelty
- **Dual Tracks:** CONTRADICTION (requires extraordinary evidence) vs. AUGMENTATION (additive findings)
- **Integration Path:** HITL findings flow to INT stage alongside SC outputs

This principle acknowledges that human intuition surfaces risks that even multi-model adversarial audit may miss—particularly "unknown unknowns" outside the models' training distribution.

## 5.0 Computational Integrity and Efficiency

The separation of reasoning (LLM) and calculation (Python) remains a core tenet.

- **The CVR Kernel:** Validated Python execution engine remains sole authorized engine for all forecasting, valuation, and integration calculations
- **The MRC Principle:** LLM emissions limited to minimal artifacts required for rigorous state passing; downstream stages leverage kernel determinism for reconstruction
- **Selective Emission:** Kernel APIs return lightweight summaries for LLM analysis, minimizing token consumption

## 6.0 Execution Environment Considerations (New in v1.3)

The 2.2e pipeline is validated for browser-based execution with manual orchestration. Future versions will target API/CLI execution.

**Browser Environment (Current):**
- Human orchestrator manages stage sequencing and file handoffs
- Each turn executes in fresh conversation context
- Validator prompt provides mechanical quality gate between stages

**API/CLI Environment (Future 2.3+):**
- Automated pipeline orchestration
- Sub-agent architecture for parallel SC execution
- Programmatic integration with financial data sources
- Reduced latency, increased throughput

The architectural decisions in 2.2e (strict state vector, externalized schemas, deterministic kernels) are designed to enable this transition without prompt rewrites.

---

# Part III: Model Limitations and the Bitter Lesson (New in v1.3)

Current frontier models still exhibit reasoning failures under context pressure—economic intuition gaps, anchoring errors, incomplete causal reasoning. These manifest as issues like implausible terminal assumptions or asymmetric scenario design.

**The key insight:** These are capability limitations, not architectural gaps requiring hot-fixes. A human analyst applying economic intuition catches most such errors. As model reasoning capabilities improve, these issues will resolve naturally—consistent with the Bitter Lesson framing that motivates the entire pipeline design.

The appropriate response is not to engineer around each observed failure mode, but to:
1. Maintain robust adversarial audit (SC, HITL) to catch reasoning errors
2. Trust that capability scaling will reduce error frequency
3. Reserve architectural intervention for genuinely structural issues (e.g., fabrication prevention via two-shot, which addresses a systematic failure mode rather than a reasoning gap)

**2.3 Development Focus:** API/CLI execution environment to unlock automation, sub-agents, and programmatic data integration. This is infrastructure investment, not error-patching.

---

# Part IV: Evolution of the Four Pillars

The original Four Pillars evolved from rigid constraints (G2.5) to guiding principles enforced by verification (G3). The 2.2e implementation further refines their role.

| Pillar | G2.5 Implementation | G3 Implementation | 2.2e Implementation |
|--------|---------------------|-------------------|---------------------|
| **P1: Causality** | Mandatory DAG template | LLM-inferred SCM with validation | Dynamic SCM + kernel verification of DAG-GIM alignment |
| **P2: Economic Convergence** | Fixed terminal assumptions | Anchored with variance justification | TF methodology anchors to DCF-implied multiples |
| **P3: Transparency** | Step-by-step logging | Causal chain reconciliation | Full state vector with MRC reconstruction |
| **P4: Information Density** | Strict token budgets | Deprecated for analytical depth | Two-shot architecture manages context naturally |

---

*This document will continue to evolve as the pipeline matures and LLM capabilities advance. Version 1.3 reflects the validated 2.2e architecture and incorporates learnings from the DAVE Inc. smoke test (December 2025).*
