# Sprint S0121 - Task checklist (US-0121)

Total tasks: 10 (T-anch + T-001..T-009). SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1; no split needed.

## Task execution order

1. T-anch (NO-OP / verification)
2. T-001 (NEW `template/.opencode/` pack tree) - parallel with T-002, T-003
3. T-002 (NEW manifest parallel sections - active + template) - parallel with T-001, T-003
4. T-003 (`bin/its-magic.js` `--host` argv parser + `--help`) - parallel with T-001, T-002
5. T-004 (`installer.ps1` `-Host`) - parallel with T-005, T-006
6. T-005 (`installer.sh` `--host`) - parallel with T-004, T-006
7. T-006 (`installer.py` `--host` - manifest authority) - parallel with T-004, T-005
8. T-008 (`check_intake_template_parity.py --scope=opencode-adapter`)
9. T-009 (Runbook `## OpenCode host mode (US-0121)` h2 + `--help` line)
10. T-007 (NEW `tests/us0121_host_mode_test.py` - 14 markers; tests last, assert all outputs)
11. Integration verification

## Task checklist

- [x] **T-anch**: Verify `# US-0121` H1 anchor present in `docs/engineering/architecture.md`; verify DEC-0120 authored Accepted at `decisions/DEC-0120.md`; verify compose guards 5/5 UNCHANGED baseline (US-0008, DEC-0045, US-0102, US-0001, US-0018); verify mixed-section `host_gates_cursor_row` predicate contract locked in architecture + DEC-0120; verify 14-marker contract-test list locked in architecture; verify `template/.opencode/` does NOT yet exist; verify `tests/us0121_host_mode_test.py` does NOT yet exist; verify `[opencode_install_include_paths]` / `[opencode_clean_paths]` sections do NOT yet exist in active + template manifest. Record results to `sprints/S0121/t-anch-verification.md`. (AC-8, AC-7 baseline; NO-OP / verification only)

- [x] **T-001**: Create `template/.opencode/` tree per architecture Q6 LOCKED + DEC-0120 §6: `agents/.gitkeep` (empty), `commands/.gitkeep` (empty), `plugins/README.md` (explains plugin slot reserved for US-0124; no plugin body), `.gitignore` (Q10 four pattern groups: `.opencode/opencode.json`, `.opencode/opencode.jsonc`, `.env`, `.env.*`, `*.local.json`, `*.local.jsonc`, `auth.json`), `README.md` (explains pack: empty-but-valid, three subdirs, gitignore posture, pointer to US-0122..US-0126). No repo-root `opencode.json`. No active `.opencode/` mirror in kit repo (Q9 YAGNI). No vendor slugs, no `model:` literals, no API keys, no `.env` contents (AC-10, US-0102). (AC-1, AC-10)

- [x] **T-002**: Add `[opencode_install_include_paths]` and `[opencode_clean_paths]` sections to `docs/engineering/context/installer-owned-paths.manifest` AND `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical). Rows per architecture Q7 LOCKED + DEC-0120 §2: `[opencode_install_include_paths]` = `.opencode/agents`, `.opencode/commands`, `.opencode/plugins`, `.opencode/.gitignore`, `.opencode/README.md`; `[opencode_clean_paths]` = `.opencode`. Existing `[install_include_paths]` / `[clean_paths]` / `[required_install_script_paths]` UNCHANGED (US-0008 additive only). Triple-installer reads opencode sections only when `--host` includes opencode. (AC-5)

- [x] **T-003**: `bin/its-magic.js` additive `--host` argv parser: accept `cursor`, `opencode`, `both` (case-insensitive, whitespace-trimmed); default `cursor` when omitted; normalize `value.toLowerCase().trim()` before validate; unknown value -> exit with `INSTALL_HOST_INVALID` (ASCII diagnostic, no GUI per D11); duplicate/conflicting `--host` argv -> fail closed `INSTALL_HOST_INVALID` (no last-wins; closes critic finding 1 `ik_us0121_upgrade_host_transition`); forward normalized `--host` to PowerShell as `-InstallHost <value>` (avoids PS `$Host` landmine), to Bash as `--host <value>`; `--help` documents `--host cursor|opencode|both` and cursor-default lock (AC-9 minimal docs hook). Critic carry-in `ik_us0121_ac9_help_test_yagni`: `--help` grep is marker 9 in locked 14-marker set; do not add 15th marker without dropping YAGNI elsewhere. (AC-2, AC-9)

- [x] **T-004**: `installer.ps1` `-InstallHost` parameter (PowerShell case-insensitive but normalize for parity) + `Host-GatesCursorRow` predicate + read `[opencode_install_include_paths]` / `[opencode_clean_paths]` when host includes opencode + host-scoped missing/upgrade/clean + orphan/stale diagnostics (`OPENCODE_ORPHANED_BY_CLEAN_CURSOR`, `OPENCODE_STALE_BY_UPGRADE_CURSOR`, `CURSOR_ORPHANED_BY_CLEAN_OPENCODE`, `CURSOR_STALE_BY_UPGRADE_OPENCODE`). Kernel paths install regardless of `--host`. Uses `-InstallHost` (not `-Host`) internally to avoid the PowerShell `$Host` automatic-variable landmine; JS forwards `-InstallHost <value>`. (AC-2, AC-3, AC-5)

- [x] **T-005**: `installer.sh` `--host` argparse (Bash case-sensitive; normalize lowercase) + same `host_gates_cursor_row` predicate + opencode section reads + same host-scoped missing/upgrade/clean + same diagnostics. (AC-2, AC-3, AC-5)

- [x] **T-006**: `installer.py` `--host` argparse (Python case-sensitive; normalize lowercase) + same predicate + opencode section reads + host-scoped missing/upgrade/clean + same diagnostics (manifest authority; PS/Bash delegate manifest reads where possible). Critic carry-in `ik_us0121_missing_overwrite_host_gap`: YAGNI - `missing` after `both` no-ops on `.opencode/` via predicate (copy-if-missing is host-scoped); no new diagnostic needed; overwrite remains US-0008 unchanged. (AC-3, AC-7)

- [x] **T-007**: Create `tests/us0121_host_mode_test.py` with 14 contract-test markers per architecture table: (1) `test_us0121_default_host_cursor_when_omitted` [AC-2]; (2) `test_us0121_host_cursor_installs_cursor_and_kernel_no_opencode` [AC-2,3,4]; (3) `test_us0121_host_opencode_skips_cursor_installs_opencode_and_kernel` [AC-2,3,4]; (4) `test_us0121_host_both_installs_both_trees` [AC-2,3,4]; (5) `test_us0121_invalid_host_fails_closed_install_host_invalid` [AC-2]; (6) `test_us0121_host_normalize_case_and_whitespace` [AC-2]; (7) `test_us0121_duplicate_host_argv_fails_closed` [AC-2]; (8) `test_us0121_clean_host_cursor_after_both_emits_orphan_diagnostic` [AC-3,7]; (9) `test_us0121_upgrade_host_cursor_after_both_emits_stale_diagnostic` [AC-3,7]; (10) `test_us0121_mixed_section_cursor_skip_when_host_opencode` [AC-5,7]; (11) `test_us0121_manifest_lists_opencode_pack` [AC-5]; (12) `test_us0121_no_secrets_in_pack` [AC-10]; (13) `test_us0121_parity_scope_opencode_adapter_registered` [AC-6]; (14) `test_us0121_triple_installer_host_parity` [AC-5]. Critic carry-in `ik_us0121_ac9_help_test_yagni`: marker 9 covers `--help` grep; keep within locked 14-marker set; do not add 15th marker without dropping YAGNI elsewhere. (AC-7)

- [x] **T-008**: Register `check_intake_template_parity.py --scope=opencode-adapter` + `US0121_PARITY_PAIRS` manifest. Critic carry-in `ik_us0121_parity_active_mirror_contradiction`: parity pairs `template/.opencode` with consumed `.opencode/` (when host includes opencode); no kit-repo active mirror (Q9 YAGNI). Scope fails when `template/.opencode/` drifts from active pack surface this story owns. Pairs: installer-owned-paths.manifest (active+template), check_intake_template_parity.py (active+template), tests/us0121_host_mode_test.py (active+template). Added to SCOPES + SCOPES["all"]. (AC-6)

- [x] **T-009**: Add `## OpenCode host mode (US-0121)` h2 to `docs/engineering/runbook.md` (minimal docs hook): overview of `--host cursor|opencode|both`; cursor-default lock; how to install opencode pack (`--host opencode|both`); how to clean (`clean --host opencode|both`); orphan/stale diagnostics reference. Installer `--help` line documents `--host` (JS + PS + sh + py). Full OpenCode operator runbook is US-0126. (AC-9)

## Integration verification (post T-009 + T-007)

- [ ] Test gate: `python -m pytest tests/us0121_host_mode_test.py -v` -> 14/14 PASS
- [ ] Parity gate: `check_intake_template_parity.py --scope=opencode-adapter` PASS
- [ ] Parity gate: active + template manifest byte-identical for opencode sections
- [ ] Compose gate: 5/5 UNCHANGED (US-0008, DEC-0045, US-0102, US-0001, US-0018)
- [ ] Byte-identity gate: `--host cursor` install byte-identical to pre-US-0121 baseline on `.cursor/` + kernel paths
- [ ] No-secrets gate: `rg "apiKey|api_key|sk-|MODEL=" template/.opencode/` -> zero hits

## Files to touch (scope)

### New (create)

- `template/.opencode/agents/.gitkeep`
- `template/.opencode/commands/.gitkeep`
- `template/.opencode/plugins/README.md`
- `template/.opencode/.gitignore`
- `template/.opencode/README.md`
- `tests/us0121_host_mode_test.py`

### Edit (scoped, additive only)

- `docs/engineering/context/installer-owned-paths.manifest` (add opencode sections)
- `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical)
- `bin/its-magic.js` (additive `--host` argv parser + `--help`)
- `installer.ps1` (`-Host` parameter + predicate + opencode sections + diagnostics)
- `installer.sh` (`--host` argparse + predicate + opencode sections + diagnostics)
- `installer.py` (`--host` argparse + predicate + opencode sections + diagnostics)
- `scripts/check_intake_template_parity.py` (register `--scope=opencode-adapter` + `US0121_PARITY_PAIRS`)
- `docs/engineering/runbook.md` (add `## OpenCode host mode (US-0121)` h2)

### Verify read-only (no mutation)

- `docs/engineering/architecture.md # US-0121` (T-anch NO-OP)
- `decisions/DEC-0120.md` (T-anch NO-OP)

### Compose-guard UNCHANGED (DO NOT TOUCH)

| File | Reason |
|---|---|
| `docs/product/backlog.md` | US-0045 canonical status - `/closure` mutates ONLY at execution time |
| `docs/product/acceptance.md` | US-0045 derived view - same |
| Compose-guard story surfaces (US-0008, DEC-0045, US-0102, US-0001, US-0018) | 5/5 UNCHANGED - US-0121 adds additive `--host` only |

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (template/.opencode tree) | T-001 |
| AC-2 (--host flag) | T-003, T-004, T-005, T-006 |
| AC-3 (install/upgrade/clean host-scoped) | T-004, T-005, T-006 |
| AC-4 (cursor coexistence byte-identity) | T-007 (markers 2-4) |
| AC-5 (manifest + triple-installer) | T-002, T-004, T-005, T-006, T-007 (markers 10, 11, 14) |
| AC-6 (parity scope) | T-008, T-007 (marker 13) |
| AC-7 (contract tests 14 markers) | T-007 |
| AC-8 (compose 5/5 UNCHANGED) | T-anch (baseline), all tasks gated |
| AC-9 (docs hook minimal) | T-003 (`--help`), T-009 (runbook h2) |
| AC-10 (no secrets in template) | T-001, T-007 (marker 12) |

**Surjectivity check**: 10/10 ACs covered (AC-1..AC-10 each have at least 1 task). No `PLAN_AC_COVERAGE_GAP`.
