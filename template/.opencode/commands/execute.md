---
description: "its-magic execute: implement tasks."
agent: dev
---

# /execute

phase_id: execute
role: dev

## Artifacts
- sprints/Sxxxx/progress.md
- sprints/Sxxxx/summary.md
- handoffs/dev_to_qa.md

## Validator bridge
Before writing to `handoffs/intake_evidence/*.json`, run `python scripts/intake_evidence_validate.py --repo . --enforce` and surface any non-zero exit reason code to the operator. The orchestrator plugin enforces persistence.

STOP
