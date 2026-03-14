# Sprint S0029 - US-0050

## Goal

Implement deterministic clean-install hygiene by introducing ownership-complete
cleanup scope, neutral starter artifact rules, and install/clean regression
coverage without breaking upgrade compatibility.

## Scope

- Story: `US-0050`
- Priority: P1
- Acceptance: `docs/product/backlog.md` (US-0050 AC-1..AC-9)

## Sizing check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 10
- Split required: no

## Milestone activation check (DEC-0009)

- Milestone context: not declared for this sprint.
- Activation transition: not applicable.

## Definition of done

- All US-0050 AC-1..AC-9 implemented and verified.
- `--clean-repo` scope is ownership-complete and deterministic across installers.
- Template starter artifacts are neutralized (no seeded operational history).
- Lifecycle regression coverage proves clean install -> clean-repo -> reinstall behavior.
- Active/template parity remains aligned for install/clean contracts.
