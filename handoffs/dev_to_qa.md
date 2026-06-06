## Dev → QA Handoff — **S0082** / **US-0093** — post-**`/execute`** → **`/qa`**

> **2026-06-07T00:30:00Z** — **`/execute`** **DONE** in fresh **dev** context (`orchestrator_run_id=auto-20260606-04`, `fresh_context_marker=dev-S0082-US0093-execute-20260607T003000Z-fresh`, `runtime_proof_id=rp-auto-20260606-04-execute-dev-20260607T003000Z-S0082-US0093`, `proof_hash=01014a9fa592e1b183f47595b20ad2c5c1fe9562aa6387b177d077dbfe47e62e`). All **T-001..T-010** marked **done**. Story **`US-0093`** remains **OPEN** (**US-0045**). Next phase is **`/qa`** (fresh **qa**).

### Sprint anchor

- **Sprint overview**: `sprints/S0082/sprint.md`
- **Atomic tasks**: `sprints/S0082/tasks.md` (T-001..T-010 — all **done**)
- **Summary**: `sprints/S0082/summary.md`
- **Binding decision**: `decisions/DEC-0079.md` (§1–§11)
- **Architecture**: `docs/engineering/architecture.md` `# US-0093`

### AC ↔ Task delivery map

| Task | AC | Status | Evidence |
|------|-----|--------|----------|
| T-001 | AC-1 | done | Scratchpad `UAT_BROWSER_PROBE_MODE` + poll keys in active/template/local-example |
| T-002 | AC-2 | done | `uat_probe_lib.py` two-tier browser + command MCP excerpts |
| T-003 | AC-3 | done | `manual_operator` verb routing with judgment precedence |
| T-004 | AC-4 | done | `process_health` / `cli_smoke` execution branches |
| T-005 | AC-5 | done | `browser_evidence_refs` schema + `--merge-result` |
| T-006 | AC-6 | done | `UAT_BROWSER_*` codes + extended `--self-test` |
| T-007 | AC-7 | done | Security deny-list unchanged; no credential fill docs |
| T-008 | AC-8 | done | Runbook + auto-orchestration-reference operator recipe |
| T-009 | AC-9 | done | `test_us0093_*` + harness §32 |
| T-010 | AC-10 | done | `--scope=us-0093` parity + architecture linkage assert |

### Test summary (dev-run)

| Check | Result |
|-------|--------|
| `python scripts/uat_probe_lib.py --self-test` | **PASS** `[UAT_PROBE_LIB_SELF_TEST_OK]` |
| `pytest -k us0093 tests/auto_command_contract_test.py` | **PASS** (6 tests) |
| `python scripts/check_intake_template_parity.py --scope=us-0093` | **PASS** `[INTAKE_TEMPLATE_PARITY_OK]` |
| `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` | **PASS** `[BUG_VALIDATION_OK]` |

### QA focus areas

1. Confirm **DEC-0078** deny-list not weakened — forbidden steps still **`UAT_PROBE_FORBIDDEN`**.
2. Confirm docs **do not** imply stdlib alone PASSes **`browser_smoke`** in **`cursor`** mode without **`browser_evidence_refs`**.
3. Confirm **`uat_probe_lib.py`** never invokes browser MCP (spawn-only / **BUG-0006**).
4. Template parity: active + `template/` byte-identical for all **DEC-0079** §11 rows.
5. Runbook CI recipe: **`UAT_BROWSER_PROBE_MODE=http_fallback`**.

### Scope guards for `/qa`

- **Do not** advance backlog status — **US-0093** stays **OPEN** until `/release`.
- **Do not** weaken **DEC-0078** security deny-list or spawn-only contract.

### Next

- **`/qa`** (fresh **qa**) for **`S0082`** / **`US-0093`**
