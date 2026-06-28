## Orchestrated architecture handoff — US-0108 / auto-20260628-04

- `timestamp=2026-06-28T22:00:00Z`
- `phase_id=architecture`
- `role=tech-lead`
- `story_id=US-0108`
- `sprint_id=(none)`
- `orchestrator_run_id=auto-20260628-04`
- `fresh_context_marker=tl-US0108-architecture-20260628T220000Z-fresh`
- `verdict=PASS`
- `next_scheduled_phase=sprint-plan`
- `default_spawn_role=tech-lead`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=3`
- `drain_terminated=false`
- `native_chain_active=true`
- `native_chain_continuing=true`
- `drain_advance_action=spawned`
- `portfolio_open_stories=4` (US-0108, US-0109, US-0111, US-0112)
- `portfolio_open_bugs=0`
- `delivery_mode=standard`
- `token_profile=lean`
- `caveman_mode=1`
- `caveman_level=full`
- `model_tier_default=balanced`
- `AUTO_QUIET=1`

### Summary

- **`/architecture`** **PASS** — **R-0096** Q1–Q10 closed; companion **DEC-0108** ratified. Locked v1 schema for `parallel_dev_pick.json`, worktree naming `.git/worktrees/us0108-<story_id>-<instance_idx>/`, selection predicate (PASS → anti-slop desc → earliest proof_issued_at), merge resolution (`first_pass_wins|last_pass_wins|manual`), resource guard (`AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL=6` lockfile cap). Compose guards confirmed: DO NOT amend US-0047 / US-0092 / US-0103 / US-0104 / US-0107.
- **10 task seeds** (T-001..T-010) within **`SPRINT_MAX_TASKS=12`** threshold; **`SPRINT_AUTO_SPLIT`** not triggered.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Architecture locks (Q1–Q10 closed)

| Q | Lock | Decision |
|---|------|----------|
| Q1 | Worktree naming + isolation | `.git/worktrees/us0108-<story_id>-<instance_idx>/` deterministic; per-worktree `GIT_DIR` + `GIT_WORK_TREE` env; gitignore `.git/worktrees/us0108-*` |
| Q2 | Selection predicate | Filter `qa_verdict=PASS`; highest `anti_slop_score` (default `0`); ties break earliest `proof_issued_at`; single winner deterministic |
| Q3 | QA cross-review mode | Sequential N QA invocations v1 (ordered, deterministic); optional `AUTO_SOVEREIGN_PARALLEL_QA=1` parallel v2 |
| Q4 | `parallel_dev_pick.json` v1 schema | `{story_id, winner_instance_id, worktree_path, qa_verdict, anti_slop_score, proof_issued_at, merge_policy, runner_ts_utc, orchestrator_run_id, loser_instance_ids[]}` write-once |
| Q5 | Merge resolution | `first_pass_wins` (default); `last_pass_wins`; `manual` → `PARALLEL_DEV_PICK_MANUAL_REQUIRED`; conflict bounded retry ≤2 then manual |
| Q6 | Resource guard | `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL` system-wide cap; atomic lockfile `.git/us0108_parallel_dev.lock`; fail-fast `PARALLEL_DEV_RESOURCE_CAP_EXHAUSTED`; release on exit |
| Q7 | Execute step integration | Step 25 (parallel dev); 26 (QA cross-review); 27 (selection); 28 (merge + loser cleanup); after US-0107 step 24 + US-0047 step 22 |
| Q8 | Backward compat | `SOVEREIGN_PARALLEL_DEV=0` = single dev; no worktrees; regression guard `test_us0108_backward_compat_single_dev_unchanged` |
| Q9 | Contract test inventory + parity | 8 `test_us0108_*` markers; parity `--scope=sovereign-parallel-dev` (`SOVEREIGN_PARALLEL_DEV_PAIRS`) |
| Q10 | Compose surfaces (read-only) | US-0104 `anti_slop_score` (read); US-0103 ledger (read); US-0107 deferrals (read); US-0108 writes nothing to upstream schemas |

### AC → Task seed mapping (surjective)

| AC | Task seeds |
|----|------------|
| AC-1 (scratchpad keys) | T-001, T-002 |
| AC-2 (worktree isolation) | T-003 |
| AC-3 (model/lens diversity) | T-004 |
| AC-4 (selection predicate) | T-005 |
| AC-5 (merge policy + pick JSON) | T-006 |
| AC-6 (resource guard) | T-007 |
| AC-7 (execute steps 25-28) | T-008 |
| AC-8 (backward compat + tests + parity) | T-009, T-010 |

### Decision

- Compose guards confirmed: **US-0047/US-0092/US-0103/US-0104/US-0107** — do NOT amend; read-only integration only.
- **DEC-0108** authored — v1 schema + helper lib API + execute step hooks + resource guard + contract tests + runbook + template parity.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Top risks (carry to /sprint-plan)

- **R1** Worktree lock conflicts — deterministic naming + per-worktree GIT_DIR mandatory
- **R2** QA cross-review latency — sequential v1 preferred; parallel opt-in v2
- **R3** Merge conflicts — bounded retry ≤2; then manual halt
- **R4** Anti-slop unavailable — graceful degrade default `0`
- **R5** Resource cap race — atomic lockfile check-and-increment
- **R6** Bulk execute interaction — system-wide cap preferred; compose guard at step 22

### Evidence refs

- `docs/engineering/research.md` (**R-0096** — Q1–Q10 closed)
- `docs/product/backlog.md` (`## US-0108` — L1–L10 discovery locks, architecture PASS appended)
- `decisions/DEC-0108.md` (companion decision)
- `docs/engineering/architecture.md` (`# US-0108` — normative section)
- `docs/engineering/state.md` (architecture checkpoint + phase boundary)
- `handoffs/po_to_tl.md` (this handoff)
- `handoffs/resume_brief.md` (top pointer)
- Shipped compose surfaces: **US-0047** (`auto-orchestration-reference.md`), **US-0092** (`auto-orchestration-reference.md`), **US-0103** (`decision_ledger_lib.py`), **US-0104** (`sovereign_critic_lib.py`), **US-0107** (`sovereign_loop_lib.py`)

### Next

- **`/sprint-plan`** (fresh **tech-lead**) for **US-0108** — materialize **S0108** sprint from 10 task seeds; AC-1..AC-8 bijection check.

### Decision gate

- **None** — architecture satisfied; sprint-plan readiness explicit.

---

## Orchestrated research handoff — US-0106 / auto-20260628-04

- `timestamp=2026-06-28T20:10:00Z`
- `phase_id=research`
- `role=tech-lead`
- `story_id=US-0106`
- `sprint_id=(none)`
- `orchestrator_run_id=auto-20260628-04`
- `fresh_context_marker=tl-US0106-research-20260628T201000Z-fresh`
- `verdict=PASS`
- `next_scheduled_phase=architecture`
- `default_spawn_role=tech-lead`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=4`
- `drain_terminated=false`
- `native_chain_active=true`
- `native_chain_continuing=true`
- `drain_advance_action=spawned`
- `portfolio_open_stories=5` (US-0106, US-0108, US-0109, US-0111, US-0112)
- `portfolio_open_bugs=0`
- `delivery_mode=standard`
- `token_profile=lean`
- `caveman_mode=1`
- `caveman_level=full`
- `model_tier_default=balanced`
- `AUTO_QUIET=1`

### Summary

- **`/research`** **PASS** — **R-0095** Q1–Q7 closed; architecture-ready locks for YAML v1 schema, lib API, review dispatch contract, cross-model policy, escalation rules, contract-test inventory, parity scope.
- Compose guards confirmed: DO NOT amend US-0069 / US-0003 / US-0104 / US-0103 / US-0105 / US-0107.
- Companion **DEC-0106** recommended (manifest artifact surface + review dispatch contracts).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Research locks (Q1–Q7 closed)

| Q | Lock | Decision |
|---|------|----------|
| Q1 | YAML v1 schema + validator CLI | `schema_version: 1`, `roles[]`, `review_obligations[]`, `allowed_self_overrides`, `cross_model_policy`, `escalation_rules`; CLI `--file`, `--repo`, `--self-test`, `--enforce`; success `[SOVEREIGN_ROLE_MANIFEST_VALIDATION_OK]`; fail-closed on unknown `role_id`, cyclic obligations without escalation, secret-shaped literals |
| Q2 | `sovereign_role_manifest_lib.py` API | `load_manifest`, `resolve_role_objective`, `build_objective_injection_block` (char-capped `SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS=512`), `list_obligations_for_phase` (capped `SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE=2`), `dispatch_role_review`, `self_test` |
| Q3 | Cross-role review spawn contract | spawn-only per BUG-0006; JSONL `handoffs/sovereign_role_reviews.jsonl` fields `{obligation_id, reviewer_role, target_role, trigger_phase, orchestrator_run_id, ts, verdict, blocking, findings_ref}`; boundary token `role_review` distinct from US-0069 phase role |
| Q4 | `cross_model_policy` ordering (US-0104 compose) | `default_order` ∈ {`role_review_first`, `critic_first`, `critic_only`, `role_review_only`}; optional per-`obligation_id` override; when `CROSS_MODEL_REVIEW=1` and `SOVEREIGN_ROLE_MANIFEST=1`, orchestrator applies policy — does not merge critic lenses with role review prompts; when either flag `0`, zero overhead |
| Q5 | `escalation_rules` + US-0107 deferral compose | blocking review (`blocking=true`, verdict `fail`) → (1) bounded same-role rework (`SOVEREIGN_ROLE_REVIEW_REWORK_MAX` default `1`), (2) operator `decision_gate`, (3) optional `append_deferral` with `reason_code=ROLE_REVIEW_BLOCKED` when `AUTO_SOVEREIGN=1`; fail-open on deferral errors |
| Q6 | Contract-test inventory + parity | 8 markers `test_us0106_{scratchpad_keys_literals, manifest_schema_v1_literals, objective_injection_char_cap, obligation_dispatch_cap, us0069_compose_no_matrix_change, us0104_compose_no_critic_schema_change, zero_overhead_default, parity_scope}`; parity `--scope=sovereign-role-manifest` (`SOVEREIGN_ROLE_MANIFEST_PAIRS`): `.cursor/scratchpad.md`, `.cursor/sovereign-role-manifest.yaml`, `template/.cursor/scratchpad.md`, `template/.cursor/sovereign-role-manifest.yaml.example`, `scripts/sovereign_role_manifest_validate.py`, `scripts/sovereign_role_manifest_lib.py`, `template/scripts/sovereign_role_manifest_validate.py` |
| Q7 | Companion DEC necessity | **DEC-0106** recommended — locks manifest surface (YAML v1 schema, validator, lib, reviews JSONL, escalation, tests); anchors R-0095 |

### Self-test anchor

**[SOVEREIGN_ROLE_MANIFEST_SELF_TEST_OK]** (research stub; production self-test at `/execute`)

### Top risks (carry to /architecture)

- **R1**: Spawn depth / latency — review obligations multiply subagent spawns per phase; default-off + per-phase cap mandatory.
- **R2**: Role collapse — review spawn mis-routed as producer phase replacement → US-0069 regression; distinct boundary token + compose guard required.
- **R3**: US-0104 interaction — critic + role review at same boundary without `cross_model_policy` causes duplicate findings or rework thrash.
- **R4**: Manifest drift from matrix — operator adds invalid `role_id` or `trigger_phase`; validator must fail-closed with remediation.
- **R5**: Escalation oscillation — blocking review → rework → re-review loops; cap + `decision_gate` required.
- **R6**: Secret leakage — free-text objectives/reviews need scan (mirror US-0103 / US-0105 patterns).

### Evidence refs

- `docs/engineering/research.md` (**R-0095** — research closure, Q1–Q7 closed)
- `docs/product/backlog.md` (`## US-0106` — `discovery_notes` + `research_notes`)
- `docs/engineering/state.md` (discovery + research checkpoints)
- `handoffs/po_to_tl.md` (this handoff)
- `handoffs/resume_brief.md` (top pointer)
- Shipped compose surfaces: **US-0069** (`auto-orchestration-reference.md`), **US-0104** (`sovereign_critic_lib.py`), **US-0107** (`sovereign_loop_lib.py`), **US-0105** (`sovereign_memory_lib.py`)

### Next

- **`/architecture`** (fresh **tech-lead**) for **US-0106** — author `# US-0106` section, companion **DEC-0106**, atomic task seeds, contract-test literals, runbook operator recipes.

### Decision gate

- **None** — research satisfied; architecture readiness explicit.

---

## Orchestrated discovery validation handoff — US-0106 / auto-20260628-04 (validation pass)

- `timestamp=2026-06-28T18:04:00Z`
- `phase_id=discovery`
- `role=po`
- `story_id=US-0106`
- `orchestrator_run_id=auto-20260628-04`
- `fresh_context_marker=po-US0106-discovery-20260628T180400Z-fresh`
- `verdict=PASS`
- `next_scheduled_phase=research`
- `default_spawn_role=tech-lead`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=4`
- `portfolio_open_stories=5` (US-0106, US-0108, US-0109, US-0111, US-0112)
- `portfolio_open_bugs=0`

### Lock validation summary

L1–L12 validated against upstream DONE stories (US-0103, US-0104, US-0105, US-0107, US-0110). All locks **PASS**. Compose guards confirmed: DO NOT amend US-0069 / US-0003 / US-0104 / US-0103 / US-0105 / US-0107. No new discovery risks surfaced (R1–R6 as captured).

### Evidence refs

- `docs/product/backlog.md` (## US-0106 — `discovery_validation` block)
- `docs/engineering/state.md` (discovery isolation evidence + phase boundary + runtime proof)
- `handoffs/resume_brief.md` (top pointer)
- `handoffs/po_to_tl.md` (this handoff)

### Next

- **`/research`** (fresh **tech-lead**) for **US-0106** — close **R-0095** Q1–Q7; YAML schema + lib + dispatch contract + US-0069 compose guards before `/architecture`.

---

## Orchestrated discovery handoff — US-0106 / auto-20260628-04

### Target

- `story_id=US-0106`
- `orchestrator_run_id=auto-20260628-04`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0106-discovery-20260629T002500Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (sovereign-loop batch per intake-sovereign-20260627-01.json)
- `priority=P2`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=4`

### Summary

- **`/discovery`** **PASS** — sovereign role-behavior manifest locked: default-off **`SOVEREIGN_ROLE_MANIFEST`** gate; **`.cursor/sovereign-role-manifest.yaml`** declares per-role **`objective_function`** + directed **`review_obligations`** graph (bootstrap O1–O4: PO→arch user-value, QA→acceptance testability, dev→arch buildability, release→QA deployability); bounded **`role_objective_block`** injection at spawn; post-phase cross-role review dispatch (spawn-only, capped); **`cross_model_policy`** composes **US-0104** without amending critic schema; **`escalation_rules`** may route blocking reviews to **US-0107** deferrals or operator **`decision_gate`**. **Compose do NOT amend** **US-0069** — phase→role matrix + preflight/post checkpoint validation **unchanged**; manifest **`role_id`** ⊆ canonical roles; review spawns are **supplementary hooks** tagged by **`obligation_id`**, not alternate **`phase_id`** roles.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (research inputs)

| Lock | Decision |
|------|----------|
| **Scratchpad keys** | `SOVEREIGN_ROLE_MANIFEST=0\|1` (default `0`); `SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS` default `512`; `SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE` default `2` |
| **Manifest path** | `.cursor/sovereign-role-manifest.yaml` + `template/.cursor/sovereign-role-manifest.yaml.example` |
| **YAML v1 sections** | `roles[]`, `review_obligations[]`, `allowed_self_overrides`, `cross_model_policy`, `escalation_rules` |
| **Default graph** | O1 PO→architecture user-value; O2 QA→PO testability; O3 dev→architecture buildability; O4 release→QA deployability |
| **Objective injection** | Char-capped `role_objective_block` for US-0069-resolved role — additive to US-0105 digest |
| **Review dispatch** | Post-phase spawn-only reviewer subagents → `handoffs/sovereign_role_reviews.jsonl`; per-phase cap |
| **US-0069 compose** | Matrix unchanged; review ≠ phase substitute; compose guard required |
| **US-0104 compose** | `cross_model_policy` ordering vs `/sovereign-critic` — critic schema unchanged |
| **US-0107 compose** | `escalation_rules` → optional `append_deferral` on blocking review cap exhaustion |

### Acceptance pointers (discovery emphasis)

- **AC-1**: Scratchpad keys + zero-overhead when `SOVEREIGN_ROLE_MANIFEST=0`.
- **AC-2**: YAML v1 schema + bootstrap example graph O1–O4.
- **AC-3**: `sovereign_role_manifest_validate.py` CLI + `--self-test`.
- **AC-4**: Objective injection for US-0069-resolved role only.
- **AC-5**: Cross-role review dispatch + reviews JSONL + per-phase cap.
- **AC-6**: `cross_model_policy` vs US-0104 — no critic schema change.
- **AC-7**: Eight `test_us0106_*` markers + `--scope=sovereign-role-manifest` parity.
- **AC-8**: Architecture, runbook, US-0069 / US-0104 compose guards.

### Top risks (carry to /research)

- **R1**: Spawn depth/latency — default-off + per-phase cap mandatory.
- **R2**: Role collapse — review spawn must not substitute producer phase role (US-0069 regression).
- **R3**: US-0104 interaction — critic + role review at same boundary without policy causes thrash.
- **R4**: Manifest/matrix drift — invalid `role_id` or `trigger_phase` must fail-closed.
- **R5**: Escalation oscillation — blocking review rework loops need cap + decision gate.
- **R6**: Secret leakage in objectives/review text — scan required.

### Research asks (new **`R-0095`**)

1. YAML v1 schema + validator CLI.
2. `sovereign_role_manifest_lib.py` API sketch.
3. Cross-role review spawn contract + reviews JSONL + US-0069 boundary token.
4. `cross_model_policy` ordering matrix vs US-0104.
5. `escalation_rules` + US-0107 deferral compose.
6. Contract-test inventory + `SOVEREIGN_ROLE_MANIFEST_PAIRS` parity.
7. Companion DEC necessity.

### Evidence refs

- `docs/product/backlog.md` (`## US-0106` — `discovery_notes` with L1–L12 + design-intent table)
- `docs/product/vision.md` (**Discovery Notes — US-0106**)
- `docs/product/acceptance.md` (`US-0106` row — unchecked, discovery PASS)
- `docs/engineering/research.md` (**`R-0095`** — discovery stub)
- `handoffs/intake_evidence/intake-sovereign-20260627-01.json`
- Shipped compose: **US-0069** (phase→role matrix), **US-0104** (`DEC-0104`, `sovereign_critic_lib.py`), **US-0107** (`DEC-0107`, `sovereign_loop_lib.py`), **US-0105** (`DEC-0105`, `sovereign_memory_lib.py`), **US-0103** (`DEC-0103`)
- Adjacent (do NOT amend): **US-0003** role definitions, **US-0023** fresh-context, **US-0088**/**US-0092**/**US-0095** orchestration stop matrix

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0106`** — close **`R-0095`** Q1–Q7; YAML schema + lib + dispatch contract + US-0069 compose guards before **`/architecture`**.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

## Orchestrated architecture handoff — US-0098 / auto-20260613-01

### Target

- `story_id=US-0098`
- `orchestrator_run_id=auto-20260613-01`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0098-architecture-20260614T080000Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `decomposition=single_story` (per **US-0051**)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=9`

### Summary

- **`/architecture`** **PASS** — **`DEC-0084`** locked; **`# US-0098`** appended; 11 atomic task seeds; eight **`test_us0098_*`** contract markers + **`DEV_ENVIRONMENT_PAIRS`** parity manifest.
- **Default-off gate**: **`DEV_AUTO_LAUNCH_PROFILE`**: `off`|`deterministic_v1` (default **`off`**); optional **`DEV_ENVIRONMENT_CONFIG`** path override.
- **Execute step 24**: after step **23** (**US-0097**); sub-steps **24a–24d**; bounded retries (**`retry_count`≤2**); explicit refresh literal **`refresh dev environment`**.
- **Detection**: four-label matrix; **US-0086** remote precedence over **docker-host-local**; Tier A/B/C execute-triggered relaunch (no mandatory watch daemon v1).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Architecture locks (sprint-plan inputs)

| Lock | Decision |
|------|----------|
| **Binding decision** | **`DEC-0084`** — composes **US-0085** / **US-0064** / **US-0086** / **US-0093** |
| **Tranche order** | A schema+gitignore → B **`dev_environment_lib.py`** → C execute step **24** → D validators + tests |
| **Task seeds** | 11 seeds (under **`SPRINT_MAX_TASKS=12`** threshold) |
| **Profile path** | **`.cursor/dev-environment.json`** + **`template/.cursor/dev-environment.json.example`**; gitignored local |
| **Execute placement** | Step **24** after **23**; zero overhead when profile **`off`** |
| **Contract tests** | **`test_us0098_dev_auto_launch_scratchpad_keys`**, **`test_us0098_execute_step24_literals`**, **`test_us0098_dev_environment_schema_contract`**, **`test_us0098_detection_mode_precedence_literals`**, **`test_us0098_reason_code_inventory`**, **`test_us0098_connect_block_field_literals`**, **`test_us0098_refresh_dev_environment_phrase_literal`**, **`test_us0098_us0086_compose_no_schema_change`** |
| **Parity scope** | **`check_intake_template_parity.py --scope=dev-environment`** (**`DEV_ENVIRONMENT_PAIRS`**) |

### Top risks (carry to /sprint-plan)

- **R1**: Relaunch loops or duplicate containers — bounded retries + idempotent profile writes.
- **R2**: Conflating **docker-host-local** with **US-0086** remote docker — explicit precedence + regression test.
- **R3**: Secret leakage in persisted profile — four-layer **US-0085** audit + gitignore local profile.

### Evidence refs

- `decisions/DEC-0084.md`
- `docs/engineering/architecture.md` (**`# US-0098`**)
- `docs/engineering/research.md` (**`R-0085`**)
- `docs/product/backlog.md` (`## US-0098` — `architecture_notes` appended)
- `docs/engineering/state.md` (Architecture checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/sprint-plan`)
- Prior research proof: `rp-auto-20260613-01-research-tech-lead-20260614T070000Z-US0098`

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`US-0098`** — materialize sprint from 11 architecture seeds; AC-1..AC-10 bijection check.

### Decision gate

- **None** — architecture satisfied; sprint-plan readiness explicit.

---

## Orchestrated discovery handoff — US-0098 / auto-20260613-01

### Target

- `story_id=US-0098`
- `orchestrator_run_id=auto-20260613-01`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0098-discovery-20260614T060000Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (per **US-0051**)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=9`

### Summary

- **`/discovery`** **PASS** — dev-loop **auto-launch profile** locked: default-off **`DEV_AUTO_LAUNCH_PROFILE`** scratchpad gate; persisted **`.cursor/dev-environment.json`** (names-only **` *Env`** refs); **execute-bound** bounded relaunch + explicit **`refresh dev environment`** operator path; **Connect** block after relaunch. **Docker-host-local** is first-class (same-machine shell/docker, not remote SSH). Distinct from **US-0065** (phase QA), **US-0086** (test routing), **US-0067** (release hints).
- **v1 exclusion**: no mandatory unbounded file-watch / **`docker compose watch`** daemon — execute-triggered automation only unless architecture later documents bounded watch.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (research inputs)

| Lock | Decision |
|------|----------|
| **Scratchpad gate** | **`DEV_AUTO_LAUNCH_PROFILE`**: `off` \| `deterministic_v1` (default **`off`**); optional **`DEV_ENVIRONMENT_CONFIG`** path |
| **Profile path** | **`.cursor/dev-environment.json`** + **`template/.cursor/dev-environment.json.example`**; **no** **`release-targets.json`** schema change |
| **Detection matrix** | **`local`**, **`docker-host-local`**, **`docker`**, **`ssh`** — docker-host-local = direct shell/docker on dev machine |
| **Relaunch triggers** | Post-**`/execute`** on runtime/container file classes + explicit refresh phrase; max retry cap architecture-locked |
| **Recipe tiers** | **A** rebuild (Dockerfile*, lockfiles); **B** restart (config); **C** local dev server (**`DEV_SERVER_*`**) |
| **Connect block** | `runtime_mode`, `connect_endpoint`, `health_path`, `service_id`/`container_id`, `target_id`, `env_refs`, `relaunch_outcome` |
| **Reason codes** | **`DEV_ENV_PROFILE_*`**, **`DEV_ENV_RELAUNCH_*`** families (inventory at **`/research`**) |
| **Security** | **US-0085** inheritance — no **`.env`** reads; names-only in git-tracked JSON |
| **Composition** | **US-0086** remote precedence when both profiles on; **US-0093** **`process_health`** may consume relaunch outcome |

### Acceptance pointers (discovery emphasis)

- **AC-1**: **`DEV_AUTO_LAUNCH_PROFILE`** default-off; manual workflows unchanged when off.
- **AC-2**: Profile schema + template example; operator seed + idempotent agent updates.
- **AC-3**: Four-label detection matrix; fail-closed when unresolved.
- **AC-4**: Execute relaunch contract + **`dev_to_qa.md`** evidence tuple.
- **AC-5**: Connect block field shapes per vision discovery template.
- **AC-6**: Compose with **US-0064**/**US-0085**/**US-0086**/**`DEV_SERVER_*`** — no parallel connectivity schema.
- **AC-7**: Explicit **`refresh dev environment`** path documented.
- **AC-8**: Bounded retries; no unbounded watch v1.
- **AC-9..AC-10**: Contract tests, template parity, architecture **`# US-0098`**.

### Top risks (carry to /research)

- **R1**: Relaunch loops or duplicate containers — bounded retries + idempotent profile writes.
- **R2**: Conflating **docker-host-local** with **US-0086** remote docker — explicit matrix + precedence table.
- **R3**: Secret leakage in persisted profile — names-only schema + **US-0085** audit paths.

### Research asks (extend **`R-0085`**)

1. Finalize profile JSON schema and gitignore/local-only policy.
2. File-class → relaunch tier table (exact paths/globs; shared **US-0086** filters where applicable).
3. **`/execute`** step wiring + **`dev_to_qa.md`** evidence tuple prose.
4. Explicit refresh command / NL synonym table.
5. Stdlib helper vs doc-only; **`check_intake_template_parity.py --scope=dev-environment`** manifest.
6. **US-0085** security audit through profile load/relaunch paths.
7. Companion **`DEC-xxxx`** necessity vs discovery locks alone.

### Evidence refs

- `docs/product/vision.md` (**`## Discovery Notes — US-0098`**)
- `docs/product/backlog.md` (`## US-0098` — `discovery_notes`)
- `docs/engineering/research.md` (**`R-0085`**)
- `handoffs/intake_evidence/US-0098-intake-20260613.json`
- `docs/engineering/runtime-connectivity.md`
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/research`)

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0098`** — close **`R-0085`** Q1–Q7; detection matrix + reason-code inventory.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

## Orchestrated architecture handoff — US-0097 / auto-20260613-01

### Target

- `story_id=US-0097`
- `orchestrator_run_id=auto-20260613-01`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0097-architecture-20260613T220000Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `decomposition=single_story` (per **US-0051**)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=10`

### Summary

- **`/architecture`** **PASS** — **`DEC-0083`** locked; **`# US-0097`** appended; 11 atomic task seeds; eight **`test_us0097_*`** contract markers + **`PROJECT_README_PAIRS`** parity manifest.
- **Installer boundary**: root **`README.md`** removed from framework **`[install_paths]`**; **`its_magic/README.md`** canonical framework surface (**DEC-0045** completion).
- **Gate separation**: **US-0091** reframed to **`its_magic/`** paths; new **`validate_project_readme_coverage.py`** + release **3g** + **`PROJECT_README_ENFORCE`** (default **`1`** post-bootstrap).
- **Phase wiring**: execute step **23** (**23a** bootstrap, **23b** delta, **23c** **US-0071** compose); release **3g** after **3f**.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Architecture locks (sprint-plan inputs)

| Lock | Decision |
|------|----------|
| **Binding decision** | **`DEC-0083`** — amends **`DEC-0045`**; reframes **DEC-0074** paths |
| **Tranche order** | A installer+migration → B bootstrap → C phase wiring → D validators + tests |
| **Task seeds** | 11 seeds (under **`SPRINT_MAX_TASKS=12`** threshold) |
| **Placeholder sentinels** | S1 its-magic H1; S2 `<!-- readme-feature-coverage-catalog -->`; S3 US-0091 catalog heading; S4 template byte-match; S5 operator-authored preserve |
| **Migration** | M1–M5 idempotent; hybrid fail-closed **`PROJECT_README_MIGRATION_AMBIGUOUS`** |
| **Kit exception** | **`FRAMEWORK_KIT_REPO=1`** for its-magic dev repo only |
| **Contract tests** | **`test_us0097_installer_manifest_no_root_readme`**, **`test_us0097_execute_step23_literals`**, **`test_us0097_release_step3g_literals`**, **`test_us0097_placeholder_sentinel_table`**, **`test_us0097_framework_validator_paths_reframed`**, **`test_us0097_project_readme_enforce_scratchpad_keys`**, **`test_us0097_project_readme_coverage_validator_contract`**, **`test_us0097_us0091_regression_guard`** |
| **Parity scope** | **`check_intake_template_parity.py --scope=project-readme`** (**`PROJECT_README_PAIRS`**) |

### Top risks (carry to /sprint-plan)

- **R1**: Migration deletes operator project prose — S5 preserve + M5 ambiguous fail-closed.
- **R2**: **US-0091** regression if framework path lock incomplete — explicit path table + regression guard test.
- **R3**: Kit vs consumer repo — **`FRAMEWORK_KIT_REPO`** detection order and validator skip.

### Evidence refs

- `decisions/DEC-0083.md`
- `docs/engineering/architecture.md` (**`# US-0097`**)
- `docs/engineering/research.md` (**`R-0084`**)
- `docs/product/backlog.md` (`## US-0097` — `architecture_notes` appended)
- `docs/engineering/state.md` (Architecture checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/sprint-plan`)
- Prior research proof: `rp-auto-20260613-01-research-tech-lead-20260613T210000Z-US0097`

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`US-0097`** — materialize sprint from 11 architecture seeds; AC-1..AC-10 bijection check.

### Decision gate

- **None** — architecture satisfied; sprint-plan readiness explicit.

---

## Orchestrated discovery handoff — US-0097 / auto-20260613-01

### Target

- `story_id=US-0097`
- `orchestrator_run_id=auto-20260613-01`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0097-discovery-20260613T200000Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (per **US-0051**)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=10`

### Summary

- **`/discovery`** **PASS** — project-owned root **`README.md`** contract locked: bootstrap scaffold on first **`/execute`** when missing/placeholder; mandatory per-shipped-story catalog growth; framework catalog confined to **`its_magic/README.md`** only. Completes **US-0062** / **DEC-0045** partial delivery (manifest still ships root README today).
- **Gate separation**: **US-0091** reframed to framework paths; new project validator + release **3g** + **`PROJECT_README_ENFORCE`** scratchpad (default-on post-bootstrap).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (research inputs)

| Lock | Decision |
|------|----------|
| **Installer boundary** | Remove root **`README.md`** from framework **`[install_paths]`**; ship framework README only under **`its_magic/`** |
| **Project scaffold** | H1 from vision + purpose + **`## For users`** + **`## For developers`** + **`## Features`** + `<!-- project-readme-feature-catalog -->` |
| **Placeholder sentinels** | S1 its-magic H1; S2 `<!-- readme-feature-coverage-catalog -->`; S3 US-0091 catalog heading; S4 template byte-match |
| **Operator prose** | Preserve when S5 (no sentinel + custom content); migration fail-closed on ambiguous hybrid |
| **Kit-repo exception** | **`FRAMEWORK_KIT_REPO=1`** for its-magic dev repo only; consumer repos never bootstrap framework root |
| **Per-story delta** | Execute + release require ≥1 user-facing blurb per shipped **`user_visible: true`** **`US-xxxx`** |
| **Tranche order** | A installer+migration → B bootstrap → C phase wiring → D validators + tests |
| **Reason codes** | Umbrella **`PROJECT_README_COVERAGE_BLOCKED`** + gap/delta/migration sub-codes |

### Acceptance pointers (discovery emphasis)

- **AC-1**: Manifest removes root README from framework install; fresh `missing` install has no framework README at root.
- **AC-2**: Non-destructive migration with S1–S5 heuristic + **`PROJECT_README_MIGRATION_AMBIGUOUS`** remediation.
- **AC-3**: Execute bootstrap when missing/placeholder; vision-sourced title/purpose.
- **AC-4**: Mandatory execute/release README delta; fail-closed when skipped.
- **AC-5**: User + developer H2 structure; framework catalog only in **`its_magic/`**.
- **AC-6**: Split validators — **US-0091** → framework paths; **`validate_project_readme_coverage.py`** → project root.
- **AC-7**: Release **3g** + **`PROJECT_README_ENFORCE`** (default **`1`** post-bootstrap).
- **AC-8..AC-10**: **US-0071** hygiene, contract tests + template parity, architecture + runbook.

### Top risks (carry to /research)

- **R1**: Migration deletes operator project prose — S5 preserve heuristic + ambiguous fail-closed.
- **R2**: **US-0091** regression if framework path lock incomplete — explicit path table in architecture.
- **R3**: Kit vs consumer repo — **`FRAMEWORK_KIT_REPO`** detection order and **US-0091** scope for kit root.

### Research asks (extend **`R-0084`**)

1. Close Q5 — execute/release step numbers and prose tokens; delta skip reason-code table.
2. Close Q6 — `validate_project_readme_coverage.py` CLI/`--report` schema; **3g** wiring with **3f**.
3. Close Q7 — hybrid migration idempotency; merge policy when root is partially customized.
4. Contract-test marker inventory + **`check_intake_template_parity.py --scope=project-readme`** manifest.
5. Confirm whether companion **`DEC-xxxx`** required or discovery locks suffice for architecture.

### Evidence refs

- `docs/product/backlog.md` (`## US-0097` — `discovery_notes` appended)
- `docs/product/vision.md` (**Discovery Notes — US-0097**)
- `docs/product/acceptance.md` (`US-0097` row — unchecked)
- `handoffs/intake_evidence/US-0097-intake-20260613.json`
- `docs/engineering/research.md` (**`R-0084`** — discovery extension appended)
- `docs/engineering/context/installer-owned-paths.manifest` (root **`README.md`** line 42 — removal target)
- Adjacent: **US-0062**, **DEC-0045**, **US-0091**, **DEC-0074**, **US-0032**, **US-0071**, **US-0017**

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0097`** — close **R-0084** Q5–Q7; validator sketch; phase wiring; migration table; architecture readiness.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

## PO intake handoff — US-0098 / cursor-20260613-US0098-intake

### Target

- `story_id=US-0098`
- `intake_run_id=cursor-20260613-US0098-intake`
- `selected_pack=first-intake-pack`
- `priority=P1`
- `decomposition=single_story` (per **US-0051**)
- `next_scheduled_phase=discovery`

### Summary

Operator **`/ask`** → **`/intake`**: during development the AI should **automatically rebuild/restart** the app after code changes (e.g. Docker containers), **persist** a dev-environment profile (operator-seeded), and **show connection parameters** — distinct from **US-0065** phase QA startup, **US-0086** test routing, and **US-0067** release hints. **Docker-host-local** (direct shell/docker on the machine) is a first-class detection label, not remote SSH.

### Scope (10 ACs)

1. Default-off scratchpad **dev auto-launch profile**.
2. Persisted **dev-environment profile** schema (names-only secret refs).
3. Deterministic **environment detection** (`local`, `docker-host-local`, `docker`, `ssh`).
4. **`/execute` bounded relaunch** after runtime/container surface changes.
5. **Operator Connect surface** after relaunch (URL/port/health; no secret values).
6. **Composition** with **US-0064** / **US-0085** / **US-0086** / **`DEV_SERVER_*`**.
7. Explicit **refresh dev environment** operator path.
8. **Bounded safety** + **`DEV_ENV_*`** reason codes (no unbounded watch v1).
9. Contract tests + template parity.
10. Architecture decision + runbook recipe.

### Plan area map (US-0081 / DEC-0064)

| `plan_area_id` | Maps to |
|----------------|---------|
| `dev-profile-schema-persistence` | **US-0098** |
| `environment-detection-heuristics` | **US-0098** |
| `execute-phase-relaunch-contract` | **US-0098** |
| `container-rebuild-orchestration` | **US-0098** |
| `operator-connection-surface` | **US-0098** |
| `scratchpad-gates-default-off` | **US-0098** |
| `composition-existing-runtime-contracts` | **US-0098** |
| `docs-tests-parity` | **US-0098** |

`coverage_complete=true`

### Overlap / duplicate check

- **US-0065** — phase runtime QA; **US-0098** adds dev-loop relaunch during execute.
- **US-0086** — automation test routing; **US-0098** adds profile + relaunch + Connect UX.
- **US-0067** — release Run/Connect/Verify; **US-0098** is in-dev, not release-only.
- **US-0085** — **`.env`** exclusion inherited; no schema change to **US-0064**.

### Intake evidence

- `handoffs/intake_evidence/US-0098-intake-20260613.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**
- `asked_topics`: all eight first-intake keys
- `missing_topics`: (none)
- `assumptions_confirmed`: (none)

### Risks (PO)

- **R1**: Relaunch loops or duplicate containers — mitigate with bounded retries + idempotent profile writes.
- **R2**: Conflating **docker-host-local** with **US-0086** remote docker — explicit detection matrix in architecture.
- **R3**: Secret leakage in persisted profile — names-only schema + **US-0085** audit in architecture.

### Research anchor

- Stub **`R-0085`** — extend in **`/discovery`** / **`/research`** (profile schema, detection matrix, relaunch triggers, compose recipes).

### Status authority

- **OPEN** per **US-0045** until QA/release closure chain.
- **Next**: **`/discovery`** (fresh **PO**) for **`US-0098`**.

---

## PO intake handoff — US-0097 / cursor-20260613-US0097-intake

### Target

- `story_id=US-0097`
- `intake_run_id=cursor-20260613-US0097-intake`
- `selected_pack=first-intake-pack`
- `priority=P1`
- `decomposition=single_story` (per **US-0051**)
- `next_scheduled_phase=discovery`

### Summary

Operator **`/ask`** follow-up: framework README must live only in **`its_magic/`**; root **`README.md`** must be a **project-owned** repo overview (users + developers) that is **bootstrapped on first story** and **extended every sprint/story** — behavior missing today despite **US-0062** intent.

### Scope (10 ACs)

1. Remove root **`README.md`** from framework install payload; **`its_magic/README.md`** only.
2. Non-destructive upgrade migration for legacy framework root README.
3. Execute-time bootstrap scaffold when root README missing/placeholder.
4. Mandatory execute/release README delta per shipped **`US-xxxx`**.
5. User + developer sections in project README (framework catalog stays in **`its_magic/`**).
6. Split validators: **US-0091** → framework; new project README coverage gate.
7. Release gate + scratchpad **`PROJECT_README_ENFORCE`** (default-on post-bootstrap).
8. **US-0071** hygiene on project blurbs.
9. Contract tests + template parity scope.
10. Architecture decision + runbook operator recipe.

### Plan area map (US-0081 / DEC-0064)

| `plan_area_id` | Maps to |
|----------------|---------|
| `installer-framework-readme-boundary` | **US-0097** |
| `project-readme-bootstrap` | **US-0097** |
| `execute-release-delta-workflow` | **US-0097** |
| `project-readme-audience-structure` | **US-0097** |
| `framework-vs-project-readme-gates` | **US-0097** |
| `upgrade-migration-non-destructive` | **US-0097** |
| `docs-tests-parity` | **US-0097** |

`coverage_complete=true`

### Overlap / duplicate check

- **US-0062** — completes partial delivery (manifest still ships root README).
- **US-0091** — reframes scope to framework paths; does not replace.
- **US-0032** — optional guides; orthogonal.
- **US-0077** — framework dual README; project uses simpler product sections.

### Intake evidence

- `handoffs/intake_evidence/US-0097-intake-20260613.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**
- `asked_topics`: all eight first-intake keys
- `missing_topics`: (none)
- `assumptions_confirmed`: (none)

### Risks (PO)

- **R1**: Migration deletes operator project prose — mitigate with placeholder detection + merge policy.
- **R2**: **US-0091** regression if framework paths wrong — explicit path lock in architecture.
- **R3**: Kit repo itself is both framework + product — research must define sentinel/exception for its-magic dev repo vs consumer repos.

### Research anchor

- Stub **`R-0084`** — extend in **`/discovery`** / **`/research`** (placeholder detection, validator sketch, manifest delta, phase wiring).

### Status authority

- **OPEN** per **US-0045** until QA/release closure chain.
- **Next**: **`/discovery`** (fresh **PO**) for **`US-0097`**.

---

## Orchestrated architecture handoff — US-0096 / auto-20260612-01

### Target

- `story_id=US-0096`
- `orchestrator_run_id=auto-20260612-01`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0096-architecture-20260613T040000Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `decomposition=single_story` (per `US-0051`)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=9`

### Summary

- **`/architecture`** **PASS** — **`DEC-0082`** locked; **`# US-0096`** appended; 12 atomic task seeds; eight **`test_us0096_*`** contract markers + **`US0096_PAIRS`** parity manifest.
- **Three-mode axis**: **`DELIVERY_MODE=standard|ultra_lean|mega_quick`** (default **`standard`**) orthogonal to **`TOKEN_PROFILE`** / **`CAVEMAN_MODE`**.
- **Resolver step 0**: **`delivery_mode`** before **DEC-0052**; reinstatement **standard-only**; **`PHASE_POLICY_CONFLICT`** when non-standard + **`AUTO_PHASE_*`**.
- **Tranche A** (always-on): default hot caps **1000/650/3000**, narrow-read all phase commands, delta handoffs, touch-graph runbook — target **≥10%** **`cache_read_tokens`** on matched **`standard`** runs.
- **Layered memory**: hot **`handoffs/active-context.md`** (non-triad); warm **`work/US-xxxx/pack.json`**; cold section-scoped reads (**`LEAN_COLD_READ_MAX_SECTIONS`** default **4**).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Architecture locks (sprint-plan inputs)

| Lock | Decision |
|------|----------|
| **Binding decision** | **`DEC-0082`** — amends **`DEC-0062`** run-class with **`delivery_mode`** |
| **Tranche order** | A universal wins → B **`ultra_lean`** → C **`mega_quick`** → D backlog routing |
| **Task seeds** | 12 seeds (at **`SPRINT_MAX_TASKS=12`** threshold — no auto-split unless hidden scope) |
| **Contract tests** | **`test_us0096_delivery_mode_scratchpad_keys`**, **`test_us0096_standard_mode_baseline_markers_preserved`**, **`test_us0096_mode_scoped_reinstatement_literals`**, **`test_us0096_ultra_lean_macro_phase_literals`**, **`test_us0096_mega_quick_routing_literals`**, **`test_us0096_pack_json_schema_contract`**, **`test_us0096_active_context_contract`**, **`test_us0096_token_profile_orthogonality_paragraph`** |
| **Parity scope** | **`check_intake_template_parity.py --scope=us-0096`** (**`US0096_PAIRS`**) |
| **Native chain** | **DEC-0080** / **DEC-0081** compose unchanged — lean modes reduce spawns, not drain-advance |

### Top risks (carry to /sprint-plan)

- **R1** Partial **`ultra_lean`** without validator/index — Tranche B gated.
- **R3** **`standard`** regression — baseline marker preservation test mandatory early.
- **R5** **`build+verify`** merged spawn — runbook E2E in execute.

### Evidence refs

- `decisions/DEC-0082.md`
- `docs/engineering/architecture.md` (**`# US-0096`**)
- `docs/engineering/research.md` (**`R-0082`**)
- `docs/product/backlog.md` (`## US-0096` — `architecture_notes` appended)
- `docs/engineering/state.md` (Architecture checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/sprint-plan`)
- `handoffs/tl_to_dev.md` (US-0096 architecture handoff)
- Prior research proof: `rp-auto-20260612-01-research-tl-20260613T030000Z-US0096`

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`US-0096`** — materialize sprint from 12 architecture seeds; AC-1..AC-12 bijection check.

### Decision gate

- **None** — architecture satisfied; sprint-plan readiness explicit.

---

## Orchestrated research handoff — US-0096 / auto-20260612-01

### Target

- `story_id=US-0096`
- `orchestrator_run_id=auto-20260612-01`
- phase completed: **`research`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0096-research-20260613T030000Z-fresh`
- `next_scheduled_phase=architecture`
- `decomposition=single_story` (per `US-0051`)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=9`

### Summary

- **`/research`** **PASS** — **`R-0082`** Q1–Q7 closed; architecture-ready locks on **`DELIVERY_MODE`**, layered memory, mode-scoped resolver, Tranche A defaults, and contract-test inventory.
- **Three-mode axis unchanged** from discovery; **DEC-0052 reinstatement applies only when `DELIVERY_MODE=standard`**; **`AUTO_PHASE_*` conflicts with non-standard mode → `PHASE_POLICY_CONFLICT`**.
- **Layered memory**: hot **`handoffs/active-context.md`** (non-triad warm index); warm **`work/US-xxxx/pack.json`** schema v1; cold section-scoped reads capped by **`LEAN_COLD_READ_MAX_SECTIONS`** (default **4**).
- **Tranche A** (always-on): tighter default hot-surface caps, narrow-read in all phase commands, delta handoffs, touch-graph policy — target **≥10%** **`cache_read_tokens`** reduction on matched **`standard`** runs.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Research locks (architecture inputs)

| Lock | Decision |
|------|----------|
| **`pack.json`** | Path **`work/<story_id>/pack.json`**; schema v1 fields (`schema_version`, `story_id`, `delivery_mode`, `status`, `ac[]`, `tasks[]`, `refs[]`, `deltas[]`, `memory_layer`); validator **`scripts/pack_json_validate.py`** |
| **Sprint coexistence** | **`standard`** → **`sprints/Sxxxx/`** authoritative; **`ultra_lean`** → **`work/`** authoritative; **`mega_quick`** → **`sprints/quick/Qxxxx/`**; no destructive overlap; no mid-story mode switch |
| **Resolver step 0** | Resolve **`delivery_mode`** before **DEC-0052**; **`ultra_lean`** → `[spec, plan, build+verify, ship]`; **`mega_quick`** → `[quick]`; **`standard`** → full **DEC-0052** pipeline |
| **`active-context.md`** | Hot index **30–80** lines; cap **`LEAN_STATE_INDEX_ROWS`** (default **80**); rollover on segment close or oversize; **not** triad member (**DEC-0054** unchanged) |
| **`mega_quick` eligibility** | Seven fail-closed codes (**`MEGA_QUICK_*`**); story-only; ≤3 AC; no companion DEC; no existing **`Sxxxx`** |
| **Tranche A defaults** | **`STATE_HOT_MAX_LINES` 1000**, **`PO_TO_TL_HOT_MAX_LINES` 650**, **`ARCH_HOT_MAX_LINES` 3000**; operator explicit values override |
| **`run_class_hash`** | Add required **`delivery_mode`** key (**DEC-0062** extension); cross-mode comparisons invalid |
| **Contract tests** | Eight **`test_us0096_*`** markers; parity **`--scope=us-0096`** (**`US0096_PAIRS`**) |

### Top risks (carry to /architecture)

- **R1** Partial delivery — **`ultra_lean`** without validator/index.
- **R2** **`active-context`** mistaken for triad surface.
- **R3** **`standard`** regression vs **`test_us0095_*`** / **`test_bug0012_*`** baselines.
- **R4** **`mega_quick`** false routing of broad stories.
- **R5** **`build+verify`** merged spawn complexity.

### Evidence refs

- `docs/engineering/research.md` (**`R-0082`** — research extension)
- `docs/product/backlog.md` (`## US-0096` — `research_notes` appended)
- `handoffs/intake_evidence/US-0096-intake-20260611.json`
- `handoffs/po_to_tl.md` (Orchestrated discovery handoff — US-0096)
- `docs/engineering/state.md` (Research checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/architecture`)
- Adjacent: **DEC-0052**, **DEC-0062**, **DEC-0054**, **DEC-0080**, **US-0053**, **US-0080**, **US-0070**, **US-0001**

### Next

- **`/architecture`** (fresh **tech-lead** context) for **`US-0096`** — author **`# US-0096`**, companion **`DEC-xxxx`**, atomic task seeds, **`test_us0096_*`** literals, runbook operator recipes.

### Decision gate

- **None** — research satisfied; architecture readiness explicit.

---

## Orchestrated discovery handoff — US-0096 / auto-20260612-01

### Target

- `story_id=US-0096`
- `orchestrator_run_id=auto-20260612-01`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0096-discovery-20260613T023000Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (per `US-0051`)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=9`

### Summary

- **`/discovery`** **PASS** — opt-in **`DELIVERY_MODE`** lifecycle-shape axis locked: **`standard`** (default, byte-compatible), **`ultra_lean`** (4 macro-phases + layered memory), **`mega_quick`** (enhanced **`/quick`** under **`/auto`**). Orthogonal to **`TOKEN_PROFILE`** (**DEC-0062**) and **`CAVEMAN_MODE`** (**DEC-0072**). Tranche A universal token wins ship always-on without mode toggle.
- **Native chain composes unchanged** (**DEC-0080** / **DEC-0081** / **BUG-0012** delivered) — lean modes reduce spawns per story, not drain-advance semantics.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (research inputs)

| Lock | Decision |
|------|----------|
| **`DELIVERY_MODE` values** | **`standard`** \| **`ultra_lean`** \| **`mega_quick`**; default **`standard`** when unset |
| **Orthogonality** | **`DELIVERY_MODE`** = lifecycle shape + artifacts only; does not substitute **`TOKEN_PROFILE`** or **`CAVEMAN_MODE`** |
| **`ultra_lean` macro-phases** | **`spec`** (PO: intake+discovery) → **`plan`** (TL: research+architecture+sprint-plan) → **`build+verify`** (dev: execute+merged qa/verify-work; **`AUTO_IMPLEMENTATION_LOOP`**) → **`ship`** (release+refresh-context) |
| **Layered memory** | Hot: **`handoffs/active-context.md`**; warm: **`work/US-xxxx/pack.json`**; cold: section-scoped vision/architecture/decisions reads |
| **`mega_quick` routing** | **`/auto`** → enhanced **`/quick`**; **`sprints/quick/Qxxxx/task.json`** + **`summary.md`**; eligibility guard for small bounded work; +1 spawn on test failure only |
| **DEC-0052 reinstatement** | Applies **only** when **`DELIVERY_MODE=standard`** |
| **Tranche order** | A universal wins → B ultra_lean → C mega_quick → D optional backlog **`delivery_mode`** routing |
| **Quality floor** | Tests before stop; no secrets/publish bypass; auditable refs in lean modes (**AC-9**) |

### Acceptance pointers (discovery emphasis)

- **AC-1**: Scratchpad + template docs for **`DELIVERY_MODE`** and optional **`LEAN_*`** keys; non-substitution paragraph.
- **AC-2**: **`standard`** byte-compatible — contract tests vs pre-**US-0096** baseline markers.
- **AC-3**: Tranche A universal wins — measurable **`cache_read_tokens`** improvement on **`run_class_hash`-matched** runs.
- **AC-4..AC-5**: **`ultra_lean`** macro-lifecycle + **`pack.json`** + **`active-context.md`** + section-scoped cold reads.
- **AC-6..AC-7**: **`mega_quick`** routing + mode-scoped phase resolver breadcrumbs.
- **AC-8**: Optional backlog **`delivery_mode`** row + **`AUTO_DELIVERY_ROUTING`** precedence.
- **AC-9..AC-12**: Quality floor, contract tests, architecture lock, token-cost evidence with **`delivery_mode`** in run-class.

### Top risks (carry to /research)

- **R1** Partial delivery — **`ultra_lean`** without memory index.
- **R2** **`active-context.md`** vs **DEC-0054** triad hot-surface rollover conflict.
- **R3** **`standard`** regression via resolver drift.
- **R4** **`mega_quick`** false routing of large cross-cutting stories.
- **R5** **`pack.json`** vs **`sprints/Sxxxx/`** coexistence rules.

### Research asks (extend **`R-0082`**)

1. **`pack.json`** canonical schema + validator sketch vs sprint folder compatibility.
2. Mode-scoped **DEC-0052** reinstatement algorithm (pseudocode + resolver integration point).
3. **`active-context.md`** rollover contract vs **DEC-0054** triad — ownership and line budgets.
4. **`mega_quick`** eligibility table + fail-closed reason codes + backlog row schema.
5. Tranche A default threshold changes vs **`LEAN_*`** operator overrides.
6. **DEC-0062** **`run_class_hash`** extension with **`delivery_mode`** field.
7. Contract-test marker inventory + **`check_intake_template_parity.py --scope=us-0096`** manifest.

### Evidence refs

- `docs/product/backlog.md` (`## US-0096` — `discovery_notes` appended)
- `docs/product/vision.md` (**Discovery Notes — US-0096**)
- `docs/product/acceptance.md` (`US-0096` row — unchecked)
- `handoffs/intake_evidence/US-0096-intake-20260611.json`
- `docs/engineering/research.md` (**`R-0082`** — discovery extension appended)
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/research`)
- Adjacent: **US-0080**, **DEC-0062**, **US-0053**, **US-0070**, **DEC-0052**, **US-0001**, **US-0092**, **US-0095**, **DEC-0080**, **DEC-0081**, **DEC-0072**, **DEC-0054**

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0096`** — deepen **`R-0082`**, lock schemas, resolver algorithm, eligibility table, and contract-test inventory before **`/architecture`**.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

## Orchestrated research handoff — US-0094 / auto-20260607-01
