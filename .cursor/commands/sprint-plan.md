---
description: "its-magic sprint plan: create sprint and atomic tasks."
---

# /sprint-plan

## Subagents
- tech-lead

## Execution model
- Run `/sprint-plan` in a fresh Tech Lead subagent context.
- After writing outputs, stop and hand off to `/plan-verify` in a new
  subagent/chat.

## Inputs
- Architecture and decisions
- Current backlog priorities
- `.cursor/scratchpad.md` — read SPRINT_MAX_TASKS and SPRINT_AUTO_SPLIT

## Outputs (artifacts)
- `sprints/Sxxxx/sprint.md`
- `sprints/Sxxxx/tasks.md`
- `sprints/Sxxxx/progress.md`
- `handoffs/tl_to_dev.md`
- `sprints/Sxxxx/plan-verify.json` (after /plan-verify)

## Stop conditions
- Missing acceptance criteria
- Decision gate triggered
- Task count exceeds SPRINT_MAX_TASKS and SPRINT_AUTO_SPLIT=1 — propose splitting before proceeding

## Steps
1. Evaluate scope: count expected tasks, read SPRINT_MAX_TASKS from scratchpad (default: 12). If tasks exceed threshold and SPRINT_AUTO_SPLIT=1, propose splitting into multiple sprints or milestones. If the work is too small for a sprint, suggest `/quick` instead.
2. Milestone activation check (DEC-0009): if this sprint belongs to a milestone, check whether this is the first sprint under that milestone. If so, transition the milestone from **created** to **active** state. Before activation, verify that `milestone.json` has real (non-placeholder) values for `name`, `goal`, and `scope`. If any are still draft/empty, populate them before proceeding. Update `phases.json` to reflect actual planned phases.
3. Create a sprint scope and goals.
4. Break work into atomic tasks.
5. Update traceability index in `docs/engineering/state.md`: add a row for each story assigned to this sprint using the DEC-0010 format (`Story | Sprint | Tasks | Status | Evidence`). Set Status = `PLANNED`, leave Evidence empty. If a story already has a row from a prior sprint, do not duplicate — update the existing row only if the sprint assignment changed.
6. Create UAT placeholder files per DEC-0009 lifecycle (placeholder state). For `uat.json`: set sprint ID and an empty steps array (`{ "sprint": "Sxxxx", "stories": [...], "steps": [], "passed": 0, "failed": 0 }`). For `uat.md`: write a header and list the target stories and their acceptance criteria — no results yet. These placeholders must be populated by QA during `/verify-work`.
7. Write TL -> Dev handoff.
8. Run `/plan-verify` to check coverage.

