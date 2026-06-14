# Sprint S0088 Tasks — US-0098

**sprint_id**: S0088  
**story_refs**: US-0098  
**dec_ref**: DEC-0084 (binding; composes DEC-0071/US-0085, US-0064, US-0086, US-0093; research R-0085)  
**task_count**: 11  
**within_limit**: true (11 ≤ `SPRINT_MAX_TASKS=12`; `SPRINT_AUTO_SPLIT` not triggered)  
**coverage**: AC-1..AC-10 surjective via T-001..T-011 (10 ACs, 11 tasks; architecture seeds 1:1; multi-AC tasks T-003, T-004, T-005, T-006, T-008/T-009/T-011)

> No implementation or test code is authored in this phase — dev owns delivery in `/execute`.

---

## T-001 — **`template/.cursor/dev-environment.json.example`** schema v1 + **`.gitignore`** / **`.cursorignore`** local profile lines — AC-2

- **ac_ref**: AC-2
- **dec_ref**: DEC-0084 §2; architecture `# US-0098` § Profile schema v1
- **description**: Add committed **`template/.cursor/dev-environment.json.example`** with schema v1 fields (`schema_version`, `detected_mode`, `operator_seeded`, `last_updated`, `compose_file`, `service`, `target_id`, `connect` with **`*Env`** keys only, `rebuild_recipe`, `env_refs`, `evidence_refs`). Add **`.cursor/dev-environment.json`** to active + template **`.gitignore`** and **`.cursorignore`**. Names-only placeholders; no secret literals.
- **files_affected**:
  - `template/.cursor/dev-environment.json.example` (new)
  - `.gitignore`
  - `.cursorignore`
  - `template/.gitignore` (or documented exception per architecture)
- **parity_touchpoints**: architecture § Atomic task seeds row 1; **`DEV_ENVIRONMENT_PAIRS`** example + gitignore pairs; **`test_us0098_dev_environment_schema_contract`**.
- **acceptance_check**:
  - Example JSON validates against schema v1 field table in DEC-0084 §2.
  - Local profile path gitignored + cursorignored in active + template.
  - No inline secret literals in committed example.
  - Contract subtest **`test_us0098_dev_environment_schema_contract`** passes.
- **status**: done

---

## T-002 — Scratchpad **`DEV_AUTO_LAUNCH_PROFILE`**, **`DEV_ENVIRONMENT_CONFIG`** (active + template + local example) — AC-1

- **ac_ref**: AC-1
- **dec_ref**: DEC-0084 §1; architecture `# US-0098` § Scratchpad keys
- **description**: Document **`DEV_AUTO_LAUNCH_PROFILE`** (`off` | `deterministic_v1`, default **`off`**) and **`DEV_ENVIRONMENT_CONFIG`** (repo-relative path, default **`.cursor/dev-environment.json`**) in active scratchpad comment block + **`template/.cursor/scratchpad.md`** + **`template/.cursor/scratchpad.local.example.md`**. Document orthogonality to **`AUTO_REMOTE_AUTOMATION_PROFILE`** (**US-0086**). When **`off`**, step **24** zero overhead.
- **files_affected**:
  - `.cursor/scratchpad.md` (comment block only)
  - `template/.cursor/scratchpad.md`
  - `template/.cursor/scratchpad.local.example.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 2; **`DEV_ENVIRONMENT_PAIRS`** scratchpad pairs; **`test_us0098_dev_auto_launch_scratchpad_keys`**.
- **acceptance_check**:
  - Both keys documented with values, defaults, and purpose.
  - Default **`off`** explicit; manual workflows unchanged when off.
  - Orthogonality to **US-0086** remote profile documented.
  - Active/template scratchpad parity for touched comment blocks.
  - Contract subtest **`test_us0098_dev_auto_launch_scratchpad_keys`** passes.
- **status**: done

---

## T-003 — **`dev_environment_lib.py`**: **`load_profile`**, schema validation, security heuristics + **`--self-test`** — AC-2, AC-8

- **ac_ref**: AC-2, AC-8
- **dec_ref**: DEC-0084 §8, §9; architecture `# US-0098` § Stdlib helper; § Security
- **description**: Implement **`scripts/dev_environment_lib.py`** with **`load_profile(path)`** (parse JSON; reject inline secrets; names-only schema validation), security heuristics per four-layer **US-0085** audit, and CLI **`--self-test`** emitting **`[DEV_ENVIRONMENT_SELF_TEST_OK]`**. Mirror to **`template/scripts/dev_environment_lib.py`**.
- **files_affected**:
  - `scripts/dev_environment_lib.py` (new)
  - `template/scripts/dev_environment_lib.py` (new)
- **parity_touchpoints**: architecture § Atomic task seeds row 3; **`DEV_ENVIRONMENT_PAIRS`** lib pair; **`test_us0098_dev_environment_schema_contract`** (schema portion).
- **acceptance_check**:
  - **`load_profile`** rejects inline secret-like literals.
  - Only **`*Env`** suffix keys allowed in **`connect`** object.
  - Violation emits **`DEV_ENV_SECRET_SURFACE_VIOLATION`** reason code constant.
  - **`python scripts/dev_environment_lib.py --self-test`** exits 0 with **`[DEV_ENVIRONMENT_SELF_TEST_OK]`**.
  - Active/template lib byte-identical.
- **status**: done

---

## T-004 — **`detect_mode`** precedence + **`classify_touched_files`** Tier A/B/C + **`build_relaunch_plan`** — AC-3, AC-4, AC-8

- **ac_ref**: AC-3, AC-4, AC-8
- **dec_ref**: DEC-0084 §3, §4; architecture `# US-0098` § Detection matrix; § Tier A/B/C
- **description**: Add **`detect_mode(repo, profile, scratchpad)`** with precedence algorithm (profile off → skip; **US-0086** remote wins over **docker-host-local**; compose + local docker → **docker-host-local**; **`DEV_SERVER_*`** → **local**; else **`DEV_ENV_DETECT_AMBIGUOUS`**). Add **`classify_touched_files(paths)`** Tier A/B/C table and **`build_relaunch_plan(mode, tier, profile)`** command list (no `.env` reads). Bounded retry constants (**`retry_count`≤2**; delays 5s/15s). Bind-mount skip default documented.
- **files_affected**:
  - `scripts/dev_environment_lib.py`
  - `template/scripts/dev_environment_lib.py`
- **parity_touchpoints**: architecture § Atomic task seeds row 4; **`test_us0098_detection_mode_precedence_literals`**, **`test_us0098_execute_step24_literals`** (tier portion), **`test_us0098_reason_code_inventory`**.
- **acceptance_check**:
  - Four detection modes implemented: **`local`**, **`docker-host-local`**, **`docker`**, **`ssh`**.
  - **US-0086** precedence over **docker-host-local** documented in code/constants.
  - Tier A/B/C file-class table matches architecture § Tier A/B/C.
  - **`retry_count`** max **2** enforced in plan builder.
  - Active/template lib parity maintained.
  - Contract subtests **`test_us0098_detection_mode_precedence_literals`** + tier/reason portions pass.
- **status**: done

---

## T-005 — **`format_connect_block`** + reason-code registry constants — AC-5, AC-8

- **ac_ref**: AC-5, AC-8
- **dec_ref**: DEC-0084 §7, §10; architecture `# US-0098` § Execute step 24; § Reason codes
- **description**: Add **`format_connect_block(profile, outcome) -> str`** emitting Markdown Connect block with mandatory fields: `runtime_mode`, `connect_endpoint`, `health_path`, `service_id`/`container_id`, `target_id`, `env_refs`, `relaunch_outcome`. Register **`DEV_ENV_PROFILE_*`** and **`DEV_ENV_RELAUNCH_*`** reason-code constants per DEC-0084 §10 inventory.
- **files_affected**:
  - `scripts/dev_environment_lib.py`
  - `template/scripts/dev_environment_lib.py`
- **parity_touchpoints**: architecture § Atomic task seeds row 5; **`test_us0098_connect_block_field_literals`**, **`test_us0098_reason_code_inventory`**.
- **acceptance_check**:
  - Connect block includes all mandatory field names per architecture table.
  - No secret values in formatted output — names-only **`env_refs`**.
  - Full reason-code inventory grep-able in lib constants.
  - Contract subtests **`test_us0098_connect_block_field_literals`** + **`test_us0098_reason_code_inventory`** pass.
  - Active/template lib parity maintained.
- **status**: done

---

## T-006 — Execute step **24** (**24a–24d**) + **`dev_to_qa.md`** evidence tuple prose (active + template **`execute.md`**) — AC-4, AC-5, AC-7

- **ac_ref**: AC-4, AC-5, AC-7
- **dec_ref**: DEC-0084 §5, §6; architecture `# US-0098` § Execute step 24
- **description**: Add execute step **24** after step **23** (**US-0097**) in active + template **`execute.md`**. Sub-steps: **24 preamble** (read gate — skip **24a–24d** when **`off`**); **24a Gate + load**; **24b Detect + persist**; **24c Relaunch (bounded)**; **24d Connect + handoff**. Document **`dev_to_qa.md`** evidence tuple fields (`dev_auto_launch_profile`, `runtime_mode`, `relaunch_tier`, `relaunch_command`, `relaunch_outcome`, `retry_count`, `reason_code`). Document exact literal **`refresh dev environment`** (case-sensitive whole phrase). Orthogonality to step **18** (**US-0065**) and step **17** (**US-0084**).
- **files_affected**:
  - `.cursor/commands/execute.md`
  - `template/.cursor/commands/execute.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 6; **`DEV_ENVIRONMENT_PAIRS`** execute pair; **`test_us0098_execute_step24_literals`**, **`test_us0098_refresh_dev_environment_phrase_literal`**.
- **acceptance_check**:
  - Step **24** placement after step **23** documented.
  - All five blocks (**preamble**, **24a**, **24b**, **24c**, **24d**) with normative contracts.
  - Evidence tuple field names grep-able in execute.md.
  - Exact phrase **`refresh dev environment`** documented (case-sensitive).
  - Zero overhead when **`DEV_AUTO_LAUNCH_PROFILE=off`** explicit.
  - Active/template **`execute.md`** byte-identical for step **24** block.
  - Contract subtests **`test_us0098_execute_step24_literals`** + **`test_us0098_refresh_dev_environment_phrase_literal`** pass.
- **status**: done

---

## T-007 — **`auto-orchestration-reference.md`** dev auto-launch § + **`runtime-connectivity.md`** cross-link — AC-6

- **ac_ref**: AC-6
- **dec_ref**: DEC-0084 §3, §7; architecture `# US-0098` § Detection matrix; § Orthogonality
- **description**: Add dev auto-launch profile section to active + template **`auto-orchestration-reference.md`**: composition with **US-0086** remote precedence, **US-0085** `.env` exclusion, **`DEV_SERVER_*`** semantics, no **`release-targets.json`** schema change. Cross-link **`docs/engineering/runtime-connectivity.md`** for Connect field alignment.
- **files_affected**:
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
  - `docs/engineering/runtime-connectivity.md` (cross-link only)
- **parity_touchpoints**: architecture § Atomic task seeds row 7; **`DEV_ENVIRONMENT_PAIRS`** auto-orchestration pair; **`test_us0098_us0086_compose_no_schema_change`**.
- **acceptance_check**:
  - Dev auto-launch § documents **US-0086** precedence over **docker-host-local**.
  - **US-0085** no-`.env`-read inheritance documented.
  - **`release-targets.json`** schema unchanged — explicit negative guard.
  - **`runtime-connectivity.md`** cross-link present.
  - Active/template auto-orchestration-reference parity for touched sections.
  - Contract subtest **`test_us0098_us0086_compose_no_schema_change`** passes.
- **status**: done

---

## T-008 — Eight **`test_us0098_*`** contract subtests — AC-9

- **ac_ref**: AC-9
- **dec_ref**: DEC-0084 §11; architecture `# US-0098` § Contract tests + parity
- **description**: Add eight additive contract subtests to **`tests/auto_command_contract_test.py`**: `test_us0098_dev_auto_launch_scratchpad_keys`, `test_us0098_execute_step24_literals`, `test_us0098_dev_environment_schema_contract`, `test_us0098_detection_mode_precedence_literals`, `test_us0098_reason_code_inventory`, `test_us0098_connect_block_field_literals`, `test_us0098_refresh_dev_environment_phrase_literal`, `test_us0098_us0086_compose_no_schema_change`. Run `pytest -k us0098` → all green.
- **files_affected**:
  - `tests/auto_command_contract_test.py`
- **parity_touchpoints**: architecture § Contract tests table; active-only.
- **acceptance_check**:
  - All eight test function names present with assertions per architecture table.
  - `pytest -k us0098` exits 0 after T-001..T-007 doc/script edits.
  - **`test_us0098_us0086_compose_no_schema_change`** confirms **`release-targets.json`** unchanged.
- **status**: done

---

## T-009 — **`DEV_ENVIRONMENT_PAIRS`** parity manifest + **`check_intake_template_parity.py --scope=dev-environment`** — AC-9

- **ac_ref**: AC-9
- **dec_ref**: DEC-0084 §11; architecture `# US-0098` § `DEV_ENVIRONMENT_PAIRS`
- **description**: Wire **`check_intake_template_parity.py --scope=dev-environment`** manifest **`DEV_ENVIRONMENT_PAIRS`** (8 surface pairs per architecture table). Ensure active ↔ template byte-identical for all touched surfaces from T-001..T-007.
- **files_affected**:
  - `scripts/check_intake_template_parity.py`
  - `template/scripts/check_intake_template_parity.py`
  - All **`DEV_ENVIRONMENT_PAIRS`** template mirrors (final parity sweep)
- **parity_touchpoints**: architecture § `DEV_ENVIRONMENT_PAIRS` table (8 pairs).
- **acceptance_check**:
  - `python scripts/check_intake_template_parity.py --scope=dev-environment` → PASS.
  - All eight **`DEV_ENVIRONMENT_PAIRS`** surfaces byte-identical active/template.
  - Parity script scope **`dev-environment`** documented in script help.
- **status**: done

---

## T-010 — Runbook operator recipes (enable, seed, refresh, troubleshooting, precedence) — AC-10

- **ac_ref**: AC-10
- **dec_ref**: DEC-0084 § Implementation tranche order; architecture `# US-0098` § Runbook operator recipes
- **description**: Add runbook operator recipes table per architecture: enable dev auto-launch; seed profile; force relaunch via **`refresh dev environment`**; profile off / manual mode; ambiguous stack remediation; remote + local both on ( **US-0086** wins); bind-mount hot reload skip. Include troubleshooting for **`DEV_ENV_*`** reason codes. Mirror to template.
- **files_affected**:
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 10; **`DEV_ENVIRONMENT_PAIRS`** runbook pair.
- **acceptance_check**:
  - Operator recipes table with ≥7 scenarios per architecture § Runbook operator recipes.
  - Troubleshooting § for **`DEV_ENV_PROFILE_*`** and **`DEV_ENV_RELAUNCH_*`** families.
  - Tranche order A→B→C→D documented for operators.
  - Active/template runbook parity for touched sections.
- **status**: done

---

## T-011 — Harness section **§26W** in **`tests/run-tests.ps1`** / **`tests/run-tests.sh`** — AC-9

- **ac_ref**: AC-9
- **dec_ref**: DEC-0084 §11; architecture `# US-0098` § Contract tests + parity (Harness)
- **description**: Register harness section **§26W** in **`tests/run-tests.ps1`** + **`tests/run-tests.sh`** covering `pytest -k us0098`, `python scripts/dev_environment_lib.py --self-test`, and `python scripts/check_intake_template_parity.py --scope=dev-environment`.
- **files_affected**:
  - `tests/run-tests.ps1`
  - `tests/run-tests.sh`
- **parity_touchpoints**: architecture § Atomic task seeds row 11; harness **§26W** (next free after **§26V**).
- **acceptance_check**:
  - Harness **§26W** registered in both run-tests scripts.
  - Section invokes all three post-edit gates from sprint.md.
  - Section header references **US-0098** / **DEC-0084**.
- **status**: done

---

## Recommended /execute ordering

1. **T-001** — schema example + gitignore (Tranche A)
2. **T-002** — scratchpad keys (Tranche A)
3. **T-003** — load_profile + security + self-test (Tranche B)
4. **T-004** — detect + classify + relaunch plan (Tranche B)
5. **T-005** — connect block + reason codes (Tranche B)
6. **T-006** — execute step 24 (Tranche C)
7. **T-007** — auto-orchestration-reference + runtime-connectivity cross-link (Tranche C)
8. **T-008** — eight test_us0098_* contract subtests (after docs/scripts)
9. **T-009** — DEV_ENVIRONMENT_PAIRS parity manifest
10. **T-010** — runbook operator recipes
11. **T-011** — harness §26W (last)
