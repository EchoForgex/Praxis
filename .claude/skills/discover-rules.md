---
name: discover-rules
description: Dynamically discover applicable workflow rules from the library for the current task. Reads the rules index (single file read), matches against task context, then fetches only matching rule bodies. Designed for user-level promotion to ~/.claude/skills/.
---

# discover-rules

Find and apply workflow rules relevant to the current task without requiring a pre-configured CLAUDE.md.

## Step 1 — Resolve library path

Read `~/.claude/development-guide/config.md`. Extract the value of `library_path:`.

## Step 2 — Read the index

Read `{library_path}/rules/index.md`. This is the only file read in this step — it contains all refined rules' metadata in a single table.

If the index is empty or does not exist, report: "No refined rules in library yet. Run /refine-insight to promote rules, then /update-index."

## Step 3 — Understand task context

The user will have provided a task description, or you have the current task in context. From this, infer applicable condition tags using the taxonomy below.

Multiple tags may apply. Be liberal — it's better to surface a slightly over-broad rule than to miss a relevant one.

### Signal → tag mapping

| Signal in task description | Inferred tags |
|---------------------------|---------------|
| "fix", "bug", "broken", "error", "crash" | `bug-reports` |
| "test", "failing test", "CI", "pipeline" | `failing-tests`, `ci-failures` |
| "new project", "start", "greenfield", "from scratch" | `greenfield` |
| "refactor", "clean up", "rewrite" | `refactor` |
| "hotfix", "urgent", "production issue" | `hotfix` |
| "API", "endpoint", "REST", "GraphQL" | `api` |
| "frontend", "UI", "component", "page" | `frontend` |
| "CLI", "command line", "terminal tool" | `cli` |
| "data", "pipeline", "ETL", "transform" | `data-pipeline` |
| "mobile", "iOS", "Android", "React Native" | `mobile` |
| "infra", "infrastructure", "deployment", "Terraform" | `infrastructure` |
| "alone", "solo", "just me" | `solo` |
| "team", "PR", "review", "colleagues" | `small-team` |
| "3+ steps", "multi-step", "complex task", "several things" | `multi-step-tasks` |
| "architecture", "design", "decision", "approach" | `architectural-decisions` |
| "parallel", "concurrent", "multiple agents" | `parallel-research` |

Always include `any` in the inferred set — rules tagged `any` apply regardless of context.

## Step 4 — Filter index

For each row in the index:
- Split the `applies_when` column by comma to get a list of tags
- If any tag in the rule's list matches any tag in the inferred set → include the rule
- `any` in the rule's list always matches

## Step 5 — Fetch matched rule bodies

For each matched rule, read `{library_path}/{file}` to get the full rule body.

## Step 6 — Present and apply

Output the matched rules clearly:

```
Applicable rules for this task:

1. **plan-mode-default** — Enter plan mode for 3+ step tasks or architectural decisions.
   [full rule body]

2. **verification-before-done** — Prove it works before marking complete.
   [full rule body]
```

Then apply them: let the matched rules shape how you approach the current task. Do not just list them — internalize and act on them.

If zero rules match beyond `any`, say so and list any `any` rules that still apply.
