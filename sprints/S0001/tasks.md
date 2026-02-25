# Tasks — Sprint S0001

## Implementation order
PS1 first (reference implementation) → JS CLI → port to sh → port to py → tests → docs.

---

## T-001: Create version tracking file
- Story: US-0018 (AC-1)
- Status: done
- File: `template/.its-magic-version`
- Description: Add a `.its-magic-version` file to the template payload. Content: `0.0.0` (placeholder, overwritten with actual version on install). Add to the `includePaths` list in all three installers so it gets copied to target repos.
- Acceptance: File exists in template/, gets installed to target repos.

## T-002: installer.ps1 — version tracking
- Story: US-0018 (AC-1)
- Status: done
- File: `installer.ps1`
- Description: After successful install (any mode), write the current its-magic version to `.its-magic-version` in the target repo. In upgrade mode, read the existing version first to display "upgrading from vX to vY". Use `Get-AppVersion` (already exists) for the source version.
- Acceptance: `.its-magic-version` written after install in all modes. In upgrade mode, old version read and displayed.

## T-003: installer.ps1 — file classification
- Story: US-0018 (AC-2)
- Status: done
- File: `installer.ps1`
- Description: Add `$FRAMEWORK_PATHS` and `$USER_DATA_PATHS` pattern arrays. Add a `Classify-File($relPath)` function that returns `framework`, `user-data`, or `mixed` based on path matching. Framework paths: `.cursor/commands`, `.cursor/rules`, `.cursor/agents`, `.cursor/skills`, `.cursor/hooks`, `.cursor/hooks.json`, `.cursor/scratchpad.local.example.md`, `scripts/validate-and-push.*`, `.github/workflows`, `docs/engineering/context`. User-data paths: `docs/product`, `docs/engineering` (except context/), `sprints`, `handoffs`, `decisions`. Mixed: `.cursor/scratchpad.md`, `README.md`. Default for unknown paths: `framework`.
- Acceptance: Function correctly classifies all 86 template files.

## T-004: installer.ps1 — upgrade mode branch
- Story: US-0018 (AC-3, AC-5)
- Status: done
- File: `installer.ps1`
- Description: Add `upgrade` to the mode validation. In the file copy loop, add an `upgrade` branch that: (a) copies files that don't exist in target (new file delivery), (b) updates framework files only if content differs, (c) skips user-data files, (d) skips mixed files but flags for review. Track counts for added/updated/unchanged/preserved/review. Support `--backup` for framework files before updating.
- Depends on: T-003
- Acceptance: Upgrade mode correctly handles all file categories. New files always delivered. User data never overwritten.

## T-005: installer.ps1 — upgrade summary output
- Story: US-0018 (AC-4)
- Status: done
- File: `installer.ps1`
- Description: After the upgrade loop, print a structured summary showing: files added (with list), files updated (with list), files unchanged (count), files preserved (count), files needing review (with list and guidance message pointing to `scratchpad.local.example.md`). Show version transition "vX → vY" in the header.
- Depends on: T-004
- Acceptance: Summary matches the format in architecture doc. All counts accurate.

## T-006: bin/its-magic.js — upgrade mode support
- Story: US-0018 (AC-3)
- Status: done
- File: `bin/its-magic.js`
- Description: Accept `upgrade` as a valid `--mode` value. Pass through to OS-specific installer. Update the help text to document upgrade mode: what it does, when to use it, example command.
- Acceptance: `its-magic --target . --mode upgrade` works. `its-magic --help` shows upgrade mode documentation.

## T-007: installer.sh — port upgrade logic
- Story: US-0018 (AC-7)
- Status: done
- File: `installer.sh`
- Description: Port all upgrade features from PS1 to Bash: (a) version read/write, (b) `classify_file()` function with same path patterns, (c) upgrade branch in copy loop, (d) upgrade summary output, (e) backup support. File comparison via `cmp -s` or `diff -q`. Use identical path patterns as PS1.
- Depends on: T-002, T-003, T-004, T-005
- Acceptance: `installer.sh --mode upgrade` produces identical behavior and output to PS1.

## T-008: installer.py — port upgrade logic
- Story: US-0018 (AC-7)
- Status: done
- File: `installer.py`
- Description: Port all upgrade features from PS1 to Python: (a) version read/write, (b) `classify_file()` function with same path patterns, (c) upgrade branch in copy loop, (d) upgrade summary output, (e) backup support. File comparison via `filecmp.cmp()`. Use identical path patterns as PS1.
- Depends on: T-002, T-003, T-004, T-005
- Acceptance: `installer.py --mode upgrade` produces identical behavior and output to PS1.

## T-009: tests/run-tests.ps1 — upgrade test
- Story: US-0018 (AC-7)
- Status: done
- File: `tests/run-tests.ps1`
- Description: Add an upgrade scenario test: (1) install into temp dir with `--mode missing`, (2) modify a user-data file (e.g. write content to `docs/product/vision.md`), (3) run `--mode upgrade`, (4) verify: framework files match template, user-data file preserved with custom content, `.its-magic-version` written, mixed files preserved.
- Depends on: T-004
- Acceptance: Test passes, validates all upgrade behaviors.

## T-010: tests/run-tests.sh — upgrade test
- Story: US-0018 (AC-7)
- Status: done
- File: `tests/run-tests.sh`
- Description: Port the upgrade scenario test from PS1 to Bash. Same test steps and assertions.
- Depends on: T-007
- Acceptance: Test passes on Unix.

## T-011: README.md — document upgrade workflow
- Story: US-0018 (AC-8), US-0015
- Status: done
- Files: `README.md`, `template/README.md`
- Description: Add an "Upgrading" section to the README documenting: (a) how to update its-magic (`npm update -g its-magic`), (b) how to upgrade a repo (`its-magic --target . --mode upgrade`), (c) what happens (framework updated, user data preserved, review warnings), (d) backup option (`--backup`), (e) note that LINT/FORMAT/TYPECHECK runbook commands are empty by design for template/installer projects. Update both root README.md and template/README.md.
- Acceptance: Upgrade workflow clearly documented. Empty runbook commands documented as intentional (US-0015).

---

## Summary

| Task | File(s) | Story | Depends on |
|------|---------|-------|------------|
| T-001 | template/.its-magic-version | AC-1 | — |
| T-002 | installer.ps1 | AC-1 | T-001 |
| T-003 | installer.ps1 | AC-2 | — |
| T-004 | installer.ps1 | AC-3, AC-5 | T-003 |
| T-005 | installer.ps1 | AC-4 | T-004 |
| T-006 | bin/its-magic.js | AC-3 | — |
| T-007 | installer.sh | AC-7 | T-002–T-005 |
| T-008 | installer.py | AC-7 | T-002–T-005 |
| T-009 | tests/run-tests.ps1 | AC-7 | T-004 |
| T-010 | tests/run-tests.sh | AC-7 | T-007 |
| T-011 | README.md, template/README.md | AC-8, US-0015 | T-004 |
