# State archive pack (2026-04-12)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 18
- First archived heading: `## QA checkpoint (2026-04-04) — S0070 / BUG-0008 / auto-20260404-03 (post-harness remediation)`
- Last archived heading: `## QA checkpoint (2026-04-04) — S0070 / BUG-0008 / auto-20260404-03 (post-harness remediation)`
- Verification tuple (mandatory):
  - archived_body_lines=41
  - preamble_lines=11
  - retained_body_lines=1192

---

## QA checkpoint (2026-04-04) — S0070 / BUG-0008 / auto-20260404-03 (post-harness remediation)

- **`/qa`** completed for **`S0070`** / **`BUG-0008`** in fresh **qa** context (`orchestrator_run_id=auto-20260404-03`).
- **Verdict**: **`sprints/S0070/qa-findings.md`** **PASS_WITH_DEFERRALS** — in-repo **BUG-0008** bar unchanged (guards, **26P2**, **`bug_issue_validate --check-acceptance`**). **`tests/report.md`** (**2026-04-04T20:25:29Z**) **794** pass / **0** fail — dev **`RELEASE_TEST_FAILED` remediation** clears prior **§26P** (**`installer_shell_bug0004_test`**) failure path; **§26P2** remains **PASS**. **Operator deferrals unchanged**: **`npm publish`** (**AC-6**); Debian global **E2E** (**AC-5**). **`BUG-0008`** remains **OPEN** (**US-0045**); **`docs/product/acceptance.md`** **BUG-0008** row stays unchecked.
- **Next recommended phase**: **`/verify-work`** for **`S0070`** / **`BUG-0008`** (`next_scheduled_phase=verify-work`) — reconcile UAT with green harness and outstanding publish/E2E evidence.

Isolation evidence (**US-0048** / **DEC-0029**):

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0070-BUG0008-qa-20260404T210000Z-fresh`
- `timestamp=2026-04-04T21:00:00Z`
- `evidence_ref=sprints/S0070/qa-findings.md,handoffs/dev_to_qa.md,handoffs/qa_to_verify_work.md,tests/report.md,docs/product/backlog.md,docs/product/acceptance.md,docs/engineering/state.md`

Strict runtime proof (**US-0056** / **DEC-0038**): canonical tuple hashed as **SHA-256** of **sorted-key JSON** over (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`). **`proof_ttl_seconds`** is serialized as a JSON **integer** (not a string) in the hashed payload.

- `orchestrator_run_id=auto-20260404-03`
- `runtime_proof_id=rp-auto-20260404-03-qa-qa-20260404T210000Z-S0070-BUG0008-rereport`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-04-04T21:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=c7634e8cdfc44c46f7312483144e1592f503208e22755f19cac353f1240ff3c7`

## Phase boundary status (post-qa post-harness-remediation, S0070 / BUG-0008 / auto-20260404-03)

- `phase_boundary=qa`
- `next_scheduled_phase=verify-work`
- `bug_id=BUG-0008`
- `story_id=(none)`
- `sprint_id=S0070`
- `orchestrator_run_id=auto-20260404-03`

**Phase boundary operator visibility (AC-10)** — compact status: `phase_boundary=qa`; `next_scheduled_phase=verify-work`; `bug_id=BUG-0008`; `sprint_id=S0070`; `orchestrator_run_id=auto-20260404-03`; `tests/report.md=794/0@2026-04-04T20:25:29Z`.

**Triad hot-surface (DEC-0054)** (post-QA S0070 post-harness-remediation hygiene):

- Post-append: `python scripts/enforce-triad-hot-surface.py --check` → **FAIL** (`ARTIFACT_HOT_SURFACE_OVERSIZE` on **`docs/engineering/state.md`**).
- `python scripts/enforce-triad-hot-surface.py --rollover` → **`rollover_complete units=1`** — **`docs/engineering/state-archive/state-pack-20260404-p.md`**.
- Final `python scripts/enforce-triad-hot-surface.py --check` → **PASS** (exit **0**).

