# PO to TL archive pack (2026-03-27)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 24
- First archived heading: `## PO → TL Handoff — US-0077 (Intake)`
- Last archived heading: `## PO → TL Handoff — US-0077 (Intake)`
- Verification tuple (mandatory):
  - archived_body_lines=18
  - retained_body_lines=786

---

## PO → TL Handoff — US-0077 (Intake)

- Scope: configurable documentation profiles with `DOC_AUDIENCE_PROFILE=user|developer|both`
  and `DOC_DETAIL_LEVEL=concise|balanced|technical-deep`.
- Goal: deterministic user-friendly vs developer-technical output strategy, including a dual
  README approach with explicit ownership boundaries.
- Overlap: extends `US-0031`/`US-0032`; must stay compatible with `US-0030` parity gates.
- Research: `R-0054` (audience split model and docs-as-code constraints).
- Intake pack evidence:
  - selected_pack=`small-intake-pack`
  - asked_topics=`outcome_success_criteria`,`impacted_components`,`constraints_compatibility_risks`,`required_tests_acceptance_checks`,`done_definition`
  - missing_topics=`(none)`
  - assumptions_confirmed=`(none)`
- Recommendation: `/discovery` for `US-0077` then `/architecture` for profile semantics and
  migration details.

---

