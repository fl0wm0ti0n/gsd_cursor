# PO to TL archive pack (2026-06-28)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 10
- First archived heading: `## Orchestrated research handoff — US-0107 / auto-20260628-04`
- Last archived heading: `## Orchestrated discovery handoff — US-0107 / auto-20260628-04`
- Verification tuple (mandatory):
  - archived_body_lines=147
  - retained_body_lines=635

---

## Orchestrated research handoff — US-0107 / auto-20260628-04

### Target

- `story_id=US-0107`
- `orchestrator_run_id=auto-20260628-04`
- phase completed: **`research`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0107-research-20260629T001600Z-fresh`
- `next_scheduled_phase=architecture`
- `decomposition=single_story` (sovereign-loop batch per intake-sovereign-20260627-01.json)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=5`

### Summary

- **`/research`** **PASS** — **`R-0094`** Q1–Q7 closed; architecture-ready locks on deferral JSONL v1, **`sovereign_loop_lib.py`** API + **`SovereignLoopStepResult`**, drain-generate PO spawn + decision gate, ntfy/hook notification adapters (email deferred v1), fail-closed **`SOVEREIGN_LOOP_GOAL_MODE_REQUIRED`** coupling, contract-test inventory, and companion **`DEC-0107`** recommendation.
- **Goal-mode**: `AUTO_SOVEREIGN=1` requires `SOVEREIGN_GOAL_MODE=goal_convergence` — no auto-enable.
- **Deferral register**: append-only JSONL with latest-state-wins open rows; shared `list_open_deferrals()` for **US-0110** compose integration.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Research locks (architecture inputs)

| Lock | Decision |
|------|----------|
| **Binding decision** | **`DEC-0107`** (to author) — composes **US-0088** / **US-0092** / **US-0095** / **US-0044** / **US-0103** / **US-0105** / **US-0110** |
| **Deferral schema** | `handoffs/sovereign_deferrals.jsonl` v1 + **`sovereign_loop_validate.py`** CLI |
| **Lib API** | **`scripts/sovereign_loop_lib.py`** — deferral CRUD, `advance_sovereign_loop`, `dispatch_notification` |
| **Drain-generate** | Ephemeral **`DrainGenerateCandidateBundle`**; PO spawn; **decision gate per candidate**; max 3 candidates/iteration |
| **Notification** | ntfy + hook v1 (stdlib urllib); email deferred; fail-open dispatch |
| **Goal coupling** | Fail-closed **`SOVEREIGN_LOOP_GOAL_MODE_REQUIRED`** when sovereign on without goal mode |
| **Contract tests** | Eight **`test_us0107_*`** + compose guards **`test_us0107_us0110_*`**, **`test_us0107_us0095_*`** |
| **Parity scope** | **`check_intake_template_parity.py --scope=sovereign-loop`** (**`SOVEREIGN_LOOP_PAIRS`**) |

### Top risks (carry to /architecture)

- **R1**: Goal-mode coupling — operator must set both `AUTO_SOVEREIGN=1` and `SOVEREIGN_GOAL_MODE=goal_convergence`.
- **R2**: Drain-generate scope creep — mandatory decision gate + 3-candidate cap per iteration.
- **R3**: Deferral cap vs **`CONVERGENCE_DEFERRALS_PENDING`** — shared open-row reader; cap blocks append.
- **R4**: Notification secrets — topic/URL local-only; never in git-tracked artifacts.
- **R5**: Sovereign terminal stops additive — must not false **`drain_terminated`** on story exhaustion alone.
- **R6**: **US-0109** ordering — deferral v1 stable first; **`DEPLOY_DEFERRED`** reason reserved.

### Evidence refs

- `docs/engineering/research.md` (**`R-0094`** — research extension)
- `scripts/sovereign_loop_lib.py` (research stub + `[SOVEREIGN_LOOP_SELF_TEST_OK]`)
- `docs/product/backlog.md` (`## US-0107` — `discovery_notes`)
- `handoffs/po_to_tl.md` (discovery handoff — US-0107)
- `handoffs/intake_evidence/intake-sovereign-20260627-01.json`
- Shipped compose: **US-0110** (`DEC-0110`), **US-0105** (`DEC-0105`), **US-0103** (`DEC-0103`)
- Prior discovery proof: `po-US0107-discovery-20260629T001500Z-fresh`

### Next

- **`/architecture`** (fresh **tech-lead** context) for **`US-0107`** — author **`# US-0107`**, companion **`DEC-0107`**, atomic task seeds, **`test_us0107_*`** literals, runbook § Sovereign Loop Mode.

### Decision gate

- **None** — research satisfied; architecture readiness explicit.

---

## Orchestrated discovery handoff — US-0107 / auto-20260628-04

### Target

- `story_id=US-0107`
- `orchestrator_run_id=auto-20260628-04`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0107-discovery-20260629T001500Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (sovereign-loop batch per intake-sovereign-20260627-01.json)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=5`

### Summary

- **`/discovery`** **PASS** — sovereign loop mode (**`AUTO_SOVEREIGN`**) locked: default-off gate orthogonal to **`full_autonomy`**; four capabilities — **deferral register** (`handoffs/sovereign_deferrals.jsonl`), **drain-generate** (PO spawn + decision gate when backlog empty but not converged), **notification dispatch** (ntfy|email|hook), **convergence hooks** (via **US-0110** `evaluate_convergence`). **Compose do NOT amend** **US-0088** / **US-0092** / **US-0095** — sovereign loop layers on native-chain drain + spawn-only. **US-0109** deploy smoke **out of scope** — integration point declaration only (`DEPLOY_DEFERRED` → register).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (research inputs)

| Lock | Decision |
|------|----------|
| **Scratchpad keys** | `AUTO_SOVEREIGN=0\|1` (default `0`); `AUTO_SOVEREIGN_DEFERRAL_MAX` default `50`; `AUTO_SOVEREIGN_DRAIN_GENERATE_MAX` default `3`; `AUTO_SOVEREIGN_DEFERRAL_POLICY` default `resolve_first`; `SOVEREIGN_NOTIFY_TARGET` default `off` |
| **Deferral register** | `handoffs/sovereign_deferrals.jsonl` JSONL v1 — bounded open rows; `append_deferral` / `resolve_deferral` API |
| **Design intent** | **Deferral** = recoverable block queue; **drain-generate** = PO proposes stories when drained-not-converged; **notification** = terminal event alerts; **convergence hooks** = US-0110 predicate gates loop |
| **Drain-generate** | Trigger: zero OPEN stories + `!converged`; PO spawn with vision + sovereign memory; **decision gate per candidate** before persistence |
| **Notification** | Events: convergence, timeout, deferral cap, drain-generate cap; fail-open dispatch errors |
| **US-0109 compose** | `DEPLOY_DEFERRED` → deferral register (US-0109 implements smoke/retry) |
| **US-0088/92/95 compose** | Layer only — stop matrix, spawn-only, native chain **unchanged** |
| **US-0103 compose** | Optional deferral provenance via `ledger_decision_id`; ledger schema unchanged |
| **US-0105 compose** | Drain-generate reads `build_injection_digest` only |
| **US-0110 compose** | Import `evaluate_convergence` as terminal predicate + drain-generate gate; do not amend DEC-0110 |

### Acceptance pointers (discovery emphasis)

- **AC-1**: Scratchpad keys + zero-overhead when `AUTO_SOVEREIGN=0`; goal-mode coupling when `1`.
- **AC-2**: Deferral register schema + bounded queue.
- **AC-3**: Orchestrator advance + deferral policy behavior.
- **AC-4**: Drain-generate PO spawn + decision gate per candidate.
- **AC-5**: Notification on convergence/timeout/caps; fail-open.
- **AC-6**: US-0109 integration point declaration (no deploy smoke in US-0107).
- **AC-7**: Eight `test_us0107_*` markers + `--scope=sovereign-loop` parity.
- **AC-8**: Backward compat — US-0088/92/95/0044 unchanged when sovereign off.

### Top risks (carry to /research)

- **R1**: Goal-mode coupling — sovereign without `goal_convergence` undefined terminal.
- **R2**: Drain-generate scope creep — decision gate mandatory.
- **R3**: Deferral cap vs convergence `CONVERGENCE_DEFERRALS_PENDING`.
- **R4**: Notification secret handling (hook URLs, ntfy topics).
- **R5**: Sovereign terminal stops vs US-0095 native-chain segments.
- **R6**: US-0109 schema ordering — deferral contract stable first.

### Research asks (new **`R-0094`**)

1. Deferral JSONL v1 schema + validator CLI.
2. `sovereign_loop_lib.py` API + `SovereignLoopStepResult`.
3. Drain-generate PO spawn contract + candidate bundle schema.
4. Notification adapters (ntfy/hook v1; email defer).
5. `AUTO_SOVEREIGN=1` × `SOVEREIGN_GOAL_MODE` coupling.
6. Contract-test inventory + `SOVEREIGN_LOOP_PAIRS` parity.
7. Companion DEC necessity.

### Evidence refs

- `docs/product/backlog.md` (`## US-0107` — `discovery_notes` with L1–L12 + design-intent table)
- `docs/product/vision.md` (**Discovery Notes — US-0107**)
- `docs/product/acceptance.md` (`US-0107` row — unchecked)
- `docs/engineering/research.md` (**`R-0094`** — discovery stub)
- `handoffs/intake_evidence/intake-sovereign-20260627-01.json`
- Shipped compose: **US-0110** (`DEC-0110`, `sovereign_convergence_lib.py`), **US-0105** (`DEC-0105`, `sovereign_memory_lib.py`), **US-0103** (`DEC-0103`, `decision_ledger_lib.py`), **US-0104** (critic)
- Adjacent (do NOT amend): **US-0088**, **US-0092**, **US-0095**, **US-0044**, **US-0069**, **US-0109** (downstream deferral writer)

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0107`** — close **`R-0094`** Q1–Q7; deferral schema + loop lib + drain-generate + notification adapters before **`/architecture`**.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

