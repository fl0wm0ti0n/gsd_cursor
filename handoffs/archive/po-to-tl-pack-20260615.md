# PO to TL archive pack (2026-06-15)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 10
- First archived heading: `## Orchestrated discovery handoff — US-0101 / auto-20260615-02`
- Last archived heading: `## Orchestrated discovery handoff — US-0101 / auto-20260615-02`
- Verification tuple (mandatory):
  - archived_body_lines=72
  - retained_body_lines=635

---

## Orchestrated discovery handoff — US-0101 / auto-20260615-02

### Target

- `story_id=US-0101`
- `orchestrator_run_id=auto-20260615-02`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0101-discovery-20260615T200000Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (per **US-0051**)
- `priority=P2`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=6`

### Summary

- **`/discovery`** **PASS** — 12 locks captured (L1–L12); **`R-0088`** extended with Q1–Q5 open for **`/research`**; **`# US-0101`** discovery_notes appended to backlog.
- **Problem framing**: operators need per-phase LLM strength control (cheap/balanced/strong) via stable aliases without hardcoding volatile vendor model IDs in template agent files.
- **Recommended model (discovery-locked)**: `MODEL_TIER_<phase>=cheap|balanced|strong` in scratchpad; tier→alias resolution (`cheap`→`fast`, `strong`→`inherit`, `balanced`→open); local catalog `.cursor/model-catalog.local.json` (gitignored); provider-mode runbook `MODEL_PROVIDER_MODE=cursor|api`.
- **Orthogonality**: **MODEL_TIER** ≠ **TOKEN_PROFILE** (DEC-0062 — context breadth only, never model choice).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (12 locks — sprint-plan inputs)

| Lock | Decision |
|------|----------|
| **L1** | **Tier enum**: `cheap` / `balanced` / `strong` — three-tier model |
| **L2** | **Default phase→tier matrix**: cheap: ask/refresh-context/memory-audit/status-reconcile/pause; balanced: intake/discovery/research/release/plan-verify; strong: architecture/execute/qa/verify-work/security-review |
| **L3** | **Tier→alias resolution**: `cheap` → `fast`, `strong` → `inherit`; `balanced` → open for research (inherit vs middle alias) |
| **L4** | **Local catalog schema**: `.cursor/model-catalog.local.json` (gitignored) + `.example.json`; maps tier → operator slug string |
| **L5** | **Template agent defaults**: aliases only in `template/.cursor/agents/`; no hardcoded vendor slugs |
| **L6** | **Provider mode runbook**: `MODEL_PROVIDER_MODE=cursor|api` subsection in runbook + auto-orchestration-reference |
| **L7** | **Scratchpad merge precedence**: local > materialized > example per DEC-0055 |
| **L8** | **Orthogonality vs TOKEN_PROFILE**: explicit non-substitution paragraph; MODEL_TIER ≠ TOKEN_PROFILE |
| **L9** | **Fail-closed reason codes**: `MODEL_TIER_INVALID`, `MODEL_CATALOG_INVALID`, `MODEL_RESOLVE_FALLBACK`, `MODEL_SLUG_UNKNOWN` |
| **L10** | **Contract test inventory**: `test_us0101_*` markers for scratchpad keys, matrix literals, orthogonality, template aliases, forbidden slug grep |
| **L11** | **Template parity scope**: `check_intake_template_parity.py --scope=model-tier` when surfaces touched |
| **L12** | **DEC-0062 compose**: new decision composes DEC-0062 without amending TOKEN_PROFILE tier meanings |

### Top risks (carry to /research)

- **R1**: Cursor subagent BYOK limitation may limit api-only mode practical value — document known limitation + workarounds.
- **R2**: Balanced tier alias ambiguity — inherit vs new middle alias (open for Q1).
- **R3**: Materializer hook scope — scratchpad-only vs active agent rewrite (open for Q2).

### Research questions (open for /research via R-0088)

- **Q1**: Finalize tier→alias mapping — should `balanced` resolve to `inherit` (stable) or a new middle alias?
- **Q2**: Local catalog JSON schema + resolver algorithm details.
- **Q3**: Agent template defaults — which roles get `fast` vs `inherit`?
- **Q4**: Provider mode runbook UX — how to document BYOK limitations clearly.
- **Q5**: Contract-test inventory + parity scope finalization.

### Evidence refs

- `docs/product/backlog.md` (`## US-0101` — `discovery_notes` appended)
- `docs/product/vision.md` (**Discovery Notes — US-0101**)
- `docs/engineering/research.md` (**`R-0088`** — discovery extension appended)
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/research`)
- `handoffs/intake_evidence/US-0101-intake-20260614.json`

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0101`** — resolve Q1–Q5; lock architecture inputs; allocate **`DEC-xxxx`**.

### Decision gate

- **None** — discovery satisfied; research readiness explicit on tier→alias resolution, catalog schema, template defaults, runbook UX, contract-test inventory.

---

