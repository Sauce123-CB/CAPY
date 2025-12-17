# Session Log: 2024-12-17

## Summary

Major architecture pivot and infrastructure work.

---

## Part 1: GitHub Cloud Sync (Completed)

### Objective
Get all three CAPY repos on GitHub for cloud access and collaboration.

### Actions
1. Reviewed unpushed commits (Workshop: 2, Production: 8)
2. **Production soft reset** - Recommitted cleanly without binaries
   - 8 commits → 4 clean commits
   - Excluded PDFs, PNGs, ZIPs via .gitignore
3. Created .gitignore for all three repos
4. Pushed all repos to GitHub:
   - `Sauce123-CB/CAPY_Workshop`
   - `Sauce123-CB/CAPY_Production`
   - `Sauce123-CB/CAPY_Archive`

### New Slash Commands
Created `.claude/commands/` with:
- `/sync` - Sync all repos
- `/promote` - Success path after smoke test
- `/iterate` - Failure path after smoke test

---

## Part 2: Architecture Pivot (Documented)

### Old Architecture: Hybrid (3 Human Touchpoints)
1. Human: Document sourcing
2. Human: RQ fan-out (AlphaSense + Gemini)
3. Human: Silicon Council

### New Architecture: One-Click Pipeline

| Stage | Execution |
|-------|-----------|
| Document Sourcing | Human uploads → Claude preprocesses |
| BASE Pipeline | Automated subagent execution |
| RQ Fan-out | 6x Gemini Deep Research API |
| ENRICH→IRR | Automated subagent execution |
| Silicon Council | 3x Claude + 3x Gemini Extended Thinking |
| HITL Audit | Optional human review |

### Why This Change
- Reduce latency (no waiting for human handoffs)
- Reduce errors (automated handoffs prevent context loss)
- Scale better (human only uploads docs, everything else automated)

### API Strategy
- Gemini Deep Research: User's Gemini Ultra account (cost-efficient)
- Gemini Extended Thinking: User's Gemini Ultra account
- Claude: Native in Claude Code

---

## Part 3: Blocking Patches Identified

### Definite Blockers (Must Fix for DAVE Smoke Test)

| # | Patch | Status |
|---|-------|--------|
| 17 | G3BASE atomization (split into 4 files) | Spec written |
| 16 | REFINE v1_2 trajectory calibration | Created, needs deploy |

### Why These Block
- **#17**: G3BASE is 2300 lines. Appendix C (~1400 lines of embedded kernel) causes:
  - Context loss in subagent
  - Schema drift
  - Format corruption
- **#16**: REFINE produces wrong JSON keys, empty coverage_manifest

### Deferred (Evaluate After Prompt Fixes)
- #2: Terminal ROIC bug (kernel)
- #11: Sensitivity analysis bug (kernel)

---

## Next Steps

1. ✅ Commit this documentation
2. Review PATCH_TRACKER for any missed blockers → checkpoint
3. Execute Patch #17 (G3BASE atomization)
4. Deploy Patch #16 (REFINE v1_2)
5. Run DAVE smoke test
6. Test `/iterate` or `/promote` based on result

---

## Files Modified This Session

### Workshop
- `CLAUDE.md` → v0.3.0 (Git workflow + slash commands)
- `TODO.md` → v0.2 (One-Click Pipeline architecture)
- `patches/PATCH_TRACKER.md` (added #17)
- `patches/SESSION_LOG_20241217.md` (this file)
- `.gitignore` (created)
- `.claude/commands/sync.md` (created)
- `.claude/commands/promote.md` (created)
- `.claude/commands/iterate.md` (created)

### Production
- `.gitignore` (created)
- Recommitted cleanly (4 commits)

### Archive
- `.gitignore` (created)

---

## Part 4: Patch Execution

### Patch #17: G3BASE Atomization (Completed)

**Source:** G3BASE_2.2.1e.md (2316 lines)

**Structure identified:**
- Lines 1-456: Core prompt (Sections I-V)
- Lines 457-779: Appendix A (Schemas)
- Lines 780-872: Appendix B (DSL/Normative Defs)
- Lines 874-2281: Appendix C (Kernel code) - **REMOVED**
- Lines 2284-2316: Appendix D (Naming conventions)

**Files created:**
| File | Lines | Content |
|------|-------|---------|
| `G3BASE_2.2.2e_PROMPT.md` | ~500 | Sections I-V + Appendix D |
| `G3BASE_2.2.2e_SCHEMAS.md` | ~220 | Appendix A (JSON schemas) |
| `G3BASE_2.2.2e_NORMDEFS.md` | ~150 | Appendix B (DSL definitions) |

**Key changes:**
- Removed ~1400 lines of embedded kernel code (Appendix C)
- Added cross-references between files
- Updated version strings to 2.2.2e

**Archived:** G3BASE_2.2.1e.md → `CAPY_Archive/prompts/base/`

### Patch #16: REFINE v1_2 Deployment (Completed)

Copied to Production:
- `prompts/refine/BASE_T1_REFINE_v1_2.md`
- `prompts/base/G3BASE_2.2.2e_PROMPT.md`
- `prompts/base/G3BASE_2.2.2e_SCHEMAS.md`
- `prompts/base/G3BASE_2.2.2e_NORMDEFS.md`
- `kernels/BASE_CVR_KERNEL_2.2.2e.py`

### Patch #12: Market Price WebSearch (Completed)

Added mandatory WebSearch requirement to G3BASE_2.2.2e_PROMPT.md Section II.A:

```markdown
-   **Market Price Requirement (MANDATORY):** Before populating `Current_Stock_Price`:
    1. Use WebSearch: "{TICKER} stock price"
    2. Extract current market price from search results
    3. Document the search timestamp
    > **DO NOT** use prices from source documents (stale) or memory (hallucinated).
```

### Patch #10: Schema Conformance Review (Completed - No Changes Needed)

**Analysis performed:**
- Reviewed G3BASE_2.2.2e_SCHEMAS.md for explicit format requirements
- Found that "Critical Schema Requirements" section already includes:
  - DAG Node Format example showing type/parents/equation structure
  - GIM Entry Format example showing mode/params/qualitative_thesis structure
- Examples use correct JSON keys (`DAG`, `GIM`, not `nodes`, `drivers`)

**Conclusion:** Atomization itself addresses schema conformance by:
1. Making schemas more prominent (dedicated file vs. buried in monolith)
2. Explicit examples already present and correct
3. Reduced context dilution means LLM pays more attention to schemas

**No additional changes required.** The smoke test will validate whether this is sufficient.

---

## Part 5: Pending Tasks

| Task | Status |
|------|--------|
| Commit Workshop changes | Pending |
| Commit Production changes | Pending |
| Sync both repos to GitHub | Pending |
| Run DAVE smoke test | Pending |
| Test /promote or /iterate | Pending |
| If atomization works, propagate to ENRICH/SCENARIO/INT/IRR | Backlog |

---

## Files Modified (Part 4)

### Workshop
- `CLAUDE.md` → v0.4.0 (atomized file documentation)
- `prompts/base/G3BASE_2.2.2e_PROMPT.md` (created)
- `prompts/base/G3BASE_2.2.2e_SCHEMAS.md` (created)
- `prompts/base/G3BASE_2.2.2e_NORMDEFS.md` (created)
- `kernels/BASE_CVR_KERNEL_2.2.2e.py` (created)
- `patches/PATCH_TRACKER.md` (updated)
- `patches/SESSION_LOG_20241217.md` (updated)

### Production
- `prompts/base/G3BASE_2.2.2e_PROMPT.md` (deployed)
- `prompts/base/G3BASE_2.2.2e_SCHEMAS.md` (deployed)
- `prompts/base/G3BASE_2.2.2e_NORMDEFS.md` (deployed)
- `prompts/refine/BASE_T1_REFINE_v1_2.md` (deployed)
- `kernels/BASE_CVR_KERNEL_2.2.2e.py` (deployed)

### Archive
- ~~`prompts/base/G3BASE_2.2.1e.md` (archived)~~ — **REVERTED** (see Part 6)

---

## Part 6: Version Labeling System Fix

### Problem Identified

During patch execution, G3BASE_2.2.1e.md was prematurely archived before the new 2.2.2e version was smoke tested. This violated the rule that CANONICAL versions must remain available until EXPERIMENTAL passes.

### Corrective Actions

1. **Restored** `G3BASE_2.2.1e.md` from Archive back to Workshop
2. **Removed** premature archive copy from `CAPY_Archive/prompts/base/`
3. **Updated CLAUDE.md** to v0.5.0 with:
   - New "Version Labeling System" section with explicit rules
   - Revised "Current Versions" table with Status and Smoke Test columns
   - Updated DEV: APPLY PATCH to enforce labeling
   - Updated DEV: MARK CANONICAL to require smoke test proof

### Current State After Fix

| File | Status | Location |
|------|--------|----------|
| G3BASE_2.2.1e.md | CANONICAL | Workshop (restored) |
| G3BASE_2.2.2e_*.md | EXPERIMENTAL | Workshop + Production |

### Lesson Learned

> **Never archive CANONICAL until EXPERIMENTAL passes smoke test.**

The new CLAUDE.md documentation now enforces this procedurally.
