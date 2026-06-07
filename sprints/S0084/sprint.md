# Sprint S0084

## Metadata

- **sprint_id**: S0084
- **story_refs**: US-0095
- **goal**: Ship Cursor-native in-chat `/auto` auto-chain — foreground sequential Task loop within one orchestrator session, 7-step IDE drain-advance-without-pause, unified cap/ledger composing **DEC-0078**, outer driver demoted to optional IDE fallback, **`AUTO_QUIET`** messaging rules, **`NATIVE_CHAIN_UNAVAILABLE`** fail-closed, six `test_us0095_*` contract markers, and 8-surface template parity — per **DEC-0080** (composes on **DEC-0078**, **US-0088**, **BUG-0006**, **DEC-0069**; research **R-0081**).
- **status**: planned
- **created_at**: 2026-06-07T20:00:00Z
- **orchestrator_run_id**: auto-20260607-02
- **fresh_context_marker**: tl-S0084-US0095-sprint-plan-20260607T200000Z-fresh

## Scope

- **US-0095**: Native in-Cursor `/auto` auto-chaining (no outer driver required)
- **Architecture**: `docs/engineering/architecture.md` `# US-0095`
- **Binding decision**: `decisions/DEC-0080.md` (Accepted 2026-06-07)
- **Research anchor**: `docs/engineering/research.md` `R-0081`

## Non-goals (hard, from DEC-0080 / architecture `# US-0095`)

- No removal of decision gates; **`decision_gate`** remains hard stop.
- No bypass of QA / release / isolation / strict-proof (**US-0048**, **US-0056**).
- No deletion of **`scripts/auto_outer_driver.py`** — demote to fallback only.
- No in-band orchestrator phase execution (**BUG-0006** / **US-0069** spawn-only unchanged).
- No vendor guarantees beyond documented Cursor foreground Task composition.
- No auto-read **`.env`**, no intake evidence mutation, no publish without **`RELEASE_PUBLISH_MODE=auto`**.
- No new scratchpad keys expected (comments only if needed).
- **Status authority (US-0045)**: US-0095 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0080**; architecture `# US-0095`; research **R-0081**
- **Governance stack**: **DEC-0078** / **US-0092** (outer driver + full_autonomy baseline — forward-link only), **US-0088** (reference Step 5), **US-0044** (backlog drain), **US-0087** (bug-queue mutex), **US-0069** (preflight/post), **DEC-0069** (resume_brief pairing), **US-0017** (template parity), **US-0094** (README intro demotion touch), **US-0045** (status authority), **US-0048** / **DEC-0029** (isolation), **US-0056** / **DEC-0038** (strict proof), **BUG-0006** (spawn-only)

## Acceptance criteria coverage (AC-1..AC-10 → T-xxx; strict bijection)

| AC | Description (summary) | Task | Architecture anchor |
|----|-----------------------|------|---------------------|
| AC-1 | Native in-chat auto-chain contract | T-001 | § Native in-chat auto-chain contract |
| AC-2 | IDE drain-advance-without-pause (7-step) | T-002 | § IDE drain-advance-without-pause |
| AC-3 | Spawn-only preserved (**BUG-0006**) | T-003 | § Native in-chat auto-chain contract (invariants) |
| AC-4 | Hard gates unchanged in stop matrix | T-004 | § Stop matrix |
| AC-5 | Outer driver demoted to fallback | T-005 | § Fallback boundary matrix |
| AC-6 | **`AUTO_QUIET`** messaging rules | T-006 | § `AUTO_QUIET` messaging |
| AC-7 | **DEC-0069** pairing before continuation | T-007 | § IDE drain-advance step 2 |
| AC-8 | Six **`test_us0095_*`** contract subtests | T-008 | § Contract tests + parity |
| AC-9 | Template parity for touched surfaces | T-009 | § Contract tests (`test_us0095_template_parity_auto_surfaces`) |
| AC-10 | Unified caps + security deny-list | T-010 | § Unified cap + ledger |

**Bijection**: **AC-1..AC-10 ↔ T-001..T-010** (strict 1:1 per architecture `# US-0095` § Atomic task seeds, consolidated). No `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 10
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (10 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Bijection**: **task_ac_bijection=true** (10 ACs, 10 tasks; 1:1 mapping)

## Governance

- **DEC-0080** (binding) — each task cites governing architecture §(s).
- **R-0081** (research anchor).
- **DEC-0078** composed — IDE-primary amendment only; outer driver retained.
- **US-0045** canonical status authority (US-0095 stays OPEN through this sprint).

## Edit surfaces and parity plan

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `.cursor/commands/auto.md` | `template/.cursor/commands/auto.md` | T-001, T-002, T-003, T-004, T-006, T-007 | Positive (US-0017) |
| 2 | `docs/engineering/auto-orchestration-reference.md` | `template/docs/engineering/auto-orchestration-reference.md` | T-001, T-002, T-004, T-006, T-007, T-010 | Positive |
| 3 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-005 | Positive |
| 4 | `README.md` (intro ¶3 + pillar) | `template/README.md` | T-005 | Positive (byte-identical per **US-0017**) |
| 5 | `tests/auto_command_contract_test.py` | (active-only) | T-008 | N/A — contract tests active-only |
| 6 | `docs/engineering/architecture.md` `# US-0095` | (active-only) | T-009 | Linkage assert only — no template mirror |

**Active-only** (read-only or reference at execute):

- `handoffs/resume_brief.md` (pairing contract — reference only per **DEC-0069**)
- `docs/engineering/state.md` (breadcrumb field docs in T-010 if needed)
- `.cursor/scratchpad.md` (comments only if touched — none expected)

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** weaken spawn-only (**BUG-0006**) or isolation/strict-proof gates.
- Do **not** mandate outer driver for IDE **`full_autonomy`** primary path.
- Do **not** emit mandatory re-`/auto` or `segment exhausted` terminal when continuation schedulable.

## Post-edit gate sequence (architecture § Contract tests)

1. `pytest -k us0095 tests/auto_command_contract_test.py` → all six subtests green
2. `python scripts/check_intake_template_parity.py --repo .` (or `--scope=us-0095` if wired) → PASS for touched surfaces
3. Forbidden-pattern grep: no mandatory outer-driver / re-`/auto` phrases in IDE-primary sections

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Native chain docs (T-001, T-003)

- Required literals: `Native in-chat auto-chain`, `foreground sequential`, `same /auto orchestrator session`, `NATIVE_CHAIN_UNAVAILABLE`
- Spawn-only invariants documented; no forbidden orchestrator in-band patterns introduced

### Drain-advance (T-002)

- 7-step algorithm + literals: `drain-advance-without-pause`, `immediately`, `without operator re-`/auto``

### Stop matrix (T-004)

- Hard gates table unchanged: `decision_gate`, isolation/strict-proof, security deny, caps, `pause_request`

### Fallback demotion (T-005)

- Runbook: new `### Native in-chat auto-chain (US-0095)`; outer driver subsection demoted to fallback
- README: `/auto` once primary; outer driver optional/fallback (**US-0094** touch)

### AUTO_QUIET (T-006)

- Suppression table in reference + `auto.md`; gates/caps/errors non-suppressible

### DEC-0069 pairing (T-007)

- Mandate `resume_brief` + `state.md` refresh before in-chat continuation; `RESUME_BRIEF_STALE` fail-closed

### Contract tests (T-008)

- Six `test_us0095_*` markers per architecture table

### Template parity (T-009)

- 8-surface inventory: `auto.md`, reference, runbook, README family, contract tests, architecture `# US-0095`

### Caps + security (T-010)

- State breadcrumb fields: `native_chain_active`, `outer_cycle_index`, `implementation_loop_index`
- Ledger `remediation_action` values: `phase_respawn`, `native_chain_continue`, `drain_advance`
- Security deny-list unchanged (**DEC-0078**)

## Risks and mitigations (architecture § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Cursor spawn depth limits | T-001 `NATIVE_CHAIN_UNAVAILABLE` + optional fallback hint |
| R2 | Docs vs behavior drift | T-008 `test_us0095_*` + forbidden-pattern grep |
| R3 | Spawn-only violation | T-003 invariants + `test_us0095_spawn_only_regression` |
| R4 | Stale `resume_brief` | T-007 `RESUME_BRIEF_STALE` fail-closed |
| R5 | IDE vs headless confusion | T-005 fallback matrix primary/fallback labels |
| R6 | Cap desync | T-010 unified ledger documentation |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 10 acceptance criteria covered 1:1 by T-001..T-010.
- `sprints/S0084/plan-verify.json` reaches **PASS** with `plan_integrity.task_ac_bijection=true`, `task_count=10`, `within_limit=true`.
- `pytest -k us0095` green; template parity for touched surfaces.
- `docs/product/backlog.md` **`## US-0095`** retains **`OPEN`** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0084`** / **US-0095** — verify AC-1..AC-10 ↔ T-001..T-010 bijection, task-count bound, governance alignment. Target: `sprints/S0084/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
