# Release notes — baseline installer checks and package-manager sync

## What shipped

- **Stable package-manager formula** — The Homebrew stable recipe stays aligned with the npm package version and tag URL so automated checks for URL and version consistency pass deterministically.
- **Runbook test command bootstrap** — Installers and the CLI missing-install path materialize a valid `TEST_COMMAND` in the engineering runbook for detectable stacks, with stack-appropriate defaults and template parity.
- **Green consolidated validation** — The full consolidated test runner reports zero failures while preserving strict baseline rows (no masked asserts).

## Gate summary

- Check-in test gate: PASS (`tests/report.md`; baseline rows per sprint QA findings; full suite green on recorded run).
- QA completion gate: PASS (sprint QA findings; no in-scope blockers).
- UAT completion gate: PASS (sprint UAT artifacts; ten steps passed, none failed).
- Isolation gate: PASS (phase isolation evidence in engineering state log for this delivery).
- Strict runtime proof gate: PASS (matching tuples, `orchestrator_run_id=auto-20260324-01`).
- Release finalization: PASS (release findings, notes, queue row, legacy pointer; backlog and acceptance aligned at verify-work).

## Run

- `start_command`: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- `runtime_mode`: `local`
- `runtime_context_ref`: `docs/engineering/runtime-connectivity.md`

## Connect

- `service_url`: `local-workspace://` (repository root on operator machine)
- `service_port`: `n/a`
- `health_endpoint`: `tests/report.md` (latest consolidated test evidence)

## Verify

- `verification_steps`:
  1. From the repository root, run the consolidated test runner above; confirm exit code `0` and a fresh row in `tests/report.md`.
  2. Run `python scripts/check-user-visible-metadata.py` (expect exit `0`).
  3. Run `python scripts/enforce-triad-hot-surface.py --check` (expect exit `0`).
  4. Open the sprint-scoped release findings file under `sprints/` for this milestone and confirm verdict **PASS**; open the release queue tracker and confirm the matching row shows status `released`.
- `expected_health_signal`: Consolidated tests **PASS**; metadata guard **PASS**; triad `--check` **PASS**; release queue row **released**; release findings verdict **PASS**

## Credentials

- `credential_source_refs` (env names only):
  - `GITHUB_TOKEN` (only if using git push in downstream publish flows)
  - `CHOCO_API_KEY` (only if using Chocolatey publish flow)
  - `DOCKER_TOKEN` (only if using container publish flow)
  - `AWS_PROFILE` (only if using AWS publish flow)
- `expected_value_source`:
  - Operator shell/session environment or CI secret store, depending on publish target.
- Never place inline secrets, tokens, or passwords in this file.

## Known Issues

- **None** for this milestone’s in-scope release contract.

## Evidence refs (engineering)

- `sprints/S0053/summary.md`
- `sprints/S0053/qa-findings.md`
- `sprints/S0053/uat.json`
- `sprints/S0053/uat.md`
- `sprints/S0053/release-findings.md`
- `handoffs/releases/S0053-release-notes.md`
- `handoffs/release_queue.md`
- `handoffs/release_notes.md`
