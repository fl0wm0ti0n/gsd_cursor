# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 25
- First archived heading: `## Orchestrated architecture handoff — US-0082 / auto-20260331-02`
- Last archived heading: `## Orchestrated intake handoff — BUG-0003 / auto-20260331-03`
- Verification tuple (mandatory):
  - archived_body_lines=55
  - retained_body_lines=798

---

## Orchestrated architecture handoff — US-0082 / auto-20260331-02

### Target

- `story_id=US-0082`
- `orchestrator_run_id=auto-20260331-02`
- phase completed: **`architecture`** (**`tech-lead`**)
- `next_scheduled_phase=sprint-plan`

### Summary

- **`DEC-0065`** locks phase-gated codebase map bootstrap: **`/architecture`** primary lifecycle guarantee (**tech-lead**), optional policy-gated **`/refresh-context`**, **`/map-codebase`** manual; idempotency, ownership, **`CODEBASE_MAP_*`** diagnostics, parity/regression expectations; **`docs/engineering/architecture.md`** **`# US-0082`**.
- Canonical backlog **Status** stays **OPEN** (**US-0045**); acceptance portfolio row for **US-0082** stays unchecked.
- Next: **`/sprint-plan`** — materialize sprint tasks against **AC-1..AC-10** under **`DEC-0065`** / **`R-0060`**.

### Evidence refs

- `decisions/DEC-0065.md`
- `docs/engineering/architecture.md` (**`# US-0082`**)
- `docs/engineering/decisions.md` (index + context pack)
- `docs/engineering/research.md` (**`R-0060`** architecture closure line)
- `docs/product/backlog.md` (**`## US-0082`** — architecture closure bullet)
- `handoffs/intake_evidence/US-0082-intake-20260331.json`
- `docs/engineering/state.md` (**Architecture checkpoint (2026-03-31) — US-0082 / auto-20260331-02**)
- `handoffs/resume_brief.md`
- `handoffs/tl_to_dev.md` (**US-0082** pre-sprint architecture section)

---

## Orchestrated intake handoff — BUG-0003 / auto-20260331-03

### Target

- `bug_id=BUG-0003`
- `orchestrator_run_id=auto-20260331-03`
- phase completed: **`intake`** (**`po`**)
- `next_scheduled_phase=discovery`

### Summary

- Canonical intake evidence remains authoritative: **`handoffs/intake_evidence/BUG-0003-intake-20260331-b.json`** (`selected_pack=small-intake-pack`, `missing_topics=[]`), revalidated for this boundary with **`[INTAKE_EVIDENCE_VALIDATION_OK]`**.
- Intake scope is bug-led and mode-specific: `missing`/`upgrade` installs still miss required scripts, with explicit reported gap `scripts/enforce-triad-hot-surface.py`; parity across `installer.ps1`, `installer.sh`, and `installer.py` remains mandatory.
- Canonical status authority unchanged (**US-0045**): **`docs/product/backlog.md`** keeps **`BUG-0003`** **OPEN**; acceptance bug row remains unchecked until downstream phases.
- Next: **`/discovery`** to isolate per-mode copy/skip logic and lock required script inventory contract before research/architecture.

### Evidence refs

- `docs/product/backlog.md` (**`## Bug issues (canonical)`** / **`### BUG-0003`**)
- `docs/product/acceptance.md` (**`## Bug acceptance (canonical)`**)
- `handoffs/intake_evidence/BUG-0003-intake-20260331-b.json`
- `docs/engineering/state.md` (**Intake checkpoint (2026-03-31) — BUG-0003 / auto-20260331-03**)
- `handoffs/resume_brief.md`

---

