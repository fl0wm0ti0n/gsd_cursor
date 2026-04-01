# PO to TL archive pack (2026-03-31)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 41
- First archived heading: `## Intake Addendum — Backlog Reconciliation After Release`
- Last archived heading: `## Intake Addendum — Backlog Reconciliation After Release`
- Verification tuple (mandatory):
  - archived_body_lines=54
  - retained_body_lines=757

---

## Intake Addendum — Backlog Reconciliation After Release

### New intake

User reports repeated drift: sprint/release artifacts show completion while
`docs/product/backlog.md` still shows story status/ACs as incomplete.

Primary requirement:
- this mismatch must be solved structurally and must not happen again.

### Overlap and duplicate evaluation

- Related stories:
  - `US-0025` (backlog-to-sprint traceability): defines linkage/index behavior.
  - `US-0024` (memory drift audit): read-only detection/reporting.
  - `US-0040`/`US-0042`: release queue + release findings artifacts.
- Assessment:
  - No direct duplicate for **enforced post-release backlog reconciliation**.
  - Existing items either provide traceability or audit visibility, but do not
    enforce deterministic backlog mutation/fail-safe behavior at release boundary.
- Decision:
  - Create a focused story `US-0043` to make this invariant explicit and testable.

### Accepted story

#### US-0043 — Backlog Reconciliation Gate for Released Sprints
- Priority: P1
- Status: OPEN
- Intent: prevent recurrence of release/backlog contradiction by enforcing
  deterministic reconciliation or fail-safe blocking with explicit reason code.

### TL guidance and boundaries

- In scope:
  - Define canonical evidence precedence for reconciliation.
  - Add deterministic release-boundary reconciliation step.
  - Add fail-safe reason code and remediation contract for drift.
  - Add regression tests for positive and negative reconciliation paths.
  - Keep active/template command/rule/docs behavior aligned.
- Out of scope:
  - Replacing story ownership semantics.
  - Reworking sprint lifecycle phases.
  - Runtime product feature changes unrelated to workflow integrity.

### Planning recommendation

1. Define a single source-of-truth precedence for completion evidence.
2. Wire reconciliation at `/release` finalize boundary (or explicit
   post-release reconciliation step with equivalent guarantees).
3. Add deterministic reason-code/error output for contradictory states.
4. Add tests covering stale backlog after release and successful auto-reconcile.

---

