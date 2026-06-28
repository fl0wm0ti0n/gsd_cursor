# Sprint S0105 — Tasks (US-0105)

**sprint_id**: S0105  
**story_refs**: US-0105  
**dec_ref**: DEC-0105 (binding; composes US-0029, US-0080, US-0103, US-0072, US-0096 — do not amend)  
**task_count**: 11  
**within_limit**: true (11 ≤ `SPRINT_MAX_TASKS=12`)  
**coverage**: AC-1..AC-8 surjective via T-001..T-011 (8 ACs, 11 tasks; multi-AC tasks T-002, T-005, T-006, T-011)

---

## Task-to-AC Bijection Table (canonical)

| Task ID | Coverage | ACs Satisfied |
|---------|----------|---------------|
| T-001 | Scratchpad keys `SOVEREIGN_MEMORY_*` (active + template) | AC-1 |
| T-002 | Scratchpad comment block + 8 reason codes in `reason_codes.md` § US-0105 + `DEC-0105` template mirror | AC-1, AC-8 |
| T-003 | Directory `docs/engineering/sovereign-memory/` + `retrospectives/.gitkeep` + archive path + template mirror | AC-2 |
| T-004 | `sovereign_memory_lib.py` read/injection core: schemas, `build_injection_digest`, `read_entries`, `schema_check`, `scan_secrets`, `self_test` | AC-3 |
| T-005 | `sovereign_memory_lib.py` mutations: `append_*`, dedup, `maybe_archive_jsonl`, `promote_from_ledger`, `write_retrospective` | AC-5, AC-6 |
| T-006 | `sovereign_memory_validate.py` + template mirror | AC-2, AC-8 |
| T-007 | Phase spawn `sovereign_memory_digest` block integration (US-0023-safe additive) | AC-4 |
| T-008 | Mistake-tagging hooks: `/auto` fix-fail, `/execute` revert, fidelity compose **US-0103** | AC-6 |
| T-009 | `/refresh-context` curator retrospective + `promote_from_ledger` wiring | AC-5 |
| T-010 | Eight `test_us0105_*` + compose regression guards in `tests/us0105_contract_test.py` | AC-7, AC-8 |
| T-011 | `SOVEREIGN_MEMORY_PAIRS` parity `--scope=sovereign-memory` + runbook `### Sovereign Memory (US-0105)` | AC-7, AC-8 |

**Total**: 11 tasks covering 8 ACs (surjective)

### AC → Task reverse map

| AC | Tasks |
|----|-------|
| AC-1 | T-001, T-002 |
| AC-2 | T-003, T-006 |
| AC-3 | T-004 |
| AC-4 | T-007 |
| AC-5 | T-005, T-009 |
| AC-6 | T-005, T-008 |
| AC-7 | T-010, T-011 |
| AC-8 | T-002, T-006, T-010, T-011 (+ architecture pre-satisfied) |

---

## Task Seeds

### T-001: Scratchpad keys `SOVEREIGN_MEMORY_*`

**Coverage**: AC-1  
**Risk**: LOW  
**Dependencies**: None  
**Tranche**: A  
**Scope**:
- Add five keys to `.cursor/scratchpad.md` and `template/.cursor/scratchpad.md` (byte-parity per US-0017):
  - `SOVEREIGN_MEMORY` ∈ {`0`, `1`}, default `0`
  - `SOVEREIGN_MEMORY_TOP_N` (int ≥ 0, default `5`)
  - `SOVEREIGN_MEMORY_TOP_K` (int ≥ 0, default `3`)
  - `SOVEREIGN_MEMORY_MAX_CHARS` (int ≥ 0, default `2048`)
  - `SOVEREIGN_MEMORY_JSONL_MAX_LINES` (int ≥ 1, default `500`)

**Exit criteria**:
- Both scratchpad files contain all five keys with correct defaults
- `test_us0105_scratchpad_keys_literals` passes (after T-010)

---

### T-002: Scratchpad comment block + reason codes § US-0105 + DEC-0105 template mirror

**Coverage**: AC-1, AC-8  
**Risk**: LOW  
**Dependencies**: T-001  
**Tranche**: A  
**Scope**:
- Add `## Sovereign Memory (US-0105 / DEC-0105)` comment block to scratchpad (active + template) documenting default-off, top-N/top-K/char-cap/rollover semantics, and compose rules
- Ensure 8 reason codes in `docs/engineering/reason_codes.md` § US-0105 per DEC-0105 §9:
  - `SOVEREIGN_MEMORY_DISABLED`, `SOVEREIGN_MEMORY_SCHEMA_INVALID`, `SOVEREIGN_MEMORY_APPEND_FAILED`, `SOVEREIGN_MEMORY_DECISION_DUPLICATE`, `SOVEREIGN_MEMORY_SECRET_DETECTED`, `SOVEREIGN_MEMORY_ARCHIVE_REQUIRED`, `SOVEREIGN_MEMORY_READ_BOUND`, `SOVEREIGN_MEMORY_PROMOTION_SKIPPED`
- Ensure `template/decisions/DEC-0105.md` byte-parity with `decisions/DEC-0105.md`

**Exit criteria**:
- Comment block present in both scratchpad files
- All 8 codes documented with blocking? column and surface
- `test_us0105_scratchpad_keys_literals` passes (after T-010)

---

### T-003: Directory surface + `.gitkeep` bootstrap

**Coverage**: AC-2  
**Risk**: LOW  
**Dependencies**: T-001  
**Tranche**: A  
**Scope**:
- Create `docs/engineering/sovereign-memory/` (+ template mirror) with `.gitkeep`
- Create `docs/engineering/sovereign-memory/retrospectives/.gitkeep` (+ template mirror)
- Document archive path `docs/engineering/sovereign-memory-archive/<basename>-<YYYYMMDDTHHMMSSZ>.jsonl` in lib (create-on-first-write; no empty tracked JSONL seeds)

**Exit criteria**:
- Active + template directory trees present with `.gitkeep` only
- `test_us0105_sovereign_memory_directory_contract` passes (after T-010)

---

### T-004: `sovereign_memory_lib.py` read/injection core + self_test

**Coverage**: AC-3  
**Risk**: HIGH  
**Dependencies**: T-001, T-003  
**Tranche**: B  
**Scope**:
- Finalize `scripts/sovereign_memory_lib.py` (+ template mirror) read/injection core from research stub:
  - `is_sovereign_memory_enabled(scratchpad) -> bool`
  - `resolve_memory_dir` / `resolve_jsonl_path`
  - `read_entries(family, *, tail_n, active_only=True)` — bounded tail read; `SOVEREIGN_MEMORY_READ_BOUND` warn
  - `schema_check(entry, family)` — four-family v1 + secret scan
  - `scan_secrets(text)` — pre-append guard
  - `build_injection_digest(repo, scratchpad) -> InjectionDigest` — top-N recent + top-K high-impact merge, char cap, empty-corpus placeholder
  - `self_test()` → `[SOVEREIGN_MEMORY_SELF_TEST_OK]`
- Lib constant `SOVEREIGN_MEMORY_READ_TAIL` default 500

**Exit criteria**:
- `python scripts/sovereign_memory_lib.py --self-test` exit 0 with success literal
- Template mirror byte-identical
- `test_us0105_jsonl_schema_contract`, `test_us0105_injection_digest_char_cap`, `test_us0105_zero_overhead_default` pass (after T-010)

---

### T-005: `sovereign_memory_lib.py` mutations + dedup + rollover + promotion

**Coverage**: AC-5, AC-6  
**Risk**: HIGH  
**Dependencies**: T-004  
**Tranche**: C  
**Scope**:
- Implement mutation helpers in `scripts/sovereign_memory_lib.py` (+ template mirror):
  - `compute_decision_key` / `dedupe_decision` — SHA-256 prefix dedup; `SOVEREIGN_MEMORY_DECISION_DUPLICATE` on duplicate
  - `append_decision` / `append_mistake` / `append_pattern` / `append_drift` — append-only + fsync + pre-append rollover hook
  - `maybe_archive_jsonl(family)` — line-cap rollover to `sovereign-memory-archive/`; fail-closed `SOVEREIGN_MEMORY_ARCHIVE_REQUIRED`
  - `promote_from_ledger(run_id, *, decision_types)` — refresh-context promotion when `AI_DECISION_LEDGER=1`
  - `write_retrospective(sprint_id, body)` — curator markdown under `retrospectives/`

**Exit criteria**:
- Append/dedup/rollover round-trip on temp fixtures
- `test_us0105_decision_dedup_branch` passes (after T-010)

---

### T-006: `sovereign_memory_validate.py` + template mirror

**Coverage**: AC-2, AC-8  
**Risk**: HIGH  
**Dependencies**: T-004  
**Tranche**: C  
**Scope**:
- Create `scripts/sovereign_memory_validate.py` (+ template mirror):
  - `--file <path>` — validate single JSONL file
  - `--repo <root>` — validate all sovereign-memory JSONL if present
  - `--family {decisions|mistakes|patterns|plan-drift|all}`
  - `--self-test` — library contract self-test
  - `--enforce` — non-zero exit on fail-closed code
- Success literal: `[SOVEREIGN_MEMORY_VALIDATION_OK]`
- Exit codes 0/1/2 mirror DEC-0103 / DEC-0104

**Exit criteria**:
- `python scripts/sovereign_memory_validate.py --self-test` exit 0
- `--enforce` returns exit 1 on invalid fixture
- Template mirror byte-identical

---

### T-007: Phase spawn `sovereign_memory_digest` block integration

**Coverage**: AC-4  
**Risk**: MEDIUM  
**Dependencies**: T-004  
**Tranche**: D  
**Scope**:
- When `SOVEREIGN_MEMORY=1`, spawn assembler appends read-only `sovereign_memory_digest` block after phase-context narrow-read, before role instructions
- Digest assembled via `build_injection_digest(repo, scratchpad)` — bounded additive input only
- **US-0023** unchanged — no phase-role change; zero overhead when `SOVEREIGN_MEMORY=0`

**Exit criteria**:
- Spawn integration prose locked in phase command execution models or spawn assembler hook
- `test_us0105_injection_digest_char_cap` passes (after T-010)
- `test_us0105_zero_overhead_default` passes (after T-010)

---

### T-008: Mistake-tagging hooks

**Coverage**: AC-6  
**Risk**: MEDIUM  
**Dependencies**: T-005  
**Tranche**: D  
**Scope**:
- Wire orchestrator-detectable mistake hooks (no-op when `SOVEREIGN_MEMORY=0`):
  - `/auto` fix exhaust → `mistake_tag=fix_failed`, `failure_reason_code=FIX_FAILED`
  - `/execute` revert/rollback → `mistake_tag=revert_applied`, `failure_reason_code=REVERT_APPLIED`
  - Plan-fidelity hard stop → `mistake_tag=plan_fidelity_violation`, `failure_reason_code=PLAN_FIDELITY_VIOLATION`
  - Scope creep → `mistake_tag=scope_creep`, `failure_reason_code=PLAN_FIDELITY_SCOPE_GATE`
- Compose **US-0103**: hook reads ledger context for `provenance_ref` but does not mutate ledger schema

**Exit criteria**:
- `test_us0105_mistake_tagging_literals` passes (after T-010)
- Closed `mistake_tag` enum matches DEC-0105 trigger table

---

### T-009: `/refresh-context` curator retrospective + ledger promotion

**Coverage**: AC-5  
**Risk**: MEDIUM  
**Dependencies**: T-005  
**Tranche**: D  
**Scope**:
- At `/refresh-context` after release:
  1. `write_retrospective(sprint_id, body)` → `retrospectives/<sprint_id>.md`
  2. When `SOVEREIGN_MEMORY=1` and `AI_DECISION_LEDGER=1`: `promote_from_ledger()` → `decisions-log.jsonl` with `provenance_ref=ledger:<decision_id>`
  3. Ledger off or empty filter → `SOVEREIGN_MEMORY_PROMOTION_SKIPPED`
- Retrospectives not injected v1

**Exit criteria**:
- Refresh-context command prose documents retrospective + promotion wiring
- Promotion path uses distinct `decisions-log.jsonl` schema (not ledger schema)

---

### T-010: Eight `test_us0105_*` + compose regression guards

**Coverage**: AC-7, AC-8  
**Risk**: HIGH  
**Dependencies**: T-004..T-009  
**Tranche**: E  
**Scope**:
- Create `tests/us0105_contract_test.py` with eight markers per DEC-0105 §12:
  1. `test_us0105_scratchpad_keys_literals`
  2. `test_us0105_sovereign_memory_directory_contract`
  3. `test_us0105_jsonl_schema_contract`
  4. `test_us0105_injection_digest_char_cap`
  5. `test_us0105_decision_dedup_branch`
  6. `test_us0105_mistake_tagging_literals`
  7. `test_us0105_zero_overhead_default`
  8. `test_us0105_compose_guards`
- Compose regression guards:
  - `test_us0105_us0029_compose_no_research_schema_change`
  - `test_us0105_us0080_injection_respects_char_cap`

**Exit criteria**:
- `pytest -k us0105` → 8/8 core markers + 2 compose guards PASS
- Tests are deterministic (no network; temp dirs for fixtures)

---

### T-011: `SOVEREIGN_MEMORY_PAIRS` parity + runbook

**Coverage**: AC-7, AC-8  
**Risk**: MEDIUM  
**Dependencies**: T-006, T-009  
**Tranche**: E  
**Scope**:
- Register `SOVEREIGN_MEMORY_PAIRS` in `scripts/check_intake_template_parity.py` (+ template mirror):
  - `scripts/sovereign_memory_lib.py` ↔ `template/scripts/sovereign_memory_lib.py`
  - `scripts/sovereign_memory_validate.py` ↔ `template/scripts/sovereign_memory_validate.py`
  - `.cursor/scratchpad.md` ↔ `template/.cursor/scratchpad.md` (`SOVEREIGN_MEMORY_*` block)
  - `docs/engineering/sovereign-memory/.gitkeep` ↔ `template/docs/engineering/sovereign-memory/.gitkeep`
  - `decisions/DEC-0105.md` ↔ `template/decisions/DEC-0105.md`
- Add `### Sovereign Memory (US-0105)` to `docs/engineering/runbook.md` (+ template mirror):
  - Enable/disable memory
  - Interpret JSONL families vs per-run ledger
  - Injection char-cap troubleshooting
  - Archive rollover remediation

**Exit criteria**:
- `python scripts/check_intake_template_parity.py --scope=sovereign-memory` → `[INTAKE_TEMPLATE_PARITY_OK]`
- Runbook section present in active + template
- Operator recipe covers enable/disable/ledger-vs-decisions-log distinction

---

## Appendix: Task Dependencies (Visual)

```
T-001 (scratchpad keys)
    ↓
T-002 (comment block + reason codes + DEC mirror)
    ↓
T-003 (directory .gitkeep bootstrap)
    ↓
T-004 (lib read/injection core + self_test)
    ↓
    ├─→ T-005 (lib mutations + dedup + rollover + promotion)
    ├─→ T-006 (validator CLI)
    └─→ T-007 (spawn digest hook)
            ↓
    T-005
            ↓
    ├─→ T-008 (mistake-tagging hooks)
    └─→ T-009 (curator retrospective + promotion)
            ↓
        T-010 (contract tests)
            ↓
        T-011 (parity + runbook)
```

**Task Execution Order**: T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 → T-008 → T-009 → T-010 → T-011
