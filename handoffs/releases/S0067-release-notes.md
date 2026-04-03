# Release notes — spawn-only `/auto` orchestration (BUG-0006 / R-0065)

## What shipped

- **Spawn-only `/auto` contract** with distinct fail-fast reason code **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** when the orchestrator performs phase work instead of spawning required role subagents — **`.cursor/commands/auto.md`**, **`template/.cursor/commands/auto.md`**, **`docs/engineering/auto-orchestration-reference.md`** (**DEC-0029** / **DEC-0038** cross-links).
- **`tests/auto_command_contract_test.py`** — **R-0065** regression (required literals, negative phrasing, active/template parity, reference assertions); invoked from **`tests/run-tests.ps1`** / **`tests/run-tests.sh`** (existing harness section).
- **Architecture lock-in**: **`docs/engineering/architecture.md`** **`# BUG-0006`**.

## Gate summary

- Check-in test gate: **PASS** (`python tests/auto_command_contract_test.py` — 4 tests).
- QA completion gate: **PASS** (`sprints/S0067/qa-findings.md`).
- UAT completion gate: **PASS** (`sprints/S0067/uat.json`, `sprints/S0067/uat.md`; **5/5**).
- Isolation gate: **PASS** (verify-work + release checkpoints in `docs/engineering/state.md`).
- Strict runtime proof gate: **PASS** (`orchestrator_run_id=auto-20260403-03`).
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
  1. Run `python tests/auto_command_contract_test.py` (expect **PASS**, 4 tests).
  2. Confirm **`.cursor/commands/auto.md`** and **`template/.cursor/commands/auto.md`** state spawn-only execution and document **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** with remediation.
  3. Spot-check **`docs/engineering/auto-orchestration-reference.md`** for spawn-only language and **`decisions/DEC-0029.md`** / **`decisions/DEC-0038.md`** links.
  4. Confirm `sprints/S0067/release-findings.md` verdict is **PASS** and `handoffs/release_queue.md` row **S0067** is **`released`**.
  5. Confirm canonical bug closure: `docs/product/backlog.md` (**BUG-0006** = **DONE**) and `docs/product/acceptance.md` (**BUG-0006** checked).
- `expected_health_signal`: Contract test green, release findings **PASS**, queue row **`released`**, backlog/acceptance aligned (**US-0045**).

## Credentials

- `credential_source_refs` (env names only): same as prior releases when publish targets are configured (`GITHUB_TOKEN`, target-specific `*Env` keys in `docs/engineering/release-targets.json`).
- Never place inline secrets in this file.

## Known issues

- **None** for in-scope **BUG-0006** / **R-0065** delivery.

## Deploy (staging / production)

- **Staging:** `DEPLOY_STAGING_COMMAND` from `docs/engineering/runbook.md` — `echo "No staging deploy target configured for this repository"`
- **Production:** `DEPLOY_PROD_COMMAND` from `docs/engineering/runbook.md` — `echo "No production deploy target configured for this repository"`

## Evidence refs (engineering)

- `sprints/S0067/summary.md`
- `sprints/S0067/qa-findings.md`
- `sprints/S0067/uat.json`
- `sprints/S0067/uat.md`
- `sprints/S0067/release-findings.md`
- `docs/engineering/architecture.md` (`# BUG-0006`)
- `docs/engineering/research.md` (**R-0065**)
- `tests/auto_command_contract_test.py`
- `.cursor/commands/auto.md`
- `template/.cursor/commands/auto.md`
- `docs/engineering/auto-orchestration-reference.md`
