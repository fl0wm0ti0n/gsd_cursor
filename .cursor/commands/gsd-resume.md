---
description: "GSD resume: load context pack and continue work."
---

# /gsd-resume

## Subagents
- curator

## Inputs
- `docs/engineering/state.md`
- `docs/engineering/decisions.md`
- `sprints/S0001/summary.md`
- `handoffs/resume_brief.md`

## Outputs (artifacts)
- Updated `docs/engineering/state.md` (if needed)

## Stop conditions
- Missing resume brief or stale state

## Steps
1. Load the context pack and open decisions.
2. Summarize current status and next steps.
3. Hand off to the appropriate phase.

