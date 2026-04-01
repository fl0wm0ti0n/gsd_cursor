# PO to TL archive pack (2026-03-30)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 36
- First archived heading: `## Intake Addendum — US-0083 Delegable Intake Clarification`
- Last archived heading: `## Intake Addendum — US-0083 Delegable Intake Clarification`
- Verification tuple (mandatory):
  - archived_body_lines=64
  - retained_body_lines=745

---

## Intake Addendum — US-0083 Delegable Intake Clarification

### New intake

User reports intake questioning is currently too strict/repetitive and often runs into blocking missing-topic gates. Desired behavior: ask sensible context-aware questions, but allow the user to explicitly delegate unresolved decisions to the agent so intake can continue.

### Overlap and duplicate evaluation

- Related stories:
  - `US-0033`: guided vs low-touch intake behavior.
  - `US-0068`: mandatory first/small intake question packs.
  - `US-0078`: enforced intake evidence gate.
- Assessment:
  - Not a duplicate; current policies preserve safety but can still create hard-block UX when users intentionally want delegation.
- Decision:
  - Create `US-0083` to add explicit delegable non-blocking path while preserving deterministic safety contracts.

### Accepted story

#### US-0083 — Delegable Intake Clarification Without Hard Blocks
- Priority: P1
- Status: OPEN
- Intent: keep adaptive clarification and safety challenge behavior, but allow explicit user-owned delegation for unresolved topics with auditable evidence.

### Intake evidence (US-0078 / DEC-0060)

- intake_run_id: `manual-20260331-US0083-intake`
- selected_pack: `small-intake-pack`
- asked_topics:
  - `outcome_success_criteria`
  - `impacted_components`
  - `constraints_compatibility_risks`
  - `required_tests_acceptance_checks`
  - `done_definition`
- missing_topics: `(none)`
- assumptions_confirmed: `(none)`
- topic_coverage refs:
  - `outcome_success_criteria` -> `ie:manual-20260331-US0083-intake:0:f47320d1be598107`
  - `impacted_components` -> `ie:manual-20260331-US0083-intake:1:854c4d96dda606ec`
  - `constraints_compatibility_risks` -> `ie:manual-20260331-US0083-intake:2:3b0d3f45d05d2eb1`
  - `required_tests_acceptance_checks` -> `ie:manual-20260331-US0083-intake:3:c7f1e87db7bc5427`
  - `done_definition` -> `ie:manual-20260331-US0083-intake:4:ed44ed177b391355`
- evidence bundle: `handoffs/intake_evidence/US-0083-intake-20260331.json`

### TL guidance and boundaries

- In scope:
  - explicit delegation contract for unresolved intake topics.
  - validator/evidence semantics that distinguish delegated vs non-delegated gaps.
  - guided/low-touch parity and deterministic diagnostics.
  - command/agent/runbook/test updates with active/template parity.
- Out of scope:
  - disabling fail-closed behavior for non-delegated missing required topics.
  - unbounded autonomous assumption-making without user opt-in.

### Planning recommendation

1. Define explicit delegation syntax/field in intake flow and evidence schema.
2. Update validator rules for delegated-topic pass path vs non-delegated block path.
3. Update `/intake` + PO guidance to reduce repetitive prompts using context-aware collapsing.
4. Add regression fixtures for delegation pass and non-delegated fail-closed behavior.

---

