# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 24
- First archived heading: `## Orchestrated discovery handoff — BUG-0003 / auto-20260331-03`
- Last archived heading: `## Orchestrated research handoff — BUG-0003 / auto-20260331-03`
- Verification tuple (mandatory):
  - archived_body_lines=54
  - retained_body_lines=794

---

## Orchestrated discovery handoff — BUG-0003 / auto-20260331-03

### Target

- `bug_id=BUG-0003`
- `orchestrator_run_id=auto-20260331-03`
- phase completed: **`discovery`** (**`po`**)
- `next_scheduled_phase=research`

### Summary

- Discovery confirms a bounded follow-up defect, not a new feature request: the unresolved risk surface is mode-specific installer completeness in `missing` and `upgrade`, with reported miss `scripts/enforce-triad-hot-surface.py`.
- Overlap with **`BUG-0001`** is lineage-only (`duplicate_of`) rather than closure-equivalence: baseline intake payload parity was fixed, but this gap is about mode-path copy/skip behavior and completeness validation after run.
- Research is now ready and scoped: (1) map per-mode branching and skip predicates in `installer.ps1` / `installer.sh` / `installer.py`, (2) define deterministic required-script inventory contract for post-install completeness, and (3) define parity/regression checks proving `missing`/`upgrade` cannot silently omit framework-critical scripts.
- Canonical status authority unchanged (**US-0045**): **`docs/product/backlog.md`** keeps **`BUG-0003`** **OPEN**; acceptance bug row remains unchecked.

### Evidence refs

- `docs/product/backlog.md` (**`## Bug issues (canonical)`** / **`### BUG-0003`** — discovery addendum)
- `handoffs/intake_evidence/BUG-0003-intake-20260331-b.json`
- `docs/engineering/state.md` (**Discovery checkpoint (2026-03-31) — BUG-0003 / auto-20260331-03**)
- `handoffs/resume_brief.md`

---

## Orchestrated research handoff — BUG-0003 / auto-20260331-03

### Target

- `bug_id=BUG-0003`
- `orchestrator_run_id=auto-20260331-03`
- phase completed: **`research`** (**`tech-lead`**)
- `next_scheduled_phase=architecture`

### Summary

- **`R-0061`** documents mode-branch inventory for `missing`/`upgrade` across `installer.ps1`, `installer.sh`, and `installer.py`: branch behavior is parity-aligned, so observed misses are inventory-source issues rather than branch drift.
- Research identifies the concrete gap: manifest-driven install source of truth omits `scripts/enforce-triad-hot-surface.py`, allowing successful `missing`/`upgrade` runs with incomplete framework script payload.
- Recommended architecture direction: keep installer ownership manifest as single required-script source of truth, add deterministic post-install completeness diagnostics, and lock parity regression tests for `missing`/`upgrade` (active + template surfaces).
- Canonical status authority unchanged (**US-0045**): **`docs/product/backlog.md`** keeps **`BUG-0003`** **OPEN**; acceptance bug row remains unchecked.

### Evidence refs

- `docs/engineering/research.md` (**`R-0061`**)
- `docs/product/backlog.md` (**`## Bug issues (canonical)`** / **`### BUG-0003`**)
- `installer.ps1`
- `installer.sh`
- `installer.py`
- `docs/engineering/context/installer-owned-paths.manifest`
- `docs/engineering/state.md` (**Research checkpoint (2026-03-31) — BUG-0003 / auto-20260331-03**)
- `handoffs/resume_brief.md`

---

