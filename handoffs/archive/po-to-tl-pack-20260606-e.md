# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 21
- First archived heading: `## Orchestrated discovery handoff — BUG-0006 / auto-20260403-03`
- Last archived heading: `## Orchestrated discovery handoff — BUG-0007 / auto-20260404-01`
- Verification tuple (mandatory):
  - archived_body_lines=76
  - retained_body_lines=771

---

## Orchestrated discovery handoff — BUG-0006 / auto-20260403-03

### Target

- `bug_id=BUG-0006`
- `orchestrator_run_id=auto-20260403-03`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-BUG0006-discovery-20260404T002000Z-fresh`
- `next_scheduled_phase=research`

### Summary

- **Scope**: **`/auto`** orchestration integrity — orchestrator **must not** perform phase work directly; each phase requires **fresh subagent** spawn per **US-0048** / **US-0069** / **US-0080**; on violation, **fail fast** with deterministic reason-code coverage (intake: **`handoffs/intake_evidence/BUG-0006-intake-20260403.json`**).
- **Discovery conclusions**: Defect is bounded to **workflow/docs/enforcement** surfaces (command + reference + optional tests); preserve existing isolation and strict-runtime-proof contracts (**DEC-0029**, **DEC-0038**); add regression that proves spawn-or-fail behavior is not bypassed by “orchestrator executes phase” paths.
- **Canonical status** (**US-0045**): **`docs/product/backlog.md`** keeps **`BUG-0006`** **OPEN**; acceptance bug row unchanged.

### Evidence refs

- `docs/product/backlog.md` (**`### BUG-0006`** — `discovery_notes`)
- `handoffs/intake_evidence/BUG-0006-intake-20260403.json`
- `.cursor/commands/auto.md`
- `docs/engineering/state.md` (**Discovery checkpoint — BUG-0006 / auto-20260403-03**; triad archive **`docs/engineering/state-archive/state-pack-20260403-n.md`**)
- `handoffs/resume_brief.md`

### Open questions for `/research`

1. Concrete locations (commands, **`auto-orchestration-reference.md`**, runbook, tests) where “direct execution” could be read as allowed vs forbidden.
2. Minimal **R-####** recommendation: doc-only hardening vs scripted guardrails vs both; align reason codes with **`PHASE_CONTEXT_ISOLATION_*`** / spawn enforcement vocabulary.
3. **Regression matrix**: positive (spawn implied) and negative (orchestrator must not claim phase completion without subagent boundary) — test or contract-check shape.

### Next

- **`/research`** (**tech-lead**, default) for **`BUG-0006`**; then **`/architecture`** / **`/sprint-plan`** per TL.
- **Decision gate before research**: none (discovery satisfied; bug **OPEN**).

---

## Orchestrated discovery handoff — BUG-0007 / auto-20260404-01

### Target

- `bug_id=BUG-0007`
- `orchestrator_run_id=auto-20260404-01`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-BUG0007-discovery-20260404T120000Z-fresh`
- `next_scheduled_phase=research`

### Summary

- **Scope**: Intake evidence integrity — **`asked_topics`** and **`topic_coverage`** must truthfully record which required-pack topics were **actually asked** in user-visible form (or satisfied via explicit **DEC-0060** mechanisms: **`delegation_ref`** with scope/rationale/confidence, **`equivalent_evidence_ref`**, or **`assumption_confirmation_ref`**). The defect is **misleading evidence**: persistence/validation may treat free-form user bug text as if it were structured answers to required questions.
- **Exemplar**: **`handoffs/intake_evidence/BUG-0007-intake-20260403.json`** — `small-intake-pack` with `asked_topics` populated and five `topic_coverage` rows using the same complaint prose as `quoted_user_text` under `satisfied_by=answer_ref` without a distinct Q/A turn; contrasts with **`.cursor/commands/intake.md`** (US-0068 / US-0078) expectation that evidence matches real questioning.
- **Canonical status** (**US-0045**): **`docs/product/backlog.md`** keeps **`BUG-0007`** **OPEN** until **`/verify-work`** closure; acceptance bug row unchanged.

### Evidence refs

- `docs/product/backlog.md` (**`### BUG-0007`** — `discovery_notes`)
- `handoffs/intake_evidence/BUG-0007-intake-20260403.json`
- `.cursor/commands/intake.md` (**interactive intake evidence gate**)
- `scripts/intake_evidence_validate.py` (validator surface for fail-closed persistence)
- `docs/engineering/state.md` (**Discovery checkpoint — BUG-0007 / auto-20260404-01**)
- `handoffs/resume_brief.md`

### Open questions for `/research`

1. Where evidence is authored relative to **actual chat turns** (PO subagent, scripts, templates) and what minimal **audit binding** (e.g. turn refs, question text hash, explicit “not asked” state) is feasible.
2. Validator and/or command changes so **`asked_topics`** cannot list topics that were never prompted, and **`topic_coverage`** cannot use **`answer_ref`** without a verifiable user answer artifact — without breaking legitimate **`delegation_ref`** / **`equivalent_evidence_ref`** flows (**US-0083**).
3. Interaction with **`/intake bug`** path: **`intake_bug_resume_brief_refresh.py`**, **`bug_issue_validate.py`**, and whether a new deterministic subcode under **`INTAKE_PERSISTENCE_BLOCKED`** is warranted.
4. **Regression matrix**: fixture JSON + validator test that fails on BUG-0007-shaped bundles.

### Next

- **`/research`** (**tech-lead**, default) for **`BUG-0007`**; then **`/architecture`** / **`/sprint-plan`** per TL.
- **Decision gate before research**: none (discovery satisfied; bug **OPEN**).

---

