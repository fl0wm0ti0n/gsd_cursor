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

- [ ] US-0015: Document empty runbook commands as intentional (LINT/FORMAT/TYPECHECK not needed for this project type)
- [ ] US-0016: Sync Homebrew stable formula version with npm on next release
- [ ] US-0017: Add template-drift guard (test or convention to keep active files and template/ aligned)
- [ ] US-0018: Smart upgrade mode for repos already using its-magic
- [ ] US-0024: Add memory-drift audit command (artifact memory vs actual codebase changes, with non-blocking report output)
- [ ] US-0025: Add explicit backlog-to-sprint traceability contract and project-wide cross-reference index
- [ ] US-0026: Define milestone lifecycle states, required artifact fields, and command update points
- [ ] US-0027: Define UAT artifact lifecycle, ownership, and completion evidence requirements
- [ ] US-0028: Security & compliance review agent with configurable profiles (10 ACs)
- [ ] US-0029: Knowledge curation & early research during intake and architecture (10 ACs)
- [ ] US-0030: Release gate for README/runbook delta checks when commands/flags change (8 ACs)
- [ ] US-0031: Optional documentation pack (Design Concept, CRS, Technical Spec) behind enable flag (8 ACs)
- [ ] US-0032: Optional per-feature user guide generation behind enable flag (8 ACs)
- [ ] US-0033: Configurable guided `/intake` behavior (clarifying questions, options, PO web research) with switchable low-touch mode (9 ACs)
- [ ] US-0034: Optional multi-repo/module compatibility observability + contract drift checks with zero-overhead default (8 ACs)
- [ ] US-0035: Component-scoped execution mode with unaffected-component protection checks and decision gates (8 ACs)
- [ ] US-0036: Official `.cursor/remote.json` template + schema/examples + fail-fast validation with zero-overhead default-off mode (9 ACs)
- [ ] US-0037: Mid-process `/auto` continuation with explicit start-from, deterministic resume source, and one-command remaining-flow execution (9 ACs)
- [ ] US-0038: Phase-triggered sync policy with guarded auto-push, mandatory tests, QA-first safety defaults, and branch protections (10 ACs)
- [ ] US-0039: Release gate tightening for check-in tests plus QA/UAT completion evidence, deterministic gate order, and template parity (10 ACs)
- [ ] US-0040: Per-sprint release notes and release queue tracker with migration/backfill, backward compatibility, and default-safe non-overwrite behavior (9 ACs)
- [x] US-0019: Clean placeholder content from template and active files
- [x] US-0020: /ask command for context-aware questions without workflow artifacts
- [x] US-0021: Critical evaluation in intake and architecture (challenge ideas, check duplicates, suggest alternatives)
- [x] US-0022: Sprint sizing rules and configurable sprint planning via scratchpad options
- [x] US-0023: Fresh subagent context per phase and /auto orchestration
