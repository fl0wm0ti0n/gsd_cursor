# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 14
- First archived heading: `## Orchestrated sprint-plan handoff — BUG-0011 / S0080 / auto-20260606-02`
- Last archived heading: `## Orchestrated sprint-plan handoff — BUG-0011 / S0080 / auto-20260606-02`
- Verification tuple (mandatory):
  - archived_body_lines=52
  - retained_body_lines=754

---

## Orchestrated sprint-plan handoff — BUG-0011 / S0080 / auto-20260606-02

### Target

- `bug_id=BUG-0011`
- `sprint_id=S0080`
- `orchestrator_run_id=auto-20260606-02`
- phase completed: **`sprint-plan`** (**`tech-lead`**)
- `fresh_context_marker=tl-S0080-BUG0011-sprint-plan-20260606T164329Z-fresh`
- `next_scheduled_phase=plan-verify`
- `dec_id=DEC-0077`
- `segment_work_item_kind=bug`
- `bug_queue_position=3` / `bug_queue_remaining=1` (sole OPEN bug)

### Summary

- **`/sprint-plan`** **PASS** — sprint **`S0080`** created; **AC-1..AC-8** surjective via **T-001..T-008**; `task_count=8`, `within_limit=true` (≤ `SPRINT_MAX_TASKS=12`); `plan-verify.json` status **PENDING**.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1, AC-2, AC-3, AC-4 | Voice section append to `caveman.mdc` (+ template mirror) |
| T-002 | AC-6 | Runbook `#### Voice compression levels` |
| T-003 | AC-5 | Nine `test_caveman_voice_*` subtests |
| T-004 | AC-5 | SHA baseline bump |
| T-005 | AC-8 | Harness **§30A** |
| T-006 | AC-7 | `test_caveman_default_off_*` regression guard |
| T-007 | AC-8 | Operator voice UAT spot-check |
| T-008 | AC-1 | Architecture + DEC linkage assert |

### Evidence refs

- `sprints/S0080/sprint.md`, `sprints/S0080/tasks.md`, `sprints/S0080/plan-verify.json`
- `decisions/DEC-0077.md`
- `docs/engineering/architecture.md` (**`# BUG-0011`**)
- `docs/product/backlog.md` (`### BUG-0011` `sprint_plan_notes`)
- `handoffs/tl_to_dev.md` (S0080 handoff prepended)
- `handoffs/qa_plan_verify.md` (S0080 PENDING queue)
- `docs/engineering/state.md` (Sprint-plan checkpoint — this run)

### Next

- **`/plan-verify`** (fresh **qa** context) for **`S0080`** / **`BUG-0011`**.

### Decision gate

- **None** — sprint plan satisfied; bug **OPEN**.

---

