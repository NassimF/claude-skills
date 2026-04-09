---
name: paper-abstract
description: >
  Generate the Abstract of a LaTeX research paper from the complete draft of all other sections.
  Trigger when the user says "write abstract", "generate abstract", "summarize the paper", or
  asks to finalize the paper. This is the LAST skill to run — after all 7 sections are complete.
  Outputs directly into the main .tex file (e.g., neurips_2026.tex) between \begin{abstract}
  and \end{abstract}.
---

# Paper Abstract Generator

## When to Use
The very last thing you write. All 7 sections must be complete first.

## Inputs Required
Read all existing section files:
- `sections/introduction.tex` — problem, gap, contributions
- `sections/related_work.tex` — landscape
- `sections/methodology.tex` — what we did
- `sections/experimental_setup.tex` — how we tested
- `sections/results.tex` — key numbers
- `sections/discussion.tex` — interpretation, limitations
- `sections/conclusion.tex` — takeaway

## Writing Structure (150-250 words)

Write exactly 5 components, each 1-2 sentences:

**1. Problem and Motivation**
Why does this matter? What is the core challenge?

**2. Gap**
What do existing approaches fail at? One specific limitation.

**3. Our Approach**
What do we do? One sentence describing the method at the highest level.

**4. Key Results**
2-3 concrete numbers. Pick the most impressive and the most representative.

**5. Significance**
One sentence on what this enables or what it means for the field.

## Writing Rules
- 150 to 250 words (strict for most venues)
- Self-contained: a reader must understand the paper from the abstract alone
- No citations — do not use `\cite{}` in the abstract
- No undefined acronyms — define RAG, LLM, KG on first use or avoid them entirely
- No vague claims — every sentence must be concrete
- At least one specific quantitative result
- Do not start with "In this paper, we..."  — start with the problem
- Every sentence must earn its place — no filler

## Output Location
The abstract goes inside the main `.tex` file, not in `sections/`. Find the main `.tex` file that has `\begin{document}`, then replace the content between `\begin{abstract}` and `\end{abstract}`.

## After Generation
1. Update the abstract in the main `.tex` file
2.  Git add, commit,  and ask the user if you should push too