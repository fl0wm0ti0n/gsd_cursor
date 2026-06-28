# Sprint S0110 — Tasks (US-0110)

**sprint_id**: S0110  
**story_refs**: US-0110  
**dec_ref**: DEC-0110 (binding; composes US-0088, US-0092, US-0095, US-0044, US-0103 — do not amend)  
**task_count**: 11  
**within_limit**: true (11 ≤ `SPRINT_MAX_TASKS=12`)  
**coverage**: AC-1..AC-8 surjective via T-001..T-011 (8 ACs, 11 tasks; multi-AC tasks T-002, T-006, T-009, T-010, T-011)

---

## Task-to-AC Bijection Table (canonical)

| Task ID | Coverage | ACs Satisfied |
|---------|----------|---------------|
| T-001 | Scratchpad keys `SOVEREIGN_GOAL_*` (active + template) | AC-1 |
| T-002 | Scratchpad comment block + 10 reason codes in `reason_codes.md` § US-0110 | AC-1, AC-8 |
| T-003 | `sovereign_convergence_lib.py` schemas + `is_goal_convergence_enabled` + `schema_check_*` + `self_test` | AC-2 |
| T-004 | `evaluate_convergence` five-conjunct predicate + degrade matrix + memoization | AC-2 |
| T-005 | `resolve_goal` vision auto-derive algorithm | AC-3 |
| T-006 | `sovereign_convergence_validate.py` + template mirror | AC-2, AC-8 |
| T-007 | `build_goal_progress_block` + curator `/refresh-context` emission | AC-4 |
| T-008 | `write_partial_delivery_report` + `check_timeout` | AC-5 |
| T-009 | Eight `test_us0110_*` contract markers | AC-6 |
| T-010 | `SOVEREIGN_CONVERGENCE_PAIRS` parity scope | AC-6, AC-8 |
| T-011 | Runbook + `phase_driven` zero-overhead + compose regression | AC-7, AC-8 |

**Total**: 11 tasks covering 8 ACs (surjective)

### AC → Task reverse map

| AC | Tasks |
|----|-------|
| AC-1 | T-001, T-002 |
| AC-2 | T-003, T-004, T-006 |
| AC-3 | T-005 |
| AC-4 | T-007 |
| AC-5 | T-008 |
| AC-6 | T-009, T-010 |
| AC-7 | T-011 |
| AC-8 | T-002, T-006, T-010, T-011 (+ architecture pre-satisfied) |

---

## Task Seeds

### T-001: Scratchpad keys `SOVEREIGN_GOAL_*`

**Coverage**: AC-1  
**Risk**: LOW  
**Dependencies**: None  
**Tranche**: A  
**Scope**:
- Add five keys to `.cursor/scratchpad.md` and `template/.cursor/scratchpad.md` (byte-parity per US-0017):
  - `SOVEREIGN_GOAL_MODE` ∈ {`phase_driven`, `goal_convergence`}, default `phase_driven`
  - `SOVEREIGN_GOAL` (free-text, default empty)
  - `SOVEREIGN_GOAL_TOP_N` (int ≥ 1, default `3`)
  - `SOVEREIGN_GOAL_MAX_CHARS` (int ≥ 64, default `512`)
  - `SOVEREIGN_GOAL_TIMEOUT_MAX` (int ≥ 0, default `0` — iteration count, disabled)

**Exit criteria**:
- Both scratchpad files contain all five keys with correct defaults
- `test_us0110_scratchpad_keys_literals` passes (after T-009)

---

### T-002: Scratchpad comment block + reason codes § US-0110

**Coverage**: AC-1, AC-8  
**Risk**: LOW  
**Dependencies**: T-001  
**Tranche**: A  
**Scope**:
- Add `## Goal-Based Convergence (US-0110 / DEC-0110)` comment block to scratchpad (active + template) documenting default-off, iteration-count timeout, and compose rules
- Add 10 reason codes to `docs/engineering/reason_codes.md` § US-0110 per DEC-0110 §10:
  - `CONVERGENCE_OPEN_STORIES_REMAIN`, `CONVERGENCE_DEFERRALS_PENDING`, `CONVERGENCE_CROSS_REVIEWER_OPEN`, `CONVERGENCE_SMOKE_PROBE_FAIL`, `CONVERGENCE_LEDGER_EXTENSIONS_UNAPPROVED`
  - `SOVEREIGN_GOAL_TIMEOUT`, `SOVEREIGN_GOAL_MODE_INVALID`, `SOVEREIGN_GOAL_MISSING`, `SOVEREIGN_GOAL_DERIVE_FAILED`, `CONVERGENCE_EVAL_FAILED`

**Exit criteria**:
- Comment block present in both scratchpad files
- All 10 codes documented with `blocked_by?` column and conjunct/trigger
- `test_us0110_reason_code_inventory` passes (after T-009)

---

### T-003: `sovereign_convergence_lib.py` schemas + self_test

**Coverage**: AC-2  
**Risk**: HIGH  
**Dependencies**: T-001  
**Tranche**: B  
**Scope**:
- Finalize `scripts/sovereign_convergence_lib.py` (+ template mirror) from research stub:
  - `ConvergenceResult` v1 schema + `schema_check_convergence_result()`
  - `goal_progress` v1 schema + `schema_check_goal_progress()`
  - `is_goal_convergence_enabled(scratchpad) -> bool`
  - `clear_eval_cache()` test helper
  - `self_test()` → `[SOVEREIGN_CONVERGENCE_SELF_TEST_OK]`
  - CLI stubs: `--self-test`, `--repo`, `--orchestrator-run-id`

**Exit criteria**:
- `python scripts/sovereign_convergence_lib.py --self-test` exit 0 with success literal
- Template mirror byte-identical
- Schema validators reject malformed fixtures

---

### T-004: `evaluate_convergence` five-conjunct predicate + memoization

**Coverage**: AC-2  
**Risk**: HIGH  
**Dependencies**: T-003  
**Tranche**: B  
**Scope**:
- Implement `evaluate_convergence(repo, scratchpad, *, orchestrator_run_id=None, iteration=None) -> ConvergenceResult`
- Five conjuncts in fixed order: `backlog_clear`, `zero_deferrals`, `critic_resolved`, `smoke_green`, `ledger_clean`
- Degrade matrix per DEC-0110 §4 (skip deferrals/critic when absent; smoke fail-closed; ledger skip when `AI_DECISION_LEDGER=0`)
- Mtime memoization key: `backlog_mtime:deferral_mtime:critic_mtime:report_mtime:uat_mtime:ledger_mtime`
- Performance budget: ≤50ms p95 on line-scoped backlog scan
- CLI `--evaluate` prints JSON

**Exit criteria**:
- `test_us0110_evaluator_five_conjunct_contract` passes
- `test_us0110_phase_driven_zero_overhead` passes (mode gate before eval)
- Memoization invalidates on mtime change

---

### T-005: `resolve_goal` vision auto-derive algorithm

**Coverage**: AC-3  
**Risk**: MEDIUM  
**Dependencies**: T-003  
**Tranche**: B  
**Scope**:
- Implement `resolve_goal(scratchpad, repo) -> GoalResolveResult` with `(goal_text, goal_source, reason_code|None)`
- Explicit `SOVEREIGN_GOAL` wins over vision derive
- Vision walk: skip headings, code fences, lists, blockquotes, Discovery/Intake Notes sections
- First `SOVEREIGN_GOAL_TOP_N` eligible paragraphs; join with `" — "`; truncate to `SOVEREIGN_GOAL_MAX_CHARS` on word boundary
- `SOVEREIGN_GOAL_DERIVE_FAILED` when vision empty/unreadable

**Exit criteria**:
- `test_us0110_goal_authoring_explicit_and_derive` passes
- Explicit goal returns `goal_source=explicit`
- Empty vision returns `SOVEREIGN_GOAL_DERIVE_FAILED`

---

### T-006: `sovereign_convergence_validate.py` + template mirror

**Coverage**: AC-2, AC-8  
**Risk**: HIGH  
**Dependencies**: T-003  
**Tranche**: C  
**Scope**:
- Create `scripts/sovereign_convergence_validate.py` (+ template mirror):
  - `--convergence-json <path|->`
  - `--goal-progress-json <path|->`
  - `--repo <root>` (validate partial-delivery + resume_brief goal_progress when present)
  - `--self-test` (lib self-test + schema fixtures)
  - `--enforce` (non-zero exit on failure)
- Success literal: `[SOVEREIGN_CONVERGENCE_VALIDATION_OK]`

**Exit criteria**:
- `python scripts/sovereign_convergence_validate.py --self-test` exit 0
- `--enforce` returns exit 1 on invalid fixture
- Template mirror byte-identical

---

### T-007: `goal_progress` block + curator `/refresh-context` hook

**Coverage**: AC-4  
**Risk**: MEDIUM  
**Dependencies**: T-004, T-005  
**Tranche**: D  
**Scope**:
- Implement `build_goal_progress_block(result, goal_text, goal_source, orchestrator_run_id) -> dict`
- Wire curator `/refresh-context` to emit fenced JSON under `### goal_progress` in `handoffs/resume_brief.md`
- Placement: after latest orchestration pointer, before prior pointers
- Only when `SOVEREIGN_GOAL_MODE=goal_convergence` and sovereign loop active

**Exit criteria**:
- `test_us0110_goal_progress_block_shape` passes
- `refresh-context.md` documents emission contract (active + template)
- CLI `--dump-progress` prints valid JSON

---

### T-008: Partial delivery report + `check_timeout`

**Coverage**: AC-5  
**Risk**: MEDIUM  
**Dependencies**: T-004, T-005  
**Tranche**: D  
**Scope**:
- Implement `write_partial_delivery_report(repo, result, goal_text, timeout_reason, orchestrator_run_id) -> Path`
- Sections: Goal, Evaluated At, Unmet Conditions, Blocked By, Completed Stories, Open Stories, Deferrals Summary, Remediation
- Idempotent overwrite of `handoffs/sovereign_partial_delivery.md`
- Implement `check_timeout(scratchpad, iteration_count) -> (bool, reason_code|None)` → `SOVEREIGN_GOAL_TIMEOUT` when iteration ≥ max and max > 0

**Exit criteria**:
- `test_us0110_partial_delivery_timeout` passes
- All eight markdown sections present on timeout write
- Default `SOVEREIGN_GOAL_TIMEOUT_MAX=0` never triggers timeout

---

### T-009: Eight `test_us0110_*` contract markers

**Coverage**: AC-6  
**Risk**: HIGH  
**Dependencies**: T-004, T-005, T-006, T-007, T-008  
**Tranche**: E  
**Scope**:
- Create `tests/us0110_contract_test.py` with eight markers per DEC-0110 §8:
  1. `test_us0110_scratchpad_keys_literals`
  2. `test_us0110_evaluator_five_conjunct_contract`
  3. `test_us0110_goal_authoring_explicit_and_derive`
  4. `test_us0110_goal_progress_block_shape`
  5. `test_us0110_partial_delivery_timeout`
  6. `test_us0110_reason_code_inventory`
  7. `test_us0110_phase_driven_zero_overhead`
  8. `test_us0110_compose_no_stop_matrix_change`

**Exit criteria**:
- `pytest -k us0110` → 8/8 PASS
- Tests are deterministic (no network; temp dirs for fixtures)

---

### T-010: `SOVEREIGN_CONVERGENCE_PAIRS` parity scope

**Coverage**: AC-6, AC-8  
**Risk**: MEDIUM  
**Dependencies**: T-003, T-006  
**Tranche**: E  
**Scope**:
- Register `SOVEREIGN_CONVERGENCE_PAIRS` in `scripts/check_intake_template_parity.py` (+ template mirror):
  - `scripts/sovereign_convergence_lib.py` ↔ `template/scripts/sovereign_convergence_lib.py`
  - `scripts/sovereign_convergence_validate.py` ↔ `template/scripts/sovereign_convergence_validate.py`
- `--scope=sovereign-convergence` exits 0 on byte-match

**Exit criteria**:
- `python scripts/check_intake_template_parity.py --scope=sovereign-convergence` → `[INTAKE_TEMPLATE_PARITY_OK]`
- Parity manifest documented in architecture `# US-0110`

---

### T-011: Runbook + zero-overhead + compose regression

**Coverage**: AC-7, AC-8  
**Risk**: MEDIUM  
**Dependencies**: T-004  
**Tranche**: E  
**Scope**:
- Add `### Goal-Based Convergence (US-0110)` to `docs/engineering/runbook.md` (+ template mirror):
  - Enable `goal_convergence` mode
  - Interpret `goal_progress` block
  - Read partial-delivery report on timeout
  - Troubleshooting reason codes
- Document `phase_driven` zero-overhead path
- `test_us0110_compose_no_stop_matrix_change` verifies US-0088/US-0092/US-0095/US-0044 files unchanged

**Exit criteria**:
- Runbook section present in active + template
- `test_us0110_phase_driven_zero_overhead` + `test_us0110_compose_no_stop_matrix_change` pass
- Operator recipe covers enable/disable/timeout remediation

---

## Appendix: Task Dependencies (Visual)

```
T-001 (scratchpad keys)
    ↓
T-002 (comment block + reason codes)
    ↓
T-003 (lib schemas + self_test)
    ↓
    ├─→ T-004 (evaluate_convergence)
    ├─→ T-005 (resolve_goal)
    └─→ T-006 (validator CLI)
            ↓
    T-004 + T-005
            ↓
    ├─→ T-007 (goal_progress)
    └─→ T-008 (partial delivery)
            ↓
        T-009 (contract tests)
            ↓
        T-010 (parity)
            ↓
        T-011 (runbook + regression)
```

**Task Execution Order**: T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 → T-008 → T-009 → T-010 → T-011
