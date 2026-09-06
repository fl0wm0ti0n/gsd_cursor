# PO to TL archive pack (2026-09-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 4
- Retained units in hot file: 8
- First archived heading: `## US-0123 spec PASS — pointer`
- Last archived heading: `## US-0121 — OpenCode adapter epic intake (US-0121..US-0126)`
- Verification tuple (mandatory):
  - archived_body_lines=70
  - retained_body_lines=617

---

## US-0123 spec PASS — pointer

- US-0123 spec (intake+discovery) PASS; Status OPEN; AC-1..AC-10 unchecked; full narrative `handoffs/archive/po-to-tl-pack-20260824.md ## Spec handoff — US-0123`; research PASS (deepened R-0109 DQ1..DQ10 LOCKED — see `handoffs/archive/po-to-tl-pack-20260824-a.md ## US-0123 research PASS — pointer` + `docs/engineering/research.md ## R-0109 ### Deepened findings — US-0123`); next `/architecture` (tech-lead) authors companion DEC-0123 + locks SOT/materializer/validator; proofs intake `6c9aabdc...0468f578` discovery `66d9fa99...d048e5f2` research `FAE07A6C...E24BF351` (model_id=glm-5.2-high).
## Spec handoff — US-0122 OpenCode role agents and Layer-1 permission table

- **Phase completed**: spec (`intake + discovery`). **Role**: po. **Story**: US-0122. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp**: intake 2026-08-24T11:33:00Z; discovery 2026-08-24T11:34:00Z. **Fresh markers**: `po-US0122-intake-20260824T113300Z-fresh`, `po-US0122-discovery-20260824T113400Z-fresh`.
- **Runtime proofs**: intake `rp-auto-20260824-01-intake-po-20260824T113300Z-US-0122` (`proof_hash=3FD8A7B437448E01750F5C3FFC64E57D76B293A015F663CA05533E5CCB943140`, ttl 2026-08-24T12:33:00Z); discovery `rp-auto-20260824-01-discovery-po-20260824T113400Z-US-0122` (`proof_hash=C8B6E58EEC9929156E8F8D71497B998E9FDD4E0AD86C9CD1C2C252362CB8BC3D`, ttl 2026-08-24T12:34:00Z).
- **Intake verdict**: PASS by existing program evidence; no new story ID allocated, no ACs wiped. `handoffs/intake_evidence/US-0121-intake-20260822.json` maps `role-agents-permissions` → [US-0122], `coverage_complete=true`, `missing_topics=[]`, `selected_pack=first-intake-pack`. US-0121 remains DONE; US-0122 remains OPEN.
- **Discovery locks D1–D10**: eight agents (`po`, `tech-lead`, `dev`, `qa`, `release`, `curator`, `security`, `auto`); Layer-1 host permissions are enforcement; short Layer-2 prompts only; PO product-doc allow + production/code deny; orchestrator no phase-artifact writes and Task allow-list only to role agents; security findings-oriented; no `.cursor/agents`/rules/skills/command-body clones; no vendor slugs in template agents; consumes US-0121 `.opencode` path and cursor-only default; `test_us0122_*` inventory/deny/clone/parity surface; architecture must lock final permission matrix.
- **Discovery question count**: 8. **Questions for `/research` / R-0109**: DQ1 exact project file form (`.opencode/agents/*.md` vs `opencode.json` `agent` table); DQ2 exact `edit` permission object syntax and precedence; DQ3 whether deny globs win over broad allow globs; DQ4 `task` allow-list syntax for seven role agents; DQ5 hidden/manual invocation settings for primary `auto` vs role agents; DQ6 whether security findings-only paths need a committed directory; DQ7 minimum contract harness for prompt-ignoring PO denial; DQ8 whether active kit repo mirrors stay template-only until US-0126.
- **Compose guards**: US-0003 / US-0023 / BUG-0006 compose only; do not clone `.cursor/agents` as enforcement. US-0123 owns provider/slug routing; no vendor slugs in template. US-0121 host default remains cursor-only until explicit `--host opencode|both`.
- **Isolation**: `phase_id=intake`, `role=po`, `model_id=gpt-5.5-medium`, `fresh_context_marker=po-US0122-intake-20260824T113300Z-fresh`; `phase_id=discovery`, `role=po`, `model_id=gpt-5.5-medium`, `fresh_context_marker=po-US0122-discovery-20260824T113400Z-fresh`; evidence refs: `docs/product/backlog.md ## US-0122`, `docs/product/vision.md ## Discovery Notes — US-0122`, this handoff.
- **Status**: OPEN. **Next**: `/research` (tech-lead) to deepen **R-0109** for US-0122. `stop_condition=STOP after spec completes; hand off via artifacts only`.

## Discovery handoff — US-0121 OpenCode template pack and installer host mode

- **Phase completed**: discovery. **Role**: po. **Story**: US-0121. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp**: 2026-08-23T07:40:00Z. **Fresh context marker**: `po-US0121-discovery-20260823T074000Z-fresh`.
- **Runtime proof**: `rp-auto-20260823-01-discovery-po-20260823T074000Z-US-0121` (`proof_hash=9c346006191ee7b9b94d4386708ec8756d7e38cb13d342d09b520f4ef3b6f3dc`, ttl 2026-08-23T08:40:00Z).
- **Locks D1–D11**: `--host cursor|opencode|both` (default cursor-only; unknown=`INSTALL_HOST_INVALID`); empty-but-valid `template/.opencode/{agents,commands,plugins}` + gitignore; coexistence (cursor-only byte-identical on `.cursor/`); manifest + triple-installer; `--scope=opencode-adapter`; no secrets/slugs; compose US-0008 additive only; epic US-0122..US-0126 out of scope; no new GUI.
- **R-0109 Q1–Q5 remain open** (not architecture locks). Discovery Q6–Q12 (pack layout, manifest encoding, kernel vs host packs, active vs template, gitignore names, companion DEC, CLI `--host` passthrough) go to `/research`.
- **Isolation**: `phase_id=discovery`, `role=po`, `fresh_context_marker=po-US0121-discovery-20260823T074000Z-fresh`, `timestamp=2026-08-23T07:40:00Z`, `evidence_ref=docs/product/backlog.md ## US-0121 + docs/product/vision.md ## Discovery Notes — US-0121 + this compact hot copy`.
- **Full narrative**: `handoffs/archive/po-to-tl-pack-20260823.md` (triad prefix-archive of this newest-first file; compact copy restored under `PO_TO_TL_HOT_MAX_LINES=650`).
- **Triad rollover**: `triad-rollover|po_to_tl` moved=1 pack=`handoffs/archive/po-to-tl-pack-20260823.md` retained_sections=8 retained_lines=623; `triad-rollover|state` moved=1 pack=`docs/engineering/state-archive/state-pack-20260823.md` then post-append moved=1 pack=`docs/engineering/state-archive/state-pack-20260823-a.md` retained_lines=998.
- **Status**: OPEN. **Next**: `/research` (tech-lead). `stop_condition=STOP after discovery completes; hand off via artifacts only`.

## US-0121 — OpenCode adapter epic intake (US-0121..US-0126)

- **Stories**: US-0121 (first slice) plus OPEN siblings US-0122..US-0126; acceptance rows unchecked.
- **Evidence**: `handoffs/intake_evidence/US-0121-intake-20260822.json` (`[INTAKE_EVIDENCE_VALIDATION_OK]`, first-intake-pack, coverage_complete=true)
- **Research**: **R-0109** stub. Brief: `docs/product/opencode-adapter-masterplan.md`
- **Phase**: intake. **Role**: po. **Verdict**: INTAKE PASS; no DECISION_GATE
- `intake_run_id=cursor-20260822-opencode-adapter-intake`, `writer_id=po-cursor-20260822`
- **Status**: OPEN per US-0045. **Next**: `/discovery` (fresh PO) for **US-0121**; US-0122–US-0126 remain OPEN.

### Isolation evidence (US-0048 / BUG-0006)

- `phase_id=intake`; `role=po`; `fresh_context_marker=po-US0121-intake-20260822T211500Z-fresh`; `timestamp=2026-08-22T21:15:00Z`

### Summary

Host-adapter on stock OpenCode: kernel + Python validators + `.opencode/` pack + one orchestrator plugin. Cursor pack stays. Default install remains **cursor-only** until `--host opencode|both`. Plugin v1 vs v2 deferred to `/research`. Standalone runtime is a separate program.

### Split rationale (US-0051)

Workflow-step slices (operator accepted via masterplan): **US-0121** pack+installer+coexistence; **US-0122** roles+permissions (success test c); **US-0123** `provider/slug`; **US-0124** spawn-only plugin (success tests a,d) + US-0092 `--invoke-cmd`; **US-0125** thin commands + validator bridge (success test b); **US-0126** runbook + `--scope=opencode-adapter`. Do not clone US-0001–US-0119.

### Assumptions locked

Default install host remains cursor-only until explicit `--host opencode|both` opt-in; OpenCode plugin v1 vs v2 deferred to `/research`.

### Compose, do not amend

US-0008 (additive `--host` only); US-0003 roles; US-0069 matrix; US-0092 outer driver; US-0101/US-0102 without Cursor aliases as runtime; BUG-0006 spawn-only; US-0023 isolation. Do not port US-0095 — the plugin is the OpenCode chain.

### Risks

R1 spawn isolation / V2 `subtask` ignored (fail closed; **R-0109** Q1–Q2). R2 dual-host parity. R3 plugin API unknown. R4 template slug leakage. R5 sovereign/standalone scope creep (deferred plan areas).

### Next scheduled phase

`/discovery` fresh PO for **US-0121**. Then `/research` (tech-lead) to deepen **R-0109**, then `/architecture`.

### Triad rollover

- `triad-rollover|state` moved=1 pack=`docs/engineering/state-archive/state-pack-20260822.md` retained_checkpoints=12 retained_lines=978
- `triad-rollover|po_to_tl` moved=1 pack=`handoffs/archive/po-to-tl-pack-20260822.md` retained_lines=580 retained_sections=7
- Full intake section also stored in that po_to_tl pack (prefix archive on newest-first file). This compact copy restored to the hot surface under `PO_TO_TL_HOT_MAX_LINES=650`.

