## Dev → QA Handoff — **S0084** / **US-0095** — post-**`/execute`** → **`/qa`**

> **2026-06-07T21:30:00Z** — **`/execute`** **PASS** in fresh **dev** context (`orchestrator_run_id=auto-20260607-02`, `fresh_context_marker=dev-S0084-US0095-execute-20260607T213000Z-fresh`, `runtime_proof_id=rp-auto-20260607-02-execute-dev-20260607T213000Z-S0084-US0095`, `proof_hash=9cc96c189853d90cb36dc822c4ea5e2df44eabf73ecf7a319c127eb7ddff351d`). All **T-001..T-010** marked **done**. Story **`US-0095`** remains **OPEN** (**US-0045**). Next phase is **`/qa`** (fresh **qa**).

### Sprint anchor

- **Sprint overview**: `sprints/S0084/sprint.md`
- **Atomic tasks**: `sprints/S0084/tasks.md` (T-001..T-010 — all **done**)
- **Plan-verify (qa)**: `sprints/S0084/plan-verify.json` (`status=PASS`)
- **Summary**: `sprints/S0084/summary.md`
- **Architecture**: `docs/engineering/architecture.md` `# US-0095`
- **Decision**: `decisions/DEC-0080.md`
- **Research**: `docs/engineering/research.md` `R-0081`

### AC ↔ Task delivery map

| Task | AC | Status | Evidence |
|------|-----|--------|----------|
| T-001 | AC-1 | done | `Native in-chat auto-chain (US-0095)` § in `auto.md` + reference Step 5 IDE-primary |
| T-002 | AC-2 | done | 7-step drain-advance algorithm with `drain-advance-without-pause`, `immediately`, `without operator re-`/auto`` |
| T-003 | AC-3 | done | Spawn-only loop invariants; US-0069 preflight/post; no BUG-0006 forbidden patterns |
| T-004 | AC-4 | done | Native-chain stop matrix; `decision_gate` hard stop unchanged |
| T-005 | AC-5 | done | Runbook `### Native in-chat auto-chain (US-0095)` primary; outer driver demoted to fallback; README intro ¶3 updated |
| T-006 | AC-6 | done | AUTO_QUIET suppression table + forbidden grep patterns |
| T-007 | AC-7 | done | DEC-0069 pairing mandate; `RESUME_BRIEF_STALE` fail-closed |
| T-008 | AC-8 | done | Seven `test_us0095_*` subtests green |
| T-009 | AC-9 | done | `--scope=us-0095` parity OK; `test_us0095_template_parity_auto_surfaces` green |
| T-010 | AC-10 | done | Unified cap/ledger; `remediation_action` values; breadcrumb fields; security deny-list unchanged |

### Gate results (dev-run)

| Check | Result |
|-------|--------|
| `pytest -k us0095 tests/auto_command_contract_test.py` | **PASS** — 7 passed |
| `python scripts/check_intake_template_parity.py --scope=us-0095` | **PASS** `[INTAKE_TEMPLATE_PARITY_OK]` |

### QA focus areas

1. Verify native-chain literals present in active + template `auto.md` and reference (byte-identical).
2. Confirm README + runbook demote outer driver to **optional** / **fallback** without deleting US-0092 autonomy headline.
3. Re-run `pytest -k us0095` and parity `--scope=us-0095` on fresh checkout.
4. Confirm spawn-only (**BUG-0006**) invariants not weakened in native-chain prose.
5. Confirm forbidden-pattern list documented but not used as mandatory IDE instructions.

### Scope guards for `/qa`

- **Do not** advance backlog status — **US-0095** stays **OPEN** until `/release`.
- **Do not** weaken isolation (**US-0048**) or strict-proof (**US-0056**) gates.
- **Do not** delete `scripts/auto_outer_driver.py`.

### Next

- **`/qa`** (fresh **qa**) for **`S0084`** / **`US-0095`**
