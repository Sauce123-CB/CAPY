# CAPY 2.2.3e Patch Tracker

Last updated: 2024-12-20

## Summary

| Status | Count |
|--------|-------|
| Complete | 12 |
| Pending | 11 |
| **Total** | **23** |

**Completion: 52%**

---

## Pipeline Smoke Test Status

| Stage | Status | Smoke Test Folder | Notes |
|-------|--------|-------------------|-------|
| BASE | ✅ Complete | `DAVE_20241214/` | Full T1→REFINE→T2 |
| RQ | ✅ Complete | `DAVE_RQ_CLAUDE_TEST/` | 7-slot with Claude Opus subagents |
| ENRICH | ✅ Complete | `DAVE_ENRICH_SMOKE_20251220_120936/` | State 1→2: $241.72→$199.25 |
| SCENARIO | ✅ Complete | `DAVE_ENRICH_SMOKE_20251220_120936/06_SCENARIO/` | E[IVPS]=$206.34, 4 scenarios, SSE 16 states |
| SILICON COUNCIL | ⏳ Pending | - | Next smoke test |
| INTEGRATION | ⏳ Pending | - | After Silicon Council |
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
| 2024-12-14 | 8 | Initial | Success | CLAUDE.md created |
| 2024-12-14 | 9 | Initial | Success | DAVE smoke test complete |
| 2024-12-15 | 13 | Initial | Success | Three-folder architecture |
| 2024-12-18 | N/A | Claude | Success | RQ_GEN 6×GDR routing + Gemini CLI setup |
| 2024-12-19 | 18 | Claude | Success | RQ 7-slot architecture (M-3a/M-3b split) |
| 2024-12-19 | 19 | Claude | Success | Claude Opus subagent RQ_ASK + direct-write protocol |
| 2024-12-20 | 20 | Claude | Success | ENRICH smoke test + Pattern 10/11 orchestration fixes |
| 2024-12-20 | 21 | Claude | Success | Direct-write protocol documentation across all stages |
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
