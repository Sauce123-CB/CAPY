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
