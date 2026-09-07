# PO to TL archive pack (2026-09-07)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 10
- First archived heading: `## Discovery handoff — US-0131 Cross-host Its-Magic runtime configuration and parity`
- Last archived heading: `## Discovery handoff — US-0131 Cross-host Its-Magic runtime configuration and parity`
- Verification tuple (mandatory):
  - archived_body_lines=59
  - retained_body_lines=602

---

## Discovery handoff — US-0131 Cross-host Its-Magic runtime configuration and parity

- **Phase completed**: discovery. **Role**: po. **Story**: US-0131 only. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp (UTC)**: 2026-09-07T19:15:00Z. **Fresh marker**: `po-US0131-discovery-20260907T191500Z-fresh`.
- **Orchestrator**: `orchestrator_run_id=auto-20260907-us0131`, `delivery_mode=ultra_lean`, macro=`spec` (intake already PASS — not re-intaken).
- **Sibling boundary**: **US-0132** OPEN (model configuration contract) — OUT OF SCOPE; do not expand into US-0132 ACs. **BUG-0015/BUG-0016** DONE — do not reopen.
- **Gap confirmed**: shared lifecycle/governance settings still resolve through Cursor-path scratchpad readers; OpenCode-only installs must not require `.cursor/`; host-specific capabilities must fail/skip deterministically.

### Discovery locks D1–D10

| ID | Lock |
|----|------|
| **D1** | Host-neutral typed config contract for shared runtime/governance (no credentials / provider secrets / vendor slugs in templates). |
| **D2** | Cursor scratchpad (DEC-0055 Model B + DEC-0039 local protection) = **compatibility adapter** into the neutral contract — not the sole SOT after migration. |
| **D3** | OpenCode-only install resolves all shared settings without `.cursor/scratchpad.md` or `.cursor/scratchpad.local.md`. |
| **D4** | Shared Python validators/outer-driver/triad/state/handoff scripts accept resolved config explicitly — no silent `.cursor` hardcode for host-neutral behavior. |
| **D5** | Cursor-only vs OpenCode-only capabilities classified; unavailable → fail/skip with reason codes; no silent unsupported parity; no Cursor command/rule body clones. |
| **D6** | `--host both` has one deterministic precedence; no conflicting duplicate writes; independent host-local overrides where schemas differ. |
| **D7** | Installer delivers examples to selected host; preserves local operator files; never overwrites active scratchpad/config. |
| **D8** | Contract tests for cursor-only / opencode-only / both + docs for precedence, migration, reason codes (active + template). |
| **D9** | **US-0132 boundary** — model catalogs / `MODEL_*` / materializers out of scope; no third `model.json` SOT. |
| **D10** | Compose US-0073/DEC-0055, DEC-0039, US-0121..US-0126, US-0092, US-0069; do not amend DEC-0086/0087/0123; do not reopen BUG-0015/0016. |

### Research questions DQ1–DQ10 (for `/research` → expect **R-0116**)

1. **DQ1**: Canonical host-neutral config path (must not require `.cursor/` on OpenCode-only).
2. **DQ2**: Typed schema + versioning + fail-closed codes for malformed/missing shared keys.
3. **DQ3**: Cursor scratchpad merge → neutral resolver mapping (preserve DEC-0055/0039).
4. **DQ4**: OpenCode-only shared-settings adapter (prefer dedicated kit config over dumping into `opencode.json` model/permission schema).
5. **DQ5**: Complete `.cursor/scratchpad*` hardcode inventory + injection API shape.
6. **DQ6**: Exact `--host both` precedence table.
7. **DQ7**: Finalize shared / Cursor-only / OpenCode-only / skip-vs-fail matrix + reason-code family.
8. **DQ8**: Installer/manifest example delivery surfaces per `--host cursor|opencode|both`.
9. **DQ9**: Minimal `test_us0131_*` inventory + fixtures (no live OpenCode CI probe).
10. **DQ10**: Docs anchors (runbook/README/auto-orchestration-reference) for precedence/migration/unsupported capability.

### Config-surface / design refs

- OpenCode: https://opencode.ai/v2/docs/config/ — `opencode.json{,c}`, `.opencode/`
- Cursor: DEC-0055 Model B scratchpad pair; DEC-0039 local preservation
- Script hardcodes: `scripts/auto_outer_driver.py`, `scripts/opencode_auto_bridge.py`, `scripts/enforce-triad-hot-surface.py`, `scripts/dev_environment_lib.py`, `scripts/caveman_compress_input.py`
- Vision: `docs/product/vision.md` `## Discovery Notes — US-0131`
- Intake (read-only): `handoffs/intake_evidence/US-0131-0132-intake-20260906.json`

### Runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260907-us0131-discovery-po-20260907T191500Z-US-0131`
- `proof_hash=7BC1124AE3DE20960D42D6FE750B9A9F4412B42D20798245BA452C1573BE83AE`
- `proof_ttl=2026-09-07T20:15:00Z`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"spec","model_id":"composer-2.5","orchestrator_run_id":"auto-20260907-us0131","phase_id":"discovery","proof_issued_at":"2026-09-07T19:15:00Z","proof_ttl_seconds":3600,"role":"po","runtime_proof_id":"rp-auto-20260907-us0131-discovery-po-20260907T191500Z-US-0131","sprint_id":"none","story_id":"US-0131"}`

### Isolation + stop

- `phase_id=discovery`, `role=po`, `story_id=US-0131`, `model_id=composer-2.5`, `fresh_context_marker=po-US0131-discovery-20260907T191500Z-fresh`
- `evidence_ref=docs/product/vision.md ## Discovery Notes — US-0131; docs/product/backlog.md ## US-0131 discovery_notes; handoffs/intake_evidence/US-0131-0132-intake-20260906.json; docs/engineering/state.md discovery checkpoint; handoffs/resume_brief.md`
- **Status**: US-0131 remains **OPEN**. **Next**: `/research` in fresh **tech-lead** subagent. Do not spawn research from this discovery chat. STOP.

---

