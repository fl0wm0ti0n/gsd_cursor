# Sprint S-BUG0014

**Bug**: BUG-0014 (Sovereign-loop era features missing from README feature coverage catalog and legacy release_notes.md)
**Orchestrator Run**: auto-20260703-01
**Priority**: P3 (low risk, doc-only)
**Effort**: 1 day
**Status**: PLANNED
**Created**: 2026-07-03T17:50:00Z
**Sprint ID**: S-BUG0014

## Goal

Full backfill of README feature coverage catalogs (both `its_magic/README.md` and `docs/developer/README.md`) with 125 catalog rows (US-0001..US-0112 + BUG-0001..BUG-0013) to satisfy AC-3 (`[README_FEATURE_COVERAGE_VALIDATE_OK]`). Sync `template/its_magic/README.md` for parity. Add 5 missing finalized-note entries to `handoffs/release_notes.md` (S0103, S0104, S0105, S0106, S0108) to satisfy AC-2.

## Tasks

- **T-001**: Backfill `its_magic/README.md` with 125 catalog rows (US-0001..US-0112 + BUG-0001..BUG-0013) in appropriate H2 sections per predicate contract
- **T-002**: Backfill `docs/developer/README.md` with same 125 catalog rows in dev H2 sections per predicate contract
- **T-003**: Sync `template/its_magic/README.md` from `its_magic/README.md` (byte-identical copy for parity)
- **T-004**: Add 5 missing release notes entries to `handoffs/release_notes.md` (S0103, S0104, S0105, S0106, S0108 — follow existing S0107/S0109+ format)

## AC Coverage (Surjective)

| AC | Task(s) | Coverage |
|----|---------|----------|
| AC-1 | T-001, T-002 | Add 125 rows to README catalog (both surfaces) |
| AC-2 | T-004 | Add 5 entries to release_notes.md |
| AC-3 | T-001, T-002, T-003 | Validator returns [README_FEATURE_COVERAGE_VALIDATE_OK] |
| AC-4 | (already passes) | bug_issue_validate passes (already passes, confirmed maintained) |

## Test Markers

- `test_bug0014_readme_catalog_backfill` — verify validator passes after T-001/T-002
- `test_bug0014_template_parity` — verify template matches source after T-003
- `test_bug0014_release_notes` — verify 5 entries present after T-004

## Compose Guards (16, ALL UNCHANGED)

US-0091, US-0097, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0106, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112

## Files to Touch

- `its_magic/README.md` — T-001
- `docs/developer/README.md` — T-002
- `template/its_magic/README.md` — T-003
- `handoffs/release_notes.md` — T-004

## Files NOT to Touch

All compose guards (US-0091, US-0097, US-0040, US-0100, US-0101, US-0102, US-0103..US-0112), all scripts, all Python/PowerShell/Shell installers.

## Sizing

- `SPRINT_MAX_TASKS=12` (default)
- `task_count=4` (within threshold)
- `SPRINT_AUTO_SPLIT_triggered=false`

## Ordering

T-001 → T-002 → T-003 → T-004 (T-003 must run after T-001/T-002 completes; T-004 is independent).

## Risks

1. **R1 (MEDIUM)**: Full 125-row backfill is large but bounded. Mitigate with deterministic row template per R-0100 Q4/Q5.
2. **R2 (LOW)**: Template copy must be refreshed AFTER catalog edits. Mitigated by explicit ordering (T-003 after T-001/T-002).
3. **R3 (INFO)**: Backlog parser does not recognize DONE/user_visible fields for US-0103..US-0110. Catalog rows added preemptively; separate backlog normalization debt tracked outside this bug.

## Stop Condition

**PASS** — No major tradeoff requires DEC (documentation-only, no architectural surface changed). No feasibility unknown (pure text-additive, bounded 125+5 rows). No data migration risk. Per R-0100 Q6, no DEC required. Handoff to `/plan-verify` then `/execute`.

## Metadata

- `fresh_context_marker=tl-BUG0014-sprintplan-20260703T175000Z-fresh`
- `timestamp=2026-07-03T17:50:00Z`
- `phase_id=sprint-plan`
- `role=tech-lead`
- `bug_id=BUG-0014`
- `orchestrator_run_id=auto-20260703-01`
- `research_id=R-0100`
- `companion_dec=none`
- `status_authority=OPEN` (US-0045 — closure at /release)
- `next_phase=/plan-verify`
- `next_phase_after_verify=/execute`
- `next_role=dev`
