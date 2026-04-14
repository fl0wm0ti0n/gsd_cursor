# State archive pack (2026-04-12)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 21
- First archived heading: `## QA checkpoint (2026-04-04) — S0070 / BUG-0008 / auto-20260404-03`
- Last archived heading: `## QA checkpoint (2026-04-04) — S0070 / BUG-0008 / auto-20260404-03 (re-validation)`
- Verification tuple (mandatory):
  - archived_body_lines=68
  - preamble_lines=11
  - retained_body_lines=1172

---

## QA checkpoint (2026-04-04) — S0070 / BUG-0008 / auto-20260404-03

- **`/qa`** completed for **`S0070`** / **`BUG-0008`** in fresh **qa** context (`orchestrator_run_id=auto-20260404-03`).
- **Verdict**: **`sprints/S0070/qa-findings.md`** **PASS_WITH_DEFERRALS** — in-repo **BUG-0008** automation **PASS** (guards, **`npm pack`** manifest CR scan, **26P2** module, **`bug_issue_validate --check-acceptance`**). **`tests/run-tests.ps1`** full harness still **non-green** on **§26P** (**`installer_shell_bug0004_test`**, **BUG-0004** / **US-0084** Windows **`sh`** — **pre-existing**, not **BUG-0008** regression); **§26P2** **PASS** when run. **Operator deferrals unchanged**: **`npm publish`** (**AC-6**); Debian global **E2E** (**AC-5**). **`BUG-0008`** remains **OPEN** (**US-0045**); **`acceptance.md`** **BUG-0008** row stays unchecked until publish + E2E + lifecycle closure.
- **Next recommended phase**: **`/verify-work`** for **`S0070`** / **`BUG-0008`** (`next_scheduled_phase=verify-work`).

Isolation evidence (**US-0048** / **DEC-0029**):

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0070-BUG0008-qa-20260404T191500Z-fresh`
- `timestamp=2026-04-04T19:15:00Z`
- `evidence_ref=sprints/S0070/qa-findings.md,sprints/S0070/sprint.md,sprints/S0070/tasks.md,sprints/S0070/uat.json,sprints/S0070/uat.md,handoffs/dev_to_qa.md,handoffs/qa_to_verify_work.md,package.json,its_magic/.its-magic-version,README.md,template/README.md,handoffs/releases/S0070-release-notes.md,handoffs/release_queue.md,docs/product/backlog.md,docs/product/acceptance.md,docs/engineering/state.md`

Strict runtime proof (**US-0056** / **DEC-0038**): canonical tuple hashed as **SHA-256** of **sorted-key JSON** over (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`). **`proof_ttl_seconds`** is serialized as a JSON **integer** (not a string) in the hashed payload.

- `orchestrator_run_id=auto-20260404-03`
- `runtime_proof_id=rp-auto-20260404-03-qa-qa-20260404T191500Z-S0070-BUG0008`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-04-04T19:15:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=9f457afa3fe51e874ae6b518f3148fff1eaf917b98632cea17381726f9d7ae17`

## QA checkpoint (2026-04-04) — S0070 / BUG-0008 / auto-20260404-03 (re-validation)

- **`/qa`** **re-validation** after dev execute (**`0.1.2-41`**) in fresh **qa** context (`orchestrator_run_id=auto-20260404-03`).
- **Verdict**: **`sprints/S0070/qa-findings.md`** **PASS_WITH_DEFERRALS** — same in-repo **BUG-0008** bar as prior QA; **triad** (**DEC-0054**): **`state.md`** was **`ARTIFACT_HOT_SURFACE_OVERSIZE`** before this checkpoint → **`python scripts/enforce-triad-hot-surface.py --rollover`** → **`docs/engineering/state-archive/state-pack-20260404-l.md`**, then **`--check`** **PASS** prior to recording this block. **`tests/run-tests.ps1`**: **§26P** **`installer_shell_bug0004_test.test_direct_sh_missing_mode_succeeds`** still **FAIL** (**pre-existing** **BUG-0004** / **US-0084** on Windows **`sh`**); **§26P2** **`installer_manifest_crlf_bug0008_test.py`** **PASS**. Harness also printed **`[TOKEN_COST_PARITY_ERROR]`** (**`auto-orchestration-reference.md`** active vs **`template/`** byte size) — **not** a **BUG-0008** regression (files outside **S0070** execute surface). **Deferrals**: **`npm publish`**; Debian **E2E** (**AC-5**). **`BUG-0008`** **OPEN**; do **not** mark **`acceptance.md`** **DONE** until published install + **E2E** + **verify-work**/**release** (**US-0045**).
- **Next recommended phase**: **`/verify-work`** (`next_scheduled_phase=verify-work`).

Isolation evidence (**US-0048** / **DEC-0029**):

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0070-BUG0008-qa-20260404T193000Z-fresh`
- `timestamp=2026-04-04T19:30:00Z`
- `evidence_ref=sprints/S0070/qa-findings.md,sprints/S0070/uat.json,sprints/S0070/uat.md,handoffs/dev_to_qa.md,handoffs/qa_to_verify_work.md,docs/engineering/state-archive/state-pack-20260404-l.md,docs/engineering/state-archive/state-pack-20260404-m.md,tests/report.md,its-magic-0.1.2-41.tgz,docs/product/backlog.md,docs/product/acceptance.md,docs/engineering/state.md`

Strict runtime proof (**US-0056** / **DEC-0038**): canonical tuple hashed as **SHA-256** of **sorted-key JSON** over (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`). **`proof_ttl_seconds`** is serialized as a JSON **integer** (not a string) in the hashed payload.

- `orchestrator_run_id=auto-20260404-03`
- `runtime_proof_id=rp-auto-20260404-03-qa-qa-20260404T193000Z-S0070-BUG0008`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-04-04T19:30:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=9d1cc09c1ca519ddb71160fabceb9a2860e7381609721a32174daa742752d425`

## Phase boundary status (post-qa, S0070 / BUG-0008 / auto-20260404-03)

- `phase_boundary=qa`
- `next_scheduled_phase=verify-work`
- `bug_id=BUG-0008`
- `story_id=(none)`
- `sprint_id=S0070`
- `orchestrator_run_id=auto-20260404-03`

**Phase boundary operator visibility (AC-10)** — compact status: `phase_boundary=qa`; `next_scheduled_phase=verify-work`; `bug_id=BUG-0008`; `sprint_id=S0070`; `orchestrator_run_id=auto-20260404-03`.

**Triad hot-surface (DEC-0054)** (post-QA S0070 re-validation hygiene):

- Pre-checkpoint: `python scripts/enforce-triad-hot-surface.py --check` -> **FAIL** (`STATE_ARCHIVE_REQUIRED` / **`ARTIFACT_HOT_SURFACE_OVERSIZE`** on **`docs/engineering/state.md`**).
- `python scripts/enforce-triad-hot-surface.py --rollover` -> **`rollover_complete units=1`** — **`docs/engineering/state-archive/state-pack-20260404-l.md`**.
- Pre-append: `python scripts/enforce-triad-hot-surface.py --check` -> **PASS** (exit **0**).
- Post-append (this QA block): `python scripts/enforce-triad-hot-surface.py --check` -> **FAIL** (`ARTIFACT_HOT_SURFACE_OVERSIZE`).
- `python scripts/enforce-triad-hot-surface.py --rollover` -> **`rollover_complete units=1`** — **`docs/engineering/state-archive/state-pack-20260404-m.md`**.
- Final `python scripts/enforce-triad-hot-surface.py --check` -> **PASS** (exit **0**).

