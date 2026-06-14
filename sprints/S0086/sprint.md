# Sprint S0086

## Metadata

- **sprint_id**: S0086
- **story_refs**: US-0096
- **goal**: Ship **`DELIVERY_MODE`** three-mode lifecycle axis (**`standard`** \| **`ultra_lean`** \| **`mega_quick`**) with Tranche A universal token wins, mode-scoped phase resolver step 0, **`ultra_lean`** macro-phases + layered memory (**`pack.json`**, **`active-context.md`**), **`mega_quick`** routing, optional backlog **`delivery_mode`** routing, quality floor, eight **`test_us0096_*`** contract markers, **`US0096_PAIRS`** parity manifest, runbook operator recipes, and **`delivery_mode`** in **`run_class_hash`** — per **DEC-0082** (composes on **DEC-0052**, **DEC-0062**, **DEC-0054**, **DEC-0080** / **DEC-0081**; research **R-0082**).
- **status**: planned
- **created_at**: 2026-06-13T05:00:00Z
- **orchestrator_run_id**: auto-20260612-01
- **fresh_context_marker**: tl-S0086-US0096-sprint-plan-20260613T050000Z-fresh

## Scope

- **US-0096**: Delivery modes — ultra-lean + mega-quick token lifecycle with layered memory
- **Architecture**: `docs/engineering/architecture.md` `# US-0096`
- **Binding decision**: `decisions/DEC-0082.md` (Accepted 2026-06-13)
- **Research anchor**: `docs/engineering/research.md` `R-0082`

## Non-goals (hard, from DEC-0082 / architecture `# US-0096`)

- No removal of **`standard`** lifecycle or mandatory lean mode for all runs.
- No bypass of tests, release gates, or secrets/publish policy in any mode.
- No deletion of existing handoff paths or **`sprints/Sxxxx/`** layout for **`standard`**.
- No substitution of **`DELIVERY_MODE`** for **`TOKEN_PROFILE`** or **`CAVEMAN_MODE`**.
- No mid-story **`DELIVERY_MODE`** switch (fail closed **`DELIVERY_MODE_SWITCH_MID_STORY`**).
- No fourth triad member — **`active-context.md`** remains non-triad (**DEC-0054** unchanged).
- No weakening **DEC-0080** / **DEC-0081** native chain or drain-advance semantics.
- **Status authority (US-0045)**: US-0096 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0082**; architecture `# US-0096`; research **R-0082**
- **Governance stack**: **DEC-0052** (mode-scoped reinstatement), **DEC-0062** (run-class + **`delivery_mode`**), **DEC-0054** (triad — **`active-context`** excluded), **US-0053** (narrow-read extension), **US-0080** (token metrics), **US-0072** (CAVEMAN orthogonality), **US-0095** / **BUG-0012** (baseline markers), **DEC-0080** / **DEC-0081** (native chain compose), **US-0001** (`/quick`), **US-0017** (template parity), **US-0045** (status authority), **US-0048** / **DEC-0029** (isolation), **US-0056** / **DEC-0038** (strict proof)

## Acceptance criteria coverage (AC-1..AC-12 → T-xxx; surjective, 12 tasks / 12 ACs)

| AC | Description (summary) | Task(s) | Architecture anchor |
|----|-----------------------|---------|---------------------|
| AC-1 | Scratchpad **`DELIVERY_MODE`** + **`LEAN_*`** keys + non-substitution | T-001 | § Three-mode axis |
| AC-2 | **`standard`** byte-compatible — baseline markers preserved | T-003 | § Mode-scoped resolver; baseline test |
| AC-3 | Tranche A universal wins (caps, narrow-read, delta handoffs, touch-graph) | T-002 | § Tranche A universal wins |
| AC-4 | **`ultra_lean`** macro-phases + **`build+verify`** / **`AUTO_IMPLEMENTATION_LOOP`** | T-004 | § ultra_lean macro-lifecycle |
| AC-5 | Layered memory — **`pack.json`** + **`active-context.md`** | T-005, T-006 | § Layered memory |
| AC-6 | **`mega_quick`** routing + seven eligibility codes | T-007 | § mega_quick mode |
| AC-7 | Mode-scoped resolver step 0 + breadcrumbs | T-003 | § Mode-scoped phase resolver |
| AC-8 | Optional backlog **`delivery_mode`** routing | T-008 | § Optional backlog routing |
| AC-9 | Quality floor checklist + **`LEAN_MEMORY_*`** gates | T-009 | § Quality floor |
| AC-10 | Eight **`test_us0096_*`** + **`US0096_PAIRS`** parity + harness **§26Q** | T-010, T-011 | § Contract tests + parity |
| AC-11 | Runbook operator recipes (when to use each mode) | T-012 | § Runbook operator recipes |
| AC-12 | **`delivery_mode`** in **`run_class_hash`** + token-cost evidence column | T-012 | § Run-class extension |

**Multi-AC tasks** (justified by architecture `# US-0096` § Atomic task seeds): **T-003** (AC-7+AC-2), **T-005/T-006** (AC-5 split by warm/hot surfaces), **T-010/T-011** (AC-10 split contract vs parity), **T-012** (AC-11+AC-12). Every AC has ≥1 task; no `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 12
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (12 ≤ 12; at threshold — `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-12 coverage; **strict 1:1 task-to-seed** (12 architecture seeds → T-001..T-012); **not** strict AC bijection (multi-AC tasks above)

## Governance

- **DEC-0082** (binding) — each task cites governing architecture §(s) and DEC §(s).
- **R-0082** (research anchor).
- **DEC-0062** amended — **`delivery_mode`** in run-class; cross-mode comparisons invalid.
- **US-0045** canonical status authority (US-0096 stays OPEN through this sprint).

## Edit surfaces and parity plan

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `.cursor/scratchpad.md` (via example) | `template/.cursor/scratchpad.local.example.md` | T-001 | Positive |
| 2 | All `.cursor/commands/*.md` (phase commands) | `template/.cursor/commands/*.md` | T-002 | Positive |
| 3 | `.cursor/commands/auto.md` | `template/.cursor/commands/auto.md` | T-003, T-004, T-007 | Positive |
| 4 | `docs/engineering/auto-orchestration-reference.md` | `template/docs/engineering/auto-orchestration-reference.md` | T-001, T-003, T-004, T-007, T-008, T-009 | Positive |
| 5 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-002, T-006, T-009, T-012 | Positive |
| 6 | `.cursor/commands/quick.md` | `template/.cursor/commands/quick.md` | T-007 | Positive |
| 7 | `scripts/pack_json_validate.py` (new) | `template/scripts/pack_json_validate.py` | T-005 | Positive |
| 8 | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` | T-011 | Positive |
| 9 | `tests/auto_command_contract_test.py` | (active-only) | T-010 | N/A |
| 10 | `tests/run-tests.ps1` / `tests/run-tests.sh` | (active-only) | T-011 | Harness **§26Q** |
| 11 | `handoffs/active-context.md` (template) | (convention doc in runbook) | T-006 | Contract doc |
| 12 | `work/<story_id>/pack.json` (convention) | (validator only) | T-005 | Schema v1 |

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** weaken **`test_us0095_*`** or **`test_bug0012_*`** under **`DELIVERY_MODE=standard`**.
- Do **not** add **`active-context.md`** to triad enforcement (**DEC-0054**).
- Do **not** allow non-standard **`AUTO_PHASE_*`** without **`PHASE_POLICY_CONFLICT`**.
- Do **not** break **DEC-0080** / **DEC-0081** native-chain spawn-only semantics.

## Post-edit gate sequence (architecture § Contract tests)

1. `pytest -k us0096 tests/auto_command_contract_test.py` → all eight subtests green
2. `pytest -k us0095 tests/auto_command_contract_test.py` → all seven subtests remain green
3. `pytest -k bug0012 tests/auto_command_contract_test.py` → all subtests remain green
4. `python scripts/check_intake_template_parity.py --scope=us-0096` → PASS (**`US0096_PAIRS`**)
5. `python scripts/pack_json_validate.py --help` or fixture validation → **`PACK_*`** codes documented

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Scratchpad + orthogonality (T-001)

- Required keys: **`DELIVERY_MODE`**, **`LEAN_MEMORY_READ`**, **`LEAN_MEMORY_WRITE`**, **`LEAN_COLD_READ_MAX_SECTIONS`**, **`LEAN_STATE_INDEX_ROWS`**, **`AUTO_DELIVERY_ROUTING`**
- Non-substitution paragraph verbatim in reference + runbook

### Tranche A (T-002)

- Default caps **1000/650/3000**; narrow-read in all phase commands; delta handoff guidance; touch-graph runbook §

### Resolver step 0 (T-003)

- Literals: **`resolve_delivery_mode`**, **`reinstatement applies only when delivery_mode=standard`**, **`PHASE_POLICY_CONFLICT`**, **`DELIVERY_MODE_SWITCH_MID_STORY`**
- **`test_us0096_standard_mode_baseline_markers_preserved`** scheduled early in execute ordering

### Layered memory (T-005, T-006)

- **`pack.json`** schema v1 + **`scripts/pack_json_validate.py`** + **`PACK_*`** codes
- **`active-context.md`** template, rollover, non-triad lock

### mega_quick (T-007)

- Seven **`MEGA_QUICK_*`** fail-closed codes; **`quick.md`** enhancements

### Contract + parity (T-010, T-011)

- Eight **`test_us0096_*`** markers per architecture table
- **`US0096_PAIRS`** (7 surface pairs + validator); harness **§26Q**

### Runbook + evidence (T-012)

- Operator recipes table (when to use / avoid each mode)
- **`delivery_mode`** column in token-cost evidence rows; **`run_class_hash`** extension docs

## Risks and mitigations (architecture § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Partial **`ultra_lean`** without validator/index | T-005 + T-006 ship before resolver E2E |
| R2 | **`active-context`** vs triad confusion | T-006 non-triad docs + **`test_us0096_active_context_contract`** |
| R3 | **`standard`** regression | T-003 + T-010 **`test_us0096_standard_mode_baseline_markers_preserved`** early |
| R4 | False **`mega_quick`** routing | T-007 seven fail-closed codes |
| R5 | **`build+verify`** merged spawn complexity | T-012 runbook E2E recipe |
| R6 | **`pack.json`** / **`sprints/`** drift | T-005 coexistence table + no mid-story switch |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 12 acceptance criteria covered surjectively by T-001..T-012.
- `sprints/S0086/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_surjective=true`, `task_count=12`, `within_limit=true`.
- `pytest -k us0096` green; `pytest -k us0095` + `pytest -k bug0012` green; template parity **`--scope=us-0096`** PASS.
- `docs/product/backlog.md` **`## US-0096`** retains **OPEN** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0086`** / **US-0096** — verify AC-1..AC-12 ↔ T-001..T-012 surjective coverage, task-seed bijection (12 seeds → 12 tasks), task-count bound at threshold, governance alignment. Target: `sprints/S0086/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
