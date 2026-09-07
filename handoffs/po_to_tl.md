## US-0118 Â— Work-kind classification (TL sprint-plan handoff)

- **Story**: `docs/product/backlog.md` `## US-0118 ? Work-kind classification + tiered delivery routing per story` (L3983)
- **Acceptance**: `docs/product/acceptance.md` US-0118 row L145 (12 ACs, OPEN)
- **Intake evidence**: `handoffs/intake_evidence/US-0118-intake.json` (first-intake-pack, validator `[INTAKE_EVIDENCE_VALIDATION_OK]`, all 8 topics covered, coverage_complete=true, plan_area_id=`work-kind-classifier`)
- **Phase**: sprint-plan (plan macro Â— third canonical phase within ultra_lean; research + architecture + sprint-plan merged per US-0096 / DEC-0082)
- **Verdict**: PASS (no DECISION_GATE; Sprint S0118 materialized with 10 tasks T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; AC-1..AC-12 surjective coverage 12/12; companion DEC-0118 Accepted; approach A1 locked; risks R1..R8 finalized; DC check clean; compose-do-not-amend verified 6/6)
- `orchestrator_run_id=auto-20260704-01`, `delivery_mode=ultra_lean`, `macro_phase=plan` (sprint-plan Â— third canonical phase of `plan` macro per ultra_lean)
- `fresh_context_marker=tl-US0118-sprint-plan-20260704T232400Z-fresh`, `timestamp (UTC)=2026-07-04T23:24:00Z`
- **Sprint anchor**: `sprints/S0118/sprint.md` (NEW Â— ultra_lean sprint plan; 10 tasks; AC-1..AC-12 surjective + DC resolution verified; metadata + scope + AC table + AC?task surjective coverage + task count + tasks + test markers + files to touch + files NOT to touch + compose guards UNCHANGED (23) + 6th-story cumulative byte-stability surface note + plan-verify readiness ultra_lean merge note + decision gate + sovereign memory note + risks R1..R8 + definition of done + isolation evidence + strict runtime proof + next phase)
- **Tasks anchor**: `sprints/S0118/tasks.md` (NEW Â— 10-task checklist with T-anch as NO-OP / verification; per-task coverage/risk/dependencies/files/scope/verification step; T-anch verifies `## US-0118` anchor exists at L1713 with no execute-phase write; T-001..T-009 mirror ultra_lean pattern adapted for 12 ACs + classifier lib + `/auto` integration + contract tests)
- **Architecture anchor**: `docs/engineering/architecture.md` `## US-0118 Â— Work-kind classification + tiered delivery routing per story` (L1713)
- **Companion DEC**: `decisions/DEC-0118.md` (Required ? Accepted; authored in `/architecture` phase Â— locks: work-kind enumeration `doc`/`mini`/`code` 3-tier, L8 precedence chain, `dev_environment_lib.classify_touched_files` reuse boundary, zero-overhead-when-off default `WORK_KIND_ROUTING=0`)
- **Research anchor**: `docs/engineering/research.md` `## R-0106 - US-0118 Work-kind classification + tiered delivery routing research`
- **Status**: OPEN per US-0045. **Next**: `/execute` (fresh dev subagent Â— first canonical phase of `build+verify` macro per ultra_lean; plan-verify merged into qa per ultra_lean Â— qa creates `plan-verify.json` within `build+verify`).

### Summary

Per-story **work-kind classifier** `scripts/work_kind_classify_lib.py:classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope) -> WorkKindClassification` returns `work_kind ? {doc, mini, code}` + `recommended_delivery_mode ? {standard, ultra_lean, mega_quick}` + `recommended_phase_plan` + `rationale` + `evidence_refs` (+ optional `rule_trace` via `--explain`). New default-off `WORK_KIND_ROUTING=0|1` scratchpad flag (zero overhead when off Â— early-return in `/auto` `resolve_delivery_mode` step 0 when `WORK_KIND_ROUTING != "1"`). Backlog rows gain optional `work_kind` + `recommended_delivery_mode` set at intake (operator accept/override; recorded in intake evidence bundle per US-0078 / DEC-0060). `/auto` `resolve_delivery_mode` step 0 consumes them when `DELIVERY_MODE`/`AUTO_PHASE_*` are unset (L8 precedence: explicit `DELIVERY_MODE` > explicit `AUTO_PHASE_*` > `WORK_KIND_ROUTING`-derived > current default; `start-from` always wins). `doc` ? `[intake, execute, release]`; `mini` ? `ultra_lean` or `mega_quick` (US-0096 eligibility); `code` ? `standard`. Reuses `scripts/dev_environment_lib.py:classify_touched_files()` tier A/B/C + `TIER_C_SKIP_PREFIXES` Â— import, do not reinvent (Q9 LOCKED). Deterministic pure-stdlib, no LLM, no network, no `.env` reads (Q3 LOCKED). Four `WORK_KIND_*` reason codes (Q2 LOCKED). 12 `test_us0118_*` contract test markers (Q4 LOCKED). New `### Work-kind routing keys (US-0118)` README sub-block (Q5 LOCKED Â— 6th sibling; README edits happen in `/execute`) + new `## Work-kind routing (US-0118)` runbook h2 (Q7 LOCKED). Triple-installer parity (Q10/installer manifest). US-0118 is the **first 6-cumulative-surface story** Â— prior 5 released blocks (US-0113 L2421 + US-0114 L2545 + US-0115 L2617 + US-0116 L2765 + US-0117 L2856) must remain byte-identical; US-0118 adds net-new-keys-only + cross-link pointers + reason-code-only entries to its own 6th sub-block, never edits prior released blocks.

### Sprint seeds (10 tasks within SPRINT_MAX_TASKS=12 Â— refined in `/sprint-plan`)

T-anch (architecture.md `## US-0118` anchor Â— RESOLVED in `/architecture` phase + compose-do-not-amend verification + import-contract lock; NO-OP / verification), T-001 (README umbrella `### Work-kind routing (US-0118) umbrella section` under `## Commands and workflow`), T-002 (per-feature `#### US-0118` operator subsection with route table + `## Work-kind routing (US-0118)` runbook h2 + `.cursor/commands/intake.md` step-5 hook + `.cursor/commands/auto.md` step-0 precedence clause), T-003 (`### Work-kind routing keys (US-0118)` 6th scratchpad ref sub-block under `### Full scratchpad reference (detailed)`), T-004 (`template/its_magic/README.md` one-way byte-sync), T-005 (validators Â— `validate_readme_feature_coverage.py --enforce` + `validate_doc_profile.py` + `check-user-visible-metadata.py` + `check_intake_template_parity.py`), T-006 (regression tests `pytest tests/scratchpad_example_parity_test.py -v` 4 passed; forbid edits to scratchpad + test), T-007 (NEW `scripts/work_kind_classify_lib.py` classifier lib per Q10 signature + Q9 import contract + Q3 determinism + `--explain` + `--self-test`), T-008 (`/auto` `resolve_delivery_mode` step-0 integration + `/intake` step-5 hook + `.cursor/scratchpad.md` `WORK_KIND_ROUTING=0` key + intake evidence schema extension), T-009 (NEW `tests/us0118_contract_test.py` 12 markers + `installer-owned-paths.manifest` + `WORK_KIND_ROUTING_PAIRS` parity validator). Execution order: T-anch ? T-007 ? T-008 ? T-009 ? T-001 ? T-002 ? T-003 ? T-004 ? T-005 ? T-006 (acyclic; T-007/T-008/T-009 first since they're the code/lib/tests Â— keeps README byte-stability surface clean for T-001..T-004; T-anch first since it's a NO-OP on architecture.md).

### AC mapping (12 ACs ? 10 tasks surjective Â— matches `sprints/S0118/sprint.md` + `sprints/S0118/tasks.md`)

| AC | Task(s) |
|----|---------|
| DC resolution (`## US-0118` anchor verification) | T-anch |
| AC-1 Classifier library | T-007 |
| AC-2 Classification rules | T-007 |
| AC-3 Scratchpad flag | T-001, T-002, T-003 |
| AC-4 Backlog row fields | T-008 |
| AC-5 Intake integration | T-008 |
| AC-6 `/auto` integration | T-008 |
| AC-7 Fail-closed reason codes | T-009 |
| AC-8 Compose, do not amend | T-anch, T-006 |
| AC-9 Contract tests + parity | T-009, T-006 |
| AC-10 Architecture notes | T-anch |
| AC-11 Runbook + command docs | T-002 |
| AC-12 Self-test + installer delivery | T-005, T-009 |

**Surjectivity check**: AC-1..AC-12 all covered (12/12) + DC resolution verified (T-anch). Multi-AC tasks: T-007 (AC-1+AC-2), T-008 (AC-4+AC-5+AC-6), T-009 (AC-7+AC-9+AC-12 partial), T-006 (AC-8+AC-9 indirect), T-anch (AC-8+AC-10). Every AC has =1 task. No `PLAN_AC_COVERAGE_GAP`.

### Companion DEC = DEC-0118 (Accepted)

`companion_dec=DEC-0118` (authored Accepted in `/architecture` phase at `decisions/DEC-0118.md`). US-0118 introduces a new routing primitive Â— DEC-0118 locks: (a) work-kind enumeration `doc`/`mini`/`code` 3-tier (alternatives: 2-tier doc/non-doc collapsed Â— rejected as too coarse; 4-tier doc/mini/standard/extended Â— rejected as over-engineered), (b) L8 precedence chain (explicit operator flags always win; classifier fills only the unset case), (c) `dev_environment_lib.classify_touched_files` reuse boundary (import, not rewrite Â— Q9 LOCKED), (d) zero-overhead-when-off contract (default `WORK_KIND_ROUTING=0`). Mirrors DEC-0082 (US-0096 delivery modes) / DEC-0052 (US-0070 phase selection) precedent.

### Compose guards UNCHANGED (23 Â— cumulative, same 23 as US-0117)

US-0118 is a code-bearing story but lives entirely **additive** to the compose surface Â— it adds a new flag, a new lib, new backlog row fields, a new precedence clause, a new README sub-block, and a new runbook h2. It does **not** amend any existing compose-surface feature. The 23 compose guards (cumulative Â— US-0118 adds no new family-internal guards because US-0118 is itself a single-feature story, not a family umbrella) remain UNCHANGED: US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062. US-0118 itself does NOT become a NEW compose guard (it's a routing primitive, not a guard Â— rejected; US-0118's contract is enforced by its own 12 `test_us0118_*` markers + the `WORK_KIND_ROUTING=0` zero-overhead-when-off contract).

### 6th-story cumulative byte-stability surface note

US-0118 is the **first 6-cumulative-surface story** Â— the cumulative byte-stability surface now covers **5 prior released blocks** (US-0113's `### Sovereign-loop era keys` L2421 + US-0114's `### Release & distribution keys` L2545 + US-0115's `### Integration & observability keys` L2617 + US-0116's `### Delivery & lifecycle keys` L2765 + US-0117's `### Phase & role governance keys` L2856). The cross-story byte-stability contract now scales from a quint to a sextet. US-0118's net-new content (`WORK_KIND_ROUTING` key + reason-code-only entries + cross-link pointers) is added to its own 6th sub-block; it never edits prior released blocks. `PARITY_OK <size> <size>` is the authoritative end-to-end byte-stability proof. Pattern now established as a sextet (S0113/S0114/S0115/S0116/S0117 + US-0118); contract pattern scales from quint to sextet without regression.

### Plan-verify readiness (ultra_lean merge note)

In **ultra_lean** delivery mode, `/plan-verify` is **merged into the `build+verify` macro under QA** Â— the orchestrator routes; this sprint does **not** pre-create `sprints/S0118/plan-verify.json`. The sprint-plan output is plan-verify-ready (surjective AC coverage 12/12, atomic tasks, test markers aligned, T-anch NO-OP documented) so QA can verify in one spawn within `build+verify`. QA creates `plan-verify.json` within `build+verify`.

### Risks finalized (R1..R8 Â— 8 risks)

R1 (MEDIUM) classification ambiguity ? Q1 tie-break highest tier wins; R2 (MEDIUM) precedence conflicts ? L8 + `WORK_KIND_DELIVERY_MODE_CONFLICT`; R3 (LOWÂ–MEDIUM) mega_quick overlap ? L6 eligibility gating; R4 (MEDIUM) backward compat ? Q8 early-return + contract test `test_us0118_default_off_zero_overhead`; R5 (LOWÂ–MEDIUM) operator trust ? Q3 `--explain` + `rule_trace`; R6 (LOW) reuse boundary drift ? Q9 import contract + contract test `test_us0118_classify_touched_files_reuse`; R7 (LOW) installer parity drift ? T-009 manifest; R8 (MEDIUM, NEW) cross-story byte-stability surface 6th sub-block ? T-003 net-new-keys-only + `PARITY_OK` proof never edits US-0113..US-0117 released blocks.

### Isolation evidence (US-0048 / DEC-0029) Â— mirror

- `phase_id=sprint-plan`, `role=tech-lead`, `story_id=US-0118`, `sprint_id=S0118` (NOW materialized), `orchestrator_run_id=auto-20260704-01`
- `delivery_mode=ultra_lean`, `macro_phase=plan` (sprint-plan Â— third canonical phase of `plan` macro per US-0096 / DEC-0082)
- `fresh_context_marker=tl-US0118-sprint-plan-20260704T232400Z-fresh`, `timestamp=2026-07-04T23:24:00Z` (UTC)
- `evidence_ref=docs/engineering/state.md (architecture checkpoint L300Â–L372 narrow-read), docs/engineering/architecture.md (## US-0118 section L1713Â–L1923 full read Â— Overview + Companion DEC + Approach A1 + Files to touch + Files NOT to touch + Sprint seeds + Test markers + Compose guards + DC resolution + Compose-do-not-amend + Risks + Stop conditions met + Sovereign memory note + Consequences + Evidence references + Isolation evidence + Strict runtime proof + Decision gate + Next scheduled phase), handoffs/po_to_tl.md (US-0118 architecture handoff L97Â–L164 narrow-read), docs/product/backlog.md (## US-0118 block L3983Â–L4025 narrow-read Â— 12 ACs verbatim + boundaries + related_us + intake_notes), docs/product/acceptance.md (US-0118 row L145 narrow-read Â— 12 ACs OPEN), sprints/S0117/sprint.md (full read as ultra_lean template), sprints/S0117/tasks.md (first ~120 lines read as ultra_lean tasks template), handoffs/resume_brief.md (top ~30 lines narrow-read for drain-advance prose shape)`
- Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the narrow-read files listed above (US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python SHA-256 computation for the strict runtime proof + powershell line-count computations + the artifact writes listed in this phase. No `.env` reads, no credentials access, no intake-evidence mutation.
- `assemble_sovereign_memory_digest(...)` NOT called (US-0118 documentation+code so far; existing digest context sufficient per R-0106 Â— S0113..S0117 retrospectives established reusable patterns; cross-link pointer pattern + angle-distinct narrative pattern + byte-stability contract now scale from quint to sextet).
- No write to `mistakes.jsonl` in sprint-plan phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).
- Prior phase strict proof consumed: `rp-auto-20260704-01-architecture-techlead-20260704T203000Z-US-0118` (from `docs/engineering/state.md` architecture checkpoint, unchanged).
- Current sprint-plan-phase strict proof recorded below.

### Strict runtime proof (mirror)

- `runtime_proof_id=rp-auto-20260704-01-sprint-plan-techlead-20260704T232400Z-US-0118`
- Canonical payload (sorted-key JSON per DEC-0038): `{"orchestrator_run_id":"auto-20260704-01","phase_id":"sprint-plan","proof_issued_at":"2026-07-04T23:24:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260704-01-sprint-plan-techlead-20260704T232400Z-US-0118","sprint_id":"S0118","story_id":"US-0118"}`
- `proof_hash=4a6b5b6125848f4cbb209ad5ea7623f715e3aea8572ce087850069e0a7da29e7` (SHA-256)
- `proof_ttl_seconds=3600`, `proof_ttl=2026-07-05T00:24:00Z` (UTC)

### Decision gate + next scheduled phase

- `decision_gate=false` (no DECISION_GATE; no hard stop; Sprint S0118 materialized with 10 tasks within SPRINT_MAX_TASKS=12; AC-1..AC-12 surjective coverage 12/12; companion DEC-0118 Accepted; approach A1 locked; risks R1..R8 finalized; DC check clean; compose-do-not-amend verified 6/6; 6th-story cumulative byte-stability surface LOCKED; classifier signature Q10 LOCKED; import contract Q9 LOCKED; reason codes Q2 LOCKED; 12 test markers Q4 LOCKED)
- `next_scheduled_phase=/execute` (role=dev per US-0069 / DEC-0051 phase?role matrix default; first canonical phase of `build+verify` macro per ultra_lean; plan-verify merged into qa per ultra_lean Â— qa creates `plan-verify.json` within `build+verify`)
- `next_scheduled_role=dev`
- `stop_condition=STOP after sprint-plan completes; hand off via artifacts only to /execute in fresh dev subagent (BUG-0006)`

---

## US-0118 Ã¢Â€Â” Work-kind classification (TL architecture handoff)

- **Story**: `docs/product/backlog.md` `## US-0118 ? Work-kind classification + tiered delivery routing per story` (L3983)
- **Acceptance**: `docs/product/acceptance.md` US-0118 row L145 (12 ACs, OPEN)
- **Intake evidence**: `handoffs/intake_evidence/US-0118-intake.json` (first-intake-pack, validator `[INTAKE_EVIDENCE_VALIDATION_OK]`, all 8 topics covered, coverage_complete=true, plan_area_id=`work-kind-classifier`)
- **Phase**: architecture (plan macro Ã¢Â€Â” second canonical phase within ultra_lean; research + architecture + sprint-plan merged per US-0096 / DEC-0082)
- **Verdict**: PASS (no DECISION_GATE; companion DEC-0118 authored Accepted in THIS phase; approach A1 locked; sprint seeds T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; risks R1..R8 finalized; DC check clean)
- `orchestrator_run_id=auto-20260704-01`, `delivery_mode=ultra_lean`, `macro_phase=plan`
- `fresh_context_marker=tl-US0118-architecture-20260704T203000Z-fresh`, `timestamp (UTC)=2026-07-04T20:30:00Z`
- **Architecture anchor**: `docs/engineering/architecture.md` `## US-0118 Ã¢Â€Â” Work-kind classification + tiered delivery routing per story` (L1713)
- **Companion DEC**: `decisions/DEC-0118.md` (Required Ã¢Â†Â’ Accepted; authored in THIS phase)
- **Research anchor**: `docs/engineering/research.md` `## R-0106 - US-0118 Work-kind classification + tiered delivery routing research` (L8754)
- **Status**: OPEN per US-0045. **Next**: `/sprint-plan` (fresh tech-lead subagent Ã¢Â€Â” third canonical phase of `plan` macro per ultra_lean).

### Summary

Per-story **work-kind classifier** `scripts/work_kind_classify_lib.py:classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope) -> WorkKindClassification` returns `work_kind Ã¢ÂˆÂˆ {doc, mini, code}` + `recommended_delivery_mode Ã¢ÂˆÂˆ {standard, ultra_lean, mega_quick}` + `recommended_phase_plan` + `rationale` + `evidence_refs` (+ optional `rule_trace` via `--explain`). New default-off `WORK_KIND_ROUTING=0|1` scratchpad flag (zero overhead when off Ã¢Â€Â” early-return in `/auto` `resolve_delivery_mode` step 0 when `WORK_KIND_ROUTING != "1"`). Backlog rows gain optional `work_kind` + `recommended_delivery_mode` set at intake (operator accept/override; recorded in intake evidence bundle per US-0078 / DEC-0060). `/auto` `resolve_delivery_mode` step 0 consumes them when `DELIVERY_MODE`/`AUTO_PHASE_*` are unset (L8 precedence: explicit `DELIVERY_MODE` > explicit `AUTO_PHASE_*` > `WORK_KIND_ROUTING`-derived > current default; `start-from` always wins). `doc` Ã¢Â†Â’ `[intake, execute, release]`; `mini` Ã¢Â†Â’ `ultra_lean` or `mega_quick` (US-0096 eligibility); `code` Ã¢Â†Â’ `standard`. Reuses `scripts/dev_environment_lib.py:classify_touched_files()` tier A/B/C + `TIER_C_SKIP_PREFIXES` Ã¢Â€Â” import, do not reinvent (Q9 LOCKED). Deterministic pure-stdlib, no LLM, no network, no `.env` reads (Q3 LOCKED). Four `WORK_KIND_*` reason codes (Q2 LOCKED). 12 `test_us0118_*` contract test markers (Q4 LOCKED). New `### Work-kind routing keys (US-0118)` README sub-block (Q5 LOCKED Ã¢Â€Â” 6th sibling; README edits happen in `/execute`, NOT here) + new `## Work-kind routing (US-0118)` runbook h2 (Q7 LOCKED). Triple-installer parity (Q10/installer manifest).

### Architecture anchor + approach A1 LOCKED

- **Architecture anchor**: `docs/engineering/architecture.md` `## US-0118 Ã¢Â€Â” Work-kind classification + tiered delivery routing per story` (L1713; appended after the existing `## US-0099` section at L1708).
- **Approach A1 LOCKED**: Single `### Work-kind routing (US-0118)` umbrella section + per-feature subsections + 6th scratchpad ref sub-block `### Work-kind routing keys (US-0118)` as a sibling to the US-0113..US-0117 sub-blocks (US-0113 L2421, US-0114 L2545, US-0115 L2617, US-0116 L2765, US-0117 L2856). US-0118 is the **6th-story cumulative byte-stability surface** Ã¢Â€Â” prior 5 released blocks must remain byte-identical; US-0118 adds net-new-keys-only + cross-link-pointers + reason-code-only entries to its own 6th sub-block, never edits prior released blocks. README edits happen in `/execute` (build+verify macro), NOT here Ã¢Â€Â” this phase only PROPOSES the sub-block name + cross-link targets in prose.

### Companion DEC = DEC-0118 (Required Ã¢Â†Â’ Accepted)

`companion_dec=DEC-0118` (authored Accepted in THIS phase at `decisions/DEC-0118.md`). US-0118 introduces a new routing primitive Ã¢Â€Â” DEC-0118 locks: (a) work-kind enumeration `doc`/`mini`/`code` 3-tier (alternatives: 2-tier doc/non-doc collapsed Ã¢Â€Â” rejected as too coarse; 4-tier doc/mini/standard/extended Ã¢Â€Â” rejected as over-engineered), (b) L8 precedence chain (explicit operator flags always win; classifier fills only the unset case), (c) `dev_environment_lib.classify_touched_files` reuse boundary (import, not rewrite Ã¢Â€Â” Q9 LOCKED), (d) zero-overhead-when-off contract (default `WORK_KIND_ROUTING=0`). Mirrors DEC-0082 (US-0096 delivery modes) / DEC-0052 (US-0070 phase selection) precedent.

### Sprint seeds preview (10 tasks within SPRINT_MAX_TASKS=12 Ã¢Â€Â” for `/sprint-plan` refinement)

T-anch (architecture.md `## US-0118` anchor Ã¢Â€Â” RESOLVED in THIS phase + compose-do-not-amend verification + import-contract lock), T-001 (classifier lib `scripts/work_kind_classify_lib.py` per Q10 signature), T-002 (scratchpad flag `WORK_KIND_ROUTING` + `.cursor/commands/auto.md` precedence clause), T-003 (intake integration `/intake` step 5), T-004 (`/auto` `resolve_delivery_mode` step-0 integration + early-return), T-005 (reason codes + fail-closed), T-006 (contract tests `tests/work_kind_classify_test.py` Ã¢Â€Â” 12 markers), T-007 (README + template parity `### Work-kind routing keys` sub-block Ã¢Â€Â” 6th sibling), T-008 (runbook cross-link `## Work-kind routing` h2), T-009 (regression + installer manifest + `WORK_KIND_ROUTING_PAIRS` parity validator). `/sprint-plan` may merge or split within the 12-task budget.

### DC resolution result

`dc_check=clean`. `grep "^## US-0118" docs/engineering/architecture.md` prior to this phase Ã¢Â†Â’ no matches. The `## US-0118` h1 anchor is **added in THIS `/architecture` phase** (per R-0105 Q-2 LOCKED pattern Ã¢Â€Â” T-anch is the resolution point). Cross-check against the full US-xxxx list in `docs/product/backlog.md`: no OTHER deferred `## US-xxxx` anchors remain unresolved. US-0117 was the **final deferred-candidate resolution point** (36 `## US-xxxx` h1 anchors added in US-0117's `/architecture` phase Ã¢Â€Â” 18 own + 18 deferred DC-1..DC-4); the deferral register is clean. US-0118 inherits no DC candidates from prior stories. No new DC candidates created by US-0118 (its own `## US-0118` anchor resolved HERE, not deferred). Deferral register remains clean Ã¢Â€Â” no carry-over to a successor story.

### Risks finalized (R1..R8 Ã¢Â€Â” 8 risks)

R1 (MEDIUM) classification ambiguity Ã¢Â†Â’ Q1 tie-break highest tier wins; R2 (MEDIUM) precedence conflicts Ã¢Â†Â’ L8 + `WORK_KIND_DELIVERY_MODE_CONFLICT`; R3 (LOWÃ¢Â€Â“MEDIUM) mega_quick overlap Ã¢Â†Â’ L6 eligibility gating; R4 (MEDIUM) backward compat Ã¢Â†Â’ Q8 early-return + contract test; R5 (LOWÃ¢Â€Â“MEDIUM) operator trust Ã¢Â†Â’ Q3 `--explain` + `rule_trace`; R6 (LOW) reuse boundary drift Ã¢Â†Â’ Q9 import contract + contract test; R7 (LOW) installer parity drift Ã¢Â†Â’ T-009 manifest; R8 (MEDIUM, NEW) cross-story byte-stability surface 6th sub-block Ã¢Â†Â’ T-007 net-new-keys-only + `PARITY_OK` proof never edits US-0113..US-0117 released blocks.

### Compose guards UNCHANGED (23 Ã¢Â€Â” cumulative, same 23 as US-0117)

US-0118 is a code-bearing story but lives entirely **additive** to the compose surface Ã¢Â€Â” it adds a new flag, a new lib, new backlog row fields, a new precedence clause, a new README sub-block, and a new runbook h2. It does **not** amend any existing compose-surface feature. The 23 compose guards (cumulative Ã¢Â€Â” US-0118 adds no new family-internal guards because US-0118 is itself a single-feature story, not a family umbrella) remain UNCHANGED: US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062. US-0118 itself does NOT become a NEW compose guard (it's a routing primitive, not a guard Ã¢Â€Â” rejected; US-0118's contract is enforced by its own 12 `test_us0118_*` markers + the `WORK_KIND_ROUTING=0` zero-overhead-when-off contract).

### Isolation evidence (US-0048 / DEC-0029) Ã¢Â€Â” mirror

- `phase_id=architecture`, `role=tech-lead`, `story_id=US-0118`, `sprint_id=(pending Ã¢Â€Â” created at sprint-plan)`, `orchestrator_run_id=auto-20260704-01`
- `delivery_mode=ultra_lean`, `macro_phase=plan` (architecture Ã¢Â€Â” second canonical phase of `plan` macro per US-0096 / DEC-0082)
- `fresh_context_marker=tl-US0118-architecture-20260704T203000Z-fresh`, `timestamp=2026-07-04T20:30:00Z` (UTC)
- `evidence_ref=docs/product/backlog.md (## US-0118 block L3983Ã¢Â€Â“L4025), docs/product/acceptance.md (US-0118 row L145), handoffs/po_to_tl.md (US-0118 research + discovery + intake handoffs), docs/engineering/state.md (research + discovery checkpoints + drain-advance breadcrumb), docs/engineering/research.md (R-0106 full entry L8754Ã¢Â€Â“L8904), docs/engineering/architecture.md (grep ^## US- anchors + US-0117 section L1420Ã¢Â€Â“L1566 read as template + DC anchor verification L1568Ã¢Â€Â“L1710), scripts/dev_environment_lib.py (TIER_C_SKIP_PREFIXES L117Ã¢Â€Â“L125 + classify_touched_files L321Ã¢Â€Â“L339 narrow-read for Q9 import-contract lock), its_magic/README.md (grep ### .*keys anchors only Ã¢Â€Â” no full-read), decisions/DEC-0082.md (full read as DEC-0118 template), decisions/DEC-0052.md (full read as DEC-0118 template), docs/product/backlog.md (grep ^## US- anchors for DC cross-check), handoffs/resume_brief.md (top ~30 lines narrow-read for drain-advance prose shape)`
- Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the narrow-read files listed above (US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python SHA-256 computation for the strict runtime proof + powershell line-count computations + the artifact writes listed in this phase. No `.env` reads, no credentials access, no intake-evidence mutation.
- `assemble_sovereign_memory_digest(...)` NOT called (US-0118 documentation-only so far Ã¢Â€Â” architecture phase writes prose + DEC only; existing digest context sufficient per R-0106).
- No write to `mistakes.jsonl` in architecture phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).
- Prior phase strict proof consumed: `rp-auto-20260704-01-research-techlead-20260704T200000Z-US-0118` (from `docs/engineering/state.md` research checkpoint, unchanged).
- Current architecture-phase strict proof recorded below.

### Strict runtime proof (mirror)

- `runtime_proof_id=rp-auto-20260704-01-architecture-techlead-20260704T203000Z-US-0118`
- Canonical payload (sorted-key JSON per DEC-0038): `{"orchestrator_run_id":"auto-20260704-01","phase_id":"architecture","proof_issued_at":"2026-07-04T20:30:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260704-01-architecture-techlead-20260704T203000Z-US-0118","sprint_id":"(pending)","story_id":"US-0118"}`
- `proof_hash=fd72d56bd8e8450cf830e3a4fa6164d5e3b98595c00fafa166ffd00669b1d3db` (SHA-256)
- `proof_ttl_seconds=3600`, `proof_ttl=2026-07-04T21:30:00Z` (UTC)

### Decision gate + next scheduled phase

- `decision_gate=false` (no DECISION_GATE; no hard stop; companion DEC-0118 authored Accepted in THIS phase; approach A1 locked; sprint seeds T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; risks R1..R8 finalized; DC check clean; compose-do-not-amend verified 6/6)
- `next_scheduled_phase=/sprint-plan` (role=tech-lead per US-0069 / DEC-0051 phaseÃ¢Â†Â’role matrix default; third canonical phase of `plan` macro per ultra_lean; research + architecture + sprint-plan merged into `plan` macro)
- `next_scheduled_role=tech-lead`
- `stop_condition=STOP after architecture completes; hand off via artifacts only to /sprint-plan in fresh tech-lead subagent (BUG-0006)`

---

# PO-to-TL handoffs

<!-- Archive pointer: US-0117 lifecycle handoffs (sprint-plan, architecture, research, spec) rolled over to `handoffs/archive/po-to-tl-pack-20260704-c.md` on 2026-07-04 by curator (US-0117 refresh-context terminal - final story in 5-story drain). US-0113/US-0114/US-0115 lifecycles in po-to-tl-pack-20260704-a/b.md; US-0116 lifecycle handoffs lost in git checkout HEAD recovery event (authoritative record in sprints/S0116/). Drain queue EMPTY - no next-story handoff to retain. -->

## US-0118 Ã¢Â€Â” Work-kind classification (TL research handoff)

- **Story**: `docs/product/backlog.md` `## US-0118 ? Work-kind classification + tiered delivery routing per story` (L3983)
- **Acceptance**: `docs/product/acceptance.md` US-0118 row L145 (12 ACs, OPEN)
- **Intake evidence**: `handoffs/intake_evidence/US-0118-intake.json` (first-intake-pack, validator `[INTAKE_EVIDENCE_VALIDATION_OK]`, all 8 topics covered, coverage_complete=true, plan_area_id=`work-kind-classifier`)
- **Phase**: research (plan macro Ã¢Â€Â” first canonical phase within ultra_lean; research + architecture + sprint-plan merged per US-0096 / DEC-0082)
- **Verdict**: PASS (no DECISION_GATE; 10/10 discovery open questions Q1..Q10 closed LOCKED; architecture seeds proposed for `/sprint-plan`; companion DEC-0118 to be authored in `/architecture`)
- `orchestrator_run_id=auto-20260704-01`, `delivery_mode=ultra_lean`, `macro_phase=plan`
- `fresh_context_marker=tl-US0118-research-20260704T200000Z-fresh`, `timestamp (UTC)=2026-07-04T20:00:00Z`
- **Research anchor**: `docs/engineering/research.md` `## R-0106 - US-0118 Work-kind classification + tiered delivery routing research`
- **Status**: OPEN per US-0045. **Next**: `/architecture` (fresh tech-lead subagent Ã¢Â€Â” second canonical phase of `plan` macro per ultra_lean; companion DEC-0118 to be authored there).

### Summary

Per-story **work-kind classifier** `scripts/work_kind_classify_lib.py:classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope) -> WorkKindClassification` returns `work_kind Ã¢ÂˆÂˆ {doc, mini, code}` + `recommended_delivery_mode` + `recommended_phase_plan` + `rationale` + `evidence_refs` (+ optional `rule_trace` via `--explain`). New default-off `WORK_KIND_ROUTING=0|1` scratchpad flag (zero overhead when off Ã¢Â€Â” early-return in `/auto` `resolve_delivery_mode` step 0 when `WORK_KIND_ROUTING != "1"`). Backlog rows gain optional `work_kind` + `recommended_delivery_mode` set at intake (operator accept/override; recorded in intake evidence bundle). `/auto` `resolve_delivery_mode` step 0 consumes them when `DELIVERY_MODE`/`AUTO_PHASE_*` are unset (L8 precedence: explicit `DELIVERY_MODE` > explicit `AUTO_PHASE_*` > `WORK_KIND_ROUTING`-derived > current default). `doc` Ã¢Â†Â’ `[intake, execute, release]`; `mini` Ã¢Â†Â’ `ultra_lean` or `mega_quick` (US-0096 eligibility); `code` Ã¢Â†Â’ `standard`. Reuses `scripts/dev_environment_lib.py:classify_touched_files()` tier A/B/C + `TIER_C_SKIP_PREFIXES` Ã¢Â€Â” import, do not reinvent (Q9). Deterministic pure-stdlib, no LLM, no network, no `.env` reads (Q3). Four `WORK_KIND_*` reason codes (Q2). 12 `test_us0118_*` contract test markers (Q4). New `### Work-kind routing keys (US-0118)` README sub-block (Q5) + new `## Work-kind routing (US-0118)` runbook h2 (Q7). Triple-installer parity (Q10/installer manifest).

### Closed questions Q1..Q10 (10/10 Ã¢Â€Â” all LOCKED)

| Q | Topic | Resolution (summary) | LOCK |
|---|-------|-----------|------|
| Q1 | Tie-break (mixed `docs/`+`src/`) | Highest tier wins: `code` > `mini` > `doc` (mirrors `classify_touched_files` tier_rank A>B>C) | LOCKED |
| Q2 | Reason-code names + remediation | `WORK_KIND_CLASSIFY_FAILED`, `WORK_KIND_DELIVERY_MODE_CONFLICT`, `WORK_KIND_ROUTING_DISABLED` (info), `WORK_KIND_PLAN_COVERAGE_MISSING` Ã¢Â€Â” each with remediation prose | LOCKED |
| Q3 | Determinism (stdlib vs LLM) | Deterministic pure-stdlib; `--explain` emits `rule_trace`; no network/`.env`/model | LOCKED |
| Q4 | Contract test markers | 12 `test_us0118_*` markers enumerated in `tests/work_kind_classify_test.py` | LOCKED |
| Q5 | Scratchpad reference extension | New sibling sub-block `### Work-kind routing keys (US-0118)` (6th sibling; preserves US-0113..US-0117 byte-stability) | LOCKED |
| Q6 | Template parity pairs | 6 `WORK_KIND_*` parity pairs (script, scratchpad, commands, runbook, manifest) + `WORK_KIND_ROUTING_PAIRS` validator | LOCKED |
| Q7 | Runbook cross-link anchor | New h2 `## Work-kind routing (US-0118)` (sibling to existing h2 sections) | LOCKED |
| Q8 | Backward-compat proof (`WORK_KIND_ROUTING=0`) | Contract test `test_us0118_default_off_zero_overhead` + early-return in `/auto` step 0 | LOCKED |
| Q9 | Intake-time accept/override gate | 3 new evidence fields: `work_kind`, `recommended_delivery_mode`, `work_kind_operator_decision Ã¢ÂˆÂˆ {accept, override}` | LOCKED |
| Q10 | Classifier input schema | `classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope) -> WorkKindClassification` dataclass | LOCKED |

### Architecture seeds preview (10 tasks within SPRINT_MAX_TASKS=12 Ã¢Â€Â” for `/sprint-plan` refinement)

T-anch (architecture.md `# US-0118` anchor + compose-do-not-amend verification + import-contract lock), T-001 (classifier lib `scripts/work_kind_classify_lib.py`), T-002 (scratchpad flag `WORK_KIND_ROUTING` + `.cursor/commands/auto.md` precedence clause), T-003 (intake integration `/intake` step 5), T-004 (`/auto` `resolve_delivery_mode` step-0 integration + early-return), T-005 (reason codes + fail-closed), T-006 (contract tests `tests/work_kind_classify_test.py` Ã¢Â€Â” 12 markers), T-007 (README + template parity `### Work-kind routing keys` sub-block), T-008 (runbook cross-link `## Work-kind routing` h2), T-009 (regression + installer manifest). `/sprint-plan` may merge or split within the 12-task budget.

### Companion DEC decision

**DEC-0118 required** (to be authored in `/architecture`, not here). US-0118 introduces a new routing primitive Ã¢Â€Â” companion DEC locks: (a) the work-kind enumeration decision (`doc`/`mini`/`code` 3-tier; alternatives rejected as over-/under-engineered), (b) the L8 precedence chain (explicit operator flags always win; classifier fills only the unset case), (c) the `dev_environment_lib.classify_touched_files` reuse boundary (import, not rewrite), (d) the zero-overhead-when-off contract (default `WORK_KIND_ROUTING=0`). Mirrors DEC-0082 / DEC-0052 precedent.

### Risks finalized (R1..R7 promoted + R8 added Ã¢Â€Â” 8 risks)

R1 (MEDIUM) classification ambiguity Ã¢Â†Â’ Q1 tie-break; R2 (MEDIUM) precedence conflicts Ã¢Â†Â’ L8 + `WORK_KIND_DELIVERY_MODE_CONFLICT`; R3 (LOWÃ¢Â€Â“MEDIUM) mega_quick overlap Ã¢Â†Â’ L6 eligibility gating; R4 (MEDIUM) backward compat Ã¢Â†Â’ Q8 early-return + contract test; R5 (LOWÃ¢Â€Â“MEDIUM) operator trust Ã¢Â†Â’ Q3 `--explain` + `rule_trace`; R6 (LOW) reuse boundary drift Ã¢Â†Â’ Q9 import contract + contract test; R7 (LOW) installer parity drift Ã¢Â†Â’ T-009 manifest; R8 (MEDIUM, NEW) cross-story byte-stability surface (6th sub-block) Ã¢Â†Â’ T-007 net-new-keys-only + `PARITY_OK` proof.

### Compose, do not amend (verified Ã¢Â€Â” 6/6)

| Story | README anchor | architecture.md anchor | Verification |
|-------|---------------|------------------------|--------------|
| US-0096 / DEC-0082 | L2617 + L2670 inline | `## US-0096` L1684 | Ã¢ÂœÂ“ exists Ã¢Â€Â” explicit `DELIVERY_MODE` still wins (L8) |
| US-0070 / DEC-0052 | L2856 | `## US-0070` L1572 | Ã¢ÂœÂ“ exists Ã¢Â€Â” `AUTO_PHASE_*` remains explicit override (L8) |
| US-0078 / DEC-0060 | L479 runbook | `## US-0078` L1596 | Ã¢ÂœÂ“ exists Ã¢Â€Â” evidence gate still runs before any write (L10) |
| US-0051 | L371 runbook | (no h1 anchor) | Ã¢ÂœÂ“ exists Ã¢Â€Â” classifier runs after decomposition evaluator (L10) |
| US-0069 / DEC-0051 | L2856 | `## US-0069` L1568 | Ã¢ÂœÂ“ exists Ã¢Â€Â” classifier only selects which phases run, not who |
| US-0103 | L2421 | `## US-0103` L1640 | Ã¢ÂœÂ“ exists Ã¢Â€Â” read-only consumer for audit trail |

All 6 compose targets verified present (read-only consumers of US-0118 Ã¢Â€Â” additive-only).

### DC (deferred-candidate) check

`grep "^## US-0118" docs/engineering/architecture.md` Ã¢Â†Â’ **no matches**. The `# US-0118` h1 anchor is **missing** from `architecture.md`. This is **expected** Ã¢Â€Â” the `# US-0118` anchor will be added in the `/architecture` phase (plan macro), NOT in `/research`. T-anch in the architecture seeds is the resolution point. Not appended to `handoffs/sovereign_deferrals.jsonl`.

### AC baselines (verified green)

- `python scripts/validate_readme_feature_coverage.py --repo .` Ã¢Â†Â’ `{"coverage_missing":[],"coverage_present":[],"coverage_total":0,"gaps":[],"status":"PASS"}` exit 0.
- `python -m pytest tests/scratchpad_example_parity_test.py -v` Ã¢Â†Â’ `4 passed in 0.08s` (BUG-0013 parity baseline green; do not weaken tests).

### Isolation evidence (US-0048 / DEC-0029) Ã¢Â€Â” mirror

- `phase_id=research`, `role=tech-lead`, `story_id=US-0118`, `sprint_id=(pending)`, `orchestrator_run_id=auto-20260704-01`
- `fresh_context_marker=tl-US0118-research-20260704T200000Z-fresh`, `timestamp=2026-07-04T20:00:00Z` (UTC)
- `evidence_ref=docs/product/backlog.md (## US-0118 block L3983Ã¢Â€Â“L4025), docs/product/acceptance.md (US-0118 row L145), handoffs/intake_evidence/US-0118-intake.json (full read), handoffs/po_to_tl.md (US-0118 discovery handoff L5Ã¢Â€Â“L103), docs/engineering/state.md (drain-advance breadcrumb + discovery checkpoint L84Ã¢Â€Â“L196), scripts/dev_environment_lib.py (TIER_C_SKIP_PREFIXES L117Ã¢Â€Â“L125 + TIER_A_PATTERNS L84Ã¢Â€Â“L102 + TIER_B_PATTERNS L104Ã¢Â€Â“L115 + classify_touched_files L321Ã¢Â€Â“L339), its_magic/README.md (grep anchors only Ã¢Â€Â” Delivery & lifecycle keys / Phase & role governance keys / Full scratchpad reference / Caveman mode), docs/engineering/architecture.md (grep ^## US-0096/^## US-0070/^## US-0069/^## US-0078/^## US-0103/^## US-0118 anchors only), docs/engineering/runbook.md (grep ^## h2 anchors only), .cursor/scratchpad.md (grep WORK_KIND_ROUTING/DELIVERY_MODE/AUTO_PHASE_PLAN/EARLY_RESEARCH/SPRINT_MAX_TASKS anchors only), .cursor/commands/auto.md (resolve_delivery_mode L284Ã¢Â€Â“L329 narrow-read), .cursor/commands/intake.md (grep decomposition/step 5/persistence anchors only), docs/engineering/research.md (R-0105 full read as template + R-0106 stub replacement)`
- Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the narrow-read files listed above (US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python SHA-256 computation for the strict runtime proof + the artifact writes listed in this prompt (research.md R-0106 entry, state.md research checkpoint append, po_to_tl.md research handoff prepend, resume_brief.md drain-advance append). No `.env` reads, no credentials access, no intake-evidence mutation.
- `assemble_sovereign_memory_digest(...)` NOT called (US-0118 first story of a new drain Ã¢Â€Â” US-0113..US-0117 retrospectives established reusable patterns; classifier work is code, not documentation Ã¢Â€Â” existing digest context sufficient for research).
- No write to `mistakes.jsonl` in research phase.

### Strict runtime proof (mirror)

- `runtime_proof_id=rp-auto-20260704-01-research-techlead-20260704T200000Z-US-0118`
- Canonical payload (sorted-key JSON per DEC-0038): `{"orchestrator_run_id":"auto-20260704-01","phase_id":"research","proof_issued_at":"2026-07-04T20:00:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260704-01-research-techlead-20260704T200000Z-US-0118","sprint_id":"(pending)","story_id":"US-0118"}`
- `proof_hash=3582430b9c41b432bc8822b16bfc32c3597cf6788c528507d3dd0e21adb23e9e` (SHA-256)
- `proof_ttl_seconds=3600`, `proof_ttl=2026-07-04T21:00:00Z` (UTC)

### Decision gate + next scheduled phase

- `decision_gate=false` (no DECISION_GATE; no hard stop; 10/10 open questions closed LOCKED; architecture seeds proposed; companion DEC-0118 to be authored in `/architecture`)
- `next_scheduled_phase=/architecture` (role=tech-lead per US-0069 / DEC-0051 phaseÃ¢Â†Â’role matrix default; second canonical phase of `plan` macro per ultra_lean; research + architecture + sprint-plan merged into `plan` macro)
- `next_scheduled_role=tech-lead`
- `stop_condition=STOP after research completes; hand off via artifacts only to /architecture in fresh tech-lead subagent (BUG-0006)`

---

## US-0118 Ã¢Â€Â” Work-kind classification (PO -> TL, discovery handoff)

- **Story**: `docs/product/backlog.md` `## US-0118 ? Work-kind classification + tiered delivery routing per story` (L3983)
- **Acceptance**: `docs/product/acceptance.md` US-0118 row L145 (12 ACs, OPEN)
- **Intake evidence**: `handoffs/intake_evidence/US-0118-intake.json` (first-intake-pack, validator `[INTAKE_EVIDENCE_VALIDATION_OK]`, all 8 topics covered, coverage_complete=true, plan_area_id=`work-kind-classifier`) Ã¢Â€Â” intake complete, read-only for discovery
- **Phase**: discovery (spec macro Ã¢Â€Â” second canonical phase within ultra_lean; intake + discovery merged per US-0096 / DEC-0082; intake already complete)
- **Verdict**: PASS (no DECISION_GATE; discovery locks L1..L10 captured; open questions Q1..Q10 delegated to `/research`)
- `orchestrator_run_id=auto-20260704-01`, `delivery_mode=ultra_lean`, `macro_phase=spec`
- `fresh_context_marker=po-US0118-discovery-20260704T194500Z-fresh`, `timestamp (UTC)=2026-07-04T19:45:00Z`
- **Status**: OPEN per US-0045. **Next**: `/research` (fresh tech-lead subagent Ã¢Â€Â” first canonical phase of `plan` macro per ultra_lean; `AUTO_ROLE_RESEARCH` empty Ã¢Â†Â’ default tech-lead).

### Summary

Per-story **work-kind classifier** `scripts/work_kind_classify_lib.py` returns `work_kind Ã¢ÂˆÂˆ {doc, mini, code}` + `recommended_delivery_mode` + `recommended_phase_plan`. New default-off `WORK_KIND_ROUTING=0|1` scratchpad flag (zero overhead when off). Backlog rows gain optional `work_kind` + `recommended_delivery_mode` set at intake (operator accept/override). `/auto` `resolve_delivery_mode` step 0 consumes them when `DELIVERY_MODE`/`AUTO_PHASE_*` are unset. `doc` Ã¢Â†Â’ `[intake, execute, release]`; `mini` Ã¢Â†Â’ `ultra_lean`/`mega_quick` per US-0096 eligibility; `code` Ã¢Â†Â’ `standard` (full lifecycle). Reuses `scripts/dev_environment_lib.py:classify_touched_files()` tier A/B/C + `TIER_C_SKIP_PREFIXES` precedent Ã¢Â€Â” extend, do not reinvent.

### Reuse anchor

`scripts/dev_environment_lib.py:classify_touched_files()` (L321) already classifies touched files into tier A/B/C with `TIER_C_SKIP_PREFIXES` (L117: `docs/`, `handoffs/`, `sprints/`, `decisions/`, `tests/`, `.cursor/commands/`, `template/docs/`). This is the natural seed for `doc` work-kind detection Ã¢Â€Â” extend/import, do not reinvent. Lock the import contract in `/architecture` (Q9).

### Discovery locks L1..L10 (verbatim from `docs/engineering/state.md` discovery checkpoint)

- **L1** (work_kind enumeration + recommended_delivery_mode field) Ã¢Â€Â” `work_kind Ã¢ÂˆÂˆ {"doc","mini","code"}` returned by `scripts/work_kind_classify_lib.py:classify_work_kind(...)`; each result also carries `recommended_delivery_mode Ã¢ÂˆÂˆ {"standard","ultra_lean","mega_quick"}`. Pure stdlib, no network, no `.env` reads.
- **L2** (WORK_KIND_ROUTING scratchpad flag default-off) Ã¢Â€Â” new `WORK_KIND_ROUTING=0|1` (default `0`). When `0`, zero overhead: `/auto` `resolve_delivery_mode` and intake persistence skip classifier entirely. Documented in `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` with merge-precedence note.
- **L3** (classifier inputs) Ã¢Â€Â” `classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope)`; inputs are prose + AC set + touched-file hints (names-only, no content reads) + component_scope string.
- **L4** (classifier outputs) Ã¢Â€Â” returns `WorkKindResult{work_kind, recommended_delivery_mode, recommended_phase_plan, rationale, evidence_refs}`. `recommended_phase_plan` is a list of canonical phase ids. `rationale` is a human-readable rule trace; `evidence_refs` are names-only file references.
- **L5** (`doc` route) Ã¢Â€Â” all touched files match `dev_environment_lib.TIER_C_SKIP_PREFIXES` or `*.md`/`README*` under skip prefixes Ã¢Â†Â’ `recommended_phase_plan=[intake, execute, release]` (skip discovery/research/architecture/sprint-plan/plan-verify/qa/verify-work).
- **L6** (`mini` route) Ã¢Â€Â” single component, ACs Ã¢Â‰Â¤ 3, no companion DEC required Ã¢Â†Â’ `ultra_lean` or `mega_quick` (reuse US-0096 `mega_quick` eligibility: AC Ã¢Â‰Â¤ 3, no DEC, single component Ã¢Â€Â” when eligible recommend `mega_quick`, else fall back to `ultra_lean`).
- **L7** (`code` route) Ã¢Â€Â” otherwise Ã¢Â†Â’ `standard` (or honor current `DELIVERY_MODE` if explicitly set). Full canonical lifecycle retained.
- **L8** (precedence chain) Ã¢Â€Â” explicit `DELIVERY_MODE` (US-0096) > explicit `AUTO_PHASE_*` (US-0070) > `WORK_KIND_ROUTING`-derived `recommended_delivery_mode` (US-0118, only when `WORK_KIND_ROUTING=1` AND backlog row carries `work_kind` AND higher-precedence keys unset) > current default lifecycle. `start-from` always wins. Documented in `.cursor/commands/auto.md`.
- **L9** (reason-code family prefix) Ã¢Â€Â” `WORK_KIND_*` family: `WORK_KIND_CLASSIFY_FAILED`, `WORK_KIND_DELIVERY_MODE_CONFLICT`, `WORK_KIND_ROUTING_DISABLED` (info), `WORK_KIND_PLAN_COVERAGE_MISSING`. Each emits remediation guidance in `sprints/Sxxxx/qa-findings.md` / `release-findings.md`.
- **L10** (intake-time accept/override gate) Ã¢Â€Â” `/intake` step 5 (after ACs drafted, after US-0051 decomposition evaluator, before persistence): when `WORK_KIND_ROUTING=1`, run classifier, propose `work_kind` + `recommended_delivery_mode`, present to operator for accept/override. Persist choice in backlog row + intake evidence bundle (`work_kind`, `recommended_delivery_mode`, `work_kind_operator_decision Ã¢ÂˆÂˆ {accept, override}`) per US-0078 / DEC-0060. Evidence gate still runs before any backlog/acceptance write.

### Open questions Q1..Q10 for `/research`

- **Q1** (tie-break rule): when a story touches both `docs/` and `src/` (mixed tier), which work-kind wins? Candidate: highest tier wins (`code` > `mini` > `doc` per `classify_touched_files` tier_rank A>B>C precedent). Confirm deterministic rule.
- **Q2** (exact reason-code names + remediation prose): finalize the four `WORK_KIND_*` reason codes (AC-7) and their remediation guidance text emitted in `qa-findings.md` / `release-findings.md`.
- **Q3** (classifier determinism): confirm classifier is deterministic pure-stdlib (rule-based) Ã¢Â€Â” NO LLM-assisted classification. Lock the rule trace format (`--explain` flag emitting rule trace per R5).
- **Q4** (contract test surface): enumerate `test_us0118_*` markers needed in `tests/work_kind_classify_test.py` Ã¢Â€Â” each work-kind classification, each recommended phase plan, default-off zero-overhead, precedence vs `DELIVERY_MODE`/`AUTO_PHASE_*`, operator override path, each fail-closed reason code.
- **Q5** (scratchpad reference extension): what new keys are added to which README sub-block? `WORK_KIND_ROUTING` likely lands under a new `### Work-kind routing keys` sub-block (sibling to US-0113..US-0117 sub-blocks) OR under `### Delivery & lifecycle keys` (US-0116). Recommend new sub-block to keep cross-story byte-stability surface clean.
- **Q6** (template parity scope): what `WORK_KIND_*` pairs need byte-identical sync? `scripts/work_kind_classify_lib.py` Ã¢Â†Â” `template/scripts/work_kind_classify_lib.py`; `.cursor/scratchpad.md` `WORK_KIND_ROUTING` row Ã¢Â†Â” `template/.cursor/scratchpad.local.example.md`; `check_intake_template_parity.py --scope=work-kind-routing` with `WORK_KIND_ROUTING_PAIRS` manifest.
- **Q7** (runbook cross-link anchor): `docs/engineering/runbook.md` h-level + line number target for `WORK_KIND_ROUTING` flag + operator recipe (how to force full lifecycle on a `doc` story by setting `DELIVERY_MODE=standard`).
- **Q8** (backward-compat proof): prove `WORK_KIND_ROUTING=0` is byte-identical to pre-US-0118 behavior Ã¢Â€Â” existing backlog rows without `work_kind` continue to route via current `DELIVERY_MODE`/`AUTO_PHASE_*` (no forced reclassification). Test marker `test_us0118_default_off_zero_overhead`.
- **Q9** (classifier reuse boundary): confirm `scripts/dev_environment_lib.py:classify_touched_files()` is extended/imported, NOT rewritten. Lock the import contract Ã¢Â€Â” does `work_kind_classify_lib.py` import `TIER_C_SKIP_PREFIXES` + `classify_touched_files` directly, or duplicate the constants?
- **Q10** (installer manifest rows): `installer-owned-paths.manifest` `[install_include_paths]` rows for `scripts/work_kind_classify_lib.py` + `template/scripts/work_kind_classify_lib.py` Ã¢Â€Â” confirm triple-installer parity (PS1/Bash/Python) ships the new script.

### Risks promoted to `/architecture`

- **R1** (MEDIUM) Ã¢Â€Â” Classification ambiguity (a story that touches both `docs/` and `src/`) Ã¢Â†Â’ deterministic tie-break rule needed (Q1).
- **R2** (MEDIUM) Ã¢Â€Â” Precedence conflicts when both `WORK_KIND_ROUTING=1` and `DELIVERY_MODE` are set Ã¢Â†Â’ documented precedence chain (L8) + `WORK_KIND_DELIVERY_MODE_CONFLICT` reason code.
- **R3** (LOWÃ¢Â€Â“MEDIUM) Ã¢Â€Â” `mega_quick` eligibility overlap with `mini` Ã¢Â†Â’ classifier recommends `mega_quick` only when US-0096 eligibility passes, else falls back to `ultra_lean` (L6).
- **R4** (MEDIUM) Ã¢Â€Â” Backward compatibility Ã¢Â€Â” existing backlog rows without `work_kind` must continue to route via current `DELIVERY_MODE`/`AUTO_PHASE_*` (no forced reclassification). Q8 proof required.
- **R5** (LOWÃ¢Â€Â“MEDIUM) Ã¢Â€Â” Operator trust Ã¢Â€Â” classifier must be deterministic and inspectable (`--explain` flag emitting rule trace) so operators can override with confidence.
- **R6** (LOW) Ã¢Â€Â” Reuse boundary drift Ã¢Â€Â” `dev_environment_lib.classify_touched_files` extended/imported, not rewritten (Q9); lock import contract in `/architecture`.
- **R7** (LOW) Ã¢Â€Â” Installer parity drift Ã¢Â€Â” triple-installer must ship `work_kind_classify_lib.py` byte-identical (Q10); manifest-driven single source of truth.

### Compose, do not amend (verification)

| Story | README anchor | architecture.md anchor | Verification |
|-------|---------------|------------------------|--------------|
| US-0096 / DEC-0082 | L1410 umbrella + L2617 keys + L1569 `#### US-0096` | `## US-0096` L1684 | Ã¢ÂœÂ“ exists Ã¢Â€Â” explicit `DELIVERY_MODE` still wins (L8) |
| US-0070 / DEC-0052 | L2015 `#### US-0070` + L2890 keys | `## US-0070` L1572 | Ã¢ÂœÂ“ exists Ã¢Â€Â” `AUTO_PHASE_*` remains explicit override (L8) |
| US-0078 / DEC-0060 | L2131 `#### US-0078` + L432 runbook | `## US-0078` L1596 | Ã¢ÂœÂ“ exists Ã¢Â€Â” evidence gate still runs before any write (L10) |
| US-0051 | L382 `### Intake decomposition` | (no h1 anchor) | Ã¢ÂœÂ“ exists Ã¢Â€Â” classifier runs after decomposition evaluator (L10) |
| US-0069 / DEC-0051 | L1996 `#### US-0069` + L2876 keys | `## US-0069` L1568 | Ã¢ÂœÂ“ exists Ã¢Â€Â” classifier only selects which phases run, not who |
| US-0103 | L982 `#### US-0103` + L2421 keys | `## US-0103` L1640 | Ã¢ÂœÂ“ exists Ã¢Â€Â” read-only consumer for audit trail |

All 6 compose targets verified present (read-only consumers of US-0118 Ã¢Â€Â” their architectural surfaces are NOT edited by US-0118).

### DC (deferred-candidate) check

`grep "^## US-0118" docs/engineering/architecture.md` Ã¢Â†Â’ **no matches**. The `## US-0118` h1 anchor is **missing** from `architecture.md`. This is **expected** Ã¢Â€Â” the `## US-0118` anchor will be added in the `/architecture` phase (plan macro), NOT in `/discovery` (spec macro). No action required here. Not appended to `handoffs/sovereign_deferrals.jsonl`.

### Fail-closed reason codes (proposed, carried from intake handoff)

`WORK_KIND_CLASSIFY_FAILED`, `WORK_KIND_DELIVERY_MODE_CONFLICT`, `WORK_KIND_ROUTING_DISABLED` (info), `WORK_KIND_PLAN_COVERAGE_MISSING`. Finalize names + remediation prose in `/research` (Q2).

### Isolation evidence (US-0048 / DEC-0029) Ã¢Â€Â” mirror

- `phase_id=discovery`, `role=po`, `story_id=US-0118`, `sprint_id=(pending)`, `orchestrator_run_id=auto-20260704-01`
- `fresh_context_marker=po-US0118-discovery-20260704T194500Z-fresh`, `timestamp=2026-07-04T19:45:00Z` (UTC)
- `evidence_ref=docs/product/backlog.md (US-0118 block L3983Ã¢Â€Â“L4022 narrow-read), docs/product/acceptance.md (US-0118 row L145 narrow-read), handoffs/intake_evidence/US-0118-intake.json (full read), handoffs/po_to_tl.md (L1Ã¢Â€Â“L40 US-0118 intake handoff narrow-read), docs/engineering/state.md (drain-advance materialization breadcrumb L84Ã¢Â€Â“L101 narrow-read), .cursor/skills/its-magic/SKILL.md (full read), scripts/dev_environment_lib.py (TIER_C_SKIP_PREFIXES L117Ã¢Â€Â“L125 + classify_touched_files L321Ã¢Â€Â“L339 narrow-read), its_magic/README.md (grep US-0096/US-0070/US-0078/US-0051/US-0069/US-0103 anchors only), docs/engineering/architecture.md (grep ^## US-* anchors only), .cursor/commands/discovery.md (full read), docs/product/backlog.md (US-0108 discovery_notes L3856Ã¢Â€Â“L3888 narrow-read for L1..L10 pattern), docs/engineering/research.md (grep R-0106 anchor only), handoffs/resume_brief.md (L1Ã¢Â€Â“L40 narrow-read for drain-advance prose shape)`
- PO subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the narrow-read files listed above (US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + powershell SHA-256 computation for the strict runtime proof + the artifact writes listed in this prompt. No `.env` reads, no credentials access, no intake-evidence mutation.
- `assemble_sovereign_memory_digest(...)` NOT called (US-0118 first story of a new drain Ã¢Â€Â” US-0113..US-0117 retrospectives established reusable patterns; classifier work is code, not documentation Ã¢Â€Â” existing digest context sufficient for discovery).
- No write to `mistakes.jsonl` in discovery phase.

### Strict runtime proof (mirror)

- `runtime_proof_id=rp-auto-20260704-01-discovery-po-20260704T194500Z-US-0118`
- Canonical payload (sorted-key JSON per DEC-0038): `{"orchestrator_run_id":"auto-20260704-01","phase_id":"discovery","proof_issued_at":"2026-07-04T19:45:00Z","proof_ttl_seconds":"3600","role":"po","runtime_proof_id":"rp-auto-20260704-01-discovery-po-20260704T194500Z-US-0118","sprint_id":"(pending)","story_id":"US-0118"}`
- `proof_hash=17b2339eb039a4854a8ba347f49b649626cf224aa48cd308914bda82d49b6488` (SHA-256)
- `proof_ttl_seconds=3600`, `proof_ttl=2026-07-04T20:45:00Z` (UTC)

### Decision gate + next scheduled phase

- `decision_gate=false` (no DECISION_GATE; no hard stop; discovery locks captured; open questions delegated to `/research`)
- `next_scheduled_phase=/research` (role=tech-lead per US-0069 / DEC-0051 phaseÃ¢Â†Â’role matrix default Ã¢Â€Â” `AUTO_ROLE_RESEARCH` is empty so default tech-lead applies; first canonical phase of `plan` macro per ultra_lean; research + sprint-plan merged into `plan` macro)
- `next_scheduled_role=tech-lead`
- `stop_condition=STOP after discovery completes; hand off via artifacts only to /research in fresh tech-lead subagent (BUG-0006)`

---

## US-0118 Ã¢Â€Â” Work-kind classification + tiered delivery routing per story (PO -> TL)

- **Story**: `docs/product/backlog.md` `## US-0118 ? Work-kind classification + tiered delivery routing per story`
- **Acceptance**: `docs/product/acceptance.md` US-0118 (12 ACs, OPEN)
- **Intake evidence**: `handoffs/intake_evidence/US-0118-intake.json` (first-intake-pack, validator `[INTAKE_EVIDENCE_VALIDATION_OK]`, all 8 topics covered, coverage_complete=true, plan_area_id=`work-kind-classifier`)
- **Status**: OPEN per US-0045. **Next**: `/discovery` (fresh PO) for US-0118.
- **Operator pain (verbatim)**: "wir mÃƒÂ¼ssen beim erstellen von userstories bzw abarbeiten erkennen ob es coding betrifft oder doku / text schreiben oder mini implementierungen welche keine komplette phasen durchlÃƒÂ¤ufe benÃƒÂ¶tigen. wie zb Architecture, qa, etc... aktuell laufen wir zb den ganzen overhead durch nur um ein readme zu aktualisieren."

### Scope summary
Per-story **work-kind classifier** `scripts/work_kind_classify_lib.py` returns `work_kind Ã¢ÂˆÂˆ {doc, mini, code}` + `recommended_delivery_mode` + `recommended_phase_plan`. New default-off `WORK_KIND_ROUTING=0|1` scratchpad flag (zero overhead when off). Backlog rows gain optional `work_kind` + `recommended_delivery_mode` set at intake (operator accept/override). `/auto` `resolve_delivery_mode` step 0 consumes them when `DELIVERY_MODE`/`AUTO_PHASE_*` are unset. `doc` -> `[intake, execute, release]`; `mini` -> `ultra_lean`/`mega_quick`; `code` -> `standard`.

### Reuse anchor
`scripts/dev_environment_lib.py:classify_touched_files()` already classifies touched files into tier A/B/C with `TIER_C_SKIP_PREFIXES` (`docs/`, `handoffs/`, `sprints/`, `decisions/`, `tests/`, `.cursor/commands/`, `template/docs/`). This is the natural seed for `doc` work-kind detection Ã¢Â€Â” extend, do not reinvent.

### Compose, do not amend
- **US-0096 / DEC-0082** (delivery modes): US-0118 makes routing per-story + derived; explicit `DELIVERY_MODE` still wins.
- **US-0070 / DEC-0052** (phase selection): `AUTO_PHASE_*` keys remain the explicit override; classifier only fills the unset case.
- **US-0078 / DEC-0060** (intake evidence): classifier proposal + operator decision recorded in the evidence bundle; gate still runs before any write.
- **US-0051** (decomposition): classifier runs after the decomposition evaluator.
- **US-0069 / DEC-0051** (phase->role matrix): unchanged; classifier only selects which phases run, not who runs them.
- **US-0103** (AI decision ledger): read-only consumer for audit trail.

### Risks to carry to /discovery and /architecture
- **R1**: Classification ambiguity (a story that touches both `docs/` and `src/`) -> deterministic tie-break rule needed (highest tier wins? `code` wins?).
- **R2**: Precedence conflicts when both `WORK_KIND_ROUTING=1` and `DELIVERY_MODE` are set -> documented precedence chain + `WORK_KIND_DELIVERY_MODE_CONFLICT` reason code.
- **R3**: `mega_quick` eligibility overlap with `mini` -> classifier should recommend `mega_quick` only when US-0096 eligibility passes, else fall back to `ultra_lean`.
- **R4**: Backward compatibility Ã¢Â€Â” existing backlog rows without `work_kind` must continue to route via current `DELIVERY_MODE`/`AUTO_PHASE_*` (no forced reclassification).
- **R5**: Operator trust Ã¢Â€Â” classifier must be deterministic and inspectable (`--explain` flag emitting rule trace) so operators can override with confidence.

### Fail-closed reason codes (proposed)
`WORK_KIND_CLASSIFY_FAILED`, `WORK_KIND_DELIVERY_MODE_CONFLICT`, `WORK_KIND_ROUTING_DISABLED` (info), `WORK_KIND_PLAN_COVERAGE_MISSING`.

### Handoff
- TL: take this handoff into `/discovery` (fresh PO) then `/architecture`. Lock the classifier contract, precedence chain, and the `dev_environment_lib` reuse boundary before `/sprint-plan`.
- Research stub: `R-0106` in `docs/engineering/research.md`.

## Intake handoff — BUG-0015 and BUG-0016 OpenCode /auto dispatch + Layer-1 permission matrix

- **Phase completed**: intake (`/intake bug`). **Role**: po. **Bugs**: BUG-0015 (primary), BUG-0016 (also OPEN). **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp**: 2026-09-06T13:35:00Z. **Fresh marker**: `po-BUG0015-BUG0016-intake-20260906T133500Z-fresh`.
- **Writer**: `writer_id=po-cursor-20260906-opencode-bugs`, `intake_run_id=cursor-20260906-BUG0015-0016-intake`.
- **Routing**: argv `/intake bug` wins over scratchpad `INTAKE_WORK_ITEM_KIND=story`. `selected_pack=small-intake-pack`. `INTAKE_GUIDED_MODE=1`.
- **Evidence**:
  - `handoffs/intake_evidence/BUG-0015-intake-20260906.json` — `[INTAKE_EVIDENCE_VALIDATION_OK]`
  - `handoffs/intake_evidence/BUG-0016-intake-20260906.json` — `[INTAKE_EVIDENCE_VALIDATION_OK]`
  - `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` — `[BUG_VALIDATION_OK]`
  - `python scripts/intake_bug_resume_brief_refresh.py ... --bug-id BUG-0015` — `[INTAKE_BUG_RESUME_BRIEF_REFRESH_OK]` (primary continuation; BUG-0016 also OPEN)
- **Operator ask**: Persist two OPEN defects — (1) OpenCode `/auto` never starts orchestrator plugin dispatch (STOP); (2) OpenCode Layer-1 role permissions block legitimate lifecycle duties (audit all roles).
- **Decomposition (recommended)**: two independently valuable bugs — dispatch wiring vs permission matrix/duty mismatch. Do not fold into US-0131/US-0132.
- **Alternatives considered**:
  1. **Two OPEN bugs** (recommended) — separate dispatch vs permissions; independently testable.
  2. **Fold into US-0131** — rejected (wrong scope: config/model parity, not runtime dispatch/permissions).
  3. **Amend DEC-0122 only without bugs** — rejected (no OPEN work item / no acceptance row).
- **BUG-0015 (primary fix target)**: `.opencode/commands/auto.md` is STOP-only; `.opencode/plugins/orchestrator.ts` exports `spawnPhase` from `setup()` return API and hooks `execute.before` write-guard only — no command/event hook invokes spawn loop on `/auto`. Compose US-0124/US-0125 ships surfaces but runtime linkage gap remains.
- **BUG-0016 (permission audit — all roles)**:

| Role | Issue |
|------|--------|
| `po` | `bash: deny` blocks mandatory validators / resume-brief refresh; edit misses `handoffs/intake_evidence/**` and bug-intake `handoffs/resume_brief.md` (DEC-0069). |
| `tech-lead` | `bash: deny` blocks research/architecture validators; literal `sprints/Sxxxx/` likely fails real ids. |
| `dev` | `bash: ask` OK-ish; same `Sxxxx` glob risk; confirm owned paths vs execute ownership. |
| `qa` | `bash: ask` OK-ish; literal `Sxxxx` glob risk. |
| `release` | `bash: ask` OK-ish; may miss `sprints/*/release-findings.md` (scope carefully). |
| `curator` | `bash: deny` blocks `enforce-triad-hot-surface.py` / materialize scripts for `/refresh-context`. |
| `security` | `edit: deny` + `bash: ask` matches DEC-0122 v1 — in-contract unless contradiction found. |
| `auto` | spawn-only OK for Task path; OpenCode still broken by BUG-0015. |

- **Duplicate check**: Distinct from BUG-0006, BUG-0012, US-0122 DONE, US-0131/US-0132 OPEN (do not expand those stories).
- **Risks**: R1 — OpenCode host plugin API may lack a clean `/auto` hook (fail closed with `OPENCODE_*`); R2 — widening bash/edit for non-dev roles must preserve success test (c) production/code deny; R3 — DEC-0122 amendment + `test_us0122_*` / template parity churn; R4 — fixing permissions without BUG-0015 still leaves `/auto` dead.
- **Isolation**: `phase_id=intake`; `role=po`; `fresh_context_marker=po-BUG0015-BUG0016-intake-20260906T133500Z-fresh`; `timestamp=2026-09-06T13:35:00Z`; `evidence_ref=docs/product/backlog.md ## Bug issues BUG-0015 + BUG-0016, docs/product/acceptance.md bug rows, handoffs/resume_brief.md, this handoff`.
- **Hot-surface note**: Full narrative also in `handoffs/archive/po-to-tl-pack-20260906.md`. Appended (not prepended) so triad oldest-prefix rollover retains the newest section under `PO_TO_TL_HOT_MAX_LINES`.
- **Status**: both OPEN per US-0045. **Next**: `/discovery` (fresh **po**) for **BUG-0015**, or `/auto bug-target=BUG-0015`. Do not run architecture/execute from this intake chat. STOP after intake.

## Discovery handoff — BUG-0015 OpenCode `/auto` dispatch wiring gap

- **Phase completed**: discovery. **Role**: po. **Bug**: BUG-0015 only. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp (UTC)**: 2026-09-06T14:05:00Z. **Fresh marker**: `po-BUG0015-discovery-20260906T140049Z-fresh`.
- **Orchestrator**: `orchestrator_run_id=auto-20260906-bug0015`, `delivery_mode=ultra_lean`, macro=`spec` (intake already DONE — not re-intaken).
- **Sibling boundary**: BUG-0016 remains OPEN and out of scope this segment (permissions only).
- **Gap confirmed (narrow-read)**: `.opencode/commands/auto.md` body is STOP-only; `.opencode/plugins/orchestrator.ts` exports `spawnPhase` from `setup()` return API and registers only `tool.hook("execute.before")` write-guard — no command/event hook starts the spawn loop on `/auto`.

### Discovery locks D1–D7

| ID | Lock |
|----|------|
| **D1** | Dispatch attaches primarily via **plugin command/event hook** that invokes the spawn loop when `/auto` starts. Thin `auto.md` stays dispatch-only (DEC-0125 DQ5). Agent prompt may restate "plugin owns spawn" but is **not** sole dispatch (success test (a) / BUG-0006). Returning `spawnPhase` from `setup()` alone is insufficient. Exact OpenCode v2 hook name → DQ1. |
| **D2** | Missing / non-function `session.create` → fail-closed **`OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`**. No in-band roleplay; no Cursor Task port; operator-visible stop with reason code. |
| **D3** | Python `scripts/auto_outer_driver.py` remains stop-matrix SOT; plugin keeps `dispatchStopMatrix` subprocess; no TS reimplementation (DEC-0124 §6). Headless `opencode run --agent auto` compose unchanged — this bug is interactive `/auto` → spawn linkage. |
| **D4** | Each spawn MUST emit `IsolationEvidence` (`parentID`, `sessionID`, `role`, `phase_id`, `timestamp`, `fresh_context_marker`) with `sessionID !== parentID`; null/throw/identical-id → **`OPENCODE_SUBTASK_IGNORED`**; persist per US-0023/US-0048/BUG-0006. |
| **D5** | Additive `test_bug0015_*` (and/or amend us0124 markers) via mock-ctx harness — assert dispatch hook registration + `/auto` entry invokes `spawnPhase`; static `auto.md` ≤20 lines / no spawn literals; **no live OpenCode probe in CI**. |
| **D6** | BUG-0016 permissions OUT OF SCOPE; US-0131/US-0132 config/model OUT OF SCOPE; do not amend DEC-0122 Layer-1 matrix here; compose US-0124/US-0125 without reopening DONE ACs. |
| **D7** | Research questions DQ1–DQ7 below → `/research` authors **R-0114** (compose R-0109; do not wipe). |

### Research questions DQ1–DQ7 (for `/research`)

1. **DQ1**: Exact OpenCode v2 plugin API surface to detect `/auto` command invocation (event/hook name, args, lifecycle) — cite current docs.
2. **DQ2**: Should the spawn loop live entirely inside plugin `setup` callbacks vs host-invoked exported `spawnPhase` after command dispatch — single-owner rule?
3. **DQ3**: First-phase selection after `/auto` on OpenCode — `resume_brief` / argv / scratchpad / US-0087 bug-queue compose?
4. **DQ4**: How do interactive plugin path and headless `opencode run --auto` share one entry without duplicate spawn (DEC-0125 R3)?
5. **DQ5**: Isolation-evidence persistence target for OpenCode-spawned phases (`state.md` only vs additional plugin-local) — minimum contract?
6. **DQ6**: Minimal contract-test inventory for dispatch wiring without live host (markers, harness extensions)?
7. **DQ7**: Does the fix require amending DEC-0124/DEC-0125 vs additive companion DEC-0015-bug / `# BUG-0015` architecture section only?

### Runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260906-bug0015-discovery-po-20260906T140500Z-BUG-0015`
- `proof_hash=700734379DE4CFE3B0509DB39E8F3208DFAEC8ADB2BA475EA8CDB9C0AF37C83F`
- `proof_ttl=2026-09-06T15:05:00Z`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"spec","model_id":"composer-2.5","orchestrator_run_id":"auto-20260906-bug0015","phase_id":"discovery","proof_issued_at":"2026-09-06T14:05:00Z","proof_ttl_seconds":3600,"role":"po","runtime_proof_id":"rp-auto-20260906-bug0015-discovery-po-20260906T140500Z-BUG-0015","sprint_id":"pending","story_id":"BUG-0015"}`

### Isolation + stop

- `phase_id=discovery`, `role=po`, `bug_id=BUG-0015`, `fresh_context_marker=po-BUG0015-discovery-20260906T140049Z-fresh`
- `evidence_ref=docs/product/vision.md ## Discovery Notes — BUG-0015; docs/product/backlog.md ### BUG-0015 discovery_notes; handoffs/intake_evidence/BUG-0015-intake-20260906.json; .opencode/commands/auto.md; .opencode/plugins/orchestrator.ts; docs/engineering/state.md discovery checkpoint; handoffs/resume_brief.md`
- **Status**: BUG-0015 remains **OPEN**. **Next**: `/research` in fresh **tech-lead** subagent. Do not spawn research from this discovery chat. STOP.

## Discovery handoff — US-0131 Cross-host Its-Magic runtime configuration and parity

- **Phase completed**: discovery. **Role**: po. **Story**: US-0131 only. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp (UTC)**: 2026-09-07T19:15:00Z. **Fresh marker**: `po-US0131-discovery-20260907T191500Z-fresh`.
- **Orchestrator**: `orchestrator_run_id=auto-20260907-us0131`, `delivery_mode=ultra_lean`, macro=`spec` (intake already PASS — not re-intaken).
- **Sibling boundary**: **US-0132** OPEN (model configuration contract) — OUT OF SCOPE; do not expand into US-0132 ACs. **BUG-0015/BUG-0016** DONE — do not reopen.
- **Gap confirmed**: shared lifecycle/governance settings still resolve through Cursor-path scratchpad readers; OpenCode-only installs must not require `.cursor/`; host-specific capabilities must fail/skip deterministically.

### Discovery locks D1–D10

| ID | Lock |
|----|------|
| **D1** | Host-neutral typed config contract for shared runtime/governance (no credentials / provider secrets / vendor slugs in templates). |
| **D2** | Cursor scratchpad (DEC-0055 Model B + DEC-0039 local protection) = **compatibility adapter** into the neutral contract — not the sole SOT after migration. |
| **D3** | OpenCode-only install resolves all shared settings without `.cursor/scratchpad.md` or `.cursor/scratchpad.local.md`. |
| **D4** | Shared Python validators/outer-driver/triad/state/handoff scripts accept resolved config explicitly — no silent `.cursor` hardcode for host-neutral behavior. |
| **D5** | Cursor-only vs OpenCode-only capabilities classified; unavailable → fail/skip with reason codes; no silent unsupported parity; no Cursor command/rule body clones. |
| **D6** | `--host both` has one deterministic precedence; no conflicting duplicate writes; independent host-local overrides where schemas differ. |
| **D7** | Installer delivers examples to selected host; preserves local operator files; never overwrites active scratchpad/config. |
| **D8** | Contract tests for cursor-only / opencode-only / both + docs for precedence, migration, reason codes (active + template). |
| **D9** | **US-0132 boundary** — model catalogs / `MODEL_*` / materializers out of scope; no third `model.json` SOT. |
| **D10** | Compose US-0073/DEC-0055, DEC-0039, US-0121..US-0126, US-0092, US-0069; do not amend DEC-0086/0087/0123; do not reopen BUG-0015/0016. |

### Research questions DQ1–DQ10 (for `/research` → expect **R-0116**)

1. **DQ1**: Canonical host-neutral config path (must not require `.cursor/` on OpenCode-only).
2. **DQ2**: Typed schema + versioning + fail-closed codes for malformed/missing shared keys.
3. **DQ3**: Cursor scratchpad merge → neutral resolver mapping (preserve DEC-0055/0039).
4. **DQ4**: OpenCode-only shared-settings adapter (prefer dedicated kit config over dumping into `opencode.json` model/permission schema).
5. **DQ5**: Complete `.cursor/scratchpad*` hardcode inventory + injection API shape.
6. **DQ6**: Exact `--host both` precedence table.
7. **DQ7**: Finalize shared / Cursor-only / OpenCode-only / skip-vs-fail matrix + reason-code family.
8. **DQ8**: Installer/manifest example delivery surfaces per `--host cursor|opencode|both`.
9. **DQ9**: Minimal `test_us0131_*` inventory + fixtures (no live OpenCode CI probe).
10. **DQ10**: Docs anchors (runbook/README/auto-orchestration-reference) for precedence/migration/unsupported capability.

### Config-surface / design refs

- OpenCode: https://opencode.ai/v2/docs/config/ — `opencode.json{,c}`, `.opencode/`
- Cursor: DEC-0055 Model B scratchpad pair; DEC-0039 local preservation
- Script hardcodes: `scripts/auto_outer_driver.py`, `scripts/opencode_auto_bridge.py`, `scripts/enforce-triad-hot-surface.py`, `scripts/dev_environment_lib.py`, `scripts/caveman_compress_input.py`
- Vision: `docs/product/vision.md` `## Discovery Notes — US-0131`
- Intake (read-only): `handoffs/intake_evidence/US-0131-0132-intake-20260906.json`

### Runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260907-us0131-discovery-po-20260907T191500Z-US-0131`
- `proof_hash=7BC1124AE3DE20960D42D6FE750B9A9F4412B42D20798245BA452C1573BE83AE`
- `proof_ttl=2026-09-07T20:15:00Z`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"spec","model_id":"composer-2.5","orchestrator_run_id":"auto-20260907-us0131","phase_id":"discovery","proof_issued_at":"2026-09-07T19:15:00Z","proof_ttl_seconds":3600,"role":"po","runtime_proof_id":"rp-auto-20260907-us0131-discovery-po-20260907T191500Z-US-0131","sprint_id":"none","story_id":"US-0131"}`

### Isolation + stop

- `phase_id=discovery`, `role=po`, `story_id=US-0131`, `model_id=composer-2.5`, `fresh_context_marker=po-US0131-discovery-20260907T191500Z-fresh`
- `evidence_ref=docs/product/vision.md ## Discovery Notes — US-0131; docs/product/backlog.md ## US-0131 discovery_notes; handoffs/intake_evidence/US-0131-0132-intake-20260906.json; docs/engineering/state.md discovery checkpoint; handoffs/resume_brief.md`
- **Status**: US-0131 remains **OPEN**. **Next**: `/research` in fresh **tech-lead** subagent. Do not spawn research from this discovery chat. STOP.

---

## Research handoff — US-0131 Cross-host Its-Magic runtime configuration and parity

- **Phase completed**: research. **Role**: tech-lead. **Story**: US-0131 only. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp (UTC)**: 2026-09-07T19:25:00Z. **Fresh marker**: `tl-US0131-research-20260907T192500Z-fresh`.
- **Orchestrator**: `orchestrator_run_id=auto-20260907-us0131`, `delivery_mode=ultra_lean`, macro=`plan` (research = first of research+architecture+sprint-plan).
- **Sibling boundary**: **US-0132** OPEN — OUT OF SCOPE (model catalogs / `MODEL_*` / materializers). **BUG-0015/BUG-0016** DONE — do not reopen.
- **Research anchor**: `docs/engineering/research.md` **`## R-0116`** (DQ1–DQ10 LOCKED; do not renumber R-0115).

### DQ locks (summary for architecture)

| DQ | Lock |
|----|------|
| **DQ1** | Host-neutral path **`.its-magic/config{,.local,.example}.json`** — no `.cursor/` required on OpenCode-only |
| **DQ2** | JSON `schema_version` + `shared` KEY map; fail-closed `HOST_CONFIG_*` |
| **DQ3** | Cursor scratchpad DEC-0055/0039 = compatibility adapter into same `shared` namespace |
| **DQ4** | OpenCode-only reads `.its-magic/` only; **forbid** dumping kit keys into `opencode.json` |
| **DQ5** | `scripts/host_runtime_config_lib.py:resolve_runtime_config` migrates shared-kernel hardcodes |
| **DQ6** | Both-host precedence: kit-local > cursor-local > kit-baseline > cursor-baseline > example > defaults |
| **DQ7** | Shared / Cursor-only / OpenCode-only / US-0132 matrix + reason-code family |
| **DQ8** | Kernel deliver `.its-magic/config.example.json`; never overwrite locals |
| **DQ9** | 10 `test_us0131_*` static/fixture markers (no live OpenCode probe) |
| **DQ10** | Runbook h2 `## Cross-host runtime configuration (US-0131)` + README + auto-orch cross-link |

### Architecture seeds

- Approach **A1** recommended (`.its-magic/` + LegacyScratchpadAdapter + resolver migration). Reject A2 (scratchpad-only), A3 (`opencode.json` store).
- Companion **DEC-0131** Required → Accepted in `/architecture`.
- Author `# US-0131` architecture H1; do not expand US-0132 ACs.

### Runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260907-us0131-research-techlead-20260907T192500Z-US-0131`
- `proof_hash=7DB90B2B345D7C4E84F0A7C78E99A662C7FF308271415ECC5F7DFEAB774BE2BE`
- `proof_ttl=2026-09-07T20:25:00Z`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"composer-2.5","orchestrator_run_id":"auto-20260907-us0131","phase_id":"research","proof_issued_at":"2026-09-07T19:25:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260907-us0131-research-techlead-20260907T192500Z-US-0131","sprint_id":"none","story_id":"US-0131"}`
- Consumed discovery proof: `rp-auto-20260907-us0131-discovery-po-20260907T191500Z-US-0131` / `7BC1124AE3DE20960D42D6FE750B9A9F4412B42D20798245BA452C1573BE83AE` — RUNTIME_PROOF_VALID (MATCH before TTL)

### Isolation + stop

- `phase_id=research`, `role=tech-lead`, `story_id=US-0131`, `model_id=composer-2.5`, `fresh_context_marker=tl-US0131-research-20260907T192500Z-fresh`
- `evidence_ref=docs/engineering/research.md ## R-0116; docs/product/backlog.md ## US-0131 research_notes; handoffs/po_to_tl.md Discovery handoff US-0131; docs/engineering/state.md discovery+critic checkpoints; docs/product/vision.md ## Discovery Notes — US-0131`
- **Status**: US-0131 remains **OPEN**. **Next**: `/architecture` in fresh **tech-lead** subagent. Do not spawn architecture from this research chat. STOP.

---

## Architecture handoff — US-0131 Cross-host Its-Magic runtime configuration and parity

- **Phase completed**: architecture. **Role**: tech-lead. **Story**: US-0131 only. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp (UTC)**: 2026-09-07T19:35:00Z. **Fresh marker**: `tl-US0131-architecture-20260907T193500Z-fresh`.
- **Orchestrator**: `orchestrator_run_id=auto-20260907-us0131`, `delivery_mode=ultra_lean`, macro=`plan` (architecture = second of research+architecture+sprint-plan).
- **Sibling boundary**: **US-0132** OPEN — OUT OF SCOPE. **BUG-0015/BUG-0016** DONE — do not reopen.
- **Architecture anchor**: `docs/engineering/architecture.md` **`# US-0131`**
- **Companion DEC**: `decisions/DEC-0131.md` (**Accepted**)
- **Research anchor**: `docs/engineering/research.md` **`## R-0116`** (DQ1–DQ10 LOCKED)

### Approach A1 LOCKED

Host-neutral `.its-magic/config{,.local,.example}.json` SOT + Cursor DEC-0055/0039 LegacyScratchpadAdapter (Model B pre-merge then DQ6 interleave) + `host_runtime_config_lib.resolve_runtime_config` shared-kernel injection. OpenCode-only without `.cursor/`. Forbid kit keys in `opencode.json`. Schema v1 + `HOST_CONFIG_*` family. 10 `test_us0131_*` markers. Sprint seeds T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12.

### Runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260907-us0131-architecture-techlead-20260907T193500Z-US-0131`
- `proof_hash=F31B058CC5CDEAF68EDD2F53F4EF790D1845CE842E2B16057247CF5FE4170C4C`
- `proof_ttl=2026-09-07T20:35:00Z`
- Consumed research proof: `rp-auto-20260907-us0131-research-techlead-20260907T192500Z-US-0131` / `7DB90B2B345D7C4E84F0A7C78E99A662C7FF308271415ECC5F7DFEAB774BE2BE` — RUNTIME_PROOF_VALID

### Isolation + stop

- `phase_id=architecture`, `role=tech-lead`, `story_id=US-0131`, `model_id=composer-2.5`, `fresh_context_marker=tl-US0131-architecture-20260907T193500Z-fresh`
- **Status**: US-0131 remains **OPEN**. **Next**: `/sprint-plan` in fresh **tech-lead** subagent (orchestrator may insert sovereign-critic of architecture first). Do not spawn sprint-plan from this architecture chat. STOP.
