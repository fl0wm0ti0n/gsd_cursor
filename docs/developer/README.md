# Developer documentation

This shard holds contributor-facing material for the **its-magic** framework. End-user
setup stays in the root `README.md` (user channel).

## Prerequisites

- **Cursor** (or compatible editor) with the workflow files installed.
- **Python 3** on PATH for scratchpad merge validation and several repo scripts.
- **Node.js** if you use npm-packaged `its-magic` or npm-driven `TEST_COMMAND` defaults.

## Workflow

- Follow phased commands under `.cursor/commands/` (`intake`, `discovery`, `architecture`,
  `sprint-plan`, `execute`, `qa`, `release`, etc.).
- Keep handoffs and `docs/engineering/state.md` updated at phase boundaries.
- Use `.cursor/scratchpad.local.md` for personal overrides; never commit secrets.

<!-- readme-feature-coverage-catalog -->

### Feature coverage catalog (US-0091)

- **BUG-0011** — Caveman mode missing voice compression rules (US-0089 incomplete delivery); traceability: `/scratchpad`, see `docs/engineering/architecture.md`.
- **US-0020** — /ask Command: Context-Aware Questions Without Workflow; traceability: `/ask`, see `docs/engineering/architecture.md`.
- **US-0022** — Sprint Sizing Rules and Configurable Sprint Planning; traceability: `/sprint-plan`, see `docs/engineering/architecture.md`.
- **US-0023** — Fresh Subagent Context Per Phase and /auto Orchestration; traceability: `/auto`, see `docs/engineering/architecture.md`.
- **US-0069** — Strict Phase Role Enforcement in /auto Orchestration; traceability: `/auto`, see `docs/engineering/architecture.md`.
- **US-0070** — Configurable Auto Phase Selection Policy; traceability: `/auto`, see `docs/engineering/architecture.md`.

## Quality gates

- Run `TEST_COMMAND` from `docs/engineering/runbook.md` before push; CI should mirror the same.
- Run `python scripts/validate_doc_profile.py` when changing documentation profile flags or
  README surfaces.
- Observe `US-0071` hygiene for user-visible script output (see runbook).

<!-- readme-feature-coverage-catalog -->

### Feature coverage catalog (US-0091)

- **BUG-0002** — map-codebase does not write codebase-map in fresh repos; traceability: `/map-codebase`, see `docs/engineering/architecture.md`.
- **BUG-0005** — `/auto` fails with stale resume target after bug intake; traceability: `/auto`, see `docs/engineering/architecture.md`.
- **BUG-0006** — `/auto` executes phases without spawning required subagents; traceability: `/auto`, see `docs/engineering/architecture.md`.
- **BUG-0007** — intake evidence records asked questions that were never asked; traceability: `/intake`, see `docs/engineering/architecture.md`.
- **BUG-0010** — Architecture triad archiver ignores `## US-xxxx` headings, blocking `/auto` with `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS`; traceability: `/auto`, see `docs/engineering/architecture.md`.
- **US-0001** — Core Workflow Commands; traceability: `US-0001`, see `docs/engineering/architecture.md`.
- **US-0002** — AI Behavior Rules; traceability: `US-0002`, see `docs/engineering/architecture.md`.
- **US-0003** — Subagent Definitions; traceability: `US-0003`, see `docs/engineering/architecture.md`.
- **US-0004** — Skill and Templates; traceability: `SKILL`, see `docs/engineering/architecture.md`.
- **US-0005** — Hook System; traceability: `US-0005`, see `docs/engineering/architecture.md`.
- **US-0006** — Artifact Templates and Starter Docs; traceability: `/write`, see `docs/engineering/architecture.md`.
- **US-0008** — CLI Installer; traceability: `US-0008`, see `docs/engineering/architecture.md`.
- **US-0010** — Voice Input Documentation; traceability: `README`, see `docs/engineering/architecture.md`.
- **US-0011** — Automation Modes; traceability: `AUTO_FLOW_MODE`, see `docs/engineering/architecture.md`.
- **US-0012** — Benchmark Suite; traceability: `US-0012`, see `docs/engineering/architecture.md`.
- **US-0013** — Team Mode; traceability: `TEAM_MODE`, see `docs/engineering/architecture.md`.
- **US-0014** — Quality Chain (3-Layer); traceability: `US-0014`, see `docs/engineering/architecture.md`.
- **US-0015** — Runbook Completion; traceability: `/installer`, see `docs/engineering/architecture.md`.
- **US-0017** — Template Drift Guard; traceability: `US-0017`, see `docs/engineering/architecture.md`.
- **US-0019** — Clean Placeholder Content from Templates and Active Files; traceability: `/strings`, see `docs/engineering/architecture.md`.
- **US-0021** — Critical Evaluation in Intake and Architecture; traceability: `/intake`, see `docs/engineering/architecture.md`.
- **US-0024** — Memory Drift Audit Command; traceability: `/memory-audit`, see `docs/engineering/architecture.md`.
- **US-0025** — Backlog-to-Sprint Traceability Contract; traceability: `/evidence`, see `docs/engineering/architecture.md`.
- **US-0026** — Milestone Lifecycle Definition and Exit Criteria; traceability: `/exit`, see `docs/engineering/architecture.md`.
- **US-0027** — UAT Artifact Lifecycle and Ownership; traceability: `/uat`, see `docs/engineering/architecture.md`.
- **US-0028** — Security & Compliance Review Agent; traceability: `/security-review`, see `docs/engineering/architecture.md`.
- **US-0029** — Knowledge Curation & Early Research; traceability: `/research`, see `docs/engineering/architecture.md`.
- **US-0030** — Release Gate for Command/Flag Documentation Delta; traceability: `/flag`, see `docs/engineering/architecture.md`.
- **US-0031** — Optional Documentation Pack (Design Concept, CRS, Technical Spec); traceability: `/check`, see `docs/engineering/architecture.md`.
- **US-0032** — Optional Feature User Guide Generation; traceability: `/story`, see `docs/engineering/architecture.md`.
- **US-0033** — Configurable Guided Intake Behavior; traceability: `/intake`, see `docs/engineering/architecture.md`.
- **US-0034** — Multi-Repo and Contract Compatibility Observability; traceability: `/intake`, see `docs/engineering/architecture.md`.
- **US-0035** — Component-Scoped Execution Mode with Protection Guards; traceability: `/intake`, see `docs/engineering/architecture.md`.
- **US-0036** — Official Remote Config Template, Docs, and Fail-Fast Validation; traceability: `/field`, see `docs/engineering/architecture.md`.
- **US-0037** — Mid-Process `/auto` Continuation with Deterministic Resume Point; traceability: `/auto`, see `docs/engineering/architecture.md`.
- **US-0038** — Phase-Triggered Sync Policy with Guarded Auto-Push; traceability: `/push`, see `docs/engineering/architecture.md`.
- **US-0039** — Release Gate Tightening for Check-In Tests and QA/UAT Completion; traceability: `/release`, see `docs/engineering/architecture.md`.
- **US-0040** — Per-Sprint Release Notes and Release Queue Tracker; traceability: `/release`, see `docs/engineering/architecture.md`.
- **US-0042** — Release Findings Artifact and Post-QA Issue Workflow; traceability: `/release`, see `docs/engineering/architecture.md`.
- **US-0043** — Backlog Reconciliation Gate for Released Sprints; traceability: `/product`, see `docs/engineering/architecture.md`.
- **US-0044** — Continuous `/auto` Backlog-Drain Mode with Fine-Tune Switches; traceability: `/auto`, see `docs/engineering/architecture.md`.
- **US-0045** — Canonical Story Status Source + Global Drift Guard; traceability: `/product`, see `docs/engineering/architecture.md`.
- **US-0046** — Explicit `/sprint-plan --bulk` Mode; traceability: `/sprint-plan`, see `docs/engineering/architecture.md`.
- **US-0047** — Explicit Bulk Execute Orchestration Mode; traceability: `/skip`, see `docs/engineering/architecture.md`.
- **US-0048** — Enforced Per-Phase Subagent Isolation with Audit Gate; traceability: `/release`, see `docs/engineering/architecture.md`.
- **US-0049** — Legacy DONE-Story Acceptance/Traceability Backfill Guard; traceability: `/release`, see `docs/engineering/architecture.md`.
- **US-0050** — Clean Install Hygiene and Complete Clean-Repo Coverage; traceability: `/product`, see `docs/engineering/architecture.md`.
- **US-0051** — Intelligent Intake Decomposition and Risk-Aware PO Questioning; traceability: `/risk`, see `docs/engineering/architecture.md`.
- **US-0052** — Optional Fresh-Project ID Namespace Bootstrap; traceability: `/decision`, see `docs/engineering/architecture.md`.
- **US-0053** — Context Compaction and Tiered Token-Cost Optimization Mode; traceability: `/ask`, see `docs/engineering/architecture.md`.
- **US-0055** — Deterministic Status Reconciliation Command; traceability: `/derived`, see `docs/engineering/architecture.md`.
- **US-0056** — Strict Runtime Proof for Per-Phase Subagent Isolation; traceability: `/auto`, see `docs/engineering/architecture.md`.
- **US-0057** — Upgrade-Safe Scratchpad Example Refresh and Parity; traceability: `/scratchpad`, see `docs/engineering/architecture.md`.
- **US-0058** — Deterministic Artifact Ordering and Write Discipline; traceability: `/order`, see `docs/engineering/architecture.md`.
- **US-0059** — Deterministic Intake Runtime Capability Guard and Single-Writer Drift Safety; traceability: `/intake`, see `docs/engineering/architecture.md`.
- **US-0060** — Deterministic State Hot-Surface Rollover and Archive Enforcement; traceability: `/engineering`, see `docs/engineering/architecture.md`.
- **US-0061** — Cross-Phase Artifact Ownership Guard and Deterministic Archive Control; traceability: `/phases`, see `docs/engineering/architecture.md`.
- **US-0062** — Installer-Owned `its_magic/` Folder for Framework Metadata; traceability: `/docs`, see `docs/engineering/architecture.md`.
- **US-0063** — OS-Aware Runbook Command Auto-Bootstrap with Verified Quality Gates; traceability: `/engineering`, see `docs/engineering/architecture.md`.
- **US-0065** — Runtime QA Autopilot for Generated Projects; traceability: `/managed`, see `docs/engineering/architecture.md`.
- **US-0066** — Generated Test Scaffolding and Auto-Run Contract; traceability: `/integration`, see `docs/engineering/architecture.md`.
- **US-0067** — Release Operator Run/Connect/Verify Hints Contract; traceability: `/connectivity`, see `docs/engineering/architecture.md`.
- **US-0068** — Mandatory Intake Question Packs for First and Small Intakes; traceability: `/acceptance`, see `docs/engineering/architecture.md`.
- **US-0071** — User-Visible Internal Metadata Sanitization Guard; traceability: `/planning`, see `docs/engineering/architecture.md`.
- **US-0072** — Deterministic Context Slimming and Archive Enforcement Across Core Artifacts; traceability: `/engineering`, see `docs/engineering/architecture.md`.
- **US-0073** — Scratchpad Delivery Simplification (Example-Only Install Policy); traceability: `/scratchpad`, see `docs/engineering/architecture.md`.
- **US-0075** — Upgrade Scratchpad Example–First Refresh (Fix Example Drift vs Materialized Baseline); traceability: `/scratchpad`, see `docs/engineering/architecture.md`.
- **US-0076** — Executable Scratchpad-Driven Sync and Auto-Push Wiring; traceability: `/scratchpad`, see `docs/engineering/architecture.md`.
- **US-0077** — Documentation Audience Profiles and Dual README Strategy; traceability: `/developer-dense`, see `docs/engineering/architecture.md`.
- **US-0078** — Enforced Interactive Intake Question Evidence; traceability: `/confirmation`, see `docs/engineering/architecture.md`.
- **US-0080** — Token-Cost Hardening for Orchestrated Runs; traceability: `/auto`, see `docs/engineering/architecture.md`.
- **US-0081** — First-Intake Full-Plan Coverage and Story-Map Gate; traceability: `/new`, see `docs/engineering/architecture.md`.
- **US-0083** — Delegable Intake Clarification Without Hard Blocks; traceability: `/repetitive`, see `docs/engineering/architecture.md`.
- **US-0085** — Gitignored `.env` for remote and release connectivity (no AI read); traceability: `/remote`, see `docs/engineering/architecture.md`.
- **US-0086** — Automation-driven remote execution selection (Docker / SSH / NL container intent); traceability: `/remote`, see `docs/engineering/architecture.md`.
- **US-0087** — `/auto` explicit bug targeting (fix all OPEN bugs / fix `BUG-####`); traceability: `/auto`, see `docs/engineering/architecture.md`.
- **US-0088** — `/auto` continuous multi-phase loop + quiet drain (close one-phase-stop gap); traceability: `/auto`, see `docs/engineering/architecture.md`.
- **US-0093** — Cursor browser-integrated UAT self-test (browser_smoke + automatable manual UI); traceability: `/uat`, see `docs/engineering/architecture.md`.

## Architecture notes

- High-level contracts live in `docs/engineering/architecture.md` (search for story ids).
- Installer ownership is driven by `docs/engineering/context/installer-owned-paths.manifest`.
- Template parity: changes in repo root often require the same edit under `template/`.

<!-- readme-feature-coverage-catalog -->

### Feature coverage catalog (US-0091)

- **BUG-0001** — Template/install payload omits intake gate scripts; traceability: `/install`, see `docs/engineering/architecture.md`.
- **BUG-0003** — Missing scripts still occur on install modes missing/upgrade; traceability: `/upgrade`, see `docs/engineering/architecture.md`.
- **BUG-0004** — installer.sh fails in shell path with `set: Illegal option -`; traceability: `/workdir`, see `docs/engineering/architecture.md`.
- **BUG-0008** — Global Linux install fails: empty `install_include_paths` when manifest is CRLF; traceability: `/usr`, see `docs/engineering/architecture.md`.
- **BUG-0009** — its-magic ships its OWN packaging CI into generated repos, breaking CI in every created project; traceability: `/installed`, see `docs/engineering/architecture.md`.
- **US-0007** — CI/CD Workflows; traceability: `/lint`, see `docs/engineering/architecture.md`.
- **US-0009** — Multiplatform Distribution; traceability: `/push`, see `docs/engineering/architecture.md`.
- **US-0016** — Homebrew Version Sync; traceability: `US-0016`, see `docs/engineering/architecture.md`.
- **US-0018** — Smart Upgrade Mode; traceability: `MIGRATION`, see `docs/engineering/architecture.md`.
- **US-0041** — End-to-End Lifecycle QA for `its-magic` Install/Upgrade/Clean; traceability: `/template`, see `docs/engineering/architecture.md`.
- **US-0054** — Configurable Multi-Target Release Publish with Confirmation Gate; traceability: `/choco`, see `docs/engineering/architecture.md`.
- **US-0064** — Remote Runtime Connectivity Contract for QA/Release/Publish; traceability: `/engineering`, see `docs/engineering/architecture.md`.
- **US-0074** — Baseline Regression Cleanup for Installer and Version Sync Checks; traceability: `/run-tests`, see `docs/engineering/architecture.md`.
- **US-0079** — First-Class Bug Issue Workflow (Open/Closed); traceability: `/devops`, see `docs/engineering/architecture.md`.
- **US-0082** — Agent-Driven Codebase Map Bootstrap; traceability: `/engineering`, see `docs/engineering/architecture.md`.
- **US-0084** — POSIX npm installer + Linux remote test targets (WSL / SSH / Docker); traceability: `/bin`, see `docs/engineering/architecture.md`.
- **US-0089** — Cursor Caveman mode (scratchpad-configurable terse responses); traceability: `/or`, see `docs/engineering/architecture.md`.
- **US-0090** — Optional Caveman-style input compression (safe file scope); traceability: `/intake`, see `docs/engineering/architecture.md`.
- **US-0091** — README ↔ backlog/acceptance feature coverage backfill + blocking drift gate; traceability: `/acceptance`, see `docs/engineering/architecture.md`.
- **US-0094** — README visionary intro + tiered feature hierarchy (root/template parity); traceability: `README.md`, see `docs/engineering/architecture.md`.
- **US-0092** — Full-autonomy `/auto` mode + outer driver + self-verification; traceability: `/auto`, see `docs/engineering/architecture.md`.

## Contracts and interfaces

- Scratchpad merge precedence: local → materialized `.cursor/scratchpad.md` →
  `.cursor/scratchpad.local.example.md` (Model B / **DEC-0055**).
- Documentation profile keys: `DOC_AUDIENCE_PROFILE`, `DOC_DETAIL_LEVEL` (**DEC-0059**).
- Optional modes: `SPEC_PACK_MODE`, `USER_GUIDE_MODE` remain orthogonal; when `0`, validators
  must not require those artifacts.

## Engineering decisions

- Decision records: `decisions/DEC-xxxx.md` and the compact index in
  `docs/engineering/decisions.md`.
- Profile semantics for this shard: **DEC-0059** and `# US-0077` in `architecture.md`.
