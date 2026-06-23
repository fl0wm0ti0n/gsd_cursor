# Release Notes — S0091 / US-0101

## Per-phase model tier selection for subagents

**Sprint**: S0091
**Story**: US-0101
**Decision**: DEC-0086 (locked)
**Research**: R-0088 (closed)
**Release date**: 2026-06-16T00:00:00Z
**Orchestrator run**: auto-20260615-02
**Verdict**: PASS

## Summary

Delivered per-phase model tier selection for its-magic subagents. Operators can now configure LLM model strength per lifecycle phase via stable Cursor aliases (`fast`, `inherit`, omit) instead of hardcoding volatile vendor slugs in template agent files. Ships `MODEL_TIER` scratchpad controls (`cheap | balanced | strong`), a default phase→tier matrix, template agent defaults using aliases only, optional `.cursor/model-catalog.local.json` for operator-maintained slug maps, and runbook guidance for `MODEL_PROVIDER_MODE=cursor|api`. Orthogonal to `TOKEN_PROFILE` (DEC-0062 / US-0080).

## Tasks Delivered (10/10)

| Task | Tranche | AC | Description |
|------|---------|-----|-------------|
| T-001 | A | AC-1 | Scratchpad keys — `MODEL_TIER_*`, `MODEL_CATALOG`, `MODEL_RESOLVE`, `MODEL_FALLBACK`, `MODEL_PROVIDER_MODE` |
| T-002 | A | AC-2 | Default phase→tier matrix documented in scratchpad comments + runbook |
| T-003 | B | AC-5 | Template agent `model:` defaults — curator→fast, po/release→inherit, others→omit |
| T-004 | B | AC-4 | `.cursor/model-catalog.local.example.json` + gitignore |
| T-005 | C | AC-4, AC-7 | `scripts/model_tier_lib.py` — resolver + catalog validation + 4 reason codes |
| T-006 | C | AC-7 | `scripts/model_tier_validate.py` — CLI validator |
| T-007 | D | AC-6 | Runbook provider-mode subsection (`MODEL_PROVIDER_MODE=cursor\|api`) |
| T-008 | D | AC-6 | Non-substitution paragraph (`MODEL_TIER ≠ TOKEN_PROFILE ≠ DELIVERY_MODE`) |
| T-009 | E | AC-8 | Eight `test_us0101_*` contract tests (8/8 passing) |
| T-010 | E | AC-8, AC-9 | `MODEL_TIER_PAIRS` parity + harness §26Z |

## DEC-0086 Locked Decisions

- L1: Tier enum `cheap | balanced | strong`
- L2: Default phase→tier matrix
- L3: Tier→alias resolution (`cheap`→`fast`, `balanced`→`inherit`, `strong`→omit)
- L4: Local catalog JSON schema + gitignore
- L5: Template agent defaults (aliases only, no vendor slugs)
- L6: Provider-mode runbook (`cursor` vs `api`)
- L7: Scratchpad merge precedence (local > materialized > example)
- L8: Orthogonality vs TOKEN_PROFILE
- L9: Fail-closed reason code family
- L10: Contract test inventory
- L11: `check_intake_template_parity.py --scope=model-tier`
- L12: Compose with DEC-0062 without amending TOKEN_PROFILE

## Contract Tests (8/8 PASS)

1. `test_us0101_scratchpad_keys` — PASS
2. `test_us0101_default_matrix_literals` — PASS
3. `test_us0101_token_profile_orthogonality` — PASS
4. `test_us0101_template_agent_model_aliases` — PASS
5. `test_us0101_forbidden_slug_grep` — PASS
6. `test_us0101_catalog_schema_contract` — PASS
7. `test_us0101_provider_mode_literals` — PASS
8. `test_us0101_reason_code_inventory` — PASS

## Files Created

- `.cursor/model-catalog.local.example.json`
- `scripts/model_tier_lib.py`
- `scripts/model_tier_validate.py`
- `template/.cursor/model-catalog.local.example.json`
- `template/scripts/model_tier_lib.py`
- `template/scripts/model_tier_validate.py`

## Files Modified

- `.cursor/scratchpad.md`, `.cursor/scratchpad.local.example.md`
- `.cursor/agents/curator.mdc`, `.cursor/agents/po.mdc`, `.cursor/agents/release.mdc`
- `template/.cursor/agents/curator.mdc`, `template/.cursor/agents/po.mdc`, `template/.cursor/agents/release.mdc`
- `.gitignore`, `template/.gitignore`
- `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
- `tests/auto_command_contract_test.py`
- `scripts/check_intake_template_parity.py`, `template/scripts/check_intake_template_parity.py`
- `tests/run-tests.ps1`
- `template/.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`

## Gate Chain

- plan-verify: PASS
- execute: PASS
- qa: PASS
- verify-work: PASS
- release: PASS

## Runtime Proof

- `runtime_proof_id=rp-auto-20260615-02-release-release-20260616T000000Z-S0091-US0101`
- `proof_hash=5637ab7eed0032d93af7c7057b2221d000030216463915fcf64645fcbb76c26e`
