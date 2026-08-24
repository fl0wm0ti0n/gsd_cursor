# PO to TL archive pack (2026-08-23)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 8
- First archived heading: `## Discovery handoff — US-0121 OpenCode template pack and installer host mode`
- Last archived heading: `## Discovery handoff — US-0121 OpenCode template pack and installer host mode`
- Verification tuple (mandatory):
  - archived_body_lines=90
  - retained_body_lines=623

---

## Discovery handoff — US-0121 OpenCode template pack and installer host mode

- **Phase completed**: discovery
- **Phase role**: po
- **Story**: US-0121 — OpenCode template pack and installer `--host cursor|opencode|both`
- **Sprint**: (pending)
- **Verdict**: PASS (no DECISION_GATE)
- **Timestamp**: 2026-08-23T07:40:00Z
- **Fresh context marker**: po-US0121-discovery-20260823T074000Z-fresh
- **Runtime proof**: `rp-auto-20260823-01-discovery-po-20260823T074000Z-US-0121` (`proof_hash=9c346006191ee7b9b94d4386708ec8756d7e38cb13d342d09b520f4ef3b6f3dc`, `proof_ttl=2026-08-23T08:40:00Z`)
- **Delivery mode**: ultra_lean
- **Macro phase**: spec (intake already complete; discovery remaining spec phase)
- **Orchestrator run**: auto-20260823-01
- **Status**: OPEN per US-0045. Acceptance checkboxes remain unchecked.

### Summary

Ship an empty-but-valid `template/.opencode/` pack and additive installer `--host cursor|opencode|both` without breaking Cursor. Default remains **cursor-only** until explicit `--host opencode|both`. The masterplan is a brief, not shipped architecture. Plugin v1 vs v2 stays on **R-0109** for `/research` (not an architecture lock here). Epic siblings US-0122..US-0126 remain OPEN and out of this slice.

### Isolation evidence (US-0048 / BUG-0006 / DEC-0029)

- `phase_id=discovery`
- `role=po`
- `fresh_context_marker=po-US0121-discovery-20260823T074000Z-fresh`
- `timestamp=2026-08-23T07:40:00Z` (UTC)
- `evidence_ref=docs/product/backlog.md ## US-0121, docs/product/vision.md ## Discovery Notes — US-0121, docs/product/acceptance.md US-0121 row (unchecked), handoffs/intake_evidence/US-0121-intake-20260822.json, docs/engineering/research.md ## R-0109, docs/product/opencode-adapter-masterplan.md (pack/installer/coexistence headings only)`
- Fresh PO subagent; `assemble_sovereign_memory_digest(...)` NOT called; no write to `mistakes.jsonl`.

### Discovery locks (D1..D11)

- **D1 (`--host`)**: `--host cursor|opencode|both`; omitted = `cursor`; unknown → `INSTALL_HOST_INVALID`. Triple-installer + `its-magic` wrapper.
- **D2 (default cursor-only)**: No implicit opt-in (no scratchpad/env/auto-detect default flip).
- **D3 (pack tree)**: `template/.opencode/{agents,commands,plugins}` (or documented equivalent) + gitignore; empty-but-valid placeholders only.
- **D4 (coexistence)**: `--host cursor` byte-identical on `.cursor/` vs pre-US-0121; `--host opencode` does not touch `.cursor/`; `--host both` keeps both trees.
- **D5 (install/upgrade/clean)**: US-0008 modes unchanged except additive host filter on OpenCode paths.
- **D6 (manifest + triple-installer)**: `installer-owned-paths.manifest` lists `template/.opencode/**`; PS/Bash/Python same `--host` semantics.
- **D7 (parity)**: `--scope=opencode-adapter` (or documented subset this story owns).
- **D8 (secrets/gitignore)**: No API keys, `.env`, or vendor slugs in pack examples (US-0102); gitignore local catalogs/auth.
- **D9 (compose US-0008)**: Additive `--host` only. No VS Code rewrite. No OpenCode fork. No Cursor command-body clones.
- **D10 (epic boundary)**: US-0122..US-0126, standalone runtime out of scope.
- **D11 (UX)**: No new GUI; OpenCode TUI/desktop/IDE; slash names + ASCII reason codes; `--help` is the US-0121 docs hook.

### Compose, do not amend (verified)

- US-0008: additive `--host` only (installer modes/backup/DEC-0045 `its_magic/` unchanged).
- US-0018: packaging delivery path unchanged.
- US-0102: pack must not leak vendor slugs.
- Do not amend US-0001 bodies, US-0003 roles, US-0069 matrix, US-0092 `--invoke-cmd`, US-0101 runtime aliases (later slices).

### DC check

`grep "^## US-0121" docs/engineering/architecture.md` → no matches (expected; H1 in `/architecture`). Not appended to `handoffs/sovereign_deferrals.jsonl`.

### Open questions for `/research` (deepen R-0109; do not close Q1–Q5)

- **R-0109 Q1–Q5 remain open** (plugin API, spawn isolation, headless CLI, provider/slug examples, permission globs). Not US-0121 execute locks.
- **Q6**: Empty-but-valid pack — is repo-root `opencode.json` required?
- **Q7**: Manifest encoding for host-specific paths.
- **Q8**: Confirm `--host` gates host packs only; kernel paths still install (discovery recommendation: yes).
- **Q9**: Active `.opencode/` mirror in this kit repo vs template-only until US-0126.
- **Q10**: Exact gitignore filenames for auth/local catalogs.
- **Q11**: Companion DEC needed? Intake/discovery: none unless `/research` says otherwise. Do not author DEC files here.
- **Q12**: `its-magic` CLI forwards `--host`.

### Risks carried to `/research`

- **R1 (MEDIUM)**: cursor-only install copies `.opencode/` — D2/D4 + `test_us0121_*`.
- **R2 (MEDIUM)**: manifest host encoding — Q7.
- **R3 (LOW–MEDIUM)**: empty pack rejected by stock OpenCode — Q6.
- **R4 (LOW)**: secret/slug leakage — D8.
- **R5 (LOW)**: scope creep into US-0122..US-0126 — D10.

### Strict runtime proof tuple (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260823-01`
- `runtime_proof_id=rp-auto-20260823-01-discovery-po-20260823T074000Z-US-0121`
- `phase_id=discovery`, `role=po`
- `proof_issued_at=2026-08-23T07:40:00Z`, `proof_ttl_seconds=3600`
- Canonical payload (sorted-key JSON): `{"delivery_mode":"ultra_lean","macro_phase":"spec","orchestrator_run_id":"auto-20260823-01","phase_id":"discovery","proof_issued_at":"2026-08-23T07:40:00Z","proof_ttl_seconds":3600,"role":"po","runtime_proof_id":"rp-auto-20260823-01-discovery-po-20260823T074000Z-US-0121","sprint_id":"(pending)","story_id":"US-0121"}`
- `proof_hash=9c346006191ee7b9b94d4386708ec8756d7e38cb13d342d09b520f4ef3b6f3dc`

### Decision gate

- `decision_gate=false`

### Next scheduled phase

- `next_scheduled_phase=/research` (role=tech-lead)
- `stop_condition=STOP after discovery completes; hand off via artifacts only`

