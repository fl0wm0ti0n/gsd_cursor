# Backlog

## US-0001 — Core Workflow Commands
- Title: Slash commands for the full dev lifecycle
- Summary: Implement Cursor slash commands covering intake, discovery, research, architecture, sprint-plan, plan-verify, execute, qa, verify-work, release, pause, resume, refresh-context.
- Priority: P0
- Status: DONE
- Notes: 19 commands implemented (plan called for 10). Additional commands: auto, quick, milestone-start, milestone-complete, map-codebase, phase-context.

## US-0002 — AI Behavior Rules
- Title: Rules for phase flow, quality, handoffs, escalation, coding standards
- Summary: Create .mdc rules that enforce structured workflow, small steps, artifact persistence, decision gates, and coding best practices.
- Priority: P0
- Status: DONE
- Notes: 5 rules implemented (plan called for 4). Added coding-standards.mdc.

## US-0003 — Subagent Definitions
- Title: Six AI team roles (PO, Tech Lead, Dev, QA, Release, Curator)
- Summary: Define subagent personas with clear inputs, outputs, and artifact responsibilities.
- Priority: P0
- Status: DONE

## US-0004 — Skill and Templates
- Title: its-magic skill with structured templates
- Summary: Create SKILL.md describing the workflow plus JSON/MD templates for stories, acceptance, architecture, decisions, sprints, handoffs, UAT, milestones, and phase context.
- Priority: P0
- Status: DONE
- Notes: 14 templates implemented (plan called for 6).

## US-0005 — Hook System
- Title: Cursor hooks for safety, context tracking, and quality gates
- Summary: Implement hooks for beforeShellExecution (block dangerous commands), beforeReadFile (warn on secrets), afterFileEdit (track code vs. context changes), stop (remind context refresh).
- Priority: P0
- Status: DONE

## US-0006 — Artifact Templates and Starter Docs
- Title: Product/engineering docs, sprint starters, handoff templates, decision records
- Summary: Create placeholder docs and starter artifacts so the workflow has files to read/write from the start.
- Priority: P0
- Status: DONE

## US-0007 — CI/CD Workflows
- Title: GitHub Actions for CI (test/lint/typecheck) and deploy (staging/prod)
- Summary: Workflows read commands from runbook.md. CI includes auto-fix retry loop. Deploy is manual dispatch.
- Priority: P1
- Status: DONE
- Notes: Expanded beyond plan with 3-layer quality chain and 5 CI jobs (checks, auto-fix, npm-test, brew-test, choco-test).

## US-0008 — CLI Installer
- Title: Drop-in installer that copies workflow files into any repo
- Summary: Node.js CLI wrapper that delegates to OS-specific installer (PowerShell, Bash, Python). Supports modes: missing, overwrite, interactive. Optional backup and clean-repo.
- Priority: P1
- Status: DONE
- Notes: Plan listed this as "optional" (section 3D). Fully implemented with triple-installer parity.

## US-0009 — Multiplatform Distribution
- Title: Publish via npm, Chocolatey, and Homebrew
- Summary: Unified release scripts handle version bump, npm publish, GitHub release, Chocolatey pack/push, and Homebrew formula update.
- Priority: P1
- Status: DONE
- Notes: Entirely beyond original plan scope.

## US-0010 — Voice Input Documentation
- Title: Document multilingual voice input options
- Summary: README documents OS dictation, Cursor voice, and local STT (Whisper) as input strategies. Includes slash-command reliability pattern.
- Priority: P2
- Status: DONE

## US-0011 — Automation Modes
- Title: Configurable automation levels via scratchpad flags
- Summary: AUTO_FLOW_MODE, PHASE_MODE, PERMISSION_MODE, RUN_TESTS_ON_EDIT, LOOP_UNTIL_GREEN, AUTO_IMPLEMENTATION_LOOP, AUTO_LOOP_MAX_CYCLES, AUTO_PAUSE_REQUEST/POLICY.
- Priority: P1
- Status: DONE
- Notes: Beyond original plan scope.

## US-0012 — Benchmark Suite
- Title: Validation and performance benchmarks
- Summary: Scenario-based, live, headless, and prompted benchmarks for verifying the kit works correctly.
- Priority: P2
- Status: DONE
- Notes: Beyond original plan scope.

## US-0013 — Team Mode
- Title: Multi-developer support with local overrides
- Summary: Shared scratchpad.md (committed) plus personal scratchpad.local.md (gitignored) with TEAM_MODE, TEAM_MEMBER, ACTIVE_TASK_IDS flags.
- Priority: P2
- Status: DONE
- Notes: Beyond original plan scope.

## US-0014 — Quality Chain (3-Layer)
- Title: Automated quality enforcement at three levels
- Summary: Layer 1 (Cursor AI loop), Layer 2 (local validate-and-push), Layer 3 (CI auto-fix). Each catches what the previous missed.
- Priority: P1
- Status: DONE
- Notes: Plan mentioned hooks + CI. The 3-layer chain with validate-and-push scripts and bounded retry loops is beyond plan.

---

## Remaining / Polish Items

## US-0015 — Runbook Completion
- Title: Configure remaining runbook commands
- Summary: Only TEST_COMMAND is set. LINT_COMMAND, FORMAT_COMMAND, TYPECHECK_COMMAND are empty. This is acceptable for a template/installer project (mostly Markdown/YAML/JSON), but should be documented as intentional.
- Priority: P3
- Status: OPEN

## US-0016 — Homebrew Version Sync
- Title: Sync Homebrew stable formula version with npm
- Summary: Homebrew stable formula is at 0.1.1, npm is at 0.1.2-17. Next release should align versions across all three channels.
- Priority: P2
- Status: OPEN

## US-0017 — Template Drift Guard
- Title: Prevent drift between active workflow files and template/ copies
- Summary: The repo uses its own workflow (self-dogfooding), so active .cursor/, docs/, sprints/ files may diverge from template/ copies. Consider a sync-check test or convention to keep them aligned.
- Priority: P2
- Status: OPEN

## US-0018 — Smart Upgrade Mode
- Title: Safe, version-aware upgrade for repos already using its-magic
- Summary: When a user updates its-magic (e.g. `npm update -g its-magic`) and re-runs the installer on a repo that already has it, the current modes don't handle this well. `missing` skips changed files, `overwrite` destroys user data, `interactive` gives no context about what actually changed. A proper upgrade needs to distinguish between framework files (commands, rules, agents, hooks, skills, CI workflows, scripts) that should be updated and user data files (docs, sprints, handoffs, decisions, runbook, scratchpad) that should be preserved.
- Priority: P1
- Status: OPEN
- Acceptance:
  - [ ] AC-1: Version tracking — installer writes a `.its-magic-version` file (or similar) in the target repo recording the installed version.
  - [ ] AC-2: File classification — files are categorized as "framework" (safe to update) or "user-data" (preserve on upgrade).
  - [ ] AC-3: New `--mode upgrade` (or equivalent) that updates framework files, preserves user data files, and warns about user-customized framework files that changed.
  - [ ] AC-4: Upgrade summary — after running, shows what was updated, what was preserved, and what needs manual attention.
  - [ ] AC-5: New-file delivery — new files added in a newer version are always copied (regardless of category).
  - [ ] AC-6: Migration notes — when file formats or required fields change between versions, guidance is provided (e.g. MIGRATION.md or inline notes).
  - [ ] AC-7: Triple installer parity — upgrade mode works identically across installer.ps1, installer.sh, and installer.py.
  - [ ] AC-8: README documents the upgrade workflow.
- Notes: This addresses the gap where users who already use its-magic update the tool and need to propagate changes to their repos without losing sprint data, decisions, or runbook customizations.

## US-0020 — /ask Command: Context-Aware Questions Without Workflow
- Title: Read-only command for questions that uses the project memory
- Summary: Add an `/ask` command that loads the project context pack (state.md, backlog.md, acceptance.md, decisions.md, architecture.md, current sprint progress) and answers user questions without creating artifacts or modifying any files. This fills the gap between "use a slash command" (triggers the workflow engine) and "just talk" (no project context loaded).
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: `/ask` command exists with read-only behavior (no file writes, no state changes)
  - [x] AC-2: Command loads context pack: state.md, backlog.md, acceptance.md, decisions.md, architecture.md, current sprint progress, runbook.md
  - [x] AC-3: Can reference existing stories, decisions, and tasks by ID
  - [x] AC-4: Works for questions, status checks, and "how does X work" queries
  - [x] AC-5: Explicitly documented in README as the lightweight interaction channel

## US-0021 — Critical Evaluation in Intake and Architecture
- Title: AI challenges ideas, checks duplicates, and suggests alternatives before accepting
- Summary: Update the PO agent behavior and the `/intake` command so the AI does not blindly accept every idea. Before creating a backlog item, the AI should: (1) check if the idea is already covered by an existing story or decision, (2) evaluate whether the approach is sound or if a simpler/better alternative exists, (3) challenge assumptions and ask "is this the right solution or just the first one?", (4) only create a story after this evaluation passes. The same critical thinking applies to `/architecture` (challenge design decisions) and `/sprint-plan` (challenge task breakdown). `/intake` remains the single entry point for bugs, features, and improvements -- no need for separate `/bug` or `/feature-request` commands.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: PO agent checks backlog for duplicates/overlaps before creating new stories
  - [x] AC-2: PO agent evaluates feasibility and suggests alternatives when appropriate
  - [x] AC-3: PO agent challenges assumptions ("is this the best approach?") before accepting
  - [x] AC-4: `/intake` command steps updated to include evaluation phase
  - [x] AC-5: `/architecture` command steps updated to include design challenge phase
  - [x] AC-6: PO and Tech Lead agent definitions updated with critical evaluation behavior
  - [x] AC-7: Evaluation is constructive, not blocking -- good ideas proceed faster, weak ideas get improved

## US-0022 — Sprint Sizing Rules and Configurable Sprint Planning
- Title: Explicit sprint sizing framework with scratchpad-configurable options
- Summary: The system currently has no explicit decision framework for sprint sizing. The Tech Lead implicitly decides how many tasks fit in a sprint and whether work should be split across multiple sprints. This story adds: (1) sprint sizing rules to the Tech Lead agent and /sprint-plan command (max tasks, when to split, when to suggest /quick), and (2) scratchpad-configurable options so teams can tune sprint planning behavior (e.g. max tasks per sprint, auto-split threshold, new-idea routing).
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: Tech Lead agent has explicit sprint sizing rules (max tasks, split criteria)
  - [x] AC-2: /sprint-plan command evaluates scope and proposes splitting when work exceeds threshold
  - [x] AC-3: Scratchpad has configurable sprint planning options (SPRINT_MAX_TASKS, SPRINT_AUTO_SPLIT)
  - [x] AC-4: When a new idea arrives during an active sprint, the system recommends whether to add it to the current sprint, defer to a new sprint, or suggest /quick
  - [x] AC-5: For initial project intake with large scope, /sprint-plan suggests milestone-based breakdown when multiple sprints are needed
  - [x] AC-6: Both active and template copies updated
  - [x] AC-7: Defaults are sensible (e.g. max 12 tasks) — teams can override via scratchpad

## US-0023 — Fresh Subagent Context Per Phase and /auto Orchestration
- Title: Enforce real new agent context at every handoff boundary
- Summary: Ensure each workflow phase runs in a fresh subagent context, make handoff files the only cross-phase memory, and redefine `/auto` as orchestration that spawns a new subagent for every phase (including each execute/qa loop cycle).
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: Core workflow rules explicitly require fresh context per phase/handoff.
  - [x] AC-2: All phase commands include an execution model section requiring new subagent contexts.
  - [x] AC-3: Agent role definitions explicitly state fresh-context behavior and stop-after-handoff.
  - [x] AC-4: `/auto` is documented as orchestrator-only and describes spawning new subagents per phase.
  - [x] AC-5: Execute/QA loop explicitly requires new Dev and QA subagent instances on every cycle.
  - [x] AC-6: Active and template workflow files are aligned for the new isolation model.

## US-0024 — Memory Drift Audit Command
- Title: Detect drift between artifact memory and actual codebase changes
- Summary: Add a read-only audit command that checks whether repository memory artifacts (state, decisions, backlog, acceptance, handoffs) still match recent codebase changes, especially when coding happened outside the workflow. This is distinct from template drift: it compares artifact claims to real code state, not active files to `template/`.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: New read-only audit command exists (for example `/memory-audit`) and does not modify source code, workflow rules, or sprint artifacts.
  - [x] AC-2: Command writes a report artifact (for example `docs/engineering/memory-drift-report.md`) with timestamp, scope, findings, and severity levels.
  - [x] AC-3: Detection coverage includes at least: changed code files without corresponding artifact updates, unresolved TODO decisions, and mismatches between declared sprint/story status and repository signals.
  - [x] AC-4: Report explicitly separates **memory drift** findings from **template drift** findings and references `US-0017` for template sync concerns.
  - [x] AC-5: Command outputs non-blocking guidance (recommended next actions, suggested commands, linked artifacts) and returns success unless invocation fails.
  - [x] AC-6: Command behavior and report format are documented in README/runbook so teams can run it before handoff, QA, or release.

## US-0025 — Backlog-to-Sprint Traceability Contract
- Title: Enforce explicit mapping between backlog stories and sprint execution artifacts
- Summary: Define and enforce a lightweight traceability contract so every OPEN/DONE story can be traced to sprint tasks and completion evidence. This closes the gap where backlog status and sprint artifacts drift without a single cross-reference index.
- Priority: P1
- Status: OPEN
- Acceptance:
  - [ ] AC-1: A canonical traceability index format is defined and documented (for example story ID -> sprint ID -> task IDs -> status/evidence links).
  - [ ] AC-2: At least one maintained artifact provides a project-wide cross-reference index spanning all active/completed sprints.
  - [ ] AC-3: "Backlog-sprint mismatch solved" is explicitly defined as: no OPEN/DONE story lacks a traceability entry, and no sprint task claims story work without a story ID.
  - [ ] AC-4: Intake/sprint planning guidance requires assigning story IDs to sprint tasks at creation time.
  - [ ] AC-5: Verification guidance includes a pre-handoff check for missing/ambiguous traceability entries.
  - [ ] AC-6: Scope stays separate from `US-0017` (template drift) and `US-0024` (memory-vs-code drift); this story focuses only on story/sprint artifact linkage.

## US-0026 — Milestone Lifecycle Definition and Exit Criteria
- Title: Define milestone lifecycle states, required fields, and command expectations
- Summary: Formalize milestone lifecycle behavior so milestones are intentionally created, populated, progressed, and completed instead of remaining placeholder-like. Clarify exactly when `milestones/*` artifacts must be updated in the workflow.
- Priority: P1
- Status: OPEN
- Acceptance:
  - [ ] AC-1: Milestone lifecycle states are defined with entry/exit criteria (at minimum: created, active, in-review/ready-to-complete, completed/cancelled).
  - [ ] AC-2: Required milestone artifact fields are defined by phase (for example `name`, `goal`, `scope`, phase list, progress expectations) and cannot stay empty past intake.
  - [ ] AC-3: `/milestone-start` and `/milestone-complete` guidance documents when and how `milestone.json`, `phases.json`, and `progress.md` are populated/updated.
  - [ ] AC-4: Process guidance distinguishes placeholder initialization from mandatory real content during execution.
  - [ ] AC-5: Handoff/verification guidance includes milestone readiness checks before completion is allowed.
  - [ ] AC-6: Scope stays separate from sprint sizing/automation stories (`US-0022`/`US-0023`); this story is lifecycle governance for milestone artifacts.

## US-0027 — UAT Artifact Lifecycle and Ownership
- Title: Define when UAT artifacts are placeholders, who populates them, and how they gate completion
- Summary: Remove confusion around `sprints/Sxxxx/uat.json` and `uat.md` by formalizing their lifecycle, ownership, and minimum content expectations across planning, QA, and verify-work phases.
- Priority: P1
- Status: OPEN
- Acceptance:
  - [ ] AC-1: UAT lifecycle is defined by phase, explicitly separating placeholder creation from execution-time population.
  - [ ] AC-2: Ownership is explicit for each UAT update step (who writes steps, records results, and marks pass/fail).
  - [ ] AC-3: Minimum required fields/content for `uat.json` and `uat.md` are defined before a sprint can be marked complete.
  - [ ] AC-4: Verify-work/release readiness guidance references UAT artifacts as required evidence, not optional placeholders.
  - [ ] AC-5: Commands/docs explain how UAT links back to story acceptance criteria and sprint tasks.
  - [ ] AC-6: Scope stays separate from `US-0024`; this story governs UAT artifact lifecycle, not memory-vs-code drift detection.

## US-0028 — Security & Compliance Review Agent
- Title: Optional security/compliance review step with configurable compliance profiles
- Summary: Add an optional security review agent and `/security-review` command activated via scratchpad flags. Runs at two workflow points: (1) post-architecture for design review, (2) post-execute for code review. Supports compliance profiles (GDPR, SOC2, HIPAA, PCI-DSS, ISO27001). Zero overhead when disabled. Findings to `docs/engineering/security-review.md`.
- Priority: P1
- Status: OPEN
- Acceptance:
  - [ ] AC-1: New agent definition `security.mdc` with inputs, outputs, persona, and artifact responsibilities.
  - [ ] AC-2: New `/security-review` command with design review and code review steps.
  - [ ] AC-3: Scratchpad flags `SECURITY_REVIEW` (on/off) and `COMPLIANCE_PROFILES` (comma-separated) control activation.
  - [ ] AC-4: When `SECURITY_REVIEW` is disabled (default), zero workflow overhead.
  - [ ] AC-5: Design review analyzes architecture decisions, data flows, auth patterns against selected profiles.
  - [ ] AC-6: Code review analyzes implementation for secrets, injection, auth/authz gaps, profile-specific requirements.
  - [ ] AC-7: Findings to `docs/engineering/security-review.md` with severity, affected components, remediation.
  - [ ] AC-8: Workflow rules invoke security review at correct points when enabled.
  - [ ] AC-9: Critical findings create decision records and block progression until resolved.
  - [ ] AC-10: Template copies include security agent, command, and placeholder security-review.md.

## US-0029 — Knowledge Curation & Early Research
- Title: Structured knowledge curation with early web research during intake and architecture
- Summary: Integrate web research into early workflow phases so PO and Tech Lead agents have external references when making decisions. Enhance `/research` for structured, referenceable output. Persist knowledge in `docs/engineering/research.md` with entry IDs, timestamps, sources, and story linkage. Curator maintains the knowledge base. Subsumes Q0002 (research persistence).
- Priority: P1
- Status: OPEN
- Acceptance:
  - [ ] AC-1: PO agent searches the web for relevant context during `/intake` and persists findings as a research entry.
  - [ ] AC-2: Tech Lead agent searches the web for technical references during `/architecture` and persists findings.
  - [ ] AC-3: `/research` produces structured output: entry ID (R-xxxx), date, topic, query, sources, findings, linked story/decision IDs, confidence.
  - [ ] AC-4: `docs/engineering/research.md` uses structured format — entries individually referenceable by ID.
  - [ ] AC-5: `/intake` and `/architecture` command steps include explicit "research external context" step before evaluation/design.
  - [ ] AC-6: Other agents can reference research entries by ID in their artifacts.
  - [ ] AC-7: Curator agent includes research knowledge base in maintenance scope (prune stale, consolidate duplicates, flag outdated).
  - [ ] AC-8: Scratchpad flag `EARLY_RESEARCH` (default: on) controls PO/TL web research; `/research` command always works manually.
  - [ ] AC-9: Research entries include status field (current/outdated/superseded) for knowledge freshness.
  - [ ] AC-10: Template copies updated with structured research.md, updated agents, updated commands.

## US-0019 — Clean Placeholder Content from Templates and Active Files
- Title: Remove useless placeholder stubs from template and active artifact files
- Summary: Template files (template/) and root-level active files ship with placeholder content like `- ...`, `Option A/B/C`, `Criterion 1/2` that adds noise. Since the framework commands and agents know how to populate these files, the placeholders are redundant. Clean all template and active artifact files to contain only section headers without fake content. JSON files keep valid minimal structure.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: All template/ artifact files (docs, sprints, handoffs, decisions) contain only section headers, no `- ...` stubs.
  - [x] AC-2: All root-level active artifact files that are still placeholders are cleaned the same way.
  - [x] AC-3: JSON placeholder files have valid minimal structure (empty arrays/strings).
  - [x] AC-4: Files with real content (vision.md, backlog.md, architecture.md, etc.) are NOT touched.
  - [x] AC-5: Template README.md is NOT touched (has real content).

## US-0030 — Release Gate for Command/Flag Documentation Delta
- Title: Block release when command/flag behavior changed without README/runbook updates
- Summary: Add a release readiness gate that compares command/flag changes against documentation updates and blocks `/release` when `README.md` and `docs/engineering/runbook.md` are stale or inconsistent for changed CLI/options/workflow flags.
- Priority: P1
- Status: OPEN
- Acceptance:
  - [ ] AC-1: Release guidance defines a mandatory "doc delta check" step before release notes are finalized.
  - [ ] AC-2: If commands/flags changed in scope, and neither `README.md` nor `docs/engineering/runbook.md` reflects the change, release is blocked with explicit remediation guidance.
  - [ ] AC-3: If only one of `README.md` or `docs/engineering/runbook.md` is updated for a command/flag change, release is blocked until parity is restored.
  - [ ] AC-4: Non-command/flag changes do not trigger this gate (no false blocking for unrelated edits).
  - [ ] AC-5: Gate output clearly lists each changed command/flag and where documentation evidence was found or missing.
  - [ ] AC-6: README and runbook required sections for command/flag documentation are explicitly defined so checks are deterministic.
  - [ ] AC-7: Release handoff format includes a pass/fail record for the doc delta gate.
  - [ ] AC-8: Template parity: active and `template/` release/runbook/readme guidance are aligned for this gate behavior.
- Boundaries:
  - In scope: workflow/process guardrails for release readiness and artifact consistency.
  - Out of scope: implementing new product features or changing command semantics beyond documentation and gate behavior.

## US-0031 — Optional Documentation Pack (Design Concept, CRS, Technical Spec)
- Title: Add optional spec-pack generation/check flow controlled by configuration
- Summary: Introduce an optional workflow path that creates and validates a documentation pack containing Design Concept, CRS, and Technical Specification artifacts when enabled; zero overhead when disabled.
- Priority: P2
- Status: OPEN
- Acceptance:
  - [ ] AC-1: A single enable flag/config exists to control spec-pack behavior, defaulting to disabled.
  - [ ] AC-2: When disabled, no extra required steps are added to intake/architecture/release flow.
  - [ ] AC-3: When enabled, workflow creates/updates three artifacts with canonical names/locations: Design Concept, CRS, Technical Specification.
  - [ ] AC-4: Each artifact has minimum required sections/fields defined so completeness is testable.
  - [ ] AC-5: Validation checks report per-artifact completeness and block progression only when enabled and required sections are missing.
  - [ ] AC-6: Traceability is defined from backlog story IDs to the generated spec-pack artifacts.
  - [ ] AC-7: Guidance clarifies ownership (which role/phase maintains each document).
  - [ ] AC-8: Template parity: active and `template/` command/rules/docs references for spec-pack mode remain aligned.
- Boundaries:
  - In scope: optional documentation-process capability and quality checks.
  - Out of scope: prescribing domain-specific content models beyond minimal required structure.

## US-0032 — Optional Feature User Guide Generation
- Title: Generate user-friendly instructions for each feature behind an explicit flag
- Summary: Add an optional workflow capability that produces and maintains end-user-facing instructions for each feature/story (what it does, how to use it, examples, limitations, troubleshooting) with deterministic structure and validation, while imposing zero overhead when disabled.
- Priority: P2
- Status: OPEN
- Acceptance:
  - [ ] AC-1: A dedicated config flag exists to enable/disable feature user guide generation, defaulting to disabled.
  - [ ] AC-2: When the flag is disabled, intake/architecture/sprint/execute/qa/release flows add no required guide-generation steps and no new blocking checks.
  - [ ] AC-3: When enabled, each accepted feature story gets a linked user guide artifact in a canonical location and naming format.
  - [ ] AC-4: A minimum required guide schema is defined and testable (at least: feature purpose, prerequisites, usage steps, example, limitations, troubleshooting).
  - [ ] AC-5: Validation reports completeness per guide and fails only when enabled and required sections are missing.
  - [ ] AC-6: Guide traceability is explicit from story ID to user guide artifact, and referenced in handoff/release context.
  - [ ] AC-7: Boundaries are enforced between user guides and technical spec-pack docs (`US-0031`) so duplicate ownership/content is avoided.
  - [ ] AC-8: Template parity is maintained for active and `template/` docs/commands/rules references related to this optional mode.
- Boundaries:
  - In scope: optional user-facing documentation process, artifact structure, validation, and traceability.
  - Out of scope: replacing technical design docs (Design Concept/CRS/Technical Spec), and writing domain-specific product manuals beyond per-feature usage guidance.

## US-0033 — Configurable Guided Intake Behavior
- Title: Let PO ask clarifying questions with options and research by default, with an off switch
- Summary: Formalize a guided intake mode where PO asks reasonable follow-up questions when scope is unclear, suggests options instead of prematurely deciding implementation, and performs intake-time web research. Add a single switch to disable this proactive behavior for teams that want low-touch intake.
- Priority: P1
- Status: OPEN
- Acceptance:
  - [ ] AC-1: `/intake` guided mode asks targeted follow-up questions only when ambiguity blocks concrete acceptance criteria.
  - [ ] AC-2: In guided mode, PO presents at least one viable option/alternative before proposing a recommendation.
  - [ ] AC-3: Guided mode explicitly preserves user decision authority (PO recommends; user decides).
  - [ ] AC-4: Guided mode includes PO web research step with persisted evidence in `docs/engineering/research.md` and linked story context.
  - [ ] AC-5: A single scratchpad switch controls guided intake behavior (default: enabled).
  - [ ] AC-6: When the switch is disabled, `/intake` adds zero proactive follow-up/options/research overhead and proceeds in low-touch mode unless user requests depth.
  - [ ] AC-7: Low-touch mode still preserves baseline safety: duplicate/overlap check against backlog remains active.
  - [ ] AC-8: `/intake` command and `po.mdc` clearly document both modes and mode-specific expectations.
  - [ ] AC-9: Active and `template/` copies remain behaviorally aligned for the new switch.
- Boundaries:
  - In scope: intake interaction behavior, explicit user choice, and mode toggling.
  - Out of scope: changing downstream architecture/sprint execution semantics.

## US-0034 — Multi-Repo and Contract Compatibility Observability
- Title: Track module/API compatibility across repos and components
- Summary: Add an optional workflow capability that watches relevant modules, docs, and API contracts across one or more repositories, then reports compatibility risk and contract drift to engineering artifacts. This is process observability and validation, not runtime feature logic.
- Priority: P1
- Status: OPEN
- Acceptance:
  - [ ] AC-1: A dedicated config toggle exists (for example `CROSS_REPO_OBSERVABILITY`), defaulting to disabled.
  - [ ] AC-2: When disabled (default), `/intake`, `/architecture`, `/execute`, and `/qa` add no required extra steps or blocking checks.
  - [ ] AC-3: When enabled, configuration supports an explicit source list of monitored repositories/modules/artifacts (at least repo path/URL, module ID, and contract/doc location).
  - [ ] AC-4: Compatibility checks include at minimum: API signature compatibility, declared version/contract mismatch detection, and documentation/API description drift signals.
  - [ ] AC-5: Findings are persisted in a canonical artifact (for example `docs/engineering/compatibility-report.md`) with severity, affected module(s), evidence, and recommended next action.
  - [ ] AC-6: If enabled and critical compatibility breakage is detected, workflow raises a decision gate before release progression.
  - [ ] AC-7: Reports are traceable to backlog story IDs and sprint/task context so QA/release can verify coverage.
  - [ ] AC-8: Active and `template/` copies of commands/rules/docs remain aligned for this optional mode.
- Boundaries:
  - In scope: workflow-level compatibility visibility, artifact persistence, and gate policy.
  - Out of scope: implementing cross-repo CI orchestration engines or runtime service mesh behavior.

## US-0035 — Component-Scoped Execution Mode with Protection Guards
- Title: Execute workflow on selected component(s) without destabilizing others
- Summary: Add a component-scoped mode so teams can target one component in a multi-component repo while protecting unaffected components through scope-aware planning and verification rules. Defaults stay lightweight when mode is off.
- Priority: P1
- Status: OPEN
- Acceptance:
  - [ ] AC-1: A dedicated scope control exists (for example `COMPONENT_SCOPE_MODE` plus `TARGET_COMPONENTS`), with mode default disabled.
  - [ ] AC-2: When disabled (default), workflow behavior is unchanged and introduces zero required overhead.
  - [ ] AC-3: When enabled, `/intake` and `/architecture` require explicit in-scope and out-of-scope component declaration in artifacts.
  - [ ] AC-4: `/sprint-plan` and task artifacts require each task to declare target component(s) and expected impacted interfaces.
  - [ ] AC-5: `/execute` guidance enforces scope-first execution (no intentional edits outside declared target components unless escalated and approved).
  - [ ] AC-6: `/qa` includes unaffected-component protection checks (for example smoke/regression checks for declared non-target components) before completion.
  - [ ] AC-7: If enabled and out-of-scope component impact is detected without prior approval, workflow triggers a decision gate.
  - [ ] AC-8: Active and `template/` command/rule/docs guidance stays behaviorally aligned for component-scoped mode.
- Boundaries:
  - In scope: workflow scoping, artifact contracts, guardrails, and validation guidance.
  - Out of scope: monorepo build-system redesign or automatic dependency graph generation beyond declared scope metadata.

## US-0036 — Official Remote Config Template, Docs, and Fail-Fast Validation
- Title: Ship canonical `.cursor/remote.json` template with schema guidance and safe validation
- Summary: Add an official remote execution configuration artifact and supporting documentation so teams can use `REMOTE_EXECUTION=1` safely. Provide clear schema/field expectations, example targets, and validation behavior that fails fast on invalid config while keeping zero overhead when `REMOTE_EXECUTION=0`.
- Priority: P1
- Status: OPEN
- Acceptance:
  - [ ] AC-1: Canonical `.cursor/remote.json` template exists in both active repo and `template/` with aligned defaults and comments/examples where appropriate.
  - [ ] AC-2: Remote config schema is documented (required vs optional fields, data types, allowed values, path/host conventions).
  - [ ] AC-3: Documentation includes at least two concrete example target configurations (for example local network host and remote VM/container endpoint) using safe placeholder values.
  - [ ] AC-4: Validation guidance is defined to fail fast when `REMOTE_EXECUTION=1` and config is missing, malformed, or semantically invalid.
  - [ ] AC-5: Validation output specifies actionable error messages (which field failed, expected format/range, and remediation hint).
  - [ ] AC-6: When `REMOTE_EXECUTION=0` (default), workflow imposes zero required remote-config steps and no false-fail checks.
  - [ ] AC-7: Security guidance explicitly prohibits committing secrets/tokens in `.cursor/remote.json` and provides approved secret-handling alternatives.
  - [ ] AC-8: README and `docs/engineering/runbook.md` document remote setup, validation behavior, and mode-specific expectations (`REMOTE_EXECUTION` on/off).
  - [ ] AC-9: Template parity is verified: active and `template/` copies of remote config references/docs/validation guidance are behaviorally aligned.
- Boundaries:
  - In scope: configuration template, schema/validation contract, docs/runbook guidance, and workflow-level safety expectations.
  - Out of scope: implementing new remote execution transport protocols or external secret-management infrastructure.

## US-0037 — Mid-Process `/auto` Continuation with Deterministic Resume Point
- Title: Continue full workflow from an explicit or resolved phase without manual phase triggers
- Summary: Users can pause mid-workflow, then run one command to continue full automation from the right phase through the remaining pipeline. Add explicit `start-from` support to `/auto`, deterministic resume-source resolution (`handoffs/resume_brief.md` first, `docs/engineering/state.md` fallback), and clear stop/log behavior while preserving safe defaults.
- Priority: P1
- Status: OPEN
- Acceptance:
  - [ ] AC-1: `/auto` supports an explicit `start-from` phase input (canonical phase IDs) to begin orchestration mid-process.
  - [ ] AC-2: When `start-from` is omitted, resume phase is resolved deterministically in this order: `handoffs/resume_brief.md` -> `docs/engineering/state.md` fallback.
  - [ ] AC-3: If both resume sources are missing, stale, or conflicting, the command fails safely with actionable guidance instead of guessing.
  - [ ] AC-4: A single `/auto` invocation from mid-process continues through all remaining phases (including execute/QA loop behavior when enabled) without requiring manual phase commands.
  - [ ] AC-5: Existing stop conditions remain enforced (decision gate, missing critical input, pause request, loop max cycles); continuation does not bypass gates.
  - [ ] AC-6: Continuation writes deterministic audit breadcrumbs to artifacts (at minimum: chosen start phase, source used, stop reason) so resume behavior is inspectable.
  - [ ] AC-7: Default-safe behavior is preserved: manual/interactive teams are unaffected unless auto continuation mode is explicitly used.
  - [ ] AC-8: `/pause`, `/resume`, and `/auto` guidance is behaviorally aligned around resume semantics to avoid contradictory flow instructions.
  - [ ] AC-9: Active and `template/` command/rule/docs copies remain aligned for the continuation behavior.
- Boundaries:
  - In scope: workflow orchestration semantics, resume-source precedence, artifact logging, and command/rule/doc parity.
  - Out of scope: changing phase deliverables, bypassing decision gates, or adding runtime product features unrelated to workflow control.

## US-0038 — Phase-Triggered Sync Policy with Guarded Auto-Push
- Title: Configurable sync cadence after completed phases with QA-first safety defaults
- Summary: Add a configurable phase-triggered sync policy that controls when local check-in sync/push is attempted (`disabled`, `manual`, `by_phase`, `by_milestone`, custom phase list). Keep behavior safe-by-default: no automatic push before QA pass for feature work, and always run check-in tests before any push attempt.
- Priority: P1
- Status: OPEN
- Acceptance:
  - [ ] AC-1: A canonical sync policy configuration exists and is documented (at minimum: `disabled`, `manual`, `by_phase`, `by_milestone`, `custom_phase_list`), with default set to a non-auto mode.
  - [ ] AC-2: Policy evaluation runs only at phase-completion boundaries and determines whether a sync attempt is eligible at that boundary.
  - [ ] AC-3: Mandatory pre-push checks always include `TEST_COMMAND`; push is blocked when tests fail, timeout, or are missing.
  - [ ] AC-4: Optional checks (`LINT_COMMAND`, `TYPECHECK_COMMAND`, formatter/lint-fix) are honored when configured in runbook and reported clearly in sync output.
  - [ ] AC-5: For feature work, automatic push before QA completion is forbidden; before QA pass, only manual user-invoked sync is allowed.
  - [ ] AC-6: If QA produced blocking findings or unresolved critical issues, sync policy must not auto-push and must emit actionable remediation guidance.
  - [ ] AC-7: Branch safety constraints are enforced for auto-sync (for example protected/default branch deny by default unless explicit opt-in allowlist is configured).
  - [ ] AC-8: Sync operations produce deterministic evidence in artifacts/logs (phase, policy mode, checks run, pass/fail, push decision, reason code).
  - [ ] AC-9: `scripts/validate-and-push.ps1` and `scripts/validate-and-push.sh` remain behaviorally aligned for mandatory test execution and gating semantics (template parity where applicable).
  - [ ] AC-10: When sync policy is disabled/manual (default), workflow overhead is near zero and existing manual push behavior remains unchanged.
- Boundaries:
  - In scope: sync policy semantics, check gating contract, safety defaults, and artifact evidence.
  - Out of scope: adding new CI providers, changing runtime product behavior, or forcing one git branching strategy for all teams.

## US-0039 — Release Gate Tightening for Check-In Tests and QA/UAT Completion
- Title: Allow release only after mandatory check-in tests and QA/UAT readiness
- Summary: Tighten release readiness so `/release` proceeds only when check-in tests have passed and QA/UAT completion criteria are met. This complements phase sync policy by enforcing a hard final gate before release artifacts are finalized.
- Priority: P1
- Status: OPEN
- Acceptance:
  - [ ] AC-1: `/release` includes an explicit mandatory gate that verifies latest check-in test result is passing (`TEST_COMMAND` baseline).
  - [ ] AC-2: If check-in test evidence is missing, stale, or failing, release is blocked with deterministic fail reason and remediation steps.
  - [ ] AC-3: `/release` requires QA completion evidence (no unresolved blocking findings in current sprint context) before proceeding.
  - [ ] AC-4: Existing UAT completeness gate remains mandatory; release fails when UAT artifacts are placeholder, incomplete, or unresolved-fail state.
  - [ ] AC-5: Gate ordering is deterministic: check-in test gate first, then QA gate, then UAT gate, then release-note/runbook updates.
  - [ ] AC-6: Release output records per-gate pass/fail status and evidence pointers in handoff/state artifacts so QA and TL can audit decisions.
  - [ ] AC-7: No release path may bypass these gates in default configuration; any override path (if allowed) requires explicit decision gate + documented rationale.
  - [ ] AC-8: Active and `template/` release/qa/execute guidance remains behaviorally aligned for gate semantics (template parity AC).
  - [ ] AC-9: Regression coverage includes positive and negative cases for each gate and for stale-evidence scenarios.
  - [ ] AC-10: Safe default behavior is preserved for teams without optional lint/typecheck commands: release still requires test + QA/UAT evidence and does not falsely fail on blank optional runbook keys.
- Boundaries:
  - In scope: release readiness policy, gate order, evidence contract, and blocking behavior.
  - Out of scope: redefining sprint lifecycle, changing acceptance ownership, or replacing existing QA/UAT artifact formats.

## US-0040 — Per-Sprint Release Notes and Release Queue Tracker
- Title: Prevent release-note overwrite and track unreleased vs released sprints
- Summary: Replace single-file release note behavior with per-sprint release note artifacts and add a canonical release queue tracker that records each sprint's release status (`unreleased`/`released`) with deterministic state updates.
- Priority: P1
- Status: OPEN
- Acceptance:
  - [ ] AC-1: `/release` writes sprint-scoped notes to a canonical path (for example `handoffs/releases/Sxxxx-release-notes.md`) and must not overwrite notes from other sprints.
  - [ ] AC-2: A canonical release queue artifact exists (for example `handoffs/release_queue.md` or `release_queue.json`) with at least sprint ID, status (`unreleased|released`), last-updated timestamp, and release-notes reference.
  - [ ] AC-3: Queue update semantics are deterministic: entering release flow for a sprint creates/updates an `unreleased` entry; successful release finalization transitions only that sprint to `released`.
  - [ ] AC-4: Default-safe behavior: if sprint identity cannot be resolved, release must not overwrite any existing release notes and must fail safely with remediation guidance.
  - [ ] AC-5: Backfill/migration behavior is defined for existing `handoffs/release_notes.md`: preserve legacy file, attempt one-time migration to sprint-scoped file when sprint context is resolvable, otherwise record manual-migration guidance.
  - [ ] AC-6: Existing workflows that read `handoffs/release_notes.md` remain backward-compatible (for example via pointer/latest summary behavior) without destructive data loss.
  - [ ] AC-7: Release readiness/reporting surfaces unreleased sprint queue entries so pending releases are visible before finalization.
  - [ ] AC-8: Release command/rules/docs define clear ownership and phase touchpoints for queue state transitions and note generation.
  - [ ] AC-9: Template parity is maintained: active and `template/` copies of release guidance/artifacts are behaviorally aligned for per-sprint notes and queue tracking.
- Boundaries:
  - In scope: release artifact conventions, migration/backfill contract, queue status lifecycle, and workflow documentation/rules updates.
  - Out of scope: changing deployment runtime behavior, introducing external release-management services, or redefining QA/UAT evidence formats.
