---
name: paper-introduction
description: >
  Generate the Introduction section of a LaTeX research paper. Trigger when the user says
  "write introduction", "generate intro", "update introduction", or asks to frame/motivate
  the paper. This skill should run AFTER related work and results are drafted. Outputs to
  sections/introduction.tex.
---

# Paper Introduction Generator

## When to Use
After `paper-related-work` and `paper-results` are complete. The introduction references the landscape and previews findings.

## Inputs Required
Ask the user for:
1. **Research problem** — one sentence
2. **Key gap** — what existing work fails to do
3. **Our approach** — what we propose, one sentence
4. **Main result** — best number to highlight
5. Read `sections/related_work.tex` and `sections/results.tex` if they exist

## Writing Structure

**Paragraph 1 — Big Picture (3-4 sentences)**
Why this research area matters. Do not start with "In recent years." Start with the core challenge. Narrow to the specific technical area.

**Paragraph 2 — Current Dominant Approach (3-4 sentences)**
The standard method and what it does well. Cite 2-3 foundational works.

**Paragraph 3 — The Gap (3-4 sentences)**
What current approaches fail at. Cite concrete numbers or failure modes. Make the gap feel urgent.

**Paragraph 4 — Our Approach (3-4 sentences)**
High-level description of what we do. Key insight only — technical details go in methodology.

**Paragraph 5 — Contributions**
```latex
Our main contributions are as follows:
\begin{itemize}
    \item Concrete, verifiable contribution 1
    \item Concrete, verifiable contribution 2
    \item Concrete, verifiable contribution 3
\end{itemize}
```

## Writing Rules
- 1 to 1.5 pages in two-column format
- Every factual claim needs `\cite{}`
- No subjective language — let numbers speak
- First person plural: "we propose", "we show"
- No forward references to nonexistent figures or tables

## Output
Write to `sections/introduction.tex`. Git add, commit, push.

## Writing Style — Humanize Your Output
- **No AI tells.** Avoid: "notably", "importantly", "it is worth noting", "leveraging", "in recent years", "a growing body of", "comprehensive", "robust", "significant", "crucial", "facilitates", "utilizing", "delve into", "shed light on", "paradigm shift"
- **Vary sentence rhythm.** Mix short punchy sentences with longer ones. Academic writing has cadence — do not produce uniform sentence lengths.
- **Active voice.** "We propose" not "A method is proposed". "The model achieves" not "It can be observed that the model achieves".
- **Be direct.** Cut filler. "X outperforms Y by 4.2 F1" not "It is worth noting that X demonstrates a notable improvement of 4.2 F1 points over Y".
- **Sound human.** Write as a researcher explaining their work to a peer at a conference — confident, precise, occasionally opinionated. Not a textbook. Not a press release.
- **No bullet lists in the paper.** Everything must be flowing prose (except contribution lists in the intro).
- **NEVER add Co-Authored-By Claude or any AI attribution in commits or paper content.**
