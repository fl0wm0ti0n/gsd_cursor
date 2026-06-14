## Sprint Plan — **S0090** / **US-0100** — post-**`/sprint-plan`** → **`/plan-verify`** (**qa**)

> **2026-06-15T04:00:00Z** — **`/sprint-plan`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260615-01`, `fresh_context_marker=tl-S0090-US0100-sprint-plan-20260615T040000Z-fresh`, `runtime_proof_id=rp-auto-20260615-01-sprint-plan-tech-lead-20260615T040000Z-S0090-US0100`, `proof_hash=c33f47806589a544ecb99e4b5c30449142bca3ef1774356415862d5ce8ac8e9f`). Sprint **`S0090`** created; **AC-1..AC-10** surjective via **T-001..T-012** (12 architecture seeds; `task_count=12`, `within_limit=true`; AC-10 pre-satisfied at architecture). Story **`US-0100`** remains **OPEN** (**US-0045**). **Do not implement** in this phase. Next phase is **`/plan-verify`** (fresh **qa**).

### Sprint anchor

- **Sprint overview**: `sprints/S0090/sprint.md`
- **Tasks**: `sprints/S0090/tasks.md` (**T-001..T-012**)
- **Plan-verify**: `sprints/S0090/plan-verify.json` (**PENDING**)
- **Architecture**: `docs/engineering/architecture.md` `# US-0100`
- **Decision**: `decisions/DEC-0085.md`
- **Research**: `docs/engineering/research.md` `R-0087`

### AC ↔ Task map (locked for /plan-verify and /execute)

| AC | Task(s) | Summary |
|----|---------|---------|
| AC-1 | T-002 | `CHANGELOG.md` + template stub |
| AC-2 | T-003 | Per-version path + example |
| AC-3 | T-001, T-004 | Lib derive/promote + `/release` step 19 |
| AC-4 | T-004, T-005 | Queue `release_version` binding |
| AC-5 | T-009 | `release-all.sh` `-F` + enforce |
| AC-6 | T-007, T-008 | Backfill script + manifest |
| AC-7 | T-001, T-006 | Validator + lib fail codes |
| AC-8 | T-004, T-010 | `release.md` step 19 + runbook |
| AC-9 | T-011, T-012 | Ten `test_us0100_*` + parity + harness §26Y |
| AC-10 | *(architecture)* | `DEC-0085` + `# US-0100` — plan-verify attestation |

### Recommended /execute ordering

1. **T-001** → **T-002** → **T-003** — Tranche A (lib + stubs)
2. **T-006** — validator (after lib)
3. **T-004** → **T-005** — `/release` step 19 + queue binding
4. **T-007** → **T-008** — backfill + manifest
5. **T-009** — `release-all.sh` `-F`
6. **T-010** — runbook version-doc workflow
7. **T-011** — contract subtests
8. **T-012** — harness §26Y + parity sweep (last)

### Scope guards for `/execute`

- **Do not** replace or overwrite non-target **`Sxxxx-release-notes.md`**.
- **Do not** pass sprint notes to **`gh -F`**.
- **Do not** bypass **`RELEASE_PUBLISH_MODE`** confirmation.
- **Do not** default **`--generate-notes`** without **`RELEASE_CHANGELOG_ALLOW_GENERATE_NOTES=1`**.

### Evidence refs

- `sprints/S0090/sprint.md`
- `sprints/S0090/tasks.md`
- `sprints/S0090/plan-verify.json`
- `handoffs/resume_brief.md` (top pointer → `/plan-verify`)

### Next

- **`/plan-verify`** (fresh **qa**) for **`S0090`** / **US-0100**

---

## Architecture — **US-0100** — post-**`/architecture`** → **`/sprint-plan`** (**tech-lead**)

> **2026-06-15T03:00:00Z** — **`/architecture`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260615-01`, `fresh_context_marker=tl-US0100-architecture-20260615T030000Z-fresh`, `runtime_proof_id=rp-auto-20260615-01-architecture-tech-lead-20260615T030000Z-US0100`, `proof_hash=bfeb6413be42db2a44de3291992c80a9839586fbc13d7b5d0439fa4e5d5f66f0`). Binding **`DEC-0085`** authored; **`# US-0100`** appended; **12** atomic task seeds (`task_count=12`, `within_limit=true` at **`SPRINT_MAX_TASKS`** threshold). Story **`US-0100`** remains **OPEN** (**US-0045**). **Do not implement** in this phase. Next phase is **`/sprint-plan`** (fresh **tech-lead**).

### Architecture anchor

- **Architecture**: `docs/engineering/architecture.md` `# US-0100`
- **Decision**: `decisions/DEC-0085.md`
- **Research**: `docs/engineering/research.md` `R-0087`

### AC ↔ Seed map (locked for sprint-plan)

| Seed | AC | Summary |
|------|-----|---------|
| 1 | AC-3, AC-7 | **`release_changelog_lib.py`** — derive/coalesce/promote/fingerprint API |
| 2 | AC-1 | **`CHANGELOG.md`** + **`template/CHANGELOG.md`** stub |
| 3 | AC-2 | Per-version path + **`vX.Y.Z-release-notes.md.example`** |
| 4 | AC-3, AC-4, AC-8 | **`/release`** step **19** (19a–19d) active + template |
| 5 | AC-4 | Queue **`release_version`** binding helper |
| 6 | AC-7 | **`release_changelog_validate.py`** + 10 reason codes |
| 7 | AC-6 | **`release_changelog_backfill.py`** Tier A/B/C |
| 8 | AC-6 | Backfill manifest + runbook operator guidance |
| 9 | AC-5 | **`release-all.sh`** **`-F`** replace **`--generate-notes`** |
| 10 | AC-8 | Runbook version-doc workflow (active + template) |
| 11 | AC-9 | Ten **`test_us0100_*`** contract subtests |
| 12 | AC-9, AC-10 | **`RELEASE_CHANGELOG_PAIRS`** parity + harness **§26Y** |

**AC-10** (architecture + decision): pre-satisfied at **`/architecture`** — **`DEC-0085`** + **`# US-0100`**.

### Recommended /sprint-plan ordering

1. Tranche A — lib + stubs (seeds **1–3**)
2. **`/release`** hook + queue binding (seeds **4–5**)
3. Validator + backfill (seeds **6–8**)
4. Publish integration (seed **9**)
5. Docs + tests + parity (seeds **10–12**)

### Scope guards for `/sprint-plan` and `/execute`

- **Do not** replace or overwrite non-target **`Sxxxx-release-notes.md`** (**US-0040**).
- **Do not** pass sprint notes to **`gh -F`** — per-version semver file only.
- **Do not** bypass **`RELEASE_PUBLISH_MODE`** confirmation (**US-0054**).
- **Do not** default **`--generate-notes`** — fail-closed unless **`RELEASE_CHANGELOG_ALLOW_GENERATE_NOTES=1`**.
- **Do not** remove **US-0067** operator hints from sprint notes.

### Top risks (carry to /sprint-plan)

- **R1**: Synthetic semver noise — Tier B manifest + **`remediation`** labels.
- **R2**: **`[Unreleased]`** promotion race — fingerprint idempotency per semver.
- **R3**: Pre-release filename edge cases — semver stem without **`v`** prefix.

### Evidence refs

- `decisions/DEC-0085.md`
- `docs/engineering/architecture.md` (`# US-0100`)
- `docs/engineering/research.md` (`R-0087`)
- `docs/product/backlog.md` (`## US-0100` — `architecture_notes`)
- `handoffs/resume_brief.md` (top pointer → `/sprint-plan`)

### Next

- **`/sprint-plan`** (fresh **tech-lead**) for **`US-0100`**

---

## Sprint Plan — **S0089** / **US-0099** — post-**`/sprint-plan`** → **`/plan-verify`** (**qa**)

> **2026-06-14T18:00:00Z** — **`/sprint-plan`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260614-01`, `fresh_context_marker=tl-S0089-US0099-sprint-plan-20260614T180000Z-fresh`, `runtime_proof_id=rp-auto-20260614-01-sprint-plan-tech-lead-20260614T180000Z-S0089-US0099`, `proof_hash=22ff8dd999cdfbddaffc07b6581f2b51e7638c82f1899f271641fbf710a54038`). Sprint **`S0089`** created; **AC-1..AC-8** surjective via **T-001..T-009** (9 architecture seeds; `task_count=9`, `within_limit=true`; AC-8 pre-satisfied at architecture). Story **`US-0099`** remains **OPEN** (**US-0045**). **Do not implement** in this phase. Next phase is **`/plan-verify`** (fresh **qa**).

### Sprint anchor

- **Sprint overview**: `sprints/S0089/sprint.md`
- **Tasks**: `sprints/S0089/tasks.md` (**T-001..T-009**)
- **Plan-verify**: `sprints/S0089/plan-verify.json` (**PENDING**)
- **Architecture**: `docs/engineering/architecture.md` `# US-0099`
- **Decision**: `decisions/DEC-0084.md` (amended § bootstrap posture)
- **Research**: `docs/engineering/research.md` `R-0086`

### AC ↔ Task map (locked for /plan-verify and /execute)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1, AC-3, AC-5 | bootstrap_dev_environment_profile + resolve_profile_path + DEV_ENV_BOOTSTRAP_* + --bootstrap CLI |
| T-002 | AC-1, AC-2 | installer.py hook after run_scratchpad_postinstall |
| T-003 | AC-4 | bin/postinstall.js spawnSync --bootstrap subprocess |
| T-004 | AC-6 | Runbook customize-after-bootstrap + DEV_ENV_PROFILE_MISSING troubleshooting |
| T-005 | AC-1, AC-7 | test_us0099_copy_when_missing + test_us0099_upgrade_idempotent |
| T-006 | AC-2, AC-3, AC-7 | test_us0099_skip_when_exists + test_us0099_path_override |
| T-007 | AC-7 | test_us0099_bootstrap_reason_code_inventory + installer/postinstall parity literals |
| T-008 | AC-7 | Harness §26X in run-tests.ps1/sh |
| T-009 | AC-7 | DEV_ENVIRONMENT_PAIRS parity verification (--scope=dev-environment) |

**AC-8** (architecture + decision): pre-satisfied at `/architecture` — **DEC-0084** amended, `# US-0099` locked; plan-verify attestation only.

### Recommended /execute ordering

1. **T-001** (Tranche A — stdlib helper + bootstrap CLI)
2. **T-002** (Tranche B — installer hook)
3. **T-003** (Tranche C — postinstall parity)
4. **T-004** (Tranche D — runbook)
5. **T-005** → **T-006** → **T-007** (contract subtests — after scripts/docs)
6. **T-008** (harness §26X)
7. **T-009** (parity sweep — last)

### Scope guards for `/execute`

- **Do not** change profile schema v1 or execute step **24** semantics.
- **Do not** overwrite existing profile files on upgrade or re-run.
- **Do not** add local profile to **`install_paths`** manifest.
- **Do not** auto-enable **`DEV_AUTO_LAUNCH_PROFILE`**.
- **Do not** bootstrap **`.cursor/remote.json`**.
- **Do not** read **`.env`** during bootstrap.

### Post-edit gates (from sprint.md)

1. `pytest -k us0099 tests/auto_command_contract_test.py`
2. `python scripts/check_intake_template_parity.py --scope=dev-environment`

### Next

- **`/plan-verify`** (fresh **qa**) for **`S0089`** / **`US-0099`**

---

## Sprint Plan — **S0088** / **US-0098** — post-**`/sprint-plan`** → **`/plan-verify`** (**qa**)

> **2026-06-14T09:00:00Z** — **`/sprint-plan`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260613-01`, `fresh_context_marker=tl-S0088-US0098-sprint-plan-20260614T090000Z-fresh`, `runtime_proof_id=rp-auto-20260613-01-sprint-plan-tech-lead-20260614T090000Z-S0088-US0098`, `proof_hash=e2ea250c9738f1723767009351a261b42226bd253880f0d31aa04a139594a69f`). Sprint **`S0088`** created; **AC-1..AC-10** surjective via **T-001..T-011** (11 architecture seeds; `task_count=11`, `within_limit=true`). Story **`US-0098`** remains **OPEN** (**US-0045**). **Do not implement** in this phase. Next phase is **`/plan-verify`** (fresh **qa**).

### Sprint anchor

- **Sprint overview**: `sprints/S0088/sprint.md`
- **Tasks**: `sprints/S0088/tasks.md` (**T-001..T-011**)
- **Plan-verify**: `sprints/S0088/plan-verify.json` (**PENDING**)
- **Architecture**: `docs/engineering/architecture.md` `# US-0098`
- **Decision**: `decisions/DEC-0084.md`
- **Research**: `docs/engineering/research.md` `R-0085`

### AC ↔ Task map (locked for /plan-verify and /execute)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-2 | dev-environment.json.example + gitignore/cursorignore |
| T-002 | AC-1 | Scratchpad DEV_AUTO_LAUNCH_PROFILE + DEV_ENVIRONMENT_CONFIG |
| T-003 | AC-2, AC-8 | dev_environment_lib.py load_profile + security + --self-test |
| T-004 | AC-3, AC-4, AC-8 | detect_mode + classify + build_relaunch_plan |
| T-005 | AC-5, AC-8 | format_connect_block + reason-code registry |
| T-006 | AC-4, AC-5, AC-7 | Execute step 24 (24a–24d) + dev_to_qa evidence tuple |
| T-007 | AC-6 | auto-orchestration-reference § + runtime-connectivity cross-link |
| T-008 | AC-9 | Eight test_us0098_* contract subtests |
| T-009 | AC-9 | DEV_ENVIRONMENT_PAIRS parity manifest |
| T-010 | AC-10 | Runbook operator recipes |
| T-011 | AC-9 | Harness §26W in run-tests.ps1/sh |

### Recommended /execute ordering

1. **T-001** → **T-002** (Tranche A — schema + scratchpad)
2. **T-003** → **T-004** → **T-005** (Tranche B — stdlib helper)
3. **T-006** → **T-007** (Tranche C — execute step 24 + docs)
4. **T-008** → **T-009** (contract tests + parity — after docs/scripts)
5. **T-010** (runbook recipes)
6. **T-011** (harness §26W — last)

### Scope guards for `/execute`

- **Do not** change **`release-targets.json`** schema — **`test_us0098_us0086_compose_no_schema_change`** mandatory.
- **Do not** read **`.env`** in helper or execute step **24** paths.
- **Do not** conflate **docker-host-local** with **US-0086** remote docker.
- **Do not** add mandatory unbounded watch daemon v1.
- **Do not** run step **24** overhead when **`DEV_AUTO_LAUNCH_PROFILE=off`**.

### Post-edit gates (from sprint.md)

1. `pytest -k us0098 tests/auto_command_contract_test.py`
2. `python scripts/dev_environment_lib.py --self-test`
3. `python scripts/check_intake_template_parity.py --scope=dev-environment`

### Next

- **`/plan-verify`** (fresh **qa**) for **`S0088`** / **`US-0098`**

---

## Sprint Plan — **S0087** / **US-0097** — post-**`/sprint-plan`** → **`/plan-verify`** (**qa**)

> **2026-06-13T23:00:00Z** — **`/sprint-plan`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260613-01`, `fresh_context_marker=tl-S0087-US0097-sprint-plan-20260613T230000Z-fresh`, `runtime_proof_id=rp-auto-20260613-01-sprint-plan-tech-lead-20260613T230000Z-S0087-US0097`, `proof_hash=839f15ffcaa54f7dc8066904b7162fd223d63af27afac30910699532633118cc`). Sprint **`S0087`** created; **AC-1..AC-10** surjective via **T-001..T-011** (11 architecture seeds; `task_count=11`, `within_limit=true`). Story **`US-0097`** remains **OPEN** (**US-0045**). **Do not implement** in this phase. Next phase is **`/plan-verify`** (fresh **qa**).

### Sprint anchor

- **Sprint overview**: `sprints/S0087/sprint.md`
- **Tasks**: `sprints/S0087/tasks.md` (**T-001..T-011**)
- **Plan-verify**: `sprints/S0087/plan-verify.json` (**PENDING**)
- **Architecture**: `docs/engineering/architecture.md` `# US-0097`
- **Decision**: `decisions/DEC-0083.md`
- **Research**: `docs/engineering/research.md` `R-0084`

### AC ↔ Task map (locked for /plan-verify and /execute)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1 | Remove root README from installer `[install_paths]` |
| T-002 | AC-2 | Migration M1–M5 + sentinels S1–S5 |
| T-003 | AC-3, AC-5 | Project README bootstrap scaffold + vision sourcing |
| T-004 | AC-3, AC-4, AC-8 | Execute step 23 (23a/23b/23c) |
| T-005 | AC-4, AC-7 | Release step 3g + gate order 3f→3g→4 |
| T-006 | AC-7 | Scratchpad PROJECT_README_ENFORCE + FRAMEWORK_KIT_REPO |
| T-007 | AC-5, AC-6 | Reframe US-0091 validator to its_magic/ paths |
| T-008 | AC-6 | validate_project_readme_coverage.py + --report schema v1 |
| T-009 | AC-9 | Eight test_us0097_* contract subtests |
| T-010 | AC-9 | PROJECT_README_PAIRS parity + harness §26V |
| T-011 | AC-10 | Runbook operator recipes |

### Recommended /execute ordering

1. **T-001** → **T-002** (Tranche A — installer + migration)
2. **T-003** (Tranche B — bootstrap scaffold)
3. **T-004** → **T-005** → **T-006** (Tranche C — phase wiring + scratchpad)
4. **T-007** → **T-008** (Tranche D — validators)
5. **T-009** → **T-010** (contract tests + parity — after docs/scripts)
6. **T-011** (runbook recipes — last)

### Scope guards for `/execute`

- **Do not** remove **`its_magic/README.md`** from framework install payload.
- **Do not** break release step **3f** (framework **US-0091** gate) — **`test_us0097_us0091_regression_guard`** mandatory.
- **Do not** conflate project and framework validators.
- **Do not** overwrite operator-authored root when **S5** detected.
- **Do not** set **`FRAMEWORK_KIT_REPO=1`** as consumer default.

### Post-edit gates (from sprint.md)

1. `pytest -k us0097 tests/auto_command_contract_test.py`
2. `python scripts/validate_project_readme_coverage.py --self-test`
3. `python scripts/check_intake_template_parity.py --scope=project-readme`

### Next

- **`/plan-verify`** (fresh **qa**) for **`S0087`** / **`US-0097`**

---

## Sprint Plan — **S0086** / **US-0096** — post-**`/plan-verify`** → **`/execute`** (**dev**)

> **2026-06-13T06:00:00Z** — **`/plan-verify`** **PASS** in fresh **qa** context (`orchestrator_run_id=auto-20260612-01`, `fresh_context_marker=qa-S0086-US0096-plan-verify-20260613T060000Z-fresh`, `runtime_proof_id=rp-auto-20260612-01-plan-verify-qa-20260613T060000Z-S0086-US0096`, `proof_hash=58898711bf0552eb3680e983929048198e250397b166b81985b46fc94dc11eb9`). **AC-1..AC-12** surjective via **T-001..T-012**; task-seed bijection confirmed; **`gates_failed=[]`**. Story **`US-0096`** remains **OPEN** (**US-0045**). Next phase is **`/execute`** (fresh **dev**).

> **2026-06-13T05:00:00Z** — **`/sprint-plan`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260612-01`, `fresh_context_marker=tl-S0086-US0096-sprint-plan-20260613T050000Z-fresh`, `runtime_proof_id=rp-auto-20260612-01-sprint-plan-tech-lead-20260613T050000Z-S0086-US0096`, `proof_hash=adcb3764f037aae8cb35a9616bf588542e47666d4e5dddaea61a96d1181c1bd2`). Sprint **`S0086`** created; **AC-1..AC-12** surjective via **T-001..T-012** (12 architecture seeds; `task_count=12`, `within_limit=true` at threshold).

### Sprint anchor

- **Sprint overview**: `sprints/S0086/sprint.md`
- **Tasks**: `sprints/S0086/tasks.md` (**T-001..T-012**)
- **Plan-verify**: `sprints/S0086/plan-verify.json` (**PASS**)
- **Architecture**: `docs/engineering/architecture.md` `# US-0096`
- **Decision**: `decisions/DEC-0082.md`
- **Research**: `docs/engineering/research.md` `R-0082`

### AC ↔ Task map (locked for /execute)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1 | DELIVERY_MODE + LEAN_* scratchpad keys + non-substitution |
| T-002 | AC-3 | Tranche A universal wins |
| T-003 | AC-7, AC-2 | Mode-scoped resolver step 0 + standard baseline guard |
| T-004 | AC-4 | ultra_lean macro-phases + build+verify |
| T-005 | AC-5 | pack.json schema v1 + pack_json_validate.py |
| T-006 | AC-5 | active-context.md template + rollover + non-triad |
| T-007 | AC-6 | mega_quick routing + seven MEGA_QUICK_* codes |
| T-008 | AC-8 | AUTO_DELIVERY_ROUTING + backlog delivery_mode field |
| T-009 | AC-9 | Quality floor checklist + LEAN_MEMORY_* gates |
| T-010 | AC-10 | Eight test_us0096_* contract subtests |
| T-011 | AC-10 | US0096_PAIRS parity + harness §26Q |
| T-012 | AC-11, AC-12 | Runbook operator recipes + delivery_mode run-class |

### Recommended /execute ordering

1. **T-001** → **T-002** (Tranche A foundation)
2. **T-003** → **T-004** (resolver + ultra_lean docs)
3. **T-005** → **T-006** (layered memory — gate Tranche B)
4. **T-007** → **T-008** (mega_quick + backlog routing)
5. **T-009** (quality floor)
6. **T-010** → **T-011** (contract tests + parity — after docs)
7. **T-012** (runbook recipes + token evidence — last)

### Scope guards for `/execute`

- **Do not** weaken **`test_us0095_*`** or **`test_bug0012_*`** under **`DELIVERY_MODE=standard`**.
- **Do not** add **`active-context.md`** to triad enforcement (**DEC-0054**).
- **Do not** allow non-standard **`AUTO_PHASE_*`** without **`PHASE_POLICY_CONFLICT`**.
- **Do not** break **DEC-0080** / **DEC-0081** native-chain spawn-only semantics.
- Run **`test_us0096_standard_mode_baseline_markers_preserved`** early after T-003.

### Post-edit gates (from sprint.md)

1. `pytest -k us0096 tests/auto_command_contract_test.py`
2. `pytest -k us0095 tests/auto_command_contract_test.py`
3. `pytest -k bug0012 tests/auto_command_contract_test.py`
4. `python scripts/check_intake_template_parity.py --scope=us-0096`

### Next

- **`/plan-verify`** (fresh **qa**) for **`S0086`** / **`US-0096`**

---

## Architecture — **US-0096** — post-**`/architecture`** → **`/sprint-plan`** (**tech-lead**)

> **2026-06-13T04:00:00Z** — **`/architecture`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260612-01`, `fresh_context_marker=tl-US0096-architecture-20260613T040000Z-fresh`, `runtime_proof_id=rp-auto-20260612-01-architecture-tech-lead-20260613T040000Z-US0096`, `proof_hash=1c530587d7b202c9a3ac979f71a980ff2533e8ff07e895d558b49cf851a0e8d8`). Binding **`DEC-0082`** authored; **`# US-0096`** appended; **12** atomic task seeds (`task_count=12`, `within_limit=true` at threshold). Story **`US-0096`** remains **OPEN** (**US-0045**). **Do not implement** in this phase. Next phase is **`/sprint-plan`** (fresh **tech-lead**).

### Architecture anchor

- **Architecture**: `docs/engineering/architecture.md` `# US-0096`
- **Decision**: `decisions/DEC-0082.md`
- **Research**: `docs/engineering/research.md` `R-0082`

### AC ↔ Seed map (locked for sprint-plan)

| Seed | AC | Summary |
|------|-----|---------|
| 1 | AC-1 | **`DELIVERY_MODE`** + **`LEAN_*`** scratchpad + non-substitution |
| 2 | AC-3 | Tranche A universal wins (caps, narrow-read, delta handoffs, touch-graph) |
| 3 | AC-7, AC-2 | Mode-scoped resolver step 0 + standard reinstatement guard |
| 4 | AC-4 | **`ultra_lean`** macro-phases + **`build+verify`** |
| 5 | AC-5 | **`pack.json`** schema + **`pack_json_validate.py`** |
| 6 | AC-5 | **`active-context.md`** template + rollover + non-triad |
| 7 | AC-6 | **`mega_quick`** routing + seven eligibility codes |
| 8 | AC-8 | **`AUTO_DELIVERY_ROUTING`** + backlog **`delivery_mode`** field |
| 9 | AC-9 | Quality floor runbook + **`LEAN_MEMORY_*`** gates |
| 10 | AC-10 | Eight **`test_us0096_*`** contract subtests |
| 11 | AC-10 | **`US0096_PAIRS`** parity + harness **§26Q** |
| 12 | AC-11, AC-12 | Runbook operator recipes + **`delivery_mode`** run-class extension |

### Recommended /sprint-plan ordering

1. Tranche A seeds (1–2) first — always-on wins
2. Resolver + standard guard (3) before lean modes
3. **`ultra_lean`** (4–6) before **`mega_quick`** (7)
4. Routing (8), quality (9), tests (10–11), runbook/evidence (12)

### Scope guards for `/sprint-plan` and `/execute`

- **Do not** weaken **`test_us0095_*`** or **`test_bug0012_*`** — additive **`test_us0096_*`** only.
- **Do not** make **`active-context.md`** a triad member — **DEC-0054** unchanged.
- **Do not** allow mid-story **`DELIVERY_MODE`** switch without fail-closed **`DELIVERY_MODE_SWITCH_MID_STORY`**.
- **Do not** break **DEC-0080** native chain / drain-advance semantics.
- Execute Tranche A before enabling **`ultra_lean`** / **`mega_quick`** in docs defaults.

### Next

- **`/sprint-plan`** (fresh **tech-lead**) for **`US-0096`**

---

## Sprint Plan — **S0085** / **BUG-0012** — post-**`/sprint-plan`** → **`/plan-verify`** (**qa**)

> **2026-06-12T22:30:00Z** — **`/sprint-plan`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260612-01`, `fresh_context_marker=tl-S0085-BUG0012-sprint-plan-20260612T223000Z-fresh`, `runtime_proof_id=rp-auto-20260612-01-sprint-plan-tech-lead-20260612T223000Z-S0085-BUG0012`, `proof_hash=5810e6f73ca2f2803bfe81724e7edc8ac71eebe476921729f2b5ee6b0cb0b172`). Sprint **`S0085`** created; **AC-1..AC-8** surjective via **T-001..T-008** (8 architecture seeds; `task_count=8`, `within_limit=true`). Bug **`BUG-0012`** remains **OPEN** (**US-0045**). **Do not implement** in this phase. Next phase is **`/plan-verify`** (fresh **qa**).

### Sprint anchor

- **Sprint overview**: `sprints/S0085/sprint.md`
- **Atomic tasks**: `sprints/S0085/tasks.md` (T-001..T-008)
- **Plan-verify (qa)**: `sprints/S0085/plan-verify.json` (`status=PENDING`)
- **Summary**: `sprints/S0085/summary.md`
- **Architecture**: `docs/engineering/architecture.md` `# BUG-0012`
- **Decision**: `decisions/DEC-0081.md`
- **Research**: `docs/engineering/research.md` `R-0083`

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1 | Orchestrator MUST Task-spawn mandate + actor distinction |
| T-002 | AC-2 | Native chain supersedes Option B; scope US-0088 fallback |
| T-003 | AC-3, AC-4 | Drain-advance step 7 no-stop + `drain_advance_action` |
| T-004 | AC-4, AC-7 | `native_chain_continuing` + resume_brief spawn pairing |
| T-005 | AC-5 | Four `test_bug0012_*` contract subtests |
| T-006 | AC-6 | Forbidden-prose negative grep |
| T-007 | AC-8 | Runbook § BUG-0012 regression verify E2E |
| T-008 | AC-8 | Template parity `--scope=bug-0012` + DEC linkage assert |

### Recommended /execute ordering

1. T-001 → T-002 → T-003 → T-004 → T-006 → T-005 → T-007 → T-008

### Scope guards for `/plan-verify` and `/execute`

- **Do not** weaken spawn-only (**BUG-0006**) or **DEC-0078** hard gates.
- **Do not** remove **`auto_outer_driver.py`** — optional fallback only.
- **Do not** break any seven **`test_us0095_*`** subtests — additive **`test_bug0012_*`** layer only.
- **Do not** fabricate `state.md` runtime checkpoints during doc edits.

### Next

- **`/plan-verify`** (fresh **qa**) for **`S0085`** / **`BUG-0012`**

---

## Sprint Plan — **S0084** / **US-0095** — post-**`/sprint-plan`** → **`/plan-verify`** (**qa**)

> **2026-06-07T20:00:00Z** — **`/sprint-plan`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260607-02`, `fresh_context_marker=tl-S0084-US0095-sprint-plan-20260607T200000Z-fresh`, `runtime_proof_id=rp-auto-20260607-02-sprint-plan-tech-lead-20260607T200000Z-S0084-US0095`, `proof_hash=88e67cca34c4a7ad46f74c61c04c2c29a7c80a9558851945817cce83c5780edf`). Sprint **`S0084`** created; **AC-1..AC-10 ↔ T-001..T-010** strict bijection; `task_count=10`, `within_limit=true`. Story **`US-0095`** remains **OPEN** (**US-0045**). **Do not implement** in this phase. Next phase is **`/plan-verify`** (fresh **qa**).

### Sprint anchor

- **Sprint overview**: `sprints/S0084/sprint.md`
- **Atomic tasks**: `sprints/S0084/tasks.md` (T-001..T-010)
- **Plan-verify (qa)**: `sprints/S0084/plan-verify.json` (`status=PENDING`)
- **Architecture**: `docs/engineering/architecture.md` `# US-0095`
- **Decision**: `decisions/DEC-0080.md`
- **Research**: `docs/engineering/research.md` `R-0081`

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1 | Native in-chat auto-chain § + reference Step 5 IDE-primary |
| T-002 | AC-2 | 7-step IDE drain-advance algorithm + literals |
| T-003 | AC-3 | Spawn-only invariants + BUG-0006 regression guard |
| T-004 | AC-4 | Stop matrix hard gates unchanged |
| T-005 | AC-5 | Runbook + README outer-driver demotion |
| T-006 | AC-6 | AUTO_QUIET suppression table + forbidden patterns |
| T-007 | AC-7 | DEC-0069 pairing mandate before continuation |
| T-008 | AC-8 | Six `test_us0095_*` contract subtests |
| T-009 | AC-9 | Template parity (8-surface inventory) |
| T-010 | AC-10 | Cap/ledger breadcrumbs + security deny-list |

### Recommended /execute ordering

1. T-001 → T-003 → T-002 → T-004 → T-007 → T-006 → T-010 → T-005 → T-008 → T-009

### Scope guards for `/plan-verify` and `/execute`

- **Do not** weaken spawn-only (**BUG-0006**) or isolation/strict-proof gates.
- **Do not** delete **`auto_outer_driver.py`** — demote to fallback only.
- **Do not** mandate outer driver for IDE **`full_autonomy`** primary path.
- **Do not** fabricate `state.md` checkpoints during doc edits (T-010 comments only).

### Next

- **`/plan-verify`** (fresh **qa**) for **`S0084`** / **`US-0095`**

---

## Architecture — **US-0095** — post-**`/architecture`** → **`/sprint-plan`** (**tech-lead**)

> **2026-06-07T19:30:00Z** — **`/architecture`** **PASS** (`orchestrator_run_id=auto-20260607-02`, `fresh_context_marker=tl-US0095-architecture-20260607T193000Z-fresh`, `runtime_proof_id=rp-auto-20260607-02-architecture-tech-lead-20260607T193000Z-US0095`, `proof_hash=ff1b750771d57ce7f753d85f6536b3a3aca19c2be595ddbe059c04a9b44626ad`). **`DEC-0080`** + **`# US-0095`** locked. Story **`US-0095`** remains **OPEN** (**US-0045**). **Do not execute** in this phase.

### Locked contracts

| Area | Lock |
|------|------|
| Native chain | Foreground sequential Task loop; same `/auto` orchestrator session |
| Drain-advance | 7-step algorithm; `drain-advance-without-pause`; immediate in-chat spawn |
| Caps/ledger | Unified with **DEC-0078**; `phase_respawn`, `native_chain_continue`, `drain_advance` |
| Fallback | IDE primary; outer driver optional; **`NATIVE_CHAIN_UNAVAILABLE`** fail-closed |
| Spawn-only | **BUG-0006** unchanged — orchestrator schedules only |
| Messaging | **`AUTO_QUIET`** table; forbidden mandatory outer-driver patterns |

### Atomic task seeds

10 seeds in **`docs/engineering/architecture.md`** **`# US-0095`** § Atomic task seeds (AC-1..AC-10 via seeds 1..10).

### Evidence refs

- `decisions/DEC-0080.md`
- `docs/engineering/architecture.md` (**`# US-0095`**)
- `docs/engineering/research.md` (**`R-0081`**)
- `docs/product/backlog.md` (`## US-0095` `architecture_notes`)

### Next

- **`/sprint-plan`** (fresh **tech-lead**) for **`US-0095`**

---

## Sprint Plan — **S0083** / **US-0094** — post-**`/sprint-plan`** → **`/plan-verify`** (**qa**)

> **2026-06-07T13:30:00Z** — **`/sprint-plan`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260607-01`, `fresh_context_marker=tl-S0083-US0094-sprint-plan-20260607T133000Z-fresh`, `runtime_proof_id=rp-auto-20260607-01-sprint-plan-tech-lead-20260607T133000Z-S0083-US0094`, `proof_hash=db8ff920147b25d12d822d32ee21b3695c12ffe0139975502d2daa0822d23efa`). Sprint **`S0083`** created; **AC-1..AC-10 ↔ T-001..T-010** strict bijection; `task_count=10`, `within_limit=true`. Story **`US-0094`** remains **OPEN** (**US-0045**). **Do not edit README.md** in this phase. Next phase is **`/plan-verify`** (fresh **qa**).

### Sprint anchor

- **Sprint overview**: `sprints/S0083/sprint.md`
- **Atomic tasks**: `sprints/S0083/tasks.md` (T-001..T-010)
- **Plan-verify (qa)**: `sprints/S0083/plan-verify.json` (`status=PENDING`)
- **Summary**: `sprints/S0083/summary.md`
- **Architecture**: `docs/engineering/architecture.md` `# US-0094`
- **Research**: `docs/engineering/research.md` `R-0080`

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1 | Replace pre-`## Features` intro (3 ¶, word budget) |
| T-002 | AC-2 | Four pillar `###` sections with id-free teasers |
| T-003 | AC-3 | Deep body sections preserved |
| T-004 | AC-4 | Coverage `--report` → zero gaps |
| T-005 | AC-5 | Byte-copy root → template + identity check |
| T-006 | AC-6 | `validate_doc_profile.py` pass |
| T-007 | AC-7 | `check-user-visible-metadata.py` pass |
| T-008 | AC-8 | Full-autonomy placement audit |
| T-009 | AC-9 | Regression contract tests green |
| T-010 | AC-10 | DEV shard unchanged |

### Recommended /execute ordering

1. T-001 → T-002 → T-003 → T-008 → T-004 → T-006 → T-007 → T-005 → T-009 → T-010

### Scope guards for `/plan-verify` and `/execute`

- **Do not** relocate catalog blocks across H2 affinity homes.
- **Do not** add new `##` H2 literals or amend **DEC-0074**.
- **Do not** edit `docs/developer/README.md` body.
- **Single-source** edit on root `README.md`; byte-copy to `template/` only after gates pass.
- **Commit** root + template README atomically.

### Next

- **`/plan-verify`** (fresh **qa**) for **`S0083`** / **`US-0094`**

---

## Architecture — **US-0094** — post-**`/architecture`** → **`/sprint-plan`** (**tech-lead**)

> **2026-06-07T13:00:00Z** — **`/architecture`** **PASS** (`orchestrator_run_id=auto-20260607-01`, `fresh_context_marker=tl-US0094-architecture-20260607T130000Z-fresh`). **`# US-0094`** appended to **`docs/engineering/architecture.md`**. Story **`US-0094`** remains **OPEN** (**US-0045**). **Do not edit README.md** in this phase.

### Locked contracts

| Area | Lock |
|------|------|
| Intro | 3 ¶ before `## Features`; 120–210 words soft / 240 hard max |
| Pillars | 4 `###` under Features — exact discovery titles |
| Catalog | 3 US-0091 blocks — affinity-home H2s immutable |
| DEC | **None new** — **`DEC-0074`** not amended |
| Parity | Single-source edit → byte-copy template |

### Atomic task seeds

10 seeds in **`docs/engineering/architecture.md`** **`# US-0094`** § Atomic task seeds (AC-1..AC-10 ↔ seeds 1..10).

### Evidence refs

- `docs/engineering/architecture.md` (**`# US-0094`**)
- `docs/engineering/research.md` (**`R-0080`**)
- `docs/product/backlog.md` (`## US-0094` `architecture_notes`)
- `handoffs/po_to_tl.md` (Orchestrated architecture handoff — US-0094)

### Next

- **`/sprint-plan`** (fresh **tech-lead**) for **`US-0094`**

---

## Sprint Plan — **S0082** / **US-0093** — post-**`/sprint-plan`** → **`/plan-verify`** (**qa**)

> **2026-06-07T00:00:00Z** — **`/sprint-plan`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260606-04`, `fresh_context_marker=tl-S0082-US0093-sprint-plan-20260607T000000Z-fresh`, `runtime_proof_id=rp-auto-20260606-04-sprint-plan-tech-lead-20260607T000000Z-S0082-US0093`, `proof_hash=b1511e92b1cd8e38b3b91fd3d8e685e8736712b1883d3cfd748f2196c6d744c0`). Sprint **`S0082`** created; **AC-1..AC-10 ↔ T-001..T-010** strict bijection; `task_count=10`, `within_limit=true`. Story **`US-0093`** remains **OPEN** (**US-0045**). Next phase is **`/plan-verify`** (fresh **qa**).

### Sprint anchor

- **Sprint overview**: `sprints/S0082/sprint.md`
- **Atomic tasks**: `sprints/S0082/tasks.md` (T-001..T-010)
- **Plan-verify (qa)**: `sprints/S0082/plan-verify.json` (`status=PENDING`)
- **Summary**: `sprints/S0082/summary.md`
- **Binding decision**: `decisions/DEC-0079.md` (§1–§11)
- **Architecture**: `docs/engineering/architecture.md` `# US-0093`
- **Research**: `docs/engineering/research.md` `R-0079`

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1 | Scratchpad `UAT_BROWSER_PROBE_MODE` + poll/fallback keys |
| T-002 | AC-2 | Browser two-tier execution + MCP command excerpts + fallback |
| T-003 | AC-3 | `manual_operator` verb routing |
| T-004 | AC-4 | `process_health` / `cli_smoke` stub completion |
| T-005 | AC-5 | `browser_evidence_refs` evidence schema + `--merge-result` |
| T-006 | AC-6 | `UAT_BROWSER_*` reason codes + `--self-test` |
| T-007 | AC-7 | Security deny-list unchanged |
| T-008 | AC-8 | Runbook + auto-orchestration-reference operator recipe |
| T-009 | AC-9 | Contract tests `test_us0093_*` + harness §32 |
| T-010 | AC-10 | Template parity `--scope=us-0093` + linkage assert |

### Recommended /execute ordering

1. T-001 → T-003 ∥ T-004 → T-002 → T-005 → T-006 → T-007 → T-008 → T-009 → T-010

### Scope guards for `/plan-verify` and `/execute`

- **Do not re-open** DEC-0079 §§1–11.
- **Do not** invoke browser MCP from **`uat_probe_lib.py`** (**BUG-0006** spawn-only).
- **Do not** fabricate **`browser_evidence_refs`** or silent PASS in **`cursor`** mode.
- **Do not** auto-read `.env`, fill credentials, or mutate intake evidence.
- **Commit** active + `template/` pairs atomically for parity rows.

### Next

- **`/plan-verify`** (fresh **qa**) for **`S0082`** / **`US-0093`**

---

## Sprint Plan — **S0081** / **US-0092** — post-**`/plan-verify`** → **`/execute`** (**dev**)

> **2026-06-06T20:15:00Z** — **`/plan-verify`** **PASS** in fresh **qa** context (`orchestrator_run_id=auto-20260606-03`, `fresh_context_marker=qa-S0081-US0092-plan-verify-20260606T201500Z-fresh`, `runtime_proof_id=rp-auto-20260606-03-plan-verify-qa-20260606T201500Z-S0081-US0092`, `proof_hash=6ce05a35c16e560e34c9a19c73297df5a731c4832a3f1aef83b0d41770664fb4`). **AC-1..AC-10 ↔ T-001..T-010** strict bijection verified; `sprints/S0081/plan-verify.json` **PASS**. Story **`US-0092`** remains **OPEN** (**US-0045**). Next phase is **`/execute`** (fresh **dev**).

> **2026-06-06T20:00:00Z** — **`/sprint-plan`** **PASS** in fresh **tech-lead** context (`fresh_context_marker=tl-S0081-US0092-sprint-plan-20260606T200000Z-fresh`, `runtime_proof_id=rp-auto-20260606-03-sprint-plan-tech-lead-20260606T200000Z-S0081-US0092`, `proof_hash=fdc8e72253d4d875598e3dc24dadf245e0b9420cdfb6642f0886dde7fe8b8862`). Sprint **`S0081`** created; `task_count=10`, `within_limit=true`.

### Sprint anchor

- **Sprint overview**: `sprints/S0081/sprint.md`
- **Atomic tasks**: `sprints/S0081/tasks.md` (T-001..T-010)
- **Plan-verify (qa)**: `sprints/S0081/plan-verify.json` (`status=PASS`)
- **Summary**: `sprints/S0081/summary.md`
- **Binding decision**: `decisions/DEC-0078.md` (§1–§11)
- **Architecture**: `docs/engineering/architecture.md` `# US-0092`
- **Research**: `docs/engineering/research.md` `R-0078`

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1 | Scratchpad `full_autonomy` enum + new keys |
| T-002 | AC-2 | `scripts/auto_outer_driver.py` |
| T-003 | AC-3 | `uat_probe_lib.py` + verify-work/qa excerpts |
| T-004 | AC-4 | Block-retry ledger + caps |
| T-005 | AC-5 | Drain-without-pause + DEC-0069 refresh |
| T-006 | AC-6 | TOKEN_PROFILE orthography audit |
| T-007 | AC-7 | Stop matrix docs |
| T-008 | AC-8 | Contract tests |
| T-009 | AC-9 | Template parity + installer manifest |
| T-010 | AC-10 | Runbook + security deny-list |

### Recommended /execute ordering

1. T-001 → T-002 → T-003 (parallel OK) → T-004 → T-005 → T-006 ∥ T-007 → T-008 → T-009 → T-010

### Scope guards for `/plan-verify` and `/execute`

- **Do not re-open** DEC-0078 §§1–11.
- **Do not weaken** spawn-only (**BUG-0006**) or isolation/strict-proof gates.
- **Do not** auto-read `.env`, mutate intake evidence, or publish without `RELEASE_PUBLISH_MODE=auto`.
- **Commit** active + `template/` pairs atomically for parity rows.

### Next

- **`/execute`** (fresh **dev**) for **`S0081`** / **`US-0092`**

---

## Sprint Plan — **S0080** / **BUG-0011** — post-**`/plan-verify`** → **`/execute`** (**dev**)

> **2026-06-06T14:46:04Z** — **`/plan-verify`** **PASS** in fresh **qa** context (`orchestrator_run_id=auto-20260606-02`, `fresh_context_marker=qa-S0080-BUG0011-plan-verify-20260606T144604Z-fresh`, `runtime_proof_id=rp-auto-20260606-02-plan-verify-qa-20260606T144604Z-S0080-BUG0011`, `proof_hash=f33352078fc4ea47f49af1012b2956e5268598c672e41eadc0e3776d15d0c279`). **`sprints/S0080/plan-verify.json`** **`status=PASS`**; **AC-1..AC-8** surjective via **T-001..T-008** (12 gates green). Bug **`BUG-0011`** remains **OPEN** (**US-0045**). Next phase is **`/execute`** (fresh **dev**).

> **2026-06-06T16:43:29Z** — **`/sprint-plan`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260606-02`, `fresh_context_marker=tl-S0080-BUG0011-sprint-plan-20260606T164329Z-fresh`, `runtime_proof_id=rp-auto-20260606-02-sprint-plan-tech-lead-20260606T164329Z-S0080-BUG0011`, `proof_hash=5759c41dd84ae77757dac24fa0b8c675133326b666ebf74acf8e139451d4ca88`). Sprint **`S0080`** created; **AC-1..AC-8** surjective via **T-001..T-008**; `task_count=8`, `within_limit=true`.

### Sprint anchor

- **Sprint overview**: `sprints/S0080/sprint.md`
- **Atomic tasks**: `sprints/S0080/tasks.md` (T-001..T-008)
- **Plan-verify (qa)**: `sprints/S0080/plan-verify.json` (`status=PASS`)
- **Summary**: `sprints/S0080/summary.md`
- **QA findings**: `sprints/S0080/qa-findings.md` (plan-verify PASS)
- **Binding decision**: `decisions/DEC-0077.md` (§1–§10)
- **Architecture**: `docs/engineering/architecture.md` `# BUG-0011`
- **Research**: `docs/engineering/research.md` `R-0077`

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1, AC-2, AC-3, AC-4 | Voice section append to `caveman.mdc` (+ template mirror) |
| T-002 | AC-6 | Runbook `#### Voice compression levels` |
| T-003 | AC-5 | Nine `test_caveman_voice_*` subtests |
| T-004 | AC-5 | SHA baseline bump (`_CAVEMAN_RULE_BASELINE_SHA256`) |
| T-005 | AC-8 | Harness **§30A** |
| T-006 | AC-7 | `test_caveman_default_off_*` regression guard |
| T-007 | AC-8 | Operator voice UAT spot-check |
| T-008 | AC-1 | Architecture + DEC linkage assert |

### Recommended /execute ordering

1. T-001 → T-002 (parallel OK) → T-004 → T-003 → T-006 → T-005 → T-008 → T-007 (UAT docs at verify-work)

### Scope guards for `/execute`

- **Do not re-open** DEC-0077 §§1–10.
- **Do not modify** `test_caveman_default_off_*` assertion bodies.
- **Do not change** `CAVEMAN_COMPRESS_INPUT` / `scripts/caveman_compress_input.py`.
- **Do not duplicate** 9-zone literal list in voice section (pointer stub only).
- **Commit** active + `template/` pairs atomically for parity rows 1–2.

### Next

- **`/execute`** (fresh **dev**) for **`S0080`** / **`BUG-0011`**

---

## Sprint Plan — **S0080** / **BUG-0011** — post-**`/sprint-plan`** → **`/plan-verify`** (**qa**) — superseded

> **2026-06-06T16:43:29Z** — **`/sprint-plan`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260606-02`, `fresh_context_marker=tl-S0080-BUG0011-sprint-plan-20260606T164329Z-fresh`, `runtime_proof_id=rp-auto-20260606-02-sprint-plan-tech-lead-20260606T164329Z-S0080-BUG0011`, `proof_hash=5759c41dd84ae77757dac24fa0b8c675133326b666ebf74acf8e139451d4ca88`). Sprint **`S0080`** created; **AC-1..AC-8** surjective via **T-001..T-008**; `task_count=8`, `within_limit=true`. Bug **`BUG-0011`** remains **OPEN** (**US-0045**). Next phase is **`/plan-verify`** (fresh **qa**).

### Sprint anchor

- **Sprint overview**: `sprints/S0080/sprint.md`
- **Atomic tasks**: `sprints/S0080/tasks.md` (T-001..T-008)
- **Plan-verify (qa)**: `sprints/S0080/plan-verify.json` (`status=PENDING`)
- **Summary**: `sprints/S0080/summary.md`
- **Binding decision**: `decisions/DEC-0077.md` (§1–§10)
- **Architecture**: `docs/engineering/architecture.md` `# BUG-0011`
- **Research**: `docs/engineering/research.md` `R-0077`

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1, AC-2, AC-3, AC-4 | Voice section append to `caveman.mdc` (+ template mirror) |
| T-002 | AC-6 | Runbook `#### Voice compression levels` |
| T-003 | AC-5 | Nine `test_caveman_voice_*` subtests |
| T-004 | AC-5 | SHA baseline bump (`_CAVEMAN_RULE_BASELINE_SHA256`) |
| T-005 | AC-8 | Harness **§30A** |
| T-006 | AC-7 | `test_caveman_default_off_*` regression guard |
| T-007 | AC-8 | Operator voice UAT spot-check |
| T-008 | AC-1 | Architecture + DEC linkage assert |

### Scope guards for `/plan-verify` and `/execute`

- **Do not re-open** DEC-0077 §§1–10.
- **Do not modify** `test_caveman_default_off_*` assertion bodies.
- **Do not change** `CAVEMAN_COMPRESS_INPUT` / `scripts/caveman_compress_input.py`.
- **Do not duplicate** 9-zone literal list in voice section (pointer stub only).
- **Commit** active + `template/` pairs atomically for parity rows 1–2.

### Next

- **`/plan-verify`** (fresh **qa**) for **`S0080`** / **`BUG-0011`**

---

## Sprint Plan — **S0079** / **BUG-0010** — post-**`/plan-verify`** → **`/execute`** (**dev**)

> **2026-06-06T14:26:51Z** — **`/plan-verify`** **PASS** in fresh **qa** context (`orchestrator_run_id=auto-20260606-02`, `fresh_context_marker=qa-S0079-BUG0010-plan-verify-20260606T142651Z-fresh`, `runtime_proof_id=rp-auto-20260606-02-plan-verify-qa-20260606T142651Z-S0079-BUG0010`, `proof_hash=3597c96a39105c8ffb3f6c7ce5e17901ac0d8a29cd64dc9086b95352cd377a9c`). **`sprints/S0079/plan-verify.json`** **`status=PASS`**; **AC-1..AC-8** surjective via **T-001..T-009** (12 gates green). Bug **`BUG-0010`** remains **OPEN** (**US-0045**). Next phase is **`/execute`** (fresh **dev**).

> **2026-06-06T17:00:00Z** — **`/sprint-plan`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260606-02`, `fresh_context_marker=tl-S0079-BUG0010-sprint-plan-20260606T170000Z-fresh`, `runtime_proof_id=rp-auto-20260606-02-sprint-plan-tech-lead-20260606T170000Z-S0079-BUG0010`, `proof_hash=2f11f1ef33664c971f80af8d98e89a9e6ef5c71d637761d1814edf1d0131edeb`). Sprint **`S0079`** created; **AC-1..AC-8** surjective via **T-001..T-009**; `task_count=9`, `within_limit=true`.

### Sprint anchor

- **Sprint overview**: `sprints/S0079/sprint.md`
- **Atomic tasks**: `sprints/S0079/tasks.md` (T-001..T-009)
- **Plan-verify (qa)**: `sprints/S0079/plan-verify.json` (`status=PASS`)
- **Summary**: `sprints/S0079/summary.md`
- **Binding decision**: `decisions/DEC-0076.md` (§1–§9)
- **Architecture**: `docs/engineering/architecture.md` `# BUG-0010`
- **Research**: `docs/engineering/research.md` `R-0076`

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1, AC-2, AC-3, AC-7 | Dual-level archiver + H1-wins merge (+ template mirror) |
| T-002 | AC-4 | `count_h2_story_headings` + `check_arch_heading_policy` + CLI |
| T-003 | AC-1, AC-2, AC-3, AC-6 | Extended `--self-test` fixture classes |
| T-004 | AC-4, AC-5 | Architecture command H1 mandate + policy step |
| T-005 | AC-5, AC-6 | Contract tests `test_bug0010_*` |
| T-006 | AC-6 | Harness **§29A** |
| T-007 | AC-1, AC-3 | Optional `triad_arch_headings/` fixtures |
| T-008 | AC-8 | Runbook legacy `## US-` remediation blurb |
| T-009 | AC-5 | Architecture + DEC linkage assert |

### Scope guards for `/plan-verify` and `/execute`

- **Do not re-open** DEC-0076 §§1–9.
- **Do not add** standalone `validate_architecture_headings.py`.
- **Do not static-fail** on grandfathered `## US-` sections.
- **Do not add** new `check_intake_template_parity.py` scope.
- **Commit** active + `template/` pairs atomically for parity rows 1–3.

### Next

- **`/execute`** (fresh **dev**) for **`S0079`** / **`BUG-0010`**

---

## TL → Dev Handoff — **BUG-0010** (post-architecture) → **`/sprint-plan`** — **superseded** by **S0079** sprint plan above

> **2026-06-06T14:22:42Z** — **`/architecture`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260606-02`, `fresh_context_marker=tl-BUG0010-architecture-20260606T142242Z-fresh`, `runtime_proof_id=rp-auto-20260606-02-architecture-tl-20260606T142242Z-BUG0010`, `proof_hash=a3a709c179134f8ac44c89cd05f5b99e132b72f5c06b8224f027131853b48f42`). Binding decision **`DEC-0076`** authored; **`docs/engineering/architecture.md`** **`# BUG-0010`** appended. Bug **`BUG-0010`** remains **OPEN** (**US-0045**). No execution started — next phase is **`/sprint-plan`** (fresh **tech-lead**).

### Architecture anchor

- **Binding decision**: `decisions/DEC-0076.md` (§1–§9)
- **Architecture**: `docs/engineering/architecture.md` **`# BUG-0010`**
- **Research**: `docs/engineering/research.md` **`R-0076`**
- **State checkpoint**: `docs/engineering/state.md` — **Architecture checkpoint (2026-06-06) — BUG-0010 / auto-20260606-02**

### Locked decisions (DEC-0076 summary)

1. **Dual-level archiver** — `STORY_HEADING_H1` + `STORY_HEADING_H2`; H1-wins precedence filter in `split_arch_stories`.
2. **Forward enforcement** — diff-gated `count_h2_story_headings` / `check_arch_heading_policy`; hard fail on `ARCH_STORY_HEADING_LEVEL_INVALID`.
3. **In-place extension** — `enforce-triad-hot-surface.py` only (no new validator script); active + `template/` byte-identical.
4. **Command contract** — `.cursor/commands/architecture.md` mandates H1 `# US-xxxx` / `# BUG-xxxx`; baseline capture in triad step 9.
5. **Regression** — extended `--self-test` + `test_bug0010_*` + harness **§29A**.
6. **Template parity** — script + architecture command + runbook triad subsection (no new parity scope).
7. **Operator docs** — legacy `## US-` rollover note + optional `##`→`#` remediation (DEC-0076 §7).

### Atomic task seeds (9; `/sprint-plan` converts to T-xxx)

See **`docs/engineering/architecture.md`** **`# BUG-0010`** § Atomic task seeds.

### Scope guards for `/sprint-plan`

- **Do not re-open** DEC-0076 §§1–9.
- **Do not add** standalone `validate_architecture_headings.py`.
- **Do not static-fail** on pre-existing `## US-` sections (diff-gated only).
- **Do not add** `check_intake_template_parity.py` new scope.
- **Do not advance** backlog status (**OPEN** until `/release`).

### Next

- **`/sprint-plan`** (fresh **tech-lead**) for **`BUG-0010`**

---

## Sprint Plan — **S0078** / **BUG-0009** — post-**`/plan-verify`** → **`/execute`** (**dev**)

> **2026-06-06T14:03:00Z** — **`/plan-verify`** **PASS** in fresh **qa** context (`orchestrator_run_id=auto-20260606-02`, `fresh_context_marker=qa-S0078-BUG0009-plan-verify-20260606T140300Z-fresh`, `runtime_proof_id=rp-auto-20260606-02-plan-verify-qa-20260606T140300Z-S0078-BUG0009`, `proof_hash=2b11ce38142dc8608181ba9fef4ccd8c2b3da76002c4dfa90734f1fd33cea379`). **`sprints/S0078/plan-verify.json`** flipped **PENDING → PASS**; **AC-1..AC-8** surjective via **T-001..T-010** verified. Bug **`BUG-0009`** remains **OPEN** (**US-0045**). **`/execute`** unblocked — next phase is **`/execute`** (fresh **dev**).

### Sprint anchor

- **Sprint overview**: `sprints/S0078/sprint.md`
- **Atomic tasks**: `sprints/S0078/tasks.md` (T-001..T-010)
- **Plan-verify (qa)**: `sprints/S0078/plan-verify.json` (`status=PASS`)
- **Summary**: `sprints/S0078/summary.md`
- **Binding decision**: `decisions/DEC-0075.md` (§1–§10)
- **Architecture**: `docs/engineering/architecture.md` `# BUG-0009`
- **Research**: `docs/engineering/research.md` `R-0075`

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1, AC-4 | Template `ci.yml` downstream-safe + checks hardening |
| T-002 | AC-2, AC-4 | Active `ci.yml` checks hardening; five jobs preserved |
| T-003 | AC-5 | Template runbook empty `TEST_COMMAND:` |
| T-004 | AC-3, AC-7 | Drift guard lib + CLI (+ template mirrors) |
| T-005 | AC-3, AC-7 | Contract tests `test_bug0009_*` |
| T-006 | AC-3 | Harness **§28B** |
| T-007 | AC-6 | Install-completeness job-inventory smoke |
| T-008 | AC-6, AC-7 | Installer manifest + parity `--scope=downstream-ci-guard` |
| T-009 | AC-8 | Operator upgrade remediation docs |
| T-010 | AC-7 | Architecture + DEC linkage assert |

### Scope guards for `/execute` (after plan-verify PASS)

- **Do not re-open** DEC-0075 §§1–10.
- **Do not strip** packaging jobs from **active** CI.
- **Do not byte-match** template and active `ci.yml`.
- **Do not add** `--scope=ci-downstream` to parity script.
- **Commit** active + `template/` pairs atomically for parity rows.

### Next

- **`/execute`** (fresh **dev**) for **`S0078`** / **`BUG-0009`**

---

## TL → Dev Handoff — **BUG-0009** (post-architecture) → **`/sprint-plan`** — **superseded** by **S0078** sprint plan above

> **2026-06-06T16:00:00Z** — **`/architecture`** **PASS** in fresh **tech-lead** context (`orchestrator_run_id=auto-20260606-02`, `fresh_context_marker=tl-BUG0009-architecture-20260606T160000Z-fresh`, `runtime_proof_id=rp-auto-20260606-02-architecture-tl-20260606T160000Z-BUG0009`, `proof_hash=47027c0a605d7150e949cd8d6fc7ad3f30280aca4cbb0462427721e2a57b0805`). Binding decision **`DEC-0075`** authored; **`docs/engineering/architecture.md`** **`# BUG-0009`** appended. Bug **`BUG-0009`** remains **OPEN** (**US-0045**). No execution started — next phase is **`/sprint-plan`** (fresh **tech-lead**).

### Architecture anchor

- **Binding decision**: `decisions/DEC-0075.md` (§1–§10)
- **Architecture**: `docs/engineering/architecture.md` **`# BUG-0009`**
- **Research**: `docs/engineering/research.md` **`R-0075`**
- **State checkpoint**: `docs/engineering/state.md` — **Architecture checkpoint (2026-06-06) — BUG-0009 / auto-20260606-02**

### Locked decisions (DEC-0075 summary)

1. **CI split** — in-place job subtraction in `template/.github/workflows/ci.yml` (`checks`+`auto-fix` only); active retains five jobs.
2. **US-0017 negative parity** — intentional active ≠ template for `ci.yml` + template runbook `TEST_COMMAND:` line; **no** `--scope=ci-downstream` on parity script.
3. **Drift guard** — `check_downstream_ci_guard.py` + `downstream_ci_guard_lib.py` (lib split); harness **§28B**; contract tests `test_bug0009_*`.
4. **Forbidden patterns** + reason codes (`DOWNSTREAM_CI_FORBIDDEN_PATTERN`, `DOWNSTREAM_CI_JOB_LEAK`, `KIT_CI_PACKAGING_JOBS_MISSING`).
5. **checks green-by-default** — `no tests configured yet` summary; fail only on configured command failure.
6. **Empty template TEST_COMMAND** — US-0063 bootstrap preserved; active runbook keeps harness.
7. **Install smoke** — extend `installer_completeness_bug0003_test.py` job inventory (missing + upgrade).
8. **Operator docs** — upgrade remediation blurb (verbatim in DEC-0075 §9).

### Atomic task seeds (10; `/sprint-plan` converts to T-xxx)

See **`docs/engineering/architecture.md`** **`# BUG-0009`** § Atomic task seeds.

### Scope guards for `/sprint-plan`

- **Do not re-open** DEC-0075 §§1–10.
- **Do not strip** packaging jobs from **active** CI.
- **Do not byte-match** template and active `ci.yml`.
- **Do not add** `check_intake_template_parity.py --scope=ci-downstream`.
- **Do not advance** backlog status (**OPEN** until `/release`).

### Next

- **`/sprint-plan`** (fresh **tech-lead**) for **`BUG-0009`**

---

## Sprint Plan — **S0077** / **US-0091** — post-**`/plan-verify`** -> **`/execute`** (**dev**)

> **2026-06-06T15:30:00Z** — **`/plan-verify`** **PASS** in fresh **qa** context (`orchestrator_run_id=auto-20260606-01`, `fresh_context_marker=qa-S0077-US0091-plan-verify-20260606T153000Z-fresh`, `runtime_proof_id=rp-auto-20260606-01-plan-verify-qa-20260606T153000Z-S0077-US0091`, `proof_hash=ef8ac907c4334bd149ce026e0ca66da7ab8669173123368690ab0762201e078f`). **`sprints/S0077/plan-verify.json`** flipped **PENDING → PASS**; **AC-1..AC-10 ↔ T-001..T-010** strict bijection verified. Story **`US-0091`** remains **OPEN** (**US-0045**). **`/execute`** unblocked — next phase is **`/execute`** (fresh **dev**).

### Sprint anchor

- **Sprint overview**: `sprints/S0077/sprint.md`
- **Atomic tasks**: `sprints/S0077/tasks.md` (T-001..T-010)
- **Plan-verify (qa)**: `sprints/S0077/plan-verify.json` (`status=PASS`)
- **Summary**: `sprints/S0077/summary.md`
- **Binding decision**: `decisions/DEC-0074.md` (§1–§10)
- **Architecture**: `docs/engineering/architecture.md` **`# US-0091`** (active-only)
- **Research**: `docs/engineering/research.md` **`R-0074`**
- **State checkpoint**: `docs/engineering/state.md` — **Sprint-plan checkpoint (2026-06-06) — US-0091 / S0077 / `auto-20260606-01`**

### Task → AC → DEC-0074 § mapping (locked 1:1)

| Task | AC | Summary | DEC-0074 § | Parity |
|------|----|---------|------------|--------|
| T-001 | AC-1 | `readme_feature_coverage_lib.py` — predicate H1–H8 + backlog parser | §1, §2 | Positive (script lib) |
| T-002 | AC-2 | Audit report (`--audit-out`, gap artifact) | §5 | Active-only (audit json) |
| T-003 | AC-3 | Three-file backfill + `user_visible:` markers | §3 | Root↔template README |
| T-004 | AC-4 | `readme-section-affinity.json` + audience boundaries | §3, §4, §6 | Positive (manifest) |
| T-005 | AC-5 | `validate_readme_feature_coverage.py` + reason codes + `--self-test` | §5, §6 | Positive (CLI) |
| T-006 | AC-6 | Release step **3f** + runbook delta-vs-static | §7 | Positive (release.md + runbook) |
| T-007 | AC-7 | Idempotent `--report` + fixtures + harness **§27U** | §5 | Active-only |
| T-008 | AC-8 | US-0071 metadata hygiene on backfilled paths | §3 | Content review |
| T-009 | AC-9 | Parity script `--scope=readme-feature-coverage` + installer manifest | §9 | Positive |
| T-010 | AC-10 | `README_FEATURE_COVERAGE_ENFORCE` toggle + activation + DEC linkage assert | §8 | Scratchpad examples |

### Dev entry conditions (satisfied at `/plan-verify`)

- `/plan-verify` flipped `sprints/S0077/plan-verify.json` **`PENDING` → `PASS`** — **`/execute`** unblocked.
- Fresh **dev** context required (US-0048 / DEC-0029 isolation); strict runtime proof (DEC-0038) at `/execute` entry and exit.
- Dev MUST edit active + `template/` in the same commit for parity rows per DEC-0074 §9.
- Dev MUST NOT rewrite **US-0030** delta gate semantics.
- Dev MUST NOT invent new `USER_*` / `DEV_*` H2 literals (DEC-0059).
- Dev MUST flip `README_FEATURE_COVERAGE_ENFORCE` **0→1** only in T-010 after `--report` shows `coverage_missing: []`.
- Dev MUST NOT wire validator into `validate-and-push` (wrong lifecycle per DEC-0074 §7).

### Recommended /execute ordering

1. **T-001** → **T-004** → **T-005** → **T-002** → **T-003** → **T-008** → **T-006** → **T-009** → **T-007** → **T-010**

### Next

- **`/execute`** (fresh **dev**) for **`S0077`** / **US-0091**

---

## Sprint Plan — **S0076** / **US-0090** — post-**`/sprint-plan`** -> **`/plan-verify`** (**qa**)

> **2026-04-18T22:30:00Z** — **`/sprint-plan`** authored in fresh **tech-lead** context (`orchestrator_run_id=auto-20260418-01`, `fresh_context_marker=tl-US0090-sprint-plan-20260418T223000Z-fresh`, `runtime_proof_id=rp-auto-20260418-01-sprint-plan-tech-lead-20260418T223000Z-US0090`, `proof_hash=df27d039db0eb77e35ae140483338045c8a5a980f866b68ff683aa80bc3e8197`). Sprint **`S0076`** created; binding decision **`DEC-0073`** (composes on **`DEC-0072`** — forward-link, no rewrite). Task count **10 / 12** (`within_limit=true`; `SPRINT_AUTO_SPLIT` not triggered); AC coverage **AC-1..AC-8 all >=1 task** (no `PLAN_AC_COVERAGE_GAP`). Story **`US-0090`** remains **OPEN** (**US-0045**). No execution started yet — next phase is **`/plan-verify`** (fresh **qa**) -> then **`/execute`** (fresh **dev**).

### Sprint anchor

- **Sprint overview**: `sprints/S0076/sprint.md`
- **Atomic tasks**: `sprints/S0076/tasks.md` (T-001..T-010)
- **Plan-verify (qa)**: `sprints/S0076/plan-verify.json` (`status=PENDING`; flip to `PASS` at `/plan-verify`)
- **Summary stub**: `sprints/S0076/summary.md`
- **Binding decision**: `decisions/DEC-0073.md` (§1–§11)
- **Substrate decision (unchanged; forward-linked)**: `decisions/DEC-0072.md`
- **Architecture**: `docs/engineering/architecture.md` **`# US-0090`** (active-only per DEC-0072 §7 row 6 precedent)
- **Research**: `docs/engineering/research.md` **`R-0073`** (shared anchor; Q9–Q19 resolution pass 2026-04-18)
- **State checkpoint**: `docs/engineering/state.md` — **Sprint-plan checkpoint (2026-04-18) — US-0090 / S0076 / `auto-20260418-01`**

### Task → AC → DEC-0073 § mapping (locked)

| Task | AC | Summary | DEC-0073 § | Parity |
|------|----|---------|------------|--------|
| T-001 | AC-1..AC-5 | `scripts/caveman_compress_input.py` (+ `template/`) — CLI binary hosting gating / sidecar atomic-write ordering / deny eval / allow grammar / safe-mode algorithm / 9-code reason vocab | §2, §3, §4 + §4.1, §5 + §5.1, §6, §7, §8 | Positive (row 1) |
| T-002 | AC-5 | `docs/engineering/runbook.md` (+ `template/`) — Caveman input compression subsection (3-step operator flow + revert + three-axis reminder + `.cursorignore` operator-owned note) | §8, §9 row 2 | Positive (row 2) |
| T-003 | AC-7 | `docs/engineering/auto-orchestration-reference.md` (+ `template/`) — replace 2-sentence paragraph with 3-sentence three-axis non-substitution paragraph | §1, §9 row 3 | Positive (row 3) |
| T-004 | AC-2 | `.gitignore` anchor + `docs/.caveman-originals/.gitkeep` | §3 | Active-only |
| T-005 | AC-6, AC-8 | `tests/auto_command_contract_test.py` — new `test_caveman_compress_input_*` subtest class (11 assertions; includes seed-7 rule byte-identity R10 guard + deny_list_version drift guard; preserves existing `test_caveman_default_off_*` byte-unchanged) | §6, §7, §9 row 1 + negative-parity | Active-only |
| T-006 | AC-6 | `tests/fixtures/caveman_compress/` — 8 fixture classes (whitespace baseline / literal-region 9 zones / deny-list / scope violation / idempotency / mode-disabled / original-missing / flag-conflict) | §9 test-strategy block | Active-only |
| T-007 | AC-8 | `docs/engineering/context/installer-owned-paths.manifest` (+ `template/`) — add `scripts/caveman_compress_input.py` row | §10, §9 row 8 | Positive (row 8) |
| T-008 | AC-8 | `scripts/check_intake_template_parity.py` (+ `template/`) — new `--scope=caveman-compress` mode | §9 row 9 | Positive (row 9) |
| T-009 | AC-6, AC-8 | `tests/installer_completeness_bug0003_test.py` extension + `tests/run-tests.ps1` / `tests/run-tests.sh` new section (candidate §26S; lock during /execute) | §10 | Active-only |
| T-010 | AC-7 | Architecture `# US-0090` linkage assert-only subtest (no rewrite) | §1, §11 + DEC-0072 §7 row 6 | Active-only |

### Multi-AC task justification (Architecture Addendum-anchored)

- **T-001 → AC-1..AC-5**: Architecture Addendum seed #1 — "script is the CLI contract; five ACs land inside one binary by design" (gating / sidecar ordering / deny eval / allow grammar / CLI contract all implemented in `scripts/caveman_compress_input.py`).
- **T-005 → AC-6 + AC-8**: Addendum seeds 5 + 7 grouped — "same test file; grouping to minimize test-file churn while keeping rule byte-identity (R10) and deny-list version (§4.2) drift-detection guards in the same subtest class".
- **T-009 → AC-6 + AC-8**: Addendum seed 10 — "tests live under AC-6; installer / harness surface is AC-8 — single fixture + harness row lands both".

### Dev entry conditions (blocking; enforced by `/plan-verify`)

- `/plan-verify` must flip `sprints/S0076/plan-verify.json` `status` from **`PENDING`** → **`PASS`** before `/execute`.
- Fresh **dev** context required (US-0048 / DEC-0029 isolation); strict runtime proof (DEC-0038) at `/execute` entry and exit.
- Dev MUST edit active + `template/` in the same commit for parity rows 1 / 2 / 3 / 8 / 9 of DEC-0073 §9.
- Dev MUST NOT edit `.cursor/rules/caveman.mdc` or its `template/` counterpart (**negative parity; R10 byte-identity**). Baseline SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` preserved.
- Dev MUST NOT modify `test_caveman_default_off_*` subtests (DEC-0072 §6 row 6 invariant — additions only in `test_caveman_compress_input_*`).
- Dev MUST NOT add new reason codes, new CLI flags (no `--mode`, no `--purge-orphans`), new allow-list profiles, or new fixture classes beyond `DEC-0073` §9 without a subsequent DEC.
- Dev MUST NOT author / reference `npx skills add` anywhere (DEC-0072 §8 carried).
- Dev MUST NOT mutate `.cursorignore` (operator-owned per US-0085 / DEC-0071); script only reads it as optional overlay.
- Dev MUST NOT rewrite / edit `.cursor/scratchpad*` files — `CAVEMAN_COMPRESS_INPUT` and `CAVEMAN_FILE_SCOPE` already exist as reserved no-ops (DEC-0072 §3); activation is semantic (script reads them), not a byte change.

### File-by-file plan (ordering for /execute; pre-implementation gotchas)

Recommended implementation order (smallest blast radius first → highest leverage):

1. **T-004** — anchor the sidecar tree (`.gitignore` + `.gitkeep`) before any script can write sidecars. Cheap, unblocks T-001 acceptance test.
2. **T-001** — author the CLI binary (active + `template/` byte-identical). Largest single task; all downstream tests depend on its interface + reason codes. Gotcha: stdlib only (no `requests` / `pyyaml` / third-party); canonical JSON output (sort_keys=True, separators=(',',':')) for stable hashes in `--report`.
3. **T-007** — installer manifest row (active + `template/`). Unblocks T-009 fixture assertion.
4. **T-008** — parity-script `--scope=caveman-compress` mode (active + `template/`). Exercises T-001 output; gives a CI hook for positive-parity drift.
5. **T-002** — runbook subsection (active + `template/`). Locked strings (three-axis paragraph + four CLI flags).
6. **T-003** — reference-doc three-sentence paragraph (active + `template/`). Replace, do not append — the existing two-sentence paragraph is the target.
7. **T-006** — fixture tree (active-only). 8 classes; literal-region class needs 9 sub-fixtures (one per DEC-0072 §4 zone).
8. **T-005** — contract-test extension (active-only, tests do not mirror). Additions only; preserve S0075 subtest bodies byte-unchanged. Lock reason-code cardinality at 9 and rule SHA-256 at baseline.
9. **T-009** — install-completeness fixture + harness section (active-only). Pick next unassigned §26-series number (candidate §26S) during /execute by inspecting last-assigned in `run-tests.ps1` / `run-tests.sh`.
10. **T-010** — assert-only architecture linkage subtest (active-only). No edit of `docs/engineering/architecture.md`.

### Parity checklist at a glance (for dev + QA cross-check)

- **Positive (active + `template/` byte-identical)**: T-001 script, T-002 runbook append, T-003 reference paragraph, T-007 manifest row, T-008 parity script `--scope=caveman-compress` mode.
- **Active-only**: T-004 `.gitignore` / `.gitkeep`, T-005 contract-tests, T-006 fixtures, T-009 install-completeness + harness section, T-010 architecture linkage subtest, `docs/engineering/architecture.md` `# US-0090` (per DEC-0072 §7 row 6 precedent).
- **NEGATIVE (MUST NOT be edited)**: `.cursor/rules/caveman.mdc` (+ mirror) baseline SHA-256 preserved; `.cursor/scratchpad*` byte strings unchanged; `.cursor/skills/its-magic/SKILL.md` (+ mirror); `.cursorignore`; `decisions/DEC-0072.md` (forward-linked only); `decisions/DEC-0073.md` (already authored at /architecture); canonical artifacts in DEC-0073 §4.1 (script self-protects).

### DEC-0073 anchors

- **§1** three-axis non-substitution (T-003, T-002) — `TOKEN_PROFILE × CAVEMAN_MODE × CAVEMAN_COMPRESS_INPUT` orthogonal.
- **§2** activation gate (T-001) — `CAVEMAN_COMPRESS_INPUT=1` + non-empty `CAVEMAN_FILE_SCOPE` + explicit `--write`.
- **§3** sidecar originals (T-001, T-004) — parallel tree under `docs/.caveman-originals/<relative/path>/<file>`; `.gitignore` anchor + `.gitkeep`.
- **§4 + §4.1** deny-list source of truth (T-001) — layered precedence: baseline → `.gitignore` merge → `.cursorignore` overlay; deny always wins.
- **§5 + §5.1** allow-list grammar (T-001) — hybrid (named profile / raw globs) + frozen `docs-prose-only` v1 profile.
- **§6** safe-mode algorithm (T-001, T-006 class 5) — strictly idempotent; aggressive deferred.
- **§7** 9-code reason vocabulary (T-001, T-005 subtest #11) — 3 families (Gating / Scope / Integrity).
- **§8** CLI contract (T-001, T-002) — `--dry-run` default / `--write` / `--verify-originals` / `--report`; conflict fails closed `CAVEMAN_COMPRESS_FLAG_CONFLICT`.
- **§9** template parity inventory (T-001, T-002, T-003, T-005, T-006, T-007, T-008) — 8 positive rows + negative-parity set.
- **§10** installer / publish (T-007, T-008, T-009) — manifest entry + parity script extension + install-completeness fixture (R11 non-negotiable).
- **§11** non-goals / cross-cutting absorbed per-task (T-002 runbook, T-005 negative-parity subtests, T-001 deny-self-protection, T-010 architecture-linkage assert-only).

### Risks (locked at architecture; sprint-plan preserves)

- **R8** aggressive filler-word drift → neutralized (§6 Option B only; no `--mode` flag ships).
- **R9** reason-code proliferation → mitigated (9 codes in 3 families locked; T-005 subtest asserts cardinality).
- **R10** rule-subsection byte-identity → mitigated (no rule edit in v1; T-005 asserts baseline SHA-256).
- **R11** install-completeness omission (BUG-0003 class) → mitigated (T-007 + T-009 non-negotiable).
- **R-S1..R-S6** (sprint-phase risks — literal-region scan false negative, deny-list baseline drift, scratchpad byte-string preservation, `.cursorignore` boundary, existing subtest byte-unchanged) → per-task acceptance checks (see `sprints/S0076/sprint.md` § Additional sprint risks).

### Governance

- **DEC-0073**, **DEC-0072**, **R-0073**, architecture `# US-0090`.
- **US-0017**, **US-0045**, **US-0048 / DEC-0029**, **US-0056 / DEC-0038**, **US-0058 / DEC-0040**, **US-0069 / DEC-0051**, **US-0080 / DEC-0062**, **US-0088**, **US-0071**, **US-0085 / DEC-0071**, **US-0078 / DEC-0060**, **BUG-0001 / DEC-0063**, **BUG-0003 / DEC-0066**, **BUG-0006**.

---

## TL -> Dev Handoff — **US-0090** (post-architecture; pre-sprint) — post-**`/architecture`** -> **`/sprint-plan`** (**tech-lead**) — **superseded** by `## Sprint Plan — S0076 / US-0090` above

> **2026-04-18T22:00:00Z** — **`/architecture`** authored in fresh **tech-lead** context (`orchestrator_run_id=auto-20260418-01`, `fresh_context_marker=tl-US0090-architecture-20260418T220000Z-fresh`, `runtime_proof_id=rp-auto-20260418-01-architecture-tech-lead-20260418T220000Z-US0090`). Binding decision **`DEC-0073`** (composes on **`DEC-0072`** — forward-link, no rewrite); architecture section **`docs/engineering/architecture.md`** **`# US-0090`** appended. No sprint created yet — next phase is **`/sprint-plan`** (fresh **tech-lead**) -> then **`/plan-verify`** (fresh **qa**) -> then **`/execute`** (fresh **dev**). Story **`US-0090`** remains **OPEN** (**US-0045**). Dev entry is blocked until `/sprint-plan` authors `sprints/SXXXX/*` and `/plan-verify` moves the plan to **PASS**.

### Architecture anchors

- **Companion DEC**: `decisions/DEC-0073.md` (§1–§11 map 1:1 to the eleven research-phase architecture-asks)
- **Architecture section**: `docs/engineering/architecture.md` **`# US-0090`** (active-only per DEC-0072 §7 row 6 precedent)
- **Substrate DEC (unchanged)**: `decisions/DEC-0072.md` (binding for US-0089; forward-linked, not rewritten, by DEC-0073)
- **Research**: `docs/engineering/research.md` **`R-0073`** (shared anchor; Q9–Q19 resolution pass dated 2026-04-18)
- **State checkpoint**: `docs/engineering/state.md` — **Architecture checkpoint (2026-04-18) — US-0090 / `auto-20260418-01`**
- **PO→TL sprint-plan brief**: `handoffs/po_to_tl.md` **`## Architecture Addendum — US-0090`** (11 atomic task seeds + test surfaces + parity touchpoints + release gates + risks)

### Atomic task seed → AC → DEC-0073 § (sprint-plan locks exact `T-xxx` identifiers)

| Seed | Summary | AC | DEC-0073 § |
|------|---------|----|-----------|
| 1 | `scripts/caveman_compress_input.py` + `template/` mirror (CLI §8; activation §2; deny §4; allow §5; algorithm §6; reason codes §7; sidecar §3) | AC-1..AC-5 | §2, §3, §4, §5, §6, §7, §8 |
| 2 | `docs/engineering/runbook.md` (+ `template/`) — `### Caveman input compression (US-0090)` subsection | AC-5, AC-7 | §9 row 2 |
| 3 | `docs/engineering/auto-orchestration-reference.md` (+ `template/`) — three-sentence non-substitution paragraph | AC-7 | §1 + §9 row 3 |
| 4 | `.gitignore` anchor `docs/.caveman-originals/` + `docs/.caveman-originals/.gitkeep` | AC-2 | §3 + §9 rows 7–8 |
| 5 | `tests/auto_command_contract_test.py` extension — `test_caveman_compress_input_*` subtests | AC-6 | §9 test strategy |
| 6 | `tests/fixtures/caveman_compress/` — 8 fixture classes | AC-6 | §9 test strategy |
| 7 | Rule byte-identity guard + deny-list version guard subtests | AC-6, AC-8 | §9 + §4.2 |
| 8 | `installer-owned-paths.manifest` (+ `template/`) — `template/scripts/caveman_compress_input.py` under `install_include_paths` | AC-8 | §10 |
| 9 | `scripts/check_intake_template_parity.py` (+ `template/`) — `--scope=caveman-compress` mode | AC-8 | §10 Option A |
| 10 | `tests/installer_completeness_bug0003_test.py` extension + new `run-tests` section (candidate `§26S`) | AC-6, AC-8 | §10 Option A + §9 |
| 11 | Architecture `# US-0090` linkage check (assert-only; no rewrite) | AC-7 | §9 row 4 |

### Dev entry conditions (blocking; enforced by `/plan-verify`)

- `/sprint-plan` must author `sprints/SXXXX/sprint.md` + `sprints/SXXXX/tasks.md` + `sprints/SXXXX/plan-verify.json` (`status=PENDING`, `reason=AWAITING_QA_PLAN_VERIFY`).
- `/plan-verify` must move `plan-verify.json` `status` from **`PENDING`** to **`PASS`** before `/execute`.
- Fresh **dev** context required (US-0048 / DEC-0029 isolation); strict runtime proof (DEC-0038) required at `/execute`.
- Dev MUST edit active + `template/` in the same commit for parity rows 1 / 2 / 3 / 8 / 9 of DEC-0073 §9.
- Dev MUST NOT edit `.cursor/rules/caveman.mdc` or its `template/` counterpart (**negative parity; R10 byte-identity**). Pre-US-0090 SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` preserved.
- Dev MUST NOT modify `test_caveman_default_off_*` subtests (DEC-0072 §6 row 6 invariant — additions only, never modifications of existing).
- Dev MUST NOT add new reason codes, new CLI flags (`--mode`, `--purge-orphans`), new allow-list profiles, or new fixture classes beyond `DEC-0073` §9 without a subsequent DEC.
- Dev MUST NOT author or reference `npx skills add` in any rule / doc / command / scratchpad / script (DEC-0072 §8 carried).

### Parity touchpoints at a glance

- **Positive (active + `template/` byte-identical)**: rows 1, 2, 3, 4, 5 of DEC-0073 §9 + installer-owned-paths manifest (§10) + `check_intake_template_parity.py` (§10).
- **Active-only (no mirror; per DEC-0072 §7 precedent)**: architecture section, contract-tests, fixtures, `.gitignore`, `.gitkeep`.
- **NEGATIVE parity (MUST NOT be edited)**: `.cursor/rules/caveman.mdc` + mirror, scratchpad byte strings, `.cursor/skills/its-magic/SKILL.md` + mirror, `.cursorignore`, all canonical-artifact / contract-surface files in DEC-0073 §4.1.

### Risks and their architecture mitigations (sprint-plan must preserve)

- **R8** (aggressive filler-word drift): **aggressive mode deferred** in v1 (§6 Option B only). No `--mode` flag ships. Sprint-plan MUST NOT reopen.
- **R9** (reason-code proliferation): 9 codes locked into 3 families (Gating / Scope / Integrity). No new codes without DEC revising §7.
- **R10** (rule-subsection byte-identity): **no rule edit** in v1 (§9 NEGATIVE parity). Byte-identity guard subtest (seed 7) is a hard requirement.
- **R11** (install-completeness omission / BUG-0003 class): install-completeness fixture extension (seed 10) is **non-negotiable**; `/release` MUST NOT ship without it.

### Scope guards for `/sprint-plan` (non-negotiables)

- Do not rewrite `DEC-0072` or `DEC-0073`. Do not re-open architecture decisions.
- Do not advance backlog status (US-0090 stays **OPEN** per **US-0045**; closure at `/release`).
- Do not seed tasks outside the 11 seeds above without explicit justification tied to a specific AC.
- Do not change `TOKEN_PROFILE` / `CAVEMAN_MODE` / strict-proof / isolation-evidence / `AUTO_QUIET` / US-0071 contracts.

---

## TL -> Dev Handoff — **S0075** / **US-0089** (post-sprint-plan) — post-**`/sprint-plan`** -> **`/plan-verify`** (**qa**) — **superseded** by US-0090 architecture handoff above

> **2026-04-18T12:45:00Z** — **`/sprint-plan`** authored in fresh **tech-lead** context (`orchestrator_run_id=auto-20260418-01`, `fresh_context_marker=tl-US0089-sprint-plan-20260418T124500Z-fresh`). Sprint **`S0075`** created; **AC-1..AC-8** map **1:1** to **`T-001..T-008`** (`plan_integrity.task_ac_bijection=true`, `task_count=8`, `SPRINT_MAX_TASKS=12`, `within_limit=true`, `SPRINT_AUTO_SPLIT` not triggered). Story **`US-0089`** remains **OPEN** (**US-0045**). No execution started yet — next phase is **`/plan-verify`** (fresh **qa**) -> then **`/execute`** (fresh **dev**).

### Sprint anchor

- **Sprint overview**: `sprints/S0075/sprint.md`
- **Atomic tasks**: `sprints/S0075/tasks.md`
- **Plan-verify (qa)**: `sprints/S0075/plan-verify.json` (`status=PENDING`, `reason=AWAITING_QA_PLAN_VERIFY`)
- **Architecture lock**: `decisions/DEC-0072.md` + `docs/engineering/architecture.md` `# US-0089`
- **Research**: `docs/engineering/research.md` `R-0073` (discovery + research extensions)
- **State checkpoint**: `docs/engineering/state.md` — **Sprint-plan checkpoint (2026-04-18) — US-0089 / S0075 / `auto-20260418-01`**

### Task -> AC bijection

| Task | AC | Locked scope (DEC-0072 anchors) |
|------|----|---------------------------------|
| T-001 | AC-1 | Scratchpad keys in `.cursor/scratchpad.md` + active/template `.cursor/scratchpad.local.example.md` (DEC-0072 §3) |
| T-002 | AC-2 | Default-off invariant subtests (DEC-0072 §6 items 6–8: existing tokens, gate vocabulary, no vendor install leak) |
| T-003 | AC-3 | `.cursor/rules/caveman.mdc` (active + `template/`) — 9-zone literal-region invariant + 5 phrases (DEC-0072 §2 / §4 / §5) |
| T-004 | AC-4 | Non-substitution paragraph in `docs/engineering/auto-orchestration-reference.md` (active + `template/`) (DEC-0072 §1) |
| T-005 | AC-5 | `### Caveman mode (US-0089)` subsection in `docs/engineering/runbook.md` (active + `template/`) (DEC-0072 §5) |
| T-006 | AC-6 | 5 remaining `test_caveman_default_off_*` subtests (DEC-0072 §6 items 1–5) |
| T-007 | AC-7 | Architecture section `# US-0089` linkage + append-bottom integrity (assertion-only; no rewrite) |
| T-008 | AC-8 | Template parity sweep + `.cursor/skills/its-magic/SKILL.md` negative-parity (DEC-0072 §7 row 8) |

### Dev entry conditions (blocking)

- `/plan-verify` must move `sprints/S0075/plan-verify.json` `status` from **`PENDING`** to **`PASS`** before `/execute`.
- Fresh **dev** context required (US-0048 / DEC-0029 isolation) and strict runtime proof (DEC-0038) for `/execute`.
- Dev MUST edit active + `template/` in the same commit for rows 2 / 3 / 4 / 5 of DEC-0072 §7.
- Dev MUST NOT edit `.cursor/skills/its-magic/SKILL.md` or its `template/` counterpart (row 8 negative-parity).
- Dev MUST NOT author or reference `npx skills add` in any rule / doc / command / scratchpad (contract subtest #8).

### Carry-forward from pre-sprint architecture handoff

The pre-sprint architecture handoff body (scope, locked decisions, file touchpoints, non-goals, test expectations, parity checklist, scope pointers) stays canonical below; sprint-plan adds task identifiers and ordering only.

---

## TL -> Dev Handoff — **US-0089** (pre-sprint architecture) — post-**`/architecture`** -> **`/sprint-plan`** (**tech-lead**)

> **2026-04-18T12:30:00Z** — **`/architecture`** **PASS** (**tech-lead**, `orchestrator_run_id=auto-20260418-01`, `fresh_context_marker=tl-US0089-architecture-20260418T123000Z-fresh`). **`DEC-0072`** locked. Story **`US-0089`** remains **OPEN** (**US-0045**). No sprint created yet — next phase is **`/sprint-plan`** (fresh **tech-lead**).

### Scope (locked by DEC-0072)

Deliver **response-side** Cursor Caveman voice mode, **default off**, with:

- **Option A orthogonal composition** — `TOKEN_PROFILE` (US-0080 / DEC-0062) and `CAVEMAN_*` are independent axes; neither substitutes for the other.
- **Option A rule-only surface** — single new `.cursor/rules/caveman.mdc` active + `template/` mirror; NO new skill.
- **Four scratchpad keys** with exact byte-literal test strings (see DEC-0072 §3).
- **9-zone literal-region invariant** preserved under `CAVEMAN_MODE=1` (DEC-0072 §4).
- **5 canonical operator toggle phrases** (DEC-0072 §5).
- **8 `test_caveman_default_off_*` subtests** extending `tests/auto_command_contract_test.py` in place (DEC-0072 §6).

### Locked decisions (summary)

| # | Decision | Lock |
|---|----------|------|
| 1 | TOKEN_PROFILE × CAVEMAN | Option A (orthogonal, non-substitution); verbatim paragraph in reference + runbook. |
| 2 | Composition surface | Option A rule-only — `.cursor/rules/caveman.mdc` active + `template/`. No skill. |
| 3 | Scratchpad keys | `CAVEMAN_MODE=0\|1` default `0`; `CAVEMAN_LEVEL=lite\|full\|ultra` default empty; reserved no-ops `CAVEMAN_COMPRESS_INPUT=0\|1` default `0`, `CAVEMAN_FILE_SCOPE=` empty. |
| 4 | Literal-region invariant | 9-zone MUST list (fenced code, paths, AC checklists, reason codes, IDs, contract markers, strict-proof fields, isolation fields, git refs). |
| 5 | Operator phrases | `caveman on`, `caveman off`, `stop caveman`, `normal mode`, `caveman: lite\|full\|ultra`. |
| 6 | Default-off tests | Extend `tests/auto_command_contract_test.py` in place — 8 subtests; no new module. |
| 7 | Template parity | 8-row inventory (DEC-0072 §7; architecture `# US-0089` §7). |
| 8 | Non-goals | No input-side compression (US-0090), no TOKEN_PROFILE change, no canonical artifact rewrites, no new deps, no vendor install path. |

### File touchpoints for `/execute`

| # | Active path | Template path | Action |
|---|-------------|---------------|--------|
| 1 | `.cursor/scratchpad.md` | n/a (example-only install, DEC-0055) | Add 4 Caveman key lines + `## Caveman mode (US-0089)` comment block. |
| 2 | `.cursor/scratchpad.local.example.md` | `template/.cursor/scratchpad.local.example.md` | Add identical 4 key lines + comment block (literal parity). |
| 3 | `.cursor/rules/caveman.mdc` (**new**) | `template/.cursor/rules/caveman.mdc` (**new**) | Create rule per DEC-0072 §2 / §4 / §5. |
| 4 | `docs/engineering/auto-orchestration-reference.md` | `template/docs/engineering/auto-orchestration-reference.md` | Insert non-substitution paragraph near `TOKEN_PROFILE` / `AUTO_QUIET` discussion. |
| 5 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | Add `### Caveman mode (US-0089)` subsection (key table, phrase catalog, non-substitution paragraph). |
| 6 | `docs/engineering/architecture.md` `# US-0089` | active-only | Already written (this phase). |
| 7 | `tests/auto_command_contract_test.py` | active-only | Extend in place (8 subtests). |
| 8 | `.cursor/skills/its-magic/SKILL.md` | `template/.cursor/skills/its-magic/SKILL.md` | **No change** — negative parity assertion. |

### Non-goals (hard)

- No input-side file compression; `CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE` remain **documented no-ops**. No script, no installer change, no file mutator. US-0090 owns that vertical.
- No change to `TOKEN_PROFILE` semantics, context packs, archive policy, or phase-context slimming.
- No rewrite of `docs/product/backlog.md` outside the `## US-0089` `architecture_notes` append, `docs/product/acceptance.md`, `docs/engineering/state.md` schema, `handoffs/intake_evidence/*.json`, or DEC files.
- No new npm / Python dependencies. No `package.json` edit.
- No `npx skills add` surfaced in runbook or rule (contract test #8 guards this).
- No modification of `.cursor/skills/its-magic/SKILL.md` (row 8 negative parity).
- No change to spawn-only orchestration (US-0048 / DEC-0029 / BUG-0006), strict runtime proof (DEC-0038), `AUTO_QUIET` non-suppressible list (US-0088), or US-0071 visible-metadata rules.
- No unit test of voice quality under `CAVEMAN_MODE=1`.

### Test expectations for `/qa`

`tests/auto_command_contract_test.py` gains 8 subtests, all file-presence / token-presence / literal-equality:

1. `test_caveman_default_off_scratchpad_keys_active` — 4 exact lines in `.cursor/scratchpad.md`.
2. `test_caveman_default_off_scratchpad_keys_example_parity` — same 4 lines in both active and template example files (byte parity).
3. `test_caveman_default_off_rule_file_present_active_template` — rule file exists active + `template/`, contains tokens `CAVEMAN_MODE`, `literal`, and all five canonical phrases.
4. `test_caveman_default_off_reference_non_substitution_paragraph` — exact non-substitution sentence in reference doc (active + `template/`).
5. `test_caveman_default_off_runbook_operator_phrases` — five phrases + non-substitution sentence in runbook (active + `template/`).
6. `test_caveman_default_off_existing_contract_tokens_intact` — existing `required` token list unchanged (may only add).
7. `test_caveman_default_off_non_suppressible_gate_vocab_preserved` — gate vocabulary intact in `auto.md` + reference.
8. `test_caveman_default_off_no_vendor_install_leak` — no `npx skills add` token anywhere.

QA must also confirm the 9-zone literal-region list is present verbatim in `.cursor/rules/caveman.mdc` (both active and `template/`).

### Template parity checklist (US-0017)

For each "active + template" row above, parity is asserted via contract subtests #2, #3, #4, #5. Dev MUST:

- Edit both surfaces in the same commit.
- Preserve byte-identical text for the non-substitution paragraph across reference + runbook + template mirrors.
- Preserve byte-identical scratchpad key lines across `.cursor/scratchpad.local.example.md` and `template/.cursor/scratchpad.local.example.md`.
- Leave `.cursor/skills/its-magic/SKILL.md` and `template/.cursor/skills/its-magic/SKILL.md` untouched.

### Scope pointers

- **`docs/engineering/architecture.md`** **`# US-0089`** — full contract.
- **`decisions/DEC-0072.md`** — Accepted decision record (exact test strings in §3 and §6).
- **`docs/engineering/research.md`** **`R-0073`** (research extension 2026-04-18) — rationale for Option A choices and 9-zone list origin.
- **`handoffs/po_to_tl.md`** — Architecture Addendum — US-0089 (tail mirror).

### Governance

- **DEC-0072** (this story).
- **DEC-0062** / **US-0080** — TOKEN_PROFILE semantics unchanged.
- **DEC-0035** / **US-0053** — tiered profile unchanged.
- **US-0088** — `AUTO_QUIET` non-suppressible gate list inherited verbatim.
- **US-0071** — visible ID metadata preserved (9-zone list zone 5).
- **US-0048** / **DEC-0029**, **US-0056** / **DEC-0038**, **BUG-0006** — spawn-only / isolation / strict-proof untouched.
- **US-0017** — active/`template/` parity.
- **DEC-0055** — scratchpad example-only install policy (row 1 has no `template/` mirror of `.cursor/scratchpad.md` itself).
- **DEC-0040** — artifact-ordering policy respected (architecture section appended at bottom).
- **US-0045** — backlog status authority stays in `docs/product/backlog.md`.

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **US-0089** — atomize DEC-0072 §7 parity inventory into tasks against AC-1..AC-8 (story has 8 ACs). Recommended mapping: 1 task per template-parity row + 1 task per test-subtest cluster + 1 task for the architecture-notes / parity sweep, all within `SPRINT_MAX_TASKS=12`. Or **`/auto start-from=sprint-plan`**.

---

## TL -> Dev Handoff — **US-0086** / **S0074** — post-**`/sprint-plan`** -> **`/plan-verify`** (**tech-lead**)

> **2026-04-13T19:45:00Z** - **`/sprint-plan`** **PASS** (**tech-lead**, **`orchestrator_run_id=auto-20260405-01`**). Story **`US-0086`** remains **OPEN** (**US-0045**). Sprint **`S0074`** created. Plan-verify **`PENDING`** (**`AWAITING_QA_PLAN_VERIFY`**) - proceed to **`/plan-verify`** (fresh **qa** context).

### Sprint S0074 summary

- **story_refs**: US-0086
- **goal**: Deliver automation-only remote execution selection with deterministic NL target resolution, fail-closed reason codes, remote-routing evidence tuple capture, US-0085 security continuity, and active/template parity.
- **task_count**: 10 (within SPRINT_MAX_TASKS=12)

### Task map (AC -> Task)

| Task | AC | Summary |
|------|----|---------|
| T-001 | AC-1 | Add automation profile keys to scratchpad surfaces (active + template), default-off/manual unchanged |
| T-002 | AC-2 | Document manual vs automation mode in runbook (active + template) |
| T-003 | AC-3 | Add deterministic mode-on routing guidance and mode-off no-reroute guardrails (commands/rules + template) |
| T-004 | AC-4 | Document/lock `start container <target_id>` resolution and fail-closed unknown/disabled behavior |
| T-005 | AC-5 | Define remote-routing evidence tuple for execute/qa handoffs |
| T-006 | AC-6 | Add deterministic optional CI recipe for remote routing |
| T-007 | AC-7 | Enforce security continuity (no `.env` reads, names-only secret posture) |
| T-008 | AC-8 | Add/extend target-resolution pass/fail tests and mode-off non-regression |
| T-009 | AC-9 | Reconcile architecture lock consistency (`# US-0086`, reason codes, key names, compatibility) |
| T-010 | AC-10 | Perform active/template parity sweep for all touched surfaces |

### Scope pointers

- **`docs/engineering/architecture.md`** **`# US-0086`** — routing precedence, reason codes, evidence tuple, compatibility boundaries
- **`docs/engineering/research.md`** **`R-0068`** — routing matrix and evidence rationale
- **`sprints/S0074/sprint.md`** — sprint metadata + AC coverage matrix
- **`sprints/S0074/tasks.md`** — atomic task definitions
- **`sprints/S0074/plan-verify.json`** — seeded **`PENDING`** for QA

### Governance

- **US-0064 / DEC-0070**: remote schema compatibility unchanged
- **US-0085 / DEC-0071**: no `.env` reads; names-only secret posture
- **US-0045**: backlog status authority remains in `docs/product/backlog.md`

### Next

- **`/plan-verify`** (fresh **qa** context) for **`S0074`** / **`US-0086`**, or **`/auto start-from=plan-verify`**.

## TL -> Dev Handoff — **US-0085** / **S0073** — post-**`/sprint-plan`** → **`/plan-verify`** (**tech-lead**)

> **2026-04-13T12:45:00Z** — **`/sprint-plan`** **PASS** (**tech-lead**, **`orchestrator_run_id=auto-20260405-01`**). Story **`US-0085`** remains **OPEN** (**US-0045**). Sprint **`S0073`** created. Plan-verify **`PENDING`** (**`AWAITING_QA_PLAN_VERIFY`**) — proceed to **`/plan-verify`** (fresh **qa** context).

### Sprint S0073 summary

- **story_refs**: US-0085
- **goal**: Deliver gitignored `.env` for remote and release connectivity with 4-layer defense-in-depth exclusion (DEC-0071), committed `.env.example`, agent/IDE exclusion, operator documentation, optional parity helper, regression tests, and template parity.
- **task_count**: 10 (within SPRINT_MAX_TASKS=12)

### Task map (AC -> Task)

| Task | AC | Summary |
|------|----|---------|
| T-001 | AC-1 | Update `.gitignore` (active) + create `template/.gitignore` with `.env`/`.env.local` |
| T-002 | AC-2 | Create `.cursorignore` (active + template) with `.env*` exclusion |
| T-003 | AC-3 | Create `.env.example` (active + template) — 20 `*Env` names, grouped |
| T-004 | AC-4 | Update `docs/engineering/runbook.md` (active + template) — `.env` recipe |
| T-005 | AC-5 | Update `docs/engineering/runtime-connectivity.md` (active + template) — `*Env` sourcing |
| T-006 | AC-6 | Update `docs/engineering/us-0084-remote-e2e.md` (active + template) — `.env` refs |
| T-007 | AC-7 | Append `.env` exclusion rule to `coding-standards.mdc` (active + template) |
| T-008 | AC-8 | Create `scripts/print_remote_env_hint.py` — names-only parity helper |
| T-009 | AC-9 | Create `tests/test_env_gitignore.py` — regression test |
| T-010 | AC-10 | Verify `remote_config_summary.py` + tests remain PASS |

### Scope pointers

- **`docs/engineering/architecture.md`** **`# US-0085`** — file layout, `.env.example` contract, defense-in-depth layers, template parity, risks
- **`decisions/DEC-0071.md`** — 4-layer `.env` exclusion contract
- **`docs/engineering/research.md`** **`R-0072`** — `*Env` inventory, `.cursorignore` semantics
- **`sprints/S0073/sprint.md`** — sprint metadata + AC coverage matrix
- **`sprints/S0073/tasks.md`** — atomic task definitions

### Governance

- **DEC-0071**: 4-layer defense-in-depth locked — `.gitignore` + `.cursorignore` + Cursor rules + operator discipline
- **US-0064** / **DEC-0070**: JSON schema unchanged; `.env` supplies values locally
- **US-0086** (OPEN): must compose with DEC-0071

### Template parity (7 touchpoints)

| # | Active path | Template path | Action |
|---|-------------|---------------|--------|
| 1 | `.gitignore` | `template/.gitignore` (**new**) | Create with `.env`/`.env.local` |
| 2 | `.cursorignore` (**new**) | `template/.cursorignore` (**new**) | Create with `.env*` patterns |
| 3 | `.env.example` (**new**) | `template/.env.example` (**new**) | 20 names, grouped |
| 4 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | `.env` copy/source recipe |
| 5 | `docs/engineering/runtime-connectivity.md` | `template/docs/engineering/runtime-connectivity.md` | `*Env` sourcing note |
| 6 | `docs/engineering/us-0084-remote-e2e.md` | `template/docs/engineering/us-0084-remote-e2e.md` | `.env`/`.env.example` refs |
| 7 | `.cursor/rules/coding-standards.mdc` | `template/.cursor/rules/coding-standards.mdc` | `.env` exclusion bullet |

### Next

- **`/plan-verify`** (fresh **qa** context) for **`S0073`** / **`US-0085`**, or **`/auto start-from=plan-verify`**.

---

## Research — **US-0094** — post-**`/research`** → **`/architecture`** (**tech-lead**)

> **2026-06-07T12:30:00Z** — **`/research`** **PASS** (`orchestrator_run_id=auto-20260607-01`, `fresh_context_marker=tl-US0094-research-20260607T123000Z-fresh`). Extended **`R-0080`** Q1–Q4. Story **`US-0094`** remains **OPEN** (**US-0045**). **Do not edit README.md** in this phase.

### Research closure summary

| Ask | Resolution |
|-----|------------|
| Q1 Pillar-catalog map | Thematic cross-links only — P1 Commands/auto, P2 Commands+Features gates, P3 Features distribution, P4 Other useful capabilities |
| Q2 Intro budget (`both`×`balanced`) | 3¶, 120–210 words soft / 240 hard; discovery draft 129 words; no new H2 |
| Q3 DEC-0074 companion | **Not required** — document IA in architecture `# US-0094` |
| Q4 Diataxis boundaries | Intro=explanation, pillars=summary, catalog=reference, Setup/How-to/walkthroughs preserved |

### Evidence

- `docs/engineering/research.md` (**`R-0080`**)
- `handoffs/po_to_tl.md` (Orchestrated research handoff — US-0094)
- `docs/product/backlog.md` (`## US-0094` `research_notes`)

### Next

- **`/architecture`** (fresh **tech-lead**) for **`US-0094`**
