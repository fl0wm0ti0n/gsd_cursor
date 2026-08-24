# State archive pack (2026-08-24)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 30
- First archived heading: `## Refresh-context terminal checkpoint â€” US-0123 / S0123 / auto-20260824-01 (segment closed, lifecycle terminal)`
- Last archived heading: `## Refresh-context terminal checkpoint â€” US-0123 / S0123 / auto-20260824-01 (segment closed, lifecycle terminal)`
- Verification tuple (mandatory):
  - archived_body_lines=85
  - preamble_lines=15
  - retained_body_lines=1137

---

## Refresh-context terminal checkpoint â€” US-0123 / S0123 / auto-20260824-01 (segment closed, lifecycle terminal)

- **phase_id**: refresh-context, **role**: curator, **story_id**: US-0123, **sprint_id**: S0123
- `orchestrator_run_id=auto-20260824-01`, `delivery_mode=ultra_lean`
- `macro_phase=ship` (refresh-context â€” third canonical phase per DEC-0082: release â†’ closure â†’ refresh-context)
- `model_id=composer-2.5` (CROSS_MODEL_REVIEW=1 â€” required)
- `verdict=PASS`
- `segment_closed=true`, `lifecycle_terminal=true`
- `native_chain_active=true`
- `stop_phase=refresh-context`
- `stop_reason=completed` (segment complete â€” NOT segment exhausted; drain-advance is orchestrator-owned)
- `fresh_context_marker=curator-US0123-refresh-context-20260824T154200Z-fresh` (NEW per BUG-0006)
- `timestamp (UTC)=2026-08-24T15:42:00Z`

### Segment closure verification (rg checks)

| Check | Command / path | Result |
|-------|----------------|--------|
| Backlog DONE | `docs/product/backlog.md` US-0123 block `Status: DONE` (L4248) | PASS |
| Acceptance checked | `docs/product/acceptance.md` `- [x] US-0123:` (L151) | PASS |
| Closure checkpoint | `docs/engineering/state.md` `phase_id=closure` + US-0123 | PASS |
| Closure artifact | `sprints/S0123/closure-verification.md` | PASS (`[VALIDATE_CLOSURE_VERIFICATION_OK]`) |
| Active context surface | `docs/engineering/state.md` L7 `## Active context surface (US-0053 / DEC-0035)` | PASS (preserved; file not emptied) |

### Triad rollover

**Rollover performed (two passes).** Pass 1 (pre-append): `python scripts/enforce-triad-hot-surface.py --rollover` â†’ units=11 â†’ `docs/engineering/state-archive/state-pack-20260824-m.md` (archived_body_lines=456; retained_body_lines=1158; first archived=`## QA checkpoint â€” US-0122`; last archived=`## Refresh-context terminal checkpoint â€” US-0122`). Pass 2 (post-append): units=1 â†’ `docs/engineering/state-archive/state-pack-20260824-n.md` (archived_body_lines=56; retained_body_lines=1186; archived=`## Sovereign-critic checkpoint â€” US-0122` refresh-context). `triad_rollover_required=true`. Final `python scripts/enforce-triad-hot-surface.py --check` â†’ PASS (exit 0).

### Segment closure summary

US-0123 (Per-role OpenCode model slug routing, DEC-0123) fully closed through all macro-phases: spec â†’ research â†’ architecture â†’ sprint-plan â†’ execute (harness-refresh) â†’ qa (loop 2) â†’ verify-work (loop 2) â†’ release (1st attempt) â†’ closure â†’ sovereign-critic â†’ refresh-context.

Final state:
- Sprint S0123 RELEASED (`handoffs/release_queue.md` status=released @ 2026-08-24T15:32:00Z).
- US-0123 DONE (`docs/product/backlog.md` L4248; `/closure` flipped OPENâ†’DONE).
- `docs/product/acceptance.md` US-0123 row `- [ ]`â†’`- [x]` (L151).
- `sprints/S0123/closure-verification.md` PASS.
- 10/10 ACs satisfied. 8/8 contract tests PASS (`tests/us0123_contract_test.py`).
- Compose guards unchanged (backlog/acceptance/architecture/DEC-0123 untouched by refresh-context).

### Non-blocking findings (carried forward)

1. `ik_us0123_installer_hook_not_contract_tested` â€” informational (T-003 installer hook not pytest-marked).

### Drain state

- `drain_active=true` (`AUTO_BACKLOG_DRAIN=1`)
- `next_eligible_open_story=US-0124` (OPEN â€” orchestrator-owned drain-advance; curator STOP)
- `next_scheduled_phase=drain-advance` (orchestrator-owned; do NOT spawn US-0124 spec from curator)

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=refresh-context`
- `role=curator`
- `model_id=composer-2.5`
- `fresh_context_marker=curator-US0123-refresh-context-20260824T154200Z-fresh`
- `timestamp=2026-08-24T15:42:00Z` (UTC)
- `evidence_ref=sprints/S0123/summary.md (terminal context) + docs/engineering/state-archive/state-pack-20260824-m.md + docs/engineering/state-archive/state-pack-20260824-n.md + handoffs/resume_brief.md (refresh-context prepend)`
- Curator subagent spawned fresh per BUG-0006 / US-0048; context limited to segment closure artifacts, triad rollover, and sprint summary compaction.
- Prior closure-phase strict proof consumed: `rp-auto-20260824-01-closure-qe-20260824T153400Z-US-0123` (proof_hash=8023B60A517FC3561E26F76D0767E2EC5A1D16FE7282F3DC89E4BE159C8F2023).

### Strict runtime proof tuple (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-refresh-context-curator-20260824T154200Z-US-0123`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"ship","model_id":"composer-2.5","orchestrator_run_id":"auto-20260824-01","phase_id":"refresh-context","proof_issued_at":"2026-08-24T15:42:00Z","proof_ttl_seconds":3600,"role":"curator","runtime_proof_id":"rp-auto-20260824-01-refresh-context-curator-20260824T154200Z-US-0123","sprint_id":"S0123","story_id":"US-0123"}`
- `proof_hash=CFB6B0111353F5799E1F1C8A3EDD8CCC3DC127322DD69D6CE8E0A3ED3BDE701D` (SHA-256 of sorted-key JSON payload)
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-08-24T16:42:00Z` (UTC = issued_at + 3600s)

### DEC-0038 proof (strict runtime proof)

- Each `/refresh-context` execution produces its own strict runtime proof with unique `runtime_proof_id` per DEC-0038.
- `proof_hash` = SHA-256 of canonical sorted-key JSON payload (12 fields: delivery_mode, macro_phase, model_id, orchestrator_run_id, phase_id, proof_issued_at, proof_ttl_seconds, role, runtime_proof_id, sprint_id, story_id).
- `proof_ttl_seconds=3600` (1-hour TTL per DEC-0038).
- `proof_issued_at=2026-08-24T15:42:00Z` (ISO-8601 UTC).
- This refresh-context runtime proof is distinct from the producer closure runtime proof (`rp-auto-20260824-01-closure-qe-20260824T153400Z-US-0123`); no proof_id reuse.

### Decision gate + next scheduled phase

- `decision_gate=false`
- `next_scheduled_phase=drain-advance` (orchestrator-owned; intended next: US-0124 spec intake+discovery)
- `stop_condition=STOP after refresh-context completes (segment boundary). Hand off via artifacts only to orchestrator for drain-advance. Do NOT spawn US-0124 from curator.

---

