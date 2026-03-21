# Acceptance

## Plan.md Section 13 — Definition of Done for the Kit

- [x] User can start `/intake` (also via voice-text) and gets follow-up questions
- [x] Story + Acceptance are written to product docs
- [x] Sprint plan generates `sprints/Sxxxx/*` + handoffs
- [x] Execute/QA/Release work via artifact-based workflow
- [x] Pause/Resume works without context drift
- [x] Decision gate creates `decisions/DEC-xxxx.md` and stops until user decides
- [x] Curator keeps `state.md` and `decisions.md` compact
- [x] Hooks work fail-open and block only clearly dangerous commands
- [x] CI/CD workflows exist and use runbook commands

## Plan.md Section 14 — Implementation Checklist

- [x] Repo structure per section 4 (achieved + expanded)
- [x] 10+ slash commands (19 implemented, plan called for 10)
- [x] 4+ rules .mdc (5 implemented, added coding-standards.mdc)
- [x] Skill + templates (14 templates, plan called for 6)
- [x] 6 subagents defined (PO, Tech Lead, Dev, QA, Release, Curator)
- [x] Hooks: hooks.json + hook.py dispatcher + scratchpad flags
- [x] Doc templates + sprint starter in place
- [x] CI/CD: ci.yml + deploy.yml + runbook keys
- [x] README extended: quick start, voice options, CI/CD usage

## Beyond-Plan Features (bonus)

- [x] CLI installer with triple-platform parity (PS1, Bash, Python)
- [x] npm / Chocolatey / Homebrew distribution
- [x] Unified release automation scripts
- [x] 3-layer quality chain (AI loop, validate-and-push, CI auto-fix)
- [x] Quick mode for small tasks
- [x] Milestones for grouping delivery phases
- [x] Benchmark suite (scenario, live, headless, prompted)
- [x] Team mode with local overrides (scratchpad.local.md)
- [x] Configurable automation modes (scratchpad flags)
- [x] Additional commands: auto, quick, map-codebase, plan-verify, verify-work, phase-context, milestone-start, milestone-complete, research

## Remaining Items

- [x] US-0015: Document empty runbook commands as intentional (LINT/FORMAT/TYPECHECK not needed for this project type)
- [x] US-0016: Sync Homebrew stable formula version with npm on next release
- [x] US-0017: Add template-drift guard (test or convention to keep active files and template/ aligned)
- [x] US-0018: Smart upgrade mode for repos already using its-magic
- [x] US-0024: Add memory-drift audit command (artifact memory vs actual codebase changes, with non-blocking report output)
- [x] US-0025: Add explicit backlog-to-sprint traceability contract and project-wide cross-reference index
- [x] US-0026: Define milestone lifecycle states, required artifact fields, and command update points
- [x] US-0027: Define UAT artifact lifecycle, ownership, and completion evidence requirements
- [x] US-0028: Security & compliance review agent with configurable profiles (10 ACs)
- [x] US-0029: Knowledge curation & early research during intake and architecture (10 ACs)
- [x] US-0030: Release gate for README/runbook delta checks when commands/flags change (8 ACs)
- [x] US-0031: Optional documentation pack (Design Concept, CRS, Technical Spec) behind enable flag (8 ACs)
- [x] US-0032: Optional per-feature user guide generation behind enable flag (8 ACs)
- [x] US-0033: Configurable guided `/intake` behavior (clarifying questions, options, PO web research) with switchable low-touch mode (9 ACs)
- [x] US-0034: Optional multi-repo/module compatibility observability + contract drift checks with zero-overhead default (8 ACs)
- [x] US-0035: Component-scoped execution mode with unaffected-component protection checks and decision gates (8 ACs)
- [x] US-0036: Official `.cursor/remote.json` template + schema/examples + fail-fast validation with zero-overhead default-off mode (9 ACs)
- [x] US-0037: Mid-process `/auto` continuation with explicit start-from, deterministic resume source, and one-command remaining-flow execution (9 ACs)
- [x] US-0038: Phase-triggered sync policy with guarded auto-push, mandatory tests, QA-first safety defaults, and branch protections (10 ACs)
- [x] US-0039: Release gate tightening for check-in tests plus QA/UAT completion evidence, deterministic gate order, and template parity (10 ACs)
- [x] US-0040: Per-sprint release notes and release queue tracker with migration/backfill, backward compatibility, and default-safe non-overwrite behavior (9 ACs)
- [x] US-0041: End-to-end lifecycle QA for `its-magic` install/upgrade/clean flows with backup, negative-path, parity, and documentation evidence (9 ACs)
- [x] US-0042: Official post-QA release-findings workflow with dedicated artifact, deterministic handoff, and parity coverage (8 ACs)
- [x] US-0043: Backlog reconciliation gate for released sprints with deterministic evidence precedence, drift fail-safe reason codes, and parity coverage (10 ACs)
- [x] US-0044: Continuous `/auto` backlog-drain mode with deterministic story selection, bounded run switches, decision-gate safety, and parity coverage (10 ACs)
- [x] US-0045: Canonical status source and global drift guard across backlog/acceptance/state with one-time normalization and fail-safe reconciliation checks (10 ACs)
- [x] US-0046: Explicit `/sprint-plan --bulk` mode for deterministic multi-story planning with bounded limits and sizing-safe grouping/splitting (10 ACs)
- [x] US-0047: Explicit bulk execute orchestration mode with fresh subagent isolation, execute↔QA loop controls, and bounded stop/skip semantics (10 ACs)
- [x] US-0048: Enforced per-phase subagent isolation with auditable evidence and fail-closed workflow/release gate checks (10 ACs)
- [x] US-0049: Legacy DONE-story acceptance/traceability backfill guard — one-time backfill + ongoing guard, audit report, reason codes, template parity (8 ACs)
- [x] US-0019: Clean placeholder content from template and active files
- [x] US-0020: /ask command for context-aware questions without workflow artifacts
- [x] US-0021: Critical evaluation in intake and architecture (challenge ideas, check duplicates, suggest alternatives)
- [x] US-0022: Sprint sizing rules and configurable sprint planning via scratchpad options
- [x] US-0023: Fresh subagent context per phase and /auto orchestration
- [x] US-0050: Clean install hygiene and complete clean-repo coverage
- [x] US-0051: Intelligent intake decomposition and risk-aware PO questioning
- [x] US-0052: Optional fresh-project ID namespace bootstrap
- [x] US-0053: Context compaction and tiered token-cost optimization mode
- [x] US-0054: Configurable multi-target release publish with confirmation gate
- [x] US-0055: Deterministic status reconciliation command for backlog/acceptance/state/resume drift
- [x] US-0056: Strict runtime proof for per-phase subagent isolation with fail-closed auto gates
- [x] US-0057: Upgrade-safe scratchpad local example refresh and installer parity
- [x] US-0058: Deterministic artifact ordering and write discipline
- [x] US-0059: Deterministic intake runtime capability guard and single-writer drift safety
- [x] US-0060: Deterministic state hot-surface rollover and archive enforcement
- [x] US-0061: Cross-phase artifact ownership guard and deterministic archive control
- [x] US-0062: Installer-owned `its_magic/` folder for framework metadata
- [x] US-0063: OS-aware runbook command auto-bootstrap with verified quality gates
- [x] US-0064: Remote runtime connectivity contract for QA/release/publish
- [x] US-0065: Runtime QA Autopilot for generated projects (startup/connectivity/logs/bounded debug retries)
- [x] US-0066: Generated test scaffolding + auto-run contract for app projects
- [x] US-0067: Release operator Run/Connect/Verify hints contract
- [x] US-0068: Mandatory intake question packs for first and small intakes
- [x] US-0069: Strict phase role enforcement in `/auto` orchestration
- [x] US-0070: Scratchpad-controlled `/auto` phase selection policy
- [x] US-0071: User-visible internal metadata sanitization guard
- [x] US-0072: Deterministic context slimming and archive enforcement across core artifacts
- [x] US-0073: Scratchpad delivery simplification (example-only install policy)
- [x] US-0074: Baseline regression cleanup for installer and version sync checks
