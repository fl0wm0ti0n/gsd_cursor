# Sprint S0103 — Tasks (US-0103)

**sprint_id**: S0103  
**story_refs**: US-0103  
**dec_ref**: DEC-0103 (binding; composes US-0070, US-0069, US-0048, US-0092 — do not amend)  
**task_count**: 11  
**within_limit**: true (11 ≤ `SPRINT_MAX_TASKS=12`)  
**coverage**: AC-1..AC-8 surjective via T-001..T-011 (8 ACs, 11 tasks; multi-AC tasks T-001, T-002, T-003, T-004, T-005, T-006, T-007, T-008, T-009, T-010, T-011)

---

## Task-to-AC Bijection Table

| Task ID | Coverage | ACs Satisfied |
|---------|----------|---------------|
| T-001 | Scratchpad keys declaration | AC-1 |
| T-002 | Ledger artifact structure + schema definition | AC-2 |
| T-003 | Helper library contract (decision_ledger_lib.py) | AC-2, AC-3, AC-4, AC-5 |
| T-004 | Validator CLI contract (ledger_validate.py) | AC-2 |
| T-005 | Plan-fidelity deviation classification table implementation | AC-3 |
| T-006 | QA cross-check implementation (qa_findings.md integration) | AC-6 |
| T-007 | Contract tests (test_us0103_*) | AC-7 |
| T-008 | Reason codes enumeration | AC-8 |
| T-009 | Documentation (architecture.md # US-0103) | AC-8 |
| T-010 | Documentation (runbook.md §AI Decision Ledger) | AC-8 |
| T-011 | Template parity verification (SOVEREIGN_LEDGER_PAIRS) | AC-1, AC-2, AC-8 |

**Total**: 11 tasks covering 8 ACs (surjective)

---

## Task Seeds

### T-001: Scratchpad Keys Declaration

**Coverage**: AC-1  
**Risk**: LOW  
**Dependencies**: None  
**Scope**:
- Create `.cursor/scratchpad.md` (if not exists) with keys:
  - `AI_DECISION_LEDGER` (enum: `0|1`, default: `0`)
  - `AUTO_PLAN_FIDELITY` (enum: `strict|relaxed|extended`, default: `strict`)
- Add documentation comments explaining zero-overhead behavior when `AI_DECISION_LEDGER=0`

**Exit criteria**:
- Scratchpad file contains both keys with correct defaults
- Keys are documented with enum values and semantics
- Template parity verified (T-011)

---

### T-002: Ledger Artifact Structure + Schema Definition

**Coverage**: AC-2  
**Risk**: MEDIUM  
**Dependencies**: None  
**Scope**:
- Create `handoffs/sovereign_decisions/` directory (if not exists)
- Create `handoffs/sovereign_decisions/.gitkeep`
- Create `template/handoffs/sovereign_decisions/.gitkeep` (byte-identical)
- Define ledger JSONL schema (12-field, all required):
  - `ts` (ISO-8601 UTC)
  - `orchestrator_run_id` (string)
  - `phase_id` (canonical phase list from DEC-0086)
  - `role` (canonical roles: dev, tech-lead, qa, po, etc.)
  - `decision_id` (UUIDv4)
  - `decision_type` (9 values: PLAN_FIDELITY_* + LEDGER_*)
  - `from_artifact`, `to_artifact`, `rationale`, `plan_fidelity`, `cross_model_reviewed`, `risk_tier`

**Exit criteria**:
- Directory structure exists with `.gitkeep` files
- Schema definition documented in `docs/engineering/architecture.md` §US-0103
- 12-field schema is complete and validated

---

### T-003: Helper Library Contract (decision_ledger_lib.py)

**Coverage**: AC-2, AC-3, AC-4, AC-5  
**Risk**: HIGH  
**Dependencies**: T-002 (schema definition must exist first)  
**Scope**:
- Create `scripts/decision_ledger_lib.py` with functions:
  - `validate_schema_v1(entry: dict) -> bool` — validates 12-field JSONL entry
  - `append_entry(entry: dict, ledger_path: Path) -> None` — append-only with fsync semantics
  - `read_ledger(ledger_path: Path) -> list[dict]` — read with bounded reads (last_n or full)
  - `build_qa_crosscheck_block(ledger_entries: list[dict]) -> dict` — produces ledger_findings dict
  - `classify_deviation(decision_type: str, plan_fidelity: str) -> enum` — deviation classification

**Exit criteria**:
- Library exists with all 5 functions defined
- `validate_schema_v1` validates all 12 fields with correct types
- `append_entry` enforces append-only + fsync semantics
- `build_qa_crosscheck_block` produces correct ledger_findings structure
- Library is functional (can be imported and called)

---

### T-004: Validator CLI Contract (ledger_validate.py)

**Coverage**: AC-2  
**Risk**: MEDIUM  
**Dependencies**: T-002, T-003 (schema + helper lib must exist)  
**Scope**:
- Create `scripts/ledger_validate.py` CLI with flags:
  - `--file <path>`: validate single ledger file
  - `--repo <root>`: validate all *.jsonl in handoffs/sovereign_decisions/
  - `--self-test`: run decision_ledger_lib.py self-test
  - `--strict-fidelity`: enforce plan-fidelity validation
- Exit codes:
  - `0`: All validations passed
  - `1`: Fail-closed code hit (schema invalid, file missing)
  - `2`: Usage error

**Exit criteria**:
- CLI exists with all 4 flags functional
- Exit codes behave as specified
- CLI can validate a sample ledger file
- --self-test runs decision_ledger_lib.py validation

---

### T-005: Plan-Fidelity Deviation Classification Table Implementation

**Coverage**: AC-3  
**Risk**: HIGH  
**Dependencies**: T-003 (classify_deviation function must exist)  
**Scope**:
- Implement deviation classification logic in `scripts/decision_ledger_lib.py`:
  - `strict` mode:
    - drop AC → `PLAN_FIDELITY_VIOLATION` (blocks)
    - reorder AC → `PLAN_FIDELITY_VIOLATION` (blocks)
    - add new scope → `PLAN_FIDELITY_SCOPE_GATE` (blocks)
    - operator-approved relaxation → `PLAN_FIDELITY_OVERRIDE` (does not block)
  - `relaxed` mode:
    - drop AC → `PLAN_FIDELITY_REORDER` (does not block)
    - reorder AC → `PLAN_FIDELITY_REORDER` (does not block)
    - add new scope → `PLAN_FIDELITY_SCOPE_GATE` (blocks)
    - operator-approved relaxation → `PLAN_FIDELITY_OVERRIDE` (does not block)
  - `extended` mode:
    - add new scope → `PLAN_FIDELITY_EXTENSION` (does not block)
    - drop/reorder AC → `PLAN_FIDELITY_REORDER` (does not block)
    - operator-approved relaxation → `PLAN_FIDELITY_OVERRIDE` (does not block)

**Exit criteria**:
- All 9 deviation types classified correctly
- Blocking behavior correct (PLAN_FIDELITY_VIOLATION, PLAN_FIDELITY_SCOPE_GATE block; PLAN_FIDELITY_REORDER, PLAN_FIDELITY_EXTENSION, PLAN_FIDELITY_OVERRIDE do not block)
- Classification logic matches DEC-0103 §3 deviation table

---

### T-006: QA Cross-Check Implementation

**Coverage**: AC-6  
**Risk**: HIGH  
**Dependencies**: T-003 (build_qa_crosscheck_block function must exist)  
**Scope**:
- Integrate `build_qa_crosscheck_block` into `/qa` phase workflow
- Ensure `/qa` phase reads ledger from `handoffs/sovereign_decisions/<orchestrator_run_id>.jsonl`
- Emit `ledger_findings` section in `qa_findings.md` with:
  - `decision_id`
  - `decision_type`
  - `rationale_summary` (truncated to 200 chars)
  - `phase_id`, `role`, `risk_tier`, `plan_fidelity_mode`

**Exit criteria**:
- `/qa` phase can read ledger and produce QA cross-check output
- `ledger_findings` structure in `qa_findings.md` matches specification
- Cross-check fails closed when ledger missing (`LEDGER_FILE_MISSING` code)

---

### T-007: Contract Tests (test_us0103_*)

**Coverage**: AC-7  
**Risk**: HIGH  
**Dependencies**: T-001, T-002, T-003, T-004, T-005, T-006 (all implementation must be complete)  
**Scope**:
- Create `tests/us0103_contract_test.py` with 6 tests:
  - `test_us0103_scratchpad_keys_exist()`: AC-1
  - `test_us0103_ledger_schema_validation()`: AC-2
  - `test_us0103_strict_mode_behavior()`: AC-3
  - `test_us0103_relaxed_mode_behavior()`: AC-4
  - `test_us0103_extended_mode_behavior()`: AC-5
  - `test_us0103_qa_crosscheck_block()`: AC-6

**Exit criteria**:
- All 6 tests pass: `pytest tests/us0103_contract_test.py`
- Tests cover all 6 acceptance criteria
- Tests are deterministic (no flaky behavior)

---

### T-008: Reason Codes Enumeration

**Coverage**: AC-8  
**Risk**: MEDIUM  
**Dependencies**: T-003, T-004, T-005 (reason codes must be defined in implementation)  
**Scope**:
- Create `docs/engineering/reason_codes.md` (if not exists)
- Add US-0103 reason codes section:
  - **PLAN_FIDELITY_*** (5 codes):
    - `PLAN_FIDELITY_VIOLATION` (blocking, strict mode deviation)
    - `PLAN_FIDELITY_OVERRIDE` (non-blocking, operator-approved relaxation)
    - `PLAN_FIDELITY_SCOPE_GATE` (blocking, new scope in strict/relaxed)
    - `PLAN_FIDELITY_EXTENSION` (non-blocking, scope extension in extended)
    - `PLAN_FIDELITY_REORDER` (non-blocking, AC drop/reorder in relaxed/extended)
  - **LEDGER_*** (6 codes):
    - `LEDGER_FILE_MISSING` (blocking, ledger missing when enabled)
    - `LEDGER_FILE_EMPTY` (blocking, ledger empty when enabled)
    - `LEDGER_SCHEMA_INVALID` (blocking, schema validation failure)
    - `LEDGER_READ_ERROR` (blocking, ledger read failure)
    - `LEDGER_WRITE_ERROR` (blocking, ledger write failure)
    - `LEDGER_FSYNC_ERROR` (blocking, fsync failure)

**Exit criteria**:
- 11 reason codes documented (5 PLAN_FIDELITY_* + 6 LEDGER_*)
- Each code has: description, blocking behavior, exit-code mapping
- Documentation matches reason codes in `decision_ledger_lib.py` and `ledger_validate.py`

---

### T-009: Documentation (architecture.md # US-0103)

**Coverage**: AC-8  
**Risk**: LOW  
**Dependencies**: T-008 (reason codes documented first)  
**Scope**:
- Add `# US-0103` section to `docs/engineering/architecture.md`
- Include:
  - Scratchpad keys (AC-1)
  - Ledger artifact schema (AC-2)
  - Helper library contract (AC-2)
  - Validator CLI contract (AC-2)
  - Plan-fidelity deviation table (AC-3, AC-4, AC-5)
  - QA cross-check contract (AC-6)
  - Contract tests inventory (AC-7)
  - Reason codes enumeration (AC-8)

**Exit criteria**:
- `docs/engineering/architecture.md` contains `# US-0103` section with all subsections
- Documentation complete and accurate
- Matches implementation

---

### T-010: Documentation (runbook.md §AI Decision Ledger)

**Coverage**: AC-8  
**Risk**: LOW  
**Dependencies**: T-009 (architecture.md must be complete first)  
**Scope**:
- Add `## AI Decision Ledger` subsection to `docs/engineering/runbook.md`
- Include:
  - How to enable US-0103 (set scratchpad keys)
  - How to audit ledger entries
  - How to interpret plan-fidelity modes
  - Common ledger failure scenarios and recovery steps

**Exit criteria**:
- Runbook contains AI Decision Ledger section
- Documentation provides practical guidance for operators
- Steps are testable and verifiable

---

### T-011: Template Parity Verification (SOVEREIGN_LEDGER_PAIRS)

**Coverage**: AC-1, AC-2, AC-8  
**Risk**: MEDIUM  
**Dependencies**: T-001, T-002, T-003, T-004, T-005, T-006, T-007, T-008, T-009, T-010 (all implementation complete)  
**Scope**:
- Add `SOVEREIGN_LEDGER_PAIRS = 4` to `scripts/check_intake_template_parity.py`
- Update parity check to verify:
  - Scratchpad keys (`.cursor/scratchpad.md`)
  - Ledger directory (`handoffs/sovereign_decisions/`)
  - Helper library (`scripts/decision_ledger_lib.py`)
  - Validator CLI (`scripts/ledger_validate.py`)
- Exit `0` on parity pass, `1` on parity fail

**Exit criteria**:
- Parity check passes for all 4 sovereign ledger pairs
- Template and active files are byte-identical where they should be
- Parity check fails loudly on divergence

---

## Appendix: Task Dependencies (Visual)

```
T-001 (scratchpad keys)
    ↓
T-002 (ledger artifact)
    ↓
T-003 (helper library)
    ↓
    ├─→ T-004 (validator CLI)
    ├─→ T-005 (deviation classification)
    └─→ T-006 (QA cross-check)
            ↓
        T-007 (tests)
            ↓
        T-008 (reason codes)
            ↓
        T-009 (architecture.md)
            ↓
        T-010 (runbook.md)
            ↓
        T-011 (parity check)
```

---

**Task Execution Order**: T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 → T-008 → T-009 → T-010 → T-011
