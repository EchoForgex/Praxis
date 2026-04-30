# Claude Code Workflow Rules (Seed Insight)

Source: personal practice / community post

## The Six Rules

### Plan Mode by Default
Models patch forward by instinct. They rarely back up and re-plan when something goes wrong. Forcing plan mode on any task with three or more steps cuts the cascade where each fix introduces two more problems.

### Subagent Strategy
Context degrades when research, debugging, planning, and implementation share one thread. One task per subagent, clean return.

### Self-Improvement Loop
The most underrated rule. Without it, every session is stateless and you correct the same mistakes for weeks. With it, `tasks/lessons.md` becomes per-project memory the next session reads before doing anything.

### Verification Before Done
The staff engineer line is the lever. It reframes the bar from "plausible output" to "would survive review." That single shift produces measurably better code.

### Demand Elegance (Balanced)
"Knowing everything I know now" is the useful reframe. It forces a second pass with full context, which usually beats the first attempt.

### Autonomous Bug Fixing
Kills the "what would you like me to do?" reflex. Logs and stack traces are evidence to read, not questions to ask back.

## Task File Conventions
- `tasks/todo.md` — per-session state
- `tasks/lessons.md` — per-project memory

## Status
- Refined rules extracted to `rules/`
- Applicable to: all project types, all team sizes
