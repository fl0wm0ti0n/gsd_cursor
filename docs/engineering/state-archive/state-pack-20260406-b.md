# State archive pack (2026-04-06)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 28
- First archived heading: `## Research checkpoint (2026-04-04) — US-0084 / auto-20260404-02`
- Last archived heading: `## Architecture checkpoint (2026-04-04) — US-0084 / auto-20260404-02`
- Verification tuple (mandatory):
  - archived_body_lines=72
  - preamble_lines=11
  - retained_body_lines=1171

---

## Research checkpoint (2026-04-04) — US-0084 / auto-20260404-02

- **`/research`** completed for **`US-0084`** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260404-02`).
- **Summary**: Repo **`installer.sh`** unconditional startup is POSIX-safe (**`set -e`** only at **`installer.sh:2`**; **BUG-0004** comment **`installer.sh:4–5`**); **`bin/its-magic.js`** spawns **`sh`** with package **`installer.sh`** on non-Windows (**`bin/its-magic.js:182–195`**). Publish parity risk is **tarball/CRLF vs git**, not a second **`template/installer.sh`** copy. Extend guards with **LF/CRLF check**, optional **`dash -n`**, and harness registration; map **WSL** / **SSH** / **Docker-over-SSH** to existing **`docs/engineering/release-targets.json`** (**`ssh-server`**, **`dockerOverSsh`**) + **`runtime-connectivity.md`**; sketch **`REMOTE_CONFIG`** helper + exit codes in **`R-0067`**. **Next recommended phase**: **`/architecture`**.

Isolation evidence (**US-0048** / **DEC-0029**):

- `phase_id=research`
- `role=tech-lead`
- `fresh_context_marker=tech-lead-US0084-research-20260404T160000Z-fresh`
- `timestamp=2026-04-04T16:00:00Z`
- `evidence_ref=docs/engineering/research.md,docs/product/backlog.md,handoffs/po_to_tl.md,installer.sh,bin/its-magic.js,package.json,docs/engineering/release-targets.json,docs/engineering/runtime-connectivity.md,.cursor/scratchpad.md,tests/installer_shell_bug0004_test.py,tests/run-tests.sh,tests/run-tests.ps1,handoffs/intake_evidence/US-0084-intake-20260404.json`

Strict runtime proof (**US-0056** / **DEC-0038**): canonical tuple hashed as **SHA-256** of **sorted-key JSON** over (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`). **`proof_ttl_seconds`** is serialized as a JSON **integer** (not a string) in the hashed payload.

- `orchestrator_run_id=auto-20260404-02`
- `runtime_proof_id=rp-auto-20260404-02-research-tech-lead-20260404T160000Z-US0084`
- `phase_id=research`
- `role=tech-lead`
- `proof_issued_at=2026-04-04T16:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=d323717a9051edfd2a5a0842694fb79a7486fe627806a8a1274f59302e3bc87e`

## Phase boundary status (post-research, US-0084 / auto-20260404-02)

- `resolved_phase_plan_snapshot`=(orchestrator materialization for **`auto-20260404-02`** — research segment; not rewritten at research writer)
- `skipped_phases_summary`=(intake omitted per resume anchor — unchanged at research writer)
- `phase_boundary=research`
- `next_scheduled_phase=architecture`
- `bug_id=(none)`
- `story_id=US-0084`
- `sprint_id=(none)`
- `orchestrator_run_id=auto-20260404-02`

**Phase boundary operator visibility (AC-10)** — compact status: `phase_boundary=research`; `next_scheduled_phase=architecture`; `bug_id=(none)`; `story_id=US-0084`; `sprint_id=(none)`; `orchestrator_run_id=auto-20260404-02`.

## Architecture checkpoint (2026-04-04) — US-0084 / auto-20260404-02

- **`/architecture`** completed for **`US-0084`** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260404-02`).
- **Summary**: Locked POSIX/dash/LF for published **`installer.sh`**, layered **CI**/**prepublish**/Python + optional **`dash -n`**, **US-0064** doc map (**WSL** / **`ssh-server`** / **`dockerOverSsh`**), helper **`scripts/remote_config_summary.py`** + exit codes, harness **H1–H5**, runbook **`REMOTE_EXECUTION`** troubleshooting + evidence cues, active/**`template/`** parity. Canonical: **`docs/engineering/architecture.md`** **`# US-0084`**. **Next recommended phase**: **`/sprint-plan`**.

Isolation evidence (**US-0048** / **DEC-0029**):

- `phase_id=architecture`
- `role=tech-lead`
- `fresh_context_marker=tech-lead-US0084-architecture-20260404T170000Z-fresh`
- `timestamp=2026-04-04T17:00:00Z`
- `evidence_ref=docs/engineering/architecture.md,docs/product/backlog.md,docs/engineering/research.md,installer.sh,package.json,docs/engineering/release-targets.json,docs/engineering/runtime-connectivity.md,docs/engineering/runbook.md,bin/its-magic.js,tests/installer_shell_bug0004_test.py,tests/run-tests.sh,tests/run-tests.ps1,handoffs/intake_evidence/US-0084-intake-20260404.json`

Strict runtime proof (**US-0056** / **DEC-0038**): canonical tuple hashed as **SHA-256** of **sorted-key JSON** over (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`). **`proof_ttl_seconds`** is serialized as a JSON **integer** (not a string) in the hashed payload.

- `orchestrator_run_id=auto-20260404-02`
- `runtime_proof_id=rp-auto-20260404-02-architecture-tech-lead-20260404T170000Z-US0084`
- `phase_id=architecture`
- `role=tech-lead`
- `proof_issued_at=2026-04-04T17:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=6bdea97d888d2d70c024c137b250f314cdd2c4544c589a8cb70f35931d776c44`

## Phase boundary status (post-architecture, US-0084 / auto-20260404-02)

- `resolved_phase_plan_snapshot`=(orchestrator materialization for **`auto-20260404-02`** — architecture segment; not rewritten at architecture writer)
- `skipped_phases_summary`=(intake omitted per resume anchor — unchanged at architecture writer)
- `phase_boundary=architecture`
- `next_scheduled_phase=sprint-plan`
- `bug_id=(none)`
- `story_id=US-0084`
- `sprint_id=(none)`
- `orchestrator_run_id=auto-20260404-02`

**Phase boundary operator visibility (AC-10)** — compact status: `phase_boundary=architecture`; `next_scheduled_phase=sprint-plan`; `bug_id=(none)`; `story_id=US-0084`; `sprint_id=(none)`; `orchestrator_run_id=auto-20260404-02`.

