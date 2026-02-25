---
description: "its-magic resume: deterministic continuation context loader."
---

# /resume

## Subagents
- curator

## Execution model
- Run `/resume` in a fresh Curator subagent context.
- When continuing to another phase, start that phase in a new subagent/chat.

## Inputs
- `docs/engineering/state.md`
- `docs/engineering/decisions.md`
- `sprints/S0001/summary.md`
- `handoffs/resume_brief.md`
- Optional automation flags from `.cursor/scratchpad.md`
- Optional operator intent to continue via `/auto start-from=<phase>`

## Outputs (artifacts)
- Updated `docs/engineering/state.md` (if needed)

## Stop conditions
- Missing resume brief or stale state

## Steps
1. Load the context pack and open decisions.
2. Parse intended resume phase from `handoffs/resume_brief.md`.
3. Validate that `resume_brief` phase is canonical and consistent with latest
   `docs/engineering/state.md` checkpoint.
4. If `resume_brief.md` is stale/unparseable/conflicting, fail fast with the
   `/auto` resolver contract format:
   `[AUTO_RESUME_ERROR] <code>: <summary>. Source=<source>. Fix: <action>.`
5. Summarize current status, deterministic resume source, and next steps.
6. For deterministic continuation, recommend:
   - explicit override: `/auto start-from=<phase>`
   - default precedence: `/auto` (argument > resume brief > state fallback)
7. If `AUTO_FLOW_MODE=auto_until_decision`, continue automation with existing
   decision gates and stop conditions preserved.

## Compatibility notes

- `/resume` remains valid for manual/interactive status recovery.
- `/resume` does not bypass `/auto` stop conditions or gate behavior.

