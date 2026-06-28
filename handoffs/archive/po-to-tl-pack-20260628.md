# PO → TL Handoff Pack 2026-06-28

## Sovereign-Loop Batch (US-0103 → US-0111)

**Intake Date**: 2026-06-28
**Stories**: 9 stories (US-0103, US-0104, US-0105, US-0106, US-0107, US-0108, US-0109, US-0110, US-0111)
**Pack Reason**: `handoffs/po_to_tl.md` exceeded `PO_TO_TL_HOT_MAX_LINES=800` during sovereign-loop batch intake
**Triad Verification**: `enforce-triad-hot-surface.py --rollover` → PASS; `--check` → PASS (hot file retained US-0111 acceptance checkbox pointer)

## Batch Composition

### US-0103 — AI Decision Ledger + Plan Fidelity Policy
- **Priority**: P0
- **Status**: OPEN (awaiting /discovery)
- **Summary**: Append-only ledger for autonomous AI decisions (deviations, innovations, constraint relaxations, replans) with strict/relaxed/extended plan fidelity scratchpad flag
- **ACs**: 8
- **Related**: US-0048, US-0069, US-0104, US-0105, US-0107
- **Evidence**: `handoffs/intake_evidence/intake-sovereign-20260627-01.json`

### US-0104 — Cross-Model Adversarial Critic
- **Priority**: P0
- **Status**: OPEN (awaiting /discovery)
- **Summary**: Per-phase critic subagent with different model than phase actor, three adversarial lenses (Challenger/Architect/Subtractor), anti-slop scoring, sovereign ledger integration
- **ACs**: 8
- **Related**: US-0103, US-0105
- **Evidence**: `handoffs/intake_evidence/intake-sovereign-20260627-01.json`

### US-0105 — Sovereign Role Behavior Manifest
- **Priority**: P1
- **Status**: OPEN (awaiting /discovery)
- **Summary**: Per-role objective + inter-role review obligations YAML manifest, cross-role review dispatch, template parity
- **ACs**: 7
- **Related**: US-0103, US-0107
- **Evidence**: `handoffs/intake_evidence/intake-sovereign-20260627-01.json`

### US-0106 — Sovereign Drift Register + Deferral Queue
- **Priority**: P1
- **Status**: OPEN (awaiting /discovery)
- **Summary**: JSONL deferral register with bounded retry + skip-after semantics, deferral reason taxonomy, sovereign ledger link
- **ACs**: 7
- **Related**: US-0103, US-0107, US-0110
- **Evidence**: `handoffs/intake_evidence/intake-sovereign-20260627-01.json`

### US-0107 — Sovereign Drain-Generate Loop
- **Priority**: P1
- **Status**: OPEN (awaiting /discovery)
- **Summary**: When portfolio empty + convergence predicate unmet, PO-loop spawn creates candidate stories from vision + sovereign memory + ledger, operator decision gate per candidate
- **ACs**: 8
- **Related**: US-0103, US-0105, US-0106, US-0110
- **Evidence**: `handoffs/intake_evidence/intake-sovereign-20260627-01.json`

### US-0108 — Parallel Instance Arbitrage (Dev Phase)
- **Priority**: P2
- **Status**: OPEN (awaiting /discovery)
- **Summary**: Spawn N parallel dev subagents in separate worktrees, same story + acceptance set, QA evaluates outputs, select best or request merge; resource guard
- **ACs**: 8
- **Related**: US-0103, US-0104, US-0110
- **Evidence**: `handoffs/intake_evidence/intake-sovereign-20260627-01.json`

### US-0109 — Self-Healing Deploy Loop
- **Priority**: P2
- **Status**: OPEN (awaiting /discovery)
- **Summary**: After /release deploy, run smoke probe, on failure spawn repair subagent with bounded retry, DEPLOY_DEFERRED on cap exhaustion
- **ACs**: 8
- **Related**: US-0103, US-0107, US-0088
- **Evidence**: `handoffs/intake_evidence/intake-sovereign-20260627-01.json`

### US-0110 — Goal-Based Convergence Loops
- **Priority**: P0
- **Status**: OPEN (awaiting /discovery)
- **Summary**: Convergence predicate evaluator (all OPEN stories DONE + 0 deferrals + all cross-reviewer findings resolved + smoke probe green + ledger has no unapproved extensions), goal progress mid-loop progress emission, partial delivery report on timeout
- **ACs**: 8
- **Related**: US-0088, US-0092, US-0095, US-0044, US-0103, US-0107
- **Evidence**: `handoffs/intake_evidence/intake-sovereign-20260627-01.json`

### US-0111 — Release-Trigger-Driven Version Changelog Derivation
- **Priority**: P2
- **Status**: OPEN (awaiting /discovery)
- **Summary**: Extend US-0100 to support multiple release trigger sources (GitHub webhook, npm publish, git tag push, manual /release command), automatic trigger source detection, version diff computation, atomic changelog promotion, sovereign ledger integration
- **ACs**: 12
- **Related**: US-0100, US-0103, US-0008, US-0054
- **Evidence**: `handoffs/intake_evidence/US-0111-intake-20260627.json`

## Delivery Order (Dependency-Driven)

1. **US-0103** (foundation: ledger + fidelity policy — all others depend on audit trail)
2. **US-0105** (role-behavior manifest → defines review obligations for critic)
3. **US-0104** (cross-model critic → uses ledger from US-0103 + manifest from US-0105)
4. **US-0106** (drift register → deferral queue for sovereign loop)
5. **US-0107** (drain-generate → needs ledger + manifest + critic from US-0103/US-0105/US-0104)
6. **US-0110** (convergence loops → terminal condition for sovereign loop)
7. **US-0108** (parallel arbitrage → dev-phase extension, lower priority)
8. **US-0109** (self-healing deploy → post-release extension, lower priority)
9. **US-0111** (release-trigger changelog → standalone extension of US-0100, no sovereign dependencies)

## Risks

- **R1**: Ledger schema evolution — US-0103 ledger must be forward-compatible with US-0104/US-0105/US-0107 write patterns
- **R2**: Critic model selection — US-0104 must deterministically select different model than phase actor; requires model-catalog query
- **R3**: Manifest authoring — US-0105 YAML schema must be stable across US-0106/US-0107 role dispatch
- **R4**: Deferral retry semantics — US-0106 bounded retry + skip-after must not orphan work items
- **R5**: Drain-generate quality — US-0107 PO-loop must produce meaningful candidates, not filler stories
- **R6**: Convergence predicate — US-0110 must be cheap to evaluate (no full backlog parse per iteration)
- **R7**: Parallel resource contention — US-0108 worktree isolation must prevent file conflicts
- **R8**: Self-healing loop scope — US-0109 must bound retry to avoid infinite repair loops
- **R9**: Trigger adapter extensibility — US-0111 adapter pattern must support future trigger sources without code changes

## Next Phase

**`/discovery`** for US-0103 (fresh PO subagent). Recommended to proceed in dependency order. US-0111 can be discovered in parallel (no sovereign dependencies).

## Evidence References

- Intake evidence bundles: `handoffs/intake_evidence/intake-sovereign-20260627-01.json`, `handoffs/intake_evidence/US-0111-intake-20260627.json`
- Sovereign-loop research: `docs/engineering/research.md` R-0088 (Q1–Q5 closed)
- Architecture anchor: `docs/engineering/architecture.md # US-0103..US-0111` (pending discovery)
- Triad verification: `docs/engineering/state.md` intake boundary (pending checkpoint)
