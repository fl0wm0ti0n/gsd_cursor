# QA Findings — US-0103

**Sprint**: S0103
**Story**: US-0103 — AI Decision Ledger + Plan Fidelity policy
**Sprint story**: sovereign loop audit ledger + plan fidelity tri-state
**QA role**: qa
**QA timestamp**: 2026-06-28T13:20:00Z
**Source handoff**: `handoffs/dev_to_qa.md`
**Sprint reference**: `sprints/S0103/summary.md`, `sprints/S0103/execute-findings.md`

## Verdict

| Verdict | PASS |
|---------|------|
| Blocking findings | 0 |
| Open issues | 0 blocking; 1 minor doc discrepancy |
| Regression (claimed) | **NOT REPRODUCED** — code matches architecture spec |

## Gate battery

| Gate | Result | Evidence |
|------|--------|----------|
| Contract tests (pytest) | **PASS** — 8/8 | `pytest tests/us0103_contract_test.py -v` |
| decision_ledger_lib.py --self-test | **PASS** | `[DECISION_LEDGER_SELF_TEST_OK]` |
| ledger_validate.py --self-test | **PASS** | exit 0 (delegates to library self-test) |
| Parity --scope=sovereign-ledger | **PASS** — pairs=5 | `[INTAKE_TEMPLATE_PARITY_OK] scope=sovereign-ledger pairs=5` |
| Ledger directory (.gitkeep) | **PASS** | `handoffs/sovereign_decisions/.gitkeep` exists |
| Template parity (ledger lib byte-identical) | **PASS** | SHA-256 match: `9355CA04...` |
| Scratchpad keys present | **PASS** | `AI_DECISION_LEDGER=0`, `AUTO_PLAN_FIDELITY=strict` in `.cursor/scratchpad.md` + template mirror |
| Reason code inventory | **PASS** — 11 codes | 5 `PLAN_FIDELITY_*` + 6 `LEDGER_*` |
| Runbook §US-0103 | **PASS** | Line 2582 + full operator recipe |
| Architecture §US-0103 | **PASS** | Line 2884 + full deviation table |
| Reason codes §US-0103 doc | **PASS** | 11 codes enumerated |
| Contract tests present (8 test_us0103_*) | **PASS** | lines 54-344, all 8 tests |
| Backward composition (US-0070/US-0069/US-0048/US-0092) | **PASS** | Test 8 enforces protected-file invariant |
| Zero-overhead invariant | **PASS** | `AI_DECISION_LEDGER=0` default → no file I/O |
| Regression (claimed in user query) | **NOT REPRODUCED** | See §Regression analysis below |

## Test output transcript

```
tests/us0103_contract_test.py::US0103ScratchpadKeysTest::test_us0103_scratchpad_keys_literals PASSED
tests/us0103_contract_test.py::US0103LedgerJsonlSchemaContractTest::test_us0103_ledger_jsonl_schema_contract PASSED
tests/us0103_contract_test.py::US0103StrictModeHardStopTest::test_us0103_strict_mode_hard_stop PASSED
tests/us0103_contract_test.py::US0103RelaxedModeReorderTest::test_us0103_relaxed_mode_reorder_with_ledger PASSED
tests/us0103_contract_test.py::US0103ExtendedModeNonblockingTest::test_us0103_extended_mode_nonblocking PASSED
tests/us0103_contract_test.py::US0103QACrosscheckTest::test_us0103_qa_crosscheck_ledger_findings PASSED
tests/us0103_contract_test.py::US0103ReasonCodeInventoryTest::test_us0103_reason_code_inventory PASSED
tests/us0103_contract_test.py::US0103US0070ComposeNoSchemaChangeTest::test_us0103_us0070_compose_no_schema_change PASSED

============================== 8 passed in 0.08s ==============================

$ python scripts/decision_ledger_lib.py --self-test
[SELF-TEST] Validating decision_ledger_lib contract...
[DECISION_LEDGER_SELF_TEST_OK]

$ python scripts/ledger_validate.py --self-test
[SELF-TEST] Validating decision_ledger_lib contract...
[DECISION_LEDGER_SELF_TEST_OK]
(exit 0)

$ python scripts/check_intake_template_parity.py --scope=sovereign-ledger
[INTAKE_TEMPLATE_PARITY_OK] scope=sovereign-ledger pairs=5
```

## Parity evidence (template / active byte-identical)

SHA-256 (scripts/decision_ledger_lib.py):
- active: `9355CA0424FD16102E27A1F71256F72843C08B00B9F828AB73710350FF504101`
- template: `9355CA0424FD16102E27A1F71256F72843C08B00B9F828AB73710350FF504101`
- result: **BYTE_IDENTICAL**

Parity scope `sovereign-ledger` enumerated 5 pairs — see `execute-findings.md` pair table (all byte-identical).

## Regression analysis

The operator-discovered query claimed a REGRESSION:

| Claimed "Expected" | Claimed "Actual" |
|----|----|
| strict: blocks drop_ac — OK | ALL modes return allow for drop_ac, reorder_ac |
| **relaxed: blocks drop_ac** *(per query)* | ALL modes return allow for drop_ac, reorder_ac |

**QA observation**: the query's "expected" claim for relaxed mode contradicts the locked architecture.

Architecture reference (`docs/engineering/architecture.md`, § Plan-fidelity deviation classification table, lines 2976–2990):

```
| Mode     | deviation_kind      | decision_type          | Outcome                 |
|----------|---------------------|------------------------|-------------------------|
| strict   | drop_ac/reorder_ac  | PLAN_FIDELITY_VIOLATION| hard stop               |
| strict   | add_scope           | PLAN_FIDELITY_SCOPE_GATE| hard stop              |
| strict   | operator_override   | PLAN_FIDELITY_OVERRIDE | recorded + continue     |
| relaxed  | drop_ac/reorder_ac  | PLAN_FIDELITY_REORDER  | recorded + continue     |  <-- NOT hard stop
| relaxed  | add_scope           | PLAN_FIDELITY_SCOPE_GATE| hard stop              |
| relaxed  | operator_override   | PLAN_FIDELITY_OVERRIDE | recorded + continue     |
| extended | drop_ac/reorder_ac  | PLAN_FIDELITY_REORDER  | recorded + continue     |
| extended | add_scope           | PLAN_FIDELITY_EXTENSION| non-blocking + report   |
| extended | operator_override   | PLAN_FIDELITY_OVERRIDE | recorded + continue     |
```

Code behavior (`scripts/decision_ledger_lib.py::_deviation_table`, lines 109–162):

| (mode, kind) | decision_type | blocking |
|---|---|---|
| (STRICT, drop_ac) | PLAN_FIDELITY_VIOLATION | True ✅ |
| (STRICT, reorder_ac) | PLAN_FIDELITY_VIOLATION | True ✅ |
| (STRICT, add_scope) | PLAN_FIDELITY_SCOPE_GATE | True ✅ |
| (STRICT, operator_override) | PLAN_FIDELITY_OVERRIDE | False ✅ |
| (RELAXED, drop_ac) | PLAN_FIDELITY_REORDER | False ✅ |
| (RELAXED, reorder_ac) | PLAN_FIDELITY_REORDER | False ✅ |
| (RELAXED, add_scope) | PLAN_FIDELITY_SCOPE_GATE | True ✅ |
| (EXTENDED, drop_ac) | PLAN_FIDELITY_REORDER | False ✅ |
| (EXTENDED, reorder_ac) | PLAN_FIDELITY_REORDER | False ✅ |
| (EXTENDED, add_scope) | PLAN_FIDELITY_EXTENSION | False ✅ |

**Conclusion: NO REGRESSION.** The implementation matches the locked architecture spec (DEC-0103 §3) exactly.

Test coverage of deviation classifier is explicit:
- `test_us0103_strict_mode_hard_stop` — asserts `blocking=True` for strict+drop_ac/reorder_ac/add_scope (lines 148-157)
- `test_us0103_relaxed_mode_reorder_with_ledger` — asserts `blocking=False` for relaxed+drop_ac/reorder_ac (lines 173-177) and `blocking=True` for relaxed+add_scope (lines 180-182)
- `test_us0103_extended_mode_nonblocking` — asserts `blocking=False` for extended+add_scope and extended+drop_ac/reorder_ac (lines 193-201)

The operator's "expected" claim ("relaxed mode blocks drop_ac") was the inaccurate premise, not the code. This is a spec-reading misunderstanding, not a regression.

## Minor findings (non-blocking)

1. **`ledger_validate.py --self-test` output message discrepancy**:
   - Execute-findings §Test evidence (lines 47-52, 104-106) claims `ledger_validate.py --self-test` emits `[LEDGER_VALIDATION_SELF_TEST_OK]`.
   - Actual behavior: `ledger_validate.py --self-test` imports and invokes `decision_ledger_lib.self_test()` (line 98), which prints `[SELF-TEST] Validating decision_ledger_lib contract...` followed by `[DECISION_LEDGER_SELF_TEST_OK]`. The validator CLI has no dedicated `[LEDGER_VALIDATION_SELF_TEST_OK]` message.
   - Exit code is 0 in both cases; functionally harmless.
   - Execute-findings text is **slightly inaccurate** but the self-test behavior is correct and green.

2. **`.cursor/scratchpad.local.example.md` does not declare `AI_DECISION_LEDGER` or `AUTO_PLAN_FIDELITY`**:
   - Not a spec violation: `scratchpad.local.example.md` covers user-local override keys, and the spec only requires the **primary** scratchpad files (`.cursor/scratchpad.md` + `template/.cursor/scratchpad.md`) and their template byte-parity copies to declare both keys per DEC-0103 §1 / AC-1.
   - Both primary scratchpads + both template copies correctly declare the keys with correct defaults.

## Acceptance criteria coverage (AC-1..AC-8)

| AC | Description | QA Verdict |
|----|-------------|------------|
| AC-1 | Scratchpad key literals | PASS — test_us0103_scratchpad_keys_literals + scratchpad grep |
| AC-2 | Ledger artifact + JSONL schema v1 + append-only | PASS — schema_check + append_entry + read_entries + test_us0103_ledger_jsonl_schema_contract |
| AC-3 | Strict-mode hard stop | PASS — test_us0103_strict_mode_hard_stop asserts blocking |
| AC-4 | Relaxed-mode drop/reorder non-blocking | PASS — test_us0103_relaxed_mode_reorder_with_ledger asserts non-blocking |
| AC-5 | Extended-mode add_scope non-blocking extension | PASS — test_us0103_extended_mode_nonblocking asserts PLAN_FIDELITY_EXTENSION non-blocking |
| AC-6 | QA cross-check ledger_findings | PASS — test_us0103_qa_crosscheck_ledger_findings asserts block shape + fail-closed codes |
| AC-7 | Eight test_us0103_* markers | PASS — all 8 present and green |
| AC-8 | Documentation + reason codes + parity | PASS — runbook §US-0103, architecture §US-0103, reason_codes §US-0103, parity `sovereign-ledger` |

**AC surjective coverage**: 8 tests × 8 AC (bijection surjective — every AC covered by ≥1 test).

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0103-US0103-qa-20260628T132000Z-fresh`
- `timestamp=2026-06-28T13:20:00Z`
- `evidence_ref=sprints/S0103/qa-findings.md,handoffs/qa_to_verify_work.md`

## Traceability index (DEC-0010)

| Story | Sprint | Tasks | Status | Evidence |
|-------|--------|-------|--------|----------|
| US-0103 | S0103 | T-001..T-011 | QA_COMPLETE (pending verify-work) | sprints/S0103/qa-findings.md, handoffs/qa_to_verify_work.md |

## Handoff

- QA verdict: **PASS**
- Next phase: **/verify-work** (fresh **qa** subagent per BUG-0006).
- Regressions to re-investigate: **none**.
