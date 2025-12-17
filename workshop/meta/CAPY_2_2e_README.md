# CAPY 2.2e Pipeline Execution Guide

This document is an operational guide for executing the CAPY 2.2e
pipeline in a browser-based LLM interface. It covers trigger commands,
required attachments, expected outputs, and common failure recovery.

## 1. Pipeline Overview

CAPY 2.2e is an 8-stage LLM-based fundamental valuation pipeline:

BASE → RQ_GEN → RQ_ASK (parallel) → ENRICH → SCENARIO → SC (parallel) →
INT → IRR

↓

PIPELINE VALIDATOR (required gate)

↓

HITL (optional)

↓

INT → IRR (reval)

### Why This Matters

-   Without file output instruction, models often dump content into
    > chat, causing formatting loss and copy/paste friction

-   Without concatenation mode instruction, INT T3 attempts to
    > regenerate \~50k tokens of upstream content, hits context limits,
    > and truncates

---

## 1.2 Mandatory Validation Protocol

**After every turn:** In the same conversation, attach `CAPY_VALIDATOR_2_2e.md` and type `/validate`. Require PASS before proceeding to next turn.

**After IRR T2 (before HITL handoff):** In a fresh conversation, run Pipeline Validator per Section 2.9.

| Validator | When | Where | Purpose |
|-----------|------|-------|---------|
| Turn Validator | After each turn | Same conversation | Catches input/output errors immediately |
| Pipeline Validator | After IRR T2, before HITL | Fresh conversation | Full CVR structural audit before handoff |

**Turn Validation (In-Conversation):**
1. In the same window where you just executed a turn
2. Attach `CAPY_VALIDATOR_2_2e.md`
3. Type: `/validate`
4. Require PASS before proceeding

**Why This Matters:** Human input errors are the primary failure mode. A wrong attachment caught immediately costs ~5 minutes. Discovered at IRR? You're debugging backwards through 8 stages.

---

## 2. Stage-by-Stage Execution Protocol

### 2.0 Document Sourcing (Pre-Pipeline)

Before initiating BASE, assemble the input corpus. Quality and
completeness of source documents directly determine pipeline output
quality.

#### Required Documents

  -----------------------------------------------------------------------
  **Document**            **Source Priority**     **Notes**
  ----------------------- ----------------------- -----------------------
  Most Recent 10-Q        AlphaSense              Current quarter
                                                  financials

  Most Recent 10-K        AlphaSense              Full-year financials,
                                                  business description,
                                                  risk factors

  Most Recent Investor    AlphaSense / IR site    Management\'s strategic
  Deck                                            framing

  Most Recent Earnings    AlphaSense              Q&A often surfaces
  Call Transcript                                 undisclosed concerns

  Material Press Releases AlphaSense / IR site    Any releases
                                                  post-dating latest
                                                  financials (M&A,
                                                  guidance changes,
                                                  executive departures,
                                                  etc.)
  -----------------------------------------------------------------------

#### Optional High-Value Documents

Depending on target complexity and recency of corporate events, consider
adding:

-   **Investor Day presentations** --- deep strategic context, long-term
    > guidance

-   **Proxy statement (DEF 14A)** --- compensation structure,
    > governance, insider ownership

-   **8-K filings** --- material events between quarterlies

-   **Analyst Day transcripts** --- if available and recent

-   **Credit agreements / bond prospectuses** --- for levered companies,
    > covenant details matter

#### Source Platform

Use **AlphaSense** as the primary source to ensure document authenticity
and version accuracy. IR websites are acceptable for investor decks and
press releases not yet indexed.

#### Pre-BASE Screen (LLM-Assisted)

Before proceeding to BASE T1, run a quick validation screen using any
capable LLM:

**Trigger:**

Review the attached document set for {Company Name}, {EXCHANGE:TICKER}.
Evaluate:

1\. COMPLETENESS: Do I have the minimum required inputs for fundamental
analysis (recent 10-K, recent 10-Q, recent transcript, investor deck)?

2\. STALENESS: Are there any gaps where material time has passed since
the most recent document? Flag if \>45 days since last earnings or if a
known catalyst has occurred.

3\. MISSING CONTEXT: Based on the documents provided, are there
references to material events, transactions, or disclosures I should
source separately (e.g., referenced acquisitions, divestitures,
refinancings, guidance revisions)?

4\. NEWS CHECK: \[Use web search\] Is there any material news in the
last 7 days that would affect the analysis?

Output a GO/NO-GO recommendation with specific gaps to fill if NO-GO.



**Attachments:** All sourced documents (zipped)

**Expected Output:** GO with confirmation of adequate coverage, or NO-GO
with specific sourcing instructions.

> ⚠️ Do NOT proceed to BASE with an incomplete document set. Garbage in,
> garbage out.

**Can Do Manually:** Look briefly through stock price and see if there
are big movements and see if there is a presser that is close to that

### 2.1 BASE (Three-Shot)

#### Turn 1: Analytical Synthesis

  -----------------------------------------------------------------------------
  **Field**                           **Value**
  ----------------------------------- -----------------------------------------
  **Trigger**                         Do Turn 1: {Company Name},
                                      {EXCHANGE:TICKER}, {As of DATE}

  **Attachments**                     G3BASE_2.2.1e.md, Company Documents
                                      (10-K, 10-Q, transcripts, presentations)

  **Output**                          {TICKER}\_BASE2.2.1eO_T1\_{YYYYMMDD}.md

  **Validation**                      JSON block present, Narratives I--IV
                                      present, no kernel execution
  -----------------------------------------------------------------------------

> ⚠️ Do NOT attach .py kernel on T1. The prompt contains kernel
> reference for semantic alignment.

#### REFINE: Calibration Review

  ---------------------------------------------------------------------------------
  **Field**                           **Value**
  ----------------------------------- ---------------------------------------------
  **Trigger**                         Do REFINE

  **Attachments**                     BASE_T1_REFINE_v1_0.docx, G3BASE_2.2.1e.md,
                                      Company Documents, BASE T1 Output

  **Output**                          {TICKER}\_BASE2.2.1eO_REFINE\_{YYYYMMDD}.md

  **Validation**                      A.1--A.6 present (corrected or validated), DR
                                      re-derivation documented, X divergence
                                      flagged if \>0.3
  ---------------------------------------------------------------------------------

**REFINE reviews:**

-   DAG business physics (revenue decomposition, cost structure, IC
    > accuracy)

-   Y0 calibration against source financials (within \~5%)

-   GIM trajectory realism vs. management guidance

-   Kernel compatibility

-   Independent DR re-derivation averaged with T1

> ⚠️ REFINE runs in fresh window. Do NOT attach kernel.

#### Turn 2: Validation & Execution

  -----------------------------------------------------------------------------
  **Field**                           **Value**
  ----------------------------------- -----------------------------------------
  **Trigger**                         Do Turn 2

  **Attachments**                     G3BASE_2.2.1e.md, REFINE Output,
                                      BASE_CVR_KERNEL_2.2.1e.py

  **Output**                          {TICKER}\_BASE2.2.1eO_T2\_{YYYYMMDD}.md

  **Validation**                      A.7 present with IVPS, kernel execution
                                      log clean, no stack traces
  -----------------------------------------------------------------------------

### 2.2 RQ_GEN (Single-Shot)

  ------------------------------------------------------------------------
  **Field**                           **Value**
  ----------------------------------- ------------------------------------
  **Trigger**                         Generate RQs for {Company Name},
                                      {EXCHANGE:TICKER}

  **Attachments**                     RQ_Gen_2.2.2e.docx, Complete BASE
                                      outputs (never original T1, unless
                                      it's missing something entirely in
                                      REFINE and T2 that needs to be
                                      stitched from T1)

  **Output**                          {TICKER}\_RQ2.2.2eO\_{YYYYMMDD}.md

  **Validation**                      A.8 present with exactly 6 RQs (3
                                      AS, 3 GDR), platform routing
                                      specified
  ------------------------------------------------------------------------

> **Complete BASE outputs** = REFINE output (A.1--A.6) + T2 output
> (A.7). If T2 consolidates everything, use T2 alone. If T2 only emits
> A.7, attach both REFINE and T2 (not original T1 unless criteria in
> table are met).

### 2.3 RQ_ASK (Parallel Execution)

Execute the 6 RQs generated in RQ_GEN on their designated platforms.
This stage runs in parallel across platforms.

  -----------------------------------------------------------------------
  **Platform**            **RQ Slots**            **Execution Method**
  ----------------------- ----------------------- -----------------------
  AlphaSense              AS-1, AS-2, AS-3        Generative AI → Deep
                                                  Research → supplement
                                                  with web search

  Gemini Deep Research    GDR-1, GDR-2, GDR-3     Deep Research mode
  -----------------------------------------------------------------------

**Execution Notes:**

-   Run all 6 RQs in parallel (no dependencies between them)

-   Capture full response output from each platform

**Output:** Compile all 6 RQ responses into a single research bundle for
ENRICH input. A bundle means copy paste into a google doc (make sure to
include question in Gem which just gives answer), and then download as a
.md file (call it something like RQ Compiled)

**Validation:** All 6 RQs answered, no platform failures, responses
substantive (not \"no results found\").

### 2.4 ENRICH (Two-Shot)

#### Turn 1: Analytical Synthesis

  -------------------------------------------------------------------------------
  **Field**                           **Value**
  ----------------------------------- -------------------------------------------
  **Trigger**                         Do Turn 1: ENRICHMENT for {Company Name},
                                      {EXCHANGE:TICKER}

  **Attachments**                     G3ENRICH_2.2.1e.md, Complete BASE outputs,
                                      Research Outputs (compiled RQ questions &
                                      responses)

  **Output**                          {TICKER}\_ENRICH2.2.1eO_T1\_{YYYYMMDD}.md

  **Validation**                      A.9 changelog present, GIM amendments
                                      documented
  -------------------------------------------------------------------------------

> ⚠️ Do NOT attach .py kernel on T1.

#### Turn 2: Validation & Execution

  -------------------------------------------------------------------------------
  **Field**                           **Value**
  ----------------------------------- -------------------------------------------
  **Trigger**                         Do Turn 2

  **Attachments**                     G3ENRICH_2.2.1e.md, T1 ENRICH Output,
                                      CVR_KERNEL_ENRICH_2.2.1e.py

  **Output**                          {TICKER}\_ENRICH2.2.1eO_T2\_{YYYYMMDD}.md

  **Validation**                      Updated A.7 with post-enrichment IVPS,
                                      kernel log clean
  -------------------------------------------------------------------------------

### 2.5 SCENARIO (Two-Shot)

#### Turn 1: Scenario Design

  -----------------------------------------------------------------------------
  **Field**                           **Value**
  ----------------------------------- -----------------------------------------
  **Trigger**                         Do Turn 1: SCENARIO for {Company Name},
                                      {EXCHANGE:TICKER}

  **Attachments**                     G3_SCENARIO_2_2_1e.md, Complete ENRICH
                                      outputs. (Maybe T2 contains T1 but maybe
                                      not so just see. It just means it has all
                                      narratives and artefacts)

  **Output**                          {TICKER}\_SCEN2.2.1eO_T1\_{YYYYMMDD}.md

  **Validation**                      4 scenarios defined (S1--S4) with P, M
                                      estimates, JSON parseable
  -----------------------------------------------------------------------------

> ⚠️ Do NOT attach .py kernel on T1.

#### Turn 2: Kernel Execution

  -----------------------------------------------------------------------------
  **Field**                           **Value**
  ----------------------------------- -----------------------------------------
  **Trigger**                         Do Turn 2

  **Attachments**                     G3_SCENARIO_2_2_1e.md, T1 Output,
                                      Complete ENRICH outputs,
                                      CVR_KERNEL_SCEN_2_2_1e.py

  **Output**                          {TICKER}\_SCEN2.2.1eO_T2\_{YYYYMMDD}.md

  **Validation**                      A.10 present with SSE, JPD, E\[IVPS\],
                                      distribution stats
  -----------------------------------------------------------------------------

### 2.6 SILICON COUNCIL (Single-Shot, Parallel)

The SC stage runs independently across multiple LLM instances for
adversarial diversity. SC operates on **epistemic parity** with
ENRICH/SCENARIO---it receives all context those stages had access to.

  -------------------------------------------------------------------------------
  **Field**                           **Value**
  ----------------------------------- -------------------------------------------
  **Trigger**                         Execute Silicon Council audit for {Company
                                      Name}, {EXCHANGE:TICKER}

  **Attachments**                     G3_SILICON_COUNCIL_2.2.1e.md, Financials
                                      bundle (.zip), RQ outputs (1--6), Complete
                                      ENRICH/SCENARIO outputs

  **Output**                          {TICKER}\_SC2.2.1eO\_{YYYYMMDD}\_{LLM}.md
                                      (e.g., \_G3PTR, \_C45ET, \_O3H)

  **Validation**                      A.11 present with findings, Pipeline Fit
                                      grade, execution_context populated
  -------------------------------------------------------------------------------

**Parallel Execution:** Run SC in 2--3 separate LLM instances (i.e.,
Claude 4.5 (extended thinking), Gem 3 Pro with deep think (OpenAI 5.2,
maybe)). Collect all A.11 outputs for INT.

#### Gemini Workaround (No .zip Support)

Gemini cannot receive .zip files. Use 10-slot allocation with SC prompt
in the prompt window (not attached):

  -----------------------------------------------------------------------
  **Slots**                           **Content**
  ----------------------------------- -----------------------------------
  2--4                                Complete ENRICH + Complete SCENARIO
                                      outputs

  1                                   RQ outputs (consolidated into
                                      single file)

  5--7                                Key financials: 10-K, 10-Q,
                                      transcript, investor deck, plus
                                      situational (8-K if material event,
                                      proxy if governance-relevant)
  -----------------------------------------------------------------------

Researcher judgment on which financials are highest-signal for the
specific target.

### 2.7 INTEGRATION (Three-Shot)

INT operates on **epistemic parity** with SC---it receives the same
context bundle plus all SC audit outputs.

#### Turn 1: Analytical Adjudication

  ----------------------------------------------------------------------------
  **Field**                           **Value**
  ----------------------------------- ----------------------------------------
  **Trigger**                         Do Turn 1: INTEGRATION for {Company
                                      Name}, {EXCHANGE:TICKER}

  **Attachments**                     G3_INTEGRATION_2_2_2e.md, Financials
                                      bundle (.zip), RQ outputs (1--6),
                                      Complete ENRICH/SCENARIO outputs, All SC
                                      outputs

  **Output**                          {TICKER}\_INT2.2.2eO_T1\_{YYYYMMDD}.md

  **Validation**                      Adjudication dispositions for all SC
                                      findings
  ----------------------------------------------------------------------------

> ⚠️ Do NOT attach .py kernel on T1.

#### Turn 2: Kernel Execution

  ----------------------------------------------------------------------------
  **Field**                           **Value**
  ----------------------------------- ----------------------------------------
  **Trigger**                         Do Turn 2

  **Attachments**                     G3_INTEGRATION_2_2_2e.md, T1 Output,
                                      Complete ENRICH/SCENARIO outputs,
                                      CVR_KERNEL_INT_2_2_2e.py

  **Output**                          {TICKER}\_INT2.2.2eO_T2\_{YYYYMMDD}.md

  **Validation**                      A.12 present, state_4_active_inputs
                                      populated, recalculations complete
  ----------------------------------------------------------------------------

#### Turn 3: Narrative Synthesis

  ----------------------------------------------------------------------------
  **Field**                           **Value**
  ----------------------------------- ----------------------------------------
  **Trigger**                         Do Turn 3

  **Attachments**                     G3_INTEGRATION_2_2_2e.md, INT T1 Output,
                                      INT T2 Output, Complete ENRICH outputs,
                                      Complete SCENARIO outputs

  **Output**                          {TICKER}\_INT2.2.2eO_T3\_{YYYYMMDD}.md

  **Validation**                      Complete CVR State 4 document, all
                                      narratives concatenated
  ----------------------------------------------------------------------------

### 2.8 IRR (Two-Shot)

#### Turn 1: Analytical

  ----------------------------------------------------------------------------
  **Field**                           **Value**
  ----------------------------------- ----------------------------------------
  **Trigger**                         Do Turn 1: IRR for {Company Name},
                                      {EXCHANGE:TICKER}

  **Attachments**                     G3_IRR_2.2.4e.md, Complete INT outputs

  **Output**                          {TICKER}\_IRR2.2.4eO_T1\_{YYYYMMDD}.md

  **Validation**                      A.13 present with CR derivation, τ
                                      estimates, multiple selection
  ----------------------------------------------------------------------------

> ⚠️ Do NOT attach .py kernel on T1.

#### Turn 2: Computational

  ----------------------------------------------------------------------------
  **Field**                           **Value**
  ----------------------------------- ----------------------------------------
  **Trigger**                         Do Turn 2

  **Attachments**                     G3_IRR_2.2.4e.md, T1 Output, Complete
                                      INT outputs, CVR_KERNEL_IRR_2.2.4e.py

  **Output**                          {TICKER}\_IRR2.2.4eO_T2\_{YYYYMMDD}.md

  **Validation**                      A.14 present with E\[IRR\], P(IRR \>
                                      Hurdle), entry price recommendations
  ----------------------------------------------------------------------------

### 2.9 Pipeline Validation (Pre-HITL Gate)

Run after completing IRR T2, before handoff to human auditors for HITL.

**Execution:** Fresh conversation (not the IRR conversation).

**Attachments:**
- `CAPY_PIPELINE_VALIDATOR_2_2e.md`
- `CAPY_2_2e_README_Clean.md`
- `prompts.zip` — All stage prompts and kernels used
- `data.zip` — Financials bundle, RQ outputs (1–6)
- `outputs.zip` — All pipeline outputs (BASE through IRR)
- `sc_audits.zip` — All SC outputs

**Trigger:** `/validate_pipeline {TICKER}`

**Gate:** PASS required before HITL handoff. FAIL requires remediation of cited issues.

---

### 2.10 HITL (Optional, Post-Pipeline-Validation Dialectic)

HITL provides human-in-the-loop adversarial audit after completing the
first pass through IRR. Findings feed back into a revalidation loop.

  -----------------------------------------------------------------------
  **Field**                           **Value**
  ----------------------------------- -----------------------------------
  **Trigger**                         HITL: BEGIN

  **Attachments**                     HITL_DIALECTIC_AUDIT_1_0.md,
                                      Complete INT outputs, Complete IRR
                                      outputs

  **Commands**                        /next (close argument), /done (end
                                      session), /status (score check)

  **Output**                          HITL audit JSON with scored
                                      findings

  **Validation**                      Final score tallied, audit record
                                      complete
  -----------------------------------------------------------------------

**Post-HITL Flow:** If HITL surfaces material findings requiring model
adjustment, re-run INT T1 → T2 → T3 incorporating HITL output as
additional SC-equivalent input, then proceed through IRR reval.

## 3. File Naming Conventions

**Pattern:** {TICKER}\_{STAGE}{VERSION}O_T{N}\_{YYYYMMDD}.md

  -------------------------------------------------------------------------
  **Stage**                           **Example Filename**
  ----------------------------------- -------------------------------------
  BASE T1                             DAVE_BASE2.2.1eO_T1_20251207.md

  BASE REFINE                         DAVE_BASE2.2.1eO_REFINE_20251207.md

  BASE T2                             DAVE_BASE2.2.1eO_T2_20251207.md

  RQ_GEN                              DAVE_RQ2.2.2eO_20251207.md

  ENRICH T1                           DAVE_ENRICH2.2.1eO_T1_20251208.md

  ENRICH T2                           DAVE_ENRICH2.2.1eO_T2_20251208.md

  SCENARIO T1                         DAVE_SCEN2.2.1eO_T1_20251208.md

  SCENARIO T2                         DAVE_SCEN2.2.1eO_T2_20251208.md

  SC                                  DAVE_SC2.2.1eO_20251208_C45ET.md

  INT T1                              DAVE_INT2.2.2eO_T1_20251209.md

  INT T2                              DAVE_INT2.2.2eO_T2_20251209.md

  INT T3                              DAVE_INT2.2.2eO_T3_20251209.md

  IRR T1                              DAVE_IRR2.2.4eO_T1_20251210.md

  IRR T2                              DAVE_IRR2.2.4eO_T2_20251210.md
  -------------------------------------------------------------------------

## 4. Common Failure Modes & Recovery

### 4.1 Attachment Errors

**Symptoms:** LLM asks clarifying questions, produces partial output,
references missing documents.

**Cause:** Forgot to attach prompt, kernel, or upstream output.

**Fix:** Re-run the turn with correct attachments. Use the validation
checklist below.

### 4.2 JSON Malformation

**Symptoms:** T2 reports parse errors, kernel fails to load artifacts.

**Cause:** Malformed brackets, unescaped quotes, truncated output.

**Fix:** T2 includes automatic JSON repair. If persistent, manually fix
bracket mismatches or quote escaping in T1 output, then re-run T2.

### 4.3 Kernel Execution Failure

**Symptoms:** Stack trace in output, A.7/A.10/A.14 missing or
incomplete.

**Common Causes:**

-   DAG node names don\'t match GIM keys

-   Y0 data missing for required drivers

-   Scenario intervention targets undefined nodes

**Fix:** Review error message, check DAG-GIM alignment in T1 output,
verify Y0 coverage in A.2. Repair T1 artifacts and re-run T2.

### 4.4 Context Exhaustion

**Symptoms:** Truncated output, incomplete artifacts, LLM mentions token
limits.

**Cause:** Input corpus too large for context window.

**Fix:** Reduce input corpus (prioritize 10-K, most recent 10-Q, 2--3
key transcripts). For very complex companies, split supplementary
materials across research questions rather than BASE input.

### 4.5 Wrong Upstream Output

**Symptoms:** LLM processes wrong company, references stale data,
artifacts inconsistent.

**Cause:** Attached T1 output from different company or outdated run.

**Fix:** Verify filename ticker and date before each turn. Re-run with
correct upstream file.

### 4.6 Chat Dialogue Instead of File Output

**Symptoms:** Model dumps output into chat window instead of creating
downloadable .md file.

**Cause:** Missing file output instruction in trigger.

**Fix:** Re-run with standard suffix: Output your complete response as a
downloadable .md file. Do not output in chat dialogue.

### 4.7 INT T3 Truncation

**Symptoms:** INT T3 output cuts off mid-document, missing sections,
model mentions token limits.

**Cause:** Model regenerates upstream content instead of copy/pasting,
exhausts context window.

**Fix:** Re-run T3 with concatenation mode suffix: CONCATENATION MODE:
Copy/paste upstream documents verbatim. Do NOT regenerate or rephrase
any text. Your job is assembly, not generation.

### 4.8 Fabrication (T1-Only Stages)

**Symptoms:** Numerical values in T1 that should only appear after
kernel execution.

**Cause:** LLM computed values instead of deferring to kernel.

**Fix:** Not critical if T2 executes kernel correctly (kernel overwrites
fabricated values). Monitor for consistency between T1 assertions and T2
kernel output.

## 5. Quality Checklist (Pre-Proceed)

Run this checklist after each turn before proceeding to the next stage.

### Universal Checks

-   Output file named correctly per convention

    > No LLM clarifying questions in output (indicates missing input)

    > No \"I don\'t have access to\...\" messages

### T1 Turns (Analytical)

-   All required narratives present

    > JSON block present and appears complete (opening/closing braces
    > match)

    > No kernel execution attempted

### T2 Turns (Execution)

-   Kernel execution log present

    > No stack traces or Python errors

    > Summary artifact present (A.7 for BASE/ENRICH, A.10 for SCENARIO,
    > A.12 for INT, A.14 for IRR)

    > IVPS/E\[IVPS\]/E\[IRR\] values are reasonable (positive, within
    > order of magnitude of price)

### Stage-Specific Checks

#### BASE REFINE

-   A.1--A.6 present (corrected or unchanged with validation notes)

    > DR re-derivation documented with X_T1, X_REFINE, X_final

    > X divergence flagged if \|X_REFINE - X_T1\| \> 0.3

    > DAG modifications documented if made

#### BASE T2

-   IVPS \> 0

    > DR between 8--20% (typical range)

    > Terminal g \< DR

#### RQ_GEN

-   Exactly 6 RQs

    > 3 AS + 3 GDR platform split

    > M-1, M-2, M-3 mandatory slots covered

#### SCENARIO T2

-   4 scenarios defined

    > Probabilities sum to 1 (within rounding)

    > E\[IVPS\] reasonable relative to base case

#### SC (each instance)

-   A.11 present with findings

    > Pipeline Fit grade assigned

    > execution_context populated

    > Findings are substantive (not generic boilerplate)

#### INT T3

-   All adjudication dispositions documented

    > State 4 E\[IVPS\] present

    > CVR State 4 Bundle in T2 output

#### IRR T2

-   E\[IRR\] present

    > P(IRR \> Hurdle) calculated

    > Entry price recommendation present

## 6. Quick Reference: Attachment Cheat Sheet

  -------------------------------------------------------------------------------------------------------
  **Stage**   **Turn**    **Prompt**                     **Upstream        **Kernel**   **Other**
                                                         Output**                       
  ----------- ----------- ------------------------------ ----------------- ------------ -----------------
  BASE        T1          G3BASE_2.2.1e.md               ---               ---          Company docs

  BASE        REFINE      BASE_T1_REFINE_v1_0.docx,      BASE T1           ---          Company docs
                          G3BASE_2.2.1e.md                                              

  BASE        T2          G3BASE_2.2.1e.md               REFINE            ✓ Execute    ---

  RQ_GEN      ---         RQ_Gen_2.2.2e.docx             Complete BASE     ---          ---
                                                         outputs                        

  RQ_ASK      ---         ---                            A.8 (RQs)         ---          AlphaSense,
                                                                                        Gemini DR

  ENRICH      T1          G3ENRICH_2.2.1e.md             Complete BASE     ---          A.8, Research
                                                         outputs                        bundle

  ENRICH      T2          G3ENRICH_2.2.1e.md             ENRICH T1         ✓ Execute    ---

  SCENARIO    T1          G3_SCENARIO_2_2_1e.md          Complete ENRICH   ---          ---
                                                         outputs                        

  SCENARIO    T2          G3_SCENARIO_2_2_1e.md          SCEN T1           ✓ Execute    Complete ENRICH
                                                                                        outputs (fresh)

  SC          ---         G3_SILICON_COUNCIL_2.2.1e.md   Complete          ---          Financials bundle
                                                         ENRICH/SCENARIO                (.zip), RQ
                                                         outputs                        outputs

  INT         T1          G3_INTEGRATION_2_2_2e.md       Complete          ---          Financials
                                                         ENRICH/SCENARIO                bundle, RQ
                                                         outputs                        outputs, All SC
                                                                                        outputs

  INT         T2          G3_INTEGRATION_2_2_2e.md       INT T1            ✓ Execute    Complete
                                                                                        ENRICH/SCENARIO
                                                                                        outputs (fresh)

  INT         T3          G3_INTEGRATION_2_2_2e.md       INT T1, INT T2    ---          Complete ENRICH
                                                                                        outputs, Complete
                                                                                        SCENARIO outputs

  IRR         T1          G3_IRR_2.2.4e.md               Complete INT      ---          ---
                                                         outputs                        

  IRR         T2          G3_IRR_2.2.4e.md               IRR T1            ✓ Execute    Complete INT
                                                                                        outputs (fresh)

  PIPELINE    ---         CAPY_PIPELINE_VALIDATOR_2_2e.md, Complete IRR   ---          prompts.zip,
  VALIDATOR               CAPY_2_2e_README_Clean.md      outputs                        data.zip,
                                                                                        outputs.zip,
                                                                                        sc_audits.zip

  HITL        ---         HITL_DIALECTIC_AUDIT_1_0.md    Complete INT      ---          (optional)
                                                         outputs, Complete              
                                                         IRR outputs                    
  -------------------------------------------------------------------------------------------------------

**Legend:**

-   **✓ Execute** = Attach .py kernel file this turn for execution

-   **(fresh)** = Re-attach for clean context even though data is in
    > prior turn output

-   **T1 turns:** Kernel reference is embedded in the prompt; do NOT
    > attach .py file (LLM will attempt execution)
