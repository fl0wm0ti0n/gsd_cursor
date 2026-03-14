# Sprint S0030 - US-0051

## Goal

Implement deterministic intake decomposition and risk-aware PO questioning so
broad/high-risk requests are split into independently valuable stories with
explicit user control and bounded guided follow-ups.

## Scope

- Story: `US-0051`
- Priority: P1
- Acceptance: `docs/product/backlog.md` (US-0051 AC-1..AC-10)

## Sizing check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 11
- Split required: no

## Milestone activation check (DEC-0009)

- Milestone context: not declared for this sprint.
- Activation transition: not applicable.

## Optional mode checks

- `COMPONENT_SCOPE_MODE=0`: no required component scope metadata added.
- `USER_GUIDE_MODE=0`: no required user-guide planning tasks added.

## Definition of done

- All US-0051 AC-1..AC-10 implemented and verified.
- Intake can propose bounded multi-story decomposition with explicit split rationale.
- User can accept/merge/adjust proposed split before persistence.
- Risk-aware questioning escalates depth for broad/high-risk intake and remains bounded.
- `INTAKE_GUIDED_MODE=0` keeps low-touch behavior with duplicate safety preserved.
- Active/template parity and regression coverage remain aligned for intake semantics.
