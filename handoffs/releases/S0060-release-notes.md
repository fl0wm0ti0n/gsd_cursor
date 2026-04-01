# Release notes — intake template parity / packaged installs (DEC-0063 / BUG-0001)

## What shipped

- **`template/scripts/`** mirrors **`intake_evidence_validate.py`**, **`intake_evidence_lib.py`**, **`intake_bug_routing_guard.py`**, and **`check_intake_template_parity.py`** (byte parity with repo **`scripts/`**).
- **`package.json` `files`** lists intake modules + parity script alongside **`template/`**.
- **Manifest** — **`docs/engineering/context/installer-owned-paths.manifest`** (+ **`template/`** copy) so install/upgrade copy paths are explicit.
- **CI** — **`scripts/check_intake_template_parity.py`**, **`tests/intake_template_parity_fixtures_test.py`**, **`tests/run-tests.ps1`** / **`tests/run-tests.sh`** §26N.
- **Governance** — **`decisions/DEC-0063.md`**, **`docs/engineering/architecture.md`** **`# BUG-0001`**.

## Gate summary

- Check-in test gate: PASS (`tests/report.md`; **770** pass / **2** fail Homebrew baseline — **out of scope**; §26N **PASS**).
- QA completion gate: PASS (`sprints/S0060/qa-findings.md`).
- UAT completion gate: PASS (`sprints/S0060/uat.json`, `sprints/S0060/uat.md`; **5/5**).
- Isolation gate: PASS (verify-work + release checkpoints on `docs/engineering/state.md`).
- Strict runtime proof gate: PASS (`orchestrator_run_id=auto-20260330-01`).
- Release finalization: PASS (release findings, canonical notes, queue row **`released`**, legacy pointer).

## Run

- `start_command`: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- `runtime_mode`: `local`
- `runtime_context_ref`: `docs/engineering/runbook.md` (TEST_COMMAND)

## Connect

- `service_url`: `local-workspace://` (repository root on operator machine)
- `service_port`: `n/a`
- `health_endpoint`: `tests/report.md` (latest consolidated test evidence)

## Verify

- `verification_steps`:
  1. From the repository root, run `python scripts/check_intake_template_parity.py --repo .` (expect `[INTAKE_TEMPLATE_PARITY_OK]`).
  2. Run `pytest tests/intake_template_parity_fixtures_test.py` (expect **1 passed**).
  3. Run `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` (expect `[BUG_VALIDATION_OK]`).
  4. Open `sprints/S0060/release-findings.md` and confirm verdict **PASS**; open `handoffs/release_queue.md` and confirm row **`S0060`** shows status **`released`**.
- `expected_health_signal`: Parity + bug validation **PASS**; release queue row **`released`**; release findings verdict **PASS**

## Credentials

- `credential_source_refs` (env names only): same as prior releases when publishing (`GITHUB_TOKEN`, keys per `docs/engineering/release-targets.json` if used).
- Never place inline secrets in this file.

## Known issues

- Full **`tests/run-tests.ps1`** may still report **2** failures on Homebrew stable vs **`package.json`** version — **out of scope** for **S0060**; tracked as baseline noise in **`tests/report.md`**.

## Deploy (staging / production)

- **Staging:** `DEPLOY_STAGING_COMMAND` from `docs/engineering/runbook.md` — `echo "No staging deploy target configured for this repository"`
- **Production:** `DEPLOY_PROD_COMMAND` from `docs/engineering/runbook.md` — `echo "No production deploy target configured for this repository"`

## Evidence refs (engineering)

- `sprints/S0060/summary.md`
- `sprints/S0060/qa-findings.md`
- `sprints/S0060/uat.json`
- `sprints/S0060/uat.md`
- `sprints/S0060/release-findings.md`
- `decisions/DEC-0063.md`
- `tests/report.md`
