# /promote {PROMPT_FILE} - Promote experimental prompt to canonical

Use after a **successful** smoke test to promote an EXPERIMENTAL prompt to CANONICAL status.

## Required argument

- `{PROMPT_FILE}`: The experimental prompt file to promote (e.g., `BASE_T1_REFINE_v1_2.md`)

## Steps

### 1. Validate preconditions

- [ ] Confirm the file exists and is marked EXPERIMENTAL
- [ ] Locate the most recent smoke test that used this prompt
- [ ] Verify smoke test result was PASS (check `run_metadata.json`)
- [ ] **Checkpoint with user** before proceeding

### 2. Update Workshop

- [ ] Update `CLAUDE.md` Current Canonical Versions table
- [ ] Remove "(EXPERIMENTAL)" label from the promoted file's entry
- [ ] If previous CANONICAL exists, mark it as HISTORICAL
- [ ] If old HISTORICAL exists, move to `CAPY_Archive/`
- [ ] Update `patches/PATCH_TRACKER.md` - mark relevant patch as DEPLOYED

### 3. Deploy to Production

- [ ] Copy promoted file to `CAPY_Production/prompts/{stage}/`
- [ ] Update Production's `CLAUDE.md` if it tracks versions

### 4. Document success

- [ ] Create entry in `patches/SESSION_LOG_{DATE}.md` if one exists for today
- [ ] Or add note to `CHANGELOG.md`

### 5. Sync both repos

- [ ] Commit Workshop changes
- [ ] Commit Production changes
- [ ] Push both to GitHub

### 6. Report

- Summary of what was promoted
- New canonical version
- Links to smoke test that validated it

## Example

```
/promote BASE_T1_REFINE_v1_2.md
```
