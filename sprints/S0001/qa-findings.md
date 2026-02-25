# QA Findings — Sprint S0001

## Scope

US-0018 (Smart Upgrade Mode, AC-1 through AC-5, AC-7, AC-8) and US-0015 (Document empty runbook commands).

## Test plan

1. AC-1: Verify `.its-magic-version` template file exists and version tracking logic in all 3 installers
2. AC-2: Verify `classify_file` / `Classify-File` function exists in all 3 installers with consistent path patterns
3. AC-3: Verify `--mode upgrade` accepted in JS CLI and all 3 installers
4. AC-4: Verify upgrade summary output in all 3 installers (added, updated, unchanged, preserved, review)
5. AC-5: Verify new file delivery logic (file not in target → always copy regardless of category)
6. AC-7: Verify triple installer parity (PS1, sh, py have matching logic)
7. AC-8: Verify README documents upgrade workflow
8. US-0015: Verify README documents empty runbook commands as intentional
9. BUG-001: Verify help text updated in all 3 installers (not just JS CLI)
10. BUG-002: Verify backup prompt excludes upgrade mode in all 3 installers
11. Tests: Verify upgrade scenario tests exist in both test runners

## Findings

### AC-1: Version tracking — PASS
- `template/.its-magic-version` exists with content `0.0.0`
- PS1: `Read-InstalledVersion` / `Write-InstalledVersion` functions present
- sh: `read_installed_version` / `write_installed_version` functions present
- py: `read_installed_version` / `write_installed_version` functions present
- `.its-magic-version` included in `$includePaths` / `include_paths` in all installers

### AC-2: File classification — PASS
- PS1: `Classify-File` with `$frameworkPrefixes`, `$frameworkExact`, `$userDataPrefixes`, `$mixedFiles`
- sh: `classify_file()` using `case` statement with correct pattern order (framework checked before user-data for `docs/engineering/context/*`)
- py: `classify_file()` with `FRAMEWORK_PREFIXES`, `FRAMEWORK_EXACT`, `USER_DATA_PREFIXES`, `MIXED_FILES` constants
- Default for unknown paths: `framework` in all three (correct — ensures new features get delivered)

### AC-3: --mode upgrade — PASS
- JS CLI: `upgrade` accepted in mode validation, help text updated with description and examples
- PS1: `[ValidateSet("missing","overwrite","interactive","upgrade")]`, upgrade branch at line 324
- sh: `choose_mode()` includes option 4 for upgrade, upgrade branch in install logic
- py: `choices=["missing", "overwrite", "interactive", "upgrade"]`, upgrade branch present

### AC-4: Upgrade summary output — PASS
- All three print: "Upgrade complete: vX -> vY" with added/updated/unchanged/preserved/review counts
- PS1 uses color-coded `Write-Host`, sh uses ANSI escape codes, py uses ANSI escape codes
- Summary format matches architecture specification

### AC-5: New file delivery — PASS
- All three installers check `if file does NOT exist in target → copy` as the first condition in the upgrade loop, before checking file category. New files always delivered.

### AC-7: Triple installer parity — PASS
- Classification logic: same path patterns across all three
- Version tracking: same read/write approach
- Upgrade flow: same algorithm (check existence → classify → compare → copy/skip)
- Summary output: same format and categories
- Backup interaction: same behavior (opt-in via --backup for upgrade mode)

### AC-8: README upgrade documentation — PASS
- "Upgrading an existing repo" section at line 67
- Documents: update command, --mode upgrade, what gets updated/preserved/reviewed, .its-magic-version tracking
- Both `README.md` and `template/README.md` updated

### US-0015: Empty runbook commands — PASS
- README lines 537-539: "Unset keys are skipped. The template ships with empty values for LINT_COMMAND, FORMAT_COMMAND, and TYPECHECK_COMMAND -- this is intentional."

### BUG-001: Help text in all installers — PASS (fixed)
- PS1 `Show-ItsMagicHelp`: upgrade documented with description and example
- sh `show_help()`: upgrade documented with description and example
- py `show_help()`: upgrade documented with description and example

### BUG-002: Backup prompt excludes upgrade — PASS (fixed)
- PS1 line 282: `if (($mode -eq "overwrite" -or $mode -eq "interactive") -and -not $backupEnabled)`
- sh line 247: `if [ "$MODE" = "overwrite" ] || [ "$MODE" = "interactive" ]`
- py line 268: `if mode in ("overwrite", "interactive") and not args.backup`
- Upgrade mode is correctly excluded from all three — no interactive prompt

### Tests — PASS
- PS1 `run-tests.ps1`: Upgrade scenario test at line 140. Uses `Invoke-Installer` wrapper with `-NonInteractive` and timeout. Tests: version file written, framework restored, user data preserved, version updated after upgrade.
- sh `run-tests.sh`: Upgrade scenario test at line 113. Uses `run_with_timeout` wrapper with stdin redirect. Same assertions as PS1.

## Deferred

- AC-6 (Migration notes for breaking format changes): deferred per sprint plan. Repos without `.its-magic-version` show "upgrading from vunknown" — acceptable for v1.

## Observations

- OBS-001 (Low): `docs/engineering/context/` classification depends on check order — framework prefix must be checked before `docs/engineering/` user-data prefix. All three installers handle this correctly (PS1/py: framework checked first; sh: case pattern order).

## Summary

**PASS** — All acceptance criteria verified (AC-1 through AC-5, AC-7, AC-8). US-0015 documented. BUG-001 and BUG-002 fixes verified. Tests cover upgrade scenario in both runners. AC-6 deferred as planned. No new bugs found.
