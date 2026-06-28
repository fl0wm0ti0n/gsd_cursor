# Release Notes — S0110 / US-0110 (Goal-Based Convergence Loops)

- **sprint_id**: S0110
- **story_refs**: US-0110
- **release_name**: `S0110 — US-0110 goal-based convergence predicate + mid-loop progress visibility`
- **release_date**: 2026-06-28
- **orchestrator_run_id**: auto-20260628-04
- **verdict**: **PASS**
- **binding_decision**: `DEC-0110`
- **composes**: `US-0088` / `US-0092` / `US-0095` / `US-0044` / `US-0103` (unchanged — read-only compose surfaces)

## Summary

Sovereign-loop terminal condition: deterministic **convergence predicate** beyond per-segment phase exhaustion, **mid-loop progress visibility**, and **partial-delivery artifact** on timeout. When operators enable `SOVEREIGN_GOAL_MODE=goal_convergence`, `scripts/sovereign_convergence_lib.py` evaluates a five-conjunct predicate (backlog clear, zero deferrals, critic resolved, smoke green, ledger clean) and returns `ConvergenceResult`. Curator `/refresh-context` emits a `goal_progress` JSON block in `handoffs/resume_brief.md` when goal convergence is active. On iteration timeout, `handoffs/sovereign_partial_delivery.md` is written with remediation guidance. Default-off `SOVEREIGN_GOAL_MODE=phase_driven` → zero overhead when not `goal_convergence`. Composes with US-0088/US-0092/US-0095/US-0044/US-0103 — reads composed surfaces only; no stop-matrix changes.

## What's new

- **Scratchpad keys (AC-1)** — `SOVEREIGN_GOAL_MODE=phase_driven|goal_convergence` (default `phase_driven`), `SOVEREIGN_GOAL`, `SOVEREIGN_GOAL_TOP_N` (default `3`), `SOVEREIGN_GOAL_MAX_CHARS` (default `512`), `SOVEREIGN_GOAL_TIMEOUT_MAX` (default `0`); active + template byte-parity.
- **Convergence evaluator (AC-2)** — `evaluate_convergence(repo, scratchpad) -> ConvergenceResult` with five-conjunct predicate, degrade matrix, memoization (≤50ms p95 budget); `scripts/sovereign_convergence_validate.py` validator CLI with `--enforce`.
- **Goal authoring (AC-3)** — explicit `SOVEREIGN_GOAL` wins; else vision top-N auto-derive; `SOVEREIGN_GOAL_DERIVE_FAILED` fail-closed when vision empty/unreadable.
- **Mid-loop progress (AC-4)** — curator `/refresh-context` step 3b emits `goal_progress` fenced JSON under `### goal_progress` in `handoffs/resume_brief.md` when `SOVEREIGN_GOAL_MODE=goal_convergence`.
- **Partial delivery (AC-5)** — `SOVEREIGN_GOAL_TIMEOUT` on iteration cap; `handoffs/sovereign_partial_delivery.md` with required sections (Goal, Evaluated At, Unmet Conditions, Blocked By, Completed Stories, Open Stories, Deferrals Summary, Remediation).
- **Contract tests (AC-6)** — Eight `test_us0110_*` markers; parity `check_intake_template_parity.py --scope=sovereign-convergence` (`SOVEREIGN_CONVERGENCE_PAIRS`, 2 pairs).
- **Backward compat (AC-7)** — `phase_driven` zero-overhead (no eval side effects); compose regression — US-0088/US-0092/US-0095/US-0044 stop-matrix unchanged.
- **Reason codes + docs (AC-8)** — 10 convergence reason codes § US-0110; runbook § Goal-Based Convergence (US-0110); architecture `# US-0110`; template byte-parity.

## Tasks Delivered (11/11)

| Task | Title | AC | Status |
|------|-------|-----|--------|
| T-001 | Scratchpad keys `SOVEREIGN_GOAL_*` | AC-1 | DONE |
| T-002 | Comment block + reason codes § US-0110 | AC-1, AC-8 | DONE |
| T-003 | Lib schemas + self_test | AC-2 | DONE |
| T-004 | `evaluate_convergence` five-conjunct + memoization | AC-2 | DONE |
| T-005 | `resolve_goal` explicit + vision derive | AC-3 | DONE |
| T-006 | `sovereign_convergence_validate.py` + template mirror | AC-2, AC-8 | DONE |
| T-007 | `goal_progress` + refresh-context step 3b | AC-4 | DONE |
| T-008 | Partial delivery + `check_timeout` | AC-5 | DONE |
| T-009 | Eight `test_us0110_*` contract markers | AC-6 | DONE |
| T-010 | `SOVEREIGN_CONVERGENCE_PAIRS` parity scope | AC-6, AC-8 | DONE |
| T-011 | Runbook + compose regression | AC-7, AC-8 | DONE |

## DEC-0110 Locked Decisions

- **L1 Scratchpad keys**: `SOVEREIGN_GOAL_MODE` default `phase_driven`; iteration-count timeout (not wall-clock); zero overhead when `phase_driven`.
- **L2 ConvergenceResult v1**: `{converged, unmet_conditions[], blocked_by[], conjuncts{}, evaluated_at, schema_version}`.
- **L3 goal_progress v1**: emitted by curator `/refresh-context` when `goal_convergence` active.
- **L4 Five-conjunct predicate**: backlog clear, zero deferrals, critic resolved, smoke green, ledger clean — with skip vs fail degrade matrix.
- **L5 Vision auto-derive**: top-N eligible paragraphs from `docs/product/vision.md`; truncate to `SOVEREIGN_GOAL_MAX_CHARS`.
- **L6 Partial delivery**: `SOVEREIGN_GOAL_TIMEOUT` + `handoffs/sovereign_partial_delivery.md` on iteration cap.
- **L7 Backward compat**: `phase_driven` → no evaluation, no progress block, no partial-delivery write.
- **L8 Contract tests**: eight `test_us0110_*` markers; parity `--scope=sovereign-convergence`.
- **L9 Reason codes**: 10 codes (`CONVERGENCE_*`, `SOVEREIGN_GOAL_*`).
- **L10 Compose surfaces**: read-only; US-0088/US-0092/US-0095/US-0044/US-0103 unchanged.

## Contract Tests (8/8 PASS)

1. `test_us0110_scratchpad_keys_literals` — PASS
2. `test_us0110_evaluator_five_conjunct_contract` — PASS
3. `test_us0110_goal_authoring_explicit_and_derive` — PASS
4. `test_us0110_goal_progress_block_shape` — PASS
5. `test_us0110_partial_delivery_timeout` — PASS
6. `test_us0110_reason_code_inventory` — PASS
7. `test_us0110_phase_driven_zero_overhead` — PASS
8. `test_us0110_compose_no_stop_matrix_change` — PASS

## Run

- **start_command**: `pytest -k us0110 tests/us0110_contract_test.py -v`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md` § **Goal-Based Convergence (US-0110 / DEC-0110)**

## Connect

- **service_url**: N/A (framework governance layer; no app runtime)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `pytest -k us0110 tests/us0110_contract_test.py -v` → expect **8 passed**.
2. `python scripts/sovereign_convergence_lib.py --self-test` → expect `[SOVEREIGN_CONVERGENCE_SELF_TEST_OK]`.
3. `python scripts/sovereign_convergence_validate.py --self-test` → expect `[SOVEREIGN_CONVERGENCE_VALIDATION_OK]`.
4. `python scripts/check_intake_template_parity.py --scope=sovereign-convergence` → expect `[INTAKE_TEMPLATE_PARITY_OK] scope=sovereign-convergence pairs=2`.
5. Confirm `.cursor/scratchpad.md` contains five `SOVEREIGN_GOAL_*` keys; template byte-identical.
6. Confirm `docs/engineering/reason_codes.md` § US-0110 lists 10 reason codes.
7. Confirm release-queue row **`S0110`** is **`released`** and backlog / acceptance show **`US-0110`** = **DONE** / checked.
8. Confirm `SOVEREIGN_GOAL_MODE=phase_driven` (default) produces no eval side effects (`test_us0110_phase_driven_zero_overhead`).

- **expected_health_signal**: Contract tests green; self-tests OK; parity PASS; **`US-0110`** surfaces as **DONE** in backlog and checked in acceptance; existing lifecycle unchanged when `SOVEREIGN_GOAL_MODE=phase_driven`.

## Credentials

- Env-reference-only policy in effect. No secrets in convergence artifacts.

## Test evidence summary

- **Contract tests**: `pytest -k us0110` → **8 passed** (1.87s).
- **Self-tests**: `sovereign_convergence_lib.py --self-test` → `[SOVEREIGN_CONVERGENCE_SELF_TEST_OK]`; `sovereign_convergence_validate.py --self-test` → `[SOVEREIGN_CONVERGENCE_VALIDATION_OK]`.
- **Parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=sovereign-convergence pairs=2.
- **UAT**: 10/10 PASS (`sprints/S0110/uat.json`).
- **Verify-work**: PASS — zero discrepancies vs `/qa` phase.
- **Compose regression**: US-0088/US-0092/US-0095/US-0044 stop-matrix unchanged — PASS.
- **Documentation**: runbook § US-0110 + architecture `# US-0110` + reason_codes § US-0110.

## Governance references

- **DEC-0110** — convergence predicate, goal_progress schema, partial-delivery artifact.
- **`docs/engineering/architecture.md`** `# US-0110`.
- **`decisions/DEC-0110.md`**.
- **`docs/engineering/runbook.md`** § Goal-Based Convergence (US-0110).
- **`docs/engineering/reason_codes.md`** § US-0110.
- **`R-0091`** — research questions (closed Q1–Q7).

## Known Issues

- None blocking release for in-scope **US-0110** / **DEC-0110** delivery.
- **`SOVEREIGN_GOAL_MODE=phase_driven`** (default): no convergence evaluation — zero overhead as designed.
- Upstream artifacts for US-0104 (critic) and US-0107 (deferrals) not yet deployed — conjuncts degrade to **skip** with informational `unmet_conditions`.

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (us0110 8/8) |
| qa | pass (no blockers) |
| verify-work | pass (8/8 ACs; UAT 10/10) |
| uat | pass (10/10 verified) |
| isolation | pass (execute+qa+verify-work distinct markers) |
| parity | pass (scope=sovereign-convergence pairs=2) |
| self_test | pass (2/2) |
| compose_regression | pass (US-0088/US-0092/US-0095/US-0044 unchanged) |
| readme_feature_coverage_3f | skipped (post-S0077 drift; kit-repo) |
| project_readme_coverage_3g | pass (kit_repo_skipped) |
| publish | skipped (RELEASE_PUBLISH_MODE=disabled) |
| finalization | pass |

## Strict proof (release phase)

- **fresh_context_marker**: `release-S0110-US0110-release-20260628T210000Z-fresh`
- **isolation_evidence_ref**: `sprints/S0110/release-findings.md,handoffs/releases/S0110-release-notes.md`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=disabled`; `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`.
- **Publish**: `RELEASE_PUBLISH_MODE=disabled` → `publish_snapshot=skipped_disabled` (deterministic no-op).

## Files created

- `scripts/sovereign_convergence_lib.py` — convergence evaluator library
- `scripts/sovereign_convergence_validate.py` — validator CLI
- `template/scripts/sovereign_convergence_lib.py` — byte-parity mirror
- `template/scripts/sovereign_convergence_validate.py` — byte-parity mirror
- `tests/us0110_contract_test.py` — 8 contract tests
- `decisions/DEC-0110.md` — locked architecture decisions

## Files modified

- `.cursor/scratchpad.md` — five `SOVEREIGN_GOAL_*` keys
- `template/.cursor/scratchpad.md` — byte-parity mirror
- `.cursor/commands/refresh-context.md` — step 3b goal_progress emission
- `template/.cursor/commands/refresh-context.md` — byte-parity mirror
- `docs/engineering/runbook.md` — § Goal-Based Convergence (US-0110)
- `template/docs/engineering/runbook.md` — byte-parity mirror
- `docs/engineering/architecture.md` — `# US-0110` section
- `docs/engineering/reason_codes.md` — § US-0110 reason code inventory
- `scripts/check_intake_template_parity.py` — `--scope=sovereign-convergence` (2 pairs)
- `template/scripts/check_intake_template_parity.py` — byte-parity mirror
- `docs/product/backlog.md` — release_notes, status DONE

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **7** OPEN stories remaining (US-0104..US-0107, US-0109..US-0111).
