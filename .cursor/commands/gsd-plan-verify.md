---
description: "GSD plan verify: verify sprint tasks against acceptance."
---

# /gsd-plan-verify

## Subagents
- tech-lead

## Inputs
- `sprints/S0001/tasks.md`
- `docs/product/acceptance.md`
- `docs/engineering/architecture.md`

## Outputs (artifacts)
- `sprints/S0001/plan-verify.json`
- `docs/engineering/state.md`

## Stop conditions
- Tasks do not cover acceptance criteria
- Decision gate triggered

## Steps
1. Check each acceptance criterion against tasks.
2. Record gaps and required changes in `plan-verify.json`.
3. Update state and handoff if needed.
