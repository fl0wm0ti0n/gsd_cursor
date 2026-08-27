# Sprint S0130 - Sprint Plan (US-0130)

## Metadata

| Field | Value |
|---|---|
| story_id | US-0130 |
| story_title | Operator-pinned sovereign-critic model (catalog role + scratchpad override) |
| sprint_id | S0130 |
| delivery_mode | ultra_lean |
| macro_phase | plan (sprint-plan terminal; /plan-verify merged into build+verify under QA per ultra_lean) |
| current_phase | sprint-plan |
| approach | A1 locked (from R-0112 DQ1–DQ8) |
| companion_DEC | none (compose DEC-0104 §5 / DEC-0087 / DEC-0086; no new fail-closed family; A6 rejected DEC-0130) |
| research_anchor | R-0112 (DQ1–DQ8 LOCKED) |
| orchestrator_run_id | auto-20260826-01 |
| fresh_context_marker | tl-US0130-sprint-plan-20260826T215200Z-fresh |
| timestamp | 2026-08-26T21:52:00Z (UTC) |
| model_id | cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 — required on isolation) |
| verdict | PASS |
| decision_gate | false |
| SPRINT_MAX_TASKS | 12 |
| SPRINT_AUTO_SPLIT | 1 |
| task_count | 8 (T-anch + T-001..T-007; within 12; no split) |
| COMPONENT_SCOPE_MODE | 0 |
| USER_GUIDE_MODE | 0 |
| plan-verify | ultra_lean — merged into build+verify under QA; plan-verify.json NOT written here |
| backlog_status | OPEN (US-0045 — not mutated; acceptance L158 unchecked) |
| critic_carry_ins | 0 new blocking; 3 architecture critic NBs `a0130ar-*` status=resolved non-blocking — routed as awareness into /execute (below) |

## Scope summary

Ship the operator pin overlay for **US-0130**: prepend a dedicated overlay inside `select_critic_model` (`scripts/sovereign_critic_lib.py` L236–267) so `/sovereign-critic` can be pinned the same way operators pin PO/SA/DEV. Precedence: exact hyphen pin `MODEL_SOVEREIGN-CRITIC` (via `phase_to_model_key("sovereign-critic")`) > optional catalog `roles.critic` when `MODEL_RESOLVE=role_catalog` > existing US-0104 opposition/`dev` fallback **UNCHANGED**. Same-slug collision keeps `CROSS_MODEL_DEGRADED_MODE` (not a hard stop). One global critic for all producer phases. Optional `critic` is an allowlist overlay (`CATALOG_OPTIONAL_ROLE_KEYS`), **not** added to required `CATALOG_ROLE_KEYS`. Hyphen exact — no underscore alias `MODEL_SOVEREIGN_CRITIC`. Examples + installer compose US-0112: add `critic` to v2 role examples; ship `role-based-balanced_cursor_only.json` as 9th example with `critic=composer-2.5-fast`; **never** write `model-catalog.local.json`.

This is an **additive overlay + validator allowlist + examples/installer + docs + parity + contract-test** change. No new fail-closed code family. No companion DEC. 10 `test_us0130_*` markers in `tests/us0130_contract_test.py` (+ template mirror). Scratchpad DQ8 comment sites (no live pin assignment). Runbook `#### Degraded fallback troubleshooting` pin-precedence note. `SOVEREIGN_CRITIC_PAIRS` add `sovereign_critic_lib.py`; `MODEL_TIER_OVERRIDES_PAIRS` add cursor_only json pair.

Out of scope: adding `critic` to required `CATALOG_ROLE_KEYS` (A2 rejected); registering `sovereign-critic` in `PHASE_LOGICAL_ROLE` (A3 rejected); underscore alias (A4 rejected); hard-stop same-slug (A5 rejected); companion DEC-0130 (A6 rejected); opening `additionalProperties` on `roles` (A7 rejected); per-lens / per-producer-phase critic models (A8 rejected); reopening US-0127/US-0128; mutating US-0129; amending US-0104 findings JSONL / lenses / `CROSS_MODEL_*` keys; writing `model-catalog.local.json`; ticking acceptance L158; marking US-0130 DONE.

## Execute awareness (architecture critic NBs — 0 blocking)

Sovereign-critic of architecture PASS (`tl-US0130-sovereign-critic-architecture-20260826T215000Z-fresh`; anti_slop=8; 0 blocking). Route these resolved NBs as execute awareness — do not re-open them as work:

| Finding | Issue key | Execute awareness |
|---|---|---|
| `a0130ar-challenger-001` | `ik_us0130_arch_proof_and_overlay_gaps` | **T-001** overlay must actually consume `MODEL_SOVEREIGN-CRITIC` via `phase_to_model_key("sovereign-critic")` (hyphen exact). Do not consume `MODEL_SOVEREIGN_CRITIC`. Pin then optional `roles.critic` when `role_catalog` then opposition UNCHANGED. Do not pass a newly loaded catalog into `_resolve_slug_for_tier`. Same-slug keeps `degraded=True`. |
| `a0130ar-architect-002` | `ik_us0130_arch_layer_coupling` | Keep layering: T-001 owns `select_critic_model` overlay; T-002 owns `CATALOG_OPTIONAL_ROLE_KEYS` + validator empty-present-critic; T-003 owns examples/installer; T-004 owns scratchpad comments (no live assignment); T-005 owns 10 markers; T-006 owns runbook; T-007 owns parity pairs. Do not add `critic` to `CATALOG_ROLE_KEYS`. Do not register synthetic phase. |
| `a0130ar-subtractor-003` | `ik_us0130_arch_scope_discipline` | Do not mark US-0130 DONE; do not tick L158; 10 markers are required (not YAGNI); T-anch is read-only ceremony — no architecture.md mutation in /execute; do not author DEC-0130; do not write `model-catalog.local.json`. |

## Acceptance criteria (9) - US-0130 (status OPEN, acceptance L158 unchecked per US-0045)

- **AC-1**: Scratchpad pin — Document `MODEL_SOVEREIGN-CRITIC=<slug>` (synthetic phase; hyphenated key). Highest precedence for critic spawn. Vendor slugs live in `.cursor/scratchpad.local.md` only; template comments use placeholders.
- **AC-2**: Catalog `roles.critic` — Additive optional v2 role key. When present, resolver uses it after the scratchpad pin. When absent, existing v2 catalogs remain valid (no forced migration / no fail-closed missing-key for `critic`).
- **AC-3**: `select_critic_model` precedence — `MODEL_SOVEREIGN-CRITIC` > `roles.critic` (when `MODEL_RESOLVE=role_catalog`) > current opposition/`dev` fallback. Synthetic-phase lookup must actually consume the pin (no ignored hyphen/underscore key mismatch).
- **AC-4**: Collision policy — If resolved critic slug equals producer slug, keep `degraded_mode=true` / `CROSS_MODEL_DEGRADED_MODE` single-model-multi-lens. Not a hard stop.
- **AC-5**: One global critic — v1 is one critic model for all producer phases. Out of scope: per-lens slugs; per-producer-phase critic overrides.
- **AC-6**: Contract tests — `test_us0130_*` cover pin-wins, catalog critic hit, omitted-key fallback, same-slug degraded path, and US-0104 findings-schema compose guard.
- **AC-7**: Compose do not amend — US-0104 findings JSONL / lenses / `CROSS_MODEL_REVIEW`+threshold+rework keys / anti-slop formula unchanged. US-0101 default phase-tier matrix unchanged. US-0102 canonical-phase precedence unchanged.
- **AC-8**: Examples + installer (US-0112 compose) — Role-based example catalogs (including `.cursor/model-catalog.local.example.role-based-balanced_cursor_only.json` and template mirrors) include a `critic` key. Installer/manifest ships updated examples; **never** writes `model-catalog.local.json`.
- **AC-9**: Docs + parity — Scratchpad CROSS_MODEL / MODEL comments, runbook critic troubleshooting, architecture `# US-0130`, template parity for touched catalog/scratchpad/lib/command surfaces.

## Task summaries (8 - T-anch + T-001..T-007)

- **T-anch** (NO-OP / verification): Verify `# US-0130` H1 in `docs/engineering/architecture.md` at L1815 (after `# US-0128` L1671, before `# US-0091` L1971); verify approach A1 + R-0112 DQ1–DQ8 LOCKED; verify compose-do-not-amend 9/9; verify 10-marker list locked; verify `select_critic_model` gap L236–267 still present; verify `CATALOG_ROLE_KEYS` has no `critic`; verify cursor_only example lacks `critic` and is not in installer lists; verify `tests/us0130_contract_test.py` does NOT yet exist. Record to `sprints/S0130/t-anch-verification.md`. NO mutation to `architecture.md` in /execute.
- **T-001** (AC-1 consume + AC-3 + AC-4 + AC-5 — overlay): Prepend overlay in `select_critic_model` per DQ2/DQ3/DQ7; + template mirror.
- **T-002** (AC-2 — optional catalog role): `CATALOG_OPTIONAL_ROLE_KEYS` + extra-key subtract + validator empty-present-critic; + template mirrors.
- **T-003** (AC-8 — examples + installer): v2 example `critic` keys + ship cursor_only as 9th with `critic=composer-2.5-fast` + manifest/installer lists; never write `model-catalog.local.json`.
- **T-004** (AC-1 docs + AC-9 — scratchpad comments): DQ8 comment sites; no live `MODEL_SOVEREIGN-CRITIC=` assignment.
- **T-005** (AC-6 + AC-7 — contract tests): `tests/us0130_contract_test.py` 10 markers + template mirror.
- **T-006** (AC-9 — runbook): `#### Degraded fallback troubleshooting` pin-precedence note; + template mirror.
- **T-007** (AC-9 — parity): `SOVEREIGN_CRITIC_PAIRS` add `sovereign_critic_lib.py`; `MODEL_TIER_OVERRIDES_PAIRS` add cursor_only json pair.

Execution order: T-anch → T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 (acyclic; overlay first, then schema, then examples, then docs/tests/parity).

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (Scratchpad pin) | T-001 (consume pin), T-004 (document pin), T-005 (markers 1, 6) |
| AC-2 (Catalog `roles.critic`) | T-002, T-005 (markers 2, 7, 8) |
| AC-3 (`select_critic_model` precedence) | T-001, T-005 (markers 1, 2, 3, 6) |
| AC-4 (Collision policy) | T-001, T-005 (marker 4) |
| AC-5 (One global critic) | T-001, T-004, T-006 |
| AC-6 (Contract tests) | T-005 (all 10 markers) |
| AC-7 (Compose do not amend) | T-anch, T-005 (marker 5) |
| AC-8 (Examples + installer) | T-003, T-005 (markers 9, 10) |
| AC-9 (Docs + parity) | T-004, T-006, T-007 |

**Surjectivity check**: 9/9 ACs covered (each AC has at least 1 task). No `PLAN_AC_COVERAGE_GAP`.

## Risks (R1–R5 — accepted from architecture)

| Risk | Severity | Mitigation in this sprint |
|---|---|---|
| R1 Operators assume pin participates in canonical-phase resolution | MEDIUM | T-004 DQ8 comments + T-006 runbook; T-005 marker 6; do not register synthetic phase |
| R2 Shipping cursor_only as 9th installer file expands US-0112 payload | MEDIUM | T-003 AC-8 names the file; never write `model-catalog.local.json`; markers 9+10 |
| R3 `_resolve_slug_for_tier` hyphen/underscore mismatch remains | LOW | DQ7 forbids fixing it here; T-001 overlay bypasses that helper for pin/catalog |
| R4 Empty-present `critic` reuses `MODEL_CATALOG_SCHEMA_V2_INVALID` | LOW | T-002 error message names the `critic` key (text, not a new code); marker 7 |
| R5 Pin slug not in catalog under `role_catalog` → `MODEL_OVERRIDE_SLUG_UNKNOWN` | LOW | Compose DEC-0087 §4; T-004 documents pin slug must appear in catalog when required |

## Compose guards (9/9 UNCHANGED — additive overlay + validator allowlist + examples/installer + docs + parity + contract-test only)

| Compose target | Verification | Result |
|---|---|---|
| US-0104 / DEC-0104 | overlay prepend; opposition + collision UNCHANGED; marker 5 | compose |
| US-0102 / DEC-0087 | chain canonical-phase-only; `critic` not in required-set; synthetic phase not registered | compose |
| US-0101 / DEC-0086 | v1 examples unchanged; matrix not extended | compose |
| US-0112 | add `critic` to v2 role examples; ship cursor_only as 9th; never write local.json | compose |
| US-0127 / US-0128 | hygiene / smoke surrogate not reopened | compose |
| US-0129 | architecture linkage guard untouched | compose |
| US-0123 | OpenCode example out of scope | compose |
| R-0088 | Cursor Task allowlist / BYOK document-only | compose |
| US-0045 / US-0048 / US-0056 | Status stays OPEN; fresh isolation; this phase mints its own proof | compose |

## Execute phase role (per DEC-0051 / US-0069)

| Phase | Role | Isolation |
|---|---|---|
| /execute | dev (fresh per BUG-0006) | {phase_id:execute, role:dev} |
| /qa | qa (fresh) | {phase_id:qa, role:qa} — creates plan-verify.json within build+verify per ultra_lean |
| /verify-work | qa (fresh) | {phase_id:verify-work, role:qa} |
| /release | release (fresh) | {phase_id:release, role:release} |
| /closure | qe (fresh) | {phase_id:closure, role:qe} |
| /refresh-context | curator (fresh) | {phase_id:refresh-context, role:curator} |

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

| Field | Value |
|---|---|
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0130 |
| sprint_id | S0130 |
| orchestrator_run_id | auto-20260826-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| fresh_context_marker | tl-US0130-sprint-plan-20260826T215200Z-fresh |
| timestamp | 2026-08-26T21:52:00Z (UTC) |
| model_id | cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 — required) |
| evidence_ref | sprints/S0130/sprint.md, sprints/S0130/tasks.md, sprints/S0130/progress.md, sprints/S0130/uat.json, sprints/S0130/uat.md, handoffs/tl_to_dev.md (US-0130 prepend), docs/engineering/state.md (sprint-plan checkpoint append-bottom + traceability row), docs/engineering/architecture.md # US-0130 (L1815 — not mutated), handoffs/resume_brief.md |

Prior phase proof consumed: `rp-auto-20260826-01-architecture-tech-lead-20260826T214500Z-US-0130` (proof_hash=B071AE0659D99E2513304490BD3D191550631E7564398EEEC4485BD556FD8B4D, ttl 2026-08-26T22:45:00Z — independent SHA-256 MATCH; consumed at 2026-08-26T21:52:00Z before RUNTIME_PROOF_STALE). Sovereign-critic architecture PASS at 2026-08-26T21:50:00Z (anti_slop_aggregate=8; 0 blocking findings; 3 NBs `a0130ar-*` status=resolved).

## Runtime proof (DEC-0038)

| Field | Value |
|---|---|
| runtime_proof_id | rp-auto-20260826-01-sprint-plan-tech-lead-20260826T215200Z-US-0130 |
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0130 |
| sprint_id | S0130 |
| orchestrator_run_id | auto-20260826-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| model_id | cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 — required) |
| proof_issued_at | 2026-08-26T21:52:00Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-08-26T22:52:00Z (UTC) |
| proof_hash | 5D0ADA062FE675333EF06E56DBC4649D22A2045C08D71456C7963893178CFED1 |
| canonical_payload | `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260826-01","phase_id":"sprint-plan","proof_issued_at":"2026-08-26T21:52:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260826-01-sprint-plan-tech-lead-20260826T215200Z-US-0130","sprint_id":"S0130","story_id":"US-0130"}` |

## Decision gate

| Field | Value |
|---|---|
| decision_gate | false |
| stop_conditions_met | yes |
| missing_acceptance_criteria | none (9/9 ACs covered; 10 contract-test markers; compose guards 9/9) |
| compose_guards | 9/9 UNCHANGED |
| dc_check | clean (`# US-0130` H1 already added in /architecture at L1815) |
| task_count | 8 (within SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1 but no split needed) |
| risks_finalized | 5/5 ACCEPTED (R1..R5) |
| approach | A1 locked |
| companion_DEC | none |
| plan-verify readiness | ultra_lean — /plan-verify merged into build+verify under QA; plan-verify.json NOT written in this spawn |
| sovereign_memory_note | `assemble_sovereign_memory_digest(...)` NOT called; no mistakes.jsonl write |

## Definition of done (sprint-plan)

- [x] 8 tasks enumerated (T-anch + T-001..T-007) — within SPRINT_MAX_TASKS=12
- [x] 9/9 ACs covered by 10 contract-test markers + compose guards 9/9 (surjective)
- [x] Task dependency graph documented
- [x] Execute phase role matrix documented (ultra_lean — /plan-verify merged into build+verify under QA)
- [x] Compose guards 9/9 UNCHANGED
- [x] Critic carry-ins (3 non-blocking from architecture sovereign-critic) routed as execute awareness
- [x] Isolation evidence + runtime proof emitted (model_id=cursor-grok-4.6-high present)
- [x] Sprint-plan checkpoint appended to `docs/engineering/state.md`
- [x] Sprint-plan handoff prepended to `handoffs/tl_to_dev.md`
- [x] Sprint-plan PASS prepended to `handoffs/resume_brief.md` (-> /execute)
- [x] UAT placeholders written (`uat.json` empty steps, `uat.md` ACs no results)
- [x] Traceability row added to `docs/engineering/state.md` (Story=US-0130 | Sprint=S0130 | Tasks=T-anch+T-001..T-007 | Status=PLANNED | Evidence empty)
- [x] Backlog status OPEN (US-0045 — not mutated); AC checkboxes untouched

## Next scheduled phase

| Field | Value |
|---|---|
| next_scheduled_phase | `/execute` (role=dev per US-0069 / DEC-0051; fresh dev subagent per BUG-0006; first canonical phase of `build+verify` macro per ultra_lean; /plan-verify merged into qa per ultra_lean — qa creates plan-verify.json within build+verify). Orchestrator runs sovereign-critic of sprint-plan first (CROSS_MODEL_REVIEW=1). Do not mandate outer driver. |
| next_scheduled_role | dev |
| next_sprint_macro | build+verify (ultra_lean — plan-verify merged into qa) |
| stop_condition | STOP after sprint-plan completes; hand off via artifacts only. Orchestrator owns critic of sprint-plan then `/execute` in fresh dev subagent per BUG-0006. Do not spawn /execute or /plan-verify from this subagent. |
| artifacts_written | sprints/S0130/ (sprint.md, tasks.md, progress.md, uat.json, uat.md), docs/engineering/state.md (sprint-plan checkpoint append-bottom + traceability row), handoffs/tl_to_dev.md (US-0130 prepend), handoffs/resume_brief.md (sprint-plan PASS prepend -> /execute) |
