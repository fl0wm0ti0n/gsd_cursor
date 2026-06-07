# Sprint S0084 Tasks — US-0095

**sprint_id**: S0084  
**story_refs**: US-0095  
**dec_ref**: DEC-0080 (binding; composes on DEC-0078, US-0088, BUG-0006, DEC-0069)  
**task_count**: 10  
**within_limit**: true (10 ≤ `SPRINT_MAX_TASKS=12`); `SPRINT_AUTO_SPLIT` not triggered  
**bijection**: AC-1..AC-10 ↔ T-001..T-010 (strict 1:1 per architecture `# US-0095` § Atomic task seeds, consolidated)

> No implementation or test code is authored in this phase — dev owns delivery in `/execute`.

---

## T-001 — Native in-chat auto-chain § in `auto.md` + reference Step 5 IDE-primary path — AC-1

- **ac_ref**: AC-1
- **dec_ref**: DEC-0080 §1–§2; architecture `# US-0095` § Native in-chat auto-chain contract
- **description**: Add **`Native in-chat auto-chain (US-0095)`** section to **`.cursor/commands/auto.md`** (+ template) with activation gate (`AUTO_FLOW_MODE=full_autonomy` + IDE context + Task tool available), continuation loop (preflight → spawn → await → verify → caps → branch), forbidden turn-boundary semantics (`stop_reason=completed (segment exhausted)` invalid when continuation schedulable), and **`NATIVE_CHAIN_UNAVAILABLE`** fail-closed. Amend **`auto-orchestration-reference.md`** Step 5 (+ template) with IDE primary path literals: `foreground sequential`, `same /auto orchestrator session`, `Native in-chat auto-chain`.
- **files_affected**:
  - `.cursor/commands/auto.md`
  - `template/.cursor/commands/auto.md`
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
- **parity_touchpoints**: DEC-0080 §9; architecture § Touch inventory rows 1–2.
- **acceptance_check**:
  - Activation gate table documents three conditions including `native_chain_active=true` breadcrumb.
  - Continuation loop mandates orchestrator must not stop after one phase/segment solely due to Cursor turn boundaries.
  - Required literals present: `Native in-chat auto-chain`, `foreground sequential`, `same /auto orchestrator session`, `NATIVE_CHAIN_UNAVAILABLE`.
  - Reference Step 5 labels IDE path as primary when `full_autonomy` + IDE context.
  - Active / template `auto.md` and reference excerpts byte-identical per **US-0017**.
- **status**: done

---

## T-002 — Document 7-step IDE drain-advance algorithm + required literals — AC-2

- **ac_ref**: AC-2
- **dec_ref**: DEC-0080 §3; architecture `# US-0095` § IDE drain-advance-without-pause
- **description**: Document deterministic **7-step** drain-advance algorithm in **`auto-orchestration-reference.md`** and **`auto.md`** IDE-primary section (+ template mirrors). Include trigger conditions (`refresh-context` boundary, drain policy, budget remaining) and normative steps: READ boundary → ASSERT **DEC-0069** pairing → SELECT next item → RELOAD scratchpad + MATERIALIZE phase plan → PREPEND `resume_brief` → APPEND `state.md` breadcrumb → IMMEDIATELY spawn first phase subagent. Required literals: `drain-advance-without-pause`, `immediately`, `without operator re-`/auto``.
- **files_affected**:
  - `.cursor/commands/auto.md`
  - `template/.cursor/commands/auto.md`
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
- **parity_touchpoints**: Reference + `auto.md` positive parity.
- **acceptance_check**:
  - All 7 algorithm steps documented with normative action verbs.
  - Trigger table matches architecture (drain/bug-queue mutex per **US-0087**).
  - No operator message requiring `auto_outer_driver.py` or manual re-`/auto` under IDE `full_autonomy`.
  - Required literals grep-able in IDE-primary sections.
- **status**: done

---

## T-003 — Spawn-only invariants + **BUG-0006** regression guard in docs — AC-3

- **ac_ref**: AC-3
- **dec_ref**: DEC-0080 §1 (loop invariants); architecture `# US-0095` § Native in-chat auto-chain contract (invariants); **BUG-0006** / **US-0069**
- **description**: Explicitly document spawn-only invariants in **`auto.md`** native-chain section: orchestrator schedules phase-role subagents only; each phase completes via fresh spawn + artifacts; orchestrator must not execute phase-role work in-band. Cross-reference **US-0069** preflight/post checks. Ensure native-chain prose introduces no forbidden **BUG-0006** patterns (`AUTO_ORCHESTRATOR_PHASE_EXECUTION`, in-band phase work). Prepare contract anchor for `test_us0095_spawn_only_regression`.
- **files_affected**:
  - `.cursor/commands/auto.md`
  - `template/.cursor/commands/auto.md`
- **parity_touchpoints**: `auto.md` active ↔ template byte-identical.
- **acceptance_check**:
  - Three loop invariants from architecture documented verbatim in intent.
  - No new prose implying orchestrator substitutes for phase-role subagents.
  - **US-0069** preflight/post check references present.
  - Forbidden **BUG-0006** pattern scan passes on touched `auto.md` sections.
- **status**: done

---

## T-004 — Confirm stop matrix hard gates unchanged in docs — AC-4

- **ac_ref**: AC-4
- **dec_ref**: DEC-0080 §4; architecture `# US-0095` § Stop matrix
- **description**: Document stop matrix in **`auto-orchestration-reference.md`** and **`auto.md`** (+ template) confirming hard gates unchanged under IDE native chain: `decision_gate`, isolation/strict-proof violations, security deny, `BACKLOG_MAX_STORIES_REACHED`, `AUTO_LOOP_MAX_CYCLES`, unrecoverable `error`, `pause_request`. Relaxable transient stops per **DEC-0078** matrix when configured. Native chain must not weaken any hard gate.
- **files_affected**:
  - `.cursor/commands/auto.md`
  - `template/.cursor/commands/auto.md`
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
- **parity_touchpoints**: Reference + `auto.md` positive parity.
- **acceptance_check**:
  - Hard-stop condition table matches architecture § Stop matrix.
  - `decision_gate` explicitly listed as hard stop (no relaxation).
  - Relaxable stops distinguished from hard stops per **DEC-0078**.
  - No prose relaxing isolation (**US-0048**) or strict-proof (**US-0056**) requirements.
- **status**: done

---

## T-005 — Runbook + README outer-driver demotion (primary `/auto` once; fallback optional) — AC-5

- **ac_ref**: AC-5
- **dec_ref**: DEC-0080 §5; architecture `# US-0095` § Fallback boundary matrix
- **description**: Runbook (+ template): add **`### Native in-chat auto-chain (US-0095)`** as primary IDE recipe; demote **`### Full-autonomy outer driver (US-0092)`** to fallback subsection with primary/fallback table (IDE = native chain primary, outer driver optional; headless/CI = outer driver recommended; `--invoke-cmd` = required). README family (+ template, byte-identical per **US-0017**): amend intro ¶3 + Autonomous AI workflow pillar — `/auto` once in Cursor primary; `scripts/auto_outer_driver.py` optional/fallback only (**US-0094** follow-on touch). Remove or rewrite mandatory outer-driver prose for IDE `full_autonomy`.
- **files_affected**:
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
  - `README.md`
  - `template/README.md`
- **parity_touchpoints**: Runbook active ↔ template; README byte-identical (**US-0017**).
- **acceptance_check**:
  - Runbook primary/fallback table matches architecture § Fallback boundary matrix.
  - README intro ¶3 names in-chat `/auto` as default IDE hands-off recipe.
  - Outer driver labeled `optional` / `fallback` adjacent to IDE path prose.
  - No mandatory `run the outer driver` phrasing in IDE-primary sections.
  - `optional` / `fallback` literals present for contract test `test_us0095_outer_driver_fallback_not_mandatory_ide`.
- **status**: done

---

## T-006 — **`AUTO_QUIET`** suppression table + forbidden grep patterns — AC-6

- **ac_ref**: AC-6
- **dec_ref**: DEC-0080 §6; architecture `# US-0095` § `AUTO_QUIET` messaging
- **description**: Add **`AUTO_QUIET`** suppression table to **`auto-orchestration-reference.md`** and **`auto.md`** (+ template): routine phase PASS and in-chat continuation suppressible when `AUTO_QUIET=1`; gates, caps, errors, `NATIVE_CHAIN_UNAVAILABLE` always non-suppressible. Document forbidden IDE-primary patterns: mandatory `run the outer driver`; `re-run /auto` between drain segments; `segment exhausted` as terminal when continuation pending; unqualified `python scripts/auto_outer_driver.py`.
- **files_affected**:
  - `.cursor/commands/auto.md`
  - `template/.cursor/commands/auto.md`
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
- **parity_touchpoints**: Reference + `auto.md` positive parity.
- **acceptance_check**:
  - Suppression table matches architecture (routine vs non-suppressible events).
  - Forbidden pattern list documented for grep/contract enforcement.
  - Drain advance under `AUTO_QUIET=1` suppresses routine prose but not outer-driver wait instructions (because none should exist).
  - Contract anchor prepared for `test_us0095_auto_quiet_no_outer_driver_mandatory`.
- **status**: done

---

## T-007 — **DEC-0069** pairing mandate before in-chat continuation — AC-7

- **ac_ref**: AC-7
- **dec_ref**: DEC-0080 §3 step 2; architecture `# US-0095` § IDE drain-advance step 2; **DEC-0069**
- **description**: Document **DEC-0069** pairing mandate in **`auto-orchestration-reference.md`** and **`auto.md`** (+ template): every phase boundary and drain advance must refresh **`resume_brief`** + **`state.md`** before scheduling in-chat continuation. Stale brief → **`RESUME_BRIEF_STALE`** fail-closed (no advance). Include `resume_brief` pairing contract references for contract test `test_us0095_resume_brief_pairing_markers`.
- **files_affected**:
  - `.cursor/commands/auto.md`
  - `template/.cursor/commands/auto.md`
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
- **parity_touchpoints**: Reference + `auto.md` positive parity.
- **acceptance_check**:
  - Pairing mandate stated before continuation spawn in both phase-chain and drain-advance paths.
  - `RESUME_BRIEF_STALE` documented as fail-closed with no in-chat advance.
  - `resume_brief` + `state.md` named as required refresh targets.
  - Contract markers align with `test_us0095_resume_brief_pairing_markers`.
- **status**: done

---

## T-008 — Implement six **`test_us0095_*`** contract subtests — AC-8

- **ac_ref**: AC-8
- **dec_ref**: DEC-0080 §7; architecture `# US-0095` § Contract tests + parity
- **description**: Add six contract subtests to **`tests/auto_command_contract_test.py`**: `test_us0095_native_in_chat_auto_chain_markers`, `test_us0095_ide_drain_advance_without_outer_driver`, `test_us0095_outer_driver_fallback_not_mandatory_ide`, `test_us0095_spawn_only_regression`, `test_us0095_auto_quiet_no_outer_driver_mandatory`, `test_us0095_resume_brief_pairing_markers`. Run `pytest -k us0095 tests/auto_command_contract_test.py` → all green.
- **files_affected**:
  - `tests/auto_command_contract_test.py`
- **parity_touchpoints**: Active-only (contract tests not mirrored to template).
- **acceptance_check**:
  - All six test function names present with assertions per architecture table.
  - `pytest -k us0095` exits 0.
  - `test_us0095_spawn_only_regression` asserts **BUG-0006** forbidden patterns not introduced.
  - `test_us0095_template_parity_auto_surfaces` deferred to T-009 if split; if combined here, still only AC-8 scope (parity test may assert surfaces exist — full parity wiring in T-009).
- **status**: done

---

## T-009 — Template parity for 8-surface touch inventory + installer scope — AC-9

- **ac_ref**: AC-9
- **dec_ref**: DEC-0080 §8; architecture `# US-0095` § Contract tests (`test_us0095_template_parity_auto_surfaces`); **US-0017**
- **description**: Ensure active ↔ `template/` byte-identical mirrors for all touched surfaces: `auto.md`, `auto-orchestration-reference.md`, runbook § US-0095, README family (if touched in T-005). Wire or extend `check_intake_template_parity.py --scope=us-0095` (or equivalent 8-row inventory). Implement `test_us0095_template_parity_auto_surfaces` asserting parity for touched command/reference/runbook paths.
- **files_affected**:
  - `template/.cursor/commands/auto.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/runbook.md`
  - `template/README.md` (if T-005 touched README)
  - `tests/auto_command_contract_test.py` (parity subtest)
  - `scripts/check_intake_template_parity.py` (scope extension if needed)
- **parity_touchpoints**: Full 8-surface inventory per **R-0081** Q6.
- **acceptance_check**:
  - `check_intake_template_parity.py` passes for `--scope=us-0095` or full touched-surface scan.
  - `test_us0095_template_parity_auto_surfaces` green.
  - Active/template deltas empty for `auto.md`, reference, runbook.
  - README root ↔ template byte-identical if T-005 edited README.
- **status**: done

---

## T-010 — State breadcrumb fields + unified cap/ledger `remediation_action` docs + security deny-list — AC-10

- **ac_ref**: AC-10
- **dec_ref**: DEC-0080 §4; architecture `# US-0095` § Unified cap + ledger; **DEC-0078** security deny-list
- **description**: Document unified cap/ledger in **`auto-orchestration-reference.md`** (+ template): `AUTO_LOOP_MAX_CYCLES` counts phase spawns + drain advances; `AUTO_IMPLEMENTATION_LOOP` → `implementation_loop_index`; `AUTO_BLOCK_RETRY_MAX` via shared `handoffs/auto_block_retry/<orchestrator_run_id>.jsonl`; new `remediation_action` values (`phase_respawn`, `native_chain_continue`, `drain_advance`). Document state breadcrumb fields per phase boundary: `native_chain_active`, `outer_cycle_index`, `implementation_loop_index`. Confirm security deny-list unchanged: no auto-read `.env`, no intake evidence mutation, no publish without `RELEASE_PUBLISH_MODE=auto`.
- **files_affected**:
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
  - `docs/engineering/state.md` (comments/examples only if needed — no checkpoint fabrication)
- **parity_touchpoints**: Reference active ↔ template.
- **acceptance_check**:
  - Cap table matches architecture § Unified cap + ledger.
  - All three breadcrumb field names documented with semantics.
  - Three new `remediation_action` values listed alongside existing `outer_reinvoke`.
  - Security deny-list explicitly unchanged from **DEC-0078**.
  - Cap ordering documented: `AUTO_LOOP_MAX_CYCLES` first, then implementation loop + block retry before recoverable retry.
- **status**: done

---

## Recommended /execute ordering

1. **T-001** — native in-chat auto-chain § + reference Step 5 (foundation)
2. **T-003** — spawn-only invariants (early guardrail)
3. **T-002** — 7-step drain-advance algorithm
4. **T-004** — stop matrix hard gates
5. **T-007** — DEC-0069 pairing mandate
6. **T-006** — AUTO_QUIET suppression table
7. **T-010** — cap/ledger + breadcrumb docs
8. **T-005** — runbook + README demotion
9. **T-008** — contract subtests (docs literals must exist first)
10. **T-009** — template parity sweep (last — after all content edits)
