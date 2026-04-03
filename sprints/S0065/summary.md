# Sprint S0065 - Closure summary (BUG-0004 / DEC-0068)

- **Orchestrator**: `auto-20260403-01`
- **Lifecycle status**: `refresh-context complete`
- **Canonical bug status**: `BUG-0004` is `DONE` in `docs/product/backlog.md` and checked in `docs/product/acceptance.md`.
- **Release status**: `S0065` is `released` in `handoffs/release_queue.md`.

## Delivered scope

1. Clarified installer startup contract in `installer.sh` to preserve POSIX-safe `/bin/sh` behavior and forbid bash-only unconditional startup options.
2. Added `tests/installer_shell_bug0004_test.py` for BUG-0004 regression coverage:
   - static forbidden-token contract,
   - direct `sh installer.sh` missing-mode path,
   - CLI Unix launcher (`node bin/its-magic.js`) path.
3. Wired BUG-0004 regression into both `tests/run-tests.sh` and `tests/run-tests.ps1` (`26P` section).
4. Preserved non-regression of installer completeness contract (`BUG-0003`) via targeted test execution.

## Verification and release evidence

- `python tests/installer_shell_bug0004_test.py` -> PASS (`3 tests`, `2 skipped` on current Windows host).
- `python tests/installer_completeness_bug0003_test.py` -> PASS.
- `sprints/S0065/qa-findings.md` -> PASS.
- `sprints/S0065/uat.json` / `sprints/S0065/uat.md` -> PASS (`6/6`).
- `sprints/S0065/release-findings.md` -> PASS; canonical notes in `handoffs/releases/S0065-release-notes.md`.

## Next portfolio recommendation

- Resume at `/discovery` for `BUG-0005` (next OPEN intake-complete bug).
