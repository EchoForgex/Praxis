---
name: update-index
description: Rebuild rules/index.md from all refined rule files. Run after any rule is added or promoted to refined status. Designed for user-level promotion to ~/.claude/skills/.
---

# update-index

Rebuild the rule index so `/discover-rules` always reflects the current library state.

## Step 1 — Resolve library path

Read `~/.claude/development-guide/config.md`. Extract the value of `library_path:`. All subsequent paths are relative to this root.

## Step 2 — Scan rule files

List all files in `{library_path}/rules/` that end in `.md` and are not `index.md`.

For each file:
1. Read the file
2. Parse frontmatter to extract: `name`, `applies_when`, `source_insight`, `source_project`
3. Read the first non-empty, non-heading line of the body — this is the summary
4. Determine status:
   - If the rule file has a `status` field in its own frontmatter, use that
   - Otherwise, read the linked `source_insight` file and check its `status` field
   - If neither is present, treat as `raw`
5. Include the rule only if status is `refined`

## Step 3 — Write index

Rewrite `{library_path}/rules/index.md` with the full rebuilt table:

```markdown
<!-- auto-generated — do not edit by hand. Update via /update-index or automatically after /refine-insight -->
<!-- only status:refined rules appear here -->

| name | file | applies_when | summary |
|------|------|--------------|---------|
| {name} | rules/{filename} | {applies_when joined by commas} | {summary} |
```

`applies_when` values are written as a comma-separated string (no spaces) for easy parsing: `any,multi-step-tasks,architectural-decisions`

## Step 4 — Report

State how many rules were scanned, how many were included (refined), and how many were skipped (raw). Example:

```
Index updated: 4 refined rules indexed, 2 skipped (raw).
rules/index.md → 4 rows
```
