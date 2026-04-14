# PO to TL archive pack (2026-04-12)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 47
- First archived heading: `## PO → TL Handoff — US-0088 (Intake, 2026-04-12)`
- Last archived heading: `## PO → TL Handoff — US-0088 (Intake, 2026-04-12)`
- Verification tuple (mandatory):
  - archived_body_lines=24
  - retained_body_lines=784

---

## PO → TL Handoff — US-0088 (Intake, 2026-04-12)

### Scope

- **US-0088** (**OPEN**): **`/auto`** must run **all intersected phases** (per **`docs/engineering/auto-orchestration-reference.md`** **Step 5**, **US-0080 / DEC-0062** expanded contract) until the **active US** or **sprint segment** is **done**, not stop after **one phase** when policy says continue.
- **`AUTO_BACKLOG_DRAIN=1`**: continue across **OPEN** stories with a **quiet operator surface** — notify only on **`decision_gate`**, **`error`**, **`pause`**, **`loop_max`**, **`blocked`**, or **missing inputs**.
- **Deliverables for dev cycle**: update **`.cursor/commands/auto.md`**, **`docs/engineering/auto-orchestration-reference.md`**, **`docs/engineering/runbook.md`**, **`tests/auto_command_contract_test.py`** (or successor), **`architecture.md`** **`# US-0088`**, **active + `template/`** scratchpad/command parity (**AC-5**).

### Risks

- **Resume / stale brief**: continuous loops must compose with **`US-0037`** and **`DEC-0069`** without **`RESUME_BRIEF_STALE`** false positives mid-run.
- **Scheduler clash**: story drain vs **`US-0087`** bug queue — preserve **single active scheduler** rules already architecture-locked for **US-0087**.
- **Quiet vs safety**: silent continuation must **not** hide mandatory **decision_gate** or **verify-work/release** evidence requirements.

### Research

- **`R-0071`** (stub): intake-era gap analysis; extend during **`/discovery`** with line-level **Step 5** vs implementation drift inventory.

### Next phase (historical — intake → discovery)

- **`/discovery`** (**`po`**, not TL) for **US-0088** — **PASS 2026-04-12** (`orchestrator_run_id=auto-20260405-01`); see **tail** **Discovery Addendum — US-0088** for **`/research`** (**tech-lead**).

---

