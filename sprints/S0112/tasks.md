# Sprint S0112 — Task Breakdown

- **story_id**: US-0112
- **sprint_id**: S0112
- **timestamp**: 2026-06-30T22:30:00Z
- **task_count**: 11
- **max_tasks_allowed**: 12
- **auto_split_triggered**: false

## Tranche A — Manifest + Architecture

### T-001 (AC-1) — Add 8 model-catalog.local.example*.json rows to active manifest

- **AC**: AC-1 (Manifest completeness)
- **Dependencies**: none
- **Description**: Add 8 rows to `docs/engineering/context/installer-owned-paths.manifest` under `[install_include_paths]`:
  - `.cursor/model-catalog.local.example.json`
  - `.cursor/model-catalog.local.example.cursor-only.json`
  - `.cursor/model-catalog.local.example.level-1-easy.json`
  - `.cursor/model-catalog.local.example.level-2-complex.json`
  - `.cursor/model-catalog.local.example.level-3-mega.json`
  - `.cursor/model-catalog.local.example.level-4-super.json`
  - `.cursor/model-catalog.local.example.role-based-balanced.json`
  - `.cursor/model-catalog.local.example.role-based-highend.json`
- **Files**: `docs/engineering/context/installer-owned-paths.manifest`
- **Success token**: 8 new rows visible in `[install_include_paths]` section
- **Framework classification**: all 8 rows = framework files (upgrade refresh, missing copy-when-absent)
- **Active catalog exclusion**: `.cursor/model-catalog.local.json` MUST NOT be in manifest

### T-002 (AC-1) — Mirror manifest rows in template manifest (byte-parity)

- **AC**: AC-1 (Manifest completeness)
- **Dependencies**: T-001
- **Description**: Byte-parity copy of 8 rows into `template/docs/engineering/context/installer-owned-paths.manifest`. Both files must be byte-identical in the `[install_include_paths]` section. Total: 16 rows (8 active + 8 template) but the manifest file is the same file referenced twice.
- **Files**: `template/docs/engineering/context/installer-owned-paths.manifest`
- **Success token**: Both manifests byte-identical (verified by test_us0112_parity_scope_model_catalog_examples)

### T-010 (AC-8) — Architecture notes in docs/engineering/architecture.md # US-0112

- **AC**: AC-8 (Architecture notes)
- **Dependencies**: none
- **Description**: Architecture notes already locked at `docs/engineering/architecture.md # US-0112` (from /architecture phase). Verify at /execute that the section persists and covers:
  - Framework vs operator catalog boundary
  - Manifest rows (8 paths, 16 total)
  - Upgrade classification (framework files; US-0075 / US-0018 / US-0057 precedence)
  - Active catalog protection (`.cursor/model-catalog.local.json` gitignored and outside manifest)
  - DEC-0086 / DEC-0087 compose
- **Files**: `docs/engineering/architecture.md`
- **Pre-condition**: Section locked in /architecture phase; verify persistence at /execute

## Tranche B — Triple Installer Verify

### T-003 (AC-2, AC-5) — Verify missing-mode installer.py logic

- **AC**: AC-2 (Missing mode delivery), AC-5 (Triple installer parity)
- **Dependencies**: T-001, T-002
- **Description**: Verify that `installer.py` `missing` mode copies all 8 `model-catalog.local.example*.json` files into target `.cursor/` when absent. Deterministic log/status per file (names-only). Same semantics as `scratchpad.local.example.md` per US-0075.
- **Files**: `scripts/installer.py`
- **Success token**: All 8 files copied when absent; no-op when already present; deterministic log per file

### T-004 (AC-2, AC-5) — Verify missing-mode installer.ps1 logic

- **AC**: AC-2 (Missing mode delivery), AC-5 (Triple installer parity)
- **Dependencies**: T-001, T-002
- **Description**: Verify that `installer.ps1` `missing` mode (PS `List-SourceFiles` + copy) adds all 8 examples when absent. PS parity with `installer.py`.
- **Files**: `scripts/installer.ps1`
- **Success token**: All 8 files copied when absent; no-op when already present; deterministic log per file

### T-005 (AC-2, AC-5) — Verify missing-mode installer.sh logic

- **AC**: AC-2 (Missing mode delivery), AC-5 (Triple installer parity)
- **Dependencies**: T-001, T-002
- **Description**: Verify that `installer.sh` `missing` mode adds all 8 examples when absent. Shell parity with Python and PS1.
- **Files**: `scripts/installer.sh`
- **Success token**: All 8 files copied when absent; no-op when already present; deterministic log per file

### T-006 (AC-3, AC-4) — Verify upgrade-mode logic

- **AC**: AC-3 (Upgrade framework refresh), AC-4 (Active catalog protection)
- **Dependencies**: T-001, T-002
- **Description**: Verify that `upgrade` mode across all three installers:
  1. Refreshes stale framework files (when template content differs; same semantics as `scratchpad.local.example.md` per US-0075)
  2. Skips unchanged files (byte-identical template == unchanged counted)
  3. NEVER touches `.cursor/model-catalog.local.json` (active catalog protection; gitignored, outside `install_include_paths` and `clean_paths`)
- **Files**: `scripts/installer.py`, `scripts/installer.ps1`, `scripts/installer.sh`
- **Success token**: Upgrade refreshes stale examples, preserves unchanged, leaves active catalog untouched

## Tranche C — Parity + Runbook

### T-007 (AC-5) — Implement --scope=model-catalog-examples parity

- **AC**: AC-5 (Triple installer parity)
- **Dependencies**: T-001, T-002
- **Description**: Add `MODEL_CATALOG_EXAMPLE_PAIRS` constant to `scripts/check_intake_template_parity.py` listing all 16 manifest row byte-parity pairs. Implement new `--scope=model-catalog-examples` argument. On invoke, validate active vs template byte-parity for the 8 rows.
- **Files**: `scripts/check_intake_template_parity.py`, `template/scripts/check_intake_template_parity.py`
- **Success token**: `[MODEL_CATALOG_EXAMPLE_PARITY_SCOPE_OK]` on pass; `MODEL_CATALOG_EXAMPLE_PARITY_SCOPE_MISMATCH` on fail

### T-008 (AC-6) — Runbook §model-catalog preset recipe

- **AC**: AC-6 (Runbook operator recipe)
- **Dependencies**: T-001
- **Description**: Add section "Model-Catalog Example Presets" under Model Tier / Catalog in `docs/engineering/runbook.md`. Document:
  - Examples ship on install (missing mode) and upgrade
  - Operator copies chosen preset → `model-catalog.local.json`
  - List all 8 preset filenames + complexity/role intent
  - Pointer to scratchpad comment block (lines 351-360) for extended documentation
- **Files**: `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
- **Success token**: Section lists all 8 filenames and documents operator workflow

## Tranche D — Tests + Parity

### T-009 (AC-7) — 8+ test_us0112_* contract markers

- **AC**: AC-7 (Contract tests + parity)
- **Dependencies**: T-001, T-002, T-003, T-004, T-005, T-006, T-007, T-008
- **Description**: Write `tests/test_us0112_contract.py` (or `tests/us0112_contract_test.py`) with 8+ pytest markers:
  - `test_us0112_manifest_lists_eight_paths_active`
  - `test_us0112_manifest_lists_eight_paths_template`
  - `test_us0112_missing_mode_adds_absent_framework_files_python`
  - `test_us0112_missing_mode_adds_absent_framework_files_ps1`
  - `test_us0112_missing_mode_adds_absent_framework_files_shell`
  - `test_us0112_upgrade_mode_refreshes_stale_framework_files`
  - `test_us0112_upgrade_mode_preserves_unchanged_files`
  - `test_us0112_upgrade_mode_never_touches_local_catalog`
  - `test_us0112_active_catalog_protection_invariant`
  - `test_us0112_triple_installer_parity_eight_examples`
  - `test_us0112_runbook_lists_eight_preset_literals`
  - `test_us0112_parity_scope_model_catalog_examples`
- **Files**: `tests/us0112_contract_test.py`
- **Success token**: All 12 markers pass; coverage across AC-1..AC-7

### T-011 (AC-8) — Verify template parity for all touched files

- **AC**: AC-8 (Architecture notes)
- **Dependencies**: T-009
- **Description**: Full template parity sweep for all files touched by US-0112:
  - `installer-owned-paths.manifest` (T-001/T-002)
  - `scripts/installer.py`, `scripts/installer.ps1`, `scripts/installer.sh` (mirror)
  - `scripts/check_intake_template_parity.py` (T-007)
  - `docs/engineering/runbook.md` (T-008)
  - `docs/engineering/architecture.md` # US-0112 (T-010)
- **Files**: all touched files in `template/`
- **Success token**: All touched files have byte-identical template copies

---

## AC surjective map

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

## Compose guards

DO NOT amend: US-0008, US-0018, US-0040, US-0054, US-0057, US-0075, US-0100, US-0101, US-0102, US-0103, US-0107, US-0110.
