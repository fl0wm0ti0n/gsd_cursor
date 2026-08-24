---
description: "its-magic architecture: technical approach and decisions."
agent: tech-lead
---

# /architecture

phase_id: architecture
role: tech-lead

## Artifacts
- docs/engineering/architecture.md
- decisions/DEC-xxxx.md
- handoffs/tl_to_dev.md

## Validator bridge
Before writing to `docs/product/backlog.md` bug rows or `docs/product/acceptance.md` bug rows, run `python scripts/bug_issue_validate.py --repo . --check-acceptance` and surface any non-zero exit reason code to the operator. The orchestrator plugin enforces persistence.

STOP
