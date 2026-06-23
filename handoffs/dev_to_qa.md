# Dev-to-QA Handoff — Sprint S0091 / US-0101

## Execute Phase Complete

**Story**: US-0101 — Per-phase model tier selection for subagents  
**Decision**: DEC-0086 (locked)  
**Sprint**: S0091  
**Phase**: execute → qa  
**Timestamp**: 2026-06-15T22:30:00Z  
**Fresh Context Marker**: `dev-US0101-execute-20260615T223000Z-fresh`

---

## Implementation Summary

All 10 tasks (T-001 through T-010) implemented per DEC-0086 architecture decisions.

### Tranche A — Scratchpad + Matrix Documentation
- **T-001** [DONE] — Scratchpad keys: `MODEL_TIER_*`, `MODEL_CATALOG`, `MODEL_RESOLVE`, `MODEL_FALLBACK`, `MODEL_PROVIDER_MODE` added to `.cursor/scratchpad.md` + `.cursor/scratchpad.local.example.md`
- **T-002** [DONE] — Default phase→tier matrix documented in scratchpad comments + runbook

### Tranche B — Template Agent Defaults + Catalog Example
- **T-003** [DONE] — Template agent `model:` defaults applied:
  - `curator.mdc` → `model: fast`
  - `po.mdc`, `release.mdc` → `model: inherit`
  - `tech-lead.mdc`, `dev.mdc`, `qa.mdc`, `security.mdc` → omit `model:` field
- **T-004** [DONE] — `.cursor/model-catalog.local.example.json` created + `.cursor/model-catalog.local.json` gitignored

### Tranche C — Resolver Library + Validator
- **T-005** [DONE] — `scripts/model_tier_lib.py` — resolver algorithm + catalog schema validation + 4 reason codes (`MODEL_TIER_INVALID`, `MODEL_CATALOG_INVALID`, `MODEL_SLUG_UNKNOWN`, `MODEL_RESOLVE_FALLBACK`)
- **T-006** [DONE] — `scripts/model_tier_validate.py` — CLI validator for tier enum, catalog schema, phase key spelling, forbidden slug grep

### Tranche D — Runbook + Provider Mode Documentation
- **T-007** [DONE] — Runbook provider-mode subsection: `MODEL_PROVIDER_MODE=cursor|api` with BYOK limitation + workaround recipes
- **T-008** [DONE] — Non-substitution paragraph: `MODEL_TIER ≠ TOKEN_PROFILE ≠ DELIVERY_MODE` (orthogonal axes)

### Tranche E — Contract Tests + Parity + Harness
- **T-009** [DONE] — Eight `test_us0101_*` contract tests implemented in `tests/auto_command_contract_test.py`
- **T-010** [DONE] — `MODEL_TIER_PAIRS` parity check + harness §26Z in `tests/run-tests.sh` + `tests/run-tests.ps1`

---

## Files Created

| File | Description |
|------|-------------|
| `.cursor/model-catalog.local.example.json` | Example local catalog schema (3-tier mapping) |
| `scripts/model_tier_lib.py` | Resolver library with tier→alias mapping + catalog validation + self-test |
| `scripts/model_tier_validate.py` | CLI validator for tier enum, catalog schema, phase keys, forbidden slugs |
| `template/.cursor/model-catalog.local.example.json` | Template copy of catalog example |
| `template/scripts/model_tier_lib.py` | Template copy of resolver library |
| `template/scripts/model_tier_validate.py` | Template copy of CLI validator |

---

## Files Modified

| File | Changes |
|------|---------|
| `.cursor/scratchpad.md` | Added `MODEL_TIER_*`, `MODEL_CATALOG`, `MODEL_RESOLVE`, `MODEL_FALLBACK`, `MODEL_PROVIDER_MODE` keys |
| `.cursor/scratchpad.local.example.md` | Mirrored scratchpad changes |
| `.cursor/agents/curator.mdc` | Added `model: fast` |
| `.cursor/agents/po.mdc` | Added `model: inherit` |
| `.cursor/agents/release.mdc` | Added `model: inherit` |
| `template/.cursor/agents/curator.mdc` | Added `model: fast` |
| `template/.cursor/agents/po.mdc` | Added `model: inherit` |
| `template/.cursor/agents/release.mdc` | Added `model: inherit` |
| `.gitignore` | Added `.cursor/model-catalog.local.json` |
| `template/.gitignore` | Added `.cursor/model-catalog.local.json` |
| `docs/engineering/runbook.md` | Added US-0101 section: model tier selection, provider mode, non-substitution paragraph, reason codes |
| `template/docs/engineering/runbook.md` | Template copy of runbook |
| `tests/auto_command_contract_test.py` | Added 8 `test_us0101_*` contract tests |
| `scripts/check_intake_template_parity.py` | Added `MODEL_TIER_PAIRS` + `--scope=model-tier` |
| `template/scripts/check_intake_template_parity.py` | Template copy of parity checker |
| `tests/run-tests.sh` | Added §26Z harness section (US-0101 model tier contract + parity) |
| `tests/run-tests.ps1` | Added §26Z harness section (US-0101 model tier contract + parity) |
| `template/.cursor/scratchpad.md` | Template copy of scratchpad |
| `template/.cursor/scratchpad.local.example.md` | Template copy of scratchpad example |
| `sprints/S0091/task.json` | Updated all task statuses to DONE |
| `sprints/S0091/summary.md` | Updated implementation status, files created/modified, test results |

---

## Test Results

### Contract Tests (8/8 PASS)

```
pytest tests/auto_command_contract_test.py -k us0101
====================== 8 passed, 135 deselected in 0.09s ======================
```

- `test_us0101_scratchpad_keys` — **PASS**
- `test_us0101_default_matrix_literals` — **PASS**
- `test_us0101_token_profile_orthogonality` — **PASS**
- `test_us0101_template_agent_model_aliases` — **PASS**
- `test_us0101_forbidden_slug_grep` — **PASS**
- `test_us0101_catalog_schema_contract` — **PASS**
- `test_us0101_provider_mode_literals` — **PASS**
- `test_us0101_reason_code_inventory` — **PASS**

### Self-Test

```
python scripts/model_tier_lib.py --self-test
[SELF-TEST] Validating model_tier_lib contract...
[MODEL_TIER_SELF_TEST_OK]
```

### Parity Check

```
python scripts/check_intake_template_parity.py --scope=model-tier
[INTAKE_TEMPLATE_PARITY_OK] scope=model-tier
```

### Full Validation

```
python scripts/model_tier_validate.py --repo .
[REPO] Validating C:\flowGit\sonstiges\gsd_cursor...
[CATALOG] Validating C:\flowGit\sonstiges\gsd_cursor\.cursor\model-catalog.local.example.json...
[SCRATCHPAD] Validating C:\flowGit\sonstiges\gsd_cursor\.cursor\scratchpad.md...
[TEMPLATE] Checking C:\flowGit\sonstiges\gsd_cursor\template\.cursor\agents...
[MODEL_TIER_VALIDATION_OK]
```

---

## Acceptance Criteria Coverage

| AC | Description | Tasks | Status |
|----|-------------|-------|--------|
| AC-1 | Scratchpad tier contract | T-001 | **PASS** |
| AC-2 | Default phase→tier matrix | T-002 | **PASS** |
| AC-3 | Tier→Cursor alias resolution | (architecture-locked in DEC-0086) | **PASS** |
| AC-4 | Local model catalog | T-004, T-005 | **PASS** |
| AC-5 | Agent template defaults | T-003 | **PASS** |
| AC-6 | Provider mode runbook | T-007, T-008 | **PASS** |
| AC-7 | Validator + reason codes | T-005, T-006 | **PASS** |
| AC-8 | Contract tests + parity | T-009, T-010 | **PASS** |
| AC-9 | Architecture + decision anchor | T-010, DEC-0086 + architecture.md # US-0101 | **PASS** |

---

## Handoff to QA

**Next Phase**: `/qa` (fresh QA subagent)  
**Purpose**: Verify AC-1..AC-9 surjective coverage via T-001..T-010  
**Evidence**: 
- `sprints/S0091/summary.md` (implementation status)
- `sprints/S0091/task.json` (task statuses = DONE)
- `tests/auto_command_contract_test.py` (8 contract tests)
- `scripts/model_tier_lib.py` (resolver + self-test)
- `scripts/model_tier_validate.py` (CLI validator)
- `docs/engineering/runbook.md` (provider mode + orthogonality)

---

## Governance Notes

- **US-0101** remains **OPEN** in `docs/product/backlog.md` (authority) — do NOT flip status
- **DEC-0086** locked — architecture decisions binding
- **R-0088** closed — research complete
- **Spawn-only (BUG-0006)**: Execute implementation persisted; spawn fresh QA for `/qa`

---

## Resume Brief Update

`handoffs/resume_brief.md` updated to point to `/qa` phase with:
- `next_scheduled_phase=qa`
- `intended_resume_phase=qa`
- `resolved_start_phase=execute`
- Contract: execute **PASS** — T-001..T-010 done; 8/8 contract tests passing; parity + harness §26Z green

---

## State.md Checkpoint

Execute checkpoint appended to `docs/engineering/state.md`:
- `phase_id=execute`
- `role=dev`
- `fresh_context_marker=dev-US0101-execute-20260615T223000Z-fresh`
- `timestamp=2026-06-15T22:30:00Z`
- `verdict=PASS`
- `evidence_ref=sprints/S0091/summary.md,handoffs/dev_to_qa.md`

---

**Handoff Status**: Ready for `/qa` phase  
**Handoff Timestamp**: 2026-06-15T22:30:00Z
