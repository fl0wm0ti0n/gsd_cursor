# Sprint S0063

- **Bug**: `BUG-0003`
- **Goal**: **Deterministic installer completeness for `missing`/`upgrade`** - implement `DEC-0066` so installer-owned required scripts are complete after successful install/upgrade, with `docs/engineering/context/installer-owned-paths.manifest` as sole required-script inventory, deterministic fail-closed diagnostics (`INSTALL_COMPLETENESS_FAILED`, `INSTALL_REQUIRED_SCRIPT_MISSING:<path>`), parity-safe behavior across `installer.ps1`/`installer.sh`/`installer.py`, and regression coverage for positive/negative/parity/symmetry paths.
- **Status**: **Execute complete - awaiting `/qa`** (`orchestrator_run_id=auto-20260331-03`; `executed_at=2026-03-31T22:04:56Z`)

## Scope (sprint-local AC themes -> backlog + DEC-0066)

- **AC-1** - Manifest-authoritative required inventory contract is explicit and enforced from `docs/engineering/context/installer-owned-paths.manifest`.
- **AC-2** - `scripts/enforce-triad-hot-surface.py` is included in installer-owned install scope with paired clean ownership semantics.
- **AC-3** - `missing` and `upgrade` mode semantics stay unchanged; completeness gate is post-install invariant only.
- **AC-4** - Post-install completeness check verifies all required manifest script paths exist.
- **AC-5** - Missing required scripts fail closed with deterministic reason codes:
  - `INSTALL_COMPLETENESS_FAILED`
  - `INSTALL_REQUIRED_SCRIPT_MISSING:<path>`
- **AC-6** - Diagnostics include actionable remediation tied to manifest parity/update path and rerun guidance.
- **AC-7** - Parity-safe implementation path keeps one contract surface across `installer.py`, `installer.ps1`, and `installer.sh`.
- **AC-8** - Positive matrix covers both `missing` and `upgrade` with required scripts present.
- **AC-9** - Negative/parity matrix covers required-script omission failure and active/template parity for installer + manifest surfaces.
- **AC-10** - Install/clean symmetry for newly required paths remains validated and traceable.

## Governance

- `decisions/DEC-0066.md`
- `docs/engineering/architecture.md` `# BUG-0003`
- `docs/engineering/research.md` `R-0061`
- Related: `BUG-0001`, `US-0018`, `US-0045`, `DEC-0038`
