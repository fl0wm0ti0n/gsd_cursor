# Release notes — S0028 (US-0049)

## Summary

- **Sprint:** S0028  
- **Story:** US-0049 — Legacy DONE-Story Acceptance/Traceability Backfill Guard  
- **Release date:** 2026-03-02  
- **Status:** Released  

## Scope

Deterministic detection and bounded repair for legacy stories where backlog is DONE but acceptance checkmarks, traceability/state, or release artifacts disagree. Includes one-time backfill mode, ongoing guard at release/reconciliation, audit report, reason codes, and template parity.

## Delivered

- **AC-1:** Detection rule documented in runbook: legacy drift = backlog DONE and (acceptance unchecked OR traceability/state lacks entry OR release artifacts lack representation).
- **AC-2:** Bounded target-scoped repair: only stories matching the rule are mutated; runbook and release step 3e.
- **AC-3:** Canonical audit artifact `docs/engineering/legacy-drift-audit.md` with required fields (story_id, prior_acceptance_state, prior_traceability_state, resolved_state, reason_code, evidence_ref, timestamp); active + template.
- **AC-4:** Reason codes: `BACKLOG_DONE_ACCEPTANCE_UNCHECKED`, `BACKLOG_DONE_TRACEABILITY_MISSING`, `BACKLOG_DONE_RELEASE_ARTIFACT_MISSING` with remediation in runbook and release fail-safe list.
- **AC-5:** One-time backfill mode: explicit trigger, detection over DONE stories, target-scoped repair, append audit; idempotent when no drift (runbook).
- **AC-6:** Ongoing guard at release: step 3e in release.md — block or target-scoped repair with audit append; deterministic (active + template).
- **AC-7:** Template parity: `template/docs/engineering/runbook.md`, `template/.cursor/commands/release.md`, `template/docs/engineering/legacy-drift-audit.md` aligned with active.
- **AC-8:** Regression: 14 US-0049 assertions in `tests/run-tests.ps1` (canonical path, runbook section, reason codes, idempotent no-drift, release guard); Pass 397, Fail 0.

## Gate evidence

| Gate | Result | Evidence |
|------|--------|----------|
| Check-in tests | PASS | tests/report.md 2026-03-02T22:00:35Z, Pass: 397, Fail: 0 |
| QA completion | PASS | sprints/S0028/qa-findings.md, no blockers |
| UAT completeness | PASS | sprints/S0028/uat.json (8/8), uat.md |
| Isolation compliance | PASS | state.md execute + qa + verify-work phase evidence for S0028 |
| Backlog reconciliation | — | US-0049 → DONE, ACs checked |

## Artifacts

- `docs/engineering/runbook.md` — Legacy DONE-story drift detection and guard (US-0049)
- `docs/engineering/legacy-drift-audit.md` (active + template)
- `.cursor/commands/release.md` — step 3e, three reason codes (active + template)
- `tests/run-tests.ps1` — block #27 US-0049 regression (14 assertions)
