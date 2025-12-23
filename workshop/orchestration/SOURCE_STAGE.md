# SOURCE Stage Orchestration

> **Version:** 1.0.1
> **Pipeline Position:** Stage 0 of 9 (PDF → SOURCE → BASE)
> **Created:** 2024-12-23

## SOURCE Stage Overview

The SOURCE stage handles PDF preprocessing - converting raw PDF documents into machine-readable text and images for analysis.

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
│  │   Check ../production/source_library/{TICKER}/ for:                  │   │
│  │   - *.pdf files                                                       │   │
│  │   - Missing *.extracted.md files (need preprocessing)                 │   │
│  │                                                                       │   │
│  │   If no PDFs found → ABORT with message                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STEP 2: TEXT EXTRACTION (pdfplumber)                                 │   │
│  │                                                                       │   │
│  │   For each PDF without .extracted.md:                                │   │
│  │   - Open with pdfplumber                                             │   │
│  │   - Extract text from each page                                      │   │
│  │   - Write to {filename}.extracted.md                                 │   │
│  │                                                                       │   │
│  │   Format:                                                             │   │
│  │   # {filename}                                                        │   │
│  │   Extracted: {ISO-8601 timestamp}                                     │   │
│  │   --- Page 1 ---                                                      │   │
│  │   {page text}                                                         │   │
│  │   --- Page 2 ---                                                      │   │
│  │   ...                                                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STEP 3: IMAGE EXTRACTION (pdf2image)                                 │   │
│  │                                                                       │   │
│  │   For each PDF without _pages/ directory:                            │   │
│  │   - Convert pages to PNG at 150 DPI                                  │   │
│  │   - Save to {filename}_pages/page_001.png, page_002.png, ...         │   │
│  │                                                                       │   │
│  │   Purpose: Visual analysis of charts, tables, presentations          │   │
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
│  ../production/source_library/{TICKER}/                                     │
│  ├── {filename}.pdf                    ← Original PDF (unchanged)          │
│  ├── {filename}.extracted.md           ← Text extraction                   │
│  ├── {filename}_pages/                 ← Page images                       │
│  │   ├── page_001.png                                                      │
│  │   ├── page_002.png                                                      │
│  │   └── ...                                                               │
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

## Implementation Code (MANDATORY - DO NOT IMPROVISE)

**CRITICAL:** Use this exact Python code. Do NOT substitute with `pdftotext` or other tools.

```python
import pdfplumber
from pdf2image import convert_from_path
from pathlib import Path
from datetime import datetime

def extract_text(pdf_path: Path) -> str:
    """Extract text from PDF using pdfplumber."""
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            text_parts.append(f"--- Page {i} ---\n{text}")
    return "\n\n".join(text_parts)

def extract_images(pdf_path: Path, output_dir: Path) -> int:
    """Convert PDF pages to PNG images at 150 DPI."""
    output_dir.mkdir(parents=True, exist_ok=True)
    images = convert_from_path(pdf_path, dpi=150)
    for i, img in enumerate(images, 1):
        img.save(output_dir / f"page_{i:03d}.png", "PNG")
    return len(images)

def preprocess_pdf(pdf_path: Path) -> dict:
    """Full preprocessing: text extraction + image extraction."""
    # Text extraction
    text = extract_text(pdf_path)
    md_path = pdf_path.with_suffix(".extracted.md")
    md_path.write_text(f"# {pdf_path.stem}\n\nExtracted: {datetime.now().isoformat()}\n\n{text}")

    # Image extraction
    img_dir = pdf_path.parent / f"{pdf_path.stem}_pages"
    page_count = extract_images(pdf_path, img_dir)

    return {"text_file": md_path, "image_dir": img_dir, "pages": page_count}

# Usage: For each PDF in source_library/{TICKER}/
for pdf_path in Path("source_library/{TICKER}").glob("*.pdf"):
    if not pdf_path.with_suffix(".extracted.md").exists():
        result = preprocess_pdf(pdf_path)
        print(f"Processed: {pdf_path.name} -> {result['pages']} pages")
```

**Execution:** Run this Python code via Bash tool. Both text AND image extraction are REQUIRED.

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
