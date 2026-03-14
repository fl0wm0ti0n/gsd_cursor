# Sprint S0029 Progress

- Story: `US-0050`
- Status: RELEASE COMPLETE
- Started: 2026-03-11
- Completed: 2026-03-11

## Task status

- Done: 10
- Pending: 0
- Blocked: 0

## Notes

- Implemented manifest-driven installer ownership contract across `installer.ps1`, `installer.sh`, and `installer.py`.
- Expanded clean-repo scope via manifest-owned paths, including docs/user-guides, validation scripts, CI workflow files, and `.its-magic-version`.
- Neutralized seeded starter history in template engineering artifacts (`status-normalization-report`, `compatibility-*`, `component-scope-*`) and removed hardcoded `DEC-0011` reference in template research header.
- Added fresh-install neutrality checks and clean-repo completeness assertions in both `tests/run-tests.ps1` and `tests/run-tests.sh`.
- Fixed QA blockers by syncing stable Homebrew formula (`packaging/homebrew/its-magic.rb`) to npm version `0.1.2-20` (URL/version/SHA256).
- Test run: `tests/run-tests.ps1` -> Pass 404, Fail 0 (`tests/report.md`, 2026-03-11T22:12:04Z).
- QA rerun PASS; no blocking findings remain for S0029.
- Verify-work completed: UAT PASS (`sprints/S0029/uat.json`, `sprints/S0029/uat.md`) with 9/9 steps passing and AC-1..AC-9 covered.
- Release finalized: queue row `S0029` set to `released`, canonical notes written at `handoffs/releases/S0029-release-notes.md`, backlog/acceptance reconciled for `US-0050`.
