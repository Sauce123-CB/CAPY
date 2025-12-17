# CAPY - Mono-Repo Root

> **Version:** 1.0.0
> **Last reviewed:** 2024-12-17

This repository contains the complete CAPY (Company Analysis PYthon) system for fundamental equity research.

---

## Workspace Routing

This mono-repo has three workspaces, each with its own CLAUDE.md:

| Workspace | Purpose | CLAUDE.md |
|-----------|---------|-----------|
| `workshop/` | Prompt development, patches, smoke tests | `workshop/CLAUDE.md` |
| `production/` | Live analysis runs on companies | `production/CLAUDE.md` |
| `archive/` | Historical versions, old analyses | `archive/CLAUDE.md` |

---

## Auto-Routing Rules

When the user's request matches these patterns, navigate to the appropriate workspace:

### Use `workshop/` for:
- "DEV:" commands (DEV: STATUS, DEV: APPLY PATCH, etc.)
- Prompt development, editing, or iteration
- Smoke tests
- Patch application
- "develop", "patch", "iterate", "fix prompt"

### Use `production/` for:
- "CAPY:" commands (CAPY: RUN, CAPY: T1, etc.)
- "SOURCE:" commands (SOURCE: UPLOAD, SOURCE: LIST)
- Running analysis on a company/ticker
- "analyze {TICKER}", "run analysis"

### Use `archive/` for:
- "ARCHIVE:" commands (ARCHIVE: LIST, ARCHIVE: RETRIEVE)
- Retrieving old versions
- "find old version", "historical"

---

## Quick Start Commands

### Switch Workspace Context

```
/workshop    - Enter Workshop mode (prompt development)
/production  - Enter Production mode (analysis runs)
/archive     - Enter Archive mode (retrieval)
```

### Common Operations

| Task | Workspace | Command |
|------|-----------|---------|
| Check prompt status | workshop | `DEV: STATUS` |
| Apply a patch | workshop | `DEV: APPLY PATCH {N}` |
| Run smoke test | workshop | `DEV: SMOKE TEST {TICKER}` |
| Analyze a company | production | `CAPY: RUN {TICKER}` |
| Upload source docs | production | `SOURCE: UPLOAD {TICKER}` |
| Find old prompt | archive | `ARCHIVE: SEARCH {query}` |

---

## Repository Structure

```
CAPY/
├── CLAUDE.md              # This file (router)
├── .gitignore             # Unified ignore rules
│
├── workshop/              # Development environment
│   ├── CLAUDE.md          # Workshop instructions
│   ├── prompts/           # All prompt files (by stage)
│   ├── kernels/           # Python kernel files
│   ├── patches/           # Patch specs and tracker
│   ├── smoke_tests/       # Test outputs
│   ├── validators/        # Validation prompts
│   ├── meta/              # Philosophy docs
│   └── orchestration/     # CC orchestrator helpers
│
├── production/            # Execution environment
│   ├── CLAUDE.md          # Production instructions
│   ├── prompts/           # CANONICAL versions only
│   ├── kernels/           # CANONICAL versions only
│   ├── validators/        # Inter-turn validators
│   ├── source_library/    # Pre-staged company docs
│   └── analyses/          # Production outputs
│
└── archive/               # Cold storage
    ├── CLAUDE.md          # Archive instructions
    ├── prompts/           # Old prompt versions
    ├── kernels/           # Old kernel versions
    ├── smoke_tests/       # Old test runs
    └── analyses/          # Old production analyses
```

---

## Cross-Workspace References

Within the mono-repo, use relative paths:

| From | To | Path |
|------|----|------|
| workshop | production | `../production/` |
| workshop | archive | `../archive/` |
| production | workshop | `../workshop/` |
| production | archive | `../archive/` |

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────┐
│                      WORKSHOP                           │
│  1. Develop patch → EXPERIMENTAL prompt                 │
│  2. Run smoke test                                      │
└──────────────────────┬──────────────────────────────────┘
                       │
           ┌───────────┴───────────┐
           ▼                       ▼
    ┌─────────────┐         ┌─────────────┐
    │   SUCCESS   │         │   FAILURE   │
    │             │         │             │
    │ Promote to  │         │ Iterate in  │
    │ CANONICAL   │         │ workshop    │
    │      │      │         └─────────────┘
    │      ▼      │
    │ Deploy to   │
    │ production/ │
    └─────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────┐
│                     PRODUCTION                          │
│  Run live analyses with CANONICAL prompts               │
└─────────────────────────────────────────────────────────┘
           │
           ▼ (monthly cleanup)
┌─────────────────────────────────────────────────────────┐
│                      ARCHIVE                            │
│  Store old versions, old analyses                       │
└─────────────────────────────────────────────────────────┘
```

---

## For Collaborators

### Clone and Setup

```bash
git clone https://github.com/Sauce123-CB/CAPY.git
cd CAPY
```

### Using Claude Code

1. Open Claude Code in the `CAPY/` directory
2. State your intent (e.g., "I want to develop prompts" or "I want to analyze AAPL")
3. Claude will route to the appropriate workspace

### GitHub

- **Main repo:** `https://github.com/Sauce123-CB/CAPY`
- **Issues:** Use for bug reports, feature requests
- **PRs:** Use for prompt/kernel changes

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2024-12-17 | Initial mono-repo migration from 3 separate repos |
