---
name: changelog
description: Maintains CHANGELOG.md in the project root with date-based headings, one bullet per commit. Invoke with /changelog before merging to sync all commits not yet listed in the file. Skips merge commits. Preserves all existing changelog content exactly. Trigger when user types /changelog or asks to update the changelog.
---

# Changelog

Run the bundled script from the project root, then report what was added.

The script lives in this skill's own `scripts/` directory. Substitute the
absolute path to wherever this skill is installed (e.g.
`~/.claude/skills/changelog/scripts/update_changelog.py`) for `<skill-dir>`
below — do not hardcode another user's home directory.

## Steps

1. Run the script (from the project root; it takes no arguments):
   ```bash
   python <skill-dir>/scripts/update_changelog.py
   ```
2. Report what the script printed (dates added and commit count).
3. If `CHANGELOG.md` is new, offer to commit it. If it already existed, leave committing to the user.

## Script behaviour

- Reads all non-merge commits via `git log --no-merges`
- Detects already-listed hashes by scanning lines matching `- … (abc1234)`
- Groups new commits by date, newest first: `## YYYY-MM-DD` heading + `- {subject} ({hash})` bullets
- Prepends new sections above existing content; never rewrites existing lines
- Prints a one-line summary or "already up to date"

## Error handling

If the script fails (not a git repo, no commits), show the error and stop — do not attempt to write the file manually.
