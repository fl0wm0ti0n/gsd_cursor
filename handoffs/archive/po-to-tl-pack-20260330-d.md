# PO to TL archive pack (2026-03-30)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 36
- First archived heading: `## Intake Addendum — BUG-0003 Missing scripts after missing/upgrade install`
- Last archived heading: `## Intake Addendum — BUG-0003 Missing scripts after missing/upgrade install`
- Verification tuple (mandatory):
  - archived_body_lines=61
  - retained_body_lines=745

---

## Intake Addendum — BUG-0003 Missing scripts after missing/upgrade install

### New intake

User reports scripts are still missing after new install/upgrade runs using modes `missing` or `upgrade`.

### Overlap and duplicate evaluation

- Related items:
  - `BUG-0001` (DONE): initial installer/template script omission issue.
  - `US-0008` / `US-0018`: installer behavior and upgrade compatibility scope.
- Assessment:
  - This appears as regression/remaining-gap behavior tied to install-mode semantics.
- Decision:
  - File `BUG-0003` and link to `BUG-0001` as duplicate/follow-up lineage.

### Accepted bug

#### BUG-0003 — Missing scripts still occur on install modes missing/upgrade
- Status: OPEN
- Intent: ensure `missing` and `upgrade` paths install complete required framework scripts without regressions.

### Intake evidence (US-0078 / DEC-0060)

- intake_run_id: `manual-20260331-BUG0003-intake`
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
  - `outcome_success_criteria` -> `ie:manual-20260331-BUG0003-intake:0:768b4db1e5b7d420`
  - `impacted_components` -> `ie:manual-20260331-BUG0003-intake:1:3d665d7e5ba486a7`
  - `constraints_compatibility_risks` -> `ie:manual-20260331-BUG0003-intake:2:b3cb8da205297562`
  - `required_tests_acceptance_checks` -> `ie:manual-20260331-BUG0003-intake:3:07dd09b460248f30`
  - `done_definition` -> `ie:manual-20260331-BUG0003-intake:4:bf8e459cf4ed4d73`
- evidence bundle: `handoffs/intake_evidence/BUG-0003-intake-20260331.json`

### TL guidance and boundaries

- In scope:
  - reproduce `missing` vs `upgrade` mode behavior for missing-script gaps.
  - validate required script inventory contract and mode-specific copy/skip logic.
  - add/install regression tests across PowerShell/Bash/Python parity paths.
- Out of scope:
  - unrelated command/rule workflow redesign.
  - broad template refactors beyond missing-script completeness.

### Planning recommendation

1. Build minimal repro matrix for `missing` and `upgrade` install modes.
2. Compare expected required script manifest vs installed results per mode.
3. Patch mode-specific install logic and parity manifests.
4. Add deterministic regression checks for both modes.

---

