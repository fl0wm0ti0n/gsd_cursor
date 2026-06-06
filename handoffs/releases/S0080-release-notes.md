# Release Notes — S0080 / BUG-0011 (Caveman voice compression rules)

- **sprint_id**: S0080
- **bug_refs**: BUG-0011
- **release_name**: `S0080 — BUG-0011 Caveman voice compression rules`
- **release_date**: 2026-06-06T17:00:00Z
- **orchestrator_run_id**: auto-20260606-02
- **verdict**: **PASS**
- **binding_decision**: `DEC-0077` (voice section in `caveman.mdc`; composes on `DEC-0072`; US-0090 orthogonal)
- **research_anchor**: `R-0077`

## Summary

Completes **US-0089** voice delivery deferred by **DEC-0072**: adds upstream-aligned voice-compression rules to `.cursor/rules/caveman.mdc` (active + template byte-identical), runbook level table, nine `test_caveman_voice_*` contract markers, harness **§30A**, and intentional SHA baseline bump. With **`CAVEMAN_MODE=1`**, assistants now follow terse/imperative prose semantics while preserving the nine literal regions and non-suppressible gate vocabulary.

## What's new

- **Voice section (AC-1..AC-4, AC-8)** — `## Voice compression (when CAVEMAN_MODE=1)` + six subsections (`### Precedence`, level table, drop rules, auto-clarity, persistence, ultra stub).
- **Template parity (AC-2)** — active/template `caveman.mdc` SHA-256 `C7AAC699C5CDF732BD029FA8C431B2A4D0B5A3A1B91E49D80C19C11C9748BC4D`.
- **Contract tests (AC-5)** — nine `test_caveman_voice_*` subtests; baseline `E10EFC32…E47DE` → `C7AAC699…8BC4D`.
- **Runbook levels (AC-6)** — `#### Voice compression levels` 2-row table; US-0090 subsection untouched.
- **Regression guard (AC-7)** — `test_caveman_default_off_bodies_regression_guard` (DEC-0072 §6 pinned SHA map).
- **Harness §30A (AC-8)** — `tests/run-tests.ps1` / `tests/run-tests.sh`.
- **Architecture linkage (AC-1)** — `test_bug0011_architecture_linkage` assert-only.

## Non-goals (explicit)

- No Wenyan modes; no input-side compression changes (**US-0090** orthogonal).
- No weakening of nine-zone literal invariant or non-suppressible gate vocabulary.
- Qualitative brevity under **`CAVEMAN_MODE=1`** remains operator-verified (UAT-1); CI asserts contract markers only.

## Run

- **start_command**: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runtime-connectivity.md`

## Connect

- **service_url**: N/A (framework/toolkit repository; no running service)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `python -m pytest tests/auto_command_contract_test.py -q -k caveman_voice`
   → expect 9 passed.
2. `python -m pytest tests/auto_command_contract_test.py -q -k "bug0011 or caveman_default_off_bodies"`
   → expect 2 passed.
3. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance`
   → expect `[BUG_VALIDATION_OK]` (exit 0).
4. Confirm active/template `.cursor/rules/caveman.mdc` SHA-256 match (harness §30A).
5. `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
   → expect Pass=808 / Fail=14 (14 pre-existing disjoint).
6. Confirm `sprints/S0080/qa-findings.md` PASS and `sprints/S0080/uat.json` 8/8 PASS (UAT-1 voice spot-check).
7. Confirm release-queue row `S0080` is `released` and backlog / acceptance show `BUG-0011` = DONE / checked.

- **expected_health_signal**: All artifact checks above pass; `BUG-0011` surfaces as `DONE` in backlog and checked in acceptance.

## Credentials

- Env-reference-only policy in effect. No inline secrets in release artifacts.

## Test evidence summary

- **Canonical `tests/run-tests.ps1`**: Pass=**808** / Fail=**14** (`tests/report.md` Timestamp=2026-06-06T14:51:40Z). +1 pass vs S0079 QA baseline; Fail=14 unchanged (disjoint from DEC-0077).
- **Contract subtests**: `pytest -k caveman_voice` 9 passed; combined filter 12 passed at verify-work.
- **Bug validator**: `[BUG_VALIDATION_OK]` pre- and post-release-write.
- **Harness §30A**: PASS.

## Governance references

- **DEC-0077** — voice section outline, SHA bump, harness §30A, runbook levels.
- **DEC-0072** — Caveman mode scaffolding; nine-zone literal invariant preserved.
- **`docs/engineering/architecture.md`** `# BUG-0011`.
- **`docs/engineering/research.md`** `R-0077`.

## Known Issues

- None blocking release. Pre-existing harness Fail=14 remains for separate triage.
- Post-S0077 readme feature coverage live `--enforce` drift (`BUG-0009` gap, `user_visible` metadata) — disjoint from BUG-0011; observation at release gate 3f.

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (808/14; 14 pre-existing disjoint) |
| qa | pass (cycle 1) |
| uat | pass (8/8; UAT-1 voice spot-check PASS) |
| isolation | pass |
| strict_proof | pass |
| caveman_voice | pass |
| readme_feature_coverage_3f | observation (pre-existing drift; S0077 canonical pass) |
| bug_validate | pass |
| finalization | pass |

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260606-02-release-release-20260606T170000Z-S0080-BUG0011`
- `proof_hash=06b929b4b97c50dfb4012154443764c17e2958c409d4df9d0b16dda5b39825fc`
- `fresh_context_marker=release-S0080-BUG0011-release-20260606T170000Z-fresh`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=by_phase`, `ALLOW_AUTO_PUSH=1`, branch `main`; `push_decision=blocked`, `reason_code=TEST_FAILED` (canonical harness Fail=14; disjoint from BUG-0011). `validate-and-push.ps1 -DryRun` script error on null stderr — policy gate `sync_push_gates.py policy` → `ok=true`.
- **Publish**: `RELEASE_PUBLISH_MODE=confirm` → `skipped_pending_operator_confirm`.

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; bug queue **empty** after BUG-0011 closure.
