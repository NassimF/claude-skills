# claude-skills

A personal collection of Claude Code skills — modular packages that extend Claude with specialized workflows, tools, and domain knowledge.

## Available Skills

- [Latex Report Generator](#latex-report-generator)
- [Skill Creator](#skill-creator)
- [Literature Review](#literature-review)
- [Paper Skills](#paper-skills)
  - [Paper Setup](#paper-setup)
  - [Paper Abstract](#paper-abstract)
  - [Paper Introduction](#paper-introduction)
  - [Paper Related Work](#paper-related-work)
  - [Paper Methodology](#paper-methodology)
  - [Paper Experimental Setup](#paper-experimental-setup)
  - [Paper Results](#paper-results)
  - [Paper Discussion](#paper-discussion)
  - [Paper Conclusion](#paper-conclusion)

---

## Skills

### Latex Report Generator

Generates and maintains a LaTeX changelog report from git commits. Each commit is appended as a structured entry, making the report a living document that accumulates over the project lifetime. Compiles to PDF automatically.

**Features:**
- Accumulates commit entries like a changelog — never overwrites existing entries
- Auto-detects the appropriate report file based on commit content (bugfixes, API changes, architecture, general)
- Supports multiple reports per project (one per concern)
- Applies a custom `.tex` template when creating a new report
- Compiles PDF via `pdflatex` (falls back to `latexmk`)
- Commits and pushes the updated `.tex` and `.pdf` automatically
- Includes a `PostToolUse` hook (`check-git-commit.sh`) that auto-triggers the skill after every `git commit`

**Input arguments** (all optional):
| Argument | Description | Default |
|---|---|---|
| `--repo <url>` | Remote git repo URL to clone or pull | Current working directory |
| `--report <path>` | Path (relative to repo root) of the `.tex` file to update | Auto-selected based on commit content |
| `--template <path>` | Path to a `.tex` template to use when creating a new report | Built-in default structure |

---

### Skill Creator

A guided workflow for creating new Claude Code skills from scratch or improving existing ones. Walks through understanding requirements, planning resources, scaffolding the skill directory, writing SKILL.md, and packaging into a distributable `.skill` file.

**Features:**
- Structured 6-step creation process: understand → plan → init → edit → package → iterate
- `init_skill.py` scaffolds a new skill directory with SKILL.md template and example resource folders
- `package_skill.py` validates the skill structure and packages it into a `.skill` zip file
- `quick_validate.py` checks frontmatter format, required fields, naming conventions, and description quality
- Includes design pattern guides for progressive disclosure, multi-step workflows, and output formatting
- Reference files: `workflows.md` (sequential/conditional patterns), `output-patterns.md` (template and example patterns)

**Input arguments:**

`init_skill.py`:
| Argument | Description |
|---|---|
| `<skill-name>` | Hyphen-case skill name (e.g. `my-skill`) |
| `--path <dir>` | Output directory where the skill folder will be created |

`package_skill.py`:
| Argument | Description | Default |
|---|---|---|
| `<path/to/skill-folder>` | Path to the skill directory to package | Required |
| `[output-directory]` | Where to save the `.skill` file | Current directory |

---

### Literature Review

Performs structured literature reviews for a research topic or paper. Discovers relevant papers from academic databases, clusters them into meaningful categories, and maintains two living Excel files throughout the project. Can generate a formatted literature review report with in-text citations on demand.

**Features:**
- **Four modes:** Search (topic/title → database query), Local (directory of papers → categorize), Manual add (name + URL → append to files), Report (generate literature review from existing papers)
- Searches Semantic Scholar, arXiv, and PubMed simultaneously and deduplicates results
- Validates paper URLs/DOIs; flags paywalled papers with a `[PAYWALLED]` prefix
- Auto-generates cluster names from paper content, or uses user-specified names
- Produces two living Excel files that are updated (never overwritten) on each run:
  - **Paper Clusters.xlsx** — cluster name, description, paper count
  - **Paper Dictionary.xlsx** — paper name, URL, summary, date, strengths, gaps, how the main paper resolves gaps (or "Open Research Directions" if no main paper is given)
- Detects and prevents duplicate entries across runs
- Generates a literature review report organized by cluster, with in-text citations `(Smith et al., 2023)` and a full references section
- Report export formats: `.md`, `.pdf`, `.html`

**Input arguments** (all optional — Claude asks for each and accepts `"none"` for defaults):
| Input | Description | Default |
|---|---|---|
| Topic / paper title | Research topic or main paper to review | Required to start |
| Output path | Where to save the `literature-review/` folder | `./literature-review/` |
| Cluster names | User-defined cluster names | Auto-generated from paper content |
| Main paper name | The primary paper being reviewed (frames the "gaps resolved" column) | None → column becomes "Open Research Directions" |
| Search depth | Number of papers to retrieve | 20 |
| Report scope | Brief (1–2p) / Standard (3–5p) / Comprehensive (7–10p) / Comparative | Asked when report is requested |
| Export format | `.md` / `.pdf` / `.html` | `.md` |

**Dependencies:** `pip install openpyxl requests`

---

## Paper Skills

A comprehensive suite of nine modular skills for writing research papers in LaTeX. Each skill handles one section and outputs directly to the paper repository. Designed to work with Overleaf via Git integration.

**Recommended execution order:**
1. Setup → 2. Related Work → 3. Methodology → 4. Experimental Setup → 5. Results → 6. Introduction → 7. Discussion → 8. Conclusion → 9. Abstract

### Paper Setup

Initializes a LaTeX project for per-section writing. Creates a `sections/` directory, generates `.tex` stub files for each section, and inserts `\input{}` lines into the main `.tex` file without modifying existing content. Idempotent—safe to run multiple times.

**Inputs:**
| Input | Description |
|---|---|
| Repo path | Path to the LaTeX project directory |
| Section names | Comma-separated section names (e.g., `introduction, related_work, methodology, experimental_setup, results, discussion, conclusion`) |

---

### Paper Abstract

Generates a concise abstract (150–250 words) from a complete paper draft. Reads all other section files and synthesizes them into 5 components: problem, gap, approach, results, significance. Must be run **last**, after all other sections are complete.

**Inputs:**
| Input | Description |
|---|---|
| All section .tex files | Read from `sections/introduction.tex`, `related_work.tex`, `methodology.tex`, etc. |

---

### Paper Introduction

Writes the Introduction section framing the research problem, existing solutions, the gap, and the proposed approach. Must be run after Related Work and Results are drafted, as it references the landscape and previews key findings.

**Inputs:**
| Input | Description |
|---|---|
| Research problem | One-sentence problem statement |
| Key gap | What existing approaches fail to address |
| Approach description | High-level overview of the proposed method |
| Main result | Best quantitative finding to highlight |
| Existing sections | Reads `related_work.tex` and `results.tex` if available |

---

### Paper Related Work

Generates the Background and Related Work section from a categorized Excel literature file. Reads papers from an Excel sheet (title, authors, year, venue, category, summary), organizes them by category, generates LaTeX with citations, and updates the BibTeX file.

**Inputs:**
| Input | Description |
|---|---|
| Excel file path | Path to literature spreadsheet (required columns: `title`, `authors`, `year`, `venue`, `category`, `summary`, `bibtex_key`) |
| BibTeX file path | Path to `reference.bib` |
| Output path | Where to write `related_work.tex` (default: `sections/related_work.tex`) |

---

### Paper Methodology

Describes the system design and technical approach. Generates subsections for problem formulation, each major component, and design decisions. Includes support for algorithms, equations, and figures with proper LaTeX conventions.

**Inputs:**
| Input | Description |
|---|---|
| Method description | Step-by-step overview of the system |
| Key components | Names and purposes of major modules |
| Novel vs. borrowed | Which parts are new contributions |
| Algorithms / equations | Pseudocode, formulas, or key math (optional) |
| Architecture figures | Diagrams (optional) |

---

### Paper Experimental Setup

Documents datasets, baselines, metrics, hyperparameters, and evaluation protocols. Describes **how** experiments were run, not the results. Includes tables for dense information and precise reproduction instructions.

**Inputs:**
| Input | Description |
|---|---|
| Datasets | Name, size, split, source, what task they test |
| Baselines | Methods to compare against |
| Metrics | What is measured (F1, EM, Recall@k, etc.) |
| Implementation details | Models, hardware, hyperparameters, versions |
| Evaluation protocol | How metrics are computed |

---

### Paper Results

Converts experimental data (CSV, JSON, or raw numbers) into formatted LaTeX tables with analysis prose. Highlights best results, provides comparisons across datasets, and contextualizes numbers with interpretation paragraphs.

**Inputs:**
| Input | Description |
|---|---|
| Result files | CSV, JSON, or raw numbers from experiments |
| Which tables | Comparisons, metrics, and ablation studies to show |
| Reference tables | If reproducing a paper, cite the original tables |

---

### Paper Discussion

Interprets results, acknowledges limitations, discusses implications, and suggests future work. Must be run after Results and Methodology are complete. Explains *why* results look the way they do and what the method cannot do.

**Inputs:**
| Input | Description |
|---|---|
| Existing sections | Reads `results.tex` and `methodology.tex` |
| User insights | What surprised you? Known limitations? Next steps? |

---

### Paper Conclusion

Writes the final section: restate problem, summarize key results, and discuss broader impact. Must be run **last**, after Introduction, Results, and Discussion are complete. Mirrors contributions from the introduction.

**Inputs:**
| Input | Description |
|---|---|
| Existing sections | Reads `introduction.tex`, `results.tex`, `discussion.tex` |

