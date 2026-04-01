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

## Discovery Notes — US-0072

- **Primary hot surfaces (AC-1 default)**: `docs/engineering/state.md`,
  `handoffs/po_to_tl.md`, and `docs/engineering/architecture.md`. Other
  `handoffs/*.md` files may grow by lifecycle design; research/architecture
  should justify any expansion beyond this triad rather than implicit scope creep.
- **Threshold authority**: Rollover and budget gates must read **merged
  scratchpad** values (for example `STATE_HOT_MAX_LINES`,
  `STATE_HOT_MAX_CHECKPOINTS`, and any analogous keys added for handoff or
  architecture hot caps) so enforcement cannot drift from operator-configured
  policy.
- **Same-phase execution**: When a hot surface exceeds its threshold, rollover
  runs in the **same** mutating phase boundary or that phase **fails closed**
  with a deterministic reason code—no silent continuation with an oversized hot
  file (aligns with AC-2, AC-4).
- **Verification evidence (AC-3)**: Successful archive passes must emit a
  deterministic tuple (`boundary`, `moved`, `retained`, `pack_ref`); pack naming
  and partitioning must stay idempotent on reruns to avoid duplicate or
  oscillating archive churn.
- **Bounded reads (AC-5–AC-6)**: Define per-phase **required** artifact reads and
  optional escalation with explicit line/file budgets; prefer hot-surface
  pointers, section indexes, or compact summaries so subagents load the latest
  relevant checkpoint first and expand only when unresolved.
- **Regression posture (AC-10)**: Tests must detect failure modes such as hot
  surface over threshold with **no** corresponding archive pack write, plus
  idempotent rerun and budget-exceeded paths.
- **Scope wall**: No overlap with `US-0071` (user-visible metadata),
  `US-0073` (scratchpad delivery), or `US-0074` (baseline test cleanup); no
  deletion of historical evidence or weakening of QA/release gates (backlog
  boundaries).

## Intake Notes — US-0073

- User requests scratchpad delivery simplification: shipping both
  `.cursor/scratchpad.md` and `.cursor/scratchpad.local.example.md` may be
  redundant; user proposes example-only baseline.
- User expectation is simpler install/update behavior while keeping deterministic
  automation behavior and no regressions in `/auto` phase/runtime controls.

## Discovery Notes — US-0073

- **Delivery decision**: Research and architecture must pick a single canonical
  installer baseline (`committed scratchpad.md` + example, or **example-only**
  with an explicit deterministic materialization path) and document the
  rationale; operators need a clear “what ships vs what is generated” contract.
- **Resolution semantics**: Any example-only model must define **merged
  scratchpad** precedence end-to-end (framework example, optional committed
  baseline if retained, user `.cursor/scratchpad.local.md`) so `/auto` and
  phase commands resolve the same flags as today — **no silent defaulting** when
  required keys are absent (`AC-2`, `AC-4`).
- **Upgrade and migration**: `--mode upgrade` and fresh install paths must
  apply the chosen policy consistently; legacy repos that already have both
  files need a deterministic migration or coexistence story without deleting
  user-owned locals (`AC-3`, `AC-5`, overlap with `US-0018` / `DEC-0039`).
- **Parity and evidence**: Installer entry points (`installer.ps1`, `.sh`,
  `.py`, CLI) and active/`template/` copies stay aligned; regression matrix
  must cover fresh install, upgrade from dual-file baseline, missing baseline
  recovery, and local override preservation (`AC-6`, `AC-8`, `AC-9`).
- **Non-regression**: Scope is delivery and config-resolution safety only — not
  removing automation controls or weakening fail-closed gates (`US-0072` triad /
  hot-surface contracts remain orthogonal).

## Intake Notes — US-0074

- User requests explicit cleanup of the remaining baseline failing checks that
  keep appearing as out-of-scope drift in QA reports.
- Focus areas are Homebrew/npm version-sync checks and installer/CLI
  `TEST_COMMAND` bootstrap checks; outcome target is a fully green baseline
  validation run for these known failures.

## Discovery Notes — US-0074

- **Named baseline set**: Discovery locks scope to the four asserts classified as
  non-blocking baseline debt in `sprints/S0051/qa-findings.md` (Homebrew URL tag,
  Homebrew `version` vs npm, installer `TEST_COMMAND` bootstrap, CLI missing-install
  `TEST_COMMAND` bootstrap); future QA for unrelated stories must not treat these
  as permanent noise once this story ships.
- **Version-sync contract**: The npm/`package.json` release line is the canonical
  semver source; the Homebrew stable formula (`packaging/homebrew/its-magic.rb`) must
  keep `url` tag, embedded `version`, and checksum lifecycle aligned with the same
  release the npm tarball/channel advertises (see also release/publish scripts in
  research).
- **`TEST_COMMAND` bootstrap**: Missing-install flows across `installer.ps1`,
  `installer.sh`, `installer.py`, and `bin/its-magic.js` must deterministically seed
  or refresh `TEST_COMMAND` in the target runbook when a stack is detectable,
  consistent with `DEC-0046` / `US-0063` precedence (user override wins; no silent
  blank where detection should apply).
- **Evidence and parity**: Regression fixes must land with active + `template/`
  parity, `tests/run-tests.*` / `tests/report.md` rows going green for all four
  checks, and operator-facing remediation notes so drift is diagnosable without
  re-triaging entire QA suites.

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

## Intake Notes — US-0075

- **Problem**: On upgrade, **`.cursor/scratchpad.md`** can change while
  **`.cursor/scratchpad.local.example.md`** does not, leaving operators without
  an up-to-date catalog to copy into **`.cursor/scratchpad.local.md`**.
- **Intent**: Treat **example** surfaces as the **primary** shipped documentation
  of new/changed scratchpad keys; keep them **in lockstep** with
  **`template/.cursor/scratchpad.local.example.md`** and refresh them on every
  upgrade path that touches scratchpad layers.
- **Success**: After upgrade, example bytes match template example; materialized
  baseline refresh never implies a **newer** key catalog in `scratchpad.md` than
  in example for the same release.
- **Constraints**: Preserve **DEC-0055** merge semantics and user-local file;
  no silent overwrite of **`.cursor/scratchpad.local.md`**.
- **Overlap**: Reasserts **US-0057** guarantees; closes reported drift under
  **US-0073** / Model B materialization ordering.
- **Refinement (2026-03-25)**: Beyond upgrade ordering, **both** scratchpad
  surfaces must list the **same** framework settings: e.g. **Team** block must
  appear in **`.cursor/scratchpad.md`** if it appears in the example, and
  **`.cursor/scratchpad.local.example.md`** must include every block present in
  the materialized file (**`/auto` role**, **phase selection**, **triad** caps
  `PO_TO_TL_*` / `ARCH_*`, etc.). Enforce with a **deterministic parity check**
  (**US-0075** **AC-11**).

## Discovery Notes — US-0075

- **Example-first operator contract**: After install or upgrade, **`.cursor/scratchpad.local.example.md`**
  must remain the **authoritative copy-from catalog** for framework keys; materialized
  **`.cursor/scratchpad.md`** must never advance to a **richer** documented key set than
  the example in the same release step (**DEC-0055** / **US-0073** ordering stays
  consistent with **AC-1** / **AC-3**).
- **Paired parity (AC-11)**: Beyond ordering, **both** shipped scratchpad surfaces must
  expose the **same** framework **section headers** and **`KEY=`** inventory (Team,
  `/auto` role/phase policy, triad **`STATE_*` / `PO_TO_TL_*` / `ARCH_*`**, and the rest),
  with **`template/`** mirrors held to the same rule so skew cannot re-enter via packaging.
- **Parity check UX**: Failures must be **deterministic** and **operator-actionable**
  (path pair, missing section or key, remediation: align to template pair, re-run upgrade,
  verify manifest paths) — no silent drift.
- **Non-goals for discovery**: No change to merged-scratchpad value precedence
  (**DEC-0055**) except where required to fix refresh **ordering**; **`.cursor/scratchpad.local.md`**
  remains user-owned and untouched by framework refresh (**AC-5**).
- **Research handoff**: Extend **`R-0052`** with concrete file-level refresh ordering,
  manifest path evidence, and a minimal **parity schema** (what counts as a “framework key”
  for the deterministic check) before **`/architecture`**.

## Intake Notes — US-0076

- **Problem**: Operators set **`SYNC_POLICY_MODE`**, **`ALLOW_AUTO_PUSH=1`**, and
  **`AUTO_PUSH_BRANCH_ALLOWLIST`** and expect **git push**; the kit today treats those
  mainly as **workflow policy** (**US-0038**) while **`validate-and-push`** does not read
  scratchpad — so **nothing pushes** unless they run push scripts manually without that
  linkage.
- **Intent**: **Wire** merged scratchpad into an **executable**, **opt-in** push path that
  honors the **same gate chain** (tests, branch allowlist, QA safety) with **deterministic
  reason codes**; **no push** when flags are off or gates fail.
- **Success**: Running the documented command after a phase (or from CI) **respects**
  scratchpad sync settings and either pushes with evidence or exits with a **known**
  **`US-0038`** reason code.
- **Constraints**: Do not weaken **US-0038**; **US-0071** safe CLI strings; cross-platform
  **PS1** / **sh** parity.
- **Alternative**: Prefer extending **`validate-and-push`** over many new entrypoints unless
  architecture mandates a split (**`/architecture`** decides).

## Discovery Notes — US-0076

- **Validated gap**: **`validate-and-push`** does not read merged scratchpad for **`ALLOW_AUTO_PUSH`**
  / **`SYNC_*`** while operators expect those flags to govern an executable push path; aligns with
  **R-0053** and **US-0038** policy-only documentation today.
- **Delivery shape**: Keep a **single story** slice — extend **`validate-and-push.ps1`/`.sh`** (and
  shared logic) unless **/architecture** documents a security-driven split; preserve **PS1**/**sh**
  parity (**AC-6**).
- **Merge contract**: Runtime reads must follow **DEC-0055** (local > materialized baseline >
  example) for sync and push keys; parse failures remain **fail-closed** with remediation (**AC-2**).
- **Scheduling semantics**: For **`by_phase`** / **`by_milestone`**, the script has no implicit
  workflow phase — **explicit invocation** (operator or CI) is the boundary signal; **Cursor** does
  not auto-run the push script unless separately documented as an optional hook (**boundaries** in
  backlog).
- **QA safety**: Blocking vs safe-to-push rule is **architecture-bounded** per **AC-5** (minimum:
  respect sprint **`qa-findings`** or equivalent when present); avoid false confidence in logs
  (**R-0053** risks).
- **Progression**: No open **product** decision gate before **/research**; **R-0053** is the current
  research anchor for TL follow-on.

## Intake Notes — US-0077

- **Problem**: Auto-maintained documentation currently reads too technical for many users,
  especially in README surfaces that mix operator, workflow, and engineering detail.
- **Intent**: Add deterministic profile controls so teams can choose **audience**
  (`user|developer|both`) and **detail depth** (`concise|balanced|technical-deep`) without
  creating conflicting docs.
- **Success**: Generated/updated docs match selected profile style and required sections, and
  release-time checks can prove completeness for the selected profile.
- **Constraints**: Preserve existing optional contracts (**US-0031** spec-pack, **US-0032**
  user-guide, **US-0030** README/runbook parity, **US-0071** user-visible metadata hygiene).
- **Alternative**: Keep a single README with lighter wording only; preferred path is explicit
  audience/depth profile semantics to avoid long-term drift.

## Discovery Notes — US-0077

- **Profile contract**: `DOC_AUDIENCE_PROFILE` and `DOC_DETAIL_LEVEL` remain the minimal,
  backward-compatible control pair; values must fail closed with reason codes and
  remediation (**backlog AC-1**).
- **Audience split model**: Prefer an explicit **dual-doc / ownership-matrix** approach
  (README vs developer doc vs pointers into `docs/**`) over wording-only edits to a single
  README — aligns with **R-0054** (Diataxis-style intent separation) and reduces drift
  against optional **US-0032** guides and **US-0031** spec-pack.
- **Bloat control**: `both` + `technical-deep` requires **bounded section budgets** and/or
  deterministic split files so operator surfaces do not grow without limit (**R-0054**
  risks).
- **Validation**: Profile completeness checks must be **deterministic per profile cell**
  (required headings/sections) and integrate with **US-0030** README/runbook/template
  parity expectations.
- **Hygiene**: User-visible generated text stays within **US-0071** guardrails; internal
  planning tokens belong in engineering artifacts and comments only.
- **Research progression**: Extend **R-0054** post-discovery with concrete artifact paths,
  mandatory section matrix, and scoped regression strategy for the profile grid (**AC-8**).

## Intake Notes — US-0078

- **Problem**: Intake can report question-pack completion and `assumptions_confirmed` without
  explicit in-session questioning/confirmation evidence, reducing trust in **US-0068** fail-closed guarantees.
- **Intent**: Require verifiable interaction evidence before persistence for mandatory question
  packs; otherwise fail closed with deterministic reason codes and remediation prompts.
- **Success**: Intake persists only when required topic coverage and any assumption confirmations
  are evidence-backed and auditable.
- **Constraints**: Preserve guided/low-touch behavior patterns while enforcing **US-0068**,
  **US-0051**, and **US-0059** contracts.
- **Alternative**: Keep policy-only declarations with no runtime evidence checks; rejected as non-verifiable.

## Discovery Notes — US-0078

- **Evidence contract**: Persistence must require a deterministic **per-required-topic** evidence pointer
  (`answer_ref` / equivalent) or an **explicit assumption-confirmation ref**; missing coverage fails closed
  per **`INTAKE_REQUIRED_TOPIC_MISSING`** / **`INTAKE_REQUIRED_PACK_INCOMPLETE`** — aligns with **`R-0055`**.
- **Assumption integrity**: **`assumptions_confirmed=yes`** (or equivalent) is invalid without in-session
  confirmation evidence; otherwise **`INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`** — extends **`US-0068`** /
  **`DEC-0050`** with verifiable semantics.
- **Artifact fields**: Persisted intake output should distinguish **`asked_topics`** from
  **`answered_topics`** (or parallel evidence) so audits can see questioning vs satisfied coverage
  (**backlog AC-4**).
- **Mode parity**: **Guided** mode keeps bounded prompts but cannot auto-satisfy required topics without
  evidence-backed assumptions; **low-touch** (`INTAKE_GUIDED_MODE=0`) stays lightweight yet still blocks
  persistence when mandatory pack coverage is unproven (**backlog AC-5 / AC-6**).
- **Research progression**: Finalize interaction-event / parser contract, exact field literals, and **AC-8**
  regression matrix in **`R-0055`** (or successor amendment) before **`/architecture`** locks **DEC**
  intake-evidence model.

## Intake Notes — US-0079

- **Problem**: Bug reports are currently handled like normal user stories, which mixes defect
  fixing with feature intent and weakens bug-focused traceability.
- **Intent**: Add a first-class bug issue workflow distinct from user stories while keeping
  lifecycle simple (`OPEN`/`DONE`) as requested.
- **Success**: Intake routes bug reports into bug issues with reproducible fields and consistent
  links through sprint, QA, verify-work, and release artifacts.
- **Constraints**: Follow lightweight policy — no mandatory severity/SLA/triage states; preserve
  existing US workflow and status reconciliation behavior.
- **Alternative**: Keep all bug reports as `US-xxxx`; rejected due domain mismatch between defects
  and feature stories.
- **Intake gate (2026-03-29, PO, `orchestrator_run_id=auto-20260329-01`)**: **`small-intake-pack`**
  evidence validated (**`handoffs/intake_evidence/US-0079-intake-20260329.json`**, **`DEC-0060`**
  **`ie:`** refs); **`/discovery`** complete **`2026-03-29`**; next workflow phase **`/research`**.

## Discovery Notes — US-0079

- **Entity split**: Defects are tracked as **`BUG-xxxx`**, not **`US-xxxx`**, with the same artifact-first discipline; feature stories and bug issues remain distinct for traceability and reconciliation.
- **Lifecycle**: **`OPEN`** and **`DONE`** only — optional labels or narrative severity may appear as text, but no mandatory triage state machine.
- **Storage preference (discovery)**: Keep canonical bug status alongside story status in **`docs/product/backlog.md`** under an explicit bug region unless file growth forces a split (**architecture** confirms).
- **Routing**: Intake or a dedicated path must **classify** bug vs feature before persistence so defects do not default into story intake.
- **Minimum fields**: Environment/context, steps, expected, actual, and evidence refs are required for actionable bugs (**R-0056**).
- **Safety**: Extend **`US-0045`** reconciliation and **`/ask`** retrieval to both ID families without weakening existing US semantics; document duplicate-tracking guardrails in **DEC** (**AC-10**).

## Research Notes — US-0079

- **Design direction**: First-class **`BUG-####`** with **`OPEN`/`DONE`** only; canonical **`## Bug issues (canonical)`** in **`docs/product/backlog.md`** unless architecture triggers file split (**`R-0056`**).
- **Routing**: Explicit bug work-item kind (command and/or scratchpad key per **DEC**) — defects must not default into **`US-xxxx`** without operator signal.
- **Validation**: Minimum fields **environment**, **steps_to_reproduce**, **expected**, **actual**, **evidence_refs**; Tier A–D tests in **`R-0056`** map to **AC-1..AC-10**.
- **Next**: **`/architecture`** locks **DEC**, allocator, reconciliation, and validator hooks.

## Architecture Notes — US-0079

- **Normative lock**: **`DEC-0061`** + **`architecture.md`** **`# US-0079`** — scratchpad **`INTAKE_WORK_ITEM_KIND`** (`story`|`bug`) and/or **`/intake bug`**; **`INTAKE_BUG_ROUTING_REQUIRED`** / mismatch family when defect prose lacks bug signal; **`## Bug acceptance (canonical)`** in **`docs/product/acceptance.md`**; optional **`bug_ids`** CSV on **`state.md`** phase boundaries when bugs mutate (**US-0070** visibility).
- **Next**: **`/sprint-plan`** maps **AC-1..AC-10** to tasks under **`DEC-0061`** / **`R-0056`**.

## Intake Notes — US-0080

- **Problem**: Orchestrated runs can accumulate very high `cache read` token volume versus input/output,
  especially in long chats with repeated large command prefixes.
- **Intent**: Harden token-cost behavior with measurable targets by slimming repeated command/context
  payloads while preserving all mandatory quality/safety gates.
- **Success**: Comparable `/auto` runs show a measurable cache-read reduction target (50% goal) with
  no regressions in phase contracts and release gates.
- **Constraints**: Keep US-0048/US-0056/US-0069/US-0039 enforcement intact; no quality gate removal.
- **Alternative**: Rely only on `TOKEN_PROFILE=lean` without structural slimming; rejected as insufficient.
- **Intake closure (2026-03-29, PO, orchestrator_run_id=auto-20260329-02)**: **`small-intake-pack`** evidence validated (**`handoffs/intake_evidence/US-0080-intake-20260329.json`**, **`DEC-0060`** **`ie:`** refs); next workflow phase **`/discovery`**.

## Discovery Notes — US-0080

- **Validated drivers**: Cache-read volume scales with **prefix size × call count** in long threads; structural slimming and **bounded phase-context surfaces** are the primary levers (**`R-0057`**).
- **Constraints**: Preserve isolation, strict-proof, role/phase, and release contracts — token savings cannot bypass **`US-0048`**, **`US-0056`**, **`US-0069`**, **`US-0039`**.
- **Research handoff**: Lock **comparable-run** definition (story class / profile / phase plan) for AC-1/AC-2; decide auditable **evidence channel** for per-run token metrics; enumerate **command + template** touchpoints for AC-3/AC-9.
- **Discovery closure (2026-03-29, PO, orchestrator_run_id=auto-20260329-02)**: Discovery complete; next workflow phase **`/research`**.

## Research Notes — US-0080

- **Vendor alignment**: Prompt caching cost drivers match **prefix × calls**; usage reporting separates
  cache read vs cache creation vs ordinary input tokens (see **`R-0057`** Anthropic source).
- **Comparable runs**: Compare only within the same declared **run-class tuple** (story, **`TOKEN_PROFILE`**,
  **`SECURITY_REVIEW`**, materialized phase plan, resume anchor) — hash for baseline stability.
- **Evidence**: Prefer committed **append-only** run metric files + **`state.md`** pointer; IDE usage as
  secondary.
- **Parity**: Slimming must cover **active + `template/`** command/rule surfaces with CI-enforced lists.
- **Research closure (2026-03-30, tech-lead, orchestrator_run_id=auto-20260329-02)**: Research complete;
  **`/architecture`** satisfied **2026-03-29** — **`DEC-0062`** / **`# US-0080`** (**`R-0057`**).

## Architecture Notes — US-0080

- **Normative lock**: **`DEC-0062`** + **`docs/engineering/architecture.md`** **`# US-0080`** — metric literals
  (**`cache_read_tokens`**, **`input_tokens`**, **`output_tokens`**, **`phase_call_count`**, optional
  **`cache_creation_tokens`**), **`run_class_hash`** for comparable runs, append-only
  **`handoffs/token_cost_runs/`** + **`token_cost_evidence_ref`**, parity manifest for slimmed surfaces,
  AC-10 trade-offs; gates **`US-0048`**, **`US-0056`**, **`US-0069`**, **`US-0039`** non-negotiable.
- **Architecture closure (2026-03-29, tech-lead, orchestrator_run_id=auto-20260329-02)**: Architecture
  complete; next workflow phase **`/sprint-plan`**.

## Intake Notes — US-0081

- **Problem**: A broad first intake can still end as one narrow story, leaving parts of the original full software plan uncovered.
- **Intent**: Require complete plan-area coverage mapping at first broad intake persistence (mapped to stories or explicitly deferred with rationale).
- **Success**: First broad intake outputs a complete story map for the submitted plan while preserving phased delivery.
- **Constraint**: Do not force all mapped stories into one sprint; this is an intake completeness contract, not execution batching.
- **Intake closure (2026-03-31, PO, manual run)**: **`small-intake-pack`** evidence validated in
  **`handoffs/intake_evidence/US-0081-intake-20260331.json`**; next workflow phase **`/discovery`**.

## Intake notes — BUG-0001

- **Defect**: Packaged **`template/scripts/`** omits **`intake_*`** modules present under repo **`scripts/`**, so installs in other repos lack mandatory **`/intake`** validator/routing tooling (**`DEC-0060`**/**`DEC-0061`** gates).
- **Scope**: Required **install completeness** for intake-critical scripts only — not wholesale active/`template/` mirroring (**user constraint**).
- **Evidence**: **`handoffs/intake_evidence/BUG-0001-intake-20260330.json`** (**`small-intake-pack`**, **`[INTAKE_EVIDENCE_VALIDATION_OK]`**); research **`R-0058`** (npm **`files`**/`template/` tarball semantics).
- **Intake closure (2026-03-30, PO, `orchestrator_run_id=manual-20260330-BUG0001`)**: Canonical **`BUG-0001`** filed; next workflow phase **`/discovery`** (TL).
- **Discovery closure (2026-03-30, PO, `orchestrator_run_id=auto-20260330-01`)**: Confirmed **`template/scripts/`** has eight non-intake modules vs three **`scripts/intake_*.py`**; **`package.json`** **`files`** ships **`template/`** + **`scripts/doc_profile_lib.py`** only — **`BUG-0001`** **OPEN**; next **`/research`** (TL).
- **Research closure (2026-03-30, TL, `orchestrator_run_id=auto-20260330-01`)**: **`R-0058`** extended — minimal copy set = three **`intake_*`** files; installers hydrate from **`template/`** only; parity across npm/Choco/Brew ties to **`template/`** tree. **`BUG-0001`** **OPEN**; next **`/architecture`** (TL) — see **`docs/engineering/state.md`** **Research checkpoint (2026-03-30) — BUG-0001 / auto-20260330-01**.
- **Architecture closure (2026-03-30, TL, `orchestrator_run_id=auto-20260330-01`)**: **`DEC-0063`** + **`architecture.md`** **`# BUG-0001`** — minimal **`template/scripts/`** mirror, **`files`** policy, parity tests, **`US-0018`**. **`BUG-0001`** **OPEN**; next **`/sprint-plan`** (TL) — see **`docs/engineering/state.md`** **Architecture checkpoint (2026-03-30) — BUG-0001 / auto-20260330-01**.
- **Sprint-plan closure (2026-03-30, TL, `orchestrator_run_id=auto-20260330-01`)**: Sprint **`S0060`** materialized (**`sprints/S0060/*`**); **`BUG-0001`** **OPEN**; next **`/plan-verify`** — see **`docs/engineering/state.md`** **Sprint-plan checkpoint (2026-03-30) — BUG-0001 / S0060 / auto-20260330-01**.

## Intake notes — BUG-0002

- **Reclassification**: Initial report captured as defect-shaped, later clarified as expectation mismatch (manual command vs desired automatic map availability).
- **Closure**: `BUG-0002` is closed as workflow expectation mismatch and linked to enhancement story **`US-0082`**.

## Intake Notes — US-0082

- **Problem**: Agents in fresh repos may miss codebase context because `codebase-map.md` generation relies on an explicit manual `/map-codebase` step.
- **Intent**: Add deterministic TL/Dev (or equivalent) ownership so codebase map is reliably created/refreshed for agent context without user guesswork.
- **Success**: Fresh lifecycle path guarantees `docs/engineering/codebase-map.md` exists (or deterministic diagnostics explain why not), while manual `/map-codebase` remains valid.
- **Constraint**: Keep map generation idempotent and ownership-safe; maintain active/template parity and avoid noisy rewrites.
- **Intake closure (2026-03-31, PO, manual run)**: **`small-intake-pack`** evidence validated in
  **`handoffs/intake_evidence/US-0082-intake-20260331.json`**; next workflow phase **`/discovery`**.
- **Orchestrated intake closure (2026-03-31, PO, `orchestrator_run_id=auto-20260331-02`)**: Reaffirms the same evidence bundle; backlog **OPEN** unchanged (**US-0045**); next **`/discovery`**.

## Intake Notes — US-0083

- **Problem**: Intake questions can feel rigid/repetitive and often block on missing fields even when the user prefers to delegate unclear decisions.
- **Intent**: Keep context-aware clarification and safety challenge behavior, but allow explicit user delegation for unresolved topics.
- **Success**: Intake can proceed without hard blocking when user explicitly delegates, while non-delegated missing required topics still fail closed.
- **Constraint**: Delegation must be explicit and evidence-bound; no silent assumption bypass.
- **Intake closure (2026-03-31, PO, manual run)**: **`small-intake-pack`** evidence validated in
  **`handoffs/intake_evidence/US-0083-intake-20260331.json`**; next workflow phase **`/discovery`**.

## Discovery Notes — US-0083

- **Discovery closure (2026-03-31T22:46:01Z, PO, `orchestrator_run_id=auto-20260331-04`)**: Delegation remains opt-in and topic-scoped; unresolved required topics without explicit delegation remain fail-closed.
- **Research asks**: finalize deterministic delegated-topic evidence shape (`ie:`-compatible refs + rationale/confidence), validator branching semantics for delegated vs non-delegated unresolved topics, and guided/low-touch parity diagnostics.
- **Status authority**: backlog remains canonical; **`US-0083`** stays **OPEN** (**US-0045**).

## Intake notes — BUG-0003

- **Defect**: Missing scripts still occur after install/upgrade with modes `missing` or `upgrade`.
- **Scope**: Installer mode-specific completeness regression/gap across script payload installation.
- **Evidence**: **`handoffs/intake_evidence/BUG-0003-intake-20260331.json`** and **`handoffs/intake_evidence/BUG-0003-intake-20260331-b.json`** (`small-intake-pack`, DEC-0060 `ie:` refs), plus installer and template script surfaces.
- **Addendum**: user-provided concrete missing file after new-repo install: `scripts/enforce-triad-hot-surface.py`.
- **Intake closure (2026-03-31, PO, manual run)**: Canonical **`BUG-0003`** filed; next workflow phase **`/discovery`** (TL).
