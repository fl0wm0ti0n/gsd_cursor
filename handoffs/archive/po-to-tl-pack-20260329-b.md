# PO to TL archive pack (2026-03-29)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 31
- First archived heading: `## Discovery Addendum — US-0079`
- Last archived heading: `## Discovery Addendum — US-0079`
- Verification tuple (mandatory):
  - archived_body_lines=39
  - retained_body_lines=788

---

## Discovery Addendum — US-0079

### Closure

**`/discovery`** (**PO**) complete for **`US-0079`** — First-Class Bug Issue Workflow (`orchestrator_run_id=auto-20260329-01`).

### Alternatives (revalidated)

1. **US-only for defects** — lowest doc churn; conflates feature intent with defects and weakens defect traceability (**rejected** for this story).
2. **Heavyweight triage** (severity/SLA states) — **out of scope** per backlog boundaries (**rejected**).
3. **First-class `BUG-xxxx` + `OPEN`/`DONE` only** — matches operator intent, **R-0056**, and **US-0042**/**US-0045** extension path (**selected**).

### Recommended path (TL / research / architecture)

- **Identity**: Deterministic **`BUG-xxxx`** namespace and ordering parallel to **`US-xxxx`** (**AC-1**).
- **Canonical storage (discovery preference)**: Dedicated bug region in **`docs/product/backlog.md`** first; split artifact only if scale demands it — **architecture** confirms (**AC-1**, **US-0045**).
- **Routing**: Explicit bug-vs-feature classification in intake/command flows — no silent default to **`US-xxxx`** for defect reports (**AC-2**).
- **Schema**: Minimum reproducibility fields + evidence refs (**AC-4**); lifecycle states **`OPEN`**/**`DONE`** only (**AC-3**).
- **Traceability**: Sprint tasks, QA, verify-work, release, **`/ask`** surfaces, and reconciliation extend to **`BUG-xxxx`** without regressing US paths (**AC-5–AC-8**).
- **Anti-duplication**: One canonical defect record; optional cross-links when a bug drives feature work (**R-0056** risks).
- **Governance**: New or amended **DEC** in **`/architecture`** for bug-vs-story boundaries and migration (**AC-10**).

### Evidence

- **`docs/product/backlog.md`** — **US-0079** discovery closure notes; **`docs/product/vision.md`** — **Discovery Notes — US-0079**.
- **`docs/engineering/research.md`** — **`R-0056`** discovery traceability line.
- **`handoffs/resume_brief.md`** → **`/research`**; **`docs/engineering/decisions.md`** context pack updated.

### Next

- **`/research`** for **`US-0079`** (deepen routing/schema/reconciliation patterns; extend **R-0056** or successor as needed).
- **`/architecture`** after research to lock **DEC**, storage, and validator contracts.

### Strict proof pointer

- Isolation + runtime proof tuple: **`docs/engineering/state.md`** — **Discovery checkpoint (2026-03-29) — US-0079 / auto-20260329-01**.

---

