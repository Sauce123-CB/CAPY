# SOURCE Stage Orchestration

> **Version:** 1.0.0
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

## Implementation Reference

See `workshop/CLAUDE.md` section "Source Document Commands" for full implementation code.

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
