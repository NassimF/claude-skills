---
name: literature-review
description: |
  Perform literature reviews for a research topic or paper. Searches academic databases (Semantic Scholar, arXiv, PubMed), categorizes papers into clusters, and maintains two living Excel files — "Paper Clusters" and "Paper Dictionary". Can also generate structured literature review reports with in-text citations. Use when the user provides a research topic or paper title to search, provides a directory of local papers to categorize, wants to manually add a paper by name/URL, or asks to generate or update a literature review report from existing papers.
---

# Literature Review

## Trigger Modes

Detect mode from user input. If ambiguous, ask.

| Mode | Trigger |
|---|---|
| **Search** | User gives a topic or paper title |
| **Local** | User gives a directory path containing papers |
| **Manual add** | User provides a paper name and/or URL to add |
| **Report** | User asks to generate/update the literature review report |

---

## Step 1 — Gather Inputs

Ask for optional inputs upfront. User can type `"none"` to accept defaults.

| Input | Question to ask | Default |
|---|---|---|
| Output path | "Where should I save the files? (or 'none' for `./literature-review/`)" | `./literature-review/` |
| Cluster names | "Do you have cluster names in mind? (or 'none' to auto-generate)" | Auto-generated |
| Main paper name | "What is the name of the main paper being reviewed? (or 'none')" | None → column becomes "Open Research Directions" |
| Search depth | "How many papers should I retrieve? Suggested: 20 (or 'none' for default 20)" | 20 |

Create the output directory if it doesn't exist.

---

## Step 2 — Paper Discovery

**Search mode:**
```bash
python3 scripts/paper_search.py search --query "<topic>" --limit <N>
```
- Returns JSON array of papers with: `name`, `url`, `date`, `authors`, `abstract`, `source`, `paywalled`
- Validate each paper URL:
  ```bash
  python3 scripts/paper_search.py validate --url "<url>"
  ```
  Returns `OK`, `PAYWALLED`, or `NOT_FOUND`. Note paywalled papers in the Dictionary with a `[PAYWALLED]` prefix on the URL.
- Read `references/apis.md` if search fails or you need to adjust query strategy.

**Local mode:** Read files from the directory. Extract title, authors, and date from content or filename.

**Manual add mode:**
1. Validate URL: `python3 scripts/paper_search.py validate --url "<url>"`
2. Check for duplicate:
   ```bash
   python3 scripts/excel_manager.py check-duplicate --output <output_dir> --name "<paper name>"
   ```
   Outputs `DUPLICATE` or `OK`. If duplicate, inform the user and stop.

---

## Step 3 — Clustering

- If user provided cluster names: use them exactly.
- Otherwise: analyze paper titles and abstracts, generate 4–8 meaningful cluster names.
- Assign each paper to one cluster.
- Count papers per cluster.

---

## Step 4 — Create/Update Excel Files

Prepare two JSON temp files, then run the scripts:

**Paper Clusters.xlsx:**
```bash
python3 scripts/excel_manager.py create-clusters \
  --topic "<topic or main paper name>" \
  --output <output_dir> \
  --clusters /tmp/clusters.json

# clusters.json format:
# [{"name": "...", "description": "...", "count": 3}, ...]

# To update an existing file:
python3 scripts/excel_manager.py update-clusters \
  --output <output_dir> --clusters /tmp/clusters.json
```

**Paper Dictionary.xlsx:**
```bash
python3 scripts/excel_manager.py create-dictionary \
  --topic "<topic or main paper name>" \
  --output <output_dir> \
  --papers /tmp/papers.json \
  [--no-main-paper]   # include this flag if no main paper was given

# papers.json format:
# [{"name": "...", "url": "...", "summary": "...", "date": "...",
#   "strengths": "...", "gaps": "...", "resolution": "..."}, ...]

# To update:
python3 scripts/excel_manager.py update-dictionary \
  --output <output_dir> --papers /tmp/papers.json
```

Fill all paper fields from the abstract and your analysis. Keep `summary` to 2–3 sentences. Be specific in `strengths` and `gaps`. Leave `resolution` blank (not "N/A") if no main paper was specified.

Both files are living documents — always append/update, never overwrite.

---

## Step 5 — Offer Report Generation

After creating or updating the Excel files, ask:

> "Would you like me to generate a literature review report based on the current papers? (or 'none' to skip)"

---

## Step 6 — Report Mode

1. **Ask for scope** (if not already known):
   - *Brief overview* (1–2 pages, high-level themes only)
   - *Standard review* (3–5 pages, cluster-by-cluster analysis)
   - *Comprehensive review* (7–10 pages, full synthesis + gap analysis)
   - *Comparative analysis* (focuses on conflicts, differences, and open problems)
   - Or `"none"` to skip.

2. **Ask for main paper** (if not already known):
   > "What is the main paper name for framing gaps and contributions? (or 'none')"

3. **Ask for export format:**
   > "Which format? `.md` / `.pdf` / `.html` (or 'none' for Markdown)"

4. **Write the report:**
   - Organize by cluster (one section per cluster)
   - Use in-text citations: `(Smith et al., 2023)`
   - Every cited paper must be real and present in the Paper Dictionary
   - End with a **References** section listing all cited papers with full citation info
   - All paper names, authors, and dates must match what is in the Excel files

5. Save the report to `<output_dir>/literature_review_report.<ext>`

---

## Notes

- **Paywalled papers:** Include them in both Excel files. Prefix their URL with `[PAYWALLED]`. Note in the summary that full text was unavailable.
- **Missing metadata:** If a field (date, authors) cannot be found, write `"Unknown"` rather than leaving blank.
- **Re-clustering:** If the user adds many new papers, offer to re-run clustering so cluster counts stay accurate.
- **API reference:** See `references/apis.md` for Semantic Scholar, arXiv, and PubMed details.
