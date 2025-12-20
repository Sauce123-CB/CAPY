# CAPY Workshop - Master TODO

> **Last updated:** 2024-12-20
> **Structure version:** 0.4 (Atomized prompts CANONICAL through ENRICH)

---

## How to Use This File

- This is the **single source of truth** for all CAPY work items
- Detailed patch specs live in `patches/CAPY_2.2.2e_Patch_Details.md`
- Session logs live in `patches/CHANGELOG.md`
- Claude should checkpoint periodically and suggest better organization

---

## Section 1: Current Sprint (2.2.2e Patches)

### Blocking Issues (Do First)

*No blocking issues - atomization complete through ENRICH.*

### Kernel Bugs (Evaluate After Prompt Fixes)

| # | Item | Type | Complexity | Status |
|---|------|------|------------|--------|
| 2 | Terminal ROIC bug - IC scaling formula | Kernel | **High** | 🔴 Pending |
| 11 | Sensitivity analysis bug - IVPS not centered | Kernel | **High** | 🔴 Pending |

*These may produce wrong numbers but won't crash pipeline. Evaluate after prompt fixes.*

### Prompt Patches (Ready to Apply)

| # | Item | Type | Complexity | Status |
|---|------|------|------------|--------|
| 3 | REFINE DAG cap 12-15 nodes | Prompt | Low | 🔴 Pending |
| 4 | Currency/jurisdiction guidance | Prompt | Low | 🔴 Pending |
| 5 | Loosen ROIC/IC narrative language | Prompt | Low | 🔴 Pending |
| 12 | Market price lookup (WebSearch) | Prompt | Low | 🔴 Pending |
| 1 | T1+T2 KG handshake enforcement | Prompt | Medium | 🔴 Pending |
| 6 | Output requirements for speed | Prompt | Medium | 🔴 Pending |
| 7 | Streamline prompts (remove embedded code) | Prompt | Medium | 🟢 Addressed by #17 |
| 10 | Schema conformance (exact JSON templates) | Prompt | Medium | 🔴 Pending |

### Validation (Spec Done, Prompt Needed)

| # | Item | Type | Complexity | Status |
|---|------|------|------------|--------|
| 14 | Inter-turn validator prompt (Opus) | Validation | Medium | 🟡 Spec only |

### Completed This Cycle

| # | Item | Type | Date | Notes |
|---|------|------|------|-------|
| 0 | PDF extraction skill | Infrastructure | 2024-12-14 | `.claude/skills/` |
| 8 | Claude Code orchestrator | Orchestrator | 2024-12-14 | Initial CLAUDE.md |
| 9 | Smoke test (DAVE) | Testing | 2024-12-14 | Baseline established |
| 13 | Folder organization | Infrastructure | 2024-12-15 | Three-folder architecture |
| 17 | **G3BASE atomization** - 4-file split | Prompt | 2024-12-20 | CANONICAL (PROMPT/SCHEMAS/NORMDEFS + kernel) |
| 16 | **REFINE v1_2** - trajectory calibration | Prompt | 2024-12-20 | CANONICAL |
| 18 | RQ 7-slot architecture (M-3a/M-3b) | Prompt | 2024-12-19 | CANONICAL |
| 19 | Claude Opus subagent RQ_ASK | Kernel | 2024-12-19 | Direct-write protocol |
| 20 | ENRICH atomization + smoke test | Prompt | 2024-12-20 | CANONICAL (4-file split) |

---

## Section 2: Infrastructure & Organization

### Immediate (This Week)

- [ ] Move prompts from `orchestration/` to proper `prompts/` subfolders
  - `RQ_Gen_2_2_2e.md` → `prompts/rq_gen/`
  - `G3_SILICON_COUNCIL_2.2.1e.md` → `prompts/silicon_council/`
  - `HITL_DIALECTIC_AUDIT_1_0_Goldilocks.md` → `prompts/hitl_audit/`
- [ ] Add collaborators to GitHub repos
- [ ] Create `prompts/rq_gen/`, `prompts/silicon_council/`, `prompts/hitl_audit/` folders

### Short-term (This Month)

- [x] Add source_library/ to Production for researcher uploads
- [ ] Run first CC-enabled smoke test using Workshop CLAUDE.md
- [ ] Validate DEV: commands work as documented
- [ ] Test DEV: COMPARE RUNS functionality
- [ ] Graduate Production CLAUDE.md from v0.1.0 to v1.0

### Documentation Debt

- [ ] Document RQ_Gen workflow in CLAUDE.md
- [ ] Document Silicon Council workflow in CLAUDE.md
- [ ] Document HITL Audit workflow in CLAUDE.md
- [ ] Write inter-turn validator prompt (#14)

---

## Section 3: One-Click Pipeline Architecture (Active)

> **Decision date:** 2024-12-17
> **Status:** Active development - this is the current direction

### Design Principles

1. **Minimize human touchpoints** - One-click execution from source docs to final output
2. **Reduce latency** - No waiting for human handoffs between stages
3. **Reduce errors** - Automated handoffs prevent context loss between stages

### Pipeline Stages

```
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 1: Document Sourcing (Human + Claude preprocessing)      │
├─────────────────────────────────────────────────────────────────┤
│ Human: Upload source PDFs to source_library/{TICKER}/          │
│ Claude: pdfplumber + pdf2image preprocessing                   │
│ Output: extracted.md files + VISUAL_MANIFEST.md                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 2: BASE Pipeline (T1 → REFINE → T2)                      │
├─────────────────────────────────────────────────────────────────┤
│ Automated: Subagent execution with atomized prompts            │
│ - G3BASE_PROMPT.md (core instructions)                         │
│ - G3BASE_SCHEMAS.md (Appendix A)                               │
│ - G3BASE_NORMDEFS.md (Appendix B)                              │
│ - BASE_CVR_KERNEL.py (Python kernel)                           │
│ Output: Kernel JSON + IVPS                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 3: Research Questions (6x Gemini Deep Research)          │
├─────────────────────────────────────────────────────────────────┤
│ Automated: Parallel API fan-out                                │
│ - 6 RQs generated from BASE output                             │
│ - All 6 sent to Gemini Deep Research API                       │
│ - User's Gemini Ultra account for cost efficiency              │
│ Output: 6 research reports                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 4: ENRICH → SCENARIO → INTEGRATION → IRR                 │
├─────────────────────────────────────────────────────────────────┤
│ Automated: Sequential subagent execution                       │
│ Output: Full valuation with scenarios                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 5: Silicon Council (3x Claude + 3x Gemini Extended)      │
├─────────────────────────────────────────────────────────────────┤
│ Automated: Parallel deliberation                               │
│ - 3 queries via Claude (native in Claude Code)                 │
│ - 3 queries via Gemini 2.5 Extended Thinking API               │
│ Output: Synthesized council verdict                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 6: HITL Audit (Optional human review)                    │
├─────────────────────────────────────────────────────────────────┤
│ Human: Review final output, approve or flag for revision       │
│ This stage can be skipped for high-confidence outputs          │
└─────────────────────────────────────────────────────────────────┘
```

### Implementation Status

| Stage | Status | Blocker |
|-------|--------|---------|
| 1. Document Sourcing | ✅ Working | None |
| 2. BASE Pipeline | ✅ Working | Atomized prompts CANONICAL |
| 3. RQ Fan-out | ✅ Working | 7-slot architecture, Claude Opus subagents |
| 4. ENRICH | ✅ Working | Atomized prompts CANONICAL |
| 5. SCENARIO→IRR | 🟡 Prompts exist | Need smoke test (next) |
| 6. Silicon Council | 🟡 Spec only | Need Gemini Extended Thinking integration |
| 7. HITL Audit | ✅ Prompt exists | None |

### Stage 3 Details (Updated 2024-12-18)

- **Gemini CLI:** v0.21.2 installed at `~/.npm-global/bin/gemini`
- **Authentication:** OAuth with Google Ultra account (`redsox12278@gmail.com`)
- **RQ_GEN:** Updated to 6×GDR routing (removed AlphaSense)
- **RQ_ASK:** Executor script at `kernels/RQ_ASK_KERNEL_2_2_2e.py`
- **Next:** Smoke test on DAVE ticker

### API Requirements

| Service | Purpose | Account |
|---------|---------|---------|
| Gemini Deep Research | RQ fan-out (6x) | User's Gemini Ultra |
| Gemini 2.5 Extended Thinking | Silicon Council (3x) | User's Gemini Ultra |
| Claude (native) | Silicon Council (3x) | Claude Code session |

### Why Not AlphaSense API?

- AlphaSense has excellent coverage for global securities
- API access is prohibitively expensive
- Manual upload by research assistant scales for tens of securities/week
- Revisit if volume increases significantly

### Eval Framework

**Goal:** Systematic comparison of prompt versions using standardized test cases.

**Ideas:**
- Golden set of companies (DAVE, ZENV, FLL, JET2)
- Automated IVPS comparison across versions
- Regression detection

**Not started.** Depends on stable 2.2.2e baseline.

### Multi-user Collaboration Patterns

**Goal:** Best practices for team working in same repos.

**Ideas:**
- Branch naming conventions
- PR review process for prompt changes
- Conflict resolution for simultaneous edits

**Not started.** Will emerge from usage.

---

## Section 4: Parking Lot

*Items that came up but aren't prioritized yet.*

- Consider splitting large prompts into modular components
- Explore MCP server for CAPY pipeline
- Investigate prompt caching for repeated runs

---

## Suggested Review Cadence

| Frequency | Action |
|-----------|--------|
| Each session | Update status of items worked on |
| Weekly | Review Section 1 progress, reprioritize if needed |
| Monthly | Review Sections 2-3, archive completed items |
| Quarterly | Review Section 4 parking lot, promote or delete |

---

## Meta: Improving This Structure

Claude should suggest improvements when:
- Too many items in one section (split it)
- Items stale for >2 weeks (flag for review)
- Dependencies between items not clear (add links)
- New category of work emerges (add section)

Current structure: 4 sections + parking lot. Is this working?
