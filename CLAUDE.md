# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a Development Guide repository — a living collection of best practices, workflow rules, and reusable skills for Claude Code projects. Its goal is to capture developer insights (like CLAUDE.md rule sets, debugging strategies, verification standards) and make them selectively applicable across projects.

**Current scope:** Project-level. Content here is developed and validated before being promoted to user-level (`~/.claude/`) commands and skills.

**End goal:** A library of user-level skills and CLAUDE.md fragments that can be composed into any new or existing project's workflow.

## Architecture Intent

### Three-layer model

1. **Raw insights** — unprocessed tips, examples, and observations captured as they're found (markdown notes, snippets, links)
2. **Refined rules** — distilled, testable workflow rules ready to be included in a CLAUDE.md (e.g. "Plan Mode by default", "Verification before done")
3. **Promoted skills** — rules packaged as Claude Code skills (`.claude/skills/`) ready for use across projects

### Key design constraint: conditional applicability

Not every rule applies to every project. When adding content, annotate it with the conditions under which it applies:
- project type (API, frontend, CLI, data pipeline, …)
- team size or solo
- maturity stage (greenfield, legacy refactor, hotfix)

This annotation layer is what enables dynamic selection — a future tool or prompt can read the conditions and determine what to include in a given project's CLAUDE.md.

## Working Conventions

### Adding new content

- Capture first in `insights/` as a raw note; refine later
- Each refined rule lives in its own file under `rules/` with a frontmatter block:

```markdown
---
name: rule-name
applies_when: [greenfield, solo, multi-step-tasks]
promotes_to: CLAUDE.md | skill | both
---
```

- Promoted skills go to `skills/` following the existing superpowers skill format (frontmatter + instruction body)

### Promoting to user-level

When a skill or rule has been validated in this project, promote it by copying to `~/.claude/skills/` (skills) or appending the relevant block to `~/.claude/CLAUDE.md` (global rules). Document the promotion in `CHANGELOG.md` with a rationale note.

### Task tracking

- `tasks/todo.md` — current session work
- `tasks/lessons.md` — cross-session memory; update after any correction or insight

## The Six Core Rules (Seed Content)

These are the validated CLAUDE.md rules that seeded this project. They live here as the canonical reference:

| Rule | When it applies |
|------|----------------|
| **Plan Mode by default** | Any task with 3+ steps or an architectural decision |
| **Subagent strategy** | Research, parallel analysis, or isolated execution tasks |
| **Self-improvement loop** | Always — update `tasks/lessons.md` after every user correction |
| **Verification before done** | Always — prove it works before marking complete |
| **Demand elegance (balanced)** | Non-trivial changes; skip for obvious single-line fixes |
| **Autonomous bug fixing** | Always — read logs and stack traces, resolve without asking back |
