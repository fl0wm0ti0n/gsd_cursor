# PO to TL archive pack (2026-03-30)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 36
- First archived heading: `## Intake Addendum — US-0082 Agent-Driven Codebase Map Bootstrap`
- Last archived heading: `## Intake Addendum — US-0082 Agent-Driven Codebase Map Bootstrap`
- Verification tuple (mandatory):
  - archived_body_lines=62
  - retained_body_lines=745

---

## Intake Addendum — US-0082 Agent-Driven Codebase Map Bootstrap

### New intake

User clarifies `BUG-0002`: the issue is expectation/workflow ownership. They expected agents to have `docs/engineering/codebase-map.md` available automatically in fresh repos, not only via a remembered manual `/map-codebase` step.

### Overlap and duplicate evaluation

- Related items:
  - `BUG-0002`: initial report captured as defect-shaped behavior.
  - `US-0001`: command surface includes `/map-codebase` but not deterministic lifecycle auto-bootstrap ownership.
- Assessment:
  - This is better tracked as a workflow enhancement story than a standalone defect.
- Decision:
  - Reclassify into `US-0082` and close `BUG-0002` as expectation mismatch.

### Accepted story

#### US-0082 — Agent-Driven Codebase Map Bootstrap
- Priority: P1
- Status: OPEN
- Intent: define deterministic TL/Dev (or equivalent phase) responsibility to create/refresh `docs/engineering/codebase-map.md` for fresh repos so agent search context is reliably available.

### Intake evidence (US-0078 / DEC-0060)

- intake_run_id: `manual-20260331-US0082-intake`
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
  - `outcome_success_criteria` -> `ie:manual-20260331-US0082-intake:0:f014b8cea3c67745`
  - `impacted_components` -> `ie:manual-20260331-US0082-intake:1:3ae6a7bf8dd02e9a`
  - `constraints_compatibility_risks` -> `ie:manual-20260331-US0082-intake:2:3206c9e3d72c1825`
  - `required_tests_acceptance_checks` -> `ie:manual-20260331-US0082-intake:3:c44e7abbbf13e929`
  - `done_definition` -> `ie:manual-20260331-US0082-intake:4:8a726eb4e7c7c4bd`
- evidence bundle: `handoffs/intake_evidence/US-0082-intake-20260331.json`

### TL guidance and boundaries

- In scope:
  - deterministic phase trigger and owner for codebase-map bootstrap in fresh repos.
  - idempotent refresh behavior + deterministic diagnostics when skipped/blocked.
  - active/template parity and regression coverage.
- Out of scope:
  - broad autonomous architecture documentation beyond codebase-map contract.
  - unrelated installer/distribution redesign.

### Planning recommendation

1. Define canonical owner and phase trigger (TL vs Dev path).
2. Implement ownership-safe write/create behavior.
3. Document runbook/command expectations and fallback manual command.
4. Add fresh-repo and rerun regression tests.

---

