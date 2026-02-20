---
description: "its-magic resume: load context pack and continue work."
---

# /resume

## Subagents
- curator

## Inputs
- `docs/engineering/state.md`
- `docs/engineering/decisions.md`
- `sprints/S0001/summary.md`
- `handoffs/resume_brief.md`
- Optional automation flags from `.cursor/scratchpad.md`

## Outputs (artifacts)
- Updated `docs/engineering/state.md` (if needed)

## Stop conditions
- Missing resume brief or stale state

## Steps
1. Load the context pack and open decisions.
2. Summarize current status and next steps.
3. Continue from the resume phase noted in `handoffs/resume_brief.md`.
4. If `AUTO_FLOW_MODE=auto_until_decision`, continue automation until the next
   decision gate, pause request, or blocker.

