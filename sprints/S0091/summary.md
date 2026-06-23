# Sprint S0091 — US-0101: Per-phase model tier selection for subagents

## Sprint Overview

**Story**: US-0101 — Per-phase model tier selection for subagents (MODEL_TIER + local catalog)  
**Decision**: DEC-0086 (locked)  
**Research**: R-0088 (closed)  
**Task Count**: 10 tasks (within SPRINT_MAX_TASKS=12 threshold)  
**Status**: released (2026-06-16T00:00:00Z)  

## Task List (Tranche A→E)

### Tranche A — Scratchpad + scratchpad docs
- **T-001** [AC-1]: Scratchpad keys — `MODEL_TIER_*`, `MODEL_CATALOG`, `MODEL_RESOLVE`, `MODEL_FALLBACK`, `MODEL_PROVIDER_MODE` in `.cursor/scratchpad.md` + template docs
- **T-002** [AC-2]: Default phase→tier matrix — document architecture-locked table in scratchpad comments + runbook

### Tranche B — Template agent defaults + catalog example
- **T-003** [AC-5]: Template agent `model:` defaults — apply `model: fast`/`model: inherit`/omit to `.cursor/agents/*.mdc` + `template/.cursor/agents/*.mdc`
- **T-004** [AC-4]: Local catalog example — `.cursor/model-catalog.local.example.json` + gitignore `.cursor/model-catalog.local.json`

### Tranche C — Resolver lib + validator
- **T-005** [AC-4, AC-7]: `model_tier_lib.py` — resolver algorithm + catalog schema validation + 4 reason codes
- **T-006** [AC-7]: `model_tier_validate.py` — CLI validator (tier enum, catalog schema, phase key spelling, forbidden slug grep)

### Tranche D — Runbook + provider-mode docs
- **T-007** [AC-6]: Runbook provider-mode subsection — `docs/engineering/runbook.md` + `auto-orchestration-reference.md` `MODEL_PROVIDER_MODE=cursor|api` + BYOK limitation + workaround recipes
- **T-008** [AC-6]: Non-substitution paragraph — explicit `MODEL_TIER` ≠ `TOKEN_PROFILE` ≠ `DELIVERY_MODE` in runbook + scratchpad comments

### Tranche E — Contract tests + parity + harness
- **T-009** [AC-8]: Eight `test_us0101_*` contract subtests — scratchpad keys, matrix literals, orthogonality, template aliases, forbidden slug grep, catalog schema, provider mode, reason codes
- **T-010** [AC-8, AC-9]: `MODEL_TIER_PAIRS` parity + harness §26Z — `check_intake_template_parity.py --scope=model-tier` + harness section

## Acceptance Criteria Mapping

| AC | Description | Tasks |
|----|-------------|-------|
| AC-1 | Scratchpad tier contract | T-001 |
| AC-2 | Default phase→tier matrix | T-002 |
| AC-3 | Tier→Cursor alias resolution | (architecture-locked in DEC-0086) |
| AC-4 | Local model catalog | T-004, T-005 |
| AC-5 | Agent template defaults | T-003 |
| AC-6 | Provider mode runbook | T-007, T-008 |
| AC-7 | Validator + reason codes | T-005, T-006 |
| AC-8 | Contract tests + parity | T-009, T-010 |
| AC-9 | Architecture + decision anchor | T-010, (pre-satisfied: DEC-0086 + architecture.md # US-0101) |

## Contract Test Inventory

Eight `test_us0101_*` contract markers:

1. `test_us0101_scratchpad_keys` — AC-1: `MODEL_TIER_<PHASE>` enum + `MODEL_TIER_DEFAULT` literals
2. `test_us0101_default_matrix_literals` — AC-2: Phase→tier table matches architecture-locked matrix
3. `test_us0101_token_profile_orthogonality` — AC-6: Grep confirms `MODEL_TIER` ≠ `TOKEN_PROFILE`
4. `test_us0101_template_agent_model_aliases` — AC-5: Template agents use `fast`/`inherit`/omit only
5. `test_us0101_forbidden_slug_grep` — AC-5: No vendor slugs in `template/.cursor/agents/`
6. `test_us0101_catalog_schema_contract` — AC-4: Validates `.cursor/model-catalog.local.example.json` schema
7. `test_us0101_provider_mode_literals` — AC-6: `MODEL_PROVIDER_MODE` enum + runbook refs
8. `test_us0101_reason_code_inventory` — AC-7: All 4 fail-closed codes in validator + lib

**Run**: `pytest -k us0101 tests/auto_command_contract_test.py`

## Risk Notes

| Risk | Mitigation |
|------|------------|
| R1: Cursor subagent BYOK limitation limits api-only mode value | Document limitation; provide workaround recipes |
| R2: `inherit` unreliable on some billing plans | Framework alias layer degrades gracefully; `strong` omits field for best fallback |
| R3: Parent agent can override subagent `model:` via Task tool | Document known Cursor behavior; stable alias layer still provides intent signal |
| R4: Operator confusion between MODEL_TIER and TOKEN_PROFILE | Explicit non-substitution paragraph in runbook + scratchpad comments |

## Implementation Status

| Task | Status | Notes |
|------|--------|-------|
| T-001 | DONE | Scratchpad keys added to `.cursor/scratchpad.md` + `.cursor/scratchpad.local.example.md` |
| T-002 | DONE | Default phase→tier matrix documented in scratchpad comments + runbook |
| T-003 | DONE | Template agent `model:` defaults applied (curator→fast, po/release→inherit, others→omit) |
| T-004 | DONE | `.cursor/model-catalog.local.example.json` created + gitignore entries |
| T-005 | DONE | `scripts/model_tier_lib.py` — resolver + catalog validation + 4 reason codes + self-test |
| T-006 | DONE | `scripts/model_tier_validate.py` — CLI validator |
| T-007 | DONE | Runbook provider-mode subsection (`MODEL_PROVIDER_MODE=cursor\|api`) |
| T-008 | DONE | Non-substitution paragraph (`MODEL_TIER ≠ TOKEN_PROFILE ≠ DELIVERY_MODE`) |
| T-009 | DONE | Eight `test_us0101_*` contract tests (8/8 passing) |
| T-010 | DONE | `MODEL_TIER_PAIRS` parity + harness §26Z |

## Files Created

| File | Description |
|------|-------------|
| `.cursor/model-catalog.local.example.json` | Example local catalog schema |
| `scripts/model_tier_lib.py` | Resolver library with tier→alias mapping + catalog validation |
| `scripts/model_tier_validate.py` | CLI validator for tier enum, catalog schema, phase keys, forbidden slugs |
| `template/.cursor/model-catalog.local.example.json` | Template copy of catalog example |
| `template/scripts/model_tier_lib.py` | Template copy of resolver library |
| `template/scripts/model_tier_validate.py` | Template copy of CLI validator |

## Files Modified

| File | Changes |
|------|---------|
| `.cursor/scratchpad.md` | Added MODEL_TIER_*, MODEL_CATALOG, MODEL_RESOLVE, MODEL_FALLBACK, MODEL_PROVIDER_MODE keys |
| `.cursor/scratchpad.local.example.md` | Mirrored scratchpad changes |
| `.cursor/agents/curator.mdc` | Added `model: fast` |
| `.cursor/agents/po.mdc` | Added `model: inherit` |
| `.cursor/agents/release.mdc` | Added `model: inherit` |
| `template/.cursor/agents/curator.mdc` | Added `model: fast` |
| `template/.cursor/agents/po.mdc` | Added `model: inherit` |
| `template/.cursor/agents/release.mdc` | Added `model: inherit` |
| `.gitignore` | Added `.cursor/model-catalog.local.json` |
| `template/.gitignore` | Added `.cursor/model-catalog.local.json` |
| `docs/engineering/runbook.md` | Added model tier section, provider mode, non-substitution paragraph, reason codes |
| `template/docs/engineering/runbook.md` | Template copy of runbook |
| `tests/auto_command_contract_test.py` | Added 8 `test_us0101_*` contract tests |
| `scripts/check_intake_template_parity.py` | Added `MODEL_TIER_PAIRS` + `--scope=model-tier` |
| `template/scripts/check_intake_template_parity.py` | Template copy of parity checker |
| `tests/run-tests.ps1` | Added §26Z harness section |
| `template/.cursor/scratchpad.md` | Template copy of scratchpad |
| `template/.cursor/scratchpad.local.example.md` | Template copy of scratchpad example |

## Test Results

```
tests/auto_command_contract_test.py -k us0101
8 passed, 135 deselected in 0.07s
```

- `test_us0101_scratchpad_keys` — PASS
- `test_us0101_default_matrix_literals` — PASS
- `test_us0101_token_profile_orthogonality` — PASS
- `test_us0101_template_agent_model_aliases` — PASS
- `test_us0101_forbidden_slug_grep` — PASS
- `test_us0101_catalog_schema_contract` — PASS
- `test_us0101_provider_mode_literals` — PASS
- `test_us0101_reason_code_inventory` — PASS

## Execution Order

Recommended execution follows tranche ordering (A→E):

1. **Tranche A** (T-001, T-002): Establish scratchpad contract and default matrix
2. **Tranche B** (T-003, T-004): Apply template defaults and create catalog example
3. **Tranche C** (T-005, T-006): Build resolver library and validator
4. **Tranche D** (T-007, T-008): Document provider mode and orthogonality
5. **Tranche E** (T-009, T-010): Implement contract tests and parity harness

## Handoff

- **From**: Tech Lead (sprint-plan)
- **To**: Dev (execute)
- **Next Phase**: `/plan-verify` (fresh QA) — verify AC-1..AC-9 surjective coverage via T-001..T-010
