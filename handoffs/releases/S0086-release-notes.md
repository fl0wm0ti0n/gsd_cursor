# Release Notes — S0086 / US-0096 (delivery modes: ultra-lean + mega-quick)

- **sprint_id**: S0086
- **story_refs**: US-0096
- **release_name**: `S0086 — US-0096 delivery modes with layered memory`
- **release_date**: 2026-06-13T16:00:00Z
- **orchestrator_run_id**: auto-20260612-01
- **verdict**: **PASS**
- **binding_decision**: `DEC-0082` (composes on `DEC-0052`, `DEC-0062`, `DEC-0080`, `DEC-0081`)
- **research_anchor**: `R-0082`

## Summary

Delivers opt-in **`DELIVERY_MODE`** axis (**`standard`** | **`ultra_lean`** | **`mega_quick`**, default **`standard`**) controlling lifecycle shape and artifact surfaces while preserving **`TOKEN_PROFILE`** / **`CAVEMAN_MODE`** orthogonality. **`ultra_lean`** collapses eleven phases into four macro-phases with layered memory (**`work/US-xxxx/pack.json`**, **`handoffs/active-context.md`**). **`mega_quick`** routes eligible work to enhanced **`/quick`**. Tranche A universal token wins ship always-on. **`standard`** mode remains byte-compatible with pre-US-0096 baseline markers.

## What's new

- **Scratchpad contract (AC-1)** — **`DELIVERY_MODE`**, **`LEAN_*`**, **`AUTO_DELIVERY_ROUTING`** keys + non-substitution paragraph in scratchpad/reference/runbook.
- **Mode-scoped resolver (AC-7)** — **`resolve_delivery_mode`** step 0 before **DEC-0052**; reinstatement **`standard`**-only; **`PHASE_POLICY_CONFLICT`**.
- **Tranche A wins (AC-3)** — narrow-read in all phase commands, default hot caps, delta handoffs, touch-graph policy.
- **ultra_lean macro-lifecycle (AC-4)** — **`spec` → `plan` → `build+verify` → `ship`**; **`AUTO_IMPLEMENTATION_LOOP`** inside **`build+verify`**.
- **Layered memory (AC-5)** — **`pack.json`** schema v1 + validator; **`active-context.md`** warm index (non-triad).
- **mega_quick routing (AC-6)** — seven **`MEGA_QUICK_*`** eligibility codes; **`/quick`** cross-ref.
- **Backlog routing (AC-8)** — optional **`delivery_mode:`** row field + precedence chain.
- **Quality floor (AC-9)** — checklist + **`LEAN_MEMORY_DISABLED`** gate.
- **Contract tests + parity (AC-10)** — eight **`test_us0096_*`** subtests; **`--scope=us-0096`** parity; harness §26U.
- **Runbook recipes (AC-11)** — operator recipes table + **`ultra_lean`** E2E recipe.
- **Token-cost evidence (AC-12)** — **`delivery_mode`** in run-class object + evidence row column mandate.

## Non-goals (explicit)

- No removal of **`standard`** full lifecycle.
- No weakening of **US-0039** release gates for **`standard`** mode.
- No **`TOKEN_PROFILE`** / **`CAVEMAN_MODE`** substitution.

## Run

- **start_command**: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md` § **Delivery modes (US-0096 / DEC-0082)**

## Connect

- **service_url**: N/A (framework/toolkit repository; no running service)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `pytest -k us0096 tests/auto_command_contract_test.py -v` → expect **8 passed** (115 subtests).
2. `pytest -k us0095 tests/auto_command_contract_test.py -v` → expect **7 passed** (no US-0095 regression).
3. `pytest -k bug0012 tests/auto_command_contract_test.py -v` → expect **5 passed** (no BUG-0012 regression).
4. `python scripts/check_intake_template_parity.py --scope=us-0096` → expect `[INTAKE_TEMPLATE_PARITY_OK]`.
5. `python scripts/pack_json_validate.py --self-test` → expect `[PACK_JSON_SELF_TEST_OK]`.
6. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` → expect `[BUG_VALIDATION_OK]`.
7. Confirm `sprints/S0086/qa-findings.md` **PASS** and `sprints/S0086/uat.json` **12/12 PASS**.
8. Confirm release-queue row `S0086` is `released` and backlog / acceptance show `US-0096` = **DONE** / checked.
9. **Operator E2E (UAT-11)**: run runbook § **`ultra_lean` E2E operator recipe** — set **`DELIVERY_MODE=ultra_lean`**, run **`/auto`** once in Cursor IDE; confirm four macro-phases and valid **`pack.json`**.
10. **Operator token evidence (UAT-12)**: append **`handoffs/token_cost_runs/<orchestrator_run_id>.md`** row with **`delivery_mode`** column per runbook.

- **expected_health_signal**: Contract tests green; `US-0096` surfaces as **DONE** in backlog and checked in acceptance; operator recipes documented.

## Credentials

- Env-reference-only policy in effect. No inline secrets in release artifacts.

## Test evidence summary

- **Contract subtests**: `pytest -k "us0096 or us0095 or bug0012"` → **20 passed**, 165 subtests (release gate re-run).
- **Template parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=us-0096.
- **Pack validator**: `[PACK_JSON_SELF_TEST_OK]`.
- **Bug validator**: `[BUG_VALIDATION_OK]` pre- and post-release-write.
- **UAT**: **12/12 PASS** (`sprints/S0086/uat.json`); UAT-11/UAT-12 procedural attestation per runbook.

## Governance references

- **DEC-0082** — delivery modes + layered memory.
- **`docs/engineering/architecture.md`** `# US-0096`.
- **`docs/engineering/research.md`** `R-0082`.
- **`decisions/DEC-0082.md`**.

## Known Issues

- None blocking release for in-scope **US-0096** / **DEC-0082** delivery.
- **readme_feature_coverage_3f**: post-**S0077** portfolio drift observation — live `--enforce` reports broad `coverage_missing` (README ID-marker format); disjoint from **US-0096** closure; not a release blocker per prior sprint precedent (**S0085**, **S0080**).

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (us0096 8/8 + us0095 7/7 + bug0012 5/5) |
| qa | pass (no blockers) |
| uat | pass (12/12; UAT-11/UAT-12 procedural attestation) |
| isolation | pass (execute+qa+verify-work distinct markers) |
| strict_proof | pass |
| parity | pass (scope=us-0096) |
| pack_validate | pass |
| bug_validate | pass |
| readme_feature_coverage_3f | observation (post-S0077 drift) |
| finalization | pass |

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260612-01-release-release-20260613T160000Z-S0086-US-0096`
- `proof_hash=20f59d2ac3731ab4dfdf67925e5b630bf208dc4c20c84892702b537619dc30b1`
- `fresh_context_marker=release-S0086-US0096-release-20260613T160000Z-fresh`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=disabled`, `ALLOW_AUTO_PUSH=1`; `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`.
- **Publish**: `RELEASE_PUBLISH_MODE=confirm` → `skipped_pending_operator_confirm` (no automated publish without explicit operator confirmation).

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories after **US-0096** closure; backlog drain budget **8** remaining.
