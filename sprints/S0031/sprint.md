# Sprint S0031 - US-0052

## Goal

Implement optional fresh-project ID namespace bootstrap so new repositories can
start at `US-0001`/`DEC-0001`/`R-0001` when explicitly enabled and eligible,
while preserving highest-existing-ID continuation for non-fresh repositories.

## Scope

- Story: `US-0052`
- Priority: P2
- Acceptance: `docs/product/backlog.md` (US-0052 AC-1..AC-8)

## Sizing check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 10
- Split required: no

## Milestone activation check (DEC-0009)

- Milestone context: not declared for this sprint.
- Activation transition: not applicable.

## Optional mode checks

- `COMPONENT_SCOPE_MODE=0`: no required component scope metadata added.
- `USER_GUIDE_MODE=0`: no required user-guide planning tasks added.

## Definition of done

- All US-0052 AC-1..AC-8 implemented and verified.
- Optional bootstrap control is explicit, documented, and default-off.
- Freshness detection is deterministic and auditable across canonical artifacts.
- Eligible bootstrap path starts at `0001`; non-fresh path remains highest-ID continuation.
- Historical IDs are never rewritten; collision safety is preserved.
- Active/template parity and regression coverage remain aligned.
