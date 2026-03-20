# Release Notes - S0050 (`US-0071`)

## What shipped

- **User-visible internal metadata guard** — `scripts/check-user-visible-metadata.py` denies planning-shaped tokens (`US-`, `DEC-`, `R-` + four digits) under deterministic roots (`bin/**`, installers, `packaging/**`, `scripts/validate-and-push.{ps1,sh}`).
- **Policy + reason codes** — runbook (+ template) documents forbidden tokens, inclusive roots, checker invocation, remediation contract, and codes `USER_VISIBLE_INTERNAL_METADATA_DETECTED`, `METADATA_SANITIZATION_POLICY_MISSING`, `METADATA_SANITIZATION_SCOPE_AMBIGUOUS` (**DEC-0053** alignment).
- **Workflow wiring** — `/execute` guard step, `/qa` checker mandate, `/release` check-in gate note for consolidated runner + US-0071 **26e** coverage; `quality.mdc` and README active+template parity.
- **Regression (26e)** — `tests/run-tests.ps1` / `tests/run-tests.sh`: clean scan, idempotent rerun, injected `bin/` leak fails closed, non-scanned `docs/` ignored, JS line-comment allowance.

## Gate summary

- Check-in test gate: PASS (in-scope **26e** per `sprints/S0050/qa-findings.md` and `tests/report.md`; suite-level fails documented out-of-scope).
- QA completion gate: PASS (`sprints/S0050/qa-findings.md`; no in-scope blockers).
- UAT completion gate: PASS (`sprints/S0050/uat.json`, `sprints/S0050/uat.md`; `10/10` pass).
- Isolation gate: PASS (`execute`, `qa`, `verify-work` isolation evidence in `docs/engineering/state.md`).
- Strict runtime proof gate: PASS (matching tuples, `orchestrator_run_id=auto-20260321-02`).
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
  1. Run `python scripts/check-user-visible-metadata.py` from repo root (expect exit `0`).
  2. Run `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` from repo root.
  3. Confirm US-0071 / section **26e** strings pass in `tests/report.md` (per `sprints/S0050/qa-findings.md`).
  4. Confirm release artifacts for `S0050`: `sprints/S0050/release-findings.md`, `handoffs/release_queue.md` (`released`), `handoffs/release_notes.md` (latest pointer).
- `expected_health_signal`: `US-0071 **26e** checks PASS; S0050 queue status is released; release findings verdict is PASS`

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

- `None` for in-scope `US-0071` release contract.
- Non-US-0071 baseline test failures (Homebrew/npm packaging, installer TEST_COMMAND bootstrap asserts) remain documented as out-of-scope in `sprints/S0050/qa-findings.md`.

## US-0071 evidence refs

- `sprints/S0050/summary.md`
- `sprints/S0050/qa-findings.md`
- `sprints/S0050/uat.json`
- `sprints/S0050/uat.md`
- `sprints/S0050/release-findings.md`
- `handoffs/releases/S0050-release-notes.md`
- `handoffs/release_queue.md`
- `handoffs/release_notes.md`
