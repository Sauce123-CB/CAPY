# Workshop ↔ Production Bridge

> **Version:** 1.0.0
> **Purpose:** Cross-context visibility between workshop/ and production/

---

## When You Need the Other Context

### From WORKSHOP, you need PRODUCTION when:
- Checking what prompts are currently deployed (`../production/prompts/`)
- Finding source documents for smoke tests (`../production/source_library/`)
- Seeing how a production run structured its outputs (`../production/analyses/`)
- Verifying CANONICAL version parity

### From PRODUCTION, you need WORKSHOP when:
- Finding EXPERIMENTAL prompts to test (`../workshop/prompts/`)
- Checking patch status (`../workshop/patches/`)
- Understanding why a prompt changed (`../workshop/patches/SESSION_LOG_*.md`)
- Getting the latest orchestration patterns (`../workshop/orchestration/`)

---

## Cross-Reference Paths

| From | To | Relative Path |
|------|----|---------------|
| workshop/ | production prompts | `../production/prompts/` |
| workshop/ | production analyses | `../production/analyses/` |
| workshop/ | source library | `../production/source_library/` |
| production/ | workshop prompts | `../workshop/prompts/` |
| production/ | patches | `../workshop/patches/` |
| production/ | orchestration | `../workshop/orchestration/` |
| either | shared patterns | `../shared/PATTERNS.md` |

---

## What Lives Where

| Content | Location | Why |
|---------|----------|-----|
| EXPERIMENTAL prompts | workshop/prompts/ | Development happens here |
| CANONICAL prompts | BOTH | workshop has source, production has deployed copy |
| Kernels (.py) | BOTH | Same pattern as prompts |
| Source documents | production/source_library/ | Heavy files, one location |
| Analysis outputs | production/analyses/ | Production runs only |
| Smoke test outputs | workshop/smoke_tests/ | Development testing |
| Orchestration patterns | workshop/orchestration/ | Developed in workshop, referenced by both |
| Shared interfaces | shared/ | Visible to both contexts |

---

## Promotion Flow

```
workshop/prompts/{stage}/          production/prompts/{stage}/
       │                                    ▲
       │ (1) Develop EXPERIMENTAL           │
       │                                    │
       ▼                                    │
workshop/smoke_tests/              (3) Copy CANONICAL
       │                                    │
       │ (2) Smoke test PASS                │
       │                                    │
       └────────────────────────────────────┘
```

---

## Common Cross-Context Operations

### "What's deployed in production?"
```
Read ../production/prompts/base/G3BASE_*.md
```

### "What source docs exist for TICKER?"
```
ls ../production/source_library/{TICKER}/
```

### "What patches are pending?"
```
Read ../workshop/patches/PATCH_TRACKER.md
```

### "What patterns should I follow?"
```
Read ../shared/PATTERNS.md
```

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2024-12-20 | Initial bridge document |
