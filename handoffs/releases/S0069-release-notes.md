# Release notes — US-0084 (POSIX npm installer + Linux remote test targets)

## What shipped

- **POSIX / LF installer hardening**: root **`.gitattributes`** (`*.sh text eol=lf`); **`installer.sh`** dash-safe startup lineage (**BUG-0004**); extended **`tests/installer_shell_bug0004_test.py`** (CR scan, forbidden `set` tokens, optional **`dash -n`** when on PATH).
- **Publish guards**: **`scripts/guard_installer_publish.py`**; **`package.json`** **`prepublishOnly`** / **`guard:installer`**; layered checks per **`docs/engineering/architecture.md`** **`# US-0084`**.
- **US-0064 alignment** (no competing schema): **`docs/engineering/runtime-connectivity.md`** dev/QA table vs **`docs/engineering/release-targets.json`**; **`docs/engineering/us-0084-remote-e2e.md`** (+ **`template/`** mirror) for Windows → WSL / SSH / Docker-over-SSH operator paths.
- **Remote config helper**: **`scripts/remote_config_summary.py`** (`--config`, **`REMOTE_CONFIG`**, deterministic exits **0–4**); **`tests/remote_config_summary_test.py`** + fixtures under **`tests/fixtures/`**; harness **H1–H5** in **`tests/run-tests.sh`** / **`tests/run-tests.ps1`**.
- **Governance**: **`decisions/DEC-0070.md`** — when **`REMOTE_EXECUTION`** is unset or falsy, helper skips **`REMOTE_CONFIG`** read, stderr one-liner, **exit 0** (not exit 5); indexed in **`docs/engineering/decisions.md`**. Scratchpad / command cues for **`REMOTE_EXECUTION`** evidence (**names-only**).
- **Ship path**: installer-owned manifest + **`template/scripts/`** parity (**BUG-0001** pattern); **`package.json` `files`** updated.

## Gate summary (pre-release / verify-work / release)

- Check-in test gate: **PASS** — `python tests/installer_shell_bug0004_test.py`, `python tests/remote_config_summary_test.py`, `python scripts/guard_installer_publish.py`, `python scripts/check_intake_template_parity.py --repo .` (re-run at verify-work; see **`sprints/S0069/uat.json`** **`verification_commands_rerun`**).
- QA gate: **PASS** (`sprints/S0069/qa-findings.md`).
- UAT gate: **PASS** (`sprints/S0069/uat.json`, **`sprints/S0069/uat.md`** — **10/10**).
- Isolation gate: **PASS** (verify-work + release checkpoints on **`docs/engineering/state.md`**).
- Strict runtime proof gate: **PASS** (`orchestrator_run_id=auto-20260404-02`, release tuple `runtime_proof_id=rp-auto-20260404-02-release-release-20260405T001000Z-S0069-US0084`, `proof_hash=418cbee2c8f7508880e1cbcae744d67877c08e68c91432b3de38f0e1773b07fc`).
- Release finalization: **COMPLETE** (`2026-04-05T00:10:00Z` — **`handoffs/release_queue.md`** row **`S0069`** → **`released`**).

## Publish posture (scratchpad)

- **`RELEASE_PUBLISH_MODE=confirm`** — no npm/git publish without explicit operator confirmation; release docs and queue state only unless a separate publish run is approved.
- **`ALLOW_AUTO_PUSH=0`** (**DEC-0018**) — **`push_decision=not_eligible`** at this boundary unless overridden.

## Run

- `start_command`: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` (includes **H1–H5** per runbook / harness).
- `runtime_mode`: `local` (remote Linux targets per **`docs/engineering/us-0084-remote-e2e.md`**).
- `runtime_context_ref`: `docs/engineering/runbook.md` (**`REMOTE_EXECUTION`**, installer troubleshooting)

## Connect

- `service_url`: `local-workspace://` + optional remote profiles per **`release-targets.json`** / **`runtime-connectivity.md`**
- `service_port`: `n/a` (tooling repo)
- `health_endpoint`: targeted checks in **`## Verify`** + **`tests/report.md`** when present

## Verify

1. `python tests/installer_shell_bug0004_test.py` — **PASS** (note: some cases skip when **`dash`** absent on Windows; documented).
2. `python tests/remote_config_summary_test.py` — **PASS**.
3. `python scripts/guard_installer_publish.py` — **PASS** (may skip **`dash`** path when not on PATH; Python CRLF/token path still enforced).
4. `python scripts/check_intake_template_parity.py --repo .` — **`[INTAKE_TEMPLATE_PARITY_OK]`**.
5. `python scripts/enforce-triad-hot-surface.py --check` — **PASS** (post-release **`state.md`** hygiene per **DEC-0054**).
6. Post-release: **`sprints/S0069/release-findings.md`** **PASS**, **`handoffs/release_queue.md`** **`S0069`** **`released`**, **`docs/product/backlog.md`** **US-0084** **DONE** — then **`/refresh-context`** (**curator**).

`expected_health_signal`: UAT **10/10**, backlog/acceptance aligned (**US-0045**), **DEC-0070** skip path stable for **`REMOTE_EXECUTION=0`**.

## Credentials

- `credential_source_refs` (env names only): **`REMOTE_CONFIG`**, SSH agent / path refs per remote policy — no inline secrets. See **`docs/engineering/release-targets.json`** for target env key names when publishing.

## Known issues

- **`dash`** may be absent on Windows CI — **H2** / optional syntax check skipped; documented (**R-0067** / QA findings).

## Deploy (staging / production)

- **Staging:** `DEPLOY_STAGING_COMMAND` from `docs/engineering/runbook.md` — `echo "No staging deploy target configured for this repository"`
- **Production:** `DEPLOY_PROD_COMMAND` from `docs/engineering/runbook.md` — `echo "No production deploy target configured for this repository"`
- **npm package:** follow org publish checklist; **`npm publish`** runs **`prepublishOnly`** → **`guard:installer`** — confirm **`RELEASE_PUBLISH_MODE`** and registry target before any publish.

## Evidence refs (engineering)

- `sprints/S0069/summary.md`
- `sprints/S0069/qa-findings.md`
- `sprints/S0069/uat.json`
- `sprints/S0069/uat.md`
- `sprints/S0069/release-findings.md`
- `decisions/DEC-0070.md`
- `docs/engineering/architecture.md` (`# US-0084`, `# US-0064` cross-ref)
- `docs/engineering/runtime-connectivity.md`
- `docs/engineering/us-0084-remote-e2e.md`
- `scripts/remote_config_summary.py`
- `scripts/guard_installer_publish.py`
- `tests/installer_shell_bug0004_test.py`
- `tests/remote_config_summary_test.py`
