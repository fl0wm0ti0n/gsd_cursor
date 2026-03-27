# PO to TL archive pack (2026-03-27)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 25
- First archived heading: `## Research Addendum — US-0076`
- Last archived heading: `## Research Addendum — US-0076`
- Verification tuple (mandatory):
  - archived_body_lines=9
  - retained_body_lines=797

---

## Research Addendum — US-0076

- **Closure**: **`/research`** (TL) for **US-0076** under `orchestrator_run_id=auto-20260327-01`; **`R-0053`** extended with implementation anchors + mitigations (`docs/engineering/research.md`).
- **Anchors**: **`validate-and-push.ps1`/`.sh`** — add merged scratchpad gate before push; reuse **`installer.py`** `merge_scratchpad_layers` / `parse_scratchpad_file` where feasible; runbook stays command source only.
- **Boundaries**: **`by_phase`** default = script invocation as phase boundary unless architecture documents **`state.md`/env/CLI** override; **AC-5** = bounded **`qa-findings.md`** scan + fixed sprint path in architecture.
- **Next**: **`/architecture`** — lock **DEC-0058** (or **DEC-0018** amendment), QA path glob, dry-run/exit-code contract, test plan (**AC-8**).

> **Placement**: prepended for hot visibility; if **DEC-0054** rollover archives top sections, a **tail** mirror of this addendum is appended after rollover (see file end).

