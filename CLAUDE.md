# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

**Praxis** is a personal rule library for Claude Code — a living collection of best practices, workflow rules, and reusable skills. It captures developer insights (CLAUDE.md rule sets, debugging strategies, verification standards) and makes them selectively applicable across projects via dynamic discovery.

**End goal:** A library of user-level skills promoted to `~/.claude/skills/`, activated globally via the bootstrap instruction in `~/.claude/CLAUDE.md` — no per-project changes required.

## Current Status

6 seed rules in library. Bootstrap instruction is live in `~/.claude/CLAUDE.md`. Next: review seed rules for promotion to `~/.claude/skills/`.

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

`/discover-rules` reads `~/.claude/praxis/config.md` for the library path, loads `rules/index.md` in a single read, matches against task context, then fetches only the relevant rule bodies. The bootstrap instruction that activates this globally lives in `~/.claude/CLAUDE.md`.

### Promoting to user-level

When skills are ready, promote them by:
1. Copy `.claude/skills/*.md` → `~/.claude/skills/`
2. Ensure `~/.claude/praxis/config.md` exists with the correct `library_path:`
3. Document the promotion in `CHANGELOG.md`

### Task tracking

- `tasks/todo.md` — current session work
- `tasks/lessons.md` — local correction log; read this at session start for context on past corrections

## HTTP Service (`service/`)

Praxis runs a FastAPI rules engine on **port 8004** alongside the file-based Claude Code library. The two systems are independent.

### Service commands

```bash
cd service

# Install deps
poetry install

# Dev server
poetry run uvicorn main:app --reload --port 8004

# Migrations
poetry run alembic upgrade head
poetry run alembic revision --autogenerate -m "<description>"
```

### Port assignments

| Service | Port |
|---------|------|
| EchoForge OS | 8000 |
| echoforge-agent | 8001 |
| MemForge | 8002 |
| echoforge-hub | 8003 |
| **Praxis** | **8004** |

### Environment

`service/.env` holds `DATABASE_URL`, `PRAXIS_SERVICE_SECRET`, `PORT`, `LOG_LEVEL`.  
OS accesses Praxis via `PRAXIS_BASE_URL` + `PRAXIS_SERVICE_TOKEN` (see `ProjectOS/.env`).

## Cross-Project Notices

Notices are centralized in `EchoForgeX_Arch/notices/`. This project's ID is `PR`.

**At session start**, check for open notices:
```bash
grep -rl "to_id: PR" /Users/jeffreysinason/Development/EchoForgeX_Arch/notices/ 2>/dev/null | xargs grep -l "status: open" 2>/dev/null
```
Read and act on any files returned before starting work.

**To file a notice**, write `NOTICE-{YYYY-MM-DD}-PR-{to_id}-{n}.md` in `/Users/jeffreysinason/Development/EchoForgeX_Arch/notices/` with standard front-matter (`from_id: PR`, `status: open`).
