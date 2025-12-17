# /sync - Sync all CAPY repos to GitHub

Synchronize Workshop, Production, and Archive repos with their GitHub remotes.

## Steps

1. **Check status of all three repos:**
   - `CAPY_Workshop`: git status + ahead/behind
   - `CAPY_Production`: git status + ahead/behind
   - `CAPY_Archive`: git status + ahead/behind

2. **Report findings:**
   - Uncommitted changes (list files)
   - Unpushed commits (count + summaries)
   - Behind remote (need to pull)

3. **If there are uncommitted changes, ask user:**
   - Stage and commit now?
   - What commit message?
   - Or skip this repo?

4. **Push all repos that are ahead:**
   - Workshop → origin/master
   - Production → origin/master
   - Archive → origin/master

5. **Report final status:**
   - All synced ✓
   - Or list any issues

## Notes

- Never force push
- Always show what will be pushed before pushing
- If conflicts exist, stop and report (don't auto-resolve)
