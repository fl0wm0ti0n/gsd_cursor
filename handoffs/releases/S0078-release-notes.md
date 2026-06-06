# Release Notes — S0078 / BUG-0009 (downstream CI packaging leak)

- **sprint_id**: S0078
- **bug_refs**: BUG-0009
- **release_name**: `S0078 — BUG-0009 downstream CI packaging job leak fix`
- **release_date**: 2026-06-06T16:15:00Z
- **orchestrator_run_id**: auto-20260606-02
- **verdict**: **PASS**
- **binding_decision**: `DEC-0075` (US-0017 negative-parity exceptions for `ci.yml` + template `TEST_COMMAND:`)
- **research_anchor**: `R-0075`

## Summary

Fixes the defect where `its-magic` copied its own self-packaging CI jobs (`npm-test`, `brew-test`, `choco-test`) into every generated repository. Downstream template CI now ships only generic `checks` + `auto-fix` jobs; the active kit retains five packaging jobs for self-distribution. Adds drift guard (`check_downstream_ci_guard.py`), harness **§28B**, install smoke, empty template `TEST_COMMAND:` bootstrap, and operator upgrade remediation docs.

## What's new

- **Template CI downstream-safe (AC-1)** — `template/.github/workflows/ci.yml` contains only `checks` + `auto-fix` job keys; green-by-default summary when no tests configured.
- **Active kit CI preserved (AC-2)** — `.github/workflows/ci.yml` retains five jobs including `npm-test`, `brew-test`, `choco-test`.
- **Drift guard (AC-3, AC-7)** — `scripts/check_downstream_ci_guard.py` + `downstream_ci_guard_lib.py` (+ template mirrors); forbidden-pattern scan + active five-job inventory.
- **Contract + harness (AC-3, AC-6)** — `test_bug0009_*` in `auto_command_contract_test.py`; harness **§28B** in `run-tests.ps1` / `run-tests.sh`.
- **Empty template TEST_COMMAND (AC-5)** — `template/docs/engineering/runbook.md` ships blank `TEST_COMMAND:` per DEC-0056 / US-0063 bootstrap.
- **Install smoke (AC-6)** — `test_downstream_ci_yml_job_inventory_*` in installer completeness fixtures.
- **Template parity scope (AC-7)** — `check_intake_template_parity.py --scope=downstream-ci-guard`; no `--scope=ci-downstream`.
- **Operator remediation (AC-8)** — README + runbook upgrade blurb (DEC-0075 §9).
- **Architecture linkage (AC-7)** — `test_bug0009_architecture_linkage` assert-only.

## Non-goals (explicit)

- No strip of packaging jobs from **active** kit CI.
- No byte-parity `--scope=ci-downstream` on intake parity script.
- No mandatory heal of stale repos without upgrade (`new_installs_upgrades_only`).

## Run

- **start_command**: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runtime-connectivity.md`

## Connect

- **service_url**: N/A (framework/toolkit repository; no running service)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `python scripts/check_downstream_ci_guard.py --self-test`
   → expect `[DOWNSTREAM_CI_GUARD_SELF_TEST_OK]` (exit 0).
2. `python scripts/check_downstream_ci_guard.py --repo . --report`
   → expect `ok=true`, `template_job_keys=[checks,auto-fix]`, active five jobs, `forbidden_hits=[]`.
3. `python scripts/check_intake_template_parity.py --scope=downstream-ci-guard`
   → expect `[INTAKE_TEMPLATE_PARITY_OK]` (exit 0).
4. `python -m pytest tests/auto_command_contract_test.py -q -k bug0009`
   → expect 6 passed.
5. `python -m pytest tests/installer_completeness_bug0003_test.py -q -k downstream_ci`
   → expect 2 passed.
6. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance`
   → expect `[BUG_VALIDATION_OK]` (exit 0).
7. Confirm template `ci.yml` SHA-256 ≠ active `ci.yml` (US-0017 negative parity).
8. Confirm `template/docs/engineering/runbook.md` line 5: `TEST_COMMAND:` (empty value).
9. `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
   → expect Pass=802 / Fail=14 (14 pre-existing disjoint).
10. Confirm `sprints/S0078/qa-findings.md` PASS and `sprints/S0078/uat.json` 8/8 PASS.
11. Confirm release-queue row `S0078` is `released` and backlog / acceptance show `BUG-0009` = DONE / checked.

- **expected_health_signal**: All artifact checks above pass; `BUG-0009` surfaces as `DONE` in backlog and checked in acceptance.

## Credentials

- Env-reference-only policy in effect. No inline secrets in release artifacts.

## Test evidence summary

- **Canonical `tests/run-tests.ps1`**: Pass=**802** / Fail=**14** (`tests/report.md` Timestamp=2026-06-06T14:08:25Z). +5 fail vs S0077 QA baseline; disjoint from DEC-0075 deliverables.
- **Drift guard**: self-test OK; `--report` `ok=true`.
- **Contract subtests**: `pytest -k bug0009` 6 passed.
- **Install smoke**: `pytest -k downstream_ci` 2 passed.
- **Bug validator**: `[BUG_VALIDATION_OK]` pre- and post-release-write.
- **Parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=downstream-ci-guard.

## Governance references

- **DEC-0075** — downstream CI shape, drift guard, US-0017 negative parity, upgrade remediation.
- **US-0017** — template parity with explicit `ci.yml` exception.
- **US-0008** / **US-0018** — installer copy paths and upgrade heal.
- **`docs/engineering/architecture.md`** `# BUG-0009`.
- **`docs/engineering/research.md`** `R-0075`.

## Known Issues

- None blocking release. Pre-existing harness Fail=14 remains for separate triage.
- OPEN bugs `BUG-0010`, `BUG-0011` remain on portfolio bug queue.
- Post-S0077 readme feature coverage live `--enforce` drift (`US-0091` `user_visible` metadata + README parity) — disjoint from BUG-0009; see `sprints/S0078/release-findings.md` §Doc gates.

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (802/14; 14 pre-existing disjoint) |
| qa | pass (cycle 1) |
| uat | pass (8/8) |
| isolation | pass |
| strict_proof | pass |
| downstream_ci_guard | pass |
| readme_feature_coverage_3f | observation (pre-existing drift; S0077 canonical pass) |
| bug_validate | pass |
| finalization | pass |

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260606-02-release-release-20260606T161500Z-S0078-BUG0009`
- `proof_hash=ca36057ca8aff89ceee48d2474bf84c5533f777c9f9cd194a1c18ef8425484bc`
- `fresh_context_marker=release-S0078-BUG0009-release-20260606T161500Z-fresh`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=by_phase`, `ALLOW_AUTO_PUSH=1`, branch `main`; `push_decision=blocked`, `reason_code=TEST_FAILED` (canonical harness Fail=14; disjoint from BUG-0009).
- **Publish**: `RELEASE_PUBLISH_MODE=confirm` → `skipped_pending_operator_confirm`.

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** for **`BUG-0010`**.
