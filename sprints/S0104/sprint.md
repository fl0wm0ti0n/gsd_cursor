# Sprint S0104

## Metadata

- **sprint_id**: S0104
- **story_refs**: US-0104
- **goal**: Ship **cross-model adversarial critic** — default-off **`CROSS_MODEL_REVIEW`** scratchpad gate, **`scripts/sovereign_critic_lib.py`** three-lens parallel jury + tier-opposition model selection, **`scripts/sovereign_critic_validate.py`** validator CLI, **`.cursor/commands/sovereign-critic.md`** orchestrator hook, anti-slop rework loop, isolation **`model_id`** v2 extension, degraded single-model-multi-lens fallback, eight **`test_us0104_*`** contract markers, **`SOVEREIGN_CRITIC_PAIRS`** parity manifest, and runbook operator recipes — per **DEC-0104** (composes **US-0048** / **US-0069** / **US-0023** / **US-0110** / **US-0103** additive only; research **R-0092**).
- **status**: planned
- **created_at**: 2026-06-28T23:00:00Z
- **orchestrator_run_id**: auto-20260628-04
- **fresh_context_marker**: tl-S0104-US0104-sprint-plan-20260628T230000Z-fresh

## Scope

- **US-0104**: Cross-Model Adversarial Critic — per-phase critic subagent with Challenger/Architect/Subtractor lenses + anti-slop scoring
- **Architecture**: `docs/engineering/architecture.md` `# US-0104`
- **Binding decision**: `decisions/DEC-0104.md` (Accepted 2026-06-28)
- **Research anchor**: `docs/engineering/research.md` `R-0092` (closed Q1–Q7)

## Non-goals (hard, from DEC-0104 / architecture `# US-0104`)

- No amendment of **US-0048** / **US-0069** / **US-0023** / **US-0110** base semantics — compose, do not amend.
- No always-on critic — default **`CROSS_MODEL_REVIEW=0`**; zero overhead when off.
- No change to **`min(lens_scores)`** aggregate formula — **US-0108** consumer depends on stable formula.
- No runtime lens invention beyond **`challenger` \| `architect` \| `subtractor`** enum.
- No new canonical phase role for critic — orchestrator-spawned command per **US-0069** compose rule.
- **Status authority (US-0045)**: US-0104 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0104**; architecture `# US-0104`; research **R-0092** (closed); research stub **`scripts/sovereign_critic_lib.py`**
- **Governance stack**: **US-0048** (isolation evidence — additive `model_id` only), **US-0069** (phase role enforcement — unchanged), **US-0023** (fresh-context semantics — unchanged), **US-0110** (`CRITIC_PATH` / conjunct 3 — unchanged), **US-0103** (`cross_model_reviewed` ledger field — additive hook), **US-0101** / **US-0102** (model resolution read-only via `model_tier_lib`), **US-0108** (anti-slop aggregate consumer — formula frozen), **US-0017** (template parity), **US-0045** (status authority)

## Acceptance criteria coverage (AC-1..AC-8 → T-xxx; surjective, 11 tasks / 8 ACs)

| AC | Description (summary) | Task(s) | Architecture anchor |
|----|-----------------------|---------|---------------------|
| AC-1 | Scratchpad keys `CROSS_MODEL_REVIEW`, `CROSS_MODEL_ANTISLOP_THRESHOLD`, `CROSS_MODEL_REWORK_MAX` + defaults + zero-overhead when `0` | T-001, T-002 | § Scratchpad keys |
| AC-2 | `/sovereign-critic` command + template mirror; orchestrator hook after producer phase when enabled | T-006 | § `/sovereign-critic` command |
| AC-3 | Three-lens enum + all lenses per invocation; reconciliation via `reconcile_findings` | T-003, T-006 | § Three lenses + parallel jury |
| AC-4 | Isolation evidence `model_id` v2 additive extension + `ISOLATION_EVIDENCE_MODEL_ID_MISSING` fail-closed | T-008 | § Isolation evidence `model_id` v2 |
| AC-5 | `sovereign_critic_lib.py` core + IO + `sovereign_critic_validate.py` validator CLI | T-003, T-004, T-005 | § Helper library; § Validator CLI |
| AC-6 | Anti-slop aggregate `min(lens_scores)` + bounded rework loop + `dev_to_qa.md` `critic_evidence` tuple | T-007 | § Anti-slop rubric + rework |
| AC-7 | Degraded single-model-multi-lens fallback + `degraded_mode` findings flag + backward compatibility | T-009, T-011 | § `select_critic_model`; § Backward compatibility |
| AC-8 | Eight `test_us0104_*` markers, reason codes, parity, runbook; architecture `# US-0104` pre-satisfied | T-002, T-005, T-010, T-011 | § Contract tests + parity; § Reason codes |

**Multi-AC tasks** (justified by architecture `# US-0104` § Atomic task seeds): **T-002** (AC-1+AC-8), **T-003** (AC-3+AC-5), **T-005** (AC-5+AC-8), **T-006** (AC-2+AC-3), **T-011** (AC-7+AC-8). Every AC has ≥1 task; no `PLAN_AC_COVERAGE_GAP`.

**AC-8 architecture pre-satisfied** at `/architecture` (`# US-0104` written in architecture phase).

## Task count

- **Total**: 11
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (11 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-8 coverage; **strict 1:1 task-to-seed** (11 architecture seeds → T-001..T-011)

## Governance

- **DEC-0104** (binding) — each task cites governing architecture §(s) and DEC §(s).
- **R-0092** (research anchor — closed).
- **US-0110** compose — `CRITIC_PATH` unchanged; US-0104 populates `handoffs/sovereign_critic_findings.jsonl`.
- **US-0045** canonical status authority (US-0104 stays OPEN through this sprint).

## Edit surfaces and parity plan

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `.cursor/scratchpad.md` | `template/.cursor/scratchpad.md` | T-001, T-002 | Positive |
| 2 | `docs/engineering/reason_codes.md` | (active-only) | T-002 | N/A |
| 3 | `decisions/DEC-0104.md` | `template/decisions/DEC-0104.md` | T-002 | Positive |
| 4 | `scripts/sovereign_critic_lib.py` | `template/scripts/sovereign_critic_lib.py` | T-003, T-004 | Positive |
| 5 | `scripts/sovereign_critic_validate.py` | `template/scripts/sovereign_critic_validate.py` | T-005 | Positive |
| 6 | `.cursor/commands/sovereign-critic.md` | `template/.cursor/commands/sovereign-critic.md` | T-006 | Positive |
| 7 | `handoffs/sovereign_critic_findings.jsonl` | (runtime artifact) | T-004 | N/A |
| 8 | `tests/us0104_contract_test.py` | (active-only) | T-010 | N/A |
| 9 | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` | T-011 | Positive |
| 10 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-011 | Positive |

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** amend **US-0048** / **US-0069** / **US-0023** / **US-0110** base semantics.
- Do **not** enable critic by default — `CROSS_MODEL_REVIEW=0` is zero-overhead discipline.
- Do **not** change **`min(lens_scores)`** aggregate formula.
- Do **not** invent runtime lenses beyond the three-lens enum.

## Post-edit gate sequence (architecture § Contract tests)

1. `pytest -k us0104` → all eight subtests + compose guards green
2. `python scripts/sovereign_critic_lib.py --self-test` → `[SOVEREIGN_CRITIC_SELF_TEST_OK]`
3. `python scripts/sovereign_critic_validate.py --self-test` → `[SOVEREIGN_CRITIC_VALIDATION_OK]`
4. `python scripts/check_intake_template_parity.py --scope=sovereign-critic` → PASS (**`SOVEREIGN_CRITIC_PAIRS`**)

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Tranche A — scratchpad keys + reason codes (T-001..T-002)

- Three **`CROSS_MODEL_*`** keys in active + template scratchpad (byte-parity)
- Comment block documenting default-off + anti-slop + rework cap semantics
- 10 reason codes in `docs/engineering/reason_codes.md` § US-0104
- **`DEC-0104`** template mirror

### Tranche B — critic library core + IO (T-003..T-004)

- Finalize **`sovereign_critic_lib.py`** from research stub: core API + `self_test`
- IO helpers: `append_finding`, `read_open_blocking`, `resolve_finding`, `build_qa_cross_reviewer_block`, `patch_ledger_cross_model_reviewed`

### Tranche C — validator + command (T-005, T-006)

- **`scripts/sovereign_critic_validate.py`** + template mirror
- **`.cursor/commands/sovereign-critic.md`** + three-lens prompt templates + `/auto` hook prose

### Tranche D — rework + isolation + degraded (T-007, T-008, T-009)

- `/auto` post-phase hook + anti-slop rework loop + `CROSS_MODEL_REWORK_CAP_EXHAUSTED` gate
- Isolation evidence **`model_id`** v2 additive extension
- Degraded single-model-multi-lens orchestration + `degraded_mode` findings flag

### Tranche E — contract tests + parity + runbook (T-010, T-011)

- Eight **`test_us0104_*`** contract markers + compose regression guards in `tests/us0104_contract_test.py`
- **`SOVEREIGN_CRITIC_PAIRS`** parity scope `--scope=sovereign-critic`
- Runbook `### Cross-Model Adversarial Critic (US-0104)` + zero-overhead default-off path

## Risks and mitigations (architecture § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Model routing unreliable (**R-0088**) | T-009: deterministic degraded fallback |
| R2 | Phase latency / token cost | T-001: default-off `CROSS_MODEL_REVIEW=0` |
| R3 | Rework oscillation | T-007: `CROSS_MODEL_REWORK_MAX` + decision gate |
| R4 | Anti-slop subjectivity | T-003: deterministic checklist rubric |
| R5 | Jury dedup drift | T-003: stable `issue_key` algorithm |
| R6 | **US-0108** aggregate coupling | Frozen `min(lens_scores)` — no formula change |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 8 acceptance criteria covered surjectively (AC-1..AC-8 → T-001..T-011).
- `sprints/S0104/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_surjective=true`, `task_count=11`, `within_limit=true`.
- `pytest -k us0104` green; parity **`--scope=sovereign-critic`** PASS.
- `python scripts/sovereign_critic_lib.py --self-test` → `[SOVEREIGN_CRITIC_SELF_TEST_OK]`.
- `python scripts/sovereign_critic_validate.py --self-test` → `[SOVEREIGN_CRITIC_VALIDATION_OK]`.
- `docs/product/backlog.md` **`## US-0104`** retains **OPEN** through plan-verify / execute / qa / verify-work; closure at `/release` (**US-0045**).

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0104`** / **US-0104** — verify AC-1..AC-8 ↔ T-001..T-011 surjective coverage, task-count bound, governance alignment. Target: `sprints/S0104/plan-verify.json` **`PENDING`** → **`PASS`**.
