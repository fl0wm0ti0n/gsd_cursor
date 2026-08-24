# Sprint S0123 - Task checklist (US-0123)

Total tasks: 10 (T-anch + T-001..T-009). SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1; no split needed.

## Task execution order

1. T-anch (NO-OP / verification)
2. T-001 (NEW example catalog `template/.opencode/model-catalog.local.example.json`)
3. T-002 (NEW materializer `scripts/opencode_model_catalog_apply.py`)
4. T-003 (Installer hook — triple-installer parity; after T-002)
5. T-004 (Validator extension `scripts/model_tier_validate.py --scope opencode-catalog`; after T-001) - parallel with T-006, T-009
6. T-006 (Gitignore verification; after T-001) - parallel with T-004, T-009
7. T-009 (Manifest rows; after T-001) - parallel with T-004, T-006
8. T-008 (README + `--scope=opencode-adapter` parity extension; after T-001 + T-009)
9. T-007 (Runbook `## OpenCode model slug routing (US-0123)` h2 one-liner; after T-001)
10. T-005 (NEW `tests/us0123_contract_test.py` — 8 markers; tests last, assert all outputs)
11. Integration verification

## Task checklist

- [x] **T-anch**: Verify `# US-0123` H1 anchor present in `docs/engineering/architecture.md` (added in /architecture phase per DEC-0076 / BUG-0010; AFTER `# US-0122` and BEFORE `# US-0089` per DEC-0073 §11); verify DEC-0123 authored Accepted at `decisions/DEC-0123.md` (§1 SOT, §2 template agents omit model, §3 single fail-closed code, §4 catalog path, §5 per-role schema, §6 example placeholders, §7 additive integration + materializer + installer hook contract, §8 always api mode, §9 validator extension, §10 runbook stub, §11 contract tests, §12 non-goals); verify compose guards 6/6 UNCHANGED baseline (US-0101/DEC-0086, US-0102/DEC-0087, US-0003, US-0122/DEC-0122, US-0121, US-0080); verify 8-marker contract-test list locked in architecture AC-8 table; verify materializer + installer hook contract locked in DEC-0123 §7; verify `template/.opencode/model-catalog.local.example.json` does NOT yet exist; verify `scripts/opencode_model_catalog_apply.py` does NOT yet exist; verify `tests/us0123_contract_test.py` does NOT yet exist; verify `scripts/model_tier_validate.py` does NOT yet have `--scope opencode-catalog`; verify `.opencode/.gitignore` (US-0121 Q10) covers `*.local.json` glob; verify `[opencode_install_include_paths]` section exists in active + template manifest (US-0121) but does NOT yet list `template/.opencode/model-catalog.local.example.json` or `scripts/opencode_model_catalog_apply.py` source rows. Record results to `sprints/S0123/t-anch-verification.md`. **Critic NB `ik_us0123_sprint_tanch_ceremony_overlap`**: T-anch is NO-OP / verification only — NO mutation to `docs/engineering/architecture.md` or `decisions/DEC-0123.md` in /execute; T-anch records baseline observations only (mirrors US-0122 T-anch ceremony). (AC-6, AC-9 baseline; NO-OP / verification only)

- [x] **T-001**: Create `template/.opencode/model-catalog.local.example.json` per architecture DQ6 LOCKED + DEC-0123 §6. Schema: `{schema_version, providers, roles}` with 8 role keys (`po`, `tech-lead`, `dev`, `qa`, `release`, `curator`, `security`, `auto`). Provider block covers DeepSeek (`@ai-sdk/deepseek`), Moonshot (`@ai-sdk/moonshot`), Z.AI (`@ai-sdk/zai`), Anthropic (`@ai-sdk/anthropic`), OpenAI (`@ai-sdk/openai`), DashScope/Qwen (`@ai-sdk/openai-compatible` + `options.baseURL`). Role values are `<your-deepseek-slug>`, `<your-kimi-slug>`, `<your-glm-slug>`, `<your-claude-slug>`, `<your-gpt-slug>` placeholders — NO real model-id slugs in `template/`. ≥2 roles have different providers (AC-7 per-role divergence — e.g. `po: anthrop/...`, `dev: deepseek/...`, `qa: moonshot/...`). Tests: marker 3 (`test_us0123_example_catalog_placeholders_only`) asserts placeholder form; marker 4 (`test_us0123_example_catalog_per_role_divergence`) asserts ≥2 different providers. (AC-2, AC-7, AC-9)

- [x] **T-002**: Create `scripts/opencode_model_catalog_apply.py` per architecture DQ7 LOCKED + DEC-0123 §7. Input: `.opencode/model-catalog.local.json` (operator-local, gitignored) + installed `.opencode/agents/<role>.md` files (written by installer from `template/.opencode/agents/*.md`). Behavior: (a) catalog **absent** → no-op, exit 0, installed agents keep `model:` omitted (no fail-closed); (b) catalog **present** → load + validate schema → for each of 8 roles: if slug is non-empty `provider/slug` and provider declared → inject `model: <provider/slug>` into installed agent's YAML frontmatter (insert key if absent; overwrite if present); if slug empty/unknown or provider undeclared → emit `OPENCODE_MODEL_SLUG_UNKNOWN` + exit non-zero (fail-closed); if catalog JSON malformed → emit `MODEL_CATALOG_INVALID` (scope-tagged `opencode-catalog`) + exit non-zero. **Never** writes to `template/`. **Never** reads or writes `.cursor/model-catalog.local.json`. **Never** reads auth credentials (auth lives in `/connect` / `~/.local/share/opencode/auth.json`). **Critic NB `ik_us0123_placeholder_slug_copy_paste_boundary` closed**: materializer MUST treat `<your-*-slug>` angle-bracket placeholder strings as **unknown** slugs (emit `OPENCODE_MODEL_SLUG_UNKNOWN`, fail-closed) — operators who copy-paste the example catalog without filling in real slugs must NOT silently get placeholder `model:` values injected into installed agents. Placeholder detection: slug matches `^<.*>$` or contains `<your-` substring → unknown. Tests: marker 5 (`test_us0123_fail_closed_unknown_slug`) asserts fail-closed including placeholder case; marker 6 (`test_us0123_materializer_no_op_when_catalog_absent`) asserts no-op when absent. (AC-1, AC-4, AC-5)

- [x] **T-003**: Installer hook — `installer.py` / `installer.ps1` / `installer.sh` invoke materializer when `--host opencode|both` AND `.opencode/model-catalog.local.json` exists at install target. If catalog absent → skip materializer (no-op; no fail-closed). If materializer fails (non-zero exit) → surface reason code + exit non-zero. Triple-installer parity: all three use the same trigger condition and the same error surface. The installer does NOT generate the catalog for the operator — operators create `.opencode/model-catalog.local.json` themselves (or copy from `template/.opencode/model-catalog.local.example.json` and fill in real slugs). **Critic NB `ik_us0123_t002_t003_installer_hook_contract` closed (from research)**: trigger = `--host opencode|both` AND catalog present; absent = skip; fail = surface reason code + exit non-zero. (AC-1, AC-5)

- [x] **T-004**: Extend `scripts/model_tier_validate.py` with `--scope opencode-catalog` per architecture DQ9 LOCKED + DEC-0123 §9 (extend-not-duplicate; new script only if too coupled). Extension adds: (a) `check_template_opencode_agents` — grep `template/.opencode/agents/**/*.md` for `model:` field (must be absent) + forbidden vendor slug patterns (`deepseek|moonshot|kimi|glm|claude|gpt|sonnet|opus|haiku|o1|o3|sk-`); D3 grep scope **excludes** `*.example.json` / `*.local.json`; also grep `template/.opencode/opencode.json{,c}` if present (must not exist in template); (b) `validate_opencode_catalog` — load `.opencode/model-catalog.local.json` (if present) → validate schema (`schema_version`, `providers`, `roles` with 8 role keys) → unknown/empty slug → `OPENCODE_MODEL_SLUG_UNKNOWN` → malformed JSON → `MODEL_CATALOG_INVALID` (scope-tagged `opencode-catalog`); (c) `check_opencode_example_catalog` — load `template/.opencode/model-catalog.local.example.json` → assert placeholder values only (no real model-id slugs) → assert ≥2 roles have different providers (AC-7); (d) reuse existing `check_forbidden_slugs_in_file` helper (extend forbidden-slug list to cover OpenCode agent files + example catalog). **Critic NB `ik_us0123_validator_extension_coupling_fallback` closed**: document in T-004 task note **when to extend `model_tier_validate.py` vs new script** — default = extend in place (DQ9 lock); fall back to new `scripts/opencode_model_catalog_validate.py` ONLY if schema divergence forces a separate validator class (e.g. OpenCode catalog schema cannot share the loader/validation base class with Cursor catalog). Trigger for fallback: `validate_opencode_catalog` cannot reuse >50% of existing `validate_cursor_catalog` helpers, OR scope-tag plumbing requires touching >3 unrelated `--scope` modes. If fallback triggers, raise DEC-0124-class follow-up; do NOT silently split. (AC-3, AC-8)

- [x] **T-005**: Create `tests/us0123_contract_test.py` with 8 markers per architecture AC-8 table:
  1. `test_us0123_template_agents_omit_model` — grep `^model:` in `template/.opencode/agents/*.md` → zero matches (AC-1, AC-3).
  2. `test_us0123_no_vendor_slugs_in_template` — D3 grep scoped to `template/.opencode/agents/**/*.md` + `template/.opencode/opencode.json{,c}` if present, **excluding** `*.example.json` / `*.local.json`; forbidden patterns `deepseek|moonshot|kimi|glm|claude|gpt|sonnet|opus|haiku|o1|o3|sk-` → zero hits (AC-3).
  3. `test_us0123_example_catalog_placeholders_only` — `template/.opencode/model-catalog.local.example.json` exists; role values match `<your-*-slug>` placeholder form; no real model-id slugs (AC-2, AC-3).
  4. `test_us0123_example_catalog_per_role_divergence` — ≥2 roles have different providers in the example catalog (AC-7, AC-9).
  5. `test_us0123_fail_closed_unknown_slug` — materializer with synthetic catalog having empty/unknown/`<your-*-slug>` placeholder slug → emits `OPENCODE_MODEL_SLUG_UNKNOWN`, exit non-zero (AC-4).
  6. `test_us0123_materializer_no_op_when_catalog_absent` — materializer with no catalog → no-op, exit 0, installed agents keep `model:` omitted (AC-1, AC-4).
  7. `test_us0123_auth_store_never_in_template_or_git` — grep for `auth.json`/`api_key`/`apikey`/`sk-` in `template/.opencode/**` → zero hits; `.opencode/.gitignore` covers `*.local.json`; auth lives in `/connect` (AC-5).
  8. `test_us0123_compose_cursor_unchanged` — `.cursor/model-catalog.local.json` schema unchanged; `MODEL_TIER_<PHASE>` / `MODEL_<PHASE>` / `MODEL_PROVIDER_MODE` / `MODEL_RESOLVE` keys remain Cursor-side; `TOKEN_PROFILE` orthogonal — slug routing ≠ token-cost profile (AC-6, AC-8).
  Mirror to `template/tests/us0123_contract_test.py` byte-identical for parity pairing. (AC-8)

- [x] **T-006**: Gitignore verification — `.opencode/.gitignore` (US-0121 Q10) covers `*.local.json` glob → `model-catalog.local.json` is covered. If the glob is narrower than `*.local.json` (e.g. only matches `secrets.local.json`), add `model-catalog.local.json` explicitly. Do not duplicate gitignore entries. T-006 asserts coverage via grep on `.opencode/.gitignore`. (AC-5)

- [x] **T-007**: Runbook stub — Add `## OpenCode model slug routing (US-0123)` h2 to `docs/engineering/runbook.md` as a **one-liner** per DEC-0123 §10 / DQ10 LOCKED: "QA/dev should default to a tool-reliable slug (a model with documented tool-calling support); Chinese API quality is operator model choice. The kit does not endorse a single vendor." US-0126 inherits and expands into a full runbook section. T-007 does NOT author a full runbook section (YAGNI — US-0126 owns it). (AC-10)

- [x] **T-008**: README + parity extension — Extend `scripts/check_intake_template_parity.py` `--scope=opencode-adapter` `OPENCODE_ADAPTER_PAIRS` to cover the example catalog + materializer + validator surface (byte-identical active ↔ template pairs where applicable; materializer is kit-only, not paired). Update `its_magic/README.md` to cross-link the OpenCode model slug routing capability + pointer to DEC-0123. Mirror parity script to `template/scripts/check_intake_template_parity.py` byte-identical. (AC-8)

- [x] **T-009**: Installer manifest rows — Add `template/.opencode/model-catalog.local.example.json` + `scripts/opencode_model_catalog_apply.py` source rows under `[opencode_install_include_paths]` in `docs/engineering/context/installer-owned-paths.manifest` AND `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical). Existing rows UNCHANGED — additive rows only. Triple-installer (PS/Bash/Python) reads opencode sections only when `--host` includes opencode (US-0121 compose; `host_gates_cursor_row` predicate). (AC-1)

## Integration verification (post T-009 + T-005)

- [x] Test gate: `python -m pytest tests/us0123_contract_test.py -v` → 8/8 PASS
- [x] Parity gate: `check_intake_template_parity.py --scope=opencode-adapter` PASS
- [x] Parity gate: active + template manifest byte-identical
- [x] Compose gate: 6/6 UNCHANGED
- [x] No-secrets gate: vendor slug grep zero hits on template (excluding `*.example.json` / `*.local.json`)
- [x] Validator gate: `python scripts/model_tier_validate.py --scope opencode-catalog` PASS
- [x] Materializer gate: no-op when catalog absent; fail-closed when present + unknown slug

## Files to touch (scope)

### New (create)

- `template/.opencode/model-catalog.local.example.json`
- `scripts/opencode_model_catalog_apply.py`
- `tests/us0123_contract_test.py`
- `template/tests/us0123_contract_test.py` (byte-identical mirror for parity)
- `sprints/S0123/t-anch-verification.md`

### Edit (scoped, additive only)

- `scripts/model_tier_validate.py` (add `--scope opencode-catalog` mode + `check_template_opencode_agents` / `validate_opencode_catalog` / `check_opencode_example_catalog`)
- `scripts/check_intake_template_parity.py` (extend `OPENCODE_ADAPTER_PAIRS` for example catalog + materializer + validator surface)
- `template/scripts/check_intake_template_parity.py` (byte-identical mirror)
- `docs/engineering/context/installer-owned-paths.manifest` (add `template/.opencode/model-catalog.local.example.json` + `scripts/opencode_model_catalog_apply.py` source rows under `[opencode_install_include_paths]`)
- `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical)
- `installer.py` (add materializer hook on `--host opencode|both` AND catalog present)
- `installer.ps1` (add materializer hook on `-InstallHost opencode|both` AND catalog present)
- `installer.sh` (add materializer hook on `--host opencode|both` AND catalog present)
- `docs/engineering/runbook.md` (append `## OpenCode model slug routing (US-0123)` h2 one-liner)
- `its_magic/README.md` (cross-link OpenCode model slug routing capability + DEC-0123 pointer)

### Verify read-only (no mutation)

- `docs/engineering/architecture.md # US-0123` (T-anch NO-OP)
- `decisions/DEC-0123.md` (T-anch NO-OP)
- `template/.opencode/agents/*.md` (US-0122 — `model:` stays omitted; materializer writes to installed agents only, not template)
- `.opencode/.gitignore` (T-006 verifies `*.local.json` glob coverage; add explicit entry only if glob is narrower)

### Compose-guard UNCHANGED (DO NOT TOUCH)

| File | Reason |
|---|---|
| `docs/product/backlog.md` | US-0045 canonical status — `/closure` mutates ONLY at execution time |
| `docs/product/acceptance.md` | US-0045 derived view — same |
| Compose-guard story surfaces (US-0101/DEC-0086, US-0102/DEC-0087, US-0003, US-0122/DEC-0122, US-0121, US-0080) | 6/6 UNCHANGED — US-0123 adds additive OpenCode catalog path only |

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

**Surjectivity check**: 10/10 ACs covered (AC-1..AC-10 each have at least 1 task). No `PLAN_AC_COVERAGE_GAP`.
