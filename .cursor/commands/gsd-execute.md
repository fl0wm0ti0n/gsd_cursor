---
description: "GSD execute: implement tasks with artifacts and state updates."
---

# /gsd-execute

## Subagents
- dev

## Inputs
- `sprints/S0001/tasks.md`
- `handoffs/tl_to_dev.md`

## Outputs (artifacts)
- Code changes
- `sprints/S0001/summary.md`
- `docs/engineering/state.md`
- `handoffs/dev_to_qa.md` (if ready)

## Stop conditions
- Decision gate triggered
- Missing task definition or unclear scope

## Steps
1. Implement one task at a time.
2. Update summary and engineering state.
3. Handoff to QA when ready.
4. If `AUTO_INSTALL_DEPS=1` in `.cursor/scratchpad.md`, install dependencies
   via the appropriate package manager without prompting.
5. If `REMOTE_EXECUTION=1` and `.cursor/remote.json` is configured, use
   remote/docker servers for heavy builds or tests when needed.

