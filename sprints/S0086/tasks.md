# Sprint S0086 Tasks — US-0096

**sprint_id**: S0086  
**story_refs**: US-0096  
**dec_ref**: DEC-0082 (binding; amends DEC-0062 run-class; composes on DEC-0052, DEC-0054, DEC-0080, DEC-0081)  
**task_count**: 12  
**within_limit**: true (12 ≤ `SPRINT_MAX_TASKS=12`; at threshold — `SPRINT_AUTO_SPLIT` not triggered)  
**coverage**: AC-1..AC-12 surjective via T-001..T-012 (12 ACs, 12 tasks; architecture seeds 1:1; multi-AC tasks T-003, T-005/T-006, T-010/T-011, T-012)

> No implementation or test code is authored in this phase — dev owns delivery in `/execute`.

---

## T-001 — **`DELIVERY_MODE`** + **`LEAN_*`** + **`AUTO_DELIVERY_ROUTING`** scratchpad keys + non-substitution paragraph — AC-1

- **ac_ref**: AC-1
- **dec_ref**: DEC-0082 §1; architecture `# US-0096` § Three-mode axis
- **description**: Document **`DELIVERY_MODE=standard|ultra_lean|mega_quick`** (default **`standard`**) in active scratchpad comment block + **`template/.cursor/scratchpad.local.example.md`**. Add optional keys **`LEAN_MEMORY_READ`**, **`LEAN_MEMORY_WRITE`**, **`LEAN_COLD_READ_MAX_SECTIONS`**, **`LEAN_STATE_INDEX_ROWS`**, **`AUTO_DELIVERY_ROUTING`** with defaults per **DEC-0082**. Publish verbatim non-substitution paragraph in **`docs/engineering/auto-orchestration-reference.md`** + **`docs/engineering/runbook.md`** (+ template mirrors).
- **files_affected**:
  - `.cursor/scratchpad.md` (comment block only — operator values unchanged unless Tranche A defaults applied in T-002)
  - `template/.cursor/scratchpad.local.example.md`
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 1; **`US0096_PAIRS`** scratchpad example pair.
- **acceptance_check**:
  - All six scratchpad keys documented with values/defaults.
  - Non-substitution paragraph verbatim in reference + runbook (active/template).
  - Default **`DELIVERY_MODE=standard`** when unset documented.
  - Active/template example parity for scratchpad comment block.
- **status**: done

---

## T-002 — Tranche A: default hot-cap deltas, narrow-read in all phase commands, delta handoff guidance, touch-graph runbook § — AC-3

- **ac_ref**: AC-3
- **dec_ref**: DEC-0082 §3; architecture `# US-0096` § Tranche A universal wins
- **description**: Apply Tranche A default threshold deltas in scratchpad **example** surfaces: **`STATE_HOT_MAX_LINES=1000`**, **`PO_TO_TL_HOT_MAX_LINES=650`**, **`ARCH_HOT_MAX_LINES=3000`** (explicit operator values in active scratchpad override — document precedence). Extend narrow-read **`Inputs`** to **all** phase commands (active + template): cite **`phase-context.md`** + story section anchor; forbid full-file reads when heading exists. Add delta handoff append guidance. Add runbook touch-graph read policy (**`codebase-map.md`** component slice + touched paths before execute).
- **files_affected**:
  - `.cursor/commands/*.md` (all phase commands)
  - `template/.cursor/commands/*.md`
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
  - `template/.cursor/scratchpad.local.example.md` (Tranche A default caps)
- **parity_touchpoints**: architecture § Atomic task seeds row 2; extends **US-0053**.
- **acceptance_check**:
  - Tranche A default caps documented in example scratchpad (1000/650/3000).
  - Every phase command **`Inputs`** includes narrow-read section-scoped guidance.
  - Delta handoff append policy documented (no full rewrites).
  - Runbook touch-graph § present with **`codebase-map.md`** reference.
  - Manual-override precedence paragraph preserved.
- **status**: done

---

## T-003 — Mode-scoped resolver step 0 in **`auto.md`** + reference; **`PHASE_POLICY_CONFLICT`**; standard reinstatement guard — AC-7, AC-2

- **ac_ref**: AC-7, AC-2
- **dec_ref**: DEC-0082 §2; architecture `# US-0096` § Mode-scoped phase resolver
- **description**: Add resolver step 0 to **`/auto`** plan materialization (**before** **DEC-0052**): resolve **`delivery_mode`** (argv **`delivery-mode=`** → backlog row when routing enabled → scratchpad → **`standard`**). Document mode plans: **`standard`** → full **DEC-0052** + **`dec0052_default`** reinstatement; **`ultra_lean`** → **`[spec, plan, build+verify, ship]`** + reinstatement **`none`**; **`mega_quick`** → **`[quick]`** when eligible. **`AUTO_PHASE_*`** applies **only** when **`delivery_mode=standard`**; non-standard + non-default **`AUTO_PHASE_*`** → **`PHASE_POLICY_CONFLICT`**. **`DELIVERY_MODE_SWITCH_MID_STORY`** fail closed. Breadcrumbs: **`delivery_mode`**, **`resolved_phase_plan`**, **`reinstatement_mode`**, **`memory_layer`**. Required literals: **`resolve_delivery_mode`**, **`reinstatement applies only when delivery_mode=standard`**, **`PHASE_POLICY_CONFLICT`**, **`DELIVERY_MODE_SWITCH_MID_STORY`**.
- **files_affected**:
  - `.cursor/commands/auto.md`
  - `template/.cursor/commands/auto.md`
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 3; **`test_us0096_mode_scoped_reinstatement_literals`** + **`test_us0096_standard_mode_baseline_markers_preserved`**.
- **acceptance_check**:
  - Resolver step 0 documented before **DEC-0052** pipeline.
  - All four required doc literals grep-able.
  - Standard mode prose asserts byte-compatible full chain + **DEC-0052** reinstatement.
  - **`PHASE_POLICY_CONFLICT`** rule explicit for non-standard + **`AUTO_PHASE_*`**.
  - Active/template parity for touched sections.
- **status**: done

---

## T-004 — **`ultra_lean`** macro-phase table + role mapping + **`build+verify`** / **`AUTO_IMPLEMENTATION_LOOP`** literals — AC-4

- **ac_ref**: AC-4
- **dec_ref**: DEC-0082 §4; architecture `# US-0096` § ultra_lean macro-lifecycle
- **description**: Document four macro-phases **`spec→plan→build+verify→ship`** with merged canonical phases and default roles (**po** / **tech-lead** / **dev+qa** / **release+curator**). Assert no eleven-phase reinstatement in **`ultra_lean`**. **`AUTO_IMPLEMENTATION_LOOP`** preserved inside **`build+verify`**; QA merges AC + UAT in one spawn. Required literals: **`build+verify`**, **`AUTO_IMPLEMENTATION_LOOP`**, **`spec`**, **`plan`**, **`ship`**.
- **files_affected**:
  - `.cursor/commands/auto.md`
  - `template/.cursor/commands/auto.md`
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 4; **`test_us0096_ultra_lean_macro_phase_literals`**.
- **acceptance_check**:
  - Macro-phase table with four rows and role mapping present.
  - All five required literals grep-able in normative blocks.
  - **`build+verify`** spawn merges execute + qa + verify-work documented.
  - No reinstatement of eleven-phase chain when **`ultra_lean`**.
  - Active/template parity for touched sections.
- **status**: done

---

## T-005 — **`pack.json`** schema v1 + **`scripts/pack_json_validate.py`** + template mirror + **`PACK_*`** codes — AC-5

- **ac_ref**: AC-5
- **dec_ref**: DEC-0082 §5; architecture `# US-0096` § `pack.json` schema v1
- **description**: Implement **`scripts/pack_json_validate.py`** with reason codes **`PACK_*`**. Schema v1 required fields: **`schema_version`** (`"1"`), **`story_id`**, **`delivery_mode`**, **`status`**, **`ac[]`**, **`tasks[]`**, **`refs[]`**, **`deltas[]`**, **`memory_layer`** (`"pack"`). Path convention **`work/<story_id>/pack.json`**. Mirror validator to **`template/scripts/pack_json_validate.py`**. Document coexistence: **`ultra_lean`** → **`work/`** authoritative; **`standard`** → **`sprints/Sxxxx/tasks.md`** authoritative; no destructive overlap.
- **files_affected**:
  - `scripts/pack_json_validate.py` (new)
  - `template/scripts/pack_json_validate.py` (new)
  - `docs/engineering/auto-orchestration-reference.md` (schema docs)
  - `template/docs/engineering/auto-orchestration-reference.md`
  - `docs/engineering/runbook.md` (convention)
  - `template/docs/engineering/runbook.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 5; **`US0096_PAIRS`** validator pair; **`test_us0096_pack_json_schema_contract`**.
- **acceptance_check**:
  - Validator exits 0 on valid fixture; fail-closed **`PACK_*`** on invalid input.
  - All nine required schema fields documented.
  - Coexistence table present (standard / ultra_lean / mega_quick).
  - Active/template validator byte-identical.
- **status**: done

---

## T-006 — **`handoffs/active-context.md`** template + rollover contract + non-triad documentation — AC-5

- **ac_ref**: AC-5
- **dec_ref**: DEC-0082 §5; architecture `# US-0096` § `active-context.md` contract; **DEC-0054** (non-triad)
- **description**: Author **`handoffs/active-context.md`** template stub with hot index row schema (**`story_id`**, **`delivery_mode`**, **`read_before_code[]`**, **`last_delta_utc`**, **`open_risks[]`** max 3). Document line budget **30–80** lines; cap **`LEAN_STATE_INDEX_ROWS`** (default **80**). Rollover: segment **`refresh-context`** complete **or** oversize → archive **`handoffs/archive/active-context-<story_id>-<utc>.md`**. **`ACTIVE_CONTEXT_OVERSIZE`** fail closed when **`LEAN_MEMORY_WRITE=1`**. Explicitly document **`active-context.md` is NOT a triad member** — **`enforce-triad-hot-surface.py`** does not scan it.
- **files_affected**:
  - `handoffs/active-context.md` (template/stub)
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
  - `docs/engineering/auto-orchestration-reference.md` (memory tier table)
  - `template/docs/engineering/auto-orchestration-reference.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 6; **`test_us0096_active_context_contract`**.
- **acceptance_check**:
  - Template stub with required row fields present.
  - Rollover triggers and archive path documented.
  - Non-triad lock explicit in runbook + reference.
  - Line budget and **`LEAN_STATE_INDEX_ROWS`** cap documented.
  - **`ACTIVE_CONTEXT_OVERSIZE`** fail-closed rule documented.
- **status**: done

---

## T-007 — **`mega_quick`** routing + seven eligibility codes + **`quick.md`** enhancements — AC-6

- **ac_ref**: AC-6
- **dec_ref**: DEC-0082 §6; architecture `# US-0096` § mega_quick mode
- **description**: When **`DELIVERY_MODE=mega_quick`** and eligible, **`/auto`** materializes **`["quick"]`** only. Document seven fail-closed codes: **`MEGA_QUICK_BUG_SEGMENT`**, **`MEGA_QUICK_AC_TOO_BROAD`**, **`MEGA_QUICK_ARCHITECTURE_REQUIRED`**, **`MEGA_QUICK_SPRINT_EXISTS`**, **`MEGA_QUICK_STORY_OVERRIDE`**, **`MEGA_QUICK_MULTI_COMPONENT`**, **`MEGA_QUICK_GATE_ESCALATION`**. Artifacts: **`sprints/quick/Qxxxx/task.json`** + **`summary.md`**. Second spawn on test failure only. Enhance **`quick.md`** (+ template) for **`/auto`** routing cross-ref. Ineligible → **`DELIVERY_MODE_INELIGIBLE`** + specific code.
- **files_affected**:
  - `.cursor/commands/auto.md`
  - `template/.cursor/commands/auto.md`
  - `.cursor/commands/quick.md`
  - `template/.cursor/commands/quick.md`
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 7; **`test_us0096_mega_quick_routing_literals`**; **`US0096_PAIRS`** quick.md pair.
- **acceptance_check**:
  - All seven **`MEGA_QUICK_*`** codes documented with rules.
  - **`/quick`** routing path documented under **`/auto`**.
  - Closure requires **`acceptance_met: true`** + green tests.
  - Second spawn only on test failure documented.
  - Active/template parity for `auto.md` + `quick.md` touched sections.
- **status**: done

---

## T-008 — **`AUTO_DELIVERY_ROUTING`** + backlog **`delivery_mode:`** row field + precedence docs — AC-8

- **ac_ref**: AC-8
- **dec_ref**: DEC-0082 §7; architecture `# US-0096` § Optional backlog routing
- **description**: Document **`AUTO_DELIVERY_ROUTING=scratchpad_only|backlog_then_scratchpad`** (default **`scratchpad_only`**). When **`backlog_then_scratchpad`**, story row may declare optional **`delivery_mode:`** field. Precedence chain: argv **`delivery-mode=`** → story row → scratchpad **`DELIVERY_MODE`** → **`standard`**. Add backlog schema documentation (comment block or runbook §) — no mandatory row migration for existing stories.
- **files_affected**:
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
  - `docs/product/backlog.md` (schema comment for **`delivery_mode:`** field — documentation only)
- **parity_touchpoints**: architecture § Atomic task seeds row 8.
- **acceptance_check**:
  - Both **`AUTO_DELIVERY_ROUTING`** values documented.
  - Precedence chain matches **DEC-0082** §7.
  - Optional backlog **`delivery_mode:`** field schema documented.
  - Default **`scratchpad_only`** documented.
  - Active/template reference parity for touched sections.
- **status**: done

---

## T-009 — Quality floor checklist in runbook + lean spawn read/write gates (**`LEAN_MEMORY_*`**) — AC-9

- **ac_ref**: AC-9
- **dec_ref**: DEC-0082 §8; architecture `# US-0096` § Quality floor
- **description**: Add runbook quality floor checklist for all lean modes: tests before stop; AC traceability in pack/task.json; new patterns → architecture/decision delta; **`active-context.md`** updated on material learnings; no secrets/publish bypass. Document **`LEAN_MEMORY_READ=0`** or **`LEAN_MEMORY_WRITE=0`** on **`ultra_lean`** spawn → **`LEAN_MEMORY_DISABLED`** (fail closed).
- **files_affected**:
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
  - `docs/engineering/auto-orchestration-reference.md` (gate table)
  - `template/docs/engineering/auto-orchestration-reference.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 9.
- **acceptance_check**:
  - Quality floor checklist with ≥5 invariants in runbook.
  - **`LEAN_MEMORY_DISABLED`** fail-closed rule documented.
  - QA checklist row for architecture/decision delta on new patterns.
  - Active/template runbook parity for touched sections.
- **status**: done

---

## T-010 — Eight **`test_us0096_*`** contract subtests — AC-10

- **ac_ref**: AC-10
- **dec_ref**: DEC-0082 §10; architecture `# US-0096` § Contract tests + parity
- **description**: Add eight additive contract subtests to **`tests/auto_command_contract_test.py`**: `test_us0096_delivery_mode_scratchpad_keys`, `test_us0096_standard_mode_baseline_markers_preserved`, `test_us0096_mode_scoped_reinstatement_literals`, `test_us0096_ultra_lean_macro_phase_literals`, `test_us0096_mega_quick_routing_literals`, `test_us0096_pack_json_schema_contract`, `test_us0096_active_context_contract`, `test_us0096_token_profile_orthogonality_paragraph`. Run `pytest -k us0096` → all green. **Preserve** **`test_us0095_*`** + **`test_bug0012_*`** green (baseline preservation subtest mandatory).
- **files_affected**:
  - `tests/auto_command_contract_test.py`
- **parity_touchpoints**: architecture § Contract tests table; active-only.
- **acceptance_check**:
  - All eight test function names present with assertions per architecture table.
  - `pytest -k us0096` exits 0 after T-001..T-009 doc/script edits.
  - `pytest -k us0095` and `pytest -k bug0012` still exit 0.
  - Baseline preservation subtest explicitly runs us0095 + bug0012 marker checks under **`standard`**.
- **status**: done

---

## T-011 — **`US0096_PAIRS`** parity manifest + harness **§26Q** — AC-10

- **ac_ref**: AC-10
- **dec_ref**: DEC-0082 §10; architecture `# US-0096` § `US0096_PAIRS`
- **description**: Wire **`check_intake_template_parity.py --scope=us-0096`** manifest **`US0096_PAIRS`** (7 surface pairs + **`pack_json_validate.py`**). Register harness section **§26Q** in **`tests/run-tests.ps1`** + **`tests/run-tests.sh`**. Ensure active ↔ template byte-identical for all touched surfaces from T-001..T-009.
- **files_affected**:
  - `scripts/check_intake_template_parity.py`
  - `template/scripts/check_intake_template_parity.py`
  - `tests/run-tests.ps1`
  - `tests/run-tests.sh`
  - `template/.cursor/commands/auto.md` (final parity sweep)
  - `template/.cursor/commands/quick.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/runbook.md`
  - `template/.cursor/scratchpad.local.example.md`
  - `template/scripts/pack_json_validate.py`
- **parity_touchpoints**: architecture § `US0096_PAIRS` table (7 pairs).
- **acceptance_check**:
  - `python scripts/check_intake_template_parity.py --scope=us-0096` → PASS.
  - Harness **§26Q** registered in both run-tests scripts.
  - All seven **`US0096_PAIRS`** surfaces byte-identical active/template.
  - Parity script scope **`us-0096`** documented in script help.
- **status**: done

---

## T-012 — Runbook operator recipes + **`delivery_mode`** in **`run_class_hash`** + token-cost evidence column — AC-11, AC-12

- **ac_ref**: AC-11, AC-12
- **dec_ref**: DEC-0082 §9, §3 target, §10; architecture `# US-0096` § Runbook operator recipes; § Run-class extension
- **description**: Add runbook operator recipes table (when to use **`standard`** / **`ultra_lean`** / **`mega_quick`**; avoid-when column). Document **`delivery_mode`** as required key in **DEC-0062** sorted run-class object. Evidence rows in **`handoffs/token_cost_runs/<orchestrator_run_id>.md`** MUST include **`delivery_mode`** column. Document comparability rules: **`ultra_lean`** vs **`standard`** same story → **`TOKEN_COST_RUN_CLASS_MISMATCH`**; Tranche A target **≥10%** **`cache_read_tokens`** reduction on matched **`standard`** runs. Add **`ultra_lean`** E2E operator recipe for **`build+verify`** merged spawn (R5 mitigation).
- **files_affected**:
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
  - `docs/engineering/auto-orchestration-reference.md` (run-class amendment)
  - `template/docs/engineering/auto-orchestration-reference.md`
  - Token-cost lib/docs if **`run_class_hash`** serialization lives in scripts (read-only locate first)
- **parity_touchpoints**: architecture § Atomic task seeds row 12; DEC-0082 §9–§10.
- **acceptance_check**:
  - Operator recipes table with three modes + when-to-use / avoid-when columns.
  - **`delivery_mode`** in run-class object documented with sorted JSON serialization note.
  - Token-cost evidence column requirement documented.
  - **`TOKEN_COST_RUN_CLASS_MISMATCH`** rule documented.
  - **`build+verify`** E2E operator recipe present (R5).
  - Active/template runbook parity for touched sections.
- **status**: done

---

## Recommended /execute ordering

1. **T-001** — scratchpad keys + non-substitution (foundation)
2. **T-002** — Tranche A universal wins (always-on baseline)
3. **T-003** — mode-scoped resolver step 0 (before lean modes)
4. **T-004** — ultra_lean macro-phases
5. **T-005** — pack.json validator (Tranche B gate)
6. **T-006** — active-context template (Tranche B gate)
7. **T-007** — mega_quick routing
8. **T-008** — backlog delivery_mode routing (Tranche D)
9. **T-009** — quality floor checklist
10. **T-010** — eight test_us0096_* contract subtests (after docs)
11. **T-011** — US0096_PAIRS parity + harness §26Q
12. **T-012** — runbook recipes + run_class_hash + token evidence (last)
