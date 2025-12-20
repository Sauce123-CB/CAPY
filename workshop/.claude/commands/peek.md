# /peek - Cross-Context Reference

**Usage:** `/peek [target]`

Temporarily look into another context without switching.

---

## Targets

### `/peek production`
Show what's deployed in production:
1. List `../production/prompts/` by stage
2. Show most recent analysis run in `../production/analyses/`
3. Report any version mismatches with workshop CANONICAL

### `/peek production prompts`
List all production prompt files with versions.

### `/peek production sources {TICKER}`
List source documents for a ticker:
```
ls ../production/source_library/{TICKER}/
```

### `/peek production run {TICKER}`
Find most recent production run for ticker:
```
find ../production/analyses/ -name "*{TICKER}*" -type d | sort | tail -1
```
Then show its `pipeline_state.json`.

### `/peek shared`
Read `../shared/PATTERNS.md` and `../shared/BRIDGE.md`.

### `/peek patches`
Show pending patches from `patches/PATCH_TRACKER.md`.

---

## Implementation

When user invokes `/peek {target}`:

1. **Do NOT change context** - stay in workshop
2. **Read the requested files** from sibling directory
3. **Report findings** concisely
4. **Return to current work** without switching

---

## Examples

**User:** `/peek production prompts`
**Claude:** Reads `../production/prompts/*/` and reports file list.

**User:** `/peek production sources DAVE`
**Claude:** Lists `../production/source_library/DAVE/` contents.

**User:** `/peek production run DAVE`
**Claude:** Finds most recent DAVE analysis, shows pipeline state.
