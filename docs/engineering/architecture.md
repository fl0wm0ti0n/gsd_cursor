
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

# US-0108 — Sovereign Parallel Instance Arbitrage (Parallel Dev v1)

## Normative locks

- Decision: **DEC-0108** (status=locked; `decisions/DEC-0108.md`).
- Research anchor: **R-0096** (Q1–Q10 CLOSED; `docs/engineering/research.md`).
- Scratchpad keys: `SOVEREIGN_PARALLEL_DEV=0` (default), `AUTO_SOVEREIGN_PARALLEL_N=3`, `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL=6`, `AUTO_SOVEREIGN_MERGE_RESOLVE=first_pass_wins`, `AUTO_SOVEREIGN_WORKTREE_KEEP=0`, `AUTO_SOVEREIGN_PARALLEL_QA=0`.
- Failure modes (reason codes): `PARALLEL_DEV_RESOURCE_CAP_EXHAUSTED`, `PARALLEL_DEV_ALL_FAIL`, `PARALLEL_DEV_MERGE_FAILED`, `PARALLEL_DEV_PICK_MANUAL_REQUIRED`.

## Layered contract (L1–L10)

| Layer | Summary |
|-------|---------|
| **L1 Feature gate** | `SOVEREIGN_PARALLEL_DEV=0` default (zero overhead) |
| **L2 Worktree isolation** | deterministic naming `us0108-<story_id>-<instance_idx>`, one per N dev |
| **L3 QA arbiter** | sequential N QA by default; `AUTO_SOVEREIGN_PARALLEL_QA=0|1` |
| **L4 Selection predicate** | filter `qa_verdict=PASS` → sort `-anti_slop_score` → tie-break earliest `proof_issued_at` |
| **L5 Merge policy** | `first_pass_wins|last_pass_wins|manual`; winner `git merge --ff-only`; artifact `handoffs/parallel_dev_pick.json` v1 |
| **L6 Resource guard** | `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL` atomic cap at spawn |
| **L7 Execute integration** | steps 25 (spawn N dev) → 26 (QA cross-review) → 27 (selection) → 28 (merge+cleanup) |
| **L8 Backward compat** | flag off ⇒ single US-0047 dev, no worktrees |
| **L9 Contract tests** | 8 markers `test_us0108_*`; parity `--scope=sovereign-parallel-dev` |
| **L10 Compose (read-only)** | reads US-0104 anti-slop + US-0103 ledger + US-0107 deferrals; does NOT write their schemas |

## AC → task mapping (surjective)

- AC-1 → T-001 (feature gate)
- AC-2 → T-002 (worktree isolation), T-003 (worktree cleanup)
- AC-3 → T-004 (QA arbiter protocol)
- AC-4 → T-005 (selection predicate), T-006 (anti-slop read-only)
- AC-5 → T-007 (merge policy), T-008 (merge artifact schema), T-009 (retry + halt)
- AC-6 → T-010 (resource guard)
- AC-7 → T-011 (execute steps 25-28), T-012 (lib module)
- AC-8 → T-013 (validator CLI), T-014 (parity scope)
- AC-9 → T-015 (contract tests), T-016 (regression test backward compat)
- AC-10 → T-017 (runbook section), T-018 (decisions.md entry)
- AC-11 → T-019 (reason codes)
- AC-12 → T-020 (template parity)

**Total**: 20 task seeds ≤ SPRINT_MAX_TASKS=24 — single sprint S0108.

## Tranche order

1. **A scratchpad+gitignore** (T-001, T-020): gate + template parity
2. **B lib module** (T-012): `scripts/sovereign_parallel_dev_lib.py`
3. **C worktree isolation** (T-002, T-003): `parallel_dev_worktree.py`
4. **D QA arbiter + selection + merge** (T-004, T-005, T-006, T-007, T-008, T-009): `parallel_dev_arbiter.py`
5. **E resource guard** (T-010)
6. **F execute integration steps 25-28** (T-011)
7. **G validator CLI + parity scope** (T-013, T-014)
8. **H contract tests + regression** (T-015, T-016)
9. **I runbook + decisions** (T-017, T-018, T-019)

## Compose guards (non-amend)

- **US-0047** (bulk execute): system-wide cap, no per-bulk-item change
- **US-0092** (full autonomy): no change to stop matrix
- **US-0103** (ledger): read-only
- **US-0104** (critic): read-only anti-slop scores
- **US-0107** (sovereign loop): read-only deferral register (winner/loser outcomes)

## Consequences

- Sprint: S0108 in `sprints/S0108/`
- Sprint artifact set: `sprint.md`, `sprint.json`, `tasks.md`, `progress.md`, `plan-verify.json`, `summary.md`, `execute-findings.md`, `qa-findings.md`, `qa-verdict.json`, `verify-work-verdict.json`, `verify-work-findings.md`, `release-findings.md`
- Handoffs: `tl_to_dev`, `qa-to-verify-work`, `verify-work-to-release`, `release_to_refresh`
- Release notes: `handoffs/releases/S0108-release-notes.md`
- Tests: `tests/us0108_contract_test.py` (8 markers)

