---
description: "its-magic refresh-context: update stale artifacts."
agent: curator
---

# /refresh-context

phase_id: refresh-context
role: curator

## Artifacts
- docs/engineering/state.md
- handoffs/resume_brief.md

## Validator bridge
Before writing to `docs/product/backlog.md` bug rows or `docs/product/acceptance.md` bug rows, run `python scripts/bug_issue_validate.py --repo . --check-acceptance` and surface any non-zero exit reason code to the operator. The orchestrator plugin enforces persistence.

STOP
