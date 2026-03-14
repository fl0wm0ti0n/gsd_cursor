# Sprint S0036 - US-0057

## Goal

Deliver upgrade-safe scratchpad example refresh behavior with deterministic
ownership rules, installer parity, diagnostics, and regression coverage.

## Scope

- Story: `US-0057`
- Priority: P1
- Acceptance: `docs/product/backlog.md` (US-0057 AC-1..AC-10)

## Sizing check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 10
- Split required: no

## Definition of done

- US-0057 AC-1..AC-10 implemented and verifiable.
- Upgrade refreshes `.cursor/scratchpad.local.example.md`.
- Upgrade preserves `.cursor/scratchpad.local.md`.
- Installer parity and docs/tests parity are maintained.
