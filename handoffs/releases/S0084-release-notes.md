# Release Notes — S0084 / US-0095 (Native in-Cursor `/auto` auto-chaining)

- **sprint_id**: S0084
- **story_refs**: US-0095
- **release_name**: `S0084 — US-0095 Native in-Cursor /auto auto-chaining (no outer driver required in IDE)`
- **release_date**: 2026-06-07T23:30:00Z
- **orchestrator_run_id**: auto-20260607-02
- **verdict**: **PASS**
- **binding_decision**: **DEC-0080** (composes **DEC-0078**, **DEC-0069**, **BUG-0006**, **US-0088**)
- **research_anchor**: **R-0081**

## Summary

Closes the IDE operator-experience gap where **`AUTO_FLOW_MODE=full_autonomy`** + backlog drain still stopped at segment boundaries and directed operators to re-run `/auto` or **`python scripts/auto_outer_driver.py`**. Ships a **native in-chat auto-chain** contract: one `/auto` orchestrator invocation continues via **foreground sequential Task loop** across intersected lifecycle phases and drain segment boundaries without mandatory outer driver or manual re-invocation — while preserving **spawn-only** (**BUG-0006** / **US-0069**), isolation (**US-0048**), strict proof (**US-0056**), and the **US-0088** / **US-0092** hard stop matrix. **`scripts/auto_outer_driver.py`** retained as **optional** headless/CI fallback.

## What's new

- **Native in-chat auto-chain (AC-1)** — `auto.md` + reference Step 5 IDE-primary; foreground sequential Task loop; **`NATIVE_CHAIN_UNAVAILABLE`** fail-closed.
- **IDE drain-advance (AC-2)** — 7-step algorithm; literals `immediately`, `without operator re-`/auto``; no mandatory outer-driver prose in IDE-primary native §.
- **Spawn-only preserved (AC-3)** — **BUG-0006** loop invariants; **US-0069** preflight/post; forbidden in-band patterns absent from native §.
- **Stop matrix unchanged (AC-4)** — hard gates: `decision_gate`, isolation/strict-proof, security deny, caps, unrecoverable `error`, `pause_request`.
- **Outer driver demoted (AC-5)** — README + runbook primary/fallback boundary; outer driver **optional** / **fallback** for IDE; file retained.
- **AUTO_QUIET operator surface (AC-6)** — suppression table; forbidden mandatory outer-driver/re-`/auto`/segment-exhausted wait patterns.
- **DEC-0069 pairing (AC-7)** — resume_brief + state.md mandate before in-chat continuation; **`RESUME_BRIEF_STALE`** fail-closed.
- **Contract tests (AC-8)** — seven `test_us0095_*` subtests green (`pytest -k us0095` → 7 passed).
- **Template parity (AC-9)** — `[INTAKE_TEMPLATE_PARITY_OK]` scope=us-0095; active + `template/` mirrors.
- **Caps + security (AC-10)** — unified cap/ledger breadcrumbs; security deny-list unchanged (no `.env` auto-read, no intake evidence mutation, no publish without **`RELEASE_PUBLISH_MODE=auto`**).

## Non-goals (explicit)

- No removal of decision gates or bypass of QA/release/isolation/strict-proof.
- No deletion of **`scripts/auto_outer_driver.py`**.
- No weakening **BUG-0006** spawn-only invariants.

## Run

- **start_command**: `pytest -k us0095 tests/auto_command_contract_test.py -v`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md` (Native in-chat auto-chain — US-0095)

## Connect

- **service_url**: N/A (framework/toolkit repository; no running service)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `pytest -k us0095 tests/auto_command_contract_test.py -v`
   → expect 7 passed (30 subtests).
2. `python scripts/check_intake_template_parity.py --scope=us-0095`
   → expect `[INTAKE_TEMPLATE_PARITY_OK]`.
3. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance`
   → expect `[BUG_VALIDATION_OK]`.
4. Confirm `.cursor/commands/auto.md` § **Native in-chat auto-chain (US-0095 / DEC-0080)** and runbook § **Native in-chat auto-chain (US-0095)** primary/fallback table.
5. Confirm `scripts/auto_outer_driver.py` exists (scope guard — not deleted).
6. Confirm `sprints/S0084/qa-findings.md` PASS and `sprints/S0084/uat.json` 10/10 PASS.
7. Confirm release-queue row `S0084` is `released` and backlog / acceptance show `US-0095` = DONE / checked.

- **expected_health_signal**: All artifact checks above pass; `US-0095` surfaces as `DONE` in backlog and checked in acceptance.

## Credentials

- Env-reference-only policy in effect. No inline secrets in release artifacts.

## Test evidence summary

- **Canonical `tests/run-tests.ps1`**: Pass=**811** / Fail=**14** (`tests/report.md` Timestamp=2026-06-07T08:24:40Z). Fail=14 pre-existing disjoint.
- **Contract subtests**: `pytest -k us0095` → **7 passed** (release re-run).
- **Parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=us-0095.
- **Bug validator**: `[BUG_VALIDATION_OK]` pre- and post-release-write.
- **readme_feature_coverage_3f**: `[README_FEATURE_COVERAGE_VALIDATE_OK]` live `--enforce` (pre-DONE flip).
- **UAT**: 10/10 PASS (`sprints/S0084/uat.json`, `sprints/S0084/uat.md`).

## Governance references

- **`decisions/DEC-0080.md`** — native in-chat auto-chain decision.
- **`docs/engineering/architecture.md`** `# US-0095`.
- **`docs/engineering/research.md`** `R-0081`.
- **DEC-0078** — outer driver / full-autonomy (composed; outer driver demoted on IDE path).
- **DEC-0069** — resume_brief + state.md pairing mandate.
- **BUG-0006** — spawn-only orchestration invariant.

## Known Issues

- None blocking release. Pre-existing harness Fail=14 remains for separate triage.
- Post-release README feature-coverage backfill for **US-0095** may be required on next `--enforce` after DONE flip (user_visible story; affinity backfill follow-up).

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (811/14; us0095 7/7; 14 pre-existing disjoint) |
| qa | pass (cycle 1) |
| uat | pass (10/10) |
| isolation | pass |
| strict_proof | pass |
| readme_feature_coverage_3f | pass (enforce=1) |
| bug_validate | pass |
| finalization | pass |

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260607-02-release-release-20260607T233000Z-S0084-US0095`
- `proof_hash=423dead28ffb878335ae77568a29c357fffc185859bf3d2fb98dd23f4fe3202d`
- `fresh_context_marker=release-S0084-US0095-release-20260607T233000Z-fresh`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=by_phase`, `ALLOW_AUTO_PUSH=1`, branch `main`; `push_decision=blocked`, `reason_code=TEST_FAILED` (canonical harness Fail=14; disjoint from US-0095).
- **Publish**: `RELEASE_PUBLISH_MODE=confirm` → `skipped_pending_operator_confirm`.

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories after US-0095 closure.
