---
name: overleaf-setup
description: >
  Set up an Overleaf project as a Git submodule inside a parent repo. Creates the parent repo
  folder structure (overleaf/ as parent, assets/ as submodule), populates it with a conference
  template zip, generates sync/push/status helper scripts, and writes an instructions file.
  Also supports re-parenting: moving an existing Overleaf submodule to a different parent repo.
  Trigger when user says "set up overleaf submodule", "add overleaf to my project",
  "overleaf git setup", "re-parent overleaf", or invokes /overleaf-setup.
---

# Overleaf Setup

## Overview

Two modes:
- **Fresh setup** — clone Overleaf project as `assets/` submodule inside a new or existing parent repo, populate with conference template
- **Re-parent** — move an existing `assets/` submodule to a different parent repo

Determine which mode the user wants before proceeding.

---

## Mode 1: Fresh Setup

### Step 1 — Collect inputs

Ask the user for all of the following before starting:

1. **Zip file path** — conference template (e.g. NeurIPS, ICML, ICLR)
2. **Overleaf project URL** — `https://git.overleaf.com/<project-id>`
3. **Overleaf token** — warn the user: _do not paste the token in the chat_. Tell them you will store it securely in `~/.git-credentials` and it will never appear in any tracked file. Ask them to provide it only when you confirm you are ready to store it.
4. **Parent repo path** (optional) — absolute path to use as the parent repo. If omitted, proceed to Step 2b.
5. **Project name** — used as the folder name if creating a new parent repo
6. **Conference name** — used in the initial commit message (e.g. "NeurIPS 2026")
7. **Push template to Overleaf now?** — yes/no. If yes, push the extracted zip contents to Overleaf immediately after setup.

### Step 2a — Resolve parent repo (path provided)

```bash
git -C <path> rev-parse --is-inside-work-tree 2>/dev/null
```
- Already a git repo: use it as-is.
- Not a git repo: run `git init <path>`.

### Step 2b — Resolve parent repo (no path provided)

Run the bundled discovery script:
```bash
python /root/.claude/skills/overleaf-setup/scripts/find_git_repos.py <current-working-dir>
```
- **Repos found** → present the list and ask the user to pick one, or choose to create a new one.
- **None found** → use the project name from Step 1 to create a new folder in the current directory, then `git init` it.

### Step 3 — Configure credential store

```bash
git config --global credential.helper store
echo "https://git:<token>@git.overleaf.com" >> ~/.git-credentials
```

The token must NOT appear in `.gitmodules` or any tracked file.

### Step 4 — Add Overleaf submodule

From inside the parent repo root:
```bash
git submodule add https://git@git.overleaf.com/<project-id> assets
```

### Step 5 — Extract zip into submodule

```bash
unzip -o <zip-path> -d <parent-repo>/assets
cd <parent-repo>/assets
git add .
git commit -m "Initialize with <conference> template"
```

If the user chose to push immediately:
```bash
git push origin master
```

### Step 6 — Copy helper scripts

Copy the three bundled scripts into the parent repo root:
```bash
cp /root/.claude/skills/overleaf-setup/assets/check_status.sh <parent-repo>/
cp /root/.claude/skills/overleaf-setup/assets/sync_overleaf.sh <parent-repo>/
cp /root/.claude/skills/overleaf-setup/assets/push_to_overleaf.sh <parent-repo>/
chmod +x <parent-repo>/check_status.sh <parent-repo>/sync_overleaf.sh <parent-repo>/push_to_overleaf.sh
```

### Step 7 — Create instructions file

Write `<parent-repo>/Overleaf sync instructions.md`:

```markdown
# Overleaf Sync Instructions

## Step 1: Check status before anything

Always run this first when starting a session:

    ./check_status.sh

- No local changes and no unpushed commits → safe to run `./sync_overleaf.sh`
- Local commits ahead → run `./push_to_overleaf.sh` first
- Conflicts → resolve manually before syncing

## Pull changes from Overleaf → local

    # Default: "Update Overleaf submodule - <date>"
    ./sync_overleaf.sh

    # Custom message:
    ./sync_overleaf.sh "Your message here"

## Push local changes → Overleaf

    # Default: "Update from local - <date>"
    ./push_to_overleaf.sh

    # Custom message:
    ./push_to_overleaf.sh "Your message here"

## Note: Remotes

- The `assets/` submodule has Overleaf as its remote — LaTeX files sync here.
- The parent repo has no remote and is local only unless connected to GitHub.
```

### Step 8 — Commit everything

```bash
cd <parent-repo>
git add .gitmodules assets check_status.sh sync_overleaf.sh push_to_overleaf.sh "Overleaf sync instructions.md"
git commit -m "Add Overleaf submodule and sync scripts"
```

Confirm success and summarize what was created.

---

## Mode 2: Re-parent

Move an existing Overleaf `assets/` submodule from one parent repo to another. In the new parent repo, everything is organized inside an `overleaf/` subfolder:

```
<new-parent-repo>/
├── (other repo contents)
└── overleaf/
    ├── assets/                       ← submodule
    ├── check_status.sh
    ├── sync_overleaf.sh
    ├── push_to_overleaf.sh
    └── Overleaf sync instructions.md
```

### Step 1 — Collect inputs

1. **Current parent repo path** — absolute path to the existing parent repo
2. **New parent repo path** — absolute path to an existing repo, or ask for a project name to create a new one
3. **Overleaf project URL** — `https://git.overleaf.com/<project-id>`
4. **Overleaf token** — confirm whether it is already in `~/.git-credentials`; if not, store it (same as Mode 1 Step 3)

### Step 2 — Remove submodule from old parent

```bash
cd <old-parent-repo>
git submodule deinit assets
git rm assets
rm -rf .git/modules/assets
git commit -m "Remove Overleaf submodule"
```

If the old parent had the submodule inside an `overleaf/` subfolder, adjust the path accordingly (e.g. `git submodule deinit overleaf/assets`).

### Step 3 — Resolve new parent repo

- If path provided and is a git repo: use it as-is.
- If path provided but not a git repo: `git init <path>`.
- If no path: run `find_git_repos.py`, present list, or create new repo using project name.

### Step 4 — Create `overleaf/` subfolder and add submodule

```bash
mkdir -p <new-parent-repo>/overleaf
cd <new-parent-repo>
git submodule add https://git@git.overleaf.com/<project-id> overleaf/assets
```

### Step 5 — Copy helper scripts into `overleaf/`

```bash
cp /root/.claude/skills/overleaf-setup/assets/check_status.sh <new-parent-repo>/overleaf/
cp /root/.claude/skills/overleaf-setup/assets/sync_overleaf.sh <new-parent-repo>/overleaf/
cp /root/.claude/skills/overleaf-setup/assets/push_to_overleaf.sh <new-parent-repo>/overleaf/
chmod +x <new-parent-repo>/overleaf/*.sh
```

### Step 6 — Create instructions file in `overleaf/`

Write `<new-parent-repo>/overleaf/Overleaf sync instructions.md` — same content as Mode 1 Step 7.

### Step 7 — Commit

```bash
cd <new-parent-repo>
git add .gitmodules overleaf/
git commit -m "Add Overleaf submodule under overleaf/"
```

Confirm success.

---

## Key constraints

- Overleaf only exposes a single `master` branch — no branching on the Overleaf side.
- Token must never appear in `.gitmodules`.
- `assets/` is the submodule; the parent folder is named by the user (default: `overleaf/`).
- All three `.sh` scripts belong in the parent repo root, not inside `assets/`.
