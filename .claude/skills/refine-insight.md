---
name: refine-insight
description: Enrich raw insights and their drafted rules. Fills in applies_when conditions, tags, promotes_to, and strengthens rule bodies. Advances status from raw → refined.
---

# refine-insight

Enhance raw insight and rule files so they carry enough metadata to be used in project composition.

## Input

The user may provide:
- A specific insight file path (e.g. `insights/2026-04-30-plan-mode.md`)
- A specific rule file path (e.g. `rules/plan-mode-default.md`)
- Nothing — scan all `insights/` files where `status: raw` and process them in order

## Step 1 — Find targets

If a path was given, derive the paired file (insight ↔ rule via `source_insight` frontmatter).

If no path given: read all files in `insights/` and collect those with `status: raw`. Process one at a time — do not batch-update without user review.

## Step 2 — Read and analyze

For each target, read both the insight file and its linked rule file. Then assess:

**Insight gaps:**
- `tags: []` — empty or thin
- `applies_when` — not present on the insight (it lives on the rule, but infer from insight content)

**Rule gaps:**
- `applies_when: []` — the most critical gap; rules without this cannot be composed
- `promotes_to` — is CLAUDE.md really right, or should this become a skill?
- Rule body — is it a direct, actionable instruction? Or vague/descriptive?

## Step 3 — Propose enrichments

Using the content of both files, propose values for each gap. Use the taxonomy below for consistency.

### applies_when taxonomy

**Project type:**
`api`, `frontend`, `cli`, `data-pipeline`, `library`, `mobile`, `infrastructure`, `fullstack`

**Team context:**
`solo`, `small-team`, `large-team`

**Maturity stage:**
`greenfield`, `active-development`, `legacy`, `hotfix`, `refactor`

**Task type:**
`multi-step-tasks`, `architectural-decisions`, `bug-reports`, `parallel-research`, `ci-failures`, `failing-tests`, `non-trivial-changes`

**Scope:**
`any` — use only when the rule genuinely applies regardless of context

### promotes_to guidance

- `CLAUDE.md` — a workflow rule; goes in a project's CLAUDE.md as a behavioral instruction
- `skill` — a procedural workflow; better expressed as a step-by-step skill file
- `both` — has both a one-line CLAUDE.md rule and a detailed skill implementation

### Rule body quality bar

A well-refined rule body:
- Opens with a direct instruction ("When X, do Y")
- Explains the reason in one sentence
- Is under 100 words
- Would not confuse a future reader who hasn't seen the original insight

If the drafted rule body is weak (vague, too long, or purely descriptive), rewrite it to meet this bar and present the rewrite for confirmation.

## Step 4 — Present and confirm

Show the user the proposed changes before writing anything:

```
Insight: insights/2026-04-30-{slug}.md
  tags:         [] → [claude-code, workflow, planning]

Rule: rules/{slug}.md
  applies_when: [] → [any, multi-step-tasks, architectural-decisions]
  promotes_to:  CLAUDE.md → CLAUDE.md  (unchanged)
  body:         (unchanged) | (rewrite proposed — see below)
```

Wait for confirmation. If the user adjusts any values, use their version.

## Step 5 — Write changes

Update both files with confirmed values. In the insight file, advance:
```yaml
status: raw → refined
```

## Step 6 — Report

After each file pair is refined:
- Confirm paths updated and new status
- Note any fields still left incomplete that need domain knowledge to fill (flag but don't block)
- If more `status: raw` files remain in the queue, ask whether to continue to the next one
