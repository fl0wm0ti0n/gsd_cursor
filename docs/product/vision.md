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
- **Version-scoped release changelog**: a cumulative semver changelog and per-version release docs list shipped **US-xxxx** / **BUG-xxxx** work with short summaries; GitHub/git publish paths attach the same canonical bodies (Keep a Changelog + **`gh release create -F`** best practice).
- **Release queue visibility**: unreleased and released sprints are tracked in a canonical queue so pending release work is always explicit.
- **Backlog-release consistency**: released sprint evidence and backlog status/AC checks are deterministically reconciled to prevent stale OPEN stories after completion.
- **Single-source status trust**: backlog is the canonical story-status source, and acceptance/state artifacts are deterministically reconciled to prevent OPEN/DONE drift.
- **Spec-pack ready**: teams can optionally require Design Concept, CRS, and Technical Spec artifacts with near-zero overhead when disabled.
- **User-guide ready**: teams can optionally require user-friendly per-feature instructions with near-zero overhead when disabled.
- **Cross-repo aware**: optional observability can track module/API compatibility across repos and surface contract drift before release decisions.
- **Component-scoped safety**: optional scoped execution can focus work on selected components while explicitly protecting unaffected components.
- **Remote-ready by configuration**: optional remote execution uses a canonical `.cursor/remote.json` contract with fail-fast validation when enabled and zero overhead when disabled.
- **Linux-host installer reliability**: globally published `its-magic` shell entrypoints remain POSIX-safe under `/bin/sh` (including dash) on SSH and container hosts; published artifacts stay aligned with repo sources.
- **Linux/Docker test ergonomics**: dev and QA can aim checks at WSL, SSH Linux hosts, or Docker contexts through documented, automatable configuration that composes with existing remote connectivity contracts—without ad-hoc connection strings in the repo.
- **Operator `.env` for connectivity secrets**: optional repo-root **`.env`** (gitignored) can hold values for env vars referenced by **`.cursor/remote.json`** and **release-targets** operator flows, with a committed **`.env.example`** (names only) and explicit **keep-out-of-AI-context** rules—without putting secrets in git or in tracked JSON.
- **Automation-only remote targeting**: when explicitly enabled for CI/DI/QA/dev/release, agents and workflows can deterministically choose Docker, SSH, or other declared targets from canonical remote config—and resolve explicit “start container \<target\>” phrasing—without burdening manual daily work.
- **Targeted bug automation**: when explicitly enabled, `/auto` can run the full defect lifecycle for one `BUG-####` or a bounded queue of OPEN bugs—without conflating defect work with story backlog drain.
- **Drop-in installer**: one command installs the entire workflow into any repo.
- **Multiplatform**: available via npm, Chocolatey, and Homebrew.
- **Voice-friendly**: multilingual voice input as a first-class input layer.
- **Security-aware**: optional compliance review (GDPR, SOC2, HIPAA, PCI-DSS, ISO27001) at design and code level — zero overhead when disabled.
- **Knowledge-first decisions**: PO and architect research external docs, APIs, and best practices before deciding — curated knowledge persists across sessions and agents.
- **Adaptive intake depth**: guided intake can proactively ask clarifying questions and suggest options, or run low-touch mode via a switch when teams prefer direct capture.
- **Optional Caveman voice (Cursor)**: teams can enable a terse, token-efficient assistant style via scratchpad flags (**default off**) without losing workflow gates; an optional follow-on path can add **safe, reversible** file compression for agent-read scope only when explicitly enabled.

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

## Intake notes — BUG-0004

- **Defect**: Shell-path installer fails immediately with `/usr/lib/node_modules/its-magic/installer.sh: 2: set: Illegal option -` when running `its-magic --mode missing`.
- **Scope**: Shell/runtime compatibility of installer startup options and CLI execution path in Linux environments.
- **Evidence**: **`handoffs/intake_evidence/BUG-0004-intake-20260403.json`** (`small-intake-pack`, DEC-0060 `ie:` refs), reported runtime output, and affected installer surface `installer.sh`.
- **Intake closure (2026-04-03, PO, manual run)**: Canonical **`BUG-0004`** filed as **OPEN**; next workflow phase **`/discovery`** (TL).

## Intake notes — BUG-0005

- **Defect**: `/auto` fails immediately after bug intake with stale resume target (`AUTO_RESUME_ERROR` / `RESUME_BRIEF_STALE`) instead of continuing workflow.
- **Scope**: Intake-to-auto continuation consistency, resume-source freshness handling, and deterministic boundary progression for bug-mode intake.
- **Evidence**: **`handoffs/intake_evidence/BUG-0005-intake-20260403.json`** (`small-intake-pack`, DEC-0060 `ie:` refs), user report, and stale `handoffs/resume_brief.md` posture after `BUG-0004` intake.
- **Intake closure (2026-04-03, PO, manual run)**: Canonical **`BUG-0005`** filed as **OPEN**; next workflow phase **`/discovery`** (TL).

## Intake notes — BUG-0006

- **Defect**: `/auto` can execute phase work without spawning the required fresh role subagent.
- **Scope**: Enforce strict phase dispatch integrity so orchestrator-only phase execution is blocked with deterministic fail-fast reason-code coverage.
- **Evidence**: **`handoffs/intake_evidence/BUG-0006-intake-20260403.json`** (`small-intake-pack`, DEC-0060 `ie:` refs), user report, and `/auto` orchestrator contract in `.cursor/commands/auto.md`.
- **Intake closure (2026-04-03, PO, manual run)**: Canonical **`BUG-0006`** filed as **OPEN**; next workflow phase **`/discovery`** (TL).

## Intake notes — BUG-0007

- **Defect**: Intake evidence records that required questions were asked and answered even when the user reports no such questions were asked.
- **Scope**: Truthful asked-vs-covered intake evidence accounting (`asked_topics`, `topic_coverage`) with fail-closed handling when required topics are not actually collected.
- **Evidence**: **`handoffs/intake_evidence/BUG-0007-intake-20260403.json`** and user-provided example **`handoffs/intake_evidence/BUG-0006-intake-20260403.json`**.
- **Intake closure (2026-04-03, PO, manual run)**: Canonical **`BUG-0007`** filed as **OPEN**; next workflow phase **`/discovery`** (TL).

## Discovery Notes — US-0085

- **`.env`-as-secret-carrier pattern** is well-established in the Node/Python ecosystem
  (`.env` in `.gitignore`, `.env.example` committed). In AI coding assistant contexts
  (Cursor, Claude Code, Copilot, Aider) the pattern requires an **additional exclusion
  layer**: agents can read any file the developer can, so `.gitignore` alone is
  insufficient. Market practice (2026) includes:
  - **`.cursorignore`** / custom agent exclusion rules to prevent IDE file-context
    ingestion of `.env`.
  - **Instruction-based guardrails** (`AGENTS.md`, `.cursorrules`, Cursor rules)
    telling agents explicitly: "do not open, search, or attach `.env`."
  - **Defense-in-depth**: zero-disk secret management (Doppler, Infisical, 1Password CLI
    `op run`, `dotenvx`) is preferred in teams; repo-level `.env` remains common for
    solo/small-team operator flows.
- **Kit-specific scope**: US-0085 stays within the **operator-local `.env`** pattern
  (gitignored, agent-excluded, operator-sourced); `.env.example` committed with
  **names only**; no inline secrets in tracked JSON (`release-targets.json`,
  `remote.json`). Agents may run commands (`ssh`, `python scripts/remote_config_summary.py`)
  when the operator has already exported env vars into the shell.
- **Template parity**: `.env.example`, `.gitignore` entries, `.cursorignore` (or
  equivalent), runbook procedure, `runtime-connectivity.md` addendum, `us-0084-remote-e2e.md`
  references, and agent/rule text must ship in both active and `template/` copies.
- **AC-8 helper decision**: Architecture may choose a small deterministic
  `scripts/print_remote_env_hint.py` (names-only, no values) or document shell-only
  sourcing with no helper — either is acceptable per acceptance.
- **Security posture**: No credentials in git; `.env` loading is operator-controlled;
  agents never read `.env`; SSH keys/passwords via agent/env references only.

## Discovery Notes — US-0086

- **Automation-only targeting**: Remote target selection is an explicit automation capability for dev/CI/DI/QA/release, not a default manual workflow requirement.
- **Manual default remains local-first**: When automation profile is off, operators keep existing local behavior with zero new mandatory remote setup overhead.
- **Deterministic intent routing**: Explicit operator phrase "start container `<target_id>`" should resolve to canonical `targets[].id` with fail-closed unknown-target diagnostics.
- **Security continuity with US-0085**: Automation can use env already loaded into shell but must never read `.env` directly and must never emit secret values in logs/handoffs.
- **Research lock needed next**: `/research` should finalize routing heuristics (changed files + explicit intent), evidence fields for handoffs, and reason-code taxonomy before `/architecture`.

## Intake notes — US-0088

- **Intent**: **`/auto`** should run **all scheduled phases** until a **user story** or **sprint segment** is **done**, with **`AUTO_BACKLOG_DRAIN=1`** continuing across stories **quietly** except **gates**, **errors**, **missing inputs**, **pause**, and **loop max** — closing the gap where implementations often **stop after one phase** and drain is **unreliable**.
- **Scope**: Normative alignment to **`docs/engineering/auto-orchestration-reference.md`** **Step 5** (**US-0080 / DEC-0062** umbrella), contract tests, runbook + template parity, optional **`AUTO_QUIET`** (or profile composition).
- **Evidence**: **`handoffs/intake_evidence/US-0088-intake-20260407.json`**; research stub **`R-0071`**.
- **Intake closure (2026-04-12, PO, Cursor)**: Backlog **`US-0088`** **OPEN**; next workflow phase **`/discovery`** (TL).

## Intake Notes — US-0089 / US-0090

- **Intent**: Bring **Caveman-style** terse communication (see external pattern **`JuliusBrussee/caveman`**) into **Cursor** usage of this kit — **best effort** alignment, **scratchpad-configured**, **default off**, **no regression** in existing automation when disabled. Optional **second story** explores **input-side** file compression with **original preserved** and **hard deny** for canonical/evidence artifacts.
- **Split**: **US-0089** = response style + scratchpad + rules/skill + tests + architecture; **US-0090** = optional compression scripts + guards + runbook — **gated** after **US-0089**.
- **Evidence**: **`handoffs/intake_evidence/US-0089-intake-20260414.json`** (**`[INTAKE_EVIDENCE_VALIDATION_OK]`**); research stub **`R-0073`**.
- **Intake closure (2026-04-14, PO, Cursor)**: Backlog **`US-0089`**, **`US-0090`** **OPEN**; next **`/discovery`** for **`US-0089`** (then **`US-0090`**).

## Discovery Notes — US-0089

- **Operator value proposition**: Operator-configurable terse assistant voice (Caveman-style) **reduces response-side token cost and cognitive clutter** in Cursor chats while preserving **all** machine-verifiable substance (reason codes, AC checklists, paths, IDs). The feature is **default off** — zero change for operators who do not opt in — and **toggleable in-session** via documented phrases so an operator can shift voice without editing the scratchpad mid-task.
- **Product-facing messaging constraints**:
  - **No hidden internal IDs in user channels** (reaffirm **US-0071**): Caveman voice **must not** drop visible **`US-xxxx`** / **`DEC-xxxx`** / **`R-xxxx`** / **`BUG-####`** / **`S-xxxx`** references that operators rely on. Terseness applies to **prose**, not to traceable identifiers or reason codes.
  - **Default-off guarantee**: with **`CAVEMAN_MODE=0`** (or key absent), normative command strings, gate ordering, spawn-only language (**BUG-0006**), and existing contract tests remain **byte-compatible**. Opt-in is explicit.
  - **Non-substitution of `TOKEN_PROFILE`**: Caveman is a **voice** layer; **`TOKEN_PROFILE`** (**US-0080**) is a **context-breadth** layer. Docs must state these are **orthogonal**, and `CAVEMAN_MODE=1` does **not** imply `TOKEN_PROFILE=lean`.
  - **Gate language preserved**: decision gates, errors, `[BUG_VALIDATION_OK]`, `[INTAKE_EVIDENCE_VALIDATION_OK]`, `blocked`, `missing input`, `pause`, and `loop_max` notifications remain **verbatim** even when Caveman is on (carryover from **US-0088 / `AUTO_QUIET`** non-suppressible list).
  - **Operator control phrasing**: documented, deterministic phrases (e.g. "enable caveman" / "disable caveman" / "stop caveman" / "normal mode") map to session toggles with predictable behavior; exact wording will be architecture-locked in **`# US-0089`**.
- **Scope boundary for messaging**: the **output-style** contract lives entirely in this story. Optional **input-side** compression (file reads, sidecar originals, deny lists) is deferred to **US-0090** and **must not** be surfaced as a Caveman capability in user-facing docs until that story ships.

## Intake Notes — US-0091

- **Problem**: Root `README.md` and the developer shard can lag behind shipped user-visible capabilities even when `US-0030` passes — the delta gate only fires when commands/flags **change**, not when a feature shipped without an initial README blurb.
- **Intent**: One-time audit + backfill across root `README.md`, `template/README.md`, and `docs/developer/README.md`, then a **blocking** static-coverage validator composed into `/release` so drift cannot recur.
- **Operator scope (2026-05-10)**: `scope_files=both`, `audience_focus=both_profiles`, `feature_set=user_visible`, `drift_guard=blocking`, `story_split=single`, `priority=P1`.
- **Evidence**: `handoffs/intake_evidence/US-0091-intake-20260510.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`); research anchor **`R-0074`**.
- **Intake closure (2026-05-10, PO)**: Backlog **`US-0091`** **OPEN**; next **`/discovery`**.

## Discovery Notes — US-0091

- **Operator value proposition**: Operators and downstream kit consumers see a **complete, trustworthy catalog** of what its-magic can do — commands, flags, scratchpad modes, and operator-affecting fixes — without hunting backlog prose. After backfill, `/release` **fails closed** when a shipped user-visible item lacks a README-family description, so documentation debt cannot silently accumulate again.
- **Product-facing messaging constraints**:
  - **Dual-audience split preserved** (**DEC-0059**): operator blurbs stay in root `README.md` under existing H2 vocabulary (`Features`, `Commands and workflow`, `Other useful capabilities`, etc.); developer traceability rows stay in `docs/developer/README.md` under `DEV_*` H2 literals — **no new H2s** for backfill (section budgets via `validate_doc_profile.py` remain authoritative).
  - **Terseness over encyclopedic guides**: backfill is **1–2 sentences per feature** plus optional command/flag tokens — not per-feature user guides (`USER_GUIDE_MODE` / **US-0032** remain orthogonal).
  - **Traceability without internal jargon** (**US-0071**): root blurbs stay operator-readable; DEV shard rows may cite `US-xxxx` / `DEC-xxxx` / scratchpad keys for implementers. No planning tokens (`orchestrator_run_id`, `fresh_context_marker`, etc.) in operator blurbs.
  - **Remediation vocabulary**: blocking failures use umbrella **`README_FEATURE_COVERAGE_BLOCKED`** with deterministic sub-codes (`README_FEATURE_COVERAGE_GAP:<US-xxxx|BUG-xxxx>`, parity/profile/input variants per acceptance) and point to the missing audience surface (root bullet vs DEV row).
  - **Grandfathering contract**: first activation of the blocking gate ships **in the same sprint** as the backfill — no retroactive `/release` block on currently DONE items until the catalog is populated (**AC-10**).
- **Predicate contract (discovery-locked for `/research`)**:
  - **Canonical input**: optional backlog block field **`user_visible: true|false`** per `## US-xxxx` / `### BUG-####` (validator reads backlog, not acceptance prose).
  - **In-scope when**: status **DONE** and `user_visible: true` (explicit) — or, during one-time migration only, unset field passes a bounded heuristic (slash-command / scratchpad-key / CLI-flag / runbook operator-action signals in backlog summary or acceptance title).
  - **Out-of-scope when**: `user_visible: false` or pure-internal invariant surface (template parity guards, archiver mechanics, schema-only validators with no operator action).
  - **Ambiguous** unset + heuristic tie → **`README_FEATURE_COVERAGE_INPUT_INVALID`** (fail closed).
  - **Acceptance row**: optional human suffix `(user_visible)` allowed for portfolio scan; **not** parsed by the validator.
- **Coverage anchor contract**: each in-scope item must be detectable in the README family — root bullet or sub-entry naming the command/flag/capability **or** containing the `US-xxxx`/`BUG-xxxx` id; DEV shard row linking id + relevant scratchpad flags. Placement follows **section affinity** (commands → `Commands and workflow`; modes/flags → `Commands and workflow` or `Other useful capabilities`; install/distribution → `Features`; dev governance → `Workflow` / `Quality gates` / `Engineering decisions`).
- **Composition boundaries**: **`US-0030`** delta gate unchanged; **`US-0091`** adds a **second static-coverage check** in the same `/release` doc-gate surface. **`US-0017`** owns byte parity; **`US-0077`** owns profile cells — this story **populates** them only.
- **Research asks**: finalize migration heuristic table, validator CLI/`--report` schema, release-gate wiring point, grandfathering toggle, and section-affinity manifest before **`/architecture`** locks **`DEC-xxxx`** companion.

## Intake notes — BUG-0009

- **Problem**: its-magic copies its **own** self-packaging GitHub Actions CI into every generated repo, so `npm-test`/`brew-test`/`choco-test` fail in downstream projects that lack `package.json`, `installer.sh`, and `packaging/chocolatey`.
- **Operator scope (2026-06-06)**: fix new installs/upgrades; existing repos heal on next upgrade; also harden generic `checks` for fresh projects with no real tests yet.
- **Evidence**: `handoffs/intake_evidence/BUG-0009-intake-20260606.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`); operator CI logs from `finance_goblin`.
- **Intake closure (2026-06-06, PO)**: Backlog **`BUG-0009`** **OPEN**; next **`/discovery`**.

## Intake notes — BUG-0010

- **Problem**: Triad archiver (`enforce-triad-hot-surface.py`) only recognizes H1 `# US-xxxx` story boundaries; repos with H2 `## US-xxxx` sections cannot auto-archive when `architecture.md` exceeds `ARCH_HOT_MAX_LINES` — `/auto` stops with `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS`.
- **Operator scope (2026-06-06)**: **both** fixes — backward-compat archiver for `## US-xxxx` rollover **and** forward enforcement of H1 `# US-xxxx` for new `/architecture` writes.
- **Evidence**: `handoffs/intake_evidence/BUG-0010-intake-20260606.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`); operator `/ask` report (discovery PASS then triad gate fail at 3021/3000 lines).
- **Intake closure (2026-06-06, PO)**: Backlog **`BUG-0010`** **OPEN**; next **`/discovery`**.

## Intake notes — BUG-0011

- **Problem**: **US-0089** shipped Caveman gates, literal invariants, and scratchpad toggles but `.cursor/rules/caveman.mdc` lacks upstream voice-compression rules — with **`CAVEMAN_MODE=1`** replies stay verbose (full sentences, filler, hedging).
- **Operator scope (2026-06-06)**: add upstream-aligned voice section (lite/full/ultra, drop filler, fragments, auto-clarity exceptions); preserve **DEC-0072** 9-zone literal invariant and **US-0090** input-compression orthogonality; no Wenyan / vendor install.
- **Evidence**: `handoffs/intake_evidence/BUG-0011-intake-20260606.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`); operator `/ask` comparing local `caveman.mdc` vs JuliusBrussee/caveman `SKILL.md`.
- **Intake closure (2026-06-06, PO)**: Backlog **`BUG-0011`** **OPEN**; next **`/discovery`**.

## Discovery Notes — BUG-0016

- **Operator value proposition**: On an OpenCode host with the `.opencode/` pack installed, each role agent (`@po`, `@tech-lead`, …) can run the **kit-mandated Python validators** and **write owned phase artifacts** under Layer-1 host permissions — without granting non-dev roles production/code write (success test (c)).
- **Defect framing (discovery-locked)**:
  - **Matrix-vs-duties gap, not missing matrix**: US-0122 / DEC-0122 §2 shipped as designed; kit contracts (US-0078/US-0079 intake validators, DEC-0069 resume brief, triad/`/refresh-context` scripts, real `sprints/S####/` paths) require bash + path globs the literal matrix denies or misspells.
  - **Distinct from BUG-0015** (DONE — `/auto` dispatch; compose note only: spawn-only Task path may now work).
  - **Distinct from US-0131 / US-0132** (config/model parity — do not expand).
  - **Distinct from US-0122 DONE** — do not reopen as a feature story; bug-fix amends the Layer-1 matrix.
- **Product-facing constraints**:
  - Preserve success test (c): non-dev `edit` keep `**` deny last; no production/code allow keys (`scripts/**`, `its_magic/**`, `**/*.py`, installer surfaces) for `po`/`tech-lead`/`qa`/`release`/`curator`/`security`/`auto`.
  - `security` stays `edit: deny` + `bash: ask` unless research finds a duty contradiction.
  - `auto` stays spawn-only (`edit`/`bash` deny; 7-role `task` allow-list).
  - Active `.opencode/agents/*.md` and `template/.opencode/agents/*.md` remain byte-parity after fix.
- **Discovery locks D1–D8**: see `docs/product/backlog.md` **`### BUG-0016`** `discovery_notes` and `handoffs/po_to_tl.md` discovery handoff.
- **Done signal (operator)**: role agents can complete validator + owned-write duties on OpenCode; static harness proves production deny for non-dev; no live OpenCode CI probe required.
- **Research asks**: DQ1–DQ8 for **`/research`** → new **`R-0115`** (compose **`R-0109`**; do not wipe). Next phase **`research`** (tech-lead).

## Discovery Notes — BUG-0015

- **Operator value proposition**: On an OpenCode host with the `.opencode/` pack installed, operators run **`/auto`** once and expect the orchestrator plugin to **start the spawn loop** (`spawnPhase` → phase→role chain → stop-matrix) so lifecycle advances — or fail closed with a documented **`OPENCODE_*`** reason code. Today the thin command reaches STOP and nothing invokes spawn.
- **Defect framing (discovery-locked)**:
  - **Compose gap, not missing surfaces**: **US-0124** / **DEC-0124** ships `spawnPhase` + stop-matrix subprocess; **US-0125** / **DEC-0125** ships dispatch-only `/auto` (`agent: auto` + STOP). Runtime linkage between slash-entry and plugin spawn is missing.
  - **Distinct from BUG-0016** (Layer-1 permissions vs kit duties — out of scope this segment).
  - **Distinct from US-0131 / US-0132** (config/model parity — do not expand).
  - **Distinct from BUG-0006 / BUG-0012** (Cursor spawn-only / native-chain regressions).
- **Product-facing messaging constraints**:
  - Thin **`auto.md`** stays dispatch-only (≤20 lines; no `ctx.session.create` / spawn logic) per **DEC-0125** DQ5.
  - Plugin remains single spawn owner; agent prompt alone is not sufficient (success test (a) / **BUG-0006**).
  - Missing `session.create` → fail-closed **`OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`** (no in-band roleplay fallback).
  - Python **`scripts/auto_outer_driver.py`** remains stop-matrix SOT (no TypeScript reimplementation).
- **Discovery locks D1–D7**: see `docs/product/backlog.md` **`### BUG-0015`** `discovery_notes` and `handoffs/po_to_tl.md` discovery handoff.
- **Done signal (operator)**: `/auto` on OpenCode starts plugin-owned spawn (or emits **`OPENCODE_*`** fail-closed); contract tests cover dispatch wiring without live OpenCode CI probe.
- **Research asks**: DQ1–DQ7 for **`/research`** → new **`R-0114`** (compose **`R-0109`**; do not wipe). Next phase **`research`** (tech-lead).

## Discovery Notes — BUG-0012

- **Operator value proposition**: When **`AUTO_FLOW_MODE=full_autonomy`** and **`AUTO_BACKLOG_DRAIN=1`** are set in Cursor IDE, operators run **`/auto` once** and expect **hands-off** advance across **multiple story segment boundaries** without manual re-**`/auto`** or mandatory **`auto_outer_driver.py`** prose — the product promise **US-0095** / **DEC-0080** shipped **2026-06-07** (**S0084**). **BUG-0012** tracks **post-delivery runtime regression**: operator reports orchestration **stops after every user-story completion** while paradoxically citing active drain/full_autonomy and instructing re-**`/auto`** — behavior resembling pre-**US-0095** manual re-invocation.
- **Regression framing (discovery-locked)**:
  - **Not a duplicate of US-0095** — that story **delivered** native in-chat auto-chain contract + static markers; this bug is **contract-vs-runtime gap** after recent adjustments (post-**US-0095** / **US-0096** era).
  - **Distinct from BUG-0005** (stale resume after bug intake), **BUG-0006** (spawn-only — preserve, do not weaken), **US-0096** (delivery-mode lifecycle shape — orthogonal).
  - **Primary failure modes (hypothesis)**: orchestrator treats Cursor turn boundary as terminal segment stop; emits forbidden mandatory re-**`/auto`** / outer-driver prose under **`full_autonomy`**; fails **DEC-0080** IDE drain-advance **step 7** (immediate next-segment spawn after **`refresh-context`**).
- **Product-facing messaging constraints**:
  - **IDE primary path**: with **`full_autonomy`**, runbook/command prose must **never** instruct mandatory re-**`/auto`** between drain segments when continuation is schedulable (**US-0095** **AC-5** / **AC-6** intent).
  - **Outer driver = optional fallback only**: **`scripts/auto_outer_driver.py`** remains for headless/CI or **`NATIVE_CHAIN_UNAVAILABLE`** — not default IDE drain path.
  - **Spawn-only preserved**: in-chat continuation is orchestrator **scheduling** of fresh phase subagents — not in-band phase-role execution (**BUG-0006** / **US-0069**).
  - **Hard gates unchanged**: **`decision_gate`**, **`loop_max`**, security deny-list, isolation (**US-0048**), strict proof (**DEC-0038**), **`resume_brief`** pairing (**DEC-0069**) — fix must not relax **DEC-0078** matrix.
  - **`AUTO_QUIET=1`**: suppress routine prose but must not reintroduce outer-driver wait or segment-exhausted terminal messaging when drain budget remains.
- **Discovery-locked fix boundary (orchestration surfaces only)**:
  - **Primary**: `.cursor/commands/auto.md` native in-chat auto-chain loop (**US-0095** / **DEC-0080**); IDE drain-advance-without-pause 7-step algorithm; orchestrator foreground Task/subagent continuation; **`handoffs/resume_brief.md`** segment pointers; **`docs/engineering/auto-orchestration-reference.md`** operator messaging rules.
  - **Secondary**: **`state.md`** **`native_chain_active`** breadcrumb truthfulness; contract tests in **`tests/auto_command_contract_test.py`** (forbidden-prose markers + behavioral regression beyond static string presence).
  - **Out of scope**: weakening spawn-only contract; deleting outer driver; changing **US-0096** delivery modes; bug-queue mutex (**US-0087**) unless regression test requires; publish automation (**RELEASE_PUBLISH_MODE=auto**).
- **Done signal (operator)**: single **`/auto`** with **`full_autonomy`** + drain observes hands-off advance across **≥2 consecutive story segments** in IDE without manual **`/auto`** between segments; contract tests lock forbidden drain-stop prose.
- **Research asks**: reconcile doc/contract PASS vs runtime FAIL; drain-advance step-7 audit; forbidden-prose inventory; **`native_chain_active`** truthfulness; **`AUTO_QUIET`** / **US-0096** interaction; multi-segment E2E strategy — extend **`R-0083`** before **`/architecture`**.

## Discovery Notes — BUG-0011

- **Operator value proposition**: When **`CAVEMAN_MODE=1`**, operators expect **visibly shorter assistant prose** (fewer output tokens, full technical accuracy) — matching the upstream Caveman intent documented in **`R-0073`**. The fix completes the **response-side voice vertical** that **US-0089** scaffolded but did not ship; it is **orthogonal** to **US-0090** input-side file compression (already **DONE**).
- **Product-facing messaging constraints**:
  - **Token savings, not roleplay**: voice rules target terse/imperative prose and dropped filler — not stereotypical "cave man" speech or Wenyan modes.
  - **Literal safety preserved**: all nine **DEC-0072** literal regions (code blocks, paths, reason codes, IDs, proof tuples, etc.) remain byte-literal under every level including **`ultra`**.
  - **User-rule precedence**: when Caveman mode is on, voice compression wins over conflicting user rules that demand "complete sentences" or high prose quality — explicit precedence paragraph required in the rule.
  - **Default-off unchanged**: **`CAVEMAN_MODE=0`** (or absent) adds zero behavioral change; existing contract tests under **`test_caveman_default_off_*`** must stay green.
- **Discovery-locked contract (rule-only per DEC-0072)**:
  - **Voice section** in `.cursor/rules/caveman.mdc` + template mirror: lite/full/ultra table, drop rules, auto-clarity exceptions, persistence.
  - **Runbook extension**: level table + operator examples under **`### Caveman mode (US-0089)`**.
  - **Contract tests**: additive **`test_caveman_voice_*`** markers; update US-0090 SHA-256 baseline intentionally after rule edit.
  - **Negative scope**: no Wenyan; no vendor token-percent claims; no `npx skills add`; no changes to **`CAVEMAN_COMPRESS_INPUT`** / **`scripts/caveman_compress_input.py`**.
- **Research asks**: SHA-256 strategy, level-table wording, precedence placement, architecture surface — see **`R-0077`** before **`/architecture`**.

## Discovery Notes — BUG-0010

- **Operator value proposition**: Long-running its-magic projects must **auto-unblock** when `architecture.md` grows past hot-surface caps — regardless of whether historical agents wrote story sections as H1 or H2. After the fix ships, `/auto` must not halt on pre-existing `## US-` repos; new architecture work must converge on the canonical H1 `# US-xxxx` contract (**DEC-0054** §2) so future rollovers stay predictable.
- **Product-facing messaging constraints**:
  - **One-time remediation**: operators with `##`-only architecture files can either wait for the archiver fix (preferred) or manually normalize headings / run manual archive — no forced bulk rewrite in this bug scope.
  - **Fail-closed vocabulary preserved**: `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS` remains for genuinely unsliceable oversize files (no story headings at either level); fix narrows the failure mode to true ambiguity, not heading-level blindness.
  - **Template parity**: active + `template/` command contracts and triad script must stay aligned (**US-0017**).
- **Dual-track contract (discovery-locked)**:
  - **Track A (rollover)**: `## US-xxxx` counts as a story-section boundary for archival slicing (same oldest-first semantics as H1).
  - **Track B (authoring)**: `/architecture` phase blocks new `## US-xxxx` story sections; mandates H1 `# US-xxxx` (and existing `# BUG-xxxx` pattern for defects).
- **Research asks**: regex/precedence table, validator placement, enforcement gate severity, self-test matrix — see **`R-0076`** before **`/architecture`**.

## Discovery Notes — BUG-0009

- **Operator value proposition**: Every its-magic-created project gets **green-by-default CI** that runs only project-agnostic checks (`checks` + optional `auto-fix` from runbook keys). Self-distribution validation (`npm pack`, Homebrew formula, Chocolatey pack) stays on the **its-magic kit repo** only — never shipped into consumer repos.
- **Product-facing messaging constraints**:
  - **Upgrade remediation**: operators with already-broken repos must run an its-magic **upgrade** (or `clean` + reinstall) to receive the corrected `ci.yml` — not a manual GitHub edit. Release notes and runbook must state this plainly.
  - **Fresh-project clarity**: when no test/lint/typecheck commands are configured, CI summary must say **no tests configured yet** and pass — not `Tests or lint failed`.
  - **No regression to kit self-CI**: its-magic's own repo keeps full packaging job coverage for npm/Homebrew/Chocolatey release confidence (**US-0007** / **US-0009**).
- **Decoupling contract (discovery-locked)**: `template/.github/workflows/ci.yml` ≠ `.github/workflows/ci.yml` after fix — explicit **`US-0017` exception** for this path; drift guard prevents re-leak.
- **Research asks**: template CI shape, drift-guard mechanism, runbook bootstrap defaults, parity exception policy, install/upgrade smoke — see **`R-0075`** before **`/architecture`**.

## Intake Notes — US-0092

- **Problem**: **US-0088** documents continuous `/auto` and backlog drain, but operators still manually re-invoke after every phase or segment — scratchpad auto flags alone do not sustain multi-turn orchestration in Cursor.
- **Intent**: Opt-in **`AUTO_FLOW_MODE=full_autonomy`** (default-off; **`auto_until_decision`** unchanged) with a **shipped stdlib outer-driver script**, self-verify UAT/QA via build/test/API/browser, bounded block auto-resolve, and drain-without-pause between OPEN items.
- **Operator constraint (hard)**: **`TOKEN_PROFILE`** affects **token cost / context breadth only** — not automation level, phase depth, drain behavior, or outer-driver invocation.
- **Evidence**: `handoffs/intake_evidence/US-0092-intake-20260606.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`); research anchor **`R-0078`**.
- **Intake closure (2026-06-06, PO)**: Backlog **`US-0092`** **OPEN**; next **`/discovery`**.

## Discovery Notes — US-0092

- **Operator value proposition**: Downstream its-magic consumers enable **`AUTO_FLOW_MODE=full_autonomy`**, run the outer driver **once**, and receive end-to-end delivery — implementation, self-verified UAT, bounded block remediation, and automatic advance to the next OPEN story/bug — without babysitting each Cursor turn.
- **Product-facing messaging constraints**:
  - **Default-off safety**: **`manual`** and **`auto_until_decision`** remain unchanged; full autonomy is explicit opt-in only.
  - **TOKEN_PROFILE orthogonality**: docs and scratchpad comments must never imply **`lean`** = less automation or **`full`** = more phases — only context breadth / token cost (**US-0080** / **DEC-0062** composition).
  - **Publish boundary**: **`RELEASE_PUBLISH_MODE=auto`** stays explicit opt-in; full_autonomy does not auto-publish.
  - **Security posture**: no auto-read **`.env`**, no intake-evidence mutation, attempt ledgers names-only (**AC-10**).
  - **Spawn-only preserved**: fresh subagent per phase (**US-0048** / **BUG-0006**) — outer driver loops **invocations**, not in-chat multi-role stacking.
- **Six-step operator flow (discovery-locked)**:
  1. Set **`AUTO_FLOW_MODE=full_autonomy`** (+ optional drain/bug-queue flags).
  2. Run shipped outer-driver script once.
  3. Inner `/auto` executes lifecycle with self-verify QA/verify-work.
  4. Recoverable blocks retry within caps.
  5. Segment completion triggers immediate next-item scheduling (drain-without-pause).
  6. Driver exits on cap, hard gate, or empty portfolio.
- **Composition boundaries**: extends **US-0088** (continuous policy) + **US-0044** (drain switches) + **US-0065/66** (runtime probes) + **US-0087** (bug-queue mutex); does not weaken isolation (**US-0048**) or strict proof (**US-0056**).
- **Research asks**: outer-driver model, stop matrix vs **US-0088**, UAT probe catalog, block-retry ledger, TOKEN_PROFILE audit scope — see **`R-0078`** before **`/architecture`**.

## Intake Notes — US-0093

- **Problem**: **US-0092** / **DEC-0078** shipped the UAT probe catalog and fail-closed vocabulary, but **`browser_smoke`**, **`process_health`**, and **`cli_smoke`** still return **`UAT_PROBE_UNRESOLVED`** without execution; **`manual_operator`** UI steps are classified but never auto-run.
- **Intent**: Wire **Cursor built-in browser** (navigate, click, type, scroll, screenshot, console/network evidence) as the **primary** web self-test path for **`/verify-work`**, **`/qa`**, and **`/execute`**; deterministic **HTTP / Playwright subprocess fallback** when browser MCP is unavailable; complete remaining probe stubs; record evidence in **`uat.json`** `probe_results[]`.
- **Operator constraint (hard)**: fail closed — no silent PASS when browser and fallback both fail; respect Cursor browser approval settings and **`PERMISSION_MODE`**; never auto-read **`.env`** or submit credentials.
- **Evidence**: `handoffs/intake_evidence/US-0093-intake-20260606.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`); research anchor **`R-0079`**.
- **Intake closure (2026-06-06, PO)**: Backlog **`US-0093`** **OPEN**; next **`/discovery`**.

## Discovery Notes — US-0093

- **Operator value proposition**: Webapp and full-stack its-magic consumers get **real browser UAT** during **`/qa`** and **`/verify-work`** — not probe-catalog stubs. Operators enable browser self-test once via scratchpad; agents navigate the running dev server, capture screenshots and console/network summaries, and write path-ref evidence operators can inspect without re-running manual checklists.
- **Product-facing messaging constraints**:
  - **Default-on when resolvable**: when web stack + health URL or dev-server port resolves, **`browser_smoke`** runs automatically — operators are not asked to install Playwright unless fallback mode is selected or MCP is unavailable.
  - **Approval posture**: Cursor browser tools require approval by default (manual, allow-list, or auto-run per Cursor Settings). Docs must state that **`UAT_BROWSER_PROBE_MODE=cursor`** composes with operator approval settings — its-magic does not bypass browser security guardrails without explicit scratchpad opt-in.
  - **Human judgment preserved**: steps requiring aesthetic judgment, subjective UX review, or explicit operator sign-off remain **`manual_operator`** with **`UAT_PROBE_UNRESOLVED`** (fail closed, documented).
  - **Spawn-only preserved**: browser MCP execution stays in fresh QA/verify-work/execute subagent contexts (**US-0048** / **BUG-0006**); stdlib lib classifies and records — it does not pretend to drive MCP from Python alone.
- **Two-tier execution contract (discovery-locked)**:
  1. **Stdlib tier** (`scripts/uat_probe_lib.py`): classify step → probe kind; resolve stack profile, health URL, dev-server port; run **HTTP** or **Playwright subprocess** when mode is fallback or MCP unavailable; execute **`process_health`** / **`cli_smoke`** via bounded subprocess; emit reason codes; never silent PASS.
  2. **Agent tier** (`.cursor/commands/verify-work.md`, **`qa.md`**, **`execute.md`**): when **`UAT_BROWSER_PROBE_MODE=cursor`** (default) and probe kind is **`browser_smoke`** or automatable **`manual_operator`**, subagent invokes Cursor browser tools (navigate → interact → screenshot → console/network read) per documented step plan; writes **`browser_evidence_refs`** into **`uat.json`** `probe_results[]` and mirrors fields in **`qa-findings.md`**.
- **Browser automation scope (reference: [Cursor Browser tools](https://cursor.com/docs/agent/tools/browser))**:
  - **In scope**: Navigate, click, type, scroll, screenshot, console output, network traffic monitoring; dev-server awareness (detect running ports from **`runtime-connectivity.md`** / scratchpad); **`@browser`** operator override for manual rescue.
  - **Out of scope**: visual-regression pixel-diff infrastructure; design-sidebar visual editing as UAT evidence; auto-bypass of enterprise origin allowlists; vendor guarantees beyond documented MCP surface.
- **`manual_operator` routing (discovery stub)**: reclassify steps with UI/workflow verbs (**click**, **fill**, **navigate**, **smoke**, **form**, **submit**, **login page**, **dashboard**) to browser probe plans when no explicit human-judgment signal (**visually**, **aesthetically**, **operator confirms**, **subjective**); judgment-only steps stay **`manual_operator`**.
- **Composition boundaries**: extends **US-0092** / **DEC-0078** probe catalog; delivers **R-0041** browser integration promise; composes **US-0065** runtime QA fields; does not weaken security deny-list or full_autonomy false-PASS guards.
- **Research asks**: agent-browser command contract, verb routing table, fallback selection, stub resolution rules, evidence schema, contract-test inventory — see **`R-0079`** before **`/architecture`**.

## Intake Notes — US-0094

- **Problem**: Root `README.md` opens with a generic template tagline and a flat feature bullet list. It does not communicate the core product promise: the operator is the **customer/dreamer** while a structured **AI dev team** can run the full delivery lifecycle — including optional **full autonomy** — with artifact-first memory in the repo.
- **Intent**: Rewrite the README opening into a clear hierarchy — **framework purpose → main features → sub-features → existing detailed sections** — re-audit all **US-0091** coverage anchors, and keep **`README.md`** and **`template/README.md`** byte-identical.
- **Operator scope (2026-06-07)**: root + template README only; DEV shard optional cross-link; preserve all deep detail sections below the new intro; foreground **US-0092** full-autonomy value prop.
- **Evidence**: `handoffs/intake_evidence/US-0094-intake-20260607.json`; research anchor **`R-0080`**.
- **Intake closure (2026-06-07, PO)**: Backlog **`US-0094`** **OPEN**; next **`/discovery`**.

## Discovery Notes — US-0094

- **Operator value proposition**: First-time readers immediately understand that **its-magic is an autonomous AI dev team framework** — the operator is the **customer and dreamer**; role-based agents (PO, Tech Lead, Dev, QA, Release, Curator) run intake → release with **artifact-first repo memory**, and optional **full autonomy** is a first-class headline capability (not a footnote in **`Commands and workflow`**).
- **Information architecture (Diataxis-aligned, per **R-0054** / **R-0080**)**:
  - **Explanation tier** (new): 2–3 visionary paragraphs **before** `## Features` — product promise and operator role.
  - **Summary tier** (new): four **main-feature pillars** as `###` subsections under existing `## Features (what its-magic can do)` — concise sub-feature bullets only; no encyclopedic duplication of catalog prose.
  - **Reference tier** (preserved): three existing `### Feature coverage catalog (US-0091)` blocks stay in their affinity-home H2 sections; all deep body sections (`Setup`, `How-to`, `Commands and workflow`, walkthroughs, `Purpose`…`Contributing`) remain below unchanged in substance.
- **Intro outline (discovery-locked — execute copies verbatim into both README files)**:
  1. **Paragraph 1 — Dreamer + team**: You bring the idea; its-magic is your structured **AI dev team** in Cursor — PO, Tech Lead, Dev, QA, Release, and Curator — that turns ideas into shipped software through explicit phases and handoff artifacts.
  2. **Paragraph 2 — Artifact-first workflow**: State lives in repo files (`docs/product`, `handoffs`, `sprints`, `decisions`) — not chat-only memory. Run `/intake` with your idea, then follow intake → discovery → architecture → sprint plan → execute → QA → release; pause/resume and decision gates keep you in control when you want to steer.
  3. **Paragraph 3 — Full autonomy headline (**US-0092**)**: When you want hands-off delivery, enable **`AUTO_FLOW_MODE=full_autonomy`** (default-off), run the shipped outer driver once, and let `/auto` drain your backlog — self-verify UAT, bounded block retry, and advance to the next OPEN story or bug without re-invoking each phase manually. Guided and decision-gated modes remain the default.
  - **Optional single DEV cross-link** (allowed per AC-10): one sentence at end of paragraph 2 or 3 pointing implementers to **`docs/developer/README.md`** — no DEV body duplication in root README.
- **Main-feature pillars (discovery-locked names and scope)** — all as `###` under `## Features` only; **no new `USER_*` H2 literals** (**DEC-0059**):
  1. **`### Autonomous AI workflow`** — phased slash commands (`/intake`…`/release`), `/auto` orchestration, pause/resume, decision gates (`DEC-xxxx`), team mode, continuous drain (**US-0088**), full autonomy + outer driver (**US-0092**).
  2. **`### Quality & verification gates`** — 3-layer quality chain (AI loop → `validate-and-push` → CI auto-fix), release/QA/UAT gates, user-visible metadata guard (**US-0071**), phase isolation proofs (**US-0048** / **US-0056**).
  3. **`### Distribution & install`** — npm / Chocolatey / Homebrew, `its-magic --target` install modes (missing/overwrite/upgrade/clean), lifecycle QA matrix (**US-0041**), multi-target publish (**US-0054**).
  4. **`### Operator control & ergonomics`** — scratchpad flags and local overrides, guided intake packs, Caveman voice/compression (**US-0089** / **US-0090**), token-cost profiles (**US-0080**), voice input, permissions/runtime connectivity.
- **Sub-feature mapping rule**: each pillar gets **3–6 teaser bullets** naming commands, flags, or outcomes in operator language; **must not** repeat the full `US-xxxx`/`BUG-xxxx` catalog lines. The authoritative 104-item index remains the three **`### Feature coverage catalog (US-0091)`** blocks (affinity homes below).
- **Full-autonomy messaging placement (discovery-locked)**:
  - **Primary**: intro paragraph 3 (before any H2).
  - **Secondary**: first or second bullet under **`### Autonomous AI workflow`** pillar (name `/auto`, `AUTO_FLOW_MODE=full_autonomy`, outer driver, drain-without-pause in plain language).
  - **Tertiary**: existing catalog line for **US-0092** stays in its affinity section — do not remove or demote.
  - **Forbidden**: burying full-autonomy value prop only under **`Developer and release deep-dive`** or deep **`Commands and workflow`** subsections without intro/pillar mention (**AC-8**).
- **Coverage-safe move rules (discovery-locked for execute / **DEC-0074** affinity)**:
  1. **Affinity homes are authoritative** — validator resolves each in-scope DONE item to one root H2 via `readme-section-affinity.json`: slash commands → **`Commands and workflow`**; scratchpad keys → **`Other useful capabilities`**; distribution/npm/choco/brew → **`Features`**; release/UAT gates → **`Commands and workflow`**; governance default → **`Other useful capabilities`**.
  2. **Three catalog blocks are immutable in parent H2** — markers `<!-- readme-feature-coverage-catalog -->` at Features (~line 27), Commands (~line 1139), and Other useful capabilities (~line 1339): every bullet retaining its `US-xxxx`/`BUG-xxxx` id must stay inside the **same parent H2 body** after restructure; reorder within block allowed; cross-H2 moves forbidden unless affinity tag changes (out of scope).
  3. **Id-preservation contract** — each catalog bullet line must still contain detectable `US-xxxx` or `BUG-xxxx` (or slash-command / scratchpad key matching `has_root_coverage`); silent deletion forbidden.
  4. **Pillar teasers are id-free** — new pillar bullets may cite commands/flags by name but must not replace catalog anchors; baseline **`coverage_total=104`**, **`coverage_missing=[]`**.
  5. **DEV shard untouched** — `docs/developer/README.md` traceability rows unchanged; root moves do not require DEV edits unless a root anchor is accidentally removed.
  6. **Post-edit gate** — `python scripts/validate_readme_feature_coverage.py --report` must PASS before merge; `validate_doc_profile.py` + `check-user-visible-metadata.py` on changed surfaces.
- **Parity workflow (discovery-locked)**: single-source edit on `README.md`, then byte-copy to `template/README.md` (or edit one and `diff`/copy); verify with `fc /b` or equivalent; **US-0017** template-drift tests must stay green. Do not edit both files independently.
- **Section budget**: add only **`###` H3** under existing H2s (primarily Features); do not add new top-level `##` headings; current 13 H2 layout preserved (**DEC-0059** / `validate_doc_profile.py`).
- **Product-facing messaging constraints**:
  - No internal planning tokens in operator blurbs (**US-0071**).
  - Full autonomy always paired with **default-off / opt-in** language — never imply always-on autonomy.
  - Replace generic "Happy coding! Build something awesome." tagline — not the H1 product name line.
- **Risks**: **R1** pillar prose duplicates catalog → mitigate teaser-only bullets + catalog unchanged; **R2** cross-H2 catalog move breaks affinity → forbid cross-H2 moves; **R3** intro bloat → cap at 3 short paragraphs; **R4** active/template drift → single-source + byte compare; **R5** overclaiming autonomy → explicit opt-in wording per **US-0092** / **DEC-0078**.
- **Research asks for **R-0080** extension**: finalize pillar-to-catalog affinity map table, intro word-count budget, and whether **DEC-0074** needs a companion §intro hierarchy lock — see **`/research`** before **`/architecture`**.

## Discovery Notes — US-0095

- **Operator value proposition**: When **`AUTO_FLOW_MODE=full_autonomy`** is enabled in Cursor IDE, operators run **`/auto` once** and expect **hands-off** delivery across **all lifecycle phases** and **backlog-drain segments** — without installing or running **`auto_outer_driver.py`** between stories. **US-0095** closes the product promise gap left by **US-0092** (outer driver as bridge) and **US-0088** Option B equivalence prose.
- **Primary vs fallback paths (discovery-locked)**:
  - **Primary (IDE)**: native in-chat auto-chain — orchestrator schedules sequential phase spawns and drain advances within one `/auto` invocation.
  - **Fallback (headless/CI)**: **`scripts/auto_outer_driver.py`** remains optional — not deleted, not required for IDE **`full_autonomy`**.
- **Six-step operator flow (IDE, `full_autonomy`)**:
  1. Set scratchpad keys (`full_autonomy`, optional drain/bug-queue).
  2. Run **`/auto`** once in Cursor (not outer driver).
  3. Orchestrator spawns each phase with fresh subagent context; verifies boundaries; chains to next phase in-chat.
  4. On segment completion, drain policy selects next OPEN item and continues without operator pause.
  5. Relaxable transient stops retry per **US-0092** matrix; hard governance gates unchanged.
  6. Exit on cap, hard gate, or empty portfolio.
- **Product-facing messaging constraints**:
  - **Default-off safety**: **`manual`** and **`auto_until_decision`** unchanged; native chain applies only under explicit **`full_autonomy`**.
  - **No false mandatory outer driver**: IDE runbook/README must not imply outer driver is required for drain when **`full_autonomy`** is on (**AC-5** / **AC-6**).
  - **Spawn-only preserved**: continuation is orchestrator **scheduling**, not in-chat multi-role execution (**BUG-0006**).
  - **Quiet mode**: **`AUTO_QUIET=1`** suppresses chatter but must not reintroduce outer-driver wait instructions between segments.
- **Composition boundaries**: extends **US-0092** / **DEC-0078** (stop matrix, caps, block-retry) + **US-0088** (continuous policy) + **US-0044** (drain) + **US-0087** (bug-queue mutex); does not weaken isolation (**US-0048**) or strict proof (**US-0056**).
- **Research asks**: native continuation model, IDE drain-advance, cap ledger, fallback boundary, operator messaging — see **`R-0081`** before **`/architecture`**.

## Intake Notes — US-0096

- **Problem**: **US-0080** / **DEC-0062** cut context breadth via **`TOKEN_PROFILE`** and command slimming, but the default lifecycle still runs **~11 subagent spawns** with heavy handoffs and per-phase **`state.md`** checkpoints — **DEC-0052** reinstatement blocks naive phase exclusion. Operators want **50–70% token reduction** at near-same code quality without breaking standard mode.
- **Intent**: New opt-in **`DELIVERY_MODE`** axis — **`standard`** (default, unchanged), **`ultra_lean`** (4 macro-phases + **`pack.json`** + memory index), **`mega_quick`** (enhanced **`/quick`** under **`/auto`**). **Layered memory**: write deltas, read vision/architecture/decisions by **section reference** — not amnesia. **Tranche A** universal wins ship without any mode toggle.
- **Operator constraint (hard)**: **`DELIVERY_MODE`** controls **lifecycle shape and artifacts only** — must not substitute for **`TOKEN_PROFILE`** (context breadth) or **`CAVEMAN_MODE`** (reply voice). **`standard`** must remain byte-compatible with pre-**US-0096** behavior.
- **Evidence**: `handoffs/intake_evidence/US-0096-intake-20260611.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`); research anchor **`R-0082`**.
- **Intake closure (2026-06-11, PO)**: Backlog **`US-0096`** **OPEN**; next **`/discovery`**.

## Discovery Notes — US-0096

- **Operator value proposition**: Operators who accept near-same code quality can cut **~50%** token burn (**`ultra_lean`**, four macro-spawns + layered memory) or **~70%+** (**`mega_quick`**, enhanced **`/quick`** path) without abandoning institutional memory — vision/architecture/decisions stay reachable by **section reference**, not amnesia. **`DELIVERY_MODE=standard`** (default) remains **byte-compatible** with today's full lifecycle.
- **Three-mode axis (discovery-locked)** — scratchpad key **`DELIVERY_MODE=standard|ultra_lean|mega_quick`** (default **`standard`** when unset):

| Mode | Lifecycle shape | Target token reduction | Primary artifacts |
|------|-----------------|------------------------|-------------------|
| **`standard`** | Today's eleven canonical phases + **DEC-0052** reinstatement | Baseline (no regression) | Existing handoffs, sprint folders, triad hot surfaces |
| **`ultra_lean`** | Four macro-phases: **`spec` → `plan` → `build+verify` → `ship`** | ~50% vs comparable **`standard`** run | **`work/US-xxxx/pack.json`**, **`handoffs/active-context.md`**, section-scoped cold reads |
| **`mega_quick`** | Enhanced **`/quick`** under **`/auto`** (1 primary spawn; +1 on test failure) | ~70%+ vs comparable **`standard`** run | **`sprints/quick/Qxxxx/task.json`**, **`summary.md`**, compact **`state.md`** index row |

- **Orthogonality table (discovery-locked — non-substitution)**:

| Axis | Controls | Must NOT control |
|------|----------|------------------|
| **`TOKEN_PROFILE`** (`lean\|balanced\|full`) | Context breadth / token cost per spawn (**DEC-0062**) | Lifecycle shape, phase count, automation level |
| **`DELIVERY_MODE`** | Lifecycle shape, artifact surface, spawn count | Context breadth, reply voice, drain/automation |
| **`CAVEMAN_MODE`** / **`CAVEMAN_LEVEL`** | Reply voice only (**DEC-0072**) | Lifecycle shape, context breadth |
| **`AUTO_FLOW_MODE=full_autonomy`** | Automation, drain-without-pause (**DEC-0078** / **DEC-0080**) | Lifecycle shape (composes with **`DELIVERY_MODE`**) |

- **Ultra_lean macro-phase mapping (discovery-locked)** — each macro-phase = **one fresh subagent spawn** (**BUG-0006** preserved); inner loops stay **inside** the macro spawn:

| Macro-phase | Role | Absorbs canonical phases | Stop / handoff |
|-------------|------|--------------------------|----------------|
| **`spec`** | **po** | **`intake`** + **`discovery`** | Writes/updates **`pack.json`** AC + discovery locks; prepends **`active-context.md`** index row |
| **`plan`** | **tech-lead** | **`research`** + **`architecture`** + **`sprint-plan`** | Locks tasks in **`pack.json`**; optional architecture/decision **delta** append when new pattern |
| **`build+verify`** | **dev** (+ **qa** only on test failure) | **`execute`** + merged **`qa`**/**`verify-work`** checklist | **`AUTO_IMPLEMENTATION_LOOP`** preserved; tests green before stop; UAT matrix in one spawn |
| **`ship`** | **release** (+ **curator** refresh) | **`release`** + **`refresh-context`** | Status flip per **US-0045**; compact evidence hashes; triad rollover when hot surfaces mutate |

- **Layered memory tiers (discovery-locked)**:
  1. **Hot** — **`handoffs/active-context.md`** (~30–80 lines, rolled over): read-before-code refs for active story; lists **`pack.json`** path, section anchors, last delta ids.
  2. **Warm** — **`work/US-xxxx/pack.json`**: AC checklist, task seeds, handoff refs, status, **`deltas[]`** pointers — canonical per-story working set for lean modes.
  3. **Cold** — vision / architecture / decisions: **section-scoped narrow-read** only (cap **`LEAN_COLD_READ_MAX_SECTIONS`**); conditional **delta append** when new patterns learned — never wholesale file reads by default.

- **Mega_quick routing (discovery-locked)**:
  - **`/auto`** reads **`DELIVERY_MODE=mega_quick`** (or backlog row override per **AC-8**) and routes to enhanced **`/quick`** semantics — **not** a replacement slash command.
  - **Eligibility signals** (any one sufficient at **`/auto`** materialization): explicit scratchpad mode; backlog story row **`delivery_mode: mega_quick`**; argv **`delivery-mode=mega_quick`**; operator **`/quick`**-class scope (small, bounded, no full sprint ceremony).
  - **Ineligible** (fail closed to **`standard`** or operator prompt — research locks exact reason code): multi-AC cross-cutting stories, open **`plan_area_inventory` > 1** without operator override, bug segments (**`INTAKE_WORK_ITEM_KIND=bug`**), stories requiring companion **`DEC-xxxx`** + architecture lock before code.
  - **Artifacts**: **`sprints/quick/Qxxxx/task.json`** holds AC + test commands; **`summary.md`** + one **`state.md`** index row; second spawn **only** on test failure.
  - **Status flip**: requires **`acceptance_met: true`** + green tests — same quality floor as **AC-9**.

- **Tranche delivery order (discovery-locked)**:
  - **Tranche A** — universal token wins (always on, no mode toggle): narrow-read context packs in **all** phase commands, tighter default hot-surface thresholds, delta handoff append guidance, touch-graph read policy in runbook.
  - **Tranche B** — **`ultra_lean`** macro-lifecycle + **`pack.json`** + **`active-context.md`**.
  - **Tranche C** — **`mega_quick`** **`/auto`** routing + enhanced **`/quick`** contract.
  - **Tranche D** — optional backlog **`delivery_mode`** row + **`AUTO_DELIVERY_ROUTING=backlog_then_scratchpad`** precedence chain.

- **Mode-scoped **DEC-0052** reinstatement (discovery-locked)**:
  - **`DELIVERY_MODE=standard`** (or unset): today's reinstatement algorithm unchanged — excluded phases reinstate per scratchpad phase plan.
  - **`ultra_lean`** / **`mega_quick`**: **no** reinstatement of eleven-phase chain; resolver materializes mode-specific plan **before** any legacy reinstatement pass; breadcrumbs record **`delivery_mode`**, **`resolved_phase_plan`**, **`memory_layer=pack|quick|standard`**.

- **Composition with native chain (**DEC-0080** / **DEC-0081** / **BUG-0012** closure)**:
  - Lean modes **reduce spawns per story**; **`full_autonomy`** drain-advance, **`native_chain_continuing`**, and **`drain_advance_action`** semantics **unchanged**.
  - **`AUTO_QUIET=1`** composes — quiet must not suppress spawn scheduling.
  - **`NATIVE_CHAIN_UNAVAILABLE`** fallback boundary unchanged — delivery-mode docs must not reintroduce mandatory outer-driver prose for IDE **`full_autonomy`**.

- **Product-facing messaging constraints**:
  - **Default-off lean modes**: unset **`DELIVERY_MODE`** = **`standard`** — no behavior change for existing downstream repos.
  - **Quality floor (all modes)**: tests before stop; no secrets deny-list bypass; **`RELEASE_PUBLISH_MODE`** unchanged; compact evidence hashes allowed in lean modes but **auditable refs retained** (**AC-9**).
  - **Not amnesia**: docs must state lean modes **read** institutional memory by reference — they **compress spawn count and hot surfaces**, not delete vision/architecture/decisions.
  - **Runbook recipe**: when to use **`standard`** vs **`ultra_lean`** vs **`mega_quick`** (greenfield vs bugfix vs one-liner) — **AC-11**.

- **Optional scratchpad tuning keys (discovery-locked names)**:
  - **`LEAN_MEMORY_READ`**, **`LEAN_MEMORY_WRITE`**, **`LEAN_COLD_READ_MAX_SECTIONS`**, **`LEAN_STATE_INDEX_ROWS`**, **`AUTO_DELIVERY_ROUTING=backlog_then_scratchpad`**.

- **Top risks (carry to /research)**:
  - **R1** Partial delivery — **`ultra_lean`** enabled without **`pack.json`** / index contract → single-story vertical slice mitigates.
  - **R2** **`active-context.md`** vs **DEC-0054** triad hot-surface — rollover ownership and line budgets must not fight **`handoffs/po_to_tl.md`** / **`state.md`** caps.
  - **R3** **`standard`** regression — contract tests must assert pre-**US-0096** baseline markers unchanged when mode unset.
  - **R4** **`mega_quick`** false routing of large cross-cutting stories — eligibility guard + fail-closed reason codes.
  - **R5** **`pack.json`** vs existing **`sprints/Sxxxx/`** layout — research must lock coexistence rules (**standard** keeps sprint folders; lean adds **`work/`** tree).

- **Research asks**: **`pack.json`** schema, mode-scoped **DEC-0052** algorithm, **`active-context.md`** vs triad rollover, **`mega_quick`** eligibility table, Tranche A threshold defaults, **DEC-0062** **`delivery_mode`** field, contract-test inventory — extend **`R-0082`** before **`/architecture`**.

## Intake Notes — US-0097

- **Problem**: New projects installed with its-magic still receive the full **framework** README at repo root (~1600 lines). **US-0062** / **DEC-0045** intended framework metadata in **`its_magic/`**, but the installer manifest still copies root **`README.md`**. No workflow step bootstraps or extends a **project-specific** repo overview as stories ship.
- **Intent**: Root **`README.md`** = **project-owned** (user repo overview + developer orientation, growing per **`US-xxxx`** / sprint). **`its_magic/README.md`** = **framework-only** catalog. Mandatory **`/execute`** / **`/release`** deltas + blocking project README validator; refactor **US-0091** to framework paths only.
- **Operator constraint (hard)**: Upgrade/migration must not destroy operator-written project prose when lifting legacy framework copy; **US-0071** hygiene applies to project blurbs.
- **Alternatives considered**: (1) extend **US-0032** optional user guides only — rejected (not root README, default-off); (2) manual README edits — rejected (observed gap); (3) single combined README — rejected (conflicts with **US-0062** separation).
- **Evidence**: `handoffs/intake_evidence/US-0097-intake-20260613.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`); research stub **`R-0084`**.
- **Intake closure (2026-06-13, PO)**: Backlog **`US-0097`** **OPEN**; next **`/discovery`**.

## Discovery Notes — US-0097

- **Operator value proposition**: Downstream repos installed with its-magic open a **project-owned** root **`README.md`** — a concise repo front door (what the product does, how to run it, how developers orient) that **grows automatically** as user-visible stories ship. The **framework** catalog (~1600 lines today) lives only under **`its_magic/README.md`**; operators are never asked to manually maintain README drift each sprint.
- **Product-facing messaging constraints**:
  - **Audience split (simpler than framework)**: project README uses two operator-facing H2s — **`## For users`** (what it does, how to run/use) and **`## For developers`** (setup, repo layout, where code/tests live). Framework **`USER_*`/`DEV_*`** vocabulary and **`readme-section-affinity.json`** apply only to **`its_magic/README.md`** — not the project root.
  - **Terseness over encyclopedic guides**: per-shipped-story blurbs are **1–2 sentences** in a **`## Features`** (or **`## What's included`**) catalog — not per-feature user guides (**US-0032** / **`USER_GUIDE_MODE`** remain orthogonal, default-off).
  - **Framework pointer, not duplication**: project README may include **one optional line** pointing to **`its_magic/README.md`** for its-magic commands — no framework command catalog in the project root.
  - **Metadata hygiene** (**US-0071**): project blurbs stay operator-readable; no planning tokens (`orchestrator_run_id`, `fresh_context_marker`, etc.).
  - **Remediation vocabulary**: blocking failures use umbrella **`PROJECT_README_COVERAGE_BLOCKED`** with deterministic sub-codes (`PROJECT_README_COVERAGE_GAP:<US-xxxx>`, bootstrap/migration/placeholder variants per acceptance).
- **Project README scaffold (discovery-locked outline)** — materialized on first **`/execute`** when root README is missing or matches a **framework-placeholder sentinel**:
  1. **H1**: `# {Project Name}` — sourced from **`docs/product/vision.md`** H1 or first substantive title line.
  2. **Purpose**: 1–3 sentences from vision Problem/Value (operator voice, not framework marketing).
  3. **`## For users`**: placeholder bullets for what-it-does + how-to-run (filled as stories ship).
  4. **`## For developers`**: setup prerequisites, repo layout pointers (`src/`, `docs/`, tests).
  5. **`## Features`** with marker `<!-- project-readme-feature-catalog -->` — empty catalog until first shipped blurb.
  6. **Optional**: one-line link to **`its_magic/README.md`** for framework workflow commands.
- **Placeholder detection contract (discovery-locked for `/research`)**:
  - **Framework sentinel signals** (any → treat as placeholder): H1 `# its-magic — AI dev team`; presence of `<!-- readme-feature-coverage-catalog -->`; heading `Feature coverage catalog (US-0091)`; byte-identity with **`template/README.md`** on fresh consumer install.
  - **Operator-authored prose** (preserve on upgrade): root README **fails** sentinel match **and** contains project-specific title/purpose **or** custom sections outside framework catalog blocks.
  - **Kit-repo exception** (**R3**): its-magic framework development repo may retain a dual-purpose root README under explicit **`FRAMEWORK_KIT_REPO=1`** scratchpad — consumer repos never set this; architecture must lock detection order (kit flag → sentinel → operator prose).
- **Per-story delta contract**: each shipped **`user_visible: true`** **`US-xxxx`** adds or updates **one** catalog bullet under **`## Features`** naming the capability in operator language (optional parenthetical id). Sprint releases may add a one-line sprint cross-link — not a substitute for per-story blurbs.
- **Gate separation (discovery-locked)**:
  - **US-0091** / **`validate_readme_feature_coverage.py`** → **`its_magic/README.md`** (+ **`template/its_magic/README.md`**) only; root **`README.md`** removed from framework coverage predicate.
  - **New** **`validate_project_readme_coverage.py`** → root **`README.md`** vs DONE **`user_visible: true`** project backlog rows.
  - **`/release`** step **3g** (name architecture-locked) runs project gate alongside existing **3f** framework gate; scratchpad **`PROJECT_README_ENFORCE=1`** default post-bootstrap (**`0`** migration-only skip with evidence).
- **Tranche delivery order**: **A** installer manifest boundary + non-destructive migration → **B** execute bootstrap scaffold → **C** mandatory execute/release deltas → **D** validators + gate separation + contract tests.
- **External UX refs**: [GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) (what/why/how, link out for deep reference); industry pattern 200–800 word front door with features catalog + quick start (**R-0084**).
- **Research asks**: finalize sentinel heuristic table, kit-repo exception rules, migration merge policy, validator CLI/`--report` schema, execute/release step prose, grandfathering toggle — see **`R-0084`** before **`/architecture`**.

## Intake Notes — US-0098

- **Problem**: During development, operators want the AI to **automatically rebuild and restart** the running app (e.g. Docker containers) after code changes and **show connection parameters** — not only at QA/release. Existing **US-0065** / **US-0086** / **US-0067** cover phase validation, test routing, and release hints but not a **continuous dev-loop relaunch** with **persisted dev-environment profile**.
- **Intent**: **Default-off** scratchpad-gated **dev auto-launch profile** — agent **detects** where development runs (**local**, **docker-host-local** with direct shell/docker on the machine, optional **docker**/**ssh** automation targets), **persists** operator-seeded profile, runs **bounded** rebuild/restart during **`/execute`**, and surfaces **Connect** info (URL/port/health, names-only secrets). Operator may seed parameters once; agent maintains profile idempotently.
- **Operator constraint (hard)**: **US-0085** rules unchanged — no **`.env`** reads; no secret literals in git; manual daily work unchanged when profile **off**.
- **Alternatives considered**: (1) extend **US-0065** only — rejected (phase-gated QA, not dev-loop); (2) extend **US-0086** only — rejected (routing without relaunch/persistence); (3) file-watch daemon v1 — deferred (bounded triggers first: execute task + explicit refresh).
- **Evidence**: `handoffs/intake_evidence/US-0098-intake-20260613.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`); research stub **`R-0085`**.
- **Intake closure (2026-06-13, PO)**: Backlog **`US-0098`** **OPEN**; next **`/discovery`**.

## Discovery Notes — US-0098

- **Operator value proposition**: When the dev auto-launch profile is **on**, the AI closes the loop after implementation work — **detect** where the app runs, **rebuild/restart** bounded stacks (containers or dev server), **persist** what it learned, and **show how to connect** — without waiting for QA/release. When **off** (default), nothing changes for manual daily work (**parity with `AUTO_REMOTE_AUTOMATION_PROFILE=off`**).
- **Connect block UX (discovery-locked template)** — emitted in chat and/or **`handoffs/dev_to_qa.md`** after successful relaunch; field names align with **`runtime-connectivity.md`** operator summary where applicable:
  - **`runtime_mode`**: `local` | `docker-host-local` | `docker` | `ssh`
  - **`connect_endpoint`**: `protocol://host:port` or `host:port` (literal host/port OK when not secret-derived; env-derived endpoints cite **`*Env` names only**)
  - **`health_path`**: optional path (e.g. `/health`, `/api/health`)
  - **`service_id`** / **`container_id`**: stack slice identifier (names/ids, not credentials)
  - **`target_id`**: when automation remote (**US-0086**) — canonical **`remote.json`** / **`release-targets.json`** id
  - **`env_refs`**: list of env **names** the operator must have set (never values)
  - **`relaunch_outcome`**: `success` | `skipped` | `failed` + reason code when not success
- **Detection matrix (discovery-locked for `/research`)**:

  | Label | Meaning | Primary signals | Not this |
  |-------|---------|-----------------|----------|
  | **`local`** | Process dev server on workstation | No active compose/docker profile; **`DEV_SERVER_COMMAND`** / stack profile from repo | Remote SSH shell |
  | **`docker-host-local`** | Same-machine **`docker`** / **`docker compose`** | Compose file path in profile or repo root; docker CLI succeeds locally; operator on Docker host (not SSH hop) | **`US-0086`** remote docker-over-SSH unless profile explicitly selects remote target |
  | **`docker`** | Automation remote container target | **`AUTO_REMOTE_AUTOMATION_PROFILE`≠off** + resolved **`target_id`** with docker semantics | Default when profile off |
  | **`ssh`** | Automation remote shell target | **`AUTO_REMOTE_AUTOMATION_PROFILE`≠off** + **`ssh-server`** (or equivalent) target | Manual SSH the operator runs themselves outside automation |

- **Relaunch trigger contract (v1, discovery-locked)**:
  1. **Execute-bound (primary)**: after **`/execute`** task completion when changed files match documented **runtime/container surface classes** (e.g. `Dockerfile*`, `docker-compose*.yml`, `compose.yaml`, `package.json`, lockfiles, `requirements*.txt`, documented runtime scripts) — **bounded** retry cap (architecture-locked, e.g. max **2** attempts).
  2. **Explicit operator refresh**: phrase **`refresh dev environment`** (architecture-locked synonym table) or dedicated command hook — fail-closed when profile **off** or target unroutable.
  3. **Excluded v1**: unbounded **`docker compose watch`** / filesystem watch daemons as mandatory automation; may document as **operator-opt-in** future extension only after bounded design passes architecture gate.
- **Container recipe tiers (discovery-locked)** — map file-class → action (research closes exact table):
  - **Tier A — full rebuild**: `Dockerfile*`, dependency manifests → `docker compose build` + `up` (or stack equivalent)
  - **Tier B — restart**: config-only or non-hot-reload surfaces → `docker compose restart <service>` or process restart
  - **Tier C — local dev server**: **`local`** mode → **`DEV_SERVER_COMMAND`** / stack-aware start (reuse **`uat_probe_lib`** / **`DEV_SERVER_*`** patterns)
- **Profile persistence (discovery-locked outline)** — path candidate **`.cursor/dev-environment.json`** (architecture-locked at **`/architecture`**):
  - **`version`**, **`detected_mode`**, **`operator_seeded`**, **`last_updated`**, **`compose_file`**, **`service`**, **`connect`** (endpoint + health + `*Env` refs), **`rebuild_recipe`**, **`evidence_refs`**
  - Committed **`template/.cursor/dev-environment.json.example`** (names-only placeholders); operator-writable persisted file gitignored or local-only per **US-0085** posture
  - Agent updates **idempotent** with evidence; operator may seed once
- **Scratchpad gate (discovery-locked proposal for `/research`)** — mirror **`AUTO_REMOTE_AUTOMATION_PROFILE`** pattern:
  - **`DEV_AUTO_LAUNCH_PROFILE`**: `off` | `deterministic_v1` (default **`off`**)
  - Optional **`DEV_ENVIRONMENT_CONFIG`**: path override (default **`.cursor/dev-environment.json`**)
  - Orthogonal to **`AUTO_REMOTE_AUTOMATION_PROFILE`** — both may be off; when dev profile on + remote automation on, **US-0086** precedence applies for remote targets
- **Repo survey (2026-06-14, PO)**: no **`.cursor/dev-environment.json`** yet; scratchpad documents **`DEV_SERVER_PORT`**, **`DEV_SERVER_COMMAND`**, **`AUTO_REMOTE_AUTOMATION_PROFILE=off`**; **`runtime-connectivity.md`** + **`release-targets.json`** provide release/QA Connect shapes; **`template/.cursor/remote.json`** exists; its-magic framework repo has no project **`docker-compose.yml`** — consumer repos may; detection must be stack-aware not hard-coded to one layout.
- **External UX / market refs**:
  - [Docker Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/) — industry pattern for **sync** vs **sync+restart** vs **rebuild** by file class; informs Tier A/B mapping but **US-0098 v1 stays execute-triggered**, not background watch (**R-0085**)
  - **`runtime-connectivity.md`** operator summary template — **Connect** block field alignment for in-dev surfacing vs **US-0067** release-only hints
  - Dev-tool expectation: AI assistants with filesystem access need **explicit post-change relaunch + connection summary** because operators cannot infer container ports from code alone
- **Research asks (extend **`R-0085`**)**: finalize profile JSON schema vs **`remote.json`** / **`release-targets.json`** boundaries; file-class → relaunch tier table; execute-step wiring location; reason-code inventory (`DEV_ENV_PROFILE_*`, `DEV_ENV_RELAUNCH_*`); explicit refresh command name; **`check_intake_template_parity.py --scope=dev-environment`** manifest rows; whether companion **`DEC-xxxx`** required beyond discovery locks.

## Intake Notes — US-0099

- **Problem**: After **US-0098** shipped, operators enabling **`DEV_AUTO_LAUNCH_PROFILE`** expect **`.cursor/dev-environment.json`** to exist when scratchpad **`DEV_ENVIRONMENT_CONFIG`** points there — but install/upgrade only delivers the **example** under **`template/`**, not the local gitignored profile.
- **Proposed fix**: Non-destructive **copy-when-missing** on **`missing`**, **`upgrade`**, and **npm postinstall** — mirror smart-upgrade local-file preservation (**US-0018**).
- **Operator outcome**: Fresh install or update leaves a starter profile ready to customize (compose service, connect refs) without manual copy step.
- **Research stub**: **`R-0086`** — extend at **`/discovery`** / **`/research`** for installer hook placement and postinstall parity with **`remote.json`** patterns if any.

## Discovery Notes — US-0099

- **Operator value proposition**: After install or upgrade, a **starter dev-environment profile** exists at the resolved path so **`DEV_AUTO_LAUNCH_PROFILE=deterministic_v1`** no longer fails with **`DEV_ENV_PROFILE_MISSING`** before the operator customizes compose service or **`*Env`** connect refs. Bootstrap is **automatic and silent** when the file is absent; **customization** (editing service name, connect refs) remains operator-owned.
- **UX contrast — `remote.json` vs `dev-environment.json`**:

  | Artifact | Bootstrap posture | Rationale |
  |----------|-------------------|-----------|
  | **`.cursor/remote.json`** | **Manual seed** from **`template/.cursor/remote.json`** (gitignored; opt-in remote) | Remote execution is default-off (**`REMOTE_EXECUTION=0`**); no auto-materialize |
  | **`.cursor/dev-environment.json`** | **Auto copy-when-missing** from **`template/.cursor/dev-environment.json.example`** | **`DEV_AUTO_LAUNCH_PROFILE`** gate expects a loadable profile when enabled; install gap is the reported defect |

- **Operator flow (discovery-locked)**:
  1. **Install / upgrade / `npm install its-magic`** — installer or postinstall copies example → resolved path **only when target absent**; log line cites bootstrap outcome (names-only).
  2. **Customize** — operator edits **`service`**, **`compose_file`**, **`connect.*Env`** refs in the local profile (no re-copy required).
  3. **Enable** — set **`DEV_AUTO_LAUNCH_PROFILE=deterministic_v1`** in scratchpad; execute step **24** loads profile without **`DEV_ENV_PROFILE_MISSING`**.
  4. **Re-upgrade** — existing local profile **preserved** (**`DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`**); smart-upgrade composition with **US-0018**.
- **Hook placement (discovery-locked for `/research`)**:
  - Run **after** **`run_scratchpad_postinstall`** on **`missing`** and **`upgrade`** so merged scratchpad supplies **`DEV_ENVIRONMENT_CONFIG`** (Model B: local > baseline > example).
  - Run **before** **`bootstrap_runbook_commands`** (orthogonal concerns; bootstrap is profile file, not runbook keys).
  - **`installer.ps1`** / **`installer.sh`** delegate to **`installer.py`** (same pattern as scratchpad-postinstall).
  - Dedicated helper **`bootstrap_dev_environment_profile()`** in **`scripts/dev_environment_lib.py`** (stdlib; **`template/`** mirror).
- **Path resolution (discovery-locked)**:
  - Resolved path = parseable repo-relative **`DEV_ENVIRONMENT_CONFIG`** from merged scratchpad, else **`DEFAULT_PROFILE_PATH`** (**.cursor/dev-environment.json**).
  - Malformed override (absolute path, traversal, empty) → fail-closed **`DEV_ENV_BOOTSTRAP_PATH_INVALID`**; do not copy.
  - Source = **`template/.cursor/dev-environment.json.example`** only — never synthesize JSON at install time.
- **Reason-code family (discovery-locked)** — new **`DEV_ENV_BOOTSTRAP_*`** distinct from **`DEV_ENV_PROFILE_*`** (install-time vs runtime load):

  | Code | When |
  |------|------|
  | **`DEV_ENV_BOOTSTRAP_COPIED`** | Target absent; example copied successfully |
  | **`DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`** | Target already present; skip (non-destructive) |
  | **`DEV_ENV_BOOTSTRAP_PATH_INVALID`** | **`DEV_ENVIRONMENT_CONFIG`** override malformed |
  | **`DEV_ENV_BOOTSTRAP_SOURCE_MISSING`** | Example source absent in packaged template |

- **Runbook UX (discovery-locked)**: **`docs/engineering/runbook.md`** § Dev environment — demote "Seed profile" prerequisite copy to **"Customize bootstrap profile"**; bootstrap is automatic on install/upgrade; manual copy only when operator wants a non-default path before first install or to reset a deleted file.
- **npm `postinstall` (discovery-locked outline)**: **`bin/postinstall.js`** today is banner-only; must invoke same bootstrap contract as installer (**`npx its-magic`** / **`npm install its-magic`** consumers). Research closes subprocess vs inline Node and scratchpad-read timing for global installs.
- **Repo survey (2026-06-14, PO)**: **`installer.py`** copies manifest files but **`.cursor/dev-environment.json`** is **`.gitignore`**d and **not** in **`install_paths`**; **`upgrade`** preserves **`user-data`** prefixes but profile path is under **`.cursor/`** (framework prefix for commands/rules only — profile is **outside** manifest copy); **`bin/postinstall.js`** has no bootstrap; runbook still lists manual seed step; **`dev_environment_lib.py`** has **`load_profile`** but no bootstrap helper yet; **`DEV_ENVIRONMENT_PAIRS`** parity scope exists from **US-0098**.
- **Tranche order (discovery-locked)**: **A** helper + reason codes → **B** installer hooks (py/ps1/sh) → **C** **`postinstall.js`** → **D** runbook + contract tests + parity manifest delta.

## Intake Notes — US-0100

- **Operator request (2026-06-15)**: Document bugfixes and user stories (with short descriptions) in release documentation — both a **growing cumulative** history (all versions → US/BUG list) and **per-release** docs; wire **GitHub/git release** to attach the right release notes following official best practices; integrate with existing its-magic release concepts (**US-0040** sprint notes, **release_queue**, **RELEASE_PUBLISH_MODE**).
- **Problem framing**: Sprint-scoped notes answer "what shipped in **S0089**?" but operators and downstream consumers also need "what shipped in **v0.1.2**?" aligned with npm/git tags; **`release-all.sh`** today calls **`gh release create --generate-notes`**, which ignores canonical its-magic narrative.
- **Recommended artifact model (intake-locked for discovery)**:
  - **Cumulative**: repo-root **`CHANGELOG.md`** ([Keep a Changelog](https://keepachangelog.com/) 1.1.0 — **`[Unreleased]`** + semver sections, ISO dates).
  - **Per-version**: **`handoffs/releases/vX.Y.Z-release-notes.md`** (or architecture-locked equivalent) — body source for GitHub Releases.
  - **Sprint layer unchanged**: **`handoffs/releases/Sxxxx-release-notes.md`** remains workflow evidence (**US-0040**).
- **Derivation precedence (intake-locked)**: finalized sprint notes → backlog title/summary → queue **`story_refs`**; include **BUG-xxxx** when sprint delivered defect work.
- **Publish compose (intake-locked)**: **`gh release create vX.Y.Z -F handoffs/releases/vX.Y.Z-release-notes.md`** per GitHub CLI best practice; respect **`RELEASE_PUBLISH_MODE`** (**US-0054**); no bypass of confirm/auto gates.
- **Research stub**: **`R-0087`** — semver mapping, backfill from ~80 released sprints, optional **`.github/release.yml`** (out of scope v1 unless discovery expands).
- **Decomposition**: **single story** **US-0100** — docs + `/release` hook + publish attach + backfill + validators.
- **Intake evidence**: `handoffs/intake_evidence/US-0100-intake-20260615.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`).
- **Next**: **`/discovery`** (fresh **PO**).

## Discovery Notes — US-0100

- **Operator value proposition**: Operators and downstream consumers need a **semver-aligned release story** — "what shipped in **v0.1.2**?" with **US-xxxx** / **BUG-xxxx** one-liners — that stays truthful across repo docs, GitHub Releases, and npm/choco/brew tags. Sprint notes (**US-0040**) answer workflow evidence; version docs answer product/version evidence.
- **Problem framing vs existing artifacts**:

  | Surface | Current behavior | Gap |
  |---------|------------------|-----|
  | **`handoffs/releases/Sxxxx-release-notes.md`** | Rich per-sprint notes (gates, Run/Connect/Verify per **US-0067**) | No semver rollup; not suitable as GitHub body wholesale |
  | **`handoffs/release_queue.md`** | **`release_version`** column exists but **mostly empty** (sparse values e.g. **`0.1.2-30`**, **`0.1.2-41`**) | No deterministic version→work-item index |
  | **`handoffs/release_notes.md`** | Legacy latest pointer only | Not cumulative history |
  | **`CHANGELOG.md`** | **Absent** | No growing version history |
  | **`handoffs/releases/vX.Y.Z-release-notes.md`** | **Absent** | No canonical GitHub/git body file |
  | **`scripts/release-all.sh`** | **`gh release create "$TAG_NAME" --generate-notes`** (lines 94–99) | Ignores its-magic narrative; auto-generated PR list |
  | **`/release` command** | Writes sprint notes + queue; optional **`RELEASE_PUBLISH_MODE`** targets | No version-doc derivation hook |
  | **`package.json`** | **`version`: `0.1.2`** | Semver source for **`release-all.sh`** bump, not yet bound to workflow releases |

- **Repo survey (discovery)**:
  - **79** shipped sprint note files under **`handoffs/releases/S*-release-notes.md`** (plus template **`Sxxxx`** stub); queue rows from **`S0011`** through **`S0089`** with **`status=released`**.
  - **`release-all.sh`** flow: **`npm version`** bump → npm publish → **`gh release create --generate-notes`** → choco/brew formula updates; **no** read of sprint notes or queue.
  - Scratchpad **`RELEASE_PUBLISH_MODE=disabled`**; **`RELEASE_TARGETS_FILE=docs/engineering/release-targets.json`** — workflow **`/release`** and operator **`release-all.sh`** are **separate paths** today; **US-0100** must document when each path writes version docs vs when publish attaches them.
  - Sprint note shape (e.g. **`S0089`**) includes **`## What's new`** bullets and **`story_refs`** — primary derivation feed for version summaries.

- **UX / operator workflow (discovery-locked)**:

  | Workflow | Operator intent | **US-0100** posture |
  |----------|-----------------|---------------------|
  | **`/release`** (workflow gate) | Finalize sprint after QA/UAT | After gates pass: derive **per-version doc** + append **CHANGELOG** section for bound **`release_version`**; populate queue **`release_version`** when semver known |
  | **`scripts/release-all.sh`** | Bump semver, npm/choco/brew + GitHub tag | After bump: use **`gh release create vX.Y.Z -F handoffs/releases/vX.Y.Z-release-notes.md`** when file exists; documented fallback when missing |
  | **CI tag push** | Automated publish | Same **`-F`** contract; no **`--generate-notes`** when canonical file present |
  | **Read cumulative history** | Audit all versions | Open repo-root **`CHANGELOG.md`** |
  | **Read sprint detail** | Run/Connect/Verify | Unchanged **`Sxxxx-release-notes.md`**; version doc cross-links sprint refs |

- **Version doc content shape (discovery-locked template)** — per-version file is **consumer-facing** (GitHub Release body + changelog section source); **not** a duplicate of full sprint gate narrative:
  - Header: version, date (ISO), git tag **`vX.Y.Z`**
  - **`## Work items`**: bullet list **`US-xxxx`** / **`BUG-xxxx`** — **one-line summary** each (from backlog title/summary or sprint **What's new**)
  - **`## Sprint evidence`**: links to **`handoffs/releases/Sxxxx-release-notes.md`** for each contributing sprint
  - **`## Operator quick links`**: pointer to **US-0067** Run/Connect/Verify in sprint notes (not duplicated inline)
  - Metadata hygiene (**US-0071**): no inline secrets; env-ref-only where credentials mentioned

- **Cumulative changelog shape (discovery-locked)** — [Keep a Changelog](https://keepachangelog.com/) **1.1.0**:
  - Repo-root **`CHANGELOG.md`**
  - Top: **`[Unreleased]`** (workflow releases not yet bound to semver)
  - Sections: **`## [X.Y.Z] - YYYY-MM-DD`** newest-first
  - Each version lists **US/BUG** ids + one-liners (may use **Added** / **Changed** / **Fixed** categories when research maps story kind → category)

- **Discovery locks for `/research` and `/architecture`** (14 locks):

  | # | Lock | Discovery decision |
  |---|------|-------------------|
  | L1 | **Cumulative path** | Repo-root **`CHANGELOG.md`** (Keep a Changelog 1.1.0) |
  | L2 | **Per-version path** | **`handoffs/releases/vX.Y.Z-release-notes.md`** (semver in filename; **`v` prefix stripped in filename**) |
  | L3 | **Sprint layer** | **`handoffs/releases/Sxxxx-release-notes.md`** unchanged (**US-0040**); never overwritten by version layer |
  | L4 | **Derivation precedence** | Finalized sprint notes (**What's new** / **story_refs**) → backlog title/summary → queue **`story_refs`**; include **BUG-xxxx** when sprint delivered defect work |
  | L5 | **GitHub body source-of-truth** | Per-version markdown file only; **`gh release create … -F <file>`**; **no `--generate-notes`** when canonical file exists |
  | L6 | **`release_version` binding** | Populate queue column on **`/release`** finalization when semver known; **`release-all.sh`** uses post-**`npm version`** value as authoritative for publish attach |
  | L7 | **Idempotency** | Re-run **`/release`** for same sprint/version must not duplicate CHANGELOG sections or per-version files |
  | L8 | **Backfill scope** | One-time/idempotent script from **~79** **`released`** queue rows + sprint notes; best-effort semver when **`release_version`** empty — operator remediation for ambiguous rows |
  | L9 | **Multi-sprint → semver** | **Open for research** — when multiple sprints share one npm publish, coalesce work items under one version section (do not drop sprint cross-links) |
  | L10 | **US-0067 compose** | Run/Connect/Verify remain sprint-note-only; version docs summarize work items + link sprint evidence |
  | L11 | **US-0054 compose** | GitHub attach respects **`RELEASE_PUBLISH_MODE`**; workflow **`/release`** may write docs under **`disabled`**; publish execution still gated |
  | L12 | **Workflow separation** | Document three paths: workflow-only **`/release`**, operator **`release-all.sh`**, CI tag — each with explicit version-doc touchpoints |
  | L13 | **Fail-closed fallbacks** | Reason-code family: **`RELEASE_CHANGELOG_VERSION_MISSING`**, **`RELEASE_CHANGELOG_DUPLICATE_VERSION`**, **`RELEASE_CHANGELOG_WORK_ITEM_GAP`**, plus documented skip/fail when **`gh`** absent or notes file missing |
  | L14 | **Validator** | **`scripts/release_changelog_validate.py`** (name locked at discovery; architecture may extend flags) |

- **Research open questions (carry to `/research` via `R-0087`)**:
  - **Q1**: Deterministic backfill semver assignment when **`release_version`** blank for most historical rows.
  - **Q2**: Category mapping (Added/Changed/Fixed) vs flat US/BUG list for Keep a Changelog compliance.
  - **Q3**: Whether workflow-only **`/release`** (no npm bump) appends to **`[Unreleased]`** only or requires explicit semver.
  - **Q4**: Coalesce algorithm when **`release-all.sh`** publishes one version covering multiple sprints since last tag.
  - **Q5**: Template parity surfaces (**`template/handoffs/releases/`**, **`template/.cursor/commands/release.md`**, optional **`template/CHANGELOG.md`** stub).

- **Design references**: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/); [GitHub CLI `gh release create -F`](https://cli.github.com/manual/gh_release_create); existing sprint note exemplar **`handoffs/releases/S0089-release-notes.md`**.
- **Research anchor**: **`R-0087`** — extend at **`/research`** with repo survey closure and Q1–Q5 answers.
- **Intake evidence**: `handoffs/intake_evidence/US-0100-intake-20260615.json`.
- **Next**: **`/research`** (fresh **tech-lead**).

## Intake Notes — US-0101

- **Operator request (2026-06-14)**: Per its-magic phase, use cheaper models for light work and strong models for coding — automatically via rules/commands/`/auto`, without brittle hardcoded model IDs; support dynamic local slug catalog; document API-only mode when only BYOK models are active.
- **Problem framing**: **`TOKEN_PROFILE`** (**US-0080** / **DEC-0062**) reduces context breadth, not LLM choice. Subagent **`model:`** in **`.cursor/agents/`** is the Cursor-native hook, but the framework ships no tier contract, no local catalog, and no provider-mode guidance.
- **Recommended model (intake-locked)**:
  - **`MODEL_TIER_<phase>=cheap|balanced|strong`** in scratchpad (local override precedence per **DEC-0055**).
  - Template agents use **`fast`** / **`inherit`** only; operator slugs in **`.cursor/model-catalog.local.json`** (gitignored).
  - **`MODEL_PROVIDER_MODE=cursor|api`** documented with subagent BYOK limitations.
- **Default matrix**: cheap → ask/refresh/memory-audit; balanced → intake/discovery/research/release/plan-verify; strong → architecture/execute/qa/verify-work/security-review.
- **Decomposition**: **single story** **US-0101**.
- **Research stub**: **`R-0088`** — materializer design, catalog schema, contract tests, UI precedence.
- **Intake evidence**: `handoffs/intake_evidence/US-0101-intake-20260614.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`).
- **Next**: **`/discovery`** (fresh **PO**).

## Discovery Notes — US-0101

- **Discovery date**: 2026-06-15T20:00:00Z
- **Problem framing**: Operators need per-phase LLM strength control (cheap for light work like ask/refresh-context, strong for coding/architecture) without hardcoding volatile vendor model IDs in template agent files. Current state: all subagents inherit one parent model or use ad-hoc `model:` slugs — no framework tier contract, no local catalog, no provider-mode guidance.
- **Recommended approach (discovery-locked)**:
  - `MODEL_TIER_<phase>=cheap|balanced|strong` in scratchpad with local override precedence per DEC-0055.
  - Tier→alias resolution: `cheap` → `fast`, `strong` → `inherit`, `balanced` → `inherit` or documented middle alias (open for research).
  - Template agents use aliases only (`fast`/`inherit`); operator slugs in `.cursor/model-catalog.local.json` (gitignored).
  - `MODEL_PROVIDER_MODE=cursor|api` documented with subagent BYOK limitations.
  - Orthogonal to `TOKEN_PROFILE` (DEC-0062 — context breadth only, never model choice).
- **12 discovery locks (L1–L12)**:
  | # | Lock | Decision |
  |---|------|----------|
  | L1 | **Tier enum** | `cheap` / `balanced` / `strong` — three-tier model |
  | L2 | **Default phase→tier matrix** | cheap: ask/refresh-context/memory-audit/status-reconcile/pause; balanced: intake/discovery/research/release/plan-verify; strong: architecture/execute/qa/verify-work/security-review |
  | L3 | **Tier→alias resolution** | `cheap` → `fast`, `strong` → `inherit`; `balanced` → open for research (inherit vs middle alias) |
  | L4 | **Local catalog schema** | `.cursor/model-catalog.local.json` (gitignored) + `.example.json`; maps tier → operator slug string |
  | L5 | **Template agent defaults** | aliases only in `template/.cursor/agents/`; no hardcoded vendor slugs |
  | L6 | **Provider mode runbook** | `MODEL_PROVIDER_MODE=cursor|api` subsection in runbook + auto-orchestration-reference |
  | L7 | **Scratchpad merge precedence** | local > materialized > example per DEC-0055 |
  | L8 | **Orthogonality vs TOKEN_PROFILE** | explicit non-substitution paragraph; MODEL_TIER ≠ TOKEN_PROFILE |
  | L9 | **Fail-closed reason codes** | `MODEL_TIER_INVALID`, `MODEL_CATALOG_INVALID`, `MODEL_RESOLVE_FALLBACK`, `MODEL_SLUG_UNKNOWN` |
  | L10 | **Contract test inventory** | `test_us0101_*` markers for scratchpad keys, matrix literals, orthogonality, template aliases, forbidden slug grep |
  | L11 | **Template parity scope** | `check_intake_template_parity.py --scope=model-tier` when surfaces touched |
  | L12 | **DEC-0062 compose** | new decision composes DEC-0062 without amending TOKEN_PROFILE tier meanings |
- **Research open questions (carry to `/research` via `R-0088`)**:
  - Q1: Finalize tier→alias mapping — balanced→inherit stable? middle alias?
  - Q2: Local catalog JSON schema + resolver algorithm details.
  - Q3: Agent template defaults — which roles get `fast` vs `inherit`?
  - Q4: Provider mode runbook UX — how to document BYOK limitations clearly.
  - Q5: Contract-test inventory + parity scope finalization.
- **Risks**:
  - R1: Cursor subagent BYOK limitation may limit api-only mode practical value.
  - R2: Balanced tier alias ambiguity — inherit vs new middle alias.
  - R3: Materializer hook scope — scratchpad-only vs active agent rewrite.
- **Design references**: existing `TOKEN_PROFILE` pattern (DEC-0062), `MODEL_PROVIDER_MODE` operator concept, `.cursor/agents/*.mdc` template structure.
- **Research anchor**: **`R-0088`** — extend at `/research` with Q1–Q5 answers.
- **Intake evidence**: `handoffs/intake_evidence/US-0101-intake-20260614.json`.
- **Next**: **`/research`** (fresh **tech-lead**).

## Discovery Notes — US-0110

- **Discovery date**: 2026-06-28T17:00:00Z
- **Orchestrator run**: `auto-20260628-04`
- **Problem framing**: Sovereign-loop autonomous delivery needs a deterministic **terminal condition** beyond per-segment phase exhaustion. Operators enabling goal-driven autonomy must see **mid-loop progress** toward an explicit or auto-derived goal and receive a **partial delivery report** when timeout caps exhaust before convergence. Today **US-0088**/**US-0092**/**US-0095** stop on segment/phase boundaries; **US-0044** drains OPEN stories but has no unified "project complete" predicate.
- **Recommended approach (discovery-locked)**:
  - `SOVEREIGN_GOAL_MODE=phase_driven|goal_convergence` (default `phase_driven`) — backward compatible.
  - `scripts/sovereign_convergence_lib.py` exposes `evaluate_convergence(repo, scratchpad)` returning `{converged, unmet_conditions[], blocked_by[]}`.
  - Convergence = all OPEN stories DONE + zero deferrals + cross-reviewer findings resolved + smoke probe green + ledger has no unapproved extensions.
  - Goal text via `SOVEREIGN_GOAL=<text>` or auto-derive from `docs/product/vision.md` top-N paragraphs.
  - Curator `/refresh-context` emits `goal_progress` block in `handoffs/resume_brief.md` during active goal-convergence loops.
  - Timeout → `SOVEREIGN_GOAL_TIMEOUT` reason code + `handoffs/sovereign_partial_delivery.md`.
- **12 discovery locks (L1–L12)**: see `docs/product/backlog.md` `## US-0110` `discovery_notes`.
- **Compose do NOT amend**: **US-0088**, **US-0092**, **US-0095**, **US-0044**, **US-0103** (read-only integration).
- **Foundation for**: **US-0107** (drain-generate + notification on convergence/timeout).
- **Research open questions (carry to `/research` via `R-0091`)**:
  - Q1: JSON schemas for `ConvergenceResult` + `goal_progress` block.
  - Q2: Full helper library API + CLI surface.
  - Q3: Graceful degrade when **US-0104**/**US-0107** artifacts not yet deployed.
  - Q4: Vision auto-derive algorithm details.
  - Q5: Contract-test inventory + parity scope.
  - Q6: Performance budget for drain-loop re-evaluation.
  - Q7: Companion DEC necessity.
- **Risks**: R1 predicate cost; R2 upstream artifact absence; R3 smoke probe canonical source; R4 native-chain interaction; R5 timeout semantics.
- **Research anchor**: **`R-0091`** (note: **`R-0090`** reserved for **US-0112**).
- **Intake evidence**: `handoffs/intake_evidence/intake-sovereign-20260627-01.json` (batch — skip re-intake).
- **Next**: **`/research`** (fresh **tech-lead**).

## Discovery Notes — US-0104

- **Discovery date**: 2026-06-28T21:35:00Z
- **Orchestrator run**: `auto-20260628-04`
- **Problem framing**: Sovereign-loop autonomous delivery benefits from **adversarial second opinion** at phase boundaries — a critic using a **different model** than the producer reduces single-model blind spots (edge-case misses, boundary violations, over-engineering). Intake locked three evaluation lenses and anti-slop scoring with rework. **US-0103** ledger already reserves **`cross_model_reviewed`**; **US-0110** convergence conjunct 3 already reads **`handoffs/sovereign_critic_findings.jsonl`** — US-0104 **implements** the producer surface those stories consume.
- **Recommended approach (discovery-locked)**:
  - Default-off **`CROSS_MODEL_REVIEW=0|1`** scratchpad gate (zero overhead when `0`).
  - After each producer phase (when enabled), **`/sovereign-critic`** spawns fresh critic subagent with **different `model_id`** (via **US-0101** / **US-0102** resolution).
  - Three fixed lenses: **Challenger** (edge cases), **Architect** (coupling/boundaries), **Subtractor** (YAGNI/over-engineering).
  - Parallel-jury reconciliation in **`scripts/sovereign_critic_lib.py`**: agreement → high confidence; single-finder → flagged medium confidence.
  - **`model_id`** additive field on **US-0048** isolation evidence for producer + critic runs.
  - Anti-slop: per-lens 0–10 scores; aggregate below threshold → bounded producer rework loop.
  - Degraded **single-model-multi-lens** when only one model resolvable (informational, not hard stop).
- **12 discovery locks (L1–L12)**: see `docs/product/backlog.md` `## US-0104` `discovery_notes`.
- **Compose do NOT amend**: **US-0048**, **US-0069**, **US-0023**, **US-0110** (read/write integration only); **US-0103** ledger field **`cross_model_reviewed`** consumed, not schema-changed.
- **Downstream consumers**: **US-0110** (critic-resolved conjunct), **US-0108** (anti-slop selection predicate), **US-0107** (sovereign loop orchestration).
- **Research open questions (carry to `/research` via `R-0092`)**:
  - Q1: Findings JSONL exact schema + validator CLI.
  - Q2: Reconciliation library API + issue-normalization key.
  - Q3: Cross-model selection algorithm (different slug than producer).
  - Q4: Anti-slop rubric + rework loop orchestration contract.
  - Q5: Isolation evidence `model_id` v2 extension matrix.
  - Q6: Contract-test inventory + parity scope.
  - Q7: Companion DEC necessity.
- **Risks**: R1 model routing reliability; R2 phase cost; R3 rework oscillation; R4 anti-slop determinism; R5 findings dedup; R6 US-0108 score stability.
- **Research anchor**: **`R-0092`** (note: **`R-0090`** = **US-0112**, **`R-0091`** = **US-0110** delivered).
- **Intake evidence**: `handoffs/intake_evidence/intake-sovereign-20260627-01.json` (batch — skip re-intake).
- **Next**: **`/research`** (fresh **tech-lead**).

## Discovery Notes — US-0105

- **Discovery date**: 2026-06-29T00:05:00Z
- **Orchestrator run**: `auto-20260628-04`
- **Problem framing**: Autonomous sovereign-loop delivery accumulates institutional knowledge (decisions, mistakes, patterns, plan drift) across runs, but today that knowledge is scattered across sprint artifacts, ledger files, and operator memory — subagents repeat errors and rediscover patterns. **US-0103** ledger audits per-run decisions; **US-0029** captures external web research — neither provides a **bounded, injectable project-level learnings substrate** for phase spawns. **US-0105** implements that substrate without amending research or token-cost contracts.
- **Recommended approach (discovery-locked)**:
  - Default-off **`SOVEREIGN_MEMORY=0|1`** scratchpad gate (zero overhead when `0`).
  - **`docs/engineering/sovereign-memory/`** with four JSONL artifacts + **`retrospectives/<sprint_id>.md`**.
  - **`scripts/sovereign_memory_lib.py`** assembles **top-N recent + top-K high-impact** digest capped by **`SOVEREIGN_MEMORY_MAX_CHARS`**.
  - Phase spawn receives read-only **`sovereign_memory_digest`** block (additive to **US-0023** fresh context).
  - Curator **`/refresh-context`** writes sprint retrospective after release; optional promotion from **US-0103** ledger.
  - Dedup on **`decisions-log.jsonl`**; mistake-tagging on failed fix/revert / fidelity violations.
- **12 discovery locks (L1–L12)**: see `docs/product/backlog.md` `## US-0105` `discovery_notes` (includes directory design-intent table).
- **Compose do NOT amend**: **US-0029** (external research), **US-0080** / **DEC-0062** (token-cost / slim commands), **US-0096** (per-story lean memory layers), **US-0103** (per-run ledger schema).
- **Downstream consumers**: **US-0107** (drain-generate reads sovereign memory + vision), **US-0110** (convergence reporting may reference drift register).
- **Research open questions (carry to `/research` via `R-0093`)**:
  - Q1: JSONL v1 exact schemas + validator CLI.
  - Q2: `sovereign_memory_lib.py` full API sketch.
  - Q3: Injection merge algorithm edge cases.
  - Q4: Mistake-tagging orchestrator wiring + **US-0103** compose.
  - Q5: JSONL rollover/archive vs **US-0072**.
  - Q6: Contract-test inventory + parity scope.
  - Q7: Companion DEC necessity.
- **Risks**: R1 token bloat; R2 research vs learnings overlap; R3 ledger vs decisions-log confusion; R4 stale injection; R5 secret leakage; R6 US-0107 API coupling.
- **Research anchor**: **`R-0093`** (note: **`R-0092`** = **US-0104** delivered).
- **Intake evidence**: `handoffs/intake_evidence/intake-sovereign-20260627-01.json` (batch — skip re-intake).
- **Next**: **`/research`** (fresh **tech-lead**).

## Discovery Notes — US-0107

- **Discovery date**: 2026-06-29T00:15:00Z
- **Orchestrator run**: `auto-20260628-04`
- **Problem framing**: Sovereign-loop batch foundations (**US-0110** convergence, **US-0103** ledger, **US-0105** memory, **US-0104** critic) are shipped or in flight — but **`/auto`** still stops when the backlog drains without a unified **project-complete** path, when recoverable blocks dead-end the loop, or when the operator must manually enqueue follow-on work. **US-0107** implements **`AUTO_SOVEREIGN`** — the orchestration mode that owns deferrals, drain-generate, notifications, and convergence hooks **on top of** **US-0088**/**US-0092**/**US-0095** (unchanged).
- **Recommended approach (discovery-locked)**:
  - Default-off **`AUTO_SOVEREIGN=0|1`** scratchpad gate (orthogonal to **`AUTO_FLOW_MODE=full_autonomy`**).
  - **`handoffs/sovereign_deferrals.jsonl`** bounded deferral register with orchestrator advance logic.
  - **Drain-generate**: when zero OPEN stories but **`evaluate_convergence()`** not satisfied → fresh **PO** spawn from **`vision.md`** + sovereign memory → **decision gate per candidate** before backlog persistence.
  - **Notification**: **`SOVEREIGN_NOTIFY_TARGET`** (ntfy|email|hook) on convergence, timeout, or cap exhaustion — fail-open.
  - **Convergence hooks**: import **US-0110** **`evaluate_convergence`** as terminal predicate + drain-generate gate; **US-0109** **`DEPLOY_DEFERRED`** writes to register (integration declaration only in US-0107).
- **12 discovery locks (L1–L12)**: see `docs/product/backlog.md` `## US-0107` `discovery_notes` (includes sovereign loop design-intent table).
- **Compose do NOT amend**: **US-0088**, **US-0092**, **US-0095**, **US-0044**, **US-0103** (ledger schema), **US-0105** (memory schemas), **US-0110** (five-conjunct predicate / **DEC-0110**).
- **Upstream dependencies (shipped)**: **US-0110** (convergence lib), **US-0103** (ledger), **US-0105** (memory read API), **US-0104** (critic — convergence conjunct 3).
- **Downstream consumers**: **US-0109** (writes **`DEPLOY_DEFERRED`** deferrals), **US-0108** (parallel dev — orthogonal v1).
- **Research open questions (carry to `/research` via `R-0094`)**:
  - Q1: Deferral JSONL exact schema + validator CLI.
  - Q2: **`sovereign_loop_lib.py`** full API + **`SovereignLoopStepResult`**.
  - Q3: Drain-generate PO spawn contract + candidate bundle schema.
  - Q4: Notification adapter matrix (ntfy/hook v1; email defer).
  - Q5: **`AUTO_SOVEREIGN=1`** × **`SOVEREIGN_GOAL_MODE`** coupling semantics.
  - Q6: Contract-test inventory + parity scope.
  - Q7: Companion DEC necessity.
- **Risks**: R1 goal-mode coupling; R2 drain-generate scope creep; R3 deferral cap vs convergence; R4 notification secrets; R5 native-chain interaction; R6 US-0109 schema ordering.
- **Research anchor**: **`R-0094`** (note: **`R-0093`** = **US-0105** delivered).
- **Intake evidence**: `handoffs/intake_evidence/intake-sovereign-20260627-01.json` (batch — skip re-intake).
- **Next**: **`/research`** (fresh **tech-lead**).

## Discovery Notes — US-0106

- **Discovery date**: 2026-06-29T00:25:00Z
- **Orchestrator run**: `auto-20260628-04`
- **Problem framing**: Sovereign-loop foundations (**US-0110**, **US-0103**, **US-0105**, **US-0104**, **US-0107**) ship deterministic convergence, audit, memory, adversarial critique, and loop orchestration — but **US-0069** enforces *which role runs each phase* without declaring *what each role optimizes for* or *which cross-role reviews are mandatory* at phase boundaries. Operators enabling full autonomy need a **single bootstrappable YAML manifest** for per-role objectives and directed review obligations (PO→architecture user-value, QA→acceptance testability, dev→architecture buildability, release→QA deployability) without amending the phase→role matrix.
- **Recommended approach (discovery-locked)**:
  - Default-off **`SOVEREIGN_ROLE_MANIFEST=0|1`** scratchpad gate (zero overhead when **`0`**).
  - **`.cursor/sovereign-role-manifest.yaml`** with **`roles[]`**, **`review_obligations[]`**, **`allowed_self_overrides`**, **`cross_model_policy`**, **`escalation_rules`**.
  - Bounded **`role_objective_block`** injection at spawn for **US-0069**-resolved role (compose **US-0105** digest — additive read-only inputs).
  - Post-phase **cross-role review dispatch** (spawn-only, capped) → **`handoffs/sovereign_role_reviews.jsonl`**.
  - **`cross_model_policy`** composes **US-0104** critic ordering without amending critic schema.
- **12 discovery locks (L1–L12)**: see `docs/product/backlog.md` `## US-0106` `discovery_notes` (includes role-behavior design-intent table).
- **Compose do NOT amend**: **US-0069** / **US-0003** (phase→role matrix + preflight/post checkpoint validation), **US-0104** (critic findings schema), **US-0103** / **US-0105** (ledger/memory schemas), **US-0107** (deferral register schema — compose via **`escalation_rules`** only).
- **Upstream dependencies (shipped)**: **US-0110**, **US-0103**, **US-0105**, **US-0104**, **US-0107**.
- **Research open questions (carry to `/research` via `R-0095`)**:
  - Q1: YAML v1 exact schema + validator CLI.
  - Q2: **`sovereign_role_manifest_lib.py`** full API sketch.
  - Q3: Cross-role review spawn contract + reviews JSONL + **US-0069** boundary token.
  - Q4: **`cross_model_policy`** ordering matrix vs **US-0104**.
  - Q5: **`escalation_rules`** + **US-0107** deferral compose.
  - Q6: Contract-test inventory + parity scope.
  - Q7: Companion DEC necessity.
- **Risks**: R1 spawn depth/latency; R2 role collapse vs **US-0069**; R3 **US-0104** interaction; R4 manifest/matrix drift; R5 escalation oscillation; R6 secret leakage.
- **Research anchor**: **`R-0095`** (note: **`R-0094`** = **US-0107** delivered).
- **Intake evidence**: `handoffs/intake_evidence/intake-sovereign-20260627-01.json` (batch — skip re-intake).
- **Next**: **`/research`** (fresh **tech-lead**).

## Intake Notes — US-0112

- **Intake date**: 2026-06-28
- **Operator request**: Model-catalog example presets (eight **`model-catalog.local.example*.json`** files) should ship on its-magic **install/upgrade**, not only live in the its-magic dev repo **`template/`**.
- **Problem**: **US-0101**/**US-0102** documented and committed examples, but **`installer-owned-paths.manifest`** never included them — operators enabling **`MODEL_RESOLVE=local_catalog`** or **`role_catalog`** must manually copy presets.
- **Recommended approach (intake-locked)**:
  - Manifest lists all eight example files under **`.cursor/`**.
  - **Framework** delivery: refresh on **`upgrade`**, add on **`missing`** — same family as **`scratchpad.local.example.md`** (**US-0075**).
  - **Never** auto-write **`model-catalog.local.json`** — operator copies chosen preset after install (multiple complexity/role options).
- **Decomposition**: single story (**US-0051**).
- **Intake evidence**: `handoffs/intake_evidence/US-0112-intake-20260628.json`
- **Next**: **`/architecture`** (fresh **tech-lead**)

## Intake Notes — US-0121

- **Intake date**: 2026-08-22T21:15:00Z
- **Orchestrator / run**: `cursor-20260822-opencode-adapter-intake` (`writer_id=po-cursor-20260822`)
- **Operator request**: German “führe einen intake mit diesem plan aus” with `docs/product/opencode-adapter-masterplan.md`.
- **Epic**: **US-0121..US-0126** (OpenCode host adapter in this repo). First slice **US-0121** (pack + installer). Siblings **US-0122** (role agents + permissions), **US-0123** (model slug routing), **US-0124** (orchestrator plugin spawn), **US-0125** (thin commands + validator bridge), **US-0126** (docs + contract tests) are **OPEN**.
- **Problem framing**: Cursor rules are advisory; BYOK keys do not apply to Cursor subagents; per-role models are aliases. Operators need host-enforced spawn, own provider keys (including Chinese APIs), and the same Python fail-closed kernel on **stock OpenCode**.
- **Recommended approach (intake-locked)**:
  - Host-adapter on unmodified OpenCode (kernel + `.opencode/` pack + one orchestrator plugin). Cursor pack stays.
  - Default install host remains **cursor-only** until explicit `--host opencode|both`.
  - Layer 1 plugin + permissions + Python > Layer 2 short agent prompts > Layer 3 thin commands.
  - Plugin API v1 vs v2 deferred to **`/research`** (**R-0109**).
  - Standalone runtime is a **separate program** (`docs/product/standalone-runtime-masterplan.md`) — not this intake.
- **Decomposition (US-0051)**: six vertical workflow-step slices (operator accepted via submitting the masterplan). Do not clone US-0001–US-0119.
- **Assumptions confirmed**: Default install host remains cursor-only until explicit `--host opencode|both` opt-in; OpenCode plugin v1 vs v2 deferred to `/research`.
- **Intake evidence**: `handoffs/intake_evidence/US-0121-intake-20260822.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`, `first-intake-pack`, `coverage_complete=true`).
- **Research stub**: **R-0109**.
- **Next**: **`/discovery`** (fresh **PO**) for **US-0121**, with epic context that US-0122–US-0126 remain OPEN siblings.

## Discovery Notes — US-0121

- **Story**: OpenCode template pack and installer `--host cursor|opencode|both` (first epic slice; siblings US-0122..US-0126 remain OPEN).
- **References**: `docs/product/opencode-adapter-masterplan.md` (brief — pack + installer + coexistence only; not shipped architecture); intake evidence `handoffs/intake_evidence/US-0121-intake-20260822.json`; research stub **R-0109** (deepen in `/research`; do not treat Q1–Q5 as architecture locks).
- **Operator UX**:
  - No new its-magic GUI. Operators use stock OpenCode TUI / desktop / IDE; Cursor users keep the existing Cursor pack unless they opt in.
  - Installer `--help` documents `--host cursor|opencode|both`. Omitted `--host` means **cursor**. Unknown values fail closed with `INSTALL_HOST_INVALID` (ASCII/CLI diagnostics, not a GUI).
  - Default install remains **cursor-only**. OpenCode files appear only after explicit `--host opencode` or `--host both`.
  - Dual-host (`--host both`) leaves `.cursor/` and `.opencode/` side by side. `--host opencode` must not mutate `.cursor/`.
  - Empty-but-valid pack: a consumer repo can receive `.opencode/` before role agents (US-0122) or the orchestrator plugin (US-0124) exist. Kit slash-command names stay; this slice does not clone Cursor command bodies.
- **Pack UX**: `template/.opencode/` ships `agents/`, `commands/`, `plugins/` (or a documented equivalent) plus gitignore so local model catalogs and auth files are not copied into git. Examples must not embed API keys, `.env` contents, or vendor model slugs (US-0102).
- **Compose**: Additive host switch on US-0008 only. No VS Code contrib rewrite. No OpenCode fork. Kernel paths (`docs/`, `scripts/`, `its_magic/`, …) stay host-agnostic unless `/research` proves otherwise.
- **Out of scope for this slice**: US-0122 role agents, US-0123 model slugs, US-0124 plugin spawn, US-0125 thin command bodies beyond placeholders, US-0126 full runbook, standalone runtime.
- **Next**: `/research` (tech-lead) to deepen **R-0109** (Q1–Q5 remain open; add pack/manifest/gitignore questions from discovery).

## Discovery Notes — US-0122

- **Story**: OpenCode role agents and Layer-1 permission table (second OpenCode adapter slice; US-0121 is DONE, siblings US-0123..US-0126 remain OPEN).
- **References**: `docs/product/opencode-adapter-masterplan.md`; intake evidence `handoffs/intake_evidence/US-0121-intake-20260822.json` (`role-agents-permissions` → US-0122, `coverage_complete=true`); research anchor **R-0109**.
- **Operator UX**:
  - Operators can manually invoke `@po`, `@dev`, etc. (or OpenCode equivalent) before the US-0124 orchestrator plugin exists.
  - Role prompts stay short and readable; the visible UX is role names plus clear permission failures, not copied Cursor command manuals.
  - Permission denial should produce deterministic, actionable diagnostics suitable for ASCII CLI/TUI workflows.
- **Layer-1 permission expectation**: host permissions enforce who can edit product docs, engineering docs, code, release artifacts, and child tasks. A prompt-ignoring PO must still be unable to write production code when `edit` is denied.
- **Compose**: reuse the US-0003 role set and US-0023/BUG-0006 spawn-isolation posture; do not clone `.cursor/agents`, `.cursor/rules`, skills, or command bodies as enforcement.
- **Open questions for `/research` (8)**: exact project file form; `edit` allow/deny precedence; deny-over-allow glob behavior; `task` allow-list syntax; hidden/manual settings for primary vs subagents; security findings-only write surface; contract harness for prompt-ignoring denial; whether active kit mirrors stay template-only until US-0126.
- **Next**: `/research` (tech-lead) to deepen **R-0109** for US-0122, then `/architecture` to lock the permission matrix.

## Intake Notes — US-0123

- **Intake date**: 2026-08-24T15:48:00Z (UTC)
- **Orchestrator / run**: `auto-20260824-01` (drain-advance from US-0122 DONE; spec macro = intake + discovery merged, ultra_lean)
- **Role / model**: po / `glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required on isolation)
- **Story**: US-0123 — Per-role OpenCode model slug routing (multi-provider). **Status: OPEN**. No new story ID allocated (reuse existing US-0123).
- **Intake evidence (reused, program bundle)**: `handoffs/intake_evidence/US-0121-intake-20260822.json` — `model-slug-routing` → [US-0123], `coverage_complete=true`, `selected_pack=first-intake-pack`, `missing_topics=[]`. Intake evidence JSON was NOT mutated (security: never mutate prior intake evidence).
- **AC contract**: AC-1..AC-10 remain the contract (unchanged). Acceptance checkboxes remain **unchecked**. Status remains **OPEN**. Do not mark US-0123 DONE.
- **Source-of-truth question for `/research` (AC-1)**: where does the kit-tier/role/phase → OpenCode `provider/slug` mapping live? Three candidates: (a) `.cursor/scratchpad.local.md` `MODEL_*` keys (kit-owned, operator-overridable); (b) `model:` YAML frontmatter in `template/.opencode/agents/<role>.md` (per-role, but risks vendor slug leakage in template — US-0102 family); (c) a **local-only** catalog file (e.g. `.opencode/model-catalog.local.json`, gitignored, never in `template/`). Architecture must pick **one** source of truth and tests must assert that choice; the other two become either fail-closed fallbacks or forbidden surfaces. This question is **not** locked here — it is the primary DQ for `/research`.
- **Assumptions confirmed (carried from US-0121 program intake)**: Default install host remains cursor-only until explicit `--host opencode|both` opt-in; OpenCode plugin v1 vs v2 deferred to `/research` (R-0109). US-0123 inherits both.
- **Compose guards (intake-locked, read-only vs sibling stories)**:
  - **US-0101 / DEC-0086**: **compose** — keep tier *names* if useful; do **not** use Cursor `fast`/`inherit` as the OpenCode runtime. OpenCode path is additive.
  - **US-0102 / DEC-0087**: **compose** — same volatile-ID rule for `template/`; local catalog / `scratchpad.local.md` holds real vendor slugs. `template/` must not contain live vendor slugs.
  - **US-0003**: agents gain `model:` on OpenCode; Cursor agent files unchanged.
  - **US-0122 / DEC-0122**: US-0122 ships `template/.opencode/agents/<role>.md` with **no** `model:` vendor slug (AC-7). US-0123 owns the **real slug resolution**; US-0122's `model:` frontmatter (if any) stays placeholder/omitted until US-0123 lands. Additive only — US-0123 does not amend US-0122's permission matrix.
  - **US-0080**: `TOKEN_PROFILE` is orthogonal — slug routing must not be substituted for token-cost profile.
- **Boundaries (intake-locked)**:
  - In scope: OpenCode model resolution (kit tier/role/phase → `provider/slug`), local catalog/examples, fail-closed codes, template hygiene, `test_us0123_*`, multi-provider examples including Chinese APIs (DeepSeek, Moonshot, Z.AI/GLM, DashScope/Qwen) without vendor IDs in `template/`.
  - Out of scope: Cursor BYOK fixes, kit-operated proxy, embedding keys, plugin spawn (US-0124), permission matrix (US-0122), thin commands (US-0125), runbook (US-0126).
- **Risks (intake-identified, to be deepened in `/research`)**:
  - R1: vendor slug leakage into `template/` (US-0102 family; AC-3).
  - R2: unknown/empty slug silently falls back to a random model (AC-4 fail-closed).
  - R3: source-of-truth ambiguity between scratchpad, agent frontmatter, and local catalog (AC-1).
  - R4: Chinese API examples committed with live vendor IDs / keys (AC-2, AC-5).
  - R5: per-role vs per-phase granularity mismatch with US-0101/US-0102 tier/phase keys (AC-1, AC-7).
  - R6: kit accidentally proxies provider traffic (AC-2 — kit must not proxy).
- **Next**: `/discovery` (same fresh PO subagent, spec macro) to author D1–D10 discovery notes and DQ1+ open questions for `/research`.

## Discovery Notes — US-0123

- **Story**: Per-role OpenCode model slug routing (multi-provider) — third OpenCode adapter slice; US-0121 DONE, US-0122 DONE, siblings US-0124..US-0126 remain OPEN.
- **Discovery date**: 2026-08-24T15:52:00Z (UTC)
- **Role / model**: po / `glm-5.2-high` (CROSS_MODEL_REVIEW=1)
- **References**: `docs/product/opencode-adapter-masterplan.md`; intake evidence `handoffs/intake_evidence/US-0121-intake-20260822.json` (`model-slug-routing` → US-0123, `coverage_complete=true`); `docs/engineering/architecture.md # US-0122` (permission matrix + no-vendor-slug AC-7 — read-only compose); `decisions/DEC-0086.md` / `DEC-0087.md` (US-0101/US-0102 — read-only compose); research anchor **R-0109**.
- **Discovery locks D1–D10**:
  - **D1 (Resolution chain shape)**: documented mapping from kit tier/role/phase keys → OpenCode `provider/slug`. Chain must be deterministic, single-source-of-truth, and testable. Architecture picks the source; tests assert it.
  - **D2 (Multi-provider examples)**: operator-local examples cover ≥ DeepSeek, Moonshot, Z.AI/GLM, and one Western provider (Anthropic / OpenAI-compatible). Examples live in **local-only** files (gitignored), never in `template/`.
  - **D3 (No vendor IDs in template)**: `template/` contains placeholders only. `test_us0123_no_vendor_slugs_in_template` greps for `deepseek|moonshot|kimi|glm|claude|gpt|sonnet|opus|haiku|o1|o3|sk-` (US-0102 family) and fails on any hit.
  - **D4 (Unknown slug fail-closed)**: invalid/empty slug emits a documented reason code (reuse `MODEL_SLUG_UNKNOWN` / `MODEL_OVERRIDE_SLUG_UNKNOWN` analogue). No silent fallback to a random model.
  - **D5 (Auth store)**: keys live in OpenCode `/connect` / host auth store. Never in plugin logs, git, or `template/`. `test_us0123_auth_store_contract` asserts the documented posture.
  - **D6 (Compose US-0101/US-0102)**: Cursor alias runtime unchanged; this story does not amend DEC-0086/0087 Cursor behavior. OpenCode path is additive. Tier *names* may be reused as labels; `fast`/`inherit` are not OpenCode runtime slugs.
  - **D7 (Per-role assignment)**: ≥ two roles can be configured to different providers in a local catalog without editing `template/`. `test_us0123_per_role_assignment` asserts two-role divergence.
  - **D8 (Contract tests)**: `test_us0123_*` cover placeholder-only template, fail-closed unknown slug, example catalog schema, and non-substitution vs `TOKEN_PROFILE`.
  - **D9 (Chinese APIs as capability)**: per-role assignment is in scope; kit-operated proxy is out of scope. Chinese API quality is operator model choice (AC-10 tool-calling note owned with US-0126 if needed).
  - **D10 (Tool-calling quality note)**: runbook note (owned with US-0126 if needed) that QA/dev should default to a tool-reliable slug; kit does not endorse a single vendor.
- **Open questions for `/research` (DQ1..DQ10)** — all routed to tech-lead, anchor **R-0109**:
  - **DQ1 (Source of truth, AC-1)**: where do slugs live — `.cursor/scratchpad.local.md` `MODEL_*` keys, `model:` frontmatter in `template/.opencode/agents/<role>.md`, or a **local-only** catalog file (e.g. `.opencode/model-catalog.local.json`, gitignored)? Architecture must pick one; tests assert that choice. (Primary DQ.)
  - **DQ2 (Placeholder vs omit `model:`)**: should `template/.opencode/agents/<role>.md` ship a `model:` key with a placeholder (e.g. `model: <your-vendor-slug>`), or omit `model:` entirely until the operator configures a local catalog? US-0122 AC-7 currently forbids real vendor slugs; does it also forbid placeholder strings?
  - **DQ3 (Fail-closed code family)**: reuse `MODEL_SLUG_UNKNOWN` / `MODEL_OVERRIDE_SLUG_UNKNOWN` analogue, or introduce an `OPENCODE_MODEL_SLUG_UNKNOWN` namespaced code? What is the exact reason-code string and where is it documented (runbook vs decisions)?
  - **DQ4 (Catalog file path)**: if a local catalog is the source of truth, what is the canonical path — `.opencode/model-catalog.local.json` (local only, gitignored) or `.cursor/model-catalog.local.json` (kit-existing, US-0101/US-0102)? Can US-0123 reuse the kit-existing catalog path so US-0101/US-0102 and US-0123 share one file, or must OpenCode have its own?
  - **DQ5 (Per-role vs per-phase)**: US-0101/US-0102 keys are per-phase (`MODEL_TIER_<PHASE>`, `MODEL_<PHASE>`); US-0123 AC-7 says "per-role". How do per-role OpenCode agents map to per-phase kit keys? Is there a role→phase matrix (US-0069) that bridges them, or does US-0123 introduce per-role keys (`MODEL_ROLE_PO`, etc.)?
  - **DQ6 (Chinese API examples without vendor IDs)**: how do we ship working DeepSeek/Moonshot/Z.AI/GLM/DashScope examples in `template/` (or in a `template/.opencode/examples/` directory) without committing live vendor IDs or keys? What is the placeholder convention (e.g. `provider: deepseek`, `slug: <your-deepseek-slug>`)?
  - **DQ7 (Compose with US-0122 agents)**: US-0122 ships `template/.opencode/agents/<role>.md` with no `model:` vendor slug. US-0123 owns the real slug resolution. Is the integration additive (US-0123 adds `model:` to existing agent files after US-0122 lands) or does US-0123 introduce a separate catalog that agents reference by name?
  - **DQ8 (Provider mode)**: `MODEL_PROVIDER_MODE=cursor|api` (US-0101) — does OpenCode host always imply `api` mode (BYOK via `/connect`), or can OpenCode also route through Cursor-managed infrastructure? How does this interact with `MODEL_RESOLVE=role_catalog`?
  - **DQ9 (Validator surface)**: do we need a new `scripts/model_slug_validate.py` (or extend `scripts/model_catalog_validate.py`) to enforce fail-closed unknown slug + placeholder-only template + per-role divergence? Or do existing US-0101/US-0102 validators cover US-0123 ACs?
  - **DQ10 (Tool-calling quality note ownership)**: AC-10 says "runbook note (owned with US-0126 if needed)". Does US-0123 ship a stub runbook line now, or defer entirely to US-0126? What is the exact wording so US-0126 can inherit without re-deriving?
- **Compose**: additive on US-0101/US-0102/US-0003; do not amend DEC-0086/0087 Cursor behavior. US-0122 permission matrix unchanged. US-0121 host default remains cursor-only until explicit `--host opencode|both`. No vendor IDs in `template/`.
- **Next**: `/research` (tech-lead) to deepen **R-0109** for US-0123 (DQ1..DQ10 remain open; do not treat as architecture locks), then `/architecture` to lock the resolution chain + source of truth.

## Intake Notes — US-0124

- **Intake date**: 2026-08-24T15:55:00Z (UTC)
- **Orchestrator / run**: `auto-20260824-01` (drain-advance from US-0123 DONE; spec macro = intake + discovery merged, ultra_lean)
- **Role / model**: po / `glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required on isolation)
- **Story**: US-0124 — OpenCode orchestrator plugin spawn-only `/auto` (plugin **is** the OpenCode native chain; do **not** port US-0095 Cursor Task-loop). **Status: OPEN**. No new story ID allocated (reuse existing US-0124).
- **Intake evidence (reused, program bundle)**: `handoffs/intake_evidence/US-0121-intake-20260822.json` — `orchestrator-plugin-spawn` + `headless-invoke-cmd` → [US-0124], `coverage_complete=true`, `selected_pack=first-intake-pack`, `missing_topics=[]`. Intake evidence JSON was **NOT** mutated (security: never mutate prior intake evidence).
- **AC contract**: AC-1..AC-11 remain the contract (unchanged). Acceptance checkboxes remain **unchecked** (`docs/product/acceptance.md` L152). Status remains **OPEN**. Do not mark US-0124 DONE. Do not mutate US-0121/US-0122/US-0123 DONE.
- **Spawn-only posture (intake-locked)**:
  - On OpenCode the plugin **is** the native chain. US-0095 Cursor Task-loop is **not** ported; `.cursor/commands/auto.md` Cursor prose is **not** copied into the plugin (AC-9).
  - `/auto` is spawn-only: resolve phase→role via **US-0069**, spawn an isolated child session, write isolation evidence, honor the **US-0092** stop matrix, and refuse orchestrator (or any role) performing another role's artifact writes.
  - Headless path uses **US-0092** `--invoke-cmd`; when native in-session chain is unavailable, emit `NATIVE_CHAIN_UNAVAILABLE` analogue rather than roleplay.
  - Plugin API v1 vs v2 is **research-locked** (**R-0109** Q1 — already LOCKED for /architecture as v2 `ctx.session.*` + `ctx.tool.hook("execute.before", …)`), not this intake.
  - Success tests (a)(d): a model that ignores its prompt still cannot skip spawn isolation (a) or continue `/auto` without the next role's fresh session (d).
- **Assumptions confirmed (carried from US-0121 program intake)**: Default install host remains cursor-only until explicit `--host opencode|both` opt-in; OpenCode plugin v1 vs v2 deferred to `/research` (R-0109). US-0124 inherits both.
- **Compose guards (intake-locked, read-only vs sibling stories)**:
  - **US-0069 / DEC-0051**: **compose** — same phase→role matrix; wrong-role spawn fails closed (`PHASE_ROLE_MISMATCH` analogue).
  - **US-0092 / DEC-0078**: **compose** — reuse outer driver + `--invoke-cmd` + stop reasons; do **not** reimplement the state machine in TypeScript.
  - **US-0095 / DEC-0080**: **do not port** — Cursor native chain is replaced by the plugin. Cursor `/auto` remains for the Cursor host.
  - **US-0023 / US-0048 / BUG-0006**: **compose** — spawn-only; fail closed if stock OpenCode cannot isolate child sessions (thin fork is deferred `opencode-fork`, not silent same-session roleplay per R-0001).
  - **US-0005**: hook-equivalent enforcement moves into the plugin + permissions (do not port Cursor hook JSON as-is).
  - **US-0121 / DEC-0121**: host default remains cursor-only until explicit `--host opencode|both`; plugin lives in `template/.opencode/plugins/` (US-0121 reserved slot).
  - **US-0122 / DEC-0122**: `template/.opencode/agents/auto.md` already ships `mode: primary`, `edit: deny`, `bash: deny`, `task` allow-list to seven role agents. The US-0124 plugin **composes with** that agent — see Discovery D9 (agent vs plugin boundary).
  - **US-0125**: thin commands are Layer 3 dispatch only; missing a convenience command must not disable plugin spawn (US-0125 AC-7). US-0124 must not own command bodies.
- **Boundaries (intake-locked)**:
  - In scope: orchestrator plugin, spawn/isolation, US-0069 mapping, stop matrix, `--invoke-cmd`, fail-closed codes, `test_us0124_*`.
  - Out of scope: reimplementing Python validators (US-0125), installer (US-0121), forking OpenCode unless research proves isolation impossible, sovereign-loop-on-opencode (deferred plan area), model slug routing (US-0123), permission matrix authoring (US-0122 — plugin consumes, does not author).
- **Risks (intake-identified, to be deepened in `/research`)**:
  - R1: V2 `subtask`/`ctx.session.create` ignored or unavailable at runtime → spawn no-ops; must fail closed (`OPENCODE_PLUGIN_SPAWN_UNSUPPORTED` analogue), never same-session roleplay (R-0001 / R-0109 Q1–Q2).
  - R2: Spawn isolation gap — if stock OpenCode cannot isolate child sessions, deferred `opencode-fork` or stop; do not silently continue.
  - R3: Plugin cannot call Task/session client as assumed — architecture must confirm `ctx.session.create` vs tool intercept only.
  - R4: Dual-host parity cost — `.cursor/commands/auto.md` and plugin diverge; mitigate by treating them as two host surfaces, not a copy.
  - R5: Subtask-ignored fail-closed — if OpenCode V2 `subtask` (or equivalent) is ignored and child sessions cannot be isolated, fail closed with documented `OPENCODE_*` reason code; do not degrade to one-chat multi-role.
  - R6: Headless `--invoke-cmd` surface unknown on OpenCode (R-0109 Q3 LOCKED for /architecture) — may require `opencode run` stdin pipe or plugin `ctx.session.prompt`.
- **Next**: `/discovery` (same fresh PO subagent, spec macro) to author D1–D10 discovery notes and DQ1+ open questions for `/research`.

## Discovery Notes — US-0124

- **Story**: OpenCode orchestrator plugin spawn-only `/auto` (fourth OpenCode adapter slice; US-0121 DONE, US-0122 DONE, US-0123 DONE, siblings US-0125..US-0126 remain OPEN).
- **Discovery date**: 2026-08-24T15:58:00Z (UTC)
- **Role / model**: po / `glm-5.2-high` (CROSS_MODEL_REVIEW=1)
- **References**: `docs/product/opencode-adapter-masterplan.md`; intake evidence `handoffs/intake_evidence/US-0121-intake-20260822.json` (`orchestrator-plugin-spawn` + `headless-invoke-cmd` → US-0124, `coverage_complete=true`); `template/.opencode/agents/auto.md` (US-0122 — read-only compose); `template/.opencode/plugins/README.md` (US-0121 reserved slot); `decisions/DEC-0051.md` (US-0069 — read-only compose); `decisions/DEC-0078.md` (US-0092 — read-only compose); `decisions/DEC-0080.md` (US-0095 — do-not-port); research anchor **R-0109** (Q1 v1 vs v2 LOCKED for /architecture as v2; Q2 Task isolation LOCKED; Q3 headless LOCKED for /architecture).
- **Discovery locks D1–D10**:
  - **D1 (Plugin location)**: orchestrator plugin lives in `template/.opencode/plugins/` (US-0121 reserved slot; `template/.opencode/plugins/README.md` already documents US-0124 ownership). Plugin file naming + entry-point shape (v2 `Plugin.define({ id, setup })`) is `/architecture`-locked per R-0109 Q1. US-0124 populates the directory; it does not create a second plugin location.
  - **D2 (Plugin API v1 vs v2 lock)**: per R-0109 Q1 (LOCKED for /architecture), US-0124 targets **v2** — `Plugin.define({ id, setup })` with `ctx.tool.hook("execute.before", …)` for write-guards and `ctx.session.create / prompt / wait` for spawn. v1 hooks (`@opencode-ai/plugin` default export) remain a documented fallback only if `/architecture` confirms v2 `ctx.session.*` is unavailable at runtime; fallback must fail closed with `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED` rather than silently degrade. US-0124 does not lock v1 vs v2 in `template/` — that is `/architecture`'s call.
  - **D3 (Spawn isolation: static vs runtime proof)**: isolation is enforced by `Session.create({ parentID, … })` + deny-list (R-0109 Q2 LOCKED). **Static proof** = contract test asserts the plugin calls `ctx.session.create` (or v1 equivalent) with a fresh `parentID` and never reuses the orchestrator session id. **Runtime proof** = a harness that runs the plugin against a stub OpenCode and asserts the spawned session id ≠ orchestrator session id. US-0124 ships both: `test_us0124_spawn_isolation_static` (grep/AST on plugin source) + `test_us0124_spawn_isolation_runtime` (stub harness). Architecture must lock the stub-harness contract.
  - **D4 (Analogue reason codes `OPENCODE_*`)**: US-0124 emits `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED` (v2 `ctx.session.create` unavailable), `OPENCODE_SUBTASK_IGNORED` (V2 `subtask` equivalent ignored — child session not isolated), `OPENCODE_HEADLESS_UNSUPPORTED` (US-0092 `--invoke-cmd` cannot resolve a non-interactive session CLI), and reuses `AUTO_ORCHESTRATOR_PHASE_EXECUTION` (orchestrator performing phase writes) + `PHASE_ROLE_MISMATCH` (wrong-role spawn) + `NATIVE_CHAIN_UNAVAILABLE` (headless fallback). Codes are documented in US-0126 runbook; US-0124 ships a stub reason-code table (US-0126 owns full text).
  - **D5 (Subtask-ignored fail-closed)**: if OpenCode V2 `subtask` (or equivalent spawn primitive) is ignored — i.e. the plugin calls spawn but the host returns without creating an isolated child session — the plugin must fail closed with `OPENCODE_SUBTASK_IGNORED` and stop `/auto`. **Forbidden**: degrading to one-chat multi-role (R-0001 / R-0109). `test_us0124_subtask_ignored_fail_closed` asserts the plugin does not continue `/auto` after a no-op spawn.
  - **D6 (No copy of `.cursor/commands/auto.md`)**: US-0124 plugin source must not paste `.cursor/commands/auto.md` Cursor Task-loop prose. `test_us0124_no_cursor_auto_clone` greps the plugin source for unique-to-Cursor phrases (e.g. `## Spawn-boundary integrity (BUG-0006)` heading, `AUTO_LOOP_MAX_CYCLES` prose) and fails on hit. Cursor `/auto` remains for the Cursor host; the OpenCode plugin is a separate implementation that **composes** US-0069 + US-0092 semantics, not a prose port.
  - **D7 (Stop-matrix wiring)**: plugin/outer-driver honors US-0092 stop reasons (decision_gate, loop_max, blocked, pause). No silent continue. `test_us0124_stop_matrix` asserts each stop reason maps to a documented plugin action (spawn next phase, hard stop, ledger write, pause boundary). The plugin does not reimplement the state machine in TypeScript; it calls into the existing `scripts/auto_outer_driver.py` reason-code family (subprocess or import — `/architecture` locks).
  - **D8 (Headless `--invoke-cmd`)**: US-0092 outer driver can invoke OpenCode non-interactive/session API. Per R-0109 Q3 (LOCKED for /architecture), the public CLI surface is uncertain — candidates are (a) a future `opencode run --prompt` flag, (b) `opencode` with stdin piping, (c) the US-0124 plugin invoking `ctx.session.prompt` programmatically. US-0124 owns the runtime path; if `/architecture` cannot confirm a headless CLI surface, US-0092 `--invoke-cmd` on OpenCode must fail closed with `OPENCODE_HEADLESS_UNSUPPORTED`. `test_us0124_invoke_cmd_hook` asserts the wiring (or the fail-closed path) — not a live OpenCode probe.
  - **D9 (Compose with US-0122 `auto.md` agent vs plugin)**: `template/.opencode/agents/auto.md` (US-0122) already ships the orchestrator **agent** — `mode: primary`, `edit: deny`, `bash: deny`, `task` allow-list to seven role agents. The US-0124 **plugin** is the **enforcement layer** that intercepts tool calls and spawns sessions; the agent is the **prompt layer** that tells the model "you are the auto orchestrator; spawn Task subagents only". Boundary: agent owns *who the model is* + permission allow-list; plugin owns *what the host does* (spawn, write-guard, stop-matrix, isolation evidence). They compose — the plugin does not replace the agent. `test_us0124_agent_plugin_compose` asserts both files exist and the plugin does not duplicate the agent's permission array.
  - **D10 (Contract tests)**: `test_us0124_*` cover spawn-only deny (AC-1), isolation evidence fields (AC-3), stop-matrix wiring (AC-6), `--invoke-cmd` hook (AC-7), subtask-ignored fail-closed (AC-8), no Cursor auto.md clone (AC-9), success tests (a)(d) (AC-4, AC-5), and secrets-no-logging (AC-11). Tests are static + stub-harness; no live OpenCode runtime probe in this slice.
- **Open questions for `/research` (DQ1..DQ8)** — all routed to tech-lead, anchor **R-0109** (US-0124-specific subsection; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 locks PRESERVED — not wiped):
  - **DQ1 (Plugin entry-point shape, AC-1)**: what is the exact v2 `Plugin.define({ id, setup })` file naming + entry point — `template/.opencode/plugins/orchestrator.ts`? `index.ts`? Does OpenCode auto-load `.opencode/plugins/*.ts` or does it require a `plugins[]` entry in `opencode.json`? (R-0109 Q1 deepens — /architecture locks.)
  - **DQ2 (Spawn API surface, AC-1, AC-4)**: is `ctx.session.create / prompt / wait` the correct v2 spawn API, or is there a dedicated `ctx.task` / `ctx.agent.spawn` handle? What is the exact signature (parentID, agent, prompt, fresh-context flag)? (R-0109 Q2 deepens.)
  - **DQ3 (Static vs runtime isolation proof, AC-3, AC-4)**: what is the minimum stub-harness contract for `test_us0124_spawn_isolation_runtime`? Can the plugin be loaded in a JS/TS test harness without a live OpenCode, or does the test require a mock `ctx`? Does OpenCode ship a test harness / mock `ctx`?
  - **DQ4 (Reason-code namespace, AC-8)**: should US-0124 emit `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`, `OPENCODE_SUBTASK_IGNORED`, `OPENCODE_HEADLESS_UNSUPPORTED` as new codes, or reuse existing `NATIVE_CHAIN_UNAVAILABLE` / `AUTO_ORCHESTRATOR_PHASE_EXECUTION` / `PHASE_ROLE_MISMATCH`? Where is the canonical reason-code table (runbook vs decisions vs `scripts/reason_codes.py`)?
  - **DQ5 (Subtask-ignored detection, AC-8)**: how does the plugin **detect** that a spawn was ignored — does `ctx.session.create` return `null`/`undefined`, throw, or return a session id identical to the parent? What is the deterministic signal? `test_us0124_subtask_ignored_fail_closed` needs a stub that returns each case.
  - **DQ6 (Stop-matrix integration, AC-6)**: does the plugin call `scripts/auto_outer_driver.py` as a subprocess, import it as a Python module from TS (unlikely), or reimplement the stop-matrix in TS (forbidden by AC-6 + D7)? If subprocess, what is the exact argv contract? If the driver must be invoked from TS, does US-0124 need a JSON-over-stdio bridge?
  - **DQ7 (Headless CLI surface, AC-7)**: which of the three R-0109 Q3 candidates (future `opencode run --prompt`, stdin pipe, plugin `ctx.session.prompt`) is the /architecture-locked headless path for US-0092 `--invoke-cmd` on OpenCode? Is there a public, stable, non-interactive CLI in current OpenCode that the kit can shell out to?
  - **DQ8 (Agent vs plugin ownership boundary, AC-1, AC-9)**: US-0122 ships `auto.md` agent with `task` allow-list; US-0124 ships the plugin. Is there any overlap that risks double-enforcement (both agent prompt and plugin refuse the same write)? Does the plugin need to read the agent's permission array, or are they fully independent surfaces? `test_us0124_agent_plugin_compose` needs the exact ownership boundary.
- **Compose**: additive on US-0069/US-0092/US-0023/US-0048/BUG-0006; do **not** port US-0095; do **not** clone `.cursor/commands/auto.md`. US-0122 `auto.md` agent unchanged. US-0121 host default remains cursor-only until explicit `--host opencode|both`. US-0125 thin commands are Layer 3 (plugin must not own command bodies). No vendor slugs in `template/` (US-0102 family).
- **Next**: `/research` (tech-lead) to deepen **R-0109** for US-0124 (DQ1..DQ8 remain open; do not treat as architecture locks), then `/architecture` to lock the plugin entry-point + spawn API + reason-code namespace + headless path + agent/plugin boundary.

## Intake Notes — US-0125

- **Intake date**: 2026-08-24T19:58:00Z (UTC)
- **Orchestrator / run**: `auto-20260824-02` (drain-advance from US-0124 DONE; spec macro = intake + discovery merged, ultra_lean)
- **Role / model**: po / `glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required on isolation)
- **Story**: US-0125 — Thin OpenCode commands + Python validator bridge (Layer 3 `.opencode/commands/*.md` are dispatch-only; plugin/CLI invokes existing `scripts/*_validate.py`; do not reimplement validators in TS). **Status: OPEN**. No new story ID allocated (reuse existing US-0125).
- **Intake evidence (reused, program bundle)**: `handoffs/intake_evidence/US-0121-intake-20260822.json` — `validator-bridge` + `thin-commands` → [US-0125], `coverage_complete=true`, `selected_pack=first-intake-pack`, `missing_topics=[]`. Intake evidence JSON was **NOT** mutated (security: never mutate prior intake evidence).
- **AC contract**: AC-1..AC-10 remain the contract (unchanged). Acceptance checkboxes remain **unchecked** (`docs/product/acceptance.md` L153). Status remains **OPEN**. Do not mark US-0125 DONE. Do not mutate US-0121/US-0122/US-0123/US-0124 DONE.
- **Dispatch-only posture (intake-locked)**:
  - Layer 3 `.opencode/commands/*.md` are named entry points (`/intake`, `/execute`, `/auto`, `/release`, …) that select the role agent, pass a short phase id + artifact path list, then **STOP**. They must not clone Cursor 200-line command bodies (AC-1, AC-9).
  - The plugin/CLI invokes existing `scripts/*_validate.py` gates; validators are **not** reimplemented in TypeScript (AC-3). Persistence-blocking gates remain Python CLIs (`intake_evidence_validate.py`, `bug_issue_validate.py`, and other fail-closed validators already in the kit).
  - Success test (b): a model that ignores its prompt still cannot run `/release` after a failing validator (AC-4). Validator non-zero exit surfaces existing kit reason codes (or a documented `OPENCODE_*` wrapper that still names the Python code) — no silent skip (AC-5).
  - Missing a convenience command must not disable US-0124 plugin spawn or Python CLIs — commands are Layer 3 (AC-7).
  - No new npm runtime in consumer app code — validator bridge is kit scripts + plugin subprocess, not a dependency of the operator's application (AC-10).
- **Assumptions confirmed (carried from US-0121 program intake)**: Default install host remains cursor-only until explicit `--host opencode|both` opt-in; OpenCode plugin v1 vs v2 deferred to `/research` (R-0109). US-0125 inherits both.
- **Compose guards (intake-locked, read-only vs sibling stories)**:
  - **US-0001**: **compose** — keep phase *names* and artifact outputs; do not triple-copy command files (AC-9). Cursor command files unchanged.
  - **US-0078 / DEC-0060**: **compose** — `intake_evidence_validate.py` remains the persistence-blocking gate; thin commands must not reimplement its rules.
  - **US-0121 / DEC-0121**: host default remains cursor-only until explicit `--host opencode|both`; thin commands live in `template/.opencode/commands/` (US-0121 reserved slot; `.gitkeep` already exists).
  - **US-0122 / DEC-0122**: thin commands dispatch to the seven role agents; they do not own permission arrays or role prompts.
  - **US-0124 / DEC-0124**: plugin may call the same Python CLIs; US-0125 owns the command files + the "Python is source of truth" contract. Missing a convenience command must not disable plugin spawn (US-0124 AC-7 ↔ US-0125 AC-7). Plugin must not own command bodies.
  - **US-0126**: owns the full OpenCode host runbook + reason-code table + `--scope=opencode-adapter` parity. US-0125 ships stub reason-code references only; US-0126 owns full text.
- **Boundaries (intake-locked)**:
  - In scope: thin `.opencode/commands/`, Python CLI bridge, clone/size guards, success test (b), `test_us0125_*`.
  - Out of scope: rewriting validators, porting full Cursor command prose, installer host flag (US-0121), model catalog (US-0123), full runbook (US-0126), plugin spawn mechanics (US-0124).
- **Risks (intake-identified, to be deepened in `/research`)**:
  - R1: Clone drift — `.opencode/commands/` accidentally copies `.cursor/commands/` bodies above threshold; mitigate with clone-guard metric + contract test (AC-2, AC-6).
  - R2: Validator reimplementation temptation — a rule that should be a Python CLI check leaks into command prose; mitigate with grep/test for policy text duplicating validator logic (AC-6).
  - R3: Reason-code ambiguity — validator non-zero exit surfaces existing kit codes vs a new `OPENCODE_*` wrapper; boundary with US-0126 reason-code namespace must be locked (AC-5).
  - R4: Optional-command fragility — missing a convenience command disables plugin spawn or Python CLIs; mitigate with AC-7 contract test.
  - R5: Success test (b) harness — `/release` after failing validator must be blocked even when the command/agent prompt says to continue; harness contract must be locked (AC-4, AC-8).
  - R6: Dual-host parity cost — `.cursor/commands/` and `.opencode/commands/` diverge; mitigate by treating them as two host surfaces, not a copy (AC-9).
- **Next**: `/discovery` (same fresh PO subagent, spec macro) to author D1–D10 discovery notes and DQ1+ open questions for `/research`.

## Discovery Notes — US-0125

- **Story**: Thin OpenCode commands + Python validator bridge (fifth OpenCode adapter slice; US-0121 DONE, US-0122 DONE, US-0123 DONE, US-0124 DONE, sibling US-0126 remains OPEN).
- **Discovery date**: 2026-08-24T20:01:00Z (UTC)
- **Role / model**: po / `glm-5.2-high` (CROSS_MODEL_REVIEW=1)
- **References**: `docs/product/opencode-adapter-masterplan.md`; intake evidence `handoffs/intake_evidence/US-0121-intake-20260822.json` (`validator-bridge` + `thin-commands` → US-0125, `coverage_complete=true`); `template/.opencode/commands/.gitkeep` (US-0121 reserved slot); `template/.opencode/agents/auto.md` (US-0122 — read-only compose); `template/.opencode/plugins/README.md` (US-0124 — read-only compose); `scripts/intake_evidence_validate.py` + `scripts/bug_issue_validate.py` (Python SOT — read-only consume); `docs/product/backlog.md ## US-0125` (AC-1..AC-10); research anchor **R-0109** (US-0124 subsection; US-0125 inherits v2 plugin + headless locks but owns the command/validator-bridge surface).
- **Discovery locks D1–D10**:
  - **D1 (Command location)**: thin commands live in `template/.opencode/commands/` (US-0121 reserved slot; `.gitkeep` already exists). US-0125 populates the directory with named `.md` files; it does not create a second command location. File naming + frontmatter shape (OpenCode `description` + dispatch prose) is `/architecture`-locked per DQ5/DQ6.
  - **D2 (Named command inventory)**: commands are phase names from US-0001 (e.g. `/intake`, `/discovery`, `/research`, `/architecture`, `/sprint-plan`, `/execute`, `/qa`, `/verify-work`, `/release`, `/closure`, `/refresh-context`, `/auto`, `/ask`, `/quick`, `/pause`, `/resume`, `/status-reconcile`, `/memory-audit`, `/milestone-start`, `/milestone-complete`, `/plan-verify`, `/phase-context`, `/map-codebase`, `/security-review`, `/sovereign-critic`), **not** 200-line clones of `.cursor/commands/*.md`. Each command file is dispatch-only: select role + phase id + artifact path list, then STOP. Exact file list is `/architecture`-locked per DQ1.
  - **D3 (Clone-guard metric)**: `test_us0125_clone_guard` enforces a documented size and/or similarity threshold vs `.cursor/commands/`. Candidate metric: (a) per-file byte/line cap (e.g. ≤ N lines, where N << 200), (b) normalized-text similarity score vs the matching `.cursor/commands/<name>.md` below a documented threshold, or (c) both. Exact threshold + algorithm is `/architecture`-locked per DQ2. The test fails on hit (AC-2).
  - **D4 (Python validators remain SOT)**: persistence-blocking gates stay as existing Python CLIs — `intake_evidence_validate.py`, `bug_issue_validate.py`, and other fail-closed validators already in the kit. Plugin/command may subprocess them; must not reimplement rules (AC-3, AC-6). The set of in-scope validators for US-0125 (vs US-0126 runbook) is `/architecture`-locked per DQ3.
  - **D5 (Success test (b) mechanism)**: `/release` (or release persistence path) after a failing validator is blocked even if the command/agent prompt says to continue. Mechanism: the plugin/command subprocess calls the Python CLI; non-zero exit → fail-closed (no persistence). `test_us0125_release_blocked_after_failing_validator` asserts the wiring (or the fail-closed path) — not a live release probe. Exact subprocess contract (plugin vs command prose) is `/architecture`-locked per DQ4.
  - **D6 (Reason-code wrapping)**: validator non-zero exit surfaces existing kit reason codes (e.g. `INTAKE_PERSISTENCE_BLOCKED`, `INTAKE_REQUIRED_TOPIC_MISSING`, `BUG_ISSUE_VALIDATION_FAILED`) **or** a documented `OPENCODE_*` wrapper that still names the Python code (e.g. `OPENCODE_VALIDATOR_FAILED: INTAKE_PERSISTENCE_BLOCKED`). No silent skip (AC-5). The wrapper-vs-reuse boundary + canonical reason-code table location is `/architecture`-locked per DQ4 + DQ6 (coordinate with US-0126, which owns the full reason-code table).
  - **D7 (Missing convenience command must not disable US-0124 plugin)**: commands are Layer 3. `test_us0125_missing_command_does_not_disable_plugin` asserts that deleting/renaming a convenience command does not break plugin spawn (US-0124) or Python CLI execution. The plugin and CLIs must run independently of the command files (AC-7).
  - **D8 (Compose US-0001 — Cursor commands unchanged)**: `.cursor/commands/*.md` are not modified by US-0125. OpenCode commands are additive. `test_us0125_cursor_commands_unchanged` asserts byte-parity of `.cursor/commands/` against the pre-US-0125 git state (or a hash manifest) (AC-9).
  - **D9 (No new npm runtime)**: the validator bridge is kit scripts (`scripts/*.py`) + plugin subprocess, not a dependency of the operator's application. `test_us0125_no_new_npm_runtime` asserts that `template/package.json` (if any) and consumer `package.json` do not gain a new runtime dependency for the validator bridge (AC-10).
  - **D10 (`test_us0125_*` inventory)**: `test_us0125_*` cover thin-command inventory (AC-1), clone guard (AC-2), validator subprocess fail-closed (AC-3), success test (b) (AC-4), reason-code wrapping (AC-5), no-policy-in-commands (AC-6), missing-command-does-not-disable-plugin (AC-7), and full `test_us0125_*` inventory (AC-8). Tests are static + stub-harness; no live OpenCode runtime probe in this slice.
- **Open questions for `/research` (DQ1..DQ8+)** — all routed to tech-lead, anchor **R-0109** (US-0125-specific subsection; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 + US-0124 DQ1..DQ8 locks PRESERVED — not wiped):
  - **DQ1 (Exact command file list, AC-1)**: what is the exact set of named `.opencode/commands/*.md` files US-0125 ships — every US-0001 phase name, or a curated subset? Is there a 1:1 mapping to `.cursor/commands/`, or a dispatch-only subset? (R-0109 deepens — /architecture locks.)
  - **DQ2 (Clone-guard threshold, AC-2)**: what is the exact per-file size cap (lines/bytes) and/or similarity threshold vs `.cursor/commands/<name>.md`? Is the metric byte-cap, normalized-text similarity, AST-shape, or a combination? What is the deterministic pass/fail boundary?
  - **DQ3 (Validators in-scope vs US-0126, AC-3)**: which Python validators are in-scope for US-0125 (subprocess bridge) vs documented in the US-0126 runbook? Is `intake_evidence_validate.py` + `bug_issue_validate.py` the full in-scope set, or are there other persistence-blocking CLIs (e.g. `closure-verification`, `enforce-triad-hot-surface`, `model_tier_validate`, `release_changelog_lib`)?
  - **DQ4 (How command invokes validator, AC-3, AC-4)**: does the thin command prose tell the agent to subprocess the Python CLI, or does the US-0124 plugin intercept the command and subprocess the validator itself? If the plugin owns the subprocess, what is the exact argv/stdout/exit-code contract? If the command prose owns it, how is success test (b) enforced against a prompt-ignoring model?
  - **DQ5 (`/auto` command vs US-0124 plugin ownership, AC-1, AC-7)**: `/auto` is special — US-0124 owns the orchestrator plugin. Does US-0125 ship a `/auto` command file at all, or does `/auto` go directly through the plugin? If US-0125 ships `/auto`, is it dispatch-only ("invoke the orchestrator agent + plugin") with no spawn logic?
  - **DQ6 (Command frontmatter shape for OpenCode, AC-1)**: what is the exact frontmatter shape OpenCode expects for `.opencode/commands/*.md` — `description` only (like Cursor), or `agent`/`mode`/`permission` fields? Does a command bind to a single role agent, or is the agent selected by prose?
  - **DQ7 (Reason-code wrapper vs reuse, AC-5)**: should US-0125 emit `OPENCODE_VALIDATOR_FAILED: <python_code>` as a wrapper, or surface the raw Python reason code (e.g. `INTAKE_PERSISTENCE_BLOCKED`)? Where is the canonical reason-code table — runbook (US-0126), decisions, or `scripts/reason_codes.py`? How does US-0125 avoid pre-empting US-0126's reason-code namespace?
  - **DQ8 (Success test (b) harness contract, AC-4, AC-8)**: what is the minimum stub-harness contract for `test_us0125_release_blocked_after_failing_validator`? Does the test stub the Python CLI (deterministic non-zero exit) and assert the command/plugin does not proceed to release persistence? Does OpenCode ship a test harness, or does US-0125 build a mock?
- **Compose**: additive on US-0001/US-0078/US-0121/US-0122/US-0124; do **not** clone `.cursor/commands/`; do **not** reimplement Python validators. US-0124 plugin unchanged (commands are Layer 3; plugin must not own command bodies). US-0121 host default remains cursor-only until explicit `--host opencode|both`. US-0122 role agents unchanged. US-0126 owns full runbook + reason-code table. No vendor slugs in `template/` (US-0102 family).
- **Next**: `/research` (tech-lead) to deepen **R-0109** for US-0125 (DQ1..DQ8 remain open; do not treat as architecture locks), then `/architecture` to lock the command file list + clone-guard threshold + validator subprocess contract + `/auto` vs plugin ownership + frontmatter shape + reason-code wrapper boundary.

## Intake Notes — US-0126

- **Intake date**: 2026-08-24T21:55:00Z (UTC)
- **Orchestrator / run**: `auto-20260824-02` (drain-advance from US-0125 / S0125 DONE; spec macro = intake + discovery merged, ultra_lean; `drain_advance_action=spawned`; native chain continuing)
- **Role / model**: po / `glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required on isolation)
- **Story**: US-0126 — Operator runbook for OpenCode host plus contract tests and `--scope=opencode-adapter` parity (sixth and final OpenCode adapter slice). Program DoD: an operator with stock OpenCode + `/connect`ed keys can run intake→…→release on a fresh install **without Cursor**, PO/Dev/QA as different sessions (optionally different providers), validators blocking persistence the same as today. **Status: OPEN**. No new story ID allocated (reuse existing US-0126).
- **Intake evidence (reused, program bundle)**: `handoffs/intake_evidence/US-0121-intake-20260822.json` — `docs-runbook-parity` → [US-0126], `coverage_complete=true`, `selected_pack=first-intake-pack`, `missing_topics=[]`. Validator re-run: `[INTAKE_EVIDENCE_VALIDATION_OK]`. Intake evidence JSON was **NOT** mutated (security: never mutate prior intake evidence; US-0121 program bundle is the canonical record for the whole epic).
- **AC contract**: AC-1..AC-10 remain the contract (unchanged). Acceptance checkbox remains **unchecked** (`docs/product/acceptance.md` L154). Status remains **OPEN**. Do not mark US-0126 DONE. Do not tick acceptance. Do not reopen US-0121..US-0125 DONE.
- **Runbook + parity posture (intake-locked)**:
  - `docs/engineering/runbook.md` (active + `template/` parity) documents stock OpenCode TUI/desktop/IDE as the UI, `--host` opt-in, `/connect` keys, and that kit UX is slash commands + reason codes (no new its-magic GUI) (AC-1).
  - Reason-code catalog documents the `OPENCODE_*` family and reuses/analogues `NATIVE_CHAIN_UNAVAILABLE`, `AUTO_ORCHESTRATOR_PHASE_EXECUTION`, spawn-isolation failures. Each code has remediation text (AC-2). US-0126 owns the full reason-code table; US-0125 ships stub references only.
  - `check_intake_template_parity.py --scope=opencode-adapter` covers pack, installer host help/manifest, agents/commands/plugin, and runbook surfaces this epic owns (AC-3).
  - `test_us0126_*` (and/or a checklist that per-story `test_us0121_*`..`test_us0125_*` exist) fail if the OpenCode pack ships without the documented test markers (AC-4).
  - README hygiene: user-visible OpenCode host blurb; no leaked DEC ids in operator sentences (US-0071 sanitization). UI is OpenCode; kit is the workflow (AC-5).
  - Program DoD documented in runbook (intake→release without Cursor; different sessions/providers; validators still block) (AC-6).
  - Default host reminder: docs state cursor-only default until `--host opencode|both` (AC-7).
  - Out-of-scope list: runbook/README explicitly exclude standalone runtime, OpenCode fork, VS Code contrib rewrite, Caveman, Cursor-browser-as-primary-UAT (AC-8).
  - Sanitization + template parity: new doc files mirrored under `template/` where installer-owned (AC-9).
  - Compose: do not delete Cursor kit docs; OpenCode is additive (AC-10).
- **Assumptions confirmed (carried from US-0121 program intake)**: Default install host remains cursor-only until explicit `--host opencode|both` opt-in; OpenCode plugin v1 vs v2 deferred to `/research` (R-0109). US-0126 inherits both.
- **Compose guards (intake-locked, read-only vs sibling stories)**:
  - **US-0071 sanitization**: operator sentences must not leak DEC ids.
  - **US-0113..US-0117 operator docs**: **compose** — add an OpenCode host section; do not rewrite Cursor command catalogs.
  - **US-0121 / DEC-0121**: host default remains cursor-only until explicit `--host opencode|both`; runbook + parity live alongside installer-owned paths; `--scope=opencode-adapter` extends the existing parity script.
  - **US-0122 / DEC-0122**: runbook references the seven role agents; does not redefine permissions.
  - **US-0123 / DEC-0123**: runbook references `/connect` keys + provider/slug routing; does not re-list vendor slugs.
  - **US-0124 / DEC-0124**: runbook documents the orchestrator plugin spawn contract + `OPENCODE_*` reason codes; does not reimplement plugin logic.
  - **US-0125 / DEC-0125**: runbook documents thin commands + validator-bridge reason-code wrapping; US-0126 owns the full reason-code table that US-0125 stubs reference.
- **Boundaries (intake-locked)**:
  - In scope: runbook, README blurb, reason-code list, `--scope=opencode-adapter`, `test_us0126_*`, template doc parity, program DoD documentation.
  - Out of scope: implementing the plugin (US-0124), inventing a GUI, Cursor browser UAT as primary, standalone runtime, OpenCode fork, VS Code contrib rewrite, Caveman, rewriting validators.
- **Risks (intake-identified, to be deepened in `/research`)**:
  - R1: Reason-code namespace collision with US-0125 stub references — mitigate by US-0126 owning the canonical table and US-0125 pointing to it (AC-2, AC-5).
  - R2: Parity-scope drift — `--scope=opencode-adapter` coverage gaps leave epic surfaces unverified; mitigate with explicit surface inventory in `/architecture` (AC-3).
  - R3: Operator-sentence DEC leakage — mitigate with US-0071 sanitization grep/test (AC-5).
  - R4: Template-parity gap — new doc files not mirrored under `template/`; mitigate with installer-owned-paths manifest + parity check (AC-9).
  - R5: Program-DoD ambiguity — "without Cursor" + "different sessions/providers" + "validators still block" must be operationally testable; mitigate with explicit DoD test contract in `/architecture` (AC-6).
  - R6: Cursor-kit deletion temptation — mitigate with AC-10 compose test (do not delete Cursor docs).
- **Next**: `/discovery` (same fresh PO subagent, spec macro) to author D1–D10 discovery notes and DQ1..DQ8+ open questions for `/research`.

## Discovery Notes — US-0126

- **Story**: Operator runbook for OpenCode host plus contract tests and `--scope=opencode-adapter` parity (sixth OpenCode adapter slice; US-0121 DONE, US-0122 DONE, US-0123 DONE, US-0124 DONE, US-0125 DONE; this is the final epic slice).
- **Discovery date**: 2026-08-24T21:58:00Z (UTC)
- **Role / model**: po / `glm-5.2-high` (CROSS_MODEL_REVIEW=1)
- **References**: `docs/product/opencode-adapter-masterplan.md`; intake evidence `handoffs/intake_evidence/US-0121-intake-20260822.json` (`docs-runbook-parity` → US-0126, `coverage_complete=true`); `docs/engineering/runbook.md` (active + `template/` parity — read-only compose); `scripts/check_intake_template_parity.py` (parity CLI — read-only extend); `docs/engineering/context/installer-owned-paths.manifest` (installer-owned doc paths); `docs/product/backlog.md ## US-0126` (AC-1..AC-10); research anchor **R-0109** (epic-level; US-0126 inherits v2 plugin + headless + reason-code locks and owns the runbook + parity + reason-code table surface).
- **Discovery locks D1–D10**:
  - **D1 (Runbook location + active/template parity)**: runbook lives at `docs/engineering/runbook.md` (active) and `template/docs/engineering/runbook.md` (parity). US-0126 adds an "OpenCode host" section to both; it does not create a second runbook file. Section anchor + heading shape is `/architecture`-locked per DQ1.
  - **D2 (Reason-code catalog location)**: the canonical `OPENCODE_*` / analogue reason-code table lives in the runbook (US-0126 owns it). US-0125 stub references point here. Codes: `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`, `OPENCODE_SUBTASK_IGNORED`, `OPENCODE_HEADLESS_UNSUPPORTED` (from US-0124), `OPENCODE_VALIDATOR_FAILED: <python_code>` wrapper (from US-0125), plus analogues of `NATIVE_CHAIN_UNAVAILABLE`, `AUTO_ORCHESTRATOR_PHASE_EXECUTION`, `PHASE_ROLE_MISMATCH`, `INTAKE_PERSISTENCE_BLOCKED` family. Exact code list + remediation text is `/architecture`-locked per DQ2 (coordinate with US-0124 + US-0125).
  - **D3 (Parity scope surface)**: `check_intake_template_parity.py --scope=opencode-adapter` covers: (a) `template/.opencode/` pack (agents/commands/plugins), (b) installer host help/manifest (`--host cursor|opencode|both`), (c) runbook active+template parity, (d) reason-code table presence, (e) `test_us0121_*`..`test_us0126_*` marker presence. Exact surface inventory + pass/fail predicate is `/architecture`-locked per DQ3.
  - **D4 (Contract-test inventory)**: `test_us0126_*` cover: runbook "OpenCode host" section presence (AC-1), reason-code catalog presence + each code has remediation text (AC-2), `--scope=opencode-adapter` parity green (AC-3), per-story `test_us0121_*`..`test_us0125_*` marker checklist (AC-4), README hygiene + no-DEC-leak in operator sentences (AC-5), program DoD documented (AC-6), default-host reminder (AC-7), out-of-scope list present (AC-8), template doc parity (AC-9), Cursor docs not deleted (AC-10). Tests are static + grep-based; no live OpenCode runtime probe in this slice. Exact test list is `/architecture`-locked per DQ4.
  - **D5 (README hygiene + sanitization)**: user-visible OpenCode host blurb in README; US-0071 sanitization grep asserts no DEC ids in operator-facing sentences. UI is OpenCode; kit is the workflow. `test_us0126_readme_no_dec_leak` + `test_us0126_runbook_no_dec_leak` enforce AC-5.
  - **D6 (Program DoD operational test)**: runbook states the epic done-test: intake→release without Cursor; PO/Dev/QA as different sessions (optionally different providers); validators still block persistence. `test_us0126_program_dod_documented` asserts the DoD text is present and operationally worded (not a live end-to-end probe). Exact DoD wording is `/architecture`-locked per DQ5.
  - **D7 (Default host reminder)**: docs state cursor-only default until `--host opencode|both`. `test_us0126_default_host_reminder` asserts the reminder is present in runbook + README. Wording is `/architecture`-locked per DQ6.
  - **D8 (Out-of-scope list)**: runbook/README explicitly exclude standalone runtime, OpenCode fork, VS Code contrib rewrite, Caveman, Cursor-browser-as-primary-UAT. `test_us0126_out_of_scope_listed` asserts each excluded item is named. Exact exclusion phrasing is `/architecture`-locked per DQ7.
  - **D9 (Template doc parity)**: new doc files (or new runbook sections) are mirrored under `template/` where installer-owned. `installer-owned-paths.manifest` (active + `template/`) updated. `test_us0126_template_doc_parity` asserts active↔template parity for installer-owned doc paths touched by this slice.
  - **D10 (Compose — Cursor docs not deleted)**: `.cursor/commands/`, `.cursor/agents/`, existing Cursor kit docs are not deleted by US-0126. `test_us0126_cursor_docs_not_deleted` asserts byte-parity (or hash manifest) of `.cursor/` against the pre-US-0126 git state. OpenCode is additive (AC-10).
- **Open questions for `/research` (DQ1..DQ8+)** — all routed to tech-lead, anchor **R-0109** (US-0126-specific subsection; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 + US-0124 DQ1..DQ8 + US-0125 DQ1..DQ8 locks PRESERVED — not wiped):
  - **DQ1 (Runbook section anchor + heading, AC-1)**: what is the exact heading text and anchor for the "OpenCode host" section in `docs/engineering/runbook.md` (active + template)? Does it live under an existing "Hosts" heading or as a new top-level section? (R-0109 deepens — /architecture locks.)
  - **DQ2 (Reason-code catalog exact list, AC-2)**: what is the exhaustive `OPENCODE_*` + analogue code list US-0126 documents? Which codes are reused from US-0124/US-0125, which are new, and which are analogues of existing kit codes? What is the canonical remediation text per code? (Coordinate with US-0124 DQ4 + US-0125 DQ6/DQ7.)
  - **DQ3 (Parity scope surface inventory, AC-3)**: what is the exact surface inventory `--scope=opencode-adapter` covers — every file/glob under `template/.opencode/`, installer host help, runbook active+template, reason-code table, test markers? What is the deterministic pass/fail predicate? Does it reuse `check_intake_template_parity.py` infrastructure or add a sibling scope flag?
  - **DQ4 (`test_us0126_*` exact test list, AC-4)**: what is the exhaustive `test_us0126_*` test list — one test per AC, or a smaller curated set? Is the per-story `test_us0121_*`..`test_us0125_*` marker checklist a single aggregate test or per-story tests? Are tests static/grep-based or do any require a stub harness?
  - **DQ5 (Program DoD wording, AC-6)**: what is the exact operational DoD sentence the runbook must contain? "without Cursor" — does that mean no `.cursor/` directory loaded, or no Cursor IDE process? "different sessions/providers" — does that mean distinct OpenCode sessions, distinct `/connect` profiles, or distinct provider slugs? "validators still block" — which validator set is the regression baseline?
  - **DQ6 (Default host reminder wording, AC-7)**: what is the exact reminder sentence? Does it appear in runbook, README, or both? Does it cross-reference US-0121 `--host` flag help text?
  - **DQ7 (Out-of-scope phrasing, AC-8)**: what is the exact exclusion list phrasing? Does each excluded item cross-reference its owning masterplan (standalone-runtime-masterplan, opencode-adapter-masterplan) or decision (DEC-0055 Caveman)?
  - **DQ8 (Template parity manifest update, AC-9)**: which installer-owned doc paths does US-0126 add to `installer-owned-paths.manifest` (active + template)? Is the runbook itself already installer-owned, or only the new "OpenCode host" section? Does the manifest need a new entry per new doc file, or a single runbook entry covers both active + template?
- **Compose**: additive on US-0071/US-0113..US-0117/US-0121/US-0122/US-0123/US-0124/US-0125; do **not** delete Cursor kit docs; do **not** reimplement plugin or validators; do **not** invent a GUI; do **not** make Cursor-browser primary UAT. US-0126 owns the full runbook + reason-code table + `--scope=opencode-adapter` parity. No vendor slugs in `template/` (US-0102 family).
- **Next**: `/research` (tech-lead) to deepen **R-0109** for US-0126 (DQ1..DQ8 remain open; do not treat as architecture locks), then `/architecture` to lock the runbook section anchor + reason-code catalog + parity scope surface + `test_us0126_*` list + program DoD wording + default-host reminder + out-of-scope phrasing + template-parity manifest updates. Do NOT add `# US-0126` to architecture.md from PO discovery — `/architecture` (tech-lead) owns that H1 after `# US-0125`.

## Discovery Notes — US-0127

- **Story**: Convergence critic conjunct — blocking-only open findings plus non-blocking auto-resolve at sovereign-critic PASS (sovereign-loop convergence slice; unblocks `CONVERGENCE_CROSS_REVIEWER_OPEN` from ~280 informational PASS concurrence rows).
- **Discovery date**: 2026-08-25T18:27:31Z (UTC)
- **Role / model**: po / `composer-2.5` (CROSS_MODEL_REVIEW=1)
- **References**: intake evidence `handoffs/intake_evidence/US-0127-intake-20260825.json`; `scripts/sovereign_convergence_lib.py` (`_critic_jsonl_has_open` drift vs US-0110 L3); `scripts/sovereign_critic_lib.py` (`read_open_blocking`, `resolve_finding` — read-only compose); `handoffs/sovereign_critic_findings.jsonl`; `docs/product/backlog.md ## US-0127` (AC-1..AC-6); compose read-only **US-0104** / **US-0110** / **US-0107**; research anchor TBD by tech-lead (research owns R-id; expect sovereign-loop subsection — not R-0109 OpenCode epic).
- **Discovery locks D1–D10**:
  - **D1 (Blocking-only convergence conjunct)**: Replace `_critic_jsonl_has_open` in `scripts/sovereign_convergence_lib.py` (+ template mirror) with blocking-only semantics matching US-0110 L3 conjunct-3 and `read_open_blocking(repo)`. Only `blocking=true` AND `status=open` rows fail convergence; informational open rows must not block.
  - **D2 (Auto-resolve at sovereign-critic PASS)**: When `/sovereign-critic` PASS and `read_open_blocking` is empty, auto-set `status=resolved` on same-run non-blocking open rows in `handoffs/sovereign_critic_findings.jsonl`. Preserve audit trail; idempotent on re-run. Scope key (orchestrator_run_id vs phase_id) is `/research`-locked per DQ1.
  - **D3 (Hygiene CLI)**: New `scripts/sovereign_critic_hygiene.py` (+ template mirror): `--report`, `--resolve-nonblocking-for-run <orchestrator_run_id>`, `--dry-run`. Deterministic reason codes; exact inventory `/research`-locked per DQ2.
  - **D4 (Contract tests)**: `test_us0127_*` cover: non-blocking open does not fail convergence; blocking open fails with `CONVERGENCE_CROSS_REVIEWER_OPEN`; auto-resolve idempotent; hygiene CLI modes; compose regressions vs US-0110 conjunct-3 and US-0104 `read_open_blocking`. Exact list `/research`-locked per DQ3.
  - **D5 (Operator docs)**: Runbook convergence / cross-reviewer section (active + template) documents blocking-only conjunct + hygiene workflow + new reason codes. Section anchor `/research`-locked per DQ4.
  - **D6 (SOVEREIGN_CRITIC_PAIRS parity)**: Extend `--scope=sovereign-critic` pair table for hygiene script + convergence lib changes. Exact rows `/research`-locked per DQ5.
  - **D7 (QA markdown fallback)**: JSONL present → blocking-only JSONL authoritative; JSONL absent → retain QA grep heuristic; neither → skip per US-0110 degrade matrix.
  - **D8 (Compose US-0104)**: Read-only — no schema, reconciliation, lens, or predicate changes to critic lib.
  - **D9 (Compose US-0110)**: Read-only — five-conjunct structure unchanged except conjunct-3 blocking-only fix.
  - **D10 (Compose US-0107)**: Read-only — deferral/drain/stop matrix unchanged.
- **Open questions for `/research` (DQ1..DQ8)** — research owns R-id allocation; route to fresh tech-lead (do not extend R-0109 OpenCode epic):
  - **DQ1 (Auto-resolve scope key, AC-2)**: same `orchestrator_run_id` only vs same `phase_id` vs all non-blocking open rows? Batch helper vs repeated `resolve_finding`?
  - **DQ2 (Hygiene CLI reason codes, AC-3)**: exhaustive code list, exit codes, stdout markers, and `--dry-run` vs apply semantics?
  - **DQ3 (`test_us0127_*` inventory, AC-4)**: exact test names, fixture JSONL shapes, and compose regression pair list?
  - **DQ4 (Runbook section anchor, AC-5)**: heading text/anchor for blocking-only + hygiene workflow in active + template runbook?
  - **DQ5 (`SOVEREIGN_CRITIC_PAIRS` extension, AC-6)**: exact pair rows beyond existing five US-0104 pairs?
  - **DQ6 (Hook placement)**: auto-resolve in convergence lib eval path vs `/sovereign-critic` command post-PASS vs hygiene CLI-only operator path?
  - **DQ7 (QA fallback alignment)**: should `_qa_findings_has_open_critic` grep adopt blocking-only keywords when JSONL partial?
  - **DQ8 (Performance/idempotency)**: bounded batch resolve, fsync policy, and re-run noop detection for large JSONL tails?
- **Compose**: read-only with **US-0104** / **US-0110** / **US-0107**; do not mutate **US-0108** or **US-0121..US-0126** DONE rows; siblings **US-0128** / **US-0129** out of scope (boundary pointer only).
- **Next**: `/research` (tech-lead) to close DQ1..DQ8 and allocate/extend research entry, then `/architecture`. Do NOT add `# US-0127` to architecture.md from PO discovery.

## Discovery Notes — US-0128

- **Story**: Convergence smoke surrogate for contract-test and waived-probe UAT slices (sovereign-loop convergence; unblocks `CONVERGENCE_SMOKE_PROBE_FAIL` when harness is green but active `uat.json` waives all smoke probe classes with no smoke-named step).
- **Discovery date**: 2026-08-26T19:43:00Z (UTC)
- **Role / model**: po / `composer-2.5` (CROSS_MODEL_REVIEW=1)
- **References**: intake evidence `handoffs/intake_evidence/US-0128-intake-20260825.json` (RE-ATTEST PASS — JSON not mutated); `scripts/sovereign_convergence_lib.py` (`_eval_smoke_green`, `_uat_smoke_passes`, `_step_is_smoke`); `sprints/S0126/uat.json` (reference waived-probe fixture); `.cursor/commands/qa.md` + `verify-work.md`; `docs/product/backlog.md ## US-0128` (AC-1..AC-6); compose read-only **US-0109** deploy smoke / **US-0126** waived uat / **US-0110** five-conjunct; research anchor TBD by tech-lead (expect **R-0111** sovereign-loop smoke subsection — do not extend R-0110 US-0127 or R-0109 OpenCode epic).
- **Discovery locks D1–D10**:
  - **D1 (Surrogate eval — AC-1)**: Extend `_eval_smoke_green` in `scripts/sovereign_convergence_lib.py` (+ template mirror) so `smoke_green` passes via surrogate when active sprint `uat.json` exists, `tests/report.md` Fail:0, all canonical smoke probe classes documented in `waived_probes[]` with `reason_code=UAT_PROBE_FORBIDDEN`, `contract_test_failed=0`, and surrogate step predicate satisfied (D2). Legacy path unchanged: real smoke-named step PASS still satisfies conjunct when surrogate path does not apply.
  - **D2 (Canonical uat step — AC-2)**: Require a uat step with `id=convergence_smoke` (preferred) **or** tail step with `probe_kind=contract_tests_primary` and `result=pass`, written by `/qa` or `/verify-work` for ultra_lean/docs slices. Exact JSON shape `/research`-locked per DQ2.
  - **D3 (Fail closed — AC-3)**: Add `CONVERGENCE_SMOKE_SURROGATE_MISSING` to convergence reason codes when uat exists but surrogate prerequisites fail (missing/incomplete waived_probes, harness Fail>0, missing surrogate step, or `contract_test_failed>0`). Retain `CONVERGENCE_SMOKE_PROBE_FAIL` for deploy/real-smoke failures. No fake browser PASS.
  - **D4 (Command contracts — AC-4)**: Update `.cursor/commands/qa.md` and `.cursor/commands/verify-work.md` (+ template mirrors) to emit the canonical convergence smoke step for slices that waive live smoke probes. Exact contract text `/research`-locked per DQ5.
  - **D5 (Contract tests — AC-5)**: `test_us0128_*` cover: S0126-style waived uat + surrogate step → convergence PASS; missing surrogate → `CONVERGENCE_SMOKE_SURROGATE_MISSING`; harness Fail>0 → fail-closed; compose regression that US-0109 deploy smoke path semantics unchanged. Exact marker list `/research`-locked per DQ6.
  - **D6 (Operator docs — AC-6)**: Runbook Goal-Based Convergence / smoke-green section (active + template) documents surrogate eligibility, waived-probe predicate, surrogate step contract, and remediation for `CONVERGENCE_SMOKE_SURROGATE_MISSING`. Section anchor `/research`-locked per DQ7.
  - **D7 (Template parity — AC-6)**: `SOVEREIGN_CONVERGENCE_PAIRS` (+ `--scope=sovereign-convergence`) covers convergence lib mirror; command mirror parity for qa/verify-work touched surfaces. Exact pair rows `/research`-locked per DQ8.
  - **D8 (Compose US-0109)**: Deploy smoke post-publish path unchanged — when deploy smoke applies, real smoke step PASS remains required; surrogate path must not weaken US-0109 semantics.
  - **D9 (Compose US-0126)**: `sprints/S0126/uat.json` waived-probe fixture is reference input only; do not reopen US-0126 DONE product scope or mutate S0126 release artifacts.
  - **D10 (Compose US-0110 / DEC-0110)**: Five-conjunct structure preserved; only smoke conjunct gains surrogate branch aligned with DEC-0110 §10 smoke-green definition. Do not amend US-0127 critic conjunct or hygiene surfaces.
- **Open questions for `/research` (DQ1..DQ8)** — research owns R-id allocation (expect **R-0111**); route to fresh tech-lead (do not extend R-0110 US-0127):
  - **DQ1 (Waived-probe inventory, AC-1)**: what is the exhaustive `probe_class` list that must appear in `waived_probes[]` with `UAT_PROBE_FORBIDDEN` before surrogate path activates (S0126 lists six — is that canonical or slice-dependent)?
  - **DQ2 (Surrogate step schema, AC-2)**: exact JSON fields for `convergence_smoke` step vs `probe_kind=contract_tests_primary` tail fallback; required `evidence_ref` / `marker` keys?
  - **DQ3 (`contract_test_failed` source, AC-1)**: top-level `uat.json` field vs derived from `steps[]` / `probe_results[]` — which is authoritative for surrogate predicate?
  - **DQ4 (Precedence matrix, AC-1)**: when both a smoke-named step and surrogate path could apply, which wins; degrade behavior when partial waivers exist?
  - **DQ5 (Command contract placement, AC-4)**: exact qa.md / verify-work.md subsection anchors and emission rules for ultra_lean/docs slices only?
  - **DQ6 (`test_us0128_*` inventory, AC-5)**: exact test names, fixture uat paths, and US-0109 compose-regression guard shape?
  - **DQ7 (Runbook anchor, AC-6)**: heading text/anchor for surrogate rules in active + template runbook?
  - **DQ8 (`SOVEREIGN_CONVERGENCE_PAIRS`, AC-6)**: additive rows for command mirrors vs convergence lib only; does `--scope=sovereign-convergence` need extension?
- **Compose**: read-only with **US-0109** / **US-0126** / **US-0110** / **US-0127**; do not mutate **US-0108** or **US-0121..US-0127** DONE rows; sibling **US-0129** / **US-0130** out of scope (boundary pointer only).
- **Next**: `/research` (tech-lead) to close DQ1..DQ8 and allocate **R-0111**, then `/architecture`. Do NOT add `# US-0128` to architecture.md from PO discovery.

## Intake Notes — US-0131 and US-0132

- **Stories**: US-0131 Cross-host Its-Magic runtime configuration and parity; US-0132 Explicit Cursor/OpenCode model configuration contract.
- **Intake date**: 2026-09-06T00:00:00Z (UTC)
- **Role / run**: po / `opencode-20260906-cross-host-config-intake`. **Evidence**: `handoffs/intake_evidence/US-0131-0132-intake-20260906.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`).
- **Operator intent**: Close the missing OpenCode workflow/configuration gaps so shared Its-Magic behavior is handled correctly in Cursor-only, OpenCode-only, and both-host installations, including scratchpad and model configuration ownership.
- **Current gaps carried into discovery**: OpenCode does not load Cursor `.mdc` rules; thin OpenCode commands do not carry the complete Cursor read/gate contract; shared scripts still contain `.cursor` assumptions; the OpenCode validator hook is not visibly wired to the declared mapping; and plugin/command closure role resolution differs.
- **Split rationale**: US-0131 defines the host-neutral runtime/configuration adapter for shared behavior. US-0132 defines model-file ownership and keeps Cursor phase/tier catalogs separate from OpenCode per-role provider catalogs. Combining them would obscure two different schemas and precedence domains.
- **Operator locks**: no silent host fallback; no duplication of Cursor command/rule bodies; no credentials or real provider slugs in templates; local operator files remain protected; unsupported host-specific features fail or skip deterministically.
- **Next**: `/discovery` (fresh **po**) for **US-0131**, then **US-0132**.
- **Discovery**: see `## Discovery Notes — US-0131` below (US-0132 discovery deferred until US-0131 segment advances).

## Discovery Notes — US-0131

- **Story**: Cross-host Its-Magic runtime configuration and parity.
- **Discovery date**: 2026-09-07T19:15:00Z (UTC)
- **Role / model**: po / `composer-2.5` (CROSS_MODEL_REVIEW=1)
- **Orchestrator**: `orchestrator_run_id=auto-20260907-us0131`, `delivery_mode=ultra_lean`, macro=`spec` (intake PASS — not re-intaken)
- **References**: `docs/product/backlog.md` `## US-0131` (AC-1..AC-8 + Boundaries); intake `handoffs/intake_evidence/US-0131-0132-intake-20260906.json` (RE-ATTEST read-only — JSON not mutated); vision intake notes above; DEC-0055 / US-0073 scratchpad Model B; DEC-0039 example refresh + local preservation; US-0121..US-0126 OpenCode adapter compose; OpenCode config surfaces https://opencode.ai/v2/docs/config/ (`opencode.json{,c}`, `.opencode/`); script hardcode inventory (`auto_outer_driver.py`, `opencode_auto_bridge.py`, `enforce-triad-hot-surface.py`, `dev_environment_lib.py`, `caveman_compress_input.py`).
- **Current gap (locked)**: Shared governance/runtime keys are still consumed via Cursor-path readers. OpenCode-only installs cannot satisfy the shared kernel without inventing a `.cursor/` dependency. Host-specific UX (Cursor `.mdc` rules, OpenCode Layer-1 agents/plugin) must stay classified — not silently assumed everywhere.
- **UX / operator config surface (discovery)**:
  - **Cursor**: team baseline `.cursor/scratchpad.md` + personal `.cursor/scratchpad.local.md` (gitignored) remain the familiar compatibility UX; installer must not overwrite active local files (DEC-0039 compose).
  - **OpenCode**: operators already use `opencode.json{,c}` + `.opencode/` for host pack/agents/commands/plugins — kit shared settings must resolve without requiring `.cursor/`; do **not** dump kit governance keys into OpenCode model/`permission` schema without an explicit architecture lock (DQ1).
  - **Both**: one deterministic precedence; no conflicting duplicate writes; independent host-local overrides where schemas differ.
- **Capability classification seed (for `/research` to finalize)**:
  - **Shared / host-neutral**: `DELIVERY_MODE`, `TOKEN_PROFILE`, `AUTO_*` orchestration keys, intake/work-kind/id-bootstrap keys, triad hot-surface thresholds, phase plan/exclude/include, state/handoff governance toggles used by Python validators and outer driver.
  - **Cursor-only (fail/skip when absent)**: `.cursor/rules/*.mdc` advisory surface, Cursor browser MCP UAT path, `REMOTE_CONFIG=.cursor/remote.json` default path, Cursor Task spawn wiring, `MODEL_PROVIDER_MODE=cursor` (compose note — model resolution owned by US-0132).
  - **OpenCode-only (fail/skip when absent)**: `.opencode/agents` Layer-1 matrix, orchestrator plugin spawn, thin `.opencode/commands`, `OPENCODE_*` reason codes, OpenCode `/connect` auth store.
  - **US-0132-owned (do not specify here)**: `.cursor/model-catalog.local.json`, `.opencode/model-catalog.local.json`, scratchpad `MODEL_*` / `MODEL_TIER_*`, materializers, volatile slug policy.
- **Discovery locks D1–D10**:
  - **D1 (Host-neutral SOT — AC-1)**: Document a typed, host-neutral configuration contract for shared Its-Magic runtime/governance settings. No credentials, provider secrets, or real vendor model slugs in the contract or templates.
  - **D2 (Cursor compatibility adapter — AC-2)**: Cursor scratchpad layers (DEC-0055 Model B merge + DEC-0039 local protection) remain a **compatibility reader/adapter** into the host-neutral contract — not silently redefined as the only SOT.
  - **D3 (OpenCode-only operation — AC-3)**: OpenCode-only install must resolve all shared settings required by supported lifecycle phases **without** requiring `.cursor/scratchpad.md` or `.cursor/scratchpad.local.md`.
  - **D4 (Shared-kernel migration — AC-4)**: Shared Python validators, outer-driver paths, triad/state/handoff governance, and common scripts accept resolved configuration explicitly; hardcoding `.cursor` for host-neutral behavior is forbidden after migration.
  - **D5 (Host-specific boundaries — AC-5)**: Cursor-only and OpenCode-only capabilities are classified; unavailable capabilities fail or skip with documented reason codes — no silent unsupported-parity claims; no cloning of Cursor command/rule bodies into OpenCode.
  - **D6 (Both-host determinism — AC-6)**: `--host both` has one deterministic precedence model, prevents conflicting duplicate writes, and preserves independent host-local overrides where schemas differ.
  - **D7 (Installer safety — AC-7)**: Install / missing / upgrade / clean deliver config **examples** to the selected host, preserve local operator files, and do not overwrite active scratchpad/config data.
  - **D8 (Verification + docs — AC-8)**: Cross-host contract tests for cursor-only, opencode-only, and both-host modes; document supported lifecycle phases, config precedence, migration, and reason-code behavior (active + template).
  - **D9 (US-0132 boundary)**: Model catalog ownership, materialization, and `MODEL_*` schemas remain **US-0132**. US-0131 may pass through resolved non-model settings only; do not invent a third undocumented model SOT (`model.json` forbidden — US-0132).
  - **D10 (Compose do-not-amend)**: Compose US-0073/DEC-0055, DEC-0039, US-0121..US-0126, US-0092 outer driver, US-0069 phase→role. Do **not** reopen BUG-0015/BUG-0016; do **not** amend Cursor or OpenCode model DECs (0086/0087/0123).
- **Open questions for `/research` (DQ1..DQ10)** — research owns **`R-0116`** allocation (do not extend R-0115 BUG-0016):
  - **DQ1 (Neutral config path — AC-1/AC-3)**: Canonical filesystem location for the host-neutral contract (repo-root kit file vs `.its-magic/` vs `.opencode/its-magic-*.json` vs other) — must not require `.cursor/` on OpenCode-only.
  - **DQ2 (Schema shape — AC-1)**: Typed schema for shared keys vs host-adapter overlays; versioning; fail-closed codes for malformed/missing required shared keys.
  - **DQ3 (Cursor adapter — AC-2)**: How scratchpad merge (baseline + local) maps into the neutral resolver without breaking DEC-0055 precedence or DEC-0039 preservation.
  - **DQ4 (OpenCode adapter — AC-3)**: How OpenCode-only installs supply shared settings (dedicated kit config file vs reading a non-model subset of `opencode.json` — latter discouraged unless architecture proves isolation from US-0132 surfaces).
  - **DQ5 (Hardcode inventory — AC-4)**: Complete inventory of `.cursor/scratchpad*` (and related) hardcodes in `scripts/` / `its_magic/` and the migration injection API shape.
  - **DQ6 (Both-host precedence — AC-6)**: Exact precedence table when Cursor adapter + OpenCode adapter + neutral file coexist under `--host both`.
  - **DQ7 (Capability matrix — AC-5)**: Finalize shared / Cursor-only / OpenCode-only / skip-vs-fail matrix with reason-code family names.
  - **DQ8 (Installer surfaces — AC-7)**: Which installer/manifest paths deliver examples per `--host cursor|opencode|both`; confirm never-overwrite rules for local operator files.
  - **DQ9 (Contract tests — AC-8)**: Minimal `test_us0131_*` marker inventory + fixture strategy (cursor-only / opencode-only / both) without live OpenCode CI probe.
  - **DQ10 (Docs parity — AC-8)**: Runbook/README/auto-orchestration-reference anchors (active + template) for precedence, migration, and unsupported-capability behavior.

## Intake Notes — US-0130

- **Story**: Operator-pinned sovereign-critic model (catalog `roles.critic` + scratchpad `MODEL_SOVEREIGN-CRITIC`).
- **Intake date**: 2026-08-26T18:00:00Z (UTC)
- **Role**: po. **Pack**: small-intake-pack. **Evidence**: `handoffs/intake_evidence/US-0130-intake-20260826.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`).
- **Operator intent**: Set the critic AI model the same way role catalogs pin PO/SA/DEV (example: `.cursor/model-catalog.local.example.role-based-balanced_cursor_only.json`).
- **Locks from guided Q&A**:
  - Precedence: `MODEL_SOVEREIGN-CRITIC` > catalog `roles.critic` > today’s opposition/`dev` fallback.
  - Collision: keep `CROSS_MODEL_DEGRADED_MODE` (not fail-closed, not auto-next-slug).
  - Granularity: one global critic for all producer phases (no per-lens v1).
  - Done includes installer/template example delivery of the new key (US-0112 compose).
- **Compose**: overlay on **US-0104** / **US-0102** / **US-0112**; do not amend critic findings schema or canonical-phase resolver.
- **Next**: `/discovery` (fresh po).
- **Handoff**: full PO→TL intake section archived at `handoffs/archive/po-to-tl-pack-20260826.md` (`triad-rollover|po_to_tl` moved=1, retained_lines=650).
- **Discovery**: see `## Discovery Notes — US-0130` below.

## Discovery Notes — US-0130

- **Story**: Operator-pinned sovereign-critic model (catalog `roles.critic` + scratchpad `MODEL_SOVEREIGN-CRITIC`).
- **Discovery date**: 2026-08-26T21:23:00Z (UTC)
- **Role / model**: po / `composer-2.5` (CROSS_MODEL_REVIEW=1)
- **References**: intake evidence `handoffs/intake_evidence/US-0130-intake-20260826.json` (RE-ATTEST PASS — JSON not mutated); `scripts/sovereign_critic_lib.py` (`select_critic_model`, `_resolve_slug_for_tier`, `CRITIC_TIER_OPPOSITION`); `scripts/model_tier_lib.py` (`CATALOG_ROLE_KEYS`, `override_key`, `resolve_model_for_phase` 5-step chain); `.cursor/model-catalog.local.example.role-based-balanced_cursor_only.json` (no `roles.critic` today); `.cursor/scratchpad.md` CROSS_MODEL / MODEL comments; `docs/product/backlog.md ## US-0130` (AC-1..AC-9); compose read-only **US-0104** / **US-0102** / **US-0112** / **US-0127** / **US-0128** DONE; research anchor TBD by tech-lead (expect **R-0112** — do not extend R-0111 US-0128).
- **Current gap (locked)**: `select_critic_model` resolves via tier opposition on synthetic phase `sovereign-critic` and does **not** read `MODEL_SOVEREIGN-CRITIC` or catalog `roles.critic`. `CATALOG_ROLE_KEYS` = `po, sa, dev, dev_difficult, qa, security, release` — no `critic`. `override_key("sovereign-critic")` → `MODEL_SOVEREIGN-CRITIC` (hyphen preserved in scratchpad key).
- **Operator locks (from intake)**: `both_precedence`, `degraded_keep`, `one_global`, `plus_installer`.
- **Discovery locks D1–D10**:
  - **D1 (Scratchpad pin — AC-1)**: Document and consume `MODEL_SOVEREIGN-CRITIC=<slug>` as highest-precedence critic pin for synthetic phase `sovereign-critic` (hyphenated scratchpad key; template comments = placeholders only; vendor slugs live in `.cursor/scratchpad.local.md`).
  - **D2 (Catalog `roles.critic` — AC-2)**: Additive optional v2 role key. When present and `MODEL_RESOLVE=role_catalog`, resolver uses it after scratchpad pin. When absent, existing v2 catalogs remain valid (no forced migration / no fail-closed missing-key). Whether `critic` joins `CATALOG_ROLE_KEYS` required-set vs optional overlay is `/research`-locked (DQ1).
  - **D3 (`select_critic_model` precedence — AC-3)**: `MODEL_SOVEREIGN-CRITIC` > `roles.critic` (when `MODEL_RESOLVE=role_catalog`) > current `CRITIC_TIER_OPPOSITION` / `_resolve_slug_for_tier("sovereign-critic", …)` / `dev` fallback. Pin lookup must consume hyphenated key (no `MODEL_SOVEREIGN_CRITIC` underscore alias miss). Implementation path: dedicated overlay in `select_critic_model` vs reusing `resolve_model_for_phase("sovereign-critic")` is `/research`-locked (DQ2).
  - **D4 (Collision policy — AC-4)**: If resolved critic slug equals producer slug, keep `degraded_mode=true` / `CROSS_MODEL_DEGRADED_MODE` single-model-multi-lens — not a hard stop, not auto-next-slug.
  - **D5 (One global critic — AC-5)**: v1 is one critic model for all producer phases. Out of scope: per-lens slugs; per-producer-phase critic overrides.
  - **D6 (Contract tests — AC-6)**: `test_us0130_*` cover pin-wins, catalog `roles.critic` hit, omitted-key fallback to opposition path, same-slug degraded path, and US-0104 findings-schema compose guard (no JSONL / lens / anti-slop regression).
  - **D7 (Compose do not amend — AC-7)**: US-0104 findings JSONL schema, three lenses, `CROSS_MODEL_REVIEW` + threshold + rework keys, anti-slop formula unchanged. US-0101 default phase-tier matrix unchanged. US-0102 canonical-phase 5-step chain unchanged (overlay only on critic selection).
  - **D8 (Examples + installer — AC-8)**: US-0112 compose — role-based example catalogs (including `.cursor/model-catalog.local.example.role-based-balanced_cursor_only.json` and template mirrors) gain `critic` key (placeholder or Cursor-only real slugs in cursor-only example). Installer/manifest ships updated examples; **never** writes `model-catalog.local.json`. Exact installer surfaces `/research`-locked (DQ5).
  - **D9 (Docs + parity — AC-9)**: Scratchpad CROSS_MODEL / MODEL comments document critic pin; runbook critic-model troubleshooting section (active + template). Architecture `# US-0130` anchor is **out of PO scope** — tech-lead authors in `/architecture` after `/research` (PO did not add to `architecture.md`).
  - **D10 (Compose guards)**: US-0127 / US-0128 DONE — do not reopen. US-0129 out of scope. Cursor Task allowlist / BYOK inheritance is document-only per **R-0088** (no runtime routing change in this slice).
- **Open questions for `/research` (DQ1..DQ8)** — research owns R-id allocation (expect **R-0112**); route to fresh tech-lead (do not extend R-0111 US-0128):
  - **DQ1 (`CATALOG_ROLE_KEYS` — AC-2)**: Should `critic` be added to the v2 schema required-set (`CATALOG_ROLE_KEYS`) or remain an optional overlay key validated only when present?
  - **DQ2 (Resolver integration — AC-3)**: Reuse `resolve_model_for_phase("sovereign-critic")` with synthetic phase registration vs dedicated pin/catalog branch inside `select_critic_model` only?
  - **DQ3 (Hyphenated scratchpad key — AC-1/AC-3)**: Exact parse rules for `MODEL_SOVEREIGN-CRITIC` vs `override_key` / scratchpad merge — confirm hyphen is preserved end-to-end (no underscore normalization).
  - **DQ4 (Example slug policy — AC-8)**: Placeholder tokens in generic examples vs real Cursor Task slugs in `role-based-balanced_cursor_only` example — which catalogs get which treatment?
  - **DQ5 (Installer compose surfaces — AC-8)**: Which installer/manifest paths must ship updated example catalogs (active vs `template/` mirrors; parity script rows)?
  - **DQ6 (`validate_catalog_v2` — AC-2)**: Schema validator changes for optional `roles.critic` — error codes and backward-compat matrix for catalogs missing the key?
  - **DQ7 (Opposition fallback interaction — AC-3)**: When pin and catalog both absent, confirm `CRITIC_TIER_OPPOSITION` + `_resolve_slug_for_tier("sovereign-critic", …)` behavior is unchanged from US-0104 baseline?
  - **DQ8 (Scratchpad doc anchors — AC-9)**: Exact comment-block placement in `.cursor/scratchpad.md` / template for `MODEL_SOVEREIGN-CRITIC` and critic pin precedence relative to existing MODEL_* / CROSS_MODEL_* sections?

## Intake Notes — US-0129

- **Story**: Architecture hot-surface rollover linkage guard (active contract preservation).
- **Intake date**: 2026-08-25T18:20:30Z (UTC). **RE-ATTEST**: 2026-08-27T07:01:00Z (`auto-20260827-01`).
- **Role**: po. **Pack**: small-intake-pack. **Evidence**: `handoffs/intake_evidence/US-0129-intake-20260825.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`; JSON not mutated on RE-ATTEST).
- **Operator intent**: Block or bounded auto-repair architecture triad rollover when active-only US/BUG heading refs required by contract tests would break; prevent US-0126 B-1 style Fail:7 after rollover archives active tokens.
- **Compose**: read-only **DEC-0054** / **DEC-0073** / **US-0049** / **US-0126** B-1 fixture; do not reopen US-0126 product scope; **US-0127** / **US-0128** / **US-0130** DONE — boundary pointer only.
- **Discovery**: see `## Discovery Notes — US-0129` below.

## Discovery Notes — US-0129

- **Story**: Architecture hot-surface rollover linkage guard (active contract preservation).
- **Discovery date**: 2026-08-27T07:02:00Z (UTC)
- **Role / model**: po / `composer-2.5` (CROSS_MODEL_REVIEW=1)
- **References**: intake evidence `handoffs/intake_evidence/US-0129-intake-20260825.json` (RE-ATTEST PASS — JSON not mutated); `scripts/enforce-triad-hot-surface.py` (`rollover_architecture`, `split_arch_stories`, `ARCH_HOT_MAX_LINES`, `ARCH_HOT_MAX_STORY_SECTIONS`); `.cursor/commands/refresh-context.md` triad rollover step; `sprints/S0126/uat.md` B-1 harness Fail:7 root cause (rollover archived `# US-0090` / `# US-0091` / `# US-0093` while contract tests grep active surface); `tests/auto_command_contract_test.py` (`test_caveman_compress_input_architecture_linkage`, `test_bug0011_architecture_linkage`, `test_us0093_architecture_linkage`); `tests/readme_feature_coverage_fixtures_test.py::test_readme_feature_coverage_architecture_linkage`; `docs/product/backlog.md ## US-0129` (AC-1..AC-6); compose read-only **DEC-0054** / **DEC-0073** / **US-0049** / **US-0126**; **US-0127** / **US-0128** / **US-0130** DONE not reopened.
- **Current gap (locked)**: `rollover_architecture` pops oldest story blocks from `docs/engineering/architecture.md` hot surface without checking whether contract tests still require those `# US-xxxx` / BUG linkage headings in the active file. US-0126 ship hit B-1: architecture rollover moved US-0090/US-0091/US-0093 tokens to `docs/engineering/architecture-archive/architecture-pack-20260825.md` while `tests/auto_command_contract_test.py` and readme-feature-coverage linkage tests still `assertIn("# US-0090")` etc. on active `architecture.md` → harness Fail:7.
- **Discovery locks D1–D10**:
  - **D1 (Linkage guard script — AC-1)**: Add `scripts/arch_linkage_guard.py` (+ `template/scripts/` mirror) invoked **pre** and **post** `python scripts/enforce-triad-hot-surface.py --rollover`; detect active-only US/BUG heading refs required by contract tests before rollover commits.
  - **D2 (Fail-closed block — AC-2)**: On violation emit `ARCH_LINKAGE_ROLLOVER_BLOCKED` with story/bug id, missing heading token, archive pack path, remediation prose. New reason-code family — registration surface in `docs/engineering/reason_codes.md` is `/research`-locked (DQ5).
  - **D3 (Optional auto-repair — AC-3)**: Bounded restore of **minimal H1 stubs** from latest `docs/engineering/architecture-archive/architecture-pack-*.md`; idempotent; audit row in `state.md` on repair. Default-off vs default-on under `AUTONOMY_STOP_POLICY` is `/research`-locked (DQ1, DQ4).
  - **D4 (Rollover wiring — AC-4)**: Wire guard into `/refresh-context` triad rollover path (between cap read and `--rollover` / after `--rollover` per DQ3); **do not** change `rollover_architecture` heading-split semantics or archiver pack format (DEC-0054 compose).
  - **D5 (Regression + harness marker — AC-5)**: US-0126 B-1 fixture — rollover without guard must FAIL linkage contract tests; with guard must PASS or emit explicit `ARCH_LINKAGE_ROLLOVER_BLOCKED` block. Harness marker name `/research`-locked (DQ6).
  - **D6 (Contract tests — AC-1..AC-5)**: `test_us0129_*` inventory covering guard pre/post hook, block metadata, optional auto-repair idempotency, refresh-context wiring grep, B-1 regression slice. Exact count/names `/research`-locked (DQ7).
  - **D7 (Compose — AC-6)**: Read-only with **DEC-0054** (triad hot-surface), **DEC-0073** (H1 anchor policy), **US-0049** (state archive contract), **US-0126** B-1 fixture only — do **not** reopen US-0126 product scope or mutate DONE rows **US-0127** / **US-0128** / **US-0130**.
  - **D8 (Template parity — AC-4)**: Script mirror, runbook h2 operator troubleshooting, `.cursor/commands/refresh-context.md` command surface parity, `check_intake_template_parity.py` pair row if applicable.
  - **D9 (Architecture anchor)**: `# US-0129` in `docs/engineering/architecture.md` is **out of PO scope** — tech-lead authors in `/architecture` after `/research` (PO did not add architecture anchor).
  - **D10 (Scope guard)**: Guard-only slice — no change to `ARCH_HOT_MAX_LINES` / `ARCH_HOT_MAX_STORY_SECTIONS` policy numbers or scratchpad defaults unless `/research` proves required (DQ8).
- **Open questions for `/research` (DQ1..DQ8)** — research owns R-id allocation (expect **R-0113**; do not extend **R-0112** US-0130); route to fresh tech-lead:
  - **DQ1 (Auto-repair default — AC-3)**: Default-off (block-only) vs default-on (auto-repair then rollover) vs operator scratchpad flag?
  - **DQ2 (Linkage discovery — AC-1)**: How to discover the authoritative set of "active-only headings required by contract tests" — static grep inventory of `tests/` for `# US-` / BUG tokens vs manifest file vs coupling to `validate_readme_feature_coverage` story list?
  - **DQ3 (Hook ordering — AC-1/AC-4)**: Pre-rollover only, post-rollover only, or both — and whether pre-hook blocks before any archive write vs post-hook rollback?
  - **DQ4 (`AUTONOMY_STOP_POLICY` — AC-2/AC-3)**: Under `full_autonomy`, fail-closed block vs attempt bounded auto-repair first — precedence and stop-matrix row?
  - **DQ5 (Reason-code registration — AC-2)**: Where to register `ARCH_LINKAGE_ROLLOVER_BLOCKED` in `docs/engineering/reason_codes.md` (new h3 vs extend triad/archive family); template mirror + runbook cross-link?
  - **DQ6 (Harness marker — AC-5)**: Exact pytest marker / harness row name for US-0126 B-1 regression slice?
  - **DQ7 (`test_us0129_*` inventory — AC-5/AC-6)**: Exact test count, names, and fixture paths (synthetic mini-architecture vs replay `architecture-pack-20260825.md`)?
  - **DQ8 (Minimal stub shape — AC-3)**: What constitutes a "minimal H1 stub" restored from archive — heading line only vs heading + one linkage sentence vs full archived section cap?

