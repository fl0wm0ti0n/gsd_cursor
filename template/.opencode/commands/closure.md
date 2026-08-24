---
description: "its-magic closure: story closure with role=qe."
agent: qa
---

# /closure

phase_id: closure
role: qe

## Artifacts
- sprints/Sxxxx/closure-verification.md
- docs/product/backlog.md (status flip)
- docs/product/acceptance.md (checkbox tick)

## Validator bridge
Before writing to `docs/product/backlog.md` bug rows or `docs/product/acceptance.md` bug rows, run `python scripts/bug_issue_validate.py --repo . --check-acceptance` and surface any non-zero exit reason code to the operator. The orchestrator plugin enforces persistence.

STOP
