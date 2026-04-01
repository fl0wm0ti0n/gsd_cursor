# Release notes - delegable intake clarification (DEC-0067 / US-0083)

## What shipped

- Intake evidence validator/library now supports explicit delegated required-topic coverage via `topic_coverage[].satisfied_by=delegation_ref`.
- Delegated rows require bounded metadata (`delegation_scope`, `delegation_rationale`, `delegation_confidence`) with deterministic fail-closed diagnostics.
- Non-delegated unresolved required-topic behavior remains unchanged fail-closed (`INTAKE_REQUIRED_TOPIC_MISSING` under `INTAKE_PERSISTENCE_BLOCKED`).
- Equivalent-evidence accounting markers (`evidence_source=equivalent_evidence_ref`, `equivalent_evidence_ref`) suppress repetitive asks without bypassing required-topic coverage rows.
- Active/template command/guidance/test parity for delegation behavior is validated by QA/verify-work evidence.

## Gate summary

- Check-in test gate: PASS (`tests/report.md`; `Pass: 779`, `Fail: 2` legacy Homebrew baseline out of scope).
- QA completion gate: PASS (`sprints/S0064/qa-findings.md`).
- UAT completion gate: PASS (`sprints/S0064/uat.json`, `sprints/S0064/uat.md`; `10/10`).
- Isolation gate: PASS (fresh verify-work provenance and release-phase fresh context marker recorded in release artifacts).
- Release finalization: PASS (release findings, canonical notes, queue row `released`, legacy pointer refreshed).

## Run

- `start_command`: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- `runtime_mode`: `local`
- `runtime_context_ref`: `docs/engineering/runbook.md` (TEST_COMMAND)

## Connect

- `service_url`: `local-workspace://` (repository root on operator machine)
- `service_port`: `n/a`
- `health_endpoint`: `tests/report.md` (latest consolidated baseline) plus targeted checks listed in `## Verify`

## Verify

- `verification_steps`:
  1. Run `python tests/intake_evidence_fixtures_test.py` (expect PASS).
  2. Run `python scripts/intake_evidence_validate.py --self-test` (expect PASS).
  3. Run `python scripts/check_intake_template_parity.py --repo .` (expect PASS).
  4. Confirm `sprints/S0064/release-findings.md` verdict is `PASS` and `handoffs/release_queue.md` row `S0064` status is `released`.
  5. Confirm canonical status alignment for `US-0083` (`docs/product/backlog.md` status `DONE`, `docs/product/acceptance.md` row checked).
- `expected_health_signal`: delegation validator tier PASS, release findings PASS, queue row `released`, and canonical status surfaces aligned.

## Credentials

- `credential_source_refs` (env names only): same as prior releases when publish targets are configured (`GITHUB_TOKEN`, target-specific `*Env` keys in `docs/engineering/release-targets.json`).
- Never place inline secrets in this file.

## Known Issues

- `tests/report.md` still includes 2 pre-existing Homebrew stable parity failures; out of scope for `S0064` / `US-0083`.

## Deploy (staging / production)

- **Staging:** `DEPLOY_STAGING_COMMAND` from `docs/engineering/runbook.md` - `echo "No staging deploy target configured for this repository"`
- **Production:** `DEPLOY_PROD_COMMAND` from `docs/engineering/runbook.md` - `echo "No production deploy target configured for this repository"`

## Evidence refs (engineering)

- `sprints/S0064/summary.md`
- `sprints/S0064/qa-findings.md`
- `sprints/S0064/uat.json`
- `sprints/S0064/uat.md`
- `sprints/S0064/release-findings.md`
- `decisions/DEC-0067.md`
- `tests/report.md`
- `scripts/intake_evidence_lib.py`
- `scripts/intake_evidence_validate.py`
- `tests/intake_evidence_fixtures_test.py`
