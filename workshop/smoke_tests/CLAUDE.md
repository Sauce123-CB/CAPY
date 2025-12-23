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

> **Generated:** 2025-12-23T12:45:55-05:00


---

# Stage: SOURCE

# SOURCE Stage Orchestration

> **Version:** 1.1.0
> **Pipeline Position:** Stage 0 of 9 (PDF → SOURCE → BASE)
> **Created:** 2024-12-23
> **Updated:** 2024-12-23 - Added table detection, image placeholders, VISUAL_MANIFEST

## SOURCE Stage Overview

The SOURCE stage handles PDF preprocessing - converting raw PDF documents into machine-readable text and images for analysis. This includes:
- **Text extraction** with table detection
- **Image placeholders** noting where charts/figures appear
- **Page images** for runtime vision analysis via VISUAL_MANIFEST

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SOURCE STAGE (Stage 0 - Preprocessing)                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INPUT: Raw PDF files dropped into repository                               │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STEP 1: SCAN FOR PDFS                                                │   │
│  │                                                                       │   │
│  │   Check source_library/{TICKER}/ for:                                │   │
│  │   - *.pdf files                                                       │   │
│  │   - Missing *.extracted.md files (need preprocessing)                 │   │
│  │                                                                       │   │
│  │   If no PDFs found → ABORT with message                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STEP 2: TEXT + TABLE EXTRACTION (pdfplumber)                         │   │
│  │                                                                       │   │
│  │   For each PDF without .extracted.md:                                │   │
│  │   - Open with pdfplumber                                             │   │
│  │   - Extract text from each page                                      │   │
│  │   - Detect and format TABLES as markdown tables                      │   │
│  │   - Note IMAGE POSITIONS as placeholders                             │   │
│  │   - Write to {filename}.extracted.md                                 │   │
│  │                                                                       │   │
│  │   Format:                                                             │   │
│  │   # {filename}                                                        │   │
│  │   *Extracted from: {filename}.pdf*                                   │   │
│  │   ## Page 1 of N                                                      │   │
│  │   {page text}                                                         │   │
│  │   ### Table 1 (Page 1)                                                │   │
│  │   | Col1 | Col2 | ...                                                 │   │
│  │   *[Image detected: page_1_img_1.png - position: x=..., y=...]*      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STEP 3: IMAGE EXTRACTION + VISUAL_MANIFEST (pdf2image)               │   │
│  │                                                                       │   │
│  │   For each PDF without _pages/ directory:                            │   │
│  │   - Convert pages to PNG at 150 DPI                                  │   │
│  │   - Save to {filename}_pages/page_001.png, page_002.png, ...         │   │
│  │   - Create VISUAL_MANIFEST.md with instructions for runtime vision   │   │
│  │                                                                       │   │
│  │   VISUAL_MANIFEST.md tells Claude which images to read at runtime    │   │
│  │   for charts, graphs, and visual data that pdfplumber can't extract  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STEP 4: GENERATE INVENTORY                                           │   │
│  │                                                                       │   │
│  │   Create/update source_library/{TICKER}/INVENTORY.md:                │   │
│  │                                                                       │   │
│  │   | PDF | Extracted Text | Page Images | Pages | Status |            │   │
│  │   |-----|----------------|-------------|-------|--------|            │   │
│  │   | 10K.pdf | 10K.extracted.md | 10K_pages/ | 245 | OK |             │   │
│  │                                                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  OUTPUT:                                                                    │
│  source_library/{TICKER}/                                                   │
│  ├── {filename}.pdf                    ← Original PDF (unchanged)          │
│  ├── {filename}.extracted.md           ← Text + tables + image placeholders│
│  ├── {filename}_pages/                 ← Page images for vision analysis   │
│  │   ├── page_001.png                                                      │
│  │   ├── page_002.png                                                      │
│  │   ├── ...                                                               │
│  │   └── VISUAL_MANIFEST.md            ← Instructions for runtime vision  │
│  └── INVENTORY.md                      ← Document manifest                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Dependencies

**System:**
```bash
brew install poppler    # Provides pdftoppm, pdftotext
```

**Python:**
```bash
pip3 install pdfplumber pdf2image pillow
```

**Verification:**
```bash
which pdftoppm          # Should return path (e.g., /opt/homebrew/bin/pdftoppm)
python3 -c "import pdfplumber; print('pdfplumber OK')"
python3 -c "from pdf2image import convert_from_path; print('pdf2image OK')"
```

## Trigger Command

```
SOURCE: UPLOAD {TICKER}
```

**Example:**
```
SOURCE: UPLOAD NVDA
```

## Implementation Code (MANDATORY - COPY VERBATIM)

**⚠️ COPY AND PASTE THIS EXACT SCRIPT. DO NOT WRITE YOUR OWN VERSION.**

Replace `{TICKER}` with actual ticker and run via `python3 << 'EOF' ... EOF`:

```python
import pdfplumber
from pdf2image import convert_from_path
from pathlib import Path
from datetime import datetime

TICKER = "{TICKER}"  # <-- REPLACE THIS
SOURCE_DIR = Path(f"source_library/{TICKER}")

def format_table(table):
    """Convert pdfplumber table to markdown format."""
    if not table or len(table) == 0:
        return ""

    # Clean cells
    def clean_cell(cell):
        if cell is None:
            return ""
        return str(cell).replace("\n", " ").strip()

    rows = [[clean_cell(cell) for cell in row] for row in table]
    if not rows:
        return ""

    # Build markdown table
    header = "| " + " | ".join(rows[0]) + " |"
    separator = "| " + " | ".join(["---"] * len(rows[0])) + " |"
    body = "\n".join("| " + " | ".join(row) + " |" for row in rows[1:])

    return f"{header}\n{separator}\n{body}"

def extract_page_content(page, page_num, total_pages):
    """Extract text, tables, and image positions from a page."""
    parts = [f"## Page {page_num} of {total_pages}\n"]

    # Extract text
    text = page.extract_text() or ""
    if text.strip():
        parts.append(text)

    # Extract tables
    tables = page.extract_tables()
    for i, table in enumerate(tables, 1):
        md_table = format_table(table)
        if md_table:
            parts.append(f"\n### Table {i} (Page {page_num})\n\n{md_table}")

    # Note image positions
    if hasattr(page, 'images') and page.images:
        for i, img in enumerate(page.images, 1):
            x, y = img.get('x0', 0), img.get('top', 0)
            parts.append(f"\n*[Image detected: page_{page_num}_img_{i}.png - position: x={x}, y={y}]*")

    return "\n\n".join(parts)

def create_visual_manifest(img_dir, pdf_name, page_count):
    """Create VISUAL_MANIFEST.md for runtime vision analysis."""
    manifest_parts = ["# Visual Analysis Manifest\n"]
    manifest_parts.append("Pages extracted for visual analysis. Use Read tool on each image.\n")
    manifest_parts.append("---\n")

    # Sample key pages (first 10, then every 5th)
    key_pages = list(range(1, min(11, page_count + 1)))
    key_pages += list(range(15, page_count + 1, 5))
    key_pages = sorted(set(key_pages))

    for p in key_pages:
        img_file = f"page_{p:03d}.png"
        manifest_parts.append(f"""
## {pdf_name}_page_{p:03d}.png

**Path:** `{img_dir.name}/{img_file}`

**Action:** Read this image and extract:

- All numerical values (revenue, margins, growth rates, etc.)

- Chart data points and trends

- Table contents

- Key metrics and KPIs
""")

    manifest_path = img_dir / "VISUAL_MANIFEST.md"
    manifest_path.write_text("\n".join(manifest_parts))
    return manifest_path

def preprocess_pdf(pdf_path):
    """Full preprocessing: text+tables, image placeholders, page images, manifest."""
    print(f"Processing: {pdf_path.name}")

    # === TEXT + TABLE EXTRACTION (pdfplumber) ===
    content_parts = [f"# {pdf_path.stem}\n"]
    content_parts.append(f"*Extracted from: {pdf_path.name}*\n")
    content_parts.append("---\n")

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages, 1):
            page_content = extract_page_content(page, i, total_pages)
            content_parts.append(page_content)

    md_path = pdf_path.with_suffix(".extracted.md")
    md_path.write_text("\n\n".join(content_parts))
    print(f"  → Text+Tables: {md_path.name}")

    # === IMAGE EXTRACTION (pdf2image) ===
    img_dir = pdf_path.parent / f"{pdf_path.stem}_pages"
    img_dir.mkdir(parents=True, exist_ok=True)
    images = convert_from_path(pdf_path, dpi=150)
    for i, img in enumerate(images, 1):
        img.save(img_dir / f"page_{i:03d}.png", "PNG")
    print(f"  → Images: {img_dir.name}/ ({len(images)} pages)")

    # === VISUAL MANIFEST ===
    manifest_path = create_visual_manifest(img_dir, pdf_path.stem, len(images))
    print(f"  → Manifest: {manifest_path.name}")

    return len(images)

# Process all PDFs
for pdf_path in sorted(SOURCE_DIR.glob("*.pdf")):
    if not pdf_path.with_suffix(".extracted.md").exists():
        preprocess_pdf(pdf_path)
    else:
        print(f"Skipping (already extracted): {pdf_path.name}")

print(f"\nDone. Verify .extracted.md, _pages/ folders, and VISUAL_MANIFEST.md exist.")
```

**Verification after running:**
```bash
ls source_library/{TICKER}/*.extracted.md           # Text files with tables
ls -d source_library/{TICKER}/*_pages/              # Image folders
ls source_library/{TICKER}/*_pages/VISUAL_MANIFEST.md  # Manifests for vision
```

**If `_pages/` folders or VISUAL_MANIFEST.md are missing, preprocessing FAILED.**

## Integration with Pipeline

The SOURCE stage is automatically invoked by `CAPY: RUN {TICKER}` as Stage 0:

1. **Check:** Does `source_library/{TICKER}/` exist with `*.extracted.md` files?
2. **If missing:** Run SOURCE: UPLOAD automatically
3. **If present:** Skip to Stage 1 (INIT)

For manual runs or debugging, run `SOURCE: UPLOAD {TICKER}` explicitly.

## Shared Storage

Source documents are stored in `../production/source_library/` - shared between workshop and production contexts. This avoids duplicate preprocessing and ensures consistency.

## Error Handling

| Error | Response |
|-------|----------|
| No PDFs found | Abort with message, prompt user to add PDFs |
| pdfplumber fails | Log error, flag in INVENTORY.md, continue with others |
| pdf2image fails | Log error, flag in INVENTORY.md (may need poppler) |
| Permission denied | Check file permissions, may need chmod |

## Validation

After SOURCE: UPLOAD completes, verify:

```bash
# Check extracted files exist
ls source_library/{TICKER}/*.extracted.md

# Check page counts match
wc -l source_library/{TICKER}/*.extracted.md

# Verify INVENTORY.md
cat source_library/{TICKER}/INVENTORY.md
```


---

# Stage: BASE

# BASE Stage Orchestration

> **Version:** 1.0.0
> **Extracted from:** workshop/CLAUDE.md v0.12.1
> **Pipeline Position:** Stage 1 of 8 (SOURCE → BASE)

---

## BASE Stage Orchestration (SOURCE → BASE)

The BASE stage transforms raw source documents (10-Ks, 10-Qs, transcripts, presentations) into State 1: the foundational Company Valuation Report with epistemic anchors, causal structure, financial model, and initial valuation.

### Architecture (v2.2.3e - EXPERIMENTAL)

**Three-Shot Execution:**

| Turn | Name | Purpose | Key Output |
|------|------|---------|------------|
| T1 | Analytical | Extract facts, build causal structure, draft model | A.1-A.6, N1-N4 (embedded in T1.md) |
| REFINE | Calibration | Y0 calibration, DAG validation, equity bridge check | Refined A.1-A.6 (standalone JSON) |
| T2 | Computational | Kernel execution via Bash (Pattern 6) | A.7 + T2.md |

**Key Design Decisions:**
- **Three-shot not two-shot:** REFINE is interposed to calibrate model before kernel
- **Pattern 2 (Source Chain):** REFINE is source of truth for A.1-A.6, not T1
- **Equity Bridge preservation:** REFINE must preserve FDSO, Total_Debt, Excess_Cash, Minority_Interest
- **No WebSearch in BASE:** Market price fetched later in IRR stage

### Directory Structure

**Canonical Snapshot (Pattern 12):** After BASE T2, 03_T2/ contains complete State 1 artifacts.

```
{analysis_dir}/
├── 00_source/                               ← Input: preprocessed source docs
│   ├── {TICKER}_10K_2024.extracted.md
│   ├── {TICKER}_10Q_Q3_2024.extracted.md
│   ├── {TICKER}_earnings_call_Q3.extracted.md
│   └── {TICKER}_investor_deck.extracted.md
│
├── 01_T1/                                   ← BASE T1 outputs
│   ├── {TICKER}_BASE_T1_AUDIT.md                (T1 narrative - human audit only)
│   └── (artifacts embedded in T1.md, extracted by REFINE)
│
├── 02_REFINE/                               ← REFINE outputs (SOURCE OF TRUTH)
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_BASE.json  (refined)
│   ├── {TICKER}_A2_ANALYTIC_KG_BASE.json        (refined)
│   ├── {TICKER}_A3_CAUSAL_DAG_BASE.json         (refined, ≤15 nodes)
│   ├── {TICKER}_A5_GIM_BASE.json                (refined, Y0 calibrated)
│   ├── {TICKER}_A6_DR_BASE.json                 (refined)
│   ├── {TICKER}_N1_THESIS_BASE.md               (refined)
│   ├── {TICKER}_N2_IC_BASE.md                   (refined)
│   ├── {TICKER}_N3_ECON_GOV_BASE.md             (refined)
│   ├── {TICKER}_N4_RISK_BASE.md                 (refined)
│   └── {TICKER}_REFINE_AUDIT.md                 (calibration log - human audit)
│
├── 03_T2/                                   ← BASE T2 outputs (canonical State 1)
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_BASE.json  (COPIED from REFINE)
│   ├── {TICKER}_A2_ANALYTIC_KG_BASE.json        (COPIED from REFINE)
│   ├── {TICKER}_A3_CAUSAL_DAG_BASE.json         (COPIED from REFINE)
│   ├── {TICKER}_A5_GIM_BASE.json                (COPIED from REFINE)
│   ├── {TICKER}_A6_DR_BASE.json                 (COPIED from REFINE)
│   ├── {TICKER}_A7_VALUATION_BASE.json          (NEW - T2 kernel output)
│   ├── {TICKER}_N1_THESIS_BASE.md               (COPIED from REFINE)
│   ├── {TICKER}_N2_IC_BASE.md                   (COPIED from REFINE)
│   ├── {TICKER}_N3_ECON_GOV_BASE.md             (COPIED from REFINE)
│   ├── {TICKER}_N4_RISK_BASE.md                 (COPIED from REFINE)
│   ├── {TICKER}_KERNEL_RECEIPT_BASE.json        (NEW - Pattern 13)
│   └── {TICKER}_BASE_T2_AUDIT.md                (human audit only)
│
└── pipeline_state.json
```

**Copy-Forward Protocol (Orchestrator executes BEFORE RQ stage):**
```bash
mkdir -p {analysis_dir}/04_RQ

# Copy all BASE artifacts from 03_T2/ with suffix rename
for f in {analysis_dir}/03_T2/{TICKER}_*_BASE.json; do
  base=$(basename "$f" | sed 's/_BASE\.json$//')
  cp "$f" "{analysis_dir}/04_RQ/${base}_RQ.json"
done

for f in {analysis_dir}/03_T2/{TICKER}_*_BASE.md; do
  base=$(basename "$f" | sed 's/_BASE\.md$//')
  cp "$f" "{analysis_dir}/04_RQ/${base}_RQ.md"
done
```

### Stage Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 0: SOURCE VALIDATION                                                   │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Verify source documents exist and are preprocessed                    │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ Check source_library/{TICKER}/ for:                                         │
│   - *.extracted.md files (preprocessed PDFs)                                │
│   - If missing: run SOURCE: UPLOAD {TICKER} first                           │
│                                                                             │
│ Create analysis folder:                                                     │
│   mkdir -p smoke_tests/{TICKER}_SMOKE_{TIMESTAMP}/00_source                 │
│   cp source_library/{TICKER}/*.extracted.md 00_source/                      │
│                                                                             │
│ Set {analysis_dir} to the new folder.                                       │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: BASE T1 — ANALYTICAL                                                │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to extract facts and build initial model          │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/base/G3BASE_2.2.3e_PROMPT.md                                   │
│   2. prompts/base/G3BASE_2.2.3e_SCHEMAS.md                                  │
│   3. prompts/base/G3BASE_2.2.3e_NORMDEFS.md                                 │
│   4. kernels/BASE_CVR_KERNEL_2.2.3e.py (FOR CONTEXT ONLY - DO NOT EXECUTE)  │
│                                                                             │
│ INPUT FILES TO ATTACH:                                                      │
│   • All files from {analysis_dir}/00_source/*.extracted.md                  │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute BASE Turn 1 for {TICKER}.                                        │
│                                                                             │
│    Your analytical tasks:                                                   │
│    1. Extract epistemic anchors from source documents (A.1)                 │
│    2. Build Analytic Knowledge Graph with causal relationships (A.2)        │
│    3. Construct Causal DAG with ≤15 nodes (A.3)                             │
│    4. Build Gestalt Impact Map (GIM) with 5-year forecast (A.5)             │
│    5. Derive Discount Rate using B.3 rubric (A.6)                           │
│    6. Write narratives N1-N4 (Thesis, IC, Economic Governor, Risk)          │
│                                                                             │
│    DO NOT execute the kernel. It is provided for context only.              │
│                                                                             │
│    Write output to {analysis_dir}/01_T1/:                                   │
│    1. {TICKER}_BASE_T1_AUDIT.md (full reasoning + embedded artifacts)       │
│                                                                             │
│    Return confirmation and filepath written."                               │
│                                                                             │
│ OUTPUT PRODUCED:                                                            │
│   • {TICKER}_BASE_T1_AUDIT.md - Complete T1 output with embedded artifacts  │
│                                                                             │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns path   │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: BASE T1 VALIDATOR                                                   │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate T1 output                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/BASE_T1_VALIDATOR.md                                           │
│                                                                             │
│ INPUT FILES:                                                                │
│   • {analysis_dir}/01_T1/{TICKER}_BASE_T1_AUDIT.md                          │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • A.1-A.6 present and extractable                                         │
│   • A.3 DAG has ≤15 nodes                                                   │
│   • A.5 GIM has 5-year forecast with required rows                          │
│   • A.6 DR in reasonable range (8-18% typically)                            │
│   • N1-N4 narratives present                                                │
│   • Equity Bridge items present (FDSO, Total_Debt, Excess_Cash)             │
│                                                                             │
│ IF FAIL: Stop. Report issues. Do not proceed to REFINE.                     │
│ IF PASS: Proceed to Step 3.                                                 │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │ (proceed only if PASS)
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: BASE REFINE — CALIBRATION                                           │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to calibrate model and extract standalone JSONs   │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE TO ATTACH:                                                      │
│   prompts/refine/BASE_T1_REFINE_v1_3.md                                     │
│                                                                             │
│ INPUT FILES TO ATTACH:                                                      │
│   • {analysis_dir}/01_T1/{TICKER}_BASE_T1_AUDIT.md                          │
│   • {analysis_dir}/00_source/*.extracted.md (for Y0 verification)           │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute BASE REFINE for {TICKER}.                                        │
│                                                                             │
│    CRITICAL: REFINE is the SOURCE OF TRUTH for A.1-A.6 (Pattern 2).         │
│    T1 artifacts are drafts; REFINE outputs are canonical.                   │
│                                                                             │
│    Your calibration tasks:                                                  │
│    1. Extract A.1-A.6 from T1 into standalone JSON files                    │
│    2. Y0 Calibration: Verify model Y0 matches reported financials (±2%)     │
│    3. DAG Validation: Ensure ≤15 nodes, no orphans, coherent structure      │
│    4. Equity Bridge Check: Preserve FDSO, Total_Debt, Excess_Cash,          │
│       Minority_Interest unchanged from T1                                   │
│    5. Extract N1-N4 narratives into standalone markdown files               │
│                                                                             │
│    Write ALL output files to {analysis_dir}/02_REFINE/:                     │
│    1. {TICKER}_A1_EPISTEMIC_ANCHORS_BASE.json                               │
│    2. {TICKER}_A2_ANALYTIC_KG_BASE.json                                     │
│    3. {TICKER}_A3_CAUSAL_DAG_BASE.json                                      │
│    4. {TICKER}_A5_GIM_BASE.json                                             │
│    5. {TICKER}_A6_DR_BASE.json                                              │
│    6. {TICKER}_N1_THESIS_BASE.md                                            │
│    7. {TICKER}_N2_IC_BASE.md                                                │
│    8. {TICKER}_N3_ECON_GOV_BASE.md                                          │
│    9. {TICKER}_N4_RISK_BASE.md                                              │
│   10. {TICKER}_REFINE_AUDIT.md (calibration log)                            │
│                                                                             │
│    Return confirmation and list of filepaths written."                      │
│                                                                             │
│ OUTPUT PRODUCED (10 files):                                                 │
│   • {TICKER}_A1-A6_BASE.json - Standalone refined artifacts                 │
│   • {TICKER}_N1-N4_BASE.md - Standalone refined narratives                  │
│   • {TICKER}_REFINE_AUDIT.md - Calibration log (human audit)                │
│                                                                             │
│ PATTERN: Source Chain (Pattern 2) - REFINE outputs are source of truth      │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns paths  │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: BASE REFINE VALIDATOR                                               │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate REFINE output                         │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/BASE_REFINE_VALIDATOR.md                                       │
│                                                                             │
│ INPUT FILES (verify ALL 10 exist in 02_REFINE/):                            │
│   {analysis_dir}/02_REFINE/{TICKER}_A1_EPISTEMIC_ANCHORS_BASE.json          │
│   {analysis_dir}/02_REFINE/{TICKER}_A2_ANALYTIC_KG_BASE.json                │
│   {analysis_dir}/02_REFINE/{TICKER}_A3_CAUSAL_DAG_BASE.json                 │
│   {analysis_dir}/02_REFINE/{TICKER}_A5_GIM_BASE.json                        │
│   {analysis_dir}/02_REFINE/{TICKER}_A6_DR_BASE.json                         │
│   {analysis_dir}/02_REFINE/{TICKER}_N1_THESIS_BASE.md                       │
│   {analysis_dir}/02_REFINE/{TICKER}_N2_IC_BASE.md                           │
│   {analysis_dir}/02_REFINE/{TICKER}_N3_ECON_GOV_BASE.md                     │
│   {analysis_dir}/02_REFINE/{TICKER}_N4_RISK_BASE.md                         │
│   {analysis_dir}/02_REFINE/{TICKER}_REFINE_AUDIT.md                         │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • ALL 10 REFINE OUTPUT FILES EXIST (block T2 if any missing)              │
│   • Y0 calibration within ±2% for Revenue, EBIT, IC                         │
│   • DAG has ≤15 nodes                                                       │
│   • Equity Bridge preserved: FDSO, Total_Debt, Excess_Cash, Minority_Int    │
│   • JSON files are valid and contain required fields                        │
│                                                                             │
│ IF FAIL: Stop. Report issues. Do not proceed to T2.                         │
│ IF PASS: Proceed to Step 5.                                                 │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │ (proceed only if PASS)
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 5: BASE T2 — COMPUTATIONAL (KERNEL EXECUTION)                          │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to execute kernel and produce A.7                 │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/base/G3BASE_2.2.3e_PROMPT.md (T2 section only)                 │
│   2. kernels/BASE_CVR_KERNEL_2.2.3e.py (EXECUTABLE)                         │
│                                                                             │
│ INPUT FILES TO ATTACH (from 02_REFINE/):                                    │
│   • {analysis_dir}/02_REFINE/{TICKER}_A5_GIM_BASE.json                      │
│   • {analysis_dir}/02_REFINE/{TICKER}_A6_DR_BASE.json                       │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute BASE Turn 2 for {TICKER}.                                        │
│                                                                             │
│    CRITICAL: Manual calculation is PROHIBITED. You MUST use Bash kernel.    │
│    CRITICAL: T2 performs NO reasoning. All judgment is locked in REFINE.    │
│                                                                             │
│    1. Validate A.5 and A.6 are well-formed (repair if needed - Pattern 5)   │
│    2. Execute kernel via Bash (Pattern 6):                                  │
│                                                                             │
│       python3 kernels/BASE_CVR_KERNEL_2.2.3e.py \                           │
│         --a5 {TICKER}_A5_GIM_BASE.json \                                    │
│         --a6 {TICKER}_A6_DR_BASE.json \                                     │
│         --output {TICKER}_A7_VALUATION_BASE.json                            │
│                                                                             │
│    3. Generate kernel receipt (Pattern 13):                                 │
│       Write {TICKER}_KERNEL_RECEIPT_BASE.json with:                         │
│       - kernel file, version, sha256                                        │
│       - input filenames                                                     │
│       - command executed                                                    │
│       - exit_code, execution_time_seconds                                   │
│                                                                             │
│    4. Copy REFINE artifacts to 03_T2/ with _BASE suffix (already there)     │
│                                                                             │
│    Write output files to {analysis_dir}/03_T2/:                             │
│    1. {TICKER}_A7_VALUATION_BASE.json (kernel output)                       │
│    2. {TICKER}_KERNEL_RECEIPT_BASE.json (execution proof)                   │
│    3. {TICKER}_BASE_T2_AUDIT.md (human audit only)                          │
│    + Copy A.1-A.6, N1-N4 from 02_REFINE/ to 03_T2/                          │
│                                                                             │
│    Return confirmation and filepaths."                                      │
│                                                                             │
│ OUTPUT PRODUCED:                                                            │
│   • {TICKER}_A7_VALUATION_BASE.json - Kernel output (E[IVPS], terminal g)   │
│   • {TICKER}_KERNEL_RECEIPT_BASE.json - Execution proof (Pattern 13)        │
│   • {TICKER}_BASE_T2_AUDIT.md - Human audit only                            │
│   • All REFINE artifacts copied to 03_T2/ (canonical State 1 snapshot)      │
│                                                                             │
│ PATTERN: Bash Kernel (Pattern 6) - execute kernel via Bash, not manual calc │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns paths  │
│ PATTERN: Kernel Receipts (Pattern 13) - verifiable proof of execution       │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 6: BASE T2 VALIDATOR                                                   │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate T2 output                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/BASE_T2_VALIDATOR.md                                           │
│                                                                             │
│ INPUT FILES:                                                                │
│   • {analysis_dir}/03_T2/{TICKER}_A7_VALUATION_BASE.json                    │
│   • {analysis_dir}/03_T2/{TICKER}_KERNEL_RECEIPT_BASE.json                  │
│   • {analysis_dir}/03_T2/{TICKER}_A5_GIM_BASE.json (cross-validate)         │
│   • {analysis_dir}/03_T2/{TICKER}_A6_DR_BASE.json (cross-validate)          │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • A.7 schema compliance                                                   │
│   • Kernel receipt exists (Pattern 13: exit_code=0, timing present)         │
│   • Values have 4+ decimal precision (proves real execution)                │
│   • E[IVPS] is positive and economically sensible                           │
│   • Terminal g < DR (perpetuity validity)                                   │
│   • All 10 artifacts (A.1-A.7, N1-N4) present in 03_T2/                     │
│                                                                             │
│ IF FAIL: Report issues. May need T2 re-execution.                           │
│ IF PASS: BASE stage complete. CVR is now State 1.                           │
│          Proceed to RQ stage with copy-forward to 04_RQ/.                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Execution Commands (DEV: SMOKE TEST BASE {TICKER})

**Step 0: Validate Source Documents**
```bash
# Check source docs exist
ls source_library/{TICKER}/

# Create analysis folder
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p smoke_tests/{TICKER}_SMOKE_${TIMESTAMP}/00_source
cp source_library/{TICKER}/*.extracted.md smoke_tests/{TICKER}_SMOKE_${TIMESTAMP}/00_source/

# Set analysis_dir
export ANALYSIS_DIR="smoke_tests/{TICKER}_SMOKE_${TIMESTAMP}"
```

**Steps 1-6: Spawn Subagents**
Use Task tool with model="opus" for each step. See Stage Flow above for exact prompts and inputs.

### Critical Patterns Applied

| Pattern | Application |
|---------|-------------|
| Pattern 1: Direct-Write | All subagents write to disk, return filepath only |
| Pattern 2: Source Chain | REFINE is source of truth for A.1-A.6, not T1 |
| Pattern 3: Two-Shot (Extended) | T1=analytical, REFINE=calibration, T2=kernel |
| Pattern 5: JSON Repair | T2 can repair malformed REFINE JSON before kernel |
| Pattern 6: Bash Kernel | T2 executes BASE_CVR_KERNEL via Bash |
| Pattern 7: Validators | Opus validator after T1, REFINE, AND T2 |
| Pattern 8: Atomized Prompts | 3 files (PROMPT/SCHEMAS/NORMDEFS) + kernel |
| Pattern 12: Canonical Snapshot | 03_T2/ contains complete State 1 with _BASE suffix |
| Pattern 13: Kernel Receipts | T2 generates {TICKER}_KERNEL_RECEIPT_BASE.json |

### BASE Stage Atomized Files (EXPERIMENTAL)

The BASE prompt v2.2.3e is split into 3 atomic files for improved context management:

| File | Purpose | Size | Changes in 2.2.3e |
|------|---------|------|-------------------|
| `G3BASE_2.2.3e_PROMPT.md` | Core instructions (Sections I-V) | ~18KB | Currency detection, kernel receipts |
| `G3BASE_2.2.3e_SCHEMAS.md` | JSON schemas (Appendix A) | ~10KB | ROIC_anchor, currency fields |
| `G3BASE_2.2.3e_NORMDEFS.md` | DSL definitions (Appendix B) | ~6KB | DR global calibration |
| `BASE_CVR_KERNEL_2.2.3e.py` | Valuation kernel | ~33KB | Terminal g from topline growth |

**Status:** EXPERIMENTAL - pending smoke test. G3BASE_2.2.2e remains CANONICAL until smoke test passes.

**Subagent loading:** Load all 3 prompt files + kernel reference. The embedded kernel (old Appendix C) has been removed.

---



---

# Stage: RQ

# RQ Stage Orchestration

> **Version:** 1.0.0
> **Extracted from:** workshop/CLAUDE.md v0.12.1
> **Pipeline Position:** Stage 2 of 8 (BASE → RQ)

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
{analysis_dir}/
├── 03_T2/                           ← Input: BASE artifacts
├── 04_RQ/                           ← RQ stage outputs
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_RQ.json   (copied from BASE)
│   ├── {TICKER}_A2_ANALYTIC_KG_RQ.json         (copied from BASE)
│   ├── {TICKER}_A3_CAUSAL_DAG_RQ.json          (copied from BASE)
│   ├── {TICKER}_A5_GIM_RQ.json                 (copied from BASE)
│   ├── {TICKER}_A6_DR_RQ.json                  (copied from BASE)
│   ├── {TICKER}_A7_VALUATION_RQ.json           (copied from BASE)
│   ├── {TICKER}_A8_RESEARCH_PLAN_RQ.json       (NEW - RQ_GEN output)
│   ├── {TICKER}_A9_RESEARCH_RESULTS_RQ.json    (NEW - RQ_ASK summary)
│   ├── {TICKER}_RQ1_INTEGRITY_RQ.md            (NEW - M-1)
│   ├── {TICKER}_RQ2_ADVERSARIAL_RQ.md          (NEW - M-2)
│   ├── {TICKER}_RQ3_MAINLINE_SCENARIOS_RQ.md   (NEW - M-3a)
│   ├── {TICKER}_RQ4_TAIL_SCENARIOS_RQ.md       (NEW - M-3b)
│   ├── {TICKER}_RQ5_DYNAMIC1_RQ.md             (NEW - D-1)
│   ├── {TICKER}_RQ6_DYNAMIC2_RQ.md             (NEW - D-2)
│   └── {TICKER}_RQ7_DYNAMIC3_RQ.md             (NEW - D-3)
├── 05_ENRICH/                       ← Next stage
└── PIPELINE_STATE.md
```

**Copy-Forward Protocol:** Before RQ_GEN, orchestrator copies BASE artifacts from 03_T2/ to 04_RQ/ with suffix rename (_BASE → _RQ) using `cp`.

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



---

# Stage: ENRICH

# ENRICH Stage Orchestration

> **Version:** 1.0.0
> **Extracted from:** workshop/CLAUDE.md v0.12.1
> **Pipeline Position:** Stage 4 of 8 (RQ → ENRICH)

---

## ENRICH Stage Orchestration (RQ → ENRICH)

The ENRICH stage integrates research findings from the RQ stage into the CVR, transitioning from State 1 (BASE output) to State 2. Research insights modify the Analytic KG, Causal DAG, GIM assumptions, and DR factors. The kernel then recalculates valuation with enriched inputs.

### Architecture (v2.2.3e - EXPERIMENTAL)

**Two-Shot Execution:**

| Turn | Name | Purpose | Key Output |
|------|------|---------|------------|
| T1 | Synthesis | Integrate RQ findings into artifacts, identify changes | Modified A.2, A.3, A.5, A.6 + A.9_ENRICHMENT_TRACE |
| T2 | Computational | Kernel execution via Bash (Pattern 6) | A.7 (recalculated) + N5 |

**Key Design Decisions:**
- **Two-shot not three-shot:** No REFINE interposed - RQ findings are already validated
- **Selective modification:** Only artifacts affected by RQ findings are modified
- **Enrichment trace (A.9):** Documents how each RQ finding maps to artifact changes
- **N5 narrative:** New narrative synthesizing research insights

### Directory Structure

**Canonical Snapshot (Pattern 12):** 05_ENRICH/ contains complete State 2 artifacts.

```
{analysis_dir}/
├── 04_RQ/                                   ← Input: RQ outputs with _RQ suffix
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_RQ.json    (copied from BASE)
│   ├── {TICKER}_A2_ANALYTIC_KG_RQ.json          (copied from BASE)
│   ├── {TICKER}_A3_CAUSAL_DAG_RQ.json           (copied from BASE)
│   ├── {TICKER}_A5_GIM_RQ.json                  (copied from BASE)
│   ├── {TICKER}_A6_DR_RQ.json                   (copied from BASE)
│   ├── {TICKER}_A7_VALUATION_RQ.json            (copied from BASE)
│   ├── {TICKER}_N1-N4_*_RQ.md                   (copied from BASE, 4 files)
│   ├── {TICKER}_A8_RESEARCH_PLAN_RQ.json        (NEW - RQ_GEN output)
│   ├── {TICKER}_A9_RESEARCH_RESULTS_RQ.json     (NEW - RQ_ASK summary)
│   └── {TICKER}_RQ1-RQ7_*_RQ.md                 (NEW - research outputs, 7 files)
│
├── 05_ENRICH/                               ← ENRICH stage outputs (canonical State 2)
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_ENRICH.json    (COPIED from RQ - unchanged)
│   ├── {TICKER}_A2_ANALYTIC_KG_ENRICH.json          (MODIFIED - new nodes from RQ)
│   ├── {TICKER}_A3_CAUSAL_DAG_ENRICH.json           (MODIFIED - new edges if needed)
│   ├── {TICKER}_A5_GIM_ENRICH.json                  (MODIFIED - updated assumptions)
│   ├── {TICKER}_A6_DR_ENRICH.json                   (MODIFIED - adjusted risk factors)
│   ├── {TICKER}_A7_VALUATION_ENRICH.json            (NEW - T2 kernel output)
│   ├── {TICKER}_A8_RESEARCH_PLAN_ENRICH.json        (COPIED from RQ)
│   ├── {TICKER}_A9_RESEARCH_RESULTS_ENRICH.json     (COPIED from RQ)
│   ├── {TICKER}_A9_ENRICHMENT_TRACE_ENRICH.json     (NEW - maps RQ→artifact changes)
│   ├── {TICKER}_N1_THESIS_ENRICH.md                 (COPIED from RQ - unchanged)
│   ├── {TICKER}_N2_IC_ENRICH.md                     (COPIED from RQ - unchanged)
│   ├── {TICKER}_N3_ECON_GOV_ENRICH.md               (COPIED from RQ - unchanged)
│   ├── {TICKER}_N4_RISK_ENRICH.md                   (COPIED from RQ - unchanged)
│   ├── {TICKER}_N5_ENRICHMENT_ENRICH.md             (NEW - research synthesis)
│   ├── {TICKER}_RQ1-RQ7_*_ENRICH.md                 (COPIED from RQ, 7 files)
│   ├── {TICKER}_KERNEL_RECEIPT_ENRICH.json          (NEW - Pattern 13)
│   ├── {TICKER}_ENRICH_T1_AUDIT.md                  (human audit only)
│   └── {TICKER}_ENRICH_T2_AUDIT.md                  (human audit only)
│
└── pipeline_state.json
```

**Copy-Forward Protocol (Orchestrator executes BEFORE ENRICH T1):**
```bash
mkdir -p {analysis_dir}/05_ENRICH

# Copy all RQ artifacts with suffix rename
for f in {analysis_dir}/04_RQ/{TICKER}_*_RQ.json; do
  base=$(basename "$f" | sed 's/_RQ\.json$//')
  cp "$f" "{analysis_dir}/05_ENRICH/${base}_ENRICH.json"
done

for f in {analysis_dir}/04_RQ/{TICKER}_*_RQ.md; do
  base=$(basename "$f" | sed 's/_RQ\.md$//')
  cp "$f" "{analysis_dir}/05_ENRICH/${base}_ENRICH.md"
done
```

### Stage Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 0: COPY-FORWARD AND INPUT VALIDATION                                   │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Orchestrator copies RQ artifacts, validates inputs                    │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ 1. Locate most recent complete RQ run:                                      │
│    find smoke_tests/ -path "*/04_RQ/*A9*.json" | sort -r | head -5          │
│                                                                             │
│ 2. Execute copy-forward (Pattern 12 - see bash script above)                │
│                                                                             │
│ 3. Verify all required input files exist in 05_ENRICH/:                     │
│    - {TICKER}_A1-A7_ENRICH.json (7 artifacts)                               │
│    - {TICKER}_A8_RESEARCH_PLAN_ENRICH.json                                  │
│    - {TICKER}_A9_RESEARCH_RESULTS_ENRICH.json                               │
│    - {TICKER}_RQ1-RQ7_*_ENRICH.md (7 research files)                        │
│                                                                             │
│ 4. READ A7 to extract baseline:                                             │
│    - E[IVPS] (State 1 value)                                                │
│    - DR (to verify changes)                                                 │
│                                                                             │
│ Set {analysis_dir} to the pipeline run folder.                              │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: ENRICH T1 — SYNTHESIS                                               │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to integrate RQ findings into artifacts           │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/enrich/G3ENRICH_2.2.3e_PROMPT.md                               │
│   2. prompts/enrich/G3ENRICH_2.2.3e_SCHEMAS.md                              │
│   3. prompts/enrich/G3ENRICH_2.2.3e_NORMDEFS.md                             │
│   4. kernels/CVR_KERNEL_ENRICH_2.2.3e.py (FOR CONTEXT ONLY - DO NOT EXECUTE)│
│                                                                             │
│ INPUT FILES TO ATTACH (from 05_ENRICH/):                                    │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A1-A7_ENRICH.json (7 artifacts)       │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A8_RESEARCH_PLAN_ENRICH.json          │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A9_RESEARCH_RESULTS_ENRICH.json       │
│   • {analysis_dir}/05_ENRICH/{TICKER}_RQ1-RQ7_*_ENRICH.md (7 research files)│
│   • {analysis_dir}/05_ENRICH/{TICKER}_N1-N4_*_ENRICH.md (4 narratives)      │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute ENRICH Turn 1 for {TICKER}.                                      │
│                                                                             │
│    Your synthesis tasks:                                                    │
│    1. For each RQ finding (RQ1-RQ7), identify artifact impact:              │
│       - Does it add new knowledge? → Update A.2 (Analytic KG)               │
│       - Does it change causal relationships? → Update A.3 (DAG)             │
│       - Does it change assumptions? → Update A.5 (GIM)                      │
│       - Does it change risk factors? → Update A.6 (DR)                      │
│    2. Document all changes in A.9_ENRICHMENT_TRACE:                         │
│       - RQ source, finding, artifact modified, field changed, rationale     │
│    3. If no changes needed for an artifact, copy unchanged                  │
│    4. Write N5 ENRICHMENT narrative synthesizing research insights          │
│                                                                             │
│    DO NOT execute the kernel. It is provided for context only.              │
│                                                                             │
│    Write output files to {analysis_dir}/05_ENRICH/:                         │
│    1. {TICKER}_A2_ANALYTIC_KG_ENRICH.json (modified if needed)              │
│    2. {TICKER}_A3_CAUSAL_DAG_ENRICH.json (modified if needed)               │
│    3. {TICKER}_A5_GIM_ENRICH.json (modified if needed)                      │
│    4. {TICKER}_A6_DR_ENRICH.json (modified if needed)                       │
│    5. {TICKER}_A9_ENRICHMENT_TRACE_ENRICH.json (NEW - required)             │
│    6. {TICKER}_N5_ENRICHMENT_ENRICH.md (NEW - required)                     │
│    7. {TICKER}_ENRICH_T1_AUDIT.md (reasoning log - human audit only)        │
│                                                                             │
│    Return confirmation and list of filepaths written."                      │
│                                                                             │
│ OUTPUT PRODUCED:                                                            │
│   • Modified A.2, A.3, A.5, A.6 (as needed based on RQ findings)            │
│   • {TICKER}_A9_ENRICHMENT_TRACE_ENRICH.json - Change manifest              │
│   • {TICKER}_N5_ENRICHMENT_ENRICH.md - Research synthesis narrative         │
│   • {TICKER}_ENRICH_T1_AUDIT.md - Human audit only                          │
│                                                                             │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns paths  │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: ENRICH T1 VALIDATOR                                                 │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate T1 output                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/ENRICH_T1_VALIDATOR.md                                         │
│                                                                             │
│ INPUT FILES:                                                                │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A9_ENRICHMENT_TRACE_ENRICH.json       │
│   • {analysis_dir}/05_ENRICH/{TICKER}_N5_ENRICHMENT_ENRICH.md               │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A2_ANALYTIC_KG_ENRICH.json            │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A5_GIM_ENRICH.json                    │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A6_DR_ENRICH.json                     │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • A9_ENRICHMENT_TRACE exists and is well-formed                           │
│   • Each RQ finding has documented disposition (applied/not applicable)     │
│   • Modified artifacts are valid JSON                                       │
│   • N5 narrative present and substantive                                    │
│   • DR changes have rationale (if DR was modified)                          │
│                                                                             │
│ IF FAIL: Stop. Report issues. Do not proceed to T2.                         │
│ IF PASS: Proceed to Step 3.                                                 │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │ (proceed only if PASS)
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: ENRICH T2 — COMPUTATIONAL (KERNEL EXECUTION)                        │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to execute kernel and produce updated A.7         │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/enrich/G3ENRICH_2.2.3e_PROMPT.md (T2 section)                  │
│   2. kernels/CVR_KERNEL_ENRICH_2.2.3e.py (EXECUTABLE)                       │
│                                                                             │
│ INPUT FILES TO ATTACH (from 05_ENRICH/):                                    │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A5_GIM_ENRICH.json                    │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A6_DR_ENRICH.json                     │
│   • {analysis_dir}/05_ENRICH/{TICKER}_ENRICH_T1_AUDIT.md (context)          │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute ENRICH Turn 2 for {TICKER}.                                      │
│                                                                             │
│    CRITICAL: Manual calculation is PROHIBITED. You MUST use Bash kernel.    │
│    CRITICAL: T2 performs NO reasoning. All judgment is locked in T1.        │
│                                                                             │
│    1. Validate A.5 and A.6 are well-formed (repair if needed - Pattern 5)   │
│    2. Execute kernel via Bash (Pattern 6):                                  │
│                                                                             │
│       python3 kernels/CVR_KERNEL_ENRICH_2.2.3e.py \                         │
│         --a5 {TICKER}_A5_GIM_ENRICH.json \                                  │
│         --a6 {TICKER}_A6_DR_ENRICH.json \                                   │
│         --output {TICKER}_A7_VALUATION_ENRICH.json                          │
│                                                                             │
│    3. Generate kernel receipt (Pattern 13):                                 │
│       Write {TICKER}_KERNEL_RECEIPT_ENRICH.json with:                       │
│       - kernel file, version, sha256                                        │
│       - input filenames                                                     │
│       - command executed                                                    │
│       - exit_code, execution_time_seconds                                   │
│                                                                             │
│    Write output files to {analysis_dir}/05_ENRICH/:                         │
│    1. {TICKER}_A7_VALUATION_ENRICH.json (kernel output)                     │
│    2. {TICKER}_KERNEL_RECEIPT_ENRICH.json (execution proof)                 │
│    3. {TICKER}_ENRICH_T2_AUDIT.md (human audit only)                        │
│                                                                             │
│    Return confirmation and filepaths."                                      │
│                                                                             │
│ OUTPUT PRODUCED:                                                            │
│   • {TICKER}_A7_VALUATION_ENRICH.json - Kernel output (E[IVPS] State 2)     │
│   • {TICKER}_KERNEL_RECEIPT_ENRICH.json - Execution proof (Pattern 13)      │
│   • {TICKER}_ENRICH_T2_AUDIT.md - Human audit only                          │
│                                                                             │
│ PATTERN: Bash Kernel (Pattern 6) - execute kernel via Bash, not manual calc │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns paths  │
│ PATTERN: Kernel Receipts (Pattern 13) - verifiable proof of execution       │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: ENRICH T2 VALIDATOR                                                 │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate T2 output                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/ENRICH_T2_VALIDATOR.md                                         │
│                                                                             │
│ INPUT FILES:                                                                │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A7_VALUATION_ENRICH.json              │
│   • {analysis_dir}/05_ENRICH/{TICKER}_KERNEL_RECEIPT_ENRICH.json            │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A5_GIM_ENRICH.json (cross-validate)   │
│   • {analysis_dir}/05_ENRICH/{TICKER}_A6_DR_ENRICH.json (cross-validate)    │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • A.7 schema compliance                                                   │
│   • Kernel receipt exists (Pattern 13: exit_code=0, timing present)         │
│   • Values have 4+ decimal precision (proves real execution)                │
│   • E[IVPS] is positive and economically sensible                           │
│   • E[IVPS] delta from State 1 is explainable by RQ findings                │
│   • Terminal g < DR (perpetuity validity)                                   │
│   • All artifacts present in 05_ENRICH/ with _ENRICH suffix                 │
│                                                                             │
│ IF FAIL: Report issues. May need T2 re-execution.                           │
│ IF PASS: ENRICH stage complete. CVR is now State 2.                         │
│          Proceed to SCENARIO stage with copy-forward to 06_SCENARIO/.       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Execution Commands (DEV: SMOKE TEST ENRICH {TICKER})

**Step 0: Copy-Forward and Validation**
```bash
# Find most recent RQ output
find smoke_tests/ -path "*/04_RQ/*A9*.json" | sort -r | head -5

# Or check production
find production/analyses/ -path "*/04_RQ/*A9*.json" | sort -r | head -5

# Set analysis_dir to the pipeline run folder
# Execute copy-forward (Pattern 12)
mkdir -p {analysis_dir}/05_ENRICH
for f in {analysis_dir}/04_RQ/{TICKER}_*_RQ.json; do
  base=$(basename "$f" | sed 's/_RQ\.json$//')
  cp "$f" "{analysis_dir}/05_ENRICH/${base}_ENRICH.json"
done
for f in {analysis_dir}/04_RQ/{TICKER}_*_RQ.md; do
  base=$(basename "$f" | sed 's/_RQ\.md$//')
  cp "$f" "{analysis_dir}/05_ENRICH/${base}_ENRICH.md"
done

# Verify inputs
ls {analysis_dir}/05_ENRICH/{TICKER}_A7_VALUATION_ENRICH.json
ls {analysis_dir}/05_ENRICH/{TICKER}_A9_RESEARCH_RESULTS_ENRICH.json
```

**Steps 1-4: Spawn Subagents**
Use Task tool with model="opus" for each step. See Stage Flow above for exact prompts and inputs.

### Critical Patterns Applied

| Pattern | Application |
|---------|-------------|
| Pattern 1: Direct-Write | All subagents write to disk, return filepath only |
| Pattern 3: Two-Shot | T1=synthesis (integrate RQ), T2=kernel execution |
| Pattern 5: JSON Repair | T2 can repair malformed T1 JSON before kernel |
| Pattern 6: Bash Kernel | T2 executes CVR_KERNEL_ENRICH via Bash |
| Pattern 7: Validators | Opus validator after T1 AND T2 |
| Pattern 8: Atomized Prompts | 3 files (PROMPT/SCHEMAS/NORMDEFS) + kernel |
| Pattern 12: Canonical Snapshot | 05_ENRICH/ contains complete State 2 with _ENRICH suffix |
| Pattern 13: Kernel Receipts | T2 generates {TICKER}_KERNEL_RECEIPT_ENRICH.json |

### ENRICH Stage Atomized Files (EXPERIMENTAL)

The ENRICH prompt v2.2.3e is split into 3 atomic files plus kernel, mirroring the BASE pattern:

| File | Purpose | Size | Changes in 2.2.3e |
|------|---------|------|-------------------|
| `G3ENRICH_2.2.3e_PROMPT.md` | Core instructions (Sections I-V) | ~24KB | Kernel receipt instructions |
| `G3ENRICH_2.2.3e_SCHEMAS.md` | JSON schemas (Appendix A) | 16KB | (unchanged from 2.2.2e) |
| `G3ENRICH_2.2.3e_NORMDEFS.md` | DSL & financial definitions (Appendix B) | ~14KB | DR global calibration |
| `CVR_KERNEL_ENRICH_2.2.3e.py` | Valuation kernel | ~40KB | Terminal g from topline growth |

**Key updates from 2.2.2e:**
- Kernel receipt generation instructions (Pattern 13)
- DR calibration against global securities universe (not S&P 500)
- Terminal g derived from topline growth (revenue + EBIT), not ROIC
- Version refs updated to G3_2.2.3e

**Status:** EXPERIMENTAL - pending smoke test. G3ENRICH_2.2.2e remains CANONICAL until smoke test passes.

**Subagent loading:** Load all 3 prompt files. Kernel executed via Bash in T2 (not embedded in subagent context).

---



---

# Stage: SCENARIO

# SCENARIO Stage Orchestration

> **Version:** 1.0.0
> **Extracted from:** workshop/CLAUDE.md v0.12.1
> **Pipeline Position:** Stage 5 of 8 (ENRICH → SCENARIO)

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
{analysis_dir}/
├── 05_ENRICH/                       ← Input: State 2 artifacts
├── 06_SCENARIO/                     ← SCENARIO stage outputs
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_SCEN.json   (copied from ENRICH)
│   ├── {TICKER}_A2_ANALYTIC_KG_SCEN.json         (copied from ENRICH)
│   ├── {TICKER}_A3_CAUSAL_DAG_SCEN.json          (copied from ENRICH)
│   ├── {TICKER}_A5_GIM_SCEN.json                 (copied from ENRICH)
│   ├── {TICKER}_A6_DR_SCEN.json                  (copied from ENRICH)
│   ├── {TICKER}_A7_VALUATION_SCEN.json           (copied from ENRICH)
│   ├── {TICKER}_A8_RESEARCH_PLAN_SCEN.json       (copied from ENRICH)
│   ├── {TICKER}_A9_RESEARCH_RESULTS_SCEN.json    (copied from ENRICH)
│   ├── {TICKER}_A9_ENRICHMENT_TRACE_SCEN.json    (copied from ENRICH)
│   ├── {TICKER}_A10_SCENARIO_SCEN.json           (NEW - T2 kernel output)
│   ├── {TICKER}_SCEN_T1.md                       (NEW - T1 narrative)
│   ├── {TICKER}_SCEN_T2.md                       (NEW - T2 narrative)
│   ├── {TICKER}_N6_SCENARIO_SCEN.md              (NEW - scenario synthesis)
│   └── {TICKER}_KERNEL_RECEIPT_SCEN.json         (NEW - Pattern 13)
├── 07_SILICON_COUNCIL/              ← Next stage
└── PIPELINE_STATE.md
```

**Copy-Forward Protocol:** Before SCENARIO T1, orchestrator copies ENRICH artifacts from 05_ENRICH/ to 06_SCENARIO/ with suffix rename (_ENRICH → _SCEN) using `cp`.

### Execution Commands (DEV: SMOKE TEST SCENARIO {TICKER})

**Step 0: Locate Most Recent ENRICH Output (Auto-Discovery)**
```
1. Search for ENRICH smoke test folders:
   ls -t workshop/smoke_tests/*ENRICH*{TICKER}* | head -5

2. If none found in workshop, check production:
   ls -t production/analyses/{TICKER}_*/05_ENRICH/ | head -5

3. Select the most recent folder with complete ENRICH output
   (must contain {TICKER}_A7_VALUATION_ENRICH.json with State 2 IVPS)

4. Set {analysis_dir} to the parent of 05_ENRICH/
   Example: workshop/smoke_tests/{TICKER}_ENRICH_SMOKE_{TIMESTAMP}/
```

**Step 1: Validate Input (Pattern 10 - MANDATORY)**
```
READ files in {analysis_dir}/05_ENRICH/ to verify:
- {TICKER}_A7_VALUATION_ENRICH.json exists with State 2 IVPS
- Extract and log: base_ivps, dr_static, terminal_g, terminal_roic
- Verify IVPS consistency with A7 JSON
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
- {analysis_dir}/06_SCENARIO/*.json (artifacts with _SCEN suffix)
- kernels/CVR_KERNEL_SCEN_2_2_2e.py

Instruct: "Execute SCENARIO T2 for {TICKER}.

CRITICAL: Manual calculation is PROHIBITED. You MUST use Bash kernel.

1. Validate T1 JSON is well-formed (repair if needed - Pattern 5)
2. Execute kernel via Bash (Pattern 6):

   python3 kernels/CVR_KERNEL_SCEN_2_2_2e.py \
     --args {scenario_execution_args} \
     --a5 {TICKER}_A5_GIM_SCEN.json \
     --a7 {TICKER}_A7_VALUATION_SCEN.json \
     --output {TICKER}_A10_SCENARIO_SCEN.json

3. Generate kernel receipt (Pattern 13):
   Write {TICKER}_KERNEL_RECEIPT_SCEN.json with:
   - kernel file, version, sha256
   - input filenames
   - command executed
   - exit_code, execution_time_seconds

Write output files to {analysis_dir}/06_SCENARIO/:
1. {TICKER}_A10_SCENARIO_SCEN.json (kernel output)
2. {TICKER}_N6_SCENARIO_SCEN.md (scenario synthesis narrative)
3. {TICKER}_KERNEL_RECEIPT_SCEN.json (execution proof)
4. {TICKER}_SCEN_T2_AUDIT.md (human audit only)

Return confirmation and filepaths."

Subagent executes kernel via Bash (Pattern 6).
Subagent writes output directly to disk (Pattern 1).
Subagent generates kernel receipt (Pattern 13).
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
| Pattern 6: Bash Kernel | T2 executes CVR_KERNEL_SCEN via Bash, never manual calculation |
| Pattern 12: Canonical Snapshot | 06_SCENARIO/ contains complete artifact set with _SCEN suffix |
| Pattern 13: Kernel Receipts | T2 generates {TICKER}_KERNEL_RECEIPT_SCEN.json for reproducibility |
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



---

# Stage: SC

# SILICON COUNCIL Stage Orchestration

> **Version:** 1.0.0
> **Extracted from:** workshop/CLAUDE.md v0.12.1
> **Pipeline Position:** Stage 6 of 8 (SCENARIO → SILICON COUNCIL)

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
│    to {output_dir}/{TICKER}_SC_{AUDIT_TYPE}_SC.json. Return confirmation."  │
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
├── 06_SCENARIO/                     ← Input: State 3 artifacts
├── 07_SILICON_COUNCIL/              ← SILICON COUNCIL outputs
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_SC.json   (copied from SCEN)
│   ├── {TICKER}_A2_ANALYTIC_KG_SC.json         (copied from SCEN)
│   ├── {TICKER}_A3_CAUSAL_DAG_SC.json          (copied from SCEN)
│   ├── {TICKER}_A5_GIM_SC.json                 (copied from SCEN)
│   ├── {TICKER}_A6_DR_SC.json                  (copied from SCEN)
│   ├── {TICKER}_A7_VALUATION_SC.json           (copied from SCEN)
│   ├── {TICKER}_A10_SCENARIO_SC.json           (copied from SCEN)
│   ├── {TICKER}_SC_ACCOUNTING_SC.json          (NEW - audit output)
│   ├── {TICKER}_SC_FIT_SC.json                 (NEW - audit output)
│   ├── {TICKER}_SC_EPISTEMIC_SC.json           (NEW - audit output)
│   ├── {TICKER}_SC_RED_TEAM_SC.json            (NEW - audit output)
│   ├── {TICKER}_SC_DISTRIBUTIONAL_SC.json      (NEW - audit output)
│   ├── {TICKER}_SC_ECONOMIC_REALISM_SC.json    (NEW - audit output)
│   └── {TICKER}_A11_AUDIT_SC.json              (NEW - consolidated audit)
├── 08_INTEGRATION/                  ← Next stage
└── PIPELINE_STATE.md
```

**Copy-Forward Protocol:** Before SC audits, orchestrator copies SCENARIO artifacts from 06_SCENARIO/ to 07_SILICON_COUNCIL/ with suffix rename (_SCEN → _SC) using `cp`.

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
    {output_dir}/{TICKER}_SC_{AUDIT_TYPE}_SC.json

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
    - {TICKER}_SC_ACCOUNTING_SC.json
    - {TICKER}_SC_FIT_SC.json
    - {TICKER}_SC_EPISTEMIC_SC.json
    - {TICKER}_SC_RED_TEAM_SC.json
    - {TICKER}_SC_DISTRIBUTIONAL_SC.json
    - {TICKER}_SC_ECONOMIC_REALISM_SC.json

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
- {TICKER}_SC_ACCOUNTING_SC.json → {TICKER}_SC_ACCOUNTING_SC.md
- {TICKER}_SC_FIT_SC.json → {TICKER}_SC_FIT_SC.md
- {TICKER}_SC_EPISTEMIC_SC.json → {TICKER}_SC_EPISTEMIC_SC.md
- {TICKER}_SC_RED_TEAM_SC.json → {TICKER}_SC_RED_TEAM_SC.md
- {TICKER}_SC_DISTRIBUTIONAL_SC.json → {TICKER}_SC_DISTRIBUTIONAL_SC.md
- {TICKER}_SC_ECONOMIC_REALISM_SC.json → {TICKER}_SC_ECONOMIC_REALISM_SC.md
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
| Pattern 12: Canonical Snapshot | 07_SILICON_COUNCIL/ contains complete artifact set with _SC suffix |

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



---

# Stage: INTEGRATION

# INTEGRATION Stage Orchestration

> **Version:** 1.0.0
> **Extracted from:** workshop/CLAUDE.md v0.12.1
> **Pipeline Position:** Stage 7 of 8 (SILICON COUNCIL → INTEGRATION)

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
├── 00_source/                       ← Source financials (10-K, 10-Q, transcripts)
├── 07_SILICON_COUNCIL/              ← Input: SC audit outputs + State 3 artifacts
├── 08_INTEGRATION/                  ← INTEGRATION outputs
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_INT.json   (adjudicated from SC)
│   ├── {TICKER}_A2_ANALYTIC_KG_INT.json         (adjudicated from SC)
│   ├── {TICKER}_A3_CAUSAL_DAG_INT.json          (adjudicated from SC)
│   ├── {TICKER}_A5_GIM_INT.json                 (adjudicated - kernel input)
│   ├── {TICKER}_A6_DR_INT.json                  (adjudicated - kernel input)
│   ├── {TICKER}_A7_VALUATION_INT.json           (T2 kernel output if cascade)
│   ├── {TICKER}_A10_SCENARIO_INT.json           (adjudicated - kernel input)
│   ├── {TICKER}_A11_AUDIT_INT.json              (copied from SC)
│   ├── {TICKER}_A12_CASCADE_INT.json            (NEW - cascade decision)
│   ├── {TICKER}_INT_T1_AUDIT.md                 (NEW - adjudication narrative)
│   ├── {TICKER}_INT_T2_AUDIT.md                 (NEW - recalculation narrative)
│   ├── {TICKER}_CVR_STATE4_INT.md               (NEW - final CVR State 4)
│   ├── {TICKER}_N1_THESIS_INT.md                (adjudicated if needed)
│   ├── {TICKER}_N2_IC_INT.md                    (adjudicated if needed)
│   ├── {TICKER}_N3_ECON_GOV_INT.md              (adjudicated if needed)
│   ├── {TICKER}_N4_RISK_INT.md                  (adjudicated if needed)
│   ├── {TICKER}_N5_ENRICHMENT_INT.md            (adjudicated if needed)
│   ├── {TICKER}_N6_SCENARIO_INT.md              (adjudicated if needed)
│   ├── {TICKER}_N7_ADJUDICATION_INT.md          (NEW - adjudication synthesis)
│   └── {TICKER}_KERNEL_RECEIPT_INT.json         (NEW - Pattern 13, if cascade)
├── 09_IRR/                          ← Next stage
└── PIPELINE_STATE.md
```

**Copy-Forward Protocol:** Before INTEGRATION T1, orchestrator copies SC artifacts from 07_SILICON_COUNCIL/ to 08_INTEGRATION/ with suffix rename (_SC → _INT) using `cp`. T1 then adjudicates and modifies these files in place.

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
│ │   • {TICKER}_ENRICH_T1_AUDIT.md (analysis narrative)                    │ │
│ │   • {TICKER}_ENRICH_T2_AUDIT.md (kernel output narrative)               │ │
│ │   • {TICKER}_A1_EPISTEMIC_ANCHORS_ENRICH.json                           │ │
│ │   • {TICKER}_A2_ANALYTIC_KG_ENRICH.json                                 │ │
│ │   • {TICKER}_A3_CAUSAL_DAG_ENRICH.json                                  │ │
│ │   • {TICKER}_A5_GIM_ENRICH.json                                         │ │
│ │   • {TICKER}_A6_DR_ENRICH.json                                          │ │
│ │   • {TICKER}_A7_VALUATION_ENRICH.json (contains Base Case IVPS)         │ │
│ │   • {TICKER}_A9_ENRICHMENT_TRACE_ENRICH.json                            │ │
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
│ │   • {TICKER}_SCEN_T1_AUDIT.md (scenario identification narrative)       │ │
│ │   • {TICKER}_SCEN_T2_AUDIT.md (SSE execution narrative)                 │ │
│ │   • {TICKER}_A10_SCENARIO_SCEN.json (scenarios, probabilities, dist)    │ │
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
│ │   • {TICKER}_SC_ACCOUNTING_SC.json (source integrity findings)          │ │
│ │   • {TICKER}_SC_FIT_SC.json (pipeline fit assessment)                   │ │
│ │   • {TICKER}_SC_EPISTEMIC_SC.json (Bayesian protocol compliance)        │ │
│ │   • {TICKER}_SC_RED_TEAM_SC.json (adversarial review)                   │ │
│ │   • {TICKER}_SC_DISTRIBUTIONAL_SC.json (distribution coherence)         │ │
│ │   • {TICKER}_SC_ECONOMIC_REALISM_SC.json (top-down plausibility)        │ │
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
│   1. prompts/integration/G3_INTEGRATION_2.2.3e_PROMPT.md                    │
│   2. prompts/integration/G3_INTEGRATION_2.2.3e_SCHEMAS.md                   │
│   3. prompts/integration/G3_INTEGRATION_2.2.3e_NORMDEFS.md                  │
│   4. kernels/CVR_KERNEL_INT_2_2_2e.py (FOR CONTEXT ONLY - DO NOT EXECUTE)   │
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
│    Then execute the SURGICAL EDIT PROTOCOL (CRITICAL):                      │
│    For each artifact (A.1, A.2, A.3, A.5, A.6, A.10):                       │
│    1. READ the State 3 version from the epistemic bundle                    │
│    2. APPLY any modifications required by your adjudication dispositions    │
│    3. WRITE the complete artifact with _S4 suffix to output_dir             │
│    If no modifications needed for an artifact, copy it unchanged.           │
│                                                                             │
│    Also extract and edit narratives N1-N6 from upstream T2 outputs.         │
│    Add [State 4: Revised per F{N}] annotations where modified.              │
│                                                                             │
│    DO NOT execute the kernel. It is provided for context only.              │
│                                                                             │
│    YOU MUST WRITE ALL OUTPUT FILES TO {analysis_dir}/08_INTEGRATION/:       │
│    1. {TICKER}_INT_T1_AUDIT.md (adjudication reasoning - human audit only)  │
│    2. {TICKER}_A1_EPISTEMIC_ANCHORS_INT.json (adjudicated)                  │
│    3. {TICKER}_A2_ANALYTIC_KG_INT.json (adjudicated)                        │
│    4. {TICKER}_A3_CAUSAL_DAG_INT.json (adjudicated)                         │
│    5. {TICKER}_A5_GIM_INT.json (adjudicated, kernel input)                  │
│    6. {TICKER}_A6_DR_INT.json (adjudicated, kernel input)                   │
│    7. {TICKER}_A10_SCENARIO_INT.json (adjudicated, kernel input)            │
│    8. {TICKER}_N1_THESIS_INT.md through {TICKER}_N7_ADJUDICATION_INT.md     │
│    9. {TICKER}_A12_CASCADE_INT.json (cascade scope + modifications)         │
│                                                                             │
│    Return confirmation and list of filepaths written."                      │
│                                                                             │
│ OUTPUT PRODUCED:                                                            │
│   • {TICKER}_INT_T1_AUDIT.md - Adjudication reasoning (human audit)         │
│   • {TICKER}_A1_EPISTEMIC_ANCHORS_INT.json - Adjudicated artifact           │
│   • {TICKER}_A2_ANALYTIC_KG_INT.json - Adjudicated artifact                 │
│   • {TICKER}_A3_CAUSAL_DAG_INT.json - Adjudicated artifact                  │
│   • {TICKER}_A5_GIM_INT.json - Adjudicated, kernel input                    │
│   • {TICKER}_A6_DR_INT.json - Adjudicated, kernel input                     │
│   • {TICKER}_A10_SCENARIO_INT.json - Adjudicated, kernel input              │
│   • {TICKER}_N1-N7_*_INT.md - Revised narratives (7 files: N1-N7)           │
│   • {TICKER}_A12_CASCADE_INT.json - Cascade scope + modifications           │
│                                                                             │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns paths │
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
│ INPUT FILES (verify ALL exist in 08_INTEGRATION/):                          │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_INT_T1_AUDIT.md                    │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_A1_EPISTEMIC_ANCHORS_INT.json      │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_A2_ANALYTIC_KG_INT.json            │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_A3_CAUSAL_DAG_INT.json             │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_A5_GIM_INT.json                    │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_A6_DR_INT.json                     │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_A10_SCENARIO_INT.json              │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_N*_INT.md (7 narrative files)      │
│   {analysis_dir}/08_INTEGRATION/{TICKER}_A12_CASCADE_INT.json               │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • ALL T1 OUTPUT FILES EXIST with _INT suffix (block T2 if missing)        │
│   • All CRITICAL findings have explicit disposition                         │
│   • All HIGH findings have explicit disposition                             │
│   • A12_CASCADE_INT.json is well-formed with valid cascade_scope            │
│   • If cascade_scope != NONE, modifications array is non-empty              │
│   • scenarios_finalized contains ≤4 scenarios                               │
│   • _INT.json artifacts are valid JSON and contain required fields          │
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
│   1. prompts/integration/G3_INTEGRATION_2.2.3e_PROMPT.md                    │
│   2. kernels/CVR_KERNEL_INT_2_2_2e.py (EXECUTABLE)                          │
│                                                                             │
│ INPUT FILES TO ATTACH (from 08_INTEGRATION/ - T1 outputs):                  │
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_INT_T1_AUDIT.md                  │
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_A5_GIM_INT.json                  │
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_A6_DR_INT.json                   │
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_A10_SCENARIO_INT.json            │
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_A12_CASCADE_INT.json             │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute INTEGRATION Turn 2 for {TICKER}.                                 │
│                                                                             │
│    CRITICAL: You receive ONLY T1 outputs. Do NOT request epistemic bundle.  │
│    CRITICAL: Manual calculation is PROHIBITED. You MUST use Bash kernel.    │
│                                                                             │
│    Read A12_CASCADE_INT.json to determine cascade_scope.                    │
│                                                                             │
│    If cascade_scope = NONE: State 4 = State 3, copy artifacts unchanged.    │
│    If cascade_scope != NONE: Execute kernel via Bash:                       │
│                                                                             │
│    python3 CVR_KERNEL_INT_2_2_2e.py \                                       │
│      --a5 {TICKER}_A5_GIM_INT.json \                                        │
│      --a6 {TICKER}_A6_DR_INT.json \                                         │
│      --a10 {TICKER}_A10_SCENARIO_INT.json \                                 │
│      --cascade {TICKER}_A12_CASCADE_INT.json \                              │
│      --output {TICKER}_A7_VALUATION_INT.json                                │
│                                                                             │
│    If kernel executed, generate kernel receipt (Pattern 13):                │
│    Write {TICKER}_KERNEL_RECEIPT_INT.json with:                             │
│    - kernel file, version, sha256                                           │
│    - input filenames                                                        │
│    - command executed                                                       │
│    - exit_code, execution_time_seconds                                      │
│                                                                             │
│    Write outputs to {analysis_dir}/08_INTEGRATION/:                         │
│    - {TICKER}_A7_VALUATION_INT.json (kernel output if cascade)              │
│    - {TICKER}_A10_SCENARIO_INT.json (updated if SSE changed)                │
│    - {TICKER}_KERNEL_RECEIPT_INT.json (if kernel executed)                  │
│    - {TICKER}_INT_T2_AUDIT.md (human audit only)                            │
│    Return confirmation and filepaths only."                                 │
│                                                                             │
│ OUTPUT PRODUCED (if cascade):                                               │
│   • {TICKER}_A7_VALUATION_INT.json - Kernel output (recalculated valuation) │
│   • {TICKER}_A10_SCENARIO_INT.json - Updated SSE (if changed)               │
│   • {TICKER}_KERNEL_RECEIPT_INT.json - Execution proof (Pattern 13)         │
│   • {TICKER}_INT_T2_AUDIT.md - Human audit only                             │
│                                                                             │
│ PATTERN: Bash Kernel (Pattern 6) - execute kernel via Bash if cascade needed│
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns path   │
│ PATTERN: Kernel Receipts (Pattern 13) - generate if kernel was executed     │
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
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_INT_T2_AUDIT.md                  │
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_A12_CASCADE_INT.json             │
│   • {analysis_dir}/08_INTEGRATION/{TICKER}_KERNEL_RECEIPT_INT.json (if any) │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • All artifacts A.1-A.12 present with _INT suffix                         │
│   • Amendment manifest documents all changes                                │
│   • state_4_active_inputs is complete                                       │
│   • State bridge shows valid State 3 → State 4 delta                        │
│   • If cascade executed: kernel receipt exists (Pattern 13), exit_code=0    │
│   • If cascade executed: values have 4+ decimal precision (real execution)  │
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
│   1. prompts/integration/G3_INTEGRATION_2.2.3e_PROMPT.md                    │
│   2. prompts/integration/G3_INTEGRATION_2.2.3e_SCHEMAS.md                   │
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
| Pattern 12: Canonical Snapshot | 08_INTEGRATION/ contains complete artifact set with _INT suffix |
| Pattern 13: Kernel Receipts | T2 generates {TICKER}_KERNEL_RECEIPT_INT.json if cascade executed |

### INTEGRATION Stage Files

| File | Location | Purpose |
|------|----------|---------|
| G3_INTEGRATION_2.2.3e_PROMPT.md | prompts/integration/ | Core instructions (Sections I-V) |
| G3_INTEGRATION_2.2.3e_SCHEMAS.md | prompts/integration/ | JSON schemas (Appendix A) |
| G3_INTEGRATION_2.2.3e_NORMDEFS.md | prompts/integration/ | DSL & financial definitions (Appendix B) |
| CVR_KERNEL_INT_2_2_2e.py | kernels/ | Recalculation kernel |
| INT_T1_VALIDATOR.md | validators/ | T1 adjudication validator |
| INT_T2_VALIDATOR.md | validators/ | T2 recalculation validator |
| INT_T3_VALIDATOR.md | validators/ | T3 final output validator |

### INTEGRATION Stage Atomized Files (EXPERIMENTAL)

| File | Purpose | Lines |
|------|---------|-------|
| `G3_INTEGRATION_2.2.3e_PROMPT.md` | Core instructions (Sections I-V) | 1307 |
| `G3_INTEGRATION_2.2.3e_SCHEMAS.md` | JSON schemas (Appendix A) | 512 |
| `G3_INTEGRATION_2.2.3e_NORMDEFS.md` | DSL & financial definitions (Appendix B) | 567 |
| `CVR_KERNEL_INT_2_2_2e.py` | Recalculation kernel | (existing) |

**Status:** EXPERIMENTAL - awaiting smoke test.

**Subagent loading:** Load all 3 prompt files. Kernel attached for T1 context, executed via Bash in T2.

---



---

# Stage: IRR

# IRR Stage Orchestration

> **Version:** 1.0.0
> **Extracted from:** workshop/CLAUDE.md v0.12.1
> **Pipeline Position:** Stage 8 of 8 (INTEGRATION → IRR)

---

## IRR Stage Orchestration (INTEGRATION → IRR)

The IRR stage is the **final stage (8/8)** of the CAPY pipeline. It transitions the CVR from State 4 (Finalized Intrinsic Value) to State 5 (Expected Return).

### Purpose and Context

**What happened before IRR:**
1. **ENRICH** produced deterministic IVPS (State 2)
2. **SCENARIO** added probabilistic scenarios (State 3)
3. **SILICON COUNCIL** audited across 6 dimensions
4. **INTEGRATION** adjudicated findings and finalized artifacts (State 4)

**What IRR does:**
The upstream stages answer "What is it worth?" IRR answers **"What will I make?"**

This requires:
1. Fetching **live market price** (mandatory WebSearch)
2. Estimating **resolution percentage (ρ)** for each scenario - how much resolves by T+1
3. Deriving **Convergence Rate (CR)** via B.13 rubric - recognition speed factors only
4. Executing kernel to calculate **E[IRR]** and distribution via Transition Factor methodology

### Architecture (v2.2.5e)

**Two-Shot Execution:**

| Turn | Name | Purpose | Key Output |
|------|------|---------|------------|
| T1 | Analytical | ρ estimation, CR derivation, live price fetch, input extraction | A.13 + IRR_INPUTS.json + T1.md |
| T2 | Computational | Kernel execution via Bash (Pattern 6) | A.14 + T2.md (FINAL: A.13 + A.14 + N7) |

**Key Design Decisions:**
- **Two-shot not three-shot:** T2 IS the final output (no T3 needed)
- **WebSearch mandatory:** T1 MUST fetch live price - stale prices = wrong IRR
- **N8 is new narrative:** Completes the N1-N7 chain from INTEGRATION
- **ρ is LLM judgment:** Resolution percentage cannot be automated - requires timeline evidence analysis

### Directory Structure

**Canonical Snapshot (Pattern 12):** 09_IRR/ contains ALL artifacts with _IRR suffix.

```
{analysis_dir}/
├── 08_INTEGRATION/                              ← INPUT: Canonical snapshot with _INT suffix
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_INT.json       (adjudicated)
│   ├── {TICKER}_A2_ANALYTIC_KG_INT.json             (adjudicated)
│   ├── {TICKER}_A3_CAUSAL_DAG_INT.json              (adjudicated)
│   ├── {TICKER}_A5_GIM_INT.json                     (adjudicated)
│   ├── {TICKER}_A6_DR_INT.json                      (adjudicated)
│   ├── {TICKER}_A7_VALUATION_INT.json               (adjudicated, kernel if cascade)
│   ├── {TICKER}_A8_RESEARCH_PLAN_INT.json           (copied from SC)
│   ├── {TICKER}_A9_RESEARCH_RESULTS_INT.json        (copied from SC)
│   ├── {TICKER}_A9_ENRICHMENT_TRACE_INT.json        (copied from SC)
│   ├── {TICKER}_A10_SCENARIO_INT.json               (adjudicated)
│   ├── {TICKER}_A11_AUDIT_INT.json                  (copied from SC)
│   ├── {TICKER}_A12_CASCADE_INT.json                (NEW: cascade trace)
│   ├── {TICKER}_N1_THESIS_INT.md                    (revised if needed)
│   ├── {TICKER}_N2_IC_INT.md                        (revised if needed)
│   ├── {TICKER}_N3_ECON_GOV_INT.md                  (revised if needed)
│   ├── {TICKER}_N4_RISK_INT.md                      (revised if needed)
│   ├── {TICKER}_N5_ENRICHMENT_INT.md                (revised if needed)
│   ├── {TICKER}_N6_SCENARIO_INT.md                  (revised if needed)
│   ├── {TICKER}_N7_ADJUDICATION_INT.md              (NEW: adjudication narrative)
│   ├── {TICKER}_RQ1-RQ7_*_INT.md                    (copied from SC, 7 files)
│   ├── {TICKER}_SC_*_AUDIT_INT.json                 (copied from SC, 6 files)
│   ├── {TICKER}_CVR_STATE4_INT.md                   (NEW: T3 concatenation for human audit)
│   └── {TICKER}_KERNEL_RECEIPT_INT.json             (if valuation kernel was re-run)
│
├── 09_IRR/                                      ← IRR stage outputs (canonical snapshot)
│   ├── {TICKER}_A1_EPISTEMIC_ANCHORS_IRR.json       (COPIED from INT by orchestrator)
│   ├── {TICKER}_A2_ANALYTIC_KG_IRR.json             (COPIED from INT by orchestrator)
│   ├── {TICKER}_A3_CAUSAL_DAG_IRR.json              (COPIED from INT by orchestrator)
│   ├── {TICKER}_A5_GIM_IRR.json                     (COPIED from INT by orchestrator)
│   ├── {TICKER}_A6_DR_IRR.json                      (COPIED from INT by orchestrator)
│   ├── {TICKER}_A7_VALUATION_IRR.json               (COPIED from INT by orchestrator)
│   ├── {TICKER}_A10_SCENARIO_IRR.json               (COPIED from INT by orchestrator)
│   ├── {TICKER}_A12_CASCADE_IRR.json                (COPIED from INT by orchestrator)
│   ├── {TICKER}_N1-N6_*_IRR.md                      (COPIED from INT by orchestrator, 6 files)
│   ├── {TICKER}_A13_RESOLUTION_IRR.json             (NEW T1: ρ estimates, CR, inputs)
│   ├── {TICKER}_IRR_INPUTS_IRR.json                 (NEW T1: extracted kernel inputs)
│   ├── {TICKER}_A14_IRR_ANALYSIS_IRR.json           (NEW T2: kernel output)
│   ├── {TICKER}_N8_IRR_IRR.md                       (NEW T2: IRR narrative)
│   ├── {TICKER}_KERNEL_RECEIPT_IRR.json             (NEW T2: kernel execution proof)
│   └── {TICKER}_IRR_T1_AUDIT.md                     (human audit only)
│
└── pipeline_state.json
```

**Copy-Forward Protocol (Orchestrator executes BEFORE IRR T1):**
```bash
mkdir -p {analysis_dir}/09_IRR

# Copy core artifacts from INTEGRATION with suffix rename
for f in {analysis_dir}/08_INTEGRATION/{TICKER}_A*_INT.json; do
  base=$(basename "$f" | sed 's/_INT\.json$//')
  cp "$f" "{analysis_dir}/09_IRR/${base}_IRR.json"
done

# Copy narratives
for f in {analysis_dir}/08_INTEGRATION/{TICKER}_N*_INT.md; do
  base=$(basename "$f" | sed 's/_INT\.md$//')
  cp "$f" "{analysis_dir}/09_IRR/${base}_IRR.md"
done
```

### Stage Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 0: COPY-FORWARD AND INPUT VALIDATION                                   │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Orchestrator (YOU) copies artifacts from INT → IRR, then validates    │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ 1. Locate most recent complete INTEGRATION run:                             │
│    find smoke_tests/ -path "*/08_INTEGRATION/*A7*_INT.json" | sort -r       │
│                                                                             │
│ 2. Execute copy-forward (Pattern 12 - see bash script above):               │
│    mkdir -p {analysis_dir}/09_IRR                                           │
│    for f in {analysis_dir}/08_INTEGRATION/{TICKER}_*_INT.*; do              │
│      # Copy with suffix rename: _INT → _IRR                                 │
│    done                                                                     │
│                                                                             │
│ 3. Verify folder contains ALL required artifact files:                      │
│    - {TICKER}_A2_ANALYTIC_KG_IRR.json    (copied from INT)                  │
│    - {TICKER}_A7_VALUATION_IRR.json      (copied from INT)                  │
│    - {TICKER}_A10_SCENARIO_IRR.json      (copied from INT)                  │
│                                                                             │
│ 4. READ key files to extract baseline metrics:                              │
│    - E[IVPS] from A7 or A10                                                 │
│    - DR from A6 or A7                                                       │
│    - Scenario count from A10                                                │
│                                                                             │
│ Set {analysis_dir} to the pipeline run folder.                              │
│ Proceed to Step 1 with 09_IRR/ folder ready.                                │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: IRR T1 — ANALYTICAL                                                 │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to perform analytical judgment                    │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/irr/G3_IRR_2.2.5e_PROMPT.md                                    │
│   2. prompts/irr/G3_IRR_2.2.5e_SCHEMAS.md                                   │
│   3. prompts/irr/G3_IRR_2.2.5e_NORMDEFS.md                                  │
│   4. kernels/CVR_KERNEL_IRR_2.2.5e.py (FOR CONTEXT ONLY - DO NOT EXECUTE)   │
│                                                                             │
│ INPUT FILES TO ATTACH (from 09_IRR/ - copied by orchestrator):              │
│   • {analysis_dir}/09_IRR/{TICKER}_A2_ANALYTIC_KG_IRR.json                  │
│   • {analysis_dir}/09_IRR/{TICKER}_A5_GIM_IRR.json                          │
│   • {analysis_dir}/09_IRR/{TICKER}_A7_VALUATION_IRR.json                    │
│   • {analysis_dir}/09_IRR/{TICKER}_A10_SCENARIO_IRR.json                    │
│   • {analysis_dir}/09_IRR/{TICKER}_N1-N6_*_IRR.md (context, 6 files)        │
│                                                                             │
│ WHY 09_IRR/ NOT 08_INTEGRATION/:                                            │
│   Pattern 12: Canonical Snapshot. Each stage folder contains COMPLETE       │
│   artifact set. Orchestrator has already copied with suffix rename.         │
│   Subagent reads from its own stage folder, writes to its own stage folder. │
│   This ensures artifact provenance is always traceable by folder.                   │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute IRR Turn 1 for {TICKER}.                                         │
│                                                                             │
│    MANDATORY FIRST STEP: WebSearch for '{TICKER} stock price' to get        │
│    current market price. Record source and timestamp. This live price       │
│    OVERRIDES any price in the State 4 bundle.                               │
│                                                                             │
│    Your analytical tasks:                                                   │
│    1. Extract and validate inputs from State 4 JSON files                   │
│    2. For each scenario in A10, estimate ρ (resolution percentage):         │
│       - Identify primary driver (legal, product, macro, earnings)           │
│       - Identify key dates/milestones before T+1                            │
│       - Default ρ ≤ 0.30 unless timeline evidence supports higher           │
│    3. Derive Convergence Rate (CR) via B.13 rubric:                         │
│       - Base rate = 0.20                                                    │
│       - Adjust ONLY for recognition factors (Categories 1-4)                │
│       - DO NOT adjust for fundamental factors (double-counting)             │
│       - Final CR in [0.10, 0.40]                                            │
│    4. Select valuation multiple per B.10 rubric                             │
│    5. Complete anti-narrative check (3 reasons market may not re-rate)      │
│                                                                             │
│    DO NOT execute the kernel. It is provided for context only.              │
│                                                                             │
│    Write 3 output files to {analysis_dir}/09_IRR/:                          │
│    1. {TICKER}_IRR_T1_AUDIT.md (reasoning narrative - human audit only)     │
│    2. {TICKER}_A13_RESOLUTION_IRR.json (kernel input - canonical artifact)  │
│    3. {TICKER}_IRR_INPUTS_IRR.json (extracted data for kernel)              │
│                                                                             │
│    Return confirmation and list of filepaths written."                      │
│                                                                             │
│ OUTPUT PRODUCED (3 files):                                                  │
│   • {TICKER}_IRR_T1_AUDIT.md - Reasoning, ρ derivation, CR derivation       │
│   • {TICKER}_A13_RESOLUTION_IRR.json - ρ per scenario, CR, inputs           │
│   • {TICKER}_IRR_INPUTS_IRR.json - Extracted market data, fundamentals,     │
│     scenarios for kernel consumption                                        │
│                                                                             │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns paths │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: IRR T1 VALIDATOR                                                    │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate T1 output                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/IRR_T1_VALIDATOR.md                                            │
│                                                                             │
│ INPUT FILES:                                                                │
│   • {analysis_dir}/09_IRR/{TICKER}_IRR_T1_AUDIT.md                          │
│   • {analysis_dir}/09_IRR/{TICKER}_A13_RESOLUTION_IRR.json                  │
│   • {analysis_dir}/09_IRR/{TICKER}_IRR_INPUTS_IRR.json                      │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • A.13 schema compliance (G3_2.2.5eIRR)                                   │
│   • All scenarios have ρ estimates                                          │
│   • ρ values in [0, 1], ρ > 0.30 has evidence                               │
│   • CR derived from recognition factors only (no double-counting)           │
│   • CR in [0.10, 0.40] or has deviation_rationale                           │
│   • Anti-narrative check has 3 substantive reasons                          │
│   • Live price documented (WebSearch evidence)                              │
│   • IRR_INPUTS.json complete and consistent with A.13                       │
│                                                                             │
│ IF FAIL: Stop. Report issues. Do not proceed to T2.                         │
│ IF PASS: Proceed to Step 3.                                                 │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │ (proceed only if PASS)
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: IRR T2 — COMPUTATIONAL (KERNEL EXECUTION)                           │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to execute kernel and produce final output        │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILES TO ATTACH:                                                     │
│   1. prompts/irr/G3_IRR_2.2.5e_PROMPT.md                                    │
│   2. kernels/CVR_KERNEL_IRR_2.2.5e.py (EXECUTABLE)                          │
│                                                                             │
│ INPUT FILES TO ATTACH (from 09_IRR/):                                       │
│   • {analysis_dir}/09_IRR/{TICKER}_IRR_T1_AUDIT.md (T1 reasoning)           │
│   • {analysis_dir}/09_IRR/{TICKER}_A13_RESOLUTION_IRR.json                  │
│   • {analysis_dir}/09_IRR/{TICKER}_IRR_INPUTS_IRR.json                      │
│                                                                             │
│ INSTRUCTION TO SUBAGENT:                                                    │
│   "Execute IRR Turn 2 for {TICKER}.                                         │
│                                                                             │
│    CRITICAL: Manual calculation is PROHIBITED. You MUST use Bash kernel.    │
│    CRITICAL: T2 performs NO reasoning. All judgment is locked in A.13.      │
│                                                                             │
│    1. Validate A.13 and IRR_INPUTS are well-formed (repair if needed)       │
│    2. Execute kernel via Bash (Pattern 6):                                  │
│                                                                             │
│       python3 kernels/CVR_KERNEL_IRR_2.2.5e.py \                            │
│         --a13 {TICKER}_A13_RESOLUTION_IRR.json \                            │
│         --inputs {TICKER}_IRR_INPUTS_IRR.json \                             │
│         --output {TICKER}_A14_IRR_ANALYSIS_IRR.json                         │
│                                                                             │
│    3. Generate kernel receipt (Pattern 13):                                 │
│       Write {TICKER}_KERNEL_RECEIPT_IRR.json with:                          │
│       - kernel file, version, sha256                                        │
│       - input filenames                                                     │
│       - command executed                                                    │
│       - exit_code, execution_time_seconds                                   │
│                                                                             │
│    4. Write N8 IRR Narrative (executive summary of expected return)         │
│                                                                             │
│    Write 3 output files to {analysis_dir}/09_IRR/:                          │
│    1. {TICKER}_A14_IRR_ANALYSIS_IRR.json (kernel output)                    │
│    2. {TICKER}_N8_IRR_IRR.md (IRR narrative)                                │
│    3. {TICKER}_KERNEL_RECEIPT_IRR.json (execution proof)                    │
│                                                                             │
│    Return confirmation and filepaths."                                      │
│                                                                             │
│ OUTPUT PRODUCED (3 files):                                                  │
│   • {TICKER}_A14_IRR_ANALYSIS_IRR.json - Kernel output (E[IRR], dist)       │
│   • {TICKER}_N8_IRR_IRR.md - IRR Narrative (executive summary)              │
│   • {TICKER}_KERNEL_RECEIPT_IRR.json - Execution proof (Pattern 13)         │
│                                                                             │
│ PATTERN: Bash Kernel (Pattern 6) - execute kernel via Bash, not manual calc │
│ PATTERN: Direct-Write (Pattern 1) - subagent writes to disk, returns paths  │
│ PATTERN: Kernel Receipts (Pattern 13) - verifiable proof of execution       │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: IRR T2 VALIDATOR                                                    │
│                                                                             │
│ ═══════════════════════════════════════════════════════════════════════════ │
│ TASK: Spawn Opus subagent to validate final IRR output                      │
│ ═══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ PROMPT FILE:                                                                │
│   validators/IRR_T2_VALIDATOR.md                                            │
│                                                                             │
│ INPUT FILES:                                                                │
│   • {analysis_dir}/09_IRR/{TICKER}_A14_IRR_ANALYSIS_IRR.json                │
│   • {analysis_dir}/09_IRR/{TICKER}_N8_IRR_IRR.md                            │
│   • {analysis_dir}/09_IRR/{TICKER}_A13_RESOLUTION_IRR.json (cross-validate) │
│   • {analysis_dir}/09_IRR/{TICKER}_KERNEL_RECEIPT_IRR.json                  │
│                                                                             │
│ VALIDATION CHECKS:                                                          │
│   • A.14 schema compliance (G3_2.2.5eIRR)                                   │
│   • Kernel receipt exists (Pattern 13: exit_code=0, timing present)         │
│   • Transition Factor analysis complete                                     │
│   • Null case IRR vs DR relationship is economically sensible               │
│   • All forks generated, probabilities sum to 1.0                           │
│   • ρ values from A.13 correctly applied                                    │
│   • Distribution statistics complete (E[IRR], P10-P90)                      │
│   • Values have 4+ decimal precision (proves real execution)                │
│   • N8 narrative present and coherent with A.14                             │
│                                                                             │
│ IF FAIL: Report issues. May need T2 re-execution.                           │
│ IF PASS: IRR stage complete. CVR is now State 5 (Expected Return).          │
│          Proceed to final CVR generation (generate_final_cvr.sh).           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Execution Commands (DEV: SMOKE TEST IRR {TICKER})

**Step 0: Auto-Discovery**
```bash
# Find most recent INTEGRATION output
find smoke_tests/ -path "*/08_INTEGRATION/*A7*.json" | sort -r | head -5

# Or check production
find production/analyses/ -path "*/08_INTEGRATION/*A7*.json" | sort -r | head -5

# Verify required files exist (with _INT suffix)
ls {analysis_dir}/08_INTEGRATION/{TICKER}_A2_ANALYTIC_KG_INT.json
ls {analysis_dir}/08_INTEGRATION/{TICKER}_A7_VALUATION_INT.json
ls {analysis_dir}/08_INTEGRATION/{TICKER}_A10_SCENARIO_INT.json

# Execute copy-forward (Pattern 12) before IRR T1
mkdir -p {analysis_dir}/09_IRR/
for f in {analysis_dir}/08_INTEGRATION/{TICKER}_*_INT.json; do
  base=$(basename "$f" | sed 's/_INT\.json$//')
  cp "$f" "{analysis_dir}/09_IRR/${base}_IRR.json"
done
for f in {analysis_dir}/08_INTEGRATION/{TICKER}_*_INT.md; do
  base=$(basename "$f" | sed 's/_INT\.md$//')
  cp "$f" "{analysis_dir}/09_IRR/${base}_IRR.md"
done
```

**Steps 1-4: Spawn Subagents**
Use Task tool with model="opus" for each step. See Stage Flow above for exact prompts and inputs.

### Critical Patterns Applied

| Pattern | Application |
|---------|-------------|
| Pattern 1: Direct-Write | T1/T2 subagents write to disk, return paths only |
| Pattern 3: Two-Shot | T1=analytical judgment, T2=kernel execution |
| Pattern 5: JSON Repair | T2 can repair malformed A.13 before kernel |
| Pattern 6: Bash Kernel | `python3 CVR_KERNEL_IRR_2.2.5e.py --a13 ... --inputs ... --output ...` |
| Pattern 7: Validators | Opus validator after T1 AND T2 |
| Pattern 8: Atomized Prompts | PROMPT + SCHEMAS + NORMDEFS + kernel |
| Pattern 10: Input Validation | READ individual _IRR.json files (copied from INT), verify E[IVPS]/DR |
| Pattern 12: Canonical Snapshot | 09_IRR/ contains complete artifact set with _IRR suffix |
| Pattern 13: Kernel Receipts | T2 generates {TICKER}_KERNEL_RECEIPT_IRR.json for reproducibility |

### IRR Stage Files

| File | Location | Purpose |
|------|----------|---------|
| G3_IRR_2.2.5e_PROMPT.md | prompts/irr/ | Core instructions (Sections I-V) |
| G3_IRR_2.2.5e_SCHEMAS.md | prompts/irr/ | JSON schemas (A.13, A.14) |
| G3_IRR_2.2.5e_NORMDEFS.md | prompts/irr/ | DSL & financial definitions (B.10-B.14) |
| CVR_KERNEL_IRR_2.2.5e.py | kernels/ | IRR kernel with CLI interface |
| IRR_T1_VALIDATOR.md | validators/ | T1 analytical validator |
| IRR_T2_VALIDATOR.md | validators/ | T2 kernel/final output validator |

### IRR Stage Atomized Files (CANONICAL)

| File | Purpose | Size |
|------|---------|------|
| `G3_IRR_2.2.5e_PROMPT.md` | Core instructions (Sections I-V) | 22KB |
| `G3_IRR_2.2.5e_SCHEMAS.md` | JSON schemas (A.13, A.14) | 10KB |
| `G3_IRR_2.2.5e_NORMDEFS.md` | DSL & financial definitions (B.10-B.14) | 20KB |
| `CVR_KERNEL_IRR_2.2.5e.py` | IRR kernel with CLI | 179KB |

**Key updates from 2.2.4e:**
- 4-file atomization (removed embedded kernel from prompt)
- CLI interface added to kernel for Pattern 6 compliance
- Version refs updated to G3_2.2.5eIRR
- INT compatibility updated to G3INT 2.2.3e

**Status:** CANONICAL - smoke tested 2024-12-22 (DAVE_ENRICH_SMOKE_20251220). G3_IRR_2_2_4e.md is HISTORICAL.

**Subagent loading:** Load all 3 prompt files. Kernel provided for T1 context, executed via Bash in T2.


---

# Stage: FINAL_CVR

# FINAL CVR Generation (Post-IRR)

> **Version:** 1.0.0
> **Extracted from:** Mega-patch plan Section 5
> **Pipeline Position:** Stage 9 of 9 (IRR → FINAL_CVR)

---

## Purpose

Generate the final human-readable CVR document ONCE, after the entire pipeline completes (post-IRR). This uses a Bash script, not Claude, to avoid truncation.

## What Goes In the Final CVR

**INCLUDE (in order):**
1. Header (ticker, date, E[IVPS], E[IRR], Pipeline Fit grade)
2. **N1:** Investment Thesis
3. **N2:** Invested Capital Modeling
4. **N3:** Economic Governor & Constraints
5. **N4:** Risk Assessment
6. **N5:** Enrichment Synthesis
7. **N6:** Scenario Model Synthesis
8. **N7:** Adjudication Synthesis
9. **N8:** IRR & Expected Return Analysis
10. **A.1-A.7:** Epistemic anchors through valuation
11. **A.10:** Scenario model
12. **A.12-A.14:** Integration trace, resolution timeline, IRR analysis

**EXCLUDE (remain in folder for audit trail):**
- RQ1-RQ7 (research inputs)
- A.8, A.9 (research plan/results)
- SC_* audits, A.11 (audit trail - findings already adjudicated into A.12)
- Kernel receipts (reproducibility artifacts)
- PIPELINE_STATE.md (orchestration state)

## Execution

```bash
# Run AFTER IRR stage completes
./workshop/scripts/generate_final_cvr.sh {TICKER} {analysis_dir}/09_IRR/
```

## Script Location

`workshop/scripts/generate_final_cvr.sh`

## Stage Flow

```
┌─────────────────────────────────────────────────────────────┐
│ FINAL_CVR (Bash Script - NO Claude)                         │
│    Input:  09_IRR/ folder with all _IRR artifacts           │
│    Script: workshop/scripts/generate_final_cvr.sh           │
│    Output: {TICKER}_FINAL_CVR.md (consolidated document)    │
│                                                             │
│    1. Concatenate N1-N8 narratives in order                 │
│    2. Embed A.1-A.7, A.10, A.12-A.14 as JSON blocks         │
│    3. Add header with summary metrics                       │
│    4. Write to {analysis_dir}/{TICKER}_FINAL_CVR.md         │
└─────────────────────────────────────────────────────────────┘
```

## Why Bash, Not Claude

1. **No truncation:** Bash `cat` preserves exact content
2. **Single concatenation:** No intermediate docs at each stage
3. **Curated content:** Final CVR contains analytical output, not working papers
4. **Audit trail preserved:** RQs, SC audits remain in folders for reproducibility

## Critical Patterns Applied

| Pattern | Application |
|---------|-------------|
| Pattern 11: Surgical Stitching | Concatenate from IRR outputs, no regeneration |
| Pattern 12: Canonical Snapshot | 09_IRR/ contains complete artifact set |


---

*End of auto-generated orchestration. Total stages: 9*
