---
description: "its-magic architecture: define approach, risks, and decisions."
---

# /architecture

## Subagents
- tech-lead

## Execution model
- Run `/architecture` in a fresh Tech Lead subagent context.
- After writing outputs, stop and hand off to `/sprint-plan` in a new
  subagent/chat.

## Inputs
- Product vision and acceptance
- Constraints and risks
- `docs/engineering/research.md`

## Outputs (artifacts)
- `docs/engineering/architecture.md`
- `docs/engineering/decisions.md`
- `docs/engineering/state.md`
- `handoffs/po_to_tl.md` (read)
- Optional (when enabled):
  - `docs/engineering/manifests/registry.manifest.yaml`
  - `docs/engineering/manifests/repo.manifest.yaml`
  - `docs/engineering/compatibility-signals.md`
- Optional (when enabled):
  - `docs/engineering/component-scope.md`

## Stop conditions
- Major tradeoff requires a decision
- Unknown feasibility or data migration risk

## Steps
1. Challenge:
   a. If `EARLY_RESEARCH=1` in `.cursor/scratchpad.md`, search for technical references (framework docs, pattern comparisons, benchmarks, security considerations) and persist as an R-xxxx entry in `docs/engineering/research.md` (auto-increment ID, per DEC-0011).
   b. Question design assumptions ("what's the alternative?").
   c. Check for simpler approaches ("can this be simpler?").
   d. Inventory risks for each architectural choice.
2. Define the minimal architecture and key components.
3. Record tradeoffs in decisions log.
4. Update engineering state and readiness.
5. Optional cross-repo observability architecture (US-0034):
   - If `CROSS_REPO_OBSERVABILITY=0`, skip this step (zero required overhead).
   - If `CROSS_REPO_OBSERVABILITY=1`, define monitored sources, manifest contract
     boundaries, compatibility signal taxonomy, and critical-gate policy
     (`COMPATIBILITY_GATE_ON_CRITICAL`) in architecture/decision artifacts.
6. Optional component-scope architecture (US-0035):
   - If `COMPONENT_SCOPE_MODE=0`, skip this step (zero required overhead).
   - If `COMPONENT_SCOPE_MODE=1`, define scoped-mode constraints in
     `docs/engineering/component-scope.md`:
     - `target_components[]`
     - `non_target_components[]`
     - `allowed_interface_touch[]`
     - escalation policy for out-of-scope impact.
7. Optional spec-pack (US-0031):
   - If `SPEC_PACK_MODE=0`, add no required spec-pack steps (zero overhead).
   - If `SPEC_PACK_MODE=1`, create or update Design Concept and Technical
     Specification at canonical paths per runbook spec-pack contract; link story
     ID in architecture/state.
8. Optional user-guide (US-0032):
   - If `USER_GUIDE_MODE=0`, add no required user-guide steps or blocking checks (zero overhead).
   - If `USER_GUIDE_MODE=1`, reference canonical user-guide path and schema in
     architecture/state for in-scope feature stories; see runbook user-guide section.

