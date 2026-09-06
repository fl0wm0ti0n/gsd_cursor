---
description: "its-magic qa: test plan, findings, verify fixes."
agent: qa
---

# /qa

phase_id: qa
role: qa

## Artifacts
- sprints/Sxxxx/qa-findings.md
- handoffs/qa_to_dev.md

## Validator bridge
Before writing to `docs/product/backlog.md` bug rows or `docs/product/acceptance.md` bug rows, run `python scripts/bug_issue_validate.py --repo . --check-acceptance` and surface any non-zero exit reason code to the operator. The orchestrator plugin enforces persistence.

STOP
