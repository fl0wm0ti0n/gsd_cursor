# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- US-0111: Release trigger adapters - multi-source release trigger abstraction (manual, git-push, github-release, npm-publish, file-watch), TriggerContext dataclass, 12/12 contract tests passing, 9 fail-closed reason codes, DEC-0111.
- US-0085 through US-0110: Core framework enhancements including multi-model orchestration, sovereign memory integration, adversarial critics, self-healing deploy, goal convergence loops, and various framework extensions (commits 45065e3-813b867).

## [Released]

### [S0111] - 2026-06-16

#### Added
- **US-0111**: Release trigger adapters - multi-source release trigger abstraction (`scripts/release_trigger_adapters.py`), supporting manual, git-push, github-release, npm-publish, and file-watch sources; TriggerContext dataclass for unified trigger context; `RELEASE_TRIGGER_SOURCES` configuration (default `manual`); 12/12 contract tests passing; 9 fail-closed reason codes (TRIGGER_SOURCE_UNKNOWN, TRIGGER_ENV_VALIDATION_FAILED, TRIGGER_FACTORY_RETURNED_NULL, TRIGGER_GITHUB_WEBHOOK_SECRET_MISMATCH, TRIGGER_NPM_PACKAGE_JSON_MISSING, TRIGGER_FILE_WATCH_POLLING_INTERVAL_INVALID, TRIGGER_GITHUB_API_RATE_LIMITED, TRIGGER_NPM_REGISTRY_UNAVAILABLE, TRIGGER_ADAPTER_FACTORY_EXCEPTION); compose guards preserved (US-0008, US-0040, US-0054, US-0100, US-0103, US-0107, US-0110); runbook documentation with operator recipes; template byte-identical mirrors.
- **DEC-0111**: Release trigger adapters architecture decision record.

#### Verification
- Contract tests: 12/12 passing (`pytest -k "us0111 or release_trigger" -v`)
- Parity scope: `release-trigger-adapters` (2 pairs validated)
- Reason codes: 9 documented with remediation paths

#### Known Issues
- None for this release unit.

### [S0109] - 2026-06-14

#### Added
- **US-0109**: Self-healing deploy with smoke probes - bounded retry loop with post-deploy smoke testing (`scripts/self_healing_deploy_lib.py`); `SMOKE_PROBE_ENABLED` flag (default `no`); max retry cap and delay bounds; 8/8 contract tests passing; 7 fail-closed reason codes; compose with US-0054 (publish guard preserved).
- **DEC-0109**: Self-healing deploy architecture decision record.

### [S0107] - 2026-06-13

#### Added
- **US-0107**: Sovereign loop orchestrator (`scripts/sovereign_loop_lib.py`) - `AUTO_SOVEREIGN` mode with deferral register (`handoffs/sovereign_deferrals.jsonl`), goal tracking in `resume_brief.md`, bounded convergence checks, notification dispatch hooks; 10/10 contract tests passing; 10 fail-closed reason codes; compose with US-0048 (phase isolation), US-0049 (sovereign state boundaries), US-0110 (goal tracking integration).
- **DEC-0107**: Sovereign loop orchestrator architecture decision record.

### [S0104] - 2026-06-12

#### Added
- **US-0104**: Sovereign memory substrate (`scripts/sovereign_memory_lib.py`) - bounded JSONL substrate with dedup (95% similarity threshold), bounded injection, curator retrospective, mistake tracking, plan drift register, decision logs; 10/10 contract tests passing; 7 fail-closed reason codes; compose guards preserved.
- **DEC-0104**: Sovereign memory substrate architecture decision record.

### [S0102] - 2026-06-10

#### Added
- **US-0102**: Per-phase model tier configuration - stable aliases (fast/balanced/strong) with model-tier-validate enforcement, optional local slug catalog, provider-mode runbook with tier resolution, `MODEL_TIER_<phase>` overrides; 10/10 contract tests passing; 7 fail-closed reason codes; compose with US-0069 (phase-role), US-0070 (phase-plan).
- **DEC-0102**: Per-phase model tier configuration architecture decision record.

### [S0101] - 2026-06-09

#### Added
- **US-0101**: Model tier catalog - three-tier structure (cheap/balanced/strong) with per-phase configuration, provider-mode catalog (cursor/codex/anthropic), local slug catalog for offline overrides; 10/10 contract tests passing; 7 fail-closed reason codes.
- **DEC-0101**: Model tier catalog architecture decision record.

### [S0100] - 2026-06-08

#### Added
- **US-0100**: Version-scoped release notes - deterministic per-version release notes generation (`scripts/release_changelog_lib.py`), `[Unreleased]` and `[X.Y.Z]` sections in CHANGELOG.md, work item derivation by version range, operator hints (Run/Connect/Verify), 10/10 contract tests passing.
- **DEC-0100**: Version-scoped release notes architecture decision record.

### [S0092] - 2026-05-25

#### Added
- **US-0092**: Token profiling with cost control - `TOKEN_PROFILE` modes (minimal/balanced/unbounded) with token_budget, max_tokens, rate_limit config; 10/10 contract tests passing.

### [S0091] - 2026-05-24

#### Added
- **US-0091**: Cross-model adversarial critics - `CROSS_MODEL_REVIEW=true` with critic model, review phases, critique findings output; 8/8 contract tests passing.

### [S0087] - 2026-05-21

#### Added
- **US-0087**: Bug issue workflow - `BUG-****` issue handling with bug-intake, bug-fix, bug-release lifecycle; bug_issue_lib.py for bug tracking; 8/8 contract tests passing.

### [S0040] - 2026-05-01

#### Added
- **US-0040**: Release notes per sprint (`handoffs/releases/S****-release-notes.md`) - sprint-structured release notes with gate summary, test results, and verification steps.

### [S0054] - 2026-05-07

#### Added
- **US-0054**: Publish confirmation guard (`scripts/release_promotion_guard.py`) - RELEASE_PROMOTION_GATE (always/never/on-version-bump) requiring explicit confirmation for publish operations.

### [S0008] - 2026-04-01

#### Added
- **US-0008**: Release orchestration (`scripts/release-all.sh`) - unified release script coordinating all release phases.

### [S0110] - 2026-06-15

#### Added
- **US-0110**: Goal convergence loops - `SOVEREIGN_GOAL_MODE={phase_driven,goal_convergence}` with goal_progress, goal_completion_gate, vision-driven goal authoring; 10/10 contract tests passing; 12 fail-closed reason codes; partial delivery report on SOVEREIGN_GOAL_TIMEOUT.
- **DEC-0110**: Goal convergence loops architecture decision record.
