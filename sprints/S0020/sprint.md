# Sprint S0020

## Goal

Deliver `US-0047` by defining explicit bulk execute orchestration behavior for
`/auto` with deterministic selection, bounded run controls, strict fresh-context
isolation, and enforced team-scoped execution guardrails.

## Scope

- **In scope**: `US-0047` (AC-1..AC-10).
- **Out of scope**: runtime product feature changes and backlog status
  canonicalization work (`US-0045`).

## Sizing Check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 10
- 10 < 12 -> within threshold. Single-story sprint, no split required.

## Milestone Check

- Milestone activation: **not applicable** for this sprint.
- Reason: no active milestone lifecycle is declared for `US-0047` in current
  planning context; sprint remains standalone and story-scoped.

## Prerequisites

- `docs/engineering/architecture.md` section for `US-0047` is finalized.
- `decisions/DEC-0024.md` is accepted for explicit bulk execute semantics.
- Research entries `R-0010`, `R-0012`, and `R-0013` are available.

## Key Decisions

- `DEC-0024`: explicit bulk execute mode with deterministic bounded controls and
  team-scoped enforcement in team mode.

## Implementation Order

Execute tasks `T-001` through `T-010` in sequence. Define explicit activation,
selection, and isolation contract first (`T-001`..`T-004`), then bounded
controls/team-scope/resume behavior (`T-005`..`T-008`), followed by
regression/parity closure (`T-009`..`T-010`).

## Risks

| Risk | Mitigation |
|------|------------|
| Bulk execution mutates unintended items | Enforce explicit activation and deterministic selection policy. |
| Team members collide on same tasks | Enforce `TEAM_MEMBER` + `ACTIVE_TASK_IDS` pre-mutation scope checks. |
| Long unattended runs hide failures | Bound run by max items and deterministic reason codes. |
| Active/template semantics drift | Include explicit parity task and regression checks. |

## Definition of Done

- Explicit bulk execute activation is documented and default-safe fallback
  behavior is preserved (AC-1).
- Selection and breadcrumb evidence include team-context snapshot when enabled
  (AC-2).
- Fresh subagent isolation remains mandatory per phase and execute↔QA cycle
  (AC-3).
- Execute↔QA loop bounds remain enforced per processed item (AC-4).
- Bounded controls and deterministic stop/skip reason codes are defined (AC-5).
- Decision gates remain mandatory in bulk mode (AC-6).
- Resume semantics for interrupted bulk runs are deterministic and documented
  (AC-7).
- Team mode out-of-scope execution is blocked/skipped with no writes (AC-8).
- Regression matrix includes positive, blocked-policy, and isolation checks
  (AC-9).
- Active/template command/docs/rules parity is complete (AC-10).
