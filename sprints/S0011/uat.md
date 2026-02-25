# UAT — Sprint S0011

## Target

- **US-0039**: Release Gate Tightening for Check-In Tests and QA/UAT Completion
  - AC-1: Mandatory check-in test gate in `/release`
  - AC-2: Release blocked on missing/stale/failing test evidence
  - AC-3: Release blocked when QA blockers remain unresolved
  - AC-4: UAT completeness gate remains mandatory and strict
  - AC-5: Deterministic release gate ordering
  - AC-6: Per-gate audit evidence in state/handoff artifacts
  - AC-7: No default bypass; override requires decision-gate evidence
  - AC-8: Active/template release semantics parity
  - AC-9: Positive and negative stale-evidence regression coverage
  - AC-10: Optional blank lint/typecheck keys do not cause false failure

## Planned verification steps

1. Verify release starts with check-in test gate and blocks on missing evidence.
2. Verify release blocks on stale test evidence with deterministic reason code.
3. Verify release blocks on failing test evidence with remediation guidance.
4. Verify release blocks when QA findings include unresolved blockers.
5. Verify release blocks when UAT artifacts are placeholder or incomplete.
6. Verify deterministic gate order is always test -> QA -> UAT -> finalize.
7. Verify no non-decision bypass path exists for failing mandatory gates.
8. Verify override path requires explicit decision gate and rationale evidence.
9. Verify per-gate verdict log includes status, reason code, and evidence refs.
10. Verify blank optional runbook keys do not trigger false release failure.

## Negative-path focus

- Missing QA/UAT completion evidence blocks release.
- No-bypass release gate behavior is enforced by default.
- Decision-gate override path requires explicit evidence and rationale.
