# Release Notes — S0077 / US-0091 (README feature coverage)

- **sprint_id**: S0077
- **story_refs**: US-0091
- **release_name**: `S0077 — US-0091 README feature coverage backfill + blocking drift gate`
- **release_date**: 2026-06-06T13:43:20Z
- **orchestrator_run_id**: auto-20260606-01
- **verdict**: **PASS**
- **binding_decision**: `DEC-0074` (composes on `DEC-0059`; extends US-0030 release doc-gate family without rewrite)
- **research_anchor**: `R-0074`

## Summary

Ships deterministic **README ↔ backlog/acceptance feature coverage**: a one-time audit and backfill across the full README family (root `README.md`, `template/README.md`, `docs/developer/README.md`), plus a stdlib-only validator wired into `/release` step **3f** so user-visible DONE stories and bugs cannot drift out of operator-facing documentation again. Composes on **US-0030** (delta gate) and **US-0077** / **DEC-0059** (audience profiles) without rewriting either.

## What's new

- **Predicate + library (AC-1)** — `scripts/readme_feature_coverage_lib.py` (+ template mirror) implements Option A: canonical `user_visible:` backlog field with H1–H8 migration heuristic when `README_FEATURE_COVERAGE_ENFORCE=0`; heuristic disabled when enforce is active.
- **Audit artifact (AC-2)** — `docs/engineering/context/readme-feature-coverage-audit.json` maps 98 in-scope DONE items to README anchors; `--report` emits sorted gaps with `id`, `kind`, `predicate_source`, `root_h2`, `dev_h2`.
- **Three-file backfill (AC-3)** — root `README.md`, `template/README.md`, and `docs/developer/README.md` populated; `coverage_missing=[]` with `README_FEATURE_COVERAGE_ENFORCE=1`.
- **Audience boundaries (AC-4)** — `docs/engineering/context/readme-section-affinity.json` (+ template mirror) locks section affinity (`affinity_version=1`, five rules); `validate_doc_profile.py` PASS preserved.
- **Validator CLI (AC-5)** — `scripts/validate_readme_feature_coverage.py` (+ template mirror) with `--self-test`, `--report`, `--enforce`, `--audit-out`; umbrella `README_FEATURE_COVERAGE_BLOCKED` and sub-codes (`GAP`, `PARITY_FAIL`, `INPUT_INVALID`, `PROFILE_VIOLATION`).
- **Release gate composition (AC-6)** — `.cursor/commands/release.md` step **3f** documents `README_FEATURE_COVERAGE_ENFORCE` skip/enforce semantics; runbook remediation table for delta (US-0030) vs static (US-0091) checks.
- **Idempotent report (AC-7)** — `--report` JSON `report_schema_version=1` with sorted keys; harness **§27U** + fixtures assert byte-identical consecutive runs.
- **Metadata hygiene (AC-8)** — backfilled blurbs pass `scripts/check-user-visible-metadata.py` on README family surfaces.
- **Template parity (AC-9)** — `check_intake_template_parity.py --scope=readme-feature-coverage`; installer manifest lists new scripts.
- **DEC linkage + enforce flip (AC-10)** — `decisions/DEC-0074.md`; scratchpad `README_FEATURE_COVERAGE_ENFORCE=1` post-backfill; architecture `# US-0091` linkage subtest.

## Non-goals (explicit)

- No rewrite of **US-0030** delta-gate semantics.
- No replacement of **DEC-0059** audience profiles or new H2 vocabulary invention.
- No per-feature user guides (**US-0032** / `USER_GUIDE_MODE`).
- No mandatory regeneration of sections already passing coverage.

## Run

- **start_command**: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runtime-connectivity.md`

## Connect

- **service_url**: N/A (framework/toolkit repository; no running service)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `python scripts/validate_readme_feature_coverage.py --self-test`
   → expect `[README_FEATURE_COVERAGE_SELF_TEST_OK]` (exit 0).
2. `python scripts/validate_readme_feature_coverage.py --repo . --report`
   → expect `status=PASS`, `coverage_missing=[]`, `coverage_total=98`.
3. `python scripts/validate_readme_feature_coverage.py --repo . --enforce`
   → expect `[README_FEATURE_COVERAGE_VALIDATE_OK]` (exit 0).
4. `python scripts/check_intake_template_parity.py --scope=readme-feature-coverage`
   → expect `[INTAKE_TEMPLATE_PARITY_OK]` (exit 0).
5. `python scripts/check-user-visible-metadata.py --repo .` → exit 0.
6. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance`
   → expect `[BUG_VALIDATION_OK]` (exit 0).
7. `python -m pytest tests/readme_feature_coverage_fixtures_test.py -q`
   → expect 3 passed.
8. Confirm `.cursor/scratchpad.md` contains `README_FEATURE_COVERAGE_ENFORCE=1`.
9. `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
   → expect Pass=802 / Fail=9 (9 pre-existing disjoint).
10. Confirm `sprints/S0077/qa-findings.md` PASS and `sprints/S0077/uat.json` 10/10 PASS.
11. Confirm release-queue row `S0077` is `released` and backlog / acceptance show `US-0091` = DONE / checked.

- **expected_health_signal**: All artifact checks above pass; `US-0091` surfaces as `DONE` in backlog and checked in acceptance.

## Credentials

- Env-reference-only policy in effect. No inline secrets in release artifacts.

## Test evidence summary

- **Canonical `tests/run-tests.ps1`**: Pass=**802** / Fail=**9** (+11 pass vs US-0090 QA baseline; 9 failures pre-existing disjoint).
- **Feature coverage validator**: self-test OK; enforce OK; report idempotent.
- **Fixtures**: `tests/readme_feature_coverage_fixtures_test.py` 3 passed / 5 subtests.
- **Bug validator**: `[BUG_VALIDATION_OK]` pre- and post-release-write.
- **Parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=readme-feature-coverage.
- **Metadata guard**: exit 0 on README family.

## Governance references

- **DEC-0074** — README feature coverage predicate, validator, release step 3f, grandfathering.
- **DEC-0059** — dual-README audience profiles (composed, not rewritten).
- **US-0030** — command/flag doc-delta gate (composed, not rewritten).
- **`docs/engineering/architecture.md`** `# US-0091` section.
- **`docs/engineering/research.md`** `R-0074`.

## Known Issues

- None blocking release. Pre-existing harness Fail=9 (Homebrew + installer runbook row) remains for separate triage.
- OPEN bugs `BUG-0009`, `BUG-0010`, `BUG-0011` on portfolio bug queue.

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (802/9; 9 pre-existing disjoint) |
| qa | pass (cycle 1) |
| uat | pass (10/10) |
| isolation | pass |
| strict_proof | pass |
| readme_feature_coverage_3f | pass (`--enforce` live) |
| bug_validate | pass |
| finalization | pass |

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260606-01-release-release-20260606T134320Z-S0077-US0091`
- `proof_hash=cbfc031254b549dfef27f12c4a6d5acb51b528835180b60252e54b44d238bd47`
- `fresh_context_marker=release-S0077-US0091-release-20260606T134320Z-fresh`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=by_phase`, `ALLOW_AUTO_PUSH=1`, branch `main`; `push_decision=blocked`, `reason_code=TEST_FAILED` (9 pre-existing harness failures).
- **Publish**: `RELEASE_PUBLISH_MODE=confirm` → `skipped_pending_operator_confirm`.

## Next phase

**`/refresh-context`** (fresh curator) for segment closeout; then `/auto` backlog drain (budget remaining = 3) or bug queue routing.
