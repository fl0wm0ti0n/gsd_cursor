# Sprint S0078 Tasks — BUG-0009

**sprint_id**: S0078  
**bug_refs**: BUG-0009  
**dec_ref**: DEC-0075 (binding; composes on US-0017 negative-parity exceptions)  
**task_count**: 10  
**within_limit**: true (10 ≤ `SPRINT_MAX_TASKS=12`); `SPRINT_AUTO_SPLIT` not triggered  
**coverage**: AC-1..AC-8 surjective via T-001..T-010 (8 ACs, 10 tasks; multi-AC rows per architecture seeds)

> No implementation or test code is authored in this phase — dev owns that in `/execute`.

---

## T-001 — Template `ci.yml` downstream-safe + checks hardening — AC-1, AC-4

- **ac_ref**: AC-1, AC-4
- **dec_ref**: DEC-0075 §1 (in-place job subtraction), §5 (checks green-by-default)
- **description**: Edit `template/.github/workflows/ci.yml` only — remove `npm-test`, `brew-test`, `choco-test` job blocks; retain `checks` + `auto-fix`. Harden `checks` job: when all runbook command keys empty/skipped → **PASS** with summary **`no tests configured yet`**; `Fail if tests or lint failed` fires only when a configured step returns `failure`. Keep filename `ci.yml`; do not touch manifest entries.
- **files_affected**:
  - `template/.github/workflows/ci.yml`
- **parity_touchpoints**: **US-0017 negative parity** — intentional ≠ active `ci.yml` (DEC-0075 §2).
- **acceptance_check**:
  - Template job inventory ⊆ `{checks, auto-fix}` only.
  - No forbidden substrings (`npm-test`, `brew-test`, `choco-test`, `npm pack`, `installer.sh`, `packaging/chocolatey`, etc.).
  - `checks` job emits `no tests configured yet` when commands empty/skipped.
  - SHA-256 differs from active `.github/workflows/ci.yml`.
- **status**: done

---

## T-002 — Active `ci.yml` checks hardening; preserve five jobs — AC-2, AC-4

- **ac_ref**: AC-2, AC-4
- **dec_ref**: DEC-0075 §1 (active kit retains packaging), §5 (checks semantics)
- **description**: Edit `.github/workflows/ci.yml` (active kit only) — apply same `checks` green-by-default semantics as T-001; **must retain** all five job ids: `checks`, `auto-fix`, `npm-test`, `brew-test`, `choco-test`. Do not remove or rename packaging jobs.
- **files_affected**:
  - `.github/workflows/ci.yml`
- **parity_touchpoints**: Active-only; must **not** byte-match template after T-001.
- **acceptance_check**:
  - All five job ids present in active `ci.yml`.
  - Packaging job step bodies unchanged (self-distribution paths intact).
  - `checks` hardened per DEC-0075 §5 (same semantics as template).
  - Post-bootstrap configured-command failures still fail `checks`.
- **status**: done

---

## T-003 — Template runbook empty `TEST_COMMAND:` header — AC-5

- **ac_ref**: AC-5
- **dec_ref**: DEC-0075 §6 (template bootstrap; US-0063 preserved)
- **description**: Set `TEST_COMMAND:` header **empty on ship** in `template/docs/engineering/runbook.md` (no value after colon). Active `docs/engineering/runbook.md` keeps powershell harness line unchanged. Documented **US-0017** exception for this header line only.
- **files_affected**:
  - `template/docs/engineering/runbook.md`
- **parity_touchpoints**: Negative parity on `TEST_COMMAND:` line only; other runbook edits still mirror per T-009.
- **acceptance_check**:
  - Template runbook `TEST_COMMAND:` line has no command value.
  - Active runbook harness line unchanged.
  - `python scripts/validate_doc_profile.py --repo .` exits 0 post-change (R5).
  - US-0063 bootstrap behavior unchanged (fills when missing on install).
- **status**: done

---

## T-004 — Drift guard lib + CLI (`downstream_ci_guard_lib.py`, `check_downstream_ci_guard.py`) — AC-3, AC-7

- **ac_ref**: AC-3, AC-7
- **dec_ref**: DEC-0075 §3 (script + lib split), §4 (forbidden patterns + reason codes)
- **description**: Implement stdlib-only `scripts/downstream_ci_guard_lib.py` (YAML job-key regex extraction, forbidden-pattern scan, active positive inventory, reason-code emitter) and `scripts/check_downstream_ci_guard.py` CLI (`--repo`, `--self-test` → `[DOWNSTREAM_CI_GUARD_SELF_TEST_OK]`, `--report` JSON). Ship byte-identical `template/scripts/` mirrors.
- **files_affected**:
  - `scripts/downstream_ci_guard_lib.py` (new)
  - `scripts/check_downstream_ci_guard.py` (new)
  - `template/scripts/downstream_ci_guard_lib.py` (byte-identical)
  - `template/scripts/check_downstream_ci_guard.py` (byte-identical)
- **parity_touchpoints**: DEC-0075 §8 rows 1–2 (positive parity).
- **acceptance_check**:
  - `--self-test` exits 0 with `[DOWNSTREAM_CI_GUARD_SELF_TEST_OK]`.
  - Template scan emits `DOWNSTREAM_CI_FORBIDDEN_PATTERN` / `DOWNSTREAM_CI_JOB_LEAK` on violation.
  - Active scan emits `KIT_CI_PACKAGING_JOBS_MISSING` when packaging job absent.
  - Active / template script SHA-256 equal per pair.
  - Stdlib-only imports (no PyYAML).
- **status**: done

---

## T-005 — Contract tests `test_bug0009_*` — AC-3, AC-7

- **ac_ref**: AC-3, AC-7
- **dec_ref**: DEC-0075 §3 (contract tests), §2 (negative SHA-256 parity)
- **description**: Extend `tests/auto_command_contract_test.py` **in place** with `test_bug0009_*` subtests: template forbidden-pattern markers; negative SHA-256 assert (template `ci.yml` ≠ active); active five-job inventory assert; guard `--report` inventory fields. Additions only — do not modify unrelated subtests.
- **files_affected**:
  - `tests/auto_command_contract_test.py`
- **parity_touchpoints**: Active-only (tests do not mirror).
- **acceptance_check**:
  - All `test_bug0009_*` subtests pass on clean tree post T-001..T-004.
  - Negative parity test fails if template/active `ci.yml` accidentally byte-match.
  - Active inventory test fails if any packaging job removed from active CI.
  - Forbidden-pattern test fails if `npm-test` reintroduced in template.
- **status**: done

---

## T-006 — Harness section **§28B** — AC-3

- **ac_ref**: AC-3
- **dec_ref**: DEC-0075 §3 (harness §28B)
- **description**: Add harness section **§28B** to `tests/run-tests.ps1` + `tests/run-tests.sh` wiring `check_downstream_ci_guard.py --self-test` and contract-test subset for `test_bug0009_*`. Section id locked as **§28B** per DEC-0075.
- **files_affected**:
  - `tests/run-tests.ps1` (§28B)
  - `tests/run-tests.sh` (§28B)
- **parity_touchpoints**: Active-only (harness).
- **acceptance_check**:
  - §28B present in both PS1 and SH runners with matching semantics.
  - Section green when guard self-test + contract subtests pass.
  - Section fails closed when template CI leak reintroduced.
- **status**: done

---

## T-007 — Install-completeness job-inventory smoke — AC-6

- **ac_ref**: AC-6
- **dec_ref**: DEC-0075 §7 (install/upgrade smoke; BUG-0003 class)
- **description**: Extend `tests/installer_completeness_bug0003_test.py` with `test_downstream_ci_yml_job_inventory_missing_mode` (`--mode missing --create` → installed `.github/workflows/ci.yml` jobs ⊆ `{checks, auto-fix}`) and `test_downstream_ci_yml_job_inventory_upgrade_mode` (same after `--mode upgrade`). Assert forbidden packaging job ids absent.
- **files_affected**:
  - `tests/installer_completeness_bug0003_test.py`
- **parity_touchpoints**: Active-only (tests).
- **acceptance_check**:
  - Both tests pass across `installer.sh`, `installer.ps1`, `installer.py` entrypoints (per existing fixture pattern).
  - Installed `ci.yml` contains only `checks` + `auto-fix` job keys.
  - Tests fail if packaging jobs leak into installed workflow.
- **status**: done

---

## T-008 — Installer manifest + parity `--scope=downstream-ci-guard` — AC-6, AC-7

- **ac_ref**: AC-6, AC-7
- **dec_ref**: DEC-0075 §7 (manifest entries), §8 rows 4–5 (parity scope)
- **description**: Add `scripts/check_downstream_ci_guard.py` and `scripts/downstream_ci_guard_lib.py` under `[install_include_paths]` in `docs/engineering/context/installer-owned-paths.manifest` (+ `template/` mirror). Extend `scripts/check_intake_template_parity.py` with `--scope=downstream-ci-guard` asserting guard script byte-identity only — **NOT** `ci.yml` byte parity.
- **files_affected**:
  - `docs/engineering/context/installer-owned-paths.manifest`
  - `template/docs/engineering/context/installer-owned-paths.manifest`
  - `scripts/check_intake_template_parity.py`
  - `template/scripts/check_intake_template_parity.py`
- **parity_touchpoints**: DEC-0075 §8 rows 4–5 (positive parity).
- **acceptance_check**:
  - Manifest lists both guard scripts under `install_include_paths`.
  - `python scripts/check_intake_template_parity.py --scope=downstream-ci-guard` exits 0.
  - Mutating active vs template guard script pair causes non-zero exit.
  - No `--scope=ci-downstream` mode added.
- **status**: done

---

## T-009 — Operator upgrade remediation docs — AC-8

- **ac_ref**: AC-8
- **dec_ref**: DEC-0075 §9 (verbatim remediation blurb)
- **description**: Ship verbatim upgrade remediation blurb from DEC-0075 §9 in README troubleshooting + `docs/engineering/runbook.md` subsection (+ `template/` runbook mirror for locked strings). Scope reminder: fix applies to new installs/upgrades; stale repos heal on **US-0018** upgrade/clean.
- **files_affected**:
  - `README.md` (troubleshooting subsection)
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md` (remediation subsection; `TEST_COMMAND:` exception per T-003)
- **parity_touchpoints**: Runbook remediation subsection positive parity (except `TEST_COMMAND:` header).
- **acceptance_check**:
  - Verbatim blurb text matches DEC-0075 §9 (mentions `its-magic --target <repo> --mode upgrade`, expected job inventory `checks` + `auto-fix` only).
  - README + runbook surfaces discoverable without internal planning tokens (**US-0071**).
  - Active/template runbook remediation strings byte-identical.
- **status**: done

---

## T-010 — Architecture + DEC linkage assert (read-only) — AC-7

- **ac_ref**: AC-7
- **dec_ref**: DEC-0075 §2, §8; architecture `# BUG-0009` § Related
- **description**: Assert-only subtest verifying `docs/engineering/architecture.md` `# BUG-0009` references **DEC-0075**, **US-0008**, **US-0017**, **US-0018**, **US-0063**, **BUG-0003**, **R-0075**, and documents US-0017 negative-parity exceptions. No rewrite of architecture or DEC files.
- **files_affected**:
  - `tests/auto_command_contract_test.py` (assert-only subtest under `test_bug0009_*` or sibling)
- **parity_touchpoints**: Active-only (read-only assert).
- **acceptance_check**:
  - Subtest passes when required cross-refs present in `# BUG-0009`.
  - Subtest fails if negative-parity table or forbidden `--scope=ci-downstream` policy removed from architecture.
  - `decisions/DEC-0075.md` exists and status Accepted (read-only assert).
- **status**: done

---

## Recommended /execute ordering

1. **T-001** — template CI subtraction (unblocks guard scans)
2. **T-002** — active CI checks hardening (preserve packaging jobs)
3. **T-003** — template runbook `TEST_COMMAND` empty header
4. **T-004** — drift guard scripts (+ template mirrors)
5. **T-005** — contract tests (depends T-001..T-004)
6. **T-006** — harness §28B (depends T-004, T-005)
7. **T-007** — install-completeness smoke (depends T-001, T-008 manifest partial)
8. **T-008** — manifest + parity scope (can parallel T-004; finalize before T-007 rerun)
9. **T-009** — operator remediation docs
10. **T-010** — linkage assert (last — after architecture stable)
