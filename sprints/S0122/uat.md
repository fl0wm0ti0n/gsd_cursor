# Sprint S0122 — UAT (US-0122, code story) — Verify-Work loop-2 live results

**sprint_id**: S0122
**story_refs**: US-0122
**phase**: verify-work (loop 2; fresh qa subagent per BUG-0006)
**role**: qa
**orchestrator_run_id**: auto-20260824-01
**delivery_mode**: ultra_lean
**macro_phase**: build+verify
**story_type**: code
**fresh_context_marker**: `qa-US0122-verify-work-20260824T131600Z-fresh`
**timestamp**: 2026-08-24T13:16:00Z (UTC)
**model_id**: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
**producer_model_id**: composer-2.5-fast (sovereign-critic phase)
**producer_runtime_proof_id**: rp-auto-20260824-01-qa-qa-loop2-20260824T131000Z-US-0122
**producer_proof_ttl**: 2026-08-24T14:10:00Z (consumed before expiry)
**verdict**: PASS
**total_steps**: 10 | **passed**: 10 | **failed**: 0 (passed + failed = total — DEC-0009 satisfied)

## Target stories + acceptance criteria (live results)

- **US-0122** — OpenCode role agents and Layer-1 permission table (10 ACs)
  - AC-1: PASS — 8 markdown agents present (marker 1).
  - AC-2: PASS — Layer-1 permission matrix locked (markers 2, 4).
  - AC-3: PASS — success test (c) static (marker 3).
  - AC-4: PASS — Layer-2 short prompts + clone guard (marker 7).
  - AC-5: PASS — US-0003 role-id parity + security findings-oriented (markers 1, 5, 8).
  - AC-6: PASS — runbook h2 one-liner at `docs/engineering/runbook.md` L3987.
  - AC-7: PASS — no vendor slugs (marker 6).
  - AC-8: PASS — 8/8 contract markers PASS (verify-work loop-2 independent re-run).
  - AC-9: PASS — compose 5/5 UNCHANGED.
  - AC-10: PASS — locked matrix consumed by tests (marker 3).

## Contract test markers (8) — PASS (verify-work loop-2 independent re-run)

`python -m pytest tests/us0122_contract_test.py -v` — verify-work loop-2 re-run: **8 passed in 0.03s**.

1. `test_us0122_agent_inventory` (AC-1, AC-5) — PASS
2. `test_us0122_po_permission_object_form` (AC-2) — PASS
3. `test_us0122_po_production_code_denial` (AC-3, AC-10) — PASS
4. `test_us0122_auto_task_allowlist` (AC-2) — PASS
5. `test_us0122_security_edit_denied` (AC-5) — PASS
6. `test_us0122_no_vendor_slugs_in_template` (AC-7) — PASS
7. `test_us0122_prompt_size_clone_guard` (AC-4) — PASS
8. `test_us0122_role_id_parity` (AC-5, AC-9) — PASS

## UAT step results

| Step | AC | Result | Evidence |
|------|----|--------|---------|
| UAT-1 | AC-1 | PASS | marker 1 — 8 agents present in `template/.opencode/agents/` |
| UAT-2 | AC-2 | PASS | markers 2, 4 — po object form; auto 7-role allow + `*` deny last |
| UAT-3 | AC-3 | PASS | marker 3 — deny-last + no-production-allow (static success test (c)) |
| UAT-4 | AC-4 | PASS | marker 7 — each agent ≤ 2 KiB; no clone markers |
| UAT-5 | AC-5 | PASS | markers 1, 5, 8 — US-0003 parity; security `edit: deny` |
| UAT-6 | AC-6 | PASS | runbook h2 one-liner at `docs/engineering/runbook.md` L3987 |
| UAT-7 | AC-7 | PASS | marker 6 — zero vendor slug hits |
| UAT-8 | AC-8 | PASS | 8/8 markers PASS (verify-work loop-2 independent re-run) |
| UAT-9 | AC-9 | PASS | compose 5/5 UNCHANGED + marker 8 role-id parity |
| UAT-10 | AC-10 | PASS | marker 3 — locked matrix from DEC-0122 §2 consumed |

## Probe results

| Probe ID | Kind | Command | Passed | Reason |
|----------|------|---------|--------|--------|
| `us0122-contract-gate` | pytest | `python -m pytest tests/us0122_contract_test.py -v` | true | `UAT_PROBE_PASS` (8/8 PASS) |
| `opencode-adapter-parity` | static | `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` | true | `UAT_PROBE_PASS` (`INTAKE_TEMPLATE_PARITY_OK`) |
| `locked-matrix-spotcheck` | static | read `template/.opencode/agents/*.md` | true | `UAT_PROBE_PASS` (8/8 match DEC-0122 §2) |
| `runbook-h2-us0122` | static | grep `docs/engineering/runbook.md` | true | `UAT_PROBE_PASS` (L3987 match) |
| `compose-guards-5-unchanged` | static | read backlog/acceptance/architecture/DEC-0122 | true | `UAT_PROBE_PASS` (5/5 UNCHANGED) |
| `byte-identical-mirrors` | static | SHA-256 compare active vs template | true | `UAT_PROBE_PASS` (3/3 identical) |
| `harness-report-fail0` | static | read `tests/report.md` L1-L5 + grep `[FAIL]` | true | `UAT_PROBE_PASS` (`Fail: 0` literal at L5; zero `[FAIL]` rows; timestamp `2026-08-24T13:02:49Z`) |

## Browser probe — not used

`UAT_BROWSER_PROBE_MODE=cursor` (default). This is a pack/contract story with no web UI surface. No `browser_smoke` step classified. Per US-0092 / DEC-0078, ACs are mapped to pytest markers as stack-profile probes with evidence (command + output). No `UAT_PROBE_UNRESOLVED` — static contract-test mapping is justified by story type. No `.env` read. No intake evidence mutation. No `UAT_PROBE_FORBIDDEN`. No fake browser PASS — `browser_probe_used=false` recorded.

## Full-harness report — claimed (read-only verification)

`tests/report.md` was read this verify-work loop-2 run. L1–L5 confirm literal `Fail: 0` at L5 with timestamp `2026-08-24T13:02:49Z`. Grep `\[FAIL\]` over `tests/report.md` returned **0 matches** — zero `[FAIL]` rows. Harness evidence is consistent with the 8/8 contract-test PASS and parity OK. No full-harness re-run performed (report not missing, not contradicting; per orchestrator brief — execute loop-2 report @ `2026-08-24T13:02:49Z` is fresh).

## Acceptance + backlog — read-only

`docs/product/acceptance.md` L150 US-0122 row remains `- [ ]` (unchecked). US-0122 NOT marked DONE. Backlog/acceptance NOT mutated by verify-work (closure owns the flip per US-0120 / DEC-0082).

## Strict runtime proof (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-verify-work-qa-20260824T131600Z-US-0122`
- `proof_issued_at=2026-08-24T13:16:00Z`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-08-24T14:16:00Z`
- `proof_hash=47C37682F5F8861E4A2D6F2515390D3F4ADE0EE8D5C5DEA61A552B21A979A409`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"verify-work","proof_issued_at":"2026-08-24T13:16:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-01-verify-work-qa-20260824T131600Z-US-0122","sprint_id":"S0122","story_id":"US-0122"}`

## Stop condition

STOP after verify-work loop-2. Hand off via artifacts only to `/release` in fresh release subagent per BUG-0006. Do not spawn `/release` from this QA subagent.
