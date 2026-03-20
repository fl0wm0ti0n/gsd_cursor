# Release Notes - S0047 (`US-0068`)

## What shipped

- Finalized mandatory deterministic intake question-pack contracts for first-intake and small-intake flows.
- Finalized fail-closed intake persistence behavior when required topic coverage is incomplete.
- Finalized required intake evidence persistence fields: `asked_topics`, `missing_topics`, and `assumptions_confirmed`.
- Finalized deterministic unknown/ambiguous stack fallback to `first-intake-pack`.
- Finalized active/template parity updates for intake command, PO guidance, runbook, README, and test assertions.

## Gate summary

- Check-in test gate: PASS (US-0068 checks validated via `tests/report.md` evidence references in `sprints/S0047/qa-findings.md`).
- QA completion gate: PASS (`sprints/S0047/qa-findings.md`, no in-scope blockers).
- UAT completion gate: PASS (`sprints/S0047/uat.json`, `sprints/S0047/uat.md`; `10/10` pass).
- Isolation gate: PASS (required `execute`, `qa`, and `verify-work` isolation + strict runtime proofs present in `docs/engineering/state.md` for `S0047`).
- Release finalization: PASS (release findings/notes/queue/pointer updated for target sprint only).

## Run

- `start_command`: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- `runtime_mode`: `local`
- `runtime_context_ref`: `docs/engineering/runtime-connectivity.md`

## Connect

- `service_url`: `local-workspace://c:/flowGit/sonstiges/gsd_cursor`
- `service_port`: `n/a`
- `health_endpoint`: `tests/report.md (latest test evidence snapshot)`

## Verify

- `verification_steps`:
  1. Run `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` from repo root.
  2. Confirm US-0068 checks pass in `tests/report.md` (as referenced by `sprints/S0047/qa-findings.md`).
  3. Confirm release artifacts are PASS for `S0047`: `sprints/S0047/release-findings.md`, `handoffs/release_queue.md`, and `handoffs/release_notes.md`.
- `expected_health_signal`: `US-0068 checks PASS; S0047 queue status is released; release findings verdict is PASS`

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

- `None` for in-scope `US-0068` release contract.
- Non-US-0068 baseline test failures remain tracked in QA artifacts and are out-of-scope for this sprint release decision.

## US-0068 evidence refs

- `sprints/S0047/summary.md`
- `sprints/S0047/qa-findings.md`
- `sprints/S0047/uat.json`
- `sprints/S0047/uat.md`
- `sprints/S0047/release-findings.md`
- `handoffs/releases/S0047-release-notes.md`
- `handoffs/release_queue.md`
- `handoffs/release_notes.md`
