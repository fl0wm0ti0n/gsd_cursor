# Sprint S0078 UAT — BUG-0009

- **Sprint**: `S0078`
- **Work item**: **BUG-0009** — downstream-safe template CI vs kit-internal active CI
- **DEC**: **DEC-0075**
- **Orchestrator run**: **auto-20260606-02**
- **Machine-readable**: `sprints/S0078/uat.json`
- **Status**: **populated** (verify-work complete)
- **Canonical backlog**: **`docs/product/backlog.md`** — **BUG-0009** **OPEN** (**US-0045**; release owns closure)

## Metadata

- **author**: qa
- **qa_verdict_reference**: `sprints/S0078/qa-findings.md` (PASS)
- **verify_work_executed_at**: 2026-06-06T16:10:30Z
- **verify_work_role**: qa
- **verify_work_fresh_context_marker**: `qa-S0078-BUG0009-verify-work-20260606T161030Z-fresh`
- **verify_work_verdict**: **PASS** (8/8 UAT steps PASS; 0 FAIL; 0 SKIP)

## Verdict summary

| Bucket | Count |
|--------|-------|
| PASS | 8 |
| FAIL | 0 |
| SKIP | 0 |
| Total | 8 |

Verify-work verdict: **PASS**. Closure preflight: **PASS** (9/9 gates). Bug **BUG-0009** remains **OPEN** per **US-0045**.

## Preconditions

- Python 3.12+ available.
- DEC-0075 execute deliverables merged (guard scripts, template CI subtraction, harness §28B).
- Active + template mirrors for `check_downstream_ci_guard.py` / `downstream_ci_guard_lib.py`.

## UAT steps

### UAT-1 — Template downstream-safe (AC-1) — `verdict=PASS`

- **DEC-0075 §**: §1
- **Command**: `python scripts/check_downstream_ci_guard.py --repo . --report`
- **Expected**: `ok=true`; `template_job_keys=[checks,auto-fix]`; `forbidden_hits=[]`.
- **Evidence**: verify-work independent re-run → `ok=true`, template keys only `checks`+`auto-fix`, zero forbidden hits.

### UAT-2 — Active five packaging jobs (AC-2) — `verdict=PASS`

- **DEC-0075 §**: §1, §4
- **Commands**: guard `--report` + `test_bug0009_active_five_job_inventory`
- **Expected**: active lists all five job ids; packaging bodies unchanged.
- **Evidence**: `active_job_keys=[checks,auto-fix,npm-test,brew-test,choco-test]`; positive inventory subtest PASS.

### UAT-3 — Drift guard + contract + §28B (AC-3) — `verdict=PASS`

- **DEC-0075 §**: §3, §4
- **Commands**: `--self-test` + `pytest -k bug0009`
- **Expected**: `[DOWNSTREAM_CI_GUARD_SELF_TEST_OK]`; 6 contract subtests PASS; harness §28B green.
- **Evidence**: self-test OK; 6 passed / 15 subtests; §28B 5/5 PASS per qa-findings + prior harness run.

### UAT-4 — Green-by-default checks (AC-4) — `verdict=PASS`

- **DEC-0075 §**: §5
- **Command**: `pytest -k test_bug0009_checks_green_by_default`
- **Expected**: `no tests configured yet` summary path; fail only on configured command failure.
- **Evidence**: contract subtest PASS; template + active ci.yml semantics aligned per DEC-0075 §5.

### UAT-5 — Empty template TEST_COMMAND (AC-5) — `verdict=PASS`

- **DEC-0075 §**: §6
- **Check**: `template/docs/engineering/runbook.md` `TEST_COMMAND:` header
- **Expected**: empty header on ship; US-0063 bootstrap fills on install.
- **Evidence**: line 5 `TEST_COMMAND:` with no value; active runbook retains harness command.

### UAT-6 — Install/upgrade smoke (AC-6) — `verdict=PASS`

- **DEC-0075 §**: §7
- **Command**: `pytest -k downstream_ci` (installer completeness fixture)
- **Expected**: missing + upgrade job-inventory tests PASS (2/2).
- **Evidence**: verify-work re-run → 2 passed.

### UAT-7 — US-0017 negative parity + linkage (AC-7) — `verdict=PASS`

- **DEC-0075 §**: §2, §3, §8
- **Commands**: `--scope=downstream-ci-guard` parity + architecture linkage subtest
- **Expected**: scoped parity OK; template ≠ active `ci.yml` SHA-256; no `--scope=ci-downstream`.
- **Evidence**: `[INTAKE_TEMPLATE_PARITY_OK]`; template `b7e6cc43…` ≠ active `740e93fa…`; `test_bug0009_architecture_linkage` PASS.

### UAT-8 — Upgrade remediation docs (AC-8) — `verdict=PASS`

- **DEC-0075 §**: §9
- **Check**: README + runbook remediation blurbs (verbatim DEC-0075 §9)
- **Expected**: operator guidance to refresh `.github/workflows/ci.yml` on upgrade.
- **Evidence**: README ~line 974; active + template runbook subsections per T-009.

## Closure preflight (9 gates — all PASS)

| Gate | Verdict | Evidence |
|------|---------|----------|
| `tasks_done` | PASS (10/10) | T-001..T-010 done per `sprints/S0078/tasks.md` |
| `ac_qa_pass` | PASS (8/8) | `sprints/S0078/qa-findings.md` §Per-AC verdicts |
| `ac_uat_pass` | PASS (8/8) | this UAT matrix |
| `plan_verify_status` | PASS | `sprints/S0078/plan-verify.json` status=PASS |
| `bug_validator` | `[BUG_VALIDATION_OK]` | verify-work independent re-run exit 0 |
| `parity` | `[INTAKE_TEMPLATE_PARITY_OK]` | `--scope=downstream-ci-guard` |
| `negative_parity` | PASS | template ≠ active `ci.yml` SHA-256; empty template `TEST_COMMAND:`; no `--scope=ci-downstream` |
| `test_baselines_no_regression` | PASS | PS1 harness Pass=802/Fail=14 vs S0077 QA 802/9 (+5 fail disjoint from BUG-0009) |
| `dec_invariants` | PASS | DEC-0075 §10 non-goals preserved; active five jobs intact; template downstream-safe |

## Results summary

**8 / 8 PASS** — ready for **`/release`**. Bug **BUG-0009** stays **OPEN** until release closure per **US-0045**.
