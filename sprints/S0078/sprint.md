# Sprint S0078

## Metadata

- **sprint_id**: S0078
- **bug_refs**: BUG-0009
- **goal**: Decouple downstream-safe template CI from kit-internal active CI — in-place job subtraction in `template/.github/workflows/ci.yml`, retain five packaging jobs in active CI, ship drift guard + harness **§28B**, checks green-by-default, empty template `TEST_COMMAND` bootstrap, install smoke, and operator upgrade remediation — per **DEC-0075** (composes on **US-0017** negative-parity exceptions + **US-0008** installer copy).
- **status**: planned
- **created_at**: 2026-06-06T14:00:23Z
- **orchestrator_run_id**: auto-20260606-02
- **fresh_context_marker**: tl-S0078-BUG0009-sprint-plan-20260606T140023Z-fresh

## Scope

- **BUG-0009**: its-magic ships kit-only packaging CI into generated repos
- **Architecture**: `docs/engineering/architecture.md` `# BUG-0009` (active-only)
- **Binding decision**: `decisions/DEC-0075.md` (Accepted 2026-06-06)
- **Research anchor**: `docs/engineering/research.md` `R-0075`

## Non-goals (hard, from DEC-0075 §10)

- No cross-repo reusable GitHub Actions workflow.
- No rename of downstream `ci.yml`.
- No change to `deploy.yml`.
- No strip of packaging jobs from **active** CI.
- No `check_intake_template_parity.py --scope=ci-downstream` byte-parity mode.
- No byte-match of template and active `ci.yml` after fix.
- No new npm/pip runtime dependencies (stdlib-only Python guard).
- No retroactive auto-fix of operator repos outside upgrade/clean copy path.
- **Status authority (US-0045)**: BUG-0009 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0075** (§1–§10); architecture `# BUG-0009`; research **R-0075**
- **Governance stack**: **US-0007** / **US-0009** (kit self-distribution CI), **US-0008** (installer copy), **US-0017** (template drift — negative-parity exceptions), **US-0018** (upgrade/clean re-copy), **US-0063** / **DEC-0056** (runbook bootstrap), **BUG-0003** / **DEC-0066** (install-completeness fixture class), **US-0045** (status authority), **US-0048** / **DEC-0029** (isolation), **US-0056** / **DEC-0038** (strict proof)

## Acceptance criteria coverage (AC-1..AC-8 → T-xxx; surjective, 10 tasks / 8 ACs)

| AC | Description (summary) | Task(s) | DEC-0075 § |
|----|-----------------------|---------|------------|
| AC-1 | Template `ci.yml` downstream-safe (`checks`+`auto-fix` only) | T-001 | §1 |
| AC-2 | Active kit CI retains five packaging jobs | T-002 | §1, §4 |
| AC-3 | Drift guard + contract tests + harness **§28B** | T-004, T-005, T-006 | §3, §4 |
| AC-4 | `checks` green-by-default (`no tests configured yet`) | T-001, T-002 | §5 |
| AC-5 | Empty template `TEST_COMMAND` + **US-0063** preserved | T-003 | §6 |
| AC-6 | Install/upgrade job-inventory smoke | T-007, T-008 | §7 |
| AC-7 | **US-0017** negative parity + guard scripts + linkage assert | T-004, T-005, T-008, T-010 | §2, §3, §8 |
| AC-8 | Operator upgrade remediation docs | T-009 | §9 |

**Multi-AC tasks** (justified by architecture `# BUG-0009` § Atomic task seeds): **T-001** (AC-1+AC-4), **T-002** (AC-2+AC-4), **T-004** (AC-3+AC-7), **T-005** (AC-3+AC-7), **T-007** (AC-6), **T-008** (AC-6+AC-7). Every AC has ≥1 task; no `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 10
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (10 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-8 coverage; **not** strict 1:1 bijection (8 ACs, 10 tasks per architecture seeds)

## Governance

- **DEC-0075** §1–§10 (binding) — each task cites governing §(s).
- **R-0075** (research anchor).
- **US-0017** negative-parity policy for `ci.yml` + template runbook `TEST_COMMAND:` line.
- **US-0045** canonical status authority (BUG-0009 stays OPEN through this sprint).

## Template parity plan (DEC-0075 §8)

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `scripts/check_downstream_ci_guard.py` | `template/scripts/check_downstream_ci_guard.py` | T-004 | Positive (byte-identical) |
| 2 | `scripts/downstream_ci_guard_lib.py` | `template/scripts/downstream_ci_guard_lib.py` | T-004 | Positive (byte-identical) |
| 3 | `docs/engineering/runbook.md` (remediation subsection) | `template/docs/engineering/runbook.md` | T-009 | Positive (except `TEST_COMMAND:` header per §2) |
| 4 | `docs/engineering/context/installer-owned-paths.manifest` | `template/docs/engineering/context/installer-owned-paths.manifest` | T-008 | Positive (guard script entries) |
| 5 | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` | T-008 | Positive (`--scope=downstream-ci-guard`) |

**Active-only** (no `template/` mirror; intentional per DEC-0075 §2):

- `template/.github/workflows/ci.yml` — downstream-safe (≠ active)
- `.github/workflows/ci.yml` — kit-internal (five jobs)
- `template/docs/engineering/runbook.md` — `TEST_COMMAND:` header line exception
- `docs/engineering/architecture.md` `# BUG-0009`
- `tests/auto_command_contract_test.py`, `tests/installer_completeness_bug0003_test.py`, harness **§28B**

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** byte-match template and active `ci.yml` after fix.
- Do **not** add `--scope=ci-downstream` to parity script.
- Do **not** strip packaging jobs from **active** CI.

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Drift guard (T-004, T-005, T-006)

- `python scripts/check_downstream_ci_guard.py --self-test` → `[DOWNSTREAM_CI_GUARD_SELF_TEST_OK]`
- Template forbidden-pattern scan + active five-job positive inventory
- Reason codes: `DOWNSTREAM_CI_FORBIDDEN_PATTERN`, `DOWNSTREAM_CI_JOB_LEAK`, `KIT_CI_PACKAGING_JOBS_MISSING`

### Contract tests (T-005)

- Extend `tests/auto_command_contract_test.py` in place with `test_bug0009_*` prefix
- Negative SHA-256 parity assert (template `ci.yml` ≠ active `ci.yml`)
- Active five-job inventory assert

### Harness (T-006)

- New section **§28B** in `tests/run-tests.ps1` + `tests/run-tests.sh`

### Install smoke (T-007)

- `test_downstream_ci_yml_job_inventory_missing_mode` + `test_downstream_ci_yml_job_inventory_upgrade_mode`
- Installed `ci.yml` job keys ⊆ `{checks, auto-fix}`; forbidden jobs absent

### Parity (T-008)

- `python scripts/check_intake_template_parity.py --scope=downstream-ci-guard` exits 0
- Guard script SHA-256 equality active vs `template/`

### Runbook validator (T-003)

- Re-run `python scripts/validate_doc_profile.py --repo .` after template runbook header change (R5 mitigation)

## Risks and mitigations (DEC-0075 §Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Strip packaging jobs from active CI | T-002 preserves five jobs; T-005 active positive inventory |
| R2 | Stale broken repos until upgrade | T-009 verbatim remediation blurb; accepted scope |
| R3 | Installer copies wrong workflow | T-007 install-completeness job-inventory tests |
| R4 | False green after bootstrap | T-001/T-002 fail-step only on configured command failure |
| R5 | Runbook validator side-effects | T-003 re-run `validate_doc_profile.py` in QA |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 8 acceptance criteria covered by T-001..T-010 (surjective; no gaps).
- `sprints/S0078/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_gap=false`, `task_count=10`, `within_limit=true`.
- `check_downstream_ci_guard.py --self-test` green; harness **§28B** green.
- Template `ci.yml` jobs ⊆ `{checks, auto-fix}`; active retains all five jobs.
- Positive-parity byte equality across DEC-0075 §8 inventory rows 1–5.
- `docs/product/backlog.md` **`### BUG-0009`** retains **`OPEN`** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0078`** / **BUG-0009** — verify AC-1..AC-8 surjective coverage, task-count bound, governance alignment. Target: `sprints/S0078/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
