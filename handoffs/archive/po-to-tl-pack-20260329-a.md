# PO to TL archive pack (2026-03-29)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 31
- First archived heading: `## Intake checkpoint — US-0079 (2026-03-29)`
- Last archived heading: `## Intake checkpoint — US-0079 (2026-03-29)`
- Verification tuple (mandatory):
  - archived_body_lines=38
  - retained_body_lines=788

---

## Intake checkpoint — US-0079 (2026-03-29)

### Summary

**`/intake`** (**PO**) complete for **`US-0079`** — First-Class Bug Issue Workflow (**`orchestrator_run_id=auto-20260329-01`**).

### Scope (restated)

- Dedicated **`BUG-xxxx`** (or equivalent) identity vs **`US-xxxx`**, canonical storage + ordering (**backlog AC-1**).
- Intake routing: bugs classified as bug issues, not user stories (**AC-2**).
- Lifecycle: **`OPEN`** / **`DONE`** only — no mandatory severity/SLA/triage (**AC-3**).
- Minimum reproducibility schema: environment/context, steps, expected, actual, evidence refs (**AC-4**).
- Sprint tasks + QA/verify-work/release may reference bug IDs; **`US-0045`** reconciliation extended (**AC-5..AC-7**).
- **`/ask`** + template/command parity + DEC for boundaries (**AC-8..AC-10**).

### Evidence

- **`handoffs/intake_evidence/US-0079-intake-20260329.json`** — **`small-intake-pack`** with full **`topic_coverage`** (**`ie:`** refs per **DEC-0060**).
- Validator: `python scripts/intake_evidence_validate.py --file handoffs/intake_evidence/US-0079-intake-20260329.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**.
- **`docs/product/backlog.md`** — **US-0079** discovery notes updated; **`docs/product/vision.md`** — intake gate line.
- Prior research: **`R-0056`** (lightweight bug model, **`US-0045`** / **`US-0042`** alignment).

### Risks / TL focus

- Migration: avoid duplicate **US+BUG** tracking for the same defect; document conversion/link rules in architecture/DEC.
- Reconciliation: extend drift guards without regressing US-only paths.

### Next

- **`/discovery`** for **`US-0079`** (refine discovery notes, triad hygiene if **`po_to_tl`** / **`state`** hot-surface triggers).
- **Decision gate before discovery**: **none** (scope locked at backlog level).

### Strict proof pointer

- Isolation + runtime proof tuple: **`docs/engineering/state.md`** — **Intake checkpoint (2026-03-29) — US-0079 / auto-20260329-01**.

---

