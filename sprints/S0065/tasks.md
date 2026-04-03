# Sprint S0065 Tasks

- **Bug**: `BUG-0004`
- **Sprint**: `S0065`
- **Governance**: `DEC-0068`; `architecture.md` `# BUG-0004`; `R-0063`; `US-0045`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Confirm and preserve Unix CLI launcher contract (`spawnSync(\"sh\", ...)`) without introducing mandatory bash dependency | AC-1 |
| T-002 | done | Harden installer startup guidance in `installer.sh` to explicit POSIX-safe option contract | AC-2 |
| T-003 | done | Add direct `sh installer.sh --mode missing` regression in dedicated BUG-0004 fixture | AC-3 |
| T-004 | done | Add CLI Unix-path regression (`node bin/its-magic.js --mode missing`) in BUG-0004 fixture | AC-4 |
| T-005 | done | Add static forbidden-token guard for bash-only startup option bundles | AC-5 |
| T-006 | done | Wire BUG-0004 fixture into `tests/run-tests.sh` and `tests/run-tests.ps1` | AC-6 |
| T-007 | done | Re-run/install compatibility checks to ensure BUG-0003 completeness contract remains unaffected | AC-7 |
| T-008 | done | Update bug lifecycle artifacts (backlog/acceptance/state/release queue/release notes/resume) through release closure | AC-8 |

## Deterministic AC-to-task mapping

- AC-1 -> T-001
- AC-2 -> T-002
- AC-3 -> T-003
- AC-4 -> T-004
- AC-5 -> T-005
- AC-6 -> T-006
- AC-7 -> T-007
- AC-8 -> T-008
