---
description: "its-magic intake: capture idea, backlog, acceptance."
agent: po
---

# /intake

phase_id: intake
role: po

## Artifacts
- docs/product/backlog.md
- docs/product/acceptance.md
- handoffs/po_to_tl.md

## Validator bridge
Before writing to `handoffs/intake_evidence/*.json`, run `python scripts/intake_evidence_validate.py --repo . --enforce` and surface any non-zero exit reason code to the operator. The orchestrator plugin enforces persistence.

STOP
