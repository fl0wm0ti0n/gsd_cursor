# State archive pack (2026-08-24)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 3
- Retained units in hot file: 27
- First archived heading: `## Discovery checkpoint — US-0123 / (pending) / auto-20260824-01`
- Last archived heading: `## Research checkpoint — US-0123 / (pending) / auto-20260824-01`
- Verification tuple (mandatory):
  - archived_body_lines=125
  - preamble_lines=15
  - retained_body_lines=1155

---

## Discovery checkpoint — US-0123 / (pending) / auto-20260824-01

- **phase_id**: discovery, **role**: po, **story_id**: US-0123, **sprint_id**: (pending)
- `orchestrator_run_id=auto-20260824-01`, `delivery_mode=ultra_lean`
- `macro_phase=spec` (intake + discovery merged per US-0096 / DEC-0082 ultra_lean macro)
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required on isolation)
- `verdict=PASS` (no DECISION_GATE; D1–D10 discovery locks authored; DQ1..DQ10 open questions routed to `/research`)
- `decision_gate=false`
- `status=OPEN` (do not mark US-0123 DONE)
- `fresh_context_marker=po-US0123-discovery-20260824T155200Z-fresh`
- `timestamp (UTC)=2026-08-24T15:52:00Z`
- `discovery_locks=D1..D10` (D1 resolution chain shape; D2 multi-provider examples local-only; D3 no vendor IDs in template; D4 unknown slug fail-closed; D5 auth store in /connect; D6 compose US-0101/US-0102 additive; D7 ≥2 roles different providers; D8 test_us0123_* contract tests; D9 Chinese APIs as capability no kit proxy; D10 tool-calling quality runbook note owned with US-0126 if needed)
- `open_questions_for_research=DQ1..DQ10` (DQ1 source of truth — primary; DQ2 placeholder vs omit model:; DQ3 fail-closed reason-code family; DQ4 catalog file path; DQ5 per-role vs per-phase mapping; DQ6 Chinese API examples without vendor IDs; DQ7 compose with US-0122 agents; DQ8 provider mode; DQ9 validator surface; DQ10 tool-calling quality note ownership)
- `research_anchor=docs/engineering/research.md ## R-0109` (US-0123 DQ1..DQ10 to be deepened by tech-lead; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 locks NOT wiped)
- `compose_guards_unchanged=5/5 verified` (same as intake; US-0101/US-0102/US-0003/US-0122/US-0121)
- `risks_carried=R1..R6` (intake-identified; to be deepened/accepted in `/research` then `/architecture`)
- `dc_check=clean` (no `# US-0123` anchor in architecture.md yet — expected; `/architecture` resolves after `/research`)

### Strict runtime proof tuple (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-discovery-po-20260824T155200Z-US-0123`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"spec","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"discovery","proof_issued_at":"2026-08-24T15:52:00Z","proof_ttl_seconds":3600,"role":"po","runtime_proof_id":"rp-auto-20260824-01-discovery-po-20260824T155200Z-US-0123","sprint_id":"(pending)","story_id":"US-0123"}`
- `proof_hash=66d9fa996e2e63eeff14bcf626828c110f1bb854cebc1c3511e503fad048e5f2` (SHA-256 of sorted-key JSON payload)
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-08-24T16:52:00Z` (UTC = issued_at + 3600s)

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=discovery`
- `role=po`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=po-US0123-discovery-20260824T155200Z-fresh`
- `timestamp=2026-08-24T15:52:00Z`
- `evidence_ref=docs/product/vision.md ## Discovery Notes — US-0123 + docs/product/backlog.md ## US-0123 + handoffs/po_to_tl.md ## Spec handoff — US-0123`

### Decision gate

- `decision_gate=false` (no DECISION_GATE; no hard stop; D1..D10 locks authored; DQ1..DQ10 open for `/research`; AC-1..AC-10 unchanged; compose guards 5/5 verified)
- `stop_conditions_met=yes` (no missing references; no decision gate triggered; discovery locks complete)

### Next scheduled phase

- `next_scheduled_phase=research` (role=tech-lead; deepen R-0109 for US-0123)
- `stop_condition=STOP after spec (intake+discovery) completes; hand off via artifacts only to /research (tech-lead). Do NOT spawn /architecture from discovery.`

## Sovereign-critic checkpoint — US-0123 / (pending) / auto-20260824-01 (producer: po / spec)

- `orchestrator_run_id=auto-20260824-01`
- `phase_id=sovereign-critic`
- `role=tech-lead`
- `producer_phase=spec` (intake + discovery merged; ultra_lean per US-0096 / DEC-0082)
- `producer_role=po`
- `producer_model_id=glm-5.2-high`
- `critic_model_id=composer-2.5-fast`
- `story_id=US-0123`
- `sprint_id=(pending)`
- `verdict=PASS` (independent checks green: no new story ID; US-0123 OPEN L4248; US-0122 DONE L4196; acceptance L151 unchecked; intake evidence NOT mutated; DQ1..DQ10 present; 0 blocking findings; anti_slop_aggregate=8)
- `fresh_context_marker=tl-US0123-sovereign-critic-spec-20260824T160000Z-fresh`
- `timestamp=2026-08-24T16:00:00Z` (UTC)
- `model_id=composer-2.5-fast` (CROSS_MODEL_REVIEW=1 — required)
- `evidence_ref=handoffs/sovereign_critic_findings.jsonl (US-0123 spec rows) + docs/product/backlog.md ## US-0123 + docs/product/vision.md ## Intake Notes — US-0123 + ## Discovery Notes — US-0123 + handoffs/po_to_tl.md ## Spec handoff — US-0123 + docs/engineering/state.md (intake + discovery checkpoints) + handoffs/intake_evidence/US-0121-intake-20260822.json (read-only verify)`
- `producer_runtime_proof_ids=rp-auto-20260824-01-intake-po-20260824T154800Z-US-0123 (proof_hash=6c9aabdc49ea8c6c4f1285b1c7a6146cd43d6e8b7bcdc4a8174dbacb0468f578); rp-auto-20260824-01-discovery-po-20260824T155200Z-US-0123 (proof_hash=66d9fa996e2e63eeff14bcf626828c110f1bb854cebc1c3511e503fad048e5f2)`
- `independent_checks=backlog US-0123 OPEN L4248; acceptance L151 unchecked; US-0122 DONE L4196; US-0121 DONE L4127; intake JSON model-slug-routing -> US-0123 coverage_complete=true not mutated; DQ1..DQ10 in vision/backlog/state; template/.opencode/agents/*.md no model: keys; compose guards 5/5 verified`
- `anti_slop_aggregate=8` (challenger=8, architect=8, subtractor=8)
- `open_blocking_findings=0` (3 non-blocking: ik_us0123_d3_dq6_grep_example_tension; ik_us0123_sot_catalog_coupling_dq14579; ik_us0123_spec_scope_minimal_pass informational)
- `status=OPEN` (do not mark US-0123 DONE)
- `next_scheduled_phase=/research`
- `next_scheduled_role=tech-lead`
- `stop_condition=STOP after sovereign-critic; hand off via artifacts only to /research in fresh tech-lead subagent (BUG-0006). Do NOT spawn /research from sovereign-critic.`

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=sovereign-critic`
- `role=tech-lead`
- `fresh_context_marker=tl-US0123-sovereign-critic-spec-20260824T160000Z-fresh`
- `timestamp=2026-08-24T16:00:00Z`
- `model_id=composer-2.5-fast` (CROSS_MODEL_REVIEW=1 — required)
- `evidence_ref=handoffs/sovereign_critic_findings.jsonl (US-0123 spec rows) + docs/engineering/state.md (this checkpoint)`

## Research checkpoint — US-0123 / (pending) / auto-20260824-01

- **phase_id**: research, **role**: tech-lead, **story_id**: US-0123, **sprint_id**: (pending)
- `orchestrator_run_id=auto-20260824-01`, `delivery_mode=ultra_lean`
- `macro_phase=plan` (research — first canonical phase of `plan` per US-0096 / DEC-0082 ultra_lean macro)
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required on isolation)
- `verdict=PASS` (no DECISION_GATE; 10/10 discovery open questions DQ1..DQ10 closed LOCKED; architecture seeds proposed; companion DEC-0123 to be authored in `/architecture`)
- `decision_gate=false`
- `status=OPEN` (do not mark US-0123 DONE; do not mutate US-0121/US-0122 DONE)
- `fresh_context_marker=tl-US0123-research-20260824T160500Z-fresh`
- `timestamp (UTC)=2026-08-24T16:05:00Z`
- `research_anchor=docs/engineering/research.md ## R-0109` (US-0123 deepened findings appended; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 locks PRESERVED — not wiped)
- `dq_locks=DQ1..DQ10` (DQ1 SOT=local-only catalog `.opencode/model-catalog.local.json`; DQ2 template agents omit `model:`; DQ3 single `OPENCODE_MODEL_SLUG_UNKNOWN` code; DQ4 catalog path `.opencode/model-catalog.local.json` separate from Cursor; DQ5 per-role schema, US-0069 bridges phase→role; DQ6 single example surface `template/.opencode/model-catalog.local.example.json` placeholders only; DQ7 additive — template agents unchanged, materializer injects into installed agents only; DQ8 OpenCode=always `api` mode, kit does not proxy; DQ9 extend `model_tier_validate.py --scope opencode-catalog`; DQ10 stub runbook line + h2 anchor, US-0126 owns full text)
- `critic_nbs_closed=3` (ik_us0123_d3_dq6_grep_example_tension → D3 grep scope excludes `*.example.json`; ik_us0123_sot_catalog_coupling_dq14579 → ONE SOT + forbidden surfaces; ik_us0123_spec_scope_minimal_pass → DQ1-DQ10 closed before marker enumeration)
- `companion_dec=decisions/DEC-0123.md` (Required — index stub appended to `docs/engineering/decisions.md`; `/architecture` flips to Accepted)
- `compose_guards_unchanged=6/6 verified` (US-0101/DEC-0086, US-0102/DEC-0087, US-0003, US-0122/DEC-0122, US-0121, US-0080)
- `risks_finalized=R1..R7` (R1 SOT ambiguity; R2 vendor slug leakage; R3 unknown slug silent fallback; R4 Chinese API vendor ID leak; R5 per-role vs per-phase mismatch; R6 kit proxy; R7 validator duplication drift)
- `dc_check=clean` (no `# US-0123` anchor in architecture.md yet — expected; `/architecture` resolves after `/research`)

### Strict runtime proof tuple (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-research-tech-lead-20260824T160500Z-US-0123`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"research","proof_issued_at":"2026-08-24T16:05:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260824-01-research-tech-lead-20260824T160500Z-US-0123","sprint_id":"(pending)","story_id":"US-0123"}`
- `proof_hash=FAE07A6C872F5A3C7028B00653A9540CEB11BAE8570B252D75676090E24BF351` (SHA-256 of sorted-key JSON payload, UTF-8 bytes via PowerShell — python missing on PATH)
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T17:05:00Z` (UTC = issued_at + 3600s)

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=research`, `role=tech-lead`, `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=tl-US0123-research-20260824T160500Z-fresh`, `timestamp=2026-08-24T16:05:00Z`
- `evidence_ref=docs/engineering/research.md (R-0109 US-0123 deepened findings) + docs/product/backlog.md ## US-0123 + docs/product/vision.md ## Intake + Discovery Notes — US-0123 + handoffs/po_to_tl.md (US-0123 spec pointer) + handoffs/sovereign_critic_findings.jsonl (US-0123 spec rows) + decisions/DEC-0086.md + decisions/DEC-0087.md (read-only compose) + scripts/model_tier_validate.py (grep anchors) + template/.opencode/agents/*.md (grep ^model: zero matches)`
- Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to narrow-read files (US-0053 / US-0096 Tranche A). No `.env` reads, no credentials access, no intake-evidence mutation, no backlog status/AC mutation.
- `assemble_sovereign_memory_digest(...)` NOT called (US-0123 first story of new drain segment; R-0109 US-0121+US-0122 context sufficient).
- No write to `mistakes.jsonl` in research phase.

### Decision gate

- `decision_gate=false` (no DECISION_GATE; no hard stop; 10/10 DQs closed LOCKED; architecture seeds proposed; companion DEC-0123 to be authored in `/architecture`)
- `stop_conditions_met=yes` (no missing references — all 6 compose targets verified; no decision gate triggered)

### Next scheduled phase

- `next_scheduled_phase=/architecture` (role=tech-lead per US-0069 / DEC-0051 phase→role matrix default; second canonical phase of `plan` macro per ultra_lean)
- `next_scheduled_role=tech-lead`
- `stop_condition=STOP after research completes; hand off via artifacts only to /architecture in fresh tech-lead subagent (BUG-0006). Do NOT spawn /architecture from this subagent.`

