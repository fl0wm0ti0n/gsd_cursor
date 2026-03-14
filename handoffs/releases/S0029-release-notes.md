# Release notes — S0029 (US-0050)

## Summary

- **Sprint:** S0029
- **Story:** US-0050 — Clean Install Hygiene and Complete Clean-Repo Coverage
- **Release date:** 2026-03-11
- **Status:** Released

## Scope

Deterministic install hygiene and cleanup coverage for `its-magic`: one ownership
source for installer paths, ownership-complete clean-repo behavior, neutral starter
engineering artifacts, hardcoded-ID neutralization, and lifecycle regression
coverage across install/upgrade/clean paths.

## Delivered

- **AC-1:** `--clean-repo` removes installer-owned artifacts with ownership-complete scope (including `.cursor`, docs, scripts, CI files, version marker).
- **AC-2:** Ownership contract defined once and consumed by `installer.ps1`, `installer.sh`, `installer.py`.
- **AC-3:** Cleanup remains non-destructive for non-framework files; safety checks passing.
- **AC-4:** Seeded operational starter history removed in `template/docs/engineering/*` neutral artifacts.
- **AC-5:** Hardcoded starter runtime reference (`DEC-0011`) removed from starter research guidance.
- **AC-6:** Fresh install baseline checks confirm neutral placeholders/no preloaded history rows.
- **AC-7:** Upgrade behavior preserved (framework updates + user-data preservation).
- **AC-8:** Regression coverage expanded for fresh install, clean-repo completeness, reinstall, and entry-point parity.
- **AC-9:** Active/template install-clean contracts remain aligned.

## Gate evidence

| Gate | Result | Evidence |
|------|--------|----------|
| Check-in tests | PASS | `tests/report.md` 2026-03-11T22:12:04Z, Pass: 404, Fail: 0 |
| QA completion | PASS | `sprints/S0029/qa-findings.md`, no blockers |
| UAT completeness | PASS | `sprints/S0029/uat.json` and `sprints/S0029/uat.md` (9/9) |
| Isolation compliance | PASS | `docs/engineering/state.md` execute + qa + verify-work evidence for S0029 |
| Backlog reconciliation | PASS | `US-0050` set to DONE; AC checkboxes reconciled |

## Artifacts

- `docs/engineering/context/installer-owned-paths.manifest`
- `template/docs/engineering/context/installer-owned-paths.manifest`
- `installer.ps1`, `installer.sh`, `installer.py`
- `template/docs/engineering/status-normalization-report.md`
- `template/docs/engineering/compatibility-report.md`
- `template/docs/engineering/compatibility-signals.md`
- `template/docs/engineering/component-scope.md`
- `template/docs/engineering/component-scope-report.md`
- `template/docs/engineering/research.md`
- `packaging/homebrew/its-magic.rb`
- `sprints/S0029/qa-findings.md`, `sprints/S0029/uat.json`, `sprints/S0029/uat.md`, `sprints/S0029/release-findings.md`
