# Sprint S0029 Summary — US-0050 Clean Install Hygiene and Complete Clean-Repo Coverage

## Delivered

1. **Canonical ownership contract (T-001 / AC-2)**  
   Added installer-owned manifest at `docs/engineering/context/installer-owned-paths.manifest` and template parity copy at `template/docs/engineering/context/installer-owned-paths.manifest` with shared `install_include_paths` and `clean_paths`.

2. **Manifest-driven installers (T-002, T-003, T-004 / AC-1, AC-2)**  
   Refactored `installer.ps1`, `installer.sh`, and `installer.py` to load and enforce the same ownership manifest for install and clean operations; removed path-list drift between installer entry points.

3. **Clean safety boundary and scope coverage (T-005 / AC-3)**  
   Expanded clean scope to manifest-owned workflow artifacts, including docs/user-guides, validate scripts, CI workflow files, and `.its-magic-version`, while preserving non-framework files outside owned paths.

4. **Neutral starter engineering artifacts (T-006 / AC-4)**  
   Removed seeded operational rows from template artifacts:
   - `template/docs/engineering/status-normalization-report.md`
   - `template/docs/engineering/compatibility-report.md`
   - `template/docs/engineering/compatibility-signals.md`
   - `template/docs/engineering/component-scope.md`
   - `template/docs/engineering/component-scope-report.md`

5. **Hardcoded starter reference neutralization (T-007 / AC-5)**  
   Replaced hardcoded reference wording in `template/docs/engineering/research.md` to remove the fixed `DEC-0011` reference in fresh installs.

6. **Fresh-install and clean lifecycle regression checks (T-008, T-009 / AC-6, AC-8)**  
   Added assertions in both test runners for:
   - ownership manifest presence after missing install,
   - neutral starter state (`(none yet)` in status normalization report),
   - no hardcoded `DEC-0011` in starter research,
   - clean-repo completeness for owned paths (docs, scripts, workflow files, version marker),
   - non-framework marker preservation.

7. **Upgrade and parity verification (T-010 / AC-7, AC-9)**  
   Reused lifecycle upgrade checks and confirmed active/template parity for ownership manifest, installer help text, and README clean semantics.

8. **QA blocker remediation (execute cycle 2)**  
   Aligned `packaging/homebrew/its-magic.rb` with current npm package version (`0.1.2-20`) by updating URL, version, and SHA256 so stable formula version-sync checks pass.

## Files changed

- `installer.ps1`, `installer.sh`, `installer.py`
- `bin/its-magic.js`
- `README.md`, `template/README.md`
- `docs/engineering/context/installer-owned-paths.manifest`
- `template/docs/engineering/context/installer-owned-paths.manifest`
- `template/docs/engineering/status-normalization-report.md`
- `template/docs/engineering/compatibility-report.md`
- `template/docs/engineering/compatibility-signals.md`
- `template/docs/engineering/component-scope.md`
- `template/docs/engineering/component-scope-report.md`
- `template/docs/engineering/research.md`
- `tests/run-tests.ps1`, `tests/run-tests.sh`
- `packaging/homebrew/its-magic.rb`
- `sprints/S0029/tasks.md`, `sprints/S0029/progress.md`, `sprints/S0029/summary.md`
- `docs/engineering/state.md`, `handoffs/dev_to_qa.md`

## Test result

- `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`: **PASS** (Pass: 404, Fail: 0).  
- Evidence: `tests/report.md` (Timestamp: 2026-03-11T22:12:04Z).

## Blockers

None.

## Release outcome

- Release gate chain PASS; sprint finalized as `released`.
- Canonical notes: `handoffs/releases/S0029-release-notes.md`.
- Queue row: `handoffs/release_queue.md` (`S0029` status `released`).
- Product reconciliation complete: `US-0050` is DONE in `docs/product/backlog.md` and checked in `docs/product/acceptance.md`.
