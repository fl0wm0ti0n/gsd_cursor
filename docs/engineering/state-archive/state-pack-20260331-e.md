# State archive pack (2026-03-31)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 35
- First archived heading: `## Research checkpoint (2026-03-30) — BUG-0001 / auto-20260330-01`
- Last archived heading: `## Architecture checkpoint (2026-03-30) — BUG-0001 / auto-20260330-01`
- Verification tuple (mandatory):
  - archived_body_lines=87
  - preamble_lines=11
  - retained_body_lines=1163

---

## Research checkpoint (2026-03-30) — BUG-0001 / auto-20260330-01

- **`/research`** (**tech-lead**, fresh context): **`BUG-0001`** confirmed **OPEN** — install completeness gap unchanged pending implementation; research narrows fix surface per **`R-0058`** extension.
- **Minimal intake script set**: `intake_evidence_validate.py` → `intake_evidence_lib.py` (stdlib-only); `intake_bug_routing_guard.py` (stdlib-only) — **three** files to mirror into **`template/scripts/`**.
- **Install / parity**: **`installer.ps1`** / **`installer.sh`** use **`template/`** as **`SOURCE_ROOT`** for consumer hydration; npm **`package.json`** **`files`** ships **`template/`** wholesale + **`scripts/doc_profile_lib.py`**; Chocolatey/Homebrew use tag archives + same installers — **triple-installer parity** = consistent **`template/`** tree (especially **`template/scripts/intake_*.py`**).
- **Handoff to architecture**: Decide **`files`** enumeration vs template-only ship, add deterministic **`scripts/`↔`template/scripts/`** parity checks for intake modules, **US-0018** new-file delivery + regression tests.
- **Next recommended phase**: **`/architecture`** for **`BUG-0001`**.

Isolation evidence (**US-0048** / **DEC-0029**):

- `phase_id=research`
- `role=tech-lead`
- `fresh_context_marker=tl-BUG0001-research-20260330T220500Z-fresh`
- `timestamp=2026-03-30T22:05:00Z`
- `evidence_ref=docs/product/backlog.md,docs/product/acceptance.md,docs/product/vision.md,handoffs/po_to_tl.md,handoffs/resume_brief.md,package.json,installer.ps1,installer.sh,scripts/intake_bug_routing_guard.py,scripts/intake_evidence_lib.py,scripts/intake_evidence_validate.py,handoffs/intake_evidence/BUG-0001-intake-20260330.json,docs/engineering/research.md`

Strict runtime proof (**US-0056** / **DEC-0038**): canonical tuple hashed as **SHA-256** of **sorted-key JSON** over (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`).

- `orchestrator_run_id=auto-20260330-01`
- `runtime_proof_id=rp-auto-20260330-01-research-tl-20260330T220500Z-BUG0001`
- `phase_id=research`
- `role=tech-lead`
- `proof_issued_at=2026-03-30T22:05:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=10e6ab62a3cf908aa01d1d7e6d193a46034b986569f837f2ec54ec62d9f324c5`

## Phase boundary status (post-research BUG-0001, auto-20260330-01)

- `resolved_phase_plan_snapshot=intersected_executable_plan` per **`## Auto continuation checkpoint (2026-03-30) — invocation auto-20260330-01 / BUG-0001`**
- `skipped_phases=intake (reason: resume anchor before phase)`
- `phase_boundary=research`
- `next_scheduled_phase=architecture`
- `bug_id=BUG-0001`
- `story_id=(none)`
- `sprint_id=(none)`
- `orchestrator_run_id=auto-20260330-01`

**Phase boundary operator visibility (AC-10)** — compact status: `phase_boundary=research`; `next_scheduled_phase=architecture`; `bug_id=BUG-0001`; `orchestrator_run_id=auto-20260330-01`.

**Triad hot-surface (DEC-0054)** (post-research BUG-0001 hygiene):

- Post-append: `python scripts/enforce-triad-hot-surface.py --check` → **FAIL** (`ARTIFACT_HOT_SURFACE_OVERSIZE`: **`docs/engineering/state.md`** over line budget).
- `python scripts/enforce-triad-hot-surface.py --rollover` → **`rollover_complete units=1`** — **`docs/engineering/state-archive/state-pack-20260330-c.md`** (first archived heading **`## Refresh-context checkpoint (2026-03-29) — post S0057 / US-0078 (auto-20260328-01)`**).
- Final `python scripts/enforce-triad-hot-surface.py --check` → **PASS** (exit **0**).
- Verification tuple: **`boundary=triad-rollover|state`**, **`moved=1`**, **`retained=27`**, **`pack_ref=docs/engineering/state-archive/state-pack-20260330-c.md`**

## Architecture checkpoint (2026-03-30) — BUG-0001 / auto-20260330-01

- **`/architecture`** (**tech-lead**, fresh context): **`BUG-0001`** remains **OPEN** — normative fix locked per **`DEC-0063`**: minimal **`template/scripts/`** mirror of three **`intake_*`** modules (parity with **`scripts/`**), **`package.json` `files`** policy (**`template/`** primary; optional explicit **`scripts/intake_*.py`** entries), deterministic parity/regression tests, **`US-0018`** upgrade delivery for new/changed intake files.
- **Artifacts**: **`decisions/DEC-0063.md`**; **`docs/engineering/architecture.md`** **`# BUG-0001`**; **`docs/engineering/decisions.md`** (context pack + **`DEC-0063`** index); **`docs/product/backlog.md`** / **`docs/product/vision.md`** architecture traceability; **`handoffs/resume_brief.md`** → **`/sprint-plan`**; **`handoffs/po_to_tl.md`** (**Architecture Addendum — BUG-0001**); **`handoffs/tl_to_dev.md`** (pre-sprint pointer).
- **Next recommended phase**: **`/sprint-plan`** for **`BUG-0001`** (`next_scheduled_phase=sprint-plan`).

Isolation evidence (**US-0048** / **DEC-0029**):

- `phase_id=architecture`
- `role=tech-lead`
- `fresh_context_marker=tl-BUG0001-architecture-20260330T230000Z-fresh`
- `timestamp=2026-03-30T23:00:00Z`
- `evidence_ref=docs/product/backlog.md,docs/product/acceptance.md,docs/product/vision.md,handoffs/po_to_tl.md,handoffs/resume_brief.md,decisions/DEC-0063.md,docs/engineering/architecture.md,docs/engineering/decisions.md,docs/engineering/research.md,package.json,template/scripts/,scripts/intake_bug_routing_guard.py,scripts/intake_evidence_lib.py,scripts/intake_evidence_validate.py,handoffs/intake_evidence/BUG-0001-intake-20260330.json`

Strict runtime proof (**US-0056** / **DEC-0038**): canonical tuple hashed as **SHA-256** of **sorted-key JSON** over (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`).

- `orchestrator_run_id=auto-20260330-01`
- `runtime_proof_id=rp-auto-20260330-01-architecture-tl-20260330T230000Z-BUG0001`
- `phase_id=architecture`
- `role=tech-lead`
- `proof_issued_at=2026-03-30T23:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=711e8e6bb804f4afae8cb96ed528224832ec4880f969cae283a515da39e5e959`

## Phase boundary status (post-architecture BUG-0001, auto-20260330-01)

- `resolved_phase_plan_snapshot=intersected_executable_plan` per **`## Auto continuation checkpoint (2026-03-30) — invocation auto-20260330-01 / BUG-0001`**
- `skipped_phases=intake (reason: resume anchor before phase)`
- `phase_boundary=architecture`
- `next_scheduled_phase=sprint-plan`
- `bug_id=BUG-0001`
- `story_id=(none)`
- `sprint_id=(none)`
- `orchestrator_run_id=auto-20260330-01`

**Phase boundary operator visibility (AC-10)** — compact status: `phase_boundary=architecture`; `next_scheduled_phase=sprint-plan`; `bug_id=BUG-0001`; `orchestrator_run_id=auto-20260330-01`.

**Triad hot-surface (DEC-0054)** (post-architecture BUG-0001 hygiene):

- Post-append: `python scripts/enforce-triad-hot-surface.py --check` → **PASS** (exit **0**); **`docs/engineering/state.md`** within line budget — no rollover at this boundary.

