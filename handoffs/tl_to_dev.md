## TL -> Dev Handoff - Sprint S0064 (US-0083 delegable intake clarification)

## Planning summary

- **Sprint**: **S0064** (next id after **S0063**)
- **Story**: **US-0083** - **Status `OPEN`** (**US-0045** authority in `docs/product/backlog.md`)
- **Task count**: **10** (within **`SPRINT_MAX_TASKS=12`**)
- **AC coverage intent**: **AC-1..AC-10** mapped **1:1** to **`T-001..T-010`** in **`sprints/S0064/tasks.md`**
- **Plan-verify**: **PENDING** (`sprints/S0064/plan-verify.json`; planned **`2026-04-01T01:20:00Z`**, role `tech-lead`) - **`/plan-verify`** required before execute
- **Bounded read**: Load this **S0064** section + **`sprints/S0064/*`** + cited governance only

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (**US-0083** AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (`# US-0083`)
- Decision: `decisions/DEC-0067.md`
- Research: `docs/engineering/research.md` (**R-0062**)
- Related: **US-0068**, **US-0078**, **US-0045**, **DEC-0050**, **DEC-0060**
- Sprint artifacts: `sprints/S0064/*`

## Focus

1. **Adaptive intake behavior (T-001, T-002)**: reduce repetitive prompting through context-aware topic handling and explicit delegation capture.
2. **Validator branch semantics (T-003, T-004, T-005)**: delegated pass path with strict required delegation evidence and unchanged non-delegated fail-closed behavior.
3. **Mode and contract parity (T-006, T-008, T-009)**: guided/low-touch parity, DEC-0060-compatible evidence shape, active/template parity.
4. **Operator guidance and regressions (T-007, T-010)**: update command/runbook/PO guidance and land deterministic delegated/non-delegated regression matrix.

## Risks

- Implicit delegation bypass if explicit topic-scoped opt-in and `ie:` binding are not enforced consistently.
- Drift between `/intake` guidance and validator reason-code behavior can create ambiguous outcomes.
- Active/template parity drift can regress installed-repo behavior for delegation schema support.

## Execution order

Run **`T-001`..`T-010`** in sequence (see **`sprints/S0064/tasks.md`**) after **`/plan-verify`** **PASS**.

## Done criteria for Dev completion

- All **10** tasks in **`sprints/S0064/tasks.md`** marked **done**
- **`sprints/S0064/plan-verify.json`** is **PASS** after **`/plan-verify`** (**QA**) before execute begins
- **`US-0083`** remains **OPEN** until downstream verify-work reconciliation (**US-0045**)

## Next phase

1. **QA**: **`/plan-verify`** for **`S0064`** / **`US-0083`**.

---

## TL -> Dev Handoff — US-0083 (Explicit delegable intake topics) — pre-sprint architecture

## Planning summary

- **Story**: **US-0083** — **Status `OPEN`** (**US-0045** authority in `docs/product/backlog.md`)
- **Architecture**: `docs/engineering/architecture.md` (`# US-0083`)
- **Decision**: `decisions/DEC-0067.md`
- **Research**: `docs/engineering/research.md` (**R-0062**)
- **Orchestrator run**: `auto-20260331-04`
- **Fresh context marker**: `tl-US0083-architecture-20260331T225217Z-fresh`
- **Bounded read**: load US-0083 backlog block + architecture section + DEC only

## Focus for `/sprint-plan`

1. Add tasks to implement `topic_coverage.satisfied_by=delegation_ref` with required fields (`delegation_scope`, `delegation_rationale`, `delegation_confidence`) while preserving DEC-0060 `ie:` binding.
2. Add tasks for deterministic validator branches: delegated pass, delegated malformed/missing fail, and unchanged non-delegated fail-closed path.
3. Add tasks for deterministic diagnostics/remediation using `INTAKE_DELEGATION_EVIDENCE_MISSING` and `INTAKE_DELEGATION_EVIDENCE_INVALID` under `INTAKE_PERSISTENCE_BLOCKED`.
4. Add tasks for guided/low-touch parity and active/template parity across intake command/rules/validator/test surfaces.
5. Add tasks for regression fixtures covering delegated pass, non-delegated block, and delegated invalid-evidence block.

## Risks to plan explicitly

- Implicit bypass risk if delegation is accepted without explicit user evidence binding.
- Contract drift risk between command prose and validator behavior/reason codes.
- Active/template parity drift risk for installed repos.

## Next phase

1. **Tech-lead**: **`/sprint-plan`** for **`US-0083`**.

---

## TL -> Dev Handoff — Sprint S0063 (BUG-0003 installer completeness)

## Planning summary

- **Sprint**: **S0063** (next id after **S0062**)
- **Bug**: **BUG-0003** - **Status `OPEN`** (**US-0045** authority in `docs/product/backlog.md`)
- **Task count**: **10** (within **`SPRINT_MAX_TASKS=12`**)
- **AC coverage intent**: Sprint-local **AC-1..AC-10** mapped **1:1** to **`T-001..T-010`** in **`sprints/S0063/tasks.md`**
- **Plan-verify**: **PASS** (`sprints/S0063/plan-verify.json`; verified **`2026-03-31T21:55:25Z`**, QA, **`auto-20260331-03`**) — **`/execute`** unblocked
- **Bounded read**: Load this **S0063** section + **`sprints/S0063/*`** + cited governance only

## Architecture and decision references

- Bug definition: `docs/product/backlog.md` (**BUG-0003** expected/actual)
- Architecture: `docs/engineering/architecture.md` (`# BUG-0003`)
- Decision: `decisions/DEC-0066.md`
- Research: `docs/engineering/research.md` (**R-0061**)
- Related: **BUG-0001**, **US-0018**, **US-0045**, **DEC-0038**
- Sprint artifacts: `sprints/S0063/*`

## Focus

1. **Inventory + ownership (T-001, T-002)**: manifest-authoritative required inventory and required triad script install/clean pairing.
2. **Invariant + diagnostics (T-003, T-004, T-005, T-006)**: post-install completeness gate with deterministic fail codes and remediation.
3. **Parity + regressions (T-007, T-008, T-009, T-010)**: shared contract across installers, positive/negative matrix, active/template parity, install/clean symmetry.

## Risks

- Manifest drift can silently reintroduce required-script omissions.
- Wrapper-level divergence can desynchronize diagnostics across PS1/SH/PY.
- Install/clean ownership asymmetry can create stale files or unintended cleanup.

## Execution order

Run **`T-001`..`T-010`** in sequence (see **`sprints/S0063/tasks.md`**) after **`/plan-verify`** **PASS**.

## Done criteria for Dev completion

- All **10** tasks in **`sprints/S0063/tasks.md`** marked **done**
- **`sprints/S0063/plan-verify.json`** is **PASS** after **`/plan-verify`** (**QA**)
- **`BUG-0003`** remains **OPEN** until downstream verify-work reconciliation (**US-0045**)

## Next phase

1. **Dev**: **`/execute`** for **`S0063`** / **`BUG-0003`** (plan-verify **PASS** recorded).

---

## TL -> Dev Handoff — BUG-0003 (installer completeness) — pre-sprint architecture

## Planning summary

- **Bug**: **BUG-0003** — **Status `OPEN`** (canonical authority: `docs/product/backlog.md`, per **US-0045**)
- **Architecture**: `docs/engineering/architecture.md` (`# BUG-0003`)
- **Decision**: `decisions/DEC-0066.md`
- **Research**: `docs/engineering/research.md` (**R-0061**)
- **Bounded read**: load BUG-0003 backlog block + architecture section + DEC only

## Focus for `/sprint-plan`

1. Add tasks for required-script inventory contract in `docs/engineering/context/installer-owned-paths.manifest`, including `scripts/enforce-triad-hot-surface.py`.
2. Add tasks for deterministic post-install completeness validation and stable reason-code surface (`INSTALL_COMPLETENESS_FAILED`, `INSTALL_REQUIRED_SCRIPT_MISSING:<path>`).
3. Add tasks for parity-safe implementation across `installer.ps1`, `installer.sh`, and `installer.py` (shared validator path preferred).
4. Add tasks for positive/negative test matrix in `missing` and `upgrade`, plus active/template parity and install/clean symmetry checks.
5. Add tasks for runbook/operator remediation text tied to deterministic diagnostics.

## Risks to plan explicitly

- Manifest drift can silently reintroduce required-script omissions.
- Wrapper parity drift can diverge diagnostics across platforms if checks are duplicated.
- Install/clean asymmetry can leave stale files or remove non-owned paths.

## Next phase

1. **Tech-lead**: **`/sprint-plan`** for **`BUG-0003`**.

---

## TL -> Dev Handoff — Sprint S0062 (US-0082 — Agent-driven codebase map bootstrap)

## Planning summary

- **Sprint**: **S0062** (next id after **S0061**)
- **Story**: **US-0082** — **Status `OPEN`** (**US-0045** authority in `docs/product/backlog.md`)
- **Task count**: **10** (within **`SPRINT_MAX_TASKS=12`**)
- **AC coverage intent**: **AC-1..AC-10** mapped **1:1** to **`T-001..T-010`** in **`sprints/S0062/tasks.md`**
- **Plan-verify**: **PASS** (`sprints/S0062/plan-verify.json`; verified **`2026-03-31T20:20:00Z`**, QA, **`auto-20260331-02`**) — **`/execute`** unblocked
- **Bounded read**: Load this **S0062** section + **`sprints/S0062/*`** + cited governance only

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (**US-0082** AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (`# US-0082`)
- Decision: `decisions/DEC-0065.md`
- Research: `docs/engineering/research.md` (**R-0060**)
- Related: **US-0001**, **BUG-0002**, **DEC-0052**, **US-0045**
- Sprint artifacts: `sprints/S0062/*`

## Focus (after plan-verify PASS)

1. **Lifecycle (T-001, T-002, T-003)**: **`/architecture`**-exit map guarantee, operator docs for manual vs auto path, idempotent refresh.
2. **Policy + diagnostics (T-004, T-005, T-006)**: ownership-safe writes, **`CODEBASE_MAP_*`** vocabulary, runbook + **`/ask`**.
3. **Parity + quality (T-007, T-008, T-009)**: active/template parity, regression matrix, existing-map compatibility.
4. **Traceability (T-010)**: **BUG-0002** closure/reclassification with backlog alignment.

## Risks

- **DEC-0052** profiles skipping **`architecture`** — mitigate per **DEC-0065** diagnostics / optional CI follow-up.
- **Merge/idempotency** semantics — avoid destructive overwrites of operator-customized maps.

## Execution order

Run **`T-001`..`T-010`** in sequence (see **`sprints/S0062/tasks.md`**) after **`/plan-verify`** **PASS**.

## Done criteria for Dev completion

- All **10** tasks in **`sprints/S0062/tasks.md`** marked **done**
- **`sprints/S0062/plan-verify.json`** is **PASS** after **`/plan-verify`** (**QA**) before execute begins
- **`US-0082`** remains **OPEN** until downstream verify-work reconciliation (**US-0045**)

## Next phase

1. **Dev**: **`/execute`** for **`S0062`** / **`US-0082`** (plan-verify **PASS** recorded).

---

## TL -> Dev Handoff — US-0082 (Agent-driven codebase map bootstrap) — pre-sprint architecture (reference)

## Planning summary

- **Story**: **US-0082** — **Status `OPEN`** (**US-0045** authority in `docs/product/backlog.md`)
- **Architecture**: **`docs/engineering/architecture.md`** (`# US-0082`)
- **Decision**: **`decisions/DEC-0065.md`**
- **Research**: **`docs/engineering/research.md`** (**R-0060**)
- **Bounded read**: load US-0082 backlog block + architecture section + DEC only

## Note

Sprint execution baton: see **Sprint S0062** section above (**`sprints/S0062/*`**).

---

## TL -> Dev Handoff — Sprint S0061 (US-0081 First-intake full-plan coverage gate)

## Planning summary

- **Sprint**: **S0061** (next id after **S0060**)
- **Story**: **US-0081** - **Status `OPEN`** (**US-0045** authority in `docs/product/backlog.md`)
- **Task count**: **10** (within **`SPRINT_MAX_TASKS=12`**)
- **AC coverage intent**: **AC-1..AC-10** mapped **1:1** to **`T-001..T-010`** in **`sprints/S0061/tasks.md`**
- **Plan-verify**: **PASS** (`sprints/S0061/plan-verify.json`; `2026-03-31T12:15:00Z`, role `qa`) - **`/execute`** unblocked
- **Bounded read**: Load this **S0061** section + **`sprints/S0061/*`** + cited governance only

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (**US-0081** AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (`# US-0081`)
- Decision: `decisions/DEC-0064.md`
- Research: `docs/engineering/research.md` (**R-0059**)
- Related: **US-0051**, **US-0068**, **US-0078**, **US-0045**
- Sprint artifacts: `sprints/S0061/*`

## Focus

1. **Coverage inventory (T-001, T-002)**: normalize major plan areas and enforce total mapping/defer accounting.
2. **Story-map integrity (T-003, T-004)**: complete mapping output while preserving vertical-slice decomposition guardrails.
3. **Mode parity + contract fields (T-005, T-006, T-009)**: low-touch enforcement and active/template parity for command/rules/validators/tests.
4. **Diagnostics + guidance (T-007, T-008)**: deterministic fail codes and operator remediation in `/ask` + runbook.
5. **Regression closure (T-010)**: pass/fail/defer matrix with guided and low-touch coverage.

## Risks

- **Over/under-normalization** of plan areas can cause false blocks or silent merges.
- **Policy/validator drift** can desynchronize prose guidance from fail-closed enforcement.
- **Template parity drift** can regress first-intake behavior in installed repos.

## Execution order

Run **`T-001`..`T-010`** in sequence (see **`sprints/S0061/tasks.md`**). Land data-contract fields and diagnostics before docs/tests closure.

## Done criteria for Dev completion

- All **10** tasks in **`sprints/S0061/tasks.md`** marked **done**
- **`sprints/S0061/plan-verify.json`** is **PASS** after **`/plan-verify`** (**QA**) before execute begins
- **`US-0081`** remains **OPEN** until downstream verify-work reconciliation (**US-0045**)

## Next phase

1. **Dev**: **`/execute`** for **`S0061`** / **`US-0081`**.

---

## TL -> Dev Handoff — US-0081 (First-intake full-plan coverage gate) — pre-sprint architecture

## Planning summary

- **Story**: **US-0081** - **Status `OPEN`** (**US-0045** authority in `docs/product/backlog.md`)
- **Architecture**: **`docs/engineering/architecture.md`** (`# US-0081`)
- **Decision**: **`decisions/DEC-0064.md`**
- **Research**: **`docs/engineering/research.md`** (**R-0059**)
- **Bounded read**: load US-0081 backlog block + architecture section + DEC only

## Focus for `/sprint-plan`

1. Add tasks for deterministic first/new/broad trigger and normalized `plan_area_inventory`.
2. Add tasks for total coverage mapping (`plan_area_id -> story_ids[] | deferred_ref`) and validator invariants.
3. Add tasks for fail-closed diagnostics under `INTAKE_PERSISTENCE_BLOCKED` with DEC-0064 subcodes.
4. Add tasks for pass/fail/defer fixtures, guided/low-touch enforcement, and active/template parity checks.
5. Add tasks for `/ask` and runbook guidance updates tied to remediation text.

## Risks to plan explicitly

- Over-blocking from poor major-area normalization.
- Contract drift between prose intake notes and validator output.
- Template parity drift for intake command/rules/tests.

## Next phase

1. **Tech-lead**: **`/sprint-plan`** for **`US-0081`**.

---

## TL -> Dev Handoff — Sprint S0060 (BUG-0001 Intake script install completeness)

> **Execute complete** **`2026-03-30`** (`orchestrator_run_id=auto-20260330-01`) — see **`docs/engineering/state.md`** **Execute checkpoint**; **`handoffs/dev_to_qa.md`**; **`sprints/S0060/summary.md`**. Next: **`/qa`**. **`BUG-0001`** **OPEN** until **`/verify-work`**.

## Planning summary

- **Sprint**: **S0060** (next id after **S0059**)
- **Bug**: **BUG-0001** — **Status `OPEN`** (**US-0045**); **`docs/product/acceptance.md`** **`BUG-0001`** row **unchecked** until **`/verify-work`**
- **Task count**: **5** (within **`SPRINT_MAX_TASKS=12`**)
- **AC coverage intent**: Sprint-local **AC-1..AC-5** (see **`sprints/S0060/sprint.md`**) mapped **1:1** to **`T-001..T-005`** in **`sprints/S0060/tasks.md`** — decomposes backlog **expected** + **`DEC-0063`**
- **Plan-verify**: **PASS** (`sprints/S0060/plan-verify.json`; **qa**, **`2026-03-30T23:55:00Z`**, `orchestrator_run_id=auto-20260330-01`) — **`/execute`** unblocked
- **Bounded read**: Load **S0060** section + **`sprints/S0060/*`** + cited paths only

## Architecture and decision references

- Bug definition: `docs/product/backlog.md` (**BUG-0001**)
- Architecture: `docs/engineering/architecture.md` (`# BUG-0001`)
- Decision: `decisions/DEC-0063.md`
- Research: `docs/engineering/research.md` (**R-0058**)
- Related: **US-0008**, **US-0018**, **DEC-0061**, **US-0030**
- Sprint artifacts: `sprints/S0060/*`

## Focus

1. **Mirror + manifest (T-001, T-002)**: **`template/scripts/`** intake trio; **`package.json` `files`** per **§2**
2. **Parity gate (T-003)**: CI-friendly **`scripts/`** ↔ **`template/scripts/`** check
3. **Upgrade (T-004)**: **`US-0018`** classification + fresh/upgrade evidence
4. **Ops (T-005)**: README/runbook + triple-installer consistency

## Risks

- **Copy drift** — T-003 parity; single-PR expectation for dual-tree edits
- **Upgrade misses files** — T-004 matrix + **`US-0018`** hooks

## Execution order

Run **`T-001`..`T-005`** in sequence (see **`sprints/S0060/tasks.md`**). Establish mirror before parity tests; upgrade evidence after files land.

## Done criteria for Dev completion

- All **5** tasks in **`sprints/S0060/tasks.md`** marked **done**
- **`sprints/S0060/plan-verify.json`** **PASS** after **`/plan-verify`** (**QA**)
- **`BUG-0001`** remains **OPEN** until **`/verify-work`** reconciles **`acceptance.md`**

## Next phase

1. **Dev**: **`/execute`** for **`S0060`** / **`BUG-0001`** — see **`handoffs/resume_brief.md`**, **`sprints/S0060/tasks.md`** (plan-verify **PASS**)

---

## TL -> Dev Handoff — Sprint S0059 (US-0080 Token-Cost Hardening)

## Planning summary

- **Sprint**: **S0059** (next id after **S0058**)
- **Story**: **US-0080** — Token-cost hardening — **Status `OPEN`** until delivery (**US-0045**)
- **Task count**: **10** (within **`SPRINT_MAX_TASKS=12`**)
- **AC coverage intent**: **AC-1..AC-10** mapped **1:1** to **`T-001..T-010`** in **`sprints/S0059/tasks.md`**
- **Plan-verify**: **PASS** (`sprints/S0059/plan-verify.json`; **qa**, **`2026-03-29T21:00:00Z`**, `orchestrator_run_id=auto-20260329-02`) — **`/execute`** unblocked.
- **Bounded read (`DEC-0062` §4)**: Load this **S0059** section + **`sprints/S0059/*`** + cited paths only; historical sprint sections below are archive — do not pull entire `tl_to_dev.md` into working context unless tasked.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0080 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (`# US-0080`)
- Decision: `decisions/DEC-0062.md`
- Research: `docs/engineering/research.md` (**R-0057**)
- Related: **DEC-0052** (run class / phase plan), **US-0053** (token profile), **US-0030** (parity), **US-0048**, **US-0056**, **US-0069**, **US-0039**
- Sprint artifacts: `sprints/S0059/*`

## Focus

1. **Metrics + comparability (T-001, T-002)**: **`DEC-0062`** §1 fields; **`run_class_hash`**; **50%** `cache_read_tokens` on comparable runs; **`TOKEN_COST_RUN_CLASS_MISMATCH`**.
2. **Slimming + parity (T-003, T-004, T-009)**: command surfaces; bounded phase context; versioned manifest + CI.
3. **Gates unchanged (T-005)**: **`/auto`** isolation / strict-proof / role / release semantics preserved.
4. **Evidence + ops (T-006, T-007)**: **`handoffs/token_cost_runs/*`**; **`token_cost_evidence_ref`**; README/runbook.
5. **Tests + closure (T-008, T-010)**: regressions; decisions index + operator citations.

## Risks

- **Over-slimming** — AC-8 + runbook deep links (**DEC-0062** §6).
- **Baseline gaming** — strict **`run_class_hash`** rule.
- **Template drift** — manifest + CI.

## Execution order

Run **`T-001`..`T-010`** in sequence (see **`sprints/S0059/tasks.md`**). Establish metric capture and **`run_class_hash`** before claiming AC-2; manifest early for T-003/T-009.

## Done criteria for Dev completion

- All **10** tasks in **`sprints/S0059/tasks.md`** marked done.
- **`sprints/S0059/plan-verify.json`** **PASS** after **`/plan-verify`** (QA) with no AC gaps.
- Lifecycle evidence in **`docs/engineering/state.md`** for **`US-0080`** / **`S0059`** per repo convention.

## Next phase

1. **Dev**: **`/execute`** for **`S0059`** / **`US-0080`** — plan-verify **PASS**; see **`docs/engineering/state.md`** plan-verify checkpoint + **`handoffs/resume_brief.md`**.
2. **QA**: **`/qa`** after dev delivery per lifecycle.

---

## TL -> Dev Handoff — US-0080 (Token-Cost Hardening) — pre-sprint architecture (historical)

> **Superseded** by **Sprint S0059** above. Retained as architecture-only tail anchor.

### Planning summary

- **Story**: **US-0080** — **Status `OPEN`** (**US-0045**)
- **Architecture**: **`docs/engineering/architecture.md`** (`# US-0080`)
- **Decision**: **`decisions/DEC-0062.md`**
- **Research**: **`docs/engineering/research.md`** (**R-0057**)

### Next phase (current)

1. **Dev**: **`/execute`** for **`S0059`** / **`US-0080`** (plan-verify **PASS**).

---

## TL -> Dev Handoff — Sprint S0058 (US-0079 First-Class Bug Issues)

## Planning summary

- **Sprint**: **S0058** (next id after **S0057**)
- **Story**: **US-0079** — First-class bug issue workflow (`BUG-####`, **`OPEN`/`DONE`**) — **Status `OPEN`** until delivery (**US-0045**)
- **Task count**: **10** (within **`SPRINT_MAX_TASKS=12`**)
- **AC coverage intent**: **AC-1..AC-10** mapped **1:1** to **`T-001..T-010`** in **`sprints/S0058/tasks.md`**
- **Plan-verify**: **PASS** (`sprints/S0058/plan-verify.json`; QA **`2026-03-29`**, `orchestrator_run_id=auto-20260329-01`) — **`/execute`** unblocked.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0079 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (`# US-0079`)
- Decision: `decisions/DEC-0061.md`
- Research: `docs/engineering/research.md` (**R-0056**)
- Related: **US-0045** (status authority), **US-0042** (release-issue traceability style), **DEC-0055** (**`INTAKE_WORK_ITEM_KIND`**), **US-0030** (parity), **US-0070** (optional **`bug_ids`** on phase boundaries)
- Sprint artifacts: `sprints/S0058/*`

## Focus

1. **Identity + storage (T-001)**: **`BUG-####`** allocator; **`## Bug issues (canonical)`**; sort discipline (**DEC-0061** §§1–2).
2. **Routing (T-002)**: scratchpad + **`/intake bug`**; **`INTAKE_BUG_ROUTING_REQUIRED`** / mismatch family; no silent **`US-xxxx`** for defects.
3. **Lifecycle + schema (T-003, T-004)**: **`OPEN`/`DONE`** only; minimum reproducibility fields + **`BUG_VALIDATION_*`**.
4. **Traceability (T-005, T-006)**: sprint + QA/UAT/release rows may cite **`BUG-xxxx`** (**US-0042** pattern).
5. **Reconciliation + surfaces (T-007, T-008)**: extend **`US-0045`** guards; **`/ask`** allowlists.
6. **Parity + closure (T-009, T-010)**: **`template/`** mirrors; decisions index + operator citations for **DEC-0061** / **`# US-0079`**.

## Risks

- **Duplicate US+BUG** — **`duplicate_of`/`supersedes`** + routing fail-closed (**DEC-0061**).
- **Validator drift** — single module + **R-0056** Tier A fixtures.
- **Reconciliation regressions** — extend US-0045 without weakening US-only paths.

## Execution order

Run **`T-001`..`T-010`** in sequence (see **`sprints/S0058/tasks.md`**). Implement allocator + backlog section before intake routing; validator before broad doc edits.

## Done criteria for Dev completion

- All **10** tasks in **`sprints/S0058/tasks.md`** marked done.
- **`sprints/S0058/plan-verify.json`** **PASS** after **`/plan-verify`** (QA) with no AC gaps.
- Lifecycle evidence in **`docs/engineering/state.md`** for **`US-0079`** / **`S0058`** per repo convention.

## Next phase

1. **Dev**: **`/execute`** for **`S0058`** / **`US-0079`** (plan-verify **PASS** recorded).

---

## TL -> Dev Handoff — Sprint S0057 (US-0078 Enforced Interactive Intake Question Evidence)

## Planning summary

- **Sprint**: **S0057** (new; next id after **S0056**)
- **Story**: **US-0078** — Runtime enforcement of intake question-pack evidence (**`DEC-0060`**, **`R-0055`**, **`DEC-0050`** packs; architecture **`# US-0078`**)
- **Task count**: **10** (within **`SPRINT_MAX_TASKS=12`**)
- **AC coverage intent**: **AC-1..AC-10** mapped **1:1** to **`T-001..T-010`** in **`sprints/S0057/tasks.md`**
- **Plan-verify**: **PASS** (`sprints/S0057/plan-verify.json`; QA **`2026-03-28`**, `orchestrator_run_id=auto-20260328-01`) — **`/execute`** unblocked.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0078 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (`# US-0078`)
- Decisions: `decisions/DEC-0060.md` (extends `decisions/DEC-0050.md`)
- Research: `docs/engineering/research.md` (**R-0055**)
- Related: **US-0068** (pack fields), **US-0033** (guided vs low-touch), **US-0030** (parity)
- PO → TL handoff: `handoffs/po_to_tl.md` (US-0078 addenda / tail mirrors under **`auto-20260328-01`**)
- Sprint artifacts: `sprints/S0057/*`

## Focus

1. **Coverage + refs (T-001)**: **`topic_coverage`** rows + **`ie:`** binding; required keys from **`selected_pack`**.
2. **Assumptions (T-002)**: literal **`assumptions_confirmed`** vs **`assumption_confirmation_ref`**; **`INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`**.
3. **Gate ordering (T-003, T-004)**: validate-then-write; persist **`asked_topics`** vs covered keys audibly.
4. **Modes (T-005, T-006)**: same validator for guided and **`INTAKE_GUIDED_MODE=0`**; no low-touch bypass.
5. **Operator UX (T-007)**: missing-topic diagnostics and remediation prompts.
6. **Evidence (T-008..T-010)**: **`R-0055`** regression matrix; active/template parity; **DEC-0060** / architecture traceability in operator docs and decisions index.

## Risks

- **`ie:`** parser drift — single module + **AC-8** golden vectors (**architecture.md**).
- **Grandfathered legacy** intake rows — read-only until next mutation; tests must not treat legacy as write **PASS** without full evidence (**DEC-0060** §5).
- **Friction in low-touch** — mitigate with **AC-7** targeted diagnostics; preserve mandatory coverage invariant.

## Execution order

Run tasks **`T-001`..`T-010`** in sequence (see **`sprints/S0057/tasks.md`**). Implement shared validation module before persistence wiring.

## Done criteria for Dev completion

- All **10** tasks in **`sprints/S0057/tasks.md`** marked done.
- **`sprints/S0057/plan-verify.json`** **PASS** after **`/plan-verify`** (QA) with no AC gaps.
- **`sprints/S0057/progress.md`**, **`sprints/S0057/uat.json`**, and **`sprints/S0057/uat.md`** updated with implementation evidence (during execute/QA per repo convention).
- **`docs/engineering/state.md`** includes lifecycle checkpoint traceability for **`US-0078`** / **`S0057`**.

## Next phase

**`/execute`** for **`S0057`** / **`US-0078`** — plan-verify **PASS** recorded in **`sprints/S0057/plan-verify.json`** and **`docs/engineering/state.md`**.

---

## TL -> Dev Handoff — Sprint S0056 (US-0077 Documentation Profiles + Dual README)

## Planning summary

- **Sprint**: S0056 (new; next id after **`S0055`** release)
- **Story**: US-0077 — Documentation audience profiles and dual README strategy (**`DEC-0059`**; merged scratchpad **`DEC-0055`**; research **`R-0054`**)
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped 1:1 to `T-001..T-010` in `sprints/S0056/tasks.md`
- **Plan-verify**: **PASS** (`sprints/S0056/plan-verify.json`; `orchestrator_run_id=auto-20260327-02`) — QA confirmed AC-1..AC-10 ↔ T-001..T-010 vs backlog + **DEC-0059**; no plan gaps before **`/execute`**.
- **Verify-work / release readiness** (**2026-03-28**): **`sprints/S0056/uat.json`** / **`sprints/S0056/uat.md`** **PASS** (`10/10`); **`docs/product/backlog.md`** **US-0077** **DONE**; **`handoffs/release_queue.md`** row **`S0056`** → **`ready`**; next phase **`/release`** (see **`docs/engineering/state.md`** verify-work checkpoint).

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0077 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (`# US-0077`)
- Decision: `decisions/DEC-0059.md` (profile semantics, dual file split, H2 literals, validator path, migration)
- Related: **US-0030** (parity), **US-0031** / **US-0032** (optional modes), **US-0071** (user-visible hygiene), **DEC-0058** pattern for merged scratchpad read in validator
- Research: `docs/engineering/research.md` (**R-0054**)
- PO → TL handoff: `handoffs/po_to_tl.md` (US-0077 addenda / tail mirror under **`auto-20260327-02`**)
- Sprint artifacts: `sprints/S0056/*`

## Focus

1. **Profile inputs + fail-closed (T-001)**: scratchpad keys, enums, merge errors; template ships explicit values; transition default per **DEC-0059** §6.
2. **Generation idempotence (T-002, T-003)**: profile drives README + developer shard content; `USER_*` vs `DEV_*` H2 table in architecture.
3. **Split + optional modes (T-004, T-005)**: **DEC-0059** §3 layout; **SPEC_PACK_MODE** / **USER_GUIDE_MODE** gating.
4. **Validator + parity (T-006, T-007)**: **`scripts/validate_doc_profile.py`**; runbook/README/template; **`installer-owned-paths.manifest`** for **`docs/developer/README.md`**.
5. **Evidence (T-008..T-010)**: Tier A/B/C tests; **US-0071** scan; **DEC-0059** traceability in operator docs and decisions index.

## Risks

- **Heading drift** vs semantic keys — mitigate with validator + fixture snapshots (**AC-6**, **AC-8**).
- **Optional-mode false failures** — explicit flag-off fixtures in **T-005** / **T-008**.
- **New developer shard path** — must stay framework-owned per manifest (**T-007**).

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0056/tasks.md`). Implement merged-scratchpad read once (installer merge helper) before splitting README content.

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0056/tasks.md` marked done.
- `sprints/S0056/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps (**PASS** — see plan-verify checkpoint in `docs/engineering/state.md`).
- `sprints/S0056/progress.md`, `sprints/S0056/uat.json`, and `sprints/S0056/uat.md` updated with implementation evidence (during execute/QA as per repo convention).
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0077` / `S0056`.

## Next phase

**`/execute`** for **`S0056`** / **`US-0077`** (plan-verify **PASS** recorded in `sprints/S0056/plan-verify.json` and `docs/engineering/state.md`).

---

## TL -> Dev Handoff — Sprint S0055 (US-0076 Executable Scratchpad Sync / Auto-Push Wiring)

## Planning summary

- **Sprint**: S0055 (new)
- **Story**: US-0076 — Executable scratchpad-driven sync and auto-push wiring (**validate-and-push** + merged scratchpad per **DEC-0055**; policy authority **DEC-0018** / **US-0038**; executable contract **DEC-0058**)
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped 1:1 to `T-001..T-010` in `sprints/S0055/tasks.md`
- **Plan-verify**: **PASS** (`sprints/S0055/plan-verify.json`; `orchestrator_run_id=auto-20260327-01`) — QA confirmed full AC↔task coverage vs backlog + **DEC-0058**; no plan gaps before **`/execute`**.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0076 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (`# US-0076`)
- Decisions: `decisions/DEC-0058.md` (executable wiring; **DEC-0018** remains policy authority); **DEC-0055** (merge precedence)
- Related: **US-0038** (gate chain / reason codes), **US-0071** (operator string hygiene)
- Research: `docs/engineering/research.md` (**R-0053**)
- PO → TL handoff: `handoffs/po_to_tl.md` (US-0076 addenda / tail mirrors under `auto-20260327-01`)
- Sprint artifacts: `sprints/S0055/*`

## Focus

1. **Merge + policy gates (T-001, T-002)**: single merge source; fail closed; short-circuit when auto-push off or manual/disabled.
2. **Pre-push chain (T-003..T-005)**: runbook tests → optional checks → branch allowlist → bounded **qa-findings** scan + **PRE_QA_AUTOPUSH_FORBIDDEN** per runbook.
3. **Parity + docs (T-006, T-007)**: PS1/sh alignment; runbook **SYNC_PHASE_BOUNDARY**, dry-run, scheduling; README + **template/**.
4. **Verification (T-008..T-010)**: regression tests; **US-0071** scan; **DEC-0058** / deprecation surfaced in operator docs.

## Risks

- **False allow / false block** from QA glob or regex — mitigate with **AC-8** fixtures and runbook examples (**DEC-0058** consequences).
- **Python merge dependency** on push path — acceptable vs duplicated precedence; ensure clear errors on missing interpreter.
- **Phase eligibility** ambiguity — default **invocation = boundary**; document **SYNC_PHASE_BOUNDARY** for CI only (**DEC-0058** §4).

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0055/tasks.md`). Prefer implementing shared merge invocation before branching-specific logic.

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0055/tasks.md` marked done.
- `sprints/S0055/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps (**PASS** after `/plan-verify`).
- `sprints/S0055/progress.md`, `sprints/S0055/uat.json`, and `sprints/S0055/uat.md` updated with implementation evidence (during execute/QA as per repo convention).
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0076` / `S0055`.

## Next phase

Plan-verify **PASS** for **`S0055`** (`sprints/S0055/plan-verify.json`). Proceed to **`/execute`** for **`S0055`** (`US-0076`).

---

## TL -> Dev Handoff — Sprint S0054 (US-0075 Scratchpad Example–First Refresh + AC-11)

## Planning summary

- **Sprint**: S0054 (new)
- **Story**: US-0075 — Upgrade scratchpad **example–first** refresh (fix example drift vs materialized baseline) + **AC-11** paired key/section parity
- **Task count**: 11 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-11 mapped 1:1 to `T-001..T-011` in `sprints/S0054/tasks.md`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0075 AC-1..AC-11)
- Architecture: `docs/engineering/architecture.md` (`# US-0075`)
- Decision: `decisions/DEC-0057.md` (**example-first ordering + paired catalog parity / AC-11** — amends operational reading of **DEC-0039** relative to baseline refresh; **DEC-0055** merge precedence unchanged)
- Related: **DEC-0039** (framework example refresh + user-local preservation), **DEC-0055** (Model B), **US-0057** / **US-0073** (prior contracts)
- Research: `docs/engineering/research.md` (`R-0052`, post-discovery US-0075)
- PO -> TL handoff: `handoffs/po_to_tl.md` (Discovery Addendum — US-0075)
- Sprint artifacts: `sprints/S0054/*`

## Focus

1. **Ordering + refresh (T-001..T-003)**: **DEC-0057** example-first invariant; upgrade/install always refreshes **scratchpad.local.example**; no stale example while materialized baseline moves.
2. **Parity surfaces (T-004, T-008)**: PS1/SH/py/CLI + **`installer-owned-paths.manifest`** (+ **`template/`** mirror).
3. **Diagnostics + docs (T-005, T-007, T-010)**: layer attribution (**DEC-0039**); README/runbook; drift remediation.
4. **Tests + QA + AC-11 (T-006, T-009, T-011)**: regression matrix for example lag; QA evidence; machine **##** + **`KEY=`** paired parity in **`tests/run-tests.*`**.

## Execution order

Run tasks `T-001`..`T-011` in sequence (see `sprints/S0054/tasks.md`).

## Done criteria for Dev completion

- All 11 tasks in `sprints/S0054/tasks.md` marked done.
- `sprints/S0054/plan-verify.json` confirms AC-1..AC-11 coverage with no gaps (**PASS** after `/plan-verify`).
- `sprints/S0054/progress.md`, `sprints/S0054/uat.json`, and `sprints/S0054/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0075` / `S0054`.

## Next phase

Proceed to **`/plan-verify`** for **`S0054`** (`US-0075`). `sprints/S0054/plan-verify.json` is currently a **PENDING** sprint-plan seed.

---

## TL -> Dev Handoff — Sprint S0053 (US-0074 Baseline Regression Cleanup)

## Planning summary

- **Sprint**: S0053 (new)
- **Story**: US-0074 — Baseline regression cleanup for installer and version sync checks
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped 1:1 to `T-001..T-010` in `sprints/S0053/tasks.md`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0074 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (`# US-0074`)
- Decision: `decisions/DEC-0056.md` (**baseline version-sync + `TEST_COMMAND` bootstrap** — npm-canonical version ↔ Homebrew stable formula; installer + CLI runbook bootstrap; triple-installer + template parity; PowerShell runner widening explicitly out of scope)
- Related: `DEC-0046` (runbook `TEST_COMMAND` bootstrap precedence), `US-0018` / `US-0057` / `US-0063` (ownership / upgrade contracts)
- Research: `docs/engineering/research.md` (`R-0051`, post-discovery US-0074)
- PO -> TL handoff: `handoffs/po_to_tl.md` (Discovery Addendum — US-0074)
- Sprint artifacts: `sprints/S0053/*`

## Focus

1. **Classification + Homebrew (T-001..T-002)**: deterministic RCA for the four baseline asserts; align `packaging/homebrew/its-magic.rb` with `package.json` / tag URL / checksum discipline.
2. **TEST_COMMAND bootstrap (T-003..T-005)**: fix installer + CLI missing-install paths so materialized runbook meets baseline-allowed values; preserve ownership contracts; PS1/SH/py/CLI parity.
3. **Evidence + parity (T-006..T-009)**: strengthen tests without masking; QA shows zero remaining four-check failures; active/`template/` parity; release/readiness artifacts cite passing baseline.
4. **Operator guidance (T-010)**: document remediation for future version/bootstrap drift.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0053/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0053/tasks.md` marked done.
- `sprints/S0053/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps (**PASS** after `/plan-verify`).
- `sprints/S0053/progress.md`, `sprints/S0053/uat.json`, and `sprints/S0053/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0074` / `S0053`.

## Next phase

Proceed to **`/plan-verify`** for **`S0053`** (`US-0074`). `sprints/S0053/plan-verify.json` is currently a **PENDING** sprint-plan seed.

---

## TL -> Dev Handoff — Sprint S0052 (US-0073 Scratchpad Delivery Simplification / Model B)

## Planning summary

- **Sprint**: S0052 (new)
- **Story**: US-0073 — Scratchpad delivery simplification (example-only install policy)
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped 1:1 to `T-001..T-010` in `sprints/S0052/tasks.md`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0073 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0073 section)
- Decision: `decisions/DEC-0055.md` (**Model B** — example-only + materialized baseline; merge precedence; parity; fail-closed diagnostics)
- Related: `DEC-0039` (scratchpad example refresh + ownership), `US-0018` / `US-0057` (upgrade + scratchpad contracts)
- Research: `docs/engineering/research.md` (`R-0050`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (Discovery Addendum — US-0073)
- Sprint artifacts: `sprints/S0052/*`

## Focus

1. **Policy + materialization (T-001..T-002)**: document and enforce **`DEC-0055`** delivery model; loaders/commands never silently infer missing required keys.
2. **Upgrade + fail-closed merge (T-003..T-005)**: upgrade preserves user local; invalid/missing baseline states fail with layer attribution and remediation.
3. **Parity + docs (T-006..T-008)**: installer surfaces + CLI + `template/` alignment; README + runbook for operators.
4. **Regression + traceability (T-009..T-010)**: install/upgrade/missing-file/local-override matrix; explicit overlap resolution with **`US-0018`** / **`US-0057`** and automation safety defaults.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0052/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0052/tasks.md` marked done.
- `sprints/S0052/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps (**PASS** after `/plan-verify`).
- `sprints/S0052/progress.md`, `sprints/S0052/uat.json`, and `sprints/S0052/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0073`.

## Next phase

Proceed to **`/plan-verify`** for **`S0052`** (`US-0073`). `sprints/S0052/plan-verify.json` is currently a **PENDING** sprint-plan seed.

---

## TL -> Dev Handoff — Sprint S0051 (US-0072 Deterministic Context Slimming + Triad Archive Enforcement)

## Planning summary

- **Sprint**: S0051 (new)
- **Story**: US-0072 — Deterministic context slimming and archive enforcement across core artifacts
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped 1:1 to `T-001..T-010` in `sprints/S0051/tasks.md`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0072 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0072 section)
- Decision: `decisions/DEC-0054.md`
- Research: `docs/engineering/research.md` (`R-0047`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (Discovery Addendum — US-0072)
- Sprint artifacts: `sprints/S0051/*`

## Focus

1. **Triad contract (T-001)**: hot/archive paths, scratchpad keys, pack naming for `state.md`, `po_to_tl.md`, `architecture.md`.
2. **Rollover + gates (T-002..T-004)**: same-phase rollover or fail-closed; verification tuple + idempotency; `/refresh-context` and mutating phases cannot skip archive proof.
3. **Read minimization (T-005..T-007)**: minimal-read sets with budgets; compact pointers; reason-code taxonomy.
4. **Safety + parity + regression (T-008..T-010)**: auditable archives, active/template docs, tests for threshold, empty-archive, idempotence, bounded reads, fail-safe.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0051/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0051/tasks.md` marked done.
- `sprints/S0051/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps (**PASS** after `/plan-verify`).
- `sprints/S0051/progress.md`, `sprints/S0051/uat.json`, and `sprints/S0051/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0072`.

## Next phase

Proceed to **`/plan-verify`** for **`S0051`** (`US-0072`). `sprints/S0051/plan-verify.json` is currently a **PENDING** sprint-plan seed.

---

## TL -> Dev Handoff — Sprint S0050 (US-0071 User-Visible Internal Metadata Sanitization Guard)

## Planning summary

- **Sprint**: S0050 (new)
- **Story**: US-0071 — User-visible internal metadata sanitization guard
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped 1:1 to `T-001..T-010` in `sprints/S0050/tasks.md`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0071 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0071 section)
- Decision: `decisions/DEC-0053.md`
- Research: `docs/engineering/research.md` (`R-0046`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (Discovery Addendum — US-0071)
- Sprint artifacts: `sprints/S0050/*`

## Focus

1. **Policy + allowlist (T-001..T-002)**: forbidden planning-shaped tokens in user-visible outputs only; explicit internal surfaces + comments-not-strings rule.
2. **Enforcement chain (T-003..T-005)**: `/execute` default guard, `/qa` automated scan with fail-closed diagnostics, structured findings with path evidence and remediation.
3. **Vocabulary + precision (T-006..T-007)**: shared reason codes; no false blocks on allowlisted docs/comments.
4. **Parity + evidence (T-008..T-010)**: active/template alignment, regression matrix (positive/negative/allowlist/idempotence), release attestation that checks ran.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0050/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0050/tasks.md` marked done.
- `sprints/S0050/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps (**PASS** after `/plan-verify`).
- `sprints/S0050/progress.md`, `sprints/S0050/uat.json`, and `sprints/S0050/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0071`.

## Next phase

Plan-verify **PASS** for **`S0050`** (`sprints/S0050/plan-verify.json`). Proceed to **`/execute`** for **`S0050`** (`US-0071`).

---

## TL -> Dev Handoff — Sprint S0049 (US-0070 Configurable Auto Phase Selection Policy)

## Planning summary

- **Sprint**: S0049 (new)
- **Story**: US-0070 — Scratchpad-controlled `/auto` phase selection policy
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped 1:1 to `T-001..T-010` in `sprints/S0049/tasks.md`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0070 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0070 section)
- Decision: `decisions/DEC-0052.md`
- Research: `docs/engineering/research.md` (`R-0049`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (Discovery Addendum — US-0070)
- Sprint artifacts: `sprints/S0049/*`

## Focus

1. **Policy contract + conflict gate (T-001)**: single active selector (`AUTO_PHASE_PLAN` / `EXCLUDE` / `INCLUDE` / `PROFILE`) and `PHASE_POLICY_CONFLICT` per `DEC-0052`.
2. **Plan materialization + breadcrumbs (T-002..T-005)**: ordered canonical plan, non-skippable reinstatement, `start-from` intersection, fail-closed invalid tokens.
3. **Continuation + modes (T-006..T-007)**: backlog-drain, bulk execute, team paths, and resume parity — reload policy, recompute plan, no silent phase revival.
4. **Parity + regression + operator UX (T-008..T-010)**: active/template docs, test coverage, boundary status with selected/skipped + reason codes.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0049/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0049/tasks.md` marked done.
- `sprints/S0049/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps (**PASS** after `/plan-verify`).
- `sprints/S0049/progress.md`, `sprints/S0049/uat.json`, and `sprints/S0049/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0070`.

## Next phase

Proceed to **`/execute`** for `S0049` (`US-0070`). Plan-verify: **PASS** (`sprints/S0049/plan-verify.json`).

---

## TL -> Dev Handoff — Sprint S0048 (US-0069 Strict Phase Role Enforcement in /auto)

## Planning summary

- **Sprint**: S0048 (new)
- **Story**: US-0069 — Strict phase role enforcement in `/auto` orchestration
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped 1:1 to `T-001..T-010` in `sprints/S0048/tasks.md`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0069 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0069 section)
- Decision: `decisions/DEC-0051.md`
- Research: `docs/engineering/research.md` (`R-0048`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (Discovery Addendum — US-0069)
- Sprint artifacts: `sprints/S0048/*`

## Focus

1. **Contract + single-valued roles (T-001)**: canonical phase→role matrix and scratchpad alternate resolution per `DEC-0051`.
2. **Preflight + fail-closed spawn (T-002..T-004)**: `PHASE_ROLE_CAPABILITY_MISSING`, checkpoint `PHASE_ROLE_MISMATCH`, and full diagnostics.
3. **Execute default deny + resume parity (T-005..T-006)**: override governance ref path; no stale resume bypass.
4. **Parity + regression + vocabulary + release evidence (T-007..T-010)**: active/template docs, tests, reason-code docs, readiness citations.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0048/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0048/tasks.md` marked done.
- `sprints/S0048/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps (**PASS**; recorded 2026-03-20).
- `sprints/S0048/progress.md`, `sprints/S0048/uat.json`, and `sprints/S0048/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0069`.

## Next phase

Proceed to **`/execute`** for `S0048` (`US-0069`).

---

## TL -> Dev Handoff — Sprint S0047 (US-0068 Mandatory Intake Question Packs)

## Planning summary

- **Sprint**: S0047 (new)
- **Story**: US-0068 — Mandatory intake question packs for first and small intakes
- **Task count**: 11 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped in `sprints/S0047/tasks.md` (remediation applied for AC-8/AC-9/AC-10)

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0068 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0068 section)
- Decision: `decisions/DEC-0050.md`
- Research: `docs/engineering/research.md` (`R-0045`, baseline `R-0041`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0068 discovery addendum)
- Sprint artifacts: `sprints/S0047/*`

## Focus

1. **Deterministic pack schemas (T-001..T-003)**: define machine-verifiable first/small intake topic coverage with required/optional classification.
2. **Fail-closed persistence policy (T-004..T-008)**: block writes on missing required coverage, allow explicit bounded assumptions, and emit deterministic reason codes.
3. **Parity + regression + fallback (T-009..T-011)**: cover active/template parity (AC-8), explicit regression matrix (AC-9), and deterministic unknown-stack fallback (AC-10).

## Execution order

Run tasks `T-001`..`T-011` in sequence (see `sprints/S0047/tasks.md`).

## Done criteria for Dev completion

- All 11 tasks in `sprints/S0047/tasks.md` marked done.
- `sprints/S0047/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0047/progress.md`, `sprints/S0047/uat.json`, and `sprints/S0047/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0068`.

## Next phase

Proceed to **`/execute`** for `S0047` (`US-0068`) after `/plan-verify`.

---

## TL -> Dev Handoff — Sprint S0046 (US-0067 Release Operator Run/Connect/Verify Hints Contract)

## Planning summary

- **Sprint**: S0046 (new)
- **Story**: US-0067 — Release operator Run/Connect/Verify hints contract
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0046/plan-verify.json`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0067 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0067 section)
- Decision: `decisions/DEC-0049.md`
- Research: `docs/engineering/research.md` (`R-0044`, baseline `R-0041`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0067 discovery addendum)
- Sprint artifacts: `sprints/S0046/*`

## Focus

1. **Canonical schema + required fields (T-001..T-003)**: fixed-order `Run -> Connect -> Verify -> Credentials(env-ref only) -> Known Issues` contract with required operator fields and credentials safety boundary.
2. **Fail-closed release and context alignment (T-004..T-007)**: deterministic latest-pointer parity, missing/ambiguous field blocking, runtime context (`local|remote`) explicitness, and QA/release evidence linkage.
3. **Parity + deterministic reruns (T-008..T-010)**: active/template parity, regression coverage, and idempotent concise operator-facing release output.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0046/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0046/tasks.md` marked done.
- `sprints/S0046/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0046/progress.md`, `sprints/S0046/uat.json`, and `sprints/S0046/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0067`.

## Next phase

Proceed to **`/execute`** for `S0046` (`US-0067`) after `/plan-verify`.

---

## TL -> Dev Handoff — Sprint S0045 (US-0066 Generated Test Scaffolding + Auto-Run)

## Planning summary

- **Sprint**: S0045 (new)
- **Story**: US-0066 — Generated test scaffolding + auto-run contract for app projects
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped in `sprints/S0045/tasks.md`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0066 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0066 section)
- Decision: `decisions/DEC-0048.md`
- Research: `docs/engineering/research.md` (`R-0043`, baseline `R-0041`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0066 section/addendum)
- Sprint artifacts: `sprints/S0045/*`

## Focus

1. **Scaffold generation contract (T-001..T-003)**: stack detection, missing-asset generation, and deterministic baseline `TEST_COMMAND` runbook wiring.
2. **QA and fail-safe behavior (T-004..T-007)**: automatic generated-test execution, unsupported-stack diagnostics, non-destructive merge precedence, and runtime-autopilot integration boundary.
3. **Parity + evidence (T-008..T-010)**: active/template parity, regression coverage, and deterministic release/readiness evidence references.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0045/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0045/tasks.md` marked done.
- `sprints/S0045/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0045/progress.md`, `sprints/S0045/uat.json`, and `sprints/S0045/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0066`.

## Next phase

Proceed to **`/execute`** for `S0045` (`US-0066`) after `/plan-verify`.

---

## TL -> Dev Handoff — Sprint S0044 (US-0065 Runtime QA Autopilot)

## Planning summary

- **Sprint**: S0044 (new)
- **Story**: US-0065 — Runtime QA Autopilot for generated projects (startup/connectivity/logs/bounded debug retries)
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped in `sprints/S0044/tasks.md`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0065 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0065 section)
- Decision: `decisions/DEC-0047.md`
- Research: `docs/engineering/research.md` (`R-0042`, baseline `R-0041`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0065 section/addendum)
- Sprint artifacts: `sprints/S0044/*`

## Focus

1. **Mandatory runtime truth path (T-001..T-004)**: startup, connectivity, log scan, bounded retries, and auditable evidence schema.
2. **Deterministic runtime policy (T-005..T-008)**: stack-profile resolution, webapp/browser checks, debug escalation, and remote-runtime compatibility.
3. **Parity + verification (T-009..T-010)**: active/template contract parity and deterministic regression paths.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0044/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0044/tasks.md` marked done.
- `sprints/S0044/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0044/progress.md`, `sprints/S0044/uat.json`, and `sprints/S0044/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0065`.

## Next phase

Proceed to **`/execute`** for `S0044` (`US-0065`) after `/plan-verify`.

---

# TL -> Dev Handoff — Sprint S0043 (US-0063 OS-Aware Runbook Bootstrap)

## Planning summary

- **Sprint**: S0043 (new)
- **Story**: US-0063 — OS-aware runbook command auto-bootstrap with verified
  quality gates
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0043/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0063 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0063 section)
- Decision: `decisions/DEC-0046.md`
- Research: `docs/engineering/research.md` (`R-0039`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0063 section)
- Sprint artifacts: `sprints/S0043/*`

## Focus

1. **Bootstrap contract + detection (T-001..T-004)**: precedence model, OS/stack
   detection, and deterministic validation diagnostics.
2. **Gate and safety behavior (T-005..T-007)**: keep mandatory baseline command
   policy and preserve user overrides on reruns.
3. **Parity + verification (T-008..T-010)**: active/template parity with
   installer/CLI/docs/tests updates.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0043/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0043/tasks.md` marked done.
- `sprints/S0043/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0043/progress.md`, `sprints/S0043/uat.json`, and
  `sprints/S0043/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes checkpoint traceability for `US-0063`.

## Next phase

Proceed to **`/execute`** for `S0043` (`US-0063`).

---

# TL -> Dev Handoff — Sprint S0041 (US-0064 Remote Connectivity Contract)

## Planning summary

- **Sprint**: S0041 (new)
- **Story**: US-0064 — Remote runtime connectivity contract for QA/release/publish
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0041/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0064 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0064 section)
- Decision: `decisions/DEC-0044.md`
- Research: `docs/engineering/research.md` (`R-0040`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0064 section)
- Sprint artifacts: `sprints/S0041/*`

## Focus

1. **Schema + validation (T-001..T-004)**: connectivity metadata + docker-over-ssh
   support and deterministic validation diagnostics.
2. **Phase integration (T-005..T-007)**: remote-aware release/qa/execute behavior
   and canonical operator connectivity doc.
3. **Parity + verification (T-008..T-010)**: active/template parity, tests, and docs.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0041/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0041/tasks.md` marked done.
- `sprints/S0041/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0041/progress.md`, `sprints/S0041/uat.json`, and
  `sprints/S0041/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes checkpoint traceability for `US-0064`.

## Next phase

Proceed to **`/execute`** for `S0041` (`US-0064`).

---

# TL -> Dev Handoff — Sprint S0040 (US-0061 Ownership Guard + Archive Control)

## Planning summary

- **Sprint**: S0040 (new)
- **Story**: US-0061 — Cross-phase artifact ownership guard and deterministic
  archive control
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0040/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0061 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0061 section)
- Decision: `decisions/DEC-0043.md`
- Research: `docs/engineering/research.md` (`R-0037`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0061 section/addendum)
- Sprint artifacts: `sprints/S0040/*`

## Focus

1. **Ownership matrix + fail-safe (T-001..T-004)**: define phase ownership,
   non-destructive mutation rules, and override evidence requirements.
2. **Archive verification control (T-005..T-006)**: deterministic archive
   verification outputs and fail-safe mismatch behavior.
3. **Parity + validation (T-007..T-010)**: preserve existing canonical
   contracts and add regression/test/doc updates.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0040/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0040/tasks.md` marked done.
- `sprints/S0040/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0040/progress.md`, `sprints/S0040/uat.json`, and
  `sprints/S0040/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes checkpoint traceability for `US-0061`.

## Next phase

Proceed to **`/execute`** for `S0040` (`US-0061`).

---

# TL -> Dev Handoff — Sprint S0039 (US-0060 State Rollover Enforcement)

## Planning summary

- **Sprint**: S0039 (new)
- **Story**: US-0060 — Deterministic state hot-surface rollover and archive enforcement
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0039/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0060 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0060 section)
- Decision: `decisions/DEC-0042.md`
- Research: `docs/engineering/research.md` (`R-0036`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0060 section/addendum)
- Sprint artifacts: `sprints/S0039/*`

## Focus

1. **Threshold contract (T-001..T-003)**: deterministic rollover triggers and
   refresh-context enforcement.
2. **Archive safety (T-004..T-006)**: non-destructive history retention,
   idempotent partitioning, and fail-safe diagnostics.
3. **Parity + validation (T-007..T-010)**: ordering compatibility, docs, tests,
   and release traceability.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0039/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0039/tasks.md` marked done.
- `sprints/S0039/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0039/progress.md`, `sprints/S0039/uat.json`, and
  `sprints/S0039/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes checkpoint traceability for `US-0060`.

## Next phase

Proceed to **`/execute`** for `S0039` (`US-0060`).

---

# TL -> Dev Handoff — Sprint S0038 (US-0059 Intake Capability Guard + Drift Safety)

## Planning summary

- **Sprint**: S0038 (new)
- **Story**: US-0059 — Deterministic intake runtime capability guard and
  single-writer drift safety
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0038/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0059 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0059 section)
- Decision: `decisions/DEC-0041.md`
- Research: `docs/engineering/research.md` (`R-0035`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0059 section/addendum)
- Sprint artifacts: `sprints/S0038/*`

## Focus

1. **Capability fail-fast (T-001..T-003)**: deterministic preflight and explicit
   fallback policy.
2. **Single-writer drift safety (T-004..T-006)**: self-write-aware drift
   semantics and fail-safe external conflict behavior.
3. **Parity + validation (T-007..T-010)**: active/template parity, tests, docs,
   and release traceability.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0038/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0038/tasks.md` marked done.
- `sprints/S0038/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0038/progress.md`, `sprints/S0038/uat.json`, and
  `sprints/S0038/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes checkpoint traceability for `US-0059`.

## Next phase

Proceed to **`/execute`** for `S0038` (`US-0059`).

---

# TL -> Dev Handoff — Sprint S0037 (US-0058 Deterministic Artifact Ordering)

## Planning summary

- **Sprint**: S0037 (new)
- **Story**: US-0058 — Deterministic artifact ordering and write discipline
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0037/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0058 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0058 section)
- Decision: `decisions/DEC-0040.md`
- Research: `docs/engineering/research.md` (`R-0033`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0058 section)
- Sprint artifacts: `sprints/S0037/*`

## Focus

1. **Ordering matrix + fail-safe (T-001..T-005)**: define canonical policy and
   command-level fail-safe anchor behavior.
2. **Idempotence + guarantees (T-006..T-008)**: preserve canonical ownership
   contracts while enforcing deterministic ordering.
3. **Validation + docs (T-009..T-010)**: regression coverage and operator docs.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0037/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0037/tasks.md` marked done.
- `sprints/S0037/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0037/progress.md`, `sprints/S0037/uat.json`, and
  `sprints/S0037/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes checkpoint traceability for `US-0058`.

## Next phase

Proceed to **`/execute`** for `S0037` (`US-0058`).

---

# TL -> Dev Handoff — Sprint S0036 (US-0057 Upgrade-Safe Scratchpad Example Refresh)

## Planning summary

- **Sprint**: S0036 (new)
- **Story**: US-0057 — Upgrade-safe scratchpad local example refresh and parity
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0036/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0057 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0057 section)
- Decision: `decisions/DEC-0039.md`
- Research: `docs/engineering/research.md` (`R-0032`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0057 section)
- Sprint artifacts: `sprints/S0036/*`

## Focus

1. **Ownership + refresh semantics (T-001..T-004)**: enforce framework-owned
   example refresh with deterministic diagnostics while preserving user-local
   scratchpad values.
2. **Parity + drift prevention (T-005..T-008)**: keep active/template and
   installer parity so new flags appear in refreshed example surfaces.
3. **Validation + docs (T-009..T-010)**: regression coverage and operator-facing
   README/runbook guidance.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0036/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0036/tasks.md` marked done.
- `sprints/S0036/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0036/progress.md`, `sprints/S0036/uat.json`, and
  `sprints/S0036/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` traceability/checkpoints updated for `US-0057`.

## Execution guardrails

- Preserve user ownership for `.cursor/scratchpad.local.md`.
- Keep framework refresh deterministic for `.cursor/scratchpad.local.example.md`.
- Maintain parity across installer scripts and template docs/files.

## Next phase

Proceed to **`/execute`** for `S0036` (`US-0057`).

---

# TL -> Dev Handoff — Sprint S0035 (US-0056 Strict Runtime Proof for Per-Phase Isolation)

## Planning summary

- **Sprint**: S0035 (new)
- **Story**: US-0056 — Strict Runtime Proof for Per-Phase Subagent Isolation
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0035/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0056 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0056 section)
- Decision: `decisions/DEC-0038.md`
- Research: `docs/engineering/research.md` (`R-0034`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0056 section/addendum)
- Sprint artifacts: `sprints/S0035/*`

## Focus

1. **Strict tuple contract (T-001..T-004)**: require deterministic runtime
   attestation fields and fail-closed reason-code taxonomy.
2. **Boundary integration (T-005..T-006)**: enforce strict-proof checks in
   `/auto`, `/verify-work`, and `/release` contracts.
3. **Operator + compatibility guidance (T-007..T-010)**: bounded legacy handling,
   diagnostics, tests, and active/template parity.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0035/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0035/tasks.md` marked done.
- `sprints/S0035/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0035/progress.md`, `sprints/S0035/uat.json`, and
  `sprints/S0035/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` traceability/checkpoints updated for `US-0056`.

## Execution guardrails

- Keep `/auto` orchestration-only semantics.
- Preserve existing mandatory release gate chain order.
- Maintain active/template parity for all strict-proof contracts.

## Next phase

Proceed to **`/execute`** for `S0035` (`US-0056`).

---

# TL -> Dev Handoff — Sprint S0034 (US-0055 Deterministic Status Reconciliation Command)

## Planning summary

- **Sprint**: S0034 (new)
- **Story**: US-0055 — Deterministic Status Reconciliation Command
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0034/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0055 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0055 section)
- Decision: `decisions/DEC-0037.md`
- Research: `docs/engineering/research.md` (`R-0031`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0055 section)
- Sprint artifacts: `sprints/S0034/*`

## Focus

1. **Reconciliation command contract (T-001..T-003)**: define deterministic
   read/repair behavior with canonical precedence and conflict handling.
2. **Normalization behavior (T-004..T-007)**: reconcile DONE+unchecked and
   acceptance/resume drift with bounded target scope and auditable evidence.
3. **Deterministic diagnostics + parity (T-008..T-010)**: reason codes,
   regression coverage, and active/template alignment.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0034/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0034/tasks.md` marked done.
- `sprints/S0034/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0034/progress.md`, `sprints/S0034/uat.json`, and
  `sprints/S0034/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` traceability row for US-0055 advances from
  `PLANNED` with evidence references.

## Execution guardrails

- Preserve canonical status ownership (`docs/product/backlog.md`).
- Reconciliation writes must be target-scoped and non-destructive.
- Keep mandatory release gate chain behavior unchanged.

## Next phase

Proceed to **`/execute`** for `S0034` (`US-0055`).

---

# TL -> Dev Handoff — Sprint S0033 (US-0054 Configurable Multi-Target Release Publish with Confirmation Gate)

## Planning summary

- **Sprint**: S0033 (new)
- **Story**: US-0054 — Configurable Multi-Target Release Publish with Confirmation Gate
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0033/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0054 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0054 section)
- Decision: `decisions/DEC-0036.md`
- Research: `docs/engineering/research.md` (`R-0029`, `R-0030`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0054 section)
- Sprint artifacts: `sprints/S0033/*`

## Focus

1. **Target schema + taxonomy (T-001..T-003)**: implement deterministic
   configurable target schema with built-in target classes and first-class
   `custom` + `ssh` support.
2. **Safety contract (T-004, T-006, T-007)**: enforce confirmation default,
   fail-fast validation, and env-reference-only secret handling.
3. **Run semantics (T-005)**: deterministic target ordering, selection, and
   skip behavior for disabled targets.
4. **Parity + guardrails (T-008..T-010)**: align active/template contract and
   preserve mandatory release gate invariants.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0033/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0033/tasks.md` marked done.
- `sprints/S0033/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0033/progress.md`, `sprints/S0033/uat.json`, and
  `sprints/S0033/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` traceability row for US-0054 advances from
  `PLANNED` with evidence references.

## Execution guardrails

- Mandatory release quality gates remain unchanged (`/qa`, `/verify-work`, `/release`).
- No inline credentials in committed target configuration.
- Keep active/template parity for all publish-target contracts.

## Next phase

Proceed to **`/execute`** for `S0033` (`US-0054`).

---

# TL -> Dev Handoff — Sprint S0032 (US-0053 Context Compaction and Tiered Token-Cost Optimization Mode)

## Planning summary

- **Sprint**: S0032 (new)
- **Story**: US-0053 — Context Compaction and Tiered Token-Cost Optimization Mode
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0032/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0053 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0053 section)
- Decision: `decisions/DEC-0035.md`
- Research: `docs/engineering/research.md` (`R-0027`, `R-0028`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0053 section)
- Sprint artifacts: `sprints/S0032/*`

## Focus

1. **Profile policy (T-001..T-003)**: implement deterministic
   `TOKEN_PROFILE=lean|balanced|full` behavior, mapping table, and explicit
   override precedence.
2. **Context compaction (T-004, T-005)**: implement bounded active-context
   contracts for `state.md` and compact decisions index policy with archive/link
   safety.
3. **Retrieval strategy (T-006)**: enforce narrow-read `/ask` policy
   (targeted-first, bounded expansion, explicit not-found behavior).
4. **Parity and guardrails (T-007..T-009)**: keep active/template contracts
   aligned and lock mandatory QA/UAT/release invariants in regression checks.
5. **Operator guidance + integrity (T-010)**: document profile tradeoffs and
   verify no destructive impact to ID/release-history semantics.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0032/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0032/tasks.md` marked done.
- `sprints/S0032/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0032/progress.md`, `sprints/S0032/uat.json`, and
  `sprints/S0032/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` traceability row for US-0053 advances from
  `PLANNED` with evidence references.

## Execution guardrails

- Mandatory safety gates remain intact (`/qa`, `/verify-work`, `/release`).
- No destructive rewrite of historical release or ID artifacts.
- Keep active/template parity for all token-profile and compaction contracts.

## Next phase

Proceed to **`/execute`** for `S0032` (`US-0053`).

---

# TL -> Dev Handoff — Sprint S0031 (US-0052 Optional Fresh-Project ID Namespace Bootstrap)

## Planning summary

- **Sprint**: S0031 (new)
- **Story**: US-0052 — Optional Fresh-Project ID Namespace Bootstrap
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-8 verified PASS in `sprints/S0031/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0052 AC-1..AC-8)
- Architecture: `docs/engineering/architecture.md` (US-0052 section)
- Decisions: `decisions/DEC-0034.md`
- Research: `docs/engineering/research.md` (`R-0024`, `R-0025`)
- PO->TL handoff: `handoffs/po_to_tl.md` (Install Hygiene + Smart Intake + Bootstrap IDs section)
- Sprint artifacts: `sprints/S0031/*`

## Focus

1. **Bootstrap control contract (T-001)**: define explicit optional bootstrap control with default-off behavior and clear operator interface.
2. **Deterministic freshness eligibility (T-002, T-005)**: detect fresh vs non-fresh repo state using canonical ID surfaces and emit actionable diagnostics when bootstrap request is ineligible.
3. **ID generation behavior (T-003, T-004, T-006)**: start at `0001` only for eligible bootstrap; otherwise continue from highest existing IDs without rewriting historical artifacts and with collision safety.
4. **Operator guidance (T-007)**: document bootstrap constraints, compatibility behavior, and migration caveats in runbook/README/help paths.
5. **Regression and parity (T-008..T-010)**: cover fresh/non-fresh/mixed-edge cases and keep active/template contracts aligned.

## Execution order

Execute tasks `T-001`..`T-010` in sequence (see `sprints/S0031/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0031/tasks.md` are marked done.
- No uncovered US-0052 acceptance criteria after `sprints/S0031/plan-verify.json` is PASS.
- `sprints/S0031/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row for US-0052 advanced from `PLANNED` with evidence references.

## Execution guardrails

- Preserve backward compatibility for non-fresh repositories (highest-ID continuation).
- Never renumber or rewrite historical IDs.
- Keep optional behavior explicit and default-off; no hidden bootstrap side effects.
- Maintain active/template parity for command, docs, and test contracts.

## Next phase

Proceed to **`/execute`** for `S0031` (`US-0052`).

---

# TL -> Dev Handoff — Sprint S0030 (US-0051 Intelligent Intake Decomposition and Risk-Aware PO Questioning)

## Planning summary

- **Sprint**: S0030 (new)
- **Story**: US-0051 — Intelligent Intake Decomposition and Risk-Aware PO Questioning
- **Task count**: 11 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0030/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0051 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0051 section)
- Decisions: `decisions/DEC-0033.md`
- Research: `docs/engineering/research.md` (`R-0024`, `R-0025`)
- PO->TL handoff: `handoffs/po_to_tl.md` (Install Hygiene + Smart Intake + Bootstrap IDs section)
- Sprint artifacts: `sprints/S0030/*`

## Focus

1. **Decomposition trigger model (T-001, T-005)**: add deterministic breadth/risk heuristics with safe single-story default for narrow intake.
2. **Split quality and persistence (T-002, T-003)**: generate vertical-slice/workflow-step split proposals and persist explicit split rationale/boundaries.
3. **User authority controls (T-004)**: require accept/merge/adjust confirmation before decomposed persistence.
4. **Risk-aware questioning (T-006, T-007)**: escalate follow-ups for broad/high-risk intake while keeping bounded rounds.
5. **Low-touch compatibility (T-008)**: preserve `INTAKE_GUIDED_MODE=0` minimal-overhead behavior with duplicate safety intact.
6. **Traceability + parity + regression (T-009..T-011)**: ensure artifact evidence, active/template alignment, and tests for split/no-split/questioning paths.

## Execution order

Execute tasks `T-001`..`T-011` in sequence (see `sprints/S0030/tasks.md`).

## Done criteria for Dev completion

- All 11 tasks in `sprints/S0030/tasks.md` are marked done.
- No uncovered US-0051 acceptance criteria after `sprints/S0030/plan-verify.json` is PASS.
- `sprints/S0030/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row for US-0051 advanced from `PLANNED` with evidence references.

## Execution guardrails

- Process/workflow/docs/tests only; no runtime product feature behavior changes.
- Decomposition must remain bounded and user-controlled (no forced uncontrolled splitting).
- Preserve low-touch compatibility and active/template parity for intake semantics.

## Next phase

Proceed to **`/execute`** for `S0030` (`US-0051`).

---

# TL -> Dev Handoff — Sprint S0029 (US-0050 Clean Install Hygiene and Complete Clean-Repo Coverage)

## Planning summary

- **Sprint**: S0029 (new)
- **Story**: US-0050 — Clean Install Hygiene and Complete Clean-Repo Coverage
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-9 verified PASS in `sprints/S0029/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0050 AC-1..AC-9)
- Architecture: `docs/engineering/architecture.md` (US-0050 section)
- Decisions: `decisions/DEC-0032.md`
- Research: `docs/engineering/research.md` (`R-0024`, `R-0025`)
- PO->TL handoff: `handoffs/po_to_tl.md` (Install Hygiene + Smart Intake + Bootstrap IDs section)
- Sprint artifacts: `sprints/S0029/*`

## Focus

1. **Ownership source of truth (T-001)**: define canonical installer-owned path contract used by all installers.
2. **Cross-installer parity (T-002..T-004)**: ensure `installer.ps1`, `installer.sh`, `installer.py` consume same ownership rules for install/clean.
3. **Cleanup safety (T-005)**: enforce explicit non-destructive boundaries for non-framework files.
4. **Template neutrality (T-006, T-007)**: remove seeded operational history and neutralize hardcoded runtime ID refs unless intentionally baseline-backed.
5. **Lifecycle regression (T-008, T-009)**: prove fresh install -> clean-repo -> reinstall behavior and full cleanup coverage.
6. **Compatibility/parity hardening (T-010)**: preserve US-0018 upgrade behavior and active/template alignment.

## Execution order

Execute tasks `T-001`..`T-010` in sequence (see `sprints/S0029/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0029/tasks.md` are marked done.
- No uncovered US-0050 acceptance criteria; `sprints/S0029/plan-verify.json` PASS after `/plan-verify`.
- `sprints/S0029/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row for US-0050 advanced from `PLANNED` with evidence references.

## Execution guardrails

- Process/workflow/docs/tests only; no runtime product feature behavior changes.
- Keep cleanup operations ownership-scoped and non-destructive.
- Maintain active/template parity for installer and starter-artifact contract behavior.

## Next phase

Proceed to **`/execute`** for `S0029` (`US-0050`).

---

# TL -> Dev Handoff — Sprint S0028 (US-0049 Legacy DONE-Story Acceptance/Traceability Backfill Guard)

## Planning summary

- **Sprint**: S0028 (new)
- **Story**: US-0049 — Legacy DONE-Story Acceptance/Traceability Backfill Guard
- **Task count**: 8 (within SPRINT_MAX_TASKS=12)
- **AC coverage**: AC-1..AC-8 explicit in `sprints/S0028/plan-verify.json`; run `/plan-verify` to confirm.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0049 AC-1..AC-8)
- Architecture: `docs/engineering/architecture.md` (US-0049 section)
- Decision: `decisions/DEC-0031.md`
- Research: `docs/engineering/research.md` (R-0023)
- PO→TL handoff: `handoffs/po_to_tl.md` (US-0049 discovery addendum)
- Sprint artifacts: `sprints/S0028/*`

## Focus

1. **Detection rule (T-001)**: Legacy drift = backlog DONE and (acceptance unchecked OR traceability/state lacks entry OR release artifacts lack representation).
2. **Target-scoped repair (T-002)**: Mutate only stories matching the rule; no broad rewrite.
3. **Audit report (T-003)**: Canonical path `docs/engineering/legacy-drift-audit.md`; required fields: story ID, prior acceptance/traceability state, resolved state, reason code, evidence ref.
4. **Reason codes (T-004)**: `BACKLOG_DONE_ACCEPTANCE_UNCHECKED`, `BACKLOG_DONE_TRACEABILITY_MISSING`, `BACKLOG_DONE_RELEASE_ARTIFACT_MISSING` with remediation.
5. **One-time backfill (T-005)**: Explicit trigger; idempotent when no drift; emit audit report.
6. **Ongoing guard (T-006)**: At release/reconciliation or dedicated check; block or repair with audit append; documented, deterministic.
7. **Template parity (T-007)**: Active and `template/` command/rule/docs for backfill and guard aligned.
8. **Regression (T-008)**: No-drift run, single-drift repair, guard block/repair with reason code.

## Execution order

Execute tasks `T-001`..`T-008` in sequence (see `sprints/S0028/tasks.md`).

## Done criteria for Dev completion

- All 8 tasks in `sprints/S0028/tasks.md` are marked done.
- No uncovered US-0049 acceptance criteria; `sprints/S0028/plan-verify.json` satisfied (run `/plan-verify` to confirm).
- `sprints/S0028/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row for US-0049 advanced from PLANNED with evidence references.

## Execution guardrails

- Process/workflow/docs only; no runtime product feature changes.
- Maintain active/template parity for backfill guard, audit report location, reason codes.
- Regression: no-drift, single-drift repair, guard block/repair with reason code.

## Next phase

Run **`/plan-verify`** for S0028; then proceed to execute and `/qa` when ready.

---

# TL -> Sprint-Plan Handoff — US-0049 (Legacy DONE-Story Acceptance/Traceability Backfill Guard) [COMPLETED]

## Architecture summary

- **Story**: US-0049 — Legacy DONE-Story Acceptance/Traceability Backfill Guard (OPEN)
- **Scope**: Detection rule (backlog DONE and acceptance unchecked or traceability/release missing), target-scoped repair only, canonical audit report, reason-code vocabulary, one-time backfill mode, ongoing guard at release/reconciliation.
- **Out of scope**: Changing US-0045 canonical status ownership or US-0043 broad reconciliation semantics.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0049 AC-1..AC-8)
- Architecture: `docs/engineering/architecture.md` (US-0049 section)
- Decision: `decisions/DEC-0031.md`
- Research: `docs/engineering/research.md` (R-0023)
- PO→TL handoff: `handoffs/po_to_tl.md` (US-0049 discovery addendum)

## Focus for `/sprint-plan`

1. **Detection rule**: Document and implement detection for legacy drift (backlog DONE and acceptance unchecked or traceability missing or release artifact missing).
2. **Audit report**: Canonical path `docs/engineering/legacy-drift-audit.md`; required fields per entry (story ID, prior acceptance/traceability state, resolved state, reason code, evidence ref).
3. **Reason codes**: `BACKLOG_DONE_ACCEPTANCE_UNCHECKED`, `BACKLOG_DONE_TRACEABILITY_MISSING`, `BACKLOG_DONE_RELEASE_ARTIFACT_MISSING` with remediation guidance.
4. **One-time backfill**: Explicit trigger; target-scoped repair; idempotent when no drift; append audit report.
5. **Ongoing guard**: At release or reconciliation (or dedicated check); block with reason code or repair with audit append; deterministic, documented.
6. **Template parity**: Active and `template/` command/rule/docs for backfill and guard aligned.
7. **Regression**: No-drift run (no changes), single-drift repair (audit entry), guard block/repair with reason code.

## Next phase

Sprint **S0028** created. Run **`/plan-verify`** for S0028; then `/execute` handoff.

---

# TL -> Dev Handoff — Sprint S0027 (US-0032 Optional Feature User Guide Generation)

## Planning summary

- **Sprint**: S0027 (new)
- **Story**: US-0032 — Optional Feature User Guide Generation
- **Task count**: 8 (within SPRINT_MAX_TASKS=12)
- **AC coverage**: AC-1..AC-8 explicit in `sprints/S0027/plan-verify.json`; no gaps

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0032 AC-1..AC-8)
- Architecture: `docs/engineering/architecture.md` (US-0032 section)
- Decision: `decisions/DEC-0030.md`
- Sprint artifacts: `sprints/S0027/*`

## Focus

1. **USER_GUIDE_MODE** flag (default 0); when disabled, zero required steps or blocking checks in any phase.
2. Canonical location: `docs/user-guides/US-xxxx.md` per feature story when enabled.
3. Minimum guide schema: Purpose, Prerequisites, Usage steps, Example, Limitations, Troubleshooting (structural validation only).
4. Validation reports completeness; release blocks with `USER_GUIDE_INCOMPLETE` only when enabled and required sections missing.
5. Traceability: story ID → user guide artifact; referenced in handoff/release context.
6. Boundaries with US-0031: user guides end-user only; no duplicate spec-pack content; document separation.
7. Template parity: active and `template/` docs/commands/rules aligned for user-guide mode.

## Execution order

Execute tasks `T-001`..`T-008` in sequence (see `sprints/S0027/tasks.md`).

## Done criteria for Dev completion

- All 8 tasks in `sprints/S0027/tasks.md` are marked done.
- No uncovered US-0032 acceptance criteria; `sprints/S0027/plan-verify.json` remains satisfied.
- `sprints/S0027/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row for US-0032 advanced from PLANNED with evidence references.

## Execution guardrails

- Process/workflow/docs only; no runtime product feature changes.
- Maintain active/template parity for intake, architecture, sprint-plan, execute, qa, release, runbook, README.
- Regression: positive/negative and USER_GUIDE_MODE=0 zero-overhead coverage in test runners.

## Next phase

After execute: run `/plan-verify` for S0027 if not already run; then `/qa` and `/verify-work` when ready.

---

# TL -> Dev Handoff — Sprint S0011 (US-0039 Release Gate Tightening)

## Planning summary

- **Sprint**: S0011 (reused; plan valid per 2026-03-02 refresh)
- **Story**: US-0039 — Release Gate Tightening for Check-In Tests and QA/UAT Completion
- **Task count**: 11 (within SPRINT_MAX_TASKS=12)
- **AC coverage**: AC-1..AC-10 explicit in `sprints/S0011/plan-verify.json`; no gaps

## Rationale for reusing S0011

- Existing S0011 plan already covers US-0039 AC-1..AC-10 with 11 atomic tasks.
- Scope and architecture unchanged; backlog/acceptance criteria match.
- Sizing and gate-order semantics remain correct; no stale/incompatible content.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0039 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0039 section)
- Decision: `decisions/DEC-0019.md` (gate order, no-bypass, override evidence)
- Sprint artifacts: `sprints/S0011/*`

## Focus

1. **Gate order**: check-in test → QA → UAT → release finalization (mandatory, deterministic).
2. **Check-in test gate**: verify latest test result passing; block on missing/stale/failing with reason codes.
3. **QA gate**: require no unresolved blocking findings before release.
4. **UAT gate**: block on placeholder, incomplete, or unresolved-fail UAT state.
5. **Evidence**: per-gate pass/fail and evidence pointers in handoff/state for audit.
6. **No bypass**: default path has no bypass; override only via decision gate + rationale.
7. **Template parity**: align `template/` release, qa, execute, runbook for gate semantics.
8. **Regression**: positive/negative/stale-evidence cases per gate; optional lint/typecheck keys do not false-fail.

## Execution order

Execute tasks `T-001`..`T-011` in sequence (see `sprints/S0011/tasks.md`).

## Done criteria for Dev completion

- All 11 tasks in `sprints/S0011/tasks.md` are marked done.
- No uncovered US-0039 acceptance criteria; `sprints/S0011/plan-verify.json` remains satisfied.
- `sprints/S0011/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row for US-0039 advanced from PLANNED with evidence references.

## Execution guardrails (release gate tightening)

- Process/workflow/docs/tests only; no runtime product feature changes.
- Maintain active/template parity for release, qa, execute, runbook, README.
- Regression: positive/negative/stale-evidence and no-bypass coverage in test runners.

## Next phase

After execute/QA/verify-work: run `/plan-verify` for S0011 if not already run; then `/release` when gates pass.

---

# TL -> Dev Handoff — Sprint S0026 (US-0031 Optional Documentation Pack)

## Sprint Overview

Sprint `S0026` is planned for `US-0031`.

- Story count: 1 (`US-0031`)
- Planned tasks: 8
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0031 AC-1..AC-8)
- Sprint artifacts: `sprints/S0026/*`

## Focus

1. Add single enable flag/config for spec-pack mode; default disabled.
2. When disabled: no extra required steps in intake/architecture/release.
3. When enabled: create/update Design Concept, CRS, Technical Specification at canonical locations.
4. Define minimum required sections/fields per artifact; validation blocks only when enabled and incomplete.
5. Define traceability from backlog story IDs to spec-pack artifacts; document ownership (role/phase per document).
6. Maintain active/template parity for spec-pack mode references.

## Execution order

Execute tasks `T-001`..`T-008` in sequence.

## Done criteria for Dev completion

- All 8 tasks in `sprints/S0026/tasks.md` are marked done.
- No uncovered US-0031 acceptance criteria in `sprints/S0026/plan-verify.json`.
- `sprints/S0026/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row advanced from `PLANNED` with evidence references.

---

# TL -> Dev Handoff — Sprint S0025 (US-0048 Per-Phase Subagent Isolation)

## Sprint Overview

Sprint `S0025` is planned for `US-0048`.

- Story count: 1 (`US-0048`)
- Planned tasks: 10
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Next phase: **`/plan-verify`** for `S0025`

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0048 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0048 section)
- Research: `docs/engineering/research.md` (`R-0018`, `R-0019`)
- Decision: `decisions/DEC-0029.md`
- Sprint artifacts: `sprints/S0025/*`

## Focus

1. Enforce `/auto` orchestrator-only behavior; fail when phase work runs without fresh subagent.
2. Define and write isolation evidence schema and canonical locations; document in runbook/commands.
3. Add isolation-compliance gates to `/verify-work` and `/release`; enforce gate order.
4. Implement reason-code taxonomy and remediation; ensure pause/resume provenance.
5. Add regression coverage and active/template parity for isolation enforcement.

## Execution order

Execute tasks `T-001`..`T-010` in sequence.

## Critical constraints

- Isolation evidence schema: phase_id, role, fresh_context_marker, timestamp, evidence_ref.
- Fail-closed on missing/invalid evidence; no silent continuation.
- Gate order at release: check-in test → QA → UAT → isolation compliance → release finalization.
- Evidence must survive pause/resume; resume requires fresh context and new evidence.

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0025/tasks.md` are marked done.
- No uncovered US-0048 acceptance criteria in `sprints/S0025/plan-verify.json`.
- `sprints/S0025/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row advanced from `PLANNED` with evidence references.

---

# TL -> Dev Handoff — Sprint S0024 (US-0035 Component-Scoped Mode)

## Sprint Overview

Sprint `S0024` is planned for `US-0035`.

- Story count: 1 (`US-0035`)
- Planned tasks: 8
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Add component scope controls with default-off behavior.
2. Add explicit scope declaration and scoped task metadata contracts.
3. Add execute/qa/release guardrails for unapproved out-of-scope impact.
4. Maintain active/template parity and regression coverage.

## Dev completion note

- Sprint `S0024` implementation is complete.
- All tasks `T-001..T-008` are done with regression evidence in `tests/report.md`.
- Sprint is ready for QA/verify/release gates with complete artifacts.

---

# TL -> Dev Handoff — Sprint S0023 (US-0034 Cross-Repo Observability)

## Sprint Overview

Sprint `S0023` is planned for `US-0034`.

- Story count: 1 (`US-0034`)
- Planned tasks: 8
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Add optional compatibility observability mode controls (default off).
2. Add source declaration contract and canonical compatibility artifacts.
3. Add critical compatibility gate behavior for release.
4. Preserve active/template parity and regression coverage.

## Dev completion note

- Sprint `S0023` implementation is complete.
- All tasks `T-001..T-008` are done with regression evidence in `tests/report.md`.
- Sprint is ready for QA/verify/release gates with complete artifacts.

---

# TL -> Dev Handoff — Sprint S0022 (US-0033 Guided Intake Mode)

## Sprint Overview

Sprint `S0022` is planned for `US-0033`.

- Story count: 1 (`US-0033`)
- Planned tasks: 9
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Add one explicit intake behavior switch (`INTAKE_GUIDED_MODE`).
2. Define guided mode and low-touch mode behavior contracts.
3. Keep duplicate-check baseline safety in both modes.
4. Preserve active/template parity and regression coverage.

## Dev completion note

- Sprint `S0022` implementation is complete.
- All tasks `T-001..T-009` are done with regression evidence in `tests/report.md`.
- Sprint is ready for QA/verify/release gates with complete artifacts.

---

# TL -> Dev Handoff — Sprint S0021 (US-0045 Canonical Status Guard)

## Sprint Overview

Sprint `S0021` is planned for `US-0045`.

- Story count: 1 (`US-0045`)
- Planned tasks: 10
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Make `docs/product/backlog.md` the canonical story-status source.
2. Define deterministic reconciliation precedence and target-scoped mutation.
3. Add one-time normalization baseline report with auditable row details.
4. Add fail-safe contradiction reason code and active/template parity checks.

## Dev completion note

- Sprint `S0021` implementation is complete.
- All tasks `T-001..T-010` are done with regression evidence in `tests/report.md`.
- Sprint is ready for QA/verify/release gates with complete artifacts.

---

# TL -> Dev Handoff — Sprint S0020 (US-0047 Explicit Bulk Execute Orchestration)

## Sprint Overview

Sprint `S0020` is planned for `US-0047`.

- Story count: 1 (`US-0047`)
- Planned tasks: 10
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Define explicit bulk execute activation semantics for `/auto`.
2. Define deterministic selection, bounded controls, and reason-code outcomes.
3. Enforce team-scoped no-write guardrails (`TEAM_MEMBER` + `ACTIVE_TASK_IDS`).
4. Maintain strict fresh-context isolation and active/template parity.

## Dev completion note

- Sprint `S0020` implementation is complete.
- All tasks `T-001..T-010` are done with regression evidence in `tests/report.md`.
- Sprint is ready for QA/verify/release gates with complete artifacts.

---

# TL -> Dev Handoff — Sprint S0019 (US-0046 Explicit Bulk Sprint Planning)

## Sprint Overview

Sprint `S0019` is planned for `US-0046`.

- Story count: 1 (`US-0046`)
- Planned tasks: 10
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Define explicit `/sprint-plan --bulk` trigger semantics with default-safe fallback.
2. Define deterministic selection/grouping and bounded stop behavior.
3. Preserve sizing safety and planning artifact completeness for each generated sprint.
4. Maintain traceability consistency and active/template parity.

## Dev completion note

- Sprint `S0019` implementation is complete.
- All tasks `T-001..T-010` are done with regression evidence in `tests/report.md`.
- Sprint is ready for QA/verify/release gates with complete artifacts.

---

# TL -> Dev Handoff — Sprint S0018 (US-0016 Homebrew Sync)

## Sprint Overview

Sprint `S0018` is planned for `US-0016`.

- Story count: 1 (`US-0016`)
- Planned tasks: 3
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Align stable Homebrew formula tag/version with npm package version.
2. Add regression checks in both test runners for alignment.
3. Reconcile product acceptance state and release artifacts.

---

# TL -> Dev Handoff — Sprint S0017 (US-0044 Backlog-Drain Auto Mode)

## Sprint Overview

Sprint `S0017` is planned for `US-0044`.

- Story count: 1 (`US-0044`)
- Planned tasks: 10
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Add optional multi-story backlog-drain behavior contract for `/auto`.
2. Add fine-tune scratchpad switches with default-safe off behavior.
3. Add deterministic reason codes and per-story breadcrumb contract.
4. Maintain active/template parity and regression coverage.

---

# TL -> Dev Handoff — Sprint S0016 (US-0015 Runbook Completion)

## Sprint Overview

Sprint `S0016` is planned for `US-0015`.

- Story count: 1 (`US-0015`)
- Planned tasks: 4
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Execution order

Execute tasks `T-001..T-004`.

## Focus

1. Document intentional empty optional runbook commands.
2. Keep active/template parity for runbook + README.
3. Add regression tests to protect the documentation contract.

---

# TL -> Dev Handoff — Sprint S0015 (US-0043 Backlog Reconciliation Gate)

## Sprint Overview

Sprint `S0015` is planned for `US-0043`: Backlog Reconciliation Gate for
Released Sprints.

- Story count: 1 (`US-0043`)
- Planned tasks: 10
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required
- Milestone activation: not applicable

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0043 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0043 section)
- Research: `docs/engineering/research.md` (`R-0007`)
- Decision: `decisions/DEC-0021.md`
- Sprint artifacts: `sprints/S0015/*`

## Execution order

Execute tasks `T-001..T-010` in sequence.

## Priority focus

1. Implement deterministic release-boundary backlog reconciliation for the
   target sprint story only.
2. Add fail-safe contradiction handling with `BACKLOG_STATUS_DRIFT`.
3. Add regression coverage for stale mismatch and positive auto-reconcile.
4. Maintain active/template parity for command/rule/doc behavior.

## Critical constraints

- No mutation of unrelated backlog stories.
- No pre-release `DONE` transitions.
- Keep behavior deterministic and evidence-driven from canonical artifacts.
- Preserve manual-mode safe defaults and existing decision-gate boundaries.

---

# TL -> Dev Handoff — Sprint S0014 (US-0042 Release Findings Workflow)

## Sprint Overview

Sprint `S0014` is planned for `US-0042` and is implementation-complete.

## Scope delivered

1. Added canonical post-QA release findings artifact contract:
   `sprints/Sxxxx/release-findings.md`.
2. Added canonical blocked-release handoff:
   `handoffs/release_to_dev.md`.
3. Updated release command and release reason-code contract for blocked post-QA
   scenarios.
4. Updated runbook/README boundary guidance for QA findings vs release findings.
5. Added active/template parity updates and regression checks in both test
   runners.
6. Captured real blocked-release evidence for `S0013`.

---

# TL -> Dev Handoff — Sprint S0013 (US-0041 Lifecycle QA Expansion)

## Sprint Overview

Sprint S0013 is planned for US-0041: End-to-End Lifecycle QA for `its-magic`
Install/Upgrade/Clean.

- Story count: 1 (`US-0041`)
- Planned tasks: 11
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required (single-story sprint)
- Milestone activation: not applicable

## Execution Order

Execute tasks `T-001` through `T-011` in sequence.

## Priority focus for this sprint

1. Add clean-repo safety lifecycle checks in PowerShell + shell tests.
2. Add CLI lifecycle tests (`its-magic` path) for `missing`, `overwrite --backup`,
   `upgrade`, and `--clean-repo`.
3. Add invalid-mode negative-path checks with deterministic non-zero behavior.
4. Extend npm local package tests and CI lifecycle subset checks.
5. Update README/runbook lifecycle QA matrix and maintain template parity.

## Critical constraints

- Use temp directories only for lifecycle tests.
- Ensure cleanup runs even after failed assertions.
- Verify non-framework markers survive clean-repo checks.
- Keep active/template docs aligned for new lifecycle QA references.

---

# TL -> Dev Handoff — Sprint S0012 (US-0040 Release Notes Queue)

## Sprint Overview

Sprint S0012 is planned for US-0040: Per-Sprint Release Notes and Release Queue
Tracker.

- Story count: 1 (`US-0040`)
- Planned tasks: 11
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required (single-story sprint remains atomic)
- Milestone activation: not applicable

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0040 AC-1..AC-9)
- Architecture: `docs/engineering/architecture.md` (US-0040 section)
- Decision: `decisions/DEC-0020.md`
- Sprint artifacts: `sprints/S0012/*`

## Execution Order

Execute tasks T-001 through T-011 sequentially.

| Task | Description | Files | AC |
|------|-------------|-------|----|
| T-001 | Define canonical per-sprint immutable release notes path and target-sprint-only write semantics | `.cursor/commands/release.md`, `handoffs/releases/Sxxxx-release-notes.md` | AC-1 |
| T-002 | Define canonical release queue tracker schema and required fields | `.cursor/commands/release.md`, `handoffs/release_queue.md`, `docs/engineering/runbook.md` | AC-2 |
| T-003 | Define deterministic queue transitions (`ready -> unreleased -> released`) for target sprint only | `.cursor/commands/release.md`, `docs/engineering/state.md` | AC-3 |
| T-004 | Define unresolved sprint fail-safe behavior and deterministic reason codes | `.cursor/commands/release.md`, `handoffs/release_queue.md`, `docs/engineering/state.md` | AC-4 |
| T-005 | Define non-destructive legacy migration/backfill for `handoffs/release_notes.md` | `.cursor/commands/release.md`, `handoffs/release_notes.md`, `handoffs/releases/Sxxxx-release-notes.md` | AC-5 |
| T-006 | Define backward-compatible legacy latest-pointer/summary behavior | `handoffs/release_notes.md`, `.cursor/commands/release.md` | AC-6 |
| T-007 | Define queue/notes mismatch fail-safe handling and remediation contract | `.cursor/commands/release.md`, `handoffs/release_queue.md`, `docs/engineering/state.md` | AC-4, AC-7 |
| T-008 | Define unreleased queue visibility in readiness and release reporting | `.cursor/commands/release.md`, `docs/engineering/state.md`, `handoffs/release_notes.md` | AC-7 |
| T-009 | Align ownership/touchpoints across verify-work, release, refresh-context guidance | `.cursor/commands/release.md`, `.cursor/rules/core.mdc`, `.cursor/rules/handoffs.mdc`, `docs/engineering/runbook.md` | AC-8 |
| T-010 | Enforce active/template parity for release queue and per-sprint note semantics | `template/.cursor/commands/release.md`, `template/.cursor/rules/core.mdc`, `template/.cursor/rules/handoffs.mdc`, `template/docs/engineering/runbook.md` | AC-9 |
| T-011 | Plan positive/negative/migration/parity regression matrix in sprint UAT artifacts | `sprints/S0012/uat.md`, `sprints/S0012/uat.json`, `sprints/S0012/plan-verify.json` | AC-1, AC-3, AC-4, AC-5, AC-6, AC-7, AC-9 |

## Critical Requirements to Preserve

1. Release notes must be sprint-scoped and never overwrite another sprint's
   note artifact.
2. Queue transitions must only mutate the target sprint row during one release
   run.
3. Unresolved sprint identity and queue/notes mismatch must fail closed with
   deterministic reason codes and remediation guidance.
4. Legacy `handoffs/release_notes.md` must remain backward-compatible while
   canonical history moves to sprint-scoped files.
5. Migration/backfill must be non-destructive and idempotent.
6. Unreleased queue entries must be visible before release finalization.
7. Active/template guidance must remain behaviorally aligned.

## QA and Validation Focus

Required verification scenarios:
- target-sprint write-only behavior for per-sprint notes
- cross-sprint overwrite prevention
- queue required-field and transition correctness
- unresolved sprint fail-safe behavior with reason codes
- queue/notes mismatch fail-safe behavior
- legacy migration success and unresolved-manual path
- migration idempotency
- backward-compatible legacy pointer behavior
- unreleased queue visibility before finalization
- active/template parity checks

## Constraints

- Keep scope strictly to US-0040 process/artifact behavior.
- Do not introduce deployment runtime changes.
- Keep migration/backfill and mismatch handling non-destructive by default.
- Maintain explicit AC traceability with no plan-verify coverage gaps.

## Done Criteria for Dev Completion

- All 11 tasks in `sprints/S0012/tasks.md` are marked done.
- No uncovered US-0040 acceptance criteria in `sprints/S0012/plan-verify.json`.
- `sprints/S0012/progress.md`, `uat.json`, and `uat.md` are updated with
  execution evidence.
- `docs/engineering/state.md` traceability row advances from `PLANNED` to the
  next lifecycle state with evidence references.

# TL -> Dev Handoff — S0010 + S0011 (US-0038 + US-0039)

## Planning summary

- Sprint split executed per sizing policy (`SPRINT_MAX_TASKS=12`,
  `SPRINT_AUTO_SPLIT=1`):
  - `S0010` for `US-0038` with 11 tasks
  - `S0011` for `US-0039` with 11 tasks
- Split rationale: the combined two-story plan would exceed atomic task design
  once required negative-path testing and template parity work is included.
- Milestone activation check: not applicable for both sprints (no active
  milestone context declared).

## S0010 — US-0038 execution focus

- Goal: deliver policy-driven sync cadence and guarded auto-push semantics.
- Required negative paths:
  - disallowed auto-push on protected/default branch without allowlist
  - disallowed auto-push on failed/missing/timed-out `TEST_COMMAND`
  - disallowed auto-push pre-QA and with unresolved QA blockers
- Mandatory outputs: deterministic sync reason codes and evidence fields in
  state/handoff artifacts.
- Script parity: keep `scripts/validate-and-push.ps1` and
  `scripts/validate-and-push.sh` behaviorally aligned with mandatory
  test-before-push gating.

## S0011 — US-0039 execution focus

- Goal: enforce strict release gate chain:
  `check-in test -> QA -> UAT -> release finalization`.
- Required negative paths:
  - block release on missing/stale/failing test evidence
  - block release on unresolved QA blockers
  - block release on incomplete/placeholder UAT
  - verify no-bypass default behavior
- Override path constraint:
  - only via explicit decision gate with rationale and approver evidence
  - release artifacts must include override evidence pointers when used

## AC traceability readiness

- `S0010`: `sprints/S0010/plan-verify.json` covers `US-0038` AC-1..AC-10 with
  no gaps.
- `S0011`: `sprints/S0011/plan-verify.json` covers `US-0039` AC-1..AC-10 with
  no gaps.
- `docs/engineering/state.md` traceability index includes PLANNED rows for
  `US-0038` and `US-0039`.

## Next execution order

1. Execute `S0010` tasks `T-001..T-011`.
2. Run `/qa` and `/verify-work` for `S0010`.
3. Execute `S0011` tasks `T-001..T-011`.
4. Run `/qa` and `/verify-work` for `S0011`.

## Dev completion note (S0010)

- Dev executed `S0010` task sequence `T-001..T-011` and marked all tasks done.
- US-0038 contract updates are completed across command guidance, runbook/README,
  validate-and-push scripts, regression planning artifacts, and template parity.
- Sprint status is now ready for `/qa` with updated `handoffs/dev_to_qa.md`
  checklist and deterministic sync evidence/reason-code expectations.

# TL -> Dev Handoff — Sprint S0009 (US-0037 Auto Continuation)

## Sprint Overview

Sprint S0009 is planned for US-0037: Mid-Process `/auto` Continuation with
Deterministic Resume Point.

- Story count: 1 (`US-0037`)
- Planned tasks: 9
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required (single sprint)
- Milestone activation: not applicable

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0037 AC-1..AC-9)
- Architecture: `docs/engineering/architecture.md` (US-0037 section)
- Decision: `decisions/DEC-0017.md`
- Sprint artifacts: `sprints/S0009/*`

## Execution Order

Execute tasks T-001 through T-009 sequentially.

| Task | Description | Files | AC |
|------|-------------|-------|----|
| T-001 | Define explicit `/auto start-from=<phase>` contract and canonical phase IDs | `.cursor/commands/auto.md` | AC-1 |
| T-002 | Define deterministic resolver precedence and precedence test coverage | `.cursor/commands/auto.md`, `sprints/S0009/uat.md` | AC-2 |
| T-003 | Define conflict/staleness/unparseable fail-fast behavior and `[AUTO_RESUME_ERROR]` codes | `.cursor/commands/auto.md`, `.cursor/rules/core.mdc`, `sprints/S0009/uat.md` | AC-3 |
| T-004 | Define one-command continuation through remaining phases | `.cursor/commands/auto.md` | AC-4 |
| T-005 | Preserve decision gates and stop-condition behavior | `.cursor/commands/auto.md`, `.cursor/rules/core.mdc` | AC-5 |
| T-006 | Define breadcrumb logging contract for `state.md` and `resume_brief.md` | `.cursor/commands/auto.md`, `.cursor/commands/pause.md`, `.cursor/commands/resume.md`, `docs/engineering/state.md`, `handoffs/resume_brief.md` | AC-6 |
| T-007 | Preserve backward compatibility and safe defaults | `.cursor/commands/auto.md`, `.cursor/commands/resume.md` | AC-7 |
| T-008 | Align `/pause`, `/resume`, `/auto` guidance and update README/runbook | `.cursor/commands/auto.md`, `.cursor/commands/resume.md`, `.cursor/commands/pause.md`, `README.md`, `docs/engineering/runbook.md` | AC-8 |
| T-009 | Verify and enforce active/template continuation parity | `template/.cursor/commands/auto.md`, `template/.cursor/commands/resume.md`, `template/.cursor/commands/pause.md`, `template/README.md`, `template/docs/engineering/runbook.md` | AC-9 |

## Critical Requirements to Preserve

1. `/auto start-from=<phase>` accepts only canonical phase IDs.
2. Resolver precedence is deterministic and ordered:
   argument > resume brief > state fallback > fail-fast.
3. Stale/conflicting/unparseable resume inputs must fail fast with actionable
   `[AUTO_RESUME_ERROR]` output (no guessing).
4. Continuation must preserve existing stop conditions and decision-gate rules.
5. Breadcrumbs must make continuation source and stop reason inspectable.
6. Manual/interactive workflows must remain unchanged by default.
7. Active/template guidance must remain behaviorally aligned.

## QA and Validation Focus

Required verification scenarios:
- precedence resolution with explicit argument override
- precedence resolution without argument (resume brief then state fallback)
- conflict case (`resume_brief` vs inferred `state` phase) with fail-fast
- stale/unparseable resume brief fail-fast handling
- `[AUTO_RESUME_ERROR]` code contract coverage
- stop-condition preservation in continuation mode
- breadcrumb field coverage in `state.md` and `resume_brief.md`
- active/template parity checks

## Constraints

- Keep scope strictly to US-0037.
- Planning assumptions must not bypass decision gates or input blockers.
- Maintain 1:1 task-to-AC mapping (`T-001`..`T-009` -> `AC-1`..`AC-9`).
- Keep changes deterministic and testable with explicit remediation guidance.

## Done Criteria for Dev Completion

- All 9 tasks in `sprints/S0009/tasks.md` are marked done.
- No uncovered US-0037 acceptance criteria in `sprints/S0009/plan-verify.json`.
- `sprints/S0009/progress.md`, `uat.json`, and `uat.md` are updated with
  execution evidence.
- Traceability row in `docs/engineering/state.md` advances from `PLANNED` to
  post-execution lifecycle state with evidence links.
# TL -> Dev Handoff — Sprint S0009 (US-0037 Auto Continuation)

## Sprint Overview

Sprint S0009 is planned for US-0037: Mid-Process `/auto` Continuation with
Deterministic Resume Point.

- Story count: 1 (`US-0037`)
- Planned tasks: 9
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required (single sprint)
- Milestone activation: not applicable

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0037 AC-1..AC-9)
- Architecture: `docs/engineering/architecture.md` (US-0037 section)
- Decision: `decisions/DEC-0017.md`
- Sprint artifacts: `sprints/S0009/*`

## Execution Order

Execute tasks T-001 through T-009 sequentially.

| Task | Description | Files | AC |
|------|-------------|-------|----|
| T-001 | Define explicit `/auto start-from=<phase>` contract and canonical phase IDs | `.cursor/commands/auto.md` | AC-1 |
| T-002 | Define deterministic resolver precedence and precedence test coverage | `.cursor/commands/auto.md`, `sprints/S0009/uat.md` | AC-2 |
| T-003 | Define conflict/staleness/unparseable fail-fast behavior and `[AUTO_RESUME_ERROR]` codes | `.cursor/commands/auto.md`, `.cursor/rules/core.mdc`, `sprints/S0009/uat.md` | AC-3 |
| T-004 | Define one-command continuation through remaining phases | `.cursor/commands/auto.md` | AC-4 |
| T-005 | Preserve decision gates and stop-condition behavior | `.cursor/commands/auto.md`, `.cursor/rules/core.mdc` | AC-5 |
| T-006 | Define breadcrumb logging contract for `state.md` and `resume_brief.md` | `.cursor/commands/auto.md`, `.cursor/commands/pause.md`, `.cursor/commands/resume.md`, `docs/engineering/state.md`, `handoffs/resume_brief.md` | AC-6 |
| T-007 | Preserve backward compatibility and safe defaults | `.cursor/commands/auto.md`, `.cursor/commands/resume.md` | AC-7 |
| T-008 | Align `/pause`, `/resume`, `/auto` guidance and update README/runbook | `.cursor/commands/auto.md`, `.cursor/commands/resume.md`, `.cursor/commands/pause.md`, `README.md`, `docs/engineering/runbook.md` | AC-8 |
| T-009 | Verify and enforce active/template continuation parity | `template/.cursor/commands/auto.md`, `template/.cursor/commands/resume.md`, `template/.cursor/commands/pause.md`, `template/README.md`, `template/docs/engineering/runbook.md` | AC-9 |

## Critical Requirements to Preserve

1. `/auto start-from=<phase>` accepts only canonical phase IDs.
2. Resolver precedence is deterministic and ordered:
   argument > resume brief > state fallback > fail-fast.
3. Stale/conflicting/unparseable resume inputs must fail fast with actionable
   `[AUTO_RESUME_ERROR]` output (no guessing).
4. Continuation must preserve existing stop conditions and decision-gate rules.
5. Breadcrumbs must make continuation source and stop reason inspectable.
6. Manual/interactive workflows must remain unchanged by default.
7. Active/template guidance must remain behaviorally aligned.

## QA and Validation Focus

Required verification scenarios:
- precedence resolution with explicit argument override
- precedence resolution without argument (resume brief then state fallback)
- conflict case (`resume_brief` vs inferred `state` phase) with fail-fast
- stale/unparseable resume brief fail-fast handling
- `[AUTO_RESUME_ERROR]` code contract coverage
- stop-condition preservation in continuation mode
- breadcrumb field coverage in `state.md` and `resume_brief.md`
- active/template parity checks

## Constraints

- Keep scope strictly to US-0037.
- Planning assumptions must not bypass decision gates or input blockers.
- Maintain 1:1 task-to-AC mapping (`T-001`..`T-009` -> `AC-1`..`AC-9`).
- Keep changes deterministic and testable with explicit remediation guidance.

## Done Criteria for Dev Completion

- All 9 tasks in `sprints/S0009/tasks.md` are marked done.
- No uncovered US-0037 acceptance criteria in `sprints/S0009/plan-verify.json`.
- `sprints/S0009/progress.md`, `uat.json`, and `uat.md` are updated with
  execution evidence.
- Traceability row in `docs/engineering/state.md` advances from `PLANNED` to
  post-execution lifecycle state with evidence links.
# TL -> Dev Handoff — Sprint S0008 (US-0036 Remote Config Contract)

## Sprint Overview

Sprint S0008 is planned for US-0036: Official Remote Config Template, Docs, and
Fail-Fast Validation.

- Story count: 1 (`US-0036`)
- Planned tasks: 10
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required (single sprint)
- Milestone activation: not applicable

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0036 AC-1..AC-9)
- Architecture: `docs/engineering/architecture.md` (US-0036 section)
- Decision: `decisions/DEC-0016.md`
- Sprint artifacts: `sprints/S0008/*`

## Execution Order

Execute tasks T-001 through T-010 sequentially.

| Task | Description | Files | ACs |
|------|-------------|-------|-----|
| T-001 | Add canonical active remote config template | `.cursor/remote.json` | AC-1, AC-3 |
| T-002 | Add template remote config parity | `template/.cursor/remote.json` | AC-1, AC-9 |
| T-003 | Define schema/contract guidance | `.cursor/commands/execute.md`, `.cursor/rules/core.mdc` | AC-2 |
| T-004 | Define mode-aware validation trigger behavior | `.cursor/commands/execute.md`, `.cursor/rules/core.mdc` | AC-4, AC-6 |
| T-005 | Define actionable fail-fast error format | `.cursor/commands/execute.md`, `.cursor/rules/quality.mdc` | AC-5, AC-4 |
| T-006 | Add security constraints for remote config | `.cursor/rules/coding-standards.mdc`, `.cursor/commands/execute.md` | AC-7 |
| T-007 | Update README remote setup and behavior docs | `README.md` | AC-3, AC-8 |
| T-008 | Update runbook validation guidance | `docs/engineering/runbook.md` | AC-4, AC-5, AC-6, AC-8 |
| T-009 | Plan/add positive + negative QA coverage | `tests/run-tests.ps1`, `tests/run-tests.sh`, `sprints/S0008/uat.md` | AC-4, AC-5, AC-6, AC-7, AC-8, AC-9 |
| T-010 | Final state/traceability and handoff cross-reference update | `docs/engineering/state.md`, `handoffs/tl_to_dev.md` | AC-9 |

## Critical Requirements to Preserve

1. Mode-aware behavior:
   - Validate remote config only when `REMOTE_EXECUTION=1`.
   - Skip remote validation entirely when `REMOTE_EXECUTION=0`.
2. Fail-fast requirement:
   - Missing, malformed, semantically invalid, or insecure config must fail fast
     in remote-enabled mode.
3. Error message contract:
   - Include field/path, expected rule, actual value/type, and remediation hint.
4. Security posture:
   - No committed secrets in `.cursor/remote.json`.
   - Use environment variable references for sensitive values.
5. Parity:
   - Active and `template/` copies must stay behaviorally aligned.
   - README and runbook guidance must not contradict each other.

## QA and Validation Focus

Negative-path coverage is mandatory in this sprint. Ensure test planning includes:
- missing `.cursor/remote.json` with `REMOTE_EXECUTION=1`
- malformed JSON syntax
- invalid enum/type/semantic values (e.g., bad target type, missing required field)
- secret-like inline values in config
- confirmation that `REMOTE_EXECUTION=0` avoids false-fail checks

Positive-path coverage should confirm:
- valid config passes in remote-enabled mode
- example targets and docs references remain consistent across active/template

## Constraints

- Keep scope strictly to US-0036.
- Do not implement remote transport backends or external secret manager logic.
- Keep edits atomic and testable with explicit AC mapping.
- Maintain template parity as a first-class requirement, not a follow-up.

## Done Criteria for Dev Completion

- All 10 tasks in `sprints/S0008/tasks.md` moved from pending to done.
- No uncovered US-0036 acceptance criteria.
- `sprints/S0008/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- Traceability row in `docs/engineering/state.md` advanced from `PLANNED` to the
  next lifecycle status with evidence links.

## Dev completion note

Dev execution completed for S0008. All T-001..T-010 tasks are marked done and
the sprint is handed off via `handoffs/dev_to_qa.md` for QA verification.

---

## Research readiness brief — BUG-0003 (pre-architecture)

- `orchestrator_run_id=auto-20260331-03`
- completed phase: `research` (`tech-lead`)
- next scheduled phase: `architecture`

### What architecture must lock

1. Required-script source of truth for installer completeness in `missing` and `upgrade`:
   - preferred: manifest-authoritative (`docs/engineering/context/installer-owned-paths.manifest`).
2. Deterministic post-install completeness diagnostics for required scripts:
   - include stable reason code contract on missing framework-critical script(s).
3. Triple-installer parity strategy:
   - keep mode semantics aligned across `installer.ps1`, `installer.sh`, `installer.py`,
     with shared validation logic where practical.
4. Regression/test obligations:
   - positive `missing`/`upgrade` completeness checks + negative missing-script fixture;
     ensure active/template parity coverage.

### Key research anchor

- `docs/engineering/research.md` (`R-0061`)
