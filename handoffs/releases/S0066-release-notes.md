# Release notes — bug-intake `resume_brief` refresh (DEC-0069 / BUG-0005)

## What shipped

- **`decisions/DEC-0069`**: Intake-time atomic refresh of **`handoffs/resume_brief.md`** after successful **`/intake bug`** persistence — **`bug_id`**, default **`discovery`** resume seed, **`resolution_source=resume_brief`**, boundary metadata, **`US-0045`** alignment (fail-closed on DONE / backlog contradiction).
- **`scripts/intake_bug_resume_brief_refresh.py`** with **`template/scripts/`** mirror; invoked from intake path; **`--self-test`** and **`--validate-file`** audit modes.
- **`.cursor/commands/intake.md`** and **`template/.cursor/commands/intake.md`** — DEC-0069 refresh step, outputs, ownership carve-out for **`resume_brief`** on bug intake.
- **`scripts/check_intake_template_parity.py`** (and template pair) extended for the new script pair.
- **`tests/intake_bug_resume_brief_bug0005_test.py`** — **R-0064** matrix; wired in **`tests/run-tests.sh`** / **`tests/run-tests.ps1`** section **26Q**.

## Gate summary

- Check-in test gate: **PASS** (`python tests/intake_bug_resume_brief_bug0005_test.py`; `python scripts/check_intake_template_parity.py --repo .`; `python scripts/intake_bug_resume_brief_refresh.py --self-test`).
- QA completion gate: **PASS** (`sprints/S0066/qa-findings.md`).
- UAT completion gate: **PASS** (`sprints/S0066/uat.json`, `sprints/S0066/uat.md`; **9/9**).
- Isolation gate: **PASS** (release checkpoint in `docs/engineering/state.md`).
- Strict runtime proof gate: **PASS** (`orchestrator_run_id=auto-20260403-02`).
- Release finalization: **PASS** (findings, canonical notes, queue row **`released`**, legacy pointer refreshed).

## Run

- `start_command`: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- `runtime_mode`: `local`
- `runtime_context_ref`: `docs/engineering/runbook.md` (TEST_COMMAND)

## Connect

- `service_url`: `local-workspace://` (repository root on operator machine)
- `service_port`: `n/a`
- `health_endpoint`: `tests/report.md` (consolidated baseline) + targeted checks in **`## Verify`**

## Verify

- `verification_steps`:
  1. Run `python tests/intake_bug_resume_brief_bug0005_test.py` (expect **PASS**).
  2. Run `python scripts/check_intake_template_parity.py --repo .` (expect **`[INTAKE_TEMPLATE_PARITY_OK]`**).
  3. Run `python scripts/intake_bug_resume_brief_refresh.py --self-test` (expect **`[INTAKE_BUG_RESUME_BRIEF_REFRESH_OK]`**).
  4. Confirm `sprints/S0066/release-findings.md` verdict is **PASS** and `handoffs/release_queue.md` row **S0066** is **`released`**.
  5. Confirm canonical bug closure: `docs/product/backlog.md` (**BUG-0005** = **DONE**) and `docs/product/acceptance.md` (**BUG-0005** checked).
- `expected_health_signal`: Targeted tests green, release findings **PASS**, queue row **`released`**, backlog/acceptance aligned (**US-0045**).

## Credentials

- `credential_source_refs` (env names only): same as prior releases when publish targets are configured (`GITHUB_TOKEN`, target-specific `*Env` keys in `docs/engineering/release-targets.json`).
- Never place inline secrets in this file.

## Known issues

- **None** for in-scope **BUG-0005** / **DEC-0069** delivery.

## Deploy (staging / production)

- **Staging:** `DEPLOY_STAGING_COMMAND` from `docs/engineering/runbook.md` — `echo "No staging deploy target configured for this repository"`
- **Production:** `DEPLOY_PROD_COMMAND` from `docs/engineering/runbook.md` — `echo "No production deploy target configured for this repository"`

## Evidence refs (engineering)

- `sprints/S0066/summary.md`
- `sprints/S0066/qa-findings.md`
- `sprints/S0066/uat.json`
- `sprints/S0066/uat.md`
- `sprints/S0066/release-findings.md`
- `decisions/DEC-0069.md`
- `scripts/intake_bug_resume_brief_refresh.py`
- `tests/intake_bug_resume_brief_bug0005_test.py`
