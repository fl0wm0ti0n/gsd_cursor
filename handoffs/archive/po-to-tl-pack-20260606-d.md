# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 22
- First archived heading: `## Orchestrated discovery handoff — BUG-0005 / auto-20260403-02`
- Last archived heading: `## Orchestrated discovery handoff — BUG-0005 / auto-20260403-02`
- Verification tuple (mandatory):
  - archived_body_lines=37
  - retained_body_lines=797

---

## Orchestrated discovery handoff — BUG-0005 / auto-20260403-02

### Target

- `bug_id=BUG-0005`
- `orchestrator_run_id=auto-20260403-02`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-BUG0005-discovery-20260403T193500Z-fresh`
- `next_scheduled_phase=research`

### Summary

- **Scope**: Post-**bug intake** `/auto` continuation — `handoffs/resume_brief.md` can still describe a pre-intake **`intake`** target, triggering **`AUTO_RESUME_ERROR` / `RESUME_BRIEF_STALE`** when `/auto` runs without explicit `start-from`. Discovery confirms this is **orchestration resume continuity**, not installer/runtime issues (**`BUG-0004`**) or installer payload completeness (**`BUG-0003`**).
- **Impacted surfaces**: `/auto` **resume-source precedence** (resume brief vs explicit start-from vs `docs/engineering/state.md` fallback); **`resume_brief` freshness** semantics and safe rewrite policy at intake boundaries; **intake→auto** breadcrumbs so the next scheduled phase matches the new bug context.
- **Canonical status** (**US-0045**): **`docs/product/backlog.md`** keeps **`BUG-0005`** **OPEN**; acceptance bug row stays unchecked.

### Evidence refs

- `docs/product/backlog.md` (**`### BUG-0005`** — `discovery_notes`)
- `handoffs/intake_evidence/BUG-0005-intake-20260403.json`
- `handoffs/resume_brief.md`
- `docs/engineering/state.md` (**Discovery checkpoint (2026-04-03) — BUG-0005 / auto-20260403-02**)

### Open questions for `/research`

1. Under what conditions should **`resume_brief`** be **auto-refreshed** or **superseded** after canonical bug intake vs requiring explicit operator rewrite?
2. What is the minimal **deterministic self-heal** (if any) that preserves resume precedence and fail-fast contracts (**US-0037**, **US-0070**) without masking real staleness?
3. **Regression matrix**: scripted or documented sequence **`/intake bug` → `/auto`** asserting valid phase resolution or expected deterministic error with **non-stale** semantics.
4. Interaction with **`state.md`** fallback when **`resume_brief`** is present but **invalid/stale** — align with existing **`AUTO_RESUME_ERROR`** vocabulary.

### Next

- **`/research`** (tech-lead) for **`BUG-0005`**; then architecture/sprint path per TL.
- **Decision gate before research**: none (discovery satisfied; bug **OPEN**).

---

