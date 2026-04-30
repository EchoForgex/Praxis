---
name: verification-before-done
applies_when: [any]
promotes_to: CLAUDE.md
status: refined
source_insight: insights/2026-04-30-claude-md-workflow-rules.md
source_project: seed
---

# Verification Before Done

Never mark a task complete without proving it works.

Diff behavior between main and your changes when relevant. Ask yourself: "Would a staff engineer approve this?" Run tests, check logs, demonstrate correctness.

The bar is "would survive review" — not "plausible output."
