# Sprint S0009

## Goal

Plan and execute US-0037 (Mid-Process `/auto` Continuation with Deterministic
Resume Point) as one atomic sprint that defines explicit `/auto start-from`
behavior, deterministic resume precedence, fail-fast conflict/staleness policy,
`[AUTO_RESUME_ERROR]` code contract, inspectable breadcrumbs, and active/template
parity across command guidance.

## Scope

- **In scope**: US-0037 (AC-1..AC-9).
- **Out of scope**: changing phase deliverables, bypassing decision gates, or
  adding runtime product features unrelated to workflow orchestration.

## Sizing Check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 9
- 9 < 12 - within threshold. Single sprint, no split required.

## Milestone Check

- Milestone activation: **not applicable** for this sprint.
- Reason: no active milestone lifecycle is declared for US-0037 in current
  planning context; sprint remains standalone.

## Prerequisites

- S0008 planning/execution context exists in state artifacts.
- DEC-0017 accepted (deterministic continuation source resolution model).
- US-0037 architecture section finalized in `docs/engineering/architecture.md`.

## Key Decisions

- DEC-0017: `/auto` continuation uses explicit override + deterministic fallback
  chain, with fail-fast behavior on ambiguity/conflict/staleness.

## Implementation Order

Execute tasks T-001 through T-009 in sequence. T-001 through T-003 establish
the deterministic start-phase and fail-fast resolver contract. T-004 through
T-006 preserve continuation and observability behavior. T-007 through T-009
cover safe defaults, command alignment, and active/template parity.

## Risks

| Risk | Mitigation |
|------|------------|
| Ambiguous resume semantics between `/auto`, `/resume`, and `/pause` | Alignment task (T-008) centralizes contract wording and behavior boundaries. |
| Silent wrong-phase continuation from stale artifacts | Conflict/staleness fail-fast contract in T-003 with explicit remediation guidance. |
| Resolver behavior hard to verify without deterministic tests | T-002/T-003 include precedence and error-code verification coverage. |
| Continuation path bypassing existing stop conditions | T-005 explicitly preserves gates and stop triggers. |
| Active/template drift in command behavior | Dedicated parity task (T-009) across active + template copies. |

## Definition of Done

- `/auto` supports explicit `start-from=<phase>` with canonical phase IDs (AC-1).
- Resolver precedence is deterministic: argument > resume brief > state fallback >
  fail-fast (AC-2).
- Conflict/stale/unparseable resume conditions fail safely with actionable
  guidance and `[AUTO_RESUME_ERROR]` codes (AC-3).
- Single `/auto` continuation runs remaining phases without manual phase triggers
  (AC-4).
- Existing stop conditions and decision gates remain enforced (AC-5).
- Continuation breadcrumbs are written to inspectable artifacts (`state.md` and
  when applicable `resume_brief.md`) (AC-6).
- Manual/interactive workflows remain unaffected unless continuation is invoked
  (AC-7).
- `/pause`, `/resume`, and `/auto` guidance is behaviorally aligned, including
  user-facing docs updates where needed (AC-8).
- Active and `template/` command/rule/doc copies remain aligned (AC-9).
