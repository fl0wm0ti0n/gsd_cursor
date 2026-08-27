# Sprint S0129 - Sprint Plan (US-0129)

## Metadata

| Field | Value |
|---|---|
| story_id | US-0129 |
| story_title | Architecture hot-surface rollover linkage guard (active contract preservation) |
| sprint_id | S0129 |
| delivery_mode | ultra_lean |
| macro_phase | plan (sprint-plan terminal; /plan-verify merged into build+verify under QA per ultra_lean) |
| current_phase | sprint-plan |
| approach | A1 locked (from R-0113 DQ1–DQ8) |
| companion_DEC | DEC-0129 (Accepted — `decisions/DEC-0129.md`; story-aligned, not sequential DEC-0127) |
| research_anchor | R-0113 (DQ1–DQ8 LOCKED; R-0112 not extended) |
| orchestrator_run_id | auto-20260827-01 |
| fresh_context_marker | tl-US0129-sprint-plan-20260827T073646Z-fresh |
| timestamp | 2026-08-27T07:36:46Z (UTC) |
| model_id | cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 — required on isolation) |
| verdict | PASS |
| decision_gate | false |
| SPRINT_MAX_TASKS | 12 |
| SPRINT_AUTO_SPLIT | 1 |
| task_count | 8 (T-anch + T-001..T-007; within 12; no split) |
| COMPONENT_SCOPE_MODE | 0 |
| USER_GUIDE_MODE | 0 |
| plan-verify | ultra_lean — merged into build+verify under QA; plan-verify.json NOT written here |
| backlog_status | OPEN (US-0045 — not mutated; acceptance L157 unchecked) |
| critic_carry_ins | 0 new blocking; 3 architecture critic NBs `a0129ar-*` status=resolved non-blocking — routed as awareness into /execute (below) |

## Scope summary

Ship the fail-closed architecture-rollover linkage guard for **US-0129**: wrap `python scripts/enforce-triad-hot-surface.py --rollover` with new `scripts/arch_linkage_guard.py` (pre + post). Discover required active `# US-dddd` / `# BUG-dddd` headings at runtime by scanning contract tests that assert against live `docs/engineering/architecture.md` (stdlib; no hand-maintained manifest). Pre-hook: if a required heading would leave the hot file and `ARCH_LINKAGE_AUTO_REPAIR=0`, emit `ARCH_LINKAGE_ROLLOVER_BLOCKED` and **do not write** archive pack or hot file. Post-hook: re-verify active linkage (packs append-only; no pack rollback). Optional repair (`ARCH_LINKAGE_AUTO_REPAIR=1`) injects minimal H1 stubs + one-line `pack_ref` before the US-0089 / US-0090 tail. Flag default-off, not in `AUTONOMY_PRESET`. Code is `security_hard` (never skip). Wire `/refresh-context` step 4: pre-guard → `--rollover` → post-guard → existing `--check`. Eight `test_us0129_*` markers + harness **26AB**. Runbook h3 under triad. `ARCH_LINKAGE_PAIRS` + `--scope=arch-linkage`. Manifest row for the new script.

This is an **additive guard + reason-code + optional stub repair + command wiring + docs + parity + contract-test** change. Archiver heading-split / pack naming / `ARCH_HOT_MAX_*` **UNCHANGED**. Companion **DEC-0129** already Accepted at architecture. Compose DEC-0054 / DEC-0073 / DEC-0076 / US-0049 / US-0126 B-1 fixture / DEC-0119 only.

Out of scope: mutating `rollover_architecture` internals (A2 rejected); YAML/manifest of required headings (A3 rejected); default-on auto-repair (A4 rejected); 10th `auto_repair_kind` / skip-on-policy (A5 rejected); sequential DEC-0127 (A6 rejected); full-section or named body-token restore (A7 rejected); raising `ARCH_HOT_MAX_*` (A8 rejected); reopening US-0126/US-0127/US-0128/US-0130; ticking acceptance L157; marking US-0129 DONE; mutating intake JSON; spawning `/plan-verify`.

## Execute awareness (architecture critic NBs — 0 blocking)

Sovereign-critic of architecture PASS (`tl-US0129-sovereign-critic-architecture-20260827T073500Z-fresh`; anti_slop=8; 0 blocking). Route these resolved NBs as execute awareness — do not re-open them as work:

| Finding | Issue key | Execute awareness |
|---|---|---|
| `a0129ar-challenger-001` | `ik_us0129_arch_proof_and_linkage_gaps` | **T-001** discovery must exclude `.tmp*` and non-`architecture.md` reads (R1 fixture false-positives). **T-003** v1 is heading-only (R3 body-token residual documented, not in v1). Do not pre-seed unrelated stubs in /execute if a required heading is already absent (R6) — remediate via AC-2 repair flag or manual H1, then rerun `--rollover`. |
| `a0129ar-architect-002` | `ik_us0129_arch_layer_coupling` | Keep layering: T-001 owns helper + pre-guard no-partial-write; T-002 owns reason_codes + `security_hard` matrix row; T-003 owns flag comment + DQ8 stub path; T-004 owns `/refresh-context` wiring; T-005 owns 8 markers + 26AB; T-006 owns runbook h3 + `ARCH_LINKAGE_PAIRS`; T-007 owns installer manifest. Import `split_arch_stories` + while-pop — do not copy-fork the archiver. Do not add `ARCH_LINKAGE_AUTO_REPAIR` to `AUTONOMY_PRESET`. |
| `a0129ar-subtractor-003` | `ik_us0129_arch_scope_discipline` | Do not mark US-0129 DONE; do not tick L157; 8 markers are required (not YAGNI); T-anch is read-only ceremony — no architecture.md mutation in /execute; do not author a second DEC; do not reopen US-0126/US-0127/US-0128/US-0130. |

## Acceptance criteria (6) - US-0129 (status OPEN, acceptance L157 unchecked per US-0045)

- **AC-1**: Linkage guard script — Add `scripts/arch_linkage_guard.py` invoked pre/post `enforce-triad-hot-surface.py --rollover`; detect active-only US/BUG heading refs required by contract tests.
- **AC-2**: Fail-closed block — On violation emit `ARCH_LINKAGE_ROLLOVER_BLOCKED` with story id, missing heading, archive pack path, remediation.
- **AC-3**: Optional auto-repair — Bounded restore of minimal heading stubs from latest archive pack before rollover commit (idempotent, audit row in state.md).
- **AC-4**: Rollover wiring — Wire guard into `/refresh-context` rollover path and harness marker; template parity for script + runbook h3 under triad (architecture locked h3, not a sibling h2).
- **AC-5**: Regression tests — US-0126 B-1 fixture class: rollover without guard FAIL; with guard PASS or explicit block. Eight `test_us0129_*` markers + harness **26AB**. Synthetic fixtures — do not replay `architecture-pack-20260825.md`.
- **AC-6**: Compose — Read-only with DEC-0054/DEC-0073/US-0049; do not reopen US-0126 product scope. (Also DEC-0076/US-0089 tail, DEC-0119 9-kind taxonomy, US-0127/US-0128/US-0130 DONE rows.)

## Task summaries (8 - T-anch + T-001..T-007)

- **T-anch** (NO-OP / verification): Verify `# US-0129` H1 in `docs/engineering/architecture.md` AFTER `# US-0128` BEFORE `# US-0130`; verify DEC-0129 Accepted; verify approach A1 + R-0113 DQ1–DQ8 LOCKED; verify compose-do-not-amend 8/8; verify 8-marker list locked; verify `scripts/arch_linkage_guard.py` and `tests/us0129_contract_test.py` do NOT yet exist. Record to `sprints/S0129/t-anch-verification.md`. NO mutation to `architecture.md` in /execute.
- **T-001** (AC-1 + AC-2 — helper + pre-guard): `scripts/arch_linkage_guard.py` `discover_required_arch_headings` + pre-guard no-partial-write; + template mirror.
- **T-002** (AC-2 — reason code + matrix): `reason_codes.md` `## US-0129` + `ARCH_LINKAGE_ROLLOVER_BLOCKED` + autonomy-stop-matrix `security_hard` row; + template mirrors.
- **T-003** (AC-3 — flag + stub restore): `ARCH_LINKAGE_AUTO_REPAIR=0` scratchpad comment (no live `=1`) + DQ8 stub restore path; + template mirrors.
- **T-004** (AC-4 — command wiring): `.cursor/commands/refresh-context.md` pre-guard → `--rollover` → post-guard → `--check`; + template mirror.
- **T-005** (AC-5 — contract tests + harness): `tests/us0129_contract_test.py` 8 markers + harness **26AB** in `run-tests.ps1` / `run-tests.sh`; + template test mirror.
- **T-006** (AC-4 / D8 — runbook + parity): runbook h3 under triad + `ARCH_LINKAGE_PAIRS` / `--scope=arch-linkage`; + template runbook.
- **T-007** (D8 — installer): `installer-owned-paths.manifest` active + template for `scripts/arch_linkage_guard.py`.

Execution order: T-anch → T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 (acyclic; guard first, then reason-code/matrix, then flag+stub, then wiring, then tests, then docs/parity/installer).

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (Linkage guard script) | T-001 (helper + pre-guard), T-005 (markers 1, 2, 6) |
| AC-2 (Fail-closed block) | T-001 (emit + no-partial-write), T-002 (reason_codes + matrix), T-005 (markers 2, 3) |
| AC-3 (Optional auto-repair) | T-003, T-005 (markers 4, 5) |
| AC-4 (Rollover wiring) | T-004, T-006, T-005 (markers 6, 7) |
| AC-5 (Regression tests) | T-005 (all 8 markers; marker 8 is B-1 class) |
| AC-6 (Compose) | T-anch |

**Surjectivity check**: 6/6 ACs covered (each AC has at least 1 task). No `PLAN_AC_COVERAGE_GAP`.

## Risks (R1–R6 — accepted from architecture)

| Risk | Severity | Mitigation in this sprint |
|---|---|---|
| R1 Helper false-positive on fixture strings or command-file greps | HIGH | T-001 exclude `.tmp*` and non-`architecture.md` reads; T-005 marker 1 |
| R2 Stub placed after `# US-0089` breaks caveman bottom-append | HIGH | T-003 DQ8 insertion before US-0089/US-0090 tail; T-005 marker 5 uses US-0089-tail fixture |
| R3 Body-token residual after heading-only repair | MEDIUM | v1 heading-only (Q3); document residual; do not reopen US-0100 |
| R4 `auto_repair_then_skip` operator expects skip | MEDIUM | T-002 `security_hard` row `auto_repair_kind=n/a` `cap=0`; never skip |
| R5 Dual pre/post latency on every `/refresh-context` | LOW | stdlib local scan; no network |
| R6 Required heading already absent at first post-ship `--rollover` | LOW | AC-2 remediation (repair flag or manual stub); do not pre-seed unrelated stubs |

## Compose guards (8/8 UNCHANGED — additive guard + reason-code + optional stub + wiring + docs + parity + contract-test only)

| Compose target | Verification | Result |
|---|---|---|
| DEC-0054 | guard wraps; `rollover_architecture` split / pack format / `ARCH_HOT_MAX_*` unchanged; marker 2 | compose |
| DEC-0073 | stub is H1 with title separator; H2 policy unchanged | compose |
| DEC-0076 / US-0089 | stub insertion before US-0089/US-0090 tail; marker 5 | compose |
| US-0049 | state.md audit row append-bottom; no archive rewrite | compose |
| US-0126 | B-1 fixture only; acceptance L154 stays checked; product scope not reopened | compose |
| US-0127 / US-0128 / US-0130 | DONE rows not reopened; L155–L156 / L158 stay checked; L157 stays unchecked | compose |
| DEC-0119 | no 10th `auto_repair_kind`; no 13th preset flag; flag not in `AUTONOMY_PRESET` | compose |
| R-0112 | US-0130 overlay not extended | compose |

## Execute phase role (per DEC-0051 / US-0069)

| Phase | Role | Isolation |
|---|---|---|
| /execute | dev (fresh per BUG-0006) | {phase_id:execute, role:dev} |
| /qa | qa (fresh) | {phase_id:qa, role:qa} — creates plan-verify.json within build+verify per ultra_lean |
| /verify-work | qa (fresh) | {phase_id:verify-work, role:qa} |
| /release | release (fresh) | {phase_id:release, role:release} |
| /closure | qe (fresh) | {phase_id:closure, role:qe} |
| /refresh-context | curator (fresh) | {phase_id:refresh-context, role:curator} |

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

| Field | Value |
|---|---|
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0129 |
| sprint_id | S0129 |
| orchestrator_run_id | auto-20260827-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| fresh_context_marker | tl-US0129-sprint-plan-20260827T073646Z-fresh |
| timestamp | 2026-08-27T07:36:46Z (UTC) |
| model_id | cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 — required) |
| evidence_ref | sprints/S0129/sprint.md, sprints/S0129/tasks.md, sprints/S0129/progress.md, sprints/S0129/uat.json, sprints/S0129/uat.md, handoffs/tl_to_dev.md (US-0129 prepend), docs/engineering/state.md (sprint-plan checkpoint append-bottom + traceability row), docs/engineering/architecture.md # US-0129 (L1527 — not mutated), handoffs/resume_brief.md |

Prior phase proof consumed: `rp-auto-20260827-01-architecture-tech-lead-20260827T073000Z-US-0129` (proof_hash=DDDA46794ED39186D77F268EE47364E3070997916777582095FF9198FEEF6196, ttl 2026-08-27T08:30:00Z — independent SHA-256 MATCH; consumed at 2026-08-27T07:36:46Z before RUNTIME_PROOF_STALE). Sovereign-critic architecture PASS at 2026-08-27T07:35:00Z (anti_slop_aggregate=8; 0 blocking findings; 3 NBs `a0129ar-*` status=resolved).

## Runtime proof (DEC-0038)

| Field | Value |
|---|---|
| runtime_proof_id | rp-auto-20260827-01-sprint-plan-tech-lead-20260827T073646Z-US-0129 |
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0129 |
| sprint_id | S0129 |
| orchestrator_run_id | auto-20260827-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| model_id | cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 — required) |
| proof_issued_at | 2026-08-27T07:36:46Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-08-27T08:36:46Z (UTC) |
| proof_hash | 8960A93B97E39E84B107001316228F5CBE69472DDF8835752862ECF4EC3B4B00 |
| canonical_payload | `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260827-01","phase_id":"sprint-plan","proof_issued_at":"2026-08-27T07:36:46Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260827-01-sprint-plan-tech-lead-20260827T073646Z-US-0129","sprint_id":"S0129","story_id":"US-0129"}` |

## Decision gate

| Field | Value |
|---|---|
| decision_gate | false |
| stop_conditions_met | yes |
| missing_acceptance_criteria | none (6/6 ACs covered; 8 contract-test markers; compose guards 8/8) |
| compose_guards | 8/8 UNCHANGED |
| dc_check | clean (`# US-0129` H1 already added in /architecture at L1527; DEC-0129 already Accepted) |
| task_count | 8 (within SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1 but no split needed) |
| risks_finalized | 6/6 ACCEPTED (R1..R6) |
| approach | A1 locked |
| companion_DEC | DEC-0129 Accepted |
| plan-verify readiness | ultra_lean — /plan-verify merged into build+verify under QA; plan-verify.json NOT written in this spawn |
| sovereign_memory_note | `assemble_sovereign_memory_digest(...)` NOT called; no mistakes.jsonl write |

## Definition of done (sprint-plan)

- [x] 8 tasks enumerated (T-anch + T-001..T-007) — within SPRINT_MAX_TASKS=12
- [x] 6/6 ACs covered by 8 contract-test markers + compose guards 8/8 (surjective)
- [x] Task dependency graph documented
- [x] Execute phase role matrix documented (ultra_lean — /plan-verify merged into build+verify under QA)
- [x] Compose guards 8/8 UNCHANGED
- [x] Critic carry-ins (3 non-blocking from architecture sovereign-critic) routed as execute awareness
- [x] Isolation evidence + runtime proof emitted (model_id=cursor-grok-4.6-high present)
- [x] Sprint-plan checkpoint appended to `docs/engineering/state.md`
- [x] Sprint-plan handoff prepended to `handoffs/tl_to_dev.md`
- [x] Sprint-plan PASS prepended to `handoffs/resume_brief.md` (-> /execute)
- [x] UAT placeholders written (`uat.json` empty steps, `uat.md` ACs no results)
- [x] Traceability row added to `docs/engineering/state.md` (Story=US-0129 | Sprint=S0129 | Tasks=T-anch+T-001..T-007 | Status=PLANNED | Evidence empty)
- [x] Backlog status OPEN (US-0045 — not mutated); AC checkboxes untouched

## Next scheduled phase

| Field | Value |
|---|---|
| next_scheduled_phase | `/execute` (role=dev per US-0069 / DEC-0051; fresh dev subagent per BUG-0006; first canonical phase of `build+verify` macro per ultra_lean; /plan-verify merged into qa per ultra_lean — qa creates plan-verify.json within build+verify). Orchestrator runs sovereign-critic of sprint-plan first (CROSS_MODEL_REVIEW=1). Do not mandate outer driver. |
| next_scheduled_role | dev |
| next_sprint_macro | build+verify (ultra_lean — plan-verify merged into qa) |
| stop_condition | STOP after sprint-plan completes; hand off via artifacts only. Orchestrator owns critic of sprint-plan then `/execute` in fresh dev subagent per BUG-0006. Do not spawn /execute or /plan-verify from this subagent. |
| artifacts_written | sprints/S0129/ (sprint.md, tasks.md, progress.md, uat.json, uat.md), docs/engineering/state.md (sprint-plan checkpoint append-bottom + traceability row), handoffs/tl_to_dev.md (US-0129 prepend), handoffs/resume_brief.md (sprint-plan PASS prepend -> /execute) |
