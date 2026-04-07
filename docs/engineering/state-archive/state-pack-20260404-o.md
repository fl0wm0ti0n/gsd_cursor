# State archive pack (2026-04-04)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 29
- First archived heading: `## Discovery checkpoint (2026-04-04) — BUG-0007 / auto-20260404-01`
- Last archived heading: `## Discovery checkpoint (2026-04-04) — BUG-0007 / auto-20260404-01`
- Verification tuple (mandatory):
  - archived_body_lines=45
  - preamble_lines=11
  - retained_body_lines=1177

---

## Discovery checkpoint (2026-04-04) — BUG-0007 / auto-20260404-01

- **`/discovery`** complete in fresh **PO** context (`orchestrator_run_id=auto-20260404-01`).
- **Summary**: Intake evidence integrity — **`asked_topics`** and **`topic_coverage`** must truthfully reflect **user-facing questions** actually posed (or valid **DEC-0060** paths: **`delegation_ref`**, **`equivalent_evidence_ref`**, **`assumption_confirmation_ref`**). **`handoffs/intake_evidence/BUG-0007-intake-20260403.json`** illustrates the failure mode: `small-intake-pack` rows record `satisfied_by=answer_ref` with the user's single bug-report utterance echoed as `quoted_user_text` across all required keys without a real Q round. Contract anchors: **`.cursor/commands/intake.md`** (US-0068 / US-0078); **`scripts/intake_evidence_validate.py`** must not certify “asked + answered” without an auditable question–answer trail or an allowed alternate satisfaction mode.
- **Research asks for TL**: (1) Authoring vs validation boundaries relative to chat turns; (2) minimal deterministic guard (validator + optional tests) for truthful **`asked_topics`** / **`topic_coverage`**; (3) **`/intake bug`** + resume-brief refresh interactions; (4) reason-code strategy (reuse vs extend **`INTAKE_PERSISTENCE_BLOCKED`** family).
- **Canonical status (US-0045)**: **`BUG-0007`** stays **OPEN** until **`/verify-work`** closure.
- **Next recommended phase**: **`/research`** (**tech-lead** default; `next_scheduled_phase=research`).

Isolation evidence (**US-0048** / **DEC-0029**):

- `phase_id=discovery`
- `role=po`
- `fresh_context_marker=po-BUG0007-discovery-20260404T120000Z-fresh`
- `timestamp=2026-04-04T12:00:00Z`
- `evidence_ref=handoffs/intake_evidence/BUG-0007-intake-20260403.json,.cursor/commands/intake.md,scripts/intake_evidence_validate.py,docs/product/backlog.md,handoffs/po_to_tl.md,handoffs/resume_brief.md,docs/engineering/state.md`

Strict runtime proof (**US-0056** / **DEC-0038**): canonical tuple hashed as **SHA-256** of **sorted-key JSON** over (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`). **`proof_ttl_seconds`** is serialized as a JSON **integer** (not a string) in the hashed payload.

- `orchestrator_run_id=auto-20260404-01`
- `runtime_proof_id=rp-auto-20260404-01-discovery-po-20260404T120000Z-BUG0007`
- `phase_id=discovery`
- `role=po`
- `proof_issued_at=2026-04-04T12:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=2e1674d84635951ec37bd91d963a7674970095665a3e214118954eae8b5f1f8f`

## Phase boundary status (post-discovery, BUG-0007 / auto-20260404-01)

- `resolved_phase_plan_snapshot`=(orchestrator materialization for **`auto-20260404-01`** — discovery segment; not rewritten at discovery writer)
- `skipped_phases_summary`=(**`intake`** omitted per resume anchor — unchanged at discovery writer)
- `phase_boundary=discovery`
- `next_scheduled_phase=research`
- `bug_id=BUG-0007`
- `story_id=(none)`
- `sprint_id=(none)`
- `orchestrator_run_id=auto-20260404-01`

**Phase boundary operator visibility (AC-10)** — compact status: `phase_boundary=discovery`; `next_scheduled_phase=research`; `bug_id=BUG-0007`; `sprint_id=(none)`; `orchestrator_run_id=auto-20260404-01`.

**Triad hot-surface (DEC-0054)** (post-discovery BUG-0007 hygiene):

- Post-append: `python scripts/enforce-triad-hot-surface.py --check` -> **FAIL** (`STATE_ARCHIVE_REQUIRED` / `ARTIFACT_HOT_SURFACE_OVERSIZE` on **`docs/engineering/state.md`**).
- `python scripts/enforce-triad-hot-surface.py --rollover` -> **`rollover_complete units=2`** — **`docs/engineering/state-archive/state-pack-20260403-y.md`** (archived oldest contiguous checkpoints per pack header: first **`## Plan-verify checkpoint (2026-04-03) — S0065 / BUG-0004 / auto-20260403-01`** through last **`## Execute checkpoint (2026-04-03) — S0065 / BUG-0004 / auto-20260403-01`**).
- Final `python scripts/enforce-triad-hot-surface.py --check` -> **PASS** (exit **0**).

