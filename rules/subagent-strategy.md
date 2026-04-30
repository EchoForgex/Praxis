---
name: subagent-strategy
applies_when: [any, parallel-research, complex-problems]
promotes_to: CLAUDE.md
---

# Subagent Strategy

Use subagents liberally to keep the main context window clean.

Offload research, exploration, and parallel analysis to subagents. For complex problems, throw more compute at it via subagents. One task per subagent for focused execution.

Context degrades when research, debugging, planning, and implementation share one thread — separate them.
