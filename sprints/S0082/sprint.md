# Sprint S0082

## Metadata

- **sprint_id**: S0082
- **story_refs**: US-0093
- **goal**: Close the browser UAT execution gap left by **US-0092** / **DEC-0078** — ship two-tier Cursor browser-integrated self-test (`UAT_BROWSER_PROBE_MODE`), complete **`process_health`** / **`cli_smoke`** stubs, automatable **`manual_operator`** verb routing, evidence schema **`browser_evidence_refs`**, fail-closed reason codes, operator docs, contract tests, and template parity — per **DEC-0079** (composes on **DEC-0078**, **US-0065**, **US-0066**).
- **status**: planned
- **created_at**: 2026-06-07T00:00:00Z
- **orchestrator_run_id**: auto-20260606-04
- **fresh_context_marker**: tl-S0082-US0093-sprint-plan-20260607T000000Z-fresh

## Scope

- **US-0093**: Cursor browser-integrated UAT self-test (browser_smoke + automatable manual UI)
- **Architecture**: `docs/engineering/architecture.md` `# US-0093`
- **Binding decision**: `decisions/DEC-0079.md` (Accepted 2026-06-06)
- **Research anchor**: `docs/engineering/research.md` `R-0079`

## Non-goals (hard, from DEC-0079 / architecture `# US-0093`)

- No stdlib-only Playwright as primary path (**R-0041** / operator intake).
- No direct browser MCP calls from **`scripts/uat_probe_lib.py`** (**BUG-0006** spawn-only preserved).
- No silent PASS when MCP unavailable or evidence missing in **`cursor`** mode.
- No auto-read **`.env`**, credential auto-fill, or intake evidence mutation.
- No replacement of human-judgment-only UAT steps; judgment tokens remain **`manual_operator`** → unresolved.
- No auto-bypass of browser approval in production-like targets without explicit scratchpad opt-in.
- **Status authority (US-0045)**: US-0093 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0079** (§1–§11); architecture `# US-0093`; research **R-0079**
- **Governance stack**: **US-0092** / **DEC-0078** (probe catalog + reason-code family — extends, does not weaken), **US-0065** / **US-0066** (runtime QA + generated tests), **US-0088** (self-verify during `/qa` / `/verify-work`), **US-0017** (template parity), **US-0045** (status authority), **US-0048** / **DEC-0029** (isolation), **US-0056** / **DEC-0038** (strict proof), **R-0041** (Cursor browser tools)

## Acceptance criteria coverage (AC-1..AC-10 → T-xxx; surjective bijection)

| AC | Description (summary) | Task | DEC-0079 § / arch anchor |
|----|-----------------------|------|--------------------------|
| AC-1 | Scratchpad **`UAT_BROWSER_PROBE_MODE`** + poll/fallback keys + docs | T-001 | §2; § Scratchpad contract |
| AC-2 | **`browser_smoke`** executes — lib + agent MCP sequence + fallback | T-002 | §1, §3, §5; § Two-tier diagram |
| AC-3 | Automatable **`manual_operator`** verb routing | T-003 | §4; § `manual_operator` verb routing |
| AC-4 | **`process_health`** / **`cli_smoke`** stub completion | T-004 | §6; § Stub completion |
| AC-5 | Evidence **`browser_evidence_refs`** + **`qa-findings.md`** mirror | T-005 | §7; § Evidence schema |
| AC-6 | **`UAT_BROWSER_*`** reason codes + **`--self-test`** + MCP heuristic | T-006 | §8; § Reason codes; § Fallback |
| AC-7 | Security deny-list unchanged; no credential fill | T-007 | §9; § Security |
| AC-8 | Runbook + **`auto-orchestration-reference.md`** operator recipe | T-008 | §10; § Operator docs |
| AC-9 | Contract tests **`test_us0093_*`** + harness **§32** | T-009 | §11; § Contract-test expectations |
| AC-10 | Template parity **`--scope=us-0093`** + installer manifest | T-010 | §11; § Template parity |

**Bijection**: **AC-1..AC-10 ↔ T-001..T-010** (strict 1:1 per architecture `# US-0093` § Atomic task seeds). No `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 10
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (10 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Bijection**: **task_ac_bijection=true** (10 ACs, 10 tasks; 1:1 mapping)

## Governance

- **DEC-0079** §1–§11 (binding) — each task cites governing §(s).
- **R-0079** (research anchor).
- **DEC-0078** forward-link only — probe vocabulary extended, security deny-list not weakened.
- **US-0045** canonical status authority (US-0093 stays OPEN through this sprint).

## Template parity plan (DEC-0079 §11 / architecture § Surfaces)

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `.cursor/scratchpad.md` + `.cursor/scratchpad.local.example.md` | `template/.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` | T-001 | Positive (locked key strings byte-identical) |
| 2 | `scripts/uat_probe_lib.py` | `template/scripts/uat_probe_lib.py` | T-002, T-003, T-004, T-006 | Positive (byte-identical) |
| 3 | `.cursor/commands/verify-work.md`, `qa.md`, `execute.md` | `template/.cursor/commands/` mirrors | T-002 | Positive (Browser UAT subsection strings) |
| 4 | `docs/engineering/runbook.md`, `auto-orchestration-reference.md` | `template/docs/engineering/` mirrors | T-008 | Positive (operator recipe strings) |
| 5 | `docs/engineering/context/installer-owned-paths.manifest` | `template/docs/engineering/context/` mirror | T-010 | Positive (if manifest touched) |
| 6 | `scripts/check_intake_template_parity.py` | active-only `--scope=us-0093` | T-010 | Positive (8-row inventory) |

**Active-only** (no `template/` mirror):

- `docs/engineering/architecture.md` `# US-0093` (architecture phase delivered)
- `tests/auto_command_contract_test.py` extensions
- `tests/run-tests.ps1` / `.sh` harness **§32** (optional)
- `sprints/S0082/uat.md` / `uat.json` (UAT placeholders → populated at verify-work)

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** invoke browser MCP from stdlib lib (**BUG-0006**).
- Do **not** fabricate **`browser_evidence_refs`** in **`cursor`** mode without agent execution.
- Do **not** weaken **DEC-0078** §8 security deny-list.

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Scratchpad + mode keys (T-001)

- Comment block documents **`UAT_BROWSER_PROBE_MODE=cursor|http_fallback|playwright_fallback`** (default **`cursor`**).
- Poll defaults **`UAT_PROCESS_HEALTH_POLL_SECONDS=60`**, **`UAT_PROCESS_HEALTH_POLL_INTERVAL_SECONDS=2`**.

### Browser execution (T-002, T-003, T-006)

- `python scripts/uat_probe_lib.py --self-test` → extended fixture classes for browser modes + verb routing.
- Agent command excerpts cite normative MCP sequence; lib emits **`execution_tier=agent`** without silent PASS.
- Fallback chain: HTTP → Playwright when **`UAT_BROWSER_FALLBACK_CHAIN=1`**.

### Stub completion (T-004)

- **`process_health`**: readiness poll until 2xx or timeout.
- **`cli_smoke`**: backtick command + exit-code assertion.

### Evidence (T-005)

- **`--merge-result`** validates evidence-required-on-PASS in **`cursor`** mode.
- Artifact layout **`sprints/Sxxxx/evidence/browser/`** documented.

### Security (T-007)

- Forbidden step → **`UAT_PROBE_FORBIDDEN`** unchanged; no **`.env`** auto-read in docs or lib.

### Contract tests (T-009)

- Positive: mode keys, **`browser_evidence_refs`**, **`UAT_BROWSER_UNAVAILABLE`** / **`FAILED`** / **`TIMEOUT`** markers.
- Negative: docs must not imply stdlib alone PASSes **`browser_smoke`** in **`cursor`** mode without evidence refs.
- `pytest -k us0093` green post-execute.

### Parity (T-010)

- `python scripts/check_intake_template_parity.py --repo . --scope=us-0093` → `[INTAKE_TEMPLATE_PARITY_OK]`.

## Risks and mitigations (architecture `# US-0093` § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | False PASS without agent evidence | T-005 evidence-required-on-PASS + T-002 **`--merge-result`** |
| R2 | Over-automation of judgment steps | T-003 verb routing; judgment tokens win |
| R3 | MCP unavailable in CI | T-001 **`http_fallback`** recipe + T-006 **`UAT_BROWSER_UNAVAILABLE`** |
| R4 | Secret exposure via browser forms | T-007 **`UAT_PROBE_FORBIDDEN`** + no credential fill |
| R5 | Partial stub delivery | Vertical contract T-001..T-010 single sprint |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 10 acceptance criteria covered 1:1 by T-001..T-010.
- `sprints/S0082/plan-verify.json` reaches **PASS** with `plan_integrity.task_ac_bijection=true`, `task_count=10`, `within_limit=true`.
- Browser probe lib extensions + command contracts + evidence schema + docs/tests/template parity green.
- `docs/product/backlog.md` **`## US-0093`** retains **`OPEN`** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0082`** / **US-0093** — verify AC-1..AC-10 ↔ T-001..T-010 bijection, task-count bound, governance alignment. Target: `sprints/S0082/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
