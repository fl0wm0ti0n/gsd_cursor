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

## R-0053

- **Date**: 2026-03-27
- **Topic**: US-0076 — executable linkage from scratchpad sync flags to **git push**
- **Query**: How can **`validate-and-push`** (or successor) read **merged** scratchpad and
  enforce **US-0038** gates without duplicating policy in two places?
- **Sources**:
  - `docs/engineering/runbook.md` (sync policy contract, **US-0038**)
  - `scripts/validate-and-push.ps1`, `scripts/validate-and-push.sh`
  - `installer.py` (`parse_scratchpad_file`, `merge_scratchpad_layers` pattern — reuse vs
    duplicate)
  - `decisions/DEC-0018.md` (if present) / `docs/product/backlog.md` **US-0038**
- **Findings**:
  - **Gap**: Scratchpad keys are **inputs** to `/auto` **documentation** of sync verdicts;
    **validate-and-push** currently keys only off **`runbook.md`** commands — no
    **`ALLOW_AUTO_PUSH`** gate.
  - **Merge rule**: Implementation should mirror **DEC-0055** precedence (**local** >
    **materialized baseline** > **example**) when reading **`SYNC_*`** / **`ALLOW_AUTO_PUSH`**
    so team **`.cursor/scratchpad.local.md`** overrides are honored.
  - **`by_phase` / `by_milestone`**: Scripts do not know “current workflow phase” unless
    passed in (**env var** / **CLI flag** / **state.md** parse) — **architecture** must pick
    one deterministic source to avoid false pushes; default-safe: **treat script invocation
    as explicit phase boundary** when **`SYNC_POLICY_MODE=by_phase`** and document that
    **Cursor does not auto-invoke** the script.
  - **QA gate**: Script cannot fully infer QA state without reading sprint artifacts;
    minimum viable check = **documented** file glob + blocking keyword scan, or **defer**
    push if **open** `qa-findings.md` for active sprint — **architecture** chooses bounded
    rule (**AC-5**).
- **Risks**:
  - **False confidence** if operators believe scratchpad alone pushes — docs must say **run
    validate-and-push** (or CI) after eligible boundaries.
  - **Secret leakage** if push script logs tokens — keep logs to reason codes and branch
    names only.
- **Linked**: US-0076, US-0038, DEC-0018, DEC-0055, US-0071
- **Confidence**: medium-high
- **Status**: current

### US-0076 research refinement (2026-03-27)

- **Implementation anchors** (repo as of research close):
  - **`scripts/validate-and-push.ps1`**: command sourcing is **runbook-only** today (`Read-RunbookKey` / `docs\engineering\runbook.md`); no read of `.cursor/scratchpad*.md`. Push/branch gating after tests must insert **merged** scratchpad evaluation **before** any `git push` attempt.
  - **`scripts/validate-and-push.sh`**: same pattern (`read_runbook_key` / `docs/engineering/runbook.md` only).
  - **`installer.py`**: canonical merge for Model B — `parse_scratchpad_file` + `merge_scratchpad_layers` (local > materialized baseline > example). **Prefer** invoking this from scripts (e.g. `python -c` with repo root) or extracting a small shared Python module **over** re-implementing merge in shell — avoids **DEC-0055** drift and keeps one precedence truth.
  - **Phase / boundary signal**: scripts have no implicit “current `/auto` phase”; align with backlog **AC-7** — default contract = **operator or CI invocation** counts as the eligible boundary for `by_phase` unless **architecture** selects a single alternate (`state.md` last `phase_boundary`, env `SYNC_PHASE_BOUNDARY`, or CLI flag), documented in **DEC-0058** / runbook.
  - **QA / AC-5**: implement a **bounded** scan of sprint **`qa-findings.md`** (path rule fixed in architecture — e.g. active sprint under `sprints/S*/`) for blocking verdict patterns; emit **`BLOCKING_QA_FINDINGS`** / **`PRE_QA_AUTOPUSH_FORBIDDEN`** per **US-0038** semantics without parsing free-form chat.
  - **Tests**: `tests/run-tests.ps1` / `tests/run-tests.sh` — dry-run / fixture-repo / exit-code assertions per **AC-8**; keep PS1/SH behavior aligned.
- **Risk mitigations**:
  - **Dual policy source**: treat **merged scratchpad** as the only source for `SYNC_*` / `ALLOW_AUTO_PUSH` / allowlist in the executable path; runbook remains source for **commands** only — document in **DEC-0058** to prevent divergent “script policy” vs **US-0038**.
  - **Parse / merge failure**: fail closed with `[SCRATCHPAD_MERGE_ERROR]`-style diagnostics (reuse installer messages where possible); **no push** on ambiguous merge.
  - **Over-push on wrong branch**: allowlist match before push; deterministic match rules in architecture + tests.
  - **Operator surprise**: stdout/stderr limited to **US-0071**-safe reason codes; optional **`--dry-run`** (or equivalent) in execute phase to print decisions without `git push`.
- **Architecture-owned gates** (not research blockers): exact `qa-findings` glob, optional `state.md` phase reader vs invocation-only default, and **DEC-0058** vs **DEC-0018** amendment split.

## R-0054

- **Date**: 2026-03-27
- **Topic**: US-0077 — configurable documentation audience/depth profiles and dual README strategy
- **Query**: What deterministic model best separates user-facing and developer-facing docs
  while preserving docs-as-code validation and low drift?
- **Sources**:
  - `docs/engineering/runbook.md` (**US-0031**, **US-0032**, **US-0030** constraints)
  - `docs/product/backlog.md` story contracts for `US-0030`, `US-0031`, `US-0032`
  - External framing: Diataxis documentation model (`https://diataxis.fr/`)
- **Findings**:
  - Existing framework already has two optional axes: technical spec-pack (**US-0031**) and
    end-user guide (**US-0032**), but README/operator surfaces still lack an explicit
    audience+depth profile contract.
  - Diataxis supports a deterministic audience split by intent: user onboarding/how-to versus
    developer reference/explanation; this maps cleanly to profile-driven section templates.
  - A profile pair (`DOC_AUDIENCE_PROFILE`, `DOC_DETAIL_LEVEL`) is a minimal extension that
    can stay backward-compatible with existing flags and preserve release validation.
  - To avoid drift/conflict, generation rules must define which sections are mandatory for each
    profile and which artifact owns each section (README vs user-guide vs spec-pack).
- **Risks**:
  - Ambiguous ownership between README and user-guides can duplicate or contradict instructions.
  - "both + technical-deep" can bloat README unless section budgets are bounded.
  - Profile matrix expansion can increase test cost unless coverage is deterministic and scoped.
- **Linked**: US-0077, US-0030, US-0031, US-0032, US-0071, DEC-0059
- **Confidence**: high
- **Status**: current
- **Delivery closure (2026-03-28)**: Normative semantics shipped in **`DEC-0059`** + **`docs/engineering/architecture.md`** **`# US-0077`** (**S0056**); this entry retained for matrix/traceability — treat architecture/decision as authoritative for literals and validator contracts.

### US-0077 — Concrete profile matrix (post-discovery, research draft for architecture lock)

**Dimensions**: `DOC_AUDIENCE_PROFILE` ∈ {`user`, `developer`, `both`} × `DOC_DETAIL_LEVEL` ∈
{`concise`, `balanced`, `technical-deep`} — **9** cells; architecture locks exact heading
strings and file paths.

**Default artifact ownership (non-overlapping intents)** — names are illustrative; architecture
may substitute equivalent paths if parity rules stay deterministic:

| Surface | Primary intent | Profile use |
|--------|----------------|-------------|
| `README.md` (root) | User/operator **how-to** entry, quickstart, limitations | All profiles read user-required content here or via explicit pointer from here |
| `docs/developer/` (or single `DEVELOPERS.md` / `docs/README.md` developer region) | Workflow, quality gates, extension points | `developer` and `both` |
| `docs/engineering/runbook.md` | Operator command keys | Unchanged **US-0030** surface; profile may control cross-links from README only |
| `docs/user-guides/US-xxxx.md` | Feature depth | **US-0032** when `USER_GUIDE_MODE=1`; profile sets **depth of examples**, not file existence when mode off |
| Spec-pack outputs | Design/CRS/technical spec | **US-0031** when `SPEC_PACK_MODE=1`; profile does not redefine spec-pack semantics |

**Mandatory *semantic* sections per cell** (validators map each key to one or more H2 headings or
anchored regions — architecture defines the literal strings):

Semantic keys (vocabulary):

- **User channel**: `USER_PURPOSE`, `USER_QUICKSTART`, `USER_EXAMPLES`, `USER_TROUBLESHOOTING`,
  `USER_LIMITATIONS`, `USER_RELATED_DOCS`
- **Developer channel**: `DEV_PREREQS`, `DEV_WORKFLOW`, `DEV_QUALITY_GATES`, `DEV_ARCHITECTURE`,
  `DEV_CONTRACTS`, `DEV_DECISIONS`

| Audience × depth | Required semantic keys (minimum) |
|------------------|----------------------------------|
| user × concise | `USER_PURPOSE`, `USER_QUICKSTART`, `USER_LIMITATIONS` |
| user × balanced | above + `USER_EXAMPLES`, `USER_RELATED_DOCS` |
| user × technical-deep | above + `USER_TROUBLESHOOTING` (expanded body budget in architecture) |
| developer × concise | `DEV_PREREQS`, `DEV_WORKFLOW` |
| developer × balanced | above + `DEV_QUALITY_GATES`, `DEV_ARCHITECTURE` |
| developer × technical-deep | above + `DEV_CONTRACTS`, `DEV_DECISIONS` |
| both × concise | union(user×concise, developer×concise) with **split enforcement**: user keys in root README, developer keys in developer shard (or bounded regions — architecture picks one scheme) |
| both × balanced | union(user×balanced, developer×balanced); **split recommended** (README + `docs/developer/*`) |
| both × technical-deep | same union; **split required** — root README stays user/operator scoped; developer-deep content **not** inlined in README body beyond short pointers |

**Section budgets (bloat control)** — soft caps for **H2 count in root `README.md` body** when using a
single file; exceeding triggers `DOC_SECTION_BUDGET_EXCEEDED` unless architecture documents an
explicit waiver path:

| Cell | README H2 budget (indicative) |
|------|-------------------------------|
| user × * | concise ≤5, balanced ≤7, technical-deep ≤9 |
| developer × * | prefer developer shard; if README-only, concise ≤4, balanced ≤6, technical-deep ≤8 |
| both × concise | ≤6 total with labeled regions |
| both × balanced | ≤8 or **must** use split files |
| both × technical-deep | README ≤6 user H2s; developer keys **only** in shard |

### US-0077 — Validation strategy (deterministic)

1. **Inputs**: merged scratchpad (**DEC-0055** precedence) for `DOC_AUDIENCE_PROFILE`,
   `DOC_DETAIL_LEVEL`; read `SPEC_PACK_MODE`, `USER_GUIDE_MODE` for additive optional checks only.
2. **Parse gate**: invalid enum / missing keys → **`DOC_PROFILE_INVALID`** with allowed-value
   remediation (align **AC-1**).
3. **Merge gate**: scratchpad merge failure → **`DOC_PROFILE_MERGE_ERROR`**; no doc mutation.
4. **Completeness scan**: for resolved profile cell, assert each required semantic key maps to an
   existing heading/region in the **owned** artifact(s); missing → **`DOC_SECTION_MISSING:<key>`**.
5. **US-0030 parity**: repeat the same profile cell requirements for **active + `template/`**
   mirrored paths; mismatch → **`DOC_TEMPLATE_PARITY_FAIL`**.
6. **Optional modes**: when `USER_GUIDE_MODE=0` / `SPEC_PACK_MODE=0`, validators **do not** require
   those artifacts; when enabled, existing **US-0032** / **US-0031** contracts add **on top** (no
   contradiction — profile adjusts README/developer surfaces only).
7. **US-0071**: user-visible generated or copied strings in README/developer shards must pass
   existing metadata guard surfaces (extend allowlists in execute phase if new tools emit stdout).
8. **AC-8 regression (tiered, scoped cost)**:
   - **Tier A — anchor fixtures** (full markdown snapshots): `user×concise`, `developer×balanced`,
     `both×technical-deep` (split layout).
   - **Tier B — table-driven presence tests**: synthetic markdown fixtures for the remaining six
     cells exercising the semantic-key → heading resolver only.
   - **Tier C — wiring smoke**: one CI path per `DOC_AUDIENCE_PROFILE` value at `balanced` depth to
     catch enum/merge wiring without 9× full E2E doc generation every run.

**Architecture-owned (explicit non-blockers)**: literal heading text, file split layout, validator
implementation location (standalone script vs installer hook), and **DEC** id for profile semantics.

## R-0055

- **Date**: 2026-03-28
- **Topic**: US-0078 — runtime enforcement of intake question-pack evidence
- **Query**: How should intake prove required topics and assumption confirmations were actually
  collected before persisting backlog/acceptance artifacts?
- **Sources**:
  - `.cursor/commands/intake.md` (US-0068 / DEC-0050 contracts)
  - `docs/engineering/runbook.md` intake sections for US-0051 / US-0068
  - External product discovery guidance on explicit assumption confirmation (assumption mapping)
- **Findings**:
  - Current contract language already requires fail-closed persistence on missing topic coverage
    and explicit assumption confirmation; gap is **evidence enforcement** at runtime.
  - Persisted fields (`asked_topics`, `missing_topics`, `assumptions_confirmed`) are insufficient
    alone when not tied to explicit interaction evidence.
  - Minimal hardening model: require deterministic evidence references for each required topic
    (`answer_ref` or confirmed assumption ref), and block if any required topic lacks one.
  - `assumptions_confirmed=yes` must require explicit user confirmation reference; inferred
    assumptions without confirmation must fail closed.
- **Risks**:
  - Overly strict enforcement can increase friction; remediation prompts must be targeted and bounded.
  - Schema drift across artifacts if evidence fields are introduced without parity updates.
  - False positives if parsers cannot reliably detect confirmation events.
- **Linked**: US-0078, US-0068, DEC-0050, DEC-0060, US-0051, US-0059
- **Confidence**: high
- **Status**: current — **US-0078 research refinement closed 2026-03-28**; **delivery closed 2026-03-29** with **`S0057`** release + **`/refresh-context`** (closes **`auto-20260328-01`**; normative lock-in **`DEC-0060`** / **`architecture.md`** **`# US-0078`**)

### US-0078 — Evidence schema (concrete v1 sketch)

Minimal persisted shape (implementation may serialize as markdown bullets or structured sidecar; **architecture** picks storage and literal `ref` format):

| Field | Purpose |
|-------|---------|
| `selected_pack` | `first-intake-pack` \| `small-intake-pack` (existing **US-0068**). |
| `asked_topics` | Ordered list of **required topic keys** for which the intake run **actually emitted** a question (or a deterministic “assumption proposal” prompt) in-session. |
| `missing_topics` | Subset of required keys still **not** satisfied at gate time (empty when passing). |
| `topic_coverage` | List of `{ topic_key, satisfied_by, ref }` — **one row per required topic** at persistence time. |
| `satisfied_by` | `answer_ref` — user supplied substantive answer tied to `ref`; or `assumption_confirmation_ref` — user explicitly confirmed a stated assumption tied to `ref`. |
| `ref` | Opaque but **canonical** pointer resolvable by validators (e.g. orchestrator message id + turn index, or hash of quoted user text + `intake_run_id`; **DEC** locks format). |
| `assumptions_confirmed` | Literal mirror of today’s contract (`(none)` / free text). |
| `assumption_confirmation_ref` | Required **whenever** `assumptions_confirmed` is non-`(none)` **and** non-empty **and** implies confirmation; must point to the **affirmative** user turn (not model inference). |

**Invariant**: `answered_topics` in backlog/vision language maps to the **set of `topic_key` entries in `topic_coverage`**; audits compare `asked_topics` vs that set to detect “claimed without ask” drift.

### US-0078 — Validation / parser rules (deterministic)

1. **Pack resolution**: derive `required_keys` from `selected_pack` per **intake.md** lists; unknown pack → fail `INTAKE_REQUIRED_PACK_INCOMPLETE`.
2. **Coverage completeness**: ∀ `k` ∈ `required_keys`, ∃ row in `topic_coverage` with `topic_key=k` and non-empty `ref` → else `INTAKE_REQUIRED_TOPIC_MISSING` (aggregate: `INTAKE_REQUIRED_PACK_INCOMPLETE` when multiple gaps).
3. **Asked-vs-covered**: ∀ `k` ∈ keys in `topic_coverage`, `k` must appear in `asked_topics` **unless** `satisfied_by=assumption_confirmation_ref` and architecture documents a single-shot “assumption bundle” ask covering multiple keys (bounded **DEC** exception); default **fail closed** if a covered key was never asked.
4. **Assumption literal integrity**: if `assumptions_confirmed` parses as affirmative / non-placeholder **without** `assumption_confirmation_ref` → `INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`.
5. **False `assumptions_confirmed`**: values like `yes`, `true`, `confirmed` (case-normalized allowlist) **without** matching `assumption_confirmation_ref` → reject (same reason code); do not infer from model-only summaries.
6. **Persistence gate**: any rule 1–5 failure → `INTAKE_PERSISTENCE_BLOCKED` **and** no backlog/acceptance mutation (align **AC-3**).
7. **Mode parity**: `INTAKE_GUIDED_MODE=0` still runs rules 1–6; low-touch may shorten **follow-ups** but **not** skip mandatory pack coverage evidence.

### US-0078 — Reason code mapping (literal alignment)

| Condition | Code |
|-----------|------|
| Missing `topic_coverage` row for required key | `INTAKE_REQUIRED_TOPIC_MISSING` |
| Multiple missing keys or pack not satisfiable | `INTAKE_REQUIRED_PACK_INCOMPLETE` |
| Affirmative assumptions without confirmation ref | `INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED` |
| Any gate failure before write | `INTAKE_PERSISTENCE_BLOCKED` (optional umbrella in diagnostics; sub-codes above remain primary) |

### US-0078 — AC-8 regression matrix and test strategy

| Case | Fixture intent | Expected |
|------|----------------|----------|
| **P1 — full answers** | All `small-intake-pack` keys in `topic_coverage` with `answer_ref` | Persistence allowed; evidence rows present in golden output |
| **P2 — assumption path** | One key satisfied by `assumption_confirmation_ref`; others `answer_ref` | Persistence allowed; refs non-empty |
| **P3 — missing topic** | Omit one `topic_coverage` row | `INTAKE_REQUIRED_TOPIC_MISSING` (or pack incomplete); **no** backlog diff |
| **P4 — false confirmation** | `assumptions_confirmed=yes` + empty `assumption_confirmation_ref` | `INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`; **no** backlog diff |
| **P5 — asked drift (optional Tier B)** | `topic_coverage` includes key absent from `asked_topics` | Fail per rule 3 default (unless DEC documents bundle exception) |

**Test implementation tiers** (cost-scoped):

- **Tier A**: table-driven validator unit tests on synthetic `intake_evidence` objects (no live LLM).
- **Tier B**: golden-file tests on minimal markdown intake handoff snippets produced by fixtures.
- **Tier C**: one integration smoke per `INTAKE_GUIDED_MODE` ∈ {0,1} ensuring gate invoked before persistence hook.

### Architecture-owned (explicit non-blockers for `/architecture`)

- **Update (2026-03-28)**: **`ref`** syntax and migration are locked in **`DEC-0060`**; evidence storage location (inline vs sidecar) remains an execute-phase implementation choice within the logical bundle shape.
- Whether `INTAKE_PERSISTENCE_BLOCKED` is always emitted with a primary sub-code or only granular codes.

## R-0056

- **Date**: 2026-03-28
- **Topic**: US-0079 — first-class bug issue workflow with open/closed lifecycle
- **Query**: How can the framework separate bugs from user stories while staying lightweight and
  avoiding heavy severity/SLA triage?
- **Sources**:
  - `docs/engineering/runbook.md` (status ownership, post-QA release issue workflow, reconciliation)
  - `docs/product/backlog.md` / `docs/product/acceptance.md` (current US-only tracking model)
  - User requirement in intake: bug workflow should be official-style but simple (`OPEN`/`DONE`)
- **Findings**:
  - Current workflow is US-centric; release and QA already distinguish defect contexts in sprint
    artifacts, but there is no first-class bug entity at intake/backlog level.
  - A lightweight `BUG-xxxx` model can align with existing open/closed status discipline and avoid
    introducing mandatory severity/SLA fields.
  - Minimal viable bug schema should include reproducibility essentials (context, steps, expected,
    actual, evidence refs) so bugs remain actionable without heavy triage bureaucracy.
  - Status reconciliation and `/ask` retrieval need explicit extension to support both US and BUG
    identifiers consistently.
- **Risks**:
  - Mixed migration period could create duplicate tracking (same defect as US and BUG) unless
    conversion/link rules are explicit.
  - Adding a second entity type increases ordering/ownership complexity if policy docs are not
    updated in lockstep.
  - Over-lightweight bug fields can reduce reproducibility if minimum schema is underspecified.
- **Linked**: US-0079, US-0045, US-0042, US-0078
- **Intake traceability (2026-03-29)**: PO intake gate **PASS** on **`auto-20260329-01`** — bundle **`handoffs/intake_evidence/US-0079-intake-20260329.json`** (**`small-intake-pack`**, **`DEC-0060`** **`ie:`** refs); aligns with findings above.
- **Discovery traceability (2026-03-29)**: PO **`/discovery`** **PASS** on **`auto-20260329-01`** — alternatives **(1) US-only / (2) heavy triage / (3) lightweight `BUG-xxxx`** with **(3)** recommended; canonical storage favor **`backlog.md`** bug region vs split file TBD in **`/architecture`**; checkpoint **`docs/engineering/state.md`** **Discovery checkpoint (2026-03-29) — US-0079 / auto-20260329-01**; next **`/research`**.
- **Research closure (2026-03-29, tech-lead, `orchestrator_run_id=auto-20260329-01`)**: Deepened routing, schema, reconciliation, and test guidance for **`/architecture`** / **DEC** (**AC-10**). Checkpoint: **`docs/engineering/state.md`** **Research checkpoint (2026-03-29) — US-0079 / auto-20260329-01**; next **`/architecture`**.
- **Recommended design direction**:
  - **Identifier**: `BUG-` + **four-digit** decimal (`BUG-0001`…), assigned with the **same deterministic “next after highest existing”** policy as **`US-xxxx`** (architecture may alias this to a shared allocator doc).
  - **Canonical home**: dedicated **`## Bug issues (canonical)`** section in **`docs/product/backlog.md`**, **append-new** for new bugs, stable ordering **by id** within the section; **split to** `docs/product/bugs.md` **only** if triad/line-budget or operator policy triggers (mirror **DEC-0054**-style compaction), with **explicit cross-links** and **US-0045** reconciliation text naming both surfaces.
  - **Status**: exactly **`OPEN`** | **`DONE`** in the bug header line (same literal discipline as stories); optional free-text **severity/narrative** allowed **outside** required state fields (no state machine).
  - **Minimum schema (AC-4)**: each bug entry is a **single markdown story-like block** with required sub-bullets or labeled lines (DEC locks literals):
    - `environment` / context (product area, OS/tooling, branch/commit if known)
    - `steps_to_reproduce` (ordered, deterministic)
    - `expected`
    - `actual`
    - `evidence_refs` (paths, logs, screenshots, or opaque refs — non-empty list)
  - **Routing (AC-2)**: **no silent** “defect prose → **`US-xxxx`**”. Require an **explicit operator signal** before persistence, e.g. **`/intake bug`** (or equivalent command flag) **and/or** scratchpad key **`INTAKE_WORK_ITEM_KIND=bug`** (name finalized in architecture) checked by intake rules; misclassified attempts → deterministic **`INTAKE_WORK_ITEM_KIND_MISMATCH`** (or successor code) **without** backlog write.
  - **Anti-duplication**: one canonical **`BUG-xxxx`** per defect; **`supersedes` / `duplicate_of`** optional fields; discourage parallel **`US-xxxx`** for same defect — if a bug drives feature work, use **`related_us`** / **`blocks_us`** link lists (markdown bullets) rather than converting the bug into a story.
  - **Sprint / QA / release (AC-5, AC-6)**: sprint **`tasks.md`** and **`summary.md`** may reference **`BUG-xxxx`** in task titles or **Traceability** rows; **`qa-findings.md`**, **`uat.*`**, **`release-findings.md`** accept **`BUG-xxxx`** alongside **`US-xxxx`** using the same “id + evidence ref” style as **US-0042** post-QA issues.
  - **`/ask` + context packs (AC-8)**: narrow-read lists and engineering **state** breadcrumbs treat **`BUG-`** as a **first-class id prefix** alongside **`US-`** (regex / allowlist extension; no semantic merge of families).
- **Constraints (reaffirmed)**:
  - No mandatory **severity / SLA / triage** states; no incident-platform integration in this story.
  - Must **not** regress **US-0045** story semantics; bug status is a **second family** with parallel reconciliation rules.
- **Alternatives / tradeoffs** (for **DEC** summary):

| Option | Upside | Downside |
|--------|--------|----------|
| **A — US-only defects** | One artifact type | Conflates feature intent and defects; weak traceability (**rejected** per discovery) |
| **B — Heavy triage** | Enterprise defect flow | Out of scope; operator overhead |
| **C — `BUG-xxxx` + OPEN/DONE (recommended)** | Clear identity, lightweight | Second allocator + reconciliation path; needs disciplined routing |
| **D — GitHub-Issues-only tracking** | External tool native | Breaks canonical **`backlog.md`** authority (**US-0045**); **rejected** for this framework |

- **Test / validation guidance (maps to AC-1..AC-10)**:
  - **Tier A — Parser/validator fixtures**: synthetic **`backlog.md`** snippets — valid bug, missing `steps_to_reproduce`, missing `evidence_refs`, illegal status literal, malformed id; expect deterministic fail codes.
  - **Tier B — Routing/intake**: guided + low-touch parity — attempt defect persistence **without** bug kind signal → **no write** + diagnostic; with signal → **`BUG-xxxx`** allocated + evidence row shape valid.
  - **Tier C — Reconciliation**: golden tests for **US-0045**-style scripts: backlog bug **OPEN** vs acceptance/state contradiction detection includes **`BUG-`** rows.
  - **Tier D — Traceability spot-check**: sprint template + one **`qa-findings`** / **`release-findings`** example line referencing **`BUG-xxxx`** (documentation or fixture).
- **Architecture / DEC gates** (**AC-10**): allocator rules, literal field names, routing keys + reason codes, optional file-split policy, migration (**grandfather**: existing defects remain prose under **`US-xxxx`** until manually ported), validator entrypoint(s), and **`acceptance.md`** row strategy (**separate bug checklist subsection** vs inline — pick one for determinism).
- **Architecture closure (2026-03-29, tech-lead, `orchestrator_run_id=auto-20260329-01`)**: **`DEC-0061`** + **`architecture.md`** **`# US-0079`** lock routing (**`INTAKE_WORK_ITEM_KIND`**, **`/intake bug`**), **`## Bug acceptance (canonical)`**, optional **`bug_ids`** on **`state.md`** phase boundaries; checkpoint **`docs/engineering/state.md`** **Architecture checkpoint (2026-03-29) — US-0079 / auto-20260329-01**; next **`/sprint-plan`**.
- **Delivery closure (2026-03-30, curator, `orchestrator_run_id=auto-20260329-01`)**: Shipped via sprint **`S0058`** — validators, canonical bug regions, §26L tests; **`/release`** **PASS**; run closed at **`/refresh-context`** — **`docs/engineering/state.md`** **Refresh-context checkpoint (2026-03-30) — post S0058 / US-0079 (auto-20260329-01)** (`stop_reason=completed`, `next_scheduled_phase=none`).
- **Sources**:
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/configuring-issues/planning-and-tracking-work-for-your-team-or-project (lightweight issue planning patterns; analog for minimal **`OPEN`/`closed`**-style workflows)
  - `docs/engineering/runbook.md`, **US-0042**, **US-0045**, **US-0078**/**DEC-0060** (evidence + fail-closed persistence precedent)
- **Confidence**: high (for recommended path **C**); medium (for exact routing key naming pending **DEC**)
- **Status**: closed (delivered with **US-0079** / **`S0058`** / **`DEC-0061`**; see delivery closure above)

## R-0057

- **Date**: 2026-03-29
- **Topic**: US-0080 — token-cost hardening for orchestration/cache-read-heavy runs
- **Query**: Which deterministic changes can reduce cache-read token volume significantly without
  weakening workflow gates?
- **Sources**:
  - `docs/engineering/runbook.md` (US-0053 token-profile and context compaction contracts)
  - Observed operator symptom: cache-read far exceeding fresh input/output in long orchestration threads
  - [Anthropic — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
    (automatic vs explicit `cache_control` breakpoints; usage fields including
    `cache_read_input_tokens` and `cache_creation_input_tokens`, and their relationship to
    `input_tokens`; default 5-minute TTL vs
    optional 1-hour TTL; minimum cacheable prefix lengths; below-minimum prompts succeed **without**
    caching—verify via usage fields when both cache counters are zero)
  - [Cursor — Dynamic context discovery](https://cursor.com/blog/dynamic-context-discovery)
    (file-backed tool outputs, incremental reads, fresh-chat boundaries—analogous operator patterns
    for limiting repeated mega-context in long agent threads)
- **Findings**:
  - High cache-read is expected when many calls repeatedly include large stable prefixes; it scales
    with call count and prefix size, not just user message size.
  - Biggest levers are structural: fewer repeated large instruction blocks and tighter per-phase
    context packs, plus fewer orchestration hops where safe.
  - `TOKEN_PROFILE=lean` helps but is insufficient alone without command/context payload slimming.
  - Comparable-run measurement must be explicit (same story class/profile) to make a 50% target auditable.
  - Vendor-reported **`cache_read_input_tokens`**-style fields are the right *conceptual* accounting
    for “cache read” in API-shaped usage; map any product-specific UI labels to those semantics in **DEC**
    so AC-1/AC-2 stay unambiguous even if the host environment changes.
  - **Run-class tuple (answers discovery open question)**: freeze a deterministic comparison key:
    `story_id` + merged **`TOKEN_PROFILE`** + **`SECURITY_REVIEW`** + materialized **`phase_policy_mode`**
    and ordered **`resolved_phase_plan`** (as recorded pre-spawn per **DEC-0052**) + resume anchor
    (`requested_start_from`, `resolution_source`, `resolved_start_phase`). Hash or canonicalize this
    tuple for regression baselines; do not compare across different phase plans or profiles.
  - **Evidence channel (answers discovery open question)**: store **append-only** per-run metric rows
    in-repo (for example `handoffs/token_cost_runs/<orchestrator_run_id>.md` or JSONL) with
    per-phase rollups: `cache_read_tokens`, `input_tokens`, `output_tokens`, phase call counts; link
    from `docs/engineering/state.md` auto continuation breadcrumbs. Treat IDE usage panes as
    supplementary—canonical audit trail remains committed artifacts.
  - **Active/template parity (answers discovery open question)**: enumerate touched paths under
    `.cursor/commands/`, `.cursor/rules/`, and `template/` mirrors; extend parity checks beyond
    scratchpad pairs (pattern aligned with existing `scripts/check-scratchpad-pair-parity.py` discipline)
    so slimming cannot ship with template drift.
- **Risks**:
  - Over-aggressive slimming can hide required policy constraints or reduce operator clarity.
  - Metric gaming risk if baseline/target run classes are not defined deterministically.
  - Divergence risk if active/template command surfaces are slimmed inconsistently.
- **Linked**: US-0080, US-0053, DEC-0035, US-0070, DEC-0052, US-0048, US-0056, US-0069
- **Research closure (2026-03-30, tech-lead, `orchestrator_run_id=auto-20260329-02`)**: Web-grounded
  extension above; discovery questions on **run-class**, **evidence placement**, and **parity scope**
  resolved at research depth — normatively locked in **`DEC-0062`** + **`architecture.md`** **`# US-0080`**.
- **Architecture closure (2026-03-29, tech-lead, `orchestrator_run_id=auto-20260329-02`)**: **`DEC-0062`**
  + **`docs/engineering/architecture.md`** **`# US-0080`** lock metric literals, **`run_class_hash`**,
  **`handoffs/token_cost_runs/`** evidence channel, parity manifest contract, AC-10 trade-offs + phase
  boundary visibility; delivery completed **`S0059`** / **US-0080** **2026-03-29**; curator **`/refresh-context`**
  **2026-03-30** (`auto-20260329-02`).
- **Confidence**: high (vendor cache accounting + structural levers); high (host label mapping delegated
  to **`DEC-0062`** §1 `metric_source` / comparability rules)
- **Status**: closed (delivered with **US-0080** / **`S0059`** / **`DEC-0062`**; see **`docs/engineering/state.md`**
  refresh-context checkpoint **`auto-20260329-02`**)

## R-0058

- **Date**: 2026-03-30
- **Topic**: BUG-0001 — template/install completeness for **`intake_*`** gate scripts
- **Query**: How does npm packaging surface affect which `template/` files reach consumers, and what does the repo ship today?
- **Sources**:
  - [npm — `package.json` → `files`](https://docs.npmjs.com/cli/v11/configuring-npm/package-json#files) (optional `files` array defines tarball contents; directory patterns include subtree for pack/install)
  - `package.json` — `files` includes `template/` wholesale
  - Repo inventory: `scripts/intake_evidence_lib.py`, `scripts/intake_evidence_validate.py`, `scripts/intake_bug_routing_guard.py` exist; `template/scripts/` contains **no** `intake_*.py` (glob audit **2026-03-30**)
- **Findings**:
  - Published tarballs include everything under `template/` that is not excluded by `.npmignore`/`.gitignore` rules in subtrees; completeness bugs in **`template/`** propagate to all npm-based installs.
  - Root `scripts/` entries are only packaged if listed in `files` or default rules — **`intake_*`** today live under **`scripts/`** but **`package.json`** does **not** enumerate them (only `scripts/doc_profile_lib.py` is extra); installers that copy from **`template/`** therefore miss **`intake_*`** unless **`template/scripts/`** is fixed or install paths pull from repo **`scripts/`**.
  - Fix axis: align **`template/scripts/`** with intake-required scripts (minimal completeness) and keep **triple-installer parity**; optional regression: assert **`intake_*`** present in packaged template or post-install tree.
  - **Transitive import closure (2026-03-30, research)**: `intake_evidence_validate.py` imports only **`intake_evidence_lib`** (plus stdlib). **`intake_evidence_lib.py`** uses stdlib only (`hashlib`, `json`, `re`, `dataclasses`, `typing`). **`intake_bug_routing_guard.py`** is stdlib-only. **Minimal intake script set** for install completeness = those **three** modules under **`template/scripts/`** (no additional repo Python deps for gates).
  - **Triple-installer / install source (2026-03-30, research)**: **`installer.ps1`** and **`installer.sh`** set install **`SOURCE_ROOT`** to the packaged **`template/`** directory adjacent to the installer — consumer workspaces are hydrated from **`template/`**, not from repo-root **`scripts/`**. Chocolatey/Homebrew fetch full GitHub tag archives, but the same installer entrypoints apply; parity across npm tarball, Choco zip, and Brew tarball therefore reduces to **keeping `template/` (especially `template/scripts/`) identical** for the shipped release artifact set — root **`scripts/intake_*`** in a source zip does **not** fix target repos unless installers or **`files`** are deliberately extended (separate design choice).
  - **Architecture handoff**: Decide **`package.json` `files`** policy (list **`template/`** only vs also root **`scripts/intake_*`**), add deterministic parity checks (**active `scripts/` ↔ `template/scripts/`** for intake modules), and regression tests or pack-time assertions so upgrades deliver new files per **US-0018**. **Resolved (2026-03-30)** — **`DEC-0063`** / **`architecture.md`** **`# BUG-0001`**.
- **Research closure (2026-03-30, tech-lead, `orchestrator_run_id=auto-20260330-01`)**: Extended after **post-discovery** inventory; handed off to **`/architecture`** — satisfied by **`DEC-0063`** below.
- **Architecture traceability (2026-03-30, tech-lead, `orchestrator_run_id=auto-20260330-01`)**: **`DEC-0063`** accepted — normative ship path locked; implementation + release completed sprint **`S0060`** **2026-03-30**.
- **Curator closure (2026-03-30, curator, `orchestrator_run_id=auto-20260330-01`)**: **`/refresh-context`** after **`S0060`** release — **`docs/engineering/state.md`** **Refresh-context checkpoint (2026-03-30) — S0060 / BUG-0001 / auto-20260330-01** (`stop_reason=completed`, `next_scheduled_phase=none`); **`R-0058`** research questions **resolved** in delivery (template mirror + parity gates per **`DEC-0063`**).
- **Linked**: BUG-0001, US-0008, US-0018, DEC-0060, DEC-0061, DEC-0063
- **Confidence**: high (local inventory + npm `files` semantics + installer source-root review + import scan)
- **Status**: closed (delivered with **BUG-0001** / **`S0060`** / **`DEC-0063`**; see **`docs/engineering/state.md`** refresh-context checkpoint **`auto-20260330-01`**)

## R-0059

- **Date**: 2026-03-31
- **Topic**: US-0081 — deterministic first-intake full-plan coverage gate
- **Query**: Which implementation/test patterns best enforce complete broad-intake plan coverage (`plan_area_id -> story_id[] | deferred_ref`) before persistence, with deterministic fail-closed diagnostics?
- **Sources**:
  - [JSON Schema draft 2020-12](https://json-schema.org/draft/2020-12)
  - [JSON Schema Validation draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-validation.html)
  - [Pytest parametrization docs](https://docs.pytest.org/parametrize.html)
  - [RFC 8785 — JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785)
  - Internal context: `docs/product/backlog.md` (`US-0081` discovery notes), `handoffs/po_to_tl.md` (Discovery Addendum — US-0081), `docs/engineering/state.md` (Discovery checkpoint 2026-03-31, `auto-20260331-01`)
- **Findings**:
  - **Coverage schema pattern**: represent broad-intake plan completeness as a machine-verifiable map with explicit XOR outcome per area: each `plan_area_id` must resolve to either non-empty `story_id[]` or `deferred_ref` (not both empty). This maps cleanly to deterministic validator logic and JSON-schema-style `oneOf` constraints.
  - **Persistence gate pattern**: run a pre-persistence coverage validator after inventory normalization; if any major `plan_area_id` is unmapped, fail closed with `INTAKE_PLAN_COVERAGE_MISSING` under `INTAKE_PERSISTENCE_BLOCKED`, plus deterministic remediation text naming missing IDs.
  - **Deterministic policy implications**: keep `docs/product/backlog.md` as status authority (US-0045), so research/scope closure lines must not auto-transition story status; `US-0081` remains `OPEN` until downstream delivery phases close acceptance.
  - **Deterministic test implications**: use parameterized pass/fail fixture rows for (a) full mapping pass, (b) justified defer pass, (c) missing mapping fail; include parity fixtures for active and `template/` intake surfaces so coverage-gate behavior cannot drift.
  - **Proof/hash implication**: strict-proof tuples should continue canonical sorted-key JSON hashing (current DEC-0038 practice). RFC 8785 reinforces the same determinism principle for stable cross-run evidence hashing.
- **Risks**:
  - **Inventory drift risk**: under-normalized `plan_area_inventory` can under-report gaps; mitigate with deterministic normalization rules and snapshot fields persisted in evidence.
  - **False-pass risk**: accepting empty/placeholder mappings defeats the gate; mitigate with non-empty constraints and explicit deferred rationale references.
  - **Parity drift risk**: active/template intake validators can diverge; mitigate with mirrored fixtures + parity checks in CI.
  - **Operator friction risk**: over-strict diagnostics can block legitimate phased plans; mitigate by allowing explicit `deferred_ref` with rationale while still requiring total area accounting.
- **Curator closure (2026-03-31, curator, `orchestrator_run_id=auto-20260331-01`)**: **`/refresh-context`** after **`S0061`** release — **`docs/engineering/state.md`** **Refresh-context checkpoint (2026-03-31) — S0061 / US-0081 / auto-20260331-01** (`stop_reason=completed`, `next_scheduled_phase=none`); **`R-0059`** findings are now fully resolved by delivered gate implementation and release evidence under **`DEC-0064`**.
- **Linked**: US-0081, US-0045, US-0056, DEC-0038, DEC-0060, DEC-0064
- **Status**: closed (delivered with **US-0081** / **`S0061`** / **`DEC-0064`**; see refresh-context closure above)

## R-0060

- **Date**: 2026-03-31
- **Topic**: US-0082 — agent-driven `codebase-map.md` bootstrap (lifecycle hooks vs manual `/map-codebase`)
- **Query**: How do Cursor-style projects usually onboard agents to repo structure, and what deterministic workflow hook patterns fit this repo’s `/auto` phases, ownership policy, and parity constraints?
- **Sources**:
  - [Cursor — Rules (customization)](https://cursor.com/docs/context/rules) — persistent markdown rules and referenced docs are the supported, version-controlled way to steer agents; no built-in automatic “codebase map” artifact.
  - [Cursor — Documentation](https://cursor.com/docs) — product docs emphasize explicit project configuration rather than implicit generated repo surveys.
  - Internal: `.cursor/commands/map-codebase.md`, `template/.cursor/commands/map-codebase.md` (declared outputs: `docs/engineering/codebase-map.md`, `docs/engineering/dependencies.json`, `docs/engineering/state.md`; phase roles **tech-lead** / **curator**).
  - Internal: `docs/product/backlog.md` (**US-0082** AC-1..AC-10, **US-0001** DONE — command exists without guaranteed lifecycle invocation).
- **Findings**:
  - **Expectation gap (confirmed)**: vendors document rules/docs as the primary onboarding surface; a dedicated **`codebase-map.md`** remains a **repo-owned workflow artifact** unless a project explicitly schedules its creation — aligns with **BUG-0002** reclassification → **US-0082**.
  - **Hook families for `/architecture` to decide** (non-exclusive): (1) **Phase-gated generation** — e.g. require or default-generate map at a named `/auto` phase boundary (**architecture**, **refresh-context**, or a profile-specific bootstrap step) with idempotent overwrite rules (**AC-3**). (2) **Preflight diagnostic** — `/ask` + runbook gate that detects missing map and routes to **`/map-codebase`** or TL/Dev action (**AC-5**, **AC-6**). (3) **CI/regression guard** — test or script fails when template/fresh-repo layout lacks map after install (**AC-8**). (4) **Orchestrator materialization** — extend deterministic `/auto` plan materialization only when policy explicitly includes map bootstrap (avoid silent scope creep vs **DEC-0052** profiles).
  - **Ownership / non-intake writers (**AC-4**)**: any auto-trigger must cite the same artifact-ownership rules as manual **`/map-codebase`** (append-only **`state.md`**, bounded writes to engineering docs) — architecture should name the authoritative writer role and conflict policy.
  - **Idempotency (**AC-3**)**: prefer content-aware refresh (stable sections, deterministic ordering) or explicit “skip if fresh” rules over timestamp-only churn unless acceptance requires audit stamps.
  - **Parity (**AC-7**)**: active + `template/` command surfaces for map/bootstrap must stay mirrored; research does not pick file-level edits — defer to **`/architecture`** + sprint tasks.
- **Risks**:
  - **Over-automation**: running map generation on every `/auto` cycle could churn **`state.md`** or create merge noise — mitigate with explicit phase/profile gating and idempotency.
  - **Under-automation**: diagnostics-only path may still leave fresh repos empty if operators skip runbook — mitigate with CI guard or default-once hook.
  - **Role drift**: if both **tech-lead** and **curator** can invoke **`/map-codebase`**, architecture must define a single default owner for auto paths to satisfy **AC-1**.
- **Research closure (2026-03-31, tech-lead, `orchestrator_run_id=auto-20260331-02`)**: Findings bounded to options + constraints; **`/architecture`** selects normative lifecycle binding and decision records (**DEC-####** as needed) without expanding backlog AC rows.
- **Architecture closure (2026-03-31, tech-lead, `orchestrator_run_id=auto-20260331-02`)**: Normative lock **`DEC-0065`** + **`docs/engineering/architecture.md`** **`# US-0082`**.
- **Delivery closure (2026-03-31, curator, `orchestrator_run_id=auto-20260331-02`)**: **`US-0082`** **DONE** / **`S0062`** **released**; research entry closed with sprint delivery per **US-0045** — see **`docs/engineering/state.md`** **Refresh-context checkpoint (2026-03-31) — S0062 / US-0082 / auto-20260331-02**.
- **Linked**: US-0082, US-0001, BUG-0002, US-0045, US-0056, DEC-0051, DEC-0052, DEC-0065
- **Confidence**: medium-high (vendor doc survey + internal command/backlog cross-check)
- **Status**: closed (**US-0082** **DONE**, **`S0062`** **released**; **`R-0060`** basis for **`DEC-0065`** / **`# US-0082`**)

## R-0061

- **Date**: 2026-03-31
- **Topic**: BUG-0003 - installer mode-path completeness for `missing` and `upgrade`
- **Query**: Which deterministic strategy should guarantee that framework-critical scripts (including `scripts/enforce-triad-hot-surface.py`) are present after `missing` and `upgrade`, with parity across `installer.ps1`, `installer.sh`, and `installer.py` plus auditable diagnostics/tests?
- **Sources**:
  - [Python `shutil` docs](https://docs.python.org/3/library/shutil.html) (overwrite semantics used by `shutil.copy2` in `installer.py`)
  - [PowerShell `Copy-Item` docs](https://learn.microsoft.com/powershell/module/microsoft.powershell.management/copy-item) (overwrite/update behavior in `installer.ps1`)
  - [Linux `cp(1)` docs](https://www.man7.org/linux/man-pages/man1/cp.1.html) (copy/update behavior in `installer.sh`)
  - [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) (deterministic canonicalization principle for stable diagnostics/proofs)
  - Internal: `installer.ps1`, `installer.sh`, `installer.py`, `docs/engineering/context/installer-owned-paths.manifest`, `docs/product/backlog.md` (`BUG-0003`), `handoffs/po_to_tl.md` (BUG-0003 discovery handoff), `docs/engineering/state.md` (BUG-0003 discovery checkpoint)
- **Findings**:
  - **Branch-logic inventory parity (confirmed)**:
    - `missing`: all three installers skip existing files and only copy absent paths (`installer.ps1` loop with `if ($mode -eq "missing") { if ($exists) { continue } ... }`; `installer.sh` `if [ "$MODE" = "missing" ]; then [ -f "$dst" ] && continue ...`; `installer.py` `if mode == "missing": if exists: continue ...`).
    - `upgrade`: all three installers evaluate categorized files and update framework-class files while preserving user-data class, and add missing files (`Classify-File` / `classify_file` branches).
    - This means path completeness is driven primarily by installer input inventory, not by branch divergence.
  - **Current gap root cause**: installer input inventory is manifest-driven (`install_include_paths`), and the manifest currently lists selected scripts but omits `scripts/enforce-triad-hot-surface.py`; therefore both `missing` and `upgrade` can complete successfully while that script remains absent.
  - **Required-script source-of-truth alternatives**:
    - **A (simplest, recommended)**: treat `docs/engineering/context/installer-owned-paths.manifest` as the single required-script source of truth; add the missing script path and keep installer code unchanged.
    - **B (dual-source fallback)**: derive required scripts from `scripts/` patterns plus manifest exclusions. Rejected as higher drift risk and harder to reason about.
    - **C (hard-coded list in each installer)**: explicit in code but highest parity/maintenance burden (three codepaths plus template mirrors).
    - Recommendation: **A** unless architecture identifies a concrete failure mode that manifest-only cannot cover.
  - **Deterministic diagnostics implications**:
    - Add a post-install completeness check in shared installer logic (prefer `installer.py` helper invoked by shell wrappers) that validates a bounded required-script set and emits stable reason codes on miss (for example `INSTALL_REQUIRED_SCRIPT_MISSING:<path>` under an install completeness umbrella).
    - Keep strict-proof hashing model unchanged (sorted-key JSON + SHA-256 per DEC-0038); reuse deterministic field ordering for any new completeness evidence blob.
  - **Deterministic test implications**:
    - Add parity fixtures for both `missing` and `upgrade` proving required scripts are present after install (active + template packaging path).
    - Add a negative fixture that intentionally omits a required script from staged template input and asserts deterministic fail code.
    - Extend runbook/install smoke tests to verify required-script manifest entries are installed and cleaned consistently with `clean_paths`.
- **Risks**:
  - **False completeness risk**: if required inventory remains implicit, installs can pass while missing critical scripts. Mitigate via single manifest source + explicit completeness validator.
  - **Parity drift risk**: if checks are duplicated in PS1/SH/PY, behavior can diverge. Mitigate with Python-shared validation path and wrapper reuse.
  - **Over-strict gate risk**: new checks could block installs in partially customized repos. Mitigate with clear framework/user-data boundaries and deterministic remediation text.
  - **Cleanup asymmetry risk**: adding install paths without matching clean-path policy can leave residue or remove wrong files. Mitigate with paired manifest review in architecture/sprint tasks.
- **Research closure (2026-03-31, tech-lead, `orchestrator_run_id=auto-20260331-03`)**: bounded BUG-0003 research complete; architecture should lock manifest authority, completeness diagnostics contract, and parity regression matrix before sprint planning.
- **Architecture closure (2026-03-31, tech-lead, `orchestrator_run_id=auto-20260331-03`)**: normative lock **`DEC-0066`** + **`docs/engineering/architecture.md`** **`# BUG-0003`**.
- **Delivery closure (2026-04-01, curator, `orchestrator_run_id=auto-20260331-03`)**: **`BUG-0003`** **DONE** / **`S0063`** **released**; refresh-context reconciliation completed across backlog/acceptance/release queue/state and this entry is now closure-fresh.
- **Linked**: BUG-0003, BUG-0001, US-0018, US-0045, US-0056, DEC-0038
- **Confidence**: high (direct code-path inventory across all three installers + platform copy semantics references)
- **Status**: closed (**`BUG-0003`** **DONE**, **`S0063`** **released**; basis for **`DEC-0066`** / **`# BUG-0003`**)

## R-0062

- **Date**: 2026-04-01
- **Topic**: US-0083 - delegable intake clarification without hard blocks
- **Query**: What deterministic evidence/validator pattern enables explicit, topic-scoped user delegation for unresolved required intake topics while preserving fail-closed behavior for non-delegated gaps and guided/low-touch parity?
- **Sources**:
  - [JSON Schema - Boolean JSON Schema combination](https://json-schema.org/understanding-json-schema/reference/combining.html) (`oneOf`/`anyOf` tradeoffs for mutually exclusive branch validation)
  - [JSON Schema - Conditional schema validation](https://json-schema.org/understanding-json-schema/reference/conditionals) (`if`/`then`/`else`, `dependentRequired` for deterministic branch requirements)
  - [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) (audit-event field model: when/where/who/what + reason/confidence)
  - Internal: `docs/product/backlog.md` (`US-0083` discovery scope/ACs), `docs/product/vision.md` (intake and adaptive questioning values), `scripts/intake_evidence_lib.py`, `scripts/intake_evidence_validate.py`, `handoffs/po_to_tl.md`, `handoffs/resume_brief.md`
- **Findings**:
  - **Current validator behavior (confirmed)**:
    - `scripts/intake_evidence_lib.py` enforces required topics strictly by requiring each required `topic_key` to have verifiable `ie:` coverage (`satisfied_by` currently limited to `answer_ref|assumption_confirmation_ref`), and fails with `INTAKE_REQUIRED_TOPIC_MISSING` + `INTAKE_PERSISTENCE_BLOCKED` when coverage is absent.
    - Guided vs low-touch parity is already intentional (`intake_guided_mode` is a no-op in validation), so delegation should not introduce mode-branching semantics.
  - **Delegation evidence shape (recommended)**:
    - Keep topic-level contract and add a third allowed branch for unresolved required topics: `satisfied_by=delegation_ref`.
    - Require deterministic row fields when delegated: `delegation_scope` (bounded decision area), `delegation_rationale` (why user delegates), `delegation_confidence` (`low|medium|high`), and quoted user opt-in text bound by `ie:` hash input.
    - Preserve DEC-0060-style binding by extending `ie:` payload verification to include the delegated branch literal and quoted delegation text; no opaque free-form bypass tokens.
  - **Validator branch semantics (recommended)**:
    - **Non-delegated unresolved required topic** -> unchanged fail-closed (`INTAKE_REQUIRED_TOPIC_MISSING` path preserved).
    - **Delegated unresolved required topic with complete evidence** -> pass topic coverage validation.
    - **Delegated unresolved required topic with malformed/incomplete evidence** -> fail-closed with deterministic delegation-specific code(s) before persistence.
  - **Alternative analysis ("what's the alternative?")**:
    - **A (simplest, recommended)**: extend existing topic row schema with `delegation_ref` branch and bounded delegation metadata.
    - **B**: separate top-level `delegations[]` structure with cross-references to topic rows. Rejected: more joins, higher mismatch risk, and harder diagnostics.
    - **C**: global intake-level delegation toggle for all missing topics. Rejected: violates discovery requirement for explicit topic-scoped delegation and increases unsafe bypass risk.
  - **Diagnostics contract implications**:
    - Delegation failures should remain under `INTAKE_PERSISTENCE_BLOCKED` envelope but use specific primary code(s), for example `INTAKE_DELEGATION_EVIDENCE_MISSING` / `INTAKE_DELEGATION_EVIDENCE_INVALID`, with remediation naming the exact topic and missing field.
    - Success-path evidence should remain machine-auditable and script-verifiable (no narrative-only acceptance).
- **Risks**:
  - **Implicit bypass risk**: weak delegation wording could allow accidental pass-through. Mitigation: strict `satisfied_by=delegation_ref` literal + `ie:`-bound explicit user opt-in quote.
  - **Schema drift risk**: adding delegated fields in active scripts without template parity can regress installs. Mitigation: active/template parity checks and fixtures in sprint scope.
  - **Over-complexity risk**: introducing too many delegation fields may recreate friction. Mitigation: minimal bounded field set (`scope`, `rationale`, `confidence`) only.
  - **Downstream ambiguity risk**: delegated topics may be mistaken as resolved facts. Mitigation: explicit delegated marker retained in evidence and surfaced to architecture/sprint artifacts.
- **Research closure (2026-04-01T00:49:10Z, tech-lead, `orchestrator_run_id=auto-20260331-04`)**: bounded research complete for `US-0083`; proceed to `/architecture` to lock final delegation row schema, exact reason-code literals, and parity/regression matrix under canonical backlog authority.
- **Delivery closure (2026-04-01T01:15:55Z, curator, `orchestrator_run_id=auto-20260331-04`)**: `US-0083` is now `DONE` and sprint `S0064` is `released`; closure posture reconciled across backlog, acceptance, release queue, sprint summary, and resume brief during `/refresh-context`.
- **Linked**: US-0083, US-0068, US-0078, US-0045, DEC-0050, DEC-0060
- **Confidence**: high (direct validator/code-path review + external conditional-schema and audit-evidence references)
- **Status**: closed (`US-0083` `DONE`, `S0064` `released`; basis realized by `DEC-0067` / `# US-0083`)

## R-0063

- **Date**: 2026-04-03
- **Topic**: BUG-0004 - installer shell startup compatibility (`set: Illegal option -`)
- **Query**: What deterministic fix path should eliminate shell startup failure when `its-magic` invokes `installer.sh` through `sh`, while preserving installer parity and minimizing regression risk?
- **Sources**:
  - [Dash as /bin/sh portability notes](https://wiki.ubuntu.com/DashAsBinSh) (POSIX-shell compatibility constraints vs bash-specific options)
  - [POSIX Shell Command Language (`set` utility)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_25) (`set -e` portability baseline)
  - Internal: `bin/its-magic.js` (Unix path spawns `sh installer.sh`), `installer.sh` (line-2 startup option handling), `tests/run-tests.sh` (installer smoke paths under `sh`)
- **Findings**:
  - **Execution-path confirmation**: CLI currently invokes `installer.sh` via `spawnSync("sh", [installer,...])`; therefore script startup must remain valid for POSIX `sh` implementations (`dash`, `busybox sh`, etc.), not only `bash`.
  - **Defect mechanism**: startup options in shell scripts are sensitive to non-POSIX flags; `pipefail` or grouped option patterns that are valid in bash can fail immediately in `/bin/sh` environments with `set: Illegal option -`.
  - **Bounded fix alternatives**:
    - **A (recommended)**: keep `installer.sh` strictly POSIX-compatible (`set -e` baseline) and avoid bash-only `set` flags; preserves current CLI invocation contract (`sh installer.sh`).
    - **B**: force CLI to execute `bash installer.sh` and require bash at runtime. Rejected for portability and additional dependency assumptions in minimal Linux environments.
    - **C**: dual-path launcher with runtime shell detection and fallback. Higher complexity without clear benefit for this script.
  - **Regression expectations**: add explicit tests that run installer paths under `sh` for `missing` and `upgrade`, plus CLI path parity check (`node bin/its-magic.js --mode missing`) to prevent reintroduction.
- **Risks**:
  - **Portability regression**: introducing bash-only semantics in future edits can silently break non-bash shells. Mitigation: keep strict `sh` execution tests.
  - **Behavior drift**: changing CLI execution shell could diverge from documented/install test flow. Mitigation: preserve `sh` contract and codify in regression coverage.
  - **False confidence risk**: a single local shell can hide cross-shell failures. Mitigation: include deterministic smoke commands in shared test harness.
- **Research closure (2026-04-03T18:23:11Z, tech-lead, `orchestrator_run_id=auto-20260403-01`)**: bounded research complete for `BUG-0004`; proceed to `/architecture` to lock chosen portability contract and required regression matrix.
- **Linked**: BUG-0004, BUG-0005, US-0008, US-0018, US-0037, US-0045
- **Confidence**: high (direct execution-path inspection + POSIX shell references + existing test harness review)
- **Status**: closed (architecture accepted via `DEC-0068`; delivery completed in `S0065`)

## R-0064

- **Date**: 2026-04-03
- **Topic**: BUG-0005 — `/auto` resume continuity after bug intake (`RESUME_BRIEF_STALE` vs deterministic precedence)
- **Query**: How can `/intake bug` → `/auto` continue without a false stale-resume block while preserving explicit `start-from`, `resume_brief`, and `state.md` precedence and existing fail-fast safety contracts?
- **Sources**:
  - Internal: `.cursor/commands/auto.md` (deterministic resume-source precedence: `start-from` → `resume_brief` → `state.md` fallback; `RESUME_BRIEF_STALE` / unparseable fail-fast), `docs/engineering/auto-orchestration-reference.md` (expanded contract), `handoffs/intake_evidence/BUG-0005-intake-20260403.json`, `docs/product/backlog.md` (**BUG-0005**), **US-0045** (canonical status authority), **US-0070** / **DEC-0052** (phase plan materialization)
- **Findings**:
  - **Precedence vs `RESUME_BRIEF_STALE`**: When `resume_brief.md` is present and parseable but semantically stale relative to a newer backlog fact (e.g. bug persisted while brief still says `intended_resume_phase=intake` for a closed cycle), strict precedence forces the orchestrator to honor the brief and fail with `RESUME_BRIEF_STALE` rather than silently falling back to `state.md`. That is consistent with the documented “no silent fallback on stale brief” rule; the defect is a **handoff gap** (brief not refreshed at bug-intake boundary), not an argument for weakening fail-fast.
  - **Options to refresh `resume_brief` after bug intake** (architecture should pick one primary + explicit alternates):
    - **A (recommended default)**: On successful canonical bug intake persistence, the intake phase writer **prepends or atomically rewrites** `handoffs/resume_brief.md` with a deterministic template: `bug_id`, `intended_resume_phase=discovery` (or next valid phase for the bug lifecycle), `orchestrator_run_id` / boundary timestamp, and explicit `resolution_source` seed so the next `/auto` run resolves **`discovery`** without override.
    - **B**: Extend `/auto` with a **narrow self-heal** path: if `resume_brief` targets a phase inconsistent with **US-0045** OPEN bug rows and `state.md` last boundary agrees on the active `bug_id`, rewrite brief deterministically and continue — higher complexity and risk of masking operator edits; requires strict predicates and reason codes.
    - **C**: Document **operator-only** remediation (`/auto start-from=discovery` or manual brief edit). Acceptable as interim guidance but does not meet **BUG-0005** “no manual override for normal continuation.”
  - **Self-healing vs explicit fail-fast**:
    - **Fail-fast** remains correct when the brief is **unparseable**, **ambiguous**, or **conflicts** with authoritative backlog without a deterministic reconciliation rule (**US-0045** wins on status; brief cannot override DONE/OPEN facts).
    - **Self-heal** is only appropriate when reconciliation inputs are **machine-verifiable** (e.g. single unambiguous OPEN bug row + last `state.md` checkpoint + intake completion marker) and the heal action is **idempotent** and **audited** in `state.md`.
  - **Regression matrix (`/intake bug` → `/auto`)** (minimum scenarios for sprint/QA):
    | # | Scenario | Expected |
    |---|----------|----------|
    | 1 | Intake persists new OPEN bug; brief updated at intake boundary | `/auto` resolves next phase (`discovery` or policy-defined) without `RESUME_BRIEF_STALE` |
    | 2 | Intake persists bug; brief intentionally absent | `/auto` uses `state.md` fallback per precedence; no false stale |
    | 3 | Operator sets explicit `start-from` | Argument precedence; no stale brief error on valid phase |
    | 4 | Brief parseable but contradicts backlog (simulated corrupt handoff) | Fail-fast with deterministic code (`RESUME_BRIEF_STALE` or dedicated conflict code); no silent continue |
    | 5 | Portfolio switch: prior bug DONE, new bug OPEN | Brief points to new `bug_id` and phase; no carryover `intake` target |
- **Risks**:
  - **Over-broad self-heal** could hide real operator intent or race with parallel edits — mitigate with strict gates and breadcrumb logging.
  - **Intake writer scope creep** if intake must infer phase plans beyond bug lifecycle — mitigate by tying refresh to documented default next phase only and deferring profile/exclude logic to `/auto` materialization (**DEC-0052**).
  - **Dual-writer conflict** if curator and intake both rewrite `resume_brief` — mitigate with single canonical writer list in architecture.
- **Research closure (2026-04-03T19:42:00Z, tech-lead, `orchestrator_run_id=auto-20260403-02`)**: bounded research complete for **BUG-0005**; proceed to **`/architecture`** to lock chosen refresh/self-heal policy, DEC/handoff updates, and executable regression matrix.
- **Delivery closure (2026-04-03T23:55:00Z, curator, `orchestrator_run_id=auto-20260403-02`)**: **`BUG-0005`** is **DONE**; sprint **`S0066`** is **released**; normative lock-in realized via **`DEC-0069`**, **`docs/engineering/architecture.md`** **`# BUG-0005`**, and **`tests/intake_bug_resume_brief_bug0005_test.py`** (R-0064 matrix); curator **`/refresh-context`** reconciles research posture with delivery.
- **Linked**: BUG-0005, US-0037, US-0045, US-0070, US-0080
- **Confidence**: high (contract text + intake evidence + backlog scope alignment)
- **Status**: closed (delivered with **BUG-0005** / **S0066** / **DEC-0069**; see **`docs/engineering/state.md`** refresh-context checkpoint **`auto-20260403-02`**)

## R-0065

- **Date**: 2026-04-04
- **Topic**: BUG-0006 — `/auto` spawn-only enforcement, fail-fast reason codes, and regression shape
- **Query**: Where can `/auto` documentation imply direct orchestrator phase execution; what minimal enforcement and reason-code vocabulary satisfies US-0048 / US-0069 / US-0080; what test shape proves spawn-or-fail without claiming runtime product orchestration?
- **Sources**:
  - Internal: `.cursor/commands/auto.md`, `docs/engineering/auto-orchestration-reference.md`, `tests/auto_command_contract_test.py`, `handoffs/intake_evidence/BUG-0006-intake-20260403.json`, `docs/product/backlog.md` (**BUG-0006**), **DEC-0029**, **DEC-0038**, **DEC-0051** (`decisions/DEC-0038.md`, `decisions/DEC-0029.md` as applicable via index)
- **Findings**:
  - **Surfaces that must stay aligned (active + template parity where mirrored)**:
    - **Normative command**: `.cursor/commands/auto.md` — already states orchestrator-only scope and subagent spawning; fix should tighten **non-negotiable** spawn language, explicit **forbidden** pattern (“orchestrator must not write phase deliverables / perform phase role work”), and add **deterministic fail-fast reason codes** listed in-command and in the reference doc.
    - **Expanded contract**: `docs/engineering/auto-orchestration-reference.md` — carry the same spawn-only rule, cross-link isolation (**DEC-0029**) and strict-proof (**DEC-0038**) gates so operators cannot satisfy one artifact and ignore the other.
    - **Handoffs**: `handoffs/resume_brief.md` / `handoffs/po_to_tl.md` — optional short pointers only; canonical enforcement text stays in command + reference to avoid drift.
  - **Reason-code vocabulary (recommended)**:
    - **Primary (new, spawn boundary)**: introduce a dedicated code for attempted orchestrator-side phase work, e.g. `AUTO_ORCHESTRATOR_PHASE_EXECUTION` or `PHASE_SUBAGENT_SPAWN_REQUIRED`, documented beside existing **`PHASE_CONTEXT_ISOLATION_VIOLATION`** so diagnostics distinguish “wrong writer” from “missing spawn instruction.”
    - **Adjacent reuse (do not overload meaning)**: keep **`PHASE_CONTEXT_ISOLATION_*`**, **`RUNTIME_PROOF_*`**, **`PHASE_ROLE_*`**, **`PHASE_POLICY_*`** families as-is; BUG-0006 adds **spawn-attempt** coverage, not a replacement for isolation or proof failures.
    - **Resume/orchestration errors**: existing **`[AUTO_RESUME_ERROR]`** codes remain separate; spawn violation is a **phase-boundary integrity** failure, not resume precedence.
  - **Enforcement model (doc-first, test-backed)**:
    - **A (recommended)**: strengthen markdown contracts + extend **`tests/auto_command_contract_test.py`** (or sibling) with required substrings: e.g. explicit “spawn fresh subagent”, “orchestrator must not execute phase work”, and each new reason code literal. Matches repo pattern for DEC-0029/0038/0051/0052 markers.
    - **B**: standalone script in `scripts/` scanning command files. Heavier; only if contract grows beyond unittest readability.
    - **C**: behavioral test in a real Cursor runtime. Out of scope for this repository’s test harness; avoid claiming product runtime enforcement.
  - **Regression matrix (minimum)**:
    | # | Scenario | Expected |
    |---|----------|----------|
    | 1 | `.cursor/commands/auto.md` retains spawn-only + orchestration-only statements | Contract test **PASS** |
    | 2 | New spawn-violation reason code(s) present in slim `auto.md` and referenced from `auto-orchestration-reference.md` | Contract test **PASS** |
    | 3 | Template parity (if `template/` mirrors `auto.md`) | Parity check **PASS** (existing intake/template patterns as applicable) |
    | 4 | No contradictory language implying orchestrator may “run” `architecture`/`execute`/etc. in-process | Grep-based or negative assertion in contract test |
  - **Alternatives (“what’s the alternative?”)**:
    - **Weaken to advisory wording only** — rejected: fails intake acceptance (fail-fast + reason codes).
    - **Single file edit without tests** — rejected: high drift risk; **`auto_command_contract_test.py`** already establishes precedent.
- **Risks**:
  - **False precision**: reason codes that overlap **`PHASE_CONTEXT_ISOLATION_VIOLATION`** confuse operators — mitigate with one-line remediation text per code in `auto.md`.
  - **Template drift**: editing active `.cursor/commands/auto.md` without `template/` mirror — mitigate with parity tooling already used elsewhere.
  - **Scope creep into real orchestrator implementation** — mitigate: docs + static tests only; DEC-0038 proof tuples remain evidence of phase completion, not a runtime subagent launcher.
- **Research closure (2026-04-04T02:45:00Z, tech-lead, `orchestrator_run_id=auto-20260403-03`)**: bounded research complete for **BUG-0006**; proceed to **`/architecture`** to lock exact reason-code literals, reference-doc diff, and unittest assertions.
- **Delivery closure (2026-04-04T10:30:00Z, curator, `orchestrator_run_id=auto-20260403-03`)**: **`BUG-0006`** is **DONE**; sprint **`S0067`** is **released**; shipped via doc + test contract — **`docs/engineering/architecture.md`** **`# BUG-0006`**, active + template **`.cursor/commands/auto.md`**, **`docs/engineering/auto-orchestration-reference.md`** (**`AUTO_ORCHESTRATOR_PHASE_EXECUTION`**, **DEC-0029** / **DEC-0038** cross-links), **`tests/auto_command_contract_test.py`**; curator **`/refresh-context`** reconciles research posture with delivery.
- **Linked**: BUG-0006, US-0048, US-0069, US-0080, US-0045, DEC-0029, DEC-0038, DEC-0051, DEC-0052
- **Confidence**: high (contract + existing contract-test pattern + discovery asks)
- **Status**: closed (delivered with **BUG-0006** / **S0067**; see **`docs/engineering/state.md`** refresh-context checkpoint **`auto-20260403-03`**)

## R-0066

- **Date**: 2026-04-04
- **Topic**: BUG-0007 — false **`asked_topics`** / **`topic_coverage`** vs real chat (intake evidence truthfulness)
- **Query**: Why can intake evidence claim all **`small-intake-pack`** topics were asked and answered when the user reports no question round; where do validator and **`/intake`** contract fail to detect this; what minimal fail-closed guards and tests close the gap without breaking **`delegation_ref`** / **`equivalent_evidence_ref`** (**US-0083**)?
- **Sources**:
  - Internal: **`handoffs/intake_evidence/BUG-0007-intake-20260403.json`**, **`scripts/intake_evidence_validate.py`**, **`scripts/intake_evidence_lib.py`** (`validate_intake_evidence`), **`.cursor/commands/intake.md`** (US-0068 / US-0078 / DEC-0060), **`handoffs/po_to_tl.md`** (orchestrated discovery handoff — **BUG-0007**), **`docs/product/backlog.md`** (**BUG-0007**), **DEC-0060** (`ie:` ref binds **`quoted_user_text`** + metadata, not “question was posed”)
- **Findings**:
  - **Empirical validator gap (pre-delivery)**: `python scripts/intake_evidence_validate.py --file handoffs/intake_evidence/BUG-0007-intake-20260403.json` returned **`[INTAKE_EVIDENCE_VALIDATION_OK]`** (exit **0**) — the exemplar misleading bundle was **certified** before **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** shipped (**`S0068`** / **`BUG-0007`**). **Post-delivery**: the same file **FAIL**s with **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** under **`INTAKE_PERSISTENCE_BLOCKED`**.
  - **Root cause hypotheses** (not mutually exclusive; architecture picks primary + mitigations):
    1. **Semantic coverage vs syntactic coverage**: **`intake_evidence_lib.validate_intake_evidence`** enforces pack keys present, **`ie:`** hash match to **`quoted_user_text`**, **`asked_topics`** membership (unless **`evidence_source=equivalent_evidence_ref`**), and delegation fields — it does **not** require distinct answers per topic, user-visible **question** text, or correlation between **`turn_index`** and an actual Q/A pair in chat.
    2. **Authoring shortcut**: PO workflow can populate **`asked_topics`** with the full required set and reuse the same (or near-duplicate) **`quoted_user_text`** across rows as **`answer_ref`**, producing internally consistent hashes while misrepresenting elicitation.
    3. **Binding limit of `ie:`**: DEC-0060 digest covers **`intake_run_id`**, **`turn_index`**, **`topic_key`**, **`satisfied_by`**, **`quoted_user_text`** — it proves payload consistency, not that **`quoted_user_text`** is an answer to the canonical prompt for **`topic_key`** nor that a prompt occurred.
    4. **Low-touch / bug path pressure**: **`/intake bug`** may emphasize backlog persistence speed; without hard validator rules, agents align fields to pass the gate rather than to mirror chat.
  - **Validator / command surfaces** (where to implement — architecture decides scope split):
    - **`scripts/intake_evidence_lib.py`**: add deterministic rules under existing umbrella **`INTAKE_PERSISTENCE_BLOCKED`** (new subcodes TBD by DEC), e.g. (a) for **`satisfied_by=answer_ref`**, reject identical **`quoted_user_text`** across multiple required-topic rows unless **`equivalent_evidence_ref`** is used; (b) optional **`question_prompt_ref`** / **`question_text`** field required for **`answer_ref`** rows; (c) heuristics that **`quoted_user_text`** must not equal a single prior “umbrella” bug report blob for every key — bounded false-positive risk, document in architecture.
    - **`scripts/intake_evidence_validate.py`**: unchanged CLI contract (`--file`, `--stdin`, `--self-test`); failures continue stderr + exit **1**.
    - **`.cursor/commands/intake.md`**: tighten normative text — **`asked_topics`** may list only topics for which a user-visible question (or allowed alternate) exists; forbid fabricating Q/A alignment pre-validator.
    - **`scripts/intake_bug_resume_brief_refresh.py`** / **`bug_issue_validate.py`**: optional cross-check that intake evidence file exists and validator **PASS** before claiming intake complete (architecture: avoid duplicate validation sources of truth).
  - **Fail-closed reason codes (recommended vocabulary; architecture locks names)** — all under umbrella **`INTAKE_PERSISTENCE_BLOCKED`** unless DEC chooses split:
    - **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** (or **`INTAKE_SYNTHETIC_ANSWER_REF`**) — duplicate / non-distinct **`quoted_user_text`** across **`answer_ref`** rows for distinct **`topic_key`** without **`equivalent_evidence_ref`**.
    - **`INTAKE_ASKED_TOPIC_NOT_EVIDENCED`** — **`asked_topics`** includes a key without a matching prompt artifact / question binding (if architecture adds **`question_*`** fields).
    - **`INTAKE_TOPIC_COVERAGE_CHAT_MISMATCH`** — reserved if future external transcript binding is introduced (optional; higher complexity).
    - Reuse existing: **`INTAKE_REQUIRED_TOPIC_MISSING`**, **`INTAKE_DELEGATION_EVIDENCE_*`**, **`INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`** — do not overload for BUG-0007-specific semantics.
  - **Regression / test matrix** (minimum):
    | # | Scenario | Expected |
    |---|----------|----------|
    | 1 | Fixture clone of **`BUG-0007-intake-20260403.json`** (duplicate prose **`answer_ref`** across keys) | Validator **FAIL** with deterministic subcode after guard lands |
    | 2 | Legitimate five distinct short answers + valid **`ie:`** refs | **PASS** |
    | 3 | **`satisfied_by=delegation_ref`** with complete delegation metadata + valid ref | **PASS** (no regression vs **US-0083** / **R-0062**) |
    | 4 | **`evidence_source=equivalent_evidence_ref`** + **`equivalent_evidence_ref`** on row; topic omitted from **`asked_topics`** per lib rules | **PASS** |
    | 5 | **`assumption_confirmation_ref`** path for assumptions | **PASS**; distinct from **`answer_ref`** abuse |
    | 6 | Active + **`template/`** parity for any **`intake.md`** / lib / installer mirror changes | Parity script **PASS** |
    | 7 | **`python scripts/intake_evidence_validate.py --self-test`** after lib change | **PASS** |
- **Risks**:
  - **False positives** if legitimate user pastes the same short answer twice — mitigate with duplicate detection scoped to “same blob across all pack keys” or minimum length / entropy thresholds (architecture-bounded).
  - **False sense of security** if only duplicate-text rule is added — deeper fix may require explicit **question** artifact or transcript binding; document residual risk in architecture.
  - **Divergence** between “validator truth” and PO behavioral honesty — mitigate with contract tests + intake command wording.
- **Alternatives**:
  - **Doc-only reminder** — rejected: validator already **PASS**es on the defect exemplar.
  - **External chat log ingestion** — likely out of scope for repo; defer unless product mandates it.
- **Research closure (2026-04-04T14:30:00Z, tech-lead, `orchestrator_run_id=auto-20260404-01`)**: bounded research complete for **BUG-0007**; proceed to **`/architecture`** to lock schema deltas, exact subcodes, grandfathering, and unittest/fixture paths.
- **Delivery closure (2026-04-05T01:30:00Z, curator, `orchestrator_run_id=auto-20260404-01`)**: **`BUG-0007`** is **DONE**; sprint **`S0068`** is **released**; shipped via **`scripts/intake_evidence_lib.py`** (**`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** + **US-0083** exemptions), active + **`template/`** **`.cursor/commands/intake.md`**, **`tests/intake_evidence_bug0007_r0066_test.py`**; curator **`/refresh-context`** reconciles research posture with delivery (**`handoffs/releases/S0068-release-notes.md`**, **`docs/engineering/state.md`** refresh-context checkpoint).
- **Linked**: BUG-0007, US-0068, US-0078, US-0079, US-0083, DEC-0060, DEC-0069, R-0062, R-0055
- **Confidence**: high (reproducible pre-ship validator gap on misleading JSON + code review of **`validate_intake_evidence`**; post-ship exemplar **FAIL** closed the gap)
- **Status**: closed (delivered with **BUG-0007** / **S0068**; see **`docs/engineering/state.md`** refresh-context checkpoint **`auto-20260404-01`**)

## R-0067 — US-0084: POSIX npm `installer.sh`, CRLF/LF, publish parity, remote test ergonomics (WSL / SSH / Docker)

- **Date**: 2026-04-04
- **Topic**: **US-0084** — reliable global **`its-magic`** install under Debian **`/bin/sh`** (often **dash**); automatable Linux remote test targeting aligned with **US-0064** / **`release-targets.json`**
- **Query**: What does the repo guarantee today for **`installer.sh`** startup vs published npm payload; how to guard **CRLF** and bash-only **`set`** regressions; how should dev/QA map **WSL**, bare **SSH**, and **Docker-over-SSH** to existing connectivity artifacts without a second schema; what helper + harness hooks close **AC-2** / **AC-5** / **AC-10**?
- **Sources**:
  - Internal: **`installer.sh`** (lines **1–5** unconditional startup; **`bin/its-magic.js`** **182–195** spawns **`sh`** + path to **`installer.sh`** on non-Windows); **`package.json`** **`files`** ( **`installer.sh`**, **`template/`**, etc. — no duplicate **`template/installer.sh`**); **`tests/installer_shell_bug0004_test.py`** (forbidden **`set -euo`** / **`pipefail`** strings + **`sh`** smoke + CLI); **`tests/run-tests.sh`** / **`tests/run-tests.ps1`** (installer sections ~**134–215**, **§26** Python installer tests); **`.cursor/scratchpad.md`** **`REMOTE_EXECUTION`**, **`REMOTE_CONFIG`**; **`docs/engineering/release-targets.json`** (**`ssh-server`**, **`dockerOverSsh`**); **`docs/engineering/runtime-connectivity.md`**; **`handoffs/po_to_tl.md`** (**US-0084**), **`docs/product/backlog.md`** (**US-0084** **discovery_notes** **`auto-20260404-02`**)
  - External: [Baeldung — Illegal option `-o pipefail` under `sh`/dash](https://www.baeldung.com/linux/illegal-option-o-pipefail) (bash-only options fail when **`/bin/sh`** is **dash**); [POSIX / dash portability discussions](https://stackoverflow.com/questions/54055549/linux-ubuntu-set-illegal-option-o-pipefail) (same failure mode class as reported **`set: Illegal option -`**)
- **Findings**:
  - **POSIX / `set` audit (repo path)**: Active **`installer.sh`** uses **`#!/usr/bin/env sh`** and a single unconditional **`set -e`** at **line 2**, with an explicit **BUG-0004** guard comment at **lines 4–5** — no **`set -u`**, **`pipefail`**, or other bash-only bundles on the startup path. **`grep '^set '`** yields only **`set -e`**. This matches the failure hypothesis in intake (**bash-only flags** and/or **CRLF**): repo source is already on the “safe” side for **`set`**.
  - **Published vs repo path**: **`package.json`** publishes **`installer.sh`** at package root (not under **`template/`**). There is **no** **`template/installer.sh`** in-repo; consumers get the same file listed in **`files`**. **Drift risk** is therefore **npm pack content vs git HEAD** (wrong version published, CRLF checked in on Windows, or manual edit without CI), not two divergent tree copies — unless future work adds a mirrored copy (then parity rules apply).
  - **CRLF / LF**: Shebang + CRLF can produce confusing parse errors; a stray carriage return before newline can make **`set`** see odd tokens. **Mitigations for architecture**: **`.gitattributes`** `*.sh text eol=lf` (if not already), **`npm` prepublish** or **CI** step: reject **`\r`** in **`installer.sh`** (and any future packaged **`*.sh`**), or run **`file`** / **`od`** / small Python check; document **`dos2unix`** in runbook (**AC-3**).
  - **CI / prepublish hooks**: Existing **`tests/installer_shell_bug0004_test.py`** blocks reintroduction of **`set -euo`** / **`pipefail`** substrings and runs **`sh`** + **`node … its-magic.js`** smokes — it does **not** run **`dash -n`** or parse-check under **`dash`** explicitly. **Recommendation**: add **`dash -n installer.sh`** (and **`template/`** copies if added) when **`dash`** is on **`PATH`** (CI matrix or optional skip), or document equivalent; keep **Python** test for token guard so Windows devs without **dash** still get signal. **`prepublishOnly`** script can call the same check for defense in depth vs tarball-only mistakes.
  - **US-0064 / `release-targets.json` alignment**: Canonical **`ssh-server`** target (**lines 92–121**) already exposes **`hostEnv`**, **`userEnv`**, **`authEnv`**, **`remoteCommand`**, **`runtime`**, and optional **`dockerOverSsh`** (**`dockerHostEnv`**, **`dockerContextEnv`**, **`composeFile`**, **`service`**). **WSL** is a **local Linux kernel** path (operators run **`sh`/`dash`** there against the same repo — not a **`release-targets`** row by default); **bare SSH** maps to **`ssh-server`** env indirection; **Docker-over-SSH** maps to **`dockerOverSsh`** fields + operator **`DOCKER_HOST`** / context docs — **no new JSON schema** needed; docs should cross-link **`runtime-connectivity.md`** operator summary template (**`docker_over_ssh`** bullet at **lines 26–27**).
  - **Scratchpad**: **`REMOTE_EXECUTION=0`** default (**`.cursor/scratchpad.md`** **104–108**); **`REMOTE_CONFIG=.cursor/remote.json`** — helper should read that path (or override), validate JSON shape **against documented US-0064 patterns** (not invent keys), and **refuse** to print secret **values** (**AC-7**).
  - **Suggested helper interface (architecture locks details)**: e.g. **`scripts/validate_remote_config.py`** or **`scripts/remote_config_summary.sh`** — args: **`--config`** defaulting from env or **`REMOTE_CONFIG`**; stdout: **target label**, **host** (env name + resolved presence only if safe), **user** env name, **identity file path reference** (path string allowed if it is a non-secret path like **`~/.ssh/id_ed25519`** — never file contents); stderr: reason. **Exit codes (suggested)**: **0** OK; **1** usage; **2** file missing / unreadable; **3** invalid JSON; **4** schema / required-field mismatch vs **US-0064** doc; **5** **`REMOTE_EXECUTION=0`** no-op fast exit (optional — architecture decides whether helper always runs or only when remote on).
  - **Test harness**: Register helper success/failure fixtures beside **`tests/installer_shell_bug0004_test.py`** in **`tests/run-tests.sh`** / **`.ps1`** (mirror **§26** style); add **`dash -n`** gate in same harness or extend **BUG-0004** test module so **AC-2** / **AC-10** stay single-entrypoint for **`/qa`**.
- **Open questions / risks (for architecture)**:
  - Whether **CI** runners guarantee **`dash`** availability vs **`busybox sh`** only — affects **skip vs hard** requirement.
  - **`prepublishOnly`** vs **GitHub Actions only** — npm maintainers publishing from Windows without local **dash** need a **Python-only** CRLF / forbidden-token check at minimum.
  - Helper **vs** documented one-liner — scope control to avoid duplicating **`runtime-connectivity.md`** maintenance.
  - **Secret leakage** in debug logs when printing “resolved” env vars — architecture should mandate **names-only** or **boolean present** flags.
- **Alternatives**:
  - **Bash-only installer** with **`#!/usr/bin/env bash`** — rejected by **AC-1** / product stance (**`/bin/sh`** global npm path).
  - **New remote schema file** — rejected; extend docs + helper around **US-0064** only.
- **Research closure (2026-04-04T16:00:00Z, tech-lead, `orchestrator_run_id=auto-20260404-02`)**: bounded research complete for **US-0084**; architecture locked in **`docs/engineering/architecture.md`** **`# US-0084`** (POSIX/LF, **`scripts/guard_installer_publish.py`**, **`scripts/remote_config_summary.py`**, harness **H1–H5**, **`DEC-0070`**).
- **Delivery closure (2026-04-05T01:30:00Z, curator, `orchestrator_run_id=auto-20260404-02`)**: **US-0084** is **DONE**; sprint **S0069** is **released**; shipped via **`.gitattributes`**, **`scripts/guard_installer_publish.py`** + **`package.json`** **`prepublishOnly`**, extended **`tests/installer_shell_bug0004_test.py`**, **`scripts/remote_config_summary.py`** + **`tests/remote_config_summary_test.py`** + fixtures, **`docs/engineering/runbook.md`**, **`runtime-connectivity.md`**, **`us-0084-remote-e2e.md`**, normative **`decisions/DEC-0070.md`**; curator **`/refresh-context`** reconciles research posture with delivery (**`handoffs/releases/S0069-release-notes.md`**, **`sprints/S0069/release-findings.md`**, **`docs/engineering/state.md`** refresh-context checkpoint).
- **Linked**: US-0084, US-0064, US-0036, BUG-0004, DEC-0070, R-0058 (intake template context)
- **Confidence**: high (repo **`installer.sh`** / CLI spawn path; **S0069** ships **LF**/forbidden-token publish guard, optional **`dash -n`**, and remote helper + harness coverage)
- **Status**: closed (delivered with **US-0084** / **S0069**; see **`docs/engineering/state.md`** refresh-context checkpoint **`auto-20260404-02`**)

## R-0068 — US-0086: automation remote execution selection (Docker / SSH / NL container intent)

- **Date**: 2026-04-04
- **Topic**: **US-0086** — scratchpad-gated **automation profile** so dev/CI/DI/QA/release can pick **Docker** vs **SSH** vs local using **`.cursor/remote.json`** / **US-0064** semantics; explicit **“start container \<id\>”** resolves to **`targets[].id`**; manual operators stay default-off.
- **Query**: What does the repo guarantee today for **agent/CI** routing vs a single **`TEST_COMMAND`**; where should policy live; how to avoid silent remote reroute when **`REMOTE_EXECUTION=0`**?
- **Sources**:
  - Internal: **`.cursor/scratchpad.md`** **`REMOTE_EXECUTION`**, **`REMOTE_CONFIG`**; **`scripts/remote_config_summary.py`**; **`docs/engineering/runtime-connectivity.md`**; **`docs/product/backlog.md`** **US-0084** / **US-0085** / **US-0064**; intake evidence **`handoffs/intake_evidence/US-0086-intake-20260404.json`**
- **Findings**:
  - **No path-based CI matrix or agent auto-target selection** ships today beyond **remote config validation** and **documented** operator flows (**US-0084**).
  - **Architecture** should lock **scratchpad key names** for an **automation profile** (distinct from manual **`REMOTE_EXECUTION`**), document **heuristics** (changed files, explicit NL intent), and **fail-closed** codes for unknown target ids.
  - **Composition with US-0085**: automation may use **env already in process**; **must not** read **`.env`** or print secrets.
- **Open questions (for `/architecture`)**: exact flag names; optional CI snippet scope; minimal unittest surface vs doc-only matrix.
- **Discovery extension (2026-04-13T18:30:00Z, po, `orchestrator_run_id=auto-20260405-01`, `fresh_context_marker=po-US0086-discovery-20260413T183000Z-fresh`)**:
  - **Mode split reaffirmed**: remote target selection remains **automation-only**; manual path stays default local/no-reroute.
  - **Intent contract**: explicit phrase **"start container `<target_id>`"** must resolve against canonical **`targets[].id`** and fail closed on unknown/disabled target.
  - **Research asks for `/research`**: lock deterministic routing heuristics (changed file classes + explicit intent), define evidence tuple for remote-run handoffs (`target_id`, `environment_label`, `automation_profile`), and enumerate reason-code names for unknown/disabled/mode-off routing cases.
  - **Security continuity**: align with **US-0085** delivered posture (names-only outputs, no `.env` reads, no secret echo in logs/handoffs).
- **External references (research phase, 2026-04-13)**:
  - GitHub Actions workflow syntax (`paths` / `paths-ignore`): [https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
  - Docker contexts (`docker context use`, `DOCKER_CONTEXT`, `--context`): [https://docs.docker.com/engine/manage-resources/contexts/](https://docs.docker.com/engine/manage-resources/contexts/)
  - OpenSSH client config (`Host` matching order, `CanonicalizeFallbackLocal`, `StrictHostKeyChecking`): [https://man7.org/linux/man-pages/man5/ssh_config.5.html](https://man7.org/linux/man-pages/man5/ssh_config.5.html)
- **Research extension (2026-04-13T19:00:00Z, tech-lead, `orchestrator_run_id=auto-20260405-01`, `fresh_context_marker=tl-US0086-research-20260413T190000Z-fresh`)**:
  - **Deterministic routing matrix (recommended for `/architecture` lock)**:
    - **Mode off** (`REMOTE_EXECUTION=0` or automation profile unset): always local; if explicit NL target is requested, return fail-closed mode-off reason.
    - **Explicit NL intent first**: phrase `start container <target_id>` resolves to exact `targets[].id`; unknown/disabled target fails closed.
    - **Heuristic fallback when automation mode is on**: changed files matching container surfaces (`Dockerfile*`, `docker-compose*.yml`, container runtime scripts) suggest Docker target; SSH deployment/runtime scripts suggest SSH target; otherwise local.
  - **Reason-code candidates** (names to be architecture-locked): `REMOTE_AUTOMATION_MODE_OFF`, `REMOTE_TARGET_UNKNOWN`, `REMOTE_TARGET_DISABLED`, `REMOTE_TARGET_UNROUTABLE`.
  - **Evidence tuple contract** for execute/qa/release handoffs and state breadcrumbs: `target_id`, `environment_label`, `automation_profile`, `routing_source` (`explicit_intent|heuristic|local_default`), `secret_surface=names_only`.
  - **External-source takeaways applied to US-0086**:
    - GitHub docs confirm path filters are deterministic and AND-composed with branch filters, supporting stable CI routing when file classes are declared explicitly.
    - Docker docs confirm deterministic context selection precedence (`--context` override, then `DOCKER_CONTEXT`, then active context), which maps cleanly to target-id-first automation behavior.
    - OpenSSH docs confirm host-specific first-match ordering and fail-fast controls (`CanonicalizeFallbackLocal no`, `StrictHostKeyChecking yes`) for safe SSH target resolution.
  - **Alternatives considered**:
    - **Single fixed remote target**: simplest implementation, but rejected because AC-4 requires explicit target-id resolution and AC-6 requires deterministic CI/routing behavior.
    - **Always-remote when automation enabled**: rejected; violates manual-local expectations and increases blast radius for unknown/misconfigured targets.
    - **Doc-only guidance with no reason codes**: rejected; not testable and not fail-closed.
  - **Risks**:
    - Drift between active and `template/` heuristics/rules could cause inconsistent routing outcomes.
    - Over-broad path filters can route local-only work to remote contexts unexpectedly.
    - Missing explicit reason-code wiring can blur mode-off vs unknown-target failures.
- **Linked**: US-0086, US-0085, US-0084, US-0064, DEC-0070
- **Confidence**: high (intake + discovery + research + delivered implementation evidence)
- **Status**: closed -- delivery aligned with **US-0086** **DONE** (**US-0045**) / curator **`/refresh-context`**
- **Delivery closure (2026-04-13T23:00:00Z, curator, `orchestrator_run_id=auto-20260405-01`)**: **`US-0086`** **DONE**; sprint **`S0074`** **released**; automation-driven remote execution selection contract delivered per **`docs/engineering/architecture.md`** **`# US-0086`** with routing reason codes and handoff/state evidence tuple expectations reconciled in the hot-surface artifacts.

## R-0069 — BUG-0008: CRLF `installer-owned-paths.manifest` breaks POSIX `awk` section headers

- **Date**: 2026-04-04
- **Topic**: **BUG-0008** — npm global install on Linux: **`[INSTALL_MANIFEST_ERROR] install_include_paths section is empty`**
- **Query**: Why does the manifest show paths but the shell installer sees an empty section?
- **Sources**:
  - Internal: **`installer.sh`** **`get_manifest_paths`** (strict **`awk`** section header equality on `$0`); operator **`cat -A`** evidence (**`^M$`**); **`.gitattributes`** (pre-fix: **`*.sh`** LF only, **US-0084**); **`template/docs/engineering/context/installer-owned-paths.manifest`**
- **Findings**:
  - **Root cause**: CRLF line endings → section header line is **`[install_include_paths]\\r`**; **`awk`** equality fails; no lines attributed to section.
  - **Mitigations**: strip trailing **`\\r`** per line before matching; enforce **`*.manifest text eol=lf`**; extend **`guard_installer_publish.py`** to reject **`\\r`** in both active and template manifest paths; **PowerShell** **`Get-ManifestSection`**: trim carriage return before **`Trim()`**.
- **Linked**: BUG-0008, US-0084
- **Confidence**: high (repro evidence on **`its-magic@0.1.2-40`**)
- **Status**: delivery closed — **`BUG-0008`** **DONE**; **`S0070`** **`released`** (`2026-04-05T22:30:00Z`, `handoffs/releases/S0070-release-notes.md`); in-repo mitigations **`0.1.2-41`**; Debian operator E2E deferred **`DEFERRED_DEBIAN_E2E_NO_RUNTIME`** (documented waiver).

## R-0070 — US-0087: `/auto` bug-targeted continuation vs story backlog drain

- **Date**: 2026-04-04
- **Topic**: **US-0087** — explicit **`/auto`** modes **fix all OPEN bugs** / **fix `BUG-####`**
- **Query**: How does resume precedence (**`start-from`**, **`resume_brief`**, **`state.md`**) interact with **`AUTO_BACKLOG_DRAIN`** (**story-only** wording in **`auto-orchestration-reference.md`**) and **`DEC-0069`** single-bug **`resume_brief`** refresh?
- **Sources**:
  - Internal: **`.cursor/commands/auto.md`**; **`docs/engineering/auto-orchestration-reference.md`** (**Optional backlog-drain** §, **Inputs**, **Deterministic resume-source precedence**, **AC-10** phase boundary visibility, reason-code baseline); **`handoffs/resume_brief.md`** patterns; **`DEC-0069`**; **`US-0044`** / **`DEC-0022`**; **`US-0070`** / **`DEC-0052`**; **`US-0079`** / **`DEC-0061`**; **`handoffs/po_to_tl.md`** (**US-0087** discovery handoff); **`tests/auto_command_contract_test.py`**
- **Findings** (intake-era baseline retained):
  - **Gap**: no first-class **bug id** selector on **`/auto`** today; **`AUTO_BACKLOG_DRAIN`** text refers to **OPEN story** selection only.
  - **Architecture must lock**: mutual exclusion or strict precedence when both story drain and bug-target mode could apply; per-segment **`bug_id`** in **`state.md`** / **`resume_brief`** for multi-bug queues; deterministic **fail-closed** when **`BUG-####`** not **OPEN** or unknown.
- **Line-level doc inventory (architecture delivery targets)** — paragraphs/sections to extend for bug-target precedence and **`AUTO_BACKLOG_DRAIN`** interaction:
  - **`.cursor/commands/auto.md`**: compact **Inputs** / **Outputs** / **Steps 1–9** (no bug-queue keys today); **Optional backlog-drain** stub (points to reference only); **Deterministic resume-source precedence** + **`start-from`** (must document bug-target argv and conflict with story drain); **Fail-fast** codes may need bug-scheduler siblings; **Configurable phase selection** cross-reference (**`DEC-0052`**) unchanged in shape but bug segments need **`bug_id`** in breadcrumbs.
  - **`docs/engineering/auto-orchestration-reference.md`**: **`## Inputs`** (add merged scratchpad keys for bug queue + explicit argv tokens); **`## Optional backlog-drain mode`** (**§337–361**) — adjacent or mirrored **`## Optional bug-queue mode`** with **one active scheduler** rule vs **`AUTO_BACKLOG_DRAIN=1`**; **`## Deterministic resume-source precedence`** (**§493+**) — clarify whether bug-target argv outranks scratchpad bug keys and how **`resume_brief`** **`bug_id`** participates; **`### Phase boundary operator visibility (AC-10)`** (**§281–290**) — extend tuple (see below); **Reason-code baseline** (**§436–474**) — add **`AUTO_BUG_*`** / queue-empty / unknown-id / not-open / scheduler-conflict codes (**names architecture-locked**).
  - **`template/`** mirrors: per **AC-10** parity, same paths as active (**`template/.cursor/commands/auto.md`**, **`template/docs/engineering/auto-orchestration-reference.md`**, scratchpad examples).
  - **`tests/auto_command_contract_test.py`** (or successor): add fixture tokens for bug-target argv spellings and **`AUTO_BACKLOG_DRAIN` + bug mode** conflict marker per **AC-7** (without weakening **BUG-0006** spawn-only strings).
- **`DEC-0069` / `BUG-0005` composition (multi-bug queue)**:
  - Post-**`/intake bug`**, **`resume_brief`** must describe the **next** runnable boundary with a **non-stale** **`intended_resume_phase`** and consistent **`bug_id`** (**US-0045** authority).
  - **Fix-all** queue: after each bug’s terminal **`refresh-context`** (or explicit segment stop), the **next** segment needs a **refreshed** brief (or deterministic **`state.md`**-authoritative cursor) so **`/auto`** without **`start-from`** does not trip **`RESUME_BRIEF_STALE`** while lawful bug-target continuation is intended.
  - Recommend architecture record: **`bug_queue_cursor`** (e.g. ordinal / remaining ids), **`segment_work_item_kind=bug|story`**, and **`story_id`** when the portfolio driver is a **US** (e.g. meta **US-0087**) vs **`bug_id`** when executing a defect lifecycle.
- **Candidate scratchpad / argv shape (for architecture to lock; not normative here)**:
  - Enable + cap: e.g. **`AUTO_BUG_DRAIN`** **`0|1`**, **`AUTO_BUG_MAX_ITEMS`**, **`AUTO_BUG_ON_BLOCK`** **`stop|skip`** (parallel to **`AUTO_BACKLOG_*`**).
  - Target selection: explicit **`/auto`** argv **architecture-locked** (**AC-1**) plus optional scratchpad mirror; single id vs **all OPEN** enumerated from **`docs/product/backlog.md`** **`## Bug issues (canonical)`** ascending numeric id (**AC-4** / **US-0079**).
- **Fail-closed reason codes (candidates for `# US-0087` matrix)** — separate from **`PHASE_POLICY_CONFLICT`** unless architecture collapses:
  - **Empty queue**: **`AUTO_BUG_QUEUE_EMPTY`** (or locked equivalent).
  - **Unknown / malformed id**: **`AUTO_BUG_TARGET_UNKNOWN`**.
  - **Not OPEN / DONE**: **`AUTO_BUG_TARGET_NOT_OPEN`**.
  - **Scheduler clash** (bug mode + **`AUTO_BACKLOG_DRAIN=1`** without resolution): **`AUTO_SCHEDULER_CONFLICT`** or explicit **precedence table** with a single winning mode (**AC-3**).
- **`AC-10` breadcrumb extensions** when **`story_id=US-0087`** (portfolio driver) vs active bug work:
  - Always record **`orchestrator_run_id`**, **`phase_boundary`**, **`next_scheduled_phase`**.
  - Add **`segment_work_item_kind`**, **`active_bug_id`** (or **`bug_id=(none)`** during meta-story-only segments), optional **`bug_queue_remaining`** / **`bug_queue_position`**, and **`backlog_drain_mode`** vs **`bug_drain_mode`** booleans so operator visibility matches **US-0044** vs **US-0087** without ambiguous double scheduling.
- **Risks**:
  - **Double scheduling** if both story drain and bug queue are “on” without a hard winner.
  - **`RESUME_BRIEF_STALE`** regressions if multi-bug segments do not refresh **`resume_brief`** at lawful boundaries (**`BUG-0005`** lineage).
  - **Reason-code drift** between **`auto.md`**, reference, **`architecture.md` `# US-0087`**, and tests.
  - **Template drift** if **`template/`** parity lags active command/reference (**AC-10**).
- **Dependencies**: **US-0070** (**`DEC-0052`** phase plan per segment), **US-0044** / **`DEC-0022`**, **DEC-0069**, **US-0079** / **`DEC-0061`** bug section authority, **BUG-0006** / **US-0069** spawn-only (unchanged).
- **External references**: N/A (repo-normative orchestration contracts only).
- **Alternatives** (for architecture):
  - **Bug drain as a profile of backlog drain** — rejected for clarity: story vs bug selection rules differ (**OPEN** stories vs **OPEN** bugs, sort keys, max items); keep **one scheduler** explicit.
  - **State-only bug cursor without `resume_brief` updates** — risky vs **`RESUME_BRIEF_STALE`**; prefer paired updates or documented exception path.
- **Linked**: US-0087, US-0044, DEC-0022, DEC-0069, BUG-0005, US-0070, DEC-0052, US-0079, DEC-0061, BUG-0006, US-0069, R-0065
- **Confidence**: high (shipped **2026-04-12** with **`S0071`** / **`US-0087`** **DONE**; findings above remain historical survey + architecture lock-in traceability)
- **Research extension (2026-04-06T15:00:00Z, tech-lead, `orchestrator_run_id=auto-20260405-01`, `fresh_context_marker=tech-lead-US0087-research-20260406T150000Z-fresh`)**: concrete doc inventory, **`DEC-0069`** queue composition notes, candidate flags/codes, **`AC-10`** tuple extensions — **closure for `/research`**; **`/architecture`** next.
- **Delivery closure (2026-04-12T20:35:00Z, curator, `orchestrator_run_id=auto-20260405-01`)**: **`US-0087`** **DONE**; sprint **`S0071`** **released**; bug-queue + mutex contract delivered per **`architecture.md`** **`# US-0087`** and static tests — **R-0070** objectives satisfied; **`US-0088`** / **`R-0071`** is the active forward research stub.
- **Status**: closed — delivery aligned with **US-0087** **DONE** (**`US-0045`**) / curator **`/refresh-context`**

## R-0071 — US-0088: continuous `/auto` loop vs one-phase-stop + drain reliability

- **Date**: 2026-04-12
- **Topic**: **US-0088** — multi-phase **`/auto`** until US/sprint boundary; quiet operator surface with **`AUTO_BACKLOG_DRAIN=1`**; harden early-stop and drain advance
- **Query**: Where does normative **Step 5** in **`docs/engineering/auto-orchestration-reference.md`** diverge from typical Cursor **one subagent spawn per `/auto`** behavior, and what contract tests best lock **continuation**?
- **Sources**:
  - Internal: **`docs/engineering/auto-orchestration-reference.md`** (**`## Steps`** item **5** — per-phase spawn loop, drain, bug-queue, security-review hooks); **`.cursor/commands/auto.md`** (**`## Steps (compact; full detail in reference)`**); **`docs/engineering/runbook.md`** (operator recipes); **`US-0044`** / **`DEC-0022`**; **`US-0037`**; **`DEC-0069`**; **`US-0069`** / **`DEC-0051`**; **`tests/auto_command_contract_test.py`**
  - External (**EARLY_RESEARCH**): attempted web lookup for general multi-agent supervisor/worker loop patterns — **unavailable** this session; analog is **supervisor schedules discrete worker runs until a global stop** (industry pattern name only; no URL persisted).
- **Findings** (line-level — **Step 5 vs compact Steps drift**):
  - **Numbering misalignment (high leverage)**: In **`auto-orchestration-reference.md`**, **`## Steps`** uses a numbered list where **item 5** is the **normative multi-phase spawn block** (“Spawn a fresh subagent for each remaining phase in the intersected resolved schedule order…”) including **`AUTO_BACKLOG_DRAIN=1` → repeat story lifecycle**, bug-queue iteration, bulk execute, team checks, and **US-0069** pre/post role gates. In **`.cursor/commands/auto.md`**, the compact list maps differently: **step 4** = “Spawn fresh subagents per intersected schedule” and **step 5** = “Implementation loop, pause, stop breadcrumbs… — reference.” Readers who say “**Step 5**” without naming the file will **equate the wrong bullets** — a direct contributor to **one-phase-stop** mis-implementation.
  - **Compression gap**: Compact **step 5** delegates the entire **per-phase iteration**, **implementation loop** (**reference** step 7), pause (**step 8**), stop reasons (**step 9**), and **resume_brief** (**step 10**) to “implementation loop” prose. That is **correct by reference** but **under-specified for Cursor** unless the normative reference block is treated as mandatory reading; **`/architecture`** should either (a) add **non-ambiguous cross-file anchors** (e.g. stable fragment ids / explicit “reference Steps 5–11”) in **`auto.md`**, or (b) accept a **documented outer-driver** pattern (operator re-invokes **`/auto`** with **`start-from`** / fresh resume) with deterministic equivalence — **AC-1** decision gate.
  - **Normative multi-phase text (reference Step 5 — excerpt targets)**: Sub-bullets under item **5** explicitly require **each phase in intersected order**, **reload + recompute phase plan at story boundary** when **`AUTO_BACKLOG_DRAIN=1`**, and parallel **bug-queue** / **bulk** iteration rules — these are the **minimum strings / semantics** contract tests should **anchor**, not only “spawn-only” literals (already covered by **`tests/auto_command_contract_test.py`**).
  - **runbook gap (research scope)**: Runbook must state **continuous** vs **single-invocation** operator expectation and tie to **Step 5** + compact steps — **`/architecture`** + execute phase deliverable per backlog **AC-7**.
- **Contract-test shape** (for **`/architecture`** / dev — not implemented in research phase):
  - **Positive**: Assert **`auto-orchestration-reference.md`** contains normative phrases for (1) **intersected resolved schedule order**, (2) **`AUTO_BACKLOG_DRAIN=1`** + **repeat** / **next eligible OPEN story**, (3) **recompute** / **reload** phase plan at **story boundary** (exact substring set to be architecture-locked to avoid brittle line noise).
  - **Positive**: Assert **`.cursor/commands/auto.md`** compact step **4** retains **intersected schedule** + **US-0069** and explicitly points to reference for **multi-phase continuation** (add marker phrase if architecture chooses).
  - **Negative / guard**: Extend existing **spawn-only** tests — no new wording that implies orchestrator may run phases in-turn (already **`test_slim_auto_no_affirmative_in_process_phase_run`**).
  - **Fixture boundary**: Tests validate **repo text**; they cannot prove Cursor schedules multiple subagent turns — **architecture** should record **expected operator behavior** (single chat continuation vs explicit re-**`/auto`**).
- **`resume_brief` / `state.md` tuple** (multi-phase depth + story cursor — **US-0037** / **DEC-0069**):
  - **Lesson from shipped segment**: **`state.md`** post-**`/verify-work`** **`next_scheduled_phase=release`** can disagree with **top-of-file** **`resume_brief`** still pointing at a **new** story’s **`discovery`** — orchestrator **state_fallback** vs brief reconciliation is required (**already observed** for **US-0087**/**US-0088**). Continuous drain must **refresh** **`intended_resume_phase`** + **`story_id`** (and **`orchestrator_run_id`** when segment policy says so) at **every** materialized stop so **`RESUME_BRIEF_STALE`** does not fire mid lawful run.
  - **Recommendation for architecture**: Pair **AC-10** updates: each phase completion appends **`phase_boundary`**, **`next_scheduled_phase`**, **`story_id`**, **`backlog_drain_stories_remaining_budget`** (and **US-0087** tuple fields when applicable); **`resume_brief`** prepended **Latest** pointer must **mirror** the same tuple for the **active** segment. Optional explicit **`phases_completed_this_invocation`** counter — only if it reduces ambiguity without duplicating **`state.md`** tail.
  - **Stale policy**: No relaxation of fail-fast **stale** rules; fix is **deterministic refresh** at boundaries (**BUG-0005** lineage), not weaker validation.
- **Quiet operator surface (`AC-2`) vs `TOKEN_PROFILE`**:
  - **`TOKEN_PROFILE`** (**lean**/**balanced**/**full**) is a **token-cost / context breadth** control (**US-0080** lineage) — **not** a substitute for **notification semantics**.
  - **Recommendation**: Introduce **`AUTO_QUIET=0|1`** (default-off) **architecture-locked** for “suppress routine phase chatter”; **allowed notifications** remain exactly backlog **AC-2** list (**decision_gate**, **error**, **pause**, **loop_max**, **blocked**, **missing inputs**). **`PHASE_MODE` / `PERMISSION_MODE`** stay orthogonal unless architecture documents an explicit composition matrix.
  - **Risk**: **`AUTO_QUIET=1`** + weak operator habit could miss **decision_gate** if gates are not surfaced as **errors** or **explicit stop_reason** — architecture must lock **non-suppressible** channels.
- **US-0087 mutex** (boundary only): Story drain vs bug-queue **single scheduler** — **`AUTO_SCHEDULER_CONFLICT`**, argv **`bug-target=`** precedence — **no new semantics** here; see **`R-0070`** and **`docs/engineering/architecture.md`** **`# US-0087`**.
- **Risks**:
  - **Doc anchor drift** between compact **`auto.md`** and reference **Steps** reintroduces **one-phase-stop** after edits.
  - **Over-automation**: continuous loop without caps (**`AUTO_LOOP_MAX_CYCLES`**, **`AUTO_BACKLOG_MAX_STORIES`**) exhausts budget — existing scratchpad guards remain mandatory.
  - **False confidence** from substring-only tests if normative **drain** sentences regress silently.
- **Next phase pointers (`/architecture`)**:
  - Lock **AC-1** continuous vs **outer-driver** equivalence; **AC-2** **`AUTO_QUIET`** (+ **`template/`** parity); **AC-3**/**AC-4** test substrings + **runbook** **AC-7**; **`architecture.md`** **`# US-0088`** stop/quiet/resume/**US-0087**-by-reference matrix; **DEC** if policy needs formal amendment beyond story section.
- **Linked**: US-0088, US-0023, US-0037, US-0044, DEC-0022, US-0080, DEC-0062, US-0087, R-0070, DEC-0069, BUG-0005, BUG-0006, US-0069
- **Confidence**: medium (repo text inventory complete; runtime Cursor scheduling out of scope)
- **Delivery closure (2026-04-13T01:30:00Z, curator, `orchestrator_run_id=auto-20260405-01`)**: **`US-0088`** **DONE**; sprint **`S0072`** **released**; continuous multi-phase + **`AUTO_QUIET`** + drain-advance contract delivered per **`architecture.md`** **`# US-0088`** and static tests — **R-0071** objectives satisfied.
- **Status**: closed — delivery aligned with **US-0088** **DONE** (**`US-0045`**) / curator **`/refresh-context`**

## R-0072 — US-0085: gitignored `.env` for remote and release connectivity (no AI read)

- **Date**: 2026-04-13
- **Topic**: **US-0085** — repo-root **`.env`** (gitignored) holding values for `*Env` fields in **`.cursor/remote.json`** and **`release-targets.json`**; committed **`.env.example`** (names only); **`.cursorignore`** + agent rule exclusion; operator-sourced outside agent context.
- **Query**: What `*Env` variable names must `.env.example` list; does `.cursorignore` alone prevent agent file-context ingestion or do Cursor rules need to augment it; is a deterministic helper script (AC-8) preferable to shell-only sourcing; what regression test shape proves `.env` gitignored and `.env.example` committed?
- **Sources**:
  - Internal: **`.gitignore`** (current — no `.env` entry); **`.cursor/remote.json`** template/schema (**`remote.json`** gitignored); **`docs/engineering/release-targets.json`** (**`*Env`** field taxonomy from **US-0064** / **DEC-0070**); **`scripts/remote_config_summary.py`**; **`docs/engineering/runtime-connectivity.md`** (active + `template/`); **`docs/engineering/us-0084-remote-e2e.md`** (active + `template/`); **`docs/product/backlog.md`** **US-0085** acceptance; intake evidence **`handoffs/intake_evidence/US-0085-intake-20260404.json`**
  - External (discovery survey): Keyway 2026 AI secrets security guide; OpenSSF security-focused AI code assistant instructions; GitGuardian `ggshield` AI prompt scanning; `.cursorignore` documentation
- **Findings** (discovery-era — extend in `/research`):
  - **Market pattern**: `.env` + `.gitignore` is baseline; AI dev tools require **`.cursorignore`** and/or explicit agent rules to exclude `.env` from IDE file context — `.gitignore` alone is insufficient because Cursor/Copilot agents have developer-level filesystem access.
  - **`*Env` inventory (TL to confirm)**: `release-targets.json` references env var names for SSH/Docker credentials (`DEPLOY_SSH_KEY_PATH`, `DOCKER_HOST`, etc.); `.cursor/remote.json` template uses `*Env` indirection for host/user/key fields. Exact name list needs repo survey in `/research`.
  - **`.cursorignore` semantics**: Acts as an analog of `.gitignore` for Cursor's file indexing/context engine. Agent rules (`.cursor/rules/`) provide a complementary behavioral layer ("do not open `.env`"). Both layers recommended for defense-in-depth.
  - **AC-8 helper**: Options are (a) small `scripts/print_remote_env_hint.py` that reads `.env.example` and prints required names without values, or (b) documented shell recipe (`source .env && env | grep REMOTE`). Architecture decides.
  - **AC-9 test**: `git check-ignore .env` returns 0 and `git check-ignore .env.example` returns non-0; implementable as a Python test or shell fixture.
- **Open questions (for `/research`)**: ~~(1)–(4) resolved~~ — see **Research extension** below.
- **Linked**: US-0085, US-0084, US-0064, DEC-0070, R-0067, R-0068
- **Confidence**: high (full repo survey + Cursor docs confirmed)
- **Status**: closed — delivery aligned with **US-0085** **DONE** (**`US-0045`**) / curator **`/refresh-context`**
- **Delivery closure (2026-04-13T18:00:00Z, curator, `orchestrator_run_id=auto-20260405-01`)**: **`US-0085`** **DONE**; sprint **`S0073`** **released**; 4-layer defense-in-depth `.env` exclusion contract delivered per **`architecture.md`** **`# US-0085`**, **`DEC-0071`**, and tests — **R-0072** objectives satisfied.
- **Research extension (2026-04-13T12:15:00Z, tech-lead, `orchestrator_run_id=auto-20260405-01`, `fresh_context_marker=tl-US0085-research-20260413T121500Z-fresh`)**:
  - **(1) `*Env` variable name inventory** — **20 unique names** across `template/.cursor/remote.json` (3: `REMOTE_DOCKER_TOKEN`, `REMOTE_SSH_USER`, `REMOTE_SSH_KEY_PATH`) and `docs/engineering/release-targets.json` (17: `PUBLIC_DOMAIN`, `CHOCO_API_KEY`, `GITHUB_TOKEN`, `DOCKER_TOKEN`, `DOCKER_RUNTIME_HOST`, `AWS_PROFILE`, `APP_DOMAIN`, `APP_IP`, `CUSTOM_DOMAIN`, `CUSTOM_IP`, `SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY`, `RUNTIME_DOMAIN`, `RUNTIME_IP`, `DOCKER_HOST`, `DOCKER_CONTEXT`). `.env.example` lists all 20 grouped by source config with comments.
  - **(2) `.cursorignore` semantics confirmed** (Cursor docs `cursor.com/docs/reference/ignore-file`): `.gitignore` syntax; blocks agent file tools (`read_file`, `grep`, `@` mentions); does **not** block terminal or MCP tools; `.env*` in default indexing ignore list but explicit `.cursorignore` adds agent-tool hard block. Open-tab caveat: files open in editor may leak. **Defense-in-depth (4 layers)**: `.gitignore` (git tracking) + `.cursorignore` (agent file tools) + Cursor rules (behavioral) + operator discipline (don't open `.env` in editor).
  - **(3) AC-8 helper recommendation**: **Option A** — `scripts/print_remote_env_hint.py` (reads `.env.example` names, validates parity with `*Env` fields, never touches `.env`, cross-platform). Option B (shell `source .env && env | grep`) is POSIX-only, leaks values — document as convenience only.
  - **(4) AC-9 test**: `git check-ignore .env` → exit 0; `git check-ignore .env.example` → exit 1. Python test in `tests/` using `subprocess.run`.
  - **(5) Template parity**: `.gitignore` (no `template/.gitignore` exists — architecture decides), `.cursorignore` (new, both), `.env.example` (new, both), `runtime-connectivity.md` (both), `us-0084-remote-e2e.md` (both), `runbook.md` (both), `.cursor/rules/coding-standards.mdc` (both).
  - **(6) Risks**: terminal bypass (medium, mitigated by rules); open-tab leak (low, operator discipline); `.env` framework collision (low, repo is toolkit); `remote_config_summary.py` unaffected (reads `remote.json` names, not `.env` values — AC-10 PASS); template `.env.example` divergence if `*Env` fields change.
  - **(7) `remote_config_summary.py` AC-10**: script reads `remote.json`, not `.env`. No changes needed. Tests remain PASS.
  - **`DEC-0038`** tuple in **`docs/engineering/state.md`**; backlog **`research_notes`** updated; **`handoffs/resume_brief.md`** → **`/architecture`**.
- **Prior historical extension (2026-04-12T23:15:00Z, tech-lead, US-0088 context)**: R-0071 findings; preserved for lineage.
- **Discovery extension (2026-04-12T22:00:00Z, PO, `orchestrator_run_id=auto-20260405-01`, `fresh_context_marker=po-US0088-discovery-20260412T220000Z-fresh`)** — survey anchor (historical):
  - **Normative vs practice**: **Step 5** describes **per-phase subagent** iteration inside **one** orchestrated **`/auto`** run until a deterministic stop; common failure mode = **single spawn** then **orchestrator turn ends** despite “continue” policy — enumerate doc/command sentences that imply multi-phase loop vs single-phase.
  - **Quiet + cost**: Merged scratchpad **`TOKEN_PROFILE=balanced`**, **`EARLY_RESEARCH=1`**, **`INTAKE_GUIDED_MODE=1`**; **`AC-2`** must pick/document **`AUTO_QUIET`** and/or composition with **`TOKEN_PROFILE` / `PHASE_MODE`** without hiding **decision_gate** or mandatory evidence paths.
  - **Drain reliability**: Under **`AUTO_BACKLOG_DRAIN=1`**, prove **phase depth** and **story cursor** advance per **US-0044** / **DEC-0022**; align **`state.md` / `resume_brief`** fields with **US-0037** / **DEC-0069** so continuous runs do not false-**`RESUME_BRIEF_STALE`** mid-segment.
  - **Test targets**: **`tests/auto_command_contract_test.py`** (or successor) — negative/positive cases for “does not stop after first spawn when policy says continue”; parity **active + `template/`** for any new scratchpad keys (**AC-5**).
  - **Mutex**: **US-0088** stays **story-centric**; **US-0087** bug-queue + **`AUTO_SCHEDULER_CONFLICT`** remains architecture-locked — research cites **R-0070** / **`# US-0087`** for boundary only.

## R-0073 — US-0089 / US-0090: external Caveman pattern vs its-magic integration

- **Date**: 2026-04-14
- **Topic**: **US-0089** / **US-0090** — Caveman-style terse responses and optional **input** compression; Cursor-only; scratchpad-configured; default off
- **Query**: What from the public **JuliusBrussee/caveman** project is **portable** into this repo as **rules/skills/docs** (no mandatory plugin install), and what must stay **out of scope** to preserve gates, **US-0078** evidence integrity, and **US-0085** secret handling?
- **Sources**:
  - External: **`https://github.com/JuliusBrussee/caveman`** (README — levels **lite/full/ultra**, optional **Wenyan** modes, **`caveman-compress`** with **original backup** pattern, Cursor install via **`npx skills add … -a cursor`**, “compress touches prose not code blocks” claim).
  - Internal: **`US-0053`**, **`US-0080`**, **`TOKEN_PROFILE`** scratchpad contract; **`.cursor/rules/`**; **`.cursor/skills/`**; **`US-0085`** **`.env`** / **`.cursorignore`**; **`DEC-0060`** **`ie:`** intake bundles under **`handoffs/intake_evidence/`**; **`BUG-0007`** truthfulness constraints on intake evidence.
- **Findings** (intake survey — extend in **`/discovery`**):
  - **Response-side (US-0089)**: Replicate **intent** (terse, imperative, drop filler) via **Cursor rules** and/or a **small skill**; map **levels** to documented scratchpad enum; **do not** claim vendor token percentages — cite **“directionally similar goal to US-0080”** instead of external benchmarks inside normative docs.
  - **Input-side (US-0090)**: External **compress** keeps a **human original** sidecar — **good pattern** for this kit’s **loss-avoidance** priority; **default deny** for **canonical product/engineering artifacts**, **intake evidence JSON**, and **any gitignored secret path** aligns with **US-0085** and **DEC-0060**.
  - **Composition**: **`TOKEN_PROFILE`** remains **context breadth / automation pack size**; **Caveman** is **voice + optional file compression** — architecture should document **non-substitution** (avoid implying **`CAVEMAN_MODE=1`** replaces **`TOKEN_PROFILE=lean`**).
  - **Install path**: Prefer **in-repo** rules/skill text over requiring **`npx skills add`** for the framework itself (**installer parity** risk if optional); consumer repos may still use upstream skill **if** architecture documents an optional path.
- **Risks**:
  - Over-compression of **markdown tables**, **AC checklists**, or **reason-code lists** → **test drift** or **validator false negatives**.
  - Accidental **rewrite** of **`handoffs/intake_evidence/*.json`** → **US-0078** / **BUG-0007** class regressions.
  - **Template drift** if only active **`.cursor/`** is updated (**US-0017**).
- **Next phase pointers (`/discovery`)**:
  - Lock **exact scratchpad key names**, **default enum**, and **“off means byte-identical behavior”** test strategy for **US-0089**.
  - Decide **minimal** script API for **US-0090** (**dry-run**, **sidecar naming**, **deny glob list**) before **`/architecture`**.
- **Linked**: US-0089, US-0090, US-0053, US-0080, US-0085, US-0078, DEC-0060, BUG-0007, US-0017
- **Confidence**: medium (external README only; no submodule vendoring in this intake)
- **Status**: open — extended at **`/discovery`** (**2026-04-18**, **US-0089**); remains stub-appropriate for **`/research`** (tech-lead) to deepen

### Discovery extension (2026-04-18, PO, `auto-20260418-01`)

- **Focus**: **US-0089** response-side only; **US-0090** compression remains out of scope for this discovery segment.
- **External reference pattern notes** (reference only, MIT — do **not** vendor):
  - **JuliusBrussee/caveman** README defines levels **`lite`** / **`full`** / **`ultra`** and an optional "Wenyan" mode; the value transferable to this kit is the **level taxonomy** and the **"compress prose, not code blocks"** discipline. Exact enum values and any "Wenyan"-style extras are **architecture-locked** under **`# US-0089`**, not promised here.
  - README claims vendor token savings per level — **do not quote** inside normative kit docs (no vendor benchmarks in `architecture.md` / `runbook.md`); at most, cite as **"directionally similar intent to US-0080 outcomes"**.
  - Upstream install path uses **`npx skills add … -a cursor`**; for this kit's framework surface, prefer **in-repo** rules / `.cursor/skills/` text over mandatory external install. Consumer repos may optionally layer the upstream skill **after** kit rules load.
- **Cursor rule / skill composition notes** (research asks for `/research`, tech-lead):
  - Minimal-surface option: **rule-only** under **`.cursor/rules/`** (voice + "literal-preserved regions" + gate-language passthrough), no new skill.
  - Expanded option: **rule + focused skill** under **`.cursor/skills/its-magic-caveman/`** composed with existing `its-magic/SKILL.md` — prefer **composition** over replacement (skill does **not** override its-magic workflow or gate artifacts).
  - In either option: Caveman behavior must be **gated on `CAVEMAN_MODE`** at rule/skill read time; when unset / `0`, the rule's additional directives must be **inert** (no behavioral drift).
- **"Default-off byte-equivalence" test strategy** (for `/research` → `/architecture` lock):
  - Extend **`tests/auto_command_contract_test.py`** (or add a focused module) to assert that with **`CAVEMAN_MODE=0`** (or absent), the set of normative contract strings (reason codes, AC checklists, gate messages, command output markers like `[BUG_VALIDATION_OK]`) remains **unchanged**.
  - Regression-lock **scratchpad key documentation markers** (active + **`template/.cursor/scratchpad.md`**) and **`.cursor/scratchpad.local.example.md`** parity so a future edit cannot silently drop the new keys.
- **Interaction with `TOKEN_PROFILE` (US-0080 / DEC-0062)**: research must produce a **precedence matrix** (or declare them fully orthogonal) for publication in **`docs/engineering/auto-orchestration-reference.md`** and/or **`runbook.md`**; **no silent override** in either direction.
- **Operator control phrasing (research asks)**: shortlist of candidate phrases + deterministic mapping to session toggle — architecture will pick a single documented set.
- **Non-goals carried into research**: no input-side file compression work (US-0090); no changes to intake evidence schema (**US-0078 / DEC-0060**); no edits to strict-proof / isolation evidence wording (**US-0056 / DEC-0038** / **US-0048 / DEC-0029**).
- **Discovery outcome**: confidence raised on boundary clarity; **`R-0073`** remains **open** for `/research` (tech-lead) deepening — no DEC yet.

### Research extension (2026-04-18, TL, `auto-20260418-01`)

> Scope: deepen **R-0073** with implementation anchors, risks, and mitigations for the **US-0089** response-side Caveman mode. **No architecture decision authored here** — options are laid out for **`/architecture`** to lock under `DEC-xxxx` and `docs/engineering/architecture.md` `# US-0089`. US-0090 (input-side compression) stays out of scope; research only notes the shared scratchpad-vocabulary seam.

- **Q1 — TOKEN_PROFILE × CAVEMAN precedence** (AC-4):
  - **Option A (recommended baseline — orthogonal)**: `TOKEN_PROFILE=lean|balanced|full` controls **context breadth / automation pack size** (US-0080 / DEC-0062); `CAVEMAN_MODE`/`CAVEMAN_LEVEL` control **reply voice** only. Neither substitutes for the other. Published as an explicit non-substitution line in `docs/engineering/auto-orchestration-reference.md` and `docs/engineering/runbook.md`. Minimal doc delta; zero behavior change when Caveman off.
  - **Option B (explicit precedence matrix)**: Publish a small table `{TOKEN_PROFILE} × {CAVEMAN_MODE}` enumerating voice + context pack per cell. Higher doc cost; useful only if architecture decides one profile must dominate (no current evidence it should).
  - **Option C (collapse into TOKEN_PROFILE)**: Add a new profile value (e.g. `lean-caveman`). **Rejected for research recommendation** — breaks US-0080 token-profile semantics, hides voice behind context-breadth control, and forces every TOKEN_PROFILE consumer to care about voice.
  - **Risks**: silent override either direction (operators reading `CAVEMAN_MODE=1` as "lean equivalent"); TOKEN_PROFILE doc drift; conflicting examples in runbook vs auto-reference.
  - **Mitigations**: single non-substitution sentence anchored by fixture test asserting both `docs/engineering/auto-orchestration-reference.md` and `docs/engineering/runbook.md` contain the phrase; template parity extends to both; architecture picks A (default) or B.
  - **Anchors**: `docs/engineering/auto-orchestration-reference.md` (§`AUTO_QUIET` / TOKEN_PROFILE), `docs/engineering/runbook.md`, `.cursor/scratchpad.md` header comments.
  - **Open ask for `/architecture`**: lock Option A (recommended) or Option B; publish precedence paragraph verbatim in active + `template/` reference + runbook.

- **Q2 — Rule-only vs rule+skill composition** (AC-3):
  - **Option A (rule-only, minimal)**: add `.cursor/rules/caveman.mdc` (with `globs: ["**/*"]` scope matching existing `core.mdc`) gated at read-time on `CAVEMAN_MODE`. Pros: single surface, lowest maintenance, easiest default-off byte-equivalence test. Cons: less discoverable as a named "skill"; harder for consumer repos to layer optional upstream Caveman skill.
  - **Option B (rule + focused skill)**: add `.cursor/rules/caveman.mdc` (gate + literal-preservation invariants) **plus** `.cursor/skills/its-magic-caveman/SKILL.md` (voice text + level mapping + operator phrasing catalog) composed with existing `.cursor/skills/its-magic/SKILL.md` (no override). Pros: discoverable, mirrors JuliusBrussee/caveman skill posture without vendoring, separates concerns (invariants vs voice). Cons: two surfaces to keep in sync; template parity duplicated.
  - **Option C (skill-only)**: rely on a skill without a rule. **Not recommended** — rules are always-on context for Cursor agents; skills are invoked/read contextually. Literal-region invariants must live in rules to be reliably enforced on every turn.
  - **Tradeoffs table anchor (architecture use)**: maintenance (A < B ≪ C), discoverability (B ≫ A > C), template parity cost (A < B; A=2 files, B=4 files incl. template mirrors), default-off regression surface (A < B).
  - **Risks**: rule drift vs skill drift; gate missed on one surface; consumer upstream Caveman install conflicting with in-repo rule.
  - **Mitigations**: pick Option A if maintenance wins; pick Option B only if discoverability justifies the extra surface; either way, put the **non-suppressible gate list** (decision_gate, error, pause, loop_max, blocked, missing-input; carry from US-0088) **inside the rule** so skills never override it; add a contract test asserting gate-marker preservation under `CAVEMAN_MODE=1`.
  - **Anchors**: `.cursor/rules/core.mdc`, `.cursor/rules/quality.mdc`, `.cursor/rules/coding-standards.mdc`, `.cursor/skills/its-magic/SKILL.md`, `template/.cursor/rules/*`, `template/.cursor/skills/its-magic/SKILL.md`.
  - **Open ask for `/architecture`**: select Option A or B; lock rule filename; if Option B, lock skill folder name (candidate `.cursor/skills/its-magic-caveman/`).

- **Q3 — Default-off invariant testing** (AC-2 / AC-6):
  - **Primary strategy**: extend `tests/auto_command_contract_test.py` with a new block of subtests `test_caveman_default_off_*` asserting:
    1. `.cursor/scratchpad.md` contains key lines `CAVEMAN_MODE=0` (or `CAVEMAN_MODE=` with documented default-0 comment) and `CAVEMAN_LEVEL=` — architecture locks exact spelling.
    2. `template/.cursor/scratchpad.local.example.md` documents the same keys (parity — mirror assertion).
    3. Existing `required` token list (spawn-only contract, reason codes, `# US-0086` tokens, `AUTO_QUIET`) remains **unchanged and intact** after US-0089 ships — regression guard on Caveman not suppressing any existing contract strings.
    4. New assertion: `auto.md` + reference doc still contain **non-suppressible gate vocabulary** (`decision_gate`, `missing input`, `pause`, `loop_max`, `blocked`, `[BUG_VALIDATION_OK]`, `[INTAKE_EVIDENCE_VALIDATION_OK]`) — Caveman MUST NOT remove these.
    5. Active/template parity: `test_template_runbook_literal_parity_active` style check extended to cover any new runbook section added for Caveman (architecture decides whether to add a section or a single paragraph).
  - **Secondary (optional focused module)**: `tests/caveman_defaults_test.py` if the caveman assertions grow past ~10 subtests (architecture choice).
  - **What we are NOT testing in US-0089**: behavioral differences under `CAVEMAN_MODE=1` (voice is a qualitative property enforced by rules, not easily asserted in unit tests); out-of-scope for AC-6. Architecture may add a smoke-level "rule file contains Caveman directive markers" assertion but cannot unit-test an LLM's voice deterministically.
  - **Risks**: test-over-reach that forces voice quality into CI; false green when rule file exists but is not loaded by Cursor.
  - **Mitigations**: keep tests file-presence + token-presence only; rely on manual operator verification for voice quality; architecture notes this limitation in `# US-0089`.
  - **Anchors**: `tests/auto_command_contract_test.py` (existing patterns for scratchpad/template parity), `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`.
  - **Open ask for `/architecture`**: confirm extension-in-place vs new module; lock the exact scratchpad key spelling (for test string match).

- **Q4 — Operator toggle vocabulary** (AC-5):
  - **Candidate phrase set (shortlist for architecture)**: `caveman on` / `caveman off` (symmetric, short); `stop caveman` / `normal mode` (aligns with upstream README discourse); `caveman: lite|full|ultra` (level-setter without a mode flip). Architecture locks **one canonical set** published in runbook.
  - **Determinism under mid-session toggles**: Cursor operator speech is free-form; the rule must specify that **only the last explicit toggle in the current conversation wins**, and on new subagent spawn the **scratchpad value** (`CAVEMAN_MODE`) is authoritative (session toggle is an overlay, not a persistent state). This matches US-0069 / DEC-0051 phase-boundary semantics — no hidden state crosses a subagent boundary.
  - **Risks**: ambiguous phrasing (`quiet caveman`, `be caveman-lite`) matching unintentionally; mid-session toggle masking a gate message (e.g. operator says "normal" mid-error flow and the agent drops a reason code by mistake).
  - **Mitigations**: rule lists exact recognized phrases (literal regex-ish catalog); toggle MUST NOT suppress non-suppressible gate surfaces for that turn; architecture documents "toggle applies to next turn onward; current-turn gate artifacts remain literal".
  - **Anchors**: `.cursor/rules/core.mdc` (pattern for documented directive lists), `docs/engineering/runbook.md`, `.cursor/scratchpad.md` (comment line pointing at runbook operator phrases section).
  - **Open ask for `/architecture`**: pick the canonical phrase set; publish in runbook + (optional) skill.

- **Q5 — Machine-verifiable artifact preservation (literal regions)** (AC-3):
  - **Protected output zones** (architecture locks as rule directives, verbatim):
    1. Fenced code blocks (``` … ``` and CODE REFERENCE blocks with `startLine:endLine:filepath`).
    2. File/path strings (anything matching `\`[\w./-]+\.(md|py|ps1|sh|json|mdc)\``).
    3. AC checklist bullets (`- [ ]` / `- [x]`) and their full ACn text.
    4. Reason codes — ALL_CAPS_WITH_UNDERSCORES tokens (explicit examples: `PHASE_CONTEXT_ISOLATION_VIOLATION`, `RUNTIME_PROOF_MISSING`, `AUTO_RESUME_ERROR`, `AUTO_SCHEDULER_CONFLICT`, `REMOTE_TARGET_UNKNOWN`, …).
    5. IDs — `US-xxxx`, `DEC-xxxx`, `R-xxxx`, `BUG-####`, `S0xxx`, `T-xxx`.
    6. Contract markers — `[BUG_VALIDATION_OK]`, `[INTAKE_EVIDENCE_VALIDATION_OK]`, `[SCRATCHPAD_PAIR_OK]`, `[ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS]` and siblings.
    7. Strict-proof tuple fields (`orchestrator_run_id`, `runtime_proof_id`, `proof_hash`, `proof_issued_at`, `proof_ttl_seconds`, `phase_id`, `role`).
    8. Isolation evidence fields (`fresh_context_marker`, `evidence_ref`, `timestamp`).
    9. Commit messages and git refs when quoted (`git commit`, `HEAD`, branch names).
  - **Garbling examples to forbid** (rule text): dropping `US-` prefix, rendering reason codes in lowercase prose, collapsing fenced code into a bullet list, truncating path strings mid-filename.
  - **Risks**: Caveman voice enthusiastically compressing a path or reason code; rule interpreted as "best effort" rather than hard invariant.
  - **Mitigations**: rule phrased as "MUST keep literal" (not "SHOULD"); test Q3/#4 asserts gate vocabulary remains present in auto.md + reference after any Caveman-related doc edits; architecture reiterates this list in `# US-0089` under a "Literal regions (hard invariant)" heading.
  - **Anchors**: `.cursor/rules/core.mdc`, `.cursor/rules/quality.mdc` (existing literal-region discipline patterns), `docs/engineering/artifact-ordering-policy.md`.
  - **Open ask for `/architecture`**: accept the nine-zone list verbatim or narrow it; publish as canonical in `# US-0089`.

- **Q6 — External pattern portability (JuliusBrussee/caveman, MIT)** (reference only):
  - **Portable concepts**: level taxonomy (`lite|full|ultra`); "compress touches prose, not code blocks" discipline; symmetric operator toggle phrasing.
  - **Non-portable (kept out of scope)**: `npx skills add … -a cursor` vendor install path (our framework ships in-repo rules/skill); vendor token-savings claims (no benchmarks in normative kit docs per US-0080 rigor); Wenyan-mode linguistic extras (cultural-specific — not required for terseness).
  - **Attribution**: architecture may add a single "Inspired by JuliusBrussee/caveman (MIT)" line in `# US-0089` and in any new skill file; no vendored code or README text.
  - **Risks**: accidental vendor-install instructions leaking into runbook; citing vendor token percentages as if they were kit benchmarks.
  - **Mitigations**: rule forbids vendor benchmark claims in normative docs; runbook Caveman section reviewed for zero `npx` references.
  - **Anchors**: `https://github.com/JuliusBrussee/caveman` (README, MIT) — **external reference only, do not vendor**.
  - **Open ask for `/architecture`**: decide attribution placement (single line vs section); confirm no vendor install instruction in runbook.

- **Q7 — Scratchpad key naming** (AC-1):
  - **Recommended enum (for architecture to lock)**:
    - `CAVEMAN_MODE=0|1` — default **0** (off). Semantics: 0 means byte-equivalent pre-US-0089 behavior; 1 means voice rule active.
    - `CAVEMAN_LEVEL=lite|full|ultra` — default empty (meaning "use default level = `full`" per rule, OR "inert when MODE=0" — architecture picks). Three-value enum matches external reference; future extension possible but not required.
  - **Alternatives considered**:
    - `CAVEMAN=off|lite|full|ultra` (single key). **Rejected for research recommendation** — collides with our existing 0|1 convention (`AUTO_QUIET`, `AUTO_BACKLOG_DRAIN`, …) and couples enable-flag with level.
    - `CAVEMAN_VOICE` instead of `CAVEMAN_MODE`. Acceptable naming variant; architecture picks. Research recommendation: `CAVEMAN_MODE` matches verb-pattern of `TOKEN_PROFILE`, `AUTO_FLOW_MODE`.
  - **Reserved-for-US-0090 keys (documented no-ops in US-0089)**: `CAVEMAN_COMPRESS_INPUT=0|1` (default **0**), `CAVEMAN_FILE_SCOPE=` (empty default). Comments in `.cursor/scratchpad.md` must state "reserved for US-0090; inert in US-0089 ship — no behavior until compression story lands".
  - **Risks**: operators reading the reserved keys and expecting behavior in US-0089; key rename churn if architecture picks a different spelling after tests lock strings.
  - **Mitigations**: explicit "reserved for US-0090, no-op" comment; contract-test string assertions deferred until architecture locks names (tech-lead writes test string values into `# US-0089` decision record so dev phase picks up the locked spelling).
  - **Anchors**: `.cursor/scratchpad.md` (lines ~148–180 — knowledge-curation and TOKEN_PROFILE block for visual placement), `template/.cursor/scratchpad.local.example.md`, `.cursor/scratchpad.local.example.md`.
  - **Open ask for `/architecture`**: lock the four key names + defaults; confirm US-0090 reserved keys stay no-ops until that story ships.

- **Q8 — Template parity touchpoints** (AC-8):
  - **Inventory (active → template mirror expectation)**:
    1. `.cursor/scratchpad.md` → `template/.cursor/scratchpad.md` (if template carries an active baseline; currently template-side equivalent is the `.example.md` helper — architecture confirms).
    2. `.cursor/scratchpad.local.example.md` → `template/.cursor/scratchpad.local.example.md` (already literally mirrored per existing `test_template_scratchpad_baseline_literal_parity_active` pattern).
    3. New `.cursor/rules/caveman.mdc` (if Option A or B for Q2) → `template/.cursor/rules/caveman.mdc`.
    4. Optional new `.cursor/skills/its-magic-caveman/SKILL.md` (if Option B for Q2) → `template/.cursor/skills/its-magic-caveman/SKILL.md`.
    5. `docs/engineering/auto-orchestration-reference.md` → `template/docs/engineering/auto-orchestration-reference.md` (if TOKEN_PROFILE precedence paragraph added).
    6. `docs/engineering/runbook.md` → `template/docs/engineering/runbook.md` (operator-phrase catalog and non-substitution paragraph).
    7. `docs/engineering/architecture.md` — active only (no template mirror for story-scoped architecture sections per existing pattern).
    8. `tests/auto_command_contract_test.py` — active only (tests do not mirror to `template/`).
    9. `.cursor/skills/its-magic/SKILL.md` — touched only if architecture decides to add a cross-link to Caveman skill (Option B); mirror under `template/` as usual.
  - **Risks**: partial mirror (rule added active-side but not template-side); US-0017 parity test regression.
  - **Mitigations**: contract-test subtests for each new template file presence; architecture lists every new file path in `# US-0089` under a "Template parity files" heading so dev phase has a checklist.
  - **Anchors**: `template/.cursor/rules/*`, `template/.cursor/skills/its-magic/SKILL.md`, existing parity subtests in `tests/auto_command_contract_test.py`.
  - **Open ask for `/architecture`**: lock the full parity inventory (A- or B-path) before sprint-plan atomizes tasks.

- **US-0090 boundary note** (non-scope, forward-link only): US-0089 establishes `CAVEMAN_MODE` + `CAVEMAN_LEVEL` vocabulary; US-0090 later gates `CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE` on top of that. Research makes **no** input-side recommendations here; `R-0073` remains the shared anchor but US-0090 will extend it in its own discovery/research cycle.

- **Summary architecture asks (for `/architecture`, DEC-xxxx hints)**:
  - `DEC-xxxx` (TOKEN_PROFILE × CAVEMAN): adopt Option A (orthogonal, non-substitution paragraph) unless explicit evidence prefers a matrix.
  - `DEC-xxxx` (rule vs rule+skill): pick Option A (rule-only) for minimal surface OR Option B (rule + focused skill) for discoverability.
  - `DEC-xxxx` (default-off test module): extend `tests/auto_command_contract_test.py` in place; lock exact scratchpad key strings before dev writes tests.
  - `DEC-xxxx` (literal regions invariant): publish the 9-zone list verbatim in `# US-0089`.
  - `DEC-xxxx` (operator phrases): pick one symmetric set; document in runbook + (optional) skill.

- **Research closure**: **R-0073** research-phase extension complete (2026-04-18, TL, `auto-20260418-01`); **no DEC-xxxx authored** (architecture owns decisions); **no architecture section** authored; story **US-0089** remains **OPEN** per **US-0045**. Next: **`/architecture`** (fresh **tech-lead**) — lock DEC(s) and write `# US-0089`.

- **Delivery closure (US-0089, curator `/refresh-context`, 2026-04-18T20:00:00Z, `auto-20260418-01`)**: **R-0073** marked **delivered / resolved** for the **US-0089** response-side Caveman-mode surface. Evidence: sprint **`S0075`** released `2026-04-18T19:00:00Z` via **`handoffs/releases/S0075-release-notes.md`**; governance locked in **`decisions/DEC-0072.md`** + **`docs/engineering/architecture.md`** **`# US-0089`**; scratchpad contract + rule surface + default-off invariant shipped in **`.cursor/scratchpad.md`**, **`.cursor/scratchpad.local.example.md`** (+ `template/`), **`.cursor/rules/caveman.mdc`** (active + `template/`), **`docs/engineering/auto-orchestration-reference.md`** (+ `template/`), **`docs/engineering/runbook.md`** (+ `template/`); regression coverage in **`tests/auto_command_contract_test.py`** (8 `test_caveman_default_off_*` subtests + 3 supplemental caveman subtests, 11 total caveman subtests, 119 subtest invocations, 0 failures). Backlog **`docs/product/backlog.md`** **US-0089** `Status: DONE`; AC-1..AC-8 `[x]`. **R-0073** remains the **shared anchor** for **US-0090** (input-side / file-compression vertical); US-0090 will extend R-0073 in its own discovery/research cycle (see `## US-0090` in `docs/product/backlog.md`). Status: **delivered (US-0089); open for US-0090 extension**.

### Discovery extension (2026-04-18, PO, `auto-20260418-01`, US-0090 input-side)

> Scope: extend **R-0073** with **input-side compression** anchors for **US-0090** built on top of the **US-0089** shipped surface (DEC-0072). No architecture decision authored here; options are laid out for the next phase `/research` (fresh **tech-lead**) to deepen and `/architecture` to lock under a new `DEC-xxxx` + `# US-0090`.

- **Context & dependency on US-0089's shipped surface**:
  - Scratchpad keys `CAVEMAN_COMPRESS_INPUT=0|1` (default **0**) and `CAVEMAN_FILE_SCOPE=` (default empty) are already declared as **documented no-ops** in `.cursor/scratchpad.md` and `.cursor/scratchpad.local.example.md` (+ `template/` mirror) per **DEC-0072** §3. **US-0090** activates them; it does **not** rename them.
  - The **9-zone literal-region invariant** (DEC-0072 §4) is the authoritative source of truth for byte-preserved regions. **US-0090** reuses this list verbatim for the file-compression path — architecture MUST NOT narrow it, may extend only with explicit DEC.
  - **TOKEN_PROFILE × CAVEMAN_MODE non-substitution** (DEC-0072 §1) is response-side. **US-0090** adds a **third** independent axis (`CAVEMAN_COMPRESS_INPUT`). Research ask: publish a three-axis non-substitution paragraph (or compact table) in `docs/engineering/auto-orchestration-reference.md` + `docs/engineering/runbook.md` (+ `template/`).
  - The `.cursor/rules/caveman.mdc` rule body is **untouched by US-0090** unless architecture opts to add a single "Input-side extension (US-0090)" subsection pointing at the script + deny-list; rule changes are otherwise out of scope.

- **Input-side compression anchors (open options for `/research` tech-lead)**:
  - **Q9 — Compression algorithm choice (input-side)**:
    - Option A (recommended baseline): **whitespace-collapse + filler-word strip + markdown-structure-preserving** prose rewrite; fenced code blocks, tables, AC checklists, reason codes, IDs skipped by the zone matcher.
    - Option B: **line-level deterministic minifier** (collapse duplicate blank lines, trim trailing whitespace, no semantic rewrite). Minimal token savings; highest safety.
    - Option C: **LLM-assisted prose compression** via a deterministic prompt. **Not recommended** — introduces non-determinism, violates idempotency AC-6, and couples compression to vendor availability.
    - Research to decide whether to publish a single algorithm or a `--mode=safe|aggressive` switch with named profiles.
  - **Q10 — Sidecar original naming**:
    - Option A: **sibling dotfile** `.<name>.caveman-original.<ext>` next to the compressed file. Pros: trivial pairing; visible in the same directory. Cons: `.gitignore` hygiene per folder.
    - Option B: **parallel tree** under `docs/.caveman-originals/<relative/path>/<file>`. Pros: single `.gitignore` anchor; no per-folder hygiene. Cons: requires relative-path reconstruction.
    - Option C: **in-repo sidecar with hash suffix** `<name>.<sha1>.caveman-original.<ext>`. Pros: collision-safe on re-runs. Cons: less human-readable.
    - Research recommendation: Option B (parallel tree) for `.gitignore` simplicity and safe publish hygiene; architecture locks the final pattern.
  - **Q11 — Deny-list source of truth**:
    - Option A: **hard-coded constants** in the compression script (fastest, deterministic; matches the PO baseline list in backlog `## US-0090` discovery_notes).
    - Option B: **`.cursorignore` / `.gitignore` aware** (respect repo ignore files automatically).
    - Option C: **hybrid** (hard-coded baseline + merge with `.cursorignore` patterns) — recommended for defense in depth.
    - Deny list MUST include at minimum: `.env`, `.env.*`, `**/*intake_evidence*/**`, `docs/product/backlog.md`, `docs/product/acceptance.md`, `docs/engineering/state.md`, `docs/engineering/decisions.md`, `decisions/DEC-*.md`, `sprints/*/plan-verify.json`, `sprints/*/uat.json`, `sprints/*/summary.md`, `sprints/*/release-findings.md`, `package.json`, `package-lock.json`, `installer.*`, `.github/workflows/*.yml`, `.cursor/hooks/*.py`, `.cursor/rules/*.mdc`, `.cursor/commands/*.md`, `.cursor/skills/**/SKILL.md`, binaries (`.png`, `.jpg`, `.pdf`, `.zip`, …).
  - **Q12 — Allow-list grammar for `CAVEMAN_FILE_SCOPE`**:
    - Option A: **comma-separated globs** (e.g. `CAVEMAN_FILE_SCOPE=docs/user-guides/**/*.md,docs/engineering/runbook.md`).
    - Option B: **named profiles** (e.g. `CAVEMAN_FILE_SCOPE=docs-prose-only` resolves to a locked glob set; `CAVEMAN_FILE_SCOPE=custom:<csv-globs>` for custom).
    - Option C: **both** (named profiles + raw globs, profile wins if listed first).
    - Deny-list MUST always be evaluated **after** allow-list expansion and **wins** on any conflict. Empty `CAVEMAN_FILE_SCOPE` (default) MUST evaluate to "no files in scope" — operator must opt in explicitly.
  - **Q13 — `dry-run` vs `write` UX**:
    - Primary entrypoint under `scripts/` (exact filename architecture-locked; candidate `scripts/caveman_compress_input.py`). Required modes: `--dry-run` (default when invoked without mode), `--write`, `--verify-originals`, `--report` (emit diff summary to stdout / JSON). Exit code **non-zero on any deny-list hit, scope violation, literal-region damage, or idempotency break** with deterministic reason code.
  - **Q14 — Idempotency test strategy (AC-6)**:
    - Fixture files under `tests/fixtures/caveman_compress/` with paired inputs + expected compressed outputs + sidecar originals; test runs compression twice and asserts byte-equality on the second run (idempotency invariant).
    - Literal-region fixtures: input containing fenced code, AC checklists, reason codes, IDs, and contract markers — test asserts 9-zone regions are byte-identical to input.
    - Deny-list fixtures: simulated path inputs for every deny-list entry — test asserts script refuses and emits `CAVEMAN_COMPRESS_DENY_HIT` (final reason-code name architecture-locked).
  - **Q15 — Reason-code vocabulary (architecture to lock verbatim)**:
    - Candidate codes (all `ALL_CAPS_WITH_UNDERSCORES`, same convention as existing repo vocabulary): `CAVEMAN_COMPRESS_SCOPE_VIOLATION`, `CAVEMAN_COMPRESS_DENY_HIT`, `CAVEMAN_COMPRESS_NOT_IDEMPOTENT`, `CAVEMAN_COMPRESS_LITERAL_REGION_DAMAGED`, `CAVEMAN_COMPRESS_ORIGINAL_MISSING`, `CAVEMAN_COMPRESS_MODE_DISABLED` (when `CAVEMAN_COMPRESS_INPUT=0`), `CAVEMAN_COMPRESS_SCOPE_EMPTY` (when allow-list empty).
    - Architecture publishes the final list in `# US-0090` and `.cursor/rules/caveman.mdc` (if the rule gains a subsection).
  - **Q16 — Three-axis non-substitution documentation** (AC-4 equivalent):
    - TOKEN_PROFILE (context breadth) × CAVEMAN_MODE (voice) × CAVEMAN_COMPRESS_INPUT (file mutation) are three **independent** axes. Research ask: pick a publication form (parallel paragraphs vs compact 2x2x2 table vs matrix) for `docs/engineering/auto-orchestration-reference.md` + `docs/engineering/runbook.md`.
  - **Q17 — Template parity touchpoints (AC-8 equivalent)**:
    - Active/template pairs in scope for US-0090 (exact list architecture-locked): `scripts/caveman_compress_input.py` (active + `template/scripts/` mirror per **US-0017**), `docs/engineering/runbook.md` (operator section active + `template/`), `docs/engineering/auto-orchestration-reference.md` (three-axis paragraph active + `template/`), `tests/fixtures/caveman_compress/` (active only; tests do not mirror), `tests/auto_command_contract_test.py` (extended in place; active only), `.cursorignore` (operator-owned; architecture confirms kit-level changes or leaves to operator), `.gitignore` (for sidecar tree, per Q10 Option B).
  - **Q18 — Security / compliance boundary**:
    - MUST respect **US-0085** `.env` / secrets prohibition; deny-list entry for `.env*` is non-negotiable.
    - MUST respect **US-0078** / **DEC-0060** intake evidence integrity; `handoffs/intake_evidence/*.json` is deny-listed.
    - MUST respect **US-0045** backlog status authority; `docs/product/backlog.md` + `docs/product/acceptance.md` are deny-listed.
    - MUST respect **DEC-0040** artifact ordering; `docs/engineering/state.md` is deny-listed.
    - MUST NOT leak `npx skills add …` install instructions anywhere in the kit (carry DEC-0072 §8 ban forward).
  - **Q19 — Installer / publish surface**:
    - **US-0017** parity: if script ships under `template/scripts/`, installer payload copies it (operator-verifiable via existing parity tests).
    - Publish surface: no new `package.json` runtime dep; no `npm` script registration required unless architecture decides to expose a convenience command. PO recommendation: no npm script in US-0090; operator invokes Python directly.

- **Updated architecture asks (for `/architecture`, DEC-xxxx hints, building on DEC-0072)**:
  - `DEC-xxxx` (input-side gate semantics): define exact activation rule for `CAVEMAN_COMPRESS_INPUT=1` + required-with-scope semantics for `CAVEMAN_FILE_SCOPE`.
  - `DEC-xxxx` (sidecar original policy): lock Q10 choice; specify path pattern and `.gitignore` stance.
  - `DEC-xxxx` (deny-list source of truth): lock Q11 choice; freeze deny-list contents with DEC revision policy.
  - `DEC-xxxx` (allow-list grammar): lock Q12 choice; specify empty-default = no-op.
  - `DEC-xxxx` (compression algorithm): lock Q9 choice; reference idempotency test strategy.
  - `DEC-xxxx` (reason-code vocabulary): lock Q15 final list verbatim.
  - `DEC-xxxx` (three-axis non-substitution): lock Q16 publication form; extend DEC-0072 §1 OR author a companion section in the new DEC.

- **Risks carried into research**:
  - (R1) Deny-list drift: hard-coded list falls behind repo reality if new canonical artifacts are added later without DEC update — mitigation: contract test listing every deny-list entry and asserting presence in the script.
  - (R2) Sidecar tree bloat: parallel-tree choice accumulates compressed-original pairs over time — mitigation: `--verify-originals --purge-orphans` subcommand (out of scope for MVP; research to flag).
  - (R3) Idempotency regression if prose rewrite is non-deterministic (e.g. ordering of filler-word strip) — mitigation: algorithm MUST be pure-deterministic (sorted, hash-stable); unit test enforces re-run equality.
  - (R4) Literal-region matcher misses a new zone introduced by a future DEC — mitigation: matcher reads the canonical 9-zone list from a single shared constant; extension requires DEC + test update; script emits `CAVEMAN_COMPRESS_LITERAL_REGION_DAMAGED` when any zone region differs post-write.

- **Non-goals carried into research**:
  - No change to **`TOKEN_PROFILE`** semantics (US-0080 / DEC-0062) — three-axis doc only.
  - No change to **US-0089** voice rule body except an optional "Input-side extension (US-0090)" subsection.
  - No rewrite of **DEC-0072**; US-0090 authors a companion DEC that **extends** DEC-0072 via §-references.
  - No vendor install path (`npx skills add …`) anywhere in the kit.
  - No change to strict-proof / isolation evidence wording (US-0056 / DEC-0038 / US-0048 / DEC-0029).
  - No mandatory auto-compress step in `/auto` pipeline.
  - No tokenizer change to Cursor itself.

- **Discovery outcome (US-0090)**: confidence raised on boundary clarity; the dependency graph on US-0089's shipped surface (scratchpad keys, literal-region invariant, non-substitution contract) is now explicit, and the deny-list + sidecar-originals + idempotency contract are scoped. **`R-0073`** remains **open** for `/research` (tech-lead) deepening on Q9–Q19 — no DEC yet. No new `R-` id allocated (shared anchor per DEC-0011 precedent and the US-0089 intake bundle plan_area_coverage).
- **Status authority**: **US-0090** remains **OPEN** in `docs/product/backlog.md` per **US-0045**; no acceptance rows checked in this phase. Next: **`/research`** (fresh **tech-lead**) for **US-0090**.

### Research phase resolution pass (2026-04-18, TL, `auto-20260418-01`, US-0090 input-side)

> Scope: resolve Q9–Q19 surfaced in the second Discovery extension above. Research phase deepens options and flags what must be locked by `/architecture` under a companion DEC to **`DEC-0072`** + `docs/engineering/architecture.md` **`# US-0090`**. **No DEC authored here.** **No architecture section authored here.** **No `R-xxxx` id allocated** — extension remains under the shared **`R-0073`** anchor (**DEC-0011** precedent; US-0089 intake bundle `plan_area_coverage` maps both stories). `fresh_context_marker=tl-US0090-research-20260418T210000Z-fresh`.

- **Scope re-confirmation**: Research authored **without rewriting** `DEC-0072`, `.cursor/rules/caveman.mdc` (active + `template/` verified byte-identical, SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`), or any architecture section. Canonical artifacts (`docs/product/backlog.md`, `docs/product/acceptance.md`, `docs/engineering/state.md`, `handoffs/intake_evidence/*.json`, `decisions/DEC-*.md`) are untouched outside the specified append points. No sprint tasks seeded.

- **Resolution matrix (Q9–Q19)**: eleven questions, zero still-open, two fully resolved as facts (architecture ratifies), nine narrowed with explicit `defer_to=architecture` decisions (options laid out; no lock attempted in research).

  - **Q9 — Compression algorithm choice** — `status=deferred_to_architecture`; `research_recommendation=hybrid two-tier`.
    - Option A (whitespace-collapse + filler-word strip + markdown-structure-preserving prose rewrite) is deterministic **only if** the filler-word list is a frozen sorted constant and every regex pass runs in fixed order. Fenced code, AC checklists, reason codes, IDs, and contract markers are skipped by the 9-zone matcher (reused verbatim from **`DEC-0072`** §4).
    - Option B (line-level minifier — collapse duplicate blank lines, trim trailing whitespace, normalize EOL to LF) is strictly deterministic by construction; minimal token savings but zero idempotency risk.
    - Option C (LLM-assisted compression) remains **rejected** (non-determinism violates **AC-6**; vendor coupling).
    - Research recommendation: architecture lock **Option B as the default** (`--mode=safe`) and offer **Option A layered under `--mode=aggressive`** for operators who accept the larger deny-list / regression-test surface. Rationale: keeps default operator experience inside the proven-idempotent envelope; aggressive mode is a named opt-in, not a silent upgrade. `defer_to=architecture`: final `--mode` grammar, whether aggressive mode ships in v1 or deferred to a follow-on story, and exact filler-word list contents.
    - Evidence refs: `docs/product/backlog.md` `## US-0090` discovery_notes (R3 idempotency risk); R-0073 second Discovery extension Q9; external anchor (not vendored): JuliusBrussee/caveman README discipline "compress touches prose, not code blocks" (cited in R-0073 intake extension).

  - **Q10 — Sidecar original naming** — `status=deferred_to_architecture`; `research_recommendation=Option B (parallel tree)`.
    - Option A (sibling dotfile `.<name>.caveman-original.<ext>`) scatters sidecars across every folder that holds a compressed file; per-folder `.gitignore` hygiene; high visibility but high maintenance.
    - Option B (parallel tree under `docs/.caveman-originals/<relative/path>/<file>`) needs a single repo-root `.gitignore` anchor (`docs/.caveman-originals/`); clean separation; requires relative-path reconstruction inside the script.
    - Option C (hash-suffix `<name>.<sha1>.caveman-original.<ext>`) is collision-safe but less human-readable and complicates `--verify-originals`.
    - Research recommendation: **Option B**. Rationale: one ignore anchor, mirrors the US-0085 philosophy of "one place, one repo-root `.gitignore` entry, no per-folder drift" (R-0072 finding), and keeps the sidecar tree inspectable via a single directory listing. `defer_to=architecture`: exact root path (candidate `docs/.caveman-originals/`), whether the root ships with a `.gitkeep` marker, and whether `.cursorignore` gains a parity entry or stays operator-owned per US-0085.
    - Evidence refs: R-0073 second Discovery extension Q10; R-0072 (US-0085 `.cursorignore` / `.gitignore` defense-in-depth) — `docs/engineering/research.md` **`R-0072`**; `docs/product/backlog.md` `## US-0090` discovery_notes (R6 secret leakage mitigation).

  - **Q11 — Deny-list source of truth** — `status=deferred_to_architecture`; `research_recommendation=Option C (hybrid, hard-coded baseline + `.gitignore` secret merge)`.
    - Option A (hard-coded constants): fastest and DEC-lockable but drifts if new canonical artifacts are added later without DEC update (R1 risk from the Discovery extension).
    - Option B (`.cursorignore` / `.gitignore` aware alone): insufficient — `.cursorignore` targets **agent file-context** exclusion, not script mutation (R-0072); `.gitignore` will not list DEC / backlog / state (they are **committed**, not ignored).
    - Option C (hybrid: hard-coded baseline **plus** `.gitignore` secret-pattern merge; optional `.cursorignore` overlay for operators who already maintain it): defense in depth, single DEC-revision policy for the canonical baseline, automatic tracking of `.env*` and other ignored secret patterns.
    - Research recommendation: Option C. The hard-coded baseline is **the backlog `## US-0090` discovery_notes hard deny-list** (enumerated below under Q18) lifted into a single Python constant; `.gitignore` merge covers repo-specific secret paths without manual DEC updates. `defer_to=architecture`: DEC-revision policy ("who can amend the hard-coded baseline, and through which DEC"), whether `.cursorignore` is merged by default or behind an opt-in flag, and how merge order is enforced (hard-coded **wins** over allow-list; ignore merges **add** denies but never remove).
    - Evidence refs: R-0073 second Discovery extension Q11; R-0072 (`.cursorignore` agent-exclusion semantics); `docs/product/backlog.md` `## US-0090` hard deny-list enumeration.

  - **Q12 — Allow-list grammar for `CAVEMAN_FILE_SCOPE`** — `status=deferred_to_architecture`; `research_recommendation=Option C (named profiles + raw globs)`.
    - Option A (comma-separated globs): flexible; no curated opinion; every operator writes their own glob set.
    - Option B (named profiles): curated, auditable, but limited unless a custom path exists.
    - Option C (hybrid: profile name **or** raw CSV globs **or** `profile:<name>;globs:<csv>` hybrid form): strictly more expressive than A or B; named profiles are reviewable defaults, raw globs escape-hatch for one-off operator scope.
    - Empty `CAVEMAN_FILE_SCOPE` (default) **must** evaluate to "no files in scope" (pure opt-in — confirmed by discovery R-0073 extension, DEC-0072 §3 documented-no-op semantics, and the **US-0045** status-authority principle).
    - Research recommendation: **Option C with a minimal v1 profile set** — single named profile `docs-prose-only` resolving to a frozen glob set (candidate: `docs/user-guides/**/*.md`, `docs/engineering/runbook.md`, `docs/engineering/state-archive/**/*.md`, `handoffs/archive/*.md`). Custom profiles added in future stories via DEC revision. `defer_to=architecture`: exact profile membership, precedence rules when profile + raw globs are both supplied, and what happens on unknown profile (research recommendation: fail closed with `CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE` candidate reason code under the Q15 vocabulary).
    - Evidence refs: R-0073 second Discovery extension Q12; `docs/product/backlog.md` `## US-0090` allow-list candidates section.

  - **Q13 — `dry-run` vs `write` UX** — `status=resolved` (concrete) **with** `defer_to=architecture` on flag conflict precedence.
    - Primary entrypoint: `scripts/caveman_compress_input.py` (candidate; final filename architecture-locked per Q17/Q19). Active + `template/scripts/` mirror per **US-0017**.
    - Required modes (all deterministic): `--dry-run` (default when invoked without a mutation mode; prints inventory + diff summary + deny-hits + literal-region sanity to stdout), `--write` (performs mutation; creates/updates sidecar), `--verify-originals` (no mutation; checks every compressed file has a valid sidecar per Q10 pattern), `--report` (emits JSON inventory to stdout; useful for CI gates).
    - Non-zero exit contract: **any** deny-list hit, scope violation, literal-region damage, idempotency break, or missing original (when `--verify-originals`) fails closed with the relevant reason code from the Q15 vocabulary. Exit code `0` only when **zero** violations and **zero** unresolved parity asserts.
    - Mode orthogonality: `--mode=safe|aggressive` (per Q9) applies to all mutation modes; `--dry-run --mode=aggressive` previews aggressive compression without writing. `--verify-originals` is mode-independent.
    - `defer_to=architecture`: flag conflict precedence (e.g. `--dry-run --write` simultaneously — research recommends fail-closed with `CAVEMAN_COMPRESS_FLAG_CONFLICT` candidate reason code; architecture ratifies), whether `--purge-orphans` ships in v1 or stays deferred (research recommends deferred — out-of-scope MVP per R-0073 R2), and whether `--report` supports multiple output formats.
    - Evidence refs: R-0073 second Discovery extension Q13; `docs/product/backlog.md` `## US-0090` UX flow bullet.

  - **Q14 — Idempotency test strategy (AC-6)** — `status=resolved` (concrete).
    - Fixture directory: `tests/fixtures/caveman_compress/` (active only; tests do not mirror to `template/` per existing US-0017 policy). Each fixture pairs `<name>.input.md` + `<name>.expected.md` + `<name>.sidecar.md` (reflecting the Q10 Option B path pattern relative to a fixture-root).
    - Required fixture classes (locked minimum set — architecture may **add** but must not **narrow**):
      1. **Whitespace baseline** — multi-blank-line collapse + trailing-whitespace trim + LF normalization (covers Option B safe-mode).
      2. **Filler-word strip** (aggressive only) — deterministic filler set removed; byte-equal on second run.
      3. **Literal-region preservation** — one fixture per 9-zone region (9 total): fenced code, file paths, AC checklists, reason codes (`ALL_CAPS_WITH_UNDERSCORES`), IDs (`US-xxxx` / `DEC-xxxx` / `R-xxxx` / `BUG-####` / `S0xxx` / `T-xxx`), contract markers (`[BUG_VALIDATION_OK]` / `[INTAKE_EVIDENCE_VALIDATION_OK]` / `[SCRATCHPAD_PAIR_OK]` / `[ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS]` / `[CODEBASE_MAP_OK]`), strict-proof tuple fields, isolation evidence fields, git/commit refs. Each fixture asserts byte-for-byte parity between input literal regions and output literal regions.
      4. **Deny-list refusal** — one fixture per deny-list entry class (enumerated under Q18): secret paths (`.env*`), intake evidence, canonical product/engineering docs, DEC files, sprint lifecycle evidence, binaries, installer/workflow/hook/rule/command/skill files. Each asserts the script exits non-zero with `CAVEMAN_COMPRESS_DENY_HIT` **before** any mutation.
      5. **Scope violation** — allow-list empty (default) → `CAVEMAN_COMPRESS_SCOPE_EMPTY`; glob outside allow-list → `CAVEMAN_COMPRESS_SCOPE_VIOLATION`.
      6. **Idempotency** — compress once, compress again, assert byte-equal (the canonical AC-6 fixture). Run under both safe and aggressive modes.
      7. **Mode-disabled** — `CAVEMAN_COMPRESS_INPUT=0` → script fails closed with `CAVEMAN_COMPRESS_MODE_DISABLED` without touching any file.
      8. **Original-missing** — `--verify-originals` on a compressed file whose sidecar is absent → `CAVEMAN_COMPRESS_ORIGINAL_MISSING`.
    - Test harness wiring: extend `tests/auto_command_contract_test.py` **in place** with a `test_caveman_compress_input_*` prefix **only after US-0090 ships** (US-0089 contract test set **unchanged** — `DEC-0072` §6 row 6 invariant preserved; new tests are **additions**, never modifications of existing `test_caveman_default_off_*` subtests). Add a new `run-tests` section (candidate `§26S` — architecture locks the number to match sprint-plan numbering convention).
    - Research recommendation stance: **concrete and implementation-ready**; architecture ratifies the fixture taxonomy + `run-tests` section number without decision tradeoffs.
    - Evidence refs: R-0073 second Discovery extension Q14; `docs/product/backlog.md` `## US-0090` AC-6 wording; `DEC-0072` §4 9-zone literal-region list; `DEC-0072` §6 `test_caveman_default_off_*` invariant.

  - **Q15 — Reason-code vocabulary** — `status=deferred_to_architecture`; `research_recommendation=adopt candidate set verbatim + two additions from Q12/Q13`.
    - Candidate set from R-0073 Discovery extension + `docs/product/backlog.md` `## US-0090` (7 canonical candidates):
      - `CAVEMAN_COMPRESS_SCOPE_VIOLATION` — allow-list glob resolved, but target path is outside resolved scope (post allow-list expansion).
      - `CAVEMAN_COMPRESS_DENY_HIT` — target path matches hard deny-list; deny wins over allow.
      - `CAVEMAN_COMPRESS_NOT_IDEMPOTENT` — second-run byte comparison fails; script refuses to overwrite.
      - `CAVEMAN_COMPRESS_LITERAL_REGION_DAMAGED` — 9-zone region differs post-write; script refuses to commit mutation.
      - `CAVEMAN_COMPRESS_ORIGINAL_MISSING` — `--verify-originals` or pre-write check found no sidecar for a compressed file.
      - `CAVEMAN_COMPRESS_MODE_DISABLED` — `CAVEMAN_COMPRESS_INPUT=0` (default) or unset; script refuses to run.
      - `CAVEMAN_COMPRESS_SCOPE_EMPTY` — `CAVEMAN_FILE_SCOPE=` empty (default); pure opt-in invariant violated.
    - Research adds two candidates for Q12 / Q13 gaps:
      - `CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE` — named profile referenced in `CAVEMAN_FILE_SCOPE` is not in the locked profile table (Q12 fail-closed).
      - `CAVEMAN_COMPRESS_FLAG_CONFLICT` — conflicting CLI flags (e.g. `--dry-run --write`; Q13).
    - All names match repo vocabulary (`ALL_CAPS_WITH_UNDERSCORES`, `CAVEMAN_COMPRESS_*` prefix, DEC-0038 / US-0088 style). All fit zone 4 of the `DEC-0072` §4 literal-region invariant automatically. All are **pre-write** or **during-write** fail-closed — no post-write reason codes proposed (a post-write failure would already be caught by `CAVEMAN_COMPRESS_LITERAL_REGION_DAMAGED` + `CAVEMAN_COMPRESS_NOT_IDEMPOTENT` ahead of commit).
    - `defer_to=architecture`: verbatim vocabulary lock in `docs/engineering/architecture.md` `# US-0090` + the companion DEC to **`DEC-0072`**; optional sync into `.cursor/rules/caveman.mdc` if Q17 adds a "Input-side extension (US-0090)" subsection.
    - Evidence refs: R-0073 second Discovery extension Q15; `docs/product/backlog.md` `## US-0090` reason-code candidates.

  - **Q16 — Three-axis non-substitution documentation form** — `status=deferred_to_architecture`; `research_recommendation=three parallel sentences (extend DEC-0072 §1 paragraph form)`.
    - Candidate forms: (A) parallel paragraphs, one per axis; (B) compact 2x2x2 table (`TOKEN_PROFILE × CAVEMAN_MODE × CAVEMAN_COMPRESS_INPUT`, 8 cells); (C) matrix with per-cell semantics.
    - Readability and maintenance: 2x2x2 is 8 dense cells and visually harder to scan; matrix is heaviest. DEC-0072 §1 already chose a 2D table for TOKEN_PROFILE × CAVEMAN_MODE; adding a third axis as a third table is symmetrically consistent **or** three sentences extending the existing non-substitution paragraph is even simpler and mirrors the `AUTO_QUIET` orthogonality precedent already in the runbook.
    - Research recommendation: **three parallel sentences** published verbatim in `docs/engineering/auto-orchestration-reference.md` and `docs/engineering/runbook.md` (active + `template/` mirrors). Draft (architecture ratifies exact wording):
      > "`TOKEN_PROFILE` controls context breadth. `CAVEMAN_MODE` controls reply voice. `CAVEMAN_COMPRESS_INPUT` controls input-side file mutation. None substitutes for another; setting one does not change the others. Combine freely."
    - Architecture option B fallback: if architecture prefers a 2x2x2 table for auditability, the table lives alongside (not replacing) the three-sentence paragraph. Architecture option C (matrix) is **not** recommended — adds doc surface for no semantic gain.
    - `defer_to=architecture`: exact wording, whether the table accompanies the sentences, and whether to extend `DEC-0072` §1 in the companion DEC or author a fresh §1 in that DEC that forward-links to `DEC-0072` §1.
    - Evidence refs: R-0073 second Discovery extension Q16; `DEC-0072` §1 non-substitution paragraph; `docs/engineering/auto-orchestration-reference.md` §TOKEN_PROFILE × CAVEMAN paragraph (already published).

  - **Q17 — Template parity touchpoints (AC-8 equivalent)** — `status=deferred_to_architecture`; `research_recommendation=8-row inventory below`.
    - Active/template pairs (exact list architecture-locked; research provides the baseline):
      1. `scripts/caveman_compress_input.py` (**new**) + `template/scripts/caveman_compress_input.py` (**new**) — byte-identical per US-0017.
      2. `docs/engineering/runbook.md` (operator UX section **addition** — dry-run → verify → write procedure; deny-list summary; `.gitignore` note for sidecar tree) + `template/docs/engineering/runbook.md` (mirror).
      3. `docs/engineering/auto-orchestration-reference.md` (three-axis non-substitution sentence **addition** per Q16) + `template/docs/engineering/auto-orchestration-reference.md` (mirror).
      4. `docs/engineering/architecture.md` `# US-0090` (**new section**; active only — story-scoped architecture sections do not mirror to `template/`, per existing DEC-0072 §7 row 6 pattern).
      5. `tests/auto_command_contract_test.py` (extended **in place** with `test_caveman_compress_input_*` subtests; active only — tests do not mirror).
      6. `tests/fixtures/caveman_compress/` (**new directory**; active only — fixtures do not mirror).
      7. `.gitignore` (add `docs/.caveman-originals/` anchor if Q10 Option B locked; active only — `.gitignore` is repo-scoped, not installed; kit installer does not own repo `.gitignore`).
      8. `.cursor/rules/caveman.mdc` optional "Input-side extension (US-0090)" subsection — **only if architecture decides** to surface the input-side deny-list + script pointer in the rule. If added, active + `template/` must stay byte-identical (research-verified current baseline SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`). If not added, rule is unchanged and the negative-parity row is tracked in sprint-plan.
    - Explicitly **NOT** touched by US-0090: `.cursorignore` (operator-owned per US-0085 architecture, unless architecture explicitly decides otherwise — research recommends leaving operator-owned and documenting in runbook), `package.json` (no new runtime dep per DEC-0072 §8 + discovery Non-goals), `.cursor/commands/*.md` (contract surfaces — deny-listed anyway), `docs/product/backlog.md` beyond the `## US-0090` research_notes + architecture_notes appendices, `docs/product/acceptance.md` (portfolio row stays unchecked until `/release`), `docs/engineering/state.md` (checkpoint appends only), `handoffs/intake_evidence/*.json`, `decisions/DEC-*.md` (new companion DEC is **added**, not "touched" in the parity sense), and `installer*` / `.github/workflows/*.yml` / `.cursor/hooks/*.py` / `.cursor/skills/**/SKILL.md`.
    - `defer_to=architecture`: final inventory lock in `# US-0090` + companion DEC §7 (mirror of `DEC-0072` §7), `.cursorignore` decision, rule-subsection decision, `.gitignore` exact anchor path (tied to Q10 Option B lock), and `run-tests` section number.
    - Evidence refs: R-0073 second Discovery extension Q17; `DEC-0072` §7 parity table (precedent); US-0017 parity policy.

  - **Q18 — Security / compliance boundary reaffirmation** — `status=resolved` (concrete; architecture ratifies verbatim).
    - **Non-negotiable** deny-list (hard-coded baseline per Q11 Option C):
      - Secrets: `.env`, `.env.*`, `**/.env`, `**/.env.*` (per **US-0085** / **R-0072**).
      - Intake evidence: `handoffs/intake_evidence/*.json`, `handoffs/intake_evidence/**/*.json` (per **US-0078** / **DEC-0060**; BUG-0007 class risk).
      - Canonical product authority: `docs/product/backlog.md`, `docs/product/acceptance.md` (per **US-0045** status authority).
      - Canonical engineering authority: `docs/engineering/state.md` (per **DEC-0040** artifact ordering), `docs/engineering/decisions.md`, `decisions/DEC-*.md` (canonical decision records; companion DEC for US-0090 is **added** not rewritten).
      - Sprint lifecycle evidence: `sprints/*/plan-verify.json`, `sprints/*/uat.json`, `sprints/*/summary.md`, `sprints/*/release-findings.md`, `sprints/*/qa-findings.md`, `sprints/*/tasks.md`, `sprints/*/sprint.md`.
      - Publish / runtime / install surfaces: `package.json`, `package-lock.json`, `installer.*` (all forms: `.sh`, `.ps1`, `.py`, `.js`, `.cmd`, `.bat`), `.github/workflows/*.yml`, `.cursor/hooks/*.py`, `bin/its-magic.js`, `packaging/homebrew/*.rb`.
      - Contract surfaces: `.cursor/rules/*.mdc`, `.cursor/commands/*.md`, `.cursor/skills/**/SKILL.md` (Caveman voice composes with them; compression must never rewrite them).
      - Manifest / parity sources: `docs/engineering/context/installer-owned-paths.manifest`, `docs/engineering/release-targets.json`, `docs/engineering/token-cost-parity-manifest.md`.
      - Binaries: `**/*.png`, `**/*.jpg`, `**/*.jpeg`, `**/*.gif`, `**/*.webp`, `**/*.pdf`, `**/*.zip`, `**/*.tar`, `**/*.tar.gz`, `**/*.tgz`, `**/*.ico`, `**/*.woff`, `**/*.woff2`, `**/*.ttf`, `**/*.eot`, `**/*.otf`, `**/*.mp3`, `**/*.mp4`, `**/*.mov`, `**/*.wav`, `**/*.bin`, `**/*.exe`, `**/*.dll`.
      - Vendor-install leak prevention: rule and runbook MUST NOT surface `npx skills add …` anywhere (carried forward from **`DEC-0072`** §8).
    - Deny always wins over allow — architecture-ratified ordering: **(1) evaluate hard deny-list → (2) evaluate `.gitignore` secret-pattern merge → (3) optional `.cursorignore` overlay → (4) only then evaluate `CAVEMAN_FILE_SCOPE` allow-list → (5) only then perform literal-region pre-write scan → (6) only then write + sidecar**. Any violation at any stage fails closed with the corresponding Q15 reason code.
    - Research stance: **resolved**; no architecture tradeoff remains on the baseline deny-list membership or ordering. Architecture ratifies verbatim in `# US-0090` + companion DEC.
    - Evidence refs: R-0073 second Discovery extension Q18; `docs/product/backlog.md` `## US-0090` discovery_notes hard deny-list; R-0072 (`.cursorignore` / `.gitignore` defense-in-depth); DEC-0072 §8 vendor-install ban; US-0085 `.env` deny anchor; US-0078 / DEC-0060 intake evidence integrity; US-0045 status authority; DEC-0040 artifact ordering.

  - **Q19 — Installer / publish surface** — `status=deferred_to_architecture`; `research_recommendation=manifest entry + no new npm script + optional parity script`.
    - `scripts/caveman_compress_input.py` must ship under `template/scripts/caveman_compress_input.py` per **US-0017** (Q17 row 1).
    - `docs/engineering/context/installer-owned-paths.manifest` (active + `template/`) must gain a `template/scripts/caveman_compress_input.py` entry under `install_include_paths` so `missing` / `upgrade` install modes both deliver the script (**BUG-0003** class risk — research explicitly flags this to avoid a repeat of the enforce-triad-hot-surface.py omission).
    - `package.json` `files` field already includes `template/` — no additional entry needed for the script itself. No new `package.json` runtime or dev dependency (per DEC-0072 §8 vendor-install ban and discovery Non-goals).
    - No new `npm` script registration. Operator invokes via `python scripts/caveman_compress_input.py --dry-run ...`. If architecture wants a convenience alias, it can add it in a future story without breaking US-0090 contracts.
    - Parity test: **two credible options** — (A) extend `scripts/check_intake_template_parity.py` with a `--scope=caveman-compress` mode; (B) add a focused `scripts/check_caveman_template_parity.py`. Research prefers **Option A** (extend existing script) to avoid script proliferation and match the BUG-0001 / BUG-0003 install-completeness pattern. `defer_to=architecture`: Option A vs B, exact CLI grammar for the extended script.
    - Publish smoke: recommend adding a single `installer_caveman_completeness_test.py` fixture (or extending the existing `installer_completeness_bug0003_test.py`) so `--mode missing` / `--mode upgrade` deliver `template/scripts/caveman_compress_input.py` to the target repo. Architecture locks the test surface.
    - `defer_to=architecture`: manifest entry placement (under `install_include_paths` vs a new caveman section), parity-test script choice (A vs B above), and install-completeness fixture strategy.
    - Evidence refs: R-0073 second Discovery extension Q19; `docs/engineering/context/installer-owned-paths.manifest`; BUG-0001 research closure (`R-0058`); BUG-0003 research closure (`R-0061`); US-0017 parity policy; DEC-0072 §8.

- **Unresolved / still-open**: **none**. Every Q9–Q19 has a concrete research stance with explicit `status=resolved` or `status=deferred_to_architecture`. Research does **not** claim any architectural decision authority.

- **Risks surfaced during resolution (carry to architecture / sprint-plan)**:
  - (R8) Q9 aggressive-mode filler-word list: if the list changes between releases, every previously-compressed-with-aggressive file risks becoming non-byte-equal on re-run — mitigation: architecture locks a DEC-revision policy for the list; `--mode=aggressive` emits the list hash in `--report` so operators can detect drift.
  - (R9) Q15 reason-code proliferation: the 9-code vocabulary (7 baseline + 2 additions) is at the upper edge of what fits on one reason-code page in the rule file. Mitigation: group into three families (scope, integrity, gating) in the architecture section + companion DEC; avoid further proliferation without DEC.
  - (R10) Q17 rule-subsection risk: if architecture adds a subsection to `.cursor/rules/caveman.mdc`, active + `template/` must stay byte-identical (US-0017); current research-verified SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` is the pre-US-0090 baseline and must be recomputed post-edit in the sprint-plan task acceptance evidence.
  - (R11) Q19 publish smoke omission: omitting the install-completeness fixture would reintroduce the exact defect class BUG-0003 fixed. Architecture must not ship US-0090 without this fixture even if sprint size pressure suggests it.

- **Architecture asks (updated; to be locked by /architecture under a companion DEC to `DEC-0072`)**:
  1. `DEC-xxxx` §1 — **Three-axis non-substitution**: exact wording (Q16); whether `DEC-0072` §1 is extended or §1 is authored fresh with a forward-link.
  2. `DEC-xxxx` §2 — **Input-side activation gate**: exact `CAVEMAN_COMPRESS_INPUT=1` + non-empty `CAVEMAN_FILE_SCOPE` activation semantics; empty-scope default fails closed with `CAVEMAN_COMPRESS_SCOPE_EMPTY`.
  3. `DEC-xxxx` §3 — **Sidecar original policy**: lock Q10 Option B path pattern + `.gitignore` anchor.
  4. `DEC-xxxx` §4 — **Deny-list source of truth**: lock Q11 Option C hybrid + DEC-revision policy for the hard-coded baseline.
  5. `DEC-xxxx` §5 — **Allow-list grammar**: lock Q12 Option C + v1 profile set membership + unknown-profile fail-closed behavior.
  6. `DEC-xxxx` §6 — **Compression algorithm**: lock Q9 hybrid tiering + filler-word list contents + `--mode` grammar.
  7. `DEC-xxxx` §7 — **Reason-code vocabulary**: lock Q15 9-code set verbatim; forbid post-write codes.
  8. `DEC-xxxx` §8 — **CLI contract**: lock Q13 flag grammar + conflict precedence + `--purge-orphans` deferral.
  9. `DEC-xxxx` §9 — **Template parity**: lock Q17 inventory + `.cursorignore` decision + rule-subsection decision.
  10. `DEC-xxxx` §10 — **Installer / publish**: lock Q19 manifest entry + parity-test strategy + install-completeness fixture.
  11. `DEC-xxxx` §11 — **Non-goals** (explicit forward-link to `DEC-0072` §8; reaffirm the carried bans).

- **Non-goals carried from discovery (unchanged)**: no `TOKEN_PROFILE` change, no rewrite of `DEC-0072`, no vendor install path, no strict-proof / isolation-evidence wording change, no mandatory auto-compress in `/auto`, no Cursor tokenizer change, no npm / pip runtime dep (stdlib-only Python), no canonical-artifact rewrites.

- **Research phase closure (US-0090)**: **PASS**. `R-0073` remains the shared anchor (US-0089 delivered; US-0090 research-phase extension appended). No new `R-xxxx` id allocated. Story **US-0090** remains **OPEN** in `docs/product/backlog.md` per **US-0045**; no acceptance rows checked. **Next**: **`/architecture`** (fresh **tech-lead**) — lock DEC-xxxx companion to `DEC-0072` + write `docs/engineering/architecture.md` `# US-0090`.

### Delivery closure (R-0073 — US-0090, 2026-04-19, curator, auto-20260418-01)

> Append-only closure trailer for R-0073. US-0090 shipped with S0076 released on 2026-04-19T00:05:00Z; this refresh-context pass reconciles the research anchor to `status=delivered` for **both** US-0089 **and** US-0090 scopes. No new research questions opened; no new R-xxxx id allocated; no rewrite of DEC-0072 or DEC-0073; no edits to architecture sections. `fresh_context_marker=curator-S0076-US0090-refresh-context-20260419T003000Z-fresh`.

- **Anchor status**: `R-0073.status=delivered` (US-0089 **delivered** @ 2026-04-18T20:00:00Z curator refresh; US-0090 **delivered** @ 2026-04-19T00:30:00Z curator refresh). Shared-anchor closure per DEC-0011 precedent; US-0089 intake bundle `plan_area_coverage` mapped both stories under R-0073.
- **US-0090 delivery coordinates**: sprint `S0076`; binding decision `DEC-0073` (composes on `DEC-0072` via forward-link, no rewrite); architecture section `docs/engineering/architecture.md` `# US-0090`; release commit `f0276d4` pushed `cfb37cf..f0276d4  main -> main`; release runtime proof `rp-auto-20260418-01-release-release-20260419T000500Z-S0076-US0090` / `proof_hash=0126c54efd3cc8158d9d0a687a66e9bce8f4eeefb89522993bb5ce805bb87e40`; refresh-context runtime proof `rp-auto-20260418-01-refresh-context-curator-20260419T003000Z-S0076-US0090` / `proof_hash=074d74d3650afe87854dc20d02524bf4330837701a2aefadb4dbfdbba3f57706`; AC-1..AC-8 all `[x]` in `docs/product/backlog.md` `## US-0090`.
- **Resolution matrix outcome**: all eleven Q9–Q19 questions resolved at /architecture → /sprint-plan and verified through /execute → /qa → /uat → /release. Q9 safe-mode minifier shipped; aggressive mode deferred to a future story by DEC-0073 §6 (R8 mitigation). Q10 Option B sidecar tree shipped with `.gitkeep` + repo-root `.gitignore` anchor. Q11 hybrid deny-list shipped (hard-coded baseline + `.gitignore` secret merge + optional `.cursorignore` overlay; deny wins). Q12 allow-list grammar shipped with `docs-prose-only` profile + raw globs + hybrid form. Q13 CLI grammar shipped (`--dry-run` default, `--write`, `--verify-originals`, `--report` with `--mode=safe` orthogonality). Q14 idempotency fixtures shipped (8 classes, 51 fixtures under `tests/fixtures/caveman_compress/`). Q15 reason-code vocabulary shipped verbatim (9 codes grouped into scope / integrity / gating families; all pre-write or during-write; no post-write codes). Q16 three-axis non-substitution sentences published in architecture verbatim and in reference/runbook as semantic paraphrase (carried-forward `PARTIAL_VERBATIM` note — non-blocking). Q17 8-row template parity shipped (script active + `template/`; runbook + reference active + `template/`; architecture section active-only; tests + fixtures active-only; `.gitignore` repo-scoped; `.cursor/rules/caveman.mdc` **unchanged** — negative parity preserved, SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`). Q18 security / compliance baseline ratified verbatim. Q19 installer parity shipped (`check_intake_template_parity.py --scope=caveman-compress` / `--scope=all` Option A; manifest entry under `install_include_paths`; `test_caveman_compress_input_shipped_by_installer` in `installer_completeness_bug0003_test.py`; no new npm runtime dep).
- **Risk resolution**: R8 (aggressive-mode filler-word drift) — mitigated by **deferral**; aggressive mode not shipped in v1 per DEC-0073 §6, so no drift surface exists. R9 (reason-code proliferation) — mitigated by DEC-0073 §7 grouping into 3 families; further additions require DEC revision. R10 (rule-subsection risk) — mitigated by **not** adding any input-side subsection to `.cursor/rules/caveman.mdc`; SHA-256 `E10EFC32…E47DE` verified byte-identical active == template end-to-end across discovery / research / architecture / sprint-plan / plan-verify / execute / qa / verify-work / release / refresh-context. R11 (install-completeness omission) — mitigated by new `test_caveman_compress_input_shipped_by_installer` fixture; BUG-0003 class defect reintroduction prevented.
- **Carried-forward non-blocking observations** (from `sprints/S0076/release-findings.md` / `handoffs/releases/S0076-release-notes.md`; recorded for operator visibility, not regressions):
  1. `PARTIAL_VERBATIM` on DEC-0073 §1 publication — architecture doc carries the verbatim three-sentence non-substitution paragraph; `docs/engineering/auto-orchestration-reference.md` and `docs/engineering/runbook.md` carry a semantic paraphrase. DEC-0072 §6 row 6 pinned test `test_caveman_default_off_reference_non_substitution_paragraph` preserved byte-unchanged. Optional future doc cleanup; no DEC amendment required.
  2. UAT-3 `--dry-run` vs `--write` narration variance — implementation binds `CAVEMAN_COMPRESS_SCOPE_EMPTY` reason code to the DEC-0073 §2 activation gate (`--write` pathway) per contract test `test_caveman_compress_input_scope_empty_reason`; UAT-spec's `--dry-run` command narrates gracefully by design. AC-4 fail-closed intent satisfied via `--write` evidence.
- **Evidence refs (US-0090 delivery)**: `sprints/S0076/release-findings.md` (PASS); `handoffs/releases/S0076-release-notes.md`; `sprints/S0076/uat.md` (15/15 PASS); `sprints/S0076/uat.json`; `sprints/S0076/qa-findings.md` (PASS cycle 1); `sprints/S0076/summary.md` (with Release phase + Refresh-context blocks); `sprints/S0076/plan-verify.json` (PASS); `decisions/DEC-0073.md`; `docs/engineering/architecture.md` `# US-0090`; `docs/product/backlog.md` `## US-0090` (DONE + AC-1..AC-8 `[x]` + `release_notes` + `refresh_context_notes`); `docs/product/acceptance.md` (US-0090 row `[x]`); `docs/engineering/status-normalization-report.md` (delta row); `handoffs/release_queue.md` (`S0076=released`); `handoffs/release_notes.md`; `docs/engineering/state.md` (Release + Refresh-context checkpoints).
- **Drain closure signal**: with US-0090 closed, `docs/product/backlog.md` now contains **zero** OPEN stories and **zero** OPEN bugs. The `/auto` orchestrator's backlog-drain segment closes here; the portfolio queue resumes at `/intake` on the next operator-initiated `/auto` invocation (no fresh drain candidate; `drain_terminated=true` with reason `no_open_stories`; `backlog_drain_stories_remaining_budget=4` of `10` left unused).
- **Open R-xxxx anchors status (post-closure)**: R-0073 **delivered** (this trailer). No `R-xxxx` currently `open`. Next research anchor allocation deferred to the next `/discovery`-phase subagent when a new story is intake'd.

### Post-delivery gap extension (2026-06-06, PO, `cursor-20260606-BUG0011-intake`)

- **Trigger**: operator `/ask` diagnosed **BUG-0011** — **US-0089** shipped Caveman gates/literals/toggles but `.cursor/rules/caveman.mdc` lacks upstream voice-compression rules (drop filler, fragments, lite/full/ultra semantics).
- **Upstream reference** (JuliusBrussee/caveman `skills/caveman/SKILL.md`, MIT): portable concepts remain **lite|full|ultra** level table, drop articles/filler/hedging/pleasantries, fragment OK at full/ultra, auto-clarity exceptions for security/destructive/ambiguous compression, pattern `[thing] [action] [reason]`.
- **Non-portable / out of scope for BUG-0011**: Wenyan modes; vendor token-percent claims; `npx skills add` install path.
- **Fix hypothesis for `/discovery`**: extend rule-only surface per **DEC-0072** Option A — add **Voice compression (when `CAVEMAN_MODE=1`)** section to `.cursor/rules/caveman.mdc` + runbook level table; additive contract-test token markers; template parity; precedence clause when **`CAVEMAN_MODE=1`** vs user-rule “complete sentences”.
- **Risk**: editing `caveman.mdc` changes SHA-256 pinned by **US-0090** negative-parity tests — sprint must update pinned hash intentionally or scope assertions to preserved substrings only (**TL** decision at **`/architecture`**).
- **Linked**: **BUG-0011**, **US-0089**, **DEC-0072**, **US-0090** (input compression orthogonal).

## R-0074 — US-0091: README ↔ backlog/acceptance feature coverage backfill + blocking drift gate

- **Date**: 2026-05-10
- **Topic**: **US-0091** — one-time audit of `README.md` against `docs/product/backlog.md` + `docs/product/acceptance.md` to identify and backfill missing **user-visible** feature descriptions, then add a **blocking** release-gate extension so feature coverage cannot drift again.
- **Query**: How does this kit currently keep `README.md` aligned with shipped user-visible features and flags, and what is the minimum surface needed to detect and prevent feature-coverage drift without duplicating `US-0030` (command/flag delta) or `US-0077` (audience profile)?
- **Sources**:
  - Internal: `docs/product/backlog.md` `US-0030` (release gate for command/flag documentation delta), `US-0077` (`DEC-0059` dual-README strategy), `US-0017` (template-drift guard), `US-0071` (user-visible metadata sanitization), `DEC-0040` (artifact ordering policy).
  - Internal: `README.md` (active, 1440 lines), `template/README.md` (mirror, 1440 lines), `docs/developer/README.md` (DEV shard per `US-0077`), `docs/engineering/runbook.md`.
  - Internal: `scripts/check-user-visible-metadata.py`, `scripts/validate_doc_profile.py`, `scripts/check_intake_template_parity.py` (existing validator patterns to compose with).
- **Findings (intake survey — extend in `/discovery` and `/research`)**:
  - **Adjacent gates**: `US-0030` already fires when commands/flags **change** without a corresponding README/runbook update. It does **not** assert that the *initial* description for an existing user-visible feature exists — so a feature shipped before `US-0030` was wired (or accepted under a path that did not flag a delta) can remain undocumented forever. `US-0091` closes this static-coverage gap.
  - **Audience boundaries**: `US-0077` / `DEC-0059` lock the dual-README strategy. The audit must respect existing `USER_*` H2s in root `README.md` and `DEV_*` H2s in `docs/developer/README.md` and **not** invent new section names; backfilled blurbs land in the appropriate H2 per `DOC_AUDIENCE_PROFILE` semantics.
  - **User-visible scope**: Per the operator's intake answer (`feature_set=user_visible`), pure-internal guards / invariant tests / refactors are out of scope (they should not appear in the user-facing surface anyway per `US-0071`). The audit's **input set** is therefore stories whose acceptance demonstrably surfaces a command, flag, file, or operator action.
  - **Parity surface**: `US-0017` template-drift guard already enforces `README.md` ↔ `template/README.md` parity; the new validator must reuse this rather than duplicate it.
  - **Validator pattern**: `scripts/validate_doc_profile.py` is the closest existing precedent for a deterministic README-section validator; the feature-coverage validator should follow the same stdlib-only Python posture and emit deterministic reason codes (e.g. `README_FEATURE_COVERAGE_GAP:<US-xxxx>`, `README_FEATURE_COVERAGE_PARITY_FAIL`, `README_FEATURE_COVERAGE_INPUT_INVALID`) under an umbrella `README_FEATURE_COVERAGE_BLOCKED`.
  - **Release-gate composition**: `US-0030` defines the existing release doc-delta gate. The `US-0091` blocking gate composes **as an extension** — `US-0091` adds a new check inside `/release`, and a single deterministic reason code surface for both static coverage and delta cases keeps remediation guidance unified.
- **Risks**:
  - **False positives** if "user-visible" is not bounded deterministically — the validator may flag DONE stories that legitimately have no user-facing surface. Mitigation: explicit per-story `user_visible: true|false` marker (or default-true with deny-list) authored into the story acceptance schema during sprint planning, with validator fail-closed on ambiguous input.
  - **One-time-vs-permanent drift** — backfilling 90+ stories in one sprint risks README bloat and audience-profile contradiction (`US-0077`). Mitigation: short blurbs (1-2 sentences per feature) bound to a single per-profile section budget; `validate_doc_profile.py` already enforces section budgets per audience cell.
  - **Template/dev-shard parity drift** — three target files (root `README.md`, `template/README.md`, `docs/developer/README.md`) means three places to keep in sync; mitigation: extend `US-0017` parity check or add a dedicated parity scope.
  - **Pre-existing release lock-in** — composing with `US-0030` means a future operator running `/release` after `US-0091` ships could be blocked retroactively. Mitigation: a one-time grandfathering or initial-population gate in the same sprint that delivers the blocking validator (architecture decision).
- **Next phase pointers (`/discovery` → `/research` → `/architecture`)**:
  - `/discovery`: deterministic "user-visible feature" predicate; section budget per audience profile; agree per-story marker location (acceptance.md row vs backlog block field).
  - `/research`: validator placement (`scripts/validate_readme_feature_coverage.py` candidate); reason-code vocabulary; release-gate wiring point (active and `template/`); migration / grandfathering options for existing DONE stories with no current README blurb.
  - `/architecture`: lock companion DEC composing on `DEC-0030` (US-0030 release gate) and `DEC-0059` (US-0077 audience profiles); sidecar migration plan; template parity inventory.
- **Linked**: US-0091, US-0030, US-0077, US-0017, US-0071, DEC-0040, DEC-0059
- **Confidence**: medium (intake survey only; `/research` will deepen)
- **Status**: open — `/discovery` (PO) extends boundary, then `/research` (tech-lead) deepens before `/architecture`

### Discovery extension (2026-06-06, PO, `orchestrator_run_id=auto-20260606-01`, `fresh_context_marker=po-US0091-discovery-20260606T132027Z-fresh`)

- **Predicate lock**: backlog block field **`user_visible: true|false`** is canonical validator input; acceptance.md optional `(user_visible)` suffix is human-scan only. In-scope = **DONE** + explicit `true` or migration-heuristic pass for unset; out-of-scope = explicit `false` or pure-internal invariant surface. Ambiguous → **`README_FEATURE_COVERAGE_INPUT_INVALID`**.
- **Migration heuristic (one-time, unset fields only)** — candidate signals for `/research` to normative-lock:
  1. Backlog summary or acceptance title references a slash-command (`/intake`, `/auto`, etc.).
  2. Backlog or acceptance mentions a scratchpad key pattern (`KEY=value` or documented flag name).
  3. Backlog cites operator CLI invocation (`python scripts/...` with user-facing purpose).
  4. DONE bug with `expected`/`actual` describing changed operator behavior → default **in-scope** unless `user_visible: false`.
  5. Pure-internal keywords (`archiver`, `template parity guard`, `intake evidence schema`, `hot-surface rollover`) without operator action → default **out-of-scope**.
- **Coverage anchor**: detectable mention required in README family — root bullet/sub-entry (command/flag/capability name or `US-xxxx`/`BUG-xxxx` id) + DEV shard row (id + scratchpad flags). **No new H2s**; section affinity per `doc_profile_lib.py` / **DEC-0059** (commands → `Commands and workflow`; modes → `Commands and workflow` or `Other useful capabilities`; distribution → `Features`; dev governance → DEV `Workflow` / `Quality gates` / `Engineering decisions`).
- **Validator candidate**: `scripts/validate_readme_feature_coverage.py` — stdlib-only, `--self-test`, `--report` with stable JSON counts, umbrella **`README_FEATURE_COVERAGE_BLOCKED`** + sub-codes per acceptance **AC-5**.
- **Release composition**: second check inside existing `/release` doc-gate surface (**US-0030** unchanged); research must locate exact hook in `validate-and-push` / release command chain (active + `template/`).
- **Grandfathering**: blocking enablement same commit as backfill merge; pre-backfill DONE items must not block `/release` (**AC-10** architecture decision).
- **Audit artifact**: deterministic gap report (JSON preferred) listing `coverage_total` / `coverage_present` / `coverage_missing` + per-id anchor target — produced during execute, referenced by validator self-test fixtures.
- **Research asks (next phase)**: normative heuristic table; CLI/`--report` schema; release wiring point; section-affinity manifest CSV/JSON; grandfathering toggle; template parity extension for new script.
- **Discovery outcome**: **PASS** — no decision gate; **`/research`** (tech-lead) deepens before **`/architecture`**.

### Research extension (2026-06-06, TL, `orchestrator_run_id=auto-20260606-01`, `fresh_context_marker=tl-US0091-research-20260606T140500Z-fresh`)

- **Closure**: **`/research`** **PASS** for **US-0091**. All six discovery research asks resolved; **no decision gate**; **`/architecture`** next.
- **Repo survey (2026-06-06)**:
  - Backlog: ~90 `## US-xxxx` story blocks + 11 `### BUG-xxxx` blocks; **zero** existing `user_visible:` markers — migration heuristic required for first predicate pass.
  - Root `README.md`: ~52 `US-xxxx`/`BUG-xxxx` token hits (traceability scattered); `Features` / `Commands and workflow` / `Other useful capabilities` H2s present; coverage incomplete vs DONE user-visible inventory.
  - `docs/developer/README.md`: six `DEV_*` H2s per **DEC-0059**; sparse per-story rows (governance prose only).
  - `template/README.md`: byte-parity with root per **US-0017** (1440 lines each at intake survey).
  - **US-0030** doc-delta gate: process-level step in release workflow (command/runbook guidance); **no** dedicated `scripts/*` delta validator today — **US-0091** adds the first **scripted** static-coverage gate composed alongside it.
  - Precedent validators: `scripts/validate_doc_profile.py` + `doc_profile_lib.py` (profile/section budgets); `scripts/bug_issue_validate.py` + `bug_issue_lib.py` (backlog block parsing); `scripts/check_intake_template_parity.py` (scoped byte-parity tables).

#### 1. User-visible predicate — implementation options

| Option | Mechanism | Pros | Cons | Verdict |
|--------|-----------|------|------|---------|
| **A (recommended)** | Backlog block field `user_visible: true\|false`; validator reads **backlog only** | Deterministic, auditable, matches discovery lock; explicit deny-list for internal stories | Requires one-time marker authoring during backfill sprint | **Adopt** |
| B | Parse `docs/product/acceptance.md` `(user_visible)` suffix | Human-scan alignment | Violates discovery lock; acceptance not canonical for machine gate | **Reject** |
| C | Heuristic-only (no explicit marker) | No marker migration | Unbounded false positives; blocks `/release` unpredictably | **Reject** |
| D | Git-diff delta only (extend US-0030) | Reuses existing gate | Does not solve static-coverage gap (AC-2) | **Out of scope** |

**Predicate algorithm (normative sketch for architecture)**:

```
for each work_item in parse_backlog(backlog.md):
  if work_item.kind not in {US, BUG}: skip
  if work_item.status != DONE: skip
  if work_item.user_visible == false: skip (out-of-scope)
  if work_item.user_visible == true: in_scope
  elif work_item.user_visible unset:
    classify = migration_heuristic(work_item)  # one-time pass only
    if classify == ambiguous: emit README_FEATURE_COVERAGE_INPUT_INVALID
    elif classify == in_scope: in_scope
    else: skip
  else: README_FEATURE_COVERAGE_INPUT_INVALID  # malformed value
```

**Migration heuristic table (unset `user_visible` only; architecture locks verbatim)**:

| Signal ID | Pattern (case-sensitive where noted) | Scope | Notes |
|-----------|--------------------------------------|-------|-------|
| H1 | `/(?:^|\s)(/[a-z][a-z0-9-]*)/` in summary/title/acceptance bullets | **in** | Slash-commands (`/intake`, `/auto`, `/release`, …) |
| H2 | Scratchpad key `^[A-Z][A-Z0-9_]+=` or backtick-wrapped key name in summary | **in** | Operator-configurable flags |
| H3 | `python scripts/[a-z0-9_./-]+\.py` in summary with operator-facing verb | **in** | CLI validators operators run |
| H4 | BUG `expected`/`actual` fields describe operator-visible behavior change | **in** | Default **in** unless `user_visible: false` |
| H5 | Keywords `archiver`, `hot-surface rollover`, `intake evidence schema`, `template parity guard`, `triad` without H1–H4 | **out** | Pure-internal invariant surfaces |
| H6 | Summary contains both H5 **and** H1–H4 | **in** | Operator action wins |
| H7 | No H1–H6 match on DONE story | **ambiguous** → `README_FEATURE_COVERAGE_INPUT_INVALID` | Forces explicit marker during backfill |
| H8 | No H1–H6 match on DONE bug | **out** | Bugs default out unless H4 or explicit `user_visible: true` |

Post-backfill: architecture SHOULD require explicit `user_visible:` on all new DONE items; heuristic path disabled when `README_FEATURE_COVERAGE_ENFORCE=1` (see §6).

#### 2. Audit report format (`--report` / gap artifact)

Stable JSON (sorted keys; UTF-8; LF; no timestamps inside report body for idempotence):

```json
{
  "coverage_missing": ["US-0048", "BUG-0003"],
  "coverage_present": ["US-0030", "US-0077"],
  "coverage_total": 42,
  "gaps": [
    {
      "dev_h2": "Quality gates",
      "id": "US-0048",
      "kind": "US",
      "predicate_source": "heuristic:H1",
      "root_h2": "Commands and workflow",
      "user_visible": true
    }
  ],
  "report_schema_version": 1,
  "repo_root": ".",
  "status": "FAIL"
}
```

- `status`: `PASS` when `coverage_missing` empty and no input/parity/profile violations; else `FAIL`.
- Gap rows sorted by `id` ascending.
- Audit artifact path (execute phase): `docs/engineering/context/readme-feature-coverage-audit.json` (active-only snapshot; not mirrored to `template/` — generated evidence per **DEC-0040**).
- Self-test fixtures: `tests/fixtures/readme_feature_coverage/` (minimal trees).

#### 3. Validator API sketch

**Entrypoint**: `scripts/validate_readme_feature_coverage.py` (stdlib-only; mirrors `validate_doc_profile.py` CLI posture).

**Library** (recommended): `scripts/readme_feature_coverage_lib.py` — predicate, README index builder, affinity resolver, reason-code emitter (same split as `bug_issue_lib` / `doc_profile_lib`).

| Flag | Purpose |
|------|---------|
| `--repo PATH` | Target repo root (default: parent of `scripts/`) |
| `--backlog PATH` | Backlog file (default: `docs/product/backlog.md`) |
| `--self-test` | Predicate matrix + report schema stability tests → `[README_FEATURE_COVERAGE_SELF_TEST_OK]` |
| `--report` | Emit stable JSON to stdout (AC-7 idempotence) |
| `--audit-out PATH` | Write gap artifact (execute/audit mode) |
| `--enforce` | Blocking mode (default when invoked from `/release`); without: report-only for migration |
| `--no-template-parity` | Skip active vs `template/` script/README parity sub-check |

**Exit codes**: `0` = pass; `1` = `README_FEATURE_COVERAGE_BLOCKED` (one or more sub-codes on stderr); `2` = invocation/self-test failure.

**Reason codes (umbrella + sub-codes per AC-5)**:

| Code | When |
|------|------|
| `README_FEATURE_COVERAGE_BLOCKED` | Umbrella on stderr first line |
| `README_FEATURE_COVERAGE_GAP:<US-xxxx\|BUG-xxxx>` | In-scope DONE item missing coverage anchor |
| `README_FEATURE_COVERAGE_PARITY_FAIL` | `README.md` ≠ `template/README.md` or script pair mismatch |
| `README_FEATURE_COVERAGE_INPUT_INVALID` | Ambiguous predicate / malformed `user_visible` |
| `README_FEATURE_COVERAGE_PROFILE_VIOLATION` | Backfill would exceed `validate_doc_profile.py` section budget |

**Coverage detection** (per in-scope id):

- **Root**: bullet or sub-entry under expected `root_h2` containing (a) slash-command token, (b) scratchpad key name, or (c) case-sensitive `\bUS-\d{4}\b` / `\bBUG-\d{4}\b` — root blurbs SHOULD prefer (a)/(b) per **US-0071** (IDs allowed in DEV shard primarily).
- **DEV shard**: table row or bullet under expected `dev_h2` containing id + at least one scratchpad key or `related_us` pointer.
- Post-check: invoke `validate_doc_profile.py` logic (import `doc_profile_lib`) for profile budget — map violations to `README_FEATURE_COVERAGE_PROFILE_VIOLATION`.

#### 4. Release-gate composition with US-0030

**US-0030** (delta-driven): release subagent compares command/flag **changes in sprint scope** against README/runbook updates — remains **unchanged** and primarily **process/agent-driven** today.

**US-0091** (static-coverage): **scripted** second check — deterministic inventory of all DONE user-visible items vs README family.

**Recommended wiring (Option A — release command step)**:

| Surface | Change |
|---------|--------|
| `.cursor/commands/release.md` | New step **`3f. README feature coverage gate (US-0091)`** after `3e` legacy drift, before step `4` UAT: run `python scripts/validate_readme_feature_coverage.py --repo . --enforce` when `README_FEATURE_COVERAGE_ENFORCE=1` in merged scratchpad; when `0`, skip with `skipped` evidence (grandfathering). Fail → `README_FEATURE_COVERAGE_BLOCKED` + sub-codes in `sprints/Sxxxx/release-findings.md`. |
| `template/.cursor/commands/release.md` | Byte-identical step **3f** block |
| `docs/engineering/runbook.md` + `template/...` | Subsection linking US-0030 doc-delta (manual) + US-0091 static coverage (scripted); remediation vocabulary table |
| `tests/run-tests.ps1` + `tests/run-tests.sh` | New section (candidate `§27`): self-test + report idempotence fixture |

**Rejected alternatives**:

- **Option B** — wire into `validate-and-push` / `sync_push_gates.py`: wrong lifecycle (pre-push ≠ release); would block pushes before backfill sprint completes.
- **Option C** — fold into `validate_doc_profile.py`: conflates audience profile budgets with feature inventory coverage; separate reason-code families required.

**Gate order within doc-gate family**: US-0030 doc-delta (agent checklist) → US-0091 static coverage (script) → both recorded in `release-findings.md` § doc gates.

#### 5. Section-affinity manifest

Ship as `docs/engineering/context/readme-section-affinity.json` (active + `template/` mirror per **US-0017**):

```json
{
  "affinity_version": 1,
  "rules": [
    {"tag": "slash_command", "root_h2": "Commands and workflow", "dev_h2": "Workflow"},
    {"tag": "scratchpad_mode", "root_h2": "Other useful capabilities", "dev_h2": "Quality gates"},
    {"tag": "distribution", "root_h2": "Features", "dev_h2": "Architecture notes"},
    {"tag": "release_gate", "root_h2": "Commands and workflow", "dev_h2": "Quality gates"},
    {"tag": "governance", "root_h2": "Other useful capabilities", "dev_h2": "Engineering decisions"}
  ]
}
```

Classifier picks first matching tag from backlog `Summary` keywords / slash-command presence; default fallback: `slash_command` when H1 matches else `governance`. Architecture locks tag→H2 mapping; **no new H2 literals**.

#### 6. Grandfathering / first-activation toggle (AC-10)

| Option | Mechanism | Verdict |
|--------|-----------|---------|
| **A (recommended)** | Scratchpad key `README_FEATURE_COVERAGE_ENFORCE=0\|1` (default **`0`**). Validator `--enforce` no-op when `0` (exit 0, print `skipped`). Flip to **`1`** in same commit as backfill merge + runbook note. | **Adopt** — matches **DEC-0058** merged-scratchpad gate pattern |
| B | Baseline manifest listing covered ids at activation | Auditable but duplicates backlog predicate; drift if manifest stale |
| C | Time-boxed env var | Not scratchpad-visible; poor operator UX |

Architecture companion **DEC-xxxx** MUST document: predicate rules, composition with **DEC-0030**/**US-0030** + **DEC-0059**, grandfathering flip procedure, heuristic disablement when enforce=1.

#### 7. Template parity inventory (US-0017 / AC-9)

Extend `scripts/check_intake_template_parity.py` with `--scope=readme-feature-coverage`:

| Active | Template |
|--------|----------|
| `scripts/validate_readme_feature_coverage.py` | `template/scripts/validate_readme_feature_coverage.py` |
| `scripts/readme_feature_coverage_lib.py` | `template/scripts/readme_feature_coverage_lib.py` |
| `docs/engineering/context/readme-section-affinity.json` | `template/docs/engineering/context/readme-section-affinity.json` |
| `.cursor/commands/release.md` (step 3f hunk only — or full-file parity per existing US-0017 policy) | `template/.cursor/commands/release.md` |
| `docs/engineering/runbook.md` (feature-coverage subsection) | `template/docs/engineering/runbook.md` |
| `docs/engineering/context/installer-owned-paths.manifest` (new script paths) | `template/.../installer-owned-paths.manifest` |

Compose with existing **US-0017** README byte-parity guard (do not duplicate root↔template README diff logic inside new validator — call parity check or rely on dedicated guard).

#### 8. External references (EARLY_RESEARCH=1)

| Ref | Takeaway for US-0091 |
|-----|---------------------|
| [borghei/Claude-Skills doc-drift-detector](https://github.com/borghei/Claude-Skills/blob/main/engineering/doc-drift-detector/SKILL.md) | Stdlib-only CLI scoring README completeness; `--threshold` CI gate pattern — adopt idempotence + JSON report shape, reject AST/doc-code coupling (we trace backlog ids not Python symbols) |
| [pytreqt](https://github.com/joernpreuss/pytreqt) | Requirement-id ↔ test traceability matrix — adopt sorted gap report + bidirectional id vocabulary (`US-xxxx`/`BUG-xxxx`) |
| [Fiberplane drift](https://fiberplane.com/blog/drift-documentation-linter/) | Anchor/provenance model for staleness — informative only; US-0091 uses backlog predicate not git provenance |
| [ryanwaits/drift](https://github.com/ryanwaits/drift) | `drift ci --min N` coverage floor — adopt blocking CI/release gate posture, not npm coupling |

#### 9. Risks (carried to architecture)

| ID | Risk | Mitigation |
|----|------|------------|
| R1 | False positives block `/release` | Explicit `user_visible:` markers + H7 fail-closed → forces resolution at backfill |
| R2 | README bloat (~90 items) | 1–2 sentence blurbs; `validate_doc_profile.py` budget check maps to `README_FEATURE_COVERAGE_PROFILE_VIOLATION` |
| R3 | Three-file parity drift | US-0017 README guard + scoped parity script; `README_FEATURE_COVERAGE_PARITY_FAIL` |
| R4 | Retroactive lock-in | `README_FEATURE_COVERAGE_ENFORCE=0` until backfill merges (same sprint) |
| R5 | US-0071 leakage in root blurbs | Prefer command/flag tokens in root; IDs in DEV shard; run `check-user-visible-metadata.py` on changed paths |
| R6 | Heuristic ambiguity at scale | H7 forces explicit marker; execute sprint authors `user_visible:` for all DONE stories |
| R7 | US-0030 / US-0091 operator confusion | Runbook subsection: delta=changes this sprint; static=all DONE user-visible inventory |

#### 10. Architecture asks (no DEC authored in research)

1. Lock companion **DEC-xxxx** §§: predicate + heuristic table + enforce key + reason codes + US-0030/US-0091 composition diagram.
2. Confirm `readme_feature_coverage_lib.py` split vs monolithic script.
3. Lock `§27` (or next) run-tests section id.
4. Decide whether step **3f** uses merged scratchpad `README_FEATURE_COVERAGE_ENFORCE` only or also accepts `--enforce` CLI override for CI fixtures.

- **Research outcome**: **PASS** — no decision gate; **`/architecture`** (tech-lead) locks **DEC-xxxx** + `architecture.md` `# US-0091`.
- **Confidence**: high (predicate + wiring + parity inventory resolved; architecture owns DEC wording)
- **Status**: open for architecture closure — do not flip **US-0091** to DONE until `/release`

### Delivery closure (R-0074 — US-0091, 2026-06-06, curator, auto-20260606-01)

> Append-only closure trailer for R-0074. US-0091 shipped with S0077 released on 2026-06-06T13:43:20Z; this refresh-context pass reconciles the research anchor to `status=delivered`. No new research questions opened; no new R-xxxx id allocated; no rewrite of DEC-0074 or architecture `# US-0091`. `fresh_context_marker=curator-S0077-US0091-refresh-context-20260606T135000Z-fresh`.

- **Anchor status**: `R-0074.status=delivered` (US-0091 **delivered** @ 2026-06-06T13:50:00Z curator refresh). Single-story anchor; no shared-anchor split required (distinct from R-0073 precedent).
- **US-0091 delivery coordinates**: sprint `S0077`; binding decision `DEC-0074` (composes on `DEC-0059`; extends US-0030 release doc-gate family without rewrite); architecture section `docs/engineering/architecture.md` `# US-0091`; release runtime proof `rp-auto-20260606-01-release-release-20260606T134320Z-S0077-US0091` / `proof_hash=cbfc031254b549dfef27f12c4a6d5acb51b528835180b60252e54b44d238bd47`; refresh-context runtime proof `rp-auto-20260606-01-refresh-context-curator-20260606T135000Z-S0077-US0091` / `proof_hash=1fe3a39c7fd03d128b3b61e68b9a07593739bd0bd290c7b109f4e23269aff1e9`; AC-1..AC-10 all `[x]` in `docs/product/backlog.md` `## US-0091`.
- **Resolution matrix outcome**: all discovery/research asks resolved at `/architecture` → `/sprint-plan` and verified through `/execute` → `/qa` → `/verify-work` → `/release`. Predicate Option A (`user_visible:` + H1–H8 heuristic) shipped; validator lib split shipped; release step **3f** composed on US-0030; three-file README backfill complete (`coverage_missing=[]`, `coverage_total=98`); `README_FEATURE_COVERAGE_ENFORCE=1` post-backfill; harness **§27U** green; template parity `--scope=readme-feature-coverage` PASS.
- **Risk resolution**: R1 (false positives) — mitigated by explicit `user_visible:` markers + H7 fail-closed on ambiguity. R2 (README bloat) — mitigated by short blurbs within existing H2 budgets per DEC-0059. R3 (three-file parity) — mitigated by US-0017 guard + scoped parity script. R4 (retroactive lock-in) — mitigated by same-sprint backfill + enforce flip. R5 (US-0071 leakage) — mitigated by metadata scan PASS on changed paths. R6 (heuristic ambiguity) — mitigated by execute-time marker authoring. R7 (US-0030/US-0091 confusion) — mitigated by runbook subsection (delta vs static inventory).
- **Evidence refs (US-0091 delivery)**: `sprints/S0077/release-findings.md` (PASS); `handoffs/releases/S0077-release-notes.md`; `sprints/S0077/uat.md` (10/10 PASS); `sprints/S0077/uat.json`; `sprints/S0077/qa-findings.md` (PASS cycle 1); `sprints/S0077/summary.md` (Release + Refresh-context blocks); `sprints/S0077/plan-verify.json` (PASS); `decisions/DEC-0074.md`; `docs/engineering/architecture.md` `# US-0091`; `docs/product/backlog.md` `## US-0091` (DONE + AC-1..AC-10 `[x]` + `release_notes` + `refresh_context_notes`); `docs/product/acceptance.md` (US-0091 row `[x]`); `handoffs/release_queue.md` (`S0077=released`); `docs/engineering/state.md` (Release + Refresh-context checkpoints).
- **Drain closure signal**: with US-0091 closed, `docs/product/backlog.md` contains **zero** OPEN stories and **three** OPEN bugs (`BUG-0009..BUG-0011`). Story-drain segment closes here; bug queue resumes at `/discovery` for `BUG-0009` on next `/auto` invocation (`drain_terminated=false`; `backlog_drain_stories_remaining_budget=3`).
- **Open R-xxxx anchors status (post-closure)**: R-0074 **delivered** (this trailer). No `R-xxxx` currently `open` for active story work. Next research anchor allocation deferred to the next `/discovery`-phase subagent when a new story or bug segment begins.

## R-0075 — BUG-0009: downstream-safe template CI vs kit-internal self-packaging CI

- **Anchor**: `bug_id=BUG-0009`; intake evidence `handoffs/intake_evidence/BUG-0009-intake-20260606.json`; related **US-0007**, **US-0008**, **US-0017**, **US-0018**, **US-0063**.
- **Status**: `delivered` (delivery closure trailer below; curator refresh **2026-06-06T16:20:00Z**).

### Discovery extension (2026-06-06, PO, `auto-20260606-02`, `fresh_context_marker=po-BUG0009-discovery-20260606T141500Z-fresh`)

#### 1. Confirmed defect mechanics

- `template/.github/workflows/ci.yml` and `.github/workflows/ci.yml` are **byte-identical** today (SHA-256 `e51d2cb100e8821cd1b34fae68a6e973617858aece04aa4441fb2785b5319891`).
- Installer manifest copies `.github/workflows` as a directory; all three entrypoints (`installer.ps1`, `installer.sh`, `installer.py`) hydrate from `template/`.
- Leaked jobs reference kit-only paths: `npm pack` / `its-magic-*.tgz`, `sh installer.sh`, `packaging/chocolatey`, `packaging/homebrew` (`brew style packaging/homebrew/its-magic.rb`).
- `template/.github/workflows/deploy.yml` is already downstream-safe (runbook-driven `workflow_dispatch` only) — **no change**.

#### 2. Discovery-locked fix boundary

| Surface | After fix | Rationale |
|---------|-----------|-----------|
| `template/.github/workflows/ci.yml` | `checks` + `auto-fix` only | Downstream-safe generic CI |
| `.github/workflows/ci.yml` (active) | All five jobs retained | Kit self-distribution validation |
| `US-0017` byte parity | **Exception** for `ci.yml` | Intentional divergence; negative-parity + drift guard |

#### 3. checks empty-project semantics (operator-locked)

- When all runbook command keys are empty/skipped → job **PASS** + explicit summary (`no tests configured yet`).
- `Fail if tests or lint failed` fires only when a **configured** test/lint step returns `failure`.
- Open tension: template `runbook.md` ships non-empty `TEST_COMMAND` (powershell harness) while **DEC-0056** documents blank-until-bootstrap — research must recommend fresh-install default.

#### 4. Research questions (for `/research` tech-lead)

1. **Template CI shape**: subtract jobs in-place vs separate `ci-downstream.yml` filename (manifest/installer implications).
2. **Drift guard**: dedicated `scripts/check_downstream_ci_guard.py` vs extend `tests/auto_command_contract_test.py`; forbidden pattern list; harness section id.
3. **Runbook bootstrap**: interaction between **US-0063** stack-aware bootstrap and downstream `checks` green-by-default on day zero.
4. **Parity policy**: `check_intake_template_parity.py --scope=ci-downstream` vs negative-parity contract test only.
5. **Install/upgrade smoke**: assert post-install `ci.yml` job inventory (`checks`, `auto-fix` present; `npm-test`/`brew-test`/`choco-test` absent).
6. **Release/docs**: upgrade remediation wording for operators with pre-fix `ci.yml`.

#### 5. Risks

- **R1**: Strip packaging jobs from active CI by mistake — mitigation: drift guard targets **template only**; active CI contract test asserts five jobs remain.
- **R2**: Stale broken repos until upgrade — accepted scope; docs must be explicit.
- **R3**: False-green if installer copies wrong workflow file — mitigation: install-completeness fixture (BUG-0003 class).

- **Discovery outcome**: **PASS** — no decision gate; **`/research`** (tech-lead) resolves Q1–Q6 before **`/architecture`**.
- **Confidence**: high (root cause confirmed; boundary locked; implementation details deferred)

### Research extension (2026-06-06, tech-lead, `auto-20260606-02`, `fresh_context_marker=tl-BUG0009-research-20260606T155605Z-fresh`)

#### External references (EARLY_RESEARCH=1)

- **Workflow templates vs reusable workflows** ([Zenn — reusable workflows basics](https://zenn.dev/atsushifx/articles/ci-gha-reusable-workflows-01-basics?locale=en)): starter/workflow **templates are copied** into each repo and do **not** auto-update; reusable workflows require a **caller `uses:` ref** to an external repo. its-magic's installer model is template-copy (**US-0008**), so decoupling belongs in the **shipped `template/.github/workflows/ci.yml` artifact**, not a cross-repo reusable workflow.
- **Enterprise reuse guidance** ([GitHub Well-Architected — scaling Actions reusability](https://wellarchitected.github.com/library/collaboration/recommendations/scaling-actions-reusability/)): provide `.github` directory templates for onboarding; keep templates focused per purpose. Supports **checks+auto-fix only** in downstream template vs full packaging in kit-internal CI.
- **Implication**: a separate downstream filename only helps if the installer still materializes **`.github/workflows/ci.yml`** (GitHub's conventional entrypoint). Renaming without installer mapping adds complexity with no benefit over in-place job subtraction.

#### Q1 — Template CI YAML shape

| Option | Summary | Verdict |
|--------|---------|---------|
| **A — In-place job subtraction** | Edit `template/.github/workflows/ci.yml` to retain `checks` + `auto-fix`; delete `npm-test`/`brew-test`/`choco-test` blocks. Manifest `[install_include_paths] .github/workflows` and `[clean_paths] .github/workflows/ci.yml` unchanged. | **Recommended** |
| B — Separate `ci-downstream.yml` | Second file in template; would still need installer/manifest policy to copy or symlink as `ci.yml`, or downstream repos would not auto-run the workflow. | Rejected — extra manifest/installer surface, same outcome |
| C — Reusable workflow `uses:` kit repo | Centralized workflow in its-magic repo; downstream calls `uses: org/its-magic/.github/workflows/ci.yml@ref`. | Rejected — breaks offline install, pins consumers to kit repo network + versioning |

**Resolution**: **Option A**. Keep filename `ci.yml` on both surfaces; intentional **byte mismatch** after fix (US-0017 exception). `deploy.yml` unchanged.

#### Q2 — Drift guard mechanism and harness wiring

| Option | Summary | Verdict |
|--------|---------|---------|
| A — Dedicated script only | New `scripts/check_downstream_ci_guard.py` (+ `template/` parity). | Partial |
| B — Contract test only | Extend `tests/auto_command_contract_test.py` with forbidden-pattern subtests. | Partial |
| **C — Script + contract markers + harness** | Script owns forbidden-pattern scan (template) + positive inventory (active); contract test asserts stable markers; `tests/run-tests.ps1` / `.sh` new section **§28B**. | **Recommended** |

**Forbidden pattern list** (template `ci.yml` must **not** match; case-sensitive substring / job-id scan):

- Job ids: `npm-test`, `brew-test`, `choco-test`
- Paths/commands: `npm pack`, `its-magic-*.tgz`, `installer.sh`, `packaging/chocolatey`, `packaging/homebrew`, `choco pack`, `brew style`

**Active positive inventory** (kit `.github/workflows/ci.yml` must contain all five job ids: `checks`, `auto-fix`, `npm-test`, `brew-test`, `choco-test`).

**Reason codes** (architecture-locked): `DOWNSTREAM_CI_FORBIDDEN_PATTERN`, `DOWNSTREAM_CI_JOB_LEAK`, `KIT_CI_PACKAGING_JOBS_MISSING`.

**`check_intake_template_parity.py`**: do **not** add byte-parity `--scope=ci-downstream` — that would contradict the intentional mismatch. Guard script is the correct surface.

#### Q3 — Fresh-project `TEST_COMMAND` / US-0063 bootstrap vs green-by-default `checks`

**Repo fact**: `template/docs/engineering/runbook.md` header currently sets non-empty `TEST_COMMAND: powershell … run-tests.ps1` while § "Intentional empty commands" documents blank-until-bootstrap (**DEC-0056** / **US-0063**) — internal contradiction.

| Surface | `TEST_COMMAND` default | Rationale |
|---------|------------------------|-----------|
| `template/docs/engineering/runbook.md` | **Empty** on ship (`TEST_COMMAND:` with no value) | Day-zero `checks` skips test/lint; job passes with explicit summary |
| Active `docs/engineering/runbook.md` | Keep powershell harness | Kit self-CI must stay green |
| `checks` workflow (both) | Update "No commands set" step → echo **`no tests configured yet`**; fail step only when `steps.test.outcome == 'failure'` or `steps.lint.outcome == 'failure'` (typecheck failures remain hard-fail when configured) | Discovery-locked semantics |

**US-0063 interaction**: installer stack-aware bootstrap writes `TEST_COMMAND` only when missing/unset in materialized runbook — preserved. Post-bootstrap downstream repos run real tests; pre-bootstrap repos stay green.

**US-0017 note**: `runbook.md` may diverge active vs template for the `TEST_COMMAND` header line only (second intentional exception candidate — architecture confirms in companion DEC).

#### Q4 — US-0017 negative-parity policy

**Recommended policy** (architecture publishes verbatim):

| Path | Parity rule |
|------|-------------|
| `template/.github/workflows/ci.yml` | Downstream-safe; **must not** byte-match active |
| `.github/workflows/ci.yml` (active) | Kit-internal; retains packaging jobs |
| `template/docs/engineering/runbook.md` | `TEST_COMMAND` empty on ship (likely ≠ active header) |
| `scripts/check_downstream_ci_guard.py` | Byte-identical active + `template/` per **US-0017** script parity |
| `check_intake_template_parity.py` | **No** new byte-parity scope for `ci.yml` |

**Contract tests**: `test_bug0009_template_ci_negative_parity` — assert `template/.github/workflows/ci.yml` ≠ `.github/workflows/ci.yml` after fix (SHA-256 differ).

#### Q5 — Install/upgrade smoke (post-copy `ci.yml` job inventory)

**Recommend**: extend `tests/installer_completeness_bug0003_test.py` (BUG-0003 / DEC-0066 class) with:

- `test_downstream_ci_yml_job_inventory_missing_mode` — `--mode missing --create` → parse installed `.github/workflows/ci.yml` job keys ⊆ `{checks, auto-fix}`; forbidden jobs absent.
- `test_downstream_ci_yml_job_inventory_upgrade_mode` — same after `--mode upgrade` overwrites framework `ci.yml`.

**Parser**: lightweight regex `^\s{2}(\w[\w-]*):` job-key scan (stdlib; no PyYAML dep) or shared helper in new `scripts/downstream_ci_guard_lib.py` if architecture prefers lib split.

**Manifest**: no change required (`install_include_paths` already lists `.github/workflows`).

#### Q6 — Release-note / docs upgrade remediation wording

**Recommended operator copy** (architecture places in README + release-notes template + runbook troubleshooting):

> **CI still runs its-magic packaging jobs?** Your project received a pre-fix workflow. Run **`its-magic --target <repo> --mode upgrade`** (or **`--mode clean`** then reinstall) to refresh `.github/workflows/ci.yml` from the corrected template. After upgrade, GitHub Actions should show only **`checks`** and **`auto-fix`** jobs — not `npm-test`, `brew-test`, or `choco-test`.

**Scope reminder**: fix applies to **new installs/upgrades**; stale repos heal on next upgrade (**US-0018**).

#### Research resolution matrix

| Q | status | Recommendation |
|---|--------|----------------|
| Q1 Template CI shape | **resolved** | In-place job subtraction in `template/.github/workflows/ci.yml` |
| Q2 Drift guard | **resolved** | `check_downstream_ci_guard.py` + §28B harness + contract subtests |
| Q3 Runbook bootstrap | **resolved** | Empty template `TEST_COMMAND`; US-0063 fills; checks summary text |
| Q4 US-0017 policy | **deferred_to_architecture** | Negative-parity table + companion DEC |
| Q5 Install smoke | **resolved** | Extend `installer_completeness_bug0003_test.py` |
| Q6 Release/docs | **resolved** | Upgrade remediation blurb (wording above) |

#### Risks (carried to architecture)

- **R1** (active CI strip): guard script **template-only** forbidden scan + **active** five-job positive assert — architecture must not merge the two paths.
- **R2** (stale repos): accepted; docs + release notes carry remediation (Q6).
- **R3** (wrong file copied): install-completeness job-inventory tests (Q5) + manifest path unchanged.
- **R4** (false green after bootstrap): once US-0063 sets `TEST_COMMAND`, real failures must still fail `checks` — no change to fail-step semantics.
- **R5** (template runbook contradiction): clearing header `TEST_COMMAND` may affect other validators expecting non-empty template runbook — sprint must re-run `validate_doc_profile.py` / push gates.

- **Research outcome**: **PASS** — Q1–Q3, Q5–Q6 **resolved**; Q4 **deferred_to_architecture** with explicit table; **no DEC authored** at research boundary.
- **Next**: **`/architecture`** (fresh tech-lead) — companion **DEC-xxxx** for US-0017 negative parity + guard contract; `# BUG-0009` architecture section.
- **Confidence**: high

### Delivery closure (R-0075 — BUG-0009, 2026-06-06, curator, auto-20260606-02)

> Append-only closure trailer for R-0075. BUG-0009 shipped with S0078 released on 2026-06-06T16:15:00Z; this refresh-context pass reconciles the research anchor to `status=delivered`. No new research questions opened; no new R-xxxx id allocated; no rewrite of DEC-0075 or architecture `# BUG-0009`. `fresh_context_marker=curator-S0078-BUG0009-refresh-context-20260606T162000Z-fresh`.

- **Anchor status**: `R-0075.status=delivered` (BUG-0009 **delivered** @ 2026-06-06T16:20:00Z curator refresh). Single-bug anchor; no shared-anchor split required.
- **BUG-0009 delivery coordinates**: sprint `S0078`; binding decision `DEC-0075` (composes on `US-0017` negative-parity exceptions + `US-0008` installer copy); architecture section `docs/engineering/architecture.md` `# BUG-0009`; release runtime proof `rp-auto-20260606-02-release-release-20260606T161500Z-S0078-BUG0009` / `proof_hash=ca36057ca8aff89ceee48d2474bf84c5533f777c9f9cd194a1c18ef8425484bc`; refresh-context runtime proof `rp-auto-20260606-02-refresh-context-curator-20260606T162000Z-S0078-BUG0009` / `proof_hash=e095e0efe855f7cfb10e9570c464641acbed1ceb04d4a0a588a256c467523705`; AC-1..AC-8 all `[x]` in `docs/product/backlog.md` `### BUG-0009`.
- **Resolution matrix outcome**: all discovery/research asks resolved at `/architecture` → `/sprint-plan` and verified through `/execute` → `/qa` → `/verify-work` → `/release`. In-place template job subtraction shipped; drift guard + harness **§28B** green; empty template `TEST_COMMAND` bootstrap; install smoke; operator upgrade remediation docs; template parity `--scope=downstream-ci-guard` PASS; US-0017 negative parity confirmed (template ≠ active `ci.yml`).
- **Risk resolution**: R1 (active CI strip) — mitigated by template-only forbidden scan + active five-job positive assert. R2 (stale repos) — mitigated by upgrade remediation blurb (Q6). R3 (wrong file copied) — mitigated by install-completeness job-inventory tests. R4 (false green after bootstrap) — mitigated by fail-step semantics unchanged post-bootstrap. R5 (runbook validator side-effects) — mitigated by `validate_doc_profile.py` PASS at execute/QA.
- **Evidence refs (BUG-0009 delivery)**: `sprints/S0078/release-findings.md` (PASS); `handoffs/releases/S0078-release-notes.md`; `sprints/S0078/uat.md` (8/8 PASS); `sprints/S0078/uat.json`; `sprints/S0078/qa-findings.md` (PASS cycle 1); `sprints/S0078/summary.md` (Release + Refresh-context blocks); `sprints/S0078/plan-verify.json` (PASS); `decisions/DEC-0075.md`; `docs/engineering/architecture.md` `# BUG-0009`; `docs/product/backlog.md` `### BUG-0009` (DONE + `release_closure_notes` + `refresh_context_notes`); `docs/product/acceptance.md` (BUG-0009 row `[x]`); `handoffs/release_queue.md` (`S0078=released`); `docs/engineering/state.md` (Release + Refresh-context checkpoints).
- **Bug queue closure signal**: with BUG-0009 closed, `docs/product/backlog.md` contains **zero** OPEN stories and **two** OPEN bugs (`BUG-0010`, `BUG-0011`). Bug-queue segment closes here; next `/auto` routes to `/discovery` for `BUG-0010` (`bug_queue_position=2/3`; `bug_queue_remaining=2`).
- **Open R-xxxx anchors status (post-closure)**: R-0075 **delivered** (this trailer). Next research anchor allocation deferred to the next `/discovery`-phase subagent when **BUG-0010** segment begins.

## R-0076 — BUG-0010: architecture triad archiver `## US-xxxx` backward compat + H1 forward enforcement

- **Anchor**: `bug_id=BUG-0010`; intake evidence `handoffs/intake_evidence/BUG-0010-intake-20260606.json`; related **US-0072**, **US-0061**, **DEC-0054**, **DEC-0043**.
- **Status**: `delivered` (delivery closure trailer below; curator refresh **2026-06-06T16:41:00Z**).

### Discovery extension (2026-06-06, PO, `auto-20260606-02`, `fresh_context_marker=po-BUG0010-discovery-20260606T141701Z-fresh`)

#### 1. Confirmed defect mechanics

- `scripts/enforce-triad-hot-surface.py` `STORY_HEADING` (line 48) matches only `^# US-\d{4}\s*[:\u2014\-].+$`.
- `split_arch_stories` → `rollover_architecture`: when `stories=[]` and `line_count(text) > ARCH_HOT_MAX_LINES`, raises `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS`.
- `cmd_self_test` architecture fixtures use only `# US-xxxx` headings — no `##`-only regression today.
- Kit repo `docs/engineering/architecture.md`: **3495** lines, **26** H1 `# US-`, **5** H2 `## US-` (mixed file). Operator downstream repo: **3021** lines, `##`-only story sections → zero archivable chunks.

#### 2. Discovery-locked fix boundary (operator both-fix)

| Track | Surface | Intent |
|-------|---------|--------|
| **A — Backward-compat rollover** | `STORY_HEADING`, `split_arch_stories`, `rollover_architecture`, `--self-test` | Treat `## US-xxxx` as story-section boundaries; oldest-first archive unchanged |
| **B — Forward enforcement** | `.cursor/commands/architecture.md`, `template/`, optional `scripts/*` validator, contract tests, runbook triad section | New `/architecture` writes must use H1 `# US-xxxx`; fail-closed when new section uses `## US-xxxx` |

**Out of scope**: mandatory bulk `##`→`#` normalization in kit repo (operator may remediate manually).

#### 3. Mixed-file precedence (discovery stub — research must lock)

- When both `# US-0067` and `## US-0067` exist, **H1 must win** (single archival unit; no double-count).
- Non-story `##` headings inside a `# US-` block must remain **intra-section** content (slice ends at next story boundary at either level).
- `BUG-xxxx` sections already use H1 `# BUG-xxxx` in kit repo — enforcement should preserve that pattern.

#### 4. Research questions (for `/research` tech-lead)

1. **Dual-level regex**: single combined pattern vs two-pass merge; delimiter parity (`:`, `—`, `-`) for `##`.
2. **Precedence table**: mixed H1+H2 same id; adjacent `##` without matching H1; preamble handling.
3. **Validator placement**: extend `enforce-triad-hot-surface.py` vs new `validate_architecture_headings.py` (+ template parity).
4. **Enforcement severity**: hard fail at `/architecture` completion vs dedicated reason code family (`ARCH_STORY_HEADING_LEVEL_INVALID` candidate).
5. **Regression matrix**: `##`-only fixture rollover; `# US-` non-regression; mixed kit-shaped fixture; idempotent second rollover; enforcement rejects new `## US-` append.
6. **Harness wiring**: `tests/run-tests.{sh,ps1}` section id; `check_intake_template_parity.py` scope if validator is new script.

#### 5. Risks

- **R1**: Double-counting `US-xxxx` at H1+H2 — mitigation: deterministic precedence (H1 wins).
- **R2**: Splitting inside a story block on inner `##` subheadings — mitigation: only `## US-\d{4}` matches story boundary, not generic `##`.
- **R3**: Enforcement blocks legitimate `##` subheadings under a `# US-` block — mitigation: validator scopes to **new top-level story headings** only.
- **R4**: Template/installer omits updated script — mitigation: installer-completeness / parity guard per **BUG-0003** class.

- **Discovery outcome**: **PASS** — no decision gate; **`/research`** (tech-lead) resolves Q1–Q6 before **`/architecture`**.
- **Confidence**: high (root cause confirmed; dual-track boundary locked; implementation details deferred)

### Research extension (2026-06-06, tech-lead, `auto-20260606-02`, `fresh_context_marker=tl-BUG0010-research-20260606T163000Z-fresh`)

#### External references (EARLY_RESEARCH=1)

- **ATX heading hierarchy** ([MarkdownPic — ATX vs Setext](https://markdownpic.com/syntax/markdown-headings-atx-vs-setext/)): ATX `#` headings are the safest default for tooling; **one H1 per document** is the conventional page title; major sections use H2+. Supports enforcing `# US-xxxx` as the canonical story-section boundary for new `/architecture` writes while treating legacy `## US-xxxx` as archival-only backward compat.
- **Structural heading guidance** ([W3C WAI — headings tutorial](https://www.w3.org/WAI/tutorials/page-structure/headings/)): headings with equal or higher rank start new sections; lower rank starts subsections. Implies generic `## Foo` inside a `# US-xxxx` block is **intra-section** content — archiver must not treat it as a story boundary.
- **Lint precedent** (markdownlint **MD025** / **MD001**): single-H1 and no-skipped-levels rules are common in doc pipelines. its-magic adopts a **narrower** subset: only `^## US-\d{4}` story-heading lines are forbidden on **new** `/architecture` writes (not global MD025 on the whole file).
- **Implication**: dual-track fix aligns with markdown best practice (H1 story sections) without breaking repos that historically used H2 — rollover reads both levels; forward path converges on H1.

#### Q1 — Dual-level regex shape and merge algorithm

| Option | Summary | Verdict |
|--------|---------|---------|
| A — Single alternation regex | `^(#{1,2}) (US\|BUG)-\d{4}\s*[:\u2014\-].+$` in one pass | Partial — loses per-id precedence |
| **B — Two-pattern scan + precedence filter** | `STORY_HEADING_H1` + `STORY_HEADING_H2` share delimiter contract; collect `(line_idx, story_id, level)`; drop H2 rows whose `story_id` has any H1 in file; sort by `line_idx`; slice | **Recommended** |
| C — Two-pass merge (H1 blocks first, then absorb orphan H2) | Complex; risks wrong ordering in mixed files | Rejected |

**Resolution**: **Option B**. Replace monolithic `STORY_HEADING` with:

```text
STORY_HEADING_H1 = ^# (?:US|BUG)-\d{4}\s*[:\u2014\-].+$
STORY_HEADING_H2 = ^## US-\d{4}\s*[:\u2014\-].+$
```

(`BUG-xxxx` only at H1 today — kit inventory confirms; H2 BUG pattern not required in v1.)

**`split_arch_stories` merge algorithm** (architecture publishes verbatim):

1. Scan all lines; collect boundary candidates `(idx, story_id, level)` where H1 matches `STORY_HEADING_H1` or H2 matches `STORY_HEADING_H2`.
2. Build `h1_ids = {story_id for candidates with level==1}`.
3. `boundaries = sorted([c for c in candidates if not (c.level==2 and c.story_id in h1_ids)], key=lambda c: c.idx)`.
4. Split preamble + contiguous blocks between boundary indices (unchanged rollover loop in `rollover_architecture`).

**Delimiter parity**: H2 uses identical `:`, `—` (U+2014), `-` separator class as H1 (discovery-locked).

#### Q2 — Mixed-file precedence table

| Scenario | Precedence | Archival unit |
|----------|------------|---------------|
| `# US-0067` only | H1 boundary | `# US-0067` block → next story boundary |
| `## US-0067` only (no H1 for 0067) | H2 boundary | `## US-0067` block → next story boundary |
| Both `# US-0067` and `## US-0067` | **H1 wins** — H2 ignored as boundary | Single unit starting at `# US-0067`; `## US-0067` content stays inside H1 slice |
| Adjacent `## US-0068` then `## US-0069` (no H1) | Each H2 is boundary | Two units, oldest-first rollover |
| `### US-0099` or `## Architecture:` | **Not** a story boundary | Intra-section content |
| `# BUG-0009` | H1 boundary (extend H1 family) | Same as `# US-xxxx` |
| Preamble before first boundary | Retained in hot file | Never archived alone |

**Kit-repo fixture shape** (research regression anchor): 26× `# US-` + 5× `## US-` (`US-0067`..`0070`, `US-0083` gate) — mixed rollover must not double-count.

#### Q3 — Validator placement and reason-code family

| Option | Summary | Verdict |
|--------|---------|---------|
| A — New `scripts/validate_architecture_headings.py` | Separate CLI + template parity + installer manifest | Rejected — duplicates regex; BUG-0003 install surface |
| B — Contract test only | No runtime enforcement | Rejected — fails operator "both" enforcement track |
| **C — Extend `enforce-triad-hot-surface.py` in place** | Add `count_h2_story_headings(text)` + `--check-arch-heading-policy [--baseline PATH]`; reuse `STORY_HEADING_H2`; template byte-parity via existing `US-0017` script mirror | **Recommended** |

**Forward-enforcement API sketch** (stdlib-only, same file):

- `count_h2_story_headings(text: str) -> int` — count lines matching `STORY_HEADING_H2`.
- `check_arch_heading_policy(repo, baseline_h2_count: int) -> Optional[str]` — if current count **>** baseline → return `ARCH_STORY_HEADING_LEVEL_INVALID` (new `## US-xxxx` story section added).
- `/architecture` step 9 (triad gate): capture `baseline_h2_count` **before** mutating `architecture.md`; after append + rollover, run heading policy check.

**Reason codes** (architecture-locked family):

| Code | When |
|------|------|
| `ARCH_STORY_HEADING_LEVEL_INVALID` | H2 `## US-xxxx` story-heading count increased during `/architecture` |
| `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS` | (unchanged) oversize file, zero boundaries after dual-level scan |
| `ARTIFACT_HOT_SURFACE_OVERSIZE` | (unchanged) single block exceeds cap post-rollover |

**`check_intake_template_parity.py`**: **no** new scope — `enforce-triad-hot-surface.py` already mirrored; extend script in active + `template/` atomically per **US-0017**.

#### Q4 — Block vs warn at `/architecture` completion

| Option | Summary | Verdict |
|--------|---------|---------|
| A — Warn only | Log legacy `## US-` count; allow phase success | Rejected — operator chose enforcement track |
| B — Static fail on any `## US-` in file | Blocks kit repo with 5 legacy H2 sections | Rejected — false positive on grandfathered content |
| **C — Diff-gated hard fail** | Fail only when `count_h2_story_headings(after) > count_h2_story_headings(before)` | **Recommended** |

**Resolution**: **Option C** — **hard fail (block)** at `/architecture` completion when the phase **introduces** a new `## US-xxxx` story heading. Grandfathered H2 sections remain rollover-visible but must not grow. Normalizing `##`→`#` (count decrease) is allowed.

**Command contract**: `.cursor/commands/architecture.md` (+ `template/`) step — mandate `# US-xxxx` / `# BUG-xxxx` for appended sections; reference `ARCH_STORY_HEADING_LEVEL_INVALID` stop token.

#### Q5 — Self-test + harness regression matrix

| Fixture class | Assert |
|---------------|--------|
| `##`-only rollover | 4× `## US-100x` over `ARCH_HOT_MAX_LINES=12` → rollover moves ≥1; post `--check` exit 0 |
| `# US-` non-regression | Existing self-test `# US-0001`/`# US-0002` fixture unchanged behavior |
| Mixed H1+H2 same id | `# US-0067` + `## US-0067` → single boundary at H1; one archival unit |
| Idempotent second rollover | Second `--rollover` → `None` when within caps |
| Enforcement delta | `count_h2` increases → `ARCH_STORY_HEADING_LEVEL_INVALID` |
| Inner `##` subheading | `# US-0001` block containing `## Details` → no extra boundary |

**Harness wiring**:

| Surface | Recommendation |
|---------|----------------|
| `enforce-triad-hot-surface.py --self-test` | Extend `cmd_self_test` with classes above (mandatory) |
| `tests/auto_command_contract_test.py` | Add `test_bug0010_*` prefix subtests (architecture command H1 mandate text; linkage to `# BUG-0010`) |
| `tests/run-tests.ps1` / `.sh` | New section **§29A** (candidate) for `test_bug0010_*`; existing triad self-test block unchanged |
| `tests/fixtures/triad_arch_headings/` | Optional minimal `##`-only + mixed markdown fixtures (architecture locks) |

#### Q6 — `BUG-xxxx` H1 parity + installer/template scope

- **Rollover**: extend H1 pattern to `# BUG-\d{4}` (7 existing kit sections) — same archival semantics as `# US-xxxx`.
- **Forward enforcement**: `/architecture` for **stories** appends `# US-xxxx`; bug fixes append `# BUG-xxxx` (already H1 in practice). H2 enforcement targets **`## US-` only** — no `## BUG-` pattern in v1.
- **Template parity**: single touchpoint — `scripts/enforce-triad-hot-surface.py` ↔ `template/scripts/enforce-triad-hot-surface.py` (byte-identical post-fix).
- **Installer manifest**: path already listed — no manifest change expected.
- **Runbook**: extend triad subsection with (a) legacy `## US-` rollover note, (b) one-time `##`→`#` operator remediation, (c) `ARCH_STORY_HEADING_LEVEL_INVALID` diagnostic.

#### Research resolution matrix

| Q | status | Recommendation |
|---|--------|----------------|
| Q1 Dual-level regex | **resolved** | Two-pattern scan + H1-wins precedence filter |
| Q2 Precedence table | **resolved** | Table above; kit mixed fixture is regression anchor |
| Q3 Validator placement | **resolved** | In-place `enforce-triad-hot-surface.py`; diff-gated API |
| Q4 Enforcement severity | **resolved** | Hard fail on H2 story-heading count increase |
| Q5 Regression matrix | **resolved** | Extended `--self-test` + `test_bug0010_*` + harness **§29A** |
| Q6 BUG parity / template | **resolved** | H1 `# BUG-` in rollover; US-0017 script mirror only |

#### Risks (carried to architecture)

- **R1** (double-count H1+H2): mitigated by H1-wins filter (Q2).
- **R2** (split on inner `##`): mitigated by strict `## US-\d{4}` boundary regex only (Q2).
- **R3** (enforcement blocks legitimate subheadings): mitigated by diff-gated policy — generic `##` inside blocks allowed (Q4).
- **R4** (template script drift): mitigated by byte-identical active + `template/` commit + existing installer-completeness path (Q6).
- **R5** (DEC-0054 §2 text says `# US-xxxx` only): architecture companion **DEC-xxxx** amends semantics doc-only — rollover + enforcement table; no threshold key changes.

- **Research outcome**: **PASS** — Q1–Q6 **resolved**; **no DEC authored** at research boundary.
- **Next**: **`/architecture`** (fresh tech-lead) — companion **DEC-xxxx** composing on **DEC-0054** + **DEC-0043**; `# BUG-0010` architecture section; lock harness **§29A** id.
- **Confidence**: high

### Delivery closure (R-0076 — BUG-0010, 2026-06-06, curator, auto-20260606-02)

> Append-only closure trailer for R-0076. BUG-0010 shipped with S0079 released on 2026-06-06T16:36:00Z; this refresh-context pass reconciles the research anchor to `status=delivered`. No new research questions opened; no new R-xxxx id allocated; no rewrite of DEC-0076 or architecture `# BUG-0010`. `fresh_context_marker=curator-S0079-BUG0010-refresh-context-20260606T164100Z-fresh`.

- **Anchor status**: `R-0076.status=delivered` (BUG-0010 **delivered** @ 2026-06-06T16:41:00Z curator refresh). Single-bug anchor; no shared-anchor split required.
- **BUG-0010 delivery coordinates**: sprint `S0079`; binding decision `DEC-0076` (composes on `DEC-0054` + `DEC-0043`); architecture section `docs/engineering/architecture.md` `# BUG-0010`; release runtime proof `rp-auto-20260606-02-release-release-20260606T163600Z-S0079-BUG0010` / `proof_hash=185901a6d7b195ae6ab54f9221953ba4311a955d70d62b76c69ca1c351ac4b14`; refresh-context runtime proof `rp-auto-20260606-02-refresh-context-curator-20260606T164100Z-S0079-BUG0010` / `proof_hash=2b42915c5f8c0ae364f6f232ef1dc8e1e647fc1932593415d264ffcc8b177ef3`; AC-1..AC-8 all `[x]` in `docs/product/backlog.md` `### BUG-0010`.
- **Resolution matrix outcome**: all discovery/research asks resolved at `/architecture` → `/sprint-plan` and verified through `/execute` → `/qa` → `/verify-work` → `/release`. Dual-level archiver (H1-wins) + diff-gated `ARCH_STORY_HEADING_LEVEL_INVALID` shipped; extended `--self-test` + `test_bug0010_*` + harness **§29A** green; command + runbook template parity PASS.
- **Risk resolution**: R1 (double-count H1+H2) — mitigated by H1-wins filter (Q2). R2 (split on inner `##`) — mitigated by strict `## US-\d{4}` boundary regex only (Q2). R3 (enforcement blocks legitimate subheadings) — mitigated by diff-gated policy (Q4). R4 (template script drift) — mitigated by byte-identical active + `template/` commit (Q6). R5 (DEC-0054 §2 text drift) — mitigated by doc-only amendment in DEC-0076 §8.
- **Evidence refs (BUG-0010 delivery)**: `sprints/S0079/release-findings.md` (PASS); `handoffs/releases/S0079-release-notes.md`; `sprints/S0079/uat.md` (8/8 PASS); `sprints/S0079/uat.json`; `sprints/S0079/qa-findings.md` (PASS); `sprints/S0079/summary.md` (Release + Refresh-context blocks); `sprints/S0079/plan-verify.json` (PASS); `decisions/DEC-0076.md`; `docs/engineering/architecture.md` `# BUG-0010`; `docs/product/backlog.md` `### BUG-0010` (DONE + `release_closure_notes` + `refresh_context_notes`); `docs/product/acceptance.md` (BUG-0010 row `[x]`); `handoffs/release_queue.md` (`S0079=released`); `docs/engineering/state.md` (Release + Refresh-context checkpoints).
- **Bug queue closure signal**: with BUG-0010 closed, `docs/product/backlog.md` contains **zero** OPEN stories and **one** OPEN bug (`BUG-0011`). Bug-queue segment closes here; next `/auto` routes to `/discovery` for `BUG-0011` (`bug_queue_position=3/3`; `bug_queue_remaining=1`).
- **Open R-xxxx anchors status (post-closure)**: R-0076 **delivered** (this trailer). Next research anchor allocation deferred to the next `/discovery`-phase subagent when **BUG-0011** segment begins.

## R-0077 — BUG-0011: Caveman voice compression rules missing from caveman.mdc (US-0089 incomplete delivery)

- **Anchor**: `bug_id=BUG-0011`; intake evidence `handoffs/intake_evidence/BUG-0011-intake-20260606.json`; related **US-0089**, **US-0090**, **DEC-0072**, **R-0073**.
- **Status**: `delivered` (discovery + research extensions below; Q1–Q7 resolved; delivery closed at curator **`/refresh-context`** **`2026-06-06T14:56:31Z`**).

### Discovery extension (2026-06-06, PO, `auto-20260606-02`, `fresh_context_marker=po-BUG0011-discovery-20260606T163655Z-fresh`)

#### 1. Confirmed defect mechanics

- `.cursor/rules/caveman.mdc` (141 lines active + `template/` mirror) ships **DEC-0072** scaffolding: scratchpad gate, 9-zone literal invariant, non-suppressible gate vocabulary, operator toggle phrases, TOKEN_PROFILE non-substitution, default-off invariant, US-0090 reserved-key no-ops.
- **Missing**: actionable voice-compression directives — no drop-filler/hedging rules, no lite/full/ultra intensity table, no auto-clarity exceptions, no persistence ("active every response"), no user-rule precedence clause.
- **DEC-0072** §6 explicitly marks voice quality under `CAVEMAN_MODE=1` as operator-verified only (not CI-testable) — which allowed US-0089 to ship without voice text.
- Operator repro: `CAVEMAN_MODE=1` + `CAVEMAN_LEVEL=full` in scratchpad → replies remain verbose (full sentences, filler, hedging).
- **US-0090 orthogonality preserved**: input-side `CAVEMAN_COMPRESS_INPUT` / `scripts/caveman_compress_input.py` are separate vertical; this bug fixes **response-side voice only**.

#### 2. Upstream reference inventory (JuliusBrussee/caveman `skills/caveman/SKILL.md`, MIT, not vendored)

| Upstream section | Portable to its-magic? | Notes |
|------------------|------------------------|-------|
| **Rules** (drop articles/filler/hedging/pleasantries; fragments OK; short synonyms; technical terms exact) | **Yes** | Align with **R-0073** intent |
| **Intensity** (lite/full/ultra table + examples) | **Yes** (lite/full/ultra only) | Wenyan rows **out of scope** |
| **Auto-Clarity** (security, destructive, ambiguous compression) | **Yes** | Resume caveman after clear part |
| **Persistence** (active every response; off only via toggles) | **Yes** | Complements scratchpad gate |
| **Boundaries** (code/commits normal; level persist) | **Partial** | its-magic adds 9-zone literal MUST on top |
| **Wenyan modes** | **No** | Per intake + **R-0073** |
| **~75% token savings claim** | **No** | No vendor benchmarks in normative docs |
| **`npx skills add` install** | **No** | DEC-0072 §2 rejects |

#### 3. Discovery-locked fix boundary (rule-only per DEC-0072 Option A)

| # | Surface | Change |
|---|---------|--------|
| 1 | `.cursor/rules/caveman.mdc` + `template/.cursor/rules/caveman.mdc` | Append **`## Voice compression (when CAVEMAN_MODE=1)`** with lite/full/ultra table, drop rules, auto-clarity, persistence, user-rule precedence; **preserve** existing 9-zone literal invariant verbatim |
| 2 | `docs/engineering/runbook.md` + `template/` | Extend **`### Caveman mode (US-0089)`** with level table + operator examples |
| 3 | `tests/auto_command_contract_test.py` | Additive **`test_caveman_voice_*`** token-presence subtests; update US-0090 SHA-256 baseline after rule edit |
| 4 | `docs/engineering/architecture.md` | New **`# BUG-0011`** section (research confirms vs amend `# US-0089`) |

**Negative scope (non-negotiable)**:

- Do **not** weaken DEC-0072 §4 nine-zone literal invariant.
- Do **not** change `CAVEMAN_COMPRESS_INPUT` semantics, deny-list, or `scripts/caveman_compress_input.py`.
- Do **not** add Wenyan, vendor benchmarks, new skill, or `npx` install path.
- Do **not** modify existing **`test_caveman_default_off_*`** subtests (DEC-0072 §6 row 6).

#### 4. US-0090 SHA-256 pin interaction (discovery stub — research must lock)

- `test_caveman_compress_input_rule_byte_identity` pins SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` (US-0090 R10 negative parity).
- Rule edit for voice section **will change** this hash — expected, not a regression.
- **Option A (recommended stub)**: bump `_CAVEMAN_RULE_BASELINE_SHA256` to post-voice SHA after delivery; keep active==template equality assertion.
- **Option B**: replace SHA pin with substring-presence markers only + active==template parity (loses immutability guard for unrelated edits).

#### 5. Research questions (for `/research` tech-lead)

1. **SHA strategy**: Option A vs B above; whether to add separate `test_caveman_voice_rule_markers_*` instead of single SHA pin.
2. **Level table wording**: upstream-adapted verbatim vs kit-native examples (React re-render from upstream vs its-magic workflow example).
3. **User-rule precedence**: exact paragraph placement in always-on rule; interaction with `.cursor/rules/quality.mdc` or user rules.
4. **Contract marker token list**: minimum viable strings for `test_caveman_voice_*` (e.g. `Voice compression`, `lite`, `full`, `ultra`, `Auto-Clarity`, `drop filler`).
5. **Runbook examples**: include upstream-style before/after table or link to rule file only.
6. **Architecture surface**: dedicated `# BUG-0011` vs amend `# US-0089` §6 non-goal removal.
7. **Ultra vs 9-zone overlap**: confirm ultra prose abbreviations cannot touch reason codes, IDs, paths (reinforce in voice section).

#### 6. Risks

- **R1**: US-0090 SHA pin breaks on rule edit — **expected**; mitigation: intentional baseline bump at execute (Q1).
- **R2**: Voice rules garble literal regions — mitigation: existing 9-zone MUST + voice section must restate non-garbling (Q7).
- **R3**: Conflicting user rules ("complete sentences") override voice — mitigation: explicit precedence paragraph (Q3).
- **R4**: `ultra` abbreviates reason codes or IDs — **forbidden** by existing invariant; voice section must not contradict.

- **Discovery outcome**: **PASS** — no decision gate; **`/research`** (tech-lead) resolves Q1–Q7 before **`/architecture`**.
- **Confidence**: high (root cause confirmed; upstream diff catalogued; fix boundary locked; US-0090 orthogonality explicit)

### Research extension (2026-06-06, tech-lead, `auto-20260606-02`, `fresh_context_marker=tl-BUG0011-research-20260606T143942Z-fresh`)

#### External references (EARLY_RESEARCH=1)

- **Cursor rule precedence** ([Cursor Docs — Rules](https://cursor.com/docs/rules)): applicable rules merge into model context; on conflict, precedence is **Team Rules → Project Rules → User Rules**. `caveman.mdc` is a project rule (`globs: ["**/*"]`, always-on). Native precedence already favors project rules over user settings, but merged context can still carry contradictory style guidance — an **explicit in-rule precedence paragraph** is required so voice compression wins deterministically when `CAVEMAN_MODE=1` (Q3).
- **Upstream voice contract** (JuliusBrussee/caveman `skills/caveman/SKILL.md`, MIT, fetched 2026-06-06): portable sections are **Persistence**, **Rules** (drop filler/hedging/pleasantries; fragments OK; technical terms exact), **Intensity** (`lite|full|ultra` rows only), **Auto-Clarity** (security/destructive/ambiguous compression pauses), **Boundaries** (code/commits normal). Wenyan rows, ~75% token claim, and `npx` install remain **out of scope** per **R-0073** / intake.
- **Implication**: delivery is a **rule-body append** only — no skill, no script, no scratchpad key changes. Preserves **DEC-0072** §2 rule-only composition and **US-0090** orthogonality.

#### Q1 — SHA-256 bump vs substring-only assertion strategy

| Option | Summary | Verdict |
|--------|---------|---------|
| **A — Dual layer: marker subtests + baseline SHA bump** | Keep `test_caveman_compress_input_rule_byte_identity` (US-0090 R10 pin) but **intentionally bump** `_CAVEMAN_RULE_BASELINE_SHA256` at `/execute` to post-voice digest; add additive `test_caveman_voice_*` token-presence subtests for the new section; retain `test_caveman_template_parity_sweep` locked-string parity for `caveman.mdc`. | **Recommended** |
| B — Markers only, drop SHA pin | Remove byte-identity guard; rely on substring markers + active==template manual review. | Rejected — loses immutability guard for unrelated future edits to pre-voice scaffolding |
| C — SHA only, no voice markers | Bump baseline without section markers. | Rejected — cannot detect accidental voice-section deletion without re-reading full file in review |

**Resolution**: **Option A**. At execute:

1. Append voice section to active + `template/.cursor/rules/caveman.mdc` (byte-identical pair).
2. Recompute SHA-256 of active rule file; update `_CAVEMAN_RULE_BASELINE_SHA256` constant in `test_caveman_compress_input_rule_byte_identity`.
3. Add `test_caveman_voice_*` subtests (Q4 list) — **additions only**; **do not modify** any `test_caveman_default_off_*` or `test_caveman_compress_input_*` assertion bodies except the single baseline constant in #2.
4. Document intentional SHA change in sprint UAT + release notes (not a regression).

Pre-voice baseline (recorded): `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`.

#### Q2 — Level table wording (upstream-adapted vs kit-native)

| Option | Summary | Verdict |
|--------|---------|---------|
| A — Upstream examples verbatim (React re-render row) | Copy upstream intensity table examples as-is. | Rejected — examples reference generic React; less aligned with kit operator repro |
| **B — Kit-native examples, upstream table shape** | Keep upstream **table column semantics** (`lite` = no filler but grammatical; `full` = drop articles + fragments; `ultra` = abbreviate prose words only) but use **its-magic-native before/after pairs**: (1) orchestration gate explanation, (2) auth-middleware bug from intake repro. Include upstream **pattern** line: `` `[thing] [action] [reason]. [next step].` `` | **Recommended** |
| C — Prose-only levels (no table) | Describe levels in bullets without markdown table. | Rejected — harder to test; upstream parity weaker |

**Resolution**: **Option B**. Rule section includes a markdown intensity table with **lite / full / ultra** rows (no Wenyan). Examples demonstrate **token-saving terse/imperative prose**, explicitly **not** stereotypical caveman roleplay. Runbook carries a shortened 2-row before/after table (Q5); rule file owns normative table.

#### Q3 — User-rule precedence paragraph placement

| Option | Summary | Verdict |
|--------|---------|---------|
| A — Amend `quality.mdc` | Global style rule references Caveman override. | Rejected — spreads voice logic outside DEC-0072 rule-only surface |
| B — Amend user-facing README only | Document precedence for operators, not agents. | Rejected — does not bind model behavior |
| **C — Self-contained subsection in `caveman.mdc`** | Under new `## Voice compression (when CAVEMAN_MODE=1)`, add `### Precedence` stating: when `CAVEMAN_MODE=1`, voice-compression directives in **this rule** override conflicting **user-rule** prose-style guidance (e.g. "write complete sentences", "blog-post quality") for **assistant reply voice only**; does **not** override user rules for tool usage, git safety, security, or commit policy. | **Recommended** |

**Resolution**: **Option C**. Place `### Precedence` immediately after the section intro (before intensity table). Contract-test marker: substring `user rule` or `user-rule` + `CAVEMAN_MODE=1` + `complete sentences` (or equivalent kit-native phrasing architecture locks verbatim). Cursor native **Project Rules > User Rules** precedence cited in architecture footnote only — normative agent text lives in `caveman.mdc`.

#### Q4 — Contract test marker token list (`test_caveman_voice_*`)

**Recommended additive subtests** (prefix `test_caveman_voice_`; active + template mirror for each `assertIn`):

| Subtest | Minimum tokens / anchors |
|---------|--------------------------|
| `test_caveman_voice_section_heading_present` | Exact heading `## Voice compression (when CAVEMAN_MODE=1)` |
| `test_caveman_voice_level_table_markers` | `lite`, `full`, `ultra` (all three in rule body) |
| `test_caveman_voice_drop_filler_directive` | `drop` + (`filler` or `hedging` or `pleasantries`) |
| `test_caveman_voice_fragment_permission` | `fragments` + `OK` (case as authored) |
| `test_caveman_voice_auto_clarity_exceptions` | `Auto-Clarity` or `auto-clarity` + (`security` or `destructive` or `ambiguous`) |
| `test_caveman_voice_persistence_directive` | `every response` or `ACTIVE EVERY RESPONSE` (kit-native casing) |
| `test_caveman_voice_user_rule_precedence` | `user rule` + `CAVEMAN_MODE=1` |
| `test_caveman_voice_ultra_prose_only_boundary` | `ultra` + (`reason code` or `reason codes`) + `never abbreviate` or equivalent deferral to 9-zone |
| `test_caveman_voice_template_parity` | `hashlib` not required — assert active `caveman.mdc` == template `caveman.mdc` **byte-identical** after voice delivery |

**Harness wiring**: new `tests/run-tests.ps1` / `.sh` section **§30A** — `Voice compression rule markers (BUG-0011)` — runs only `test_caveman_voice_*` prefix (candidate; architecture locks section id).

**Invariants preserved**:

- All `test_caveman_default_off_*` bodies **unchanged** (**DEC-0072** §6).
- All `test_caveman_compress_input_*` bodies **unchanged** except `_CAVEMAN_RULE_BASELINE_SHA256` constant (**US-0090** R10 bump).
- `test_caveman_default_off_reference_non_substitution_paragraph` pinned sentence **byte-unchanged**.

#### Q5 — Runbook example selection and depth

| Option | Summary | Verdict |
|--------|---------|---------|
| A — Link to rule only | Runbook mentions voice levels exist; no examples. | Rejected — operator discoverability gap persists |
| **B — Compact before/after table + rule pointer** | Under `### Caveman mode (US-0089)`, add `#### Voice compression levels` with 2-row table: (1) technical explain at `full`, (2) destructive warning at auto-clarity break. Point to `.cursor/rules/caveman.mdc` for full contract. | **Recommended** |
| C — Duplicate full upstream table in runbook | Full intensity table + 6 examples in runbook. | Rejected — doc drift risk; violates minimal-doc principle |

**Resolution**: **Option B**. Do **not** modify `### Caveman input compression (US-0090)` subsection. Template mirror per **US-0017**.

#### Q6 — Architecture surface (`# BUG-0011` vs amend `# US-0089`)

| Option | Summary | Verdict |
|--------|---------|---------|
| A — Amend `# US-0089` only | Extend US-0089 section; no bug section. | Rejected — breaks BUG-0009/BUG-0010 bug-section traceability pattern |
| **B — Dedicated `# BUG-0011` + cross-link from `# US-0089`** | New `docs/engineering/architecture.md` `# BUG-0011` owns voice-section delivery, AC map, atomic task seeds, SHA bump policy, harness §30A. Add one forward-link from `# US-0089` §6 replacing "Not tested: voice quality" with "voice rules delivered in **BUG-0011**; qualitative brevity remains operator-verified (not CI)". | **Recommended** |
| C — Companion DEC only | DEC-0077 without architecture section. | Rejected — insufficient execute surface |

**Resolution**: **Option B**; companion **DEC-xxxx** at architecture (likely **DEC-0077** if next id free) composing on **DEC-0072** without rewrite.

#### Q7 — Ultra-level abbreviation vs 9-zone literal overlap

**Analysis**: Upstream `ultra` abbreviates **ordinary prose words** (DB/auth/config/req/res) but forbids abbreviating code symbols, function names, API names, error strings. Local **DEC-0072** §4 nine-zone list is **strict superset** — reason codes, IDs, paths, proof tuples, gate tokens are already byte-literal MUST.

| Risk | Mitigation (voice section text) |
|------|----------------------------------|
| Ultra abbreviates `PHASE_CONTEXT_ISOLATION_VIOLATION` | Voice section MUST state: **reason codes** remain byte-literal — defer to `## Literal-region invariant (9-zone hard MUST)`; repeat forbidden garbling examples |
| Ultra drops `US-` prefix from IDs | Same — cite zone 5 + forbidden example already in rule |
| Ultra collapses fenced code | Zone 1 MUST unchanged; voice section: "code blocks unchanged" (upstream Rules line) |
| Ultra abbreviates `decision_gate` token | US-0088 non-suppressible list already byte-literal; voice section cross-refs `## Non-suppressible gate vocabulary` |

**Resolution**: Voice section **must not** weaken or paraphrase the existing 9-zone block. Add one `### Ultra and literal regions` stub under voice compression that **defers** to the existing invariant (no duplicate zone list — pointer only). Contract test `test_caveman_voice_ultra_prose_only_boundary` (Q4) locks the deferral sentence.

#### Research resolution matrix

| Q | status | Recommendation |
|---|--------|----------------|
| Q1 SHA strategy | **resolved** | Dual layer: bump `_CAVEMAN_RULE_BASELINE_SHA256` + additive `test_caveman_voice_*` |
| Q2 Level table wording | **resolved** | Kit-native examples; upstream table semantics; no Wenyan |
| Q3 User-rule precedence | **resolved** | `### Precedence` subsection in `caveman.mdc` only |
| Q4 Contract markers | **resolved** | Nine `test_caveman_voice_*` subtests + harness **§30A** candidate |
| Q5 Runbook examples | **resolved** | Compact 2-row table under Caveman mode; US-0090 subsection untouched |
| Q6 Architecture surface | **resolved** | Dedicated `# BUG-0011` + `# US-0089` §6 cross-link amendment |
| Q7 Ultra vs 9-zone | **resolved** | Deferral stub; no duplicate zone list; marker subtest |

#### Risks (carried to architecture)

- **R1** (US-0090 SHA pin break): **expected** at execute; bump baseline + release-note callout (Q1).
- **R2** (literal garbling): mitigated by unchanged 9-zone MUST + ultra deferral stub (Q7).
- **R3** (user-rule conflict): mitigated by `### Precedence` paragraph + Cursor project-rule precedence (Q3).
- **R4** (ultra abbreviates reason codes): **forbidden** by existing invariant; voice section must defer not contradict (Q7).
- **R5** (doc drift runbook vs rule): runbook carries summary table only; rule owns normative text (Q5).
- **R6** (accidental edit to DEC-0072 pinned tests): execute must not touch `test_caveman_default_off_*` bodies or non-substitution sentence (Q4 invariants).

- **Research outcome**: **PASS** — Q1–Q7 **resolved**; **no DEC authored** at research boundary.
- **Next**: **`/architecture`** (fresh tech-lead) — companion **DEC-xxxx** composing on **DEC-0072**; `# BUG-0011` architecture section; voice-section verbatim outline for execute.
- **Confidence**: high

### Delivery closure (R-0077 — BUG-0011, 2026-06-06, curator, auto-20260606-02)

> Append-only closure trailer for R-0077. BUG-0011 shipped with S0080 released on 2026-06-06T17:00:00Z; this refresh-context pass reconciles the research anchor to `status=delivered`. No new research questions opened; no new R-xxxx id allocated; no rewrite of DEC-0077 or architecture `# BUG-0011`. `fresh_context_marker=curator-S0080-BUG0011-refresh-context-20260606T145631Z-fresh`.

- **Anchor status**: `R-0077.status=delivered` (BUG-0011 **delivered** @ 2026-06-06T14:56:31Z curator refresh). Single-bug anchor; no shared-anchor split required.
- **BUG-0011 delivery coordinates**: sprint `S0080`; binding decision `DEC-0077` (composes on `DEC-0072`); architecture section `docs/engineering/architecture.md` `# BUG-0011`; release runtime proof `rp-auto-20260606-02-release-release-20260606T170000Z-S0080-BUG0011` / `proof_hash=06b929b4b97c50dfb4012154443764c17e2958c409d4df9d0b16dda5b39825fc`; refresh-context runtime proof `rp-auto-20260606-02-refresh-context-curator-20260606T145631Z-S0080-BUG0011` / `proof_hash=95970384cfd1aa7986f234be6fc8b3f88558ea2a8e10b092a3947d9170fba911`; AC-1..AC-8 all `[x]` in `docs/product/backlog.md` `### BUG-0011`.
- **Resolution matrix outcome**: all discovery/research asks resolved at `/architecture` → `/sprint-plan` and verified through `/execute` → `/qa` → `/verify-work` → `/release`. Voice section + nine `test_caveman_voice_*` + harness **§30A** + intentional SHA bump `E10EFC32…E47DE` → `C7AAC699…8BC4D` shipped; UAT-1 operator voice spot-check **PASS**.
- **Risk resolution**: R1 (US-0090 SHA pin break) — mitigated by intentional baseline bump + release-note callout (Q1). R2 (literal garbling) — mitigated by unchanged 9-zone MUST + ultra deferral stub (Q7). R3 (user-rule conflict) — mitigated by `### Precedence` paragraph (Q3). R4 (ultra abbreviates reason codes) — mitigated by existing invariant deferral (Q7). R5 (doc drift runbook vs rule) — mitigated by compact runbook table only (Q5). R6 (accidental DEC-0072 test edit) — mitigated by pinned `test_caveman_default_off_*` bodies unchanged (Q4).
- **Evidence refs (BUG-0011 delivery)**: `sprints/S0080/release-findings.md` (PASS); `handoffs/releases/S0080-release-notes.md`; `sprints/S0080/uat.md` (8/8 PASS); `sprints/S0080/uat.json`; `sprints/S0080/qa-findings.md` (PASS); `sprints/S0080/summary.md` (Release + Refresh-context blocks); `sprints/S0080/plan-verify.json` (PASS); `decisions/DEC-0077.md`; `docs/engineering/architecture.md` `# BUG-0011`; `docs/product/backlog.md` `### BUG-0011` (DONE + `release_closure_notes` + `refresh_context_notes`); `docs/product/acceptance.md` (BUG-0011 row `[x]`); `handoffs/release_queue.md` (`S0080=released`); `docs/engineering/state.md` (Release + Refresh-context checkpoints).
- **Portfolio drain closure signal**: with BUG-0011 closed, `docs/product/backlog.md` contains **zero** OPEN stories and **zero** OPEN bugs. Bug-queue segment (`BUG-0009..BUG-0011`) and `auto-20260606-02` orchestrator run close here; next `/auto` invocation routes to **`/intake`** (`drain_terminated=true`; `drain_terminated_reason=no_open_stories`; `backlog_drain_stories_remaining_budget=3` of `10` left unused).
- **Open R-xxxx anchors status (post-closure)**: R-0077 **delivered** (this trailer). Next research anchor allocation deferred to the next `/discovery`-phase subagent when a new work item is intaked.

## R-0078 — US-0092: full-autonomy `/auto`, outer driver, self-verify UAT, TOKEN_PROFILE orthogonality

- **Date**: 2026-06-06
- **Topic**: Opt-in full-autonomy orchestration beyond **US-0088** documented outer-driver equivalence
- **Query**: How should **`AUTO_FLOW_MODE=full_autonomy`** compose with **US-0088** stop matrix, ship a stdlib outer-driver script, expand UAT self-verify beyond **US-0065/66** generated-project scope, and audit **`TOKEN_PROFILE`** so it affects token cost only — not automation level?
- **Status**: `delivered` (discovery + research extensions below; Q1–Q6 resolved; delivery closed at curator **`/refresh-context`** **`2026-06-06T22:45:00Z`**)
- **Intake plan areas**: `full-autonomy-flow-mode`, `outer-driver-script`, `self-verify-uat-runtime`, `block-auto-resolve`, `drain-without-pause`, `token-profile-orthogonality`, `docs-tests-parity`
- **Open questions for TL**:
  1. Outer-driver invocation model (CLI wrapper vs documented Cursor hook vs `/loop` composition)
  2. Full_autonomy stop matrix — which **US-0088** gates relax vs remain hard
  3. UAT probe catalog and fail-closed reason codes for unresolvable stacks
  4. Block-retry ledger schema and cap interaction with **`AUTO_IMPLEMENTATION_LOOP`**
  5. TOKEN_PROFILE orthogonality audit grep scope (scratchpad comments, auto-orchestration-reference, runbook, README)
- **Related**: **US-0088**, **US-0044**, **US-0065**, **US-0066**, **US-0080**, **R-0071**
- **Discovery extension (2026-06-06T18:30:00Z, po, `orchestrator_run_id=auto-20260606-03`, `fresh_context_marker=po-US0092-discovery-20260606T183000Z-fresh`)**:
  - **Flow-mode contract reaffirmed**: **`AUTO_FLOW_MODE=full_autonomy`** is default-off alongside **`manual`** and **`auto_until_decision`**; discovery locks the six-step operator flow (enable → outer-driver start → inner lifecycle + self-verify → bounded block retry → drain-without-pause → deterministic stop). **`TOKEN_PROFILE`** orthogonality is a hard operator constraint — research must enumerate conflicting prose locations and propose grep + contract-test markers without changing tier semantics.
  - **Outer-driver research priority**: stdlib **`scripts/`** entrypoint that re-invokes **`/auto`** until stop — not operator-manual-only; must be deterministically equivalent to **US-0088** outer-driver contract. Compare CLI wrapper vs documented Cursor hook vs **`/loop`** composition; lock argv, exit codes, and runbook recipe.
  - **Stop matrix (discovery ask)**: classify **US-0088** gates into **hard** (isolation, strict-proof, publish, decision_gate, security deny-list) vs **relaxable under full_autonomy** (transient blocked/missing_input, UAT/QA retry under **`AUTO_IMPLEMENTATION_LOOP`**). **`RELEASE_PUBLISH_MODE=auto`** remains explicit opt-in.
  - **Self-verify expansion**: derive UAT steps from acceptance; probe catalog for build/test/API/browser/health keyed by stack profile; fail closed **`UAT_PROBE_UNRESOLVED`** (name TBD at architecture) — compose **US-0065** / **US-0066** beyond generated-project scope.
  - **Block-retry ledger**: per-attempt schema (timestamp, stop_reason, remediation_action, outcome); cap interaction with **`AUTO_LOOP_MAX_CYCLES`** and **`AUTO_IMPLEMENTATION_LOOP`**; names-only evidence.
  - **Drain-without-pause**: segment boundary must refresh **`resume_brief`** + **`state.md`** per **DEC-0069** before outer driver schedules next item; scheduler mutex with **US-0087** unchanged.
  - **Deliverables for `/research` closure**: normative stop-matrix table, outer-driver sketch, probe catalog draft, ledger schema, TOKEN_PROFILE audit file list, contract-test marker inventory — feed **`/architecture`** **`# US-0092`**.

### Research extension (2026-06-06T19:05:00Z, tech-lead, `orchestrator_run_id=auto-20260606-03`, `fresh_context_marker=tl-US0092-research-20260606T190500Z-fresh`)

- **Status**: **closed for `/research`** — Q1–Q6 resolved; **`/architecture`** next. No new **`R-xxxx`** allocated (extend **`R-0078`** per **DEC-0011** intake anchor).
- **External (EARLY_RESEARCH)**: Industry outer-loop drivers (Microsoft Conductor script steps with exit-code routing; SREGym `driver_loop`; intellegix `loop_driver.py` exit codes 0=complete / 1=max-iterations / 2=budget / 3=stagnation / 124=timeout) confirm **stdlib subprocess loop + deterministic exit-code vocabulary + resume state file** as the portable pattern — aligns with **US-0088** Option B equivalence without vendor Cursor multi-turn guarantees.

#### Q1 — Outer-driver invocation model (`status=resolved`)

| Option | Summary | Verdict |
|--------|---------|---------|
| A | **Shipped stdlib Python script** under **`scripts/`** (recommended name **`auto_outer_driver.py`**) — polls **`resume_brief`** + **`state.md`** phase boundary, re-invokes documented **`/auto`** hook until deterministic stop | **Preferred** — satisfies AC-2 “not operator-manual-only”; active + **`template/`** mirror per **US-0017**. |
| B | **Documented Cursor hook only** (operator copies `/auto start-from=…` each turn) | **Rejected as sole delivery** — **US-0088** Option B allowed as equivalence class but **US-0092** requires shipped script. |
| C | **`/loop` command composition** | **Rejected** — **`/loop`** is in-session recurring prompt cadence, not cross-turn lifecycle orchestration with **DEC-0038** / **DEC-0069** boundary refresh. |

**Script sketch (architecture-locks exact names)**:

- **Activation gate**: require merged scratchpad **`AUTO_FLOW_MODE=full_autonomy`** (exact literal); default-off — exit **2** with reason **`AUTO_FLOW_MODE_NOT_FULL_AUTONOMY`** when absent or other mode.
- **Stdlib-only**: **`argparse`**, **`json`**, **`hashlib`**, **`pathlib`**, **`subprocess`**, **`re`**, **`datetime`** — no third-party deps.
- **Argv**: `--repo PATH` (default `.`); `--max-cycles INT` (optional override of **`AUTO_LOOP_MAX_CYCLES`**); `--max-stories INT` (optional override of **`AUTO_BACKLOG_MAX_STORIES`**); `--dry-run` (emit planned invocations only); `--invoke-cmd TEXT` (optional shell prefix — e.g. documented Cursor CLI wrapper; default prints normative **`/auto …`** line for operator/agent runner).
- **Loop body**: (1) read **`handoffs/resume_brief.md`** **`intended_resume_phase`** + **`orchestrator_run_id`**; (2) invoke hook; (3) parse latest **`state.md`** phase-boundary block for **`stop_reason`**, **`next_scheduled_phase`**, drain counters; (4) branch — continue, drain-advance, block-retry, or exit.
- **Exit codes** (process-level; architecture may add **`stop_reason` stdout token**):

| Code | Meaning |
|------|---------|
| **0** | **`completed`** — segment/portfolio terminal per policy (incl. empty backlog when drain enabled). |
| **1** | Hard stop — **`decision_gate`**, unrecoverable **`error`**, isolation/strict-proof failure, security deny. |
| **2** | Configuration — **`AUTO_FLOW_MODE`** not **`full_autonomy`**, scratchpad parse failure. |
| **3** | **`loop_max`** — **`AUTO_LOOP_MAX_CYCLES`** exhausted. |
| **4** | **`BACKLOG_MAX_STORIES_REACHED`** / drain cap. |
| **5** | **`pause_request`** / **`AUTO_PAUSE_REQUEST`**. |
| **6** | Recoverable block retry cap exhausted (**`BLOCK_RETRY_CAP_EXHAUSTED`**). |
| **124** | Subprocess/hook **timeout** (optional **`AUTO_OUTER_DRIVER_TIMEOUT_SECONDS`**). |

- **Runbook recipe**: new subsection **`### Full-autonomy outer driver (US-0092)`** — enable scratchpad keys → run **`python scripts/auto_outer_driver.py --repo .`** once → interpret exit code table → troubleshooting (stale brief, scheduler mutex, caps).
- **Spawn-only preserved**: script **loops invocations**, never performs phase-role work (**`BUG-0006`** / **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** unchanged).

#### Q2 — Full_autonomy stop matrix vs **US-0088** (`status=resolved`)

**Invariant**: **`full_autonomy`** relaxes **recoverable transient stops** and **operator re-invocation**, not **governance gates**.

| Condition | **US-0088** (all modes) | **`full_autonomy` delta** | Operator notify |
|-----------|-------------------------|---------------------------|-----------------|
| Next phase, no hard stop | Continue inner `/auto` | Same; outer driver **re-invokes** when Cursor ends turn early | Quiet OK if **`AUTO_QUIET=1`** |
| **`decision_gate`** | Hard stop | **No change — hard** | Always |
| Unrecoverable **`error`** | Hard stop | **No change — hard** | Always |
| Critical **`missing_input`** | Hard stop | **No change — hard** | Always |
| Transient **`missing_input`** (recoverable — e.g. stale brief fixable by refresh) | Hard stop | **Relaxable** — bounded block-retry → remediation phase | Notify on cap |
| **`pause_request`** / **`AUTO_PAUSE_REQUEST`** | Hard stop | **No change — hard** | Always |
| **`loop_max`** / **`AUTO_LOOP_MAX_CYCLES`** | Hard stop | **No change — hard** (outer + inner caps) | Always |
| **`blocked`** — sync/scope/transient | Hard stop | **Relaxable** when ledger classifies recoverable | Notify on cap |
| **`blocked`** — isolation / strict-proof / ownership | Hard stop | **No change — hard** | Always |
| UAT/QA fail | Hard stop (operator) | **Relaxable** when **`AUTO_IMPLEMENTATION_LOOP=1`** — retry **`execute`→`qa`→`verify-work`** within caps | Notify on cap |
| Segment complete + **`AUTO_BACKLOG_DRAIN=1`** | Advance (may need manual re-**`/auto`**) | **Drain-without-pause** — outer driver schedules next item **immediately** | Segment handoff notify |
| **`BACKLOG_MAX_STORIES_REACHED`** | Hard stop | **No change — hard** | Always |
| **`AUTO_SCHEDULER_CONFLICT`** | Hard stop | **No change — hard** | Always |
| **`RELEASE_PUBLISH_MODE=auto`** | Explicit opt-in | **No change — hard default-off** | Always on publish |
| Security deny (**.env`**, intake evidence mutation) | Hard deny | **No change — hard** | Always |

**Orthogonal keys (unchanged semantics)**: **`TOKEN_PROFILE`**, **`AUTO_QUIET`**, **`PHASE_MODE`**, **`PERMISSION_MODE`** — **`full_autonomy`** does not substitute for any of these.

#### Q3 — UAT probe catalog + fail-closed reason codes (`status=resolved`)

**Scope**: generalize **US-0065** runtime readiness + **US-0066** **`TEST_COMMAND`** beyond generated-project repos when stack profile resolves from repo signals (**`package.json`**, **`pyproject.toml`**, **`go.mod`**, **`pom.xml`**, **`*.csproj`**, scratchpad **`TEST_COMMAND`**, **`docs/engineering/runtime-connectivity.md`**).

**Probe catalog** (acceptance step → probe; architecture locks table in **`# US-0092`**):

| Probe kind | Resolves when | Execution | Evidence surface |
|------------|---------------|-----------|------------------|
| **`build`** | Stack profile maps build script (`npm run build`, `cargo build`, `dotnet build`, …) | Subprocess, bounded timeout | **`uat.json`** `probe_results[]`, **`qa-findings.md`** |
| **`test`** | **`TEST_COMMAND`** non-empty (**US-0063** / **US-0066**) or profile default | Subprocess | Same + command stdout/stderr **path refs** (not inline secrets) |
| **`api_health`** | **`runtime-connectivity.md`** or acceptance names URL/health path | HTTP GET (stdlib **`urllib`**) | status code + latency |
| **`process_health`** | Acceptance names startup command (**US-0065** pattern) | Subprocess + readiness poll | retry ledger snippet |
| **`browser_smoke`** | Web stack + optional **`PLAYWRIGHT_*`** / documented curl fallback | Subprocess or HTTP | screenshot/path ref optional |
| **`cli_smoke`** | Acceptance names CLI + expected exit/output | Subprocess | exit code + truncated stdout |
| **`manual_operator`** | Step explicitly requires human judgment | **Not auto-run** | **`UAT_PROBE_UNRESOLVED`** unless operator maps to probe |

**Fail-closed reason codes** (no silent PASS):

| Code | When |
|------|------|
| **`UAT_PROBE_UNRESOLVED`** | Acceptance step cannot map to any probe for resolved stack profile |
| **`UAT_STACK_PROFILE_UNKNOWN`** | No deterministic profile from repo signals |
| **`UAT_PROBE_TIMEOUT`** | Probe exceeded bounded timeout |
| **`UAT_PROBE_FAILED`** | Probe ran; assertion failed |
| **`UAT_PROBE_FORBIDDEN`** | Step would require **`.env`**, gitignored secret path, or intake evidence mutation (**AC-10**) |
| **`UAT_PROBE_PASS`** | Probe succeeded (evidence recorded) |

**Composition**: **`/verify-work`** and **`/qa`** share probe resolver lib (recommended **`scripts/uat_probe_lib.py`** + **`template/`** mirror); generated-project path remains **US-0065** / **US-0066** fast path when **`stack_profile=generated`**.

#### Q4 — Block-retry ledger schema + **`AUTO_IMPLEMENTATION_LOOP`** cap interaction (`status=resolved`)

**Ledger path**: append-only **`handoffs/auto_block_retry/<orchestrator_run_id>.jsonl`** (names-only; no secrets, no file contents).

**Record schema** (one JSON object per line):

```json
{
  "attempt_id": "br-<orchestrator_run_id>-<seq>",
  "timestamp": "<ISO8601Z>",
  "orchestrator_run_id": "<id>",
  "story_id": "US-xxxx|BUG-xxxx|(none)",
  "stop_reason": "blocked|missing_input|uat_fail|qa_fail",
  "reason_code": "<optional sub-code>",
  "remediation_action": "execute|qa|verify-work|refresh-context|outer_reinvoke",
  "outcome": "retry_scheduled|hard_stop|cap_exhausted",
  "outer_cycle_index": 1,
  "implementation_loop_index": 1
}
```

**Cap interaction (recommended lock)**:

| Cap | Scope | Interaction |
|-----|-------|-------------|
| **`AUTO_LOOP_MAX_CYCLES`** | **Outer-driver `/auto` invocations** (incl. drain advances) | Each outer loop iteration increments; hard stop at cap (**unchanged**). |
| **`AUTO_IMPLEMENTATION_LOOP`** | **Inner** **`execute`↔`qa`↔`verify-work`** remediation | When **`1`**, UAT/QA fail triggers remediation attempts; each full remediation cycle increments **`implementation_loop_index`**; hard stop when **`implementation_loop_index >= AUTO_LOOP_MAX_CYCLES`** within same story segment. |
| **`AUTO_BLOCK_RETRY_MAX`** (new scratchpad key, default **3**, architecture-locked) | Per-**`stop_reason`** recoverable retries | Block-retry ledger rows for same **`(story_id, stop_reason)`** ≤ max; exceed → **`BLOCK_RETRY_CAP_EXHAUSTED`** (exit **6**). |
| **`AUTO_BACKLOG_MAX_STORIES`** | Drain breadth | Unchanged — outer driver exit **4**. |

**Ordering**: outer driver checks **`AUTO_LOOP_MAX_CYCLES`** first; inner orchestrator checks **`AUTO_IMPLEMENTATION_LOOP`** + **`AUTO_BLOCK_RETRY_MAX`** before scheduling remediation; unrecoverable classes bypass ledger.

#### Q5 — **`TOKEN_PROFILE` orthogonality audit (`status=resolved`)

**Hard rule (operator constraint)**: **`TOKEN_PROFILE=lean|balanced|full`** affects **context breadth / token cost only** — never automation level, phase depth, drain, outer-driver invocation, or **`AUTO_FLOW_MODE`**.

**Grep scope** (active + **`template/`** where mirrored):

| Surface | Purpose |
|---------|---------|
| **`.cursor/scratchpad.md`**, **`template/.cursor/scratchpad.md`**, **`.cursor/scratchpad.local.example.md`** | Comment blocks |
| **`docs/engineering/auto-orchestration-reference.md`** | TOKEN_PROFILE tier prose |
| **`docs/engineering/runbook.md`** | Token-cost section — **known conflict**: both active + template line **`lowers default automation breadth`** (must fix at execute) |
| **`README.md`**, **`template/README.md`**, **`its_magic/README.md`** | Operator-facing tier docs |
| **`.cursor/commands/auto.md`** | Cross-refs only (should already be orthogonal post-**US-0088**) |

**Forbidden pattern grep** (CI/contract negative assertions): `automation breadth`, `lowers default automation`, `TOKEN_PROFILE.*drain`, `TOKEN_PROFILE.*outer`, `TOKEN_PROFILE.*full_autonomy`, `lean.*less automation`, `full.*more automation`.

**Contract-test marker strings** (add in **`tests/auto_command_contract_test.py`** at execute):

- Positive: **`TOKEN_PROFILE controls context breadth / token cost only`** (or existing Caveman non-substitution extension).
- Positive: **`AUTO_FLOW_MODE=full_autonomy`** literal in scratchpad comment block.
- Negative: runbook must **not** contain **`lowers default automation breadth`** after fix.
- Positive: **`scripts/auto_outer_driver.py`** exists (post-execute) + doc reference **`Full-autonomy outer driver (US-0092)`**.

#### Q6 — Contract-test + template parity inventory (`status=resolved`)

| # | Surface | Parity |
|---|---------|--------|
| 1 | **`scripts/auto_outer_driver.py`** | active + **`template/scripts/`** |
| 2 | **`scripts/uat_probe_lib.py`** (if split from monolith) | active + template |
| 3 | Scratchpad keys: **`AUTO_FLOW_MODE`** enum adds **`full_autonomy`**; optional **`AUTO_BLOCK_RETRY_MAX`**, **`AUTO_OUTER_DRIVER_TIMEOUT_SECONDS`** | active + template scratchpad + local example |
| 4 | **`.cursor/commands/auto.md`**, **`docs/engineering/auto-orchestration-reference.md`** | stop matrix § **US-0092** |
| 5 | **`.cursor/commands/verify-work.md`**, **`.cursor/commands/qa.md`** | self-verify probe contract excerpt |
| 6 | **`docs/engineering/runbook.md`** | outer-driver + full_autonomy subsection |
| 7 | **`docs/engineering/architecture.md`** | **`# US-0092`** (architecture phase) |
| 8 | **`tests/auto_command_contract_test.py`** | markers per Q5 + outer-driver + drain-advance-without-operator phrases |
| 9 | **`tests/run-tests.ps1`** / **`.sh`** harness section (candidate **§31**) | optional at architecture |

- **Linked (closure)**: **US-0088**, **US-0044**, **US-0065**, **US-0066**, **US-0080**, **US-0087**, **US-0048**, **US-0056**, **DEC-0069**, **DEC-0038**, **R-0071**, **R-0042**
- **Confidence**: high (repo inventory + **US-0088** `# US-0088` stop matrix extended; runtime Cursor scheduling remains out of scope)
- **Next phase pointers (`/architecture`)**: lock companion **`DEC-xxxx`**, **`# US-0092`** section, exact script filename/exit codes, probe lib split, **`AUTO_BLOCK_RETRY_MAX`** default, runbook + orthography fix list.

### Delivery closure (R-0078 — US-0092, 2026-06-06, curator, auto-20260606-03)

> Append-only closure trailer for R-0078. US-0092 shipped with S0081 released on 2026-06-06T22:30:00Z; this refresh-context pass reconciles the research anchor to `status=delivered`. No new research questions opened; no new R-xxxx id allocated; no rewrite of DEC-0078 or architecture `# US-0092`. `fresh_context_marker=curator-S0081-US0092-refresh-context-20260606T224500Z-fresh`.

- **Anchor status**: `R-0078.status=delivered` (US-0092 **delivered** @ 2026-06-06T22:45:00Z curator refresh). Single-story anchor; no shared-anchor split required.
- **US-0092 delivery coordinates**: sprint `S0081`; binding decision `DEC-0078` (composes on `US-0088`, `DEC-0062`, `DEC-0047`, `DEC-0048`); architecture section `docs/engineering/architecture.md` `# US-0092`; release runtime proof `rp-auto-20260606-03-release-release-20260606T223000Z-S0081-US0092` / `proof_hash=c090713e2791b75a697db7e09c9a874a257e3d79b742436837b6d84d2d1d0c78`; refresh-context runtime proof `rp-auto-20260606-03-refresh-context-curator-20260606T224500Z-S0081-US0092` / `proof_hash=1c258ea1f3e22f19aa5019ca9a7b060da75950ca52c67d0e8b2795ef55d974f9`; AC-1..AC-10 all `[x]` in `docs/product/backlog.md` `## US-0092`.
- **Resolution matrix outcome**: all discovery/research asks resolved at `/architecture` → `/sprint-plan` and verified through `/execute` → `/qa` → `/verify-work` → `/release`. Outer driver + UAT probe lib + stop matrix + block-retry ledger + TOKEN_PROFILE orthography audit shipped; UAT **10/10** PASS.
- **Evidence refs (US-0092 delivery)**: `sprints/S0081/release-findings.md` (PASS); `handoffs/releases/S0081-release-notes.md`; `sprints/S0081/uat.md` (10/10 PASS); `sprints/S0081/uat.json`; `sprints/S0081/qa-findings.md` (PASS); `sprints/S0081/summary.md` (Release + Refresh-context blocks); `sprints/S0081/plan-verify.json` (PASS); `decisions/DEC-0078.md`; `docs/engineering/architecture.md` `# US-0092`; `docs/product/backlog.md` `## US-0092` (DONE + `release_notes` + `refresh_context_notes`); `docs/product/acceptance.md` (US-0092 row `[x]`); `handoffs/release_queue.md` (`S0081=released`); `docs/engineering/state.md` (Refresh-context checkpoint); `docs/engineering/state-archive/state-pack-20260606-y.md` (release checkpoint archive).
- **Portfolio drain closure signal**: with US-0092 closed, `docs/product/backlog.md` contains **zero** OPEN stories and **zero** OPEN bugs. Backlog-drain segment (`US-0090` → `US-0091` → `US-0092`) on `auto-20260606-03` closes here; next `/auto` invocation routes to **`/intake`** (`drain_terminated=true`; `drain_terminated_reason=no_open_stories`; `backlog_drain_stories_remaining_budget=2` of `10` left unused).
- **Open R-xxxx anchors status (post-closure)**: R-0078 **delivered** (this trailer). Next research anchor allocation deferred to the next `/discovery`-phase subagent when a new work item is intaked.

## R-0079 — US-0093: Cursor browser-integrated UAT self-test

- **Date**: 2026-06-06
- **Topic**: Cursor built-in browser as primary UAT probe path; manual_operator UI automation; probe stub completion
- **Query**: How should its-magic wire **DEC-0078** `browser_smoke` / `manual_operator` probes to Cursor browser MCP tools, stdlib fallbacks, and `uat.json` evidence without silent PASS?
- **Sources**:
  - https://cursor.com/docs/agent/tools/browser
  - Internal: `scripts/uat_probe_lib.py`, `decisions/DEC-0078.md`, `.cursor/commands/verify-work.md`, `.cursor/commands/qa.md`, **R-0041**
- **Findings** (discovery extension 2026-06-06 — **do not close**; research phase owns closure):
  - **Root cause (confirmed)**: `scripts/uat_probe_lib.py` `execute_probe` returns **`UAT_PROBE_UNRESOLVED`** for **`process_health`**, **`browser_smoke`**, and **`cli_smoke`** (stub branches); **`manual_operator`** always unresolved at execution despite **`classify_step`** routing. **US-0092** / **DEC-0078** delivered catalog + fail-closed vocabulary only — execution gap is intentional deferral now closed by **US-0093**.
  - **Two-tier execution model (discovery-locked)**:
    - **Tier 1 — stdlib** (`uat_probe_lib.py`): classify → resolve stack/URL/port; run HTTP GET health or Playwright/curl subprocess when **`UAT_BROWSER_PROBE_MODE`** is fallback or MCP probe signals unavailable; complete **`process_health`** (subprocess + readiness poll) and **`cli_smoke`** (exit-code assertion); emit reason codes; never silent PASS.
    - **Tier 2 — agent** (`verify-work.md`, `qa.md`, `execute.md`): when mode is **`cursor`** (default) and kind is **`browser_smoke`** or automatable **`manual_operator`**, subagent invokes Cursor browser MCP (navigate, click, type, scroll, screenshot, console/network read per [Cursor Browser docs](https://cursor.com/docs/agent/tools/browser)); writes **`browser_evidence_refs`** to **`uat.json`** `probe_results[]` and **`qa-findings.md`**.
  - **Scratchpad key (AC-1 stub)**: **`UAT_BROWSER_PROBE_MODE=cursor|http_fallback|playwright_fallback`** (default **`cursor`**); composes with **`PERMISSION_MODE`** and Cursor browser approval settings (manual / allow-list / auto-run).
  - **`manual_operator` routing (discovery stub)**: reclassify steps with UI/workflow verbs (**click**, **fill**, **navigate**, **smoke**, **form**, **submit**) to browser plans; retain **`manual_operator`** + **`UAT_PROBE_UNRESOLVED`** when judgment signals present (**visually**, **aesthetically**, **operator confirms**, **subjective**).
  - **New fail-closed codes (minimum)**: **`UAT_BROWSER_UNAVAILABLE`**, **`UAT_BROWSER_PROBE_FAILED`**, **`UAT_BROWSER_PROBE_TIMEOUT`** — applied when cursor path and configured fallback both fail.
  - **Evidence contract (AC-5 stub)**: `probe_results[]` field **`browser_evidence_refs`** — screenshot paths, console error count/summary, network failure summary (names/paths only, no secrets); aligns with **US-0065** AC-6 mirror fields in **`qa-findings.md`**.
  - **Security**: no auto-read **`.env`**, no credential auto-fill, **`UAT_PROBE_FORBIDDEN`** unchanged; respect Cursor origin/approval guardrails; enterprise allowlist behavior documented as operator-configured (vendor).
- **Open questions for `/research` (Q1–Q6)**:
  1. **Agent-browser command contract** — exact MCP invocation sequence, evidence write-back hook, and failure propagation from agent tier to lib reason codes.
  2. **Verb routing table** — deterministic automatable vs judgment-only classifier extensions in `classify_step`.
  3. **Fallback selection** — MCP-unavailable detection heuristic; HTTP vs Playwright precedence; CI/headless behavior.
  4. **`process_health` / `cli_smoke` parse rules** — acceptance-text → command/expected-output extraction; readiness poll timeout defaults.
  5. **Evidence schema** — artifact directory layout, field cardinality, console/network summary normalization.
  6. **Parity inventory** — contract-test markers (`pytest -k us0093`), template mirror list, `check_intake_template_parity.py --scope=us-0093` wiring.
- **Risks**:
  - Browser MCP unavailable in CI/headless → **`UAT_BROWSER_UNAVAILABLE`** + fallback modes; must not false PASS.
  - Over-automation of judgment steps → verb routing table + explicit deny signals.
  - Dual-tier desync (lib PASS without agent evidence) → evidence-required fields + fail-closed when refs missing.
  - Secret exposure via browser form fill → hard deny + no credential paths.
- **Linked**: US-0093, US-0092, US-0065, US-0088, R-0041, DEC-0078
- **Confidence**: high (Q1–Q6 resolved at research extension below)
- **Status**: **closed for `/research`** — Q1–Q6 resolved; **`/architecture`** next

### Research extension (2026-06-06T23:15:00Z, tech-lead, `orchestrator_run_id=auto-20260606-04`, `fresh_context_marker=tl-US0093-research-20260606T231500Z-fresh`)

- **Status**: **closed for `/research`** — Q1–Q6 resolved; **`/architecture`** next. No new **`R-xxxx`** allocated (extend **`R-0079`** per **DEC-0011** intake anchor).
- **External (EARLY_RESEARCH)**: [Cursor Browser docs](https://cursor.com/docs/agent/tools/browser) confirm native MCP tools (**navigate**, **click**, **type**, **scroll**, **screenshot**, **console output**, **network traffic**); dev-server awareness; log files for selective grep; approval modes (manual / allow-list / auto-run); enterprise origin allowlist — aligns with two-tier model where **stdlib cannot invoke MCP** (**BUG-0006** / **US-0048** spawn-only preserved).

#### Q1 — Agent-browser command contract (`status=resolved`)

**Invariant**: **`scripts/uat_probe_lib.py`** never calls Cursor browser MCP directly. When **`UAT_BROWSER_PROBE_MODE=cursor`** (default) and **`classify_step`** yields **`browser_smoke`** or automatable **`manual_operator`**, the lib returns a **probe plan** with **`execution_tier=agent`** and **`reason_code=UAT_PROBE_UNRESOLVED`** until the phase subagent completes browser work — **no silent PASS**.

**Dispatch table**:

| Caller | `execution_tier` | Behavior |
|--------|------------------|----------|
| **`uat_probe_lib.py` CLI** (`--report`) | **`stdlib`** or **`agent_deferred`** | In **`cursor`** mode: emit plan + **`UAT_PROBE_UNRESOLVED`** (or configured fallback if **`--allow-fallback`**) — never fabricate **`browser_evidence_refs`**. |
| **`/verify-work`**, **`/qa`**, **`/execute`** subagent | **`agent`** | Execute MCP sequence below; merge final **`probe_results[]`** row into **`sprints/Sxxxx/uat.json`** + mirror **`qa-findings.md`**. |

**Normative MCP sequence** (architecture locks exact wording in command specs):

1. **Resolve target URL** — read **`docs/engineering/runtime-connectivity.md`** (first `http(s)://`); else infer dev-server port from **`package.json`** `scripts.dev` / `scripts.start` + scratchpad **`DEV_SERVER_PORT`**; prefer existing running server (Cursor dev-server awareness per vendor docs).
2. **`browser_navigate`** — load health/app URL; respect enterprise origin allowlist (operator-configured).
3. **Step plan** — map acceptance step verbs to **`browser_click`** / **`browser_type`** / **`browser_scroll`** only when automatable (Q2); **never** fill password/credential fields or read **`.env`** paths.
4. **`browser_screenshot`** — write to **`sprints/Sxxxx/evidence/browser/<probe_id>-<seq>.png`** (max **5** per probe — Q5).
5. **Console + network evidence** — read console log file / network summary per Cursor browser tools; emit **counts + summary path refs** only (no inline secrets).
6. **Verdict** — set **`passed`**, **`reason_code`** (`UAT_PROBE_PASS` | **`UAT_BROWSER_PROBE_FAILED`** | **`UAT_BROWSER_PROBE_TIMEOUT`**), and **`browser_evidence_refs`** (required when **`passed=true`** in **`cursor`** mode).
7. **Fallback trigger** — if MCP tools unavailable (headless CI, enterprise denylist, subagent tool list lacks browser): record **`UAT_BROWSER_UNAVAILABLE`**, then run stdlib fallback chain (Q3) in same subagent turn when mode allows; if fallback also fails → **`UAT_BROWSER_PROBE_FAILED`** (no PASS).

**Write-back hook** (recommended at architecture):

- Subagent updates **`uat.json`** `probe_results[]` in place (match on **`step`** hash or **`probe_id`** UUID assigned at classify time).
- Optional lib helper: **`python scripts/uat_probe_lib.py --merge-result <path/to/fragment.json>`** — validates schema, enforces evidence-required-on-PASS for **`cursor`** mode.
- **`qa-findings.md`** mirror: duplicate **`browser_evidence_refs`** + **`probe_mode`** under runtime browser subsection (**US-0065** AC-6 fields).

**Rejected alternative**: stdlib-only Playwright as primary — rejected; operator intake locks **Cursor browser** as primary path (**R-0041** / discovery contract).

#### Q2 — `manual_operator` verb routing table (`status=resolved`)

**Classifier extension** in **`classify_step`** — **precedence: judgment deny signals win** over automatable UI signals when both appear in one step.

| Signal class | Tokens (case-insensitive substring) | Route | `reason_code` at classify |
|--------------|-------------------------------------|-------|---------------------------|
| **Judgment-only** | `visually`, `aesthetically`, `operator confirms`, `subjective`, `human judgment`, `eyeball`, `manually verify appearance`, `approve layout` | **`manual_operator`** | **`UAT_PROBE_UNRESOLVED`** |
| **Secret/forbidden** | `.env`, `password`, `credential`, `api key`, `intake_evidence` | **`None`** | **`UAT_PROBE_FORBIDDEN`** |
| **Automatable UI** | `click`, `fill`, `navigate`, `smoke`, `form`, `submit`, `button`, `page load`, `scroll`, `type into`, `select`, `checkbox`, `dropdown`, `ui`, `browser` | **`browser_smoke`** (or **`manual_operator`→`browser_smoke` reclass**) | `""` when URL/stack resolves |
| **Generic manual** | `manual`, `operator`, `human`, `judgment` (without UI verbs) | **`manual_operator`** | **`UAT_PROBE_UNRESOLVED`** |

**Reclass rule**: when step matches **automatable UI** and **not** judgment-only, override prior **`manual_operator`** classification to **`browser_smoke`** with **`execution_tier=agent`** when **`UAT_BROWSER_PROBE_MODE=cursor`**.

**Self-test fixtures** (execute): mixed-verb step `"operator visually confirms button click"` → **`manual_operator`** + unresolved; `"click submit on login form smoke test"` → **`browser_smoke`** when health URL present.

#### Q3 — Fallback selection (`status=resolved`)

**Scratchpad key** (AC-1): **`UAT_BROWSER_PROBE_MODE=cursor|http_fallback|playwright_fallback`** (default **`cursor`**).

| Mode | Primary | Fallback chain (on failure / MCP unavailable) |
|------|---------|-----------------------------------------------|
| **`cursor`** | Agent MCP sequence (Q1) | **`http_fallback`** → optional **`playwright_fallback`** when scratchpad **`UAT_BROWSER_FALLBACK_CHAIN=1`** (default **on** in CI) |
| **`http_fallback`** | Stdlib **`urllib`** GET to health URL (reuse **`api_health`** logic + optional HTML title sniff) | None — fail **`UAT_BROWSER_PROBE_FAILED`** |
| **`playwright_fallback`** | Subprocess **`npx playwright screenshot`** or **`python -m playwright`** when **`PLAYWRIGHT_*`** / **`node_modules/@playwright`** detected | **`http_fallback`** if Playwright missing → **`UAT_BROWSER_UNAVAILABLE`** |

**MCP-unavailable heuristic** (deterministic):

1. Environment **`CI=true`** or **`GITHUB_ACTIONS=true`** → skip MCP; enter fallback chain immediately with **`UAT_BROWSER_UNAVAILABLE`** recorded on probe row.
2. Subagent tool inventory lacks browser MCP → same.
3. Enterprise origin allowlist blocks target URL → **`UAT_BROWSER_UNAVAILABLE`** + operator message (vendor-configured).

**HTTP vs Playwright precedence**: in **`cursor`** mode fallback, try **HTTP first** (cheaper, stdlib-only), then **Playwright** only when step requires DOM interaction verbs and HTTP returned 200 without sufficient evidence.

**CI/headless**: document **`UAT_BROWSER_PROBE_MODE=http_fallback`** for downstream CI; never false PASS — missing URL → **`UAT_PROBE_UNRESOLVED`**.

#### Q4 — `process_health` / `cli_smoke` parse rules (`status=resolved`)

**`process_health`** (stdlib **`execution_tier=stdlib`** only):

| Source | Extraction rule |
|--------|-----------------|
| Acceptance step | Backtick command `` `npm run dev` `` or quoted `"npm start"`; regex `run\s+([^\s;]+)` after startup verbs |
| **`package.json`** | `scripts.start` / `scripts.dev` when profile **`node`** |
| Scratchpad | **`DEV_SERVER_COMMAND`** override |
| Readiness | Poll **`_read_health_url(repo)`** every **`UAT_PROCESS_HEALTH_POLL_INTERVAL_SECONDS`** (default **2**) until HTTP 2xx or cap **`UAT_PROCESS_HEALTH_POLL_SECONDS`** (default **60**, architecture-locked) |
| Verdict | Subprocess alive + readiness → **`UAT_PROBE_PASS`**; timeout → **`UAT_PROBE_TIMEOUT`**; non-zero exit → **`UAT_PROBE_FAILED`** |

**`cli_smoke`**:

| Source | Extraction rule |
|--------|-----------------|
| Acceptance step | Backtick command; patterns `exit code 0`, `exits successfully`, `run CLI` |
| Stack default | **`python -m <module> --help`** only when step explicitly says `help` / `version` — else unresolved |
| Assertion | **`exit_code == 0`** required; optional stdout substring match from `expect "..."` / `output contains "..."` |
| Verdict | Same reason-code family as **DEC-0078** §4 |

**Rejected alternative**: LLM free-form command inference — rejected; parse rules must be regex/deterministic for contract tests.

#### Q5 — Evidence schema (`status=resolved`)

**Artifact layout**: **`sprints/Sxxxx/evidence/browser/`** (gitignored binary OK; path refs in JSON only).

**`probe_results[]` row** (extends **DEC-0078** schema):

```json
{
  "probe_id": "pr-<uuid>",
  "probe_kind": "browser_smoke",
  "execution_tier": "agent",
  "probe_mode": "cursor",
  "step": "<truncated acceptance step>",
  "passed": true,
  "reason_code": "UAT_PROBE_PASS",
  "browser_evidence_refs": {
    "navigation_url": "http://localhost:3000/",
    "screenshots": ["sprints/Sxxxx/evidence/browser/pr-<uuid>-01.png"],
    "console_summary": {
      "error_count": 0,
      "warning_count": 1,
      "summary_path": "sprints/Sxxxx/evidence/browser/pr-<uuid>-console.txt"
    },
    "network_summary": {
      "failed_request_count": 0,
      "summary_path": "sprints/Sxxxx/evidence/browser/pr-<uuid>-network.txt"
    }
  }
}
```

**Cardinality**: max **5** screenshot paths; summary files **names/paths only** in JSON (no secret values). **`passed=true`** in **`cursor`** mode **requires** non-empty **`browser_evidence_refs.navigation_url`** + at least one screenshot or console/network summary path — else downgrade to **`UAT_BROWSER_PROBE_FAILED`**.

**`qa-findings.md` mirror** (**US-0065** AC-6): duplicate **`navigation_url`**, **`console_summary`**, **`network_summary`**, **`probe_mode`** under **Runtime browser evidence** subsection.

#### Q6 — Contract-test + template parity inventory (`status=resolved`)

| # | Surface | Parity |
|---|---------|--------|
| 1 | **`scripts/uat_probe_lib.py`** — browser mode keys, verb routing, stub completion, new reason codes, `--self-test` | active + **`template/scripts/`** |
| 2 | **`.cursor/commands/verify-work.md`**, **`qa.md`**, **`execute.md`** — **Browser UAT self-test (US-0093)** subsection with MCP sequence | active + **`template/.cursor/commands/`** |
| 3 | Scratchpad: **`UAT_BROWSER_PROBE_MODE`**, optional **`UAT_BROWSER_FALLBACK_CHAIN`**, **`UAT_PROCESS_HEALTH_POLL_SECONDS`** | active + template scratchpad + local example |
| 4 | **`docs/engineering/runbook.md`**, **`auto-orchestration-reference.md`** | browser self-test operator recipe |
| 5 | **`docs/engineering/architecture.md`** | **`# US-0093`** (architecture phase) |
| 6 | **`tests/auto_command_contract_test.py`** | **`test_us0093_*`** markers (mode key, reason codes, `browser_evidence_refs`, command excerpts) |
| 7 | **`scripts/check_intake_template_parity.py`** | new **`--scope=us-0093`** pair table (extends **us-0092** + execute.md) |
| 8 | **`tests/run-tests.ps1`** / **`.sh`** | optional harness **§32** at execute |

**Contract-test marker strings** (add at execute):

- Positive: **`UAT_BROWSER_PROBE_MODE`** literal in scratchpad comment block.
- Positive: **`browser_evidence_refs`** in verify-work + qa command excerpts.
- Positive: **`UAT_BROWSER_UNAVAILABLE`**, **`UAT_BROWSER_PROBE_FAILED`**, **`UAT_BROWSER_PROBE_TIMEOUT`** in uat_probe_lib + docs.
- Negative: command docs must **not** imply stdlib alone PASSes **`browser_smoke`** in **`cursor`** mode without evidence refs.

**Parity scope wiring**: **`python scripts/check_intake_template_parity.py --scope=us-0093`** → **`[INTAKE_TEMPLATE_PARITY_OK]`** (table authored at execute).

- **Linked (closure)**: **US-0093**, **US-0092**, **US-0065**, **US-0088**, **R-0041**, **DEC-0078**, **BUG-0006**
- **Confidence**: high (repo inventory + Cursor browser vendor docs + discovery-locked two-tier contract)
- **Next phase pointers (`/architecture`)**: lock companion **`DEC-xxxx`**, **`# US-0093`** section, exact lib API (`execution_tier`, `--merge-result`), poll defaults, evidence schema literals, **`us-0093`** parity table, contract-test inventory.

### Delivery closure trailer (2026-06-07T01:30:00Z, release, `orchestrator_run_id=auto-20260606-04`, `fresh_context_marker=release-S0082-US0093-release-20260607T013000Z-fresh`, `sprint_id=S0082`)

- **Status**: **delivered** — Q1–Q6 resolved at `/research`; architecture locked **DEC-0079**; sprint **S0082** executed, QA/verify-work/release **PASS**; **US-0093** **DONE**.
- **Resolution matrix outcome**: all discovery/research asks resolved at `/architecture` → `/sprint-plan` and verified through `/execute` → `/qa` → `/verify-work` → `/release`. Two-tier browser UAT (stdlib classify + agent Cursor browser MCP + HTTP/Playwright fallback), verb routing table, process_health/cli_smoke stub completion, browser_evidence_refs schema, and UAT_BROWSER_* reason codes shipped; UAT **10/10** PASS.
- **Evidence refs (US-0093 delivery)**: `sprints/S0082/release-findings.md` (PASS); `handoffs/releases/S0082-release-notes.md`; `sprints/S0082/uat.md` (10/10 PASS); `sprints/S0082/uat.json`; `sprints/S0082/qa-findings.md` (PASS); `sprints/S0082/summary.md`; `sprints/S0082/plan-verify.json` (PASS); `decisions/DEC-0079.md`; `docs/engineering/architecture.md` `# US-0093`; `docs/product/backlog.md` `## US-0093` (DONE + `release_notes`); `docs/product/acceptance.md` (US-0093 row `[x]`); `handoffs/release_queue.md` (`S0082=released`); `docs/engineering/state.md` (Release checkpoint).
- **Portfolio drain closure signal**: with US-0093 closed, `docs/product/backlog.md` contains **zero** OPEN stories and **zero** OPEN bugs. Backlog-drain segment (`US-0091` → `US-0092` → `US-0093`) on `auto-20260606-04` closes here; next `/auto` invocation routes to **`/intake`** (`drain_terminated=true`; `drain_terminated_reason=no_open_stories`; `backlog_drain_stories_remaining_budget=1` of `10` left unused).
- **Open R-xxxx anchors status (post-closure)**: R-0079 **delivered** (this trailer). Next research anchor allocation deferred to the next `/discovery`-phase subagent when a new work item is intaked.

## R-0080 — US-0094: README visionary intro + tiered feature hierarchy

- **Status**: **delivered** (delivery closure trailer below; curator refresh **2026-06-07T17:00:00Z**)
- **Story**: **US-0094**
- **Problem**: README opens with generic template copy; product promise (operator as dreamer + autonomous AI dev team) is buried below install instructions and a flat bullet list.
- **Research questions**:
  1. **Narrative lead pattern** — recommend a 2–3 paragraph "what this is" block before `## Features`, aligned with **DEC-0059** USER_* cells and **US-0071** metadata hygiene.
  2. **Main vs sub feature tiers** — pillar grouping for 100+ anchors without duplicating the **US-0091** catalog; use `###` under existing H2s vs a new `## Main capabilities` (architecture must not invent forbidden H2s).
  3. **Full-autonomy placement** — how to foreground **US-0092** (`AUTO_FLOW_MODE=full_autonomy`, `/auto`, drain) in operator language without contradicting default-off scratchpad contract.
  4. **Coverage-safe moves** — section-affinity rules when relocating bullets so `validate_readme_feature_coverage.py` stays `coverage_missing=[]`.
  5. **Parity workflow** — edit-once copy to `template/README.md` vs generate step; **US-0017** byte-identical requirement.
- **External refs**: Diataxis tutorial/how-to vs reference split (**R-0054**); README best practices for developer product landing pages.
- **Linked**: **US-0091**, **US-0077**, **US-0092**, **DEC-0074**, **DEC-0059**
- **Discovery findings (2026-06-07, PO, `auto-20260607-01`)**:
  - **Q1 narrative lead — RESOLVED at discovery**: 3 paragraphs before `## Features` — (1) dreamer + role-based AI team, (2) artifact-first `/intake`→`/release` workflow + pause/resume/decision gates, (3) opt-in **`AUTO_FLOW_MODE=full_autonomy`** + outer driver + `/auto` drain (**US-0092**, default-off). Replace generic tagline ("Happy coding!…"); keep H1 `# its-magic — AI dev team`. Optional one-sentence link to **`docs/developer/README.md`**.
  - **Q2 main vs sub tiers — RESOLVED at discovery**: four pillars as **`###` under `## Features (what its-magic can do)`** only — **Autonomous AI workflow**, **Quality & verification gates**, **Distribution & install**, **Operator control & ergonomics**. Each pillar: 3–6 teaser bullets (commands/flags/outcomes). **Rejected**: new `## Main capabilities` H2 (would violate **DEC-0059** budget / USER_* vocabulary). **US-0091 catalog** stays in three affinity-home blocks inside existing H2s (Features chunk, Commands chunk, Other useful capabilities chunk) — pillars do not replace catalog.
  - **Q3 full-autonomy placement — RESOLVED at discovery**: primary = intro ¶3; secondary = first pillar bullet; tertiary = existing **US-0092** catalog line in Commands affinity section. Mandatory default-off / opt-in pairing per **DEC-0078**.
  - **Q4 coverage-safe moves — RESOLVED at discovery**: affinity resolver (`readme-section-affinity.json`) is normative — slash_command→Commands, scratchpad_mode→Other useful capabilities, distribution→Features, release_gate→Commands, governance→Other useful capabilities. Catalog bullets with `US-xxxx`/`BUG-xxxx` ids must remain in same parent H2 body; cross-H2 moves forbidden; reorder within block OK. Preserve `<!-- readme-feature-coverage-catalog -->` markers (3 sites). Post-edit `validate_readme_feature_coverage.py --report` gate. Baseline: **104/104 PASS**.
  - **Q5 parity workflow — RESOLVED at discovery**: edit `README.md` once → byte-copy to `template/README.md`; verify identity before commit; no independent dual edits.
  - **Open for `/research`**: intro word-count budget for `both`×`balanced` cell; pillar-to-catalog thematic cross-reference table (navigation only, not moves); whether **DEC-0074** needs §intro hierarchy companion or discovery locks suffice for execute.

### Research extension (2026-06-07T12:30:00Z, tech-lead, `orchestrator_run_id=auto-20260607-01`, `fresh_context_marker=tl-US0094-research-20260607T123000Z-fresh`)

- **Status**: **closed for `/research`** — Q1–Q4 resolved; **`/architecture`** next. No new **`R-xxxx`** allocated (extend **`R-0080`** per **DEC-0011** intake anchor).
- **External (EARLY_RESEARCH=1)**: [Diátaxis map](https://diataxis.fr/map/) — four documentation modes (tutorial, how-to, reference, explanation) are distinct by user need, not a mandatory linear read order; [Diátaxis in complex hierarchies](https://diataxis.fr/complex-hierarchies/) — landing/README pages should read as **overviews** with headings and short intros that orient readers to deeper material without duplicating reference bodies. Confirms discovery tier split: visionary **explanation** (pre-H2 intro) + pillar **summary** (`###` teasers) + preserved **reference** (catalog blocks) + unchanged **how-to/tutorial** (`Setup`, `How-to`, walkthroughs).

#### Q1 — Pillar-to-catalog thematic affinity map (`status=resolved`)

**Normative rule**: this table is for **pillar teaser cross-links only** (e.g. “see catalog in **Commands and workflow**”) — **not** catalog relocations. Structural affinity remains **`readme-section-affinity.json`** + **DEC-0074** §4 (cross-H2 moves forbidden).

| Pillar (`###` under `## Features`) | Primary catalog parent H2 (structural home — immutable) | Thematic cross-link scope (teaser bullets may name) | Representative catalog IDs (remain in home H2) |
|-----------------------------------|--------------------------------------------------------|-----------------------------------------------------|--------------------------------------------------|
| **Autonomous AI workflow** | **`Commands and workflow`** (phase/auto/orchestration lines) | `/intake`→`/release` lifecycle, `/auto`, pause/resume, decision gates (`DEC-xxxx`), team mode, backlog/bug drain (**US-0088**), **`AUTO_FLOW_MODE=full_autonomy`** + outer driver (**US-0092**) | `US-0092`, `US-0088`, `US-0044`, `US-0087`, `US-0023`, `US-0037`, `US-0069`, `US-0056`, `US-0070`, `BUG-0006` |
| **Quality & verification gates** | **`Commands and workflow`** (release/QA/UAT/gate lines) + **`Features`** (`/acceptance` catalog line only) | 3-layer quality chain, `/qa` / `/verify-work` / `/uat`, release gates, plan-verify, metadata guard, browser UAT (**US-0093**) | `US-0091`, `US-0093`, `US-0071`, `US-0039`, `US-0048`, `US-0014`, `US-0065`, `US-0066`, `US-0030` |
| **Distribution & install** | **`Features`** (distribution-tagged lines — primary) + scattered install/publish lines in **`Commands and workflow`** | npm / npx / Chocolatey / Homebrew, `its-magic --target` modes (missing/overwrite/upgrade/clean), lifecycle QA matrix, multi-target publish | `US-0009`, `US-0041`, `US-0008`, `US-0016`, `US-0054`, `US-0084`, `US-0007`, `BUG-0001`, `BUG-0003`, `BUG-0008`, `BUG-0009` |
| **Operator control & ergonomics** | **`Other useful capabilities`** (scratchpad/governance lines — primary) | scratchpad flags + `scratchpad.local.md`, guided intake packs, Caveman voice/compression (**US-0089** / **US-0090**), **`TOKEN_PROFILE`** cost profiles (**US-0080**), voice input, permissions/runtime connectivity | `US-0089`, `US-0090`, `US-0080`, `US-0013`, `US-0033`, `US-0035`, `US-0073`, `US-0010`, `US-0012`, `US-0011` |

**Catalog block inventory** (baseline **104/104 PASS**; parent H2 fixed):

| Catalog block marker | Parent H2 | ~item count | Pillar teaser may point here |
|---------------------|-----------|-------------|------------------------------|
| `<!-- readme-feature-coverage-catalog -->` (~line 27) | **`Features (what its-magic can do)`** | 20 | **P3** primary; **P2** (`/acceptance`) |
| same marker (~line 1139) | **`Commands and workflow`** | ~60 | **P1** + **P2** (shared home — teasers split by theme, ids stay) |
| same marker (~line 1339) | **`Other useful capabilities`** | ~24 | **P4** primary |

**Pillar bullet rules (execute)**:

1. **Id-free teasers** — pillar bullets cite commands/flags/outcomes by name; **must not** copy catalog `US-xxxx`/`BUG-xxxx` lines.
2. **Optional one-line cross-link** per pillar — plain-language pointer to the catalog block in its parent H2 (no anchor moves).
3. **Full-autonomy placement unchanged** — intro ¶3 (primary) + **P1** pillar bullet (secondary) + existing **`US-0092`** catalog line (tertiary).

#### Q2 — Intro word/line budget for `both`×`balanced` (`status=resolved`)

**Profile context**: default merged scratchpad resolves **`DOC_AUDIENCE_PROFILE=both`** × **`DOC_DETAIL_LEVEL=balanced`** (**DEC-0059** §6). `validate_doc_profile.py` enforces **H2 count** in root README for required **`USER_*`** keys — **`both`×`balanced` budget = 8 H2** (`doc_profile_lib.ROOT_BUDGET`). **US-0094** adds only **`###` H3** pillars under existing **`## Features`** — **no new `##` H2 literals** — so H2 budget is **unchanged**.

**Intro prose** (lines before first `## Features`) is **pre-H2** and **not** counted by `validate_doc_profile.py`. Budget is a **research/architecture lock** to mitigate risk **R3** (intro bloat).

| Constraint | Soft target | Hard max (execute MUST NOT exceed) |
|------------|-------------|-------------------------------------|
| Paragraph count | 3 (discovery lock) | 3 |
| Words per paragraph | 40–70 | 80 |
| Total intro words | 120–210 | 240 |
| Lines per paragraph (≤90 cols wrap) | 2–3 | 4 |
| Total intro lines (non-blank) | 8–10 | 12 |
| Optional DEV cross-link (`docs/developer/README.md`) | ≤25 words in ¶2 or ¶3 | 1 sentence only |

**Calibration**: discovery-locked draft (vision **Discovery Notes — US-0094**) measures **129 words** / **3 paragraphs** — within soft target. Execute should replace generic tagline (lines 5–9) with discovery copy ±10% word variance; **do not** add a 4th paragraph or bullet list in the intro zone.

**Validation at execute**: manual AC-1 review + `validate_doc_profile.py` (H2) + `check-user-visible-metadata.py`; no new scripted intro-length gate required for **US-0094** scope.

#### Q3 — Does **DEC-0074** need a §intro hierarchy companion? (`status=resolved`)

**Verdict: No — backlog/vision/discovery locks suffice; do not amend DEC-0074.**

| Factor | Assessment |
|--------|------------|
| **DEC-0074 scope** | Predicate, validator, section-affinity manifest, catalog id-preservation, release step **3f** — **static coverage** contract |
| **US-0094 scope** | Narrative **information architecture** (intro + pillar teasers) atop existing anchors |
| **Overlap** | Both require **no new USER_* H2 literals** and **no cross-H2 catalog moves** — already locked in **DEC-0074** §3–§4 and discovery |
| **Gap** | Intro/pillar tier semantics are **product positioning**, not coverage-detection rules |

**Architecture path**: document intro + pillar contract in **`docs/engineering/architecture.md`** **`# US-0094`**; optional companion **`DEC-xxxx`** only if architecture wants a formal IA decision — **not** a **DEC-0074** amendment. Execute cites discovery locks + **`R-0080`** Q1–Q4; re-run **`validate_readme_feature_coverage.py --report`** per **AC-4**.

#### Q4 — Diataxis tier boundary examples (`status=resolved`)

Mapping per **R-0054** / [Diátaxis](https://diataxis.fr/) — README tiers for **US-0094**:

| Diataxis mode | README region | US-0094 action | Boundary example (in vs out) |
|---------------|---------------|----------------|------------------------------|
| **Explanation** | 3 intro paragraphs **before** `## Features` | **NEW** — visionary promise, operator-as-dreamer, opt-in autonomy | **In**: “artifact-first memory lives in repo files.” **Out**: install command tables (belong in **Setup**) |
| **Summary / landing overview** | Four `###` pillars under `## Features` | **NEW** — 3–6 teaser bullets each | **In**: “Run `/auto` to drain your backlog (opt-in full autonomy).” **Out**: full `/auto` flag matrix (stays in **Commands and workflow** body + catalog) |
| **Reference** | Three `### Feature coverage catalog (US-0091)` blocks | **PRESERVED** — id-indexed 104-item index | **In**: `- \`/auto\` — … (\`US-0092\`).` **Out**: duplicating that line in pillar bullets |
| **How-to** | `## Setup`, `## How-to` | **PRESERVED** — procedural steps | **In**: `its-magic --target . --mode missing`. **Out**: repeating upgrade steps in **P3** pillar |
| **Tutorial** | `## Walkthrough examples` | **PRESERVED** — learning-oriented sequences | **In**: numbered phase walkthrough. **Out**: moving walkthrough steps into intro |
| **Reference (deep)** | `## Commands and workflow` body (below catalog), `## Developer and release deep-dive` | **PRESERVED** | **In**: slash-command reference prose. **Out**: relocating catalog ids to pillars |

**Anti-patterns (execute guards)**:

- Pillar tier must not become a second catalog (encyclopedic `US-xxxx` lists).
- Intro must not include install/CI procedure steps (violates Diataxis explanation vs how-to boundary).
- Full-autonomy value prop must not live only in **Developer and release deep-dive** (**AC-8**).

- **Linked (closure)**: **US-0094**, **US-0091**, **DEC-0074**, **DEC-0059**, **US-0092**, **DEC-0078**, **R-0054**
- **Confidence**: high (repo baseline 104/104 PASS + Diataxis external framing + discovery locks)
- **Next phase pointers (`/architecture`)**: author **`# US-0094`** section with intro/pillar contract, Q1 affinity table, Q2 budget literals, Diataxis tier map; **no DEC-0074 amendment**; optional **`DEC-xxxx`** only if architecture formalizes IA; execute rewrites intro + pillars without catalog id moves.

### Delivery closure trailer (2026-06-07T16:30:00Z, release, `orchestrator_run_id=auto-20260607-01`, `fresh_context_marker=release-S0083-US0094-release-20260607T163000Z-fresh`, `sprint_id=S0083`)

- **Status**: **delivered** — Q1–Q4 resolved at `/research`; architecture locked **`# US-0094`** (no companion DEC); sprint **S0083** executed, QA/verify-work/release **PASS**; **US-0094** **DONE**.
- **Resolution matrix outcome**: all discovery/research asks resolved at `/architecture` → `/sprint-plan` and verified through `/execute` → `/qa` → `/verify-work` → `/release`. README visionary intro (3 ¶, 136 words), four discovery-locked pillar **`###`** sections under **`## Features`**, three catalog blocks preserved in affinity homes, root ↔ **`template/README.md`** byte parity, **`coverage_missing=[]`**, **`coverage_total=104`**; UAT **10/10** PASS.
- **Evidence refs (US-0094 delivery)**: `sprints/S0083/release-findings.md` (PASS); `handoffs/releases/S0083-release-notes.md`; `sprints/S0083/uat.md` (10/10 PASS); `sprints/S0083/uat.json`; `sprints/S0083/qa-findings.md` (PASS); `sprints/S0083/summary.md`; `sprints/S0083/plan-verify.json` (PASS); `docs/engineering/architecture.md` `# US-0094`; `docs/product/backlog.md` `## US-0094` (DONE + `release_notes`); `docs/product/acceptance.md` (US-0094 row `[x]`); `handoffs/release_queue.md` (`S0083=released`); `README.md`, `template/README.md`; `docs/engineering/state.md` (Release checkpoint).
- **Portfolio drain closure signal**: with US-0094 closed, `docs/product/backlog.md` contains **zero** OPEN stories and **zero** OPEN bugs. Backlog-drain segment on `auto-20260607-01` closes here; next `/auto` invocation routes to **`/intake`** (`drain_terminated=true`; `drain_terminated_reason=no_open_stories`; `backlog_drain_stories_remaining_budget=0`).
- **Open R-xxxx anchors status (post-closure)**: R-0080 **delivered** (this trailer). Next research anchor allocation deferred to the next `/discovery`-phase subagent when a new work item is intaked.

## R-0081 — US-0095: Native in-Cursor `/auto` auto-chaining (no outer driver required)

- **Date**: 2026-06-07
- **Topic**: Native in-chat auto-chain for **`AUTO_FLOW_MODE=full_autonomy`** — phase + drain continuation without mandatory **`auto_outer_driver.py`**
- **Query**: How should `/auto` orchestrator continue across intersected lifecycle phases and backlog-drain segment boundaries **within one Cursor IDE invocation** while preserving spawn-only (**BUG-0006**), isolation (**US-0048**), strict proof (**US-0056**), and the **US-0092** hard stop matrix — with outer driver demoted to optional headless/CI fallback?
- **Status**: **delivered** (delivery closure trailer below; curator refresh **2026-06-07T23:45:00Z**)
- **Story**: **US-0095**
- **Problem**: **US-0092** / **DEC-0078** shipped **`scripts/auto_outer_driver.py`** as the multi-turn bridge for **`AUTO_FLOW_MODE=full_autonomy`** + backlog drain, but operators running `/auto` inside Cursor IDE still hit **`stop_reason=completed (segment exhausted)`** and are told to re-run `/auto` or the outer driver — contradicting hands-off drain expectations.
- **Linked**: **US-0092**, **DEC-0078**, **US-0088**, **US-0044**, **US-0087**, **BUG-0006**, **US-0069**, **US-0048**, **US-0056**, **DEC-0069**, **DEC-0038**, **R-0078**
- **Intake evidence**: `handoffs/intake_evidence/US-0095-intake-20260607.json`
- **Discovery extension**: `docs/product/backlog.md` `## US-0095` — `discovery_notes`; `docs/product/vision.md` — **Discovery Notes — US-0095**

### Research extension (2026-06-07T19:00:00Z, tech-lead, `orchestrator_run_id=auto-20260607-02`, `fresh_context_marker=tl-US0095-research-20260607T190000Z-fresh`)

- **External (EARLY_RESEARCH)**: [Cursor Subagents docs](https://cursor.com/docs/subagents) confirm the parent agent can delegate via the **Task tool** in **foreground** mode (blocks until subagent completes — sequential chain) or **background** mode (async fleet). Cursor 2.4+ ships default subagents; custom role subagents live under **`.cursor/agents/`**. [Cursor changelog (2026-04-24)](https://cursor.com/changelog/04-24-26) adds **`/multitask`** for async subagent fleets — orthogonal to lifecycle phase ordering (phases remain **strictly sequential** per **reference Step 5**). Community guidance ([forum layering/managing agents](https://forum.cursor.com/t/layering-managing-agents/158222)) notes **hooks** (`subagentStop` → `followup_message`) as an alternate continuation seam — **rejected as primary** for its-magic (non-portable across installs; spawn-only contract already maps cleanly to foreground Task loop). **Conclusion**: normative IDE continuation = orchestrator **foreground sequential Task spawn loop** within one `/auto` session; outer driver remains portable fallback when Task/subagent scheduling is unavailable (headless/CI).

#### Q1 — Native continuation mechanism (`status=resolved`)

| Option | Summary | Verdict |
|--------|---------|---------|
| A | **Foreground sequential Task/subagent loop** — orchestrator spawns phase-role subagent → awaits completion → runs US-0069 preflight + DEC-0038 post-check → schedules next spawn **in the same `/auto` orchestrator turn** | **Preferred** — matches Cursor subagent foreground mode; preserves **BUG-0006** (orchestrator schedules only). |
| B | **Background subagent + poll/`Await`** | **Rejected for phase chain** — nondeterministic boundary ordering; post-check may race artifact writes. |
| C | **Orchestrator in-band phase execution** | **Rejected** — **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** (**BUG-0006**). |
| D | **Outer-driver-only continuation** | **Rejected as primary IDE path** — remains fallback per Q4; **US-0095** closes the IDE gap **US-0092** left open. |
| E | **Cursor hooks (`subagentStop` follow-up)** | **Deferred / non-primary** — useful enhancement later; not required for v1 contract; architecture may note as optional operator overlay. |

**Normative pattern (architecture-locks exact prose tokens)**:

1. **Activation**: merged scratchpad **`AUTO_FLOW_MODE=full_autonomy`** (exact literal) **and** invocation context = Cursor IDE (default when `/auto` runs in Agent panel without `--invoke-cmd`).
2. **Chain driver**: orchestrator executes **reference Step 5** as a **`while` continuation loop**:
   - resolve next `phase_id` from intersected schedule **or** drain-advance target (Q2);
   - **US-0069** preflight (role matrix + capability gate);
   - **spawn fresh subagent** (`Task` tool, `subagent_type` = canonical role, `readonly` when phase is read-only);
   - **await** subagent completion (foreground);
   - verify isolation evidence + strict-proof tuple in `state.md`;
   - increment continuation counters (Q3);
   - branch stop matrix → continue spawn, drain-advance, block-retry, or hard stop.
3. **Forbidden**: orchestrator authors phase deliverables, merges subagent output as phase completion, or skips spawn for any scheduled `phase_id`.
4. **Turn-boundary semantics**: under native chain, **`stop_reason=completed (segment exhausted)`** is **not** a valid terminal state when (a) next intersected phase exists, (b) drain policy selects another OPEN item, or (c) relaxable stop is within retry budget — orchestrator **must** schedule continuation instead of emitting operator wait instructions.
5. **Fail-closed when native chain unavailable** (no Task tool, spawn denied, depth limit): stop with candidate reason **`NATIVE_CHAIN_UNAVAILABLE`** + remediation listing headless fallback (`auto_outer_driver.py`) — **not** mandatory for IDE when chain is available.

**Risks**: **R1** Cursor depth/tool-policy blocks nested spawns → document bounds + **`NATIVE_CHAIN_UNAVAILABLE`** fail-closed. **R3** spawn-only violation if orchestrator summarizes phase work in-band → contract tests + **US-0069** post-checks unchanged.

#### Q2 — IDE drain-advance algorithm (`status=resolved`)

Deterministic **drain-advance-without-pause** when **`full_autonomy`** + (**`AUTO_BACKLOG_DRAIN=1`** or bug-queue per **US-0087**). Composes **US-0044**, **US-0087**, **DEC-0069**, **reference Step 5** item 5.

**Trigger** (all must hold):

- Segment terminal phase completed: `stop_phase=refresh-context` (or story terminal boundary when `refresh-context` omitted from plan).
- `stop_reason=completed` (not hard gate).
- Drain enabled: `AUTO_BACKLOG_DRAIN=1` (story) **or** bug-queue active with resolved target (**US-0087** mutex unchanged).
- `backlog_drain_stories_remaining_budget > 0` (story drain) or bug-queue budget not exhausted.

**Algorithm** (orchestrator scheduling — not phase-role work):

```
1. READ latest phase-boundary block in docs/engineering/state.md
   (stop_phase, stop_reason, story_id, sprint_id, orchestrator_run_id,
    backlog_drain_stories_remaining_budget, bug_queue_remaining).
2. ASSERT DEC-0069 pairing: completed phase refreshed resume_brief + state.md
   (stale → fail-closed RESUME_BRIEF_STALE; no drain advance).
3. IF story drain:
     a. DECREMENT budget counter in state boundary (initial = AUTO_BACKLOG_MAX_STORIES
        at materialization; minus segments completed this run).
     b. SELECT next OPEN story from docs/product/backlog.md per AUTO_STORY_SELECTION
        (priority_then_backlog_order — unchanged).
     c. IF no eligible OPEN story → set drain_terminated=true,
        drain_terminated_reason=no_open_stories; STOP chain (completed).
     d. IF budget == 0 → stop_reason BACKLOG_MAX_STORIES_REACHED (hard).
   ELSE IF bug-queue (US-0087):
     a. SELECT next OPEN BUG-#### ascending; respect AUTO_BUG_MAX_ITEMS.
     b. IF queue empty → AUTO_BUG_QUEUE_EMPTY (hard).
4. RELOAD merged scratchpad; MATERIALIZE resolved_phase_plan (US-0070);
   INTERSECT with segment entry phase (typically discovery or intake if skipped).
5. PREPEND handoffs/resume_brief.md top pointer:
   story_id|bug_id, intended_resume_phase=<first scheduled phase>,
   orchestrator_run_id=<unchanged>, backlog_drain_active, budget counters.
6. APPEND state.md materialization breadcrumb for new segment.
7. IMMEDIATELY spawn first phase subagent (goto Q1 chain step 2) — no operator
   re-/auto, no outer-driver instruction under full_autonomy IDE path.
```

**Scheduler mutex** (**US-0087**): unchanged — `AUTO_SCHEDULER_CONFLICT` when both drain flags set without `bug-target=` argv.

**Risks**: **R4** stale `resume_brief` between advances → **DEC-0069** fail-closed unchanged. **R2** docs claim drain while behavior stops → contract tests (Q6).

#### Q3 — Cap + ledger interaction (`status=resolved`)

**Principle**: IDE native chain and outer driver **share one accounting model** — same scratchpad keys, same ledger path, same counter semantics — so caps cannot desync between paths (**discovery R6**).

| Cap | Scope (unified) | IDE native chain behavior | Outer driver behavior |
|-----|-----------------|---------------------------|------------------------|
| **`AUTO_LOOP_MAX_CYCLES`** | **Continuation cycles per `orchestrator_run_id`** — each **phase spawn boundary** after materialization counts **1**; each **drain segment advance** counts **1**; inner `execute`↔`qa` remediation cycles count toward **`implementation_loop_index`** not outer cycle when `AUTO_IMPLEMENTATION_LOOP=1` | Orchestrator increments `outer_cycle_index` in memory + state breadcrumb before each spawn/advance; at cap → `stop_reason=loop_max` (hard) | Same — `scripts/auto_outer_driver.py` already increments `outer_cycle` per hook re-invocation (**R-0078** Q4) |
| **`AUTO_IMPLEMENTATION_LOOP`** | Inner **`execute`→`qa`→`verify-work`** remediation | When `1`, UAT/QA fail schedules remediation spawns within same story segment; each full cycle increments `implementation_loop_index`; hard stop when `implementation_loop_index >= AUTO_LOOP_MAX_CYCLES` | Unchanged |
| **`AUTO_BLOCK_RETRY_MAX`** | Per **`(story_id, stop_reason)`** recoverable retries | Before scheduling recoverable retry, orchestrator **reads** ledger; if count ≥ max → `BLOCK_RETRY_CAP_EXHAUSTED` (hard). On retry scheduled, **append** ledger row with `remediation_action=phase_respawn` (not `outer_reinvoke`) | Existing `outer_reinvoke` rows preserved; same ledger file |
| **`AUTO_BACKLOG_MAX_STORIES`** | Drain breadth per run | Decrement `backlog_drain_stories_remaining_budget` in `state.md` at each segment advance; hard stop at **0** with `BACKLOG_MAX_STORIES_REACHED` | Exit **4** (unchanged) |

**Ledger path** (unchanged): append-only **`handoffs/auto_block_retry/<orchestrator_run_id>.jsonl`**.

**New `remediation_action` values** (architecture ratifies): `phase_respawn`, `native_chain_continue`, `drain_advance` — alongside existing `outer_reinvoke`.

**Ordering** (unchanged from **R-0078** / **DEC-0078**): check **`AUTO_LOOP_MAX_CYCLES`** first; then **`AUTO_IMPLEMENTATION_LOOP`** + **`AUTO_BLOCK_RETRY_MAX`** before recoverable retry; unrecoverable classes bypass ledger.

**State breadcrumb fields** (add at execute): `native_chain_active=true|false`, `outer_cycle_index`, `implementation_loop_index` on each phase boundary when `full_autonomy`.

#### Q4 — Outer driver fallback boundary matrix (`status=resolved`)

| Context | Native in-chat chain | Outer driver (`auto_outer_driver.py`) | Operator messaging |
|---------|---------------------|----------------------------------------|-------------------|
| **Cursor IDE + `full_autonomy`** | **Primary** — default hands-off recipe | **Optional fallback** — headless escape hatch, troubleshooting, Task-tool denial | **Must not** state outer driver is **required** for drain |
| **Headless / CI / scripted runner** | **Unavailable** (no Task tool) | **Recommended** — `python scripts/auto_outer_driver.py --repo . [--invoke-cmd …]` | Runbook labels **headless primary** |
| **`--invoke-cmd` / external agent runner** | N/A | **Required** bridge | Document in runbook § US-0092 + new § US-0095 |
| **`manual` / `auto_until_decision`** | **Not required** — single-phase or gate-stop behavior unchanged | Optional | No change |
| **Native chain fail-closed (`NATIVE_CHAIN_UNAVAILABLE`)** | Stops | **Suggested fallback** (one line, non-mandatory tone) | Non-suppressible error |
| **Relaxable transient stop exhausted** | Stops in-chat | Operator **may** re-run outer driver | Notify on cap |

**README / runbook demotion wording** (execute applies):

- Replace mandatory phrasing: ~~"run the shipped outer driver once"~~ as **sole** full-autonomy recipe → **"run `/auto` once in Cursor"** (primary); outer driver **"for headless/CI or when native chain is unavailable"**.
- Preserve **US-0092** autonomy headline — demote, do not delete.
- **US-0094** intro ¶3 touch: within US-0095 execute scope per discovery.

**Risks**: **R5** dual-path confusion → runbook table (above) + explicit **Primary vs fallback** labels.

#### Q5 — Operator messaging + `AUTO_QUIET` (`status=resolved`)

**Invariant**: Under **`AUTO_FLOW_MODE=full_autonomy`** IDE native chain, segment and phase handoffs **must not** emit **mandatory wait** instructions (`run auto_outer_driver.py`, `re-run /auto`, `segment exhausted — operator action required`) when continuation is schedulable.

| Event | `AUTO_QUIET=0` | `AUTO_QUIET=1` |
|-------|----------------|----------------|
| Routine phase PASS | May notify | **Suppress** |
| Native chain continuing to next phase | Compact breadcrumb OK | **Suppress** (optional one-line `chain_continuing` also suppressible) |
| Drain advance to next story/bug | Segment handoff notify OK | **Suppress** routine segment prose; **no** outer-driver instruction |
| `decision_gate`, errors, `loop_max`, `blocked`, missing critical input, pause | **Always** (non-suppressible) | **Always** |
| `BACKLOG_MAX_STORIES_REACHED`, `BLOCK_RETRY_CAP_EXHAUSTED` | **Always** | **Always** |
| `NATIVE_CHAIN_UNAVAILABLE` | **Always** + fallback hint | **Always** |

**Forbidden grep patterns** (active `auto.md` + reference `full_autonomy` IDE sections after execute):

- `run the outer driver` (as mandatory IDE step)
- `re-run /auto` (between segments when drain active + native chain available)
- `segment exhausted` (as terminal under `full_autonomy` when continuation pending)
- `python scripts/auto_outer_driver.py` without **optional** / **fallback** qualifier in IDE-primary prose

**Orthogonality**: **`AUTO_QUIET`** unchanged vs **`TOKEN_PROFILE`** (**DEC-0035** / **US-0088**).

#### Q6 — Contract-test + template parity inventory (`status=resolved`)

**Pytest markers** (add class `test_us0095_*` — run `pytest -k us0095 tests/auto_command_contract_test.py`):

| Test | AC | Assertions |
|------|-----|------------|
| `test_us0095_native_in_chat_auto_chain_markers` | AC-1 | `auto.md` + reference contain **`Native in-chat auto-chain`**, **`foreground sequential`**, **`same /auto orchestrator session`**, **`NATIVE_CHAIN_UNAVAILABLE`** (or architecture-locked synonym) |
| `test_us0095_ide_drain_advance_without_outer_driver` | AC-2 | Normative **`drain-advance-without-pause`** + **`immediately`** + **`without operator re-`/auto`**` in IDE-primary section; **no** mandatory outer-driver phrase in that section |
| `test_us0095_outer_driver_fallback_not_mandatory_ide` | AC-5 | README + runbook: **`optional`** / **`fallback`** adjacent to outer-driver mentions in full-autonomy IDE recipe |
| `test_us0095_spawn_only_regression` | AC-3 | Reuse **BUG-0006** forbidden orchestrator-phase strings; add **`native chain`** section does not introduce forbidden patterns |
| `test_us0095_auto_quiet_no_outer_driver_mandatory` | AC-6 | Reference documents quiet suppression + non-suppressible list includes cap/gate errors; negative grep for mandatory outer-driver between segments |
| `test_us0095_resume_brief_pairing_markers` | AC-7 | `auto.md` or reference cites **DEC-0069** refresh before in-chat continuation |
| `test_us0095_template_parity_auto_surfaces` | AC-9 | Byte or literal parity active ↔ `template/` for touched `auto.md`, reference excerpts, runbook subsection |

**Touch inventory** (execute):

| # | Surface | Parity |
|---|---------|--------|
| 1 | **`.cursor/commands/auto.md`** | active + **`template/.cursor/commands/auto.md`** — new § **Native in-chat auto-chain (US-0095)**; demote outer-driver equivalence to fallback in IDE path |
| 2 | **`docs/engineering/auto-orchestration-reference.md`** | active + template — Step 5 amendment: IDE primary path; Option B equivalence scoped to fallback |
| 3 | **`docs/engineering/runbook.md`** | active + template — new **`### Native in-chat auto-chain (US-0095)`** + demote **`### Full-autonomy outer driver (US-0092)`** to fallback |
| 4 | **`README.md`**, **`template/README.md`** | intro ¶3 + pillar bullet demotion (**US-0094** follow-on) |
| 5 | **`handoffs/resume_brief.md`** pairing contract | documented in reference (no schema change) |
| 6 | **`tests/auto_command_contract_test.py`** | markers above |
| 7 | **`docs/engineering/architecture.md`** | **`# US-0095`** (architecture phase) |
| 8 | Scratchpad comments | only if new keys required (research: **none** — reuse existing caps) |

- **Confidence**: high on contract shape (repo inventory + Cursor subagent docs); runtime depth limits remain operator-verified at UAT.
- **Next phase pointers (`/architecture`)**: lock companion **`DEC-xxxx`** (if needed beyond discovery locks), **`# US-0095`**, exact reason codes (`NATIVE_CHAIN_UNAVAILABLE`), state breadcrumb fields, runbook primary/fallback table, contract-test literal strings, README demotion copy.

### Delivery closure trailer (2026-06-07T23:30:00Z, release, `orchestrator_run_id=auto-20260607-02`, `fresh_context_marker=release-S0084-US0095-release-20260607T233000Z-fresh`, `sprint_id=S0084`)

- **Status**: **delivered** — Q1–Q6 resolved at `/research`; architecture locked **`DEC-0080`** + **`# US-0095`**; sprint **S0084** executed, QA/verify-work/release **PASS**; **US-0095** **DONE**.
- **Resolution matrix outcome**: all discovery/research asks resolved at `/architecture` → `/sprint-plan` and verified through `/execute` → `/qa` → `/verify-work` → `/release`. Native in-chat auto-chain contract shipped in **`auto.md`** + reference; 7-step IDE drain-advance-without-pause; **`NATIVE_CHAIN_UNAVAILABLE`** fail-closed; **`AUTO_QUIET`** forbidden mandatory outer-driver/re-`/auto` patterns; outer driver demoted to optional IDE fallback / headless primary; seven **`test_us0095_*`** contract subtests green; template parity **`--scope=us-0095`**; UAT **10/10** PASS.
- **Evidence refs (US-0095 delivery)**: `sprints/S0084/release-findings.md` (PASS); `handoffs/releases/S0084-release-notes.md`; `sprints/S0084/uat.md` (10/10 PASS); `sprints/S0084/uat.json`; `sprints/S0084/qa-findings.md` (PASS); `sprints/S0084/summary.md`; `sprints/S0084/plan-verify.json` (PASS); `decisions/DEC-0080.md`; `docs/engineering/architecture.md` `# US-0095`; `docs/product/backlog.md` `## US-0095` (DONE + `release_notes`); `docs/product/acceptance.md` (US-0095 row `[x]`); `handoffs/release_queue.md` (`S0084=released`); `tests/auto_command_contract_test.py` (`test_us0095_*`); `docs/engineering/state.md` (Release checkpoint).
- **Portfolio drain closure signal**: with US-0095 closed, `docs/product/backlog.md` contains **zero** OPEN stories and **zero** OPEN bugs. Backlog-drain segment on `auto-20260607-02` closes at **`/refresh-context`**; next `/auto` invocation routes to **`/intake`** (`drain_terminated=true`; `drain_terminated_reason=no_open_stories`; `backlog_drain_stories_remaining_budget=9` unused of initial **10**).
- **Open R-xxxx anchors status (post-closure)**: R-0081 **delivered** (this trailer). Next research anchor allocation deferred to the next `/discovery`-phase subagent when a new work item is intaked.

## R-0082 — US-0096: Delivery modes (ultra_lean + mega_quick) with layered memory

- **Date**: 2026-06-11
- **Topic**: Opt-in **`DELIVERY_MODE`** lifecycle-shape axis — token reduction via fewer spawns and layered memory without amnesia
- **Query**: How should **`ultra_lean`** (4 macro-phases + **`pack.json`**) and **`mega_quick`** (enhanced **`/quick`**) compose with **DEC-0052** reinstatement, **US-0080** token metrics, and institutional memory (vision/architecture/decisions narrow-read)?
- **Status**: **resolved for `/research`** (Q1–Q7 closed — architecture next)
- **Story**: **US-0096**
- **Problem**: Default eleven-phase lifecycle + **DEC-0052** non-skippable reinstatement limits token savings from **`TOKEN_PROFILE=lean`** alone; operators need mode-scoped lifecycle shapes that preserve code quality and document changes for later runs.
- **Linked**: **US-0080**, **DEC-0062**, **US-0053**, **US-0070**, **DEC-0052**, **US-0001**, **US-0092**, **US-0095**, **DEC-0072**
- **Intake evidence**: `handoffs/intake_evidence/US-0096-intake-20260611.json`
- **Discovery extension**: **`/discovery`** **PASS** — **`2026-06-13T02:30:00Z`**, PO, `orchestrator_run_id=auto-20260612-01`, `fresh_context_marker=po-US0096-discovery-20260613T023000Z-fresh` (see below)
- **Research asks (intake-locked)**:
  1. **`pack.json`** canonical path and schema vs existing sprint folder compatibility
  2. Mode-scoped **DEC-0052** reinstatement algorithm
  3. **`active-context.md`** rollover contract vs **DEC-0054** triad hot-surface
  4. **`mega_quick`** eligibility rules and backlog **`delivery_mode`** row schema
  5. Universal wins (Tranche A) default threshold changes vs operator override
  6. **DEC-0062** run-class object extension with **`delivery_mode`** field
  7. Contract-test marker inventory + template parity scope
- **Next phase pointers**: **`/discovery`** (PO) → **`/research`** (TL) → **`/architecture`** (TL, **`DEC-xxxx`**)

### Discovery extension (2026-06-13T02:30:00Z, PO, `orchestrator_run_id=auto-20260612-01`, `fresh_context_marker=po-US0096-discovery-20260613T023000Z-fresh`)

- **`/discovery`** **PASS** — product framing and mode contracts locked for **`/research`** deep-dive.
- **Q1 (`pack.json` path/schema)**: canonical path **`work/US-xxxx/pack.json`** (discovery-locked); research must lock JSON schema fields (`story_id`, `delivery_mode`, `ac[]`, `tasks[]`, `refs[]`, `deltas[]`, `status`, `memory_layer`) and coexistence with **`sprints/Sxxxx/`** when **`standard`** mode used on same repo — no destructive overlap.
- **Q2 (mode-scoped DEC-0052)**: resolver reads **`DELIVERY_MODE`** **before** reinstatement; **`standard`** only gets today's reinstatement; **`ultra_lean`** materializes `[spec, plan, build+verify, ship]`; **`mega_quick`** materializes `[quick]` (+ conditional retry spawn); breadcrumbs: **`delivery_mode`**, **`resolved_phase_plan`**, **`memory_layer`**.
- **Q3 (`active-context.md` vs DEC-0054)**: hot index at **`handoffs/active-context.md`** (~30–80 lines); research must lock rollover trigger (story segment close vs line cap), relationship to triad surfaces (**`po_to_tl.md`**, **`state.md`**, **`architecture.md`**) — **`active-context`** is **warm index**, not fourth triad member unless architecture decides otherwise.
- **Q4 (`mega_quick` eligibility)**: discovery signals — scratchpad mode, backlog **`delivery_mode: mega_quick`**, argv **`delivery-mode=`**, small-scope heuristics; research must lock fail-closed reason codes for ineligible stories (cross-cutting AC, bug segments, architecture-first stories).
- **Q5 (Tranche A universal wins)**: always-on narrow-read in all phase commands, tighter hot-surface defaults, delta handoff guidance, touch-graph reads — research quantifies default threshold deltas vs operator **`LEAN_*`** overrides.
- **Q6 (DEC-0062 extension)**: append **`delivery_mode`** to **`run_class_hash`** object; **`handoffs/token_cost_runs/<orchestrator_run_id>.md`** rows must include mode for AC-12 comparability.
- **Q7 (contract tests + parity)**: research inventories **`test_us0096_*`** marker names, **`pack.json`** schema validator sketch, **`check_intake_template_parity.py --scope=us-0096`** manifest rows, phase-command literal updates across active + **`template/`**.
- **Composition note**: **`DELIVERY_MODE`** unset — **orthogonal** to **DEC-0080** native chain (**R-0083** Q5 confirmed); lean modes reduce per-story spawns, not drain-advance semantics.
- **Status**: **resolved for `/research`** — discovery satisfied; research extension below closes Q1–Q7.

### Research extension (2026-06-13T03:00:00Z, tech-lead, `orchestrator_run_id=auto-20260612-01`, `fresh_context_marker=tl-US0096-research-20260613T030000Z-fresh`)

- **External (EARLY_RESEARCH)**:
  - [The Missing Memory Hierarchy (arxiv 2603.09023)](https://arxiv.org/abs/2603.09023v1) — L1 working window + demand-paged L2/L3/L4; **hit-rate** over single-window capacity; aligns with **`active-context`** (L1 index) + **`pack.json`** (L2 warm) + section-scoped cold reads.
  - [Agent Memory Techniques — hierarchical memory layers](https://github.com/NirDiamant/Agent_Memory_Techniques/blob/main/all_techniques/13_hierarchical_memory_layers/hierarchical_memory_layers.ipynb) — L1/L2/L3 promotion/demotion; **cascading retrieval** (search hot → warm → cold on miss).
  - [Memory Tiering HOT/WARM/COLD (clawRxiv 2603.00037)](https://clawrxiv.io/abs/2603.00037) — explicit tier targets (HOT **<500 tokens**, WARM **1000–3000**); prune-on-complete to warm/cold — maps to **`active-context`** line budget + **`pack.json`** story close.
  - **Conclusion**: industry pattern validates discovery locks; its-magic implementation stays **file-based** (no vector DB) — simpler, auditable, template-parity friendly.

#### Q1 — `pack.json` canonical schema + sprint coexistence (`status=resolved`)

**Canonical path**: **`work/<story_id>/pack.json`** (e.g. **`work/US-0096/pack.json`**). One warm pack per active story segment; created at first **`ultra_lean`** spawn (**`spec`**) or lazily on mode switch.

**Schema v1** (JSON object — validator: **`scripts/pack_json_validate.py`**, reason codes **`PACK_*`**):

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `schema_version` | string | yes | Literal **`"1"`** |
| `story_id` | string | yes | **`US-xxxx`** |
| `delivery_mode` | string | yes | **`ultra_lean`** when pack active |
| `status` | string | yes | **`OPEN`** \| **`IN_PROGRESS`** \| **`DONE`** |
| `ac` | array | yes | Objects: `{ "id": "AC-n", "text": string, "met": bool }` |
| `tasks` | array | yes | Objects: `{ "id": "T-nnn", "title": string, "status": "pending\|done" }` |
| `refs` | array | yes | Objects: `{ "kind": "vision\|architecture\|decisions\|handoff\|sprint", "path": string, "section"?: string }` |
| `deltas` | array | yes | Append-only: `{ "utc": ISO8601, "phase": string, "summary": string, "paths": string[] }` |
| `memory_layer` | string | yes | Literal **`"pack"`** |
| `sprint_id` | string \| null | no | Set when **`standard`** sprint folder also exists — cross-link only |
| `orchestrator_run_id` | string | no | Last writer run id |

**Coexistence with `sprints/Sxxxx/`** (no destructive overlap):

| Mode | Primary task surface | Sprint folder |
|------|---------------------|---------------|
| **`standard`** | **`sprints/Sxxxx/tasks.md`** | **Authoritative** — unchanged |
| **`ultra_lean`** | **`work/US-xxxx/pack.json`** `tasks[]` | **Optional** — created only if story later switches to **`standard`** or release needs **`Sxxxx`** traceability; pack **`sprint_id`** links when both exist |
| **`mega_quick`** | **`sprints/quick/Qxxxx/task.json`** | **Separate namespace** — no **`work/`** pack |

**Rules**: **`work/`** never deletes or mutates **`sprints/`**; mode switch **`ultra_lean` → `standard`** mid-story fails closed (**`DELIVERY_MODE_SWITCH_MID_STORY`**) unless architecture documents explicit migration (out of scope — operator completes segment in one mode).

#### Q2 — Mode-scoped **DEC-0052** reinstatement algorithm (`status=resolved`)

**Integration point**: **`/auto`** plan materialization — **step 0** before existing **DEC-0052** pipeline (**`R-0049`** steps 1–6).

**Pseudocode**:

```
delivery_mode := resolve_delivery_mode(argv, backlog_row, merged_scratchpad)
  // precedence: argv delivery-mode= > backlog delivery_mode > DELIVERY_MODE > "standard"

if delivery_mode == "mega_quick":
  if not mega_quick_eligible(story, backlog, scratchpad):
    FAIL DELIVERY_MODE_INELIGIBLE + reason_code
  plan := ["quick"]
  reinstatement := "none"
  memory_layer := "quick"
  GOTO persist_breadcrumbs

if delivery_mode == "ultra_lean":
  plan := ["spec", "plan", "build+verify", "ship"]
  reinstatement := "none"   // macro-phases embed qa+verify inside build+verify
  memory_layer := "pack"
  GOTO persist_breadcrumbs

// delivery_mode == "standard" (unset counts as standard)
candidate := dec0052_expand_policy(scratchpad)     // AUTO_PHASE_* — unchanged
plan := dec0052_apply_reinstatement(candidate)     // full default non-skippable set
plan := dec0052_intersect_start_from(plan, argv)
reinstatement := "dec0052_default"
memory_layer := "standard"
persist_breadcrumbs(delivery_mode, plan, reinstatement, memory_layer)
```

**Macro-phase → role mapping** ( **`ultra_lean`** only):

| Macro | Canonical phases merged | Default role |
|-------|------------------------|--------------|
| **`spec`** | `intake` + `discovery` | **po** |
| **`plan`** | `research` + `architecture` + `sprint-plan` | **tech-lead** |
| **`build+verify`** | `execute` + `qa` + `verify-work` (+ **`AUTO_IMPLEMENTATION_LOOP`**) | **dev** / **qa** per sub-step |
| **`ship`** | `release` + `refresh-context` | **release** / **curator** |

**Breadcrumbs** ( **`state.md`** + **`resume_brief.md`** ): **`delivery_mode`**, **`resolved_phase_plan`**, **`reinstatement_mode`**, **`memory_layer`**.

**Orthogonality**: **`AUTO_PHASE_EXCLUDE`** / **`INCLUDE`** / **`PROFILE`** apply **only** when **`delivery_mode=standard`**; non-standard mode + non-default **`AUTO_PHASE_*`** → **`PHASE_POLICY_CONFLICT`** (fail closed).

#### Q3 — `active-context.md` vs **DEC-0054** triad (`status=resolved`)

**Verdict**: **`handoffs/active-context.md`** is a **warm spawn index** — **not** a fourth triad member. **DEC-0054** triad unchanged: **`state.md`**, **`handoffs/po_to_tl.md`**, **`docs/engineering/architecture.md`**.

| Surface | Tier | Owner phase | Line budget |
|---------|------|-------------|-------------|
| **`active-context.md`** | Hot index | **`spec`/`plan`/`build+verify`/`ship`** writers; rollover on **`refresh-context`** | Target **30–80** lines; hard cap **`LEAN_STATE_INDEX_ROWS`** (default **80**) |
| **`pack.json`** | Warm | All **`ultra_lean`** spawns read; append **`deltas[]`** | File size soft cap **16 KiB** (architecture) |
| Vision/arch/decisions sections | Cold | Section-scoped narrow-read; cap **`LEAN_COLD_READ_MAX_SECTIONS`** (default **4**) | Per-spawn |

**Rollover contract**:

1. **Trigger A** — story segment **`refresh-context`** complete → archive to **`handoffs/archive/active-context-<story_id>-<utc>.md`**, rewrite hot file with next-story stub or empty template.
2. **Trigger B** — line count **>** **`LEAN_STATE_INDEX_ROWS`** before segment close → same archive path (fail-closed **`ACTIVE_CONTEXT_OVERSIZE`** if spawn proceeds without rollover when **`LEAN_MEMORY_WRITE=1`**).
3. **Triad interaction** — **`enforce-triad-hot-surface.py`** does **not** scan **`active-context.md`**; no **`STATE_ARCHIVE_REQUIRED`** coupling. **`po_to_tl.md`** in **`ultra_lean`** may shrink to orchestrator handoff stub; full detail lives in **`pack.json`** + **`active-context`**.

**Content template** (hot index rows): `story_id`, `delivery_mode`, `read_before_code[]` (path + optional section anchor), `last_delta_utc`, `open_risks[]` (max 3 bullets).

#### Q4 — `mega_quick` eligibility + backlog row schema (`status=resolved`)

**Routing**: **`DELIVERY_MODE=mega_quick`** OR backlog row **`delivery_mode: mega_quick`** (when **`AUTO_DELIVERY_ROUTING=backlog_then_scratchpad`**) → **`/auto`** materializes **`["quick"]`** only (+ conditional **+1** spawn on test failure inside **`/quick`**).

**Eligibility table** (fail-closed — all must pass):

| # | Rule | Pass | Fail reason code |
|---|------|------|------------------|
| E1 | Work item kind | **`story`** only | **`MEGA_QUICK_BUG_SEGMENT`** |
| E2 | Acceptance count | **`ac` ≤ 3** (count backlog AC bullets) | **`MEGA_QUICK_AC_TOO_BROAD`** |
| E3 | Cross-cutting flags | No **`DEC-xxxx`** companion required in discovery/arch notes | **`MEGA_QUICK_ARCHITECTURE_REQUIRED`** |
| E4 | Existing sprint | No active **`sprints/Sxxxx/`** for story | **`MEGA_QUICK_SPRINT_EXISTS`** |
| E5 | Story override | Row **`delivery_mode`** not **`standard`** when routing enabled | **`MEGA_QUICK_STORY_OVERRIDE`** |
| E6 | Component scope | **`COMPONENT_SCOPE_MODE=0`** OR single component in **`TARGET_COMPONENTS`** | **`MEGA_QUICK_MULTI_COMPONENT`** |
| E7 | Security / publish | No elevated gates beyond default **`/quick`** stop conditions | **`MEGA_QUICK_GATE_ESCALATION`** |

**Backlog row optional field** (Tranche D — **`AC-8`**):

```yaml
delivery_mode: mega_quick   # optional; values: standard | ultra_lean | mega_quick
```

**Precedence**: argv **`delivery-mode=`** → story row → scratchpad **`DELIVERY_MODE`** → **`standard`**.

**Artifacts**: **`sprints/quick/Qxxxx/task.json`** (AC mirror + **`acceptance_met`**) + **`summary.md`** + one **`state.md`** index row; status flip requires **`acceptance_met: true`** + green tests (**AC-6**).

#### Q5 — Tranche A universal wins vs **`LEAN_*`** overrides (`status=resolved`)

**Principle**: Tranche A ships **always-on** — no **`DELIVERY_MODE`** toggle. Operator **`LEAN_*`** and existing **`*_HOT_MAX_*`** keys **override** tighter defaults (manual-override precedence per scratchpad comment block).

**Proposed default threshold deltas** (architecture locks exact literals in **`DEC-xxxx`**):

| Key | Current default | Tranche A default | Δ | Override key |
|-----|-----------------|-------------------|---|--------------|
| **`STATE_HOT_MAX_LINES`** | 1200 | **1000** | −17% | explicit value wins |
| **`PO_TO_TL_HOT_MAX_LINES`** | 800 | **650** | −19% | explicit value wins |
| **`ARCH_HOT_MAX_LINES`** | 3500 | **3000** | −14% | explicit value wins |
| **`LEAN_COLD_READ_MAX_SECTIONS`** | (unset) | **4** | new | **`LEAN_COLD_READ_MAX_SECTIONS`** |
| **`LEAN_STATE_INDEX_ROWS`** | (unset) | **80** | new | **`LEAN_STATE_INDEX_ROWS`** |

**Always-on behaviors** (no new scratchpad gate):

1. **Narrow-read in all phase commands** — each command **`Inputs`** cites **`docs/engineering/phase-context.md`** + story section anchor; forbid full-file reads of vision/architecture/decisions when section heading exists (**extends **US-0053****).
2. **Delta handoffs** — phase commands append **delta paragraphs** only (no full rewrites of prior handoff bodies).
3. **Touch-graph reads** — runbook documents: read **`codebase-map.md`** component slice + touched paths only before execute (**AC-3** measurable on **`run_class_hash`-matched **`standard`** runs**).
4. **Token target (Tranche A alone)**: **≥10%** **`cache_read_tokens`** reduction on matched **`standard`** runs vs pre-**US-0096** baseline (conservative vs **50%** full-story **`ultra_lean`** claim).

**`LEAN_MEMORY_READ` / `LEAN_MEMORY_WRITE`**: default **`1`** when pack/active-context paths exist; **`0`** fails closed on **`ultra_lean`** spawn (**`LEAN_MEMORY_DISABLED`**).

#### Q6 — **DEC-0062** `run_class_hash` extension (`status=resolved`)

**Amendment** (companion **`DEC-xxxx`** at architecture — extends **DEC-0062** §2):

Add required key to run-class object:

- **`delivery_mode`**: **`standard`** \| **`ultra_lean`** \| **`mega_quick`** (merged scratchpad + argv resolution at plan materialization)

**Serialization**: existing **`canonical_json_dumps`** + **`compute_run_class_hash`** — append key in **sorted** order; all pre-**US-0096** baselines rebaseline with **`delivery_mode=standard`**.

**Evidence rows** (**`handoffs/token_cost_runs/<orchestrator_run_id>.md`**): MUST include **`delivery_mode`** column + hash object echo.

**Comparability rules**:

| Comparison | Valid? |
|------------|--------|
| **`standard`** vs **`standard`**, same other keys | yes — AC-2 / AC-3 |
| **`ultra_lean`** vs **`standard`**, same story | **no** — **`TOKEN_COST_RUN_CLASS_MISMATCH`** (different lifecycle) |
| **`ultra_lean`** vs **`ultra_lean`**, same story | yes — AC-12 lean trajectory |
| **`mega_quick`** vs **`mega_quick`**, eligible story class | yes — target **≥70%** reduction vs matched **`standard`** baseline (operator-run acceptable) |

**Orthogonality preserved**: **`TOKEN_PROFILE`**, **`CAVEMAN_MODE`**, **`AUTO_QUIET`** remain independent dimensions in hash object (unchanged keys).

#### Q7 — Contract-test inventory + template parity manifest (`status=resolved`)

**Proposed `test_us0096_*` markers** (architecture locks exact names in **`tests/auto_command_contract_test.py`**):

| Test | Intent |
|------|--------|
| **`test_us0096_delivery_mode_scratchpad_keys`** | Active + template scratchpad document **`DELIVERY_MODE`**, **`LEAN_*`**, **`AUTO_DELIVERY_ROUTING`**, non-substitution paragraph |
| **`test_us0096_standard_mode_baseline_markers_preserved`** | **`DELIVERY_MODE=standard`** / unset — **`test_us0095_*`** + **`test_bug0012_*`** markers still pass (AC-2 regression guard) |
| **`test_us0096_mode_scoped_reinstatement_literals`** | **`auto.md`** — reinstatement applies **only** when **`delivery_mode=standard`** |
| **`test_us0096_ultra_lean_macro_phase_literals`** | Four macro-phases + role table + **`AUTO_IMPLEMENTATION_LOOP`** inside **`build+verify`** |
| **`test_us0096_mega_quick_routing_literals`** | **`/auto`** → **`/quick`** path + eligibility fail-closed codes |
| **`test_us0096_pack_json_schema_contract`** | Schema fields + validator script presence + **`work/US-xxxx/pack.json`** path literal |
| **`test_us0096_active_context_contract`** | **`handoffs/active-context.md`** path, line budget, rollover triggers; **not** triad member |
| **`test_us0096_token_profile_orthogonality_paragraph`** | **`DELIVERY_MODE`** × **`TOKEN_PROFILE`** × **`CAVEMAN_MODE`** non-substitution in reference + runbook |

**`check_intake_template_parity.py --scope=us-0096`** manifest (**`US0096_PAIRS`** — architecture adds to script):

| Active | Template |
|--------|----------|
| `.cursor/scratchpad.md` (via example) | `template/.cursor/scratchpad.local.example.md` |
| `.cursor/commands/auto.md` | `template/.cursor/commands/auto.md` |
| `docs/engineering/auto-orchestration-reference.md` | `template/docs/engineering/auto-orchestration-reference.md` |
| `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` |
| `.cursor/commands/quick.md` | `template/.cursor/commands/quick.md` |
| `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` |
| `scripts/pack_json_validate.py` (new) | `template/scripts/pack_json_validate.py` |

**Harness**: register **`§26Q`** (or next free) in **`tests/run-tests.ps1`** / **`tests/run-tests.sh`**.

**Confidence**: **high** on mode-scoped reinstatement + orthogonality; **medium** on Tranche A **10%** standard-run reduction (requires execute measurement); **medium** on **`build+verify`** merged spawn ergonomics (operator E2E in runbook).

**Risks carried to architecture**:

| ID | Risk | Mitigation |
|----|------|------------|
| **R1** | **`ultra_lean`** without memory index | Tranche B blocked until **`pack.json`** validator + **`active-context`** template ship |
| **R2** | **`active-context`** vs triad confusion | Explicit non-triad lock in **`DEC-xxxx`** + contract test |
| **R3** | **`standard`** regression | **`test_us0096_standard_mode_baseline_markers_preserved`** |
| **R4** | **`mega_quick`** false routing | Eligibility table + seven fail-closed codes |
| **R5** | **`pack.json`** / **`sprints/`** drift | Coexistence table + no mid-story mode switch |

**Next phase pointers (`/architecture`)**: author **`# US-0096`** + companion **`DEC-xxxx`** (mode orthogonality, resolver step 0, **`run_class_hash`** extension, Tranche A defaults); lock **`test_us0096_*`** literals + **`US0096_PAIRS`**; runbook operator recipes per mode.

## R-0083 — BUG-0012: full_autonomy native-chain runtime regression (post-US-0095)

- **Date**: 2026-06-12
- **Topic**: **`AUTO_FLOW_MODE=full_autonomy`** + **`AUTO_BACKLOG_DRAIN=1`** — operator observes manual re-**`/auto`** after each story segment despite **US-0095** / **DEC-0080** native in-chat auto-chain delivery
- **Query**: Why does Cursor IDE **`/auto`** orchestrator stop at segment boundaries with "re-run /auto" / drain-active messaging when **DEC-0080** mandates in-chat continuation and 7-step drain-advance-without-pause — and what enforcement (command prose, orchestrator loop, contract tests, operator runbook) closes the gap between **shipped contract** and **observed runtime**?
- **Status**: **resolved for `/research`** (Q1–Q6 closed — architecture next)
- **Bug**: **BUG-0012**
- **Problem**: **US-0095** marked **DONE** (**S0084**, **2026-06-07**) with contract tests and doc markers for native-chain + forbidden outer-driver-mandatory prose; operator reports regression **2026-06-12** — behavior feels **less auto** than pre-adjustment runs; stops after every user-story completion while citing active drain/full_autonomy.
- **Linked**: **US-0095**, **DEC-0080**, **US-0092**, **DEC-0078**, **US-0088**, **US-0044**, **BUG-0006**, **DEC-0069**
- **Intake evidence**: `handoffs/intake_evidence/BUG-0012-intake-20260612.json`
- **Prior arc**: operator **`/ask`** (**2026-06-07**) diagnosed same symptom → **US-0095** intake → native-chain shipped; current report = **post-delivery regression** not re-litigation of feature intent.
- **Research asks (intake-locked)**:
  1. Reconcile **doc/contract PASS** vs **operator runtime FAIL** — agent compliance vs missing executable hook?
  2. Drain-advance trigger audit: does orchestrator execute **DEC-0080** step 7 (immediate spawn) or stop at **`stop_reason=completed (segment exhausted)`**?
  3. Forbidden-prose grep inventory — which end-of-run templates still emit mandatory re-**`/auto`** under **`full_autonomy`**?
  4. **`native_chain_active`** breadcrumb truthfulness in **`state.md`** at segment stop
  5. Interaction with **`AUTO_QUIET=1`**, recent **US-0096** / delivery-mode docs, and Task-tool availability (**`NATIVE_CHAIN_UNAVAILABLE`** path)
  6. Regression test strategy: multi-segment operator E2E + contract markers beyond static string presence
- **Next phase pointers**: **`/discovery`** (PO) → **`/research`** (TL) → **`/architecture`** (TL)

### Discovery extension (2026-06-12T20:45:00Z, PO, `orchestrator_run_id=auto-20260612-01`, `fresh_context_marker=po-BUG0012-discovery-20260612T204500Z-fresh`)

- **`/discovery`** **PASS** — regression framing locked: **US-0095** delivered contract; **BUG-0012** = **runtime/operator-observed** failure post-recent adjustments.
- **Q1 (contract vs runtime)**: prioritize orchestrator **executable continuation loop** audit in `.cursor/commands/auto.md` + reference — static marker presence insufficient if agent stops at turn boundary.
- **Q2 (drain-advance step 7)**: after **`refresh-context`** + **DEC-0069** pairing, orchestrator must **immediately** spawn first phase of next drain segment — invalid terminal: **`stop_reason=completed (segment exhausted)`** when OPEN stories remain and budget > 0.
- **Q3 (forbidden prose)**: inventory end-of-run templates that emit mandatory re-**`/auto`**, "run outer driver", or "segment exhausted" under **`full_autonomy`** + drain — cross-check **`tests/auto_command_contract_test.py`** markers.
- **Q4 (`native_chain_active`)**: verify **`state.md`** breadcrumb reflects actual continuation path at segment boundary (not set true at materialization then false at stop).
- **Q5 (interactions)**: **`AUTO_QUIET=1`** must not suppress continuation while reintroducing wait prose; **US-0096** delivery-mode docs must not contradict IDE-primary **DEC-0080** path; document **`NATIVE_CHAIN_UNAVAILABLE`** fallback boundary.
- **Q6 (tests)**: multi-segment operator E2E recipe (≥2 consecutive story boundaries) + additive contract markers for forbidden drain-stop prose and drain-advance spawn evidence.
- **Status**: **resolved for `/research`** — Q1–Q6 closed below.

### Research extension (2026-06-12T21:30:00Z, tech-lead, `orchestrator_run_id=auto-20260612-01`, `fresh_context_marker=tl-BUG0012-research-20260612T213000Z-fresh`)

- **External (EARLY_RESEARCH)**: [Cursor Subagents docs](https://cursor.com/docs/subagents) — foreground Task mode blocks until subagent completes; parent orchestrator **must** schedule the next spawn after await. No platform hook auto-continues `/auto` — continuation is **agent-behavior + command-spec** enforced only. **Conclusion**: **BUG-0012** is an **enforcement/compliance gap**, not a missing feature contract (**US-0095** / **DEC-0080** already normative).

#### Q1 — Doc/contract PASS vs operator runtime FAIL (`status=resolved`)

| Layer | Evidence | Verdict |
|-------|----------|---------|
| **Static contract** | Seven **`test_us0095_*`** subtests green (`pytest -k us0095`); template parity **`--scope=us-0095`** PASS at **US-0095** release | **PASS** — normative prose + markers shipped |
| **Operator runtime** | Operator report **2026-06-12**: stops after every story segment; cites active **`full_autonomy`** + drain; instructs manual re-**`/auto`** | **FAIL** — post-delivery regression |
| **Executable hook** | No stdlib/Cursor hook enforces orchestrator `while` loop; continuation relies on **`/auto`** orchestrator agent compliance | **Missing** — primary root cause |

**Divergence map** (orchestrator stops despite schedulable continuation):

| # | Surface | Conflict | Risk |
|---|---------|----------|------|
| 1 | **`.cursor/commands/auto.md`** § Steps (L419–420) | Retains **US-0088** escape: *"Outer-driver equivalence applies when a single invocation cannot schedule multiple subagent turns"* — primes stop at turn boundary under **`full_autonomy`** | **High** — contradicts § Native in-chat auto-chain primary path |
| 2 | **`.cursor/commands/auto.md`** § Continuous multi-phase (L68) | *"Stop segment; `AUTO_BACKLOG_DRAIN=1` may advance"* — ambiguous vs native chain **must** drain-advance | **High** |
| 3 | **`docs/engineering/auto-orchestration-reference.md`** § Full-autonomy matrix (L783) | *"Outer driver **re-invokes** when Cursor ends turn early"* — legacy **US-0092** row; not scoped to non-**`full_autonomy`** / fallback-only | **Medium** |
| 4 | **Phase command specs** (11 files) | *"stop and hand off … in a new subagent/chat"* — **correct** for phase-role subagents (**BUG-0006**); orchestrator must **not** treat phase stop as run terminal | **Medium** — agent conflation |
| 5 | **`handoffs/resume_brief.md`** contract lines | *"Contract: `/auto` continuation targets `research`"* — orchestrator may echo as **operator** instruction vs **Task-spawn** obligation | **Medium** |
| 6 | **No runtime attestation** | `state.md` lacks `drain_advance_action` / `native_chain_continuing` — cannot prove step 7 executed | **Medium** — audit gap |

**Root-cause verdict**: **agent compliance gap** (orchestrator stops after phase/subagent return) amplified by **residual US-0088/US-0092 stop priming** in **`auto.md`** + reference — **not** re-litigation of **US-0095** intent. Fix = strengthen orchestrator-only continuation mandate + behavioral contract tests + continuation-truth breadcrumbs (**architecture**).

#### Q2 — Drain-advance step 7 spawn audit (`status=resolved`)

**Normative contract** (**DEC-0080** / **R-0081** Q2): after `stop_phase=refresh-context` + `stop_reason=completed` + drain enabled + budget > 0, orchestrator executes 7-step algorithm; **step 7** = **IMMEDIATELY** Task-spawn first phase of next segment — **no** operator re-**`/auto`**.

**Observed failure mode** (operator repro): steps **1–6** often complete (**DEC-0069** `resume_brief` + `state.md` refresh evidenced in segment boundaries) but **step 7 spawn skipped** — orchestrator emits segment-complete / drain-active messaging and stops. Invalid terminal: **`stop_reason=completed (segment exhausted)`** (or equivalent prose) when OPEN stories remain and `backlog_drain_stories_remaining_budget > 0`.

**Evidence from current run** (`auto-20260612-01`): discovery checkpoint sets `native_chain_active=true`, `next_scheduled_phase=research`, `stop_reason=completed` at **phase** boundary — **correct** for intra-segment phase handoff; proves **DEC-0069** pairing works. Operator bug targets **inter-segment drain-advance** after **`refresh-context`** on **story** segments — same step 7 obligation applies.

**Gap**: no contract test asserts step **7** spawn obligation distinct from static **`immediately`** / **`without operator re-`/auto`**` literals; no `state.md` field records whether drain-advance spawn occurred.

#### Q3 — Forbidden-prose grep inventory (`status=resolved`)

**Normative forbidden patterns** (**DEC-0080** / **R-0081** Q5): mandatory `run the outer driver`; `re-run /auto` between drain segments; `segment exhausted` as terminal when continuation pending; unqualified `python scripts/auto_outer_driver.py` in IDE-primary **`full_autonomy`** prose.

| Surface | Forbidden pattern present? | Notes |
|---------|---------------------------|-------|
| **`auto.md`** § Native in-chat auto-chain | **Listed as forbidden** (L144) — positive guard only | `test_us0095_ide_drain_advance` checks native section lacks `run the outer driver` |
| **`auto.md`** § Steps + US-0088 matrix | **Ambiguous stop priming** (L68, L419–420) | Not covered by **`test_us0095_*`** |
| **`auto-orchestration-reference.md`** native sections | **Forbidden list** (L862–864) — positive | No negative grep test |
| **`auto-orchestration-reference.md`** full-autonomy matrix | **Outer driver re-invokes** (L783) | Legacy row; contradicts IDE-primary under **`full_autonomy`** |
| **Phase commands** (`discovery.md`, `research.md`, …) | **No** forbidden drain-stop phrases | Correct — phase-role stop only |
| **`handoffs/resume_brief.md`** | **No** mandatory re-**`/auto`** in template | Uses `/auto` as orchestrator context label |
| **`README.md`** / **`runbook.md`** | **optional** / **fallback** adjacent (US-0095 shipped) | Covered by `test_us0095_outer_driver_fallback_not_mandatory_ide` |

**`test_us0095_*` coverage gap**: seven subtests assert **positive markers** only — **no** negative grep across full **`auto.md`** + reference under **`full_autonomy`**; **no** assertion that orchestrator response templates forbid drain-stop prose; **no** scan of US-0088 matrix rows for native-chain precedence.

#### Q4 — `native_chain_active` breadcrumb truthfulness (`status=resolved`)

**Current semantics**: `native_chain_active=true` set when activation gate holds (**`AUTO_FLOW_MODE=full_autonomy`** + IDE + Task tool) — at materialization and phase boundaries (`state.md` L1117, L1164).

**Truthfulness gap**: field reflects **gate eligibility** (scratchpad + context), **not** **continuation action taken**. Orchestrator can set `native_chain_active=true` then stop without spawn — operator sees paradoxical "native chain active" + "run `/auto` again".

**Architecture recommendation**: add continuation-truth fields at segment boundary:

- `native_chain_continuing=true|false` — orchestrator scheduled next spawn/advance this boundary
- `drain_advance_action=spawned|skipped|not_applicable` — step 7 outcome
- `stop_reason` must **not** be `completed (segment exhausted)` when `native_chain_continuing=true`

#### Q5 — `AUTO_QUIET=1`, US-0096, `NATIVE_CHAIN_UNAVAILABLE` (`status=resolved`)

| Interaction | Finding | Verdict |
|-------------|---------|---------|
| **`AUTO_QUIET=1`** | Suppresses routine phase/drain prose; **must not** suppress continuation scheduling. Risk: agents conflate "quiet" with "stop after brief status." Table (auto.md L137–142) forbids outer-driver wait under quiet — **does not** forbid re-**`/auto`** instruction in agent-authored end-of-run text | **Contributing** — messaging ambiguity; not root cause alone |
| **US-0096** / **`R-0082`** | Delivery-mode axis (**`DELIVERY_MODE`**) — open stub; **no** `DELIVERY_MODE` key in merged scratchpad; no `.cursor/commands` delivery-mode prose active | **Orthogonal** when unset — no active contradiction with **DEC-0080** IDE-primary path |
| **`NATIVE_CHAIN_UNAVAILABLE`** | Fail-closed when Task denied / spawn depth limit; optional outer-driver hint | **Not operator path** — symptom is drain-active + re-**`/auto`**, not unavailable error |

**Precedence lock (architecture)**: under **`AUTO_FLOW_MODE=full_autonomy`** + IDE + Task available, **DEC-0080** native chain **supersedes** US-0088 Option B / US-0092 outer-driver re-invoke rows for continuation — fallback only on **`NATIVE_CHAIN_UNAVAILABLE`** or explicit headless/CI context.

#### Q6 — Regression test strategy (`status=resolved`)

**Existing**: `test_us0095_*` (7 subtests) — static marker parity; green at US-0095 release; **insufficient** for **BUG-0012** runtime regression.

**Proposed additive markers** (architecture locks exact names):

| Test | Intent |
|------|--------|
| `test_bug0012_forbidden_drain_stop_prose_negative_grep` | Negative grep: no mandatory `re-run /auto`, `segment exhausted` terminal, `run the outer driver` in **`auto.md`** + reference **native-chain + full_autonomy** normative blocks |
| `test_bug0012_orchestrator_post_subagent_spawn_mandate` | **`auto.md`** contains explicit orchestrator **MUST Task-spawn** next phase/segment after subagent return when continuation schedulable (distinct from phase-role "stop") |
| `test_bug0012_drain_advance_step7_no_stop_between_6_and_7` | Step 6 → step 7 **IMMEDIATELY** spawn — no "stop" / "hand off to operator" between steps in normative algorithm |
| `test_bug0012_native_chain_precedence_over_option_b` | Under **`full_autonomy`**, native chain primary prose precedes / supersedes US-0088 outer-driver equivalence escape in **`auto.md`** Steps |

**Operator multi-segment E2E recipe** (runbook — architecture adds § **BUG-0012 regression verify**):

1. Scratchpad: **`AUTO_FLOW_MODE=full_autonomy`**, **`AUTO_BACKLOG_DRAIN=1`**, **`AUTO_BACKLOG_MAX_STORIES≥2`**, **`AUTO_QUIET=1`**.
2. Backlog: **≥2 OPEN stories** (distinct segments).
3. Single **`/auto`** in Cursor IDE Agent panel.
4. Complete **story A** full lifecycle through **`refresh-context`**.
5. **Pass**: orchestrator drain-advances to **story B** first phase **without** operator re-**`/auto`** and **without** mandatory outer-driver / "segment exhausted" terminal prose.
6. Repeat for **story B** boundary or stop at hard gate / budget cap.
7. Evidence: `state.md` segment boundaries show `drain_advance_action=spawned`; `resume_brief` top pointer advances `story_id`.

**Fix surface inventory** (architecture / execute):

| # | Surface | Change |
|---|---------|--------|
| 1 | **`.cursor/commands/auto.md`** (+ template) | Orchestrator-only continuation block; clarify US-0088 matrix vs native chain; demote Option B to **`NATIVE_CHAIN_UNAVAILABLE`** / headless only |
| 2 | **`docs/engineering/auto-orchestration-reference.md`** (+ template) | Scope L783 outer-driver row to fallback; add step-7 spawn attestation fields |
| 3 | **`handoffs/resume_brief.md`** pairing contract | Wording: orchestrator **MUST Task-spawn** — not "operator runs `/auto`" |
| 4 | **`docs/engineering/state.md`** breadcrumbs | `native_chain_continuing`, `drain_advance_action` |
| 5 | **`tests/auto_command_contract_test.py`** | Four **`test_bug0012_*`** markers above |
| 6 | **`docs/engineering/runbook.md`** | Multi-segment E2E recipe |

**Preserved invariants**: **BUG-0006** spawn-only; **DEC-0078** hard gates; **DEC-0038** strict proof; **DEC-0069** resume_brief pairing; outer driver **optional fallback** only.

- **Confidence**: **high** on contract-vs-runtime diagnosis and fix surface; **medium** on Cursor spawn-depth limits (operator E2E required).
- **Next phase pointers (`/architecture`)**: author **`# BUG-0012`** (or amend **`# US-0095`** regression section); lock orchestrator continuation mandate, breadcrumb truth fields, **`test_bug0012_*`** literals, runbook E2E; confirm whether companion **`DEC-xxxx`** needed (research: optional — may extend **DEC-0080** amendment).

### Delivery closure (2026-06-13T02:00:00Z, curator, `orchestrator_run_id=auto-20260612-01`, `fresh_context_marker=curator-S0085-BUG0012-refresh-context-20260613T020000Z-fresh`)

> Append-only closure trailer for **R-0083**. **BUG-0012** shipped with **S0085** released **2026-06-13T01:30:00Z**; this refresh-context pass reconciles the research anchor to `status=delivered`. Evidence: **`handoffs/releases/S0085-release-notes.md`**, **`decisions/DEC-0081.md`**, **`docs/engineering/architecture.md`** **`# BUG-0012`**, five **`test_bug0012_*`** contract subtests, runbook § **BUG-0012 regression verify**, template parity **`--scope=bug-0012`**. No new **`R-xxxx`** allocated; no rewrite of **DEC-0080** body (amended by **DEC-0081** only).

- **Anchor status**: **`R-0083.status=delivered`** (**BUG-0012** **DONE** @ **2026-06-13T02:00:00Z** curator refresh).
- **Research phase status**: **closed** (Q1–Q6 resolved; architecture + execute + release delivered).
- **Forward pointer**: **`US-0096`** / **`R-0082`** (stub — extend at **`/discovery`**).

### Delivery closure (2026-06-13T17:00:00Z, curator, `orchestrator_run_id=auto-20260612-01`, `fresh_context_marker=curator-S0086-US0096-refresh-context-20260613T170000Z-fresh`)

> Append-only closure trailer for **R-0082**. **US-0096** shipped with **S0086** released **2026-06-13T16:00:00Z**; this refresh-context pass reconciles the research anchor to `status=delivered`. Evidence: **`handoffs/releases/S0086-release-notes.md`**, **`decisions/DEC-0082.md`**, **`docs/engineering/architecture.md`** **`# US-0096`**, eight **`test_us0096_*`** contract subtests, **`scripts/pack_json_validate.py`**, runbook § **Delivery modes**, template parity **`--scope=us-0096`**. No new **`R-xxxx`** allocated; no rewrite of **DEC-0052** / **DEC-0062** / **DEC-0080** / **DEC-0081** bodies.

- **Anchor status**: **`R-0082.status=delivered`** (**US-0096** **DONE** @ **2026-06-13T17:00:00Z** curator refresh).
- **Research phase status**: **closed** (Q1–Q7 resolved at **`/research`**; architecture + execute + release delivered).
- **Portfolio drain closure signal**: with **US-0096** closed, `docs/product/backlog.md` contains **zero** OPEN stories and **zero** OPEN bugs. Backlog-drain segment on **`auto-20260612-01`** closes at **`/refresh-context`**; next **`/auto`** invocation routes to **`/intake`** (`drain_terminated=true`; `drain_terminated_reason=no_open_stories`; `backlog_drain_stories_remaining_budget=8` of initial **10**).
- **Open R-xxxx anchors status (post-closure)**: **R-0082** **delivered** (this trailer). Next research anchor allocation deferred to the next **`/discovery`**-phase subagent when a new work item is intaked.

## R-0084 — US-0097: Project-owned root README bootstrap + per-story/sprint growth

- **Status**: `delivered` (delivery closure trailer above; curator refresh **2026-06-14T05:00:00Z**)
- **Topic**: Separate framework README (`its_magic/README.md`) from project-owned root `README.md` — bootstrap on first story, mandatory per-shipped-story growth, gate separation from **US-0091**
- **Story**: **US-0097**
- **Problem**: **DEC-0045** / **US-0062** declared `its_magic/README.md` as framework surface, but **`installer-owned-paths.manifest`** still installs root **`README.md`** (~1600-line its-magic catalog). No workflow step bootstraps or extends a project-specific repo overview as stories ship.
- **Intake evidence**: `handoffs/intake_evidence/US-0097-intake-20260613.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`)
- **Linked**: **US-0062**, **DEC-0045**, **US-0091**, **DEC-0074**, **US-0077**, **US-0032**, **US-0030**, **US-0071**, **US-0017**, **US-0094**
- **Research questions (intake-locked)**:
  1. **Installer manifest delta** — remove root `README.md` from framework install payload; confirm `its_magic/README.md` + `template/its_magic/README.md` parity path
  2. **Placeholder sentinel table** — deterministic signals for framework vs operator-authored root README
  3. **Migration merge policy** — non-destructive upgrade when lifting legacy framework root copy
  4. **Bootstrap trigger** — execute-time materialization when missing/placeholder; vision title sourcing
  5. **Per-story delta wiring** — mandatory execute/release steps; fail-closed reason family
  6. **Project validator sketch** — `validate_project_readme_coverage.py` predicate vs DONE `user_visible: true` rows
  7. **Gate separation** — reframe **US-0091** paths; release step 3g composition with 3f
  8. **Kit-repo exception** — `FRAMEWORK_KIT_REPO=1` dual-purpose root README for its-magic dev repo only

### Discovery extension (2026-06-13T20:00:00Z, PO, `orchestrator_run_id=auto-20260613-01`, `fresh_context_marker=po-US0097-discovery-20260613T200000Z-fresh`)

- **External (EARLY_RESEARCH=1)**: [GitHub — About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) — README answers what/why/how; keep concise, link deep reference to docs. Industry pattern (200–800 words): title + pitch + quick start + scannable features + developer setup — aligns with discovery-locked project scaffold (not framework encyclopedia).

#### Q1 — Installer ownership boundary (`status=resolved at discovery`)

| Path | Today | Target |
|------|-------|--------|
| Root `README.md` | In `[install_paths]` line 42 | **Removed** from framework install payload — project-owned |
| `its_magic/README.md` | Present (mirrors framework catalog) | **Canonical** framework README surface (**DEC-0045**) |
| `template/README.md` | Framework byte source (**US-0017**) | Stays framework kit source; **not** copied to consumer root on `missing` install |

**Normative**: fresh **`missing`** install on empty consumer target lays down **no** framework README at root; optional minimal pointer stub deferred to bootstrap (**Q4**).

#### Q2 — Framework placeholder sentinel table (`status=resolved at discovery`)

| Signal ID | Detection rule | Verdict |
|-----------|----------------|---------|
| **S1** | H1 matches `# its-magic — AI dev team` (exact or normalized whitespace) | placeholder |
| **S2** | Contains `<!-- readme-feature-coverage-catalog -->` | placeholder |
| **S3** | Heading contains `Feature coverage catalog (US-0091)` | placeholder |
| **S4** | Byte-identical to `template/README.md` on consumer install | placeholder |
| **S5** | None of S1–S4 **and** custom title/purpose outside framework blocks | **operator-authored** — preserve |

**Ambiguous** (partial S1–S4 match + mixed content) → **`PROJECT_README_MIGRATION_AMBIGUOUS`** (fail closed; runbook remediation).

#### Q3 — Kit-repo exception (`status=resolved at discovery`)

- **Consumer repos** (default): root README is **project-owned** only; framework catalog in **`its_magic/README.md`**.
- **its-magic framework dev repo**: scratchpad **`FRAMEWORK_KIT_REPO=1`** skips consumer bootstrap and preserves dual-purpose root README for dogfooding; **US-0091** continues to validate framework paths under **`its_magic/`** + kit root per architecture lock.
- **Detection order**: `FRAMEWORK_KIT_REPO=1` → sentinel table → operator-authored heuristic.

#### Q4 — Project README scaffold (`status=resolved at discovery`)

Locked outline (execute materializes when trigger fires):

```
# {Project Name}          ← vision.md H1
{1–3 sentence purpose}    ← vision Problem/Value distillate
## For users              ← what it does; how to run (placeholders OK at bootstrap)
## For developers         ← setup; repo layout; tests pointer
## Features
<!-- project-readme-feature-catalog -->
*(catalog grows per shipped US-xxxx)*
*Framework workflow commands: see [its_magic/README.md](its_magic/README.md).*
```

**Bootstrap trigger**: first **`/execute`** completion for a project story when root README missing **or** any placeholder sentinel (**S1–S4**) matches.

#### Q5 — Per-story delta + phase wiring (`status=open for /research`)

- **Execute** (mandatory): add/update ≥1 user-facing blurb under `<!-- project-readme-feature-catalog -->` for target **`US-xxxx`** before phase PASS.
- **Release** (mandatory when story ships): re-verify blurb present; sprint summary cross-link optional additive only.
- **Fail-closed family**: **`PROJECT_README_DELTA_SKIPPED`**, **`PROJECT_README_COVERAGE_GAP:<US-xxxx>`** — exact sub-codes architecture-locked.
- **Open**: exact execute.md / release.md step numbers; composition with **US-0032** optional user-guide block (orthogonal, zero overhead when `USER_GUIDE_MODE=0`).

#### Q6 — Validator + gate separation (`status=open for /research`)

| Validator | Input paths | Predicate |
|-----------|-------------|-----------|
| **`validate_readme_feature_coverage.py`** (**US-0091**) | `its_magic/README.md`, `template/its_magic/README.md` | DONE `user_visible: true` **framework** items |
| **`validate_project_readme_coverage.py`** (**US-0097**) | root `README.md` | DONE `user_visible: true` **project** backlog items |

- Release **3f** unchanged for framework; new **3g** for project gate.
- Scratchpad **`PROJECT_README_ENFORCE=0|1`** (default **`1`** post-bootstrap; **`0`** migration-only with skipped evidence).

#### Q7 — Migration merge policy (`status=open for /research`)

1. If root matches placeholder (**S1–S4**) and `its_magic/README.md` missing or older → copy framework content to `its_magic/README.md` (non-destructive).
2. Replace root with bootstrap scaffold (**Q4**) or minimal pointer per operator policy table.
3. If operator-authored (**S5**) → **do not** overwrite; add optional `its_magic/README.md` if absent; emit migration evidence tuple.

- **Open**: idempotent re-run rules; conflict when root is hybrid (partial framework + operator edits).

- **Confidence**: **high** on ownership split and sentinel table; **medium** on hybrid migration edge cases and kit-repo **US-0091** path lock.
- **Next phase pointers (`/research`)**: close Q5–Q7; CLI/`--report` schema; contract-test marker inventory; `check_intake_template_parity.py --scope=project-readme` manifest; confirm companion **`DEC-xxxx`** needed.

### Research extension (2026-06-13T21:00:00Z, tech-lead, `orchestrator_run_id=auto-20260613-01`, `fresh_context_marker=tl-US0097-research-20260613T210000Z-fresh`)

- **External (EARLY_RESEARCH=1)**: [GitHub — About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) — README answers what/why/how; keep concise; link deep reference to docs/wikis. Confirms discovery-locked **200–800 word** project front door (title + pitch + quick start + scannable features + developer setup) vs framework encyclopedia under **`its_magic/`**.
- **Repo survey**: **`execute.md`** steps end at **22** (triad); **`release.md`** doc gates end at **3f** (framework README); **`validate_readme_feature_coverage.py`** reads root **`README.md`** + **`docs/developer/README.md`** per **DEC-0074** — must reframe to **`its_magic/README.md`** family only; **`installer-owned-paths.manifest`** line 42 still lists root **`README.md`** in **`[install_paths]`**; no **`validate_project_readme_coverage.py`** exists yet; **`check_intake_template_parity.py`** has no **`--scope=project-readme`**.

#### Q5 — Per-story delta + phase wiring (`status=resolved`)

**Execute placement** — new step **23** after step **22** (triad hot-surface), mirroring optional-gate pattern from step **16** (**US-0032**) and mandatory guard pattern from step **20** (**US-0071**):

| Sub-step | Contract |
|----------|----------|
| **23 (preamble)** | Read merged scratchpad **`FRAMEWORK_KIT_REPO`** (default **`0`**). When **`1`**, skip **23a**/**23b** consumer bootstrap/delta (kit-repo exception per Q3). Read **`PROJECT_README_ENFORCE`** for delta obligation context (default **`1`** post-bootstrap). |
| **23a Bootstrap** | When root **`README.md`** missing **or** any placeholder sentinel **S1–S4** matches (Q2 table), materialize discovery-locked scaffold (Q4) sourcing H1/purpose from **`docs/product/vision.md`**. Emit bootstrap evidence tuple in execute checkpoint. |
| **23b Per-story delta (mandatory)** | Before **`/execute`** PASS for target **`US-xxxx`**: add or update **≥1** user-facing catalog bullet under **`<!-- project-readme-feature-catalog -->`** containing **`\\bUS-xxxx\\b`** (optional parenthetical id). Applies to **`user_visible: true`** project stories. Fail closed → **`PROJECT_README_DELTA_SKIPPED`**. |
| **23c Hygiene compose** | Project README prose edits subject to step **20** (**US-0071**) — no duplicate validator invocation beyond step **20** when README unchanged. |

**Release placement** — new step **3g** immediately after **3f**, before step **4** (UAT):

| Gate | Contract |
|------|----------|
| **3g Project README coverage** | Read merged scratchpad **`PROJECT_README_ENFORCE`** (default **`1`** post-bootstrap). When **`0`**: skip with **`skipped`** evidence in **`sprints/Sxxxx/release-findings.md`** § doc gates (migration/grandfathering only — same pattern as **3f** + **`README_FEATURE_COVERAGE_ENFORCE=0`**). When **`1`**: run **`python scripts/validate_project_readme_coverage.py --repo . --enforce`**. On failure: umbrella **`PROJECT_README_COVERAGE_BLOCKED`** + sub-codes on stderr. Active + **`template/.cursor/commands/release.md`** byte-identical **3g** block (full-file parity per **US-0017**). |

**Orthogonality locks**:

| Adjacent step | Interaction |
|---------------|-------------|
| **Execute 16** (**US-0032** / **`USER_GUIDE_MODE`**) | Zero overhead when **`USER_GUIDE_MODE=0`** — optional **`docs/user-guides/US-xxxx.md`** remains orthogonal to root catalog blurbs. |
| **Release 3d** (**US-0032**) | Same — no cross-block when user-guide mode off. |
| **Release 3f** (**US-0091**) | Framework gate unchanged; **3g** is additive sibling — both may run when respective enforce keys are **`1`**. |

**Fail-closed reason-code table** (architecture locks exact strings):

| Code | Phase | Trigger | Remediation |
|------|-------|---------|-------------|
| **`PROJECT_README_COVERAGE_BLOCKED`** | release | umbrella when **3g** enforce run fails | inspect sub-codes |
| **`PROJECT_README_COVERAGE_GAP:<US-xxxx>`** | release / validator | DONE **`user_visible: true`** item lacks catalog blurb | add bullet under **`## Features`** / marker |
| **`PROJECT_README_DELTA_SKIPPED`** | execute | target story shipped without catalog update | run **23b** before handoff |
| **`PROJECT_README_BOOTSTRAP_SKIPPED`** | execute | missing/placeholder root not materialized | run **23a** |
| **`PROJECT_README_MIGRATION_AMBIGUOUS`** | upgrade / migration | hybrid root (Q7) | runbook manual merge |
| **`PROJECT_README_PLACEHOLDER_UNRESOLVED`** | execute / migration | sentinel classifier inconclusive | apply S1–S5 table |
| **`PROJECT_README_ENFORCE_SKIPPED`** | release | **`PROJECT_README_ENFORCE=0`** | record migration evidence only |
| **`PROJECT_README_INPUT_INVALID`** | validator | backlog/README parse failure | fix inputs |
| **`PROJECT_README_SENTINEL_CONFLICT`** | migration | partial sentinel + operator prose | fail closed; operator resolves |

**Sprint cross-link** (optional additive): release notes may reference **`sprints/Sxxxx/summary.md`** — **not** a substitute for per-story catalog blurbs.

#### Q6 — Validator + gate separation (`status=resolved`)

**Path lock** (reframes **US-0091** / **DEC-0074** without rewriting **DEC-0074** body — architecture + companion **`DEC-0083`** amend scope):

| Surface | **US-0091** (framework) — after reframe | **US-0097** (project) — new |
|---------|----------------------------------------|----------------------------|
| Root **`README.md`** | **Excluded** from framework coverage predicate | **Sole** project validator input |
| **`its_magic/README.md`** | **Primary** framework catalog surface | Out of scope (pointer only from project root) |
| **`template/its_magic/README.md`** | Parity / install source | Out of scope |
| **`template/README.md`** | Framework kit source — **not** copied to consumer root on **`missing`** install | Out of scope |
| **`docs/developer/README.md`** | Remains framework DEV shard for **US-0091** | Out of scope for project gate |

**Kit-repo exception**: when **`FRAMEWORK_KIT_REPO=1`**, project validator **skips** root (same as execute **23** skip); **US-0091** continues on **`its_magic/`** paths + kit root per architecture lock.

**New scripts** (mirror **US-0091** stdlib-only split):

| Script | Role |
|--------|------|
| **`scripts/project_readme_coverage_lib.py`** | Sentinel detection (S1–S5), backlog parser reuse, catalog-section extractor, coverage predicate |
| **`scripts/validate_project_readme_coverage.py`** | CLI entrypoint |

**CLI flags** (parallel to **`validate_readme_feature_coverage.py`**):

| Flag | Purpose |
|------|---------|
| **`--repo PATH`** | Target repo root (default: parent of **`scripts/`**) |
| **`--backlog PATH`** | Default **`docs/product/backlog.md`** under **`--repo`** |
| **`--self-test`** | Predicate matrix + report schema stability → **`[PROJECT_README_COVERAGE_SELF_TEST_OK]`** |
| **`--report`** | Emit stable JSON report to stdout |
| **`--audit-out PATH`** | Write gap audit JSON |
| **`--enforce`** | Blocking mode for **`/release`** step **3g** |
| **`--no-kit-skip`** | Test hook — ignore **`FRAMEWORK_KIT_REPO=1`** skip |

**Coverage predicate** (normative sketch):

```
for each work_item in parse_backlog(backlog.md):
  if work_item.kind not in {US, BUG}: skip
  if work_item.status != DONE: skip
  if work_item.user_visible == false: skip
  if work_item.user_visible unset and PROJECT_README_ENFORCE == 0: skip (migration pass)
  if work_item.user_visible unset and PROJECT_README_ENFORCE == 1:
    emit PROJECT_README_INPUT_INVALID  # require explicit marker post-bootstrap
  catalog_section = extract_between_markers(root_readme, "<!-- project-readme-feature-catalog -->")
  if catalog_section contains \b{work_item.id}\b: present else gap
```

**`--report` JSON schema v1** (sorted keys, trailing newline — same canonical JSON helper as **US-0091**):

```json
{
  "catalog_marker_present": true,
  "coverage_missing": ["US-xxxx"],
  "coverage_present": ["US-xxxx"],
  "coverage_total": 0,
  "framework_paths_excluded": true,
  "gaps": [{"id": "US-xxxx", "kind": "US", "predicate_source": "explicit:true", "user_visible": true}],
  "kit_repo_skipped": false,
  "report_schema_version": 1,
  "repo_root": ".",
  "status": "PASS"
}
```

**Scratchpad keys**:

| Key | Values | Default | Notes |
|-----|--------|---------|-------|
| **`PROJECT_README_ENFORCE`** | **`0`** \| **`1`** | **`1`** post-bootstrap | **`0`** migration/grandfathering only — must record **`PROJECT_README_ENFORCE_SKIPPED`** evidence |
| **`FRAMEWORK_KIT_REPO`** | **`0`** \| **`1`** | **`0`** | Consumer repos never set **`1`** |

**Release composition with 3f**: gate order **3e → 3f (framework) → 3g (project) → 4 (UAT)** — independent enforce toggles; failure in either blocks release when respective enforce key is **`1`**.

#### Q7 — Migration merge policy (`status=resolved`)

**Idempotent migration algorithm** (upgrade / first-run after manifest fix):

| Step | Condition | Action | Re-run |
|------|-----------|--------|--------|
| **M1** | **`FRAMEWORK_KIT_REPO=1`** | Skip consumer migration; preserve dual-purpose root | no-op |
| **M2** | Root matches **S5** (operator-authored) | **Never** overwrite root; copy framework content to **`its_magic/README.md`** only if missing or older/smaller than root placeholder | idempotent |
| **M3** | Root matches **S1–S4** (placeholder) and **`its_magic/README.md`** missing | Copy root → **`its_magic/README.md`** (non-destructive lift) | skip if **`its_magic`** already populated |
| **M4** | Root matches **S1–S4** after **M3** | Replace root with project scaffold (**Q4**) or minimal pointer per operator policy | skip if root already project scaffold (no S1–S4) |
| **M5** | **Hybrid** (see below) | Fail closed **`PROJECT_README_MIGRATION_AMBIGUOUS`** | same error |

**Hybrid detection rule** (fail closed):

- **`match_count(S1–S4) >= 2`** **AND** custom H1/purpose outside framework blocks → **ambiguous**
- **OR** **S1** H1 present **AND** **`## For users`** / **`## For developers`** project sections already populated with non-framework prose → **ambiguous** (partial migration state)
- **OR** root contains **both** **`<!-- readme-feature-coverage-catalog -->`** **and** **`<!-- project-readme-feature-catalog -->`** with conflicting content → **`PROJECT_README_SENTINEL_CONFLICT`**

**Merge policy when root partially customized**:

| Root state | Policy |
|------------|--------|
| **S5 only** (no sentinels) | Preserve root verbatim; ensure **`its_magic/README.md`** exists |
| **Single sentinel + empty project sections** | Treat as placeholder → **M3**/**M4** |
| **Multiple sentinels + operator edits** | **M5** ambiguous — operator manual merge per runbook |
| **Project scaffold already present** | No migration action |

**Grandfathering**: **`PROJECT_README_ENFORCE=0`** during migration window; flip to **`1`** only after **`--report`** shows **`coverage_missing: []`** for explicit **`user_visible: true`** DONE rows (same activation pattern as **`README_FEATURE_COVERAGE_ENFORCE`** per **DEC-0074**).

#### Q8 — Contract-test inventory + template parity manifest (`status=resolved`)

**Proposed `test_us0097_*` markers** (architecture locks exact names in **`tests/auto_command_contract_test.py`**):

| Test | Intent |
|------|--------|
| **`test_us0097_installer_manifest_no_root_readme`** | **`installer-owned-paths.manifest`** excludes root **`README.md`** from **`[install_paths]`**; includes **`its_magic/README.md`** |
| **`test_us0097_execute_step23_literals`** | **`execute.md`** step **23** bootstrap/delta/skip prose + reason codes |
| **`test_us0097_release_step3g_literals`** | **`release.md`** step **3g** + **`PROJECT_README_ENFORCE`** + validator invocation |
| **`test_us0097_placeholder_sentinel_table`** | S1–S4 + S5 + ambiguous/hybrid literals in lib or runbook |
| **`test_us0097_framework_validator_paths_reframed`** | **US-0091** validator reads **`its_magic/README.md`** — not consumer root |
| **`test_us0097_project_readme_enforce_scratchpad_keys`** | Active + template scratchpad document **`PROJECT_README_ENFORCE`**, **`FRAMEWORK_KIT_REPO`** |
| **`test_us0097_project_readme_coverage_validator_contract`** | Script presence + **`[PROJECT_README_COVERAGE_SELF_TEST_OK]`** + report schema fields |
| **`test_us0097_us0091_regression_guard`** | Framework gate **3f** markers preserved; root removed from **US-0091** predicate paths |

**`check_intake_template_parity.py --scope=project-readme`** manifest (**`PROJECT_README_PAIRS`** — architecture adds to script):

| Active | Template |
|--------|----------|
| **`scripts/validate_project_readme_coverage.py`** | **`template/scripts/validate_project_readme_coverage.py`** |
| **`scripts/project_readme_coverage_lib.py`** | **`template/scripts/project_readme_coverage_lib.py`** |
| **`.cursor/commands/execute.md`** | **`template/.cursor/commands/execute.md`** |
| **`.cursor/commands/release.md`** | **`template/.cursor/commands/release.md`** |
| **`docs/engineering/runbook.md`** | **`template/docs/engineering/runbook.md`** |
| **`docs/engineering/context/installer-owned-paths.manifest`** | **`template/docs/engineering/context/installer-owned-paths.manifest`** |
| **`.cursor/scratchpad.local.example.md`** | **`template/.cursor/scratchpad.local.example.md`** |
| **`scripts/check_intake_template_parity.py`** | **`template/scripts/check_intake_template_parity.py`** |

**Harness**: register next free section in **`tests/run-tests.ps1`** / **`tests/run-tests.sh`** (follow **§26Q** / **US-0096** precedent).

#### Companion DEC decision (`status=resolved`)

**Verdict**: companion **`DEC-0083`** **required** at **`/architecture`** — discovery locks alone insufficient for **AC-10**:

| Factor | Rationale |
|--------|-----------|
| **AC-10** | Mandates **`decisions/DEC-xxxx.md`** + **`# US-0097`** |
| **DEC-0045** / **US-0062** amendment | Installer ownership boundary completion |
| **DEC-0074** path reframe | **US-0091** scope narrows to framework paths — normative amendment via companion DEC, not silent code drift |
| Precedent | **US-0096** → **`DEC-0082`**; **US-0091** → **`DEC-0074`** |

**Not optional** (contrast **US-0094** — intro-only, no companion DEC). Research does **not** author **`DEC-0083`** here.

**Confidence**: **high** on phase step numbers, validator API parity, gate order, and DEC requirement; **medium** on hybrid migration edge cases (operator E2E in runbook).

**Risks carried to architecture**:

| ID | Risk | Mitigation |
|----|------|------------|
| **R1** | Migration deletes operator prose | S5 preserve + **M5** ambiguous fail-closed |
| **R2** | **US-0091** regression | Explicit path table + **`test_us0097_us0091_regression_guard`** |
| **R3** | Kit vs consumer repo | **`FRAMEWORK_KIT_REPO`** detection order + validator skip |

**Research phase closure (US-0097)**: **PASS**. **`R-0084`** Q1–Q8 resolved. Story **US-0097** remains **OPEN** per **US-0045**. **Next**: **`/architecture`** (fresh **tech-lead**) — author **`DEC-0083`**, **`# US-0097`**, atomic task seeds, **`test_us0097_*`** literals, **`PROJECT_README_PAIRS`**.

### Delivery closure trailer — R-0084 (US-0097)

> Append-only closure trailer for **R-0084**. **US-0097** shipped with **S0087** released on **2026-06-14T04:30:00Z**; this refresh-context pass reconciles the research anchor to `status=delivered`. No new research questions opened; no new R-xxxx id allocated; no rewrite of **DEC-0083** or architecture `# US-0097`. `fresh_context_marker=curator-S0087-US0097-refresh-context-20260614T050000Z-fresh`.

- **Anchor status**: **`R-0084.status=delivered`** (**US-0097** **DONE** @ **2026-06-14T05:00:00Z** curator refresh). Single-story anchor; no shared-anchor split required.
- **Evidence**: sprint **`S0087`** released via **`handoffs/releases/S0087-release-notes.md`**; governance locked in **`decisions/DEC-0083.md`** + **`docs/engineering/architecture.md`** **`# US-0097`**; **`scripts/validate_project_readme_coverage.py`** + **`scripts/project_readme_coverage_lib.py`**; execute step **23** + release step **3g**; eight **`test_us0097_*`** contract subtests; template parity **`--scope=project-readme`** (**`PROJECT_README_PAIRS`**); UAT **10/10**.
- **Research phase status**: **closed** (Q1–Q8 resolved at **`/research`**; architecture + execute + release delivered).
- **Portfolio drain closure signal**: with **US-0097** closed, **`docs/product/backlog.md`** contains **1 OPEN** story (**`US-0098`**) and **0 OPEN** bugs. Backlog-drain segment on **`auto-20260613-01`** closes at **`/refresh-context`**; next native-chain drain advance → **`/discovery`** for **`US-0098`** (`drain_terminated=false`; `backlog_drain_active=true`; `backlog_drain_stories_remaining_budget=9` of initial **10**).
- **Open R-xxxx anchors status (post-closure)**: **R-0084** **delivered** (this trailer). Active forward stub: **R-0085** (intake stub for **US-0098**). Next research extension deferred to **`/discovery`** for **US-0098**.

## R-0085 — US-0098: Dev environment auto-launch profile (detect, persist, relaunch, connect)

- **Status**: **closed for `/research`** — architecture-ready (**2026-06-14T07:00:00Z**, tech-lead, `orchestrator_run_id=auto-20260613-01`)
- **Topic**: Operator-requested **dev-loop** automation — after implementation changes, **rebuild/restart** running stack (containers or dev server), **persist** detected dev environment, and **surface connection parameters** to the operator (not release-only).
- **Intake evidence**: `handoffs/intake_evidence/US-0098-intake-20260613.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`)
- **Discovery extension (2026-06-14T06:00:00Z, PO, `fresh_context_marker=po-US0098-discovery-20260614T060000Z-fresh`)**:
  - **Scratchpad proposal**: **`DEV_AUTO_LAUNCH_PROFILE`**: `off`|`deterministic_v1` (default **`off`**); optional **`DEV_ENVIRONMENT_CONFIG`** path override (default **`.cursor/dev-environment.json`**); orthogonal to **`AUTO_REMOTE_AUTOMATION_PROFILE`**
  - **Profile path**: **`.cursor/dev-environment.json`** + committed **`template/.cursor/dev-environment.json.example`** (names-only); do **not** extend **`release-targets.json`** schema (**US-0064** unchanged)
  - **Detection matrix** (discovery-locked): **`local`** (process dev server); **`docker-host-local`** (same-machine compose/docker — operator on Docker host, not SSH hop); **`docker`** / **`ssh`** only when automation remote profile resolves a target (**US-0086** precedence)
  - **Relaunch v1 triggers**: (a) post-**`/execute`** task when touched files ∈ runtime/container surface classes; (b) explicit operator **`refresh dev environment`**; **exclude** mandatory background **`docker compose watch`**
  - **Recipe tiers**: **A** rebuild (`Dockerfile*`, lockfiles) → `docker compose build`+`up`; **B** restart (config/non-hot-reload); **C** **`local`** → **`DEV_SERVER_COMMAND`** / stack profile
  - **Connect block fields**: `runtime_mode`, `connect_endpoint`, `health_path`, `service_id`, `container_id`, `target_id`, `env_refs`, `relaunch_outcome` — align **`runtime-connectivity.md`**; distinct from **US-0067** release-only timing
  - **Reason-code families (candidates)**: `DEV_ENV_PROFILE_DISABLED`, `DEV_ENV_PROFILE_INVALID`, `DEV_ENV_DETECT_AMBIGUOUS`, `DEV_ENV_COMPOSE_UNRESOLVED`, `DEV_ENV_RELAUNCH_FAILED`, `DEV_ENV_RELAUNCH_RETRY_EXhaustED`, `DEV_ENV_CONNECT_UNAVAILABLE`
  - **External refs**: [Docker Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/) (sync/rebuild file-class industry pattern — informs tier table, not v1 watch daemon)
- **Research questions (remaining for `/research`)** — **all resolved** in research extension below
- **Overlap anchors**: **US-0065**, **US-0086**, **US-0067**, **US-0085**, **US-0064**, **US-0093** (`process_health` / **`DEV_SERVER_COMMAND`**)

### Research extension (2026-06-14T07:00:00Z, tech-lead, `orchestrator_run_id=auto-20260613-01`, `fresh_context_marker=tl-US0098-research-20260614T070000Z-fresh`)

- **External (EARLY_RESEARCH=1)**: [Compose Develop specification — `develop.watch` actions](https://github.com/compose-spec/compose-spec/blob/main/develop.md) — industry file-class mapping: **`rebuild`** for `Dockerfile*` / lockfiles / dependency manifests; **`restart`** / **`sync+restart`** for config-only surfaces; **`sync`** for bind-mounted source (hot reload without image rebuild). **US-0098 v1** maps these action classes to execute-triggered **Tier A/B/C** recipes — **does not** ship mandatory **`docker compose watch`** daemon (discovery exclusion reaffirmed).
- **Repo survey**: **`execute.md`** steps end at **23** (**US-0097** project README); no **`dev_environment_lib.py`**; **`.cursor/dev-environment.json`** absent; **`.gitignore`** gitignores **`.cursor/remote.json`** but not yet **`dev-environment.json`**; **`check_intake_template_parity.py`** has no **`--scope=dev-environment`**; **`runtime-connectivity.md`** operator summary template exists; **US-0086** path filters documented in **`auto-orchestration-reference.md`** / **`R-0068`** (`Dockerfile*`, `docker-compose*.yml`, container runtime scripts).

#### Q1 — Profile schema + git policy (`status=resolved`)

**Canonical path**: **`.cursor/dev-environment.json`** (override via scratchpad **`DEV_ENVIRONMENT_CONFIG`**). Committed example: **`template/.cursor/dev-environment.json.example`**.

**Schema v1** (names-only; no **`release-targets.json`** schema change):

| Field | Type | Operator seed | Agent write | Notes |
|-------|------|---------------|-------------|-------|
| **`schema_version`** | integer | optional | required | **`1`** for v1 |
| **`detected_mode`** | enum | optional | required | **`local`** \| **`docker-host-local`** \| **`docker`** \| **`ssh`** |
| **`operator_seeded`** | boolean | set **`true`** on first manual seed | may flip **`false`** after agent merge | audit only |
| **`last_updated`** | ISO UTC string | optional | required on write | idempotent merge key |
| **`compose_file`** | string path | yes | yes | relative repo path; required for docker modes when known |
| **`service`** | string | yes | yes | compose service name |
| **`target_id`** | string | yes | yes | when **`docker`**/**`ssh`** via **US-0086** |
| **`connect`** | object | yes | yes | **`endpoint`** (literal host:port or **`protocol://host:port`** OK when not secret-derived); **`health_path`**; **`*Env`** keys only (**`hostEnv`**, **`portEnv`**, **`protocolEnv`**) — never values |
| **`rebuild_recipe`** | object | optional | yes | **`default_tier`** **`A`**\|**`B`**\|**`C`**; optional **`build_command`** / **`up_command`** / **`restart_command`** string templates (no secret literals) |
| **`env_refs`** | string[] | yes | merge | sorted unique env **names** operator must have set |
| **`evidence_refs`** | string[] | no | append | sprint/task/handoff refs |

**Git / ignore policy** (mirror **`.cursor/remote.json`** posture per **US-0085**):

| Artifact | Track in git? | Policy |
|----------|---------------|--------|
| **`template/.cursor/dev-environment.json.example`** | **yes** | names-only placeholders |
| **`.cursor/dev-environment.json`** | **no** | add **`.cursor/dev-environment.json`** to **`.gitignore`** + **`.cursorignore`** (defense-in-depth layer 2) |
| Operator seed in chat | n/a | agent writes/merges local file only; never paste secret values into JSON |

**Idempotent agent writes**: merge by field — operator-seeded **`connect.*Env`** names preserved unless superseded with evidence; **`evidence_refs`** append-only; **`last_updated`** always bumped.

#### Q2 — File-class → relaunch tier table (`status=resolved`)

Shared **container surface** globs align with **US-0086** / **`R-0068`** (deterministic path filters). **Highest matching tier wins** when multiple classes touch in one execute task.

| Tier | Action | Glob / path patterns (repo-relative) | Relaunch recipe (mode-dependent) |
|------|--------|--------------------------------------|----------------------------------|
| **A — rebuild** | `docker compose build` + `up -d` (docker-host-local / remote docker) | `Dockerfile`, `Dockerfile.*`, `**/Dockerfile`, `docker-compose*.yml`, `compose.y*ml`, `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `requirements*.txt`, `pyproject.toml`, `poetry.lock`, `Pipfile.lock`, `go.mod`, `go.sum`, `Cargo.toml`, `Cargo.lock`, `*.csproj`, `global.json` | Full image rebuild + recreate |
| **B — restart** | `docker compose restart <service>` or process restart | `*.env.example`, `nginx.conf`, `**/traefik/**`, `**/supervisord*.conf`, `application.y*ml`, `application*.properties`, `config/*.y*ml`, `docker-compose*.yml` **env-only** delta when Tier A patterns absent, container **entrypoint/cmd** scripts under `scripts/docker/` or `docker/` | Config / non-hot-reload surfaces |
| **C — local dev server** | **`DEV_SERVER_COMMAND`** / stack-aware start (**US-0093** / **`uat_probe_lib`**) | Applies when **`detected_mode=local`** and Tier A/B patterns absent but **`src/**`, `app/**`, `lib/**`, `pages/**`, `api/**`** or stack hot-reload paths touched | Process restart only |
| **Skip** | no relaunch | Docs-only, tests-only, `.md`, `.cursor/commands/**`, `handoffs/**`, `sprints/**`, `docs/**` (unless compose/runtime script under those trees matches Tier A/B) | Emit **`DEV_ENV_RELAUNCH_SKIPPED_NO_SURFACE`** |

**Bind-mounted source on docker-host-local**: when Tier A/B absent and only Tier C-like source paths change, default **`DEV_ENV_RELAUNCH_SKIPPED_NO_SURFACE`** (container sync/hot-reload assumed) — operator may force via explicit refresh (**Q4**). Architecture may document opt-in profile flag **`rebuild_recipe.restart_on_source_change`** (default **`false`**) in **`DEC-0084`**.

#### Q3 — Execute wiring + `dev_to_qa.md` evidence (`status=resolved`)

**Execute placement** — new step **24** after step **23** (**US-0097**), before execute completion / QA handoff:

| Sub-step | Contract |
|----------|----------|
| **24 (preamble)** | Read merged scratchpad **`DEV_AUTO_LAUNCH_PROFILE`** (default **`off`**) and optional **`DEV_ENVIRONMENT_CONFIG`**. When **`off`**, skip **24a–24d** with zero overhead (manual parity). |
| **24a Gate + profile load** | Validate profile path; run names-only schema check; fail closed → **`DEV_ENV_PROFILE_INVALID`**. When missing and detection cannot infer stack → **`DEV_ENV_PROFILE_MISSING`**. |
| **24b Detection + persist** | Run detection algorithm (**Q2** / precedence table below); merge **`detected_mode`**, **`compose_file`**, **`service`**, **`target_id`**, **`connect`**, **`env_refs`** idempotently into profile file. |
| **24c Relaunch (bounded)** | When execute task touched files match Tier A/B/C (**Q2**) **or** explicit refresh trigger fired (**Q4**): run tier recipe; **`retry_count`** max **2** (attempts **0..1** retry); delays **5s** then **15s**; non-transient failures fail fast (missing compose file, disabled target). |
| **24d Connect + handoff** | On success or skip/fail, append **Dev environment relaunch** + **Connect** sections to **`handoffs/dev_to_qa.md`** (and optional chat mirror). |

**`handoffs/dev_to_qa.md` evidence tuple** (mandatory when step **24** runs and profile **on**):

```markdown
## Dev environment relaunch (US-0098)

| Field | Value |
|-------|-------|
| `dev_auto_launch_profile` | deterministic_v1 |
| `runtime_mode` | docker-host-local |
| `relaunch_tier` | A \| B \| C \| (none) |
| `relaunch_command` | names-only command string(s) executed |
| `relaunch_outcome` | success \| skipped \| failed |
| `retry_count` | 0..2 |
| `reason_code` | (none) or DEV_ENV_* |

### Connect (operator)

| Field | Value |
|-------|-------|
| `runtime_mode` | … |
| `connect_endpoint` | … |
| `health_path` | … |
| `service_id` / `container_id` | … |
| `target_id` | … (when remote) |
| `env_refs` | [NAME_ONLY, …] |
| `relaunch_outcome` | … |
```

**Orthogonality**: step **18** (**US-0065**) runtime QA autopilot remains phase verdict evidence — distinct from **24** dev-loop relaunch. Step **17** (**US-0084**) remote cues compose when both fire.

#### Q4 — Explicit refresh hook (`status=resolved`)

| Trigger | v1 behavior |
|---------|-------------|
| **Primary NL phrase** | Exact literal **`refresh dev environment`** (case-sensitive, whole-phrase match in operator message or **`/execute`** argument — same strictness as **US-0086** **`start container <target_id>`**) |
| **Runbook synonyms (documentation only; not parsed v1)** | "rebuild dev stack", "restart dev environment", "reload dev containers" — map operators to primary phrase |
| **Optional command hook** | **`.cursor/commands/refresh-dev-environment.md`** thin wrapper delegating to execute step **24c** semantics (architecture may defer to runbook-only v1) |
| **Profile off** | Fail closed → **`DEV_ENV_PROFILE_DISABLED`** + remediation ("set **`DEV_AUTO_LAUNCH_PROFILE=deterministic_v1`**") |
| **Unroutable stack** | **`DEV_ENV_COMPOSE_UNRESOLVED`** or **`DEV_ENV_DETECT_AMBIGUOUS`** |

Explicit refresh **always** attempts relaunch (Tier from profile **`rebuild_recipe.default_tier`** or **B** when unset) even when no execute file-class match — bounded retries apply.

#### Q5 — Stdlib helper + template parity (`status=resolved`)

**Recommendation**: ship **`scripts/dev_environment_lib.py`** (+ **`template/scripts/`** mirror) — not doc-only. Rationale: schema validation, tier classification, and detection are testable; mirrors **`uat_probe_lib.py`**, **`project_readme_coverage_lib.py`** precedent.

**Public surface (architecture-locks exact names)**:

| Function / CLI | Purpose |
|----------------|---------|
| **`load_profile(path) -> dict`** | Parse JSON; reject inline secrets; validate required fields |
| **`classify_touched_files(paths) -> tier\|None`** | **Q2** table |
| **`detect_mode(repo, profile, scratchpad) -> (mode, reason_code\|None)`** | Detection precedence |
| **`build_relaunch_plan(mode, tier, profile) -> list[str]`** | Command list (no env value reads) |
| **`format_connect_block(profile, outcome) -> str`** | Markdown Connect block |
| **`python scripts/dev_environment_lib.py --self-test`** | **`[DEV_ENVIRONMENT_SELF_TEST_OK]`** contract marker |

**Parity manifest** — new **`DEV_ENVIRONMENT_PAIRS`** + **`check_intake_template_parity.py --scope=dev-environment`**:

| # | Active path | Template path |
|---|-------------|---------------|
| 1 | `.cursor/commands/execute.md` (step **24** block) | `template/.cursor/commands/execute.md` |
| 2 | `.cursor/scratchpad.md` (**`DEV_AUTO_LAUNCH_*`** keys) | `template/.cursor/scratchpad.md` |
| 3 | `.cursor/scratchpad.local.example.md` | `template/.cursor/scratchpad.local.example.md` |
| 4 | `template/.cursor/dev-environment.json.example` | (self — byte match active example) |
| 5 | `scripts/dev_environment_lib.py` | `template/scripts/dev_environment_lib.py` |
| 6 | `docs/engineering/runbook.md` (dev environment §) | `template/docs/engineering/runbook.md` |
| 7 | `docs/engineering/auto-orchestration-reference.md` (dev auto-launch §) | `template/docs/engineering/auto-orchestration-reference.md` |
| 8 | `.gitignore` (**dev-environment.json** line) | `template/.gitignore` (if present) or documented exception row |

**Contract-test markers** ( **`tests/auto_command_contract_test.py`** — architecture literals):

- **`test_us0098_dev_auto_launch_scratchpad_keys`**
- **`test_us0098_execute_step24_literals`**
- **`test_us0098_dev_environment_schema_contract`**
- **`test_us0098_detection_mode_precedence_literals`**
- **`test_us0098_reason_code_inventory`**
- **`test_us0098_connect_block_field_literals`**
- **`test_us0098_refresh_dev_environment_phrase_literal`**
- **`test_us0098_us0086_compose_no_schema_change`** (regression guard)

Harness section **§26W** (or next free) in **`tests/run-tests.ps1`** / **`tests/run-tests.sh`**.

#### Q6 — Security audit (**US-0085** inheritance) (`status=resolved`)

Four defense layers (extends **US-0085** / **DEC-0071**):

| Layer | Control |
|-------|---------|
| 1 — Schema | **`load_profile`** rejects inline secret-like literals (reuse remote-config heuristic patterns from **DEC-0016**); only **`*Env`** suffix keys in **`connect`** |
| 2 — Ignore files | **`.gitignore`** + **`.cursorignore`** block **`.cursor/dev-environment.json`** from agent file tools |
| 3 — Agent rules | No **`.env`** read; Connect output lists **`env_refs`** names only |
| 4 — Runtime | Relaunch subprocess inherits operator shell env — helper **never** opens **`.env`**; no **`docker compose`** env-file flags pointing at **`.env`** in v1 recipes |

**Audit paths**: profile load (**24a**), profile persist (**24b**), relaunch command construction (**24c**), Connect emission (**24d**), helper **`--self-test`**. Violation → **`DEV_ENV_SECRET_SURFACE_VIOLATION`**.

#### Q7 — Companion DEC necessity (`status=resolved`)

**Companion `DEC-0084` required at `/architecture`** — discovery locks alone insufficient:

| Factor | Why DEC |
|--------|---------|
| New persisted artifact + scratchpad keys | **`DEV_AUTO_LAUNCH_PROFILE`**, **`DEV_ENVIRONMENT_CONFIG`** |
| Cross-story composition | **US-0086** precedence, **US-0065** boundary, **US-0085** inheritance, **US-0093** **`DEV_SERVER_*`** |
| Execute contract | Step **24** sub-steps + retry cap |
| Detection precedence | Four-label matrix + **`docker-host-local`** vs remote disambiguation |
| Reason-code families | **`DEV_ENV_PROFILE_*`**, **`DEV_ENV_RELAUNCH_*`** registry |

**Alternative rejected**: architecture-only (**US-0094** / **R-0080** pattern) — rejected because **US-0098** introduces new operator-local JSON + execute automation cross-cutting **≥3** delivered decisions.

#### Detection precedence algorithm (`status=resolved`)

1. **`DEV_AUTO_LAUNCH_PROFILE=off`** → no detection/relaunch (manual unchanged).
2. Load profile from **`DEV_ENVIRONMENT_CONFIG`** or **`.cursor/dev-environment.json`**.
3. When **`AUTO_REMOTE_AUTOMATION_PROFILE=deterministic_v1`** **and** **US-0086** resolves a target: **`docker`** type → mode **`docker`** + **`target_id`**; **`ssh`** type → mode **`ssh`** + **`target_id`** (**US-0086** wins over local compose).
4. Else when compose file resolvable (profile **`compose_file`** or repo-root **`compose.y*ml`/`docker-compose*.yml`**) **and** local **`docker`** CLI succeeds → **`docker-host-local`**.
5. Else when **`DEV_SERVER_COMMAND`** set or stack profile inferable (**US-0065** / **`uat_probe_lib`**) → **`local`**.
6. Else → fail closed **`DEV_ENV_DETECT_AMBIGUOUS`**.

#### Reason-code inventory (`status=resolved`)

**`DEV_ENV_PROFILE_*`**: **`DEV_ENV_PROFILE_DISABLED`**, **`DEV_ENV_PROFILE_INVALID`**, **`DEV_ENV_PROFILE_MISSING`**, **`DEV_ENV_DETECT_AMBIGUOUS`**, **`DEV_ENV_COMPOSE_UNRESOLVED`**, **`DEV_ENV_TARGET_DISABLED`**, **`DEV_ENV_SECRET_SURFACE_VIOLATION`**

**`DEV_ENV_RELAUNCH_*`**: **`DEV_ENV_RELAUNCH_SKIPPED_NO_SURFACE`**, **`DEV_ENV_RELAUNCH_SKIPPED_PROFILE_OFF`**, **`DEV_ENV_RELAUNCH_FAILED`**, **`DEV_ENV_RELAUNCH_RETRY_EXHAUSTED`**, **`DEV_ENV_RELAUNCH_TIMEOUT`**, **`DEV_ENV_CONNECT_UNAVAILABLE`**

#### Risks (carry to `/architecture`)

- **R1**: Relaunch loops / duplicate containers — mitigated by **`retry_count`≤2** + idempotent profile writes + no watch daemon v1.
- **R2**: **`docker-host-local`** conflated with **US-0086** remote docker — mitigated by detection precedence step **3** vs **4** + explicit matrix in **`DEC-0084`**.
- **R3**: Secret leakage — mitigated by Q6 four-layer audit + gitignore local profile.
- **R4**: Execute step proliferation — step **24** gated default-off; zero overhead when **`off`**.

- **Confidence**: **high** on schema, tier table, execute placement, security; **medium** on bind-mount skip default (operator override via refresh).
- **Status**: **closed for `/research`** — architecture-ready; deliver **`DEC-0084`** + **`# US-0098`** at **`/architecture`**
- **Next phase pointers**: **`/architecture`** (TL) → **`/sprint-plan`** (TL)

> Append-only closure trailer for **R-0085**. **US-0098** shipped with **S0088** released on **2026-06-14T12:30:00Z**; this refresh-context pass reconciles the research anchor to `status=delivered`. No new research questions opened; no new R-xxxx id allocated; no rewrite of **DEC-0084** or architecture `# US-0098`. `fresh_context_marker=curator-S0088-US0098-refresh-context-20260614T130000Z-fresh`.

- **Anchor status**: **`R-0085.status=delivered`** (**US-0098** **DONE** @ **2026-06-14T13:00:00Z** curator refresh). Single-story anchor; no shared-anchor split required.
- **Evidence**: sprint **`S0088`** released via **`handoffs/releases/S0088-release-notes.md`**; governance locked in **`decisions/DEC-0084.md`** + **`docs/engineering/architecture.md`** **`# US-0098`**; **`scripts/dev_environment_lib.py`** + **`--self-test`**; execute step **24**; eight **`test_us0098_*`** contract subtests; template parity **`--scope=dev-environment`** (**`DEV_ENVIRONMENT_PAIRS`**); UAT **10/10**.
- **Research phase status**: **closed** (Q1–Q7 resolved at **`/research`**; architecture + execute + release delivered).
- **Portfolio drain closure signal**: with **US-0098** closed, **`docs/product/backlog.md`** contains **0 OPEN** stories and **0 OPEN** bugs. Backlog-drain run **`auto-20260613-01`** terminates at **`/refresh-context`** (`drain_terminated=true`; `drain_terminated_reason=no_open_stories`; `backlog_drain_stories_remaining_budget=8` of initial **10**; **2** stories consumed: **US-0097**, **US-0098**). Next operator action: **`/intake`**.
- **Open R-xxxx anchors status (post-closure)**: **R-0085** **delivered** (this trailer). No active forward research stubs for open portfolio work.

## R-0086 — US-0099: Dev-environment profile auto-bootstrap on install/upgrade

- **Story**: **US-0099** (intake **2026-06-14**; discovery **2026-06-14**; research **2026-06-14**)
- **Status**: **closed for `/research`** — architecture-ready (**2026-06-14T16:00:00Z**, tech-lead, `orchestrator_run_id=auto-20260614-01`)
- **Problem**: **DEC-0084** ships **`template/.cursor/dev-environment.json.example`** and gitignored local path but install/upgrade does not materialize **`.cursor/dev-environment.json`** — operators hit **`DEV_ENV_PROFILE_MISSING`** when enabling **`DEV_AUTO_LAUNCH_PROFILE`** without manual copy.

### Discovery findings (2026-06-14, PO)

**Repo survey**:

| Surface | Current behavior | US-0099 target |
|---------|------------------|----------------|
| **`installer.py`** **`missing`/`upgrade`** | Manifest copy + **`run_scratchpad_postinstall`** + **`bootstrap_runbook_commands`**; no profile bootstrap | Add post-postinstall hook calling **`bootstrap_dev_environment_profile()`** |
| **`installer.ps1`** / **`installer.sh`** | Delegate scratchpad-postinstall to Python | Same delegation for bootstrap hook |
| **`bin/postinstall.js`** | Banner-only (`npm install` / `npx its-magic`) | Invoke same bootstrap contract |
| **`installer-owned-paths.manifest`** | Example under **`template/`** via parity; local profile **not** in **`install_paths`** | Unchanged — bootstrap is runtime copy, not manifest row |
| **`.gitignore`** / **`.cursorignore`** | **`.cursor/dev-environment.json`** excluded | Unchanged (**DEC-0084**) |
| **`docs/engineering/runbook.md`** § Dev environment | "Seed profile" = manual **`Copy-Item`** prerequisite | Demote to **customize-after-bootstrap** |
| **`template/.cursor/remote.json`** | Manual seed; gitignored; default-off remote | **Contrast only** — dev profile auto-bootstrap because **`DEV_AUTO_LAUNCH_PROFILE`** expects loadable file |

**Discovery resolutions (Q1–Q4)**:

| Ask | Discovery lock | Research follow-up |
|-----|----------------|-------------------|
| **Q1** Hook placement | **After** **`run_scratchpad_postinstall`** on **`missing`** + **`upgrade`**; **before** **`bootstrap_runbook_commands`**; helper in **`dev_environment_lib.py`**; PS1/SH → Python | CLI flags (`--bootstrap`, `--target`); exit-code table; log token literals |
| **Q2** **`postinstall.js`** | Must share bootstrap contract with installer; read merged scratchpad when repo root detectable, else default path | Subprocess **`python scripts/dev_environment_lib.py --bootstrap`** vs inline Node; global-install cwd edge cases |
| **Q3** Reason codes | New **`DEV_ENV_BOOTSTRAP_*`** family (install-time) distinct from **`DEV_ENV_PROFILE_*`** (runtime) | Inventory: **`COPIED`**, **`SKIPPED_EXISTS`**, **`PATH_INVALID`**, **`SOURCE_MISSING`** |
| **Q4** Decision | **Amend DEC-0084** § bootstrap posture — not a new **`DEC-xxxx`** | Amendment paragraph prose + architecture **`# US-0099`** cross-ref |

**Path resolution contract (discovery-locked)**:

1. Parse merged scratchpad **`DEV_ENVIRONMENT_CONFIG`** (Model B layers already applied by postinstall).
2. If absent or empty → **`DEFAULT_PROFILE_PATH`** (**.cursor/dev-environment.json**).
3. Reject absolute paths, `..` traversal, non-`.json` suffix (fail-closed **`DEV_ENV_BOOTSTRAP_PATH_INVALID`**).
4. Source = **`template/.cursor/dev-environment.json.example`** relative to packaged template root.
5. Target exists → skip (**`DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`**); else **`shutil.copy2`** (**`DEV_ENV_BOOTSTRAP_COPIED`**).

**Tranche order (discovery-locked)**: **A** helper + reason codes → **B** installer hooks → **C** postinstall → **D** runbook + **`test_us0099_*`** + parity manifest delta.

### Research extension (2026-06-14T16:00:00Z, tech-lead, `orchestrator_run_id=auto-20260614-01`, `fresh_context_marker=tl-US0099-research-20260614T160000Z-fresh`)

- **External (EARLY_RESEARCH=1)**: [npm scripts lifecycle — `postinstall`](https://docs.npmjs.com/cli/v11/using-npm/scripts/) — **`postinstall`** runs after dependency install/update; keep hooks **minimal and idempotent** (npm recommends avoiding heavy **`install`** scripts). Industry pattern for config bootstrap: check **`fs.existsSync(dest)`** before **`copyFileSync`** ([Stack Overflow — copy JSON on install](https://stackoverflow.com/questions/64448989/how-to-copy-a-json-config-file-when-installing-my-package); [w3tutorials — postinstall asset copy](https://www.w3tutorials.net/blog/how-to-automatically-copy-files-from-package-to-local-directory-via-postinstall-npm-script/)). **US-0099** adopts copy-when-missing (not merge/sync) and delegates logic to stdlib Python helper (mirrors **`virtualenv-postinstall`** subprocess precedent for cross-language install hooks).
- **Repo survey (2026-06-14, tech-lead)**: **`dev_environment_lib.py`** ships **`load_profile`**, **`--self-test`**, **`--load`** but **no** **`bootstrap_dev_environment_profile()`** yet; **`installer.py`** calls **`run_scratchpad_postinstall`** then **`bootstrap_runbook_commands`** on **`missing`**/**`upgrade`** (lines ~879–886, ~959–966) with no profile hook; **`merge_scratchpad_layers`** / **`parse_scratchpad_file`** in **`installer.py`** are the canonical Model B scratchpad read — bootstrap helper **should reuse** the same merge semantics (import or duplicate minimal parser in lib to avoid circular imports); **`bin/postinstall.js`** banner-only; **`bin/its-magic.js`** uses **`spawnSync`** for PS1/SH — postinstall should **`spawnSync`** Python helper same as installer delegation; **`DEV_ENVIRONMENT_PAIRS`** (8 rows from **US-0098**) already covers **`dev_environment_lib.py`**, runbook, example JSON — **no new byte-parity rows** for root-only **`installer.py`** / **`bin/postinstall.js`** (contract-test literal guards instead).

#### Q5 — Helper CLI surface (`status=resolved`)

**Recommendation**: extend **`scripts/dev_environment_lib.py`** (+ **`template/scripts/`** mirror) with **`bootstrap_dev_environment_profile()`** and **`--bootstrap`** CLI — same stdlib-helper precedent as **R-0085** Q5 / **US-0098**.

**Public API (architecture-locks exact names)**:

| Symbol | Signature / flag | Purpose |
|--------|------------------|---------|
| **`bootstrap_dev_environment_profile`** | `(target_root: Path, source_root: Path \| None = None, scratchpad: dict \| None = None) -> tuple[str, str]` | Returns **`(reason_code, log_channel)`** where **`log_channel`** is **`stdout`** or **`stderr`** token line |
| **`resolve_profile_path`** | `(target_root: Path, scratchpad: dict) -> tuple[Path \| None, str \| None]` | Parse **`DEV_ENVIRONMENT_CONFIG`**; return **`(None, DEV_ENV_BOOTSTRAP_PATH_INVALID)`** when malformed |
| **`--bootstrap`** | CLI flag | Run install-time bootstrap |
| **`--target`** | repo root (default **`cwd`**) | Consumer repo path |
| **`--source-root`** | template root (default **`<pkg>/template`**) | Packaged example source tree |

**Path validation** (fail-closed; discovery locks reaffirmed):

- Reject absolute paths, **`..`** segments, paths outside repo root, non-**`.json`** suffix → **`DEV_ENV_BOOTSTRAP_PATH_INVALID`** (no copy; no silent fallback to default when override present but invalid).
- When **`DEV_ENVIRONMENT_CONFIG`** absent/empty → **`DEFAULT_PROFILE_PATH`** (**.cursor/dev-environment.json**).
- Source = **`{source_root}/.cursor/dev-environment.json.example`** only → missing source → **`DEV_ENV_BOOTSTRAP_SOURCE_MISSING`**.

**Exit codes**:

| Code | When |
|------|------|
| **0** | **`DEV_ENV_BOOTSTRAP_COPIED`** or **`DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`** (install continues) |
| **1** | **`DEV_ENV_BOOTSTRAP_PATH_INVALID`**, **`DEV_ENV_BOOTSTRAP_SOURCE_MISSING`**, or unexpected I/O error |

**User-visible log tokens** (**DEC-0053** — no **`US-xxxx`** / sprint ids on operator channel):

| Outcome | Token (stdout unless noted) |
|---------|----------------------------|
| Copied | **`[DEV_ENV_BOOTSTRAP_OK] copied: <repo-relative-target>`** |
| Skipped | **`[DEV_ENV_BOOTSTRAP_OK] skipped: profile exists at <repo-relative-target>`** |
| Path invalid | **`[DEV_ENV_BOOTSTRAP_ERROR] DEV_ENV_BOOTSTRAP_PATH_INVALID`** (stderr) |
| Source missing | **`[DEV_ENV_BOOTSTRAP_ERROR] DEV_ENV_BOOTSTRAP_SOURCE_MISSING`** (stderr) |
| Postinstall no repo | **`[DEV_ENV_BOOTSTRAP_SKIP] no consumer repository detected`** (stdout; exit **0**) |

**Reason-code constants** (add to **`dev_environment_lib.py`** alongside **`DEV_ENV_PROFILE_*`**):

- **`DEV_ENV_BOOTSTRAP_COPIED`**
- **`DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`**
- **`DEV_ENV_BOOTSTRAP_PATH_INVALID`**
- **`DEV_ENV_BOOTSTRAP_SOURCE_MISSING`**

**Installer wiring** (Python — architecture literals):

```python
# After run_scratchpad_postinstall(...); before bootstrap_runbook_commands(...)
if not bootstrap_dev_environment_profile_installer_hook(target_root, source_root):
    return 1
```

Thin wrapper **`bootstrap_dev_environment_profile_installer_hook`** in **`installer.py`** calls **`dev_environment_lib.bootstrap_dev_environment_profile`** with merged scratchpad from **`merge_scratchpad_layers`**. **`installer.ps1`** / **`installer.sh`** — **no** new surface; continue delegating to **`installer.py`**.

#### Q2 residual — Postinstall invocation (`status=resolved`)

**Recommendation**: **`bin/postinstall.js`** invokes Python subprocess — **not** inline Node copy — so bootstrap semantics stay single-sourced in **`dev_environment_lib.py`**.

**Algorithm**:

1. After existing banner, resolve **consumer repo root**: walk up from **`process.cwd()`** for **`.cursor/scratchpad.md`** or **`its_magic/.its-magic-version`** (max **6** parents); if none → emit **`[DEV_ENV_BOOTSTRAP_SKIP] no consumer repository detected`** and exit **0** (global **`npm install -g`** / package-dir cwd edge case per discovery risk **R1**).
2. Resolve **package template root**: **`path.join(__dirname, '..', 'template')`** (same layout as **`installer.py`** **`source_root`**).
3. **`spawnSync(python, [lib_path, '--bootstrap', '--target', repoRoot, '--source-root', templateRoot], { stdio: 'inherit', cwd: repoRoot })`** where **`python`** = **`process.env.PYTHON`** or **`python3`** or **`python`** (first on **`PATH`**).
4. Map exit code: **0** → success banner line; **1** → print remediation hint but **do not** fail **`npm install`** lifecycle (match scratchpad-postinstall soft-fail posture — log error, continue). Architecture may tighten to fail-closed on **`SOURCE_MISSING`** only.

**Parity with installer**: both paths call identical **`--bootstrap`** CLI; postinstall **does not** re-implement scratchpad merge — helper reads merged layers from target repo disk (requires **`run_scratchpad_postinstall`** to have run first on installer paths; on pure **`npm install its-magic`** in consumer repo, merged **`.cursor/scratchpad.md`** must already exist or helper uses example-only layer + default path).

#### Q6 — Contract tests + parity delta (`status=resolved`)

**Contract-test markers** (**`tests/auto_command_contract_test.py`** — architecture literals):

| Marker | AC | Asserts |
|--------|-----|---------|
| **`test_us0099_copy_when_missing`** | AC-1 | Temp repo: absent target → **`--bootstrap`** creates file; content matches example; **`DEV_ENV_BOOTSTRAP_COPIED`** token |
| **`test_us0099_skip_when_exists`** | AC-2 | Pre-seed customized bytes → second bootstrap → unchanged mtime/content; **`DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`** |
| **`test_us0099_upgrade_idempotent`** | AC-1, AC-2 | Simulate **`upgrade`** double-call → skip on second; no overwrite |
| **`test_us0099_path_override`** | AC-3 | Scratchpad **`DEV_ENVIRONMENT_CONFIG=custom/dev.json`** → copy to override; invalid override → **`PATH_INVALID`**, no file |
| **`test_us0099_postinstall_parity`** | AC-4 | **`bin/postinstall.js`** contains **`--bootstrap`** + **`dev_environment_lib.py`** spawn literal |
| **`test_us0099_installer_hook_literals`** | AC-1 | **`installer.py`** calls bootstrap **after** **`run_scratchpad_postinstall`** and **before** **`bootstrap_runbook_commands`** on **`missing`** + **`upgrade`** |
| **`test_us0099_bootstrap_reason_code_inventory`** | AC-7 | All four **`DEV_ENV_BOOTSTRAP_*`** codes defined in **`dev_environment_lib.py`** |

Harness: **`tests/run-tests.ps1`** / **`tests/run-tests.sh`** section **§26X** (or next free after **US-0098** §26W).

**`DEV_ENVIRONMENT_PAIRS` delta** (**`check_intake_template_parity.py --scope=dev-environment`**):

| # | Change | Rationale |
|---|--------|-----------|
| 1–8 | **Unchanged** from **US-0098** | Example, lib, runbook, execute step **24**, scratchpad keys already paired |
| — | **No new rows** for **`installer.py`**, **`installer.ps1`**, **`installer.sh`**, **`bin/postinstall.js`** | Root-only install surfaces — **contract-test literal guards** instead of template byte parity (**US-0097** installer-boundary precedent) |
| 9 (optional) | **`.gitignore`** **`.cursor/dev-environment.json`** line ↔ **`template/.gitignore`** | Only if architecture adds line to template mirror; otherwise document exception in **`# US-0099`** |

**Runbook delta** (already in pair row 6): replace "Seed profile" prerequisite with **customize-after-bootstrap** + **`DEV_ENV_PROFILE_MISSING`** troubleshooting referencing auto-bootstrap.

#### Q7 — Idempotency matrix (`status=resolved`)

**Rule**: existence check only — **no** byte comparison, merge, or timestamp refresh (**discovery lock**; mitigates risk **R2**).

| Install mode | Target state | Path config | Expected outcome | Disk after |
|--------------|--------------|-------------|------------------|------------|
| **`missing`** | absent | default | **`DEV_ENV_BOOTSTRAP_COPIED`** | Example bytes at **`.cursor/dev-environment.json`** |
| **`missing`** | absent | valid override | **`DEV_ENV_BOOTSTRAP_COPIED`** | Example at override path |
| **`missing`** | absent | invalid override | **`DEV_ENV_BOOTSTRAP_PATH_INVALID`** | No new file |
| **`missing`** | present (any) | default | **`DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`** | Unchanged |
| **`upgrade`** | absent | default | **`DEV_ENV_BOOTSTRAP_COPIED`** | Example copied |
| **`upgrade`** | present customized | default | **`DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`** | Operator prose preserved |
| **`upgrade`** | present customized | valid override | **`DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`** | Unchanged at override path |
| **npm postinstall** | absent | default | **`DEV_ENV_BOOTSTRAP_COPIED`** | Same as **`missing`** |
| **npm postinstall** | present | any | **`DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`** | Unchanged |
| **Re-run** (any mode) | present | any | **`DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`** | Idempotent |
| **Global npm** (no repo) | n/a | n/a | **`[DEV_ENV_BOOTSTRAP_SKIP]`** exit **0** | No side effects |

**Composition with US-0018**: smart-upgrade preserves **`user-data`** / local files; bootstrap adds **`.cursor/dev-environment.json`** only when absent — compatible because profile is gitignored local state, not manifest **`install_paths`** row.

#### Q4 residual — Decision pointer (`status=resolved`)

**No new `DEC-xxxx`**. Amend **`DEC-0084`** § bootstrap posture at **`/architecture`** (discovery lock reaffirmed):

- Install/upgrade/postinstall **copy-when-missing** from committed example.
- **`remote.json`** remains manual-seed (contrast table preserved).
- **`DEV_ENV_BOOTSTRAP_*`** reason family documented alongside **`DEV_ENV_PROFILE_*`**.

**Tranche order** (unchanged): **A** helper + codes → **B** installer hooks → **C** postinstall → **D** runbook + **`test_us0099_*`** + parity check.

**Top risks (carry to `/architecture`)**:

- **R1**: Global-install / wrong cwd — **`[DEV_ENV_BOOTSTRAP_SKIP]`** path documented in runbook.
- **R2**: Accidental overwrite — existence-only skip; contract tests **`skip_when_exists`** + **`upgrade_idempotent`** mandatory.
- **R3**: User-visible logs leak planning ids — **DEC-0053** scan on tokens above.

**Evidence refs**: `docs/product/vision.md` (**`## Discovery Notes — US-0099`**), `docs/product/backlog.md` (`## US-0099`), `handoffs/intake_evidence/US-0099-intake-20260614.json`, `scripts/dev_environment_lib.py`, `installer.py`, `bin/postinstall.js`, `decisions/DEC-0084.md`, `handoffs/archive/po-to-tl-pack-20260613.md` (US-0099 discovery handoff).

**Next phase pointers**: **`/architecture`** (TL) → **`/sprint-plan`**

> Append-only closure trailer for **R-0086**. **US-0099** shipped with **S0089** released on **2026-06-14T23:30:00Z**; this refresh-context pass reconciles the research anchor to `status=delivered`. No new research questions opened; no new R-xxxx id allocated; no rewrite of **DEC-0084** amended § bootstrap posture or architecture `# US-0099`. `fresh_context_marker=curator-S0089-US0099-refresh-context-20260615T000000Z-fresh`.

- **Anchor status**: **`R-0086.status=delivered`** (**US-0099** **DONE** @ **2026-06-15T00:00:00Z** curator refresh). Single-story anchor; no shared-anchor split required.
- **Research phase status**: **closed** (Q1–Q7 resolved at **`/research`**; architecture + execute + release delivered).
- **Portfolio drain closure signal**: with **US-0099** closed, **`docs/product/backlog.md`** contains **0 OPEN** stories and **0 OPEN** bugs. Backlog-drain run **`auto-20260614-01`** terminates at **`/refresh-context`** (`drain_terminated=true`; `drain_terminated_reason=no_open_stories`; `backlog_drain_stories_remaining_budget=7` of initial **8**; **1** story consumed: **US-0099**). Next operator action: **`/intake`**.
- **Open R-xxxx anchors status (post-closure)**: **R-0086** **delivered** (this trailer). No active forward research stubs for open portfolio work.

## R-0087 — US-0100: Version-scoped release changelog and GitHub release-note attachment

- **Story**: **US-0100** (intake **2026-06-15**; discovery **2026-06-15**; research **2026-06-15**)
- **Status**: **closed for `/research`** — architecture-ready (**2026-06-15T02:00:00Z**, tech-lead, `orchestrator_run_id=auto-20260615-01`)
- **Problem**: **US-0040** sprint notes and **`release_queue`** track workflow releases, but there is no semver-aligned cumulative changelog listing **US-xxxx** / **BUG-xxxx** with short summaries; **`scripts/release-all.sh`** uses **`gh release create --generate-notes`**, ignoring canonical its-magic bodies.

### Intake findings (2026-06-15, PO)

**Market / best-practice survey**:

| Pattern | Recommendation for US-0100 |
|---------|---------------------------|
| [Keep a Changelog](https://keepachangelog.com/) 1.1.0 | Repo-root **`CHANGELOG.md`**: **`[Unreleased]`** + semver sections (newest first), ISO dates, categorized bullets (Added/Changed/Fixed…) |
| [GitHub CLI `gh release create`](https://cli.github.com/manual/gh_release_create) | Prefer **`-F notes-file.md`** over **`--generate-notes`** when canonical body exists ([cli#8372](https://github.com/cli/cli/issues/8372): **`--generate-notes`** = GitHub Release Notes API; distinct from tag annotations) |
| Semantic Versioning | Align with **`package.json`** version + git tag **`vX.Y.Z`** from **`release-all.sh`** |
| Single source of truth | Derive GitHub release body from same per-version markdown as cumulative changelog section |

**Repo survey (intake)**:

| Surface | Current behavior | US-0100 target |
|---------|------------------|----------------|
| **`handoffs/releases/Sxxxx-release-notes.md`** | Rich sprint-scoped notes (**US-0040**) | Remain canonical sprint evidence; feed version doc derivation |
| **`handoffs/release_queue.md`** | **`release_version`** optional until finalization | Populate on **`/release`**; cross-link version docs |
| **`scripts/release-all.sh`** | **`gh release create --generate-notes`** | Use canonical version notes file when present |
| **`CHANGELOG.md`** | Absent | Introduce cumulative artifact + backfill from released sprints |
| **`/release` command** | Writes sprint notes + queue | Also append version changelog + per-version doc |

### Discovery findings (2026-06-15, PO)

**Repo survey (2026-06-15, TL verification)**:

| Metric | Count | Notes |
|--------|-------|-------|
| **`released`** queue rows | **78** | **`handoffs/release_queue.md`** |
| Rows with **`release_version`** set | **3** | **`S0050`→`0.1.2-30`**, **`S0070`→`0.1.2-41`**, **`S0071`→`0.1.2-41`** (duplicate semver — coalesce exemplar) |
| Rows with empty **`release_version`** | **75** | Require backfill policy |
| Sprint note files | **79** shipped + **`Sxxxx`** stub | Primary derivation feed (**`## What's new`**, **`story_refs`**) |
| **`package.json`** semver | **`0.1.2`** | Authoritative for **`release-all.sh`** bump only today |
| **`RELEASE_PUBLISH_MODE`** | **`disabled`** | Workflow **`/release`** may write docs; publish execution still gated (**US-0054** / **DEC-0036**) |
| GitHub attach today | **`scripts/release-all.sh`** L94–99 | **`gh release create "$TAG_NAME" --generate-notes`** — no sprint/queue read |

**Discovery locks (14)**: reaffirmed at research — L1 **`CHANGELOG.md`**, L2 **`handoffs/releases/{semver}-release-notes.md`**, L3 sprint layer unchanged, L4 derivation precedence, L5 **`-F`** per-version SOT, L6 queue binding, L7 idempotency, L8 backfill, L9 multi-sprint coalesce, L10 **US-0067** compose, L11 **US-0054** compose, L12 three workflow paths, L13 reason codes, L14 **`scripts/release_changelog_validate.py`**.

### Research extension (2026-06-15T02:00:00Z, tech-lead, `orchestrator_run_id=auto-20260615-01`, `fresh_context_marker=tl-US0100-research-20260615T020000Z-fresh`)

- **External (EARLY_RESEARCH=1)**: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) — maintain **`[Unreleased]`** at top; at release, rename section to version+date and recreate empty **`[Unreleased]`** ([issue #253](https://github.com/olivierlacan/keep-a-changelog/issues/253): update changelog in same PR as feature when possible). [GitHub CLI `gh release create`](https://cli.github.com/manual/gh_release_create) — **`-F file.md`** for operator-curated bodies; **`--generate-notes`** invokes GitHub Release Notes API (PR/commit derived, not its-magic narrative). Community pattern ([cli#9276](https://github.com/cli/cli/issues/9276)): extract version section from **`CHANGELOG.md`** — **US-0100** adopts explicit per-version file as SOT instead of runtime CHANGELOG parsing for **`gh`** attach (simpler, fail-closed).

#### Q1 — Backfill semver when queue rows lack `release_version` (`status=resolved`)

**Problem**: **75/78** released rows have blank **`release_version`**; only **3** explicit values exist.

**Recommendation**: **three-tier deterministic backfill** (idempotent script + operator manifest override):

| Tier | Source | Semver assignment | Queue side-effect |
|------|--------|-------------------|-------------------|
| **A — explicit** | Row **`release_version`** non-empty | Use as-is (**`0.1.2-30`**, **`0.1.2-41`**) | No synthetic label |
| **B — operator manifest** | **`docs/engineering/context/release-version-backfill.manifest.yaml`** (architecture-locked path) | Manual **`sprint_id`→`semver`** map for known npm/git history | Write **`remediation=backfill_manifest=<semver>`** |
| **C — synthetic workflow** | All remaining **`released`** rows | **`0.0.0-wf.{NNN}`** where **`NNN`** = zero-padded sprint number (**`S0089`→`0.0.0-wf.089`**) | Write **`remediation=backfill_synthetic=0.0.0-wf.089`** |

**Ordering**: process rows sorted by **`last_updated`** ascending for first-run manifest generation; emit **`CHANGELOG.md`** sections **newest-first** (Keep a Changelog).

**Ambiguity handling**:

- Duplicate explicit semver (**`S0070`** + **`S0071`** → **`0.1.2-41`**) → **coalesce** (see Q2); not ambiguous.
- Manifest collision (two sprints → same semver without coalesce intent) → **`RELEASE_CHANGELOG_BACKFILL_AMBIGUOUS`**; block backfill until manifest fixed.
- Missing sprint note file → skip row with **`RELEASE_CHANGELOG_SPRINT_ORPHAN`** in backfill report (do not invent work items).

**Alternative rejected**: assign all **75** rows to current **`package.json`** **`0.1.2`** — loses per-sprint audit trail and violates L8 "best-effort semver" without collapsing history.

**Alternative rejected**: git-tag archaeology — tags sparse/inconsistent vs workflow releases; non-deterministic for consumer repos.

#### Q2 — Multi-sprint coalesce into single semver version sections (`status=resolved`)

**Problem**: Multiple workflow sprints may share one npm bump / git tag (**`release-all.sh`**) or duplicate **`release_version`** (**`S0070`/`S0071`**).

**Recommendation**: **coalesce key = normalized semver** (strip leading **`v`**, semver-parse per [SemVer 2.0](https://semver.org/)).

**Coalesce algorithm** (shared helper — architecture name **`release_changelog_lib.py`**):

1. Collect all **`released`** queue rows sharing target semver (explicit field or post-**`npm version`** **`NEW_VERSION`**).
2. Derive work items per sprint via L4 precedence: sprint **`## What's new`** / **`story_refs`** → backlog title/summary → queue **`story_refs`**; include **BUG-xxxx** when sprint delivered defect work.
3. **Dedupe** work items by id (stable sort: **US** then **BUG** numeric).
4. Emit **one** per-version file **`handoffs/releases/{semver}-release-notes.md`** with:
   - **`## Work items`** — merged bullets
   - **`## Sprint evidence`** — links to **each** contributing **`Sxxxx-release-notes.md`**
5. Emit **one** **`CHANGELOG.md`** section **`## [{semver}] - {ISO date}`** — date = latest contributing sprint **`last_updated`** (UTC date component).
6. **Idempotency**: regenerate overwrites same semver artifacts; fingerprint = **`semver + sorted(work_item_ids)`**; second run must not duplicate bullets (**L7**).

**`release-all.sh` window**: after **`npm version`**, coalesce all **`released`** rows with empty **`release_version`** since last recorded git tag (or since last queue row with semver matching prior **`package.json`**) into **`NEW_VERSION`**; bind **`release_version=NEW_VERSION`** on those rows during attach step.

**Alternative rejected**: one sprint → one semver always — contradicts operator **`release-all.sh`** batch publish and existing **`0.1.2-41`** duplicate.

#### Q3 — `[Unreleased]` section workflow posture (`status=resolved`)

**Problem**: Workflow **`/release`** often finalizes sprints without npm bump (**`RELEASE_PUBLISH_MODE=disabled`**); Keep a Changelog expects **`[Unreleased]`** for not-yet-tagged work.

**Recommendation** (Keep a Changelog 1.1.0 aligned):

| Trigger | **`CHANGELOG.md`** | Per-version file | Queue **`release_version`** |
|---------|-------------------|------------------|----------------------------|
| **`/release`** PASS, semver **unknown** | Append work items under top **`## [Unreleased]`** (categorized Added/Fixed) | **Do not create** | Leave empty |
| **`/release`** PASS, semver **explicit** on row | **Promote**: move **`[Unreleased]`** + target sprint items into **`## [X.Y.Z] - date`**; recreate empty **`[Unreleased]`** | **Create/update** **`handoffs/releases/X.Y.Z-release-notes.md`** | Set **`release_version=X.Y.Z`** |
| **`release-all.sh`** post-**`npm version`** | Same promotion using **`NEW_VERSION`** | Same | Bind all coalesced rows |

**`[Unreleased]`** is **mandatory** header at top of **`CHANGELOG.md`** (empty placeholder allowed). Validator **`RELEASE_CHANGELOG_UNRELEASED_MISSING`** when absent.

**Promotion idempotency**: if semver section already exists with same fingerprint → no-op (log **`RELEASE_CHANGELOG_IDEMPOTENCY_OK`**); if semver exists with different work items → **`RELEASE_CHANGELOG_DUPLICATE_VERSION`** fail-closed.

**Alternative rejected**: require semver on every **`/release`** — blocks workflow-only releases that historically shipped without npm (**78** rows mostly blank).

#### Q4 — GitHub `-F` body source-of-truth vs sprint `Sxxxx` notes (`status=resolved`)

**Recommendation** (reaffirms discovery **L5**):

| Artifact | Role | Passed to **`gh release create -F`**? |
|----------|------|--------------------------------------|
| **`handoffs/releases/{semver}-release-notes.md`** | **Canonical GitHub/git body SOT** | **Yes** |
| **`handoffs/releases/Sxxxx-release-notes.md`** | Sprint workflow evidence (**US-0040** gates, **US-0067** Run/Connect/Verify) | **Never** |
| **`CHANGELOG.md`** | Cumulative operator audit | **No** (human doc; optional future extract per cli#9276 — out of v1 scope) |

**Derivation precedence** (structured data, single helper):

```
sprint Sxxxx notes → backlog summaries → queue story_refs
        ↓
release_changelog_lib.build_version_doc(semver, sprint_ids[])
        ↓
handoffs/releases/{semver}-release-notes.md  ──→  gh -F
        ↓
extract_changelog_section() → CHANGELOG.md append/rewrite
```

**`release-all.sh` attach** (replace L94–99):

```bash
VERSION_NOTES="handoffs/releases/${NEW_VERSION}-release-notes.md"
if [[ -f "$VERSION_NOTES" ]]; then
  gh release create "$TAG_NAME" -F "$VERSION_NOTES" --title "$TAG_NAME" $GH_PRERELEASE
else
  # fail-closed default; optional scratchpad RELEASE_CHANGELOG_ALLOW_GENERATE_NOTES=1 fallback
  err "RELEASE_CHANGELOG_VERSION_DOC_MISSING: $VERSION_NOTES"
fi
```

**`/release` publish path** (**US-0054** / **DEC-0036**): when **`RELEASE_PUBLISH_MODE`** **`confirm|auto`** and git-type target enabled, use same **`-F`** path — docs may be written under **`disabled`**; publish execution remains gated.

**Alternative rejected**: **`--generate-notes`** as default when file missing — violates operator truthfulness goal; keep opt-in fallback only.

#### Q5 — Validator reason-code family (`RELEASE_CHANGELOG_*`) (`status=resolved`)

**Script**: **`scripts/release_changelog_validate.py`** (+ **`template/scripts/`** mirror) — discovery **L14** name locked.

**Core fail-closed codes** (AC-7 + discovery **L13**):

| Code | Condition | Remediation |
|------|-----------|-------------|
| **`RELEASE_CHANGELOG_VERSION_MISSING`** | **`released`** row has semver bound in queue but no matching **`CHANGELOG`** section + per-version file | Re-run **`/release`** derivation or backfill |
| **`RELEASE_CHANGELOG_DUPLICATE_VERSION`** | Two **`CHANGELOG`** sections same semver, or idempotency fingerprint mismatch on re-derive | Manual merge; fix helper input |
| **`RELEASE_CHANGELOG_WORK_ITEM_GAP`** | Queue **`story_refs`** / sprint note work item absent from semver doc | Re-derive from sprint notes |
| **`RELEASE_CHANGELOG_ORDER_INVALID`** | Semver sections not newest-first | Re-sort **`CHANGELOG.md`** |
| **`RELEASE_CHANGELOG_UNRELEASED_MISSING`** | No top **`[Unreleased]`** header | Add Keep a Changelog header block |
| **`RELEASE_CHANGELOG_QUEUE_DRIFT`** | Queue **`release_version`** ≠ changelog binding for sprint | Reconcile queue or changelog |
| **`RELEASE_CHANGELOG_VERSION_DOC_MISSING`** | Semver finalized but **`handoffs/releases/{semver}-release-notes.md`** absent | Run derivation before **`gh`** attach |
| **`RELEASE_CHANGELOG_SPRINT_ORPHAN`** | **`released`** sprint not referenced in any semver section nor **`[Unreleased]`** | Backfill or promote |
| **`RELEASE_CHANGELOG_BACKFILL_AMBIGUOUS`** | Manifest collision / unresolved semver | Fix **`release-version-backfill.manifest.yaml`** |
| **`RELEASE_CHANGELOG_IDEMPOTENCY_VIOLATION`** | Duplicate work-item bullets same version on re-run | Fix helper dedupe |

**Category mapping** (closes discovery category ask — supplementary):

| Work item kind | **`CHANGELOG.md` category** | Per-version **`## Work items`** |
|----------------|----------------------------|--------------------------------|
| **`US-xxxx`** (default) | **Added** | Flat bullet with one-liner |
| **`BUG-xxxx`** | **Fixed** | Flat bullet with one-liner |
| **`user_visible: false`** story | **Changed** (or omit from consumer-facing doc — architecture chooses; default **Changed**) | Include if sprint **`story_refs`** lists it |

**Gate integration**: optional **`/release`** step after finalization (non-blocking when **`PROJECT_README_ENFORCE`-style grandfathering** not needed — default **enforce** for US-0100 scope). **`release-all.sh`** runs **`--enforce`** before **`gh`** attach.

#### Q6 — Publish integration + template parity (`status=resolved`)

**Shared helper surfaces** (both **`/release`** and **`release-all.sh`**):

| Surface | Writer | Reader |
|---------|--------|--------|
| **`scripts/release_changelog_lib.py`** | Derivation + coalesce + promote **`[Unreleased]`** | **`release_changelog_validate.py`**, **`release-all.sh`**, **`/release`** |
| **`scripts/release_changelog_backfill.py`** | One-time/idempotent Tier A/B/C backfill | Validator + backfill report |

**Template parity** (consumer repos):

| Path | Ship in **`template/`** |
|------|-------------------------|
| **`CHANGELOG.md`** | Stub (Keep a Changelog header + empty **`[Unreleased]`**) |
| **`handoffs/releases/vX.Y.Z-release-notes.md.example`** | Pattern doc (rename at use) |
| **`template/handoffs/releases/Sxxxx-release-notes.md`** | **Unchanged** (**US-0040**) |
| **`scripts/release_changelog_validate.py`** | Mirror + harness row |
| **`scripts/release_changelog_lib.py`** | Mirror |
| **`.cursor/commands/release.md`** | Version-doc steps (**US-0017** parity) |

**Compose with **US-0054** / **DEC-0036****: doc writes are **not** publish; **`RELEASE_PUBLISH_MODE=disabled`** remains valid; git/npm targets invoke **`-F`** only when mode allows. **`release-targets.json`** unchanged schema — optional future **`notesFileEnv`** out of v1.

**Dependencies for architecture**:

- **US-0040** — sprint notes remain evidence; no overwrite
- **US-0054** / **DEC-0036** — publish confirmation boundary preserved
- **US-0067** — operator hints stay in sprint notes; version doc links only
- **US-0008** — extend **`release-all.sh`** GitHub step
- **US-0017** — template command parity

**Top risks (carry to `/architecture`)**:

- **R1**: Backfill synthetic semver noise — mitigate with manifest Tier B + clear **`remediation`** column labels.
- **R2**: **`[Unreleased]`** promotion race on parallel sprints — serialize promotion per semver via fingerprint/idempotency.
- **R3**: Windows filename edge cases for semver pre-release (**`0.1.2-41`**) — use semver as filename stem (no **`v`** prefix per **L2**); test contract marker.
- **R4**: **`--generate-notes`** fallback temptation — default fail-closed; document opt-in scratchpad only.

**Evidence refs**: `handoffs/intake_evidence/US-0100-intake-20260615.json`, `docs/product/vision.md` (**Discovery Notes — US-0100**), `docs/product/backlog.md` (`## US-0100`), `handoffs/release_queue.md`, `handoffs/releases/S0089-release-notes.md`, `scripts/release-all.sh`, `docs/engineering/release-targets.json`, `.cursor/commands/release.md`, `.cursor/scratchpad.md` (**`RELEASE_PUBLISH_MODE=disabled`**)

**Next phase pointers**: **`/architecture`** (TL) — new **`DEC-xxxx`** locks artifact paths, helper API, backfill manifest, compose rules with **US-0040** / **US-0054**

> Append-only closure trailer for **R-0087**. **US-0100** shipped with **S0090** released on **2026-06-15T08:00:00Z**; this refresh-context pass reconciles the research anchor to `status=delivered`. No new research questions opened; no new **`R-xxxx`** id allocated; no rewrite of **DEC-0085** or architecture **`# US-0100`**. `fresh_context_marker=curator-S0090-US0100-refresh-context-20260615T090000Z-fresh`.

- **Anchor status**: **`R-0087.status=delivered`** (**US-0100** **DONE** @ **2026-06-15T09:00:00Z** curator refresh). Single-story anchor; no shared-anchor split required.
- **Research phase status**: **closed** (Q1–Q5 resolved at **`/research`**; architecture + execute + release delivered).
- **Portfolio drain closure signal**: with **US-0100** closed, **`docs/product/backlog.md`** contains **0 OPEN** stories and **0 OPEN** bugs. Backlog-drain run **`auto-20260615-01`** terminates at **`/refresh-context`** (`drain_terminated=true`; `drain_terminated_reason=no_open_stories`; `backlog_drain_stories_remaining_budget=6` of initial **7**; **1** story consumed: **US-0100**). Next operator action: **`/intake`**.
- **Open R-xxxx anchors status (post-closure)**: **R-0087** **delivered** (this trailer). No active forward research stubs for open portfolio work.
