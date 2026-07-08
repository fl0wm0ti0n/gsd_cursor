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
- [x] US-0075: Upgrade scratchpad example-first refresh and paired catalog parity (DEC-0057 / AC-11)
- [x] US-0076: Executable scratchpad-driven sync and auto-push wiring (DEC-0018 implementation)
- [x] US-0077: Documentation audience profiles and dual README strategy
- [x] US-0078: Enforced interactive intake question evidence (UAT closure: `sprints/S0057/uat.json`, `sprints/S0057/uat.md`, verify-work **2026-03-28** / `orchestrator_run_id=auto-20260328-01`; release **2026-03-29**: `sprints/S0057/release-findings.md`, `handoffs/releases/S0057-release-notes.md`)
- [x] US-0079: First-class bug issue workflow (open/closed only)
- [x] US-0080: Token-cost hardening for orchestrated runs (UAT closure: `sprints/S0059/uat.json`, `sprints/S0059/uat.md`, verify-work **2026-03-29** / `orchestrator_run_id=auto-20260329-02`; release **2026-03-29**: `sprints/S0059/release-findings.md`, `handoffs/releases/S0059-release-notes.md`, queue **`S0059`** → **`released`**)
- [x] US-0081: First-intake full-plan coverage and story-map gate
- [x] US-0082: Agent-driven codebase map bootstrap (UAT closure: `sprints/S0062/uat.json`, `sprints/S0062/uat.md`, verify-work **2026-03-31T21:20:00Z** / `orchestrator_run_id=auto-20260331-02`)
- [x] US-0083: Delegable intake clarification without hard blocks
- [x] US-0084: POSIX npm installer + Linux remote test targets (WSL / SSH / Docker)
- [x] US-0085: Gitignored `.env` for remote and release connectivity (no AI read)
- [x] US-0086: Automation-driven remote execution selection (Docker / SSH / NL container intent)
- [x] US-0087: `/auto` explicit bug targeting (fix all OPEN bugs / fix `BUG-####`)
- [x] US-0088: `/auto` continuous multi-phase loop + quiet backlog drain (close one-phase-stop gap)
- [x] US-0089: Cursor Caveman mode (scratchpad-configurable terse responses; default off; parity + tests)
- [x] US-0090: Optional Caveman-style input compression (safe file scope, originals preserved, gated after US-0089)
- [x] US-0091: README ↔ backlog/acceptance feature coverage backfill across root README.md, template/README.md, and docs/developer/README.md, plus blocking release-gate extension composing on US-0030 (10 ACs)
- [x] US-0092: Full-autonomy `/auto` mode — shipped outer driver, self-build/self-test UAT, block auto-resolve, drain-without-pause, TOKEN_PROFILE token-cost-only orthogonality (10 ACs) (UAT closure: `sprints/S0081/uat.json`, `sprints/S0081/uat.md`, verify-work **2026-06-06T22:00:00Z** / `orchestrator_run_id=auto-20260606-03`; release **2026-06-06T22:30:00Z** / `handoffs/releases/S0081-release-notes.md`, queue **`S0081`** → **`released`**)
- [x] US-0093: Cursor browser-integrated UAT self-test — execute browser_smoke/manual UI probes, complete process_health/cli_smoke stubs, evidence in uat.json (10 ACs)
- [x] US-0094: README visionary intro + tiered feature hierarchy — autonomous AI dev team positioning, main/sub feature tiers, full US/BUG coverage preserved, root/template byte parity (10 ACs) (UAT closure: `sprints/S0083/uat.json`, `sprints/S0083/uat.md`, verify-work **2026-06-07T15:30:00Z** / `orchestrator_run_id=auto-20260607-01`; release **2026-06-07T16:30:00Z** / `handoffs/releases/S0083-release-notes.md`, queue **`S0083`** → **`released`**)
- [x] US-0095: Native in-Cursor `/auto` auto-chaining — `full_autonomy` + drain continues in-chat across phases and segment boundaries without `auto_outer_driver.py`; spawn-only + hard gates preserved; outer driver optional fallback (10 ACs) (UAT closure: `sprints/S0084/uat.json`, `sprints/S0084/uat.md`, verify-work **2026-06-07T22:30:00Z** / `orchestrator_run_id=auto-20260607-02`; release **2026-06-07T23:30:00Z** / `handoffs/releases/S0084-release-notes.md`, queue **`S0084`** → **`released`**)
- [x] US-0096: Delivery modes — `DELIVERY_MODE` ultra_lean + mega_quick with layered memory (pack.json, active-context index), universal token wins, standard lifecycle byte-compatible (12 ACs)
- [x] US-0097: Project-owned root README — framework README confined to `its_magic/` only; bootstrap on first project story; mandatory per-story/sprint README growth; separated project vs framework doc gates (10 ACs) (UAT closure: `sprints/S0087/uat.json`, `sprints/S0087/uat.md`, verify-work **2026-06-14T02:00:00Z** / `orchestrator_run_id=auto-20260613-01`; release **2026-06-14T04:30:00Z** / `handoffs/releases/S0087-release-notes.md`, queue **`S0087`** → **`released`**)
- [x] US-0098: Dev environment auto-launch profile — detect/persist dev runtime, bounded rebuild/relaunch after execute changes, operator connection surface; docker-host-local vs remote; default-off scratchpad gate (10 ACs) (UAT closure: `sprints/S0088/uat.json`, `sprints/S0088/uat.md`, verify-work **2026-06-14T12:00:00Z** / `orchestrator_run_id=auto-20260613-01`; release **2026-06-14T12:30:00Z** / `handoffs/releases/S0088-release-notes.md`, queue **`S0088`** → **`released`**)
- [x] US-0099: Auto-bootstrap dev-environment profile on install/upgrade — non-destructive copy of template example to `.cursor/dev-environment.json` when missing; npm postinstall parity; runbook customize-after-bootstrap (8 ACs) (UAT closure: `sprints/S0089/uat.json`, `sprints/S0089/uat.md`, verify-work **2026-06-14T23:00:00Z** / `orchestrator_run_id=auto-20260614-01`; release **2026-06-14T23:30:00Z** / `handoffs/releases/S0089-release-notes.md`, queue **`S0089`** → **`released`**)
- [x] US-0100: Version-scoped release changelog — cumulative CHANGELOG with US/BUG summaries per semver, per-version release docs, `/release` derivation + GitHub/git notes attachment composing with US-0040/US-0054 (10 ACs)
- [x] US-0101: Per-phase model tier selection for subagents — MODEL_TIER scratchpad (cheap/balanced/strong), stable Cursor aliases, optional local slug catalog, provider-mode runbook; orthogonal to TOKEN_PROFILE (9 ACs) (release **2026-06-16T00:00:00Z** / `handoffs/releases/S0091-release-notes.md`, queue **`S0091`** → **`released`**)
- [x] US-0102: Direct per-phase model slug override and role-based catalog presets — extend US-0101 tier-based selection with `MODEL_<PHASE>=<vendor-slug>` direct override, role-based catalog v2 (po/sa/dev/dev_difficult/qa/security/release), backward compatible 3-tier baseline, `/ask` phase reinforcement, precedence logic, validator extensions, contract tests (10 ACs) (release **2026-06-26T00:00:00Z** / `handoffs/releases/S0092-release-notes.md`, queue **`S0092`** → **`released`**)
- [x] US-0103: AI Decision Ledger + Plan Fidelity policy — append-only JSONL ledger of autonomous AI decisions + plan-fidelity tri-state (strict/relaxed/extended); QA cross-check (8 ACs) (UAT closure: `sprints/S0103/uat.json`, `sprints/S0103/uat.md`, verify-work **2026-06-28T14:00:00+02:00** / `orchestrator_run_id=auto-20260628-03`; release **2026-06-28T15:00:00+02:00** / `handoffs/releases/S0103-release-notes.md`, queue **`S0103`** → **`released`**)
- [x] US-0104: Cross-Model Adversarial Critic — per-phase critic subagent with different model, three-lens evaluation (Challenger/Architect/Subtractor), anti-slop scoring, degraded fallback (8 ACs) (verify-work **2026-06-29** / `orchestrator_run_id=auto-20260628-04`; release **2026-06-29** / `handoffs/releases/S0104-release-notes.md`, queue **`S0104`** → **`released`**)
- [x] US-0105: Sovereign Memory — `docs/engineering/sovereign-memory/` substrate (decisions-log, mistakes, patterns, plan-drift-register JSONL + sprint retrospectives), bounded top-N/top-K char-capped injection via `sovereign_memory_lib.py`, curator retrospective + dedup/mistake-tagging; compose US-0029/US-0080/US-0103 (8 ACs) (verify-work **2026-06-29** / `orchestrator_run_id=auto-20260628-04`; release **2026-06-29** / `handoffs/releases/S0105-release-notes.md`, queue **`S0105`** → **`released`**)
- [x] US-0106: DONE (2026-06-29) per S0106 release — Sovereign Role-Behavior Manifest (verify-work PASS 2026-06-29 / auto-20260628-04; release 2026-06-29 / handoffs/releases/S0106-release-notes.md, queue S0106 → released)
- [x] US-0107: Sovereign Loop Mode (AUTO_SOVEREIGN) — deferral register, drain-generate with PO decision gate, notification dispatch (ntfy|email|hook), convergence hooks via US-0110, US-0109 deferral integration point (8 ACs) (qa **2026-06-29** / `orchestrator_run_id=auto-20260628-04`; release **2026-06-29** / `handoffs/releases/S0107-release-notes.md`, queue **`S0107`** → **`released`**)
- [x] US-0108: Parallel Instance Arbitrage for dev phase — N parallel dev subagents in worktrees, QA picks winner, merge policy, resource guard (8 ACs) (verify-work **2026-06-29** / `orchestrator_run_id=auto-20260628-04`; UAT 8/8 PASS; release **2026-06-29** / `handoffs/releases/S0108-release-notes.md`, queue **`S0108`** → **`released`**)
- [x] US-0109: Self-Healing Deploy Loop — post-deploy smoke probe + bounded retry loop; DEPLOY_DEFERRED on cap exhaustion (9 ACs) (verify-work **2026-06-30** / `orchestrator_run_id=auto-20260628-04`; release **2026-06-30** / `handoffs/releases/S0109-release-notes.md`, queue **`S0109`** → **`released`**)
- [x] US-0110: Goal-Based Convergence Loops — convergence predicate evaluator, goal progress visibility, partial delivery report (8 ACs) — DONE (2026-06-28, S0110)
- [x] US-0111: Release-trigger-driven version changelog derivation — trigger adapter system (GitHub/npm/git tag/manual), version diff, atomic [Unreleased] promotion, sovereign ledger integration; compose with US-0100/US-0103 (12 ACs)
- [x] US-0112: Ship model-catalog example presets on install/upgrade — all eight `.cursor/model-catalog.example*.json` files in installer manifest; missing/upgrade framework delivery; never overwrite `model-catalog.local.json`; runbook + contract tests + parity (8 ACs) (release R0112, 2026-06-30, `handoffs/releases/S0112-release-notes.md`)
- [x] US-0113: Sovereign-loop operator documentation in framework README — per-feature guides (US-0103–US-0112), extended Full scratchpad reference, catalog preservation, framework README parity (8 ACs)
- [x] US-0114: Release & distribution operator documentation in framework README — per-feature guides (US-0111, US-0112, US-0041, US-0062), extended Full scratchpad reference, catalog preservation, framework README parity (8 ACs)
  - [x] US-0115: Integration & observability operator documentation in framework README — per-feature guides (US-0034, US-0084, US-0086, US-0093, US-0096, US-0101, US-0102), extended Full scratchpad reference, catalog preservation, framework README parity (8 ACs)
  - [x] US-0116: Delivery & lifecycle operator documentation in framework README — per-feature guides (US-0092, US-0095, US-0098, US-0099), extended Full scratchpad reference, catalog preservation, framework README parity (8 ACs)
  - [x] US-0117: Phase & role governance operator documentation in framework README — per-feature guides (US-0069–US-0072, US-0075–US-0082, US-0083, US-0085, US-0087–US-0090), extended Full scratchpad reference, catalog preservation, framework README parity (8 ACs)
- [x] US-0118: Work-kind classification + tiered delivery routing per story — deterministic `scripts/work_kind_classify_lib.py` classifier (doc/mini/code), `WORK_KIND_ROUTING` scratchpad flag (default-off), backlog row `work_kind`/`recommended_delivery_mode` fields, `/intake` + `/auto` integration with explicit precedence vs `DELIVERY_MODE`/`AUTO_PHASE_*`, fail-closed reason codes, tests + parity, architecture/runbook docs (12 ACs)
- [x] US-0119: Autonomous-autonomy presets and configurable hard-stop relaxation — `AUTONOMY_PRESET={none|balanced|full}` scratchpad flag with deterministic expansion into twelve per-feature autonomy flags, `AUTONOMY_STOP_POLICY={block|auto_repair_then_block|auto_repair_then_skip}` flag, autonomy stop matrix manifest with YAML companion + validator, twelve per-feature flags wired, bounded auto-repair ledger, backward-compatible default (`AUTONOMY_PRESET=none` = byte-identical pre-US-0119), security-hard gates never softened, operator authority preserved via state.md breadcrumbs, compose (read-only) with US-0092/US-0095/US-0056/US-0068/US-0096/BUG-0007 (13 ACs)
- [x] US-0120: Separate `/closure` phase after `/release` with exclusive Story Closure responsibility — new `.cursor/commands/closure.md` (active + template), DEC-0052 phase→role mapping update, DEC-0082 ultra_lean macro phase update, `/auto` orchestration wiring, release.md step 10–12 removal, closure-verification.md schema + validator, closure isolation evidence + runtime proof, contract tests, backward compat for in-flight stories, architecture/runbook/command docs, compose (read-only) with US-0043/US-0045/US-0040/US-0048/US-0056/US-0096 (12 ACs)

## Bug acceptance (canonical)

Per **`DEC-0061`** §8 / **`US-0079`**: portfolio checkbox rows **`- [ ]` / `- [x]`** per **`BUG-xxxx`**, sorted by id, derived from **`docs/product/backlog.md`** **`## Bug issues (canonical)`** — never the inverse (**`US-0045`** bug family). When no bug issues exist, leave this subsection as narrative stub only (no orphan **`BUG-####`** rows).

- [x] BUG-0001: Template/install payload omits intake gate scripts
- [x] BUG-0002: map-codebase does not write codebase-map in fresh repos
- [x] BUG-0003: Missing scripts still occur on install modes missing/upgrade
- [x] BUG-0004: installer.sh fails in shell path with `set: Illegal option -`
- [x] BUG-0005: `/auto` fails with stale resume target after bug intake
- [x] BUG-0006: `/auto` executes phases without spawning required subagents (UAT closure: `sprints/S0067/uat.json`, `sprints/S0067/uat.md`, verify-work **2026-04-04T08:30:00Z** / `orchestrator_run_id=auto-20260403-03`)
- [x] BUG-0007: intake evidence records asked questions that were never asked (UAT closure: `sprints/S0068/uat.json`, `sprints/S0068/uat.md`, verify-work **2026-04-04T23:45:00Z** / `orchestrator_run_id=auto-20260404-01`; release notes `handoffs/releases/S0068-release-notes.md`, queue **`S0068`** → **`ready`**)
- [x] BUG-0008: Global Linux install fails when installer manifest is CRLF (empty `install_include_paths` parse)
- [x] BUG-0009: its-magic ships its own packaging CI (npm/installer.sh/chocolatey jobs) into generated repos, breaking CI in every created project (UAT closure: `sprints/S0078/uat.json`, `sprints/S0078/uat.md`, verify-work **2026-06-06T16:10:30Z** / `orchestrator_run_id=auto-20260606-02`; release notes `handoffs/releases/S0078-release-notes.md`, queue **`S0078`** → **`released`**)
- [x] BUG-0010: Architecture triad archiver ignores `## US-xxxx` headings — `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS` blocks `/auto` when architecture.md exceeds cap (UAT closure: `sprints/S0079/uat.json`, `sprints/S0079/uat.md`, verify-work **2026-06-06T16:33:28Z** / `orchestrator_run_id=auto-20260606-02`; release notes `handoffs/releases/S0079-release-notes.md`, queue **`S0079`** → **`released`**)
- [x] BUG-0011: Caveman mode missing voice compression rules — `CAVEMAN_MODE=1` does not produce terse replies (US-0089 incomplete delivery) (UAT closure: `sprints/S0080/uat.json`, `sprints/S0080/uat.md`, verify-work **2026-06-06T16:53:00Z** / `orchestrator_run_id=auto-20260606-02`; release notes `handoffs/releases/S0080-release-notes.md`, queue **`S0080`** → **`released`**)
- [x] BUG-0012: `/auto` full_autonomy stops after each story despite native chain (US-0095 regression) (UAT closure: `sprints/S0085/uat.json`, `sprints/S0085/uat.md`, verify-work **2026-06-13T00:15:00Z** / `orchestrator_run_id=auto-20260612-01`; release notes `handoffs/releases/S0085-release-notes.md`, queue **`S0085`** → **`released`**)
- [x] BUG-0013: Scratchpad example stale: template example missing features written to canonical scratchpad
- [x] BUG-0014: Sovereign-loop era features missing from README feature coverage catalog and legacy release_notes.md (UAT closure: `sprints/S-BUG0014/uat.json`, `sprints/S-BUG0014/uat.md`, verify-work **2026-07-03T20:05:00Z** / `orchestrator_run_id=auto-20260703-01`; release notes `handoffs/releases/S-BUG0014-release-notes.md`, queue **`S-BUG0014`** → **`released`**)

Validator (backlog bugs + optional drift vs this section): `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance`.
