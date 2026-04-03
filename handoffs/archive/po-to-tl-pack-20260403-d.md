# PO to TL archive pack (2026-04-03)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 43
- First archived heading: `## Intake Addendum — Explicit Bulk Planning + Bulk Execution Modes`
- Last archived heading: `## Intake Addendum — Explicit Bulk Planning + Bulk Execution Modes`
- Verification tuple (mandatory):
  - archived_body_lines=61
  - retained_body_lines=742

---

## Intake Addendum — Explicit Bulk Planning + Bulk Execution Modes

### New intake

User requests two explicit high-autonomy capabilities:
1. Bulk sprint planning mode so one command can plan many OPEN stories.
2. Bulk execution mode so planned sprints/stories run with fresh agent contexts
   and execute↔QA loops until bounded stop conditions.

### Overlap and duplicate evaluation

- Related stories:
  - `US-0023`: fresh subagent context per phase/handoff (already established).
  - `US-0044`: optional `/auto` backlog-drain mode with bounded controls.
  - `US-0045`: canonical status source and drift guard.
- Assessment:
  - not a duplicate of `US-0044`; this intake requests explicit command-level
    bulk modes (especially for planning) rather than only flag-driven behavior.
  - complements `US-0023`; preserves and operationalizes fine-granular context
    isolation in explicit bulk execution semantics.
  - compatible with `US-0045`; status integrity remains orthogonal to planning/
    execution batching behavior.
- Research reference:
  - `R-0010` (explicit bulk modes + deterministic bounded orchestration).
- Decision:
  - create two dedicated stories: `US-0046` (bulk sprint planning) and
    `US-0047` (bulk execute orchestration).

### Accepted stories

#### US-0046 — Explicit `/sprint-plan --bulk` Mode
- Priority: P1
- Status: OPEN
- Intent: allow explicit, bounded planning of multiple OPEN stories in one run
  while preserving sizing/splitting safety.

#### US-0047 — Explicit Bulk Execute Orchestration Mode
- Priority: P1
- Status: OPEN
- Intent: allow explicit, bounded multi-item execution with mandatory fresh
  subagent isolation and deterministic execute↔QA loop controls.

### TL guidance and boundaries

- In scope:
  - explicit mode contracts for bulk planning and bulk execution
  - deterministic selection/grouping and bounded limits
  - stop/skip reason-code semantics and breadcrumb auditability
  - strict preservation of decision gates and fail-safe behavior
  - active/template parity for command/rule/docs updates
- Out of scope:
  - runtime product feature changes
  - bypassing release/decision safety controls
  - replacing artifact-first handoff model

### Suggested implementation order

1. `US-0046` first to make backlog-to-sprint generation explicit and bounded.
2. `US-0047` second to consume planned backlog/sprint scope in autonomous runs
   with strict context isolation guarantees.

