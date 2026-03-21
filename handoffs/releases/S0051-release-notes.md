# Release Notes - S0051 (`US-0072`)

## What shipped

- **Triad hot-surface enforcement** — `scripts/enforce-triad-hot-surface.py` (`--check`, `--rollover`, `--self-test`) caps merged-scratchpad growth on `docs/engineering/state.md`, `handoffs/po_to_tl.md`, and `docs/engineering/architecture.md`.
- **Deterministic archives** — oversize hot surfaces roll into packs under `handoffs/archive/` and `docs/engineering/architecture-archive/` with verification headers (`boundary`, moved/retained counts, `pack_ref`) per **`DEC-0054`**.
- **Phase contracts** — documented triad gates on `/refresh-context`, `/intake`, `/discovery`, `/architecture`, `/execute` (active + template); `docs/engineering/phase-context.md` (+ template); runbook minimal-read budgets and reason codes; scratchpad keys `PO_TO_TL_*` / `ARCH_*` (+ template + local example).
- **Regression (26f)** — `tests/run-tests.ps1` / `tests/run-tests.sh` cover script existence, self-test, repo `--check`, idempotent rerun, and documentation parity rows.

## Gate summary

- Check-in test gate: PASS (`tests/report.md`; in-scope **26f** / triad + **26e** metadata guard rows per `sprints/S0051/qa-findings.md`; suite-level fails out-of-scope).
- QA completion gate: PASS (`sprints/S0051/qa-findings.md`; no in-scope blockers).
- UAT completion gate: PASS (`sprints/S0051/uat.json`, `sprints/S0051/uat.md`; `10/10` pass).
- Isolation gate: PASS (`execute`, `qa`, `verify-work` isolation evidence in `docs/engineering/state.md`).
- Strict runtime proof gate: PASS (matching tuples, `orchestrator_run_id=auto-20260322-01`).
- Release finalization: PASS (release findings, notes, queue row, legacy pointer; backlog/acceptance already aligned for target story).

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
  1. Run `python scripts/enforce-triad-hot-surface.py --self-test` from repo root (expect exit `0`).
  2. Run `python scripts/enforce-triad-hot-surface.py --check` from repo root (expect exit `0`).
  3. Run `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` from repo root; confirm triad / **26f** rows PASS in `tests/report.md` (per `sprints/S0051/qa-findings.md`).
  4. Confirm release artifacts for `S0051`: `sprints/S0051/release-findings.md`, `handoffs/release_queue.md` (`S0051` → `released`), `handoffs/release_notes.md` (latest pointer).
- `expected_health_signal`: Triad `--check` PASS; **26f** checks PASS in `tests/report.md`; S0051 queue status is `released`; release findings verdict is PASS

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

- `None` for in-scope `US-0072` release contract.
- Non-US-0072 baseline test failures (Homebrew/npm packaging, installer TEST_COMMAND bootstrap asserts) remain documented as out-of-scope in `sprints/S0051/qa-findings.md` (**US-0074**).

## US-0072 evidence refs

- `sprints/S0051/summary.md`
- `sprints/S0051/qa-findings.md`
- `sprints/S0051/uat.json`
- `sprints/S0051/uat.md`
- `sprints/S0051/release-findings.md`
- `handoffs/releases/S0051-release-notes.md`
- `handoffs/release_queue.md`
- `handoffs/release_notes.md`
