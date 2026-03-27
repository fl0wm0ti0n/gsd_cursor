# PO to TL archive pack (2026-03-27)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 23
- First archived heading: `## PO → TL Handoff — US-0077 (Intake)`
- Last archived heading: `## PO → TL Handoff — US-0077 (Intake)`
- Verification tuple (mandatory):
  - archived_body_lines=40
  - retained_body_lines=765

---

## PO → TL Handoff — US-0077 (Intake)

### New intake

Request: make documentation output configurable from technical to user-friendly, with explicit
audience targeting and a dual README strategy.

### Overlap

- `US-0031` (DONE): technical spec-pack mode exists; does not control README audience/depth.
- `US-0032` (DONE): user-guide mode exists; does not coordinate profile-driven README output.
- `US-0030` (DONE): README/runbook parity gate exists; new profile rules must integrate.

### Decomposition

- **Single story** `US-0077` to keep profile policy + artifact generation + validation in one
  vertical slice.

### Intake pack

- selected_pack=`small-intake-pack`
- asked_topics=`outcome_success_criteria`,`impacted_components`,`constraints_compatibility_risks`,`required_tests_acceptance_checks`,`done_definition`
- missing_topics=`(none)`
- assumptions_confirmed=`(none)`

### TL scope

- Define scratchpad profile keys for audience and detail level.
- Specify deterministic README strategy and section ownership boundaries.
- Preserve compatibility with `SPEC_PACK_MODE` and `USER_GUIDE_MODE`.
- Add profile-aware validation + regression matrix with deterministic reason codes.
- Intake research reference: `R-0054` (Diataxis-aligned audience split).

### Recommendation

Proceed with `/discovery` for `US-0077`, then `/architecture` to lock profile semantics and
migration behavior for existing repos.

---

