# PO to TL archive pack (2026-06-14)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 10
- First archived heading: `## Intake handoff — US-0101 / cursor-20260614-US0101-intake`
- Last archived heading: `## Intake handoff — US-0101 / cursor-20260614-US0101-intake`
- Verification tuple (mandatory):
  - archived_body_lines=67
  - retained_body_lines=635

---

## Intake handoff — US-0101 / cursor-20260614-US0101-intake

### Target

- `story_id=US-0101`
- `intake_run_id=cursor-20260614-US0101-intake`
- `selected_pack=small-intake-pack`
- `decomposition=single_story` (per **US-0051**)
- `priority=P2`
- `next_scheduled_phase=discovery`

### Summary

Operator wants **per-phase LLM model strength** in its-magic: cheap models for light phases (`/ask`, `/refresh-context`), strong models for coding/architecture (`/execute`, `/architecture`), applied automatically when **`/auto`** spawns role subagents — **without** hardcoding volatile model IDs in framework **`template/`** files.

### Problem framing

| Gap | Today | Target |
|-----|-------|--------|
| Model per phase | All subagents inherit parent chat model or ad-hoc slugs | **`MODEL_TIER`** scratchpad + agent **`model:`** aliases |
| ID volatility | Slugs like `composer-2.5` / `claude-opus-4-8` change | Stable **`fast`** / **`inherit`** in template; optional **local catalog** for slugs |
| Cost vs context | **`TOKEN_PROFILE`** trims context only (**DEC-0062**) | **`MODEL_TIER`** selects LLM; explicit non-substitution docs |
| API-only / BYOK | Undocumented | **`MODEL_PROVIDER_MODE=cursor|api`** runbook + subagent BYOK caveats |

### Default tier matrix (intake-locked for discovery)

| Tier | Phases |
|------|--------|
| **cheap** | `ask`, `refresh-context`, `memory-audit`, `status-reconcile`, `pause` |
| **balanced** | `intake`, `discovery`, `research`, `release`, `plan-verify` |
| **strong** | `architecture`, `execute`, `quick`, `qa`, `verify-work`, `security-review` |

Resolution: **`cheap` → `fast`**, **`strong`/`balanced` → `inherit`** (or local catalog slug when **`MODEL_RESOLVE=local_catalog`**).

### Constraints (hard)

- **Orthogonal to `TOKEN_PROFILE`** — never conflate lean profile with cheap model.
- **Template forbidden slugs** — no `composer-*`, `claude-*`, `gpt-*`, `opus-*` in **`template/.cursor/agents/`**.
- **Isolation unchanged** — **US-0048** / **BUG-0006** spawn-only; tier config must not weaken gates.
- **API-only caveat** — document that Cursor subagents may not inherit custom API keys (known product limitation); workaround = parent model + **`inherit`** or manual phase chats.

### Research asks (**`R-0088`** stub)

1. Materializer vs static agent **`model:`** — when does scratchpad override apply?
2. **`local_catalog`** schema versioning and upgrade path.
3. Contract-test strategy: forbidden slug grep + tier matrix literals.
4. Interaction with **Settings → Agents → Subagents** UI overrides (document precedence).
5. SDK / **`auto_outer_driver.py`** optional per-send model (reference only in v1).

### Intake evidence

- `handoffs/intake_evidence/US-0101-intake-20260614.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**
- `asked_topics`: outcome_success_criteria, impacted_components, constraints_compatibility_risks, required_tests_acceptance_checks, done_definition
- `assumptions_confirmed=(none)`

### Alternatives considered

1. **Hardcode slugs in template agents** — rejected (ID churn, breaks on API-only).
2. **Extend `TOKEN_PROFILE=lean` to imply cheap model** — rejected (violates **DEC-0062**).
3. **Dynamic `models.list()` at IDE spawn** — deferred (SDK path only in v1; aliases + local catalog for IDE).

### Status

**OPEN** per **US-0045**. **Next**: **`/discovery`** (fresh **PO**).

---

