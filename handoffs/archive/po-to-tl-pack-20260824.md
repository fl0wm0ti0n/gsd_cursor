# PO to TL archive pack (2026-08-24)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 10
- First archived heading: `## Spec handoff — US-0123 Per-role OpenCode model slug routing (multi-provider)`
- Last archived heading: `## Spec handoff — US-0123 Per-role OpenCode model slug routing (multi-provider)`
- Verification tuple (mandatory):
  - archived_body_lines=18
  - retained_body_lines=647

---

## Spec handoff — US-0123 Per-role OpenCode model slug routing (multi-provider)

- **Phase completed**: spec (`intake + discovery` merged; ultra_lean). **Role**: po. **Story**: US-0123. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Orchestrator run**: `auto-20260824-01` (drain-advance from US-0122 DONE). **Macro phase**: spec (intake + discovery). **Delivery mode**: ultra_lean.
- **Timestamps**: intake 2026-08-24T15:48:00Z; discovery 2026-08-24T15:52:00Z (UTC). **Fresh markers**: `po-US0123-intake-20260824T154800Z-fresh`, `po-US0123-discovery-20260824T155200Z-fresh`.
- **Model**: `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required on isolation).
- **Runtime proofs (DEC-0038)**:
  - intake `rp-auto-20260824-01-intake-po-20260824T154800Z-US-0123` (`proof_hash=6c9aabdc49ea8c6c4f1285b1c7a6146cd43d6e8b7bcdc4a8174dbacb0468f578`, ttl 2026-08-24T16:48:00Z).
  - discovery `rp-auto-20260824-01-discovery-po-20260824T155200Z-US-0123` (`proof_hash=66d9fa996e2e63eeff14bcf626828c110f1bb854cebc1c3511e503fad048e5f2`, ttl 2026-08-24T16:52:00Z).
- **Intake verdict**: PASS by existing program evidence; **no new story ID allocated**, no ACs wiped, intake evidence JSON not mutated. `handoffs/intake_evidence/US-0121-intake-20260822.json` maps `model-slug-routing` → [US-0123], `coverage_complete=true`, `missing_topics=[]`, `selected_pack=first-intake-pack`. US-0121 DONE, US-0122 DONE; US-0123 remains OPEN; AC-1..AC-10 remain the contract; acceptance checkboxes unchecked.
- **Source-of-truth question for `/research` (AC-1)**: where does the kit-tier/role/phase → OpenCode `provider/slug` mapping live? Candidates: (a) `.cursor/scratchpad.local.md` `MODEL_*` keys; (b) `model:` YAML frontmatter in `template/.opencode/agents/<role>.md`; (c) a **local-only** catalog file (e.g. `.opencode/model-catalog.local.json`, gitignored). Architecture must pick one; tests assert that choice. **Not locked here** — primary DQ for `/research`.
- **Discovery locks D1–D10**: D1 resolution chain shape (deterministic, single-source-of-truth, testable); D2 multi-provider examples (DeepSeek, Moonshot, Z.AI/GLM, one Western) in local-only files; D3 no vendor IDs in `template/` (US-0102 family grep); D4 unknown slug fail-closed (`MODEL_SLUG_UNKNOWN` analogue, no silent fallback); D5 auth store in OpenCode `/connect` (never logs/git/template); D6 compose US-0101/US-0102 additive (Cursor aliases not OpenCode runtime); D7 ≥2 roles to different providers without editing `template/`; D8 `test_us0123_*` contract tests (placeholder-only, fail-closed, catalog schema, non-substitution vs TOKEN_PROFILE); D9 Chinese APIs as capability (no kit proxy); D10 tool-calling quality runbook note (owned with US-0126 if needed).
- **Discovery question count**: 10. **Questions for `/research` (R-0109)**: DQ1 source of truth (scratchpad vs agent `model:` frontmatter vs local catalog) — primary; DQ2 placeholder vs omit `model:` in template agents; DQ3 fail-closed reason-code family (`MODEL_SLUG_UNKNOWN` analogue vs `OPENCODE_*` namespace); DQ4 catalog file path (`.opencode/model-catalog.local.json` local-only vs reuse `.cursor/model-catalog.local.json`); DQ5 per-role vs per-phase mapping (US-0069 role→phase bridge vs new `MODEL_ROLE_*` keys); DQ6 Chinese API examples without vendor IDs (placeholder convention); DQ7 compose with US-0122 agents (additive `model:` later vs separate catalog reference); DQ8 provider mode (OpenCode = always `api` BYOK vs Cursor-managed); DQ9 validator surface (new `model_slug_validate.py` vs extend existing US-0101/US-0102 validators); DQ10 tool-calling quality note ownership (US-0123 stub vs defer entirely to US-0126).
- **Compose guards**: US-0101 / DEC-0086 compose only (no Cursor `fast`/`inherit` as OpenCode runtime); US-0102 / DEC-0087 compose only (no vendor IDs in `template/`); US-0003 agents gain `model:` on OpenCode; US-0122 / DEC-0122 permission matrix unchanged (US-0122 AC-7 forbids real vendor slugs; US-0123 owns real slug resolution, additive later); US-0121 host default remains cursor-only until explicit `--host opencode|both`; US-0080 TOKEN_PROFILE orthogonal (no substitution).
- **Risks (intake + discovery)**: R1 vendor slug leakage in `template/` (AC-3); R2 unknown/empty slug silent fallback (AC-4); R3 source-of-truth ambiguity (AC-1); R4 Chinese API examples with live vendor IDs/keys (AC-2, AC-5); R5 per-role vs per-phase granularity mismatch (AC-1, AC-7); R6 kit accidentally proxies provider traffic (AC-2). All routed to `/research` for deepening.
- **Isolation**: `phase_id=intake`, `role=po`, `model_id=glm-5.2-high`, `fresh_context_marker=po-US0123-intake-20260824T154800Z-fresh`; `phase_id=discovery`, `role=po`, `model_id=glm-5.2-high`, `fresh_context_marker=po-US0123-discovery-20260824T155200Z-fresh`; evidence refs: `docs/product/backlog.md ## US-0123`, `docs/product/vision.md ## Intake Notes — US-0123` + `## Discovery Notes — US-0123`, this handoff.
- **Status**: OPEN. **Next**: `/research` (tech-lead) to deepen **R-0109** for US-0123 (DQ1..DQ10 remain open; do not treat as architecture locks), then `/architecture` to lock the resolution chain + source of truth. `stop_condition=STOP after spec completes; hand off via artifacts only`.

