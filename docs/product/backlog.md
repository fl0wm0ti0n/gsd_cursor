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
- Status: DONE
- Acceptance:
  - [x] AC-1: Runbook explicitly documents that optional command keys may remain intentionally blank for this project type.
  - [x] AC-2: README explicitly documents that empty optional runbook command keys are intentional defaults, not missing configuration errors.
  - [x] AC-3: Active and `template/` runbook/README guidance remains behaviorally aligned for this intent.
  - [x] AC-4: Regression checks verify the intent statement remains present in docs artifacts.

## US-0016 — Homebrew Version Sync
- Title: Sync Homebrew stable formula version with npm
- Summary: Homebrew stable formula is at 0.1.1, npm is at 0.1.2-17. Next release should align versions across all three channels.
- Priority: P2
- Status: DONE
- Acceptance:
  - [x] AC-1: Homebrew stable formula URL tag version is aligned with `package.json` version.
  - [x] AC-2: Homebrew stable formula `version` field is aligned with `package.json` version.
  - [x] AC-3: Regression checks validate version alignment to prevent drift.

## US-0017 — Template Drift Guard
- Title: Prevent drift between active workflow files and template/ copies
- Summary: The repo uses its own workflow (self-dogfooding), so active .cursor/, docs/, sprints/ files may diverge from template/ copies. Consider a sync-check test or convention to keep them aligned.
- Priority: P2
- Status: DONE

## US-0018 — Smart Upgrade Mode
- Title: Safe, version-aware upgrade for repos already using its-magic
- Summary: When a user updates its-magic (e.g. `npm update -g its-magic`) and re-runs the installer on a repo that already has it, the current modes don't handle this well. `missing` skips changed files, `overwrite` destroys user data, `interactive` gives no context about what actually changed. A proper upgrade needs to distinguish between framework files (commands, rules, agents, hooks, skills, CI workflows, scripts) that should be updated and user data files (docs, sprints, handoffs, decisions, runbook, scratchpad) that should be preserved.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: Version tracking — installer writes a `.its-magic-version` file (or similar) in the target repo recording the installed version.
  - [x] AC-2: File classification — files are categorized as "framework" (safe to update) or "user-data" (preserve on upgrade).
  - [x] AC-3: New `--mode upgrade` (or equivalent) that updates framework files, preserves user data files, and warns about user-customized framework files that changed.
  - [x] AC-4: Upgrade summary — after running, shows what was updated, what was preserved, and what needs manual attention.
  - [x] AC-5: New-file delivery — new files added in a newer version are always copied (regardless of category).
  - [x] AC-6: Migration notes — when file formats or required fields change between versions, guidance is provided (e.g. MIGRATION.md or inline notes).
  - [x] AC-7: Triple installer parity — upgrade mode works identically across installer.ps1, installer.sh, and installer.py.
  - [x] AC-8: README documents the upgrade workflow.
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
- Status: DONE
- Acceptance:
  - [x] AC-1: A canonical traceability index format is defined and documented (for example story ID -> sprint ID -> task IDs -> status/evidence links).
  - [x] AC-2: At least one maintained artifact provides a project-wide cross-reference index spanning all active/completed sprints.
  - [x] AC-3: "Backlog-sprint mismatch solved" is explicitly defined as: no OPEN/DONE story lacks a traceability entry, and no sprint task claims story work without a story ID.
  - [x] AC-4: Intake/sprint planning guidance requires assigning story IDs to sprint tasks at creation time.
  - [x] AC-5: Verification guidance includes a pre-handoff check for missing/ambiguous traceability entries.
  - [x] AC-6: Scope stays separate from `US-0017` (template drift) and `US-0024` (memory-vs-code drift); this story focuses only on story/sprint artifact linkage.

## US-0026 — Milestone Lifecycle Definition and Exit Criteria
- Title: Define milestone lifecycle states, required fields, and command expectations
- Summary: Formalize milestone lifecycle behavior so milestones are intentionally created, populated, progressed, and completed instead of remaining placeholder-like. Clarify exactly when `milestones/*` artifacts must be updated in the workflow.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: Milestone lifecycle states are defined with entry/exit criteria (at minimum: created, active, in-review/ready-to-complete, completed/cancelled).
  - [x] AC-2: Required milestone artifact fields are defined by phase (for example `name`, `goal`, `scope`, phase list, progress expectations) and cannot stay empty past intake.
  - [x] AC-3: `/milestone-start` and `/milestone-complete` guidance documents when and how `milestone.json`, `phases.json`, and `progress.md` are populated/updated.
  - [x] AC-4: Process guidance distinguishes placeholder initialization from mandatory real content during execution.
  - [x] AC-5: Handoff/verification guidance includes milestone readiness checks before completion is allowed.
  - [x] AC-6: Scope stays separate from sprint sizing/automation stories (`US-0022`/`US-0023`); this story is lifecycle governance for milestone artifacts.

## US-0027 — UAT Artifact Lifecycle and Ownership
- Title: Define when UAT artifacts are placeholders, who populates them, and how they gate completion
- Summary: Remove confusion around `sprints/Sxxxx/uat.json` and `uat.md` by formalizing their lifecycle, ownership, and minimum content expectations across planning, QA, and verify-work phases.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: UAT lifecycle is defined by phase, explicitly separating placeholder creation from execution-time population.
  - [x] AC-2: Ownership is explicit for each UAT update step (who writes steps, records results, and marks pass/fail).
  - [x] AC-3: Minimum required fields/content for `uat.json` and `uat.md` are defined before a sprint can be marked complete.
  - [x] AC-4: Verify-work/release readiness guidance references UAT artifacts as required evidence, not optional placeholders.
  - [x] AC-5: Commands/docs explain how UAT links back to story acceptance criteria and sprint tasks.
  - [x] AC-6: Scope stays separate from `US-0024`; this story governs UAT artifact lifecycle, not memory-vs-code drift detection.

## US-0028 — Security & Compliance Review Agent
- Title: Optional security/compliance review step with configurable compliance profiles
- Summary: Add an optional security review agent and `/security-review` command activated via scratchpad flags. Runs at two workflow points: (1) post-architecture for design review, (2) post-execute for code review. Supports compliance profiles (GDPR, SOC2, HIPAA, PCI-DSS, ISO27001). Zero overhead when disabled. Findings to `docs/engineering/security-review.md`.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: New agent definition `security.mdc` with inputs, outputs, persona, and artifact responsibilities.
  - [x] AC-2: New `/security-review` command with design review and code review steps.
  - [x] AC-3: Scratchpad flags `SECURITY_REVIEW` (on/off) and `COMPLIANCE_PROFILES` (comma-separated) control activation.
  - [x] AC-4: When `SECURITY_REVIEW` is disabled (default), zero workflow overhead.
  - [x] AC-5: Design review analyzes architecture decisions, data flows, auth patterns against selected profiles.
  - [x] AC-6: Code review analyzes implementation for secrets, injection, auth/authz gaps, profile-specific requirements.
  - [x] AC-7: Findings to `docs/engineering/security-review.md` with severity, affected components, remediation.
  - [x] AC-8: Workflow rules invoke security review at correct points when enabled.
  - [x] AC-9: Critical findings create decision records and block progression until resolved.
  - [x] AC-10: Template copies include security agent, command, and placeholder security-review.md.

## US-0029 — Knowledge Curation & Early Research
- Title: Structured knowledge curation with early web research during intake and architecture
- Summary: Integrate web research into early workflow phases so PO and Tech Lead agents have external references when making decisions. Enhance `/research` for structured, referenceable output. Persist knowledge in `docs/engineering/research.md` with entry IDs, timestamps, sources, and story linkage. Curator maintains the knowledge base. Subsumes Q0002 (research persistence).
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: PO agent searches the web for relevant context during `/intake` and persists findings as a research entry.
  - [x] AC-2: Tech Lead agent searches the web for technical references during `/architecture` and persists findings.
  - [x] AC-3: `/research` produces structured output: entry ID (R-xxxx), date, topic, query, sources, findings, linked story/decision IDs, confidence.
  - [x] AC-4: `docs/engineering/research.md` uses structured format — entries individually referenceable by ID.
  - [x] AC-5: `/intake` and `/architecture` command steps include explicit "research external context" step before evaluation/design.
  - [x] AC-6: Other agents can reference research entries by ID in their artifacts.
  - [x] AC-7: Curator agent includes research knowledge base in maintenance scope (prune stale, consolidate duplicates, flag outdated).
  - [x] AC-8: Scratchpad flag `EARLY_RESEARCH` (default: on) controls PO/TL web research; `/research` command always works manually.
  - [x] AC-9: Research entries include status field (current/outdated/superseded) for knowledge freshness.
  - [x] AC-10: Template copies updated with structured research.md, updated agents, updated commands.

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
- Status: DONE
- Acceptance:
  - [x] AC-1: Release guidance defines a mandatory "doc delta check" step before release notes are finalized.
  - [x] AC-2: If commands/flags changed in scope, and neither `README.md` nor `docs/engineering/runbook.md` reflects the change, release is blocked with explicit remediation guidance.
  - [x] AC-3: If only one of `README.md` or `docs/engineering/runbook.md` is updated for a command/flag change, release is blocked until parity is restored.
  - [x] AC-4: Non-command/flag changes do not trigger this gate (no false blocking for unrelated edits).
  - [x] AC-5: Gate output clearly lists each changed command/flag and where documentation evidence was found or missing.
  - [x] AC-6: README and runbook required sections for command/flag documentation are explicitly defined so checks are deterministic.
  - [x] AC-7: Release handoff format includes a pass/fail record for the doc delta gate.
  - [x] AC-8: Template parity: active and `template/` release/runbook/readme guidance are aligned for this gate behavior.
- Boundaries:
  - In scope: workflow/process guardrails for release readiness and artifact consistency.
  - Out of scope: implementing new product features or changing command semantics beyond documentation and gate behavior.

## US-0031 — Optional Documentation Pack (Design Concept, CRS, Technical Spec)
- Title: Add optional spec-pack generation/check flow controlled by configuration
- Summary: Introduce an optional workflow path that creates and validates a documentation pack containing Design Concept, CRS, and Technical Specification artifacts when enabled; zero overhead when disabled.
- Priority: P2
- Status: DONE
- Acceptance:
  - [x] AC-1: A single enable flag/config exists to control spec-pack behavior, defaulting to disabled.
  - [x] AC-2: When disabled, no extra required steps are added to intake/architecture/release flow.
  - [x] AC-3: When enabled, workflow creates/updates three artifacts with canonical names/locations: Design Concept, CRS, Technical Specification.
  - [x] AC-4: Each artifact has minimum required sections/fields defined so completeness is testable.
  - [x] AC-5: Validation checks report per-artifact completeness and block progression only when enabled and required sections are missing.
  - [x] AC-6: Traceability is defined from backlog story IDs to the generated spec-pack artifacts.
  - [x] AC-7: Guidance clarifies ownership (which role/phase maintains each document).
  - [x] AC-8: Template parity: active and `template/` command/rules/docs references for spec-pack mode remain aligned.
- Boundaries:
  - In scope: optional documentation-process capability and quality checks.
  - Out of scope: prescribing domain-specific content models beyond minimal required structure.

## US-0032 — Optional Feature User Guide Generation
- Title: Generate user-friendly instructions for each feature behind an explicit flag
- Summary: Add an optional workflow capability that produces and maintains end-user-facing instructions for each feature/story (what it does, how to use it, examples, limitations, troubleshooting) with deterministic structure and validation, while imposing zero overhead when disabled.
- Priority: P2
- Status: DONE
- Acceptance:
  - [x] AC-1: A dedicated config flag exists to enable/disable feature user guide generation, defaulting to disabled.
  - [x] AC-2: When the flag is disabled, intake/architecture/sprint/execute/qa/release flows add no required guide-generation steps and no new blocking checks.
  - [x] AC-3: When enabled, each accepted feature story gets a linked user guide artifact in a canonical location and naming format.
  - [x] AC-4: A minimum required guide schema is defined and testable (at least: feature purpose, prerequisites, usage steps, example, limitations, troubleshooting).
  - [x] AC-5: Validation reports completeness per guide and fails only when enabled and required sections are missing.
  - [x] AC-6: Guide traceability is explicit from story ID to user guide artifact, and referenced in handoff/release context.
  - [x] AC-7: Boundaries are enforced between user guides and technical spec-pack docs (`US-0031`) so duplicate ownership/content is avoided.
  - [x] AC-8: Template parity is maintained for active and `template/` docs/commands/rules references related to this optional mode.
- Boundaries:
  - In scope: optional user-facing documentation process, artifact structure, validation, and traceability.
  - Out of scope: replacing technical design docs (Design Concept/CRS/Technical Spec), and writing domain-specific product manuals beyond per-feature usage guidance.
 - Discovery notes:
   - Per-feature user guides should follow a consistent, testable schema (purpose, prerequisites, usage steps, example, limitations, troubleshooting) aligned with docs-as-code patterns.
   - Guides must live in a canonical, story-linked location and be updated alongside code so feature behavior and user instructions change atomically.
   - User-guide mode remains optional and flag-controlled, with zero additional required steps or gates when disabled.
   - User guides complement but do not replace spec-pack artifacts from US-0031; each serves a distinct audience and ownership model.

## US-0033 — Configurable Guided Intake Behavior
- Title: Let PO ask clarifying questions with options and research by default, with an off switch
- Summary: Formalize a guided intake mode where PO asks reasonable follow-up questions when scope is unclear, suggests options instead of prematurely deciding implementation, and performs intake-time web research. Add a single switch to disable this proactive behavior for teams that want low-touch intake.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: `/intake` guided mode asks targeted follow-up questions only when ambiguity blocks concrete acceptance criteria.
  - [x] AC-2: In guided mode, PO presents at least one viable option/alternative before proposing a recommendation.
  - [x] AC-3: Guided mode explicitly preserves user decision authority (PO recommends; user decides).
  - [x] AC-4: Guided mode includes PO web research step with persisted evidence in `docs/engineering/research.md` and linked story context.
  - [x] AC-5: A single scratchpad switch controls guided intake behavior (default: enabled).
  - [x] AC-6: When the switch is disabled, `/intake` adds zero proactive follow-up/options/research overhead and proceeds in low-touch mode unless user requests depth.
  - [x] AC-7: Low-touch mode still preserves baseline safety: duplicate/overlap check against backlog remains active.
  - [x] AC-8: `/intake` command and `po.mdc` clearly document both modes and mode-specific expectations.
  - [x] AC-9: Active and `template/` copies remain behaviorally aligned for the new switch.
- Boundaries:
  - In scope: intake interaction behavior, explicit user choice, and mode toggling.
  - Out of scope: changing downstream architecture/sprint execution semantics.

## US-0034 — Multi-Repo and Contract Compatibility Observability
- Title: Track module/API compatibility across repos and components
- Summary: Add an optional workflow capability that watches relevant modules, docs, and API contracts across one or more repositories, then reports compatibility risk and contract drift to engineering artifacts. This is process observability and validation, not runtime feature logic.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: A dedicated config toggle exists (for example `CROSS_REPO_OBSERVABILITY`), defaulting to disabled.
  - [x] AC-2: When disabled (default), `/intake`, `/architecture`, `/execute`, and `/qa` add no required extra steps or blocking checks.
  - [x] AC-3: When enabled, configuration supports an explicit source list of monitored repositories/modules/artifacts (at least repo path/URL, module ID, and contract/doc location).
  - [x] AC-4: Compatibility checks include at minimum: API signature compatibility, declared version/contract mismatch detection, and documentation/API description drift signals.
  - [x] AC-5: Findings are persisted in a canonical artifact (for example `docs/engineering/compatibility-report.md`) with severity, affected module(s), evidence, and recommended next action.
  - [x] AC-6: If enabled and critical compatibility breakage is detected, workflow raises a decision gate before release progression.
  - [x] AC-7: Reports are traceable to backlog story IDs and sprint/task context so QA/release can verify coverage.
  - [x] AC-8: Active and `template/` copies of commands/rules/docs remain aligned for this optional mode.
- Boundaries:
  - In scope: workflow-level compatibility visibility, artifact persistence, and gate policy.
  - Out of scope: implementing cross-repo CI orchestration engines or runtime service mesh behavior.

## US-0035 — Component-Scoped Execution Mode with Protection Guards
- Title: Execute workflow on selected component(s) without destabilizing others
- Summary: Add a component-scoped mode so teams can target one component in a multi-component repo while protecting unaffected components through scope-aware planning and verification rules. Defaults stay lightweight when mode is off.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: A dedicated scope control exists (for example `COMPONENT_SCOPE_MODE` plus `TARGET_COMPONENTS`), with mode default disabled.
  - [x] AC-2: When disabled (default), workflow behavior is unchanged and introduces zero required overhead.
  - [x] AC-3: When enabled, `/intake` and `/architecture` require explicit in-scope and out-of-scope component declaration in artifacts.
  - [x] AC-4: `/sprint-plan` and task artifacts require each task to declare target component(s) and expected impacted interfaces.
  - [x] AC-5: `/execute` guidance enforces scope-first execution (no intentional edits outside declared target components unless escalated and approved).
  - [x] AC-6: `/qa` includes unaffected-component protection checks (for example smoke/regression checks for declared non-target components) before completion.
  - [x] AC-7: If enabled and out-of-scope component impact is detected without prior approval, workflow triggers a decision gate.
  - [x] AC-8: Active and `template/` command/rule/docs guidance stays behaviorally aligned for component-scoped mode.
- Boundaries:
  - In scope: workflow scoping, artifact contracts, guardrails, and validation guidance.
  - Out of scope: monorepo build-system redesign or automatic dependency graph generation beyond declared scope metadata.

## US-0036 — Official Remote Config Template, Docs, and Fail-Fast Validation
- Title: Ship canonical `.cursor/remote.json` template with schema guidance and safe validation
- Summary: Add an official remote execution configuration artifact and supporting documentation so teams can use `REMOTE_EXECUTION=1` safely. Provide clear schema/field expectations, example targets, and validation behavior that fails fast on invalid config while keeping zero overhead when `REMOTE_EXECUTION=0`.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: Canonical `.cursor/remote.json` template exists in both active repo and `template/` with aligned defaults and comments/examples where appropriate.
  - [x] AC-2: Remote config schema is documented (required vs optional fields, data types, allowed values, path/host conventions).
  - [x] AC-3: Documentation includes at least two concrete example target configurations (for example local network host and remote VM/container endpoint) using safe placeholder values.
  - [x] AC-4: Validation guidance is defined to fail fast when `REMOTE_EXECUTION=1` and config is missing, malformed, or semantically invalid.
  - [x] AC-5: Validation output specifies actionable error messages (which field failed, expected format/range, and remediation hint).
  - [x] AC-6: When `REMOTE_EXECUTION=0` (default), workflow imposes zero required remote-config steps and no false-fail checks.
  - [x] AC-7: Security guidance explicitly prohibits committing secrets/tokens in `.cursor/remote.json` and provides approved secret-handling alternatives.
  - [x] AC-8: README and `docs/engineering/runbook.md` document remote setup, validation behavior, and mode-specific expectations (`REMOTE_EXECUTION` on/off).
  - [x] AC-9: Template parity is verified: active and `template/` copies of remote config references/docs/validation guidance are behaviorally aligned.
- Boundaries:
  - In scope: configuration template, schema/validation contract, docs/runbook guidance, and workflow-level safety expectations.
  - Out of scope: implementing new remote execution transport protocols or external secret-management infrastructure.

## US-0037 — Mid-Process `/auto` Continuation with Deterministic Resume Point
- Title: Continue full workflow from an explicit or resolved phase without manual phase triggers
- Summary: Users can pause mid-workflow, then run one command to continue full automation from the right phase through the remaining pipeline. Add explicit `start-from` support to `/auto`, deterministic resume-source resolution (`handoffs/resume_brief.md` first, `docs/engineering/state.md` fallback), and clear stop/log behavior while preserving safe defaults.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: `/auto` supports an explicit `start-from` phase input (canonical phase IDs) to begin orchestration mid-process.
  - [x] AC-2: When `start-from` is omitted, resume phase is resolved deterministically in this order: `handoffs/resume_brief.md` -> `docs/engineering/state.md` fallback.
  - [x] AC-3: If both resume sources are missing, stale, or conflicting, the command fails safely with actionable guidance instead of guessing.
  - [x] AC-4: A single `/auto` invocation from mid-process continues through all remaining phases (including execute/QA loop behavior when enabled) without requiring manual phase commands.
  - [x] AC-5: Existing stop conditions remain enforced (decision gate, missing critical input, pause request, loop max cycles); continuation does not bypass gates.
  - [x] AC-6: Continuation writes deterministic audit breadcrumbs to artifacts (at minimum: chosen start phase, source used, stop reason) so resume behavior is inspectable.
  - [x] AC-7: Default-safe behavior is preserved: manual/interactive teams are unaffected unless auto continuation mode is explicitly used.
  - [x] AC-8: `/pause`, `/resume`, and `/auto` guidance is behaviorally aligned around resume semantics to avoid contradictory flow instructions.
  - [x] AC-9: Active and `template/` command/rule/docs copies remain aligned for the continuation behavior.
- Boundaries:
  - In scope: workflow orchestration semantics, resume-source precedence, artifact logging, and command/rule/doc parity.
  - Out of scope: changing phase deliverables, bypassing decision gates, or adding runtime product features unrelated to workflow control.

## US-0038 — Phase-Triggered Sync Policy with Guarded Auto-Push
- Title: Configurable sync cadence after completed phases with QA-first safety defaults
- Summary: Add a configurable phase-triggered sync policy that controls when local check-in sync/push is attempted (`disabled`, `manual`, `by_phase`, `by_milestone`, custom phase list). Keep behavior safe-by-default: no automatic push before QA pass for feature work, and always run check-in tests before any push attempt.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: A canonical sync policy configuration exists and is documented (at minimum: `disabled`, `manual`, `by_phase`, `by_milestone`, `custom_phase_list`), with default set to a non-auto mode.
  - [x] AC-2: Policy evaluation runs only at phase-completion boundaries and determines whether a sync attempt is eligible at that boundary.
  - [x] AC-3: Mandatory pre-push checks always include `TEST_COMMAND`; push is blocked when tests fail, timeout, or are missing.
  - [x] AC-4: Optional checks (`LINT_COMMAND`, `TYPECHECK_COMMAND`, formatter/lint-fix) are honored when configured in runbook and reported clearly in sync output.
  - [x] AC-5: For feature work, automatic push before QA completion is forbidden; before QA pass, only manual user-invoked sync is allowed.
  - [x] AC-6: If QA produced blocking findings or unresolved critical issues, sync policy must not auto-push and must emit actionable remediation guidance.
  - [x] AC-7: Branch safety constraints are enforced for auto-sync (for example protected/default branch deny by default unless explicit opt-in allowlist is configured).
  - [x] AC-8: Sync operations produce deterministic evidence in artifacts/logs (phase, policy mode, checks run, pass/fail, push decision, reason code).
  - [x] AC-9: `scripts/validate-and-push.ps1` and `scripts/validate-and-push.sh` remain behaviorally aligned for mandatory test execution and gating semantics (template parity where applicable).
  - [x] AC-10: When sync policy is disabled/manual (default), workflow overhead is near zero and existing manual push behavior remains unchanged.
- Boundaries:
  - In scope: sync policy semantics, check gating contract, safety defaults, and artifact evidence.
  - Out of scope: adding new CI providers, changing runtime product behavior, or forcing one git branching strategy for all teams.

## US-0039 — Release Gate Tightening for Check-In Tests and QA/UAT Completion
- Title: Allow release only after mandatory check-in tests and QA/UAT readiness
- Summary: Tighten release readiness so `/release` proceeds only when check-in tests have passed and QA/UAT completion criteria are met. This complements phase sync policy by enforcing a hard final gate before release artifacts are finalized.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: `/release` includes an explicit mandatory gate that verifies latest check-in test result is passing (`TEST_COMMAND` baseline).
  - [x] AC-2: If check-in test evidence is missing, stale, or failing, release is blocked with deterministic fail reason and remediation steps.
  - [x] AC-3: `/release` requires QA completion evidence (no unresolved blocking findings in current sprint context) before proceeding.
  - [x] AC-4: Existing UAT completeness gate remains mandatory; release fails when UAT artifacts are placeholder, incomplete, or unresolved-fail state.
  - [x] AC-5: Gate ordering is deterministic: check-in test gate first, then QA gate, then UAT gate, then release-note/runbook updates.
  - [x] AC-6: Release output records per-gate pass/fail status and evidence pointers in handoff/state artifacts so QA and TL can audit decisions.
  - [x] AC-7: No release path may bypass these gates in default configuration; any override path (if allowed) requires explicit decision gate + documented rationale.
  - [x] AC-8: Active and `template/` release/qa/execute guidance remains behaviorally aligned for gate semantics (template parity AC).
  - [x] AC-9: Regression coverage includes positive and negative cases for each gate and for stale-evidence scenarios.
  - [x] AC-10: Safe default behavior is preserved for teams without optional lint/typecheck commands: release still requires test + QA/UAT evidence and does not falsely fail on blank optional runbook keys.
- Boundaries:
  - In scope: release readiness policy, gate order, evidence contract, and blocking behavior.
  - Out of scope: redefining sprint lifecycle, changing acceptance ownership, or replacing existing QA/UAT artifact formats.
- Discovery notes:
  - Mandatory gates: check-in test (TEST_COMMAND), QA completion (no unresolved blocking findings), UAT completeness (no placeholder/incomplete/fail state).
  - Deterministic order: test → QA → UAT → release-note/runbook; enforced and documented for auditability.
  - Evidence contract: per-gate pass/fail and evidence pointers recorded in handoff/state so decisions are auditable.
  - Bypass: none in default path; any override requires explicit decision gate + documented rationale.
  - Template parity: active and template release/qa/execute guidance aligned for gate semantics.

## US-0040 — Per-Sprint Release Notes and Release Queue Tracker
- Title: Prevent release-note overwrite and track unreleased vs released sprints
- Summary: Replace single-file release note behavior with per-sprint release note artifacts and add a canonical release queue tracker that records each sprint's release status (`unreleased`/`released`) with deterministic state updates.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: `/release` writes sprint-scoped notes to a canonical path (for example `handoffs/releases/Sxxxx-release-notes.md`) and must not overwrite notes from other sprints.
  - [x] AC-2: A canonical release queue artifact exists (for example `handoffs/release_queue.md` or `release_queue.json`) with at least sprint ID, status (`unreleased|released`), last-updated timestamp, and release-notes reference.
  - [x] AC-3: Queue update semantics are deterministic: entering release flow for a sprint creates/updates an `unreleased` entry; successful release finalization transitions only that sprint to `released`.
  - [x] AC-4: Default-safe behavior: if sprint identity cannot be resolved, release must not overwrite any existing release notes and must fail safely with remediation guidance.
  - [x] AC-5: Backfill/migration behavior is defined for existing `handoffs/release_notes.md`: preserve legacy file, attempt one-time migration to sprint-scoped file when sprint context is resolvable, otherwise record manual-migration guidance.
  - [x] AC-6: Existing workflows that read `handoffs/release_notes.md` remain backward-compatible (for example via pointer/latest summary behavior) without destructive data loss.
  - [x] AC-7: Release readiness/reporting surfaces unreleased sprint queue entries so pending releases are visible before finalization.
  - [x] AC-8: Release command/rules/docs define clear ownership and phase touchpoints for queue state transitions and note generation.
  - [x] AC-9: Template parity is maintained: active and `template/` copies of release guidance/artifacts are behaviorally aligned for per-sprint notes and queue tracking.
- Boundaries:
  - In scope: release artifact conventions, migration/backfill contract, queue status lifecycle, and workflow documentation/rules updates.
  - Out of scope: changing deployment runtime behavior, introducing external release-management services, or redefining QA/UAT evidence formats.

## US-0041 — End-to-End Lifecycle QA for `its-magic` Install/Upgrade/Clean
- Title: Add live lifecycle tests for install, update, backup, and cleanup safety
- Summary: Extend QA beyond static/template checks to run full end-to-end lifecycle validation of the actual `its-magic` command and platform installers. Cover fresh install, overwrite with backup, upgrade behavior, and clean-repo safety so regressions in real user flows are detected before release.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: Add deterministic E2E tests for fresh install (`missing` mode) validating required files and `.its-magic-version` creation.
  - [x] AC-2: Add E2E tests for overwrite + backup (`overwrite --backup`) validating backup structure, timestamped snapshot creation, and recoverability guidance.
  - [x] AC-3: Add E2E tests for upgrade flow (`upgrade`) validating framework-file refresh, user-data preservation, and new-file delivery.
  - [x] AC-4: Add E2E tests for cleanup flow (`--clean-repo`) validating only framework artifacts are removed while non-its-magic project files remain untouched.
  - [x] AC-5: Add negative-path tests (invalid mode/args, malformed target state, missing permissions) with fail-fast and actionable error output checks.
  - [x] AC-6: Cover CLI entrypoint path (`its-magic ...`) and direct installer path (`installer.ps1`/`installer.sh`) with behavior parity assertions.
  - [x] AC-7: Ensure OS/platform parity for lifecycle checks (PowerShell + shell paths locally, and CI jobs for npm/choco/brew smoke + lifecycle subset).
  - [x] AC-8: Ensure tests are isolated/idempotent (temp dirs only, cleanup on failure, no mutation of repo working files).
  - [x] AC-9: Document lifecycle QA matrix and expected pass/fail evidence in `README.md` and `docs/engineering/runbook.md`.
- Boundaries:
  - In scope: QA coverage expansion for installer/CLI lifecycle behavior and release confidence.
  - Out of scope: redesigning installer feature semantics or adding new install modes not already planned.

## US-0042 — Release Findings Artifact and Post-QA Issue Workflow
- Title: Standardize how release-step issues are documented, triaged, and handed back
- Summary: Define an official workflow for issues discovered after QA (for example during `/release` gates), including a dedicated findings artifact similar to QA findings, deterministic reason-code mapping, and clear handoff/ownership semantics.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: Canonical release-step findings artifact is defined (for example `sprints/Sxxxx/release-findings.md`) with required sections: gate status, blocking/non-blocking findings, reason codes, evidence refs, remediation.
  - [x] AC-2: `/release` guidance writes/updates release findings when a gate blocks and references deterministic reason codes.
  - [x] AC-3: Release-blocked scenarios produce a standard handoff path back to implementation (`handoffs/release_to_dev.md` or equivalent documented contract).
  - [x] AC-4: `docs/engineering/state.md` and queue artifacts remain synchronized with release findings status (`unreleased|blocked|released`) without contradictory records.
  - [x] AC-5: Decision-gate override path explicitly requires release findings evidence and rationale linkage (`DEC-xxxx` reference).
  - [x] AC-6: QA and release boundaries are clear: QA findings stay in `qa-findings.md`; post-QA release issues are recorded in release findings artifact.
  - [x] AC-7: Regression coverage includes at least one blocked release scenario verifying artifact creation/update and handoff behavior.
  - [x] AC-8: Active/template parity is maintained for command/docs/rules references of the release findings workflow.
- Boundaries:
  - In scope: process/workflow documentation, artifact contracts, handoff semantics, and deterministic evidence flow for post-QA release issues.
  - Out of scope: changing runtime deployment behavior or replacing existing QA/UAT artifact models.

## US-0043 — Backlog Reconciliation Gate for Released Sprints
- Title: Prevent drift between released sprint evidence and backlog story status
- Summary: Add a deterministic reconciliation contract so once a sprint reaches `released`, linked story status and acceptance checkmarks in `docs/product/backlog.md` are synchronized from canonical sprint/release evidence. Block or fail safely when contradictory states are detected.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: Define canonical evidence precedence for story completion reconciliation (at minimum: release queue status, sprint release notes, QA findings, UAT status, and release findings when present).
  - [x] AC-2: `/release` (or deterministic post-release boundary step) updates linked backlog story status to `DONE` when all mandatory evidence gates are PASS.
  - [x] AC-3: `/release` (or post-release step) reconciles acceptance checkbox state for the linked story based on completion evidence, not manual memory.
  - [x] AC-4: If sprint is `released` but backlog story is still `OPEN` or acceptance checkboxes are contradictory, workflow fails safely with explicit reason code and remediation guidance.
  - [x] AC-5: Reason code vocabulary includes a dedicated drift code (for example `BACKLOG_STATUS_DRIFT`) with deterministic evidence references.
  - [x] AC-6: Reconciliation mutates only the target story/story IDs linked to the target sprint and must not modify unrelated backlog entries.
  - [x] AC-7: Regression coverage includes at least one negative case (`released` sprint + stale backlog) and one positive case (automatic reconciliation to consistent state).
  - [x] AC-8: Active and `template/` command/rule/docs guidance remains behaviorally aligned for reconciliation semantics.
  - [x] AC-9: Readme/runbook documents the reconciliation invariant and where to inspect evidence when drift is detected.
  - [x] AC-10: Default-safe behavior is preserved for non-released stories/sprints (no premature `DONE` transitions before release gates pass).
- Boundaries:
  - In scope: backlog/sprint/release artifact consistency rules, fail-safe detection, reconciliation behavior, and regression tests.
  - Out of scope: redefining story acceptance ownership, replacing sprint lifecycle phases, or changing runtime feature behavior.

## US-0044 — Continuous `/auto` Backlog-Drain Mode with Fine-Tune Switches
- Title: Let `/auto` continue across planned stories until completion (bounded and safe)
- Summary: Extend `/auto` from single-story continuation to optional backlog-drain orchestration mode. When enabled, `/auto` should deterministically select next eligible OPEN story and continue through full workflow repeatedly until backlog target is reached, while preserving decision gates, stop conditions, and explicit operator controls.
- Priority: P1
- Status: DONE
- Acceptance:
  - [x] AC-1: A dedicated scratchpad switch enables/disables multi-story backlog-drain mode (default off, preserving current behavior).
  - [x] AC-2: Deterministic story selection policy is defined and documented (for example by priority, then backlog order), including tie behavior.
  - [x] AC-3: `/auto` can iterate story-by-story through full lifecycle (`discovery -> ... -> release -> refresh-context`) without manual re-invocation while mode is enabled.
  - [x] AC-4: Fine-tune switches exist for bounded execution (at minimum max stories per run and stop-on-blocking-story policy).
  - [x] AC-5: Decision gates remain mandatory and pause backlog-drain progression until user decision is recorded.
  - [x] AC-6: If one story blocks, deterministic behavior is configurable (`stop_immediately` vs `skip_and_continue`) and always recorded with reason codes.
  - [x] AC-7: Breadcrumb/state artifacts record per-story start/stop outcomes, selected policy settings, and final backlog-drain summary for auditability.
  - [x] AC-8: Existing execute↔qa auto loop controls continue to work within each story cycle and do not regress.
  - [x] AC-9: Active and `template/` command/rule/docs guidance remains behaviorally aligned for backlog-drain semantics.
  - [x] AC-10: Default-safe backward compatibility is preserved: with mode disabled, `/auto` behavior remains current checkpointed continuation.
- Boundaries:
  - In scope: process/workflow orchestration semantics, configuration switches, deterministic selection/stop behavior, and artifact evidence.
  - Out of scope: bypassing decision approvals, redefining story acceptance content, or runtime product feature logic changes.

## US-0045 — Canonical Story Status Source + Global Drift Guard
- Title: Make backlog the canonical status source and prevent cross-artifact story drift
- Summary: Define a deterministic workflow contract where `docs/product/backlog.md` is the canonical source for story `OPEN|DONE` status, and `docs/product/acceptance.md` plus `docs/engineering/state.md` are reconciled from canonical evidence. Include one-time normalization for already-drifted stories and fail-safe guardrails that block contradictory release progression.
- Priority: P1
- Status: DONE
- Discovery notes:
  - Canonical state owner: `docs/product/backlog.md` for story status.
  - Secondary/derived views: `docs/product/acceptance.md` checklist state and `docs/engineering/state.md` trace checkpoints.
  - Expected operator UX: deterministic mismatch report (story id, previous values, resolved values, evidence refs, remediation).
  - Safety boundary: normalization and reconciliation remain target-scoped and non-destructive for unrelated stories.
- Acceptance:
  - [x] AC-1: Define and document canonical ownership: backlog story status is authoritative; acceptance/state are derived or reconciled views.
  - [x] AC-2: Add deterministic reconciliation rules for `backlog.md` <-> `acceptance.md` <-> `state.md` with explicit precedence and mutation scope.
  - [x] AC-3: Add a one-time normalization procedure that repairs existing mismatches for historically completed stories (for example OPEN in backlog but DONE/PASS evidence exists).
  - [x] AC-4: Ensure normalization emits an auditable report of changed stories, prior values, new values, and evidence references.
  - [x] AC-5: Add fail-safe reason code(s) for contradictory status states detected at release/reconciliation boundaries, with actionable remediation guidance.
  - [x] AC-6: Guardrails must be target-scoped and non-destructive to unrelated stories/sprints; no broad blind rewrites.
  - [x] AC-7: `/auto` and `/execute` documentation explicitly states they do not infer implementation readiness from non-canonical status artifacts.
  - [x] AC-8: `/sprint-plan` guidance clarifies planning source and expected behavior for multiple OPEN backlog items versus sprint sizing limits.
  - [x] AC-9: Add regression coverage for (a) existing-drift normalization pass and (b) post-normalization drift prevention on subsequent workflow runs.
  - [x] AC-10: Maintain active/template parity for all command/docs/rules updates tied to this contract.
- Boundaries:
  - In scope: workflow-state contracts, normalization/reconciliation behavior, drift detection, command guidance, and regression tests.
  - Out of scope: changing runtime product features, bypassing decision gates, or removing sprint sizing policies.

## US-0046 — Explicit `/sprint-plan --bulk` Mode
- Title: Plan multiple OPEN backlog stories into bounded sprint sets in one run
- Summary: Add an explicit bulk planning mode for `/sprint-plan` so teams can intentionally generate multiple sprint plans from eligible OPEN backlog stories in one invocation. Keep deterministic grouping/splitting rules, bounded limits, and default-safe single-scope behavior when bulk mode is not enabled.
- Priority: P1
- Status: DONE
- Discovery notes:
  - Explicit operator intent is required for bulk planning activation; default path remains current single-scope planning behavior.
  - Selection/grouping model should be deterministic and inspectable (priority + backlog order, then documented split/group rule).
  - Planning completeness must remain identical to non-bulk output quality for every generated sprint artifact set.
  - Bulk planning should optimize throughput without relaxing `SPRINT_MAX_TASKS` and `SPRINT_AUTO_SPLIT` safety rules.
- Acceptance:
  - [x] AC-1: `/sprint-plan` defines an explicit bulk mode trigger (flag/argument or equivalent), defaulting to current non-bulk behavior.
  - [x] AC-2: Bulk mode uses deterministic story selection policy (at minimum priority + backlog order) and documents tie handling.
  - [x] AC-3: Bulk mode applies bounded limits (for example max stories and/or max generated sprints per run) with explicit stop reason output.
  - [x] AC-4: Sprint sizing constraints (`SPRINT_MAX_TASKS`, `SPRINT_AUTO_SPLIT`) remain enforced per generated sprint and never bypassed.
  - [x] AC-5: Grouping/splitting contract is documented (single-story sprint vs multi-story sprint) with deterministic decision criteria.
  - [x] AC-6: Generated planning artifacts remain complete for each sprint (`sprint.md`, `tasks.md`, `progress.md`, UAT placeholders, `plan-verify` readiness).
  - [x] AC-7: Traceability index/state updates remain deterministic and non-duplicative when bulk mode creates multiple sprint entries.
  - [x] AC-8: Decision gates and missing-input stops are preserved; bulk planning must fail safe on ambiguous or incomplete acceptance criteria.
  - [x] AC-9: Regression coverage includes positive and negative bulk-planning cases, including boundary-limit behavior.
  - [x] AC-10: Active and `template/` command/rule/docs guidance stays behaviorally aligned for bulk planning semantics.
- Boundaries:
  - In scope: planning orchestration semantics, deterministic selection/grouping/splitting, bounded controls, and artifact completeness.
  - Out of scope: auto-implementation execution of planned sprints, runtime feature behavior changes, or bypassing sprint sizing policies.

## US-0047 — Explicit Bulk Execute Orchestration Mode
- Title: Execute planned sprints/stories continuously with fresh agent contexts and bounded safety controls
- Summary: Add an explicit bulk execution mode that runs planned work sprint-by-sprint (or story-by-story) with mandatory fresh subagent contexts at fine granularity, execute↔QA loop behavior, and deterministic stop/skip controls so users can avoid manual command chaining.
- Priority: P1
- Status: DONE
- Discovery notes:
  - Bulk execution should be explicit-mode only; existing non-bulk behavior remains default-safe.
  - Isolation contract remains strict in bulk mode: fresh context per phase and per execute↔QA loop cycle.
  - Team mode requires member-scoped execution (`TEAM_MEMBER` + `ACTIVE_TASK_IDS`) so out-of-scope tasks are never executed.
  - Bounded controls and reason codes are required for explainability (max items, block/skip policy, stop reason, resume point).
- Acceptance:
  - [x] AC-1: An explicit bulk execute mode is defined (new command or explicit mode argument), defaulting to current non-bulk behavior when disabled.
  - [x] AC-2: Bulk execution uses deterministic work-item selection policy and records selection source/evidence in state breadcrumbs, including team-context inputs (`TEAM_MODE`, `TEAM_MEMBER`, `ACTIVE_TASK_IDS`) when enabled.
  - [x] AC-3: Fresh subagent isolation is mandatory per phase and per execute↔QA cycle for each sprint/story handled in bulk mode.
  - [x] AC-4: Execute↔QA loop controls remain bounded (`AUTO_IMPLEMENTATION_LOOP`, max cycle controls) and are enforced per sprint/story iteration.
  - [x] AC-5: Bounded run controls exist (for example max sprints/stories per run, stop-vs-skip on blocked item) with explicit reason-code output.
  - [x] AC-6: Decision gates remain mandatory and pause bulk execution progression until user decision is recorded.
  - [x] AC-7: Resume semantics are deterministic for interrupted bulk runs (checkpoint source, next item, stop reason) and are documented.
  - [x] AC-8: In team mode, bulk execution must not run tasks outside the current member context (`TEAM_MEMBER` + `ACTIVE_TASK_IDS`); out-of-scope tasks are deterministically skipped/blocked with explicit reason codes and no writes.
  - [x] AC-9: Regression coverage includes positive progression, blocked-item policy behavior, and fresh-context isolation expectations.
  - [x] AC-10: Active and `template/` command/rule/docs guidance stays behaviorally aligned for bulk execution semantics.
- Boundaries:
  - In scope: execution orchestration semantics, isolation guarantees, bounded controls, and deterministic auditability.
  - Out of scope: changing runtime product feature logic, bypassing release/decision gates, or replacing artifact-first handoff model.

## US-0048 — Enforced Per-Phase Subagent Isolation with Audit Gate
- Title: Enforce fresh subagent isolation for every workflow phase with fail-closed auditability
- Summary: Close the execution-compliance gap by making phase isolation a hard-enforced contract (not guidance), requiring auditable per-phase isolation evidence and blocking progression/release when isolation proof is missing or violated.
- Priority: P1
- Status: DONE
- Discovery notes:
  - Current policy text already mandates phase isolation, but operator execution can still drift without deterministic enforcement.
  - The guard must fail closed on missing or contradictory isolation evidence.
  - Enforcement should preserve default workflow behavior while making violations explicit and traceable.
  - Operator expectation: on isolation failure, operators get explicit diagnostics (reason code, phase, evidence ref, remediation) — no silent block or continuation.
  - Research scope: isolation evidence schema, canonical evidence artifact locations, verify/release gate integration, reason-code taxonomy, and resume provenance; out of scope: runtime product features, external orchestration platform migration.
- Acceptance:
  - [x] AC-1: `/auto` enforces orchestrator-only behavior and must fail if phase work is executed without spawning a fresh subagent context.
  - [x] AC-2: Each phase transition writes mandatory isolation evidence (phase id, role, fresh-context marker, timestamp, evidence ref) to canonical artifacts.
  - [x] AC-3: `/execute` and `/qa` loop runs enforce fresh-context-per-cycle semantics with deterministic evidence fields.
  - [x] AC-4: Missing/invalid isolation evidence triggers deterministic fail-safe reason code(s) and stops progression.
  - [x] AC-5: `/verify-work` and `/release` include an isolation-compliance gate that blocks finalization on unresolved isolation violations.
  - [x] AC-6: Isolation evidence schema is documented in runbook and reflected in command contracts (`/auto`, `/execute`, `/qa`, `/release`).
  - [x] AC-7: Reason-code taxonomy includes explicit isolation violations/remediation guidance (for example `PHASE_CONTEXT_ISOLATION_MISSING`, `PHASE_CONTEXT_ISOLATION_VIOLATION`).
  - [x] AC-8: Regression coverage includes positive and negative isolation cases (missing evidence, reused context, invalid role/phase mapping).
  - [x] AC-9: Resume behavior remains deterministic; isolation evidence must survive pause/resume boundaries without ambiguity.
  - [x] AC-10: Active and `template/` command/rule/docs guidance remains behaviorally aligned for isolation enforcement semantics.
- Boundaries:
  - In scope: workflow contract enforcement, evidence schema, gates, reason codes, and regression coverage.
  - Out of scope: runtime product feature behavior changes or external orchestration platform migration.

## US-0049 — Legacy DONE-Story Acceptance/Traceability Backfill Guard
- Title: Guard and one-time backfill for backlog DONE vs acceptance/traceability drift
- Summary: Add deterministic detection and bounded repair for legacy stories where canonical backlog shows DONE but acceptance checkmarks or traceability/release artifacts disagree. Include optional one-time backfill mode, ongoing guard at reconciliation/release boundaries, explicit audit report entries and reason codes, and template parity plus regression coverage expectations.
- Priority: P1
- Status: DONE
- Notes: Context: US-0017 and US-0030 were DONE in backlog but unchecked in acceptance and not clearly represented in traceability/release artifacts. Per R-0023. Released S0028 2026-03-02.
- Discovery notes:
  - Detection rule: legacy drift = backlog status DONE and (acceptance item unchecked OR traceability index/state lacks entry OR release artifacts lack clear representation for that story).
  - One-time backfill: explicit trigger runs detection and repair once; emits audit report; idempotent when no drift. Ongoing guard: at release/reconciliation (or dedicated check) detects drift and either blocks with reason code or performs target-scoped repair with audit append.
  - Audit report: canonical artifact (e.g. docs/engineering/legacy-drift-audit.md) with story ID, prior acceptance/traceability state, resolved state(s), reason code, evidence ref.
  - Reason codes: BACKLOG_DONE_ACCEPTANCE_UNCHECKED, BACKLOG_DONE_TRACEABILITY_MISSING, BACKLOG_DONE_RELEASE_ARTIFACT_MISSING (or equivalent) with remediation per code.
  - Boundaries: target-scoped repair only; no change to canonical status ownership (US-0045) or broad reconciliation semantics (US-0043). Template parity and regression coverage required.
- Acceptance:
  - [x] AC-1: Define and document detection rule: story is "legacy drift" when backlog status is DONE and (acceptance checklist item for that story is unchecked OR traceability index/state lacks entry OR release artifacts lack clear representation for that story).
  - [x] AC-2: Bounded target-scoped repair: normalization mutates only stories that match the legacy-drift rule; no broad destructive rewrite of unrelated backlog/acceptance/state/release artifacts.
  - [x] AC-3: Audit report format is defined with required fields: story ID, prior acceptance state, prior traceability state, resolved state(s), reason code, evidence reference; report written to a canonical artifact (e.g. `docs/engineering/legacy-drift-audit.md` or equivalent).
  - [x] AC-4: Reason-code vocabulary includes at least: `BACKLOG_DONE_ACCEPTANCE_UNCHECKED`, `BACKLOG_DONE_TRACEABILITY_MISSING`, `BACKLOG_DONE_RELEASE_ARTIFACT_MISSING` (or equivalent), with remediation guidance per code.
  - [x] AC-5: Optional one-time backfill mode: explicit trigger (e.g. command or flag) runs detection and repair once for all current legacy-drift stories and emits the audit report; idempotent and safe when no drift exists.
  - [x] AC-6: Ongoing guard: at release or reconciliation boundaries (or dedicated check), workflow detects legacy drift and either blocks with reason code and remediation or performs target-scoped repair with audit append; behavior is documented and deterministic.
  - [x] AC-7: Template parity: active and `template/` command/rule/docs guidance for backfill guard, audit report location, and reason codes remain behaviorally aligned.
  - [x] AC-8: Regression coverage includes at least: (a) one-time backfill run with no drift (no changes, report empty or "no drift"), (b) one-time backfill run with one legacy-drift story (repair applied, audit entry created), (c) ongoing guard blocks or repairs when drift is present and reports reason code.
- Boundaries:
  - In scope: detection rule, target-scoped repair, audit report schema, reason codes, one-time backfill and ongoing guard behavior, template parity, regression tests.
  - Out of scope: changing canonical status ownership (US-0045), broad reconciliation semantics (US-0043), or runtime product feature behavior.

## US-0050 — Clean Install Hygiene and Complete Clean-Repo Coverage
- Title: Ensure fresh installs are history-free and cleanup removes all framework-owned artifacts
- Summary: Eliminate seeded historical data and inconsistent cleanup behavior by expanding `--clean-repo` coverage, neutralizing starter artifacts, and adding regression tests so first-time installs start clean and deterministic.
- Priority: P1
- Status: DONE
- Discovery notes:
  - `--clean-repo` currently leaves framework-owned files in some installs (for example workflow scripts, workflow CI files, user-guide docs, and version marker), creating partial cleanup states.
  - Some starter engineering artifacts include historical seeded rows or cross-references that can look like imported project memory in fresh repos.
  - A hardcoded per-script cleanup list is drift-prone; ownership-based manifest cleanup (or equivalent single source of truth) is safer across PS1/SH/PY installers.
  - Fresh-install trust requires explicit regression coverage for install -> clean -> reinstall cycles.
- Acceptance:
  - [x] AC-1: `--clean-repo` removes all installer-managed workflow artifacts deterministically, including `.cursor`, `docs/product`, `docs/engineering`, `docs/user-guides`, `sprints`, `handoffs`, `decisions`, `.github/workflows`, `scripts/validate-and-push.*`, and `.its-magic-version` (or an equivalent ownership-complete set).
  - [x] AC-2: Cleanup ownership is defined once (manifest/source-of-truth) and consumed consistently by all installer implementations (`installer.ps1`, `installer.sh`, `installer.py`) to prevent path-list drift.
  - [x] AC-3: Cleanup remains non-destructive for non-framework project files; safety contract is explicit and tested.
  - [x] AC-4: Template starter artifacts under `template/docs/engineering/*` remove historical seeded operational data; placeholders are neutral and suitable for new repos.
  - [x] AC-5: Starter docs avoid hardcoded cross-repo references to specific runtime IDs (for example `DEC-0011`) unless matching baseline records are intentionally shipped and documented.
  - [x] AC-6: Fresh install in an empty repo with `--mode missing` yields clean baseline artifacts (no preloaded story/decision history rows beyond neutral placeholders).
  - [x] AC-7: Upgrade behavior from US-0018 remains intact (framework updates + user-data preservation), with no regressions from hygiene changes.
  - [x] AC-8: Regression tests cover fresh install, clean-repo, reinstall, and parity across installer entry points; tests assert zero preloaded history and complete cleanup.
  - [x] AC-9: Active and `template/` copies stay behaviorally aligned for install/clean contracts and starter artifact expectations.
- Boundaries:
  - In scope: installer cleanup coverage, starter artifact hygiene, ID-reference neutralization policy, and regression coverage.
  - Out of scope: runtime product feature logic, release-process redesign, or removing artifact-first workflow.

## US-0051 — Intelligent Intake Decomposition and Risk-Aware PO Questioning
- Title: Split broad intake into multiple stories and ask more when scope/risk is high
- Summary: Improve intake quality by decomposing broad ideas into multiple focused user stories with explicit split rationale, and by making PO questioning adaptive to breadth/risk/unknowns rather than ambiguity-only triggers.
- Priority: P1
- Status: DONE
- Discovery notes:
  - Current intake persistence tends to produce one large story with many ACs for broad requests.
  - Current guided questioning behavior is primarily ambiguity-triggered; broad but superficially concrete requests can receive too few clarifying questions.
  - Story splitting should use vertical-slice and workflow-step heuristics to keep stories testable and sprint-friendly.
  - Adaptive questioning should preserve low-touch mode while raising intake depth when change impact/risk is high.
- Acceptance:
  - [x] AC-1: `/intake` can propose multi-story decomposition when intake breadth exceeds defined splitting heuristics (scope size, feature count, risk surface, or workflow-step complexity).
  - [x] AC-2: Generated stories are independently valuable and testable (vertical-slice oriented), not technical-layer-only fragments.
  - [x] AC-3: Split rationale is persisted (why split, split axes used, and boundaries between generated stories).
  - [x] AC-4: User decision authority is explicit: user can accept, merge, or adjust proposed split before final persistence.
  - [x] AC-5: Small/narrow intake remains single-story by default (no forced over-splitting).
  - [x] AC-6: Guided questioning adapts to scope/risk/unknowns; high-impact intake triggers additional targeted questions even when baseline acceptance appears concrete.
  - [x] AC-7: Adaptive questioning remains concise and bounded; it does not create unstructured interview loops.
  - [x] AC-8: `INTAKE_GUIDED_MODE=0` low-touch behavior remains available and keeps minimal overhead, while duplicate/overlap safety stays mandatory.
  - [x] AC-9: Intake artifacts (`backlog.md`, `acceptance.md`, `handoffs/po_to_tl.md`) include decomposition and questioning evidence for traceability.
  - [x] AC-10: Active and `template/` intake/PO guidance plus regression checks stay aligned for decomposition + adaptive-question semantics.
- Boundaries:
  - In scope: intake decomposition logic, guided-question policy, persistence contracts, and parity/testing.
  - Out of scope: downstream execution/release semantics or runtime product feature behavior.

## US-0052 — Optional Fresh-Project ID Namespace Bootstrap
- Title: Allow fresh projects to start IDs at US-0001 and DEC-0001
- Summary: Add an optional bootstrap mode so new repositories without existing history can begin story/decision/research numbering from 0001, while preserving current highest-ID continuation behavior for existing repos.
- Priority: P2
- Status: DONE
- Discovery notes:
  - Teams expect first intake in a fresh project to start from `US-0001` and `DEC-0001`.
  - Existing repos must remain backward-compatible and continue highest-existing-ID behavior to avoid collisions.
  - Bootstrap should be explicit/opt-in and deterministic; no silent renumbering of existing artifacts.
- Acceptance:
  - [x] AC-1: A documented optional bootstrap control exists (flag/config/command) to initialize ID namespaces for fresh projects.
  - [x] AC-2: When bootstrap mode is enabled and no prior IDs exist, first generated IDs start at `US-0001`, `DEC-0001`, and `R-0001`.
  - [x] AC-3: When existing IDs are present, generation continues from highest existing ID; bootstrap mode does not rewrite historical IDs.
  - [x] AC-4: Freshness detection is deterministic and auditable (clear criteria for "new project" eligibility).
  - [x] AC-5: ID generation remains collision-safe across stories, decisions, and research artifacts in normal sequential workflow.
  - [x] AC-6: Operator guidance documents bootstrap behavior, constraints, and migration caveats in README/runbook/command help.
  - [x] AC-7: Regression tests cover fresh bootstrap path, non-fresh continuation path, and mixed-artifact edge cases.
  - [x] AC-8: Active and `template/` contracts remain aligned for namespace-bootstrap behavior.
- Boundaries:
  - In scope: ID bootstrap controls, deterministic detection rules, compatibility behavior, and documentation/tests.
  - Out of scope: retroactive renumbering/migration of existing project histories.

## US-0053 — Context Compaction and Tiered Token-Cost Optimization Mode
- Title: Add lean/balanced/full token profile and compact active memory surfaces
- Summary: Reduce recurring token usage by introducing a tiered token profile control and by compacting high-traffic context artifacts (`state.md`, `decisions.md`, and `/ask` read policy) while preserving release/QA/UAT safety gates and traceability.
- Priority: P1
- Status: DONE
- Discovery notes:
  - Current artifact-first memory provides strong auditability, but high-traffic files (especially `docs/engineering/state.md`) have grown large and are repeatedly queried.
  - `/ask` currently allows broad context reads; many operator questions only require recent checkpoints and targeted story sections.
  - User explicitly requested a tiered token-saver approach that minimizes feature loss by disabling only lower-priority overhead defaults.
  - Decomposition evaluator outcome: single-story recommended for this intake because all requested changes share one operational objective (token-cost reduction with safety invariants), have tightly coupled acceptance boundaries, and can be validated in one policy/test pass.
  - User authority evidence: user accepted this intake direction and requested execution as one intake item with tiered mode included.
  - Discovery validation: tiered profile control should be operator-simple (`lean|balanced|full`) with deterministic profile mapping and explicit per-flag override precedence.
  - Discovery validation: apply progressive context retrieval for `/ask` (targeted sections first; widen only when unresolved) and hot-vs-archive compaction for `state.md`/`decisions.md`.
  - Discovery references captured in `docs/product/vision.md` and `R-0026` (prompt caching + progressive context patterns).
- Acceptance:
  - [x] AC-1: Add documented tiered token profile control (for example `TOKEN_PROFILE=lean|balanced|full`) with deterministic default behavior and explicit mapping to underlying scratchpad switches.
  - [x] AC-2: Lean profile reduces overhead by default (looping/research/automation intensity and optional non-critical modes) without changing mandatory quality gates (`/qa`, `/verify-work`, `/release` chain).
  - [x] AC-3: Balanced/full profiles preserve current capabilities with explicit operator override precedence (manual flag values can override profile defaults where documented).
  - [x] AC-4: `docs/engineering/state.md` gains a deterministic hot-vs-archive strategy (active compact section + archived historical packs) so active reads stay bounded.
  - [x] AC-5: `docs/engineering/decisions.md` is compacted to a current context index with bounded summaries and canonical links to full `decisions/DEC-xxxx.md` records.
  - [x] AC-6: `/ask` contract is updated to a narrow-read policy (question-scoped retrieval, targeted sections first, expand only when unresolved) with zero write side effects preserved.
  - [x] AC-7: Active and `template/` command/agent/runbook/README/scratchpad contracts remain aligned for token-profile and compaction semantics.
  - [x] AC-8: Regression checks cover profile mapping behavior, guardrail invariants (mandatory gates unchanged), and compact-context policy/parity assertions.
  - [x] AC-9: Operator guidance documents tradeoffs and recommended usage for lean/balanced/full profiles, including when to temporarily escalate from lean to full.
  - [x] AC-10: Existing story/decision/research ID semantics and release queue/history integrity remain unchanged (no destructive history rewrite).
- Boundaries:
  - In scope: token-profile control, context compaction policy/contracts, `/ask` retrieval policy, and parity/regression updates.
  - Out of scope: removing mandatory release safety gates, changing canonical story-status ownership, or deleting historical evidence artifacts.

## US-0054 — Configurable Multi-Target Release Publish with Confirmation Gate
- Title: Add configurable release targets including generic/SSH with operator-confirmed publish
- Summary: Enable optional post-release publishing through configurable targets so different projects can publish to npm/choco/brew, git-only, docker, cloud providers, or custom SSH destinations using a safe confirmation step before execution.
- Priority: P1
- Status: DONE
- Discovery notes:
  - Current framework finalizes workflow release artifacts, but downstream publish destinations vary across users and repositories.
  - User requested adjustable target configuration, including generic/custom servers and SSH-based destinations.
  - User requested "half-automatic" behavior where the agent asks for confirmation before publish actions.
  - Decomposition evaluator outcome: single-story recommended because target configuration schema, confirmation flow, and publish execution safety are tightly coupled and should be validated in one integrated contract.
  - User authority evidence: user explicitly approved taking this as intake with configurable custom/SSH support.
- Acceptance:
  - [x] AC-1: Add a documented configurable publish-target contract (for example in runbook/config) supporting multiple target entries with deterministic schema validation.
  - [x] AC-2: Target contract supports built-in types (at minimum: npm, choco, brew, git, docker, cloud) plus a generic custom-command target type.
  - [x] AC-3: Target contract supports SSH-based publish/deploy targets (host/port/user/auth reference/remote command) without requiring hardcoded provider logic.
  - [x] AC-4: Publish flow provides operator confirmation gate by default (half-automatic mode), requiring explicit approval before executing selected targets.
  - [x] AC-5: Operator can select one or multiple configured targets per publish run with deterministic ordering and clear skip behavior for disabled targets.
  - [x] AC-6: Missing/invalid target configuration fails fast with actionable diagnostics and no partial publish side effects.
  - [x] AC-7: Secret handling for target credentials/tokens/keys is env-reference based (no inline secret literals in committed config).
  - [x] AC-8: Active and `template/` contracts remain aligned for target schema, confirmation semantics, and execution guidance.
  - [x] AC-9: Regression tests cover target-schema validation, confirmation gate behavior, SSH/custom-target handling, and deterministic reason codes.
  - [x] AC-10: Existing mandatory quality gates and release artifact finalization behavior remain unchanged when publish targets are disabled or not selected.
- Boundaries:
  - In scope: configurable publish-target schema, confirmation gate behavior, target selection/execution policy, SSH/custom support, documentation and parity tests.
  - Out of scope: replacing provider CLIs, forcing one hosting platform, or embedding secret values directly in repo artifacts.

## US-0055 — Deterministic Status Reconciliation Command
- Title: Add deterministic command to detect and reconcile backlog/acceptance/state/resume drift
- Summary: Add a dedicated reconciliation command that detects status inconsistencies (for example DONE stories with unchecked ACs or acceptance drift), applies deterministic repair to canonical/derived artifacts, and prepares resume metadata so `/auto` can continue from the correct next OPEN story and phase.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User observed post-release drift where canonical story status was DONE but acceptance/AC checkboxes remained unchecked in historical sections.
  - Existing commands (`/memory-audit`, `/refresh-context`, `/release`) cover detection, compaction, and target-sprint reconciliation, but not a dedicated deterministic cross-artifact repair pass.
  - User requested a command to "check and clean chaos" and restore a reliable continuation baseline for `/auto`.
  - Decomposition evaluator outcome: single-story recommended because detection rules, deterministic repair, and resume orchestration are tightly coupled and should be validated in one contract.
  - User authority evidence: user explicitly requested taking this as intake.
- Acceptance:
  - [x] AC-1: Add a documented reconciliation command (for example `/status-reconcile`) with deterministic read/repair steps for status artifacts.
  - [x] AC-2: Command detects contradictions across canonical/derived status surfaces at minimum for: backlog story status, backlog AC checkboxes, acceptance checklist rows, and resume intent metadata.
  - [x] AC-3: Canonical ownership is preserved (`docs/product/backlog.md` status is source of truth); derived artifacts are reconciled to canonical status unless explicit release evidence indicates canonical drift.
  - [x] AC-4: DONE stories with unchecked ACs are deterministically normalized with explicit audit evidence (changed story IDs, prior values, resolved values, timestamp).
  - [x] AC-5: Acceptance checklist (`docs/product/acceptance.md`) is reconciled to canonical backlog status for affected stories with target-scoped mutation semantics.
  - [x] AC-6: `handoffs/resume_brief.md` is updated deterministically to the next eligible OPEN story and correct intended phase for safe `/auto` continuation.
  - [x] AC-7: Reconciliation writes structured evidence to canonical audit artifact(s) and appends a state checkpoint with reason codes/remediation when blocked.
  - [x] AC-8: Deterministic reason-code contract exists for conflict/blocked paths (for example canonical conflict, ambiguous next phase, unresolved release evidence).
  - [x] AC-9: Regression tests cover normalization paths (DONE+unchecked, acceptance drift, resume drift, no-op clean state) and reason-code behavior.
  - [x] AC-10: Active and `template/` command/runbook/README contracts remain aligned for reconciliation semantics and guardrails.
- Boundaries:
  - In scope: workflow/process reconciliation of status artifacts and deterministic continuation readiness.
  - Out of scope: changing feature behavior, rewriting unrelated historical narratives, or bypassing mandatory release-quality gates.

## US-0056 — Strict Runtime Proof for Per-Phase Subagent Isolation
- Title: Enforce runtime-attested per-phase subagent isolation with fail-closed auto gates
- Summary: Add strict runtime proof so `/auto` cannot claim per-phase isolation based only on artifact markers. Each phase must carry unique runtime attestation evidence (for example per-phase execution IDs) and `/auto` must fail closed if attestation is missing, reused, stale, or contradictory.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User observed that recent `/auto` progression appeared in one visible chat despite isolation evidence rows.
  - Existing US-0048/DEC-0029 contract focuses on evidence fields in artifacts, but does not guarantee strong runtime attestation that each phase used a distinct fresh subagent execution.
  - User explicitly requested strict proof.
  - Decomposition evaluator outcome: single-story recommended because runtime attestation schema, phase-gate enforcement, and resume behavior are tightly coupled and should be validated in one integrated contract.
  - User authority evidence: user explicitly requested this as intake.
  - Discovery refinement: strict-proof boundary requires runtime attestation tuple with uniqueness/freshness checks and deterministic linkage to checkpoint evidence.
  - Research reference: `R-0034`; architecture decision gate opened at `DEC-0038`.
  - Decision update: `DEC-0038` approved; story is ready for `/sprint-plan`.
- Acceptance:
  - [x] AC-1: Define and document a strict runtime attestation contract for per-phase execution (beyond artifact-only markers), including required unique proof fields per phase run.
  - [x] AC-2: `/auto` requires runtime attestation evidence for each completed phase and fails closed when missing/invalid/reused/stale.
  - [x] AC-3: Attestation evidence is linked to canonical state checkpoints with deterministic mapping (phase, role, timestamp, evidence ref, runtime proof id).
  - [x] AC-4: Add deterministic reason codes for strict-proof failures (for example attestation missing, reused proof id, ambiguous proof linkage, stale proof).
  - [x] AC-5: Resume and pause contracts include strict-proof provenance so continuation cannot silently proceed after unverifiable phase boundaries.
  - [x] AC-6: Release/isolation gate semantics consume strict runtime attestation in addition to existing isolation evidence fields.
  - [x] AC-7: Reconciliation/backfill guidance is provided for legacy runs lacking strict attestation without rewriting unrelated history.
  - [x] AC-8: Operator guidance explains how to inspect strict-proof evidence and diagnose fail-closed outcomes.
  - [x] AC-9: Regression tests cover pass/fail paths for strict-proof enforcement, including reused/missing proof IDs and pause/resume continuity.
  - [x] AC-10: Active and `template/` contracts stay aligned for strict-proof semantics across command, runbook, README, and rules.
- Boundaries:
  - In scope: workflow orchestration proof/attestation contracts and fail-closed enforcement.
  - Out of scope: product runtime feature changes or external orchestration platform migration.

## US-0057 — Upgrade-Safe Scratchpad Example Refresh and Parity
- Title: Ensure scratchpad local example is reliably refreshed on upgrade without overwriting user scratchpad
- Summary: Improve installer upgrade behavior so `.cursor/scratchpad.local.example.md` is consistently refreshed with newest options and guidance, while preserving user-owned scratchpad files. Ensure parity across PS1/sh/py installers and clear diagnostics when example/user surfaces differ.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User reports that `its-magic --mode upgrade` can leave `scratchpad.local.example` with fewer/newly missing options while related options already exist in user scratchpad.
  - Existing upgrade contracts (US-0018/US-0050) cover framework vs user-data boundaries broadly, but this issue indicates drift risk on the scratchpad example/user interplay.
  - Decomposition evaluator outcome: single-story recommended because installer ownership, upgrade parity, and scratchpad diagnostics are tightly coupled and should be validated together.
  - User authority evidence: user explicitly requested this as intake.
  - Intake research reference: `R-0032`.
  - Decision update: `DEC-0039` accepted (ownership + upgrade parity contract).
- Acceptance:
  - [x] AC-1: Define deterministic ownership/upgrade policy for `.cursor/scratchpad.local.example.md` and related scratchpad surfaces (framework-owned vs user-owned).
  - [x] AC-2: `--mode upgrade` refreshes framework-owned scratchpad example content to latest contract without overwriting user-owned scratchpad values.
  - [x] AC-3: Installer parity is enforced across `installer.ps1`, `installer.sh`, and `installer.py` for scratchpad example handling.
  - [x] AC-4: Upgrade diagnostics clearly report scratchpad example refresh status and whether user scratchpad remains preserved.
  - [x] AC-5: New scratchpad options introduced in framework releases are guaranteed to appear in refreshed example surfaces after upgrade.
  - [x] AC-6: Behavior is deterministic when user scratchpad already contains some/new options; no duplicate or conflicting guidance is produced.
  - [x] AC-7: Existing US-0018/US-0050 upgrade and clean-repo guarantees remain intact (no regressions).
  - [x] AC-8: Active/template parity remains aligned for scratchpad example contract and installer behavior.
  - [x] AC-9: Regression tests cover fresh install, upgrade with user-modified scratchpad, and mixed-option drift scenarios.
  - [x] AC-10: README/runbook guidance documents expected upgrade outcomes and troubleshooting for scratchpad example drift.
- Boundaries:
  - In scope: installer/upgrade process behavior and scratchpad example/user contract documentation/tests.
  - Out of scope: changing runtime workflow semantics unrelated to scratchpad configuration surfaces.

## US-0058 — Deterministic Artifact Ordering and Write Discipline
- Title: Enforce deterministic top-down/bottom-up ordering rules when updating workflow artifacts
- Summary: Define and enforce per-file ordering semantics so updates always land in the correct section/order (for example append-only logs at bottom, canonical prioritized lists in deterministic order). Prevent mixed insertion behavior that makes `state.md`, `backlog.md`, and `acceptance.md` hard to trust and maintain.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User reports inconsistent insertion patterns (some updates at top, some at bottom) across key artifacts (`docs/engineering/state.md`, `docs/product/backlog.md`, `docs/product/acceptance.md`).
  - Current contracts define canonical ownership for status but do not fully standardize insertion/order policy for every mutable artifact surface.
  - Decomposition evaluator outcome: single-story recommended because ordering policy, command-write touchpoints, and regression guarantees are tightly coupled and should be shipped as one deterministic contract.
  - User authority evidence: user explicitly requested this as intake.
  - Intake research reference: `R-0033`.
  - Decision update: `DEC-0040` accepted (ordering matrix + fail-safe anchors).
- Acceptance:
  - [x] AC-1: Define a canonical ordering matrix for mutable workflow artifacts (at minimum: `state.md`, `backlog.md`, `acceptance.md`, handoff summary surfaces) with explicit policy per file (`append-bottom`, `prepend-top`, or `sorted-canonical`).
  - [x] AC-2: `docs/engineering/state.md` follows one deterministic checkpoint ordering policy and no command writes checkpoints in conflicting direction.
  - [x] AC-3: `docs/product/backlog.md` story ordering is deterministic (for example by numeric story ID) and preserved across all commands that mutate backlog content.
  - [x] AC-4: `docs/product/acceptance.md` ordering/checkbox rows are deterministically aligned to canonical backlog ordering.
  - [x] AC-5: Command contracts that mutate these files are updated to reference the ordering matrix and fail-safe behavior when placement anchors are missing/ambiguous.
  - [x] AC-6: Repeated command runs are idempotent for ordering (no oscillation/re-shuffle on no-op updates).
  - [x] AC-7: Existing canonical ownership/reconciliation guarantees (US-0045/US-0055) remain intact with no status-precedence regressions.
  - [x] AC-8: Active/template parity is preserved for ordering contracts and affected command docs/rules.
  - [x] AC-9: Regression tests cover positive and negative paths (correct placement, ambiguous anchor fail-safe, and no-op/idempotent re-run).
  - [x] AC-10: README/runbook documents ordering policy and troubleshooting guidance for drifted artifact order.
- Boundaries:
  - In scope: workflow artifact ordering contracts, command mutation behavior, and parity/testing/docs updates.
  - Out of scope: changing product runtime features or redefining story semantics.

## US-0059 — Deterministic Intake Runtime Capability Guard and Single-Writer Drift Safety
- Title: Fail fast on missing role-specific subagent capability and prevent self-write drift false positives in intake
- Summary: Harden intake runtime behavior so `/intake` does not silently degrade when required role-specific subagent capability is unavailable, and does not misclassify its own deterministic writes as external concurrent drift. Add deterministic diagnostics and bounded single-writer safeguards.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User observed an intake run reporting that `po` subagent could not run in the environment and fallback execution continued in-band.
  - Same run reported mid-run backlog drift after writing artifacts, likely conflating self-writes with external concurrent edits.
  - Existing contracts enforce fresh-context role isolation and fail-safe drift behavior, but capability negotiation and writer-identity semantics are not explicit enough for this runtime path.
  - Decomposition evaluator outcome: single-story recommended because capability fail-fast, writer-lock semantics, and drift diagnostics are tightly coupled and should be validated together.
  - User authority evidence: user explicitly requested bug intake.
  - Intake research reference: `R-0035`.
  - Decision update: `DEC-0041` accepted (intake capability fail-fast + single-writer drift safety contract).
- Acceptance:
  - [x] AC-1: `/intake` validates required role-specific subagent capability (`po`) before work starts and fails fast when unavailable.
  - [x] AC-2: Add deterministic fail code for capability mismatch (for example `SUBAGENT_CAPABILITY_UNAVAILABLE`) with actionable remediation guidance.
  - [x] AC-3: Intake runtime must not silently degrade to in-band execution when role-specific subagent is required unless explicit policy opt-in is configured.
  - [x] AC-4: Add deterministic single-writer guard semantics for intake artifact mutation (writer identity/run-id scope) to distinguish self-write vs external concurrent writes.
  - [x] AC-5: Drift detection distinguishes self-write changes from true external mutation and avoids false concurrent-writer blocking.
  - [x] AC-6: On true concurrent writer detection, intake fails safe with deterministic reason code and no partial conflicting overwrite.
  - [x] AC-7: Intake ordering and canonical ownership contracts remain preserved (`backlog` canonical, sorted-canonical placement, target-scoped writes).
  - [x] AC-8: Active/template parity is maintained for command/rule/docs contracts related to capability checks and drift safety behavior.
  - [x] AC-9: Regression tests cover capability-missing fail-fast path, self-write non-false-positive path, and real concurrent-writer fail-safe path.
  - [x] AC-10: README/runbook operator guidance documents capability prerequisites, deterministic diagnostics, and recovery flow.
- Boundaries:
  - In scope: workflow runtime guards, intake execution policy, drift-detection semantics, deterministic diagnostics, and parity/testing/docs updates.
  - Out of scope: runtime product feature behavior, external orchestrator platform migration, or weakening existing fail-closed safety gates.

## US-0060 — Deterministic State Hot-Surface Rollover and Archive Enforcement
- Title: Enforce bounded state hot-surface size with deterministic archive rollover
- Summary: Prevent `docs/engineering/state.md` from unbounded growth by enforcing deterministic rollover thresholds and automatic archival of older checkpoints into `docs/engineering/state-archive/` packs while preserving traceability and fail-safe behavior.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User reports very large `state.md` growth in new repositories (for example ~1800 lines after two sprints), indicating compaction policy is not being enforced strongly enough.
  - Existing `US-0053` compaction contract defines hot-surface + archive strategy, but current behavior appears policy-only and lacks deterministic rollover trigger enforcement.
  - Decomposition evaluator outcome: single-story recommended because threshold policy, archive mechanics, and command-level mutation behavior are tightly coupled and best validated together.
  - User authority evidence: user explicitly requested this as intake.
  - Intake research reference: `R-0036`.
  - Decision update: `DEC-0042` accepted (deterministic state rollover enforcement contract).
- Acceptance:
  - [x] AC-1: Define deterministic rollover trigger for `docs/engineering/state.md` (for example max checkpoints and/or max lines) with explicit default values.
  - [x] AC-2: When trigger is exceeded, commands archive older checkpoints into canonical `docs/engineering/state-archive/state-pack-*.md` and keep only bounded recent hot-surface checkpoints.
  - [x] AC-3: Archive operation is non-destructive and preserves evidence references and ordering chronology.
  - [x] AC-4: Archive pack naming and partitioning are deterministic and idempotent on reruns (no duplicate/oscillating pack creation).
  - [x] AC-5: Hot-surface and archive writes remain append-safe and fail closed on ambiguous anchors or archive-write errors (no partial corruption).
  - [x] AC-6: `/ask` and `/refresh-context` retrieval behavior remains accurate with hot+archive split (latest-first on hot surface, bounded expansion to archive when needed).
  - [x] AC-7: Existing canonical ownership and ordering contracts (US-0045/US-0055/US-0058) remain intact with no regressions.
  - [x] AC-8: Active/template parity is maintained for command contracts, policy docs, and archive artifacts.
  - [x] AC-9: Regression tests cover threshold crossing, rollover success path, idempotent re-run path, and archive-write fail-safe path.
  - [x] AC-10: README/runbook documents rollover thresholds, archive behavior, and operator remediation for fail-safe outcomes.
- Boundaries:
  - In scope: state compaction enforcement contract, deterministic archive rollover mechanics, command/policy parity, and regression/docs updates.
  - Out of scope: changing feature delivery workflow semantics or deleting historical evidence.

## US-0061 — Cross-Phase Artifact Ownership Guard and Deterministic Archive Control
- Title: Prevent cross-phase artifact deletions and enforce deterministic archive execution boundaries
- Summary: Introduce a cross-phase artifact ownership contract so phases cannot delete or rewrite content owned by other phases unless an explicit override-authorized phase is defined. Tighten archival behavior with deterministic pack boundaries, execution controls, and verification to stop silent history loss and unbounded growth.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User reports that in a fresh repository run, prior `architecture.md` story sections were deleted, which violates expected historical continuity.
  - User requests a generalized rule across relevant artifacts/phases: each phase may update its own owned scope, but must not delete other-phase content unless the phase is explicitly designated as an override authority.
  - User also requests stricter, more specific archive control because `state.md` can still grow excessively while archive behavior appears policy-only.
  - Decomposition evaluator outcome: single-story recommended because ownership-guard contracts, override authority matrix, and archive execution controls are tightly coupled and should be validated together.
  - User authority evidence: user explicitly requested this intake.
  - Intake research reference: `R-0037`.
  - Decision update: `DEC-0043` accepted (cross-phase ownership guard + archive verification fail-safe contract).
- Acceptance:
  - [x] AC-1: Define a deterministic phase-to-artifact ownership matrix for all mutable workflow artifacts (including explicit owned scope and prohibited mutations per phase).
  - [x] AC-2: Non-override phases must fail safe when a write would delete or rewrite unrelated phase-owned sections, with deterministic reason code and remediation guidance.
  - [x] AC-3: Introduce explicit override-authorized phase list per artifact (or per section), and require auditable evidence when override mutation is used.
  - [x] AC-4: `docs/engineering/architecture.md` must be protected by non-destructive history-preservation semantics (append or target-section update only); unrelated story sections cannot be removed by normal phase runs.
  - [x] AC-5: Ordering policy and command contracts are extended so ownership guard enforcement is consistent across `/intake`, `/discovery`, `/research`, `/architecture`, `/sprint-plan`, `/execute`, `/qa`, `/verify-work`, `/release`, and `/refresh-context`.
  - [x] AC-6: State archive control is strengthened with deterministic boundary algorithm and explicit execution behavior (not policy-only), including stable pack naming and idempotent reruns.
  - [x] AC-7: Archive operations must provide deterministic verification outputs (what moved, what stayed hot, boundary evidence) and fail closed on mismatch/partial-write risk.
  - [x] AC-8: Existing canonical ownership guarantees (US-0045/US-0055) and deterministic ordering rules (US-0058) remain intact with no precedence regressions.
  - [x] AC-9: Active/template parity is maintained for ownership matrix, override rules, archive controls, and all affected command/rule docs.
  - [x] AC-10: Regression tests cover prevention of cross-phase deletion, authorized override path, archive-boundary determinism/idempotence, and fail-safe behavior.
- Boundaries:
  - In scope: artifact ownership guardrails, override authority model, deterministic archive execution controls, and parity/testing/docs updates.
  - Out of scope: changing product runtime features or deleting historical evidence to reduce file size.

## US-0062 — Installer-Owned `its_magic/` Folder for Framework Metadata
- Title: Separate framework metadata from project content using a dedicated `its_magic/` installation surface
- Summary: Install framework-owned, non-project artifacts (for example README pointer/docs and version marker) into a dedicated `its_magic/` folder so project content (`src`, `docs`, feature files) remains clearly separated from installer/runtime metadata.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User requests clearer separation: framework/installer files should live in `its_magic/`, while project artifacts stay in project-owned locations.
  - User explicitly identifies README and version marker as candidate framework-owned metadata for relocation into `its_magic/`.
  - Existing install/upgrade/clean behavior already has ownership concepts, but top-level placement still mixes framework metadata and project-facing artifacts.
  - Decomposition evaluator outcome: single-story recommended because installer paths, ownership manifest, upgrade/clean parity, and migration compatibility are tightly coupled.
  - User authority evidence: user explicitly requested this intake.
  - Intake research reference: `R-0038`.
- Acceptance:
  - [x] AC-1: Define deterministic ownership boundary for installer-managed framework metadata under canonical folder `its_magic/`.
  - [x] AC-2: Move/emit framework-owned metadata artifacts (including version marker and framework README surface) into `its_magic/` on fresh install.
  - [x] AC-3: Preserve project-owned artifacts (for example `src/`, project `docs/`, app/runtime files) outside `its_magic/` with no forced relocation.
  - [x] AC-4: Upgrade mode migrates legacy top-level framework metadata into `its_magic/` deterministically and idempotently.
  - [x] AC-5: Clean-repo logic removes framework-owned `its_magic/` content while preserving project-owned content outside the ownership set.
  - [x] AC-6: Ownership manifest/schema is updated to classify `its_magic/` entries correctly for install/upgrade/clean operations.
  - [x] AC-7: CLI/help and runbook/README guidance document which files are framework-owned in `its_magic/` vs project-owned.
  - [x] AC-8: Active/template parity is maintained for installer scripts, templates, and ownership policy docs.
  - [x] AC-9: Regression tests cover fresh install, upgrade migration, missing/overwrite modes, and clean-repo behavior for `its_magic/` boundaries.
  - [x] AC-10: Migration path is backward-compatible and non-destructive for existing repositories with previous file layout.
  - Decision update: `DEC-0045` accepted (installer-owned `its_magic/` metadata boundary + legacy migration compatibility).
- Boundaries:
  - In scope: installer ownership boundaries, file-placement contracts, migration/clean behavior, and parity/testing/docs updates.
  - Out of scope: changing project feature runtime behavior or moving project business artifacts into `its_magic/`.

## US-0063 — OS-Aware Runbook Command Auto-Bootstrap with Verified Quality Gates
- Title: Auto-generate real runbook test/lint/typecheck commands per OS and project stack
- Summary: Remove first-run blockers by auto-bootstrapping `docs/engineering/runbook.md` commands for new repositories using OS + stack detection, while preserving strict quality gates and avoiding placeholder-only configuration.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User reports first sprint blocked because runbook commands were not defined for the target environment.
  - User requires quality checks to remain strict and real (no placeholder bypass), and expects OS-aware defaults.
  - Example mismatch observed: Windows operator context while `TEST_COMMAND` is `sh tests/run-tests.sh`.
  - Decomposition evaluator outcome: single-story recommended because installer bootstrap, command verification, and gate compatibility are tightly coupled.
  - User authority evidence: user explicitly requested intake.
  - Intake research reference: `R-0039`.
- Acceptance:
  - [x] AC-1: Define deterministic runbook bootstrap contract for install/upgrade/new-repo onboarding with explicit precedence (`user override > detected defaults > safe fallback`).
  - [x] AC-2: Detect operator OS/shell and generate OS-appropriate command defaults (for example PowerShell on Windows, sh/bash on Unix) for framework baseline checks.
  - [x] AC-3: Detect project stack signals (`package.json`, `pyproject.toml`, `go.mod`, etc.) and emit concrete `TEST_COMMAND` defaults; optional lint/typecheck commands are emitted when confidently detectable.
  - [x] AC-4: Generated commands must be validated/probed; unresolved or invalid command generation fails with deterministic diagnostics and remediation guidance (no silent placeholder success).
  - [x] AC-5: Mandatory quality gate semantics remain intact (`TEST_COMMAND` required; release/sync gates still fail on missing/failing baseline evidence).
  - [x] AC-6: Optional command compatibility remains preserved (`LINT_COMMAND`/`TYPECHECK_COMMAND` may be blank when undetectable and are reported as skipped, not pass).
  - [x] AC-7: Existing repositories with explicit runbook commands are not destructively overwritten; bootstrap is non-destructive and idempotent.
  - [x] AC-8: Installer/CLI/help and runbook/README documentation clearly explain OS-aware bootstrap behavior, override flow, and diagnostics.
  - [x] AC-9: Active/template parity is maintained across installers, template runbook, bootstrap logic, and tests.
  - [x] AC-10: Regression tests cover Windows and Unix default paths, stack detection outcomes, invalid-command fail-fast behavior, and non-destructive reruns.
  - Decision update: `DEC-0046` accepted (OS-aware runbook bootstrap + deterministic diagnostics contract).
- Boundaries:
  - In scope: runbook command bootstrap logic, OS/stack detection, verification diagnostics, and parity/testing/docs updates.
  - Out of scope: weakening release/quality gate contracts or replacing project-specific quality policy decisions.

## US-0064 — Remote Runtime Connectivity Contract for QA/Release/Publish
- Title: Extend release targets with deploy/runtime connectivity metadata and remote phase execution support
- Summary: Expand `docs/engineering/release-targets.json` to include runtime connectivity details (domain, IP, port, ingress/Traefik, Docker-over-SSH options) and use this contract across release/QA/execute phases for remote contexts. Agents must provide operator-ready connection info and persist a canonical hosting/connectivity document.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User requests extending release/publish target config to cover runtime connection details and remote deployment/validation needs.
  - User explicitly asks for domain/IP/port/Traefik and Docker via SSH possibilities in target schema.
  - User expects phases to consume this info when project context is remote, including remote QA/debug paths.
  - User expects agents to communicate connection details clearly to operators (how to connect, where hosted) and persist this in documentation.
  - Decomposition evaluator outcome: single-story recommended because target schema, phase integration, operator reporting, and docs/evidence are tightly coupled.
  - User authority evidence: user explicitly requested intake.
  - Intake research reference: `R-0040`.
  - Decision update: `DEC-0044` accepted (remote connectivity schema + phase-consumption contract).
- Acceptance:
  - [x] AC-1: Extend `docs/engineering/release-targets.json` schema with deterministic runtime connectivity fields (domain, ip/host, port, protocol, ingress/Traefik metadata, environment labels).
  - [x] AC-2: Add deterministic schema support for Docker-over-SSH execution targets with required fields for remote host/auth/env references and container context.
  - [x] AC-3: Release target validation enforces required connectivity fields per target type and fails fast with deterministic diagnostics when invalid/incomplete.
  - [x] AC-4: `/release` consumes enriched connectivity data and emits operator-ready publish/connect instructions (where hosted, how to connect, target endpoint summary).
  - [x] AC-5: `/qa` can use connectivity contract to run remote verification/debug checks when target context is remote, with deterministic no-op/skip behavior when not applicable.
  - [x] AC-6: `/execute` and/or relevant runtime phases honor remote target context for deployment/debug flow when configured, preserving existing safety gates.
  - [x] AC-7: Add canonical documentation artifact for hosting/connectivity summary (for example `docs/engineering/runtime-connectivity.md`) and keep it updated by release flow.
  - [x] AC-8: Operator-facing output and handoff artifacts include local vs remote execution context and connection endpoints without leaking secrets.
  - [x] AC-9: Active/template parity is maintained for schema, commands, docs, and sample target configuration.
  - [x] AC-10: Regression tests cover schema validation, remote/local phase behavior, operator connectivity output, and documentation updates.
- Boundaries:
  - In scope: release-target schema extension, remote phase consumption contract, operator connectivity reporting, and parity/testing/docs updates.
  - Out of scope: introducing secret-inline storage, replacing existing mandatory release/quality gates, or adding vendor-specific lock-in requirements.

## US-0065 — Runtime QA Autopilot for Generated Projects
- Title: Enforce runtime startup, connectivity, log inspection, and bounded self-debug in execute/qa phases
- Summary: For project repositories generated/managed with its-magic, require runtime validation beyond static checks: start the app/service, verify health/connectivity, inspect logs/errors, and run bounded auto-debug retries before reporting PASS.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User reports real generated-repo failure where workflow did not start app locally, did not inspect logs, and did not perform bounded debug retries.
  - Existing QA/execute contracts focus on runbook checks and findings but do not hard-require runtime startup/connectivity validation.
  - Decomposition evaluator outcome: multi-story split accepted because runtime autopilot, generated tests, release operator hints, and intake questioning are related but independently testable.
  - User authority evidence: user explicitly requested the 4-story split (`A-D`) during intake.
  - Intake research reference: `R-0041`.
  - Discovery refinement (US-0065-only): enforce deterministic runtime failure
    reason-code families and keep scope boundary strict (runtime verification
    contract/evidence only; no test scaffolding or release-hint schema work in
    this story).
- Acceptance:
  - [x] AC-1: Define a mandatory runtime validation contract for generated project repos: startup attempt, health/connectivity check, log/error scan, and deterministic PASS/FAIL criteria.
  - [x] AC-2: `/qa` must fail with deterministic reason code when runtime startup fails or endpoint/process remains unreachable after bounded retries.
  - [x] AC-3: `/execute` and `/qa` support bounded self-debug retries (`attempt <= configured max`) with explicit evidence of each retry outcome.
  - [x] AC-4: QA evidence must include startup command, environment context (local/remote), health result, log summary, retry count, and final verdict.
  - [x] AC-5: Runtime checks are stack-aware (Node/Python/Go/Java/.NET at minimum) with deterministic fallback behavior for unknown stacks.
  - [x] AC-6: If webapp context is detected, runtime QA includes browser-level verification path and console/network error inspection guidance where applicable.
  - [x] AC-7: Optional debug-mode workflow is integrated as an escalation path for reproducible runtime failures with bounded instrumentation/cleanup semantics.
  - [x] AC-8: Remote-runtime mode remains supported via `release-targets` connectivity contract and uses sanitized endpoint/auth-reference reporting.
  - [x] AC-9: Active/template parity is maintained for command/rule/runbook/readme surfaces describing runtime autopilot behavior.
  - [x] AC-10: Regression coverage includes success path, startup-fail path, unreachable-endpoint path, and bounded-retry exhaustion with deterministic reason codes.
- Boundaries:
  - In scope: workflow/process runtime validation behavior for generated repositories and evidence contracts.
  - Out of scope: implementing app-specific business logic fixes beyond bounded auto-debug attempts.

## US-0066 — Generated Test Scaffolding and Auto-Run Contract
- Title: Auto-generate baseline tests for app projects and enforce automatic execution in execute/qa
- Summary: During implementation in generated repos, create baseline unit/integration/acceptance test scaffolding by stack/project type, wire it to `TEST_COMMAND`, and require automatic QA execution with evidence.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User requests generated project repositories to receive real runnable tests automatically, not only framework-repo checks.
  - Current baseline gates rely on configured runbook commands but do not guarantee initial test scaffolding for new app repos.
  - Decomposition evaluator outcome: split accepted to keep runtime autopilot and test scaffolding independently verifiable.
  - User authority evidence: user explicitly requested this as Story B in intake.
  - Intake research reference: `R-0041`.
  - Discovery refinement (US-0066-only): deterministic scaffold ownership and rerun idempotence are mandatory so generated tests are created when missing without clobbering user-authored tests/commands.
  - Story boundary reminder: keep release operator hint schema and mandatory intake questionnaire policy in `US-0067` and `US-0068`.
- Acceptance:
  - [x] AC-1: Define deterministic stack/project detection for baseline test scaffold generation (Node/Python/Go/Java/.NET minimum).
  - [x] AC-2: `/execute` generates baseline unit/integration/acceptance test files for app projects when missing and records generated paths in evidence.
  - [x] AC-3: Generated test setup deterministically updates `docs/engineering/runbook.md` `TEST_COMMAND` to runnable baseline command for detected stack.
  - [x] AC-4: `/qa` must execute generated baseline tests automatically and include pass/fail evidence in `qa-findings`.
  - [x] AC-5: If generation is not possible for a detected stack, workflow fails closed with deterministic diagnostics and remediation guidance.
  - [x] AC-6: Existing user-authored tests/commands are preserved (non-destructive merge/append behavior) with deterministic precedence rules.
  - [x] AC-7: Generated tests integrate with runtime autopilot contract so non-starting apps cannot PASS QA even if static tests pass.
  - [x] AC-8: Active/template parity is maintained for generation rules, command docs, and test guidance.
  - [x] AC-9: Regression coverage includes fresh project generation, rerun idempotence, existing-tests preservation, and unsupported-stack fail-fast behavior.
  - [x] AC-10: Release/readiness artifacts reference generated-test evidence in a deterministic and auditable way.
- Boundaries:
  - In scope: workflow-level test scaffolding and execution contracts in generated repositories.
  - Out of scope: full framework-specific advanced test architecture for every ecosystem.

## US-0067 — Release Operator Run/Connect/Verify Hints Contract
- Title: Require operator-ready startup/connectivity guidance in sprint release artifacts
- Summary: Make release output operator-actionable by requiring a deterministic `Run/Connect/Verify` section in sprint notes and legacy pointer surfaces, including startup command, endpoint, health check, env-ref credentials source, and known issues.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User reports release and sprint-end output currently lacks enough practical hints to run and validate shipped features quickly.
  - Existing release notes primarily summarize shipped changes and gate state; operator run/connect guidance is not mandatory.
  - Decomposition evaluator outcome: split accepted to keep release-UX contract testable independently from runtime/test contracts.
  - User authority evidence: user explicitly requested this as Story C in intake.
  - Intake research reference: `R-0041`.
  - Research refinement reference (US-0067-only): `R-0044`.
  - Discovery refinement (US-0067-only): required section schema should be deterministic and order-stable as `Run -> Connect -> Verify -> Credentials(env-ref only) -> Known Issues` to keep reruns idempotent and operator-readable.
  - Discovery refinement (US-0067-only): release finalization must fail closed when required operator fields are missing/ambiguous, with deterministic reason codes and remediation guidance in release findings.
  - Discovery refinement (US-0067-only): local vs remote runtime context must be explicit and consistent with `docs/engineering/runtime-connectivity.md` when that contract exists.
  - Story boundary reminder: keep runtime QA autopilot in `US-0065`, generated test scaffolding in `US-0066`, and intake questionnaire policy in `US-0068`.
- Acceptance:
  - [x] AC-1: Define required `Run/Connect/Verify` section schema for `handoffs/releases/Sxxxx-release-notes.md`.
  - [x] AC-2: Schema includes exact start command(s), runtime mode (`local|remote`), endpoint (`url/ip:port`), expected health signal, and known issues.
  - [x] AC-3: Credentials/auth guidance must reference env variable names only (no inline secrets) and include where values are expected.
  - [x] AC-4: Legacy pointer `handoffs/release_notes.md` includes concise latest run/connect summary linking to canonical sprint notes.
  - [x] AC-5: If required run/connect fields are missing or ambiguous, release finalization fails closed with deterministic reason code and remediation.
  - [x] AC-6: Local vs remote context is explicitly surfaced and aligned with `runtime-connectivity` documentation when available.
  - [x] AC-7: QA and release findings include references proving run/connect guidance was validated against actual verification evidence.
  - [x] AC-8: Active/template parity is maintained for release command docs/templates and runbook guidance.
  - [x] AC-9: Regression coverage includes valid guidance generation, missing-field fail-safe behavior, and secret-redaction checks.
  - [x] AC-10: Operator-facing output remains concise and deterministic across repeated release reruns (idempotent formatting/content contract).
- Boundaries:
  - In scope: release artifact schema and operator guidance quality.
  - Out of scope: deployment platform-specific orchestration engines.

## US-0068 — Mandatory Intake Question Packs for First and Small Intakes
- Title: Enforce structured intake questionnaires with required coverage before persistence
- Summary: Strengthen intake quality by requiring deterministic question packs: a comprehensive first-intake questionnaire and a compact small-intake questionnaire, with required answer coverage before backlog/acceptance persistence.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User reports intake still sometimes proceeds without sufficient clarifying questions despite prior requests.
  - Existing guided intake supports adaptive questions but does not enforce fixed minimum topic coverage sets for first-intake and small-intake modes.
  - Decomposition evaluator outcome: split accepted so questioning policy can be validated independently from runtime/release contracts.
  - User authority evidence: user explicitly requested mandatory first-intake and small-intake question sets with examples.
  - Intake research reference: `R-0041`.
  - Research refinement reference (US-0068-only): `R-0045`.
  - Discovery refinement (US-0068-only): enforce deterministic pack schemas with explicit topic IDs and required/optional classification so coverage checks are machine-verifiable.
  - Discovery refinement (US-0068-only): fail-closed persistence gate must emit deterministic missing-topic reason codes and optional bounded-assumption confirmation path before write.
  - Discovery refinement (US-0068-only): low-touch mode remains available but cannot bypass critical safety coverage capture.
  - Discovery refinement (US-0068-only): intake artifacts must persist coverage evidence (`asked_topics`, `missing_topics`, `assumptions_confirmed`) for deterministic downstream trust.
- Acceptance:
  - [x] AC-1: Define deterministic first-intake question pack with mandatory coverage for users/problem, runtime target/environment, language/framework/runtime, architecture preference, UI/design expectations, security/compliance, non-functional priorities, and scope/timeline.
  - [x] AC-2: Define deterministic small-intake question pack with mandatory coverage for outcome/success criteria, impacted components, constraints/compatibility risks, required tests/acceptance checks, and done definition.
  - [x] AC-3: Intake must not persist story artifacts until required question-pack coverage is satisfied or explicit bounded assumptions are confirmed by user.
  - [x] AC-4: Guided mode keeps adaptive follow-ups, but now with enforceable minimum pack coverage and bounded rounds.
  - [x] AC-5: Low-touch mode remains available but still enforces critical minimum safety questions when required fields are missing.
  - [x] AC-6: Intake output persists questioning evidence (asked topics, unresolved assumptions, confirmations) in backlog/acceptance/handoff artifacts.
  - [x] AC-7: Deterministic reason codes are emitted when intake is blocked due to missing required answers.
  - [x] AC-8: Active/template parity is maintained for intake command, PO agent guidance, runbook, and README documentation.
  - [x] AC-9: Regression coverage includes first-intake flow, small-intake flow, low-touch compatibility, and blocked-on-missing-answer behavior.
  - [x] AC-10: Question packs remain language/project aware with deterministic fallback for unknown stack context.
- Boundaries:
  - In scope: intake workflow policy, required-question coverage, and persistence gating.
  - Out of scope: replacing user authority with forced architectural decisions by AI.

## US-0069 — Strict Phase Role Enforcement in /auto Orchestration
- Title: Fail closed when /auto cannot run a phase with its required role capability
- Summary: Prevent role collapse (for example execute running as tech-lead) by enforcing deterministic phase-to-role mapping in `/auto`, with hard fail-fast behavior when the required role capability is unavailable.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User reported a generated repository run where `/auto` performed intake and then coding under tech-lead context instead of routing through intended phase roles.
  - Existing contracts define per-phase role intent, but capability enforcement is inconsistent across phases and can permit unintended fallback behavior in some repos.
  - User authority evidence: user explicitly requested intake to close this orchestration gap.
  - Discovery refinement (US-0069-only): enforce **preflight** role-capability resolution before each phase spawn; post-hoc evidence alone is insufficient.
  - Discovery refinement (US-0069-only): for phases with allowed role alternates, require **deterministic policy + precedence** so expected role is single-valued at each boundary.
  - Discovery refinement (US-0069-only): reject checkpoint completion when `role` in isolation evidence conflicts with the phase contract (fail-closed mismatch).
  - Discovery refinement (US-0069-only): align `proof_hash`/strict-proof `role` with the same resolved canonical role as isolation evidence for auditable linkage.
  - Discovery refinement (US-0069-only): default-deny non-`dev` execute contexts unless a documented override contract exists.
  - Research refinement reference (US-0069-only): `R-0048`.
- Acceptance:
  - [x] AC-1: Define canonical deterministic phase->role mapping contract for `/auto` (`intake=po`, `discovery=po`, `research=po|tech-lead` per policy, `architecture=tech-lead`, `sprint-plan=tech-lead`, `plan-verify=qa|tech-lead` per policy, `execute=dev`, `qa=qa`, `verify-work=qa`, `release=release`, `refresh-context=curator|po` per policy).
  - [x] AC-2: `/auto` must fail closed with deterministic reason code when required phase role capability is unavailable (no implicit fallback to unrelated role).
  - [x] AC-3: Boundary validation must reject phase completion evidence when `role` does not match expected role contract for that phase run.
  - [x] AC-4: Deterministic diagnostics must include phase id, expected role, actual role/capability result, and remediation guidance.
  - [x] AC-5: `/execute` specifically must never run under tech-lead context unless explicitly allowed by a documented override contract (default deny).
  - [x] AC-6: Resume/continuation logic preserves role enforcement; stale resume sources cannot bypass role checks.
  - [x] AC-7: Active/template parity is maintained for `/auto`, phase command docs, and related runbook/readme guidance.
  - [x] AC-8: Regression coverage includes capability-available pass path, missing-capability fail-fast path, role-mismatch checkpoint rejection, and no-silent-fallback assertions.
  - [x] AC-9: Reason-code vocabulary for role enforcement is deterministic and documented (for example `PHASE_ROLE_CAPABILITY_MISSING`, `PHASE_ROLE_MISMATCH`).
  - [x] AC-10: Release/readiness artifacts include auditable references proving required phase roles were used for completed lifecycle boundaries.
- Boundaries:
  - In scope: orchestration role mapping, capability enforcement, and evidence validation contracts.
  - Out of scope: changing product/business implementation semantics of generated repositories.

## US-0070 — Configurable Auto Phase Selection Policy
- Title: Add scratchpad-controlled phase inclusion/exclusion for /auto
- Summary: Let operators fine-tune which lifecycle phases `/auto` should run by introducing deterministic scratchpad parameters for phase selection, while preserving safety gates and fail-fast semantics.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User requests a configurable way to skip selected phases in `/auto` (for example skip `research` or `sprint-plan`) without abandoning automation.
  - Existing `/auto` supports mode toggles (backlog drain, bulk execute, pause), but does not expose a canonical phase-selection contract.
  - User authority evidence: user explicitly requested this intake as a new idea.
  - Discovery refinement (US-0070-only): treat phase plan as a **resolved ordered subset** of the canonical lifecycle (`intake` → `refresh-context`), computed once per run (and on resume) and written to continuation breadcrumbs before any phase spawn.
  - Discovery refinement (US-0070-only): support **one active policy mode** at a time with deterministic precedence — for example `AUTO_PHASE_PLAN=full` (default), `AUTO_PHASE_EXCLUDE=<csv>`, `AUTO_PHASE_INCLUDE=<csv>`, or `AUTO_PHASE_PROFILE=<name>` — with explicit conflict/fail-closed rules when multiple modes are set.
  - Discovery refinement (US-0070-only): define **non-skippable phases** by default (at minimum anything that records isolation + strict-proof evidence required for downstream gates, and any phase `/auto` uses for mandatory safety such as `qa` / `verify-work` / `release` unless a named **explicit high-risk profile** documents the exception and operator acknowledgment fields).
  - Discovery refinement (US-0070-only): `start-from=<phase>` must **intersect** with the resolved phase plan (only phases at or after the start anchor that remain in the plan); empty intersection fails closed with diagnostics listing resolved plan vs requested start.
  - Discovery refinement (US-0070-only): resume and backlog-drain/bulk/team modes must persist and re-validate the same phase-policy inputs so skipped phases do not “reappear” silently on continuation.
  - Discovery refinement (US-0070-only): operator-visible breadcrumbs should list **selected phases**, **skipped phases + reason** (`default_full_plan`, `policy_exclude`, `non_skippable_gate`, etc.), and invalid-token **fail-fast codes** (unknown phase id, empty plan, policy conflict).
  - Research follow-up (US-0070-only): `/research` should produce a precedence matrix, default non-skippable phase set, named profile sketch, and explicit compatibility notes with the `US-0069` phase→role contract (skipping a phase must not substitute roles or bypass capability gates).
  - Research refinement reference (US-0070-only): `R-0049`.
  - Architecture refinement reference (US-0070-only): `DEC-0052`.
- Acceptance:
  - [x] AC-1: Define canonical scratchpad contract for selectable phase policy (include list, exclude list, or named profile) with deterministic precedence.
  - [x] AC-2: `/auto` resolves effective phase plan deterministically and records it in continuation breadcrumbs before execution.
  - [x] AC-3: Unknown or invalid phase identifiers in policy fail closed with deterministic diagnostics (no silent ignore).
  - [x] AC-4: Safety-critical gates cannot be bypassed silently; policy defines which phases are non-skippable by default and why.
  - [x] AC-5: `start-from=<phase>` and phase-selection policy interaction is deterministic and documented.
  - [x] AC-6: Team/bulk/backlog-drain modes remain compatible with phase-selection policy and preserve bounded stop behavior.
  - [x] AC-7: Resume behavior persists selected-phase policy context so continuation is consistent after interruption.
  - [x] AC-8: Active/template parity is maintained for `/auto`, scratchpad examples, runbook, and README documentation.
  - [x] AC-9: Regression coverage includes default profile (all phases), selective skip examples (`research`, `sprint-plan`), invalid config fail-fast, and resume consistency checks.
  - [x] AC-10: Operator-facing status output clearly shows selected/skipped phases and reason codes at each boundary.
- Boundaries:
  - In scope: workflow orchestration policy for phase selection and diagnostics.
  - Out of scope: per-phase internal implementation logic changes unrelated to selection control.

## US-0071 — User-Visible Internal Metadata Sanitization Guard
- Title: Block internal planning identifiers from user-visible software surfaces
- Summary: Prevent development/planning metadata (for example `US-xxxx` IDs) from appearing in user-visible UI/output by enforcing deterministic sanitization checks in implementation and QA, while allowing internal docs and code comments.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User reports repeated leakage where User Story IDs are written into visible UI elements or other end-user-facing software surfaces.
  - User requirement: planning/development identifiers are allowed only in internal documentation and code comments, not in user-visible software content.
  - Existing contracts do not define a global user-visible metadata redaction policy across generated project outputs.
  - Intake research reference: `R-0046`.
  - Intake pack evidence:
    - selected_pack=`small-intake-pack`
    - asked_topics=`outcome_success_criteria`,`impacted_components`,`constraints_compatibility_risks`,`required_tests_acceptance_checks`,`done_definition`
    - missing_topics=`(none)`
    - assumptions_confirmed=`(none)`
  - Discovery refinement (2026-03-21): user-visible surfaces scoped to operator/end-user software outputs (CLI/UI/errors/installer-visible text), excluding internal `docs/**`, `.cursor/**`, sprint/handoff/decision artifacts, and code comments; forbidden baseline patterns remain `US|DEC|R` + four digits in those outputs only.
  - Discovery refinement (2026-03-21): execute/QA/release evidence must prove checks ran with deterministic reason codes and remediation refs; active/template parity required for policy-bearing surfaces.
- Acceptance:
  - [x] AC-1: Define deterministic policy for forbidden internal-planning token patterns in user-visible software surfaces (minimum: `US-[0-9]{4}`, `DEC-[0-9]{4}`, `R-[0-9]{4}`).
  - [x] AC-2: Define deterministic allowlist for internal-only surfaces where these identifiers are permitted (documentation artifacts and code comments at minimum).
  - [x] AC-3: `/execute` adds/uses a non-bypass default guard that prevents introducing forbidden tokens into user-visible UI/text output files for in-scope changes.
  - [x] AC-4: `/qa` performs automated verification for this policy and fails closed with deterministic reason code when leakage is detected.
  - [x] AC-5: Findings/remediation guidance must include exact evidence refs (file/path context), detected token class, and safe replacement guidance.
  - [x] AC-6: Deterministic reason-code vocabulary is documented (for example `USER_VISIBLE_INTERNAL_METADATA_DETECTED`, `METADATA_SANITIZATION_POLICY_MISSING`).
  - [x] AC-7: Existing valid internal references in docs/comments remain allowed and are not falsely blocked by the guard.
  - [x] AC-8: Active/template parity is maintained for command guidance, rules, runbook, and README surfaces.
  - [x] AC-9: Regression coverage includes positive (no leak), negative (leak blocked), allowlist behavior, and rerun idempotence checks.
  - [x] AC-10: Release/readiness artifacts include auditable evidence that user-visible metadata sanitization checks were executed and passed.
- Boundaries:
  - In scope: workflow-level policy and validation for user-visible internal metadata leakage.
  - Out of scope: content moderation/business copywriting standards unrelated to internal planning metadata.

## US-0072 — Deterministic Context Slimming and Archive Enforcement Across Core Artifacts
- Title: Enforce compact hot-surfaces and bounded phase reads for state, handoffs, and architecture
- Summary: Prevent unbounded artifact growth and reduce subagent hallucination risk by enforcing deterministic archive rollover for large core artifacts (`state`, handoffs, architecture), plus strict phase read budgets and minimal context packs.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User reports `docs/engineering/state.md` keeps growing while `docs/engineering/state-archive/` remains empty, indicating rollover is not being effectively enforced.
  - User reports very large `handoffs` and `docs/engineering/architecture.md`, causing high-context noise and increased misunderstanding risk for subagents.
  - User expects small, role-relevant context surfaces while preserving required historical evidence and problem-solving quality.
  - Existing stories (`US-0053`, `US-0060`, `US-0061`) define compaction/ownership contracts, but operational enforcement appears incomplete in active runs.
  - Intake research reference: `R-0047`.
  - Intake pack evidence:
    - selected_pack=`small-intake-pack`
    - asked_topics=`outcome_success_criteria`,`impacted_components`,`constraints_compatibility_risks`,`required_tests_acceptance_checks`,`done_definition`
    - missing_topics=`(none)`
    - assumptions_confirmed=`(none)`
  - Discovery refinement (2026-03-22): default enforcement triad is `state.md`, `handoffs/po_to_tl.md`, and `architecture.md`; other handoffs require explicit architecture justification to include. Thresholds and hot caps must bind to merged scratchpad keys; rollover executes in the same mutating phase or fails closed.
  - Discovery refinement (2026-03-22): minimal-read policy requires per-phase required files + bounded escalation; verification tuple `boundary`/`moved`/`retained`/`pack_ref` plus idempotent pack behavior; regression must catch oversize-hot-without-archive.
  - Research refinement (2026-03-22): extended **`R-0047`** — triad scoped to `state.md` / `po_to_tl.md` / `architecture.md`; scratchpad-bound thresholds (extend beyond `STATE_HOT_*` for the latter two); phase×artifact mutation ownership (`refresh-context` vs PO vs tech-lead boundaries); minimal-read budgets + compact pointer artifacts; reason-code and regression alignment with `R-0033`/`R-0036`/`R-0037`.
  - Architecture refinement reference (US-0072-only): **`DEC-0054`** (triad thresholds, archive paths, same-phase rollover, verification tuple, minimal-read/reason-code contract).
- Acceptance:
  - [x] AC-1: Define deterministic hot/archive contract for `docs/engineering/state.md`, `handoffs/po_to_tl.md`, and `docs/engineering/architecture.md` with explicit thresholds and pack naming.
  - [x] AC-2: When threshold is exceeded, rollover must execute in the same phase boundary or fail closed with deterministic reason code (no silent continuation with oversized hot files).
  - [x] AC-3: Archive execution writes deterministic verification evidence (`boundary`, `moved`, `retained`, `pack_ref`) and is idempotent on reruns.
  - [x] AC-4: `/refresh-context` and any phase mutating high-growth artifacts must enforce archive verification gates before completion.
  - [x] AC-5: Define deterministic minimal-read policy per phase (required files + optional escalation path) with bounded line/file budgets.
  - [x] AC-6: Introduce compact phase-context artifacts (hot summaries/pointers) so subagents read latest relevant evidence first and expand only when unresolved.
  - [x] AC-7: Deterministic reason-code taxonomy covers archive and context-budget failures (for example `STATE_ARCHIVE_REQUIRED`, `CONTEXT_BUDGET_EXCEEDED`, `ARTIFACT_HOT_SURFACE_OVERSIZE`).
  - [x] AC-8: Existing safety and traceability guarantees remain intact (no historical evidence loss; archive references remain auditable and linked).
  - [x] AC-9: Active/template parity is maintained for command contracts, scratchpad/runbook/readme guidance, and archive directory docs.
  - [x] AC-10: Regression coverage includes threshold-crossing success, empty-archive regression detection, idempotent rollover, bounded-read enforcement, and fail-safe behavior.
- Boundaries:
  - In scope: workflow artifact compaction enforcement, archive verification, and phase-context minimization policy.
  - Out of scope: deleting historical evidence, weakening QA/release gates, or changing product-runtime behavior.

## US-0073 — Scratchpad Delivery Simplification (Example-Only Install Policy)
- Title: Decide and enforce whether installer should ship only scratchpad example by default
- Summary: Evaluate and implement a deterministic installer policy for scratchpad artifacts so delivery is simplified (example-only baseline) without breaking automation defaults, upgrade behavior, or parity across installer entry points.
- Priority: P1
- Status: DONE
- Discovery notes:
  - User requests simplifying delivery: shipping both `.cursor/scratchpad.md` and `.cursor/scratchpad.local.example.md` feels redundant; user proposes example-only as sufficient.
  - Existing contracts (`US-0018`, `US-0057`, `DEC-0039`) define upgrade-safe scratchpad behavior and ownership; discovery narrows the open question to **one canonical delivery model** (retain committed baseline vs example-only with explicit materialization) and **merged resolution order** so automation flags stay deterministic.
  - Cross-cutting risk: `/auto` and phase commands must keep the same effective policy after install/upgrade; missing required keys must **fail closed** with diagnostics — no permissive silent defaults (`AC-2`, `AC-4`).
  - Migration: upgrade and clean-install paths must handle legacy dual-file repos and preserved `.cursor/scratchpad.local.md` without violating framework vs user ownership.
  - Parity: all installer surfaces + active/`template/` scratchpad-related artifacts stay aligned; tests must cover fresh install, upgrade from legacy, missing baseline, and local override preservation (`AC-6`, `AC-9`).
  - Intake research reference: `R-0050` (expand with delivery-model + merge-precedence findings in `/research`).
  - Research pointer (2026-03-23): per **`R-0050`** — canonical **Model A vs Model B**
    delivery choice, **merged precedence** (local → baseline/materialized →
    example), upgrade/migration invariants, installer parity, and regression
    matrix; see `docs/engineering/research.md` (`## R-0050`).
  - Architecture refinement reference (US-0073-only): **`DEC-0055`** — **Model B**
    (example-only + materialized baseline), merge precedence, upgrade/legacy
    invariants, parity surfaces; see `docs/engineering/architecture.md` (**US-0073**
    section).
  - Intake pack evidence:
    - selected_pack=`small-intake-pack`
    - asked_topics=`outcome_success_criteria`,`impacted_components`,`constraints_compatibility_risks`,`required_tests_acceptance_checks`,`done_definition`
    - missing_topics=`(none)`
    - assumptions_confirmed=`(none)`
- Acceptance:
  - [x] AC-1: Define canonical installer delivery policy for scratchpad artifacts (`scratchpad.md` + example, or example-only with explicit fallback semantics), with deterministic rationale.
  - [x] AC-2: If example-only mode is selected, `/auto` and phase commands must still resolve required flags deterministically (no missing-config silent fallback).
  - [x] AC-3: Upgrade mode (`its-magic --mode upgrade`) preserves user-owned local overrides and applies the selected scratchpad delivery policy consistently.
  - [x] AC-4: Missing/invalid scratchpad baseline state fails closed with deterministic diagnostics and remediation guidance.
  - [x] AC-5: Ownership boundaries are explicit for framework-owned vs user-owned scratchpad artifacts and remain compatible with clean-repo behavior.
  - [x] AC-6: Installer parity is maintained across `installer.ps1`, `installer.sh`, `installer.py`, and CLI entrypoint behavior.
  - [x] AC-7: Documentation (README + runbook) clearly explains the chosen model, migration path, and operator actions.
  - [x] AC-8: Active/template parity is preserved for scratchpad-related contracts and examples.
  - [x] AC-9: Regression coverage includes fresh install, upgrade from legacy model, missing-file recovery, and local override preservation.
  - [x] AC-10: Decision evidence references overlap resolution with `US-0018`/`US-0057` and confirms no regression in automation safety defaults.
- Boundaries:
  - In scope: installer delivery model, config-resolution safety, parity/docs/tests for scratchpad artifacts.
  - Out of scope: removing automation controls or weakening existing fail-closed runtime gates.

## US-0074 — Baseline Regression Cleanup for Installer and Version Sync Checks
- Title: Resolve remaining baseline failing checks and restore fully green validation baseline
- Summary: Close the known persistent baseline test failures so `tests/run-tests.*` becomes fully green again, focusing on Homebrew/npm version alignment and installer/CLI `TEST_COMMAND` bootstrap regressions.
- Priority: P1
- Status: DONE
- Discovery notes:
  - Recent QA passes for in-scope stories still report recurring out-of-scope baseline failures, reducing confidence in end-to-end compatibility health.
  - Current known failing checks include:
    - `Homebrew stable formula URL uses npm version tag`
    - `Homebrew stable formula version matches npm version`
    - `Installer bootstraps TEST_COMMAND for detectable stack`
    - `CLI missing install bootstraps TEST_COMMAND for detectable stack`
  - User explicitly requests these remaining baseline checks to be cleared.
  - Intake research reference: `R-0051` (extended post-discovery: **Post-discovery findings
    (2026-03-24) — US-0074** in `docs/engineering/research.md`; TL **`/research`** checkpoint
    in `docs/engineering/state.md`).
  - Intake pack evidence:
    - selected_pack=`small-intake-pack`
    - asked_topics=`outcome_success_criteria`,`impacted_components`,`constraints_compatibility_risks`,`required_tests_acceptance_checks`,`done_definition`
    - missing_topics=`(none)`
    - assumptions_confirmed=`(none)`
  - Discovery refinement (2026-03-24, PO):
    - Scope is exactly the four baseline asserts listed above (no expansion into
      unrelated triad, scratchpad, or release-gate stories).
    - Homebrew work centers on `packaging/homebrew/its-magic.rb` + publish/version
      bump mechanics that must stay aligned with `package.json` / npm release tags.
    - `TEST_COMMAND` work spans triple installer + CLI missing-install paths and
      target `docs/engineering/runbook.md` (and `template/` mirror) with
      stack-aware detection per existing runbook/bootstrap contracts.
    - Primary evidence anchors for research: `sprints/S0051/qa-findings.md`,
      `tests/report.md`, `packaging/homebrew/its-magic.rb`, installer/CLI sources,
      `docs/engineering/research.md` (`R-0051`).
    - PO → TL handoff addendum: `handoffs/po_to_tl.md` (Discovery Addendum —
      US-0074); checkpoint: `docs/engineering/state.md` discovery section for
      **`US-0074`**.
  - Architecture (2026-03-24, Tech Lead): contract locked in **`DEC-0056`**
    (`decisions/DEC-0056.md`); narrative and traceability in
    `docs/engineering/architecture.md` **`# US-0074`**; research basis **`R-0051`**
    (`docs/engineering/research.md`); checkpoint: `docs/engineering/state.md`
    architecture section for **`US-0074`**.
- Acceptance:
  - [x] AC-1: Reproduce and classify each currently failing baseline check with deterministic root-cause notes and owning artifact paths.
  - [x] AC-2: Fix Homebrew stable formula URL/version sync with npm version source so both baseline checks pass deterministically.
  - [x] AC-3: Fix installer and CLI missing-install `TEST_COMMAND` bootstrap behavior for detectable stacks with deterministic fallback diagnostics.
  - [x] AC-4: Preserve existing upgrade/install ownership contracts (`US-0018`, `US-0057`, `US-0063`) with no regressions.
  - [x] AC-5: Ensure cross-platform parity across `installer.ps1`, `installer.sh`, `installer.py`, and CLI wrapper behavior.
  - [x] AC-6: Update tests to assert corrected behavior without masking failures; no forced pass shortcuts.
  - [x] AC-7: QA findings for this story must show zero remaining baseline failures from the known four-check set.
  - [x] AC-8: Active/template parity is maintained for formulas, installer scripts, runbook/readme guidance, and validation scripts.
  - [x] AC-9: Release/readiness artifacts include auditable evidence of all four formerly failing checks now passing.
  - [x] AC-10: Document deterministic remediation guidance for future regressions in these baseline areas.
- Boundaries:
  - In scope: baseline regression cleanup for known failing installer/version-sync checks and related parity/docs/tests.
  - Out of scope: introducing unrelated feature work beyond these baseline failures.
