# Session Log: 2024-12-16 (WORKSHOP)

## Context

This session received handoff from CAPY_Production smoke test findings. The Production session validated CC infrastructure (T1, REFINE work via Opus subagents) but revealed critical prompt engineering bugs.

## What Was Done

### 1. Received Handoff from Production

`CAPY_Production/WORKSHOP_HANDOFF_20241216.md` documented:
- T2 subagent fabrication (fixed in Production CLAUDE.md)
- T2 validator false positive with Haiku (fixed: use Opus)
- Schema mismatches: REFINE outputs `nodes`/`drivers`, kernel expects `DAG`/`GIM`
- Empty `coverage_manifest`
- Multi-period GIM format not kernel-compatible
- No trajectory validation before kernel execution

### 2. Created REFINE v1_2

**File:** `prompts/refine/BASE_T1_REFINE_v1_2.md`

Added:
- **Section 2.5: Trajectory Calibration (Hard Gate)**
  - Step 1: Simulate Checkpoints (Y1, Y5, Y10)
  - Step 2: Internal Consistency Checks
  - Step 3: Epistemic Anchor Comparison (vs A.1 p10/p50/p90)
  - Step 4: Economic Plausibility flags (EBIT>60%, ROIC>50% sustained, etc.)
  - Step 5: Repair Loop (max 3 iterations)

- **Section 4: Kernel Schema Requirements**
  - `DAG` key (not `nodes`)
  - `GIM` key (not `drivers`)
  - `coverage_manifest` must be populated
  - Single DSL per driver (no multi-period)
  - DSL mode reference table

- **Section C.5: Output format** for trajectory calibration results

### 3. Updated PATCH_TRACKER.md

Added PATCH-2024-12-16-001 (#16): Trajectory Calibration & Schema Enforcement

### 4. Updated CLAUDE.md

- Version 0.1.0 → 0.2.0
- Marked REFINE v1_2 as EXPERIMENTAL in canonical versions table

### 5. Committed and Merged

All changes merged to master in CAPY_Workshop.

---

## Critical Discovery: Patch #7 Severity Upgrade

### Original Classification
- **Patch #7:** "Streamline prompts (remove embedded code)"
- **Severity:** Medium (token efficiency)

### Revised Classification
- **Severity:** **HIGH/CRITICAL** (correctness blocker)

### Evidence

G3BASE has ~2300 lines, ~1400 of which are Appendix C (embedded kernel code). This causes:

1. **Format corruption** - Escaped characters (`\*`, `\'`, `\[`) and broken line breaks from Word/PDF conversion paths
2. **Attention degradation** - Long prompt buries critical schema requirements
3. **Schema drift** - Code shows correct keys but model treats as "reference," not mandatory
4. **Hallucination vector** - Model may "simulate" execution instead of following schema strictly
5. **Maintenance nightmare** - Kernel updates require prompt updates (version skew)

### Root Cause Analysis

The REFINE v1_1 said "verify JSON structure matches kernel requirements" but:
- Provided no concrete schema examples
- Kernel code was in G3BASE Appendix C (not REFINE)
- Embedded code was format-corrupted
- Model read "review it to ensure alignment" as advisory

---

## Blocker Identified

**G3BASE Appendix C must be removed before next smoke test.**

### Why It's a Blocker

1. Even with REFINE v1_2 schema requirements, T1 may still output wrong keys
2. REFINE would have to fix T1's schema errors (downstream patching)
3. Root cause (G3BASE prompt length + embedded code) remains unfixed
4. Next smoke test likely to hit same issues

### Required Fix (Option B from session)

Create G3BASE 2.2.2e by:
1. **Remove Appendix C entirely** (kernel code stays in .py file only)
2. **Add explicit JSON schema examples inline** (not code blocks, just structure)
3. **Clean up format corruption** (escaped chars, broken lines)
4. **Add unit conventions section**

---

## State Summary

### Files Changed (WORKSHOP)

| File | Change |
|------|--------|
| `prompts/refine/BASE_T1_REFINE_v1_2.md` | Created (trajectory calibration + schema) |
| `patches/PATCH_TRACKER.md` | Added #16, updated counts |
| `CLAUDE.md` | v0.2.0, REFINE v1_2 marked experimental |

### Files NOT Changed (Deferred)

| File | Reason |
|------|--------|
| `prompts/base/G3BASE_2.2.2e.md` | Requires Appendix C removal (blocker fix) |
| `validators/CAPY_INTERTURN_VALIDATOR_CC.md` | Low priority |

---

## Tomorrow's Session: Start Here

### Priority 1: Create G3BASE 2.2.2e

1. Read current G3BASE_2.2.1e.md
2. Remove Appendix C (lines ~874-2280, embedded kernel code)
3. Add explicit schema examples inline at artifact definition points
4. Add unit conventions section (from handoff doc)
5. Clean up format corruption throughout
6. Commit as EXPERIMENTAL

### Priority 2: Deploy to Production

1. Copy G3BASE_2.2.2e.md and REFINE v1_2 to Production
2. Update Production CLAUDE.md canonical versions

### Priority 3: Re-run Smoke Test

```
CAPY: INIT DAVE "Dave Inc" 2024-12-16
CAPY: RUN BASE_PIPELINE
```

### Acceptance Criteria

- [ ] T1 outputs correct schema keys (`DAG`, `GIM`, populated `coverage_manifest`)
- [ ] REFINE trajectory calibration runs and produces plausible metrics
- [ ] No schema repair step needed before kernel
- [ ] T2 kernel produces plausible IVPS

---

## Key Files to Reference

| File | Location | Purpose |
|------|----------|---------|
| WORKSHOP_HANDOFF_20241216.md | CAPY_Production | Full findings from smoke test |
| PATCH_TRACKER.md | CAPY_Workshop/patches | All patches including #16 |
| BASE_T1_REFINE_v1_2.md | CAPY_Workshop/prompts/refine | New REFINE with trajectory cal |
| G3BASE_2.2.1e.md | CAPY_Workshop/prompts/base | Current (needs cleanup) |
| DAVE_kernel_output.json | CAPY_Production/analyses/DAVE_*/03_T2 | Evidence of garbage financials |
