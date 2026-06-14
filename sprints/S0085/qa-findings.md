# QA Findings — S0085 / BUG-0012

## Metadata

- **sprint_id**: S0085
- **bug_id**: BUG-0012
- **dec_id**: DEC-0081 (amends DEC-0080 enforcement layer; composes on DEC-0078, BUG-0006, DEC-0069)
- **research_anchor**: R-0083
- **role**: qa
- **timestamp**: 2026-06-12T23:45:00Z
- **orchestrator_run_id**: auto-20260612-01
- **fresh_context_marker**: qa-S0085-BUG0012-qa-20260612T234500Z-fresh
- **inputs_reviewed**: `handoffs/dev_to_qa.md`, `sprints/S0085/tasks.md`, `sprints/S0085/summary.md`, `sprints/S0085/plan-verify.json`, `docs/product/backlog.md` `### BUG-0012`, `decisions/DEC-0081.md`, `.cursor/commands/auto.md`, `docs/engineering/auto-orchestration-reference.md`, `docs/engineering/runbook.md`, `handoffs/resume_brief.md`, `tests/auto_command_contract_test.py`, `scripts/check_intake_template_parity.py`.

## Overall verdict

**PASS** — All 8 ACs (AC-1..AC-8) satisfied on independent QA re-run; five `test_bug0012_*` contract subtests green (20 subtests); seven `test_us0095_*` regression subtests green (30 subtests); template parity `--scope=bug-0012` OK; bug validator OK; DEC-0081 required literals present; forbidden-prose negative grep green; runbook § **BUG-0012 regression verify** 6-step recipe present; spawn-only (**BUG-0006**) and **DEC-0078** hard gates preserved. Bug **BUG-0012** remains **OPEN** per **US-0045** (closure at `/release`).

- `ac_coverage`: AC-1..AC-8 = 8/8 PASS
- `regressions_found`: **none attributable to BUG-0012**
- `parity_verified`: true (`check_intake_template_parity.py --scope=bug-0012` → `[INTAKE_TEMPLATE_PARITY_OK]`)
- `bug_validator`: `[BUG_VALIDATION_OK]`
- `decision_gate_posture`: none required
- `blocking_findings`: **none**

## Test plan

| Step | Command / check | Expected | Result |
|------|-----------------|----------|--------|
| 1 | `pytest -k bug0012 tests/auto_command_contract_test.py -v` | 5 passed | **PASS** (5 passed, 20 subtests) |
| 2 | `pytest -k us0095 tests/auto_command_contract_test.py -v` | 7 passed | **PASS** (7 passed, 30 subtests) |
| 3 | `python scripts/check_intake_template_parity.py --scope=bug-0012` | `[INTAKE_TEMPLATE_PARITY_OK]` | **PASS** |
| 4 | `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` | `[BUG_VALIDATION_OK]` | **PASS** |
| 5 | Manual: `auto.md` orchestrator mandate § | Required literals + actor distinction table | **PASS** |
| 6 | Manual: native-chain precedence | `native chain supersedes Option B`; Option B scoped to `NATIVE_CHAIN_UNAVAILABLE` | **PASS** |
| 7 | Manual: drain-advance step 6→7 | No operator stop; `drain_advance_action` enum documented | **PASS** |
| 8 | Manual: continuation breadcrumbs | `native_chain_continuing` distinct from `native_chain_active` | **PASS** |
| 9 | Manual: forbidden-prose negative grep | No mandatory re-`/auto`/outer-driver in IDE-primary normative blocks | **PASS** |
| 10 | Manual: `resume_brief` spawn pairing | orchestrator **MUST Task-spawn** — not operator re-`/auto` | **PASS** |
| 11 | Manual: runbook § **BUG-0012 regression verify** | 6-step recipe + evidence fields | **PASS** |
| 12 | Scope guard: `scripts/auto_outer_driver.py` exists | file retained (optional fallback) | **PASS** |
| 13 | Scope guard: `test_us0095_*` bodies unchanged | no regression in assertion bodies | **PASS** |

## Per-AC verdicts (AC-1..AC-8)

### AC-1 — Orchestrator **MUST Task-spawn** mandate + actor distinction — `verdict=PASS`

- **Task**: T-001
- **evidence_ref**: `.cursor/commands/auto.md` § **Orchestrator post-subagent continuation mandate (BUG-0012 / DEC-0081)** — literals `orchestrator MUST Task-spawn`, `post-subagent continuation`, `phase-role stop is not run terminal`; actor distinction table (phase-role stops vs orchestrator continues). `test_bug0012_orchestrator_post_subagent_spawn_mandate` green.

### AC-2 — Native chain precedence over US-0088 Option B — `verdict=PASS`

- **Task**: T-002
- **evidence_ref**: `native chain supersedes Option B` in `auto.md` + reference; US-0088 matrix / Steps item 5 scoped to **`NATIVE_CHAIN_UNAVAILABLE`** / headless fallback. `test_bug0012_native_chain_precedence_over_option_b` green.

### AC-3 — Drain-advance step 7 no-stop between steps 6–7 — `verdict=PASS`

- **Task**: T-003
- **evidence_ref**: Step 6→7 documented as immediate spawn with no operator stop; forbidden segment-exhausted terminal when continuation pending. `test_bug0012_drain_advance_step7_no_stop_between_6_and_7` green.

### AC-4 — Continuation-truth breadcrumbs — `verdict=PASS`

- **Task**: T-003, T-004
- **evidence_ref**: `native_chain_continuing` and `drain_advance_action=spawned|skipped|not_applicable` documented in `auto.md` + reference; invalid `skipped` when budget > 0 + OPEN item stated. Continuation invariant: `native_chain_continuing=true` ⇒ no segment-exhausted stop.

### AC-5 — Four **`test_bug0012_*`** contract subtests green — `verdict=PASS`

- **Task**: T-005
- **evidence_ref**: Five `test_bug0012_*` functions present (incl. `test_bug0012_architecture_dec_linkage`); `pytest -k bug0012` → **5 passed**, 20 subtests.

### AC-6 — Forbidden-prose negative grep — `verdict=PASS`

- **Task**: T-006
- **evidence_ref**: `test_bug0012_forbidden_drain_stop_prose_negative_grep` green; no mandatory re-`/auto`/outer-driver in IDE-primary `full_autonomy` normative blocks; **DEC-0078** hard-gate vocabulary unchanged.

### AC-7 — **`resume_brief`** orchestrator spawn wording — `verdict=PASS`

- **Task**: T-004
- **evidence_ref**: `handoffs/resume_brief.md` top pointer — orchestrator **MUST Task-spawn** next phase; **`/auto`** is orchestrator context label, not operator re-invocation instruction (**DEC-0069** pairing).

### AC-8 — Runbook multi-segment E2E + template parity — `verdict=PASS`

- **Task**: T-007, T-008
- **evidence_ref**: Runbook § **BUG-0012 regression verify** — 6-step operator recipe with evidence fields (`drain_advance_action=spawned`, `native_chain_continuing=true`, `resume_brief` `story_id` advance). `check_intake_template_parity.py --scope=bug-0012` → `[INTAKE_TEMPLATE_PARITY_OK]`; `test_bug0012_architecture_dec_linkage` confirms **DEC-0081** + **R-0083** + amends **DEC-0080**.

## Runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260612-01`
- `runtime_proof_id=rp-auto-20260612-01-qa-qa-20260612T234500Z-S0085-BUG0012`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-06-12T23:45:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=0fd090c5d3ed8dca98253bbeeddef287c252d140e2b1c56047247ede5bc2b78f`
- `fresh_context_marker=qa-S0085-BUG0012-qa-20260612T234500Z-fresh`
- Linkage to prior execute proof `rp-auto-20260612-01-execute-dev-20260612T233000Z-S0085-BUG0012` / `proof_hash=653c77de89db574bc30ac8bde19bba268724aed19aa6cf2cd568213374faf15d` via shared `orchestrator_run_id`, `bug_id`, `sprint_id`.

Canonical payload: `{"orchestrator_run_id":"auto-20260612-01","phase_id":"qa","proof_issued_at":"2026-06-12T23:45:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260612-01-qa-qa-20260612T234500Z-S0085-BUG0012"}`.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0085-BUG0012-qa-20260612T234500Z-fresh`
- `timestamp=2026-06-12T23:45:00Z`
- `evidence_ref=sprints/S0085/qa-findings.md,handoffs/qa_to_verify_work.md,handoffs/dev_to_qa.md,handoffs/resume_brief.md,docs/engineering/state.md,sprints/S0085/uat.json,sprints/S0085/uat.md,docs/product/backlog.md`

## Next phase

- **`/verify-work`** (fresh **qa**) for **`S0085`** / **`BUG-0012`**.
