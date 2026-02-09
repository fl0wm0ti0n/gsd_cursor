---
description: "GSD sprint plan: create sprint and atomic tasks."
---

# /gsd-sprint-plan

## Subagents
- tech-lead

## Inputs
- Architecture and decisions
- Current backlog priorities

## Outputs (artifacts)
- `sprints/S0001/sprint.md`
- `sprints/S0001/tasks.md`
- `sprints/S0001/progress.md`
- `handoffs/tl_to_dev.md`
 - `sprints/S0001/plan-verify.json` (after /gsd-plan-verify)

## Stop conditions
- Missing acceptance criteria
- Decision gate triggered

## Steps
1. Create a sprint scope and goals.
2. Break work into atomic tasks.
3. Write TL -> Dev handoff.
4. Run `/gsd-plan-verify` to check coverage.

