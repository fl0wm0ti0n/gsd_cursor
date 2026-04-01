# Sprint S0063 Tasks

- **Bug**: `BUG-0003`
- **Sprint**: `S0063`
- **Governance**: `DEC-0066`; `architecture.md` `# BUG-0003`; `R-0061`; `US-0045`; `US-0018`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Update `docs/engineering/context/installer-owned-paths.manifest` (and template mirror if owned) so required-script inventory is explicit for installer completeness checks, with no alternate hidden inventory source | AC-1 |
| T-002 | done | Ensure `scripts/enforce-triad-hot-surface.py` is present in installer-owned install include paths and paired clean ownership policy | AC-2 |
| T-003 | done | Preserve existing `missing`/`upgrade` branch semantics while adding completeness enforcement strictly as post-install invariant | AC-3 |
| T-004 | done | Implement deterministic post-install validator that checks all required manifest script paths exist after copy/classification | AC-4 |
| T-005 | done | Emit fail-closed deterministic diagnostics `INSTALL_COMPLETENESS_FAILED` and `INSTALL_REQUIRED_SCRIPT_MISSING:<path>` on missing required scripts | AC-5 |
| T-006 | done | Add remediation text in installer outputs/runbook guidance pointing to manifest parity/update path and rerun actions | AC-6 |
| T-007 | done | Implement parity-safe shared validation contract across `installer.py` and wrappers (`installer.ps1`, `installer.sh`) with identical reason-code semantics | AC-7 |
| T-008 | done | Add positive-path regression coverage for both `missing` and `upgrade` ensuring required scripts are present after successful install | AC-8 |
| T-009 | done | Add negative + parity regression coverage: staged required-script omission fails deterministically; active/template installer + manifest surfaces remain aligned | AC-9 |
| T-010 | done | Add install/clean symmetry checks for required script paths so ownership remains paired and non-destructive | AC-10 |

## Deterministic AC-to-task mapping

- AC-1 -> T-001
- AC-2 -> T-002
- AC-3 -> T-003
- AC-4 -> T-004
- AC-5 -> T-005
- AC-6 -> T-006
- AC-7 -> T-007
- AC-8 -> T-008
- AC-9 -> T-009
- AC-10 -> T-010
