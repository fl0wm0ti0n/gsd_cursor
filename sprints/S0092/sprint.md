# Sprint S0092

## Metadata

- **sprint_id**: S0092
- **story_refs**: US-0102
- **goal**: Ship **direct per-phase model slug override** and **role-based catalog presets** — **`MODEL_<PHASE>`** scratchpad keys, **`MODEL_RESOLVE=role_catalog`** opt-in, unified 5-step precedence in **`model_tier_lib.py`**, catalog schema **v2** optional **`roles`**, three new fail-closed reason codes, eight **`test_us0102_*`** contract markers, **`MODEL_TIER_OVERRIDES_PAIRS`** parity manifest, harness **§26AA**, and runbook operator recipes — per **DEC-0087** (composes **DEC-0086** / **US-0101** — do not amend).
- **status**: planned
- **created_at**: 2026-06-25T19:30:00Z
- **orchestrator_run_id**: auto-20260615-02
- **fresh_context_marker**: tl-S0092-US0102-sprint-plan-20260625T193000Z-fresh

## Scope

- **US-0102**: Direct per-phase model slug override and role-based catalog presets (US-0101 extension)
- **Architecture**: `docs/engineering/architecture.md` `# US-0102`
- **Binding decision**: `decisions/DEC-0087.md` (Accepted 2026-06-25)

## Non-goals (hard, from DEC-0087 / architecture `# US-0102`)

- No amendment of **US-0101** / **DEC-0086** tier baseline — compose only.
- No migration from tier-only to direct override — backward compatible.
- No volatile vendor slugs in **`template/`** files — placeholders only.
- No replacement of tiers with role presets — **`MODEL_RESOLVE=role_catalog`** is opt-in.
- No **`TOKEN_PROFILE`** behavior changes — orthogonal axis per **DEC-0062**.
- No weakening of **US-0023** / **US-0048** spawn isolation gates.
- **Status authority (US-0045)**: US-0102 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0087**; architecture `# US-0102`; **DEC-0086** (US-0101 tier layer)
- **Governance stack**: **DEC-0051** (phase→role matrix), **US-0003** (template agent aliases), **US-0080** / **DEC-0062** (TOKEN_PROFILE orthogonality), **US-0092** / **DEC-0078** (programmatic `model` documented only), **US-0017** (template parity), **US-0045** (status authority), **US-0048** / **DEC-0029** (isolation), **US-0056** / **DEC-0038** (strict proof), **DEC-0080** / **DEC-0081** (native chain compose)

## Acceptance criteria coverage (AC-1..AC-10 → T-xxx; surjective, 11 tasks / 10 ACs)

| AC | Description (summary) | Task(s) | Architecture anchor |
|----|-----------------------|---------|---------------------|
| AC-1 | **`MODEL_<PHASE>`** direct override scratchpad keys + precedence | T-001 | § Scratchpad keys; § Precedence chain |
| AC-2 | 5-step precedence resolution in **`model_tier_lib.py`** | T-005 | § Precedence chain; § Direct slug validation |
| AC-3 | Catalog schema **v2** optional **`roles`** + examples | T-003, T-006 | § Catalog schema v2 |
| AC-4 | Role catalog resolver when **`MODEL_RESOLVE=role_catalog`** | T-005 | § Role catalog resolver |
| AC-5 | **`/ask`** phase **`MODEL_ASK`** reinforcement | T-001 | § `/ask` phase |
| AC-6 | Tier-only backward compatibility unchanged | T-005 | § Backward compatibility |
| AC-7 | Template stability — no vendor slugs in **`template/`** | T-003, T-004 | § Template policy |
| AC-8 | Validator extensions + three new reason codes | T-006, T-007 | § Reason codes |
| AC-9 | Eight **`test_us0102_*`** + parity + harness | T-009, T-010, T-011 | § Contract tests + parity |
| AC-10 | Documentation + runbook + architecture anchor | T-002, T-008 | § Runbook; **DEC-0087** + `# US-0102` (architecture pre-satisfied) |

**Multi-AC tasks** (justified by architecture `# US-0102` § Atomic task seeds): **T-001** (AC-1+AC-5), **T-003** (AC-3+AC-7), **T-005** (AC-2+AC-4+AC-6), **T-006** (AC-3+AC-8), **T-009/T-010/T-011** (AC-9 split contract vs parity vs harness). Every AC has ≥1 task or architecture-phase attestation; no `PLAN_AC_COVERAGE_GAP`. **AC-10** architecture section pre-satisfied at **`/architecture`** — dev tasks **T-002**, **T-008** cover scratchpad/runbook docs.

## Task count

- **Total**: 11
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (11 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-10 coverage; **strict 1:1 task-to-seed** (11 architecture seeds → T-001..T-011); **not** strict AC bijection (multi-AC tasks above)

## Governance

- **DEC-0087** (binding) — each task cites governing architecture §(s) and DEC §(s).
- **DEC-0086** compose — tier layer unchanged; overlay steps 1 and 3 only.
- **US-0045** canonical status authority (US-0102 stays OPEN through this sprint).

## Edit surfaces and parity plan

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `.cursor/scratchpad.md` | `template/.cursor/scratchpad.md` | T-001, T-002 | Positive |
| 2 | `.cursor/scratchpad.local.example.md` | `template/.cursor/scratchpad.local.example.md` | T-001 | Positive |
| 3 | `.cursor/model-catalog.local.example.role-based-balanced.json` | `template/.cursor/model-catalog.local.example.role-based-balanced.json` | T-003 | Positive |
| 4 | `.cursor/model-catalog.local.example.role-based-highend.json` | `template/.cursor/model-catalog.local.example.role-based-highend.json` | T-003 | Positive |
| 5 | `template/.cursor/model-catalog.local.example.json` | (self) | T-004 | Positive |
| 6 | `scripts/model_tier_lib.py` | `template/scripts/model_tier_lib.py` | T-005, T-006 | Positive |
| 7 | `scripts/model_tier_validate.py` | `template/scripts/model_tier_validate.py` | T-007 | Positive |
| 8 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-008 | Positive |
| 9 | `tests/auto_command_contract_test.py` | (active-only) | T-009 | N/A |
| 10 | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` | T-010 | Positive |
| 11 | `tests/run-tests.ps1` / `tests/run-tests.sh` | (active-only) | T-011 | Harness **§26AA** |

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** hardcode vendor slugs in **`template/`** files.
- Do **not** amend **DEC-0086** / **US-0101** tier locks.
- Do **not** require migration from tier-only configurations.
- Do **not** weaken spawn isolation evidence gates.

## Post-edit gate sequence (architecture § Contract tests)

1. `pytest -k us0102 tests/auto_command_contract_test.py` → all eight subtests green
2. `python scripts/check_intake_template_parity.py --scope=model-tier-overrides` → PASS (**`MODEL_TIER_OVERRIDES_PAIRS`**)

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Tranche A — scratchpad keys + docs (T-001..T-002)

- **`MODEL_<PHASE>`** keys documented (placeholder comments; include **`MODEL_ASK`**)
- **`MODEL_RESOLVE=role_catalog`** enum extension + precedence comment block

### Tranche B — catalog v2 examples + template stability (T-003..T-004)

- Role-based catalog example JSON files (placeholder slugs only)
- Template scratchpad tier-only examples; no vendor slugs in template catalog files

### Tranche C — resolver + validator lib (T-005..T-007)

- Unified **`resolve_model_for_phase()`** 5-step precedence; v1/v2 catalog load; phase→role constants
- Catalog v2 validation rules; **`MODEL_CATALOG_SCHEMA_V2_INVALID`**
- **`model_tier_validate.py`** direct slug keys + three new reason codes

### Tranche D — runbook (T-008)

- Direct override precedence, role catalog operator recipe, **`ai_modell_auslegung_cursor_highend.md`** reference (non-normative)

### Tranche E — contract tests + parity + harness (T-009..T-011)

- Eight **`test_us0102_*`** contract subtests; **`MODEL_TIER_OVERRIDES_PAIRS`** parity; harness **§26AA**

## Risks and mitigations (architecture § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Precedence confusion (override vs tier vs role) | T-005 + **`test_us0102_precedence_chain`** |
| R2 | Vendor slugs committed to template | T-004 + **`test_us0102_no_vendor_slugs_in_template`** |
| R3 | v1 catalog break on v2 validator | T-006 + **`test_us0102_tier_only_backward_compat`** |
| R4 | Role mapping drift vs **DEC-0051** | T-005 shared constants + **`test_us0102_role_catalog_resolver`** |
| R5 | Isolation gates weakened | No resolver changes to spawn paths; model selection orthogonal |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 10 acceptance criteria covered surjectively (AC-10 attested at plan-verify from architecture phase + T-002/T-008 docs).
- `sprints/S0092/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_surjective=true`, `task_count=11`, `within_limit=true`.
- `pytest -k us0102` green; parity **`--scope=model-tier-overrides`** PASS.
- `docs/product/backlog.md` **`## US-0102`** retains **OPEN** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0092`** / **US-0102** — verify AC-1..AC-10 ↔ T-001..T-011 surjective coverage, task-seed bijection (11 seeds → 11 tasks), task-count bound, governance alignment. Target: `sprints/S0092/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
