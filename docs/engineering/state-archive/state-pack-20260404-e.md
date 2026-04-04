# State archive pack (2026-04-04)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 26
- First archived heading: `## Discovery checkpoint (2026-04-04) — BUG-0006 / auto-20260403-03`
- Last archived heading: `## Discovery checkpoint (2026-04-04) — BUG-0006 / auto-20260403-03`
- Verification tuple (mandatory):
  - archived_body_lines=45
  - preamble_lines=11
  - retained_body_lines=1166

---

## Discovery checkpoint (2026-04-04) — BUG-0006 / auto-20260403-03

- **`/discovery`** complete in fresh **PO** context (`orchestrator_run_id=auto-20260403-03`).
- **Summary**: Bounded **orchestration integrity** defect — **`/auto`** must **not** execute phase work in orchestrator context; each lifecycle phase requires a **fresh role subagent** spawn per **US-0048** / **US-0069** / **US-0080** (`.cursor/commands/auto.md`). Done criteria from intake: deterministic **fail-fast** when direct orchestrator phase execution is attempted, with explicit **reason-code** coverage for missing subagent spawn; preserve isolation + strict-runtime-proof contracts (**DEC-0029**, **DEC-0038**); add **regression** proving rejection of in-orchestrator phase execution. Intake evidence: **`handoffs/intake_evidence/BUG-0006-intake-20260403.json`** (`small-intake-pack`, required topics satisfied).
- **Research asks for TL**: (1) Where `/auto` (and related docs) can imply or allow direct phase execution vs spawn-only; (2) minimal enforcement surface (command text, reference doc cross-links, optional validator/tests) for spawn-or-fail semantics; (3) deterministic reason-code vocabulary aligned with existing **`PHASE_CONTEXT_ISOLATION_*`** / **`RUNTIME_PROOF_*`** families; (4) regression shape (scripted or doc-contract test) that fails if orchestrator “runs” a phase without subagent boundary.
- **Canonical status (US-0045)**: **`docs/product/backlog.md`** keeps **`BUG-0006`** **OPEN**; no acceptance mutation.
- **Next recommended phase**: **`/research`** (**tech-lead** default; `next_scheduled_phase=research`).

Isolation evidence (**US-0048** / **DEC-0029**):

- `phase_id=discovery`
- `role=po`
- `fresh_context_marker=po-BUG0006-discovery-20260404T002000Z-fresh`
- `timestamp=2026-04-04T00:20:00Z`
- `evidence_ref=handoffs/intake_evidence/BUG-0006-intake-20260403.json,.cursor/commands/auto.md,docs/engineering/auto-orchestration-reference.md,docs/product/backlog.md,handoffs/po_to_tl.md,handoffs/resume_brief.md,docs/engineering/state.md`

Strict runtime proof (**US-0056** / **DEC-0038**): canonical tuple hashed as **SHA-256** of **sorted-key JSON** over (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`). **`proof_ttl_seconds`** is serialized as a JSON **integer** (not a string) in the hashed payload.

- `orchestrator_run_id=auto-20260403-03`
- `runtime_proof_id=rp-auto-20260403-03-discovery-po-20260404T002000Z-BUG0006`
- `phase_id=discovery`
- `role=po`
- `proof_issued_at=2026-04-04T00:20:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=348e89ad0bdf932474b46a68c6eb58abc97b55237ec0a97b14855ee6d21a16a4`

## Phase boundary status (post-discovery, BUG-0006 / auto-20260403-03)

- `resolved_phase_plan_snapshot`=(orchestrator materialization for **`auto-20260403-03`** — discovery segment; not rewritten at discovery writer)
- `skipped_phases_summary`=(prior segment: `intake` omitted per resume anchor — unchanged at discovery writer)
- `phase_boundary=discovery`
- `next_scheduled_phase=research`
- `bug_id=BUG-0006`
- `story_id=(none)`
- `sprint_id=(none)`
- `orchestrator_run_id=auto-20260403-03`

**Phase boundary operator visibility (AC-10)** — compact status: `phase_boundary=discovery`; `next_scheduled_phase=research`; `bug_id=BUG-0006`; `sprint_id=(none)`; `orchestrator_run_id=auto-20260403-03`.

**Triad hot-surface (DEC-0054)** (post-discovery BUG-0006 hygiene):

- Post-append: `python scripts/enforce-triad-hot-surface.py --check` -> **FAIL** (`STATE_ARCHIVE_REQUIRED` / `ARTIFACT_HOT_SURFACE_OVERSIZE` on **`docs/engineering/state.md`**).
- `python scripts/enforce-triad-hot-surface.py --rollover` -> **`rollover_complete units=1`** — **`docs/engineering/state-archive/state-pack-20260403-n.md`**.
- Final `python scripts/enforce-triad-hot-surface.py --check` -> **PASS** (exit **0**).

