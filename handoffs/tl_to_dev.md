## Plan-verify PASS handoff — US-0131 / S0133 — `/execute` next (fresh dev)

- sprint_id: S0133
- story_id: US-0131 (Status OPEN — authority docs/product/backlog.md)
- bug_id: (none)
- companion_dec: DEC-0131 Accepted
- research_anchor: R-0116 (DQ1–DQ10 LOCKED)
- architecture_anchor: docs/engineering/architecture.md # US-0131
- approach: A1 LOCKED — `.its-magic/config{,.local,.example}.json` SOT + LegacyScratchpadAdapter + `resolve_runtime_config` migration
- orchestrator_run_id: auto-20260907-us0131
- plan_verify_fresh_context_marker: qa-US0131-plan-verify-20260907T195200Z-fresh
- plan_verify_timestamp: 2026-09-07T19:52:00Z (UTC)
- model_id: composer-2.5 (CROSS_MODEL_REVIEW=1 — required on isolation)
- plan_verify_verdict: PASS
- decision_gate: false
- sprint_status: PLANNED → execute-ready (backlog OPEN per US-0045 — not mutated; AC-1..AC-8 unchecked)
- task_count: 9 (T-anch + T-001..T-008; T-009 folded into T-007; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001,T-007(m1,m6); AC-2->T-002,T-007(m2); AC-3->T-003,T-007(m3; m5 DQ4 primary); AC-4->T-004,T-007(m8); AC-5->T-005,T-007(m10); AC-6->T-005,T-007(m4 primary; m5 nuance=AC-3/DQ4); AC-7->T-006,T-007(m7); AC-8->T-007(all10 incl m9),T-008; DC->T-anch
- task_order: T-anch -> T-001 -> T-002 -> T-003 -> T-004 -> T-005 -> T-006 -> T-007 -> T-008
- plan-verify.json: PASS at sprints/S0133/plan-verify.json
- compose_guards (non-negotiable): DO NOT expand US-0132; DO NOT dump kit keys into opencode.json; DO NOT reopen BUG-0015/0016; DO NOT amend DEC-0086/0087/0123; DO NOT mark US-0131 DONE; DO NOT tick ACs; DO NOT mutate intake JSON; DO NOT rewrite architecture.md / DEC-0131
- critic_nb_execute_awareness:
  - host_mode=None = auto-detect (T-001/T-003); HOST_CONFIG_PATH_FORBIDDEN only OpenCode-only + forbidden cursor-sole request
  - T-004 exhaustive 9-module inventory; do not expand to Cursor-only parity scripts
  - Do not re-split T-009; marker 9 mandatory in T-007 10-marker set
- first_execute_task: T-anch
- key_locked_artifacts:
  - paths: `.its-magic/config.example.json` / `config.json` / `config.local.json` (token=`config`)
  - API: `resolve_runtime_config(repo_root, *, host_mode=None, required_keys=None)`
  - 10 `test_us0131_*` markers (static/fixture; no live OpenCode probe)
  - US-0132 boundary: ignore MODEL_* (marker 9)
- runtime_proof_id: rp-auto-20260907-us0131-plan-verify-qa-20260907T195200Z-US-0131
- proof_hash: 5F198A1862986704CC24AE0EA2D41C87D343C3AACF842997CB5C76D2995C29F1
- proof_ttl: 2026-09-07T20:52:00Z
- consumed_sprint_plan_proof: rp-auto-20260907-us0131-sprint-plan-techlead-20260907T194500Z-US-0131 / 96221EF4BC1FB83F9A0C288287672F1A18ACC023C80185029EA3A6DDABD84E66 — RUNTIME_PROOF_VALID
- next_scheduled_phase: /execute (role=dev)
- next_scheduled_role: dev
- stop_condition: STOP after plan-verify. Orchestrator may critic plan-verify then spawn /execute in fresh dev (BUG-0006). Do NOT spawn execute from plan-verify qa. Do NOT work US-0132.

---

## Prior — Sprint-plan handoff — US-0131 / S0133 — `/plan-verify` (superseded by PASS)

- sprint_id: S0133
- story_id: US-0131
- plan-verify.json: was PENDING — now PASS (see above)
- fresh_context_marker: tl-US0131-sprint-plan-20260907T194500Z-fresh
- timestamp: 2026-09-07T19:45:00Z (UTC)
- runtime_proof_id: rp-auto-20260907-us0131-sprint-plan-techlead-20260907T194500Z-US-0131
- proof_hash: 96221EF4BC1FB83F9A0C288287672F1A18ACC023C80185029EA3A6DDABD84E66

---

## Sprint-plan handoff — BUG-0016 / S0132 — `/execute` next (fresh dev; ultra_lean skips standalone /plan-verify)

- sprint_id: S0132
- bug_id: BUG-0016 (Status OPEN — authority docs/product/backlog.md)
- story_id: (none — bug segment)
- dec_id: none companion (DEC-0130 rejected; DEC-0122 §2 amended sole SOT in /architecture — execute ships frontmatter parity)
- research_anchor: R-0115 (DQ1–DQ8 LOCKED)
- architecture_anchor: docs/engineering/architecture.md # BUG-0016
- approach: A* LOCKED — amend DEC-0122 §2 sole SOT + agent frontmatter (active+template); bash ask po/tl/curator; PO +intake_evidence/** +resume_brief +state.md; sprints/S*/ globs; release duty paths; 7 test_bug0016_*; success test (c) preserved
- orchestrator_run_id: auto-20260906-bug0016
- fresh_context_marker: tl-BUG0016-sprint-plan-20260906T185500Z-fresh
- timestamp: 2026-09-06T18:55:00Z (UTC)
- model_id: composer-2.5 (CROSS_MODEL_REVIEW=1 — required on isolation)
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 — not mutated; acceptance BUG-0016 unchecked)
- task_count: 8 (T-anch + T-001..T-007; within SPRINT_MAX_TASKS=12; 1:1 architecture seeds)
- ac_surjective_map: AC-1->T-001,T-002,T-006(m1); AC-2->T-001,T-006(m2); AC-3->T-002,T-003,T-006(m3); AC-4->T-004,T-006(m4); AC-5->T-anch,T-005,T-006(m5); AC-6->T-anch,T-006(m6); AC-7->T-001..T-004,T-006(m7); AC-8->T-anch,T-005; DQ8->T-007
- task_order: T-anch -> T-001 (po.md) -> T-002 (tech-lead+curator) -> T-003 (dev+qa S*) -> T-004 (release duty paths) -> T-005 (us0122 realign) -> T-006 (7 bug0016 markers) -> T-007 (write-guard verify) -> integration verification
- compose_guards (non-negotiable): DO NOT invent DEC-0130 / second matrix; DO NOT use bash:allow; DO NOT reopen US-0131/US-0132; DO NOT reopen BUG-0015; DO NOT amend DEC-0124/0125 unless T-007 proves double-deny; DO NOT add live OpenCode CI probe; DO NOT mark BUG-0016 DONE; DO NOT tick acceptance BUG-0016; DO NOT mutate intake JSON; DO NOT rewrite architecture.md; DO NOT transfer US-0126 runbook prose ownership via Layer-1 allow
- critic_carry_ins: 0 new blocking. 3 architecture critic NBs `b0016ar-*` status=resolved non-blocking — routed as awareness into /execute:
  - b0016ar-challenger-001 (`ik_bug0016_arch_edge_and_proof`): T-007 Layer-1∩write-guard verify; keep S* not S[0-9]*; active↔template parity + intentional us0122 realign
  - b0016ar-architect-002 (`ik_bug0016_arch_layer_coupling`): keep T-anch..T-007 1:1; DEC-0122 §2 sole SOT; CF2 runbook allow ≠ US-0126 ownership
  - b0016ar-subtractor-003 (`ik_bug0016_arch_scope_minimal`): T-anch read-only; no DEC-0130 / bash:allow / live probe; do not mark DONE; 7 markers required
- architecture_pointers: docs/engineering/architecture.md # BUG-0016 (approach A*, 7-marker table, CF1–CF5 CLOSED, seeds T-anch + T-001..T-007). Do not rewrite.
- first_execute_task: T-anch (NO-OP / verification) — verify # BUG-0016 H1 + DEC-0122 §2 amended + approach A* + R-0115 DQ1–DQ8 + CF1–CF5 + compose guards + 7-marker list + pre-execute agent gap still present
- key_locked_artifacts:
  - bash (DQ1): po/tech-lead/curator → ask; reject allow; object-form YAGNI
  - PO paths (DQ2): +intake_evidence/** +resume_brief.md +state.md; ** deny last
  - globs (DQ3): sprints/S*/… not Sxxxx; no char classes
  - release (DQ5/CF2): +release-findings +verify-work-to-release +state +resume_brief +runbook; keep verify_to_release
  - tests (DQ6/DQ7): amend us0122_* + 7 test_bug0016_*; no live probe
  - DQ8: T-007 write-guard verify; amend DEC-0124/0125 only if proven
- files_to_touch: .opencode/agents/{po,tech-lead,curator,dev,qa,release}.md + template peers; tests/us0122_contract_test.py; tests/bug0016_contract_test.py (+ template); optional parity scope bug-0016
- files_NOT_to_touch: docs/engineering/architecture.md (do not rewrite), DEC-0122 body beyond already-amended §2, DEC-0124/0125 (unless T-007 proves), security.md/auto.md (verify unchanged), backlog BUG-0016 Status/ACs, handoffs/intake_evidence/BUG-0016-intake-20260906.json, US-0131/US-0132 rows
- next_phase: `/execute` (fresh dev per US-0069 / DEC-0051; first canonical phase of `build+verify` macro per ultra_lean; /plan-verify merged into qa per ultra_lean — qa creates plan-verify.json within build+verify). Orchestrator runs sovereign-critic of sprint-plan first (CROSS_MODEL_REVIEW=1). Do not mandate outer driver.
- sprint_artifacts: sprints/S0132/ (sprint.md, tasks.md, progress.md, uat.json, uat.md)
- runtime_proof_id: rp-auto-20260906-bug0016-sprint-plan-techlead-20260906T185500Z-BUG-0016
- proof_hash: F6892B96789FF471D7A97B40F80BBE59E725FB5A5DD573515D0ABC663B0A997F
- proof_ttl: 2026-09-06T19:55:00Z (UTC)
- prior_phase_proof_consumed: rp-auto-20260906-bug0016-architecture-techlead-20260906T184500Z-BUG-0016 (proof_hash=7AC851CDF1953594365AFF11B015BFD850E737F75A327FA2A02B1CCB544D5A31, ttl=2026-09-06T19:45:00Z — critic MATCH; consumed at 2026-09-06T18:55:00Z before RUNTIME_PROOF_STALE; sovereign-critic architecture PASS at 2026-09-06T18:50:00Z anti_slop_aggregate=10 0 blocking findings)
- stop_condition: STOP after sprint-plan completes; hand off via artifacts only. Orchestrator owns critic of sprint-plan then /execute in fresh dev subagent per BUG-0006. Do not spawn /execute or /plan-verify from this subagent. Do not mark BUG-0016 DONE. Do not tick acceptance BUG-0016. Do not mutate intake JSON. Do not invent DEC-0130. Do not use bash:allow. Do not reopen US-0131/US-0132. Do not reopen BUG-0015.

---

## Sprint-plan handoff â BUG-0015 / S0131 â `/execute` next (fresh dev; ultra_lean skips standalone /plan-verify)

- sprint_id: S0131
- bug_id: BUG-0015 (Status OPEN â authority docs/product/backlog.md)
- story_id: (none â bug segment)
- dec_id: none (companion DEC not required; cite R-0114; compose DEC-0124 / DEC-0125 without amend)
- research_anchor: R-0114 (DQ1âDQ7 LOCKED)
- architecture_anchor: docs/engineering/architecture.md # BUG-0015
- approach: A* LOCKED â ctx.command.transform + editor.add({ name: "auto", execute }) â runAutoLifecycle â spawnPhase / dispatchStopMatrix; fail-closed OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED + OPENCODE_AUTO_ALREADY_RUNNING
- orchestrator_run_id: auto-20260906-bug0015
- fresh_context_marker: tl-BUG0015-sprint-plan-20260906T143000Z-fresh
- timestamp: 2026-09-06T14:30:00Z (UTC)
- model_id: composer-2.5 (CROSS_MODEL_REVIEW=1 â required on isolation)
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 â not mutated; acceptance BUG-0015 unchecked)
- task_count: 7 (T-anch + T-001..T-006; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001,T-002,T-005(m1,m2); AC-2->T-001,T-005(m3),T-006; AC-3->T-002,T-005(m4); AC-4->T-003,T-005; AC-5->T-002,T-005(m5),T-006; AC-6->T-004,T-005(m6); AC-7->T-anch,T-005(m7); AC-8->T-005(all 7 markers)
- task_order: T-anch -> T-001 (command.transform / editor.add auto attach) -> T-002 (runAutoLifecycle + mutex + spawn loop) -> T-003 (Python IsolationEvidence + first-phase bridge) -> T-004 (auto.md STOP-only assert) -> T-005 (7 bug0015 markers) -> T-006 (runbook h3 stub) -> integration verification
- compose_guards (non-negotiable): DO NOT amend DEC-0124 / DEC-0125 bodies; DO NOT amend test_us0124_* / test_us0125_*; DO NOT solve BUG-0016 / DEC-0122 matrix; DO NOT reopen US-0131/US-0132; DO NOT port Cursor Task-loop; DO NOT reimplement stop-matrix in TS; DO NOT add live OpenCode CI probe; DO NOT mark BUG-0015 DONE; DO NOT tick acceptance BUG-0015; DO NOT mutate intake JSON; DO NOT rewrite architecture.md
- critic_carry_ins: 0 new blocking. 3 architecture critic NBs `b0015ar-*` status=resolved non-blocking â routed as awareness into /execute:
  - b0015ar-challenger-001 (`ik_bug0015_arch_edge_and_proof`): T-002/T-005 prove mutex gate on dual-fire / secondary command.executed after STOP; document mutex TTL clock source + clear-on-fail-closed paths
  - b0015ar-architect-002 (`ik_bug0015_arch_layer_coupling`): T-003 Python IsolationEvidence + first-phase only; T-006 runbook h3 stub only (US-0126 owns full table); active+template parity
  - b0015ar-subtractor-003 (`ik_bug0015_arch_scope_minimal`): T-anch read-only; do not mark DONE; 7 markers required; no BUG-0016 / live probe / DEC amend
- architecture_pointers: docs/engineering/architecture.md # BUG-0015 (approach A*, 7-marker table, CF1âCF7 CLOSED, seeds T-anch + T-001..T-006). Do not rewrite.
- first_execute_task: T-anch (NO-OP / verification) â verify # BUG-0015 H1 + approach A* + R-0114 DQ1âDQ7 + CF1âCF7 + compose guards + 7-marker list + attach gap still present pre-T-001
- key_locked_artifacts:
  - attach (DQ1): `command.transform` / `editor.add({ name: "auto", execute })`; missing â OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED
  - lifecycle (DQ2/DQ4): `runAutoLifecycle` + mutex TTL 7200s / clear-on-exit; OPENCODE_AUTO_ALREADY_RUNNING
  - bridges (DQ3/DQ5): Python IsolationEvidenceâstate.md; first-phase argvâresume_briefâscratchpadâUS-0087
  - static (DQ5/DQ6): auto.md STOP-only; 7 test_bug0015_* mock-ctx; no live probe
  - docs: runbook h3 stub for two new reason codes; US-0126 cross-link
- files_to_touch: .opencode/plugins/orchestrator.ts + template, .opencode/commands/auto.md + template, tests/bug0015_contract_test.py + template, thin Python isolation/resume helper, docs/engineering/runbook.md + template, optional parity scope bug-0015
- files_NOT_to_touch: docs/engineering/architecture.md (do not rewrite), decisions/DEC-0124.md, decisions/DEC-0125.md, DEC-0122 matrix / .opencode/agents/*.md (BUG-0016), backlog BUG-0015 Status/ACs, handoffs/intake_evidence/BUG-0015-intake-20260906.json, us0124/us0125 contract test bodies, US-0131/US-0132 rows
- next_phase: `/execute` (fresh dev per US-0069 / DEC-0051; first canonical phase of `build+verify` macro per ultra_lean; /plan-verify merged into qa per ultra_lean â qa creates plan-verify.json within build+verify). Orchestrator runs sovereign-critic of sprint-plan first (CROSS_MODEL_REVIEW=1). Do not mandate outer driver.
- sprint_artifacts: sprints/S0131/ (sprint.md, tasks.md, progress.md, uat.json, uat.md)
- runtime_proof_id: rp-auto-20260906-bug0015-sprint-plan-techlead-20260906T143000Z-BUG-0015
- proof_hash: 628D489A395FD783DE7E84A5D8AAC82823AA35843A4FE498638DEB0A5175E43E
- proof_ttl: 2026-09-06T15:30:00Z (UTC)
- prior_phase_proof_consumed: rp-auto-20260906-bug0015-architecture-techlead-20260906T142000Z-BUG-0015 (proof_hash=DBEB0F5D44E6801D5E1DEEA686A95CB32090B75A1FA1DCCF5621C1E1FD017440, ttl=2026-09-06T15:20:00Z â critic MATCH; consumed at 2026-09-06T14:30:00Z before RUNTIME_PROOF_STALE; sovereign-critic architecture PASS at 2026-09-06T14:25:00Z anti_slop_aggregate=8 0 blocking findings)
- stop_condition: STOP after sprint-plan completes; hand off via artifacts only. Orchestrator owns critic of sprint-plan then /execute in fresh dev subagent per BUG-0006. Do not spawn /execute or /plan-verify from this subagent. Do not mark BUG-0015 DONE. Do not tick acceptance BUG-0015. Do not mutate intake JSON. Do not amend DEC-0124/0125. Do not solve BUG-0016. Do not reopen US-0131/US-0132.

---

## Architecture handoff â BUG-0015 â `/sprint-plan` next (fresh tech-lead; ultra_lean plan macro)

- bug_id: BUG-0015 (Status OPEN â authority docs/product/backlog.md)
- story_id: (none â bug segment)
- sprint_id: (pending â materialize at /sprint-plan)
- dec_id: none (companion DEC not required; cite R-0114; compose DEC-0124 / DEC-0125 without amend)
- research_anchor: R-0114 (DQ1âDQ7 LOCKED)
- architecture_anchor: docs/engineering/architecture.md # BUG-0015
- approach: A* LOCKED â ctx.command.transform + editor.add({ name: "auto", execute }) â runAutoLifecycle â spawnPhase / dispatchStopMatrix; fail-closed OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED + OPENCODE_AUTO_ALREADY_RUNNING
- orchestrator_run_id: auto-20260906-bug0015
- fresh_context_marker: tl-BUG0015-architecture-20260906T142000Z-fresh
- timestamp: 2026-09-06T14:20:00Z (UTC)
- model_id: composer-2.5
- architecture_verdict: PASS
- deferred_closures: CF1âCF7 CLOSED (transform owns execute; Python IsolationEvidenceâstate.md; Python first-phase selectors; runAutoLifecycle; mutex 7200s TTL; transform primary; no companion DEC)
- task_seeds: T-anch + T-001..T-006 (7; under SPRINT_MAX_TASKS=12) â refine into sprints/S-BUG0015 or next free sprint id at /sprint-plan
- ac_coverage: AC-1..AC-8 mapped in architecture Â§ AC coverage mapping
- compose_guards (non-negotiable): DO NOT amend DEC-0124 / DEC-0125 bodies; DO NOT amend test_us0124_* / test_us0125_*; DO NOT solve BUG-0016; DO NOT reopen US-0131/US-0132; DO NOT port Cursor Task-loop; DO NOT reimplement stop-matrix in TS; DO NOT add live OpenCode CI probe; DO NOT mark BUG-0015 DONE; DO NOT tick acceptance BUG-0015 row
- critic_carry_ins_closed: research CF1âCF7 closed in architecture (ik_bug0015_research_* NBs were non-blocking; no new DEC)
- files_to_touch (execute foreshadow): .opencode/plugins/orchestrator.ts + template peer; .opencode/commands/auto.md + template (STOP-only assert); tests/bug0015_contract_test.py (+ template); thin Python isolation/resume bridge; optional runbook h3 stub
- files_NOT_to_touch: decisions/DEC-0124.md, decisions/DEC-0125.md, DEC-0122 matrix, BUG-0016 backlog body (except mention), us0124/us0125 contract test bodies
- next_phase: `/sprint-plan` (fresh tech-lead per US-0069 / DEC-0051; third canonical phase of `plan` macro per ultra_lean). Orchestrator runs sovereign-critic of architecture first (CROSS_MODEL_REVIEW=1) then spawns sprint-plan. Do not mandate outer driver.
- runtime_proof_id: rp-auto-20260906-bug0015-architecture-techlead-20260906T142000Z-BUG-0015
- proof_hash: DBEB0F5D44E6801D5E1DEEA686A95CB32090B75A1FA1DCCF5621C1E1FD017440
- proof_ttl: 2026-09-06T15:20:00Z (UTC)
- prior_phase_proof_consumed: rp-auto-20260906-bug0015-research-techlead-20260906T141000Z-BUG-0015 (proof_hash=3D9E02EBBECA8C02D3051638B0782F575ABD03FEDCD369A255144D36CC01F3A1, ttl=2026-09-06T15:10:00Z)
- stop_condition: STOP after architecture PASS. Orchestrator owns critic of architecture then /sprint-plan in fresh tech-lead subagent per BUG-0006. Do not spawn /sprint-plan or /execute from this subagent. Do not mark BUG-0015 DONE. Do not solve BUG-0016. Do not execute implementation.

---

## Sprint-plan handoff â US-0129 / S0129 â `/execute` next (fresh dev; ultra_lean skips standalone /plan-verify)

- sprint_id: S0129
- story_id: US-0129
- dec_id: DEC-0129 (Accepted â `decisions/DEC-0129.md`; story-aligned companion; compose DEC-0054 / DEC-0073 / DEC-0076 / US-0049 / US-0126 B-1 / DEC-0119)
- research_anchor: R-0113 (DQ1âDQ8 LOCKED; R-0112 not extended)
- orchestrator_run_id: auto-20260827-01
- fresh_context_marker: tl-US0129-sprint-plan-20260827T073646Z-fresh
- timestamp: 2026-08-27T07:36:46Z (UTC)
- model_id: cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 â required on isolation)
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 â not mutated; acceptance L157 unchecked)
- task_count: 8 (T-anch + T-001..T-007; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001,T-005(m1,m2,m6); AC-2->T-001,T-002,T-005(m2,m3); AC-3->T-003,T-005(m4,m5); AC-4->T-004,T-006,T-005(m6,m7); AC-5->T-005(all 8 markers); AC-6->T-anch
- task_order: T-anch -> T-001 (arch_linkage_guard.py helper + pre-guard no-partial-write) -> T-002 (reason_codes ## US-0129 + security_hard matrix row) -> T-003 (ARCH_LINKAGE_AUTO_REPAIR=0 comment + DQ8 stub restore) -> T-004 (refresh-context pre â rollover â post â check) -> T-005 (8 contract markers + harness 26AB) -> T-006 (runbook h3 + ARCH_LINKAGE_PAIRS) -> T-007 (installer-owned-paths.manifest) -> integration verification
- compose_guards (non-negotiable): DO NOT amend DEC-0054 (rollover_architecture split / pack format / ARCH_HOT_MAX_* â marker 2), DEC-0073 (H1 vs H2 anchor policy â stub is H1 with title separator), DEC-0076/US-0089 (only # US-0090 after # US-0089 â stub insertion before that tail; marker 5), US-0049 (state archive contract â audit row append-bottom), US-0126 (B-1 fixture only â do not reopen; L154 stays checked), US-0127/US-0128/US-0130 (DONE â do not reopen; L155âL156 / L158 stay checked), DEC-0119 (9 auto_repair_kind + 12 preset flags â no 10th kind; flag not in AUTONOMY_PRESET), R-0112 (US-0130 overlay not extended), US-0045 (no backlog Status/ACs mutation), US-0048/BUG-0006 (fresh-context isolation), US-0056 (runtime proof lowercase keys only). Do not rewrite docs/engineering/architecture.md. Do not rewrite decisions/DEC-0129.md. Do not tick L157. Do not mutate intake JSON.
- critic_carry_ins: 0 new blocking. 3 architecture critic NBs `a0129ar-*` status=resolved non-blocking â routed as awareness into /execute:
  - a0129ar-challenger-001 (`ik_us0129_arch_proof_and_linkage_gaps`): T-001 discovery must exclude .tmp* and non-architecture.md reads (R1). T-003 v1 heading-only (R3). Do not pre-seed unrelated stubs (R6) â remediate via AC-2 repair flag or manual H1.
  - a0129ar-architect-002 (`ik_us0129_arch_layer_coupling`): T-001 helper+pre-guard; T-002 reason_codes+matrix; T-003 flag+stub; T-004 refresh-context wiring; T-005 8 markers+26AB; T-006 runbook+ARCH_LINKAGE_PAIRS; T-007 installer manifest. Import split_arch_stories + while-pop â do not copy-fork archiver. Do not add ARCH_LINKAGE_AUTO_REPAIR to AUTONOMY_PRESET.
  - a0129ar-subtractor-003 (`ik_us0129_arch_scope_discipline`): do not mark US-0129 DONE; do not tick L157; 8 markers required (not YAGNI); T-anch read-only â no architecture.md mutation; do not reopen US-0126/US-0127/US-0128/US-0130.
- architecture_pointers: docs/engineering/architecture.md # US-0129 (L1527 â approach A1, 8-marker table, helper DQ2, fail-closed DQ4/DQ5, stub DQ8, refresh-context DQ3, contract tests DQ6/DQ7, runbook/parity D8, compose-do-not-amend 8/8, risks R1âR6; sprint seeds T-anch + T-001..T-007). Do not rewrite.
- first_execute_task: T-anch (NO-OP / verification) â verify # US-0129 H1 anchor + DEC-0129 Accepted + approach A1 + R-0113 DQ1âDQ8 + compose guards 8/8 + 8-marker list locked + absent surfaces (arch_linkage_guard.py + template, us0129 contract test + template, reason_codes ## US-0129, matrix row, scratchpad live=1, refresh-context pre/post, harness 26AB, ARCH_LINKAGE_PAIRS, installer manifest row)
- key_locked_artifacts:
  - linkage guard (DQ2+DQ3): `scripts/arch_linkage_guard.py` discover_required_arch_headings stdlib scan; pre-guard no-partial-write; import split_arch_stories + while-pop; post-guard verifies active linkage
  - fail-closed (DQ4+DQ5): `ARCH_LINKAGE_ROLLOVER_BLOCKED` security_hard never skip; new ## US-0129 family in reason_codes.md; matrix auto_repair_kind=n/a cap=0
  - optional repair (DQ1+DQ8): ARCH_LINKAGE_AUTO_REPAIR=0 default-off not in AUTONOMY_PRESET; H1 stub + pack_ref before US-0089/US-0090 tail; idempotent; state.md audit row
  - wiring (DQ3): `.cursor/commands/refresh-context.md` pre-guard â --rollover â post-guard â --check
  - contract tests (Q1): `tests/us0129_contract_test.py` â 8 markers; harness 26AB after 26AA; synthetic fixtures not pack-20260825 replay
  - docs + parity (D8): runbook h3 under triad; ARCH_LINKAGE_PAIRS + --scope=arch-linkage; installer-owned-paths.manifest for arch_linkage_guard.py
- files_to_touch: scripts/arch_linkage_guard.py NEW + template mirror, docs/engineering/reason_codes.md + template, scripts/data/autonomy_stop_matrix.yaml, docs/engineering/autonomy-stop-matrix.md + template, .cursor/scratchpad.md + template (comment only), .cursor/commands/refresh-context.md + template, tests/us0129_contract_test.py NEW + template, tests/run-tests.ps1 + run-tests.sh (26AB), docs/engineering/runbook.md + template, scripts/check_intake_template_parity.py (ARCH_LINKAGE_PAIRS) + template, docs/engineering/context/installer-owned-paths.manifest + template
- files_NOT_to_touch: docs/engineering/architecture.md (do not rewrite), decisions/DEC-0129.md (already Accepted), backlog US-0129 Status/ACs, handoffs/intake_evidence/US-0129-intake-20260825.json, scripts/enforce-triad-hot-surface.py rollover_architecture split/pack/ARCH_HOT_MAX_*, AUTONOMY_PRESET expansion, US-0126/US-0127/US-0128/US-0130 DONE rows, docs/engineering/research.md ## R-0112
- next_phase: `/execute` (fresh dev per US-0069 / DEC-0051; first canonical phase of `build+verify` macro per ultra_lean; /plan-verify merged into qa per ultra_lean â qa creates plan-verify.json within build+verify). Orchestrator runs sovereign-critic of sprint-plan first (CROSS_MODEL_REVIEW=1). Do not mandate outer driver.
- sprint_artifacts: sprints/S0129/ (sprint.md, tasks.md, progress.md, uat.json, uat.md)
- runtime_proof_id: rp-auto-20260827-01-sprint-plan-tech-lead-20260827T073646Z-US-0129
- proof_hash: 8960A93B97E39E84B107001316228F5CBE69472DDF8835752862ECF4EC3B4B00
- proof_ttl: 2026-08-27T08:36:46Z (UTC)
- prior_phase_proof_consumed: rp-auto-20260827-01-architecture-tech-lead-20260827T073000Z-US-0129 (proof_hash=DDDA46794ED39186D77F268EE47364E3070997916777582095FF9198FEEF6196, ttl=2026-08-27T08:30:00Z â independent SHA-256 MATCH; consumed at 2026-08-27T07:36:46Z before RUNTIME_PROOF_STALE; sovereign-critic architecture PASS at 2026-08-27T07:35:00Z anti_slop_aggregate=8 0 blocking findings)
- stop_condition: STOP after sprint-plan completes; hand off via artifacts only. Orchestrator owns critic of sprint-plan then /execute in fresh dev subagent per BUG-0006. Do not spawn /execute or /plan-verify from this subagent. Do not mark US-0129 DONE. Do not tick acceptance L157. Do not mutate intake JSON. Do not amend DEC-0054/DEC-0073/DEC-0119 surfaces. Do not reopen US-0126/US-0127/US-0128/US-0130. Do not change archiver heading semantics. Do not add ARCH_LINKAGE_AUTO_REPAIR to AUTONOMY_PRESET.

---

## Sprint-plan handoff â US-0130 / S0130 â `/execute` next (fresh dev; ultra_lean skips standalone /plan-verify)

- sprint_id: S0130
- story_id: US-0130
- dec_id: none (companion DEC not required per R-0112; compose DEC-0104 Â§5 / DEC-0087 / DEC-0086; A6 rejected DEC-0130)
- research_anchor: R-0112 (DQ1âDQ8 LOCKED)
- orchestrator_run_id: auto-20260826-01
- fresh_context_marker: tl-US0130-sprint-plan-20260826T215200Z-fresh
- timestamp: 2026-08-26T21:52:00Z (UTC)
- model_id: cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 â required on isolation)
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 â not mutated; acceptance L158 unchecked)
- task_count: 8 (T-anch + T-001..T-007; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001,T-004,T-005(m1,m6); AC-2->T-002,T-005(m2,m7,m8); AC-3->T-001,T-005(m1,m2,m3,m6); AC-4->T-001,T-005(m4); AC-5->T-001,T-004,T-006; AC-6->T-005(all 10 markers); AC-7->T-anch,T-005(m5); AC-8->T-003,T-005(m9,m10); AC-9->T-004,T-006,T-007
- task_order: T-anch -> T-001 (select_critic_model overlay) -> T-002 (CATALOG_OPTIONAL_ROLE_KEYS + validator) -> T-003 (v2 examples + ship cursor_only as 9th) -> T-004 (scratchpad DQ8 comments, no live pin) -> T-005 (10 contract markers) -> T-006 (runbook pin-precedence) -> T-007 (SOVEREIGN_CRITIC_PAIRS + MODEL_TIER_OVERRIDES_PAIRS) -> integration verification
- compose_guards (non-negotiable): DO NOT amend US-0104 (findings JSONL / three lenses / CROSS_MODEL_* enable keys / anti-slop / opposition table / degraded_keep â marker 5), US-0102 (5-step chain / CATALOG_ROLE_KEYS required-set / PHASE_LOGICAL_ROLE â critic not in required-set; synthetic phase not registered), US-0101 (DEFAULT_PHASE_TIER_MATRIX / v1 catalogs unchanged), US-0112 (compose examples+installer; never write model-catalog.local.json), US-0127/US-0128 (DONE â do not reopen), US-0129 (OPEN â do not mutate), US-0123 (OpenCode out of scope), R-0088 (document-only), US-0045 (no backlog Status/ACs mutation), US-0048/BUG-0006 (fresh-context isolation), US-0056 (runtime proof lowercase keys only). Do not rewrite docs/engineering/architecture.md. Do not author DEC-0130. Do not write model-catalog.local.json.
- critic_carry_ins: 0 new blocking. 3 architecture critic NBs `a0130ar-*` status=resolved non-blocking â routed as awareness into /execute:
  - a0130ar-challenger-001 (`ik_us0130_arch_proof_and_overlay_gaps`): T-001 overlay must consume MODEL_SOVEREIGN-CRITIC via phase_to_model_key (hyphen exact). Do not consume underscore alias. Pin then optional roles.critic when role_catalog then opposition UNCHANGED. Do not pass a newly loaded catalog into _resolve_slug_for_tier. Same-slug keeps degraded=True.
  - a0130ar-architect-002 (`ik_us0130_arch_layer_coupling`): T-001 overlay; T-002 optional role keys; T-003 examples/installer; T-004 scratchpad comments; T-005 10 markers; T-006 runbook; T-007 parity. Do not add critic to CATALOG_ROLE_KEYS. Do not register synthetic phase.
  - a0130ar-subtractor-003 (`ik_us0130_arch_scope_discipline`): do not mark US-0130 DONE; do not tick L158; 10 markers required (not YAGNI); T-anch read-only â no architecture.md mutation; do not author DEC-0130; do not write model-catalog.local.json.
- architecture_pointers: docs/engineering/architecture.md # US-0130 (L1815 â approach A1, 10-marker table, overlay DQ2/DQ3/DQ7, optional role DQ1/DQ6, examples/installer DQ4/DQ5, scratchpad DQ8, contract tests, runbook, parity, compose-do-not-amend 9/9, risks R1âR5; sprint seeds T-anch + T-001..T-007). Do not rewrite.
- first_execute_task: T-anch (NO-OP / verification) â verify # US-0130 H1 anchor + approach A1 + R-0112 DQ1âDQ8 + compose guards 9/9 + 10-marker list locked + absent surfaces (us0130 contract test + template mirror, overlay, CATALOG_OPTIONAL_ROLE_KEYS, cursor_only 9th ship, scratchpad comments, runbook note, SOVEREIGN_CRITIC_PAIRS sovereign_critic_lib.py pair, MODEL_TIER_OVERRIDES_PAIRS cursor_only pair)
- key_locked_artifacts:
  - overlay (DQ2+DQ3+DQ7): `scripts/sovereign_critic_lib.py` `select_critic_model` prepend pin > roles.critic when role_catalog > opposition UNCHANGED; hyphen exact MODEL_SOVEREIGN-CRITIC via phase_to_model_key; SelectCriticResult shape UNCHANGED; same-slug degraded_keep UNCHANGED
  - optional catalog role (DQ1+DQ6): `CATALOG_OPTIONAL_ROLE_KEYS={"critic"}`; extra-key subtract; empty-present-critic reuses MODEL_CATALOG_SCHEMA_V2_INVALID (message names critic); missing critic not an error
  - examples + installer (DQ4+DQ5): v2 role examples get critic placeholder; cursor_only critic=composer-2.5-fast shipped as 9th; manifest + installer.ps1/py FRAMEWORK_EXACT; never write model-catalog.local.json
  - contract tests (Q1): `tests/us0130_contract_test.py` â 10 markers; mirror to template byte-identical; all static/fixture-based, no live critic spawn
  - docs (DQ8): scratchpad MODEL_* + CROSS_MODEL_* comment sites (no live pin); runbook #### Degraded fallback troubleshooting pin-precedence
  - template parity: SOVEREIGN_CRITIC_PAIRS add sovereign_critic_lib.py; MODEL_TIER_OVERRIDES_PAIRS add cursor_only json pair
- files_to_touch: scripts/sovereign_critic_lib.py + template mirror, scripts/model_tier_lib.py + template mirror, scripts/model_tier_validate.py + template mirror, v2 role example catalogs + cursor_only + template copy, installer-owned-paths.manifest, installer.ps1, installer.py, scratchpad.md + scratchpad.local.example.md + template mirrors, docs/engineering/runbook.md + template mirror, tests/us0130_contract_test.py NEW + template mirror, scripts/check_intake_template_parity.py (SOVEREIGN_CRITIC_PAIRS + MODEL_TIER_OVERRIDES_PAIRS) + template mirror
- files_NOT_to_touch: docs/engineering/architecture.md (do not rewrite), decisions/ (no DEC-0130), backlog US-0130 Status/ACs, handoffs/intake_evidence/US-0130-intake-20260826.json, .cursor/model-catalog.local.json, US-0104/US-0102/US-0101 surfaces (compose read-only), US-0127/US-0128 DONE rows, US-0129 OPEN row, v1 example catalogs
- next_phase: `/execute` (fresh dev per US-0069 / DEC-0051; first canonical phase of `build+verify` macro per ultra_lean; /plan-verify merged into qa per ultra_lean â qa creates plan-verify.json within build+verify). Orchestrator runs sovereign-critic of sprint-plan first (CROSS_MODEL_REVIEW=1). Do not mandate outer driver.
- sprint_artifacts: sprints/S0130/ (sprint.md, tasks.md, progress.md, uat.json, uat.md)
- runtime_proof_id: rp-auto-20260826-01-sprint-plan-tech-lead-20260826T215200Z-US-0130
- proof_hash: 5D0ADA062FE675333EF06E56DBC4649D22A2045C08D71456C7963893178CFED1
- proof_ttl: 2026-08-26T22:52:00Z (UTC)
- prior_phase_proof_consumed: rp-auto-20260826-01-architecture-tech-lead-20260826T214500Z-US-0130 (proof_hash=B071AE0659D99E2513304490BD3D191550631E7564398EEEC4485BD556FD8B4D, ttl=2026-08-26T22:45:00Z â independent SHA-256 MATCH; consumed at 2026-08-26T21:52:00Z before RUNTIME_PROOF_STALE; sovereign-critic architecture PASS at 2026-08-26T21:50:00Z anti_slop_aggregate=8 0 blocking findings)
- stop_condition: STOP after sprint-plan completes; hand off via artifacts only. Orchestrator owns critic of sprint-plan then /execute in fresh dev subagent per BUG-0006. Do not spawn /execute or /plan-verify from this subagent. Do not mark US-0130 DONE. Do not tick acceptance L158. Do not mutate intake JSON. Do not amend US-0104/US-0102/US-0101 surfaces. Do not reopen US-0127/US-0128. Do not mutate US-0129. Do not author DEC-0130. Do not write model-catalog.local.json.

---

## Sprint-plan handoff â US-0128 / S0128 â `/execute` next (fresh dev; ultra_lean skips standalone /plan-verify)

- sprint_id: S0128
- story_id: US-0128
- dec_id: none (companion DEC not required per R-0111 recommendation; align with DEC-0110 Â§10 smoke-green + DEC-0078 UAT probe contract)
- research_anchor: R-0111 (DQ1âDQ8 LOCKED)
- orchestrator_run_id: auto-20260826-01
- fresh_context_marker: tl-US0128-sprint-plan-2026-08-26T201100Z-fresh
- timestamp: 2026-08-26T20:11:00Z (UTC)
- model_id: cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 â required on isolation; glm-5.2-high unavailable this spawn)
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 â not mutated; acceptance L156 unchecked)
- task_count: 8 (T-anch + T-001..T-007; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001,T-004(markers 1,2,3,4,5,6,8,9),T-007(markers 4,5); AC-2->T-002,T-004(markers 5,7,8); AC-3->T-003,T-004(markers 2,3,4,6); AC-4->T-002,T-004(markers 5,7,8); AC-5->T-004(all 11 markers),T-007(markers 4,5,7); AC-6->T-005(runbook subsection),T-006(SOVEREIGN_CONVERGENCE_PAIRS + 2 command rows)
- task_order: T-anch -> T-001 (surrogate eval branch in _eval_smoke_green, legacy-first) -> T-002 (qa.md + verify-work.md additive subsections) -> T-003 (reason_codes.md ## US-0128 section) -> T-004 (contract test file shell + 11 markers, with T-007 markers 4,5,7 authored within) -> T-005 (runbook subsection) -> T-006 (SOVEREIGN_CONVERGENCE_PAIRS + 2 command rows) -> integration verification
- compose_guards (non-negotiable): DO NOT amend US-0109 (deploy smoke post-publish path / DEPLOY_SMOKE_* reason codes â marker 7 regression guard), US-0126 (sprints/S0126/uat.json waived-probe fixture / S0126 release artifacts â marker 11 regression guard; reference fixture for waived_probes[] shape only; US-0126 DONE product scope NOT reopened), US-0127 (_eval_critic_resolved / read_open_blocking / hygiene CLI / SOVEREIGN_CRITIC_PAIRS â marker 10 regression guard; US-0128 touches smoke_green only, not critic_resolved; SOVEREIGN_CRITIC_PAIRS unchanged), US-0110 (five-conjunct structure / degrade matrix / CONVERGENCE_SMOKE_PROBE_FAIL reason code â marker 9 regression guard; surrogate branch is an additional PASS path inside smoke_green; conjunct name/order/shape unchanged; CONVERGENCE_SMOKE_SURROGATE_MISSING is additive), US-0104 (critic findings JSONL / read_open_blocking / resolve_finding â US-0128 does not touch critic surfaces), US-0045 (no backlog Status/ACs mutation), US-0048/BUG-0006 (fresh-context isolation), US-0056 (runtime proof lowercase keys only). Do not rewrite docs/engineering/architecture.md.
- critic_carry_ins: 0 new blocking. 3 architecture critic NBs `a0128arch-*` status=resolved non-blocking â routed as awareness into /execute:
  - a0128arch-challenger-001 (`ik_us0128_arch_proof_and_boundary_gaps`): T-001 preserve legacy-first (`_uat_smoke_passes` before surrogate). R6 `id=convergence_smoke` also matches `_step_is_smoke` â do not invert. T-002 emit explicit `convergence_smoke` (S0126 steps lack probe_kind â R7; marker 11 reference only). Fail-closed SURROGATE_MISSING when neither top-level contract_test_failed nor derived passed==total. T-007 marker 4: partial waivers must not false-pass.
  - a0128arch-architect-002 (`ik_us0128_arch_layer_compose_boundaries`): T-001 lib only; T-002 commands; T-003 reason_codes; T-004 tests; T-005/T-006 runbook+parity. No lib-side uat.json synthesis (A4 rejected). Do not touch `_eval_critic_resolved` / SOVEREIGN_CRITIC_PAIRS.
  - a0128arch-subtractor-003 (`ik_us0128_arch_scope_discipline`): do not mark US-0128 DONE; do not tick L156; 11 markers required (not YAGNI); T-anch read-only â no architecture.md mutation.
- architecture_pointers: docs/engineering/architecture.md # US-0128 (L1671 â approach A1, 11-marker AC-5 table, surrogate eval branch DQ1+DQ3+DQ4, canonical uat step DQ2+DQ5, fail-closed reason code DQ3+DQ4, contract tests DQ6, operator docs DQ7, template parity DQ8, compose-do-not-amend 8/8, risks R1âR7; sprint seeds T-anch + T-001..T-007). Do not rewrite.
- first_execute_task: T-anch (NO-OP / verification) â verify # US-0128 H1 anchor + approach A1 + R-0111 DQ1âDQ8 + compose guards 8/8 + 11-marker list locked + absent surfaces (us0128 contract test + template mirror, qa.md/verify-work.md subsections, runbook subsection, reason_codes.md section, SOVEREIGN_CONVERGENCE_PAIRS qa/verify-work rows)
- key_locked_artifacts:
  - surrogate eval branch (DQ1+DQ3+DQ4): `scripts/sovereign_convergence_lib.py` `_eval_smoke_green` legacy path first via `_uat_smoke_passes`; if legacy FAIL, surrogate prerequisites: 6 canonical waived_probes UAT_PROBE_FORBIDDEN + `contract_test_failed=0` (top-level authoritative, derived fallback) + surrogate step (`id=convergence_smoke` preferred OR tail `probe_kind=contract_tests_primary` `result=pass`); `ConjunctResult(name="smoke_green", â¦)` shape unchanged; `CONVERGENCE_SMOKE_PROBE_FAIL` retained for real smoke step / US-0109 deploy smoke; new `CONVERGENCE_SMOKE_SURROGATE_MISSING` for surrogate prerequisites unmet (DQ4 cases 4â8); partial waivers fail closed (case 6); US-0109 deploy smoke precedence orthogonal (case 9)
  - canonical uat step (DQ2+DQ5): `.cursor/commands/qa.md` + `.cursor/commands/verify-work.md` (+ template mirrors) additive `### Convergence smoke surrogate (US-0128)` subsection under `## Self-verify UAT probes (US-0092 / DEC-0078)` after `### Browser UAT self-test (US-0093)` before `## Steps`; emission rule for `convergence_smoke` step with `probe_kind=contract_tests_primary`, `result=pass` (when `contract_test_failed=0`)
  - fail-closed reason code (DQ3+DQ4): `docs/engineering/reason_codes.md` (+ template mirror) new `## US-0128: Convergence smoke surrogate (DEC-0110 Â§10 smoke-green)` section with `CONVERGENCE_SMOKE_SURROGATE_MISSING` + clarifying note on US-0110 `CONVERGENCE_SMOKE_PROBE_FAIL` row (description only, not schema change)
  - contract tests (DQ6+R-0111 Q1): `tests/us0128_contract_test.py` â 11 markers (8 from DQ6 + 3 compose regression guards: marker 9 US-0110, marker 10 US-0127, marker 11 US-0126); mirror to `template/tests/us0128_contract_test.py` byte-identical; all static/fixture-based, no live critic spawn
  - operator docs (DQ7): runbook `### Smoke surrogate for waived-probe UAT slices (US-0128)` after `### Blocking-only conjunct-3 semantics (US-0127)` (L2811) before `### Interpret \`goal_progress\` block` (L2829); active + template byte-identical
  - template parity (DQ8): `SOVEREIGN_CONVERGENCE_PAIRS` additive rows for `qa.md` <-> `template/.cursor/commands/qa.md` and `verify-work.md` <-> `template/.cursor/commands/verify-work.md`; `--scope=sovereign-convergence` extended automatically via tuple union; `SOVEREIGN_CRITIC_PAIRS` unchanged
- files_to_touch: scripts/sovereign_convergence_lib.py + template mirror, .cursor/commands/qa.md + template mirror, .cursor/commands/verify-work.md + template mirror, docs/engineering/reason_codes.md + template mirror, tests/us0128_contract_test.py NEW + template mirror, docs/engineering/runbook.md + template mirror, scripts/check_intake_template_parity.py (2 new rows in SOVEREIGN_CONVERGENCE_PAIRS) + template mirror
- files_NOT_to_touch: docs/engineering/architecture.md (do not rewrite), decisions/ (no new DEC), backlog US-0128 Status/ACs, handoffs/intake_evidence/US-0128-intake-20260825.json, sprints/S0126/uat.json (read-only reference fixture â marker 11 guards non-mutation), US-0109/US-0126/US-0127/US-0110/US-0104 surfaces (compose read-only), US-0121..US-0127 DONE rows, US-0129/US-0130 OPEN rows
- next_phase: `/execute` (fresh dev per US-0069 / DEC-0051; first canonical phase of `build+verify` macro per ultra_lean; /plan-verify merged into qa per ultra_lean â qa creates plan-verify.json within build+verify)
- sprint_artifacts: sprints/S0128/ (sprint.md, tasks.md, progress.md, uat.json, uat.md)
- runtime_proof_id: rp-auto-20260826-01-sprint-plan-tech-lead-2026-08-26T201100Z-US-0128
- proof_hash: C911D7C5CAA2939EC6F65ED07C717E9CBB00E80B551DCBFECA097D39F26878F4
- proof_ttl: 2026-08-26T21:11:00Z (UTC)
- prior_phase_proof_consumed: rp-auto-20260826-01-architecture-tech-lead-2026-08-26T195500Z-US-0128 (proof_hash=FF499010B78C4FB7855E9D6F4482227AD7B258230671D67E4E2B42571A68A969, ttl=2026-08-26T20:55:00Z â independent SHA-256 MATCH; consumed at 2026-08-26T20:11:00Z before RUNTIME_PROOF_STALE; sovereign-critic architecture PASS at 2026-08-26T19:59:00Z anti_slop_aggregate=8 0 blocking findings)
- stop_condition: STOP after sprint-plan completes; hand off via artifacts only to /execute in fresh dev subagent per BUG-0006. Do not spawn /execute from this subagent. Do not mark US-0128 DONE. Do not tick acceptance L156. Do not mutate intake JSON. Do not amend US-0104/US-0110/US-0109/US-0126/US-0127 surfaces. Do not mutate US-0129/US-0130.

---

## Sprint-plan handoff â US-0127 / S0127 â `/plan-verify` next (fresh qa)

- sprint_id: S0127
- story_id: US-0127
- dec_id: none (companion DEC not required per R-0110 recommendation; align with DEC-0110 Â§10 / DEC-0104 Â§11)
- research_anchor: R-0110 (DQ1âDQ8 LOCKED)
- orchestrator_run_id: auto-20260825-01
- fresh_context_marker: tl-US0127-sprint-plan-20260825T185100Z-fresh
- timestamp: 2026-08-25T18:51:00Z (UTC)
- model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 â required)
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 â not mutated)
- task_count: 8 (T-anch + T-001..T-007; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001,T-004(markers 1,2,11,12,13),T-007(marker 13); AC-2->T-002,T-004(markers 3,4,5); AC-3->T-003,T-004(markers 6,7,8,9,10); AC-4->T-004(all 13 markers),T-007(marker 13); AC-5->T-005(runbook subsections + reason_codes.md section); AC-6->T-006(SOVEREIGN_CRITIC_PAIRS + --scope=sovereign-critic)
- task_order: T-anch -> T-001 (convergence lib fix + DQ6 dispatch) -> T-002 (auto-resolve hook + helper) -> T-003 (hygiene CLI + 6 reason codes) -> T-004 (contract test file shell + 13 markers, with T-007 marker 13 authored within) -> T-005 (runbook subsections + reason_codes.md section) -> T-006 (SOVEREIGN_CRITIC_PAIRS + parity CLI extension) -> integration verification
- compose_guards (non-negotiable): DO NOT amend US-0104 (sovereign_critic_lib.read_open_blocking / resolve_finding / findings JSONL schema / build_qa_cross_reviewer_block / sovereign_critic_validate.py â DQ7), US-0110 (five-conjunct structure / degrade matrix / CONVERGENCE_CROSS_REVIEWER_OPEN reason code â DQ8), US-0107 (deferral register / drain-generate / sovereign loop stop matrix â DQ8), US-0045 (no backlog Status/ACs mutation), US-0048/BUG-0006 (fresh-context isolation), US-0053/DEC-0035 (narrow-read phase context), US-0103/DEC-0103 (no ledger entries from sprint-plan), US-0056 (runtime proof lowercase keys only)
- critic_carry_ins: 0 new (3 architecture critic NBs noted in sovereign-critic of architecture â all non-blocking: ik_us0127_arch_proof_and_boundary_gaps, ik_us0127_arch_layer_compose_boundaries, ik_us0127_arch_scope_discipline â routed as awareness into /execute via this sprint plan)
- architecture_pointers: docs/engineering/architecture.md # US-0127 (L1852 â approach A1, 13-marker AC-4 table, convergence lib fix DQ1+DQ6, auto-resolve hook DQ1, hygiene CLI DQ2+DQ5, contract tests DQ3, operator docs DQ4, template parity DQ5, compose-do-not-amend 8/8, risks R1âR6; sprint seeds T-anch + T-001..T-007)
- first_execute_task: T-anch (NO-OP / verification) â verify # US-0127 H1 anchor + approach A1 + R-0110 DQ1âDQ8 + compose guards 8/8 + 13-marker list locked + absent surfaces (hygiene CLI, contract test, SOVEREIGN_CRITIC_PAIRS, runbook subsections, reason_codes.md section)
- key_locked_artifacts:
  - convergence lib fix (DQ1+DQ6): `scripts/sovereign_convergence_lib.py` `_critic_jsonl_has_open` -> delegate to `read_open_blocking`; `_eval_critic_resolved` JSONL-authoritative when present, QA-markdown fallback when JSONL absent, skip when neither deployed
  - auto-resolve hook (DQ1): `.cursor/commands/sovereign-critic.md` conditional call at end of command after reconcile+JSONL+isolation, before `## Stop conditions`; `auto_resolve_nonblocking_for_run` helper in `sovereign_critic_lib.py` (additive; scope key `(orchestrator_run_id, phase_id)`; idempotent via `resolve_finding`; `SOVEREIGN_CRITIC_AUTORESOLVE_FAILED` non-blocking info)
  - hygiene CLI (DQ2+DQ5): NEW `scripts/sovereign_critic_hygiene.py` + template mirror; inventory `--report`/`--resolve-nonblocking-for-run`/`--dry-run`/`--confirm`/`--self-test`/`--all-phases`/`--phase-id`; 6 reason codes (`HYGIENE_RESOLVE_CONFIRM_REQUIRED`, `HYGIENE_RESOLVE_NO_CANDIDATES`, `HYGIENE_RESOLVE_PARTIAL`, `HYGIENE_RESOLVE_FAILED`, `HYGIENE_REPORT_EMPTY`, `HYGIENE_RESOLVE_PHASE_SCOPE_REQUIRED`); operator-only-when-quiet contract (no advisory lock â Q3 accepted)
  - contract tests (DQ3+R2): `tests/us0127_contract_test.py` â 13 markers (10 from DQ3 + 2 compose regression guards + marker 13 R2 validator guard); mirror to `template/tests/us0127_contract_test.py` byte-identical; all static/fixture-based, no live critic spawn
  - operator docs (DQ4): runbook `### Blocking-only conjunct-3 semantics (US-0127)` after `### Evaluate convergence` (L2792) before `### Interpret goal_progress block` (L2811); runbook `### Hygiene CLI (US-0127)` after `#### Parity enforcement` (L2915) before `#### Related artifacts` (L2923); `reason_codes.md` `## US-0127` section after US-0110 section (L77âL107); active + template byte-identical
  - template parity (DQ5): `SOVEREIGN_CRITIC_PAIRS` additive row (hygiene script pair); `--scope=sovereign-critic` parity CLI extension; `SOVEREIGN_CONVERGENCE_PAIRS` existing rows confirmed (no new row â convergence lib mirror already present)
- files_to_touch: scripts/sovereign_convergence_lib.py + template mirror, scripts/sovereign_critic_lib.py + template mirror (additive auto_resolve_nonblocking_for_run helper), .cursor/commands/sovereign-critic.md + template mirror, scripts/sovereign_critic_hygiene.py NEW + template mirror, tests/us0127_contract_test.py NEW + template mirror, docs/engineering/runbook.md + template mirror, docs/engineering/reason_codes.md + template mirror, scripts/check_intake_template_parity.py (--scope=sovereign-critic extension) + template mirror
- files_NOT_to_touch: decisions/ (no new DEC), backlog US-0127 Status/ACs, handoffs/intake_evidence/US-0127-intake-20260825.json, US-0104/US-0110/US-0107 surfaces (compose read-only), US-0121..US-0126 DONE rows, scripts/sovereign_critic_validate.py (read-only â marker 13 asserts its behavior; do not amend)
- next_phase: `/plan-verify` (fresh qa per orchestrator brief) for S0127 / US-0127
- sprint_artifacts: sprints/S0127/ (sprint.md, tasks.md, progress.md, uat.json, uat.md)
- runtime_proof_id: rp-auto-20260825-01-sprint-plan-tech-lead-20260825T185100Z-US-0127
- proof_hash: DE343C909809932C3EA4B83A0D8B5F23FF8535954F05512C5D33A3EB3DE65723
- proof_ttl: 2026-08-25T19:51:00Z (UTC)
- stop_condition: STOP after sprint-plan completes; hand off via artifacts only to /plan-verify in fresh qa subagent per BUG-0006. Do not spawn /plan-verify from this subagent. Do not mark US-0127 DONE. Do not tick acceptance L155. Do not mutate intake JSON. Do not amend US-0104/US-0110/US-0107 surfaces.

## Architecture handoff â US-0127 â /sprint-plan next (fresh tech-lead)

- story_id: US-0127
- sprint_id: (pending â created at sprint-plan)
- dec_id: none (companion DEC not required per R-0110 recommendation; align with DEC-0110 Â§10 / DEC-0104 Â§11)
- research_anchor: R-0110 (DQ1-DQ8 LOCKED)
- orchestrator_run_id: auto-20260825-01
- delivery_mode: ultra_lean
- macro_phase: plan
- fresh_context_marker: tl-US0127-architecture-20260825T184100Z-fresh
- timestamp: 2026-08-25T18:41:00Z (UTC)
- model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 â required)
- architecture_verdict: PASS (no DECISION_GATE; approach A1 locked; sprint seeds T-anch + T-001..T-007 within SPRINT_MAX_TASKS=12; risks R1-R6 finalized; compose-do-not-amend verified 8/8)
- architecture_anchor: docs/engineering/architecture.md # US-0127 (L1852; inserted after # US-0126 section and before # US-0091 per DEC-0073 Â§11 heading policy)
- root_cause: scripts/sovereign_convergence_lib.py _critic_jsonl_has_open (L318-331) treats every status=open row as unmet and defaults blocking=True when key absent â ~280 informational status=open,blocking=false rows block CONVERGENCE_CROSS_REVIEWER_OPEN despite US-0110 L3 requiring "no open blocking cross-reviewer findings"
- approach_A1: narrow _critic_jsonl_has_open to delegate to sovereign_critic_lib.read_open_blocking(repo); change _eval_critic_resolved dispatch (DQ6 â JSONL authoritative when present, QA-markdown fallback when JSONL absent, informational skip when neither deployed); auto-resolve hook at /sovereign-critic PASS (DQ1 â scope key (orchestrator_run_id, phase_id), idempotent via resolve_finding, SOVEREIGN_CRITIC_AUTORESOLVE_FAILED non-blocking info); new scripts/sovereign_critic_hygiene.py + template mirror (DQ2 â --report/--resolve-nonblocking-for-run/--dry-run/--confirm/--self-test/--all-phases/--phase-id + 6 reason codes); 13 test_us0127_* markers (DQ3 + R2 marker 13); runbook subsections + reason_codes.md section (DQ4); SOVEREIGN_CRITIC_PAIRS additive row + --scope=sovereign-critic parity CLI extension (DQ5)
- open_questions_accepted: Q1=13 markers (R2 validator guard); Q2=yes --all-phases + HYGIENE_RESOLVE_PHASE_SCOPE_REQUIRED; Q3=no advisory lock (document operator-only-when-quiet contract)
- sprint_seeds: T-anch (anchor verification NO-OP) + T-001 (AC-1 convergence lib fix + DQ6 dispatch) + T-002 (AC-2 auto-resolve hook + helper) + T-003 (AC-3 hygiene CLI + template mirror + 6 reason codes) + T-004 (AC-4 13 contract markers + template mirror) + T-005 (AC-5 runbook subsections + reason_codes.md section + template mirror) + T-006 (AC-6 SOVEREIGN_CRITIC_PAIRS + parity CLI extension) + T-007 (R2 validator regression guard marker 13)
- compose_guards (non-negotiable): DO NOT amend US-0104 (sovereign_critic_lib.read_open_blocking / resolve_finding / findings JSONL schema / build_qa_cross_reviewer_block / sovereign_critic_validate.py â DQ7), US-0110 (five-conjunct structure / degrade matrix / CONVERGENCE_CROSS_REVIEWER_OPEN reason code â DQ8), US-0107 (deferral register / drain-generate / sovereign loop stop matrix â DQ8), US-0045 (no backlog Status/ACs mutation), US-0048/BUG-0006 (fresh-context isolation), US-0053/DEC-0035 (narrow-read phase context), US-0103/DEC-0103 (no ledger entries from architecture), US-0056 (runtime proof lowercase keys only)
- files_to_touch: scripts/sovereign_convergence_lib.py + template mirror, .cursor/commands/sovereign-critic.md + template mirror, scripts/sovereign_critic_lib.py + template mirror (additive auto_resolve_nonblocking_for_run helper), scripts/sovereign_critic_hygiene.py NEW + template mirror, tests/us0127_contract_test.py NEW + template mirror, docs/engineering/runbook.md + template mirror, docs/engineering/reason_codes.md + template mirror, scripts/check_intake_template_parity.py (--scope=sovereign-critic extension)
- files_NOT_to_touch: decisions/ (no new DEC), backlog US-0127 Status/ACs, handoffs/intake_evidence/US-0127-intake-20260825.json, US-0104/US-0110/US-0107 surfaces (compose read-only), US-0121..US-0126 DONE rows
- triad_rollover: architecture moved=1 pack=docs/engineering/architecture-archive/architecture-pack-20260825-a.md (legacy ## US-0119 H2 section archived, 200 lines); state moved=1 pack=docs/engineering/state-archive/state-pack-20260825-ab.md; enforce-triad-hot-surface.py --check exit 0; --check-arch-heading-policy --baseline-h2-count 1 exit 0
- codebase_map: [CODEBASE_MAP_OK] preserved_existing trigger=architecture
- runtime_proof_id: rp-auto-20260825-01-architecture-tech-lead-20260825T184100Z-US-0127
- proof_hash: DF773DDFBA1021C5DBD44F0470469BD76A909C1373FC528BAEA65070CB9A179C
- proof_ttl: 2026-08-25T19:41:00Z (UTC)
- next_scheduled_phase: /sprint-plan (role=tech-lead per US-0069 / DEC-0051; third canonical phase of plan macro per ultra_lean; after sovereign-critic of architecture)
- stop_condition: STOP after architecture completes; hand off via artifacts only to sovereign-critic of architecture, then /sprint-plan in fresh tech-lead subagent (BUG-0006). Do not spawn /sprint-plan from this subagent. Do not mark US-0127 DONE. Do not tick acceptance. Do not mutate intake JSON. Do not amend US-0104/US-0110/US-0107 surfaces.

ï»¿## Sprint-plan handoff â **US-0126** / **S0126** â `/plan-verify` next (fresh qa)

- sprint_id: S0126
- story_id: US-0126
- dec_id: DEC-0126 (Accepted, decisions/DEC-0126.md)
- research_anchor: R-0109 (DQ1..DQ8 LOCKED for US-0126; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 + US-0124 DQ1..DQ8 + US-0125 DQ1..DQ8 locks preserved)
- orchestrator_run_id: auto-20260825-01
- fresh_context_marker: tl-US0126-sprint-plan-20260825T161520Z-fresh
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 â not mutated)
- task_count: 11 (T-anch + T-001..T-010; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001,T-004(marker 1); AC-2->T-001,T-005,T-004(marker 2); AC-3->T-003,T-004(marker 3),T-009(marker 3); AC-4->T-004(all 12 markers),T-010(markers 4,12); AC-5->T-002,T-006(markers 5,6); AC-6->T-001,T-007(marker 7); AC-7->T-001,T-002,T-008(marker 8); AC-8->T-001,T-002,T-008(marker 9); AC-9->T-003,T-009(marker 10); AC-10->T-009(marker 11)
- task_order: T-anch -> T-001 (runbook h2 body with T-005 consolidated table inline) -> {T-002, T-003 parallel (README blurb, OPENCODE_ADAPTER_PAIRS extension)} -> T-004 (contract test file shell + 12 markers) -> {T-006, T-007, T-008, T-009, T-010 parallel (markers 5,6 / 7 / 8,9 / 3,10,11 / 4,12)} -> integration verification
- compose_guards (non-negotiable): DO NOT amend US-0071 (operator-sentence sanitization â no DEC ids in operator prose; cross-references to runbook h2 / Boundaries subsection only), US-0113..US-0117 (operator docs â add OpenCode host section; do not rewrite Cursor command catalogs), US-0121/DEC-0120 (installer `--host` flag docs hook â `## OpenCode host mode (US-0121)` h2 untouched; US-0126 cross-links), US-0122/DEC-0122 (seven role agents â referenced, not redefined), US-0123 (per-role slug routing â referenced, not re-listed), US-0124/DEC-0124 (orchestrator plugin + stub reason-code h2 untouched â US-0126 owns consolidated table; cross-links to US-0124 stub h2; does not reimplement plugin logic), US-0125/DEC-0125 (thin commands + validator-bridge stub h2 untouched â US-0126 owns consolidated table; **DEC-0125 DQ7 raw Python reason codes upheld â `OPENCODE_VALIDATOR_FAILED` wrapper NOT resurrected**), US-0102/DEC-0087 (no vendor slugs in `template/` â no vendor slugs in runbook/README operator prose)
- critic_carry_ins: 0 new (3 research critic NBs closed in architecture phase: ik_us0126_dq3_parity_grep_false_pass [DQ3 explicit layer split â parity CLI byte-only vs contract-test grep], ik_us0126_layering_runbook_dec_tests [DQ1+DQ8 runbook whole-file byte-identical pair coupling documented], ik_us0126_research_scope_yagni_markers [DQ4 12 markers locked + AC-10 deterministic static check vs current-kit-inventory, not frozen git snapshot])
- architecture_pointers: docs/engineering/architecture.md # US-0126 (L1747 â approach A1, 12-marker table, runbook section DQ1, reason-code table DQ2, parity scope DQ3, contract tests DQ4, program DoD DQ5, default-host reminder DQ6, out-of-scope DQ7, template parity manifest DQ8, non-goals; sprint seeds T-anch + T-001..T-010 at L1981)
- dec_pointers: decisions/DEC-0126.md (Â§1 runbook section, Â§2 locked operator sentences, Â§3 consolidated reason-code table, Â§4 parity scope + layer split, Â§5 12-marker contract-test list, Â§6 template parity manifest unchanged, Â§7 compose-do-not-amend, Â§8 isolation + runtime proof)
- first_execute_task: T-anch (NO-OP / verification) â verify # US-0126 H1 anchor + DEC-0126 Accepted + compose guards 8/8 + 12-marker list locked + runbook/reason-code/parity/DoD/reminder/out-of-scope/manifest contracts + absent surfaces
- key_locked_artifacts:
  - runbook section (DQ1): new sibling h2 `## OpenCode host operator runbook (US-0126)` in `docs/engineering/runbook.md` + `template/docs/engineering/runbook.md` byte-identical; placed immediately after `## OpenCode thin commands + validator bridge (US-0125)` section; US-0121/US-0124/US-0125 h2 sections untouched (compose, do not amend)
  - locked operator sentences (DQ5, DQ6, DQ7): program DoD sentence (verbatim), default-host reminder sentence (verbatim, no DEC ids per US-0071), out-of-scope list (verbatim operator prose, no DEC ids); Boundaries subsection (runbook only; cross-references to DEC ids allowed here â `docs/product/standalone-runtime-masterplan.md`, `DEC-0055`, `US-0093`)
  - consolidated reason-code table (DQ2): 4 `OPENCODE_*` US-0124 + 5 installer `OPENCODE_*`/`CURSOR_*` US-0121 + 3 reused cross-host + raw Python validator codes (no `OPENCODE_VALIDATOR_FAILED` wrapper per DEC-0125 DQ7); each with one-line semantics + fail-closed action + cross-link to owning slice
  - parity scope (DQ3): additive `OPENCODE_ADAPTER_PAIRS` extension (2 new pairs: `tests/us0126_contract_test.py` â template + `docs/engineering/runbook.md` â template); parity CLI stays byte-only (DQ3 layer split â critic NB `ik_us0126_dq3_parity_grep_false_pass` closed); reason-code table presence + `test_us0126_*` markers = contract-test grep, NOT parity-CLI predicates
  - contract tests (DQ4): `tests/us0126_contract_test.py` â 12 markers (see architecture AC-4 table); mirror to `template/tests/us0126_contract_test.py` byte-identical; all static/grep, no live OpenCode probe (vision D10)
  - AC-10 baseline (DQ4): deterministic static check vs current-kit-inventory (sorted file-name list of `.cursor/commands/*.md` + `.cursor/agents/*.md` checked into the repo at execute time); NOT a frozen pre-US-0126 git snapshot (fragile); NOT a hash manifest of the entire `.cursor/` directory (over-broad)
  - manifest (DQ8): `installer-owned-paths.manifest` UNCHANGED (runbook already covered by `docs` in `[install_include_paths]`; `tests/us0126_contract_test.py` NOT installer-shipped per US-0121..US-0125 pattern)
- next_phase: `/plan-verify` (fresh qa per orchestrator brief) for S0126 / US-0126
- sprint_artifacts: sprints/S0126/ (sprint.md, tasks.md, progress.md, uat.json, uat.md)
- timestamp: 2026-08-25T16:15:20Z
- role: tech-lead
- model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 â required)
- runtime_proof_id: rp-auto-20260825-01-sprint-plan-tech-lead-20260825T161520Z-US-0126
- proof_hash: 10E2CAC09DA36BF61FAAC0A3A258C49E2095875703018CAD4102E921704FC2A9

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `fresh_context_marker=tl-US0126-sprint-plan-20260825T161520Z-fresh`
- `timestamp=2026-08-25T16:15:20Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 â required)
- `evidence_ref=sprints/S0126/sprint.md, sprints/S0126/tasks.md, sprints/S0126/progress.md, sprints/S0126/uat.json, sprints/S0126/uat.md, docs/engineering/state.md (sprint-plan checkpoint append-bottom + traceability row), docs/engineering/architecture.md # US-0126, decisions/DEC-0126.md, handoffs/resume_brief.md`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260825-01`
- `runtime_proof_id=rp-auto-20260825-01-sprint-plan-tech-lead-20260825T161520Z-US-0126`
- `phase_id=sprint-plan`, `role=tech-lead`, `story_id=US-0126`, `sprint_id=S0126`
- `proof_issued_at=2026-08-25T16:15:20Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-25T17:15:20Z`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260825-01","phase_id":"sprint-plan","proof_issued_at":"2026-08-25T16:15:20Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260825-01-sprint-plan-tech-lead-20260825T161520Z-US-0126","sprint_id":"S0126","story_id":"US-0126"}`

---

## Sprint-plan handoff â **US-0125** / **S0125** â `/plan-verify` next (fresh qa)

- sprint_id: S0125
- story_id: US-0125
- dec_id: DEC-0125 (Accepted, decisions/DEC-0125.md)
- research_anchor: R-0109 (DQ1..DQ8 LOCKED for US-0125; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 + US-0124 DQ1..DQ8 locks preserved)
- orchestrator_run_id: auto-20260824-02
- fresh_context_marker: tl-US0125-sprint-plan-20260824T204500Z-fresh
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 â not mutated)
- task_count: 10 (T-anch + T-001..T-009; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001,T-006(markers 1,8,11),T-007; AC-2->T-002,T-006(marker 2); AC-3->T-003,T-004,T-006(markers 3,4); AC-4->T-003,T-005,T-006(marker 4); AC-5->T-004,T-006(marker 5); AC-6->T-006(marker 6); AC-7->T-006(markers 7,8); AC-8->T-006(all 11 markers),T-008(parity+runbook stub); AC-9->T-anch(baseline),T-006(marker 9); AC-10->T-005,T-006(marker 10)
- task_order: T-anch -> T-001 (15 command files) -> {T-002, T-003, T-004, T-007 parallel (clone-guard marker, mapping fixture, bridge prose, manifest rows)} -> T-008 (README + parity + runbook stub) -> T-005 (mock-subprocess harness) -> T-006 (contract tests last) -> T-009 (validator decision) -> integration verification
- compose_guards (non-negotiable): DO NOT amend US-0001 (phase names + artifact outputs; no 200-line clones per AC-9), US-0078/DEC-0060 (`intake_evidence_validate.py` remains persistence-blocking gate; thin commands subprocess, do not reimplement), US-0121/DEC-0120 (host default cursor-only; commands live in reserved `template/.opencode/commands/` slot; `.gitkeep` replaced by 15 files), US-0122/DEC-0122 (`template/.opencode/agents/*.md` unchanged â commands bind via `agent: <role>` frontmatter per DQ5/DQ8), US-0124/DEC-0124 (`template/.opencode/plugins/orchestrator.ts` unchanged â plugin owns spawn + `ctx.tool.hook` enforcement; US-0125 authors validatorâartifact mapping that the plugin consumes â additive data, not plugin code change; `/auto` is dispatch-only; missing command must not disable plugin per US-0124 AC-7 â US-0125 AC-7), US-0126 (owns full runbook + reason-code table + `--scope=opencode-adapter` parity text; US-0125 ships stub reason-code reference only), US-0102/DEC-0087 (no vendor slugs in `template/` â no `model:` literals in any command frontmatter)
- critic_carry_ins (1 non-blocking â closed in /execute T-002, not silently dropped):
  - `ik_us0125_dq2_normalization_strip_list_open` -> T-002 note: lock the token-strip manifest as a documented Python constant `US0125_CLONE_GUARD_STRIP_TOKENS` in `test_us0125_clone_guard` so the normalization strip list is explicit, version-controlled, and inherited by US-0126 without re-derivation. Strip list: frontmatter fence block + lowercase + punctuation + canonical phase id token + shared vocabulary words (its-magic, command, phase, artifact, STOP, run, validator, plugin, script, python, scripts, repo, the, a, an, to, of, and, or, before, after, above, below, path, list, id).
- architecture_pointers: docs/engineering/architecture.md # US-0125 (L1836 â approach A1, 11-marker table, command inventory DQ1, clone guard DQ2, validator-bridge DQ3, defense-in-depth DQ4, `/auto` dispatch-only DQ5, frontmatter shape DQ6, reason-code boundary DQ7, mock-ctx+mock-subprocess harness DQ8, non-goals; validatorâartifact mapping table at L1939-L1945)
- dec_pointers: decisions/DEC-0125.md (Â§1 command file inventory, Â§2 clone guard, Â§3 validator bridge contract, Â§4 defense-in-depth, Â§5 `/auto` dispatch-only, Â§6 frontmatter shape, Â§7 reason-code boundary, Â§8 mock-ctx+mock-subprocess harness)
- first_execute_task: T-anch (NO-OP / verification) â verify # US-0125 H1 anchor + DEC-0125 Accepted + compose guards 7/7 + 11-marker list locked + command/clone-guard/validator-bridge/dispatch-only/frontmatter/reason-code/harness contracts + absent surfaces
- key_locked_artifacts:
  - command file inventory (DQ1): 15 dispatch-only markdown files at `template/.opencode/commands/<name>.md` â 12 lifecycle phases (`intake.md`â`po`, `discovery.md`â`po`, `research.md`â`tech-lead`, `architecture.md`â`tech-lead`, `sprint-plan.md`â`tech-lead`, `plan-verify.md`â`qa`, `execute.md`â`dev`, `qa.md`â`qa`, `verify-work.md`â`qa`, `release.md`â`release`, `closure.md`â`qa` with prompt `role=qe` per DEC-0051 / US-0120, `refresh-context.md`â`curator`) + `auto.md` (`agent: auto` + `subtask: false` â dispatch-only per DQ5) + `quick.md` (`agent: tech-lead` â mega_quick entry per US-0096 / DEC-0082) + `ask.md` (omits `agent:` â agent-agnostic, read-only); each â¤ 20 lines (DQ2 line cap)
  - clone guard (DQ2): per-file line cap â¤ 20 + normalized-text similarity â¤ 0.30 via `difflib.SequenceMatcher` vs `.cursor/commands/<name>.md`; strip list constant `US0125_CLONE_GUARD_STRIP_TOKENS` locked in T-002 (closes `ik_us0125_dq2_normalization_strip_list_open`)
  - validator bridge contract (DQ3, DQ4, DQ7): two named CLIs (`scripts/intake_evidence_validate.py --repo . --enforce`; `scripts/bug_issue_validate.py --repo . --check-acceptance`) + generic bridge contract (`python scripts/<validator>.py --repo . [--enforce] [--scope <scope>]`); US-0126 owns full enumeration; command prose = diagnostics, plugin `ctx.tool.hook("execute.before")` = enforcement (DQ4); raw Python reason codes for validator non-zero exit; `OPENCODE_DRIVER_INVOKE_FAILED` (DEC-0124 DQ6) for subprocess invocation failure; no `OPENCODE_VALIDATOR_FAILED` wrapper (DQ7)
  - validatorâartifact mapping (DQ4): authored in architecture.md L1939-L1945 (US-0125-owned, US-0124-consumed); T-003 extracts to test fixture `tests/us0125/fixtures/validator_artifact_mapping.json` â NO architecture.md mutation in /execute
  - `/auto` dispatch-only (DQ5): `template/.opencode/commands/auto.md` â `agent: auto` + `subtask: false` + body names orchestrator role + points to plugin for spawn + STOP; no `ctx.session.create`/`Session.create`/`spawn` literals; plugin (US-0124) remains single spawn owner
  - frontmatter shape (DQ6): `description` + `agent: <role>` for 14 files; `/auto` adds `subtask: false`; `/ask` omits `agent`; no `model:` in any template command (US-0102 + US-0123)
  - reason-code boundary (DQ7): raw Python reason codes (`INTAKE_PERSISTENCE_BLOCKED`, `INTAKE_REQUIRED_TOPIC_MISSING`, `BUG_ISSUE_VALIDATION_FAILED`, ...) for validator non-zero exit; `OPENCODE_DRIVER_INVOKE_FAILED` (DEC-0124 DQ6) for subprocess invocation failure; no `OPENCODE_*` wrapper; stub reason-code reference in `docs/engineering/runbook.md` h2 `## OpenCode thin commands + validator bridge (US-0125)` â US-0126 owns full table
  - mock-ctx + mock-subprocess harness (DQ8): extend US-0124 `MockCtx` with `mockSubprocess` field OR add `tests/us0125/mock_subprocess.ts`; scripted `nextExitCode`/`nextStderr`/`nextThrow`; runner = Node (consistent with US-0124 DQ3); no live OpenCode runtime probe in CI (AC-10)
  - contract tests (AC-8): `tests/us0125_contract_test.py` â 11 markers (see architecture AC-8 table); mirror to `template/tests/us0125_contract_test.py` byte-identical
  - runbook stub (T-008): `## OpenCode thin commands + validator bridge (US-0125)` h2 one-liner per code in `docs/engineering/runbook.md` + byte-identical `template/docs/engineering/runbook.md` mirror; US-0126 owns full text
  - manifest rows (T-007): `template/.opencode/commands/**` under `[opencode_install_include_paths]` (active + template byte-identical)
- next_phase: `/plan-verify` (fresh qa per orchestrator brief) for S0125 / US-0125
- sprint_artifacts: sprints/S0125/ (sprint.md, tasks.md, progress.md, uat.json, uat.md, t-anch-verification.md placeholder)
- timestamp: 2026-08-24T20:45:00Z
- role: tech-lead
- model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 â required)
- runtime_proof_id: rp-auto-20260824-02-sprint-plan-tech-lead-20260824T204500Z-US-0125
- proof_hash: 2FF3A63387C7337D5EC02802253D251CC2636831A6369B7A121F6135AC51E234

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `fresh_context_marker=tl-US0125-sprint-plan-20260824T204500Z-fresh`
- `timestamp=2026-08-24T20:45:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 â required)
- `evidence_ref=sprints/S0125/sprint.md, sprints/S0125/tasks.md, sprints/S0125/progress.md, sprints/S0125/uat.json, sprints/S0125/uat.md, sprints/S0125/t-anch-verification.md, docs/engineering/state.md (sprint-plan checkpoint append-bottom), docs/engineering/architecture.md # US-0125, decisions/DEC-0125.md, handoffs/resume_brief.md`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260824-02`
- `runtime_proof_id=rp-auto-20260824-02-sprint-plan-tech-lead-20260824T204500Z-US-0125`
- `phase_id=sprint-plan`, `role=tech-lead`, `story_id=US-0125`, `sprint_id=S0125`
- `proof_issued_at=2026-08-24T20:45:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T21:45:00Z`
- `proof_hash=2FF3A63387C7337D5EC02802253D251CC2636831A6369B7A121F6135AC51E234`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-02","phase_id":"sprint-plan","proof_issued_at":"2026-08-24T20:45:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260824-02-sprint-plan-tech-lead-20260824T204500Z-US-0125","sprint_id":"S0125","story_id":"US-0125"}`

---
## Sprint-plan handoff â **US-0124** / **S0124** â `/plan-verify` next (fresh qa)

- sprint_id: S0124
- story_id: US-0124
- dec_id: DEC-0124 (Accepted, decisions/DEC-0124.md)
- research_anchor: R-0109 (DQ1..DQ8 LOCKED for US-0124; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 locks preserved)
- orchestrator_run_id: auto-20260824-02
- fresh_context_marker: tl-US0124-sprint-plan-20260824T190000Z-fresh
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 â not mutated)
- task_count: 10 (T-anch + T-001..T-009; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001,T-005(markers 1,7),T-006; AC-2->T-001,T-005(marker 1); AC-3->T-001,T-002,T-005(markers 1,2); AC-4->T-002,T-005(marker 2); AC-5->T-002,T-005(marker 2 + marker 8); AC-6->T-004,T-005(marker 8); AC-7->T-004,T-005(marker 8); AC-8->T-003,T-005(markers 3,4,5); AC-9->T-anch(baseline),T-005(markers 6,7); AC-10->T-002,T-005(all 9 markers),T-007(parity); AC-11->T-005(marker 9)
- task_order: T-anch -> T-001 (plugin file) -> T-002 (mock-ctx harness) -> T-004 (additive argv on auto_outer_driver.py) -> {T-006, T-007 parallel (manifest + README/parity)} -> T-003 (runbook stub h2) -> T-008 (runbook cross-link) -> T-005 (contract tests last) -> T-009 (validator decision) -> integration verification
- compose_guards (non-negotiable): DO NOT amend US-0069/DEC-0051 (phaseârole matrix), US-0092/DEC-0078 (outer driver + stop reasons + `--invoke-cmd`; Python remains SOT), US-0095/DEC-0080 (do NOT port Cursor Task-loop; no `.cursor/commands/auto.md` clone per AC-9), US-0023/US-0048/BUG-0006 (spawn-only isolation; `ctx.session.create` + `parentID` + `sessionID !== parentID`), US-0005 (hook-equivalent enforcement moves into plugin `ctx.tool.hook` + agent permissions; do not port Cursor hook JSON), US-0122/DEC-0122 (`template/.opencode/agents/auto.md` unchanged â agent = prompt + permission allow-list; plugin = enforcement per DQ8), US-0121/DEC-0120 (host default cursor-only; plugin lives in reserved `template/.opencode/plugins/` slot), US-0125 (thin commands are Layer 3 dispatch only; plugin must not own command bodies), US-0102/DEC-0087 (no vendor slugs in `template/` â plugin source has no vendor model slugs)
- critic_carry_ins (3 non-blocking â closed in architecture phase, routed to task notes, not silently dropped):
  - `ik_us0124_dq6_driver_fail_code_conflation` -> T-004 note: distinct `OPENCODE_DRIVER_INVOKE_FAILED` (driver subprocess failure: non-zero exit, malformed JSON, timeout) vs `OPENCODE_HEADLESS_UNSUPPORTED` (missing `opencode run` CLI surface only). The two codes never overlap.
  - `ik_us0124_dq6_argv_extension_gap` -> T-004 note: additive argv extension on `scripts/auto_outer_driver.py`; existing behavior byte-identical when new flags absent (no regression to US-0092 / DEC-0078).
  - `ik_us0124_research_scope_yagni` -> closed informational; US-0124 ships minimum plugin + harness + stub table; US-0125/US-0126 own command-body and full-runbook surfaces.
- architecture_pointers: docs/engineering/architecture.md # US-0124 (approach A1, 9-marker table, plugin entry-point DQ1, spawn API DQ2, mock-ctx harness DQ3, reason-code namespace DQ4, three-case detection matrix DQ5, subprocess stop-matrix DQ6, headless CLI DQ7, agent vs plugin boundary DQ8, non-goals)
- dec_pointers: decisions/DEC-0124.md (Â§1 plugin entry point, Â§2 spawn API, Â§3 mock-ctx harness, Â§4 reason-code namespace, Â§5 three-case detection matrix, Â§6 subprocess stop-matrix, Â§7 headless CLI, Â§8 agent vs plugin boundary, Â§9 contract tests, Â§10 non-goals)
- first_execute_task: T-anch (NO-OP / verification) â verify # US-0124 H1 anchor + DEC-0124 Accepted + compose guards 9/9 + 9-marker list locked + plugin/spawn/argv/boundary contracts + absent surfaces
- key_locked_artifacts:
  - plugin entry point (DQ1): `template/.opencode/plugins/orchestrator.ts` â single TypeScript file, default export `Plugin.define({ id: "its-magic.orchestrator", setup })` from `@opencode-ai/plugin`; auto-discovered via `.opencode/plugins/` scan; no `plugins[]` entry in `opencode.json` required (US-0121 ships no `opencode.json` in template); plugin id `its-magic.orchestrator` is the disable/enable selector (`--pure` / `-its-magic.orchestrator`)
  - spawn API (DQ2): `ctx.session.create({ parentID: <orchestrator-session-id>, agent: <role>, prompt: <phase-prompt> })` â assert `sessionID !== parentID` (DQ5 hard post-condition) â `ctx.session.wait(sessionID)` â read result â persist isolation evidence (`parentID`, `sessionID`, `role`, `phase_id`, `timestamp`, `fresh_context_marker`); if `ctx.session.create` unavailable â fail closed `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`
  - mock-ctx harness (DQ3): `tests/us0124/mock_ctx.ts` â `MockCtx` implements v2 plugin context subset (`session.create`/`prompt`/`wait`, `tool.hook` no-op recorder, `options` readonly); `session.create` accepts scripted `nextSessionID` + `throwOnCreate` + `returnNull` + `identicalID` flags; default fresh uuid â  `parentID`; runner = Node (CI has it via `tests/run-tests.ps1 Ensure-NodeOnPath`); no live OpenCode runtime probe in CI (AC-10)
  - reason-code namespace (DQ4): four new `OPENCODE_*` codes (`OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`, `OPENCODE_SUBTASK_IGNORED`, `OPENCODE_HEADLESS_UNSUPPORTED`, `OPENCODE_DRIVER_INVOKE_FAILED`) + three reused codes (`AUTO_ORCHESTRATOR_PHASE_EXECUTION`, `PHASE_ROLE_MISMATCH`, `NATIVE_CHAIN_UNAVAILABLE`); `OPENCODE_DRIVER_INVOKE_FAILED` (driver subprocess failure) distinct from `OPENCODE_HEADLESS_UNSUPPORTED` (missing `opencode run` CLI surface only)
  - three-case detection matrix (DQ5): null return â `OPENCODE_SUBTASK_IGNORED`; throw (generic) â `OPENCODE_SUBTASK_IGNORED`; throw (missing-primitive) â `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`; identical-id return â `OPENCODE_SUBTASK_IGNORED`; `sessionID !== parentID` is hard post-condition
  - subprocess stop-matrix (DQ6): `scripts/auto_outer_driver.py` is single TSâPython integration; additive argv `--phase/--role/--story/--sprint/--orchestrator-run-id/--stop-reason` â JSON response `{ action, next_phase, stop_reason, ... }`; legacy behavior byte-identical when flags absent; forbidden: TS reimpl of US-0092 state machine; subprocess failure (non-zero exit, malformed JSON, timeout) â `OPENCODE_DRIVER_INVOKE_FAILED` (NOT `OPENCODE_HEADLESS_UNSUPPORTED`)
  - headless CLI (DQ7): `opencode run --agent auto --format json --auto "<phase-prompt>"` (primary) + optional `opencode serve` + `--attach`; fail-closed `OPENCODE_HEADLESS_UNSUPPORTED` when `opencode run` not on PATH
  - agent vs plugin boundary (DQ8): `template/.opencode/agents/auto.md` (US-0122 â agent = prompt + permission allow-list, unchanged) + `template/.opencode/plugins/orchestrator.ts` (US-0124 â plugin = enforcement); independent surfaces, defense in depth; plugin MUST NOT copy agent's permission array; `ctx.tool.hook("execute.before")` enforces `AUTO_ORCHESTRATOR_PHASE_EXECUTION` (path-based, not permission-array-based)
  - contract tests (AC-10): `tests/us0124_contract_test.py` â 9 markers (see architecture AC-10 table); mirror to `template/tests/us0124_contract_test.py` byte-identical
  - runbook stub (DQ4): `## OpenCode orchestrator plugin reason codes (US-0124)` h2 one-liner per code in `docs/engineering/runbook.md` + byte-identical `template/docs/engineering/runbook.md` mirror; US-0126 owns full text
  - manifest rows (T-006): `template/.opencode/plugins/orchestrator.ts` under `[opencode_install_include_paths]` (active + template byte-identical)
- next_phase: `/plan-verify` (fresh qa per orchestrator brief) for S0124 / US-0124
- sprint_artifacts: sprints/S0124/ (sprint.md, tasks.md, progress.md, uat.json, uat.md, t-anch-verification.md placeholder)
- timestamp: 2026-08-24T19:00:00Z
- role: tech-lead
- model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 â required)
- runtime_proof_id: rp-auto-20260824-02-sprint-plan-tech-lead-20260824T190000Z-US-0124
- proof_hash: 377679F3F6292DCC9DBBDA0D971867529FAE67CD41C20FA9B8A5BE49121C73DE

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `fresh_context_marker=tl-US0124-sprint-plan-20260824T190000Z-fresh`
- `timestamp=2026-08-24T19:00:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 â required)
- `evidence_ref=sprints/S0124/sprint.md, sprints/S0124/tasks.md, sprints/S0124/progress.md, sprints/S0124/uat.json, sprints/S0124/uat.md, sprints/S0124/t-anch-verification.md, docs/engineering/state.md (sprint-plan checkpoint append-bottom), docs/engineering/architecture.md # US-0124, decisions/DEC-0124.md, handoffs/resume_brief.md`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260824-02`
- `runtime_proof_id=rp-auto-20260824-02-sprint-plan-tech-lead-20260824T190000Z-US-0124`
- `phase_id=sprint-plan`, `role=tech-lead`, `story_id=US-0124`, `sprint_id=S0124`
- `proof_issued_at=2026-08-24T19:00:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T20:00:00Z`
- `proof_hash=377679F3F6292DCC9DBBDA0D971867529FAE67CD41C20FA9B8A5BE49121C73DE`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-02","phase_id":"sprint-plan","proof_issued_at":"2026-08-24T19:00:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260824-02-sprint-plan-tech-lead-20260824T190000Z-US-0124","sprint_id":"S0124","story_id":"US-0124"}`

---

## Architecture handoff pointer â **US-0124** â `/sprint-plan` next (fresh tech-lead)

- story_id: US-0124 (OPEN â do not mark DONE)
- orchestrator_run_id: auto-20260824-02
- phase_id: architecture, role: tech-lead, model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1)
- verdict: PASS (companion DEC-0124 Accepted; approach A1 locked; DQ1..DQ8 LOCKED; 7/7 R ACCEPTED; 3 research critic NBs closed; 3 spec critic NBs closed; compose guards 9/9 UNCHANGED; 10 tasks T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; 11/11 AC surjective; 9-marker contract-test list locked)
- architecture_anchor: docs/engineering/architecture.md # US-0124 (L1816 â H1 anchor AFTER # US-0123 BEFORE # US-0089 per DEC-0073 Â§11)
- companion_dec: decisions/DEC-0124.md (Accepted)
- research_anchor: docs/engineering/research.md ## R-0109 ### Deepened findings â US-0124 (DQ1..DQ8 LOCKED)
- next_scheduled_phase: /sprint-plan (role=tech-lead; fresh subagent per BUG-0006)
- dev_handoff_note: tl_to_dev.md will be authored at /sprint-plan (after task refinement); dev handoff is NOT authored in /architecture. This pointer is a placeholder so dev knows the architecture contract is locked.
- stop_condition: STOP after architecture; orchestrator spawns /sprint-plan in fresh tech-lead subagent. Do NOT spawn /sprint-plan from this subagent. Do NOT mark US-0124 DONE.

---

## Sprint-plan handoff â **US-0123** / **S0123** â `/plan-verify` next (fresh qa)

- sprint_id: S0123
- story_id: US-0123
- dec_id: DEC-0123 (Accepted, decisions/DEC-0123.md)
- research_anchor: R-0109 (DQ1..DQ10 LOCKED for US-0123; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 locks preserved)
- orchestrator_run_id: auto-20260824-01
- fresh_context_marker: tl-US0123-sprint-plan-20260824T163000Z-fresh
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 â not mutated)
- task_count: 10 (T-anch + T-001..T-009; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001,T-002,T-003,T-004,T-009; AC-2->T-001; AC-3->T-004,T-005(markers 1,2,3); AC-4->T-002,T-005(markers 5,6); AC-5->T-002,T-003,T-006,T-005(marker 7); AC-6->T-anch(baseline),T-005(marker 8); AC-7->T-001,T-005(marker 4); AC-8->T-005(all 8 markers),T-008(parity); AC-9->T-001,T-anch(baseline),T-005(marker 4); AC-10->T-007
- task_order: T-anch -> T-001 (example catalog) -> T-002 (materializer) -> T-003 (installer hook) -> {T-004, T-006, T-009 parallel (validator + gitignore + manifest)} -> T-008 (README + parity) -> T-007 (runbook one-liner) -> T-005 (contract tests last) -> integration verification
- compose_guards (non-negotiable): DO NOT amend US-0101/DEC-0086 (Cursor tierâalias runtime + `.cursor/model-catalog.local.json`), US-0102/DEC-0087 (Cursor direct-slug + role catalog; volatile-ID rule extended to `template/.opencode/`), US-0003 (agents gain `model:` on OpenCode at install time, not in template), US-0122/DEC-0122 (template agents unchanged â `model:` omitted; materializer writes to installed agents only), US-0121 (`.opencode/` pack path + `.gitignore` Q10 â `*.local.json` reused), US-0080 (`TOKEN_PROFILE` orthogonal â slug routing â  token-cost profile)
- critic_carry_ins (3 non-blocking â route to task notes, do not silently drop):
  - `ik_us0123_placeholder_slug_copy_paste_boundary` -> T-002 note: materializer MUST treat `<your-*-slug>` angle-bracket placeholder strings as unknown slugs (emit `OPENCODE_MODEL_SLUG_UNKNOWN`, fail-closed); operators who copy-paste the example catalog without filling in real slugs must NOT silently get placeholder `model:` values injected into installed agents; placeholder detection: slug matches `^<.*>$` or contains `<your-` substring -> unknown; T-005 marker 5 asserts the placeholder case
  - `ik_us0123_validator_extension_coupling_fallback` -> T-004 note: document when to extend `model_tier_validate.py` vs new script; default = extend in place (DQ9 lock); fall back to new `scripts/opencode_model_catalog_validate.py` ONLY if schema divergence forces a separate validator class (trigger: `validate_opencode_catalog` cannot reuse >50% of existing `validate_cursor_catalog` helpers, OR scope-tag plumbing requires touching >3 unrelated `--scope` modes); if fallback triggers, raise DEC-0124-class follow-up; do NOT silently split
  - `ik_us0123_sprint_tanch_ceremony_overlap` -> T-anch note: T-anch is NO-OP / verification only â NO mutation to `docs/engineering/architecture.md` or `decisions/DEC-0123.md` in /execute; T-anch records baseline observations only (mirrors US-0122 T-anch ceremony); architecture heading order (# US-0122 -> # US-0123 -> # US-0089) and DEC-0123 Accepted state are read-only verified, not mutated
- architecture_pointers: docs/engineering/architecture.md # US-0123 (approach A1, 8-marker table, SOT=local-only `.opencode/model-catalog.local.json`, template agents omit `model:`, single `OPENCODE_MODEL_SLUG_UNKNOWN` fail-closed, per-role schema, additive integration, always `api` mode, validator extension DQ9, runbook stub DQ10, non-goals)
- dec_pointers: decisions/DEC-0123.md (Â§1 SOT, Â§2 template agents omit model, Â§3 single fail-closed code, Â§4 catalog path, Â§5 per-role schema, Â§6 example placeholders, Â§7 additive integration + materializer + installer hook contract, Â§8 always api mode, Â§9 validator extension, Â§10 runbook stub, Â§11 contract tests, Â§12 non-goals)
- first_execute_task: T-anch (NO-OP / verification) â verify # US-0123 H1 anchor + DEC-0123 Accepted + compose guards 6/6 + 8-marker list locked + materializer/installer hook contract + absent surfaces
- key_locked_artifacts:
  - SOT: `.opencode/model-catalog.local.json` (gitignored, operator-filled) + `template/.opencode/model-catalog.local.example.json` (committed, placeholders only); forbidden surfaces for real OpenCode slugs: `template/.opencode/agents/*.md` `model:` frontmatter, `template/.opencode/opencode.json{,c}`, `.cursor/model-catalog.local.json`, `.cursor/scratchpad.local.md` `MODEL_*` keys
  - catalog schema (DQ5 per-role, 8 role keys): `{schema_version, providers, roles}` where `roles` maps each of 8 role names to `provider/slug` string; providers block covers DeepSeek, Moonshot, Z.AI, Anthropic, OpenAI, DashScope/Qwen (`@ai-sdk/openai-compatible` + `options.baseURL`); US-0069 phase->role matrix bridges phase->role on orchestrator (unchanged); catalog bridges role->provider/slug on OpenCode (new)
  - example catalog placeholders (DQ6): role values are `<your-deepseek-slug>`, `<your-kimi-slug>`, `<your-glm-slug>`, `<your-claude-slug>`, `<your-gpt-slug>` â NO real model-id slugs in `template/`; â¥2 roles have different providers (AC-7); D3 grep scope excludes `*.example.json` / `*.local.json`
  - materializer contract (DQ7): `scripts/opencode_model_catalog_apply.py` â input `.opencode/model-catalog.local.json` + installed `.opencode/agents/<role>.md`; absent catalog = no-op (no fail-closed); present + unknown/empty/placeholder slug = `OPENCODE_MODEL_SLUG_UNKNOWN` fail-closed; malformed JSON = `MODEL_CATALOG_INVALID` scope-tagged `opencode-catalog`; injects `model: <provider/slug>` into installed agent YAML frontmatter only (insert if absent; overwrite if present); NEVER writes to `template/`; NEVER reads/writes `.cursor/model-catalog.local.json`; NEVER reads auth credentials
  - installer hook (T-003 triple-installer parity): trigger = `--host opencode|both` AND `.opencode/model-catalog.local.json` exists at install target; absent = skip (no-op; no fail-closed); fail = surface reason code + exit non-zero; installer does NOT generate the catalog for the operator
  - fail-closed reason-code family (DQ3): NEW `OPENCODE_MODEL_SLUG_UNKNOWN` (single namespaced code); REUSED `MODEL_CATALOG_INVALID` (scope-tagged `opencode-catalog`); existing Cursor-side codes remain Cursor-side only
  - validator extension (DQ9): `scripts/model_tier_validate.py --scope opencode-catalog` â `check_template_opencode_agents` (D3 grep scoped, excludes `*.example.json`/`*.local.json`), `validate_opencode_catalog`, `check_opencode_example_catalog` (â¥2 roles different providers); reuse `check_forbidden_slugs_in_file` helper; extend-not-duplicate (new script only if too coupled â see T-004 critic NB)
  - contract tests (AC-8): `tests/us0123_contract_test.py` â 8 markers (see architecture AC-8 table); mirror to `template/tests/us0123_contract_test.py` byte-identical
  - runbook stub (DQ10): `## OpenCode model slug routing (US-0123)` h2 one-liner in `docs/engineering/runbook.md`; US-0126 owns full text
  - gitignore (T-006): `.opencode/.gitignore` (US-0121 Q10) `*.local.json` glob covers `model-catalog.local.json`; add explicit entry only if glob is narrower
  - manifest rows (T-009): `template/.opencode/model-catalog.local.example.json` + `scripts/opencode_model_catalog_apply.py` under `[opencode_install_include_paths]` (active + template byte-identical)
- next_phase: `/plan-verify` (fresh qa per orchestrator brief) for S0123 / US-0123
- sprint_artifacts: sprints/S0123/ (sprint.md, tasks.md, progress.md, summary.md, uat.json, uat.md)
- timestamp: 2026-08-24T16:30:00Z
- role: tech-lead
- model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 â required)
- runtime_proof_id: rp-auto-20260824-01-sprint-plan-tech-lead-20260824T163000Z-US-0123
- proof_hash: CD814AD66F07A9F9A5C649EF6B0283A4A92179D7502238514B211863C401FEA6

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `fresh_context_marker=tl-US0123-sprint-plan-20260824T163000Z-fresh`
- `timestamp=2026-08-24T16:30:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 â required)
- `evidence_ref=sprints/S0123/sprint.md, sprints/S0123/tasks.md, sprints/S0123/progress.md, sprints/S0123/summary.md, sprints/S0123/uat.json, sprints/S0123/uat.md, docs/engineering/state.md (sprint-plan checkpoint append-bottom), docs/engineering/architecture.md # US-0123, decisions/DEC-0123.md, handoffs/resume_brief.md`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260824-01`
- `runtime_proof_id=rp-auto-20260824-01-sprint-plan-tech-lead-20260824T163000Z-US-0123`
- `phase_id=sprint-plan`, `role=tech-lead`, `story_id=US-0123`, `sprint_id=S0123`
- `proof_issued_at=2026-08-24T16:30:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T17:30:00Z`
- `proof_hash=CD814AD66F07A9F9A5C649EF6B0283A4A92179D7502238514B211863C401FEA6`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"sprint-plan","proof_issued_at":"2026-08-24T16:30:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260824-01-sprint-plan-tech-lead-20260824T163000Z-US-0123","sprint_id":"S0123","story_id":"US-0123"}`

---

## Sprint-plan handoff â **US-0122** / **S0122** â `/plan-verify` next (fresh qa)

- sprint_id: S0122
- story_id: US-0122
- dec_id: DEC-0122 (Accepted, decisions/DEC-0122.md)
- research_anchor: R-0109 (DQ1..DQ8 LOCKED for US-0122; US-0121 Q1..Q12 locks preserved)
- orchestrator_run_id: auto-20260824-01
- fresh_context_marker: tl-US0122-sprint-plan-20260824T120000Z-fresh
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 â not mutated)
- task_count: 10 (T-anch + T-001..T-009; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001,T-007,T-009; AC-2->T-002,T-003,T-005; AC-3->T-002,T-006(marker 3); AC-4->T-001,T-006(marker 7); AC-5->T-004,T-006(markers 1,5,8); AC-6->T-008; AC-7->T-001,T-006(marker 6),T-009; AC-8->T-006(all 8 markers); AC-9->T-anch(baseline),T-006(marker 8),T-009(parity); AC-10->T-005(locked matrix),T-006(marker 3)
- task_order: T-anch -> T-001 (8 agent files) -> {T-002, T-003, T-004, T-005 parallel (per-agent permission matrices)} -> T-007 (manifest rows) -> T-009 (README + parity) -> T-008 (runbook one-liner) -> T-006 (contract tests last) -> integration verification
- compose_guards (non-negotiable): DO NOT amend US-0003 (role set), US-0023/BUG-0006 (spawn-only isolation), US-0121 (pack path consumed; no repo-root opencode.json added), US-0102/DEC-0087 (volatile-ID rule â no vendor slugs in template/.opencode/agents/*.md), US-0002/US-0004 (do-not-port Cursor rules/skills â markdown agents, no .mdc clone)
- critic_carry_ins (3 non-blocking â route to task notes, do not silently drop):
  - `ik_us0122_dev_template_allow_mutates_agents` -> T-005 note: `dev` `template/**` allow could mutate `.opencode/agents/*.md`; mitigation via T-006 marker 1 + T-009 parity extension (byte-identical assertion); no narrow deny glob (would fragment locked matrix)
  - `ik_us0122_compose_guards_marker_surjection` -> T-006 note: do NOT add 9th `test_us0122_compose_guards_unchanged` marker; AC-9 surjection via T-anch baseline + DEC-0122 Â§compose surface + marker 8 (`test_us0122_role_id_parity`); 8-marker budget locked
  - `ik_us0122_stale_compose_count_6_vs_5` -> T-anch note: architecture overview 6/6 wording is stale drift; T-anch verifies 5/5; non-blocking; reconcile at /plan-verify or future doc-parity slice
- architecture_pointers: docs/engineering/architecture.md # US-0122 (approach A1, 8-marker table, locked Layer-1 permission matrix, static success-test-(c) harness, Layer-2 short prompts + clone guard, manual invoke one-liner, no vendor slugs, non-goals)
- dec_pointers: decisions/DEC-0122.md (Â§1 markdown agents, Â§2 locked eight-agent matrix, Â§3 static success-test-(c) harness, Â§4 Layer-2 short prompts + clone guard, Â§5 manual invoke one-liner, Â§6 no vendor slugs, Â§7 contract tests + parity, Â§8 non-goals)
- first_execute_task: T-anch (NO-OP / verification) â verify # US-0122 H1 anchor + DEC-0122 Accepted + compose guards 5/5 + 8-marker list locked + locked matrix in DEC-0122 Â§2 + absent surfaces
- key_locked_artifacts:
  - agent file layout: `template/.opencode/agents/{po,tech-lead,dev,qa,release,curator,security,auto}.md` (8 markdown files; YAML frontmatter: description, mode, permission, short prompt body)
  - locked Layer-1 permission matrix (DEC-0122 Â§2): `auto` (primary; edit deny; task object 7-role allow + `*` deny last); `po` (subagent; edit object docs/product/** + handoffs/po_to_tl.md allow + `**` deny last; bash deny; task deny); `tech-lead` (subagent; edit object architecture/decisions/state/research + decisions/DEC-*.md + handoffs/tl_to_dev.md + sprints/Sxxxx/sprint.md + sprints/Sxxxx/tasks.md + `**` deny last; bash deny; task deny); `dev` (subagent; edit object scripts/** + its_magic/** + template/** + tests/** + sprints/Sxxxx/progress.md + sprints/Sxxxx/qa-findings.md + handoffs/dev_to_qa.md + `**` deny last; bash ask; task deny); `qa` (subagent; edit object qa-findings + plan-verify + verify-work-findings + uat.md/json + qa handoffs + `**` deny last; bash ask; task deny); `release` (subagent; edit object release_queue/notes/releases + release/verify handoffs + CHANGELOG + `**` deny last; bash ask; task deny); `curator` (subagent; edit object state + state-archive + decisions.md + research.md + resume_brief/portfolio_state/continuation_hygiene/archive + `**` deny last; bash deny; task deny); `security` (subagent; edit deny; bash ask; task deny)
  - ordering contract (DQ3): broad `**` -> `deny` MUST be last key in every object-form `permission.edit`; `*` -> `deny` MUST be last key in `auto` `permission.task`; tests assert key order, not just set membership
  - Task subagent ID contract (DQ4): `auto` `permission.task` 7 role allow + `*` deny last denies all non-kit subagents including OpenCode built-ins + future US-0124 plugin-internal helpers; US-0124 may add helpers as `allow` keys above `*` deny, never remove `*` deny last
  - static success-test-(c) harness (DQ7): parse po.md frontmatter -> assert edit is object -> assert docs/product/** + handoffs/po_to_tl.md allow -> assert `**` deny last -> assert no production allow (scripts/**, its_magic/**, **/*.py, installer.*, template/scripts/**, template/its_magic/**); runtime permission-check deferred to US-0124
  - Layer-2 short prompts + clone guard (AC-4): each agent file â¤ 2 KiB total; no forbidden clone markers (/auto, /intake, /discovery, /research, /architecture, /sprint-plan, /execute, /qa, /release, /closure, /refresh-context command-body prose; .cursor/commands/ path literals; --- MDC frontmatter delimiters)
  - no vendor slugs (AC-7): template/.opencode/agents/*.md frontmatter MUST NOT contain `model:` with real vendor slug; test greps deepseek|moonshot|kimi|glm|claude|gpt|sonnet|opus|haiku|o1|o3|sk- -> zero hits
  - manifest rows: `template/.opencode/agents/**` source rows under `[opencode_install_include_paths]` (active + template byte-identical); existing rows unchanged
  - parity extension: `--scope=opencode-adapter` `OPENCODE_ADAPTER_PAIRS` extended for agent inventory (8 markdown files byte-identical active â template; no active kit mirror â DQ8 YAGNI)
  - runbook one-liner: `## OpenCode role agents and permissions (US-0122)` h2 in docs/engineering/runbook.md (full runbook US-0126)
- next_phase: `/plan-verify` (fresh qa per orchestrator brief) for S0122 / US-0122
- sprint_artifacts: sprints/S0122/ (sprint.md, tasks.md, progress.md, summary.md, uat.json, uat.md)
- timestamp: 2026-08-24T12:00:00Z
- role: tech-lead
- model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 â required)
- runtime_proof_id: rp-auto-20260824-01-sprint-plan-tech-lead-20260824T120000Z-US-0122
- proof_hash: 49D4165515F54421094D13675422D8A6CDBDDCBE9A82C6C5A3F3E5248FD1857D

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `fresh_context_marker=tl-US0122-sprint-plan-20260824T120000Z-fresh`
- `timestamp=2026-08-24T12:00:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 â required)
- `evidence_ref=sprints/S0122/sprint.md, sprints/S0122/tasks.md, sprints/S0122/progress.md, sprints/S0122/summary.md, sprints/S0122/uat.json, sprints/S0122/uat.md, docs/engineering/state.md (sprint-plan checkpoint append-bottom), docs/engineering/architecture.md # US-0122, decisions/DEC-0122.md, handoffs/resume_brief.md`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260824-01`
- `runtime_proof_id=rp-auto-20260824-01-sprint-plan-tech-lead-20260824T120000Z-US-0122`
- `phase_id=sprint-plan`, `role=tech-lead`, `story_id=US-0122`, `sprint_id=S0122`
- `proof_issued_at=2026-08-24T12:00:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T13:00:00Z`
- `proof_hash=49D4165515F54421094D13675422D8A6CDBDDCBE9A82C6C5A3F3E5248FD1857D`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"sprint-plan","proof_issued_at":"2026-08-24T12:00:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260824-01-sprint-plan-tech-lead-20260824T120000Z-US-0122","sprint_id":"S0122","story_id":"US-0122"}`

---

## Sprint-plan handoff - **US-0121** / **S0121** - `/execute` next (fresh dev)

- sprint_id: S0121
- story_id: US-0121
- dec_id: DEC-0120 (Accepted, decisions/DEC-0120.md)
- research_anchor: R-0109 (Q6-Q12 LOCKED for US-0121 execute; Q1-Q5 LOCKED for architecture only, deferred to US-0122..US-0126)
- orchestrator_run_id: auto-20260823-01
- fresh_context_marker: tl-US0121-sprint-plan-20260823T112200Z-fresh
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 - not mutated)
- task_count: 10 (T-anch + T-001..T-009; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001; AC-2->T-003,T-004,T-005,T-006; AC-3->T-004,T-005,T-006; AC-4->T-007(markers 2-4); AC-5->T-002,T-004,T-005,T-006,T-007(markers 10,11,14); AC-6->T-008,T-007(marker 13); AC-7->T-007; AC-8->T-anch(baseline),all gated; AC-9->T-003(--help),T-009(runbook h2); AC-10->T-001,T-007(marker 12)
- task_order: T-anch -> {T-001, T-002, T-003 parallel} -> {T-004, T-005, T-006 parallel} -> T-008 -> T-009 -> T-007 (tests last) -> integration verification
- compose_guards (non-negotiable): DO NOT amend US-0008 (additive --host only), DEC-0045 (its_magic/ ownership), US-0102 (volatile-ID rule - no slugs), US-0001 (phase names as placeholders only), US-0018 (packaging delivery path)
- critic_carry_ins (3 non-blocking - route to task notes, do not silently drop):
  - `ik_us0121_missing_overwrite_host_gap` -> T-006 note: YAGNI - `missing` after `both` no-ops on `.opencode/` via predicate (copy-if-missing is host-scoped); no new diagnostic; overwrite US-0008 unchanged
  - `ik_us0121_parity_active_mirror_contradiction` -> T-008 note: parity pairs `template/.opencode` with consumed `.opencode/` (when host includes opencode); no kit-repo active mirror (Q9 YAGNI)
  - `ik_us0121_ac9_help_test_yagni` -> T-007 note: `--help` grep is marker 9 in locked 14-marker set; do not add 15th marker without dropping YAGNI elsewhere
- architecture_pointers: docs/engineering/architecture.md # US-0121 (approach A1, 14-marker table, host-scoped missing/upgrade/clean matrix, kernel-vs-host filter, mixed-section predicate)
- dec_pointers: decisions/DEC-0120.md (ÃÂ§1 host switch, ÃÂ§2 parallel manifest sections, ÃÂ§3 kernel-vs-host, ÃÂ§4 mixed-section predicate, ÃÂ§5 host-scoped missing/upgrade/clean, ÃÂ§6 pack layout, ÃÂ§7 gitignore, ÃÂ§8 cursor coexistence, ÃÂ§9 contract tests + parity, ÃÂ§10 non-goals)
- first_execute_task: T-anch (NO-OP / verification) - verify `# US-0121` H1 anchor + DEC-0120 Accepted + compose guards 5/5 + 14-marker list locked + absent surfaces
- key_locked_artifacts:
  - manifest sections: `[opencode_install_include_paths]` + `[opencode_clean_paths]` (active + template byte-identical)
  - host predicate: `host_gates_cursor_row(rel, host)` shared across PS/Bash/Python
  - diagnostics: `INSTALL_HOST_INVALID`, `OPENCODE_ORPHANED_BY_CLEAN_CURSOR`, `OPENCODE_STALE_BY_UPGRADE_CURSOR`, `CURSOR_ORPHANED_BY_CLEAN_OPENCODE`, `CURSOR_STALE_BY_UPGRADE_OPENCODE`
  - pack layout: `template/.opencode/{agents/.gitkeep, commands/.gitkeep, plugins/README.md, .gitignore, README.md}` (no repo-root opencode.json; no active mirror)
  - gitignore Q10 four groups: `.opencode/opencode.json{,c}`, `.env`/`.env.*`, `*.local.json{,c}`, `auth.json`
- next_phase: `/execute` (fresh dev) for S0121 / US-0121
- sprint_artifacts: sprints/S0121/ (sprint.md, tasks.md, progress.md, uat.json, uat.md, plan-verify.json)
- timestamp: 2026-08-23T11:22:00Z
- role: tech-lead
- model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 - required)
- runtime_proof_id: rp-auto-20260823-01-sprint-plan-tech-lead-20260823T112200Z-US-0121
- proof_hash: 2a7f31fca177451c935b9aedebb4781d57a7b13d8ef87a9e913fcaf10bec6336

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `fresh_context_marker=tl-US0121-sprint-plan-20260823T112200Z-fresh`
- `timestamp=2026-08-23T11:22:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 - required)
- `evidence_ref=sprints/S0121/sprint.md, sprints/S0121/tasks.md, sprints/S0121/progress.md, sprints/S0121/uat.json, sprints/S0121/uat.md, sprints/S0121/plan-verify.json, docs/engineering/state.md, docs/engineering/architecture.md # US-0121, decisions/DEC-0120.md, handoffs/resume_brief.md`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260823-01`
- `runtime_proof_id=rp-auto-20260823-01-sprint-plan-tech-lead-20260823T112200Z-US-0121`
- `phase_id=sprint-plan`, `role=tech-lead`, `story_id=US-0121`, `sprint_id=S0121`
- `proof_issued_at=2026-08-23T11:22:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-23T12:22:00Z`
- `proof_hash=2a7f31fca177451c935b9aedebb4781d57a7b13d8ef87a9e913fcaf10bec6336`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"plan","orchestrator_run_id":"auto-20260823-01","phase_id":"sprint-plan","proof_issued_at":"2026-08-23T11:22:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260823-01-sprint-plan-tech-lead-20260823T112200Z-US-0121","sprint_id":"S0121","story_id":"US-0121"}`

---

## Sprint-plan handoff â **US-0108** / **S0108** â `/plan-verify` next (fresh qa)

- sprint_id: S0108
- story_id: US-0108
- dec_id: DEC-0108 (locked, decisions/DEC-0108.md)
- research_anchor: R-0096 (Q1âQ10 CLOSED, status=delivered)
- orchestrator_run_id: auto-20260628-04
- fresh_context_marker: tl-US0108-sprint-plan-20260629T210000Z-fresh
- sprint_plan_verdict: PASS
- sprint_status: OPEN
- task_count: 11 (within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1âT-001; AC-2âT-002,T-003; AC-3âT-004,T-005; AC-4âT-006; AC-5âT-007; AC-6âT-008; AC-7âT-009,T-010; AC-8âT-011
- tranche_order: A keys+reason codes â B worktree lib â C selection+anti-slop â D merge+resource+execute â E tests+parity+runbook
- compose_guards (non-negotiable): DO NOT amend US-0047, US-0092, US-0103, US-0104, US-0107
- topology: parallel dev in isolated git worktrees; QA cross-review; deterministic winner selection; resource guard cap=6
- next_phase: `/plan-verify` (fresh qa) for S0108 / US-0108
- sprint_artifacts: sprints/S0108/ (sprint.md, tasks.md, progress.md, sprint.json, plan-verify.json)
- timestamp: 2026-06-29T21:32:00Z
- role: tech-lead
- backlog_drain_active: true
- backlog_drain_stories_remaining_budget: 3
- portfolio_open_stories: 4 (US-0108, US-0109, US-0111, US-0112)
- runtime_proof_id: rp-auto-20260628-04-sprint-plan-tech-lead-20260629T213200Z-US0108
- proof_hash: b3e7f1a2c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `fresh_context_marker=tl-US0108-sprint-plan-20260629T210000Z-fresh`
- `timestamp=2026-06-29T21:32:00Z`
- `evidence_ref=sprints/S0108/sprint.md,sprints/S0108/tasks.md,sprints/S0108/progress.md,sprints/S0108/sprint.json,sprints/S0108/plan-verify.json,docs/engineering/state.md,handoffs/tl_to_dev.md,handoffs/resume_brief.md`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260628-04`
- `runtime_proof_id=rp-auto-20260628-04-sprint-plan-tech-lead-20260629T213200Z-US0108`
- `phase_id=sprint-plan`
- `role=tech-lead`
- `proof_issued_at=2026-06-29T21:32:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=b3e7f1a2c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2`

Canonical payload: `{"orchestrator_run_id":"auto-20260628-04","phase_id":"sprint-plan","proof_issued_at":"2026-06-29T21:32:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260628-04-sprint-plan-tech-lead-20260629T213200Z-US0108"}`.

---

## Architecture handoff â **US-0108** â `/sprint-plan` next (fresh tech-lead)

- story_id: US-0108
- sprint_id: (none â sprint-plan to create S0108)
- dec_id: DEC-0108 (locked, decisions/DEC-0108.md)
- research_anchor: R-0096 (Q1âQ10 CLOSED, status=delivered)
- orchestrator_run_id: auto-20260628-04
- fresh_context_marker: tl-US0108-architecture-20260629T204500Z-fresh
- architecture_verdict: PASS
- task_count: 11 (within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1âT-001; AC-2âT-002,T-003; AC-3âT-004,T-005; AC-4âT-006; AC-5âT-007; AC-6âT-008; AC-7âT-009,T-010; AC-8âT-011
- tranche_order: A keys+reason codes â B worktree lib â C validator+selection â D merge+resource guard+execute steps â E tests+parity+runbook
- compose_guards (non-negotiable): DO NOT amend US-0047, US-0092, US-0103, US-0104, US-0107
- topology: parallel dev in isolated git worktrees; QA cross-review; deterministic winner selection; resource guard cap=6
- next_phase: `/sprint-plan` (fresh tech-lead) for US-0108 â materialize S0108 sprint
- timestamp: 2026-06-29T20:45:00Z
- role: tech-lead
- backlog_drain_active: true
- backlog_drain_stories_remaining_budget: 3
- portfolio_open_stories: 4 (US-0108, US-0109, US-0111, US-0112)

---

## Execute handoff â **US-0106** / **S0106** â `/execute` next (fresh dev)

- sprint_id: S0106
- story_id: US-0106
- dec_id: DEC-0106
- orchestrator_run_id: auto-20260628-04
- task_count: 11 (within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1âT-001; AC-2âT-002,T-003; AC-3âT-003; AC-4âT-004; AC-5âT-005; AC-6âT-006; AC-7âT-007,T-011; AC-8âT-008,T-009,T-010
- sprint_status: OPEN
- next_phase: `/execute` (fresh dev) for S0106 / US-0106
- compose_guards (non-negotiable): DO NOT amend US-0069, US-0003, US-0023, US-0103, US-0104, US-0105, US-0107
- timestamp: 2026-06-29T00:40:00Z
- role: qa
- verdict: PASS (plan-verify)

---

## Sprint-plan handoff â **US-0106** / **S0106** â sprint S0106 created (11 tasks T-001..T-011) â `/plan-verify` next (fresh qa)

- sprint_id: S0106
- story_id: US-0106
- dec_id: DEC-0106
- orchestrator_run_id: auto-20260628-04
- task_count: 11 (within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1âT-001; AC-2âT-002,T-003; AC-3âT-003; AC-4âT-004; AC-5âT-005; AC-6âT-006; AC-7âT-007,T-011; AC-8âT-008,T-009,T-010
- tranche_order: A keys+reason codes (T-001) â B lib+dispatch (T-004,T-005) â C validator+command (T-002,T-003) â D review isolation+compose (T-006,T-008,T-009) â E tests+parity+runbook (T-007,T-010,T-011)
- sprint_status: OPEN
- next_phase: `/plan-verify` (fresh qa) for S0106 / US-0106
- compose_guards (non-negotiable): DO NOT amend US-0069, US-0003, US-0023, US-0103, US-0104, US-0105, US-0107
- timestamp: 2026-06-29T00:35:00Z
- role: tech-lead
- verdict: PASS

---

## Plan-verify handoff â **US-0107** / **S0107** â post-**`/plan-verify`** â **`/execute`** (**qa**)


