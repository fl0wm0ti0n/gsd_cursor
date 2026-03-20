# Vision

## Problem
AI coding assistants in Cursor lose context across sessions, produce fragmented work without structure, and lack a repeatable process for turning ideas into shipped software. Teams and solo developers face:
- Knowledge rot: critical decisions and context live only in chat history and get lost.
- No structured workflow: ad-hoc prompting leads to inconsistent quality.
- No pause/resume: long-running projects can't be paused and resumed cleanly.
- No escalation: AI makes high-impact decisions silently instead of asking.
- No quality chain: no automated checks between code and deployment.

## Audience
- Solo developers and small teams using Cursor IDE who want a structured, repeatable AI-assisted development workflow.
- Developers building projects that span multiple sessions and need persistent context.
- Teams that want role-based AI collaboration (PO, Tech Lead, Dev, QA, Release, Curator) without external orchestration tools.

## Value
- **One command to start**: user describes the idea, AI handles the rest (intake → discovery → architecture → sprint → execute → QA → release).
- **Artifact-first memory**: all decisions, state, and progress live in files — the repo is the memory, not the chat.
- **Memory trust check**: a read-only audit can detect when code changed without matching updates in state, decisions, backlog, acceptance, or handoffs.
- **Release doc integrity**: release readiness can enforce README/runbook parity when commands or flags evolve.
- **Pause/resume without drift**: checkpoint and resume at any point with clean context.
- **Mid-process auto continuation**: restart automation from a deterministic phase checkpoint and continue remaining phases with one command.
- **Optional backlog-drain automation**: when explicitly enabled, `/auto` can continue across multiple planned stories with bounded switches and deterministic stop/skip policies.
- **Explicit bulk sprint planning**: optional bulk planning mode can turn many OPEN stories into bounded sprint plans with deterministic grouping and safety limits.
- **Explicit bulk execution orchestration**: optional bulk execute mode can run sprint-by-sprint with fresh agent contexts, execute↔QA loops, and bounded stop controls.
- **Decision gates**: AI escalates high-impact decisions to the user instead of guessing.
- **3-layer quality chain**: in-editor AI loop → local validate-and-push → CI auto-fix.
- **Policy-driven sync cadence**: optional phase/milestone-triggered sync can be configured, with safe default-off behavior and QA-first constraints.
- **Release safety gate**: release proceeds only after mandatory check-in tests and QA/UAT evidence pass deterministic gates.
- **Release history without overwrite**: per-sprint release notes preserve historical records instead of reusing a single mutable file.
- **Release queue visibility**: unreleased and released sprints are tracked in a canonical queue so pending release work is always explicit.
- **Backlog-release consistency**: released sprint evidence and backlog status/AC checks are deterministically reconciled to prevent stale OPEN stories after completion.
- **Single-source status trust**: backlog is the canonical story-status source, and acceptance/state artifacts are deterministically reconciled to prevent OPEN/DONE drift.
- **Spec-pack ready**: teams can optionally require Design Concept, CRS, and Technical Spec artifacts with near-zero overhead when disabled.
- **User-guide ready**: teams can optionally require user-friendly per-feature instructions with near-zero overhead when disabled.
- **Cross-repo aware**: optional observability can track module/API compatibility across repos and surface contract drift before release decisions.
- **Component-scoped safety**: optional scoped execution can focus work on selected components while explicitly protecting unaffected components.
- **Remote-ready by configuration**: optional remote execution uses a canonical `.cursor/remote.json` contract with fail-fast validation when enabled and zero overhead when disabled.
- **Drop-in installer**: one command installs the entire workflow into any repo.
- **Multiplatform**: available via npm, Chocolatey, and Homebrew.
- **Voice-friendly**: multilingual voice input as a first-class input layer.
- **Security-aware**: optional compliance review (GDPR, SOC2, HIPAA, PCI-DSS, ISO27001) at design and code level — zero overhead when disabled.
- **Knowledge-first decisions**: PO and architect research external docs, APIs, and best practices before deciding — curated knowledge persists across sessions and agents.
- **Adaptive intake depth**: guided intake can proactively ask clarifying questions and suggest options, or run low-touch mode via a switch when teams prefer direct capture.

## Look and Feel
- CLI-first: ASCII banner, clean terminal output.
- Slash-command driven: `/intake`, `/execute`, `/qa`, etc.
- Minimal footprint: zero npm dependencies, no build step.
- Convention over configuration: works out of the box with sensible defaults, configurable via scratchpad flags.

## UX References
- its-magic methodology: structured intake → rückfragen → specs → plan → execute → verify.
- Cursor IDE native: commands, rules, agents, hooks, skills.
- GitHub-style workflow: issues → PRs → CI → deploy.

## Discovery Notes — US-0045
- Canonical-source pattern: one artifact owns authoritative state; secondary views are derived/reconciled.
- Deterministic evidence model: status transitions should be evidence-first, never inferred from stale parallel artifacts.
- UX expectation: operators should get explicit mismatch diagnostics (which US, old/new state, evidence used, remediation) instead of silent auto-edits.
- Safety expectation: historical normalization must be auditable and scoped, so unrelated stories are never mutated by drift repair logic.

## Discovery Notes — US-0046 and US-0047
- Explicit-mode UX: high-autonomy behavior should be command-explicit (`--bulk`) rather than implicit side effects, so operators can choose between normal and bulk semantics.
- Bounded orchestration expectation: every bulk run needs deterministic limits (max items, stop/skip policy, reason codes) to avoid runaway planning/execution.
- Isolation expectation: fresh subagent context remains mandatory at fine granularity in bulk execution (per phase and execute↔QA cycle).
- Team-scope expectation: in team mode, bulk execution must honor member/task context and never run out-of-scope tasks.
- Safety expectation: default behavior remains unchanged unless bulk mode is explicitly enabled.

## Discovery Notes — US-0048

- Phase-isolation policy must be enforceable, not advisory-only.
- Orchestrator compliance requires auditable per-phase evidence proving fresh
  subagent contexts.
- Missing/invalid isolation evidence should fail closed at workflow progression
  and release boundaries with deterministic reason codes.
- Pause/resume checkpoints should preserve isolation provenance so continuation
  remains trustworthy.
- **Operator UX**: When isolation fails or evidence is missing, operators must
  see explicit diagnostics (reason code, phase id, evidence ref, remediation
  guidance) — no silent continuation or vague blocking.
- **Research boundaries**: Evidence schema (phase id, role, fresh-context marker,
  timestamp, evidence ref), canonical artifact locations for evidence, and
  verify/release gate integration are in scope for research; runtime product
  behavior and external orchestration platform changes are out of scope.

## Discovery Notes — US-0039

- Release gate tightening must be **mandatory**: check-in test baseline, QA completion evidence, and UAT completeness — no release path without all three in default configuration.
- **Deterministic gate order** is required: check-in test first, then QA gate, then UAT gate, then release-note/runbook updates; ordering must be documented and enforced so audit trails are unambiguous.
- **Auditable gate evidence**: each gate must write pass/fail and evidence pointers to handoff/state artifacts so QA and TL can verify decisions; no silent or inferred state.
- **No bypass without decision gate**: any override path (if allowed) requires explicit user decision and documented rationale (e.g. DEC-xxxx); default configuration has no bypass.
- **Template parity**: active and `template/` release/qa/execute guidance must stay behaviorally aligned for gate semantics so installed repos get the same release-safety contract.

## Discovery Notes — US-0049

- **Legacy drift**: Stories marked DONE in backlog but unchecked in acceptance or missing in traceability/release artifacts (e.g. US-0017, US-0030) need deterministic detection, target-scoped repair, and an ongoing guard so the gap does not recur.
- **Backfill vs guard**: One-time backfill mode repairs existing drift with an auditable report; ongoing guard runs at reconciliation/release boundaries (or dedicated check) to block or repair with explicit reason codes.
- **Scope**: Bounded repair only for stories that match "backlog DONE and (acceptance unchecked or traceability/release missing)"; no broad destructive rewrite. Template parity and regression coverage are required.
- **Operator UX**: Detection and repair must be inspectable: audit report with story ID, prior/resolved state, reason code, evidence ref; guard block must emit explicit reason codes and remediation so operators can fix or escalate by decision.
- **Research anchor**: R-0023 (legacy DONE-story backfill guard) supports detection rule, audit schema, and reason-code vocabulary; TL should align implementation with US-0045 (canonical source) and US-0043 (release-boundary reconciliation) without duplicating their scope.

## Discovery Notes — US-0032

- **Audience split**: Per-feature user guides serve end users and should remain clearly separate from internal technical docs like Design Concept, CRS, and Technical Spec.
- **Optional mode expectation**: User-guide generation must be controlled by a single flag, defaulting to off, with zero required workflow overhead when disabled (no extra gates or required artifacts).
- **Guide schema**: Each feature guide should follow a deterministic structure (purpose, prerequisites, step-by-step usage, example, limitations, troubleshooting) so completeness is testable rather than subjective.
- **Traceability**: Guides should be named and stored canonically (for example one guide per story/feature ID) and referenced from backlog, acceptance, and release handoffs when the mode is enabled.
- **Docs-as-code alignment**: User guides live in-repo alongside code, are updated in the same change as the feature, and are validated via simple structural checks instead of manual checklists.

## Discovery Notes — US-0050, US-0051, US-0052

- Fresh-install trust requires two guarantees: starter artifacts are neutral (no historical seeded project rows), and `--clean-repo` removes every installer-owned artifact deterministically.
- Cleanup ownership should be centrally defined (manifest-style or equivalent single source) and shared across installer implementations to prevent path drift and partial-clean states.
- Broad intake should not collapse into one oversized story; intake needs decomposition heuristics (vertical slices/workflow-step splits) with explicit user approval of proposed splits.
- Guided PO behavior should adapt to intake breadth and risk, not ambiguity alone, while keeping low-touch mode available for teams that prefer minimal interaction.
- Fresh-project teams may need optional namespace bootstrap so first IDs begin at `US-0001`/`DEC-0001`, without rewriting existing-history repos.

## Discovery Notes — US-0053

- **Token-efficiency objective**: Reduce recurring token cost by narrowing default
  retrieval scope and compaction of high-traffic context artifacts, while
  keeping mandatory QA/UAT/release safety gates intact.
- **Tiered profile UX expectation**: operators need one explicit policy switch
  (`lean|balanced|full`) instead of many ad-hoc toggles; profile behavior and
  override precedence must be deterministic and documented.
- **Context architecture expectation**: maintain a compact hot context for
  frequent reads and an archive path for historical detail, so routine
  `/ask`/phase runs avoid loading full lifecycle history.
- **`/ask` interaction expectation**: query resolution should be question-scoped
  (targeted sections first, progressive expansion only when unresolved) with
  strict read-only behavior preserved.
- **Discovery references**:
  - OpenAI prompt caching docs:
    `https://platform.openai.com/docs/guides/prompt-caching`
  - Anthropic prompt caching docs:
    `https://platform.claude.com/docs/en/build-with-claude/prompt-caching`
  - Progressive context loading pattern reference:
    `https://williamzujkowski.github.io/posts/from-150k-to-2k-tokens-how-progressive-context-loading-revolutionizes-llm-development-workflows/`

## Discovery Notes — US-0054

- **Target variability expectation**: release publish destinations differ by
  repository; publish targets must be configurable rather than hardcoded.
- **Half-automatic safety expectation**: publish actions should require explicit
  operator confirmation before execution by default.
- **Target taxonomy expectation**: support built-in destination types plus a
  generic custom-command type for non-standard environments.
- **SSH/generic server expectation**: SSH-based targets must be first-class in
  configuration (host/user/port/auth reference/remote command) so teams can
  deploy to custom servers without provider-specific coupling.
- **Security expectation**: credentials/tokens/keys should be env-reference
  based; no inline secrets in committed configuration.
- **Determinism expectation**: target selection/order, disabled-target skip
  behavior, and invalid-config failures must be deterministic and auditable.
- **Discovery references**:
  - GitHub deployment environments and protection rules:
    `https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments`
  - GitHub managing deployment environments:
    `https://docs.github.com/en/actions/how-tos/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment`
  - CircleCI deploy over SSH:
    `https://circleci.com/docs/guides/deploy/deploy-over-ssh`

## Discovery Notes — US-0055

- **Operator expectation**: teams need a deterministic command to detect and
  reconcile cross-artifact status drift (backlog/acceptance/state/resume)
  without ad-hoc manual edits.
- **Canonical precedence expectation**: backlog story status remains authoritative;
  derived artifacts must reconcile to backlog unless release evidence reveals
  canonical conflict requiring fail-closed remediation.
- **Scope boundary expectation**: reconciliation must be target-scoped and
  auditable (changed stories + before/after values), avoiding broad historical
  rewrites.
- **Continuation expectation**: reconciliation should restore deterministic
  `resume_brief` intent so `/auto` can continue from the correct next OPEN story
  and phase.
- **Diagnostics expectation**: blocked/conflict paths need deterministic reason
  codes and clear remediation guidance.

## Intake Notes — US-0056

- User requests strict runtime proof that `/auto` truly runs per-phase fresh
  subagent executions, not only artifact-level isolation markers.
- Required outcome: fail-closed enforcement when runtime proof is missing,
  reused, stale, or ambiguous.
- Expected scope: attestation schema, phase-gate integration, resume/pause
  provenance, and operator diagnostics for strict-proof failures.

## Discovery Notes — US-0056

- Runtime-isolation confidence must be proven by execution-time attestations, not
  only artifact text fields written after the fact.
- Attestation must be uniquely bound to phase execution and validated at each
  `/auto` boundary before continuation.
- Failure paths must be fail-closed with deterministic reason codes and
  remediation guidance so operators can recover safely.
- Pause/resume and release/isolation gates must consume strict attestation
  evidence to prevent unverifiable continuation.

## Intake Notes — US-0057

- User requests reliable upgrade handling for `.cursor/scratchpad.local.example.md`.
- Problem statement: `--mode upgrade` may leave scratchpad example with fewer
  options or mismatched guidance while some options already exist in user
  scratchpad surfaces.
- Expected scope: deterministic framework-vs-user ownership policy for
  scratchpad files, installer parity across PS1/sh/py, and explicit operator
  diagnostics/troubleshooting guidance for drift.

## Discovery Notes — US-0057

- `.cursor/scratchpad.local.example.md` must be treated as framework-owned and
  refreshed on upgrade.
- `.cursor/scratchpad.local.md` must remain user-owned and preserved.
- Installer output should provide deterministic, operator-visible diagnostics
  for example refresh status and local-file preservation.

## Intake Notes — US-0058

- User requests deterministic ordering discipline for artifact updates; current
  behavior appears mixed (top vs bottom insertion) across key files.
- Problem surfaces include `docs/engineering/state.md`,
  `docs/product/backlog.md`, and `docs/product/acceptance.md`.
- Expected scope: per-file ordering matrix (top-down/bottom-up/sorted),
  command-level mutation consistency, idempotent ordering behavior, and
  documentation/test coverage.

## Discovery Notes — US-0058

- A single canonical ordering matrix is required to avoid command-specific
  insertion drift.
- Commands that mutate ordering-sensitive artifacts must consume the same policy
  artifact and fail closed on ambiguous placement anchors.
- Re-run idempotence is mandatory: no reorder churn when there is no semantic
  change.

## Intake Notes — US-0059

- User reports intake runtime showing a role-capability mismatch (`po` subagent
  unavailable) followed by fallback execution in the same context.
- Same run reported backlog "changed mid-run" after intake persistence, implying
  possible self-write drift false positive behavior.
- Expected outcome: deterministic fail-fast on missing required subagent
  capability, plus single-writer drift semantics that distinguish self-writes
  from true concurrent external writers.

## Discovery Notes — US-0059

- Intake runtime must validate required role capability before mutation starts;
  default behavior is fail-fast, not silent in-band fallback.
- Drift guard needs deterministic writer/run identity so self-generated writes
  are not treated as external concurrent mutation.
- External conflicting writer activity must remain fail-safe with deterministic
  reason code and no partial overwrite behavior.

## Intake Notes — US-0060

- User reports `docs/engineering/state.md` grows very quickly in fresh repos
  (around 1800 lines after two sprints), despite prior compaction expectations.
- Expected outcome: deterministic, enforced rollover from hot surface to
  `docs/engineering/state-archive/` packs with bounded hot-surface size.
- Required behavior: non-destructive archival, idempotent reruns, and fail-safe
  handling when archive operations cannot be completed safely.

## Discovery Notes — US-0060

- Compaction must move from policy-only guidance to deterministic trigger
  enforcement (`max lines` and `max checkpoints`).
- Archive boundary selection and pack naming must be stable so reruns do not
  duplicate or reorder history.
- Fail-safe behavior must block partial mutation when archive boundary detection
  or archive write persistence fails.

## Intake Notes — US-0061

- User requests a global cross-phase non-destructive write rule: each phase can
  update only its owned artifact scope and must not delete text owned by other
  phases unless an explicit override-authorized phase is defined.
- User reports prior architecture history loss in a fresh repository run, which
  indicates missing ownership guardrails for `docs/engineering/architecture.md`.
- User requests stricter and more specific archive control to ensure archival is
  actually executed deterministically (not policy-only) while keeping `state.md`
  bounded.

## Discovery Notes — US-0061

- Ordering policy and canonical status ownership are necessary but not sufficient
  to prevent cross-phase destructive rewrites; an explicit ownership matrix is
  required.
- `docs/engineering/architecture.md` needs an explicit non-destructive contract
  (append new story sections / target-section-only update) to preserve history.
- Archive controls must include deterministic verification outputs and fail-safe
  mismatch handling, not just threshold configuration.

## Intake Notes — US-0062

- User requests a dedicated installer-owned folder (`its_magic/`) for
  framework metadata and non-project files (for example README framework surface
  and version marker).
- User expects project-owned artifacts (such as `src/`, project docs, and
  feature/runtime files) to remain outside this framework metadata folder.
- Expected outcome: deterministic install/upgrade/clean ownership behavior with
  clear separation between framework-managed vs project-managed files.

## Intake Notes — US-0063

- User requests onboarding-safe runbook auto-configuration that does not weaken
  quality gates and does not rely on placeholders.
- User expects OS-aware command defaults (for example Windows vs Unix) and
  stack-aware command generation for project checks.
- User reports practical mismatch case: Windows environment while runbook
  baseline command is Unix shell (`sh tests/run-tests.sh`).

## Intake Notes — US-0064

- User requests extending release/target configuration with runtime connectivity
  details such as domain, IP/host, port, and Traefik/ingress context.
- User requests Docker-over-SSH support as first-class remote runtime/deploy
  option.
- User expects remote-aware phase behavior: release/qa (and relevant execution
  steps) should consume this contract when project context is remote.
- User expects agents to provide clear operator connection information (where
  hosted, how to connect) and write this in a canonical document.

## Intake Notes — US-0065 to US-0068

- User requests stronger real-project runtime verification in generated repos:
  start app/service, verify connectivity/health, inspect logs, and attempt
  bounded self-debug retries before QA can pass.
- User requests generated baseline tests (unit/integration/acceptance) to be
  scaffolded and run automatically as part of execute/qa quality evidence.
- User requests operator-ready release outputs with concrete
  `Run/Connect/Verify` guidance (commands, endpoints/ports, expected health
  checks, env-ref credential sources, known issues).
- User requests mandatory intake question packs:
  - first-intake comprehensive questionnaire,
  - small-intake minimal questionnaire,
  with required coverage before persistence.

## Intake Notes — US-0069 and US-0070

- User reports a real generated-repository orchestration drift where `/auto`
  effectively ran only tech-lead for implementation flow, skipping intended
  role separation (`dev`, `qa`, `release`, etc.).
- User expects strict fail-closed role enforcement per phase, with no silent
  fallback to unrelated roles when required capability is unavailable.
- User requests a configurable scratchpad parameter to fine-tune which phases
  `/auto` runs (for example skip `research` or `sprint-plan`) while retaining
  deterministic behavior and safety visibility.

## Discovery Notes — US-0069

- Role enforcement must be a **preflight gate**: `/auto` resolves the required
  capability for the next canonical phase **before** spawning phase work, and
  fails closed if the required role is unavailable (no silent substitution).
- The canonical phase→role contract in backlog AC-1 is the source of truth;
  phases that allow multiple roles (`research`, `plan-verify`, `refresh-context`)
  require a **deterministic disambiguation policy** (for example scratchpad
  policy keys with documented precedence) so the expected role is never
  ambiguous at runtime.
- Phase completion is invalid when isolation evidence lists a `role` that does
  not satisfy the expected role contract for that `phase_id` (including
  policy-resolved alternates).
- **`execute` must default to `dev`**: `tech-lead` (or any non-dev) execution
  context is denied unless an explicit, documented override contract exists
  (default deny aligns with AC-5).
- Diagnostics must be operator-actionable: include `phase_id`, expected role(s),
  observed role/capability resolution, deterministic reason code, and
  remediation (for example spawn the correct subagent role or adjust policy).
- Strict runtime proof and isolation tuples must carry the same **resolved
  canonical role** so US-0048 evidence and US-0056 attestation stay aligned for
  auditors.
- Resume and `start-from` paths must run the same role preflight; stale or
  partial resume sources cannot bypass capability checks (AC-6).
- Scope boundary: this story covers **role mapping and enforcement** only;
  configurable phase inclusion/exclusion for `/auto` remains **`US-0070`**.

## Discovery Notes — US-0070

- Operators need **deterministic scratchpad controls** to include/exclude lifecycle
  phases (for example skip `research` / `sprint-plan`) without turning `/auto`
  into a manual phase runner; defaults must remain “full canonical lifecycle”.
- Phase selection must be **policy-single-valued**: one resolution path
  (`full` vs `exclude list` vs `include list` vs named `profile`) with documented
  precedence and fail-closed behavior on conflicts or unknown phase ids.
- **Safety gates cannot be silently bypassed**: default policy marks
  evidence-bearing and QA/release-related phases as non-skippable; any narrower
  profile must be explicitly named and traceable (not an accidental empty
  config).
- **`start-from` composes** with the resolved plan: execution begins at the
  latest of “resume/start anchor” and “first phase in resolved plan”, with empty
  intersection failing fast and listing both inputs.
- **Continuation parity**: backlog-drain, bulk execute, team scope, and pause
  boundaries must carry the same resolved phase plan metadata so resumes do not
  re-run skipped phases or drop policy without operator visibility.
- **Observability**: status output and `state.md` breadcrumbs should show
  `effective_phase_plan`, `skipped_phases`, and deterministic reason codes at
  phase boundaries for auditability.
- **Non-overlap with US-0069**: phase selection changes which phases run; it must
  not weaken role-capability preflight — skipped phases simply never spawn.

## Intake Notes — US-0071

- User reports repeated leakage of planning/development identifiers (for example
  User Story IDs) into user-visible UI/software outputs.
- User requires a strict boundary: such identifiers are allowed in internal
  documentation and code comments, but not in user-visible product surfaces.
- User expects deterministic automated enforcement during implementation and QA,
  with fail-closed diagnostics when leakage is detected.

## Discovery Notes — US-0071

- **User-visible surface** (for this kit): any software output intended for
  operators or end users outside internal engineering docs — including CLI
  stdout/stderr, generated app UI copy, user-facing error strings, and
  installer-visible messages — but excluding repository documentation trees,
  `docs/**`, `.cursor/**` policy text, sprint/handoff markdown, and
  source comments.
- **Forbidden token classes** (minimum baseline): planning identifiers matching
  `US-[0-9]{4}`, `DEC-[0-9]{4}`, and `R-[0-9]{4}` in those user-visible
  surfaces; research may extend the taxonomy without narrowing AC-1’s minimum.
- **Allowlisted internal-only use**: backlog, acceptance, architecture, state,
  handoffs, decisions, research notes, and code comments remain valid homes for
  those tokens; guards must target **outputs**, not **internal artifact
  authoring**.
- **Execute/QA contract**: default non-bypass checks on in-scope changes;
  deterministic fail-closed findings with path/context, token class, and
  remediation (aligns with AC-3–AC-5); reason codes such as
  `USER_VISIBLE_INTERNAL_METADATA_DETECTED` and
  `METADATA_SANITIZATION_POLICY_MISSING` (AC-6) should be documented in
  runbook/command surfaces.
- **False-positive control**: pattern scope is planning-id shaped tokens in
  user-visible channels only — not generic “US” substrings in prose where
  context proves non-planning usage; QA negatives must prove leak blocking without
  breaking allowlisted docs/comments (AC-7, AC-9).
- **Parity**: active and template copies of commands, rules, runbook, and README
  stay aligned when policy text or guard instructions change (AC-8).
- **Non-overlap**: does not subsume `US-0069` role routing, `US-0070` phase
  selection, or general content/style governance (see backlog boundaries).

## Intake Notes — US-0072

- User reports state archiving is still not functioning in practice: active
  `state.md` grows while `state-archive` remains empty.
- User reports high-growth handoff and architecture artifacts are becoming too
  large, increasing context noise and agent misunderstanding/hallucination risk.
- User requests a stronger process that keeps artifacts compact and ensures
  subagents read only necessary context for each phase without losing required
  historical evidence.

## Discovery Notes — US-0065

- Runtime QA for generated projects must be evidence-first and executable: PASS
  requires successful startup, reachability/health validation, runtime log
  inspection, and bounded retry outcomes, not only static command checks.
- Bounded self-debug behavior needs deterministic limits and explicit per-attempt
  traceability so retries increase reliability without creating unbounded loops.
- Stack-aware startup/health command resolution should cover at least
  Node/Python/Go/Java/.NET with deterministic fallback and fail-safe handling
  when no reliable runtime profile is available.
- Webapp contexts should include browser-level verification guidance (smoke
  navigation plus console/network error inspection) as part of runtime QA
  evidence when applicable.
- QA artifacts should capture canonical runtime evidence fields: startup command,
  runtime mode (`local|remote`), endpoint/health result, log summary, retry
  ledger, and final reason-coded verdict.
- Reason-code taxonomy should be explicit and deterministic across runtime
  failure boundaries (startup failure, unreachable endpoint, critical log signal,
  retry budget exhaustion, unresolved stack profile) with operator remediation
  guidance.
- Story boundary must remain strict: US-0065 defines runtime verification
  contract/evidence; generated test scaffolding and release operator hints remain
  in US-0066/US-0067.
- Discovery remediation rerun for strict-proof continuity confirms no scope
  change: US-0065 remains limited to runtime verification contract/evidence only.

## Discovery Notes — US-0066

- Generated-project quality should include baseline runnable tests by default;
  quality gates cannot assume tests already exist in fresh app repositories.
- Test scaffold generation must be deterministic and non-destructive: create
  missing baseline tests and runnable command wiring without overwriting
  user-authored test suites or custom test commands.
- QA must execute generated baseline tests automatically and produce explicit
  evidence for pass/fail outcomes; absence of runnable generation for a detected
  stack must fail closed with reason-coded remediation.
- Rerun behavior should be idempotent and auditable: repeated execute/qa passes
  must not duplicate scaffolding or oscillate runbook command configuration.
- Scope boundary must remain strict: US-0066 covers test scaffold generation and
  automatic execution evidence; runtime startup autopilot remains in US-0065,
  release operator hints remain in US-0067.

## Discovery Notes — US-0067

- Release outputs should include a deterministic operator contract section with
  fixed ordering and concise required fields: `Run` -> `Connect` -> `Verify` ->
  `Credentials (env-ref only)` -> `Known Issues`.
- `Run` should capture exact startup command(s) and runtime mode (`local|remote`)
  to avoid operator ambiguity across local and remote execution contexts.
- `Connect` should capture endpoint details (`url/ip:port`) and expected health
  signal so first verification is reproducible from release notes alone.
- `Credentials` guidance must remain reference-only (env variable names and
  value source), with explicit no-secret-inline policy in release surfaces.
- Release finalization should fail closed when any required run/connect/verify
  field is missing or ambiguous, with deterministic reason-coded remediation.
- Scope boundary must remain strict: this story defines release operator hints
  contract only; runtime QA autopilot stays in `US-0065`, test scaffolding in
  `US-0066`, and intake question-pack policy in `US-0068`.

## Discovery Notes — US-0068

- Intake must enforce deterministic minimum topic coverage before persistence,
  not only adaptive "ask more when unclear" behavior.
- Two canonical questionnaire packs are required: first-intake comprehensive
  and small-intake compact, each with explicit required coverage topics.
- Persistence gating must be fail-closed when required answers are missing,
  unless bounded assumptions are explicitly confirmed by the user and recorded.
- Low-touch mode remains supported, but it must still ask and capture a minimum
  critical safety subset before allowing persistence.
- Intake outputs should carry auditable questioning evidence
  (covered topics, missing topics, assumption confirmations, and block reason
  codes) so downstream phases can trust intake completeness deterministically.
- Scope boundary must remain strict: `US-0068` defines intake questionnaire and
  persistence-gate policy only; runtime QA/test scaffolding/release operator
  guidance remain in `US-0065`/`US-0066`/`US-0067`.
