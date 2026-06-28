# Release Notes — S0107 / US-0107 (Sovereign Loop Mode)

- **sprint_id**: S0107
- **story_refs**: US-0107
- **release_name**: `S0107 — US-0107 sovereign loop mode (AUTO_SOVEREIGN) + deferral register + drain-generate`
- **release_date**: 2026-06-29
- **orchestrator_run_id**: auto-20260628-04
- **verdict**: **PASS**
- **binding_decision**: `DEC-0107`
- **composes**: `US-0088` / `US-0092` / `US-0095` / `US-0103` / `US-0105` / `US-0110` (unchanged — sovereign loop layers on native chain)

## Summary

Default-off sovereign loop orchestration for project-level autonomous delivery. When operators enable `AUTO_SOVEREIGN=1` (requires `SOVEREIGN_GOAL_MODE=goal_convergence`), the loop owns deferrals, drain-generate, notifications, and convergence hooks on top of existing US-0088/US-0092/US-0095 stop matrix. `handoffs/sovereign_deferrals.jsonl` provides a bounded deferral register; `scripts/sovereign_loop_lib.py` implements `advance_sovereign_loop`, drain-generate spawn inputs with mandatory per-candidate decision gate, and fail-open notification adapters (ntfy/hook; email deferred v1). US-0110 `evaluate_convergence` gates drain-generate; US-0109 `DEPLOY_DEFERRED` integration declared in runbook. Default `AUTO_SOVEREIGN=0` → zero overhead.

## What's new

- **Scratchpad keys (AC-1)** — Nine `AUTO_SOVEREIGN_*` + `SOVEREIGN_NOTIFY_*` keys with DEC-0107 defaults; fail-closed `SOVEREIGN_LOOP_GOAL_MODE_REQUIRED` when sovereign on without goal_convergence; active + template byte-parity.
- **Deferral register (AC-2)** — `handoffs/sovereign_deferrals.jsonl` JSONL v1 schema + `handoffs/sovereign_deferrals/.gitkeep` bootstrap; `append_deferral` / `resolve_deferral` / `list_open_deferrals` API; cap enforcement via `AUTO_SOVEREIGN_DEFERRAL_MAX`.
- **Orchestrator advance (AC-3)** — `advance_sovereign_loop` + `SovereignLoopStepResult`; `AUTO_SOVEREIGN_DEFERRAL_POLICY` branches (stop/skip/resolve_first).
- **Drain-generate (AC-4)** — PO spawn inputs + candidate bundle schema; 3-candidate cap; spawn-only per US-0095; mandatory decision gate prose in `/auto`.
- **Notification dispatch (AC-5)** — `dispatch_notification` ntfy/hook adapters fail-open; email deferred v1; `SOVEREIGN_NOTIFY_TARGET=off` zero overhead.
- **Convergence + US-0109 (AC-6)** — US-0110 compose via `list_open_deferrals` for `zero_deferrals`; runbook § US-0109 `DEPLOY_DEFERRED` integration declaration.
- **Contract tests + docs (AC-7, AC-8)** — Eight `test_us0107_*` markers + 2 compose guards; parity `--scope=sovereign-loop` (`SOVEREIGN_LOOP_PAIRS`, 6 pairs); runbook § Sovereign Loop Mode; 12 reason codes § US-0107.

## Tasks Delivered (12/12)

| Task | Title | AC | Status |
|------|-------|-----|--------|
| T-001 | `AUTO_SOVEREIGN_*` + `SOVEREIGN_NOTIFY_*` scratchpad keys | AC-1 | DONE |
| T-002 | Sovereign Loop comment block + 12 reason codes § US-0107 | AC-1, AC-8 | DONE |
| T-003 | `sovereign_deferrals/.gitkeep` + sidecar schema | AC-2 | DONE |
| T-004 | Deferral CRUD, secret scan, self-test core | AC-2, AC-3 | DONE |
| T-005 | `advance_sovereign_loop` full algorithm | AC-3 | DONE |
| T-006 | `sovereign_loop_validate.py` CLI + template mirror | AC-2, AC-8 | DONE |
| T-007 | Drain-generate spawn inputs + `/auto` decision gate prose | AC-4 | DONE |
| T-008 | `dispatch_notification` ntfy/hook adapters | AC-5 | DONE |
| T-009 | US-0110 `zero_deferrals` compose import | AC-6 | DONE |
| T-010 | Eight `test_us0107_*` + 2 compose guards | AC-7, AC-8 | DONE |
| T-011 | `SOVEREIGN_LOOP_PAIRS` parity `--scope=sovereign-loop` | AC-7 | DONE |
| T-012 | Runbook § Sovereign Loop Mode + US-0109 declaration | AC-6, AC-8 | DONE |

## DEC-0107 Locked Decisions

- **L1 Scratchpad keys**: `AUTO_SOVEREIGN=0|1` default `0`; deferral/drain-generate/notify config; goal-mode coupling fail-closed.
- **L2 Deferral register**: JSONL v1 at `handoffs/sovereign_deferrals.jsonl`; cap `AUTO_SOVEREIGN_DEFERRAL_MAX`.
- **L3 Orchestrator advance**: `advance_sovereign_loop` consults deferrals per policy before story selection.
- **L4 Drain-generate**: PO spawn when backlog empty + not converged; decision gate per candidate; cap `AUTO_SOVEREIGN_DRAIN_GENERATE_MAX`.
- **L5 Notification**: fail-open ntfy/hook; email deferred v1.
- **L6 US-0109 integration**: `DEPLOY_DEFERRED` schema contract declared; no deploy smoke in US-0107.
- **L7 Compose US-0088/0092/0095**: stop matrix unchanged; sovereign adds terminal stops only.
- **L8 Compose US-0103**: optional deferral provenance; ledger schema unchanged.
- **L9 Compose US-0105**: drain-generate reads injection digest API when enabled.
- **L10 Compose US-0110**: convergence hooks; no DEC-0110 amendment.
- **L11 Compose US-0044/US-0087**: drain mutex unchanged.
- **L12 Contract tests + parity**: eight `test_us0107_*` + `SOVEREIGN_LOOP_PAIRS`.

## Contract Tests (10/10 PASS)

1. `test_us0107_scratchpad_keys_literals` — PASS
2. `test_us0107_deferral_jsonl_schema_contract` — PASS
3. `test_us0107_advance_deferral_policy_literals` — PASS
4. `test_us0107_drain_generate_gate_contract` — PASS
5. `test_us0107_notification_fail_open_literals` — PASS
6. `test_us0107_goal_mode_coupling_fail_closed` — PASS
7. `test_us0107_zero_overhead_default` — PASS
8. `test_us0107_compose_no_stop_matrix_change` — PASS
9. `test_us0107_us0110_convergence_import_contract` — PASS
10. `test_us0107_us0095_spawn_only_regression_guard` — PASS

## Run

- **start_command**: `pytest -k us0107 tests/us0107_contract_test.py -v`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md` § **Sovereign Loop Mode (US-0107)**

## Connect

- **service_url**: N/A (framework governance layer; no app runtime)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `pytest -k us0107 tests/us0107_contract_test.py -v` → expect **10 passed**.
2. `python scripts/sovereign_loop_lib.py --self-test` → expect `[SOVEREIGN_LOOP_SELF_TEST_OK]`.
3. `python scripts/sovereign_loop_validate.py --self-test` → expect `[SOVEREIGN_LOOP_VALIDATION_OK]`.
4. `python scripts/check_intake_template_parity.py --scope=sovereign-loop` → expect `[INTAKE_TEMPLATE_PARITY_OK] scope=sovereign-loop pairs=6`.
5. Confirm `.cursor/scratchpad.md` contains nine `AUTO_SOVEREIGN_*` + `SOVEREIGN_NOTIFY_*` keys; template byte-identical.
6. Confirm `docs/engineering/reason_codes.md` § US-0107 lists 12 reason codes.
7. Confirm release-queue row **`S0107`** is **`released`** and backlog / acceptance show **`US-0107`** = **DONE** / checked.
8. Confirm `AUTO_SOVEREIGN=0` (default) produces noop advance and no filesystem writes (`test_us0107_zero_overhead_default`).

- **expected_health_signal**: Contract tests green; self-tests OK; parity PASS; **`US-0107`** surfaces as **DONE** in backlog and checked in acceptance; existing lifecycle unchanged when `AUTO_SOVEREIGN=0`.

## Credentials

- Env-reference-only policy in effect. Notification hook URLs and ntfy topics must not appear in git-tracked artifacts.

## Test evidence summary

- **Contract tests**: `pytest -k us0107` → **10 passed** (1.85s).
- **Self-tests**: `sovereign_loop_lib.py --self-test` → `[SOVEREIGN_LOOP_SELF_TEST_OK]`; `sovereign_loop_validate.py --self-test` → `[SOVEREIGN_LOOP_VALIDATION_OK]`.
- **Parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=sovereign-loop pairs=6.
- **QA**: PASS — 8/8 ACs (`sprints/S0107/qa-verdict.json`).
- **Compose regression**: US-0088/0092/0095 stop matrix unchanged — PASS; US-0110 zero_deferrals import — PASS; US-0095 spawn-only drain-generate — PASS.
- **Documentation**: runbook § Sovereign Loop Mode + architecture `# US-0107` + reason_codes § US-0107.

## Governance references

- **DEC-0107** — sovereign loop schemas, advance algorithm, drain-generate, notification contracts.
- **`docs/engineering/architecture.md`** `# US-0107`.
- **`decisions/DEC-0107.md`**.
- **`docs/engineering/runbook.md`** § Sovereign Loop Mode (US-0107).
- **`docs/engineering/reason_codes.md`** § US-0107.
- **`R-0094`** — research questions (closed Q1–Q7).

## Known Issues

- None blocking release for in-scope **US-0107** / **DEC-0107** delivery.
- **`AUTO_SOVEREIGN=0`** (default): noop advance, no deferral writes — zero overhead as designed.
- **Email notification** v1 intentionally deferred — `SOVEREIGN_NOTIFY_TARGET=email` returns `SOVEREIGN_NOTIFY_TARGET_INVALID`.
- Drain-generate candidate population remains PO subagent responsibility post-spawn; lib ships empty bundle scaffold and spawn inputs only.

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (us0107 10/10) |
| qa | pass (no blockers; 8/8 ACs) |
| verify-work | not_run (QA evidence primary; handoffs/verify_to_release.md stale S0105) |
| uat | waived (contract_tests_primary) |
| isolation | pass (execute+qa distinct markers) |
| parity | pass (scope=sovereign-loop pairs=6) |
| self_test | pass (2/2) |
| compose_regression | pass (US-0088/0092/0095 + US-0110 + US-0095) |
| readme_feature_coverage_3f | skipped (post-S0077 drift; kit-repo) |
| project_readme_coverage_3g | pass (kit_repo_skipped) |
| publish | skipped (RELEASE_PUBLISH_MODE=disabled) |
| finalization | pass |

## Strict proof (release phase)

- **fresh_context_marker**: `release-S0107-20260629T002300Z-fresh`
- **isolation_evidence_ref**: `sprints/S0107/release-findings.md,handoffs/releases/S0107-release-notes.md`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=disabled`; `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`.
- **Publish**: `RELEASE_PUBLISH_MODE=disabled` → `publish_snapshot=skipped_disabled` (deterministic no-op).

## Files created

- `scripts/sovereign_loop_lib.py` — deferral register, advance algorithm, drain-generate, notifications
- `scripts/sovereign_loop_validate.py` — validator CLI
- `template/scripts/sovereign_loop_lib.py` — byte-parity mirror
- `template/scripts/sovereign_loop_validate.py` — byte-parity mirror
- `handoffs/sovereign_deferrals/.gitkeep` — deferral register bootstrap
- `template/handoffs/sovereign_deferrals/.gitkeep` — byte-parity mirror
- `tests/us0107_contract_test.py` — 10 contract tests
- `decisions/DEC-0107.md` — locked architecture decisions

## Files modified

- `.cursor/scratchpad.md` — nine `AUTO_SOVEREIGN_*` + `SOVEREIGN_NOTIFY_*` keys
- `template/.cursor/scratchpad.md` — byte-parity mirror
- `.cursor/commands/auto.md` — sovereign loop advance + drain-generate decision gate prose
- `template/.cursor/commands/auto.md` — byte-parity mirror
- `scripts/sovereign_convergence_lib.py` — additive `list_open_deferrals` import for `zero_deferrals`
- `docs/engineering/runbook.md` — § Sovereign Loop Mode (US-0107)
- `docs/engineering/reason_codes.md` — § US-0107 reason code inventory
- `scripts/check_intake_template_parity.py` — `--scope=sovereign-loop` (6 pairs)
- `docs/product/backlog.md` — US-0107 status DONE
- `docs/product/acceptance.md` — US-0107 checked

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **5** OPEN stories remaining (US-0106, US-0108, US-0109, US-0111, US-0112).
