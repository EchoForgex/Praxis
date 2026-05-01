# Praxis

A personal rule library for Claude Code. Captures developer best practices as structured, conditionally applicable rules and injects only the relevant ones at task time — no per-project CLAUDE.md configuration required.

## How it works

1. **Capture** — `/add-insight` turns any source (URL, PDF, paste, verbal) into a raw insight + draft rule files
2. **Refine** — `/refine-insight` enriches rules with `applies_when` metadata so they know when they apply
3. **Discover** — `/discover-rules` reads task context, matches against the rule index, and injects relevant rules
4. **Import** — `/import-rules` extracts rules from an existing CLAUDE.md or .cursorrules file

Rules live in one place. Any project that runs `/discover-rules` gets the applicable subset — nothing is duplicated across projects.

## Prerequisites

- [Claude Code](https://claude.ai/code) CLI

## Setup

```bash
# 1. Clone the repo
git clone <repo-url> ~/Development/Praxis

# 2. Create the config file
mkdir -p ~/.claude/praxis
echo "library_path: $HOME/Development/Praxis" > ~/.claude/praxis/config.md

# 3. Copy skills to user-level
cp ~/Development/Praxis/.claude/skills/*.md ~/.claude/skills/

# 4. Add bootstrap instruction to ~/.claude/CLAUDE.md
echo "\nBefore starting any task with 3+ steps, invoke /discover-rules with a brief task description." >> ~/.claude/CLAUDE.md
```

## Skills

| Skill | Description |
|-------|-------------|
| `/add-insight` | Capture a new insight from any source; creates raw insight + rule files |
| `/refine-insight` | Enrich a raw rule with `applies_when` metadata; advances it to `refined` |
| `/discover-rules` | Find and apply rules relevant to the current task |
| `/update-index` | Rebuild `rules/index.md` from all refined rule files |
| `/import-rules` | Extract rules from an existing CLAUDE.md or .cursorrules file |

## Directory structure

```
Praxis/
  insights/       Raw and refined insight files
  rules/          One rule file per extracted rule; index.md is auto-generated
  .claude/skills/ Skill files (copy to ~/.claude/skills/ for user-level use)
  CHANGELOG.md
```

## Versioning

See [CHANGELOG.md](CHANGELOG.md).
