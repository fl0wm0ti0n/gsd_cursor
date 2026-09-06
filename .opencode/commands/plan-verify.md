---
description: "its-magic plan-verify: acceptance coverage check."
agent: qa
---

# /plan-verify

phase_id: plan-verify
role: qa

## Artifacts
- sprints/Sxxxx/plan-verify.json
- handoffs/qa_to_dev.md

## Validator bridge
Before writing to `docs/product/backlog.md` bug rows or `docs/product/acceptance.md` bug rows, run `python scripts/bug_issue_validate.py --repo . --check-acceptance` and surface any non-zero exit reason code to the operator. The orchestrator plugin enforces persistence.

STOP
