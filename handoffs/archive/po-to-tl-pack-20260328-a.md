# PO to TL archive pack (2026-03-28)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 29
- First archived heading: `## PO → TL Handoff — US-0079 (Intake)`
- Last archived heading: `## PO → TL Handoff — US-0079 (Intake)`
- Verification tuple (mandatory):
  - archived_body_lines=19
  - retained_body_lines=800

---

## PO → TL Handoff — US-0079 (Intake)

- Request: treat bug reports as first-class issues (not US stories) using official-style agile/dev
  workflow, but keep lifecycle simple (`OPEN`/`DONE`) and avoid severity/SLA/triage overhead.
- Scope: bug identifier/model + intake routing + traceability through sprint/QA/release and status
  reconciliation updates.
- Overlap: complements post-QA release issue handling (**US-0042**) and status ownership
  (**US-0045**); separate from intake-evidence hardening (**US-0078**).
- Research anchor: `R-0056`.
- Intake pack evidence:
  - selected_pack=`small-intake-pack`
  - asked_topics=`outcome_success_criteria`,`impacted_components`,`constraints_compatibility_risks`,`required_tests_acceptance_checks`,`done_definition`
  - missing_topics=`(none)`
  - assumptions_confirmed=`(none)`
- Recommendation: `/discovery` for `US-0079` then `/architecture` to lock bug-vs-story boundaries
  and migration rules.

---

