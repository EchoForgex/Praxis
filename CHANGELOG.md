# Changelog

## v0.1 — Foundation (2026-05-01)

First publishable release. Establishes the core capture-to-discovery pipeline and project identity.

### Added
- `/add-insight` skill — capture insights from URLs, PDFs, local files, paste, or verbal description; creates raw insight + one rule file per distinct rule
- `/refine-insight` skill — enrich raw rules with `applies_when` metadata, tags, promotes_to; advances status raw → refined; appends changelog entries to rule files
- `/discover-rules` skill — runtime discovery; reads index (single file), matches task context, injects relevant rule bodies
- `/update-index` skill — rebuilds `rules/index.md` from all refined rule files; called automatically by add-insight and refine-insight
- `/import-rules` skill — ingest an existing CLAUDE.md, .cursorrules, or copilot-instructions.md and extract rules into Praxis format
- `rules/index.md` — auto-generated index of all `status: refined` rules
- `~/.claude/praxis/config.md` — library path config for user-level skill resolution
- 6 seed rules: plan-mode-default, subagent-strategy, self-improvement-loop, verification-before-done, demand-elegance, autonomous-bug-fixing
- `status: deprecated` support — deprecated rules are excluded from the index
- Per-rule `changelog:` frontmatter field — tracks refinement history per rule

### Changed
- Project renamed from DevelopmentGuide to Praxis
- Config path moved from `~/.claude/development-guide/config.md` → `~/.claude/praxis/config.md`

---

## 2026-04-30 — Initial scaffold

- Initial scaffold: `insights/`, `rules/`, `skills/`, `tasks/`
- Six core workflow rules extracted from seed insight to `rules/`
- `CLAUDE.md` defining project purpose, three-layer model, and working conventions
