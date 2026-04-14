# Sprint S0072

- **Story**: **`US-0088`**
- **Goal**: Ship **continuous story-centric `/auto`** (multi-phase per invocation or **documented outer-driver equivalence** per **`# US-0088`** **AC-1**), **reference Step 5** cross-anchors in **`.cursor/commands/auto.md`** and **`docs/engineering/auto-orchestration-reference.md`**, **`AUTO_QUIET`** default-off quiet contract (**AC-2**) orthogonal to **`TOKEN_PROFILE`**, **`US-0044`** / **`DEC-0022`** drain **recompute** semantics with **contract-test** coverage (**AC-3**, **AC-4**), **`template/`** parity for new keys and touched surfaces (**AC-5**), **`architecture.md`** **`# US-0088`** kept authoritative (**AC-6**), **runbook** operator recipe for continuous **`/auto`** + drain + caps/gates (**AC-7**). **Spawn-only** (**`BUG-0006`**) and **`US-0087`** mutex **by reference only** — per **`docs/engineering/architecture.md`** **`# US-0088`** and **`docs/engineering/research.md`** **`R-0071`**.
- **Status**: **OPEN** — **`sprints/S0072/plan-verify.json`** **`PENDING`** (**`AWAITING_QA_PLAN_VERIFY`**); next **`/plan-verify`** (**qa**, default per **DEC-0051**).

## Scope (sprint-local AC themes)

- **AC-1** - **Spec + command docs**: **`.cursor/commands/auto.md`**, **`docs/engineering/auto-orchestration-reference.md`**, **`docs/engineering/runbook.md`** — **continuous `/auto`** vs **single-turn**; **deterministic stop reasons** vocabulary **unchanged**, semantics for **looping** runs; **reference Step 5** anchor unambiguous vs compact step numbering (**`R-0071`**).
- **AC-2** - **Quiet mode**: operator notifications **only** on **`decision_gate`**, **`error`**, **`pause`**, **`loop_max`**, **`blocked`**, **missing inputs**; document **`AUTO_QUIET`** (and **`TOKEN_PROFILE`** orthogonality); **active + `template/`** parity.
- **AC-3** - **Backlog drain**: one **`/auto`** invocation (or documented equivalent driver) runs **multiple phases** until **US** or **sprint-segment** boundary per **`US-0044`**; **contract tests** prove **drain advance** / phase-depth / story-cursor phrases when policy requires continuation.
- **AC-4** - **Regression tests**: **`tests/auto_command_contract_test.py`** asserts **does not stop after first spawn when policy says continue** + **reference Step 5** alignment; retain **spawn-only** negatives (**`BUG-0006`**).
- **AC-5** - **Template parity** for **new scratchpad keys** (**`AUTO_QUIET`**) and **command/reference excerpts** touched by **US-0088**.
- **AC-6** - **`architecture.md`** **`# US-0088`**: stop matrix, quiet policy, **`US-0044`**, **`US-0087`** mutex, **`US-0037`** / **`DEC-0069`**, **`BUG-0006`** unchanged — reconcile any post-execute drift.
- **AC-7** - **Runbook**: operator recipe — **continuous `/auto`**, **drain**, caps (**`AUTO_BACKLOG_MAX_STORIES`**), pause, gates, quiet flags.

## Governance

- `docs/engineering/architecture.md` `# US-0088`
- `docs/engineering/research.md` `R-0071`
- Related: **`US-0044`**, **`DEC-0022`**, **`US-0045`**, **`US-0037`**, **`DEC-0069`**, **`US-0087`**, **`BUG-0006`**, **`US-0069`**, **`US-0080`**, **`DEC-0062`**
