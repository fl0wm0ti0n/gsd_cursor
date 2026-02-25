---
description: "its-magic refresh context: compact state and decisions."
---

# /refresh-context

## Subagents
- curator

## Execution model
- Run `/refresh-context` in a fresh Curator subagent context.
- After writing outputs, stop. Next phase starts in a new subagent/chat.

## Inputs
- Current sprint artifacts
- Decisions and handoffs

## Outputs (artifacts)
- `docs/engineering/state.md`
- `docs/engineering/decisions.md`
- `sprints/S0001/summary.md`

## Stop conditions
- Missing critical artifacts

## Steps
1. Compact state and decisions into a short context pack.
2. Update sprint summary with current status.
3. Ensure handoffs and state are consistent.

