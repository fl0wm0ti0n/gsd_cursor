# Release Notes - S0046 (`US-0067`)

## What shipped

- Finalized deterministic release operator hints contract for `US-0067` with required canonical section order:
  `Run -> Connect -> Verify -> Credentials -> Known Issues`.
- Finalized mandatory operator fields for startup command, runtime mode/context, service URL/port, health endpoint, verification steps, expected health signal, and known-issues reporting.
- Finalized credentials guidance as env-reference-only with expected value-source location semantics (no inline secrets).
- Finalized deterministic fail-closed release behavior for missing/ambiguous/unsafe operator hint states.
- Finalized concise latest-pointer parity in `handoffs/release_notes.md` with canonical linkage.

## Gate summary

- Check-in test gate: PASS (US-0067 checks validated via `tests/report.md` evidence references in QA findings).
- QA completion gate: PASS (`sprints/S0046/qa-findings.md`, no in-scope blockers).
- UAT completion gate: PASS (`sprints/S0046/uat.json`, `sprints/S0046/uat.md`; `10/10` pass).
- Isolation gate: PASS (required prior phase isolation + strict runtime proof tuples present in `docs/engineering/state.md`).
- Release finalization: PASS (release findings, canonical notes, queue row, and legacy pointer finalized for `S0046`).

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
  2. Confirm US-0067 release-contract checks pass in `tests/report.md` (as referenced by `sprints/S0046/qa-findings.md`).
  3. Confirm release gate artifacts are in PASS state for `S0046`: `sprints/S0046/release-findings.md`, `handoffs/release_queue.md`, and `handoffs/release_notes.md`.
- `expected_health_signal`: `US-0067 checks PASS; S0046 queue status is released; release findings verdict is PASS`

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

- `None` for in-scope `US-0067` release contract.
- Non-US-0067 baseline test failures remain tracked in QA artifacts and are out-of-scope for this sprint release decision.

## US-0067 evidence refs

- `sprints/S0046/summary.md`
- `sprints/S0046/qa-findings.md`
- `sprints/S0046/uat.json`
- `sprints/S0046/uat.md`
- `sprints/S0046/release-findings.md`
- `handoffs/releases/S0046-release-notes.md`
- `handoffs/release_queue.md`
- `handoffs/release_notes.md`
