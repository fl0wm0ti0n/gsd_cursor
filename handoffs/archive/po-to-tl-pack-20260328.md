# PO to TL archive pack (2026-03-28)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 29
- First archived heading: `## PO → TL Handoff — US-0078 (Intake)`
- Last archived heading: `## PO → TL Handoff — US-0078 (Intake)`
- Verification tuple (mandatory):
  - archived_body_lines=20
  - retained_body_lines=800

---

## PO → TL Handoff — US-0078 (Intake)

- Scope: fix intake runtime gap where required question-pack topics and `assumptions_confirmed`
  can be persisted without explicit interaction evidence.
- Problem evidence: observed intake output claimed deterministic pack coverage while user reports
  no questions were asked; this conflicts with US-0068 fail-closed intent.
- Overlap: extends enforcement of **US-0068 / DEC-0050** and adaptive questioning **US-0051**
  without changing decomposition heuristics.
- Recommendation: architecture should lock an evidence model (e.g., answered-topic refs and
  assumption-confirmation refs), fail-closed diagnostics, and migration for existing artifacts.
- Research anchor: `R-0055`.
- Intake pack evidence:
  - selected_pack=`small-intake-pack`
  - asked_topics=`outcome_success_criteria`,`impacted_components`,`constraints_compatibility_risks`,`required_tests_acceptance_checks`,`done_definition`
  - missing_topics=`(none)`
  - assumptions_confirmed=`(none)`
- Next: `/discovery` for `US-0078`.

---

