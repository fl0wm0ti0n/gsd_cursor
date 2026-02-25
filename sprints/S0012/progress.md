# Progress — Sprint S0012

## Summary
- Sprint lifecycle status: dev-complete
- Total tasks: 11
- Done: 11
- In progress: 0
- Pending: 0

## Task status
| Task | Story | Status | Notes |
|------|-------|--------|-------|
| T-001 | US-0040 | done | Canonical sprint-scoped notes contract and path added in active/template `/release` guidance plus `handoffs/releases/Sxxxx-release-notes.md` placeholders |
| T-002 | US-0040 | done | Canonical queue schema added via `handoffs/release_queue.md` and runbook updates (active/template) |
| T-003 | US-0040 | done | Deterministic `ready -> unreleased -> released` target-sprint-only transition semantics defined |
| T-004 | US-0040 | done | Unresolved sprint fail-safe and reason-code contract added (`RELEASE_SPRINT_UNRESOLVED`) |
| T-005 | US-0040 | done | Legacy migration/backfill contract defined as non-destructive and idempotent |
| T-006 | US-0040 | done | Legacy `handoffs/release_notes.md` converted to backward-compatible pointer/summary behavior |
| T-007 | US-0040 | done | Queue/notes mismatch fail-safe handling and reason codes defined |
| T-008 | US-0040 | done | Unreleased queue visibility requirements added to legacy pointer and release flow guidance |
| T-009 | US-0040 | done | Ownership and phase touchpoints aligned across `/release`, `core.mdc`, and `handoffs.mdc` |
| T-010 | US-0040 | done | Active/template parity enforced for command, rules, runbook, README, and new release artifacts |
| T-011 | US-0040 | done | Regression matrix added to `S0012` UAT + plan-verify and automated checks added in both test runners |

## Validation evidence
- Automated regression suite: `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`
  - Result: PASS (`Pass: 142`, `Fail: 0`)
  - Evidence: `tests/report.md` (`Timestamp: 2026-02-25T23:11:21Z`)
- Positive path checks passed:
  - sprint-scoped canonical notes path checks
  - queue artifact and target-sprint-only transition semantics checks
- Negative/fail-safe checks passed:
  - unresolved sprint fail-safe reason-code contract checks
  - mismatch reason-code contract checks (`QUEUE_ENTRY_MISSING`,
    `NOTES_REF_MISSING`, `STATUS_TRANSITION_INVALID`)
- Migration/backward-compatibility checks passed:
  - legacy unresolved migration reason-code contract checks
  - legacy pointer behavior + queue visibility checks
- Parity checks passed across active/template release command, runbook, and README.
