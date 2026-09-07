# PO to TL archive pack (2026-09-07)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 10
- First archived heading: `## Discovery handoff — BUG-0016 OpenCode Layer-1 permissions vs kit duties`
- Last archived heading: `## Discovery handoff — BUG-0016 OpenCode Layer-1 permissions vs kit duties`
- Verification tuple (mandatory):
  - archived_body_lines=52
  - retained_body_lines=639

---

## Discovery handoff — BUG-0016 OpenCode Layer-1 permissions vs kit duties

- **Phase completed**: discovery. **Role**: po. **Bug**: BUG-0016 only. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp (UTC)**: 2026-09-06T18:20:00Z. **Fresh marker**: `po-BUG0016-discovery-20260906T181957Z-fresh`.
- **Orchestrator**: `orchestrator_run_id=auto-20260906-bug0016`, `delivery_mode=ultra_lean`, macro=`spec` (intake already DONE — not re-intaken).
- **Sibling boundary**: BUG-0015 is **DONE** (dispatch fix shipped) — out of scope except compose note that auto spawn-only Task path may now work; this segment is **permissions matrix vs kit duties only**. US-0131/US-0132 out of scope.
- **Gap confirmed (narrow-read)**: `.opencode/agents/*.md` + `template/.opencode/agents/*.md` peers are byte-identical and match `decisions/DEC-0122.md` §2 literally; incompatible with kit phase contracts (validators + real sprint/handoff paths).

### Discovery locks D1–D8

| ID | Lock |
|----|------|
| **D1** | Validator roles **`po` / `tech-lead` / `curator`**: change `bash: deny` → **`bash: ask`** (parity with `dev`/`qa`/`release`). Reject `bash: allow`. Optional bash **object** allowlist (`python *` → ask, `*` → deny last) is a research refinement only — not required to unblock duties. |
| **D2** | **PO edit** add allows: `handoffs/intake_evidence/**`, `handoffs/resume_brief.md`; keep `docs/product/**` + `handoffs/po_to_tl.md`; `**` → deny **last**. Success test (c) preserved (no production/code allow). Whether PO also needs `docs/engineering/state.md` for phase checkpoints → DQ2. |
| **D3** | Replace literal placeholder globs `sprints/Sxxxx/…` with real OpenCode minimatch **`sprints/S*/…`** for tech-lead (`sprint.md`, `tasks.md`), dev (`progress.md`, `qa-findings.md`), qa (qa-findings / plan-verify / verify-work / uat paths). Exact pattern (`S*` vs `S[0-9]*` vs `sprints/*/`) → DQ3. |
| **D4** | **tech-lead** + **curator** get `bash: ask` so triad/`enforce-triad-hot-surface.py` and research/architecture validators can run under operator prompt (same posture as D1). |
| **D5** | **release** edit add: `sprints/S*/release-findings.md` + `handoffs/verify-work-to-release.md` (kit uses both `verify_to_release.md` and `verify-work-to-release.md`); keep existing release handoff/CHANGELOG allows; `bash: ask` unchanged. |
| **D6** | **Amend DEC-0122 §2** as the primary matrix SOT (bug-fix of US-0122 contract). Optional thin companion **DEC-0130** at `/architecture` for audit trail only — must not become a second competing matrix. Do not reopen US-0122 as a feature story. |
| **D7** | Tests: extend **static permission-object harness** — additive `test_bug0016_*` and/or amend `us0122_*` markers; assert bash postures, new allow globs, `S*` not `Sxxxx`, deny-last ordering, no production allow for non-dev; active↔template parity. **No live OpenCode probe in CI**. |
| **D8** | Boundaries: BUG-0015 DONE = compose note only; US-0131/US-0132 do not expand; `security` (`edit: deny`, `bash: ask`) and `auto` (spawn-only Task allow-list) stay in-contract unless research finds a duty contradiction. |

### Research questions DQ1–DQ8 (for `/research` → **R-0115**)

1. **DQ1**: Confirm OpenCode bash object-form command patterns (`python *`, `python scripts/*`) vs shorthand `ask` — least-privilege recommendation for po/tl/curator without blocking validators.
2. **DQ2**: Does PO Layer-1 edit need `docs/engineering/state.md` (and/or triad-related paths) for phase-checkpoint duties, or do orchestrator/curator own those writes on OpenCode?
3. **DQ3**: Exact sprint glob string that matches real ids (`S0131`, `S-BUG0014`) under OpenCode minimatch — lock `sprints/S*/file` vs alternatives; prove `Sxxxx` never matches.
4. **DQ4**: Curator/tech-lead required script inventory (validators + `enforce-triad-hot-surface.py` + materialize) — any bash object patterns beyond shorthand `ask`?
5. **DQ5**: Release path completeness — any other missing owned writes (`resume_brief.md`, `state.md`, `runbook.md`) beyond release-findings + verify-work-to-release?
6. **DQ6**: Amend-in-place DEC-0122 revision shape vs thin companion DEC-0130 — single SOT rule; impact on `test_us0122_*` vs new `test_bug0016_*`.
7. **DQ7**: Minimal static harness marker list (expected ≥6) covering D1–D5 + success test (c); fixture strategy without live host.
8. **DQ8**: Compose guards with BUG-0015 DONE / US-0124 plugin write-guard — any Layer-1 vs plugin double-deny interaction to document?

### Intake evidence (already DONE — do not re-intake)

- `handoffs/intake_evidence/BUG-0016-intake-20260906.json` (`small-intake-pack`, `[INTAKE_EVIDENCE_VALIDATION_OK]`)
- Research refs to deepen: `R-0109` (US-0122 permission locks); `decisions/DEC-0122.md` §2

### Runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260906-bug0016-discovery-po-20260906T182000Z-BUG-0016`
- `proof_hash=1381C92191BD8EF182ADF0942BD68777D2A45613C5808497311B2BCC06C18935`
- `proof_ttl=2026-09-06T19:20:00Z`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"spec","model_id":"composer-2.5","orchestrator_run_id":"auto-20260906-bug0016","phase_id":"discovery","proof_issued_at":"2026-09-06T18:20:00Z","proof_ttl_seconds":3600,"role":"po","runtime_proof_id":"rp-auto-20260906-bug0016-discovery-po-20260906T182000Z-BUG-0016","sprint_id":"none","story_id":"BUG-0016"}`

### Isolation + stop

- `phase_id=discovery`, `role=po`, `bug_id=BUG-0016`, `fresh_context_marker=po-BUG0016-discovery-20260906T181957Z-fresh`
- `evidence_ref=docs/product/vision.md ## Discovery Notes — BUG-0016; docs/product/backlog.md ### BUG-0016 discovery_notes; handoffs/intake_evidence/BUG-0016-intake-20260906.json; decisions/DEC-0122.md §2; .opencode/agents/*.md; template/.opencode/agents/*.md; docs/engineering/state.md discovery checkpoint; handoffs/resume_brief.md`
- **Status**: BUG-0016 remains **OPEN**. **Next**: `/research` in fresh **tech-lead** subagent. Do not spawn research from this discovery chat. STOP.

---

