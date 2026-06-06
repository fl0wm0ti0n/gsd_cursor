# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 14
- First archived heading: `## Orchestrated research handoff — US-0093 / auto-20260606-04`
- Last archived heading: `## Orchestrated research handoff — US-0093 / auto-20260606-04`
- Verification tuple (mandatory):
  - archived_body_lines=51
  - retained_body_lines=766

---

## Orchestrated research handoff — US-0093 / auto-20260606-04

### Target

- `story_id=US-0093`
- `orchestrator_run_id=auto-20260606-04`
- phase completed: **`research`** (**`tech-lead`**)
- `next_scheduled_phase=architecture`
- `fresh_context_marker=tl-US0093-research-20260606T231500Z-fresh`
- `decomposition=single_story` (PO default; per `US-0051`)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=2`

### Summary

- **`/research`** **PASS** — **`R-0079`** Q1–Q6 resolved. Two-tier browser UAT contract locked: **`uat_probe_lib.py`** = classify + stdlib fallbacks + **`process_health`**/**`cli_smoke`** completion; agent phase commands = Cursor browser MCP primary when **`UAT_BROWSER_PROBE_MODE=cursor`** (default).
- **Agent contract (Q1)**: MCP sequence navigate → interact → screenshot → console/network summaries → merge **`browser_evidence_refs`** into **`uat.json`** / **`qa-findings.md`**; lib emits **`execution_tier=agent`** and withholds PASS until evidence present.
- **Verb routing (Q2)**: judgment-only tokens win; automatable UI verbs reclassify to **`browser_smoke`**.
- **Fallback (Q3)**: MCP-unavailable/CI → **`UAT_BROWSER_UNAVAILABLE`** then HTTP → Playwright chain per mode key.
- **Stub completion (Q4)**: deterministic parse rules for health/cli probes + readiness poll defaults (60s).
- **Evidence (Q5)**: **`sprints/Sxxxx/evidence/browser/`** layout + **`browser_evidence_refs`** schema.
- **Parity (Q6)**: **`test_us0093_*`**, **`--scope=us-0093`**, command spec subsections.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Architecture inputs (from research)

1. Lock **`DEC-xxxx`** composing on **DEC-0078** — new reason codes, **`UAT_BROWSER_PROBE_MODE`**, evidence schema, dual-tier dispatch.
2. **`# US-0093`** in **`architecture.md`** — probe plan API, verb table, fallback matrix, poll defaults.
3. No decision gate unless architecture finds blocking conflict (none identified).

### Evidence refs

- `docs/engineering/research.md` (**`R-0079`** research extension — Q1–Q6 resolved)
- `docs/product/backlog.md` (`## US-0093` — `research_notes` appended)
- `handoffs/resume_brief.md` (architecture pointer)
- `docs/engineering/state.md` (Research checkpoint — this run)
- `scripts/uat_probe_lib.py`; `.cursor/commands/verify-work.md`, `qa.md`, `execute.md`
- `docs/engineering/architecture.md` (`# US-0092` baseline); `decisions/DEC-0078.md`
- Prior: `handoffs/archive/po-to-tl-pack-20260606-t.md` (discovery handoff)

### Next

- **`/architecture`** (fresh **tech-lead** context) for **`US-0093`** — author **`DEC-xxxx`** + **`# US-0093`** from **`R-0079`** resolutions.

### Decision gate

- **None** — research satisfied; story **OPEN**.

---

