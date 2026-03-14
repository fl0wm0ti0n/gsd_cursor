# Sprint S0029 Tasks

- Story: `US-0050`
- Sprint: `S0029`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Define canonical installer ownership manifest contract for managed install/clean paths | AC-2 |
| T-002 | done | Refactor `installer.ps1` to consume ownership contract for clean/install scope | AC-1, AC-2 |
| T-003 | done | Refactor `installer.sh` to consume ownership contract for clean/install scope | AC-1, AC-2 |
| T-004 | done | Refactor `installer.py` to consume ownership contract for clean/install scope | AC-1, AC-2 |
| T-005 | done | Enforce non-destructive cleanup boundaries for non-framework files and document safety behavior | AC-3 |
| T-006 | done | Neutralize seeded operational history in `template/docs/engineering/*` starter artifacts | AC-4 |
| T-007 | done | Remove or neutralize hardcoded runtime ID references in starter docs, or ship consistent baseline references | AC-5 |
| T-008 | done | Add fresh-install baseline checks (`--mode missing`) asserting no preloaded history rows | AC-6 |
| T-009 | done | Add lifecycle regression tests for clean-repo completeness and reinstall parity across installer entry points | AC-8 |
| T-010 | done | Verify upgrade compatibility (US-0018) and active/template parity for install/clean behavior | AC-7, AC-9 |
