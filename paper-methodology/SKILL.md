---
name: paper-methodology
description: >
  Generate the Methodology section of a LaTeX research paper from architecture notes and method
  descriptions. Trigger when the user says "write methodology", "generate method section", "describe
  the approach", "write system design", or asks to explain how the system works in paper format.
  Outputs to sections/methodology.tex.
---

# Paper Methodology Generator

## When to Use
After the user has a clear understanding of their method — either from reproduction notes or from designing a new approach.

## Inputs Required
Ask the user for:
1. **Method description** — what does the system do, step by step?
2. **Key components** — what are the major modules or stages?
3. **What is novel vs borrowed** — which parts are from prior work, which are new?
4. **Any algorithms or equations** — pseudocode, formulas, key math
5. **Architecture figures** — if they have diagrams (optional)

## Writing Structure

**Opening paragraph (3-4 sentences)**
High-level overview of the full pipeline. A reader should understand the entire approach from this paragraph alone before diving into subsections.

**Subsection: Problem Formulation**
- Define notation: inputs, outputs, symbols
- Formal problem statement
- Keep it concise — 1 paragraph with key equations

**Subsection per major component**
For each component of the pipeline:
- What it does (purpose)
- How it works (mechanism)
- Why this design choice (justification)
- Reference prior work if building on existing methods

**Subsection: Key Design Decisions (optional)**
If there are non-obvious choices, explain them with brief justification.

## LaTeX Conventions

**For algorithms:**
```latex
\begin{algorithm}[t]
\caption{Algorithm Name}
\label{alg:name}
\begin{algorithmic}[1]
\REQUIRE Input description
\ENSURE Output description
\STATE Step 1
\STATE Step 2
\IF{condition}
    \STATE Step 3
\ENDIF
\RETURN result
\end{algorithmic}
\end{algorithm}
```

**For equations:**
```latex
\begin{equation}
    \text{score}(p) = \alpha \cdot f(p) + (1-\alpha) \cdot g(p)
    \label{eq:scoring}
\end{equation}
```

**For figures:**
```latex
\begin{figure}[t]
    \centering
    \includegraphics[width=\linewidth]{figures/pipeline.pdf}
    \caption{Overview of our approach. [Describe what each part shows.]}
    \label{fig:pipeline}
\end{figure}
```

## Writing Rules
- ~2 to 2.5 pages in two-column format (methodology is typically the longest section)
- Define all notation before using it
- Clearly distinguish what is existing work vs your contribution
- Use `\paragraph{Step 1: Name.}` for fine-grained structure within subsections
- Include at least one algorithm box or equation
- Reference figures when describing the pipeline
- Be precise enough that someone could reimplement from this section

## Output
Write to `sections/methodology.tex`. Git add, commit, push.

## Writing Style — Humanize Your Output
- **No AI tells.** Avoid: "notably", "importantly", "it is worth noting", "leveraging", "in recent years", "a growing body of", "comprehensive", "robust", "significant", "crucial", "facilitates", "utilizing", "delve into", "shed light on", "paradigm shift"
- **Vary sentence rhythm.** Mix short punchy sentences with longer ones. Academic writing has cadence — do not produce uniform sentence lengths.
- **Active voice.** "We propose" not "A method is proposed". "The model achieves" not "It can be observed that the model achieves".
- **Be direct.** Cut filler. "X outperforms Y by 4.2 F1" not "It is worth noting that X demonstrates a notable improvement of 4.2 F1 points over Y".
- **Sound human.** Write as a researcher explaining their work to a peer at a conference — confident, precise, occasionally opinionated. Not a textbook. Not a press release.
- **No bullet lists in the paper.** Everything must be flowing prose (except contribution lists in the intro).
- **NEVER add Co-Authored-By Claude or any AI attribution in commits or paper content.**
