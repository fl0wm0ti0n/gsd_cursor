# Sprint S0081

## Metadata

- **sprint_id**: S0081
- **story_refs**: US-0092
- **goal**: Ship opt-in **`AUTO_FLOW_MODE=full_autonomy`** (default-off) with stdlib outer driver **`scripts/auto_outer_driver.py`**, shared UAT probe resolver **`scripts/uat_probe_lib.py`**, bounded block-retry ledger, drain-without-pause, TOKEN_PROFILE orthogonality audit, stop-matrix docs, contract tests, and template parity — per **DEC-0078** (composes on **US-0088**, **DEC-0062**, **DEC-0047**, **DEC-0048**).
- **status**: planned
- **created_at**: 2026-06-06T20:00:00Z
- **orchestrator_run_id**: auto-20260606-03
- **fresh_context_marker**: tl-S0081-US0092-sprint-plan-20260606T200000Z-fresh

## Scope

- **US-0092**: Full-autonomy `/auto` mode + outer driver + self-verification
- **Architecture**: `docs/engineering/architecture.md` `# US-0092`
- **Binding decision**: `decisions/DEC-0078.md` (Accepted 2026-06-06)
- **Research anchor**: `docs/engineering/research.md` `R-0078`

## Non-goals (hard, from DEC-0078 / architecture `# US-0092`)

- No removal of all decision gates globally; **`decision_gate`** remains hard stop.
- No bypass of QA / release / isolation / strict-proof (**US-0048**, **US-0056**).
- No change to **`TOKEN_PROFILE`** tier semantics beyond orthogonality clarification.
- No vendor Cursor multi-turn guarantee beyond documented outer-driver hook.
- No auto-read **`.env`**, no intake evidence mutation, no publish without **`RELEASE_PUBLISH_MODE=auto`**.
- No substitution for spawn-only phase-role subagents (**BUG-0006** / **US-0069** unchanged).
- **Status authority (US-0045)**: US-0092 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0078** (§1–§11); architecture `# US-0092`; research **R-0078**
- **Governance stack**: **US-0088** (continuous `/auto` + stop matrix baseline), **US-0044** (backlog drain), **US-0065** / **US-0066** (runtime QA + generated tests), **US-0080** / **DEC-0062** (TOKEN_PROFILE), **US-0087** (bug-queue mutex), **US-0017** (template parity), **US-0045** (status authority), **US-0048** / **DEC-0029** (isolation), **US-0056** / **DEC-0038** (strict proof), **DEC-0069** (boundary refresh)

## Acceptance criteria coverage (AC-1..AC-10 → T-xxx; surjective bijection)

| AC | Description (summary) | Task | DEC-0078 § / arch anchor |
|----|-----------------------|------|--------------------------|
| AC-1 | Scratchpad **`full_autonomy`** enum + new keys + interaction docs | T-001 | §1; § Scratchpad contract |
| AC-2 | Shipped **`scripts/auto_outer_driver.py`** (stdlib, argv/exit codes) | T-002 | §2; § Outer-driver script API |
| AC-3 | Self-verify via **`uat_probe_lib.py`** + **`/verify-work`** / **`/qa`** excerpts | T-003 | §3; § UAT probe contract |
| AC-4 | Block auto-resolve ledger + cap interaction | T-004 | §4; § Block-retry ledger |
| AC-5 | Drain-without-pause + **DEC-0069** boundary refresh | T-005 | §5; § Drain-without-pause |
| AC-6 | **`TOKEN_PROFILE`** orthogonality audit + grep fixes | T-006 | §6; § TOKEN_PROFILE orthogonality |
| AC-7 | Stop matrix in **`auto.md`**, **`auto-orchestration-reference.md`** | T-007 | §7; § Stop matrix |
| AC-8 | Contract tests in **`auto_command_contract_test.py`** | T-008 | §8; § Contract-test expectations |
| AC-9 | Template parity + installer manifest entries | T-009 | §9; § Surfaces |
| AC-10 | Security deny-list + runbook outer-driver recipe | T-010 | §10; § Security; § Runbook |

**Bijection**: **AC-1..AC-10 ↔ T-001..T-010** (strict 1:1 per architecture `# US-0092` § Atomic task seeds). No `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 10
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (10 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Bijection**: **task_ac_bijection=true** (10 ACs, 10 tasks; 1:1 mapping)

## Governance

- **DEC-0078** §1–§11 (binding) — each task cites governing §(s).
- **R-0078** (research anchor).
- **US-0088** forward-link only — stop matrix extends, does not rewrite.
- **US-0045** canonical status authority (US-0092 stays OPEN through this sprint).

## Template parity plan (DEC-0078 §9 / architecture § Surfaces)

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `.cursor/scratchpad.md` + `.cursor/scratchpad.local.example.md` | `template/.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` | T-001 | Positive (locked key strings byte-identical) |
| 2 | `scripts/auto_outer_driver.py` | `template/scripts/auto_outer_driver.py` | T-002 | Positive (byte-identical) |
| 3 | `scripts/uat_probe_lib.py` | `template/scripts/uat_probe_lib.py` | T-003 | Positive (byte-identical) |
| 4 | `.cursor/commands/verify-work.md`, `.cursor/commands/qa.md` | `template/.cursor/commands/verify-work.md`, `template/.cursor/commands/qa.md` | T-003 | Positive (self-verify excerpt strings) |
| 5 | `.cursor/commands/auto.md` | `template/.cursor/commands/auto.md` | T-007 | Positive (stop matrix § strings) |
| 6 | `docs/engineering/auto-orchestration-reference.md` | `template/docs/engineering/auto-orchestration-reference.md` | T-006, T-007 | Positive (orthography + stop matrix) |
| 7 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-006, T-010 | Positive (outer-driver subsection + orthography fix) |
| 8 | `docs/engineering/context/installer-owned-paths.manifest` | `template/docs/engineering/context/installer-owned-paths.manifest` | T-009 | Positive (new script paths) |
| 9 | `README.md` family cross-refs (if touched) | `template/README.md` | T-006 | Positive when edited (US-0017) |

**Active-only** (no `template/` mirror):

- `docs/engineering/architecture.md` `# US-0092` (architecture phase delivered)
- `tests/auto_command_contract_test.py` extensions
- `handoffs/auto_block_retry/` ledger directory (runtime artifact)
- `sprints/S0081/uat.md` / `uat.json` (UAT placeholders → populated at verify-work)

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** weaken spawn-only (**BUG-0006**) or isolation/strict-proof gates.
- Do **not** auto-read **`.env`** or mutate intake evidence.
- Do **not** imply **`TOKEN_PROFILE`** changes automation level after audit.

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Outer driver (T-002, T-005)

- `python scripts/auto_outer_driver.py --dry-run` with `AUTO_FLOW_MODE=full_autonomy` → planned invocations emitted
- Activation gate: mode not `full_autonomy` → exit **2** `AUTO_FLOW_MODE_NOT_FULL_AUTONOMY`
- Drain-advance branch without operator pause when drain policy enabled

### UAT probes (T-003)

- `python scripts/uat_probe_lib.py --self-test` (or equivalent) → probe catalog resolves/fail-closed reason codes
- Shared resolver wired in **`/verify-work`** and **`/qa`** command excerpts

### Block-retry ledger (T-004)

- Append-only JSONL under `handoffs/auto_block_retry/<orchestrator_run_id>.jsonl`; names-only fields

### TOKEN_PROFILE audit (T-006)

- Grep forbidden patterns absent post-fix; runbook “automation breadth” conflict removed active + template
- Contract markers: `TOKEN_PROFILE controls context breadth / token cost only`

### Contract tests (T-008)

- Positive: `AUTO_FLOW_MODE=full_autonomy`, outer-driver path, drain-advance-without-operator phrases
- Negative: forbidden TOKEN_PROFILE automation-proxy strings

### Parity (T-009)

- `python scripts/check_intake_template_parity.py --repo .` passes for touched surfaces
- Installer manifest lists new scripts

### Security (T-010)

- Runbook `### Full-autonomy outer driver (US-0092)` + security deny-list callout
- No publish without **`RELEASE_PUBLISH_MODE=auto`**

## Risks and mitigations (architecture `# US-0092` § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Infinite driver loop | T-002 `AUTO_LOOP_MAX_CYCLES` + exit codes |
| R2 | Self-verify false PASS | T-003 fail-closed `UAT_PROBE_UNRESOLVED` |
| R3 | TOKEN_PROFILE doc drift | T-006 grep + T-008 contract markers |
| R4 | Security (secrets/publish) | T-010 hard deny-list + publish gate |
| R5 | Partial delivery (flags without driver) | Vertical contract T-001..T-010 single sprint |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 10 acceptance criteria covered 1:1 by T-001..T-010.
- `sprints/S0081/plan-verify.json` reaches **PASS** with `plan_integrity.task_ac_bijection=true`, `task_count=10`, `within_limit=true`.
- Outer driver + probe lib + ledger + docs/tests/template parity green.
- `docs/product/backlog.md` **`## US-0092`** retains **`OPEN`** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0081`** / **US-0092** — verify AC-1..AC-10 ↔ T-001..T-010 bijection, task-count bound, governance alignment. Target: `sprints/S0081/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
