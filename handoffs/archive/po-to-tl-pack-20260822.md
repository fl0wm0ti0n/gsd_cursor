# PO to TL archive pack (2026-08-22)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 7
- First archived heading: `## US-0121 — OpenCode adapter epic intake (US-0121..US-0126)`
- Last archived heading: `## US-0121 — OpenCode adapter epic intake (US-0121..US-0126)`
- Verification tuple (mandatory):
  - archived_body_lines=72
  - retained_body_lines=580

---

## US-0121 — OpenCode adapter epic intake (US-0121..US-0126)

- **Story**: `docs/product/backlog.md` `## US-0121` (first slice) plus OPEN siblings **US-0122..US-0126**
- **Acceptance**: `docs/product/acceptance.md` US-0121..US-0126 rows (unchecked, OPEN)
- **Intake evidence**: `handoffs/intake_evidence/US-0121-intake-20260822.json` (`first-intake-pack`, validator `[INTAKE_EVIDENCE_VALIDATION_OK]`, `coverage_complete=true`, 16 plan areas)
- **Research**: `docs/engineering/research.md` **R-0109** (intake stub)
- **Source brief**: `docs/product/opencode-adapter-masterplan.md`
- **Phase**: intake
- **Phase role**: po
- **Verdict**: INTAKE PASS; no DECISION_GATE
- `intake_run_id=cursor-20260822-opencode-adapter-intake`, `writer_id=po-cursor-20260822`
- **Status**: OPEN per US-0045. **Next**: `/discovery` (fresh **PO**) for **US-0121** with epic context that US-0122–US-0126 are OPEN siblings.

### Isolation evidence (US-0048 / BUG-0006)

- `phase_id=intake`
- `role=po`
- `fresh_context_marker=po-US0121-intake-20260822T211500Z-fresh`
- `timestamp=2026-08-22T21:15:00Z`
- `evidence_ref=handoffs/po_to_tl.md` (this section)

### Summary

Ship its-magic as a second host pack for **stock OpenCode**: same artifact kernel and Python fail-closed gates; role behavior and `/auto` spawn enforced by OpenCode permissions plus one orchestrator plugin. Cursor pack remains. Default install host stays **cursor-only** until explicit `--host opencode|both`. Plugin API v1 vs v2 is **not** intake-locked (**R-0109** / `/research`). Standalone runtime is a different program.

### Split rationale (US-0051)

- **Why split**: one mega-story would mix installer, permissions, models, plugin spawn, validators, and docs; slices would not be independently testable.
- **Split axis**: vertical workflow steps (operator-accepted via submitting the masterplan).
- **Boundaries**:
  - **US-0121** pack + installer + coexistence
  - **US-0122** seven roles + orchestrator agents + Layer-1 permissions (success test c)
  - **US-0123** `provider/slug` routing, multi-provider, no template vendor IDs
  - **US-0124** spawn-only plugin + US-0069 + isolation + stop matrix + `--invoke-cmd` (success tests a, d)
  - **US-0125** thin commands + Python validator bridge (success test b)
  - **US-0126** runbook + reason codes + `--scope=opencode-adapter`
- **Not cloned**: US-0001–US-0119. **Not this program**: standalone runtime.

### Assumptions locked

Default install host remains cursor-only until explicit `--host opencode|both` opt-in; OpenCode plugin v1 vs v2 deferred to `/research`.

### Compose, do not amend

- US-0008 installer semantics except additive `--host`
- US-0003 roles as contract
- US-0069 phase→role matrix
- US-0092 outer driver / `--invoke-cmd`
- US-0101 / US-0102 semantics without Cursor aliases as OpenCode runtime
- BUG-0006 spawn-only; US-0023 isolation
- Do **not** port US-0095 native Cursor chain — the plugin **is** the chain on OpenCode

### Risks carried to discovery / research

- R1 (HIGH): stock OpenCode cannot isolate child sessions / V2 `subtask` ignored — fail closed; fork is deferred, not silent roleplay (**R-0001**, **R-0109** Q1–Q2)
- R2 (MEDIUM): dual-host parity cost — thin commands + `--scope=opencode-adapter`
- R3 (MEDIUM): plugin API v1 vs v2 unknown at intake — `/research` lock
- R4 (LOW): template vendor-slug leakage — US-0123 grep tests
- R5 (LOW): scope creep into sovereign-loop / standalone runtime — inventory deferrals already persisted

### Plan-area coverage

Mapped to stories: template pack, installer host mode, cursor coexistence → US-0121; roles/permissions → US-0122; model slugs → US-0123; plugin spawn + headless invoke-cmd → US-0124; validator bridge + thin commands → US-0125; docs/parity → US-0126. Deferred: sovereign-loop-on-opencode, standalone-runtime, opencode-fork, vscode-shell-port, caveman-voice-port, cursor-browser-uat.

### Next scheduled phase

**`/discovery`** in a **fresh PO** subagent for **US-0121** (install slice first). Carry epic context: US-0122–US-0126 stay OPEN; do not start standalone-runtime intake. After discovery: **`/research`** (tech-lead) to deepen **R-0109** (plugin spawn + installer ownership), then **`/architecture`**.

### Triad rollover

Recorded after `python scripts/enforce-triad-hot-surface.py --rollover` then `--check` (see follow-up line if units moved).

