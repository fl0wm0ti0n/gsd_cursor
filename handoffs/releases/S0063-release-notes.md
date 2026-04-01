# Release notes — installer completeness hardening (DEC-0066 / BUG-0003)

## What shipped

- Installer completeness is now enforced by a manifest-authoritative required-script contract (`[required_install_script_paths]`) in active and template `installer-owned-paths.manifest`.
- `scripts/enforce-triad-hot-surface.py` is now explicitly owned for install and clean paths and mirrored under `template/scripts/`.
- `installer.py` enforces deterministic post-install completeness for `missing` and `upgrade` (`INSTALL_COMPLETENESS_FAILED`, `INSTALL_REQUIRED_SCRIPT_MISSING:<path>`).
- Wrapper parity is preserved: `installer.ps1` and `installer.sh` delegate to Python completeness validation (`--validate-install-completeness`) with the same reason-code surface.
- Regression coverage ships in `tests/installer_completeness_bug0003_test.py`, wired into `tests/run-tests.ps1` and `tests/run-tests.sh`.

## Gate summary

- Check-in test gate: PASS (`tests/report.md`; `Pass: 779`, `Fail: 2` Homebrew baseline out of scope).
- QA completion gate: PASS (`sprints/S0063/qa-findings.md`).
- UAT completion gate: PASS (`sprints/S0063/uat.json`, `sprints/S0063/uat.md`; `10/10`).
- Isolation gate: PASS (verify-work and release checkpoints on `docs/engineering/state.md`).
- Strict runtime proof gate: PASS (`orchestrator_run_id=auto-20260331-03`).
- Release finalization: PASS (findings, canonical notes, queue row `released`, legacy pointer, resume advanced).

## Run

- `start_command`: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- `runtime_mode`: `local`
- `runtime_context_ref`: `docs/engineering/runbook.md` (TEST_COMMAND)

## Connect

- `service_url`: `local-workspace://` (repository root on operator machine)
- `service_port`: `n/a`
- `health_endpoint`: `tests/report.md` (latest consolidated baseline) + targeted checks listed in `## Verify`

## Verify

- `verification_steps`:
  1. Run `python tests/installer_completeness_bug0003_test.py` (expect PASS).
  2. Run `python installer.py --validate-install-completeness --target .` (expect PASS).
  3. Confirm `sprints/S0063/release-findings.md` verdict is `PASS` and `handoffs/release_queue.md` row `S0063` is `released`.
  4. Confirm canonical bug closure alignment: `docs/product/backlog.md` (`BUG-0003` = `DONE`) and `docs/product/acceptance.md` (`BUG-0003` checked).
- `expected_health_signal`: Completeness validator PASS, BUG-0003 regression PASS, release findings PASS, queue row `released`, canonical bug status surfaces aligned.

## Credentials

- `credential_source_refs` (env names only): same as prior releases when publish targets are configured (`GITHUB_TOKEN`, target-specific `*Env` keys in `docs/engineering/release-targets.json`).
- Never place inline secrets in this file.

## Known issues

- Full `tests/run-tests.ps1` still reports 2 pre-existing Homebrew stable parity failures; this remains out of scope for `S0063` / `BUG-0003`.

## Deploy (staging / production)

- **Staging:** `DEPLOY_STAGING_COMMAND` from `docs/engineering/runbook.md` — `echo "No staging deploy target configured for this repository"`
- **Production:** `DEPLOY_PROD_COMMAND` from `docs/engineering/runbook.md` — `echo "No production deploy target configured for this repository"`

## Evidence refs (engineering)

- `sprints/S0063/summary.md`
- `sprints/S0063/qa-findings.md`
- `sprints/S0063/uat.json`
- `sprints/S0063/uat.md`
- `sprints/S0063/release-findings.md`
- `decisions/DEC-0066.md`
- `tests/report.md`
- `tests/installer_completeness_bug0003_test.py`
- `installer.py`
- `installer.ps1`
- `installer.sh`
