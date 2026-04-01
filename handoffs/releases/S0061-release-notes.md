# Release notes — first-intake full-plan coverage gate (DEC-0064 / US-0081)

## What shipped

- Intake evidence gate now enforces complete first-intake plan coverage with machine-verifiable fields: `plan_area_inventory`, `plan_area_coverage`, and `coverage_complete=true`.
- Deterministic fail-closed diagnostics for coverage gaps are active under `INTAKE_PERSISTENCE_BLOCKED` (`INTAKE_PLAN_COVERAGE_MISSING`, `INTAKE_PLAN_AREA_ID_INVALID`, `INTAKE_PLAN_COVERAGE_CONTRACT_INVALID`, `INTAKE_PLAN_DEFERRED_REF_MISSING`).
- Guided and low-touch intake modes share the same complete-plan validator path.
- Active/template parity is validated for intake policy and validator surfaces.

## Gate summary

- Check-in test gate: PASS (`tests/report.md` baseline present; targeted release checks re-run and PASS).
- QA completion gate: PASS (`sprints/S0061/qa-findings.md`).
- UAT completion gate: PASS (`sprints/S0061/uat.json`, `sprints/S0061/uat.md`; **10/10**).
- Isolation gate: PASS (verify-work + release checkpoints on `docs/engineering/state.md`).
- Strict runtime proof gate: PASS (`orchestrator_run_id=auto-20260331-01`).
- Release finalization: PASS (release findings, canonical notes, queue row `released`, legacy pointer refreshed).

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
  1. Run `python tests/intake_evidence_fixtures_test.py` (expect `[INTAKE_EVIDENCE_FIXTURES_OK]`).
  2. Run `python scripts/check_intake_template_parity.py --repo .` (expect `[INTAKE_TEMPLATE_PARITY_OK]`).
  3. Confirm `sprints/S0061/release-findings.md` verdict is **PASS** and `handoffs/release_queue.md` row `S0061` status is `released`.
  4. Confirm backlog/acceptance alignment for `US-0081` (`docs/product/backlog.md` status `DONE`, `docs/product/acceptance.md` row checked).
- `expected_health_signal`: Targeted validators PASS; release findings PASS; queue row `released`; canonical status surfaces aligned.

## Credentials

- `credential_source_refs` (env names only): same as prior releases when publish targets are configured (`GITHUB_TOKEN`, target-specific `*Env` keys in `docs/engineering/release-targets.json`).
- Never place inline secrets in this file.

## Known issues

- Baseline `tests/report.md` still records Homebrew stable parity failures (`2`) from historical US-0016 scope; out-of-scope for `S0061`.

## Deploy (staging / production)

- **Staging:** `DEPLOY_STAGING_COMMAND` from `docs/engineering/runbook.md` — `echo "No staging deploy target configured for this repository"`
- **Production:** `DEPLOY_PROD_COMMAND` from `docs/engineering/runbook.md` — `echo "No production deploy target configured for this repository"`

## Evidence refs (engineering)

- `sprints/S0061/summary.md`
- `sprints/S0061/qa-findings.md`
- `sprints/S0061/uat.json`
- `sprints/S0061/uat.md`
- `sprints/S0061/release-findings.md`
- `decisions/DEC-0064.md`
- `tests/report.md`
