# Release Queue Tracker

Canonical release queue for sprint-level release state.

## Queue rows

| sprint_id | story_refs | status | last_updated | release_notes_ref | gate_snapshot | release_version | remediation |
|-----------|------------|--------|--------------|-------------------|---------------|-----------------|-------------|

## Status model

- `planned`: sprint exists, release flow not entered
- `ready`: verify-work completed and release is eligible to start
- `unreleased`: release flow entered; notes written; finalization not completed
- `released`: release finalization completed for the sprint
- `blocked`: deterministic fail-safe condition requiring remediation

## Deterministic transition contract

- Allowed lifecycle: `planned -> ready -> unreleased -> released`.
- `blocked` can be set on deterministic failure conditions.
- Only the target sprint row may change during one `/release` run.
- No destructive auto-reconciliation is allowed by default.

## Fail-safe reason codes

- `RELEASE_SPRINT_UNRESOLVED`
- `LEGACY_NOTES_SPRINT_UNRESOLVED`
- `QUEUE_ENTRY_MISSING`
- `NOTES_REF_MISSING`
- `STATUS_TRANSITION_INVALID`
- `BACKLOG_STATUS_DRIFT`
- `CANONICAL_STATUS_CONFLICT`
- `COMPATIBILITY_CRITICAL_OPEN`
- `COMPONENT_SCOPE_VIOLATION_UNAPPROVED`

## Remediation guidance

- `RELEASE_SPRINT_UNRESOLVED`: set explicit sprint context (`Sxxxx`) and rerun `/release`.
- `LEGACY_NOTES_SPRINT_UNRESOLVED`: preserve legacy notes, identify sprint manually, then create target sprint notes file.
- `QUEUE_ENTRY_MISSING`: create the target sprint queue row with required fields, then rerun `/release`.
- `NOTES_REF_MISSING`: add canonical `release_notes_ref` for target sprint row and rerun `/release`.
- `STATUS_TRANSITION_INVALID`: correct row status to a valid predecessor state and rerun `/release`.
- `BACKLOG_STATUS_DRIFT`: reconcile target story status/ACs in `docs/product/backlog.md` using release evidence, then rerun `/release`.
- `CANONICAL_STATUS_CONFLICT`: resolve canonical backlog status mismatch versus derived artifacts and rerun `/release`.
- `COMPATIBILITY_CRITICAL_OPEN`: resolve or explicitly decide on open critical compatibility findings before rerun.
- `COMPONENT_SCOPE_VIOLATION_UNAPPROVED`: resolve or explicitly approve out-of-scope component impact before rerun.
