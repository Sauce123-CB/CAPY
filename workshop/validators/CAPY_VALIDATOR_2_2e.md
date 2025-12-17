# CAPY 2.2e Turn Validator

Run after any pipeline turn to validate before proceeding. Catches human input errors—the primary failure mode.

---

## Usage

In the same conversation where you just executed a turn:

1. Attach this prompt
2. Type: `/validate`

Claude will automatically check the turn output and attachments from the current conversation.

---

## Validation Protocol

When you see `/validate`, execute all phases below against the turn just completed in this conversation.

### Phase 1: Input Verification (CRITICAL)

Check what the human attached for the turn just executed:

**Verify:**
- Correct prompt file for this stage?
- Required upstream output(s) present?
- Kernel .py attached? (T2 only—flag if attached on T1 or REFINE)
- Filename consistency? (ticker, date, stage all match across attachments)

**Required Inputs by Stage:**

| Stage | Turn | Required |
|-------|------|----------|
| BASE | T1 | Prompt (G3BASE_2.2.1e.md), Company docs |
| BASE | REFINE | REFINE prompt (BASE_T1_REFINE_v1_0.docx), BASE prompt (G3BASE_2.2.1e.md), Company docs, BASE T1 |
| BASE | T2 | Prompt (G3BASE_2.2.1e.md), REFINE output (not T1), Kernel |
| RQ_GEN | — | Prompt (RQ_Gen_2.2.2e.docx), Complete BASE outputs |
| RQ_ASK | — | A.8 (RQs), AlphaSense, Gemini DR |
| ENRICH | T1 | Prompt (G3ENRICH_2.2.1e.md), Complete BASE outputs, A.8, Research bundle |
| ENRICH | T2 | Prompt (G3ENRICH_2.2.1e.md), ENRICH T1, Kernel |
| SCENARIO | T1 | Prompt (G3_SCENARIO_2_2_1e.md), Complete ENRICH outputs |
| SCENARIO | T2 | Prompt (G3_SCENARIO_2_2_1e.md), SCEN T1, Complete ENRICH outputs (fresh), Kernel |
| SC | — | Prompt (G3_SILICON_COUNCIL_2.2.1e.md), Financials bundle (.zip), RQ outputs (1–6), Complete ENRICH/SCENARIO outputs |
| INT | T1 | Prompt (G3_INTEGRATION_2_2_2e.md), Financials bundle, RQ outputs (1–6), Complete ENRICH/SCENARIO outputs, All SC outputs |
| INT | T2 | Prompt (G3_INTEGRATION_2_2_2e.md), INT T1, Complete ENRICH/SCENARIO outputs (fresh), Kernel |
| INT | T3 | Prompt (G3_INTEGRATION_2_2_2e.md), INT T1, INT T2, Complete ENRICH outputs, Complete SCENARIO outputs |
| IRR | T1 | Prompt (G3_IRR_2.2.4e.md), Complete INT outputs |
| IRR | T2 | Prompt (G3_IRR_2.2.4e.md), IRR T1, Complete INT outputs (fresh), Kernel |
| HITL | — | Prompt (HITL_DIALECTIC_AUDIT_1_0.md), Complete INT outputs, Complete IRR outputs |

**"Complete BASE outputs"** = REFINE output (A.1–A.6) + T2 output (A.7). If T2 consolidates everything, use T2 alone. If T2 only emits A.7, attach both REFINE and T2 (not original T1 unless needed for something missing from REFINE/T2).

**"Complete X outputs"** = All turns from that stage bundled. If final turn consolidates everything, use that alone. If not, attach all turn outputs.

---

### Phase 2: Output Completeness

Check the output just produced:

- File emitted as .md (not chat dialogue)?
- Named per convention? (`{TICKER}_{STAGE}{VERSION}O_T{N}_{YYYYMMDD}.md`)
- Required artifacts present?

| Stage Output | Required Artifacts |
|--------------|-------------------|
| BASE T1 | A.1, A.2, A.3, A.5, A.6 |
| BASE REFINE | A.1–A.6 (corrected or validated), DR re-derivation with X_T1, X_REFINE, X_final |
| BASE T2 | A.1–A.7 |
| RQ_GEN | A.8 (exactly 6 RQs: 3 AS, 3 GDR) |
| RQ_ASK | 6 research responses compiled |
| ENRICH T1 | A.9 changelog, GIM amendments documented |
| ENRICH T2 | Updated A.7 with post-enrichment IVPS |
| SCENARIO T1 | 4 scenarios (S1–S4) with P, M estimates |
| SCENARIO T2 | A.10 with SSE, JPD, E[IVPS], distribution stats |
| SC | A.11 with findings, Pipeline Fit grade, execution_context |
| INT T1 | Adjudication dispositions for all SC findings |
| INT T2 | A.12 present, state_4_active_inputs populated |
| INT T3 | Complete CVR State 4 (all narratives concatenated) |
| IRR T1 | A.13 with CR derivation, τ estimates, multiple selection |
| IRR T2 | A.14 with E[IRR], P(IRR > Hurdle), entry price recommendations |

- JSON parseable (brackets match)?

---

### Phase 3: Execution Success (T2 Only)

For T2 turns, check:

- Kernel execution log present?
- No stack traces or Python errors?
- Summary artifact populated?
  - BASE T2: A.7 with IVPS
  - ENRICH T2: Updated A.7 with post-enrichment IVPS
  - SCENARIO T2: A.10 with E[IVPS], SSE, JPD, distribution stats
  - INT T2: A.12 with State 4 E[IVPS], state_4_active_inputs
  - IRR T2: A.14 with E[IRR], P(IRR > Hurdle)

---

### Phase 4: Sanity Bounds

Quick reasonableness (not analytical audit):

- IVPS > 0
- DR between 8–20% (typical range)
- Terminal g < DR
- Scenario probabilities sum ≈ 1.0 (within rounding)
- E[IRR] between -50% and +100%

---

### Phase 5: Stage-Specific Checks

#### BASE REFINE
- DR re-derivation documented with X_T1, X_REFINE, X_final?
- X_final = (X_T1 + X_REFINE) / 2?
- X divergence flagged if |X_REFINE - X_T1| > 0.3?
- DAG modifications documented if made?
- Y0 calibration confirmed within ~5% of source financials?

#### RQ_GEN
- Exactly 6 RQs?
- 3 AS + 3 GDR platform split?
- M-1, M-2, M-3 mandatory slots covered?

#### SC
- execution_context populated?
- Findings substantive (not generic boilerplate)?
- Pipeline Fit grade assigned with reasoning?

#### INT T3
- All narratives concatenated (not regenerated)?
- No truncation?
- All sections present: ENRICH narratives, SCENARIO narratives, INT T1 adjudication, INT T2 A.12?

---

## Output Format

**PASS:**
```
VALIDATOR: PASS
Ready to proceed to {next stage/turn}.
```

**FAIL:**
```
VALIDATOR: FAIL

Issues:
1. [Phase]: [Issue]

Fix:
- [Action]
```
