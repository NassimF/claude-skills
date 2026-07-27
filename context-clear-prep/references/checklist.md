# Context Clear Prep — Audit Checklist

Work through every category. For each item, note: ✅ OK / ⚠️ needs update / N/A.

---

## 1. Specs files

Look for `specs/` directory in the current project root.

- **roadmap.md**: Are all completed tasks marked `[x]`? Does each completed phase have a Notes block documenting deviations, findings, or gotchas? Are any phases marked ⏳ that are actually done?
- **tech-stack.md**: Do directory paths match what actually exists on disk? Are model names, conda env names, and tool versions current?
- **mission.md**: Does it still reflect the project goal? (rarely needs updating)
- **Feature spec dirs** (`specs/YYYY-MM-DD-*/`): Are plan.md checkboxes accurate? Any requirements or validation items that need updating based on what actually happened?

If there is a `CLAUDE.md` in the project root, check if it references paths or configs that have changed.

---

## 2. Git state

Run `git status` and `git log --oneline -5`.

- Any **modified files** not staged? Should they be committed or discarded?
- Any **untracked files** that belong in the repo? (scripts, spec files, output files)
- Any **untracked files** that should NOT be in the repo? (large data, model weights, secrets — add to `.gitignore` instead)
- Is the current **branch** correct? (should be on a feature branch if mid-phase, or master if between phases)

---

## 3. .gitignore

Check the `.gitignore` file (create if missing).

Common items that should be ignored but often aren't:
- Large datasets / audio / video files (`*.flac`, `*.mp4`, `*.wav`, `data/raw/`)
- Model weights and checkpoints (`*.pt`, `*.pth`, `*.bin`, `*.safetensors`, `exp/`, `dump/`)
- HuggingFace cache dirs (`.cache/`)
- Python artifacts (`__pycache__/`, `*.pyc`, `.eggs/`, `dist/`, `*.egg-info/`)
- Secrets and credentials (`.env`, `*.key`, `credentials.json`)
- OS artifacts (`.DS_Store`, `Thumbs.db`)
- IDE files (`.vscode/`, `.idea/`)
- Log files that are auto-generated (but keep manually written `.md` logs)

---

## 4. Changelog

Check if `CHANGELOG.md` exists in the project root.

- If it exists: run `git log --oneline` and compare against the changelog. Are recent commits missing?
- If it doesn't exist but the project has multiple commits: note it as optional (don't create automatically without user approval — some projects don't use changelogs).
- If the `/changelog` skill is available, note that it can be used to sync the changelog.

---

## 5. Memory files

Find the project memory directory: `~/.claude/projects/<hash>/memory/MEMORY.md`.

The hash is derived from the working directory path. Check `ls ~/.claude/projects/` to find the right one (match by project name in the path).

Check:
- Does `MEMORY.md` have an entry for **current phase status**? Is it accurate?
- Are there entries for **key decisions made this session** that a future Claude wouldn't know from reading the code?
- Are there **stale entries** (e.g., phase marked in-progress that is now done)?
- Is there anything **non-obvious** from this session worth preserving? (e.g., workarounds applied, compatibility fixes, why a tool was bypassed)

Do NOT save:
- Things derivable from reading the code or git history
- Ephemeral task details only relevant to this session
- Debugging steps that led to a fix (the fix is already in the code)

---

## 6. Output summary format

Present findings like this:

```
**Specs**
- roadmap.md: Phase 2 checkboxes not ticked ⚠️
- tech-stack.md: OK ✅

**Git**
- 3 untracked files in data/kaldi/ — should commit ⚠️
- data/raw/ (43 GB) — should be in .gitignore ⚠️

**.gitignore**
- Missing: data/raw/, *.flac, exp/ ⚠️

**Changelog**
- No CHANGELOG.md — N/A

**Memory**
- project_status.md: Phase 2 marked pending, should be done ⚠️
- No entry for ESPnet Kaldi bypass workaround — worth saving ⚠️
```

Then ask for approval before writing anything.
