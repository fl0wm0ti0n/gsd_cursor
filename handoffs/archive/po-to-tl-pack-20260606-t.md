# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 14
- First archived heading: `## Orchestrated discovery handoff — US-0093 / auto-20260606-04`
- Last archived heading: `## Orchestrated discovery handoff — US-0093 / auto-20260606-04`
- Verification tuple (mandatory):
  - archived_body_lines=72
  - retained_body_lines=766

---

## Orchestrated discovery handoff — US-0093 / auto-20260606-04

### Target

- `story_id=US-0093`
- `orchestrator_run_id=auto-20260606-04`
- phase completed: **`discovery`** (**`po`**)
- `next_scheduled_phase=research`
- `fresh_context_marker=po-US0093-discovery-20260606T230000Z-fresh`
- `decomposition=single_story` (PO default; per `US-0051`)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=2`

### Summary

- **Execution gap**: **US-0092** / **DEC-0078** shipped UAT probe catalog + fail-closed vocabulary, but **`browser_smoke`**, **`process_health`**, and **`cli_smoke`** still return **`UAT_PROBE_UNRESOLVED`** in **`scripts/uat_probe_lib.py`**; **`manual_operator`** UI steps are never auto-run. **US-0093** closes the gap with **Cursor built-in browser** as primary web self-test path + HTTP/Playwright fallback + stub completion.
- **Two-tier contract (discovery-locked)**: stdlib lib classifies, runs subprocess fallbacks, completes health/cli stubs; QA/verify-work/execute subagents invoke Cursor browser MCP and write **`browser_evidence_refs`** to **`uat.json`** / **`qa-findings.md`**.
- **`UAT_BROWSER_PROBE_MODE`**: **`cursor`** (default) | **`http_fallback`** | **`playwright_fallback`** — composes with **`PERMISSION_MODE`** and Cursor browser approval settings.
- **Spawn-only preserved**: **US-0048** / **BUG-0006** unchanged — browser MCP runs in fresh phase subagents, not from Python stdlib alone.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Acceptance pointers (discovery emphasis)

- **AC-1**: **`UAT_BROWSER_PROBE_MODE`** scratchpad key + approval/`PERMISSION_MODE` interaction docs.
- **AC-2**: **`browser_smoke` executes** — agent-browser contract in command specs; fallback when MCP unavailable.
- **AC-3**: Automatable **`manual_operator`** UI verb routing; judgment-only stays fail closed.
- **AC-4**: **`process_health`** / **`cli_smoke`** stub completion via bounded subprocess.
- **AC-5**: **`browser_evidence_refs`** in **`uat.json`** + **`qa-findings.md`** mirror.
- **AC-6**: New reason codes **`UAT_BROWSER_UNAVAILABLE`**, **`UAT_BROWSER_PROBE_FAILED`**, **`UAT_BROWSER_PROBE_TIMEOUT`**.
- **AC-7–AC-10**: Security deny-list, runbook recipe, contract tests, template parity.

### Top risks (carry to /research)

- **R1** False PASS without agent evidence — dual-tier contract + required evidence refs.
- **R2** Over-automation of judgment steps — verb routing table.
- **R3** MCP unavailable in CI — fallback modes + **`UAT_BROWSER_UNAVAILABLE`**.
- **R4** Secret exposure via browser — **`UAT_PROBE_FORBIDDEN`** + no credential fill.
- **R5** Partial stub delivery — single-story vertical contract.

### Research asks (extend **`R-0079`**)

1. Agent-browser command contract — MCP step sequence + evidence write-back in **`verify-work.md`** / **`qa.md`** / **`execute.md`**.
2. **`manual_operator` verb routing table** — automatable vs judgment-only classifier rules.
3. Fallback selection — MCP-unavailable detection; HTTP vs Playwright precedence.
4. **`process_health` / `cli_smoke` parse rules** — acceptance text → command extraction.
5. Evidence schema — artifact paths, console/network summary shape.
6. Contract-test + template parity inventory (`pytest -k us0093`, `--scope=us-0093`).

### Evidence refs

- `docs/product/backlog.md` (`## US-0093` — discovery_notes appended)
- `docs/product/vision.md` (**Intake Notes — US-0093** + **Discovery Notes — US-0093**)
- `docs/product/acceptance.md` (`US-0093` row — unchecked)
- `handoffs/intake_evidence/US-0093-intake-20260606.json`
- `docs/engineering/research.md` (**`R-0079`** — discovery extension appended)
- `scripts/uat_probe_lib.py` (stub branches lines 170–172, 215–217)
- `docs/engineering/architecture.md` (`# US-0092` UAT probe contract table)
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/research`)
- Adjacent: **US-0092**, **DEC-0078**, **US-0065**, **R-0041**

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0093`** — deepen **`R-0079`**, lock two-tier contract, verb routing, fallback rules, and evidence schema before **`/architecture`**.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

