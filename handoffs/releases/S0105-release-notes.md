# Release Notes — S0105 / US-0105 (Sovereign Memory)

- **sprint_id**: S0105
- **story_refs**: US-0105
- **release_name**: `S0105 — US-0105 sovereign memory substrate + bounded phase injection`
- **release_date**: 2026-06-29
- **orchestrator_run_id**: auto-20260628-04
- **verdict**: **PASS**
- **binding_decision**: `DEC-0105`
- **composes**: `US-0029` / `US-0080` / `US-0103` / `US-0072` / `US-0096` (unchanged — new directory surface only)

## Summary

Default-off project-level institutional memory for the sovereign loop. When operators enable `SOVEREIGN_MEMORY=1`, cross-run learnings persist in `docs/engineering/sovereign-memory/` JSONL artifacts (decisions-log, mistakes, patterns, plan-drift-register) plus sprint retrospectives. `scripts/sovereign_memory_lib.py` assembles a char-capped `sovereign_memory_digest` (top-N recent + top-K high-impact) injected read-only at phase spawn. Curator `/refresh-context` writes retrospectives and may promote US-0103 ledger highlights. Decision dedup via `decision_key`; mistake-tagging on orchestrator-detectable failure events. Default `SOVEREIGN_MEMORY=0` → zero overhead. Composes with US-0029/US-0080/US-0103 — no research schema, token-profile, or ledger schema changes.

## What's new

- **Scratchpad keys (AC-1)** — `SOVEREIGN_MEMORY=0|1` (default `0`), `SOVEREIGN_MEMORY_TOP_N` (default `5`), `SOVEREIGN_MEMORY_TOP_K` (default `3`), `SOVEREIGN_MEMORY_MAX_CHARS` (default `2048`), `SOVEREIGN_MEMORY_JSONL_MAX_LINES` (default `500`); active + template byte-parity.
- **Sovereign-memory directory (AC-2)** — `docs/engineering/sovereign-memory/` + `retrospectives/`; create-on-first-write JSONL bootstrap; `.gitkeep` parity; v1 field contracts per DEC-0105.
- **Injection lib (AC-3)** — `build_injection_digest()` merges top-N recent + top-K high-impact; dedupe by `entry_id`; hard truncate to `SOVEREIGN_MEMORY_MAX_CHARS`.
- **Phase spawn hook (AC-4)** — Read-only `sovereign_memory_digest` block in spawn context when enabled; US-0023 additive semantics preserved.
- **Curator retrospective (AC-5)** — `/refresh-context` writes `retrospectives/<sprint_id>.md`; optional `promote_from_ledger()` when `AI_DECISION_LEDGER=1`; retros not injected v1.
- **Dedup + mistake-tagging (AC-6)** — `append_decision()` SHA-256 `decision_key` dedup; mistake hooks on `FIX_FAILED` / `REVERT_APPLIED` / `PLAN_FIDELITY_VIOLATION` family.
- **Contract tests + docs (AC-7, AC-8)** — Eight `test_us0105_*` markers + 2 compose guards; parity `--scope=sovereign-memory` (`SOVEREIGN_MEMORY_PAIRS`, 6 pairs); runbook § US-0105; architecture `# US-0105`; 8 reason codes § US-0105.

## Tasks Delivered (11/11)

| Task | Title | AC | Status |
|------|-------|-----|--------|
| T-001 | `SOVEREIGN_MEMORY_*` scratchpad keys | AC-1 | DONE |
| T-002 | Comment block + 8 reason codes § US-0105 | AC-1, AC-8 | DONE |
| T-003 | `sovereign-memory/` directory bootstrap | AC-2 | DONE |
| T-004 | `sovereign_memory_lib.py` read/injection core | AC-3 | DONE |
| T-005 | Append/dedup/rollover/promotion/retrospective | AC-5, AC-6 | DONE |
| T-006 | `sovereign_memory_validate.py` + template mirror | AC-2, AC-8 | DONE |
| T-007 | Phase spawn `sovereign_memory_digest` hook | AC-4 | DONE |
| T-008 | Mistake-tagging hooks in `/auto` + `/execute` | AC-6 | DONE |
| T-009 | `/refresh-context` curator retrospective wiring | AC-5 | DONE |
| T-010 | Eight `test_us0105_*` + 2 compose guards | AC-7, AC-8 | DONE |
| T-011 | `SOVEREIGN_MEMORY_PAIRS` parity + runbook § US-0105 | AC-7, AC-8 | DONE |

## DEC-0105 Locked Decisions

- **L1 Scratchpad keys**: five `SOVEREIGN_MEMORY_*` keys; default `SOVEREIGN_MEMORY=0`; zero overhead when off.
- **L2 Directory surface**: four JSONL families + retrospectives; create-on-first-write bootstrap.
- **L3 JSONL v1 schemas**: shared base fields + family extensions; secret scan heuristics.
- **L4 Injection algorithm**: global top-N + top-K merge; char cap server-side in lib.
- **L5 Phase spawn hook**: additive read-only digest; US-0023 fresh-context unchanged.
- **L6 Curator retrospective**: markdown per sprint; optional ledger promotion.
- **L7 Dedup contract**: `decision_key` SHA-256 prefix; `SOVEREIGN_MEMORY_DECISION_DUPLICATE` on reject.
- **L8 Mistake-tagging**: closed enum v1; orchestrator hooks in auto/execute.
- **L9 US-0103 compose**: per-run ledger unchanged; optional `promote_from_ledger`.
- **L10 US-0029 compose**: `research.md` schema unchanged; `provenance_ref=R-xxxx` only.
- **L11 US-0080 compose**: lib-side digest truncation; `TOKEN_PROFILE` unchanged.
- **L12 Growth/archive**: JSONL rollover to `sovereign-memory-archive/`; distinct from US-0072 triad.

## Contract Tests (10/10 PASS)

1. `test_us0105_scratchpad_keys_literals` — PASS
2. `test_us0105_sovereign_memory_directory_contract` — PASS
3. `test_us0105_jsonl_schema_contract` — PASS
4. `test_us0105_injection_digest_char_cap` — PASS
5. `test_us0105_decision_dedup_branch` — PASS
6. `test_us0105_mistake_tagging_literals` — PASS
7. `test_us0105_zero_overhead_default` — PASS
8. `test_us0105_compose_guards` — PASS
9. `test_us0105_us0029_compose_no_research_schema_change` — PASS
10. `test_us0105_us0080_injection_respects_char_cap` — PASS

## Run

- **start_command**: `pytest -k us0105 tests/us0105_contract_test.py -v`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md` § **Sovereign Memory (US-0105)**

## Connect

- **service_url**: N/A (framework governance layer; no app runtime)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `pytest -k us0105 tests/us0105_contract_test.py -v` → expect **10 passed**.
2. `python scripts/sovereign_memory_lib.py --self-test` → expect `[SOVEREIGN_MEMORY_SELF_TEST_OK]`.
3. `python scripts/sovereign_memory_validate.py --self-test` → expect `[SOVEREIGN_MEMORY_VALIDATION_OK]`.
4. `python scripts/check_intake_template_parity.py --scope=sovereign-memory` → expect `[INTAKE_TEMPLATE_PARITY_OK] scope=sovereign-memory pairs=6`.
5. Confirm `.cursor/scratchpad.md` contains five `SOVEREIGN_MEMORY_*` keys; template byte-identical.
6. Confirm `docs/engineering/reason_codes.md` § US-0105 lists 8 reason codes.
7. Confirm release-queue row **`S0105`** is **`released`** and backlog / acceptance show **`US-0105`** = **DONE** / checked.
8. Confirm `SOVEREIGN_MEMORY=0` (default) produces no writes or injection (`test_us0105_zero_overhead_default`).

- **expected_health_signal**: Contract tests green; self-tests OK; parity PASS; **`US-0105`** surfaces as **DONE** in backlog and checked in acceptance; existing lifecycle unchanged when `SOVEREIGN_MEMORY=0`.

## Credentials

- Env-reference-only policy in effect. No secrets in JSONL text fields (secret-scan heuristics enforced).

## Test evidence summary

- **Contract tests**: `pytest -k us0105` → **10 passed** (1.65s).
- **Self-tests**: `sovereign_memory_lib.py --self-test` → `[SOVEREIGN_MEMORY_SELF_TEST_OK]`; `sovereign_memory_validate.py --self-test` → `[SOVEREIGN_MEMORY_VALIDATION_OK]`.
- **Parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=sovereign-memory pairs=6.
- **Verify-work**: PASS — zero discrepancies vs `/qa` phase.
- **Compose regression**: US-0029 research schema unchanged — PASS; US-0080 char cap honored — PASS; US-0103 ledger read-only promotion — PASS; US-0072 triad archive path distinct — PASS.
- **Documentation**: runbook § US-0105 + architecture `# US-0105` + reason_codes § US-0105.

## Governance references

- **DEC-0105** — sovereign-memory schemas, injection, dedup, retrospective contracts.
- **`docs/engineering/architecture.md`** `# US-0105`.
- **`decisions/DEC-0105.md`**.
- **`docs/engineering/runbook.md`** § Sovereign Memory (US-0105).
- **`docs/engineering/reason_codes.md`** § US-0105.
- **`R-0093`** — research questions (closed Q1–Q7).

## Known Issues

- None blocking release for in-scope **US-0105** / **DEC-0105** delivery.
- **`SOVEREIGN_MEMORY=0`** (default): no JSONL writes, no injection — zero overhead as designed.
- **`test_regression` mistake hook** in enum but deferred v1.1 per DEC-0105 §6 — acceptable non-blocking.
- JSONL files create-on-first-write; only `.gitkeep` tracked at bootstrap.

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (us0105 10/10) |
| qa | pass (no blockers) |
| verify-work | pass (8/8 ACs) |
| uat | waived (contract_tests_primary) |
| isolation | pass (execute+qa+verify-work distinct markers) |
| parity | pass (scope=sovereign-memory pairs=6) |
| self_test | pass (2/2) |
| compose_regression | pass (US-0029/US-0080/US-0103/US-0072) |
| readme_feature_coverage_3f | skipped (post-S0077 drift; kit-repo) |
| project_readme_coverage_3g | pass (kit_repo_skipped) |
| publish | skipped (RELEASE_PUBLISH_MODE=disabled) |
| finalization | pass |

## Strict proof (release phase)

- **fresh_context_marker**: `release-S0105-US0105-20260629T001300Z-fresh`
- **isolation_evidence_ref**: `sprints/S0105/release-findings.md,handoffs/releases/S0105-release-notes.md`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=disabled`; `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`.
- **Publish**: `RELEASE_PUBLISH_MODE=disabled` → `publish_snapshot=skipped_disabled` (deterministic no-op).

## Files created

- `scripts/sovereign_memory_lib.py` — memory library
- `scripts/sovereign_memory_validate.py` — validator CLI
- `template/scripts/sovereign_memory_lib.py` — byte-parity mirror
- `template/scripts/sovereign_memory_validate.py` — byte-parity mirror
- `docs/engineering/sovereign-memory/.gitkeep` — directory bootstrap
- `docs/engineering/sovereign-memory/retrospectives/.gitkeep` — retrospectives bootstrap
- `tests/us0105_contract_test.py` — 10 contract tests
- `decisions/DEC-0105.md` — locked architecture decisions

## Files modified

- `.cursor/scratchpad.md` — five `SOVEREIGN_MEMORY_*` keys
- `template/.cursor/scratchpad.md` — byte-parity mirror
- `.cursor/commands/auto.md` — sovereign_memory_digest hook prose
- `.cursor/commands/execute.md` — mistake-tagging hook prose
- `.cursor/commands/refresh-context.md` — curator retrospective wiring
- `template/.cursor/commands/*` — byte-parity mirrors
- `docs/engineering/runbook.md` — § Sovereign Memory (US-0105)
- `docs/engineering/architecture.md` — `# US-0105` section
- `docs/engineering/reason_codes.md` — § US-0105 reason code inventory
- `docs/engineering/auto-orchestration-reference.md` — spawn digest hook
- `scripts/check_intake_template_parity.py` — `--scope=sovereign-memory` (6 pairs)
- `docs/product/backlog.md` — US-0105 status DONE
- `docs/product/acceptance.md` — US-0105 checked

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **6** OPEN stories remaining (US-0106..US-0109, US-0111..US-0112).
