---
name: subagent-strategy
applies_when: [any, parallel-research, multi-step-tasks]
promotes_to: CLAUDE.md
status: refined
source_insight: insights/2026-04-30-claude-md-workflow-rules.md
source_project: seed
---

# Subagent Strategy

Use subagents liberally to keep the main context window clean.

Offload research, exploration, and parallel analysis to subagents. For complex problems, throw more compute at it via subagents. One task per subagent for focused execution.

Context degrades when research, debugging, planning, and implementation share one thread — separate them.
