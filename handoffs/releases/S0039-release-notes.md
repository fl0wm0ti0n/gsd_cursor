# Release Notes - Sprint S0039

- Sprint: `S0039`
- Story: `US-0060`
- Date: 2026-03-14
- Status: released

## Highlights

- Added deterministic state rollover threshold controls:
  - `STATE_HOT_MAX_LINES`
  - `STATE_HOT_MAX_CHECKPOINTS`
- Added enforced rollover contract in `/refresh-context` for hot-surface bounds.
- Added fail-safe reason codes for archive boundary/write failures:
  - `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS`
  - `STATE_ARCHIVE_WRITE_FAILED`
- Updated artifact ordering/runbook/README/test contracts with parity coverage.

## Verification

- QA: PASS (`sprints/S0039/qa-findings.md`)
- UAT: PASS (`sprints/S0039/uat.json`, `sprints/S0039/uat.md`)
- Release gate: PASS (`sprints/S0039/release-findings.md`)
