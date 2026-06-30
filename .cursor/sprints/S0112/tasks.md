# Sprint S0112 — Tasks

Story: US-0112 — Ship model-catalog example presets on install/upgrade

## Tranche A - Manifest parity

**T-001** (AC-1): Add 8 model-catalog.local.example*.json rows to installer-owned-paths.manifest  
**T-002** (AC-1): Mirror the same rows in template/docs/engineering/context/installer-owned-paths.manifest

## Tranche B - Installer logic

**T-003** (AC-2, AC-5): Verify installer.py missing-mode copies all 8 preset files when absent  
**T-004** (AC-2, AC-5): Verify installer.ps1 missing-mode copies all 8 preset files when absent  
**T-005** (AC-2, AC-5): Verify installer.sh missing-mode copies all 8 preset files when absent  
**T-006** (AC-3, AC-4): Verify upgrade-mode (across all three installers) refreshes only stale preset examples but never touches local files

## Tranche C - Test markers

**T-007** (AC-5): Add MODEL_CATALOG_EXAMPLE_PAIRS and --scope=model-catalog-examples to scripts/check_intake_template_parity.py  
**T-008** (AC-6): Add § Model-catalog Example Presets (US-0112) to docs/engineering/runbook.md with all 8 preset filenames and operator usage recipe  
**T-009** (AC-7): Define all 8 test markers (test_us0112_*) in tests/us0112_contract_test.py

## Tranche D - Architecture

**T-010** (AC-8): Lock # US-0112 section in docs/engineering/architecture.md  
**T-011** (AC-8): Verify template parity for all touched files via scripts/check_intake_template_parity.py --scope=model-catalog-examples

---

## AC Surjective Coverage

- AC-1 → T-001, T-002
- AC-2 → T-003, T-004, T-005
- AC-3 → T-006
- AC-4 → T-006
- AC-5 → T-003, T-004, T-005, T-007
- AC-6 → T-008
- AC-7 → T-009
- AC-8 → T-010, T-011

Task count: 11 (within SPRINT_MAX_TASKS=12, split not triggered)
