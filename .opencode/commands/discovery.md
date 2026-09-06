---
description: "its-magic discovery: collect UX and product references."
agent: po
---

# /discovery

phase_id: discovery
role: po

## Artifacts
- docs/product/vision.md
- handoffs/po_to_tl.md

## Validator bridge
Before writing to `handoffs/intake_evidence/*.json`, run `python scripts/intake_evidence_validate.py --repo . --enforce` and surface any non-zero exit reason code to the operator. The orchestrator plugin enforces persistence.

STOP
