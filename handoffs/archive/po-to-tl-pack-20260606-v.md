# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 14
- First archived heading: `## Orchestrated architecture handoff — US-0093 / auto-20260606-04`
- Last archived heading: `## Orchestrated architecture handoff — US-0093 / auto-20260606-04`
- Verification tuple (mandatory):
  - archived_body_lines=68
  - retained_body_lines=766

---

## Orchestrated architecture handoff — US-0093 / auto-20260606-04

### Target

- `story_id=US-0093`
- `orchestrator_run_id=auto-20260606-04`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0093-architecture-20260606T233000Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `decomposition=single_story` (PO default; per `US-0051`)
- `priority=P1`
- `dec_id=DEC-0079`

### Summary

- **`/architecture`** **PASS** — **`DEC-0079`** authored; **`docs/engineering/architecture.md`** **`# US-0093`** appended; two-tier browser UAT contract locked (stdlib classify + agent Cursor browser MCP); **`UAT_BROWSER_PROBE_MODE`** scratchpad key; verb routing table; **`browser_evidence_refs`** evidence schema; **`process_health`**/**`cli_smoke`** stub completion; reason codes **`UAT_BROWSER_*`**; composes on **US-0092**/**DEC-0078** without weakening spawn-only or security deny-list.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Locked decisions (DEC-0079 summary)

1. **Two-tier model** — stdlib lib never calls browser MCP; agent commands own Tier 2 when **`UAT_BROWSER_PROBE_MODE=cursor`** (default).
2. **Scratchpad keys** — **`UAT_BROWSER_PROBE_MODE`**, **`UAT_BROWSER_FALLBACK_CHAIN`**, poll defaults; orthogonal to **`PERMISSION_MODE`**.
3. **Agent MCP sequence** — navigate → interact → screenshot → console/network → evidence write-back; **`--merge-result`** optional validator.
4. **Verb routing** — judgment tokens win; automatable UI reclassifies to **`browser_smoke`**.
5. **Fallback chain** — MCP-unavailable heuristic (CI/headless) → HTTP → Playwright; fail closed.
6. **Stub completion** — **`process_health`** readiness poll (60s default); **`cli_smoke`** deterministic parse.
7. **Evidence schema** — **`browser_evidence_refs`** under **`sprints/Sxxxx/evidence/browser/`**; PASS requires refs in cursor mode.
8. **Reason codes** — **`UAT_BROWSER_UNAVAILABLE`**, **`UAT_BROWSER_PROBE_FAILED`**, **`UAT_BROWSER_PROBE_TIMEOUT`**.
9. **Security** — **DEC-0078** deny-list unchanged; no credential auto-fill.
10. **Template parity** — **`--scope=us-0093`** + **`test_us0093_*`**.

### Atomic task seeds (10; `/sprint-plan` converts to T-xxx)

See **`docs/engineering/architecture.md`** **`# US-0093`** § Atomic task seeds.

| # | Seed | AC |
|---|------|-----|
| 1 | Scratchpad mode + poll/fallback keys | AC-1 |
| 2 | **`uat_probe_lib.py`** mode, routing, **`--merge-result`** | AC-2, AC-3 |
| 3 | Agent-browser MCP in verify-work/qa/execute | AC-2 |
| 4 | **`process_health`** + **`cli_smoke`** completion | AC-4 |
| 5 | Evidence schema + qa-findings mirror | AC-5 |
| 6 | **`UAT_BROWSER_*`** reason codes + self-test | AC-6 |
| 7 | HTTP/Playwright fallback chain | AC-2, AC-6 |
| 8 | Runbook + auto-orchestration-reference recipe | AC-8 |
| 9 | Contract tests **`test_us0093_*`** | AC-9 |
| 10 | Template parity **`--scope=us-0093`** + security assert | AC-7, AC-10 |

### Evidence refs

- `decisions/DEC-0079.md`
- `docs/engineering/architecture.md` (**`# US-0093`**)
- `docs/engineering/decisions.md` (index + context pack)
- `docs/product/backlog.md` (`## US-0093` `architecture_notes`)
- `docs/engineering/research.md` (**`R-0079`**)
- `docs/engineering/state.md` (Architecture checkpoint — this run)
- `handoffs/resume_brief.md` (sprint-plan pointer)

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`US-0093`** — seed sprint from 10 task seeds + AC ↔ § map.

### Decision gate

- **None** — architecture satisfied; story **OPEN**.

---

