# Sprint S0012

## Goal

Deliver `US-0040` (Per-Sprint Release Notes and Release Queue Tracker) with
non-overwriting sprint-scoped release notes, deterministic queue lifecycle
transitions, safe legacy migration/backfill handling, backward-compatible legacy
read behavior, and fail-closed mismatch reason-code semantics.

## Scope

- **In scope**: `US-0040` (AC-1..AC-9).
- **Out of scope**: deployment runtime behavior changes, external release
  management integrations, and QA/UAT evidence model redesign.

## Sizing Check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 11
- 11 < 12 -> within threshold. Single-story sprint, no split required.

## Milestone Check

- Milestone activation: **not applicable** for this sprint.
- Reason: no active milestone lifecycle is declared for `US-0040` in current
  planning context; sprint remains standalone and story-scoped.

## Prerequisites

- `docs/engineering/architecture.md` section for `US-0040` is finalized.
- `decisions/DEC-0020.md` is accepted and governs per-sprint notes and queue
  transition semantics.
- Existing legacy release file `handoffs/release_notes.md` is present and must
  be treated as compatibility and migration input.

## Key Decisions

- `DEC-0020`: canonical release artifacts are sprint-scoped notes plus queue
  index; legacy file remains backward-compatible pointer/summary.
- `DEC-0020`: transition ownership is deterministic and target-sprint-scoped
  (`ready -> unreleased -> released`, with `blocked` for failures).

## Implementation Order

Execute tasks `T-001` through `T-011` in sequence. Establish artifact contracts
and transitions first (`T-001`..`T-004`), then migration/backward compatibility
and fail-safe mismatch handling (`T-005`..`T-007`), then readiness visibility,
ownership touchpoints, template parity, and regression matrix closure
(`T-008`..`T-011`).

## Risks

| Risk | Mitigation |
|------|------------|
| Queue/notes metadata drift could cause invalid release state | Define explicit reason codes and fail-closed transition policy before release finalization. |
| Legacy migration may be ambiguous for unresolved sprint identity | Keep migration non-destructive and provide deterministic manual-migration guidance path. |
| Backward compatibility readers may still depend on legacy file shape | Keep `handoffs/release_notes.md` as latest-pointer/summary contract and avoid destructive history rewrites. |
| Cross-sprint overwrite regression risk | Enforce target-sprint-only notes mutation and add explicit overwrite-prevention negative tests. |
| Active/template behavior drift | Include a dedicated parity task before sprint completion. |

## Definition of Done

- `/release` writes sprint-scoped notes to canonical
  `handoffs/releases/Sxxxx-release-notes.md` and does not overwrite other
  sprint notes (AC-1).
- Canonical queue artifact with required fields exists and is documented as
  source of release status truth (AC-2).
- Queue transition semantics are deterministic for release-entry and
  finalization paths on target sprint only (AC-3).
- Unresolved sprint identity fails safely with no destructive note overwrite and
  actionable remediation guidance (AC-4).
- Legacy `handoffs/release_notes.md` migration/backfill contract is defined as
  non-destructive and idempotent for resolvable/unresolved contexts (AC-5).
- Backward-compatible legacy read path remains supported through pointer/latest
  summary behavior (AC-6).
- Readiness/reporting explicitly surfaces unreleased queue entries before
  finalization (AC-7).
- Release command/rules/docs define ownership and phase touchpoints for queue
  transitions and note generation (AC-8).
- Active and template copies stay behaviorally aligned for release notes and
  queue semantics (AC-9).
