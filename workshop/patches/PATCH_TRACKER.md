# CAPY 2.2.3e Patch Tracker

Last updated: 2024-12-21

## Summary

| Status | Count |
|--------|-------|
| Complete | 18 |
| Pending | 10 |
| **Total** | **28** |

**Completion: 64%**

---

## Pipeline Smoke Test Status

| Stage | Status | Smoke Test Folder | Notes |
|-------|--------|-------------------|-------|
| BASE | ✅ Complete | `DAVE_20241214/` | Full T1→REFINE→T2 |
| RQ | ✅ Complete | `DAVE_RQ_CLAUDE_TEST/` | 7-slot with Claude Opus subagents |
| ENRICH | ✅ Complete | `DAVE_ENRICH_SMOKE_20251220_120936/` | State 1→2: $241.72→$199.25 |
| SCENARIO | ✅ Complete | `DAVE_ENRICH_SMOKE_20251220_120936/06_SCENARIO/` | E[IVPS]=$206.34, 4 scenarios, SSE 16 states |
| SILICON COUNCIL | ✅ Complete | `DAVE_ENRICH_SMOKE_20251220_120936/07_SILICON_COUNCIL/` | 6 parallel audits, A11 consolidated, prompts CANONICAL |
| INTEGRATION | ✅ Complete | `DAVE_ENRICH_SMOKE_20251220_120936/08_INTEGRATION/` | Prompts CANONICAL, E[IVPS]=$206.34, cascade=NONE, kernel verified |
| IRR | ⏳ Pending | - | Final stage |

**Goal:** Full autonomous CAPY (all stages chain without human intervention)

---

## Completed Patches

| # | Item | Type | Deliverable |
|---|------|------|-------------|
| 0 | PDF extraction skill | Infrastructure | `.claude/skills/pdf-processor/` |
| 8 | Claude Code orchestrator | Orchestrator | `CLAUDE.md` |
| 9 | Smoke test (DAVE) | Testing | `smoke_tests/DAVE_20241214/` |
| 13 | Folder organization | Infrastructure | Three-folder architecture |
| 14 | Inter-turn validator | Validation | Spec in CLAUDE.md (prompt NOT written) |
| 21 | SCENARIO smoke test (DAVE) | Testing | `DAVE_ENRICH_SMOKE_20251220_120936/06_SCENARIO/` |
| 22 | Validator model guidance | Orchestrator | CLAUDE.md (ALWAYS use Opus) |
| 23 | Acquisition premium lump sum | Prompt | G3_SCENARIO_2.2.2e_PROMPT.md |
| 24 | Silicon Council atomization | Prompt | G3_SC_2.2.2e_*.md (10 files) |
| 25 | SC smoke test + State 2/3 fix | Testing | `DAVE_ENRICH_SMOKE_20251220/07_SILICON_COUNCIL/` |
| 26 | Pattern 11 Surgical Stitching | Orchestrator | `ORCHESTRATION_KEY_PATTERNS.md` |
| 27 | INTEGRATION atomization + orchestration | Prompt | `G3_INTEGRATION_2.2.2e_*.md` (3 files) + CLAUDE.md Stage Flow |
| 28 | INTEGRATION validators | Validation | `INT_T1_VALIDATOR.md`, `INT_T2_VALIDATOR.md`, `INT_T3_VALIDATOR.md` |
| 29 | INT 2.2.3e deterministic handoff | Prompt | `G3_INTEGRATION_2.2.3e_PROMPT.md` - surgical edit mandate, kernel execution |
| 30 | **INTEGRATION smoke test** | Testing | `DAVE_ENRICH_SMOKE_20251220_120936/08_INTEGRATION/` |

---

## Pending Patches

| # | Item | Complexity | Type | Target Files |
|---|------|------------|------|--------------|
| 17 | **G3BASE atomization** (split into 4 files) | **High** | Prompt | G3BASE |
| 16 | Trajectory calibration + schema enforcement | **High** | Prompt | REFINE, G3BASE |
| 1 | T1+T2 KG handshake | Medium | Prompt | G3BASE, REFINE |
| 2 | Terminal ROIC bug | **High** | Kernel | All kernels (lines ~400-445) |
| 3 | REFINE DAG cap 12-15 | Low | Prompt | REFINE |
| 4 | Currency guidance | Low | Prompt | G3BASE, README |
| 5 | Loosen ROIC/IC language | Low | Prompt | G3BASE Phase B |
| 6 | Output requirements for speed | Medium | Prompt | All G3 prompts |
| 7 | Streamline prompts (remove embedded code) | Medium | Prompt | **Addressed by #17** |
| 10 | Schema conformance (exact JSON templates) | Medium | Prompt | G3BASE |
| 11 | Sensitivity analysis bug | **High** | Kernel | All kernels (line ~602) |
| 12 | Market price lookup (WebSearch) | Low | Prompt | CLAUDE.md, G3BASE |

---

## Blocking Issues (Kernel Bugs)

These require kernel code changes before prompts will work correctly:

1. **#2 Terminal ROIC bug** - IC scaling formula produces 80% ROIC vs 38% target
2. **#11 Sensitivity analysis bug** - IVPS values not centered on base case

---

## By Type

| Type | Done | Pending |
|------|------|---------|
| Infrastructure/Skills | 2 | 0 |
| Orchestrator | 2 | 0 |
| Validation | 1 (spec only) | 0 |
| Prompt patches | 0 | 7 |
| Kernel patches | 0 | 2 |
| Testing | 1 | 0 |

---

## Patch Application Log

| Date | Patch # | Applied By | Result | Notes |
|------|---------|------------|--------|-------|
| 2024-12-23 | 31 | Claude | Success | Kernel CLI wrappers (all 5 kernels) |
| 2024-12-14 | 8 | Initial | Success | CLAUDE.md created |
| 2024-12-14 | 9 | Initial | Success | DAVE smoke test complete |
| 2024-12-15 | 13 | Initial | Success | Three-folder architecture |
| 2024-12-18 | N/A | Claude | Success | RQ_GEN 6×GDR routing + Gemini CLI setup |
| 2024-12-19 | 18 | Claude | Success | RQ 7-slot architecture (M-3a/M-3b split) |
| 2024-12-19 | 19 | Claude | Success | Claude Opus subagent RQ_ASK + direct-write protocol |
| 2024-12-20 | 20 | Claude | Success | ENRICH smoke test + Pattern 10/11 orchestration fixes |
| 2024-12-20 | 21 | Claude | Success | Direct-write protocol documentation across all stages |
| 2024-12-20 | 25 | Claude | Success | SC smoke test, State 2/3 semantic fix, prompts→CANONICAL |
| 2024-12-20 | 26 | Claude | Success | Pattern 11 Surgical Stitching + Markdown generation default |
| 2024-12-20 | 27 | Claude | Success | INTEGRATION atomized (3 files) + full Stage Flow orchestration docs |
| 2024-12-20 | 28 | Claude | Success | INT T1/T2/T3 validators created, CLAUDE.md Current Versions updated |
| 2024-12-21 | 29 | Claude | Success | INT 2.2.2e→2.2.3e: Deterministic T1→T2 handoff, surgical edit mandate, kernel execution mandate |
| 2024-12-21 | 30 | Claude | Success | INTEGRATION smoke test complete, prompts→CANONICAL, kernel verified |
| | | | | |

---

## How to Apply a Patch

1. Read patch details in `CAPY_2.2.2e_Patch_Details.md`
2. Use `DEV: APPLY PATCH {N}` command
3. Update this tracker with result
4. Run smoke test to validate
5. If passing, mark new version as CANONICAL

---

## PATCH-2024-12-16-001: Trajectory Calibration & Schema Enforcement (#16)

**Date:** 2024-12-16
**Source:** BASE_PIPELINE smoke test (DAVE) in CAPY_Production
**Status:** PENDING

### Problem Statement

REFINE prompt produces DAG/GIM artifacts that:
1. Use wrong JSON keys (`nodes` instead of `DAG`, `drivers` instead of `GIM`)
2. Emit empty `coverage_manifest`
3. Use multi-period GIM format kernel doesn't support
4. Have unit inconsistencies causing cascade failures in kernel
5. Have no validation that simulated trajectories produce plausible financials

### Patches Required

| ID | File | Change | Priority |
|----|------|--------|----------|
| P1 | BASE_T1_REFINE_v1_1.md → v1_2.md | Add Section 2.5 Trajectory Calibration | HIGH |
| P2 | BASE_T1_REFINE_v1_2.md | Add kernel schema requirements | HIGH |
| P3 | G3BASE_2.2.1e.md → 2.2.2e.md | Add unit conventions | MEDIUM (deferred) |
| P4 | G3BASE_2.2.2e.md | Add schema examples to artifact specs | MEDIUM (deferred) |
| P5 | CAPY_INTERTURN_VALIDATOR_CC.md | Add T2-specific checks | LOW |

### Evidence

- `CAPY_Production/analyses/DAVE_CAPY_20251207_113714/03_T2/DAVE_kernel_output.json` shows garbage financials
- `CAPY_Production/WORKSHOP_HANDOFF_20241216.md` has full details

### Acceptance Criteria

- [ ] Fresh DAVE smoke test passes T2 with plausible IVPS
- [ ] No schema repair step needed between REFINE and kernel
- [ ] Trajectory calibration catches implausible metrics before kernel execution

---

## PATCH-2024-12-17-001: G3BASE Atomization (#17)

**Date:** 2024-12-17
**Source:** Context loss observed in subagent execution
**Status:** PENDING

### Problem Statement

G3BASE_2.2.1e.md is ~2300 lines including:
- Core prompt (~900 lines)
- Appendix A: Schemas (~400 lines)
- Appendix B: Normative Definitions (~600 lines)
- Appendix C: Python Kernel (~400 lines) - REDUNDANT with .py file

When this monolithic file is loaded into a subagent:
1. LLM attention is diluted across massive context
2. Appendix C duplicates the kernel that already exists as a .py file
3. Schema definitions get lost in the middle of the prompt
4. Format corruption and schema drift occur in outputs

### Solution: Split into 4 Atomic Files

| File | Content | Est. Lines |
|------|---------|------------|
| `G3BASE_2.2.2e_PROMPT.md` | Core instructions only (Sections 1-4) | ~900 |
| `G3BASE_2.2.2e_SCHEMAS.md` | Appendix A: JSON schemas | ~400 |
| `G3BASE_2.2.2e_NORMDEFS.md` | Appendix B: Normative definitions | ~600 |
| `BASE_CVR_KERNEL_2.2.2e.py` | Python kernel (already exists) | ~400 |

### Orchestration Change

Subagent prompt loading changes from:
```
Load: G3BASE_2.2.1e.md (monolithic)
```
To:
```
Load: G3BASE_2.2.2e_PROMPT.md
Load: G3BASE_2.2.2e_SCHEMAS.md
Load: G3BASE_2.2.2e_NORMDEFS.md
Reference: BASE_CVR_KERNEL_2.2.2e.py (for execution, not reading into prompt)
```

### Files to Create

1. `prompts/base/G3BASE_2.2.2e_PROMPT.md` - Extract Sections 1-4
2. `prompts/base/G3BASE_2.2.2e_SCHEMAS.md` - Extract Appendix A
3. `prompts/base/G3BASE_2.2.2e_NORMDEFS.md` - Extract Appendix B
4. Keep `kernels/BASE_CVR_KERNEL_2.2.1e.py` → rename to 2.2.2e

### Files to Archive

- `prompts/base/G3BASE_2.2.1e.md` → `CAPY_Archive/prompts/base/`

### Acceptance Criteria

- [ ] All 4 files created and internally consistent
- [ ] No content lost in split
- [ ] Appendix C (embedded kernel) removed entirely
- [ ] CLAUDE.md updated with new file structure
- [ ] Production CLAUDE.md orchestration updated
- [ ] Smoke test passes with atomized structure

---

## PATCH-2024-12-19-001: RQ 7-Slot Architecture (#18)

**Date:** 2024-12-19
**Source:** DAVE RQ Claude smoke test evaluation
**Status:** COMPLETE

### Problem Statement

The 6-slot RQ architecture with consolidated M-3 (Scenario H.A.D.) was producing incomplete scenario coverage:
1. M-3 covered only 4-5 scenarios in a single query
2. BNPL product launch scenario was missed for DAVE
3. Single consolidated query was 40KB (longest output), still incomplete
4. SCENARIO stage requires 8 scenarios to select top 4 for modeling

### Solution: Expand to 7 Slots with M-3 Split

**Before (v2.2.2):**
- 6 RQ slots: M-1, M-2, M-3, D-1, D-2, D-3
- M-3 covered 2-3 mainline + 1-2 tail (4-5 total)
- Single consolidated scenario query

**After (v2.2.3):**
- 7 RQ slots: M-1, M-2, M-3a, M-3b, D-1, D-2, D-3
- M-3a: 4 mainline scenarios (products, M&A, regulatory, strategy)
- M-3b: 4 tail scenarios (2 Blue Sky + 2 Black Swan)
- 8 total scenarios researched

### Files Modified

| File | Change |
|------|--------|
| `orchestration/RQ_Gen_2_2_3e.md` | New file - 7-slot spec with M-3a/M-3b |
| `validators/A8_VALIDATOR.md` | Updated count validation (6→7), added Scenario_Candidates check |
| `kernels/RQ_ASK_KERNEL_2_2_3e.py` | Renamed, updated MAX_CONCURRENT to 7 |
| `workshop/CLAUDE.md` | Updated RQ Stage section with 7-slot architecture |

### Additional Fix: Subagent Direct-Write Protocol

To eliminate orchestrator transcription bottleneck (which took 3-6x longer than research):
- Subagents now write output directly to disk
- Subagent prompt includes output path
- Orchestrator only verifies files exist

### Evidence

- `smoke_tests/DAVE_RQ_CLAUDE_TEST/` - 6 parallel Claude Opus subagents executed successfully
- RQ3 (scenarios) was 40KB but still missed BNPL launch scenario
- Transcription took ~15 minutes vs ~4 minutes for research execution

### Acceptance Criteria

- [x] RQ_Gen_2_2_3e.md created with 7-slot spec
- [x] A8_VALIDATOR.md updated for 7 RQs, M-3a/M-3b, Scenario_Candidates
- [x] RQ_ASK_KERNEL renamed and updated
- [x] workshop/CLAUDE.md updated with new architecture
- [x] Direct-write protocol documented
- [ ] Smoke test with 7-slot architecture (pending next run)

---

## PATCH-2024-12-19-002: Claude Opus Subagent RQ_ASK Implementation

**Date:** 2024-12-19
**Source:** DAVE RQ Claude smoke test (successful execution)
**Status:** COMPLETE (pending commit)

### Summary

Successfully implemented and tested Claude Opus subagents as the primary execution engine for RQ_ASK stage, replacing/complementing Gemini Deep Research. This enables parallel research execution with direct file output, eliminating the orchestrator transcription bottleneck.

### What Was Built

**1. Claude Opus Subagent Execution Pattern**

The orchestrator launches 7 parallel Task subagents (type: `general-purpose`) with:
- WebSearch and WebFetch tool permissions
- Explicit output path for direct-write
- Research query from A.8 Research Plan
- CLAUDE_DEEP_RESEARCH_WRAPPER prompt template

**2. Execution Flow**
```
Orchestrator                           7 Parallel Subagents
    │                                        │
    ├──► Task(RQ1, output_path)  ──────────► WebSearch → Write → Return filepath
    ├──► Task(RQ2, output_path)  ──────────► WebSearch → Write → Return filepath
    ├──► Task(RQ3, output_path)  ──────────► WebSearch → Write → Return filepath
    ├──► Task(RQ4, output_path)  ──────────► WebSearch → Write → Return filepath
    ├──► Task(RQ5, output_path)  ──────────► WebSearch → Write → Return filepath
    ├──► Task(RQ6, output_path)  ──────────► WebSearch → Write → Return filepath
    └──► Task(RQ7, output_path)  ──────────► WebSearch → Write → Return filepath
                                              │
    ◄──────────── TaskOutput (all 7) ─────────┘
                                              │
    Verify files exist ◄──────────────────────┘
    Report to user
```

**3. Key Innovation: Direct-Write Protocol**

Problem: In initial smoke test, orchestrator had to transcribe 43,000 words from subagent memory to files, taking 3-6x longer than the research itself.

Solution: Subagents write their own output to disk before returning.

Subagent prompt includes:
```
After completing your research, use the Write tool to save your report to:
{output_dir}/RQ{N}_{topic}.md

Return only a confirmation with the filepath.
```

### Files Created/Modified

| File | Type | Change |
|------|------|--------|
| `orchestration/RQ_Gen_2_2_3e.md` | Created | 7-slot RQ generation prompt |
| `kernels/RQ_ASK_KERNEL_2_2_3e.py` | Renamed/Updated | Added Claude executor, MAX_CONCURRENT=7 |
| `validators/A8_VALIDATOR.md` | Updated | 7 RQs, M-3a/M-3b, Scenario_Candidates |
| `validators/CAPY_VALIDATOR_2_2e.md` | Updated | 7 RQs, M-3a/M-3b checks |
| `validators/CAPY_INTERTURN_VALIDATOR_CC.md` | Updated | 7 RQs in artifacts table |
| `validators/CAPY_PIPELINE_VALIDATOR_2_2e.md` | Updated | 7 RQs, RQ outputs (1-7) |
| `workshop/CLAUDE.md` | Updated | v0.6.0, 7-slot architecture, direct-write protocol |
| `smoke_tests/DAVE_RQ_CLAUDE_TEST/` | Created | 6 research reports + summary JSON |

### Smoke Test Results (DAVE_RQ_CLAUDE_TEST)

**Execution Metrics:**
- 6 parallel Claude Opus subagents (7-slot not yet tested)
- Wall-clock time: ~4 minutes for research execution
- Total output: ~43,000 words across 6 reports
- All 6 tasks completed successfully

**Output Files:**
| File | Size | Coverage |
|------|------|----------|
| RQ1_Accounting_Governance.md | 21KB | M-1 Integrity Check |
| RQ2_Bull_Bear_Arguments.md | 26KB | M-2 Adversarial Synthesis |
| RQ3_Historical_Precedents.md | 40KB | M-3 Scenario H.A.D. |
| RQ4_Growth_TAM.md | 8KB | L1 Growth/TAM |
| RQ5_Unit_Economics_Credit.md | 12KB | L2 Unit Economics |
| RQ6_Competitive_Dynamics.md | 13KB | L3 Competitive Dynamics |
| A9_RESEARCH_RESULTS_DAVE_CLAUDE_20251219.json | 8KB | Summary metadata |

**Quality Assessment:**
- Research reports are detailed, well-cited, comprehensive
- Citations include dates and source types
- Structural consistency across reports
- One gap identified: BNPL product launch scenario missing (fixed by M-3 split)

### Dependencies and Integration Points

**1. Claude Code Permissions**

The following must be pre-approved in Claude Code settings or the user will be prompted:
- `WebSearch` - for research queries
- `WebFetch` - for fetching specific URLs
- `Write` - for direct output to disk

**2. Orchestrator Protocol**

When launching RQ_ASK via Claude subagents, the orchestrator must:
1. Create output directory: `{analysis_dir}/04_RQ/` or `smoke_tests/{test_name}/`
2. Launch 7 parallel Task calls with `subagent_type: "general-purpose"`
3. Include output path in each subagent prompt
4. Use `run_in_background: true` for parallel execution
5. Retrieve results via `TaskOutput` (blocking or polling)
6. Verify output files exist
7. Generate A.9 summary JSON

**3. Prompt Template (CLAUDE_DEEP_RESEARCH_WRAPPER)**

Located in `kernels/RQ_ASK_KERNEL_2_2_3e.py` lines 78-122:
```python
CLAUDE_DEEP_RESEARCH_WRAPPER = """You are a Deep Research Agent...

CITATION REQUIREMENTS:
- Every factual claim MUST include an inline citation
- Use format: [Source Name, Date] or [SEC Filing Type, Date]
...

OUTPUT STRUCTURE:
## Executive Summary
## Detailed Findings
## Key Uncertainties
## Sources

RESEARCH QUESTION:
{query}"""
```

**4. A.9 Output Schema**

The orchestrator generates A.9_RESEARCH_RESULTS with:
```json
{
  "ticker": "DAVE",
  "execution_timestamp": "ISO-8601",
  "executor": "claude",
  "total_queries": 7,
  "successful_queries": 7,
  "results": [
    {
      "rq_id": "RQ1",
      "status": "SUCCESS",
      "coverage_objective": "M-1 Integrity Check",
      "output_file": "RQ1_Accounting_Governance.md",
      "word_count": 5800
    }
  ]
}
```

### Known Limitations

1. **Write Tool Quirk:** For new files, Write tool sometimes requires a Read first (encountered during transcription). Direct subagent writes don't have this issue.

2. **No Automatic Retry:** If a subagent fails, no automatic retry logic exists yet. Orchestrator should check TaskOutput status and re-launch failed RQs.

3. **Output Path Must Be Absolute:** Subagents need absolute paths for Write tool.

4. **Citation Quality Varies:** Some subagents produce better citations than others. May need prompt refinement.

### Future Improvements

1. **Implement retry logic** for failed subagents
2. **Add streaming progress** - subagents could write incremental status
3. **Citation extraction** - parse SOURCES section into structured data
4. **Quality scoring** - automated assessment of research completeness

### Acceptance Criteria

- [x] Claude Opus subagents execute research queries successfully
- [x] Parallel execution works (6 confirmed, 7 expected)
- [x] Direct-write protocol eliminates transcription bottleneck
- [x] Research output quality meets standards (detailed, cited, comprehensive)
- [x] Integration documented in workshop/CLAUDE.md
- [x] All validators updated for 7-slot architecture
- [x] Smoke test evidence preserved in DAVE_RQ_CLAUDE_TEST/
- [ ] 7-slot smoke test with M-3a/M-3b split (next run)
- [ ] Production deployment (after 7-slot validation)

### Commit Checklist

Files to stage:
```
workshop/orchestration/RQ_Gen_2_2_3e.md           # NEW
workshop/kernels/RQ_ASK_KERNEL_2_2_3e.py          # RENAMED from 2_2_2e
workshop/validators/A8_VALIDATOR.md               # UPDATED
workshop/validators/CAPY_VALIDATOR_2_2e.md        # UPDATED
workshop/validators/CAPY_INTERTURN_VALIDATOR_CC.md # UPDATED
workshop/validators/CAPY_PIPELINE_VALIDATOR_2_2e.md # UPDATED
workshop/CLAUDE.md                                 # UPDATED
workshop/patches/PATCH_TRACKER.md                  # UPDATED
workshop/smoke_tests/DAVE_RQ_CLAUDE_TEST/          # NEW (test evidence)
```

Suggested commit message:
```
feat(RQ): implement Claude Opus subagent execution with 7-slot architecture

- Expand RQ slots from 6 to 7 (M-1, M-2, M-3a, M-3b, D-1, D-2, D-3)
- Split M-3 into M-3a (4 mainline) and M-3b (4 tail) for 8 total scenarios
- Add Claude Opus as primary RQ_ASK executor with WebSearch/WebFetch
- Implement direct-write protocol to eliminate orchestrator transcription
- Update all validators for 7-slot architecture
- Include DAVE smoke test evidence (6 parallel subagents, 43K words)

Closes #18
```

---

## PATCH-2024-12-21-001: INT 2.2.3e Deterministic Handoff Architecture (#29)

**Date:** 2024-12-21
**Source:** INT smoke test failure (kernel did not execute - T2 simulated calculations manually)
**Status:** COMPLETE

### Problem Statement

INT smoke test for DAVE revealed:
1. Kernel did NOT execute - T2 subagent performed manual calculations instead
2. Root cause: T1→T2 handoff was non-deterministic (T2 had to re-interpret changes)
3. Orchestrator included unauthorized escape clause allowing manual calculation
4. No explicit Bash command template was provided

### Solution: Deterministic Handoff Architecture

**Before (2.2.2e):**
- T1 outputs adjudication JSON only
- T2 re-ingests full epistemic bundle + interprets what to change
- T2 "may" execute kernel (ambiguous)

**After (2.2.3e):**
- T1 outputs COMPLETE, EDITED artifacts (A.1-A.3, A.5, A.6, A.10) + narratives (N1-N6)
- T2 receives ONLY T1 outputs + kernel (NO epistemic bundle)
- T2 MUST execute kernel via Bash (explicit command template)
- T3 receives T1+T2 outputs only (no upstream narrative re-ingestion)

### Changes Applied

| Edit | Section | Change |
|------|---------|--------|
| 1 | A.x T1 Spec | Added surgical edit mandate + T1 output file list |
| 2 | A.x T2 Spec | Removed epistemic bundle, added kernel execution mandate + Bash template |
| 3 | A.x T3 Spec | Receives T1+T2 only, no upstream narratives |
| 4 | A.x Data Flow | Rewrote diagram showing file-based handoffs |
| 5 | II.F Bundle | Removed A.8, A.9, A.11, A.12 from final CVR |
| 6 | V.D Artifacts | Cleaned artifact list, added deprecation note |

### Files Modified

| File | Change |
|------|--------|
| `G3_INTEGRATION_2.2.2e_PROMPT.md` → `G3_INTEGRATION_2.2.3e_PROMPT.md` | Renamed + 6 surgical edits |

### Key Architectural Principles Established

1. **Deterministic Handoff:** T1 writes files → T2 reads files (no re-interpretation)
2. **Kernel Execution Mandate:** T2 MUST use Bash, no manual calculation
3. **Clean Final CVR:** Excludes procedural artifacts (A.8, A.9, A.11, A.12)
4. **Narrative Flow:** N1-N6 edited by T1, N7-N9 generated by T3

### Acceptance Criteria

- [x] T1 specification includes surgical edit mandate
- [x] T1 output file list specified (9 files)
- [x] T2 receives only T1 outputs (no epistemic bundle)
- [x] T2 includes explicit Bash kernel command template
- [x] T3 receives T1+T2 only (no upstream narratives)
- [x] Final CVR excludes deprecated artifacts
- [x] Version bumped to 2.2.3e
- [x] INT smoke test with new architecture (2024-12-21)

---

## PATCH-2024-12-20-001: ENRICH Stage Smoke Test & Orchestration Fixes (#20)

**Date:** 2024-12-20
**Source:** ENRICH smoke test for DAVE
**Status:** COMPLETE

### Problem Statement

1. Initial ENRICH smoke test used wrong inputs ($127.68 IVPS instead of $241.72) due to orchestrator assuming file contents from filenames instead of reading them
2. Direct-write protocol was documented in Pattern 1 but not explicitly specified in all subagent dispatch sections
3. No Source Discovery protocol for cold-start ENRICH invocation

### Solution

**1. Pattern 10: Input Source Validation Protocol**

Added to ORCHESTRATION_KEY_PATTERNS.md:
- Always READ files (not just `ls`) before using as inputs
- Extract and log key metrics (IVPS, DR) before proceeding
- Never assume file contents from filenames
- If folder incomplete, search for most recent complete run

**2. Explicit Direct-Write Protocol in All Subagent Sections**

Updated production/CLAUDE.md for:
- BASE_T1, BASE_REFINE, BASE_T2
- RQ_GEN, RQ_ASK
- ENRICH_T1, ENRICH_T2

Each now explicitly states:
- "Use the Write tool to save to: {path}"
- "After writing, return ONLY: 'Complete. File: {path}'"
- "DO NOT return the file contents"

**3. Source Discovery for Cold-Start**

Added Stage 0 to ENRICH section:
```
1. Find candidate runs: find analyses/ -name "*{TICKER}*" -type d
2. Identify most recent COMPLETE run (has required artifacts)
3. READ and validate (extract IVPS, log baseline)
4. Set RUN_ID, proceed to Stage 1
```

### Smoke Test Results

**Run:** `DAVE_ENRICH_SMOKE_20251220_120936`

| Metric | State 1 (BASE) | State 2 (ENRICH) | Change |
|--------|----------------|------------------|--------|
| IVPS | $241.72 | $199.25 | -17.6% |
| DR | 13.0% | 13.25% | +25 bps |
| Terminal ROIC | 49.3% | 40.9% | -8.4 ppts |

**Artifacts Generated:**
- DAVE_ENRICH_T1.md (86KB)
- DAVE_ENRICH_T2.md (11KB)
- A2-A7 JSON files

### Files Modified

| File | Change |
|------|--------|
| `workshop/orchestration/ORCHESTRATION_KEY_PATTERNS.md` | Added Pattern 10, enhanced Pattern 1 |
| `production/CLAUDE.md` | Explicit direct-write protocol in all sections, Stage 0 Source Discovery |
| `workshop/CLAUDE.md` | Added Pattern 10 note to smoke test section |
| `workshop/patches/PATCH_TRACKER.md` | Updated with smoke test status |

### Acceptance Criteria

- [x] Pattern 10 documented and applied
- [x] Direct-write protocol explicit in all subagent sections
- [x] Source Discovery (Stage 0) added to ENRICH
- [x] ENRICH smoke test passes with correct inputs
- [x] State 1 IVPS correctly captured ($241.72)
- [x] T1 → T2 flow works with kernel execution
- [ ] Cold-start "Do ENRICH on DAVE" test in fresh window

### Path Forward

1. **SCENARIO smoke test** - Next stage to validate
2. **INTEGRATION smoke test** - After SCENARIO
3. **IRR smoke test** - Final stage
4. **Full CAPY test** - Chain all stages without human intervention

---

## PATCH-2024-12-20-002: Direct-Write Protocol Documentation (#21)

**Date:** 2024-12-20
**Source:** Review of orchestration patterns during ENRICH smoke test
**Status:** COMPLETE

### Summary

Ensured all subagent dispatch sections in production/CLAUDE.md explicitly document the direct-write protocol per Pattern 1. This prevents orchestrator from attempting to transcribe subagent outputs (which causes truncation).

### Pattern 1 Enhancement

Added to ORCHESTRATION_KEY_PATTERNS.md:

**Anti-Patterns (PROHIBITED):**
- Subagent returns full content → Orchestrator writes with Write tool (TRUNCATION RISK)
- Orchestrator manually transcribes subagent output (ERROR RISK)
- Orchestrator embeds subagent output in next prompt without reading from disk

**Plan Documentation Standard:**
When describing subagent tasks, always specify:
1. Tool used: "Subagent uses Write tool to save to {path}"
2. Return format: "Returns confirmation + filepath only"
3. Verification step: "Orchestrator verifies with `ls -la`"

### Acceptance Criteria

- [x] Pattern 1 enhanced with anti-patterns and documentation standard
- [x] All subagent sections in production/CLAUDE.md use explicit protocol
- [x] Step numbering fixed (no duplicate step numbers)

---

## PATCH-2024-12-23-001: Kernel CLI Wrapper Scripts (#31)

**Date:** 2024-12-23
**Source:** ZENV smoke test kernel execution failure
**Status:** COMPLETE

### Problem Statement

**All 5 CVR kernels lack CLI interfaces.** They are designed as importable Python modules only:

```python
# Kernel entry point (NO argparse)
def execute_cvr_workflow(kg, dag_artifact, gim_artifact, dr_trace, ...):
    ...

# NO if __name__ == '__main__': block
```

But orchestration expects CLI execution:
```bash
python3 BASE_CVR_KERNEL_2.2.3e.py --a2 ... --a5 ... --output ...
```

**Failure Mode:** When T2 subagent attempted to run kernel via Bash, it failed because no CLI interface exists. This is a **systematic gap** affecting all kernels, not a one-off bug.

### Root Cause

The kernels were originally designed for notebook/import usage, not orchestrated pipeline execution. The orchestration pattern (Pattern 12/13) requires Bash execution with JSON file I/O, but kernels only accept in-memory Python objects.

### Solution: CLI Wrapper Scripts

Created 5 wrapper scripts in `workshop/scripts/` that provide argparse interfaces for all kernels:

| Wrapper | Kernel | Key Inputs | Output |
|---------|--------|------------|--------|
| `run_base_kernel.py` | BASE_CVR_KERNEL_2.2.3e | A2, A3, A5, A6 | A7 |
| `run_enrich_kernel.py` | CVR_KERNEL_ENRICH_2.2.3e | A2, A3, A5, A6 | A7 |
| `run_scen_kernel.py` | CVR_KERNEL_SCEN_2_2_2e | A2, A3, A5, A6, A7, args | A10 |
| `run_int_kernel.py` | CVR_KERNEL_INT_2_2_2e | A2, A3, A5, A6, A10, cascade | A7 (recalc) |
| `run_irr_kernel.py` | CVR_KERNEL_IRR_2.2.5e | A2, A7, A10, A13 | A14 |

### Technical Implementation

Each wrapper handles:

1. **Artifact Unwrapping:** Accepts both `{"A.X_...": {...}}` wrapped format and raw JSON
   ```python
   kg = a2_raw.get('A.2_ANALYTIC_KG', a2_raw)  # Handle both formats
   ```

2. **DR Schema Normalization:** Finds DR value in multiple locations
   ```python
   dr_value = a6_inner.get('DR') or a6_inner.get('DR_Static')
   if 'derivation_trace' in a6_inner:
       dr_value = a6_inner['derivation_trace'].get('DR_Static', dr_value)
   dr_trace = {'derivation_trace': {'DR_Static': dr_value}}
   ```

3. **importlib.util Loading:** Kernel filenames have dots (e.g., `2.2.3e.py`) which break `__import__`
   ```python
   spec = importlib.util.spec_from_file_location("kernel", kernel_file)
   kernel = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(kernel)
   ```

4. **Exit Codes:** Returns 0 on success, 1 on failure for orchestrator validation

### Usage Example

```bash
python3 scripts/run_base_kernel.py \
    --a2 03_T2/ZENV_A2_ANALYTIC_KG_BASE.json \
    --a3 03_T2/ZENV_A3_CAUSAL_DAG_BASE.json \
    --a5 03_T2/ZENV_A5_GIM_BASE.json \
    --a6 03_T2/ZENV_A6_DR_BASE.json \
    --output 03_T2/ZENV_A7_VALUATION_BASE.json
```

### Smoke Test Evidence

**ZENV BASE T2:** IVPS = 4.31 BRL/share (validated as reasonable for ZENV)

### Files Created

| File | Lines | Status |
|------|-------|--------|
| `scripts/run_base_kernel.py` | 154 | Tested ✅ |
| `scripts/run_enrich_kernel.py` | 146 | Ready |
| `scripts/run_scen_kernel.py` | 170 | Ready |
| `scripts/run_int_kernel.py` | 191 | Ready |
| `scripts/run_irr_kernel.py` | 139 | Ready |

### Commit

`bf09d3b` - feat(scripts): add CLI wrappers for all 5 CVR kernels

### Acceptance Criteria

- [x] All 5 kernels have CLI wrappers
- [x] Wrappers handle artifact unwrapping (wrapped/raw formats)
- [x] Wrappers handle DR schema normalization
- [x] Wrappers use importlib.util for dot-versioned filenames
- [x] Wrappers return proper exit codes
- [x] BASE wrapper tested with ZENV (IVPS=4.31)
- [x] Committed and pushed to master

### Future Considerations

1. **Wrapper versioning:** If kernel API changes, wrappers may need updates
2. **Kernel receipt integration:** Wrappers could generate Pattern 13 receipts
3. **Unit test suite:** Automated tests for wrappers with mock data
