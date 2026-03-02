# UAT — Sprint S0013

## Target

- **US-0041**: End-to-End Lifecycle QA for `its-magic` Install/Upgrade/Clean
  - AC-1: Fresh install lifecycle validation (`missing`) with required artifacts
    and version file behavior
  - AC-2: Overwrite + backup lifecycle validation and recoverability guidance
  - AC-3: Upgrade lifecycle validation for framework refresh + user-data preserve
    + new-file delivery
  - AC-4: Clean-repo lifecycle safety validation (remove framework artifacts,
    preserve non-framework files)
  - AC-5: Negative-path fail-fast coverage for invalid mode/args and malformed
    target state
  - AC-6: CLI entrypoint and direct installer path parity validation
  - AC-7: PowerShell/shell/CI lifecycle parity coverage
  - AC-8: Isolated and idempotent temp-dir execution/cleanup behavior
  - AC-9: Lifecycle QA matrix documented in README and runbook

## Executed verification steps and results

1. **AC-1** - Verified fresh install lifecycle checks validate required artifacts
   and `.its-magic-version` creation.
   **Result:** PASS
   **Evidence:** `tests/run-tests.ps1`, `tests/run-tests.sh`
2. **AC-2** - Verified overwrite + backup lifecycle checks confirm backup snapshot
   behavior.
   **Result:** PASS
   **Evidence:** `tests/run-tests.ps1`, `tests/run-tests.sh`
3. **AC-3** - Verified upgrade lifecycle checks confirm framework refresh and
   user-data preservation.
   **Result:** PASS
   **Evidence:** `tests/run-tests.ps1`, `tests/run-tests.sh`,
   `packaging/npm/test-npm-local.ps1`, `packaging/npm/test-npm-local.sh`
4. **AC-4** - Verified clean-repo safety checks confirm framework removal and
   non-framework marker preservation.
   **Result:** PASS
   **Evidence:** `tests/run-tests.ps1`, `tests/run-tests.sh`,
   `packaging/npm/test-npm-local.ps1`, `packaging/npm/test-npm-local.sh`,
   `.github/workflows/ci.yml`
5. **AC-5** - Verified invalid-mode negative-path checks exist and fail fast.
   **Result:** PASS
   **Evidence:** `tests/run-tests.ps1`, `tests/run-tests.sh`
6. **AC-6** - Verified lifecycle coverage exists for both CLI and direct installer
   execution paths.
   **Result:** PASS
   **Evidence:** `tests/run-tests.ps1`, `tests/run-tests.sh`
7. **AC-7** - Verified platform parity subset for PowerShell/shell and CI
   npm/brew/choco jobs.
   **Result:** PASS
   **Evidence:** `.github/workflows/ci.yml`
8. **AC-8** - Verified isolated/idempotent temp-dir test design with cleanup.
   **Result:** PASS
   **Evidence:** `tests/run-tests.ps1`, `tests/run-tests.sh`
9. **AC-9** - Verified lifecycle QA matrix documentation and template parity.
   **Result:** PASS
   **Evidence:** `README.md`, `docs/engineering/runbook.md`,
   `template/README.md`, `template/docs/engineering/runbook.md`

## Negative-path focus

- Invalid mode handling fails fast in both PowerShell and shell runners.
- Clean-repo safety preserves non-framework markers in lifecycle test targets.
- Existing baseline non-US-0041 failures remain tracked separately and do not
  block US-0041 acceptance validation.
