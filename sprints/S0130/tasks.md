# Sprint S0130 - Task checklist (US-0130)

Total tasks: 8 (T-anch + T-001..T-007). SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1; no split needed.

**Isolation**: `tl-US0130-sprint-plan-20260826T215200Z-fresh` · `model_id=cursor-grok-4.6-high` · `orchestrator_run_id=auto-20260826-01`

## Task execution order

1. T-anch (NO-OP / verification)
2. T-001 (`select_critic_model` overlay in `scripts/sovereign_critic_lib.py` + template mirror per DQ2/DQ3/DQ7)
3. T-002 (`CATALOG_OPTIONAL_ROLE_KEYS` + `_validate_roles_object` extra-key subtract + validator empty-present-critic + template mirrors per DQ1/DQ6)
4. T-003 (v2 example `critic` keys + ship cursor_only as 9th + manifest/installer lists per DQ4/DQ5; never write `model-catalog.local.json`)
5. T-004 (scratchpad DQ8 comment sites; no live `MODEL_SOVEREIGN-CRITIC=` assignment)
6. T-005 (NEW `tests/us0130_contract_test.py` + template mirror — 10 markers)
7. T-006 (runbook `#### Degraded fallback troubleshooting` pin-precedence note + template mirror per DQ8)
8. T-007 (`SOVEREIGN_CRITIC_PAIRS` add `sovereign_critic_lib.py`; `MODEL_TIER_OVERRIDES_PAIRS` add cursor_only json pair)
9. Integration verification

## Critic NB awareness (execute)

- **T-001** (`a0130ar-challenger-001`): consume `MODEL_SOVEREIGN-CRITIC` via `phase_to_model_key("sovereign-critic")` — hyphen exact. Do not consume underscore alias. Overlay order: pin → optional `roles.critic` when `role_catalog` → opposition UNCHANGED. Do not pass a newly loaded catalog into `_resolve_slug_for_tier`. Same-slug keeps `degraded=True`.
- **T-002** (`a0130ar-architect-002`): do not add `critic` to `CATALOG_ROLE_KEYS`. Optional allowlist subtract only. Empty-present-critic reuses `MODEL_CATALOG_SCHEMA_V2_INVALID` (message names `critic`; no new reason-code family). Missing `critic` is not an error.
- **T-anch / T-005** (`a0130ar-subtractor-003`): T-anch read-only; no `architecture.md` mutation; do not mark US-0130 DONE; 10 markers required (not YAGNI); do not author DEC-0130; do not write `model-catalog.local.json`.

## Task checklist

- [x] **T-anch**: Verify `# US-0130` H1 present in `docs/engineering/architecture.md` at L1815 (added in /architecture per DEC-0076 / BUG-0010; AFTER `# US-0128` L1671 and BEFORE `# US-0091` L1971); verify approach A1 locked + R-0112 DQ1–DQ8 LOCKED; verify compose-do-not-amend 9/9 baseline (US-0104, US-0102, US-0101, US-0112, US-0127/US-0128, US-0129, US-0123, R-0088, US-0045/US-0048/US-0056); verify 10-marker contract-test list locked in architecture; verify `select_critic_model` root cause at `scripts/sovereign_critic_lib.py` L236–267 still maps producer → opposition via `CRITIC_TIER_OPPOSITION` then `_resolve_slug_for_tier("sovereign-critic", …)` and does NOT read `MODEL_SOVEREIGN-CRITIC` or `roles.critic`; verify `CATALOG_ROLE_KEYS` (model_tier_lib.py L85–87) has no `critic`; verify `phase_to_model_key` hyphen path; verify `.cursor/model-catalog.local.example.role-based-balanced_cursor_only.json` exists but lacks `"critic"` and is absent from `installer-owned-paths.manifest` `[install_include_paths]` and installer.ps1/installer.py `FRAMEWORK_EXACT` lists; verify `template/.cursor/model-catalog.local.example.role-based-balanced_cursor_only.json` does NOT yet exist; verify `tests/us0130_contract_test.py` + template mirror do NOT yet exist; verify `SOVEREIGN_CRITIC_PAIRS` currently hygiene-only (no `sovereign_critic_lib.py` pair); verify `MODEL_TIER_OVERRIDES_PAIRS` lacks cursor_only json pair; verify runbook `#### Degraded fallback troubleshooting` (~L2948) has no US-0130 pin-precedence note; verify no live `MODEL_SOVEREIGN-CRITIC=` assignment in committed scratchpad. Record results to `sprints/S0130/t-anch-verification.md`. T-anch is NO-OP / verification only — NO mutation to `docs/engineering/architecture.md` in /execute. (AC-7 baseline; NO-OP / verification only)

- [x] **T-001**: Edit `scripts/sovereign_critic_lib.py` AND `template/scripts/sovereign_critic_lib.py` (byte-identical) per architecture DQ2/DQ3/DQ7 LOCKED. Prepend overlay **inside** `select_critic_model` before L250–252 opposition. Overlay order: (1) Exact pin `pad.get(phase_to_model_key("sovereign-critic"))` → `MODEL_SOVEREIGN-CRITIC` nonempty → use that slug; validate via `validate_direct_slug` when `MODEL_RESOLVE` is `local_catalog`/`role_catalog` and a catalog is loaded (DEC-0087 §4); when `alias_only`, pin is an opaque slug. (2) Else if `MODEL_RESOLVE=role_catalog`: load catalog from `MODEL_CATALOG` (default `.cursor/model-catalog.local.json`); if `roles.critic` present and nonempty → use it; catalog miss on optional `critic` is **not** `MODEL_ROLE_SLUG_UNKNOWN` — fall through. (3) Else existing opposition: `_resolve_slug_for_tier("sovereign-critic", …)` **UNCHANGED**; do not pass a newly loaded catalog into that helper. (4) Existing same-slug comparison → `degraded=True` / `CROSS_MODEL_DEGRADED_MODE` **UNCHANGED**. `SelectCriticResult` shape UNCHANGED. One global critic (no per-lens / per-phase critic overrides). Do **not** consume `MODEL_SOVEREIGN_CRITIC` (underscore). Do **not** register `sovereign-critic` in `PHASE_LOGICAL_ROLE`, `CANONICAL_PHASE_IDS`, or `DEFAULT_PHASE_TIER_MATRIX`. MUST keep active ↔ template byte-identical after edit. Tests: markers 1, 2, 3, 4, 6. (AC-1 consume, AC-3, AC-4, AC-5)

- [x] **T-002**: Edit `scripts/model_tier_lib.py` AND `template/scripts/model_tier_lib.py` (byte-identical) plus `scripts/model_tier_validate.py` AND template mirror per architecture DQ1/DQ6 LOCKED. Introduce `CATALOG_OPTIONAL_ROLE_KEYS = frozenset({"critic"})`. `_validate_roles_object`: extra = `actual_keys - CATALOG_ROLE_KEYS - CATALOG_OPTIONAL_ROLE_KEYS`. Do **not** add `critic` to `CATALOG_ROLE_KEYS`, `LOGICAL_ROLE_TO_CATALOG_KEY`, or `PHASE_LOGICAL_ROLE`. Validator required-role loop stays `for role_name in CATALOG_ROLE_KEYS`. After that loop, if `"critic" in roles`: require nonempty string; empty/whitespace reuses `MODEL_CATALOG_SCHEMA_V2_INVALID` (message names the `critic` key; **no new reason-code family**). Missing `critic` is not an error. Unknown extras still fail-closed. MUST keep active ↔ template byte-identical after edit. Tests: markers 7, 8. (AC-2)

- [x] **T-003**: Examples + installer per architecture DQ4/DQ5 LOCKED (AC-8). Add `"critic": "<your-critic-model-slug>"` to v2 role-based-balanced + highend (active `.cursor/` + `template/`). Edit `.cursor/model-catalog.local.example.role-based-balanced_cursor_only.json` to add `"critic": "composer-2.5-fast"`; **ship as 9th example** — add `template/.cursor/model-catalog.local.example.role-based-balanced_cursor_only.json` copy + `docs/engineering/context/installer-owned-paths.manifest` `[install_include_paths]` row + `installer.ps1` / `installer.py` `FRAMEWORK_EXACT` explicit lists (`installer.sh` glob already matches). v1 examples (`example.json`, `cursor-only.json`, `level-1-easy` … `level-4-super`) **unchanged**. `role-based-budget.json` out of installer compose this slice. OpenCode example out of scope (US-0123). **Never write** `.cursor/model-catalog.local.json`. Tests: markers 9, 10. (AC-8)

- [x] **T-004**: Scratchpad DQ8 comment sites (AC-1 docs + AC-9). Two comment sites, mirrored to `template/.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and active `scratchpad.local.example.md`: (1) Next to `MODEL_<PHASE>` examples after `MODEL_REFRESH-CONTEXT` hyphen precedent: synthetic-phase pin `MODEL_SOVEREIGN-CRITIC=<your-critic-model-slug>` — not a canonical phase; hyphen exact; no underscore alias; vendor slugs in `.cursor/scratchpad.local.md` only. **No live assignment** in committed scratchpad. (2) Next to `CROSS_MODEL_*` keys after `CROSS_MODEL_REWORK_MAX` comments, before enabled assignments: precedence pin > `roles.critic` (when `role_catalog`) > opposition/`dev`; same-slug keeps `CROSS_MODEL_DEGRADED_MODE`; one global critic. MUST keep active ↔ template byte-identical after edit. (AC-1, AC-9)

- [x] **T-005**: Create `tests/us0130_contract_test.py` with 10 markers per architecture Q1 + R-0112 inventory (AC-6 + AC-7). Markers:
  1. `test_us0130_pin_wins_over_catalog_and_opposition` — nonempty `MODEL_SOVEREIGN-CRITIC` wins over catalog `roles.critic` and opposition (AC-1/AC-3/AC-6).
  2. `test_us0130_catalog_critic_hit_when_pin_absent` — pin absent + `MODEL_RESOLVE=role_catalog` + nonempty `roles.critic` → catalog slug used (AC-2/AC-3/AC-6).
  3. `test_us0130_omitted_critic_falls_back_to_opposition` — pin absent + catalog missing `critic` → existing opposition/`dev` fallback (AC-2/AC-3/AC-6).
  4. `test_us0130_same_slug_keeps_degraded_mode` — resolved critic slug equals producer slug → `degraded=True` / `CROSS_MODEL_DEGRADED_MODE` (not hard stop) (AC-4/AC-6).
  5. `test_us0130_compose_us0104_findings_schema_unchanged` — findings JSONL / three lenses / `CROSS_MODEL_*` enable keys / anti-slop unchanged (AC-7/AC-6).
  6. `test_us0130_underscore_alias_not_consumed` — `MODEL_SOVEREIGN_CRITIC` (underscore) is ignored; hyphen pin is the only consumed key (DQ3) (AC-1/AC-3/AC-6).
  7. `test_us0130_extra_critic_allowed_missing_not_error` — extra `critic` allowed; missing `critic` not an error; empty-present reuses `MODEL_CATALOG_SCHEMA_V2_INVALID` (DQ6) (AC-2/AC-6).
  8. `test_us0130_critic_not_in_catalog_role_keys` — `critic` not in `CATALOG_ROLE_KEYS` (DQ1) (AC-2/AC-6).
  9. `test_us0130_cursor_only_example_ships_critic` — cursor_only example has `critic=composer-2.5-fast` and is the 9th installer-shipped example (DQ4/DQ5) (AC-8/AC-6).
  10. `test_us0130_installer_never_writes_local_catalog` — installer/manifest never writes `model-catalog.local.json` (DQ5) (AC-8/AC-6).
  All markers static/fixture-based; no live critic spawn. Mirror to `template/tests/us0130_contract_test.py` byte-identical. (AC-6, AC-7)

- [x] **T-006**: Edit `docs/engineering/runbook.md` AND `template/docs/engineering/runbook.md` (byte-identical) per architecture DQ8 LOCKED. In `#### Degraded fallback troubleshooting` (~L2948) document pin precedence (`MODEL_SOVEREIGN-CRITIC` > `roles.critic` when `role_catalog` > opposition/`dev`) and optional `roles.critic` (do not change same-slug = not hard stop). MUST keep active ↔ template byte-identical after edit. (AC-9)

- [x] **T-007**: Edit `scripts/check_intake_template_parity.py` AND `template/scripts/check_intake_template_parity.py` (byte-identical). Add `("scripts/sovereign_critic_lib.py", "template/scripts/sovereign_critic_lib.py")` to `SOVEREIGN_CRITIC_PAIRS` (hygiene pair retained). Add `(".cursor/model-catalog.local.example.role-based-balanced_cursor_only.json", "template/.cursor/model-catalog.local.example.role-based-balanced_cursor_only.json")` to `MODEL_TIER_OVERRIDES_PAIRS`. `MODEL_TIER_PAIRS` already covers lib/validator/scratchpad — no change required there. `--scope=sovereign-critic` and `--scope=model-tier-overrides` extend automatically via tuple union. MUST keep active ↔ template byte-identical after edit. Tests: markers 9, 10 + `python scripts/check_intake_template_parity.py --scope=sovereign-critic` and `--scope=model-tier-overrides` exit 0. (AC-9)

## Integration verification (post T-007)

- [x] Test gate: `python -m pytest tests/us0130_contract_test.py -v` -> 10/10 PASS
- [x] Parity gate: `check_intake_template_parity.py --scope=sovereign-critic` PASS
- [x] Parity gate: `check_intake_template_parity.py --scope=model-tier-overrides` PASS
- [x] Parity gate: active + template sovereign_critic_lib.py byte-identical
- [x] Parity gate: active + template model_tier_lib.py + model_tier_validate.py byte-identical
- [x] Parity gate: active + template scratchpad.md + scratchpad.local.example.md byte-identical
- [x] Parity gate: active + template runbook.md byte-identical
- [x] Parity gate: active + template check_intake_template_parity.py byte-identical
- [x] Parity gate: active + template us0130_contract_test.py byte-identical
- [x] Compose gate: 9/9 UNCHANGED (US-0104/US-0102/US-0101/US-0112/US-0127/US-0128/US-0129/US-0123/US-0045)
- [x] Compose gate: `pytest tests/us0104_contract_test.py -q` PASS (marker 5)
- [x] No-secrets gate: `api_key`/`apikey`/`sk-`/`auth.json`/`.env` grep zero hits on edited files
- [x] Never-write gate: `.cursor/model-catalog.local.json` not created/mutated

## Files to touch (scope)

### New (create)

- `tests/us0130_contract_test.py`
- `template/tests/us0130_contract_test.py` (byte-identical mirror for parity)
- `template/.cursor/model-catalog.local.example.role-based-balanced_cursor_only.json` (9th example ship)
- `sprints/S0130/t-anch-verification.md`

### Edit (scoped, additive only)

- `scripts/sovereign_critic_lib.py` (overlay inside `select_critic_model` per DQ2/DQ3/DQ7)
- `template/scripts/sovereign_critic_lib.py` (byte-identical mirror)
- `scripts/model_tier_lib.py` (`CATALOG_OPTIONAL_ROLE_KEYS` + extra-key subtract)
- `template/scripts/model_tier_lib.py` (byte-identical mirror)
- `scripts/model_tier_validate.py` (empty-present-critic branch)
- `template/scripts/model_tier_validate.py` (byte-identical mirror)
- `.cursor/model-catalog.local.example.role-based-balanced.json` (add `critic` placeholder)
- `template/.cursor/model-catalog.local.example.role-based-balanced.json` (byte-identical mirror)
- `.cursor/model-catalog.local.example.role-based-highend.json` (add `critic` placeholder)
- `template/.cursor/model-catalog.local.example.role-based-highend.json` (byte-identical mirror)
- `.cursor/model-catalog.local.example.role-based-balanced_cursor_only.json` (add `critic=composer-2.5-fast`)
- `docs/engineering/context/installer-owned-paths.manifest` (add cursor_only row)
- `template/docs/engineering/context/installer-owned-paths.manifest` (if mirrored)
- `installer.ps1` / `installer.py` (`FRAMEWORK_EXACT` add cursor_only)
- `.cursor/scratchpad.md` + `template/.cursor/scratchpad.md` (DQ8 comments)
- `.cursor/scratchpad.local.example.md` + `template/.cursor/scratchpad.local.example.md` (DQ8 comments)
- `docs/engineering/runbook.md` + `template/docs/engineering/runbook.md` (pin-precedence note)
- `scripts/check_intake_template_parity.py` + template mirror (`SOVEREIGN_CRITIC_PAIRS` + `MODEL_TIER_OVERRIDES_PAIRS`)

### Verify read-only (no mutation)

- `docs/engineering/architecture.md # US-0130` (T-anch NO-OP; DQ1..DQ8 locks + 10-marker table are the locked source of truth)
- `docs/product/backlog.md ## US-0130` (read-only Status/ACs — US-0045; sprint-plan notes already written this phase)
- `docs/product/acceptance.md` US-0130 row L158 (read-only — US-0045 derived view)
- `handoffs/intake_evidence/US-0130-intake-20260826.json` (read-only — never mutate prior intake evidence)

### Compose-guard UNCHANGED (DO NOT TOUCH)

| File | Reason |
|---|---|
| `docs/product/backlog.md` Status/ACs | US-0045 canonical status — `/closure` mutates ONLY at execution time |
| `docs/product/acceptance.md` | US-0045 derived view — same |
| `docs/engineering/architecture.md` | Do not rewrite; T-anch is verification only |
| `decisions/` / `DEC-0130` | No new DEC (per R-0112; A6 rejected) |
| `.cursor/model-catalog.local.json` | never write (DQ5 / AC-8) |
| US-0104 surfaces (findings JSONL / lenses / `CROSS_MODEL_*` keys / anti-slop) | compose read-only — marker 5 |
| US-0102 surfaces (`CATALOG_ROLE_KEYS` required-set / 5-step chain / `PHASE_LOGICAL_ROLE`) | compose read-only |
| US-0101 surfaces (`DEFAULT_PHASE_TIER_MATRIX` / v1 catalogs) | compose read-only |
| US-0127 / US-0128 DONE rows | do not reopen |
| US-0129 OPEN row | do not mutate |
| v1 example catalogs | do not add `roles.critic` |

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

**Surjectivity check**: 9/9 ACs covered (AC-1..AC-9 each have at least 1 task). No `PLAN_AC_COVERAGE_GAP`.
