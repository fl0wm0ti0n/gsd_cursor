
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