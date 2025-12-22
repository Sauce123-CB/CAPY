# CAPY Mega-Patch: Atomization + Pipeline Fixes

**Patch ID:** PATCH-2024-12-22-001
**Priority:** CRITICAL (blocks clean execution of all pipeline stages)
**Status:** Planning
**Last Updated:** 2024-12-22

---

## Consolidated TODO Items

This mega-patch consolidates multiple pending items from `TODO.md`:

| # | Item | Status | Resolution |
|---|------|--------|------------|
| 1 | T1+T2 KG handshake enforcement | ✅ IN PATCH | REFINE fix (see Section 8) |
| 2 | Terminal ROIC bug - IC scaling | ✅ IN PATCH | Kernel fix (see Section 7) |
| 3 | REFINE DAG cap 12-15 nodes | ✅ ALREADY DONE | Verified in REFINE v1.2 |
| 4 | Currency/jurisdiction guidance | ✅ IN PATCH | Auto-detect from financials (see Section 13) |
| 5 | Loosen ROIC/IC narrative language | 🔶 DEFERRED | Cosmetic, low priority |
| 6 | Output requirements for speed | ✅ SUBSUMED | Fixed by atomization |
| 10 | Schema conformance (exact templates) | ✅ EXPECTED FIX | Atomization should resolve |
| 11 | Sensitivity analysis bug | 🔶 DEFERRED | Low priority, possibly one-time error |
| 12 | Market price lookup (WebSearch) | ✅ ALREADY DONE | Verified in BASE & IRR |
| 15 | DR rubric calibration (too high) | ✅ IN PATCH | Global universe calibration (see Section 14) |

---

## Problem Statement

Consolidated markdown documents (T1.md, T2.md, T3.md) that embed JSON artifacts get truncated when Claude produces them, causing downstream stages to receive incomplete inputs.

**Empirical Evidence:**
- INT T3 for DAVE: A10 has precision loss (16→2-5 digits) and 3+ missing fields
- Mathematical proof: Sum of standalone artifacts (38.5K) > total T3.md (38K)
- Root cause: Claude optimizes for human readability (rounds, filters "redundant" fields)

---

## Solution Overview

This mega-patch addresses five categories of issues:

1. **Artifact Atomization** (Pattern 12) - Every artifact becomes an individual file
2. **Kernel Execution Receipts** (Pattern 13) - Verifiable proof of real execution
3. **Terminal ROIC Bug Fix** - Derive g from topline growth, not ROIC
4. **REFINE Handshake Fix** - Preserve Equity Bridge items (FDSO, debt, cash)
5. **Full Pipeline Orchestration** - PDF preprocessing → IRR in one command

---

## Section 1: Full Artifact Atomization

**Core Principle:** Every artifact and narrative becomes an individual file. Consolidated markdown is produced ONLY for human audit, never as machine input.

**Canonical Snapshot Principle:** Each stage folder contains a COMPLETE set of all artifacts with that stage's suffix. Orchestrator copies forward unchanged files via `cp` (NOT Claude read/write) before each stage.

### Naming Convention (Stage-Based)

```
{TICKER}_{ARTIFACT}_{STAGE}.{ext}

Examples:
- DAVE_A5_GIM_BASE.json       # A5 after BASE stage
- DAVE_A5_GIM_ENRICH.json     # A5 after ENRICH stage (if modified)
- DAVE_A5_GIM_INT.json        # A5 after INTEGRATION stage
- DAVE_N1_THESIS_BASE.md      # N1 narrative after BASE
- DAVE_BASE_T1_AUDIT.md       # Human audit only (NOT machine input)
```

### Stage Suffixes

| Stage | Suffix | State |
|-------|--------|-------|
| BASE | `_BASE` | State 1 |
| RQ | `_RQ` | - |
| ENRICH | `_ENRICH` | State 2 |
| SCENARIO | `_SCEN` | State 3 |
| SILICON COUNCIL | `_SC` | - |
| INTEGRATION | `_INT` | State 4 |
| IRR | `_IRR` | State 5 |

---

## Section 2: Complete Canonical Snapshot by Stage

**Each stage folder contains ALL artifacts from prior stages (copied forward) PLUS new/modified artifacts.**

### BASE Stage Canonical Snapshot (10 files)
| File | Origin |
|------|--------|
| `{TICKER}_A1_EPISTEMIC_ANCHORS_BASE.json` | NEW |
| `{TICKER}_A2_ANALYTIC_KG_BASE.json` | NEW |
| `{TICKER}_A3_CAUSAL_DAG_BASE.json` | NEW |
| `{TICKER}_A5_GIM_BASE.json` | NEW |
| `{TICKER}_A6_DR_BASE.json` | NEW |
| `{TICKER}_A7_VALUATION_BASE.json` | NEW (T2 kernel) |
| `{TICKER}_N1_THESIS_BASE.md` | NEW |
| `{TICKER}_N2_IC_BASE.md` | NEW |
| `{TICKER}_N3_ECON_GOV_BASE.md` | NEW |
| `{TICKER}_N4_RISK_BASE.md` | NEW |

### RQ Stage Canonical Snapshot (19 files)
| File | Origin |
|------|--------|
| `{TICKER}_A1_EPISTEMIC_ANCHORS_RQ.json` | COPIED from BASE |
| `{TICKER}_A2_ANALYTIC_KG_RQ.json` | COPIED from BASE |
| `{TICKER}_A3_CAUSAL_DAG_RQ.json` | COPIED from BASE |
| `{TICKER}_A5_GIM_RQ.json` | COPIED from BASE |
| `{TICKER}_A6_DR_RQ.json` | COPIED from BASE |
| `{TICKER}_A7_VALUATION_RQ.json` | COPIED from BASE |
| `{TICKER}_N1_THESIS_RQ.md` | COPIED from BASE |
| `{TICKER}_N2_IC_RQ.md` | COPIED from BASE |
| `{TICKER}_N3_ECON_GOV_RQ.md` | COPIED from BASE |
| `{TICKER}_N4_RISK_RQ.md` | COPIED from BASE |
| `{TICKER}_A8_RESEARCH_PLAN_RQ.json` | NEW |
| `{TICKER}_A9_RESEARCH_RESULTS_RQ.json` | NEW |
| `{TICKER}_RQ1_INTEGRITY_RQ.md` | NEW (M-1) |
| `{TICKER}_RQ2_ADVERSARIAL_RQ.md` | NEW (M-2) |
| `{TICKER}_RQ3_MAINLINE_SCENARIOS_RQ.md` | NEW (M-3a) |
| `{TICKER}_RQ4_TAIL_SCENARIOS_RQ.md` | NEW (M-3b) |
| `{TICKER}_RQ5_DYNAMIC1_RQ.md` | NEW (D-1) |
| `{TICKER}_RQ6_DYNAMIC2_RQ.md` | NEW (D-2) |
| `{TICKER}_RQ7_DYNAMIC3_RQ.md` | NEW (D-3) |

### ENRICH Stage Canonical Snapshot (20 files)
| File | Origin |
|------|--------|
| `{TICKER}_A1_EPISTEMIC_ANCHORS_ENRICH.json` | COPIED from RQ |
| `{TICKER}_A2_ANALYTIC_KG_ENRICH.json` | MODIFIED |
| `{TICKER}_A3_CAUSAL_DAG_ENRICH.json` | MODIFIED |
| `{TICKER}_A5_GIM_ENRICH.json` | MODIFIED |
| `{TICKER}_A6_DR_ENRICH.json` | MODIFIED |
| `{TICKER}_A7_VALUATION_ENRICH.json` | MODIFIED (T2 kernel) |
| `{TICKER}_A8_RESEARCH_PLAN_ENRICH.json` | COPIED from RQ |
| `{TICKER}_A9_RESEARCH_RESULTS_ENRICH.json` | COPIED from RQ |
| `{TICKER}_A9_ENRICHMENT_TRACE_ENRICH.json` | NEW |
| `{TICKER}_N1_THESIS_ENRICH.md` | COPIED from RQ |
| `{TICKER}_N2_IC_ENRICH.md` | COPIED from RQ |
| `{TICKER}_N3_ECON_GOV_ENRICH.md` | COPIED from RQ |
| `{TICKER}_N4_RISK_ENRICH.md` | COPIED from RQ |
| `{TICKER}_N5_ENRICHMENT_ENRICH.md` | NEW |
| `{TICKER}_RQ1_INTEGRITY_ENRICH.md` | COPIED from RQ |
| `{TICKER}_RQ2_ADVERSARIAL_ENRICH.md` | COPIED from RQ |
| `{TICKER}_RQ3_MAINLINE_SCENARIOS_ENRICH.md` | COPIED from RQ |
| `{TICKER}_RQ4_TAIL_SCENARIOS_ENRICH.md` | COPIED from RQ |
| `{TICKER}_RQ5_DYNAMIC1_ENRICH.md` | COPIED from RQ |
| `{TICKER}_RQ6_DYNAMIC2_ENRICH.md` | COPIED from RQ |
| `{TICKER}_RQ7_DYNAMIC3_ENRICH.md` | COPIED from RQ |

### SCENARIO Stage Canonical Snapshot (22 files)
| File | Origin |
|------|--------|
| `{TICKER}_A1_EPISTEMIC_ANCHORS_SCEN.json` | COPIED from ENRICH |
| `{TICKER}_A2_ANALYTIC_KG_SCEN.json` | COPIED from ENRICH |
| `{TICKER}_A3_CAUSAL_DAG_SCEN.json` | COPIED from ENRICH |
| `{TICKER}_A5_GIM_SCEN.json` | COPIED from ENRICH |
| `{TICKER}_A6_DR_SCEN.json` | COPIED from ENRICH |
| `{TICKER}_A7_VALUATION_SCEN.json` | COPIED from ENRICH |
| `{TICKER}_A8_RESEARCH_PLAN_SCEN.json` | COPIED from ENRICH |
| `{TICKER}_A9_RESEARCH_RESULTS_SCEN.json` | COPIED from ENRICH |
| `{TICKER}_A9_ENRICHMENT_TRACE_SCEN.json` | COPIED from ENRICH |
| `{TICKER}_A10_SCENARIO_SCEN.json` | NEW (T2 kernel) |
| `{TICKER}_N1_THESIS_SCEN.md` | COPIED from ENRICH |
| `{TICKER}_N2_IC_SCEN.md` | COPIED from ENRICH |
| `{TICKER}_N3_ECON_GOV_SCEN.md` | COPIED from ENRICH |
| `{TICKER}_N4_RISK_SCEN.md` | COPIED from ENRICH |
| `{TICKER}_N5_ENRICHMENT_SCEN.md` | COPIED from ENRICH |
| `{TICKER}_N6_SCENARIO_SCEN.md` | NEW |
| `{TICKER}_RQ1_INTEGRITY_SCEN.md` | COPIED from ENRICH |
| `{TICKER}_RQ2_ADVERSARIAL_SCEN.md` | COPIED from ENRICH |
| `{TICKER}_RQ3_MAINLINE_SCENARIOS_SCEN.md` | COPIED from ENRICH |
| `{TICKER}_RQ4_TAIL_SCENARIOS_SCEN.md` | COPIED from ENRICH |
| `{TICKER}_RQ5_DYNAMIC1_SCEN.md` | COPIED from ENRICH |
| `{TICKER}_RQ6_DYNAMIC2_SCEN.md` | COPIED from ENRICH |
| `{TICKER}_RQ7_DYNAMIC3_SCEN.md` | COPIED from ENRICH |

### SILICON COUNCIL Stage Canonical Snapshot (29 files)
| File | Origin |
|------|--------|
| *(All 22 files from SCENARIO copied with _SC suffix)* | COPIED from SCEN |
| `{TICKER}_SC_ACCOUNTING_AUDIT_SC.json` | NEW |
| `{TICKER}_SC_FIT_AUDIT_SC.json` | NEW |
| `{TICKER}_SC_EPISTEMIC_AUDIT_SC.json` | NEW |
| `{TICKER}_SC_RED_TEAM_AUDIT_SC.json` | NEW |
| `{TICKER}_SC_DISTRIBUTIONAL_AUDIT_SC.json` | NEW |
| `{TICKER}_SC_ECONOMIC_REALISM_AUDIT_SC.json` | NEW |
| `{TICKER}_A11_AUDIT_SC.json` | NEW (consolidated) |

### INTEGRATION Stage Canonical Snapshot (31 files)
| File | Origin |
|------|--------|
| `{TICKER}_A1_EPISTEMIC_ANCHORS_INT.json` | MODIFIED (adjudicated) |
| `{TICKER}_A2_ANALYTIC_KG_INT.json` | MODIFIED (adjudicated) |
| `{TICKER}_A3_CAUSAL_DAG_INT.json` | MODIFIED (adjudicated) |
| `{TICKER}_A5_GIM_INT.json` | MODIFIED (adjudicated) |
| `{TICKER}_A6_DR_INT.json` | MODIFIED (adjudicated) |
| `{TICKER}_A7_VALUATION_INT.json` | MODIFIED (T2 kernel if cascade) |
| `{TICKER}_A8_RESEARCH_PLAN_INT.json` | COPIED from SC |
| `{TICKER}_A9_RESEARCH_RESULTS_INT.json` | COPIED from SC |
| `{TICKER}_A9_ENRICHMENT_TRACE_INT.json` | COPIED from SC |
| `{TICKER}_A10_SCENARIO_INT.json` | MODIFIED (adjudicated) |
| `{TICKER}_A11_AUDIT_INT.json` | COPIED from SC |
| `{TICKER}_A12_CASCADE_INT.json` | NEW |
| `{TICKER}_N1_THESIS_INT.md` | MODIFIED (if revised) |
| `{TICKER}_N2_IC_INT.md` | MODIFIED (if revised) |
| `{TICKER}_N3_ECON_GOV_INT.md` | MODIFIED (if revised) |
| `{TICKER}_N4_RISK_INT.md` | MODIFIED (if revised) |
| `{TICKER}_N5_ENRICHMENT_INT.md` | MODIFIED (if revised) |
| `{TICKER}_N6_SCENARIO_INT.md` | MODIFIED (if revised) |
| `{TICKER}_N7_ADJUDICATION_INT.md` | NEW |
| `{TICKER}_RQ1_INTEGRITY_INT.md` | COPIED from SC |
| `{TICKER}_RQ2_ADVERSARIAL_INT.md` | COPIED from SC |
| `{TICKER}_RQ3_MAINLINE_SCENARIOS_INT.md` | COPIED from SC |
| `{TICKER}_RQ4_TAIL_SCENARIOS_INT.md` | COPIED from SC |
| `{TICKER}_RQ5_DYNAMIC1_INT.md` | COPIED from SC |
| `{TICKER}_RQ6_DYNAMIC2_INT.md` | COPIED from SC |
| `{TICKER}_RQ7_DYNAMIC3_INT.md` | COPIED from SC |
| `{TICKER}_SC_*_AUDIT_INT.json` | COPIED from SC (6 files) |
| `{TICKER}_CVR_STATE4_INT.md` | NEW (T3 concatenation) |

### IRR Stage Canonical Snapshot (34 files)
| File | Origin |
|------|--------|
| *(All 31 files from INTEGRATION copied with _IRR suffix)* | COPIED from INT |
| `{TICKER}_A13_RESOLUTION_IRR.json` | NEW |
| `{TICKER}_A14_IRR_ANALYSIS_IRR.json` | NEW (T2 kernel) |
| `{TICKER}_N7_IRR_IRR.md` | NEW |

---

## Section 3: Pattern 12 - Canonical Snapshot with Orchestrator Copy-Forward

**Problem:** Tracking which artifact came from which stage (A1 from BASE, A2 from ENRICH, A10 from SCEN) creates complex provenance logic that invites orchestration errors.

**Solution:** Each stage folder contains a COMPLETE snapshot of all artifacts. Orchestrator copies forward unchanged files via `cp` before each stage.

**Critical:** Copy operation uses `cp` command (Bash tool), NOT Claude read/write. If Claude reads a file to "copy" it, truncation can occur.

**Orchestrator Protocol (between stages):**

```bash
# Example: After ENRICH completes, before SCENARIO starts

# Step 1: Create SCENARIO folder
mkdir -p {analysis_dir}/06_SCENARIO

# Step 2: Copy ALL artifacts from ENRICH with suffix rename
for f in {analysis_dir}/05_ENRICH/{TICKER}_*_ENRICH.json; do
  base=$(basename "$f" | sed 's/_ENRICH\.json$//')
  cp "$f" "{analysis_dir}/06_SCENARIO/${base}_SCEN.json"
done

for f in {analysis_dir}/05_ENRICH/{TICKER}_*_ENRICH.md; do
  base=$(basename "$f" | sed 's/_ENRICH\.md$//')
  cp "$f" "{analysis_dir}/06_SCENARIO/${base}_SCEN.md"
done

# Step 3: Spawn SCENARIO subagent
# Subagent creates/overwrites only what it changes (A10, N6)
# All other files already present with _SCEN suffix
```

**Subagent Instruction:**
- "Load all files from {stage_folder}/"
- "Output only artifacts you CREATE or MODIFY"
- "Unchanged artifacts are already in folder (copied by orchestrator)"

**Benefits:**
1. No provenance tracking - just "load from previous folder"
2. Claude never touches unchanged files
3. Each folder is a complete state snapshot
4. Simple debugging - compare folders to see what changed

---

## Section 4: Pattern 13 - Kernel Execution Receipts

**Problem:** Need verifiable proof of kernel execution for reproducibility.

**Solution:** Each T2 (kernel execution) produces a receipt artifact:

```json
{
  "artifact_type": "KERNEL_EXECUTION_RECEIPT",
  "ticker": "DAVE",
  "stage": "BASE",
  "timestamp": "2024-12-22T10:30:00Z",
  "kernel": {
    "file": "BASE_CVR_KERNEL_2.2.3e.py",
    "version": "2.2.3e",
    "sha256": "abc123..."
  },
  "inputs": {
    "a5_gim": "{TICKER}_A5_GIM_BASE.json",
    "a6_dr": "{TICKER}_A6_DR_BASE.json"
  },
  "command": "python3 BASE_CVR_KERNEL_2.2.3e.py --a5 ... --a6 ... --output ...",
  "outputs": {
    "a7_valuation": "{TICKER}_A7_VALUATION_BASE.json"
  },
  "exit_code": 0,
  "execution_time_seconds": 2.3
}
```

**Naming:** `{TICKER}_KERNEL_RECEIPT_{STAGE}.json`

**Reproducibility:** Copy inputs + kernel to Colab, run command, verify outputs match.

---

## Section 5: Final CVR Generation (Post-IRR)

**Problem:** Claude truncates consolidated markdown when asked to produce it. Intermediate concatenation at each stage is unnecessary overhead.

**Solution:** Generate the final human-readable CVR document ONCE, after the entire pipeline completes (post-IRR). Use a Bash script, not Claude.

### What Goes In the Final CVR

**INCLUDE (in order):**
1. Header (ticker, date, E[IVPS], E[IRR], Pipeline Fit grade)
2. **N1:** Investment Thesis
3. **N2:** Invested Capital Modeling
4. **N3:** Economic Governor & Constraints
5. **N4:** Risk Assessment
6. **N5:** Enrichment Synthesis
7. **N6:** Scenario Model Synthesis
8. **N7:** IRR & Expected Return Analysis
9. **A.1-A.7:** Epistemic anchors through valuation
10. **A.10:** Scenario model
11. **A.12-A.14:** Integration trace, resolution timeline, IRR analysis

**EXCLUDE (remain in folder for audit trail):**
- RQ1-RQ7 (research inputs)
- A.8, A.9 (research plan/results)
- SC_* audits, A.11 (audit trail - findings already adjudicated into A.12)
- Kernel receipts (reproducibility artifacts)
- PIPELINE_STATE.md (orchestration state)

### Concat Script

```bash
#!/bin/bash
# workshop/scripts/generate_final_cvr.sh
# Run AFTER IRR stage completes

TICKER=$1
IRR_DIR=$2
OUTPUT_FILE="${TICKER}_FINAL_CVR.md"

echo "# CAPY Final CVR: ${TICKER}" > $OUTPUT_FILE
echo "Generated: $(date)" >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

# Narratives (N1-N7)
for n in N1 N2 N3 N4 N5 N6 N7; do
  f=$(ls ${IRR_DIR}/*_${n}_*_IRR.md 2>/dev/null | head -1)
  if [ -f "$f" ]; then
    echo "---" >> $OUTPUT_FILE
    echo "## ${n}: $(basename $f)" >> $OUTPUT_FILE
    cat "$f" >> $OUTPUT_FILE
    echo "" >> $OUTPUT_FILE
  fi
done

# Core artifacts (A.1-A.7, A.10, A.12-A.14)
for a in A1 A2 A3 A5 A6 A7 A10 A12 A13 A14; do
  f=$(ls ${IRR_DIR}/*_${a}_*_IRR.json 2>/dev/null | head -1)
  if [ -f "$f" ]; then
    echo "---" >> $OUTPUT_FILE
    echo "## ${a}: $(basename $f)" >> $OUTPUT_FILE
    echo '```json' >> $OUTPUT_FILE
    cat "$f" >> $OUTPUT_FILE
    echo '```' >> $OUTPUT_FILE
    echo "" >> $OUTPUT_FILE
  fi
done

echo "Generated: $OUTPUT_FILE"
```

**Usage:** `./generate_final_cvr.sh DAVE 09_IRR/`

### Why This Approach

1. **Single concatenation:** No intermediate docs at INTEGRATION or other stages
2. **Bash, not Claude:** Avoids truncation entirely
3. **Curated content:** Final CVR contains analytical output, not working papers
4. **Audit trail preserved:** RQs, SC audits remain in folders for reproducibility

---

## Section 7: Terminal ROIC Bug Fix (Kernel Bug #2)

**Problem:** Current kernel derives terminal g from NOPAT growth, then uses ROIC for reinvestment rate. ROIC is unreliable due to accounting artifacts in Invested Capital modeling.

**Root Cause:** IC is hard to model consistently across securities (sometimes in cash flow statement, sometimes hidden in income statement). This causes ROIC to be unreliable, which propagates to reinvestment rate errors.

**Solution:** Derive g from topline growth (revenue and EBIT), which the model handles reliably.

### Current Code (Problematic)
```python
# Lines 400-436 in BASE_CVR_KERNEL_2.2.2e.py
terminal_roic_r = forecast_df['ROIC'].iloc[-1]  # Unreliable
terminal_g = np.mean(nopat_growth_rates[-3:])   # Depends on ROIC
reinvestment_rate = terminal_g / terminal_roic_r  # Garbage in, garbage out
```

### Fixed Code
```python
# === TERMINAL GROWTH DERIVATION ===
# Derive g from topline growth (revenue/EBIT), NOT from ROIC/IC relationship.
# Revenue and EBIT growth are modeled reliably; IC is accounting-dependent.

revenue_growth_rates = forecast_df['Revenue'].pct_change().values[1:]
ebit_growth_rates = forecast_df['EBIT'].pct_change().values[1:]

revenue_g = np.mean(revenue_growth_rates[-3:])
ebit_g = np.mean(ebit_growth_rates[-3:])

# Use average of the two (not min - avoid over-conservatism)
terminal_g_estimate = (revenue_g + ebit_g) / 2

# Apply cap: GDP × 1.4 (allows above-GDP growth, prevents excess)
# Rationale: Some companies legitimately grow faster than GDP at terminal.
# Cap at 1.4× GDP to allow for share-gainers while preventing absurd values.
GDP_PROXY = 0.025
GDP_MULTIPLIER = 1.4
terminal_g_cap = GDP_PROXY * GDP_MULTIPLIER  # 3.5%

# Also respect RFR if available (natural ceiling)
if rfr is not None:
    terminal_g_cap = min(terminal_g_cap, rfr)

terminal_g = min(terminal_g_estimate, terminal_g_cap)
terminal_g = max(terminal_g, 0)  # Floor at 0

# Final sanity check against DR
if terminal_g >= dr:
    logger.warning(f"Terminal g ({terminal_g:.4f}) >= DR ({dr:.4f}). Capping at 80% of DR.")
    terminal_g = dr * 0.80

# === REINVESTMENT RATE ===
# Use ROIC anchor from A.1 epistemic anchors, NOT modeled ROIC
roic_anchor = core_data.get('ROIC_anchor', 0.15)  # From A.1 industry median
reinvestment_rate_terminal = terminal_g / roic_anchor if roic_anchor > EPSILON else 0

# Cap reinvestment at 100% (can't reinvest more than you earn)
reinvestment_rate_terminal = min(reinvestment_rate_terminal, 1.0)

logger.info(f"Terminal: g={terminal_g:.4f} (from topline), "
            f"reinvestment={reinvestment_rate_terminal:.4f} (ROIC anchor={roic_anchor:.4f})")
```

### Upstream Requirement

**A.1 must include `ROIC_p50`** (industry median ROIC from base rates) for reinvestment calculation.

### Files to Modify

| File | Change |
|------|--------|
| `BASE_CVR_KERNEL_2.2.2e.py` | Lines ~400-450: Replace terminal g logic |
| `CVR_KERNEL_ENRICH_2.2.2e.py` | Same section |
| `CVR_KERNEL_SCEN_2_2_2e.py` | Same section |
| `CVR_KERNEL_INT_2_2_2e.py` | Same section |
| `CVR_KERNEL_IRR_2.2.5e.py` | Same section |
| `G3BASE_2.2.2e_SCHEMAS.md` | Add `ROIC_anchor` to A.1 schema |

---

## Section 8: REFINE Handshake Fix (TODO #1)

**Problem:** REFINE focuses on DAG expansion but doesn't explicitly preserve Equity Bridge items (FDSO, Total_Debt, Excess_Cash, Minority_Interest). These can get lost, causing IVPS calculation errors (e.g., 13.5M shares vs 14.5M).

**Solution:** Add explicit preservation check to REFINE Section C (Y0 Calibration).

### Change 1: Section C Output Format (lines 286-292)

**Current:**
```
=== Y0 CALIBRATION ===
Revenue: Model [X] vs Reported [Y] → [Z]% [PASS/FAIL]
EBIT: Model [X] vs Reported [Y] → [Z]% [PASS/FAIL]
Invested_Capital: Model [X] vs Reported [Y] → [Z]% [PASS/FAIL]

Calibration Status: [PASS / FAIL - requires iteration]
```

**Fixed:**
```
=== Y0 CALIBRATION ===
Revenue: Model [X] vs Reported [Y] → [Z]% [PASS/FAIL]
EBIT: Model [X] vs Reported [Y] → [Z]% [PASS/FAIL]
Invested_Capital: Model [X] vs Reported [Y] → [Z]% [PASS/FAIL]
Equity Bridge: [FDSO, Total_Debt, Excess_Cash, Minority_Interest] → Preserved from T1 [YES/NO]

Calibration Status: [PASS / FAIL - requires iteration]
```

### Change 2: Critical Reminders Section (line 350)

**Add new bullet:**
```markdown
- **Equity Bridge items (FDSO, Total_Debt, Excess_Cash, Minority_Interest) must be preserved unchanged from T1. These drive IVPS calculation.**
```

### Files to Modify

| File | Change |
|------|--------|
| `BASE_T1_REFINE_v1_2.md` → `v1_3.md` | Add Equity Bridge line to Section C, add Critical Reminder |

---

## Section 6: Autonomous Permissions Configuration

**Problem:** A 2-3 hour pipeline cannot have permission prompts interrupting execution. Claude Code's default behavior asks for confirmation on Bash commands, file writes, etc.

**Solution:** Configure `.claude/settings.json` in the CAPY project root to grant all necessary permissions upfront.

### Required Settings File

**File:** `CAPY/.claude/settings.json` (commit to git)

```json
{
  "permissions": {
    "allow": [
      "Bash(*)",
      "Read(**)",
      "Edit(**)",
      "Write(**)",
      "WebFetch",
      "WebSearch",
      "Glob",
      "Grep"
    ],
    "defaultMode": "acceptEdits"
  }
}
```

### Permission Breakdown

| Permission | Purpose |
|------------|---------|
| `Bash(*)` | All shell commands (kernel execution, git, file ops) |
| `Read(**)` | Read any file recursively (source docs, artifacts) |
| `Edit(**)` | Edit any file recursively (prompt iteration) |
| `Write(**)` | Write any file recursively (artifacts, outputs) |
| `WebFetch` | Fetch web content (documentation, references) |
| `WebSearch` | Live market price lookup (IRR stage mandatory) |
| `Glob` | File pattern matching |
| `Grep` | Content search |
| `defaultMode: acceptEdits` | Auto-accept file modifications without prompt |

### Why This Configuration

1. **Bash(*)** - Kernels execute via `python3 kernel.py --args`. Without this, every kernel call prompts.
2. **WebSearch** - IRR T1 MUST fetch live market price. Without this, pipeline halts waiting for permission.
3. **defaultMode: acceptEdits** - Subagents write artifacts directly to disk. Without this, every Write prompts.

### Alternative: CLI Flag

For one-off runs without modifying settings:
```bash
claude --dangerously-skip-permissions "CAPY: RUN DAVE"
```

But the settings.json approach is preferred for repeatability and team consistency.

### Files to Create

| File | Action |
|------|--------|
| `CAPY/.claude/settings.json` | CREATE with permissions above |

---

## Section 9: Full Pipeline Orchestration (Production CLAUDE.md)

**Problem:** Production CLAUDE.md has individual stage commands but no single command that chains the entire pipeline from PDF preprocessing to IRR.

**Solution:** Add `CAPY: RUN {TICKER}` command that orchestrates all stages.

### New Command: CAPY: RUN {TICKER}

```markdown
### CAPY: RUN {TICKER}

**Executes the FULL CAPY pipeline from raw PDFs to IRR.**

This is the one-click autonomous execution command. User provides raw PDFs; pipeline produces complete CVR with E[IRR].

```
┌─────────────────────────────────────────────────────────────┐
│  CAPY: RUN {TICKER} (Full Autonomous Pipeline)             │
├─────────────────────────────────────────────────────────────┤
│  Stage 0: PDF_PREPROCESSING                                 │
│     └── Check source_library/{TICKER}/ for raw PDFs        │
│         If *.extracted.md missing or stale → run SOURCE:   │
│         UPLOAD preprocessing (pdfplumber + pdf2image)      │
│         Output: *.extracted.md files ready for analysis    │
│                                                             │
│  Stage 1: INIT                                              │
│     └── Create analysis folder, copy sources to 00_source/ │
│                                                             │
│  Stage 2: BASE_PIPELINE (T1 → REFINE → T2)                 │
│     └── Validate after each turn → FAIL? Stop              │
│                                                             │
│  Stage 3: RQ_STAGE (RQ_GEN → 7× parallel RQ_ASK)           │
│     └── Validate A.8, A.9 → FAIL? Stop                     │
│                                                             │
│  Stage 4: ENRICH_STAGE (T1 → T2)                           │
│     └── Validate → FAIL? Stop                              │
│                                                             │
│  Stage 5: SCENARIO_STAGE (T1 → T2)                         │
│     └── Validate A.10 → FAIL? Stop                         │
│                                                             │
│  Stage 6: SILICON_COUNCIL (6× parallel audits → A.11)      │
│     └── Validate → FAIL? Stop                              │
│                                                             │
│  Stage 7: INTEGRATION (T1 → T2 → T3)                       │
│     └── Validate each turn → FAIL? Stop                    │
│                                                             │
│  Stage 8: IRR (T1 → T2)                                    │
│     └── Validate → COMPLETE                                │
│                                                             │
│  Stage 9: FINAL_CVR                                         │
│     └── Run generate_final_cvr.sh to produce consolidated  │
│         human-readable document (Section 5)                │
└─────────────────────────────────────────────────────────────┘
```

**Behavior:**
- Runs autonomously without human checkpoints (use individual stage commands for debugging)
- Updates PIPELINE_STATE.md after each stage
- On validation failure: Stops and reports
- On fatal error: Writes error state, stops cleanly

**Prerequisite:** `source_library/{TICKER}/` must exist with raw PDF files (10-K, 10-Q, transcripts, presentations). Stage 0 handles preprocessing.
```

### Stage 0: PDF Preprocessing Details

Stage 0 invokes the existing `SOURCE: UPLOAD` preprocessing logic:

1. **Check for raw PDFs:** `source_library/{TICKER}/*.pdf`
2. **Check for existing extractions:** `source_library/{TICKER}/*.extracted.md`
3. **If extractions missing or older than PDFs:** Run preprocessing
   - `pdfplumber` for text-based PDFs (filings, transcripts)
   - `pdf2image` + filtering for visual content (earnings decks, presentations)
4. **Output:** `*.extracted.md` files in same folder
5. **Proceed to Stage 1** with preprocessed sources

**Note:** If user has already run `SOURCE: UPLOAD {TICKER}` manually, Stage 0 detects existing `.extracted.md` files and skips preprocessing (idempotent).

### Individual Stage Commands

For debugging, users can run stages individually. Production CLAUDE.md documents:
- `CAPY: RUN BASE_STAGE` - Just BASE pipeline (T1 → REFINE → T2)
- `CAPY: RUN RQ_STAGE` - Just RQ generation and execution
- `CAPY: RUN ENRICH_STAGE` - Just ENRICH (T1 → T2)
- `CAPY: RUN SCENARIO_STAGE` - Just SCENARIO (T1 → T2)
- `CAPY: RUN SC_STAGE` - Just Silicon Council (6× parallel audits)
- `CAPY: RUN INT_STAGE` - Just INTEGRATION (T1 → T2 → T3)
- `CAPY: RUN IRR_STAGE` - Just IRR (T1 → T2)

These exist in workshop CLAUDE.md and must be ported to production.

---

## Section 10: Multi-Stage Autonomous Execution

### Pipeline State Document

After each turn/stage, orchestrator updates:

**File:** `{analysis_dir}/PIPELINE_STATE.md`

```markdown
# CAPY Pipeline State: {TICKER}
Last updated: {timestamp}

## Current Position
- **Stage:** ENRICH
- **Turn:** T2
- **Status:** COMPLETE

## Completed Stages
| Stage | Status | E[IVPS] | Key Metric | Timestamp |
|-------|--------|---------|------------|-----------|
| BASE | ✓ | $241.72 | DR=13.0% | 2024-12-22T10:00 |
| RQ | ✓ | - | 7/7 queries | 2024-12-22T10:30 |
| ENRICH | ✓ | $199.25 | DR=13.25% | 2024-12-22T11:00 |

## Next Stage
- **Stage:** SCENARIO
- **Inputs:** 20 files in 05_ENRICH/
- **Expected outputs:** A10, N6

## File Manifest (Current Canonical Snapshot)
[List of all files in current stage folder]
```

### Auto-Compact Recovery Protocol

When context compacts mid-pipeline:
1. Orchestrator re-reads PIPELINE_STATE.md
2. Identifies current stage and turn
3. Re-reads relevant canonical snapshot (previous stage folder)
4. Continues from where it left off

---

## Section 11: Validator Rewrite

### New Validator Requirements

**1. Input/Output Verification**
```markdown
## File Presence Check
- [ ] All expected input files present (per canonical snapshot)
- [ ] All expected output files created
- [ ] File naming matches convention: {TICKER}_{ARTIFACT}_{STAGE}.{ext}
- [ ] No orphan files (unexpected files in folder)
```

**2. Kernel Execution Verification**
```markdown
## Kernel Execution Proof
- [ ] KERNEL_RECEIPT_{STAGE}.json exists
- [ ] exit_code = 0
- [ ] Output values have 4+ decimal precision (proves real execution)
  - Example: 199.2534712... = REAL
  - Example: 199.25 = LIKELY SIMULATED (Claude rounded)
- [ ] Input file hashes match receipt
- [ ] Output file matches kernel stdout
```

**3. Labeling Consistency**
```markdown
## Labeling Check
- [ ] All files have correct stage suffix (_BASE, _ENRICH, etc.)
- [ ] PIPELINE_STATE.md updated with correct stage
- [ ] No stale suffixes from prior stages
```

---

## Section 12: Files to Modify

### Phase 1: Foundation

| File | Change |
|------|--------|
| `workshop/CLAUDE.md` | Add Pattern 12/13, update all stage flows |
| `production/CLAUDE.md` | Add CAPY: RUN {TICKER}, add missing stage docs |
| `shared/PATTERNS.md` | Add Pattern 12, 13 documentation |

### Phase 2: Kernel Fixes

| File | Change |
|------|--------|
| `BASE_CVR_KERNEL_2.2.2e.py` → `2.2.3e` | Terminal g fix (Section 7) |
| `CVR_KERNEL_ENRICH_2.2.2e.py` → `2.2.3e` | Same |
| `CVR_KERNEL_SCEN_2_2_2e.py` → `2.2.3e` | Same |
| `CVR_KERNEL_INT_2_2_2e.py` → `2.2.3e` | Same |
| `CVR_KERNEL_IRR_2.2.5e.py` → `2.2.6e` | Same |

### Phase 3: Prompt Fixes

| File | Change |
|------|--------|
| `BASE_T1_REFINE_v1_2.md` → `v1_3` | Equity Bridge fix (Section 8) |
| `G3BASE_2.2.2e_PROMPT.md` → `2.2.3e` | Currency Detection section (Section 13) |
| `G3BASE_2.2.2e_SCHEMAS.md` → `2.2.3e` | Add ROIC_anchor to A.1, currency to A.2, DR methodology update |
| `G3BASE_2.2.2e_NORMDEFS.md` → `2.2.3e` | DR rubric recalibration - global universe (Section 14) |
| `G3ENRICH_2.2.2e_PROMPT.md` → `2.2.3e` | Currency verification (inherit from A.2) |
| `G3ENRICH_2.2.2e_NORMDEFS.md` → `2.2.3e` | DR rubric recalibration (consistency with BASE) |
| All stage prompts | Atomized output mandate (Section V rewrite) |

### Phase 4: New Files

| File | Purpose |
|------|---------|
| `CAPY/.claude/settings.json` | Autonomous permissions (Section 6) |
| `workshop/scripts/generate_final_cvr.sh` | Post-pipeline CVR concatenation |
| Per-stage validators | File presence checks |

---

## Section 13: Currency Auto-Detection Fix (TODO #4)

**Priority:** CRITICAL (destroys runs on any cross-listed company)

**Problem:** No explicit currency guidance in BASE prompt. Cross-listed securities (e.g., ADRs, dual-listings) may have financials in one currency (EUR, GBP) but trade in USD. The model can confuse currencies, producing nonsensical IVPS values.

**Example:** A UK-listed company reports in GBP. Without guidance, model might mix GBP revenues with USD prices, producing garbage.

**Solution:** Auto-detect currency from source financials and enforce throughout.

### Detection Logic

```
1. Read 10-K/10-Q headers for currency declaration
   - "Amounts in thousands except per share data" + country code
   - Explicit "Currency: EUR" or similar

2. If ambiguous, check which currency makes revenues realistic
   - $10B revenue for a mid-cap → probably wrong currency
   - €2B revenue for European small-cap → plausible

3. Default to currency of published financials (NOT trading exchange)
```

### Required Changes

**1. G3BASE_2.2.2e_PROMPT.md - Section I (Trigger)**

Add explicit currency detection step:

```markdown
## Currency Detection (MANDATORY)

Before beginning analysis, identify the REPORTING CURRENCY:

1. Check 10-K/10-Q cover page for currency declaration
2. Verify revenue/EBIT/assets are denominated in this currency
3. Document in A.2.market_context.reporting_currency

**All GIM, DR, IVPS calculations must be in REPORTING CURRENCY.**
**Convert market price to reporting currency for final IVPS comparison.**
```

**2. G3BASE_2.2.2e_SCHEMAS.md - A.2 Schema**

Add currency field to market_context:

```json
"market_context": {
  "ticker": "string",
  "primary_exchange": "string",
  "reporting_currency": "string",      // ADD: "USD", "EUR", "GBP", etc.
  "price_currency": "string",          // ADD: Currency of market price
  "fx_rate_to_reporting": "number",    // ADD: If price_currency != reporting_currency
  ...
}
```

**3. All Downstream Stages**

Must preserve and use `reporting_currency` from A.2. Kernels already work in consistent units; this just enforces documentation.

### Files to Modify

| File | Change |
|------|--------|
| `G3BASE_2.2.2e_PROMPT.md` → `2.2.3e` | Add Currency Detection section to trigger |
| `G3BASE_2.2.2e_SCHEMAS.md` → `2.2.3e` | Add currency fields to A.2 market_context |
| `G3ENRICH_2.2.2e_PROMPT.md` → `2.2.3e` | Inherit currency context (verify, don't re-detect) |
| All downstream prompts | No changes needed (inherit from A.2) |

### Validation

Smoke test on a cross-listed security (e.g., a European ADR) to verify currency propagation.

---

## Section 14: DR Rubric Recalibration (Global Securities Universe)

**Priority:** HIGH (produces systematically elevated discount rates)

**Problem:** The current X (Risk Multiplier) rubric produces a right-skewed distribution of discount rates that are too high. The model appears to be calibrated against S&P 500 securities (~500 companies), but this creates systematic bias:

1. **Right-skew:** Long tail of very high DRs, non-normal distribution
2. **Overcounting risk:** Model assigns high X values to securities that are "average" globally
3. **Range compression at low end:** Very few securities actually get X < 0.7, even stable monopolies

**Root Cause:** S&P 500 is a curated list of large, stable, US-listed companies. When the model treats S&P 500 as "average risk," anything smaller, younger, or non-US gets pushed toward the high end. But globally, there are 50,000+ publicly traded securities - S&P 500 represents the LOW-risk tail of the global distribution.

### Current Rubric (Problematic)

```
DR = RFR + (ERP × X)    where ERP = 5.0%, X ∈ [0.5, 2.2]

| X Range | Risk Profile |
|---------|--------------|
| 0.5 - 0.8 | Low risk (stable, profitable, low leverage) |
| 0.9 - 1.2 | Average risk |
| 1.3 - 1.6 | Above average risk |
| 1.7 - 2.2 | High risk (unprofitable, high leverage, early stage) |
```

**Issue:** At X=0.5, DR ≈ 6.75% (RFR 4.25% + 2.5%). Very few companies get this, even stable monopolies.
At X=1.8 (DAVE), DR ≈ 13.25%. But DAVE is a profitable fintech, not a speculative biotech.

### Fixed Rubric (Global Calibration)

```
DR = RFR + (ERP × X)    where ERP = 5.0%, X ∈ [0.5, 2.0]

| X Range | Risk Profile | Calibration Examples |
|---------|--------------|----------------------|
| 0.5 - 0.6 | Very low risk | Waste Management, utilities, quasi-monopolies with stable growing FCF |
| 0.6 - 0.8 | Low risk | Walmart, Microsoft, Apple, large diversified companies with moats |
| 0.8 - 1.0 | Below average | Google, typical S&P 500 industrial (Caterpillar, Honeywell) |
| 1.0 - 1.2 | Average (global) | Typical Russell 2000 company, profitable mid-cap growth |
| 1.2 - 1.5 | Above average | Small-cap with concentration risk, typical MSCI EM constituent |
| 1.5 - 1.8 | High risk | Small emerging market growth, unprofitable growth, early-stage |
| 1.8 - 2.0 | Very high risk | Speculative (quantum computing hype, poor-prospect biotech, near-fraud) |
```

### Key Changes

1. **Cap reduced:** 2.2 → 2.0 (reserves extreme high end for truly speculative securities)
2. **Explicit global calibration instruction:** Model must calibrate against 50,000+ global securities, not S&P 500
3. **Named anchors:** Provide concrete examples across the full range to guide calibration
4. **Redistribute middle:** A typical S&P 500 company is now ~0.8-0.9, not 1.0

### Implication for DAVE

Under global calibration:
- DAVE is a profitable US-listed fintech with $300M+ revenue
- Small-cap with some concentration risk (member base)
- Relative to global universe: Slightly above average risk
- Expected X: ~1.1-1.3 (not 1.8)
- Expected DR: ~9.75-10.75% (not 13.25%)

### Required Changes

**1. G3BASE_2.2.2e_NORMDEFS.md - Section B.3 (Discount Rate)**

Replace the X table with the new globally-calibrated version above, plus add:

```markdown
### Risk Multiplier Calibration (CRITICAL)

**Reference class:** The universe of 50,000+ globally traded public securities.
**NOT** the S&P 500 or any curated index of large-cap US stocks.

The S&P 500 represents the LOW-RISK tail of the global distribution. A typical
S&P 500 company should receive X ≈ 0.8-0.9, not X ≈ 1.0.

**Calibration Anchors:**
| Security | X | Rationale |
|----------|---|-----------|
| Waste Management (WM) | 0.5 | Quasi-monopoly, stable FCF, defensive |
| Walmart (WMT) | 0.65 | Scale moat, but retail disruption risk |
| Microsoft (MSFT) | 0.7 | Diversified, dominant, recurring revenue |
| Alphabet (GOOGL) | 0.85 | Tech risk, but dominant, profitable |
| Caterpillar (CAT) | 0.9 | Typical S&P 500 industrial |
| Typical Russell 2000 company | 1.1 | Average for global investable universe |
| Typical MSCI EM constituent | 1.4 | Governance, currency, less transparency |
| Small EM growth company | 1.7 | High execution and macro risk |
| Speculative pre-revenue | 1.9-2.0 | Near-zero margin of safety |

**Sanity check:** If your X > 1.5, the company should have clear pathological risk
factors (unprofitable, early stage, poor unit economics, governance red flags).
```

**2. G3BASE_2.2.2e_SCHEMAS.md - A.6 Schema**

Update DR derivation methodology description:

```json
"1.3_dr_derivation_methodology": {
  "DR_Static": "RFR + (ERP * X). X (Risk Multiplier) is calibrated against the global universe of 50,000+ public securities (NOT S&P 500). X ∈ [0.5, 2.0]."
}
```

### Files to Modify

| File | Change |
|------|--------|
| `G3BASE_2.2.2e_NORMDEFS.md` → `2.2.3e` | Replace X table, add global calibration instruction |
| `G3BASE_2.2.2e_SCHEMAS.md` → `2.2.3e` | Update DR methodology description |
| `G3ENRICH_2.2.2e_NORMDEFS.md` → `2.2.3e` | Same X table update (consistency) |

### Validation

Re-run DAVE smoke test after fix. Expected:
- X ≈ 1.1-1.3 (was 1.8)
- DR ≈ 9.75-10.75% (was 13.25%)
- IVPS should increase significantly (lower DR → higher PV)

---

## Implementation Phases

### Phase 1: Foundation (CLAUDE.md + Pattern Documentation)
- Add Pattern 12, 13 to shared/PATTERNS.md
- Update workshop/CLAUDE.md with explicit file enumeration
- Update production/CLAUDE.md with CAPY: RUN {TICKER} and missing stages
- Verify: Patterns documented, commands defined

### Phase 2: Full Pipeline Retrofit (BASE→IRR)
- Apply kernel fixes (terminal g) to all kernels
- Apply REFINE handshake fix
- Update all stage prompts with atomized output mandate
- Create/update validators for file presence checks
- Create concat_stage.sh script
- Full pipeline smoke test (DAVE BASE→IRR)

**Rationale:** Once patterns are established in Phase 1, all stages follow same approach. Full pipeline test validates everything.

---

## Verification Strategy

1. **Phase 1 validation:** CLAUDE.md changes reviewed, patterns documented
2. **Phase 2 validation:** Full pipeline test (DAVE BASE→IRR)
3. **File presence check:** All enumerated files exist at each stage
4. **Kernel verification:** E[IVPS] and E[IRR] match baseline (within floating point tolerance)
5. **Terminal g verification:** DAVE terminal g should be ~2-3% (from topline), not anomalous

---

## Success Criteria

1. No truncation in any artifact at any stage
2. Each stage's orchestrator section enumerates exact input files
3. Human audit files clearly marked `_AUDIT.md`
4. Full pipeline (DAVE) produces valid E[IVPS] and E[IRR]
5. Terminal g derived from topline growth, capped at GDP × 1.4
6. Equity Bridge items preserved through REFINE
7. All validators pass with individual file checks
8. `CAPY: RUN DAVE` executes autonomously from preprocessed sources to final IRR
9. Currency auto-detected from source financials and documented in A.2
10. DR calibrated against global universe (DAVE X ≈ 1.1-1.3, DR ≈ 9.75-10.75%)

---

## Rollback Plan

- Keep existing prompts as CANONICAL until each phase passes smoke test
- New atomized prompts use version bump (2.2.2e → 2.2.3e)
- If atomization fails, revert to embedded pattern for that stage
- Kernel fixes are backward compatible (only changes internal logic)
