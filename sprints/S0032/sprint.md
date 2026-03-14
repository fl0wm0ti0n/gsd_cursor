# Sprint S0032 - US-0053

## Goal

Implement context compaction and tiered token-cost optimization mode with
deterministic profile behavior (`lean|balanced|full`), narrow-read `/ask`
retrieval, and preserved mandatory QA/UAT/release guardrails.

## Scope

- Story: `US-0053`
- Priority: P1
- Acceptance: `docs/product/backlog.md` (US-0053 AC-1..AC-10)

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

- US-0053 AC-1..AC-10 are implemented and verifiable.
- `TOKEN_PROFILE` contract is explicit with deterministic mapping and override
  precedence.
- Active context compaction and archive policy are defined and applied without
  destructive history rewrites.
- `/ask` narrow-read retrieval policy is implemented and remains read-only.
- Active/template parity and regression coverage are in place.
