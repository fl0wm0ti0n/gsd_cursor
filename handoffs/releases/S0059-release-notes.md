# Release notes — token-cost hardening (DEC-0062 / US-0080)

## What shipped

- **Slim `/auto` orchestrator** — `.cursor/commands/auto.md` (~187 lines) with full prose in **`docs/engineering/auto-orchestration-reference.md`**.
- **Metrics + comparability** — **`scripts/token_cost_lib.py`**, **`scripts/token_cost_compare.py`**, **`tests/fixtures/token_cost/`**, **`tests/token_cost_fixtures_test.py`** (`run_class_hash`, **AC-2** contract).
- **Evidence channel** — **`handoffs/token_cost_runs/README.md`**, sample **`handoffs/token_cost_runs/auto-20260329-02.md`**; **`token_cost_evidence_ref`** on **`docs/engineering/state.md`** execute checkpoint.
- **Parity + CI** — **`docs/engineering/token-cost-parity-manifest.md`** v1, **`scripts/check_token_cost_parity.py`**, **`tests/run-tests.ps1`** / **`tests/run-tests.sh`** §26M; **`template/`** mirrors for manifest-listed paths.
- **Operator guidance** — **`README.md`**, **`docs/engineering/runbook.md`** (fresh context, **`start-from`**, **`TOKEN_PROFILE`**, evidence paths); **`handoffs/tl_to_dev.md`** bounded-read note for **S0059**.
- **Governance** — **`decisions/DEC-0062.md`**, **`docs/engineering/architecture.md`** **`# US-0080`**, **`docs/engineering/research.md`** **`R-0057`**.

## Gate summary

- Check-in test gate: PASS (`tests/report.md`; **768** pass / **0** fail; §26M token-cost / parity rows **PASS**).
- QA completion gate: PASS (`sprints/S0059/qa-findings.md`; no in-scope blockers).
- UAT completion gate: PASS (`sprints/S0059/uat.json`, `sprints/S0059/uat.md`; **10/10**).
- Isolation gate: PASS (phase isolation evidence through verify-work + release checkpoint on `docs/engineering/state.md`).
- Strict runtime proof gate: PASS (`orchestrator_run_id=auto-20260329-02`).
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
  1. From the repository root, run the consolidated test runner above; confirm §26M / token-cost parity checks **PASS**.
  2. Run `python scripts/check_token_cost_parity.py --repo .` (expect `[TOKEN_COST_PARITY_OK]`).
  3. Run `python tests/token_cost_fixtures_test.py` and `python tests/auto_command_contract_test.py` (expect exit `0`).
  4. Open `sprints/S0059/release-findings.md` and confirm verdict **PASS**; open `handoffs/release_queue.md` and confirm row **`S0059`** shows status **`released`**.
- `expected_health_signal`: Parity + fixtures + contract tests **PASS**; release queue row **`released`**; release findings verdict **PASS**

## Credentials

- `credential_source_refs` (env names only): same as prior releases (`GITHUB_TOKEN`, publish keys as applicable per `docs/engineering/release-targets.json`).
- Never place inline secrets in this file.

## Known issues

- **AC-2** live **50%** `cache_read_tokens` delta remains operator/vendor-metric evidence when host maps metrics; CI enforces **run_class_hash** comparability, parity manifest, and regression fixtures (**DEC-0062**).

## Deploy (staging / production)

- **Staging:** `DEPLOY_STAGING_COMMAND` from `docs/engineering/runbook.md` — `echo "No staging deploy target configured for this repository"`
- **Production:** `DEPLOY_PROD_COMMAND` from `docs/engineering/runbook.md` — `echo "No production deploy target configured for this repository"`

## Evidence refs (engineering)

- `sprints/S0059/summary.md`
- `sprints/S0059/qa-findings.md`
- `sprints/S0059/uat.json`
- `sprints/S0059/uat.md`
- `sprints/S0059/release-findings.md`
- `decisions/DEC-0062.md`
- `handoffs/token_cost_runs/auto-20260329-02.md`
- `tests/report.md`
