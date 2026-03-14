# Sprint S0033 - US-0054

## Goal

Implement configurable multi-target release publish with default confirmation
gate, including generic custom targets and first-class SSH target support.

## Scope

- Story: `US-0054`
- Priority: P1
- Acceptance: `docs/product/backlog.md` (US-0054 AC-1..AC-10)

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

- US-0054 AC-1..AC-10 are implemented and verifiable.
- Publish-target schema and validation are deterministic and documented.
- Confirmation gate defaults are enforced for publish execution.
- `custom` and `ssh` target support is available without provider hardcoding.
- Active/template parity and regression coverage are in place.
