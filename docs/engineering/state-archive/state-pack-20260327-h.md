# State archive pack (2026-03-27)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 35
- First archived heading: `## Research checkpoint (2026-03-24) — US-0074`
- Last archived heading: `## Research checkpoint (2026-03-24) — US-0074`
- Verification tuple (mandatory):
  - archived_body_lines=43
  - preamble_lines=11
  - retained_body_lines=1186

---

## Research checkpoint (2026-03-24) — US-0074

- `/research` completed for **`US-0074`** in fresh **tech-lead** context (baseline
  regression cleanup: Homebrew/npm sync + `TEST_COMMAND` bootstrap root-cause
  notes).
- Deliverable: **`R-0051`** extended with **Post-discovery findings (2026-03-24) —
  US-0074** in `docs/engineering/research.md` (assert contracts, owning paths,
  npm-canonical vs formula, installer/CLI parity notes).
- Artifacts updated:
  - `docs/engineering/research.md` (`R-0051` post-discovery subsection)
  - `docs/product/backlog.md` (US-0074 research pointer)
  - `handoffs/resume_brief.md` (next phase → **`/architecture`**)
  - `docs/engineering/decisions.md` (current context pack → post-research)
  - `docs/engineering/state.md` (this checkpoint + boundary status)
- Next recommended phase: **`/architecture`** for **`US-0074`**.
- Stop boundary: research-only run complete in this context.

Isolation evidence (**US-0048** / **DEC-0029**):

- phase_id=research
- role=tech-lead
- fresh_context_marker=tech-lead-US0074-research-20260324T150000Z-fresh
- timestamp=2026-03-24T15:00:00Z
- evidence_ref=docs/engineering/research.md,docs/product/backlog.md,handoffs/resume_brief.md,docs/engineering/decisions.md,docs/engineering/state.md,sprints/S0051/qa-findings.md,tests/run-tests.ps1,tests/run-tests.sh,packaging/homebrew/its-magic.rb,package.json

Strict runtime proof (**US-0056** / **DEC-0038**):

- orchestrator_run_id=auto-20260324-01
- runtime_proof_id=rp-auto-20260324-01-research-tech-lead-20260324T150000Z-US0074
- phase_id=research
- role=tech-lead
- proof_issued_at=2026-03-24T15:00:00Z
- proof_ttl_seconds=3600
- proof_hash=d97a51b44c58fec96fe0f0e9d785e1f1296337edd9946869d1c99af3115c3ebf

## Phase boundary status (post-research, US-0074 / auto-20260324-01)

- `resolved_phase_plan_snapshot=intersected_executable_plan` per
  `## Auto continuation checkpoint (2026-03-24) — invocation auto-20260324-01 / US-0074`
- `skipped_phases=intake (reason: resume_anchor_before_phase)`
- `phase_boundary=research`
- `next_scheduled_phase=architecture`

