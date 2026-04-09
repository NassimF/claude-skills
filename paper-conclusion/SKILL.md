---
name: paper-conclusion
description: >
  Generate the Conclusion section of a LaTeX research paper. Trigger when the user says "write
  conclusion", "generate conclusion", "wrap up the paper", or asks to summarize the paper.
  This is the LAST section to write. Outputs to sections/conclusion.tex.
---

# Paper Conclusion Generator

## When to Use
Last section to write. All other sections should be complete.

## Inputs Required
Read all existing section files:
- `sections/introduction.tex` — problem and contributions
- `sections/results.tex` — key findings
- `sections/discussion.tex` — limitations and future work

## Writing Structure

**Paragraph 1: Restate the Problem and Approach (3-4 sentences)**
Briefly restate what problem we addressed and what our approach was. Do not copy from the introduction — rephrase with the benefit of having presented the full paper.

**Paragraph 2: Summarize Key Results (3-4 sentences)**
Highlight the most important quantitative results. Pick 2-3 numbers that tell the story. Connect them to the contributions promised in the introduction.

**Paragraph 3: Broader Impact and Forward Look (2-3 sentences)**
What does this work enable? What is the next step for the field? End on a concrete, forward-looking note — not vague optimism.

## Writing Rules
- ~0.5 page in two-column format (conclusions are short)
- Do not introduce new information or results
- Do not repeat the abstract verbatim — this is a different summary written for a reader who has read the entire paper
- Mirror the contributions from the introduction — show they were delivered
- End with a strong final sentence
- No citations needed unless referencing a specific future direction

## Output
Write to `sections/conclusion.tex`. Git add, commit, push.

## Writing Style — Humanize Your Output
- **No AI tells.** Avoid: "notably", "importantly", "it is worth noting", "leveraging", "in recent years", "a growing body of", "comprehensive", "robust", "significant", "crucial", "facilitates", "utilizing", "delve into", "shed light on", "paradigm shift"
- **Vary sentence rhythm.** Mix short punchy sentences with longer ones. Academic writing has cadence — do not produce uniform sentence lengths.
- **Active voice.** "We propose" not "A method is proposed". "The model achieves" not "It can be observed that the model achieves".
- **Be direct.** Cut filler. "X outperforms Y by 4.2 F1" not "It is worth noting that X demonstrates a notable improvement of 4.2 F1 points over Y".
- **Sound human.** Write as a researcher explaining their work to a peer at a conference — confident, precise, occasionally opinionated. Not a textbook. Not a press release.
- **No bullet lists in the paper.** Everything must be flowing prose (except contribution lists in the intro).
- **NEVER add Co-Authored-By Claude or any AI attribution in commits or paper content.**
