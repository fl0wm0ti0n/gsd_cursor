# Sprint S0112 — Ship model-catalog example presets on install/upgrade

- **story_id**: US-0112
- **orchestrator_run_id**: auto-20260628-04
- **dec_id**: DEC-0112 (Accepted)
- **research_anchor**: R-0090 (delivered, Q1–Q8 closed)
- **status**: PLANNED
- **timestamp**: 2026-06-30T22:30:00Z
- **fresh_context_marker**: tl-US0112-sprintplan-20260630T223000Z-fresh
- **delivery_mode**: standard
- **native_chain_active**: true
- **SPRINT_MAX_TASKS**: 12
- **task_count**: 11 (within threshold; no split)

## Overview

Close the operator gap after US-0101 / US-0102 / DEC-0086 / DEC-0087 where eight committed `template/.cursor/model-catalog.local.example*.json` presets (base, cursor-only, level 1–4, role-based balanced/highend) exist and are documented in scratchpad comments but `installer-owned-paths.manifest` omits them — so `missing` and `upgrade` installs do not copy examples into consumer `.cursor/` repos.

- **Classification**: 8 `model-catalog.local.example*.json` files as **framework files**
- **Missing mode**: copy when absent (same semantics as `scratchpad.local.example.md`)
- **Upgrade mode**: refresh when template differs, skip when unchanged (US-0075 / US-0018 / US-0057 precedent)
- **Active catalog protection**: `.cursor/model-catalog.local.json` remains gitignored and OUTSIDE manifest `install_include_paths` and `clean_paths`; installer NEVER copies examples to that path automatically

## Compose guards (non-negotiable — DO NOT amend)

| Story | Status | Reason |
|-------|--------|--------|
| US-0008 | Read-only | Installer manifest-driven copy semantics unchanged |
| US-0018 | Compose | Smart upgrade framework rules reused |
| US-0040 | Read-only | Per-sprint release notes semantics unchanged |
| US-0054 | Read-only | Configurable release publishing unchanged |
| US-0057 | Compose | Framework file refresh semantics reused |
| US-0075 | Compose | Framework file refresh semantics reused |
| US-0100 | Read-only | Semantic changelog unchanged |
| US-0101 | Read-only | Catalog schema unchanged (DEC-0086) |
| US-0102 | Read-only | Role catalog precedence unchanged (DEC-0087) |
| US-0103 | Read-only | Ledger semantics unchanged |
| US-0107 | Read-only | Daemon loop semantics unchanged |
| US-0110 | Read-only | Goal convergence semantics unchanged |

## Task list (T-001..T-011, 11 tasks, within SPRINT_MAX_TASKS=12)

### Tranche A (manifest + architecture)

- **T-001** (AC-1): Add 8 `model-catalog.local.example*.json` rows to active `docs/engineering/context/installer-owned-paths.manifest` under `[install_include_paths]`
- **T-002** (AC-1): Mirror manifest rows in `template/docs/engineering/context/installer-owned-paths.manifest` (byte-parity; 16 rows total)
- **T-010** (AC-8): Architecture notes already locked at `docs/engineering/architecture.md # US-0112` — verify at `/execute`

### Tranche B (triple installer verify)

- **T-003** (AC-2, AC-5): Verify missing-mode `installer.py` logic adds absent framework files
- **T-004** (AC-2, AC-5): Verify missing-mode `installer.ps1` logic adds absent framework files
- **T-005** (AC-2, AC-5): Verify missing-mode `installer.sh` logic adds absent framework files
- **T-006** (AC-3, AC-4): Verify upgrade-mode logic refreshes stale framework files, skips unchanged, never touches active `model-catalog.local.json`

### Tranche C (parity + runbook)

- **T-007** (AC-5): Implement `check_intake_template_parity.py --scope=model-catalog-examples` with `MODEL_CATALOG_EXAMPLE_PAIRS` constant
- **T-008** (AC-6): Write runbook §model-catalog preset recipe (operator copies one preset to active catalog)

### Tranche D (tests + parity)

- **T-009** (AC-7): Write 8+ `test_us0112_*` contract test markers
- **T-011** (AC-8): Verify template parity for all touched files

## AC surjective map (AC-1..AC-8 → T-001..T-011)

| AC | Tasks |
|----|-------|
| AC-1 (Manifest completeness) | T-001, T-002 |
| AC-2 (Missing mode delivery) | T-003, T-004, T-005 |
| AC-3 (Upgrade framework refresh) | T-006 |
| AC-4 (Active catalog protection) | T-006 |
| AC-5 (Triple installer parity) | T-003, T-004, T-005, T-007 |
| AC-6 (Runbook operator recipe) | T-008 |
| AC-7 (Contract tests + parity) | T-009 |
| AC-8 (Architecture notes) | T-010, T-011 |

## Test markers (12 markers, 8+)

| Marker | Coverage |
|--------|----------|
| test_us0112_manifest_lists_eight_paths_active | AC-1 |
| test_us0112_manifest_lists_eight_paths_template | AC-1 |
| test_us0112_missing_mode_adds_absent_framework_files_python | AC-2, AC-5 |
| test_us0112_missing_mode_adds_absent_framework_files_ps1 | AC-2, AC-5 |
| test_us0112_missing_mode_adds_absent_framework_files_shell | AC-2, AC-5 |
| test_us0112_upgrade_mode_refreshes_stale_framework_files | AC-3 |
| test_us0112_upgrade_mode_preserves_unchanged_files | AC-3 |
| test_us0112_upgrade_mode_never_touches_local_catalog | AC-4 |
| test_us0112_active_catalog_protection_invariant | AC-4 |
| test_us0112_triple_installer_parity_eight_examples | AC-5 |
| test_us0112_runbook_lists_eight_preset_literals | AC-6 |
| test_us0112_parity_scope_model_catalog_examples | AC-7 |

## Parity scope

- **scope**: `model-catalog-examples`
- **constant**: `MODEL_CATALOG_EXAMPLE_PAIRS`
- **pair count**: 16 (8 active + 8 template byte-parity rows)

## Top risks

| ID | Risk | Mitigation |
|----|------|------------|
| R1 | Stale upgrade when example filename changes | Deterministic manifest list + idempotent upgrade copy |
| R2 | Operator confusion if all 8 land but none selected | Runbook recipe mandatory |
| R3 | Active catalog accidental install | Manifest exclusion invariant + regression guard test |
| R4 | Triple installer drift | Single manifest source of truth; parity test |
| R5 | npm `package.json` files gap | Covered by `template/` glob; verify at /execute |
| R6 | US-0075 / US-0018 precedence | Same framework-file semantics; additive only |

## Next phase

- **/plan-verify** (fresh QA subagent spawn)
- Validates AC surjective map, task list, parity scope, and compose guards
- Composes with compose-boundary validation

---

Issued: 2026-06-30T22:30:00Z
Phase ID: sprint-plan
Role: tech-lead
Orchestrator Run ID: auto-20260628-04
Runtime Proof ID: rp-auto-20260628-04-sprintplan-tech-lead-20260630T223000Z-US0112
