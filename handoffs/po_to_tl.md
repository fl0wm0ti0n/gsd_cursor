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

---

## Orchestrated discovery handoff — BUG-0005 / auto-20260403-02

### Target

- `bug_id=BUG-0005`
- `orchestrator_run_id=auto-20260403-02`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-BUG0005-discovery-20260403T193500Z-fresh`
- `next_scheduled_phase=research`

### Summary

- **Scope**: Post-**bug intake** `/auto` continuation — `handoffs/resume_brief.md` can still describe a pre-intake **`intake`** target, triggering **`AUTO_RESUME_ERROR` / `RESUME_BRIEF_STALE`** when `/auto` runs without explicit `start-from`. Discovery confirms this is **orchestration resume continuity**, not installer/runtime issues (**`BUG-0004`**) or installer payload completeness (**`BUG-0003`**).
- **Impacted surfaces**: `/auto` **resume-source precedence** (resume brief vs explicit start-from vs `docs/engineering/state.md` fallback); **`resume_brief` freshness** semantics and safe rewrite policy at intake boundaries; **intake→auto** breadcrumbs so the next scheduled phase matches the new bug context.
- **Canonical status** (**US-0045**): **`docs/product/backlog.md`** keeps **`BUG-0005`** **OPEN**; acceptance bug row stays unchecked.

### Evidence refs

- `docs/product/backlog.md` (**`### BUG-0005`** — `discovery_notes`)
- `handoffs/intake_evidence/BUG-0005-intake-20260403.json`
- `handoffs/resume_brief.md`
- `docs/engineering/state.md` (**Discovery checkpoint (2026-04-03) — BUG-0005 / auto-20260403-02**)

### Open questions for `/research`

1. Under what conditions should **`resume_brief`** be **auto-refreshed** or **superseded** after canonical bug intake vs requiring explicit operator rewrite?
2. What is the minimal **deterministic self-heal** (if any) that preserves resume precedence and fail-fast contracts (**US-0037**, **US-0070**) without masking real staleness?
3. **Regression matrix**: scripted or documented sequence **`/intake bug` → `/auto`** asserting valid phase resolution or expected deterministic error with **non-stale** semantics.
4. Interaction with **`state.md`** fallback when **`resume_brief`** is present but **invalid/stale** — align with existing **`AUTO_RESUME_ERROR`** vocabulary.

### Next

- **`/research`** (tech-lead) for **`BUG-0005`**; then architecture/sprint path per TL.
- **Decision gate before research**: none (discovery satisfied; bug **OPEN**).

---

## Orchestrated discovery handoff — BUG-0006 / auto-20260403-03

### Target

- `bug_id=BUG-0006`
- `orchestrator_run_id=auto-20260403-03`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-BUG0006-discovery-20260404T002000Z-fresh`
- `next_scheduled_phase=research`

### Summary

- **Scope**: **`/auto`** orchestration integrity — orchestrator **must not** perform phase work directly; each phase requires **fresh subagent** spawn per **US-0048** / **US-0069** / **US-0080**; on violation, **fail fast** with deterministic reason-code coverage (intake: **`handoffs/intake_evidence/BUG-0006-intake-20260403.json`**).
- **Discovery conclusions**: Defect is bounded to **workflow/docs/enforcement** surfaces (command + reference + optional tests); preserve existing isolation and strict-runtime-proof contracts (**DEC-0029**, **DEC-0038**); add regression that proves spawn-or-fail behavior is not bypassed by “orchestrator executes phase” paths.
- **Canonical status** (**US-0045**): **`docs/product/backlog.md`** keeps **`BUG-0006`** **OPEN**; acceptance bug row unchanged.

### Evidence refs

- `docs/product/backlog.md` (**`### BUG-0006`** — `discovery_notes`)
- `handoffs/intake_evidence/BUG-0006-intake-20260403.json`
- `.cursor/commands/auto.md`
- `docs/engineering/state.md` (**Discovery checkpoint — BUG-0006 / auto-20260403-03**; triad archive **`docs/engineering/state-archive/state-pack-20260403-n.md`**)
- `handoffs/resume_brief.md`

### Open questions for `/research`

1. Concrete locations (commands, **`auto-orchestration-reference.md`**, runbook, tests) where “direct execution” could be read as allowed vs forbidden.
2. Minimal **R-####** recommendation: doc-only hardening vs scripted guardrails vs both; align reason codes with **`PHASE_CONTEXT_ISOLATION_*`** / spawn enforcement vocabulary.
3. **Regression matrix**: positive (spawn implied) and negative (orchestrator must not claim phase completion without subagent boundary) — test or contract-check shape.

### Next

- **`/research`** (**tech-lead**, default) for **`BUG-0006`**; then **`/architecture`** / **`/sprint-plan`** per TL.
- **Decision gate before research**: none (discovery satisfied; bug **OPEN**).

---

## Orchestrated discovery handoff — BUG-0007 / auto-20260404-01

### Target

- `bug_id=BUG-0007`
- `orchestrator_run_id=auto-20260404-01`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-BUG0007-discovery-20260404T120000Z-fresh`
- `next_scheduled_phase=research`

### Summary

- **Scope**: Intake evidence integrity — **`asked_topics`** and **`topic_coverage`** must truthfully record which required-pack topics were **actually asked** in user-visible form (or satisfied via explicit **DEC-0060** mechanisms: **`delegation_ref`** with scope/rationale/confidence, **`equivalent_evidence_ref`**, or **`assumption_confirmation_ref`**). The defect is **misleading evidence**: persistence/validation may treat free-form user bug text as if it were structured answers to required questions.
- **Exemplar**: **`handoffs/intake_evidence/BUG-0007-intake-20260403.json`** — `small-intake-pack` with `asked_topics` populated and five `topic_coverage` rows using the same complaint prose as `quoted_user_text` under `satisfied_by=answer_ref` without a distinct Q/A turn; contrasts with **`.cursor/commands/intake.md`** (US-0068 / US-0078) expectation that evidence matches real questioning.
- **Canonical status** (**US-0045**): **`docs/product/backlog.md`** keeps **`BUG-0007`** **OPEN** until **`/verify-work`** closure; acceptance bug row unchanged.

### Evidence refs

- `docs/product/backlog.md` (**`### BUG-0007`** — `discovery_notes`)
- `handoffs/intake_evidence/BUG-0007-intake-20260403.json`
- `.cursor/commands/intake.md` (**interactive intake evidence gate**)
- `scripts/intake_evidence_validate.py` (validator surface for fail-closed persistence)
- `docs/engineering/state.md` (**Discovery checkpoint — BUG-0007 / auto-20260404-01**)
- `handoffs/resume_brief.md`

### Open questions for `/research`

1. Where evidence is authored relative to **actual chat turns** (PO subagent, scripts, templates) and what minimal **audit binding** (e.g. turn refs, question text hash, explicit “not asked” state) is feasible.
2. Validator and/or command changes so **`asked_topics`** cannot list topics that were never prompted, and **`topic_coverage`** cannot use **`answer_ref`** without a verifiable user answer artifact — without breaking legitimate **`delegation_ref`** / **`equivalent_evidence_ref`** flows (**US-0083**).
3. Interaction with **`/intake bug`** path: **`intake_bug_resume_brief_refresh.py`**, **`bug_issue_validate.py`**, and whether a new deterministic subcode under **`INTAKE_PERSISTENCE_BLOCKED`** is warranted.
4. **Regression matrix**: fixture JSON + validator test that fails on BUG-0007-shaped bundles.

### Next

- **`/research`** (**tech-lead**, default) for **`BUG-0007`**; then **`/architecture`** / **`/sprint-plan`** per TL.
- **Decision gate before research**: none (discovery satisfied; bug **OPEN**).

---

## PO → TL discovery handoff — **US-0087** (`auto-20260405-01`)

- **Scope recap**: Add **explicit** **`/auto`** bug targeting — **fix all OPEN bugs** (canonical backlog section, ascending id) or **single `BUG-####`** — with **spawn-only** orchestration unchanged; **default-off** new scratchpad keys; **one active scheduler** vs **`AUTO_BACKLOG_DRAIN`** (**US-0044**/**DEC-0022**); per-segment **`bug_id`** breadcrumbs in **`resume_brief`**/**`state.md`** aligned with **DEC-0069** (no stale **`RESUME_BRIEF_STALE`** on lawful runs). Intake evidence: `handoffs/intake_evidence/US-0087-intake-20260404.json`.
- **Acceptance pointers**: **AC-1** argv spellings; **AC-2** scratchpad/**`template/`**; **AC-3** precedence + conflict doc; **AC-4** queue + max items + empty queue code; **AC-5** resume/state fields; **AC-6** spawn-only; **AC-7** contract tests; **AC-8** **`architecture.md` `# US-0087`** matrix; **AC-9** runbook; **AC-10** parity.
- **Top risks**: double scheduling (story drain + bug queue); **`resume_brief`** freshness regressions; under-specified operator syntax; reason-code drift vs **`# US-0087`**.
- **Research asks** (extend **`R-0070`**):
  1. Enumerate **`auto.md`** + **`auto-orchestration-reference.md`** paragraphs that must change for bug-target precedence and **`AUTO_BACKLOG_DRAIN`** interaction.
  2. Map **`DEC-0069`**/**`BUG-0005`** requirements onto multi-bug queue + segment boundaries.
  3. Propose **architecture-locked** flag names + **fail-closed** reason codes (**AC-3**/**AC-4**/**AC-8**).
  4. Define **`AC-10`** breadcrumb tuple extensions for **`orchestrator_run_id`** segments when **`story_id=US-0087`** (before **`bug_id`** is set mid-queue).
- **Next phase**: **`/research`** (tech-lead default, **`US-0070`** plan).

---

## Research Addendum — US-0087 (tail mirror)

- **Orchestrator**: **`auto-20260405-01`** — **`/research`** complete in fresh **tech-lead** context (**`2026-04-06T15:00:00Z`**).
- **Evidence**: **`docs/engineering/research.md`** **`R-0070`** (extended inventory, **`DEC-0069`** queue notes, candidate **`AUTO_BUG_*`** + reason codes, **`AC-10`** tuple extensions); **`docs/product/backlog.md`** (**`research_notes`** under **`## US-0087`**); **`docs/engineering/state.md`** (Research checkpoint + **DEC-0038** **`proof_hash=cee06560f1e1278278d76d01df64466bd9f8ae942e344c65bf50cdc51251c111`**); **`handoffs/resume_brief.md`** → **`/architecture`**.
- **Findings**: Line-level targets in **`auto.md`** / **`auto-orchestration-reference.md`** / **`template/`**; **one scheduler** vs **`AUTO_BACKLOG_DRAIN`**: architecture must lock precedence or hard fail (**`AUTO_SCHEDULER_CONFLICT`** candidate); multi-bug segments need **`resume_brief`** + **`state.md`** alignment to avoid **`RESUME_BRIEF_STALE`**; contract tests extend **`tests/auto_command_contract_test.py`** per **AC-7**.
- **Next**: **`/architecture`** — **`docs/engineering/architecture.md`** **`# US-0087`** (reason-code matrix, locked flag names, interaction table).
- **Decision gate before architecture**: none (research satisfied; story **OPEN** **US-0045**).

---

## Discovery Addendum — US-0088 (tail)

- **Orchestrator**: **`auto-20260405-01`** — discovery complete in fresh **PO** context (**`2026-04-12T22:00:00Z`**).
- **`fresh_context_marker=po-US0088-discovery-20260412T220000Z-fresh`**
- **Evidence**: **`docs/product/backlog.md`** (**`## US-0088`** — discovery_notes **PASS**); **`docs/engineering/state.md`** (Discovery checkpoint + isolation + **DEC-0038** strict proof); **`docs/engineering/research.md`** **`R-0071`** (discovery survey extension); **`handoffs/resume_brief.md`** → **`/research`**.
- **Scope recap**: **Continuous `/auto`** through intersected phases per **Step 5** until **US** or **sprint-segment** boundary; **`AUTO_BACKLOG_DRAIN=1`** with **`backlog_drain_stories_remaining_budget=9`**; **quiet** operator notifications only on **`decision_gate`**, **`error`**, **`pause`**, **`loop_max`**, **`blocked`**, **missing inputs**; regression for **one-phase-stop** + **drain advance**; **spawn-only** unchanged (**BUG-0006** / **US-0069**).
- **Scratchpad context (merged)**: **`INTAKE_GUIDED_MODE=1`**, **`EARLY_RESEARCH=1`**, **`TOKEN_PROFILE=balanced`** — research must reconcile **`AC-2`** with optional **`AUTO_QUIET`** vs profile composition.
- **Research asks** (extend **`R-0071`**):
  1. Line-level **Step 5** vs **`auto.md`** / reference / runbook drift that enables **single-spawn** misread.
  2. **Contract-test** shape: assert continuation when policy requires it; fixture boundaries for orchestrator vs subagent roles.
  3. **`resume_brief` / `state.md`** tuple for **phase depth** + **story cursor** under **US-0037** / **DEC-0069** during long **`/auto`** runs.
  4. **US-0087** mutex: cite **R-0070** / **`# US-0087`** only — no new bug-queue semantics in **US-0088**.
- **Risks**: Over-quiet automation hiding gates; **RESUME_BRIEF_STALE** false positives; template/command parity drift (**AC-5** / **AC-10**).
- **Status authority**: **`US-0088`** remains **OPEN** in **`docs/product/backlog.md`** (**US-0045**).
- **Next** *(historical at discovery writer)*: **`/research`** — **PASS** **`2026-04-12T23:15:00Z`**; see **Research Addendum — US-0088** below → **`/architecture`**.
- **Decision gate before research**: none (discovery satisfied).

---

## Research Addendum — US-0088 (tail mirror)

- **Orchestrator**: **`auto-20260405-01`** — **`/research`** complete in fresh **tech-lead** context (**`2026-04-12T23:15:00Z`**).
- **Evidence**: **`docs/engineering/research.md`** **`R-0071`** (Step 5 vs compact-step drift, contract-test anchors, **`AUTO_QUIET`** vs **`TOKEN_PROFILE`**, **`resume_brief`/`state.md`** pairing); **`docs/product/backlog.md`** (**`research_notes`** under **`## US-0088`**); **`docs/engineering/state.md`** (Research checkpoint + **DEC-0038** **`proof_hash=dce665eedb088088e3205e3c81575c45af5cdda1108af0aa3b4f6370461c52c0`**); **`handoffs/resume_brief.md`** → **`/architecture`**.
- **Findings**: Normative **multi-phase** loop lives in **`auto-orchestration-reference.md`** **`## Steps`** item **5**; **`.cursor/commands/auto.md`** compact numbering diverges — architecture should lock cross-anchors or outer-driver equivalence (**AC-1**).
- **Next**: **`/architecture`** — **`docs/engineering/architecture.md`** **`# US-0088`** (quiet, drain, resume, tests) + optional **DEC** if required.
- **Decision gate before architecture**: none (research satisfied; story **OPEN** **US-0045**).

---

## Sprint Plan Addendum — US-0088 (tail mirror)

- **Orchestrator**: **`auto-20260405-01`** — **`/sprint-plan`** complete in fresh **tech-lead** context (**`2026-04-12T23:55:00Z`**).
- **`fresh_context_marker=tl-US0088-sprint-plan-20260412T235500Z-fresh`**
- **Evidence**: **`docs/product/backlog.md`** (**`sprint_plan_notes`** under **`## US-0088`**); **`sprints/S0072/sprint.md`**, **`sprints/S0072/tasks.md`**, **`sprints/S0072/plan-verify.json`** (**PENDING** / **`AWAITING_QA_PLAN_VERIFY`**); **`docs/engineering/state.md`** (Sprint-plan checkpoint + **DEC-0038** **`proof_hash=e160a10f33af56b56437d3be302aeceedc47ab995563169402a068b82b3318ae`**); **`handoffs/resume_brief.md`**, **`handoffs/tl_to_dev.md`**, **`handoffs/qa_plan_verify.md`** → **`/plan-verify`** (**qa**).
- **Coverage intent**: **AC-1..AC-7** ↔ **T-001..T-007** for continuous **`/auto`**, **`AUTO_QUIET`**, **`US-0044`** drain + tests, **`template/`** parity, **`# US-0088`** consistency, runbook recipe.
- **Status authority**: **`US-0088`** remains **OPEN** in **`docs/product/backlog.md`** (**US-0045**).
- **Next**: **`/plan-verify`** (**qa**) for **`S0072`** — then **`/execute`** (**dev**) when **`plan-verify.json`** → **PASS**.

---

## Discovery Addendum — US-0085 (tail)

- **Orchestrator**: **`auto-20260405-01`** — discovery complete in fresh **PO** context (**`2026-04-13T12:05:00Z`**).
- **`fresh_context_marker=po-US0085-discovery-20260413T120500Z-fresh`**
- **Evidence**: **`docs/product/backlog.md`** (**`## US-0085`** — discovery_notes **PASS**); **`docs/product/vision.md`** (**Discovery Notes — US-0085**); **`docs/engineering/state.md`** (Discovery checkpoint + isolation + **DEC-0038** strict proof); **`docs/engineering/research.md`** **`R-0072`** (discovery survey stub); **`handoffs/resume_brief.md`** → **`/research`**.
- **Scope recap**: Standardize **repo-root `.env`** (gitignored) for `*Env` values used by **`.cursor/remote.json`** and **`release-targets.json`** operator connectivity flows (**US-0064**); committed **`.env.example`** with names only; **`.cursorignore`** + agent/rule exclusion so AI never reads `.env`; runbook + `runtime-connectivity.md` + `us-0084-remote-e2e.md` doc updates; optional AC-8 helper; template parity; regression tests.
- **Intake evidence**: `handoffs/intake_evidence/US-0085-intake-20260404.json` (**`small-intake-pack`**, **`[INTAKE_EVIDENCE_VALIDATION_OK]`**).
- **Market context**: `.env` + `.gitignore` is baseline; AI dev tools require **`.cursorignore`** and/or explicit agent rules because agents have developer-level filesystem access. Defense-in-depth (config exclusion + behavioral rules) is industry practice.
- **Repo survey findings**: `.gitignore` exists (no `.env` entry); no `.cursorignore`; no `.env.example`; `runtime-connectivity.md` and `us-0084-remote-e2e.md` in active + `template/`.
- **Research asks** (extend **`R-0072`** in **`/research`**):
  1. Full `*Env` variable name inventory from `.cursor/remote.json` template and `release-targets.json` schema for `.env.example` content.
  2. `.cursorignore` file format and path-matching semantics; whether Cursor rules augment or replace it for agent file-context exclusion.
  3. AC-8 decision inputs: deterministic `scripts/print_remote_env_hint.py` (names-only) vs documented shell recipe.
  4. AC-9 regression test shape: `git check-ignore` fixture or Python test.
  5. Template parity touchpoints for new/modified files (`.gitignore`, `.cursorignore`, `.env.example`, runbook, runtime-connectivity, us-0084-remote-e2e, rules).
- **Risks**: `.cursorignore` syntax may differ across Cursor versions; `.env` pattern may conflict with framework-generated `.env` in generated projects; AC-8 helper could leak secret patterns if not strictly names-only.
- **Status authority**: **`US-0085`** remains **OPEN** in **`docs/product/backlog.md`** (**US-0045**).
- **Next**: ~~**`/research`**~~ → **`/architecture`** (tech-lead) for **US-0085**.
- **Decision gate before research**: none (discovery satisfied; story **OPEN**).

---

## Research Addendum — US-0085 (tail mirror)

- **Orchestrator**: **`auto-20260405-01`** — **`/research`** complete in fresh **tech-lead** context (**`2026-04-13T12:15:00Z`**).
- **`fresh_context_marker=tl-US0085-research-20260413T121500Z-fresh`**
- **Evidence**: **`docs/engineering/research.md`** **`R-0072`** (extended — `*Env` inventory, `.cursorignore` semantics, AC-8/AC-9 recommendations, template parity, risks); **`docs/product/backlog.md`** (**`research_notes`** under **`## US-0085`**); **`docs/engineering/state.md`** (Research checkpoint + **DEC-0038** **`proof_hash=b04b45a6f9110e8da20cfee684320bc05c2cb775387f651a2ab315aa982f221b`**); **`handoffs/resume_brief.md`** → **`/architecture`**.
- **Key findings**:
  1. **`*Env` inventory**: 20 unique env var names (3 from `remote.json` template, 17 from `release-targets.json`) for `.env.example`.
  2. **`.cursorignore` confirmed**: `.gitignore` syntax, blocks agent file tools, does **not** block terminal/MCP. Defense-in-depth requires 4 layers.
  3. **AC-8**: recommend `scripts/print_remote_env_hint.py` (names-only, cross-platform, parity check with JSON schemas).
  4. **AC-9**: `git check-ignore` Python test fixture.
  5. **Template parity**: 7 touchpoints; no `template/.gitignore` exists (architecture decides create vs omit).
  6. **AC-10**: `remote_config_summary.py` unaffected — reads `remote.json` names, not `.env` values.
  7. **Risks**: terminal bypass (medium), open-tab leak (low), framework collision (low).
- **Next**: **`/architecture`** — **`docs/engineering/architecture.md`** **`# US-0085`** (defense-in-depth layers, `.env.example` content contract, template parity decisions, AC-8 helper shape).
- **Decision gate before architecture**: none (research satisfied; story **OPEN** **US-0045**).

---

## Discovery Addendum — US-0086 (tail)

- **Orchestrator**: **`auto-20260405-01`** — discovery complete in fresh **PO** context (**`2026-04-13T18:30:00Z`**).
- **`fresh_context_marker=po-US0086-discovery-20260413T183000Z-fresh`**
- **Evidence**: **`docs/product/backlog.md`** (**`## US-0086`** — discovery_notes **PASS**); **`docs/product/vision.md`** (**Discovery Notes — US-0086**); **`docs/engineering/research.md`** (**`R-0068`** discovery extension); **`docs/engineering/state.md`** (Discovery checkpoint + isolation + **DEC-0038** strict proof); **`handoffs/resume_brief.md`** → **`/research`**.
- **Scope recap**: keep **manual** workflow default local/no-reroute; add **automation-only** deterministic target choice path for dev/CI/DI/QA/release when enabled.
- **Locked discovery contracts**:
  1. Explicit intent phrase **"start container `<target_id>`"** resolves to canonical **`targets[].id`**.
  2. Unknown/disabled target must fail closed with deterministic reason-code diagnostics.
  3. Composition with **US-0085** remains strict: no `.env` reads, names-only outputs, no secret echo in evidence.
- **Research asks** (`/research`, extend **`R-0068`**):
  1. Deterministic routing matrix from changed-file classes + explicit operator intent for Docker/SSH/local selection.
  2. Evidence tuple contract for automation remote runs (`target_id`, `environment_label`, `automation_profile`) across execute/qa/release handoffs.
  3. Candidate reason-code vocabulary and scratchpad key naming options for architecture lock.
  4. Minimum regression-test surface for target-id resolution and mode-off/no-reroute behavior.
- **Status authority**: **`US-0086`** remains **OPEN** in **`docs/product/backlog.md`** (**US-0045**).
- **Next**: **`/research`** (**tech-lead**) for **`US-0086`**.
- **Decision gate before research**: none (discovery satisfied; story **OPEN**).

---

## Research Addendum — US-0086 (tail mirror)

- **Orchestrator**: **`auto-20260405-01`** — **`/research`** complete in fresh **tech-lead** context (**`2026-04-13T19:00:00Z`**).
- **`fresh_context_marker=tl-US0086-research-20260413T190000Z-fresh`**
- **Evidence**: **`docs/engineering/research.md`** **`R-0068`** (research extension with routing matrix, reason-code candidates, evidence tuple contract, external references); **`docs/product/backlog.md`** (**`research_notes`** under **`## US-0086`**); **`docs/engineering/state.md`** (Research checkpoint + **DEC-0038** strict proof); **`handoffs/resume_brief.md`** → **`/architecture`**.
- **Key findings**:
  1. **Routing precedence**: explicit NL intent `start container <target_id>` first, then automation-mode heuristic fallback, else local default.
  2. **External contract anchors**: GitHub path filters support deterministic CI routing; Docker context precedence supports stable target binding; OpenSSH options support fail-fast host validation.
  3. **Evidence tuple**: `target_id`, `environment_label`, `automation_profile`, `routing_source`, `secret_surface=names_only`.
  4. **Reason-code candidates** for architecture lock: `REMOTE_AUTOMATION_MODE_OFF`, `REMOTE_TARGET_UNKNOWN`, `REMOTE_TARGET_DISABLED`, `REMOTE_TARGET_UNROUTABLE`.
  5. **Security continuity** with **US-0085**: no `.env` reads; no secret values in logs/handoffs.
- **Next**: **`/architecture`** — lock scratchpad key names, reason codes, routing matrix, and parity/test surfaces for **AC-1..AC-10**.
- **Decision gate before architecture**: none (research satisfied; story **OPEN** **US-0045**).

---

## PO → TL Handoff — US-0089 / US-0090 (Intake) (tail mirror)

> Placement: **tail** hot copy for TL read model (**runbook**). Prefix rollovers: **`handoffs/archive/po-to-tl-pack-20260414.md`** (first **US-0089**/**US-0090** prepend), then **`handoffs/archive/po-to-tl-pack-20260414-a.md`** (line-cap rebalance).

### New intake

Operator wants **Caveman-style** terse communication (**JuliusBrussee/caveman**-like) in **Cursor**, **scratchpad-configurable**, **default off**, **without losing** existing **its-magic** features. **Split stories**: **US-0089** (response style + scratchpad + rules/skill + tests) then **US-0090** (optional **input-side** file compression with **original preserved** and **hard deny** for canonical/evidence paths).

### Evidence

- **`handoffs/intake_evidence/US-0089-intake-20260414.json`** — **`first-intake-pack`**, **`[INTAKE_EVIDENCE_VALIDATION_OK]`** (`intake_run_id=cursor-20260414-caveman-intake`).
- **`docs/product/backlog.md`** — **`## US-0089`**, **`## US-0090`**; **`docs/product/acceptance.md`**; **`docs/product/vision.md`**; **`docs/engineering/research.md`** **`R-0073`**.

### Decomposition (US-0051)

- **US-0089**: Caveman **output** mode + scratchpad keys + **rules/skill** + **`architecture.md`** **`# US-0089`** + tests (**default-off** invariant).
- **US-0090**: Optional compress path; **gates** on **`CAVEMAN_MODE`** + explicit compress policy; **deny** intake evidence, backlog, acceptance, **`state.md`**, **`.env`**; **`template/`** parity.

### TL scope / risks

- Lock **`TOKEN_PROFILE`** vs **`CAVEMAN_*`** composition (**US-0080** lineage).
- **US-0090** loss avoidance: **sidecar originals** + immutable deny-list; never rewrite **`handoffs/intake_evidence/*.json`** by default (**US-0078** / **DEC-0060**).

### Triad (**DEC-0054**) verification tuple

- **boundary**: `2026-04-14` (intake + line-cap rebalance)
- **moved**: (1) first prepend → **`handoffs/archive/po-to-tl-pack-20260414.md`** (`units=4,1`); (2) rebalance prefix → **`handoffs/archive/po-to-tl-pack-20260414-a.md`** (`units=1`)
- **retained**: hot **`handoffs/po_to_tl.md`** within **`PO_TO_TL_HOT_MAX_LINES`** / section caps after second rollover
- **pack_ref**: **`handoffs/archive/po-to-tl-pack-20260414.md`**, **`handoffs/archive/po-to-tl-pack-20260414-a.md`**
- **tooling**: `python scripts/enforce-triad-hot-surface.py --rollover` then `--check` → **PASS**

### Recommendation

**`/discovery`** (**US-0089** first) → **`/research`** (**`R-0073`**) → **`/architecture`** → **`/sprint-plan`** (**US-0089** before **US-0090**).

---

## Discovery Addendum — US-0089 (tail mirror)

- **Orchestrator**: **`auto-20260418-01`** — **`/discovery`** complete in fresh **PO** context (**`2026-04-18T12:05:00Z`**).
- **`fresh_context_marker=po-US0089-discovery-20260418T120500Z-fresh`**
- **Scope closure**: Response-side (voice) only; input-side file compression stays fully out of scope (explicit handoff to **US-0090**). Confirmed in-scope surfaces = scratchpad keys (**`CAVEMAN_MODE`** default **0**, **`CAVEMAN_LEVEL`** enum reserved — exact values architecture-locked), Cursor rules and/or focused skill composing with existing **`.cursor/skills/its-magic/SKILL.md`**, operator control phrasing contract, tests (default-off byte-equivalence + scratchpad doc markers), **`# US-0089`** architecture section, and **`template/`** parity for all touched `.cursor/` + `docs/engineering/` surfaces.
- **Risks flagged for research/architecture**: (1) Caveman voice vs **US-0021** anti-fluff + **US-0088 `AUTO_QUIET`** non-suppressible gate list — gate language, reason codes, `[BUG_VALIDATION_OK]`, `[INTAKE_EVIDENCE_VALIDATION_OK]`, `blocked`, `missing input`, `pause`, `loop_max` must stay verbatim; (2) **US-0071** — terseness does not license dropping visible **`US-xxxx`** / **`DEC-xxxx`** / **`R-xxxx`** / **`BUG-####`** IDs or reason codes from user-facing output; (3) **US-0080 / `TOKEN_PROFILE`** composition — orthogonal by default; docs must publish precedence matrix or explicit non-substitution statement (no silent override either direction); (4) literal-region preservation rule (fenced code, paths, AC checklists, filenames) as machine-verifiable invariant; (5) template parity drift if only active **`.cursor/`** is updated (**US-0017**).
- **Decision gate posture**: **none** — discovery satisfied; no DEC requested at this boundary. Story remains **OPEN** in **`docs/product/backlog.md`** per **US-0045**.
- **Next phase**: **`/research`** (fresh **tech-lead**) extending **`R-0073`** — lock composition contract options, default-off byte-equivalence test strategy, operator control phrasing shortlist, and TOKEN_PROFILE precedence matrix. No architecture/sprint artifacts authored in this PO discovery segment.
- **Artifact refs**:
  - **`docs/product/backlog.md`** — **`## US-0089`** `discovery_notes` (2026-04-18, PO, `auto-20260418-01`)
  - **`docs/product/vision.md`** — **Discovery Notes — US-0089**
  - **`docs/engineering/research.md`** — **`R-0073`** Discovery extension (2026-04-18)
  - **`handoffs/resume_brief.md`** — new top pointer post-`/discovery` US-0089
  - **`docs/engineering/state.md`** — Discovery checkpoint (2026-04-18) — US-0089 / `auto-20260418-01` (isolation + DEC-0038 strict proof + phase boundary block + AC-10 line + preflight for `/research`)

---

## Research Addendum — US-0089 (tail mirror)

> Placement: **tail** hot copy for TL read model. `orchestrator_run_id=auto-20260418-01`. Research-phase extension of **`R-0073`** completed in fresh **tech-lead** context (**`2026-04-18T12:15:00Z`**, `fresh_context_marker=tl-US0089-research-20260418T121500Z-fresh`).

- **Closure**: **`/research`** (**tech-lead**) **PASS** for **US-0089**. **`R-0073`** extended with eight implementation anchors, risks, and mitigations; **no DEC authored** (architecture owns decisions); **no architecture section** authored.
- **Anchors (summary)**:
  1. **TOKEN_PROFILE × CAVEMAN**: recommend **Option A (orthogonal, non-substitution)** — `TOKEN_PROFILE` owns context-breadth (**US-0080** / **DEC-0062**), `CAVEMAN_*` owns voice; publish a single non-substitution paragraph in `docs/engineering/auto-orchestration-reference.md` + `docs/engineering/runbook.md` (+ `template/` mirrors). Option B (explicit precedence matrix) is the architecture-fallback; Option C (collapse) rejected.
  2. **Rule vs rule+skill**: Option A = `.cursor/rules/caveman.mdc` only (minimal surface); Option B = rule + `.cursor/skills/its-magic-caveman/SKILL.md` (discoverability). Skill-only rejected. Non-suppressible gate list stays in the rule either way.
  3. **Default-off tests**: extend **`tests/auto_command_contract_test.py`** in place with `test_caveman_default_off_*` subtests (scratchpad key presence active + `template/`, existing `required` token list intact, non-suppressible gate vocabulary preserved). Voice quality **not** unit-tested.
  4. **Operator toggle vocabulary**: shortlist `caveman on|off`, `stop caveman` / `normal mode`, `caveman: lite|full|ultra`. Scratchpad is authoritative across subagent spawns; session toggle = overlay for next turn; current-turn gate artifacts remain literal.
  5. **Literal-region invariant**: 9-zone protected set (fenced code, paths, AC checklists, ALL_CAPS reason codes, IDs `US-xxxx`/`DEC-xxxx`/`R-xxxx`/`BUG-####`/`S0xxx`/`T-xxx`, contract markers `[BUG_VALIDATION_OK]`/`[INTAKE_EVIDENCE_VALIDATION_OK]`, strict-proof tuple fields, isolation-evidence fields, commit/git refs). Rule MUST, not SHOULD.
  6. **External pattern (JuliusBrussee/caveman, MIT)**: portable concepts only (levels, "compress prose not code"); vendor install path (`npx skills add`) and token-savings claims stay **out** of normative kit docs; single-line attribution acceptable.
  7. **Scratchpad key naming**: recommend `CAVEMAN_MODE=0|1` default **0**, `CAVEMAN_LEVEL=lite|full|ultra` default empty; reserved-for-US-0090 keys `CAVEMAN_COMPRESS_INPUT=0|1` (default **0**) and `CAVEMAN_FILE_SCOPE=` (empty) as documented **no-ops** until US-0090.
  8. **Template parity inventory**: 9-item file list for **`/sprint-plan`** to atomize (scratchpad active + template, scratchpad example active + template, new rule active + template, optional new skill active + template, reference + runbook + template mirrors, architecture + tests active-only).
- **Architecture asks (DEC-xxxx hints)**:
  - `DEC-xxxx` — TOKEN_PROFILE × CAVEMAN precedence (**Option A** recommended; Option B fallback).
  - `DEC-xxxx` — rule-only (Option A) vs rule + focused skill (Option B).
  - `DEC-xxxx` — scratchpad key spellings locked **before** contract tests reference them.
  - `DEC-xxxx` — 9-zone literal-region invariant published in `# US-0089`.
  - `DEC-xxxx` — canonical operator phrase set + runbook publication location.
- **Status authority**: **US-0089** stays **OPEN** in **`docs/product/backlog.md`** per **US-0045**.
- **Next phase**: **`/architecture`** (fresh **tech-lead**) for **US-0089** — lock DEC(s) + write `docs/engineering/architecture.md` `# US-0089`.
- **Decision-gate posture**: **none** expected at pre-architecture boundary (architecture asks are routine, not gate-blocking).
- **Artifact refs**:
  - **`docs/engineering/research.md`** — **`R-0073`** Research extension (2026-04-18, TL, `auto-20260418-01`)
  - **`docs/product/backlog.md`** — **`## US-0089`** `research_notes` (2026-04-18, TL, `auto-20260418-01`)
  - **`handoffs/resume_brief.md`** — new top pointer post-`/research` US-0089
  - **`docs/engineering/state.md`** — Research checkpoint (2026-04-18) — US-0089 / `auto-20260418-01` (isolation + DEC-0038 strict proof + phase boundary block + AC-10 line + preflight for `/architecture`)

---

## Architecture Addendum — US-0089 (tail mirror)

> Placement: **tail** hot copy for TL read model. `orchestrator_run_id=auto-20260418-01`. Architecture-phase lock completed in fresh **tech-lead** context (**`2026-04-18T12:30:00Z`**, `fresh_context_marker=tl-US0089-architecture-20260418T123000Z-fresh`).

- **Closure**: **`/architecture`** (**tech-lead**) **PASS** for **US-0089**. **`DEC-0072`** authored and accepted; **`docs/engineering/architecture.md`** **`# US-0089`** written; **`docs/engineering/decisions.md`** (index + canonical record) updated.
- **DEC ref**: **`DEC-0072`** — *Caveman mode scratchpad contract, composition surface, and default-off invariant*. Status **Accepted** 2026-04-18.
- **Locked decisions (summary)**:
  1. **TOKEN_PROFILE × CAVEMAN precedence** = **Option A (orthogonal, non-substitution)**. Verbatim non-substitution paragraph in `docs/engineering/auto-orchestration-reference.md` + `docs/engineering/runbook.md` (active + `template/`).
  2. **Composition surface** = **Option A (rule-only)**. New `.cursor/rules/caveman.mdc` active + `template/.cursor/rules/caveman.mdc`. **No new skill** in US-0089; `.cursor/skills/its-magic/SKILL.md` unchanged.
  3. **Scratchpad keys**: `CAVEMAN_MODE=0|1` default **`0`**; `CAVEMAN_LEVEL=lite|full|ultra` default empty (fallback `full` when MODE=1; unknown value -> `CAVEMAN_LEVEL_UNKNOWN`). Reserved-for-US-0090 no-ops `CAVEMAN_COMPRESS_INPUT=0|1` default **`0`** and `CAVEMAN_FILE_SCOPE=` empty (documented no-ops with explicit "inert in US-0089" comments).
  4. **9-zone literal-region invariant** (hard **MUST**): fenced code, file paths, AC checklists, reason codes (`ALL_CAPS_WITH_UNDERSCORES`), IDs (`US-xxxx`/`DEC-xxxx`/`R-xxxx`/`BUG-####`/`S0xxx`/`T-xxx`), contract markers (`[BUG_VALIDATION_OK]`/`[INTAKE_EVIDENCE_VALIDATION_OK]`/siblings), strict-proof tuple fields (DEC-0038), isolation evidence fields (DEC-0029), git/commit refs.
  5. **Canonical operator phrases**: `caveman on`, `caveman off`, `stop caveman`, `normal mode`, `caveman: lite|full|ultra`. Scratchpad authoritative across subagent spawns; session toggles are next-turn overlays only; current-turn gate artifacts remain literal.
  6. **Default-off tests**: extend `tests/auto_command_contract_test.py` **in place** with **8** `test_caveman_default_off_*` subtests (exact byte strings locked in DEC-0072 §3 / §6).
  7. **Template parity inventory** — 8 rows locked in architecture `# US-0089` §7 + DEC-0072 §7; includes negative-parity row for `.cursor/skills/its-magic/SKILL.md` (no change).
  8. **Non-goals (hard)**: no input-side compression (US-0090 only), no `TOKEN_PROFILE` change, no canonical artifact rewrites, no new npm/python deps, no `npx skills add` leak, no voice-quality unit test.
- **Next phase**: **`/sprint-plan`** (fresh **tech-lead**) for **US-0089** — atomize DEC-0072 §7 parity inventory into tasks against **AC-1..AC-8** (within `SPRINT_MAX_TASKS=12`).
- **Decision-gate posture**: **none** expected before **`/sprint-plan`**.
- **Status authority**: **US-0089** stays **OPEN** in **`docs/product/backlog.md`** per **US-0045**.
- **Artifact refs**:
  - **`decisions/DEC-0072.md`**
  - **`docs/engineering/architecture.md`** **`# US-0089`**
  - **`docs/engineering/decisions.md`** (index + context pack; canonical full-record entry)
  - **`docs/product/backlog.md`** — **`## US-0089`** `architecture_notes` (2026-04-18, TL, `auto-20260418-01`)
  - **`handoffs/tl_to_dev.md`** — **US-0089** pre-sprint architecture handoff (top of file)
  - **`handoffs/resume_brief.md`** — new top pointer post-`/architecture` US-0089 (prior post-`/research` US-0089 marked superseded)
  - **`docs/engineering/state.md`** — Architecture checkpoint (2026-04-18) — US-0089 / `auto-20260418-01` (isolation + DEC-0038 strict proof + phase boundary block + AC-10 line + preflight for `/sprint-plan`)

## Research → Architecture handoff — US-0090 (input-side Caveman-style compression)

- **From**: **tech-lead** (**`/research`** phase for US-0090, `auto-20260418-01`, `fresh_context_marker=tl-US0090-research-20260418T210000Z-fresh`)
- **To**: **tech-lead** (fresh **`/architecture`** subagent, next phase; **do not reuse this phase's context**)
- **Research anchor**: **`R-0073`** (extended under shared anchor — **no** new `R-xxxx` allocated; US-0089 intake bundle `plan_area_coverage` maps both stories; DEC-0011 precedent).
- **Research closure**: **PASS**. Eleven questions **Q9–Q19** resolved — **Q13 / Q14 / Q18** `status=resolved` (concrete; architecture ratifies verbatim); **Q9 / Q10 / Q11 / Q12 / Q15 / Q16 / Q17 / Q19** `status=deferred_to_architecture` with explicit research recommendations; **zero** `still-open`.
- **Evidence (read these first, in order)**:
  1. `docs/engineering/research.md` **`R-0073`** "Research phase resolution pass (2026-04-18, TL, `auto-20260418-01`, US-0090 input-side)" — authoritative Q9–Q19 resolution matrix, option tradeoffs, and risk catalog (R8–R11).
  2. `docs/product/backlog.md` `## US-0090` `research_notes (2026-04-18, TL, ...)` — condensed summary; backlog status **OPEN** (US-0045).
  3. `decisions/DEC-0072.md` — the **binding** contract US-0090 extends (do **NOT** rewrite; extend under a new companion DEC).
  4. `.cursor/rules/caveman.mdc` + `template/.cursor/rules/caveman.mdc` — byte-identical; SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` at research time.
  5. `docs/engineering/architecture.md` `# US-0089` — substrate; new `# US-0090` section is an **addition**, not a replacement.
  6. `docs/engineering/runbook.md` Caveman subsection + `docs/engineering/auto-orchestration-reference.md` `TOKEN_PROFILE × CAVEMAN_MODE` paragraph — extension points for Q16 three-axis publication.
  7. `handoffs/intake_evidence/US-0089-intake-20260418.json` — intake bundle; `plan_area_coverage` includes US-0090 under the shared `R-0073` anchor.

- **What architecture MUST decide (eleven sections, candidate companion DEC §1–§11)**:
  1. **§1 — Three-axis non-substitution** (Q16): exact wording for the `TOKEN_PROFILE` vs `CAVEMAN_MODE` vs `CAVEMAN_COMPRESS_INPUT` orthogonality paragraph in `docs/engineering/auto-orchestration-reference.md` + `docs/engineering/runbook.md` (active + `template/`); decide three parallel sentences (research recommended) vs 2x2x2 table fallback; decide whether `DEC-0072` §1 is extended in-place or §1 of the companion DEC forward-links to `DEC-0072` §1.
  2. **§2 — Activation gate** (Q13): exact `CAVEMAN_COMPRESS_INPUT=1` + non-empty `CAVEMAN_FILE_SCOPE` activation semantics; empty-scope default = pure opt-in (no files in scope; fails closed with `CAVEMAN_COMPRESS_SCOPE_EMPTY`); decide flag-conflict precedence rules (e.g. `--dry-run --write` simultaneously — research recommends fail-closed with `CAVEMAN_COMPRESS_FLAG_CONFLICT`); lock whether `--purge-orphans` ships in v1 (research recommends **deferred**).
  3. **§3 — Sidecar original policy** (Q10): lock Option B parallel-tree path pattern `docs/.caveman-originals/<relative/path>/<file>`; decide `.gitkeep` presence; decide whether `.cursorignore` receives a parity entry (research recommends leaving operator-owned per **US-0085**).
  4. **§4 — Deny-list source of truth** (Q11): lock Option C hybrid (hard-coded baseline + `.gitignore` secret-pattern merge + optional `.cursorignore` overlay); decide DEC-revision policy for the hard-coded baseline ("who can amend and through which DEC"); decide evaluation order — research recommends **deny-hard → ignore-merge → cursorignore overlay → allow-list → literal-region scan → write**.
  5. **§5 — Allow-list grammar** (Q12): lock Option C hybrid (named profile + raw globs + `profile:<name>;globs:<csv>` hybrid form); lock v1 profile set membership — candidate `docs-prose-only` → `docs/user-guides/**/*.md`, `docs/engineering/runbook.md`, `docs/engineering/state-archive/**/*.md`, `handoffs/archive/*.md`; decide unknown-profile behavior (research recommends fail-closed with `CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE`).
  6. **§6 — Compression algorithm** (Q9): lock hybrid tiering — `--mode=safe` default (line-level minifier: duplicate-blank-line collapse + trailing-whitespace trim + LF normalization) and `--mode=aggressive` opt-in (whitespace-collapse + frozen filler-word list + markdown-structure-preservation); decide whether aggressive mode ships in v1 or defers; lock exact `--mode` grammar and filler-word list contents (if aggressive ships); LLM-assisted compression **rejected** — architecture must not reopen.
  7. **§7 — Reason-code vocabulary** (Q15): lock 9-code set verbatim: `CAVEMAN_COMPRESS_SCOPE_VIOLATION`, `CAVEMAN_COMPRESS_DENY_HIT`, `CAVEMAN_COMPRESS_NOT_IDEMPOTENT`, `CAVEMAN_COMPRESS_LITERAL_REGION_DAMAGED`, `CAVEMAN_COMPRESS_ORIGINAL_MISSING`, `CAVEMAN_COMPRESS_MODE_DISABLED`, `CAVEMAN_COMPRESS_SCOPE_EMPTY`, `CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE`, `CAVEMAN_COMPRESS_FLAG_CONFLICT`; forbid post-write reason codes (all must be pre-write / during-write); group into three families (scope, integrity, gating) to control proliferation risk (R9).
  8. **§8 — CLI contract** (Q13): lock entrypoint name `scripts/caveman_compress_input.py`; lock modes `--dry-run` (default when no mutation mode), `--write`, `--verify-originals`, `--report`; lock exit-code contract (non-zero on any violation; `0` only when zero violations and zero unresolved parity asserts); `--mode=safe|aggressive` orthogonal to mutation mode.
  9. **§9 — Template parity** (Q17): lock 8-row inventory — (a) `scripts/caveman_compress_input.py` + `template/scripts/caveman_compress_input.py` byte-identical; (b) `docs/engineering/runbook.md` operator-UX section + mirror; (c) `docs/engineering/auto-orchestration-reference.md` three-axis paragraph + mirror; (d) `docs/engineering/architecture.md` `# US-0090` active-only; (e) `tests/auto_command_contract_test.py` extension **active-only**; (f) `tests/fixtures/caveman_compress/` active-only; (g) `.gitignore` `docs/.caveman-originals/` anchor; (h) optional `.cursor/rules/caveman.mdc` "Input-side extension (US-0090)" subsection — decide yes/no; if yes, active + `template/` must stay byte-identical (US-0017, risk R10).
  10. **§10 — Installer / publish surface** (Q19): lock `docs/engineering/context/installer-owned-paths.manifest` entry for `template/scripts/caveman_compress_input.py` under `install_include_paths` (defense against BUG-0003 regression class — risk R11); no new npm script; no new runtime dep per **`DEC-0072`** §8; decide parity-test strategy — (A) extend `scripts/check_intake_template_parity.py --scope=caveman-compress` (research recommended) vs (B) new `scripts/check_caveman_template_parity.py`; decide install-completeness fixture — extend `tests/installer_completeness_bug0003_test.py` vs new `tests/installer_caveman_completeness_test.py`.
  11. **§11 — Non-goals** (forward-link to `DEC-0072` §8; reaffirm carried bans): no `TOKEN_PROFILE` change, no `DEC-0072` rewrite, no vendor install path (no `npx skills add …`), no strict-proof / isolation-evidence wording change, no mandatory auto-compress in `/auto`, no tokenizer change, no npm / pip runtime dep (stdlib-only Python), no canonical-artifact rewrites (backlog / acceptance / state / intake-evidence / DEC-* / sprint-* / contract surfaces).

- **Mandatory architecture artifacts** (architecture phase must produce):
  1. **Companion DEC** (next available `DEC-xxxx` after current max) with §1–§11 above; forward-links (not rewrites) to `DEC-0072`.
  2. `docs/engineering/architecture.md` **`# US-0090`** section (active-only; does **not** mirror to `template/` per existing DEC-0072 §7 row 6 pattern) linking `# US-0089`, **US-0053**, **US-0085**, **US-0078** / **DEC-0060**, and explicitly enumerating forbidden surfaces (Q18 deny-list).
  3. `docs/engineering/decisions.md` index + full-record entry for the companion DEC (canonical context pack).
  4. `handoffs/tl_to_dev.md` pre-sprint architecture handoff prepended at top; preserve prior US-0089 stanza as superseded (lineage).
  5. `handoffs/resume_brief.md` new top pointer post-`/architecture` for US-0090 (mark prior post-`/research` US-0090 pointer superseded).
  6. `docs/engineering/state.md` Architecture checkpoint (2026-04-18) — US-0090 / `auto-20260418-01` (isolation + DEC-0038 strict proof + phase boundary block + AC-10 line + preflight for `/sprint-plan`).

- **Risks carried to architecture** (from research resolution pass):
  - **R8** (Q9): aggressive-mode filler-word list drift → mitigation = architecture locks DEC-revision policy + `--report` emits list hash for operator drift detection.
  - **R9** (Q15): reason-code proliferation at 9 codes — upper edge for single rule-file page. Mitigation = group into three families; forbid further proliferation without DEC.
  - **R10** (Q17): if architecture adds a `caveman.mdc` subsection, active + `template/` byte-identity must hold (US-0017); sprint-plan task acceptance evidence must recompute SHA-256 post-edit; pre-US-0090 baseline `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`.
  - **R11** (Q19): omitting install-completeness fixture would reintroduce the exact defect class **BUG-0003** fixed. Architecture must not ship US-0090 without this fixture even under sprint-size pressure.

- **Scope guards for architecture** (non-negotiables; do not cross):
  - **Do not rewrite** `DEC-0072` — write a new companion DEC that extends via §-references.
  - **Do not change** `.cursor/rules/caveman.mdc` without mirroring in `template/` byte-identically (US-0017).
  - **Do not change** `TOKEN_PROFILE` / `CAVEMAN_MODE` semantics (US-0080, DEC-0062, DEC-0072 §1 orthogonality).
  - **Do not change** strict-proof / isolation-evidence wording (US-0056 / DEC-0038, US-0048 / DEC-0029) or AC-10 phase-boundary block contract.
  - **Do not change** `AUTO_QUIET` non-suppressible list (US-0088), spawn-only / phase-role (US-0069 / DEC-0051 / BUG-0006), or user-visible metadata policy (US-0071).
  - **Do not alter** `docs/product/backlog.md` status for US-0090 (stays **OPEN** — US-0045 status authority; closure at `/release`).
  - **Do not** seed sprint tasks — that is `/sprint-plan`'s job after `/architecture` lands the companion DEC.

- **Next phase**: **`/architecture`** (fresh **tech-lead**) for **US-0090** — lock companion DEC §1–§11 (as above) + write `# US-0090` architecture section.
- **Decision-gate posture**: **none** expected before `/architecture` produces the companion DEC; architecture phase **is itself** the decision gate.
- **Status authority**: **US-0090** stays **OPEN** per **US-0045**. No acceptance rows checked by research.
- **Artifact refs**:
  - `docs/engineering/research.md` **`R-0073`** "Research phase resolution pass (2026-04-18 ...)" (appended this phase)
  - `docs/product/backlog.md` **`## US-0090`** `research_notes (2026-04-18, TL, auto-20260418-01)` (appended this phase)
  - `docs/engineering/state.md` — Research checkpoint (2026-04-18) — US-0090 / `auto-20260418-01` (isolation + DEC-0038 strict proof + phase boundary block + AC-10 line + preflight for `/architecture`)
  - `handoffs/resume_brief.md` — new top pointer post-`/research` US-0090 (prior post-`/discovery` US-0090 pointer marked superseded)
  - `decisions/DEC-0072.md` (binding substrate; architecture extends via companion DEC)
  - `.cursor/rules/caveman.mdc` + `template/.cursor/rules/caveman.mdc` (byte-identical research-verified baseline)
  - `docs/engineering/architecture.md` **`# US-0089`** (substrate for new `# US-0090` section)

## Architecture Addendum — US-0090 (companion DEC authored; ready for `/sprint-plan`)

- **From**: **tech-lead** (**`/architecture`** phase for US-0090, `auto-20260418-01`, `fresh_context_marker=tl-US0090-architecture-20260418T220000Z-fresh`)
- **To**: **tech-lead** (fresh **`/sprint-plan`** subagent, next phase; **do not reuse this phase's context**). Parallel handoff at top of `handoffs/tl_to_dev.md` (`## TL -> Dev Handoff — US-0090 (post-architecture)`).
- **Binding decision**: **`DEC-0073`** (**composes on** **`DEC-0072`** via forward-link; does **NOT** rewrite `DEC-0072`). `§1`–`§11` map 1:1 to the eleven research-phase architecture-asks above.
- **Architecture section**: **`docs/engineering/architecture.md`** **`# US-0090`** appended (active-only — story-scoped architecture sections do not mirror to `template/`; DEC-0072 §7 row 6 precedent).
- **Research closure**: all eight deferred questions resolved (Q9 — safe-mode minifier only / aggressive deferred; Q10 — Option B parallel tree; Q11 — Option C hybrid; Q12 — Option C hybrid with frozen `docs-prose-only` profile; Q15 — 9-code vocab grouped in three families; Q16 — three parallel sentences extending DEC-0072 §1 in place; Q17 — 8-row parity inventory + rule-subsection decided **NO** in v1; Q19 — manifest entry + extend existing parity script + extend existing completeness test). Three concrete questions (Q13/Q14/Q18) ratified verbatim. Four risks (R8/R9/R10/R11) resolved by architectural means.

### Atomic task seeds (one per AC; `/sprint-plan` converts to `T-xxx` and may split/group)

| # | Seed | AC | DEC-0073 § | Active surface(s) | Template surface(s) |
|---|------|----|-----------|-------------------|---------------------|
| 1 | **`scripts/caveman_compress_input.py`** — implement CLI (`--dry-run` default, `--write`, `--verify-originals`, `--report`), activation gate (§2), deny-list layered eval (§4), allow-list grammar (§5), safe-mode minifier (§6), reason-code emission (§7), atomic sidecar write order (§3). Stdlib Python only. | AC-1, AC-2, AC-3, AC-4, AC-5 (CLI) | §2, §3, §4, §5, §6, §7, §8 | `scripts/caveman_compress_input.py` | `template/scripts/caveman_compress_input.py` (byte-identical) |
| 2 | **Runbook subsection** — `### Caveman input compression (US-0090)` with 3-step dry-run → verify → write procedure, deny summary, `.cursorignore` operator-owned note, sidecar explanation. | AC-5, AC-7 | §1 three-sentence paragraph + §9 row 2 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` |
| 3 | **Three-axis non-substitution paragraph** — replace DEC-0072 §1 paragraph with three parallel sentences (`TOKEN_PROFILE` / `CAVEMAN_MODE` / `CAVEMAN_COMPRESS_INPUT`). | AC-7 | §1 + §9 row 3 | `docs/engineering/auto-orchestration-reference.md` | `template/docs/engineering/auto-orchestration-reference.md` |
| 4 | **Sidecar tree anchor** — `docs/.caveman-originals/.gitkeep` (new; empty file) + repo-root `.gitignore` anchor `docs/.caveman-originals/`. | AC-2 | §3 + §9 rows 7 & 8 | `.gitignore`, `docs/.caveman-originals/.gitkeep` | n/a (installer does not own repo `.gitignore`; sidecar root is repo-local state) |
| 5 | **Contract-test extension** — extend `tests/auto_command_contract_test.py` in place with `test_caveman_compress_input_*` prefix. **Must not** modify existing `test_caveman_default_off_*` subtests (DEC-0072 §6 row 6 invariant). | AC-6 | §9 test strategy | `tests/auto_command_contract_test.py` | n/a (tests do not mirror) |
| 6 | **Fixture directory** — `tests/fixtures/caveman_compress/` with 8 fixture classes (whitespace / literal-region / deny-list / scope / idempotency / mode-disabled / original-missing / flag-conflict). | AC-6 | §9 test strategy classes 1–8 | `tests/fixtures/caveman_compress/` | n/a |
| 7 | **Rule byte-identity guard + deny-list version guard** — add two subtests under (5): (a) SHA-256 equality of `.cursor/rules/caveman.mdc` active vs `template/`; (b) stable `--report deny_list_version` hash. | AC-6, AC-8 | §9 test strategy + §4.2 | `tests/auto_command_contract_test.py` (same file as seed 5) | n/a |
| 8 | **Installer manifest entry** — add `template/scripts/caveman_compress_input.py` under `install_include_paths` (active + `template/`). | AC-8 | §10 | `docs/engineering/context/installer-owned-paths.manifest` | `template/docs/engineering/context/installer-owned-paths.manifest` |
| 9 | **Parity-test extension** — extend `scripts/check_intake_template_parity.py` with `--scope=caveman-compress` mode asserting script byte-identity. | AC-8 | §10 Option A | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` |
| 10 | **Install-completeness fixture extension** — extend `tests/installer_completeness_bug0003_test.py` to verify `--mode missing` + `--mode upgrade` deliver `template/scripts/caveman_compress_input.py` across all three installer entrypoints (`installer.sh`, `installer.ps1`, `installer.py`). Add new `run-tests` section (candidate `§26S`; sprint-plan locks exact number) in `tests/run-tests.ps1` + `tests/run-tests.sh`. | AC-8, AC-6 | §10 Option A + §9 test strategy | `tests/installer_completeness_bug0003_test.py`, `tests/run-tests.ps1`, `tests/run-tests.sh` | n/a (tests + harness active-only) |
| 11 | **Architecture section linkage check** — assert-only task verifying `docs/engineering/architecture.md` **`# US-0090`** references `# US-0089`, US-0053, US-0085, US-0078 / DEC-0060 and enumerates forbidden surfaces. No rewrite. | AC-7 | §9 row 4 | `docs/engineering/architecture.md` (read-only check) | n/a |

**Task count**: 11 candidate seeds. `SPRINT_MAX_TASKS=12` (default). Sprint-plan may group seeds 5 & 7 (same test file) and/or 1 & 4 (one commit pair) to land at `T-001..T-009` or `T-001..T-010`. `SPRINT_AUTO_SPLIT` NOT expected to trigger.

### Test surfaces (no implementation here; sprint-plan + execute own code)

- **`tests/auto_command_contract_test.py`** — extend **in place** with `test_caveman_compress_input_*` subtests (mandatory). Existing `test_caveman_default_off_*` UNCHANGED byte-for-byte (DEC-0072 §6 row 6 invariant).
- **`tests/fixtures/caveman_compress/`** — 8 fixture classes (see DEC-0073 §9).
- **`tests/installer_completeness_bug0003_test.py`** — extend with caveman-script delivery assertion (R11; non-negotiable).
- **`tests/run-tests.ps1` + `tests/run-tests.sh`** — new section (candidate `§26S`; sprint-plan locks).
- **No new pytest module** in v1 (follow DEC-0072 / US-0089 precedent — in-place extension).

### Template parity touchpoints (8-row positive + 4-class negative)

**Positive parity (active + `template/` byte-identical)**:

1. `scripts/caveman_compress_input.py` ↔ `template/scripts/caveman_compress_input.py`
2. `docs/engineering/runbook.md` ↔ `template/docs/engineering/runbook.md` (caveman-compression subsection)
3. `docs/engineering/auto-orchestration-reference.md` ↔ `template/docs/engineering/auto-orchestration-reference.md` (three-sentence paragraph)
4. `docs/engineering/context/installer-owned-paths.manifest` ↔ `template/docs/engineering/context/installer-owned-paths.manifest` (caveman script entry)
5. `scripts/check_intake_template_parity.py` ↔ `template/scripts/check_intake_template_parity.py` (scope extension)

**Active-only (no mirror; per DEC-0072 §7 precedent)**:

6. `docs/engineering/architecture.md` `# US-0090` section
7. `tests/auto_command_contract_test.py` + `tests/fixtures/caveman_compress/`
8. `.gitignore` + `docs/.caveman-originals/.gitkeep`

**NEGATIVE parity (MUST NOT be edited in v1)**:

- `.cursor/rules/caveman.mdc` + `template/.cursor/rules/caveman.mdc` (SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` preserved; rule byte-identity guard subtest enforces).
- `.cursor/scratchpad.md`, `.cursor/scratchpad.local.example.md`, `template/.cursor/scratchpad.local.example.md` (key byte-strings from DEC-0072 §3 preserved; semantics activate without rename).
- `.cursor/skills/its-magic/SKILL.md` + mirror (DEC-0072 §7 row 9 preserved).
- `.cursorignore` (operator-owned per US-0085 / DEC-0071).
- All canonical-artifact / contract-surface files listed in DEC-0073 §4.1.

### Release / verify gates

- **`/plan-verify`**: AC-1..AC-8 ↔ `T-xxx` 1:1 bijection; governance anchors verified (`DEC-0073`, `DEC-0072` composition, `# US-0090`, `R-0073`).
- **`/execute`**: dev MUST commit active + `template/` pairs atomically for parity rows 1–5; MUST NOT edit any NEGATIVE-parity file; MUST keep `test_caveman_default_off_*` byte-unchanged.
- **`/qa`**: canonical `tests/run-tests.ps1` (+ `run-tests.sh`) green for the new `§26S` + all existing sections; targeted pytest — all `test_caveman_compress_input_*` + `test_caveman_default_off_*` pass; `bug_issue_validate.py` `[BUG_VALIDATION_OK]`; rule byte-identity guard green; deny-list version guard green; install-completeness fixture green for `--mode missing` + `--mode upgrade` across all three entrypoints.
- **`/verify-work`**: UAT 8/8 on AC-1..AC-8; isolation evidence + strict-proof tuples present for every phase in `docs/engineering/state.md`; `handoffs/release_queue.md` → `ready`.
- **`/release`**: flip backlog `OPEN` → `DONE`; check AC-1..AC-8 in `docs/product/backlog.md` + portfolio row in `docs/product/acceptance.md`; author `sprints/SXXXX/release-findings.md` + `handoffs/releases/SXXXX-release-notes.md`; release-queue `ready` → `released`; publish mode: per existing `RELEASE_PUBLISH_MODE` operator default (no new publish flag).

### Risks carried (architecture-resolved; sprint-plan should preserve mitigations)

- **R8** — filler-word drift → neutralized in v1 by **deferring aggressive mode** (DEC-0073 §6). Sprint-plan must NOT reopen.
- **R9** — reason-code proliferation → locked 9-code set grouped into three families (DEC-0073 §7). Sprint-plan must NOT add codes.
- **R10** — rule-subsection byte-identity → **no rule edit in v1** (DEC-0073 §9 NEGATIVE parity). Sprint-plan must NOT seed a rule-subsection task. Byte-identity guard subtest (seed 7) is a hard requirement.
- **R11** — install-completeness omission (BUG-0003 class) → install-completeness fixture extension (seed 10) is **non-negotiable**. Sprint-plan MUST seed it regardless of sprint-size pressure. `/release` MUST NOT ship without it.

### Scope guards for `/sprint-plan` (non-negotiables; do not cross)

- **Do not re-open** any architecture-locked decision in DEC-0073 §§1–11.
- **Do not rewrite** `DEC-0072` or `DEC-0073`. Sprint-plan authors `sprints/SXXXX/*`, not DECs.
- **Do not edit** `.cursor/rules/caveman.mdc` (byte-identity preserved — seed 7 guard asserts).
- **Do not add** new reason codes, new CLI flags (e.g. `--mode`, `--purge-orphans`), new profiles, new fixture classes beyond §9, or new deny-list entries without a subsequent DEC.
- **Do not change** `TOKEN_PROFILE` / `CAVEMAN_MODE` / strict-proof (DEC-0038) / isolation-evidence (DEC-0029) / `AUTO_QUIET` (US-0088) / US-0071 contracts.
- **Do not advance** backlog status. US-0090 stays **OPEN** per **US-0045** (closure at `/release`).
- **Do not seed tasks** outside the 11 seeds above without explicit justification tied to a specific AC.

### Mandatory `/sprint-plan` deliverables (next phase)

1. `sprints/SXXXX/sprint.md` with summary, AC table, locked DEC anchors (`DEC-0073` + `DEC-0072` composition), research anchor (`R-0073`), success gate.
2. `sprints/SXXXX/tasks.md` with `T-001..T-Nxx` atomic tasks + AC map + DEC-0073 § locks per row.
3. `sprints/SXXXX/plan-verify.json` `status=PENDING`, `reason=AWAITING_QA_PLAN_VERIFY`.
4. Empty-stub scaffold: `sprints/SXXXX/summary.md`, `sprints/SXXXX/qa-findings.md`, `sprints/SXXXX/uat.json`, `sprints/SXXXX/uat.md`, `sprints/SXXXX/release-findings.md`.
5. `handoffs/tl_to_dev.md` sprint-plan stanza prepended; prior architecture stanza preserved as lineage.
6. `handoffs/qa_plan_verify.md` QA entrypoint pointer.
7. `handoffs/resume_brief.md` new top pointer post-`/sprint-plan`; intended_resume_phase=`plan-verify`.
8. `docs/engineering/state.md` Sprint-plan checkpoint (isolation + strict proof + phase boundary block + AC-10 compact line + `[BUG_VALIDATION_OK]`).
9. `docs/product/backlog.md` **`## US-0090`** `sprint_plan_notes` appended (US-0090 remains **OPEN** per **US-0045**).

### Artifact refs (architecture phase materializations)

- `decisions/DEC-0073.md` (new; composes on `DEC-0072`).
- `docs/engineering/decisions.md` — `## Current context pack` header refreshed + `DEC-0073` entry appended to "Compact decision index".
- `docs/engineering/architecture.md` `# US-0090` (new section appended at bottom).
- `docs/product/backlog.md` `## US-0090` `architecture_notes (2026-04-18, TL, auto-20260418-01)` appended.
- `docs/engineering/state.md` — Architecture checkpoint (2026-04-18) — US-0090 / `auto-20260418-01` (isolation + strict proof + phase boundary block + AC-10 line).
- `handoffs/tl_to_dev.md` — **US-0090 architecture** stanza prepended at top; prior US-0089 stanza preserved.
- `handoffs/resume_brief.md` — new top pointer post-`/architecture` US-0090 (prior post-`/research` US-0090 pointer marked superseded).
- `handoffs/po_to_tl.md` — this `## Architecture Addendum — US-0090` section appended.

### Next phase

- **`/sprint-plan`** (fresh **tech-lead**) for **US-0090** — seed `sprints/SXXXX/*` from the 11 task seeds above + the AC ↔ § map.
- **Decision-gate posture**: **none** expected — architecture phase IS the decision gate; sprint-plan translates decisions into atomic tasks.
- **Status authority**: **US-0090** stays **OPEN** per **US-0045**. No acceptance rows checked by architecture.

