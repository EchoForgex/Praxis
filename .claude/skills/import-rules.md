---
name: import-rules
description: Ingest an existing CLAUDE.md, .cursorrules, copilot-instructions.md, or .mdc file and extract its rules into Praxis format. Creates one raw insight file and one rule file per extracted rule. Designed for user-level promotion to ~/.claude/skills/.
---

# import-rules

Extract rules from an existing AI config file and bring them into the Praxis library as raw insight + rule files.

## Input

The user provides a file path to import. Supported formats:
- `CLAUDE.md` — Claude Code project instructions
- `.cursorrules` — legacy Cursor rules file
- `.cursor/rules/*.mdc` — Cursor MDC rule files (one file or a directory)
- `.github/copilot-instructions.md` — GitHub Copilot instructions
- Any `.md` or `.txt` file containing freeform AI instructions

## Step 1 — Resolve library path

Read `~/.claude/praxis/config.md`. Extract the value of `library_path:`.

## Step 2 — Read the source file

Read the file at the provided path. If it does not exist, report the error and stop.

For `.mdc` files: parse the YAML frontmatter separately from the body. The `description` field is useful context for rule intent.

## Step 3 — Extract distinct rules

Analyze the file content and identify every distinct rule or instruction it contains. A distinct rule is one that:
- Addresses a different behavior, workflow, or decision pattern
- Could stand alone as a self-contained instruction
- Would have a different `applies_when` profile than its siblings

**Extraction signals to look for:**
- Numbered or bulleted lists of instructions
- Headings that introduce a behavioral rule
- "Always", "Never", "When X, do Y" patterns
- Named conventions (e.g. "Plan Mode", "Verification")
- Negative instructions ("Don't ask", "Never mock")

**What to skip:**
- Project-specific context (tech stack, file paths, team names) that isn't a generalizable rule
- Setup instructions or one-time commands
- Repetitive restatements of the same rule

List the rules you intend to create before writing files, with proposed slugs. Present this list to the user for confirmation. Allow the user to exclude any rule or adjust a slug before proceeding.

## Step 4 — Create insight file

One insight file covers the entire imported file as its source.

File path: `{library_path}/insights/YYYY-MM-DD-import-{slug}.md`

- `YYYY-MM-DD`: today's date
- `{slug}`: 2–4 word kebab-case description of the source (e.g. `cursor-rules`, `team-claude-md`)

Frontmatter:
```yaml
---
date: YYYY-MM-DD
sources:
  - url: <absolute path of the imported file>
    type: local-file
source_project: <infer from file path or ask user>
status: raw
tags: []
---
```

Body: brief description of the source file and a summary of what was extracted.

## Step 5 — Create one rule file per extracted rule

For each rule confirmed in Step 3, create `{library_path}/rules/{slug}.md`.

Use a descriptive slug specific to that rule — not the insight slug.

Frontmatter:
```yaml
---
name: {slug}
applies_when: []
promotes_to: CLAUDE.md
source_insight: insights/YYYY-MM-DD-import-{insight-slug}.md
source_project: <same as insight>
status: raw
---
```

Body: the rule as extracted — cleaned up for clarity but not yet enriched. Keep it close to the original intent.

Leave `applies_when: []` — that is filled in during `/refine-insight`.

## Step 6 — Update index

Invoke `/update-index`. Since all new rules are `status: raw`, they will not appear in the index yet — but running the update ensures the index is consistent.

## Step 7 — Report

Tell the user:
- Path of the insight file created
- List of all rule files created with their proposed slugs and a one-line summary of each
- Total count: N rules extracted from the source file
- Recommended next step: run `/refine-insight` to enrich `applies_when` and promote rules to `refined`
