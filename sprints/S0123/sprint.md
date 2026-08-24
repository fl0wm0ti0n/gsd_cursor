# Sprint S0123 - Sprint Plan (US-0123)

## Metadata

| Field | Value |
|---|---|
| story_id | US-0123 |
| story_title | Per-role OpenCode model slug routing (multi-provider) |
| sprint_id | S0123 |
| delivery_mode | ultra_lean |
| macro_phase | plan (sprint-plan — terminal canonical phase per ultra_lean; /plan-verify runs standalone per orchestrator brief, role=qa) |
| current_phase | sprint-plan |
| approach | A1 locked |
| companion_DEC | DEC-0123 (Accepted) |
| research_anchor | R-0109 (DQ1..DQ10 LOCKED for US-0123; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 locks preserved) |
| orchestrator_run_id | auto-20260824-01 |
| fresh_context_marker | tl-US0123-sprint-plan-20260824T163000Z-fresh |
| timestamp | 2026-08-24T16:30:00Z (UTC) |
| verdict | PASS |
| decision_gate | false |
| SPRINT_MAX_TASKS | 12 |
| SPRINT_AUTO_SPLIT | 1 |
| task_count | 10 (T-anch + T-001..T-009; within 12; no split) |
| CROSS_MODEL_REVIEW | 1 (model_id=glm-5.2-high required) |
| COMPONENT_SCOPE_MODE | 0 |
| USER_GUIDE_MODE | 0 |
| plan-verify | standalone /plan-verify next (role=qa per orchestrator brief); plan-verify.json NOT written in this spawn |
| backlog_status | OPEN (US-0045 — not mutated) |
| ac_checkboxes | unchecked (US-0045 — not mutated) |

## Scope summary

Ship the third slice of the OpenCode adapter epic (US-0121..US-0126): a **per-role `provider/slug` resolution chain** for the OpenCode host. Each of the eight roles (`po`, `tech-lead`, `dev`, `qa`, `release`, `curator`, `security`, `auto`) can resolve to a real `provider/model-id` slug (DeepSeek, Moonshot, Z.AI/GLM, Anthropic, OpenAI, OpenAI-compatible DashScope/Qwen, …) without leaking vendor IDs into `template/`, without the kit proxying provider traffic, and without amending Cursor's US-0101/US-0102 runtime.

This is an **additive contract + materializer** change. US-0123 adds: (a) one example catalog `template/.opencode/model-catalog.local.example.json` (committed, placeholders only); (b) one materializer `scripts/opencode_model_catalog_apply.py` that reads operator-local `.opencode/model-catalog.local.json` (gitignored) and injects `model: <provider/slug>` into **installed** `.opencode/agents/<role>.md` only — never into `template/`; (c) one installer hook on `--host opencode|both` with triple-installer parity; (d) one validator extension `scripts/model_tier_validate.py --scope opencode-catalog` (extend-not-duplicate per DQ9); (e) one contract test file `tests/us0123_contract_test.py` (8 markers); (f) one runbook h2 one-liner; (g) installer manifest rows; (h) `--scope=opencode-adapter` parity extension. Template agent files (`template/.opencode/agents/*.md`) are NOT edited by US-0123 — `model:` stays omitted in template (inherits US-0122 AC-7); the materializer injects `model:` into installed agent files only, when a local catalog is present.

Single source of truth = `.opencode/model-catalog.local.json` (gitignored, operator-filled) + example `template/.opencode/model-catalog.local.example.json` (committed, placeholders only). Single fail-closed reason code `OPENCODE_MODEL_SLUG_UNKNOWN` for unknown/empty slug when catalog is present (DQ3); malformed JSON reuses `MODEL_CATALOG_INVALID` scope-tagged `opencode-catalog`. When catalog is **absent**, the materializer is a no-op — **no fail-closed** (catalog is optional). OpenCode host is **always `api` mode** (BYOK via `/connect`); the kit does NOT proxy traffic. Auth keys never live in catalog, template, or git (AC-5). Cursor `MODEL_PROVIDER_MODE` / `MODEL_RESOLVE` / `MODEL_TIER_<PHASE>` / `MODEL_<PHASE>` keys remain Cursor-side only (AC-6 compose, not amend).

Out of scope: US-0124 (orchestrator plugin spawn loop + runtime permission-check hook), US-0125 (thin command bodies), US-0126 (full runbook), repo-root `opencode.json`, active kit `.opencode/agents/` mirror, kit-operated proxy for Chinese APIs, Cursor BYOK fixes, embedding keys, plugin spawn, new validator script (default rejected — DQ9 extend in place).

## Acceptance criteria (10) - US-0123 (status OPEN, checkboxes untouched per US-0045)

- **AC-1**: Resolution chain — documented mapping from kit tier/role/phase keys to OpenCode `provider/slug`. Architecture picks the single source of truth (scratchpad vs agent frontmatter); tests assert that choice.
- **AC-2**: Multi-provider examples — operator-local examples cover at least DeepSeek, Moonshot, Z.AI, and one Western provider. Kit does **not** proxy traffic.
- **AC-3**: No vendor IDs in template — grep/`test_us0123_*` fail if `template/` contains live vendor slugs (same family as US-0102). Placeholders only.
- **AC-4**: Unknown slug fail-closed — invalid/empty slug emits a documented reason code (reuse `MODEL_SLUG_UNKNOWN` / `MODEL_OVERRIDE_SLUG_UNKNOWN` analogue, not silent fallback to a random model).
- **AC-5**: Auth store — docs + tests state keys live in OpenCode `/connect` / host auth store, never in plugin logs, git, or template.
- **AC-6**: Compose US-0101/US-0102 — Cursor alias runtime unchanged; this story does not amend DEC-0086/0087 Cursor behavior. OpenCode path is additive.
- **AC-7**: Per-role assignment — at least two roles can be configured to different providers in a local catalog without editing `template/`.
- **AC-8**: Contract tests — `test_us0123_*` cover placeholder-only template, fail-closed unknown slug, example catalog schema, and non-substitution vs `TOKEN_PROFILE`.
- **AC-9**: Chinese APIs required as capability — assignment per role is in scope; kit-operated proxy is out of scope.
- **AC-10**: Tool-calling quality — runbook note (owned with US-0126 if needed) that QA/dev should default to a tool-reliable slug; Chinese API quality is operator model choice.

## Task summaries (10 - T-anch + T-001..T-009)

- **T-anch** (NO-OP / verification): Verify `# US-0123` H1 anchor in `docs/engineering/architecture.md` AFTER `# US-0122` and BEFORE `# US-0089` (DEC-0073 §11); verify DEC-0123 Accepted; verify compose guards 6/6 UNCHANGED baseline (US-0101/DEC-0086, US-0102/DEC-0087, US-0003, US-0122/DEC-0122, US-0121, US-0080); verify 8-marker contract-test list locked in architecture AC-8 table; verify materializer + installer hook contract locked in DEC-0123 §7; verify `template/.opencode/model-catalog.local.example.json` does NOT yet exist; verify `scripts/opencode_model_catalog_apply.py` does NOT yet exist; verify `tests/us0123_contract_test.py` does NOT yet exist; verify `scripts/model_tier_validate.py` does NOT yet have `--scope opencode-catalog`; verify `.opencode/.gitignore` (US-0121 Q10) covers `*.local.json` glob. Record to `sprints/S0123/t-anch-verification.md`. **Critic NB `ik_us0123_sprint_tanch_ceremony_overlap` closed**: T-anch is NO-OP / verification only — NO mutation to `docs/engineering/architecture.md` or `decisions/DEC-0123.md` in /execute; T-anch records baseline observations only (mirrors US-0122 T-anch ceremony). (AC-6, AC-9 baseline; NO-OP / verification only)
- **T-001** (NEW example catalog): Create `template/.opencode/model-catalog.local.example.json` with placeholder `provider/slug` per role per architecture DQ6 LOCKED + DEC-0123 §6. Schema: `{schema_version, providers, roles}` with 8 role keys. Provider block covers DeepSeek, Moonshot, Z.AI, Anthropic, OpenAI + DashScope/Qwen custom OpenAI-compatible (`@ai-sdk/openai-compatible` + `options.baseURL`). Role values are `<your-deepseek-slug>`, `<your-kimi-slug>`, `<your-glm-slug>`, `<your-claude-slug>`, `<your-gpt-slug>` placeholders — NO real model-id slugs in `template/`. ≥2 roles have different providers (AC-7 per-role divergence). (AC-2, AC-7, AC-9)
- **T-002** (NEW materializer): Create `scripts/opencode_model_catalog_apply.py` per architecture DQ7 LOCKED + DEC-0123 §7. Input: `.opencode/model-catalog.local.json` + installed `.opencode/agents/<role>.md` files. Behavior: (a) catalog **absent** → no-op, exit 0, installed agents keep `model:` omitted (no fail-closed); (b) catalog **present** → load + validate schema → for each of 8 roles: if slug is non-empty `provider/slug` and provider declared → inject `model: <provider/slug>` into installed agent's YAML frontmatter (insert if absent; overwrite if present); if slug empty/unknown or provider undeclared → emit `OPENCODE_MODEL_SLUG_UNKNOWN` + exit non-zero (fail-closed); if catalog JSON malformed → emit `MODEL_CATALOG_INVALID` (scope-tagged `opencode-catalog`) + exit non-zero. **Never** writes to `template/`. **Never** reads or writes `.cursor/model-catalog.local.json`. **Never** reads auth credentials. **Critic NB `ik_us0123_placeholder_slug_copy_paste_boundary` closed**: materializer MUST treat `<your-*-slug>` angle-bracket placeholder strings as **unknown** slugs (emit `OPENCODE_MODEL_SLUG_UNKNOWN`, fail-closed) — operators who copy-paste the example catalog without filling in real slugs must NOT silently get placeholder `model:` values injected into installed agents. Placeholder detection: slug matches `^<.*>$` or contains `<your-` substring → unknown. (AC-1, AC-4, AC-5)
- **T-003** (Installer hook — triple-installer parity): `installer.py` / `installer.ps1` / `installer.sh` invoke materializer when `--host opencode|both` AND `.opencode/model-catalog.local.json` exists at install target. If catalog absent → skip materializer (no-op; no fail-closed). If materializer fails (non-zero exit) → surface reason code + exit non-zero. Triple-installer parity: all three use the same trigger condition and the same error surface. The installer does NOT generate the catalog for the operator — operators create `.opencode/model-catalog.local.json` themselves (or copy from example and fill in real slugs). (AC-1, AC-5)
- **T-004** (Validator extension): Extend `scripts/model_tier_validate.py` with `--scope opencode-catalog` per architecture DQ9 LOCKED + DEC-0123 §9 (extend-not-duplicate; new script only if too coupled). Extension adds: (a) `check_template_opencode_agents` — grep `template/.opencode/agents/**/*.md` for `model:` field (must be absent) + forbidden vendor slug patterns (`deepseek|moonshot|kimi|glm|claude|gpt|sonnet|opus|haiku|o1|o3|sk-`); D3 grep scope **excludes** `*.example.json` / `*.local.json`; also grep `template/.opencode/opencode.json{,c}` if present (must not exist in template); (b) `validate_opencode_catalog` — load `.opencode/model-catalog.local.json` (if present) → validate schema (`schema_version`, `providers`, `roles` with 8 role keys) → unknown/empty slug → `OPENCODE_MODEL_SLUG_UNKNOWN` → malformed JSON → `MODEL_CATALOG_INVALID` (scope-tagged `opencode-catalog`); (c) `check_opencode_example_catalog` — load `template/.opencode/model-catalog.local.example.json` → assert placeholder values only (no real model-id slugs) → assert ≥2 roles have different providers (AC-7); (d) reuse existing `check_forbidden_slugs_in_file` helper (extend forbidden-slug list to cover OpenCode agent files + example catalog). **Critic NB `ik_us0123_validator_extension_coupling_fallback` closed**: document in T-004 task note **when to extend `model_tier_validate.py` vs new script** — default = extend in place (DQ9 lock); fall back to new `scripts/opencode_model_catalog_validate.py` ONLY if schema divergence forces a separate validator class (e.g. OpenCode catalog schema cannot share the loader/validation base class with Cursor catalog). Trigger for fallback: `validate_opencode_catalog` cannot reuse >50% of existing `validate_cursor_catalog` helpers, OR scope-tag plumbing requires touching >3 unrelated `--scope` modes. If fallback triggers, raise DEC-0124-class follow-up; do NOT silently split. (AC-3, AC-8)
- **T-005** (Contract tests): Create `tests/us0123_contract_test.py` with 8 markers per architecture AC-8 table: (1) `test_us0123_template_agents_omit_model` [AC-1, AC-3]; (2) `test_us0123_no_vendor_slugs_in_template` [AC-3]; (3) `test_us0123_example_catalog_placeholders_only` [AC-2, AC-3]; (4) `test_us0123_example_catalog_per_role_divergence` [AC-7, AC-9]; (5) `test_us0123_fail_closed_unknown_slug` [AC-4] — includes `<your-*-slug>` placeholder case; (6) `test_us0123_materializer_no_op_when_catalog_absent` [AC-1, AC-4]; (7) `test_us0123_auth_store_never_in_template_or_git` [AC-5]; (8) `test_us0123_compose_cursor_unchanged` [AC-6, AC-8] — includes `TOKEN_PROFILE` orthogonality. Mirror to `template/tests/us0123_contract_test.py` byte-identical for parity pairing. (AC-8)
- **T-006** (Gitignore verification): Verify `.opencode/.gitignore` (US-0121 Q10) covers `*.local.json` glob → `model-catalog.local.json` is covered. If the glob is narrower than `*.local.json`, add `model-catalog.local.json` explicitly. Do not duplicate gitignore entries. T-006 asserts coverage via grep on `.opencode/.gitignore`. (AC-5)
- **T-007** (Runbook stub): Add `## OpenCode model slug routing (US-0123)` h2 to `docs/engineering/runbook.md` as a **one-liner** per DEC-0123 §10 / DQ10 LOCKED: "QA/dev should default to a tool-reliable slug (a model with documented tool-calling support); Chinese API quality is operator model choice. The kit does not endorse a single vendor." US-0126 inherits and expands into a full runbook section. T-007 does NOT author a full runbook section (YAGNI — US-0126 owns it). (AC-10)
- **T-008** (README + parity extension): Extend `scripts/check_intake_template_parity.py` `--scope=opencode-adapter` `OPENCODE_ADAPTER_PAIRS` to cover the example catalog + materializer + validator surface (byte-identical active ↔ template pairs where applicable). Update `its_magic/README.md` to cross-link the OpenCode model slug routing capability + pointer to DEC-0123. Mirror parity script to `template/scripts/check_intake_template_parity.py` byte-identical. (AC-8)
- **T-009** (Installer manifest rows): Add `template/.opencode/model-catalog.local.example.json` + `scripts/opencode_model_catalog_apply.py` source rows under `[opencode_install_include_paths]` in `docs/engineering/context/installer-owned-paths.manifest` AND `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical). Existing rows UNCHANGED — additive rows only. Triple-installer (PS/Bash/Python) reads opencode sections only when `--host` includes opencode (US-0121 compose). (AC-1)

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (resolution chain / SOT) | T-001, T-002, T-003, T-004, T-009 |
| AC-2 (multi-provider examples, no proxy) | T-001 |
| AC-3 (no vendor IDs in template) | T-004, T-005 (markers 1, 2, 3) |
| AC-4 (unknown slug fail-closed) | T-002, T-005 (markers 5, 6) |
| AC-5 (auth store /connect) | T-002, T-003, T-006, T-005 (marker 7) |
| AC-6 (compose US-0101/US-0102) | T-anch (baseline), T-005 (marker 8) |
| AC-7 (per-role assignment) | T-001, T-005 (marker 4) |
| AC-8 (contract tests) | T-005 (all 8 markers), T-008 (parity extension) |
| AC-9 (Chinese APIs as capability) | T-001, T-anch (baseline), T-005 (marker 4) |
| AC-10 (tool-calling quality runbook) | T-007 |

**Surjectivity check**: 10/10 ACs covered (each AC has at least 1 task). No `PLAN_AC_COVERAGE_GAP`.

## Critic carry-ins (3 non-blocking findings from architecture sovereign-critic — not silently dropped)

- `ik_us0123_placeholder_slug_copy_paste_boundary` → T-002 task note: materializer MUST treat `<your-*-slug>` angle-bracket placeholder strings as unknown slugs (emit `OPENCODE_MODEL_SLUG_UNKNOWN`, fail-closed). Operators who copy-paste the example catalog without filling in real slugs must NOT silently get placeholder `model:` values injected into installed agents. Placeholder detection: slug matches `^<.*>$` or contains `<your-` substring → unknown. T-005 marker 5 asserts the placeholder case.
- `ik_us0123_validator_extension_coupling_fallback` → T-004 task note: document when to extend `model_tier_validate.py` vs new script. Default = extend in place (DQ9 lock). Fall back to new `scripts/opencode_model_catalog_validate.py` ONLY if schema divergence forces a separate validator class. Trigger: `validate_opencode_catalog` cannot reuse >50% of existing `validate_cursor_catalog` helpers, OR scope-tag plumbing requires touching >3 unrelated `--scope` modes. If fallback triggers, raise DEC-0124-class follow-up; do NOT silently split.
- `ik_us0123_sprint_tanch_ceremony_overlap` → T-anch task note: T-anch is NO-OP / verification only — NO mutation to `docs/engineering/architecture.md` or `decisions/DEC-0123.md` in /execute; T-anch records baseline observations only (mirrors US-0122 T-anch ceremony). Architecture heading order (# US-0122 → # US-0123 → # US-0089) and DEC-0123 Accepted state are read-only verified, not mutated.

## Compose guards (6/6 UNCHANGED — additive OpenCode catalog path only)

| Compose target | Verification | Result |
|---|---|---|
| US-0101 / DEC-0086 (Cursor tier→alias runtime + `.cursor/model-catalog.local.json`) | OpenCode path additive; Cursor catalog separate; `MODEL_TIER_<PHASE>` / `MODEL_PROVIDER_MODE` Cursor-side only | ✅ untouched |
| US-0102 / DEC-0087 (Cursor direct-slug + role catalog) | OpenCode catalog schema independent; `MODEL_<PHASE>` / `MODEL_RESOLVE` Cursor-side only; volatile-ID rule extended to `template/.opencode/` | ✅ untouched |
| US-0003 (agents gain `model:` on OpenCode) | materializer injects `model:` into installed agents; template agents unchanged | ✅ exists — additive |
| US-0122 / DEC-0122 (permission matrix + `template/.opencode/agents/*.md`) | US-0123 does not edit template agents; materializer writes to installed agents only; `model:` stays omitted in template | ✅ untouched |
| US-0121 (`.opencode/` pack path + `.gitignore` Q10) | `*.local.json` gitignore reused; no new gitignore entry needed (T-006 verifies) | ✅ consumed — additive |
| US-0080 (`TOKEN_PROFILE` orthogonality) | slug routing ≠ token-cost profile; marker 8 asserts | ✅ untouched |

Contract test `test_us0123_compose_cursor_unchanged` (marker 8) enforces at execute boundary. Compose-guards baseline verified read-only in T-anch.

## Task dependency graph

```
[T-anch] --> [T-001] (example catalog) --> [T-002] (materializer) --> [T-003] (installer hook, after T-002)
                                          |
                                          v
                                      [T-004] (validator extension, after T-001)
                                          |
                                          v
                                      [T-006] (gitignore verify, after T-001)
                                          |
                                          v
                                      [T-009] (manifest rows, after T-001)
                                          |
                                          v
                                      [T-008] (README + parity, after T-001 + T-009)
                                          |
                                          v
                                      [T-007] (runbook one-liner, after T-001)
                                          |
                                          v
                                  [T-005] (contract tests last, assert all outputs)
                                          |
                                          v
                                  Integration verification
```

**Execution order (deterministic)**: T-anch → T-001 (example catalog) → T-002 (materializer) → T-003 (installer hook) → {T-004, T-006, T-009 parallel (validator + gitignore + manifest)} → T-008 (README + parity) → T-007 (runbook one-liner) → T-005 (contract tests last, assert all outputs) → integration verification.

## Execute phase role (per DEC-0051 / US-0069)

| Phase | Role | Isolation |
|---|---|---|
| /plan-verify | qa (fresh per BUG-0006) | {phase_id:plan-verify, role:qa} — standalone per orchestrator brief |
| /execute | dev (fresh per BUG-0006) | {phase_id:execute, role:dev} |
| /qa | qa (fresh) | {phase_id:qa, role:qa} |
| /verify-work | qa (fresh) | {phase_id:verify-work, role:qa} |
| /release | release (fresh) | {phase_id:release, role:release} |
| /closure | qe (fresh) | {phase_id:closure, role:qe} |
| /refresh-context | curator (fresh) | {phase_id:refresh-context, role:curator} |

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

| Field | Value |
|---|---|
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0123 |
| sprint_id | S0123 |
| orchestrator_run_id | auto-20260824-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| fresh_context_marker | tl-US0123-sprint-plan-20260824T163000Z-fresh |
| timestamp | 2026-08-24T16:30:00Z (UTC) |
| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 — required) |
| evidence_ref | sprints/S0123/sprint.md, sprints/S0123/tasks.md, sprints/S0123/progress.md, sprints/S0123/summary.md, sprints/S0123/uat.json, sprints/S0123/uat.md, handoffs/tl_to_dev.md (US-0123 prepend), docs/engineering/state.md (sprint-plan checkpoint append-bottom), docs/engineering/architecture.md # US-0123, decisions/DEC-0123.md |

Prior phase proof consumed: `rp-auto-20260824-01-architecture-tech-lead-20260824T162000Z-US-0123` (proof_hash=6959A3AD8A262CF404582DDFA30C7C4E273E66E799DEBF1C13CB8C8BD0E32E73). Sovereign-critic architecture PASS at 2026-08-24T16:28:00Z (anti_slop_aggregate=8; 0 blocking findings; 3 non-blocking carry-forwards routed to task notes above).

## Runtime proof (DEC-0038)

| Field | Value |
|---|---|
| runtime_proof_id | rp-auto-20260824-01-sprint-plan-tech-lead-20260824T163000Z-US-0123 |
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0123 |
| sprint_id | S0123 |
| orchestrator_run_id | auto-20260824-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 — required) |
| proof_issued_at | 2026-08-24T16:30:00Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-08-24T17:30:00Z (UTC) |
| proof_hash | CD814AD66F07A9F9A5C649EF6B0283A4A92179D7502238514B211863C401FEA6 |
| canonical_payload | `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"sprint-plan","proof_issued_at":"2026-08-24T16:30:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260824-01-sprint-plan-tech-lead-20260824T163000Z-US-0123","sprint_id":"S0123","story_id":"US-0123"}` |

## Decision gate

| Field | Value |
|---|---|
| decision_gate | false |
| stop_conditions_met | yes |
| missing_acceptance_criteria | none (10/10 ACs covered by 8 contract-test markers + compose guards + T-007 runbook one-liner) |
| compose_guards | 6/6 UNCHANGED (additive OpenCode catalog path only) |
| dc_check | clean |
| task_count | 10 (within SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1 but no split needed) |
| risks_finalized | 7/7 ACCEPTED (R1..R7 from R-0109 US-0123) + 2 research critic NBs closed (C1 catalog optional vs fail-closed; C2 T-002/T-003 interface) + 3 architecture critic NBs routed to task notes (placeholder boundary; validator coupling fallback; T-anch ceremony overlap) |
| approach | A1 locked |
| Q | DQ1..DQ10 LOCKED for US-0123; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 locks preserved |
| plan-verify readiness | standalone /plan-verify next (role=qa per orchestrator brief); plan-verify.json NOT written in this spawn |
| sovereign_memory_note | `assemble_sovereign_memory_digest(...)` NOT called; no mistakes.jsonl write |

## Definition of done (sprint-plan)

- [x] 10 tasks enumerated (T-anch + T-001..T-009) — within SPRINT_MAX_TASKS=12
- [x] 10/10 ACs covered by 8 contract-test markers + compose guards + T-007 runbook one-liner (surjective)
- [x] Task dependency graph documented
- [x] Execute phase role matrix documented (including standalone /plan-verify per orchestrator brief)
- [x] Compose guards 6/6 UNCHANGED (additive OpenCode catalog path only)
- [x] Critic carry-ins (3) explicitly routed to task notes (not silently dropped)
- [x] Isolation evidence + runtime proof emitted (model_id=glm-5.2-high present)
- [x] Sprint-plan checkpoint appended to `docs/engineering/state.md` (append-bottom; never truncate)
- [x] Sprint-plan handoff prepended to `handoffs/tl_to_dev.md`
- [x] Sprint-plan PASS prepended to `handoffs/resume_brief.md` (→ /plan-verify, role=qa)
- [x] UAT placeholders written (`uat.json` empty steps, `uat.md` ACs no results)
- [x] Backlog status OPEN (US-0045 — not mutated); AC checkboxes untouched

## Next scheduled phase

| Field | Value |
|---|---|
| next_scheduled_phase | `/plan-verify` (role=qa per orchestrator brief; fresh qa subagent per BUG-0006) |
| next_scheduled_role | qa |
| next_sprint_macro | plan (terminal — /plan-verify is the verification gate before build+verify macro) |
| stop_condition | STOP after sprint-plan completes; hand off via artifacts only to /plan-verify in fresh qa subagent per BUG-0006. Do not spawn /plan-verify from this subagent. |
| artifacts_written | sprints/S0123/sprint.md, sprints/S0123/tasks.md, sprints/S0123/progress.md, sprints/S0123/summary.md, sprints/S0123/uat.json, sprints/S0123/uat.md, docs/engineering/state.md (sprint-plan checkpoint append-bottom), handoffs/tl_to_dev.md (US-0123 prepend), handoffs/resume_brief.md (sprint-plan PASS prepend → /plan-verify) |
