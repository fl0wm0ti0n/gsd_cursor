# UAT Report Cycle 2 — US-0119 / S0119 / qa

**story_id**: US-0119 — Autonomous-autonomy presets + configurable hard-stop relaxation
**sprint_id**: S0119
**phase_id**: qa (UAT merged per ultra_lean)
**qa_cycle**: 2
**verdict**: **CANNOT_RUN**

---

## Cannot-run reason (cycle 2)

UAT is gated on:
- `qa-verdict.json` PASS — **currently FAIL in cycle 2** (7 blocking findings)
- `verify-work-verdict.json` PASS — **currently CANNOT_RUN in cycle 2** (execute-summary.md missing)

Both gates are FAIL/CANNOT_RUN. UAT cannot proceed.

---

## What UAT would test (deferred to cycle 3)

Acceptance tests (per DEC-0119 §9) gated on qa-verdict PASS:
1. AT-1: Set `AUTONOMY_PRESET=none` in scratchpad, run orchestrator, observe byte-identical pre-US-0119 behavior end-to-end
2. AT-2: Set `AUTONOMY_PRESET=balanced`, verify 8-flag expansion consumed correctly
3. AT-3: Set `AUTONOMY_PRESET=full`, verify 12-flag expansion consumed correctly
4. AT-4: Set `AUTONOMY_STOP_POLICY=auto_repair_then_block`, verify dispatch to bounded ledger
5. AT-5: Set `AUTONOMY_STOP_POLICY=auto_repair_then_skip`, verify skip dispatch
6. AT-6: Set cap override, verify cap enforcement at 3 attempts
7. AT-7: Set security-hard reason code, verify NEVER auto-repaired
8. AT-8: Verify breadcrumbs emitted in state.md at phase boundaries

---

## Status: deferred to cycle 3

After dev execute cycle 3 produces execute-summary.md + all 12 tasks PASS + qa-verdict cycle 3 PASS, UAT will be run in /qa cycle 3 or /verify-work as applicable per ultra_lean merge.
