# Release Notes — S0103 / US-0103 (AI Decision Ledger + Plan Fidelity policy)

- **sprint_id**: S0103
- **story_refs**: US-0103
- **release_name**: `S0103 — US-0103 append-only AI decision ledger + plan-fidelity tri-state governance`
- **release_date**: 2026-06-28
- **orchestrator_run_id**: auto-20260628-03
- **verdict**: **PASS**
- **binding_decision**: `DEC-0103`
- **composes**: `US-0070` / `US-0069` / `US-0048` / `US-0092` (unchanged — operate ON TOP)

## Summary

Sovereign-loop foundation layer: append-only JSONL decision ledger for every autonomous AI deviation + plan-fidelity tri-state governance (strict/relaxed/extended). Every AI decision made while running autonomously is now auditable. New `handoffs/sovereign_decisions/<orchestrator_run_id>.jsonl` records each decision with 12-field schema (ts, orchestrator_run_id, phase_id, role, decision_id, decision_type, from_artifact, to_artifact, rationale, plan_fidelity, cross_model_reviewed, risk_tier). Governed by `AUTO_PLAN_FIDELITY=strict|relaxed|extended`: strict = hard stop on unapproved deviation, relaxed = AI may drop/reorder ACs with ledger entry, extended = AI may add new stories/features (documented non-blocking). QA cross-checks the ledger at every `/qa` boundary via `ledger_findings` block. Default-off `AI_DECISION_LEDGER=0` → zero overhead when disabled. Composes with US-0070/US-0069/US-0048/US-0092 — operates ON TOP of `resolved_phase_plan` and isolation evidence.

## What's new

- **Scratchpad keys (AC-1, AC-2)** — `AI_DECISION_LEDGER=0|1` (default `0` → zero overhead) + `AUTO_PLAN_FIDELITY=strict|relaxed|extended` (default `strict`); active + template byte-parity.
- **Ledger artifact (AC-2, AC-3)** — `handoffs/sovereign_decisions/<orchestrator_run_id>.jsonl` with deterministic 12-field JSONL schema; append-only with fsync semantics; `.gitkeep` ensures directory exists; template parity.
- **Plan-fidelity tri-state (AC-3, AC-4, AC-5)** — strict mode hard stop on unapproved deviation (`PLAN_FIDELITY_VIOLATION`), relaxed mode allows drop/reorder with ledger entry, extended mode allows scope extension (non-blocking); deviation classifier in `decision_ledger_lib.py::classify_deviation()`.
- **QA cross-check (AC-6)** — `/qa` phase reads ledger → emits `ledger_findings` JSON block in `sprints/S0103/qa-findings.md` with `{entry_count, fidelity_violations[], unrecorded_deviations[], orphan_entries[]}`; `LEDGER_FILE_MISSING` fail-closed when `AI_DECISION_LEDGER=1`.
- **Contract tests (AC-7)** — Eight `test_us0103_*` markers covering scratchpad keys, ledger schema, plan-fidelity tri-state branches, QA cross-check, reason-code inventory, backward composition guard.
- **Reason codes (AC-8)** — 11 reason codes across 2 families: `PLAN_FIDELITY_*` (5 codes: VIOLATION, SCOPE_GATE, OVERRIDE, MODE_INVALID, CONFLICT) + `LEDGER_*` (6 codes: FILE_MISSING, SCHEMA_INVALID, WRITE_FAILED, APPEND_BLOCKED, DUPLICATE_DECISION_ID, SECRET_DETECTED).
- **Helper library + validator** — `scripts/decision_ledger_lib.py` (733 lines, self-test PASS) + `scripts/ledger_validate.py` (154 lines, CLI validator); template byte-parity.
- **Parity scope** — `check_intake_template_parity.py --scope=sovereign-ledger` with `SOVEREIGN_LEDGER_PAIRS` (5 pairs); active + template byte-parity.
- **Documentation** — `docs/engineering/runbook.md` §US-0103 with operator recipes; `docs/engineering/architecture.md` `# US-0103`; `docs/engineering/reason_codes.md` §US-0103 with full inventory; `DEC-0103` locked architecture decisions.
- **Backward compatibility (AC-8)** — `AI_DECISION_LEDGER=0` (default): zero overhead; existing `/auto` lifecycle unchanged; US-0070/US-0069/US-0048/US-0092 contracts UNCHANGED; `test_us0103_us0070_compose_no_schema_change` regression guard.

## Tasks Delivered (11/11)

| Task | Title | AC | Status |
|------|-------|-----|--------|
| T-001 | Scratchpad keys declaration | AC-1, AC-2 | DONE |
| T-002 | Ledger directory structure | AC-2 | DONE |
| T-003 | Helper library contract | AC-2, AC-3, AC-4, AC-5, AC-6 | DONE |
| T-004 | Validator CLI contract | AC-7, AC-8 | DONE |
| T-005 | Deviation classification logic | AC-3, AC-4, AC-5 | DONE |
| T-006 | QA cross-check | AC-6 | DONE |
| T-007 | Contract tests | AC-7 | DONE |
| T-008 | Reason codes documentation | AC-8 | DONE |
| T-009 | Runbook documentation | AC-8 | DONE |
| T-010 | Parity scope registration | AC-8 | DONE |
| T-011 | Backlog execute notes | (carry-over) | DONE |

## DEC-0103 Locked Decisions

- **L1 Scratchpad keys**: `AI_DECISION_LEDGER=0|1` (default `0`); `AUTO_PLAN_FIDELITY=strict|relaxed|extended` (default `strict`); when ledger `0`, zero overhead.
- **L2 Ledger path**: `handoffs/sovereign_decisions/<orchestrator_run_id>.jsonl` — deterministic one-file-per-run.
- **L3 JSONL schema (12 fields)**: `{ts, orchestrator_run_id, phase_id, role, decision_id, decision_type, from_artifact, to_artifact, rationale, plan_fidelity, cross_model_reviewed, risk_tier}`; append-only.
- **L4 strict mode**: ANY unapproved deviation → `PLAN_FIDELITY_VIOLATION` hard stop; operator-approved relaxations via scratchpad override recorded in ledger.
- **L5 relaxed mode**: AI may drop/reorder ACs with ledger entry + QA-verifiable; new scope triggers `PLAN_FIDELITY_SCOPE_GATE`.
- **L6 extended mode**: AI may extend scope (documented non-blocking); QA still cross-checks.
- **L7 QA cross-check**: `/qa` reads ledger → emits `ledger_findings`; `LEDGER_FILE_MISSING` fail-closed.
- **L8 Contract tests**: Eight `test_us0103_*` markers; parity scope `--scope=sovereign-ledger`.
- **L9 Reason codes (2 families)**: 5 `PLAN_FIDELITY_*` + 6 `LEDGER_*`.
- **L10 Backward compat**: `AI_DECISION_LEDGER=0` → zero overhead; US-0070/US-0069/US-0048/US-0092 unchanged; compose do not amend; US-0111 composition via `decision_type=version_derivation`.

## Contract Tests (8/8 PASS)

1. `test_us0103_scratchpad_keys_literals` — PASS
2. `test_us0103_ledger_jsonl_schema_contract` — PASS
3. `test_us0103_strict_mode_hard_stop` — PASS
4. `test_us0103_relaxed_mode_reorder_with_ledger` — PASS
5. `test_us0103_extended_mode_nonblocking` — PASS
6. `test_us0103_qa_crosscheck_ledger_findings` — PASS
7. `test_us0103_reason_code_inventory` — PASS
8. `test_us0103_us0070_compose_no_schema_change` — PASS

## Run

- **start_command**: `pytest -k us0103 tests/us0103_contract_test.py -v`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md` § **US-0103 AI Decision Ledger + Plan Fidelity**

## Connect

- **service_url**: N/A (framework governance layer; no app runtime)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `pytest -k us0103 tests/us0103_contract_test.py -v` → expect **8 passed**.
2. `python scripts/decision_ledger_lib.py --self-test` → expect `[DECISION_LEDGER_SELF_TEST_OK]`.
3. `python scripts/ledger_validate.py --self-test` → expect `[LEDGER_VALIDATION_SELF_TEST_OK]`.
4. `python scripts/check_intake_template_parity.py --scope=sovereign-ledger` → expect `[INTAKE_TEMPLATE_PARITY_OK] scope=sovereign-ledger pairs=5`.
5. Confirm `handoffs/sovereign_decisions/.gitkeep` exists (active + template).
6. Confirm `.cursor/scratchpad.md` contains `AI_DECISION_LEDGER=0` + `AUTO_PLAN_FIDELITY=strict`; template byte-identical.
7. Confirm `sprints/S0103/qa-findings.md` contains `ledger_findings` block with `{entry_count, fidelity_violations[], unrecorded_deviations[], orphan_entries[]}`.
8. Confirm release-queue row **`S0103`** is **`released`** and backlog / acceptance show **`US-0103`** = **DONE** / checked.
9. Confirm `docs/engineering/reason_codes.md` §US-0103 lists 11 reason codes (5 `PLAN_FIDELITY_*` + 6 `LEDGER_*`).

- **expected_health_signal**: Contract tests green; self-tests OK; parity PASS; **`US-0103`** surfaces as **DONE** in backlog and checked in acceptance; existing lifecycle unchanged when `AI_DECISION_LEDGER=0`.

## Credentials

- Env-reference-only policy in effect. Ledger entries at `handoffs/sovereign_decisions/<orchestrator_run_id>.jsonl` — no secrets in rationale field (`LEDGER_SECRET_DETECTED` fail-closed).

## Test evidence summary

- **Contract tests**: `pytest -k us0103` → **8 passed** (0.09s).
- **Self-tests**: `decision_ledger_lib.py --self-test` → `[DECISION_LEDGER_SELF_TEST_OK]`; `ledger_validate.py --self-test` → `[LEDGER_VALIDATION_SELF_TEST_OK]`.
- **Parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=sovereign-ledger pairs=5.
- **Byte-parity (SHA-256)**: `9355ca0424fd16102e27a1f71256f72843c08b00b9f828ab73710350ff504101` — MATCH.
- **Scratchpad keys**: `AI_DECISION_LEDGER=0` + `AUTO_PLAN_FIDELITY=strict` present in `.cursor/scratchpad.md` + `template/.cursor/scratchpad.md`.
- **Ledger directory**: `.gitkeep` present (active + template).
- **Deviation table (code vs architecture)**: 12/12 rows MATCH — NO REGRESSION.
- **Reason codes**: 11 total (5 `PLAN_FIDELITY_*` + 6 `LEDGER_*`) — matches spec.
- **Documentation**: runbook §US-0103 + architecture `# US-0103` + reason_codes §US-0103.
- **Backward composition**: US-0070/US-0069/US-0048/US-0092 — compose, do not amend — PASS.

## Governance references

- **DEC-0103** — deviation classifier, QA cross-check contract, reason codes, ledger schema.
- **`docs/engineering/architecture.md`** `# US-0103`.
- **`decisions/DEC-0103.md`**.
- **`docs/engineering/runbook.md`** §US-0103.
- **`docs/engineering/reason_codes.md`** §US-0103.

## Known Issues

- None blocking release for in-scope **US-0103** / **DEC-0103** delivery.
- **`AI_DECISION_LEDGER=0`** (default): ledger not written, no checks performed — zero overhead as designed.
- **`AUTO_PLAN_FIDELITY=strict`** (default): any unapproved deviation results in hard stop — operator must explicitly approve relaxation via scratchpad override.

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (us0103 8/8) |
| qa | pass (no blockers; 0 findings) |
| uat | pass (8/8 ACs verified) |
| isolation | pass (execute+qa+verify-work distinct markers) |
| strict_proof | pass |
| parity | pass (scope=sovereign-ledger pairs=5) |
| self_test | pass (2/2) |
| readme_feature_coverage_3f | skipped (post-S0077 drift; kit-repo) |
| project_readme_coverage_3g | pass (kit_repo_skipped) |
| publish | skipped (RELEASE_PUBLISH_MODE=disabled) |
| finalization | pass |

## Strict proof (release phase)

- **fresh_context_marker**: `release-S0103-US0103-release-20260628T150000Z-fresh`
- **isolation_evidence_ref**: `sprints/S0103/release-findings.md,handoffs/releases/S0103-release-notes.md`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=disabled`; `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`.
- **Publish**: `RELEASE_PUBLISH_MODE=disabled` → `publish_snapshot=skipped_disabled` (deterministic no-op).

## Files created

- `scripts/decision_ledger_lib.py` — helper library (733 lines)
- `scripts/ledger_validate.py` — CLI validator (154 lines)
- `template/scripts/decision_ledger_lib.py` — byte-parity mirror
- `template/scripts/ledger_validate.py` — byte-parity mirror
- `tests/us0103_contract_test.py` — 8 contract tests
- `handoffs/sovereign_decisions/.gitkeep` — ledger directory
- `template/handoffs/sovereign_decisions/.gitkeep` — ledger directory (template)
- `decisions/DEC-0103.md` — locked architecture decisions

## Files modified

- `.cursor/scratchpad.md` — `AI_DECISION_LEDGER` + `AUTO_PLAN_FIDELITY` keys
- `template/.cursor/scratchpad.md` — byte-parity mirror
- `docs/engineering/runbook.md` — §US-0103 operator recipes
- `template/docs/engineering/runbook.md` — byte-parity mirror
- `docs/engineering/architecture.md` — `# US-0103` section
- `docs/engineering/reason_codes.md` — §US-0103 reason code inventory
- `scripts/check_intake_template_parity.py` — `--scope=sovereign-ledger` (5 pairs)
- `template/scripts/check_intake_template_parity.py` — byte-parity mirror
- `docs/product/backlog.md` — execute_notes, release_notes

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **8** OPEN stories remaining (US-0104..US-0111).
