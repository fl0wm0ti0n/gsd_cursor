# Release Notes — S0104 / US-0104 (Cross-Model Adversarial Critic)

- **sprint_id**: S0104
- **story_refs**: US-0104
- **release_name**: `S0104 — US-0104 cross-model adversarial critic + three-lens jury reconciliation`
- **release_date**: 2026-06-29
- **orchestrator_run_id**: auto-20260628-04
- **verdict**: **PASS**
- **binding_decision**: `DEC-0104`
- **composes**: `US-0048` / `US-0069` / `US-0023` / `US-0103` / `US-0110` (unchanged — populate surfaces US-0110 already reads)

## Summary

Default-off cross-model adversarial critic for the sovereign loop. When operators enable `CROSS_MODEL_REVIEW=1`, `/auto` spawns `/sovereign-critic` after each producer phase using a different model. The critic evaluates through three fixed lenses (Challenger, Architect, Subtractor); `scripts/sovereign_critic_lib.py` reconciles findings via parallel-jury rules (agreement → high confidence; single-finder → flagged). Findings append to `handoffs/sovereign_critic_findings.jsonl` (15-field v1 schema). Anti-slop scoring triggers a bounded producer rework loop; degraded single-model-multi-lens fallback when catalog cannot resolve a distinct critic slug. Isolation evidence gains additive `model_id` v2 when critic is enabled. Default `CROSS_MODEL_REVIEW=0` → zero overhead. Composes with US-0048/US-0069/US-0023/US-0103/US-0110 — no base isolation tuple or `CRITIC_PATH` changes.

## What's new

- **Scratchpad keys (AC-1)** — `CROSS_MODEL_REVIEW=0|1` (default `0`), `CROSS_MODEL_ANTISLOP_THRESHOLD` (default `6`), `CROSS_MODEL_REWORK_MAX` (default `2`); active + template byte-parity.
- **`/sovereign-critic` command (AC-2)** — `.cursor/commands/sovereign-critic.md` + template mirror; `/auto` orchestrator hook after producer phase when enabled.
- **Three-lens jury (AC-3)** — Fixed enum `challenger` / `architect` / `subtractor`; `reconcile_findings()` agreement and single-finder branches.
- **Isolation `model_id` v2 (AC-4)** — Additive optional field on US-0048 evidence tuple when critic enabled; `ISOLATION_EVIDENCE_MODEL_ID_MISSING` fail-closed only when `CROSS_MODEL_REVIEW=1`.
- **Findings artifact + lib (AC-5)** — `handoffs/sovereign_critic_findings.jsonl`; `scripts/sovereign_critic_lib.py` + `scripts/sovereign_critic_validate.py` CLI.
- **Anti-slop rework (AC-6)** — Aggregate `min(lens_scores)`; rework loop capped by `CROSS_MODEL_REWORK_MAX`; `critic_evidence` tuple in `dev_to_qa.md`.
- **Degraded fallback (AC-7)** — `select_critic_model` single-slug path → `degraded_mode=true` + three sequential lens spawns; informational `CROSS_MODEL_DEGRADED_MODE`.
- **Contract tests + docs (AC-8)** — Eight `test_us0104_*` markers + 2 compose guards; parity `--scope=sovereign-critic` (`SOVEREIGN_CRITIC_PAIRS`, 5 pairs); runbook § US-0104; architecture `# US-0104`; 10 reason codes § US-0104.

## Tasks Delivered (11/11)

| Task | Title | AC | Status |
|------|-------|-----|--------|
| T-001 | `CROSS_MODEL_*` scratchpad keys | AC-1 | DONE |
| T-002 | Comment block + 10 reason codes § US-0104 | AC-1, AC-8 | DONE |
| T-003 | `sovereign_critic_lib.py` core API + self_test | AC-3, AC-5 | DONE |
| T-004 | IO helpers + `patch_ledger_cross_model_reviewed` | AC-5 | DONE |
| T-005 | `sovereign_critic_validate.py` + template mirror | AC-5, AC-8 | DONE |
| T-006 | `/sovereign-critic` command + `/auto` hook prose | AC-2 | DONE |
| T-007 | Anti-slop rework loop + `critic_evidence` tuple | AC-6 | DONE |
| T-008 | Isolation evidence `model_id` v2 + fail-closed gate | AC-4 | DONE |
| T-009 | Degraded single-model-multi-lens fallback | AC-7 | DONE |
| T-010 | Eight `test_us0104_*` + 2 compose guards | AC-8 | DONE |
| T-011 | `SOVEREIGN_CRITIC_PAIRS` parity + runbook § US-0104 | AC-8 | DONE |

## DEC-0104 Locked Decisions

- **L1 Scratchpad keys**: `CROSS_MODEL_REVIEW` default `0`; anti-slop threshold `6`; rework cap `2`; zero overhead when `0`.
- **L2 `/sovereign-critic` command**: Fresh critic subagent after producer phase when enabled.
- **L3 Three lenses**: `challenger` / `architect` / `subtractor` — all run per invocation.
- **L4 Findings JSONL v1**: 15 fields at `handoffs/sovereign_critic_findings.jsonl`.
- **L5 Reconciliation**: `ik_<sha16>` issue keys; ≥2 lenses → `confidence=high`; single lens → `medium` + `single_finder=true`.
- **L6 `model_id` v2**: Additive US-0048 extension; required when critic enabled.
- **L7 Anti-slop + rework**: `min(lens_scores)` aggregate; cap → `CROSS_MODEL_REWORK_CAP_EXHAUSTED` decision gate.
- **L8 Degraded fallback**: Same-model multi-lens when distinct slug unavailable — not a hard stop.
- **L9 Ledger hook**: `cross_model_reviewed=true` on US-0103 entries when `AI_DECISION_LEDGER=1`.
- **L10 Contract tests**: eight `test_us0104_*` + 2 compose guards; parity `--scope=sovereign-critic`.
- **L11 Reason codes**: 10 `CROSS_MODEL_*` + `ISOLATION_EVIDENCE_MODEL_ID_MISSING`.
- **L12 Compose do NOT amend**: US-0048 base tuple, US-0069 role matrix, US-0023 fresh-context, US-0110 `CRITIC_PATH`.

## Contract Tests (10/10 PASS)

1. `test_us0104_scratchpad_keys_literals` — PASS
2. `test_us0104_sovereign_critic_command_literals` — PASS
3. `test_us0104_three_lens_enum_contract` — PASS
4. `test_us0104_findings_jsonl_schema_contract` — PASS
5. `test_us0104_reconciliation_agreement_branches` — PASS
6. `test_us0104_model_id_isolation_evidence_extension` — PASS
7. `test_us0104_antislop_rework_cap_literals` — PASS
8. `test_us0104_degraded_fallback_zero_overhead` — PASS
9. `test_us0104_us0048_compose_no_base_schema_change` — PASS
10. `test_us0104_us0110_critic_path_unchanged` — PASS

## Run

- **start_command**: `pytest -k us0104 tests/us0104_contract_test.py -v`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md` § **Cross-Model Adversarial Critic (US-0104)**

## Connect

- **service_url**: N/A (framework governance layer; no app runtime)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `pytest -k us0104 tests/us0104_contract_test.py -v` → expect **10 passed**.
2. `python scripts/sovereign_critic_lib.py --self-test` → expect `[SOVEREIGN_CRITIC_SELF_TEST_OK]`.
3. `python scripts/sovereign_critic_validate.py --self-test` → expect `[SOVEREIGN_CRITIC_VALIDATION_OK]`.
4. `python scripts/check_intake_template_parity.py --scope=sovereign-critic` → expect `[INTAKE_TEMPLATE_PARITY_OK] scope=sovereign-critic pairs=5`.
5. Confirm `.cursor/scratchpad.md` contains three `CROSS_MODEL_*` keys; template byte-identical.
6. Confirm `docs/engineering/reason_codes.md` § US-0104 lists 10 reason codes.
7. Confirm release-queue row **`S0104`** is **`released`** and backlog / acceptance show **`US-0104`** = **DONE** / checked.
8. Confirm `CROSS_MODEL_REVIEW=0` (default) produces no critic side effects (`test_us0104_degraded_fallback_zero_overhead`).

- **expected_health_signal**: Contract tests green; self-tests OK; parity PASS; **`US-0104`** surfaces as **DONE** in backlog and checked in acceptance; existing lifecycle unchanged when `CROSS_MODEL_REVIEW=0`.

## Credentials

- Env-reference-only policy in effect. No secrets in findings JSONL rationale fields.

## Test evidence summary

- **Contract tests**: `pytest -k us0104` → **10 passed** (1.69s).
- **Self-tests**: `sovereign_critic_lib.py --self-test` → `[SOVEREIGN_CRITIC_SELF_TEST_OK]`; `sovereign_critic_validate.py --self-test` → `[SOVEREIGN_CRITIC_VALIDATION_OK]`.
- **Parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=sovereign-critic pairs=5.
- **Verify-work**: PASS — zero discrepancies vs `/qa` phase.
- **Compose regression**: US-0048 base isolation tuple unchanged — PASS; US-0110 `CRITIC_PATH` unchanged — PASS.
- **Documentation**: runbook § US-0104 + architecture `# US-0104` + reason_codes § US-0104.

## Governance references

- **DEC-0104** — critic findings schema, reconciliation, anti-slop, degraded fallback.
- **`docs/engineering/architecture.md`** `# US-0104`.
- **`decisions/DEC-0104.md`**.
- **`docs/engineering/runbook.md`** § Cross-Model Adversarial Critic (US-0104).
- **`docs/engineering/reason_codes.md`** § US-0104.
- **`R-0092`** — research questions (closed Q1–Q7).

## Known Issues

- None blocking release for in-scope **US-0104** / **DEC-0104** delivery.
- **`CROSS_MODEL_REVIEW=0`** (default): no critic spawn or findings writes — zero overhead as designed.
- **`sprints/S0104/uat.json`** remains placeholder (0 steps) — contract tests are primary gate; no UAT AC in DEC-0104.

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (us0104 10/10) |
| qa | pass (no blockers) |
| verify-work | pass (8/8 ACs) |
| uat | waived (contract_tests_primary) |
| isolation | pass (execute+qa+verify-work distinct markers) |
| parity | pass (scope=sovereign-critic pairs=5) |
| self_test | pass (2/2) |
| compose_regression | pass (US-0048 base + US-0110 CRITIC_PATH) |
| readme_feature_coverage_3f | skipped (post-S0077 drift; kit-repo) |
| project_readme_coverage_3g | pass (kit_repo_skipped) |
| publish | skipped (RELEASE_PUBLISH_MODE=disabled) |
| finalization | pass |

## Strict proof (release phase)

- **fresh_context_marker**: `release-S0104-US0104-20260629T000300Z-fresh`
- **isolation_evidence_ref**: `sprints/S0104/release-findings.md,handoffs/releases/S0104-release-notes.md`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=disabled`; `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`.
- **Publish**: `RELEASE_PUBLISH_MODE=disabled` → `publish_snapshot=skipped_disabled` (deterministic no-op).

## Files created

- `scripts/sovereign_critic_lib.py` — critic library
- `scripts/sovereign_critic_validate.py` — validator CLI
- `template/scripts/sovereign_critic_lib.py` — byte-parity mirror
- `template/scripts/sovereign_critic_validate.py` — byte-parity mirror
- `.cursor/commands/sovereign-critic.md` — critic phase command
- `template/.cursor/commands/sovereign-critic.md` — byte-parity mirror
- `tests/us0104_contract_test.py` — 10 contract tests
- `decisions/DEC-0104.md` — locked architecture decisions

## Files modified

- `.cursor/scratchpad.md` — three `CROSS_MODEL_*` keys
- `template/.cursor/scratchpad.md` — byte-parity mirror
- `.cursor/commands/auto.md` — sovereign-critic hook prose
- `template/.cursor/commands/auto.md` — byte-parity mirror
- `docs/engineering/runbook.md` — § Cross-Model Adversarial Critic (US-0104)
- `template/docs/engineering/runbook.md` — byte-parity mirror
- `docs/engineering/architecture.md` — `# US-0104` section
- `docs/engineering/reason_codes.md` — § US-0104 reason code inventory
- `scripts/check_intake_template_parity.py` — `--scope=sovereign-critic` (5 pairs)
- `template/scripts/check_intake_template_parity.py` — byte-parity mirror
- `docs/product/backlog.md` — US-0104 status DONE
- `docs/product/acceptance.md` — US-0104 checked

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **7** OPEN stories remaining (US-0105..US-0109, US-0111..US-0112).
