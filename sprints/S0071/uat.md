# Sprint S0071 UAT — US-0087 (`/auto` explicit bug targeting)

- **Sprint**: `S0071`
- **Work item**: **US-0087**
- **Orchestrator run**: **auto-20260405-01**
- **Machine-readable**: `sprints/S0071/uat.json`
- **Populated**: **2026-04-12T18:00:00Z** (DEC-0009 — no longer placeholder)
- **Overall**: **PASS** — **10** / **10** steps **pass** (**0** fail)
- **Canonical backlog / acceptance**: **`docs/product/backlog.md`** (**US-0087** **OPEN**); **`docs/product/acceptance.md`** **US-0087** row remains **unchecked** until **`/release`** + curator/backlog closure (**US-0045**).

## UAT steps (results)

| Step | AC | Result | Summary |
|------|-----|--------|---------|
| UAT-1 | AC-1 | **pass** | `bug-target=` argv literals + fail-closed codes in `auto.md`, reference, template `auto.md`; contract tests. |
| UAT-2 | AC-2 | **pass** | `AUTO_BUG_*` keys default-off on active + template scratchpad paths; pair parity **OK**. |
| UAT-3 | AC-3 | **pass** | Bug-target resume precedence + `AUTO_SCHEDULER_CONFLICT` mutex documented; harness aligned. |
| UAT-4 | AC-4 | **pass** | OPEN-only queue, numeric sort, `AUTO_BUG_MAX_ITEMS`, `AUTO_BUG_QUEUE_EMPTY` in reference. |
| UAT-5 | AC-5 | **pass** | Segment fields for `resume_brief` / `state.md` (DEC-0069 / AC-10); story segment fields verified for this delivery. |
| UAT-6 | AC-6 | **pass** | Spawn-only `/auto`; no in-process phase execution; BUG-0006 / US-0069 cross-refs. |
| UAT-7 | AC-7 | **pass** | `auto_command_contract_test.py` green; full harness **794** pass / **0** fail (`tests/report.md` **2026-04-07T20:56:59Z**). |
| UAT-8 | AC-8 | **pass** | `architecture.md` **# US-0087** reason codes and interaction matrix. |
| UAT-9 | AC-9 | **pass** | Runbook “targeted bug auto drain” (+ template). |
| UAT-10 | AC-10 | **pass** | Template parity for touched paths (tests + summary evidence). |

## Evidence bundle (in-repo)

- **`sprints/S0071/summary.md`** — implemented scope + test commands
- **`sprints/S0071/qa-findings.md`** — **PASS**, **US-0066** generated-test refs (`tests/report.md`, `tests/`)
- **`handoffs/qa_to_verify_work.md`** — QA → verify-work handoff
- **`docs/engineering/state.md`** — execute (initial + remediation) + QA isolation + strict proofs

## Results summary (traceability)

- **US-0087** acceptance criteria **AC-1..AC-10** are mapped **1:1** to **UAT-1..UAT-10** above; all **pass** based on documented delivery + **PASS** **`/qa`** (**TEST_COMMAND** + targeted pytest).
- Portfolio checkbox **US-0087** in **`docs/product/acceptance.md`** is **not** flipped here — **US-0045** authority is **`docs/product/backlog.md`** through **`/release`** / **`/refresh-context`**.
- **Next phase**: **`/release`** (fresh **release** role) or **`/auto start-from=release`** with `orchestrator_run_id=auto-20260405-01`.
