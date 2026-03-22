## Discovery Addendum — US-0075 (2026-03-26)

### Discovery focus

- Example **`.cursor/scratchpad.local.example.md`** must refresh on every install/upgrade scratchpad touch **before or with** materialized **`.cursor/scratchpad.md`** (**AC-1**, **AC-3**).
- **AC-11**: machine-verifiable paired **section + `KEY=`** inventory (active + **`template/`** pairs); no framework key in only one paired file without a documented manifest exception.

### TL conclusions

- Ordering + parity are one contract across installers, manifest, and tests (splitting re-opens drift).
- Example = operator copy-from catalog; materialized baseline = **DEC-0055** merge input; **`.cursor/scratchpad.local.md`** stays user-owned — diagnostics name which layer changed (**AC-5**).
- Regression: stale-example + fresh-template upgrade → post-run example matches template bytes (**AC-6**, **AC-9**).

### Research targets (**`R-0052`**)

1. Deterministic refresh sequence: **`installer.ps1` / `.sh` / `.py`**, **`bin/its-magic.js`**, **`installer-owned-paths.manifest`** (+ `template/` mirror).
2. Parity check spec: normalization, **`KEY=`** taxonomy, allowed value-only differences in example.
3. **DEC-0055** / **DEC-0039** / **US-0057** interaction — amend **DEC** only if ordering needs normative text beyond current records.

### Next

- **`/research`** (extend **`R-0052`**), then **`/architecture`** if a **DEC** tweak is required.

> Full narrative also in `docs/product/vision.md` (**Discovery Notes — US-0075**) and `docs/product/backlog.md` (discovery refinement). Prior rollover copy: `handoffs/archive/po-to-tl-pack-20260321-c.md`.

---

## Intake Addendum — Configurable Guided Intake Behavior

### New intake

User requests stronger PO intake behavior:
- Ask reasonable follow-up questions when unclear.
- Suggest options instead of prematurely selecting implementation.
- Include PO web research.
- Provide a switch to disable this proactive behavior.

### Overlap and duplicate evaluation

- Existing overlap:
  - `US-0021` (DONE): already requires critical evaluation, alternatives, and user-final-decision behavior.
  - `US-0029` (inconsistent status across artifacts, but behavior already present in active command/agent docs): includes PO early web research and `EARLY_RESEARCH` toggle.
- Gap identified:
  - No single intake behavior switch that disables proactive follow-up + options + intake-time research while keeping baseline duplicate safety.
- Decision:
  - Create `US-0033` as a focused behavior-mode story instead of reopening/compressing prior story scope.

### Accepted story

#### US-0033 — Configurable Guided Intake Behavior
- Priority: P1
- Status: OPEN
- Intent: default guided intake quality, optional low-touch mode for teams that want minimal interaction overhead.

### TL guidance and boundaries

- In scope:
  - Define one explicit scratchpad flag for intake behavior mode (default guided/on).
  - Specify guided mode requirements (targeted follow-ups, options, recommendation without overriding user decision).
  - Specify low-touch mode requirements (no proactive follow-up/options/research overhead).
  - Preserve baseline duplicate/overlap check in both modes.
  - Keep active and `template/` guidance aligned.
- Out of scope:
  - Changing architecture/sprint/release semantics.
  - Removing manual `/research` usage when low-touch mode is enabled.

## Intake Addendum — Multi-Repo Compatibility + Component-Scoped Execution

### New intake (German source summary)

User asks for:
1. Monitoring across multiple repos/modules for software modules, docs, API descriptions, and API compatibility.
2. A way to work on one component in a repo with multiple components, without breaking others.

This is accepted as workflow/process capability (not runtime application feature behavior).

### Overlap and duplicate evaluation

- No direct duplicate found in current backlog.
- Closest related stories, but distinct scope:
  - `US-0017` template drift guard: parity/sync concern, not compatibility observability.
  - `US-0024` memory drift audit: compares artifacts vs code in one repo, read-only audit; no cross-repo contract focus.
  - `US-0025` traceability contract: links stories and sprint tasks; does not enforce component scoping or compatibility checks.
  - `US-0033` guided intake behavior: interaction mode only, not execution scoping or module compatibility validation.
- Workflow overlap noted with `/intake`, `/architecture`, `/execute`, `/qa`, but no existing story provides these capabilities end-to-end.

### Split decision

- Decision: create **two stories** (`US-0034`, `US-0035`) instead of one merged story.
- Rationale:
  - Different trigger and risk model:
    - `US-0034` is observability + compatibility signal generation and optional release gate behavior.
    - `US-0035` is day-to-day scoped execution safety and out-of-scope impact control.
  - Splitting keeps acceptance tests concrete and avoids mixed pass/fail semantics.

### Accepted stories

#### US-0034 — Multi-Repo and Contract Compatibility Observability
- Priority: P1
- Status: OPEN
- Key intent: optional, flag-driven compatibility visibility across repos/modules/contracts with zero-overhead default when disabled.

#### US-0035 — Component-Scoped Execution Mode with Protection Guards
- Priority: P1
- Status: OPEN
- Key intent: optional, flag-driven component targeting and unaffected-component protection checks with zero-overhead default when disabled.

### TL architecture boundaries

- In scope:
  - Define canonical flags and defaults for both stories.
  - Define canonical artifacts for compatibility findings and scoped-impact evidence.
  - Define decision-gate rules for critical compatibility breakage or unapproved out-of-scope impact.
  - Ensure command/rule/doc updates include active + `template/` parity.
- Out of scope:
  - Runtime service behavior changes.
  - Full cross-repo orchestration platform implementation.
  - Build-system redesign across monorepos.

### Suggested implementation order

1. `US-0035` first to reduce immediate change-risk in multi-component repos.
2. `US-0034` second to add broader compatibility observability and release-time confidence.

## Intake Addendum — Official Remote Config Template, Docs, and Validation

### New intake

User request: "Ship official `.cursor/remote.json` template + docs + validation."

Confirmed context in scratchpad:
- `REMOTE_EXECUTION` flag already exists.
- `REMOTE_CONFIG=.cursor/remote.json` already exists.
- Repository currently lacks an official `.cursor/remote.json` template artifact.

### Overlap and duplicate evaluation

- No direct duplicate found in current backlog.
- Related but non-duplicate stories:
  - `US-0017` template drift guard: parity governance only; does not define remote config schema or validation contract.
  - `US-0030` release doc-delta gate: release-time docs parity check; does not define remote execution configuration behavior.
  - `US-0028` optional security review: establishes "optional feature with zero-overhead-off mode" pattern; remote config is separate capability.
- Decision: create a new story so remote config contract/safety requirements remain explicit and testable.

### Accepted story

#### US-0036 — Official Remote Config Template, Docs, and Fail-Fast Validation
- Priority: P1
- Status: OPEN
- Intent: make remote execution safe and deterministic by shipping canonical config artifacts, schema guidance, and strict validation rules when enabled.

### TL guidance and boundaries

- In scope:
  - Canonical `.cursor/remote.json` in active + `template/`.
  - Documented schema/field contract and example targets.
  - Fail-fast validation behavior for enabled mode (`REMOTE_EXECUTION=1`).
  - Clear error-message contract and remediation hints.
  - Security guidance: no secrets committed in repo config.
  - README + runbook instructions, plus template parity verification.
  - Zero-overhead behavior when `REMOTE_EXECUTION=0`.
- Out of scope:
  - Implementing new remote transport protocols/backends.
  - Building external secret-management infrastructure.

### Planning recommendation

1. Define the remote config schema first (required/optional fields + allowed values).
2. Implement and document validation contract second (including error text expectations).
3. Add docs/runbook/README coverage and parity checks across active + template copies.
4. Include negative-path QA cases (missing file, malformed JSON, invalid fields, secret-like values).

---

## Intake Addendum — Mid-Process Full Automation Continuation

### New intake

User asks for a way to start full automation from mid-process:
- pause/resume plus scratchpad `PHASE_MODE=auto` still feels step-by-step with manual prompts
- expectation is one command that continues the remaining workflow automatically from the correct point

### Overlap and duplicate evaluation

- Existing overlap:
  - `US-0023` (DONE): defines fresh subagent context per phase and `/auto` orchestration model.
  - Existing commands `.cursor/commands/auto.md`, `.cursor/commands/resume.md`, `.cursor/commands/pause.md` describe pieces of the behavior.
- Gap identified:
  - No explicit `/auto` mid-process resume-point input contract (`start-from` style).
  - No deterministic precedence contract for resume source resolution (resume brief vs state fallback) with conflict handling.
  - No single, testable "continue remaining phases without manual phase triggers" acceptance contract.
- Decision:
  - Create a new focused story (`US-0037`) instead of reopening `US-0023`, so implementation scope stays concrete and regression-safe.

### Accepted story

#### US-0037 — Mid-Process `/auto` Continuation with Deterministic Resume Point
- Priority: P1
- Status: OPEN
- Intent: make `/auto` continuation behavior explicit, deterministic, and testable while preserving current safe defaults and decision gates.

### TL guidance and boundaries

- In scope:
  - Add explicit `/auto` `start-from` phase support.
  - Define deterministic resume-source precedence (`handoffs/resume_brief.md` first, then `docs/engineering/state.md` fallback).
  - Define safe failure behavior for missing/stale/conflicting resume inputs.
  - Require one-command continuation through remaining phases with existing stop conditions.
  - Add continuation breadcrumbs/logging to artifacts for inspectability.
  - Align `/pause`, `/resume`, `/auto` semantics and keep active + `template/` parity.
- Out of scope:
  - Bypassing decision gates or missing-input blockers.
  - Changing phase deliverables or introducing unrelated runtime features.

### Suggested implementation order

1. Define canonical phase IDs and `start-from` validation contract.
2. Implement deterministic resume-source resolver and conflict policy.
3. Update `/auto`, `/resume`, `/pause` docs/rules for semantic alignment.
4. Add QA cases for explicit start, implicit resume, conflict, missing source, and stop-reason logging.

---

## Intake Addendum — Phase-Triggered Sync + Release Gate Tightening

### New intake (translated requirement intent)

User asks for:
1. Push/sync functionality triggered after completed phases.
2. Configurable cadence defining which phase intervals trigger sync.
3. Prefer sync only after tests and QA are complete.
4. Automatic check-in tests should always run.
5. Release should happen only after those checks.

### Overlap and duplicate evaluation

- No direct duplicate found in backlog.
- Related but non-duplicate stories:
  - `US-0014` quality chain: establishes local validate-and-push and CI layering, but not phase-trigger policy semantics.
  - `US-0030` release doc-delta gate: release-time documentation parity, not test/QA gate ordering.
  - `US-0037` auto continuation: orchestration resume behavior, not sync/push policy.
- Current workflow/script observations:
  - `scripts/validate-and-push.ps1` and `scripts/validate-and-push.sh` already enforce check-before-push in manual invocation flow.
  - `/qa` currently suggests validate-and-push before pushing, but does not enforce phase-trigger policy.
  - `/release` currently has UAT readiness gate, but no explicit mandatory check-in test + QA gate ordering contract.

### Split decision

- Decision: split into **two stories**.
- Rationale:
  - Sync cadence policy and guarded auto-push (`US-0038`) is phase-boundary orchestration behavior.
  - Release gate tightening (`US-0039`) is a final-stage blocking policy with deterministic evidence requirements.
  - Splitting avoids ambiguous acceptance tests and keeps safety gates independently verifiable.

### Accepted stories

#### US-0038 — Phase-Triggered Sync Policy with Guarded Auto-Push
- Priority: P1
- Status: OPEN
- Intent: configurable sync cadence with default-off safety, mandatory test checks, and no auto-push before QA pass for feature work.

#### US-0039 — Release Gate Tightening for Check-In Tests and QA/UAT Completion
- Priority: P1
- Status: OPEN
- Intent: `/release` proceeds only when check-in tests, QA, and UAT readiness gates pass in deterministic order.

### TL guidance and boundaries

- In scope:
  - Canonical sync policy modes and phase-trigger eligibility contract.
  - Mandatory `TEST_COMMAND` pre-push gate semantics with optional lint/typecheck integration.
  - Branch safety defaults (default deny for protected/default branch auto-push, explicit opt-in required).
  - Deterministic release gate order and evidence logging in state/handoff artifacts.
  - Active and `template/` parity for affected commands/rules/scripts docs.
- Out of scope:
  - New CI platform integrations.
  - Runtime application feature changes unrelated to workflow/release policy.
  - Forcing a single branching model across all repos.

### Recommended implementation order

1. Define `US-0038` policy schema and default-safe behavior first.
2. Implement release gate sequence (`US-0039`) using explicit evidence contracts.
3. Align `/execute`, `/qa`, `/release`, runbook notes, and validate-and-push scripts with the same decision vocabulary.
4. Add QA negative tests for pre-QA auto-push prevention, stale check evidence, and gate bypass attempts.

---

## Intake Addendum — Non-Overwriting Release Notes + Unreleased Sprint Queue

### New intake

User confirmed implementation of prior release-file recommendation:
1. Avoid overwriting single `handoffs/release_notes.md`.
2. Track unreleased sprints explicitly.

### Overlap and duplicate evaluation

- No direct duplicate found in backlog.
- Closest related stories:
  - `US-0038`: sync-policy evidence and push cadence semantics.
  - `US-0039`: release gate ordering and readiness blocking.
- Assessment: related but non-duplicate.
  - Existing stories govern gating and readiness criteria.
  - New request governs release artifact lifecycle/history preservation and queue visibility.
- Decision: create a new focused story to keep lifecycle/migration requirements testable.

### Accepted story

#### US-0040 — Per-Sprint Release Notes and Release Queue Tracker
- Priority: P1
- Status: OPEN
- Intent: preserve release history by sprint and provide deterministic queue state for unreleased/released sprint tracking.

### TL guidance and boundaries

- In scope:
  - Canonical per-sprint release note artifact path and naming contract.
  - Canonical release queue artifact with deterministic state transitions (`unreleased` -> `released`).
  - Safe migration/backfill behavior for existing `handoffs/release_notes.md`.
  - Backward compatibility behavior for workflows still reading `handoffs/release_notes.md`.
  - Command/rule/doc updates plus active/template parity checks.
- Out of scope:
  - Runtime deployment pipeline changes.
  - External release-management platform integration.
  - Redefining QA/UAT evidence model.

### Planning recommendation

1. Define canonical artifact contracts first (per-sprint notes + queue schema + ownership).
2. Define migration/backfill semantics second (resolvable sprint vs unresolved legacy content).
3. Update release command/rules/docs with deterministic transitions and fail-safe behavior.
4. Add QA coverage for overwrite prevention, unresolved sprint context, migration path, and parity checks.

---

## Intake Addendum — Lifecycle QA Expansion for Installer + CLI

### New intake

User requests deeper live QA for installation lifecycle behavior, including:
- install/update flows via `its-magic` command
- overwrite + backup behavior
- clean-repo safety (no accidental deletion of non-framework files)
- parity across PowerShell/shell/CI paths

### Overlap and duplicate evaluation

- Existing overlap:
  - `US-0008` (CLI installer) provides feature implementation.
  - current tests provide baseline install/upgrade checks.
- Gap identified:
  - missing full end-to-end lifecycle verification for clean-repo safety,
    CLI/direct-installer parity, and negative-path fail-fast behavior.
- Decision:
  - create focused QA expansion story `US-0041` (already added to backlog) to
    avoid mixing feature semantics with test-hardening scope.

### Accepted story

#### US-0041 — End-to-End Lifecycle QA for `its-magic` Install/Upgrade/Clean
- Priority: P1
- Status: OPEN
- Intent: increase release confidence with deterministic lifecycle coverage for
  install, overwrite+backup, upgrade, clean-repo safety, and invalid-argument paths.

### TL guidance and boundaries

- In scope:
  - lifecycle E2E test matrix for installer and CLI invocation paths
  - temp-dir isolation/idempotency guarantees in test scripts
  - platform parity subset in CI (`npm-test`, `brew-test`, `choco-test`)
  - README/runbook lifecycle QA documentation updates
- Out of scope:
  - redesigning installer behavior
  - introducing new installer modes or runtime deployment changes

---

## Intake Addendum — Post-QA Release Findings Workflow

### New intake

User requested an official workflow for issues found after QA at release gates,
with documentation symmetry to QA findings.

### Accepted story

#### US-0042 — Release Findings Artifact and Post-QA Issue Workflow
- Priority: P1
- Status: DONE
- Intent: ensure post-QA release issues are captured deterministically in a
  dedicated artifact + handoff path.

---

## Intake Addendum — Backlog Reconciliation After Release

### New intake

User reports repeated drift: sprint/release artifacts show completion while
`docs/product/backlog.md` still shows story status/ACs as incomplete.

Primary requirement:
- this mismatch must be solved structurally and must not happen again.

### Overlap and duplicate evaluation

- Related stories:
  - `US-0025` (backlog-to-sprint traceability): defines linkage/index behavior.
  - `US-0024` (memory drift audit): read-only detection/reporting.
  - `US-0040`/`US-0042`: release queue + release findings artifacts.
- Assessment:
  - No direct duplicate for **enforced post-release backlog reconciliation**.
  - Existing items either provide traceability or audit visibility, but do not
    enforce deterministic backlog mutation/fail-safe behavior at release boundary.
- Decision:
  - Create a focused story `US-0043` to make this invariant explicit and testable.

### Accepted story

#### US-0043 — Backlog Reconciliation Gate for Released Sprints
- Priority: P1
- Status: OPEN
- Intent: prevent recurrence of release/backlog contradiction by enforcing
  deterministic reconciliation or fail-safe blocking with explicit reason code.

### TL guidance and boundaries

- In scope:
  - Define canonical evidence precedence for reconciliation.
  - Add deterministic release-boundary reconciliation step.
  - Add fail-safe reason code and remediation contract for drift.
  - Add regression tests for positive and negative reconciliation paths.
  - Keep active/template command/rule/docs behavior aligned.
- Out of scope:
  - Replacing story ownership semantics.
  - Reworking sprint lifecycle phases.
  - Runtime product feature changes unrelated to workflow integrity.

### Planning recommendation

1. Define a single source-of-truth precedence for completion evidence.
2. Wire reconciliation at `/release` finalize boundary (or explicit
   post-release reconciliation step with equivalent guarantees).
3. Add deterministic reason-code/error output for contradictory states.
4. Add tests covering stale backlog after release and successful auto-reconcile.

---

## Intake Addendum — US-0015 Completion Clarification

### Context

`US-0015` already exists in backlog and does not require a new intake story.
The required work is execution completion: make the optional empty runbook
commands explicitly documented as intentional and regression-protected.

### Scope confirmation

- Keep optional command keys blank by default for this template repo.
- Document this intent clearly in runbook and README (active + template).
- Add regression checks so intent does not regress.

### Discovery notes

- Primary references reviewed for reconciliation patterns:
  - Evidence-first release readiness/checklist approaches (quality-gate style).
  - Status synchronization patterns where checklist completeness drives state
    transition, but only when deterministic evidence is present.
- Discovery conclusion:
  - Keep scope process/workflow-level and deterministic.
  - Prefer canonical evidence precedence + fail-safe drift reason codes over
    permissive auto-correction.

---

## Intake Addendum — Continuous `/auto` Backlog-Drain Mode

### New intake

User requests that once plans and stories are already defined, `/auto` should
continue working across stories until delivery completion, with configurable
switches to fine-tune stopping behavior.

### Overlap and duplicate evaluation

- Related stories:
  - `US-0037`: deterministic mid-process continuation for one flow.
  - `US-0038`: phase-triggered sync policy and guarded push controls.
  - `US-0043`: deterministic release/backlog reconciliation.
- Assessment:
  - no direct duplicate for **multi-story backlog-drain orchestration mode**.
  - existing stories govern single-flow continuation and safety gates, but not
    deterministic next-story selection + bounded multi-story progression.
- External references reviewed per `R-0008`:
  - deterministic checkpoint/replay orchestration patterns
  - human-approval gate patterns for high-impact operations
- Decision:
  - create `US-0044` as a dedicated orchestration story with explicit switches.

### Accepted story

#### US-0044 — Continuous `/auto` Backlog-Drain Mode with Fine-Tune Switches
- Priority: P1
- Status: OPEN
- Intent: allow optional unattended multi-story progress while preserving current
  safe defaults and decision-gate controls.

### TL guidance and boundaries

- In scope:
  - switch-controlled enable/disable of backlog-drain mode (default off)
  - deterministic next-story selection policy
  - bounded execution controls (max stories per run, stop/skip on blocked story)
  - per-story breadcrumbs and final run summary artifacts
  - active/template parity for command/rule/docs behavior
- Out of scope:
  - bypassing decision gates
  - changing story acceptance ownership/content model
  - runtime product behavior changes unrelated to workflow orchestration

---

## Intake Addendum — Canonical Story Status + Global Drift Normalization

### New intake

User requests a durable fix for recurring status drift across
`docs/product/backlog.md`, `docs/product/acceptance.md`, and
`docs/engineering/state.md`, including known completed stories still marked OPEN.
Intake objective is to make this mismatch class deterministic and non-recurring.

### Overlap and duplicate evaluation

- Related stories:
  - `US-0043`: released-sprint backlog reconciliation at release boundary.
  - `US-0044`: optional multi-story `/auto` backlog-drain orchestration.
  - `US-0025`: backlog-to-sprint traceability contract (still OPEN).
- Assessment:
  - not a duplicate of `US-0043`; current scope is broader than release boundary
    and includes historical normalization + cross-artifact status ownership.
  - complements `US-0044`; automation breadth does not solve status authority.
  - compatible with `US-0025`; this intake focuses status truth and drift guard.
- Research reference:
  - `R-0009` (canonical source + reconciliation/normalization pattern).
- Decision:
  - create `US-0045` as a dedicated P1 workflow integrity story.

### Accepted story

#### US-0045 — Canonical Story Status Source + Global Drift Guard
- Priority: P1
- Status: OPEN
- Intent: establish one authoritative status source and deterministic
  reconciliation so OPEN/DONE contradictions stop recurring in normal operation.

### TL guidance and boundaries

- In scope:
  - canonical story-status ownership contract (backlog authoritative)
  - deterministic reconciliation rules across backlog/acceptance/state
  - one-time historical normalization with auditable output
  - fail-safe reason-code handling for contradictory states
  - command/rule/doc updates plus active/template parity checks
- Out of scope:
  - runtime application feature changes
  - bypassing release/decision safety gates
  - replacing sprint sizing/planning policy with unbounded batching

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
