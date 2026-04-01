# State archive pack (2026-03-31)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 35
- First archived heading: `## Intake checkpoint (2026-03-30) — BUG-0001 / manual-20260330-BUG0001`
- Last archived heading: `## Intake checkpoint (2026-03-30) — BUG-0001 / manual-20260330-BUG0001`
- Verification tuple (mandatory):
  - archived_body_lines=37
  - preamble_lines=11
  - retained_body_lines=1193

---

## Intake checkpoint (2026-03-30) — BUG-0001 / manual-20260330-BUG0001

- **`/intake bug`** (PO) filed **`BUG-0001`**: packaged **`template/scripts/`** omits **`intake_*`** modules that exist under repo **`scripts/`**; **`package.json`** **`files`** includes **`template/`** — defect propagates to consumer installs (**scope**: intake-required script completeness only, not full mirror parity).
- **Pre-persistence gate**: `python scripts/intake_evidence_validate.py --file handoffs/intake_evidence/BUG-0001-intake-20260330.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`** (`intake_run_id=manual-20260330-BUG0001-intake`, **`small-intake-pack`**).
- **Post-persistence**: `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` → **`[BUG_VALIDATION_OK]`** (run after this checkpoint write).
- **Research**: **`R-0058`** (npm **`files`** semantics + repo inventory).
- **Next recommended phase**: **`/discovery`** (**TL**) for **`BUG-0001`** — installer/`template/scripts/` vs **`scripts/intake_*`**, tests, triple-installer parity.

Isolation evidence (**US-0048** / **DEC-0029**):

- `phase_id=intake`
- `role=po`
- `fresh_context_marker=po-BUG0001-intake-20260330T014500Z-fresh`
- `timestamp=2026-03-30T01:45:00Z`
- `evidence_ref=docs/product/backlog.md,docs/product/acceptance.md,docs/product/vision.md,handoffs/po_to_tl.md,handoffs/resume_brief.md,handoffs/intake_evidence/BUG-0001-intake-20260330.json,docs/engineering/research.md,scripts/intake_evidence_validate.py`

Strict runtime proof (**US-0056** / **DEC-0038**): canonical tuple hashed as **SHA-256** of **sorted-key JSON** over (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`).

- `orchestrator_run_id=manual-20260330-BUG0001`
- `runtime_proof_id=rp-manual-20260330-BUG0001-intake-po-20260330T014500Z-BUG0001`
- `phase_id=intake`
- `role=po`
- `proof_issued_at=2026-03-30T01:45:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=223e943fb52cac85ec752def20691e05b7d9c265e97ebff2a65d8bacbe0fc780`

## Phase boundary status (post-intake BUG-0001, manual-20260330-BUG0001)

- `phase_boundary=intake`
- `next_scheduled_phase=discovery`
- `bug_id=BUG-0001`
- `story_id=(none)`
- `sprint_id=(none)`
- `orchestrator_run_id=manual-20260330-BUG0001`

**Triad hot-surface (DEC-0054)** (post-intake BUG-0001 hygiene):

