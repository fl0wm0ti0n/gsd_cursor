# Sprint S0011

## Goal

Deliver `US-0039` (Release Gate Tightening for Check-In Tests and QA/UAT
Completion) with strict ordered release gates, deterministic failure reasons,
mandatory evidence requirements, no-bypass default behavior, and explicit
decision-gate override evidence.

## Scope

- **In scope**: `US-0039` (AC-1..AC-10).
- **Out of scope**: changing sprint lifecycle ownership model or replacing the
  existing QA/UAT artifact formats.

## Sizing Check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 11
- 11 < 12 -> within threshold. Single-story sprint, no split required.

## Milestone Check

- Milestone activation: **not applicable** for this sprint.
- Reason: no active milestone lifecycle is declared for `US-0039` in current
  planning context; sprint remains standalone and story-scoped.

## Prerequisites

- `docs/engineering/architecture.md` section for `US-0039` is finalized.
- `decisions/DEC-0019.md` is accepted and governs release gate ordering.
- `US-0038` sync-policy semantics are planned as upstream evidence source.

## Key Decisions

- `DEC-0019`: deterministic gate order is mandatory:
  `check-in test -> QA -> UAT -> release finalization`.

## Implementation Order

Execute tasks `T-001` through `T-011` in sequence. Define gate ordering and
evidence contracts first (`T-001`..`T-004`), then no-bypass and override-path
semantics (`T-005`..`T-007`), then regression, parity, and final traceability
closure (`T-008`..`T-011`).

## Risks

| Risk | Mitigation |
|------|------------|
| Gate order inconsistencies between docs and command behavior | Use a single ordered gate vocabulary in release, QA, and runbook guidance. |
| Stale evidence edge cases are under-specified | Add stale/missing/failing evidence negative-path matrix and explicit reason codes. |
| Override path accidentally acts as hidden bypass | Require decision-gate artifact evidence and rationale for every override path. |
| Optional lint/typecheck keys may cause false blocking | Preserve mandatory baseline scope as test + QA + UAT only. |
| Active/template drift for release semantics | Include explicit parity task before sprint completion. |

## Definition of Done

- `/release` includes strict mandatory check-in test gate with deterministic pass
  criteria and explicit fail reasons (AC-1, AC-2).
- QA completion evidence is mandatory and blocks release when blockers remain
  unresolved (AC-3).
- UAT completeness gate remains mandatory and blocks placeholder/incomplete/fail
  states (AC-4).
- Gate ordering is deterministic and enforced before release finalization
  outputs (AC-5).
- Release output records per-gate pass/fail status and evidence refs for
  auditing in handoff/state artifacts (AC-6).
- Default no-bypass behavior is preserved; any exception must pass explicit
  decision-gate override with rationale evidence (AC-7).
- Active and template command/docs guidance remains aligned (AC-8).
- Regression coverage includes positive and negative stale-evidence scenarios
  per gate (AC-9).
- Optional blank lint/typecheck keys do not cause false release failures while
  mandatory test + QA + UAT gates remain enforced (AC-10).
