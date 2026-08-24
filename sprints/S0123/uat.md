# Sprint S0123 — UAT (US-0123, code story) — verify-work loop-2 results (post harness-refresh)

**sprint_id**: S0123
**story_refs**: US-0123
**phase**: verify-work (build+verify macro) — loop 2
**role**: qa (fresh per BUG-0006)
**orchestrator_run_id**: auto-20260824-01
**delivery_mode**: ultra_lean
**macro_phase**: build+verify
**story_type**: code
**fresh_context_marker**: `qa-US0123-verify-work-20260824T152400Z-fresh` (NEW; distinct from prior `qa-US0123-verify-work-20260824T150100Z-fresh` and `qa-US0123-qa-20260824T145500Z-fresh`)
**timestamp**: 2026-08-24T15:24:00Z (UTC)
**model_id**: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
**producer_model_id**: composer-2.5-fast (sovereign-critic qa-loop2 phase)
**producer_runtime_proof_id**: rp-auto-20260824-01-qa-qa-20260824T151700Z-US-0123-loop2
**producer_proof_hash**: 9CC32FD6A0EE8C0EDE3696E060BDBD8A8F19E914BFFBE51719E1A7B79704F107
**producer_proof_ttl**: 2026-08-24T16:17:00Z (consumed before expiry — OK)
**verdict**: **PASS** (10/10 ACs; 8/8 contract tests live re-run; parity + validator; compose 6/6 UNCHANGED; byte-identical mirrors; no fake browser PASS; **full-harness Fail:0 claim upheld — report fresh**)
**total_steps**: 10 | **passed**: 10 | **failed**: 0

## Target stories + acceptance criteria

- **US-0123** — Per-role OpenCode model slug routing (multi-provider) (10 ACs)
  - AC-1: PASS — Resolution chain — marker 1 (template agents omit `model:`) + marker 6 (materializer no-op when catalog absent). Architecture picks single SOT; tests assert.
  - AC-2: PASS — Multi-provider examples — marker 3; 6 providers (deepseek, moonshot, zai, anthropic, openai, dashscope) >=4 required. Kit does not proxy traffic.
  - AC-3: PASS — No vendor IDs in template — markers 1, 2, 3 + grep `^model:` 0 matches. Placeholders only.
  - AC-4: PASS — Unknown slug fail-closed — markers 5, 6 — `OPENCODE_MODEL_SLUG_UNKNOWN` reason code (incl. `<your-*-slug>` placeholder case); no-op when catalog absent.
  - AC-5: PASS — Auth store — marker 7 — auth.json/api_key/sk- never in template or git.
  - AC-6: PASS — Compose US-0101/US-0102 — marker 8 — Cursor alias runtime unchanged; OpenCode additive; TOKEN_PROFILE orthogonal.
  - AC-7: PASS — Per-role assignment — marker 4 — >=2 roles configurable to different providers (po->anthropic, dev->deepseek, qa->moonshot, tech-lead->zai, release->openai) without editing `template/`.
  - AC-8: PASS — Contract tests — 8/8 PASS live re-run; markers cover placeholder-only, fail-closed, schema, non-substitution.
  - AC-9: PASS — Chinese APIs as capability — marker 4 — deepseek/moonshot/zai/dashscope present; kit-operated proxy out of scope.
  - AC-10: PASS — Tool-calling quality — runbook h2 `## OpenCode model slug routing (US-0123)` present + byte-identical mirror.

## Contract test markers (8) — 8/8 PASS (verify-work loop-2 live re-run)

`python -m pytest tests/us0123_contract_test.py -v` -> **8 passed in 0.20s** (exit 0; Python 3.12.10; pytest 9.1.1)

1. `test_us0123_template_agents_omit_model` (AC-1, AC-3) — PASS
2. `test_us0123_no_vendor_slugs_in_template` (AC-3) — PASS
3. `test_us0123_example_catalog_placeholders_only` (AC-2, AC-3) — PASS
4. `test_us0123_example_catalog_per_role_divergence` (AC-7, AC-9) — PASS
5. `test_us0123_fail_closed_unknown_slug` (AC-4) — PASS — includes `<your-*-slug>` placeholder case
6. `test_us0123_materializer_no_op_when_catalog_absent` (AC-1, AC-4) — PASS
7. `test_us0123_auth_store_never_in_template_or_git` (AC-5) — PASS
8. `test_us0123_compose_cursor_unchanged` (AC-6, AC-8) — PASS — includes TOKEN_PROFILE orthogonality

## UAT step results

| Step | AC | Result | Evidence |
|------|----|--------|----------|
| UAT-1 | AC-1 | PASS | markers 1 + 6 (live re-run) |
| UAT-2 | AC-2 | PASS | marker 3 — 6 providers |
| UAT-3 | AC-3 | PASS | markers 1,2,3 + grep 0 matches |
| UAT-4 | AC-4 | PASS | markers 5,6 — fail-closed |
| UAT-5 | AC-5 | PASS | marker 7 |
| UAT-6 | AC-6 | PASS | marker 8 — Cursor unchanged |
| UAT-7 | AC-7 | PASS | marker 4 — per-role divergence |
| UAT-8 | AC-8 | PASS | 8/8 markers live re-run |
| UAT-9 | AC-9 | PASS | marker 4 — Chinese APIs present |
| UAT-10 | AC-10 | PASS | runbook h2 byte-identical |

**Counts**: total=10, passed=10, failed=0 (passed + failed = total per DEC-0009).

## Probe results

| Probe ID | Kind | Command | Passed | Reason |
|----------|------|---------|--------|--------|
| `us0123-contract-gate` | pytest | `python -m pytest tests/us0123_contract_test.py -v` | true | 8/8 PASS exit 0 (0.20s) |
| `opencode-adapter-parity` | static | `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` | true | `[INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter` |
| `opencode-catalog-validator` | static | `python scripts/model_tier_validate.py --scope opencode-catalog --repo .` | true | `[MODEL_TIER_VALIDATION_OK]` |
| `harness-report-fresh` | static | read `tests/report.md` header timestamp | true | report @ 2026-08-24T15:12:17Z matches execute harness-refresh handoff @ 2026-08-24T15:12:30Z (fresh) |
| `harness-zero-fail-rows` | static | Grep `\[FAIL\]` over `tests/report.md` | true | 0 matches (zero `[FAIL]` rows) |
| `compose-guards-6-unchanged` | static | read backlog/acceptance/architecture/DEC-0123/template agents/mirrors | true | backlog OPEN; acceptance unchecked; arch anchor; DEC-0123 Accepted; 0 `^model:`; mirrors byte-identical |
| `acceptance-row-unchecked` | static | read acceptance L151 + backlog US-0123 row | true | US-0123 NOT marked DONE; QA did not mutate backlog/acceptance |

## Browser probe — not used

`UAT_BROWSER_PROBE_MODE=cursor` (default). Pack/contract story with no web UI surface. No `browser_smoke` step classified. Per US-0092 / DEC-0078, ACs are mapped to pytest markers + static checks as stack-profile probes with evidence (command + output). No `.env` read. No intake evidence mutation. No `UAT_PROBE_FORBIDDEN`. **No fake browser PASS** — `browser_probe_used=false` recorded.

## Full-harness claim — UPHELD (fresh report, loop 2)

`tests/report.md` header: `Timestamp: 2026-08-24T15:12:17Z` / `Pass: 845` / `Fail: 0`. The report timestamp **matches** the execute harness-refresh handoff timestamp (`2026-08-24T15:12:30Z`) within ~13s — report is FRESH. Grep `\[FAIL\]` over `tests/report.md` returned **0 matches** (zero `[FAIL]` rows). Per QA PASS-claim rule, the full-harness `Fail: 0` claim is **UPHELD** for US-0123 loop-2.

`release_harness_refresh_required` flag from loop-1 is now **satisfied** — release gate-1 may consume the fresh `tests/report.md` directly without another refresh.

## Acceptance + backlog — read-only

`docs/product/acceptance.md` L151 US-0123 row remains `- [ ]` (unchecked). US-0123 NOT marked DONE. Backlog/acceptance NOT mutated by verify-work (closure owns the flip per US-0120 / DEC-0082).

## Compose guards (6/6 UNCHANGED)

| # | Guard | Evidence |
|---|-------|----------|
| 1 | `docs/product/backlog.md` US-0123 | `Status: OPEN` (not mutated) |
| 2 | `docs/product/acceptance.md` US-0123 | `- [ ] US-0123` (unchecked; not mutated) |
| 3 | `docs/engineering/architecture.md` US-0123 | `# US-0123` anchor present (not mutated) |
| 4 | `decisions/DEC-0123.md` | `Status: Accepted` (not mutated) |
| 5 | `template/.opencode/agents/*.md` | grep `^model:` -> 0 matches (no `model:` keys in template) |
| 6 | Byte-identical mirrors | runbook + manifest + 3 paired scripts all SHA-256 equal active<->template |

## Non-blocking findings (carry-forward)

- `ik_us0123_installer_hook_not_contract_tested` (carry-forward): installer `--host opencode|both` hook is not pytest-marked. Non-blocking — T-003 hook covered by installer parity + manual spot-check.

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=verify-work`
- `role=qa`
- `fresh_context_marker=qa-US0123-verify-work-20260824T152400Z-fresh` (NEW; not reused)
- `timestamp=2026-08-24T15:24:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required; **NEW** fresh_context_marker)
- `evidence_ref=sprints/S0123/verify-work-findings.md, sprints/S0123/uat.json, sprints/S0123/uat.md, handoffs/verify_to_release.md, docs/engineering/state.md (verify-work loop-2 checkpoint append-bottom)`
- QA verify-work subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward; no subagent spawned from this QA subagent.

## Strict runtime proof (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-verify-work-qa-20260824T152400Z-US-0123`
- `proof_issued_at=2026-08-24T15:24:00Z`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-08-24T16:24:00Z`
- `proof_hash=5DBDB6549E0E7841974CE7A8D8FE81889AB7ADD0ED79F8FA10AF4C4CD7CA3BE8`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"verify-work","proof_issued_at":"2026-08-24T15:24:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-01-verify-work-qa-20260824T152400Z-US-0123","sprint_id":"S0123","story_id":"US-0123"}`

## Stop condition

STOP after /verify-work loop-2. Hand off via artifacts only to `/release` in fresh release subagent per BUG-0006. Do not spawn `/release` from this qa subagent. Do not mark US-0123 DONE.
