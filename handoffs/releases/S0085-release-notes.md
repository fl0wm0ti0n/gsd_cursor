# Release Notes — S0085 / BUG-0012 (native-chain drain-advance enforcement)

- **sprint_id**: S0085
- **bug_refs**: BUG-0012
- **release_name**: `S0085 — BUG-0012 native-chain drain-advance enforcement`
- **release_date**: 2026-06-13T01:30:00Z
- **orchestrator_run_id**: auto-20260612-01
- **verdict**: **PASS**
- **binding_decision**: `DEC-0081` (amends `DEC-0080` enforcement layer; composes on `DEC-0078`, `BUG-0006`, `DEC-0069`)
- **research_anchor**: `R-0083`

## Summary

Fixes post-**US-0095** runtime regression where `/auto` with **`AUTO_FLOW_MODE=full_autonomy`** + **`AUTO_BACKLOG_DRAIN=1`** stopped after each story segment despite native in-chat auto-chain contract. **DEC-0081** adds orchestrator **MUST Task-spawn** mandate, native-chain precedence over US-0088 Option B, drain-advance step 6→7 no-stop, continuation-truth breadcrumbs (`native_chain_continuing`, `drain_advance_action`), five `test_bug0012_*` contract subtests, forbidden-prose negative grep, and runbook § **BUG-0012 regression verify** E2E recipe.

## What's new

- **Orchestrator mandate (AC-1)** — `auto.md` § **Orchestrator post-subagent continuation mandate (BUG-0012 / DEC-0081)** + actor distinction table.
- **Native-chain precedence (AC-2)** — `native chain supersedes Option B`; Option B scoped to `NATIVE_CHAIN_UNAVAILABLE` / headless fallback only.
- **Drain-advance no-stop (AC-3, AC-4)** — step 6→7 immediate spawn; `drain_advance_action` enum; `native_chain_continuing` breadcrumbs.
- **Contract tests (AC-5, AC-6)** — five `test_bug0012_*` subtests + forbidden-prose negative grep.
- **Resume pairing (AC-7)** — `resume_brief` orchestrator **MUST Task-spawn** wording (not operator re-`/auto`).
- **E2E recipe (AC-8)** — runbook § **BUG-0012 regression verify**; template parity `--scope=bug-0012`.

## Non-goals (explicit)

- No spawn-only weakening (**BUG-0006** preserved).
- No removal of outer driver (**US-0092** optional fallback retained).
- No **US-0096** delivery-mode changes.

## Run

- **start_command**: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md`

## Connect

- **service_url**: N/A (framework/toolkit repository; no running service)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `pytest -k bug0012 tests/auto_command_contract_test.py -v` → expect **5 passed**.
2. `pytest -k us0095 tests/auto_command_contract_test.py -v` → expect **7 passed** (no US-0095 regression).
3. `python scripts/check_intake_template_parity.py --scope=bug-0012` → expect `[INTAKE_TEMPLATE_PARITY_OK]`.
4. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` → expect `[BUG_VALIDATION_OK]`.
5. Confirm `sprints/S0085/qa-findings.md` **PASS** and `sprints/S0085/uat.json` **8/8 PASS**.
6. Confirm release-queue row `S0085` is `released` and backlog / acceptance show `BUG-0012` = **DONE** / checked.
7. **Operator E2E (UAT-8)**: run runbook § **BUG-0012 regression verify** — scratchpad `AUTO_FLOW_MODE=full_autonomy`, `AUTO_BACKLOG_DRAIN=1`, ≥2 OPEN stories, single `/auto` in Cursor IDE; confirm drain-advance to story B without operator re-`/auto`.

- **expected_health_signal**: Contract tests green; `BUG-0012` surfaces as **DONE** in backlog and checked in acceptance; multi-segment native-chain E2E passes operator recipe.

## Credentials

- Env-reference-only policy in effect. No inline secrets in release artifacts.

## Test evidence summary

- **Contract subtests**: `pytest -k "bug0012 or us0095"` → **12 passed**, 50 subtests.
- **Template parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=bug-0012.
- **Bug validator**: `[BUG_VALIDATION_OK]` pre- and post-release-write.
- **UAT**: **8/8 PASS** (`sprints/S0085/uat.json`); UAT-8 procedural attestation per runbook.

## Governance references

- **DEC-0081** — enforcement layer amending **DEC-0080**.
- **`docs/engineering/architecture.md`** `# BUG-0012`.
- **`docs/engineering/research.md`** `R-0083`.
- **`decisions/DEC-0081.md`**.

## Known Issues

- None blocking release for in-scope **BUG-0012** / **DEC-0081** delivery.
- **readme_feature_coverage_3f**: post-**S0077** portfolio drift observation — live `--enforce` reports broad `coverage_missing` (README ID-marker format); disjoint from **BUG-0012** closure; not a release blocker per prior sprint precedent (**S0080**, **S0078**).

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (bug0012 5/5 + us0095 7/7) |
| qa | pass (no blockers) |
| uat | pass (8/8; UAT-8 procedural attestation) |
| isolation | pass (execute+qa+verify-work distinct markers) |
| strict_proof | pass |
| parity | pass (scope=bug-0012) |
| bug_validate | pass |
| readme_feature_coverage_3f | observation (post-S0077 drift) |
| finalization | pass |

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260612-01-release-release-20260613T013000Z-S0085-BUG0012`
- `proof_hash=44b55cf523c1c6721f1b9e359e683a9216379d5b314f401b0a722f667f51afe2`
- `fresh_context_marker=release-S0085-BUG0012-release-20260613T013000Z-fresh`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=disabled`, `ALLOW_AUTO_PUSH=1`; `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`.
- **Publish**: `RELEASE_PUBLISH_MODE=confirm` → `skipped_pending_operator_confirm` (no automated publish without explicit operator confirmation).

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; bug queue **empty** after **BUG-0012** closure; portfolio next OPEN story **US-0096**.
