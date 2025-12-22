# CAPY Shared Patterns

> **Version:** 1.1.0
> **Scope:** Patterns visible to BOTH workshop/ and production/
> **Authority:** This file is the canonical source for orchestration patterns

---

## Quick Reference

| Pattern | One-liner |
|---------|-----------|
| 1. Direct-Write | Subagent writes to disk, returns path only |
| 2. Source Chain | REFINE is source of truth for A.1-A.6, not T1 |
| 3. Two-Shot | T1 = synthesis, T2 = validation + execution |
| 4. Embed vs Read | Small files embed, large files subagent reads |
| 5. JSON Repair | T2 can fix malformed JSON before kernel |
| 6. Bash Kernel | Execute Python via Bash, never fabricate |
| 7. Validators | Opus validator after each turn |
| 8. Atomized Prompts | Split into PROMPT/SCHEMAS/NORMDEFS |
| 9. Pipeline State | `pipeline_state.json` tracks progress |
| 10. Input Validation | READ files, don't assume from filenames |
| 11. Surgical Stitching | T3 concatenates from T1/T2, no regeneration |
| 12. Canonical Snapshot | Each stage folder = complete artifact set; orchestrator cp (not Claude) |
| 13. Kernel Receipts | JSON proof of real kernel execution (sha256, exit_code, timing) |

---

## Full Pattern Definitions

See `workshop/orchestration/ORCHESTRATION_KEY_PATTERNS.md` for complete documentation.

This file exists so both workshop/ and production/ can reference the same pattern numbering without loading the full doc.

### Pattern 12: Canonical Snapshot with Orchestrator Copy-Forward

**Problem:** Tracking artifact provenance across stages is error-prone.

**Solution:** Each stage folder contains a COMPLETE snapshot of all artifacts with that stage's suffix. Orchestrator copies forward unchanged files via `cp` (NOT Claude read/write) before each stage.

**Naming Convention:**
```
{TICKER}_{ARTIFACT}_{STAGE}.{ext}

Examples:
- DAVE_A5_GIM_BASE.json       # A5 after BASE stage
- DAVE_A5_GIM_ENRICH.json     # A5 after ENRICH (if modified)
- DAVE_N1_THESIS_BASE.md      # N1 narrative after BASE
```

**Stage Suffixes:**
| Stage | Suffix |
|-------|--------|
| BASE | `_BASE` |
| RQ | `_RQ` |
| ENRICH | `_ENRICH` |
| SCENARIO | `_SCEN` |
| SILICON COUNCIL | `_SC` |
| INTEGRATION | `_INT` |
| IRR | `_IRR` |

**Orchestrator Protocol (between stages):**
```bash
# After ENRICH completes, before SCENARIO starts
mkdir -p {analysis_dir}/06_SCENARIO

# Copy ALL artifacts with suffix rename (Bash, not Claude)
for f in {analysis_dir}/05_ENRICH/{TICKER}_*_ENRICH.json; do
  base=$(basename "$f" | sed 's/_ENRICH\.json$//')
  cp "$f" "{analysis_dir}/06_SCENARIO/${base}_SCEN.json"
done
```

**Critical:** Copy uses `cp` command, NOT Claude read/write. If Claude reads to "copy," truncation can occur.

### Pattern 13: Kernel Execution Receipts

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
  "command": "python3 BASE_CVR_KERNEL_2.2.3e.py --a5 ... --output ...",
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

## Pipeline Dependency Chain

```
BASE_T1 → BASE_REFINE → BASE_T2 → RQ_GEN → RQ_ASK → ENRICH_T1 → ENRICH_T2 → SCENARIO → INTEGRATION → IRR
                ↑                                        ↑
         (Source of Truth                    (Source of Truth
          for A.1-A.6)                        for State 2)
```

---

## Folder Conventions

| Stage | Output Folder | Key Files |
|-------|---------------|-----------|
| SOURCE | `00_source/` | `*.extracted.md` (preprocessed PDFs) |
| BASE T1 | `01_T1/` | `{TICKER}_BASE_T1.md` |
| BASE REFINE | `02_REFINE/` | `{TICKER}_BASE_REFINE.md` |
| BASE T2 | `03_T2/` | `{TICKER}_BASE_T2.md`, `{TICKER}_A*_BASE.json` |
| RQ | `04_RQ/` | `{TICKER}_A8_*.json`, `{TICKER}_RQ*.md` |
| ENRICH | `05_ENRICH/` | `{TICKER}_*_ENRICH.{md,json}` |
| SCENARIO | `06_SCENARIO/` | `{TICKER}_*_SCEN.{md,json}` |
| SILICON COUNCIL | `07_SILICON_COUNCIL/` | `{TICKER}_SC_*_SC.json`, `{TICKER}_A11_*.json` |
| INTEGRATION | `08_INTEGRATION/` | `{TICKER}_*_INT.{md,json}` |
| IRR | `09_IRR/` | `{TICKER}_*_IRR.{md,json}`, `{TICKER}_FINAL_CVR.md` |

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.1.0 | 2024-12-22 | Added Patterns 11-13, updated folder conventions for atomic naming |
| 1.0.0 | 2024-12-20 | Initial creation from workshop patterns |
