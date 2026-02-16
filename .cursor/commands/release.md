---
description: "its-magic release: prepare release notes and runbook updates."
---

# /release

## Subagents
- release

## Inputs
- `sprints/S0001/summary.md`
- `docs/engineering/runbook.md`

## Outputs (artifacts)
- `handoffs/release_notes.md`
- `docs/engineering/runbook.md`
- `docs/engineering/state.md`

## Stop conditions
- Deploy command missing for requested environment
- Decision gate triggered

## Steps
1. Write release notes and versioning notes.
2. Update runbook commands if needed.
3. Update state and readiness.
4. If `AUTO_RELEASE_NOTES=1` in `.cursor/scratchpad.md`, generate
   `handoffs/release_notes.md` via the release notes script.

