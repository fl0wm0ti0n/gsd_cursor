# Release notes — codebase map bootstrap (DEC-0065 / US-0082)

## What shipped

- Phase-gated **`scripts/materialize_codebase_map.py`** (+ **`template/scripts/`** mirror) for idempotent **`docs/engineering/codebase-map.md`** and **`dependencies.json`** bootstrap; preserves non-bootstrap maps; deterministic stdout tokens (**`[CODEBASE_MAP_OK]`**, **`CODEBASE_MAP_BLOCKED:*`**, **`[CODEBASE_MAP_MISSING]`**).
- **`/architecture`** step 10 materializer gate; **`/map-codebase`** / **`/refresh-context`** / **`/ask`** guidance (active + template); runbook **Codebase map bootstrap** section; installer manifest + **`package.json`** `files`.
- Regression: **`tests/codebase_map_materialize_test.py`**; **`tests/run-tests.ps1`** / **`tests/run-tests.sh`** §26N.

## Gate summary

- Check-in test gate: PASS (`tests/report.md` baseline; targeted verify-work checks PASS).
- QA completion gate: PASS (`sprints/S0062/qa-findings.md`).
- UAT completion gate: PASS (`sprints/S0062/uat.json`, `sprints/S0062/uat.md`; **10/10**).
- Isolation gate: PASS (delivery chain + release checkpoints on `docs/engineering/state.md`).
- Strict runtime proof gate: PASS (`orchestrator_run_id=auto-20260331-02`).
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
  1. Run `python tests/codebase_map_materialize_test.py` (expect OK).
  2. Run `python scripts/materialize_codebase_map.py --repo . --trigger architecture` (expect `[CODEBASE_MAP_OK]` or preserved-existing semantics).
  3. Confirm `sprints/S0062/release-findings.md` verdict is **PASS** and `handoffs/release_queue.md` row `S0062` status is `released`.
  4. Confirm backlog/acceptance alignment for `US-0082` (`docs/product/backlog.md` status `DONE`, `docs/product/acceptance.md` row checked).
- `expected_health_signal`: Materializer tier PASS; release findings PASS; queue row `released`; canonical status surfaces aligned.

## Credentials

- `credential_source_refs` (env names only): same as prior releases when publish targets are configured (`GITHUB_TOKEN`, target-specific `*Env` keys in `docs/engineering/release-targets.json`).
- Never place inline secrets in this file.

## Known issues

- Baseline `tests/report.md` still records Homebrew stable parity failures (`2`) from historical scope; **out of scope** for **S0062** / **US-0082**.

## Deploy (staging / production)

- **Staging:** `DEPLOY_STAGING_COMMAND` from `docs/engineering/runbook.md` — `echo "No staging deploy target configured for this repository"`
- **Production:** `DEPLOY_PROD_COMMAND` from `docs/engineering/runbook.md` — `echo "No production deploy target configured for this repository"`

## Evidence refs (engineering)

- `sprints/S0062/summary.md`
- `sprints/S0062/qa-findings.md`
- `sprints/S0062/uat.json`
- `sprints/S0062/uat.md`
- `sprints/S0062/release-findings.md`
- `decisions/DEC-0065.md`
- `tests/report.md`
- `scripts/materialize_codebase_map.py`
