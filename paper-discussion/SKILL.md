---
name: paper-discussion
description: >
  Generate the Discussion section of a LaTeX research paper. Trigger when the user says "write
  discussion", "analyze results", "discuss findings", "write limitations", or asks to interpret
  results, discuss implications, or outline future work. Outputs to sections/discussion.tex.
---

# Paper Discussion Generator

## When to Use
After results are complete. This section interprets what the results mean, acknowledges limitations, and suggests future directions.

## Inputs Required
1. Read `sections/results.tex` — what did we find?
2. Read `sections/methodology.tex` — what did we do?
3. Ask the user:
   - What surprised you in the results?
   - What are the known limitations of the approach?
   - What would you do next if you had more time?

## Writing Structure

**Paragraph 1-2: Key Findings Interpreted**
Go beyond restating numbers. Explain *why* the results look the way they do. Connect findings to design decisions from the methodology.

Example: Instead of "We achieve 52.4 F1", write "The 4.2-point improvement on multi-hop tasks suggests that iterative PPR re-seeding effectively recovers evidence that single-pass traversal misses, particularly for 3-4 hop questions where standard PPR signal attenuates."

**Paragraph 3: Unexpected or Nuanced Findings**
Discuss results that were surprising, mixed, or require nuance. This shows intellectual honesty and depth.

**Paragraph 4-5: Limitations**
Be direct and specific. Common categories:
- Scope: what datasets, domains, or scales were not tested
- Method: known failure modes or assumptions
- Evaluation: what the metrics do not capture
- Cost: computational requirements or dependencies

Do not hide limitations — reviewers will find them. Being upfront builds credibility.

**Paragraph 6: Future Work**
2-3 concrete directions, each with a brief justification for why it matters. Avoid vague statements like "we will explore more datasets." Instead: "Extending iterative re-seeding to conversational settings, where the query evolves across turns, would test whether the graph structure supports episodic memory."

## Writing Rules
- ~0.5 to 1 page in two-column format
- Interpret, do not restate results
- Be honest about limitations — this builds trust with reviewers
- Future work should be specific and actionable
- Cite related work when connecting findings to broader trends
- Do not introduce new results in the discussion

## Output
Write to `sections/discussion.tex`. Git add, commit, push.

## Writing Style — Humanize Your Output
- **No AI tells.** Avoid: "notably", "importantly", "it is worth noting", "leveraging", "in recent years", "a growing body of", "comprehensive", "robust", "significant", "crucial", "facilitates", "utilizing", "delve into", "shed light on", "paradigm shift"
- **Vary sentence rhythm.** Mix short punchy sentences with longer ones. Academic writing has cadence — do not produce uniform sentence lengths.
- **Active voice.** "We propose" not "A method is proposed". "The model achieves" not "It can be observed that the model achieves".
- **Be direct.** Cut filler. "X outperforms Y by 4.2 F1" not "It is worth noting that X demonstrates a notable improvement of 4.2 F1 points over Y".
- **Sound human.** Write as a researcher explaining their work to a peer at a conference — confident, precise, occasionally opinionated. Not a textbook. Not a press release.
- **No bullet lists in the paper.** Everything must be flowing prose (except contribution lists in the intro).
- **NEVER add Co-Authored-By Claude or any AI attribution in commits or paper content.**
