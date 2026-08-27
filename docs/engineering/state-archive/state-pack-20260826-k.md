# State archive pack (2026-08-26)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 25
- First archived heading: `## Intake checkpoint — US-0127..US-0129 batch / auto-20260825-01 (drain-generate persistence)`
- Last archived heading: `## Intake checkpoint — US-0127..US-0129 batch / auto-20260825-01 (drain-generate persistence)`
- Verification tuple (mandatory):
  - archived_body_lines=50
  - preamble_lines=15
  - retained_body_lines=1180

---

## Intake checkpoint — US-0127..US-0129 batch / auto-20260825-01 (drain-generate persistence)

- **phase_id**: intake
- **role**: po
- **model_id**: composer-2.5 (CROSS_MODEL_REVIEW=1 — required)
- **story_id**: US-0127
- **batch_story_ids**: US-0127, US-0128, US-0129
- **sprint_id**: pending
- **orchestrator_run_id**: auto-20260825-01
- **intake_run_id**: intake-drain-gen-auto-20260825-01-1
- **writer_id**: po-drain-gen-auto-20260825-01-1
- **delivery_mode**: ultra_lean
- **macro_phase**: spec
- **verdict**: INTAKE PASS (3 stories persisted OPEN; decision_gate=false)
- **fresh_context_marker**: po-US0127-intake-20260825T182030Z-fresh (NEW per US-0048 / BUG-0006)
- **timestamp**: 2026-08-25T18:20:30Z (UTC)
- **intake_evidence**: handoffs/intake_evidence/US-0127-intake-20260825.json, US-0128-intake-20260825.json, US-0129-intake-20260825.json (`[INTAKE_EVIDENCE_VALIDATION_OK]` each)
- **selected_pack**: small-intake-pack (per story; bounded refinements of US-0104/US-0110/US-0107/DEC-0054)
- **missing_topics**: []
- **assumptions_confirmed**: (none)
- **decomposition**: operator accepted all 3 drain-generate candidates (gate PASSED); split axis sovereign-loop-convergence (US-0127, US-0128) vs architecture-hot-surface (US-0129)
- **independent_checks**: backlog US-0127..US-0129 Status OPEN appended after US-0126; acceptance L155-L157 unchecked; US-0108/US-0121..US-0126 DONE rows and ticks untouched; intake_evidence_validate.py PASS x3
- **next_scheduled_phase**: `/discovery` (fresh PO for US-0127)
- **next_scheduled_role**: po
- **stop_condition**: STOP after intake artifacts. Orchestrator spawns `/discovery` in fresh PO subagent. Do NOT spawn discovery from this subagent. Do NOT mutate DONE rows.

### Triad hot-surface verification tuple (DEC-0054)

- pre_append_rollover=python scripts/enforce-triad-hot-surface.py --rollover exit 0 (units=2,1 state+po_to_tl)
- po_to_tl_pack=handoffs/archive/po-to-tl-pack-20260825-a.md (full intake handoff) + po-to-tl-pack-20260825-b.md (compact pointer)
- state_pack=docs/engineering/state-archive/state-pack-20260825-x.md
- post_rollover_check=python scripts/enforce-triad-hot-surface.py --check exit 0

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=intake`, `role=po`, `model_id=composer-2.5` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=po-US0127-intake-20260825T182030Z-fresh` (NEW per US-0048 / BUG-0006)
- `timestamp=2026-08-25T18:20:30Z` (UTC)
- Fresh PO intake subagent per BUG-0006 / US-0048 isolation; operator gate already PASSED for drain-generate candidates. No prior chat history. No `.env` reads. No DONE row mutation. No intake-evidence mutation of US-0121 bundle.

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260825-01`
- `runtime_proof_id=rp-auto-20260825-01-intake-po-20260825T182030Z-US-0127`
- `phase_id=intake`, `role=po`, `story_id=US-0127`, `sprint_id=pending`
- `proof_issued_at=2026-08-25T18:20:30Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-25T19:20:30Z` (UTC)
- `proof_hash=7C37D25CBCD5494B16AFC39478ED7E73A8CABFBF351034E9C14AAEE386B87134`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"spec","model_id":"composer-2.5","orchestrator_run_id":"auto-20260825-01","phase_id":"intake","proof_issued_at":"2026-08-25T18:20:30Z","proof_ttl_seconds":3600,"role":"po","runtime_proof_id":"rp-auto-20260825-01-intake-po-20260825T182030Z-US-0127","sprint_id":"pending","story_id":"US-0127"}`

