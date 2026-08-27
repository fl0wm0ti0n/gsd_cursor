# State archive pack (2026-08-26)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 24
- First archived heading: `## Discovery checkpoint — US-0127 / auto-20260825-01`
- Last archived heading: `## Discovery checkpoint — US-0127 / auto-20260825-01`
- Verification tuple (mandatory):
  - archived_body_lines=48
  - preamble_lines=15
  - retained_body_lines=1174

---

## Discovery checkpoint — US-0127 / auto-20260825-01

- **phase_id**: discovery
- **role**: po
- **model_id**: composer-2.5 (CROSS_MODEL_REVIEW=1 — required)
- **story_id**: US-0127
- **batch_story_ids**: US-0128, US-0129 (siblings — not discovery-locked in this spawn)
- **sprint_id**: pending
- **orchestrator_run_id**: auto-20260825-01
- **intake_run_id**: intake-drain-gen-auto-20260825-01-1
- **delivery_mode**: ultra_lean
- **macro_phase**: spec
- **verdict**: DISCOVERY PASS (decision_gate=false)
- **fresh_context_marker**: po-US0127-discovery-20260825T182731Z-fresh (NEW per US-0048 / BUG-0006)
- **timestamp**: 2026-08-25T18:27:31Z (UTC)
- **discovery_locks**: D1 blocking-only conjunct (`_critic_jsonl_has_open` → `read_open_blocking` semantics); D2 auto-resolve non-blocking at sovereign-critic PASS; D3 `scripts/sovereign_critic_hygiene.py`; D4 `test_us0127_*`; D5 runbook/reason codes; D6 `SOVEREIGN_CRITIC_PAIRS`; D7 QA fallback degrade; D8–D10 compose US-0104/US-0110/US-0107 read-only
- **research_questions**: DQ1..DQ8 routed to `/research` (research owns R-id; sovereign-loop subsection — not R-0109 OpenCode epic)
- **independent_checks**: backlog US-0127 discovery_notes appended; Status OPEN unchanged; AC-1..AC-6 unchecked; acceptance L155 unchecked; US-0108/US-0121..US-0126 DONE preserved; US-0128/US-0129 blocks untouched; vision `## Discovery Notes — US-0127` appended; po_to_tl prepended; resume_brief prepended → `/research` role=tech-lead
- **next_scheduled_phase**: `/research` (fresh tech-lead for US-0127)
- **next_scheduled_role**: tech-lead
- **stop_condition**: STOP after discovery artifacts. Orchestrator spawns `/research` in fresh tech-lead subagent. Do NOT spawn research from this subagent. Do NOT mutate DONE rows. Do NOT author architecture.md `# US-0127`.

### Triad hot-surface verification tuple (DEC-0054)

- pre_append_rollover=python scripts/enforce-triad-hot-surface.py --rollover exit 0 (rollover_complete units=2,1 state+po_to_tl)
- po_to_tl_pack=handoffs/archive/po-to-tl-pack-20260825-c.md (1 unit; archived US-0123 spec pointer prefix)
- state_pack=docs/engineering/state-archive/state-pack-20260825-y.md (2 units; archived_body_lines=94; preamble_lines=15)
- retained=state.md hot surface incl. US-0127 discovery checkpoint; Active context surface preserved
- post_rollover_check=python scripts/enforce-triad-hot-surface.py --check exit 0

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=discovery`, `role=po`, `model_id=composer-2.5` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=po-US0127-discovery-20260825T182731Z-fresh` (NEW per US-0048 / BUG-0006)
- `timestamp=2026-08-25T18:27:31Z` (UTC)
- Fresh PO discovery subagent per BUG-0006 / US-0048 isolation; consumed intake producer proof `rp-auto-20260825-01-intake-po-20260825T182030Z-US-0127`. No prior chat history. No `.env` reads. No DONE row mutation.

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260825-01`
- `runtime_proof_id=rp-auto-20260825-01-discovery-po-20260825T182731Z-US-0127`
- `phase_id=discovery`, `role=po`, `story_id=US-0127`, `sprint_id=pending`
- `proof_issued_at=2026-08-25T18:27:31Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-25T19:27:31Z` (UTC)
- `proof_hash=649D169D12BFDDDE4F2071BB0B1048A558E890B85C14C2B1042E13CB6469B981`
- `hash_recompute_confirmation=true`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"spec","model_id":"composer-2.5","orchestrator_run_id":"auto-20260825-01","phase_id":"discovery","proof_issued_at":"2026-08-25T18:27:31Z","proof_ttl_seconds":3600,"role":"po","runtime_proof_id":"rp-auto-20260825-01-discovery-po-20260825T182731Z-US-0127","sprint_id":"pending","story_id":"US-0127"}`

