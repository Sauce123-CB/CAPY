# WORKSHOP Handoff: BASE_PIPELINE Smoke Test Findings

**Date:** 2024-12-16
**Source:** CAPY_Production smoke test (DAVE)
**Run ID:** DAVE_CAPY_20251207_113714

---

## Executive Summary

Full BASE_PIPELINE smoke test completed. T1 and REFINE work correctly via Opus subagent dispatch. T2 revealed critical issues requiring both CLAUDE.md fixes (done) and prompt patches (WORKSHOP scope).

**Bottom line:** The pipeline executes end-to-end, but the kernel output reveals DAG/GIM configuration bugs that produce garbage financials. Prompts need patches to prevent these bugs upstream.

---

## What Worked

1. **T1 (Opus subagent):** Successfully generated investment thesis, 4 narratives, artifacts A.1-A.6
2. **REFINE (Opus subagent):** Successfully expanded DAG (9→15 nodes), calibrated DR, refined GIM
3. **T1/REFINE validators (Haiku):** Correctly passed valid outputs
4. **Kernel execution:** Ran successfully once schema issues were fixed

---

## What Failed

### 1. T2 Subagent Fabrication

**Problem:** When T2 was dispatched to a subagent, it "simulated" kernel execution instead of running Python. Output looked plausible (IVPS=$127.68) but was completely fabricated.

**Root cause:** Subagents can't reliably execute external Python. They narrate what they think the output should be.

**Fix applied (CLAUDE.md v0.2.2):** T2 must be executed by orchestrator directly via Bash, not subagent.

### 2. T2 Validator False Positive (Haiku)

**Problem:** Haiku validator returned PASS for fabricated T2 output. It couldn't distinguish simulated from real kernel execution.

**Fix applied (CLAUDE.md v0.2.2):** T2 validator now requires Opus model.

### 3. Schema Mismatches (REFINE → Kernel)

**Problem:** REFINE output used different JSON keys than kernel expects:
- REFINE: `A.3_CAUSAL_DAG.nodes` → Kernel expects: `A.3_CAUSAL_DAG.DAG`
- REFINE: `A.5_GESTALT_IMPACT_MAP.drivers` → Kernel expects: `A.5_GESTALT_IMPACT_MAP.GIM`
- REFINE: `coverage_manifest: {}` (empty) → Kernel requires populated manifest

**Fix applied (CLAUDE.md v0.2.2):** Documented schema fix step in T2 execution. Orchestrator repairs before kernel run.

**Fix needed (WORKSHOP):** Prompts should enforce correct schema upstream so repairs aren't needed.

### 4. DAG/GIM Configuration Bugs

**Problem:** Even after schema fixes, kernel output revealed fundamental modeling errors:

```json
"_execution_notes": {
  "warnings": [
    "Revenue_CAGR_Y1_Y5 is negative (-0.5%) - indicates DAG equation issues",
    "EBIT_Margin_Y5 is 55.7% - unrealistically high, DAG cost structure likely misconfigured",
    "ROIC values 80%+ throughout forecast - suggests Invested_Capital scaling issues",
    "Subscription_Revenue dominates by Y5 ($443K) vs ExtraCash ($5K) - revenue mix inverted"
  ]
}
```

**Root cause hypotheses:**
1. Unit inconsistencies (MTMs in millions vs thousands, revenue components not aligned)
2. GIM trajectories don't connect properly to DAG equations
3. No upstream validation that simulated trajectories produce plausible results

**Fix needed (WORKSHOP):** Add trajectory calibration to REFINE prompt.

---

## Required WORKSHOP Updates

### Update 1: REFINE Prompt v1_1 → v1_2

**File:** `prompts/refine/BASE_T1_REFINE_v1_2.md`

**Add Section 2.5: Trajectory Calibration (Hard Gate)**

```markdown
### 2.5 Trajectory Calibration (Hard Gate)

After Y0 calibration passes, simulate the DAG forward to verify computational and economic coherence.

**Step 1: Simulate Checkpoints**

Manually propagate the DAG at Y1, Y5, and Y10:
1. Apply GIM DSL to compute exogenous driver values at each checkpoint
2. Evaluate DAG equations in topological order
3. Record all GAAP line items: Revenue, Gross Profit, EBIT, NOPAT, Invested Capital, FCF, ROIC

**Step 2: Internal Consistency Checks**

Verify computational correctness:
- Components sum to aggregates (revenue segments → total revenue, cost items → total costs)
- No sign flips without economic justification
- No divide-by-zero or undefined values
- Units consistent across equations (thousands vs millions vs ratios)

**Step 3: Epistemic Anchor Comparison**

For each metric with a corresponding A.1 base rate distribution:
- Compare simulated terminal/convergence values to p10/p50/p90 bounds
- Values beyond p10 or p90 require explicit justification or bug diagnosis
- Document any justified outliers with reasoning

| Metric | Simulated Y10 | A.1 Range (p10-p90) | Status |
|--------|---------------|---------------------|--------|
| ROIC | | | |
| EBIT Margin | | | |
| Revenue Growth | | | |

**Step 4: Economic Plausibility**

Flag for review if:
- EBIT margin > 60% or < -20%
- ROIC > 50% sustained beyond Y5
- Revenue CAGR inverts sign vs. driver assumptions (e.g., positive growth drivers but declining revenue)
- Any major revenue/cost component flips from dominant to negligible (>50% to <10%) without thesis support

**Step 5: Repair Loop (If Checks Fail)**

1. Identify failure type:
   - **Dimensional**: Units mismatch → fix equation scaling factors
   - **Semantic**: Wrong variable reference → fix equation structure
   - **Parametric**: GIM values misconfigured → adjust DSL parameters

2. Trace root cause to first equation producing anomaly

3. Apply minimal targeted fix, preserving analytical intent

4. Re-run simulation to verify repair

5. Maximum 3 repair iterations before halting with documented errors

**Output Requirement**

Include calibration results in REFINE output:

```
=== TRAJECTORY CALIBRATION ===
Checkpoints Simulated: Y1, Y5, Y10

Metric          Y0      Y1      Y5      Y10     Status
Revenue ($K)
EBIT Margin
ROIC

Epistemic Anchor Comparison:
[Metric]: Simulated [X] vs p10-p90 [Y-Z] → [PASS/FLAG]

Repairs Applied: [None / List]

Calibration Status: [PASS / FAIL]
```

Do NOT emit final artifacts if calibration fails after 3 repair attempts.
```

**Add Section: Kernel Schema Requirements**

```markdown
### Schema Requirements (Kernel Compatibility)

Your JSON artifacts MUST use these exact structures for kernel compatibility:

#### A.3_CAUSAL_DAG Schema

```json
{
  "A.3_CAUSAL_DAG": {
    "DAG": {                          // NOT "nodes"
      "NodeName": {
        "type": "Exogenous_Driver" | "Endogenous_Driver" | "Financial_Line_Item",
        "parents": ["Parent1", "Parent2"],
        "equation": "GET('Parent1') * GET('Parent2')"
      }
    },
    "coverage_manifest": {            // MUST be populated, NOT empty
      "NodeName": "covered"
    }
  }
}
```

#### A.5_GESTALT_IMPACT_MAP Schema

```json
{
  "A.5_GESTALT_IMPACT_MAP": {
    "GIM": {                           // NOT "drivers"
      "DriverName": {
        "mode": "STATIC" | "LINEAR_FADE" | "CAGR_INTERP" | "EXPLICIT_SCHEDULE",
        "params": { ... }
      }
    }
  }
}
```

**Single DSL per driver:** Do NOT use multi-period formats like `Y1_Y3`, `Y4_Y10`. Each driver gets ONE DSL specification that covers the full forecast horizon.
```

---

### Update 2: G3BASE Prompt 2.2.1e → 2.2.2e

**File:** `prompts/base/G3BASE_2.2.2e.md`

**Add Section: Unit Conventions**

```markdown
### Unit Conventions

All values in A.2_ANALYTIC_KG.Y0_data use consistent units:

| Category | Unit | Example |
|----------|------|---------|
| Revenue, Costs, EBIT, etc. | Thousands ($000s) | 545500 = $545.5M |
| Members (Total_Members, MTMs) | Millions | 2.77 = 2.77M members |
| Per-unit metrics (CAC, Subscription_Price) | Dollars | 19 = $19 |
| Rates (Churn, ChargeOff, etc.) | Decimal | 0.15 = 15% |
| Originations, DaveCard_Spend | Actual count | 8000000 = 8M originations |

**DAG equation unit consistency:** When combining values with different units, equations must include appropriate scaling factors.

Example: Subscription_Revenue from MTMs (millions) and Price (dollars)
```
"equation": "GET('MTMs') * GET('Subscription_Price_Monthly') * 12 * 1000"
//          millions    *  dollars                        * months * scale to $000s
```
```

**Add Schema Examples to Artifact Specifications**

In each artifact section, add explicit JSON schema examples showing the exact key names the kernel expects (DAG not nodes, GIM not drivers, etc.).

---

### Update 3: Validator Prompt Enhancement (Optional)

**File:** `validators/CAPY_INTERTURN_VALIDATOR_CC.md`

**Add T2-specific check:**

```markdown
### T2-Specific Validation

For BASE_T2 stage, additionally verify:

1. **Kernel execution evidence:** Output must contain `_execution_notes` with `kernel_version` and `execution_status` fields that match the actual kernel (G3_2.2.1e)

2. **No simulation language:** Output must NOT contain phrases like "simulated", "would produce", "estimated based on" - these indicate fabrication

3. **Trajectory sanity:** Check that key metrics are plausible:
   - Revenue_CAGR_Y1_Y5 should be positive (or justified if negative)
   - EBIT_Margin should be < 60% (unless justified)
   - ROIC should be < 50% (unless justified as temporary)
```

---

## Deployment Checklist

When applying these updates in WORKSHOP:

1. [ ] Create `BASE_T1_REFINE_v1_2.md` with trajectory calibration + schema requirements
2. [ ] Create `G3BASE_2.2.2e.md` with unit conventions + schema examples
3. [ ] Update validator prompt with T2-specific checks (optional)
4. [ ] Test updated prompts with a fresh DAVE run
5. [ ] If tests pass, deploy to CAPY_Production/prompts/
6. [ ] Update CAPY_Production/VERSION.md with new prompt versions

---

## Files for Reference

From this smoke test (in CAPY_Production):

| File | Description |
|------|-------------|
| `analyses/DAVE_CAPY_20251207_113714/01_T1/DAVE_BASE_T1.md` | Working T1 output |
| `analyses/DAVE_CAPY_20251207_113714/02_REFINE/DAVE_BASE_REFINE.md` | Working REFINE output (has schema issues) |
| `analyses/DAVE_CAPY_20251207_113714/03_T2/DAVE_kernel_input.json` | Raw extracted JSON (has schema issues) |
| `analyses/DAVE_CAPY_20251207_113714/03_T2/DAVE_kernel_input_fixed.json` | Schema-corrected JSON (kernel runs) |
| `analyses/DAVE_CAPY_20251207_113714/03_T2/DAVE_kernel_output.json` | Actual kernel output (shows DAG/GIM bugs) |

---

## Summary

| Issue | Where Fixed | Status |
|-------|-------------|--------|
| T2 subagent fabrication | CLAUDE.md (Production) | Done |
| T2 validator false positive | CLAUDE.md (Production) | Done |
| Schema mismatch documentation | CLAUDE.md (Production) | Done |
| Schema enforcement upstream | REFINE prompt (WORKSHOP) | TODO |
| Trajectory calibration | REFINE prompt (WORKSHOP) | TODO |
| Unit conventions | G3BASE prompt (WORKSHOP) | TODO |

**Next action:** Open CAPY_Workshop and apply the prompt patches documented above.

---

## Patch Tracker Entry

Add this to `CAPY_Workshop/patches/PATCH_TRACKER.md`:

```markdown
## PATCH-2024-12-16-001: Trajectory Calibration & Schema Enforcement

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
| P3 | G3BASE_2.2.1e.md → 2.2.2e.md | Add unit conventions | MEDIUM |
| P4 | G3BASE_2.2.2e.md | Add schema examples to artifact specs | MEDIUM |
| P5 | CAPY_INTERTURN_VALIDATOR_CC.md | Add T2-specific checks | LOW |

### Evidence

- `CAPY_Production/analyses/DAVE_CAPY_20251207_113714/03_T2/DAVE_kernel_output.json` shows garbage financials
- `CAPY_Production/WORKSHOP_HANDOFF_20241216.md` has full details

### Acceptance Criteria

- [ ] Fresh DAVE smoke test passes T2 with plausible IVPS
- [ ] No schema repair step needed between REFINE and kernel
- [ ] Trajectory calibration catches implausible metrics before kernel execution
```
