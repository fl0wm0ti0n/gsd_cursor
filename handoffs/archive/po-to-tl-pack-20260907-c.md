# PO to TL archive pack (2026-09-07)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 10
- First archived heading: `## US-0119 Â— Autonomous-autonomy presets (INTAKE ? DISCOVERY handoff)`
- Last archived heading: `## US-0119 Â— Autonomous-autonomy presets (INTAKE ? DISCOVERY handoff)`
- Verification tuple (mandatory):
  - archived_body_lines=62
  - retained_body_lines=603

---

## US-0119 Â— Autonomous-autonomy presets (INTAKE ? DISCOVERY handoff)

- **Story**: `docs/product/backlog.md` `## US-0119 ? Autonomous-autonomy presets and configurable hard-stop relaxation`
- **Acceptance**: `docs/product/acceptance.md` US-0119 row (13 ACs, OPEN)
- **Intake evidence**: `handoffs/intake_evidence/US-0119-intake-20260705.json` (first-intake-pack, all 8 topics covered, coverage_complete=true, plan_area_id=`autonomy-presets`)
- **Phase**: discovery (intake complete; next is discovery)
- **Verdict**: INTAKE PASS; no DECISION_GATE
- `orchestrator_run_id=auto-20260705-us0119-intake`, `intake_run_id=auto-20260705-us0119-intake`
- **Status**: OPEN per US-0045. **Next**: `/discovery` (fresh PO for US-0119).

### Summary

`AUTONOMY_PRESET={none|balanced|full}` scratchpad flag that deterministically expands into twelve per-feature autonomy flags (additive consumers on existing surfaces; no existing consumer semantics change). `AUTONOMY_STOP_POLICY={block|auto_repair_then_block|auto_repair_then_skip}` flag that classifies every fail-closed reason code as `security_hard` (never auto-resolved) or `autonomy_resolvable` (bounded auto-repair with ledger cap). Authority manifest `docs/engineering/autonomy-stop-matrix.md` + YAML companion `scripts/data/autonomy_stop_matrix.yaml` + validator `scripts/validate_autonomy_stop_matrix.py`. Bounded auto-repair ledger at `handoffs/autonomy_repair_ledger/<orchestrator_run_id>.jsonl`. `autonomy_relaxed` breadcrumb in `docs/engineering/state.md` at every phase boundary where a stop code was softened. Security-hard gates NEVER softened (PHASE_CONTEXT_ISOLATION_*, RUNTIME_PROOF_*, PHASE_ROLE_*, PHASE_OWNERSHIP_VIOLATION, INTAKE_REQUIRED_TOPIC_MISSING, INTAKE_PERSISTENCE_BLOCKED, AUTO_SCHEDULER_CONFLICT, RESUME_BRIEF_STALE (when RESUME_BRIEF_AUTO_REFRESH != 1), SECURITY_REVIEW critical findings). Backward-compatible default (`AUTONOMY_PRESET=none` = byte-identical pre-US-0119). Compose (read-only) with US-0092/US-0095/US-0056/US-0068/US-0096/BUG-0007: preset layer is additive only, never rewrites semantics.

### Companion DEC = DEC-0119 (to be authored in `/architecture`)

Required ? Accepted; authored in `/architecture` phase. Mirrors DEC-0078 / DEC-0052 precedent.

### Risks (locked at architecture)

- R1 backward-compat regression (MEDIUM Â— test_us0119_preset_none_is_noop)
- R2 security gate bypass matrix (MEDIUM Â— test_us0119_security_hard_gates_never_auto_repaired)
- R3 repair ledger growth (LOW Â— per-run cap + gitignore)
- R4 operator confusion (MEDIUM Â— breadcrumb + ledger)
- R5 preset-expansion vs explicit precedence (LOW-MEDIUM Â— LOCKED: explicit per-flag > preset > defaults)

### Compose, do not amend

- US-0092/US-0095 (full-autonomy + native chain) Â— unchanged
- US-0056 (strict runtime proof) Â— unchanged; `RUNTIME_PROOF_KIND=lightweight` is opt-in lighter attestation inside autonomy mode
- US-0068 (mandatory intake packs) Â— unchanged; US-0078 / DEC-0060 evidence gate NEVER bypassed
- US-0096 (delivery modes) Â— unchanged
- BUG-0007 (truthfulness) Â— unchanged; `INTAKE_ASSUME_STACK_CONTEXT=1` auto-derives with assumption_confirmation_ref contract preserved

### Test markers (10 locked)

- `test_us0119_preset_none_is_noop`
- `test_us0119_preset_balanced_expansion`
- `test_us0119_preset_full_expansion`
- `test_us0119_explicit_flag_overrides_preset`
- `test_us0119_preset_expansion_uses_known_keys_only`
- `test_us0119_matrix_validator_passes`
- `test_us0119_security_hard_gates_never_auto_repaired`
- `test_us0119_stop_policy_affects_repair_dispatch`
- `test_us0119_repair_ledger_cap_escalates`
- `test_us0119_matrix_no_orphan_codes`

### Open questions for /discovery

- Q1: exact list of `autonomy_resolvable` reason codes from /auto /intake /execute /qa /release
- Q2: per-reason-code `auto_repair_kind` taxonomy
- Q3: matrix cap defaults Â— 3 or per-`(reason)` tuning?
- Q4: `RUNTIME_PROOF_KIND=lightweight` Â— proof_ttl reduced? or same TTL as strict_hash?
- Q5: `SOVEREIGN_DRAIN_RISK_THRESHOLD` Â— `low|medium|high` enum with what criteria per tier?
- Q6: `RELEASE_PUBLISH_AUTO_CONFIRM` Â— is "known targets" = allowlist only, or includes previously-confirmed?
- Q7: `INTAKE_MINIMAL_PACK` Â— what is the threshold for "established project" (max US-xxxx id + stack known)?
- Q8: matrix validator Â— should it grep `.cursor/commands/*.md` or maintain an explicit reason-code manifest?
- Q9: `AUTONOMY_REPAIR_CAP_EXHAUSTED` Â— new stop code, or extension of existing `BLOCK_RETRY_CAP_EXHAUSTED`?
- Q10: breadcrumb format in state.md Â— one-line per soft-stop, or aggregated per phase?

---

