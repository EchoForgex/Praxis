# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

**Praxis** is a personal rule library for Claude Code — a living collection of best practices, workflow rules, and reusable skills. It captures developer insights (CLAUDE.md rule sets, debugging strategies, verification standards) and makes them selectively applicable across projects via dynamic discovery.

**End goal:** A library of user-level skills and a global `~/.claude/CLAUDE.md` instruction that activates rule discovery across all projects — no per-project changes required.

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

This annotation layer is what enables dynamic selection — `/discover-rules` reads these conditions at task time and returns only what applies, without any per-project CLAUDE.md configuration.

## Working Conventions

### Adding new content

Use `/add-insight` to capture anything worth keeping — paste text, give a URL (web page, GitHub repo, YouTube, social post), or describe it verbally. The skill creates a raw insight file and drafts a structured rule for review.

**Insight frontmatter** (`insights/YYYY-MM-DD-{slug}.md`):
```yaml
---
date: YYYY-MM-DD
sources:
  - url: <URL | "paste" | "verbal">
    type: web | github | youtube | social-linkedin | social-twitter | social-reddit | pdf | local-file | paste | verbal
source_project: <project name or "none">
status: raw
tags: []
---
```
Multiple co-sources are listed as additional entries under `sources`. One insight file covers all of them.

**Rule frontmatter** (`rules/{slug}.md`):
```yaml
---
name: rule-name
applies_when: [condition1, condition2]
promotes_to: CLAUDE.md | skill | both
source_insight: insights/YYYY-MM-DD-{slug}.md
source_project: <project name or "none">
---
```

**Directory roles:**
- `.claude/skills/` — skills under development; designed for `~/.claude/skills/` from day one
- `skills/` — content staged for promotion to user-level (`~/.claude/skills/`)
- `rules/index.md` — auto-generated index of all `status: refined` rules; do not edit by hand

### Dynamic rule discovery

No per-project CLAUDE.md changes are needed. The bootstrap instruction lives once in `~/.claude/CLAUDE.md`:
```
Before starting any task with 3+ steps, invoke /discover-rules with a brief task description.
```

This activates rule discovery globally. `/discover-rules` reads `~/.claude/praxis/config.md` for the library path, loads `rules/index.md` in a single read, matches against task context, then fetches only the relevant rule bodies. Individual project CLAUDE.md files stay focused on project-specific context only.

### Promoting to user-level

When skills are ready, promote them by:
1. Copy `.claude/skills/*.md` → `~/.claude/skills/`
2. Add the bootstrap instruction to `~/.claude/CLAUDE.md` (once, covers all projects)
3. Ensure `~/.claude/praxis/config.md` exists with the correct `library_path:`
4. Document the promotion in `CHANGELOG.md`

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
