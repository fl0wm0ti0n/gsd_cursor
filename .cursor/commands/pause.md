---
description: "its-magic pause: write checkpoint and resume brief."
---

# /pause

## Subagents
- curator

## Execution model
- Run `/pause` in a fresh Curator subagent context.
- After writing outputs, stop.

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
3. Record deterministic continuation breadcrumbs in `docs/engineering/state.md`:
   - `invocation_mode=auto|manual`
   - `requested_start_from`
   - `resolved_start_phase`
   - `resolution_source`
   - `resolution_status`
   - `stop_reason=pause_request|manual_pause`
   - `stop_phase`
   - `timestamp`
4. Write `handoffs/resume_brief.md` with next actions and canonical intended
   resume phase (`intake|discovery|research|architecture|sprint-plan|plan-verify|execute|qa|verify-work|release|refresh-context`).
5. If pause metadata is stale or ambiguous, fail fast with:
   `[AUTO_RESUME_ERROR] <code>: <summary>. Source=<source>. Fix: <action>.`
6. If this pause was requested via `AUTO_PAUSE_REQUEST=1`, reset the flag to `0`
   after checkpoint is complete.

