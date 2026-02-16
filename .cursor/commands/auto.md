---
description: "its-magic auto: run phases sequentially until decision gate."
---

# /auto

## Subagents
- curator
- tech-lead

## Inputs
- `AUTO_FLOW_MODE` and `PHASE_MODE` from `.cursor/scratchpad.md`
- Current product and engineering docs

## Outputs (artifacts)
- Updated phase artifacts for each step
- `docs/engineering/state.md`
- `handoffs/resume_brief.md` if stopped

## Stop conditions
- Decision gate triggered
- Missing critical input

## Steps
1. Read automation flags from scratchpad.
2. Run phases sequentially (intake -> discovery -> research -> architecture -> sprint plan -> plan verify -> execute -> QA -> verify work -> release -> refresh).
3. Stop at decision gate or missing info and write resume brief.
