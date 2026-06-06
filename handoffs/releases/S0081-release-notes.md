# Release Notes — S0081 / US-0092 (Full-autonomy outer driver)

- **sprint_id**: S0081
- **story_refs**: US-0092
- **release_name**: `S0081 — US-0092 Full-autonomy /auto mode + outer driver + self-verification`
- **release_date**: 2026-06-06T22:30:00Z
- **orchestrator_run_id**: auto-20260606-03
- **verdict**: **PASS**
- **binding_decision**: `DEC-0078` (composes on US-0088, DEC-0062, DEC-0047, DEC-0048)
- **research_anchor**: `R-0078`

## Summary

Ships opt-in **`AUTO_FLOW_MODE=full_autonomy`** (default-off) with a stdlib **outer driver** (`scripts/auto_outer_driver.py`), **UAT probe library** (`scripts/uat_probe_lib.py`) for fail-closed self-verify in `/verify-work` and `/qa`, bounded **block-retry ledger**, **drain-without-pause** semantics, **TOKEN_PROFILE orthogonality** audit, and a documented **full-autonomy stop matrix**. Extends **US-0088** continuous multi-phase `/auto` without weakening spawn-only isolation (**BUG-0006**).

## What's new

- **Scratchpad keys (AC-1)** — `AUTO_FLOW_MODE=full_autonomy` enum alongside `manual` and `auto_until_decision`; `AUTO_BLOCK_RETRY_MAX=3`; optional `AUTO_OUTER_DRIVER_TIMEOUT_SECONDS`; active + template + local-example parity.
- **Outer driver (AC-2)** — `scripts/auto_outer_driver.py` stdlib argv/exit-code API; `--self-test`; activation gate exit **2** `AUTO_FLOW_MODE_NOT_FULL_AUTONOMY` on default scratchpad; runbook operator recipe.
- **UAT probe lib (AC-3)** — `scripts/uat_probe_lib.py` seven probe kinds; fail-closed `UAT_PROBE_UNRESOLVED`, `UAT_PROBE_FORBIDDEN`, etc.; `/verify-work` + `/qa` self-verify excerpts.
- **Block-retry ledger (AC-4)** — `handoffs/auto_block_retry/` directory; `BLOCK_RETRY_CAP_EXHAUSTED` exit **6** documented.
- **Drain-without-pause (AC-5)** — outer driver drain-advance without operator pause phrases; `BACKLOG_MAX_STORIES_REACHED` exit **4**.
- **TOKEN_PROFILE orthography (AC-6)** — normative sentence in `auto-orchestration-reference.md` + runbook; removed runbook “automation breadth” conflict.
- **Stop matrix (AC-7)** — `### Full-autonomy stop matrix (US-0092)` in `auto.md` + reference; `RELEASE_PUBLISH_MODE=auto` explicit opt-in.
- **Contract tests (AC-8)** — nine `test_us0092_*` subtests green; US-0088 markers not weakened.
- **Template parity (AC-9)** — `check_intake_template_parity.py --scope=us-0092`; installer manifest lists new scripts.
- **Security / audit (AC-10)** — runbook `### Full-autonomy outer driver (US-0092)` security deny-list (no `.env`, no intake mutation, no publish without `RELEASE_PUBLISH_MODE=auto`).

## Non-goals (explicit)

- No bypass of QA/release/isolation/strict-proof gates (**US-0048**, **US-0056**).
- No change to **`TOKEN_PROFILE`** tier semantics beyond orthogonality clarification.
- No vendor Cursor multi-turn guarantees beyond documented outer-driver hook.
- No auto-read **`.env`** or mutate intake evidence.

## Run

- **start_command**: `python scripts/auto_outer_driver.py --repo . --dry-run` (default scratchpad → exit 2 `AUTO_FLOW_MODE_NOT_FULL_AUTONOMY`; set `AUTO_FLOW_MODE=full_autonomy` to enable)
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runtime-connectivity.md`

## Connect

- **service_url**: N/A (framework/toolkit repository; no running service)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `python -m pytest tests/auto_command_contract_test.py -q -k us0092`
   → expect 9 passed.
2. `python scripts/auto_outer_driver.py --self-test`
   → expect `[AUTO_OUTER_DRIVER_SELF_TEST_OK]`.
3. `python scripts/uat_probe_lib.py --self-test`
   → expect `[UAT_PROBE_LIB_SELF_TEST_OK]`.
4. `python scripts/check_intake_template_parity.py --repo . --scope=us-0092`
   → expect `[INTAKE_TEMPLATE_PARITY_OK]`.
5. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance`
   → expect `[BUG_VALIDATION_OK]`.
6. `python scripts/auto_outer_driver.py --repo . --dry-run` (default scratchpad)
   → expect exit **2** `AUTO_FLOW_MODE_NOT_FULL_AUTONOMY`.
7. Confirm `sprints/S0081/qa-findings.md` PASS and `sprints/S0081/uat.json` 10/10 PASS.
8. Confirm release-queue row `S0081` is `released` and backlog / acceptance show `US-0092` = DONE / checked.

- **expected_health_signal**: All artifact checks above pass; `US-0092` surfaces as `DONE` in backlog and checked in acceptance.

## Credentials

- Env-reference-only policy in effect. No inline secrets in release artifacts. Outer driver deny-list blocks `.env` reads.

## Test evidence summary

- **Canonical `tests/run-tests.ps1`**: Pass=**808** / Fail=**14** (`tests/report.md` Timestamp=2026-06-06T17:10:23Z). Fail=14 pre-existing disjoint.
- **Contract subtests**: `pytest -k us0092` 9 passed (release re-run).
- **Outer driver + UAT probe**: self-tests OK.
- **Bug validator**: `[BUG_VALIDATION_OK]` pre- and post-release-write.
- **Parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=us-0092.

## Governance references

- **DEC-0078** — full_autonomy flow mode, outer driver, UAT probes, stop matrix, block-retry ledger.
- **US-0088** — continuous multi-phase `/auto` (extended, not weakened).
- **DEC-0062** — TOKEN_PROFILE token-cost-only orthogonality.
- **`docs/engineering/architecture.md`** `# US-0092`.
- **`docs/engineering/research.md`** `R-0078`.

## Known Issues

- None blocking release. Pre-existing harness Fail=14 remains for separate triage.
- Post-S0077 readme feature coverage live `--enforce` drift (`BUG-0009` gap, `user_visible` metadata, README parity) — disjoint from US-0092; observation at release gate 3f.

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (808/14; us0092 9/9; 14 pre-existing disjoint) |
| qa | pass (cycle 1) |
| uat | pass (10/10) |
| isolation | pass |
| strict_proof | pass |
| readme_feature_coverage_3f | observation (post-S0077 drift; S0077 canonical pass) |
| bug_validate | pass |
| finalization | pass |

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260606-03-release-release-20260606T223000Z-S0081-US0092`
- `proof_hash=c090713e2791b75a697db7e09c9a874a257e3d79b742436837b6d84d2d1d0c78`
- `fresh_context_marker=release-S0081-US0092-release-20260606T223000Z-fresh`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=by_phase`, `ALLOW_AUTO_PUSH=1`, branch `main`; `push_decision=blocked`, `reason_code=TEST_FAILED` (canonical harness Fail=14; disjoint from US-0092).
- **Publish**: `RELEASE_PUBLISH_MODE=confirm` → `skipped_pending_operator_confirm`.

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories.
