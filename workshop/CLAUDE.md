# CAPY Workshop - Prompt Development Environment

> **Version:** 0.8.0
> **Last reviewed:** 2024-12-19
> **Review cadence:** Weekly during active development, monthly otherwise

This workspace is for **developing, testing, and iterating** on CAPY prompts and kernels.

For **production analysis runs**, use `../production/` instead.

---

## CLAUDE.md Versioning

This instruction file is itself experimental and will evolve.

When updating this file:
1. Increment version number above
2. Note change in git commit message
3. If significant change, add entry to `patches/PATCH_TRACKER.md`

---

## Folder Structure

```
workshop/
├── prompts/           # All prompt files
│   ├── base/          # G3BASE (Turn 1)
│   ├── refine/        # REFINE prompts
│   ├── enrich/        # ENRICH stage
│   ├── scenario/      # SCENARIO stage
│   ├── integration/   # INTEGRATION stage
│   ├── irr/           # IRR stage
│   ├── rq_gen/        # Research Question generation
│   ├── silicon_council/  # Silicon Council deliberation
│   └── hitl_audit/    # Human-in-the-loop audit protocols
├── kernels/           # Python kernel files
├── meta/              # Philosophy docs, READMEs
├── validators/        # Validation prompts
├── orchestration/     # CC orchestrator helpers (CLAUDE.md stubs, etc.)
├── patches/           # Patch specs and tracker
└── smoke_tests/       # Test outputs (pruned monthly)
```

---

## Version Labeling System

### Source of Truth

The **"Current Versions" table** (below) is the authoritative registry for prompt status.

### Status Definitions

| Status | Definition | Evidence Required |
|--------|------------|-------------------|
| **CANONICAL** | Passed smoke test in Production | Smoke test folder in table |
| **EXPERIMENTAL** | Created/modified, awaiting smoke test | None (default for new files) |
| **HISTORICAL** | Previous canonical, superseded | Archived after new version becomes CANONICAL |

### Lifecycle

```
NEW FILE CREATED
      │
      ▼
 EXPERIMENTAL ──────smoke test────────► PASS ──────► CANONICAL
      │                                    │              │
      │                                    │              ▼
      │                                FAIL          (old CANONICAL
      │                                    │          becomes HISTORICAL,
      │                                    ▼          moved to Archive)
      └──────────────────────────► /iterate
                                  (stays EXPERIMENTAL,
                                   update patches)
```

### Critical Rules

1. **CANONICAL requires proof:** A prompt can only be CANONICAL if a passing smoke test folder exists
2. **Never archive CANONICAL early:** Do NOT move CANONICAL to Archive until EXPERIMENTAL passes smoke test
3. **Workshop + Production parity:** Both must always have a CANONICAL version available as fallback

**Rule:** Keep max 3 versions per prompt. HISTORICAL versions go to `../archive/`.

---

## Development Commands

### DEV: STATUS

Report current state:
- List all prompts with version labels (CANONICAL/EXPERIMENTAL/HISTORICAL)
- Show pending patches from `patches/PATCH_TRACKER.md`
- List recent smoke tests

### DEV: APPLY PATCH {N}

Apply a specific patch from `patches/CAPY_2.2.2e_Patch_Details.md`:

**Step 0: Confirm user preferences**
Before proceeding, ask user:
- **Autonomous mode:** Apply patch, version, test, and report back?
- **Checkpoint mode:** Pause for approval between each step?

Then proceed based on preference:

1. Read the patch details for item #{N}
2. Identify target files from "Files to Touch" section
3. Make the specified changes
4. Update version number (e.g., 2.2.1e → 2.2.2e)
5. **Version Labeling (CRITICAL):**
   - Add new file row to "Current Versions" table with Status = EXPERIMENTAL
   - Keep existing CANONICAL row unchanged (do NOT archive yet)
   - Smoke Test column = "-" for new EXPERIMENTAL file
6. Update `patches/PATCH_TRACKER.md`

### DEV: SMOKE TEST {TICKER}

Run a quick validation of the current CANONICAL prompts:

1. Create folder: `smoke_tests/{TICKER}_{YYYYMMDD}_{HHMMSS}/`
   - Example: `smoke_tests/DAVE_20241215_143022/`
2. Create `run_metadata.json` in that folder:
   ```json
   {
     "ticker": "DAVE",
     "run_id": "DAVE_20241215_143022",
     "run_timestamp": "2024-12-15T14:30:22Z",
     "prompt_versions": {
       "base": "G3BASE_2.2.1e.md",
       "refine": "BASE_T1_REFINE_v1_1.md",
       "kernel": "BASE_CVR_KERNEL_2.2.1e.py"
     },
     "source_docs": ["list of input files"],
     "validation_result": null
   }
   ```
3. **Source documents** - obtain from one of:
   - `../../production/analyses/{TICKER}_*/00_source/` (preferred - reuse existing)
   - User-provided path
   - WebSearch for recent filings (if user approves, saves time)

**Input Source Validation (Pattern 10 - MANDATORY):**
When smoke test requires prior-stage artifacts (e.g., ENRICH needs BASE outputs):
- READ files in specified folder to verify contents (not just `ls`)
- Extract and log State N IVPS before proceeding
- Never assume file contents from filenames
- If folder incomplete, search for most recent complete run
- Verify IVPS consistency: markdown must match kernel output JSON

4. Use Task subagent to run BASE T1 with:
   - Current canonical `prompts/base/G3BASE_*.md`
   - Current canonical `kernels/BASE_CVR_KERNEL_*.py`
   - Source documents from step 3
5. Run validator on output
6. Update `run_metadata.json` with validation result
7. Report PASS/WARN/FAIL

### DEV: COMPARE {VERSION1} {VERSION2}

Compare two versions of a prompt or kernel:
- Show structural differences
- Highlight added/removed sections
- Summarize semantic changes

### DEV: COMPARE RUNS {TICKER} [N]

Compare the N most recent runs for a ticker (default N=2):

1. List all folders in `smoke_tests/` matching `{TICKER}_*`
2. Sort by timestamp (extracted from folder name)
3. Load `run_metadata.json` from each of the N most recent
4. Report:
   - Run timestamps
   - Prompt versions used in each
   - Validation results (PASS/WARN/FAIL)
   - If prompt versions differ, highlight which changed
5. Optionally diff key outputs (IVPS, major metrics) if T2 completed

### DEV: MARK CANONICAL {FILE} {SMOKE_TEST_FOLDER}

Promote an EXPERIMENTAL file to CANONICAL:

**Requires:** Smoke test folder path (e.g., `smoke_tests/DAVE_20241217_143022`)

**Always checkpoint with user before each step.**

1. **Verify smoke test (REQUIRED):**
   - Check `{SMOKE_TEST_FOLDER}/run_metadata.json` exists
   - Confirm `validation_result` = PASS
   - If not PASS, abort and suggest `/iterate` instead
   → **confirm with user**
2. Demote current CANONICAL to HISTORICAL:
   - Move old file to `../archive/prompts/{stage}/`
   - Remove CANONICAL row from "Current Versions" table
   → **confirm with user**
3. Mark specified file as new CANONICAL:
   - Update "Current Versions" table: Status = CANONICAL, Smoke Test = {folder_id}
   → **confirm with user**
4. Copy to `../production/` (deployment step) → **confirm with user**

### DEV: DEPLOY TO PROD

Copy all CANONICAL files to `../../production/`:

1. Identify all CANONICAL prompts and kernels
2. Copy to Production folder (overwrite existing)
3. Update Production's VERSION.md with deployment timestamp

---

## Git Workflow

### Repository Structure

| Repo | Purpose | GitHub |
|------|---------|--------|
| `CAPY` | Complete CAPY system (mono-repo) | `Sauce123-CB/CAPY` |



### What Gets Committed

| Include | Exclude (via .gitignore) |
|---------|--------------------------|
| `.md` prompts, docs | `*.pdf`, `*.PDF` |
| `.py` kernels | `*.png`, `*.jpg` |
| `.json` configs, outputs | `*.zip` |
| `extracted.md` source text | `*.pyc`, `__pycache__/` |
| Validation results | `.claude/settings.local.json` |

**PDFs and images live in Dropbox only** - collaborators access via shared Dropbox folder.

### Sync Protocol

Before starting a session:
```
git fetch origin  # Check for remote changes
git status        # Verify clean working tree
```

After making changes:
```
git add <files>
git commit -m "Descriptive message"
git push origin master
```

### Cross-Repo Workflow

The Workshop ↔ Production cycle:

```
┌─────────────────────────────────────────────────────────┐
│                      WORKSHOP                           │
│  1. Develop patch → EXPERIMENTAL prompt                 │
│  2. Deploy to Production for smoke test                 │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                     PRODUCTION                          │
│  3. Run smoke test with EXPERIMENTAL prompt             │
│  4. Document results                                    │
└──────────────────────┬──────────────────────────────────┘
                       │
           ┌───────────┴───────────┐
           ▼                       ▼
    ┌─────────────┐         ┌─────────────┐
    │   SUCCESS   │         │   FAILURE   │
    │             │         │             │
    │ /promote    │         │ /iterate    │
    │ - Mark      │         │ - Document  │
    │   canonical │         │   findings  │
    │ - Sync both │         │ - Update    │
    │   repos     │         │   patches   │
    │ - Update    │         │ - Sync both │
    │   CLAUDE.md │         │   repos     │
    └─────────────┘         └─────────────┘
```

### Slash Commands

Custom commands for common git operations (in `.claude/commands/`):

| Command | Purpose |
|---------|---------|
| `/sync` | Sync repo to GitHub |
| `/promote {FILE}` | Promote EXPERIMENTAL → CANONICAL after successful smoke test |
| `/iterate {TICKER}` | Document failed smoke test, update patch backlog |

---

## Subagent Protocol

To manage context effectively:

1. **Read only necessary and sufficient prompt files** - avoid loading files that aren't needed for the current task, but do load what's required (sometimes that's multiple patches together)
2. **For patch work:** Spawn Task subagent with only the patch spec + target file(s)
3. **For smoke tests:** Spawn Task subagent with prompt + kernel + source docs
4. **Orchestrator only reads summaries**, not full analytical outputs (unless user requests otherwise)

---

## Development Protocols

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

### Forward Compatibility Protocol

**Before modifying any stage prompt:**

1. **Identify consumers:** Which downstream stages use this stage's output?
2. **Check compatibility:** Review downstream prompts for:
   - Artifact references (e.g., "RQ Outputs (1-6)" → "(1-7)")
   - Slot architecture assumptions
   - File delivery expectations
3. **Update downstream:** Propagate changes before smoke testing
4. **Document:** Note compatibility updates in commit message

**Pipeline dependencies:**
| If you change... | Check these downstream stages... |
|------------------|----------------------------------|
| BASE | RQ_GEN, ENRICH, SCENARIO, all |
| RQ_GEN | ENRICH (RQ slot references) |
| ENRICH | SCENARIO, INTEGRATION |
| SCENARIO | INTEGRATION, IRR |

---

## RQ Stage Orchestration (RQ_GEN → RQ_ASK)

The RQ (Research Question) stage bridges BASE analysis and ENRICH/SCENARIO stages by executing external research queries via parallel subagents.

### Architecture (v2.2.3)

**7-Slot Framework:**
- 4 Mandatory slots (M-1, M-2, M-3a, M-3b)
- 3 Dynamic slots (D-1, D-2, D-3 for Lynchpin coverage)

**Mandatory Coverage:**
| Slot | Coverage | Purpose |
|------|----------|---------|
| M-1 | Integrity Check | Forensic accounting, governance flags |
| M-2 | Adversarial Synthesis | Bull/bear arguments, litigation |
| M-3a | Mainline Scenario H.A.D. | 4 mainline scenarios (products, M&A, regulatory, strategy) |
| M-3b | Tail Scenario H.A.D. | 4 tail scenarios (2 Blue Sky + 2 Black Swan) |

**Scenario Coverage:** 8 total scenarios researched (4 mainline + 4 tail) to ensure SCENARIO stage has sufficient candidates.

### Stage Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. RQ_GEN (Opus Subagent)                                   │
│    Input:  {TICKER}_BASE_T1.md + {TICKER}_BASE_REFINE.md +  │
│            {TICKER}_BASE_T2.md + RQ_Gen_2_2_3e.md           │
│    Output: A.8_RESEARCH_STRATEGY_MAP (JSON)                 │
│    Save:   04_RQ/{TICKER}_A8_RESEARCH_PLAN.json             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. A.8 VALIDATOR (Opus Subagent)                            │
│    Prompt: validators/A8_VALIDATOR.md                       │
│    Check:  Schema, 7 RQs, M-1/M-2/M-3a/M-3b coverage,       │
│            8 scenario candidates, retrieval-only verbs      │
│    Output: PASS/FAIL + issues                               │
└──────────────────────┬──────────────────────────────────────┘
                       │ (proceed only if PASS)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. RQ_ASK (7 Parallel Subagents)                            │
│    Kernel: kernels/RQ_ASK_KERNEL_2_2_3e.py                  │
│    Execute: 7 parallel Claude/Gemini research subagents     │
│    Each subagent writes output directly to disk             │
│    Output: A.9_RESEARCH_RESULTS (JSON) + 7 markdown files   │
│    Save:   04_RQ/{TICKER}_A9_*.json + RQ1-RQ7_*.md          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. A.9 VALIDATOR (Opus Subagent)                            │
│    Prompt: validators/A9_VALIDATOR.md                       │
│    Check:  Success rate, response length, content quality   │
│    Output: PASS/WARN/FAIL + recommendation                  │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

RQ outputs go in the analysis folder's `04_RQ/` subdirectory:
```
production/analyses/{TICKER}_CAPY_{TIMESTAMP}/
├── 01_T1/
├── 02_REFINE/
├── 03_T2/
├── 04_RQ/                           ← RQ stage outputs
│   ├── {TICKER}_A8_RESEARCH_PLAN.json
│   ├── {TICKER}_A8_validation.json
│   ├── {TICKER}_A9_RESEARCH_RESULTS_{TS}.json
│   └── {TICKER}_A9_validation.json
├── 05_ENRICH/                       ← Next stage
└── pipeline_state.json
```

### Execution Commands

**Step 1: Generate A.8 (RQ_GEN)**
```
Spawn Opus subagent with:
- orchestration/RQ_Gen_2_2_2e.md (prompt)
- {analysis_dir}/01_T1/{TICKER}_BASE_T1.md
- {analysis_dir}/02_REFINE/{TICKER}_BASE_REFINE.md
- {analysis_dir}/03_T2/{TICKER}_BASE_T2.md

Instruct: "Generate A.8_RESEARCH_STRATEGY_MAP for {TICKER}. Output pure JSON."
```

**Step 2: Validate A.8**
```
Spawn Opus subagent with:
- validators/A8_VALIDATOR.md
- The A.8 JSON from step 1

Instruct: "Validate this A.8 artifact."
```

**Step 3: Execute RQ_ASK**
```bash
python workshop/kernels/run_rq_ask.py \
    {analysis_dir}/04_RQ/{TICKER}_A8_RESEARCH_PLAN.json \
    {analysis_dir}/04_RQ \
    {TICKER}
```

**Step 4: Validate A.9**
```
Spawn Opus subagent with:
- validators/A9_VALIDATOR.md
- The A.9 JSON from step 3

Instruct: "Validate this A.9 artifact."
```

### RQ Stage Files

| File | Location | Purpose |
|------|----------|---------|
| RQ_Gen_2_2_3e.md | orchestration/ | RQ generation prompt (7-slot, 8 scenarios) |
| RQ_ASK_KERNEL_2_2_3e.py | kernels/ | Async parallel subagent executor |
| run_rq_ask.py | kernels/ | CLI wrapper for RQ_ASK |
| A8_VALIDATOR.md | validators/ | A.8 schema/semantic validator (7-slot) |
| A9_VALIDATOR.md | validators/ | A.9 completeness validator |

### Execution Configuration

**Subagent Options:**
- **Claude Opus:** Via Task tool with WebSearch/WebFetch permissions (recommended)
- **Gemini Deep Research:** Via CLI with OAuth authentication

**Execution Parameters:**
- **Concurrency:** 7 parallel subagents
- **Timeout:** 10 minutes per query
- **Output:** Each subagent writes directly to disk (no orchestrator transcription)

### Critical: Subagent Direct-Write Protocol

To avoid orchestrator bottleneck, subagents MUST write their output directly to disk:

1. Subagent prompt includes output path: `{output_dir}/RQ{N}_{topic}.md`
2. Subagent uses Write tool to save research report before returning
3. Subagent returns only confirmation + filepath
4. Orchestrator verifies files exist, reports to user

**This eliminates the 3-6x time overhead from orchestrator transcription.**

---

## Monthly Cleanup Protocol

Run on the 1st of each month:

1. For each prompt folder:
   - Keep: CANONICAL, EXPERIMENTAL (if exists), HISTORICAL
   - Move anything older to `../archive/prompts/`

2. For smoke_tests/:
   - Keep runs from last 30 days
   - Move older runs to `../archive/smoke_tests/`

3. Commit archive changes to `CAPY_Archive` repo

---

## File Naming Conventions

**Prompts:** `{STAGE}_{VERSION}.md`
- Example: `G3BASE_2.2.1e.md`, `G3BASE_2.2.2e.md`

**Kernels:** `{STAGE}_CVR_KERNEL_{VERSION}.py`
- Example: `BASE_CVR_KERNEL_2.2.1e.py`

**No spaces in filenames.** Use underscores.

**Version format:** `{MAJOR}.{MINOR}.{PATCH}{VARIANT}`
- Example: `2.2.1e` where `e` = experimental branch

---

## Current Versions

### Analysis Pipeline (Prompts + Kernels)

| Stage | Prompt | Status | Smoke Test | Kernel |
|-------|--------|--------|------------|--------|
| BASE | G3BASE_2.2.1e.md | CANONICAL | DAVE_20241210 | BASE_CVR_KERNEL_2.2.1e.py |
| BASE | G3BASE_2.2.2e_*.md (atomized) | EXPERIMENTAL | - | BASE_CVR_KERNEL_2.2.2e.py |
| REFINE | BASE_T1_REFINE_v1_1.md | CANONICAL | DAVE_20241210 | - |
| REFINE | BASE_T1_REFINE_v1_2.md | EXPERIMENTAL | - | - |
| ENRICH | G3ENRICH_2.2.1e.md | CANONICAL | DAVE_20241210 | CVR_KERNEL_ENRICH_2.2.1e.py |
| ENRICH | G3ENRICH_2.2.2e_*.md (atomized) | EXPERIMENTAL | - | CVR_KERNEL_ENRICH_2.2.2e.py |
| SCENARIO | G3_SCENARIO_2_2_1e.md | CANONICAL | DAVE_20241210 | CVR_KERNEL_SCEN_2_2_1e.py |
| INTEGRATION | G3_INTEGRATION_2_2_2e.md | CANONICAL | DAVE_20241210 | CVR_KERNEL_INT_2_2_2e.py |
| IRR | G3_IRR_2_2_4e.md | CANONICAL | DAVE_20241210 | CVR_KERNEL_IRR_2_2_4e.py |

### Orchestration & Workflow

| Component | File | Status | Smoke Test |
|-----------|------|--------|------------|
| Research Question Gen | RQ_Gen_2_2_3e.md | EXPERIMENTAL | DAVE_RQ_CLAUDE_TEST |
| Research Question Gen (legacy) | RQ_Gen_2_2_2e.md | HISTORICAL | - |
| RQ Executor | RQ_ASK_KERNEL_2_2_3e.py | EXPERIMENTAL | DAVE_RQ_CLAUDE_TEST |
| RQ Executor CLI | run_rq_ask.py | EXPERIMENTAL | - |
| Silicon Council | G3_SILICON_COUNCIL_2.2.1e.md | CANONICAL | DAVE_20241210 |
| HITL Audit | HITL_DIALECTIC_AUDIT_1_0_Goldilocks.md | CANONICAL | DAVE_20241210 |

### Validators

| Component | File | Status | Smoke Test |
|-----------|------|--------|------------|
| Pipeline Validator | CAPY_PIPELINE_VALIDATOR_2_2e.md | CANONICAL | DAVE_20241210 |
| Inter-turn Validator | CAPY_VALIDATOR_2_2e.md | CANONICAL | DAVE_20241210 |
| A.8 Validator | A8_VALIDATOR.md | EXPERIMENTAL | - |
| A.9 Validator | A9_VALIDATOR.md | EXPERIMENTAL | - |

### BASE Stage Atomized Files (EXPERIMENTAL)

The BASE prompt v2.2.2e is split into 3 atomic files for improved context management:

| File | Purpose | Est. Lines |
|------|---------|------------|
| `G3BASE_2.2.2e_PROMPT.md` | Core instructions (Sections I-V) | ~500 |
| `G3BASE_2.2.2e_SCHEMAS.md` | JSON schemas (Appendix A) | ~200 |
| `G3BASE_2.2.2e_NORMDEFS.md` | DSL definitions (Appendix B) | ~150 |

**Status:** EXPERIMENTAL - awaiting smoke test. Once promoted to CANONICAL, G3BASE_2.2.1e.md moves to Archive.

**Subagent loading:** Load all 3 files + kernel. The embedded kernel (old Appendix C) has been removed.

### ENRICH Stage Atomized Files (EXPERIMENTAL)

The ENRICH prompt v2.2.2e is split into 3 atomic files plus kernel, mirroring the BASE pattern:

| File | Purpose | Est. Lines |
|------|---------|------------|
| `G3ENRICH_2.2.2e_PROMPT.md` | Core instructions (Sections I-V) | ~450 |
| `G3ENRICH_2.2.2e_SCHEMAS.md` | JSON schemas (Appendix A) | ~350 |
| `G3ENRICH_2.2.2e_NORMDEFS.md` | DSL & financial definitions (Appendix B) | ~300 |
| `CVR_KERNEL_ENRICH_2.2.2e.py` | Valuation kernel | ~900 |

**Key updates from 2.2.1e:**
- 7-slot RQ architecture references (M-1, M-2, M-3a, M-3b, D-1, D-2, D-3)
- 4-file atomization for context management
- Version refs updated to G3_2.2.2e

**Status:** EXPERIMENTAL - awaiting smoke test.

**Subagent loading:** Load all 3 prompt files. Kernel executed via Bash in T2 (not embedded in subagent context).
