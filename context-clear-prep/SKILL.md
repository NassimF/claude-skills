---
name: context-clear-prep
description: Prepares the current project for a context window clear. Run when the user says "prepare for context clear", "ready for context wipe", "clean up before compacting", "/context-clear-prep", or asks to save everything before losing context. Audits specs files, git state, .gitignore, changelogs, and memory files; presents a summary of needed changes; asks for user approval; then applies all changes and commits. Ends by confirming everything is saved and ready for context clear.
---

# Context Clear Prep

Audit the current project state, present a summary of needed changes, get user approval, apply changes, and confirm readiness for context clear.

## Workflow

### Step 1 — Audit (read only, no writes)

Read `references/checklist.md` and work through every category. Collect all findings without writing anything yet.

### Step 2 — Present summary and ask for approval

Present findings grouped by category as a concise bullet list or table. Then use AskUserQuestion with three options:

- **Apply all** — proceed with everything found
- **Apply with modifications** — ask what to skip or change before proceeding
- **Skip** — do nothing

Do not write any files before the user responds.

### Step 3 — Apply changes (only after approval)

Apply in this order:
1. Update specs files (roadmap checkboxes, Notes blocks, path corrections)
2. Update `.gitignore` if needed
3. Stage and commit all project changes (`git add` specific files, not `-A`)
4. Update `CHANGELOG.md` if it exists and is behind commits
5. Update memory files — add/update entries for current phase status and non-obvious decisions

### Step 4 — Final confirmation

Run `git status` to confirm a clean working tree. Then tell the user:

> **Ready for context clear.** All specs are up to date, changes are committed, and memory is saved. You can safely wipe the context now.

## Rules

- Never write files before Step 2 approval
- If "Apply with modifications" is chosen, clarify what to change before proceeding
- Commit messages follow project conventions — check `git log --oneline -3` for style
- Memory updates go to the project memory dir — read `MEMORY.md` first to avoid duplicates
- If no git repo exists, skip all git steps and say so
- Read `references/checklist.md` for the full per-category audit checklist
