# Sprint S0025 - US-0048

## Goal

Enforce per-phase subagent isolation as a hard workflow contract with auditable
evidence and fail-closed gates at verify-work and release.

## Scope

- Story: `US-0048`
- Decision: `DEC-0029`
- Research: `R-0018`, `R-0019`
- Architecture: `docs/engineering/architecture.md` (US-0048 section)

## Sizing check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 10
- Split required: no

## Definition of done

- All US-0048 AC-1..AC-10 implemented and verified.
- Isolation evidence schema, gates, reason codes, and active/template parity complete.
