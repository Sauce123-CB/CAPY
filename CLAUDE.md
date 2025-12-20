# CAPY - Mono-Repo Root

> **Version:** 1.3.0
> **Last reviewed:** 2024-12-20

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
| workshop | shared | `../shared/` |
| production | workshop | `../workshop/` |
| production | archive | `../archive/` |
| production | shared | `../shared/` |

### Shared Layer

The `shared/` directory contains resources visible to ALL contexts:

| File | Purpose |
|------|---------|
| `shared/PATTERNS.md` | Quick-reference for 10 orchestration patterns |
| `shared/BRIDGE.md` | How workshop ↔ production connect |

**Always read `shared/PATTERNS.md` when executing pipeline stages.**

### Cross-Context Peek

Both workshop and production have a `/peek` command to look into sibling contexts without switching:
- From workshop: `/peek production`, `/peek production sources DAVE`
- From production: `/peek workshop`, `/peek workshop patches`

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

## Pipeline Development Protocols

### Forward Compatibility Protocol

**Before promoting any stage prompt to CANONICAL or moving to the next pipeline stage:**

1. **Audit downstream stages:** Identify all pipeline stages that consume output from the changed stage
2. **Check compatibility:** Verify downstream prompts are compatible with:
   - New artifact schemas
   - New slot architectures (e.g., 6-slot → 7-slot)
   - New file delivery patterns (e.g., atomized prompts)
   - New tool calls (e.g., WebSearch for market prices)
3. **Update downstream prompts:** Propagate changes before running the next stage
4. **Document in commit message:** Note which downstream stages were updated for compatibility

**Pipeline dependency chain:**
```
BASE → RQ_GEN → ENRICH → SCENARIO → INTEGRATION → IRR
              ↘ SC/HITL ↗
```

**Common forward compatibility issues:**
- Slot architecture changes (M-1/M-2/M-3 vs M-1/M-2/M-3a/M-3b)
- Artifact schema changes (new fields, renamed keys)
- File delivery pattern changes (single file vs atomized files)
- Tool dependency changes (WebSearch availability)

### Checkpoint Protocol (MANDATORY)

**ALWAYS checkpoint before modifying ANY file.**

This is non-negotiable. Do NOT edit, write, or modify files without explicit user approval.

**Before ANY file modification:**
1. **State** exactly which file(s) you intend to modify
2. **Show** the specific changes you plan to make (old → new)
3. **Wait** for explicit user approval ("yes", "proceed", "do it", etc.)
4. **Only then** execute the edit

**Rationale:** Unchecked edits cause catastrophic errors. Reading files is fine. Modifying files requires approval.

**No exceptions.** Even "trivial" changes require checkpoint. If you're uncertain whether something counts as a modification, checkpoint anyway.

**Violations:** If you modify a file without checkpointing, immediately revert the change and apologize.

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
| 1.2.0 | 2024-12-19 | Added Pipeline Development Protocols (Forward Compatibility, Checkpoint) |
| 1.1.0 | 2024-12-18 | Made auto-routing mandatory and explicit on first turn |
| 1.0.0 | 2024-12-17 | Initial mono-repo migration from 3 separate repos |
