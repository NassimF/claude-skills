# claude-skills

A personal collection of Claude Code skills — modular packages that extend Claude with specialized workflows, tools, and domain knowledge.

## Available Skills

- [Latex Report Generator](#latex-report-generator)
- [Skill Creator](#skill-creator)
- [Literature Review](#literature-review)

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
