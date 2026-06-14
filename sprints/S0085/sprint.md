# Sprint S0085

## Metadata

- **sprint_id**: S0085
- **bug_refs**: BUG-0012
- **goal**: Close **DEC-0080** contract-vs-runtime gap for native-chain orchestrator compliance — orchestrator **MUST Task-spawn** mandate, native-chain precedence over US-0088 Option B, drain-advance step 7 no-stop, continuation-truth breadcrumbs (`native_chain_continuing`, `drain_advance_action`), four **`test_bug0012_*`** contract markers, forbidden-prose negative grep, runbook multi-segment E2E, and 6-surface template parity — per **DEC-0081** (amends **DEC-0080** enforcement layer only; composes on **DEC-0078**, **BUG-0006**, **DEC-0069**; research **R-0083**).
- **status**: planned
- **created_at**: 2026-06-12T22:30:00Z
- **orchestrator_run_id**: auto-20260612-01
- **fresh_context_marker**: tl-S0085-BUG0012-sprint-plan-20260612T223000Z-fresh

## Scope

- **BUG-0012**: `/auto` full_autonomy stops after each story despite native chain (US-0095 regression)
- **Architecture**: `docs/engineering/architecture.md` `# BUG-0012`
- **Binding decision**: `decisions/DEC-0081.md` (Accepted 2026-06-12)
- **Research anchor**: `docs/engineering/research.md` `R-0083`

## Non-goals (hard, from DEC-0081 / architecture `# BUG-0012`)

- No weakening **BUG-0006** spawn-only or **DEC-0078** hard gates.
- No removal of **`scripts/auto_outer_driver.py`** — optional fallback preserved.
- No change to **US-0096** delivery-mode axis.
- No rewrite of **DEC-0080** intent — enforcement-layer amendment only.
- No modification of **DEC-0038** strict-proof tuple schema (additive breadcrumb fields only).
- No fabrication of `state.md` runtime checkpoints during doc edits (comments/examples only).
- **Status authority (US-0045)**: BUG-0012 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0081**; architecture `# BUG-0012`; research **R-0083**
- **Governance stack**: **DEC-0080** (amended enforcement only), **DEC-0078** (hard gates unchanged), **US-0095** / **S0084** (prior delivery — additive layer), **US-0088** (Option B scoped to fallback), **US-0092** (outer driver fallback), **BUG-0006** / **US-0069** (spawn-only), **DEC-0069** (resume_brief pairing), **US-0017** (template parity), **US-0045** (status authority), **US-0048** / **DEC-0029** (isolation), **US-0056** / **DEC-0038** (strict proof)

## Acceptance criteria coverage (AC-1..AC-8 → T-xxx; surjective, 8 tasks / 8 ACs)

| AC | Description (summary) | Task(s) | Architecture anchor |
|----|-----------------------|---------|---------------------|
| AC-1 | Orchestrator **MUST Task-spawn** mandate + actor distinction | T-001 | § Orchestrator compliance contract |
| AC-2 | Native chain precedence over US-0088 Option B | T-002 | § Native-chain precedence |
| AC-3 | Drain-advance step 7 no-stop between steps 6–7 | T-003 | § Drain-advance step 7 enforcement |
| AC-4 | Continuation-truth breadcrumbs | T-003, T-004 | § Continuation-truth breadcrumbs |
| AC-5 | Four **`test_bug0012_*`** contract subtests | T-005 | § Contract tests |
| AC-6 | Forbidden-prose negative grep | T-006 | § Forbidden-prose negative enforcement |
| AC-7 | **`resume_brief`** spawn wording (orchestrator schedules, not operator re-`/auto`) | T-004 | § `resume_brief` + reference alignment |
| AC-8 | Runbook multi-segment E2E + template parity | T-007, T-008 | § Operator E2E recipe; § Template parity |

**Multi-AC tasks** (justified by architecture `# BUG-0012` § Atomic task seeds): **T-003** (AC-3+AC-4), **T-004** (AC-4+AC-7), **T-007** (AC-8 runbook), **T-008** (AC-8 parity). Every AC has ≥1 task; no `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 8
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (8 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-8 coverage; **strict 1:1 task-to-seed** (8 architecture seeds → T-001..T-008); **not** strict AC bijection (T-003/T-004 share AC-4; T-007/T-008 share AC-8)

## Governance

- **DEC-0081** (binding) — each task cites governing architecture §(s) and DEC §(s).
- **R-0083** (research anchor).
- **DEC-0080** composed — amendment to enforcement layer only; all seven **`test_us0095_*`** must remain green.
- **US-0045** canonical status authority (BUG-0012 stays OPEN through this sprint).

## Edit surfaces and parity plan

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `.cursor/commands/auto.md` | `template/.cursor/commands/auto.md` | T-001, T-002, T-003, T-004 | Positive (US-0017) |
| 2 | `docs/engineering/auto-orchestration-reference.md` | `template/docs/engineering/auto-orchestration-reference.md` | T-002, T-003, T-004 | Positive |
| 3 | `handoffs/resume_brief.md` (pairing contract lines) | (template pairing guidance in reference) | T-004 | Pairing contract |
| 4 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-007 | Positive |
| 5 | `tests/auto_command_contract_test.py` | (active-only) | T-005, T-006, T-008 | N/A — contract tests active-only |
| 6 | `docs/engineering/architecture.md` `# BUG-0012` | (active-only) | T-008 | Linkage assert only |

**Active-only** (read-only or reference at execute):

- `docs/engineering/state.md` (breadcrumb field docs / comments in T-003/T-004)
- `scripts/check_intake_template_parity.py` (scope extension `--scope=bug-0012` if needed)

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** weaken spawn-only (**BUG-0006**) or **DEC-0078** hard gates.
- Do **not** mandate outer driver for IDE **`full_autonomy`** primary path.
- Do **not** break any seven **`test_us0095_*`** subtests — **BUG-0012** is additive only.

## Post-edit gate sequence (architecture § Contract tests)

1. `pytest -k bug0012 tests/auto_command_contract_test.py` → all four subtests green
2. `pytest -k us0095 tests/auto_command_contract_test.py` → all seven subtests remain green
3. `python scripts/check_intake_template_parity.py --scope=bug-0012` (or equivalent 6-row inventory) → PASS for touched surfaces
4. Forbidden-pattern negative grep passes in native-chain + full_autonomy normative blocks

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Orchestrator mandate (T-001)

- Required literals: `orchestrator MUST Task-spawn`, `post-subagent continuation`, `phase-role stop is not run terminal`
- Actor distinction: phase-role subagent stops; orchestrator continues when schedulable

### Native-chain precedence (T-002)

- Required literal: `native chain supersedes Option B`
- US-0088 matrix + Steps item 5 scoped to **`NATIVE_CHAIN_UNAVAILABLE`** / headless only

### Drain-advance + breadcrumbs (T-003, T-004)

- Step 6→7 immediate spawn — no operator stop between
- Fields: `native_chain_continuing`, `drain_advance_action` documented with semantics
- **DEC-0069** pairing: orchestrator **MUST Task-spawn** — not operator re-`/auto`

### Contract tests (T-005, T-006)

- Four `test_bug0012_*` markers per architecture table
- Negative grep subtest covers forbidden drain-stop prose

### Runbook E2E (T-007)

- § **BUG-0012 regression verify** — ≥2 story segments, single `/auto`, evidence fields

### Template parity (T-008)

- 6-surface inventory: `auto.md`, reference, `resume_brief` pairing, contract tests, architecture `# BUG-0012`, runbook E2E
- Read-only DEC-0081 + architecture linkage assert

## Risks and mitigations (architecture § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Doc fix passes tests; runtime still stops | T-007 operator E2E recipe + `native_chain_continuing` attestation |
| R2 | Over-broad edits relax hard gates | T-005/T-006 assert **DEC-0078** unchanged; forbidden grep scoped |
| R3 | Phase-role vs orchestrator conflation | T-001 actor distinction diagram + mandate literals |
| R4 | **AUTO_QUIET=1** messaging ambiguity | T-001 scheduling independent of quiet; forbidden wait prose |
| R5 | Break **US-0095** contract tests | T-008 preserves all **`test_us0095_*`** green |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 8 acceptance criteria covered surjectively by T-001..T-008.
- `sprints/S0085/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_surjective=true`, `task_count=8`, `within_limit=true`.
- `pytest -k bug0012` green; `pytest -k us0095` green; template parity for touched surfaces.
- `docs/product/backlog.md` **`### BUG-0012`** retains **OPEN** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0085`** / **BUG-0012** — verify AC-1..AC-8 ↔ T-001..T-008 surjective coverage, task-count bound, governance alignment. Target: `sprints/S0085/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
