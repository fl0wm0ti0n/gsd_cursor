# Sprint S0122 — Verify-Work Findings (US-0122) — loop 2

**sprint_id**: S0122
**story_refs**: US-0122
**phase**: verify-work (loop 2; fresh qa subagent per BUG-0006)
**role**: qa
**orchestrator_run_id**: auto-20260824-01
**delivery_mode**: ultra_lean
**macro_phase**: build+verify
**fresh_context_marker**: `qa-US0122-verify-work-20260824T131600Z-fresh`
**timestamp**: 2026-08-24T13:16:00Z (UTC)
**model_id**: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required on isolation)
**producer_model_id**: composer-2.5-fast (sovereign-critic)
**producer_runtime_proof_id**: rp-auto-20260824-01-qa-qa-loop2-20260824T131000Z-US-0122
**producer_proof_hash**: 94B1960081A51EF41401934B5D3A386DB8C90EFADCF0149C60695DAC7A33F143
**producer_proof_ttl**: 2026-08-24T14:10:00Z (consumed before expiry — OK)
**verdict**: **PASS**

---

## Live re-verification (this verify-work loop-2 run — no rubber-stamp)

### 1. Contract gate — 8/8 PASS (independent re-run)

Command: `python -m pytest tests/us0122_contract_test.py -v`

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: G:\workdir\github\sonstiges\gsd_cursor
collecting ... collected 8 items

tests/us0122_contract_test.py::test_us0122_agent_inventory PASSED        [ 12%]
tests/us0122_contract_test.py::test_us0122_po_permission_object_form PASSED [ 25%]
tests/us0122_contract_test.py::test_us0122_po_production_code_denial PASSED [ 37%]
tests/us0122_contract_test.py::test_us0122_auto_task_allowlist PASSED    [ 50%]
tests/us0122_contract_test.py::test_us0122_security_edit_denied PASSED   [ 62%]
tests/us0122_contract_test.py::test_us0122_no_vendor_slugs_in_template PASSED [ 75%]
tests/us0122_contract_test.py::test_us0122_prompt_size_clone_guard PASSED [ 87%]
tests/us0122_contract_test.py::test_us0122_role_id_parity PASSED         [100%]

============================== 8 passed in 0.03s ==============================
```

Exit code: 0. **8/8 PASS** — independent verify-work loop-2 re-run confirms producer + QA + sovereign-critic claims. No `[FAIL]` lines.

### 2. Parity gate — PASS

Command: `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter`

Output: `[INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter`

Exit code: 0.

### 3. Full-harness report — claimed (read-only verification)

`tests/report.md` L1–L5:

```
# its-magic Test Report

Timestamp: 2026-08-24T13:02:49Z
Pass: 845
Fail: 0
```

- Literal `Fail: 0` at L5 — PASS.
- `rg "\[FAIL\]" tests/report.md` — **0 matches** (no `[FAIL]` rows).
- Timestamp `2026-08-24T13:02:49Z` matches the execute loop-2 producer report referenced in the orchestrator brief. Fresh and consistent.
- No full-harness re-run performed (report not missing, not contradicting; per orchestrator brief).

### 4. Acceptance row — read-only, unchecked

`docs/product/acceptance.md` L150: `- [ ] US-0122: OpenCode role agents and Layer-1 permission table ...` — remains unchecked. US-0122 NOT marked DONE. Backlog/acceptance NOT mutated by verify-work.

### 5. Compose guards 5/5 UNCHANGED — read-only

| Compose target | Surface | verify-work mutation? |
|----------------|---------|------------------------|
| US-0003 | role identifiers in `template/.opencode/agents/*.md` stems | read-only — none |
| US-0023 / BUG-0006 | `auto` Task-spawns role agents (no same-session roleplay) | read-only — none |
| US-0121 | `template/.opencode/**` pack path; no repo-root `opencode.json` | read-only — none |
| US-0102 / DEC-0087 | no vendor slugs in `template/.opencode/agents/*.md` | read-only — none |
| US-0002 / US-0004 | do NOT port Cursor rules/skills as OpenCode enforcement | read-only — none |

---

## UAT step results (10/10 PASS — populated, not placeholder)

| Step | AC | Result | Evidence |
|------|----|--------|---------|
| UAT-1 | AC-1 | PASS | marker 1 — 8 agents present in `template/.opencode/agents/` |
| UAT-2 | AC-2 | PASS | markers 2, 4 — po object form; auto 7-role allow + `*` deny last |
| UAT-3 | AC-3 | PASS | marker 3 — deny-last + no-production-allow (static success test (c)) |
| UAT-4 | AC-4 | PASS | marker 7 — each agent ≤ 2 KiB; no clone markers |
| UAT-5 | AC-5 | PASS | markers 1, 5, 8 — US-0003 parity; security `edit: deny` |
| UAT-6 | AC-6 | PASS | runbook h2 one-liner at `docs/engineering/runbook.md` L3987 |
| UAT-7 | AC-7 | PASS | marker 6 — zero vendor slug hits |
| UAT-8 | AC-8 | PASS | 8/8 markers PASS (independent verify-work loop-2 re-run) |
| UAT-9 | AC-9 | PASS | compose 5/5 UNCHANGED + marker 8 role-id parity |
| UAT-10 | AC-10 | PASS | marker 3 — locked matrix from DEC-0122 §2 consumed by tests |

- **Total**: 10 | **Passed**: 10 | **Failed**: 0 (passed + failed = total — DEC-0009 satisfied)
- **Browser probe**: not used (pack/contract story — no web UI surface; static contract-test mapping justified per US-0092 / DEC-0078). No `UAT_PROBE_UNRESOLVED`; no `.env` read; no intake evidence mutation. No fake browser PASS.

---

## AC checklist

- [x] AC-1 — eight markdown agents present in `template/.opencode/agents/` (po, tech-lead, dev, qa, release, curator, security, auto).
- [x] AC-2 — Layer-1 permission matrix locked per DEC-0122 §2 (po object+deny-last; auto 7-role allow + `*` deny last).
- [x] AC-3 — success test (c) static: marker 3 proves PO cannot write production paths via deny-last + no-production-allow (host permission, not prose).
- [x] AC-4 — Layer-2 short prompts: each agent ≤ 2 KiB; no clone markers (marker 7).
- [x] AC-5 — US-0003 role-id parity; security `edit: deny` findings-oriented (markers 1, 5, 8).
- [x] AC-6 — runbook `## OpenCode role agents and permissions (US-0122)` h2 one-liner present.
- [x] AC-7 — no vendor slugs in `template/.opencode/agents/*.md` (marker 6 zero hits).
- [x] AC-8 — 8 contract-test markers, 8/8 PASS (verify-work loop-2 independent re-run).
- [x] AC-9 — compose 5/5 UNCHANGED (US-0003, US-0023/BUG-0006, US-0121, US-0102/DEC-0087, US-0002/US-0004).
- [x] AC-10 — locked matrix consumed by tests (marker 3 asserts po production-code denial).

---

## Blocking findings

None. All gates green; 8/8 contract tests PASS (independent re-run); parity OK; harness `Fail: 0` literal with zero `[FAIL]` rows; UAT populated 10/10 PASS; compose 5/5 UNCHANGED.

## Non-blocking observations (carried forward, not blocking)

- `ik_us0122_stale_compose_count_6_vs_5` — architecture overview 6/6 wording stale; T-anch verifies 5/5. Doc-parity slice deferred.
- `ik_us0122_sxxxx_literal_glob_runtime` — Sxxxx globs are runtime pattern placeholders. Closed at plan-verify.
- `ik_us0122_dev_template_agent_permission_escalation` — `dev` `template/**` allow could mutate agents; parity gate sufficient. Closed.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=verify-work`
- `role=qa`
- `fresh_context_marker=qa-US0122-verify-work-20260824T131600Z-fresh`
- `timestamp=2026-08-24T13:16:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required on isolation)
- `evidence_ref=sprints/S0122/verify-work-findings.md, sprints/S0122/uat.json, sprints/S0122/uat.md, handoffs/verify_to_release.md`

## Strict runtime proof (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-verify-work-qa-20260824T131600Z-US-0122`
- `proof_issued_at=2026-08-24T13:16:00Z`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-08-24T14:16:00Z` (UTC = issued_at + 3600s)
- `proof_hash=47C37682F5F8861E4A2D6F2515390D3F4ADE0EE8D5C5DEA61A552B21A979A409`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"verify-work","proof_issued_at":"2026-08-24T13:16:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-01-verify-work-qa-20260824T131600Z-US-0122","sprint_id":"S0122","story_id":"US-0122"}`

## Next phase

`/release` (role=release, fresh subagent per BUG-0006). STOP — do not spawn /release from this verify-work subagent.
