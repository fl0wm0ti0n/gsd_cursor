# Release notes — first-class bug issues (DEC-0061 / US-0079)

## What shipped

- **`scripts/bug_issue_lib.py`** — canonical bug region rules, validation reason codes (`BUG_VALIDATION_*`, `BUG_RECONCILE_ACCEPTANCE_*`), ordering and field checks.
- **`scripts/bug_issue_validate.py`** — `--self-test`, `--backlog`, `--check-acceptance`, `--print-next-id`.
- **`scripts/intake_bug_routing_guard.py`** — defect-shaped prose vs story kind → **`INTAKE_BUG_ROUTING_REQUIRED`** (**DEC-0061** §5).
- **`tests/bug_issue_fixtures_test.py`** — **R-0056** Tier A/B matrix; **`tests/run-tests.ps1`** / **`tests/run-tests.sh`** §26L.
- **`docs/product/backlog.md`** — **`## Bug issues (canonical)`**; **`docs/product/acceptance.md`** — **`## Bug acceptance (canonical)`** (post-Remaining Items per **DEC-0061** §8).
- **Workflow/docs** — `.cursor/commands/intake.md`, `ask.md`, `execute.md`, `status-reconcile.md`, `core.mdc`, `docs/engineering/runbook.md`, README (+ `template/` / `its_magic/` parity); **`decisions/DEC-0061`**; **`architecture.md`** **`# US-0079`**.

## Gate summary

- Check-in test gate: PASS (`tests/report.md`; **758** pass / **2** fail baseline-only Homebrew vs npm; §26L bug-issue rows **PASS**).
- QA completion gate: PASS (sprint QA findings; no in-scope blockers).
- UAT completion gate: PASS (sprint UAT artifacts; **10/10**).
- Isolation gate: PASS (phase isolation evidence in `docs/engineering/state.md` for this delivery through verify-work; **release** checkpoint appended).
- Strict runtime proof gate: PASS (`orchestrator_run_id=auto-20260329-01`).
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
  1. From the repository root, run the consolidated test runner above; confirm §26L bug-issue rows **PASS** (expect **2** unrelated Homebrew/npm baseline **FAIL** until **US-0016** / **US-0074** alignment).
  2. Run `python scripts/bug_issue_validate.py --self-test` (expect exit `0`, `[BUG_VALIDATION_OK]`).
  3. Run `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` (expect `[BUG_VALIDATION_OK]`).
  4. Run `python tests/bug_issue_fixtures_test.py` (expect exit `0`, `[BUG_ISSUE_FIXTURES_OK]`).
  5. Open `sprints/S0058/release-findings.md` and confirm verdict **PASS**; open `handoffs/release_queue.md` and confirm row **`S0058`** shows status **`released`**.
- `expected_health_signal`: Bug validators + fixtures **PASS**; consolidated tests show documented baseline noise only; release queue row **`released`**; release findings verdict **PASS**

## Credentials

- `credential_source_refs` (env names only): same as prior releases (`GITHUB_TOKEN`, publish keys as applicable per `docs/engineering/release-targets.json`).
- Never place inline secrets in this file.

## Known issues

- **Homebrew stable vs npm** version asserts remain **FAIL** in the full suite until packaging alignment (**US-0016** / **US-0074** baseline); excluded from **US-0079** release gate per QA/UAT.

## Deploy (staging / production)

- **Staging:** `DEPLOY_STAGING_COMMAND` from `docs/engineering/runbook.md` — `echo "No staging deploy target configured for this repository"`
- **Production:** `DEPLOY_PROD_COMMAND` from `docs/engineering/runbook.md` — `echo "No production deploy target configured for this repository"`

## Evidence refs (engineering)

- `sprints/S0058/summary.md`
- `sprints/S0058/qa-findings.md`
- `sprints/S0058/uat.json`
- `sprints/S0058/uat.md`
- `sprints/S0058/release-findings.md`
- `decisions/DEC-0061.md`
- `tests/report.md`
