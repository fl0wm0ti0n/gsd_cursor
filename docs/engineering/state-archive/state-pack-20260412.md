# State archive pack (2026-04-12)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 22
- First archived heading: `## Execute checkpoint (2026-04-05) — S0070 / BUG-0008 / auto-20260404-03`
- Last archived heading: `## Execute checkpoint (2026-04-05) — S0070 / BUG-0008 / auto-20260404-03`
- Verification tuple (mandatory):
  - archived_body_lines=41
  - preamble_lines=11
  - retained_body_lines=1190

---

## Execute checkpoint (2026-04-05) — S0070 / BUG-0008 / auto-20260404-03

- **`/execute`** completed for **`S0070`** / **`BUG-0008`** in fresh **dev** context (`orchestrator_run_id=auto-20260404-03`).
- **Summary**: Semver **`0.1.2-41`** (**`package.json`**, **`its_magic/.its-magic-version`**); **`npm pack`** inspection — template **`installer-owned-paths.manifest`** **no** `\r`; **`npm run prepublishOnly`** + **`python scripts/guard_installer_publish.py`** **PASS**; **README** + **`template/README`** operator note (**BUG-0008**); **`tests/installer_manifest_crlf_bug0008_test.py`** **PASS** with **`awk`** on PATH; **§26P2** wired in **`run-tests.sh`** / **`.ps1`**. Draft **`handoffs/releases/S0070-release-notes.md`**; **`handoffs/release_queue.md`** **`S0070`** → **`planned`**. **Not done here**: **`npm publish`**; Debian/docker-dmz **global E2E** (AC-5). **`BUG-0008`** remains **OPEN** (**US-0045**); **`R-0069`** **not** closed.
- **Next recommended phase**: **`/qa`** for **`S0070`** / **`BUG-0008`** (`next_scheduled_phase=qa`).

Isolation evidence (**US-0048** / **DEC-0029**):

- `phase_id=execute`
- `role=dev`
- `fresh_context_marker=dev-S0070-BUG0008-execute-20260405T001200Z-fresh`
- `timestamp=2026-04-05T00:12:00Z`
- `evidence_ref=sprints/S0070/tasks.md,sprints/S0070/summary.md,sprints/S0070/uat.json,sprints/S0070/uat.md,sprints/S0070/release-findings.md,package.json,its_magic/.its-magic-version,README.md,template/README.md,handoffs/releases/S0070-release-notes.md,handoffs/release_queue.md,handoffs/dev_to_qa.md,docs/product/backlog.md,docs/engineering/state.md`

Strict runtime proof (**US-0056** / **DEC-0038**): canonical tuple hashed as **SHA-256** of **sorted-key JSON** over (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`). **`proof_ttl_seconds`** is serialized as a JSON **integer** (not a string) in the hashed payload.

- `orchestrator_run_id=auto-20260404-03`
- `runtime_proof_id=rp-auto-20260404-03-execute-dev-20260405T001200Z-S0070-BUG0008`
- `phase_id=execute`
- `role=dev`
- `proof_issued_at=2026-04-05T00:12:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=09660f33f6cdc77fee7a00f80b4e1b69d239bac31a3837b178892a8b698f3447`

## Phase boundary status (post-execute, S0070 / BUG-0008 / auto-20260404-03)

- `phase_boundary=execute`
- `next_scheduled_phase=qa`
- `bug_id=BUG-0008`
- `story_id=(none)`
- `sprint_id=S0070`
- `orchestrator_run_id=auto-20260404-03`

**Phase boundary operator visibility (AC-10)** — compact status: `phase_boundary=execute`; `next_scheduled_phase=qa`; `bug_id=BUG-0008`; `sprint_id=S0070`; `orchestrator_run_id=auto-20260404-03`.

**Triad hot-surface (DEC-0054)** (post-execute S0070 hygiene):

- Post-append: `python scripts/enforce-triad-hot-surface.py --check` -> **FAIL** (`STATE_ARCHIVE_REQUIRED` / `ARTIFACT_HOT_SURFACE_OVERSIZE` on **`docs/engineering/state.md`**).
- `python scripts/enforce-triad-hot-surface.py --rollover` -> **`rollover_complete units=1`** — **`docs/engineering/state-archive/state-pack-20260404-k.md`**.
- Final `python scripts/enforce-triad-hot-surface.py --check` -> **PASS** (exit **0**).

