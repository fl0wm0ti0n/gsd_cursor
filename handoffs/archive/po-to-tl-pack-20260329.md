# PO to TL archive pack (2026-03-29)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 31
- First archived heading: `## PO → TL Handoff — US-0080 (Intake)`
- Last archived heading: `## PO → TL Handoff — US-0080 (Intake)`
- Verification tuple (mandatory):
  - archived_body_lines=19
  - retained_body_lines=788

---

## PO → TL Handoff — US-0080 (Intake)

- Request: create a token-cost hardening story with measurable targets; user reports cache-read tokens
  massively exceeding fresh input/output during repeated intake/auto usage in the same chat.
- Scope: command/context payload slimming + measurable run evidence, with explicit goal to reduce
  comparable `/auto` cache-read tokens by **50%**.
- Overlap: extends US-0053/DEC-0035 (token profile + compaction) and must preserve all safety gates
  (US-0048, US-0056, US-0069, US-0039).
- Research anchor: `R-0057`.
- Intake pack evidence:
  - selected_pack=`small-intake-pack`
  - asked_topics=`outcome_success_criteria`,`impacted_components`,`constraints_compatibility_risks`,`required_tests_acceptance_checks`,`done_definition`
  - missing_topics=`(none)`
  - assumptions_confirmed=`(none)`
- Recommendation: `/discovery` for `US-0080`, then `/architecture` to lock metric definitions and
  accepted trade-offs.

---

