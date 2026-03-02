# Tasks — Sprint S0013

## US-0041: End-to-End Lifecycle QA for `its-magic` Install/Upgrade/Clean

### T-001: Add PowerShell clean-repo safety lifecycle test
- Story: US-0041
- Status: done
- Files: `tests/run-tests.ps1`
- Description: Add deterministic clean-repo verification that framework artifacts
  are removed while non-its-magic marker files remain untouched.
- AC covered: AC-4, AC-8

### T-002: Add shell clean-repo safety lifecycle test
- Story: US-0041
- Status: done
- Files: `tests/run-tests.sh`
- Description: Mirror clean-repo safety verification in shell runner with same
  scope and idempotent temp-dir cleanup behavior.
- AC covered: AC-4, AC-7, AC-8
- Depends on: T-001

### T-003: Add PowerShell CLI lifecycle path tests (`its-magic` command)
- Story: US-0041
- Status: done
- Files: `tests/run-tests.ps1`, `bin/its-magic.js`
- Description: Validate CLI-driven install lifecycle for `missing`, `overwrite
  --backup`, and `upgrade` flows in temp dirs.
- AC covered: AC-1, AC-2, AC-3, AC-6, AC-8
- Depends on: T-002

### T-004: Add shell CLI lifecycle path tests (`its-magic` command)
- Story: US-0041
- Status: done
- Files: `tests/run-tests.sh`, `bin/its-magic.js`
- Description: Mirror CLI lifecycle path validation in shell runner for parity.
- AC covered: AC-1, AC-2, AC-3, AC-6, AC-7, AC-8
- Depends on: T-003

### T-005: Add negative-path lifecycle tests for invalid mode/args
- Story: US-0041
- Status: done
- Files: `tests/run-tests.ps1`, `tests/run-tests.sh`
- Description: Add fail-fast checks for invalid mode/arguments and verify
  non-zero exits with actionable output patterns.
- AC covered: AC-5, AC-6, AC-7
- Depends on: T-004

### T-006: Expand local npm package smoke to lifecycle subset
- Story: US-0041
- Status: done
- Files: `packaging/npm/test-npm-local.ps1`, `packaging/npm/test-npm-local.sh`
- Description: Extend npm local tests to include upgrade and clean-repo safety
  subset via `its-magic` command.
- AC covered: AC-3, AC-4, AC-6, AC-7
- Depends on: T-005

### T-007: Extend CI jobs with lifecycle subset checks
- Story: US-0041
- Status: done
- Files: `.github/workflows/ci.yml`
- Description: Add bounded lifecycle subset checks in CI for npm/brew/choco paths
  without increasing flakiness risk.
- AC covered: AC-7, AC-8
- Depends on: T-006

### T-008: Document lifecycle QA matrix in runbook
- Story: US-0041
- Status: done
- Files: `docs/engineering/runbook.md`
- Description: Document lifecycle QA matrix, expected pass/fail evidence, and
  command-level verification paths.
- AC covered: AC-9
- Depends on: T-007

### T-009: Document lifecycle QA matrix in README
- Story: US-0041
- Status: done
- Files: `README.md`
- Description: Add user-facing lifecycle QA coverage overview and where to run
  local/CI checks.
- AC covered: AC-9
- Depends on: T-008

### T-010: Validate active/template documentation parity for lifecycle references
- Story: US-0041
- Status: done
- Files: `template/README.md`, `template/docs/engineering/runbook.md`
- Description: Ensure lifecycle QA documentation references stay behaviorally
  aligned in template copies where applicable.
- AC covered: AC-7, AC-9
- Depends on: T-009

### T-011: Finalize traceability, plan-verify evidence, and handoff readiness
- Story: US-0041
- Status: done
- Files: `docs/engineering/state.md`, `handoffs/tl_to_dev.md`, `sprints/S0013/plan-verify.json`, `sprints/S0013/uat.md`, `sprints/S0013/uat.json`
- Description: Finalize sprint traceability row, coverage mapping, and execution
  handoff with lifecycle-specific QA focus.
- AC covered: AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9
- Depends on: T-010
