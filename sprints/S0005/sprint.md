# Sprint S0005

## Goal

Deliver US-0025, US-0027, and US-0026 by adding traceability contracts,
formalizing UAT artifact lifecycle, and defining milestone lifecycle governance.
All three stories are guidance/documentation changes to existing command files,
state artifacts, and their template copies. No new tooling or automation logic.

## Scope

- **In scope**: US-0025 (AC-1..AC-6), US-0027 (AC-1..AC-6), US-0026 (AC-1..AC-6).
- **Story sequence** (per PO recommendation): US-0025 first, US-0027 second,
  US-0026 third.
- **Out of scope**: US-0017 (template drift guard), US-0024 (memory drift audit —
  handled in S0004), US-0022/US-0023 (sprint sizing/automation).

## Sizing Check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- S0004 existing tasks: 6 (US-0024, all pending)
- New tasks needed: 9 (US-0025: 3, US-0027: 3, US-0026: 3)
- Combined (S0004 + new): 15 > 12 — exceeds threshold.
- Result: **new sprint S0005 created**. S0004 kept as-is for US-0024.

## Prerequisites

- S0004 (US-0024) should be executed first. S0005 does not depend on S0004's
  implementation output, but execution order preserves PO-planned sequencing
  and keeps sprint boundaries clean.

## Shared decisions

- DEC-0009: Artifact lifecycle taxonomy (placeholder → populated → verified),
  phase-ownership matrix, minimum evidence rules. All three stories reference
  this taxonomy.
- DEC-0010: Traceability index lives in `docs/engineering/state.md`.

## Risks

- Three stories touch overlapping command files (`sprint-plan.md`,
  `verify-work.md`). Dev must apply changes incrementally per story sequence
  to avoid merge conflicts within the sprint.
- All changes are guidance/documentation. Effectiveness depends on AI reading
  and following updated command steps and lifecycle rules.
- Template parity risk: active and template copies must be updated together
  in every task.
- Traceability backfill (T-001) requires reviewing historical sprint artifacts
  to reconstruct accurate story-sprint-task mappings.

## Definition of Done

- Traceability index exists in `state.md` with backfilled entries for all
  historical sprints and maintenance steps in sprint-plan/verify-work (US-0025).
- UAT lifecycle is documented with placeholder/populated/verified states,
  ownership chain, and minimum content rules referenced by sprint-plan,
  verify-work, and release commands (US-0027).
- Milestone lifecycle states, required fields, and exit criteria are defined
  in milestone-start, milestone-complete, and sprint-plan commands (US-0026).
- All active command file changes have matching template copies.
