# PO to TL archive pack (2026-06-25)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 10
- First archived heading: `## Orchestrated sprint-plan handoff — US-0102 / S0092 / auto-20260615-02`
- Last archived heading: `## Orchestrated architecture handoff — US-0102 / auto-20260615-02`
- Verification tuple (mandatory):
  - archived_body_lines=114
  - retained_body_lines=635

---

## Orchestrated sprint-plan handoff — US-0102 / S0092 / auto-20260615-02

### Target

- `story_id=US-0102`
- `sprint_id=S0092`
- `orchestrator_run_id=auto-20260615-02`
- phase completed: **`sprint-plan`** (**`tech-lead`**)
- `fresh_context_marker=tl-S0092-US0102-sprint-plan-20260625T193000Z-fresh`
- `next_scheduled_phase=plan-verify`
- `decomposition=single_story` (per **US-0051**)
- `priority=P2`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=5`

### Summary

- **`/sprint-plan`** **PASS** — sprint **`S0092`** created; **AC-1..AC-10** surjective via **T-001..T-011**; `task_count=11`, `within_limit=true` (≤ `SPRINT_MAX_TASKS=12`); `plan-verify.json` status **PENDING**.
- **Binding decision**: **`DEC-0087`** — composes **DEC-0086** (do not amend).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1, AC-5 | **`MODEL_<PHASE>`** scratchpad keys + **`MODEL_ASK`** |
| T-002 | AC-10 | **`MODEL_RESOLVE=role_catalog`** enum + precedence docs |
| T-003 | AC-3, AC-7 | Catalog schema v2 role-based example JSON files |
| T-004 | AC-7 | Template stability — no vendor slugs in template |
| T-005 | AC-2, AC-4, AC-6 | **`model_tier_lib.py`** unified 5-step resolver |
| T-006 | AC-3, AC-8 | Catalog v2 validation + **`MODEL_CATALOG_SCHEMA_V2_INVALID`** |
| T-007 | AC-8 | **`model_tier_validate.py`** extensions + three new reason codes |
| T-008 | AC-10 | Runbook direct override + role catalog subsection |
| T-009 | AC-9 | Eight **`test_us0102_*`** contract subtests |
| T-010 | AC-9 | **`MODEL_TIER_OVERRIDES_PAIRS`** parity scope |
| T-011 | AC-9 | Harness **§26AA** |

### Evidence refs

- `sprints/S0092/sprint.md`, `sprints/S0092/tasks.md`, `sprints/S0092/plan-verify.json`
- `decisions/DEC-0087.md`
- `docs/engineering/architecture.md` (**`# US-0102`**)
- `docs/product/backlog.md` (`## US-0102` — `sprint_plan_notes`)
- `handoffs/tl_to_dev.md` (S0092 handoff prepended)
- `handoffs/qa_plan_verify.md` (S0092 PENDING queue)
- `docs/engineering/state.md` (Sprint-plan checkpoint — this run)

### Next

- **`/plan-verify`** (fresh **qa** context) for **`S0092`** / **`US-0102`**.

### Decision gate

- **None** — sprint plan satisfied; story **OPEN**.

---

## Orchestrated architecture handoff — US-0102 / auto-20260615-02

### Target

- `story_id=US-0102`
- `orchestrator_run_id=auto-20260615-02`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0102-architecture-20260625T190000Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `decomposition=single_story` (per **US-0051**)
- `priority=P2`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=5`

### Summary

- **`/architecture`** **PASS** — **`DEC-0087`** locked; **`# US-0102`** appended; **11** atomic task seeds; eight **`test_us0102_*`** contract markers + **`MODEL_TIER_OVERRIDES_PAIRS`** parity manifest.
- **5-step precedence**: `MODEL_<PHASE>` > tier > role_catalog > default > alias.
- **Extend in place**: **`model_tier_lib.py`** (no separate overrides module).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Architecture locks (sprint-plan inputs)

| Lock | Decision |
|------|----------|
| **Binding decision** | **`DEC-0087`** — composes **DEC-0086** (do not amend) |
| **Tranche order** | A scratchpad → B catalog examples → C resolver+validator → D runbook → E tests+parity |
| **Task seeds** | 11 seeds (under **`SPRINT_MAX_TASKS=12`** threshold) |
| **Catalog v2** | Optional **`roles`** section; v1 backward compatible |
| **Contract tests** | **`test_us0102_direct_override_keys`**, **`test_us0102_precedence_chain`**, **`test_us0102_catalog_schema_v2`**, **`test_us0102_role_catalog_resolver`**, **`test_us0102_tier_only_backward_compat`**, **`test_us0102_no_vendor_slugs_in_template`**, **`test_us0102_reason_codes`**, **`test_us0102_ask_phase_reinforcement`** |
| **Parity scope** | **`check_intake_template_parity.py --scope=model-tier-overrides`** (**`MODEL_TIER_OVERRIDES_PAIRS`**) |

### Top risks (carry to /sprint-plan)

- **R1**: Precedence confusion — locked 5-step chain + contract test.
- **R2**: Vendor slugs in template — grep gate + placeholder-only examples.
- **R3**: v1 catalog break on v2 validator — explicit v1 path unchanged.

### Evidence refs

- `decisions/DEC-0087.md`
- `docs/engineering/architecture.md` (**`# US-0102`**)
- `docs/product/backlog.md` (`## US-0102` — `architecture_notes` appended)
- `docs/engineering/state.md` (Architecture checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/sprint-plan`)
- `handoffs/intake_evidence/US-0102-intake-20260624.json`

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`US-0102`** — materialize sprint from 11 architecture seeds; AC-1..AC-10 bijection check.

### Decision gate

- **None** — architecture satisfied; sprint-plan readiness explicit.

---

