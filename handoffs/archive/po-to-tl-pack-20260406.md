# PO to TL archive pack (2026-04-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 45
- First archived heading: `## Discovery Addendum — US-0046 and US-0047`
- Last archived heading: `## Discovery Addendum — US-0046 and US-0047`
- Verification tuple (mandatory):
  - archived_body_lines=50
  - retained_body_lines=755

---

## Discovery Addendum — US-0046 and US-0047

### Discovery focus and references

- Discovery objective: convert intake-level bulk-mode intent into architecture-
  ready orchestration constraints with deterministic safety boundaries.
- References captured:
  - existing `/auto` bounded backlog-drain semantics (`US-0044`)
  - fresh-context isolation contract (`US-0023`)
  - team-local context fields (`TEAM_MODE`, `TEAM_MEMBER`, `ACTIVE_TASK_IDS`)
  - research anchor: `R-0010`

### Discovery conclusions for TL

- Bulk behavior should be command-explicit, not implicit:
  - normal mode stays lightweight and predictable
  - bulk mode activates only on explicit operator intent.
- `US-0046` should remain planning-only:
  - may generate multiple sprint plans in one run
  - must preserve all sizing/splitting and completeness guarantees.
- `US-0047` should remain execution-only:
  - consumes planned scope
  - preserves strict fresh-context isolation and execute↔QA loop safety bounds.
- Team mode must be execution-scoping aware in bulk runs:
  - only in-scope member tasks execute
  - out-of-scope tasks are deterministically skipped/blocked with reason codes.

### Research handoff targets

1. Define explicit bulk-mode triggers and precedence when both normal and bulk
   inputs are present.
2. Define deterministic selection/grouping policies and boundary-limit behavior
   for `US-0046`.
3. Define deterministic execution selection, skip/stop semantics, and resume
   checkpoint schema for `US-0047`.
4. Define team-context enforcement contract (`TEAM_MEMBER`/`ACTIVE_TASK_IDS`)
   and failure/skip reason-code vocabulary.
5. Define regression matrix for positive throughput, bounded-stop behavior, and
   non-execution of out-of-scope tasks.

### Recommendation

- Proceed to `/research` for `US-0046` and `US-0047` with emphasis on
  deterministic explicit-mode contracts, member-scope enforcement, and bounded
  orchestration safety.

---

# PO -> TL Handoff — Intake: Install Hygiene + Smart Intake + Bootstrap IDs

