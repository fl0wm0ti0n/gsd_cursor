# QA findings - Sprint S0065 (BUG-0004 / DEC-0068)

- **Verdict**: PASS
- **Scope**: POSIX-safe installer shell startup contract and regression harness wiring.
- **Orchestrator run**: `auto-20260403-01`

## Checks

1. `python tests/installer_shell_bug0004_test.py` -> PASS (`Ran 3`, `skipped=2` on Windows host lacking `sh`/`node` in PATH).
2. `python tests/installer_completeness_bug0003_test.py` -> PASS (non-regression against DEC-0066 completeness checks).
3. Static contract check in fixture confirms forbidden startup token bundles absent from `installer.sh`.
4. `tests/run-tests.sh` and `tests/run-tests.ps1` include section `26P` and execute BUG-0004 fixture.

## Findings

- No in-scope blockers.
- Environment caveat captured: runtime shell path checks are skipped when `sh` or `node` is unavailable; static guard remains active.

## Evidence refs

- `installer.sh`
- `tests/installer_shell_bug0004_test.py`
- `tests/run-tests.sh`
- `tests/run-tests.ps1`
- `tests/installer_completeness_bug0003_test.py`
