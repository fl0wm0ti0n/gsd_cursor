# Release Notes — S0033 (US-0054)

- Sprint: `S0033`
- Story: `US-0054`
- Date: 2026-03-13
- Status: released

## Scope delivered

- Added configurable multi-target publish controls in scratchpad:
  `RELEASE_PUBLISH_MODE`, `RELEASE_TARGETS_FILE`, `RELEASE_TARGETS_DEFAULT`.
- Added canonical target schema (`docs/engineering/release-targets.json`) with
  built-in targets and generic `custom` + `ssh` support.
- Added runbook/README guidance for default confirmation-gated publish behavior.
- Extended release command contract with deterministic target validation,
  selection/order rules, and reason codes:
  `PUBLISH_TARGET_CONFIG_INVALID`, `PUBLISH_CONFIRMATION_REQUIRED`,
  `PUBLISH_TARGET_EXECUTION_FAILED`.
- Added regression coverage for US-0054 contract and parity assertions in both
  test runners.

## Gate evidence

- tests: `tests/report.md` (2026-03-13T17:09:21Z, Pass: 476, Fail: 0)
- QA: `sprints/S0033/qa-findings.md` (PASS)
- UAT: `sprints/S0033/uat.json`, `sprints/S0033/uat.md` (10/10 PASS)
- release audit: `sprints/S0033/release-findings.md` (PASS)

## Finalization

- Backlog status reconciled: `US-0054` -> `DONE`.
- Acceptance status reconciled: `US-0054` checked.
- Release queue updated: `S0033` -> `released`.
