# PO to TL archive pack (2026-06-12)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 14
- First archived heading: `## Orchestrated sprint-plan handoff — BUG-0012 / S0085 / auto-20260612-01`
- Last archived heading: `## Orchestrated sprint-plan handoff — BUG-0012 / S0085 / auto-20260612-01`
- Verification tuple (mandatory):
  - archived_body_lines=51
  - retained_body_lines=789

---

## Orchestrated sprint-plan handoff — BUG-0012 / S0085 / auto-20260612-01

### Target

- `bug_id=BUG-0012`
- `sprint_id=S0085`
- `orchestrator_run_id=auto-20260612-01`
- phase completed: **`sprint-plan`** (**`tech-lead`**)
- `fresh_context_marker=tl-S0085-BUG0012-sprint-plan-20260612T223000Z-fresh`
- `next_scheduled_phase=plan-verify`
- `segment_work_item_kind=bug`
- `dec_id=DEC-0081`

### Summary

- **`/sprint-plan`** **PASS** — sprint **`S0085`** created; **AC-1..AC-8** surjective via **T-001..T-008** (8 architecture seeds 1:1); `task_count=8`, `within_limit=true` (≤ `SPRINT_MAX_TASKS=12`); `plan-verify.json` status **PENDING**.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1 | Orchestrator MUST Task-spawn mandate + actor distinction |
| T-002 | AC-2 | Native chain supersedes Option B; scope US-0088 fallback |
| T-003 | AC-3, AC-4 | Drain-advance step 7 no-stop + `drain_advance_action` |
| T-004 | AC-4, AC-7 | `native_chain_continuing` + resume_brief spawn pairing |
| T-005 | AC-5 | Four `test_bug0012_*` contract subtests |
| T-006 | AC-6 | Forbidden-prose negative grep |
| T-007 | AC-8 | Runbook § BUG-0012 regression verify E2E |
| T-008 | AC-8 | Template parity `--scope=bug-0012` + DEC linkage assert |

### Evidence refs

- `sprints/S0085/sprint.md`, `sprints/S0085/tasks.md`, `sprints/S0085/plan-verify.json`, `sprints/S0085/summary.md`
- `decisions/DEC-0081.md`
- `docs/engineering/architecture.md` (**`# BUG-0012`**)
- `docs/product/backlog.md` (`### BUG-0012` `sprint_plan_notes`)
- `handoffs/tl_to_dev.md` (S0085 handoff prepended)
- `handoffs/qa_plan_verify.md` (S0085 PENDING queue)
- `docs/engineering/state.md` (Sprint-plan checkpoint — this run)

### Next

- **`/plan-verify`** (fresh **qa** context) for **`S0085`** / **`BUG-0012`**.

### Decision gate

- **None** — sprint plan satisfied; bug **OPEN**.

---

