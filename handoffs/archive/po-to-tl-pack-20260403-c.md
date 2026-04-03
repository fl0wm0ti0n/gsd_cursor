# PO to TL archive pack (2026-04-03)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 43
- First archived heading: `## PO -> TL Handoff - BUG-0006 (Intake)`
- Last archived heading: `## Discovery Addendum — US-0045`
- Verification tuple (mandatory):
  - archived_body_lines=71
  - retained_body_lines=766

---

## PO -> TL Handoff - BUG-0006 (Intake)

### Summary

- New canonical bug: **`BUG-0006`** — `/auto` executes phases without spawning required subagents.
- Intake mode: **`/intake bug`** (bug routing explicit); selected pack: **`small-intake-pack`**.
- Intake evidence bundle: `handoffs/intake_evidence/BUG-0006-intake-20260403.json` (all required topics covered, `missing_topics=[]`).

### Problem framing

- `/auto` is contractually an orchestrator that must spawn fresh role subagents per phase.
- Reported defect indicates phase work can execute directly in orchestrator context (missing required subagent spawn).
- Requested outcome explicitly includes deterministic fail-fast reason-code coverage.

### Scope for discovery/research

1. Confirm whether any code path allows phase execution without subagent spawn.
2. Define/confirm deterministic fail-fast reason code(s) for spawn violations (and remediation text).
3. Add regression coverage proving violation is blocked and reason-code evidence is emitted.
4. Preserve existing guarantees: phase-role enforcement, isolation evidence, strict runtime proof, and phase-boundary breadcrumbs.

### Suggested next phase

- **`/discovery`** for `BUG-0006` in fresh **PO** context.

---

## Discovery Addendum — US-0045

### Discovery focus and references

- Discovery objective: refine `US-0045` from intake scope into architecture-ready
  status-contract boundaries and operator-facing drift diagnostics.
- References captured:
  - product vision value statement for single-source status trust
  - current artifact set: `backlog.md`, `acceptance.md`, `state.md`
  - release boundary reconciliation precedent from `US-0043`
  - research anchor: `R-0009`

### Discovery conclusions for TL

- Canonical ownership should be explicit and singular:
  - `docs/product/backlog.md` owns story `OPEN|DONE`.
- Secondary artifacts should be treated as derived/reconciled views:
  - `docs/product/acceptance.md` for portfolio checklist visibility.
  - `docs/engineering/state.md` for checkpoint/evidence traceability.
- Historical drift already exists and needs one-time normalization before strict
  guardrails can become reliable.
- Operator UX must prefer deterministic explainability over silent mutation:
  emit per-story mismatch evidence and remediation guidance.

### Research handoff targets

1. Define precedence and conflict-resolution semantics when backlog, acceptance,
   and state disagree.
2. Define normalization entry criteria and safe mutation scope (targeted writes
   only, no broad rewrites).
3. Define reason-code contract for contradictory states and where the contract
   is enforced in release/reconciliation flow.
4. Define regression matrix for:
   - pre-existing drift normalization
   - post-normalization drift prevention
   - non-target-story non-mutation guarantees

### Recommendation

- Proceed to `/research` for `US-0045` with emphasis on deterministic precedence
  model, auditable normalization report schema, and fail-safe reason-code design.

---

