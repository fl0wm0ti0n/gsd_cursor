# PO to TL archive pack (2026-07-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 7
- First archived heading: `## Architecture handoff — US-0119 / (pending) / auto-20260705-us0119-intake`
- Last archived heading: `## Research handoff — US-0119 / (pending) / auto-20260705-us0119-intake`
- Verification tuple (mandatory):
  - archived_body_lines=120
  - retained_body_lines=580

---

## Architecture handoff — US-0119 / (pending) / auto-20260705-us0119-intake

**Phase completed**: architecture
**Phase role**: tech-lead
**Story**: US-0119 Autonomous-autonomy presets and configurable hard-stop relaxation
**Verdict**: PASS (companion DEC-0119 authored Accepted; approach A1 locked; 12 sprint seeds within SPRINT_MAX_TASKS=12; risks R1..R8 finalized)
**Timestamp**: 2026-07-05T22:45:00Z (UTC)
**Fresh context marker**: tl-US0119-architecture-20260705T224500Z-fresh
**Runtime proof**: rp-auto-20260705-us0119-architecture-techlead-20260705T224500Z-US-0119 (proof_hash=71d0ac09ece22e540a8c8002555fe8f6720c6b5bcd77eb6b6eb09cc34360b1e9, proof_ttl=2026-07-05T23:45:00Z)
**Delivery mode**: ultra_lean (plan macro = research+architecture+sprint-plan merged)
**Macro phase**: plan (architecture — second canonical phase of plan macro per US-0096 / DEC-0082)

### Summary

`## US-0119` h1 anchor added to `docs/engineering/architecture.md` in THIS phase (T-anch NO-OP in /execute). Companion DEC `decisions/DEC-0119.md` authored Accepted. Approach A1 locked (single vertical-slice approach — no alternatives retained). 12 sprint seeds T-anch + T-001..T-011 within SPRINT_MAX_TASKS=12. Risks R1..R8 finalized. Compose-do-not-amend verified 6/6. DC check clean. Strict runtime proof recorded.

### Architecture anchor

- `docs/engineering/architecture.md` `## US-0119` (added in THIS phase per R-0105 Q-2 LOCKED pattern; T-anch NO-OP / verification in /execute)
- Companion DEC `decisions/DEC-0119.md` (authored Accepted in THIS phase; mirrors DEC-0082 / DEC-0078 precedent)

### Compose, do not amend (verified — 6/6)

| Story | Status |
|-------|--------|
| US-0092 / DEC-0078 | ✓ UNCHANGED |
| US-0095 | ✓ UNCHANGED |
| US-0056 / DEC-0038 | ✓ UNCHANGED |
| US-0068 / DEC-0060 | ✓ UNCHANGED |
| US-0096 / DEC-0082 | ✓ UNCHANGED |
| BUG-0007 | ✓ UNCHANGED |

### Sprint seeds preview (12 tasks within SPRINT_MAX_TASKS=12)

T-anch + T-001..T-011. /sprint-plan may merge or split within the 12-task budget.

### Risks finalized (R1..R8)

R1 (MEDIUM) backward-compat; R2 (MEDIUM) security gate bypass; R3 (LOW) repair ledger growth; R4 (MEDIUM) operator confusion; R5 (LOW-MEDIUM) preset-expansion precedence; R6 (LOW) compose-do-not-amend drift; R7 (LOW) matrix validator; R8 (LOW-MEDIUM) breadcrumb granularity.

### Decision gate + next scheduled phase

- `decision_gate=false` (no DECISION_GATE; companion DEC-0119 authored Accepted; approach A1 locked; 12 sprint seeds; risks R1..R8 finalized; DC clean; compose 6/6)
- `next_scheduled_phase=/sprint-plan` (role=tech-lead; third canonical phase of plan macro per ultra_lean)
- `stop_condition=STOP after architecture completes; hand off via artifacts only to /sprint-plan in fresh tech-lead subagent (BUG-0006)`

---

## Research handoff — US-0119 / (pending) / auto-20260705-us0119-intake

**Phase completed**: research
**Phase role**: tech-lead
**Story**: US-0119 Autonomous-autonomy presets and configurable hard-stop relaxation
**Verdict**: PASS (10/10 open questions closed LOCKED; architecture seeds proposed)
**Timestamp**: 2026-07-05T22:30:00Z (UTC)
**Fresh context marker**: tl-US0119-research-20260705T223000Z-fresh
**Runtime proof**: rp-auto-20260705-us0119-research-techlead-20260705T223000Z-US-0119 (proof_hash=f347aafdf2117b0b0fbc505d88c08322553a778d173f50b3d000418aeccc1eb2, proof_ttl=2026-07-05T23:30:00Z)
**Delivery mode**: ultra_lean (plan macro = research+architecture+sprint-plan merged)
**Macro phase**: plan (research — first canonical phase)

### Summary

AUTONOMY_PRESET={none|balanced|full} scratchpad flag deterministically expands into twelve per-feature autonomy flags (additive consumers; no existing semantics change). AUTONOMY_STOP_POLICY={block|auto_repair_then_block|auto_repair_then_skip} classifies every fail-closed reason code as `security_hard` (never auto-resolved) or `autonomy_resolvable` (bounded auto-repair with ledger cap). Authority manifest `docs/engineering/autonomy-stop-matrix.md` + YAML companion `scripts/data/autonomy_stop_matrix.yaml` + validator `scripts/validate_autonomy_stop_matrix.py`. Bounded auto-repair ledger `handoffs/autonomy_repair_ledger/<orchestrator_run_id>.jsonl`. `autonomy_relaxed` breadcrumb in `docs/engineering/state.md`. Security-hard gates NEVER softened. Backward-compatible default (`AUTONOMY_PRESET=none` = byte-identical pre-US-0119). Compose (read-only) with US-0092/US-0095/US-0056/US-0068/US-0096/BUG-0007.

### Closed questions Q1..Q10 (10/10 LOCKED)

**Q1** (reason-code enumeration): 22 `autonomy_resolvable` reason codes finalized. `/auto` 13 (ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS, STATE_TIMESTAMP_NON_MONOTONIC, ARTIFACT_HOT_SURFACE_OVERSIZE, BLOCK_RETRY_CAP_EXHAUSTED, STATE_PHASE_AMBIGUOUS, RESUME_BRIEF_MISSING, PLAN_FIDELITY_VIOLATION, ISOLATION_EVIDENCE_INVALID, MEGA_QUICK_ARCHITECTURE_REQUIRED, EXEC_BULK_MAX_ITEMS_REACHED, EXEC_TEAM_SCOPE_BLOCKED, EXEC_TEAM_SCOPE_SKIPPED, BRANCH_NOT_ALLOWLISTED); `/intake` 4 (INTAKE_REQUIRED_PACK_INCOMPLETE, INTAKE_REQUIRED_TOPIC_MISSING malformed, INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED ref missing, INTAKE_PLAN_COVERAGE_MISSING); `/execute` 2 (DOC_SECTION_BUDGET_EXCEEDED, DOC_TEMPLATE_PARITY_FAIL); `/qa` 1 (TEST_COMMAND_MISSING); `/release` 2 (RELEASE_PUBLISH_MODE not auto, DEV_ENV_PROFILE_MISSING). LOCKED.

**Q2** (auto_repair_kind taxonomy): 9 values — reorder_anchors, fix_timestamp, truncate_hot_surface, reset_retry_counter, disambiguate_state, auto_refresh_brief, approve_plan_deviation, regenerate_isolation_evidence, skip_confirmation_gate. Each reason code maps 1:1 to auto_repair_kind (or n/a for security_hard). LOCKED.

**Q3** (matrix cap defaults): Uniform cap = 3 per (orchestrator_run_id, reason_code). Override optional via AUTONOMY_REPAIR_CAP_OVERRIDE. LOCKED.

**Q4** (RUNTIME_PROOF_KIND=lightweight TTL): Same TTL = 3600s as strict_hash. Only attestation kind changes (counter+timestamp, not SHA-256). LOCKED.

**Q5** (SOVEREIGN_DRAIN_RISK_THRESHOLD): Three-tier: low (docs/tests only), medium (src single-component), high (src multi-component OR companion DEC). SOVEREIGN_DRAIN_AUTO_ACCEPT=1 auto-accepts only low. LOCKED.

**Q6** (RELEASE_PUBLISH_AUTO_CONFIRM): Allowlist-only via RELEASE_TARGETS_ALLOWLIST (new scratchpad key). Previously-confirmed targets NOT auto-confirmed. LOCKED.

**Q7** (INTAKE_MINIMAL_PACK threshold): MAX_US_ID >= US-0100 AND STACK_KNOWN = true. LOCKED.

**Q8** (matrix validator): Explicit YAML manifest (scripts/data/autonomy_stop_matrix.yaml), not grep-based. Validator checks (a) no orphan code in scripts (b) security_hard — auto_repair_kind=n/a (c) autonomy_resolvable — finite cap (d) every command-repo reason code is in YAML. LOCKED.

**Q9** (AUTONOMY_REPAIR_CAP_EXHAUSTED): NEW code (not extension of BLOCK_RETRY_CAP_EXHAUSTED). Separate concerns — BLOCK_RETRY is operator/story-level; AUTONOMY_REPAIR is autonomy/run-level. LOCKED.

**Q10** (breadcrumb format): One-line per soft-stop (not aggregated per-phase). Format: `autonomy_relaxed: <reason_code> -> <auto_repair_kind>` at phase boundary. LOCKED.

### Architecture seeds (12 tasks within SPRINT_MAX_TASKS=12)

T-anch, T-001 (autonomy_preset_lib.py), T-002 (scratchpad flags), T-003 (stop-matrix md+yaml+validator), T-004 (wire 12 flags into consumers), T-005 (repair ledger), T-006 (breadcrumb in state.md), T-007 (contract tests 10 markers), T-008 (README 7th sub-block + template parity), T-009 (runbook + commands anchors), T-010 (installer manifest), T-011 (regression baseline).

### Companion DEC decision

**DEC-0119 required** (to be authored in `/architecture`). Locks: (a) none|balanced|full 3-tier preset (alternatives 2-tier/4-tier rejected), (b) security_hard|autonomy_resolvable 2-tier (soft_warn rejected), (c) 12 flags additive consumers only (test_us0119_preset_expansion_uses_known_keys_only), (d) AUTONOMY_PRESET=none byte-identical default, (e) uniform cap=3 (AUTONOMY_REPAIR_CAP_OVERRIDE provides flexibility). Mirrors DEC-0078 / DEC-0082 precedent.

### Risks finalized (R1..R8 — 8 risks)

R1 backward-compat; R2 security gate bypass; R3 repair ledger growth; R4 operator confusion; R5 preset-expansion precedence (explicit > preset > defaults); R6 compose-do-not-amend drift; R7 matrix validator YAML-not-grep (Q8); R8 breadcrumb one-line-not-aggregate (Q10).

### Compose, do not amend (verified 6/6)

US-0092 —, US-0095 —, US-0056 —, US-0068 —, US-0096 —, BUG-0007 —

### DC check

grep "^# US-0119" docs/engineering/architecture.md -> no matches (expected; T-anch resolves in /architecture).

### AC baselines

- validate_readme_feature_coverage.py PASS
- pytest tests/scratchpad_example_parity_test.py 4 passed

### Handoff

**Next phase**: `/architecture` (role=tech-lead; second canonical phase of plan macro per ultra_lean)
**Stop condition**: STOP after research completes; hand off via artifacts only to /architecture in fresh tech-lead subagent (BUG-0006)
**Artifacts produced**: docs/engineering/research.md R-0107 full entry; docs/engineering/state.md research checkpoint; handoffs/po_to_tl.md research handoff prepended

---


