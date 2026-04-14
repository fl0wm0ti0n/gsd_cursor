# PO to TL archive pack (2026-04-13)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 47
- First archived heading: `## Intake context (fresh PO run)`
- Last archived heading: `## Duplicate/overlap evaluation`
- Verification tuple (mandatory):
  - archived_body_lines=20
  - retained_body_lines=797

---

## Intake context (fresh PO run)

User reported real-world first-time install and cleanup trust gaps in external repos:

1. `--clean-repo` leaves framework artifacts behind.
2. Fresh installs still contain starter references/history that look like copied memory.
3. Broad intake still collapses into one oversized story with too few PO follow-up questions.
4. Fresh-project teams want optional ID bootstrap (`US-0001` / `DEC-0001`).

## Duplicate/overlap evaluation

- Related stories:
  - `US-0018` (upgrade mode), `US-0019` (placeholder cleanup), `US-0041` (installer lifecycle QA), `US-0033` (guided intake behavior), `US-0046`/`US-0047` (bulk planning/execution).
- Assessment:
  - No direct duplicate for end-to-end clean-install hygiene + complete clean-repo coverage + starter neutrality policy.
  - No direct duplicate for intake decomposition heuristics plus risk-aware questioning.
  - No direct duplicate for explicit fresh-project ID namespace bootstrap.
- Decision:
  - Split into three stories (`US-0050`, `US-0051`, `US-0052`) to avoid one oversized mixed-scope intake.

