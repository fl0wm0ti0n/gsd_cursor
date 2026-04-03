# PO to TL archive pack (2026-04-03)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 43
- First archived heading: `## PO -> TL Handoff - BUG-0005 (Intake)`
- Last archived heading: `## PO -> TL Handoff - BUG-0005 (Intake)`
- Verification tuple (mandatory):
  - archived_body_lines=47
  - retained_body_lines=773

---

## PO -> TL Handoff - BUG-0005 (Intake)

### Intake context

User reports `/auto` fails immediately after a canonical bug intake:

- prior bug intake completed for `BUG-0004`
- command run next: `/auto`
- observed failure: `AUTO_RESUME_ERROR` with stale resume target (`resume target says intake`)

### Duplicate/overlap evaluation

- Related items:
  - `BUG-0004` (installer shell-option failure) - different defect class.
  - `US-0037` / `US-0070` (auto resume and phase selection contracts).
  - `US-0045` (canonical status and derived-artifact reconciliation expectations).
- Assessment:
  - not a duplicate of `BUG-0004`; this intake targets orchestrator continuation state after intake, not installer runtime behavior.
  - likely a handoff/freshness mismatch where `resume_brief` remains pre-intake while backlog reflects new open bug.
- Decision:
  - persist as `BUG-0005` under bug workflow.

### Intake evidence and routing

- selected_pack=`small-intake-pack`
- asked_topics=`outcome_success_criteria`,`impacted_components`,`constraints_compatibility_risks`,`required_tests_acceptance_checks`,`done_definition`
- missing_topics=`(none)`
- assumptions_confirmed=`(none)`
- evidence bundle: `handoffs/intake_evidence/BUG-0005-intake-20260403.json`
- routing: explicit `/intake bug` request (command-level bug mode) satisfied.

### TL discovery focus

1. Reconstruct deterministic sequence `/intake bug` -> `/auto` and identify where resume target freshness is lost.
2. Define canonical source precedence when intake creates a new open bug and `resume_brief` is stale (`resume_brief` vs backlog/state).
3. Decide bounded fix path:
   - update intake to refresh resume breadcrumbs after successful bug persistence, or
   - update `/auto` to accept valid post-intake canonical context without false `RESUME_BRIEF_STALE` block.
4. Preserve fail-fast diagnostics for truly invalid resume sources while eliminating this false-positive path.
5. Add regression coverage for immediate post-intake `/auto` continuation.

### Recommendation

Proceed to `/discovery` for `BUG-0005` and lock a deterministic non-ambiguous continuation contract before architecture.

---

