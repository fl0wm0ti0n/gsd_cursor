---
description: "its-magic research: risks, patterns, dependencies."
agent: tech-lead
---

# /research

phase_id: research
role: tech-lead

## Artifacts
- docs/engineering/research.md
- handoffs/tl_to_dev.md

## Validator bridge
Before writing to `docs/product/backlog.md` bug rows or `docs/product/acceptance.md` bug rows, run `python scripts/bug_issue_validate.py --repo . --check-acceptance` and surface any non-zero exit reason code to the operator. The orchestrator plugin enforces persistence.

STOP
