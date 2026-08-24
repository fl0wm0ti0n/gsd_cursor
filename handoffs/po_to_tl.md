## US-0123 spec PASS — pointer

- US-0123 spec (intake+discovery) PASS; Status OPEN; AC-1..AC-10 unchecked; full narrative `handoffs/archive/po-to-tl-pack-20260824.md ## Spec handoff — US-0123`; research PASS (deepened R-0109 DQ1..DQ10 LOCKED — see `handoffs/archive/po-to-tl-pack-20260824-a.md ## US-0123 research PASS — pointer` + `docs/engineering/research.md ## R-0109 ### Deepened findings — US-0123`); next `/architecture` (tech-lead) authors companion DEC-0123 + locks SOT/materializer/validator; proofs intake `6c9aabdc...0468f578` discovery `66d9fa99...d048e5f2` research `FAE07A6C...E24BF351` (model_id=glm-5.2-high).
## Spec handoff — US-0122 OpenCode role agents and Layer-1 permission table

- **Phase completed**: spec (`intake + discovery`). **Role**: po. **Story**: US-0122. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp**: intake 2026-08-24T11:33:00Z; discovery 2026-08-24T11:34:00Z. **Fresh markers**: `po-US0122-intake-20260824T113300Z-fresh`, `po-US0122-discovery-20260824T113400Z-fresh`.
- **Runtime proofs**: intake `rp-auto-20260824-01-intake-po-20260824T113300Z-US-0122` (`proof_hash=3FD8A7B437448E01750F5C3FFC64E57D76B293A015F663CA05533E5CCB943140`, ttl 2026-08-24T12:33:00Z); discovery `rp-auto-20260824-01-discovery-po-20260824T113400Z-US-0122` (`proof_hash=C8B6E58EEC9929156E8F8D71497B998E9FDD4E0AD86C9CD1C2C252362CB8BC3D`, ttl 2026-08-24T12:34:00Z).
- **Intake verdict**: PASS by existing program evidence; no new story ID allocated, no ACs wiped. `handoffs/intake_evidence/US-0121-intake-20260822.json` maps `role-agents-permissions` → [US-0122], `coverage_complete=true`, `missing_topics=[]`, `selected_pack=first-intake-pack`. US-0121 remains DONE; US-0122 remains OPEN.
- **Discovery locks D1–D10**: eight agents (`po`, `tech-lead`, `dev`, `qa`, `release`, `curator`, `security`, `auto`); Layer-1 host permissions are enforcement; short Layer-2 prompts only; PO product-doc allow + production/code deny; orchestrator no phase-artifact writes and Task allow-list only to role agents; security findings-oriented; no `.cursor/agents`/rules/skills/command-body clones; no vendor slugs in template agents; consumes US-0121 `.opencode` path and cursor-only default; `test_us0122_*` inventory/deny/clone/parity surface; architecture must lock final permission matrix.
- **Discovery question count**: 8. **Questions for `/research` / R-0109**: DQ1 exact project file form (`.opencode/agents/*.md` vs `opencode.json` `agent` table); DQ2 exact `edit` permission object syntax and precedence; DQ3 whether deny globs win over broad allow globs; DQ4 `task` allow-list syntax for seven role agents; DQ5 hidden/manual invocation settings for primary `auto` vs role agents; DQ6 whether security findings-only paths need a committed directory; DQ7 minimum contract harness for prompt-ignoring PO denial; DQ8 whether active kit repo mirrors stay template-only until US-0126.
- **Compose guards**: US-0003 / US-0023 / BUG-0006 compose only; do not clone `.cursor/agents` as enforcement. US-0123 owns provider/slug routing; no vendor slugs in template. US-0121 host default remains cursor-only until explicit `--host opencode|both`.
- **Isolation**: `phase_id=intake`, `role=po`, `model_id=gpt-5.5-medium`, `fresh_context_marker=po-US0122-intake-20260824T113300Z-fresh`; `phase_id=discovery`, `role=po`, `model_id=gpt-5.5-medium`, `fresh_context_marker=po-US0122-discovery-20260824T113400Z-fresh`; evidence refs: `docs/product/backlog.md ## US-0122`, `docs/product/vision.md ## Discovery Notes — US-0122`, this handoff.
- **Status**: OPEN. **Next**: `/research` (tech-lead) to deepen **R-0109** for US-0122. `stop_condition=STOP after spec completes; hand off via artifacts only`.

## Discovery handoff — US-0121 OpenCode template pack and installer host mode

- **Phase completed**: discovery. **Role**: po. **Story**: US-0121. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp**: 2026-08-23T07:40:00Z. **Fresh context marker**: `po-US0121-discovery-20260823T074000Z-fresh`.
- **Runtime proof**: `rp-auto-20260823-01-discovery-po-20260823T074000Z-US-0121` (`proof_hash=9c346006191ee7b9b94d4386708ec8756d7e38cb13d342d09b520f4ef3b6f3dc`, ttl 2026-08-23T08:40:00Z).
- **Locks D1–D11**: `--host cursor|opencode|both` (default cursor-only; unknown=`INSTALL_HOST_INVALID`); empty-but-valid `template/.opencode/{agents,commands,plugins}` + gitignore; coexistence (cursor-only byte-identical on `.cursor/`); manifest + triple-installer; `--scope=opencode-adapter`; no secrets/slugs; compose US-0008 additive only; epic US-0122..US-0126 out of scope; no new GUI.
- **R-0109 Q1–Q5 remain open** (not architecture locks). Discovery Q6–Q12 (pack layout, manifest encoding, kernel vs host packs, active vs template, gitignore names, companion DEC, CLI `--host` passthrough) go to `/research`.
- **Isolation**: `phase_id=discovery`, `role=po`, `fresh_context_marker=po-US0121-discovery-20260823T074000Z-fresh`, `timestamp=2026-08-23T07:40:00Z`, `evidence_ref=docs/product/backlog.md ## US-0121 + docs/product/vision.md ## Discovery Notes — US-0121 + this compact hot copy`.
- **Full narrative**: `handoffs/archive/po-to-tl-pack-20260823.md` (triad prefix-archive of this newest-first file; compact copy restored under `PO_TO_TL_HOT_MAX_LINES=650`).
- **Triad rollover**: `triad-rollover|po_to_tl` moved=1 pack=`handoffs/archive/po-to-tl-pack-20260823.md` retained_sections=8 retained_lines=623; `triad-rollover|state` moved=1 pack=`docs/engineering/state-archive/state-pack-20260823.md` then post-append moved=1 pack=`docs/engineering/state-archive/state-pack-20260823-a.md` retained_lines=998.
- **Status**: OPEN. **Next**: `/research` (tech-lead). `stop_condition=STOP after discovery completes; hand off via artifacts only`.

## US-0121 — OpenCode adapter epic intake (US-0121..US-0126)

- **Stories**: US-0121 (first slice) plus OPEN siblings US-0122..US-0126; acceptance rows unchecked.
- **Evidence**: `handoffs/intake_evidence/US-0121-intake-20260822.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`, first-intake-pack, coverage_complete=true)
- **Research**: **R-0109** stub. Brief: `docs/product/opencode-adapter-masterplan.md`
- **Phase**: intake. **Role**: po. **Verdict**: INTAKE PASS; no DECISION_GATE
- `intake_run_id=cursor-20260822-opencode-adapter-intake`, `writer_id=po-cursor-20260822`
- **Status**: OPEN per US-0045. **Next**: `/discovery` (fresh PO) for **US-0121**; US-0122–US-0126 remain OPEN.

### Isolation evidence (US-0048 / BUG-0006)

- `phase_id=intake`; `role=po`; `fresh_context_marker=po-US0121-intake-20260822T211500Z-fresh`; `timestamp=2026-08-22T21:15:00Z`

### Summary

Host-adapter on stock OpenCode: kernel + Python validators + `.opencode/` pack + one orchestrator plugin. Cursor pack stays. Default install remains **cursor-only** until `--host opencode|both`. Plugin v1 vs v2 deferred to `/research`. Standalone runtime is a separate program.

### Split rationale (US-0051)

Workflow-step slices (operator accepted via masterplan): **US-0121** pack+installer+coexistence; **US-0122** roles+permissions (success test c); **US-0123** `provider/slug`; **US-0124** spawn-only plugin (success tests a,d) + US-0092 `--invoke-cmd`; **US-0125** thin commands + validator bridge (success test b); **US-0126** runbook + `--scope=opencode-adapter`. Do not clone US-0001–US-0119.

### Assumptions locked

Default install host remains cursor-only until explicit `--host opencode|both` opt-in; OpenCode plugin v1 vs v2 deferred to `/research`.

### Compose, do not amend

US-0008 (additive `--host` only); US-0003 roles; US-0069 matrix; US-0092 outer driver; US-0101/US-0102 without Cursor aliases as runtime; BUG-0006 spawn-only; US-0023 isolation. Do not port US-0095 — the plugin is the OpenCode chain.

### Risks

R1 spawn isolation / V2 `subtask` ignored (fail closed; **R-0109** Q1–Q2). R2 dual-host parity. R3 plugin API unknown. R4 template slug leakage. R5 sovereign/standalone scope creep (deferred plan areas).

### Next scheduled phase

`/discovery` fresh PO for **US-0121**. Then `/research` (tech-lead) to deepen **R-0109**, then `/architecture`.

### Triad rollover

- `triad-rollover|state` moved=1 pack=`docs/engineering/state-archive/state-pack-20260822.md` retained_checkpoints=12 retained_lines=978
- `triad-rollover|po_to_tl` moved=1 pack=`handoffs/archive/po-to-tl-pack-20260822.md` retained_lines=580 retained_sections=7
- Full intake section also stored in that po_to_tl pack (prefix archive on newest-first file). This compact copy restored to the hot surface under `PO_TO_TL_HOT_MAX_LINES=650`.

## Discovery handoff Ã¢Â€Â” US-0119 Autonomous-autonomy presets (spec macro)

**Phase completed**: discovery
**Phase role**: po
**Story**: US-0119 Autonomous-autonomy presets and configurable hard-stop relaxation
**Verdict**: PASS (no DECISION_GATE)
**Timestamp**: 2026-07-05T21:50:00Z
**Fresh context marker**: po-US0119-discovery-20260705T215000Z-fresh
**Runtime proof**: rp-auto-20260705-us0119-discovery-po-20260705T215000Z-US-0119 (proof_hash=71f1f55775f4d33bdd469f860eddfb7b4361ac462077386d27863f8c22c1cf86, proof_ttl=2026-07-05T22:50:00Z)
**Delivery mode**: ultra_lean (spec+plan merged)
**Macro phase**: spec (intake+discovery merged)

### Summary

AUTONOMY_PRESET={none|balanced|full} scratchpad flag that deterministically expands into twelve per-feature autonomy flags. AUTONOMY_STOP_POLICY={block|auto_repair_then_block|auto_repair_then_skip} flag that classifies every fail-closed reason code as security_hard (never auto-resolved) or autonomy_resolvable (bounded auto-repair with ledger cap). Compose (read-only) with US-0092/US-0095/US-0056/US-0068/US-0096/BUG-0007 Ã¢Â€Â” preset layer is additive only, never rewrites existing semantics.

### Discovery locks (L1..L12)

**L1**: AUTONOMY_PRESET=none|balanced|full (default none) in .cursor/scratchpad.md + template/.cursor/scratchpad.local.example.md. When none, byte-identical pre-US-0119 behavior.

**L2**: scripts/autonomy_preset_lib.py:expand_autonomy_preset(preset, overrides) returns dict. Expansion is deterministic. Explicit per-flag values win over preset expansion.

**L3**: AUTONOMY_STOP_POLICY=block|auto_repair_then_block|auto_repair_then_skip (default block).

**L4**: docs/engineering/autonomy-stop-matrix.md + template/docs/engineering/autonomy-stop-matrix.md (parity). YAML companion scripts/data/autonomy_stop_matrix.yaml + scripts/validate_autonomy_stop_matrix.py.

**L5**: Twelve per-feature flags documented and consumed: INTAKE_AUTONOMY_MODE, INTAKE_MINIMAL_PACK, INTAKE_ASSUME_STACK_CONTEXT, WORK_KIND_AUTO_ACCEPT, CROSS_MODEL_REWORK_EXHAUSTED_POLICY, CROSS_MODEL_SKIP_PHASES, RESUME_BRIEF_AUTO_REFRESH, RUNTIME_PROOF_KIND, GOAL_CONVERGENCE_INTERVAL, SOVEREIGN_DRAIN_AUTO_ACCEPT, RELEASE_PUBLISH_AUTO_CONFIRM, AUTONOMY_STOP_POLICY.

**L6**: Twelve flags do NOT exist yet in scratchpad (grep yields zero matches). US-0119 ADDS these twelve keys net-new.

**L7**: AUTONOMY_PRESET=none produces byte-identical pre-US-0119 orchestrator behavior. Contract test test_us0119_preset_none_is_noop enforces.

**L8**: security_hard gates NEVER softened. Contract test test_us0119_security_hard_gates_never_auto_repaired enforces matrix divergence.

**L9**: Append-only handoffs/autonomy_repair_ledger/<orchestrator_run_id>.jsonl. Cap per (run, reason_code). AUTONOMY_REPAIR_CAP_EXHAUSTED terminal stop reason.

**L10**: autonomy_relaxed breadcrumbs in docs/engineering/state.md.

**L11**: Compose do-not-amend Ã¢Â€Â” US-0092/US-0095/US-0056/US-0068/US-0096/BUG-0007 untouched. Contract test test_us0119_preset_expansion_uses_known_keys_only enforces.

**L12**: Ten contract test markers (test_us0119_*).

### Open questions Q1..Q10 for /research

**Q1** enumerate every autonomy_resolvable reason-code from /auto /intake /execute /qa /release.

**Q2** per-reason-code auto_repair_kind taxonomy.

**Q3** matrix cap defaults Ã¢Â€Â” uniform 3 or per-code tuning?

**Q4** RUNTIME_PROOF_KIND=lightweight TTL same as strict_hash?

**Q5** SOVEREIGN_DRAIN_RISK_THRESHOLD low|medium|high criteria per tier.

**Q6** RELEASE_PUBLISH_AUTO_CONFIRM allowlist only or includes previously-confirmed?

**Q7** INTAKE_MINIMAL_PACK threshold for "established project".

**Q8** matrix validator grep commands vs explicit manifest.

**Q9** AUTONOMY_REPAIR_CAP_EXHAUSTED new code vs extension of BLOCK_RETRY_CAP_EXHAUSTED.

**Q10** breadcrumb format in state.md Ã¢Â€Â” one-line per soft-stop or aggregated per phase?

### Risks R1..R6 carried to /architecture

**R1** (MEDIUM) backward-compat regression Ã¢Â€Â” test_us0119_preset_none_is_noop.

**R2** (MEDIUM) security gate bypass matrix Ã¢Â€Â” test_us0119_security_hard_gates_never_auto_repaired.

**R3** (LOW) repair ledger growth Ã¢Â€Â” per-run cap + gitignore.

**R4** (MEDIUM) operator confusion Ã¢Â€Â” breadcrumb + ledger audit surface.

**R5** (LOW-MEDIUM) preset-expansion vs explicit-key precedence Ã¢Â€Â” LOCKED: explicit > preset > defaults.

**R6** (LOW) compose-do-not-amend drift Ã¢Â€Â” test_us0119_preset_expansion_uses_known_keys_only.

### Compose do-not-amend (verified)

- US-0092: Ã¢ÂœÂ“ exists Ã¢Â€Â” delivery confirmation gate unchanged
- US-0095: Ã¢ÂœÂ“ exists Ã¢Â€Â” native auto-chain unchanged
- US-0056: Ã¢ÂœÂ“ exists as inline reference Ã¢Â€Â” strict runtime proof semantics UNCHANGED
- US-0068: Ã¢ÂœÂ“ exists as intake evidence gate Ã¢Â€Â” NEVER bypassed
- US-0096: Ã¢ÂœÂ“ exists Ã¢Â€Â” delivery modes unchanged
- BUG-0007: Ã¢ÂœÂ“ exists as anti-echo truthfulness rule Ã¢Â€Â” assumption_confirmation_ref contract preserved

### DC check

grep "^## US-0119" docs/engineering/architecture.md Ã¢Â†Â’ no matches. Expected (anchor added in /architecture phase). Not appended to sovereign_deferrals.jsonl.

### Validator gates

- validate_readme_feature_coverage.py PASS
- scratchpad_example_parity_test.py 4 passed

### Isolation evidence

- phase_id=discovery, role=po, story_id=US-0119, sprint_id=(pending)
- orchestrator_run_id=auto-20260705-us0119-intake
- fresh_context_marker=po-US0119-discovery-20260705T215000Z-fresh
- timestamp=2026-07-05T21:50:00Z (UTC)
- evidence_ref=docs/product/backlog.md (## US-0119 L4028-4070), handoffs/intake_evidence/US-0119-intake-20260705.json, handoffs/po_to_tl.md, handoffs/resume_brief.md, docs/engineering/research.md (R-0107 stub L8907-8928), docs/engineering/architecture.md (grep ^## US-0119 + compose targets), .cursor/scratchpad.md (grep autonomy keys Ã¢Â€Â” zero matches confirming L6), docs/product/acceptance.md (US-0119 row L146)
- assemble_sovereign_memory_digest(...) NOT called
- No write to mistakes.jsonl

### Decision gate

decision_gate=false (no DECISION_GATE)
stop_conditions_met=yes

### Next scheduled phase

next_scheduled_phase=/research
next_scheduled_role=tech-lead
next_scheduled_sprint_macro=plan
stop_condition=STOP after discovery completes; hand off to /research in fresh tech-lead subagent

---

# PO-to-TL handoffs

<!-- Archive pointer: US-0117 lifecycle handoffs (sprint-plan, architecture, research, spec) rolled over to `handoffs/archive/po-to-tl-pack-20260704-c.md` on 2026-07-04 by curator (US-0117 refresh-context terminal - final story in 5-story drain). US-0113/US-0114/US-0115 lifecycles in po-to-tl-pack-20260704-a/b.md; US-0116 lifecycle handoffs lost in git checkout HEAD recovery event (authoritative record in sprints/S0116/). Drain queue EMPTY - no next-story handoff to retain. -->

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

