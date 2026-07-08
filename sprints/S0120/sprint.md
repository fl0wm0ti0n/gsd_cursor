# Sprint S0120 — US-0120 Separate `/closure` phase after `/release`

## Metadata

- **Sprint ID**: S0120
- **Story**: US-0120
- **Delivery mode**: ultra_lean
- **Macro phase plan**: [spec, plan, build+verify, ship]
- **Current phase**: CLOSED (refresh-context complete — segment terminal)
- **Status**: RELEASED / CLOSED
- **Intake evidence**: handoffs/intake_evidence/US-0120-intake.json
- **Discovery locks**: sprints/S0120/discovery-locks.md
- **Companion DEC**: DEC-0120 (Required → Accepted; locks phase ownership, phase ordering, input prerequisites, output artifacts, compose relationships, template parity, orchestrator verification, backward compat)

## Scope

Extract Story Closure responsibilities (backlog status flip + acceptance checkbox + state checkpoint) from `/release` step 10-12 into a dedicated `/closure` phase with exclusive responsibility. Update lifecycle structure across all delivery modes (standard, ultra_lean, mega_quick). Wire orchestration in `/auto`. Produce closure isolation evidence + runtime proof per US-0048/US-0056. Define closure-verification.md artifact schema. Add contract tests. Update DEC-0052 (phase→role matrix) + DEC-0082 (delivery mode macro phases). Document in architecture.md + runbook.md + auto.md. Compose (read-only) with US-0043/US-0045/US-0040/US-0048/US-0056/US-0096.

## Acceptance criteria (12)

- **AC-1**: New `/closure` command file (active + template mirror)
- **AC-2**: Phase→role mapping update in DEC-0052 (add closure:qe)
- **AC-3**: Ultra-lean macro phase update in DEC-0082 (ship = release→closure→refresh-context)
- **AC-4**: Orchestration wiring in `/auto` (after release, before refresh-context)
- **AC-5**: Release.md step 10–12 removal (backlog reconciliation moved to /closure)
- **AC-6**: Closure verification artifact schema (`sprints/Sxxxx/closure-verification.md`)
- **AC-7**: Closure isolation evidence contract (per-phase per US-0048)
- **AC-8**: Closure runtime proof contract (per-phase per US-0056)
- **AC-9**: Contract tests (10+ markers in `tests/us0120_closure_phase_test.py`)
- **AC-10**: Backward compatibility for in-flight stories (drain hook detection)
- **AC-11**: Documentation (architecture runbook + auto.md phase wiring)
- **AC-12**: Compose, do not amend (6 surfaces read-only: US-0043/US-0045/US-0040/US-0048/US-0056/US-0096)

## Tasks

### T-anch (NO-OP / verification)

**Acceptance criteria**: AC-2, AC-3, AC-11
**Dependencies**: None
**Risk**: LOW
**Verification**: `rg "^## US-0096" docs/engineering/architecture.md` → match at L1684; verify DEC-0052 phase→role matrix exists; verify DEC-0082 delivery mode table exists; verify `## Story closure (US-0120)` NOT YET added to runbook.md

**Steps**:
1. Verify `## US-0096` anchor exists in architecture.md (compose guard)
2. Verify DEC-0052 phase→role matrix exists at `decisions/DEC-0052.md`
3. Verify DEC-0082 delivery mode table exists at `decisions/DEC-0082.md`
4. Verify runbook.md does NOT yet contain `## Story closure (US-0120)`
5. Verify `.cursor/commands/closure.md` does NOT yet exist
6. Record verification results

**Files to verify (read-only)**:
- `docs/engineering/architecture.md` (L1684)
- `decisions/DEC-0052.md` (phase→role matrix)
- `decisions/DEC-0082.md` (delivery mode table)
- `docs/engineering/runbook.md` (absence of ## Story closure heading)
- `.cursor/commands/closure.md` (absence)

**Output**: `sprints/S0120/t-anch-verification.md`

---

### T-001 (closure command file — active)

**Acceptance criteria**: AC-1, AC-5, AC-7, AC-8, AC-10
**Dependencies**: T-anch (VERIFIED)
**Risk**: MEDIUM

**Steps**:
1. Create `.cursor/commands/closure.md` with structure:
   - Subagents: qe (fresh per BUG-0006)
   - Execution model: fresh qe subagent context
   - Isolation evidence write requirement (US-0048 / DEC-0029)
   - Inputs (narrow-read per US-0053)
   - Outputs (closure-verification.md + state.md checkpoint + backlog.md flip + acceptance.md check)
   - Stop conditions (CLOSURE_RELEASE_EVIDENCE_MISSING)
   - Input prerequisites (release queue released + release notes EXISTS + qa-findings EXISTS)
   - Output artifacts contract (4 mandatory artifacts)
   - Backlog reconciliation contract (US-0043 / DEC-0021)
   - Canonical status source (US-0045 / DEC-0025)
   - Orchestrator post-closure verification contract (rg checks)
   - Fail-safe reason codes (CLOSURE_RELEASE_EVIDENCE_MISSING, CLOSURE_VERIFICATION_FAILED, CANONICAL_STATUS_CONFLICT, BACKLOG_STATUS_DRIFT)
   - Artifact ordering contract (backlog.md → acceptance.md → state.md → closure-verification.md)
   - Cross-phase ownership guard (closure owns status flip + acceptance check + state checkpoint + closure-verification.md; does NOT own release artifacts)

**Files to create**:
- `.cursor/commands/closure.md`

**Output**: `.cursor/commands/closure.md`

---

### T-002 (closure command file — template mirror)

**Acceptance criteria**: AC-1, AC-12
**Dependencies**: T-001 (DONE)
**Risk**: MEDIUM

**Steps**:
1. Copy `.cursor/commands/closure.md` to `template/.cursor/commands/closure.md`
2. Verify byte-identical (PARITY_OK)
3. Update `scripts/check_intake_template_parity.py` closure entry in COMMAND_PAIRS

**Files to create**:
- `template/.cursor/commands/closure.md` (byte-identical copy)

**Files to modify**:
- `scripts/check_intake_template_parity.py` (add closure to COMMAND_PAIRS)

**Output**: `template/.cursor/commands/closure.md` + checker update

---

### T-003 (DEC-0052 phase→role mapping update)

**Acceptance criteria**: AC-2, AC-12
**Dependencies**: T-anch (VERIFIED)
**Risk**: MEDIUM

**Steps**:
1. Read `decisions/DEC-0052.md`
2. Update phase→role matrix to add `closure:qe` (fallback `curator` when `qe` unavailable)
3. Add AUTO_ROLE_CLOSURE scratchpad key documentation
4. Verify compose guards UNCHANGED (US-0043/US-0045/US-0040/US-0048/US-0056/US-0096 not edited)

**Files to modify**:
- `decisions/DEC-0052.md` (add closure row to phase→role matrix + AUTO_ROLE_CLOSURE key)

**Output**: `decisions/DEC-0052.md` updated

---

### T-004 (DEC-0082 delivery mode macro phase update)

**Acceptance criteria**: AC-3, AC-12
**Dependencies**: T-anch (VERIFIED)
**Risk**: MEDIUM

**Steps**:
1. Read `decisions/DEC-0082.md`
2. Update delivery mode table: ship macro = [release, closure, refresh-context] (3 phases)
3. Update phase plan arrays:
   - standard: [..., execute, qa, verify-work, release, closure, refresh-context]
   - ultra_lean: [spec, plan, build+verify, ship] where ship = [release, closure, refresh-context]
   - mega_quick: [spec, build+verify, ship] where ship = [release, closure, refresh-context]
4. Verify compose guards UNCHANGED

**Files to modify**:
- `decisions/DEC-0082.md` (delivery mode table + phase plan arrays)

**Output**: `decisions/DEC-0082.md` updated

---

### T-005 (release.md step 10-12 removal)

**Acceptance criteria**: AC-5, AC-12
**Dependencies**: T-001 (DONE)
**Risk**: MEDIUM

**Steps**:
1. Read `.cursor/commands/release.md`
2. Remove steps 10-12:
   - Step 10: Backlog reconciliation (US-0043 / DEC-0021)
   - Step 11: Derived status views reconciliation (US-0045 / DEC-0025)
   - Step 12: Normalization report
3. Replace with pointer: "Backlog reconciliation is now handled by the dedicated `/closure` phase — see `.cursor/commands/closure.md`"
4. Update `template/.cursor/commands/release.md` (byte-identical)
5. Verify release subagent focuses on release artifacts only (no status flip, no acceptance check, no state checkpoint)

**Files to modify**:
- `.cursor/commands/release.md` (remove steps 10-12, add pointer)
- `template/.cursor/commands/release.md` (byte-identical)

**Output**: `.cursor/commands/release.md` + template mirror updated

---

### T-006 (orchestration wiring in `/auto`)

**Acceptance criteria**: AC-4, AC-12
**Dependencies**: T-001 (DONE), T-003 (DONE), T-004 (DONE)
**Risk**: MEDIUM

**Steps**:
1. Read `.cursor/commands/auto.md`
2. Add closure to phase plan arrays (all 3 delivery modes):
   - standard: insert `closure` after `release`, before `refresh-context`
   - ultra_lean: ship = [release, closure, refresh-context]
   - mega_quick: ship = [release, closure, refresh-context]
3. Add AUTO_ROLE_CLOSURE scratchpad key documentation
4. Add closure to native chain spawn sequence (after release, before refresh-context)
5. Verify compose guards UNCHANGED

**Files to modify**:
- `.cursor/commands/auto.md` (phase plan arrays + AUTO_ROLE_CLOSURE key + native chain)

**Output**: `.cursor/commands/auto.md` updated

---

### T-007 (closure-verification.md schema)

**Acceptance criteria**: AC-6, AC-8
**Dependencies**: T-001 (DONE)
**Risk**: LOW

**Steps**:
1. Define `closure-verification.md` schema:
   ```markdown
   # Closure Verification — US-xxxx / Sxxxx
   
   ## Story
   - story_id: US-xxxx
   - sprint_id: Sxxxx
   
   ## Closure execution
   - closure_date: ISO-8601 UTC timestamp
   - closure_role: qe (or curator if qe unavailable)
   - orchestrator_run_id: <orchestrator_run_id>
   - fresh_context_marker: <fresh_context_marker>
   
   ## Pre-closure status
   - backlog_status: OPEN (must be OPEN before closure)
   - acceptance_checked: [ ] (must be unchecked before closure)
   
   ## Release evidence consumed
   - release_queue_status: released (source: handoffs/release_queue.md)
   - release_notes_ref: handoffs/releases/Sxxxx-release-notes.md (EXISTS with PASS verdict)
   - qa_findings_ref: sprints/Sxxxx/qa-findings.md (EXISTS)
   - release_findings_ref: sprints/Sxxxx/release-findings.md (if present)
   - uat_ref: sprints/Sxxxx/uat.json + uat.md (if present)
   
   ## Post-closure status
   - backlog_status: DONE (must be DONE after closure)
   - acceptance_checked: [x] (must be checked after closure)
   
   ## Isolation evidence (US-0048 / DEC-0029)
   - phase_id: closure
   - role: qe (or curator)
   - fresh_context_marker: <marker>
   - timestamp: ISO-8601 UTC
   - evidence_ref: sprints/Sxxxx/closure-verification.md
   - state_checkpoint_ref: docs/engineering/state.md (closure checkpoint)
   
   ## Runtime proof (US-0056 / DEC-0038)
   - runtime_proof_id: <runtime_proof_id>
   - proof_hash: <proof_hash>
   - proof_ttl_seconds: 3600
   - proof_ttl: ISO-8601 UTC
   - payload: sorted-key JSON with {orchestrator_run_id, phase_id, role, runtime_proof_id, story_id, sprint_id}
   ```
2. Add schema documentation to closure.md Inputs section
3. Add validator contract (future task T-010)

**Output**: `sprints/S0120/closure-verification-schema.md` (schema documentation)

---

### T-008 (backward compat drain hook)

**Acceptance criteria**: AC-10
**Dependencies**: T-006 (DONE)
**Risk**: LOW

**Steps**:
1. Read `.cursor/commands/auto.md` drain-advance hook
2. Add closure detection logic:
   - After drain-advance selects a story, check if story is in /release or /closure
   - If /release completed but closure not performed (backlog OPEN + acceptance unchecked), spawn /closure
   - If /closure already performed (backlog DONE + acceptance checked), skip to /refresh-context
3. Add CLOSURE_RELEASE_EVIDENCE_MISSING fail-gate check to closure.md
4. Document in closure.md backward compat section

**Files to modify**:
- `.cursor/commands/auto.md` (drain hook closure detection)

**Output**: `.cursor/commands/auto.md` drain hook updated

---

### T-009 (contract tests)

**Acceptance criteria**: AC-9
**Dependencies**: T-001 (DONE), T-002 (DONE), T-003 (DONE), T-004 (DONE), T-005 (DONE), T-006 (DONE), T-007 (DONE)
**Risk**: MEDIUM

**Steps**:
1. Create `tests/us0120_closure_phase_test.py` with 10+ markers:
   ```python
   def test_us0120_closure_command_file_exists_active():
       """AC-1: .cursor/commands/closure.md exists"""
   
   def test_us0120_closure_command_file_exists_template():
       """AC-1: template/.cursor/commands/closure.md exists"""
   
   def test_us0120_closure_command_file_parity():
       """AC-1: active + template byte-identical (PARITY_OK)"""
   
   def test_us0120_dec_0052_phase_role_matrix_includes_closure():
       """AC-2: DEC-0052 phase→role matrix includes closure:qe"""
   
   def test_us0120_dec_0082_ship_macro_includes_closure():
       """AC-3: DEC-0082 ship macro = [release, closure, refresh-context]"""
   
   def test_us0120_auto_phase_plan_includes_closure():
       """AC-4: /auto phase plan includes closure after release"""
   
   def test_us0120_release_md_steps_10_12_removed():
       """AC-5: release.md does NOT contain step 10-12 backup (reconciliation)"""
   
   def test_us0120_closure_verification_schema_defined():
       """AC-6: closure-verification.md schema defined"""
   
   def test_us0120_compose_guards_unchanged():
       """AC-12: US-0043/US-0045/US-0040/US-0048/US-0056/US-0096 untouched"""
   
   def test_us0120_backward_compat_drain_hook():
       """AC-10: drain hook detects in-flight stories needing closure"""
   ```
2. Run tests with pytest
3. Document test markers in closure.md

**Files to create**:
- `tests/us0120_closure_phase_test.py`

**Output**: `tests/us0120_closure_phase_test.py` + pytest results

---

### T-010 (documentation — architecture runbook)

**Acceptance criteria**: AC-11
**Dependencies**: T-anch (VERIFIED), T-001 (DONE), T-003 (DONE), T-004 (DONE), T-006 (DONE)
**Risk**: MEDIUM

**Steps**:
1. Add `## US-0120` section to `docs/engineering/architecture.md`:
   - Overview: separate /closure phase after /release with exclusive Story Closure responsibility
   - Companion DEC: DEC-0120
   - Approach A1: extract closure from release step 10-12 → dedicated /closure phase
   - Files to touch: closure.md (active+template), DEC-0052, DEC-0082, auto.md, release.md
   - Files NOT to touch: US-0043/US-0045/US-0040/US-0048/US-0056/US-0096 (compose guards)
   - Sprint seeds preview: 10 tasks (T-anch + T-001..T-009)
   - Test markers: 10 markers in tests/us0120_closure_phase_test.py
   - Compose guards UNCHANGED (6 surfaces)
   - Risks finalized: R1 (MEDIUM) template parity, R2 (MEDIUM) orchestrator verification, R3 (LOW) backward compat
   - Stop conditions met
   - Sovereign memory note
   - Consequences (reduced release scope, dedicated closure phase, improved fidelity)
   - Evidence references
   - Isolation evidence
   - Strict runtime proof
   - Decision gate
   - Next scheduled phase
2. Add `## Story closure (US-0120)` section to `docs/engineering/runbook.md`:
   - Overview: /closure phase operator recipe
   - When to run: after /release completes, before /refresh-context
   - How to verify: check state.md for closure checkpoint + runtime proof
   - How to manually trigger: for in-flight stories, spawn /closure subagent
   - Troubleshooting: CLOSURE_RELEASE_EVIDENCE_MISSING, CLOSURE_VERIFICATION_FAILED
3. Update `templates/docs/engineering/architecture.md` (+ US-0120 section, byte-identical)
4. Update `templates/docs/engineering/runbook.md` (+ ## Story closure section, byte-identical)

**Files to modify**:
- `docs/engineering/architecture.md` (add ## US-0120 section)
- `docs/engineering/runbook.md` (add ## Story closure (US-0120) section)
- `templates/docs/engineering/architecture.md` (byte-identical)
- `templates/docs/engineering/runbook.md` (byte-identical)

**Output**: architecture.md + runbook.md updated (active + template)

---

## AC → Task mapping

| AC | Task(s) |
|----|---------|
| AC-1 | T-001, T-002 |
| AC-2 | T-anch, T-003 |
| AC-3 | T-anch, T-004 |
| AC-4 | T-006 |
| AC-5 | T-001, T-005 |
| AC-6 | T-007 |
| AC-7 | T-001 |
| AC-8 | T-001, T-007 |
| AC-9 | T-009 |
| AC-10 | T-001, T-008 |
| AC-11 | T-anch, T-010 |
| AC-12 | T-anch, T-002, T-003, T-004, T-005, T-006, T-010 |

**Surjectivity check**: 12/12 ACs covered (AC-1..AC-12 each have ≥1 task). T-anch covers 5 ACs (AC-2, AC-3, AC-11, AC-12). T-001 covers 5 ACs (AC-1, AC-5, AC-7, AC-8, AC-10). All ACs have at least one task. No `PLAN_AC_COVERAGE_GAP`.

## Definition of done

- [ ] 10 tasks completed (T-anch + T-001..T-009)
- [ ] 12/12 acceptance criteria satisfied
- [ ] 6 compose surfaces read-only (US-0043/US-0045/US-0040/US-0048/US-0056/US-0096)
- [ ] closure.md byte-identical (active + template)
- [ ] DEC-0052 phase→role matrix includes closure:qe
- [ ] DEC-0082 ship macro = [release, closure, refresh-context]
- [ ] /auto phase plan includes closure after release
- [ ] release.md step 10-12 removed (reconciliation moved to /closure)
- [ ] closure-verification.md schema documented
- [ ] 10+ contract tests in tests/us0120_closure_phase_test.py
- [ ] drain hook detects in-flight stories needing closure
- [ ] architecture.md + runbook.md updated (active + template)
- [ ] backlog.md US-0120 status flipped OPEN → DONE
- [ ] acceptance.md US-0120 row `[ ]` → `[x]`
- [ ] state.md closure checkpoint appended
- [ ] closure-verification.md artifact written
- [ ] isolation evidence + runtime proof per US-0048/US-0056 contracts
- [ ] all release gates pass (test gate, isolation gate, compose gate)
- [ ] DEC-0120 written + locked
- [ ] PARITY_OK proof for closure.md (active + template)
- [ ] PARITY_OK proof for release.md (active + template)
- [ ] PARITY_OK proof for architecture.md (active + template)
- [ ] PARITY_OK proof for runbook.md (active + template)

## Next phase

**/research** (plan macro — first canonical phase per ultra_lean)
- Role: tech-lead
- Sprint: S0120 (already materialized)
- Focus: close 10 open questions Q1..Q10, finalize approach A1, lock DEC-0120
- Output: updated sprint.md with final approach + DEC-0120 content

## Isolation evidence (US-0048 / DEC-0029)

| Field | Value |
|-------|-------|
| phase_id | discovery |
| role | po |
| story_id | US-0120 |
| sprint_id | (pending) |
| orchestrator_run_id | manual-20260706-us0120-intake |
| fresh_context_marker | po-US0120-discovery-20260706T211500Z-fresh |
| timestamp | 2026-07-06T21:15:00Z |
| delivery_mode | ultra_lean |
| macro_phase | spec |
| fresh_subagent | Yes (BUG-0006 + US-0048) |
| compose_only | Yes (6 surfaces read-only: US-0043/US-0045/US-0040/US-0048/US-0056/US-0096) |
| prior_phase | (none — first story phase after intake) |

## Strict runtime proof (US-0056 / DEC-0038)

| Field | Value |
|-------|-------|
| runtime_proof_id | rp-manual-20260706-us0120-discovery-po-20260706T211500Z-US-0120 |
| phase_id | discovery |
| role | po |
| story_id | US-0120 |
| sprint_id | (pending) |
| orchestrator_run_id | manual-20260706-us0120-intake |
| proof_issued_at | 2026-07-06T21:15:00Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-07-06T22:15:00Z |
| payload | sorted-key JSON: `{"orchestrator_run_id":"manual-20260706-us0120-intake","phase_id":"discovery","proof_issued_at":"2026-07-06T21:15:00Z","proof_ttl_seconds":3600,"role":"po","runtime_proof_id":"rp-manual-20260706-us0120-discovery-po-20260706T211500Z-US-0120","sprint_id":"(pending)","story_id":"US-0120"}` |
| proof_hash | 51904ba4bcf99779abeefa06c65c9214961a54a6175b42432de6ba6387ecebc4 |

## Decision gate

| Field | Value |
|-------|-------|
| decision_gate | false |
| stop_conditions_met | Yes |
| next_phase | /research |
| next_role | tech-lead |
| next_sprint_macro | plan |
| stop_condition | STOP after discovery completes; hand off via artifacts only to /research in fresh tech-lead subagent |
| artifacts_written | sprints/S0120/discovery-locks.md, sprints/S0120/sprint.md, docs/engineering/state.md (discovery checkpoint appended), handoffs/po_to_tl.md (US-0120 discovery block prepended), handoffs/resume_brief.md (US-0120 block prepended) |

---

**Phase completed**: discovery (spec macro — second canonical phase within ultra_lean; intake already complete)
**Phase role**: po (Product Owner)
**Story**: US-0120
**Sprint**: S0120 (pending)
**Orchestrator run**: manual-20260706-us0120-intake
**Delivery mode**: ultra_lean
**Macro phase**: spec
**Fresh subagent**: Yes (BUG-0006 + US-0048 isolation)
**Compose only**: Yes (6 surfaces read-only: US-0043/US-0045/US-0040/US-0048/US-0056/US-0096)
**Timestamp**: 2026-07-06T21:15:00Z
**Stop condition**: STOP after discovery completes; hand off via artifacts only to /research in fresh tech-lead subagent
**Next phase**: /research (plan macro — first canonical phase per ultra_lean)
**Next role**: tech-lead
**Next sprint macro**: plan
