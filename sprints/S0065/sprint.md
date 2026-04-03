# Sprint S0065

- **Bug**: `BUG-0004`
- **Goal**: Enforce POSIX-safe installer shell startup for Unix CLI `sh` invocation (`DEC-0068`) and lock deterministic regression coverage for direct `sh` and CLI invocation paths.
- **Status**: **Released** (`orchestrator_run_id=auto-20260403-01`; `released_at=2026-04-03T19:09:48Z`)

## Scope (sprint-local AC themes -> backlog + DEC-0068)

- **AC-1** - Keep Unix CLI invocation contract on `sh installer.sh` (no forced bash dependency).
- **AC-2** - Keep installer startup path POSIX-safe (`set -e` baseline; no unconditional bash-only `set` flags).
- **AC-3** - Add deterministic regression test for direct `sh installer.sh --mode missing`.
- **AC-4** - Add deterministic regression test for CLI Unix path (`node bin/its-magic.js --mode missing`).
- **AC-5** - Add static guard against forbidden startup option bundles that cause `/bin/sh` failures.
- **AC-6** - Wire BUG-0004 regression into cross-platform test harness (`run-tests.sh` and `run-tests.ps1`).
- **AC-7** - Preserve non-regression of existing installer completeness contract (BUG-0003 / DEC-0066).
- **AC-8** - Maintain canonical status and release traceability updates through verify-work/release.

## Governance

- `decisions/DEC-0068.md`
- `docs/engineering/architecture.md` `# BUG-0004`
- `docs/engineering/research.md` `R-0063`
- Related: `BUG-0005`, `US-0008`, `US-0018`, `US-0045`
