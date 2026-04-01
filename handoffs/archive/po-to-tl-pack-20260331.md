# PO to TL archive pack (2026-03-31)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 41
- First archived heading: `## Orchestrated intake handoff — US-0082 / auto-20260331-02`
- Last archived heading: `## Intake Addendum — BUG-0003 script-specific regression detail`
- Verification tuple (mandatory):
  - archived_body_lines=71
  - retained_body_lines=800

---

## Orchestrated intake handoff — US-0082 / auto-20260331-02

### Target

- `story_id=US-0082`
- `orchestrator_run_id=auto-20260331-02`
- phase completed: **`intake`** (**`po`**)
- `next_scheduled_phase=discovery`

### Summary

- Prior **`small-intake-pack`** evidence remains authoritative: **`handoffs/intake_evidence/US-0082-intake-20260331.json`** (`intake_run_id=manual-20260331-US0082-intake`). This run records the formal **`/auto`** intake boundary in **`docs/engineering/state.md`** only.
- Canonical backlog **Status** stays **OPEN** (**US-0045**); acceptance portfolio row for **US-0082** stays unchecked.
- Next: **`/discovery`** — refine lifecycle touchpoints for **`docs/engineering/codebase-map.md`**, ownership-safe triggers, **`/map-codebase`** manual path, diagnostics, and active/template parity scope already listed in **AC-1..AC-10**.

### Evidence refs

- `docs/product/backlog.md` (**`## US-0082`**)
- `docs/product/vision.md` (**Intake Notes — US-0082**)
- `handoffs/intake_evidence/US-0082-intake-20260331.json`
- `docs/engineering/state.md` (**Intake checkpoint (2026-03-31) — US-0082 / auto-20260331-02**)

---

## Intake Addendum — BUG-0003 script-specific regression detail

### New intake

User adds concrete repro detail for `BUG-0003`: `scripts/enforce-triad-hot-surface.py` is missing after installing `its-magic` in a new repo (reported on `missing`/`upgrade` paths).

### Overlap and duplicate evaluation

- Related items:
  - `BUG-0003`: existing open installer script-completeness regression.
  - `BUG-0001`: prior baseline installer script omission issue.
- Assessment:
  - Not a new bug ID; this is a concrete evidence addendum that narrows reproduction.
- Decision:
  - Append detail to `BUG-0003` and keep status `OPEN`.

### Intake evidence (US-0078 / DEC-0060)

- intake_run_id: `manual-20260331-BUG0003-intake-b`
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
  - `outcome_success_criteria` -> `ie:manual-20260331-BUG0003-intake-b:0:adedea9666737991`
  - `impacted_components` -> `ie:manual-20260331-BUG0003-intake-b:1:3bf31789a879b248`
  - `constraints_compatibility_risks` -> `ie:manual-20260331-BUG0003-intake-b:2:beb0115a9aca9570`
  - `required_tests_acceptance_checks` -> `ie:manual-20260331-BUG0003-intake-b:3:b466edf66052c63a`
  - `done_definition` -> `ie:manual-20260331-BUG0003-intake-b:4:a5cb9dfe463da408`
- evidence bundle: `handoffs/intake_evidence/BUG-0003-intake-20260331-b.json`

### TL guidance and boundaries

- In scope:
  - confirm whether `enforce-triad-hot-surface.py` belongs to required installed script set for `missing` and `upgrade`.
  - isolate where mode-specific filters/manifests drop this file.
  - add explicit regression checks for this script in install parity tests.
- Out of scope:
  - unrelated workflow policy changes outside installer completeness.

---

