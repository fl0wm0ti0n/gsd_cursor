# Sprint S0103

## Metadata

- **sprint_id**: S0103
- **story_refs**: US-0103
- **goal**: Ship **AI Decision Ledger + Plan Fidelity policy** — append-only JSONL decision ledger per orchestrator run + plan-fidelity tri-state governance (strict/relaxed/extended) + QA cross-check contract — default-off (`AI_DECISION_LEDGER=0`), composable with US-0070/US-0069/US-0048/US-0092.
- **status**: planned
- **created_at**: 2026-06-28T13:10:00Z
- **orchestrator_run_id**: auto-20260628-01
- **fresh_context_marker**: tl-S0103-US0103-architecture-20260628T131000Z-fresh

## Scope

- **US-0103**: AI Decision Ledger + Plan Fidelity policy (sovereign-loop foundation)
- **Architecture**: `docs/engineering/architecture.md` `# US-0103`
- **Binding decision**: `decisions/DEC-0103.md` (Accepted 2026-06-28)
- **Research anchor**: `docs/engineering/research.md` `R-0089` (resolved 2026-06-28)

## Non-goals (hard, from DEC-0103 / architecture `# US-0103`)

- No amendment of **US-0070** / **US-0069** / **US-0048** / **US-0092** — composable, do not amend.
- No always-on ledger — default-off (`AI_DECISION_LEDGER=0`) preserves zero-overhead discipline.
- No mandatory QA/release gate weakening — US-0103 writes alongside, never mutates existing files.
- No changes to isolation evidence semantics — US-0103 may reference isolation evidence as `from_artifact` but does not alter US-0048 contracts.
- **Status authority (US-0045)**: US-0103 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0103**; architecture `# US-0103`; `R-0089` (resolved)
- **Governance stack**: **DEC-0051** (phase→role matrix), **US-0070** (phase selection — unchanged), **US-0069** (phase role enforcement — unchanged), **US-0048** (isolation — unchanged), **US-0092** (full-autonomy outer driver — unchanged), **US-0111** (ledger consumer — composes), **US-0017** (template parity), **US-0045** (status authority)

## Acceptance criteria coverage (AC-1..AC-8 → T-xxx; surjective, 11 tasks / 8 ACs)

| AC | Description (summary) | Task(s) | Architecture anchor |
|----|-----------------------|---------|---------------------|
| AC-1 | Scratchpad keys `AI_DECISION_LEDGER=0|1` + `AUTO_PLAN_FIDELITY=strict|relaxed|extended`; zero-overhead default | T-001 | § Scratchpad keys |
| AC-2 | Artifact `handoffs/sovereign_decisions/<orchestrator_run_id>.jsonl` with 12-field JSONL schema; append-only | T-002, T-003, T-004, T-005 | § Ledger JSONL schema; § Helper library; § Validator CLI |
| AC-3 | strict mode — any unapproved deviation → `PLAN_FIDELITY_VIOLATION` hard stop; operator-approved relaxations via scratchpad override recorded | T-002, T-003 | § Plan-fidelity deviation classification table |
| AC-4 | relaxed mode — AI may drop/reorder ACs with ledger entry + QA-verifiable; new ACs/stories results in decision gate | T-003 | § Plan-fidelity deviation classification table |
| AC-5 | extended mode — AI may extend scope with new stories/features; documented but non-blocking; QA still cross-checks | T-003 | § Plan-fidelity deviation classification table |
| AC-6 | QA cross-check — `/qa` phase reads ledger + emits `ledger_findings` in `qa-findings.md` | T-006 | § QA cross-check contract |
| AC-7 | Contract tests `test_us0103_*` for scratchpad, schema, tri-state, QA cross-check | T-007, T-008, T-009, T-010 | § Contract tests + parity |
| AC-8 | Documentation runbook + architecture `# US-0103`; template/ byte-parity; reason codes `PLAN_FIDELITY_*` + `LEDGER_*` inventory | T-002, T-003, T-006, T-011 | § Reason codes; § Integration points |

**Multi-AC tasks** (justified by architecture `# US-0103` § Atomic task seeds): **T-002** (AC-2+AC-3), **T-003** (AC-2+AC-4+AC-5), **T-004** (AC-2+AC-8), **T-005** (AC-2+AC-8), **T-006** (AC-6+AC-8), **T-011** (AC-8). Every AC has ≥1 task or architecture-phase attestation; no `PLAN_AC_COVERAGE_GAP`.

**AC-11 architecture pre-satisfied** at `/architecture` (T-011 anchor: `# US-0103` written in this phase).

## Task count

- **Total**: 11
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (11 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-8 coverage; **strict 1:1 task-to-seed** (11 architecture seeds → T-001..T-011)

## Governance

- **DEC-0103** (binding) — each task cites governing architecture §(s) and DEC §(s).
- **US-0070** compose — phase selection policy unchanged; ledger writes on top of `resolved_phase_plan`.
- **US-0069** compose — phase role enforcement unchanged; ledger `role` field records who emitted.
- **US-0048** compose — isolation evidence unchanged; ledger entry may reference isolation evidence.
- **US-0092** compose — outer driver unchanged; ledger writes fire as side-effect of phase transitions.
- **US-0045** canonical status authority (US-0103 stays OPEN through this sprint).

## Edit surfaces and parity plan

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `.cursor/scratchpad.md` | `template/.cursor/scratchpad.md` | T-001 | Positive |
| 2 | `.cursor/scratchpad.local.example.md` | `template/.cursor/scratchpad.local.example.md` | T-001 | Positive |
| 3 | `scripts/decision_ledger_lib.py` | `template/scripts/decision_ledger_lib.py` | T-004 | Positive |
| 4 | `scripts/ledger_validate.py` | `template/scripts/ledger_validate.py` | T-004, T-005 | Positive |
| 5 | `handoffs/sovereign_decisions/.gitkeep` | `template/handoffs/sovereign_decisions/.gitkeep` | T-003 | Positive |
| 6 | `handoffs/qa_to_verify.md` | (active-only) | T-006 | N/A |
| 7 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-006, T-011 | Positive |
| 8 | `tests/auto_command_contract_test.py` | (active-only) | T-007 | N/A |
| 9 | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` | T-008 | Positive |
| 10 | `tests/run-tests.ps1` / `tests/run-tests.sh` | (active-only) | T-009 | Harness |
| 11 | `docs/engineering/architecture.md` | `template/docs/engineering/architecture.md` | T-010, T-011 | Active-only (# US-0103 pre-satisfied) |

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** amend **US-0070** / **US-0069** / **US-0048** / **US-0092** semantics.
- Do **not** enable ledger by default — `AI_DECISION_LEDGER=0` is zero-overhead discipline.
- Do **not** weaken QA/release gates — ledger writes alongside, never mutates existing files.
- Do **not** alter isolation evidence contracts — US-0103 may reference but not change US-0048.

## Post-edit gate sequence (architecture § Contract tests)

1. `pytest -k us0103 tests/auto_command_contract_test.py` → all eight subtests green
2. `python scripts/decision_ledger_lib.py --self-test` → `[DECISION_LEDGER_SELF_TEST_OK]`
3. `python scripts/ledger_validate.py --self-test` → `[DECISION_LEDGER_SELF_TEST_OK]`
4. `python scripts/check_intake_template_parity.py --scope=sovereign-ledger` → PASS (**`SOVEREIGN_LEDGER_PAIRS`**)

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Tranche A — scratchpad keys + directory structure (T-001..T-003)

- **`AI_DECISION_LEDGER=0|1`** (default 0) + **`AUTO_PLAN_FIDELITY=strict|relaxed|extended`** (default strict) documented in scratchpad comment block
- `handoffs/sovereign_decisions/.gitkeep` + template mirror (empty directory placeholder)
- `.cursorignore` no-op for ledger directory (ledger is git-tracked, not ignored)

### Tranche B — ledger library + validator (T-004..T-005)

- **`scripts/decision_ledger_lib.py`** — `append_entry()`, `read_entries()`, `schema_check()`, `summary_digest()`, `classify_deviation()`, `build_qa_findings_block()`, `self_test()`
- **`scripts/ledger_validate.py`** — `--file <path>`, `--repo <root>`, `--self-test`, `--enforce`, `--qa-find`
- 12-field JSONL schema v1 (locked in DEC-0103)
- 9 `DecisionType` values (5 `PLAN_FIDELITY_*` + 4 `LEDGER_*`)
- 11 `ReasonCode` values (5 `PLAN_FIDELITY_*` + 6 `LEDGER_*`)

### Tranche C — QA cross-check (T-006)

- `/qa` phase reads ledger → emits `ledger_findings` block in `qa-findings.md`
- 7-field block schema: `orchestrator_run_id`, `ledger_path`, `total_entries`, `violations_count`, `scope_gates_count`, `extensions_count`, `top_violations[]` (max 5)
- Runbook operator recipe — how to audit ledger, how to interpret QA findings

### Tranche D — contract tests + parity + harness (T-007..T-009)

- Eight **`test_us0103_*`** contract subtests
- **`SOVEREIGN_LEDGER_PAIRS`** parity manifest for `--scope=sovereign-ledger` (2 file pairs)
- Harness section for US-0103 in `tests/run-tests.ps1` / `tests/run-tests.sh`

### Tranche E — integration points + backward compat (T-010..T-011)

- Integration points with US-0070/US-0069/US-0048/US-0092 (compose, do not amend)
- Backward compatibility matrix (default-off + composition stability)
- Architecture `# US-0103` pre-satisfied at `/architecture` phase
- Runbook operator recipe — how to audit ledger, how to respond to QA findings

## Risks and mitigations (architecture § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Ledger contention under concurrent writes | T-004: one file per run + append-only + fsync; orchestrator enforces single-writer-per-run |
| R2 | Token budget blow-up on ledger reads | T-004: `summary_digest()` + `last_n=100` bounded reads; 10K lines/run cap |
| R3 | Deviation classification ambiguity | T-004: §3 deviation table is architecture-locked; `classify_deviation()` is single source of truth |
| R4 | Ledger corruption | T-004: `schema_check()` fail-closed per line; non-fatal recoverable append on next valid line; `LEDGER_CORRUPT` hard stop requires operator remediation |
| R5 | Sovereign-loop composition stability | T-009: `test_us0103_us0070_compose_no_schema_change` regression guard; §3 table frozen; US-0104..US-0110 contract depends on v1 schema |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 8 acceptance criteria covered surjectively (AC-1..AC-8 → T-001..T-011).
- `sprints/S0103/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_surjective=true`, `task_count=11`, `within_limit=true`.
- `pytest -k us0103` green; parity **`--scope=sovereign-ledger`** PASS.
- `python scripts/decision_ledger_lib.py --self-test` → `[DECISION_LEDGER_SELF_TEST_OK]`.
- `python scripts/ledger_validate.py --self-test` → `[DECISION_LEDGER_SELF_TEST_OK]`.
- `docs/product/backlog.md` **`## US-0103`** retains **OPEN** through plan-verify / execute / qa / verify-work; closure at `/release` (**US-0045**).

## Next

- **`/sprint-plan`** (fresh **tech-lead**) for **`S0103`** / **US-0103** — materialize sprint from 11 architecture seeds; AC-1..AC-8 bijection check. Target sprint ID: **S0103**.
