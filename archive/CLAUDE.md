# CAPY Archive - Cold Storage

> **Version:** 0.2.0
> **Last reviewed:** 2024-12-19
> **Review cadence:** Monthly

This workspace stores **old versions** of prompts, kernels, smoke tests, and analyses.

For **active development**, use `../workshop/`.
For **production runs**, use `../production/`.

---

## Folder Structure

```
archive/
├── prompts/       # Old prompt versions (older than HISTORICAL)
├── kernels/       # Old kernel versions
├── smoke_tests/   # Old test runs (>30 days)
├── analyses/      # Old production analyses (optional archival)
└── patches/       # Historical patch notes and changelogs
```

---

## Commands

### ARCHIVE: LIST

List archived items by category:
- Prompts (grouped by stage)
- Kernels (grouped by stage)
- Smoke tests (by date)
- Analyses (by ticker and date)

### ARCHIVE: RETRIEVE {FILENAME}

Copy a specific archived file back to Workshop for reference.
Does not delete from archive.

### ARCHIVE: SEARCH {QUERY}

Search archive for files matching query (filename or content grep).

---

## Archival Policy

Files are moved here during monthly cleanup:
- Prompt/kernel versions older than HISTORICAL
- Smoke tests older than 30 days
- Production analyses older than 90 days (optional)

**Nothing is deleted from Archive** - it's permanent storage.

---

## Notes

- Archive is git-tracked for history
- Large binary files (PDFs, images) may be gitignored
- If Archive grows too large, consider offloading to cloud storage

---

## Checkpoint Protocol

**Default behavior: Checkpoint before retrieval or deletion.**

When performing archive operations:
1. **Confirm file identity** before retrieving (show metadata)
2. **Verify destination** before copying files
3. **Never delete** without explicit user confirmation
