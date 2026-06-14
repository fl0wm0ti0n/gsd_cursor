# Sprint S0085 Tasks — BUG-0012

**sprint_id**: S0085  
**bug_refs**: BUG-0012  
**dec_ref**: DEC-0081 (binding; amends DEC-0080 enforcement layer; composes on DEC-0078, BUG-0006, DEC-0069)  
**task_count**: 8  
**within_limit**: true (8 ≤ `SPRINT_MAX_TASKS=12`); `SPRINT_AUTO_SPLIT` not triggered  
**coverage**: AC-1..AC-8 surjective via T-001..T-008 (8 ACs, 8 tasks; architecture seeds 1:1; T-003/T-004 share AC-4; T-007/T-008 share AC-8)

> No implementation or test code is authored in this phase — dev owns delivery in `/execute`.

---

## T-001 — Orchestrator-only **MUST Task-spawn** continuation block in `auto.md` — AC-1

- **ac_ref**: AC-1
- **dec_ref**: DEC-0081 §1; architecture `# BUG-0012` § Orchestrator compliance contract
- **description**: Add orchestrator-only continuation mandate block to **`.cursor/commands/auto.md`** (+ template): after foreground subagent return, when continuation schedulable (next phase, drain target, relaxable retry within budget), orchestrator **MUST Task-spawn** next phase-role subagent per **US-0069** preflight; **must not** treat phase-role handoff as run terminal; **must not** emit mandatory re-**`/auto`** or **`auto_outer_driver.py`** terminal prose. Document actor distinction table (phase-role subagent stops vs orchestrator continues). Required literals: **`orchestrator MUST Task-spawn`**, **`post-subagent continuation`**, **`phase-role stop is not run terminal`**.
- **files_affected**:
  - `.cursor/commands/auto.md`
  - `template/.cursor/commands/auto.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 1; DEC-0081 §1.
- **acceptance_check**:
  - Orchestrator-only block distinct from phase-role command "stop" semantics.
  - Actor distinction table present (phase-role vs `/auto` orchestrator).
  - All three required doc literals grep-able in orchestrator context sections.
  - No prose implying orchestrator executes phase-role work in-band (**BUG-0006**).
  - Active / template `auto.md` byte-identical per **US-0017**.
- **status**: done

---

## T-002 — Scope US-0088 matrix + Steps Option B to fallback; **`native chain supersedes Option B`** — AC-2

- **ac_ref**: AC-2
- **dec_ref**: DEC-0081 §1 (native-chain precedence); architecture `# BUG-0012` § Native-chain precedence over US-0088 Option B
- **description**: Amend **`auto.md`** § Continuous multi-phase (US-0088 matrix) and Steps item 5 (+ template): under **`AUTO_FLOW_MODE=full_autonomy`** + IDE + Task available, native chain **must** continue in-chat — not "stop segment; operator may advance". Scope Option B outer-driver equivalence to **`NATIVE_CHAIN_UNAVAILABLE`** / headless/CI/`--invoke-cmd` only. Mirror amendments in **`auto-orchestration-reference.md`** full-autonomy matrix (outer-driver re-invoke row = fallback). Required literal: **`native chain supersedes Option B`**.
- **files_affected**:
  - `.cursor/commands/auto.md`
  - `template/.cursor/commands/auto.md`
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 2; DEC-0081 §1 + §4 demote ambiguous rows.
- **acceptance_check**:
  - US-0088 continuous matrix clarifies native chain **must** advance in IDE **`full_autonomy`**.
  - Steps item 5 Option B scoped to **`NATIVE_CHAIN_UNAVAILABLE`** / headless only.
  - Reference full-autonomy matrix L783-class row scoped to fallback.
  - Required literal `native chain supersedes Option B` present.
  - Active/template mirrors byte-identical for touched sections.
- **status**: done

---

## T-003 — Harden drain-advance steps 6→7 — no operator stop; `drain_advance_action` attestation docs — AC-3, AC-4

- **ac_ref**: AC-3, AC-4
- **dec_ref**: DEC-0081 §2–§3; architecture `# BUG-0012` § Drain-advance step 7 enforcement; § Continuation-truth breadcrumbs
- **description**: Amend drain-advance algorithm in **`auto-orchestration-reference.md`** and **`auto.md`** (+ template): between **DEC-0080** steps **6** and **7**, orchestrator **must not** emit operator wait instructions, set **`stop_reason=completed (segment exhausted)`** when drain budget > 0 and eligible OPEN item exists, or skip Task-spawn for step **7**. Document **`drain_advance_action=spawned|skipped|not_applicable`** attestation on `state.md` phase boundary (`skipped` when budget > 0 + OPEN item exists is **invalid**). Add breadcrumb field docs/comments for **`drain_advance_action`** in reference and `state.md` guidance (comments only — no checkpoint fabrication).
- **files_affected**:
  - `.cursor/commands/auto.md`
  - `template/.cursor/commands/auto.md`
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
  - `docs/engineering/state.md` (comments/examples only if needed)
- **parity_touchpoints**: architecture § Atomic task seeds row 3.
- **acceptance_check**:
  - Step 6→7 documented as immediate spawn with no operator stop between.
  - Forbidden segment-exhausted terminal when continuation pending under **`full_autonomy`**.
  - `drain_advance_action` enum and semantics documented.
  - Invalid `skipped` when budget > 0 + OPEN item exists explicitly stated.
  - Reference + `auto.md` active/template parity for touched sections.
- **status**: done

---

## T-004 — `native_chain_continuing` breadcrumb + **`resume_brief`** orchestrator spawn pairing wording — AC-4, AC-7

- **ac_ref**: AC-4, AC-7
- **dec_ref**: DEC-0081 §3, §6; architecture `# BUG-0012` § Continuation-truth breadcrumbs; § `resume_brief` + reference alignment; **DEC-0069**
- **description**: Document **`native_chain_continuing`** (`true` when orchestrator scheduled next spawn/advance this boundary) alongside existing **`native_chain_active`** gate field. Update **`resume_brief`** template pairing contract lines (+ reference): orchestrator **MUST Task-spawn** next phase — **`/auto`** is orchestrator context label, not operator re-invocation instruction. Invariant: `native_chain_continuing=true` ⇒ no mandatory re-**`/auto`** prose; `stop_reason` ≠ `completed (segment exhausted)` when continuation pending.
- **files_affected**:
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
  - `.cursor/commands/auto.md` (pairing cross-ref if needed)
  - `template/.cursor/commands/auto.md`
  - `handoffs/resume_brief.md` (template pairing lines — not live checkpoint fabrication)
- **parity_touchpoints**: architecture § Atomic task seeds row 4; DEC-0081 §3 + §6.
- **acceptance_check**:
  - `native_chain_continuing` field documented with semantics distinct from `native_chain_active`.
  - **DEC-0069** pairing lines state orchestrator **MUST Task-spawn** — not "operator runs `/auto`".
  - Continuation invariant documented (no segment-exhausted stop when continuing).
  - Reference active/template parity for breadcrumb + pairing sections.
- **status**: done

---

## T-005 — Implement four **`test_bug0012_*`** contract subtests — AC-5

- **ac_ref**: AC-5
- **dec_ref**: DEC-0081 §5; architecture `# BUG-0012` § Contract tests
- **description**: Add four additive contract subtests to **`tests/auto_command_contract_test.py`**: `test_bug0012_forbidden_drain_stop_prose_negative_grep`, `test_bug0012_orchestrator_post_subagent_spawn_mandate`, `test_bug0012_drain_advance_step7_no_stop_between_6_and_7`, `test_bug0012_native_chain_precedence_over_option_b`. Run `pytest -k bug0012 tests/auto_command_contract_test.py` → all green. **Preserve** all seven **`test_us0095_*`** subtests green (additive layer only).
- **files_affected**:
  - `tests/auto_command_contract_test.py`
- **parity_touchpoints**: architecture § Contract tests table; active-only.
- **acceptance_check**:
  - All four test function names present with assertions per architecture table.
  - `pytest -k bug0012` exits 0 after T-001..T-004 doc edits.
  - `pytest -k us0095` still exits 0 (no regression).
  - Spawn mandate test asserts **`orchestrator MUST Task-spawn`** literal in `auto.md`.
- **status**: done

---

## T-006 — Negative grep forbidden drain-stop prose in full_autonomy normative blocks — AC-6

- **ac_ref**: AC-6
- **dec_ref**: DEC-0081 §4; architecture `# BUG-0012` § Forbidden-prose negative enforcement
- **description**: Ensure **`test_bug0012_forbidden_drain_stop_prose_negative_grep`** (T-005) covers negative grep scope: mandatory `re-run /auto` between drain segments; `segment exhausted` as terminal when continuation pending; mandatory `run the outer driver` in IDE-primary path; unqualified `python scripts/auto_outer_driver.py` without **optional** / **fallback** qualifier. Remediate any hits in **`auto.md`** + **`auto-orchestration-reference.md`** full_autonomy / native-chain normative blocks (+ template mirrors) surfaced by grep.
- **files_affected**:
  - `.cursor/commands/auto.md`
  - `template/.cursor/commands/auto.md`
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
  - `tests/auto_command_contract_test.py` (negative grep assertions — may overlap T-005 subtest 1)
- **parity_touchpoints**: architecture § Forbidden-prose table; DEC-0081 §4.
- **acceptance_check**:
  - Negative grep passes on IDE-primary **`full_autonomy`** / native-chain normative blocks.
  - Forbidden patterns from architecture table absent or qualified as optional/fallback.
  - `test_bug0012_forbidden_drain_stop_prose_negative_grep` green.
  - **DEC-0078** hard-gate vocabulary unchanged (no relaxation).
- **status**: done

---

## T-007 — Runbook § **BUG-0012 regression verify** — multi-segment operator E2E recipe — AC-8

- **ac_ref**: AC-8
- **dec_ref**: DEC-0081 §7; architecture `# BUG-0012` § Operator E2E recipe
- **description**: Add runbook subsection **`### BUG-0012 regression verify`** (+ template mirror) with 6-step operator recipe: scratchpad **`AUTO_FLOW_MODE=full_autonomy`**, **`AUTO_BACKLOG_DRAIN=1`**, **`AUTO_BACKLOG_MAX_STORIES≥2`**, **`AUTO_QUIET=1`**; backlog ≥2 OPEN stories; single **`/auto`** in Cursor IDE; complete story A through **`refresh-context`**; **Pass** = drain-advance to story B first phase without operator re-**`/auto`** and without forbidden terminal prose; evidence: `drain_advance_action=spawned`, `native_chain_continuing=true`, `resume_brief` `story_id` advance.
- **files_affected**:
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
- **parity_touchpoints**: architecture § Operator E2E recipe; DEC-0081 §7.
- **acceptance_check**:
  - Runbook subsection title **`BUG-0012 regression verify`** present.
  - All six recipe steps documented with pass/fail criteria.
  - Evidence fields named: `drain_advance_action`, `native_chain_continuing`, `resume_brief` `story_id`.
  - Active/template runbook delta byte-identical.
- **status**: done

---

## T-008 — Template parity `--scope=bug-0012`; preserve **`test_us0095_*`** green; architecture + DEC linkage assert — AC-8

- **ac_ref**: AC-8
- **dec_ref**: DEC-0081 §8; architecture `# BUG-0012` § Template parity
- **description**: Ensure active ↔ `template/` byte-identical mirrors for all touched surfaces: `auto.md`, `auto-orchestration-reference.md`, runbook § BUG-0012. Wire or extend `check_intake_template_parity.py --scope=bug-0012` (6-row inventory). Add read-only linkage assert subtest (e.g. `test_bug0012_architecture_dec_linkage`) verifying `# BUG-0012` references **DEC-0081**, **R-0083**, amends **DEC-0080**. Final gate: `pytest -k us0095` + `pytest -k bug0012` both green.
- **files_affected**:
  - `template/.cursor/commands/auto.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/runbook.md`
  - `tests/auto_command_contract_test.py` (linkage assert)
  - `scripts/check_intake_template_parity.py` (scope extension if needed)
- **parity_touchpoints**: architecture § Template parity (6 surfaces); DEC-0081 §8.
- **acceptance_check**:
  - `check_intake_template_parity.py --scope=bug-0012` passes (or equivalent 6-row scan).
  - Active/template deltas empty for `auto.md`, reference, runbook.
  - Linkage assert confirms **DEC-0081** + **R-0083** + **DEC-0080** amend relationship.
  - `pytest -k us0095` and `pytest -k bug0012` both exit 0.
- **status**: done

---

## Recommended /execute ordering

1. **T-001** — orchestrator MUST Task-spawn mandate (foundation)
2. **T-002** — native chain supersedes Option B (precedence)
3. **T-003** — drain-advance step 7 no-stop + `drain_advance_action`
4. **T-004** — `native_chain_continuing` + resume_brief pairing
5. **T-006** — forbidden-prose remediation (before/alongside contract tests)
6. **T-005** — four `test_bug0012_*` contract subtests (docs literals must exist)
7. **T-007** — runbook E2E recipe
8. **T-008** — template parity sweep + linkage assert (last)
