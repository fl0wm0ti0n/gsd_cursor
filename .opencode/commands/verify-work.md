---
description: "its-magic verify-work: UAT verification."
agent: qa
---

# /verify-work

phase_id: verify-work
role: qa

## Artifacts
- sprints/Sxxxx/uat.json
- sprints/Sxxxx/uat.md
- handoffs/qa_to_verify.md

## Validator bridge
Before writing to `docs/product/backlog.md` bug rows or `docs/product/acceptance.md` bug rows, run `python scripts/bug_issue_validate.py --repo . --check-acceptance` and surface any non-zero exit reason code to the operator. The orchestrator plugin enforces persistence.

STOP
