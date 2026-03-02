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

## UAT execution results (verify-work 2026-03-02)

| Step | Description | Result | AC(s) | Evidence |
|------|--------------|--------|-------|----------|
| UAT-1 | Release starts with check-in test gate and blocks on missing evidence | **PASS** | AC-1, AC-2 | release.md, qa-findings.md |
| UAT-2 | Release blocks on stale test evidence (RELEASE_TEST_STALE) | **PASS** | AC-2 | release.md, state.md |
| UAT-3 | Release blocks on failing test evidence (RELEASE_TEST_FAILED) | **PASS** | AC-2 | release.md, run-tests.ps1 |
| UAT-4 | Release blocks when QA findings include unresolved blockers | **PASS** | AC-3 | release.md, qa-findings.md |
| UAT-5 | Release blocks when UAT artifacts are placeholder or incomplete | **PASS** | AC-4 | release.md, uat.md |
| UAT-6 | Deterministic gate order: check-in test → QA → UAT → finalize | **PASS** | AC-5 | release.md, runbook.md |
| UAT-7 | No non-decision bypass path for failing mandatory gates | **PASS** | AC-7 | release.md, core.mdc |
| UAT-8 | Override path requires decision gate and rationale (RELEASE_GATE_OVERRIDE_APPROVED) | **PASS** | AC-7 | DEC-0019.md, release.md |
| UAT-9 | Per-gate verdict log includes status, reason_code, evidence_refs | **PASS** | AC-6 | state.md, runbook.md |
| UAT-10 | Blank optional runbook keys do not trigger false release failure | **PASS** | AC-10 | runbook.md, qa-findings.md |

**Totals:** Passed: 10 | Failed: 0 | Total: 10

**Verdict:** **UAT PASS** — All US-0039 acceptance criteria covered by executed steps; no unresolved failures.

### AC-linked summary

- **AC-1, AC-2**: Check-in test gate and evidence validity (missing/stale/fail) — UAT-1, UAT-2, UAT-3 PASS.
- **AC-3**: QA completion gate — UAT-4 PASS.
- **AC-4**: UAT completeness gate — UAT-5 PASS.
- **AC-5**: Deterministic gate ordering — UAT-6 PASS.
- **AC-6**: Per-gate audit evidence in state/handoff — UAT-9 PASS.
- **AC-7**: No default bypass; override requires decision evidence — UAT-7, UAT-8 PASS.
- **AC-8**: Template parity — verified in QA (release.md active/template); regression matrix in plan-verify.json.
- **AC-9**: Regression coverage (positive/negative/stale) — plan-verify.json regression_matrix_planned; tests/run-tests.ps1 US-0039 assertions.
- **AC-10**: Optional blank LINT/TYPECHECK do not fail release — UAT-10 PASS; runbook Optional-command compatibility (US-0039).

## UAT gate failure behavior (US-0039)

Explicit failure behavior for release block:

- **Placeholder**: `uat.json`/`uat.md` empty or template-only → `RELEASE_UAT_INCOMPLETE`; remediation: run `/verify-work`, populate UAT, rerun `/release`.
- **Incomplete**: Steps exist but not all have results or passed+failed ≠ total → `RELEASE_UAT_INCOMPLETE`; complete UAT, rerun `/release`.
- **Unresolved fail**: One or more steps failed and not resolved → `RELEASE_UAT_FAILED`; resolve or document acceptance, rerun `/release`.

Verified state = all steps populated, results recorded, no unresolved fail.

## Release gate regression matrix (US-0039)

| Scenario | Gate | Expected | Reason code / evidence |
|----------|------|----------|------------------------|
| Positive: test pass, QA clear, UAT complete | all | PASS | All gates pass; finalization proceeds |
| Negative: missing test evidence | check-in test | BLOCK | RELEASE_TEST_EVIDENCE_MISSING |
| Negative: stale test evidence | check-in test | BLOCK | RELEASE_TEST_STALE |
| Negative: failing tests | check-in test | BLOCK | RELEASE_TEST_FAILED |
| Negative: unresolved QA blockers | QA | BLOCK | RELEASE_QA_BLOCKERS_OPEN |
| Negative: missing QA evidence | QA | BLOCK | RELEASE_QA_EVIDENCE_MISSING |
| Negative: placeholder UAT | UAT | BLOCK | RELEASE_UAT_INCOMPLETE |
| Negative: unresolved UAT fail | UAT | BLOCK | RELEASE_UAT_FAILED |
| No-bypass: no silent skip | default | BLOCK | No non-decision bypass path |
| Override: with decision evidence | override | ALLOW | RELEASE_GATE_OVERRIDE_APPROVED + DEC ref |

Coverage: positive (all gates pass), negative (each gate blocks with correct reason code), stale evidence (test/QA/UAT), no-bypass behavior, override with evidence.

## Negative-path focus

- Missing QA/UAT completion evidence blocks release.
- No-bypass release gate behavior is enforced by default.
- Decision-gate override path requires explicit evidence and rationale.
