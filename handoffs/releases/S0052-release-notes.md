# Release notes — scratchpad installer (example-only + materialized baseline)

## What shipped

- **Example-only manifest** — Install payloads ship scratchpad example material; the active workspace scratchpad file is **materialized** from template when missing (or refreshed per policy), not copied as a static manifest blob.
- **Merge validation** — Deterministic merged resolution (local → materialized baseline → example) with fail-closed diagnostics when configuration cannot be resolved safely.
- **Recovery path** — Python installer exposes a post-install scratchpad repair entry point; PowerShell and shell installers delegate to the same path for parity.
- **Docs and automation contracts** — README, runbook, and `/auto` inputs describe the delivery model; triad hot-surface enforcement aligns merged scratchpad policy with the new baseline layer.

## Gate summary

- Check-in test gate: PASS (`tests/report.md`; in-scope installer / scratchpad rows per sprint QA findings; full suite green on recorded run).
- QA completion gate: PASS (sprint QA findings; no in-scope blockers).
- UAT completion gate: PASS (sprint UAT artifacts; ten steps passed, none failed).
- Isolation gate: PASS (`execute`, `qa`, `verify-work` isolation evidence in engineering state log).
- Strict runtime proof gate: PASS (matching tuples, `orchestrator_run_id=auto-20260323-01`).
- Release finalization: PASS (release findings, notes, queue row, legacy pointer; backlog and acceptance already aligned for the delivered story).

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

- `sprints/S0052/summary.md`
- `sprints/S0052/qa-findings.md`
- `sprints/S0052/uat.json`
- `sprints/S0052/uat.md`
- `sprints/S0052/release-findings.md`
- `handoffs/releases/S0052-release-notes.md`
- `handoffs/release_queue.md`
- `handoffs/release_notes.md`
