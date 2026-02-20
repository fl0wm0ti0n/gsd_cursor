---
description: "its-magic auto: run phases sequentially until decision gate."
---

# /auto

## Subagents
- curator
- tech-lead

## Inputs
- `AUTO_FLOW_MODE` and `PHASE_MODE` from `.cursor/scratchpad.md`
- `AUTO_IMPLEMENTATION_LOOP`, `AUTO_LOOP_MAX_CYCLES` from `.cursor/scratchpad.md`
- `AUTO_PAUSE_REQUEST`, `AUTO_PAUSE_POLICY` from `.cursor/scratchpad.md`
- Current product and engineering docs

## Outputs (artifacts)
- Updated phase artifacts for each step
- `docs/engineering/state.md`
- `handoffs/resume_brief.md` if stopped
- `sprints/S0001/qa-findings.md` and `handoffs/qa_to_dev.md` when loop finds issues

## Stop conditions
- Decision gate triggered
- Missing critical input
- `AUTO_PAUSE_REQUEST=1` reached at a safe boundary
- `AUTO_LOOP_MAX_CYCLES` reached with unresolved defects

## Steps
1. Read automation flags from scratchpad.
2. Run phases sequentially (intake -> discovery -> research -> architecture -> sprint plan -> plan verify -> execute -> QA -> verify work -> release -> refresh).
3. If `AUTO_IMPLEMENTATION_LOOP=1`, loop between `execute` and `QA` until QA has no blocking findings, then continue to `verify work` and `release`.
4. If `AUTO_PAUSE_REQUEST=1`, complete the current safe boundary (`AUTO_PAUSE_POLICY`) and run `/pause` to persist checkpoint artifacts.
5. Stop at decision gate or missing info and write resume brief.
