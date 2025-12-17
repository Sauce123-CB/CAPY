# CAPY 2.2.2e Patch Tracker

Last updated: 2024-12-17

## Summary

| Status | Count |
|--------|-------|
| Complete | 5 |
| Pending | 12 |
| **Total** | **17** |

**Completion: 29%**

---

## Completed Patches

| # | Item | Type | Deliverable |
|---|------|------|-------------|
| 0 | PDF extraction skill | Infrastructure | `.claude/skills/pdf-processor/` |
| 8 | Claude Code orchestrator | Orchestrator | `CLAUDE.md` |
| 9 | Smoke test (DAVE) | Testing | `smoke_tests/DAVE_20241214/` |
| 13 | Folder organization | Infrastructure | Three-folder architecture |
| 14 | Inter-turn validator | Validation | Spec in CLAUDE.md (prompt NOT written) |

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
