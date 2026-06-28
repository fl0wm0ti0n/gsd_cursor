# Sprint S0107 — Tasks (US-0107)

**sprint_id**: S0107  
**story_refs**: US-0107  
**dec_ref**: DEC-0107 (binding; composes US-0088, US-0092, US-0095, US-0044, US-0103, US-0105, US-0110 — do not amend)  
**task_count**: 12  
**within_limit**: true (12 ≤ `SPRINT_MAX_TASKS=12`)  
**coverage**: AC-1..AC-8 surjective via T-001..T-012 (8 ACs, 12 tasks; multi-AC tasks T-002, T-004, T-009, T-012)

---

## Task-to-AC Bijection Table (canonical)

| Task ID | Coverage | ACs Satisfied |
|---------|----------|---------------|
| T-001 | Scratchpad keys `AUTO_SOVEREIGN_*` + `SOVEREIGN_NOTIFY_*` (active + template) | AC-1 |
| T-002 | Scratchpad comment block + 12 reason codes in `reason_codes.md` § US-0107 + `DEC-0107` template mirror | AC-1, AC-8 |
| T-003 | Bootstrap `handoffs/sovereign_deferrals/.gitkeep` + sidecar `sovereign_loop_state.json` v1 contract + template mirrors | AC-2 |
| T-004 | `sovereign_loop_lib.py` deferral CRUD + `list_open_deferrals` + `schema_check_deferral` + secret scan + self-test core | AC-2, AC-3 |
| T-005 | `sovereign_loop_lib.py` `advance_sovereign_loop` + `SovereignLoopStepResult` bodies | AC-3 |
| T-006 | `sovereign_loop_validate.py` CLI + template mirror | AC-2, AC-7 |
| T-007 | Drain-generate: `build_drain_generate_spawn_inputs` + bundle schema + `/auto` PO spawn + decision gate wiring | AC-4 |
| T-008 | `dispatch_notification` ntfy/hook adapters (fail-open; email defer stub) | AC-5 |
| T-009 | US-0110 `zero_deferrals` compose via `list_open_deferrals()` (no DEC-0110 amend) | AC-3, AC-6 |
| T-010 | Eight `test_us0107_*` + compose guards in `tests/us0107_contract_test.py` | AC-7, AC-8 |
| T-011 | `SOVEREIGN_LOOP_PAIRS` parity `--scope=sovereign-loop` registration | AC-7 |
| T-012 | Runbook § Sovereign Loop Mode + US-0109 `DEPLOY_DEFERRED` integration declaration | AC-6, AC-8 |

**Total**: 12 tasks covering 8 ACs (surjective)

### AC → Task reverse map

| AC | Tasks |
|----|-------|
| AC-1 | T-001, T-002 |
| AC-2 | T-003, T-004, T-006 |
| AC-3 | T-004, T-005, T-009 |
| AC-4 | T-007 |
| AC-5 | T-008 |
| AC-6 | T-009, T-012 |
| AC-7 | T-006, T-010, T-011 |
| AC-8 | T-002, T-010, T-012 (+ architecture pre-satisfied) |

---

## Task Seeds

### T-001: Scratchpad keys `AUTO_SOVEREIGN_*` + `SOVEREIGN_NOTIFY_*`

**Coverage**: AC-1  
**Risk**: LOW  
**Dependencies**: None  
**Tranche**: A  
**Scope**:
- Add keys to `.cursor/scratchpad.md` and `template/.cursor/scratchpad.md` (byte-parity per US-0017):
  - `AUTO_SOVEREIGN` ∈ {`0`, `1`}, default `0`
  - `AUTO_SOVEREIGN_DEFERRAL_MAX` (int ≥ 1, default `50`)
  - `AUTO_SOVEREIGN_DRAIN_GENERATE_MAX` (int ≥ 0, default `3`)
  - `AUTO_SOVEREIGN_DEFERRAL_POLICY` ∈ {`stop`, `skip`, `resolve_first`}, default `resolve_first`
  - `SOVEREIGN_NOTIFY_TARGET` ∈ {`off`, `ntfy`, `email`, `hook`}, default `off`
  - `SOVEREIGN_NOTIFY_NTFY_TOPIC` (string, default empty — local-only)
  - `SOVEREIGN_NOTIFY_NTFY_BASE` (URL, default empty — local-only)
  - `SOVEREIGN_NOTIFY_HOOK_URL` (URL, default empty — local-only)
  - `SOVEREIGN_NOTIFY_EMAIL_TO` (email, default empty — email v1 deferred)

**Exit criteria**:
- Both scratchpad files contain all nine keys with correct defaults
- `test_us0107_scratchpad_keys_literals` passes (after T-010)

---

### T-002: Scratchpad comment block + reason codes § US-0107 + DEC-0107 template mirror

**Coverage**: AC-1, AC-8  
**Risk**: LOW  
**Dependencies**: T-001  
**Tranche**: A  
**Scope**:
- Add `## Sovereign Loop Mode (US-0107 / DEC-0107)` comment block to scratchpad (active + template) documenting default-off, goal-mode coupling (`SOVEREIGN_GOAL_MODE=goal_convergence` required when `AUTO_SOVEREIGN=1`), deferral policy, notification targets, and compose rules
- Ensure 12 reason codes in `docs/engineering/reason_codes.md` § US-0107 per DEC-0107 §9:
  - `SOVEREIGN_LOOP_DISABLED`, `SOVEREIGN_LOOP_GOAL_MODE_REQUIRED`, `SOVEREIGN_DEFERRAL_CAP_EXCEEDED`, `SOVEREIGN_DEFERRAL_SCHEMA_INVALID`, `SOVEREIGN_DEFERRAL_APPEND_FAILED`, `SOVEREIGN_DRAIN_GENERATE_CAP`, `SOVEREIGN_DRAIN_GENERATE_BLOCKED`, `SOVEREIGN_NOTIFY_DISPATCH_FAILED`, `SOVEREIGN_NOTIFY_TARGET_INVALID`, `SOVEREIGN_NOTIFY_CONFIG_MISSING`, `SOVEREIGN_LOOP_ADVANCE_BLOCKED`, `DEPLOY_DEFERRED`
- Ensure `template/decisions/DEC-0107.md` byte-parity with `decisions/DEC-0107.md`

**Exit criteria**:
- Comment block present in both scratchpad files
- All 12 codes documented with blocking? column and surface
- `test_us0107_scratchpad_keys_literals` passes (after T-010)

---

### T-003: Bootstrap deferrals directory + sidecar state contract

**Coverage**: AC-2  
**Risk**: LOW  
**Dependencies**: T-001  
**Tranche**: A  
**Scope**:
- Create `handoffs/sovereign_deferrals/.gitkeep` (+ template mirror)
- Document sidecar `handoffs/sovereign_loop_state.json` v1 schema (per-run drain-generate iteration counter keyed by `orchestrator_run_id`)
- Create-on-first-write policy for `handoffs/sovereign_deferrals.jsonl` — no empty tracked JSONL seed

**Exit criteria**:
- Active + template `.gitkeep` trees present
- Sidecar schema documented in lib (T-004) and architecture cross-ref
- `test_us0107_deferral_jsonl_schema_contract` passes (after T-010)

---

### T-004: `sovereign_loop_lib.py` deferral CRUD + `list_open_deferrals` + self-test core

**Coverage**: AC-2, AC-3  
**Risk**: HIGH  
**Dependencies**: T-001, T-003  
**Tranche**: B  
**Scope**:
- Finalize `scripts/sovereign_loop_lib.py` (+ template mirror) deferral core from research stub:
  - `is_sovereign_loop_enabled(scratchpad)` — requires `AUTO_SOVEREIGN=1` AND `SOVEREIGN_GOAL_MODE=goal_convergence`
  - `resolve_deferrals_path(repo_root)` — canonical path
  - `schema_check_deferral(entry)` — v1 validation + secret scan
  - `list_open_deferrals(repo, *, scratchpad)` — latest-state-wins open rows
  - `append_deferral(...)` / `resolve_deferral(deferral_id)` — append-only CRUD; cap at `AUTO_SOVEREIGN_DEFERRAL_MAX`
  - `count_drain_generate_iterations(repo, orchestrator_run_id)` — sidecar counter
  - `self_test()` → `[SOVEREIGN_LOOP_SELF_TEST_OK]`

**Exit criteria**:
- `python scripts/sovereign_loop_lib.py --self-test` exit 0 with success literal
- Template mirror byte-identical
- Round-trip append/resolve/list on temp fixtures
- `test_us0107_deferral_jsonl_schema_contract`, `test_us0107_goal_mode_coupling_fail_closed`, `test_us0107_zero_overhead_default` pass (after T-010)

---

### T-005: `advance_sovereign_loop` + `SovereignLoopStepResult` bodies

**Coverage**: AC-3  
**Risk**: HIGH  
**Dependencies**: T-004  
**Tranche**: C  
**Scope**:
- Implement `advance_sovereign_loop(repo, scratchpad, *, orchestrator_run_id) -> SovereignLoopStepResult` per DEC-0107 §5 pseudocode:
  1. Disabled → `noop`
  2. Goal mode mismatch → `blocked` + `SOVEREIGN_LOOP_GOAL_MODE_REQUIRED`
  3. `evaluate_convergence(...)` via US-0110 import
  4. Converged → `terminal_converged` + notification hook
  5. Timeout → `terminal_timeout` + partial-delivery report
  6. Deferral policy gate (`stop` / `skip` / `resolve_first`)
  7. OPEN stories remain → `continue`
  8. Zero OPEN + not converged + under cap → `drain_generate`
  9. Caps exhausted → sovereign terminal + notification
- **`SovereignLoopStepResult` v1**: `action` ∈ {`noop`, `continue`, `defer`, `drain_generate`, `terminal_converged`, `terminal_timeout`, `terminal_cap`, `blocked`}; optional fields per architecture

**Exit criteria**:
- Advance branches covered on temp fixtures for each policy mode
- `test_us0107_advance_deferral_policy_literals` passes (after T-010)
- Sovereign terminal stops additive — do not replace native stop matrix

---

### T-006: `sovereign_loop_validate.py` CLI + template mirror

**Coverage**: AC-2, AC-7  
**Risk**: HIGH  
**Dependencies**: T-004  
**Tranche**: C  
**Scope**:
- Create `scripts/sovereign_loop_validate.py` (+ template mirror):
  - `--file <path>` — validate single deferral JSONL file
  - `--repo <root>` — validate deferrals if present
  - `--self-test` — library contract self-test
  - `--enforce` — non-zero exit on fail-closed code
- Success literal: `[SOVEREIGN_LOOP_VALIDATION_OK]`
- Exit codes 0/1/2 mirror DEC-0103 / DEC-0105 pattern

**Exit criteria**:
- `python scripts/sovereign_loop_validate.py --self-test` exit 0
- `--enforce` returns exit 1 on invalid fixture
- Template mirror byte-identical

---

### T-007: Drain-generate PO spawn + decision gate wiring

**Coverage**: AC-4  
**Risk**: HIGH  
**Dependencies**: T-005  
**Tranche**: D  
**Scope**:
- Implement `build_drain_generate_spawn_inputs(...)` in `sovereign_loop_lib.py` (+ template mirror)
- **`DrainGenerateCandidateBundle` v1**: max 3 candidates/iteration; fields per architecture
- Wire `/auto` orchestrator: spawn fresh **PO** subagent (spawn-only **US-0095**); ephemeral id `drain-gen-{orchestrator_run_id}-{iteration}`
- PO inputs: vision narrow-read; optional `sovereign_memory_digest` when `SOVEREIGN_MEMORY=1`; convergence `unmet_conditions[]`, `blocked_by[]`, `goal_text`
- **Decision gate (mandatory per candidate)**: accept → `/intake` or backlog append; reject → discard; no auto-append

**Exit criteria**:
- Bundle schema validated; 3-candidate cap enforced
- Decision gate prose locked in `/auto` orchestrator model
- `test_us0107_drain_generate_gate_contract` passes (after T-010)

---

### T-008: `dispatch_notification` ntfy/hook adapters

**Coverage**: AC-5  
**Risk**: MEDIUM  
**Dependencies**: T-005  
**Tranche**: D  
**Scope**:
- Implement `dispatch_notification(scratchpad, event_type, payload)` in `sovereign_loop_lib.py` (+ template mirror)
- **Events**: `convergence`, `timeout`, `deferral_cap`, `drain_generate_cap`
- **Adapters v1**: ntfy (stdlib urllib POST); hook (JSON POST); email **deferred** stub returning `SOVEREIGN_NOTIFY_TARGET_INVALID`
- **Fail-open**: adapter errors log `SOVEREIGN_NOTIFY_DISPATCH_FAILED`; loop continues
- **Secrets**: topic/URL values local-only; never in git-tracked artifacts

**Exit criteria**:
- Fail-open behavior on adapter errors (mock/temp fixtures)
- `test_us0107_notification_fail_open_literals` passes (after T-010)
- `SOVEREIGN_NOTIFY_TARGET=off` → zero overhead path

---

### T-009: US-0110 `zero_deferrals` compose via `list_open_deferrals()`

**Coverage**: AC-3, AC-6  
**Risk**: MEDIUM  
**Dependencies**: T-004  
**Tranche**: D  
**Scope**:
- Wire **US-0110** convergence predicate to import `list_open_deferrals()` from `sovereign_loop_lib` for `zero_deferrals` conjunct
- **Do not amend** `DEC-0110` or `sovereign_convergence_lib.py` five-conjunct predicate — additive import only
- Document **US-0109** integration: `DEPLOY_DEFERRED` rows (`work_item_kind=deploy`) on deploy smoke cap exhaustion — schema stable in US-0107; no deploy smoke logic

**Exit criteria**:
- Convergence reads open deferrals when sovereign enabled; skip when `AUTO_SOVEREIGN=0`
- `test_us0107_us0110_convergence_import_contract` passes (after T-010)
- US-0109 integration contract documented (runbook expanded in T-012)

---

### T-010: Eight `test_us0107_*` + compose regression guards

**Coverage**: AC-7, AC-8  
**Risk**: HIGH  
**Dependencies**: T-004..T-009  
**Tranche**: E  
**Scope**:
- Create `tests/us0107_contract_test.py` with eight markers per DEC-0107 §12:
  1. `test_us0107_scratchpad_keys_literals`
  2. `test_us0107_deferral_jsonl_schema_contract`
  3. `test_us0107_advance_deferral_policy_literals`
  4. `test_us0107_drain_generate_gate_contract`
  5. `test_us0107_notification_fail_open_literals`
  6. `test_us0107_goal_mode_coupling_fail_closed`
  7. `test_us0107_zero_overhead_default`
  8. `test_us0107_compose_no_stop_matrix_change`
- Compose regression guards:
  - `test_us0107_us0110_convergence_import_contract`
  - `test_us0107_us0095_spawn_only_regression_guard`

**Exit criteria**:
- `pytest -k us0107` → 8/8 core markers + 2 compose guards PASS
- Tests are deterministic (no network; temp dirs for fixtures)

---

### T-011: `SOVEREIGN_LOOP_PAIRS` parity registration

**Coverage**: AC-7  
**Risk**: MEDIUM  
**Dependencies**: T-006  
**Tranche**: E  
**Scope**:
- Register `SOVEREIGN_LOOP_PAIRS` in `scripts/check_intake_template_parity.py` (+ template mirror):
  - `scripts/sovereign_loop_lib.py` ↔ `template/scripts/sovereign_loop_lib.py`
  - `scripts/sovereign_loop_validate.py` ↔ `template/scripts/sovereign_loop_validate.py`
  - `.cursor/scratchpad.md` ↔ `template/.cursor/scratchpad.md` (`AUTO_SOVEREIGN_*` + `SOVEREIGN_NOTIFY_*` block)
  - `handoffs/sovereign_deferrals/.gitkeep` ↔ `template/handoffs/sovereign_deferrals/.gitkeep`
  - `decisions/DEC-0107.md` ↔ `template/decisions/DEC-0107.md`

**Exit criteria**:
- `python scripts/check_intake_template_parity.py --scope=sovereign-loop` → `[INTAKE_TEMPLATE_PARITY_OK]`

---

### T-012: Runbook § Sovereign Loop Mode + US-0109 integration declaration

**Coverage**: AC-6, AC-8  
**Risk**: LOW  
**Dependencies**: T-002, T-009  
**Tranche**: E  
**Scope**:
- Add `### Sovereign Loop Mode (US-0107)` to `docs/engineering/runbook.md` (+ template mirror):
  - Enable/disable sovereign loop (`AUTO_SOVEREIGN` + `SOVEREIGN_GOAL_MODE=goal_convergence`)
  - Deferral register operator workflow (append/resolve/cap)
  - Drain-generate decision gate operator path
  - Notification target configuration (local-only secrets)
  - Backward compat: `AUTO_SOVEREIGN=0` zero overhead
- Document **US-0109** `DEPLOY_DEFERRED` integration contract (`work_item_kind=deploy`, schema v1 fields)

**Exit criteria**:
- Runbook section present in active + template
- Operator recipe covers enable/disable/goal-mode coupling/deferral-cap/drain-generate gate
- US-0109 integration declaration explicit (no deploy smoke in US-0107)

---

## Appendix: Task Dependencies (Visual)

```
T-001 (scratchpad keys)
    ↓
T-002 (comment block + reason codes + DEC mirror)
    ↓
T-003 (deferrals .gitkeep + sidecar contract)
    ↓
T-004 (lib deferral CRUD + list_open_deferrals + self_test)
    ↓
    ├─→ T-005 (advance_sovereign_loop + SovereignLoopStepResult)
    ├─→ T-006 (validator CLI)
    └─→ T-009 (US-0110 zero_deferrals compose)
            ↓
    T-005
            ↓
    ├─→ T-007 (drain-generate + decision gate)
    └─→ T-008 (dispatch_notification)
            ↓
        T-010 (contract tests)
            ↓
    ├─→ T-011 (parity registration)
    └─→ T-012 (runbook + US-0109 declaration)
```

**Task Execution Order**: T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 → T-008 → T-009 → T-010 → T-011 → T-012
