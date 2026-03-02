# Sprint S0013

## Goal

Deliver `US-0041` (End-to-End Lifecycle QA for `its-magic` Install/Upgrade/Clean)
with live lifecycle validation for installer + CLI paths, including backup,
cleanup safety, negative-path handling, and platform parity evidence.

## Scope

- **In scope**: `US-0041` (AC-1..AC-9).
- **Out of scope**: redesigning installer semantics or introducing new install
  modes outside current contract.

## Sizing Check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 11
- 11 < 12 -> within threshold. Single-story sprint, no split required.

## Milestone Check

- Milestone activation: **not applicable** for this sprint.
- Reason: no active milestone lifecycle is declared for `US-0041` in current
  planning context; sprint remains standalone and story-scoped.

## Prerequisites

- `US-0041` acceptance criteria are present in `docs/product/backlog.md`.
- Existing lifecycle test baseline exists in:
  - `tests/run-tests.ps1`
  - `tests/run-tests.sh`
  - `packaging/npm/test-npm-local.ps1`
  - `packaging/npm/test-npm-local.sh`
  - `.github/workflows/ci.yml`

## Key Decisions

- Prioritize highest-risk lifecycle gaps first: clean-repo safety, CLI lifecycle
  path coverage, and negative-path validation.
- Keep tests isolated/idempotent using temporary directories with deterministic
  cleanup.

## Implementation Order

Execute tasks `T-001` through `T-011` in sequence. First close lifecycle gaps in
core test runners (`T-001`..`T-005`), then extend packaging/CI lifecycle subset
coverage (`T-006`..`T-007`), then document matrix and close traceability/handoff
artifacts (`T-008`..`T-011`).

## Risks

| Risk | Mitigation |
|------|------------|
| Clean-repo tests accidentally remove non-test files | Use dedicated temp dirs and assert safety markers before/after cleanup. |
| CLI and installer behavior drift across platforms | Add parity assertions in PS/sh runners and CI subset checks. |
| Negative-path behavior remains non-deterministic | Add explicit invalid-argument/invalid-mode tests with fail-fast expectations. |
| Expanded tests become flaky | Keep tests local-temp only, deterministic setup/teardown, and bounded timeouts. |
| Docs drift from implemented behavior | Update runbook/README lifecycle matrix in same sprint and verify references. |

## Definition of Done

- Fresh install lifecycle checks validate required artifacts and version file
  behavior (AC-1).
- Overwrite + backup lifecycle checks validate snapshot behavior and recoverability
  guidance (AC-2).
- Upgrade lifecycle checks validate framework refresh + user-data preservation +
  new-file delivery expectations (AC-3).
- Clean-repo lifecycle checks validate removal scope safety against non-framework
  files (AC-4).
- Negative-path checks validate deterministic fail-fast behavior and actionable
  messaging coverage (AC-5).
- CLI entrypoint and direct installer path parity checks are present in test
  suites (AC-6).
- Platform parity is covered across PowerShell/shell local runners and CI
  lifecycle subset jobs (AC-7).
- Tests are isolated/idempotent with explicit temp-dir cleanup on success/failure
  paths (AC-8).
- Lifecycle QA matrix and evidence expectations are documented in `README.md` and
  `docs/engineering/runbook.md` (AC-9).
