# Release notes — interactive intake evidence enforcement (DEC-0060 / US-0078)

## What shipped

- **`scripts/intake_evidence_lib.py`** — pack resolution, `ie:` ref build/verify, `validate_intake_evidence()` with deterministic reason codes (`INTAKE_REQUIRED_TOPIC_MISSING`, `INTAKE_REQUIRED_PACK_INCOMPLETE`, `INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`, `INTAKE_PERSISTENCE_BLOCKED`), asked-vs-covered and assumption binding; guided/low-touch parity.
- **`scripts/intake_evidence_validate.py`** — CLI `--self-test`, `--file`, `--stdin`.
- **`tests/intake_evidence_fixtures_test.py`** — **R-0055** **AC-8** matrix (P1–P5) + unknown pack + subprocess golden JSON smoke.
- **Workflow/docs** — `.cursor/commands/intake.md`, `po.mdc`, `core.mdc`, `execute.md`, `docs/engineering/runbook.md`, README surfaces (+ `template/` / `its_magic/` parity); **`decisions/DEC-0060`**; **`architecture.md`** **`# US-0078`**.

## Gate summary

- Check-in test gate: PASS (`tests/report.md`; **743** pass / **2** fail baseline-only Homebrew vs npm; §26k intake rows **PASS**).
- QA completion gate: PASS (sprint QA findings; no in-scope blockers).
- UAT completion gate: PASS (sprint UAT artifacts; **10/10**).
- Isolation gate: PASS (phase isolation evidence in `docs/engineering/state.md` for this delivery, including **release** checkpoint).
- Strict runtime proof gate: PASS (`orchestrator_run_id=auto-20260328-01`).
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
  1. From the repository root, run the consolidated test runner above; confirm §26k intake evidence rows **PASS** (expect **2** unrelated Homebrew/npm baseline **FAIL** until **US-0016** / **US-0074** alignment).
  2. Run `python scripts/intake_evidence_validate.py --self-test` (expect exit `0`, `[INTAKE_EVIDENCE_SELF_TEST_OK]`).
  3. Run `python tests/intake_evidence_fixtures_test.py` (expect exit `0`, `[INTAKE_EVIDENCE_FIXTURES_OK]`).
  4. Open `sprints/S0057/release-findings.md` and confirm verdict **PASS**; open `handoffs/release_queue.md` and confirm row **`S0057`** shows status **`released`**.
- `expected_health_signal`: Intake validator + fixtures **PASS**; consolidated tests show documented baseline noise only; release queue row **`released`**; release findings verdict **PASS**

## Credentials

- `credential_source_refs` (env names only): same as prior releases (`GITHUB_TOKEN`, publish keys as applicable per `docs/engineering/release-targets.json`).
- Never place inline secrets in this file.

## Known issues

- **Homebrew stable vs npm** version asserts remain **FAIL** in the full suite until packaging alignment (**US-0016** / **US-0074** baseline); excluded from **US-0078** release gate per QA/UAT.
- Grandfathered legacy intake rows: next intake-driven mutation must supply full **`topic_coverage`** per **DEC-0060**.

## Evidence refs (engineering)

- `sprints/S0057/summary.md`
- `sprints/S0057/qa-findings.md`
- `sprints/S0057/uat.json`
- `sprints/S0057/uat.md`
- `sprints/S0057/release-findings.md`
- `decisions/DEC-0060.md`
- `tests/report.md`
