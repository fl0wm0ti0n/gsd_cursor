#!/usr/bin/env python3
"""Insert sovereign-loop era documentation into its_magic/README.md"""

with open('its_magic/README.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find insertion point - after the sovereign-loop catalog entries (around line 1177)
insert_idx = None
for i, line in enumerate(lines):
    if '## Other useful capabilities' in line:
        insert_idx = i
        break

if insert_idx is None:
    print("ERROR: Could not find insertion point")
    exit(1)

sovereign_docs = """
## Sovereign-Loop Era Features (Default Off, Opt-In)

The sovereign-loop era features enable AI agents to operate with increased autonomy, persistent learning, multi-model validation, and self-healing capabilities. All features are **disabled by default** (zero overhead when off) and can be individually enabled via scratchpad configuration.

---

### US-0103: AI Decision Ledger & Plan Fidelity Policy

**What it is:**
A structured audit trail that logs every autonomous AI decision with context (situation), rationale (why), alternatives considered, and outcome. Tracks plan adherence with three fidelity modes.

**Why use it:**
- **Transparency:** See exactly what decisions the AI made and why
- **Accountability:** Maintain audit trail for compliance/regulatory needs
- **Learning:** Review past decisions to improve future AI behavior
- **Trust:** Build confidence in autonomous AI actions

**When to enable:**
- Development projects requiring decision auditability
- Team environments where AI actions need review
- Compliance/regulatory scenarios
- Experimentation phases where you want to understand AI reasoning

**How to enable:**
```markdown
# .cursor/scratchpad.local.md
AI_DECISION_LEDGER=1          # Enable decision logging (default: 0)
AUTO_PLAN_FIDELITY=relaxed    # Plan adherence: strict|relaxed|extended (default: relaxed)
```

**Key flags:**
- `AI_DECISION_LEDGER=0|1` — Master enable/disable
- `AUTO_PLAN_FIDELITY=strict|relaxed|extended`
  - `strict`: Must follow plan exactly; deviations require explicit approval
  - `relaxed`: Can deviate with documented rationale (recommended default)
  - `extended`: Can extend plan with new tasks, logged as additions

**Storage:** `docs/engineering/decision-ledger.jsonl` (JSON Lines format)

**What gets logged:**
Each entry: decision_id, situation (context), rationale (why), alternatives[], outcome

**Overhead:** ~10 lines/decision; zero when `AI_DECISION_LEDGER=0`

**Deep dive:** `docs/engineering/runbook.md` § AI Decision Ledger

---

### US-0104: Cross-Model Adversarial Critic

**What it is:**
For each major decision, spawns a separate AI model (or same model with different prompt) to challenge/critique the primary response. Compares outputs and reconciles differences.

**Why use it:**
- **Quality assurance:** Catch errors/biases single-model might miss
- **Robustness:** Multiple perspectives reduce hallucination risk
- **Validation:** Independent verification of reasoning
- **Learning:** Improve model selection based on performance

**When to enable:**
- High-stakes architectural decisions
- Compliance/regulatory code
- Learning/experimentation phases
- Any scenario where single-model trust is insufficient

**How to enable:**
```markdown
# .cursor/scratchpad.local.md
CROSS_MODEL_REVEIW=1                        # Enable cross-model review (default: 0)
CROSS_MODEL_REVIEW_MODE=adversarial         # Review mode: adversarial|consultative (default: adversarial)
CROSS_MODEL_REVIEW_MIN_AGREEMENT=0.6        # Min agreement threshold 0.0-1.0 (default: 0.6)
```

**Key flags:**
- `CROSS_MODEL_REVIEW=0|1` — Master enable/disable
- `CROSS_MODEL_REVIEW_MODE=adversarial|consultative`
  - `adversarial`: Models actively challenge each other (more rigorous)
  - `consultative`: Models provide independent opinions (less confrontational)
- `CROSS_MODEL_REVIEW_MIN_AGREEMENT=0.0-1.0` — Agreement threshold
  - Below threshold → `DECISION_GATE` blocks progression
  - Higher values = more agreement required (slower but more rigorous)

**How it works:**
1. Primary model generates decision
2. Critic model reviews/challenges (different model or adversarial prompt)
3. Comparison engine measures agreement (semantic similarity + key-point overlap)
4. If agreement < threshold → `DECISION_GATE` blocks until operator review

**Storage:** `docs/engineering/cross-model-reviews/` (per-decision review files)

**Overhead:** 2x API calls perdecision; zero when `CROSS_MODEL_REVIEW=0`

**Deep dive:** `docs/engineering/runbook.md` § Cross-Model Adversarial Critic

---

### US-0105: Sovereign Memory

**What it is:**
Persistent institutional memory stored in `docs/engineering/sovereign-memory/`. Tracks decisions, mistakes, and patterns across sessions. Injects relevant learnings into AI context at startup.

**Why use it:**
- **Learning from mistakes:** Avoid repeating past errors
- **Pattern recognition:** Identify recurring issues and successes
- **Context richness:** Provide historical perspective to AI decisions
- **Knowledge preservation:** Retain learnings across sessions/repos

**When to enable:**
- Long-running projects with iterative development
- Teams wanting to capture institutional knowledge
- Scenarios where learning from past mistakes is valuable
- Multi-session workflows where context loss is problematic

**How to enable:**
```markdown
# .cursor/scratchpad.local.md
SOVEREIGN_MEMORY=1                    # Enable sovereign memory (default: 0)
SOVEREIGN_MEMORY_TOP_N=5              # Recent N decisions to inject (default: 5)
SOVEREIGN_MEMORY_TOP_K=3              # High-impact patterns to inject (default: 3)
SOVEREIGN_MEMORY_MAX_CHARS=2048       # Max chars per injection (default: 2048)
SOVEREIGN_MEMORY_JSONL_MAX_LINES=500  # Max lines before rollover (default: 500)
```

**Key flags:**
- `SOVEREIGN_MEMORY=0|1` — Master enable/disable
- `SOVEREIGN_MEMORY_TOP_N=1-20` — How many recent decisions to remember
- `SOVEREIGN_MEMORY_TOP_K=0-10` — How many high-impact patterns to inject
- `SOVEREIGN_MEMORY_MAX_CHARS=256-4096` — Character budget per injection
- `SOVEREIGN_MEMORY_JSONL_MAX_LINES=100-1000` — Rollover threshold

**Storage:**
- `docs/engineering/sovereign-memory/decisions.jsonl` — Decision log
- `docs/engineering/sovereign-memory/mistakes.jsonl` — Mistake catalog
- `docs/engineering/sovereign-memory/patterns.jsonl` — Pattern recognition
- `docs/engineering/sovereign-memory/plan-drift-register.jsonl` — Plan deviations
- `docs/engineering/sovereign-memory/retrospectives/` — Sprint retrospectives

**What gets logged:**
- **Decisions:** Major choices with context/rationale
- **Mistakes:** Failed approaches with lessons learned
- **Patterns:** Recurring issues/successes across sessions
- **Plan drift:** When execution deviates from plan
- **Retrospectives:** End-of-sprint learning summaries

**Overhead:** ~5 lines/entry; zero when `SOVEREIGN_MEMORY=0`

**Deep dive:** `docs/engineering/runbook.md` § Sovereign Memory

---

### US-0108: Parallel Instance Arbitrage

**What it is:**
During `/execute`, spawns N parallel AI instances (worktrees) working independently on the same task. After execution, uses multi-model consensus voting to select the best result.

**Why use it:**
- **Quality:** Multiple approaches increase chance of best solution
- **Robustness:** Catches errors single instance might miss
- **Speed:** Parallel execution can be faster than sequential trial-and-error
- **Learning:** Compare different approaches to identify best patterns

**When to enable:**
- High-stakes executions where quality is critical
- Complex tasks where multiple approaches are viable
- Parallelizable workloads (multiple files/modules)
- Experimentation with different AI strategies

**How to enable:**
```markdown
# .cursor/scratchpad.local.md
SOVEREIGN_PARALLEL_DEV=1                    # Enable parallel arbitrage (default: 0)
AUTO_SOVEREIGN_PARALLEL_N=5                 # Parallel instances (default: 5)
AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL=10        # Max total in flight (default: 10)
AUTO_SOVEREIGN_PARALLEL_QA=1                # Enable parallel QA (default: 1)
AUTO_SOVEREIGN_MERGE_RESOLVE=median         # Merge strategy: median|weighted|conservative (default: median)
```

**Key flags:**
- `SOVEREIGN_PARALLEL_DEV=0|1` — Master enable/disable
- `AUTO_SOVEREIGN_PARALLEL_N=2-10` — Number of parallel instances
- `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL=5-20` — Max concurrent instances
- `AUTO_SOVEREIGN_PARALLEL_QA=0|1` — Enable parallel QA validation
- `AUTO_SOVEREIGN_MERGE_RESOLVE=median|weighted|conservative` — Result selection strategy

**How it works:**
1. Spawns N independent AI instances in separate worktrees
2. Each instance works autonomously on the same task
3. After all complete, multi-model consensus voting selects best result
4. Winner is merged; others are discarded (worktrees cleaned up)

**Storage:** `docs/engineering/parallel-arbitrage/` (per-execution logs)

**Overhead:** Nx resource usage; zero when `SOVEREIGN_PARALLEL_DEV=0`

**Deep dive:** `docs/engineering/runbook.md` § Parallel Instance Arbitrage

---

### US-0107: Self-Healing Deploy Loop

**What it is:**
After `/release`, automatically probes deployment health. If issues detected, attempts bounded retry with different configurations (model, parameters, approach). Tracks deployment confidence over time.

**Why use it:**
- **Reliability:** Auto-recover from transient deployment failures
- **Confidence:** Build trust in deployment process
- **Learning:** Track what configurations work best
- **Reduced toil:** Less manual intervention for common issues

**When to enable:**
- Automated deployment pipelines
- High-frequency release cycles
- Scenarios where deployment failures are common
- Teams wanting self-healing infrastructure

**How to enable:**
```markdown
# .cursor/scratchpad.local.md
AUTO_SOVEREIGN_SELF_HEALING_DEPLOY=1        # Enable self-healing (default: 0)
AUTO_SOVEREIGN_DEPLOY_RETRY_MAX=3           # Max retry attempts (default: 3)
AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC=30  # Health check timeout (default: 30)
AUTO_SOVEREIGN_DEPLOY_PROBE_KIND=acceptance_smoke  # Probe type (default: acceptance_smoke)
SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH=smoke-tests/  # Test path (default: smoke-tests/)
AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT=http://localhost:8080/health  # Health URL (default: localhost:8080/health)
```

**Key flags:**
- `AUTO_SOVEREIGN_SELF_HEALING_DEPLOY=0|1` — Master enable/disable
- `AUTO_SOVEREIGN_DEPLOY_RETRY_MAX=1-10` — Max retry attempts
- `AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC=10-300` — Health check timeout
- `AUTO_SOVEREIGN_DEPLOY_PROBE_KIND=acceptance_smoke|health_endpoint` — Probe strategy
- `SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH` — Path to smoke tests
- `AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT` — Health check URL

**How it works:**
1. After `/release`, probes health endpoint or runs smoke tests
2. If healthy → deployment success
3. If unhealthy → retries with different config (up to `RETRY_MAX`)
4. Exhausts retries → `DEPLOY_DEFERRED` (manual intervention required)

**Storage:** `docs/engineering/deploy-health/` (per-deployment logs)

**Overhead:** ~30 sec/probe; zero when `AUTO_SOVEREIGN_SELF_HEALING_DEPLOY=0`

**Deep dive:** `docs/engineering/runbook.md` § Self-Healing Deploy

---

### US-0110: Goal Convergence

**What it is:**
Tracks convergence toward explicit goals over time. Measures goal progress, detects stagnation/oscillation, and can halt when convergence criteria met.

**Why use it:**
- **Goal alignment:** Ensure execution is actually achieving stated goals
- **Stagnation detection:** Identify when progress has stalled
- **Oscillation prevention:** Stop when bouncing between states without progress
- **Success criteria:** Define when "good enough" has been achieved

**When to enable:**
- Long-running iterative processes
- Goal-driven development workflows
- Scenarios where "done" is subjective
- Multi-phase workflows with convergence criteria

**How to enable:**
```markdown
# .cursor/scratchpad.local.md
SOVEREIGN_GOAL_MODE=goal_convergence        # Goal mode: phase_driven|goal_convergence (default: phase_driven)
SOVEREIGN_GOAL=Increase code coverage to 80%  # Explicit goal (default: empty = auto-derive)
SOVEREIGN_GOAL_TOP_N=3                      # Vision paragraphs for auto-derive (default: 3)
SOVEREIGN_GOAL_MAX_CHARS=512                # Goal char limit (default: 512)
SOVEREIGN_GOAL_TIMEOUT_MAX=3                # Iteration cap (0=disabled) (default: 0)
```

**Key flags:**
- `SOVEREIGN_GOAL_MODE=phase_driven|goal_convergence`
  - `phase_driven`: Standard phase-based execution (default)
  - `goal_convergence`: Track toward explicit goal
- `SOVEREIGN_GOAL` — Explicit goal text (empty = auto-derive from vision)
- `SOVEREIGN_GOAL_TOP_N=1-10` — How many vision paragraphs to use (when auto-deriving)
- `SOVEREIGN_GOAL_MAX_CHARS=64-1024` — Goal text char limit
- `SOVEREIGN_GOAL_TIMEOUT_MAX=0-100` — Iteration cap (0 = disabled)

**How it works:**
1. Define goal (explicit text or auto-derive from vision)
2. Each iteration measures progress toward goal
3. Detects stagnation (no progress) or oscillation (bouncing)
4. Can halt when convergence criteria met (goal achieved or timeout)

**Storage:** `docs/engineering/goal-convergence/` (per-goal tracking)

**Overhead:** ~5 lines/iteration; zero when `SOVEREIGN_GOAL_MODE=phase_driven`

**Deep dive:** `docs/engineering/runbook.md` § Goal Convergence

---

### US-0106: Role-Based Model Catalog

**What it is:**
Maps model tiers to role-specific catalogs. Enables different subagents to use different model strengths based on their role (e.g., architect gets stronger models, simple tasks get cheaper models).

**Why use it:**
- **Cost optimization:** Use cheaper models for simple tasks
- **Quality matching:** Use stronger models for complex tasks
- **Role specialization:** Tailor model selection to subagent expertise
- **Flexibility:** Fine-grained control over model allocation

**When to enable:**
- Multi-tier model access available
- Cost-sensitive deployments
- Complex workflows with varying task complexity
- Team environments with role-based responsibilities

**How to enable:**
```markdown
# .cursor/scratchpad.local.md
MODEL_CATALOG=.cursor/model-catalog.local.json  # Catalog path (default: .cursor/model-catalog.local.json)
MODEL_RESOLVE=role_catalog                  # Resolution: alias_only|local_catalog|role_catalog (default: alias_only)
MODEL_FALLBACK=inherit                      # Fallback when role mismatch (default: inherit)
```

**Key flags:**
- `MODEL_CATALOG` — Path to model catalog JSON
- `MODEL_RESOLVE=alias_only|local_catalog|role_catalog`
  - `alias_only`: Single model for all roles (default)
  - `local_catalog`: Tier-based selection from catalog
  - `role_catalog`: Role-specific model mapping (recommended)
- `MODEL_FALLBACK=inherit` — Fallback when role has no mapping

**Catalog format:**
```json
{
  "models": [
    {
      "id": "cheap",
      "name": "GPT-4o-mini",
      "roles": ["intake", "refresh-context"]
    },
    {
      "id": "strong",
      "name": "GPT-4o",
      "roles": ["architect", "execute", "qa"]
    }
  ],
  "roles": {
    "architect": "strong",
    "intake": "cheap",
    "default": "balanced"
  }
}
```

**Storage:** `.cursor/model-catalog.local.json` (user-defined)

**Overhead:** Zero catalog lookup; zero when `MODEL_RESOLVE=alias_only`

**Deep dive:** `docs/engineering/runbook.md` § Role-Based Model Catalog

---

### US-0111: Release Trigger Adapters

**What it is:**
Extends `/release` with pluggable trigger adapters. Supports GitHub webhooks, npm publish events, git tag detection, and manual triggers. Routes release flow based on trigger source.

**Why use it:**
- **Automation:** Trigger releases from external events
- **CI/CD integration:** Connect to existing deployment pipelines
- **Flexibility:** Multiple trigger sources for different workflows
- **Traceability:** Log which trigger initiated each release

**When to enable:**
- GitHub-centric workflows
- npm package publishing
- CI/CD pipeline integration
- Multi-source release triggers

**How to enable:**
```markdown
# .cursor/scratchpad.local.md
RELEASE_TRIGGER_SOURCE=manual                 # Trigger source: manual|github|npm|git_tag|auto (default: manual)
RELEASE_TRIGGER_TIMEOUT_SEC=30                # Adapter timeout (default: 30)
RELEASE_TRIGGER_FALLBACK_TO_LOCAL=1           # Fallback to local mode (default: 1)
```

**Key flags:**
- `RELEASE_TRIGGER_SOURCE=manual|github|npm|git_tag|auto`
  - `manual`: Standard `/release` command (default)
  - `github`: GitHub webhook trigger
  - `npm`: npm publish event
  - `git_tag`: Git tag detection
  - `auto`: Auto-detect based on context
- `RELEASE_TRIGGER_TIMEOUT_SEC=5-300` — Adapter timeout
- `RELEASE_TRIGGER_FALLBACK_TO_LOCAL=0|1` — Fallback on adapter failure

**How it works:**
1. Detects trigger source (webhook/event/tag/manual)
2. Routes to appropriate adapter
3. Adapter extracts release context (version, changelog, etc.)
4. Initiates standard `/release` flow with adapter context

**Storage:** `docs/engineering/release-triggers/` (per-trigger logs)

**Overhead:** ~1 sec/trigger detection; zero when `RELEASE_TRIGGER_SOURCE=manual`

**Deep dive:** `docs/engineering/runbook.md` § Release Trigger Adapters

---

### US-0112: Model Catalog Example Presets

**What it is:**
Ships 8 pre-configured model catalog examples covering different complexity levels (level 1–4) and role-based configurations. Installers copy examples to `.cursor/` on install/upgrade.

**Why use it:**
- **Quick start:** Use pre-built catalogs instead of manual config
- **Best practices:** Examples follow proven patterns
- **Complexity matching:** Choose catalog appropriate to project size
- **Role optimization:** Use role-based catalogs for team workflows

**When to use:**
- Fresh its-magic installations
- Upgrading to new its-magic version
- Starting new project with known complexity
- Migrating from tier-based to role-based model selection

**How to use:**
```bash
# After install/upgrade, example catalogs are in .cursor/
ls .cursor/model-catalog.local.example.*.json

# Copy desired example to active catalog
cp .cursor/model-catalog.local.example.level-2-complex.json .cursor/model-catalog.local.json

# Or use role-based catalog
cp .cursor/model-catalog.local.example.role-based-balanced.json .cursor/model-catalog.local.json

# Enable role_catalog resolution
# .cursor/scratchpad.local.md
MODEL_RESOLVE=role_catalog
```

**Available examples:**
1. `model-catalog.local.example.json` — Minimal placeholder
2. `model-catalog.local.example.cursor-only.json` — Cursor-only models
3. `model-catalog.local.example.level-1-easy.json` — Small/simple apps
4. `model-catalog.local.example.level-2-complex.json` — Complex multi-service
5. `model-catalog.local.example.level-3-mega.json` — Mega-complex/monoliths
6. `model-catalog.local.example.level-4-super.json` — High-sophisticated/mission-critical
7. `model-catalog.local.example.role-based-balanced.json` — Role preset (balanced)
8. `model-catalog.local.example.role-based-highend.json` — Role preset (high-end)

**Storage:** `.cursor/model-catalog.local.example.*.json` (shipped examples)

**Overhead:** Zero (static files); managed by installer

**Deep dive:** `docs/engineering/runbook.md` § Model Catalog Presets

---

## Sovereign-Loop Era Configuration Summary

All sovereign-loop features are **disabled by default** (zero overhead when off). Enable individually via `.cursor/scratchpad.local.md`:

| Feature | Flag | Default | Recommended |
|---------|------|---------|-------------|
| AI Decision Ledger | `AI_DECISION_LEDGER` | `0` | `1` (for auditability) |
| Plan Fidelity | `AUTO_PLAN_FIDELITY` | `relaxed` | `relaxed` |
| Cross-Model Critic | `CROSS_MODEL_REVIEW` | `0` | `1` (for validation) |
| Sovereign Memory | `SOVEREIGN_MEMORY` | `0` | `1` (for learning) |
| Parallel Arbitrage | `SOVEREIGN_PARALLEL_DEV` | `0` | `0` (high cost) |
| Self-Healing Deploy | `AUTO_SOVEREIGN_SELF_HEALING_DEPLOY` | `0` | `1` (for CI/CD) |
| Goal Convergence | `SOVEREIGN_GOAL_MODE` | `phase_driven` | `phase_driven` |
| Model Catalog | `MODEL_RESOLVE` | `alias_only` | `role_catalog` |
| Release Triggers | `RELEASE_TRIGGER_SOURCE` | `manual` | `auto` (for CI/CD) |

**Zero overhead when off:** All features add zero overhead, tokens, or file writes when disabled.

**Individual enablement:** Enable features independently based on project needs.

**Recommended starting point:**
```markdown
# .cursor/scratchpad.local.md (minimal sovereign-loop config)
AI_DECISION_LEDGER=1
SOVEREIGN_MEMORY=1
CROSS_MODEL_REVIEW=1
MODEL_RESOLVE=role_catalog
MODEL_CATALOG=.cursor/model-catalog.local.json
```

**Full sovereign-loop config (for experimentation):**
```markdown
# .cursor/scratchpad.local.md (all sovereign features)
AI_DECISION_LEDGER=1
AUTO_PLAN_FIDELITY=relaxed
CROSS_MODEL_REVIEW=1
CROSS_MODEL_REVIEW_MODE=adversarial
CROSS_MODEL_REVIEW_MIN_AGREEMENT=0.6
SOVEREIGN_MEMORY=1
SOVEREIGN_MEMORY_TOP_N=5
SOVEREIGN_MEMORY_TOP_K=3
SOVEREIGN_MEMORY_MAX_CHARS=2048
SOVEREIGN_PARALLEL_DEV=0  # High cost; enable for specific tasks only
AUTO_SOVEREIGN_SELF_HEALING_DEPLOY=1
SOVEREIGN_GOAL_MODE=goal_convergence
MODEL_RESOLVE=role_catalog
RELEASE_TRIGGER_SOURCE=auto
```

"""

# Insert sovereign docs before "Other useful capabilities"
lines.insert(insert_idx, sovereign_docs)

with open('its_magic/README.md', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Successfully inserted sovereign-loop documentation at line {insert_idx + 1}")
