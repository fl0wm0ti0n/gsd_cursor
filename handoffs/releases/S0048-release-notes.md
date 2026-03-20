# Release Notes - S0048 (`US-0069`)

## What shipped

- Strict deterministic phase→role mapping for `/auto` with scratchpad alternates (`AUTO_ROLE_RESEARCH`, `AUTO_ROLE_PLAN_VERIFY`, `AUTO_ROLE_REFRESH_CONTEXT`) per **DEC-0051**.
- Prefail-closed preflight when required role capability is missing (`PHASE_ROLE_CAPABILITY_MISSING`); no unrelated-role spawn.
- Post-completion boundary checks for isolation `role` vs expected contract (`PHASE_ROLE_MISMATCH`).
- Execute default `dev` with audited override path (`AUTO_EXECUTE_ROLE_OVERRIDE` + `EXECUTE_OVERRIDE_GOVERNANCE_REF`).
- Resume / `start-from` parity: preflight recomputation on every continuation.
- Active + template parity for `/auto`, `/release` gates **4a**/**4b**, runbook, README, scratchpad examples; regression section **26c** in both test runners.

## Gate summary

- Check-in test gate: PASS (US-0069 in-scope checks per `sprints/S0048/qa-findings.md` and `tests/report.md`).
- QA completion gate: PASS (`sprints/S0048/qa-findings.md`; no in-scope blockers).
- UAT completion gate: PASS (`sprints/S0048/uat.json`, `sprints/S0048/uat.md`; `10/10` pass).
- Isolation gate: PASS (`execute`, `qa`, `verify-work` isolation evidence in `docs/engineering/state.md`).
- Strict runtime proof gate: PASS (matching tuples, `orchestrator_run_id=auto-20260320-01`).
- Release finalization: PASS (release findings, notes, queue row, legacy pointer updated for target sprint only).

## Run

- `start_command`: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- `runtime_mode`: `local`
- `runtime_context_ref`: `docs/engineering/runtime-connectivity.md`

## Connect

- `service_url`: `local-workspace://c:/flowGit/sonstiges/gsd_cursor`
- `service_port`: `n/a`
- `health_endpoint`: `tests/report.md` (latest test evidence snapshot)

## Verify

- `verification_steps`:
  1. Run `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` from repo root.
  2. Confirm US-0069 / section **26c** strings pass in `tests/report.md` (per `sprints/S0048/qa-findings.md`).
  3. Confirm release artifacts for `S0048`: `sprints/S0048/release-findings.md`, `handoffs/release_queue.md` (`released`), `handoffs/release_notes.md` (latest pointer).
- `expected_health_signal`: `US-0069 checks PASS; S0048 queue status is released; release findings verdict is PASS`

## Credentials

- `credential_source_refs` (env names only):
  - `GITHUB_TOKEN` (only if using git push in downstream publish flows)
  - `CHOCO_API_KEY` (only if using choco publish flow)
  - `DOCKER_TOKEN` (only if using docker publish flow)
  - `AWS_PROFILE` (only if using aws publish flow)
- `expected_value_source`:
  - Operator shell/session environment or CI secret store, depending on publish target.
- Never place inline secrets/tokens/passwords in this file.

## Known Issues

- `None` for in-scope `US-0069` release contract.
- Non-US-0069 baseline test failures (Homebrew/npm packaging asserts) remain documented as out-of-scope in `sprints/S0048/qa-findings.md`.

## US-0069 evidence refs

- `sprints/S0048/summary.md`
- `sprints/S0048/qa-findings.md`
- `sprints/S0048/uat.json`
- `sprints/S0048/uat.md`
- `sprints/S0048/release-findings.md`
- `handoffs/releases/S0048-release-notes.md`
- `handoffs/release_queue.md`
- `handoffs/release_notes.md`
