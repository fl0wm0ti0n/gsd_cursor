# QA Findings — US-0112 / S0112 (auto-20260628-04)

## Independent QA verification (fresh subagent)

- **sprint_id**: S0112
- **story_id**: US-0112
- **story_title**: Ship model-catalog example presets on install/upgrade
- **qa_role**: qa (fresh QA subagent spawn)
- **timestamp**: 2026-06-30T23:00:00Z
- **orchestrator_run_id**: auto-20260628-04
- **fresh_context_marker**: qa-S0112-US0112-qa-20260630T230000Z-fresh
- **runtime_proof_id**: rp-auto-20260628-04-qa-qa-20260630T230000Z-US0112

---

## 1. Test Execution Results

**Command**: `pytest tests/us0112_contract_test.py -v`

| # | Test Marker | Result |
|---|-------------|--------|
| 1 | `test_us0112_manifest_lists_eight_paths_active` | PASS |
| 2 | `test_us0112_manifest_lists_eight_paths_template` | PASS |
| 3 | `test_us0112_missing_mode_adds_absent_framework_files_ps1` | PASS |
| 4 | `test_us0112_missing_mode_adds_absent_framework_files_python` | PASS |
| 5 | `test_us0112_missing_mode_adds_absent_framework_files_shell` | PASS |
| 6 | `test_us0112_upgrade_mode_refreshes_stale_framework_files` | PASS |
| 7 | `test_us0112_upgrade_mode_preserves_unchanged_files` | PASS |
| 8 | `test_us0112_upgrade_mode_never_touches_local_catalog` | PASS |
| 9 | `test_us0112_active_catalog_protection_invariant` | PASS |
| 10 | `test_us0112_parity_scope_model_catalog_examples` | PASS |
| 11 | `test_us0112_triple_installer_parity_eight_examples` | PASS |
| 12 | `test_us0112_runbook_lists_eight_preset_literals` | PASS |

**Summary**: 12/12 PASS, 0 failures.

---

## 2. Template Parity Verification

**Command**: `python scripts/check_intake_template_parity.py --scope=model-catalog-examples`

**Result**: `[INTAKE_TEMPLATE_PARITY_OK] scope=model-catalog-examples`

Byte-parity verified for all touched files:
- `installer-owned-paths.manifest` (active ↔ template) — 16 rows (8 active + 8 template)
- `installer.py` / `installer.ps1` / `installer.sh` (active ↔ template)
- `check_intake_template_parity.py` (active ↔ template) — MODEL_CATALOG_EXAMPLE_PAIRS present
- `runbook.md` (active ↔ template) — § model-catalog preset delivery
- `architecture.md` (active ↔ template) — # US-0112 section
- `tests/us0112_contract_test.py` (new file mirrored to template)

---

## 3. AC Coverage Verification

| AC | Description | Evidence | Status |
|----|-------------|----------|--------|
| AC-1 | Manifest lists 8 preset paths | 8 rows in `[install_include_paths]` active + template manifests (lines 17–24) | **SATISFIED** |
| AC-2 | Missing-mode delivery (triple installer) | `installer.py` FRAMEWORK_EXACT (8 paths), `installer.ps1` $frameworkExact (8 paths), `installer.sh` classify_file `model-catalog.local.example*.json` glob | **SATISFIED** |
| AC-3 | Upgrade-mode framework refresh | installer.py byte-compare vs template, installer.ps1 $frameworkExact refresh, installer.sh classify_file case — all framework semantics | **SATISFIED** |
| AC-4 | Active catalog protection | `.cursor/model-catalog.local.json` NOT in manifest, NOT in FRAMEWORK_EXACT, NOT in $frameworkExact, gitignored | **SATISFIED** |
| AC-5 | Triple installer parity | All 3 installers cover all 8 examples as framework files | **SATISFIED** |
| AC-6 | Runbook operator recipe | `docs/engineering/runbook.md` § "Model-catalog example preset delivery (US-0112 / DEC-0112)" with 8 preset filenames + operator usage | **SATISFIED** |
| AC-7 | Contract tests + parity | 12/12 PASS + parity `--scope=model-catalog-examples` PASS | **SATISFIED** |
| AC-8 | Architecture notes | `docs/engineering/architecture.md` `# US-0112` documents framework vs operator boundary, manifest rows, upgrade classification, DEC-0086/DEC-0087 compose | **SATISFIED** |

**AC verdict**: 8/8 SATISFIED.

---

## 4. Compose Guard Verification

12 composition surfaces verified UNCHANGED:

| # | Guard Story | Compose Rule | Status |
|---|-------------|--------------|--------|
| 1 | US-0008 | Installer CLI / manifest-driven copy unchanged | UNCHANGED |
| 2 | US-0018 | Smart upgrade framework semantics unchanged | UNCHANGED |
| 3 | US-0040 | Canonical release artifacts unchanged | UNCHANGED |
| 4 | US-0054 | Publish confirmation gates unchanged | UNCHANGED |
| 5 | US-0057 | Example-first refresh semantics unchanged | UNCHANGED |
| 6 | US-0075 | Scratchpad example-first semantics unchanged | UNCHANGED |
| 7 | US-0100 | Version-scoped changelog unchanged | UNCHANGED |
| 8 | US-0101 | Model tier base unchanged | UNCHANGED |
| 9 | US-0102 | Model tier delivery unchanged (US-0112 extends delivery only) | UNCHANGED |
| 10 | US-0103 | AI decision ledger unchanged | UNCHANGED |
| 11 | US-0107 | Sovereign loop mode unchanged | UNCHANGED |
| 12 | US-0110 | Goal-based convergence unchanged | UNCHANGED |

**Compose verdict**: 12/12 surfaces VERIFIED UNCHANGED. No regressions.

---

## 5. Reason Codes Verification

- US-0111 `RELEASE_TRIGGER_*` (9 codes) — all preserved in `docs/engineering/reason_codes.md`
- No new US-0112-specific reason codes required (US-0112 is installer delivery, inherits `RELEASE_TRIGGER_*` from US-0100/US-0111)
- US-0103 `PLAN_FIDELITY_*` / `LEDGER_*` — preserved
- US-0110 `CONVERGENCE_*` — preserved
- US-0107 `SOVEREIGN_LOOP_*` — preserved
- US-0105 `SOVEREIGN_MEMORY_*` — preserved
- US-0109 `DEPLOY_HEALING_*` — preserved

**Reason codes verdict**: All existing codes preserved. No new codes needed. No regressions.

---

## 6. Blockers

None.

---

## 7. QA Verdict

**PASS** — All acceptance criteria satisfied. 12/12 tests green. Compose guards clean. Template parity verified. Reason codes intact. Ready for /verify-work.

| Field | Value |
|-------|-------|
| Verdict | PASS |
| Reason code | QA_PASSED |
| Test results | 12/12 PASS |
| Parity | [INTAKE_TEMPLATE_PARITY_OK] scope=model-catalog-examples |
| AC satisfied | 8/8 |
| Compose guards verified | 12/12 UNCHANGED |
| Reason codes | All preserved |
| Blockers | none |
| Ready for | /verify-work |
