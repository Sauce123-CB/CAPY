# CAPY Workshop - Prompt Development Environment

> **Version:** 0.10.0
> **Last reviewed:** 2024-12-20
> **Review cadence:** Weekly during active development, monthly otherwise

This workspace is for **developing, testing, and iterating** on CAPY prompts and kernels.

For **production analysis runs**, use `../production/` instead.

---

## Auto-Peek Protocol

**When to automatically look at production (without user asking):**

| Trigger | Auto-Action |
|---------|-------------|
| Need source docs for smoke test | `ls ../production/source_library/{TICKER}/` |
| Checking what's currently deployed | `ls ../production/prompts/{stage}/` |
| Need to verify CANONICAL parity | Read `../production/prompts/{stage}/{file}` and compare |
| Looking for prior analysis outputs | `find ../production/analyses/ -name "*{TICKER}*"` |
| Need orchestration patterns | Read `../shared/PATTERNS.md` |

**When to automatically look at shared:**

| Trigger | Auto-Action |
|---------|-------------|
| Executing any pipeline stage | Read `../shared/PATTERNS.md` (pattern quick-ref) |
| Unsure how contexts connect | Read `../shared/BRIDGE.md` |

**Implementation:** Just do it. Don't ask permission to read sibling directories. Report what you found.

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

### Validator Subagent Model: ALWAYS Opus

**Do NOT use haiku for validators.** Validators appear simple but require nuanced reasoning (e.g., detecting internal contradictions between prose and JSON, catching $0 impact for scenarios that claim +$50 magnitude). The cost savings from haiku are not worth the missed errors.

---

## Common Orchestration Mistakes

| Mistake | Why It Happens | Fix |
|---------|----------------|-----|
| Using haiku for validators | Task tool says "prefer haiku for quick tasks" | Validators are NOT quick tasks - always use Opus |
| Empty gim_overlay for acquisition scenarios | Treating acquisition as "structural" rather than lump sum | Acquisition premiums ARE lump sums - use EXPLICIT_SCHEDULE |
| Not re-reading CLAUDE.md mid-session | Context window pressure | Re-check before validator and T2 calls |

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
| BASE | G3BASE_2.2.2e_*.md (atomized) | CANONICAL | DAVE_20241220 | BASE_CVR_KERNEL_2.2.2e.py |
| BASE | G3BASE_2.2.1e.md | HISTORICAL | DAVE_20241210 | BASE_CVR_KERNEL_2.2.1e.py |
| REFINE | BASE_T1_REFINE_v1_2.md | CANONICAL | DAVE_20241220 | - |
| REFINE | BASE_T1_REFINE_v1_1.md | HISTORICAL | DAVE_20241210 | - |
| ENRICH | G3ENRICH_2.2.2e_*.md (atomized) | CANONICAL | DAVE_ENRICH_20241220 | CVR_KERNEL_ENRICH_2.2.2e.py |
| ENRICH | G3ENRICH_2.2.1e.md | HISTORICAL | DAVE_20241210 | CVR_KERNEL_ENRICH_2.2.1e.py |
| SCENARIO | G3_SCENARIO_2.2.2e_*.md (atomized) | CANONICAL | DAVE_ENRICH_SMOKE_20251220 | CVR_KERNEL_SCEN_2_2_2e.py |
| SCENARIO | G3_SCENARIO_2_2_1e.md | HISTORICAL | DAVE_20241210 | CVR_KERNEL_SCEN_2_2_1e.py |
| INTEGRATION | G3_INTEGRATION_2.2.2e_*.md (atomized) | EXPERIMENTAL | - | CVR_KERNEL_INT_2.2.2e.py |
| INTEGRATION | G3_INTEGRATION_2_2_2e.md | CANONICAL | DAVE_20241210 | CVR_KERNEL_INT_2_2_2e.py |
| IRR | G3_IRR_2_2_4e.md | CANONICAL | DAVE_20241210 | CVR_KERNEL_IRR_2_2_4e.py |

### Orchestration & Workflow

| Component | File | Status | Smoke Test |
|-----------|------|--------|------------|
| Research Question Gen | RQ_Gen_2_2_3e.md | CANONICAL | DAVE_RQ_CLAUDE_TEST |
| Research Question Gen (legacy) | RQ_Gen_2_2_2e.md | HISTORICAL | - |
| RQ Executor | RQ_ASK_KERNEL_2_2_3e.py | CANONICAL | DAVE_RQ_CLAUDE_TEST |
| RQ Executor CLI | run_rq_ask.py | CANONICAL | DAVE_RQ_CLAUDE_TEST |
| Silicon Council | G3_SC_2.2.2e_*.md (atomized) | CANONICAL | DAVE_ENRICH_SMOKE_20251220 |
| Silicon Council | G3_SILICON_COUNCIL_2.2.1e.md | HISTORICAL | DAVE_20241210 |
| HITL Audit | HITL_DIALECTIC_AUDIT_1_0_Goldilocks.md | CANONICAL | DAVE_20241210 |

### Validators

| Component | File | Status | Smoke Test |
|-----------|------|--------|------------|
| Pipeline Validator | CAPY_PIPELINE_VALIDATOR_2_2e.md | CANONICAL | DAVE_20241210 |
| Inter-turn Validator | CAPY_VALIDATOR_2_2e.md | CANONICAL | DAVE_20241210 |
| A.8 Validator | A8_VALIDATOR.md | EXPERIMENTAL | - |
| A.9 Validator | A9_VALIDATOR.md | EXPERIMENTAL | - |
| SCENARIO T1 Validator | SCENARIO_T1_VALIDATOR.md | EXPERIMENTAL | - |
| A.10 Validator | A10_VALIDATOR.md | EXPERIMENTAL | - |
| SC Validator | SC_VALIDATOR.md | CANONICAL | DAVE_ENRICH_SMOKE_20251220 |
| INT T1 Validator | INT_T1_VALIDATOR.md | EXPERIMENTAL | - |
| INT T2 Validator | INT_T2_VALIDATOR.md | EXPERIMENTAL | - |
| INT T3 Validator | INT_T3_VALIDATOR.md | EXPERIMENTAL | - |

### BASE Stage Atomized Files (CANONICAL)

The BASE prompt v2.2.2e is split into 3 atomic files for improved context management:

| File | Purpose | Size |
|------|---------|------|
| `G3BASE_2.2.2e_PROMPT.md` | Core instructions (Sections I-V) | 16KB |
| `G3BASE_2.2.2e_SCHEMAS.md` | JSON schemas (Appendix A) | 9KB |
| `G3BASE_2.2.2e_NORMDEFS.md` | DSL definitions (Appendix B) | 5KB |
| `BASE_CVR_KERNEL_2.2.2e.py` | Valuation kernel | 32KB |

**Status:** CANONICAL - smoke tested 2024-12-20. G3BASE_2.2.1e.md is HISTORICAL.

**Subagent loading:** Load all 3 prompt files + kernel reference. The embedded kernel (old Appendix C) has been removed.

### ENRICH Stage Atomized Files (CANONICAL)

The ENRICH prompt v2.2.2e is split into 3 atomic files plus kernel, mirroring the BASE pattern:

| File | Purpose | Size |
|------|---------|------|
| `G3ENRICH_2.2.2e_PROMPT.md` | Core instructions (Sections I-V) | 22KB |
| `G3ENRICH_2.2.2e_SCHEMAS.md` | JSON schemas (Appendix A) | 16KB |
| `G3ENRICH_2.2.2e_NORMDEFS.md` | DSL & financial definitions (Appendix B) | 13KB |
| `CVR_KERNEL_ENRICH_2.2.2e.py` | Valuation kernel | 39KB |

**Key updates from 2.2.1e:**
- 7-slot RQ architecture references (M-1, M-2, M-3a, M-3b, D-1, D-2, D-3)
- 4-file atomization for context management
- Version refs updated to G3_2.2.2e

**Status:** CANONICAL - smoke tested 2024-12-20. G3ENRICH_2.2.1e.md is HISTORICAL.

**Subagent loading:** Load all 3 prompt files. Kernel executed via Bash in T2 (not embedded in subagent context).

---

## SCENARIO Stage Orchestration (ENRICH → SCENARIO)

The SCENARIO stage transitions the CVR from deterministic State 2 (ENRICH output) to probabilistic State 3 by modeling discrete high-impact scenarios as causal interventions.

### Architecture (v2.2.2e)

**4-Scenario Limit:** Maximum 4 scenarios, prioritized by |P × M| (expected materiality).

**Scenario Types:**
| Type | Definition | Example |
|------|------------|---------|
| MAINLINE | High-probability, moderate impact | Expected M&A, product launch |
| BLUE_SKY | Low-probability transformative upside | Market dominance, breakthrough adoption |
| BLACK_SWAN | Low-probability catastrophic downside | Technological obsolescence, existential regulatory |

**Integration:** Structured State Enumeration (SSE) produces 2^4 = 16 states, filtered by constraints, renormalized to joint probability distribution.

### Stage Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. SCENARIO T1 (Opus Subagent)                              │
│    Input:  ENRICH T2 artifacts (A.1-A.9) +                  │
│            Scenario Research (RQ M-3a, M-3b outputs) +      │
│            G3_SCENARIO_2.2.2e_*.md (3 atomized files) +     │
│            CVR_KERNEL_SCEN_2_2_2e.py (contextual only)      │
│    Output: Scenario Execution Arguments JSON (in markdown)  │
│    Save:   06_SCENARIO/{TICKER}_SCEN_T1_{DATE}.md           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. SCENARIO T1 VALIDATOR (Opus Subagent)                    │
│    Prompt: validators/SCENARIO_T1_VALIDATOR.md              │
│    Check:  4 scenarios defined, probabilities valid,        │
│            interventions well-formed, constraints present   │
│    Output: PASS/FAIL + issues                               │
└──────────────────────┬──────────────────────────────────────┘
                       │ (proceed only if PASS)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. SCENARIO T2 (Opus Subagent)                              │
│    Input:  T1 output + ENRICH artifacts (fresh re-ingest)   │
│            + CVR_KERNEL_SCEN_2_2_2e.py (executable)         │
│    Execute: Kernel via Bash (Pattern 6)                     │
│    Output: A.10_SCENARIO_MODEL_OUTPUT (JSON) + narrative    │
│    Save:   06_SCENARIO/{TICKER}_SCEN_T2_{DATE}.md           │
│            + {TICKER}_A10_SCENARIO.json                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. A.10 VALIDATOR (Opus Subagent)                           │
│    Prompt: validators/A10_VALIDATOR.md                      │
│    Check:  Schema compliance, SSE math, distribution        │
│            metrics, Economic Governor satisfied             │
│    Output: PASS/WARN/FAIL + issues                          │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

SCENARIO outputs go in the analysis folder's `06_SCENARIO/` subdirectory:
```
production/analyses/{TICKER}_CAPY_{TIMESTAMP}/
├── 04_RQ/
├── 05_ENRICH/                       ← Input: State 2 artifacts
│   ├── {TICKER}_ENRICH_T1.md
│   ├── {TICKER}_ENRICH_T2.md
│   ├── A2_ANALYTIC_KG.json
│   ├── A3_CAUSAL_DAG.json
│   ├── A5_GESTALT_IMPACT_MAP.json
│   ├── A6_DR_DERIVATION_TRACE.json
│   └── A7_kernel_output.json
├── 06_SCENARIO/                     ← SCENARIO stage outputs
│   ├── {TICKER}_SCEN_T1_{DATE}.md
│   ├── {TICKER}_SCEN_T2_{DATE}.md
│   └── {TICKER}_A10_SCENARIO.json
├── 07_INTEGRATION/                  ← Next stage
└── pipeline_state.json
```

### Execution Commands (DEV: SMOKE TEST SCENARIO {TICKER})

**Step 0: Locate Most Recent ENRICH Output (Auto-Discovery)**
```
1. Search for ENRICH smoke test folders:
   ls -t workshop/smoke_tests/*ENRICH*{TICKER}* | head -5

2. If none found in workshop, check production:
   ls -t production/analyses/{TICKER}_*/05_ENRICH/ | head -5

3. Select the most recent folder with complete ENRICH output
   (must contain A7_kernel_output.json with State 2 IVPS)

4. Set {analysis_dir} to the parent of 05_ENRICH/
   Example: workshop/smoke_tests/{TICKER}_ENRICH_SMOKE_{TIMESTAMP}/
```

**Step 1: Validate Input (Pattern 10 - MANDATORY)**
```
READ files in {analysis_dir}/05_ENRICH/ to verify:
- A7_kernel_output.json exists with State 2 IVPS
- Extract and log: base_ivps, dr_static, terminal_g, terminal_roic
- Verify IVPS consistency: markdown must match kernel output JSON
```

**Step 2: Execute SCENARIO T1 (Opus Subagent)**
```
Spawn Opus subagent with:
- prompts/scenario/G3_SCENARIO_2.2.2e_PROMPT.md
- prompts/scenario/G3_SCENARIO_2.2.2e_SCHEMAS.md
- prompts/scenario/G3_SCENARIO_2.2.2e_NORMDEFS.md
- {analysis_dir}/05_ENRICH/*.md (all ENRICH artifacts)
- {analysis_dir}/04_RQ/RQ*_M-3a*.md, RQ*_M-3b*.md (scenario research)
- kernels/CVR_KERNEL_SCEN_2_2_2e.py (for context only, DO NOT EXECUTE)

Instruct: "Execute SCENARIO T1 for {TICKER}. Emit Scenario Execution
Arguments JSON embedded in markdown. DO NOT execute kernel."

Subagent writes output directly to disk (Pattern 1).
```

**Step 3: Validate SCENARIO T1**
```
Spawn Opus subagent with:
- validators/SCENARIO_T1_VALIDATOR.md
- The T1 output from step 2

Instruct: "Validate this SCENARIO T1 artifact."
```

**Step 4: Execute SCENARIO T2 (Opus Subagent)**
```
Spawn Opus subagent with:
- T1 output (for embedded JSON)
- {analysis_dir}/05_ENRICH/*.json (artifacts re-ingested fresh)
- kernels/CVR_KERNEL_SCEN_2_2_2e.py

Instruct: "Execute SCENARIO T2 for {TICKER}. Load kernel via Bash
and execute. Emit A.10_SCENARIO_MODEL_OUTPUT as JSON file."

Subagent executes kernel via Bash (Pattern 6).
Subagent writes output directly to disk (Pattern 1).
```

**Step 5: Validate A.10**
```
Spawn Opus subagent with:
- validators/A10_VALIDATOR.md
- The A.10 JSON from step 4

Instruct: "Validate this A.10 artifact."
```

### Critical Patterns Applied

| Pattern | Application |
|---------|-------------|
| Pattern 1: Direct-Write | Subagent writes T1/T2 output to disk, returns path only |
| Pattern 3: Two-Shot | T1 = analytical synthesis (no kernel), T2 = kernel execution |
| Pattern 5: JSON Repair | T2 can repair malformed T1 JSON before kernel execution |
| Pattern 6: Bash Kernel | T2 executes CVR_KERNEL_SCEN_2_2_2e.py via Bash |
| Pattern 7: Validators | Opus validator after T1 AND after T2 |
| Pattern 8: Atomized Prompts | 3 files (PROMPT/SCHEMAS/NORMDEFS) + kernel |
| Pattern 10: Input Validation | READ ENRICH artifacts, verify State 2 IVPS before T1 |

### SCENARIO Stage Files

| File | Location | Purpose |
|------|----------|---------|
| G3_SCENARIO_2.2.2e_PROMPT.md | prompts/scenario/ | Core instructions (Sections I-V) |
| G3_SCENARIO_2.2.2e_SCHEMAS.md | prompts/scenario/ | JSON schemas (Appendix A) |
| G3_SCENARIO_2.2.2e_NORMDEFS.md | prompts/scenario/ | DSL & financial definitions (Appendix B) |
| CVR_KERNEL_SCEN_2_2_2e.py | kernels/ | Scenario/SSE kernel |
| SCENARIO_T1_VALIDATOR.md | validators/ | T1 schema/semantic validator |
| A10_VALIDATOR.md | validators/ | A.10 completeness validator |

### SCENARIO Stage Atomized Files (EXPERIMENTAL)

The SCENARIO prompt v2.2.2e is split into 3 atomic files plus kernel:

| File | Purpose | Size |
|------|---------|------|
| `G3_SCENARIO_2.2.2e_PROMPT.md` | Core instructions (Sections I-V) | ~22KB |
| `G3_SCENARIO_2.2.2e_SCHEMAS.md` | JSON schemas (Appendix A) | ~20KB |
| `G3_SCENARIO_2.2.2e_NORMDEFS.md` | DSL & financial definitions (Appendix B) | ~14KB |
| `CVR_KERNEL_SCEN_2_2_2e.py` | Scenario/SSE kernel | 82KB |

**Key updates from 2.2.1e:**
- 3-file atomization for context management
- References updated to G3ENRICH_2.2.2e (7-slot RQ architecture)
- Schema version updated to G3_2.2.2eS
- Embedded kernel (old Appendix C) removed - delivered as separate file

**Status:** CANONICAL - smoke tested 2024-12-20 (DAVE). G3_SCENARIO_2_2_1e.md is HISTORICAL.

**Subagent loading:** Load all 3 prompt files. Kernel executed via Bash in T2 (not embedded in subagent context).

---

## SILICON COUNCIL Stage Orchestration (SCENARIO → SILICON COUNCIL)

The SILICON COUNCIL stage provides adversarial audit of MRC State 3 before finalization in INTEGRATION.

### Architecture (v2.2.2e)

**6-Audit Parallel Framework:**
- 6 specialized Opus subagents execute in parallel
- Each receives full Epistemic Parity Bundle (same context as upstream stages)
- Each writes JSON fragment directly to disk (Pattern 1)
- Validator consolidates into A.11_AUDIT_REPORT
- Simple consolidation only (INTEGRATION handles deconflicting)

**Audit Types:**
| Audit | Focus | A.11 Section |
|-------|-------|--------------|
| ACCOUNTING | Source integrity, ATP verification, data accuracy | source_integrity |
| FIT | Pipeline suitability, blind spots rubric | pipeline_fit_assessment |
| EPISTEMIC | Bayesian protocol compliance, Economic Governor | epistemic_integrity_assessment |
| RED_TEAM | Adversarial "what could go wrong" analysis | red_team_findings |
| DISTRIBUTIONAL | Distribution shape, investment implications | distributional_coherence |
| ECONOMIC_REALISM | Top-down plausibility, implied metrics check | economic_realism |

### Stage Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 0. AUTO-DISCOVERY: Locate Most Recent SCENARIO Output                       │
│    find smoke_tests/ -name "*SCENARIO*" -o -name "*A10*.json" | sort -r     │
│    Identify folder with complete 06_SCENARIO/ artifacts                     │
│    READ and validate: extract E[IVPS], State 3 metrics                      │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. PREPARE EPISTEMIC PARITY BUNDLE                                          │
│    Collect from {analysis_dir}:                                             │
│    - /source_docs/ (pre-processed financials)                               │
│    - /04_RQ/ (RQ1-RQ7 outputs)                                              │
│    - /05_ENRICH/ (A2-A7 + narratives)                                       │
│    - /06_SCENARIO/ (A10 + narratives)                                       │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. PARALLEL FAN-OUT: 6 Opus Subagents (Task tool, run_in_background: true)  │
│                                                                             │
│    Each subagent receives:                                                  │
│    - G3_SC_2.2.2e_PREAMBLE.md                                               │
│    - G3_SC_2.2.2e_{AUDIT_TYPE}.md                                           │
│    - G3_SC_2.2.2e_NORMDEFS.md                                               │
│    - G3_SC_2.2.2e_BLIND_SPOTS.md (FIT audit only)                           │
│    - Full Epistemic Parity Bundle                                           │
│                                                                             │
│    Instruct: "Execute {AUDIT_TYPE} audit for {TICKER}. Write JSON output    │
│    to {output_dir}/SC_{AUDIT_TYPE}_AUDIT.json. Return confirmation only."   │
│                                                                             │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
│  │ACCOUNTING │ │   FIT     │ │ EPISTEMIC │ │ RED_TEAM  │ │  DISTRIB  │ │ECON_REAL  │
│  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
│        │             │             │             │             │             │
│        ▼             ▼             ▼             ▼             ▼             ▼
│    Write to      Write to      Write to      Write to      Write to      Write to
│    disk          disk          disk          disk          disk          disk
└──────────────────────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. VALIDATOR (Opus Subagent)                                                │
│    Input: 6 JSON fragments from step 2                                      │
│    Prompt: validators/SC_VALIDATOR.md                                       │
│    Task: Simple consolidation into A.11_AUDIT_REPORT                        │
│          - Stitch JSON fragments                                            │
│          - Add metadata (ticker, date, execution context)                   │
│          - Generate critical_findings_summary                               │
│          - Generate executive_synthesis                                     │
│    Output: {TICKER}_A11_AUDIT_REPORT.json                                   │
│    Note: NO deconflicting - INTEGRATION handles that                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Directory Structure

SILICON COUNCIL outputs go in the analysis folder's `07_SILICON_COUNCIL/` subdirectory:
```
{analysis_dir}/
├── 05_ENRICH/                       ← Input: State 2 artifacts
├── 06_SCENARIO/                     ← Input: State 3 artifacts
│   ├── {TICKER}_SCEN_T1_*.md
│   ├── {TICKER}_SCEN_T2_*.md
│   └── {TICKER}_A10_SCENARIO.json
├── 07_SILICON_COUNCIL/              ← SILICON COUNCIL outputs
│   ├── SC_ACCOUNTING_AUDIT.json
│   ├── SC_FIT_AUDIT.json
│   ├── SC_EPISTEMIC_AUDIT.json
│   ├── SC_RED_TEAM_AUDIT.json
│   ├── SC_DISTRIBUTIONAL_AUDIT.json
│   ├── SC_ECONOMIC_REALISM_AUDIT.json
│   └── {TICKER}_A11_AUDIT_REPORT.json
└── 08_INTEGRATION/                  ← Next stage
```

### Execution Commands (DEV: SMOKE TEST SILICON COUNCIL {TICKER})

**Step 0: Auto-Discovery (Pattern 10 - MANDATORY)**
```
1. Search for SCENARIO outputs:
   find smoke_tests/ -name "*{TICKER}*A10*.json" | sort -r | head -5

2. If none in smoke_tests, check production:
   find production/analyses/ -name "*{TICKER}*A10*.json" | sort -r | head -5

3. Select most recent folder with complete 06_SCENARIO/
   (must contain A10_SCENARIO.json with E[IVPS])

4. READ and validate:
   - Extract E[IVPS], distribution stats
   - Verify State 2 → State 3 bridge is complete
   - Log baseline metrics

5. Set {analysis_dir} and {output_dir}
   Create 07_SILICON_COUNCIL/ if needed
```

**Step 1: Prepare Epistemic Parity Bundle**
```
Read all files from:
- {analysis_dir}/source_docs/ (or production/source_library/{TICKER}/)
- {analysis_dir}/04_RQ/
- {analysis_dir}/05_ENRICH/
- {analysis_dir}/06_SCENARIO/

Verify bundle completeness:
- 7 RQ files present
- ENRICH T1, T2, A2-A7 present
- SCENARIO T1, T2, A10 present
```

**Step 2: Execute 6 Parallel Audits**
```
Spawn 6 Opus subagents in parallel with Task tool:

For each AUDIT_TYPE in [ACCOUNTING, FIT, EPISTEMIC, RED_TEAM, DISTRIBUTIONAL, ECONOMIC_REALISM]:

Task(
  subagent_type: "general-purpose",
  model: "opus",
  run_in_background: true,
  prompt: """
    You are executing the {AUDIT_TYPE} audit for {TICKER}.

    Read the following prompt files:
    - prompts/silicon_council/G3_SC_2.2.2e_PREAMBLE.md
    - prompts/silicon_council/G3_SC_2.2.2e_{AUDIT_TYPE}.md
    - prompts/silicon_council/G3_SC_2.2.2e_NORMDEFS.md
    [For FIT only: - prompts/silicon_council/G3_SC_2.2.2e_BLIND_SPOTS.md]

    Epistemic Parity Bundle is in: {analysis_dir}

    Execute the audit per the prompt instructions.

    Write your JSON output to:
    {output_dir}/SC_{AUDIT_TYPE}_AUDIT.json

    Return ONLY: "Complete. File: {filepath}"
    Do NOT return the JSON content.
  """
)

Wait for all 6 tasks to complete via TaskOutput.
Verify all 6 JSON files exist with ls -la.
```

**Step 3: Run Validator**
```
Spawn Opus subagent:

Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
    You are the Silicon Council Validator for {TICKER}.

    Read: validators/SC_VALIDATOR.md

    Input files in {output_dir}/:
    - SC_ACCOUNTING_AUDIT.json
    - SC_FIT_AUDIT.json
    - SC_EPISTEMIC_AUDIT.json
    - SC_RED_TEAM_AUDIT.json
    - SC_DISTRIBUTIONAL_AUDIT.json
    - SC_ECONOMIC_REALISM_AUDIT.json

    Consolidate into A.11_AUDIT_REPORT per validator instructions.

    Write output to: {output_dir}/{TICKER}_A11_AUDIT_REPORT.json

    Return ONLY: "Complete. File: {filepath}"
  """
)

Verify A11 file exists.
Report summary to user.
```

**Step 4: Generate Markdown Copies (for human audit)**
```
Convert all JSON outputs to Markdown for human readability:
- SC_ACCOUNTING_AUDIT.json → SC_ACCOUNTING_AUDIT.md
- SC_FIT_AUDIT.json → SC_FIT_AUDIT.md
- SC_EPISTEMIC_AUDIT.json → SC_EPISTEMIC_AUDIT.md
- SC_RED_TEAM_AUDIT.json → SC_RED_TEAM_AUDIT.md
- SC_DISTRIBUTIONAL_AUDIT.json → SC_DISTRIBUTIONAL_AUDIT.md
- SC_ECONOMIC_REALISM_AUDIT.json → SC_ECONOMIC_REALISM_AUDIT.md
- {TICKER}_A11_AUDIT_REPORT.json → {TICKER}_A11_AUDIT_REPORT.md

Keep both JSON (for pipeline) and Markdown (for human audit).
Use simple JSON-to-Markdown conversion, do NOT transcribe/rewrite content.
```

### Critical Patterns Applied

| Pattern | Application |
|---------|-------------|
| Pattern 1: Direct-Write | Each audit subagent writes JSON to disk, returns path only |
| Pattern 7: Validators | Opus validator consolidates 6 fragments into A.11 |
| Pattern 8: Atomized Prompts | Preamble + 6 audit files + NORMDEFS + BLIND_SPOTS |
| Pattern 10: Input Validation | Auto-discover SCENARIO outputs, verify E[IVPS] before audits |

### SILICON COUNCIL Stage Files

| File | Location | Purpose |
|------|----------|---------|
| G3_SC_2.2.2e_PREAMBLE.md | prompts/silicon_council/ | Mission, inputs, guiding principles |
| G3_SC_2.2.2e_ACCOUNTING.md | prompts/silicon_council/ | Source integrity audit |
| G3_SC_2.2.2e_FIT.md | prompts/silicon_council/ | Pipeline fit assessment |
| G3_SC_2.2.2e_EPISTEMIC.md | prompts/silicon_council/ | Epistemic integrity audit |
| G3_SC_2.2.2e_RED_TEAM.md | prompts/silicon_council/ | Adversarial review |
| G3_SC_2.2.2e_DISTRIBUTIONAL.md | prompts/silicon_council/ | Distribution coherence |
| G3_SC_2.2.2e_ECON_REALISM.md | prompts/silicon_council/ | Economic realism audit |
| G3_SC_2.2.2e_NORMDEFS.md | prompts/silicon_council/ | Normative definitions reference |
| G3_SC_2.2.2e_BLIND_SPOTS.md | prompts/silicon_council/ | Pipeline blind spots reference |
| SC_VALIDATOR.md | validators/ | Consolidation validator |

### SILICON COUNCIL Stage Atomized Files (EXPERIMENTAL)

The SILICON COUNCIL prompt v2.2.2e is split into 10 atomic files:

| File | Purpose |
|------|---------|
| `G3_SC_2.2.2e_PREAMBLE.md` | Shared header (mission, inputs, guiding principles) |
| `G3_SC_2.2.2e_ACCOUNTING.md` | Source integrity audit objective |
| `G3_SC_2.2.2e_FIT.md` | Pipeline fit assessment objective |
| `G3_SC_2.2.2e_EPISTEMIC.md` | Epistemic integrity audit objective |
| `G3_SC_2.2.2e_RED_TEAM.md` | Red team adversarial review objective |
| `G3_SC_2.2.2e_DISTRIBUTIONAL.md` | Distributional coherence review objective |
| `G3_SC_2.2.2e_ECON_REALISM.md` | Economic realism audit objective (NEW) |
| `G3_SC_2.2.2e_NORMDEFS.md` | Normative definitions reference |
| `G3_SC_2.2.2e_BLIND_SPOTS.md` | Pipeline blind spots reference |
| `SC_VALIDATOR.md` | Consolidation validator |

**Key updates from 2.2.1e:**
- Atomized from 1 monolithic file to 10 specialized files
- Added Economic Realism audit (6th parallel audit)
- Changed from multi-LLM parallel execution to Claude Opus parallel subagents
- Simple consolidation validator (no deconflicting - INTEGRATION handles that)
- Direct-write protocol for all audit outputs

**Status:** EXPERIMENTAL - awaiting smoke test. G3_SILICON_COUNCIL_2.2.1e.md remains CANONICAL until smoke test passes.

**Subagent loading:** Each subagent loads Preamble + its audit file + NORMDEFS (+ BLIND_SPOTS for FIT only).

---

## INTEGRATION Stage Orchestration (SILICON COUNCIL → INTEGRATION)

### Purpose and Context

The INTEGRATION stage is the **final analytical stage** of the CAPY pipeline. It transitions the CVR from State 3 (Probabilistic) to State 4 (Finalized).

**What happened before INTEGRATION:**
1. **ENRICH** produced a deterministic intrinsic value per share (IVPS) calculation with artifacts A.1-A.9
2. **SCENARIO** added probabilistic scenario analysis on top, producing A.10 with E[IVPS] and distribution
3. **SILICON COUNCIL** audited both stages across 6 dimensions, producing A.11 audit reports

**What INTEGRATION does:**
1. **T1 (Adjudication):** Receives ALL upstream artifacts + ALL audit findings. Adjudicates each audit finding (ACCEPT/REJECT/MODIFY) against primary evidence. Determines what needs recalculation.
2. **T2 (Recalculation):** Executes kernel if any modifications were accepted. Produces finalized artifacts with amendments applied.
3. **T3 (Final Output):** Produces the **complete, clean, finalized CVR** - all narratives, all artifacts, no deprecated content. This is THE document for human review or IRR stage.

**Why Epistemic Parity matters:**
The INTEGRATION subagent must have access to the same evidence that upstream stages used. It cannot adjudicate audit findings without seeing the original source documents, RQ outputs, and analytical artifacts. This is non-negotiable.

### Architecture (v2.2.2e)

**Three-Shot Execution:**

| Turn | Name | Purpose | Key Output |
|------|------|---------|------------|
| T1 | Adjudication | Review SC findings, adjudicate against evidence | Adjudication decisions + T1 Handoff JSON |
| T2 | Recalculation | Execute kernel if cascade required | Finalized artifacts A.1-A.12 + state_4_active_inputs |
| T3 | Final Output | Produce complete CVR State 4 document | Clean, unified document with N1-N7 + A.1-A.12 |

### Directory Structure

```
{analysis_dir}/
├── 00_source/ or source_docs/       ← Source financials (10-K, 10-Q, transcripts)
├── 04_RQ/                           ← Research outputs (RQ1-RQ7, A.8, A.9)
├── 05_ENRICH/                       ← State 2 artifacts (A.1-A.9 + narratives)
├── 06_SCENARIO/                     ← State 3 artifacts (A.10 + narratives)
├── 07_SILICON_COUNCIL/              ← Audit outputs (A.11 from all instances)
├── 08_INTEGRATION/                  ← INTEGRATION outputs
│   ├── {TICKER}_INT_T1_{DATE}.md        ← T1: Adjudication output
│   ├── {TICKER}_INT_T2_{DATE}.md        ← T2: Recalculation output
│   ├── {TICKER}_INT_T3_{DATE}.md        ← T3: Final CVR State 4
│   └── {TICKER}_A12_INTEGRATION_TRACE.json
└── 09_IRR/                          ← Next stage (receives T3 output)
```

### Stage Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 0: AUTO-DISCOVERY AND INPUT VALIDATION                                 │
│                                                                             │
│ Locate most recent complete pipeline run:                                   │
│   find smoke_tests/ -name "*A11*.json" | sort -r | head -5                  │
│                                                                             │
│ Verify folder contains ALL required inputs (see Step 1).                    │
│ READ key files to extract baseline metrics:                                 │
│   - E[IVPS] from A.10                                                       │
│   - Pipeline Fit grade(s) from A.11                                         │
│   - Count of CRITICAL/HIGH findings                                         │
│                                                                             │
│ Set {analysis_dir} to the pipeline run folder.                              │
│ Create 08_INTEGRATION/ if it doesn't exist.                                 │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: PREPARE EPISTEMIC PARITY BUNDLE                                     │
│                                                                             │
│ The T1 subagent MUST receive everything Silicon Council received,           │
│ PLUS the A.11 audit outputs. This is mandatory for principled adjudication. │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ SOURCE DOCUMENTS (Discovery Record)                                     │ │
│ │ Location: {analysis_dir}/00_source/ or /source_docs/                    │ │
│ │                                                                         │ │
│ │ Files:                                                                  │ │
│ │   • 10-K filing (full or extracted.md)                                  │ │
│ │   • 10-Q filings (all available quarters)                               │ │
│ │   • Earnings call transcripts                                           │ │
│ │   • Investor presentations                                              │ │
│ │   • Pre-processed financials spreadsheet                                │ │
│ │                                                                         │ │
│ │ Why needed: Primary evidence for adjudicating disputed claims.          │ │
│ │ The subagent may need to verify facts cited by SC audits.               │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ RESEARCH QUESTION OUTPUTS                                               │ │
│ │ Location: {analysis_dir}/04_RQ/                                         │ │
│ │                                                                         │ │
│ │ Files:                                                                  │ │
│ │   • RQ1_*.md through RQ7_*.md (7 research reports)                      │ │
│ │   • {TICKER}_A8_RESEARCH_PLAN.json                                      │ │
│ │   • {TICKER}_A9_RESEARCH_RESULTS.json                                   │ │
│ │                                                                         │ │
│ │ Why needed: External research that informed ENRICH/SCENARIO.            │ │
│ │ SC may have challenged assumptions based on RQ findings.                │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ ENRICH OUTPUTS (State 2 - Deterministic IVPS)                           │ │
│ │ Location: {analysis_dir}/05_ENRICH/                                     │ │
│ │                                                                         │ │
│ │ Files:                                                                  │ │
│ │   • {TICKER}_ENRICH_T1.md (analysis narrative)                          │ │
│ │   • {TICKER}_ENRICH_T2.md (kernel output narrative)                     │ │
│ │   • A1_EPISTEMIC_ANCHORS.json                                           │ │
│ │   • A2_ANALYTIC_KG.json                                                 │ │
│ │   • A3_CAUSAL_DAG.json                                                  │ │
│ │   • A5_GESTALT_IMPACT_MAP.json                                          │ │
│ │   • A6_DR_DERIVATION_TRACE.json                                         │ │
│ │   • A7_LIGHTWEIGHT_VALUATION_SUMMARY.json (contains Base Case IVPS)     │ │
│ │   • A9_ENRICHMENT_TRACE.json                                            │ │
│ │                                                                         │ │
│ │ Why needed: The deterministic valuation that SCENARIO built upon.       │ │
│ │ SC may have challenged base case assumptions.                           │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ SCENARIO OUTPUTS (State 3 - Probabilistic E[IVPS])                      │ │
│ │ Location: {analysis_dir}/06_SCENARIO/                                   │ │
│ │                                                                         │ │
│ │ Files:                                                                  │ │
│ │   • {TICKER}_SCEN_T1.md (scenario identification narrative)             │ │
│ │   • {TICKER}_SCEN_T2.md (SSE execution narrative)                       │ │
│ │   • {TICKER}_A10_SCENARIO.json (scenarios, probabilities, distribution) │ │
│ │                                                                         │ │
│ │ Why needed: The probabilistic layer that SC audited.                    │ │
│ │ SC may have challenged scenario selection, probabilities, or SSE math.  │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ SILICON COUNCIL OUTPUTS (A.11 Audit Reports)                            │ │
│ │ Location: {analysis_dir}/07_SILICON_COUNCIL/                            │ │
│ │                                                                         │ │
│ │ Files:                                                                  │ │
│ │   • SC_ACCOUNTING_AUDIT.json (source integrity findings)                │ │
│ │   • SC_FIT_AUDIT.json (pipeline fit assessment)                         │ │
│ │   • SC_EPISTEMIC_AUDIT.json (Bayesian protocol compliance)              │ │
│ │   • SC_RED_TEAM_AUDIT.json (adversarial review)                         │ │
│ │   • SC_DISTRIBUTIONAL_AUDIT.json (distribution coherence)               │ │
│ │   • SC_ECONOMIC_REALISM_AUDIT.json (top-down plausibility)              │ │
│ │   • {TICKER}_A11_AUDIT_REPORT.json (consolidated audit report)          │ │
│ │   • *.md versions of above (human-readable)                             │ │
│ │                                                                         │ │
│ │ Why needed: THE INPUT that triggers adjudication.                       │ │
│ │ Each finding must be evaluated: ACCEPT, REJECT, or MODIFY.              │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ VERIFICATION: Before proceeding, confirm ALL folders exist and contain     │
│ the expected files. Log file counts. If anything is missing, STOP.         │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: INTEGRATION T1 — ADJUDICATION                                       │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to adjudicate Silicon Council findings            │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/integration/G3_INTEGRATION_2.2.2e_PROMPT.md                    │
│   2. prompts/integration/G3_INTEGRATION_2.2.2e_SCHEMAS.md                   │
│   3. prompts/integration/G3_INTEGRATION_2.2.2e_NORMDEFS.md                  │
│   4. kernels/CVR_KERNEL_INT_2.2.2e.py (FOR CONTEXT ONLY - DO NOT EXECUTE)   │
│                                                                             │
│ INPUT FILES TO ATTACH (Full Epistemic Parity Bundle from Step 1):           │
│   • ALL source documents from 00_source/                                    │
│   • ALL RQ outputs from 04_RQ/                                              │
│   • ALL ENRICH outputs from 05_ENRICH/                                      │
│   • ALL SCENARIO outputs from 06_SCENARIO/                                  │
│   • ALL SILICON COUNCIL outputs from 07_SILICON_COUNCIL/                    │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute INTEGRATION Turn 1 for {TICKER}.                                 │
│                                                                             │
│    Your task: Adjudicate all Silicon Council findings against the           │
│    primary evidence. For each finding, determine disposition:               │
│    ACCEPT (State 3 needs modification), REJECT (State 3 stands),            │
│    or MODIFY (partial adjustment needed).                                   │
│                                                                             │
│    Execute Phases A-C per the prompt:                                       │
│    - Phase A: Initialization and Triage (dock all findings)                 │
│    - Phase B: Adjudication Loop (evaluate each finding)                     │
│    - Phase C: Scenario Reconciliation (finalize scenario set)               │
│                                                                             │
│    DO NOT execute the kernel. It is provided for context only.              │
│                                                                             │
│    Output: Adjudication decisions + T1 Handoff JSON (cascade scope).        │
│    Write output to: {output_dir}/{TICKER}_INT_T1_{DATE}.md                  │
│    Return confirmation and filepath only."                                  │
│                                                                             │
│ OUTPUT PRODUCED:                                                            │
│   • {TICKER}_INT_T1_{DATE}.md containing:                                   │
│     - Adjudication reasoning for each finding                               │
│     - Disposition (ACCEPT/REJECT/MODIFY) for each finding                   │
│     - T1 Handoff JSON with:                                                 │
│       • cascade_scope (FULL/PARTIAL_SCENARIO/PARTIAL_SSE/NONE)              │
│       • modifications_to_apply (list of specific changes)                   │
│       • scenarios_finalized (post-reconciliation scenario set)              │
│                                                                             │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns path  │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: INTEGRATION T1 VALIDATOR                                            │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate T1 output                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/INT_T1_VALIDATOR.md                                            │
│                                                                             │
│ INPUT FILE:                                                                 │
│   {output_dir}/{TICKER}_INT_T1_{DATE}.md (from Step 2)                      │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • All CRITICAL findings have explicit disposition                         │
│   • All HIGH findings have explicit disposition                             │
│   • T1 Handoff JSON is well-formed and complete                             │
│   • cascade_scope is valid enum value                                       │
│   • If cascade_scope != NONE, modifications_to_apply is non-empty           │
│   • scenarios_finalized contains ≤4 scenarios                               │
│                                                                             │
│ IF FAIL: Stop. Report issues. Do not proceed to T2.                         │
│ IF PASS: Proceed to Step 4.                                                 │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │ (proceed only if PASS)
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: INTEGRATION T2 — RECALCULATION                                      │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to execute recalculation cascade (if needed)      │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/integration/G3_INTEGRATION_2.2.2e_PROMPT.md                    │
│   2. prompts/integration/G3_INTEGRATION_2.2.2e_SCHEMAS.md                   │
│   3. prompts/integration/G3_INTEGRATION_2.2.2e_NORMDEFS.md                  │
│   4. kernels/CVR_KERNEL_INT_2.2.2e.py (EXECUTABLE IN T2)                    │
│                                                                             │
│ INPUT FILES TO ATTACH:                                                      │
│   • {output_dir}/{TICKER}_INT_T1_{DATE}.md (T1 output with Handoff JSON)    │
│   • State 3 artifacts RE-INGESTED FRESH from 06_SCENARIO/:                  │
│     - {TICKER}_A10_SCENARIO.json                                            │
│     - A5_GESTALT_IMPACT_MAP.json (if GIM modifications needed)              │
│     - A7_LIGHTWEIGHT_VALUATION_SUMMARY.json                                 │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute INTEGRATION Turn 2 for {TICKER}.                                 │
│                                                                             │
│    Your task: Apply the modifications from T1 and execute recalculation     │
│    cascade if required.                                                     │
│                                                                             │
│    Execute Phases D-E per the prompt:                                       │
│    - Phase D: Recalculation Cascade (execute kernel if cascade needed)      │
│    - Phase E: Distributional Re-Analysis (document State 3→4 bridge)        │
│                                                                             │
│    If cascade_scope = NONE: Lock State 4 = State 3, no kernel execution.    │
│    If cascade_scope != NONE: Load kernel via Bash and execute appropriate   │
│    functions (execute_cvr_workflow, execute_scenario_intervention, etc.)    │
│                                                                             │
│    Output:                                                                  │
│    - Finalized artifacts A.1-A.12 with amendments applied                   │
│    - A.12_INTEGRATION_TRACE (full adjudication record)                      │
│    - state_4_active_inputs (pre-merged inputs for IRR)                      │
│                                                                             │
│    Write outputs to:                                                        │
│    - {output_dir}/{TICKER}_INT_T2_{DATE}.md                                 │
│    - {output_dir}/{TICKER}_A12_INTEGRATION_TRACE.json                       │
│    Return confirmation and filepaths only."                                 │
│                                                                             │
│ OUTPUT PRODUCED:                                                            │
│   • {TICKER}_INT_T2_{DATE}.md containing:                                   │
│     - Recalculation cascade log (what was executed)                         │
│     - State 3 → State 4 bridge (delta analysis)                             │
│     - All finalized artifacts A.1-A.12 embedded                             │
│     - state_4_active_inputs block                                           │
│   • {TICKER}_A12_INTEGRATION_TRACE.json (standalone artifact)               │
│                                                                             │
│ PATTERN: Bash Kernel (Pattern 6) - execute kernel via Bash if cascade needed│
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns path   │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 5: INTEGRATION T2 VALIDATOR                                            │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate T2 output                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/INT_T2_VALIDATOR.md                                            │
│                                                                             │
│ INPUT FILES:                                                                │
│   • {output_dir}/{TICKER}_INT_T2_{DATE}.md                                  │
│   • {output_dir}/{TICKER}_A12_INTEGRATION_TRACE.json                        │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • All artifacts A.1-A.12 present                                          │
│   • Amendment manifest documents all changes                                │
│   • state_4_active_inputs is complete                                       │
│   • State bridge shows valid State 3 → State 4 delta                        │
│   • If cascade executed: kernel output validates (sums to 1.0, etc.)        │
│   • A.12 schema compliance                                                  │
│                                                                             │
│ IF FAIL: Stop. Report issues. Do not proceed to T3.                         │
│ IF PASS: Proceed to Step 6.                                                 │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │ (proceed only if PASS)
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 6: INTEGRATION T3 — FINAL CVR OUTPUT                                   │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to produce complete, finalized CVR State 4        │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ THIS IS THE FINAL OUTPUT. It must be:                                       │
│   • Complete (all narratives N1-N7, all artifacts A.1-A.12)                 │
│   • Clean (no deprecated content, no duplication)                           │
│   • Ready for human review or IRR stage consumption                         │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/integration/G3_INTEGRATION_2.2.2e_PROMPT.md                    │
│   2. prompts/integration/G3_INTEGRATION_2.2.2e_SCHEMAS.md                   │
│                                                                             │
│ INPUT FILES TO ATTACH:                                                      │
│   • {output_dir}/{TICKER}_INT_T1_{DATE}.md (adjudication work)              │
│   • {output_dir}/{TICKER}_INT_T2_{DATE}.md (finalized artifacts)            │
│                                                                             │
│ DO NOT ATTACH deprecated upstream narratives (BASE_T2, ENRICH_T2, SCEN_T2). │
│ The adjudicated versions from T1/T2 supersede those.                        │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute INTEGRATION Turn 3 for {TICKER}.                                 │
│                                                                             │
│    Your task: Produce the COMPLETE, FINALIZED CVR State 4 document.         │
│    This is THE output of the entire CAPY pipeline to date.                  │
│                                                                             │
│    Execute Phase F per the prompt:                                          │
│    - Compile all narratives N1-N7 (finalized versions from T1/T2)           │
│    - Embed all artifacts A.1-A.12 (finalized versions from T2)              │
│    - Include state_4_active_inputs (for IRR consumption)                    │
│                                                                             │
│    Narrative inventory:                                                     │
│    - N1: Investment Thesis (finalized)                                      │
│    - N2: Invested Capital Modeling (finalized)                              │
│    - N3: Economic Governor & Constraints (finalized)                        │
│    - N4: Risk Assessment & DR Derivation (finalized)                        │
│    - N5: Enrichment Synthesis (finalized)                                   │
│    - N6: Scenario Model Synthesis (finalized)                               │
│    - N7: Adjudication Synthesis (from T1 work)                              │
│                                                                             │
│    Artifact inventory:                                                      │
│    - A.1 through A.12 (all finalized, amendments applied)                   │
│    - state_4_active_inputs                                                  │
│                                                                             │
│    The output must contain NO deprecated content and NO duplication.        │
│    A human analyst reading only this document should have everything        │
│    they need to understand and evaluate the valuation.                      │
│                                                                             │
│    Write output to: {output_dir}/{TICKER}_INT_T3_{DATE}.md                  │
│    Return confirmation and filepath only."                                  │
│                                                                             │
│ OUTPUT PRODUCED:                                                            │
│   • {TICKER}_INT_T3_{DATE}.md — THE COMPLETE CVR STATE 4 DOCUMENT           │
│     This file contains:                                                     │
│     - Executive Summary with E[IVPS], key metrics, confidence               │
│     - N1-N7 narratives (finalized, adjudicated)                             │
│     - A.1-A.12 artifacts (finalized, amendments applied)                    │
│     - state_4_active_inputs (computational inputs for IRR)                  │
│     - Pipeline Fit assessment and confidence characterization               │
│                                                                             │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns path   │
│ PATTERN: Surgical Stitching (Pattern 11) - concatenate from T1/T2 outputs   │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 7: INTEGRATION T3 VALIDATOR                                            │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate final CVR output                      │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/INT_T3_VALIDATOR.md                                            │
│                                                                             │
│ INPUT FILE:                                                                 │
│   {output_dir}/{TICKER}_INT_T3_{DATE}.md                                    │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • All narratives N1-N7 present                                            │
│   • All artifacts A.1-A.12 present and complete                             │
│   • state_4_active_inputs present and complete                              │
│   • No deprecated content (check for stale State 3 references)              │
│   • No duplication (narratives not repeated)                                │
│   • Executive summary matches embedded artifact values                      │
│   • Document is self-contained (human can read without other files)         │
│                                                                             │
│ IF FAIL: Report issues. May need T3 re-execution.                           │
│ IF PASS: INTEGRATION stage complete. Output ready for human or IRR.         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Execution Commands (DEV: SMOKE TEST INTEGRATION {TICKER})

Execute the steps above in sequence. Key commands:

**Step 0: Auto-Discovery**
```bash
# Find most recent pipeline run with SC outputs
find smoke_tests/ -name "*{TICKER}*A11*.json" | sort -r | head -5

# Or check production
find production/analyses/ -name "*{TICKER}*A11*.json" | sort -r | head -5

# Set analysis_dir to parent folder
# Create output directory
mkdir -p {analysis_dir}/08_INTEGRATION/
```

**Step 1: Verify Bundle Completeness**
```bash
# Verify all input folders exist and have files
ls {analysis_dir}/00_source/
ls {analysis_dir}/04_RQ/
ls {analysis_dir}/05_ENRICH/
ls {analysis_dir}/06_SCENARIO/
ls {analysis_dir}/07_SILICON_COUNCIL/

# Count files in each
find {analysis_dir}/00_source/ -type f | wc -l
find {analysis_dir}/04_RQ/ -type f | wc -l
# ... etc
```

**Steps 2-7: Spawn Subagents**
Use Task tool with model="opus" for each step. See Stage Flow above for exact prompts and inputs.

### Critical Patterns Applied

| Pattern | Application |
|---------|-------------|
| Pattern 1: Direct-Write | All subagents write to disk, return filepath only |
| Pattern 3: Two-Shot (Extended) | T1=adjudication, T2=recalculation, T3=final output |
| Pattern 5: JSON Repair | T2 can repair malformed T1 JSON before kernel execution |
| Pattern 6: Bash Kernel | T2 executes CVR_KERNEL_INT via Bash if cascade required |
| Pattern 7: Validators | Opus validator after T1, T2, AND T3 |
| Pattern 8: Atomized Prompts | 3 files (PROMPT/SCHEMAS/NORMDEFS) + kernel |
| Pattern 10: Input Validation | Verify full bundle before T1; verify artifacts before T2/T3 |
| Pattern 11: Surgical Stitching | T3 concatenates from T1/T2, no regeneration |

### INTEGRATION Stage Files

| File | Location | Purpose |
|------|----------|---------|
| G3_INTEGRATION_2.2.2e_PROMPT.md | prompts/integration/ | Core instructions (Sections I-V) |
| G3_INTEGRATION_2.2.2e_SCHEMAS.md | prompts/integration/ | JSON schemas (Appendix A) |
| G3_INTEGRATION_2.2.2e_NORMDEFS.md | prompts/integration/ | DSL & financial definitions (Appendix B) |
| CVR_KERNEL_INT_2.2.2e.py | kernels/ | Recalculation kernel |
| INT_T1_VALIDATOR.md | validators/ | T1 adjudication validator |
| INT_T2_VALIDATOR.md | validators/ | T2 recalculation validator |
| INT_T3_VALIDATOR.md | validators/ | T3 final output validator |

### INTEGRATION Stage Atomized Files (EXPERIMENTAL)

| File | Purpose | Lines |
|------|---------|-------|
| `G3_INTEGRATION_2.2.2e_PROMPT.md` | Core instructions (Sections I-V) | 1307 |
| `G3_INTEGRATION_2.2.2e_SCHEMAS.md` | JSON schemas (Appendix A) | 512 |
| `G3_INTEGRATION_2.2.2e_NORMDEFS.md` | DSL & financial definitions (Appendix B) | 567 |
| `CVR_KERNEL_INT_2.2.2e.py` | Recalculation kernel | (existing) |

**Status:** EXPERIMENTAL - awaiting smoke test.

**Subagent loading:** Load all 3 prompt files. Kernel attached for T1 context, executed via Bash in T2.
