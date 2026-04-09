---
paper-related-work
description: >
  Generate the Related Work section of a LaTeX research paper from a Excel literature file.
  Use this skill whenever the user asks to write, update, or regenerate their related work or background section,
  or when they mention updating the literature Excel and want the paper to reflect the changes.
  Also trigger when the user says "update background", "regenerate related work", "sync literature to paper",
  or references their categorized paper list. This skill reads the structured Excel file containing categorized
  papers with metadata, and produces a LaTeX \section or \subsection for Background/Related Work that can be
  pushed directly to the Overleaf-synced Git repository.
---

# Paper Related Work Generator

## Overview
This skill generates the **Background and Related Work** section of a NeurIPS-formatted LaTeX paper.
It reads from a living Excel file that contains categorized papers with metadata (title, authors, year,
venue, category, summary, link) and produces well-structured LaTeX output.

## Context: HippoRAG 2 Research
The current research is focused on reproducing and building upon **HippoRAG 2** (arXiv:2502.14802),
a non-parametric continual learning framework for LLMs that enhances RAG with knowledge graphs and
Personalized PageRank. Key topics for the related work include:
- Retrieval-Augmented Generation (RAG)
- Knowledge Graphs for LLMs
- Continual Learning / Non-Parametric Memory
- Multi-hop Reasoning
- Graph-based Retrieval (GraphRAG, LightRAG, RAPTOR)
- Dense vs Sparse Retrieval

## Inputs
1. **Excel file path**: Path to the living literature Excel file (`.xlsx`)
   - Required columns: `title`, `authors`, `year`, `venue`, `category`, `summary`, `bibtex_key`
   - Optional columns: `link`, `notes`, `relevance_score`
2. **BibTeX file path**: Path to `reference.bib` in the repo
3. **Output path**: Where to write the generated `.tex` file (e.g., `sections/related_work.tex`)
4. **Repo root**: Path to the Git-synced Overleaf repo

## Step-by-Step Workflow

### Step 1: Read and Parse the Excel File
```python
import openpyxl
# Read the Excel file, extract all rows into structured records
# Group papers by their 'category' column
# Sort categories by relevance or alphabetically
```

### Step 2: Organize by Category
Group the papers into subsections based on the `category` column. Typical categories might include:
- Retrieval-Augmented Generation
- Knowledge Graph-Enhanced Retrieval
- Continual Learning for LLMs
- Multi-hop Question Answering
- Graph-based Methods (PageRank, PPR)

### Step 3: Generate LaTeX
For each category, generate a `\subsection{}` with:
- An opening paragraph that frames why this area is relevant
- Citations for each paper using `\cite{bibtex_key}`
- A synthesis paragraph that connects papers within the category
- Transitions between subsections

The output should follow this structure:
```latex
\section{Related Work}
\label{sec:related_work}

% Opening paragraph framing the overall landscape

\subsection{Retrieval-Augmented Generation}
\label{subsec:rag}
% Synthesized discussion of RAG papers with \cite{} references

\subsection{Knowledge Graph-Enhanced Retrieval}
\label{subsec:kg-retrieval}
% Discussion of KG approaches

% ... more subsections based on categories in Excel
```

### Step 4: Update BibTeX
- Check `reference.bib` for any missing entries
- If papers in the Excel have a `bibtex` column, append missing entries to the .bib file
- Flag any papers that need manual BibTeX entries

### Step 5: Write and Integrate
1. Write the generated LaTeX to the output path (e.g., `sections/related_work.tex`)
2. Check if `main.tex` (or `neurips_2026.tex`) already has an `\input{sections/related_work}` line
3. If not, instruct the user on where to add it
4. Stage, commit, and push the changes:
```bash
cd <repo_root>
git add sections/background.tex reference.bib
git commit -m "Update related work section from literature review list"
git push
```

## Output Format
- Pure LaTeX, NeurIPS-compatible
- Use `\cite{}` for all references (not inline URLs)
- Use `\subsection{}` for each category
- Include `\label{}` on every section and subsection
- Keep paragraphs concise and synthesis-oriented (not just listing papers)

## Quality Guidelines
- **Synthesize, don't list**: Group related papers and discuss trends, not paper-by-paper summaries
- **Show gaps**: Identify what prior work doesn't address that motivates your research
- **Connect to your work**: End the section with a paragraph positioning HippoRAG 2 reproduction/extension
- **Be current**: Prioritize recent papers (2023-2026) while citing foundational work

## Git Integration
After generating the LaTeX:
```bash
cd <repo_root>
git add -A
git commit -m "Update: Related work section/ [$(date +%Y-%m-%d)]"
git push origin main
```
This push syncs automatically with Overleaf via the Git integration.

## Maintenance
Every time you update the Excel file with new papers:
1. Rerun this skill
2. The background section regenerates with the new papers included
3. Push to Git → Overleaf updates automatically

This keeps your writing in sync with your literature review at all times.

## Writing Style — Humanize Your Output
- **No AI tells.** Avoid: "notably", "importantly", "it is worth noting", "leveraging", "in recent years", "a growing body of", "comprehensive", "robust", "significant", "crucial", "facilitates", "utilizing", "delve into", "shed light on", "paradigm shift"
- **Vary sentence rhythm.** Mix short punchy sentences with longer ones. Academic writing has cadence — do not produce uniform sentence lengths.
- **Active voice.** "We propose" not "A method is proposed". "The model achieves" not "It can be observed that the model achieves".
- **Be direct.** Cut filler. "X outperforms Y by 4.2 F1" not "It is worth noting that X demonstrates a notable improvement of 4.2 F1 points over Y".
- **Sound human.** Write as a researcher explaining their work to a peer at a conference — confident, precise, occasionally opinionated. Not a textbook. Not a press release.
- **No bullet lists in the paper.** Everything must be flowing prose (except contribution lists in the intro).
- **NEVER add Co-Authored-By Claude or any AI attribution in commits or paper content.**
