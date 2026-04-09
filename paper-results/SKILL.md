---
name: paper-results
description: >
  Generate the Results section of a LaTeX research paper from experimental data (CSV, JSON, or
  raw numbers). Trigger when the user says "write results", "generate results tables", "format
  results for paper", "update numbers", or provides experimental output to turn into LaTeX tables.
  Outputs to sections/results.tex.
---

# Paper Results Generator

## When to Use
After experiments are run and you have numbers. This skill turns raw results into formatted LaTeX tables with analysis prose.

## Inputs Required
1. **Result files** — CSV, JSON, or raw numbers the user provides
2. **What tables to generate** — which comparisons, which metrics
3. **Reference tables** — if reproducing a paper, which original tables are we matching?
4. Read `sections/experimental_setup.tex` to ensure consistency

## Writing Structure

For each table or group of results:

**1. The Table**
```latex
\begin{table}[t]
\caption{Descriptive caption that includes the metric, reader model, and what varies.}
\label{tab:descriptive-name}
\centering
\small
\begin{tabular}{l|ccccc|c}
\toprule
\textbf{Method} & \textbf{Dataset1} & \textbf{Dataset2} & ... & \textbf{Avg.} \\
\midrule
Baseline 1 & 45.2 & 67.3 & ... & 56.3 \\
Baseline 2 & 48.1 & 69.0 & ... & 58.6 \\
\midrule
Our Method & \textbf{52.4} & \textbf{73.1} & ... & \textbf{62.8} \\
\bottomrule
\end{tabular}
\end{table}
```

**2. Analysis prose (1-2 paragraphs after each table)**
- State the main finding: "Our method achieves the highest average F1 of 62.8, outperforming the strongest baseline by 4.2 points."
- Explain patterns: "The improvement is most pronounced on multi-hop datasets (MuSiQue, 2Wiki), where graph traversal provides the largest benefit."
- Note exceptions honestly: "On single-hop QA (NQ, PopQA), dense retrieval remains competitive."

## Table Formatting Rules
- `\textbf{}` for the best result in each column
- `\underline{}` for the second-best result
- Use `\toprule`, `\midrule`, `\bottomrule` from booktabs (no `\hline`)
- Include an Avg. column when comparing across datasets
- Use `\small` or `\footnotesize` for wide tables
- Consistent decimal places within each metric (1 decimal for F1/EM, 1 for Recall)
- Align numbers on decimal point when possible

## Section Structure
```latex
\section{Results}
\label{sec:results}

\subsection{Main Results}
% Primary comparison table + analysis

\subsection{Retrieval Performance}
% Recall@k table + analysis (if applicable)

\subsection{Ablation Studies}
% What happens when we remove components? (if applicable)
```

## Writing Rules
- ~1.5 to 2 pages in two-column format
- State findings as facts, not opinions
- Always contextualize numbers: "52.4 F1, a 4.2-point improvement over..."
- Be honest about where the method does not help
- Reference tables in text: "As shown in Table~\ref{tab:name}"
- Do not re-explain the setup — that is in experimental setup
- Compare against the same baselines listed in experimental setup

## Output
Write to `sections/results.tex`. Git add, commit, push.

## Writing Style — Humanize Your Output
- **No AI tells.** Avoid: "notably", "importantly", "it is worth noting", "leveraging", "in recent years", "a growing body of", "comprehensive", "robust", "significant", "crucial", "facilitates", "utilizing", "delve into", "shed light on", "paradigm shift"
- **Vary sentence rhythm.** Mix short punchy sentences with longer ones. Academic writing has cadence — do not produce uniform sentence lengths.
- **Active voice.** "We propose" not "A method is proposed". "The model achieves" not "It can be observed that the model achieves".
- **Be direct.** Cut filler. "X outperforms Y by 4.2 F1" not "It is worth noting that X demonstrates a notable improvement of 4.2 F1 points over Y".
- **Sound human.** Write as a researcher explaining their work to a peer at a conference — confident, precise, occasionally opinionated. Not a textbook. Not a press release.
- **No bullet lists in the paper.** Everything must be flowing prose (except contribution lists in the intro).
- **NEVER add Co-Authored-By Claude or any AI attribution in commits or paper content.**
