# State archive pack (2026-04-06)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 29
- First archived heading: `## Discovery checkpoint (2026-04-04) — US-0084 / auto-20260404-02`
- Last archived heading: `## Discovery checkpoint (2026-04-04) — US-0084 / auto-20260404-02`
- Verification tuple (mandatory):
  - archived_body_lines=36
  - preamble_lines=11
  - retained_body_lines=1188

---

## Discovery checkpoint (2026-04-04) — US-0084 / auto-20260404-02

- **`/discovery`** completed for **`US-0084`** in fresh **PO** context (`orchestrator_run_id=auto-20260404-02`).
- **Verdict**: **complete** — problem reframed around **published npm** **`installer.sh`** POSIX/dash + **LF** vs repo drift, **CRLF**/bash-only **`set`** class; surfaces scoped to installer/publish pipeline, runbook + **US-0064** alignment (**`release-targets.json`**, **`runtime-connectivity.md`**), optional **`scripts/`** helper, harness/parity; **research asks** captured in **`docs/product/backlog.md`** and **`handoffs/po_to_tl.md`**. **Next recommended phase**: **`/research`** (tech-lead default).

Isolation evidence (**US-0048** / **DEC-0029**):

- `phase_id=discovery`
- `role=po`
- `fresh_context_marker=po-US0084-discovery-20260404T150000Z-fresh`
- `timestamp=2026-04-04T15:00:00Z`
- `evidence_ref=handoffs/intake_evidence/US-0084-intake-20260404.json,docs/product/backlog.md,docs/product/acceptance.md,handoffs/po_to_tl.md,docs/engineering/release-targets.json,docs/engineering/runtime-connectivity.md,docs/engineering/architecture.md,handoffs/resume_brief.md,docs/engineering/state.md`

Strict runtime proof (**US-0056** / **DEC-0038**): canonical tuple hashed as **SHA-256** of **sorted-key JSON** over (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`). **`proof_ttl_seconds`** is serialized as a JSON **integer** (not a string) in the hashed payload.

- `orchestrator_run_id=auto-20260404-02`
- `runtime_proof_id=rp-auto-20260404-02-discovery-po-20260404T150000Z-US0084`
- `phase_id=discovery`
- `role=po`
- `proof_issued_at=2026-04-04T15:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=d565385fc8b94780eba3fb5b4bd76804c24e4a4b7c711ba5d1bf79256bbb07ec`

## Phase boundary status (post-discovery, US-0084 / auto-20260404-02)

- `resolved_phase_plan_snapshot`=(orchestrator materialization for **`auto-20260404-02`** — discovery segment; not rewritten at discovery writer)
- `skipped_phases_summary`=(intake omitted per resume anchor — unchanged at discovery writer)
- `phase_boundary=discovery`
- `next_scheduled_phase=research`
- `bug_id=(none)`
- `story_id=US-0084`
- `sprint_id=(none)`
- `orchestrator_run_id=auto-20260404-02`

**Phase boundary operator visibility (AC-10)** — compact status: `phase_boundary=discovery`; `next_scheduled_phase=research`; `bug_id=(none)`; `story_id=US-0084`; `sprint_id=(none)`; `orchestrator_run_id=auto-20260404-02`.

