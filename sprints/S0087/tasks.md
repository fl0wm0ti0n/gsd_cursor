# Sprint S0087 Tasks — US-0097

**sprint_id**: S0087  
**story_refs**: US-0097  
**dec_ref**: DEC-0083 (binding; amends DEC-0045; reframes DEC-0074 paths; composes on DEC-0059, US-0030, US-0071, US-0017)  
**task_count**: 11  
**within_limit**: true (11 ≤ `SPRINT_MAX_TASKS=12`; `SPRINT_AUTO_SPLIT` not triggered)  
**coverage**: AC-1..AC-10 surjective via T-001..T-011 (10 ACs, 11 tasks; architecture seeds 1:1; multi-AC tasks T-003, T-004, T-005, T-007, T-009/T-010)

> No implementation or test code is authored in this phase — dev owns delivery in `/execute`.

---

## T-001 — Remove root **`README.md`** from installer **`[install_paths]`**; confirm **`its_magic/README.md`** in manifest — AC-1

- **ac_ref**: AC-1
- **dec_ref**: DEC-0083 §1; architecture `# US-0097` § Ownership matrix
- **description**: Remove root **`README.md`** from **`docs/engineering/context/installer-owned-paths.manifest`** **`[install_paths]`** (manifest line 42 today). Confirm **`its_magic/README.md`** remains in install paths. Mirror change to **`template/docs/engineering/context/installer-owned-paths.manifest`**. Fresh **`missing`** install on empty consumer target must lay down **no** framework README at root.
- **files_affected**:
  - `docs/engineering/context/installer-owned-paths.manifest`
  - `template/docs/engineering/context/installer-owned-paths.manifest`
- **parity_touchpoints**: architecture § Atomic task seeds row 1; **`PROJECT_README_PAIRS`** manifest pair; **`test_us0097_installer_manifest_no_root_readme`**.
- **acceptance_check**:
  - Root **`README.md`** absent from **`[install_paths]`** in active + template manifests.
  - **`its_magic/README.md`** present in **`[install_paths]`**.
  - Active/template manifest parity for touched sections.
  - Contract subtest **`test_us0097_installer_manifest_no_root_readme`** passes.
- **status**: done

---

## T-002 — Migration **M1–M5** + sentinel **S1–S5** in **`project_readme_coverage_lib.py`** + runbook migration § — AC-2

- **ac_ref**: AC-2
- **dec_ref**: DEC-0083 §2, §5; architecture `# US-0097` § Migration M1–M5; § Placeholder sentinels
- **description**: Implement **`scripts/project_readme_coverage_lib.py`** with sentinel detection **S1–S5** (detection order: **`FRAMEWORK_KIT_REPO=1`** → S1–S4 → S5), migration algorithm **M1–M5** (idempotent), and hybrid fail-closed reason codes (**`PROJECT_README_MIGRATION_AMBIGUOUS`**, **`PROJECT_README_SENTINEL_CONFLICT`**). Mirror to **`template/scripts/project_readme_coverage_lib.py`**. Add runbook migration § with remediation steps for ambiguous/hybrid roots.
- **files_affected**:
  - `scripts/project_readme_coverage_lib.py` (new)
  - `template/scripts/project_readme_coverage_lib.py` (new)
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 2; **`PROJECT_README_PAIRS`** lib pair; **`test_us0097_placeholder_sentinel_table`**.
- **acceptance_check**:
  - **S1–S5** detection rules implemented per DEC-0083 §2 table.
  - **M1–M5** steps idempotent; **M2** preserves operator-authored root; **M5** fail-closed.
  - Nine **`PROJECT_README_*`** reason codes documented in runbook.
  - Active/template lib byte-identical.
  - Contract subtest **`test_us0097_placeholder_sentinel_table`** passes.
- **status**: done

---

## T-003 — Project README bootstrap scaffold + **`vision.md`** H1/purpose sourcing helper — AC-3, AC-5

- **ac_ref**: AC-3, AC-5
- **dec_ref**: DEC-0083 §4; architecture `# US-0097` § Project README scaffold
- **description**: Add bootstrap scaffold materializer to **`project_readme_coverage_lib.py`**: H1 from **`docs/product/vision.md`**, 1–3 sentence purpose, **`## For users`**, **`## For developers`**, **`## Features`**, **`<!-- project-readme-feature-catalog -->`**, framework pointer to **`its_magic/README.md`**. Trigger: root missing or any **S1–S4** sentinel. Document scaffold structure in runbook.
- **files_affected**:
  - `scripts/project_readme_coverage_lib.py`
  - `template/scripts/project_readme_coverage_lib.py`
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 3; **`test_us0097_execute_step23_literals`** (bootstrap portion).
- **acceptance_check**:
  - Scaffold template matches architecture § Project README scaffold block.
  - Vision H1/purpose sourcing helper documented.
  - Bootstrap trigger (missing or S1–S4) documented.
  - Framework catalog confined to **`its_magic/README.md`** — no **USER_*/DEV_*** catalogs at root.
  - Active/template lib parity maintained.
- **status**: done

---

## T-004 — Execute step **23** (**23a**/**23b**/**23c**) in **`execute.md`** + reason codes — AC-3, AC-4, AC-8

- **ac_ref**: AC-3, AC-4, AC-8
- **dec_ref**: DEC-0083 §6; architecture `# US-0097` § Execute step 23
- **description**: Add execute step **23** after step **22** (triad hot-surface) in active + template **`execute.md`**. Sub-steps: **23 preamble** (read **`FRAMEWORK_KIT_REPO`** — skip **23a**/**23b** when **`1`**); **23a Bootstrap** (materialize scaffold when missing/placeholder); **23b Delta (mandatory)** (≥1 catalog bullet with **`\bUS-xxxx\b`** under **`<!-- project-readme-feature-catalog -->`** — fail **`PROJECT_README_DELTA_SKIPPED`**); **23c Hygiene** (compose with step **20** **US-0071** — no duplicate validator when README unchanged). Document reason codes.
- **files_affected**:
  - `.cursor/commands/execute.md`
  - `template/.cursor/commands/execute.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 4; **`PROJECT_README_PAIRS`** execute pair; **`test_us0097_execute_step23_literals`**.
- **acceptance_check**:
  - Step **23** placement after step **22** documented.
  - All four sub-steps (**preamble**, **23a**, **23b**, **23c**) with normative contracts.
  - Reason codes **`PROJECT_README_DELTA_SKIPPED`**, **`PROJECT_README_BOOTSTRAP_SKIPPED`**, **`PROJECT_README_PLACEHOLDER_UNRESOLVED`** grep-able.
  - **US-0071** compose **23c** — no duplicate hygiene when README unchanged.
  - Active/template **`execute.md`** byte-identical for step **23** block.
  - Contract subtest **`test_us0097_execute_step23_literals`** passes.
- **status**: done

---

## T-005 — Release step **3g** in **`release.md`** + gate order **3f→3g→4** — AC-4, AC-7

- **ac_ref**: AC-4, AC-7
- **dec_ref**: DEC-0083 §7; architecture `# US-0097` § Release step 3g
- **description**: Add release step **3g** immediately after **3f**, before step **4** (UAT) in active + template **`release.md`**. When **`PROJECT_README_ENFORCE=1`**: run **`python scripts/validate_project_readme_coverage.py --repo . --enforce`**. When **`0`**: skip with **`PROJECT_README_ENFORCE_SKIPPED`** evidence. On failure: umbrella **`PROJECT_README_COVERAGE_BLOCKED`** + **`PROJECT_README_COVERAGE_GAP:<US-xxxx>`**. Gate order: **3e → 3f (framework) → 3g (project) → 4 (UAT)**.
- **files_affected**:
  - `.cursor/commands/release.md`
  - `template/.cursor/commands/release.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 5; **`PROJECT_README_PAIRS`** release pair; **`test_us0097_release_step3g_literals`**.
- **acceptance_check**:
  - Step **3g** placement after **3f**, before step **4** documented.
  - Validator invocation + enforce toggle documented.
  - Umbrella + sub reason codes grep-able.
  - Independent enforce toggles for framework (**3f**) vs project (**3g**) explicit.
  - Active/template **`release.md`** byte-identical for step **3g** block.
  - Contract subtest **`test_us0097_release_step3g_literals`** passes.
- **status**: done

---

## T-006 — Scratchpad **`PROJECT_README_ENFORCE`**, **`FRAMEWORK_KIT_REPO`** (active + template example) — AC-7

- **ac_ref**: AC-7
- **dec_ref**: DEC-0083 §10; architecture `# US-0097` § Scratchpad keys
- **description**: Document **`PROJECT_README_ENFORCE`** (**`0`** \| **`1`**, default **`1`** post-bootstrap) and **`FRAMEWORK_KIT_REPO`** (**`0`** \| **`1`**, default **`0`**) in active scratchpad comment block + **`template/.cursor/scratchpad.local.example.md`**. Document grandfathering: **`PROJECT_README_ENFORCE=0`** during migration until **`--report`** clean.
- **files_affected**:
  - `.cursor/scratchpad.md` (comment block only)
  - `template/.cursor/scratchpad.local.example.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 6; **`PROJECT_README_PAIRS`** scratchpad pair; **`test_us0097_project_readme_enforce_scratchpad_keys`**.
- **acceptance_check**:
  - Both keys documented with values, defaults, and purpose.
  - Consumer repos never **`FRAMEWORK_KIT_REPO=1`** documented.
  - Grandfathering / migration window documented.
  - Active/template example parity for scratchpad comment block.
  - Contract subtest **`test_us0097_project_readme_enforce_scratchpad_keys`** passes.
- **status**: done

---

## T-007 — Reframe **`validate_readme_feature_coverage.py`** / **US-0091** to **`its_magic/`** paths only; preserve release **3f** — AC-5, AC-6

- **ac_ref**: AC-5, AC-6
- **dec_ref**: DEC-0083 §8; architecture `# US-0097` § Validators; § Ownership matrix
- **description**: Reframe **`scripts/validate_readme_feature_coverage.py`** (**US-0091**) to read **`its_magic/README.md`**, **`template/its_magic/README.md`**, **`docs/developer/README.md`** only — **exclude** consumer root **`README.md`**. Preserve release step **3f** framework gate behavior. Mirror to template. Update path table docs.
- **files_affected**:
  - `scripts/validate_readme_feature_coverage.py`
  - `template/scripts/validate_readme_feature_coverage.py`
  - `docs/engineering/runbook.md` (path table update if needed)
  - `template/docs/engineering/runbook.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 7; **`test_us0097_framework_validator_paths_reframed`**, **`test_us0097_us0091_regression_guard`**.
- **acceptance_check**:
  - Root **`README.md`** excluded from **US-0091** predicate paths.
  - **`its_magic/README.md`** primary framework catalog path.
  - Release **3f** preserved — no regression in framework gate.
  - Active/template validator parity for touched sections.
  - Contract subtests **`test_us0097_framework_validator_paths_reframed`** + **`test_us0097_us0091_regression_guard`** pass.
- **status**: done

---

## T-008 — **`validate_project_readme_coverage.py`** + **`project_readme_coverage_lib.py`** + **`--report`** schema v1 + **`FRAMEWORK_KIT_REPO`** skip — AC-6

- **ac_ref**: AC-6
- **dec_ref**: DEC-0083 §9; architecture `# US-0097` § Validators
- **description**: Implement **`scripts/validate_project_readme_coverage.py`** CLI entrypoint with flags **`--repo`**, **`--backlog`**, **`--self-test`**, **`--report`**, **`--audit-out`**, **`--enforce`**, **`--no-kit-skip`**. Compose on **`project_readme_coverage_lib.py`**. **`--report`** JSON schema v1 fields per architecture. Self-test token **`[PROJECT_README_COVERAGE_SELF_TEST_OK]`**. Skip root validation when **`FRAMEWORK_KIT_REPO=1`**. Mirror to template.
- **files_affected**:
  - `scripts/validate_project_readme_coverage.py` (new)
  - `template/scripts/validate_project_readme_coverage.py` (new)
  - `scripts/project_readme_coverage_lib.py`
  - `template/scripts/project_readme_coverage_lib.py`
- **parity_touchpoints**: architecture § Atomic task seeds row 8; **`PROJECT_README_PAIRS`** validator pair; **`test_us0097_project_readme_coverage_validator_contract`**.
- **acceptance_check**:
  - All CLI flags documented and functional.
  - **`--report`** schema v1 fields match architecture table.
  - Self-test exits 0 with **`[PROJECT_README_COVERAGE_SELF_TEST_OK]`**.
  - **`FRAMEWORK_KIT_REPO=1`** skip documented and functional.
  - Active/template validator byte-identical.
  - Contract subtest **`test_us0097_project_readme_coverage_validator_contract`** passes.
- **status**: done

---

## T-009 — Eight **`test_us0097_*`** contract subtests — AC-9

- **ac_ref**: AC-9
- **dec_ref**: DEC-0083 §12; architecture `# US-0097` § Contract tests + parity
- **description**: Add eight additive contract subtests to **`tests/auto_command_contract_test.py`**: `test_us0097_installer_manifest_no_root_readme`, `test_us0097_execute_step23_literals`, `test_us0097_release_step3g_literals`, `test_us0097_placeholder_sentinel_table`, `test_us0097_framework_validator_paths_reframed`, `test_us0097_project_readme_enforce_scratchpad_keys`, `test_us0097_project_readme_coverage_validator_contract`, `test_us0097_us0091_regression_guard`. Run `pytest -k us0097` → all green.
- **files_affected**:
  - `tests/auto_command_contract_test.py`
- **parity_touchpoints**: architecture § Contract tests table; active-only.
- **acceptance_check**:
  - All eight test function names present with assertions per architecture table.
  - `pytest -k us0097` exits 0 after T-001..T-008 doc/script edits.
  - **`test_us0097_us0091_regression_guard`** confirms framework **3f** preserved.
- **status**: done

---

## T-010 — **`PROJECT_README_PAIRS`** parity manifest + harness **§26V** — AC-9

- **ac_ref**: AC-9
- **dec_ref**: DEC-0083 §12; architecture `# US-0097` § `PROJECT_README_PAIRS`
- **description**: Wire **`check_intake_template_parity.py --scope=project-readme`** manifest **`PROJECT_README_PAIRS`** (8 surface pairs per architecture table). Register harness section **§26V** in **`tests/run-tests.ps1`** + **`tests/run-tests.sh`**. Ensure active ↔ template byte-identical for all touched surfaces from T-001..T-008.
- **files_affected**:
  - `scripts/check_intake_template_parity.py`
  - `template/scripts/check_intake_template_parity.py`
  - `tests/run-tests.ps1`
  - `tests/run-tests.sh`
  - All **`PROJECT_README_PAIRS`** template mirrors (final parity sweep)
- **parity_touchpoints**: architecture § `PROJECT_README_PAIRS` table (8 pairs).
- **acceptance_check**:
  - `python scripts/check_intake_template_parity.py --scope=project-readme` → PASS.
  - Harness **§26V** registered in both run-tests scripts.
  - All eight **`PROJECT_README_PAIRS`** surfaces byte-identical active/template.
  - Parity script scope **`project-readme`** documented in script help.
- **status**: done

---

## T-011 — Runbook operator recipes (bootstrap, migration, gate troubleshooting) — AC-10

- **ac_ref**: AC-10
- **dec_ref**: DEC-0083 § Implementation tranche order; architecture `# US-0097` § Runbook operator recipes
- **description**: Add runbook operator recipes table per architecture: fresh consumer repo bootstrap; legacy framework root README migration; operator-authored root (S5) preserve; hybrid/ambiguous remediation; migration window with **`PROJECT_README_ENFORCE=0`**; kit repo dogfooding with **`FRAMEWORK_KIT_REPO=1`**. Include troubleshooting for **`PROJECT_README_COVERAGE_BLOCKED`**, **`PROJECT_README_MIGRATION_AMBIGUOUS`**, and related reason codes. Mirror to template.
- **files_affected**:
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 11; **`PROJECT_README_PAIRS`** runbook pair.
- **acceptance_check**:
  - Operator recipes table with ≥6 scenarios per architecture § Runbook operator recipes.
  - Troubleshooting § for umbrella + migration reason codes.
  - Tranche order A→B→C→D documented for operators.
  - Active/template runbook parity for touched sections.
- **status**: done

---

## Recommended /execute ordering

1. **T-001** — installer manifest boundary (Tranche A)
2. **T-002** — migration + sentinels lib (Tranche A)
3. **T-003** — bootstrap scaffold (Tranche B)
4. **T-004** — execute step 23 (Tranche C)
5. **T-005** — release step 3g (Tranche C)
6. **T-006** — scratchpad keys (Tranche C)
7. **T-007** — US-0091 path reframe (Tranche D)
8. **T-008** — project validator (Tranche D)
9. **T-009** — eight test_us0097_* contract subtests (after docs/scripts)
10. **T-010** — PROJECT_README_PAIRS parity + harness §26V
11. **T-011** — runbook operator recipes (last)
