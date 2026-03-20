# Sprint S0039 - US-0060

## Goal

Deliver deterministic state hot-surface rollover enforcement so
`docs/engineering/state.md` remains bounded while preserving non-destructive
archive history.

## Scope

- Story: `US-0060`
- Priority: P1
- Acceptance: `docs/product/backlog.md` (US-0060 AC-1..AC-10)

## Sizing check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 10
- Split required: no

## Definition of done

- US-0060 AC-1..AC-10 are implemented and verifiable.
- Rollover thresholds and fail-safe diagnostics are documented/enforced.
- Active/template parity and regression coverage are in place.
