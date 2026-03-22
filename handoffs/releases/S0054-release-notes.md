# Release notes — scratchpad example-first upgrade and paired catalog parity

## What shipped

- **Example-first scratchpad refresh** — Install and upgrade paths refresh **`.cursor/scratchpad.local.example.md`** from the shipped template before or bundled with materialized **`.cursor/scratchpad.md`** handling, so operators always see an up-to-date copy-from catalog (**`DEC-0057`**).
- **`[SCRATCHPAD_LAYER]` diagnostics** — Operator-visible lines distinguish example refresh, baseline materialize/skip, and preserved user local (**`DEC-0039`** alignment).
- **AC-11 machine gate** — **`scripts/check-scratchpad-pair-parity.py`** enforces paired **section + `KEY=`** set equality on active and template baseline ↔ example pairs; wired into **`tests/run-tests.ps1`** and **`tests/run-tests.sh`**.
- **Docs and parity** — README + runbook (active + `template/`) describe upgrade behavior, drift troubleshooting, and manifest anchors.

## Gate summary

- Check-in test gate: PASS (`tests/report.md`; **712 / 0** on recorded run; pair parity + scratchpad lifecycle rows per sprint QA findings).
- QA completion gate: PASS (sprint QA findings; no in-scope blockers).
- UAT completion gate: PASS (sprint UAT artifacts; eleven steps passed, none failed).
- Isolation gate: PASS (phase isolation evidence in engineering state log for this delivery).
- Strict runtime proof gate: PASS (matching tuples, `orchestrator_run_id=auto-20260326-01`).
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
  1. From the repository root, run the consolidated test runner above; confirm exit code `0` and updated summary in `tests/report.md` (**expect `[SCRATCHPAD_PAIR_OK]`** when pair parity runs).
  2. Run `python scripts/check-user-visible-metadata.py` (expect exit `0`).
  3. Run `python scripts/enforce-triad-hot-surface.py --check` (expect exit `0`).
  4. Open `sprints/S0054/release-findings.md` and confirm verdict **PASS**; open `handoffs/release_queue.md` and confirm row **`S0054`** shows status **`released`**.
- `expected_health_signal`: Consolidated tests **PASS**; metadata guard **PASS**; triad **`--check`** **PASS**; release queue row **`released`**; release findings verdict **PASS**

## Credentials

- `credential_source_refs` (env names only): same as prior releases (`GITHUB_TOKEN`, publish keys as applicable per `docs/engineering/release-targets.json`).
- Never place inline secrets in this file.

## Known issues

- **None** for this milestone’s in-scope release contract.

## Evidence refs (engineering)

- `sprints/S0054/summary.md`
- `sprints/S0054/qa-findings.md`
- `sprints/S0054/uat.json`
- `sprints/S0054/uat.md`
- `sprints/S0054/release-findings.md`
- `decisions/DEC-0057.md`
- `tests/report.md`
