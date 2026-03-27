# PO to TL archive pack (2026-03-27)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 26
- First archived heading: `## Discovery Addendum — US-0077`
- Last archived heading: `## Discovery Addendum — US-0077`
- Verification tuple (mandatory):
  - archived_body_lines=39
  - retained_body_lines=762

---

## Discovery Addendum — US-0077

### Discovery focus and references

- **Objective**: Refine **US-0077** into architecture-ready documentation profile semantics,
  dual-README / dual-doc boundaries, and validation contracts — anchored on **R-0054**
  (Diataxis-style audience split + docs-as-code).
- **References**: `docs/product/vision.md` (**Intake** + **Discovery Notes — US-0077**),
  `docs/product/backlog.md` (**US-0077**), `docs/engineering/research.md` (**R-0054**);
  constraints **US-0030**, **US-0031**, **US-0032**, **US-0071**.

### Discovery conclusions for TL

- **Strategy**: Prefer explicit **ownership matrix** + deterministic split (or clearly
  bounded dual sections) over single-README tone-only edits — reduces contradiction with
  optional user guides and spec-pack.
- **Controls**: Keep scratchpad profile pair minimal; fail-closed invalid combinations;
  cap growth for `both` + `technical-deep` via section budgets and/or split artifacts.
- **Gates**: Profile completeness = deterministic required sections per cell + template
  parity; user-visible outputs stay **US-0071**-clean.

### Research handoff

- Extend **R-0054** with: mandatory section matrix per profile cell, recommended file split
  vs single-file layout, conflict rules when optional modes are enabled, and scoped test
  matrix notes for **AC-8**.

### Recommendation

- **`/research`** (**R-0054** extension) → **`/architecture`** (new/amended **DEC** per **AC-10**).

### Decision gate before research

- **None** — remaining choices (exact paths, budgets, validator placement) are
  research/architecture-owned; **no** PO product gate should stop **`/auto`** before
  **`/research`**.

---

