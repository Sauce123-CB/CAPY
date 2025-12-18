# CAPY - Mono-Repo Root

> **Version:** 1.1.0
> **Last reviewed:** 2024-12-18

This repository contains the complete CAPY (Company Analysis PYthon) system for fundamental equity research.

---

## MANDATORY AUTO-ROUTING (FIRST TURN)

**ON THE VERY FIRST USER MESSAGE, YOU MUST:**

1. **Classify** the user's intent into one of three workspaces
2. **Read** that workspace's CLAUDE.md file immediately
3. **Execute** the user's request using the workspace context

**DO NOT** ask the user which workspace they want. **DO NOT** describe the routing system. Just route silently and execute.

---

## Routing Classification

Classify the user's first message and route accordingly:

### → Route to `workshop/` when the user mentions:
- "DEV:" commands (DEV: STATUS, DEV: APPLY PATCH, etc.)
- Prompt development, editing, iteration, or fixing
- Smoke tests or testing prompts
- Patch application or patch development
- Keywords: "develop", "patch", "iterate", "fix prompt", "edit prompt", "prompt", "kernel", "process", "workflow design"

**Action:** Read `workshop/CLAUDE.md`, then execute the request.

### → Route to `production/` when the user mentions:
- "CAPY:" commands (CAPY: RUN, CAPY: T1, etc.)
- "SOURCE:" commands (SOURCE: UPLOAD, SOURCE: LIST)
- Running analysis on a specific company or ticker
- Keywords: "analyze", "run analysis", "run on", ticker symbols (AAPL, MSFT, etc.), company names

**Action:** Read `production/CLAUDE.md`, then execute the request.

### → Route to `archive/` when the user mentions:
- "ARCHIVE:" commands (ARCHIVE: LIST, ARCHIVE: RETRIEVE)
- Retrieving old versions or historical data
- Keywords: "old version", "historical", "archive", "retrieve", "find old"

**Action:** Read `archive/CLAUDE.md`, then execute the request.

### → Stay at root if:
- The request is about the mono-repo structure itself
- The request is about this CLAUDE.md file
- The request explicitly asks about routing
- The intent is genuinely ambiguous (ask for clarification only then)

---

## Workspaces Overview

| Workspace | Purpose | CLAUDE.md |
|-----------|---------|-----------|
| `workshop/` | Prompt development, patches, smoke tests | `workshop/CLAUDE.md` |
| `production/` | Live analysis runs on companies | `production/CLAUDE.md` |
| `archive/` | Historical versions, old analyses | `archive/CLAUDE.md` |

---

## Quick Reference Commands

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
| 1.1.0 | 2024-12-18 | Made auto-routing mandatory and explicit on first turn |
| 1.0.0 | 2024-12-17 | Initial mono-repo migration from 3 separate repos |
