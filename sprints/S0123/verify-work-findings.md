# Verify-work Findings — US-0123 / S0123 (loop 2 — post harness-refresh)

- **phase_id**: verify-work
- **role**: qa (fresh per BUG-0006; loop 2 after execute harness-refresh)
- **story_id**: US-0123
- **sprint_id**: S0123
- **orchestrator_run_id**: auto-20260824-01
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **AUTO_IMPLEMENTATION_LOOP**: harness-refresh gate-1 unblock (loop 2)
- **fresh_context_marker**: qa-US0123-verify-work-20260824T152400Z-fresh (NEW; distinct from prior `qa-US0123-verify-work-20260824T150100Z-fresh` and `qa-US0123-qa-20260824T145500Z-fresh`)
- **timestamp (UTC)**: 2026-08-24T15:24:00Z
- **model_id**: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required on isolation)
- **producer_model_id**: composer-2.5-fast (sovereign-critic qa-loop2 phase)
- **producer_runtime_proof_id**: rp-auto-20260824-01-qa-qa-20260824T151700Z-US-0123-loop2
- **producer_proof_hash**: 9CC32FD6A0EE8C0EDE3696E060BDBD8A8F19E914BFFBE51719E1A7B79704F107
- **producer_proof_ttl**: 2026-08-24T16:17:00Z (consumed before expiry — OK)
- **verdict**: **PASS** (10/10 ACs; 8/8 contract tests live re-run; opencode-adapter parity; opencode-catalog validator; compose 6/6 UNCHANGED; byte-identical mirrors; no fake browser PASS; **full-harness Fail:0 claim upheld — report fresh**)
- **story_status**: OPEN (not marked DONE — US-0045; closure owns the flip)
- **blocking_findings**: 0
- **non_blocking_findings**: 1 (carry-forward `ik_us0123_installer_hook_not_contract_tested`)
- **acceptance_row_unchecked**: true (`docs/product/acceptance.md` L151 — `- [ ] US-0123`; read-only)
- **next_scheduled_phase**: /release
- **next_scheduled_role**: release
- **stop_condition**: STOP after /verify-work loop-2. Hand off via artifacts only to /release. Do not spawn /release from this qa subagent. Do not mark US-0123 DONE.

## Test plan (runbook-derived; live re-run — loop 2)

| # | Check | Command | Result |
|---|-------|---------|--------|
| 1 | Contract tests (8 markers) — live re-run | `python -m pytest tests/us0123_contract_test.py -v` | **8/8 PASS** (0.20s, exit 0) |
| 2 | OpenCode adapter parity — live re-run | `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` | **PASS** (`[INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter`) |
| 3 | OpenCode catalog validator — live re-run | `python scripts/model_tier_validate.py --scope opencode-catalog --repo .` | **PASS** (`[MODEL_TIER_VALIDATION_OK]`) |
| 4 | Full-harness report fresh | read `tests/report.md` header | **PASS** — `Timestamp: 2026-08-24T15:12:17Z` / `Pass: 845` / `Fail: 0` (literal L5); matches execute harness-refresh handoff timestamp `2026-08-24T15:12:30Z` within ~13s |
| 5 | Zero `[FAIL]` rows | Grep `\[FAIL\]` over `tests/report.md` | **0 matches** |
| 6 | Acceptance row unchecked | read `docs/product/acceptance.md` L151 | `- [ ] US-0123` (not mutated) |
| 7 | Compose guards 6/6 UNCHANGED | read backlog, acceptance, architecture, DEC-0123, template agents, mirrors | **PASS** — backlog OPEN; acceptance unchecked; arch anchor; DEC-0123 Accepted; template agents no `model:`; mirrors byte-identical |

## Contract test markers (live re-run — loop 2)

`python -m pytest tests/us0123_contract_test.py -v` -> **8 passed in 0.20s** (exit 0; Python 3.12.10; pytest 9.1.1)

| # | Marker | AC | Result |
|---|--------|----|--------|
| 1 | `test_us0123_template_agents_omit_model` | AC-1, AC-3 | PASS |
| 2 | `test_us0123_no_vendor_slugs_in_template` | AC-3 | PASS |
| 3 | `test_us0123_example_catalog_placeholders_only` | AC-2, AC-3 | PASS |
| 4 | `test_us0123_example_catalog_per_role_divergence` | AC-7, AC-9 | PASS |
| 5 | `test_us0123_fail_closed_unknown_slug` | AC-4 | PASS |
| 6 | `test_us0123_materializer_no_op_when_catalog_absent` | AC-1, AC-4 | PASS |
| 7 | `test_us0123_auth_store_never_in_template_or_git` | AC-5 | PASS |
| 8 | `test_us0123_compose_cursor_unchanged` | AC-6, AC-8 | PASS |

## AC coverage (10/10)

| AC | Status | Evidence |
|----|--------|----------|
| AC-1 Resolution chain | COVERED | marker 1 + 6 (materializer no-op when absent; template omits model) |
| AC-2 Multi-provider examples | COVERED | marker 3 — 6 providers (deepseek, moonshot, zai, anthropic, openai, dashscope) >=4 required |
| AC-3 No vendor IDs in template | COVERED | markers 1, 2, 3 + grep `^model:` 0 matches |
| AC-4 Unknown slug fail-closed | COVERED | markers 5, 6 — `OPENCODE_MODEL_SLUG_UNKNOWN` + no-op when catalog absent |
| AC-5 Auth store | COVERED | marker 7 — auth.json/api_key/sk- never in template or git |
| AC-6 Compose US-0101/US-0102 | COVERED | marker 8 — Cursor alias runtime unchanged; OpenCode additive; TOKEN_PROFILE orthogonal |
| AC-7 Per-role assignment | COVERED | marker 4 — >=2 roles configurable to different providers |
| AC-8 Contract tests | COVERED | 8/8 PASS live re-run; markers cover placeholder-only, fail-closed, schema, non-substitution |
| AC-9 Chinese APIs as capability | COVERED | marker 4 — deepseek/moonshot/zai/dashscope present; kit-operated proxy out of scope |
| AC-10 Tool-calling quality | COVERED | runbook h2 one-liner `## OpenCode model slug routing (US-0123)` present + byte-identical mirror |

## UAT probes (DEC-0009 / US-0092 / DEC-0078)

`UAT_BROWSER_PROBE_MODE=cursor` (default). Pack/contract story — no web UI surface. No `browser_smoke` step classified. ACs mapped to pytest markers + static checks as stack-profile probes. No `.env` read. No intake evidence mutation. No `UAT_PROBE_FORBIDDEN`. **No fake browser PASS** — `browser_probe_used=false` recorded in `sprints/S0123/uat.json`.

| Probe ID | Kind | Command | Passed | Reason |
|----------|------|---------|--------|--------|
| `us0123-contract-gate` | pytest | `python -m pytest tests/us0123_contract_test.py -v` | true | 8/8 PASS exit 0 (0.20s) |
| `opencode-adapter-parity` | static | `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` | true | `[INTAKE_TEMPLATE_PARITY_OK]` |
| `opencode-catalog-validator` | static | `python scripts/model_tier_validate.py --scope opencode-catalog --repo .` | true | `[MODEL_TIER_VALIDATION_OK]` |
| `harness-report-fresh` | static | read `tests/report.md` header timestamp | true | report @ 2026-08-24T15:12:17Z matches execute harness-refresh handoff @ 2026-08-24T15:12:30Z (fresh) |
| `harness-zero-fail-rows` | static | Grep `\[FAIL\]` over `tests/report.md` | true | 0 matches (zero `[FAIL]` rows) |
| `compose-guards-6-unchanged` | static | read backlog/acceptance/architecture/DEC-0123/template agents/mirrors | true | backlog OPEN; acceptance unchecked; arch anchor; DEC-0123 Accepted; 0 `^model:`; mirrors byte-identical |
| `acceptance-row-unchecked` | static | read acceptance L151 + backlog US-0123 row | true | US-0123 NOT marked DONE; QA did not mutate backlog/acceptance |

## Full-harness claim — UPHELD (fresh report, loop 2)

`tests/report.md` header: `Timestamp: 2026-08-24T15:12:17Z` / `Pass: 845` / `Fail: 0`. The report timestamp **matches** the execute harness-refresh handoff timestamp (`2026-08-24T15:12:30Z`) within ~13s — report is FRESH. Grep `\[FAIL\]` over `tests/report.md` returned **0 matches** (zero `[FAIL]` rows). Per QA PASS-claim rule, the full-harness `Fail: 0` claim is **UPHELD** for US-0123 loop-2.

`release_harness_refresh_required` flag from loop-1 is now **satisfied** — release gate-1 may consume the fresh `tests/report.md` directly without another refresh.

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

- `ik_us0123_installer_hook_not_contract_tested` (carry-forward): installer `--host opencode|both` hook not pytest-marked. Non-blocking — T-003 hook covered by installer parity + manual spot-check.

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=verify-work`
- `role=qa`
- `story_id=US-0123`
- `sprint_id=S0123`
- `fresh_context_marker=qa-US0123-verify-work-20260824T152400Z-fresh` (NEW; not reused)
- `timestamp=2026-08-24T15:24:00Z` (UTC)
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required on isolation; **NEW** fresh_context_marker per US-0048 — marker reuse = stale isolation evidence)
- `evidence_ref=sprints/S0123/verify-work-findings.md + sprints/S0123/uat.json + sprints/S0123/uat.md + handoffs/verify_to_release.md + docs/engineering/state.md (verify-work loop-2 checkpoint append-bottom)`
- QA verify-work subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward; no subagent spawned from this QA subagent.

## Strict runtime proof tuple (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-verify-work-qa-20260824T152400Z-US-0123`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"verify-work","proof_issued_at":"2026-08-24T15:24:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-01-verify-work-qa-20260824T152400Z-US-0123","sprint_id":"S0123","story_id":"US-0123"}`
- `proof_hash=5DBDB6549E0E7841974CE7A8D8FE81889AB7ADD0ED79F8FA10AF4C4CD7CA3BE8`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-08-24T16:24:00Z` (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

## Stop condition

STOP after /verify-work loop-2. Hand off via artifacts only to `/release` in fresh release subagent per BUG-0006. Do not spawn `/release` from this qa subagent. Do not mark US-0123 DONE.
