# CAPY Shared Patterns

> **Version:** 1.0.0
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

---

## Full Pattern Definitions

See `workshop/orchestration/ORCHESTRATION_KEY_PATTERNS.md` for complete documentation.

This file exists so both workshop/ and production/ can reference the same pattern numbering without loading the full doc.

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
| BASE T1 | `01_T1/` | `{TICKER}_BASE_T1.md` |
| BASE REFINE | `02_REFINE/` | `{TICKER}_BASE_REFINE.md` |
| BASE T2 | `03_T2/` | `{TICKER}_BASE_T2.md`, `A*.json` |
| RQ | `04_RQ/` | `A8*.json`, `RQ*.md` |
| ENRICH | `05_ENRICH/` | `{TICKER}_ENRICH_T1.md`, `{TICKER}_ENRICH_T2.md` |
| SCENARIO | `06_SCENARIO/` | `{TICKER}_SCENARIO.md` |
| INTEGRATION | `07_INTEGRATION/` | `{TICKER}_INTEGRATION.md` |
| IRR | `08_IRR/` | `{TICKER}_IRR.md` |

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2024-12-20 | Initial creation from workshop patterns |
