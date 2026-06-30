# Sprint S0112 Progress

- sprint_id: S0112
- story_id: US-0112
- story_title: Ship model-catalog example presets on install/upgrade
- dec_ref: DEC-0112
- research_ref: R-0090
- status: OPEN
- created_at: 2026-06-30T22:50:00Z
- orchestrator_run_id: auto-20260628-04

## Compose Guards (non-negotiable)

1. US-0008: installer CLI unchanged
2. US-0018: smart upgrade semantics unchanged
3. US-0040: canonical release artifacts unchanged
4. US-0054: publish confirmation gates unchanged
5. US-0057: example-first refresh unchanged
6. US-0075: scratchpad example-first unchanged
7. US-0100: version-scoped changelog unchanged
8. US-0101: per-phase model tier unchanged
9. US-0102: model-catalog installer presets unchanged
10. US-0103: AI decision ledger unchanged
11. US-0107: sovereign loop mode unchanged
12. US-0110: goal-based convergence unchanged

## AC-to-task surjective map

| AC | Tasks | Status |
|----|-------|--------|
| AC-1 | T-001, T-002 | DONE |
| AC-2 | T-003, T-004, T-005 | DONE |
| AC-3 | T-006 | DONE |
| AC-4 | T-006 | DONE |
| AC-5 | T-003, T-004, T-005, T-007 | DONE |
| AC-6 | T-008 | DONE |
| AC-7 | T-009 | DONE |
| AC-8 | T-010, T-011 | DONE |

## Tranche A — Manifest + Architecture

- [x] **T-001** AC-1 — Active manifest: 8 `.cursor/model-catalog.local.example*.json` rows added to `docs/engineering/context/installer-owned-paths.manifest` under `[install_include_paths]`.
- [x] **T-002** AC-1 — Template manifest: byte-identical mirror at `template/docs/engineering/context/installer-owned-paths.manifest`. Total 16 rows (8 active + 8 template).
- [x] **T-010** AC-8 — Architecture notes: `docs/engineering/architecture.md` `# US-0112` section documents framework vs operator boundary, manifest rows, upgrade classification, DEC-0086/DEC-0087 compose.

## Tranche B — Triple Installer Verify

- [x] **T-003** AC-2, AC-5 — Python installer: `installer.py` `missing` mode copies 8 examples when absent; `FRAMEWORK_EXACT` set includes all 8 paths.
- [x] **T-004** AC-2, AC-5 — PowerShell installer: `installer.ps1` `missing` mode copies 8 examples; `$frameworkExact` array includes all 8 paths.
- [x] **T-005** AC-2, AC-5 — Shell installer: `installer.sh` `missing` mode copies 8 examples; `classify_file` case pattern includes `.cursor/model-catalog.local.example*.json`.
- [x] **T-006** AC-3, AC-4 — Upgrade mode: all three installers refresh stale framework files (template content differs), skip unchanged, never touch `.cursor/model-catalog.local.json` (gitignored, outside manifest).

## Tranche C — Parity + Runbook

- [x] **T-007** AC-5 — Parity scope: `scripts/check_intake_template_parity.py` `--scope=model-catalog-examples` with `MODEL_CATALOG_EXAMPLE_PAIRS` constant (16 manifest row pairs).
- [x] **T-008** AC-6 — Runbook recipe: `docs/engineering/runbook.md` § "Model-catalog example preset delivery (US-0112 / DEC-0112)" lists all 8 filenames, documents operator workflow (copy preset → `model-catalog.local.json`), parity scope, reason codes.

## Tranche D — Tests + Parity

- [x] **T-009** AC-7 — Contract tests: `tests/us0112_contract_test.py` with 12 `test_us0112_*` markers covering manifest paths, missing-mode classification, upgrade-mode logic, active catalog protection, triple installer parity, runbook literals, parity scope.
- [x] **T-011** AC-8 — Template parity: all touched files have byte-identical template copies (manifest, runbook, architecture, contract tests, parity script).

## Execute phase summary

All 11 tasks (T-001..T-011) completed. 8/8 ACs satisfied. Compose guards verified (12 surfaces UNCHANGED). Test suite: 12/12 markers PASS. Parity: `[MODEL_CATALOG_EXAMPLE_PARITY_SCOPE_OK]` for `--scope=model-catalog-examples`.

**Deliverables**:
- Manifest: 8 rows added to active + template (16 total)
- Installers: Python/PowerShell/Shell all classify 8 examples as framework
- Parity script: `MODEL_CATALOG_EXAMPLE_PAIRS` constant + `--scope=model-catalog-examples`
- Runbook: § US-0112 lists 8 filenames + operator recipe
- Contract tests: 12 markers in `tests/us0112_contract_test.py`
- Architecture: `# US-0112` section locked
- Template mirrors: all touched files byte-identical

**Next phase**: `/qa` (fresh QA subagent spawn)
