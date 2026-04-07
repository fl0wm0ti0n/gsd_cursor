# PO to TL archive pack (2026-04-05)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 45
- First archived heading: `## PO → TL discovery handoff — **US-0087** (`auto-20260405-01`)`
- Last archived heading: `## PO → TL discovery handoff — **US-0087** (`auto-20260405-01`)`
- Verification tuple (mandatory):
  - archived_body_lines=14
  - retained_body_lines=795

---

## PO → TL discovery handoff — **US-0087** (`auto-20260405-01`)

- **Scope recap**: Add **explicit** **`/auto`** bug targeting — **fix all OPEN bugs** (canonical backlog section, ascending id) or **single `BUG-####`** — with **spawn-only** orchestration unchanged; **default-off** new scratchpad keys; **one active scheduler** vs **`AUTO_BACKLOG_DRAIN`** (**US-0044**/**DEC-0022**); per-segment **`bug_id`** breadcrumbs in **`resume_brief`**/**`state.md`** aligned with **DEC-0069** (no stale **`RESUME_BRIEF_STALE`** on lawful runs). Intake evidence: `handoffs/intake_evidence/US-0087-intake-20260404.json`.
- **Acceptance pointers**: **AC-1** argv spellings; **AC-2** scratchpad/**`template/`**; **AC-3** precedence + conflict doc; **AC-4** queue + max items + empty queue code; **AC-5** resume/state fields; **AC-6** spawn-only; **AC-7** contract tests; **AC-8** **`architecture.md` `# US-0087`** matrix; **AC-9** runbook; **AC-10** parity.
- **Top risks**: double scheduling (story drain + bug queue); **`resume_brief`** freshness regressions; under-specified operator syntax; reason-code drift vs **`# US-0087`**.
- **Research asks** (extend **`R-0070`**):
  1. Enumerate **`auto.md`** + **`auto-orchestration-reference.md`** paragraphs that must change for bug-target precedence and **`AUTO_BACKLOG_DRAIN`** interaction.
  2. Map **`DEC-0069`**/**`BUG-0005`** requirements onto multi-bug queue + segment boundaries.
  3. Propose **architecture-locked** flag names + **fail-closed** reason codes (**AC-3**/**AC-4**/**AC-8**).
  4. Define **`AC-10`** breadcrumb tuple extensions for **`orchestrator_run_id`** segments when **`story_id=US-0087`** (before **`bug_id`** is set mid-queue).
- **Next phase**: **`/research`** (tech-lead default, **`US-0070`** plan).

---

