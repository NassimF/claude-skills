---
name: init-specs
description: Create a project's "constitution" — the core spec files mission.md, tech-stack.md, and roadmap.md — inside a specs/ directory. Use when the user wants to initialize project specs, scaffold a specs/constitution, set up mission/tech-stack/roadmap files, plan out project phases, or asks to "init specs" / run the init-specs skill. Works for a brand-new project or to formalize an existing one.
---

# Init Specs

Create a project's **constitution**: three spec files under a `specs/` directory —
`mission.md`, `tech-stack.md`, and `roadmap.md`.

## Workflow (follow in order)

### 1. Get the project description

The whole constitution is derived from a description of the project. Obtain it before anything else:

- Ask the user **either** to point to a description **file** (e.g. a README, a brief, a `CLAUDE.md`,
  a doc path) **or** to write the description directly in the chat.
- Read the file if given; otherwise use the pasted text.
- If a strong description source already exists in the project (e.g. `CLAUDE.md`, `README.md`),
  offer it as the default so the user can just confirm.

Do not proceed until there is a concrete description to work from.

### 2. Draft the three files internally (do NOT write to disk yet)

From the description, draft the content for each file:

- **`mission.md`** — what the project is, who it's for, the problem it solves, the goal/deliverable,
  and success criteria / non-negotiable requirements. The "why" and "what", not the "how".
- **`tech-stack.md`** — the concrete technologies, languages, frameworks, key libraries, models,
  data sources, and infra the project uses. Prefer specifics (pinned versions where known).
- **`roadmap.md`** — the high-level implementation order **in very small phases of work**. Each
  phase should be a small, independently completable, verifiable chunk (not a big milestone). Use a
  checkbox list so progress can be tracked, e.g.:

  ```markdown
  # Roadmap

  - [ ] Phase 1: <one small, concrete deliverable>
  - [ ] Phase 2: <the next small chunk>
  - [ ] Phase 3: ...
  ```

  Keep phases granular — if a phase feels like it bundles several distinct tasks, split it.

### 3. Confirm with the user via AskUserQuestion (REQUIRED — before writing to disk)

**Important:** You MUST call the `AskUserQuestion` tool, with the questions **grouped** to cover all
three files, **before** writing anything to disk. This is a hard requirement — never write the files
without this confirmation step.

Group the questions into a single `AskUserQuestion` call (one question per file, grouped together) so
the user reviews mission, tech-stack, and roadmap in one pass. For each, present your drafted
direction and let the user confirm or adjust — for example:

- **Mission** — confirm the goal/scope/success criteria you drafted (or revise).
- **Tech stack** — confirm the technology choices (or swap/add/remove).
- **Roadmap** — confirm the phase breakdown and granularity (or resplit / reorder).

Offer sensible options based on your drafts, and make your recommended option first (label it
"(Recommended)"). Users can always pick "Other" to give custom input. Incorporate the answers.

### 4. Write the files

After the user answers, create the `specs/` directory (if missing) and write the three files:

```
specs/
├── mission.md
├── tech-stack.md
└── roadmap.md
```

Use the description path/text plus the confirmed answers as the source of truth. Keep each file
focused and concise. Then briefly report what was written and where.

## Notes

- Default location is `specs/` at the project root unless the user specifies otherwise.
- If any of the three files already exist, show what exists and confirm before overwriting.
- Keep the files as living documents: `roadmap.md` in particular is meant to be updated (check off
  phases) as work proceeds.
