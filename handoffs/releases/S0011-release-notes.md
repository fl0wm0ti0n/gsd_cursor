# Release notes — S0011 (US-0039)

## Summary

- **Sprint:** S0011  
- **Story:** US-0039 — Release Gate Tightening for Check-In Tests and QA/UAT Completion  
- **Release date:** 2026-03-02  
- **Status:** Released  

## Scope

Mandatory release gate chain (check-in test → QA → UAT → finalization), evidence validity contract, no-bypass default, override evidence contract, per-gate audit schema, and optional-command compatibility (blank LINT/TYPECHECK do not fail release).

## Delivered

- **AC-1:** Mandatory check-in test gate in `/release` (TEST_COMMAND baseline).
- **AC-2:** Release blocked on missing/stale/failing test evidence with RELEASE_TEST_EVIDENCE_MISSING, RELEASE_TEST_STALE, RELEASE_TEST_FAILED.
- **AC-3:** Release blocked when QA blockers remain; QA completion gate in release.md, qa.md, handoffs/qa_to_dev.md.
- **AC-4:** UAT completeness gate mandatory and strict (RELEASE_UAT_INCOMPLETE, RELEASE_UAT_FAILED).
- **AC-5:** Deterministic gate order: check-in test → QA → UAT → finalize.
- **AC-6:** Per-gate audit verdict (verdict, reason_code, remediation, evidence_refs) in state/handoff/runbook.
- **AC-7:** No default bypass; override requires decision-gate evidence (DEC-0019, release.md, core.mdc).
- **AC-8:** Active/template release semantics parity (release.md, qa, execute, runbook, README).
- **AC-9:** Regression coverage: positive/negative/stale-evidence matrix in S0011 uat, plan-verify, tests.
- **AC-10:** Blank optional LINT/TYPECHECK runbook keys do not cause false release failure (runbook US-0039 AC-10).

## Gate evidence

| Gate             | Result | Evidence |
|------------------|--------|----------|
| Check-in tests   | PASS   | tests/report.md 2026-03-01T23:44:53Z, Pass: 349, Fail: 0 |
| QA completion    | PASS   | sprints/S0011/qa-findings.md, no blockers |
| UAT completeness | PASS   | sprints/S0011/uat.json (10/10), uat.md, verified_state=true |
| Backlog reconciliation | — | US-0039 → DONE, ACs checked |

## Artifacts

- `.cursor/commands/release.md`, `docs/engineering/runbook.md` (gate chain, evidence contract, no-bypass, override)
- `sprints/S0011/uat.md`, `sprints/S0011/uat.json` (regression matrix, gate failure behavior)
- `sprints/S0011/qa-findings.md`, `sprints/S0011/release-findings.md`
- `decisions/DEC-0019.md`, `.cursor/rules/core.mdc`
- `tests/run-tests.ps1`, `tests/run-tests.sh` (US-0039 regression assertions)
- Template parity: `template/.cursor/commands/release.md` (QA/UAT gate sections)

## Notes

- Gate order is strict and documented; no step may be skipped or reordered.
- Optional runbook keys (LINT_COMMAND, TYPECHECK_COMMAND) when blank are reported as skipped and do not block release.
