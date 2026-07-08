# PO to TL archive pack (2026-07-08)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 4
- Retained units in hot file: 7
- First archived heading: `## Sprint-plan handoff -> US-0120 Separate /closure phase (plan macro)`
- Last archived heading: `## Discovery handoff -> US-0120 Separate `/closure` phase after `/release` (spec macro)`
- Verification tuple (mandatory):
  - archived_body_lines=213
  - retained_body_lines=580

---

## Sprint-plan handoff -> US-0120 Separate /closure phase (plan macro)

**Phase completed**: sprint-plan
**Phase role**: tech-lead
**Story**: US-0120
**Verdict**: PASS (no DECISION_GATE)
**Timestamp**: 2026-07-07T21:55:00Z
**Fresh context marker**: tl-US0120-sprint-plan-20260707T215500Z-fresh
**Runtime proof**: rp-manual-20260707-us0120-sprint-plan-tl-20260707T215500Z-US-0120 (proof_hash=a702bc1226d474ad9851db6a8e1e5fa89f48adb22a54fa60c5d5b59a447e27a, proof_ttl=2026-07-07T22:55:00Z)

**Summary**: Sprint plan generated (sprints/S0120/sprint-plan.md + sprints/S0120/tasks.md). 10 tasks (T-anch + T-001..T-010) within SPRINT_MAX_TASKS=12. Task dependency graph: T-anch first (NO-OP / verification of architecture anchor at L2125 + compose guards), {T-001, T-003, T-004} parallel (closure.md active + DEC-0052 rows + DEC-0082 ship macro), {T-002, T-005, T-006} parallel (template closure.md + release.md step-10-12-removal + validator script), T-007 (isolation+proof contract), T-008 (10 contract tests), T-009 (drain hook + installer manifest), T-010 (runbook `## Story closure (US-0120)` h2), integration verification last. Execute phase role: dev (fresh per BUG-0006). QA phase role: qa (creates plan-verify.json per ultra_lean merger). Verify-work phase role: qa. Compose guards 6/6 UNCHANGED (US-0043/US-0045/US-0040/US-0048/US-0056/US-0096 verified read-only). All 12 ACs covered by 10 test markers (surjective). DC check clean. 10/10 Q LOCKED, 8/8 R ACCEPTED, A1 locked. plan-verify merged into qa per ultra_lean.

**Next action**: /execute (dev, first phase of build+verify macro per ultra_lean)

**Artifacts written**:
- sprints/S0120/sprint-plan.md (NEW — sprint plan + phase role matrix + task dependency graph + decision gate + isolation evidence + runtime proof)
- sprints/S0120/tasks.md (NEW — 10-task checklist with per-task AC coverage + files to touch/skip)
- docs/engineering/state.md (sprint-plan checkpoint appended)
- handoffs/po_to_tl.md (this sprint-plan handoff prepended)
- handoffs/resume_brief.md (drain-advance prepended)

## Architecture handoff -> US-0120 Separate /closure phase (plan macro)

**Phase completed**: architecture
**Phase role**: tech-lead
**Story**: US-0120 — Separate /closure phase after /release with exclusive Story Closure responsibility
**Verdict**: PASS (no DECISION_GATE)
**Timestamp**: 2026-07-07T21:50:00Z
**Fresh context marker**: tl-US0120-architecture-20260707T215000Z-fresh
**Runtime proof**: rp-manual-20260707-us0120-architecture-tl-20260707T215000Z-US-0120 (proof_hash=6293266bfcdf3e6e668cf28a34d831e55cc05a17e5dea1fc8ee94b70ca67b99f, proof_ttl=2026-07-07T22:50:00Z)

**Summary**: Architecture section appended to docs/engineering/architecture.md L2125 (H1 # US-0120). 12 acceptance criteria mapped to 10 sprint seeds (T-anch + T-001..T-010). Compose guards 6/6 UNCHANGED (US-0043/US-0045/US-0040/US-0048/US-0056/US-0096 read-only). Approach A1 locked: dedicated /closure phase with qe role + orchestrator rg verification. DEC-0052 phase->role matrix extended (closure|qe|AUTO_ROLE_CLOSURE override). DEC-0082 ship macro extended [release, closure, refresh-context]. release.md steps 10-12 removed with pointer to /closure. 10 test markers enumerated. 10/10 discovery locks D1..D12 resolved. 8/8 risks R1..R8 ACCEPTED. DC check clean.

**Next action**: /sprint-plan (tech-lead, third phase of plan macro per ultra_lean)

## Research handoff -> US-0120 Separate `/closure` phase after `/release` (plan macro)

**Phase completed**: research
**Phase role**: tech-lead
**Story**: US-0120 Separate `/closure` phase after `/release` with exclusive Story Closure responsibility
**Verdict**: PASS (no DECISION_GATE)
**Timestamp**: 2026-07-07T21:45:00Z
**Fresh context marker**: tl-US0120-research-20260707T214500Z-fresh
**Delivery mode**: ultra_lean
**Macro phase**: plan (research + architecture + sprint-plan merged)
**Work kind**: doc

### Summary

Extract Story Closure from /release step 10-12 into dedicated /closure phase with exclusive qe role ownership. Ship macro: release â†’ closure â†’ refresh-context (3 phases). Orchestrator post-closure rg verification enforces materialization fidelity. Compose (read-only) with 6 surfaces: US-0043, US-0045, US-0040, US-0048, US-0056, US-0096.

### Approach locked (A1)

**Approach A1** (locked): Dedicated /closure phase with exclusive qe ownership + orchestrator post-verification. Resolves US-0119 fidelity gap; follows "one phase, one responsibility" principle. Alternatives rejected: A2 (keep closure in /release + add verification â€” same BUG-0006 fidelity pattern), A3 (extract to /qa â€” conflates quality findings with status reconciliation, violates phase ordering).

### Open questions Q1..Q10 â€” ALL LOCKED

- **Q1 (closure-verification.md schema)** â†’ REQUIRED: story_id, closure_date, closure_role, pre_closure_status, post_closure_status, release_evidence_refs[], isolation_evidence{}, runtime_proof{}. OPTIONAL: normalization_notes, backward_compat_note.
- **Q2 (AUTO_ROLE_CLOSURE fallback)** â†’ LOCKED: qe â†’ curator (primary â†’ fallback). Deterministic; if both fail, escalate with CLOSURE_ROLE_UNAVAILABLE.
- **Q3 (closure role in DEC-0052)** â†’ LOCKED: ADD new row closure:qe (distinct phase, NOT inheritance from /qa). ADD AUTO_ROLE_CLOSURE override + preflight capability row.
- **Q4 (drain hook detection)** â†’ LOCKED: 3-signal: release_queue status=released + backlog Status:OPEN + acceptance [ ] â†’ spawn /closure. Pre-US-0120 legacy drift = CLOSURE_LEGACY_DRIFT.
- **Q5 (backward compat)** â†’ LOCKED: FORWARD-COMPAT ONLY. Already-DONE stories untouched. US-0120 does NOT retroactively create closure-verification.md for prior stories.
- **Q6 (format .json vs .md)** â†’ LOCKED: **closure-verification.md** (markdown). Resolves discovery.md D4 discrepancy (said .json). Follows lifecycle artifact convention (qa-findings.md, release-findings.md).
- **Q7 (rg post-closure verification)** â†’ LOCKED: Two deterministic rg checks: (1) rg "^- Status: DONE$" backlog.md (target story block), (2) rg "^- \[x\] US-xxxx:" acceptance.md. State.md: two-stage grep phase_id=closure + story_id=US-xxxx.
- **Q8 (release.md renumbering)** â†’ LOCKED: Remove steps 10-12 (backlog reconciliation + derived views + normalization). Old step 13 â†’ new step 10 (with closure pointer). Sequential renumbering, no gaps. Active + template byte-identical.
- **Q9 (compose surface anchors)** â†’ LOCKED: US-0096 has ## US-0096 anchor at L1684. US-0043/US-0045/US-0040/US-0048/US-0056 have inline references (no dedicated ## anchors). Verify via inline grep.
- **Q10 (test markers)** â†’ LOCKED: 10 markers in tests/us0120_closure_phase_test.py (closure file exists active+template, parity, DEC-0052 closure, DEC-0082 ship macro, /auto phase plan, release.md steps 10-12 removed, schema validator, compose guards, backward compat drain hook).

### Risks R1..R8 â€” ALL ACCEPTED

- **R1 (MEDIUM)**: Subagent fidelity gap (qe claims closure but files unchanged). Mitigation: D12 orchestrator post-closure rg verification â†’ CLOSURE_VERIFICATION_FAILED.
- **R2 (LOW)**: Backward compat for in-flight stories. Mitigation: Q4 detection logic.
- **R3 (LOW-MEDIUM)**: DEC-0052 scope creep. Mitigation: T-003 scoped edit + contract test.
- **R4 (LOW-MEDIUM)**: DEC-0082 scope creep. Mitigation: T-004 scoped edit + contract test.
- **R5 (LOW)**: release.md step 10-12 removal deterministic renumbering. Mitigation: T-005 + contract test.
- **R6 (LOW)**: Template parity drift for closure.md. Mitigation: T-001 + T-002 byte-identical construction + parity checker extension.
- **R7 (LOW)**: Closure-verification.md schema rigidity. Mitigation: extensible schema with optional fields.
- **R8 (LOW)**: Backward compat for already-released S0119. Mitigation: Q4 detection logic SKIPS DONE stories.

### Compose guards (6/6 UNCHANGED)

US-0043, US-0045, US-0040, US-0048, US-0056, US-0096 â€” all verified present as read-only consumers. No edits scheduled.

### DC check

- `grep "^## US-0120" docs/engineering/architecture.md` â†’ no matches (expected; anchor added in /architecture phase)
- Not appended to deferrals.jsonl

### Sprint seeds preview (for /sprint-plan)

- **Task count**: 10 tasks (T-anch + T-001..T-009) within SPRINT_MAX_TASKS=12
- **Test markers**: 10 markers in tests/us0120_closure_phase_test.py
- **Files to touch**: closure.md (active+template), DEC-0052, DEC-0082, auto.md, release.md (active+template), scratchpad.md, closure-verification.md schema validator, contract tests, architecture.md (## US-0120), runbook.md (## Story closure (US-0120))
- **Files NOT to touch**: US-0043/US-0045/US-0040/US-0048/US-0056/US-0096 surfaces (compose guards)

### Decision gate

- `decision_gate=false`
- `stop_conditions_met=yes`
- All 10/10 open questions LOCKED
- All 8/8 risks ACCEPTED
- Approach A1 locked
- Compose guards 6/6 UNCHANGED

### Next scheduled phase

- **next_scheduled_phase=/architecture** (tech-lead role, fresh subagent per BUG-0006)
- **stop_condition=STOP after research completes; hand off via artifacts only to /architecture**

---

## Discovery handoff -> US-0120 Separate `/closure` phase after `/release` (spec macro)

**Phase completed**: discovery
**Phase role**: po
**Story**: US-0120 Separate `/closure` phase after `/release` with exclusive Story Closure responsibility
**Verdict**: PASS (no DECISION_GATE)
**Timestamp**: 2026-07-06T21:30:00Z
**Fresh context marker**: po-US0120-discovery-20260706T213000Z-fresh
**Runtime proof**: rp-auto-20260706-01-discovery-PO-20260706T213000Z-US-0120 (proof_hash=447f401d9ca72415e0f3d607829eaced5fb14cbbffd71a48a336de48a9d040dd, proof_ttl=2026-07-06T22:30:00Z)
**Delivery mode**: ultra_lean (spec+plan merged)
**Macro phase**: spec (intake+discovery merged)
**Companion DEC**: none (modifies DEC-0052 + DEC-0082 directly)
**Work kind**: doc
**Plan area**: lifecycle-governance

### Summary

Extract Story Closure (Status DONE in backlog.md + acceptance checkbox + state checkpoint + closure-verification artifact) from /release step 10-12 into a dedicated /closure phase with exclusive qe role ownership. New ultra_lean ship macro: release -> closure -> refresh-context (3 phases). Orchestrator post-closure rg verification (D12) ensures materialization fidelity (fixes US-0119 closure-lï¿½cke pattern). Compose (read-only) with US-0043/US-0045/US-0040/US-0048/US-0056/US-0096.

### Discovery locks (D1..D12)

**D1 (phase ownership)**: /closure phase role = qe (fresh qe subagent per BUG-0006 / US-0048 isolation). Fallback: curator when qe unavailable.

**D2 (phase ordering)**: /closure executes AFTER /release PASS (release artifacts written, queue updated), BEFORE /refresh-context. Ultra_lean ship macro becomes release -> closure -> refresh-context (3 phases). Standard: ... -> execute -> qa -> verify-work -> release -> closure -> refresh-context. All 3 delivery modes (standard, ultra_lean, mega_quick) include closure.

**D3 (input prerequisites)**: /closure requires (a) release queue row status=released, (b) handoffs/releases/Sxxxx-release-notes.md EXISTS with PASS verdict, (c) sprints/Sxxxx/qa-findings.md EXISTS. Fail-gated: CLOSURE_RELEASE_EVIDENCE_MISSING.

**D4 (output artifacts)**: (a) docs/product/backlog.md target story status OPEN -> DONE (canonical ownership per US-0045), (b) docs/product/acceptance.md target checkbox [ ] -> [x] (derived view per US-0045), (c) docs/engineering/state.md closure checkpoint (derived view per US-0045), (d) sprints/Sxxxx/closure-verification.json NEW artifact documenting closure execution with isolation evidence + runtime proof references.

**D5 (compose with US-0043)**: /closure is the executor of backlog reconciliation that US-0043 defines. US-0043 contract UNCHANGED; closure implements it as a dedicated phase. Evidence precedence: release queue -> release notes -> qa-findings -> uat -> release-findings.

**D6 (compose with US-0045)**: /closure follows US-0045 canonical status ownership: backlog.md is canonical owner (mutated FIRST); acceptance.md and state.md are derived views (mutated SECOND, atomically). Contradiction -> CANONICAL_STATUS_CONFLICT fail-gate.

**D7 (compose with US-0040)**: /closure operates AFTER release artifacts are written (US-0040 contract). Release writes release notes + queue; closure writes status/acceptance. No overlap.

**D8 (compose with US-0048)**: /closure produces its own isolation evidence entry in state.md per US-0048 (phase_id=closure, role=qe, fresh_context_marker, timestamp). Fresh qe subagent per BUG-0006.

**D9 (compose with US-0056)**: /closure produces its own strict runtime proof per US-0056 (sorted-key JSON payload, SHA-256 proof_hash, proof_ttl_seconds=3600). Per DEC-0038.

**D10 (release.md step 10-12 removal)**: After US-0120 ships, .cursor/commands/release.md steps 10-12 are REMOVED and replaced with a pointer: "Backlog reconciliation is now handled by the dedicated /closure phase -- see .cursor/commands/closure.md".

**D11 (template parity)**: New .cursor/commands/closure.md must be byte-identical to template/.cursor/commands/closure.md (active <-> template mirror). Checked by check_intake_template_parity.py.

**D12 (orchestrator post-closure verification)**: After /closure returns, orchestrator runs direct rg verification: (a) rg "^- Status: DONE$" docs/product/backlog.md (target story block), (b) rg "^\*- \[x\] US-xxxx:" docs/product/acceptance.md (target row). If either FAIL -> escalate to operator with CLOSURE_VERIFICATION_FAILED.

### Composition notes

**Compose, do not amend (6/6 UNCHANGED)**: US-0043 (backlog reconciliation contract), US-0045 (canonical status source), US-0040 (release artifacts), US-0048 (isolation evidence), US-0056 (runtime proof), US-0096 (delivery modes). All verified present (read-only consumers of US-0120).

**DC check**: `grep "^## US-0120" docs/engineering/architecture.md` -> no matches (expected; anchor will be added in /architecture phase).

### Open questions for /research (Q1..Q10)

**Q1** (closure-verification artifact schema): exact fields, required vs optional, format (.json vs .md).
**Q2** (closure role designation): qe by default, fallback to curator; canonical choice confirmation.
**Q3** (phase->role matrix extension): DEC-0052 closure row placement, role column syntax.
**Q4** (drain hook in-flight story detection): /auto drain-advance hook detects stories that completed /release but skipped closure (status still OPEN) -> spawn /closure.
**Q5** (backward compat for status-drift stories): US-0108 etc. -- forward-compat only, no retroactive closure.
**Q6** (template parity scope): .cursor/commands/closure.md <-> template/.cursor/commands/closure.md byte-identical enforcement.
**Q7** (orchestrator rg verification regex): exact patterns for post-closure verification.
**Q8** (release.md step renumbering): after removing steps 10-12, renumber remaining steps 13+ -> 10+.
**Q9** (compose surface verification): 6 architectural anchors present and unchanged.
**Q10** (test coverage): 10 contract tests in tests/us0120_closure_phase_test.py.

### Risks carried to /architecture (R1..R6)

**R1 (MEDIUM)**: Subagent execution fidelity (US-0119 pattern -- release subagent claimed closure but files unchanged). Mitigated by orchestrator-side post-closure rg verification (D12).

**R2 (MEDIUM)**: Backward compat for in-flight stories (stories currently in /release when US-0120 ships). Detection logic in /auto drain hook (Q4) must handle both cases (closure already performed vs skipped).

**R3 (LOW-MEDIUM)**: DEC-0052 phase->role matrix scope creep. Only ADD closure:qe row; must NOT modify existing role mappings.

**R4 (LOW-MEDIUM)**: DEC-0082 delivery-mode table scope creep. Only ADD closure to ship macro; must NOT modify other macro definitions.

**R5 (LOW)**: release.md step 10-12 removal scope. Only remove closure responsibilities; must NOT modify other release steps.

**R6 (LOW)**: Template parity drift. .cursor/commands/closure.md active <-> template must stay byte-identical across all future edits.

### Isolation evidence

- phase_id=discovery, role=po, story_id=US-0120, sprint_id=S0120
- orchestrator_run_id=auto-20260706-01
- fresh_context_marker=po-US0120-discovery-20260706T213000Z-fresh
- timestamp=2026-07-06T21:30:00Z (UTC)
- evidence_ref=docs/product/backlog.md (US-0120 block L3972-4038), docs/product/acceptance.md (US-0120 row L146), handoffs/intake_evidence/US-0120-intake-20260706.json (full read), handoffs/po_to_tl.md (current US-0120 block L1-59 narrow-read), docs/engineering/state.md (US-0118 discovery checkpoint L84-107 narrow-read, US-0119 discovery checkpoint L121-176 narrow-read), .cursor/commands/release.md (steps 10-12 L334-347 narrow-read for D10 removal scope; release gate chain L88-101; backlog reconciliation contract L148-168; canonical status source L169-188), docs/engineering/architecture.md (grep ^## US-0043/^## US-0045/^## US-0040/^## US-0096/^## US-0048/^## US-0056 anchors only -- all 6 verified present), decisions/DEC-0052.md (phase->role matrix), decisions/DEC-0082.md (ship macro table)
- PO subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward; no MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + the artifact writes listed in this prompt. No .env reads, no credentials access, no intake-evidence mutation.

### Strict runtime proof

- runtime_proof_id=rp-auto-20260706-01-discovery-PO-20260706T213000Z-US-0120
- Canonical payload (sorted-key JSON per DEC-0038): {"orchestrator_run_id":"auto-20260706-01","phase_id":"discovery","proof_issued_at":"2026-07-06T21:30:00Z","proof_ttl_seconds":3600,"role":"po","runtime_proof_id":"rp-auto-20260706-01-discovery-PO-20260706T213000Z-US-0120","sprint_id":"S0120","story_id":"US-0120"}
- proof_hash=447f401d9ca72415e0f3d607829eaced5fb14cbbffd71a48a336de48a9d040dd (SHA-256, python hashlib)
- proof_ttl_seconds=3600, proof_ttl=2026-07-06T22:30:00Z (UTC)

### Decision gate + next scheduled phase

- decision_gate=false (no DECISION_GATE)
- next_scheduled_phase=/research (role=tech-lead per US-0069 / DEC-0051)
- stop_condition=STOP after discovery completes; hand off via artifacts only to /research in fresh tech-lead subagent (BUG-0006)

---

