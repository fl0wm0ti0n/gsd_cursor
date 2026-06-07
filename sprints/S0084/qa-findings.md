# QA Findings — S0084 / US-0095

## Metadata

- **sprint_id**: S0084
- **story_id**: US-0095
- **governance**: **DEC-0080** + architecture `# US-0095` + **R-0081**
- **role**: qa
- **timestamp**: 2026-06-07T22:00:00Z
- **orchestrator_run_id**: auto-20260607-02
- **fresh_context_marker**: qa-S0084-US0095-qa-20260607T220000Z-fresh
- **inputs_reviewed**: `handoffs/dev_to_qa.md`, `sprints/S0084/tasks.md`, `sprints/S0084/summary.md`, `sprints/S0084/plan-verify.json`, `docs/product/backlog.md` `## US-0095`, `decisions/DEC-0080.md`, `.cursor/commands/auto.md`, `docs/engineering/auto-orchestration-reference.md`, `docs/engineering/runbook.md`, `README.md`, `tests/auto_command_contract_test.py`.

## Overall verdict

**PASS** — All 10 ACs (AC-1..AC-10) satisfied on independent QA re-run; seven `test_us0095_*` contract subtests green; template parity `--scope=us-0095` OK; native in-chat auto-chain literals present in active + template surfaces; outer driver demoted to optional/fallback without deleting US-0092 autonomy headline; spawn-only (**BUG-0006**) invariants preserved; hard stop matrix unchanged; `scripts/auto_outer_driver.py` retained. Story **US-0095** remains **OPEN** per **US-0045** (closure at `/release`).

- `ac_coverage`: AC-1..AC-10 = 10/10 PASS
- `regressions_found`: **none attributable to US-0095**
- `parity_verified`: true (`check_intake_template_parity.py --scope=us-0095` → `[INTAKE_TEMPLATE_PARITY_OK]`)
- `decision_gate_posture`: none required

## Test plan

| Step | Command / check | Expected | Result |
|------|-----------------|----------|--------|
| 1 | `pytest -k us0095 tests/auto_command_contract_test.py -v` | 7 passed | **PASS** (7 passed, 30 subtests) |
| 2 | `python scripts/check_intake_template_parity.py --scope=us-0095` | `[INTAKE_TEMPLATE_PARITY_OK]` | **PASS** |
| 3 | Manual: `auto.md` + reference native-chain § | Required literals (Native in-chat, foreground sequential, NATIVE_CHAIN_UNAVAILABLE) | **PASS** |
| 4 | Manual: drain-advance algorithm | 7-step algorithm; `drain-advance-without-pause`, `immediately`, `without operator re-`/auto`` | **PASS** |
| 5 | Manual: spawn-only invariants | BUG-0006 / US-0069 markers; no forbidden in-band patterns in native § | **PASS** |
| 6 | Manual: stop matrix hard gates | decision_gate, loop_max, security deny unchanged | **PASS** |
| 7 | Manual: README + runbook outer-driver demotion | optional/fallback labeling; native chain primary in IDE | **PASS** |
| 8 | Manual: AUTO_QUIET suppression table | forbidden mandatory outer-driver patterns documented | **PASS** |
| 9 | Manual: DEC-0069 pairing | resume_brief + state.md mandate; RESUME_BRIEF_STALE fail-closed | **PASS** |
| 10 | Manual: caps + security deny-list | unified ledger; remediation_action values; no .env auto-read | **PASS** |
| 11 | Scope guard: `scripts/auto_outer_driver.py` exists | file retained (not deleted) | **PASS** |

## Per-AC verdicts (AC-1..AC-10)

### AC-1 — Native in-chat auto-chain — `verdict=PASS`

- **Task**: T-001
- **evidence_ref**: `.cursor/commands/auto.md` § **Native in-chat auto-chain (US-0095 / DEC-0080)** — foreground sequential Task loop within same `/auto` session; orchestrator must not stop solely at turn boundaries when continuation schedulable. `docs/engineering/auto-orchestration-reference.md` § **Native in-chat auto-chain** + **reference Step 5** IDE-primary path. `test_us0095_native_in_chat_auto_chain_markers` green.

### AC-2 — Drain-without-pause (IDE) — `verdict=PASS`

- **Task**: T-002
- **evidence_ref**: 7-step **IDE drain-advance-without-pause** algorithm in `auto.md` (steps 1–7) and reference § **IDE drain-advance-without-pause algorithm**; literals `immediately`, `without operator re-`/auto``; no mandatory outer-driver prose in IDE-primary native §. `test_us0095_ide_drain_advance_without_outer_driver` green.

### AC-3 — Spawn-only preserved — `verdict=PASS`

- **Task**: T-003
- **evidence_ref**: **Loop invariants (spawn-only — BUG-0006 unchanged)** in `auto.md`; US-0069 preflight/post references; forbidden in-band patterns absent from native §. `test_us0095_spawn_only_regression` green.

### AC-4 — Stop matrix unchanged for hard gates — `verdict=PASS`

- **Task**: T-004
- **evidence_ref**: `auto.md` § stop matrix — hard stops: `decision_gate`, isolation/strict-proof violations, security deny, `BACKLOG_MAX_STORIES_REACHED`, `AUTO_LOOP_MAX_CYCLES`, unrecoverable `error`, `pause_request`; relaxable transient stops per DEC-0078 when configured. Reference stop matrix table unchanged for hard gates.

### AC-5 — Outer driver demoted to fallback — `verdict=PASS`

- **Task**: T-005
- **evidence_ref**: `README.md` intro ¶3 — `/auto` once in Cursor primary; outer driver **optional** / **fallback** for headless/CI. `runbook.md` § **Native in-chat auto-chain (US-0095)** + **Primary / fallback boundary** table; § **Full-autonomy outer driver (US-0092) — fallback**. `scripts/auto_outer_driver.py` retained. `test_us0095_outer_driver_fallback_not_mandatory_ide` green.

### AC-6 — Operator surface / AUTO_QUIET — `verdict=PASS`

- **Task**: T-006
- **evidence_ref**: `auto.md` § **`AUTO_QUIET` under native chain** — suppression table; forbidden mandatory outer-driver/re-`/auto`/segment-exhausted wait patterns; gates/caps/errors non-suppressible. `test_us0095_auto_quiet_no_outer_driver_mandatory` green.

### AC-7 — DEC-0069 pairing — `verdict=PASS`

- **Task**: T-007
- **evidence_ref**: **DEC-0069 pairing mandate** in `auto.md` native §; drain-advance step 2 ASSERT pairing; stale brief → `RESUME_BRIEF_STALE` fail-closed. `test_us0095_resume_brief_pairing_markers` green.

### AC-8 — Contract tests — `verdict=PASS`

- **Task**: T-008
- **evidence_ref**: Seven `test_us0095_*` subtests in `tests/auto_command_contract_test.py`; QA re-run `pytest -k us0095` → **7 passed**.

### AC-9 — Template parity — `verdict=PASS`

- **Task**: T-009
- **evidence_ref**: `python scripts/check_intake_template_parity.py --scope=us-0095` → `[INTAKE_TEMPLATE_PARITY_OK]`; `test_us0095_template_parity_auto_surfaces` green (active + `template/` mirrors for `auto.md`, reference, runbook).

### AC-10 — Caps + security — `verdict=PASS`

- **Task**: T-010
- **evidence_ref**: Reference § unified cap/ledger — `AUTO_LOOP_MAX_CYCLES`, `AUTO_BACKLOG_MAX_STORIES`, `AUTO_BLOCK_RETRY_MAX`; `remediation_action` values (`phase_respawn`, `native_chain_continue`, `drain_advance`); breadcrumb fields (`native_chain_active`, `outer_cycle_index`, `implementation_loop_index`); **Security deny-list** unchanged (no auto-read `.env`, no intake evidence mutation, no publish without `RELEASE_PUBLISH_MODE=auto`).

## Runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260607-02`
- `runtime_proof_id=rp-auto-20260607-02-qa-qa-20260607T220000Z-S0084-US0095`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-06-07T22:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=50d7b0b434e81342d1e8789e25e9c59bf6b51f280820cbdd639c8c2156a8682a`
- `fresh_context_marker=qa-S0084-US0095-qa-20260607T220000Z-fresh`
- Linkage to prior execute proof `rp-auto-20260607-02-execute-dev-20260607T213000Z-S0084-US0095` / `proof_hash=9cc96c189853d90cb36dc822c4ea5e2df44eabf73ecf7a319c127eb7ddff351d` via shared `orchestrator_run_id`, `story_id`, `sprint_id`.

Canonical payload: `{"dec_id":"DEC-0080","fresh_context_marker":"qa-S0084-US0095-qa-20260607T220000Z-fresh","orchestrator_run_id":"auto-20260607-02","phase":"qa","role":"qa","sprint_id":"S0084","story_id":"US-0095","timestamp":"20260607T220000Z"}`.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0084-US0095-qa-20260607T220000Z-fresh`
- `timestamp=2026-06-07T22:00:00Z`
- `evidence_ref=[sprints/S0084/qa-findings.md, handoffs/qa_to_verify_work.md, handoffs/dev_to_qa.md, handoffs/resume_brief.md, docs/engineering/state.md]`

## Next phase

- **`/verify-work`** (fresh **qa**) for **`S0084`** / **`US-0095`**.
