# Sprint S0019

## Goal

Deliver `US-0046` by defining explicit `/sprint-plan --bulk` behavior with
deterministic selection/grouping, bounded planning limits, and complete
multi-sprint artifact contracts while preserving default-safe non-bulk behavior.

## Scope

- **In scope**: `US-0046` (AC-1..AC-10).
- **Out of scope**: bulk execution orchestration (`US-0047`) and runtime product
  feature changes.

## Sizing Check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 10
- 10 < 12 -> within threshold. Single-story sprint, no split required.

## Milestone Check

- Milestone activation: **not applicable** for this sprint.
- Reason: no active milestone lifecycle is declared for `US-0046` in current
  planning context; sprint remains standalone and story-scoped.

## Prerequisites

- `docs/engineering/architecture.md` sections for `US-0046` and `US-0047` are
  finalized.
- `decisions/DEC-0023.md` is accepted for explicit bulk planning mode semantics.
- Research entries `R-0010`, `R-0011`, and `R-0013` are available.

## Key Decisions

- `DEC-0023`: explicit bulk planning mode trigger with deterministic bounded
  policy and preserved non-bulk defaults.

## Implementation Order

Execute tasks `T-001` through `T-010` in sequence. Define trigger and selection
contract first (`T-001`..`T-003`), then grouping/sizing and artifact completeness
semantics (`T-004`..`T-007`), followed by regression/parity/final traceability
closure (`T-008`..`T-010`).

## Risks

| Risk | Mitigation |
|------|------------|
| Bulk planning overproduces sprint artifacts | Enforce bounded max-story/max-sprint controls with explicit stop reasons. |
| Ambiguous grouping/splitting behavior | Define deterministic grouping order and sizing-first split rules. |
| Generated sprint artifacts become incomplete in bulk path | Require the same completeness checklist as non-bulk planning per sprint output. |
| Active/template semantics drift | Include explicit parity task and plan-verify coverage. |

## Definition of Done

- `/sprint-plan` defines explicit bulk trigger semantics with default-safe
  non-bulk fallback (AC-1).
- Story selection policy is deterministic and documented with stable tie behavior
  (AC-2).
- Bounded limits and deterministic stop outputs are defined (AC-3).
- Sizing constraints are preserved per generated sprint (AC-4).
- Grouping/splitting decision contract is deterministic and explicit (AC-5).
- Required planning artifacts are complete for each generated sprint (AC-6).
- Traceability/state update behavior is deterministic and non-duplicative (AC-7).
- Decision/missing-input fail-safe behavior is preserved in bulk mode (AC-8).
- Regression matrix covers positive/negative/boundary behavior (AC-9).
- Active and template guidance remains behaviorally aligned (AC-10).
