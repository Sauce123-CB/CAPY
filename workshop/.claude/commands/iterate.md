# /iterate {TICKER} - Document failed/partial smoke test and update patches

Use after a **failed or partially successful** smoke test to capture findings and queue improvements.

## Required argument

- `{TICKER}`: The ticker from the smoke test (e.g., `DAVE`)

## Steps

### 1. Locate smoke test results

- Find most recent `analyses/{TICKER}_*/` in Production
- Or `smoke_tests/{TICKER}_*/` in Workshop
- Load `run_metadata.json` and validation results
- **Checkpoint:** Confirm correct run with user

### 2. Analyze failures

- Read validation output (WARN/FAIL items)
- Identify root causes:
  - Schema drift?
  - Missing fields?
  - Format errors?
  - Prompt ambiguity?
- Categorize by severity (CRITICAL / HIGH / MEDIUM / LOW)

### 3. Document findings in Workshop

- Create or update `patches/SESSION_LOG_{DATE}.md`:
  ```markdown
  ## Smoke Test: {TICKER} - {TIMESTAMP}

  **Result:** FAIL / PARTIAL

  **Issues Found:**
  1. [CRITICAL] Description...
  2. [HIGH] Description...

  **Root Cause Analysis:**
  - ...

  **Proposed Patches:**
  - Patch #{N}: Description
  ```

### 4. Update patch backlog

- Add new items to `patches/PATCH_TRACKER.md`:
  - Issue description
  - Priority (based on severity)
  - Target file(s)
  - Proposed fix
- If existing patch addresses the issue, update its priority/notes

### 5. Update TODO.md

- Add actionable items for next session
- Reference patch numbers

### 6. Sync both repos

- Commit Production smoke test results (if not already committed)
- Commit Workshop documentation updates
- Push both to GitHub

### 7. Report

- Summary of issues found
- Patches added/updated
- Recommended next steps

## Example

```
/iterate DAVE
```
