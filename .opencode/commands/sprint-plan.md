---
description: "its-magic sprint-plan: sprint and task list."
agent: tech-lead
---

# /sprint-plan

phase_id: sprint-plan
role: tech-lead

## Artifacts
- sprints/Sxxxx/sprint.md
- sprints/Sxxxx/tasks.md
- handoffs/tl_to_dev.md

## Validator bridge
Before writing to `docs/product/backlog.md` bug rows or `docs/product/acceptance.md` bug rows, run `python scripts/bug_issue_validate.py --repo . --check-acceptance` and surface any non-zero exit reason code to the operator. The orchestrator plugin enforces persistence.

STOP
