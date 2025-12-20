# /peek - Cross-Context Reference

**Usage:** `/peek [target]`

Temporarily look into another context without switching.

---

## Targets

### `/peek workshop`
Show what's in development:
1. List EXPERIMENTAL prompts in `../workshop/prompts/`
2. Show pending patches from `../workshop/patches/PATCH_TRACKER.md`
3. Report recent smoke tests

### `/peek workshop prompts`
List all workshop prompt files with status (CANONICAL/EXPERIMENTAL).

### `/peek workshop patches`
Show pending patches:
```
Read ../workshop/patches/PATCH_TRACKER.md
```

### `/peek workshop smoke {TICKER}`
Find recent smoke tests for ticker:
```
ls ../workshop/smoke_tests/{TICKER}_* | sort | tail -3
```

### `/peek workshop patterns`
Read orchestration patterns:
```
Read ../workshop/orchestration/ORCHESTRATION_KEY_PATTERNS.md
```

### `/peek shared`
Read `../shared/PATTERNS.md` and `../shared/BRIDGE.md`.

---

## Implementation

When user invokes `/peek {target}`:

1. **Do NOT change context** - stay in production
2. **Read the requested files** from sibling directory
3. **Report findings** concisely
4. **Return to current work** without switching

---

## Examples

**User:** `/peek workshop prompts`
**Claude:** Reads `../workshop/prompts/*/` and reports EXPERIMENTAL files.

**User:** `/peek workshop patches`
**Claude:** Shows pending patch items.

**User:** `/peek shared`
**Claude:** Shows shared patterns and bridge doc.
