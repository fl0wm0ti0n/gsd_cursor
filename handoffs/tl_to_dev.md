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
