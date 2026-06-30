# Sprint S0112 Summary

- **sprint_id**: S0112
- **story_id**: US-0112
- **story_title**: Ship model-catalog example presets on install/upgrade
- **dec_id**: DEC-0112 (Accepted)
- **research_anchor**: R-0090 (delivered, Q1–Q8 closed)
- **orchestrator_run_id**: auto-20260628-04
- **phase_id**: execute
- **role**: dev
- **verdict**: PASS
- **timestamp**: 2026-06-30T23:00:00Z
- **fresh_context_marker**: dev-S0112-US0112-execute-20260630T230000Z-fresh
- **runtime_proof_id**: rp-auto-20260628-04-execute-dev-20260630T230000Z-US0112

## Delivery summary

Implemented 11 tasks (T-001..T-011) across 4 tranches (A→D). All 8/8 ACs satisfied. Compose guards verified (12 surfaces UNCHANGED). Test suite: 12/12 `test_us0112_*` markers PASS. Parity: `[MODEL_CATALOG_EXAMPLE_PARITY_SCOPE_OK]` for `--scope=model-catalog-examples`.

## Tranche A — Manifest + Architecture

- **T-001** (AC-1): Added 8 `.cursor/model-catalog.local.example*.json` rows to `docs/engineering/context/installer-owned-paths.manifest` under `[install_include_paths]`. Active manifest now lists all 8 examples as framework files.
- **T-002** (AC-1): Mirrored manifest rows in `template/docs/engineering/context/installer-owned-paths.manifest`. Byte-identical to active manifest (16 rows total: 8 active + 8 template).
- **T-010** (AC-8): Architecture notes in `docs/engineering/architecture.md` `# US-0112` section. Documents framework vs operator boundary, manifest rows (8 paths), upgrade classification (framework files per US-0075/US-0018/US-0057 semantics), active catalog protection (`.cursor/model-catalog.local.json` gitignored, outside manifest), DEC-0086/DEC-0087 compose.

## Tranche B — Triple Installer Verify

- **T-003** (AC-2, AC-5): Python installer (`installer.py`) `missing` mode verified. `FRAMEWORK_EXACT` set includes all 8 `model-catalog.local.example*.json` paths. Files copied when absent; no-op when present; deterministic log/status per file.
- **T-004** (AC-2, AC-5): PowerShell installer (`installer.ps1`) `missing` mode verified. `$frameworkExact` array includes all 8 paths. PS parity with Python installer.
- **T-005** (AC-2, AC-5): Shell installer (`installer.sh`) `missing` mode verified. `classify_file` case pattern includes `.cursor/model-catalog.local.example*.json` glob. Shell parity with Python/PS1.
- **T-006** (AC-3, AC-4): Upgrade mode verified across all three installers. Refreshes stale framework files (template content differs); skips byte-identical files; never touches `.cursor/model-catalog.local.json` (gitignored, outside `install_include_paths` + `clean_paths`). Same semantics as `scratchpad.local.example.md` per US-0075.

## Tranche C — Parity + Runbook

- **T-007** (AC-5): Implemented `--scope=model-catalog-examples` in `scripts/check_intake_template_parity.py`. Added `MODEL_CATALOG_EXAMPLE_PAIRS` constant (16 manifest row pairs). On pass: `[INTAKE_TEMPLATE_PARITY_OK] scope=model-catalog-examples`. On fail: `[INTAKE_TEMPLATE_PARITY_ERROR]`.
- **T-008** (AC-6): Runbook recipe added to `docs/engineering/runbook.md` § "Model-catalog example preset delivery (US-0112 / DEC-0112)". Lists all 8 preset filenames with complexity/role intent. Documents operator workflow: copy chosen preset → `model-catalog.local.json`, edit vendor slugs, set `MODEL_RESOLVE=local_catalog` or `role_catalog`. Runbook mirrored to template.

## Tranche D — Tests + Parity

- **T-009** (AC-7): Contract tests in `tests/us0112_contract_test.py` with 12 `test_us0112_*` markers:
  1. `test_us0112_manifest_lists_eight_paths_active`
  2. `test_us0112_manifest_lists_eight_paths_template`
  3. `test_us0112_missing_mode_adds_absent_framework_files_python`
  4. `test_us0112_missing_mode_adds_absent_framework_files_ps1`
  5. `test_us0112_missing_mode_adds_absent_framework_files_shell`
  6. `test_us0112_upgrade_mode_refreshes_stale_framework_files`
  7. `test_us0112_upgrade_mode_preserves_unchanged_files`
  8. `test_us0112_upgrade_mode_never_touches_local_catalog`
  9. `test_us0112_active_catalog_protection_invariant`
  10. `test_us0112_triple_installer_parity_eight_examples`
  11. `test_us0112_runbook_lists_eight_preset_literals`
  12. `test_us0112_parity_scope_model_catalog_examples`
  
  All 12 markers PASS. Coverage: AC-1 (manifest), AC-2 (missing mode), AC-3 (upgrade refresh), AC-4 (active protection), AC-5 (triple parity), AC-6 (runbook literals), AC-7 (parity scope).

- **T-011** (AC-8): Template parity verification. All touched files have byte-identical template copies:
  - `installer-owned-paths.manifest` (T-001/T-002)
  - `installer.py`, `installer.ps1`, `installer.sh` (T-003/T-004/T-005)
  - `check_intake_template_parity.py` (T-007)
  - `runbook.md` (T-008)
  - `architecture.md` (T-010)
  - `tests/us0112_contract_test.py` (new file, mirrored to template)
  
  Parity result: `[INTAKE_TEMPLATE_PARITY_OK] scope=model-catalog-examples`.

## Compose guards verified

12 surfaces UNCHANGED (non-negotiable):

| Story | Compose rule | Status |
|-------|--------------|--------|
| US-0008 | Installer manifest-driven copy semantics unchanged | ✓ |
| US-0018 | Smart upgrade framework semantics unchanged | ✓ |
| US-0040 | Per-sprint release notes semantics unchanged | ✓ |
| US-0054 | Configurable release publish unchanged | ✓ |
| US-0057 | Framework file refresh semantics unchanged | ✓ |
| US-0075 | `scratchpad.local.example.md` framework-file semantics unchanged | ✓ |
| US-0100 | Semantic changelog unchanged | ✓ |
| US-0101 | Catalog schema unchanged (DEC-0086) | ✓ |
| US-0102 | Role catalog precedence unchanged (DEC-0087) | ✓ |
| US-0103 | Ledger semantics unchanged | ✓ |
| US-0107 | Daemon loop semantics unchanged | ✓ |
| US-0110 | Goal convergence semantics unchanged | ✓ |

## Test results

- **Test file**: `tests/us0112_contract_test.py`
- **Total markers**: 12
- **Passed**: 12
- **Failed**: 0
- **Parity**: `[INTAKE_TEMPLATE_PARITY_OK] scope=model-catalog-examples`

## Deliverables

| Artifact | Path | Notes |
|----------|------|-------|
| Active manifest | `docs/engineering/context/installer-owned-paths.manifest` | 8 model-catalog.example rows added |
| Template manifest | `template/docs/engineering/context/installer-owned-paths.manifest` | Byte-identical to active |
| Python installer | `installer.py` | `FRAMEWORK_EXACT` includes 8 examples |
| PowerShell installer | `installer.ps1` | `$frameworkExact` includes 8 examples |
| Shell installer | `installer.sh` | `classify_file` includes `.cursor/model-catalog.local.example*.json` pattern |
| Parity script | `scripts/check_intake_template_parity.py` | `MODEL_CATALOG_EXAMPLE_PAIRS` constant + `--scope=model-catalog-examples` |
| Runbook | `docs/engineering/runbook.md` | § US-0112 lists 8 filenames + operator recipe |
| Architecture | `docs/engineering/architecture.md` | `# US-0112` section locked |
| Contract tests | `tests/us0112_contract_test.py` | 12 markers PASS |

## Sprint artifacts

- `sprints/S0112/sprint.json` — sprint metadata (status=OPEN, phase=execute, verdict=PASS)
- `sprints/S0112/sprint.md` — sprint plan (11 tasks, 4 tranches)
- `sprints/S0112/tasks.md` — task breakdown (T-001..T-011, AC map)
- `sprints/S0112/progress.md` — per-task completion notes
- `sprints/S0112/summary.md` — this file
- `docs/engineering/state.md` — execute checkpoint + isolation evidence + strict runtime proof
- `handoffs/dev_to_qa.md` — execute → qa handoff
- `handoffs/resume_brief.md` — resume pointer for /qa

## Next phase

`/qa` (fresh QA subagent spawn) for US-0112 / S0112. QA validates deliverables, runs test suite, verifies parity, checks compose guards, writes `sprints/S0112/qa-findings.md`.
