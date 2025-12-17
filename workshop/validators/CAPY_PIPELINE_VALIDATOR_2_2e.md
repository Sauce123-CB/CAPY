# CAPY 2.2e Pipeline Validator

Post-pipeline validation audit. Run after completing IRR (or HITL if executed) to validate full CVR before use.

---

## Usage

In a fresh conversation:

1. Attach this prompt
2. Attach the README (`CAPY_2_2e_README_Clean.md`) as canonical specification
3. Attach three .zip bundles:
   - **prompts.zip** — All stage prompts used (G3BASE, BASE_T1_REFINE, RQ_Gen, G3ENRICH, G3_SCENARIO, G3_SILICON_COUNCIL, G3_INTEGRATION, G3_IRR, kernels)
   - **data.zip** — Financials, RQ outputs (1–6), SC outputs
   - **outputs.zip** — All pipeline outputs (BASE T1/REFINE/T2, RQ_GEN, ENRICH T1/T2, SCENARIO T1/T2, INT T1/T2/T3, IRR T1/T2)
4. Type: `/validate_pipeline {TICKER}`

---

## Validation Protocol

When you see `/validate_pipeline {TICKER}`, execute all phases below. Reference the attached README as canonical specification for all requirements.

---

### Phase 1: Output Completeness

**1.1 File Inventory**

Verify all required outputs present in outputs.zip:

| Stage | Required Files |
|-------|----------------|
| BASE | `{TICKER}_BASE2.2.1eO_T1_{DATE}.md`, `{TICKER}_BASE2.2.1eO_REFINE_{DATE}.md`, `{TICKER}_BASE2.2.1eO_T2_{DATE}.md` |
| RQ_GEN | `{TICKER}_RQ2.2.2eO_{DATE}.md` |
| ENRICH | `{TICKER}_ENRICH2.2.1eO_T1_{DATE}.md`, `{TICKER}_ENRICH2.2.1eO_T2_{DATE}.md` |
| SCENARIO | `{TICKER}_SCEN2.2.1eO_T1_{DATE}.md`, `{TICKER}_SCEN2.2.1eO_T2_{DATE}.md` |
| SC | `{TICKER}_SC2.2.1eO_{DATE}_{LLM}.md` (2–3 instances, e.g., `_G3PTR`, `_C45ET`, `_O3H`) |
| INT | `{TICKER}_INT2.2.2eO_T1_{DATE}.md`, `{TICKER}_INT2.2.2eO_T2_{DATE}.md`, `{TICKER}_INT2.2.2eO_T3_{DATE}.md` |
| IRR | `{TICKER}_IRR2.2.4eO_T1_{DATE}.md`, `{TICKER}_IRR2.2.4eO_T2_{DATE}.md` |

Flag: Missing files, naming convention violations, date inconsistencies across stages.

**1.2 Artifact Inventory**

Verify required artifacts present in each output:

| Output | Required Artifacts |
|--------|-------------------|
| BASE T1 | A.1, A.2, A.3, A.5, A.6 |
| BASE REFINE | A.1–A.6 (corrected or validated), DR re-derivation with X_T1, X_REFINE, X_final |
| BASE T2 | A.1–A.7 |
| RQ_GEN | A.8 (exactly 6 RQs: 3 AS, 3 GDR, M-1/M-2/M-3 mandatory slots covered) |
| ENRICH T1 | A.9 changelog, GIM amendments documented |
| ENRICH T2 | Updated A.7 with post-enrichment IVPS |
| SCENARIO T1 | 4 scenarios (S1–S4) with P, M estimates |
| SCENARIO T2 | A.10 with SSE, JPD, E[IVPS], distribution stats |
| SC (each) | A.11 with findings, Pipeline Fit grade, execution_context |
| INT T1 | Adjudication dispositions for all SC findings |
| INT T2 | A.12 present, state_4_active_inputs populated |
| INT T3 | Complete CVR State 4 (all narratives concatenated) |
| IRR T1 | A.13 with CR derivation, τ estimates, multiple selection |
| IRR T2 | A.14 with E[IRR], P(IRR > Hurdle), entry price recommendations |

Flag: Missing artifacts, incomplete JSON blocks, truncated outputs.

**1.3 Truncation Check**

For each output file, verify:
- No mid-sentence cutoffs
- JSON blocks have matching open/close braces
- INT T3 contains all expected sections (not cut short)

---

### Phase 2: Input/Output Chain Integrity

Verify each stage received correct inputs per README Section 6 (Attachment Cheat Sheet).

**2.1 BASE Chain**
- [ ] T1 received: Prompt (G3BASE_2.2.1e.md), Company docs
- [ ] REFINE received: REFINE prompt (BASE_T1_REFINE_v1_0.docx), BASE prompt (G3BASE_2.2.1e.md), Company docs, BASE T1 output
- [ ] T2 received: Prompt (G3BASE_2.2.1e.md), REFINE output (not T1), Kernel

**2.2 RQ_GEN Chain**
- [ ] Received: Prompt (RQ_Gen_2.2.2e.docx), Complete BASE outputs (REFINE + T2, or consolidated T2 if it contains all artifacts)

**"Complete BASE outputs"** = REFINE output (A.1–A.6) + T2 output (A.7). If T2 consolidates everything, use T2 alone. If T2 only emits A.7, need both REFINE and T2 (not original T1 unless needed for something missing).

**2.3 ENRICH Chain**
- [ ] T1 received: Prompt (G3ENRICH_2.2.1e.md), Complete BASE outputs, A.8, Research bundle (6 RQ responses)
- [ ] T2 received: Prompt (G3ENRICH_2.2.1e.md), ENRICH T1, Kernel

**2.4 SCENARIO Chain**
- [ ] T1 received: Prompt (G3_SCENARIO_2_2_1e.md), Complete ENRICH outputs
- [ ] T2 received: Prompt (G3_SCENARIO_2_2_1e.md), SCEN T1, Complete ENRICH outputs (fresh), Kernel

**2.5 SC Chain (Epistemic Parity)**
- [ ] Each SC instance received: Prompt (G3_SILICON_COUNCIL_2.2.1e.md), Financials bundle (.zip), RQ outputs (1–6), Complete ENRICH/SCENARIO outputs
- [ ] SC did NOT receive: BASE outputs (removed to avoid confusion)
- [ ] SC did NOT receive: Stage prompts for other stages (audits execution, not methodology)

**2.6 INT Chain (Epistemic Parity)**
- [ ] T1 received: Prompt (G3_INTEGRATION_2_2_2e.md), Financials bundle, RQ outputs (1–6), Complete ENRICH/SCENARIO outputs, All SC outputs
- [ ] T2 received: Prompt (G3_INTEGRATION_2_2_2e.md), INT T1, Complete ENRICH/SCENARIO outputs (fresh), Kernel
- [ ] T3 received: Prompt (G3_INTEGRATION_2_2_2e.md), INT T1, INT T2, Complete ENRICH outputs, Complete SCENARIO outputs
- [ ] T3 did NOT receive: SC outputs (already adjudicated in T1), Financials, RQs

**2.7 IRR Chain**
- [ ] T1 received: Prompt (G3_IRR_2.2.4e.md), Complete INT outputs
- [ ] T2 received: Prompt (G3_IRR_2.2.4e.md), IRR T1, Complete INT outputs (fresh), Kernel

**2.8 HITL Chain (if executed)**
- [ ] Received: Prompt (HITL_DIALECTIC_AUDIT_1_0.md), Complete INT outputs, Complete IRR outputs

Flag: Wrong upstream output attached, missing inputs, T1/REFINE turns with kernel attached.

---

### Phase 3: Kernel Execution Integrity

**3.1 Execution Verification**

For each T2 turn (BASE, ENRICH, SCENARIO, INT, IRR):
- [ ] Kernel execution log present in output
- [ ] No Python stack traces or errors
- [ ] Kernel version matches stage (BASE_CVR_KERNEL_2.2.1e.py, CVR_KERNEL_ENRICH_2.2.1e.py, CVR_KERNEL_SCEN_2_2_1e.py, CVR_KERNEL_INT_2_2_2e.py, CVR_KERNEL_IRR_2.2.4e.py)

**3.2 Fabrication Detection**

Check for T1 fabrication (LLM computed values that should only come from kernel):

| Stage | T1 Should NOT Contain | T2 Should Contain |
|-------|----------------------|-------------------|
| BASE T1 | IVPS numerical value | A.7 with IVPS |
| ENRICH T1 | Updated IVPS | Updated A.7 with post-enrichment IVPS |
| SCENARIO T1 | E[IVPS], SSE, JPD values | A.10 with E[IVPS], SSE, JPD, distribution stats |
| INT T1 | State 4 E[IVPS] | A.12 with recalculated values, state_4_active_inputs |
| IRR T1 | E[IRR] numerical value | A.14 with E[IRR], P(IRR > Hurdle) |

Flag: Numerical values in T1 outputs that should only appear post-kernel.

**3.3 Kernel Output Traceability**

Verify T2 kernel outputs flow forward correctly:
- BASE T2 A.7 IVPS → referenced in ENRICH
- ENRICH T2 A.7 IVPS → referenced in SCENARIO
- SCENARIO T2 A.10 E[IVPS] → referenced in INT
- INT T2 A.12 E[IVPS] → referenced in IRR
- IRR T2 A.14 E[IRR] → final output

Flag: Value discontinuities between stages without documented adjustments.

---

### Phase 4: Economic Realism

**4.1 Sanity Bounds**

| Metric | Valid Range | Location |
|--------|-------------|----------|
| IVPS | > 0 | BASE T2 A.7, ENRICH T2 A.7 |
| Discount Rate (DR) | 8–20% (typical range) | BASE REFINE A.6, all T2 outputs |
| Terminal Growth (g) | < DR | BASE T2 A.7 |
| Scenario Probabilities | Sum ≈ 1.0 (within rounding) | SCENARIO T2 A.10 |
| E[IVPS] | > 0, within 3x of base IVPS | SCENARIO T2 A.10, INT T2 A.12 |
| E[IRR] | -50% to +100% | IRR T2 A.14 |
| P(IRR > Hurdle) | 0–100% | IRR T2 A.14 |

Flag: Out-of-bounds values with specific location.

**4.2 DR Derivation Check (BASE REFINE)**

- [ ] X_T1 documented
- [ ] X_REFINE independently derived
- [ ] X_final = (X_T1 + X_REFINE) / 2
- [ ] If |X_REFINE - X_T1| > 0.3, divergence flagged in REFINE output
- [ ] DR_final = RFR + ERP × X_final
- [ ] Y0 calibration confirmed within ~5% of source financials

Flag: Missing derivation components, unaveraged X, unflagged divergence.

---

### Phase 5: State Evolution Coherence

**5.1 MRC State Progression**

Verify state vector evolution per README Section 1:

| State | Stage | Artifacts |
|-------|-------|-----------|
| MRC State 1 | BASE T2 | A.1–A.7 |
| MRC State 2 | ENRICH T2 | A.1–A.9 (refined) |
| MRC State 3 | SCENARIO T2 | A.1–A.10 (probabilistic) |
| MRC State 4 | INT T2/T3 | A.1–A.12 (adjudicated) |
| MRC State 5 | IRR T2 | A.1–A.14 (expected return) |

Flag: Missing state markers, artifacts not carrying forward.

**5.2 Amendment Traceability**

- [ ] ENRICH A.9 changelog documents what changed from BASE
- [ ] If DAG modified in REFINE, changes documented
- [ ] If DAG/GIM modified in ENRICH, changes reflected in A.9
- [ ] SC findings in A.11 → addressed in INT T1 adjudications
- [ ] INT adjudication dispositions → reflected in A.12 state_4_active_inputs

Flag: Undocumented changes, SC findings without INT disposition.

---

### Phase 6: Semantic Consistency

**6.1 DAG-GIM Alignment**

- [ ] All DAG nodes have corresponding GIM entries
- [ ] All GIM exogenous drivers are DAG leaf nodes
- [ ] No orphan nodes (defined but not connected)
- [ ] Node naming consistent across all outputs

**6.2 Y0 Calibration**

- [ ] BASE REFINE confirms Y0 calibration within ~5% of source financials
- [ ] Key financial metrics (Revenue, EBITDA, FCF) traceable to source docs in data.zip

**6.3 RQ Coverage**

- [ ] A.8 contains exactly 6 RQs (3 AS, 3 GDR)
- [ ] M-1, M-2, M-3 mandatory slots covered
- [ ] All 6 RQs have corresponding responses in data.zip
- [ ] RQ responses substantive (not "no results found")

---

### Phase 7: SC/INT Audit Quality

**7.1 SC Substantiveness**

For each SC output:
- [ ] A.11 findings are specific to this company (not generic boilerplate)
- [ ] Pipeline Fit grade assigned with reasoning
- [ ] execution_context populated

**7.2 INT Adjudication Completeness**

- [ ] Every SC finding has a disposition (Accept, Reject, Partial)
- [ ] Dispositions include reasoning
- [ ] Accepted findings reflected in model adjustments (if material)

**7.3 INT T3 Concatenation Integrity**

- [ ] T3 is assembly, not regeneration (text matches upstream sources)
- [ ] All sections present: ENRICH narratives, SCENARIO narratives, INT T1 adjudication, INT T2 A.12
- [ ] No truncation

---

## Output Format

**PASS:**
```
PIPELINE VALIDATOR: PASS

Summary:
- Files: {N} outputs validated
- Stages: BASE → RQ_GEN → RQ_ASK → ENRICH → SCENARIO → SC ({N} instances) → INT → IRR
- MRC States: 1 → 2 → 3 → 4 → 5 confirmed
- Final E[IRR]: {value}
- P(IRR > Hurdle): {value}

CVR ready for use.
```

**FAIL:**
```
PIPELINE VALIDATOR: FAIL

Critical Issues:
1. [Phase X.Y]: [Issue description]
   Location: [File/Artifact]
   Impact: [Why this matters]

Warnings:
1. [Phase X.Y]: [Issue description]

Required Fixes:
- [Specific action to remediate each critical issue]

Re-run affected stages before using CVR.
```

**PARTIAL PASS:**
```
PIPELINE VALIDATOR: PARTIAL PASS

Passed Phases: [list]
Failed Phases: [list]

Issues:
1. [Phase X.Y]: [Issue]

CVR usable with noted caveats:
- [Caveat 1]
```

---

## Notes

- This validator checks syntactic and structural integrity, not analytical quality
- Economic realism checks are sanity bounds, not investment recommendations
- For methodology audit, use HITL stage
- Reference README Section 2 (Stage-by-Stage Protocol) and Section 6 (Attachment Cheat Sheet) as canonical specification
