# Release notes — S0112 / US-0112 (R0112)

- **Date:** 2026-06-30
- **Story:** US-0112 — Ship model-catalog example presets on install/upgrade
- **Decision:** DEC-0112 (Accepted)
- **Research anchor:** R-0090 (delivered)
- **Release ID:** R0112
- **Sprint:** S0112
- **Orchestrator run:** auto-20260628-04

## Summary

US-0112 ships framework example delivery for model-catalog presets. All eight `.cursor/model-catalog.local.example*.json` preset files are now listed in `installer-owned-paths.manifest` (active + template mirror) and delivered by `missing` and `upgrade` installer modes. The operator active catalog (`.cursor/model-catalog.local.json`) remains gitignored and outside the installer manifest. Triple installer parity (Python, PowerShell, Shell) is maintained. Runbook documents the operator recipe. Contract tests (12 markers) and parity scope (`--scope=model-catalog-examples`) confirm correctness.

## Tasks delivered (11/11)

| Task | AC | Description |
|------|-----|-------------|
| T-001 | AC-1 | Active manifest: 8 model-catalog.example rows added |
| T-002 | AC-1 | Template manifest: byte-identical mirror |
| T-003 | AC-2,5 | Python installer missing mode: FRAMEWORK_EXACT includes 8 examples |
| T-004 | AC-2,5 | PowerShell installer missing mode: $frameworkExact includes 8 examples |
| T-005 | AC-2,5 | Shell installer missing mode: classify_file includes example glob |
| T-006 | AC-3,4 | Upgrade mode: refresh stale, skip unchanged, never touch local catalog |
| T-007 | AC-5 | MODEL_CATALOG_EXAMPLE_PAIRS + --scope=model-catalog-examples in parity script |
| T-008 | AC-6 | Runbook recipe: 8 preset filenames + operator workflow |
| T-009 | AC-7 | 12 test_us0112_* contract markers |
| T-010 | AC-8 | Architecture.md # US-0112 section |
| T-011 | AC-8 | Template parity verification (all touched files mirrored) |

## Compose guards (12/12 UNCHANGED)

US-0008, US-0018, US-0040, US-0054, US-0057, US-0075, US-0100, US-0101, US-0102, US-0103, US-0107, US-0110

## Test markers (12/12 PASS)

- test_us0112_manifest_lists_eight_paths_active
- test_us0112_manifest_lists_eight_paths_template
- test_us0112_missing_mode_adds_absent_framework_files_python
- test_us0112_missing_mode_adds_absent_framework_files_ps1
- test_us0112_missing_mode_adds_absent_framework_files_shell
- test_us0112_upgrade_mode_refreshes_stale_framework_files
- test_us0112_upgrade_mode_preserves_unchanged_files
- test_us0112_upgrade_mode_never_touches_local_catalog
- test_us0112_active_catalog_protection_invariant
- test_us0112_triple_installer_parity_eight_examples
- test_us0112_runbook_lists_eight_preset_literals
- test_us0112_parity_scope_model_catalog_examples

## Parity scope

`--scope=model-catalog-examples` [INTAKE_TEMPLATE_PARITY_OK]
- MODEL_CATALOG_EXAMPLE_PAIRS: 16 manifest row pairs (8 active + 8 template)

## Files touched

| File | Classification |
|------|---------------|
| `docs/engineering/context/installer-owned-paths.manifest` | manifest (8 rows added) |
| `template/docs/engineering/context/installer-owned-paths.manifest` | manifest (byte-identical mirror) |
| `installer.py` | framework file (FRAMEWORK_EXACT includes 8 examples) |
| `installer.ps1` | framework file ($frameworkExact includes 8 examples) |
| `installer.sh` | framework file (classify_file includes example glob) |
| `scripts/check_intake_template_parity.py` | parity script (MODEL_CATALOG_EXAMPLE_PAIRS) |
| `docs/engineering/runbook.md` | runbook recipe |
| `template/docs/engineering/runbook.md` | runbook mirror |
| `docs/engineering/architecture.md` | architecture notes # US-0112 |
| `tests/us0112_contract_test.py` | contract tests (12 markers) |

## Backward compatibility

- `RELEASE_TRIGGER_SOURCE=manual` default unchanged
- `installer-owned-paths.manifest` additive rows (8 new paths)
- Upgrade classification reuses framework-file semantics from US-0075/US-0018/US-0057
- No changes to catalog schema, model_tier_lib.py, or resolution logic
- Active catalog (`.cursor/model-catalog.local.json`) remains gitignored and never touched by installer

## Run

- **start_command:** `pytest tests/us0112_contract_test.py -v`
- **runtime_mode:** local
- **runtime_context_ref:** N/A (installer framework delivery, no runtime service)

## Connect

- **service_url:** N/A (framework file delivery, no running service)
- **service_port:** N/A
- **health_endpoint:** N/A

## Verify

1. `pytest tests/us0112_contract_test.py -v` → 12 passed
2. `python scripts/check_intake_template_parity.py --scope=model-catalog-examples` → [INTAKE_TEMPLATE_PARITY_OK]
3. Verify `docs/engineering/context/installer-owned-paths.manifest` lists all 8 example paths
4. Verify `installer.py` `FRAMEWORK_EXACT` includes all 8 example paths
5. Verify `docs/engineering/runbook.md` § US-0112 lists all 8 preset filenames

## Credentials

- No credentials required (installer framework file delivery)

## Known Issues

- None

## Gate snapshot

- QA: PASS (0 blocking findings)
- UAT: PASS (12/12 steps)
- Isolation: PASS (distinct fresh_context_marker per phase)
- Strict proof: PASS
- Publish: skipped (RELEASE_PUBLISH_MODE=disabled)
- Sync: disabled (SYNC_POLICY_MODE=disabled)
