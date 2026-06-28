# Sprint S0104 — Tasks (US-0104)

**sprint_id**: S0104  
**story_refs**: US-0104  
**dec_ref**: DEC-0104 (binding; composes US-0048, US-0069, US-0023, US-0110, US-0103 — do not amend)  
**task_count**: 11  
**within_limit**: true (11 ≤ `SPRINT_MAX_TASKS=12`)  
**coverage**: AC-1..AC-8 surjective via T-001..T-011 (8 ACs, 11 tasks; multi-AC tasks T-002, T-003, T-005, T-006, T-011)

---

## Task-to-AC Bijection Table (canonical)

| Task ID | Coverage | ACs Satisfied |
|---------|----------|---------------|
| T-001 | Scratchpad keys `CROSS_MODEL_*` (active + template) | AC-1 |
| T-002 | Scratchpad comment block + 10 reason codes in `reason_codes.md` § US-0104 + `DEC-0104` template mirror | AC-1, AC-8 |
| T-003 | `sovereign_critic_lib.py` core: enable gate, issue key, reconciliation, model selection, anti-slop rubric, schema_check, self_test | AC-3, AC-5 |
| T-004 | `sovereign_critic_lib.py` IO: append_finding, read_open_blocking, resolve_finding, build_qa_cross_reviewer_block, patch_ledger_cross_model_reviewed | AC-5 |
| T-005 | `sovereign_critic_validate.py` + template mirror | AC-5, AC-8 |
| T-006 | `.cursor/commands/sovereign-critic.md` + template + three-lens prompts + `/auto` hook prose | AC-2, AC-3 |
| T-007 | `/auto` post-phase hook + anti-slop rework loop + `dev_to_qa.md` `critic_evidence` tuple | AC-6 |
| T-008 | Isolation evidence `model_id` v2 additive extension + `ISOLATION_EVIDENCE_MODEL_ID_MISSING` fail-closed | AC-4 |
| T-009 | Degraded single-model-multi-lens orchestration in `/auto` + `degraded_mode` findings flag | AC-7 |
| T-010 | Eight `test_us0104_*` + compose regression guards in `tests/us0104_contract_test.py` | AC-8 |
| T-011 | `SOVEREIGN_CRITIC_PAIRS` parity `--scope=sovereign-critic` + runbook `### Cross-Model Adversarial Critic (US-0104)` | AC-7, AC-8 |

**Total**: 11 tasks covering 8 ACs (surjective)

### AC → Task reverse map

| AC | Tasks |
|----|-------|
| AC-1 | T-001, T-002 |
| AC-2 | T-006 |
| AC-3 | T-003, T-006 |
| AC-4 | T-008 |
| AC-5 | T-003, T-004, T-005 |
| AC-6 | T-007 |
| AC-7 | T-009, T-011 |
| AC-8 | T-002, T-005, T-010, T-011 (+ architecture pre-satisfied) |

---

## Task Seeds

### T-001: Scratchpad keys `CROSS_MODEL_*`

**Coverage**: AC-1  
**Risk**: LOW  
**Dependencies**: None  
**Tranche**: A  
**Scope**:
- Add three keys to `.cursor/scratchpad.md` and `template/.cursor/scratchpad.md` (byte-parity per US-0017):
  - `CROSS_MODEL_REVIEW` ∈ {`0`, `1`}, default `0`
  - `CROSS_MODEL_ANTISLOP_THRESHOLD` (int 0–10, default `6`)
  - `CROSS_MODEL_REWORK_MAX` (int ≥ 0, default `2`)

**Exit criteria**:
- Both scratchpad files contain all three keys with correct defaults
- `test_us0104_scratchpad_keys_literals` passes (after T-010)

---

### T-002: Scratchpad comment block + reason codes § US-0104 + DEC-0104 template mirror

**Coverage**: AC-1, AC-8  
**Risk**: LOW  
**Dependencies**: T-001  
**Tranche**: A  
**Scope**:
- Add `## Cross-Model Adversarial Critic (US-0104 / DEC-0104)` comment block to scratchpad (active + template) documenting default-off, anti-slop threshold, rework cap, and compose rules
- Add 10 reason codes to `docs/engineering/reason_codes.md` § US-0104 per DEC-0104 §11:
  - `CROSS_MODEL_REVIEW_DISABLED`, `CROSS_MODEL_CRITIC_SPAWN_FAILED`, `CROSS_MODEL_MODEL_COLLISION`, `CROSS_MODEL_ANTISLOP_FAIL`, `CROSS_MODEL_REWORK_CAP_EXHAUSTED`, `CROSS_MODEL_FINDINGS_INVALID`, `CROSS_MODEL_RECONCILE_FAILED`, `CROSS_MODEL_DEGRADED_MODE`, `CROSS_MODEL_CRITIC_MODEL_UNAVAILABLE`, `ISOLATION_EVIDENCE_MODEL_ID_MISSING`
- Ensure `template/decisions/DEC-0104.md` byte-parity with `decisions/DEC-0104.md`

**Exit criteria**:
- Comment block present in both scratchpad files
- All 10 codes documented with blocking? column and surface
- `test_us0104_scratchpad_keys_literals` passes (after T-010)

---

### T-003: `sovereign_critic_lib.py` core API + self_test

**Coverage**: AC-3, AC-5  
**Risk**: HIGH  
**Dependencies**: T-001  
**Tranche**: B  
**Scope**:
- Finalize `scripts/sovereign_critic_lib.py` (+ template mirror) from research stub:
  - `is_cross_model_review_enabled(scratchpad) -> bool`
  - `compute_issue_key(finding_text) -> str` (`ik_<sha16>` algorithm)
  - `reconcile_findings(raw_findings) -> ReconciliationResult` (≥2 lenses → high; single → medium)
  - `select_critic_model(producer_model_id, scratchpad, phase_id) -> SelectCriticResult` (tier opposition)
  - `score_lens_antislop(lens, checklist_hits) -> int` (4-item checklist × 2.5 pts)
  - `compute_anti_slop_aggregate(lens_scores) -> int` (`min(lens_scores)`)
  - `schema_check(entry) -> (bool, error|None)` (15-field v1)
  - `self_test()` → `[SOVEREIGN_CRITIC_SELF_TEST_OK]`

**Exit criteria**:
- `python scripts/sovereign_critic_lib.py --self-test` exit 0 with success literal
- Template mirror byte-identical
- `test_us0104_three_lens_enum_contract`, `test_us0104_reconciliation_agreement_branches` pass (after T-010)

---

### T-004: `sovereign_critic_lib.py` IO + ledger hook

**Coverage**: AC-5  
**Risk**: HIGH  
**Dependencies**: T-003  
**Tranche**: B  
**Scope**:
- Implement IO helpers in `scripts/sovereign_critic_lib.py` (+ template mirror):
  - `append_finding(path, entry) -> (bool, reason_code|None)` (append-only JSONL + fsync)
  - `read_open_blocking(repo) -> list[dict]`
  - `resolve_finding(path, finding_id, status) -> bool`
  - `build_qa_cross_reviewer_block(repo) -> dict` (`cross_reviewer_findings` for `qa-findings.md`)
  - `patch_ledger_cross_model_reviewed(...)` (US-0103 `cross_model_reviewed=True` when ledger enabled)
- Canonical findings path: `handoffs/sovereign_critic_findings.jsonl`

**Exit criteria**:
- Append/read/resolve round-trip on temp fixtures
- `test_us0104_findings_jsonl_schema_contract` passes (after T-010)

---

### T-005: `sovereign_critic_validate.py` + template mirror

**Coverage**: AC-5, AC-8  
**Risk**: HIGH  
**Dependencies**: T-003  
**Tranche**: C  
**Scope**:
- Create `scripts/sovereign_critic_validate.py` (+ template mirror):
  - `--file <path>` — validate single JSONL file
  - `--repo <root>` — validate `handoffs/sovereign_critic_findings.jsonl` if present
  - `--self-test` — library contract self-test
  - `--enforce` — non-zero exit on fail-closed code
  - `--open-blocking` — list open blocking findings (stdout JSON)
- Success literal: `[SOVEREIGN_CRITIC_VALIDATION_OK]`

**Exit criteria**:
- `python scripts/sovereign_critic_validate.py --self-test` exit 0
- `--enforce` returns exit 1 on invalid fixture
- Template mirror byte-identical

---

### T-006: `/sovereign-critic` command + three-lens prompts + `/auto` hook

**Coverage**: AC-2, AC-3  
**Risk**: MEDIUM  
**Dependencies**: T-001  
**Tranche**: C  
**Scope**:
- Create `.cursor/commands/sovereign-critic.md` (+ template mirror):
  - Inputs: `phase_id`, `role`, `evidence_ref`, `producer_model_id`, artifact digest
  - Three lens prompt templates: `challenger`, `architect`, `subtractor`
  - All three lenses run per invocation (parallel jury)
  - Outputs: append findings JSONL + optional `cross_reviewer_findings` in sprint `qa-findings.md`
- Document `/auto` orchestrator post-phase hook prose (after producer phase when `CROSS_MODEL_REVIEW=1`)

**Exit criteria**:
- `test_us0104_sovereign_critic_command_literals` passes (after T-010)
- `test_us0104_three_lens_enum_contract` passes (after T-010)
- Active + template command files byte-identical

---

### T-007: Anti-slop rework loop + `dev_to_qa.md` evidence tuple

**Coverage**: AC-6  
**Risk**: HIGH  
**Dependencies**: T-003, T-004, T-006  
**Tranche**: D  
**Scope**:
- Wire `/auto` post-phase hook after `/sovereign-critic`:
  1. Compute aggregate via `compute_anti_slop_aggregate`
  2. If aggregate < `CROSS_MODEL_ANTISLOP_THRESHOLD` and blocking findings exist → rework loop
  3. Increment `rework_generation` per `(orchestrator_run_id, phase_id)`
  4. If `rework_generation < CROSS_MODEL_REWORK_MAX`: re-spawn producer (fresh context per US-0023) → `CROSS_MODEL_ANTISLOP_FAIL`
  5. Else → `CROSS_MODEL_REWORK_CAP_EXHAUSTED` decision gate
- Add additive `critic_evidence` block to `dev_to_qa.md` evidence tuple when `CROSS_MODEL_REVIEW=1`

**Exit criteria**:
- `test_us0104_antislop_rework_cap_literals` passes (after T-010)
- Rework cap and decision gate prose locked in `/auto` command

---

### T-008: Isolation evidence `model_id` v2 extension

**Coverage**: AC-4  
**Risk**: MEDIUM  
**Dependencies**: T-001  
**Tranche**: D  
**Scope**:
- Additive `model_id` field on US-0048 evidence tuple (base five fields unchanged)
- Required on **both** producer and critic isolation entries when `CROSS_MODEL_REVIEW=1`; omitted when `0`
- Fail-closed `ISOLATION_EVIDENCE_MODEL_ID_MISSING` when critic enabled and `model_id` absent

**Exit criteria**:
- `test_us0104_model_id_isolation_evidence_extension` passes (after T-010)
- `test_us0104_us0048_compose_no_base_schema_change` passes (after T-010)

---

### T-009: Degraded single-model-multi-lens fallback

**Coverage**: AC-7  
**Risk**: MEDIUM  
**Dependencies**: T-003, T-006  
**Tranche**: D  
**Scope**:
- When `select_critic_model` resolves same slug as producer (or catalog miss): `degraded_mode=true`
- Three sequential fresh subagent spawns (same `model_id`, different lens prompts)
- All findings record `degraded_mode=true`; reason `CROSS_MODEL_DEGRADED_MODE` (informational, not hard stop)
- Zero overhead when `CROSS_MODEL_REVIEW=0`

**Exit criteria**:
- `test_us0104_degraded_fallback_zero_overhead` passes (after T-010)
- Degraded path documented in `/auto` + runbook

---

### T-010: Eight `test_us0104_*` + compose regression guards

**Coverage**: AC-8  
**Risk**: HIGH  
**Dependencies**: T-003..T-009  
**Tranche**: E  
**Scope**:
- Create `tests/us0104_contract_test.py` with eight markers per DEC-0104 §12:
  1. `test_us0104_scratchpad_keys_literals`
  2. `test_us0104_sovereign_critic_command_literals`
  3. `test_us0104_three_lens_enum_contract`
  4. `test_us0104_findings_jsonl_schema_contract`
  5. `test_us0104_reconciliation_agreement_branches`
  6. `test_us0104_model_id_isolation_evidence_extension`
  7. `test_us0104_antislop_rework_cap_literals`
  8. `test_us0104_degraded_fallback_zero_overhead`
- Compose regression guards:
  - `test_us0104_us0048_compose_no_base_schema_change`
  - `test_us0104_us0110_critic_path_unchanged`

**Exit criteria**:
- `pytest -k us0104` → 8/8 core markers + 2 compose guards PASS
- Tests are deterministic (no network; temp dirs for fixtures)

---

### T-011: `SOVEREIGN_CRITIC_PAIRS` parity + runbook

**Coverage**: AC-7, AC-8  
**Risk**: MEDIUM  
**Dependencies**: T-005, T-009  
**Tranche**: E  
**Scope**:
- Register `SOVEREIGN_CRITIC_PAIRS` in `scripts/check_intake_template_parity.py` (+ template mirror):
  - `scripts/sovereign_critic_lib.py` ↔ `template/scripts/sovereign_critic_lib.py`
  - `scripts/sovereign_critic_validate.py` ↔ `template/scripts/sovereign_critic_validate.py`
  - `.cursor/commands/sovereign-critic.md` ↔ `template/.cursor/commands/sovereign-critic.md`
  - `.cursor/scratchpad.md` ↔ `template/.cursor/scratchpad.md` (`CROSS_MODEL_*` block)
  - `decisions/DEC-0104.md` ↔ `template/decisions/DEC-0104.md`
- Add `### Cross-Model Adversarial Critic (US-0104)` to `docs/engineering/runbook.md` (+ template mirror):
  - Enable/disable critic
  - Interpret findings JSONL
  - Degraded fallback troubleshooting
  - Anti-slop rework remediation

**Exit criteria**:
- `python scripts/check_intake_template_parity.py --scope=sovereign-critic` → `[INTAKE_TEMPLATE_PARITY_OK]`
- Runbook section present in active + template
- Operator recipe covers enable/disable/rework cap/degraded mode

---

## Appendix: Task Dependencies (Visual)

```
T-001 (scratchpad keys)
    ↓
T-002 (comment block + reason codes + DEC mirror)
    ↓
T-003 (lib core + self_test)
    ↓
    ├─→ T-004 (lib IO + ledger hook)
    ├─→ T-005 (validator CLI)
    └─→ T-006 (sovereign-critic command)
            ↓
    T-004 + T-006 + T-003
            ↓
    ├─→ T-007 (rework loop + dev_to_qa tuple)
    ├─→ T-008 (model_id isolation v2)
    └─→ T-009 (degraded fallback)
            ↓
        T-010 (contract tests)
            ↓
        T-011 (parity + runbook)
```

**Task Execution Order**: T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 → T-008 → T-009 → T-010 → T-011
