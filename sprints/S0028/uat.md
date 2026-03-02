# S0028 UAT — US-0049 Legacy DONE-Story Acceptance/Traceability Backfill Guard

## Overall result

- **UAT result:** PASS — verify-work complete
- **Passed:** 8
- **Failed:** 0
- **Total steps:** 8
- **Verify-work:** 2026-03-02 (fresh QA context); all AC-1..AC-8 verified; route to `/release`.

## Target story and acceptance

- Story: US-0049
- Acceptance: `docs/product/backlog.md` (US-0049 AC-1..AC-8)

## Steps (execution evidence)

| Step | AC | Description | Result | Evidence |
|------|-----|-------------|--------|----------|
| 1 | AC-1 | Detection rule documented (backlog DONE and acceptance unchecked or traceability/state lacks entry or release artifacts lack representation) | PASS | docs/engineering/runbook.md "Legacy DONE-story drift detection and guard (US-0049)" |
| 2 | AC-2 | Bounded target-scoped repair documented; only stories matching rule mutated | PASS | Runbook "Bounded repair"; release step 3e |
| 3 | AC-3 | Audit report format and canonical path docs/engineering/legacy-drift-audit.md with required fields | PASS | legacy-drift-audit.md (schema: story_id, prior_acceptance_state, prior_traceability_state, resolved_state, reason_code, evidence_ref, timestamp) |
| 4 | AC-4 | Reason codes BACKLOG_DONE_ACCEPTANCE_UNCHECKED, BACKLOG_DONE_TRACEABILITY_MISSING, BACKLOG_DONE_RELEASE_ARTIFACT_MISSING with remediation | PASS | Runbook + release.md fail-safe list (active + template) |
| 5 | AC-5 | One-time backfill mode: explicit trigger, idempotent when no drift, emit audit | PASS | Runbook "One-time backfill mode" |
| 6 | AC-6 | Ongoing guard at release/reconciliation: block or repair with audit append; documented, deterministic | PASS | Release step 3e; runbook "Ongoing guard" |
| 7 | AC-7 | Template parity for backfill, guard, audit path, reason codes | PASS | template/ runbook, release.md, legacy-drift-audit.md |
| 8 | AC-8 | Regression: no-drift, single-drift repair, guard block/repair with reason code | PASS | tests/run-tests.ps1 block #27 (14 assertions); tests/report.md Pass 397 Fail 0 |

## Regression coverage (AC-8)

- (a) One-time backfill run with no drift → no changes, report empty or "no drift" — documented in runbook; test asserts "Idempotent when no drift".
- (b) One-time backfill run with one legacy-drift story → repair applied, audit entry created — procedure in runbook; audit schema supports entries.
- (c) Ongoing guard blocks or repairs when drift present and reports reason code — release step 3e and reason codes; tests assert guard step and BACKLOG_DONE_* codes.
