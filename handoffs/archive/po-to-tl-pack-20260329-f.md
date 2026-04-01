# PO to TL archive pack (2026-03-29)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 32
- First archived heading: `## Architecture Addendum — US-0078`
- Last archived heading: `## Architecture Addendum — US-0078`
- Verification tuple (mandatory):
  - archived_body_lines=24
  - retained_body_lines=789

---

## Architecture Addendum — US-0078

### Closure

**`/architecture`** (**tech-lead**) complete for **`US-0078`** (`orchestrator_run_id=auto-20260328-01`).

### Decision

- **`decisions/DEC-0060.md`** — interactive intake evidence; canonical **`ref`** = **`ie:<intake_run_id>:<turn_index>:<sha256_16>`** (sorted-key JSON hash payload per §4); extends **`DEC-0050`** without replacing pack lists.

### Architecture

- **`docs/engineering/architecture.md`** **`# US-0078`** — evidence model, validation pipeline, guided/low-touch parity, risks, **`AC-8`** ↔ **`R-0055`**, migration (grandfather until next intake mutation).

### Next

- **`/sprint-plan`** for **`US-0078`**.

### Decision gate before sprint-plan

- **None** — normative schema, **`ref`** format, and migration policy are locked.

---

