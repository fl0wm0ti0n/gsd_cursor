# State archive pack (2026-04-07)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 24
- First archived heading: `## Architecture checkpoint (2026-04-04) — BUG-0008 / auto-20260404-03`
- Last archived heading: `## Architecture checkpoint (2026-04-04) — BUG-0008 / auto-20260404-03`
- Verification tuple (mandatory):
  - archived_body_lines=45
  - preamble_lines=11
  - retained_body_lines=1186

---

## Architecture checkpoint (2026-04-04) — BUG-0008 / auto-20260404-03

- **`/architecture`** completed for **`BUG-0008`** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260404-03`).
- **Summary**: **`docs/engineering/architecture.md`** **`# BUG-0008`** — CRLF manifest → empty **`install_include_paths`** (**R-0069**); in-repo mitigations (**`installer.sh`** **`get_manifest_paths`**, **`.gitattributes`**, **`guard_installer_publish.py`** + **`template/`**, **`installer.ps1`**, **`tests/installer_manifest_crlf_bug0008_test.py`**, **`run-tests`** **26P2**); **remaining operator delivery** = version bump + **`npm publish`** + Debian global E2E; **`R-0069`** delivery-closed when backlog marks **BUG-0008** **DONE** after QA/release.
- **Artifacts**: **`docs/engineering/architecture.md`**, **`docs/product/backlog.md`** (**`architecture_notes`** under **`### BUG-0008`**), **`handoffs/tl_to_dev.md`** (compact pointer), **`docs/engineering/research.md`** (**R-0069** remains **open** until delivery), **`docs/engineering/state.md`**
- **Canonical bug status (US-0045)**: **`BUG-0008`** remains **OPEN** in **`docs/product/backlog.md`** only.
- **Next recommended phase**: **`/sprint-plan`** for **`BUG-0008`** (`next_scheduled_phase=sprint-plan`).

Isolation evidence (**US-0048** / **DEC-0029**):

- `phase_id=architecture`
- `role=tech-lead`
- `fresh_context_marker=tl-BUG0008-architecture-20260404T230000Z-fresh`
- `timestamp=2026-04-04T23:00:00Z`
- `evidence_ref=docs/engineering/architecture.md,docs/product/backlog.md,docs/engineering/research.md,installer.sh,installer.ps1,.gitattributes,scripts/guard_installer_publish.py,template/scripts/guard_installer_publish.py,tests/installer_manifest_crlf_bug0008_test.py,tests/run-tests.sh,tests/run-tests.ps1,handoffs/tl_to_dev.md,docs/engineering/state.md`

Strict runtime proof (**US-0056** / **DEC-0038**): canonical tuple hashed as **SHA-256** of **sorted-key JSON** over (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`). **`proof_ttl_seconds`** is serialized as a JSON **integer** (not a string) in the hashed payload.

- `orchestrator_run_id=auto-20260404-03`
- `runtime_proof_id=rp-auto-20260404-03-architecture-tech-lead-20260404T230000Z-BUG0008`
- `phase_id=architecture`
- `role=tech-lead`
- `proof_issued_at=2026-04-04T23:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=9a555d86738cd0c067785a90c3096b37257390c472ffff40174d94aa69e6cd13`

## Phase boundary status (post-architecture, BUG-0008 / auto-20260404-03)

- `resolved_phase_plan_snapshot`=(orchestrator materialization for **`auto-20260404-03`** — architecture writer does not rewrite full plan)
- `skipped_phases_summary`=(not rewritten at architecture writer)
- `phase_boundary=architecture`
- `next_scheduled_phase=sprint-plan`
- `bug_id=BUG-0008`
- `story_id=(none)`
- `sprint_id=(none)`
- `orchestrator_run_id=auto-20260404-03`

**Phase boundary operator visibility (AC-10)** — compact status: `phase_boundary=architecture`; `next_scheduled_phase=sprint-plan`; `bug_id=BUG-0008`; `sprint_id=(none)`; `orchestrator_run_id=auto-20260404-03`.

**Triad hot-surface (DEC-0054)** (post-architecture BUG-0008 hygiene):

- Post-append: `python scripts/enforce-triad-hot-surface.py --check` → **FAIL** (`ARTIFACT_HOT_SURFACE_OVERSIZE` on **`docs/engineering/state.md`**).
- `python scripts/enforce-triad-hot-surface.py --rollover` → **`rollover_complete units=1`** — **`docs/engineering/state-archive/state-pack-20260404-i.md`** (first/last archived heading: **`## Plan-verify checkpoint (2026-04-04) — S0067 / BUG-0006 / auto-20260403-03`**).
- Final `python scripts/enforce-triad-hot-surface.py --check` → **PASS** (exit **0**).

