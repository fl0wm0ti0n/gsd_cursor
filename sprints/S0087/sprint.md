# Sprint S0087

## Metadata

- **sprint_id**: S0087
- **story_refs**: US-0097
- **goal**: Complete **DEC-0045** / **US-0062** partial delivery — project-owned root **`README.md`** with execute-time bootstrap, mandatory per-shipped-story catalog delta, non-destructive upgrade migration (**M1–M5**), gate separation from **US-0091** / **DEC-0074** (framework paths under **`its_magic/`** only), new **`validate_project_readme_coverage.py`**, release step **3g**, scratchpad **`PROJECT_README_ENFORCE`** / **`FRAMEWORK_KIT_REPO`**, eight **`test_us0097_*`** contract markers, **`PROJECT_README_PAIRS`** parity manifest, and runbook operator recipes — per **DEC-0083** (amends **DEC-0045**; reframes **DEC-0074** paths; research **R-0084**).
- **status**: planned
- **created_at**: 2026-06-13T23:00:00Z
- **orchestrator_run_id**: auto-20260613-01
- **fresh_context_marker**: tl-S0087-US0097-sprint-plan-20260613T230000Z-fresh

## Scope

- **US-0097**: Project-owned root README bootstrap + per-story/sprint growth (framework README in **`its_magic/`** only)
- **Architecture**: `docs/engineering/architecture.md` `# US-0097`
- **Binding decision**: `decisions/DEC-0083.md` (Accepted 2026-06-13)
- **Research anchor**: `docs/engineering/research.md` `R-0084`

## Non-goals (hard, from DEC-0083 / architecture `# US-0097`)

- No single combined framework + project README at root.
- No extension of **US-0091** validator to cover project root (split validators only).
- No deletion of operator-authored project prose when **S5** detected (**M2** preserve).
- No **`FRAMEWORK_KIT_REPO=1`** default for consumer repos.
- No rewrite of **DEC-0074** body — path reframe via **DEC-0083** + architecture only.
- No mandatory **US-0032** user-guide overhead when **`USER_GUIDE_MODE=0`**.
- No removal of framework catalog from **`its_magic/README.md`**.
- **Status authority (US-0045)**: US-0097 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0083**; architecture `# US-0097`; research **R-0084**
- **Governance stack**: **DEC-0045** (amended — installer boundary completion), **DEC-0074** (path reframe — **US-0091**), **US-0062** (partial delivery completion), **US-0091** (framework validator reframe), **US-0071** (prose hygiene compose **23c**), **US-0030** (delta doc gate unchanged), **US-0017** (template parity), **US-0045** (status authority), **US-0048** / **DEC-0029** (isolation), **US-0056** / **DEC-0038** (strict proof), **DEC-0080** / **DEC-0081** (native chain compose)

## Acceptance criteria coverage (AC-1..AC-10 → T-xxx; surjective, 11 tasks / 10 ACs)

| AC | Description (summary) | Task(s) | Architecture anchor |
|----|-----------------------|---------|---------------------|
| AC-1 | Installer ownership — root **`README.md`** excluded from **`[install_paths]`** | T-001 | § Ownership matrix |
| AC-2 | Non-destructive migration **M1–M5** + sentinels **S1–S5** | T-002 | § Migration M1–M5; § Placeholder sentinels |
| AC-3 | Execute bootstrap scaffold when missing/placeholder | T-003, T-004 | § Execute step 23 (**23a**) |
| AC-4 | Mandatory execute/release README delta per shipped story | T-004, T-005 | § Execute step 23 (**23b**); § Release step **3g** |
| AC-5 | User + developer audience structure; framework catalog in **`its_magic/`** only | T-003, T-007 | § Project README scaffold; § Ownership matrix |
| AC-6 | Split validators — **US-0091** → framework; project → root | T-007, T-008 | § Validators |
| AC-7 | Release **3g** + scratchpad **`PROJECT_README_ENFORCE`** | T-005, T-006 | § Release step **3g**; § Scratchpad keys |
| AC-8 | **US-0071** hygiene compose on project blurbs | T-004 | § Execute step 23 (**23c**) |
| AC-9 | Eight **`test_us0097_*`** + **`PROJECT_README_PAIRS`** parity + harness | T-009, T-010 | § Contract tests + parity |
| AC-10 | Architecture + runbook operator recipes | T-011 | § Runbook operator recipes; **DEC-0083** |

**Multi-AC tasks** (justified by architecture `# US-0097` § Atomic task seeds): **T-003** (AC-3+AC-5), **T-004** (AC-3+AC-4+AC-8), **T-005** (AC-4+AC-7), **T-007** (AC-5+AC-6), **T-009/T-010** (AC-9 split contract vs parity). Every AC has ≥1 task; no `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 11
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (11 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-10 coverage; **strict 1:1 task-to-seed** (11 architecture seeds → T-001..T-011); **not** strict AC bijection (multi-AC tasks above)

## Governance

- **DEC-0083** (binding) — each task cites governing architecture §(s) and DEC §(s).
- **R-0084** (research anchor).
- **DEC-0045** amended — root **`README.md`** no longer framework install payload.
- **US-0045** canonical status authority (US-0097 stays OPEN through this sprint).

## Edit surfaces and parity plan

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `docs/engineering/context/installer-owned-paths.manifest` | `template/docs/engineering/context/installer-owned-paths.manifest` | T-001 | Positive |
| 2 | `scripts/project_readme_coverage_lib.py` (new) | `template/scripts/project_readme_coverage_lib.py` | T-002, T-003, T-008 | Positive |
| 3 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-002, T-011 | Positive |
| 4 | `.cursor/commands/execute.md` | `template/.cursor/commands/execute.md` | T-004 | Positive |
| 5 | `.cursor/commands/release.md` | `template/.cursor/commands/release.md` | T-005 | Positive |
| 6 | `.cursor/scratchpad.local.example.md` | `template/.cursor/scratchpad.local.example.md` | T-006 | Positive |
| 7 | `scripts/validate_readme_feature_coverage.py` | `template/scripts/validate_readme_feature_coverage.py` | T-007 | Positive |
| 8 | `scripts/validate_project_readme_coverage.py` (new) | `template/scripts/validate_project_readme_coverage.py` | T-008 | Positive |
| 9 | `tests/auto_command_contract_test.py` | (active-only) | T-009 | N/A |
| 10 | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` | T-010 | Positive |
| 11 | `tests/run-tests.ps1` / `tests/run-tests.sh` | (active-only) | T-010 | Harness **§26V** |

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** remove **`its_magic/README.md`** from framework install payload.
- Do **not** break release step **3f** (framework **US-0091** gate) — **`test_us0097_us0091_regression_guard`** mandatory.
- Do **not** conflate project and framework validators into one script.
- Do **not** overwrite operator-authored root README when **S5** detected.
- Do **not** set **`FRAMEWORK_KIT_REPO=1`** as consumer default.

## Post-edit gate sequence (architecture § Contract tests)

1. `pytest -k us0097 tests/auto_command_contract_test.py` → all eight subtests green
2. `python scripts/validate_project_readme_coverage.py --self-test` → **`[PROJECT_README_COVERAGE_SELF_TEST_OK]`**
3. `python scripts/check_intake_template_parity.py --scope=project-readme` → PASS (**`PROJECT_README_PAIRS`**)
4. Framework regression: release **3f** + **`validate_readme_feature_coverage.py`** paths unchanged except reframe to **`its_magic/`**

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Tranche A — installer + migration (T-001, T-002)

- Root **`README.md`** removed from **`[install_paths]`**; **`its_magic/README.md`** retained
- **M1–M5** idempotent migration; **S1–S5** sentinel table; hybrid fail-closed reason codes

### Tranche B — bootstrap (T-003)

- Project scaffold from **`docs/product/vision.md`** H1/purpose
- Catalog marker **`<!-- project-readme-feature-catalog -->`**

### Tranche C — phase wiring (T-004, T-005, T-006)

- Execute step **23** (**23a**/**23b**/**23c**) after step **22**
- Release step **3g** after **3f**, before step **4**
- Scratchpad **`PROJECT_README_ENFORCE`**, **`FRAMEWORK_KIT_REPO`**

### Tranche D — validators + tests (T-007, T-008, T-009, T-010, T-011)

- **US-0091** path reframe; new project validator + **`--report`** schema v1
- Eight **`test_us0097_*`** markers; **`PROJECT_README_PAIRS`**; harness **§26V**
- Runbook operator recipes (bootstrap, migration, gate troubleshooting)

## Risks and mitigations (architecture § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Migration deletes operator prose | T-002 **S5** preserve + **M5** fail-closed |
| R2 | **US-0091** regression | T-007 path table + T-009 **`test_us0097_us0091_regression_guard`** |
| R3 | Kit vs consumer repo | T-006/T-008 **`FRAMEWORK_KIT_REPO`** detection order + validator skip |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 10 acceptance criteria covered surjectively by T-001..T-011.
- `sprints/S0087/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_surjective=true`, `task_count=11`, `within_limit=true`.
- `pytest -k us0097` green; parity **`--scope=project-readme`** PASS; project validator self-test green.
- `docs/product/backlog.md` **`## US-0097`** retains **OPEN** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0087`** / **US-0097** — verify AC-1..AC-10 ↔ T-001..T-011 surjective coverage, task-seed bijection (11 seeds → 11 tasks), task-count bound, governance alignment. Target: `sprints/S0087/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
