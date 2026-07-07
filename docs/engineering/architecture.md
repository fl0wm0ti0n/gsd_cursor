
# US-0106 — Sovereign Role-Behavior Manifest (per-role objectives + cross-role review obligations)

## Overview

**US-0106** adds a single YAML manifest (`.cursor/sovereign-role-manifest.yaml`) declaring per-role **`objective_function`**, directed **`review_obligations`** graph (who reviews whose artifacts at which phase boundary), **`allowed_self_overrides`** (closed enum of mutable facets), **`cross_model_policy`** (ordering with US-0104 critic), and **`escalation_rules`** (blocking-review → US-0107 deferral chain). The manifest is an **additive** layer on top of US-0069 spawn machinery. Review spawns are supplementary post-phase hooks — they never substitute for the US-0069 producer role. Default OFF (`SOVEREIGN_ROLE_MANIFEST=0`) — zero overhead when disabled.

**Binding decision**: **DEC-0106**. **Research anchor**: **R-0095** (Q1–Q7 closed). **Compose guards (non-negotiable)**: DO NOT amend US-0069, US-0003, US-0023, US-0103, US-0104, US-0105, US-0107. **Upstream DONE dependencies**: US-0103, US-0104, US-0105, US-0107, US-0110.

**Fresh context marker**: `tl-US0106-architecture-20260629T003000Z-fresh`
**Orchestrator run id**: `auto-20260628-04`
**Timestamp**: 2026-06-29T00:30:00Z
**Verdict**: PASS
**Next**: `/sprint-plan`

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A | **Single YAML manifest** + validator + lib + spawn injection + post-phase review dispatch | **Preferred** — matches DEC-0103 / DEC-0104 / DEC-0105 / DEC-0107 precedent (additive layer on US-0069). |
| B | **Hardcode objectives in scratchpad** (no YAML) | **Rejected** — operator cannot customize role behavior without file edit + validator; scratchpad proliferation. |
| C | **Embed objectives in `.cursor/rules/*.md`** | **Rejected** — rules are per-file guidance; role objectives are per-spawn context injection; distinct lifecycle. |
| D | **Amend US-0069 phase→role matrix** to inject review spawns as new phase_ids | **Rejected** — violates compose guard L10; review spawns are supplementary hooks, not alternate phase completions. |
| E | **Replace US-0104 critic** with role reviews | **Rejected** — distinct purpose (cross-role vs cross-model); `cross_model_policy` declares ordering, not substitution. |

## Normative locks (L1–L12 from research R-0095)

| Lock | Decision |
|------|----------|
| **L1** Scratchpad keys | `SOVEREIGN_ROLE_MANIFEST=0\|1` (default `0`); `SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS` int default `512`; `SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE` int default `2`. When `0`, zero overhead (no manifest reads, no objective injection, no review dispatch). |
| **L2** Manifest path | `.cursor/sovereign-role-manifest.yaml` active + `template/.cursor/sovereign-role-manifest.yaml.example`; example bootstrap ships intake locked default graph O1–O4; operator may fork — validator enforces schema not prose. |
| **L3** YAML v1 schema | Top-level keys: `schema_version` (`1`), `roles[]`, `review_obligations[]`, `allowed_self_overrides`, `cross_model_policy`, `escalation_rules`. `roles[]`: `role_id` ∈ {`po`,`tech-lead`,`dev`,`qa`,`release`,`curator`}, `objective_function` (non-empty, max 1024 chars at file; injection truncated to L1 cap), optional `constraints[]` (immutable strings). `review_obligations[]`: `obligation_id` (unique slug), `reviewer_role`, `target_role`, `trigger_phase` (canonical phase id from US-0069 matrix), `review_focus` (enum v1: `user_value_drift`,`testability`,`buildability`,`deployability`), `artifact_refs[]` (bounded path/glob tokens), optional `blocking` (bool default `false`). |
| **L4** Default obligation graph (bootstrap) | **O1** PO reviews tech-lead `architecture` output for `user_value_drift`; **O2** QA reviews PO `discovery`/`intake` acceptance artifacts for `testability`; **O3** dev reviews tech-lead `architecture` for `buildability`; **O4** release reviews QA `qa` output for `deployability`. |
| **L5** Objective injection | `build_objective_injection_block(scratchpad, resolved_role_id)` → read-only `role_objective_block` appended after phase-context narrow-read, alongside optional US-0105 digest; hard truncate to `SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS`; names-only / no secrets. Does not alter US-0069 expected role for the phase. |
| **L6** Cross-role review dispatch | After producer phase checkpoint passes US-0069 `PHASE_ROLE_*` gates, orchestrator queries obligations where `trigger_phase == completed_phase_id` and `target_role == producer_resolved_role`. For each (cap `SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE`): spawn fresh reviewer subagent with narrow-read of `artifact_refs[]` + producer evidence ref; append result to `handoffs/sovereign_role_reviews.jsonl`. Review spawn uses `reviewer_role` capability preflight (same fail-closed family as US-0069 but distinct boundary token `role_review`). Spawn-only per BUG-0006 — review is not a substitute for producer phase completion. |
| **L7** `allowed_self_overrides` | Closed enum v1: `verbosity`, `detail_level`, `tone` — roles may adjust only listed facets in spawn-local instructions; `constraints[]` and `objective_function` core sentence immutable without manifest edit + validator pass. |
| **L8** `cross_model_policy` (US-0104 compose) | Manifest section: `default_order` ∈ {`role_review_first`,`critic_first`,`critic_only`,`role_review_only`}; optional per-obligation override. When `CROSS_MODEL_REVIEW=1` and `SOVEREIGN_ROLE_MANIFEST=1`, orchestrator applies policy at boundary — does not merge critic lenses with role review prompts. |
| **L9** `escalation_rules` (US-0107 compose) | On `blocking=true` review with verdict `fail`: apply rule chain — (1) bounded same-role rework (`SOVEREIGN_ROLE_REVIEW_REWORK_MAX` default `1`), (2) operator `decision_gate`, (3) optional `append_deferral` with `reason_code=ROLE_REVIEW_BLOCKED` when `AUTO_SOVEREIGN=1` + `blocking_review_action=defer`. Fail-open on deferral errors (log `ROLE_REVIEW_DEFERRAL_FAILED`, do not block). US-0107 `sovereign_deferrals.jsonl` schema unchanged. |
| **L10** Compose US-0069 (non-negotiable) | **Phase→role matrix unchanged**. Preflight resolves producer role exactly as DEC-0051. Review spawns never substitute producer role. Isolation evidence for producer phase still records producer `role` only. Compose regression `test_us0106_us0069_compose_no_matrix_change` required. |
| **L11** Compose US-0103 / US-0105 | Optional ledger tuple cites `role_review_id` from reviews JSONL; memory digest injection order: phase-context → sovereign memory → role objective. No ledger/memory schema changes. |
| **L12** Contract tests + parity | `scripts/sovereign_role_manifest_validate.py` CLI (`--file`, `--repo`, `--self-test`, `--enforce`); eight `test_us0106_*` markers; `check_intake_template_parity.py --scope=sovereign-role-manifest` (`SOVEREIGN_ROLE_MANIFEST_PAIRS`); reason-code family `SOVEREIGN_ROLE_*` + `ROLE_REVIEW_*` in `docs/engineering/reason_codes.md`; architecture `# US-0106`, runbook § Sovereign Role-Behavior Manifest. |

## AC → task surjective map

| AC | Tasks |
|----|-------|
| AC-1 Scratchpad keys + zero-overhead when `0` | T-001 |
| AC-2 YAML v1 schema + default bootstrap graph O1–O4 | T-002, T-003 |
| AC-3 Validator CLI + secret scan + unknown role fail-closed | T-003 |
| AC-4 Objective injection for US-0069-resolved role only | T-004 |
| AC-5 Cross-role review dispatch + reviews JSONL + per-phase cap | T-005 |
| AC-6 `cross_model_policy` ordering vs US-0104 — no critic schema change | T-006 |
| AC-7 Eight `test_us0106_*` markers + parity scope | T-007, T-011 |
| AC-8 Architecture, runbook, US-0069 / US-0104 compose guards | T-008, T-009, T-010 |

## Tranche order (A→E)

| Tranche | Tasks |
|---------|-------|
| **A** Scratchpad keys + reason codes | T-001 |
| **B** Lib + dispatch contract | T-004, T-005 |
| **C** Validator + command | T-002, T-003 |
| **D** Review isolation + compose | T-006, T-008, T-009 |
| **E** Tests + parity + runbook | T-007, T-010, T-011 |

## Task seeds (T-001..T-011)

**T-001** Scratchpad keys (AC-1): append `SOVEREIGN_ROLE_MANIFEST=0`, `SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS=512`, `SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE=2` to `.cursor/scratchpad.md` + template mirror. Zero-overhead when `0`.

**T-002** Bootstrap manifest YAML (AC-2): create `.cursor/sovereign-role-manifest.yaml` + `template/.cursor/sovereign-role-manifest.yaml.example` with `schema_version: 1`, `roles[]` (6 canonical roles with `objective_function`), `review_obligations[]` (O1–O4 default graph from L4), `allowed_self_overrides` (closed enum L7), `cross_model_policy` (L8), `escalation_rules` (L9).

**T-003** Validator + command (AC-3): create `scripts/sovereign_role_manifest_validate.py` (template mirror) with `--file`, `--repo`, `--self-test`, `--enforce`. Success token `[SOVEREIGN_ROLE_MANIFEST_VALIDATION_OK]`. Fail-closed: unknown `role_id`, unknown `trigger_phase`, cyclic obligations without `escalation_rules`, `objective_function` > 1024 chars, secret-shaped literals.

**T-004** Objective injection lib (AC-4): create `scripts/sovereign_role_manifest_lib.py` (template mirror) with `load_manifest(scratchpad)`, `resolve_role_objective(role_id, manifest)`, `build_objective_injection_block(scratchpad, role_id)` (hard truncate to `SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS`). When `SOVEREIGN_ROLE_MANIFEST=0`, short-circuit to no-op. Injection additive to US-0105 digest; does not alter US-0069 expected role.

**T-005** Review dispatch (AC-5): `list_obligations_for_phase(phase_id, target_role, manifest)` + `dispatch_role_review(obligation, producer_evidence, scratchpad)` in `sovereign_role_manifest_lib.py`. Cap `SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE`. Create `handoffs/sovereign_role_reviews.jsonl` (+ template `.gitkeep`). Append row: `{schema_version, obligation_id, reviewer_role, target_role, trigger_phase, orchestrator_run_id, ts, verdict, blocking, findings_ref}`. Spawn-only per BUG-0006 — distinct `role_review` boundary token.

**T-006** `cross_model_policy` (AC-6): implement `resolve_critic_ordering(default_order, obligation_id, overrides)` in `sovereign_role_manifest_lib.py`. When `CROSS_MODEL_REVIEW=1` and `SOVEREIGN_ROLE_MANIFEST=1`, orchestrator applies policy. Does not amend `sovereign_critic_findings.jsonl` schema or US-0104 critic lenses.

**T-007** Contract tests (AC-7): create `tests/us0106_contract_test.py` with 8 markers: `test_us0106_scratchpad_keys_literals`, `test_us0106_manifest_schema_v1_literals`, `test_us0106_objective_injection_char_cap`, `test_us0106_obligation_dispatch_cap`, `test_us0106_us0069_compose_no_matrix_change`, `test_us0106_us0104_compose_no_critic_schema_change`, `test_us0106_zero_overhead_default`, `test_us0106_parity_scope`.

**T-008** Compose guard US-0069 (AC-8): `test_us0106_us0069_compose_no_matrix_change` — verify phase→role matrix unchanged (DEC-0051) when `SOVEREIGN_ROLE_MANIFEST=1`. Review spawns supplementary.

**T-009** Compose guard US-0104 (AC-8): `test_us0106_us0104_compose_no_critic_schema_change` — verify `sovereign_critic_findings.jsonl` schema unchanged when `CROSS_MODEL_REVIEW=1`.

**T-010** Runbook recipe (AC-8): append § "Sovereign Role-Behavior Manifest" to `docs/engineering/runbook.md` — operator recipe for manifest edit, validator invocation, review dispatch troubleshooting.

**T-011** Template parity (AC-7): `check_intake_template_parity.py --scope=sovereign-role-manifest` — 7 pairs (scratchpad + manifest YAML + example manifest + validator + lib + template validator + template lib). Token `[INTAKE_TEMPLATE_PARITY_OK]`.

## Compose guards (non-negotiable)

- **DO NOT amend** US-0069 — phase→role matrix + preflight/post checkpoint validation unchanged (L10).
- **DO NOT amend** US-0003 — canonical role definitions unchanged.
- **DO NOT amend** US-0023 — fresh subagent per phase unchanged (review spawns are supplementary fresh subagents).
- **DO NOT amend** US-0103 — per-run ledger 12-field schema unchanged; optional `role_review_id` citation additive (L11).
- **DO NOT amend** US-0104 — critic lenses + `sovereign_critic_findings.jsonl` schema unchanged; `cross_model_policy` declares ordering, not substitution (L8, T-006, T-009).
- **DO NOT amend** US-0105 — sovereign memory entries/digest JSONL shapes unchanged; injection order additive (L11).
- **DO NOT amend** US-0107 — deferral register + `advance_sovereign_loop` semantics unchanged; `escalation_rules` `append_deferral` call uses existing API with `reason_code=ROLE_REVIEW_BLOCKED` (L9).

## Risks

1. **Spawn depth / latency**: review obligations multiply subagent spawns per phase → mitigated by default-off (`SOVEREIGN_ROLE_MANIFEST=0`) + per-phase cap (`SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE=2`).
2. **Role collapse**: review spawn mis-routed as producer phase replacement → mitigated by distinct `role_review` boundary token + compose guard L10 + regression test T-008.
3. **US-0104 interaction**: critic + role review at same boundary without `cross_model_policy` → mitigated by L8 ordering modes (T-006).
4. **Manifest drift from matrix**: operator adds invalid `role_id` or `trigger_phase` → mitigated by validator fail-closed (T-003).
5. **Escalation oscillation**: blocking review → rework → re-review loops → mitigated by `SOVEREIGN_ROLE_REVIEW_REWORK_MAX=1` + operator `decision_gate` (L9).
6. **Secret leakage**: free-text objectives/reviews → mitigated by validator secret scan (T-003, mirror US-0103 / US-0105 patterns).

## Evidence references

- `docs/product/backlog.md` — `## US-0106` (discovery notes + research notes)
- `docs/engineering/research.md` — `R-0095` (Q1–Q7 closed)
- `decisions/DEC-0106.md` — binding decision (locked)
- `handoffs/po_to_tl.md` — discovery handoff + research handoff
- `docs/engineering/state.md` — discovery checkpoint + research checkpoint + architecture checkpoint (this section)
- Shipped compose surfaces: US-0069 (`auto-orchestration-reference.md` phase→role matrix), US-0104 (`sovereign_critic_lib.py`), US-0107 (`sovereign_loop_lib.py`), US-0105 (`sovereign_memory_lib.py`), US-0103 (decision ledger), US-0110 (convergence)

---

# US-0108 — Parallel Instance Arbitrage for dev phase

## Overview

**US-0108** adds parallel dev subagent spawning in isolated git worktrees for the same execute task. Under `SOVEREIGN_PARALLEL_DEV=1`, execute step 25 spawns N dev instances (default 3); step 26 QA cross-review evaluates all N; step 27 selects winner deterministically (PASS → highest anti-slop → earliest proof); step 28 merges winner to main and cleans up losers. Resource guard caps system-wide parallelism. Compose guards (non-negotiable): DO NOT amend US-0047, US-0092, US-0103, US-0104, US-0107.

**Binding decision**: **DEC-0108**. **Research anchor**: **R-0096** (Q1–Q10 CLOSED; `status=delivered`). **Fresh context marker**: `tl-US0108-architecture-20260629T204500Z-fresh`. **Orchestrator run id**: `auto-20260628-04`. **Timestamp**: 2026-06-29T20:45:00Z. **Verdict**: PASS. **Next**: `/sprint-plan`.

## Normative locks (L1–L10 from research R-0096)

| Lock | Decision |
|------|----------|
| **L1** Scratchpad keys + defaults | `SOVEREIGN_PARALLEL_DEV=0\|1` (default `0` — zero overhead); `AUTO_SOVEREIGN_PARALLEL_N` int ≥1 default `3`; `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL` int ≥1 default `6`; `AUTO_SOVEREIGN_MERGE_RESOLVE` ∈ {`first_pass_wins`,`last_pass_wins`,`manual`} default `first_pass_wins`; `AUTO_SOVEREIGN_WORKTREE_KEEP=0\|1` default `0`; `AUTO_SOVEREIGN_PARALLEL_QA=0\|1` default `0`; optional `AUTO_SOVEREIGN_PARALLEL_MODEL_<idx>`, `AUTO_SOVEREIGN_PARALLEL_LENS_<idx>` per-instance overrides. |
| **L2** Worktree isolation | Deterministic naming `.git/worktrees/us0108-<story_id>-<instance_idx>/`; per-worktree `GIT_DIR` + `GIT_WORK_TREE` env; gitignore `.git/worktrees/us0108-*` in template; no shared lock conflicts. |
| **L3** Model/lens diversity | Instance 0 = baseline; instance 1..N-1 optional `AUTO_SOVEREIGN_PARALLEL_MODEL_<idx>` / `AUTO_SOVEREIGN_PARALLEL_LENS_<idx>` overrides; unset inherits `MODEL_<PHASE>`. |
| **L4** Selection predicate | (1) filter `qa_verdict=PASS`; (2) highest `anti_slop_score` (default `0` when critic absent); (3) tie-break earliest `proof_issued_at`; single winner deterministic. Sequential N QA v1; optional `AUTO_SOVEREIGN_PARALLEL_QA=1` parallel v2. |
| **L5** Merge policy + pick artifact | `AUTO_SOVEREIGN_MERGE_RESOLVE`: `first_pass_wins` (default), `last_pass_wins`, `manual` → halt. Merge artifact `handoffs/parallel_dev_pick.json` v1 schema `{schema_version:1, story_id, winner_instance_id, worktree_path, qa_verdict, anti_slop_score, proof_issued_at, merge_policy, runner_ts_utc, orchestrator_run_id, loser_instance_ids[]}`. Bounded conflict retry ≤2 then manual halt. |
| **L6** Resource guard | `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL` system-wide cap; atomic lockfile `.git/us0108_parallel_dev.lock`; spawn fails fast `PARALLEL_DEV_RESOURCE_CAP_EXHAUSTED`; release on instance exit. |
| **L7** Execute phase integration | Steps 25 (spawn N dev) → 26 (QA cross-review) → 27 (selection) → 28 (merge+cleanup). After US-0107 sovereign-loop step 24; after US-0047 bulk execute step 22. |
| **L8** Backward compat | `SOVEREIGN_PARALLEL_DEV=0` = single dev per US-0047 unchanged; no worktrees; no parallel QA; no pick JSON; no resource guard; US-0047/US-0092 semantics unchanged. Regression guard `test_us0108_backward_compat_single_dev_unchanged`. |
| **L9** Contract tests + parity | Eight `test_us0108_*` markers: scratchpad+defaults, worktree isolation, selection determinism, merge+pick schema, resource cap, execute steps 25-28, backward compat, parity `--scope=sovereign-parallel-dev` (`SOVEREIGN_PARALLEL_DEV_PAIRS`). |
| **L10** Compose (read-only) | US-0108 reads US-0104 anti-slop scores (read-only); US-0103 ledger entries (read-only); US-0107 deferral register (read-only). US-0108 does NOT write to US-0104 critic schema, US-0103 ledger schema, US-0107 deferral schema, US-0047 bulk orchestration. |

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A | **Additive parallel-dev layer on existing execute** — new steps 25-28 after US-0047 step 22; read-only compose with US-0104/US-0103/US-0107 | **Preferred** — zero-overhead default; composes without amending upstream |
| B | **Replace US-0047 dev spawn with parallel-first** | **Rejected** — violates compose guard; breaks all single-dev semantics |
| C | **Shared worktree with concurrent branches** | **Rejected** — git lock conflicts; violates isolation requirement |
| D | **Random winner selection** | **Rejected** — non-deterministic; violates testability |
| E | **Unbounded merge retries** | **Rejected** — risks infinite loops; bounded retry ≤2 mandatory |

## AC → task surjective map

| AC | Tasks |
|----|-------|
| AC-1 Scratchpad keys + zero-overhead when `0` | T-001 |
| AC-2 Worktree isolation (naming, GIT_DIR, cleanup) | T-002, T-003 |
| AC-3 Selection predicate (PASS → anti-slop → earliest) | T-004, T-005 |
| AC-4 Merge policy + `parallel_dev_pick.json` v1 | T-006 |
| AC-5 Resource guard (system-wide cap + lockfile) | T-007 |
| AC-6 Execute steps 25-28 + lib integration | T-008 |
| AC-7 Backward compat (zero change when off) + tests | T-009, T-010 |
| AC-8 Parity `--scope=sovereign-parallel-dev` + runbook | T-011 |

**Surjectivity check**: AC-1..AC-8 all covered. **Total**: 11 task seeds ≤ `SPRINT_MAX_TASKS=12` — `SPRINT_AUTO_SPLIT` not triggered.

## Task seeds (T-001..T-011)

| ID | Title | Tranche |
|----|-------|---------|
| **T-001** | Scratchpad keys (`SOVEREIGN_PARALLEL_DEV`, `AUTO_SOVEREIGN_PARALLEL_N`, `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL`, `AUTO_SOVEREIGN_MERGE_RESOLVE`, `AUTO_SOVEREIGN_WORKTREE_KEEP`, `AUTO_SOVEREIGN_PARALLEL_QA`) + reason code inventory (`PARALLEL_DEV_*`) | A |
| **T-002** | Worktree isolation lib: `parallel_dev_arbiter_lib.py` — `create_worktree(story_id, instance_idx)`, `list_worktrees()`, `remove_worktree()` per L2 naming `.git/worktrees/us0108-<story_id>-<instance_idx>/` | B |
| **T-003** | Worktree cleanup post-merge: winner promote, loser delete per `AUTO_SOVEREIGN_WORKTREE_KEEP`; fail-open `PARALLEL_DEV_WORKTREE_CLEANUP_FAILED` | B |
| **T-004** | Selection predicate: `select_winner(qa_results[])` — filter PASS → sort `-anti_slop_score` → tie-break earliest `proof_issued_at`; default `0` when critic absent | C |
| **T-005** | Anti-slop score reader: read-only extract `anti_slop_score` from sprint `qa-findings.md` or `sovereign_critic_findings.jsonl`; graceful degrade default `0` when US-0104 absent | C |
| **T-006** | Merge policy + `parallel_dev_pick.json` v1 schema: `first_pass_wins|last_pass_wins|manual`; write-once artifact; bounded retry ≤2 | D |
| **T-007** | Resource guard: atomic lockfile `.git/us0108_parallel_dev.lock`; `acquire_parallel_slot()` / `release_parallel_slot()`; fail-fast `PARALLEL_DEV_RESOURCE_CAP_EXHAUSTED` | D |
| **T-008** | Execute steps 25-28: spawn N dev → QA cross-review → selection → merge+cleanup; after US-0047 step 22 + US-0107 step 24 | D |
| **T-009** | Backward compat guard: `SOVEREIGN_PARALLEL_DEV=0` path — zero behavior change; regression test `test_us0108_backward_compat_single_dev_unchanged` | E |
| **T-010** | Eight `test_us0108_*` contract markers in `tests/us0108_contract_test.py` + validator CLI `parallel_dev_arbiter_validate.py` | E |
| **T-011** | Parity `SOVEREIGN_PARALLEL_DEV_PAIRS` in `scripts/check_intake_template_parity.py --scope=sovereign-parallel-dev` + runbook § Parallel Instance Arbitrage | E |

## Tranche order

1. **A** keys + reason codes (T-001)
2. **B** worktree lib (T-002, T-003)
3. **C** validator + selection (T-004, T-005)
4. **D** merge + resource guard + execute steps (T-006, T-007, T-008)
5. **E** tests + parity + runbook (T-009, T-010, T-011)

## Compose guards (non-negotiable)

| Story | Compose rule |
|-------|--------------|
| **US-0047** | Bulk execute step 22 unchanged; US-0108 system-wide cap checked **after** bulk cap evaluation. |
| **US-0092** | Full autonomy outer driver unchanged; parallel dev is execute-phase internal. |
| **US-0103** | Ledger schema unchanged; US-0108 reads `handoffs/sovereign_decisions/*.jsonl` only. |
| **US-0104** | Critic schema unchanged; US-0108 reads `anti_slop_score` from sprint `qa-findings.md` only. |
| **US-0107** | Deferral register schema unchanged; US-0108 may append winner/loser outcome rows as consumer. |

## Risks

| Risk | Mitigation |
|------|------------|
| **R1** Worktree lock conflicts | Deterministic naming + per-worktree GIT_DIR + GIT_WORK_TREE |
| **R2** QA cross-review latency | Sequential v1 default; parallel opt-in v2 |
| **R3** Merge conflicts | Bounded retry ≤2; then `PARALLEL_DEV_MERGE_CONFLICT` halt |
| **R4** Anti-slop unavailable | Graceful degrade default `0` when critic absent |
| **R5** Resource cap race | Atomic lockfile check-and-increment |
| **R6** Bulk execute interaction | System-wide cap preferred; checked after US-0047 step 22 |

## Consequences

- Sprint: S0108 in `sprints/S0108/`
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

---

# US-0109 — Self-Healing Deploy Loop (post-deploy smoke probe + bounded retry + DEPLOY_DEFERRED)

## Overview

**US-0109** adds a post-deploy smoke probe + bounded retry loop on top of the US-0054 publish chain. After `[RELEASE_PUBLISH_OK]`, a two-stage smoke probe (health HTTP GET + acceptance smoke runner) validates the deployed artifact. On probe FAIL, the publish path is re-entered idempotently up to `AUTO_SOVEREIGN_DEPLOY_RETRY_MAX` (default 3). After retry-cap exhaustion, a DEPLOY_DEFERRED tuple is written to the US-0107 deferral register via `append_deferral(work_item_kind=deploy)`. Compose guards (non-negotiable): DO NOT amend US-0054, US-0100, US-0103, US-0107, US-0110.

**Binding decision**: **DEC-0109**. **Research anchor**: **R-0097** (Q1–Q11 CLOSED; `status=delivered`). **Fresh context marker**: `tl-US0109-architecture-20260630T001100Z-fresh`. **Orchestrator run id**: `auto-20260628-04`. **Timestamp**: 2026-06-30T00:11:00Z. **Verdict**: PASS. **Next**: `/sprint-plan`.

## Normative locks (L1–L10 from research R-0097)

| Lock | Decision |
|------|----------|
| **L1** Scratchpad keys + defaults | `AUTO_SOVEREIGN_SELF_HEALING_DEPLOY=0\|1` (default `0` — zero overhead); `AUTO_SOVEREIGN_DEPLOY_RETRY_MAX` int ≥ 1 default `3`; `AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC` int ≥ 1 default `30`; `AUTO_SOVEREIGN_DEPLOY_PROBE_KIND` ∈ {`health_endpoint`, `acceptance_smoke`, `both`} default `both`; `SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH` default `tests/deploy_smoke/`; `AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT` names-only env ref (US-0085 compose). Fail-closed `DEPLOY_HEALING_PROBE_TARGET_MISSING` when health endpoint unresolvable. |
| **L2** Post-deploy smoke probe | Runs after US-0054 publish PASS (`[RELEASE_PUBLISH_OK]`). Two-stage probe: **(a) health HTTP GET** — target URL from names-only scratchpad/env ref (`AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT`), timeout `AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC`, success = HTTP 2xx; **(b) acceptance smoke** — bounded pytest runner at `SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH` (default `tests/deploy_smoke/`) via `pytest -x --timeout=30 -q`. Both stages MUST pass to emit `[DEPLOY_SMOKE_PROBE_OK]`. |
| **L3** Bounded retry loop | On probe FAIL: re-enter US-0054 publish with bounded retry up to `AUTO_SOVEREIGN_DEPLOY_RETRY_MAX`. Retry reuses existing publish path — does NOT amend US-0054 publish targets/semantics. Retry emits `DEPLOY_HEALING_RETRY_ATTEMPT` reason-code log entry per attempt. Idempotent (no duplicated artifacts, no duplicate ledger rows). |
| **L4** DEPLOY_DEFERRED state | After retry cap exhaustion: call US-0107 `append_deferral` with `work_item_kind=deploy`, `reason_code=DEPLOY_DEFERRED`, `work_item_ref=<current_story_id>`, `source_orchestrator_run_id=<runner>`, `remediation_hint=<smoke_summary>` (truncated to 512 chars per US-0107 L2 schema), `blocked_by_phase="release"`, `retry_count=<retry_max>`. Orchestrator continues per `AUTO_SOVEREIGN_DEFERRAL_POLICY` — does NOT halt. |
| **L5** Compose US-0054 (read-only) | US-0054 publish targets / confirmation gate / runbook recipe UNCHANGED. US-0109 re-enters publish PASS point only — does not alter confirmation gate semantics, does not alter publish target schema, does not alter release-notes wiring. Regression guard `test_us0109_us0054_compose_no_publish_semantics_change` required. |
| **L6** Compose US-0100 (read-only) | US-0100 version-scoped changelog / [Unreleased] promotion / GitHub notes UNCHANGED. US-0109 does not trigger changelog writes — only release gate consumes publish PASS. |
| **L7** Compose US-0107 (consumer) | US-0107 deferral register schema UNCHANGED. US-0109 is consumer of `append_deferral(...)` API only — no schema extension, no new `work_item_kind` values beyond `deploy`. Reads `list_open_deferrals` only for converge gating (US-0110 composes). |
| **L8** Compose US-0103 (read-only) | Ledger schema UNCHANGED. US-0109 may cite `deploy_deferral_id` on append basis (optional — v1 additive). |
| **L9** Contract tests + parity | Eight `test_us0109_*` core markers + 2 compose guards (`test_us0109_us0054_compose_no_publish_semantics_change`, `test_us0109_us0100_compose_no_changelog_change`). Validator `scripts/self_healing_deploy_validate.py` CLI with `--self-test`, `--repo`, `--file`, `--enforce`. Success token `[SELF_HEALING_DEPLOY_VALIDATION_OK]`. Parity `--scope=sovereign-self-healing-deploy` (`SOVEREIGN_SELF_HEALING_DEPLOY_PAIRS`, 6 pairs). |
| **L10** Reason code family | Section § US-0109 in `docs/engineering/reason_codes.md` — codes: `DEPLOY_HEALING_DISABLED` (info), `DEPLOY_HEALING_SMOKE_HEALTH_FAIL`, `DEPLOY_HEALING_SMOKE_ACCEPTANCE_FAIL`, `DEPLOY_HEALING_RETRY_ATTEMPT`, `DEPLOY_HEALING_RETRY_CAP_EXHAUSTED`, `DEPLOY_HEALING_DEFERRED`, `DEPLOY_HEALING_PROBE_TARGET_MISSING`, `DEPLOY_HEALING_TIMEOUT`. `DEPLOY_DEFERRED` already reserved in US-0107 runbook — confirmed reuse. |

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A | **Additive post-publish hook** — steps 29-31 after US-0054 publish PASS; re-enter publish path on probe FAIL; DEPLOY_DEFERRED via US-0107 | **Preferred** — zero-overhead default; composes without amending upstream |
| B | **Replace US-0054 publish with retry-first** | **Rejected** — violates compose guard; breaks all single-publish semantics |
| C | **Fresh subagent spawn per retry** | **Rejected** — no fresh boundary token needed; reuse publish subagent/handler |
| D | **Probe-kind bypass (only HTTP ping)** | **Rejected** — violates acceptance coverage requirement |
| E | **Deploy smoke in US-0107** | **Rejected** — US-0107 owns deferral register only; deploy smoke is US-0109 |

## AC → task surjective map

| AC | Tasks |
|----|-------|
| AC-1 Scratchpad keys + zero-overhead when `0` | T-001 |
| AC-2 Post-deploy smoke probe + probe_kind | T-002, T-003 |
| AC-3 Bounded retry loop | T-004 |
| AC-4 DEPLOY_DEFERRED state transition (US-0107 `append_deferral`) | T-005 |
| AC-5 Contract tests + backward compat | T-006, T-007 |
| AC-6 Validator CLI + tokens | T-008 |
| AC-7 Compose regression guards | T-009 |
| AC-8 Parity + runbook + reason codes | T-010 |
| AC-9 Execute steps 29-31 wiring | T-011 |

**Surjectivity check**: AC-1..AC-9 all covered. **Total**: 11 task seeds ≤ `SPRINT_MAX_TASKS=12` — `SPRINT_AUTO_SPLIT` not triggered.

## Task seeds (T-001..T-011)

| ID | Title | Tranche |
|----|-------|---------|
| **T-001** | Scratchpad keys (`AUTO_SOVEREIGN_SELF_HEALING_DEPLOY`, `AUTO_SOVEREIGN_DEPLOY_RETRY_MAX`, `AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC`, `AUTO_SOVEREIGN_DEPLOY_PROBE_KIND`, `SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH`, `AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT`) + reason code inventory (8 codes § US-0109) | A |
| **T-002** | Self-healing deploy lib: `scripts/self_healing_deploy_lib.py` — `run_health_probe(scratchpad)`, `run_acceptance_smoke(scratchpad)`, `run_smoke_probe_chain(scratchpad)` per L2 two-stage chain; names-only URL resolution (US-0085 compose); output schema per §2 | B |
| **T-003** | Probe target resolution: `resolve_health_endpoint_url(scratchpad)` — names-only env ref resolution (`os.environ[ref]`); fail-closed `DEPLOY_HEALING_PROBE_TARGET_MISSING` when absent; secret scan | B |
| **T-004** | Bounded retry loop: `run_deploy_healing_loop(repo, scratchpad, publish_handler)` — re-enter publish on probe FAIL; per-attempt `DEPLOY_HEALING_RETRY_ATTEMPT` reason log; cap at `AUTO_SOVEREIGN_DEPLOY_RETRY_MAX`; idempotency invariant | B |
| **T-005** | DEPLOY_DEFERRED transition: `emit_deploy_deferral(repo, scratchpad, smoke_summary)` calling US-0107 `append_deferral(...)` with `work_item_kind=deploy`, `reason_code=DEPLOY_DEFERRED`, `remediation_hint=<summary>` (truncated to 512) | B |
| **T-006** | Eight `test_us0109_*` core contract markers + 2 compose guards in `tests/us0109_contract_test.py` | C |
| **T-007** | Backward compat guard: `AUTO_SOVEREIGN_SELF_HEALING_DEPLOY=0` byte-identical publish path; regression `test_us0109_backward_compat_off_path_byte_identical` | C |
| **T-008** | Validator CLI: `scripts/self_healing_deploy_validate.py` with `--self-test` (`[SELF_HEALING_DEPLOY_VALIDATION_OK]`), `--repo`, `--file`, `--enforce` | C |
| **T-009** | Compose guard US-0054: `test_us0109_us0054_compose_no_publish_semantics_change` + Compose guard US-0100: `test_us0109_us0100_compose_no_changelog_change` | D |
| **T-010** | Parity `--scope=sovereign-self-healing-deploy` (`SOVEREIGN_SELF_HEALING_DEPLOY_PAIRS`, 6 pairs) in `check_intake_template_parity.py` + runbook § Self-Healing Deploy Loop (operator recipe for probe-failure remediation) | D |
| **T-011** | Execute steps 29-31 wiring: step 29 smoke probe, step 30 retry loop, step 31 DEPLOY_DEFERRED on exhaustion; after US-0108 steps 25-28, before US-0107 step 24 | D |

## Tranche order

1. **A** keys + reason codes (T-001)
2. **B** lib + probe + retry + deferral (T-002, T-003, T-004, T-005)
3. **C** tests + backward compat + validator (T-006, T-007, T-008)
4. **D** compose guards + parity + runbook + execute wiring (T-009, T-010, T-011)

## Compose guards (non-negotiable)

| Story | Compose rule |
|-------|--------------|
| **US-0054** | Publish targets / confirmation gate / release-notes wiring UNCHANGED. US-0109 re-enters publish PASS point only. |
| **US-0100** | Changelog / [Unreleased] / GitHub notes UNCHANGED. US-0109 does not trigger changelog writes. |
| **US-0103** | Ledger schema UNCHANGED. Optional `deploy_deferral_id` citation additive (v1). |
| **US-0107** | Deferral register schema UNCHANGED. US-0109 consumer of `append_deferral(...)` API only. |
| **US-0110** | Convergence predicate UNCHANGED. US-0110 reads open deferrals (no new logic). |

## Risks

| Risk | Mitigation |
|------|------------|
| **R1** Smoke probe source ambiguity (US-0093 UAT vs US-0109 deploy smoke) | `probe_kind` enum separation: US-0109 `two_stage` distinct from US-0093 UAT browser smoke |
| **R2** Secret leakage in probe config | Names-only ref contract (US-0085); fail-closed on absent env key; no secret values in scratchpad |
| **R3** Retry-loop side effects | Re-enter publish PASS path only (no execute re-entry); idempotent (no duplicate ledger rows; retry_count tag) |
| **R4** US-0107 ordering dependency | Mitigated — US-0107 DONE (released S0107); deferral register schema frozen |
| **R5** Convergence interaction | US-0110 reads open deferrals; `DEPLOY_DEFERRED` rows contribute to `zero_deferrals` conjunct; no new US-0110 logic required |
| **R6** Deploy-timeout vs sovereign-loop-timeout precedence | Deploy-timeout wins concurrent; `DEPLOY_HEALING_TIMEOUT` deferral emitted |

## Execute steps 29-31 wiring (AC-9)

| Step | Action | Position |
|------|--------|----------|
| **29** | Post-deploy smoke probe (two-stage per L2) | After step 28 (US-0108 merge+cleanup); after US-0047 step 22 + US-0107 step 24 |
| **30** | Retry loop: on probe FAIL, re-enter publish PASS path; on cap exhaustion → step 31 | After step 29 |
| **31** | DEPLOY_DEFERRED tuple via `append_deferral` (L4) | After step 30 |

## Consequences

- Sprint: S0109 in `sprints/S0109/`
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

## Evidence references

- `docs/product/backlog.md` — `## US-0109` (discovery notes + research notes)
- `docs/engineering/research.md` — `R-0097` (Q1–Q11 closed)
- `decisions/DEC-0109.md` — binding decision (locked)
- `handoffs/po_to_tl.md` — discovery handoff + research handoff
- `docs/engineering/state.md` — discovery checkpoint + research checkpoint + architecture checkpoint (this section)
- Shipped compose surfaces: US-0054 (`release_publish.py`), US-0100 (`version_changelog.py`), US-0103 (`decision_ledger_lib.py`), US-0107 (`sovereign_loop_lib.py` + `sovereign_deferrals.jsonl`), US-0110 (`sovereign_convergence_lib.py`)

# US-0111 — Release-Trigger-Driven Version Changelog Derivation

- **Priority**: P2
- **Status**: OPEN
- **Sprint**: S0111
- **DEC**: DEC-0111
- **Research**: R-0098 (Q1–Q10 CLOSED)
- **Compose guards**: US-0100 (read-only), US-0054 (read-only), US-0103 (append-only consumer), US-0008 (read-only), US-0040 (read-only), US-0107 (read-only), US-0110 (read-only)

## Story Summary

Extend US-0100 version-scoped changelog generation to support multiple release trigger sources (GitHub webhook, npm publish, git tag push, manual /release command) beyond the current /release-only path. Detect trigger source automatically, extract version information, compute version diff via `release_changelog_lib.compare_versions()`, generate `handoffs/releases/{semver}-release-notes.md`, atomically promote `[Unreleased]` to `[semver]` in `CHANGELOG.md`, and emit `(semver, previous_semver, timestamp)` event for downstream processing. Maintain backward compatibility with `RELEASE_TRIGGER_SOURCE=manual`. Integrate with sovereign-loop US-0103 ledger for audit trail.

## Architecture

### Adapter Registry Pattern

`scripts/release_trigger_adapters.py` provides extensible abstract `ReleaseAdapter` base class with four concrete adapters:

1. `GithubReleaseAdapter` — parses GitHub webhook payload (`action=published`), extracts tag from `release.tag_name`, queries GitHub API for previous release tag (sorted by `created_at` descending, skip current). Handles missing tag → fail `RELEASE_TRIGGER_TAG_MISSING`. Handles missing previous → fail `RELEASE_TRIGGER_PREVIOUS_MISSING`.
2. `NpmPublishAdapter` — reads `package.json` version, queries npm registry for previous published versions (`npm view {pkg} versions --json`), computes previous_version via semver comparison. Handles missing package.json → fail `RELEASE_TRIGGER_PACKAGE_JSON_MISSING`.
3. `GitTagAdapter` — parses git tag push event (extract tag from ref), sorts all tags by `taggerdate` descending, computes previous_version via semver comparison. Handles missing tag → fail `RELEASE_TRIGGER_TAG_MISSING`.
4. `ManualReleaseAdapter` — backward-compatible with existing `/release` command behavior when `RELEASE_TRIGGER_SOURCE=manual` (default).

### `TriggerContext` Data Structure

```python
@dataclass
class TriggerContext:
    version: str  # semver string
    previous_version: Optional[str]  # semver string or None if first release
    source: str  # adapter identifier: "github"|"npm"|"git_tag"|"manual"
    metadata: dict  # adapter-specific payload
```

All downstream consumers (compare_versions, notes generation, ledger event) consume `TriggerContext` only — never adapter-specific payloads.

### Scratchpad Keys

| Key | Values | Default |
|-----|--------|---------|
| `RELEASE_TRIGGER_SOURCE` | `manual\|github\|npm\|git_tag` | `manual` |

When `RELEASE_TRIGGER_SOURCE=manual` (default), existing `/release` path is byte-identical — zero behavior change.

### US-0100 Compose (Read-Only)

US-0111 calls `release_changelog_lib.compare_versions(target_version)` and `promote_unreleased()` — both functions remain unchanged. US-0111 extends adapter dispatch layer **before** these calls. No US-0100 API changes.

### US-0103 Ledger Compose (Consumer-Only Append)

Emit `(semver, previous_semver, timestamp, derivation_decisions[])` event via `append_entry(decision_type=version_derivation, payload=event_dict)`. Ledger schema unchanged; US-0111 uses existing API. JSON event written to `handoffs/release_events/{iso-timestamp}-{semver}.json`.

### Atomic Promotion

Write to temp file in same directory as target, then `os.replace(temp, target)`. On Windows, catch `PermissionError` and retry once after 0.1s sleep. On failure: restore previous `CHANGELOG.md`, fail with `RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED`.

## Reason Codes (AC-10)

9 fail-closed codes: `RELEASE_TRIGGER_ADAPTER_FAILED`, `RELEASE_TRIGGER_TAG_MISSING`, `RELEASE_TRIGGER_PREVIOUS_MISSING`, `RELEASE_TRIGGER_PACKAGE_JSON_MISSING`, `RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED`, `RELEASE_TRIGGER_NOTES_WRITE_FAILED`, `RELEASE_TRIGGER_EVENT_EMIT_FAILED`, `RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED`, `RELEASE_TRIGGER_SOURCE_INVALID`.

## Contract Tests (AC-11)

`test_us0111_*` markers in `tests/us0111_contract_test.py`:

| Marker | Coverage |
|--------|----------|
| `test_us0111_adapter_registry_dispatch` | AC-1 — registry dispatch by source |
| `test_us0111_github_adapter_success_fail_closed` | AC-2 — GitHub webhook + API queries |
| `test_us0111_npm_adapter_success_fail_closed` | AC-3 — npm registry queries |
| `test_us0111_git_tag_adapter_success_fail_closed` | AC-4 — git tag push + semver sort |
| `test_us0111_manual_backward_compat_byte_identical` | AC-5 — manual path unchanged |
| `test_us0111_compare_versions_from_trigger_integration` | AC-6 — TriggerContext → compare_versions |
| `test_us0111_atomic_promotion_temp_rename` | AC-7 — os.replace + Windows best-effort |
| `test_us0111_per_version_notes_atomic_write` | AC-8 — notes file atomic write |
| `test_us0111_ledger_event_emit_shape` | AC-9 — (semver, previous, ts, decisions[]) |
| `test_us0111_reason_code_inventory_9_codes` | AC-10 — 9 codes present |
| `test_us0111_us0100_compose_no_derivation_semantics_change` | Compose — US-0100 unchanged |
| `test_us0111_us0054_compose_no_publish_semantics_change` | Compose — US-0054 unchanged |

Parity: `check_intake_template_parity.py --scope=release-triggers` when trigger logic or adapters touched.

## Risks (from R-0098)

- **R1**: GitHub rate limiting (60/h unauth vs 5k/h auth) — mitigate with `GITHUB_TOKEN` env var + git history fallback.
- **R2**: npm private registry auth via `.npmrc` inheritance.
- **R3**: Annotated vs lightweight tag ordering — use semver sort.
- **R4**: Windows atomic rename best-effort — document + test fallback.
- **R5**: Auto-detection ambiguity in CI — priority order documented (Q9).
- **R6**: Ledger event shape — JSON with `{semver, previous_semver, timestamp, derivation_decisions}`.

## AC surjective map

| AC | Title | Task |
|----|-------|------|
| AC-1 | Trigger adapter registry | T-001 |
| AC-2 | GitHub webhook adapter | T-002 |
| AC-3 | npm publish trigger | T-003 |
| AC-4 | Git tag push trigger | T-004 |
| AC-5 | Manual backward compatibility | T-005 |
| AC-6 | Version comparison logic | T-006 |
| AC-7 | Atomic promotion | T-007 |
| AC-8 | Per-version notes generation | T-008 |
| AC-9 | Sovereign loop integration | T-009 |
| AC-10 | Fail-closed reason codes | T-010 |
| AC-11 | Contract tests + template parity | T-011 |
| AC-12 | Documentation + runbook updates | T-012 |

All 12 ACs mapped 1:1 to 12 tasks — bijection (hence surjective). Task count 12 ≤ `SPRINT_MAX_TASKS=12`. At threshold exactly, `SPRINT_AUTO_SPLIT` not triggered.

## Tranche Order

1. **A** — adapter registry + `TriggerContext` (T-001)
2. **B** — four concrete adapters (T-002, T-003, T-004, T-005)
3. **C** — version comparison (T-006) + atomic promotion (T-007) + per-version notes (T-008) + sovereign loop integration (T-009) + reason codes (T-010)
4. **D** — contract tests (T-011) + documentation + runbook (T-012)

---

# US-0112 — Ship Model-Catalog Example Presets on Install/upgrade

## Overview

**US-0112** extends the installer framework (US-0008/US-0018/US-0057/US-0075) to deliver all 8 committed `model-catalog.local.example*.json` presets (base, cursor-only, level 1–4, role-based balanced/highend) via the installer manifest. Previously these files existed only in `template/.cursor/` but were absent from `installer-owned-paths.manifest`, forcing operators to manually copy presets when enabling `MODEL_RESOLVE=local_catalog` or `role_catalog`. US-0112 completes DEC-0086/DEC-0087 delivery without altering catalog schema, model precedence, or the active operator-owned `model-catalog.local.json`.

**Binding decision**: **DEC-0112** (Accepted). **Research anchor**: **R-0090** (delivered; Q1–Q8 closed). **Compose guards (non-negotiable)**: DO NOT amend US-0008, US-0018, US-0040, US-0054, US-0057, US-0075, US-0100, US-0101, US-0102, US-0103, US-0107, US-0110. **Upstream DONE dependencies**: US-0018, US-0057, US-0075, US-0101, US-0102.

**Fresh context marker**: `tl-US0112-architecture-20260630T220000Z-fresh`
**Orchestrator run id**: `auto-20260628-04`
**Timestamp**: 2026-06-30T22:00:00Z
**Verdict**: PASS
**Next**: `/sprint-plan`

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A | **Add 8 example paths to installer manifest** (active + template byte-parity); classify as framework files; `missing` copy-when-absent; `upgrade` refresh when template differs; never touch `model-catalog.local.json` | **Preferred** — reuses US-0075/US-0018/US-0057 framework semantics; zero new code paths; manifest-driven single source of truth |
| B | **Auto-bootstrap `model-catalog.local.json` from a default preset** | **Rejected** — 8 presets exist; operator choice required; catalog schema ownership conflict with DEC-0086/DEC-0087; violates gitignore boundary (L5) |
| C | **Hardcode installer copy logic for 8 examples** (no manifest change) | **Rejected** — violates US-0008 installer manifest-driven pattern; requires installer code changes per example file |
| D | **New installer classification mode** for examples vs framework | **Rejected** — framework file semantics (US-0075/US-0018/US-0057) already cover refresh-on-stale behavior; ADDITIVE only |
| E | **Amend DEC-0086/DEC-0087** catalog schema or precedence | **Rejected** — violates compose guard; US-0112 completes delivery path only |

## Normative locks (L1–L10 from research R-0090)

| Lock | Decision |
|------|----------|
| **L1** Eight preset filenames | `.cursor/model-catalog.local.example.json`, `.cursor/model-catalog.local.example.cursor-only.json`, `.cursor/model-catalog.local.example.level-1-easy.json`, `.cursor/model-catalog.local.example.level-2-complex.json`, `.cursor/model-catalog.local.example.level-3-mega.json`, `.cursor/model-catalog.local.example.level-4-super.json`, `.cursor/model-catalog.local.example.role-based-balanced.json`, `.cursor/model-catalog.local.example.role-based-highend.json` |
| **L2** Manifest rows | 8 paths added under `[install_include_paths]` in both active `docs/engineering/context/installer-owned-paths.manifest` + `template/docs/engineering/context/installer-owned-paths.manifest` (16 rows total, byte-parity) |
| **L3** Missing mode | `installer.py` / `installer.ps1` / `installer.sh` `missing` mode copies each example into target `.cursor/` when absent; deterministic log/status per file (names-only); same semantics as `scratchpad.local.example.md` |
| **L4** Upgrade framework refresh | `upgrade` mode classifies `model-catalog.local.example*.json` as framework; overwrite when template content differs (same semantics as `scratchpad.local.example.md` per US-0075); unchanged examples counted as unchanged; **never** modifies `model-catalog.local.json` |
| **L5** Active catalog protection | `.cursor/model-catalog.local.json` remains gitignored and outside `install_include_paths` and `clean_paths`; no installer mode copies template examples to that path automatically |
| **L6** Triple installer parity | PS1 `List-SourceFiles` / Python equivalent / Bash equivalent all read single `[install_include_paths]` manifest; all 8 examples included from packaged `template/` |
| **L7** Runbook recipe anchor | `docs/engineering/runbook.md` § Model Tier / Catalog subsection; documents: examples ship on install/upgrade; operator copies chosen preset → `model-catalog.local.json`; lists all 8 filenames + complexity/role intent |
| **L8** Test markers | 8+ `test_us0112_*` markers: `test_us0112_manifest_lists_eight_paths`, `test_us0112_missing_adds_absent_examples`, `test_us0112_upgrade_refreshes_framework_examples`, `test_us0112_upgrade_preserves_unchanged`, `test_us0112_local_catalog_never_touched`, `test_us0112_triple_installer_parity`, `test_us0112_runbook_lists_eight_filenames`, `test_us0112_parity_scope_model_catalog_examples` |
| **L9** Parity scope | `check_intake_template_parity.py --scope=model-catalog-examples` with `MODEL_CATALOG_EXAMPLE_PAIRS` constant (16 rows active+template manifest byte-parity) |
| **L10** Architecture section | `docs/engineering/architecture.md` `# US-0112` documents framework vs operator boundary, manifest rows, upgrade classification, DEC-0086/DEC-0087 compose |

## AC → task surjective map

| AC | Tasks |
|----|-------|
| AC-1 Manifest completeness (8 paths) | T-001, T-002 |
| AC-2 Missing mode delivery (triple installer) | T-003, T-004, T-005 |
| AC-3 Upgrade framework refresh | T-006 |
| AC-4 Active catalog protection | T-009 |
| AC-5 Triple installer parity | T-003, T-004, T-005 |
| AC-6 Runbook operator recipe | T-008 |
| AC-7 Contract tests + parity | T-007, T-009 |
| AC-8 Architecture notes + DEC-0112 + template parity | T-010, T-011 |

**Surjectivity check**: AC-1..AC-8 all covered. **Total**: 11 task seeds ≤ `SPRINT_MAX_TASKS=12` — `SPRINT_AUTO_SPLIT` not triggered.

## Task seeds (T-001..T-011)

| ID | Title | AC | Tranche |
|----|-------|----|:---------|:---------|
|---|-----|--|-----|
| T-001 | Add 8 `model-catalog.local.example*.json` rows to active `docs/engineering/context/installer-owned-paths.manifest` under `[install_include_paths]` | AC-1 | A |
| T-002 | Mirror 8 rows in `template/docs/engineering/context/installer-owned-paths.manifest` (byte-parity; 16 rows total active vs template) | AC-1 | A |
| T-003 | Verify `missing`-mode `installer.py` logic copies 8 absent framework files (same semantics as `scratchpad.local.example.md`) | AC-2, AC-5 | B |
| T-004 | Verify `missing`-mode `installer.ps1` logic parity (`List-SourceFiles` includes all 8 examples) | AC-2, AC-5 | B |
| T-005 | Verify `missing`-mode `installer.sh` logic parity (manifest-driven file set identical) | AC-2, AC-5 | B |
| T-006 | Verify `upgrade`-mode logic: refresh stale `model-catalog.local.example*.json`, skip unchanged, never touch `model-catalog.local.json`; framework classification per US-0075/US-0018/US-0057 semantics | AC-3, AC-4 | B |
| T-007 | Implement `check_intake_template_parity.py --scope=model-catalog-examples` with `MODEL_CATALOG_EXAMPLE_PAIRS` constant (active vs template manifest byte-parity check) | AC-7 | C |
| T-008 | Write runbook `§model-catalog` preset recipe (operator copies one preset → `model-catalog.local.json`); lists all 8 filenames + complexity/role intent; anchor `docs/engineering/runbook.md` § Model Tier / Catalog | AC-6 | C |
| T-009 | Write 8+ `test_us0112_*` contract test markers in `tests/us0112_contract_test.py`: manifest 8 paths, missing adds, upgrade refreshes, upgrade preserves unchanged, local never touched, triple parity, runbook literals, parity scope | AC-7 | C |
| T-010 | Document architecture notes in `docs/engineering/architecture.md` `# US-0112` (framework vs operator boundary, manifest rows, upgrade classification, DEC-0086/DEC-0087 compose) + author companion `decisions/DEC-0112.md` | AC-8 | D |
| T-011 | Verify template parity for all touched files (manifest, runbook, architecture, DEC-0112) | AC-8 | D |

## Tranche order

1. **A** — manifest rows (active + template byte-parity) (T-001, T-002)
2. **B** — installer missing/upgrade framework-file copy + refresh (T-003, T-004, T-005, T-006)
3. **C** — parity scope `--scope=model-catalog-examples` + runbook recipe + contract tests (T-007, T-008, T-009)
4. **D** — architecture notes + DEC-0112 + template parity verification (T-010, T-011)

## Compose guards (non-negotiable)

| Story | Compose rule |
|-------|--------------|
| **US-0008** | Installer manifest-driven copy semantics unchanged — US-0112 adds rows only |
| **US-0018** | Smart upgrade framework semantics unchanged — US-0112 is consumer of same framework classification |
| **US-0040** | Per-sprint release notes semantics unchanged |
| **US-0054** | Configurable release publish unchanged | **US-0057** | Framework file refresh semantics unchanged — US-0112 reuses same pattern |
| **US-0075** | `scratchpad.local.example.md` framework-file semantics unchanged — US-0112 applies same semantics to `model-catalog.local.example*.json` |
| **US-0100** | Semantic changelog unchanged |
| **US-0101** | Catalog schema unchanged (DEC-0086); US-0112 does NOT alter `model_tier_lib.py` or `MODEL_TIER_*` or alias resolution |
| **US-0102** | Role catalog precedence unchanged (DEC-0087); US-0112 does NOT amend precedence |
| **US-0103** | Ledger semantics unchanged |
| **US-0107** | Daemon loop semantics unchanged |
| **US-0110** | Goal convergence semantics unchanged |

## Risks

1. **Installer manifest drift**: 8 new rows added but not kept in sync across active/template — mitigated by byte-parity constant `MODEL_CATALOG_EXAMPLE_PAIRS` + `test_us0112_manifest_lists_eight_paths`.
2. **Active catalog accidental install**: `model-catalog.local.json` leaked into manifest — mitigated by `test_us0112_local_catalog_never_touched` regression guard.
3. **Triple installer drift**: PS1/Python/Bash diverge — mitigated by single manifest source of truth + `test_us0112_triple_installer_parity`.
4. **Stale upgrade after rename**: operator's example file from prior version lingers — mitigated by framework refresh semantics (overwrite when template differs; US-0075/US-0018/US-0057 precedent).
5. **Operator confusion (8 presets, no selection guidance)**: mitigated by runbook recipe listing all 8 filenames + complexity/role intent (L7).
6. **npm `package.json` files gap**: mitigated — already covered by `template/` glob; verify at /execute.

## Consequences

- Sprint: S0112 (pending /sprint-plan)
- Status authority: **OPEN** per **US-0045**; closure at `/release`.
- Installer manifest grows by 8 rows × 2 (active + template) = 16 total rows.
- Operator gains access to 8 model-catalog example presets after install/upgrade.
- Active catalog (`model-catalog.local.json`) remains under operator full control.
- No new installer code paths; no catalog schema changes; no precedence changes.

## Evidence references

- `docs/product/backlog.md` — `## US-0112` (discovery notes + research notes)
- `docs/engineering/research.md` — `R-0090` (Q1–Q8 closed)
- `decisions/DEC-0112.md` — binding decision (locked)
- `handoffs/po_to_tl.md` — discovery handoff + research handoff
- `docs/engineering/state.md` — discovery checkpoint + research checkpoint + architecture checkpoint (this section)
- Shipped compose surfaces: US-0018 (smart upgrade), US-0057 (framework file refresh), US-0075 (example-first refresh), US-0101 (DEC-0086 catalog schema), US-0102 (DEC-0087 role catalog)

# BUG-0013 — Scratchpad example stale (template example missing 9 sections written to canonical)

## Overview

**BUG-0013** is a packaging/parity defect — not a feature story. The canonical `.cursor/scratchpad.md` (540 lines) has been extended with 9 sovereign-loop feature sections (US-0103 through US-0111) that were never mirrored to `template/.cursor/scratchpad.local.example.md` (379 lines, stale). `installer.py` already reads from `template/` (correct per R-0099 Q2); the installer manifest already lists `template/.cursor/scratchpad.local.example.md` (correct). The fix is a deterministic file-copy + parity enforcement + runbook anchoring. No architectural decision record (DEC) required — R-0099 Q6 confirmed compose guards honored, no DEC surface.

**Research anchor**: **R-0099** (delivered 2026-07-01T23:01:00Z, Q1–Q6 closed). **Companion DEC: none** (per R-0099 Q6). **Status authority**: **OPEN** per **US-0045** (closure at `/release`).

## Fix approach (locked)

1. **(A1) File-copy sync** — replace `template/.cursor/scratchpad.local.example.md` with canonical `.cursor/scratchpad.md` content, **preserving** the example-only header comment (first 5 lines documenting consumer-facing copy-to-local semantics) and **excluding** any project-local override section (operator-specific values). Feature-flag keys, section structure, and default values must match canonical byte-for-byte after the header.
2. **(A2) Parity enforcement** — single-source-of-truth contract: template example = packaged consumer view of canonical scratchpad. No installer.py / installer.ps1 / installer.sh changes required.
3. **(A3) Regression proof** — new test file `tests/scratchpad_example_parity_test.py` enforcing feature-flag-key and section-header parity between template example and canonical (diff-ignore-list covers example-header + project-local overrides).
4. **(A4) Runbook anchor** — new § "Scratchpad example parity" in `docs/engineering/runbook.md` documenting: when canonical scratchpad is extended, template example must be re-synced; single-source-of-truth preference.
5. **(A5) Validator satisfaction** — AC-5 (`bug_issue_validate.py --check-acceptance` → `[BUG_VALIDATION_OK]`) and AC-6 (`intake_bug_resume_brief_refresh.py --bug-id BUG-0013 --validate-file` → PASS).

## Files to touch

| File | Action | Notes |
|---|---|---|
| `template/.cursor/scratchpad.local.example.md` | sync from canonical | preserve example-header (lines 1–5); exclude project-local overrides section |
| `tests/scratchpad_example_parity_test.py` | new | parity + header-preserved + local-overrides-preserved |
| `docs/engineering/runbook.md` | add § | "Scratchpad example parity" |
| `docs/product/backlog.md` | append | research_notes + architecture_notes (this phase done) |
| `docs/engineering/state.md` | append | architecture checkpoint (this phase done) |
| `docs/engineering/architecture.md` | append | this `# BUG-0013` H1 section (per DEC-0054/DEC-0076/BUG-0010 authoring mandate) |
| `handoffs/resume_brief.md` | prepend | next-phase pointer `/sprint-plan` |

## Files NOT to touch

- `.cursor/scratchpad.md` — canonical source of truth (do not modify during fix).
- `installer.py`, `installer.ps1`, `installer.sh` — already correct per R-0099 Q2.
- `template/.cursor/scratchpad.md` — not a packaged source (installer reads from template example, not canonical copy).
- All compose guards — **UNCHANGED**: US-0008, US-0040, US-0054, US-0100, US-0101, US-0102, US-0103, US-0107, US-0110.

## Sprint task seeds (3 tasks; default `SPRINT_MAX_TASKS=12`)

- **T-001** — Sync `template/.cursor/scratchpad.local.example.md` from canonical `.cursor/scratchpad.md`: copy canonical content (lines 1 through 387, lines 540 through EOF) preserving example-only header (first 5 lines) and excluding any project-local override section. Do NOT copy project-local flag overrides.
- **T-002** — Write parity test `tests/scratchpad_example_parity_test.py`: `test_bug0013_parity_check`, `test_bug0013_header_preserved`, `test_bug0013_local_overrides_preserved`, plus per-section coverage markers (`test_bug0013_section_US0103_present` … `test_bug0013_section_US0111_present`). Parity scope: `--scope=scratchpad-example`.
- **T-003** — Add runbook section "Scratchpad example parity" to `docs/engineering/runbook.md`: documents when canonical is extended, template must re-sync; single-source-of-truth preference.

## Test markers (3 minimum, 12 recommended)

- `test_bug0013_parity_check` — template example contains every feature-flag key and section header present in canonical.
- `test_bug0013_header_preserved` — example-only header (first 5 lines of template) is intact and not overwritten by canonical.
- `test_bug0013_local_overrides_preserved` — project-local overrides section (operator-specific values) is not leaked into template.
- Per-section markers (optional but recommended): `test_bug0013_section_US0103_present`, `test_bug0013_section_US0110_present`, `test_bug0013_section_US0104_present`, `test_bug0013_section_US0105_present`, `test_bug0013_section_US0107_present`, `test_bug0013_section_US0106_present`, `test_bug0013_section_US0108_present`, `test_bug0013_section_US0109_present`, `test_bug0013_section_US0111_present`.

## Risks

- **R1** (from R-0099) — Template example future divergence → mitigated by T-002 parity test + T-003 runbook §.
- **R2** (from R-0099) — Project-local overrides leak into template → mitigated by explicit diff ignore-list in parity test.
- **R3** (residual) — `template/.cursor/scratchpad.local.example.md` example header drift over time → mitigate by locking header to a stable 5-line block and asserting `test_bug0013_header_preserved` in every `/qa` run. No fix required now.

## Compose-guards confirmation

**8 guards UNCHANGED**: US-0008, US-0040, US-0054, US-0100, US-0101, US-0102, US-0103, US-0107, US-0110. This bug lives entirely outside the compose surface (no compose-surface files touched by T-001/T-002/T-003).

## Evidence references

- `docs/product/backlog.md` — `### BUG-0013` (discovery + research + architecture notes — this phase done for research+architecture)
- `docs/engineering/research.md` — `R-0099` (delivered, Q1–Q6 closed)
- `docs/engineering/architecture.md` — this `# BUG-0013` section
- `docs/engineering/state.md` — architecture checkpoint (this phase)
- `handoffs/resume_brief.md` — next-phase pointer to `/sprint-plan`
- `docs/engineering/runbook.md` — § "Scratchpad example parity" (to be added at /execute)
- `tests/scratchpad_example_parity_test.py` — parity test (to be added at /execute)

## Stop condition

**PASS** — no major tradeoff requires DEC; no feasibility unknown; no data migration risk. Per R-0099 Q6, no DEC required. Handoff to `/sprint-plan` (tech-lead, fresh subagent spawn).

# BUG-0014 — README Catalog Coverage Backfill (sovereign-loop era features + release_notes legacy pointer)

## Overview

**BUG-0014** is a documentation-coverage defect — sovereign-loop era features (US-0103..US-0112, BUG-0013) were released between 2026-06-28 and 2026-07-02 without being added to the README feature coverage catalog surfaces. Additionally, `handoffs/release_notes.md` is missing finalized-note entries for 5 sprints (S0103, S0104, S0105, S0106, S0108). The validator `validate_readme_feature_coverage.py --enforce` reports 117 missing coverage rows — full backfill required.

**Research anchor**: **R-0100** (delivered 2026-07-03T17:35:00Z, Q1–Q6 closed). **Companion DEC: none** (documentation-only, no architectural surface changed). **Status authority**: **OPEN** per **US-0045** (closure at `/release`).

## Fix approach (locked)

1. **(A1) Full catalog backfill**: Add 125 catalog rows (112 US + 13 BUG) to BOTH `its_magic/README.md` (root H2 sections) and `docs/developer/README.md` (dev H2 sections). Row format: `its_magic/README.md` uses bullet with item_id mention (e.g. `/slug description **US-xxxx**`); `docs/developer/README.md` uses bold item_id or traceability line (e.g. `**US-xxxx** description`).
2. **(A2) Template parity sync**: After catalog edits to `its_magic/README.md`, byte-copy to `template/its_magic/README.md` to satisfy parity check.
3. **(A3) Release notes backfill**: Add 5 finalized-note entries to `handoffs/release_notes.md` (S0103, S0104, S0105, S0106, S0108), following existing S0107/S0109–S0112 format.

## Files to touch

| File | Action | Notes |
|---|---|---|
| `its_magic/README.md` | backfill 125 catalog rows | US-0001..US-0112 + BUG-0001..BUG-0013 in root H2 sections |
| `docs/developer/README.md` | backfill same 125 catalog rows | US-0001..US-0112 + BUG-0001..BUG-0013 in dev H2 sections |
| `template/its_magic/README.md` | byte-copy from `its_magic/README.md` | after catalog edits (parity check) |
| `handoffs/release_notes.md` | add 5 finalized-note entries | S0103, S0104, S0105, S0106, S0108 (follow S0107/S0109–S0112 format) |

## Files NOT to touch

- All compose guards: US-0091, US-0097, US-0040, US-0100, US-0101, US-0102, US-0103..US-0112 (UNCHANGED)
- All scripts (`scripts/validate_readme_feature_coverage.py`, `scripts/readme_feature_coverage_lib.py`, etc.)
- All installer files (`installer.py`, `installer.ps1`, `installer.sh`)
- All sovereign-loop scripts and Python/PowerShell/Shell files

## Sprint task seeds (4 tasks; default `SPRINT_MAX_TASKS=12`)

- **T-001** — Backfill `its_magic/README.md` with 125 catalog rows (US-0001..US-0112 + BUG-0001..BUG-0013) in appropriate H2 sections. Row format per R-0100 Q4.
- **T-002** — Backfill `docs/developer/README.md` with same 125 catalog rows in dev H2 sections. Bold item_id or traceability line format.
- **T-003** — Sync `template/its_magic/README.md` from `its_magic/README.md` (byte-identical copy after edits).
- **T-004** — Add 5 missing release notes entries to `handoffs/release_notes.md` (S0103, S0104, S0105, S0106, S0108).

## Test markers (3 minimum)

- `test_bug0014_readme_catalog_backfill` — verify `validate_readme_feature_coverage.py --enforce` returns `[README_FEATURE_COVERAGE_VALIDATE_OK]` after T-001/T-002.
- `test_bug0014_template_parity` — verify `template/its_magic/README.md` matches `its_magic/README.md` after T-003.
- `test_bug0014_release_notes` — verify 5 entries present in `handoffs/release_notes.md` after T-004.

## Compose-guards confirmation

**16 guards UNCHANGED**: US-0091, US-0097, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0106, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112. This bug lives entirely outside the compose surface (documentation-only, no code/scripts/installers touched).

## Risks

- **R1 (MEDIUM)**: Full 125-row backfill is large but bounded. Mitigate with deterministic row template per R-0100 Q4/Q5, peer-review traceability before `/qa`.
- **R2 (LOW)**: Template copy of `its_magic/README.md` must be refreshed AFTER catalog edits. Mitigate with explicit step ordering in sprint (T-003 after T-001).
- **R3 (INFO)**: Backlog parser does not recognize DONE/user_visible fields for US-0103..US-0110 (parser-normalization debt tracked separately). Mitigate by adding catalog rows preemptively for those 8 US items.

## Evidence references

- `docs/product/backlog.md` — `### BUG-0014` (lines 4168–4182, discovery + research + architecture notes)
- `docs/engineering/research.md` — `R-0100` (delivered, Q1–Q6 closed)
- `docs/engineering/architecture.md` — this `# BUG-0014` section
- `docs/engineering/state.md` — architecture checkpoint (this phase)
- `handoffs/resume_brief.md` — next-phase pointer to `/sprint-plan`
- `handoffs/release_notes.md` — 5 entries to be added at `/execute`
- `its_magic/README.md` lines 65–88 — 125 rows to be added at `/execute`
- `docs/developer/README.md` — 125 rows to be added at `/execute`

## Stop condition

**PASS** — no major tradeoff requires DEC; no feasibility unknown; no data migration risk. Per R-0100 Q6, no DEC required. Handoff to `/sprint-plan` (tech-lead, fresh subagent spawn).

---

# US-0113 — Sovereign-loop operator documentation in framework README

## Overview

**US-0113** is a documentation-only story closing the operator-documentation gap for the sovereign-loop era feature set (US-0103..US-0112, excluding US-0106 which belongs to the US-0117 family). It adds an umbrella `### Sovereign-loop era (US-0103–US-0112)` narrative section under `## Commands and workflow` in `its_magic/README.md`, with 9 nested per-feature `####` operator subsections, plus a matching extension of the `### Full scratchpad reference (detailed)` section with sovereign-loop keys grouped by feature. The framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`) is kept byte-identical via one-way copy. No code, schema, installer, scratchpad canonical, or runbook content changes.

**Binding decision**: **companion_dec=none** (US-0113 is documentation-only; no architectural, policy, or schema surface is being changed; R-0101 Q-scope resolved as docs backfill only). **Research anchor**: **R-0101** (delivered 2026-07-04T00:47:30Z, 3/3 open questions closed). **Compose guards (non-negotiable)**: DO NOT amend US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103..US-0112. **Status authority**: **OPEN** per **US-0045** (closure at `/release`).

**Fresh context marker**: `tl-US0113-architecture-20260703T232718Z-fresh`
**Orchestrator run id**: `auto-20260704-01`
**Timestamp**: 2026-07-03T23:27:18Z
**Verdict**: PASS
**Next**: `/sprint-plan`

## Companion DEC

**companion_dec=none**. Confirmed (not overriding research R-0101). Justification:

- US-0113 introduces **no** new architectural surface — no schema, no code path, no installer classification, no policy, no precedence rule, no role matrix change.
- The "operator-documentation gap closing" pattern is a recurring documentation-only pattern already established by BUG-0013 / BUG-0014 (both shipped with `companion_dec=none` per R-0099 / R-0100). US-0113 follows the same precedent.
- The 3 discovery open questions were all resolved within the `plan` macro as docs backfill decisions (R-0101 § open_questions_resolution); none required operator input or a tradeoff record.
- Next available DEC id would be `DEC-0113` (highest existing is `DEC-0112` in `decisions/DEC-0112.md`); reserving it would be wasteful since there is no decision surface to record.

## Approach locked

**approach_locked=A1** — Single umbrella `### Sovereign-loop era (US-0103–US-0112)` section with 9 nested `#### US-xxxx` subsections (h4 under h3 umbrella), placed under `## Commands and workflow` (L350), before `### Full scratchpad reference (detailed)` (L940).

### Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| **A1** | Single umbrella `### Sovereign-loop era (US-0103–US-0112)` + 9 nested `#### US-xxxx` subsections (h4 under h3) | **Locked** — preferred for navigation; matches existing README hierarchy pattern (umbrella → per-feature detail); preserves AC-2 "per-feature operator subsections" wording naturally; keeps the 9 features visually grouped as an era rather than scattered across `## Commands and workflow`. |
| **A2** | Flat 9 `#### US-xxxx` subsections directly under `## Commands and workflow` with cross-links but no umbrella | **Rejected** — loses era grouping; scatters sovereign-loop features among unrelated workflow subsections; weakens AC-1 (umbrella section is an explicit AC); harder for operators to discover the sovereign-loop feature cluster. |
| **A3** | Place umbrella under `## Features (what its-magic can do)` instead of `## Commands and workflow` | **Rejected** — `## Features` already has the US-0091 catalog one-liners (L63 anchor, L1235–L1243); AC-1 explicitly requires the umbrella under `## Commands and workflow`; narrative operator guides are workflow-shaped, not catalog-shaped. |

## Files to touch

| File | Action | Notes |
|---|---|---|
| `its_magic/README.md` | append umbrella + 9 subsections under `## Commands and workflow`; extend `### Full scratchpad reference (detailed)` | AC-1, AC-2, AC-3; catalog block L63 + L1235–L1243 treated as read-only (AC-4) |
| `template/its_magic/README.md` | one-way byte-sync copy from `its_magic/README.md` after edits | AC-5 lockstep; `cmd /c fc /b` + `check_intake_template_parity.py` re-run required |

**Explicitly NOT touched** (decision):

- `docs/engineering/architecture.md` — the 5 missing `# US-xxxx` h1 anchors (US-0103/0104/0105/0107/0110) are **deferred to US-0117** (phase & role governance family), not added in US-0113. See carry-over (a) below. The only architecture.md edit in this phase is the append of this `## US-0113` section (the architecture anchor for US-0113 itself).
- `docs/developer/README.md` — research R-0101 did not identify this as a touch target. AC-6 (audience + metadata hygiene) is a **validator gate**, not an edit mandate; US-0113 narrative subsections live in the framework README pair only. The developer README is a separate audience surface owned by US-0097 (project README parity) compose guard.

## Files NOT to touch

- `.cursor/scratchpad.md` — canonical source of truth (never edit in docs stories; BUG-0013 precedent).
- `template/.cursor/scratchpad.local.example.md` — canonical example (BUG-0013 ownership; US-0113 does not extend the scratchpad canonical, only documents existing keys in README).
- `docs/product/backlog.md` — status authority (closure only at `/release`).
- `docs/engineering/runbook.md` — AC-7 cross-links only; **no new runbook content** (AC-7 forbids duplication). All 9 runbook anchors already exist (R-0101 § runbook cross-link targets).
- `docs/developer/README.md` — separate audience surface; not in US-0113 scope (see above).
- `docs/engineering/architecture.md` (other than this `## US-0113` append) — 5 missing feature h1 anchors deferred to US-0117.
- `installer.py`, `installer.ps1`, `installer.sh` — no installer changes (US-0008/US-0018/US-0057/US-0075 compose guards).
- All scripts (`scripts/validate_readme_feature_coverage.py`, `scripts/check_intake_template_parity.py`, `scripts/validate_doc_profile.py`, `scripts/check-user-visible-metadata.py`, etc.) — validators are read-only gates, not edit targets.
- All sovereign-loop scripts and Python/PowerShell/Shell files — US-0103..US-0112 features are **documented only**, not amended.

## Sprint seeds (T-001..T-006)

**6 task seeds** (≤ `SPRINT_MAX_TASKS=12` — `SPRINT_AUTO_SPLIT` not triggered).

| ID | Title | AC | Tranche |
|----|-------|----|:---------|:---------|
| **T-001** | Add `### Sovereign-loop era (US-0103–US-0112)` umbrella section under `## Commands and workflow` (L350), before `### Full scratchpad reference` (L940). Content: default-off posture callout, 9-step recommended enable order (AI_DECISION_LEDGER → SOVEREIGN_MEMORY → CROSS_MODEL_REVIEW → SOVEREIGN_GOAL_MODE=goal_convergence → AUTO_SOVEREIGN → SOVEREIGN_PARALLEL_DEV → AUTO_SOVEREIGN_SELF_HEALING_DEPLOY → RELEASE_TRIGGER_SOURCE → US-0112 presets), runbook pointer, zero-overhead-when-off contract paragraph. | AC-1 | A |
| **T-002** | Add 9 per-feature `#### US-xxxx` operator subsections nested under the umbrella, ordered US-id-ascending (US-0103 → US-0104 → US-0105 → US-0107 → US-0108 → US-0109 → US-0110 → US-0111 → US-0112). Each subsection: 1–3 sentence narrative (sovereign-loop angle for US-0111/US-0112), master enable flag + related keys with defaults, zero-overhead-when-off wording, runbook cross-link (existing anchor only — no duplication). US-0112 subsection references existing delivery/catalog keys (no new scratchpad block). US-0111/US-0112 subsections include "see US-0114 for release-workflow operator docs on this feature" pointers. | AC-2, AC-7 | A |
| **T-003** | Extend `### Full scratchpad reference (detailed)` (L940) with sovereign-loop keys. Ordering: **mirror `.cursor/scratchpad.md` L388–539 canonical ordering** (US-0103 → US-0110 → US-0104 → US-0105 → US-0107 → US-0108 → US-0109 → US-0111 → US-0112), NOT strict US-id-ascending. 9 sub-sub-sections grouped by feature. US-0112 sub-sub-section notes no dedicated sovereign-loop block; references L181–199 delivery/catalog keys. Default-off / zero-overhead-when-off wording per AC-3. | AC-3 | A |
| **T-004** | Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md` (one-way copy after T-001/T-002/T-003 complete). Re-run `cmd /c fc /b its_magic\README.md template\its_magic\README.md` (expect no differences) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK]`). | AC-5 | B |
| **T-005** | Run validators (AC-4, AC-6) and fix any drift. `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → expect `[README_FEATURE_COVERAGE_VALIDATE_OK]` with `coverage_missing=["US-0117"]` unchanged. `python scripts/validate_doc_profile.py` + `python scripts/check-user-visible-metadata.py` → expect PASS. Fix any narrative prose that leaks internal IDs (DEC-xxxx/R-xxxx/reason-codes) into user-visible sentences; US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. | AC-4, AC-6 | B |
| **T-006** | Run regression tests (AC-8) and confirm green. `python -m pytest tests/scratchpad_example_parity_test.py -q` → expect 4 passed (US-0113 does NOT modify `.cursor/scratchpad.md` or `template/.cursor/scratchpad.local.example.md`). Confirm no test weakenings — if a test fails, the prose is wrong, not the test. | AC-8 | B |

### AC → task surjective map

| AC | Tasks |
|----|-------|
| AC-1 Umbrella section | T-001 |
| AC-2 Per-feature operator subsections | T-002 |
| AC-3 Full scratchpad reference extension | T-003 |
| AC-4 Coverage preserved | T-005 |
| AC-5 Framework README parity | T-004 |
| AC-6 Audience + metadata hygiene | T-005 |
| AC-7 Runbook cross-links per feature | T-002 |
| AC-8 Regression tests | T-006 |

**Surjectivity check**: AC-1..AC-8 all covered. **Total**: 6 task seeds ≤ `SPRINT_MAX_TASKS=12` — `SPRINT_AUTO_SPLIT` not triggered.

## Test markers (existing — no new tests proposed)

| Marker | File | AC covered | Notes |
|--------|------|------------|-------|
| `test_bug0013_parity_check` + 3 companions | `tests/scratchpad_example_parity_test.py` | AC-5 (indirect), AC-8 | Confirms `.cursor/scratchpad.md` ↔ `template/.cursor/scratchpad.local.example.md` parity; US-0113 does not touch either file, so tests remain green by construction. |
| `validate_readme_feature_coverage.py --enforce` | `scripts/validate_readme_feature_coverage.py` | AC-4 | Coverage gate; `coverage_missing=["US-0117"]` must remain unchanged. |
| `check_intake_template_parity.py` | `scripts/check_intake_template_parity.py` | AC-5 | Framework README byte-parity gate. |
| `validate_doc_profile.py` | `scripts/validate_doc_profile.py` | AC-6 | Audience profile gate. |
| `check-user-visible-metadata.py` | `scripts/check-user-visible-metadata.py` | AC-6 | Metadata hygiene gate. |

**No new tests proposed.** R-0101 confirmed no test weakenings; AC-8 is satisfied by existing tests remaining green. Adding new tests would violate the "no test weakenings" spirit (US-0113 is documentation-only; tests are read-only gates).

## Compose guards (non-negotiable — all UNCHANGED)

| Story | Compose rule |
|-------|--------------|
| **US-0091** | Feature coverage catalog anchor `<!-- readme-feature-coverage-catalog -->` (L63) + one-liners (L1235–L1243) UNCHANGED — US-0113 appends narrative sections outside the catalog block. |
| **US-0097** | Project README parity surface UNCHANGED — US-0113 touches framework README pair only, not project README. |
| **US-0017** | Framework README parity contract UNCHANGED — US-0113 preserves byte-parity via T-004 lockstep. |
| **US-0040** | Per-sprint release notes semantics UNCHANGED. |
| **US-0100** | Semantic changelog UNCHANGED. |
| **US-0101** | Catalog schema (DEC-0086) UNCHANGED. |
| **US-0102** | Role catalog precedence (DEC-0087) UNCHANGED. |
| **US-0103** | AI Decision Ledger schema/semantics UNCHANGED — documented only. |
| **US-0104** | Cross-Model Adversarial Critic schema/semantics UNCHANGED — documented only. |
| **US-0105** | Sovereign Memory schema/semantics UNCHANGED — documented only. |
| **US-0107** | Sovereign Loop Mode schema/semantics UNCHANGED — documented only. |
| **US-0108** | Parallel Instance Arbitrage schema/semantics UNCHANGED — documented only. |
| **US-0109** | Self-Healing Deploy Loop schema/semantics UNCHANGED — documented only. |
| **US-0110** | Goal-Based Convergence schema/semantics UNCHANGED — documented only. |
| **US-0111** | Release Trigger Adapters schema/semantics UNCHANGED — documented only (sovereign-loop angle; release-workflow angle belongs to US-0114). |
| **US-0112** | Model-Catalog Example Presets schema/semantics UNCHANGED — documented only (sovereign-loop angle; release-workflow angle belongs to US-0114). |

**16 guards UNCHANGED.** US-0113 lives entirely outside the compose surface (documentation-only; no code/scripts/installers/scratchpad canonical touched).

## Carry-overs from research (resolution)

### (a) 5 missing `# US-xxxx` h1 anchors in `architecture.md`

**Decision: DEFER to US-0117** (phase & role governance family, which owns US-0069..US-0090 and naturally covers architecture anchors for sovereign-loop features).

**Justification**:

- AC-7 only requires **runbook** cross-links, which exist for all 9 features (R-0101 § runbook cross-link targets). The missing `architecture.md` h1 anchors are NOT a US-0113 AC.
- US-0113 is scoped as a **framework README** documentation story (`its_magic/README.md` pair). The `architecture.md` h1 anchors are an internal engineering-docs surface, not an operator-facing README surface. Mixing the two would blur the story's vertical-slice boundary.
- US-0117 (phase & role governance family) is the natural owner: it already covers architecture-doc anchors for governance features, and adding 5 minimal `# US-xxxx` h1 sections (summarizing locked normative content from R-0089/R-0092/R-0093/R-0094/R-0091 + DEC-0103/0104/0105/0107/0110) fits its scope cleanly.
- Deferring keeps US-0113 at 6 task seeds (well under `SPRINT_MAX_TASKS=12`); adding T-007 would still fit but would cross the story's vertical-slice boundary.

**Deferral note for orchestrator**: This is a **deferral candidate** for the orchestrator's segment-boundary advance hook. **DO NOT append to `handoffs/sovereign_deferrals.jsonl` in architecture phase** (per instructions). Note for orchestrator: when US-0117 enters `plan` macro, its discovery should narrow-read this section and add the 5 missing h1 anchors as a task seed. Anchor format to use at that time: `# US-xxxx — <feature title>` (matching existing `# US-0108`, `# US-0109`, `# US-0111`, `# US-0112` format).

### (b) Scratchpad reference extension ordering

**Decision: Mirror `.cursor/scratchpad.md` L388–539 canonical ordering** (US-0103 → US-0110 → US-0104 → US-0105 → US-0107 → US-0108 → US-0109 → US-0111 → US-0112), NOT strict US-id-ascending.

**Justification**:

- The canonical scratchpad is the **source of truth** for sovereign-loop key grouping. Mirroring its ordering preserves source-of-truth parity and makes it trivial for operators to cross-reference a key in the README against the canonical scratchpad.
- Strict US-id-ascending ordering (US-0103 → US-0104 → US-0105 → US-0107 → ...) would re-order keys relative to the canonical scratchpad, creating a cognitive mismatch for operators who read both surfaces.
- The AC-2 per-feature **narrative subsections** (umbrella area) use US-id-ascending ordering (matching backlog `related_us` field) — this is the **narrative** surface where chronological/US-id ordering aids discovery. The AC-3 **scratchpad reference extension** is a **reference** surface where canonical-source parity aids lookup. The two surfaces have distinct ordering rationales; locking them differently is intentional, not inconsistent.
- This matches the research recommendation (R-0101 § Recommended architecture approach point 2).

## Risks (finalized)

| Risk | Severity | Mitigation |
|------|----------|------------|
| **AC-5 parity lockstep** — `its_magic/README.md` edited but `template/its_magic/README.md` not synced (or vice versa) | **MEDIUM** | T-004 mandates one-way copy `its_magic/README.md` → `template/its_magic/README.md` after T-001/T-002/T-003 complete. Execute-phase must run `cmd /c fc /b its_magic\README.md template\its_magic\README.md` (expect no differences) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK]`). QA must re-verify both gates. |
| **AC-8 regression tests** — coverage parity contract tests weakened or failing | **LOW–MEDIUM** | US-0113 is documentation-only; **forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` in execute-phase task list. If a test fails, the prose is wrong, not the test — fix prose, never relax test. T-006 confirms green. |
| **AC-4 coverage drift** — catalog block accidentally reflowed | **LOW** | T-005 runs `validate_readme_feature_coverage.py --enforce`; `coverage_missing=["US-0117"]` must remain unchanged. Catalog block L63 + L1235–L1243 treated as read-only. |
| **AC-6 metadata leakage** — internal IDs (DEC-xxxx/R-xxxx/reason-codes) leak into user-visible prose | **LOW** | T-005 runs `validate_doc_profile.py` + `check-user-visible-metadata.py`; US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. |
| **Decomposition drift (US-0114 angle overlap)** — US-0111/US-0112 subsections overlap confusingly with US-0114 | **LOW** | US-0113 subsections include explicit "see US-0114 for release-workflow operator docs on this feature" pointers (T-002). US-0113 = sovereign-loop angle; US-0114 = release-workflow angle. |

## Stop conditions

**stop_conditions_met=yes**:

- **No major tradeoff requires DEC** — confirmed (companion_dec=none; documentation-only; no architectural surface).
- **No feasibility unknown** — R-0101 closed all 3 discovery open questions; architecture phase resolved both carry-overs.
- **No data migration risk** — documentation-only; no schema, no data, no installer changes.

## Decision gate check

**No DECISION_GATE raised.** Architecture phase revealed no question requiring operator input. Both carry-overs resolved by tech-lead within the `plan` macro (defer h1 anchors to US-0117; lock scratchpad reference ordering = canonical mirror). No sovereign-memory digest call needed (US-0113 is documentation-only; existing digest context sufficient per R-0101).

## Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called (US-0113 documentation-only; existing digest context sufficient per R-0101). Sovereign-loop pattern identified for curator retrospective at segment close: "operator-documentation gap closing follows 5-story decomposition by functional family with angle-distinct narratives for features that span families (US-0111/US-0112 appear in both US-0113 sovereign-loop and US-0114 release-workflow with distinct angles)." No write to `mistakes.jsonl` in architecture phase.

## Consequences

- Sprint: S0113 (pending `/sprint-plan`).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.
- Framework README pair grows by umbrella + 9 subsections + scratchpad reference extension (both `its_magic/README.md` and `template/its_magic/README.md` byte-identical).
- 5 missing `architecture.md` h1 anchors deferred to US-0117.
- No new tests; no new DECs; no compose-surface changes.

## Evidence references

- `docs/product/backlog.md` — `## US-0113` block (lines 3893–3909)
- `docs/engineering/research.md` — `R-0101` (delivered, 3/3 open questions closed)
- `handoffs/po_to_tl.md` — research handoff (topmost block) + discovery handoff
- `docs/engineering/state.md` — research checkpoint (latest) + architecture checkpoint (this phase, appended)
- `handoffs/resume_brief.md` — top block updated to reflect architecture complete
- `.cursor/scratchpad.md` — sovereign-loop keys block (L388–539) — canonical source for AC-3 extension ordering
- `its_magic/README.md` — L350 (`## Commands and workflow`) umbrella target; L940 (`### Full scratchpad reference (detailed)`) extension target
- `docs/engineering/architecture.md` — h1 inventory confirmed: `# US-0108` (L120), `# US-0109` (L220), `# US-0111` (L335), `# US-0112` (L454) exist; US-0103/0104/0105/0107/0110 missing (deferred to US-0117)
- `decisions/DEC-0112.md` — highest existing DEC (next available would be DEC-0113; not used — companion_dec=none)




# US-0114 — Release & distribution operator documentation in framework README

## Overview

**US-0114** is a documentation-only story closing the operator-documentation gap for the **release & distribution** functional family — US-0111 (Release Trigger Adapters), US-0112 (Model-Catalog Example Presets), US-0041 (End-to-End Lifecycle QA), US-0062 (Installer-Owned `its_magic/` Folder for Framework Metadata). It adds an umbrella `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` narrative section under `## Commands and workflow` (L350) in `its_magic/README.md`, as a sibling to US-0113's `### Sovereign-loop era (US-0103–US-0112)` umbrella (L940). The umbrella carries 4 nested per-feature `#### US-xxxx` operator subsections ordered US-id-ascending (US-0041 → US-0062 → US-0111 → US-0112), with bidirectional `see US-0113 for sovereign-loop angle` pointers in the US-0111/US-0112 subsections. A matching `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` sub-block is appended to `### Full scratchpad reference (detailed)` (L1225) as a sibling to `### Sovereign-loop era keys` (L1242), covering **net-new** keys only (US-0062's `PROJECT_README_ENFORCE` / `FRAMEWORK_KIT_REPO`) + grouped cross-links to existing US-0054 publish controls (L541–547) and shared `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` (L1233/L1235) + cross-link pointers to US-0113's block for overlapping US-0111/US-0112 keys. The framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`) is kept byte-identical via one-way copy. No code, schema, installer, scratchpad canonical, or runbook content changes.

**Binding decision**: **companion_dec=none** (US-0114 is documentation-only; no architectural, policy, or schema surface is being changed; R-0102 § Decision-gate check confirmed no DEC required). **Research anchor**: **R-0102** (delivered 2026-07-04T02:45:40Z, 4/4 open questions closed). **Compose guards (non-negotiable)**: DO NOT amend US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0041, US-0062. **Status authority**: **OPEN** per **US-0045** (closure at `/release`).

**Fresh context marker**: `tl-US0114-architecture-20260704T043446Z-fresh`
**Orchestrator run id**: `auto-20260704-01`
**Timestamp**: 2026-07-04T04:34:46Z
**Verdict**: PASS
**Next**: `/sprint-plan`

## Companion DEC

**companion_dec=none**. Confirmed (not overriding research R-0102). Justification:

- US-0114 introduces **no** new architectural surface — no schema, no code path, no installer classification, no policy, no precedence rule, no role matrix change. It is a pure documentation backfill of the release & distribution family operator surface.
- The "operator-documentation gap closing" pattern is a recurring documentation-only pattern already established by US-0113 (sibling, `companion_dec=none` per R-0101) and BUG-0013 / BUG-0014 (both shipped with `companion_dec=none` per R-0099 / R-0100). US-0114 follows the same precedent as its US-0113 sibling.
- The 4 discovery open questions were all resolved within the `plan` macro as docs backfill decisions (R-0102 § Discovery open question resolution); none required operator input or a tradeoff record. The DC-2 deferral (US-0041/US-0062 architecture.md h1 anchors) is a triad-hygiene carry-over to US-0117, not a tradeoff requiring a DEC.
- US-0114's release-workflow angle on US-0111/US-0112 does not amend DEC-0111 / DEC-0112 — those decisions define the features; US-0114 only documents the operator angle. No DEC surface is touched.
- Reserving a DEC id would be wasteful since there is no decision surface to record.

## Approach locked

**approach_locked=A1** — Single umbrella `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` section with 4 nested `#### US-xxxx` subsections (h4 under h3 umbrella), placed under `## Commands and workflow` (L350), as a **sibling** to US-0113's `### Sovereign-loop era (US-0103–US-0112)` umbrella (L940). Recommended placement: immediately **after** the closing of the US-0113 sovereign-loop umbrella block (which ends before L1225 `### Full scratchpad reference (detailed)`), keeping the two family umbrellas visually adjacent.

### Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| **A1** | Single umbrella `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` + 4 nested `#### US-xxxx` subsections (h4 under h3) | **Locked** — preferred for navigation; consistent with US-0113 sibling approach (umbrella → per-feature detail); preserves AC-2 "per-feature operator subsections" wording naturally; keeps the 4 release & distribution features visually grouped as a functional family rather than scattered; mirrors US-0113's established pattern so the README has a uniform era/family-umbrella shape. |
| **A2** | Flat 4 `#### US-xxxx` subsections directly under `## Commands and workflow` with cross-links but no umbrella | **Rejected** — loses family grouping; scatters release & distribution features among unrelated workflow subsections; weakens AC-1 (umbrella section is an explicit AC); breaks parity with US-0113's sibling pattern; harder for operators to discover the release & distribution feature cluster. |
| **A3** | Place umbrella under `## Features (what its-magic can do)` instead of `## Commands and workflow` | **Rejected** — `## Features` already has the US-0091 catalog one-liners; AC-1 explicitly requires the umbrella under `## Commands and workflow`; narrative operator guides are workflow-shaped, not catalog-shaped. Same rationale that rejected A3 for US-0113. |

**Simplicity check**: A1 is the simplest approach that meets all 8 ACs. A2 violates AC-1. A3 violates AC-1. No simpler viable alternative exists; the alternative would be "do nothing" which fails AC-1..AC-3.

## Files to touch

| File | Action | Notes |
|---|---|---|
| `its_magic/README.md` | append `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` umbrella + 4 nested `#### US-xxxx` operator subsections under `## Commands and workflow` (L350), after the US-0113 sovereign-loop umbrella block (ends before L1225); append `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` sub-block under `### Full scratchpad reference (detailed)` (L1225), as sibling to `### Sovereign-loop era keys` (L1242) | AC-1, AC-2, AC-3, AC-7; catalog block (L63 anchor + L1235–L1243 one-liners) treated as read-only (AC-4); net-new keys only + cross-link pointers (AC-3) |
| `template/its_magic/README.md` | one-way byte-sync copy from `its_magic/README.md` after T-001/T-002/T-003 complete | AC-5 lockstep; `cmd /c fc /b its_magic\README.md template\its_magic\README.md` + `python scripts/check_intake_template_parity.py` re-run required |

**Explicitly NOT touched** (decision):

- `docs/engineering/architecture.md` — the missing `# US-0041` and `# US-0062` h1 anchors are **deferred to US-0117** (DC-2, parallel to US-0113's DC-1). See carry-over (a) below. The only architecture.md edit in this phase is the append of this `# US-0114` section (the architecture anchor for US-0114 itself).

## Files NOT to touch

- `.cursor/scratchpad.md` — canonical source of truth (never edit in docs stories; BUG-0013 precedent; US-0114 only documents existing keys).
- `template/.cursor/scratchpad.local.example.md` — canonical example (BUG-0013 ownership; US-0114 does not extend the scratchpad canonical, only documents existing keys in README).
- `docs/product/backlog.md` — status authority (closure only at `/release`). **Note:** working-tree copy has 185 stray `0xa7` bytes (encoding regression flagged in R-0102) — research phase is read-only; orchestrator to restore encoding hygiene before execute so AC-4 can be re-verified post-execute.
- `docs/engineering/runbook.md` — AC-7 cross-links only; **no new runbook content** (AC-7 forbids duplication). All 4 runbook anchors already exist (US-0041 → `## Lifecycle QA matrix (US-0041)` L2522; US-0062 → `## Project README coverage validation (US-0097 / DEC-0083)` L171 with explanatory note; US-0111/US-0112 → existing anchors per R-0102).
- `docs/developer/README.md` — separate audience surface owned by US-0097 (project README parity) compose guard; AC-6 is a validator gate, not an edit mandate.
- `docs/engineering/architecture.md` (other than this `# US-0114` append) — missing `# US-0041` / `# US-0062` h1 anchors deferred to US-0117 (DC-2). **Do NOT add DC-2 anchors here.**
- `installer.py`, `installer.ps1`, `installer.sh` — no installer changes (US-0008/US-0018/US-0057/US-0075 + US-0062/DEC-0045 + US-0041/BUG-0003 compose guards).
- All scripts (`scripts/validate_readme_feature_coverage.py`, `scripts/check_intake_template_parity.py`, `scripts/validate_doc_profile.py`, `scripts/check-user-visible-metadata.py`, etc.) — validators are read-only gates, not edit targets.
- All release & distribution scripts and Python/PowerShell/Shell files — US-0111/US-0112/US-0041/US-0062 features are **documented only**, not amended.
- All test files (`tests/scratchpad_example_parity_test.py`, etc.) — read-only regression gates (AC-8).

## Sprint seeds (T-001..T-006)

**6 task seeds** (≤ `SPRINT_MAX_TASKS=12` — `SPRINT_AUTO_SPLIT` not triggered; mirror US-0113 sibling pattern).

| ID | Title | AC | Tranche |
|----|-------|----|:---------|:---------|
| **T-001** | Add `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` umbrella section under `## Commands and workflow` (L350), placed immediately after the US-0113 sovereign-loop umbrella block (ends before L1225 `### Full scratchpad reference`). Content: default-off posture callout, 4-step recommended enable order (US-0062 → US-0041 → US-0112 → US-0111), runbook pointer line, zero-overhead-when-off contract paragraph. | AC-1 | A |
| **T-002** | Add 4 per-feature `#### US-xxxx` operator subsections nested under the umbrella, ordered US-id-ascending (US-0041 → US-0062 → US-0111 → US-0112). Each subsection: 1–3 sentence narrative (release-workflow angle for US-0111/US-0112), master enable flag + related keys with defaults, zero-overhead-when-off wording, runbook cross-link (existing anchor only — no duplication). US-0062 subsection cross-links to `## Project README coverage validation (US-0097 / DEC-0083)` (L171) with explanatory note "(US-0062 installer ownership boundary amended by US-0097 / DEC-0083; original DEC-0045 referenced from `docs/engineering/decisions.md` § DEC-0045)". US-0041 subsection cross-links to `## Lifecycle QA matrix (US-0041)` (L2522). US-0111/US-0112 subsections include bidirectional "see US-0113 for sovereign-loop angle" pointers (mirror US-0113's "see US-0114" pointer convention per R-0101). | AC-2, AC-7 | A |
| **T-003** | Extend `### Full scratchpad reference (detailed)` (L1225) with `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` sub-block, as sibling to `### Sovereign-loop era keys` (L1242). Net-new key rows ONLY (US-0062's `PROJECT_README_ENFORCE` / `FRAMEWORK_KIT_REPO` with defaults + flip guidance) + grouped cross-links to existing US-0054 publish controls (`RELEASE_PUBLISH_MODE` / `RELEASE_TARGETS_FILE` / `RELEASE_TARGETS_DEFAULT` — L541–547) and shared `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` (L1233/L1235) + cross-link pointers to US-0113's `### Sovereign-loop era keys` block for overlapping US-0111/US-0112 keys (`RELEASE_TRIGGER_SOURCE` / `RELEASE_TRIGGER_TIMEOUT_SEC` / `RELEASE_TRIGGER_FALLBACK_TO_LOCAL` / `DELIVERY_MODE` / `TOKEN_PROFILE` / `ID_NAMESPACE_BOOTSTRAP` / `MODEL_TIER`). No duplicate key rows. Default-off / zero-overhead-when-off wording per AC-3. | AC-3 | A |
| **T-004** | Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md` (one-way copy after T-001/T-002/T-003 complete). Re-run `cmd /c fc /b its_magic\README.md template\its_magic\README.md` (expect no differences) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK]`). | AC-5 | B |
| **T-005** | Run validators (AC-4, AC-6) and fix any drift. `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → expect `[README_FEATURE_COVERAGE_VALIDATE_OK]` with `coverage_missing=["US-0117"]` unchanged (DC-1 + DC-2 out-of-scope). Note: working-tree `docs/product/backlog.md` encoding hygiene (185 stray `0xa7` bytes) must be restored by orchestrator before this gate can re-pass post-execute. `python scripts/validate_doc_profile.py` + `python scripts/check-user-visible-metadata.py` → expect PASS. Fix any narrative prose that leaks internal IDs (DEC-xxxx/R-xxxx/reason-codes) into user-visible sentences; US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. | AC-4, AC-6 | B |
| **T-006** | Run regression tests (AC-8) and confirm green. `python -m pytest tests/scratchpad_example_parity_test.py -q` → expect 4 passed (US-0114 does NOT modify `.cursor/scratchpad.md` or `template/.cursor/scratchpad.local.example.md`). Confirm no test weakenings — if a test fails, the prose is wrong, not the test. | AC-8 | B |

### AC → task surjective map

| AC | Tasks |
|----|-------|
| AC-1 Umbrella section | T-001 |
| AC-2 Per-feature operator subsections | T-002 |
| AC-3 Full scratchpad reference extension | T-003 |
| AC-4 Coverage preserved | T-005 |
| AC-5 Framework README parity | T-004 |
| AC-6 Audience + metadata hygiene | T-005 |
| AC-7 Runbook cross-links per feature | T-002 |
| AC-8 Regression tests | T-006 |

**Surjectivity check**: AC-1..AC-8 all covered. **Total**: 6 task seeds ≤ `SPRINT_MAX_TASKS=12` — `SPRINT_AUTO_SPLIT` not triggered.

## Test markers (existing — no new tests proposed)

| Marker | File | AC covered | Notes |
|--------|------|------------|-------|
| `test_bug0013_parity_check` + 3 companions | `tests/scratchpad_example_parity_test.py` | AC-5 (indirect), AC-8 | Confirms `.cursor/scratchpad.md` ↔ `template/.cursor/scratchpad.local.example.md` parity; US-0114 does not touch either file, so tests remain green by construction. |
| `validate_readme_feature_coverage.py --enforce` | `scripts/validate_readme_feature_coverage.py` | AC-4 | Coverage gate; `coverage_missing=["US-0117"]` must remain unchanged (DC-1 + DC-2 out-of-scope). |
| `check_intake_template_parity.py` | `scripts/check_intake_template_parity.py` | AC-5 | Framework README byte-parity gate. |
| `validate_doc_profile.py` | `scripts/validate_doc_profile.py` | AC-6 | Audience profile gate. |
| `check-user-visible-metadata.py` | `scripts/check-user-visible-metadata.py` | AC-6 | Metadata hygiene gate. |

**No new tests proposed.** R-0102 confirmed no test weakenings; AC-8 is satisfied by existing tests remaining green. Adding new tests would violate the "no test weakenings" spirit (US-0114 is documentation-only; tests are read-only gates).

## Compose guards (non-negotiable — all UNCHANGED)

| Story | Compose rule |
|-------|--------------|
| **US-0091** | Feature coverage catalog anchor `<!-- readme-feature-coverage-catalog -->` (L63) + one-liners UNCHANGED — US-0114 appends narrative sections outside the catalog block. |
| **US-0097** | Project README parity surface UNCHANGED — US-0114 touches framework README pair only, not project README. (US-0062 cross-links here.) |
| **US-0017** | Framework README parity contract UNCHANGED — US-0114 preserves byte-parity via T-004 lockstep. |
| **US-0040** | Per-sprint release notes semantics UNCHANGED. |
| **US-0100** | Semantic changelog UNCHANGED. |
| **US-0101** | Catalog schema (DEC-0086) UNCHANGED. |
| **US-0102** | Role catalog precedence (DEC-0087) UNCHANGED. |
| **US-0103** | AI Decision Ledger schema/semantics UNCHANGED — documented only. |
| **US-0104** | Cross-Model Adversarial Critic schema/semantics UNCHANGED — documented only. |
| **US-0105** | Sovereign Memory schema/semantics UNCHANGED — documented only. |
| **US-0107** | Sovereign Loop Mode schema/semantics UNCHANGED — documented only. |
| **US-0108** | Parallel Instance Arbitrage schema/semantics UNCHANGED — documented only. |
| **US-0109** | Self-Healing Deploy Loop schema/semantics UNCHANGED — documented only. |
| **US-0110** | Goal-Based Convergence schema/semantics UNCHANGED — documented only. |
| **US-0111** | Release Trigger Adapters schema/semantics UNCHANGED — documented only (release-workflow angle owned by US-0114; sovereign-loop angle shipped in US-0113). |
| **US-0112** | Model-Catalog Example Presets schema/semantics UNCHANGED — documented only (release-workflow angle owned by US-0114; sovereign-loop angle shipped in US-0113). |
| **US-0041** | End-to-End Lifecycle QA schema/semantics UNCHANGED — documented only (release-workflow angle). |
| **US-0062** | Installer-Owned `its_magic/` folder boundary (DEC-0045, amended by DEC-0083/US-0097) UNCHANGED — documented only. |

**18 guards UNCHANGED.** US-0114 lives entirely outside the compose surface (documentation-only; no code/scripts/installers/scratchpad canonical touched).

## Carry-overs from research (resolution)

### (a) Missing `# US-0041` and `# US-0062` h1 anchors in `architecture.md` (DC-2)

**Decision: DEFER to US-0117** (phase & role governance family, which inherits DC-1 from US-0113 + DC-2 from US-0114 as architecture.md triad hygiene closure).

**Justification**:

- AC-7 only requires **runbook** cross-links, which exist for all 4 features (R-0102 § Per-feature sub-findings: US-0041 → L2522; US-0062 → L171 via US-0097/DEC-0083; US-0111/US-0112 → existing anchors). The missing `architecture.md` h1 anchors are NOT a US-0114 AC.
- US-0114 is scoped as a **framework README** documentation story (`its_magic/README.md` pair). The `architecture.md` h1 anchors are an internal engineering-docs surface, not an operator-facing README surface. Mixing the two would blur the story's vertical-slice boundary.
- US-0117 (phase & role governance family) is the natural owner: it already inherits DC-1 (5 missing h1 anchors for US-0103/0104/0105/0107/0110) from US-0113, and adding DC-2 (2 missing h1 anchors for US-0041/US-0062) fits its architecture-doc triad hygiene closure scope cleanly.
- Deferring keeps US-0114 at 6 task seeds (well under `SPRINT_MAX_TASKS=12`); adding T-007 would cross the story's vertical-slice boundary.
- Structurally parallel to US-0113's DC-1 deferral rationale (R-0101).

**Deferral note for orchestrator**: This is a **DC-2 deferral candidate** for the orchestrator's segment-boundary advance hook. **DO NOT append to `handoffs/sovereign_deferrals.jsonl` in architecture phase** (per instructions). Note for orchestrator: when US-0117 enters `plan` macro, its discovery should narrow-read this section and US-0113's carry-over (a), and add the 7 missing h1 anchors (5 from DC-1 + 2 from DC-2) as task seeds. Anchor format: `# US-xxxx — <feature title>` (matching existing `# US-0108`, `# US-0109`, `# US-0111`, `# US-0112` format).

### (b) Scratchpad reference extension — net-new keys + cross-link pointers only

**Decision: LOCK net-new keys + cross-link pointers** (per R-0102 open question #1 resolution).

**Justification**:

- US-0111's `RELEASE_TRIGGER_SOURCE` / `RELEASE_TRIGGER_TIMEOUT_SEC` / `RELEASE_TRIGGER_FALLBACK_TO_LOCAL` and US-0112's `DELIVERY_MODE` / `TOKEN_PROFILE` / `ID_NAMESPACE_BOOTSTRAP` / `MODEL_TIER` are **already present** in `its_magic/README.md` L1338–1358 inside `### Sovereign-loop era keys (US-0103–US-0112)` (L1242, shipped by US-0113/S0113).
- Re-documenting those 7 keys in a parallel `### Release & distribution keys` sub-block would (a) duplicate 7 keys, (b) risk byte-instability / divergence if defaults or wording drift between the two sub-blocks, and (c) violate US-0113's byte-stability contract on its sovereign-loop keys block.
- The net-new-only + cross-link-pointer approach preserves US-0113's byte-stability, avoids duplication, and gives operators a single canonical location per key (US-0113's block for US-0111/US-0112 overlap keys; US-0114's block for US-0062 net-new keys + grouped cross-links to US-0054/AUTO_INSTALL_DEPS/AUTO_RELEASE_NOTES).

## Risks (finalized)

| Risk | Severity | Mitigation |
|------|----------|------------|
| **AC-3 overlap divergence** — US-0111/US-0112 overlap keys re-documented in US-0114's reference sub-block, drifting from US-0113's block | **MEDIUM→LOW** | LOCK net-new keys + cross-link pointers only (carry-over (b)); US-0114's `### Release & distribution keys` sub-block covers ONLY net-new keys (US-0062's `PROJECT_README_ENFORCE` / `FRAMEWORK_KIT_REPO`) + grouped cross-links to existing US-0054 publish controls + shared `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` + cross-link pointers to US-0113's block for overlapping US-0111/US-0112 keys. No duplicate key rows. US-0113's `### Sovereign-loop era keys` block byte-stability preserved. T-003 enforces; QA re-verifies. |
| **AC-5 parity lockstep** — `its_magic/README.md` edited but `template/its_magic/README.md` not synced (or vice versa) | **MEDIUM** | T-004 mandates one-way copy `its_magic/README.md` → `template/its_magic/README.md` after T-001/T-002/T-003 complete. Execute-phase must run `cmd /c fc /b its_magic\README.md template\its_magic\README.md` (expect no differences) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK]`). QA must re-verify both gates. Same mitigation as US-0113. |
| **AC-7 US-0062 anchor** — US-0062 has no dedicated runbook `## US-0062` h2 anchor; cross-link must target an existing anchor | **MEDIUM→LOW** | Cross-link to `## Project README coverage validation (US-0097 / DEC-0083)` (L171) with explanatory note "(US-0062 installer ownership boundary amended by US-0097 / DEC-0083; original DEC-0045 referenced from `docs/engineering/decisions.md` § DEC-0045)". This is the canonical active-anchor surface per DEC-0045 (declared) + DEC-0083 (amended). T-002 enforces; QA re-verifies. |
| **AC-8 regression tests** — coverage parity contract tests weakened or failing | **LOW–MEDIUM** | US-0114 is documentation-only; **forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` in execute-phase task list. If a test fails, the prose is wrong, not the test — fix prose, never relax test. T-006 confirms green. |
| **AC-4 coverage drift** — catalog block accidentally reflowed OR working-tree backlog.md encoding regression blocks validator | **LOW** (catalog) / **MEDIUM** (encoding) | T-005 runs `validate_readme_feature_coverage.py --enforce`; `coverage_missing=["US-0117"]` must remain unchanged. Catalog block treated as read-only. **Encoding hygiene:** working-tree `docs/product/backlog.md` has 185 stray `0xa7` bytes (Windows-1252 corruption from untracked scripts per R-0102) — orchestrator must restore encoding hygiene before execute so AC-4 can be re-verified post-execute. Research phase is read-only on backlog.md. |
| **AC-6 metadata leakage** — internal IDs (DEC-xxxx/R-xxxx/reason-codes) leak into user-visible prose | **LOW** | T-005 runs `validate_doc_profile.py` + `check-user-visible-metadata.py`; US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. US-0062's explanatory note is the only place a DEC id appears in prose — kept inside a parenthetical cross-link, not a user-visible sentence. |
| **Decomposition drift (US-0113 angle overlap)** — US-0111/US-0112 US-0114 subsections overlap confusingly with US-0113's subsections | **LOW** | US-0114 subsections include explicit "see US-0113 for sovereign-loop angle" pointers (T-002). US-0113 = sovereign-loop angle (shipped S0113); US-0114 = release-workflow angle. Bidirectional pointers already in US-0113's subsections (per R-0101). |

## Stop conditions

**stop_conditions_met=yes**:

- **No major tradeoff requires DEC** — confirmed (companion_dec=none; documentation-only; no architectural surface; R-0102 § Decision-gate check confirmed no DEC required).
- **No feasibility unknown** — R-0102 closed all 4 discovery open questions; architecture phase resolved both carry-overs (DC-2 defer to US-0117; scratchpad reference extension net-new + cross-link pointers only).
- **No data migration risk** — documentation-only; no schema, no data, no installer changes.

## Decision gate check

**No DECISION_GATE raised.** Architecture phase revealed no question requiring operator input. Both carry-overs resolved by tech-lead within the `plan` macro (defer DC-2 h1 anchors to US-0117; lock scratchpad reference extension = net-new keys + cross-link pointers). No sovereign-memory digest call needed (US-0114 documentation-only; existing digest context sufficient per R-0102).

## Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called (US-0114 documentation-only; existing digest context sufficient per R-0102). Sovereign-loop pattern identified for curator retrospective at segment close: "release & distribution family operator documentation follows US-0113's umbrella + per-feature subsection pattern, with net-new-keys-only + cross-link-pointer scratchpad reference extension to preserve byte-stability on the sibling era block." No write to `mistakes.jsonl` in architecture phase.

## Consequences

- Sprint: S0114 (pending `/sprint-plan`).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.
- Framework README pair grows by umbrella + 4 subsections + scratchpad reference extension (both `its_magic/README.md` and `template/its_magic/README.md` byte-identical).
- 2 missing `architecture.md` h1 anchors (`# US-0041`, `# US-0062`) deferred to US-0117 (DC-2, parallel to US-0113's DC-1 — 5 anchors).
- No new tests; no new DECs; no compose-surface changes.

## Evidence references

- `docs/product/backlog.md` — `## US-0114` block (lines 3911–3927)
- `docs/engineering/research.md` — `R-0102` (delivered 2026-07-04T02:45:40Z, 4/4 open questions closed)
- `handoffs/po_to_tl.md` — research handoff (topmost block) + discovery handoff
- `docs/engineering/state.md` — research checkpoint (latest) + architecture checkpoint (this phase, appended)
- `handoffs/resume_brief.md` — top block updated to reflect architecture complete
- `.cursor/scratchpad.md` — release & distribution keys (L200–209 RELEASE_PUBLISH_MODE/RELEASE_TARGETS_*, L258–267 PROJECT_README_ENFORCE/FRAMEWORK_KIT_REPO, L529–539 RELEASE_TRIGGER_*, L66–67 AUTO_INSTALL_DEPS/AUTO_RELEASE_NOTES, L181–186 DELIVERY_MODE/TOKEN_PROFILE/ID_NAMESPACE_BOOTSTRAP) — canonical source for AC-3 extension (net-new + cross-links)
- `its_magic/README.md` — L350 (`## Commands and workflow`) umbrella target; L940 (`### Sovereign-loop era` US-0113 sibling umbrella); L1225 (`### Full scratchpad reference (detailed)`) extension target; L1242 (`### Sovereign-loop era keys` US-0113 sibling block — byte-stability preserved)
- `docs/engineering/architecture.md` — h1 inventory confirmed: `# US-0111` (L335), `# US-0112` (L454), `# US-0113` (L717) exist; `# US-0041` and `# US-0062` missing (deferred to US-0117 as DC-2)
- `docs/engineering/decisions.md` — DEC-0045 (US-0062 installer-owned boundary), DEC-0083 (US-0097 amends DEC-0045), DEC-0111 (US-0111), DEC-0112 (US-0112) — referenced, not amended



## US-0115 — Integration & observability operator documentation in framework README

### Overview

**US-0115** is a documentation-only story closing the operator-documentation gap for the **integration & observability** functional family — US-0034 (Cross-repo compatibility observability), US-0084 (Codebase map freshness gate), US-0086 (Handoff hygiene validator), US-0093 (Scratchpad drift detector), US-0096 (Active context handoff), US-0101 (Model tier resolution), US-0102 (Role-based model catalog). It adds an umbrella `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102) umbrella section` under `## Commands and workflow` (L350) in `its_magic/README.md`, as a sibling to US-0113's `### Sovereign-loop era (US-0103–US-0112) umbrella section` (L940) and US-0114's `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112) umbrella section` (L1225). The umbrella carries 7 nested per-feature `#### US-xxxx` operator subsections ordered US-id-ascending (US-0034 → US-0084 → US-0086 → US-0093 → US-0096 → US-0101 → US-0102), with bidirectional `see US-0114 for installer-payload angle` pointers in the US-0101/US-0102 subsections (angle-distinct narrative contract — US-0115 owns resolver mechanics + role catalog; US-0114 owns installer payload US-0112 presets). A matching `### Integration & observability keys (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` sub-block is appended to `### Full scratchpad reference (detailed)` (L1410) as a sibling to `### Sovereign-loop era keys (US-0103–US-0112)` (L1427) and `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` (L1551), covering **net-new** keys only (US-0034 `CROSS_REPO_OBSERVABILITY` family, US-0096 `LEAN_MEMORY_*` family + `AUTO_DELIVERY_ROUTING`, US-0101 5 resolver keys, US-0102 `MODEL_SLUG_<PHASE_ID>`) + cross-link pointer to US-0114's block for the `DELIVERY_MODE` overlap + grouped cross-link to the main reference list above L1410 for US-0086's `REMOTE_EXECUTION` family + reason-code-only entries for US-0084 (`INSTALL_MANIFEST_ERROR`) / US-0093 (`SCRATCHPAD_HEADER_DRIFT` / `BACKLOG_STATUS_DRIFT`). The framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`) is kept byte-identical via one-way copy. No code, schema, installer, scratchpad canonical, or runbook content changes.

**Binding decision**: **companion_dec=none** (US-0115 is documentation-only; no architectural, policy, or schema surface is being changed; R-0103 § Decision-gate check confirmed no DEC required — mirrors US-0113 / US-0114 sibling precedent). **Research anchor**: **R-0103** (delivered 2026-07-04T07:53:00Z, 6/6 open questions closed). **Compose guards (non-negotiable, 23 — UNCHANGED, cumulative across all prior stories)**: DO NOT amend US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062. **Status authority**: **OPEN** per **US-0045** (closure at `/release`).

**Fresh context marker**: `tl-US0115-architecture-20260704T080200Z-fresh`
**Orchestrator run id**: `auto-20260704-01`
**Timestamp**: 2026-07-04T08:02:00Z
**Verdict**: PASS
**Next**: `/sprint-plan`

### Companion DEC

**companion_dec = none**. US-0115 is documentation-only (mirrors US-0113 / US-0114 sibling precedent). No architectural, policy, or schema surface is being changed. Grep for `^## DEC-` in `docs/engineering/decisions.md` confirmed no US-0115 companion DEC is required and none was proposed in R-0103 § Decision-gate check. The DC-3 deferral (7 missing `# US-xxxx` h1 anchors) is a triad-hygiene carry-over to US-0117, not a tradeoff requiring a DEC.

### Approach locked — A1

**A1: Single `### Integration & observability` umbrella + 7 nested `#### US-xxxx` subsections (h4 under h3 umbrella), sibling to US-0113's `### Sovereign-loop era` (L940) and US-0114's `### Release & distribution` (L1225) umbrellas, inserted immediately after the closing of US-0114's umbrella block (before L1410 `### Full scratchpad reference (detailed)`).**

**Justification**:
- **Consistency with prior stories** — US-0113 established the umbrella+subsection shape for the sovereign-loop family; US-0114 mirrored it for the release & distribution family; US-0115 mirrors it for the integration & observability family. Three sibling umbrellas in release order (US-0113 → US-0114 → US-0115) under `## Commands and workflow` form a clean triad.
- **Design challenge: alternatives considered.**
  - **A2 (rejected):** 7 separate top-level `### US-xxxx` h3 sections scattered under `## Commands and workflow` rather than grouped under an umbrella. Rejected: breaks the family-grouping precedent set by US-0113/US-0114, hurts operator discoverability (no single entry point for the integration & observability family), and complicates the AC-1 acceptance criterion which explicitly requires an umbrella section.
  - **A3 (rejected):** Reuse US-0034's existing L585 `### Optional cross-repo observability (US-0034)` h3 as the umbrella and nest the other 6 features under it. Rejected: US-0034 is one feature among seven; elevating it to umbrella-holder conflates a feature section with a family section, breaks byte-stability of the pre-US-0115 L585 block, and breaks the family-parity contract (US-0113/US-0114 each have a dedicated umbrella header).
  - **A1 is the only viable option** that satisfies AC-1 (umbrella section), preserves US-0113/US-0114 sibling consistency, and respects byte-stability of prior released blocks. Lock A1.

### Files to touch

- `its_magic/README.md` — APPEND umbrella `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102) umbrella section` (after US-0114 umbrella close, before L1410) + 7 nested `#### US-xxxx` operator subsections (US-0034 → US-0084 → US-0086 → US-0093 → US-0096 → US-0101 → US-0102) + `### Integration & observability keys` sub-block under `### Full scratchpad reference (detailed)` (after US-0114's `### Release & distribution keys` block at L1551) covering net-new keys + cross-link pointers + reason-code-only entries.
- `template/its_magic/README.md` — byte-identical sync via one-way copy from `its_magic/README.md` (AC-5).

### Files NOT to touch

- `.cursor/scratchpad.md` — canonical scratchpad; US-0115 documents keys in README, never edits the canonical source.
- `docs/product/backlog.md` — status authority (US-0045); encoding hygiene prerequisite flagged separately to orchestrator.
- `docs/engineering/runbook.md` — AC-7 cross-links only (all 7 anchors pre-exist); no new runbook content.
- `docs/developer/README.md` — US-0097 compose guard.
- `docs/engineering/architecture.md` — other than this US-0115 anchor append; DC-3 (7 missing h1 anchors) deferred to US-0117.
- `installer.py` / `installer.ps1` / `installer.sh`, `scripts/*`, any test file — out of scope (documentation-only story).
- **Do NOT modify US-0113's `### Sovereign-loop era` / `### Sovereign-loop era keys` blocks (L940 / L1427) or US-0114's `### Release & distribution` / `### Release & distribution keys` blocks (L1225 / L1551)** in `its_magic/README.md` — byte-stability contract (both already released in S0113 / S0114). US-0115 adds cross-link pointers to these blocks from its own net-new block; it never edits them. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1551 range (no removals/modifications to US-0113's L1427 or US-0114's L1551 blocks).

### Sprint seeds (T-001..T-006)

6 tasks within `SPRINT_MAX_TASKS=12` (mirror US-0113 / US-0114 sibling pattern; `SPRINT_AUTO_SPLIT` not triggered):

| Task | Description | ACs covered |
|------|-------------|-------------|
| **T-001** | Add umbrella `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102) umbrella section` under `## Commands and workflow` (after US-0114 umbrella close, before L1410). Default-off framing for optional features (US-0034 / US-0096 / US-0101 / US-0102) + always-on framing for publish/QA guards (US-0084 / US-0086 / US-0093). 7-step enable order (US-0034 → US-0096 → US-0101 → US-0102 → US-0084 → US-0086 → US-0093) + runbook pointer line. | AC-1 |
| **T-002** | Add 7 per-feature `#### US-xxxx` operator subsections under the umbrella, ordered US-id-ascending (US-0034 → US-0084 → US-0086 → US-0093 → US-0096 → US-0101 → US-0102). US-0034 = cross-link only to existing L585 README section (byte-stability) + runbook cross-link to L1167. US-0096 = **net-new narrative** (R-0103 CORRECTION: no pre-existing L591 README section — L591 is a runbook line) + runbook cross-link to L591. US-0101/US-0102 = bidirectional "see US-0114 for installer-payload angle" pointers (angle-distinct narrative contract). US-0084/US-0086/US-0093 = reason codes + runbook cross-links (no scratchpad key blocks). Runbook cross-links per feature: US-0034 → L1167 h2; US-0084 → L1441/L1459 h3; US-0086 → L1398/L1471 h3; US-0093 → L1999 h3 (parent h2 = US-0065 runtime QA autopilot contract L1486); US-0096 → L591 h3; US-0101 → L653 h2; US-0102 → L771 h2. | AC-2, AC-7 |
| **T-003** | Add `### Integration & observability keys (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` sub-block under `### Full scratchpad reference (detailed)` (after US-0114's `### Release & distribution keys` block L1551). Net-new key rows only: US-0034 `CROSS_REPO_OBSERVABILITY` / `COMPATIBILITY_GATE_ON_CRITICAL` / `COMPATIBILITY_SOURCES`; US-0096 `LEAN_MEMORY_READ` / `LEAN_MEMORY_WRITE` / `LEAN_COLD_READ_MAX_SECTIONS` / `LEAN_STATE_INDEX_ROWS` / `AUTO_DELIVERY_ROUTING`; US-0101 `MODEL_TIER_DEFAULT` / `MODEL_CATALOG` / `MODEL_RESOLVE` / `MODEL_FALLBACK` / `MODEL_PROVIDER_MODE`; US-0102 `MODEL_SLUG_<PHASE_ID>` (with composition-on-US-0101 note). Cross-link pointers: `DELIVERY_MODE` → US-0114's block (US-0114 owns that row); US-0086 `REMOTE_EXECUTION` family → grouped cross-link to main reference list above L1410 (mirrors US-0114's `AUTO_INSTALL_DEPS`/`AUTO_RELEASE_NOTES` grouped cross-link pattern). Reason-code-only entries for US-0084 (`INSTALL_MANIFEST_ERROR`) / US-0093 (`SCRATCHPAD_HEADER_DRIFT` / `BACKLOG_STATUS_DRIFT`) + runbook cross-links. No duplicate key rows. Byte-stability of US-0113's L1427 + US-0114's L1551 blocks preserved (net-new-keys-only + cross-link-pointer shape). | AC-3 |
| **T-004** | Sync `template/its_magic/README.md` byte-identical via one-way copy from `its_magic/README.md`. Re-run `python -c "a=open(r'its_magic/README.md','rb').read(); b=open(r'template/its_magic/README.md','rb').read(); print('PARITY_OK' if a==b else 'PARITY_DIFF')"` (expect `PARITY_OK`) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`). | AC-5 |
| **T-005** | Run validators: `python scripts/validate_readme_feature_coverage.py --enforce` (expect `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0 — catalog block read-only) + `python scripts/validate_doc_profile.py` (expect `[DOC_PROFILE_VALIDATE_OK]`) + `python scripts/check-user-visible-metadata.py` (expect exit 0; US-IDs only in parenthetical catalog tags). | AC-4, AC-6 |
| **T-006** | Run regression tests: `python -m pytest tests/scratchpad_example_parity_test.py -q` (expect 4/4 PASS). **Forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` — if a test fails, the prose is wrong, not the test (fix prose, never relax test). | AC-8 |

**Execution order**: T-001 (umbrella) → T-002 (7 subsections) → T-003 (scratchpad ref extension) → T-004 (template byte-sync) → T-005 (validators) → T-006 (regression tests). Acyclic, mirrors US-0113/US-0114.

### Test markers

Same 5 as US-0113 / US-0114 (no new tests proposed):

1. `tests/scratchpad_example_parity_test.py` — 4 markers (AC-5 indirect via scratchpad canonical parity, AC-8).
2. `scripts/validate_readme_feature_coverage.py --enforce` — AC-4.
3. `scripts/check_intake_template_parity.py` — AC-5.
4. `scripts/validate_doc_profile.py` — AC-6.
5. `scripts/check-user-visible-metadata.py` — AC-6.

### Compose guards (UNCHANGED — 23 guards, cumulative)

US-0115 is documentation-only and lives entirely outside the compose surface. The 23 compose guards (cumulative across all prior stories — US-0113 carried 18, US-0114 carried 18, US-0115 adds 5 family-internal guards to the documentation-only list for completeness: US-0034, US-0084, US-0086, US-0093, US-0096) remain UNCHANGED:

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062.

### Stop conditions

**stop_conditions_met=yes**:

- **No DEC required** — confirmed (companion_dec=none; documentation-only; mirrors US-0113 / US-0114 sibling precedent; R-0103 § Decision-gate check confirmed no DEC candidate).
- **No feasibility unknown** — R-0103 closed all 6 discovery open questions (split resolution on US-0034/US-0096 narrative shape; net-new keys + cross-link pointers LOCKED for AC-3; reason-code-only entries for US-0084/US-0093; US-0086 grouped cross-link; US-0093 runbook anchor h-level CONFIRMED = h3; DC-3 deferred to US-0117).
- **No data migration risk** — documentation-only; no schema, no data, no installer, no scratchpad canonical changes.

### DC-3 resolution (deferred to US-0117)

**DC-3**: 7 missing `# US-xxxx` h1 anchors in active `docs/engineering/architecture.md` for the US-0115 family — `# US-0034`, `# US-0084`, `# US-0086`, `# US-0093`, `# US-0096`, `# US-0101`, `# US-0102`. Grep for `^# US-(0034|0084|0086|0093|0096|0101|0102)` in `docs/engineering/architecture.md` returned no matches (confirmed in R-0103 § Discovery open question #6 resolution). Not a US-0115 blocker — AC-7 is satisfiable via runbook cross-links (all 7 features have existing verified runbook anchors). US-0117 (Phase & role governance family) inherits DC-1 (5 anchors from US-0113: US-0103/0104/0105/0107/0110) + DC-2 (2 anchors from US-0114: US-0041/US-0062) + DC-3 (7 anchors from US-0115) = **14 total missing h1 anchors** as architecture.md triad hygiene closure.

**Deferral note for orchestrator**: This is a **deferral candidate** for the orchestrator's segment-boundary advance hook. **DO NOT append to `handoffs/sovereign_deferrals.jsonl` in architecture phase** (per instructions — segment-boundary advance hook handles it, not phase boundaries). `/architecture` documents the deferral in this findings block; does NOT add the h1 anchors. When US-0117 enters `plan` macro, its discovery should narrow-read this section and add the 7 missing h1 anchors as a task seed. Anchor format to use at that time: `# US-xxxx — <feature title>` (matching existing `# US-0108`, `# US-0109`, `# US-0111`, `# US-0112`, `# US-0113`, `# US-0114` format).

### Risks (finalized)

| Risk | Severity | Mitigation |
|------|----------|------------|
| **AC-3 byte-stability (3rd-story cumulative surface)** — US-0115 is the third story to extend `### Full scratchpad reference`; cumulative surface now covers 2 prior released blocks (US-0113 L1427 + US-0114 L1551). Risk of accidentally editing a prior released block. | **MEDIUM** | Net-new-keys-only + cross-link-pointer shape LOCKED in `/architecture` (T-003). Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1551 range (no removals/modifications to US-0113's L1427 or US-0114's L1551 blocks). QA re-verifies. Mirrors S0114 retrospective pattern. |
| **AC-5 parity lockstep** — `its_magic/README.md` edited but `template/its_magic/README.md` not synced (or vice versa). | **MEDIUM** | T-004 mandates one-way copy `its_magic/README.md` → `template/its_magic/README.md` after T-001/T-002/T-003 complete. Execute-phase must re-run byte-parity check + `check_intake_template_parity.py`. QA re-verifies both gates. |
| **AC-2 US-0096 net-new narrative (R-0103 CORRECTION)** — Discovery handoff claimed "L591 `### Delivery modes` in README"; R-0103 confirmed L591 is a **runbook** line, not a README line. No pre-existing US-0096 README narrative section. | **LOW–MEDIUM** | `#### US-0096` subsection is net-new narrative (no byte-stability risk — no prior README section to preserve) + runbook cross-link to L591. Architecture locks the correction; execute-phase T-002 follows it. |
| **AC-2 US-0101/US-0102 angle overlap with US-0114** — US-0101/US-0102 model-tier-resolution + role-catalog angle owned by US-0115 vs US-0114's US-0112 installer-payload angle. | **MEDIUM→LOW** | Bidirectional "see US-0114 for installer-payload angle" pointers in US-0101/US-0102 subsections (T-002). US-0115 owns resolver mechanics + role catalog (DEC-0086 / DEC-0087); US-0114 owns installer payload (US-0112 presets). Angle boundary explicit. |
| **AC-3 `DELIVERY_MODE` overlap** — US-0114's `### Release & distribution keys` block (L1551) references `DELIVERY_MODE` from the release-workflow angle; US-0096 is in US-0115's family. | **MEDIUM→LOW** | Cross-link pointer to US-0114's block; US-0115 does NOT re-document `DELIVERY_MODE` defaults; US-0114 owns that row. |
| **AC-7 runbook cross-links** — 7 features, all anchors pre-exist (unlike US-0114's US-0062 gap which required an explanatory note). US-0093 h-level CONFIRMED = h3 (parent h2 = US-0065 runtime QA autopilot contract L1486). | **LOW** | All 7 anchors verified in R-0103: US-0034 L1167 h2; US-0084 L1441/L1459 h3; US-0086 L1398/L1471 h3; US-0093 L1999 h3; US-0096 L591 h3; US-0101 L653 h2; US-0102 L771 h2. |
| **AC-4 encoding hygiene prerequisite (carried from US-0114)** — Working-tree `docs/product/backlog.md` has 185 stray `0xa7` (§) bytes per R-0102. Orchestrator must restore encoding hygiene before execute so AC-4 can be re-verified post-execute. | **MEDIUM (carried)** | `/architecture` makes no backlog.md edits. Flag to orchestrator: restore backlog.md encoding hygiene before execute. NOT a US-0115 blocker (research was read-only on backlog.md; architecture is read-only on backlog.md). |
| **AC-8 regression tests** — coverage parity contract tests weakened or failing. | **LOW–MEDIUM** | US-0115 is documentation-only; **forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` in execute-phase task list. If a test fails, fix prose, never relax test. T-006 confirms green. |
| **AC-1 umbrella placement** — Risk of inserting the umbrella inside US-0114's block rather than after it. | **LOW** | Insert after US-0114 umbrella close (before L1410 `### Full scratchpad reference`), NOT inside it. Mirrors US-0114-after-US-0113 placement pattern. |
| **Decomposition drift** — Drain mutex (US-0115 ships first; US-0116/US-0117 pick up other families). US-0101/US-0102 angle overlap with US-0114 is the only intentional cross-story overlap. | **LOW** | Bounded by angle-distinct narrative contract; bidirectional pointers (T-002). |

### Decision gate check

**No DECISION_GATE raised.** Architecture phase revealed no question requiring operator input. All 6 R-0103 carry-overs resolved by tech-lead within the `plan` macro:

1. Umbrella placement confirmed — after US-0114 umbrella close, before L1410.
2. Scratchpad reference extension placement confirmed — after US-0114's `### Release & distribution keys` block (L1551).
3. 7 per-feature subsection ordering confirmed — US-id-ascending (US-0034 → US-0084 → US-0086 → US-0093 → US-0096 → US-0101 → US-0102).
4. US-0034 cross-link-only shape confirmed (research recommendation (a) — cross-link to existing L585 README section, byte-stability preserved).
5. US-0096 net-new narrative shape confirmed (R-0103 CORRECTION — no pre-existing L591 README section; `#### US-0096` is net-new narrative + runbook cross-link to L591).
6. Bidirectional "see US-0114 for installer-payload angle" pointer convention confirmed in US-0101/US-0102 subsections.
7. DC-3 deferral confirmed — 7 missing h1 anchors deferred to US-0117 (US-0117 inherits 14 total).
8. Working-tree backlog.md encoding hygiene regression flagged to orchestrator for execute coordination.
9. Angle boundary for US-0101/US-0102 vs US-0114's US-0112 confirmed — US-0115 owns resolver mechanics + role catalog (DEC-0086 / DEC-0087); US-0114 owns installer payload (US-0112 presets).
10. `#### US-0084` / `#### US-0093` subsections document reason codes + runbook cross-links only (no scratchpad key blocks).

No sovereign-memory digest call needed (US-0115 is documentation-only; existing digest context sufficient per R-0103). Verdict: **PASS**.

### Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called (US-0115 documentation-only; existing digest context sufficient per R-0103). Sovereign-loop pattern for curator retrospective at segment close: "integration & observability family operator documentation completes the US-0113/US-0114/US-0115 umbrella triad under `## Commands and workflow`; cross-story byte-stability contract now covers **two** prior released blocks (US-0113 L1427 + US-0114 L1551) — net-new-keys-only + cross-link-pointer shape is the established triad-closure pattern." No write to `mistakes.jsonl` in architecture phase.

### Consequences

- Sprint: S0115 (pending `/sprint-plan`).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.
- Framework README pair grows by umbrella + 7 subsections + scratchpad reference extension (both `its_magic/README.md` and `template/its_magic/README.md` byte-identical).
- 7 missing `architecture.md` h1 anchors deferred to US-0117 (DC-3, parallel to US-0113's DC-1 — 5 anchors — and US-0114's DC-2 — 2 anchors; US-0117 inherits 14 total).
- No new tests; no new DECs; no compose-surface changes.

### Evidence references

- `docs/product/backlog.md` — `## US-0115` block (lines 3929–3945, 8 ACs)
- `docs/engineering/research.md` — `R-0103` (delivered 2026-07-04T07:53:00Z, 6/6 open questions closed; 7 per-feature sub-findings)
- `handoffs/po_to_tl.md` — research handoff (topmost block) + discovery handoff
- `docs/engineering/state.md` — research checkpoint (latest) + architecture checkpoint (this phase, appended)
- `handoffs/resume_brief.md` — top block updated to reflect architecture complete
- `.cursor/scratchpad.md` — integration & observability keys (L156–161 TOKEN_PROFILE, L181–186 DELIVERY_MODE/LEAN_MEMORY_*, L221–228 CROSS_REPO_OBSERVABILITY family, L230–234 COMPONENT_SCOPE, L355–374 MODEL_TIER/MODEL_CATALOG/MODEL_RESOLVE/MODEL_SLUG) — canonical source for AC-3 extension (net-new + cross-links)
- `its_magic/README.md` — L350 (`## Commands and workflow`) umbrella target; L585 (`### Optional cross-repo observability (US-0034)` — existing US-0034 section, cross-link target for US-0034 subsection); L940 (`### Sovereign-loop era` US-0113 sibling umbrella); L1225 (`### Release & distribution` US-0114 sibling umbrella); L1410 (`### Full scratchpad reference (detailed)`) extension target; L1427 (`### Sovereign-loop era keys` US-0113 sibling block — byte-stability preserved); L1551 (`### Release & distribution keys` US-0114 sibling block — byte-stability preserved)
- `docs/engineering/runbook.md` — 7 anchors: US-0034 L1167 h2; US-0084 L1441/L1459 h3; US-0086 L1398/L1471 h3; US-0093 L1999 h3 (parent h2 = US-0065 runtime QA autopilot contract L1486); US-0096 L591 h3; US-0101 L653 h2; US-0102 L771 h2
- `docs/engineering/architecture.md` — h1 inventory confirmed: `# US-0111` (L335), `# US-0112` (L454), `# US-0113` (L717), `# US-0114` (L914) exist; `# US-0034`/`# US-0084`/`# US-0086`/`# US-0093`/`# US-0096`/`# US-0101`/`# US-0102` missing (deferred to US-0117 as DC-3)
- `docs/engineering/decisions.md` — DEC-0082 (US-0096 delivery modes), DEC-0086 (US-0101 per-phase model tier), DEC-0087 (US-0102 role-based model catalog), DEC-0045 (US-0062 installer-owned boundary, referenced via US-0084 publish guard), DEC-0047 (US-0065 runtime QA autopilot contract, referenced via US-0093) — referenced, not amended; no US-0115 companion DEC

---

## US-0116 — Delivery & lifecycle operator documentation in framework README

### Overview

**US-0116** is a documentation-only story closing the operator-documentation gap for the **delivery & lifecycle** functional family — US-0092 (Delivery confirmation gate / full-autonomy outer driver + security posture), US-0095 (Native in-chat auto-chain), US-0098 (Dev environment auto-launch), US-0099 (Dev-environment copy-when-missing bootstrap). It adds an umbrella `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` under `## Commands and workflow` (L350) in `its_magic/README.md`, as the **4th sibling** to US-0113's `### Sovereign-loop era (US-0103–US-0112) umbrella section` (L940), US-0114's `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112) umbrella section` (L1225), and US-0115's `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102) umbrella section` (L1410). The umbrella carries 4 nested per-feature `#### US-xxxx` operator subsections ordered US-id-ascending (US-0092 → US-0095 → US-0098 → US-0099), inserted immediately after the closing of US-0115's umbrella block (before L1665 `### Full scratchpad reference (detailed)`). A matching `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` sub-block is appended to `### Full scratchpad reference (detailed)` (L1665) as the **4th sibling** to US-0113's `### Sovereign-loop era keys` (L1682), US-0114's `### Release & distribution keys` (L1806), and US-0115's `### Integration & observability keys` (L1878), inserted immediately after US-0115's keys block close (before L2026 `### Remote execution config`). The sub-block covers **true net-new key rows** only (US-0098's 2 dev-environment keys: `DEV_AUTO_LAUNCH_PROFILE` / `DEV_ENVIRONMENT_CONFIG`) + **reason-code-only entries** for US-0099 (`DEV_ENV_BOOTSTRAP_*` family + `DEV_ENV_PROFILE_MISSING` — 5 reason codes) + **grouped cross-link pointers** to pre-US-0116 README surfaces for US-0092/US-0095 keys + **cross-link pointers** to US-0114's `### Release & distribution keys` block for `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` overlap + optional cross-link pointer to US-0115's `### Integration & observability keys` block for `LEAN_MEMORY_*` family (default omit — angle-distinct). The framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`) is kept byte-identical via one-way copy. No code, schema, installer, scratchpad canonical, or runbook content changes.

**Binding decision**: **companion_dec=none** (US-0116 is documentation-only; no architectural, policy, or schema surface is being changed; R-0104 § Decision gate recommendation confirmed no DEC required — mirrors US-0113 / US-0114 / US-0115 sibling precedent; grep `^## DEC-` in `docs/engineering/decisions.md` returned no matches — confirmed no companion DEC exists). **Research anchor**: **R-0104** (delivered 2026-07-04T09:30:00Z, 8/8 open questions closed). **Compose guards (non-negotiable, 23 — UNCHANGED, cumulative across all prior stories)**: DO NOT amend US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062. **Status authority**: **OPEN** per **US-0045** (closure at `/release`).

**Fresh context marker**: `tl-US0116-architecture-20260704T094900Z-fresh`
**Orchestrator run id**: `auto-20260704-01`
**Timestamp**: 2026-07-04T09:49:00Z
**Verdict**: PASS
**Next**: `/sprint-plan`

### Companion DEC

**companion_dec = none**. US-0116 is documentation-only (mirrors US-0113 / US-0114 / US-0115 sibling precedent). No architectural, policy, or schema surface is being changed. Grep for `^## DEC-` in `docs/engineering/decisions.md` returned no matches — confirmed no US-0116 companion DEC is required and none was proposed in R-0104 § Decision gate recommendation. The DC-4 deferral (4 missing `# US-0092` / `# US-0095` / `# US-0098` / `# US-0099` h1 anchors) is a triad-hygiene carry-over to US-0117, not a tradeoff requiring a DEC.

### Approach locked — A1

**A1: Single `### Delivery & lifecycle` umbrella + 4 nested `#### US-xxxx` subsections (h4 under h3 umbrella), sibling to US-0113's `### Sovereign-loop era` (L940), US-0114's `### Release & distribution` (L1225), and US-0115's `### Integration & observability` (L1410) umbrellas, inserted immediately after the closing of US-0115's umbrella block (before L1665 `### Full scratchpad reference (detailed)`).**

**Justification**:
- **Consistency with prior stories** — US-0113 established the umbrella+subsection shape for the sovereign-loop family; US-0114 mirrored it for the release & distribution family; US-0115 mirrored it for the integration & observability family. Four sibling umbrellas in release order (US-0113 → US-0114 → US-0115 → US-0116) under `## Commands and workflow` form a clean quad.
- **Design challenge: alternatives considered.**
  - **A2 (rejected):** 4 separate top-level `### US-xxxx` h3 sections scattered under `## Commands and workflow` rather than grouped under an umbrella. Rejected: breaks the family-grouping precedent set by US-0113/US-0114/US-0115, hurts operator discoverability (no single entry point for the delivery & lifecycle family), and complicates the AC-1 acceptance criterion which explicitly requires an umbrella section.
  - **A3 (rejected):** Reuse an existing delivery & lifecycle README section as the umbrella and nest the other 3 features under it. Rejected: the existing pre-US-0116 README surfaces for US-0092/US-0095 keys (`### Automation modes` L880, `### Sync policy (US-0038)` L909, `### Optional /auto backlog-drain mode (US-0044)` L2370) are feature-mode blocks, not family-grouping blocks; elevating any one to umbrella-holder conflates a feature section with a family section, breaks byte-stability of the pre-US-0116 blocks, and breaks the family-parity contract (US-0113/US-0114/US-0115 each have a dedicated umbrella header). US-0098 has no pre-US-0116 README section at all.
  - **A1 is the only viable option** that satisfies AC-1 (umbrella section), preserves US-0113/US-0114/US-0115 sibling consistency, and respects byte-stability of prior released blocks. Lock A1.

### Files to touch

- `its_magic/README.md` — APPEND umbrella `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` (after US-0115 umbrella close, before L1665) + 4 nested `#### US-xxxx` operator subsections (US-0092 → US-0095 → US-0098 → US-0099) + `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` sub-block under `### Full scratchpad reference (detailed)` (after US-0115's `### Integration & observability keys` block at L1878; before L2026 `### Remote execution config`) covering 2 net-new key rows (US-0098) + 5 reason-code-only entries (US-0099) + grouped cross-link pointers (US-0092/US-0095 → pre-US-0116 surfaces; `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` → US-0114 L1806; optional `LEAN_MEMORY_*` → US-0115 L1878 default omit).
- `template/its_magic/README.md` — byte-identical sync via one-way copy from `its_magic/README.md` (AC-5).

### Files NOT to touch

- `.cursor/scratchpad.md` — canonical scratchpad; US-0116 documents keys in README, never edits the canonical source.
- `docs/product/backlog.md` — status authority (US-0045); encoding hygiene prerequisite flagged separately to orchestrator.
- `docs/engineering/runbook.md` — AC-7 cross-links only (all 4 anchors pre-exist); no new runbook content.
- `docs/developer/README.md` — US-0097 compose guard.
- `docs/engineering/architecture.md` — other than this US-0116 anchor append; DC-4 (4 missing h1 anchors) deferred to US-0117.
- `installer.py` / `installer.ps1` / `installer.sh`, `scripts/*`, any test file — out of scope (documentation-only story).
- **Do NOT modify US-0113's `### Sovereign-loop era` / `### Sovereign-loop era keys` blocks (L940 / L1682), US-0114's `### Release & distribution` / `### Release & distribution keys` blocks (L1225 / L1806), or US-0115's `### Integration & observability` / `### Integration & observability keys` blocks (L1410 / L1878)** in `its_magic/README.md` — byte-stability contract (all 3 already released in S0113 / S0114 / S0115). US-0116 adds cross-link pointers to these blocks from its own net-new block; it never edits them. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1878 range (no removals/modifications to US-0113's L1682, US-0114's L1806, or US-0115's L1878 blocks).

### Sprint seeds (T-001..T-006)

6 tasks within `SPRINT_MAX_TASKS=12` (mirror US-0113 / US-0114 / US-0115 sibling pattern; `SPRINT_AUTO_SPLIT` not triggered):

| Task | Description | ACs covered |
|------|-------------|-------------|
| **T-001** | Add umbrella `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` under `## Commands and workflow` (after US-0115 umbrella close, before L1665). Default-off framing for optional runtime features (US-0092 / US-0095 opt-in via `AUTO_FLOW_MODE=full_autonomy`; US-0098 opt-in via `DEV_AUTO_LAUNCH_PROFILE`); bootstrap-on-install framing for US-0099 (install-time only, zero runtime cost). 4-step enable order (US-0099 bootstrap → US-0098 auto-launch → US-0095 native in-chat chain primary → US-0092 outer-driver fallback) + runbook pointer line + zero-overhead-when-off contract line. | AC-1 |
| **T-002** | Add 4 per-feature `#### US-xxxx` operator subsections under the umbrella, ordered US-id-ascending (US-0092 → US-0095 → US-0098 → US-0099). US-0092 = full-autonomy outer driver + DEC-0078 security posture + hard caps + native-chain-vs-outer-driver routing (US-0095 primary, US-0092 fallback) + runbook cross-link to L1958 h3 + L1989 h4 (parent h2 = `## Auto continuation resume contract` L1587). US-0095 = native in-chat auto-chain (primary IDE recipe; compose-on-US-0044 `AUTO_BACKLOG_DRAIN`; drain-advance suppression `AUTO_QUIET=1`; `AUTO_IMPLEMENTATION_LOOP` + `AUTO_PAUSE_*` interaction; grouped cross-link to `### Automation modes` L880 + main reference list; optional `LEAN_MEMORY_*` cross-link to US-0115 L1878 — default omit, angle-distinct) + runbook cross-link to L1900 h3 (parent h2 = L1587). US-0098 = `DEV_AUTO_LAUNCH_PROFILE` default-off + `DEV_ENVIRONMENT_CONFIG` path + orthogonality to US-0065 / US-0086 / US-0067 / `AUTO_REMOTE_AUTOMATION_PROFILE` + detection precedence (US-0086 remote wins over docker-host-local per DEC-0084 §3) + compose-with-US-0099 + runbook cross-link to L244 h2. US-0099 = install-time copy-when-missing bootstrap (never overwrites) + customize-after-bootstrap contract + `DEV_ENV_BOOTSTRAP_*` reason-code family (5 codes) + `DEV_ENV_PROFILE_MISSING` remediation + compose-with-US-0098 + runbook cross-link to L244 (parent h2) with secondary pointers to L250 (bootstrap paragraph) + L301 (normative contract anchor). | AC-2, AC-7 |
| **T-003** | Add `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` sub-block under `### Full scratchpad reference (detailed)` (after US-0115's `### Integration & observability keys` block L1878; before L2026 `### Remote execution config`). True net-new key rows (2): US-0098 `DEV_AUTO_LAUNCH_PROFILE=off\|deterministic_v1` (default `off`) + `DEV_ENVIRONMENT_CONFIG=repo-relative path` (default `.cursor/dev-environment.json`). Reason-code-only entries (5): US-0099 `DEV_ENV_BOOTSTRAP_COPIED` / `DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS` / `DEV_ENV_BOOTSTRAP_PATH_INVALID` / `DEV_ENV_BOOTSTRAP_SOURCE_MISSING` / `DEV_ENV_PROFILE_MISSING`. Grouped cross-link pointers (no duplicate rows): US-0092/US-0095 keys (`AUTO_FLOW_MODE` / `AUTO_IMPLEMENTATION_LOOP` / `AUTO_PAUSE_*` / `AUTO_LOOP_MAX_CYCLES` / `AUTO_BACKLOG_MAX_STORIES` / `ALLOW_AUTO_PUSH` / `AUTO_PUSH_BRANCH_ALLOWLIST` / `AUTO_BACKLOG_DRAIN` / `AUTO_BUG_QUEUE` etc.) → `### Automation modes` L880 + `### Sync policy (US-0038)` L909 + `### Optional /auto backlog-drain mode (US-0044)` L2370 + main reference list (NOT to US-0113's L1682 block — those keys are not there); `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` → US-0114's `### Release & distribution keys` block (L1806); optional `LEAN_MEMORY_*` → US-0115's `### Integration & observability keys` block (L1878) — default omit (angle-distinct per open question #2). Byte-stability of US-0113 L1682 + US-0114 L1806 + US-0115 L1878 blocks preserved (net-new-keys-only + cross-link-pointer + reason-code-only shape; 4th-story cumulative surface). | AC-3 |
| **T-004** | Sync `template/its_magic/README.md` byte-identical via one-way copy from `its_magic/README.md`. Re-run `python -c "a=open(r'its_magic/README.md','rb').read(); b=open(r'template/its_magic/README.md','rb').read(); print('PARITY_OK' if a==b else 'PARITY_DIFF')"` (expect `PARITY_OK`) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`). | AC-5 |
| **T-005** | Run validators: `python scripts/validate_readme_feature_coverage.py --enforce` (expect `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0 — catalog block L63 read-only) + `python scripts/validate_doc_profile.py` (expect `[DOC_PROFILE_VALIDATE_OK]`) + `python scripts/check-user-visible-metadata.py` (expect exit 0; US-IDs only in parenthetical catalog tags `(US-xxxx)`). | AC-4, AC-6 |
| **T-006** | Run regression tests: `python -m pytest tests/scratchpad_example_parity_test.py -q` (expect 4/4 PASS). **Forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` — if a test fails, the prose is wrong, not the test (fix prose, never relax test). | AC-8 |

**Execution order**: T-001 (umbrella) → T-002 (4 subsections) → T-003 (scratchpad ref extension) → T-004 (template byte-sync) → T-005 (validators) → T-006 (regression tests). Acyclic, mirrors US-0113/US-0114/US-0115.

### Test markers

Same 5 as US-0113 / US-0114 / US-0115 (no new tests proposed):

1. `tests/scratchpad_example_parity_test.py` — 4 markers (AC-5 indirect via scratchpad canonical parity, AC-8).
2. `scripts/validate_readme_feature_coverage.py --enforce` — AC-4.
3. `scripts/check_intake_template_parity.py` — AC-5.
4. `scripts/validate_doc_profile.py` — AC-6.
5. `scripts/check-user-visible-metadata.py` — AC-6.

### Compose guards (UNCHANGED — 23 guards, cumulative)

US-0116 is documentation-only and lives entirely outside the compose surface. The 23 compose guards (cumulative across all prior stories — same 23 as US-0115; US-0116 adds no new family-internal guards because all 4 in-scope features are delivery & lifecycle operators, not compose-surface features) remain UNCHANGED:

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062.

### Stop conditions

**stop_conditions_met=yes**:

- **No DEC required** — confirmed (companion_dec=none; documentation-only; mirrors US-0113 / US-0114 / US-0115 sibling precedent; R-0104 § Decision gate recommendation confirmed no DEC candidate; grep `^## DEC-` in decisions.md returned no matches).
- **No feasibility unknown** — R-0104 closed all 8 spec open questions (cross-link-only to pre-US-0116 surfaces for US-0092/US-0095; `LEAN_MEMORY_*` angle-distinct default omit; `DELIVERY_MODE` bidirectional cross-link to US-0114; `AUTO_INSTALL_DEPS`/`AUTO_RELEASE_NOTES` cross-link to US-0114; runbook anchor h-levels CONFIRMED — US-0092 L1958 h3 + L1989 h4, US-0095 L1900 h3, US-0098 L244 h2, US-0099 L250 inside US-0098 h2 + L301 normative contract anchor; DC-4 deferred to US-0117; 4th-story byte-stability contract LOCKED; `AUTO_LOOP_MAX_CYCLES` / `AUTO_BACKLOG_MAX_STORIES` exact key names CONFIRMED).
- **No data migration risk** — documentation-only; no schema, no data, no installer, no scratchpad canonical changes.

### DC-4 resolution (deferred to US-0117)

**DC-4**: 4 missing `# US-xxxx` h1 anchors in active `docs/engineering/architecture.md` for the US-0116 family — `# US-0092`, `# US-0095`, `# US-0098`, `# US-0099`. Grep for `^# US-(0092|0095|0098|0099)` in `docs/engineering/architecture.md` returned no matches (confirmed in R-0104 § DC-4 confirmation; only present in archive packs; US-0098/US-0099 are referenced as `# US-0098` / `# US-0099` (bootstrap posture) in runbook L301 but have no dedicated h1 in active `architecture.md`). Not a US-0116 blocker — AC-7 is satisfiable via runbook cross-links (all 4 features have existing verified runbook anchors). US-0117 (Phase & role governance family) inherits DC-1 (5 anchors from US-0113: US-0103/0104/0105/0107/0110) + DC-2 (2 anchors from US-0114: US-0041/US-0062) + DC-3 (7 anchors from US-0115: US-0034/US-0084/US-0086/US-0093/US-0096/US-0101/US-0102) + DC-4 (4 anchors from US-0116: US-0092/US-0095/US-0098/US-0099) = **18 total missing `# US-xxxx` h1 anchors** as architecture.md triad hygiene closure.

**Deferral note for orchestrator**: This is a **deferral candidate** for the orchestrator's segment-boundary advance hook. **DO NOT append to `handoffs/sovereign_deferrals.jsonl` in architecture phase** (per instructions — segment-boundary advance hook handles it, not phase boundaries). `/architecture` documents the deferral in this findings block; does NOT add the h1 anchors. When US-0117 enters `plan` macro, its discovery should narrow-read this section and add the 4 missing h1 anchors as a task seed. Anchor format to use at that time: `# US-xxxx — <feature title>` (matching existing `# US-0108`, `# US-0109`, `# US-0111`, `# US-0112`, `# US-0113`, `# US-0114`, `# US-0115` format).

### Risks (finalized)

| Risk | Severity | Mitigation |
|------|----------|------------|
| **AC-3 byte-stability (4th-story cumulative surface — first 4-cumulative-surface story)** — US-0116 is the fourth story to extend `### Full scratchpad reference`; cumulative surface now covers 3 prior released blocks (US-0113 L1682 + US-0114 L1806 + US-0115 L1878). Risk of accidentally editing a prior released block. | **MEDIUM** | Net-new-keys-only (US-0098's 2 keys) + reason-code-only entries (US-0099's 5 reason codes) + grouped cross-link pointers LOCKED in `/architecture` (T-003). Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1878 range (no removals/modifications to US-0113's L1682, US-0114's L1806, or US-0115's L1878 blocks). QA re-verifies. Mirrors S0114 / S0115 retrospective pattern extended to 4th story. |
| **AC-5 parity lockstep** — `its_magic/README.md` edited but `template/its_magic/README.md` not synced (or vice versa). | **MEDIUM** | T-004 mandates one-way copy `its_magic/README.md` → `template/its_magic/README.md` after T-001/T-002/T-003 complete. Execute-phase must re-run byte-parity check + `check_intake_template_parity.py`. QA re-verifies both gates. |
| **AC-2 US-0092/US-0095 angle overlap (native chain vs outer driver)** — Both share `AUTO_FLOW_MODE=full_autonomy` opt-in. | **LOW** | Primary/fallback boundary table mirrors runbook L1921–L1926 (US-0095 primary IDE; US-0092 fallback headless/CI or `NATIVE_CHAIN_UNAVAILABLE`). Angle-distinct narrative contract — US-0095 owns process angle (orchestrator self-chain mechanism); US-0092 owns security posture + outer-driver fallback. |
| **AC-2 US-0098/US-0099 angle boundary (runtime vs install-time)** — Both share the `## Dev environment auto-launch (US-0098 / DEC-0084)` h2 at runbook L244. | **LOW** | US-0098 = execute-phase runtime gate (default-off `DEV_AUTO_LAUNCH_PROFILE`); US-0099 = install-time bootstrap (copy-when-missing, runs only on `missing` / `upgrade` / `postinstall`). Distinct narrative angles — no overlap. T-002 separates them as `#### US-0098` and `#### US-0099` subsections under the umbrella. |
| **AC-3 `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` overlap (cross-link to US-0114)** — US-0114's `### Release & distribution keys` block (L1806) owns these rows. | **MEDIUM→LOW** | Cross-link pointer to US-0114's block (T-003); US-0116 does NOT re-document `DELIVERY_MODE` defaults; US-0114 owns those rows. Angle-distinct: US-0114 = release-workflow angle; US-0116 = auto-chain lifecycle-shape / enablement angle. |
| **AC-3 `LEAN_MEMORY_*` family overlap (cross-link to US-0115)** — US-0115's `### Integration & observability keys` block (L1878) owns the canonical `LEAN_MEMORY_*` family rows per US-0096/DEC-0082. | **LOW** | Default omit; US-0095 is angle-distinct from US-0096's `LEAN_MEMORY_*` family (process angle vs memory angle). If the US-0095 composition narrative is essential, T-002 adds a brief single-sentence pointer ("composes with `LEAN_MEMORY_*` family documented in `### Integration & observability keys` above") — no key row duplication. |
| **AC-3 `AUTO_BACKLOG_DRAIN` / `AUTO_BUG_QUEUE` overlap (cross-link to US-0044/US-0087/US-0088)** — These keys are documented in pre-US-0116 README surfaces, NOT in US-0113's L1682 block. | **LOW** | Grouped cross-link pointer to `### Optional /auto backlog-drain mode (US-0044)` README section (L2370) and US-0087/US-0088 catalog one-liners (L2261/L2263); NOT a cross-link to US-0113's sovereign-loop keys block (those keys are not there — confirmed in R-0104 open question #1). |
| **AC-7 runbook cross-links** — 4 features, all anchors pre-exist (no gap, unlike US-0114's US-0062). US-0099 has no dedicated top-level runbook h2. | **LOW** | All 4 anchors verified in R-0104: US-0092 L1958 h3 + L1989 h4 (parent h2 = `## Auto continuation resume contract` L1587); US-0095 L1900 h3 (parent h2 = L1587); US-0098 L244 h2 (top-level); US-0099 L250 (paragraph inside US-0098's h2) + L301 normative contract anchor. T-002 uses the AC-7 cross-link format for US-0099 (L244 parent h2 with secondary pointers to L250 + L301). |
| **AC-4 encoding hygiene prerequisite (carried from US-0114)** — Working-tree `docs/product/backlog.md` has 185 stray `0xa7` (§) bytes per R-0102 / R-0103 / R-0104. Orchestrator must restore encoding hygiene before execute so AC-4 can be re-verified post-execute. | **MEDIUM (carried)** | `/architecture` makes no backlog.md edits. Flag to orchestrator: restore backlog.md encoding hygiene before execute. NOT a US-0116 blocker (research + architecture are read-only on backlog.md). |
| **AC-8 regression tests (4th-story cumulative surface)** — coverage parity contract tests weakened or failing. | **LOW–MEDIUM** | US-0116 is documentation-only; **forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` in execute-phase task list. If a test fails, fix prose, never relax test. T-006 confirms green. |
| **AC-1 umbrella placement (4th sibling)** — Risk of inserting the umbrella inside US-0115's block rather than after it. | **LOW** | Insert after US-0115 umbrella close (before L1665 `### Full scratchpad reference`), NOT inside it. Mirrors US-0115-after-US-0114 placement pattern. |
| **DC-4 architecture.md h1 anchors (4 missing)** — Triad-hygiene carry-over, not a US-0116 blocker. | **LOW** | Defer to US-0117 — US-0117 inherits DC-1 (5) + DC-2 (2) + DC-3 (7) + DC-4 (4) = 18 total. AC-7 satisfied via runbook cross-links. |
| **Decomposition drift** — Drain mutex (US-0116 ships first; US-0117 picks up the phase & role governance family). No intentional cross-story overlap with US-0117. | **LOW** | Bounded by angle-distinct narrative contract; US-0116 owns delivery & lifecycle feature operator guides only; US-0117 owns phase command catalog + role governance. |
| **Cross-story byte-stability contract (4th story)** — US-0116 is the fourth story to extend `### Full scratchpad reference`. | **MEDIUM** | Net-new-keys-only (US-0098's 2 keys) + reason-code-only entries (US-0099's 5 reason codes) + grouped cross-link pointers; execute verifies pure-addition `git diff` in the L1878–end range. Pattern now established as a quad (S0113/S0114/S0115 + US-0116). |

### Decision gate check

**No DECISION_GATE raised.** Architecture phase revealed no question requiring operator input. All 13 R-0104 carry-overs resolved by tech-lead within the `plan` macro:

1. Umbrella placement confirmed — immediately after the closing of the US-0115 integration & observability umbrella block (before L1665 `### Full scratchpad reference`), NOT inside it.
2. Scratchpad reference extension placement confirmed — immediately after the closing of US-0115's `### Integration & observability keys` block (L1878); before L2026 `### Remote execution config`. NOT inside US-0115's block.
3. 4 per-feature subsection ordering confirmed — US-id-ascending (US-0092 → US-0095 → US-0098 → US-0099).
4. US-0092/US-0095 grouped cross-link pointer to pre-US-0116 README surfaces confirmed (no net-new key rows for US-0092/US-0095).
5. US-0098 net-new key rows confirmed (`DEV_AUTO_LAUNCH_PROFILE` / `DEV_ENVIRONMENT_CONFIG` — the only true net-new key rows in the delivery & lifecycle keys sub-block).
6. US-0099 reason-code-only entries confirmed (5 reason codes — `DEV_ENV_BOOTSTRAP_*` family + `DEV_ENV_PROFILE_MISSING`; no scratchpad key block).
7. Cross-link pointer to US-0114's `### Release & distribution keys` block (L1806) for `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` overlap confirmed (byte-stability — US-0114 owns those rows).
8. Optional cross-link pointer to US-0115's `### Integration & observability keys` block (L1878) for `LEAN_MEMORY_*` family overlap — default omit confirmed (angle-distinct per R-0104 open question #2 resolution).
9. DC-4 deferral confirmed — 4 missing h1 anchors (US-0092 / US-0095 / US-0098 / US-0099) deferred to US-0117 (US-0117 inherits 18 total).
10. Working-tree backlog.md encoding hygiene regression (185 stray 0xa7 bytes per R-0102 / R-0103 / R-0104) flagged to orchestrator for execute coordination.
11. Angle boundary for US-0092 vs US-0095 confirmed — US-0095 = primary (IDE native chain); US-0092 = optional fallback (headless/CI or `NATIVE_CHAIN_UNAVAILABLE`).
12. Angle boundary for US-0098 vs US-0099 confirmed — US-0098 = execute-phase runtime gate (default-off); US-0099 = install-time bootstrap (copy-when-missing, runs only on `missing` / `upgrade` / `postinstall`).
13. `#### US-0099` AC-7 cross-link format confirmed — points to L244 (parent h2 `## Dev environment auto-launch (US-0098 / DEC-0084)`) with secondary pointers to L250 (the bootstrap paragraph) and L301 (normative contract anchor `# US-0098` / `# US-0099` (bootstrap posture)); US-0099 does NOT have a dedicated top-level runbook h2.

No sovereign-memory digest call needed (US-0116 is documentation-only; existing digest context sufficient per R-0104 — S0113/S0114/S0115 retrospectives established the reusable patterns applied here; the cross-link pointer pattern + angle-distinct narrative pattern + cross-story byte-stability contract now form a quad). Verdict: **PASS**.

### Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called (US-0116 documentation-only; existing digest context sufficient per R-0104). Sovereign-loop pattern for curator retrospective at segment close: "delivery & lifecycle family operator documentation completes the US-0113/US-0114/US-0115/US-0116 umbrella quad under `## Commands and workflow`; cross-story byte-stability contract now covers **three** prior released blocks (US-0113 L1682 + US-0114 L1806 + US-0115 L1878) — net-new-keys-only + cross-link-pointer + reason-code-only shape is the established quad-closure pattern; US-0116 is the first 4-cumulative-surface story." No write to `mistakes.jsonl` in architecture phase.

### Consequences

- Sprint: S0116 (pending `/sprint-plan`).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.
- Framework README pair grows by umbrella + 4 subsections + scratchpad reference extension (both `its_magic/README.md` and `template/its_magic/README.md` byte-identical).
- 4 missing `architecture.md` h1 anchors deferred to US-0117 (DC-4, parallel to US-0113's DC-1 — 5 anchors, US-0114's DC-2 — 2 anchors, and US-0115's DC-3 — 7 anchors; US-0117 inherits 18 total).
- No new tests; no new DECs; no compose-surface changes.

### Evidence references

- `docs/product/backlog.md` — `## US-0116` block (lines 3947–3963, 8 ACs)
- `docs/engineering/research.md` — `R-0104` (delivered 2026-07-04T09:30:00Z, 8/8 open questions closed; 4 per-feature sub-findings)
- `handoffs/po_to_tl.md` — research handoff (topmost block) + spec handoff
- `docs/engineering/state.md` — research checkpoint (latest) + architecture checkpoint (this phase, appended)
- `handoffs/resume_brief.md` — top block updated to reflect architecture complete
- `.cursor/scratchpad.md` — delivery & lifecycle keys (L11–22 auto implementation loop / pause policy, L30–38 full-autonomy interaction, L41–56 backlog drain / bug queue, L63 active, L142–148 sync policy / auto-push allowlist, L173–186 delivery mode / lean memory, L201 release publish, L295–298 dev auto-launch profile) — canonical source for AC-3 extension (net-new + cross-links)
- `its_magic/README.md` — L350 (`## Commands and workflow`) umbrella target; L880 (`### Automation modes` — pre-US-0116 US-0092/US-0095 surface, grouped cross-link target); L909 (`### Sync policy (US-0038)` — pre-US-0116 US-0092 surface, grouped cross-link target); L940 (`### Sovereign-loop era` US-0113 sibling umbrella — byte-stability preserved); L1225 (`### Release & distribution` US-0114 sibling umbrella — byte-stability preserved); L1410 (`### Integration & observability` US-0115 sibling umbrella — byte-stability preserved); L1665 (`### Full scratchpad reference (detailed)`) extension target; L1682 (`### Sovereign-loop era keys` US-0113 sibling block — byte-stability preserved); L1806 (`### Release & distribution keys` US-0114 sibling block — byte-stability preserved + cross-link target for `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES`); L1878 (`### Integration & observability keys` US-0115 sibling block — byte-stability preserved + optional cross-link target for `LEAN_MEMORY_*`); L2026 (`### Remote execution config`) — confirmed insertion point for `### Delivery & lifecycle keys` block (before this line); L2261/L2263 (US-0087/US-0088 catalog one-liners — pre-US-0116 grouped cross-link targets); L2370 (`### Optional /auto backlog-drain mode (US-0044)` — pre-US-0116 grouped cross-link target for `AUTO_BACKLOG_DRAIN` / `AUTO_BUG_QUEUE` family)
- `docs/engineering/runbook.md` — 4 anchors: US-0092 L1958 h3 + L1989 h4 (parent h2 = `## Auto continuation resume contract` L1587); US-0095 L1900 h3 (parent h2 = L1587); US-0098 L244 h2 (top-level); US-0099 L250 (paragraph inside US-0098 h2) + L301 (normative contract anchor)
- `docs/engineering/architecture.md` — h1 inventory confirmed: `# US-0111` (L335), `# US-0112` (L454), `# US-0113` (L717), `# US-0114` (L914), `# US-0115` (L1117) exist; `# US-0092`/`# US-0095`/`# US-0098`/`# US-0099` missing (deferred to US-0117 as DC-4)
- `docs/engineering/decisions.md` — DEC-0078 (US-0092 security posture), DEC-0080 (US-0095 native chain), DEC-0081 (US-0095 orchestrator continuation), DEC-0082 (US-0096 delivery modes, referenced via `LEAN_MEMORY_*` overlap), DEC-0084 (US-0098/US-0099 dev environment + bootstrap posture), DEC-0018 (sync policy disabled, referenced via `AUTO_PUSH_BRANCH_ALLOWLIST`), DEC-0038 (runtime proof) — referenced, not amended; no US-0116 companion DEC (grep `^## DEC-` returned no matches)



## US-0117 — Phase & role governance operator documentation in framework README

### Overview

**US-0117** is a documentation-only story closing the operator-documentation gap for the **phase & role governance** functional family — the LARGEST family in the 5-story drain (18 features: US-0069, US-0070, US-0071, US-0072, US-0075, US-0076, US-0077, US-0078, US-0079, US-0080, US-0081, US-0082, US-0083, US-0085, US-0087, US-0088, US-0089, US-0090). It adds the **5th sibling umbrella** `### Phase & role governance (US-0069 / US-0070 / US-0071 / US-0072 / US-0075 / US-0076 / US-0077 / US-0078 / US-0079 / US-0080 / US-0081 / US-0082 / US-0083 / US-0085 / US-0087 / US-0088 / US-0089 / US-0090) umbrella section` under `## Commands and workflow` (L350) in `its_magic/README.md`, as a sibling to US-0113's `### Sovereign-loop era` (L940), US-0114's `### Release & distribution` (L1225), US-0115's `### Integration & observability` (L1410), and US-0116's `### Delivery & lifecycle` (L1665) umbrellas, inserted after US-0116's umbrella close (before L1665 `### Full scratchpad reference (detailed)`). The umbrella carries 18 nested per-feature `#### US-xxxx` operator subsections ordered US-id-ascending. A matching `### Phase & role governance keys (US-0069 / ... / US-0090)` sub-block is appended to `### Full scratchpad reference (detailed)` (L1665) as the **5th sibling** to US-0113's `### Sovereign-loop era keys` (L1682), US-0114's `### Release & distribution keys` (L1806), US-0115's `### Integration & observability keys` (L1878), and US-0116's `### Delivery & lifecycle keys` (L2225), inserted after US-0116's keys block close (before `### Remote execution config`). The sub-block covers **46 net-new key rows** across 10 features (US-0069/0070/0079/0080/0081/0083/0087/0088/0089/0090) + **9 reason-code-only entries** (7 features) + **7 prose-only / runbook-cross-link-only entries** (US-0071/0072/0075/0076/0077/0078/0085) + **cross-link pointers** (`DELIVERY_MODE` -> US-0114 L1806; `LEAN_MEMORY_*` -> US-0115 L1877 default omit; `TOKEN_PROFILE` -> main reference list + US-0080 subsection; `CODEBASE_MAP_REFRESH_ON_ROLLOVER` -> US-0082 subsection). Two labeling corrections locked: US-0082 = **Codebase map** (per runbook L63 + DEC-0065; spec handoff's "Input compression" is a mislabel); US-0090 = **Caveman input compression** (per runbook L2099 + DEC-0073; spec handoff's "Phase governance integration" is a mislabel — "phase governance integration" is the umbrella's introductory framing AC-1, not a separate `#### US-0090` subsection). US-0089 = **Auto orchestration** (per scratchpad L21/L135 + 18-feature family; note US-id collision with runbook h2 `## Caveman mode (US-0089)` L2032 — `/architecture` locks the resolution: the `#### US-0089` subsection title is "Auto orchestration", NOT "Caveman mode"). The framework README pair (`its_magic/README.md` <-> `template/its_magic/README.md`) is kept byte-identical via one-way copy. No code, schema, installer, scratchpad canonical, or runbook content changes.

**Binding decision**: **companion_dec=none** (US-0117 is documentation-only; no architectural, policy, or schema surface is being changed; R-0105 § Decision-gate check confirmed no DEC required — mirrors US-0113 / US-0114 / US-0115 / US-0116 sibling precedent; grep `^## DEC-` in `docs/engineering/decisions.md` returned no US-0117 companion DEC). **Research anchor**: **R-0105** (delivered 2026-07-04T16:54:35Z, 8/8 open questions closed; 18 per-feature sub-findings; AC-3 approach locked; DC-1..DC-4 confirmed = 18 deferred + 18 own = 36 total h1 anchors to add in `/architecture`; AC baselines green; deepened risks). **Compose guards (non-negotiable, 23 — UNCHANGED, cumulative across all prior stories — same 23 as US-0116)**: DO NOT amend US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062. **Status authority**: **OPEN** per **US-0045** (closure at `/release`).

**Fresh context marker**: `tl-US0117-architecture-20260704T171500Z-fresh`
**Orchestrator run id**: `auto-20260704-01`
**Timestamp**: 2026-07-04T17:15:00Z (UTC)
**Verdict**: PASS
**Next**: `/sprint-plan`

### Companion DEC

**companion_dec = none**. US-0117 is documentation-only (mirrors US-0113 / US-0114 / US-0115 / US-0116 sibling precedent). No architectural, policy, or schema surface is being changed. Grep for `^## DEC-` in `docs/engineering/decisions.md` returned no matches — confirmed no US-0117 companion DEC is required and none was proposed in R-0105 § Decision-gate check. The DC-1+DC-2+DC-3+DC-4 resolution (36 h1 anchors added in THIS phase) is a triad-hygiene closure, not a tradeoff requiring a DEC.

### Approach locked (A1)

**Approach A1** (locked): Single `### Phase & role governance` umbrella + 18 nested `#### US-xxxx` subsections (h4 under h3 umbrella), sibling to US-0113's `### Sovereign-loop era`, US-0114's `### Release & distribution`, US-0115's `### Integration & observability`, and US-0116's `### Delivery & lifecycle` umbrellas, inserted after US-0116's umbrella under `## Commands and workflow`. Consistency with prior 4 stories.

| Option | Summary | Verdict |
|--------|---------|---------|
| **A1** | **Single umbrella + 18 nested subsections + 5th scratchpad ref sub-block** (net-new keys + cross-link pointers + reason-code-only + prose-only) | **Preferred** — matches US-0113 / US-0114 / US-0115 / US-0116 sibling precedent (5th sibling). |
| A2 (rejected) | Reuse an existing phase governance README section as umbrella and nest the other 17 features under it. | **Rejected** — pre-US-0117 README surfaces for phase/role keys (`### Automation modes` L880, `### Sync policy (US-0038)` L909, `### Optional /auto backlog-drain mode (US-0044)` L2370) are feature-mode blocks, not family-grouping blocks; elevating any one to umbrella-holder conflates a feature section with a family section, breaks byte-stability of pre-US-0117 blocks, and breaks the family-parity contract (prior 4 stories each have a dedicated umbrella header). Several US-0117 features (US-0069 / US-0070 / US-0071 / US-0075 / US-0077 / US-0085) have no pre-US-0117 README section at all. |
| A3 (rejected) | Split the 18 features across 2 umbrellas ("phase governance" + "role governance"). | **Rejected** — breaks the 5-sibling parity contract (prior 4 stories each have ONE umbrella per family); the 18 features form one coherent family per backlog.md US-0117 decomposition (US-0051); splitting would fragment the operator catalog. |

### Files to touch

- `its_magic/README.md` — APPEND umbrella `### Phase & role governance (US-0069 / ... / US-0090) umbrella section` (after US-0116 umbrella close, before L1665 `### Full scratchpad reference (detailed)`) + 18 nested `#### US-xxxx` operator subsections (US-0069 -> US-0070 -> US-0071 -> US-0072 -> US-0075 -> US-0076 -> US-0077 -> US-0078 -> US-0079 -> US-0080 -> US-0081 -> US-0082 -> US-0083 -> US-0085 -> US-0087 -> US-0088 -> US-0089 -> US-0090) + `### Phase & role governance keys (US-0069 / ... / US-0090)` sub-block under `### Full scratchpad reference (detailed)` (after US-0116's `### Delivery & lifecycle keys` block at L2225; before `### Remote execution config`). Sub-block covers 46 net-new key rows + 9 reason-code-only entries + 7 prose-only / runbook-cross-link-only entries + cross-link pointers.
- `template/its_magic/README.md` — byte-identical one-way copy of `its_magic/README.md` (AC-5 parity; T-004).

### Files NOT to touch

- `.cursor/scratchpad.md` — canonical scratchpad; US-0117 documents keys in README, never edits the canonical source.
- `template/.cursor/scratchpad.local.example.md` — framework parity file; US-0117 does not extend the example scratchpad (AC-3 extension is in README only).
- `docs/product/backlog.md` — status authority; US-0117 remains OPEN until `/release`.
- `docs/engineering/runbook.md` — AC-7 cross-links only (no runbook edits; US-0117 points TO existing runbook anchors, never edits them).
- `docs/developer/README.md` — US-0097 compose guard.
- `docs/engineering/architecture.md` — **other than this `## US-0117` append + the 36 DC anchors appended below**, no edits. Execute-phase does NOT add h1 anchors.
- `installer.py` / `installer.ps1` / `installer.sh` / `scripts/*` — no code or installer changes (US-0117 documentation-only).
- `tests/scratchpad_example_parity_test.py` — AC-8 regression test; forbid edits.
- **Do NOT modify US-0113's `### Sovereign-loop era` / `### Sovereign-loop era keys` blocks (L940 / L1682), US-0114's `### Release & distribution` / `### Release & distribution keys` blocks (L1225 / L1806), US-0115's `### Integration & observability` / `### Integration & observability keys` blocks (L1410 / L1878), or US-0116's `### Delivery & lifecycle` / `### Delivery & lifecycle keys` blocks (L1665 / L2225)** in `its_magic/README.md` — byte-stability contract (all 4 already released in S0113 / S0114 / S0115 / S0116). US-0117 adds cross-link pointers to these blocks from its own 5th sub-block; it never edits them. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2225 range (no removals/modifications to US-0113's L1682, US-0114's L1806, US-0115's L1878, or US-0116's L2225 blocks).

### Sprint seeds (T-001..T-006 + T-anch = 7 tasks within SPRINT_MAX_TASKS=12)

| Task | AC | Description | Role |
|------|----|-------------|------|
| **T-anch** | AC-2 / AC-8 | Add 36 `## US-xxxx` h1 anchors to `docs/engineering/architecture.md` (18 own: US-0069/0070/0071/0072/0075/0076/0077/0078/0079/0080/0081/0082/0083/0085/0087/0088/0089/0090 + 18 deferred DC-1+DC-2+DC-3+DC-4: US-0103/0104/0105/0107/0110 + US-0041/0062 + US-0034/0084/0086/0093/0096/0101/0102 + US-0092/0095/0098/0099) + the `# US-0117` anchor (already authored in `/architecture`). Minimal 3–5 line normative sections. **First-time DC anchor addition in architecture phase** (resolved HERE, not deferred to `/execute`). | B |
| **T-001** | AC-1 | Add umbrella `### Phase & role governance (US-0069 / ... / US-0090) umbrella section` under `## Commands and workflow` (after US-0116 umbrella close, before L1665). 18-step enable order (US-id-ascending) + runbook pointer line + zero-overhead-when-off contract line + "phase governance integration" introductory framing (AC-1). | B |
| **T-002** | AC-2 / AC-7 | Add 18 per-feature operator subsections (US-0069 -> US-0090) under the umbrella. Two labeling corrections applied: US-0082 = "Codebase map" (NOT "Input compression"); US-0090 = "Caveman input compression" (NOT "Phase governance integration"); US-0089 = "Auto orchestration" (NOT "Caveman mode" — runbook US-id collision resolved). Each subsection carries AC-7 runbook cross-link. | B |
| **T-003** | AC-3 | Add `### Phase & role governance keys` sub-block under `### Full scratchpad reference (detailed)` (after US-0116 L2225 block). 46 net-new key rows (10 features) + 9 reason-code-only entries (7 features) + 7 prose-only / runbook-cross-link-only entries (US-0071/0072/0075/0076/0077/0078/0085) + cross-link pointers (`DELIVERY_MODE` -> US-0114; `LEAN_MEMORY_*` -> US-0115 default omit; `TOKEN_PROFILE` -> main ref + US-0080; `CODEBASE_MAP_REFRESH_ON_ROLLOVER` -> US-0082). 5th-story cumulative byte-stability surface — prior 4 blocks byte-identical. | B |
| **T-004** | AC-5 | Sync `template/its_magic/README.md` byte-identical to `its_magic/README.md` (one-way copy). Verify `PARITY_OK <size> <size>`. | B |
| **T-005** | AC-4 / AC-6 | Run validators: `python scripts/validate_readme_feature_coverage.py --repo . --enforce` -> `[README_FEATURE_COVERAGE_VALIDATE_OK]` with `coverage_missing=["US-0117"]` unchanged (US-0117 not in catalog surface). `python scripts/validate_doc_profile.py --repo .` + `python scripts/check-user-visible-metadata.py --repo .` + `python scripts/check_intake_template_parity.py --repo .` -> expect PASS. Fix any narrative prose leaking internal IDs. | B |
| **T-006** | AC-8 | Run regression tests: `python -m pytest tests/scratchpad_example_parity_test.py -v` -> 4 passed. Forbid edits to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, `tests/scratchpad_example_parity_test.py`. | B |

**Execution order**: T-anch -> T-001 -> T-002 -> T-003 -> T-004 -> T-005 -> T-006. Acyclic. (T-anch first because it is on `architecture.md`, not `its_magic/README.md`; doing it first keeps the README byte-stability surface clean for subsequent T-001..T-004.)

### Test markers (5 — same as prior stories)

- `tests/scratchpad_example_parity_test.py` (4 tests)
- `scripts/validate_readme_feature_coverage.py --enforce`
- `scripts/validate_doc_profile.py`
- `scripts/check-user-visible-metadata.py`
- `scripts/check_intake_template_parity.py`

### Compose guards UNCHANGED (23 cumulative — same 23 as US-0116)

US-0117 is documentation-only and lives entirely outside the compose surface. The 23 compose guards (cumulative across all prior stories — US-0117 adds no new family-internal guards because all 18 in-scope features are phase & role governance operators, not compose-surface features) remain UNCHANGED:

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062.

### DC-1 + DC-2 + DC-3 + DC-4 resolution (final deferred-candidate resolution point)

US-0117 is the **final story in the 5-story drain** and the **final deferred-candidate resolution point** for the architecture.md triad hygiene closure. It inherits 18 missing `# US-xxxx` h1 anchors from prior released stories AND owns 18 anchors for its own features (also missing — confirmed by grep in R-0105). Total h1 anchors added in THIS `/architecture` phase: **36** (18 own + 18 deferred).

- **DC-1** (5, from US-0113): US-0103, US-0104, US-0105, US-0107, US-0110 (sovereign-loop era family).
- **DC-2** (2, from US-0114): US-0041, US-0062 (release & distribution family).
- **DC-3** (7, from US-0115): US-0034, US-0084, US-0086, US-0093, US-0096, US-0101, US-0102 (integration & observability family).
- **DC-4** (4, from US-0116): US-0092, US-0095, US-0098, US-0099 (delivery & lifecycle family).
- **18 own** (US-0117 family): US-0069, US-0070, US-0071, US-0072, US-0075, US-0076, US-0077, US-0078, US-0079, US-0080, US-0081, US-0082, US-0083, US-0085, US-0087, US-0088, US-0089, US-0090.

**First time the architecture phase adds DC anchors** (prior 4 stories deferred them to US-0117). Resolution approach (Q-2 LOCKED in R-0105): add in `/architecture`, NOT `/execute` — keeps anchors as architecture artifacts per `docs/engineering/artifact-ownership-policy.md`. NOT appended to `handoffs/sovereign_deferrals.jsonl` — the anchors ARE being resolved in this phase. Each anchor is a minimal 3–5 line normative section; full architectural content for each feature remains in their original DEC / R-xxxx entries. Anchor format: `## US-xxxx — <feature title>` (matching existing `## US-0115` / `## US-0116` format). The 36 anchors are appended below this `## US-0117` section.

### Risks finalized

| Risk | Severity | Mitigation |
|------|----------|------------|
| **AC-3 byte-stability (5th-story cumulative surface — first 5-cumulative-surface story)** — US-0117 is the fifth story to extend `### Full scratchpad reference`; cumulative surface now covers 4 prior released blocks (US-0113 L1682 + US-0114 L1806 + US-0115 L1878 + US-0116 L2225). Risk of accidentally editing a prior released block. | **MEDIUM** | Net-new-keys-only (46 keys) + cross-link-pointer + reason-code-only (9) + prose-only (7) shape LOCKED in `/architecture` (T-003). Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2225 range (no removals/modifications to US-0113's L1682, US-0114's L1806, US-0115's L1878, or US-0116's L2225 blocks). QA re-verifies. Mirrors S0114 / S0115 / S0116 retrospective pattern extended to 5th story. |
| **AC-5 parity lockstep** — `template/its_magic/README.md` must be byte-identical to `its_magic/README.md`. | **MEDIUM** | T-004 one-way copy + `PARITY_OK <size> <size>` byte-parity check. |
| **AC-7 anchor gaps + labeling ambiguities** — 18 features; two labeling corrections (US-0082 = Codebase map; US-0090 = Caveman input compression) + one US-id collision (runbook `## Caveman mode (US-0089)` L2032 vs 18-feature family US-0089 = Auto orchestration). | **MEDIUM** | R-0105 closed all anchor gaps (all 18 features have verified runbook anchors). Labeling corrections LOCKED in T-002. US-0089 title resolution LOCKED: `#### US-0089` subsection = "Auto orchestration" (NOT "Caveman mode"). |
| **AC-8 regression tests** — coverage parity contract tests weakened or failing. | **LOW–MEDIUM** | US-0117 is documentation-only; **forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` in execute-phase. If a test fails, fix prose, never relax test. T-006 confirms green. |
| **DC anchor resolution (first-time in `/architecture`)** — 36 h1 anchors + `# US-0117` to add in `/architecture`; ~1670 lines post-addition, under 3000-line cap. | **MEDIUM** | T-anch adds all 36 anchors in `/execute` (task seeded HERE, executed in build+verify macro). Architecture phase authors the `# US-0117` section + the 36 anchor stubs (appended below) as the normative contract; execute-phase materializes them in `architecture.md` if not already present. **Mitigation**: anchors appended in THIS phase (resolved here, not deferred further). |
| **AC-2 18-subsection scope size** — 2–4x prior stories' T-002 load. | **MEDIUM** | Keep T-002 as a single task with 18 subsections (mirror prior stories' pattern; dev subagent can handle 18 subsections — it's documentation, not code). Split only if dev subagent progress stalls. |
| **AC-4 encoding hygiene prerequisite (carried from US-0114)** — 185 stray `0xa7` (section sign) bytes in working-tree `docs/product/backlog.md` per R-0102 / R-0103 / R-0104 / R-0105. | **MEDIUM (carried)** | `/architecture` makes no backlog.md edits. Flag to orchestrator: restore backlog.md encoding hygiene before execute so AC-4 can be re-verified post-execute. NOT a US-0117 blocker (research + architecture are read-only on backlog.md). |
| **US-0087 key surface size** — 18 net-new key rows (largest in family). | **MEDIUM** | Angle boundary with US-0088 / US-0092 (US-0116 family, cross-link only) explicit. T-003 groups US-0087 keys under one sub-heading. |
| **Decomposition drift** — Drain mutex (US-0117 is the last story; no successor in this drain). | **LOW** | Bounded by angle-distinct narrative contract; US-0117 owns phase & role governance feature operator guides only. |

### Stop conditions met

- **No DEC required** — confirmed (US-0117 documentation-only; mirrors US-0113 / US-0114 / US-0115 / US-0116 sibling precedent; grep `^## DEC-` returned no matches).
- **No feasibility unknown** — R-0105 closed all 8 spec open questions (Q1–Q8); AC-3 approach locked; DC resolution approach locked (Q-2); key surface resolved via scratchpad grep (Q-3); 5th-story byte-stability contract locked (Q-8).
- **No data migration risk** — US-0117 is documentation-only; no schema, installer, or canonical-file migration.

**No DECISION_GATE raised.** Architecture phase revealed no question requiring operator input. DC-1+DC-2+DC-3+DC-4 resolved by tech-lead within the `plan` macro (36 h1 anchors added in THIS phase). No sovereign-memory digest call needed (US-0117 is documentation-only; existing digest context sufficient per R-0105 — S0113 / S0114 / S0115 / S0116 retrospectives established the reusable patterns applied here; the cross-link pointer pattern + angle-distinct narrative pattern + cross-story byte-stability contract now form a quad scaled to the 5th story). Verdict: **PASS**.

### Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called (US-0117 documentation-only; existing digest context sufficient per R-0105). Sovereign-loop pattern for curator retrospective at segment close: "phase & role governance family operator documentation completes the US-0113 / US-0114 / US-0115 / US-0116 / US-0117 umbrella quint under `## Commands and workflow`; cross-story byte-stability contract now covers **four** prior released blocks (US-0113 L1682 + US-0114 L1806 + US-0115 L1878 + US-0116 L2225) — net-new-keys-only + cross-link-pointer + reason-code-only + prose-only shape is the established quint-closure pattern; US-0117 is the first 5-cumulative-surface story and the final deferred-candidate resolution point (36 architecture.md h1 anchors added). No write to `mistakes.jsonl` in architecture phase.

### Consequences

- Sprint: S0117 (pending `/sprint-plan`).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.
- Framework README pair grows by umbrella + 18 subsections + scratchpad reference extension (both `its_magic/README.md` and `template/its_magic/README.md` byte-identical).
- **36 architecture.md h1 anchors RESOLVED in this phase** (18 own + 18 deferred DC-1+DC-2+DC-3+DC-4) — final deferred-candidate resolution point. Appended below.
- No new tests; no new DECs; no compose-surface changes.

### Evidence references

- `docs/product/backlog.md` — `## US-0117` block (lines 3965–3981, 8 ACs)
- `docs/engineering/research.md` — `R-0105` (delivered 2026-07-04T16:54:35Z, 8/8 open questions closed; 18 per-feature sub-findings; AC-3 approach locked; DC-1..DC-4 confirmed = 36 total; AC baselines green; deepened risks)
- `handoffs/po_to_tl.md` — research handoff (topmost block) + spec handoff
- `docs/engineering/state.md` — research checkpoint (latest) + architecture checkpoint (this phase, appended)
- `handoffs/resume_brief.md` — top block updated to reflect architecture complete
- `.cursor/scratchpad.md` — phase & role governance keys (L21/L89–91 role overrides, L102–105 phase plan, L77–80 bug queue, L11–22 auto loop, L30–38 full-autonomy, L41–56 backlog drain, L63 active, L135 orchestration, L201 release publish, L295–298 dev auto-launch) — canonical source for AC-3 extension (net-new + cross-links)
- `its_magic/README.md` — L350 (`## Commands and workflow`) umbrella target; L940 (US-0113 sibling umbrella — byte-stability preserved); L1225 (US-0114 sibling umbrella — byte-stability preserved); L1410 (US-0115 sibling umbrella — byte-stability preserved); L1665 (US-0116 sibling umbrella + `### Full scratchpad reference (detailed)` extension target); L1682 (US-0113 keys block — byte-stability preserved); L1806 (US-0114 keys block — byte-stability preserved + cross-link target for `DELIVERY_MODE`); L1878 (US-0115 keys block — byte-stability preserved + optional cross-link target for `LEAN_MEMORY_*`); L2225 (US-0116 keys block — byte-stability preserved + insertion point for `### Phase & role governance keys` sub-block); L880 / L909 / L2370 (pre-US-0117 grouped cross-link targets for `AUTO_BACKLOG_DRAIN` / `AUTO_BUG_QUEUE` family)
- `docs/engineering/runbook.md` — 18 anchors (per R-0105 § Per-feature sub-findings): US-0069 L1711 h2; US-0070 L1753 h2; US-0071 L303 h2; US-0072 L550 h2; US-0075 L1949 h3 + L2535 h2; US-0076 L63 h2; US-0077 L98 h2; US-0078 L479 h2; US-0079 L512 h2; US-0080 L550 h2 + L570 h3; US-0081 L2032 h3; US-0082 L63 h2; US-0083 L479 h2 + L591 h3; US-0085 L1628 h2; US-0087 L1809 h2 + L1958 h3; US-0088 L1838 h2; US-0089 L1398 h3 + L1838 h2; US-0090 L2099 h3
- `docs/engineering/architecture.md` — h1 inventory confirmed: `# US-0106` (L2), `# US-0108` (L120), `# US-0109` (L220), `# US-0111` (L335), `# US-0112` (L454), `# US-0113` (L717), `# US-0114` (L914), `## US-0115` (L1117), `## US-0116` (L1265) exist; `## US-0117` + 36 DC anchors added in THIS phase (appended below)
- `docs/engineering/decisions.md` — DEC-0051 (US-0069 phase-role), DEC-0052 (US-0070 phase plan), DEC-0053 (US-0071 metadata guard), DEC-0035 (US-0080 / US-0072 token profile), DEC-0039 / DEC-0057 (US-0075 scratchpad parity), DEC-0065 (US-0082 codebase map), DEC-0059 / DEC-0067 (US-0077 delegation), DEC-0060 (US-0078 env file), DEC-0061 (US-0079 bug queue), DEC-0073 (US-0090 caveman input compression), DEC-0029 (US-0085 fresh-context markers), DEC-0078 (US-0087 full-autonomy), DEC-0038 (runtime proof) — referenced, not amended; no US-0117 companion DEC (grep `^## DEC-` returned no matches)

### Isolation evidence (per US-0048 / DEC-0029)

Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to artifact files (narrow-read per US-0053 — research.md R-0105 entry only, po_to_tl.md top research handoff block, backlog.md US-0117 block L3965–3981, state.md US-0117 research checkpoint, resume_brief.md top ~30 lines, architecture.md grep US-0113..US-0117 + DC-1..DC-4 anchors, decisions.md grep `^## DEC-`). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python timestamp/hash computation. `assemble_sovereign_memory_digest(...)` NOT called (US-0117 documentation-only; existing digest context sufficient per R-0105). No write to `mistakes.jsonl` in architecture phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).

### Strict runtime proof (DEC-0038)

- **runtime_proof_id**: `rp-auto-20260704-01-architecture-techlead-20260704T171500Z-US-0117`
- **canonical_payload** (sorted-key JSON per DEC-0038): `{"approach_locked":"A1","companion_dec":"none","delivery_mode":"ultra_lean","dc_anchors_added":36,"macro_phase":"plan","orchestrator_run_id":"auto-20260704-01","phase_id":"architecture","proof_issued_at":"2026-07-04T17:15:00Z","proof_ttl_seconds":3600,"research_anchor":"R-0105","role":"tech-lead","story_id":"US-0117","verdict":"PASS"}`
- **proof_ttl**: 2026-07-04T18:15:00Z (1-hour TTL per DEC-0038)

---

### 36 DC anchors (appended below — minimal normative sections)

The following 36 `## US-xxxx` h1 anchors are added in THIS `/architecture` phase as the final deferred-candidate resolution. Each is a minimal 3–5 line normative section; full architectural content for each feature remains in their original DEC / R-xxxx entries. 18 own (US-0117 family) + 18 deferred (DC-1 from US-0113 + DC-2 from US-0114 + DC-3 from US-0115 + DC-4 from US-0116).

## US-0069 — Phase→role matrix

Story US-0069 — Phase→role matrix. Per-phase role admission + checkpoint validation + per-role override (`AUTO_ROLE_RESEARCH` / `AUTO_ROLE_PLAN_VERIFY` / `AUTO_ROLE_REFRESH_CONTEXT`). Fail-closed on mismatch. See `# US-0117` for the operator documentation angle. Binding: DEC-0051; runbook `## Strict /auto phase→role enforcement (US-0069 / DEC-0051)` L1711 h2.

## US-0070 — Phase selection policy

Story US-0070 — Phase selection policy. Resolved ordered phase plan via `AUTO_PHASE_PLAN` / `AUTO_PHASE_EXCLUDE` / `AUTO_PHASE_INCLUDE` / `AUTO_PHASE_PROFILE`; exactly-one-active-mode after merge; conflict -> fail closed (`PHASE_POLICY_CONFLICT` / `PHASE_PLAN_UNKNOWN_PHASE`). See `# US-0117`. Binding: DEC-0052; runbook `## Configurable /auto phase plan (US-0070 / DEC-0052)` L1753 h2.

## US-0071 — Metadata sanitization

Story US-0071 — Metadata sanitization. Validator gate (not a runtime toggle): `scripts/check-user-visible-metadata.py` forbids internal IDs (DEC-xxxx / R-xxxx / reason-codes) in user-visible prose; US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. See `# US-0117`. Binding: DEC-0053; runbook `## User-visible internal metadata guard (US-0071 / DEC-0053)` L303 h2.

## US-0072 — Context slimming

Story US-0072 — Context slimming. Concept of context compaction / token-cost control; runtime toggle is `TOKEN_PROFILE=lean|balanced|full` (DEC-0035, owned by US-0080) + `LEAN_MEMORY_*` family (DEC-0082, owned by US-0115). See `# US-0117`. Binding: DEC-0035; runbook `## Context compaction and token profile mode (US-0053 / DEC-0035)` L550 h2 (shared with US-0080).

## US-0075 — Scratchpad example-first refresh

Story US-0075 — Scratchpad example-first refresh. Parity-contract feature materialized via `tests/scratchpad_example_parity_test.py` + `installer.py materialize_scratchpad_example()`; canonical `.cursor/scratchpad.md` <-> `template/.cursor/scratchpad.local.example.md` byte-parity. See `# US-0117`. Binding: DEC-0039 / DEC-0057; runbook `### Scratchpad example parity` L1949 h3 + `## Scratchpad example upgrade contract (US-0057 / DEC-0039 / DEC-0057)` L2535 h2.

## US-0076 — Codebase map (freshness gate)

Story US-0076 — Codebase map freshness gate. Freshness gate on `docs/engineering/codebase-map.md`; runtime toggle `CODEBASE_MAP_REFRESH_ON_ROLLOVER=1` (default off) owned by US-0082's bootstrap-mechanism narrative. See `# US-0117` and `## US-0082`. Binding: DEC-0065; runbook `## Codebase map bootstrap (US-0082 / DEC-0065)` L63 h2 (shared with US-0082).

## US-0077 — Delegation policy

Story US-0077 — Delegation policy. Intake-evidence delegation path: `topic_coverage[].satisfied_by=delegation_ref` + required `delegation_scope` / `delegation_rationale` / `delegation_confidence`; fail-closed on missing/malformed (`INTAKE_DELEGATION_EVIDENCE_MISSING`). See `# US-0117`. Binding: DEC-0059 / DEC-0067; runbook `## Documentation profile validation (US-0077 / DEC-0059)` L98 h2.

## US-0078 — Env file bootstrap (intake evidence harness)

Story US-0078 — Env file bootstrap. Install-time copy-when-missing mechanism for intake-evidence env file; harness contract (validator + installer). See `# US-0117` and `## US-0083`. Binding: DEC-0060; runbook `## Interactive intake evidence validation (US-0078 / DEC-0060 / US-0083 / DEC-0067)` L479 h2 (shared with US-0083).

## US-0079 — Bug queue routing

Story US-0079 — Bug queue routing. Bug-targeted `/auto` via `AUTO_BUG_QUEUE` / `AUTO_BUG_TARGET` / `AUTO_BUG_MAX_ITEMS` / `AUTO_BUG_ON_BLOCK`; mutex vs `AUTO_BACKLOG_DRAIN` without bug-target argv; `AUTO_BUG_TARGET=all-open|BUG-####` required when `AUTO_BUG_QUEUE=1`. See `# US-0117`. Binding: DEC-0061; runbook `## Bug issues (US-0079 / DEC-0061)` L512 h2.

## US-0080 — Auto quiet mode

Story US-0080 — Auto quiet mode. `AUTO_QUIET=1` suppresses non-essential stdout; angle-distinct from `TOKEN_PROFILE` (US-0072 / US-0080 shared runbook anchor). See `# US-0117`. Binding: DEC-0035; runbook `## Context compaction and token profile mode (US-0053 / DEC-0035)` L550 h2 + `### Auto quiet mode` L570 h3.

## US-0081 — Caveman mode

Story US-0081 — Caveman mode. `CAVEMAN_MODE=1` / `CAVEMAN_LEVEL=<n>` engages compressed-output operator mode; `CAVEMAN_LEVEL_UNKNOWN` reason code on invalid level. See `# US-0117`. Binding: DEC-0073; runbook `## Caveman mode (US-0089)` L2032 h3 (note: runbook h2 uses US-0089 id colliding with US-0081 family — US-0081 owns the caveman-mode feature; US-0089 owns auto orchestration; `/architecture` locks the resolution).

## US-0082 — Codebase map (bootstrap mechanism)

Story US-0082 — Codebase map bootstrap mechanism. **Label correction**: authoritative label = "Codebase map" (per runbook L63 + DEC-0065; spec handoff's "Input compression" is a mislabel). `CODEBASE_MAP_REFRESH_ON_ROLLOVER=1` (default off) triggers `scripts/materialize_codebase_map.py` on rollover. See `# US-0117` and `## US-0076`. Binding: DEC-0065; runbook `## Codebase map bootstrap (US-0082 / DEC-0065)` L63 h2.

## US-0083 — Scratchpad delivery keys

Story US-0083 — Scratchpad delivery keys. `AUTO_DELIVERY_ROUTING` net-new key + cross-link to US-0114 for `DELIVERY_MODE` + `DELIVERY_MODE_SWITCH_MID_STORY` reason code. See `# US-0117` and `## US-0078`. Binding: DEC-0067 / DEC-0060; runbook `## Interactive intake evidence validation (US-0078 / DEC-0060 / US-0083 / DEC-0067)` L479 h2 + `### Scratchpad delivery keys` L591 h3.

## US-0085 — Context fresh-context markers

Story US-0085 — Context fresh-context markers. `fresh_context_marker` is an isolation-evidence field (not a runtime toggle); `PHASE_CONTEXT_ISOLATION_MISSING` reason code on missing marker. See `# US-0117`. Binding: DEC-0029; runbook `## Phase-context isolation (US-0048 / DEC-0029)` L1628 h2.

## US-0087 — Full-autonomy mode

Story US-0087 — Full-autonomy mode. 18 net-new key rows (largest in family): `AUTO_FLOW_MODE` / `AUTO_IMPLEMENTATION_LOOP` / `AUTO_LOOP_MAX_CYCLES` / `AUTO_BLOCK_RETRY_MAX` / `RELEASE_PUBLISH_MODE` / `CROSS_MODEL_REVIEW` / `CROSS_MODEL_ANTISLOP_THRESHOLD` / `CROSS_MODEL_REWORK_MAX` / `SOVEREIGN_MEMORY` + family (5) / `AUTO_SOVEREIGN` + family (4) / `SOVEREIGN_GOAL_MODE` + `BLOCK_RETRY_CAP_EXHAUSTED` / `NATIVE_CHAIN_UNAVAILABLE` reason codes. See `# US-0117`. Binding: DEC-0078; runbook `## Full-autonomy mode (US-0087 / DEC-0078)` L1809 h2 + `### Full-autonomy interaction` L1958 h3.

## US-0088 — Automation modes

Story US-0088 — Automation modes. 9 net-new keys: `AUTO_BACKLOG_DRAIN` / `AUTO_BACKLOG_MAX_STORIES` / `AUTO_BACKLOG_ON_BLOCK` / `AUTO_STORY_SELECTION` / `AUTO_EXECUTE_BULK` / `AUTO_EXECUTE_MAX_ITEMS` / `AUTO_EXECUTE_ON_BLOCK` / `AUTO_EXECUTE_SELECTION` / `AUTO_TEAM_SCOPE_ENFORCE` + `BLOCK_RETRY_CAP_EXHAUSTED` reason code. See `# US-0117`. Binding: DEC-0078; runbook `## Automation modes (US-0088)` L1838 h2.

## US-0089 — Auto orchestration

Story US-0089 — Auto orchestration. **US-id collision resolution**: authoritative label = "Auto orchestration" (per scratchpad L21/L135 + 18-feature family; runbook h2 `## Caveman mode (US-0089)` L2032 is a US-id collision — US-0089 in the 18-feature family is Auto orchestration, NOT Caveman mode). 2 net-new keys: `AUTO_PAUSE_REQUEST` / `AUTO_REMOTE_AUTOMATION_PROFILE`. See `# US-0117`. Binding: DEC-0078; runbook `### Auto orchestration` L1398 h3 + `## Automation modes (US-0088)` L1838 h2.

## US-0090 — Caveman input compression

Story US-0090 — Caveman input compression. **Label correction**: authoritative label = "Caveman input compression" (per runbook L2099 + DEC-0073; spec handoff's "Phase governance integration" is a mislabel — "phase governance integration" is the umbrella's introductory framing AC-1, not a separate `#### US-0090` subsection). 2 net-new keys: `CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE` + `CAVEMAN_COMPRESS_SCOPE_EMPTY` reason code. See `# US-0117`. Binding: DEC-0073; runbook `### Caveman input compression` L2099 h3.

## US-0103 — Sovereign loop ledger (DC-1, from US-0113)

Story US-0103 — Sovereign loop ledger. Append-only sovereign-loop event log (`sovereign_loop_lib.py` advance/drain-generate/notification); default-off `AUTO_SOVEREIGN` (US-0107) composes on this. See `# US-0113`. Binding: DEC-0103; research R-0089.

## US-0104 — Cross-model critic (DC-1, from US-0113)

Story US-0104 — Cross-model critic. `CROSS_MODEL_REVIEW` / `CROSS_MODEL_ANTISLOP_THRESHOLD` / `CROSS_MODEL_REWORK_MAX` keys; cross-model review dispatch with antislop threshold + bounded rework. See `# US-0113`. Binding: DEC-0104; research R-0092.

## US-0105 — Convergence gate (DC-1, from US-0113)

Story US-0105 — Convergence gate. `evaluate_convergence` five-conjunct gate + `goal_progress` emission; composes on US-0103 ledger. See `# US-0113`. Binding: DEC-0105; research R-0093.

## US-0107 — Sovereign loop mode (DC-1, from US-0113)

Story US-0107 — Sovereign loop mode. Default-off `AUTO_SOVEREIGN` orchestrates sovereign-loop advance/drain-generate/notification; fail-closed goal-mode coupling; deferral JSONL v1 + validator. See `# US-0113`. Binding: DEC-0107; research R-0094.

## US-0110 — Goal-based convergence loops (DC-1, from US-0113)

Story US-0110 — Goal-based convergence loops. Five-conjunct `evaluate_convergence`, `goal_progress` emission, partial-delivery report; composes on US-0103 / US-0105. See `# US-0113`. Binding: DEC-0110; research R-0091.

## US-0041 — Release notes derivation (DC-2, from US-0114)

Story US-0041 — Release notes derivation. Atomic `[Unreleased] -> [semver]` promotion via `release_changelog_lib.promote_unreleased()`; release-trigger-driven changelog derivation. See `# US-0114`. Binding: DEC-0041.

## US-0062 — Sync policy + auto-push allowlist (DC-2, from US-0114)

Story US-0062 — Sync policy + auto-push allowlist. `SYNC_POLICY_MODE=disabled` (DEC-0018 default); `AUTO_PUSH_BRANCH_ALLOWLIST` gated sync; release-publish-mode contract. See `# US-0114`. Binding: DEC-0062 / DEC-0018.

## US-0034 — Cross-repo compatibility observability (DC-3, from US-0115)

Story US-0034 — Cross-repo compatibility observability. Monitored sources, manifest contract boundaries, compatibility signal taxonomy, critical-gate policy (`COMPATIBILITY_GATE_ON_CRITICAL`). Default-off (`CROSS_REPO_OBSERVABILITY=0`). See `# US-0115`. Binding: DEC-0034.

## US-0084 — Codebase map freshness gate (DC-3, from US-0115)

Story US-0084 — Codebase map freshness gate. Freshness gate on `docs/engineering/codebase-map.md`; `CODEBASE_MAP_REFRESH_ON_ROLLOVER` default off. See `# US-0115` and `## US-0082`. Binding: DEC-0065.

## US-0086 — Handoff hygiene validator (DC-3, from US-0115)

Story US-0086 — Handoff hygiene validator. `scripts/check_handoff_hygiene.py` validates handoff files against schema; fail-closed on missing/malformed. See `# US-0115`. Binding: DEC-0086.

## US-0093 — Scratchpad drift detector (DC-3, from US-0115)

Story US-0093 — Scratchpad drift detector. Detects drift between canonical `.cursor/scratchpad.md` and framework example; validator gate. See `# US-0115`. Binding: DEC-0093.

## US-0096 — Active context handoff / lean memory (DC-3, from US-0115)

Story US-0096 — Active context handoff. `LEAN_MEMORY_*` family (DEC-0082) for memory-layer mechanics; delivery-mode-aware handoff shape. See `# US-0115`. Binding: DEC-0082.

## US-0101 — Model tier resolution (DC-3, from US-0115)

Story US-0101 — Model tier resolution. Resolves model tier per role + delivery mode; composes on US-0102 catalog. See `# US-0115`. Binding: DEC-0101.

## US-0102 — Role-based model catalog (DC-3, from US-0115)

Story US-0102 — Role-based model catalog. Role-based model catalog presets shipped on install/upgrade (US-0112); `model-catalog.local.example.*.json` framework files. See `# US-0115`. Binding: DEC-0102.

## US-0092 — Delivery confirmation gate / full-autonomy outer driver (DC-4, from US-0116)

Story US-0092 — Delivery confirmation gate. Full-autonomy outer driver + security posture; delivery confirmation gate at end of drain. See `# US-0116`. Binding: DEC-0078.

## US-0095 — Native in-chat auto-chain (DC-4, from US-0116)

Story US-0095 — Native in-chat auto-chain. Native in-chat auto-chain continuation; orchestrator continuation contract. See `# US-0116`. Binding: DEC-0080 / DEC-0081.

## US-0098 — Dev environment auto-launch (DC-4, from US-0116)

Story US-0098 — Dev environment auto-launch. `DEV_AUTO_LAUNCH_PROFILE` / `DEV_ENVIRONMENT_CONFIG` keys; execute-phase runtime gate (default-off). See `# US-0116`. Binding: DEC-0084.

## US-0099 — Dev-environment copy-when-missing bootstrap (DC-4, from US-0116)

Story US-0099 — Dev-environment copy-when-missing bootstrap. Install-time bootstrap (copy-when-missing, runs only on `missing` / `upgrade` / `postinstall`); `DEV_ENV_BOOTSTRAP_*` family + `DEV_ENV_PROFILE_MISSING` reason codes. See `# US-0116`. Binding: DEC-0084.


## US-0118 — Work-kind classification + tiered delivery routing per story

### Overview

**US-0118** is the first **code-bearing** story in the new drain (US-0113..US-0117 were documentation-only). It introduces a deterministic **per-story work-kind classifier** `scripts/work_kind_classify_lib.py:classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope) -> WorkKindClassification` returning `work_kind ∈ {doc, mini, code}` + `recommended_delivery_mode ∈ {standard, ultra_lean, mega_quick}` + `recommended_phase_plan` (list of canonical phase ids) + `rationale` + `evidence_refs` (+ optional `rule_trace` via `--explain`). Gated by a new default-off scratchpad flag `WORK_KIND_ROUTING=0|1` (zero overhead when off — early-return in `/auto` `resolve_delivery_mode` step 0 + `/intake` step 5 skip when `WORK_KIND_ROUTING != "1"`). Backlog rows gain optional `work_kind` + `recommended_delivery_mode` fields set at intake (operator accept/override; recorded in intake evidence bundle per US-0078 / DEC-0060). `/auto` `resolve_delivery_mode` step 0 consumes them when `DELIVERY_MODE`/`AUTO_PHASE_*` are unset (L8 precedence: explicit `DELIVERY_MODE` > explicit `AUTO_PHASE_*` > `WORK_KIND_ROUTING`-derived > current default; `start-from` always wins). `doc` → `[intake, execute, release]`; `mini` → `ultra_lean` or `mega_quick` (US-0096 eligibility); `code` → `standard`. Reuses `scripts/dev_environment_lib.py:classify_touched_files()` (tier A/B/C + `TIER_C_SKIP_PREFIXES`) — import, do not reinvent (Q9 LOCKED). Deterministic pure-stdlib, no LLM, no network, no `.env` reads (Q3 LOCKED). Four `WORK_KIND_*` reason codes (Q2 LOCKED). 12 `test_us0118_*` contract test markers (Q4 LOCKED). New `### Work-kind routing keys (US-0118)` README sub-block (Q5 LOCKED — 6th sibling; README edits happen in `/execute`, NOT here) + new `## Work-kind routing (US-0118)` runbook h2 (Q7 LOCKED). Triple-installer parity (Q10/installer manifest).

**Binding decision**: **companion_dec=DEC-0118** (Required → Accepted; authored in THIS phase). US-0118 introduces a new routing primitive — DEC-0118 locks: (a) the work-kind enumeration decision (`doc`/`mini`/`code` 3-tier; alternatives: 2-tier doc/non-doc collapsed — rejected as too coarse; 4-tier doc/mini/standard/extended — rejected as over-engineered), (b) the L8 precedence chain (explicit operator flags always win; classifier fills only the unset case), (c) the `dev_environment_lib.classify_touched_files` reuse boundary (import, not rewrite — Q9 LOCKED), (d) the zero-overhead-when-off contract (default `WORK_KIND_ROUTING=0`). Mirrors DEC-0082 (US-0096 delivery modes) / DEC-0052 (US-0070 phase selection) precedent. **Research anchor**: **R-0106** (delivered 2026-07-04T20:00:00Z, 10/10 open questions Q1..Q10 closed LOCKED; architecture seeds T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; AC baselines green; risks R1..R8 finalized). **Compose guards (non-negotiable, 23 — UNCHANGED, cumulative across all prior stories — same 23 as US-0117)**: US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062. **Status authority**: **OPEN** per **US-0045** (closure at `/release`).

**Fresh context marker**: `tl-US0118-architecture-20260704T203000Z-fresh`
**Orchestrator run id**: `auto-20260704-01`
**Timestamp**: 2026-07-04T20:30:00Z (UTC)
**Verdict**: PASS
**Next**: `/sprint-plan`


### Companion DEC

**companion_dec = DEC-0118** (Required → Accepted; authored in THIS phase at `decisions/DEC-0118.md`). US-0118 introduces a new routing primitive (per-story work-kind classifier) with a precedence-chain tradeoff (L8: explicit `DELIVERY_MODE` > explicit `AUTO_PHASE_*` > `WORK_KIND_ROUTING`-derived > current default) and a work-kind enumeration tradeoff (`doc`/`mini`/`code` 3-tier vs alternative 2-tier or 4-tier schemes). Mirrors DEC-0082 (US-0096 delivery modes) / DEC-0052 (US-0070 phase selection) precedent: a new routing primitive gets a companion DEC locking the precedence chain + enumeration choice + reuse boundary + zero-overhead-when-off contract. The DC-1+DC-2+DC-3+DC-4 resolution (36 h1 anchors) was already performed in US-0117's `/architecture` phase (final deferred-candidate resolution point) — US-0118 inherits a clean deferral register. See `decisions/DEC-0118.md` for the decision body.

### Approach locked (A1)

**Approach A1** (locked): Single `### Work-kind routing (US-0118)` umbrella section + per-feature subsections + 6th scratchpad ref sub-block `### Work-kind routing keys (US-0118)` as a sibling to the US-0113..US-0117 sub-blocks (US-0113 L2421, US-0114 L2545, US-0115 L2617, US-0116 L2765, US-0117 L2856). US-0118 is the **6th-story cumulative byte-stability surface** — first 6-cumulative-surface story. Prior 5 released blocks (US-0113..US-0117) must remain byte-identical between `its_magic/README.md` and `template/its_magic/README.md`; US-0118 adds net-new-keys-only + cross-link-pointers + reason-code-only entries to its own 6th sub-block, never edits prior released blocks. README edits happen in `/execute` (build+verify macro), NOT here — this phase only PROPOSES the sub-block name + cross-link targets in prose.

| Option | Summary | Verdict |
|--------|---------|---------|
| **A1** | **Single `### Work-kind routing (US-0118)` umbrella + per-feature subsections + 6th scratchpad ref sub-block** (net-new keys + cross-link pointers + reason-code-only) | **Preferred** — matches US-0113 / US-0114 / US-0115 / US-0116 / US-0117 sibling precedent (6th sibling); preserves byte-stability of prior 5 released blocks. |
| A2 (rejected) | Extend `### Delivery & lifecycle keys` (US-0116) sub-block with `WORK_KIND_ROUTING` key. | **Rejected** — breaks US-0116's byte-stability (released block in S0116); Q5 LOCKED rejected this alternative explicitly. |
| A3 (rejected) | 2-tier work-kind enumeration (`doc`/`non-doc`) collapsed; or 4-tier (`doc`/`mini`/`standard`/`extended`). | **Rejected** — 2-tier too coarse (conflates `mini` and `code`); 4-tier over-engineered (no operator demand for `extended`); 3-tier mirrors `dev_environment_lib.classify_touched_files` tier A/B/C precedent. |


### Files to touch

- `scripts/work_kind_classify_lib.py` — **NEW**. Pure-stdlib classifier exposing `classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope) -> WorkKindClassification` dataclass (Q10 LOCKED signature). Implements doc/mini/code rules per L5/L6/L7 + Q1 tie-break (highest tier wins). `--explain` flag emits `rule_trace` (Q3). `--self-test` exits 0 (AC-12). Imports `TIER_C_SKIP_PREFIXES` + `classify_touched_files` from `dev_environment_lib` (Q9 LOCKED import contract — no duplication).
- `scripts/installer.py` (or `/auto` orchestrator) — `resolve_delivery_mode` step 0 minimal hook (early-return when `WORK_KIND_ROUTING != "1"`; precedence clause per L8). T-004.
- `its_magic/README.md` — **NEW** `### Work-kind routing (US-0118)` umbrella section + per-feature subsections + `### Work-kind routing keys (US-0118)` 6th scratchpad ref sub-block (Q5 LOCKED — 6th sibling; net-new keys + cross-link pointers + reason-code-only; never edits prior US-0113..US-0117 blocks). T-007. (Edits happen in `/execute`, NOT here.)
- `template/its_magic/README.md` — one-way byte-sync of `its_magic/README.md`. T-007/T-004.
- `tests/us0118_contract_test.py` (or `tests/work_kind_classify_test.py` per R-0106) — **NEW**. 12 `test_us0118_*` markers (Q4 LOCKED). T-006.
- `docs/engineering/runbook.md` — **NEW** `## Work-kind routing (US-0118)` h2 cross-link section (Q7 LOCKED). Content: `WORK_KIND_ROUTING` flag, L8 precedence, operator recipe (force full lifecycle on `doc` story via `DELIVERY_MODE=standard`), `--explain` usage, four `WORK_KIND_*` reason codes. T-008.
- `template/docs/engineering/runbook.md` — parity one-way copy of runbook h2.
- `.cursor/scratchpad.md` — **NEW** `WORK_KIND_ROUTING=0` key (default off) + `WORK_KIND_*` reason-code family (example scratchpad only — canonical scratchpad edits deferred to `/execute`). T-002.
- `template/.cursor/scratchpad.local.example.md` — mirror of `WORK_KIND_ROUTING` row.
- `.cursor/commands/auto.md` — `resolve_delivery_mode` step-0 precedence clause (L8 chain). T-002/T-004.
- `.cursor/commands/intake.md` — step-5 classifier hook (after ACs drafted, after US-0051 decomposition evaluator, before persistence). T-003.
- `template/.cursor/commands/auto.md` + `template/.cursor/commands/intake.md` — parity one-way copy (when template mirrors commands).
- `handoffs/intake_evidence/*.json` — schema extension: 3 new optional fields `work_kind`, `recommended_delivery_mode`, `work_kind_operator_decision ∈ {accept, override}` (Q9 LOCKED). T-003.
- `installer-owned-paths.manifest` — `[install_include_paths]` rows for `scripts/work_kind_classify_lib.py` + `template/scripts/work_kind_classify_lib.py`. T-009.
- `scripts/check_intake_template_parity.py` — `WORK_KIND_ROUTING_PAIRS` manifest constant + `--scope=work-kind-routing` flag (Q6 LOCKED). T-009.
- `decisions/DEC-0118.md` — **NEW** companion DEC (authored in THIS phase).
- `docs/engineering/architecture.md` — **this `## US-0118` section** (T-anch; authored in THIS phase).

### Files NOT to touch

- `docs/product/backlog.md` — US-0045 status authority; release-only. (US-0118 remains OPEN until `/release`. Backlog row fields `work_kind` / `recommended_delivery_mode` are added per-story at intake time only when `WORK_KIND_ROUTING=1` and operator accepts — this is a schema extension, NOT a bulk edit of existing rows. No forced reclassification of existing rows.)
- `docs/product/acceptance.md` — release-only.
- Prior-released US-0113..US-0117 README blocks (`### Sovereign-loop era` L940 + `### Sovereign-loop era keys` L2421 / `### Release & distribution` L1225 + `### Release & distribution keys` L2545 / `### Integration & observability` L1410 + `### Integration & observability keys` L2617 / `### Delivery & lifecycle` L1665 + `### Delivery & lifecycle keys` L2765 / `### Phase & role governance` + `### Phase & role governance keys` L2856) in `its_magic/README.md` — **byte-stability contract** (all 5 already released in S0113..S0117). US-0118 adds cross-link pointers to these blocks from its own 6th sub-block; it never edits them. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2856 range (no removals/modifications to US-0113's L2421, US-0114's L2545, US-0115's L2617, US-0116's L2765, or US-0117's L2856 blocks).
- `scripts/sovereign_loop_lib.py` — compose-do-not-amend (US-0103 read-only consumer).
- `scripts/sovereign_convergence_lib.py` — compose-do-not-amend (US-0105 read-only consumer).
- `scripts/dev_environment_lib.py` — **REUSE only — do not modify**. Import `classify_touched_files` + `TIER_C_SKIP_PREFIXES` from `dev_environment_lib` (Q9 LOCKED import contract). Contract test `test_us0118_classify_touched_files_reuse` enforces the import boundary.
- `tests/scratchpad_example_parity_test.py` — AC-8 regression baseline; forbid edits.
- Compose-guard stories (23 — US-0091, US-0097, US-0017, US-0040, US-0100..US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062) — read-only consumers; additive-only.


### Sprint seeds (T-anch + T-001..T-009 — 10 tasks within SPRINT_MAX_TASKS=12)

| Task | AC | Description | Role |
|------|----|-------------|------|
| **T-anch** | AC-10 | Add `## US-0118` h1 anchor to `docs/engineering/architecture.md` (per US-0118 h1-anchor policy; mirrors `## US-0113`..`## US-0117` format). Verify compose-do-not-amend: US-0096, US-0070, US-0078, US-0051, US-0069, US-0103 surfaces remain read-only (no edits to their architecture sections). Lock the import contract for `dev_environment_lib.classify_touched_files` reuse (Q9 boundary). | B |
| **T-001** | AC-1 / AC-2 | Create `scripts/work_kind_classify_lib.py` exposing `classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope) -> WorkKindClassification` per Q10 signature. Pure stdlib; import `TIER_C_SKIP_PREFIXES` + `classify_touched_files` from `dev_environment_lib` (no duplication — Q9). Implement the three rules (doc/mini/code) per L5/L6/L7 + Q1 tie-break (highest tier wins). Implement `--explain` flag emitting `rule_trace` (Q3). Implement `--self-test` (AC-12) exiting 0. | B |
| **T-002** | AC-3 / AC-6 | Add `WORK_KIND_ROUTING=0` (default off) to `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` with merge-precedence note (US-0078 model B: local > materialized baseline > example). Document the L8 precedence chain in `.cursor/commands/auto.md` `resolve_delivery_mode` step 0. (README scratchpad reference sub-block `### Work-kind routing keys (US-0118)` is added in T-007, not here.) | B |
| **T-003** | AC-4 / AC-5 | Extend `/intake` step 5 to run the classifier when `WORK_KIND_ROUTING=1` (after ACs drafted, after US-0051 decomposition evaluator, before persistence). Present `work_kind` + `recommended_delivery_mode` to operator for accept/override (Q9). Persist choice in backlog row (`- work_kind`, `- recommended_delivery_mode`) + intake evidence bundle (`work_kind`, `recommended_delivery_mode`, `work_kind_operator_decision`). US-0078 evidence gate still runs before any backlog/acceptance write. | B |
| **T-004** | AC-6 | `/auto` `resolve_delivery_mode` step-0 integration: add precedence clause to `.cursor/commands/auto.md`: when `WORK_KIND_ROUTING=1` AND backlog row carries `work_kind` AND `DELIVERY_MODE` unset AND `AUTO_PHASE_*` unset → derive `resolved_phase_plan` from `recommended_delivery_mode`. Explicit `DELIVERY_MODE` / `AUTO_PHASE_*` / `start-from` always win (L8). Early-return when `WORK_KIND_ROUTING != "1"` (zero overhead — Q8). | B |
| **T-005** | AC-7 | Emit the four `WORK_KIND_*` reason codes (Q2) with remediation prose in `sprints/Sxxxx/qa-findings.md` / `release-findings.md`. `WORK_KIND_ROUTING_DISABLED` is info-only (not fail-closed); the other three are fail-closed. | B |
| **T-006** | AC-9 | Create `tests/work_kind_classify_test.py` (or `tests/us0118_contract_test.py`) with the 12 `test_us0118_*` markers enumerated in Q4. Active + `template/` parity for the new script + scratchpad lines. | B |
| **T-007** | AC-3 | Add `### Work-kind routing keys (US-0118)` sub-block to `its_magic/README.md` `### Full scratchpad reference (detailed)` (after the US-0117 `### Phase & role governance keys` block L2856) — documents `WORK_KIND_ROUTING` key + four reason codes + cross-link pointer to `### Release & distribution keys` for `DELIVERY_MODE` precedence. One-way copy to `template/its_magic/README.md`. Verify `PARITY_OK <size> <size>`. (README edits happen in `/execute`, not `/architecture`.) | B |
| **T-008** | AC-11 | Append `## Work-kind routing (US-0118)` h2 to `docs/engineering/runbook.md` (Q7) + `template/docs/engineering/runbook.md` parity. Content: `WORK_KIND_ROUTING` flag, L8 precedence, operator recipe (force full lifecycle on `doc` story via `DELIVERY_MODE=standard`), `--explain` usage, four reason codes. | B |
| **T-009** | AC-9 / AC-12 | Add `tests/work_kind_classify_test.py` to the active test suite; verify 4-prior pytest still green. Add `scripts/work_kind_classify_lib.py` + `template/scripts/work_kind_classify_lib.py` to `installer-owned-paths.manifest` `[install_include_paths]` (Q10/installer parity — triple-installer PS1/Bash/Python ships the new script). Add `WORK_KIND_ROUTING_PAIRS` to `scripts/check_intake_template_parity.py` + `--scope=work-kind-routing` flag (Q6). | B |

**Execution order**: T-anch → T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 → T-008 → T-009. Acyclic. (T-anch first because it is on `architecture.md`, not `its_magic/README.md` — keeps the README byte-stability surface clean for T-001..T-007.)

**Total task seeds: 10 (T-anch + T-001..T-009) — within `SPRINT_MAX_TASKS=12`.** `/sprint-plan` may merge or split within the 12-task budget.


### Test markers (12 — from R-0106 Q4 LOCKED)

`test_us0118_doc_kind_routes_to_lean_plan`, `test_us0118_mini_kind_routes_to_ultra_lean`, `test_us0118_mini_kind_routes_to_mega_quick_when_eligible`, `test_us0118_code_kind_routes_to_standard`, `test_us0118_explicit_delivery_mode_wins_over_work_kind`, `test_us0118_auto_phase_wins_over_work_kind`, `test_us0118_routing_off_is_noop`, `test_us0118_classify_touched_files_reuse`, `test_us0118_intake_evidence_records_work_kind`, `test_us0118_reason_codes_preserved`, `test_us0118_default_off_zero_overhead`, `test_us0118_explain_emits_rule_trace` (in `tests/work_kind_classify_test.py` per R-0106 Q4; or `tests/us0118_contract_test.py` — name finalized in `/sprint-plan`).

Plus the regression baseline marker: `tests/scratchpad_example_parity_test.py` (4 tests — BUG-0013 parity baseline; do not weaken).

### Compose guards UNCHANGED (23 cumulative — same 23 as US-0117)

US-0118 is a code-bearing story but lives entirely **additive** to the compose surface — it adds a new flag (`WORK_KIND_ROUTING`), a new lib (`work_kind_classify_lib.py`), new backlog row fields, a new precedence clause, a new README sub-block, and a new runbook h2. It does **not** amend any existing compose-surface feature. The 23 compose guards (cumulative across all prior stories — US-0118 adds no new family-internal guards because US-0118 is itself a single-feature story, not a family umbrella) remain UNCHANGED:

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062.

**Does US-0118 itself become a NEW compose guard?** **NO.** US-0118 is a **routing primitive**, not a compose-surface guard. The 6 read-only compose consumers (US-0096 / US-0070 / US-0078 / US-0051 / US-0069 / US-0103) consume US-0118's output; they are not amended by it. Adding US-0118 to the compose-guard list would conflate a routing primitive with a guard — rejected. US-0118's contract is enforced by its own 12 `test_us0118_*` markers + the `WORK_KIND_ROUTING=0` zero-overhead-when-off contract (test `test_us0118_default_off_zero_overhead`).

### DC (deferred-candidate) resolution

`dc_check=clean`. `grep "^## US-0118" docs/engineering/architecture.md` prior to this phase → **no matches**. The `## US-0118` h1 anchor is **added in THIS `/architecture` phase** (per R-0105 Q-2 LOCKED pattern — architecture artifacts live in `architecture.md`, not in `/execute`; T-anch in the sprint seeds is the resolution point). 

Cross-check against the full US-xxxx list in `docs/product/backlog.md`: no OTHER deferred `## US-xxxx` anchors remain unresolved. US-0117 was the **final deferred-candidate resolution point** (36 `## US-xxxx` h1 anchors added in US-0117's `/architecture` phase — 18 own + 18 deferred DC-1..DC-4); the deferral register is clean. US-0118 inherits no DC candidates from prior stories. No new DC candidates are created by US-0118 (its own `## US-0118` anchor is resolved HERE, not deferred). Deferral register remains clean — no carry-over to a successor story.

### Compose, do not amend (verification — read-only consumers of US-0118)

| Story | README anchor | architecture.md anchor | Verification |
|-------|---------------|------------------------|--------------|
| US-0096 / DEC-0082 (delivery modes) | L2617 `### Integration & observability keys` (DELIVERY_MODE cross-link) + L2670 inline ref | `## US-0096` L1684 | ✓ exists — explicit `DELIVERY_MODE` still wins (L8); US-0118 only fills the unset case |
| US-0070 / DEC-0052 (phase selection) | L2856 `### Phase & role governance keys` (AUTO_PHASE_* canonical) | `## US-0070` L1572 | ✓ exists — `AUTO_PHASE_*` remains explicit override; classifier only fills the unset case |
| US-0078 / DEC-0060 (intake evidence) | L479 runbook `## Interactive intake evidence validation` | `## US-0078` L1596 | ✓ exists — evidence gate still runs before any write (L10); classifier proposal + operator decision recorded in evidence bundle |
| US-0051 (decomposition) | L371 runbook `## Intake decomposition and risk-aware questioning` | (no h1 anchor) | ✓ exists — classifier runs after the decomposition evaluator (L10) |
| US-0069 / DEC-0051 (phase→role matrix) | L2856 `### Phase & role governance keys` | `## US-0069` L1568 | ✓ exists — classifier only selects which phases run, not who runs them |
| US-0103 (AI decision ledger) | L2421 `### Sovereign-loop era keys` | `## US-0103` L1640 | ✓ exists — read-only consumer for audit trail |

All 6 compose targets verified present (read-only consumers of US-0118 — their architectural surfaces are NOT edited by US-0118; additive-only: new flag, new lib, new row fields, new precedence clause, new sub-block, new runbook h2).


### Risks finalized (R1..R8 — promoted from R-0106)

| Risk | Severity | Mitigation |
|------|----------|------------|
| **R1** Classification ambiguity (mixed `docs/` + `src/` tiers) | **MEDIUM** | Q1 LOCKED: highest tier wins (`code` > `mini` > `doc`) per `classify_touched_files` tier_rank A>B>C. Single-pass deterministic. Contract test `test_us0118_code_kind_routes_to_standard` covers the mixed-tier case. |
| **R2** Precedence conflicts (`WORK_KIND_ROUTING=1` + `DELIVERY_MODE` set) | **MEDIUM** | L8 precedence chain LOCKED + `WORK_KIND_DELIVERY_MODE_CONFLICT` reason code (Q2). Explicit operator flags always win; classifier fills only the unset case. Contract test `test_us0118_explicit_delivery_mode_wins_over_work_kind` + `test_us0118_auto_phase_wins_over_work_kind`. |
| **R3** `mega_quick` eligibility overlap with `mini` | **LOW–MEDIUM** | L6 LOCKED: classifier recommends `mega_quick` only when US-0096 eligibility passes (AC≤3, no DEC, single component), else falls back to `ultra_lean`. Contract test `test_us0118_mini_kind_routes_to_mega_quick_when_eligible` + `test_us0118_mini_kind_routes_to_ultra_lean`. |
| **R4** Backward compatibility (existing backlog rows without `work_kind`) | **MEDIUM** | Q8 LOCKED: `WORK_KIND_ROUTING=0` default-off + early-return in `/auto` step 0 + `/intake` step 5 skip. No forced reclassification, no schema-migration. Contract test `test_us0118_default_off_zero_overhead`. |
| **R5** Operator trust (deterministic + inspectable) | **LOW–MEDIUM** | Q3 LOCKED: deterministic pure-stdlib + `--explain` flag emitting `rule_trace` (Q10). Contract test `test_us0118_explain_emits_rule_trace`. Operators can override with confidence. |
| **R6** Reuse boundary drift (`dev_environment_lib.classify_touched_files` rewritten vs imported) | **LOW** | Q9 LOCKED (in T-001): `work_kind_classify_lib.py` imports `TIER_C_SKIP_PREFIXES` + `classify_touched_files` from `dev_environment_lib` — no duplication. Contract test `test_us0118_classify_touched_files_reuse`. |
| **R7** Installer parity drift (triple-installer must ship new script) | **LOW** | T-009 adds both `scripts/work_kind_classify_lib.py` + `template/scripts/work_kind_classify_lib.py` to `installer-owned-paths.manifest` `[install_include_paths]`. Manifest-driven single source of truth. |
| **R8** Cross-story byte-stability surface (6th sub-block) — US-0118 is the first NEW story after the US-0113..US-0117 quint; it adds a 6th sub-block to `### Full scratchpad reference (detailed)`. Risk of accidentally editing a prior released block (US-0113 L2421 / US-0114 L2545 / US-0115 L2617 / US-0116 L2765 / US-0117 L2856). | **MEDIUM** | T-007 mandates net-new-keys-only + cross-link-pointer + reason-code-only shape; never edits prior released blocks. Execute-phase verifies `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2856 range (no removals/modifications to US-0113..US-0117 blocks). QA re-verifies. `PARITY_OK <size> <size>` authoritative end-to-end proof. Pattern now scales from quint to 6th story. |

### Stop conditions met

- **No DEC required beyond DEC-0118** — DEC-0118 authored in THIS phase (Required → Accepted; mirrors DEC-0082 / DEC-0052 precedent).
- **No feasibility unknown** — R-0106 closed all 10 discovery open questions Q1..Q10; approach A1 locked; sprint seeds T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; risks R1..R8 finalized; DC check clean.
- **No data migration risk** — `WORK_KIND_ROUTING=0` default-off + no forced reclassification of existing backlog rows (Q8 LOCKED). New `work_kind` / `recommended_delivery_mode` fields are optional; absence is valid.
- **Compose-do-not-amend verified** — all 6 compose targets (US-0096 / US-0070 / US-0078 / US-0051 / US-0069 / US-0103) verified present with existing `## US-xxxx` h1 anchors in `architecture.md`; US-0118 is additive-only.

**No DECISION_GATE raised.** Architecture phase revealed no question requiring operator input. DC check clean (no new DC candidates). Verdict: **PASS**.

### Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called (US-0118 documentation-only so far — architecture phase writes prose + DEC only; existing digest context sufficient per R-0106 — S0113..S0117 retrospectives established the reusable patterns applied here: cross-link pointer pattern scales to 6th story; angle-distinct narrative pattern extends to the routing-primitive angle (distinct from prior 5 documentation-family angles); cross-story byte-stability contract now scales from quint to 6th story; DC anchor resolution pattern proven (US-0117 was the final deferred-candidate resolution point — US-0118 inherits a clean deferral register). No write to `mistakes.jsonl` in architecture phase.

### Consequences

- Sprint: S0118 (pending `/sprint-plan`).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.
- New code surface: `scripts/work_kind_classify_lib.py` (NEW) + `tests/work_kind_classify_test.py` (NEW) + installer manifest rows.
- New doc surface: `## US-0118` h1 anchor in `architecture.md` (this section) + `### Work-kind routing keys (US-0118)` README sub-block (in `/execute`) + `## Work-kind routing (US-0118)` runbook h2 (in `/execute`).
- New scratchpad surface: `WORK_KIND_ROUTING=0` key + `WORK_KIND_*` reason-code family (in `/execute`).
- New command surface: `.cursor/commands/auto.md` precedence clause + `.cursor/commands/intake.md` step-5 hook (in `/execute`).
- New evidence schema: `work_kind` / `recommended_delivery_mode` / `work_kind_operator_decision` fields in `handoffs/intake_evidence/*.json` (in `/execute`).
- **`WORK_KIND_ROUTING=0` (default)**: zero overhead — `/auto` `resolve_delivery_mode` + `/intake` step 5 skip classifier entirely; existing backlog rows without `work_kind` route via current `DELIVERY_MODE`/`AUTO_PHASE_*` precedence (no forced reclassification).
- **`WORK_KIND_ROUTING=1`**: classifier runs at intake (after ACs) and at `/auto` step 0; `recommended_delivery_mode` derived from `work_kind` fills the unset case (L8 precedence); explicit operator flags always win.
- **23/23 compose guards UNCHANGED** (additive-only). 6 read-only compose consumers (US-0096 / US-0070 / US-0078 / US-0051 / US-0069 / US-0103) consume US-0118 output; not amended.
- DC resolution: `## US-0118` h1 anchor added in THIS phase (per R-0105 Q-2 LOCKED pattern); deferral register clean — no carry-over.

### Evidence references

- `docs/product/backlog.md` — `## US-0118` block (L3983–L4025, 12 ACs)
- `docs/product/acceptance.md` — US-0118 row L145 (12 ACs, OPEN)
- `docs/engineering/research.md` — `## R-0106` (delivered 2026-07-04T20:00:00Z, 10/10 open questions Q1..Q10 closed LOCKED; architecture seeds T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; companion DEC-0118 required; AC baselines green; risks R1..R8 finalized)
- `handoffs/po_to_tl.md` — research handoff (topmost block) + discovery handoff + intake handoff
- `docs/engineering/state.md` — research checkpoint (latest) + architecture checkpoint (this phase, appended)
- `handoffs/resume_brief.md` — top block updated to reflect architecture complete
- `scripts/dev_environment_lib.py` — `TIER_C_SKIP_PREFIXES` (L117–L125: `docs/`, `handoffs/`, `sprints/`, `decisions/`, `tests/`, `.cursor/commands/`, `template/docs/`) + `classify_touched_files` (L321–L339: tier A/B/C with `tier_rank={"A":3,"B":2,"C":1}`, highest matching tier wins) — reuse anchor (Q9 LOCKED import contract)
- `its_magic/README.md` — L2421 (US-0113 keys block — byte-stability preserved); L2545 (US-0114 keys block — byte-stability preserved); L2617 (US-0115 keys block — byte-stability preserved); L2765 (US-0116 keys block — byte-stability preserved); L2856 (US-0117 keys block — byte-stability preserved + insertion point for `### Work-kind routing keys (US-0118)` 6th sub-block in `/execute`)
- `docs/engineering/architecture.md` — h1 inventory confirmed: `## US-0069` L1568, `## US-0070` L1572, `## US-0078` L1596, `## US-0103` L1640, `## US-0096` L1684 exist (read-only consumers of US-0118); `## US-0118` added in THIS phase (appended below the existing `## US-0099` section)
- `decisions/DEC-0118.md` — companion DEC (authored in THIS phase)
- `.cursor/scratchpad.md` — `WORK_KIND_ROUTING` (new key, added in `/execute`); `DELIVERY_MODE` / `AUTO_PHASE_*` / `SPRINT_MAX_TASKS` (existing — grep anchors only)
- `.cursor/commands/auto.md` — `resolve_delivery_mode` step 0 (precedence clause added in `/execute`)
- `.cursor/commands/intake.md` — step 5 (classifier hook added in `/execute`)


### Isolation evidence (per US-0048 / DEC-0029)

- `phase_id=architecture`
- `role=tech-lead`
- `story_id=US-0118`
- `sprint_id=(pending — created at sprint-plan)`
- `orchestrator_run_id=auto-20260704-01`
- `delivery_mode=ultra_lean`, `macro_phase=plan` (architecture — second canonical phase of `plan` macro per US-0096 / DEC-0082; research + architecture + sprint-plan merged)
- `fresh_context_marker=tl-US0118-architecture-20260704T203000Z-fresh`
- `timestamp=2026-07-04T20:30:00Z` (UTC)
- `evidence_ref=docs/product/backlog.md (## US-0118 block L3983–L4025 narrow-read), docs/product/acceptance.md (US-0118 row L145 narrow-read), handoffs/intake_evidence/US-0118-intake.json (cross-reference only — not read this phase), handoffs/po_to_tl.md (US-0118 research handoff L5–L93 + discovery handoff L95–L193 + intake handoff L196–L231 narrow-read), docs/engineering/state.md (research checkpoint L197–L297 + discovery checkpoint L102–L196 + drain-advance breadcrumb L84–L101 narrow-read), docs/engineering/research.md (R-0106 entry L8754–L8904 full read), docs/engineering/architecture.md (grep ^## US- anchors + US-0117 section L1420–L1566 read as template + DC anchor verification L1568–L1710 + US-0099 last line L1710), scripts/dev_environment_lib.py (TIER_C_SKIP_PREFIXES L117–L125 + classify_touched_files L321–L339 narrow-read for Q9 import-contract lock), its_magic/README.md (grep ### .*keys anchors only — no full-read), decisions/DEC-0082.md (full read as DEC-0118 template), decisions/DEC-0052.md (full read as DEC-0118 template), docs/product/backlog.md (grep ^## US- anchors for DC cross-check), handoffs/resume_brief.md (top ~30 lines narrow-read for drain-advance prose shape)`
- Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the narrow-read files listed above (US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python SHA-256 computation for the strict runtime proof + powershell line-count computations + the artifact writes listed in this phase (architecture.md `## US-0118` section append, decisions/DEC-0118.md NEW, po_to_tl.md architecture handoff prepend, state.md architecture checkpoint append, resume_brief.md drain-advance append). No `.env` reads, no credentials access, no intake-evidence mutation (read-only for this phase).
- `assemble_sovereign_memory_digest(...)` NOT called (US-0118 documentation-only so far — architecture phase writes prose + DEC only; existing digest context sufficient per R-0106 — S0113..S0117 retrospectives established reusable patterns; classifier code is built in `/execute`, not here).
- No write to `mistakes.jsonl` in architecture phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).
- Prior phase strict proof consumed: `rp-auto-20260704-01-research-techlead-20260704T200000Z-US-0118` (from `docs/engineering/state.md` research checkpoint L281–L285, unchanged).
- Current architecture-phase strict proof recorded below.

### Strict runtime proof (DEC-0038)

- **runtime_proof_id**: `rp-auto-20260704-01-architecture-techlead-20260704T203000Z-US-0118`
- **canonical_payload** (sorted-key JSON per DEC-0038): `{"orchestrator_run_id":"auto-20260704-01","phase_id":"architecture","proof_issued_at":"2026-07-04T20:30:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260704-01-architecture-techlead-20260704T203000Z-US-0118","sprint_id":"(pending)","story_id":"US-0118"}`
- **proof_hash**: `fd72d56bd8e8450cf830e3a4fa6164d5e3b98595c00fafa166ffd00669b1d3db` (SHA-256 of the sorted-key JSON payload above, computed via python `hashlib.sha256`)
- **proof_ttl_seconds**: 3600
- **proof_ttl**: 2026-07-04T21:30:00Z (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

### Decision gate

- `decision_gate=false` (no DECISION_GATE; no hard stop; companion DEC-0118 authored Accepted in THIS phase; approach A1 locked; sprint seeds T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; risks R1..R8 finalized; DC check clean; compose-do-not-amend verified 6/6)
- `stop_conditions_met=yes` (no missing references — all 6 compose targets verified; no decision gate triggered; AC baselines green: `validate_readme_feature_coverage.py` PASS + `pytest tests/scratchpad_example_parity_test.py` 4 passed)

### Next scheduled phase

- `next_scheduled_phase=/sprint-plan` (role=tech-lead per US-0069 / DEC-0051 phase→role matrix default; third canonical phase of `plan` macro per ultra_lean; research + architecture + sprint-plan merged into `plan` macro)
- `next_scheduled_role=tech-lead`
- `next_scheduled_sprint_macro=plan`
- `stop_condition=STOP after architecture completes; hand off via artifacts only to /sprint-plan in fresh tech-lead subagent (BUG-0006)`

---

## US-0119 — Autonomous-autonomy presets and configurable hard-stop relaxation

### Overview

US-0119 adds two orthogonal primitives on top of the existing sovereignty stack (US-0092 / US-0095 / US-0103 / US-0104 / US-0105 / US-0107):

1. **`AUTONOMY_PRESET={none|balanced|full}`** (default `none`) — an ergonomic scratchpad flag that deterministically expands into twelve per-feature autonomy flags (all of which already exist individually or are added here as net-new keys). Each preset bundles the combination an operator would otherwise configure manually. `AUTONOMY_PRESET=none` is byte-identical to pre-US-0119 behaviour.
2. **`AUTONOMY_STOP_POLICY={block|auto_repair_then_block|auto_repair_then_skip}`** (default `block`) — classifies every fail-closed reason code in `docs/engineering/autonomy-stop-matrix.md` as either `security_hard` (never auto-resolved under any preset / policy) or `autonomy_resolvable` (bounded auto-repair with an append-only ledger before escalation).

The two mechanisms compose: the preset controls *which* per-feature flags are flipped on; the stop policy controls *how* softened reason codes are handled at phase boundaries. Neither mechanism modifies the semantics of the underlying consumers — the preset is an expansion into existing keys, and the stop policy is a dispatch layer on top of existing reason-code emissions.

### Companion DEC

**`decisions/DEC-0119.md`** — authored in THIS architecture phase (status=Accepted). Locks:
- (a) `AUTONOMY_PRESET` 3-tier enumeration `none|balanced|full` (default `none`)
- (b) `AUTONOMY_STOP_POLICY` 3-value enumeration `block|auto_repair_then_block|auto_repair_then_skip` (default `block`)
- (c) Two-tier stop classification `security_hard|autonomy_resolvable`
- (d) `security_hard` rows never auto-repaired (bounded cap = 0 from matrix)
- (e) Nine `auto_repair_kind` taxonomy values from R-0107 Q2
- (f) Nine `autonomy_resolvable` reason codes per Q2 mapping
- (g) `autonomy_repair_kind` taxonomy + uniform cap = 3 per `(run, reason_code)` per Q3
- (h) `AUTONOMY_PRESET=none` is byte-identical to pre-US-0119
- (i) Twelve per-feature flags are additive consumers only (no existing consumer semantics change)
- (j) Precedence: explicit per-flag > preset expansion > scratchpad defaults

Mirrors DEC-0082 (delivery modes) / DEC-0078 (full-autonomy stop matrix) precedent.

### Approach A1 (LOCKED)

Single vertical-slice approach. No alternatives retained — 2-tier (`none|full` preset) rejected as too coarse; 4-tier (`none|low|medium|high`) rejected as over-engineered (no operator demand); 3-tier stop-class (`security_hard|autonomy_resolvable|soft_warn`) rejected as over-engineered (operators want binary never/yes).

**A1 components**:

| Component | Artifact | Responsibility |
|-----------|----------|----------------|
| `AUTONOMY_PRESET` flag | `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` | Scratchpad key; net-new (13th key in autonomy block) |
| `AUTONOMY_STOP_POLICY` flag | `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` | Scratchpad key; net-new (14th key in autonomy block) |
| Preset expansion lib | `scripts/autonomy_preset_lib.py` | `expand_autonomy_preset(preset, overrides) -> dict`; pure stdlib; `--self-test` + `--explain` |
| Stop-matrix manifest | `docs/engineering/autonomy-stop-matrix.md` + `template/docs/engineering/autonomy-stop-matrix.md` | Operator-facing authority file; `security_hard` and `autonomy_resolvable` rows |
| Stop-matrix YAML | `scripts/data/autonomy_stop_matrix.yaml` | Machine-readable companion for validators |
| Matrix validator | `scripts/validate_autonomy_stop_matrix.py` | `--self-test`; checks orphan codes, `security_hard` → `auto_repair_kind=n/a`, `autonomy_resolvable` → finite `cap` |
| Twelve per-feature flags | `.cursor/scratchpad.md` | Net-new keys; expansion targets (existing consumers where applicable) |
| Bounded repair ledger | `handoffs/autonomy_repair_ledger/<orchestrator_run_id>.jsonl` | Append-only; per-run cap from matrix; gitignored |
| Breadcrumb | `docs/engineering/state.md` phase boundary | `autonomy_relaxed: <reason_code> -> <auto_repair_kind>` one-line per soft-stop (Q10 LOCKED) |
| Consumer wiring | `/auto`, `/intake`, `/execute`, `/qa`, `/release` | Wire 12 flags into existing consumers (additive only) |
| Tests + parity | `tests/us0119_autonomy_preset_test.py` + `check_intake_template_parity.py --scope=us-0119` | 10 contract test markers + template parity enforcement |
| Documentation | `docs/engineering/architecture.md` (this section) + `docs/engineering/runbook.md` (h2) + `.cursor/commands/auto.md` (anchor) | Operator-facing docs + template parity |

**Execution order**: T-anch → T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 → T-008 → T-009 → T-010 → T-011 (acyclic; T-001..T-003 first since they're the code/manifest/flags foundation).

### Files to touch

| File | Change |
|------|--------|
| `docs/engineering/architecture.md` | Add `## US-0119` section (THIS phase — T-anch NO-OP / verification; no write in execute) |
| `.cursor/scratchpad.md` | Add `AUTONOMY_PRESET`, `AUTONOMY_STOP_POLICY`, 12 per-feature flags |
| `template/.cursor/scratchpad.local.example.md` | Mirror scratchpad additions |
| `scripts/autonomy_preset_lib.py` | NEW — `expand_autonomy_preset(preset, overrides) -> dict` |
| `template/scripts/autonomy_preset_lib.py` | NEW — byte-identical copy |
| `scripts/data/autonomy_stop_matrix.yaml` | NEW — machine-readable stop classification |
| `scripts/validate_autonomy_stop_matrix.py` | NEW — matrix validator |
| `template/scripts/validate_autonomy_stop_matrix.py` | NEW — byte-identical copy |
| `docs/engineering/autonomy-stop-matrix.md` | NEW — operator-facing authority file |
| `template/docs/engineering/autonomy-stop-matrix.md` | NEW — byte-identical copy |
| `tests/us0119_autonomy_preset_test.py` | NEW — 10 contract test markers |
| `.cursor/commands/auto.md` | Add `## Autonomy presets (US-0119)` anchor |
| `template/.cursor/commands/auto.md` | Mirror |
| `docs/engineering/runbook.md` | Add `## Autonomy presets (US-0119)` h2 |
| `template/docs/engineering/runbook.md` | Mirror |
| `its_magic/README.md` | Add `### Autonomy preset keys (US-0119)` sub-block (7th sub-block; preserves cross-story byte-stability surface) |
| `template/its_magic/README.md` | Mirror (byte-stability preserved) |
| `docs/engineering/state.md` | `autonomy_relaxed` breadcrumb at phase boundaries; architecture checkpoint (THIS phase) |
| `decisions/DEC-0119.md` | NEW — companion DEC (THIS phase) |
| `handoffs/po_to_tl.md` | Prepend architecture handoff (THIS phase) |
| `installer-owned-paths.manifest` | Add rows for new scripts |

### Files NOT to touch (compose, do not amend)

| File | Reason |
|------|--------|
| `.cursor/commands/execute.md` | US-0092 outer-driver semantics UNCHANGED |
| `.cursor/commands/qa.md` | US-0095 native auto-chain UNCHANGED |
| `.cursor/commands/release.md` | US-0056 strict runtime proof semantics UNCHANGED (`RUNTIME_PROOF_KIND=lightweight` is only an opt-in lighter attestation — proof kind select, not semantics rewrite) |
| `.cursor/commands/intake.md` (evidence gate logic) | US-0068 intake evidence gate NEVER bypassed; `INTAKE_AUTONOMY_MODE=1` only auto-derives answers on known-stack repeat projects |
| `scripts/scratchpad_example_parity_test.py` | BUG-0013 regression tests UNCHANGED |
| `handoffs/intake_evidence/US-*.json` (prior entries) | BUG-0007 truthfulness UNCHANGED — schema extension optional, never retroactive |

### Sprint seeds (12 tasks within SPRINT_MAX_TASKS=12)

| Seed | Description | AC coverage |
|------|-------------|-------------|
| **T-anch** | Verify `## US-0119` h1 anchor present in `architecture.md` (added in THIS phase); verify compose-do-not-amend 6/6 compose targets; lock compose-guard UNCHANGED set (23+ guards) | AC-12, AC-11 |
| **T-001** | `scripts/autonomy_preset_lib.py` — `expand_autonomy_preset(preset, overrides) -> dict` + `--self-test` + `--explain`; pure stdlib; deterministic | AC-1, AC-2 |
| **T-002** | Add `AUTONOMY_PRESET` + `AUTONOMY_STOP_POLICY` + 12 per-feature flags in `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md`; merge-precedence note (explicit > preset > defaults) | AC-1, AC-3, AC-5 |
| **T-003** | `docs/engineering/autonomy-stop-matrix.md` + `template/docs/engineering/autonomy-stop-matrix.md` parity + `scripts/data/autonomy_stop_matrix.yaml` + `scripts/validate_autonomy_stop_matrix.py --self-test` | AC-4, AC-10 |
| **T-004** | Wire 12 per-feature flags into existing consumers — `/auto` auto-expansion + `/intake` INTAKE_AUTONOMY_MODE / INTAKE_MINIMAL_PACK / INTAKE_ASSUME_STACK_CONTEXT + `/execute` RUNTIME_PROOF_KIND + `/qa` GOAL_CONVERGENCE_INTERVAL + `/release` RELEASE_PUBLISH_AUTO_CONFIRM | AC-5 |
| **T-005** | Bounded auto-repair ledger `handoffs/autonomy_repair_ledger/<orchestrator_run_id>.jsonl` + cap logic + `AUTONOMY_REPAIR_CAP_EXHAUSTED` terminal stop reason | AC-8 |
| **T-006** | `autonomy_relaxed` breadcrumb in `docs/engineering/state.md` at phase boundary (one-line per soft-stop per Q10) | AC-9 |
| **T-007** | Contract tests `tests/us0119_autonomy_preset_test.py` — 10 markers: preset-none-noop, balanced-expansion, full-expansion, explicit-flag-overrides-preset, expansion-uses-known-keys-only, matrix-validator-passes, security-hard-gates-never-auto-repaired, stop-policy-repair-dispatch, repair-ledger-cap-escalates, matrix-no-orphan-codes | AC-6, AC-7, AC-10 |
| **T-008** | README `### Autonomy preset keys (US-0119)` 7th sub-block + `check_intake_template_parity.py --scope=us-0119` + `AUTONOMY_PRESET_PAIRS` manifest | AC-10, AC-11 |
| **T-009** | Runbook cross-link `## Autonomy presets (US-0119)` h2 + `.cursor/commands/auto.md` `## Autonomy presets (US-0119)` anchor + template parity | AC-11 |
| **T-010** | `installer-owned-paths.manifest` rows for `scripts/autonomy_preset_lib.py` + `template/scripts/autonomy_preset_lib.py` + `scripts/validate_autonomy_stop_matrix.py` + `template/scripts/validate_autonomy_stop_matrix.py` | AC-10 |
| **T-011** | Regression tests `pytest tests/scratchpad_example_parity_test.py -v` 4 passed + forbid edits to scratchpad + test; `PARITY_OK <size> <size>` byte-stability proof | AC-6, AC-10 |

### Test markers (AC-10 → 10 markers)

| Marker | AC | Description |
|--------|----| -----|
| `test_us0119_preset_none_is_noop` | AC-6 | `AUTONOMY_PRESET=none` produces byte-identical pre-US-0119 behaviour |
| `test_us0119_preset_balanced_expansion` | AC-2 | balanced expands into documented 12 flags |
| `test_us0119_preset_full_expansion` | AC-2 | full expands into documented 12 flags (superset of balanced) |
| `test_us0119_explicit_flag_overrides_preset` | AC-2 | explicit per-flag > preset expansion |
| `test_us0119_preset_expansion_uses_known_keys_only` | AC-12 | expansion output contains only keys in pre-US-0119 scratchpad schema |
| `test_us0119_matrix_validator_passes` | AC-4 | `scripts/validate_autonomy_stop_matrix.py --self-test` exits 0 |
| `test_us0119_security_hard_gates_never_auto_repaired` | AC-7 | matrix `security_hard` rows all carry `auto_repair_kind=n/a` |
| `test_us0119_stop_policy_affects_repair_dispatch` | AC-3 | `auto_repair_then_block` vs `auto_repair_then_skip` dispatch correctly |
| `test_us0119_repair_ledger_cap_escalates` | AC-8 | cap exhaustion → `AUTONOMY_REPAIR_CAP_EXHAUSTED` terminal stop |
| `test_us0119_matrix_no_orphan_codes` | AC-4 | no orphan reason codes outside YAML manifest |

### Compose guards UNCHANGED (6/6 verified)

| Story | architecture.md anchor | Status |
|-------|------------------------|--------|
| US-0092 / DEC-0078 | `## US-0092` L1696 | ✓ exists — delivery confirmation gate UNCHANGED; AUTONOMY_PRESET only adds relaxation layer above |
| US-0095 | `## US-0095` L1700 | ✓ exists — native auto-chain UNCHANGED |
| US-0056 / DEC-0038 | (inline reference — no h1 anchor; strict runtime proof semantics referenced in architecture text; `RUNTIME_PROOF_KIND=lightweight` is opt-in lighter attestation only — proof kind select, not semantics rewrite) | ✓ UNCHANGED |
| US-0068 / DEC-0060 | (inline reference — no h1 anchor; intake evidence gate referenced in intake commands; `INTAKE_AUTONOMY_MODE=1` only auto-derives answers on known-stack repeat projects — evidence gate NEVER bypassed) | ✓ UNCHANGED |
| US-0096 / DEC-0082 | `## US-0096` L1684 | ✓ exists — delivery modes UNCHANGED; AUTONOMY_PRESET only softens governance gates within them |
| BUG-0007 | (no h1 anchor — truthfulness rule; `INTAKE_ASSUME_STACK_CONTEXT=1` auto-fills stack/runtime from backlog history with `assumption_confirmation_ref` contract preserved) | ✓ UNCHANGED |

### DC (deferred-candidate) check

`grep "^## US-0119" docs/engineering/architecture.md` → **no matches prior to THIS write**. The `## US-0119` h1 anchor is added in THIS `/architecture` phase per R-0105 Q-2 LOCKED pattern (architecture artifacts live in `architecture.md`; T-anch resolves anchor presence in `/execute`). No deferred-candidate carry-over.

### Compose-do-not-amend verification

All 6 compose targets (US-0092 / US-0095 / US-0056 / US-0068 / US-0096 / BUG-0007) verified present in `architecture.md` with existing anchors or inline references; US-0119 is additive-only. US-0119 inherits no DC candidates from prior stories. No new DC candidates are created by US-0119 (its own `## US-0119` anchor is resolved HERE). Deferral register remains clean — no carry-over to a successor story.

### Risks finalized (R1..R8)

| Risk | Severity | Mitigation |
|------|----------|------------|
| **R1** Backward-compat regression (`AUTONOMY_PRESET=none` byte-identical to pre-US-0119) | MEDIUM | `test_us0119_preset_none_is_noop` asserts byte-identical surface; explicit-flag > preset > default precedence chain |
| **R2** Security gate bypass via matrix drift | MEDIUM | `test_us0119_security_hard_gates_never_auto_repaired` asserts matrix divergence; validator `--self-test` enforces `auto_repair_kind=n/a` on all `security_hard` rows |
| **R3** Repair ledger growth | LOW | Per-run cap = 3 (Q3 LOCKED) + gitignore at `handoffs/autonomy_repair_ledger/*.jsonl`; operator override via `AUTONOMY_REPAIR_CAP_OVERRIDE` |
| **R4** Operator confusion (softened gates) | MEDIUM | Breadcrumb `autonomy_relaxed:` in state.md + ledger audit surface + `AUTONOMY_REPAIR_CAP_EXHAUSTED` terminal stop reason; `AUTONOMY_PRESET=none` default preserves current behaviour |
| **R5** Preset-expansion vs explicit-key precedence | LOW–MEDIUM | LOCKED: explicit per-flag > preset > defaults (documented in scratchpad merge-precedence note per US-0078 model B) |
| **R6** Compose-do-not-amend drift (expansion uses unknown keys) | LOW | `test_us0119_preset_expansion_uses_known_keys_only` enforces only pre-US-0119 scratchpad schema keys |
| **R7** Matrix validator grep fragility | LOW | LOCKED: explicit YAML manifest (Q8 LOCKED from R-0107), not grep-only; `scripts/data/autonomy_stop_matrix.yaml` is single source of truth |
| **R8** Breadcrumb format granularity (one-line per soft-stop vs aggregated) | LOW–MEDIUM | LOCKED: one-line per soft-stop (Q10 LOCKED from R-0107); operator can count per-code softening events |

### Stop conditions

- `decision_gate=false` — no decision gate triggered; companion DEC-0119 authored Accepted in THIS phase
- `missing_acceptance_criteria=none` — all 12 ACs covered by sprint seeds
- `task_count=12` (T-anch + T-001..T-011) — within `SPRINT_MAX_TASKS=12`
- `compose_guards=6/6 UNCHANGED` — verified
- `dc_check=clean` — no deferred-candidate carry-over

### Consequences

- **Positive**: Operators gain a single `AUTONOMY_PRESET=balanced|full` switch that deterministically configures twelve autonomy flags; `AUTONOMY_STOP_POLICY` provides explicit control over how softened non-security stops are handled; audit trail via ledger + breadcrumb; backward-compatible default.
- **Negative**: More scratchpad surface area (14 new keys: `AUTONOMY_PRESET` + `AUTONOMY_STOP_POLICY` + 12 per-feature flags); new code surface (`autonomy_preset_lib.py` + `validate_autonomy_stop_matrix.py` + tests); new stop-matrix authority file; 7th cumulative byte-stability sub-block in README.
- **Neutral**: Implementation lives in `/execute`; this decision fixes the architecture contract only. `/sprint-plan` may merge or split the 12 task seeds within the 12-task budget.

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=architecture`, `role=tech-lead`, `story_id=US-0119`, `sprint_id=(pending)`, `orchestrator_run_id=auto-20260705-us0119-intake`
- `delivery_mode=ultra_lean`, `macro_phase=plan` (architecture — second canonical phase of `plan` macro per US-0096 / DEC-0082; research + architecture + sprint-plan merged)
- `fresh_context_marker=tl-US0119-architecture-20260705T224500Z-fresh`
- `timestamp=2026-07-05T22:45:00Z` (UTC)
- `evidence_ref=docs/product/backlog.md (## US-0119 block L4028-L4070 narrow-read — 12 ACs), docs/product/acceptance.md (US-0119 row L146 narrow-read — 12 ACs OPEN), handoffs/po_to_tl.md (US-0119 research handoff L1-L205 narrow-read), docs/engineering/state.md (research checkpoint L854-L890 narrow-read), docs/engineering/research.md (R-0107 entry L8907-L9001 full read), docs/engineering/architecture.md (## US-0118 section L1713-L1923 as template + compose-anchor verification), decisions/DEC-0118.md (full read as DEC-0119 template), .cursor/scratchpad.md (AUTONOMY_PRESET/AUTONOMY_STOP_POLICY/12 per-feature flag grep — zero matches confirming net-new), handoffs/resume_brief.md (top ~15 lines narrow-read)`
- Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the narrow-read files listed above (US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python SHA-256 computation for the strict runtime proof + the artifact writes listed in this phase (architecture.md `## US-0119` section append, decisions/DEC-0119.md NEW, po_to_tl.md architecture handoff prepend, state.md architecture checkpoint append). No `.env` reads, no credentials access, no intake-evidence mutation.
- `assemble_sovereign_memory_digest(...)` NOT called (US-0119 code+docs; existing digest context sufficient per R-0107 — US-0113..US-0118 introspectives established reusable patterns; autonomy-preset angle adds distinct 7th-family dimension).
- No write to `mistakes.jsonl` in architecture phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).
- Prior phase strict proof consumed: `rp-auto-20260705-us0119-research-techlead-20260705T223000Z-US-0119` (from R-0107 entry, unchanged).
- Current architecture-phase strict proof recorded below.

### Strict runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260705-us0119-architecture-techlead-20260705T224500Z-US-0119`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"plan","orchestrator_run_id":"auto-20260705-us0119-intake","phase_id":"architecture","proof_issued_at":"2026-07-05T22:45:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260705-us0119-architecture-techlead-20260705T224500Z-US-0119","sprint_id":"(pending)","story_id":"US-0119"}`
- `proof_hash=71d0ac09ece22e540a8c8002555fe8f6720c6b5bcd77eb6b6eb09cc34360b1e9` (SHA-256 of the sorted-key JSON payload above)
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-07-05T23:45:00Z` (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

### Decision gate

- `decision_gate=false` (no DECISION_GATE; companion DEC-0119 authored Accepted in THIS phase; approach A1 locked; sprint seeds T-anch + T-001..T-011 within SPRINT_MAX_TASKS=12; risks R1..R8 finalized; DC check clean; compose-do-not-amend verified 6/6)
- `stop_conditions_met=yes` (no missing references — all 6 compose targets verified; no decision gate triggered; AC baselines green)

### Next scheduled phase

- `next_scheduled_phase=/sprint-plan` (role=tech-lead per US-0069 / DEC-0051 phase→role matrix default; third canonical phase of `plan` macro per ultra_lean; research + architecture + sprint-plan merged into `plan` macro)
- `next_scheduled_role=tech-lead`
- `next_scheduled_sprint_macro=plan`
- `stop_condition=STOP after architecture completes; hand off via artifacts only to /sprint-plan in fresh tech-lead subagent (BUG-0006)`

---

# US-0120 — Dedicated `/closure` phase for exclusive Story Closure responsibility

## Overview

**US-0120** extracts Story Closure (Status `OPEN`→`DONE` in `docs/product/backlog.md` + acceptance checkbox `[ ]`→`[x]` in `docs/product/acceptance.md` + `docs/engineering/state.md` closure checkpoint + `sprints/Sxxxx/closure-verification.md` artifact) from `/release` step 10–12 into a **dedicated `/closure` phase** with exclusive `qe` role ownership. The ultra-lean ship macro becomes `release → closure → refresh-context` (3 phases instead of 2). Orchestrator post-closure `rg` verification enforces materialization fidelity (fixes the US-0119 closure fidelity gap where the release subagent claimed closure but files remained `OPEN`/unchecked — same pattern as BUG-0006 execute cycle).

This is a **governance-only** change: no new code surfaces beyond a schema validator (`scripts/validate_closure_verification.py`) and contract tests (`tests/us0120_closure_phase_test.py`). The compose surface (US-0043, US-0045, US-0040, US-0048, US-0056, US-0096) remains UNCHANGED — `/closure` is the dedicated executor of the contracts those stories already define. Forward-compat only (R8 ACCEPTED): already-DONE stories are untouched; no retroactive `closure-verification.md` generation.

**Research anchor**: **R-0108** (research `docs/engineering/state.md` L1102–L1231 — resolved all 10 open questions Q1..Q10 LOCKED; 8 risks R1..R8 ACCEPTED; approach A1 locked; compose guards 6/6 UNCHANGED). **No companion DEC** (modifies DEC-0052 phase→role matrix + DEC-0082 ship macro directly — both are additive scoped edits, no new DEC needed per R-0108 ID resolution).

**Fresh context marker**: `tl-US0120-architecture-20260707T215000Z-fresh`
**Orchestrator run id**: `manual-20260707-us0120`
**Timestamp**: 2026-07-07T21:50:00Z (UTC)
**Verdict**: PASS
**Next**: `/sprint-plan`

## Approach locked (A1 — from discovery)

**Approach A1** (locked, carried from discovery): Extract Story Closure from `/release` step 10–12 into dedicated `/closure` phase with exclusive `qe` role ownership. Ship macro becomes 3-phase: `release → closure → refresh-context`. Orchestrator post-closure `rg` verification enforces materialization fidelity. Forward-compat only (no retroactive closure for already-DONE stories).

| Option | Summary | Verdict |
|--------|---------|---------|
| **A1** | **Dedicated `/closure` phase with exclusive `qe` ownership + orchestrator post-verification** | **Preferred** — resolves US-0119 fidelity gap; follows "one phase, one responsibility" principle; deterministic drain hook detection for in-flight stories. |
| A2 (rejected) | Keep closure inside `/release` but add orchestrator-side verification of step 10–12 execution. | **Rejected** — same fidelity pattern as US-0119 BUG-0006; release subagent overloaded with 19 steps; verification cannot fix non-materialization. |
| A3 (rejected) | Extract closure into `/qa` phase (`qa` already owns quality gate). | **Rejected** — conflates quality findings with status reconciliation (different US-0043 contract); `/qa` runs BEFORE `/release`, closure must run AFTER `/release`; violates phase ordering. |

## Phase definition

### /closure phase contract

| Attribute | Value |
|-----------|-------|
| **phase_id** | `closure` |
| **macro_phase** | `ship` (ultra_lean), canonical for all 3 delivery modes (standard, ultra_lean, mega_quick) |
| **role** | `qe` (default; `curator` fallback via `AUTO_ROLE_CLOSURE` scratchpad override — Q2 LOCKED) |
| **phase ordering** | AFTER `/release` PASS; BEFORE `/refresh-context` |
| **input prerequisites** | (a) `handoffs/release_queue.md` row `status=released` exists for target sprint, (b) `handoffs/releases/Sxxxx-release-notes.md` EXISTS with PASS verdict, (c) `sprints/Sxxxx/qa-findings.md` EXISTS. Fail-gated: `CLOSURE_RELEASE_EVIDENCE_MISSING`. |
| **outputs (all mandatory)** | (1) `docs/product/backlog.md` target story block: `- Status: OPEN` → `- Status: DONE` (canonical ownership per US-0045), (2) `docs/product/acceptance.md` target row: `- [ ] US-xxxx:` → `- [x] US-xxxx:`, (3) `docs/engineering/state.md` closure checkpoint append (phase_id=closure, role, story_id, sprint_id, fresh_context_marker, timestamp, verdict), (4) `sprints/Sxxxx/closure-verification.md` NEW artifact (schema below) |
| **orchestrator post-verification (D12)** | After `/closure` returns, orchestrator runs direct `rg` verification: (i) `rg "^- Status: DONE$" docs/product/backlog.md` constrained to target story block, (ii) `rg "^\- \[x\] US-xxxx:" docs/product/acceptance.md`. State.md: two-stage grep `rg "phase_id=closure" docs/engineering/state.md \| rg "story_id=US-xxxx"`. If any check FAIL → escalate `CLOSURE_VERIFICATION_FAILED`. |

### closure-verification.md schema (Q6/Q7 LOCKED)

Markdown format (not JSON — Q6 LOCKED; follows existing lifecycle artifact convention: qa-findings.md, release-findings.md, uat.md — all `.md`).

**REQUIRED fields** (validator `scripts/validate_closure_verification.py` checks these):

| Field | Format | Description |
|-------|--------|-------------|
| `story_id` | `US-xxxx` | Target story ID |
| `closure_date` | ISO-8601 UTC (e.g. `2026-07-07T22:00:00Z`) | When closure executed |
| `closure_role` | `qe \| curator` | Actual role that performed closure |
| `pre_closure_status` | `OPEN` | Pre-condition status (must be `OPEN`) |
| `post_closure_status` | `DONE` | Post-condition status (must be `DONE`) |
| `release_evidence_refs[]` | array of paths | Paths to release artifacts closure consumed (release_queue row ref, release-notes ref, qa-findings ref; optionally uat ref, release-findings ref) |
| `isolation_evidence{}` | object | `{phase_id: closure, role, fresh_context_marker, timestamp, evidence_ref: closure-verification.md path}` per US-0048 |
| `runtime_proof{}` | object | `{runtime_proof_id, proof_hash, proof_ttl_seconds: 3600}` per US-0056 / DEC-0038 |

**OPTIONAL fields** (extensible — Q7 LOCKED):

| Field | Format | Description |
|-------|--------|-------------|
| `normalization_notes` | free-text | Edge cases (legacy stories, in-flight reconciliation) |
| `backward_compat_note` | free-text | For in-flight story closure at US-0120 ship boundary |

Schema is **additive-extensible**: validator only checks required fields; future extensions do not break prior closure-verification.md files (R7 ACCEPTED).

## Artifacts

### New artifacts

| Artifact | Path | Responsibility |
|----------|------|----------------|
| `/closure` command (active) | `.cursor/commands/closure.md` | NEW — closure phase command for operator/subagent |
| `/closure` command (template) | `template/.cursor/commands/closure.md` | NEW — byte-identical mirror (T-002; `check_intake_template_parity.py --scope=closure-phase` enforces) |
| Closure verification artifact | `sprints/Sxxxx/closure-verification.md` | NEW — per-sprint closure execution record |
| Closure validator | `scripts/validate_closure_verification.py` | NEW — enforces required-field schema; pure stdlib |
| Contract tests | `tests/us0120_closure_phase_test.py` | NEW — 10 test markers (Q10 LOCKED) |
| This section | `docs/engineering/architecture.md` `# US-0120` | NEW (this phase) |
| Runbook section | `docs/engineering/runbook.md` `## Story closure (US-0120)` | NEW in `/execute` |

### Mutated artifacts (scoped edits only)

| Artifact | Mutation | Scope |
|----------|----------|-------|
| `.cursor/commands/release.md` (active + template) | Remove steps 10–12 (backlog reconciliation + derived views + normalization report); insert pointer at new step 10: "Backlog reconciliation is now handled by the dedicated `/closure` phase — see `.cursor/commands/closure.md`." Renumber old step 13 → new step 10, old step 14 → new step 11, etc. Sequential renumbering, no gaps. Active + template byte-identical. | T-005 |
| `decisions/DEC-0052.md` | ADD canonical phase→role matrix row: `closure \| qe \| AUTO_ROLE_CLOSURE scratchpad override to curator allowed`. ADD `AUTO_ROLE_CLOSURE` row to §2 override contract table. ADD `closure` row to §3 preflight capability gate. Existing 12 phase→role mappings UNTOUCHED. | T-003 |
| `decisions/DEC-0082.md` | Modify ship macro from `[release, refresh-context]` → `[release, closure, refresh-context]` (2→3 phases). Other macro definitions UNTOUCHED. | T-004 |
| `.cursor/commands/auto.md` + `template/.cursor/commands/auto.md` | Add closure to phase plan arrays in all delivery modes; after `/release` completes, orchestrator spawns closure subagent (fresh per BUG-0006). Add `AUTO_ROLE_CLOSURE` scratchpad key. | T-004 |
| `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` | Add `AUTO_ROLE_CLOSURE` key + closure phase pointer. | T-003/T-004 |
| `docs/engineering/state.md` | Append architecture checkpoint (this phase); runtime closure checkpoints appended per-sprint by `/closure`. | This phase |
| `handoffs/po_to_tl.md` | Prepend architecture handoff block (this phase). | This phase |
| `installer-owned-paths.manifest` | Add rows for new scripts + closure.md active + template. | T-009 |

### Files NOT to touch (compose guard UNCHANGED)

| File | Reason |
|------|--------|
| `docs/product/backlog.md` | US-0045 canonical status — `/closure` mutates ONLY at execution time. |
| `docs/product/acceptance.md` | US-0045 derived view — same. |
| Compose-guard story surfaces (US-0043, US-0045, US-0040, US-0048, US-0056, US-0096) | All 6 UNCHANGED — `/closure` EXECUTES their existing contracts. |

## Contracts

### DEC-0052 phase→role matrix extension (scoped — R3 ACCEPTED)

**ADD only** — existing 12 phase→role mappings UNTOUCHED.

| §1 Canonical phase→role matrix | New row |
|-------------------------------|---------|
| `closure` \| `qe` \| `AUTO_ROLE_CLOSURE` override to `curator` | |

| §2 Override contract table | New row |
|---------------------------|---------|
| `AUTO_ROLE_CLOSURE` \| values: `qe`, `curator` \| default: `qe` \| `curator must not write qa-owned surfaces` | |

| §3 Preflight capability gate | New row |
|------------------------------|---------|
| `closure` \| capability: `role:qe` or override \| fail-closed: `PHASE_CAPABILITY_MISSING` | |

### DEC-0082 ship macro extension (scoped — R4 ACCEPTED)

| Macro phase | Old ship | New ship |
|-------------|----------|----------|
| `ship` | `[release, refresh-context]` (2) | `[release, closure, refresh-context]` (3) |

### /auto orchestration wiring (AC-4)

1. All 3 delivery modes include `closure` after `release`.
2. After `/release` PASS → spawn closure subagent (fresh `qe` / `curator` fallback per BUG-0006).
3. After `/closure` PASS → spawn `/refresh-context` (unchanged).
4. `AUTO_ROLE_CLOSURE` scratchpad key (empty = `qe` fallback per Q2).

### Orchestrator post-closure verification protocol (D12 — R1 mitigation)

After `/closure` completes, orchestrator runs deterministic `rg` checks:

```
rg "^- Status: DONE$" docs/product/backlog.md  # constrained to target story block
rg "^\- \[x\] US-xxxx:" docs/product/acceptance.md  # exact match
rg "phase_id=closure" docs/engineering/state.md | rg "story_id=US-xxxx"  # two-stage
```

MISMATCH → fail-gate `CLOSURE_VERIFICATION_FAILED` (non-suppressible, R1 ACCEPTED).

### Drain hook for in-flight stories (Q4 — R2 mitigation)

1. Enumerate stories with `release_queue.md` row `status=released`.
2. For each, check `backlog.md` status + `acceptance.md` checkbox.
   - If `Status: OPEN` AND `- [ ] US-xxxx:` → closure SKIPPED.
   - **Post-US-0120**: spawn `/closure` with backfill mode.
   - **Pre-US-0120**: `CLOSURE_LEGACY_DRIFT` (manual reconciliation or automatic backfill; no retroactive closure-verification.md).
3. SKIP `Status: DONE` stories (R8 — no retroactive touch for US-0108/US-0119).

## Orchestrator wiring

### /auto phase plan update

Phase plan arrays in all 3 delivery modes:
- **standard**: `[..., release, closure, refresh-context]`
- **ultra_lean**: `[release, closure, refresh-context]`
- **mega_quick**: `[..., release, closure, refresh-context]`

### /closure subagent spawn contract

```
phase_id=closure
role=qe (or curator via AUTO_ROLE_CLOSURE override)
story_id=US-xxxx
sprint_id=Sxxxx
orchestrator_run_id=<current>
fresh_context_marker=tl-US0120-closure-<timestamp>-fresh (per BUG-0006)
```

Fresh subagent per BUG-0006 / US-0048 isolation. Produces own isolation evidence + runtime proof per US-0048 / US-0056.

### Release subagent post-US-0120

`.cursor/commands/release.md` steps 10–12 REMOVED. New step 10 = pointer to `/closure`. Release subagent focuses on release artifacts only. Active + template byte-identical (R5/R6 ACCEPTED).

## Compose guards (6/6 UNCHANGED)

| Compose target | Verification | Result |
|---|---|---|
| US-0043 | inline ref (20 matches) — US-0120 EXECUTES US-0043 | ✅ read-only |
| US-0045 | inline ref (20 matches) — US-0120 FOLLOWS US-0045 | ✅ read-only |
| US-0040 | inline ref (7 matches) — US-0120 operates AFTER US-0040 | ✅ read-only |
| US-0048 | inline ref (3 matches) — US-0120 produces own isolation evidence | ✅ read-only |
| US-0056 | inline ref (3 matches) — US-0120 produces own runtime proof | ✅ read-only |
| US-0096 | `## US-0096` at L1684 | ✅ read-only (ship macro extended, semantics unchanged) |

Contract test `test_us0120_compose_guards_unchanged` enforces at execute boundary.

## Risks mitigated

All 8 risks from R-0108 ACCEPTED:

| Risk | Severity | Mitigation |
|------|----------|------------|
| R1: Subagent fidelity gap | MEDIUM | D12 orchestrator post-closure `rg` → `CLOSURE_VERIFICATION_FAILED` |
| R2: In-flight story backward compat | LOW | Q4 drain hook 3-signal detection |
| R3: DEC-0052 scope creep | LOW–MEDIUM | T-003 scoped ADDITIVE edit |
| R4: DEC-0082 scope creep | LOW–MEDIUM | T-004 scoped ship-only edit |
| R5: release.md renumbering | LOW | T-005 deterministic renumber |
| R6: closure.md template parity drift | LOW | T-001+T-002 byte-identical + parity checker extension |
| R7: closure-verification.md schema rigidity | LOW | Extensible schema, required-field-only validator |
| R8: Already-released S0119 backward compat | LOW | Q4 SKIPs DONE stories |

## Sprint seeds preview (10 tasks within SPRINT_MAX_TASKS=12)

| Seed | Description | AC |
|------|-------------|-----|
| **T-anch** | Verify `# US-0120` H1 anchor present; compose guards 6/6; DEC-0052/DEC-0082 scoped-edit contract. | AC-12, AC-11 |
| **T-001** | NEW `.cursor/commands/closure.md` (active). | AC-1 |
| **T-002** | NEW `template/.cursor/commands/closure.md` (byte-identical). | AC-1 |
| **T-003** | DEC-0052 scoped edit + `AUTO_ROLE_CLOSURE` scratchpad key. | AC-2 |
| **T-004** | DEC-0082 ship + auto.md phase plan arrays + closure spawn. | AC-3, AC-4 |
| **T-005** | release.md step 10–12 removal + renumbering (active + template). | AC-5 |
| **T-006** | NEW `scripts/validate_closure_verification.py`. | AC-6 |
| **T-007** | Closure isolation evidence + runtime proof contract in closure.md. | AC-7, AC-8 |
| **T-008** | NEW `tests/us0120_closure_phase_test.py` (10 markers). | AC-9 |
| **T-009** | Drain hook + installer manifest rows. | AC-10 |
| **T-010** | Runbook `## Story closure (US-0120)` h2 + architecture.md (this). | AC-11 |

**Total: 10 tasks (T-anch + T-001..T-010) — within `SPRINT_MAX_TASKS=12`.**

## Test markers (10 — Q10 LOCKED)

| Marker | AC |
|--------|----|
| `test_us0120_closure_command_file_exists_active` | AC-1 |
| `test_us0120_closure_command_file_exists_template` | AC-1 |
| `test_us0120_closure_command_file_parity` | AC-1 |
| `test_us0120_dec_0052_phase_role_matrix_includes_closure` | AC-2 |
| `test_us0120_dec_0082_ship_macro_includes_closure` | AC-3 |
| `test_us0120_auto_phase_plan_includes_closure` | AC-4 |
| `test_us0120_release_md_steps_10_12_removed` | AC-5 |
| `test_us0120_closure_verification_schema_defined` | AC-6 |
| `test_us0120_compose_guards_unchanged` | AC-12 |
| `test_us0120_backward_compat_drain_hook` | AC-10 |

Surjective AC coverage: markers 1-3→AC-1, 4→AC-2, 5→AC-3, 6→AC-4, 7→AC-5, 8→AC-6, 9→AC-12, 10→AC-10; AC-7/AC-8/AC-9/AC-11 covered indirectly by markers 1+8/4/6.

## DC check

`dc_check=clean`. No `# US-0120` or `## US-0120` existed prior to THIS write. H1 anchor added per DEC-0076 / BUG-0010 heading policy. Deferral register clean.

## Stop conditions

- `decision_gate=false`
- `missing_acceptance_criteria=none` (12/12 ACs covered)
- `compose_guards=6/6 UNCHANGED`
- `dc_check=clean`
- 10/10 Q LOCKED, 8/8 R ACCEPTED, A1 locked
- Triad baseline `baseline_h2_count=41` preserved (H1 used)
- Codebase map gate: delegated to `/sprint-plan` handoff

## Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called. No write to `mistakes.jsonl`.

## Consequences

- **Positive**: Closure gets exclusive phase ownership (resolves US-0119 fidelity gap); lifecycle follows "one phase, one responsibility".
- **Negative**: New command file (active + template); new validator; new tests; one extra spawn cycle in ship macro.
- **Neutral**: DEC-0052 + DEC-0082 additive scoped edits; compose UNCHANGED; forward-compat only.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=architecture`, `role=tech-lead`, `story_id=US-0120`, `sprint_id=S0120`
- `orchestrator_run_id=manual-20260707-us0120`
- `delivery_mode=ultra_lean`, `macro_phase=plan`
- `fresh_context_marker=tl-US0120-architecture-20260707T215000Z-fresh`
- `timestamp=2026-07-07T21:50:00Z` (UTC)
- `evidence_ref=docs/product/backlog.md (## US-0120 L4072-L4119), docs/product/acceptance.md (US-0120 L147), handoffs/po_to_tl.md (top research + discovery handoffs), docs/engineering/state.md (research checkpoint L1102-L1231 full read), docs/engineering/architecture.md (## US-0096 L1684 + inline refs for US-0043/US-0045/US-0040/US-0048/US-0056 + DC clean + H2 baseline=41)`
- Fresh tech-lead subagent per BUG-0006 / US-0048; no prior chat history.
- Prior proof consumed: `rp-manual-20260707-us0120-research-tl-20260707T214500Z-US-0120`
- Triad baseline `baseline_h2_count=41` preserved via H1 anchor.

## Strict runtime proof (DEC-0038)

- `runtime_proof_id=rp-manual-20260707-us0120-architecture-tl-20260707T215000Z-US-0120`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"plan","orchestrator_run_id":"manual-20260707-us0120","phase_id":"architecture","proof_issued_at":"2026-07-07T21:50:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-manual-20260707-us0120-architecture-tl-20260707T215000Z-US-0120","sprint_id":"S0120","story_id":"US-0120"}`
- `proof_hash=6293266bfcdf3e6e668cf28a34d831e55cc05a17e5dea1fc8ee94b70ca67b99f`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-07-07T22:50:00Z`

## Decision gate

- `decision_gate=false` (no companion DEC per R-0108 — scoped edits to DEC-0052 + DEC-0082 directly)
- `stop_conditions_met=yes`

## Next scheduled phase

- `next_scheduled_phase=/sprint-plan` (tech-lead, third phase of `plan` macro)
- `next_scheduled_role=tech-lead`
- `stop_condition=STOP after architecture completes; hand off via artifacts only to /sprint-plan in fresh tech-lead subagent per BUG-0006`

---
