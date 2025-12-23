# CAPY Workshop - Prompt Development Environment

> **Version:** 0.14.1
> **Last reviewed:** 2024-12-23
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

**Key Patterns for Pipeline Execution:**
- Pattern 12: Canonical Snapshot - each stage folder contains COMPLETE artifact set; orchestrator uses `cp` (not Claude) for copy-forward
- Pattern 13: Kernel Receipts - JSON proof of real kernel execution (sha256, exit_code, timing)
- See `../shared/PATTERNS.md` for patterns 1-13 documentation

**Canonical Snapshot Naming:** `{TICKER}_{ARTIFACT}_{STAGE}.{ext}` (e.g., `DAVE_A5_GIM_ENRICH.json`)

---

## CLAUDE.md Versioning

This instruction file is itself experimental and will evolve.

When updating this file:
1. Increment version number above
2. Note change in git commit message
3. If significant change, add entry to `patches/PATCH_TRACKER.md`

---

## Folder Structure

### Workshop Folder

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
├── claude_snapshots/  # Archived CLAUDE.md versions
└── smoke_tests/       # Test outputs (pruned monthly)
```

### Analysis Folder Structure (Smoke Tests & Production)

Each analysis run creates this folder structure:

```
{TICKER}_{CONTEXT}_{YYYYMMDD}_{HHMMSS}/
├── 00_source/              # Input documents (copied from source_library)
├── 01_T1/                  # BASE Turn 1 outputs
├── 02_REFINE/              # BASE REFINE outputs
├── 03_T2/                  # BASE Turn 2 / Kernel outputs
├── 04_RQ/                  # RQ_Gen + RQ_Ask outputs (A.8, A.9, RQ1-RQ7)
├── 05_ENRICH/              # ENRICH T1 + T2 outputs
├── 06_SCENARIO/            # SCENARIO outputs + A.10
├── 07_SILICON_COUNCIL/     # SC 6× audit outputs + A.11
├── 08_INTEGRATION/         # INTEGRATION T1-T3 outputs + A.12
├── 09_IRR/                 # IRR outputs + A.13 + A.14
├── PIPELINE_STATE.md       # Progress tracker (updated after each stage)
└── {TICKER}_FINAL_CVR.md   # Consolidated human-readable output (post-IRR)
```

**Context naming:**
- Smoke tests: `{TICKER}_SMOKE_{YYYYMMDD}_{HHMMSS}`
- Production: `{TICKER}_CAPY_{YYYYMMDD}_{HHMMSS}`

**Each stage folder contains a complete artifact snapshot** (Pattern 12). Unchanged artifacts are copied forward with suffix rename by the orchestrator using `cp` (not Claude read/write).

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

## Source Document Commands

These commands handle PDF preprocessing - converting raw PDFs into machine-readable text for analysis.

### SOURCE: UPLOAD {TICKER}

> **⚠️ MANDATORY: Read `orchestration/SOURCE_STAGE.md` BEFORE preprocessing.**
> **⚠️ DO NOT use `pdftotext`. Use the Python implementation below.**
> **⚠️ BOTH text extraction AND image extraction are REQUIRED.**

Auto-find, organize, and preprocess PDF documents for a company.

**Trigger:** User says `SOURCE: UPLOAD {TICKER}` after dropping PDFs into the repository.

**Steps:**

1. **Scan for unprocessed PDFs:**
   - Check `../production/source_library/{TICKER}/` for existing docs
   - Find any `*.pdf` files NOT yet having corresponding `*.extracted.md`

2. Create `../production/source_library/{TICKER}/` if it doesn't exist

3. **Auto-preprocess each PDF:**
   - Text extraction: `pdfplumber` → `{filename}.extracted.md`
   - Visual extraction: `pdf2image` → `{filename}_pages/` (PNG images)
   - Both outputs saved alongside the PDF

4. Generate/update inventory file `source_library/{TICKER}/INVENTORY.md`:
   ```markdown
   # {TICKER} Source Documents

   Last updated: {YYYY-MM-DD HH:MM}

   ## Documents
   | PDF | Extracted Text | Page Images | Pages |
   |-----|----------------|-------------|-------|
   | filename.pdf | filename.extracted.md | filename_pages/ | N |
   ```

5. Report: "Found {N} PDFs. Processed into source_library/{TICKER}/. Ready for CAPY: RUN."

**Preprocessing Implementation:**

```python
import pdfplumber
from pdf2image import convert_from_path
from pathlib import Path

def extract_text(pdf_path: Path) -> str:
    """Extract text from PDF using pdfplumber."""
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            text_parts.append(f"--- Page {i} ---\n{text}")
    return "\n\n".join(text_parts)

def extract_images(pdf_path: Path, output_dir: Path) -> int:
    """Convert PDF pages to PNG images."""
    output_dir.mkdir(parents=True, exist_ok=True)
    images = convert_from_path(pdf_path, dpi=150)
    for i, img in enumerate(images, 1):
        img.save(output_dir / f"page_{i:03d}.png", "PNG")
    return len(images)

def preprocess_pdf(pdf_path: Path):
    """Full preprocessing: text + images."""
    # Text extraction
    text = extract_text(pdf_path)
    md_path = pdf_path.with_suffix(".extracted.md")
    md_path.write_text(f"# {pdf_path.stem}\n\nExtracted: {datetime.now().isoformat()}\n\n{text}")

    # Image extraction
    img_dir = pdf_path.parent / f"{pdf_path.stem}_pages"
    page_count = extract_images(pdf_path, img_dir)

    return {"text_file": md_path, "image_dir": img_dir, "pages": page_count}
```

**Dependencies:**
```bash
brew install poppler              # Provides pdftoppm for pdf2image
pip3 install pdfplumber pdf2image pillow
```

See `LOCAL_ENV_SETUP.md` for full installation instructions.

**Usage Notes:**
- Source documents live in `../production/source_library/` (shared between workshop and production)
- Workshop smoke tests copy from source_library to analysis 00_source/
- Multiple filings per company supported (10-K, 10-Q, transcripts, presentations)
- If preprocessing fails, PDF is kept but flagged in INVENTORY.md
- Running again will find any new PDFs and add to existing folder

---

## Pipeline Execution Commands

These commands execute the CAPY analysis pipeline. They can be run in either workshop (for smoke tests) or production (for real analyses).

### CAPY: RUN {TICKER}

**Executes the FULL CAPY pipeline from raw PDFs to IRR.**

This is the one-click autonomous execution command. Requires raw PDFs in `source_library/{TICKER}/` or pre-existing smoke test folder.

```
┌─────────────────────────────────────────────────────────────┐
│  CAPY: RUN {TICKER} (Full Autonomous Pipeline)              │
├─────────────────────────────────────────────────────────────┤
│  Stage 0: SOURCE_PREPROCESSING                              │
│     └── Check source_library/{TICKER}/ for raw PDFs         │
│         If *.extracted.md missing → run SOURCE: UPLOAD      │
│                                                             │
│  Stage 1: INIT                                              │
│     └── Create analysis folder, copy sources to 00_source/  │
│                                                             │
│  Stage 2: BASE (T1 → REFINE → T2)                          │
│     └── Validate after each turn → FAIL? Stop               │
│     └── Copy-forward artifacts to 04_RQ/ (Pattern 12)       │
│                                                             │
│  Stage 3: RQ (RQ_GEN → 7× parallel RQ_ASK)                 │
│     └── Validate A.8, A.9 → FAIL? Stop                      │
│     └── Copy-forward artifacts to 05_ENRICH/                │
│                                                             │
│  Stage 4: ENRICH (T1 → T2)                                 │
│     └── Validate → FAIL? Stop                               │
│     └── Copy-forward artifacts to 06_SCENARIO/              │
│                                                             │
│  Stage 5: SCENARIO (T1 → T2)                               │
│     └── Validate A.10 → FAIL? Stop                          │
│     └── Copy-forward artifacts to 07_SILICON_COUNCIL/       │
│                                                             │
│  Stage 6: SILICON_COUNCIL (6× parallel audits → A.11)      │
│     └── Validate → FAIL? Stop                               │
│     └── Copy-forward artifacts to 08_INTEGRATION/           │
│                                                             │
│  Stage 7: INTEGRATION (T1 → T2 → T3)                       │
│     └── Validate each turn → FAIL? Stop                     │
│     └── Copy-forward artifacts to 09_IRR/                   │
│                                                             │
│  Stage 8: IRR (T1 → T2)                                    │
│     └── Validate → COMPLETE                                 │
│                                                             │
│  Stage 9: FINAL_CVR                                         │
│     └── Run generate_final_cvr.sh for consolidated output   │
└─────────────────────────────────────────────────────────────┘
```

**Behavior:**
- Runs autonomously without human checkpoints
- Updates PIPELINE_STATE.md after each stage
- On validation failure: Stops and reports
- On fatal error: Writes error state, stops cleanly

**Copy-Forward Protocol (Pattern 12):**
Between each stage, the orchestrator copies ALL artifacts from the previous stage folder to the next stage folder with suffix rename. This uses `cp` command (Bash), NOT Claude read/write, to avoid truncation.

```bash
# Example: After ENRICH completes, before SCENARIO starts
for f in {analysis_dir}/05_ENRICH/{TICKER}_*_ENRICH.json; do
  base=$(basename "$f" | sed 's/_ENRICH\.json$//')
  cp "$f" "{analysis_dir}/06_SCENARIO/${base}_SCEN.json"
done
```

---

### CAPY: RUN {START}->{END} {TICKER}

**Executes a PARTIAL pipeline from {START} stage through {END} stage.**

Use this for debugging, re-running specific stages, or resuming after a failure.

**Valid stages:** SOURCE, BASE, RQ, ENRICH, SCENARIO, SC, INT, IRR

**Examples:**
```
CAPY: RUN BASE->SCENARIO DAVE     # Run BASE through SCENARIO, stop before SC
CAPY: RUN ENRICH->IRR DAVE        # Resume from ENRICH through IRR
CAPY: RUN SCENARIO->SCENARIO DAVE # Re-run just SCENARIO stage
```

**Prerequisites:**
- For partial runs starting after BASE, the prior stage's output folder must exist with complete artifacts
- Pattern 10 (Input Validation): READ files to verify completeness before proceeding

**Behavior:**
- Same as full pipeline, but starts at {START} and stops after {END}
- Copy-forward protocol applies between stages
- Validation occurs after each stage

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


---

## Stage Orchestration (External Files)

**Pipeline orchestration has been extracted into separate versioned files** for maintainability and context management.

### Stage Reference Table

| Stage | File | Pipeline Position |
|-------|------|-------------------|
| SOURCE | `orchestration/SOURCE_STAGE.md` | 0/9 (PDF → SOURCE) |
| BASE | `orchestration/BASE_STAGE.md` | 1/9 (SOURCE → BASE) |
| RQ | `orchestration/RQ_STAGE.md` | 2/9 (BASE → RQ) |
| ENRICH | `orchestration/ENRICH_STAGE.md` | 3/9 (RQ → ENRICH) |
| SCENARIO | `orchestration/SCENARIO_STAGE.md` | 4/9 (ENRICH → SCENARIO) |
| SILICON COUNCIL | `orchestration/SC_STAGE.md` | 5/9 (SCENARIO → SC) |
| INTEGRATION | `orchestration/INTEGRATION_STAGE.md` | 6/9 (SC → INTEGRATION) |
| IRR | `orchestration/IRR_STAGE.md` | 7/9 (INTEGRATION → IRR) |
| FINAL CVR | `orchestration/FINAL_CVR_STAGE.md` | 8/9 (Post-IRR concatenation) |

### When to Read Stage Files

**Before executing any stage:** Read the corresponding orchestration file. Each file contains:
- Stage flow diagram with step-by-step instructions
- Directory structure and file naming
- Copy-forward protocol (Pattern 12)
- Exact subagent prompts and input files
- Validator instructions
- Critical patterns applied

**Example:**
```
# Before running ENRICH stage
Read: workshop/orchestration/ENRICH_STAGE.md
```

### Orchestration File Versioning

Each stage file includes a version header extracted from CLAUDE.md:
```
> **Version:** 1.0.0
> **Extracted from:** workshop/CLAUDE.md v0.12.1
```

When updating orchestration, increment the stage file version and note in commit message.

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

### Canonical Snapshot Artifact Naming (Pattern 12)

**Artifacts:** `{TICKER}_{ARTIFACT}_{STAGE}.{ext}`

Each artifact gets a stage suffix indicating when it was created or last modified.

| Stage | Suffix | Example |
|-------|--------|---------|
| BASE | `_BASE` | `DAVE_A5_GIM_BASE.json` |
| RQ | `_RQ` | `DAVE_A8_RESEARCH_PLAN_RQ.json` |
| ENRICH | `_ENRICH` | `DAVE_A7_VALUATION_ENRICH.json` |
| SCENARIO | `_SCEN` | `DAVE_A10_SCENARIO_SCEN.json` |
| SILICON COUNCIL | `_SC` | `DAVE_A11_AUDIT_SC.json` |
| INTEGRATION | `_INT` | `DAVE_A12_CASCADE_INT.json` |
| IRR | `_IRR` | `DAVE_A14_IRR_ANALYSIS_IRR.json` |

**Narratives:** `{TICKER}_{NARRATIVE}_{STAGE}.md`
- Example: `DAVE_N1_THESIS_BASE.md`, `DAVE_N5_ENRICHMENT_ENRICH.md`

**Human Audit Files:** `{TICKER}_{STAGE}_AUDIT.md` (NOT machine input)
- Example: `DAVE_BASE_T1_AUDIT.md`

**Kernel Receipts:** `{TICKER}_KERNEL_RECEIPT_{STAGE}.json`
- Example: `DAVE_KERNEL_RECEIPT_BASE.json`

---

## Current Versions

### Analysis Pipeline (Prompts + Kernels)

| Stage | Prompt | Status | Smoke Test | Kernel |
|-------|--------|--------|------------|--------|
| BASE | G3BASE_2.2.3e_*.md (atomized) | **EXPERIMENTAL** | Pending | BASE_CVR_KERNEL_2.2.3e.py |
| BASE | G3BASE_2.2.2e_*.md (atomized) | CANONICAL | DAVE_20241220 | BASE_CVR_KERNEL_2.2.2e.py |
| BASE | G3BASE_2.2.1e.md | HISTORICAL | DAVE_20241210 | BASE_CVR_KERNEL_2.2.1e.py |
| REFINE | BASE_T1_REFINE_v1_3.md | **EXPERIMENTAL** | Pending | - |
| REFINE | BASE_T1_REFINE_v1_2.md | CANONICAL | DAVE_20241220 | - |
| REFINE | BASE_T1_REFINE_v1_1.md | HISTORICAL | DAVE_20241210 | - |
| ENRICH | G3ENRICH_2.2.3e_*.md (atomized) | **EXPERIMENTAL** | Pending | CVR_KERNEL_ENRICH_2.2.3e.py |
| ENRICH | G3ENRICH_2.2.2e_*.md (atomized) | CANONICAL | DAVE_ENRICH_20241220 | CVR_KERNEL_ENRICH_2.2.2e.py |
| ENRICH | G3ENRICH_2.2.1e.md | HISTORICAL | DAVE_20241210 | CVR_KERNEL_ENRICH_2.2.1e.py |
| SCENARIO | G3_SCENARIO_2.2.2e_*.md (atomized) | CANONICAL | DAVE_ENRICH_SMOKE_20251220 | CVR_KERNEL_SCEN_2_2_2e.py |
| SCENARIO | G3_SCENARIO_2_2_1e.md | HISTORICAL | DAVE_20241210 | CVR_KERNEL_SCEN_2_2_1e.py |
| INTEGRATION | G3_INTEGRATION_2.2.3e_*.md (atomized) | CANONICAL | DAVE_ENRICH_SMOKE_20251220 | CVR_KERNEL_INT_2_2_2e.py |
| INTEGRATION | G3_INTEGRATION_2_2_2e.md | HISTORICAL | DAVE_20241210 | CVR_KERNEL_INT_2_2_2e.py |
| IRR | G3_IRR_2.2.5e_*.md (atomized) | CANONICAL | DAVE_ENRICH_SMOKE_20251220 | CVR_KERNEL_IRR_2.2.5e.py |
| IRR | G3_IRR_2_2_4e.md | HISTORICAL | DAVE_20241210 | CVR_KERNEL_IRR_2_2_4e.py |

### Orchestration & Workflow

| Component | File | Status | Smoke Test |
|-----------|------|--------|------------|
| SOURCE Stage | orchestration/SOURCE_STAGE.md | **EXPERIMENTAL** | Pending |
| BASE Stage | orchestration/BASE_STAGE.md | **EXPERIMENTAL** (updated for 2.2.3e) | Pending |
| ENRICH Stage | orchestration/ENRICH_STAGE.md | **EXPERIMENTAL** (updated for 2.2.3e) | Pending |
| Research Question Gen | RQ_Gen_2_2_3e.md | CANONICAL | DAVE_RQ_CLAUDE_TEST |
| Research Question Gen (legacy) | RQ_Gen_2_2_2e.md | HISTORICAL | - |
| RQ Executor | RQ_ASK_KERNEL_2_2_3e.py | CANONICAL | DAVE_RQ_CLAUDE_TEST |
| RQ Executor CLI | run_rq_ask.py | CANONICAL | DAVE_RQ_CLAUDE_TEST |
| Silicon Council | G3_SC_2.2.2e_*.md (atomized) | CANONICAL | DAVE_ENRICH_SMOKE_20251220 |
| Silicon Council | G3_SILICON_COUNCIL_2.2.1e.md | HISTORICAL | DAVE_20241210 |
| HITL Audit | HITL_DIALECTIC_AUDIT_1_0_Goldilocks.md | CANONICAL | DAVE_20241210 |
| PDF Preprocessing | SOURCE: UPLOAD (workshop/CLAUDE.md) | **EXPERIMENTAL** | Pending |

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
| INT T1 Validator | INT_T1_VALIDATOR.md | CANONICAL | DAVE_ENRICH_SMOKE_20251220 |
| INT T2 Validator | INT_T2_VALIDATOR.md | CANONICAL | DAVE_ENRICH_SMOKE_20251220 |
| INT T3 Validator | INT_T3_VALIDATOR.md | CANONICAL | DAVE_ENRICH_SMOKE_20251220 |
| IRR T1 Validator | IRR_T1_VALIDATOR.md | CANONICAL | DAVE_ENRICH_SMOKE_20251220 |
| IRR T2 Validator | IRR_T2_VALIDATOR.md | CANONICAL | DAVE_ENRICH_SMOKE_20251220 |

---

