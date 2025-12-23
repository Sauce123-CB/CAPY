#!/bin/bash
# rebuild_smoke_claude.sh
# Concatenates orchestration files into smoke_tests/CLAUDE.md
#
# Usage: ./rebuild_smoke_claude.sh
# Run from: workshop/scripts/ or workshop/
#
# This script generates a CLAUDE.md file for the smoke_tests/ directory
# that contains ALL orchestration inline, ensuring strong instruction following.

set -e

# Find workshop directory (script may be run from scripts/ or workshop/)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [[ "$SCRIPT_DIR" == */scripts ]]; then
    WORKSHOP_DIR="$(dirname "$SCRIPT_DIR")"
else
    WORKSHOP_DIR="$SCRIPT_DIR"
fi

cd "$WORKSHOP_DIR"

OUT="smoke_tests/CLAUDE.md"
ORCH_DIR="orchestration"

# Ensure smoke_tests directory exists
mkdir -p smoke_tests

echo "Generating $OUT from $ORCH_DIR/*.md..."

# Write header
cat > "$OUT" << 'HEADER'
# CAPY Smoke Test Execution Environment

> **AUTO-GENERATED** - Do not edit directly
> **Rebuild:** `../scripts/rebuild_smoke_claude.sh`
> **Source:** `../orchestration/*.md`

This CLAUDE.md is purpose-built for pipeline execution. All orchestration
is inlined to ensure strong instruction following.

For development tasks (patching, versioning), use `../CLAUDE.md` instead.

---

## Quick Reference

**Working Directory:** All paths in this file are relative to `workshop/` (the parent directory).
When executing stages, work from `workshop/` context.

**Source Documents:** Located in `../production/source_library/{TICKER}/`

**Output Location:** `smoke_tests/{TICKER}_SMOKE_{YYYYMMDD}_{HHMMSS}/`

---

## RUN {START}->{END} {TICKER}

Execute pipeline stages from {START} through {END} for the given ticker.

**Valid stages:** SOURCE, BASE, RQ, ENRICH, SCENARIO, SC, INT, IRR

**Examples:**
- `RUN SOURCE->IRR DAVE` - Full pipeline
- `RUN BASE->ENRICH DAVE` - Partial pipeline
- `RUN SCENARIO->SCENARIO DAVE` - Single stage re-run

**Behavior:**
1. Validate prerequisites:
   - For SOURCE: Check `../production/source_library/{TICKER}/` has PDFs
   - For other starts: Check prior stage folder exists with complete artifacts
2. Create analysis folder if starting fresh: `{TICKER}_SMOKE_{YYYYMMDD}_{HHMMSS}/`
3. Execute each stage in sequence per orchestration below
4. **Run validators after each stage (MANDATORY - do not skip)**
5. Update PIPELINE_STATE.md after each stage
6. Stop on validation failure and report

**Critical Instructions:**
- Follow EVERY step in each stage's orchestration
- Do NOT skip validators - this is a common failure mode
- Use Bash `cp` for copy-forward, NOT Claude read/write
- Execute kernels via Bash, NOT manual calculation

---

## Pipeline Execution Checklist (MANDATORY)

**On receiving ANY `RUN` command, your FIRST action is TodoWrite.**

The todo list is your persistent execution state. It survives context compaction and ensures no steps are skipped. Create it BEFORE doing anything else.

### Master Template

| # | Stage | Task | content | activeForm |
|---|-------|------|---------|------------|
| 1 | SOURCE | Check PDFs | SOURCE: Check PDFs exist | Checking source PDFs |
| 2 | SOURCE | Preprocess | SOURCE: Run preprocessing | Preprocessing PDFs |
| 3 | SOURCE | Validate | SOURCE: Validate extraction | Validating extraction |
| 4 | SOURCE | Init folder | SOURCE: Create folder and copy | Creating analysis folder |
| 5 | BASE | T1 | BASE T1: Run subagent | Running BASE T1 |
| 6 | BASE | T1 validator | BASE T1: Validator | Validating BASE T1 |
| 7 | BASE | REFINE | BASE REFINE: Run subagent | Running REFINE |
| 8 | BASE | REFINE validator | BASE REFINE: Validator | Validating REFINE |
| 9 | BASE | T2 | BASE T2: Run kernel | Running BASE T2 kernel |
| 10 | BASE | T2 validator | BASE T2: Validator | Validating BASE T2 |
| 11 | BASE | Copy-forward | BASE: Copy-forward to RQ | Copying to RQ folder |
| 12 | RQ | RQ_GEN | RQ: Generate research plan | Generating RQ plan |
| 13 | RQ | RQ_GEN validator | RQ: RQ_GEN validator | Validating RQ plan |
| 14 | RQ | RQ_ASK | RQ: Execute 7 queries | Executing RQ queries |
| 15 | RQ | RQ_ASK validator | RQ: RQ_ASK validator | Validating RQ results |
| 16 | RQ | Copy-forward | RQ: Copy-forward to ENRICH | Copying to ENRICH folder |
| 17 | ENRICH | T1 | ENRICH T1: Run subagent | Running ENRICH T1 |
| 18 | ENRICH | T1 validator | ENRICH T1: Validator | Validating ENRICH T1 |
| 19 | ENRICH | T2 | ENRICH T2: Run kernel | Running ENRICH T2 kernel |
| 20 | ENRICH | T2 validator | ENRICH T2: Validator | Validating ENRICH T2 |
| 21 | ENRICH | Copy-forward | ENRICH: Copy-forward to SCENARIO | Copying to SCENARIO folder |
| 22 | SCENARIO | T1 | SCENARIO T1: Run subagent | Running SCENARIO T1 |
| 23 | SCENARIO | T1 validator | SCENARIO T1: Validator | Validating SCENARIO T1 |
| 24 | SCENARIO | T2 | SCENARIO T2: Run kernel | Running SCENARIO T2 kernel |
| 25 | SCENARIO | T2 validator | SCENARIO T2: Validator | Validating SCENARIO T2 |
| 26 | SCENARIO | Copy-forward | SCENARIO: Copy-forward to SC | Copying to SC folder |
| 27 | SC | Audits | SC: Run 6 parallel audits | Running Silicon Council |
| 28 | SC | Validator | SC: Validator | Validating SC audits |
| 29 | SC | Copy-forward | SC: Copy-forward to INT | Copying to INT folder |
| 30 | INT | T1 | INT T1: Run adjudication | Running INT T1 |
| 31 | INT | T1 validator | INT T1: Validator | Validating INT T1 |
| 32 | INT | T2 | INT T2: Run kernel | Running INT T2 kernel |
| 33 | INT | T2 validator | INT T2: Validator | Validating INT T2 |
| 34 | INT | T3 | INT T3: Generate State 4 CVR | Running INT T3 |
| 35 | INT | T3 validator | INT T3: Validator | Validating INT T3 |
| 36 | INT | Copy-forward | INT: Copy-forward to IRR | Copying to IRR folder |
| 37 | IRR | T1 | IRR T1: Resolution + market price | Running IRR T1 |
| 38 | IRR | T1 validator | IRR T1: Validator | Validating IRR T1 |
| 39 | IRR | T2 | IRR T2: Run kernel | Running IRR T2 kernel |
| 40 | IRR | T2 validator | IRR T2: Validator | Validating IRR T2 |
| 41 | FINAL | Generate CVR | FINAL: Generate consolidated CVR | Generating final CVR |

### Stage Index (for slicing)

| Stage | First Step | Last Step |
|-------|------------|-----------|
| SOURCE | 1 | 4 |
| BASE | 5 | 11 |
| RQ | 12 | 16 |
| ENRICH | 17 | 21 |
| SCENARIO | 22 | 26 |
| SC | 27 | 29 |
| INT | 30 | 36 |
| IRR | 37 | 40 |
| FINAL | 41 | 41 |

### TodoWrite Protocol

**On `RUN {START}->{END} {TICKER}`:**

1. Look up `{START}` in Stage Index → get First Step
2. Look up `{END}` in Stage Index → get Last Step
3. Slice Master Template rows [First:Last] inclusive
4. Call TodoWrite with sliced rows (all `status: "pending"`)
5. Begin execution at step 1 of your slice

**Example:** `RUN ENRICH->INT DAVE`
- ENRICH First = 17, INT Last = 36
- Slice steps 17-36 (20 items)
- TodoWrite creates 20-item checklist
- Execute from "ENRICH T1: Run subagent"

### Checklist Rules

1. **Mark `in_progress` BEFORE starting** each step
2. **Mark `completed` IMMEDIATELY after** success
3. **On validation FAIL:** Stop pipeline, do NOT mark completed, report failure
4. **After context compaction:** Read todo list to find current position
5. **Only ONE step** should be `in_progress` at any time
6. **Never skip validators** - they are explicit checklist items

---

## Stage Execution Order

```
SOURCE → BASE → RQ → ENRICH → SCENARIO → SC → INTEGRATION → IRR → FINAL_CVR
```

When running `RUN {START}->{END}`:
1. Find START in the sequence above
2. Execute all stages from START through END (inclusive)
3. Skip stages before START (assume artifacts exist)

---

HEADER

# Append timestamp
echo "> **Generated:** $(date -Iseconds)" >> "$OUT"
echo "" >> "$OUT"

# Define stage order
STAGES=(SOURCE BASE RQ ENRICH SCENARIO SC INTEGRATION IRR FINAL_CVR)

# Append each orchestration file
for stage in "${STAGES[@]}"; do
    file="${ORCH_DIR}/${stage}_STAGE.md"
    if [ -f "$file" ]; then
        echo "" >> "$OUT"
        echo "---" >> "$OUT"
        echo "" >> "$OUT"
        echo "# Stage: ${stage}" >> "$OUT"
        echo "" >> "$OUT"
        cat "$file" >> "$OUT"
        echo "" >> "$OUT"
        echo "Appended: $file"
    else
        echo "Warning: $file not found, skipping"
    fi
done

# Write footer
echo "" >> "$OUT"
echo "---" >> "$OUT"
echo "" >> "$OUT"
echo "*End of auto-generated orchestration. Total stages: ${#STAGES[@]}*" >> "$OUT"

# Report stats
LINE_COUNT=$(wc -l < "$OUT" | tr -d ' ')
WORD_COUNT=$(wc -w < "$OUT" | tr -d ' ')

echo ""
echo "=========================================="
echo "Generated: $OUT"
echo "Lines: $LINE_COUNT"
echo "Words: $WORD_COUNT"
echo "=========================================="
echo ""
echo "To use: cd workshop/smoke_tests && claude"
echo "Then run: RUN SOURCE->ENRICH {TICKER}"
