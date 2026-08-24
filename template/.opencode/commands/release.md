---
description: "its-magic release: release notes and runbook updates."
agent: release
---

# /release

phase_id: release
role: release

## Artifacts
- handoffs/release_queue.md
- handoffs/releases/Sxxxx-release-notes.md
- handoffs/release_notes.md

## Validator bridge
Before writing to `handoffs/release_queue.md` or `handoffs/releases/*-release-notes.md`, run `python scripts/bug_issue_validate.py --repo . --check-acceptance` and surface any non-zero exit reason code to the operator. The orchestrator plugin enforces persistence.

STOP
