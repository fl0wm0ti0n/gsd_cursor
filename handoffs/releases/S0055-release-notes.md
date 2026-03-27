# Release notes — executable scratchpad-driven sync and validate-and-push (DEC-0058)

## What shipped

- **`scripts/sync_push_gates.py`** — Merged scratchpad policy evaluation (**DEC-0055** / installer merge only); pre/post subcommands with **DEC-0018** reason codes, **qa-findings** scan bounds (**DEC-0058** §6), branch allowlist, **PRE_QA** / blocking QA rules.
- **`scripts/validate-and-push.ps1`** / **`validate-and-push.sh`** — Invoke Python gates; mandatory **TEST_COMMAND** from runbook; optional lint/typecheck when set; **`-DryRun`** / **`--dry-run`**; no silent push when policy disables or blocks.
- **Docs + installer** — Runbook **Executable validate-and-push wiring (DEC-0058)**; README/template; **`sync_push_gates.py`** on installer manifest; tests **26h** fixtures.

## Gate summary

- Check-in test gate: PASS (`tests/report.md`; **721** pass / **2** fail baseline-only; **26h** sync asserts **PASS**).
- QA completion gate: PASS (sprint QA findings; no in-scope blockers).
- UAT completion gate: PASS (sprint UAT artifacts; **10/10**).
- Isolation gate: PASS (phase isolation evidence in `docs/engineering/state.md` for this delivery).
- Strict runtime proof gate: PASS (`orchestrator_run_id=auto-20260327-01`).
- Release finalization: PASS (release findings, notes, queue row, legacy pointer; backlog and acceptance aligned).

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
  1. From the repository root, run the consolidated test runner above; confirm exit code `0` and updated summary in `tests/report.md` (expect **26h** sync / validate-and-push rows **PASS**).
  2. Run `python scripts/check-user-visible-metadata.py` (expect exit `0`).
  3. Optional: `powershell -ExecutionPolicy Bypass -File scripts/validate-and-push.ps1 -DryRun` on a branch that satisfies merged scratchpad + allowlist (or expect deterministic **no_push** reason codes when not eligible).
  4. Open `sprints/S0055/release-findings.md` and confirm verdict **PASS**; open `handoffs/release_queue.md` and confirm row **`S0055`** shows status **`released`**.
- `expected_health_signal`: Consolidated tests **PASS** (baseline **2** fails documented as out-of-scope); metadata guard **PASS**; release queue row **`released`**; release findings verdict **PASS**

## Credentials

- `credential_source_refs` (env names only): same as prior releases (`GITHUB_TOKEN`, publish keys as applicable per `docs/engineering/release-targets.json`).
- Never place inline secrets in this file.

## Known issues

- **Homebrew stable vs npm** version asserts remain **FAIL** in the full suite until packaging alignment (**US-0074** baseline); excluded from **US-0076** release gate per QA.
- Optional doc hygiene: align any stray `sh scripts/validate-and-push.sh` references to **bash** where operators copy-paste (follow-up only).

## Evidence refs (engineering)

- `sprints/S0055/summary.md`
- `sprints/S0055/qa-findings.md`
- `sprints/S0055/uat.json`
- `sprints/S0055/uat.md`
- `sprints/S0055/release-findings.md`
- `decisions/DEC-0058.md`
- `tests/report.md`
