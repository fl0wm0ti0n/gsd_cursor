# QA Findings — S0078 / BUG-0009 (cycle 1)

## Metadata

- **sprint_id**: S0078
- **bug_id**: BUG-0009
- **dec_id**: DEC-0075 (composes on US-0017 negative-parity exceptions)
- **cycle**: 1
- **role**: qa
- **timestamp**: 2026-06-06T14:10:30Z
- **orchestrator_run_id**: auto-20260606-02
- **fresh_context_marker**: qa-S0078-BUG0009-qa-20260606T141030Z-fresh
- **inputs_reviewed**: `sprints/S0078/tasks.md`, `sprints/S0078/summary.md`, `sprints/S0078/plan-verify.json`, `handoffs/dev_to_qa.md`, `decisions/DEC-0075.md`, `docs/product/backlog.md` `### BUG-0009`, `docs/engineering/architecture.md` `# BUG-0009`, `tests/run-tests.ps1` §28B.

## Overall verdict

**PASS** — All 8 ACs (AC-1..AC-8) satisfied; harness **§28B** green; drift guard + contract + install smoke verified; US-0017 negative parity confirmed (template `ci.yml` ≠ active SHA-256; template runbook `TEST_COMMAND:` empty); no `--scope=ci-downstream` on parity script. Bug **BUG-0009** remains **OPEN** per **US-0045** (closure at `/release`).

- `ac_coverage`: AC-1..AC-8 = 8/8 PASS
- `regressions_found`: **none attributable to BUG-0009** (harness Fail=14 vs S0077 QA baseline Fail=9; +5 net from pre-existing US-0091/triad/state drift disjoint from DEC-0075 deliverables)
- `parity_verified`: true (`check_intake_template_parity.py --scope=downstream-ci-guard` → `[INTAKE_TEMPLATE_PARITY_OK]`)
- `bug_validator`: `[BUG_VALIDATION_OK]`
- `decision_gate_posture`: none required

## Test plan

| Step | Command / check | Expected | Result |
|------|-----------------|----------|--------|
| 1 | `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1` | §28B green; BUG-0009 harness assertions pass | **PASS** — Pass=802 / Fail=14 (`tests/report.md` Timestamp=2026-06-06T14:08:25Z); §28B lines 816–820 all `[PASS]` |
| 2 | `python scripts/check_downstream_ci_guard.py --self-test` | `[DOWNSTREAM_CI_GUARD_SELF_TEST_OK]` exit 0 | **PASS** |
| 3 | `python scripts/check_downstream_ci_guard.py --repo . --report` | `ok=true`, template=`[checks,auto-fix]`, active=5 jobs, `forbidden_hits=[]` | **PASS** |
| 4 | `python scripts/check_intake_template_parity.py --scope=downstream-ci-guard` | `[INTAKE_TEMPLATE_PARITY_OK]` | **PASS** |
| 5 | `python -m pytest tests/auto_command_contract_test.py -q -k bug0009` | 6 passed | **PASS** (6 passed, 15 subtests) |
| 6 | `python -m pytest tests/installer_completeness_bug0003_test.py -q -k downstream_ci` | 2 passed | **PASS** |
| 7 | `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` | `[BUG_VALIDATION_OK]` | **PASS** |
| 8 | Template vs active `ci.yml` SHA-256 | Must differ (US-0017 negative parity) | **PASS** — active `740e93fa…`, template `b7e6cc43…`, `equal=False` |
| 9 | Template runbook `TEST_COMMAND:` header | Empty on ship (AC-5 / DEC-0075 §6) | **PASS** — `template/docs/engineering/runbook.md` line 5: `TEST_COMMAND:` (no value) |
| 10 | No `--scope=ci-downstream` on parity script | Forbidden per DEC-0075 §2 | **PASS** — only `downstream-ci-guard` scope wired; contract subtest asserts rejection |
| 11 | Active CI packaging jobs preserved | `npm-test`, `brew-test`, `choco-test` present | **PASS** — `.github/workflows/ci.yml` retains all three job ids |
| 12 | Template CI downstream-safe | No packaging jobs | **PASS** — `template/.github/workflows/ci.yml` has only `checks` + `auto-fix` job keys |

## Per-AC verdicts (AC-1..AC-8)

### AC-1 — Template `ci.yml` downstream-safe — `verdict=PASS`

- **DEC-0075 §**: §1
- **evidence_ref**: `template/.github/workflows/ci.yml` job keys ⊆ `{checks, auto-fix}`; guard `--report` `template_job_keys=["checks","auto-fix"]`, `forbidden_hits=[]`.

### AC-2 — Active kit CI retains five packaging jobs — `verdict=PASS`

- **DEC-0075 §**: §1, §4
- **evidence_ref**: `.github/workflows/ci.yml` contains `checks`, `auto-fix`, `npm-test`, `brew-test`, `choco-test`; guard `--report` `active_job_keys` lists all five; `test_bug0009_active_five_job_inventory` PASS.

### AC-3 — Drift guard + contract tests + harness §28B — `verdict=PASS`

- **DEC-0075 §**: §3, §4
- **evidence_ref**: `check_downstream_ci_guard.py` + `downstream_ci_guard_lib.py` (+ template mirrors); `--self-test` OK; harness §28B (5 assertions) all PASS; `test_bug0009_*` (6 subtests) PASS.

### AC-4 — `checks` green-by-default — `verdict=PASS`

- **DEC-0075 §**: §5
- **evidence_ref**: Template and active `ci.yml` use `no tests configured yet` summary path; fail-step only on configured command failure (dev handoff + contract subtests).

### AC-5 — Empty template `TEST_COMMAND` + US-0063 preserved — `verdict=PASS`

- **DEC-0075 §**: §6
- **evidence_ref**: `template/docs/engineering/runbook.md` ships empty `TEST_COMMAND:` header; active runbook retains harness `TEST_COMMAND`; install smoke shows `[RUNBOOK_BOOTSTRAP]` fills defaults on install.

### AC-6 — Install/upgrade job-inventory smoke — `verdict=PASS`

- **DEC-0075 §**: §7
- **evidence_ref**: `test_downstream_ci_yml_job_inventory_missing_mode` + `test_downstream_ci_yml_job_inventory_upgrade_mode` PASS (2/2); installer manifest rows for guard scripts per T-008.

### AC-7 — US-0017 negative parity + guard scripts + linkage — `verdict=PASS`

- **DEC-0075 §**: §2, §3, §8
- **evidence_ref**: Template ≠ active `ci.yml` SHA-256; `--scope=downstream-ci-guard` parity OK; no `--scope=ci-downstream`; `test_bug0009_architecture_linkage` PASS; guard scripts byte-identical active/template.

### AC-8 — Operator upgrade remediation docs — `verdict=PASS`

- **DEC-0075 §**: §9
- **evidence_ref**: README upgrade blurb references refreshing `.github/workflows/ci.yml` from corrected template (line ~974); active + template runbook remediation subsections present per dev handoff T-009.

## Canonical check-in baseline comparison

| Checkpoint | Pass | Fail | Notes |
|------------|------|------|-------|
| US-0091 QA (S0077) | 802 | 9 | Prior story QA baseline |
| **BUG-0009 QA (S0078)** | **802** | **14** | **+0 pass / +5 fail** (disjoint drift) |

**Pre-existing Fail=9 (subset still failing, disjoint from BUG-0009)**:

1. Homebrew stable formula URL uses npm version tag
2. Homebrew stable formula version matches npm version
3. scratchpad includes TOKEN_PROFILE (active)
4. auto includes strict-proof boundary step 11b (active)
5. auto includes strict-proof boundary step 11b (template)
6. scratchpad pair parity check passes on repo
7. slim auto command contract markers pass

**New Fail=5 vs S0077 baseline (not BUG-0009 scope)**:

1. state documents active context surface policy (active) — state.md growth collateral
2. triad check passes on repo — hot-surface cap collateral from sprint checkpoints
3. triad check idempotent rerun passes — same
4. check_intake_template_parity --scope=caveman-compress passes — US-0090 collateral
5. validate_readme_feature_coverage repo --report / idempotent / readme-feature-coverage parity — US-0091 collateral (`README_FEATURE_COVERAGE_INPUT_INVALID: US-0091`)

**BUG-0009 harness additions (all PASS)**: `check_downstream_ci_guard.py` exists; `downstream_ci_guard_lib.py` exists; self-test; `--scope=downstream-ci-guard` parity; `BUG-0009 contract subtests pass`.

## Generated baseline test evidence (US-0066 / DEC-0048)

- `generated_test_stack_profile`: python (stdlib)
- `generated_test_command`: `python -m pytest tests/auto_command_contract_test.py -q -k bug0009`
- `generated_test_result`: pass
- `generated_test_output_ref`: 6 passed, 15 subtests passed
- `generated_test_paths_ref`: `tests/auto_command_contract_test.py` (`test_bug0009_*`)
- `generated_test_reason_code`: (none — pass)

## Runtime QA evidence (US-0065)

Not applicable — CI template / guard / installer story; no application runtime startup required. `runtime_final_verdict=skipped`; `runtime_reason_code=N/A_CI_GUARD_STORY`.

## Blocking findings

None.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0078-BUG0009-qa-20260606T141030Z-fresh`
- `timestamp=2026-06-06T14:10:30Z`
- `evidence_ref=sprints/S0078/qa-findings.md,handoffs/qa_to_verify_work.md,handoffs/resume_brief.md,docs/engineering/state.md,tests/report.md`

## Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260606-02`
- `runtime_proof_id=rp-auto-20260606-02-qa-qa-20260606T141030Z-S0078-BUG0009`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-06-06T14:10:30Z`
- `proof_ttl_seconds=3600`
- `proof_hash=1708a5437f10b539c018ab4d18fcef357b700094117eaf0f16f88baab5e11078`

Canonical payload: `{"orchestrator_run_id":"auto-20260606-02","phase_id":"qa","proof_issued_at":"2026-06-06T14:10:30Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260606-02-qa-qa-20260606T141030Z-S0078-BUG0009"}`.

## Next phase

**`/verify-work`** (fresh **qa** subagent) — BUG-0009 remains OPEN until verify-work + `/release` closure per US-0045.
