# Sprint S0088

## Metadata

- **sprint_id**: S0088
- **story_refs**: US-0098
- **goal**: Ship default-off **dev-loop auto-launch profile** — **`DEV_AUTO_LAUNCH_PROFILE`** scratchpad gate, persisted **`.cursor/dev-environment.json`** schema v1, **`scripts/dev_environment_lib.py`** stdlib helper, four-label detection matrix with **US-0086** precedence, execute step **24** (**24a–24d**) bounded Tier A/B/C relaunch, **`dev_to_qa.md`** evidence tuple + Connect block, explicit **`refresh dev environment`** phrase, eight **`test_us0098_*`** contract markers, **`DEV_ENVIRONMENT_PAIRS`** parity manifest, harness **§26W**, and runbook operator recipes — per **DEC-0084** (composes **US-0085** / **US-0064** / **US-0086** / **US-0093**; research **R-0085**).
- **status**: planned
- **created_at**: 2026-06-14T09:00:00Z
- **orchestrator_run_id**: auto-20260613-01
- **fresh_context_marker**: tl-S0088-US0098-sprint-plan-20260614T090000Z-fresh

## Scope

- **US-0098**: Dev environment auto-launch profile — detect/persist dev runtime, bounded rebuild/relaunch after execute changes, operator connection surface
- **Architecture**: `docs/engineering/architecture.md` `# US-0098`
- **Binding decision**: `decisions/DEC-0084.md` (Accepted 2026-06-14)
- **Research anchor**: `docs/engineering/research.md` `R-0085`

## Non-goals (hard, from DEC-0084 / architecture `# US-0098`)

- No mandatory unbounded **`docker compose watch`** daemon v1 — execute-triggered automation only.
- No **`release-targets.json`** schema change (**US-0064** unchanged).
- No **`.env`** reads — **US-0085** inheritance; names-only refs in persisted profile.
- No always-on relaunch — default **`DEV_AUTO_LAUNCH_PROFILE=off`**; zero overhead when off.
- No replacement of **US-0065** phase QA or **US-0086** test routing — compose only.
- No mandatory **US-0032** user-guide overhead when **`USER_GUIDE_MODE=0`**.
- **Status authority (US-0045)**: US-0098 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0084**; architecture `# US-0098`; research **R-0085**
- **Governance stack**: **DEC-0071** / **US-0085** (no `.env` reads), **US-0064** (connectivity schema unchanged), **US-0086** (remote precedence), **US-0065** (phase QA boundary), **US-0093** (`DEV_SERVER_*` / `process_health` compose), **US-0097** (execute step **23** precedes step **24**), **US-0017** (template parity), **US-0045** (status authority), **US-0048** / **DEC-0029** (isolation), **US-0056** / **DEC-0038** (strict proof), **DEC-0080** / **DEC-0081** (native chain compose)

## Acceptance criteria coverage (AC-1..AC-10 → T-xxx; surjective, 11 tasks / 10 ACs)

| AC | Description (summary) | Task(s) | Architecture anchor |
|----|-----------------------|---------|---------------------|
| AC-1 | Default-off scratchpad **`DEV_AUTO_LAUNCH_PROFILE`** gate | T-002 | § Scratchpad keys |
| AC-2 | Profile schema v1 + gitignore local profile | T-001, T-003 | § Profile schema v1 |
| AC-3 | Four-label detection matrix; fail-closed when unresolved | T-004 | § Detection matrix |
| AC-4 | Execute step **24** bounded relaunch + **`dev_to_qa.md`** evidence | T-004, T-006 | § Execute step 24; § Tier A/B/C |
| AC-5 | Connect block field shapes after relaunch | T-005, T-006 | § Execute step 24 (**24d**) |
| AC-6 | Compose with **US-0064**/**US-0085**/**US-0086**/**`DEV_SERVER_*`** | T-007 | § Detection matrix; § Orthogonality |
| AC-7 | Explicit **`refresh dev environment`** operator path | T-006 | § Execute step 24 |
| AC-8 | Bounded retries + **`DEV_ENV_*`** reason codes | T-003, T-004, T-005 | § Tier A/B/C; § Reason codes |
| AC-9 | Eight **`test_us0098_*`** + **`DEV_ENVIRONMENT_PAIRS`** parity + harness | T-008, T-009, T-011 | § Contract tests + parity |
| AC-10 | Architecture + runbook operator recipes | T-010 | § Runbook operator recipes; **DEC-0084** |

**Multi-AC tasks** (justified by architecture `# US-0098` § Atomic task seeds): **T-003** (AC-2+AC-8), **T-004** (AC-3+AC-4+AC-8), **T-005** (AC-5+AC-8), **T-006** (AC-4+AC-5+AC-7), **T-008/T-009/T-011** (AC-9 split contract vs parity vs harness). Every AC has ≥1 task; no `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 11
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (11 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-10 coverage; **strict 1:1 task-to-seed** (11 architecture seeds → T-001..T-011); **not** strict AC bijection (multi-AC tasks above)

## Governance

- **DEC-0084** (binding) — each task cites governing architecture §(s) and DEC §(s).
- **R-0085** (research anchor).
- **US-0085** inheritance — four-layer secret audit; no `.env` reads.
- **US-0045** canonical status authority (US-0098 stays OPEN through this sprint).

## Edit surfaces and parity plan

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `template/.cursor/dev-environment.json.example` | (self — byte match) | T-001 | Positive |
| 2 | `.gitignore` / `.cursorignore` | `template/.gitignore` or documented exception | T-001 | Positive |
| 3 | `.cursor/scratchpad.md` | `template/.cursor/scratchpad.md` | T-002 | Positive |
| 4 | `.cursor/scratchpad.local.example.md` | `template/.cursor/scratchpad.local.example.md` | T-002 | Positive |
| 5 | `scripts/dev_environment_lib.py` (new) | `template/scripts/dev_environment_lib.py` | T-003, T-004, T-005 | Positive |
| 6 | `.cursor/commands/execute.md` | `template/.cursor/commands/execute.md` | T-006 | Positive |
| 7 | `docs/engineering/auto-orchestration-reference.md` | `template/docs/engineering/auto-orchestration-reference.md` | T-007 | Positive |
| 8 | `docs/engineering/runtime-connectivity.md` | (active-only cross-link) | T-007 | N/A |
| 9 | `tests/auto_command_contract_test.py` | (active-only) | T-008 | N/A |
| 10 | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` | T-009 | Positive |
| 11 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-010 | Positive |
| 12 | `tests/run-tests.ps1` / `tests/run-tests.sh` | (active-only) | T-011 | Harness **§26W** |

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** change **`release-targets.json`** schema — **`test_us0098_us0086_compose_no_schema_change`** mandatory.
- Do **not** read **`.env`** in helper or execute step **24** paths.
- Do **not** conflate **docker-host-local** with **US-0086** remote docker — precedence table + regression test.
- Do **not** add mandatory unbounded watch daemon v1.
- Do **not** run step **24** overhead when **`DEV_AUTO_LAUNCH_PROFILE=off`**.

## Post-edit gate sequence (architecture § Contract tests)

1. `pytest -k us0098 tests/auto_command_contract_test.py` → all eight subtests green
2. `python scripts/dev_environment_lib.py --self-test` → **`[DEV_ENVIRONMENT_SELF_TEST_OK]`**
3. `python scripts/check_intake_template_parity.py --scope=dev-environment` → PASS (**`DEV_ENVIRONMENT_PAIRS`**)

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Tranche A — schema + gitignore + scratchpad (T-001, T-002)

- **`template/.cursor/dev-environment.json.example`** schema v1 (names-only)
- **`.gitignore`** + **`.cursorignore`** local profile lines
- Scratchpad **`DEV_AUTO_LAUNCH_PROFILE`**, **`DEV_ENVIRONMENT_CONFIG`**

### Tranche B — stdlib helper (T-003, T-004, T-005)

- **`load_profile`**, schema validation, security heuristics, **`--self-test`**
- **`detect_mode`**, **`classify_touched_files`**, **`build_relaunch_plan`**
- **`format_connect_block`** + reason-code registry constants

### Tranche C — execute step 24 (T-006, T-007)

- Execute step **24** (**24a–24d**) after step **23**; zero overhead when profile **`off`**
- **`dev_to_qa.md`** evidence tuple prose
- **`auto-orchestration-reference.md`** dev auto-launch § + **`runtime-connectivity.md`** cross-link

### Tranche D — validators + tests (T-008, T-009, T-010, T-011)

- Eight **`test_us0098_*`** markers; **`DEV_ENVIRONMENT_PAIRS`**; harness **§26W**
- Runbook operator recipes (enable, seed, refresh, troubleshooting, precedence)

## Risks and mitigations (architecture § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Relaunch loops / duplicate containers | T-004 bounded **`retry_count`≤2** + idempotent profile writes |
| R2 | docker-host-local vs remote conflation | T-004 precedence + T-008 **`test_us0098_detection_mode_precedence_literals`** |
| R3 | Secret leakage in persisted profile | T-001 gitignore + T-003 four-layer audit |
| R4 | Execute step proliferation | T-002 default-off gate; T-006 zero overhead when **`off`** |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 10 acceptance criteria covered surjectively by T-001..T-011.
- `sprints/S0088/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_surjective=true`, `task_count=11`, `within_limit=true`.
- `pytest -k us0098` green; parity **`--scope=dev-environment`** PASS; helper self-test green.
- `docs/product/backlog.md` **`## US-0098`** retains **OPEN** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0088`** / **US-0098** — verify AC-1..AC-10 ↔ T-001..T-011 surjective coverage, task-seed bijection (11 seeds → 11 tasks), task-count bound, governance alignment. Target: `sprints/S0088/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
