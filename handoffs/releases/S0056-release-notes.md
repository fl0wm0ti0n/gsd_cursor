# Release notes — documentation audience profiles and dual README (DEC-0059)

## What shipped

- **Scratchpad** — `DOC_AUDIENCE_PROFILE` and `DOC_DETAIL_LEVEL` on active + template baseline and `.cursor/scratchpad.local.example.md` (defaults per **DEC-0059** §6); invalid enums → `DOC_PROFILE_INVALID`; merge failures → `DOC_PROFILE_MERGE_ERROR`.
- **`scripts/doc_profile_lib.py`** — 9-cell resolution, H2 mapping, budgets, template parity helpers, non-destructive `ensure_doc_surfaces_merged`.
- **`scripts/validate_doc_profile.py`** — `--repo`, `--no-template-parity`, `--self-test`; optional-mode stderr hints when `SPEC_PACK_MODE` / `USER_GUIDE_MODE` are on.
- **Installer** — `installer.py` `_doc_profile_sync` after merged scratchpad validation (idempotent section append).
- **Surfaces** — Root `README.md` + `docs/developer/README.md` (and `template/` mirrors) with normative `USER_*` / `DEV_*` H2 split and **Contributing** pointer pattern.
- **Tests** — `tests/doc_profile_fixtures_test.py`; `tests/run-tests.ps1` / `run-tests.sh` §26j wiring.

## Gate summary

- Check-in test gate: PASS (`tests/report.md`; **730** pass / **2** fail baseline-only; tiered doc-profile + §26j rows **PASS**).
- QA completion gate: PASS (sprint QA findings; no in-scope blockers).
- UAT completion gate: PASS (sprint UAT artifacts; **10/10**).
- Isolation gate: PASS (phase isolation evidence in `docs/engineering/state.md` for this delivery, including **release** checkpoint).
- Strict runtime proof gate: PASS (`orchestrator_run_id=auto-20260327-02`).
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
  1. From the repository root, run the consolidated test runner above; confirm exit code `0` and updated summary in `tests/report.md` (expect **§26j** doc-profile rows **PASS**).
  2. Run `python scripts/validate_doc_profile.py --repo .` (expect exit `0`, `[DOC_PROFILE_VALIDATE_OK]`).
  3. Run `python tests/doc_profile_fixtures_test.py` (expect exit `0`, `[DOC_PROFILE_FIXTURES_OK]`).
  4. Run `python scripts/check-user-visible-metadata.py --repo .` (expect exit `0`).
  5. Open `sprints/S0056/release-findings.md` and confirm verdict **PASS**; open `handoffs/release_queue.md` and confirm row **`S0056`** shows status **`released`**.
- `expected_health_signal`: Consolidated tests **PASS** (baseline **2** fails documented as out-of-scope); doc profile validator + fixtures **PASS**; metadata guard **PASS**; release queue row **`released`**; release findings verdict **PASS**

## Credentials

- `credential_source_refs` (env names only): same as prior releases (`GITHUB_TOKEN`, publish keys as applicable per `docs/engineering/release-targets.json`).
- Never place inline secrets in this file.

## Known issues

- **Homebrew stable vs npm** version asserts remain **FAIL** in the full suite until packaging alignment (**US-0016** / **US-0074** baseline); excluded from **US-0077** release gate per QA/UAT.

## Evidence refs (engineering)

- `sprints/S0056/summary.md`
- `sprints/S0056/qa-findings.md`
- `sprints/S0056/uat.json`
- `sprints/S0056/uat.md`
- `sprints/S0056/release-findings.md`
- `decisions/DEC-0059.md`
- `tests/report.md`
