# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- semver-sections-newest-first -->

## [Unreleased]

### Added

- **US-0107** — Sovereign loop mode (AUTO_SOVEREIGN) — default-off `AUTO_SOVEREIGN` scratchpad gate (nine keys + notify config); `handoffs/sovereign_deferrals.jsonl` bounded deferral register; `scripts/sovereign_loop_lib.py` advance algorithm + drain-generate spawn inputs with mandatory per-candidate decision gate; fail-open ntfy/hook notification dispatch (email deferred v1); US-0110 convergence compose via `list_open_deferrals`; US-0109 `DEPLOY_DEFERRED` integration declaration; ten `test_us0107_*` contract tests (8 core + 2 compose guards); parity `--scope=sovereign-loop`; 12 reason codes; runbook § Sovereign Loop Mode (**DEC-0107**).
- **US-0105** — Sovereign memory — default-off `SOVEREIGN_MEMORY` scratchpad gate (five keys including `SOVEREIGN_MEMORY_JSONL_MAX_LINES`); `docs/engineering/sovereign-memory/` JSONL substrate (decisions-log, mistakes, patterns, plan-drift-register + sprint retrospectives); bounded top-N/top-K char-capped injection via `scripts/sovereign_memory_lib.py`; phase spawn `sovereign_memory_digest` hook; curator `/refresh-context` retrospective + optional ledger promotion; decision dedup + mistake-tagging hooks; ten `test_us0105_*` contract tests (8 core + 2 compose guards); parity `--scope=sovereign-memory`; 8 reason codes; runbook § Sovereign Memory (**DEC-0105**).
- **US-0104** — Cross-model adversarial critic — default-off `CROSS_MODEL_REVIEW` scratchpad gate; `/sovereign-critic` per-phase critic spawn with tier-opposition model selection; three-lens evaluation (Challenger/Architect/Subtractor) + parallel-jury reconciliation via `scripts/sovereign_critic_lib.py`; `handoffs/sovereign_critic_findings.jsonl` 15-field schema; anti-slop scoring + bounded rework loop; degraded single-model-multi-lens fallback; isolation evidence `model_id` v2 additive extension; ten `test_us0104_*` contract tests (8 core + 2 compose guards); parity `--scope=sovereign-critic`; 10 reason codes; runbook § Cross-Model Adversarial Critic (**DEC-0104**).
- **US-0110** — Goal-based convergence loops — `SOVEREIGN_GOAL_MODE=phase_driven|goal_convergence` scratchpad keys (default-off zero overhead); `scripts/sovereign_convergence_lib.py` five-conjunct `evaluate_convergence` predicate with degrade matrix and memoization; vision auto-derive goal authoring; curator `/refresh-context` `goal_progress` block in `resume_brief.md`; `SOVEREIGN_GOAL_TIMEOUT` partial-delivery report; eight `test_us0110_*` contract tests; parity `--scope=sovereign-convergence`; 10 reason codes; runbook § Goal-Based Convergence (**DEC-0110**).
- **US-0040** — Replace single-file release note behavior with per-sprint release note artifacts and add a canonical release queue tracker that records each sprint's release...
- **US-0100** — **Architecture + decision (AC-10)** — **`DEC-0085`** + architecture **`# US-0100`**.
- **US-0101** — Per-phase model tier selection for subagents — `MODEL_TIER` scratchpad (`cheap|balanced|strong`), stable Cursor aliases (`fast`/`inherit`/omit), optional local slug catalog, provider-mode runbook; orthogonal to `TOKEN_PROFILE` (DEC-0086).
- **US-0102** — Direct per-phase model slug override and role-based catalog presets — `MODEL_<PHASE>` direct override, catalog schema v2 role presets, 5-step precedence chain, backward compatible with US-0101 tier baseline (DEC-0087).
