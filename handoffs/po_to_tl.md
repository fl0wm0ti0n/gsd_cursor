## Discovery Addendum — US-0045

### Discovery focus and references

- Discovery objective: refine `US-0045` from intake scope into architecture-ready
  status-contract boundaries and operator-facing drift diagnostics.
- References captured:
  - product vision value statement for single-source status trust
  - current artifact set: `backlog.md`, `acceptance.md`, `state.md`
  - release boundary reconciliation precedent from `US-0043`
  - research anchor: `R-0009`

### Discovery conclusions for TL

- Canonical ownership should be explicit and singular:
  - `docs/product/backlog.md` owns story `OPEN|DONE`.
- Secondary artifacts should be treated as derived/reconciled views:
  - `docs/product/acceptance.md` for portfolio checklist visibility.
  - `docs/engineering/state.md` for checkpoint/evidence traceability.
- Historical drift already exists and needs one-time normalization before strict
  guardrails can become reliable.
- Operator UX must prefer deterministic explainability over silent mutation:
  emit per-story mismatch evidence and remediation guidance.

### Research handoff targets

1. Define precedence and conflict-resolution semantics when backlog, acceptance,
   and state disagree.
2. Define normalization entry criteria and safe mutation scope (targeted writes
   only, no broad rewrites).
3. Define reason-code contract for contradictory states and where the contract
   is enforced in release/reconciliation flow.
4. Define regression matrix for:
   - pre-existing drift normalization
   - post-normalization drift prevention
   - non-target-story non-mutation guarantees

### Recommendation

- Proceed to `/research` for `US-0045` with emphasis on deterministic precedence
  model, auditable normalization report schema, and fail-safe reason-code design.

---

## Intake Addendum — Explicit Bulk Planning + Bulk Execution Modes

### New intake

User requests two explicit high-autonomy capabilities:
1. Bulk sprint planning mode so one command can plan many OPEN stories.
2. Bulk execution mode so planned sprints/stories run with fresh agent contexts
   and execute↔QA loops until bounded stop conditions.

### Overlap and duplicate evaluation

- Related stories:
  - `US-0023`: fresh subagent context per phase/handoff (already established).
  - `US-0044`: optional `/auto` backlog-drain mode with bounded controls.
  - `US-0045`: canonical status source and drift guard.
- Assessment:
  - not a duplicate of `US-0044`; this intake requests explicit command-level
    bulk modes (especially for planning) rather than only flag-driven behavior.
  - complements `US-0023`; preserves and operationalizes fine-granular context
    isolation in explicit bulk execution semantics.
  - compatible with `US-0045`; status integrity remains orthogonal to planning/
    execution batching behavior.
- Research reference:
  - `R-0010` (explicit bulk modes + deterministic bounded orchestration).
- Decision:
  - create two dedicated stories: `US-0046` (bulk sprint planning) and
    `US-0047` (bulk execute orchestration).

### Accepted stories

#### US-0046 — Explicit `/sprint-plan --bulk` Mode
- Priority: P1
- Status: OPEN
- Intent: allow explicit, bounded planning of multiple OPEN stories in one run
  while preserving sizing/splitting safety.

#### US-0047 — Explicit Bulk Execute Orchestration Mode
- Priority: P1
- Status: OPEN
- Intent: allow explicit, bounded multi-item execution with mandatory fresh
  subagent isolation and deterministic execute↔QA loop controls.

### TL guidance and boundaries

- In scope:
  - explicit mode contracts for bulk planning and bulk execution
  - deterministic selection/grouping and bounded limits
  - stop/skip reason-code semantics and breadcrumb auditability
  - strict preservation of decision gates and fail-safe behavior
  - active/template parity for command/rule/docs updates
- Out of scope:
  - runtime product feature changes
  - bypassing release/decision safety controls
  - replacing artifact-first handoff model

### Suggested implementation order

1. `US-0046` first to make backlog-to-sprint generation explicit and bounded.
2. `US-0047` second to consume planned backlog/sprint scope in autonomous runs
   with strict context isolation guarantees.

## Discovery Addendum — US-0046 and US-0047

### Discovery focus and references

- Discovery objective: convert intake-level bulk-mode intent into architecture-
  ready orchestration constraints with deterministic safety boundaries.
- References captured:
  - existing `/auto` bounded backlog-drain semantics (`US-0044`)
  - fresh-context isolation contract (`US-0023`)
  - team-local context fields (`TEAM_MODE`, `TEAM_MEMBER`, `ACTIVE_TASK_IDS`)
  - research anchor: `R-0010`

### Discovery conclusions for TL

- Bulk behavior should be command-explicit, not implicit:
  - normal mode stays lightweight and predictable
  - bulk mode activates only on explicit operator intent.
- `US-0046` should remain planning-only:
  - may generate multiple sprint plans in one run
  - must preserve all sizing/splitting and completeness guarantees.
- `US-0047` should remain execution-only:
  - consumes planned scope
  - preserves strict fresh-context isolation and execute↔QA loop safety bounds.
- Team mode must be execution-scoping aware in bulk runs:
  - only in-scope member tasks execute
  - out-of-scope tasks are deterministically skipped/blocked with reason codes.

### Research handoff targets

1. Define explicit bulk-mode triggers and precedence when both normal and bulk
   inputs are present.
2. Define deterministic selection/grouping policies and boundary-limit behavior
   for `US-0046`.
3. Define deterministic execution selection, skip/stop semantics, and resume
   checkpoint schema for `US-0047`.
4. Define team-context enforcement contract (`TEAM_MEMBER`/`ACTIVE_TASK_IDS`)
   and failure/skip reason-code vocabulary.
5. Define regression matrix for positive throughput, bounded-stop behavior, and
   non-execution of out-of-scope tasks.

### Recommendation

- Proceed to `/research` for `US-0046` and `US-0047` with emphasis on
  deterministic explicit-mode contracts, member-scope enforcement, and bounded
  orchestration safety.

---

# PO -> TL Handoff — Intake: Install Hygiene + Smart Intake + Bootstrap IDs

## Intake context (fresh PO run)

User reported real-world first-time install and cleanup trust gaps in external repos:

1. `--clean-repo` leaves framework artifacts behind.
2. Fresh installs still contain starter references/history that look like copied memory.
3. Broad intake still collapses into one oversized story with too few PO follow-up questions.
4. Fresh-project teams want optional ID bootstrap (`US-0001` / `DEC-0001`).

## Duplicate/overlap evaluation

- Related stories:
  - `US-0018` (upgrade mode), `US-0019` (placeholder cleanup), `US-0041` (installer lifecycle QA), `US-0033` (guided intake behavior), `US-0046`/`US-0047` (bulk planning/execution).
- Assessment:
  - No direct duplicate for end-to-end clean-install hygiene + complete clean-repo coverage + starter neutrality policy.
  - No direct duplicate for intake decomposition heuristics plus risk-aware questioning.
  - No direct duplicate for explicit fresh-project ID namespace bootstrap.
- Decision:
  - Split into three stories (`US-0050`, `US-0051`, `US-0052`) to avoid one oversized mixed-scope intake.

## Accepted stories

### US-0050 — Clean Install Hygiene and Complete Clean-Repo Coverage
- Priority: P1
- Status: OPEN
- Intent: deterministic fresh install without seeded history + deterministic complete cleanup of installer-owned artifacts.

### US-0051 — Intelligent Intake Decomposition and Risk-Aware PO Questioning
- Priority: P1
- Status: OPEN
- Intent: decompose broad intake into multiple focused stories and increase questioning depth based on scope/risk (not ambiguity only).

### US-0052 — Optional Fresh-Project ID Namespace Bootstrap
- Priority: P2
- Status: OPEN
- Intent: allow explicit bootstrap of IDs from 0001 in truly fresh repos while preserving highest-existing continuation for non-fresh repos.

## Research reference

- `R-0024`: starter/template hygiene, deterministic cleanup ownership, vertical-slice story splitting, and adaptive elicitation questioning patterns.

## TL boundaries

- In scope:
  - installer cleanup ownership contract and parity across PS1/SH/PY.
  - starter artifact neutralization policy for template docs.
  - intake decomposition and adaptive PO questioning contracts.
  - optional ID bootstrap with deterministic eligibility rules.
  - regression coverage and active/template parity.
- Out of scope:
  - runtime product feature behavior changes.
  - retroactive renumbering of existing project histories.
  - bypassing existing release/decision-gate safety contracts.

## Risks

- Cleanup scope expansion could accidentally remove non-framework files if ownership rules are unclear.
- Intake decomposition may over-split without bounded heuristics and explicit user approval.
- Bootstrap ID mode could collide with existing repos if freshness detection is weak.

## Recommendation

1. Architecture first on `US-0050` (ownership manifest + cleanup safety + starter neutrality).
2. Then `US-0051` (decomposition heuristics + risk-aware questioning with bounded prompts).
3. Then `US-0052` (explicit bootstrap mode with deterministic fresh-repo detection).
4. Ensure parity/regression checks are planned as first-class tasks in the same sprint sequence.

## Next phase

- Proceed to `/research` for `US-0050`, `US-0051`, and `US-0052` (or `/architecture` directly if research depth is considered sufficient via `R-0024`).

---

## PO → TL Handoff — US-0076 (Intake)

> Placement note: appended after **DEC-0054** rollover archived the prior top copy into `handoffs/archive/po-to-tl-pack-20260324.md`; TL read model uses file **tail** (runbook).

### New intake

User requests **executable** behavior: scratchpad **`SYNC_POLICY_MODE`**, **`ALLOW_AUTO_PUSH`**, and **`AUTO_PUSH_BRANCH_ALLOWLIST`** should **drive** whether/when **git push** runs — not remain **policy-only** relative to **`validate-and-push`**.

### Overlap

- **US-0038** (DONE): eligibility contract — **US-0076** implements the missing **script/operator** linkage.
- **DEC-0018**: amend or extend with **DEC-0058** (execute phase) for “scratchpad + script” contract.

### Decomposition

- **Single story** **US-0076** — scratchpad parse/merge, gate chain, script changes, docs, tests, decision.

### Intake pack

- selected_pack=`small-intake-pack`
- asked_topics=`outcome_success_criteria`,`impacted_components`,`constraints_compatibility_risks`,`required_tests_acceptance_checks`,`done_definition`
- missing_topics=`(none)`
- assumptions_confirmed=`(none)`

### TL scope

- Prefer **extend `validate-and-push.ps1` / `.sh`** to read **merged** scratchpad; add **dry-run** / **reason-code** exits; map **`by_phase`** to **explicit invocation** contract unless architecture selects **state.md** phase reader.
- **AC-5** QA blocking rule needs a **bounded, testable** definition.
- Research: **`R-0053`**.

### Recommendation

**`/discovery`** → **`/research`** (finalize **R-0053**) → **`/architecture`** (**`DEC-0058`**) → **`/sprint-plan`**.

---

## Discovery Addendum — US-0076

> Placement: **tail** hot copy after **DEC-0054** rollover archived an earlier **prepend** into
> `handoffs/archive/po-to-tl-pack-20260327-a.md` (same wording).

- **Scope**: Executable merged-scratchpad wiring for **`SYNC_*`**, **`ALLOW_AUTO_PUSH`**, and
  **`AUTO_PUSH_BRANCH_ALLOWLIST`** so opt-in push honors the **US-0038** gate chain with
  deterministic reason codes; **no** behavior change when auto-push is off.
- **Conclusions**: Gap validated (**R-0053**): **`validate-and-push`** currently does not enforce
  scratchpad merge inputs. **PO** recommends extending **`validate-and-push`** (PS1/SH parity) over
  new entrypoints unless architecture mandates a split. **`by_phase`**/**`by_milestone`** need an
  explicit boundary signal at invocation (not implicit Cursor phase). **AC-5** QA blocking rule
  must be architecture-bounded (sprint artifact contract).
- **Next recommendation**: Proceed with **`/research`** ( **`R-0053`** current) then **`/architecture`**
  to lock phase-boundary input, QA scan rule, installer/Python merge reuse vs duplicate, and
  **DEC-0058** / **DEC-0018** amendment plan.
- **Artifacts**: `docs/product/vision.md` (Discovery Notes — US-0076), `docs/product/backlog.md`
  (US-0076 discovery refinements), `docs/engineering/research.md` (**R-0053**).

---

## Research Addendum — US-0076 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with prepended **Research Addendum — US-0076**). `orchestrator_run_id=auto-20260327-01`.

- **Closure**: **`/research`** (TL) complete for **US-0076**; **`R-0053`** extended with implementation anchors + mitigations.
- **Anchors**: **`validate-and-push.ps1`/`.sh`** — merged scratchpad gate before push; prefer **`installer.py`** `merge_scratchpad_layers` / `parse_scratchpad_file`; runbook remains command source only.
- **Boundaries**: **`by_phase`** default = invocation as boundary unless architecture fixes **`state.md`/env/CLI**; **AC-5** = bounded **`qa-findings.md`** scan + sprint path in architecture.
- **Next**: **`/architecture`** — **DEC-0058** (or **DEC-0018** amendment), QA glob, dry-run/exit codes, **AC-8** tests.

---

## Architecture Addendum — US-0076 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with prepended **Architecture Addendum — US-0076**). `orchestrator_run_id=auto-20260327-01`.

- **Decision**: **`decisions/DEC-0058.md`** accepted — executable scratchpad → **validate-and-push**; **`DEC-0018`** policy authority retained.
- **AC-5**: **`sprints/S*/qa-findings.md`** bounded scan per **DEC-0058** §6.
- **Phase signal**: default **invocation**; optional **`SYNC_PHASE_BOUNDARY`** env.
- **Next**: **`/sprint-plan`**.

---

## Discovery Addendum — US-0077 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with prepended **Discovery Addendum — US-0077**). `orchestrator_run_id=auto-20260327-02`.

- **Scope**: Documentation audience/depth profiles + dual README strategy; preserve **US-0030** / **US-0031** / **US-0032** / **US-0071**; anchor **R-0054**.
- **Conclusions**: Ownership matrix + bounded sections/split preferred; profile validation with deterministic reason codes; **US-0071** on user-visible outputs.
- **Next**: **`/sprint-plan`** — **`/architecture`** complete (**`DEC-0059`**).
- **Decision gate before research** (historical): **none**.
- **Artifacts**: `docs/product/vision.md`, `docs/product/backlog.md`, `handoffs/po_to_tl.md`, `docs/engineering/state.md`, `docs/engineering/research.md` (**R-0054**).

---

## Research Addendum — US-0077 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with prepended **Research Addendum — US-0077**). `orchestrator_run_id=auto-20260327-02`.

- **Closure**: **`/research`** (TL) complete; **`R-0054`** — profile matrix + validation tiers + reason-code draft.
- **Next**: **`/sprint-plan`** — **`/architecture`** complete (**`DEC-0059`**).
- **Decision gate before architecture**: **none** (closed).

---

## Architecture Addendum — US-0077 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with prepended **Architecture Addendum — US-0077**). `orchestrator_run_id=auto-20260327-02`.

- **Decision**: **`decisions/DEC-0059.md`** — dual README (**`USER_*`** / **`DEV_*`**), validator **`scripts/validate_doc_profile.py`**, tiered **AC-8**, **`US-0030`** parity + manifest path for **`docs/developer/README.md`**.
- **Next**: **`/sprint-plan`**.
- **Decision gate before sprint-plan**: **none**.

---

## Discovery Addendum — US-0078 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with archived **Discovery Addendum — US-0078** in **`handoffs/archive/po-to-tl-pack-20260328-b.md`**). `orchestrator_run_id=auto-20260328-01`.

- **Scope**: Runtime intake question-pack **evidence** before persistence (**US-0068** / **DEC-0050**); per-topic **`answer_ref`** or explicit assumption-confirmation ref; reject unverifiable **`assumptions_confirmed`**.
- **Conclusions**: Persist **`asked_topics`** vs answered/coverage evidence; **guided** and **low-touch** both **fail closed** without proof; extend **`R-0055`** then **DEC** for schema + migration.
- **Next**: **`/architecture`** for **`US-0078`** (**`/research`** complete; **`R-0055`** refined).
- **Decision gate before research** (historical): **none**.

---

## Research Addendum — US-0078 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with prepended **Research Addendum — US-0078**, archived to **`handoffs/archive/po-to-tl-pack-20260328-d.md`** on post-research triad rollover). `orchestrator_run_id=auto-20260328-01`.

- **Closure**: **`/research`** (**tech-lead**) complete; **`R-0055`** — schema, rules, **AC-8** tiers.
- **Next**: **`/architecture`** — **DEC-0050** / DEC for **`ref`** format + migration.
- **Decision gate before architecture**: **none**.

---

## Architecture Addendum — US-0078 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with prepended **Architecture Addendum — US-0078**). `orchestrator_run_id=auto-20260328-01`.

- **Decision**: **`decisions/DEC-0060.md`** — **`ie:`** **`ref`** binding; extends **`DEC-0050`**; grandfather migration until next intake mutation.
- **Architecture**: **`docs/engineering/architecture.md`** **`# US-0078`**.
- **Next**: **`/sprint-plan`**.
- **Decision gate before sprint-plan**: **none**.

---

## PO → TL Handoff — US-0080 (Intake)

- **Orchestrator**: **`auto-20260329-02`** — intake complete in fresh **PO** context.
- **Evidence**: **`handoffs/intake_evidence/US-0080-intake-20260329.json`** — **`[INTAKE_EVIDENCE_VALIDATION_OK]`** (`small-intake-pack`, **`ie:`** per **DEC-0060**).
- **Research anchor**: **`R-0057`** (current) — structural levers (command/context slimming, comparable-run measurement); **`TOKEN_PROFILE=lean`** alone insufficient.
- **Alternatives**: **(1)** status quo pricing tolerance — rejected; **(2)** profile-only — rejected; **(3)** slimming + bounded phase-context + auditable metrics — **recommended** (aligned with backlog).
- **Artifacts**: **`docs/product/backlog.md`** (US-0080 intake closure + topic_coverage), **`docs/product/vision.md`** (intake closure line), **`handoffs/resume_brief.md`** → **`/discovery`**, **`docs/engineering/state.md`** (isolation + strict proof + phase boundary; triad rollover **`docs/engineering/state-archive/state-pack-20260329-m.md`**).
- **Next**: **`/discovery`** for **`US-0080`**, then **`/research`** / **`/architecture`** to lock metric definitions and **DEC** for **AC-10** trade-offs.
- **Decision gate before discovery**: **none** (intake evidence satisfied).

---

## PO → TL Handoff — US-0080 (Discovery)

- **Orchestrator**: **`auto-20260329-02`** — discovery complete in fresh **PO** context.
- **Evidence**: **`docs/product/backlog.md`** (US-0080 discovery notes), **`docs/product/vision.md`** (**Discovery Notes — US-0080**), **`docs/engineering/state.md`** (Discovery checkpoint + strict proof); research anchor remains **`R-0057`** (current).
- **Findings**: Dominant lever is **structural** — reduce repeated large command/policy prefixes and tighten **per-phase context packs** while preserving mandatory gates; **`TOKEN_PROFILE=lean`** alone insufficient.
- **Research asks**: Deterministic **run-class/baseline** for AC-1/AC-2; **metric/evidence** placement contract; **active/template** parity list for slimmed orchestration surfaces.
- **Risks**: Over-slimming obscuring policy; baseline drift enabling metric gaming; template divergence.
- **Artifacts**: **`handoffs/resume_brief.md`** → **`/research`** for **`US-0080`**.
- **Next**: **`/research`** (then **`/architecture`**) to lock metric definitions and **DEC** for **AC-10** trade-offs.
- **Decision gate before research**: **none** (discovery satisfied).

---

## PO → TL Handoff — US-0080 (Research)

- **Orchestrator**: **`auto-20260329-02`** — research complete in fresh **tech-lead** context.
- **Evidence**: **`docs/engineering/research.md`** **`R-0057`** (extension + research closure line);
  **`docs/product/backlog.md`** / **`docs/product/vision.md`** (research closure notes);
  **`docs/engineering/state.md`** (Research checkpoint + strict proof; triad rollover
  **`docs/engineering/state-archive/state-pack-20260329-o.md`**).
- **Findings**: **Run-class tuple** frozen for AC-1/AC-2 comparability; **append-only in-repo metric
  records** + **`state.md`** pointer for AC-6; **explicit parity manifest** for `.cursor/commands/`,
  `.cursor/rules/`, `template/` mirrors (AC-3/AC-9); vendor **`cache_read_input_tokens`** semantics
  as conceptual anchor for metric naming in upcoming **DEC**.
- **Artifacts**: **`handoffs/resume_brief.md`** → **`/architecture`** for **`US-0080`**.
- **Next**: **`/architecture`** to lock **`architecture.md`** story section + **DEC** for AC-10.
- **Decision gate before architecture**: **none** (research satisfied; story **OPEN**).

---

## Architecture Addendum — US-0080 (tail mirror)

- **Orchestrator**: **`auto-20260329-02`** — architecture complete in fresh **tech-lead** context.
- **Evidence**: **`decisions/DEC-0062.md`**; **`docs/engineering/architecture.md`** **`# US-0080`**;
  **`docs/engineering/decisions.md`** (context pack + **`DEC-0062`** index); **`docs/engineering/research.md`**
  **`R-0057`** architecture closure line; **`docs/engineering/state.md`** (Architecture checkpoint + strict
  proof; triad rollover if hot-surface enforcement runs post-append).
- **Decision**: **`DEC-0062`** — metric fields, **`run_class_hash`**, **`handoffs/token_cost_runs/`** channel,
  **`token_cost_evidence_ref`**, parity manifest, AC-10 trade-offs / phase boundary visibility.
- **Artifacts**: **`docs/product/backlog.md`**, **`docs/product/vision.md`** (architecture closure),
  **`handoffs/tl_to_dev.md`**, **`handoffs/resume_brief.md`** → **`/sprint-plan`**.
- **Next (historical)**: **`/sprint-plan`** — satisfied by **Sprint-plan Addendum** below.
- **Decision gate before sprint-plan**: **none** (architecture satisfied).

---

## Sprint-plan Addendum — US-0080 / S0059 (tail mirror)

- **Orchestrator**: **`auto-20260329-02`** — sprint-plan complete in fresh **tech-lead** context.
- **Evidence**: **`sprints/S0059/sprint.md`**, **`sprints/S0059/tasks.md`**, **`sprints/S0059/plan-verify.json`** (**PENDING**); **`docs/engineering/state.md`** (Sprint-plan checkpoint + strict proof); **`handoffs/tl_to_dev.md`**, **`handoffs/resume_brief.md`**, **`handoffs/qa_plan_verify.md`**.
- **Sprint**: **`S0059`** — **T-001..T-010** ↔ **AC-1..AC-10**; governance **`DEC-0062`**, **`# US-0080`**, **`R-0057`**.
- **Next**: **`/plan-verify`** for **`S0059`** / **`US-0080`** (story **OPEN**).
- **Decision gate before plan-verify**: **none** (sprint artifacts materialized).

---

## Plan-verify Addendum — US-0080 / S0059 (tail)

- **Orchestrator**: **`auto-20260329-02`** — plan-verify **PASS** in fresh **qa** context (**`2026-03-29T21:00:00Z`**).
- **Evidence**: **`sprints/S0059/plan-verify.json`** (**PASS**); **`docs/engineering/state.md`** (plan-verify checkpoint + strict proof); **`handoffs/tl_to_dev.md`**, **`handoffs/resume_brief.md`**, **`handoffs/qa_plan_verify.md`**.
- **Sprint**: **`S0059`** — story **`US-0080`** **OPEN** (**US-0045**).
- **Next**: **`/execute`** for **`S0059`** / **`US-0080`**.
- **Decision gate before execute**: **none** (plan-verify satisfied).

---

## Execute Addendum — US-0080 / S0059 (tail)

- **Orchestrator**: **`auto-20260329-02`** — **`/execute`** complete in fresh **dev** context (**`2026-03-29T22:15:00Z`**).
- **Evidence**: **`sprints/S0059/summary.md`**, **`sprints/S0059/tasks.md`** (**T-001..T-010** **done**), **`handoffs/dev_to_qa.md`**, **`handoffs/token_cost_runs/auto-20260329-02.md`**, **`docs/engineering/token-cost-parity-manifest.md`**, **`docs/engineering/state.md`** (execute checkpoint + strict proof); reduced-length **`/auto`** + **`docs/engineering/auto-orchestration-reference.md`**.
- **Governance**: **`DEC-0062`** (**§6** trade-offs), **`architecture.md`** **`# US-0080`**, **`R-0057`** — story **`OPEN`** (**US-0045**).
- **Next**: **`/qa`** for **`S0059`** / **`US-0080`**.
- **Decision gate before qa**: **none** (execute satisfied for dev scope).

---

## Discovery Addendum — US-0081

- **Orchestrator**: **`auto-20260331-01`** — discovery complete in fresh **PO** context.
- **Evidence**: **`docs/product/backlog.md`** (US-0081 discovery checkpoint note), **`docs/engineering/state.md`** (discovery checkpoint + strict proof), **`handoffs/resume_brief.md`** (resume target set to research).
- **Findings**: First/new/broad intake must produce deterministic complete-plan accounting before persistence. Discovery defines required mapping contract for research: normalized `plan_area_inventory`; coverage binding `plan_area_id -> story_id[] | deferred_ref`; fail-closed gap handling via `INTAKE_PLAN_COVERAGE_MISSING` under `INTAKE_PERSISTENCE_BLOCKED`; bounded decomposition allowed but no silent omission of major plan areas.
- **Research handoff scope**: finalize machine-verifiable schema fields and validator behavior, lock deterministic diagnostics/remediation text, and define parity/test matrix for active + `template/` intake surfaces.
- **Status authority**: story remains **`OPEN`** in **`docs/product/backlog.md`** per **US-0045**.
- **Next**: **`/research`** for **`US-0081`**.
- **Decision gate before research**: **none** (discovery checkpoint satisfied).

---

## Research Addendum — US-0081 (tail)

- **Orchestrator**: **`auto-20260331-01`** — research complete in fresh **tech-lead** context.
- **Evidence**: **`docs/engineering/research.md`** (**`R-0059`**), **`docs/product/backlog.md`** (US-0081 research closure line, status still **OPEN**), **`docs/engineering/state.md`** (research checkpoint + strict proof), **`handoffs/resume_brief.md`** (resume target set to architecture).
- **Findings**: Lock deterministic first-intake coverage gate pattern: normalize `plan_area_inventory`; require total `plan_area_id -> story_id[] | deferred_ref` coverage; fail closed on unmapped major areas with `INTAKE_PLAN_COVERAGE_MISSING` under `INTAKE_PERSISTENCE_BLOCKED`; preserve backlog status authority (US-0045). Regression scope: pass/fail/defer matrix + active/template parity checks.
- **Next**: **`/architecture`** for **`US-0081`**.
- **Decision gate before architecture**: **none** (research checkpoint satisfied; story remains **OPEN**).

---

## Architecture Addendum — US-0081 (tail)

- **Orchestrator**: **`auto-20260331-01`** — architecture complete in fresh **tech-lead** context.
- **Evidence**: **`decisions/DEC-0064.md`**; **`docs/engineering/architecture.md`** **`# US-0081`**; **`docs/product/backlog.md`** (`architecture_notes`, status still **OPEN**); **`docs/engineering/decisions.md`** (index update); **`docs/engineering/state.md`** (architecture checkpoint + strict proof); **`handoffs/tl_to_dev.md`**; **`handoffs/resume_brief.md`**.
- **Decision**: **`DEC-0064`** — deterministic first/new/broad intake coverage gate: normalized `plan_area_inventory`, total `plan_area_id -> story_ids[] | deferred_ref` contract, fail-closed `INTAKE_PERSISTENCE_BLOCKED` subcodes, and pass/fail/defer verification + active/template parity requirements.
- **Status authority**: **`docs/product/backlog.md`** remains canonical; **`US-0081`** stays **OPEN** (**US-0045**).
- **Next**: **`/sprint-plan`** for **`US-0081`**.
- **Decision gate before sprint-plan**: **none** (architecture satisfied).

---

## Sprint-plan Addendum — US-0081 / S0061 (tail)

- **Orchestrator**: **`auto-20260331-01`** — sprint-plan complete in fresh **tech-lead** context.
- **Evidence**: **`sprints/S0061/sprint.md`**, **`sprints/S0061/tasks.md`**, **`sprints/S0061/plan-verify.json`** (**PENDING**), **`sprints/S0061/summary.md`**, **`sprints/S0061/qa-findings.md`**, **`sprints/S0061/uat.json`**, **`sprints/S0061/uat.md`**, **`sprints/S0061/release-findings.md`**; **`docs/product/backlog.md`** (`sprint_plan_notes`, status still **OPEN**); **`handoffs/tl_to_dev.md`**, **`handoffs/qa_plan_verify.md`**, **`handoffs/resume_brief.md`**, **`docs/engineering/state.md`** sprint-plan checkpoint + strict proof.
- **Sprint**: **`S0061`** — deterministic mapping **AC-1..AC-10** ↔ **T-001..T-010**.
- **Status authority**: **`docs/product/backlog.md`** remains canonical; **`US-0081`** stays **OPEN** (**US-0045**).
- **Next**: **`/plan-verify`** for **`S0061`** / **`US-0081`**.
- **Decision gate before plan-verify**: **none** (sprint artifacts materialized; QA verification pending).

---

## Plan-verify Addendum — US-0081 / S0061 (tail)

- **Orchestrator**: **`auto-20260331-01`** — plan-verify **PASS** in fresh **qa** context (**`2026-03-31T12:15:00Z`**).
- **Evidence**: **`sprints/S0061/plan-verify.json`** (**PASS**), **`sprints/S0061/sprint.md`**, **`sprints/S0061/summary.md`**, **`docs/product/backlog.md`** (`plan_verify_notes`, status still **OPEN**), **`docs/engineering/state.md`** (plan-verify checkpoint + isolation + strict proof), **`handoffs/tl_to_dev.md`**, **`handoffs/qa_plan_verify.md`**, **`handoffs/resume_brief.md`**.
- **Verdict**: Deterministic AC-to-task coverage verified (**AC-1..AC-10** ↔ **T-001..T-010**, no gaps) and governance alignment confirmed against **`DEC-0064`**, **`architecture.md`** **`# US-0081`**, and **`R-0059`**.
- **Status authority**: **`docs/product/backlog.md`** remains canonical; **`US-0081`** stays **OPEN** (**US-0045**).
- **Next**: **`/execute`** for **`S0061`** / **`US-0081`**.
- **Decision gate before execute**: **none** (plan-verify satisfied).

---

## Orchestrated intake handoff — US-0082 / auto-20260331-02

### Target

- `story_id=US-0082`
- `orchestrator_run_id=auto-20260331-02`
- phase completed: **`intake`** (**`po`**)
- `next_scheduled_phase=discovery`

### Summary

- Prior **`small-intake-pack`** evidence remains authoritative: **`handoffs/intake_evidence/US-0082-intake-20260331.json`** (`intake_run_id=manual-20260331-US0082-intake`). This run records the formal **`/auto`** intake boundary in **`docs/engineering/state.md`** only.
- Canonical backlog **Status** stays **OPEN** (**US-0045**); acceptance portfolio row for **US-0082** stays unchecked.
- Next: **`/discovery`** — refine lifecycle touchpoints for **`docs/engineering/codebase-map.md`**, ownership-safe triggers, **`/map-codebase`** manual path, diagnostics, and active/template parity scope already listed in **AC-1..AC-10**.

### Evidence refs

- `docs/product/backlog.md` (**`## US-0082`**)
- `docs/product/vision.md` (**Intake Notes — US-0082**)
- `handoffs/intake_evidence/US-0082-intake-20260331.json`
- `docs/engineering/state.md` (**Intake checkpoint (2026-03-31) — US-0082 / auto-20260331-02**)

---

## Orchestrated discovery handoff — US-0082 / auto-20260331-02

### Target

- `story_id=US-0082`
- `orchestrator_run_id=auto-20260331-02`
- phase completed: **`discovery`** (**`po`**)
- `next_scheduled_phase=research`

### Summary

- Discovery treated **AC-1..AC-10** and **Boundaries** in **`docs/product/backlog.md`** as the bounded problem statement; no backlog status mutation (**US-0045**).
- **`/research`** should produce **`R-####`** findings on lifecycle hook options, **`/map-codebase`** behavior, ownership-safe triggers, diagnostics, and parity/test expectations—without preempting **`/architecture`**.

### Evidence refs

- `docs/product/backlog.md` (**`## US-0082`** — discovery closure bullet)
- `handoffs/intake_evidence/US-0082-intake-20260331.json`
- `docs/engineering/state.md` (**Discovery checkpoint (2026-03-31) — US-0082 / auto-20260331-02**)
- `handoffs/resume_brief.md`

---

## Orchestrated research handoff — US-0082 / auto-20260331-02

### Target

- `story_id=US-0082`
- `orchestrator_run_id=auto-20260331-02`
- phase completed: **`research`** (**`tech-lead`**)
- `next_scheduled_phase=architecture`

### Summary

- **`R-0060`** records vendor-aligned onboarding practice (rules/docs as primary agent context), confirms the manual **`/map-codebase`** contract, and lists **hook-option families** (phase-gated generation, preflight diagnostics, CI guard, orchestrator profile extension) plus idempotency/ownership/parity risks for **`/architecture`** to lock — **no DEC-xxxx** and **no architecture section** written in research.
- Canonical backlog **Status** stays **OPEN** (**US-0045**); acceptance portfolio row for **US-0082** stays unchecked.

### Evidence refs

- `docs/engineering/research.md` (**`R-0060`**)
- `docs/product/backlog.md` (**`## US-0082`** — research closure bullet)
- `handoffs/intake_evidence/US-0082-intake-20260331.json`
- `docs/engineering/state.md` (**Research checkpoint (2026-03-31) — US-0082 / auto-20260331-02**)
- `handoffs/resume_brief.md`

---

## Orchestrated architecture handoff — US-0082 / auto-20260331-02

### Target

- `story_id=US-0082`
- `orchestrator_run_id=auto-20260331-02`
- phase completed: **`architecture`** (**`tech-lead`**)
- `next_scheduled_phase=sprint-plan`

### Summary

- **`DEC-0065`** locks phase-gated codebase map bootstrap: **`/architecture`** primary lifecycle guarantee (**tech-lead**), optional policy-gated **`/refresh-context`**, **`/map-codebase`** manual; idempotency, ownership, **`CODEBASE_MAP_*`** diagnostics, parity/regression expectations; **`docs/engineering/architecture.md`** **`# US-0082`**.
- Canonical backlog **Status** stays **OPEN** (**US-0045**); acceptance portfolio row for **US-0082** stays unchecked.
- Next: **`/sprint-plan`** — materialize sprint tasks against **AC-1..AC-10** under **`DEC-0065`** / **`R-0060`**.

### Evidence refs

- `decisions/DEC-0065.md`
- `docs/engineering/architecture.md` (**`# US-0082`**)
- `docs/engineering/decisions.md` (index + context pack)
- `docs/engineering/research.md` (**`R-0060`** architecture closure line)
- `docs/product/backlog.md` (**`## US-0082`** — architecture closure bullet)
- `handoffs/intake_evidence/US-0082-intake-20260331.json`
- `docs/engineering/state.md` (**Architecture checkpoint (2026-03-31) — US-0082 / auto-20260331-02**)
- `handoffs/resume_brief.md`
- `handoffs/tl_to_dev.md` (**US-0082** pre-sprint architecture section)

---

## Orchestrated intake handoff — BUG-0003 / auto-20260331-03

### Target

- `bug_id=BUG-0003`
- `orchestrator_run_id=auto-20260331-03`
- phase completed: **`intake`** (**`po`**)
- `next_scheduled_phase=discovery`

### Summary

- Canonical intake evidence remains authoritative: **`handoffs/intake_evidence/BUG-0003-intake-20260331-b.json`** (`selected_pack=small-intake-pack`, `missing_topics=[]`), revalidated for this boundary with **`[INTAKE_EVIDENCE_VALIDATION_OK]`**.
- Intake scope is bug-led and mode-specific: `missing`/`upgrade` installs still miss required scripts, with explicit reported gap `scripts/enforce-triad-hot-surface.py`; parity across `installer.ps1`, `installer.sh`, and `installer.py` remains mandatory.
- Canonical status authority unchanged (**US-0045**): **`docs/product/backlog.md`** keeps **`BUG-0003`** **OPEN**; acceptance bug row remains unchecked until downstream phases.
- Next: **`/discovery`** to isolate per-mode copy/skip logic and lock required script inventory contract before research/architecture.

### Evidence refs

- `docs/product/backlog.md` (**`## Bug issues (canonical)`** / **`### BUG-0003`**)
- `docs/product/acceptance.md` (**`## Bug acceptance (canonical)`**)
- `handoffs/intake_evidence/BUG-0003-intake-20260331-b.json`
- `docs/engineering/state.md` (**Intake checkpoint (2026-03-31) — BUG-0003 / auto-20260331-03**)
- `handoffs/resume_brief.md`

---

## Orchestrated discovery handoff — BUG-0003 / auto-20260331-03

### Target

- `bug_id=BUG-0003`
- `orchestrator_run_id=auto-20260331-03`
- phase completed: **`discovery`** (**`po`**)
- `next_scheduled_phase=research`

### Summary

- Discovery confirms a bounded follow-up defect, not a new feature request: the unresolved risk surface is mode-specific installer completeness in `missing` and `upgrade`, with reported miss `scripts/enforce-triad-hot-surface.py`.
- Overlap with **`BUG-0001`** is lineage-only (`duplicate_of`) rather than closure-equivalence: baseline intake payload parity was fixed, but this gap is about mode-path copy/skip behavior and completeness validation after run.
- Research is now ready and scoped: (1) map per-mode branching and skip predicates in `installer.ps1` / `installer.sh` / `installer.py`, (2) define deterministic required-script inventory contract for post-install completeness, and (3) define parity/regression checks proving `missing`/`upgrade` cannot silently omit framework-critical scripts.
- Canonical status authority unchanged (**US-0045**): **`docs/product/backlog.md`** keeps **`BUG-0003`** **OPEN**; acceptance bug row remains unchecked.

### Evidence refs

- `docs/product/backlog.md` (**`## Bug issues (canonical)`** / **`### BUG-0003`** — discovery addendum)
- `handoffs/intake_evidence/BUG-0003-intake-20260331-b.json`
- `docs/engineering/state.md` (**Discovery checkpoint (2026-03-31) — BUG-0003 / auto-20260331-03**)
- `handoffs/resume_brief.md`

---

## Orchestrated research handoff — BUG-0003 / auto-20260331-03

### Target

- `bug_id=BUG-0003`
- `orchestrator_run_id=auto-20260331-03`
- phase completed: **`research`** (**`tech-lead`**)
- `next_scheduled_phase=architecture`

### Summary

- **`R-0061`** documents mode-branch inventory for `missing`/`upgrade` across `installer.ps1`, `installer.sh`, and `installer.py`: branch behavior is parity-aligned, so observed misses are inventory-source issues rather than branch drift.
- Research identifies the concrete gap: manifest-driven install source of truth omits `scripts/enforce-triad-hot-surface.py`, allowing successful `missing`/`upgrade` runs with incomplete framework script payload.
- Recommended architecture direction: keep installer ownership manifest as single required-script source of truth, add deterministic post-install completeness diagnostics, and lock parity regression tests for `missing`/`upgrade` (active + template surfaces).
- Canonical status authority unchanged (**US-0045**): **`docs/product/backlog.md`** keeps **`BUG-0003`** **OPEN**; acceptance bug row remains unchecked.

### Evidence refs

- `docs/engineering/research.md` (**`R-0061`**)
- `docs/product/backlog.md` (**`## Bug issues (canonical)`** / **`### BUG-0003`**)
- `installer.ps1`
- `installer.sh`
- `installer.py`
- `docs/engineering/context/installer-owned-paths.manifest`
- `docs/engineering/state.md` (**Research checkpoint (2026-03-31) — BUG-0003 / auto-20260331-03**)
- `handoffs/resume_brief.md`

---

## Orchestrated intake handoff — US-0083 / auto-20260331-04

### Target

- `story_id=US-0083`
- `orchestrator_run_id=auto-20260331-04`
- phase completed: **`intake`** (**`po`**)
- `next_scheduled_phase=discovery`

### Summary

- Intake evidence refreshed for this orchestrated boundary with deterministic `small-intake-pack` coverage in `handoffs/intake_evidence/US-0083-intake-20260331-b.json` (`missing_topics=[]`, `assumptions_confirmed=(none)`), validated by `scripts/intake_evidence_validate.py`.
- Canonical status authority unchanged (**US-0045**): `docs/product/backlog.md` keeps `US-0083` as **OPEN**.
- Discovery should focus on explicit delegation semantics: when delegation is valid evidence vs when required topics remain fail-closed, plus guided/low-touch parity and deterministic diagnostics.

### Evidence refs

- `docs/product/backlog.md` (**`## US-0083`**)
- `handoffs/intake_evidence/US-0083-intake-20260331-b.json`
- `handoffs/intake_evidence/US-0083-intake-20260331.json`
- `docs/product/vision.md` (**Intake Notes — US-0083**)
- `docs/product/acceptance.md` (**US-0083 row remains unchecked**)
- `handoffs/resume_brief.md`

---

## Orchestrated discovery handoff — US-0083 / auto-20260331-04

### Target

- `story_id=US-0083`
- `orchestrator_run_id=auto-20260331-04`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0083-discovery-20260331T224601Z-fresh`
- `next_scheduled_phase=research`

### Summary

- Discovery narrowed the delegation contract: delegation must be explicit and topic-scoped for unresolved required intake topics; non-delegated unresolved required topics continue to fail closed.
- Research should lock deterministic evidence and validator semantics: delegated-topic representation (DEC-0060-compatible refs), required rationale/confidence metadata, and fail-closed diagnostics when delegation evidence is absent or malformed.
- Guided vs low-touch parity must be explicit in research outputs so delegation behavior is consistent across both modes without silent bypasses.
- Canonical status authority unchanged (**US-0045**): `docs/product/backlog.md` keeps `US-0083` as **OPEN**.

### Evidence refs

- `docs/product/backlog.md` (**`## US-0083`** — discovery closure bullets)
- `docs/product/vision.md` (**`## Discovery Notes — US-0083`**)
- `docs/product/acceptance.md` (**US-0083 row remains unchecked**)
- `handoffs/intake_evidence/US-0083-intake-20260331-b.json`
- `handoffs/resume_brief.md`

---

## Orchestrated research handoff — US-0083 / auto-20260331-04

### Target

- `story_id=US-0083`
- `orchestrator_run_id=auto-20260331-04`
- phase completed: **`research`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0083-research-20260401T004910Z-fresh`
- `next_scheduled_phase=architecture`

### Summary

- Research completed as **`R-0062`** with explicit option analysis for delegable intake evidence while preserving fail-closed safety for non-delegated required-topic gaps.
- Recommended architecture direction is the simplest bounded extension of current `topic_coverage` semantics: allow `satisfied_by=delegation_ref` (topic-scoped only) plus required `delegation_scope`, `delegation_rationale`, and `delegation_confidence`, all tied to DEC-0060-compatible `ie:` evidence binding.
- Validator branch contract for architecture lock: (1) non-delegated unresolved required topic remains existing `INTAKE_REQUIRED_TOPIC_MISSING` fail-closed behavior, (2) delegated topic with complete evidence passes, (3) delegated topic with missing/malformed evidence fails closed under delegation-specific deterministic diagnostics.
- Guided/low-touch parity remains required (no mode-specific bypass semantics).
- Canonical status authority unchanged (**US-0045**): `docs/product/backlog.md` keeps `US-0083` as **OPEN**.

### Evidence refs

- `docs/engineering/research.md` (**`R-0062`**)
- `docs/product/backlog.md` (**`## US-0083`** — research closure bullet)
- `docs/product/vision.md` (**Intake Notes / Discovery Notes — US-0083**)
- `scripts/intake_evidence_lib.py`
- `scripts/intake_evidence_validate.py`
- `handoffs/resume_brief.md`
