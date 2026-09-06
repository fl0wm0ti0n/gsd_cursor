# Sprint S0132 - Sprint Plan (BUG-0016)

## Metadata

| Field | Value |
|---|---|
| bug_id | BUG-0016 |
| story_id | (none — bug segment) |
| story_title | OpenCode Layer-1 permissions vs kit duties (amend DEC-0122 §2) |
| sprint_id | S0132 |
| delivery_mode | ultra_lean |
| macro_phase | plan (sprint-plan terminal; /plan-verify merged into build+verify under QA per ultra_lean) |
| current_phase | sprint-plan |
| approach | A* locked (from R-0115 DQ1–DQ8; CF1–CF5 CLOSED) |
| companion_DEC | none (DEC-0130 rejected; DEC-0122 §2 amended sole SOT in /architecture) |
| research_anchor | R-0115 (DQ1–DQ8 LOCKED) |
| architecture_anchor | docs/engineering/architecture.md # BUG-0016 |
| orchestrator_run_id | auto-20260906-bug0016 |
| fresh_context_marker | tl-BUG0016-sprint-plan-20260906T185500Z-fresh |
| timestamp | 2026-09-06T18:55:00Z (UTC) |
| model_id | composer-2.5 (CROSS_MODEL_REVIEW=1 — required on isolation) |
| verdict | PASS |
| decision_gate | false |
| SPRINT_MAX_TASKS | 12 |
| SPRINT_AUTO_SPLIT | 1 |
| task_count | 8 (T-anch + T-001..T-007; within 12; no split; 1:1 from architecture seeds) |
| COMPONENT_SCOPE_MODE | 0 |
| USER_GUIDE_MODE | 0 |
| plan-verify | ultra_lean — merged into build+verify under QA; plan-verify.json NOT written here |
| backlog_status | OPEN (US-0045 — not mutated; acceptance BUG-0016 unchecked) |
| critic_carry_ins | 0 new blocking; 3 architecture critic NBs `b0016ar-*` status=resolved non-blocking — routed as awareness into /execute (below) |

## Scope summary

Close the **OpenCode Layer-1 permission matrix vs kit phase-duty gap**. US-0122 / DEC-0122 §2 shipped a host-enforced matrix that matches agent frontmatter literally but blocks required lifecycle validators and owned writes: `po`/`tech-lead`/`curator` `bash: deny`; PO missing intake_evidence / resume_brief / state.md edit allows; literal `sprints/Sxxxx/` globs; release missing duty paths.

**Approach A\***: Ship matching **active + template** `.opencode/agents/*.md` frontmatter to the **already-amended DEC-0122 §2** (sole SOT — amended in `/architecture`). Bash: po/tl/curator → `ask` (reject `allow`). PO edit adds intake_evidence/**, resume_brief.md, state.md. Replace permission-key `sprints/Sxxxx/…` → `sprints/S*/…`. Release adds release-findings, verify-work-to-release, state.md, resume_brief.md, runbook.md. Preserve deny-last + success test (c). Amend `test_us0122_*` expectations + add **7** additive `test_bug0016_*`. T-007 verifies Layer-1 ∩ write-guard does not re-deny duty globs (amend DEC-0124/0125 **only if** proven). `security`/`auto` unchanged. No companion DEC. No live OpenCode CI probe.

Out of scope: reopening US-0122 as a feature story; US-0131/US-0132; BUG-0015 (DONE — compose note only); bash:`allow`; Cursor Task port; live OpenCode CI probe; preemptively amending DEC-0124/0125; marking BUG-0016 DONE; ticking acceptance BUG-0016.

## Execute awareness (architecture critic NBs — 0 blocking)

Sovereign-critic of architecture PASS (`critic-BUG0016-architecture-20260906T185000Z-fresh`; anti_slop=10; 0 blocking). Route these resolved NBs as execute awareness — do not re-open them as work:

| Finding | Issue key | Execute awareness |
|---|---|---|
| `b0016ar-challenger-001` | `ik_bug0016_arch_edge_and_proof` | **T-007**: Prove Layer-1 ∩ write-guard does not re-deny duty globs; amend DEC-0124/0125 only if proven; keep `S*` (not `S[0-9]*`); enforce active↔template parity + intentional us0122 realign. |
| `b0016ar-architect-002` | `ik_bug0016_arch_layer_coupling` | Keep **T-anch..T-007 1:1** from architecture seeds; DEC-0122 §2 remains sole matrix SOT; execute ships frontmatter parity; CF2 runbook allow does not transfer US-0126 prose ownership. |
| `b0016ar-subtractor-003` | `ik_bug0016_arch_scope_minimal` | T-anch ceremony overlap acceptable. Do not invent DEC-0130 / `bash:allow` / live OpenCode probe. Do not mark BUG-0016 DONE. 7 markers required (not YAGNI). |

## Acceptance criteria (8) - BUG-0016 (status OPEN, acceptance unchecked per US-0045)

- **AC-1**: `po` / `tech-lead` / `curator` use `bash: ask` (not deny/allow) so validators can run under operator prompt.
- **AC-2**: PO edit allows `handoffs/intake_evidence/**`, `handoffs/resume_brief.md`, `docs/engineering/state.md`; `**` deny last; no production/code allow.
- **AC-3**: tech-lead / dev / qa / release sprint permission keys use `sprints/S*/…` (not literal `Sxxxx`).
- **AC-4**: release edit allows `sprints/S*/release-findings.md`, `handoffs/verify-work-to-release.md`, `docs/engineering/state.md`, `handoffs/resume_brief.md`, `docs/engineering/runbook.md` (keep `verify_to_release.md`).
- **AC-5**: Success test (c) preserved — non-dev roles have no production/code allow; deny-last ordering intact (static harness).
- **AC-6**: `security` (`edit: deny`, `bash: ask`) and `auto` (spawn-only Task allow-list) unchanged.
- **AC-7**: Active ↔ template `.opencode/agents/*.md` byte-identical parity after edits.
- **AC-8**: DEC-0122 §2 remains sole matrix SOT (amended in architecture; execute ships frontmatter + us0122 realign; no DEC-0130).

Adjacent duty (from R-0115 DQ8 / CF3 — covered by T-007): Layer-1 ∩ plugin write-guard does not re-deny owning-role duty globs; amend DEC-0124/0125 only if contradiction proven.

## Task summaries (8 - T-anch + T-001..T-007)

- **T-anch** (NO-OP / verification): Verify `# BUG-0016` H1 + DEC-0122 §2 amended (sole SOT) + approach A* + R-0115 DQ1–DQ8 + CF1–CF5 closed + no DEC-0130 + success test (c) prose intact. Record to `sprints/S0132/t-anch-verification.md`. NO mutation to `architecture.md` / DEC-0122 body in /execute (DEC already amended).
- **T-001** (AC-1, AC-2, AC-7): Amend `po.md` active+template: `bash: ask`; add intake_evidence/**, resume_brief.md, state.md; `**` deny last.
- **T-002** (AC-1, AC-3, AC-7): Amend `tech-lead.md` + `curator.md`: `bash: ask`; tech-lead `Sxxxx`→`S*` for sprint.md/tasks.md.
- **T-003** (AC-3, AC-7): Amend `dev.md` + `qa.md`: sprint keys `Sxxxx`→`S*`.
- **T-004** (AC-4, AC-7): Amend `release.md`: +release-findings, +verify-work-to-release, +state.md, +resume_brief.md, +runbook.md; keep verify_to_release.
- **T-005** (AC-5, AC-8): Amend `tests/us0122_contract_test.py` expectations to amended §2 matrix (+ template if paired).
- **T-006** (AC-1..AC-8): Add 7 `test_bug0016_*` markers + active↔template parity gate.
- **T-007** (DQ8 / CF3): Verify plugin write-guard does not re-deny duty globs for owning roles; document only; amend DEC-0124/0125 **only if** contradiction proven.

Execution order: T-anch → T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 (acyclic; agents first, then us0122 realign, then additive markers, then write-guard verify).

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (bash ask po/tl/curator) | T-001, T-002, T-006 (marker 1) |
| AC-2 (PO intake/resume/state) | T-001, T-006 (marker 2) |
| AC-3 (S* sprint globs) | T-002, T-003, T-006 (marker 3) |
| AC-4 (release duty paths) | T-004, T-006 (marker 4) |
| AC-5 (success test (c)) | T-anch, T-005, T-006 (marker 5) |
| AC-6 (security/auto unchanged) | T-anch, T-006 (marker 6) |
| AC-7 (active↔template parity) | T-001..T-004, T-006 (marker 7) |
| AC-8 (DEC-0122 sole SOT) | T-anch, T-005 |
| DQ8 Layer-1 ∩ write-guard | T-007 |

**Surjectivity check**: 8/8 ACs covered (each AC has at least 1 task) + DQ8 via T-007. No `PLAN_AC_COVERAGE_GAP`.

## Risks (R1–R5 — accepted from architecture)

| Risk | Severity | Mitigation in this sprint |
|---|---|---|
| R1 deny-last vs OpenCode docs order | MEDIUM → LOW | CF1: preserve deny-last; document divergence; T-anch/T-005/T-006 |
| R2 `sprints/S*` breadth | LOW | Kit naming; marker 3; keep `S*` not `S[0-9]*` |
| R3 Plugin write-guard double-deny | LOW | CF3 / T-007; amend DEC-0124/0125 only if proven |
| R4 Companion DEC second SOT | LOW | CF4: no DEC-0130; T-anch verifies |
| R5 us0122_* expectation churn | LOW | Intentional SOT realign (T-005) + additive bug0016_* (T-006) |

## Compose guards (UNCHANGED — frontmatter parity + test realign + additive markers + verify only)

| Compose target | Verification | Result |
|---|---|---|
| DEC-0122 §2 | Sole matrix SOT — already amended in /architecture; execute ships frontmatter + us0122 realign; no second matrix | compose |
| DEC-0124 / US-0124 | Write-guard UNCHANGED unless T-007 proves double-deny | compose |
| DEC-0125 / US-0125 | Command surfaces UNCHANGED | compose |
| US-0126 | Full runbook prose ownership UNCHANGED; Layer-1 runbook allow ≠ ownership transfer (CF2) | compose |
| US-0131 / US-0132 | config/model parity NOT reopened | compose |
| BUG-0015 | DONE — compose note only; permissions-only this sprint | compose |
| US-0045 / US-0048 / US-0056 | Status stays OPEN; fresh isolation; this phase mints its own proof | compose |

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
| bug_id | BUG-0016 |
| story_id | BUG-0016 |
| sprint_id | S0132 |
| orchestrator_run_id | auto-20260906-bug0016 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| fresh_context_marker | tl-BUG0016-sprint-plan-20260906T185500Z-fresh |
| timestamp | 2026-09-06T18:55:00Z (UTC) |
| model_id | composer-2.5 (CROSS_MODEL_REVIEW=1 — required) |
| evidence_ref | sprints/S0132/sprint.md, sprints/S0132/tasks.md, sprints/S0132/progress.md, sprints/S0132/uat.json, sprints/S0132/uat.md, handoffs/tl_to_dev.md (BUG-0016 prepend), docs/engineering/state.md (sprint-plan checkpoint prepend + traceability row), docs/engineering/architecture.md # BUG-0016 (not mutated), handoffs/resume_brief.md |

Prior phase proof consumed: `rp-auto-20260906-bug0016-architecture-techlead-20260906T184500Z-BUG-0016` (proof_hash=7AC851CDF1953594365AFF11B015BFD850E737F75A327FA2A02B1CCB544D5A31, ttl 2026-09-06T19:45:00Z — independent SHA-256 MATCH via critic; consumed at 2026-09-06T18:55:00Z before RUNTIME_PROOF_STALE). Sovereign-critic architecture PASS at 2026-09-06T18:50:00Z (anti_slop_aggregate=10; 0 blocking findings; 3 NBs `b0016ar-*` status=resolved).

## Runtime proof (DEC-0038)

| Field | Value |
|---|---|
| runtime_proof_id | rp-auto-20260906-bug0016-sprint-plan-techlead-20260906T185500Z-BUG-0016 |
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | BUG-0016 |
| sprint_id | S0132 |
| orchestrator_run_id | auto-20260906-bug0016 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| model_id | composer-2.5 (CROSS_MODEL_REVIEW=1 — required) |
| proof_issued_at | 2026-09-06T18:55:00Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-09-06T19:55:00Z (UTC) |
| proof_hash | F6892B96789FF471D7A97B40F80BBE59E725FB5A5DD573515D0ABC663B0A997F |
| canonical_payload | `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"composer-2.5","orchestrator_run_id":"auto-20260906-bug0016","phase_id":"sprint-plan","proof_issued_at":"2026-09-06T18:55:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260906-bug0016-sprint-plan-techlead-20260906T185500Z-BUG-0016","sprint_id":"S0132","story_id":"BUG-0016"}` |

## Decision gate

| Field | Value |
|---|---|
| decision_gate | false |
| stop_conditions_met | yes |
| missing_acceptance_criteria | none (8/8 ACs covered; 7 contract-test markers; compose guards UNCHANGED) |
| compose_guards | DEC-0122 sole SOT + DEC-0124/0125/US-0126/0131/0132/BUG-0015/0045 UNCHANGED (except intentional §2 frontmatter ship) |
| dc_check | clean (`# BUG-0016` H1 already added in /architecture) |
| task_count | 8 (within SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1 but no split needed; 1:1 seeds) |
| risks_finalized | 5/5 ACCEPTED (R1..R5) |
| approach | A* locked |
| companion_DEC | none |
| plan-verify readiness | ultra_lean — /plan-verify merged into build+verify under QA; plan-verify.json NOT written in this spawn |
| sovereign_memory_note | `assemble_sovereign_memory_digest(...)` NOT called; no mistakes.jsonl write |

## Definition of done (sprint-plan)

- [x] 8 tasks enumerated (T-anch + T-001..T-007) — within SPRINT_MAX_TASKS=12; 1:1 from architecture seeds
- [x] 8/8 ACs covered by 7 contract-test markers + compose guards (surjective) + DQ8 via T-007
- [x] Task dependency graph documented
- [x] Execute phase role matrix documented (ultra_lean — /plan-verify merged into build+verify under QA)
- [x] Compose guards UNCHANGED (except intentional frontmatter ship to amended §2)
- [x] Critic carry-ins (3 non-blocking from architecture sovereign-critic) routed as execute awareness
- [x] Isolation evidence + runtime proof emitted (model_id=composer-2.5 present)
- [x] Sprint-plan checkpoint prepended to `docs/engineering/state.md`
- [x] Sprint-plan handoff prepended to `handoffs/tl_to_dev.md`
- [x] Sprint-plan PASS prepended to `handoffs/resume_brief.md` (-> /execute)
- [x] UAT placeholders written (`uat.json` empty/pending steps, `uat.md` ACs no results)
- [x] Traceability row added to `docs/engineering/state.md` (Story=BUG-0016 | Sprint=S0132 | Tasks=T-anch+T-001..T-007 | Status=PLANNED | Evidence empty)
- [x] Backlog status OPEN (US-0045 — not mutated); AC checkboxes untouched; sprint_plan_notes appended

## Next scheduled phase

| Field | Value |
|---|---|
| next_scheduled_phase | `/execute` (role=dev per US-0069 / DEC-0051; fresh dev subagent per BUG-0006; first canonical phase of `build+verify` macro per ultra_lean; /plan-verify merged into qa per ultra_lean — qa creates plan-verify.json within build+verify). Orchestrator runs sovereign-critic of sprint-plan first (CROSS_MODEL_REVIEW=1). Do not mandate outer driver. |
| next_scheduled_role | dev |
| next_sprint_macro | build+verify (ultra_lean — plan-verify merged into qa) |
| stop_condition | STOP after sprint-plan completes; hand off via artifacts only. Orchestrator owns critic of sprint-plan then `/execute` in fresh dev subagent per BUG-0006. Do not spawn /execute or /plan-verify from this subagent. |
| artifacts_written | sprints/S0132/ (sprint.md, tasks.md, progress.md, uat.json, uat.md), docs/engineering/state.md (sprint-plan checkpoint + traceability), handoffs/tl_to_dev.md (BUG-0016 prepend), handoffs/resume_brief.md (sprint-plan PASS prepend -> /execute), docs/product/backlog.md (sprint_plan_notes append; Status OPEN) |
