# QA Findings — S0105 / US-0105

**Sprint**: S0105  
**Story**: US-0105 — Sovereign Memory  
**Phase**: `/qa` (post-execute)  
**QA role**: qa  
**QA timestamp**: 2026-06-29T00:11:00Z  
**Orchestrator run ID**: auto-20260628-04  
**Fresh context marker**: qa-S0105-US0105-20260629T001100Z-fresh  
**Source handoff**: `handoffs/dev_to_qa.md`  
**Sprint reference**: `sprints/S0105/summary.md`, `sprints/S0105/execute-findings.md`, `sprints/S0105/tasks.md`  
**Binding decision**: `decisions/DEC-0105.md`

## Verdict

| Verdict | **PASS** |
|---------|----------|
| Blocking findings | 0 |
| Open issues | 0 |
| US-0105 status | **OPEN** (US-0045 — closure at `/release` only) |

## Gate battery

| Gate | Result | Evidence |
|------|--------|----------|
| Contract tests (`pytest -k us0105`) | **PASS** — 10/10 | 8 core markers + 2 compose guards |
| `sovereign_memory_lib.py --self-test` | **PASS** | `[SOVEREIGN_MEMORY_SELF_TEST_OK]` exit 0 |
| `sovereign_memory_validate.py --self-test` | **PASS** | `[SOVEREIGN_MEMORY_VALIDATION_OK]` exit 0 |
| Parity `--scope=sovereign-memory` | **PASS** — pairs=6 | `[INTAKE_TEMPLATE_PARITY_OK]` |
| Scratchpad keys (active + template) | **PASS** | Five `SOVEREIGN_MEMORY_*` keys with DEC-0105 defaults |
| Directory bootstrap | **PASS** | `.gitkeep` + `retrospectives/.gitkeep` active + template |
| Phase spawn digest hook | **PASS** | `sovereign_memory_digest` in auto-orchestration, execute, lib block builder |
| Mistake-tagging hooks | **PASS** | `/auto` fix-fail + fidelity; `/execute` revert; closed enum + `record_mistake_hook` |
| Curator retrospective | **PASS** | `/refresh-context` documents `write_retrospective` + `promote_from_ledger`; retros not injected v1 |
| JSONL rollover | **PASS** | `maybe_archive_jsonl` on append; `SOVEREIGN_MEMORY_ARCHIVE_REQUIRED` fail-closed |
| Reason codes § US-0105 | **PASS** | 8 codes in `docs/engineering/reason_codes.md` |
| Runbook § US-0105 | **PASS** | `docs/engineering/runbook.md` § Sovereign Memory |
| Architecture `# US-0105` | **PASS** | Pre-satisfied per execute handoff |
| Zero-overhead default | **PASS** | `SOVEREIGN_MEMORY=0` → no writes, empty digest, no block (`test_us0105_zero_overhead_default`) |
| `state.md` untouched | **PASS** | Not modified per execute handoff and QA instruction |

## Test output transcript

```
tests/us0105_contract_test.py::US0105ScratchpadKeysTest::test_us0105_scratchpad_keys_literals PASSED
tests/us0105_contract_test.py::US0105DirectoryContractTest::test_us0105_sovereign_memory_directory_contract PASSED
tests/us0105_contract_test.py::US0105JsonlSchemaContractTest::test_us0105_jsonl_schema_contract PASSED
tests/us0105_contract_test.py::US0105InjectionDigestCharCapTest::test_us0105_injection_digest_char_cap PASSED
tests/us0105_contract_test.py::US0105DecisionDedupBranchTest::test_us0105_decision_dedup_branch PASSED
tests/us0105_contract_test.py::US0105MistakeTaggingLiteralsTest::test_us0105_mistake_tagging_literals PASSED
tests/us0105_contract_test.py::US0105ZeroOverheadDefaultTest::test_us0105_zero_overhead_default PASSED
tests/us0105_contract_test.py::US0105ComposeGuardsTest::test_us0105_compose_guards PASSED
tests/us0105_contract_test.py::US0105US0029ComposeTest::test_us0105_us0029_compose_no_research_schema_change PASSED
tests/us0105_contract_test.py::US0105US0080InjectionCharCapTest::test_us0105_us0080_injection_respects_char_cap PASSED

===================== 10 passed, 226 deselected in 1.60s ======================

$ python scripts/sovereign_memory_lib.py --self-test
[SOVEREIGN_MEMORY_SELF_TEST_OK]

$ python scripts/sovereign_memory_validate.py --self-test
[SOVEREIGN_MEMORY_SELF_TEST_OK]
[SOVEREIGN_MEMORY_VALIDATION_OK]

$ python scripts/check_intake_template_parity.py --scope=sovereign-memory
[INTAKE_TEMPLATE_PARITY_OK] scope=sovereign-memory pairs=6
```

## Parity evidence (`SOVEREIGN_MEMORY_PAIRS`)

| Pair | Result |
|------|--------|
| `scripts/sovereign_memory_lib.py` ↔ template | **IDENTICAL** (parity scope) |
| `scripts/sovereign_memory_validate.py` ↔ template | **IDENTICAL** (parity scope) |
| `.cursor/scratchpad.md` `SOVEREIGN_MEMORY_*` block ↔ template | **PASS** |
| `docs/engineering/sovereign-memory/.gitkeep` ↔ template | **PASS** |
| `decisions/DEC-0105.md` ↔ template | **PASS** |
| Retrospectives `.gitkeep` ↔ template | **PASS** |

## AC coverage

| AC | Verdict | Primary evidence |
|----|---------|------------------|
| AC-1 | **PASS** | `test_us0105_scratchpad_keys_literals` — five keys + zero-overhead when `0` |
| AC-2 | **PASS** | `test_us0105_sovereign_memory_directory_contract` + validator v1 schemas; create-on-first-write JSONL |
| AC-3 | **PASS** | `test_us0105_injection_digest_char_cap` — top-N + top-K merge + char cap |
| AC-4 | **PASS** | Spawn hook prose + `build_injection_digest_block`; US-0023 additive read-only |
| AC-5 | **PASS** | `test_us0105_compose_guards` — refresh-context retrospective + ledger promotion |
| AC-6 | **PASS** | `test_us0105_decision_dedup_branch` + `test_us0105_mistake_tagging_literals` |
| AC-7 | **PASS** | Eight `test_us0105_*` + parity `--scope=sovereign-memory` pairs=6 |
| AC-8 | **PASS** | Reason codes, runbook, architecture, compose guards US-0029/US-0080 |

## Informational notes (non-blocking)

| ID | Category | Summary |
|----|----------|---------|
| QA-S0105-001 | optional-defer | `test_regression` mistake hook in enum but deferred v1.1 per DEC-0105 §6 — acceptable |
| QA-S0105-002 | bootstrap | JSONL files create-on-first-write; only `.gitkeep` tracked at bootstrap — per DEC-0105 |
| QA-S0105-003 | ac-extension | Fifth scratchpad key `SOVEREIGN_MEMORY_JSONL_MAX_LINES` extends backlog AC-1 prose — documented in DEC-0105 |

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0105-US0105-20260629T001100Z-fresh`
- `timestamp=2026-06-29T00:11:00Z`
- `evidence_ref=sprints/S0105/qa-findings.md,sprints/S0105/qa-verdict.json,handoffs/dev_to_qa.md,sprints/S0105/summary.md,sprints/S0105/execute-findings.md,tests/us0105_contract_test.py,decisions/DEC-0105.md`

## Next phase

Spawn fresh **qa** subagent for **`/verify-work`** on **S0105** / **US-0105** (spawn-only per BUG-0006). Do **not** flip US-0105 to DONE or modify `docs/engineering/state.md`.
