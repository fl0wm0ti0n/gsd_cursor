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
