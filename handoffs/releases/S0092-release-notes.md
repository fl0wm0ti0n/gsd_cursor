# Release Notes — S0092 / US-0102 (direct per-phase model slug override)

- **sprint_id**: S0092
- **story_refs**: US-0102
- **release_name**: `S0092 — US-0102 direct per-phase model slug override and role-based catalog presets`
- **release_date**: 2026-06-26T00:00:00Z
- **orchestrator_run_id**: auto-20260615-02
- **verdict**: **PASS**
- **binding_decision**: `DEC-0087`
- **composes**: `US-0101` / `DEC-0086` (unchanged)

## Summary

Extends **US-0101** tier-based model selection with **direct per-phase vendor slug override** (`MODEL_<PHASE>=<slug>`) and optional **role-based catalog presets** (catalog schema v2). The 3-tier baseline remains the default/fallback: precedence `MODEL_<PHASE>` > `MODEL_TIER_<PHASE>` > `role_catalog` (when `MODEL_RESOLVE=role_catalog`) > `MODEL_TIER_DEFAULT` > Cursor alias. Backward compatible — tier-only and v1 catalog configurations unchanged. `/ask` phase reinforced with `MODEL_ASK` direct override.

## What's new

- **Direct override scratchpad keys (AC-1, AC-5)** — `MODEL_<PHASE>` including `MODEL_ASK`; precedence documented in scratchpad + template mirrors.
- **Unified resolver (AC-2, AC-4, AC-6)** — `resolve_model_for_phase()` in `scripts/model_tier_lib.py` with 5-step precedence chain.
- **Catalog schema v2 (AC-3)** — optional `roles` section (`po`, `sa`, `dev`, `dev_difficult`, `qa`, `security`, `release`); v1 catalogs still valid.
- **Role-based examples (AC-3, AC-7)** — `.cursor/model-catalog.local.example.role-based-balanced.json`, `.cursor/model-catalog.local.example.role-based-highend.json` (placeholder slugs only).
- **Validator extensions (AC-8)** — `MODEL_OVERRIDE_SLUG_UNKNOWN`, `MODEL_ROLE_SLUG_UNKNOWN`, `MODEL_CATALOG_SCHEMA_V2_INVALID`.
- **Contract tests + parity (AC-9)** — eight `test_us0102_*` subtests; `MODEL_TIER_OVERRIDES_PAIRS`; harness **§26AA**; `--scope=model-tier-overrides`.
- **Documentation (AC-10)** — runbook § US-0102; architecture `# US-0102`; `MODEL_RESOLVE=alias_only|local_catalog|role_catalog`.

## Tasks Delivered (11/11)

| Task | Tranche | AC | Description |
|------|---------|-----|-------------|
| T-001 | A | AC-1, AC-5 | `MODEL_<PHASE>` scratchpad keys + `MODEL_ASK` |
| T-002 | A | AC-10 | `MODEL_RESOLVE` enum + 5-step precedence comments |
| T-003 | B | AC-3, AC-7 | Catalog v2 role-based example JSON files |
| T-004 | B | AC-7 | Template stability — tier-only primary; no vendor slugs |
| T-005 | C | AC-2, AC-4, AC-6 | `resolve_model_for_phase()` unified resolver |
| T-006 | C | AC-3, AC-8 | Catalog v2 validation + `MODEL_CATALOG_SCHEMA_V2_INVALID` |
| T-007 | C | AC-8 | `model_tier_validate.py` extensions + three reason codes |
| T-008 | D | AC-10 | Runbook US-0102 operator subsection |
| T-009 | E | AC-9 | Eight `test_us0102_*` contract subtests |
| T-010 | E | AC-9 | `MODEL_TIER_OVERRIDES_PAIRS` parity scope |
| T-011 | E | AC-9 | Harness §26AA |

## DEC-0087 Locked Decisions

- Compose **DEC-0086** — do not amend US-0101 / tier baseline
- 5-step precedence: direct slug > tier > role_catalog > default > alias
- Extend `model_tier_lib.py` in place (no separate overrides module)
- Catalog schema v2 optional `roles`; v1 backward compatible
- Template files: placeholder slugs only; operator slugs in gitignored local files
- Eight `test_us0102_*` contract markers + `--scope=model-tier-overrides` parity

## Contract Tests (8/8 PASS)

1. `test_us0102_direct_override_keys` — PASS
2. `test_us0102_precedence_chain` — PASS
3. `test_us0102_catalog_schema_v2` — PASS
4. `test_us0102_role_catalog_resolver` — PASS
5. `test_us0102_tier_only_backward_compat` — PASS
6. `test_us0102_no_vendor_slugs_in_template` — PASS
7. `test_us0102_reason_codes` — PASS
8. `test_us0102_ask_phase_reinforcement` — PASS

## Run

- **start_command**: `pytest -k us0102 tests/auto_command_contract_test.py -v`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md` § **Per-phase model slug override (US-0102 / DEC-0087)**

## Connect

- **service_url**: N/A (framework configuration layer; no app runtime)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `pytest -k us0102 tests/auto_command_contract_test.py -v` → expect **8 passed**.
2. `pytest -k us0101 tests/auto_command_contract_test.py -v` → expect **8 passed** (backward compat).
3. `python scripts/model_tier_validate.py --repo .` → expect `[MODEL_TIER_VALIDATION_OK]`.
4. `python scripts/check_intake_template_parity.py --scope=model-tier-overrides` → expect `[INTAKE_TEMPLATE_PARITY_OK]`.
5. `python scripts/model_tier_lib.py --self-test` → expect **PASS**.
6. Confirm `sprints/S0092/uat.json` **10/10 PASS** and `sprints/S0092/qa-findings.md` **PASS** (0 blockers).
7. Confirm release-queue row **`S0092`** is **`released`** and backlog / acceptance show **`US-0102`** = **DONE** / checked.
8. Confirm `.cursor/scratchpad.local.md` examples document `MODEL_<PHASE>` keys (operator-local; no vendor slugs in `template/`).

- **expected_health_signal**: Contract tests green; validator OK; **`US-0102`** surfaces as **DONE** in backlog and checked in acceptance; tier-only configs unchanged.

## Credentials

- Env-reference-only policy in effect. Operator model slugs belong in `.cursor/scratchpad.local.md` and `.cursor/model-catalog.local.json` (gitignored) — never in template files.

## Test evidence summary

- **Contract subtests**: `pytest -k "us0102 or us0101"` → **16 passed** (release gate re-run).
- **Validator**: `[MODEL_TIER_VALIDATION_OK]`.
- **Template parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=model-tier-overrides.
- **UAT**: **10/10 PASS** (`sprints/S0092/uat.json`).

## Governance references

- **DEC-0087** — precedence chain, catalog v2, resolver extensions.
- **`docs/engineering/architecture.md`** `# US-0102`.
- **`decisions/DEC-0087.md`**.

## Known Issues

- None blocking release for in-scope **US-0102** / **DEC-0087** delivery.
- **readme_feature_coverage_3f**: post-**S0077** portfolio drift on **`its_magic/README.md`** family — kit-repo observation per **S0085**–**S0090** precedent (disjoint from **US-0102** closure).

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (us0102 8/8 + us0101 8/8) |
| qa | pass (no blockers) |
| uat | pass (10/10) |
| isolation | pass (execute+qa+verify-work distinct markers) |
| strict_proof | pass |
| parity | pass (scope=model-tier-overrides) |
| readme_feature_coverage_3f | observation (post-S0077 drift; kit-repo) |
| project_readme_coverage_3g | pass (kit_repo_skipped) |
| version_doc_19 | pass ([Unreleased] append) |
| publish | skipped (RELEASE_PUBLISH_MODE=disabled) |
| finalization | pass |

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260615-02-release-release-20260626T000000Z-S0092-US0102`
- `proof_hash=18d3bed52733e0325eac9068b5aa61f07a97153791217d1e23e4e62663e0b858`
- `fresh_context_marker=release-S0092-US0102-release-20260626T000000Z-fresh`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=disabled`; `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`.
- **Publish**: `RELEASE_PUBLISH_MODE=disabled` → `publish_snapshot=skipped_disabled` (deterministic no-op).

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **4** remaining.
