# Release Notes - S0049 (`US-0070`)

## What shipped

- Scratchpad-controlled `/auto` **phase plan resolution**: exactly one active mode among `AUTO_PHASE_PLAN`, `AUTO_PHASE_EXCLUDE`, `AUTO_PHASE_INCLUDE`, `AUTO_PHASE_PROFILE` with `PHASE_POLICY_CONFLICT` on merge conflict (**DEC-0052**).
- **Materialized ordered phase list** before first spawn; continuation breadcrumbs record selected phases, skipped phases + reasons, and policy metadata.
- **Fail-closed validation** for unknown phase tokens, empty include, unknown profile, and related diagnostics.
- **Non-skippable reinstatement** defaults for safety/evidence-chain phases (`qa`, `verify-work`, `release`, prerequisites per **DEC-0052**); high-risk profiles only with documented acknowledgment + registry.
- **`start-from=<phase>` intersection** with resolved plan; empty intersection fails with plan vs anchor listing.
- **Resume / multi-mode parity**: `AUTO_BACKLOG_DRAIN`, `AUTO_EXECUTE_BULK`, `TEAM_MODE` paths reload merged scratchpad and recompute plan; no silent revival of omitted phases (**US-0069** / **DEC-0051** alignment — no role substitution when phases are omitted).
- Active + template parity for `/auto`, scratchpad examples, runbook, README; regression section **26d** in `tests/run-tests.ps1` and `tests/run-tests.sh`.
- Operator-facing **boundary status**: selected/skipped phases and reason codes.

## Gate summary

- Check-in test gate: PASS (in-scope **26d** per `sprints/S0049/qa-findings.md` and `tests/report.md`).
- QA completion gate: PASS (`sprints/S0049/qa-findings.md`; no in-scope blockers).
- UAT completion gate: PASS (`sprints/S0049/uat.json`, `sprints/S0049/uat.md`; `10/10` pass).
- Isolation gate: PASS (`execute`, `qa`, `verify-work` isolation evidence in `docs/engineering/state.md`).
- Strict runtime proof gate: PASS (matching tuples, `orchestrator_run_id=auto-20260321-01`).
- Release finalization: PASS (release findings, notes, queue row, legacy pointer, backlog reconciliation for target story only).

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
  2. Confirm US-0070 / section **26d** strings pass in `tests/report.md` (per `sprints/S0049/qa-findings.md`).
  3. Confirm release artifacts for `S0049`: `sprints/S0049/release-findings.md`, `handoffs/release_queue.md` (`released`), `handoffs/release_notes.md` (latest pointer).
- `expected_health_signal`: `US-0070 checks PASS; S0049 queue status is released; release findings verdict is PASS`

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

- `None` for in-scope `US-0070` release contract.
- Non-US-0070 baseline test failures (Homebrew/npm packaging, installer TEST_COMMAND bootstrap asserts) remain documented as out-of-scope in `sprints/S0049/qa-findings.md`.

## US-0070 evidence refs

- `sprints/S0049/summary.md`
- `sprints/S0049/qa-findings.md`
- `sprints/S0049/uat.json`
- `sprints/S0049/uat.md`
- `sprints/S0049/release-findings.md`
- `handoffs/releases/S0049-release-notes.md`
- `handoffs/release_queue.md`
- `handoffs/release_notes.md`
