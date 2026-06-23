# QA Findings — Sprint S0091 / US-0101

## Summary

**Verdict**: **PASS**
**Story**: US-0101 — Per-phase model tier selection for subagents
**Decision**: DEC-0086 (locked)
**Sprint**: S0091
**Phase**: qa
**Timestamp**: 2026-06-15T23:00:00Z
**Fresh Context Marker**: `qa-US0101-qa-20260615T230000Z-fresh`
**Orchestrator Run**: `auto-20260615-02`

---

## AC Verification Results

### AC-1: Scratchpad tier contract — PASS

**Evidence**: `.cursor/scratchpad.md` lines 327-349 contain all required keys:
- `MODEL_TIER_DEFAULT=balanced`
- `MODEL_TIER_<PHASE>` documented with per-phase override semantics
- `MODEL_CATALOG=.cursor/model-catalog.local.json`
- `MODEL_RESOLVE=alias_only`
- `MODEL_FALLBACK=inherit`
- `MODEL_PROVIDER_MODE=cursor`

Non-substitution paragraph present: `MODEL_TIER ≠ TOKEN_PROFILE ≠ DELIVERY_MODE`.
Template parity: `.cursor/scratchpad.local.example.md` mirrors scratchpad.
Contract test: `test_us0101_scratchpad_keys` **PASS**.

### AC-2: Default phase→tier matrix — PASS

**Evidence**: Architecture-locked matrix documented in:
- `.cursor/scratchpad.md` lines 333-337 (comment block)
- `docs/engineering/architecture.md` lines 2702-2709 (# US-0101 section)
- `docs/engineering/runbook.md` lines 668-675

Matrix matches DEC-0086 locked table:
- `cheap`: ask, refresh-context, memory-audit, status-reconcile, pause
- `balanced`: intake, discovery, research, release, plan-verify
- `strong`: architecture, execute, quick, qa, verify-work, security-review
- `auto`: inherits parent (no tier override)

Contract test: `test_us0101_default_matrix_literals` **PASS**.

### AC-3: Tier→Cursor alias resolution — PASS

**Evidence**: Tier→alias mapping implemented in `scripts/model_tier_lib.py`:
- `TIER_ALIAS_MAP`: cheap→fast, balanced→inherit, strong→None (omit)
- `resolve_model_tier()` implements DEC-0086 §3 resolver algorithm (7 steps)
- `DEFAULT_PHASE_TIER_MATRIX` contains all 17 canonical phases

Documented in DEC-0086 §2 and architecture.md lines 2711-2719.

### AC-4: Local model catalog — PASS

**Evidence**:
- `.cursor/model-catalog.local.example.json` exists with schema_version=1, tiers object with cheap/balanced/strong keys
- `.gitignore` line 14: `.cursor/model-catalog.local.json` (gitignored)
- `template/.gitignore` line 7: `.cursor/model-catalog.local.json` (template parity)
- `scripts/model_tier_lib.py` implements `validate_catalog_schema()` and `load_catalog()`
- `scripts/model_tier_validate.py` validates catalog schema via CLI

Contract test: `test_us0101_catalog_schema_contract` **PASS**.

### AC-5: Agent template defaults — PASS

**Evidence**: Template agent `model:` fields verified:

| Agent | Tier | `model:` field | File |
|-------|------|----------------|------|
| curator | cheap | `model: fast` | `template/.cursor/agents/curator.mdc` line 3 |
| po | balanced | `model: inherit` | `template/.cursor/agents/po.mdc` line 3 |
| release | balanced | `model: inherit` | `template/.cursor/agents/release.mdc` line 3 |
| tech-lead | strong | *(omit)* | `template/.cursor/agents/tech-lead.mdc` — no `model:` field |
| dev | strong | *(omit)* | `template/.cursor/agents/dev.mdc` — no `model:` field |
| qa | strong | *(omit)* | `template/.cursor/agents/qa.mdc` — no `model:` field |
| security | strong | *(omit)* | `template/.cursor/agents/security.mdc` — no `model:` field |

Active agents (`.cursor/agents/`) mirror template defaults.
No forbidden vendor slugs (`composer-`, `claude-`, `gpt-`, `opus-`) in any `template/.cursor/agents/*.mdc`.

Contract tests: `test_us0101_template_agent_model_aliases` **PASS**, `test_us0101_forbidden_slug_grep` **PASS**.

### AC-6: Provider mode runbook — PASS

**Evidence**: `docs/engineering/runbook.md` lines 653-767 contain:
- Model tier section with key table (lines 659-666)
- Default phase→tier matrix (lines 668-675)
- Provider mode subsection `MODEL_PROVIDER_MODE=cursor|api` (lines 677-697)
- BYOK limitation: subagents do NOT inherit custom API keys/base URLs (lines 684-687)
- Workaround recipes: parent model + inherit, manual phase runs, local catalog override (lines 689-697)
- Non-substitution paragraph: `MODEL_TIER ≠ TOKEN_PROFILE ≠ DELIVERY_MODE` (lines 699-708)
- Explicit statement: "These are **independent axes** — none substitutes for another" (line 706)

Template parity: `template/docs/engineering/runbook.md` mirrors active runbook.

Contract tests: `test_us0101_token_profile_orthogonality` **PASS**, `test_us0101_provider_mode_literals` **PASS**.

### AC-7: Validator + reason codes — PASS

**Evidence**:
- `scripts/model_tier_validate.py` — CLI validator with:
  - Tier enum validation (`validate_tier_enum()`)
  - Catalog schema validation (`validate_catalog()`)
  - Phase key spelling validation (`validate_phase_key()`)
  - Forbidden vendor slug grep (`check_forbidden_slugs_in_file()`, `check_template_agents()`)
- All 4 reason codes present in both `model_tier_lib.py` and `model_tier_validate.py`:
  - `MODEL_TIER_INVALID` — unknown tier value
  - `MODEL_CATALOG_INVALID` — malformed catalog JSON
  - `MODEL_SLUG_UNKNOWN` — tier key missing from catalog
  - `MODEL_RESOLVE_FALLBACK` — catalog lookup failed, using fallback
- Self-test: `python scripts/model_tier_lib.py --self-test` → `[MODEL_TIER_SELF_TEST_OK]`
- Full validation: `python scripts/model_tier_validate.py --repo .` → `[MODEL_TIER_VALIDATION_OK]`

Contract test: `test_us0101_reason_code_inventory` **PASS**.

### AC-8: Contract tests + parity — PASS

**Evidence**: Eight `test_us0101_*` contract tests in `tests/auto_command_contract_test.py` lines 2689-2800:

```
pytest tests/auto_command_contract_test.py -k us0101 -v
8 passed, 135 deselected in 0.08s
```

| Test | AC | Status |
|------|-----|--------|
| `test_us0101_scratchpad_keys` | AC-1 | PASS |
| `test_us0101_default_matrix_literals` | AC-2 | PASS |
| `test_us0101_token_profile_orthogonality` | AC-6 | PASS |
| `test_us0101_template_agent_model_aliases` | AC-5 | PASS |
| `test_us0101_forbidden_slug_grep` | AC-5 | PASS |
| `test_us0101_catalog_schema_contract` | AC-4 | PASS |
| `test_us0101_provider_mode_literals` | AC-6 | PASS |
| `test_us0101_reason_code_inventory` | AC-7 | PASS |

Parity: `python scripts/check_intake_template_parity.py --scope=model-tier` → `[INTAKE_TEMPLATE_PARITY_OK]`

### AC-9: Architecture + decision anchor — PASS

**Evidence**:
- Architecture anchor: `docs/engineering/architecture.md` line 2671 `# US-0101: Per-phase model tier selection for subagents (MODEL_TIER + local catalog)` — self-contained summary with tier contract, resolution chain, catalog schema, template defaults, provider mode, reason codes
- Decision anchor: `decisions/DEC-0086.md` (locked) — normative statement with 10 sections
- `MODEL_TIER_PAIRS` parity in `scripts/check_intake_template_parity.py` lines 231-238
- Harness §26Z in `tests/run-tests.ps1` lines 1615-1621 (parity + self-test + contract tests)
- Research anchor: `R-0088` (closed)

---

## Additional Verification

### Self-test
```
python scripts/model_tier_lib.py --self-test
[SELF-TEST] Validating model_tier_lib contract...
[MODEL_TIER_SELF_TEST_OK]
```

### Full validation
```
python scripts/model_tier_validate.py --repo .
[REPO] Validating C:\flowGit\sonstiges\gsd_cursor...
[CATALOG] Validating .cursor\model-catalog.local.example.json...
[SCRATCHPAD] Validating .cursor\scratchpad.md...
[TEMPLATE] Checking template\.cursor\agents...
[MODEL_TIER_VALIDATION_OK]
```

### Parity check
```
python scripts/check_intake_template_parity.py --scope=model-tier
[INTAKE_TEMPLATE_PARITY_OK] scope=model-tier
```

---

## Blocking Findings

**None.**

---

## Non-blocking Observations

1. Template parity is complete — all active files have corresponding template copies.
2. AC surjective coverage confirmed — every AC (AC-1 through AC-9) is covered by at least one task.
3. US-0101 remains OPEN in `docs/product/backlog.md` (authority) — status not flipped per US-0045.

---

## Handoff

**Next Phase**: `/verify-work` (fresh QA subagent)
**QA Verdict**: **PASS** — all 9 ACs satisfied, 8/8 contract tests passing, zero blocking findings.
