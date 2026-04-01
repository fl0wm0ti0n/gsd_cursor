# PO to TL archive pack (2026-03-31)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 43
- First archived heading: `## Intake Addendum — Canonical Story Status + Global Drift Normalization`
- Last archived heading: `## Intake Addendum — Canonical Story Status + Global Drift Normalization`
- Verification tuple (mandatory):
  - archived_body_lines=46
  - retained_body_lines=773

---

## Intake Addendum — Canonical Story Status + Global Drift Normalization

### New intake

User requests a durable fix for recurring status drift across
`docs/product/backlog.md`, `docs/product/acceptance.md`, and
`docs/engineering/state.md`, including known completed stories still marked OPEN.
Intake objective is to make this mismatch class deterministic and non-recurring.

### Overlap and duplicate evaluation

- Related stories:
  - `US-0043`: released-sprint backlog reconciliation at release boundary.
  - `US-0044`: optional multi-story `/auto` backlog-drain orchestration.
  - `US-0025`: backlog-to-sprint traceability contract (still OPEN).
- Assessment:
  - not a duplicate of `US-0043`; current scope is broader than release boundary
    and includes historical normalization + cross-artifact status ownership.
  - complements `US-0044`; automation breadth does not solve status authority.
  - compatible with `US-0025`; this intake focuses status truth and drift guard.
- Research reference:
  - `R-0009` (canonical source + reconciliation/normalization pattern).
- Decision:
  - create `US-0045` as a dedicated P1 workflow integrity story.

### Accepted story

#### US-0045 — Canonical Story Status Source + Global Drift Guard
- Priority: P1
- Status: OPEN
- Intent: establish one authoritative status source and deterministic
  reconciliation so OPEN/DONE contradictions stop recurring in normal operation.

### TL guidance and boundaries

- In scope:
  - canonical story-status ownership contract (backlog authoritative)
  - deterministic reconciliation rules across backlog/acceptance/state
  - one-time historical normalization with auditable output
  - fail-safe reason-code handling for contradictory states
  - command/rule/doc updates plus active/template parity checks
- Out of scope:
  - runtime application feature changes
  - bypassing release/decision safety gates
  - replacing sprint sizing/planning policy with unbounded batching

