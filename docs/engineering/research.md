# Research

## Entry format (per DEC-0011)

Each research entry uses the R-xxxx ID format with semi-structured fields.

**Required fields**: ID (R-xxxx), Date (YYYY-MM-DD), Topic (short description).
**Optional fields**: Query, Sources, Findings, Linked (US-xxxx/DEC-xxxx refs),
Confidence (high/medium/low, default: medium), Status (current/outdated/superseded,
default: current).

### Auto-increment convention

Assign the next sequential R-xxxx ID by incrementing from the highest existing
entry in this file. Before creating a new entry, read this file to determine the
current highest ID.

### Cross-referencing guidance

Reference research entries by ID in other artifacts using the format "per R-xxxx".
Examples:
- In decisions: "per R-0001, prompt-level isolation is unreliable"
- In architecture: "R-0003 confirms the library supports streaming"
- In handoffs: "see R-0002 for competitor analysis"

Agents, commands, and handoffs should cite entry IDs whenever research informed
a decision or recommendation.

---

## R-0001

- **Date**: 2026-02-23
- **Topic**: Subagent context isolation for phase independence
- **Query**: How to guarantee independent review behavior across agent phases
- **Findings**:
  - Prompt-level instructions like "ignore prior chat" are advisory and not a
    reliable isolation boundary.
  - Artifact-first handoffs (`handoffs/*.md` + docs/sprints) already provide a
    strong context-transfer mechanism that supports hard context resets.
  - `/auto` must be orchestration-only; if it performs multi-role work in one
    context it undermines phase independence.
  - Execute/QA loops need explicit fresh-instance semantics (`dev` then `qa`,
    repeat with new instances) to preserve review integrity.
  - US-0023 validates that role switching inside one chat is not enough to
    guarantee independent review behavior. True independence requires fresh
    subagent context boundaries at each phase handoff.
- **Risks**:
  - Documentation-level enforcement can drift if future command files are added
    without the execution-model section.
  - Runtime orchestration behavior still depends on command execution discipline;
    this story hardens rules and artifacts but does not add external runtime
    enforcement code.
- **Linked**: US-0023, DEC-0007
- **Confidence**: high
- **Status**: current

## R-0002

- **Date**: 2026-02-24
- **Topic**: Manifest-driven contract governance for multi-repo compatibility
- **Query**: Registry + local manifest patterns and contract-diff propagation for
  API compatibility impact analysis
- **Sources**:
  - https://backstage.io/docs/features/software-catalog
  - https://docs.pact.io/pact_broker/can_i_deploy
  - https://github.com/oasdiff/oasdiff
- **Findings**:
  - Registry-style inventory models improve cross-system discoverability when
    paired with owner-maintained local metadata.
  - Consumer/provider contract matrices support deterministic compatibility
    decisions by linking producer changes to consumer verification context.
  - API diff tooling patterns reinforce structured "change signal" reporting
    (from/to version, breaking/additive classification, and evidence links).
  - For this project, these patterns map cleanly to workflow artifacts without
    requiring runtime orchestration claims.
- **Linked**: US-0034, US-0035, DEC-0013, DEC-0014, DEC-0015
- **Confidence**: medium
- **Status**: current

## R-0003

- **Date**: 2026-02-25
- **Topic**: Remote config contract safety and fail-fast validation patterns
- **Query**: Canonical JSON config contract and secure secret-handling guidance
  for optional remote execution
- **Sources**:
  - https://12factor.net/config
  - https://json-schema.org/learn/miscellaneous-examples.html
  - https://tour.json-schema.org/content/01-Getting-Started/04-Enumerated-Values
- **Findings**:
  - Environment variables are the preferred channel for deploy-varying and
    sensitive configuration; committed repo config should reference env vars,
    not include raw secrets.
  - A contract-first JSON approach with required fields and explicit enums gives
    deterministic validation and clearer failure modes.
  - For optional capabilities, mode-aware validation preserves low-friction
    defaults: strict checks only when the optional mode is explicitly enabled.
- **Linked**: US-0036, DEC-0016
- **Confidence**: high
- **Status**: current

## R-0004

- **Date**: 2026-02-25
- **Topic**: Deterministic workflow resume-source precedence for `/auto` continuation
- **Query**: How should a workflow orchestrator resolve start phase safely across
  explicit operator input, resume handoff artifacts, and state fallback?
- **Sources**:
  - `.cursor/commands/auto.md`
  - `.cursor/commands/resume.md`
  - `.cursor/commands/pause.md`
  - `handoffs/resume_brief.md`
  - `docs/engineering/state.md`
  - `docs/product/backlog.md` (US-0037 ACs)
- **Findings**:
  - Deterministic behavior requires strict precedence, with explicit user intent
    (`start-from`) highest to prevent hidden inference overrides.
  - `resume_brief.md` is the strongest implicit checkpoint source when no
    explicit override exists because it is purpose-built for intended resume
    phase declaration.
  - `state.md` works as fallback only with conservative inference and explicit
    ambiguity handling; permissive parsing risks phase misrouting.
  - Safe continuation requires fail-fast on stale/conflicting sources rather
    than guessing, plus structured error codes for reproducible QA.
  - Breadcrumb fields for source, resolved phase, and stop reason are necessary
    for inspectability and post-hoc debugging of automation flow.
- **Linked**: US-0037, DEC-0017
- **Confidence**: high
- **Status**: current

## R-0005

- **Date**: 2026-02-25
- **Topic**: Guarded phase-sync and deterministic release gate sequencing
- **Query**: What minimum workflow policy model enforces safe auto-sync cadence
  and no-bypass release readiness while preserving manual default behavior?
- **Sources**:
  - `docs/product/backlog.md` (US-0038 and US-0039 ACs)
  - `.cursor/commands/auto.md`
  - `.cursor/commands/execute.md`
  - `.cursor/commands/qa.md`
  - `.cursor/commands/release.md`
  - `docs/engineering/runbook.md`
  - `scripts/validate-and-push.ps1`
  - `scripts/validate-and-push.sh`
- **Findings**:
  - Existing local scripts already establish check-before-push baseline with
    tests as the critical guard; architecture should preserve this and formalize
    it as mandatory policy for any push eligibility path.
  - Safe default behavior is best preserved with non-auto sync mode
    (`manual`/`disabled`) and explicit opt-in for auto-push behavior.
  - QA-first protection for feature work is necessary to prevent early auto-push;
    before QA pass, only explicit manual sync should remain allowed.
  - Release hardening is most auditable with fixed gate order:
    check-in test evidence -> QA completion -> UAT completion -> release
    finalization.
  - Override capability should remain exception-only via explicit decision gate,
    never as default release behavior.
- **Linked**: US-0038, US-0039, DEC-0018, DEC-0019
- **Confidence**: high
- **Status**: current

## R-0006

- **Date**: 2026-02-25
- **Topic**: Immutable release-note artifacts plus queue-based release lifecycle
  tracking
- **Query**: What minimal workflow model prevents release-note overwrite while
  preserving backward compatibility and deterministic unreleased/released status?
- **Sources**:
  - `docs/product/backlog.md` (US-0040 ACs)
  - `handoffs/release_notes.md`
  - `.cursor/commands/release.md`
  - `docs/engineering/state.md`
  - `docs/engineering/architecture.md`
- **Findings**:
  - Single mutable release-note artifacts are inherently overwrite-prone and
    cannot safely represent independent sprint release history.
  - Sprint-scoped notes with canonical naming (`Sxxxx-release-notes.md`) provide
    a simple immutable history boundary with low process complexity.
  - A queue index with explicit status transitions (`planned|ready|unreleased|
    released|blocked`) is required for deterministic release visibility and
    failure handling.
  - Backward compatibility is best preserved by retaining
    `handoffs/release_notes.md` as latest-pointer summary while moving canonical
    history to `handoffs/releases/`.
  - Safe behavior under ambiguity requires fail-closed transitions and explicit
    reason codes rather than automatic destructive reconciliation.
- **Linked**: US-0040, DEC-0020
- **Confidence**: high
- **Status**: current

## R-0007

- **Date**: 2026-02-26
- **Topic**: Deterministic backlog reconciliation at release boundary
- **Query**: How should released-sprint evidence drive backlog story status/AC
  synchronization without unsafe broad mutation?
- **Sources**:
  - `docs/product/backlog.md` (US-0043 ACs)
  - `handoffs/release_queue.md`
  - `handoffs/releases/S0013-release-notes.md`
  - `sprints/S0013/release-findings.md`
  - `tests/report.md`
  - https://jfrog.com/blog/the-power-of-evidence-collection-and-release-lifecycle-management
  - https://www.tqsystems.io/blog/release-readiness-checklist
- **Findings**:
  - Evidence-first gates are more reliable than manual status edits when release
    artifacts are already canonical and deterministic.
  - Reconciliation should use strict precedence (release queue + release notes +
    QA/UAT/release-findings evidence) and remain target-sprint scoped.
  - Safe defaults require fail-closed behavior on contradictions (for example
    released sprint with OPEN story or unchecked ACs) with explicit reason code.
  - Automated reconciliation must not mutate unrelated stories; mutation scope
    should be constrained to stories linked to the target sprint.
  - Regression checks should include both stale-negative and auto-reconcile
    positive scenarios to prevent recurrence.
- **Linked**: US-0043, DEC-0021
- **Confidence**: high
- **Status**: current

## R-0008

- **Date**: 2026-02-27
- **Topic**: Multi-story auto backlog drain with bounded safety controls
- **Query**: How should `/auto` continue across multiple planned stories while
  preserving deterministic checkpoints, decision gates, and operator control?
- **Sources**:
  - https://learn.microsoft.com/en-us/agent-framework/tutorials/workflows/checkpointing-and-resuming
  - https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview
  - https://github.com/Azure/durabletask/wiki/Writing-Task-Orchestrations
  - https://cordum.io/blog/approvals-for-autonomous-workflows
  - https://agentic-patterns.com/patterns/human-in-loop-approval-framework/
- **Findings**:
  - Safe long-running orchestration patterns use deterministic checkpoints and
    replay-safe state transitions at each completed unit of work.
  - Backlog-drain automation needs bounded run controls (for example max stories
    per run / max consecutive release attempts) to prevent runaway sessions.
  - Human/decision gates should remain enforced for high-impact or ambiguous
    changes; approvals are risk controls, not disabled by default.
  - Deterministic queue selection and explicit reason codes are necessary for
    predictable continuation when one story blocks.
  - A mode switch is required so teams can choose between story-by-story auto
    behavior and full backlog-drain behavior without changing core defaults.
- **Linked**: US-0044
- **Confidence**: medium
- **Status**: current

## R-0009

- **Date**: 2026-02-26
- **Topic**: Canonical backlog status ownership and cross-artifact drift prevention
- **Query**: Should one artifact own story status and how should workflow enforce
  consistency across backlog, acceptance, and engineering state?
- **Sources**:
  - `docs/product/backlog.md`
  - `docs/product/acceptance.md`
  - `docs/engineering/state.md`
  - `.cursor/commands/release.md`
  - `.cursor/commands/auto.md`
  - https://martinfowler.com/articles/evodb.html
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/CanonicalDataModel.html
- **Findings**:
  - A single canonical source for workflow status reduces contradictory outcomes
    when multiple artifacts are edited asynchronously.
  - Derived/secondary artifacts should be reconciled from canonical state at
    deterministic boundaries instead of requiring manual parity edits.
  - Drift must fail safe with explicit reason codes and remediation, otherwise
    OPEN/DONE contradictions silently accumulate and break automation trust.
  - One-time normalization is needed when historical artifacts already diverge;
    guardrails alone do not repair existing inconsistencies.
  - `/auto` and `/sprint-plan` behavior should remain bounded and deterministic;
    canonical status ownership complements backlog-drain controls but does not
    replace planning/sizing policies.
- **Linked**: US-0045
- **Confidence**: medium
- **Status**: current

## R-0010

- **Date**: 2026-02-28
- **Topic**: Explicit bulk planning and bulk execution orchestration modes
- **Query**: How should workflow support high-autonomy multi-story delivery while
  preserving deterministic safety boundaries and fresh subagent isolation?
- **Sources**:
  - `.cursor/commands/auto.md`
  - `.cursor/commands/sprint-plan.md`
  - `docs/product/backlog.md` (`US-0023`, `US-0044`, `US-0045`)
  - https://learn.microsoft.com/en-us/agent-framework/tutorials/workflows/checkpointing-and-resuming
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/scheduler-agent-supervisor
- **Findings**:
  - Existing `/auto` already covers multi-story continuation when backlog-drain
    controls are enabled, but operator intent remains implicit in flags.
  - Teams benefit from explicit command-level modes for high-impact behavior:
    dedicated bulk planning and bulk execution reduce ambiguity.
  - Deterministic bounded controls are required for both planning and execution
    bulk modes (selection policy, max items, block/skip policy, stop reasons).
  - Fresh subagent isolation should remain mandatory at fine granularity (at
    minimum per phase and per execute/qa cycle), even in bulk mode.
  - Safe defaults should preserve current single-scope behavior unless bulk mode
    is explicitly enabled.
- **Linked**: US-0046, US-0047
- **Confidence**: medium
- **Status**: current

## R-0011

- **Date**: 2026-03-01
- **Topic**: Deterministic bulk planning with bounded batch semantics
- **Query**: Which planning patterns support explicit bulk story-to-sprint planning
  with deterministic ordering, fairness, and bounded throughput controls?
- **Sources**:
  - https://www.growingscrummasters.com/keywords/priority-queues/
  - https://github.com/ori88c/starvation-free-priority-queue
  - https://arxiv.org/html/2507.15457v1
- **Findings**:
  - Priority-queue planning is practical when ordering policy is explicit and
    stable (for this workflow: priority, then backlog order).
  - Bounded batch size is a core safety control: it prevents runaway planning
    runs and keeps output reviewable in one cycle.
  - Fairness constraints (for example starvation-aware ordering) reduce the risk
    that low-priority stories never get planned in bulk mode.
  - Batch policy trade-offs are predictable: larger batches increase throughput
    but also increase review/coordination complexity; bounded limits should be
    first-class controls.
  - For this project, deterministic selection + bounded limits + explicit stop
    reasons are the minimum contract for `/sprint-plan --bulk`.
- **Linked**: US-0046
- **Confidence**: medium
- **Status**: current

## R-0012

- **Date**: 2026-03-01
- **Topic**: Team-scoped bulk execution using lease/ownership patterns
- **Query**: Which execution-control patterns prevent duplicate work and enforce
  member-scoped task processing in concurrent bulk runs?
- **Sources**:
  - https://woodruff.dev/lease-pattern-in-net-a-lock-with-an-expiration-date-that-saves-your-data/
  - https://docs.dapr.io/developing-applications/building-blocks/distributed-lock/distributed-lock-api-overview/
  - https://www.c-sharpcorner.com/article/designing-a-distributed-job-locking-system-net-redis-sql/
- **Findings**:
  - Lease/ownership semantics are a strong fit for duplicate-work prevention:
    acquire atomically, renew while active, release or expire deterministically.
  - Expiring leases are safer than indefinite locks for long-running automation,
    because crashed/stalled workers do not hold ownership forever.
  - Ownership tokens are required so only the current owner can renew/release;
    this protects against accidental cross-member task mutation.
  - For this workflow, team context (`TEAM_MEMBER`, `ACTIVE_TASK_IDS`) should act
    as execution-scope filters before any task mutation in bulk mode.
  - When a task is out of scope or ownership cannot be validated, behavior should
    be deterministic skip/block with explicit reason code and breadcrumb output.
- **Linked**: US-0047
- **Confidence**: medium
- **Status**: current

## R-0013

- **Date**: 2026-03-01
- **Topic**: Architecture tradeoffs for explicit bulk planning/execution modes
- **Query**: What architecture constraints keep explicit bulk planning/execution
  safe, deterministic, and team-collision resistant?
- **Sources**:
  - https://en.wikipedia.org/wiki/Fair_queuing
  - https://docs.aws.amazon.com/batch/latest/userguide/fair-share-scheduling.html
  - https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/avoding-processing-duplicates-in-multiple-producer-consumer-system.html
  - https://github.com/hibiken/asynq/wiki/Unique-Tasks
- **Findings**:
  - Explicit mode activation is a key control: high-impact bulk behavior should
    require direct operator intent, not implicit default paths.
  - Fairness-aware queueing concepts strengthen deterministic planning policies by
    preventing starvation when many lower-priority stories remain open.
  - Duplicate-work prevention patterns consistently rely on ownership semantics
    plus bounded lease/visibility windows and deterministic retry/skip handling.
  - Team-safe execution requires a strict pre-mutation scope filter and explicit
    reason-code behavior when ownership/scope checks fail.
  - For this workflow, the minimal safe contract is: explicit mode, bounded run
    controls, ownership/scope checks, and auditable breadcrumbs for each item.
- **Linked**: US-0046, US-0047
- **Confidence**: medium
- **Status**: current

## R-0014

- **Date**: 2026-03-01
- **Topic**: Canonical status ownership and drift normalization guardrails
- **Query**: Which workflow contract best prevents recurring OPEN/DONE drift
  across backlog, acceptance, and engineering state while remaining auditable?
- **Sources**:
  - `docs/product/backlog.md`
  - `docs/product/acceptance.md`
  - `docs/engineering/state.md`
  - `.cursor/commands/auto.md`
  - `.cursor/commands/execute.md`
  - `.cursor/commands/sprint-plan.md`
  - `.cursor/commands/release.md`
- **Findings**:
  - Status ownership must be singular; `backlog.md` is the canonical owner for
    `OPEN|DONE` story state.
  - Derived artifacts (`acceptance.md`, `state.md`) should be reconciled from
    canonical status at deterministic boundaries (release/reconciliation), not
    edited as independent authorities.
  - Historical drift needs a one-time normalization baseline with append-only
    audit output to avoid silent rewrites.
  - Guardrails must be target-scoped and non-destructive; broad global rewrites
    are unsafe for multi-sprint projects.
  - Contradictions at boundary should fail closed with explicit reason code and
    remediation guidance.
- **Linked**: US-0045, DEC-0025
- **Confidence**: high
- **Status**: current

## R-0015

- **Date**: 2026-03-01
- **Topic**: Configurable guided intake mode with low-touch switch
- **Query**: How to provide proactive PO clarification behavior by default while
  allowing teams to disable overhead without losing baseline safety?
- **Sources**:
  - `docs/product/backlog.md` (`US-0033`)
  - `handoffs/po_to_tl.md` (US-0033 intake addendum)
  - `.cursor/commands/intake.md`
  - `.cursor/agents/po.mdc`
- **Findings**:
  - A single explicit switch is sufficient for operator intent and predictable
    intake interaction behavior.
  - Guided mode should be conditional: ask follow-up only when ambiguity blocks
    concrete acceptance criteria to avoid unnecessary friction.
  - Low-touch mode should remove proactive overhead but keep duplicate/overlap
    safety checks active.
  - Intake-time research belongs to guided mode and should be persisted with
    R-xxxx evidence for auditability.
  - Active/template parity is necessary because intake behavior is inherited from
    template guidance in newly installed repos.
- **Linked**: US-0033, DEC-0026
- **Confidence**: high
- **Status**: current

## R-0016

- **Date**: 2026-03-01
- **Topic**: Optional cross-repo compatibility observability defaults and gating
- **Query**: How can workflow track API/contract compatibility across repos with
  zero-overhead defaults and deterministic critical gate behavior?
- **Sources**:
  - `docs/product/backlog.md` (`US-0034`)
  - `docs/engineering/architecture.md` (US-0034 section)
  - `.cursor/commands/intake.md`
  - `.cursor/commands/architecture.md`
  - `.cursor/commands/execute.md`
  - `.cursor/commands/qa.md`
  - `.cursor/commands/release.md`
- **Findings**:
  - Optional mode with explicit default-off toggle is the safest baseline for
    heterogeneous projects.
  - Compatibility observability needs canonical artifacts for signals/findings so
    QA and release can verify coverage deterministically.
  - Source declarations must be explicit (`repo/module/contract/docs`) to avoid
    ambiguous monitoring scope.
  - Critical unresolved findings require release decision gating only when the
    critical-gate policy is enabled.
  - Template parity is mandatory because command/rules/docs behavior is inherited
    during installation.
- **Linked**: US-0034, DEC-0027
- **Confidence**: high
- **Status**: current

## R-0017

- **Date**: 2026-03-01
- **Topic**: Optional component-scoped execution guardrails
- **Query**: How should workflow enforce target-component-only execution while
  preserving default-off behavior and deterministic escalation for out-of-scope
  impact?
- **Sources**:
  - `docs/product/backlog.md` (`US-0035`)
  - `.cursor/commands/intake.md`
  - `.cursor/commands/architecture.md`
  - `.cursor/commands/sprint-plan.md`
  - `.cursor/commands/execute.md`
  - `.cursor/commands/qa.md`
  - `.cursor/commands/release.md`
- **Findings**:
  - Scope metadata must be explicit (`target_components`,
    `non_target_components`, `allowed_interface_touch`) when mode is enabled.
  - Planning must carry component scope into tasks to make QA verification
    deterministic.
  - Disabled mode must remain zero-overhead to avoid unnecessary ceremony in
    single-component projects.
  - Out-of-scope impact requires explicit escalation path and decision gate
    before release finalization when unresolved.
  - Scope report artifact improves auditability for unaffected-component checks.
- **Linked**: US-0035, DEC-0028
- **Confidence**: high
- **Status**: current

## R-0018

- **Date**: 2026-03-01
- **Topic**: Enforced workflow phase-isolation auditability
- **Query**: Which enforcement patterns best prevent context-reuse drift in
  multi-phase orchestrated workflows while keeping deterministic pause/resume and
  release safety?
- **Sources**:
  - `docs/product/backlog.md` (`US-0048`)
  - `handoffs/po_to_tl.md` (US-0048 addendum)
  - `docs/engineering/state.md` (checkpoint + breadcrumb patterns)
  - `.cursor/commands/auto.md`, `.cursor/commands/execute.md`, `.cursor/commands/qa.md`, `.cursor/commands/release.md`
  - OWASP — Fail Securely: https://owasp.org/www-community/Fail_securely
  - W3C — PROV-DM (provenance data model): https://www.w3.org/TR/prov-dm/
  - IETF/RFC Editor — RFC 4998 (Evidence Record Syntax / long-term integrity evidence): https://www.rfc-editor.org/rfc/rfc4998.html
  - OPA Gatekeeper docs (deny-by-default enforcementAction semantics as an analogy for fail-closed gates): https://open-policy-agent.github.io/gatekeeper/website/docs/howto/
- **Findings**:
  - Policy-only requirements are insufficient; enforcement must be **fail-closed**
    at progression boundaries (if evidence cannot be verified, do not proceed).
  - Per-phase isolation evidence must be **machine-checkable and minimal**:
    `phase_id`, `role`, `fresh_context_marker`, `timestamp`, `evidence_ref`.
  - “Fail securely” applies directly: on exception/uncertainty, treat isolation as
    **not proven** and block with deterministic diagnostics (reason code + remediation).
  - Release-path verification is an effective final control to prevent silent
    acceptance of process drift.
  - Resume checkpoints must preserve **isolation provenance** so continuation does
    not silently reuse prior context after interruption.
- **Linked**: US-0048
- **Confidence**: medium
- **Status**: current

## R-0019

- **Date**: 2026-03-01
- **Topic**: US-0048 — Enforced per-phase isolation evidence schema, fail-closed
  gates, and resume provenance
- **Query**: Workflow orchestration isolation patterns, immutable audit evidence
  schema, fail-closed gates on missing evidence, resume checkpoint provenance for
  deterministic continuation.
- **Sources**:
  - `docs/product/backlog.md` (US-0048 ACs) and `handoffs/po_to_tl.md` (US-0048 addendum)
  - `docs/engineering/state.md` (checkpoint/breadcrumb precedent)
  - `.cursor/commands/auto.md`, `.cursor/commands/execute.md`, `.cursor/commands/qa.md`, `.cursor/commands/release.md`
  - OWASP — Fail Securely: https://owasp.org/www-community/Fail_securely
  - W3C — PROV-DM (provenance data model): https://www.w3.org/TR/prov-dm/
  - IETF/RFC Editor — RFC 4998 (Evidence Record Syntax / long-term integrity evidence): https://www.rfc-editor.org/rfc/rfc4998.html
  - OPA Gatekeeper docs (deny/warn/dryrun semantics as a clear enforcement analogy): https://open-policy-agent.github.io/gatekeeper/website/docs/howto/
  - Microsoft Learn — Agent Framework workflow checkpoints: https://learn.microsoft.com/en-us/agent-framework/tutorials/workflows/checkpointing-and-resuming
- **Findings**:
  - **Phase isolation**: Enforced data isolation across execution phases with
    only explicitly passed inputs eliminates context pollution; each phase
    boundary should produce machine-checkable evidence (phase id, role,
    fresh-context marker, timestamp, evidence ref).
  - **Evidence schema**: Immutable audit trails require append-only recording,
    timestamps (ISO 8601), and stable references. Minimal schema for isolation
    evidence: `phase_id`, `role`, `fresh_context_marker`, `timestamp`,
    `evidence_ref`; optional (only if needed): `session_id`, `parent_phase`
    (resume provenance). For this repo, Git history already provides baseline
    integrity; cryptographic “tamper evidence” can remain optional unless an AC
    explicitly requires it.
  - **Fail-closed gates**: When enforcement cannot verify (e.g. missing or
    invalid isolation evidence), progression must be blocked with deterministic
    reason codes and remediation guidance; fail-closed is the secure default for
    compliance-sensitive boundaries (verify-work, release). (“Fail securely”:
    exceptions/unknowns are treated as **not authorized / not proven**.)
  - **Resume provenance**: Checkpoints should carry isolation provenance so
    continuation does not silently reuse context; deterministic resume
    requires replay-safe state and explicit start-phase + evidence refs in
    breadcrumbs.
  - **Canonical locations**: Evidence can live in phase-scoped artifacts
    (e.g. state.md sections, handoff footers, or a dedicated isolation log);
    single canonical index (e.g. in state.md or runbook) improves gate
    checkability.
- **Risks**:
  - Fail-closed at release can create operator friction if evidence writing is
    inconsistent; reason-code taxonomy and remediation steps are essential.
  - Resume provenance adds artifact surface; schema must stay minimal to avoid
    drift between written evidence and gate expectations.
- **Linked**: US-0048, R-0018
- **Confidence**: high
- **Status**: current

## R-0020

- **Date**: 2026-03-02
- **Topic**: US-0039 — Release gate tightening: deterministic order, evidence
  freshness, no-bypass contract, reason-code taxonomy, template parity
- **Query**: Deterministic release gate order, stale-evidence handling,
  no-bypass defaults and override contract, reason-code taxonomy with
  remediation guidance, and template-parity risk for release/QA/execute
  guidance.
- **Sources**:
  - Azure Pipelines deployment gates (pre/post deployment, stage sequencing):
    https://learn.microsoft.com/en-us/azure/devops/pipelines/release/approvals/gates
  - InfoQ pipeline quality gates and ordering:
    https://www.infoq.com/articles/pipeline-quality-gates/
  - Harness CI: flaky/stale test handling, quarantine, test policies:
    https://developer.harness.io/docs/continuous-integration/use-ci/run-tests/test-management/
  - GitLab approval bypass policy and audit:
    https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/approval_policies_bypass
  - SonarQube quality gates and association hierarchy:
    https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-quality-gates/
  - Fast paths to green: CI failure taxonomies and remediation:
    https://medium.com/@ThinkingLoop/fast-paths-to-green-12-ci-failure-taxonomies-532195abb366
  - Harness step failure strategy and guided failures:
    https://developer.harness.io/docs/continuous-delivery/x-platform-cd-features/executions/step-failure-strategy-settings
  - Project artifacts: `.cursor/commands/release.md`, `handoffs/po_to_tl.md`
    (US-0039 addendum), R-0005, DEC-0019
- **Findings**:
  - **Deterministic gate order**: Pre-deployment gates run before a stage;
    post-deployment gates run after completion and before the next stage.
    Fixed sequence (e.g. build → test → QA → UAT → release-note finalization)
    yields unambiguous audit trails; ordering must be documented and enforced
    so no gate is skipped or reordered implicitly (Azure Pipelines gates,
    InfoQ quality-gate sequencing).
  - **Evidence freshness and stale handling**: Stale or missing test/QA evidence
    must block release with explicit reason, not infer pass. Patterns: (1)
    require timestamp or run-id for latest evidence and define max age or
    “re-run required” policy; (2) quarantine/skip policies for flaky tests
    should not replace mandatory baseline pass; (3) remediation should point
    to re-run commands and evidence artifact locations (Harness test
    policies, Dagster freshness checks). For this workflow: gate reads
    canonical evidence artifacts (e.g. `tests/report.md`, `qa-findings.md`,
    `uat.json`); missing or stale evidence → block with deterministic code
    (e.g. `RELEASE_TEST_STALE`, `RELEASE_QA_EVIDENCE_MISSING`) and
    remediation (run TEST_COMMAND, re-run QA, complete verify-work).
  - **No-bypass defaults and override contract**: Default path must not skip
    gates. Override only via explicit decision gate: user approval, documented
    rationale (e.g. DEC-xxxx), and audit trail. GitLab and Guidewire show
    override as exception path with admin/approval; SonarQube associates one
    gate per project to avoid ambiguous bypass. For US-0039: no default
    bypass; any override requires explicit decision gate + rationale and
    optional `RELEASE_GATE_OVERRIDE_APPROVED` with DEC reference.
  - **Reason-code taxonomy and remediation**: Shared failure taxonomy improves
    MTTR (Thinking Loop CI taxonomies; Harness step failure strategy).
    Recommended codes for US-0039: `RELEASE_SPRINT_UNRESOLVED`,
    `RELEASE_TEST_FAILED`, `RELEASE_TEST_STALE`, `RELEASE_QA_EVIDENCE_MISSING`,
    `RELEASE_QA_BLOCKERS_OPEN`, `RELEASE_UAT_INCOMPLETE`, `RELEASE_UAT_FAILED`,
    `RELEASE_GATE_OVERRIDE_APPROVED` (with DEC ref). Each code must have
    documented remediation (what to fix, which artifact/command, and next
    step). Existing release command already uses RELEASE_* prefix; align
    handoff/runbook vocabulary with that set.
  - **Template parity risk**: Active and `template/` release/qa/execute
    guidance must stay behaviorally aligned so installed repos get the same
    release-safety contract. Drift between active and template causes
    inconsistent gate semantics for new installs. Mitigation: (1) list
    canonical files that must match (release.md, qa.md, execute.md,
    runbook sections, release-findings/reason-code docs); (2) include
    template-parity verification in release checklist or regression tests;
    (3) document gate order and reason codes in both active and template
    copies (Gruntwork/template drift patterns).
- **Risks**:
  - Stale-evidence thresholds (e.g. max age for test report) need a simple
    rule to avoid false blocks; prefer “evidence exists and passed” plus
    optional timestamp check rather than complex TTL.
  - Template parity is process/documentation; automated diff or checklist
    reduces but does not eliminate drift risk.
- **Linked**: US-0039, DEC-0019, R-0005
- **Confidence**: high
- **Status**: current

## R-0021

- **Date**: 2026-03-02
- **Topic**: Per-feature user guides and docs-as-code patterns
- **Query**: How to design optional, per-feature end-user guides (what it does, how to use it, limitations, troubleshooting) that integrate cleanly into a docs-as-code workflow without adding overhead when disabled.
- **Sources**:
  - https://docs.github.com/en/contributing/writing-for-github-docs/best-practices-for-github-docs
  - https://gatsbyjs.com/contributing/docs-contributions/how-to-write-a-how-to-guide
  - https://unmarkdown.com/blog/docs-as-code-2026
  - https://docs.gitscrum.com/en/best-practices/documentation-as-code/
- **Findings**:
  - Feature documentation works best when treated as code: version-controlled, reviewed, and deployed alongside the feature so behavior and docs change atomically.
  - Per-feature user guides are most helpful as short, task-focused how-to documents with a consistent schema: purpose, prerequisites, step-by-step usage, example, limitations, and troubleshooting.
  - Clear separation between conceptual docs, reference, and how-to guides avoids duplication with technical specs (e.g. Design Concept/CRS/Technical Spec) while keeping each artifact focused on a single audience.
  - Docs-as-code workflows prefer predictable, canonical locations and filenames (for example one guide per feature/story ID) plus lightweight frontmatter or metadata for linking and validation.
  - Quality and maintainability improve when user guides are part of “definition of done” for a feature and validated via simple structural checks (required sections present) instead of subjective content scoring.
- **Linked**: US-0032, US-0031
- **Confidence**: high
- **Status**: current

## R-0022

- **Date**: 2026-03-02
- **Topic**: Canonical location, naming, and workflow gates for per-feature user guides
- **Query**: How should optional per-feature user guides be organized (directory structure, naming, definition-of-done, and validation) in a docs-as-code workflow while remaining flag-controlled and low-overhead when disabled?
- **Sources**:
  - https://docs.gitscrum.com/en/best-practices/documentation-as-code/
  - https://contribute.docs.astro.build/docs-for-code-changes/new-feature-docs
  - https://www.elastic.co/docs/contribute-docs/content-types/how-tos
  - https://docs.gitlab.com/ee/development/documentation/site_architecture/folder_structure.html
  - https://docs.gitlab.com/development/documentation/feature_flags/
- **Findings**:
  - Mature docs-as-code systems typically group user-facing docs by audience and feature area (for example `doc/user/<area>/<feature>.md`) rather than by ticket alone; story IDs are better treated as metadata/frontmatter and cross-reference anchors than as the sole filename pattern.
  - Per-feature guides for new capabilities are most effective as short, task-focused how-to documents that answer "what is it, what is it used for, and how do I use it?" with concrete examples and minimal implementation detail; this aligns with US-0032’s schema (purpose, prerequisites, usage steps, example, limitations, troubleshooting).
  - Definition-of-done patterns commonly require doc updates in the *same change* as the feature code (same PR/branch) so behavior and guides deploy atomically; for an optional mode, this requirement should be gated on the user-guide flag being enabled.
  - Directory conventions favor a canonical user-docs root (for example `docs/user-guides/`) with subfolders or filenames that reflect product area plus a stable identifier; for this repo, a simple and testable option is `docs/user-guides/<story-id>.md` with optional `<area>-US-xxxx.md` variants when the product surface grows.
  - Validation is usually structural rather than semantic: automated checks assert presence of required sections/headings and basic link/format sanity; deeper content quality remains a review concern. When user-guide mode is off, these checks should be skipped entirely to preserve zero-overhead behavior.
  - Feature-flagged capabilities are documented as normal user-facing features but annotated with flag metadata (name, default state, rollout history); this suggests that US-0032 should not hard-couple guide existence to feature-flag internals, but it may support optional frontmatter fields for flag references when relevant.
- **Linked**: US-0032, US-0031
- **Confidence**: high
- **Status**: current

## R-0023

- **Date**: 2026-03-02
- **Topic**: Legacy DONE-story acceptance/traceability backfill guard and audit reporting
- **Query**: How to detect and repair backlog DONE vs acceptance/traceability drift with bounded, auditable backfill and ongoing guard; reason codes and report format.
- **Sources**:
  - `docs/product/backlog.md` (US-0045, US-0043), `docs/product/acceptance.md`
  - US-0017 and US-0030 as observed cases: DONE in backlog, unchecked in acceptance, not clearly in traceability/release artifacts
- **Findings**:
  - Canonical backlog DONE with unchecked acceptance or missing traceability is a recurring symptom when stories were completed before reconciliation/guardrails existed; one-time backfill plus ongoing guard closes the gap.
  - Deterministic normalization should be target-scoped (only stories where backlog says DONE and acceptance/traceability disagree), with explicit audit report entries (story ID, prior state, resolved state, reason code, evidence ref) and no broad destructive rewrite.
  - Reason-code vocabulary should include at least: `BACKLOG_DONE_ACCEPTANCE_UNCHECKED`, `BACKLOG_DONE_TRACEABILITY_MISSING`, `BACKLOG_DONE_RELEASE_ARTIFACT_MISSING` (or equivalent) so remediation is actionable.
  - Optional one-time backfill mode (explicit trigger) plus ongoing guard (e.g. at release/reconciliation boundaries or dedicated check command) keeps legacy repair separate from continuous prevention; template parity and regression coverage expectations should be explicit in ACs.
  - Scope stays consistent with US-0045 (canonical source, target-scoped repair) and US-0043 (release-boundary reconciliation); this story focuses on the guard/backfill procedure, audit report schema, and reason-code contract.
- **Linked**: US-0049, US-0045, US-0043
- **Confidence**: high
- **Status**: current

## R-0024

- **Date**: 2026-03-11
- **Topic**: Fresh-install hygiene, intake decomposition, and adaptive intake questioning
- **Query**: How to prevent seeded-history starter artifacts in template installs, how to split broad intake into multiple user stories, and how to adapt clarifying questions by risk/complexity.
- **Sources**:
  - https://blog.nimblepros.com/blogs/create-github-template-repo-for-boilerplate/
  - https://stackoverflow.com/questions/77198326/clone-template-repo-into-empty-repo-zero-history
  - https://agileforall.com/story-splitting/
  - https://nextagile.ai/blogs/agile/vertical-slicing-and-horizontal-slicing/
  - https://nextgenanalysts.co.uk/7-proven-techniques-for-splitting-user-stories-with-real-examples/
  - https://www.businessanalyststoolkit.com/requirements-elicitation-questions/
  - https://www.designgurus.io/answers/detail/proactive-question-asking-to-clarify-ambiguous-requirements
- **Findings**:
  - Template/starter repositories should initialize with neutral baseline artifacts and no inherited project history. New-project trust improves when starter files avoid seeded operational rows and use placeholder/default content only.
  - Cleanup behavior should be deterministic and ownership-complete; maintaining one source of truth for managed paths reduces cleanup drift across installer implementations.
  - Broad requirements are best decomposed using vertical slices and workflow-step splits so each story is testable and delivers standalone user value.
  - Decomposition quality improves when split rationale is explicit (feature axis, workflow step, risk boundary) and user-confirmed before persistence.
  - Clarifying-question strategy should consider risk and scope breadth, not only explicit ambiguity. High-impact or cross-cutting requests benefit from extra targeted questions even when initial acceptance appears concrete.
  - Questioning should stay bounded and outcome-focused; short targeted probes plus examples/edge cases reduce assumption risk without turning intake into an open-ended interview.
- **Linked**: US-0050, US-0051, US-0052
- **Confidence**: medium
- **Status**: current

## R-0025

- **Date**: 2026-03-11
- **Topic**: Architecture patterns for deterministic cleanup ownership and adaptive intake depth
- **Query**: Which technical patterns best support complete installer cleanup coverage, neutral starter templates, bounded story decomposition, and risk-aware intake questioning.
- **Sources**:
  - https://argo-cd.readthedocs.io/en/stable/user-guide/multiple_sources/
  - https://git-scm.com/docs/gitignore.html
  - https://git-scm.com/docs/git-clean.html
  - https://agileforall.com/story-splitting/
  - https://www.businessanalyststoolkit.com/requirements-elicitation-questions/
  - https://www.pmi.org/learning/library/uncover-gaps-requirements-risk-management-9910
- **Findings**:
  - Duplicate path ownership across multiple implementations is fragile; one canonical manifest/source-of-truth for managed artifacts reduces drift and keeps cleanup behavior consistent.
  - `.gitignore` controls tracking of untracked files but is not a substitute for deterministic uninstall/clean behavior for already-managed artifacts; explicit cleanup contracts are still required.
  - Safe cleanup requires a strict ownership boundary: remove only installer-owned artifacts, never non-framework project files.
  - Large requirements are better split into independently testable vertical slices/workflow steps; this supports clearer planning, faster validation, and lower risk than one large cross-cutting story.
  - Elicitation quality improves when question depth is adjusted by uncertainty/risk surface, not ambiguity alone; targeted bounded follow-ups reduce assumptions while keeping intake concise.
- **Linked**: US-0050, US-0051, US-0052, DEC-0032, DEC-0033, DEC-0034
- **Confidence**: medium
- **Status**: current

## R-0026

- **Date**: 2026-03-12
- **Topic**: Token-cost optimization patterns for artifact-first AI workflows
- **Query**: Which practical patterns reduce token usage in multi-phase AI workflows while preserving quality gates, traceability, and operator control.
- **Sources**:
  - https://arxiv.org/html/2501.14723v2
  - https://williamzujkowski.github.io/posts/from-150k-to-2k-tokens-how-progressive-context-loading-revolutionizes-llm-development-workflows/
  - https://enricopiovano.com/blog/llm-cost-optimization-caching-strategies
- **Findings**:
  - Progressive context loading (start narrow, expand only when needed) is a high-impact strategy for reducing token spend without degrading task outcomes on routine questions.
  - Separating hot operational context from historical archives keeps retrieval bounded: most runs need latest lifecycle state, not full historical logs.
  - Compact indexes with links to canonical detail files are more token-efficient than repeating full histories in every high-traffic artifact.
  - Tiered policy profiles (`lean|balanced|full`) are operator-friendly: they reduce overhead by switching defaults while preserving explicit opt-in for deeper checks.
  - Quality gates should remain invariant under cost optimization; savings should come from retrieval scope, optional-mode defaults, and loop frequency controls, not from removing release/QA/UAT safety checks.
- **Linked**: US-0053
- **Confidence**: medium
- **Status**: current

## R-0027

- **Date**: 2026-03-12
- **Topic**: Research basis for tiered token profile and compact-context policy
- **Query**: Which implementation patterns reduce token usage in artifact-first
  coding workflows while preserving deterministic quality gates and operator
  control.
- **Sources**:
  - https://platform.openai.com/docs/guides/prompt-caching
  - https://platform.claude.com/docs/en/build-with-claude/prompt-caching
  - https://arxiv.org/html/2601.16746v1
  - https://williamzujkowski.github.io/posts/from-150k-to-2k-tokens-how-progressive-context-loading-revolutionizes-llm-development-workflows/
- **Findings**:
  - Stable-prefix caching patterns support lower recurring input cost when
    repeated instructions are kept deterministic and front-loaded, which aligns
    with keeping policy contracts stable across runs.
  - Progressive retrieval (targeted read first, expand only when unresolved)
    is a practical high-impact strategy for reducing context volume versus broad
    default file loading.
  - Context pruning/compression must remain task-aware; compacting high-traffic
    artifacts is effective only when canonical links to full history stay
    available for escalation and audit.
  - Tiered operator profiles are preferable to many independent switches for
    day-to-day use, provided profile-to-flag mapping and override precedence are
    explicit and deterministic.
  - Token optimization should not remove mandatory reliability gates; savings
    should come from retrieval scope, optional-mode defaults, and loop intensity
    control while preserving QA/UAT/release chain invariants.
- **Risks**:
  - Over-compaction can hide required evidence or create stale summaries if
    archive-link contracts are weak.
  - Ambiguous profile precedence can produce non-deterministic behavior between
    profile defaults and manual overrides.
  - Excessively aggressive lean defaults can reduce analysis depth if temporary
    escalation guidance is missing.
- **Linked**: US-0053
- **Confidence**: medium
- **Status**: current

## R-0028

- **Date**: 2026-03-12
- **Topic**: Architecture tradeoffs for profile-based token optimization and compact state surfaces
- **Query**: Which architecture choices best support deterministic token-saver
  profiles and compact active-context artifacts without weakening release
  reliability.
- **Sources**:
  - https://martinfowler.com/articles/feature-toggles.html
  - https://platform.openai.com/docs/guides/prompt-caching
  - https://platform.claude.com/docs/en/build-with-claude/prompt-caching
  - https://docs.eventsourcingdb.io/best-practices/snapshots-and-performance/
- **Findings**:
  - A profile switch behaves most predictably when treated like a controlled
    feature-toggle policy: explicit mode, bounded scope, and deterministic
    precedence over derived defaults.
  - Caching-oriented token savings are strongest when the stable instruction
    prefix remains consistent; architecture should avoid unnecessary churn in
    high-reuse prompt scaffolding.
  - A snapshot-style active-context model plus archive references can keep
    operational reads fast, provided canonical links preserve full traceability.
  - Compaction should be write-safe and non-destructive: archive historical
    checkpoints, keep an active bounded context for routine reads, and escalate
    to archive only when question scope requires it.
- **Risks**:
  - Profile sprawl if mode semantics are underspecified.
  - Archive drift if active snapshots are not consistently refreshed.
  - Hidden regressions if mandatory gate invariants are not explicitly locked in
    tests.
- **Linked**: US-0053, DEC-0035
- **Confidence**: medium
- **Status**: current

## R-0029

- **Date**: 2026-03-13
- **Topic**: Configurable multi-target publishing with operator confirmation and SSH support
- **Query**: Which patterns support safe half-automatic release publishing across heterogeneous targets (registry, git, docker, cloud, custom servers/SSH) with configurable per-project behavior.
- **Sources**:
  - https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
  - https://docs.github.com/en/actions/how-tos/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment
  - https://circleci.com/docs/guides/deploy/deploy-over-ssh
  - https://octopus.com/docs/infrastructure/deployment-targets/linux/ssh-deployments
- **Findings**:
  - A safe "half-automatic" publish flow is best modeled as explicit
    operator confirmation before deployment/publish execution.
  - Project-specific release destinations vary significantly; target definitions
    should be data-driven in configuration rather than hardcoded in workflow
    logic.
  - SSH remains a common generic deployment transport and should be supported as
    a first-class configurable target with env-referenced credentials.
  - Deterministic fail-fast validation and clear per-target diagnostics prevent
    partial publish side effects on invalid config.
  - Multi-target execution should be ordered and selectable per run so teams can
    publish only a subset (for example npm-only, docker-only, or cloud-only).
- **Risks**:
  - Ambiguous target schema can cause non-deterministic or unsafe publish runs.
  - Inline credential handling can create secret leakage risk.
  - Missing confirmation boundaries can accidentally trigger irreversible publish actions.
- **Linked**: US-0054
- **Confidence**: medium
- **Status**: current

## R-0030

- **Date**: 2026-03-13
- **Topic**: Deterministic schema and safety contracts for configurable publish targets
- **Query**: Which implementation contracts provide safe, configurable, and auditable multi-target publish behavior including SSH/custom destinations.
- **Sources**:
  - https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
  - https://docs.github.com/en/actions/how-tos/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment
  - https://circleci.com/docs/guides/deploy/deploy-over-ssh
  - https://octopus.com/docs/infrastructure/deployment-targets/linux/ssh-deployments
- **Findings**:
  - Safe publish automation is strongest when release finalization and target
    publish are separate stages with explicit confirmation between them.
  - Target definitions should be strongly typed and validated before execution
    to prevent partial side effects (missing host/auth/command should fail-fast).
  - SSH target support should use env-referenced credentials and explicit
    command templates, with no inline secret literals.
  - Multi-target runs should support deterministic target ordering and explicit
    per-target enabled/disabled semantics.
  - Auditability improves when each attempted target writes structured outcome:
    selected/skipped/blocked/published with reason code and evidence ref.
- **Risks**:
  - Ambiguous target schema can create non-deterministic publish runs.
  - Missing confirmation boundary can allow unintended irreversible publishes.
  - Weak secret contract can leak credentials in committed config.
- **Linked**: US-0054
- **Confidence**: medium
- **Status**: current

## R-0031

- **Date**: 2026-03-13
- **Topic**: Deterministic status reconciliation command design
- **Query**: Which reconciliation contracts best prevent backlog/acceptance/state/resume drift while preserving canonical ownership and safe continuation.
- **Sources**:
  - docs/engineering/runbook.md (canonical status ownership + legacy drift guard)
  - .cursor/commands/release.md (target-scoped reconciliation and fail-safe reason codes)
  - .cursor/commands/memory-audit.md (read-only drift detection scope and evidence model)
  - .cursor/commands/auto.md (resume precedence and fail-fast continuation contract)
- **Findings**:
  - Reconciliation should preserve canonical ownership: backlog story status is
    source-of-truth; acceptance/state/resume are derived and should be normalized
    to canonical status in bounded target scope.
  - A dedicated repair command should be distinct from `/memory-audit`:
    `/memory-audit` detects/report-only, while reconciliation applies explicit
    deterministic writes with audit evidence.
  - Deterministic mutation boundaries are required to avoid broad historical
    rewrites: update only mismatched story blocks and linked derived rows.
  - Resume reliability improves when reconciliation also sets
    `handoffs/resume_brief.md` to next OPEN story and intended next phase with
    resolver breadcrumb metadata.
  - Blocked/conflict paths should fail closed with reason codes and remediation
    instead of partial silent correction.
- **Risks**:
  - Over-broad normalization can rewrite unrelated story history.
  - Ambiguous precedence can produce non-deterministic repairs.
  - Reconciliation without evidence logs can hide true release-state conflicts.
- **Linked**: US-0055
- **Confidence**: medium
- **Status**: current

## R-0032

- **Date**: 2026-03-14
- **Topic**: Upgrade-safe example/local config handling for scratchpad templates
- **Query**: Which config-management patterns support safe upgrades of example
  files while preserving user-local overrides and preventing missing/new option
  drift.
- **Sources**:
  - https://compose-spec.github.io/compose-spec/13-merge.html
  - https://docs.docker.com/compose/how-tos/multiple-compose-files/merge
  - Internal implementation references:
    - `installer.ps1`
    - `installer.sh`
    - `installer.py`
- **Findings**:
  - Base-plus-local-override patterns are most robust when shared defaults are
    updated independently from user-local override files.
  - Upgrade flows should treat example/default files as framework-owned and
    refresh them on upgrade, while preserving user-local files.
  - Deterministic merge/precedence behavior (base first, local overrides second)
    reduces drift where new options appear only in one surface.
  - Operator diagnostics should explicitly report when framework examples were
    refreshed and when user files intentionally remain unchanged.
- **Risks**:
  - If example/default files are not refreshed during upgrade, operators miss new
    flags and contracts.
  - If user-local files are overwritten, personal/project overrides can be lost.
  - Inconsistent installer parity across PS1/sh/py can create platform-specific
    drift.
- **Linked**: US-0057
- **Confidence**: medium
- **Status**: current

## R-0033

- **Date**: 2026-03-14
- **Topic**: Deterministic ordering policies for mutable workflow artifacts
- **Query**: Which ordering strategies best support reliable append/update
  behavior for mixed artifact types (event logs, canonical lists, derived
  checklists) without drift and oscillation.
- **Sources**:
  - https://grafana.com/blog/2024/01/04/the-concise-guide-to-loki-how-to-work-with-out-of-order-and-older-logs
  - https://grafana.com/docs/loki/latest/configure/bp-configure
  - Internal implementation references:
    - `docs/engineering/state.md`
    - `docs/product/backlog.md`
    - `docs/product/acceptance.md`
- **Findings**:
  - Event-like artifacts are most reliable with a single append direction and
    strict monotonic insertion policy.
  - Canonical enumerations (story backlogs) need deterministic sort keys to
    avoid ordering drift under multi-command mutation.
  - Derived checklist artifacts should align ordering with canonical source to
    preserve quick auditability.
  - Missing/ambiguous insertion anchors should fail safe instead of writing in
    fallback random positions.
  - Idempotent rewrite behavior is required so repeated no-op runs do not
    reshuffle blocks.
- **Risks**:
  - Enforcing ordering without migration guidance can create noisy diffs on first
    normalization.
  - Partial command adoption can keep mixed-order behavior alive.
  - Overly broad auto-sorting can accidentally rewrite unrelated narrative
    sections.
- **Linked**: US-0058
- **Confidence**: medium
- **Status**: current

## R-0034

- **Date**: 2026-03-14
- **Topic**: Strict runtime attestation patterns for phase-isolated orchestration
- **Query**: Which lightweight attestation patterns provide strong per-run
  uniqueness/freshness guarantees for orchestration boundaries while remaining
  auditable and fail-closed.
- **Sources**:
  - Internal workflow contracts:
    - `.cursor/commands/auto.md`
    - `docs/engineering/state.md`
    - `docs/engineering/decisions.md`
  - Prior isolation decision:
    - `decisions/DEC-0029.md`
- **Findings**:
  - Artifact-only evidence is necessary but insufficient for strict runtime
    proof; boundaries need a runtime-bound attestation tuple.
  - Minimal strict tuple should include:
    - `runtime_proof_id` (globally unique per phase run),
    - `orchestrator_run_id` (unique per `/auto` invocation),
    - `phase_id`,
    - `role`,
    - `proof_issued_at` (RFC3339 UTC),
    - `proof_ttl_seconds`,
    - `proof_hash` over deterministic fields.
  - Boundary validation should fail closed when:
    - tuple missing required fields,
    - `runtime_proof_id` reused across phase runs,
    - proof age exceeds TTL/freshness policy,
    - tuple cannot be deterministically linked to state checkpoint evidence.
  - Pause/resume needs strict-proof provenance pointer so resumed runs cannot
    silently continue past unverifiable boundaries.
  - Legacy runs lacking strict tuple should follow bounded compatibility guidance
    (explicit remediation path) rather than history rewrite.
- **Risks**:
  - Overly strict freshness windows can create false blocks on slower runs.
  - Weak uniqueness generation can produce accidental proof collisions.
  - Partial adoption across active/template commands can reintroduce ambiguity.
- **Linked**: US-0056
- **Confidence**: medium
- **Status**: current

## R-0035

- **Date**: 2026-03-11
- **Topic**: Intake runtime capability mismatch and self-write drift false-positive controls
- **Query**: What deterministic intake runtime pattern prevents silent
  role-subagent degradation and avoids misclassifying self-writes as external
  concurrent artifact drift.
- **Sources**:
  - Internal command contract:
    - `.cursor/commands/intake.md`
  - Internal runtime artifacts:
    - `docs/product/backlog.md`
    - `docs/product/acceptance.md`
    - `docs/engineering/state.md`
  - Reported runtime transcript evidence from first intake in fresh repo.
- **Findings**:
  - Required role-subagent capability should be validated before mutation begins;
    when unavailable, deterministic fail-fast diagnostics are safer than implicit
    in-band fallback.
  - Drift detection must include writer identity/run correlation so known
    self-generated writes are not treated as external concurrent mutation.
  - Single-writer safety is strongest with bounded lock scope across targeted
    intake artifacts plus explicit release/timeout semantics.
  - True external concurrent-writer detection should remain fail-safe and produce
    deterministic reason code + remediation guidance.
  - Ordering/ownership contracts remain compatible when guards are target-scoped
    and avoid broad rewrites.
- **Risks**:
  - Locking semantics that are too broad can create avoidable operator friction.
  - Optional fallback modes without explicit policy can reintroduce silent
    behavioral drift.
  - Incomplete template parity can cause inconsistent behavior across fresh
    repositories.
- **Linked**: US-0059
- **Confidence**: medium
- **Status**: current

## R-0036

- **Date**: 2026-03-11
- **Topic**: Deterministic state hot-surface rollover and archive trigger patterns
- **Query**: Which retention/compaction patterns support deterministic bounded
  hot-surface state files with non-destructive archive rollover and idempotent
  rerun behavior.
- **Sources**:
  - Internal policy/contracts:
    - `docs/engineering/state.md`
    - `docs/engineering/state-archive/README.md`
    - `docs/engineering/runbook.md`
  - External references:
    - https://docs.confluent.io/kafka/design/log_compaction.html
    - https://www.confluent.io/learn/kafka-retention/
- **Findings**:
  - Policy-only compaction is insufficient for bounded growth; deterministic
    rollover triggers (size/checkpoint thresholds) are required for predictable
    behavior.
  - Hybrid retention patterns (bounded hot surface + archived history) preserve
    quick current-context reads while keeping full historical evidence.
  - Idempotent compaction requires stable partitioning/naming and deterministic
    cut lines so reruns do not duplicate or reshuffle archived data.
  - Fail-safe behavior on archive-write failure is critical: block mutation and
    emit deterministic diagnostics rather than partial writes.
  - Retrieval policy should remain latest-first on hot surface with bounded
    archive expansion only when unresolved.
- **Risks**:
  - Too-small thresholds can reduce immediate troubleshooting context.
  - Non-deterministic rollover boundaries can produce archive churn.
  - Archive I/O failures without fail-safe guards can break traceability.
- **Linked**: US-0060
- **Confidence**: medium
- **Status**: current

## R-0037

- **Date**: 2026-03-15
- **Topic**: Cross-phase artifact ownership guards and deterministic archive execution controls
- **Query**: Which contract patterns prevent phase-level accidental deletion of other-phase artifact content while preserving intentional override paths, and which archive controls ensure deterministic bounded hot-surface behavior.
- **Sources**:
  - Internal command/policy artifacts:
    - `.cursor/commands/intake.md`
    - `.cursor/commands/architecture.md`
    - `.cursor/commands/refresh-context.md`
    - `docs/engineering/artifact-ordering-policy.md`
    - `docs/engineering/runbook.md`
  - Internal observed behavior:
    - user-reported architecture history deletion in fresh repo run
    - user-reported continued `state.md` growth despite rollover policy
- **Findings**:
  - Ordering policies alone are insufficient to prevent cross-phase destructive rewrites; a separate phase-ownership matrix is needed (who can mutate which artifact sections).
  - Safe default is non-destructive mutation: phase-local target updates only; unrelated section deletion/rewrite must fail closed with deterministic diagnostics.
  - Override-authorized mutation should be explicit, narrow, and auditable (phase identity, artifact scope, reason, evidence reference), not implicit.
  - `architecture.md` requires explicit history-preservation semantics because it aggregates prior story decisions and can be damaged by broad rewrite templates.
  - Archive controls must include deterministic execution evidence (partition boundary, items moved, items retained) and idempotent pack naming to avoid silent no-op drift.
  - Rollover thresholds without verifiable execution path can leave hot-surface growth effectively unbounded in practice.
- **Risks**:
  - Over-constrained ownership rules can block legitimate maintenance updates.
  - Ambiguous override boundaries can become a bypass path for destructive edits.
  - Archive verification metadata that is too verbose can reduce token savings.
- **Linked**: US-0061
- **Confidence**: medium
- **Status**: current

## R-0038

- **Date**: 2026-03-15
- **Topic**: Installer-owned metadata boundary via dedicated `its_magic/` folder
- **Query**: Which deterministic installer ownership patterns keep framework
  metadata isolated in a dedicated folder while preserving project-owned
  artifacts and backward-compatible upgrade/clean behavior.
- **Sources**:
  - Internal installer/ownership artifacts:
    - `installer.ps1`
    - `installer.sh`
    - `installer.py`
    - `bin/its-magic.js`
    - `.cursor/ownership.manifest.json`
  - Internal docs/tests:
    - `README.md`
    - `docs/engineering/runbook.md`
    - `tests/run-tests.ps1`
    - `tests/run-tests.sh`
- **Findings**:
  - A dedicated framework-owned folder boundary reduces ambiguity between
    installer metadata and project/business artifacts.
  - Deterministic migration is required for existing repos that already contain
    top-level metadata paths; idempotent reruns avoid layout churn.
  - Ownership manifest must classify `its_magic/` entries explicitly so
    install/upgrade/clean semantics stay consistent.
  - Clean behavior should only remove manifest-owned framework files and must
    not infer ownership for project artifacts outside declared scope.
  - Operator documentation must clearly distinguish framework-owned metadata
    from project-owned content (`src`, app docs, runtime files).
- **Risks**:
  - Misclassified ownership can cause accidental project-file relocation/deletion.
  - Partial migration paths can leave hybrid layouts that confuse operators.
  - Packaging/installer parity gaps can drift behavior across platforms.
- **Linked**: US-0062
- **Confidence**: medium
- **Status**: current

## R-0039

- **Date**: 2026-03-15
- **Topic**: OS-aware runbook command bootstrap with mandatory quality-gate safety
- **Query**: Which deterministic onboarding patterns auto-generate valid
  runbook commands per OS/project stack without weakening mandatory test gates.
- **Sources**:
  - Internal gate contracts and docs:
    - `docs/engineering/runbook.md`
    - `.cursor/commands/release.md`
    - `.cursor/commands/qa.md`
    - `README.md`
  - Internal installer/bootstrap surfaces:
    - `installer.ps1`
    - `installer.sh`
    - `installer.py`
    - `bin/its-magic.js`
  - User-observed mismatch:
    - Windows operator context while baseline runbook command used `sh`.
- **Findings**:
  - Mandatory baseline quality gate should remain `TEST_COMMAND`; onboarding can
    reduce friction by pre-filling valid defaults rather than relaxing gates.
  - Bootstrap should be OS-aware and shell-aware (PowerShell on Windows,
    shell/bash on Unix) for framework baseline test commands.
  - Stack-signal detection should provide best-effort concrete defaults for test
    (and optional lint/typecheck when confidently known), with deterministic
    fallback and clear remediation when unresolved.
  - Generated command probing/validation avoids committing unusable defaults and
    prevents silent placeholder drift.
  - Non-destructive precedence (`user-set > detected > fallback`) preserves
    existing repo intent while enabling new-repo automation.
- **Risks**:
  - Incorrect stack inference can generate noisy/invalid defaults.
  - Excessively strict validation can over-block uncommon but valid setups.
  - Platform parity drift across installer variants can fragment behavior.
- **Linked**: US-0063
- **Confidence**: medium
- **Status**: current

## R-0040

- **Date**: 2026-03-15
- **Topic**: Remote runtime connectivity schema + phase consumption for QA/release/publish
- **Query**: Which deterministic configuration and workflow patterns allow
  release targets to carry runtime connectivity metadata (domain/ip/port/ingress
  and Docker-over-SSH) while enabling safe remote-aware QA/release behavior and
  operator connection reporting.
- **Sources**:
  - Internal target/phase artifacts:
    - `docs/engineering/release-targets.json`
    - `.cursor/commands/release.md`
    - `.cursor/commands/qa.md`
    - `.cursor/commands/execute.md`
    - `docs/engineering/runbook.md`
  - User requirement context:
    - remote connectivity fields and Traefik/ingress possibilities
    - Docker via SSH support
    - operator-friendly connection info + canonical document output
- **Findings**:
  - Existing publish target model should be extended with deterministic
    connectivity metadata fields and type-specific validation constraints.
  - Docker-over-SSH should be represented as explicit target contract variant
    (or deterministic subtype) with env-reference-only sensitive fields.
  - Remote-aware phase behavior must be opt-in/config-driven and keep existing
    mandatory release/quality gates unchanged.
  - QA/release outputs should include connection endpoint summaries and local vs
    remote execution context while redacting secret/auth material.
  - A canonical runtime-connectivity document improves operator handoff and
    reproducibility for debug/support workflows.
- **Risks**:
  - Over-complex target schema can reduce usability for local-only repos.
  - Inadequate redaction can expose sensitive infrastructure data.
  - Remote execution ambiguity can cause accidental no-op or wrong-target checks.
- **Linked**: US-0064
- **Confidence**: medium
- **Status**: current

## R-0041

- **Date**: 2026-03-16
- **Topic**: Runtime QA autopilot for generated repos, structured test scaffolding,
  release operator run/connect hints, and mandatory intake question packs
- **Query**: Which deterministic workflow patterns enforce real runtime
  validation (startup/connectivity/log/debug), language-aware baseline test
  generation, operator-ready release run/connect guidance, and intake
  questionnaire coverage before persistence.
- **Sources**:
  - Cursor Browser tools:
    https://cursor.com/docs/agent/tools/browser
  - Cursor Debug Mode:
    https://cursor.com/docs/agent/debug-mode
  - Internal workflow contracts:
    - `.cursor/commands/execute.md`
    - `.cursor/commands/qa.md`
    - `.cursor/commands/release.md`
    - `.cursor/commands/intake.md`
    - `.cursor/agents/dev.mdc`
    - `.cursor/agents/qa.mdc`
- **Findings**:
  - Generated-project quality confidence requires mandatory runtime validation,
    not only static/test-command checks. Minimal deterministic chain:
    startup attempt -> health/connectivity check -> log/error scan ->
    bounded self-debug retries -> explicit verdict.
  - Browser-level verification is a practical, automatable path for webapp
    runtime checks (UI path validation + console/network evidence), and should
    be integrated where project type indicates browser surface.
  - Debug-mode workflow provides a bounded escalation path for reproducible
    runtime failures: hypothesis/instrumentation/reproduction/evidence-based fix,
    followed by cleanup.
  - Baseline test scaffolding should be stack-aware and non-destructive:
    generate when missing, preserve explicit user tests/commands, and wire
    deterministic `TEST_COMMAND` evidence into QA/release gates.
  - Release artifacts should include a strict operator-facing
    `Run/Connect/Verify` section so users can immediately start and validate
    shipped software without guesswork.
  - Intake reliability improves when required topic coverage is explicit:
    first-intake comprehensive pack and small-intake minimal pack, with bounded
    assumptions requiring user confirmation before persistence.
- **Risks**:
  - Over-broad runtime retries can mask deeper design issues if bounds/reason
    codes are weak.
  - Stack detection errors can generate unusable starter tests if fallback rules
    are underspecified.
  - Mandatory intake packs can increase friction if low-touch compatibility is
    not preserved with deterministic minimum gates.
- **Linked**: US-0065, US-0066, US-0067, US-0068
- **Confidence**: high
- **Status**: current

## R-0042

- **Date**: 2026-03-16
- **Topic**: US-0065 runtime QA autopilot contract refinements (startup/readiness, bounded retries, runtime log severity evidence)
- **Query**: Which concrete runtime-validation patterns should be mandated for generated-project QA so PASS requires real startup and reachability proof, bounded retry behavior, and structured error/log evidence.
- **Sources**:
  - https://playwright.dev/docs/test-webserver
  - https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
  - https://opentelemetry.io/docs/specs/otel/logs/data-model/
- **Findings**:
  - Runtime readiness should be endpoint-driven with explicit startup timeout and accepted health-response semantics; this aligns with deterministic startup -> readiness proof in QA evidence.
  - Retry policy must be bounded and selective: retry only transient startup/connectivity failures, cap attempts, and use backoff to avoid retry storms; persistent failures must fail closed with explicit reason code.
  - Runtime log analysis should carry normalized severity evidence and explicit error thresholds (ERROR/FATAL boundaries) so PASS cannot ignore critical runtime signals.
  - QA evidence for US-0065 should minimally include startup command, readiness endpoint/result, retry ledger (attempts and delays), and log severity summary for reproducibility.
  - Webapp runtime checks should include browser-surface verification when applicable, but remain under US-0065 scope as runtime truth validation (not release-hint or test-scaffold scope).
- **Risks**:
  - Overly strict startup timeouts can create false negatives for slower stacks.
  - Broad retry scope can hide non-transient defects and extend failing runs.
  - Log-severity mapping drift across stacks can cause inconsistent PASS/FAIL unless thresholds are explicit.
- **Linked**: US-0065, R-0041
- **Confidence**: high
- **Status**: current

## R-0043

- **Date**: 2026-03-16
- **Topic**: US-0066 generated baseline test scaffolding contract (stack-aware templates, non-destructive reruns, deterministic auto-run linkage)
- **Query**: Which concrete cross-stack test-scaffold and execution conventions should drive deterministic baseline generation for new app repos while preserving existing user tests/commands and enforcing automatic QA execution evidence.
- **Sources**:
  - https://jestjs.io/docs/next/getting-started
  - https://docs.pytest.org/en/7.4.x/getting-started.html
  - https://pkg.go.dev/testing
  - https://maven.apache.org/surefire/maven-surefire-plugin/examples/inclusion-exclusion.html
  - https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-csharp-with-xunit
  - `docs/product/backlog.md` (`US-0066` ACs and boundaries)
  - `handoffs/po_to_tl.md` (US-0066 discovery addendum)
- **Findings**:
  - Baseline scaffold generation should follow ecosystem-native discovery conventions so generated tests are runnable immediately by default (`test_*.py`/`*_test.py` for pytest, `*_test.go` for Go, Surefire include patterns for Java, `dotnet new xunit` + `dotnet test` for .NET, and standard Jest bootstrap for Node).
  - Deterministic stack profiles should map to one minimal baseline `TEST_COMMAND` per detected stack, with explicit fail-closed diagnostics when no supported profile resolves; unresolved detection must not silently skip scaffold generation.
  - Non-destructive behavior is mandatory: create only missing baseline artifacts, never overwrite existing user-authored tests/config by default, and use deterministic precedence (`user-authored existing assets` > `generated baseline missing assets`).
  - Idempotent reruns require stable path conventions and explicit generated-path evidence so repeated `/execute` runs do not create duplicate test files or oscillating command/config rewrites.
  - `/qa` should treat generated baseline tests as mandatory execution evidence (pass/fail + command + output reference), but story scope remains test scaffolding and auto-run contract only; runtime startup/connectivity verdict remains governed by `US-0065`.
- **Risks**:
  - Over-eager detection can generate scaffolds for the wrong stack in polyglot repos unless profile-selection precedence is explicit.
  - Non-destructive merge rules that are too weak can still clobber existing project test layout or command intent.
  - Rigid single-command defaults can miss repo-specific test runners unless remediation/fallback diagnostics are actionable.
- **Linked**: US-0066, R-0041
- **Confidence**: high
- **Status**: current

## R-0044

- **Date**: 2026-03-16
- **Topic**: US-0067 release operator Run/Connect/Verify hints contract hardening
- **Query**: Which release-artifact schema and validation patterns ensure
  deterministic operator-ready `Run/Connect/Verify` guidance with fail-closed
  behavior on missing or ambiguous fields, while preserving `US-0067`-only scope.
- **Sources**:
  - `docs/product/backlog.md` (`US-0067` discovery refinements and acceptance)
  - `handoffs/po_to_tl.md` (Discovery Addendum — `US-0067`)
  - `docs/engineering/runtime-connectivity.md`
  - `handoffs/releases/S0045-release-notes.md`
  - `handoffs/release_notes.md`
  - `.cursor/commands/release.md`
- **Findings**:
  - A deterministic fixed-order operator section (`Run -> Connect -> Verify ->
    Credentials(env-ref only) -> Known Issues`) is necessary to keep release
    reruns idempotent and operator-readable.
  - Required fields should be schema-validated at release finalization with
    fail-closed behavior; missing or ambiguous values must block completion with
    deterministic reason code + remediation guidance.
  - Credentials guidance must remain env-reference-only (variable names and
    source location), with explicit prohibition of inline secrets in release
    artifacts.
  - Runtime context must be explicit (`local|remote`) and, when available,
    endpoint/connectivity claims should align with
    `docs/engineering/runtime-connectivity.md`.
  - Canonical sprint release notes should carry full operator details, while
    `handoffs/release_notes.md` should remain a concise latest-pointer summary
    that links to canonical per-sprint notes.
- **Risks**:
  - Overly permissive validation can allow nominal "PASS" release output that is
    not operationally actionable.
  - Inconsistent active/template guidance may reintroduce drift in required
    operator sections for fresh installs.
  - Ambiguous local/remote endpoint reporting can create incorrect operator
    runbook steps even when release gates pass.
- **Linked**: US-0067, R-0041
- **Confidence**: high
- **Status**: current

## R-0045

- **Date**: 2026-03-17
- **Topic**: US-0068 mandatory intake question-pack enforcement and coverage evidence contract
- **Query**: Which deterministic intake questionnaire patterns enforce required coverage for first and small intakes, block persistence on missing critical answers, and preserve low-touch compatibility with auditable evidence.
- **Sources**:
  - `docs/product/backlog.md` (`US-0068` discovery refinements and acceptance)
  - `handoffs/po_to_tl.md` (Discovery Addendum - `US-0068`)
  - `.cursor/commands/intake.md`
  - `.cursor/agents/po.mdc`
  - https://www.atlassian.com/agile/project-management/user-stories
  - https://www.productplan.com/glossary/user-story/
- **Findings**:
  - Intake quality is more reliable when question coverage is explicit and machine-verifiable; topic IDs plus required/optional classification are needed for deterministic checks.
  - First-intake and small-intake packs should remain distinct to keep high-signal collection without forcing full questionnaires on low-scope follow-up requests.
  - Persistence gating must fail closed when required coverage is missing, with deterministic reason codes and remediation guidance before any backlog/acceptance write.
  - Bounded assumptions are a safe compatibility path only when user confirmation is explicit and persisted as structured evidence.
  - Low-touch mode can remain available if critical safety topics are still mandatory and recorded (`asked_topics`, `missing_topics`, `assumptions_confirmed`).
- **Risks**:
  - Overly broad required packs can increase intake friction and encourage low-quality responses.
  - Weak topic taxonomy can create false "coverage complete" outcomes that miss critical requirements.
  - Inconsistent active/template command guidance can reintroduce intake-policy drift in fresh installs.
- **Linked**: US-0068, R-0041
- **Confidence**: high
- **Status**: current

## R-0046

- **Date**: 2026-03-17 (extended 2026-03-21)
- **Topic**: US-0071 user-visible internal metadata sanitization guard
- **Query**: Which deterministic policy/check patterns prevent internal planning identifiers from leaking into user-visible software surfaces while keeping internal docs/comments usable.
- **Sources**:
  - `docs/product/backlog.md` (`US-0071` intake, discovery refinements, AC-1..AC-10)
  - `docs/product/vision.md` (Discovery Notes — `US-0071`)
  - `handoffs/po_to_tl.md` (Discovery Addendum — `US-0071`)
  - `https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html`
  - `https://owasp.org/www-community/Improper_Error_Handling`
  - `https://cwe.mitre.org/data/definitions/200.html`
  - `https://cwe.mitre.org/data/definitions/209.html`
- **Findings**:
  - User-facing output should be treated as a sanitized surface; internal implementation and planning identifiers must not be emitted to end users by default.
  - Deterministic allowlist/denylist policy is needed to avoid ambiguous enforcement: deny planning-token patterns in user-visible surfaces, allow internal docs and code comments.
  - Enforcement should be automated in execute and qa with fail-closed behavior and evidence refs, not manual review only.
  - Diagnostics should be specific and actionable (detected token class, evidence path/context, safe-remediation guidance), consistent with secure error-handling principles.
  - Regression checks should explicitly validate both negative paths (leak detection) and allowlist behavior (no false blocks for docs/comments).
  - **Post-discovery scope (2026-03-21)**: “User-visible” means operator/end-user **software outputs** (CLI stdout/stderr, UI copy, thrown/propagated error strings, installer-visible text). **Out of scope for the guard**: internal `docs/**`, `.cursor/**`, sprint/handoff/decision artifacts, and **code comments**—these remain valid homes for `US|DEC|R` planning IDs.
  - **Minimum forbidden patterns (AC-1)**: treat `US-[0-9]{4}`, `DEC-[0-9]{4}`, and `R-[0-9]{4}` as the baseline deny set in disallowed channels; tune matching to planning-shaped tokens to limit accidental hits on unrelated strings.
  - **Reason-code contract (AC-6)**: document a small deterministic vocabulary (for example `USER_VISIBLE_INTERNAL_METADATA_DETECTED`, `METADATA_SANITIZATION_POLICY_MISSING`) and require the same codes in execute/QA/release evidence for traceability.
  - **Release/readiness (AC-10)**: readiness artifacts should attest that sanitization checks **ran and passed** (not merely that policy text exists).
  - **Parity (AC-8)**: policy-bearing command/rule/runbook/README guidance must stay aligned in **active** vs **template** install trees so fresh installs inherit the same guard semantics.
- **Risks**:
  - Overbroad pattern matching can cause false positives and developer friction.
  - Narrow matching can miss nonstandard planning markers and allow leakage.
  - Inconsistent active/template policy surfaces can reintroduce drift for new installs.
  - Channel misclassification (treating internal docs as “user-visible” or vice versa) can produce false failures or missed leaks.
- **Linked**: US-0071
- **Confidence**: high
- **Status**: current

## R-0047

- **Date**: 2026-03-17 (extended 2026-03-22)
- **Topic**: US-0072 deterministic context slimming and archive enforcement across core artifacts
- **Query**: Which deterministic execution patterns enforce archive rollover for hot artifacts and minimize subagent context load without losing auditable historical evidence.
- **Sources**:
  - `docs/product/backlog.md` (`US-0053`, `US-0060`, `US-0061`, `US-0072`)
  - `docs/engineering/state.md` (current hot-surface growth and latest checkpoints)
  - `docs/engineering/state-archive/README.md`
  - `https://fivenines.io/blog/logrotate-the-complete-guide/`
  - `https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html`
- **Findings**:
  - Archive strategy must be enforced as an execution gate, not documentation only; when thresholds are exceeded, rollover or fail-closed should occur in the same boundary.
  - Deterministic verification evidence (`boundary`, `moved`, `retained`, `pack_ref`) is required to make archive behavior auditable and avoid silent no-op rollover paths.
  - High-growth artifact strategy should separate hot summaries from historical archive packs to preserve fast, low-noise reads while retaining full evidence.
  - Subagent quality improves when phase reads are bounded and retrieval expands only when unresolved; this reduces irrelevant-context hallucination risk.
  - Idempotent archive pack naming/partitioning is essential to prevent duplicate or oscillating archive churn on reruns.
  - **Post-discovery (2026-03-22) — scope triad + policy binding**: Canonical hot/archive enforcement targets for US-0072 are `docs/engineering/state.md`, `handoffs/po_to_tl.md`, and `docs/engineering/architecture.md`; additional `handoffs/*` compaction requires explicit architecture justification. Thresholds for `state.md` should continue to resolve from merged scratchpad (`STATE_HOT_MAX_LINES`, `STATE_HOT_MAX_CHECKPOINTS` per `.cursor/scratchpad.md` + `.cursor/scratchpad.local.md`); parallel scratchpad keys (or documented derived defaults) should be introduced for `po_to_tl` and `architecture` surfaces so caps are operator-configurable and auditable, not hardcoded only in prose.
  - **Post-discovery — phase×artifact mutation ownership**: Rollover/compaction must run in the same phase that would otherwise leave an oversized hot surface, or fail closed: `refresh-context` / curator path remains the natural owner for `state.md` hot rollover (already evidenced in `state.md` checkpoints); `po_to_tl.md` growth is driven by PO intake/discovery handoffs — those phases (or a single designated PO-boundary command) must own pre-completion archive/split checks when that file exceeds policy; `architecture.md` mutations are tech-lead/architecture-phase owned — that boundary should enforce append-only history rules (per `R-0037` / `US-0061`) plus optional hot-summary front-matter or sibling compact index when size thresholds breach.
  - **Post-discovery — minimal-read + AC-6 compact pointers**: Per-phase default read sets should name only canonical inputs for that command (for example backlog slice + prior phase handoff + one engineering index), with explicit numeric line/file budgets and an escalation path (“expand to archive pack X only when question unresolved”). Compact phase-context artifacts can be thin “latest pointer” blocks in hot headers or `docs/engineering/*-context.md` siblings that link to archive packs and sprint IDs without duplicating full checkpoint bodies.
  - **Post-discovery — reason codes + regression hooks (AC-7/AC-10)**: Align taxonomy with backlog examples (`STATE_ARCHIVE_REQUIRED`, `CONTEXT_BUDGET_EXCEEDED`, `ARTIFACT_HOT_SURFACE_OVERSIZE`, `STATE_ARCHIVE_VERIFICATION_FAILED`) and add fail-closed codes for “threshold exceeded but no `pack_ref` written”. Regression tests should assert: synthetic oversize hot file triggers rollover or deterministic stop; empty archive when rollover required; idempotent second run does not duplicate packs; bounded-read policy violations emit expected codes — mirroring patterns in `R-0033` (ordering), `R-0036` (rollover triggers), and `R-0037` (ownership + archive verification).
- **Risks**:
  - Over-aggressive compaction can hide needed context if archive pointers are weak.
  - Weak enforcement can leave thresholds breached indefinitely while claiming policy compliance.
  - Non-deterministic pack boundaries can break traceability and increase operator confusion.
  - Splitting ownership across three hot files increases the chance one path forgets enforcement unless each mutating command documents a mandatory pre-completion gate.
- **Linked**: US-0072, US-0060, US-0061, R-0033, R-0036, R-0037
- **Confidence**: medium-high
- **Status**: current

## R-0048

- **Date**: 2026-03-20
- **Topic**: US-0069 strict phase role enforcement and preflight capability
  resolution for `/auto` orchestration
- **Query**: Which deterministic workflow patterns enforce a single resolved role
  per phase boundary, fail closed when the required capability is missing, and
  keep isolation evidence aligned with strict runtime attestation (no silent
  role substitution).
- **Sources**:
  - `docs/product/backlog.md` (`US-0069` acceptance and discovery refinements)
  - `docs/product/vision.md` (Discovery Notes — `US-0069`)
  - `.cursor/commands/auto.md` (orchestration model, isolation + strict-proof
    contracts)
  - `handoffs/po_to_tl.md` (Discovery Addendum — `US-0069`)
  - `docs/engineering/research.md` (`R-0001` subagent isolation baseline)
  - https://open-policy-agent.github.io/gatekeeper/website/docs/failing-closed/
  - https://dev.to/uu/pre-action-authorization-the-missing-security-layer-for-ai-agents-3l0p
- **Findings**:
  - **Preflight over post-hoc**: Admission-style systems treat “cannot evaluate
    policy” as deny when configured to fail closed; the same principle maps to
    `/auto` as **resolve required role/capability before spawning phase work**,
    not only validating artifacts afterward.
  - **Single-valued role at the boundary**: When a phase allows alternates
    (`research`, `plan-verify`, `refresh-context`), a documented precedence
    order (for example scratchpad policy keys) must yield exactly one expected
    role for that run so diagnostics, isolation `role`, and strict-proof
    `role` stay aligned.
  - **Default deny for high-risk phases**: `execute` mapped to `dev` with
    explicit override-only exceptions matches least-privilege and separation-of-
    duties patterns; implicit fallback to `tech-lead` (or any unrelated role)
    undermines review integrity already described in `R-0001`.
  - **Evidence consistency**: Isolation evidence (`phase_id`, `role`, marker)
    and strict runtime proof tuples must reference the **same resolved
    canonical role**; mismatch should fail closed per backlog discovery
    refinements.
  - **Resume/start-from parity**: Continuation paths must rerun the same
    preflight; stale resume artifacts cannot bypass capability checks without
    creating a silent downgrade of enforcement.
  - **Operator actionability**: Blockers should emit deterministic reason codes
    (vocabulary per AC-9), plus `phase_id`, expected vs observed role/capability,
    and remediation (spawn correct role, fix policy, or document override).
- **Risks**:
  - Over-strict policy without escape hatches can block legitimate constrained
    environments unless override contracts are rare, explicit, and audited.
  - Alternate-role precedence that is hard to discover increases misconfiguration
    and false “capability missing” stops.
  - Documentation-only enforcement still depends on human/tool discipline;
    regression tests (AC-8) are needed to prevent drift in command templates.
- **Linked**: US-0069, US-0048, US-0056, DEC-0029, DEC-0038, R-0001
- **Confidence**: high
- **Status**: current

## R-0049

- **Date**: 2026-03-21
- **Topic**: US-0070 scratchpad-controlled `/auto` phase selection policy
  (precedence, non-skippable gates, profiles, and `US-0069` compatibility)
- **Query**: How should operators configure a resolved ordered phase subset
  without silent safety bypass, conflicting policy modes, or role/capability
  substitution when phases are omitted from the plan?
- **Sources**:
  - `docs/product/backlog.md` (`US-0070` discovery refinements and ACs)
  - `docs/product/vision.md` (Discovery Notes — `US-0070`)
  - `.cursor/commands/auto.md` (canonical phase order, isolation + strict-proof
    boundaries, `start-from`, backlog-drain, bulk execute, team scope)
  - `docs/engineering/research.md` (`R-0004` resume precedence, `R-0048`
    preflight role enforcement)
  - `handoffs/po_to_tl.md` (Discovery Addendum — `US-0070`)
- **Findings**:
  - **Single active policy mode (fail-closed on conflict)**: At most one of
    `AUTO_PHASE_PLAN=full` (default), `AUTO_PHASE_EXCLUDE=<csv>`,
    `AUTO_PHASE_INCLUDE=<csv>`, or `AUTO_PHASE_PROFILE=<name>` may be active;
    if two or more non-default selectors are set simultaneously, resolve with
    a deterministic `PHASE_POLICY_CONFLICT` (or equivalent) and **no** plan
    materialization.
  - **Precedence matrix (evaluation order when implementing)**:
    1. Parse scratchpad + `scratchpad.local` merge (template parity on install).
    2. Detect policy mode; on conflict, stop (above).
    3. Expand mode to a **candidate** ordered list:
       - `full`: canonical lifecycle order (`intake` → `refresh-context`, plus
         documented optional inserts such as `/security-review` when enabled).
       - `exclude`: `full` minus excluded ids (validate tokens).
       - `include`: only listed ids, **re-sorted** into canonical order (reject
         unknown ids; reject empty result).
       - `profile`: expand named profile to an include/exclude or ordered
         subset per profile registry (unknown profile → fail closed).
    4. Apply **non-skippable reinstatement** (default profile): reinsert any
       phase in the **default non-skippable set** that was removed, with reason
       `non_skippable_gate` in breadcrumbs (unless operator selected a named
       **high-risk profile** that documents explicit exceptions and required
       acknowledgment fields — then reinstatement rules come from the profile
       spec, not the default set).
    5. Intersect with `start-from=<phase>`: keep phases from the requested
       anchor forward **that remain** in the plan; empty intersection → fail
       closed with diagnostics (`resolved_plan` vs `requested_start`).
    6. Persist resolved plan + skipped-phase reasons to continuation
       breadcrumbs **before** first spawn (per backlog discovery).
  - **Default non-skippable phase set (baseline recommendation)**:
    - **Safety gates**: `qa`, `verify-work`, `release` — always reinstate in
      default profile; aligns with AC-4 and existing sync/release contracts.
    - **Evidence-chain integrity**: any phase whose skip would leave a later
      phase without a valid prior isolation + strict-proof checkpoint for the
      same story/run should be treated as non-skippable in default profile
      (typically the full upstream chain for active implementation loops); exact
      minimal subgraph can be tightened in architecture but **must not** silently
      drop required tuples.
  - **Named profile sketch (`profile_high_risk_dev_fast` — illustrative only)**:
    - Declared intent: accelerate early phases for trusted sandboxes only.
    - Documented exceptions: may allow omitting selected upstream phases **only**
      when paired with explicit operator acknowledgment fields (for example
      `AUTO_PHASE_HIGH_RISK_ACK=<token>` + profile version ref).
    - Must still emit deterministic **skipped** reasons and must **not** mark
      downstream gates as passed without their checkpoints.
  - **`US-0069` compatibility (no role substitution via skipping)**:
    - Role resolution applies **per phase that remains in the resolved plan**
      only; skipping `research` does **not** reassign `architecture` to `po`.
    - Preflight capability gate runs before each spawn for planned phases; a
      skipped phase imposes **no** spawn and **no** alternate-role fallback for
      a different phase.
    - Resume/backlog-drain/bulk/team paths must reload the same phase-policy
      inputs and recompute the plan; stale plans cannot revive skipped phases
      silently.
  - **Failure taxonomy (operator-actionable)**: reserve deterministic codes for
    unknown phase token, empty plan after include, policy conflict, invalid
    profile, `start-from` empty intersection, and reinstatement diagnostics —
    aligned with backlog “invalid-token fail-fast codes” requirement.
- **Risks**:
  - Overly permissive profiles could reintroduce silent gate bypass if
    acknowledgment and evidence rules are weak.
  - `include` mode can accidentally construct sparse plans that break evidence
    chains unless architecture defines minimal mandatory subgraphs explicitly.
  - Documentation-only policy remains dependent on command implementation and
    tests (AC-9) to prevent drift across active vs template installs.
- **Linked**: US-0070, US-0069, DEC-0051, R-0004, R-0048
- **Confidence**: high
- **Status**: current

## R-0050

- **Date**: 2026-03-23
- **Topic**: US-0073 scratchpad delivery simplification (example-only install policy)
- **Query**: How to simplify delivered scratchpad artifacts while preserving
  deterministic merged resolution for `/auto` and phase commands, fail-closed
  missing-key behavior, upgrade parity, and explicit ownership per `DEC-0039` /
  `US-0057`.
- **Sources**:
  - `docs/product/backlog.md` (`US-0018`, `US-0057`, `US-0073`)
  - `docs/product/vision.md` (Discovery Notes — `US-0073`)
  - `handoffs/po_to_tl.md` (Discovery Addendum — `US-0073`)
  - `decisions/DEC-0039.md` (example refresh + ownership)
  - `README.md` (upgrade + scratchpad ownership behavior)
  - `docs/engineering/research.md` (`R-0049` merged scratchpad reload semantics for
    `/auto` phase plans — config loaders must stay consistent with “recompute
    from merged bytes” expectations)
  - `https://12factor.net/config`
  - `https://stackoverflow.com/questions/6009/how-do-you-deal-with-configuration-files-in-source-control`
- **Findings**:
  - **Two delivery models (architecture must pick one)**:
    - **Model A — committed baseline**: ship/maintain `.cursor/scratchpad.md` as
      the framework baseline plus `.cursor/scratchpad.local.example.md` (current
      shape); lowest surprise for commands that open `scratchpad.md` directly.
    - **Model B — example-only**: ship **only** the example (and docs); any
      effective baseline must be **materialized** deterministically (install step,
      first-run copy, or explicit generator) so merged reads still resolve every
      required automation key — **never** infer missing keys silently (`US-0073`
      `AC-2`, `AC-4`).
  - **Canonical merged precedence (recommended for implementation)** — apply
    after both files are loaded as key/value sets (exact merge mechanics in
    architecture; order is the invariant):
    1. **`.cursor/scratchpad.local.md`** (user-owned) overrides framework keys
       where present; must never be deleted or overwritten by install/upgrade
       (`US-0018`, `DEC-0039`).
    2. **Repo `.cursor/scratchpad.md`** when Model A is selected, **or** the
       **materialized baseline** produced under Model B (must be stable and
       auditable — same bytes as would have been committed, or a documented
       generated equivalent).
    3. **`.cursor/scratchpad.local.example.md`** (framework-owned, refreshable on
       upgrade per `DEC-0039`) supplies defaults only for keys not set above.
    4. If a **required** key is still absent or invalid after merge → **fail
       closed** with diagnostics naming the layer(s) checked (local, baseline /
       materialized, example) and remediation (`US-0073` `AC-4`).
  - **Upgrade / legacy migration**:
    - Repos with **both** historical files need a deterministic rule: either
      retain committed `scratchpad.md` under Model A, or migrate to Model B by
      documenting what happens to an existing committed baseline (preserve user
      edits vs replace with materialized template) — ambiguity is a defect.
    - `--mode upgrade` must apply the chosen delivery policy while preserving
      `.cursor/scratchpad.local.md` and refreshing only framework-owned example
      content (`US-0073` discovery addendum; `DEC-0039`).
  - **Parity**: `installer.ps1`, `installer.sh`, `installer.py`, CLI, and
    `template/` copies must implement the **same** policy and merge semantics
    (`US-0073` `AC-6`, `AC-8`).
  - **Regression matrix** (minimum): fresh install, upgrade from dual-file
    legacy, missing baseline / missing materialization, local-only override;
    each failure mode should emit deterministic reason codes, not silent
    defaults (`US-0073` `AC-9`, `AC-10`).
- **Risks**:
  - Example-only delivery may cause missing-default behavior if command loaders
    still assume `scratchpad.md` exists on disk without a materialization step.
  - Migration inconsistency across installer implementations creates
    cross-platform drift.
  - Ambiguous precedence between generated defaults and local overrides produces
    non-deterministic `/auto` behavior — prevented only by documenting and
    testing the merge order above.
- **Linked**: US-0073, US-0018, US-0057, DEC-0039
- **Confidence**: high
- **Status**: current

## R-0051

- **Date**: 2026-03-22
- **Topic**: US-0074 baseline regression cleanup for remaining failing checks
- **Query**: Which deterministic remediation patterns can restore full baseline check health for Homebrew/npm version sync and installer/CLI `TEST_COMMAND` bootstrap failures.
- **Sources**:
  - `sprints/S0050/qa-findings.md` (current failing-check list)
  - `docs/product/backlog.md` (`US-0063`, `US-0018`, `US-0057`, `US-0074`)
  - `https://docs.brew.sh/Formula-Cookbook`
  - `https://docs.npmjs.com/about-semantic-versioning`
- **Findings**:
  - Baseline check closure needs explicit source-of-truth precedence for version values (npm package version as canonical) to keep Homebrew URL/version assertions deterministic.
  - Installer bootstrap failures should be treated as contract regressions: stack detection + command generation path must be validated for both installer and CLI entry paths.
  - Fixes must avoid masking checks; acceptance should require formerly failing checks to pass explicitly in QA evidence.
  - Cross-platform installer parity is essential to avoid one-path green and another path red behavior.
- **Risks**:
  - Patch-only fixes to one artifact (for example formula only) may leave upstream source/version derivation inconsistent.
  - Platform-specific bootstrap assumptions can reintroduce failures on different shells/environments.
  - Regression assertions can become flaky if test fixtures do not pin deterministic inputs.
- **Linked**: US-0074, US-0063, US-0018, US-0057
- **Confidence**: medium-high
- **Status**: current

### Post-discovery findings (2026-03-24) — US-0074

- **Evidence anchors**: `sprints/S0051/qa-findings.md` (four-check classification at QA time),
  `tests/run-tests.ps1` / `tests/run-tests.sh` (exact assert strings), current
  `tests/report.md` (re-run baseline; operator should re-execute tests for story AC-7).
- **npm vs Homebrew (root cause — version drift)**:
  - **Canonical version**: `package.json` `version` is the single source of truth for baseline
    sync checks.
  - **Assert contract**: tests require `packaging/homebrew/its-magic.rb` to contain the
    literal tarball segment `v{package.json.version}.tar.gz` and a Ruby `version
    "{package.json.version}"` line (see `# 4b) Homebrew stable formula version sync` in
    `tests/run-tests.ps1` / `tests/run-tests.sh`).
  - **Failure mode**: `package.json` / npm release tag bumped without updating the committed
    formula `url`, `version`, and (for real brew use) `sha256` — asserts fail even when the
    product is otherwise healthy. Release automation (`scripts/release-all*.ps1`, npm
    `release:brew-only`, etc.) should be treated as the operational backstop so the formula
    cannot lag npm.
- **TEST_COMMAND bootstrap (root cause — contract vs detector output)**:
  - **Owning surfaces**: `installer.ps1` / `installer.sh` / `installer.py`
    (`Get-DetectedRunbookDefaults` / `detect_runbook_defaults` + `Invoke-RunbookBootstrap` /
    `bootstrap_runbook_commands`), delegated CLI entry `bin/its-magic.js` (spawns PS1 or SH
    installer), installed file `docs/engineering/runbook.md` (from `template/` tree), narrative
    contract in `docs/engineering/runbook.md` (active) + template mirror.
  - **Baseline test contract**: installer and CLI missing-install scenarios assert the
    materialized runbook’s `TEST_COMMAND` line matches **only**
    `npm run test` **or** `sh tests/run-tests.sh` (PowerShell test runner command is **not**
    accepted by the baseline grep/regex).
  - **Detector behavior**: when `package.json` exists and `scripts.test` is non-empty,
    installers prefer `npm run test` (matches baseline). If that path is skipped (no test
    script) **and** the stack falls through on Windows/Python installers, **PowerShell**
    `tests/run-tests.ps1` is chosen — **that value fails the US-0074 baseline asserts** even
    though it is a valid local test command. `installer.sh` never emits the PowerShell branch;
    it prefers `sh tests/run-tests.sh` when present after npm/go/python — cross-check parity
    when changing detection order.
  - **Secondary failure modes**: `npm` / `sh` missing on the install host marks the candidate
    invalid → bootstrap notes + possible install failure with empty unresolved `TEST_COMMAND`;
    non-empty pre-seeded `TEST_COMMAND` in template skips auto-fill (by design) — mismatches
    must be caught by tests, not masked.
- **Remediation direction (for architecture / execute)**:
  - Keep formula aligned on every version bump (automate or gate in CI).
  - Either narrow installers to emit only baseline-allowed `TEST_COMMAND` values for
    detectable stacks, **or** extend tests to accept the PowerShell runner **only** if
    product intent is to treat it as a first-class bootstrap outcome (document tradeoff in
    architecture — avoids hiding real Windows defaults).

## R-0052

- **Date**: 2026-03-25
- **Topic**: US-0075 scratchpad **example–first** refresh and **AC-11** paired key/section
  parity (no catalog skew between materialized baseline and framework example)
- **Query**: Where should upgrade/install enforce ordering so
  **`.cursor/scratchpad.local.example.md`** never lags template while
  **`.cursor/scratchpad.md`** moves; how should a deterministic parity gate be specified
  and implemented?
- **Sources**:
  - `docs/product/backlog.md` (**US-0075**)
  - `docs/product/vision.md` (Intake / Discovery notes — **US-0075**)
  - `handoffs/po_to_tl.md` (Discovery Addendum — **US-0075**)
  - `decisions/DEC-0055.md`, `decisions/DEC-0039.md` (ownership + upgrade-safe example)
  - `installer.py`, `installer.ps1`, `installer.sh`, `bin/its-magic.js`
  - `docs/engineering/context/installer-owned-paths.manifest` (+ `template/` mirror)
- **Findings**:
  - **Problem class**: Under **Model B** (**DEC-0055** / **US-0073**), materialized
    **`.cursor/scratchpad.md`** can be refreshed (copy loop +/or
    `run_scratchpad_postinstall` / `materialize_scratchpad_baseline`) while the
    framework-owned **example** file remains stale relative to the shipped template pair —
    operators lose a trustworthy copy-from catalog (**DEC-0039**, **US-0057** regression
    posture).
  - **Ordering invariant (product)**: Any step that advances the materialized baseline from
    **`template/.cursor/scratchpad.md`** must be preceded by or atomically bundled with
    refresh of **`.cursor/scratchpad.local.example.md`** from
    **`template/.cursor/scratchpad.local.example.md`** so the example never ends “older than
    template” when the baseline moved (**US-0075** **AC-1**, **AC-3**).
  - **AC-11**: Require the **same** set of documented **`##` section headers** and
    **`KEY=`** lines in each **paired** surface (active and template), with values allowed
    to differ only where the story documents intentional conservative defaults; default is
    **no** one-sided keys (**US-0075** **AC-11**).
  - **Diagnostics**: Operator-visible output should label **example refresh** vs
    **materialized baseline** vs **user local preserved** with reason-coded paths aligned
    to **DEC-0039** (**US-0075** **AC-5**).
- **Risks**:
  - File-copy iteration order alone is not a contract; without an explicit ordering rule,
    future refactors can reintroduce “baseline first, example later” skew.
  - A naive string equality test between baseline and example will false-fail — parity is
    on **structure** (headers + keys), not identical values.
  - Template vs active drift if checks run only on one tree.
- **Linked**: US-0075, US-0073, US-0057, DEC-0055, DEC-0039
- **Confidence**: high
- **Status**: current

### Post-discovery findings (2026-03-26) — US-0075

- **Installer / manifest file anchors (code-level)**:
  - **`installer.py`**
    - Constants: `SCRATCHPAD_BASELINE_REL`, `SCRATCHPAD_EXAMPLE_REL`, `SCRATCHPAD_LOCAL_REL`;
      merge/validation: `merge_scratchpad_layers`, `validate_merged_scratchpad`;
      materialization: `materialize_scratchpad_baseline`, `run_scratchpad_postinstall`
      (invoked with `mode=upgrade` after the upgrade copy loop).
    - **`mode == "upgrade"`** path (~L669+): iterates `files` from the ownership manifest;
      tracks `scratchpad_example_rel = ".cursor/scratchpad.local.example.md"` status
      (`added` / `updated` / `unchanged` / `not-in-manifest`); then calls
      `run_scratchpad_postinstall(..., "upgrade")` (materialized baseline refresh +
      merged validation). **Architecture should treat this ordering as explicit policy**:
      ensure example copy-from-template cannot logically follow baseline-only advancement
      (either reorder operations, duplicate targeted refresh, or add a post-postinstall
      example sync) — **US-0075** closes the gap.
  - **`installer.ps1` / `installer.sh`**: parity surfaces for install/upgrade delegation;
      must keep **same** scratchpad ordering + diagnostics contract as **`installer.py`**
      (**US-0075** **AC-4**).
  - **`bin/its-magic.js`**: operator CLI entry (`--mode upgrade`); ensure spawned installer
      path cannot skip example refresh that the Python upgrade path would perform.
  - **`docs/engineering/context/installer-owned-paths.manifest`** (and
    **`template/docs/engineering/context/installer-owned-paths.manifest`**): both list
    **`.cursor/scratchpad.md`** and **`.cursor/scratchpad.local.example.md`** under
    `[install_include_paths]` — manifest parity is part of the triple-installer contract.
  - **Template pair (source of truth for bytes)**:
    - **`template/.cursor/scratchpad.md`**
    - **`template/.cursor/scratchpad.local.example.md`**
    - Installed mirrors: **`.cursor/scratchpad.md`**, **`.cursor/scratchpad.local.example.md`**
- **Parity check design (AC-11 / tests)**:
  - **Scope**: Two **paired** comparisons:
    1. **Active repo**: **`.cursor/scratchpad.md`** ↔ **`.cursor/scratchpad.local.example.md`**
    2. **Template tree**: **`template/.cursor/scratchpad.md`** ↔
       **`template/.cursor/scratchpad.local.example.md`**
  - **Extraction rules (deterministic)**:
    - **Section set**: all markdown headings that are `## ...` at line start (trimmed),
      after removing the leading `## ` — record stable title text for set comparison.
    - **Key set**: lines matching `^[A-Z][A-Z0-9_]*=` (framework **KEY=** assignments),
      taking the identifier before `=` as the canonical key name; ignore commented lines
      (`#` first non-whitespace) and blank lines.
    - **Value stance**: do **not** require value equality between baseline and example;
      only require **set equality** of sections and keys unless a key is listed in a
      **small manifest allowlist** of documented *local-only* exceptions (default **empty**
      per **US-0075**).
  - **Failure output**: emit symmetric difference lists
    (`only_in_baseline`, `only_in_example`) with file paths so operators and CI logs are
    actionable; align reason codes with **DEC-0039** / scratchpad merge diagnostics where
    applicable.
  - **Placement**: implement as a **focused assert** in **`tests/run-tests.ps1`** and
    **`tests/run-tests.sh`** (and optionally a small **`scripts/`** helper invoked by both)
    so **AC-11** is machine-verified, not manual-only.
  - **Upgrade regression tests** (**US-0075** **AC-6**): extend existing upgrade fixtures
    (already touch **`.cursor/scratchpad.local.example.md`** in **`tests/run-tests.sh`**) so
    post-upgrade bytes for the example **match template** whenever the baseline was updated
    in the same run; assert **ordering** via staged temp trees (stale example + fresh
    template) if needed.
