# Sprint S0120 — Sprint Plan (US-0120)

## Metadata

| Field | Value |
|---|---|
| story_id | US-0120 |
| story_title | Separate /closure phase after /release with exclusive Story Closure responsibility |
| sprint_id | S0120 |
| delivery_mode | ultra_lean |
| macro_phase | build+verify (next — after plan macro completes) |
| current_phase | sprint-plan (terminal phase of plan macro) |
| approach | A1 locked (dedicated /closure phase, qe role, orchestrator rg verification) |
| companion_DEC | none (scoped edits to DEC-0052 + DEC-0082 directly, per R-0108) |
| orchestrator_run_id | manual-20260707-us0120 |
| fresh_context_marker | tl-US0120-sprint-plan-20260707T215500Z-fresh |
| timestamp | 2026-07-07T21:55:00Z (UTC) |
| verdict | PASS |
| decision_gate | false |
| SPRINT_MAX_TASKS | 12 |
| SPRINT_AUTO_SPLIT | 1 |
| task_count | 10 (within SPRINT_MAX_TASKS=12; no split needed) |
| plan-verify | merged into qa per ultra_lean (qa creates plan-verify.json within build+verify) |

## Scope summary

Extract Story Closure (backlog `OPEN`→`DONE` + acceptance `[ ]`→`[x]` + state.md closure checkpoint + closure-verification.md artifact) from `/release` step 10–12 into a dedicated `/closure` phase with exclusive `qe` role ownership. Ship macro becomes `[release, closure, refresh-context]` (3 phases). Governance-only change: no new code surfaces beyond schema validator + contract tests. Compose 6/6 UNCHANGED (US-0043/US-0045/US-0040/US-0048/US-0056/US-0096).

## Phase role matrix (per DEC-0051 / US-0069)

| Phase | Role | Notes |
|---|---|---|
| execute | dev (fresh per BUG-0006) | first phase of build+verify macro |
| qa | qa | verifies /execute outputs; creates plan-verify.json (merged per ultra_lean) |
| verify-work | qa | final verify gate before /release |
| release | release | release artifacts only (steps 10-12 removed) |
| closure | qe (default) / curator (AUTO_ROLE_CLOSURE override) | NEW — exclusive Story Closure |
| refresh-context | curator | segment closeout |

## Task list (10 tasks — T-anch + T-001..T-010)

### T-anch (NO-OP / verification)

- **Description**: Verify architectural anchor + compose-guard integrity. `# US-0120` H1 anchor at `docs/engineering/architecture.md` L2125 already added in `/architecture` phase (per R-0105 Q-2 LOCKED). No execute-phase write to architecture.md for this anchor. Verify DEC-0052/DEC-0082 scoped-edit contract exists. Verify `.cursor/commands/closure.md` does NOT yet exist. Verify `## Story closure (US-0120)` NOT YET in runbook.md.
- **File paths (read-only)**: `docs/engineering/architecture.md` L2125, `decisions/DEC-0052.md`, `decisions/DEC-0082.md`, `docs/engineering/runbook.md`, `.cursor/commands/closure.md` (absence), `template/.cursor/commands/closure.md` (absence)
- **Acceptance criteria reference**: AC-11 (documentation baseline), AC-12 (compose guards UNCHANGED baseline)
- **Dependencies**: None
- **Estimated complexity**: LOW (read-only verification)
- **Risk**: LOW
- **Execution mode**: NO-OP / verification only; no file mutation

### T-001 (NEW `.cursor/commands/closure.md` — active)

- **Description**: Author the /closure command file (active). Structure per architecture.md `## US-0120` Phase definition: Subagents (qe, fresh per BUG-0006); Execution model (fresh qe subagent context); Isolation evidence write requirement (US-0048 / DEC-0029, phase_id=closure, role=qe); Inputs (narrow-read US-0053/US-0096 Tranche A); Outputs (4 mandatory: backlog.md flip, acceptance.md check, state.md closure checkpoint, closure-verification.md); Stop conditions; Input prerequisites (release_queue.md status=released + release-notes EXISTS + qa-findings EXISTS — fail-gated CLOSURE_RELEASE_EVIDENCE_MISSING); Backlog reconciliation contract (US-0043/DEC-0021); Canonical status source (US-0045/DEC-0025); Orchestrator post-closure verification protocol (rg checks); Fail-safe reason codes (CLOSURE_RELEASE_EVIDENCE_MISSING, CLOSURE_VERIFICATION_FAILED, CANONICAL_STATUS_CONFLICT, BACKLOG_STATUS_DRIFT, PHASE_OWNERSHIP_VIOLATION, PHASE_OVERRIDE_EVIDENCE_MISSING); Artifact ordering contract (backlog.md → acceptance.md → state.md → closure-verification.md); Cross-phase ownership guard (closure owns status flip + acceptance check + state checkpoint + closure-verification.md; does NOT touch release artifacts).
- **File paths (create)**: `.cursor/commands/closure.md`
- **Acceptance criteria reference**: AC-1 (closure command file active), AC-5 (release step 10-12 contract — closure takes over), AC-7 (closure isolation evidence contract), AC-8 (closure runtime proof contract), AC-10 (drain hook backward compat contract)
- **Dependencies**: T-anch (VERIFIED compose guard anchors exist)
- **Estimated complexity**: MEDIUM
- **Risk**: MEDIUM (command file design is the core artifact)
- **Scope**: governance-only (no new binary/script logic in T-001; script in T-006)

### T-002 (NEW `template/.cursor/commands/closure.md` — byte-identical mirror)

- **Description**: Copy `.cursor/commands/closure.md` to `template/.cursor/commands/closure.md`. Verify byte-identical (PARITY_OK). Extend `scripts/check_intake_template_parity.py` COMMAND_PAIRS with closure entry (scope=closure-phase).
- **File paths (create/edit)**: `template/.cursor/commands/closure.md` (NEW, byte-identical); `scripts/check_intake_template_parity.py` (add closure scope)
- **Acceptance criteria reference**: AC-1 (template mirror), AC-12 (compose guards UNCHANGED — template parity does not touch compose surfaces)
- **Dependencies**: T-001 (DONE)
- **Estimated complexity**: LOW (copy + parity checker extension)
- **Risk**: LOW

### T-003 (DEC-0052 phase→role matrix + AUTO_ROLE_CLOSURE scratchpad key)

- **Description**: Scoped ADDITIVE edit to `decisions/DEC-0052.md`: (i) add `closure | qe | AUTO_ROLE_CLOSURE scratchpad override to curator allowed` row to §1 canonical phase→role matrix; (ii) add `AUTO_ROLE_CLOSURE` row to §2 override contract table (values: qe, curator; default: qe; curator must not write qa-owned surfaces); (iii) add `closure` row to §3 preflight capability gate (capability: role:qe or override; fail-closed: PHASE_CAPABILITY_MISSING). Existing 12 phase→role mappings UNTOUCHED. Add AUTO_ROLE_CLOSURE scratchpad key block to `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md`.
- **File paths (edit)**: `decisions/DEC-0052.md`, `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`
- **Acceptance criteria reference**: AC-2 (DEC-0052 phase→role matrix update), AC-12 (compose guards UNCHANGED — DEC-0052 is the target of scoped edit, not a compose-guard surface)
- **Dependencies**: T-anch (VERIFIED DEC-0052 matrix exists)
- **Estimated complexity**: MEDIUM
- **Risk**: MEDIUM (scoped ADDITIVE edit — strictly no row deletions/renumber of existing 12)

### T-004 (DEC-0082 ship macro + auto.md phase plan + closure spawn)

- **Description**: Scoped edit to `decisions/DEC-0082.md`: ship macro `[release, refresh-context]` (2) → `[release, closure, refresh-context]` (3); other macro definitions UNTOUCHED. Update `.cursor/commands/auto.md` + `template/.cursor/commands/auto.md`: add closure to phase plan arrays in all 3 delivery modes (standard, ultra_lean, mega_quick); after `/release` completes, orchestrator spawn contract describes closure subagent spawn (fresh per BUG-0006; phase_id=closure, role=qe/curator fallback, story_id, sprint_id, orchestrator_run_id, fresh_context_marker). Add AUTO_ROLE_CLOSURE scratchpad pointer.
- **File paths (edit)**: `decisions/DEC-0082.md`, `.cursor/commands/auto.md`, `template/.cursor/commands/auto.md`
- **Acceptance criteria reference**: AC-3 (DEC-0082 ship macro update), AC-4 (/auto orchestration wiring)
- **Dependencies**: T-anch (VERIFIED DEC-0082 table exists)
- **Estimated complexity**: MEDIUM
- **Risk**: MEDIUM (3 delivery modes + 2 auto.md files must stay byte-identical)

### T-005 (release.md step 10-12 removal + renumbering — active + template)

- **Description**: `.cursor/commands/release.md`: remove steps 10 (Backlog reconciliation US-0043/DEC-0021), 11 (Derived status views reconciliation US-0045/DEC-0025), 12 (Normalization report). Insert new step 10 pointer: "Backlog reconciliation is now handled by the dedicated `/closure` phase — see `.cursor/commands/closure.md`." Old step 13 → new step 10, old step 14 → new step 11, ..., sequential renumbering no gaps. Repeat byte-identical in `template/.cursor/commands/release.md`. Release subagent post-US-0120 focuses on release artifacts only (no status flip, no acceptance check, no state checkpoint).
- **File paths (edit)**: `.cursor/commands/release.md`, `template/.cursor/commands/release.md`
- **Acceptance criteria reference**: AC-5 (release step 10-12 removal)
- **Dependencies**: T-001 (DONE — `/closure` command must exist for pointer target)
- **Estimated complexity**: MEDIUM (sequential renumbering across ~8 steps; byte-identical across 2 files)
- **Risk**: LOW (R5 ACCEPTED; deterministic renumber)

### T-006 (NEW `scripts/validate_closure_verification.py`)

- **Description**: Pure-stdlib validator for `sprints/Sxxxx/closure-verification.md` schema (per architecture.md L2169-L2189). Required fields: `story_id` (US-xxxx), `closure_date` (ISO-8601 UTC), `closure_role` (qe|curator), `pre_closure_status` (OPEN), `post_closure_status` (DONE), `release_evidence_refs[]` (array of paths), `isolation_evidence{}` (object per US-0048), `runtime_proof{}` (object per US-0056/DEC-0038). Optional fields allowed: `normalization_notes`, `backward_compat_note`. Schema additive-extensible: validator only checks required fields. CLI: `python scripts/validate_closure_verification.py --file sprints/Sxxxx/closure-verification.md`. Exit codes: 0=valid, 1=invalid with deterministic reason code `CLOSURE_VERIFICATION_SCHEMA_INVALID`.
- **File paths (create)**: `scripts/validate_closure_verification.py`
- **Acceptance criteria reference**: AC-6 (closure-verification.md schema validator), AC-8 (runtime proof contract enforced by validator)
- **Dependencies**: T-001 (DONE — closure.md command defines the schema contract), T-002 (DONE — template parity context), T-003 (DONE — role=qe|curator contract from DEC-0052)
- **Estimated complexity**: MEDIUM
- **Risk**: LOW (pure stdlib; schema per architecture.md Q6/Q7 LOCKED)

### T-007 (closure.md isolation evidence + runtime proof contract sections)

- **Description**: Extend `.cursor/commands/closure.md` with concrete per-phase contracts: (i) Isolation evidence contract — /closure appends closure checkpoint to `docs/engineering/state.md` with `{phase_id: closure, role: qe, fresh_context_marker, timestamp, evidence_ref: sprints/Sxxxx/closure-verification.md}` per US-0048/DEC-0029; (ii) Runtime proof contract — /closure computes sorted-key JSON payload `{delivery_mode, macro_phase:ship, orchestrator_run_id, phase_id:closure, proof_issued_at, proof_ttl_seconds:3600, role:qe, runtime_proof_id, sprint_id, story_id}` per DEC-0038; SHA-256 → proof_hash; proof_ttl=issued_at+3600s; emits `RUNTIME_PROOF_MISSING` / `RUNTIME_PROOF_INVALID` / `RUNTIME_PROOF_REUSED` / `RUNTIME_PROOF_STALE` / `RUNTIME_PROOF_AMBIGUOUS_LINK` fail codes.
- **File paths (edit)**: `.cursor/commands/closure.md`, `template/.cursor/commands/closure.md` (byte-identical)
- **Acceptance criteria reference**: AC-7 (closure isolation evidence), AC-8 (closure runtime proof)
- **Dependencies**: T-001 (DONE), T-006 (DONE — validator schema contract)
- **Estimated complexity**: MEDIUM
- **Risk**: LOW

### T-008 (NEW `tests/us0120_closure_phase_test.py` — 10 markers)

- **Description**: 10 contract test markers in `tests/us0120_closure_phase_test.py`:
   1. `test_us0120_closure_command_file_exists_active` — AC-1: `.cursor/commands/closure.md` EXISTS
   2. `test_us0120_closure_command_file_exists_template` — AC-1: `template/.cursor/commands/closure.md` EXISTS
   3. `test_us0120_closure_command_file_parity` — AC-1: active + template byte-identical (PARITY_OK)
   4. `test_us0120_dec_0052_phase_role_matrix_includes_closure` — AC-2: DEC-0052 includes closure|qe row
   5. `test_us0120_dec_0082_ship_macro_includes_closure` — AC-3: DEC-0082 ship=[release,closure,refresh-context]
   6. `test_us0120_auto_phase_plan_includes_closure` — AC-4: /auto phase plan includes closure after release
   7. `test_us0120_release_md_steps_10_12_removed` — AC-5: release.md does NOT contain step 10-12 backup (reconciliation)
   8. `test_us0120_closure_verification_schema_defined` — AC-6: closure-verification.md schema + validator exists
   9. `test_us0120_compose_guards_unchanged` — AC-12: US-0043/US-0045/US-0040/US-0048/US-0056/US-0096 untouched
   10. `test_us0120_backward_compat_drain_hook` — AC-10: drain hook detects in-flight stories needing closure

  Surjective AC coverage: markers 1-3→AC-1, 4→AC-2, 5→AC-3, 6→AC-4, 7→AC-5, 8→AC-6, 9→AC-12, 10→AC-10. AC-7/AC-8/AC-9/AC-11 covered indirectly by markers 1+8/4/6.
- **File paths (create)**: `tests/us0120_closure_phase_test.py`
- **Acceptance criteria reference**: AC-9 (contract tests)
- **Dependencies**: T-001..T-007 (all DONE — tests assert the outputs of T-001..T-007)
- **Estimated complexity**: MEDIUM
- **Risk**: MEDIUM (tests are the contract enforcement)

### T-009 (drain hook detection + installer manifest rows)

- **Description**: Drain hook detection for in-flight stories at US-0120 ship boundary (per architecture.md Q4 / R2 mitigation): 3-signal check in `/auto` drain-advance — (i) release_queue row status=released, (ii) backlog.md Status:OPEN, (iii) acceptance.md `[ ]` unchecked → closure SKIPPED → post-US-0120 spawn `/closure` backfill; pre-US-0120 `CLOSURE_LEGACY_DRIFT` (manual reconciliation; no retroactive closure-verification.md per R8 ACCEPTED). SKIP `Status: DONE` stories. Installer manifest rows: extend `docs/engineering/context/installer-owned-paths.manifest` `[install_include_paths]` for `scripts/validate_closure_verification.py` + `.cursor/commands/closure.md` (active) + `template/.cursor/commands/closure.md` (template). Triple-installer parity (PS1/Bash/Python) documented in architecture.md.
- **File paths (edit/create)**: `docs/engineering/context/installer-owned-paths.manifest` (extend); drain-hook contract documented in `.cursor/commands/closure.md` (already in T-001/T-007)
- **Acceptance criteria reference**: AC-10 (drain hook backward compat)
- **Dependencies**: T-001 (DONE), T-002 (DONE), T-006 (DONE), T-008 (DONE — drain hook test asserts T-009 contract)
- **Estimated complexity**: LOW-MEDIUM
- **Risk**: LOW (R2 ACCEPTED, R7 ACCEPTED)

### T-010 (runbook `## Story closure (US-0120)` h2 + documentation)

- **Description**: Add `## Story closure (US-0120)` h2 to `docs/engineering/runbook.md`: overview of `/closure` phase operator recipe; when to run (after `/release` PASS, before `/refresh-context`); how to verify (state.md closure checkpoint + runtime proof); how to manually trigger (for in-flight stories spawn `/closure` subagent); troubleshooting (CLOSURE_RELEASE_EVIDENCE_MISSING, CLOSURE_VERIFICATION_FAILED, CANONICAL_STATUS_CONFLICT, BACKLOG_STATUS_DRIFT). architecture.md `# US-0120` H1 section already added in `/architecture` phase (L2125 — T-010 is NO-OP on architecture.md; verifies the section exists).
- **File paths (edit)**: `docs/engineering/runbook.md`
- **File paths (verify read-only)**: `docs/engineering/architecture.md` L2125 (confirm `# US-0120` present; no execute-mutation)
- **Acceptance criteria reference**: AC-11 (documentation complete), AC-12 (compose guards UNCHANGED — architecture.md H1 is NOT a compose-guard mutation)
- **Dependencies**: T-anch (VERIFIED architecture.md anchor), T-001..T-009 (DONE — runbook summarizes execute outputs)
- **Estimated complexity**: LOW (single h2 append)
- **Risk**: LOW

## Task dependency graph

```
[T-anch] ──► [T-001] ──► [T-002]
          │            └─► [T-005]
          │            └─► [T-006] ──► [T-007]
          │            └─► [T-003]
          │            └─► [T-004]
          │                        │
          └──────────────────► [T-006] (depends on T-003 as well)
                               │
                               ▼
                           [T-008] (needs T-001..T-007 DONE)
                               │
                               ▼
                           [T-009] (depends on T-001, T-002, T-006, T-008)
                               │
                               ▼
                           [T-010] (depends on T-anch, T-001..T-009)
                               │
                               ▼
                       [integration verification]
                       (all 10 tests pass; PARITY_OK proofs; compose 6/6 UNCHANGED)
```

**Parallelism after T-anch**:
- Tier 1 (parallel): T-001, T-003, T-004
- Tier 2 (parallel, after T-001): T-002, T-005, T-006
- Tier 3 (after T-001 + T-003): T-006 (already blocked by T-003 for role contract)
- Tier 4 (after T-001 + T-006): T-007
- Tier 5 (after T-001..T-007): T-008
- Tier 6 (after T-001, T-002, T-006, T-008): T-009
- Tier 7 (final): T-010 (after all T-001..T-009)

**Execution order (deterministic)**: T-anch → {T-001, T-003, T-004 parallel} → {T-002, T-005, T-006 parallel} → T-007 → T-008 → T-009 → T-010 → integration verification.

## Integration verification (final — after T-010)

After all 10 tasks complete, run integration verification:

1. **Test gate**: `python -m pytest tests/us0120_closure_phase_test.py -v` → 10/10 PASS
2. **Parity gates**:
   - `.cursor/commands/closure.md` ↔ `template/.cursor/commands/closure.md` PARITY_OK
   - `.cursor/commands/release.md` ↔ `template/.cursor/commands/release.md` PARITY_OK
   - `check_intake_template_parity.py --scope=closure-phase` PASS
3. **Compose gates**: 6/6 UNCHANGED (US-0043/US-0045/US-0040/US-0048/US-0056/US-0096)
4. **Schema gate**: `scripts/validate_closure_verification.py --self-test` PASS
5. **Drain hook smoke**: 3-signal check logic asserted by `test_us0120_backward_compat_drain_hook`

## Execute phase role (per DEC-0051 / US-0069)

| Phase | Role | Isolation |
|---|---|---|
| /execute | **dev** | fresh subagent per BUG-0006; isolation evidence {phase_id:execute, role:dev} |
| /qa | **qa** | fresh qa subagent; isolation evidence {phase_id:qa, role:qa}; creates plan-verify.json (merged per ultra_lean) |
| /verify-work | **qa** | fresh qa subagent; isolation evidence {phase_id:verify-work, role:qa} |
| /release | **release** | fresh release subagent; isolation evidence {phase_id:release, role:release} |
| /closure | **qe** | fresh qe/curator subagent; isolation evidence {phase_id:closure, role:qe} |
| /refresh-context | **curator** | fresh curator subagent |

## Isolation evidence (US-0048 / DEC-0029)

| Field | Value |
|---|---|
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0120 |
| sprint_id | S0120 |
| orchestrator_run_id | manual-20260707-us0120 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| fresh_context_marker | tl-US0120-sprint-plan-20260707T215500Z-fresh |
| timestamp | 2026-07-07T21:55:00Z (UTC) |
| evidence_ref | sprints/S0120/sprint-plan.md (this file), sprints/S0120/tasks.md (per-task file manifest), docs/engineering/state.md (sprint-plan checkpoint appended), handoffs/po_to_tl.md (sprint-plan handoff prepended) |

Prior phase proof consumed: `rp-manual-20260707-us0120-architecture-tl-20260707T215000Z-US-0120` (proof_hash=6293266bfcdf3e6e668cf28a34d831e55cc05a17e5dea1fc8ee94b70ca67b99f).

## Runtime proof (DEC-0038)

| Field | Value |
|---|---|
| runtime_proof_id | rp-manual-20260707-us0120-sprint-plan-tl-20260707T215500Z-US-0120 |
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0120 |
| sprint_id | S0120 |
| orchestrator_run_id | manual-20260707-us0120 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| proof_issued_at | 2026-07-07T21:55:00Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-07-07T22:55:00Z (UTC) |
| proof_hash | a702bc1226d474ad9851db6a8e1e5fa89f48adb22a54fa60c5d5b59a447e27a (SHA-256) |
| canonical_payload (sorted-key JSON) | `{"delivery_mode":"ultra_lean","macro_phase":"plan","orchestrator_run_id":"manual-20260707-us0120","phase_id":"sprint-plan","proof_issued_at":"2026-07-07T21:55:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-manual-20260707-us0120-sprint-plan-tl-20260707T215500Z-US-0120","sprint_id":"S0120","story_id":"US-0120"}` |

## Decision gate

| Field | Value |
|---|---|
| decision_gate | false |
| stop_conditions_met | yes |
| missing_acceptance_criteria | none (12/12 ACs covered by 10 test markers) |
| compose_guards | 6/6 UNCHANGED (US-0043/US-0045/US-0040/US-0048/US-0056/US-0096) |
| dc_check | clean |
| task_count | 10 (within SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1 but no split needed) |
| risks_finalized | 8/8 ACCEPTED (R1..R8 from R-0108) |
| approach | A1 locked |
| Q | 10/10 LOCKED |
| plan-verify readiness | merged into qa per ultra_lean |
| sovereign_memory_note | assemble_sovereign_memory_digest(...) NOT called; no mistakes.jsonl write |

## Definition of done (sprint-plan)

- [x] 10 tasks enumerated (T-anch + T-001..T-010) — within SPRINT_MAX_TASKS=12
- [x] 12/12 ACs covered by test markers (surjective)
- [x] Task dependency graph documented
- [x] Execute phase role matrix documented (dev / qa / qe / curator)
- [x] Compose guards 6/6 UNCHANGED
- [x] Isolation evidence + runtime proof emitted
- [x] Sprint-plan checkpoint appended to `docs/engineering/state.md`
- [x] Sprint-plan handoff prepended to `handoffs/po_to_tl.md`
- [x] Drain-advance prepended to `handoffs/resume_brief.md`

## Next scheduled phase

| Field | Value |
|---|---|
| next_scheduled_phase | `/execute` (dev, first phase of build+verify macro per ultra_lean) |
| next_scheduled_role | dev |
| next_sprint_macro | build+verify |
| stop_condition | STOP after sprint-plan completes; hand off via artifacts only to /execute in fresh dev subagent per BUG-0006 |
| artifacts_written | sprints/S0120/sprint-plan.md (NEW), sprints/S0120/tasks.md (NEW), docs/engineering/state.md (sprint-plan checkpoint appended), handoffs/po_to_tl.md (sprint-plan handoff prepended), handoffs/resume_brief.md (drain-advance prepended) |
