# Architecture

## Overview

## Components

## Risks

## Decisions

# US-0112 — Model-catalog example preset delivery

**Story**: US-0112 (Ship model-catalog example presets on install/upgrade)
**Decision**: DEC-0112 (Accepted)
**Research anchor**: R-0090 (delivered, Q1–Q8 closed)

## Framework vs operator boundary

The 8 `model-catalog.local.example*.json` presets are **framework files** under installer manifest control. They ship on install/upgrade and are refreshed when stale (same semantics as `scratchpad.local.example.md` per US-0075/US-0018/US-0057).

The active operator-owned `.cursor/model-catalog.local.json` is **gitignored**, outside `install_include_paths` and `clean_paths`, and never touched by any installer mode. This is a DEC-0086/DEC-0087 boundary — US-0112 completes delivery of existing presets without altering catalog schema (US-0101) or role precedence (US-0102).

## Manifest rows (8 paths)

Under `[install_include_paths]` in both `docs/engineering/context/installer-owned-paths.manifest` and `template/docs/engineering/context/installer-owned-paths.manifest` (16 rows total, byte-parity):

1. `.cursor/model-catalog.local.example.json`
2. `.cursor/model-catalog.local.example.cursor-only.json`
3. `.cursor/model-catalog.local.example.level-1-easy.json`
4. `.cursor/model-catalog.local.example.level-2-complex.json`
5. `.cursor/model-catalog.local.example.level-3-mega.json`
6. `.cursor/model-catalog.local.example.level-4-super.json`
7. `.cursor/model-catalog.local.example.role-based-balanced.json`
8. `.cursor/model-catalog.local.example.role-based-highend.json`

## Upgrade classification (framework files)

- **Missing mode**: copies all 8 examples when absent; no-op when present; deterministic log/status per file.
- **Upgrade mode**: refreshes stale framework files (template content differs); skips byte-identical files; never touches `.cursor/model-catalog.local.json`.
- **Triple installer parity**: `installer.py`, `installer.ps1`, `installer.sh` all classify `.cursor/model-catalog.local.example*.json` as `framework` via explicit enumeration in `FRAMEWORK_EXACT` (Python) / `$frameworkExact` (PowerShell) / case pattern (Bash).

## DEC-0086 / DEC-0087 compose

US-0112 does **not** amend:
- US-0101 (catalog schema, DEC-0086)
- US-0102 (role catalog precedence, DEC-0087)
- US-0054 (publish confirmation gates)
- US-0057 (example-first refresh)
- US-0075 (scratchpad example-first)

US-0112 only extends the installer manifest to include the 8 example presets as framework files, completing DEC-0086/DEC-0087 delivery path.

## Active catalog protection invariant

`.cursor/model-catalog.local.json` is:
- Gitignored (not tracked)
- Outside `install_include_paths` (not manifest-copied)
- Outside `clean_paths` (not manifest-cleaned)
- Never auto-populated by any installer mode
- Operator-owned; installer respects DEC-0086/DEC-0087 ownership boundary

## Test markers (8+)

`tests/us0112_contract_test.py` provides:
- `test_us0112_manifest_lists_eight_paths` (active + template)
- `test_us0112_missing_mode_adds_absent_framework_files` (Python/PS1/Bash)
- `test_us0112_upgrade_mode_refreshes_stale_framework_files`
- `test_us0112_upgrade_mode_preserves_unchanged_files`
- `test_us0112_upgrade_mode_never_touches_local_catalog`
- `test_us0112_active_catalog_protection_invariant`
- `test_us0112_parity_scope_model_catalog_examples`
- `test_us0112_runbook_lists_eight_preset_literals`

## Parity scope

`scripts/check_intake_template_parity.py --scope=model-catalog-examples` validates active vs template byte-parity for the manifest rows (16 rows total). Constant: `MODEL_CATALOG_EXAMPLE_PAIRS` includes the manifest pair.

## Reason codes

- `MODEL_CATALOG_EXAMPLE_PARITY_SCOPE_OK`
- `MODEL_CATALOG_EXAMPLE_PARITY_SCOPE_MISMATCH`

## Compose guards (non-negotiable)

DO NOT amend: US-0008, US-0018, US-0040, US-0054, US-0057, US-0075, US-0100, US-0101, US-0102, US-0103, US-0107, US-0110.

US-0112 is additive only — extends manifest + installer classification; no schema/precedence changes.
