# PO to TL archive pack (2026-04-03)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 44
- First archived heading: `## PO -> TL Handoff - BUG-0007 (Intake)`
- Last archived heading: `## PO -> TL Handoff - BUG-0007 (Intake)`
- Verification tuple (mandatory):
  - archived_body_lines=28
  - retained_body_lines=800

---

## PO -> TL Handoff - BUG-0007 (Intake)

### Summary

- New canonical bug: **`BUG-0007`** — intake evidence records asked questions that were never asked.
- Intake mode: **`/intake bug`**; selected pack: **`small-intake-pack`**.
- Evidence bundle: `handoffs/intake_evidence/BUG-0007-intake-20260403.json`.
- User-provided example artifact: `handoffs/intake_evidence/BUG-0006-intake-20260403.json`.

### Problem framing

- Intake contract requires truthful evidence binding between asked topics and covered answers.
- Report indicates generated `asked_topics` + `topic_coverage` can claim user answers for required topics without an actual question round.
- This is an intake-evidence integrity defect, not just phrasing quality.

### Discovery targets

1. Reconstruct intake writer path that populates `asked_topics` and `topic_coverage`.
2. Verify whether "asked-vs-covered" rule is being bypassed by synthetic default text.
3. Define fail-fast behavior when required topic prompts were not actually asked (`INTAKE_PERSISTENCE_BLOCKED` path).
4. Add regression tests for short `/intake bug` reports to ensure no fabricated asked/answered rows.

### Suggested next phase

- **`/discovery`** for `BUG-0007` in fresh **PO** context.

---

