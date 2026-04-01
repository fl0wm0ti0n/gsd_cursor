# PO to TL archive pack (2026-03-30)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 36
- First archived heading: `## Intake Addendum — BUG-0002 map-codebase output missing in fresh repos`
- Last archived heading: `## Intake Addendum — US-0081 First-Intake Full-Plan Coverage Gate`
- Verification tuple (mandatory):
  - archived_body_lines=125
  - retained_body_lines=745

---

## Intake Addendum — BUG-0002 map-codebase output missing in fresh repos

### New intake

User reports that in freshly created test repos, `docs/engineering/codebase-map.md` is not written after running `/map-codebase`.

### Overlap and duplicate evaluation

- Related items:
  - `US-0001` includes command surface baseline (`/map-codebase` exists).
  - No existing canonical bug issue tracks missing `codebase-map.md` output in fresh repos.
- Assessment:
  - Not a duplicate of `BUG-0001`; this is a different artifact-write defect.
- Decision:
  - File `BUG-0002` under bug workflow.

### Accepted bug

#### BUG-0002 — map-codebase does not write codebase-map in fresh repos
- Status: OPEN
- Intent: restore deterministic `/map-codebase` output behavior for fresh repos so required engineering map artifact is always created/updated.

### Intake evidence (US-0078 / DEC-0060)

- intake_run_id: `manual-20260331-BUG0002-intake`
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
  - `outcome_success_criteria` -> `ie:manual-20260331-BUG0002-intake:0:d9ce46389b897fab`
  - `impacted_components` -> `ie:manual-20260331-BUG0002-intake:1:845c246da40f500e`
  - `constraints_compatibility_risks` -> `ie:manual-20260331-BUG0002-intake:2:0424ff42f9198e9e`
  - `required_tests_acceptance_checks` -> `ie:manual-20260331-BUG0002-intake:3:e146723191b19c97`
  - `done_definition` -> `ie:manual-20260331-BUG0002-intake:4:9862c619670e9aa0`
- evidence bundle: `handoffs/intake_evidence/BUG-0002-intake-20260331.json`

### TL guidance and boundaries

- In scope:
  - Reproduce and isolate why `/map-codebase` skips `docs/engineering/codebase-map.md` in fresh repos.
  - Ensure deterministic write/create behavior and idempotent reruns.
  - Add regression coverage for fresh-repo path.
  - Keep active/template parity for command/rule references.
- Out of scope:
  - Redesigning command scope beyond expected output contract.
  - Unrelated installer/distribution changes.

### Planning recommendation

1. Reproduce in a minimal fresh repo with current installer payload.
2. Trace write path and preconditions for `codebase-map.md`.
3. Patch contract enforcement for required outputs.
4. Add fixture/regression tests and parity checks.

---

## Intake Addendum — US-0081 First-Intake Full-Plan Coverage Gate

### New intake

User reports a broad first intake in a test repo created only one small user story after follow-up, which is considered incorrect for full-plan capture. Required behavior: first broad intake must cover all major plan areas, even when delivery is phased.

### Overlap and duplicate evaluation

- Related stories:
  - `US-0051`: intake decomposition and risk-aware questioning.
  - `US-0068`: mandatory intake question packs.
  - `US-0078`: machine-verifiable intake evidence gate.
- Assessment:
  - Not a direct duplicate; current policies enforce questionnaire coverage and decomposition guidance but do not hard-enforce complete broad-plan coverage mapping.
- Decision:
  - Create `US-0081` to add a deterministic first-intake coverage-map gate.

### Accepted story

#### US-0081 — First-Intake Full-Plan Coverage and Story-Map Gate
- Priority: P1
- Status: OPEN
- Intent: block broad first-intake persistence until all identified plan areas are mapped to stories or explicitly deferred with rationale.

### Intake evidence (US-0078 / DEC-0060)

- intake_run_id: `manual-20260331-US0081-intake`
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
  - `outcome_success_criteria` -> `ie:manual-20260331-US0081-intake:0:f9b95e24ba99de7c`
  - `impacted_components` -> `ie:manual-20260331-US0081-intake:1:323aa726b46902ee`
  - `constraints_compatibility_risks` -> `ie:manual-20260331-US0081-intake:2:8ef89c7612e81b81`
  - `required_tests_acceptance_checks` -> `ie:manual-20260331-US0081-intake:3:861467f86be38785`
  - `done_definition` -> `ie:manual-20260331-US0081-intake:4:53e2347b4b964785`
- evidence bundle: `handoffs/intake_evidence/US-0081-intake-20260331.json`

### TL guidance and boundaries

- In scope:
  - broad-intake complete-plan inventory and story-map persistence contract.
  - deterministic fail-closed diagnostics when plan-area coverage is missing.
  - command/agent/docs/test updates with active/template parity.
- Out of scope:
  - forcing all mapped stories into one sprint.
  - altering downstream phase ownership or release semantics.

### Planning recommendation

1. Define machine-verifiable plan-area mapping schema for intake outputs.
2. Add persistence gate and reason codes (coverage missing -> blocked).
3. Update `/intake`, PO policy, runbook, and `/ask` guidance.
4. Add regression fixtures for full coverage, justified defer, and blocked writes.

---

