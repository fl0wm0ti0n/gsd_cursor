# Architecture archive pack (2026-04-13)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 34
- First archived heading: `# US-0046: Explicit `/sprint-plan --bulk` Mode`
- Last archived heading: `# US-0047: Explicit Bulk Execute Orchestration Mode`
- Verification tuple (mandatory):
  - archived_body_lines=224
  - preamble_lines=10
  - retained_body_lines=3442

---

# US-0046: Explicit `/sprint-plan --bulk` Mode

## Overview

US-0046 adds an explicit bulk planning mode for `/sprint-plan` so multiple OPEN
stories can be planned in one bounded run. The architecture keeps current
single-scope behavior as default and adds deterministic selection/grouping rules
only when bulk mode is explicitly enabled.

## Assumption challenge and alternatives

### Option A: Keep current `/sprint-plan` behavior only

Pros:
- No command contract changes.
- Lowest implementation complexity.

Cons:
- Does not satisfy the requirement for explicit multi-story planning throughput.
- Forces repetitive manual planning runs for large backlogs.

### Option B: Implicitly auto-bulk whenever many OPEN stories exist

Pros:
- Minimal user input.
- High throughput potential.

Cons:
- Ambiguous operator intent.
- High risk of surprising large planning mutations.
- Harder to audit and bound safely.

### Option C: Explicit bulk planning trigger with bounded deterministic policy (chosen)

Pros:
- Clear operator intent and safer defaults.
- Deterministic selection/grouping output.
- Predictable bounded behavior with explicit stop reasons.

Cons:
- Adds policy controls and additional regression surface.

## Minimal architecture

### 1) Explicit mode trigger and defaults

- Add an explicit trigger for bulk planning in `/sprint-plan` (flag/argument).
- Default behavior without trigger remains current non-bulk planning.
- Invalid or ambiguous bulk arguments fail safe with actionable guidance.

### 2) Deterministic story selection policy

Selection order:
1. Story priority (highest first)
2. Backlog order (stable tie-breaker)

Policy requirements:
- Stable ordering for reproducibility.
- No hidden randomness.
- Story selection evidence logged in planning breadcrumbs.

### 3) Bounded planning controls

Required controls:
- max stories per bulk run
- max generated sprints per run

Stop outcomes must be deterministic and recorded:
- reached max stories
- reached max generated sprints
- no eligible OPEN stories
- blocked by missing/ambiguous acceptance

### 4) Grouping and splitting contract

Bulk planning uses deterministic grouping:
- prefer single-story sprints by default,
- allow multi-story grouping only when estimated task count remains within
  `SPRINT_MAX_TASKS`,
- if estimated size exceeds threshold and `SPRINT_AUTO_SPLIT=1`, split and
  continue within run bounds.

No grouping rule may bypass sizing safety controls.

### 5) Artifact completeness and traceability

For each generated sprint, planning output must be complete:
- `sprint.md`
- `tasks.md`
- `progress.md`
- UAT placeholders
- `plan-verify` readiness contract

Traceability updates in `state.md` must remain deterministic and non-duplicative.

### 6) Risk model

| Risk | Mitigation |
|------|------------|
| Bulk run plans too much at once | bounded max stories/sprints controls + explicit stop reasons |
| Story starvation in repeated bulk runs | deterministic priority ordering with stable backlog tie-break and periodic fairness review |
| Incomplete generated artifacts | enforce per-sprint completeness checklist before moving to next item |
| Confusing behavior change for current users | explicit mode trigger; default non-bulk behavior unchanged |

## Decision linkage

- Research basis: `R-0010`, `R-0011`, `R-0013`
- Decision: `DEC-0023`

---

# US-0047: Explicit Bulk Execute Orchestration Mode

## Overview

US-0047 introduces explicit bulk execution orchestration that processes planned
sprints/stories continuously while preserving strict fresh-context isolation,
execute↔QA loop controls, and deterministic stop/skip behavior. In team mode,
execution must be scoped to member-owned tasks only.

## Assumption challenge and alternatives

### Option A: Rely only on existing `/auto` flag combinations

Pros:
- Reuses current functionality.
- No new command-level contract.

Cons:
- Operator intent remains implicit and easier to misconfigure.
- Team-member task scoping is not explicit in execution contract.
- Harder to communicate/verify bounded behavior per run.

### Option B: Global bulk execute without team-scope enforcement

Pros:
- Maximum throughput in single-user scenarios.

Cons:
- Unsafe for concurrent team members.
- High duplicate-work and task-collision risk.

### Option C: Explicit bulk execute mode with team-scoped guardrails (chosen)

Pros:
- Clear activation semantics and safer defaults.
- Enforces member/task scope in team mode.
- Keeps bounded and auditable behavior.

Cons:
- Requires additional scope-check logic and reason-code coverage.

## Minimal architecture

### 1) Explicit mode trigger and defaults

- Define explicit bulk execute mode (new command or explicit mode argument).
- Without explicit trigger, keep current non-bulk execution behavior.
- Invalid/ambiguous trigger input fails safe with remediation.

### 2) Work-item selection and breadcrumbs

Selection policy must be deterministic and logged:
- selected sprint/story id
- selection policy source
- team-context snapshot (when enabled):
  `TEAM_MODE`, `TEAM_MEMBER`, `ACTIVE_TASK_IDS`

### 3) Isolation and loop contract

- Fresh subagent context is mandatory per phase for each item.
- Fresh subagent context is mandatory for each execute↔QA loop cycle.
- Loop bounds (`AUTO_IMPLEMENTATION_LOOP`, max cycles) apply per item.

### 4) Team-scope enforcement model

When `TEAM_MODE=1`:
- only tasks in `ACTIVE_TASK_IDS` for the current `TEAM_MEMBER` are executable,
- pre-mutation scope validation is mandatory before task execution writes,
- out-of-scope tasks must be handled deterministically:
  - `skip` with reason code, or
  - `block` with reason code based on configured policy,
- no writes are allowed for out-of-scope tasks.

### 5) Bounded controls and stop policy

Required bounded controls:
- max items per run
- block handling policy (`stop` or `skip`)

Deterministic stop/skip outcomes:
- max items reached
- blocked item stop
- blocked item skipped
- no eligible scoped items
- decision gate pause

### 6) Resume semantics

Interrupted bulk runs require deterministic checkpoint fields:
- last completed item
- next candidate item
- stop reason
- stop phase
- team-context snapshot (if team mode)

Resume must continue safely from recorded checkpoint state.

### 7) Risk model

| Risk | Mitigation |
|------|------------|
| Duplicate or conflicting team execution | member-scope filter + no-write rule for out-of-scope tasks |
| Long unattended runs hide failures | bounded controls + deterministic reason-code breadcrumbs |
| Context bleed between items | fresh subagent per phase and per execute↔QA cycle |
| Ambiguous resume after interruption | explicit checkpoint schema with next-item and stop metadata |

## Decision linkage

- Research basis: `R-0010`, `R-0012`, `R-0013`
- Decision: `DEC-0024`

---

