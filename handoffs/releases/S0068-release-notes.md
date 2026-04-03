# Release notes — intake evidence truthfulness guard (BUG-0007 / R-0066)

## What shipped

- **`scripts/intake_evidence_lib.py`** (+ **`template/scripts/`** parity) — duplicate / non-distinct **`answer_ref`** **`quoted_user_text`** guard across required **`small-intake-pack`** topics; fail-fast **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** with **US-0083** exemptions (**`equivalent_evidence_ref`**, **`delegation_ref`**, **`assumption_confirmation_ref`**).
- **Active + template** **`.cursor/commands/intake.md`** — truthful **`asked_topics`** / **`topic_coverage`**; forbid synthetic echo; governance cross-links.
- **`tests/intake_evidence_bug0007_r0066_test.py`** — **R-0066** matrix rows **1–5** (FAIL exemplar + PASS paths); **`tests/run-tests.sh`** / **`tests/run-tests.ps1`** §**26R**.
- **`python scripts/intake_evidence_validate.py --self-test`** and **`check_intake_template_parity.py`** harness alignment.
- **Architecture / research**: **`docs/engineering/architecture.md`** **`# BUG-0007`**, **`docs/engineering/research.md`** **`R-0066`**.

## Gate summary (pre-release / verify-work)

- Check-in test gate: **PASS** (`python tests/intake_evidence_bug0007_r0066_test.py`; **`python scripts/intake_evidence_validate.py --self-test`**; **`python scripts/check_intake_template_parity.py --repo .`**).
- QA completion gate: **PASS** (`sprints/S0068/qa-findings.md`).
- UAT completion gate: **PASS** (`sprints/S0068/uat.json`, `sprints/S0068/uat.md`; **6/6**).
- Isolation gate: **PASS** (verify-work checkpoint in `docs/engineering/state.md`).
- Strict runtime proof gate: **PASS** (`orchestrator_run_id=auto-20260404-01`, release tuple `runtime_proof_id=rp-auto-20260404-01-release-release-20260405T001000Z-S0068-BUG0007`, `proof_hash=6c824be4c8dfb3ecb25de8e8ca90910789436a2c916489fb15a935baf3c64202`).
- Release finalization: **COMPLETE** (`2026-04-05T00:10:00Z` — queue **`S0068`** → **`released`**).

## Run

- `start_command`: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` (includes §26R / parity checks per runbook).
- `runtime_mode`: `local`
- `runtime_context_ref`: `docs/engineering/runbook.md` (TEST_COMMAND)

## Connect

- `service_url`: `local-workspace://` (repository root on operator machine)
- `service_port`: `n/a`
- `health_endpoint`: `tests/report.md` (consolidated baseline) + targeted checks in **`## Verify`**

## Verify

- `verification_steps`:
  1. Run `python tests/intake_evidence_bug0007_r0066_test.py` (expect **PASS**).
  2. Run `python scripts/intake_evidence_validate.py --self-test` (expect **`[INTAKE_EVIDENCE_SELF_TEST_OK]`**).
  3. Run `python scripts/check_intake_template_parity.py --repo .` (expect **`[INTAKE_TEMPLATE_PARITY_OK]`**).
  4. Confirm exemplar `handoffs/intake_evidence/BUG-0007-intake-20260403.json` fails validation with **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`**.
  5. Post-release: confirm `sprints/S0068/release-findings.md` **PASS**, `handoffs/release_queue.md` row **S0068** **`released`**, **`docs/product/backlog.md`** **BUG-0007** **DONE**, then run **`/refresh-context`** (curator) per lifecycle.
- `expected_health_signal`: R-0066 tests green, UAT **6/6**, backlog/acceptance aligned (**US-0045**).

## Credentials

- `credential_source_refs` (env names only): same as prior releases when publish targets are configured (`GITHUB_TOKEN`, target-specific `*Env` keys in `docs/engineering/release-targets.json`).
- Never place inline secrets in this file.

## Known issues

- **None** for in-scope **BUG-0007** / **R-0066** delivery.

## Deploy (staging / production)

- **Staging:** `DEPLOY_STAGING_COMMAND` from `docs/engineering/runbook.md` — `echo "No staging deploy target configured for this repository"`
- **Production:** `DEPLOY_PROD_COMMAND` from `docs/engineering/runbook.md` — `echo "No production deploy target configured for this repository"`

## Evidence refs (engineering)

- `sprints/S0068/summary.md`
- `sprints/S0068/qa-findings.md`
- `sprints/S0068/uat.json`
- `sprints/S0068/uat.md`
- `sprints/S0068/release-findings.md`
- `docs/engineering/architecture.md` (`# BUG-0007`)
- `docs/engineering/research.md` (**R-0066**)
- `scripts/intake_evidence_lib.py`
- `tests/intake_evidence_bug0007_r0066_test.py`
- `.cursor/commands/intake.md`
- `template/.cursor/commands/intake.md`
