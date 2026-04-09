---
name: paper-setup
description: >
  Set up a LaTeX paper project with per-section .tex files. Trigger when the user says "set up
  paper structure", "split my tex file into sections", "create section files", "set up Overleaf
  repo", "initialize paper", or asks to organize a LaTeX project for collaborative or skill-based
  writing. This skill creates stub .tex files for each section and inserts \input{} lines into the
  main .tex file without modifying existing content.
---

# Paper Structure Setup

## What This Skill Does
Takes a LaTeX project with a single `.tex` file and sets it up for per-section writing:
1. Creates a `sections/` folder with one `.tex` stub per section
2. Creates a `figures/` folder
3. Inserts `\input{sections/...}` lines into the main `.tex` file before `\end{document}`
4. Adds commonly needed LaTeX packages if missing
5. Does NOT modify or delete any existing content

## When to Use
- Starting a new paper project
- Setting up an Overleaf repo cloned via Git
- Preparing a project for per-section Claude Code skills

## How to Use

### Prompt Examples
The user might say:
- "Set up my paper with these sections: introduction, related work, methodology, experiments, results, discussion, conclusion"
- "Split my NeurIPS template into section files"
- "Initialize paper structure for my Overleaf repo at /path/to/repo"

### What to Ask the User
1. **Repo path** — where is the LaTeX project?
2. **Section names** — what sections do they want? Use underscores for multi-word names.

If the user does not specify sections, suggest this standard set:
```
introduction, related_work, methodology, experimental_setup, results, discussion, conclusion
```

### Run the Script
```bash
bash [path/to/setup_paper_structure.sh] <repo_path> <section1> <section2> ...
```

Example:
```bash
bash setup_paper_structure.sh ~/Neurips introduction related_work methodology experimental_setup results discussion conclusion
```

### What the Script Does Step by Step

**Step 1: Auto-detect the main .tex file**
Scans `*.tex` files in the repo for the one containing `\begin{document}`.

**Step 2: Create `sections/` and `figures/` directories**

**Step 3: Create section stub files**
For each section name, creates `sections/<name>.tex` with:
```latex
% =============================================================================
% SECTION NAME (uppercased)
% =============================================================================
\section{Section Name}
\label{sec:section_name}

% TODO: Add content for this section
```
Underscores in names are converted to spaces and title-cased for the `\section{}` title.
Example: `related_work` → `\section{Related Work}`

**Step 4: Insert `\input{}` lines**
Adds a block before `\end{document}` in the main `.tex` file:
```latex
% ── PAPER SECTIONS (auto-generated) ──────────────────────────────────────────
\input{sections/introduction}
\input{sections/related_work}
\input{sections/methodology}
...
% ─────────────────────────────────────────────────────────────────────────────
```
If `\input{sections/` already exists, this step is skipped (safe to run twice).

**Step 5: Add missing packages**
Checks for and adds if missing: `booktabs`, `algorithm`, `algorithmic`.

**Step 6: Stage for git**
Runs `git add` on all new and modified files.

### After Running
Tell the user:
```
git commit -m "Add per-section paper structure"
git push
```
Then verify it compiles on Overleaf.

## Important Notes
- The script does NOT create a backup file
- The script does NOT modify or delete existing content in the .tex file
- The script only inserts `\input{}` lines — the user removes default template content when ready
- The script is idempotent — safe to run multiple times
- Section order in the `\input{}` block matches the order passed as arguments