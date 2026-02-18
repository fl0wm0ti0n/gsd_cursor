---
description: "its-magic pause: write checkpoint and resume brief."
---

# /pause

## Subagents
- curator

## Inputs
- Current sprint progress and state
- Optional intent: immediate pause or graceful pause after current boundary

## Outputs (artifacts)
- `docs/engineering/state.md`
- `sprints/S0001/progress.md`
- `handoffs/resume_brief.md`

## Stop conditions
- Missing state or progress updates

## Steps
1. Write a short checkpoint of current work.
2. Update sprint progress and state.
3. Write a resume brief with next actions.
4. Record the intended resume phase in `handoffs/resume_brief.md` (for example:
   execute, qa, verify-work, release).
5. If this pause was requested via `AUTO_PAUSE_REQUEST=1`, reset the flag to `0`
   after checkpoint is complete.

