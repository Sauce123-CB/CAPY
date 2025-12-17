# CAPY Changelog

Chronological log of all patching sessions, infrastructure changes, and decisions.

---

## 2024-12-15: Initial Organization Session

**Participants:** Benjamin + Claude Code

**Duration:** ~2 hours

### Problem Statement
- 23 files in flat directory structure
- No version control
- No separation between prompt dev and production runs
- No collaboration infrastructure
- File naming issues (spaces, `(1)` suffixes)
- CLAUDE.md only covered pipeline orchestration, not prompt development

### Decisions Made

1. **Three-folder architecture**
   - Workshop: prompt development, patching, smoke tests
   - Production: running analyses on companies
   - Archive: cold storage for old versions
   - *Rationale:* Folder determines mode - eliminates dispatcher ambiguity

2. **GitHub for version control**
   - Three private repos created
   - Dropbox + Git coexist (Dropbox syncs, Git versions)
   - *Rationale:* Team collaboration, history tracking, rollback capability

3. **HHMMSS timestamps in folder names**
   - Format: `{TICKER}_{YYYYMMDD}_{HHMMSS}`
   - *Rationale:* Supports 100s of runs per day per ticker

4. **Three version labels per prompt**
   - CANONICAL (smoke tested, production-ready)
   - EXPERIMENTAL (WIP, untested)
   - HISTORICAL (previous canonical, rollback option)
   - *Rationale:* Max 3 versions in Workshop, older goes to Archive

5. **Prompts vs Outputs separation**
   - Prompt templates → `prompts/` folder (including rq_gen, silicon_council, hitl_audit)
   - Run outputs → numbered stage folders in each analysis (04_RQ, 05_SC, 06_HITL)
   - *Rationale:* Separation of concerns - templates vs artifacts

6. **HYBRID architecture for now**
   - Human orchestrates RQ/SC/HITL steps manually
   - Future AUTO CAPY mode planned
   - *Rationale:* Not ready for full automation; need smoke test first

7. **User checkpoint prompts in Workshop CLAUDE.md**
   - DEV: APPLY PATCH asks autonomous vs checkpoint mode
   - DEV: MARK CANONICAL requires confirmation at each step
   - *Rationale:* User may want different levels of control

8. **Production CLAUDE.md marked as DRAFT**
   - v0.1.0 with checklist for v1.0
   - *Rationale:* Instructions are scaffolding only; need full smoke test

### Files Created
- `CAPY_Workshop/CLAUDE.md` (234 lines)
- `CAPY_Production/CLAUDE.md` (283 lines)
- `CAPY_Archive/CLAUDE.md` (63 lines)
- `CAPY_Workshop/patches/PATCH_TRACKER.md`
- `CAPY_Workshop/patches/CHANGELOG.md` (this file)

### Files Reorganized
- 23 files from flat structure → Workshop subfolders
- Fixed: `CVR_KERNEL_INT_2_2_2e (1).py` → `CVR_KERNEL_INT_2_2_2e.py`
- Fixed: `CVR_KERNEL_IRR_2_2_4e (1).py` → `CVR_KERNEL_IRR_2_2_4e.py`
- Fixed: `DAVE BASE OUTPUT.md` → `DAVE_BASE_OUTPUT.md`

### Git Commits
- Workshop: `b26e6e9` - Initial commit: CAPY Workshop v0.1.0
- Production: `5c9b04c` - Initial commit: CAPY Production v0.1.0 (DRAFT)
- Archive: `f590a84` - Initial commit: CAPY Archive v0.1.0

### Open Items for Next Session
- [ ] Move prompts from `orchestration/` to `prompts/rq_gen/`, `prompts/silicon_council/`, `prompts/hitl_audit/`
- [ ] Add collaborators to GitHub repos
- [ ] Run first smoke test using new Workshop CLAUDE.md
- [ ] Begin applying 2.2.2e patches

---

## 2024-12-15: Source Library Addition (continued session)

**Participants:** Benjamin + Claude Code

### Changes Made

1. **Added `source_library/` to Production**
   - Location: `CAPY_Production/source_library/{TICKER}/`
   - Purpose: Pre-staging area for researcher uploads
   - Files: PDFs, extracted markdown, page images

2. **Added `SOURCE: UPLOAD {TICKER}` command**
   - Auto-creates company folder
   - Organizes uploaded files
   - Generates INVENTORY.md per company

3. **Updated `CAPY: INIT` command**
   - Now copies from `source_library/{TICKER}/` instead of working directory
   - Prompts user if source folder missing

### Rationale
- Researchers can upload company documents independently
- Documents persist between analysis runs
- Clean separation: upload → organize → analyze

---

## Template for Future Entries

```markdown
## YYYY-MM-DD: Session Title

**Participants:**
**Duration:**

### Problem/Goal

### Decisions Made

### Changes Made

### Git Commits

### Open Items
```
