# Release notes - installer shell startup portability guard (DEC-0068 / BUG-0004)

## What shipped

- Installer startup contract in `installer.sh` now explicitly documents POSIX-safe `/bin/sh` requirements and forbids unconditional bash-only startup option bundles.
- Added BUG-0004 regression suite `tests/installer_shell_bug0004_test.py` for:
  - startup static guard against forbidden `set` bundles,
  - direct `sh installer.sh --mode missing`,
  - CLI Unix launcher path (`node bin/its-magic.js --mode missing`).
- Wired BUG-0004 suite into both `tests/run-tests.sh` and `tests/run-tests.ps1` (`26P`).
- Preserved non-regression against BUG-0003 completeness contract (`tests/installer_completeness_bug0003_test.py`).

## Gate summary

- Check-in test gate: PASS (`python tests/installer_shell_bug0004_test.py`; `python tests/installer_completeness_bug0003_test.py`).
- QA completion gate: PASS (`sprints/S0065/qa-findings.md`).
- UAT completion gate: PASS (`sprints/S0065/uat.json`, `sprints/S0065/uat.md`; `6/6`).
- Isolation gate: PASS (verify-work and release checkpoints recorded in `docs/engineering/state.md`).
- Strict runtime proof gate: PASS (`orchestrator_run_id=auto-20260403-01`).
- Release finalization: PASS (findings, canonical notes, queue row `released`, legacy pointer refreshed).

## Run

- `start_command`: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- `runtime_mode`: `local`
- `runtime_context_ref`: `docs/engineering/runbook.md` (TEST_COMMAND)

## Connect

- `service_url`: `local-workspace://` (repository root on operator machine)
- `service_port`: `n/a`
- `health_endpoint`: `tests/report.md` (consolidated baseline) + targeted checks in `## Verify`

## Verify

- `verification_steps`:
  1. Run `python tests/installer_shell_bug0004_test.py` (expect PASS; runtime path checks may skip when `sh`/`node` unavailable).
  2. Run `python tests/installer_completeness_bug0003_test.py` (expect PASS).
  3. Confirm `sprints/S0065/release-findings.md` verdict is `PASS` and `handoffs/release_queue.md` row `S0065` is `released`.
  4. Confirm canonical bug closure alignment: `docs/product/backlog.md` (`BUG-0004` = `DONE`) and `docs/product/acceptance.md` (`BUG-0004` checked).
- `expected_health_signal`: BUG-0004 fixture present and green, release findings PASS, queue row `released`, canonical bug status surfaces aligned.

## Credentials

- `credential_source_refs` (env names only): same as prior releases when publish targets are configured (`GITHUB_TOKEN`, target-specific `*Env` keys in `docs/engineering/release-targets.json`).
- Never place inline secrets in this file.

## Known issues

- On Windows hosts without `sh` or `node` in PATH, two runtime BUG-0004 checks are skipped by design; static startup guard still runs and enforces contract.

## Deploy (staging / production)

- **Staging:** `DEPLOY_STAGING_COMMAND` from `docs/engineering/runbook.md` - `echo "No staging deploy target configured for this repository"`
- **Production:** `DEPLOY_PROD_COMMAND` from `docs/engineering/runbook.md` - `echo "No production deploy target configured for this repository"`

## Evidence refs (engineering)

- `sprints/S0065/summary.md`
- `sprints/S0065/qa-findings.md`
- `sprints/S0065/uat.json`
- `sprints/S0065/uat.md`
- `sprints/S0065/release-findings.md`
- `decisions/DEC-0068.md`
- `tests/installer_shell_bug0004_test.py`
- `tests/installer_completeness_bug0003_test.py`
- `installer.sh`
