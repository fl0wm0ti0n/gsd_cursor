# Sprint S0089 Tasks — US-0099

**sprint_id**: S0089  
**story_refs**: US-0099  
**dec_ref**: DEC-0084 (binding, amended § bootstrap posture; composes US-0098, US-0018, US-0085; research R-0086)  
**task_count**: 9  
**within_limit**: true (9 ≤ `SPRINT_MAX_TASKS=12`; `SPRINT_AUTO_SPLIT` not triggered)  
**coverage**: AC-1..AC-8 surjective via T-001..T-009 (8 ACs, 9 tasks; architecture seeds 1:1; AC-8 pre-satisfied at architecture; multi-AC tasks T-001, T-002, T-005, T-006, T-007)

> No implementation or test code is authored in this phase — dev owns delivery in `/execute`.

---

## T-001 — **`bootstrap_dev_environment_profile`**, **`resolve_profile_path`**, four **`DEV_ENV_BOOTSTRAP_*`** constants, **`--bootstrap`** CLI + log tokens — AC-1, AC-3, AC-5

- **ac_ref**: AC-1, AC-3, AC-5
- **dec_ref**: DEC-0084 § bootstrap posture; architecture `# US-0099` § Stdlib helper + CLI; § Path resolution
- **description**: Extend **`scripts/dev_environment_lib.py`** (+ template mirror) with **`bootstrap_dev_environment_profile(target_root, source_root=None, scratchpad=None)`** returning **`(reason_code, log_channel)`**; **`resolve_profile_path(target_root, scratchpad)`** returning **`(Path | None, error_code | None)`**; four **`DEV_ENV_BOOTSTRAP_*`** constants; CLI flags **`--bootstrap`**, **`--target`**, **`--source-root`**; user-visible log tokens per architecture table (**`[DEV_ENV_BOOTSTRAP_OK]`**, **`[DEV_ENV_BOOTSTRAP_ERROR]`**, **`[DEV_ENV_BOOTSTRAP_SKIP]`**). Source = **`{source_root}/.cursor/dev-environment.json.example`** only. Exit **0** for **`COPIED`** / **`SKIPPED_EXISTS`**; **1** for **`PATH_INVALID`** / **`SOURCE_MISSING`**.
- **files_affected**:
  - `scripts/dev_environment_lib.py`
  - `template/scripts/dev_environment_lib.py`
- **parity_touchpoints**: architecture § Atomic task seeds row 1; **`DEV_ENVIRONMENT_PAIRS`** lib pair; does not alter example schema (AC-5 names-only contract preserved).
- **acceptance_check**:
  - All four **`DEV_ENV_BOOTSTRAP_*`** constants defined and grep-able.
  - **`resolve_profile_path`** rejects absolute paths, **`..`**, non-**`.json`** suffix → **`DEV_ENV_BOOTSTRAP_PATH_INVALID`**.
  - Default path **`.cursor/dev-environment.json`** when **`DEV_ENVIRONMENT_CONFIG`** unset.
  - **`shutil.copy2`** only when target absent; skip when exists.
  - CLI **`--bootstrap`** runs bootstrap with documented exit codes.
  - Active/template lib byte-identical for touched symbols.
- **status**: done

---

## T-002 — **`bootstrap_dev_environment_profile_installer_hook`** in **`installer.py`** — AC-1, AC-2

- **ac_ref**: AC-1, AC-2
- **dec_ref**: DEC-0084 § bootstrap posture; architecture `# US-0099` § Hook placement
- **description**: Add thin **`bootstrap_dev_environment_profile_installer_hook(target_root, source_root)`** wrapper in **`installer.py`**. Invoke after **`run_scratchpad_postinstall`**, before **`bootstrap_runbook_commands`** on both **`missing`** and **`upgrade`** paths. Fail-closed return **1** only on **`PATH_INVALID`** / **`SOURCE_MISSING`**; **`SKIPPED_EXISTS`** and **`COPIED`** continue. **`installer.ps1`** / **`installer.sh`** unchanged (delegate to **`installer.py`**).
- **files_affected**:
  - `installer.py`
- **parity_touchpoints**: architecture § Atomic task seeds row 2; **`test_us0099_installer_hook_literals`** (Tranche D).
- **acceptance_check**:
  - Hook placement after **`run_scratchpad_postinstall`**, before **`bootstrap_runbook_commands`** on **`missing`** + **`upgrade`**.
  - Never overwrites existing profile at resolved path.
  - Deterministic log line on copy or skip (names-only; **DEC-0053** compliant).
  - Contract subtest **`test_us0099_installer_hook_literals`** passes (after T-007).
- **status**: done

---

## T-003 — **`bin/postinstall.js`**: repo-root walk + **`spawnSync`** **`--bootstrap`** subprocess — AC-4

- **ac_ref**: AC-4
- **dec_ref**: DEC-0084 § bootstrap posture; architecture `# US-0099` § Hook placement (**postinstall.js**)
- **description**: After banner in **`bin/postinstall.js`**: walk up from **`process.cwd()`** max **6** parents for **`.cursor/scratchpad.md`** or **`its_magic/.its-magic-version`**; if none → **`[DEV_ENV_BOOTSTRAP_SKIP] no consumer repository detected`**, exit **0**. Else **`spawnSync`** Python **`scripts/dev_environment_lib.py --bootstrap --target <repo> --source-root <template>`**. On exit **1**, log remediation hint but do not fail **`npm install`** lifecycle.
- **files_affected**:
  - `bin/postinstall.js`
- **parity_touchpoints**: architecture § Atomic task seeds row 3; **`test_us0099_postinstall_parity`**.
- **acceptance_check**:
  - Contains **`--bootstrap`** + **`dev_environment_lib.py`** spawn literals.
  - Repo detection walk documented (max 6 parents).
  - Global npm edge case exits **0** with skip token.
  - Idempotent on re-run (delegates to helper skip-if-exists).
  - Contract subtest **`test_us0099_postinstall_parity`** passes (after T-007).
- **status**: done

---

## T-004 — Runbook § Dev environment: customize-after-bootstrap; **`DEV_ENV_PROFILE_MISSING`** troubleshooting; bootstrap reason-code family — AC-6

- **ac_ref**: AC-6
- **dec_ref**: DEC-0084 § bootstrap posture; architecture `# US-0099` § Runbook operator UX delta
- **description**: Update **`docs/engineering/runbook.md`** § Dev environment (active + template mirror): bootstrap automatic on install/upgrade/postinstall; manual copy demoted to **customize-after-bootstrap**; troubleshooting for **`DEV_ENV_PROFILE_MISSING`** references auto-bootstrap path; document four **`DEV_ENV_BOOTSTRAP_*`** install-time reason codes distinct from runtime **`DEV_ENV_PROFILE_*`** / **`DEV_ENV_RELAUNCH_*`**.
- **files_affected**:
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 4; **`DEV_ENVIRONMENT_PAIRS`** runbook pair (row 6).
- **acceptance_check**:
  - Before/after UX table per architecture § Runbook operator UX delta.
  - **`DEV_ENV_PROFILE_MISSING`** troubleshooting references bootstrap + customize steps.
  - Install-time **`DEV_ENV_BOOTSTRAP_*`** family documented.
  - Active/template runbook parity for touched sections.
- **status**: done

---

## T-005 — **`test_us0099_copy_when_missing`**, **`test_us0099_upgrade_idempotent`** — AC-1, AC-7

- **ac_ref**: AC-1, AC-7
- **dec_ref**: DEC-0084 § bootstrap posture; architecture `# US-0099` § Contract tests + parity
- **description**: Add contract subtests **`test_us0099_copy_when_missing`** (absent target → **`--bootstrap`** creates file; **`DEV_ENV_BOOTSTRAP_COPIED`** token) and **`test_us0099_upgrade_idempotent`** (double bootstrap → skip on second; no overwrite).
- **files_affected**:
  - `tests/auto_command_contract_test.py`
- **parity_touchpoints**: architecture § Contract tests table rows 1–3; active-only.
- **acceptance_check**:
  - Both test function names present with assertions per architecture table.
  - **`test_us0099_copy_when_missing`** verifies file creation + token.
  - **`test_us0099_upgrade_idempotent`** verifies second run skips without mutation.
- **status**: done

---

## T-006 — **`test_us0099_skip_when_exists`**, **`test_us0099_path_override`** — AC-2, AC-3, AC-7

- **ac_ref**: AC-2, AC-3, AC-7
- **dec_ref**: DEC-0084 § bootstrap posture; architecture `# US-0099` § Path resolution; § Idempotency matrix
- **description**: Add contract subtests **`test_us0099_skip_when_exists`** (pre-seed customized bytes → unchanged; **`DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`**) and **`test_us0099_path_override`** (valid override copies; invalid → **`PATH_INVALID`**, no file).
- **files_affected**:
  - `tests/auto_command_contract_test.py`
- **parity_touchpoints**: architecture § Contract tests table rows 2, 4; active-only.
- **acceptance_check**:
  - Pre-seeded file bytes unchanged after bootstrap.
  - Valid **`DEV_ENVIRONMENT_CONFIG`** override copies to override path.
  - Invalid override emits **`DEV_ENV_BOOTSTRAP_PATH_INVALID`**; no file created.
- **status**: done

---

## T-007 — **`test_us0099_bootstrap_reason_code_inventory`**, **`test_us0099_installer_hook_literals`**, **`test_us0099_postinstall_parity`** — AC-7

- **ac_ref**: AC-7
- **dec_ref**: DEC-0084 §10 (bootstrap family); architecture `# US-0099` § Contract tests + parity
- **description**: Add contract subtests **`test_us0099_bootstrap_reason_code_inventory`** (all four **`DEV_ENV_BOOTSTRAP_*`** in lib), **`test_us0099_installer_hook_literals`** (hook placement on **`missing`** + **`upgrade`**), **`test_us0099_postinstall_parity`** (**postinstall.js** spawn literals). Run `pytest -k us0099` → all seven subtests green.
- **files_affected**:
  - `tests/auto_command_contract_test.py`
- **parity_touchpoints**: architecture § Contract tests table rows 5–7; active-only.
- **acceptance_check**:
  - All seven **`test_us0099_*`** function names present.
  - `pytest -k us0099 tests/auto_command_contract_test.py` exits 0 after T-001..T-004 edits.
  - Reason-code inventory grep-able in **`dev_environment_lib.py`**.
- **status**: done

---

## T-008 — Harness section **§26X** in **`tests/run-tests.ps1`** / **`tests/run-tests.sh`** — AC-7

- **ac_ref**: AC-7
- **dec_ref**: DEC-0084 § bootstrap posture; architecture `# US-0099` § Contract tests + parity (Harness)
- **description**: Register harness section **§26X** (next after **§26W**) in **`tests/run-tests.ps1`** + **`tests/run-tests.sh`** covering `pytest -k us0099` and `python scripts/check_intake_template_parity.py --scope=dev-environment`.
- **files_affected**:
  - `tests/run-tests.ps1`
  - `tests/run-tests.sh`
- **parity_touchpoints**: architecture § Atomic task seeds row 8; harness **§26X** (next free after **§26W**).
- **acceptance_check**:
  - Harness **§26X** registered in both run-tests scripts.
  - Section invokes post-edit gates from sprint.md.
  - Section header references **US-0099** / **DEC-0084** amended § bootstrap posture.
- **status**: done

---

## T-009 — Verify **`check_intake_template_parity.py --scope=dev-environment`** still **PASS** (**`DEV_ENVIRONMENT_PAIRS`** unchanged) — AC-7

- **ac_ref**: AC-7
- **dec_ref**: DEC-0084 §11; architecture `# US-0099` § `DEV_ENVIRONMENT_PAIRS`
- **description**: Final parity sweep: ensure active ↔ template byte-identical for all **`DEV_ENVIRONMENT_PAIRS`** surfaces touched in T-001 + T-004. Confirm **`DEV_ENVIRONMENT_PAIRS`** rows **1–8** unchanged (no new rows for root-only **`installer.py`** / **`bin/postinstall.js`** — contract-test literal guards per **US-0097** precedent). Run `python scripts/check_intake_template_parity.py --scope=dev-environment` → PASS.
- **files_affected**:
  - All **`DEV_ENVIRONMENT_PAIRS`** template mirrors (final parity sweep)
  - `scripts/check_intake_template_parity.py` (verify only — no manifest change expected)
- **parity_touchpoints**: architecture § Atomic task seeds row 9; **`DEV_ENVIRONMENT_PAIRS`** 8-surface inventory unchanged.
- **acceptance_check**:
  - `python scripts/check_intake_template_parity.py --scope=dev-environment` → **`[INTAKE_TEMPLATE_PARITY_OK]`**.
  - No unintended **`DEV_ENVIRONMENT_PAIRS`** row additions.
  - Active/template lib + runbook mirrors byte-identical post-T-001/T-004.
- **status**: done

---

## Recommended /execute ordering

1. **T-001** — stdlib helper + bootstrap CLI (Tranche A)
2. **T-002** — installer hook (Tranche B)
3. **T-003** — postinstall parity (Tranche C)
4. **T-004** — runbook customize-after-bootstrap (Tranche D — docs first)
5. **T-005** → **T-006** → **T-007** — contract subtests (after scripts/docs)
6. **T-008** — harness §26X
7. **T-009** — parity verification sweep (last)
