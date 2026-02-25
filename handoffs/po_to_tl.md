# PO -> TL Handoff — Intake: Release Doc Delta Gate + Optional Spec Pack

## Intake Context

User request in fresh `/intake` context:

1. Release gate must include README/runbook delta check when commands/flags changed.
2. Also create Design Concept, CRS, and Technical Specification if enabled.

This is treated as process/workflow enhancement (not feature implementation).

## Overlap and Duplicate Evaluation

- No direct duplicate found in current backlog.
- Related but non-duplicate stories:
  - `US-0015`: runbook command documentation intent (narrower and already handled).
  - `US-0024`: memory drift auditing (advisory/read-only, not release blocking).
  - `US-0028` and `US-0029`: optional flag-driven behavior pattern (useful precedent).
- Decision: add two new stories instead of modifying existing ones to keep scope explicit and testable.

## Stories Accepted

### US-0030 — Release Gate for Command/Flag Documentation Delta
- Intent: prevent release drift where behavior changes are not reflected in docs.
- Scope: release/process guardrail requiring README + runbook parity for changed commands/flags.
- Priority: P1
- Status: OPEN
- Backlog artifact: `docs/product/backlog.md` (8 ACs)

### US-0031 — Optional Documentation Pack (Design Concept, CRS, Technical Spec)
- Intent: support teams that require formal docs without imposing overhead on everyone.
- Scope: optional generation/validation path controlled by config/flag.
- Priority: P2
- Status: OPEN
- Backlog artifact: `docs/product/backlog.md` (8 ACs)

## Split/Merge Rationale

- Split was chosen because the stories have different triggers and risks:
  - `US-0030` is always in release-critical path and should be strict/blocking.
  - `US-0031` is optional and policy-driven, with zero-overhead expectation when disabled.
- Merging would blur blocking behavior and make acceptance testing ambiguous.

## Boundaries for TL

- In scope:
  - Workflow rules/commands/readiness checks.
  - Artifact conventions, role ownership, and pass/fail criteria.
  - Template parity where process guidance exists in both active and `template/`.
- Out of scope:
  - New runtime product features.
  - Domain-specific content authoring beyond minimum structure for Design Concept/CRS/Technical Spec.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Delta check over-blocks unrelated releases | Throughput drops | Require explicit changed command/flag evidence before gate applies |
| Delta check under-detects actual behavior changes | Doc drift persists | Define canonical detection scope and required evidence output in gate report |
| README vs runbook ownership unclear | Ping-pong and delays | Assign ownership by phase/role and enforce in handoff checklist |
| Optional spec-pack defaults to noisy workflow | Team friction | Keep default disabled and require explicit enable flag |
| Spec-pack artifacts become shallow placeholders | False confidence | Enforce minimum required sections and completeness checks |
| Active/template drift for new guidance | Inconsistent installs | Include template parity AC and verify in release checklist |

## TL Planning Recommendations

1. Implement `US-0030` first (higher release risk reduction, tighter scope).
2. Implement `US-0031` second (optional path, broader cross-phase ownership).
3. Define one canonical flag for spec-pack enablement early in architecture.
4. Define deterministic evidence format for doc-delta gate output so QA can assert pass/fail reliably.

## Expected Deliverables in Next Phases

- Architecture defines:
  - command/flag delta detection boundaries,
  - blocking conditions and override policy (if any),
  - spec-pack artifact names/locations and required sections.
- Sprint plan maps both stories to tasks with explicit template parity checks.
- QA verifies gating behavior with positive/negative cases for both enabled and disabled modes.

---

## Intake Addendum — Optional User-Friendly Feature Instructions

### New intake

User asks for "an option for generating a user-friendly instruction/doc of every feature."

### Overlap and duplicate evaluation

- Closest overlap: `US-0031` (optional spec-pack with Design Concept, CRS, Technical Spec).
- Assessment: related but not duplicate.
  - `US-0031` targets internal/engineering specification artifacts.
  - New request targets user-facing, feature-level usage instructions.
- Decision: create a new story to avoid mixing audiences, ownership, and acceptance checks.

### Accepted story

#### US-0032 — Optional Feature User Guide Generation
- Priority: P2
- Status: OPEN
- Why separate from `US-0031`:
  - Keeps technical spec completeness checks separate from user-guide quality checks.
  - Prevents one optional mode from becoming ambiguous and overly broad.
  - Preserves clear role boundaries (technical authorship vs end-user documentation tone).

### TL guidance and boundaries

- In scope:
  - Optional, flag-controlled per-feature user guide artifacts.
  - Deterministic required sections and validation when enabled.
  - Story-to-guide traceability and release/handoff references.
  - Active/template parity for docs/commands/rules touching this mode.
- Out of scope:
  - Replacing or merging with `US-0031` technical spec-pack artifacts.
  - Mandatory overhead in default mode.
  - Full product manual generation beyond per-feature guidance.

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
