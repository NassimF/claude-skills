---
name: paper-experimental-setup
description: >
  Generate the Experimental Setup section of a LaTeX research paper. Trigger when the user says
  "write experimental setup", "describe the experiments", "write setup section", or asks to document
  datasets, baselines, metrics, or hyperparameters. This section describes HOW experiments were run,
  not the results. Outputs to sections/experimental_setup.tex.
---

# Paper Experimental Setup Generator

## When to Use
After methodology is drafted and before results. This section documents everything a reader needs to reproduce the experiments.

## Inputs Required
Ask the user for:
1. **Datasets** — name, size, split, source, what task they test
2. **Baselines / compared methods** — what are we comparing against?
3. **Metrics** — what do we measure? (F1, EM, Recall@k, etc.)
4. **Implementation details** — models used, hardware, hyperparameters
5. **Evaluation protocol** — how are metrics computed? any special procedures?

## Writing Structure

**Subsection: Datasets**
For each dataset, one paragraph covering:
- Name and citation
- What it tests (factual QA, multi-hop reasoning, etc.)
- Size (number of queries, corpus size)
- Why we chose it

Use a table if there are 4+ datasets:
```latex
\begin{table}[t]
\caption{Dataset statistics.}
\label{tab:datasets}
\centering
\small
\begin{tabular}{lccc}
\toprule
\textbf{Dataset} & \textbf{Queries} & \textbf{Corpus} & \textbf{Task} \\
\midrule
MuSiQue & 2,417 & 24K & Multi-hop QA \\
\bottomrule
\end{tabular}
\end{table}
```

**Subsection: Baselines**
List each compared method with a one-sentence description and citation. Group them logically (e.g., dense retrievers, graph-based methods, iterative methods).

**Subsection: Evaluation Metrics**
Define each metric precisely. For example:
- Passage Recall@k: percentage of queries where at least one supporting passage appears in top-k
- F1: token-level overlap between predicted and gold answers
- EM: exact match after normalization

**Subsection: Implementation Details**
- Models: which LLM, which embedder, specific versions
- Hardware: GPU type, memory
- Hyperparameters: learning rate, PPR damping factor, number of retrieved passages, etc.
- Runtime: how long does indexing/inference take
- Code availability: mention if releasing code

## Writing Rules
- ~1 page in two-column format
- Be precise enough for reproduction — exact model names, versions, seeds
- Cite the source for every dataset and baseline method
- Use consistent terminology with the methodology section
- Do not discuss results here — only setup
- Use tables for dense information (datasets, hyperparameters)

## Output
Write to `sections/experimental_setup.tex`. Git add, commit, push.

## Writing Style — Humanize Your Output
- **No AI tells.** Avoid: "notably", "importantly", "it is worth noting", "leveraging", "in recent years", "a growing body of", "comprehensive", "robust", "significant", "crucial", "facilitates", "utilizing", "delve into", "shed light on", "paradigm shift"
- **Vary sentence rhythm.** Mix short punchy sentences with longer ones. Academic writing has cadence — do not produce uniform sentence lengths.
- **Active voice.** "We propose" not "A method is proposed". "The model achieves" not "It can be observed that the model achieves".
- **Be direct.** Cut filler. "X outperforms Y by 4.2 F1" not "It is worth noting that X demonstrates a notable improvement of 4.2 F1 points over Y".
- **Sound human.** Write as a researcher explaining their work to a peer at a conference — confident, precise, occasionally opinionated. Not a textbook. Not a press release.
- **No bullet lists in the paper.** Everything must be flowing prose (except contribution lists in the intro).
- **NEVER add Co-Authored-By Claude or any AI attribution in commits or paper content.**
