# Sprint S0010

## Goal

Deliver `US-0038` (Phase-Triggered Sync Policy with Guarded Auto-Push) with
deterministic phase-boundary sync policy evaluation, mandatory pre-push test
gating, QA-first auto-push restrictions, branch safety constraints, and
auditable sync decision evidence while preserving default manual behavior.

## Scope

- **In scope**: `US-0038` (AC-1..AC-10).
- **Out of scope**: runtime git orchestration redesign, CI provider changes, or
  forcing a single branch strategy for all teams.

## Sizing Check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 11
- 11 < 12 -> within threshold. Single-story sprint, no split required.

## Milestone Check

- Milestone activation: **not applicable** for this sprint.
- Reason: no active milestone lifecycle is declared for `US-0038` in current
  planning context; sprint remains standalone and story-scoped.

## Prerequisites

- `docs/engineering/architecture.md` section for `US-0038` is finalized.
- `decisions/DEC-0018.md` is accepted and governs sync policy semantics.
- Existing validate-and-push scripts remain the baseline check chain contract.

## Key Decisions

- `DEC-0018`: policy-driven guarded auto-sync model with deterministic reason
  codes and fail-closed safety defaults.

## Implementation Order

Execute tasks `T-001` through `T-011` in sequence. Establish policy and
eligibility contracts first (`T-001`..`T-004`), then sync evidence and docs
alignment (`T-005`..`T-008`), then negative-path regression and parity closure
(`T-009`..`T-011`).

## Risks

| Risk | Mitigation |
|------|------------|
| Auto-push semantics become ambiguous across commands/docs | Centralize policy vocabulary and reason codes in runbook + command updates. |
| Optional runbook keys cause false blocking | Keep `TEST_COMMAND` as mandatory baseline and treat optional keys as conditional checks only. |
| Unsafe branch auto-push behavior | Enforce deny-by-default with explicit allowlist contract and negative tests. |
| QA-first guard could be bypassed accidentally | Add explicit pre-QA and blocker-state denial scenarios in QA/UAT coverage. |
| Active/template drift for changed guidance | Complete parity task across active + `template/` copies before sprint close. |

## Definition of Done

- Canonical sync policy modes are defined and documented with default non-auto
  behavior (AC-1, AC-10).
- Policy eligibility evaluates only at phase boundaries with deterministic
  decision outcomes (AC-2).
- Pre-push gating always requires `TEST_COMMAND`; failures/timeouts/missing test
  evidence block push (AC-3).
- Optional lint/typecheck/formatter checks are honored only when configured and
  reported clearly (AC-4).
- Feature auto-push is disallowed before QA completion; QA blockers prevent
  auto-push with remediation guidance (AC-5, AC-6).
- Branch safety deny-by-default behavior is enforced for auto-sync unless
  explicitly allowlisted (AC-7).
- Sync evidence records phase, mode, checks, push decision, and reason code
  deterministically in workflow artifacts (AC-8).
- `scripts/validate-and-push.ps1` and `scripts/validate-and-push.sh` are kept
  behaviorally aligned with mandatory test-before-push semantics (AC-9).
