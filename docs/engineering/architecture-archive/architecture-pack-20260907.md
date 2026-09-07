# Architecture archive pack (2026-09-07)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3000, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 19
- First archived heading: `# US-0123 — Per-role OpenCode model slug routing (multi-provider)`
- Last archived heading: `# US-0123 — Per-role OpenCode model slug routing (multi-provider)`
- Verification tuple (mandatory):
  - archived_body_lines=268
  - preamble_lines=1
  - retained_body_lines=2758

---

# US-0123 — Per-role OpenCode model slug routing (multi-provider)

## Overview

**US-0123** is the third slice of the six-story OpenCode adapter epic (US-0121..US-0126). US-0121 shipped the empty-but-valid `template/.opencode/` pack + the `--host` installer switch. US-0122 populated the pack with eight markdown role agents and locked the Layer-1 permission matrix (with `model:` omitted from every template agent per AC-7). US-0123 owns the **per-role `provider/slug` resolution chain** for the OpenCode host: each of the eight roles can resolve to a real `provider/model-id` slug (DeepSeek, Moonshot, Z.AI/GLM, Anthropic, OpenAI, OpenAI-compatible DashScope/Qwen, …) without leaking vendor IDs into `template/`, without the kit proxying provider traffic, and without amending Cursor's US-0101/US-0102 runtime.

This is an **additive contract + materializer** change: one example catalog file (`template/.opencode/model-catalog.local.example.json`), one materializer script (`scripts/opencode_model_catalog_apply.py`), one installer hook on `--host opencode|both` (triple-installer parity), one validator extension (`scripts/model_tier_validate.py --scope opencode-catalog`), one contract test file (`tests/us0123_contract_test.py`), one runbook h2 one-liner, and the companion DEC-0123. Template agent files (`template/.opencode/agents/*.md`) are NOT edited by US-0123 — the materializer injects `model:` into **installed** agent files only, when a local catalog is present.

**Research anchor**: **R-0109** US-0123 deepened findings (DQ1..DQ10 LOCKED for `/architecture`; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 locks PRESERVED, not wiped; 7 risks R1..R7 ACCEPTED; approach A1 locked; compose guards 6/6 verified; 3 spec critic NBs closed; 2 research critic NBs closed here: `ik_us0123_dq7_catalog_optional_vs_failclosed` and `ik_us0123_t002_t003_installer_hook_contract`). **Companion DEC**: **DEC-0123** (authored Accepted in THIS phase — captures the locked SOT + schema + fail-closed code + materializer contract + validator extension so US-0124..US-0126 inherit without re-deriving).

**Fresh context marker**: `tl-US0123-architecture-20260824T162000Z-fresh`
**Orchestrator run id**: `auto-20260824-01`
**Timestamp**: 2026-08-24T16:20:00Z (UTC)
**Verdict**: PASS
**Next**: `/sprint-plan`

## Approach locked (A1 — from R-0109 DQ1..DQ10)

**Approach A1** (locked): Single source of truth = local-only catalog `.opencode/model-catalog.local.json` (gitignored, operator-filled) + example `template/.opencode/model-catalog.local.example.json` (committed, placeholders only). Template agents omit `model:` (inherits US-0122 AC-7). The materializer `scripts/opencode_model_catalog_apply.py` reads the catalog (if present) and injects `model: <provider/slug>` into **installed** `.opencode/agents/<role>.md` files only — never into `template/`. The installer invokes the materializer when `--host opencode|both` AND a local catalog is present (triple-installer parity). When the catalog is **absent**, the materializer is a no-op — **no fail-closed** (catalog is optional; absent catalog = OpenCode uses its default model). When the catalog is **present** but a role's slug is unknown/empty, the materializer emits `OPENCODE_MODEL_SLUG_UNKNOWN` and fails closed (DQ3 LOCKED — single namespaced code; malformed JSON reuses `MODEL_CATALOG_INVALID` scope-tagged `opencode-catalog`). The catalog schema is **per-role** (8 role keys); US-0069 / DEC-0051 phase→role matrix bridges phase→role on the orchestrator side (unchanged). OpenCode host is **always `api` mode** (BYOK via `/connect`); the kit does NOT proxy traffic. Auth keys never live in catalog, template, or git (AC-5). Cursor `MODEL_PROVIDER_MODE` / `MODEL_RESOLVE` / `MODEL_TIER_<PHASE>` / `MODEL_<PHASE>` keys remain Cursor-side only (AC-6 compose, not amend). The validator is extended in place: `scripts/model_tier_validate.py --scope opencode-catalog`. A stub runbook h2 ships one line; US-0126 owns the full text (DQ10).

| Option | Summary | Verdict |
|--------|---------|---------|
| **A1** | **Local-only `.opencode/model-catalog.local.json` SOT + example catalog + materializer injects into installed agents only + single `OPENCODE_MODEL_SLUG_UNKNOWN` fail-closed + per-role schema + extend `model_tier_validate.py --scope opencode-catalog` + stub runbook h2** | **Preferred** — additive only; composes with US-0101/US-0102/US-0003/US-0122/US-0121/US-0080; AC-3 provable via scoped D3 grep; AC-4 provable via fail-closed test; critic NBs closed. |
| A2 (rejected) | Scratchpad `MODEL_*` keys as OpenCode SOT + bridge materializer | **Rejected** — couples two hosts through one file; scratchpad keys are per-phase (Cursor), not per-role (OpenCode); schema drift risk (DQ1). |
| A3 (rejected) | `model:` placeholder in `template/.opencode/agents/*.md` frontmatter | **Rejected** — violates US-0102 volatile-ID rule + US-0122 AC-7; false-fails the D3 grep; worse template hygiene (DQ2). |
| A4 (rejected) | Shared `.cursor/model-catalog.local.json` across hosts | **Rejected** — union schema couples two hosts; Cursor schema is tier/role, OpenCode schema is provider/slug per role (DQ4). |
| A5 (rejected) | New `scripts/opencode_model_catalog_validate.py` validator | **Rejected as default** — DQ9 locks "extend, don't duplicate"; only if extension proves too coupled does architecture fall back to a new script. Default: extend `model_tier_validate.py`. |
| A6 (rejected) | Kit-operated proxy for Chinese APIs | **Rejected** — AC-2/AC-9 require Chinese APIs as **capability**, not kit proxy; OpenCode host = always `api` (BYOK via `/connect`) (DQ8). |

## Components

### Source of truth (DQ1 LOCKED — AC-1)

```
.opencode/model-catalog.local.json                  # gitignored, operator-filled (real slugs)
template/.opencode/model-catalog.local.example.json  # committed, placeholders only
```

- **Forbidden surfaces** for real OpenCode slugs:
  - `template/.opencode/agents/*.md` `model:` frontmatter (must be omitted in template — DQ2)
  - `template/.opencode/opencode.json{,c}` (must not exist in template — R-0109 Q6 US-0121 lock preserved)
  - `.cursor/model-catalog.local.json` (Cursor-side, separate host + schema — DQ4)
  - `.cursor/scratchpad.local.md` `MODEL_*` keys (Cursor-side compose only — DQ1)
- The kit does NOT share one catalog across hosts. Different hosts, different schemas, different files.

### Catalog schema (DQ5 LOCKED — AC-7, per-role, 8 role keys)

```json
{
  "schema_version": 2,
  "providers": {
    "deepseek": { "npm": "@ai-sdk/deepseek" },
    "moonshot": { "npm": "@ai-sdk/moonshot" },
    "zai": { "npm": "@ai-sdk/zai" },
    "anthropic": { "npm": "@ai-sdk/anthropic" },
    "openai": { "npm": "@ai-sdk/openai" },
    "dashscope": {
      "npm": "@ai-sdk/openai-compatible",
      "options": { "baseURL": "https://dashscope.aliyuncs.com/compatible-mode/v1" }
    }
  },
  "roles": {
    "po": "anthropic/<your-claude-slug>",
    "tech-lead": "zai/<your-glm-slug>",
    "dev": "deepseek/<your-deepseek-slug>",
    "qa": "moonshot/<your-kimi-slug>",
    "release": "openai/<your-gpt-slug>",
    "curator": "anthropic/<your-claude-slug>",
    "security": "anthropic/<your-claude-slug>",
    "auto": "zai/<your-glm-slug>"
  }
}
```

- 8 role keys: `po`, `tech-lead`, `dev`, `qa`, `release`, `curator`, `security`, `auto` (matches US-0003 role set + `auto` per US-0122).
- Each value is a `provider/slug` string. Provider names are documented OpenCode built-ins (DeepSeek, Moonshot, Z.AI, Anthropic, OpenAI) or custom OpenAI-compatible (`dashscope`/Qwen via `@ai-sdk/openai-compatible` + `options.baseURL`).
- US-0069 / DEC-0051 phase→role matrix bridges `phase_id → role` on the orchestrator (unchanged); the catalog bridges `role → provider/slug` on OpenCode (new). No per-phase keys on OpenCode.
- Per-role divergence (AC-7) is expressed by assigning different `provider/slug` values to different roles. Tests assert ≥2 roles have different providers in the example catalog.

### Example catalog placeholders (DQ6 LOCKED — AC-2, AC-3, AC-9)

- Single example surface = `template/.opencode/model-catalog.local.example.json`.
- Provider names allowed (DeepSeek, Moonshot, Z.AI, Anthropic, OpenAI, DashScope) — informational, not vendor IDs.
- Real model-id slugs **forbidden** in `template/` — operators fill `<your-deepseek-slug>`, `<your-kimi-slug>`, `<your-glm-slug>`, `<your-claude-slug>`, `<your-gpt-slug>` placeholders in the local `.opencode/model-catalog.local.json`.
- D3 grep scope = `template/.opencode/agents/**/*.md` + `template/.opencode/opencode.json{,c}` (if present), **excluding** `*.example.json` / `*.local.json`. Provider names in the example catalog do NOT false-fail the D3 grep.
- Example covers ≥ DeepSeek, Moonshot, Z.AI, and one Western provider (Anthropic) — satisfies AC-2. No vendor IDs in `template/` — satisfies AC-3. Per-role assignment demonstrates AC-9 (Chinese APIs as capability, no kit proxy).

### Materializer contract (DQ7 LOCKED — AC-1, AC-5, AC-6 — critic NB `ik_us0123_t002_t003_installer_hook_contract` closed)

`scripts/opencode_model_catalog_apply.py`:

- **Input**: `.opencode/model-catalog.local.json` (operator-local, gitignored) + installed `.opencode/agents/<role>.md` files (written by the installer from `template/.opencode/agents/*.md`).
- **Behavior**:
  - If catalog **absent**: no-op. Installed agents keep `model:` omitted. OpenCode uses its default model. **No fail-closed.** (critic NB `ik_us0123_dq7_catalog_optional_vs_failclosed` closed — absent catalog = no fail-closed; present + unknown = `OPENCODE_MODEL_SLUG_UNKNOWN`.)
  - If catalog **present**: load + validate schema. For each of the 8 roles:
    - If slug is a non-empty `provider/slug` string and provider is declared → inject `model: <provider/slug>` into the installed agent's YAML frontmatter (insert key if absent; overwrite if present). Template files are NOT touched.
    - If slug is empty/unknown or provider is undeclared → emit `OPENCODE_MODEL_SLUG_UNKNOWN` and exit non-zero (fail-closed).
    - If catalog JSON is malformed → emit `MODEL_CATALOG_INVALID` (scope-tagged `opencode-catalog`) and exit non-zero.
- **Never** writes to `template/`. **Never** reads or writes `.cursor/model-catalog.local.json`. **Never** reads auth credentials (auth lives in `/connect` / `~/.local/share/opencode/auth.json`).

### Installer hook (T-003 — triple-installer parity — critic NB closed)

`installer.py` / `installer.ps1` / `installer.sh` invoke the materializer when:
- `--host opencode` OR `--host both` is selected, AND
- `.opencode/model-catalog.local.json` exists at the install target.

If the catalog is absent, the installer skips the materializer (no-op; no fail-closed). If the materializer fails (non-zero exit), the installer surfaces the reason code and exits non-zero. Triple-installer parity: all three installers use the same trigger condition and the same error surface. The installer does NOT generate the catalog for the operator — operators create `.opencode/model-catalog.local.json` themselves (or copy from `template/.opencode/model-catalog.local.example.json` and fill in real slugs).

### Validator extension (DQ9 LOCKED — AC-8)

Extend `scripts/model_tier_validate.py` with `--scope opencode-catalog` (default extension; new script only if too coupled — DQ9). The extension adds:

- `check_template_opencode_agents`: grep `template/.opencode/agents/**/*.md` for `model:` field (must be absent) + forbidden vendor slug patterns (`deepseek|moonshot|kimi|glm|claude|gpt|sonnet|opus|haiku|o1|o3|sk-`). D3 grep scope **excludes** `*.example.json` / `*.local.json`. Also grep `template/.opencode/opencode.json{,c}` if present (must not exist in template).
- `validate_opencode_catalog`: load `.opencode/model-catalog.local.json` (if present) → validate schema (`schema_version`, `providers`, `roles` with 8 role keys) → unknown/empty slug → `OPENCODE_MODEL_SLUG_UNKNOWN` → malformed JSON → `MODEL_CATALOG_INVALID` (scope-tagged `opencode-catalog`).
- `check_opencode_example_catalog`: load `template/.opencode/model-catalog.local.example.json` → assert placeholder values only (no real model-id slugs — grep for known slug patterns) → assert ≥2 roles have different providers (AC-7 per-role divergence).
- Reuse existing `check_forbidden_slugs_in_file` helper (extend the forbidden-slug list to cover OpenCode agent files + example catalog).

### Fail-closed reason-code family (DQ3 LOCKED — AC-4)

- **New code**: `OPENCODE_MODEL_SLUG_UNKNOWN` — emitted by the materializer when catalog is present but a role's slug is unknown/empty or provider is undeclared. Single namespaced code; do NOT introduce `OPENCODE_MODEL_CATALOG_INVALID`, `OPENCODE_MODEL_ROLE_SLUG_UNKNOWN`, etc.
- **Reused code**: `MODEL_CATALOG_INVALID` — emitted for malformed OpenCode catalog JSON, scope-tagged `opencode-catalog` (same semantics, different file). No new code pile.
- Existing Cursor-side codes (`MODEL_SLUG_UNKNOWN`, `MODEL_OVERRIDE_SLUG_UNKNOWN`, `MODEL_ROLE_SLUG_UNKNOWN`, `MODEL_TIER_INVALID`, `MODEL_RESOLVE_FALLBACK`, `MODEL_CATALOG_SCHEMA_V2_INVALID`) remain Cursor-side only — not emitted on the OpenCode path.

### Provider mode posture (DQ8 LOCKED — AC-2, AC-6)

- OpenCode host = **always `api` mode** (BYOK via `/connect`). The kit does NOT proxy provider traffic. `MODEL_PROVIDER_MODE=cursor|api` (US-0101 / DEC-0086 §5) is a Cursor-side scratchpad key; on OpenCode it is irrelevant (always `api`). `MODEL_RESOLVE=role_catalog` (US-0102 / DEC-0087) is Cursor-side; on OpenCode the catalog is `.opencode/model-catalog.local.json` (DQ1), not the Cursor role catalog. The two hosts have independent resolution chains.
- Documented in the runbook stub (US-0123 ships one line; US-0126 owns full text).

### Runbook stub (DQ10 LOCKED — AC-10)

`docs/engineering/runbook.md` gets a new h2 `## OpenCode model slug routing (US-0123)` with the locked one-line note: "QA/dev should default to a tool-reliable slug (a model with documented tool-calling support); Chinese API quality is operator model choice. The kit does not endorse a single vendor." US-0126 inherits and expands into a full runbook section. US-0123 does NOT author a full runbook section.

### Gitignore verification (T-006)

`.opencode/.gitignore` (US-0121 Q10) already ignores `*.local.json` under `.opencode/` — `model-catalog.local.json` is covered by the glob. T-006 verifies the glob covers the catalog filename; if the glob is narrower than `*.local.json`, add `model-catalog.local.json` explicitly. Do not duplicate gitignore entries.

### AC-8 contract-test list (locked — 8 markers)

`tests/us0123_contract_test.py` — markers:

| # | Marker | AC |
|---|--------|-----|
| 1 | `test_us0123_template_agents_omit_model` (grep `^model:` in `template/.opencode/agents/*.md` → zero matches; inherits US-0122 AC-7) | AC-1, AC-3 |
| 2 | `test_us0123_no_vendor_slugs_in_template` (D3 grep scoped to `template/.opencode/agents/**/*.md` + `template/.opencode/opencode.json{,c}` if present, **excluding** `*.example.json` / `*.local.json`; forbidden patterns `deepseek|moonshot|kimi|glm|claude|gpt|sonnet|opus|haiku|o1|o3|sk-` → zero hits) | AC-3 |
| 3 | `test_us0123_example_catalog_placeholders_only` (`template/.opencode/model-catalog.local.example.json` exists; role values match `<your-*-slug>` placeholder form; no real model-id slugs) | AC-2, AC-3 |
| 4 | `test_us0123_example_catalog_per_role_divergence` (≥2 roles have different providers in the example catalog — AC-7 per-role divergence) | AC-7, AC-9 |
| 5 | `test_us0123_fail_closed_unknown_slug` (materializer with synthetic catalog having empty/unknown slug → emits `OPENCODE_MODEL_SLUG_UNKNOWN`, exit non-zero) | AC-4 |
| 6 | `test_us0123_materializer_no_op_when_catalog_absent` (materializer with no catalog → no-op, exit 0, installed agents keep `model:` omitted) | AC-1, AC-4 |
| 7 | `test_us0123_auth_store_never_in_template_or_git` (grep for `auth.json`/`api_key`/`apikey`/`sk-` in `template/.opencode/**` → zero hits; `.opencode/.gitignore` covers `*.local.json`; auth lives in `/connect`) | AC-5 |
| 8 | `test_us0123_compose_cursor_unchanged` (`.cursor/model-catalog.local.json` schema unchanged; `MODEL_TIER_<PHASE>` / `MODEL_<PHASE>` / `MODEL_PROVIDER_MODE` / `MODEL_RESOLVE` keys remain Cursor-side; `TOKEN_PROFILE` orthogonal — slug routing ≠ token-cost profile) | AC-6, AC-8 |

Surjective AC coverage: AC-1 (markers 1, 6), AC-2 (marker 3), AC-3 (markers 1, 2, 3), AC-4 (markers 5, 6), AC-5 (marker 7), AC-6 (marker 8), AC-7 (marker 4), AC-8 (full set + marker 8), AC-9 (marker 4 + example catalog providers), AC-10 (T-007 runbook stub). Every AC has ≥1 marker.

## Risks mitigated

All 7 risks from R-0109 US-0123 ACCEPTED, plus 2 research critic NBs closed:

| Risk | Severity | Mitigation |
|------|----------|------------|
| R1: SOT ambiguity between scratchpad, agent frontmatter, and local catalog | MEDIUM → LOW | DQ1 locks ONE SOT (`.opencode/model-catalog.local.json`); marker 1 `test_us0123_template_agents_omit_model` + marker 8 `test_us0123_compose_cursor_unchanged` assert forbidden surfaces stay clean. |
| R2: Vendor slug leakage into `template/.opencode/agents/*.md` or `template/.opencode/opencode.json` | MEDIUM → LOW | DQ2 omits `model:` in template; T-004 `check_template_opencode_agents` (D3 grep scoped, excludes `*.example.json`) + marker 2 enforce. |
| R3: Unknown/empty slug silently falls back to a random model | MEDIUM → LOW | DQ3 single fail-closed `OPENCODE_MODEL_SLUG_UNKNOWN`; T-002 materializer emits code; marker 5 asserts. |
| R4: Chinese API examples committed with live vendor IDs / keys | LOW–MEDIUM → LOW | DQ6 single example surface with placeholders only; T-001 example catalog uses `<your-deepseek-slug>` placeholders; marker 3 asserts; auth keys live in `/connect` (DQ7, AC-5). |
| R5: Per-role vs per-phase granularity mismatch with US-0101/US-0102 | LOW–MEDIUM → LOW | DQ5 per-role catalog on OpenCode, US-0069 phase→role matrix bridges; marker 4 asserts ≥2 roles different providers. |
| R6: Kit accidentally proxies provider traffic | LOW → LOW | DQ8 OpenCode host = always `api` (BYOK via `/connect`), kit does not proxy; marker 7 asserts posture; T-anch compose-do-not-amend verifies AC-2. |
| R7: Validator duplication drift | LOW → LOW | DQ9 extend `scripts/model_tier_validate.py` (preferred) over new script; T-004 extends in place; markers consume the extended validator. |
| C1 (critic NB): `ik_us0123_dq7_catalog_optional_vs_failclosed` | → closed | Absent catalog = no-op (no fail-closed); present + unknown = `OPENCODE_MODEL_SLUG_UNKNOWN`. Marker 6 asserts no-op; marker 5 asserts fail-closed. |
| C2 (critic NB): `ik_us0123_t002_t003_installer_hook_contract` | → closed | T-002 materializer + T-003 installer hook interface locked: trigger = `--host opencode|both` AND catalog present; absent = skip; fail = surface reason code + exit non-zero. Triple-installer parity. |

## Non-goals (this slice)

- **US-0124** (orchestrator plugin spawn loop) — no plugin body; runtime permission-check harness deferred; v1/v2 plugin choice deferred.
- **US-0125** (thin command bodies) — `template/.opencode/commands/` ships `.gitkeep` only (US-0121 pack).
- **US-0126** (full runbook) — T-007 one-liner only.
- **Repo-root `opencode.json`** — not shipped (R-0109 Q6 US-0121 lock preserved).
- **Active kit `.opencode/agents/` mirror** — YAGNI (inherits US-0122 DQ8 / R-0109 Q9 US-0121).
- **Kit-operated proxy for Chinese APIs** — out of scope (AC-2/AC-9; DQ8).
- **Cursor BYOK fixes** — out of scope (AC-6 compose, not amend).
- **Embedding keys** — out of scope.
- **Plugin spawn** — out of scope (US-0124).
- **New validator script** — default rejected (DQ9 extend in place); only if extension proves too coupled.

## Compose guards (UNCHANGED — additive only)

| Compose target | Verification | Result |
|---|---|---|
| US-0101 / DEC-0086 (Cursor tier→alias runtime + `.cursor/model-catalog.local.json`) | OpenCode path additive; Cursor catalog separate; `MODEL_TIER_<PHASE>` / `MODEL_PROVIDER_MODE` Cursor-side only | ✅ untouched |
| US-0102 / DEC-0087 (Cursor direct-slug + role catalog) | OpenCode catalog schema independent; `MODEL_<PHASE>` / `MODEL_RESOLVE` Cursor-side only; volatile-ID rule extended to `template/.opencode/` | ✅ untouched |
| US-0003 (agents gain `model:` on OpenCode) | materializer injects `model:` into installed agents; template agents unchanged | ✅ exists — additive |
| US-0122 / DEC-0122 (permission matrix + `template/.opencode/agents/*.md`) | US-0123 does not edit template agents; materializer writes to installed agents only; `model:` stays omitted in template | ✅ untouched |
| US-0121 (`.opencode/` pack path + `.gitignore` Q10) | `*.local.json` gitignore reused; no new gitignore entry needed | ✅ consumed — additive |
| US-0080 (`TOKEN_PROFILE` orthogonality) | slug routing ≠ token-cost profile; marker 8 asserts | ✅ untouched |

Contract test `test_us0123_compose_cursor_unchanged` (marker 8) enforces at execute boundary.

## Sprint seeds preview (within SPRINT_MAX_TASKS=12)

| Seed | Description | AC |
|------|-------------|-----|
| **T-anch** | Verify `# US-0123` H1 anchor placed AFTER `# US-0122` and BEFORE `US-0089`; DEC-0123 Accepted; compose guards 6/6; 8-marker list locked; materializer + installer hook contract locked in DEC-0123. | AC-6, AC-9 |
| **T-001** | NEW example catalog `template/.opencode/model-catalog.local.example.json` with placeholder `provider/slug` per role — covers DeepSeek, Moonshot, Z.AI, Anthropic, OpenAI + DashScope/Qwen custom provider block. | AC-2, AC-7, AC-9 |
| **T-002** | NEW materializer `scripts/opencode_model_catalog_apply.py` — reads `.opencode/model-catalog.local.json` → injects `model: <provider/slug>` into installed `.opencode/agents/<role>.md` only; no-op when catalog absent; fail-closed `OPENCODE_MODEL_SLUG_UNKNOWN` on unknown/empty slug; `MODEL_CATALOG_INVALID` (scope-tagged) on malformed JSON. | AC-1, AC-4, AC-5 |
| **T-003** | Installer hook — `installer.py` / `installer.ps1` / `installer.sh` invoke materializer when `--host opencode|both` AND catalog present; triple-installer parity; absent = skip; fail = surface reason code + exit non-zero. | AC-1, AC-5 |
| **T-004** | Validator extension `scripts/model_tier_validate.py --scope opencode-catalog` — `check_template_opencode_agents` (D3 grep scoped, excludes `*.example.json`), `validate_opencode_catalog`, `check_opencode_example_catalog` (≥2 roles different providers). | AC-3, AC-8 |
| **T-005** | Contract tests `tests/us0123_contract_test.py` — 8 markers (see AC-8 table above). | AC-8 |
| **T-006** | Gitignore verification — `.opencode/.gitignore` (US-0121 Q10) covers `*.local.json`; verify `model-catalog.local.json` is covered by glob; add explicit entry only if glob is narrower. | AC-5 |
| **T-007** | Runbook stub `docs/engineering/runbook.md` h2 `## OpenCode model slug routing (US-0123)` + one-line note — US-0126 inherits. | AC-10 |
| **T-008** | README + template parity — `check_intake_template_parity.py --scope opencode-adapter` extension for catalog + materializer + validator surface; `its_magic/README.md` cross-link. | AC-8 |
| **T-009** | Installer manifest rows for `template/.opencode/model-catalog.local.example.json` + `scripts/opencode_model_catalog_apply.py` under `[opencode_install_include_paths]` + triple-installer parity. | AC-1 |

**Total: 10 tasks (T-anch + T-001..T-009) — within `SPRINT_MAX_TASKS=12`.** `/sprint-plan` may merge or split within the 12-task budget.

**AC mapping (10 ACs → 10 tasks surjective)**: AC-1 → T-001+T-002+T-003+T-004; AC-2 → T-001; AC-3 → T-004+T-005; AC-4 → T-002+T-005; AC-5 → T-002+T-003+T-006; AC-6 → T-anch+T-005; AC-7 → T-001+T-005; AC-8 → T-005+T-008; AC-9 → T-001+T-anch; AC-10 → T-007.

## DC check

`dc_check=clean`. No `# US-0123` or `## US-0123` existed in `architecture.md` prior to THIS write (verified by R-0109 US-0123 DC check). H1 anchor added per DEC-0076 / BUG-0010 heading policy. Deferral register clean.

## Stop conditions

- `decision_gate=false`
- `missing_acceptance_criteria=none` (10/10 ACs covered by 8 contract-test markers + compose guards + T-007 runbook stub)
- `compose_guards=6/6 UNCHANGED (additive only)`
- `dc_check=clean`
- DQ1..DQ10 LOCKED for US-0123; 7/7 R ACCEPTED; A1 locked; 2 research critic NBs closed; 3 spec critic NBs closed (carried from research)
- Triad baseline `baseline_h2_count=40` preserved (H1 used, not H2)
- Triad `--rollover` ran (state.md was oversize at 1219/1200 lines; rollover archived 1 unit → state.md now 999 lines); `--check` PASS after rollover; heading policy check pending (see below)

## Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called. No write to `mistakes.jsonl`.

## Consequences

- **Positive**: Operators can run `@dev` on DeepSeek and `@po` on Anthropic (or any per-role assignment) before the US-0124 plugin exists; success test (c) for AC-3 is provable via scoped D3 grep; AC-4 fail-closed is provable via `OPENCODE_MODEL_SLUG_UNKNOWN`; epic US-0124..US-0126 inherits the locked SOT + schema + materializer contract via DEC-0123 without re-deriving; US-0101/US-0102/US-0003/US-0122/US-0121/US-0080 compose unchanged.
- **Negative**: One new template file (example catalog); one new script (materializer); one validator extension; one new contract test file (8 markers); one runbook h2 one-liner; installer hook in three installers.
- **Neutral**: US-0121 pack path consumed (additive); US-0122 template agents unchanged; US-0102 volatile-ID rule respected; Cursor `MODEL_*` keys unchanged.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=architecture`, `role=tech-lead`, `story_id=US-0123`, `sprint_id=(pending — created at sprint-plan)`
- `orchestrator_run_id=auto-20260824-01`
- `delivery_mode=ultra_lean`, `macro_phase=plan` (architecture — second canonical phase of `plan` macro per US-0096 / DEC-0082)
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required; this spawn's producer model)
- `fresh_context_marker=tl-US0123-architecture-20260824T162000Z-fresh`, `timestamp=2026-08-24T16:20:00Z` (UTC)
- `evidence_ref=docs/engineering/architecture.md # US-0123 (this section), decisions/DEC-0123.md (companion DEC), docs/engineering/research.md ## R-0109 (US-0123 deepened findings DQ1..DQ10 LOCKED), docs/product/backlog.md ## US-0123 (D1..D10 + 10 ACs + DQ1..DQ10, status OPEN untouched, AC checkboxes untouched), docs/product/acceptance.md US-0123 row (unchecked), docs/product/vision.md ## Intake + Discovery Notes — US-0123, handoffs/po_to_tl.md US-0123 section, handoffs/sovereign_critic_findings.jsonl US-0123 research rows (2 non-blocking carry-forwards closed here), decisions/DEC-0086.md (read-only compose), decisions/DEC-0087.md (read-only compose), decisions/DEC-0122.md (read-only compose), scripts/model_tier_validate.py (grep anchors — DQ9 extend-not-duplicate lock), template/.opencode/agents/*.md (grep ^model: zero matches), docs/engineering/architecture.md # US-0122 (format template), docs/engineering/decisions.md ## DEC-0123 (stub), handoffs/resume_brief.md (US-0123 sovereign-critic PASS prepend)`
- Fresh tech-lead subagent per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to narrow-read files (US-0053). No `.env` reads, no credentials access, no intake-evidence mutation, no backlog status/AC mutation.
- Prior proof consumed: `rp-auto-20260824-01-research-tech-lead-20260824T160500Z-US-0123` (`proof_hash=FAE07A6C872F5A3C7028B00653A9540CEB11BAE8570B252D75676090E24BF351`, ttl 2026-08-24T17:05:00Z — consumed before RUNTIME_PROOF_STALE).
- Triad baseline `baseline_h2_count=40` preserved via H1 anchor (no new H2 `## US-` headings added).

## Strict runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-architecture-tech-lead-20260824T162000Z-US-0123`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"architecture","proof_issued_at":"2026-08-24T16:20:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260824-01-architecture-tech-lead-20260824T162000Z-US-0123","sprint_id":"(pending)","story_id":"US-0123"}`
- `proof_hash=6959A3AD8A262CF404582DDFA30C7C4E273E66E799DEBF1C13CB8C8BD0E32E73` (SHA-256 of sorted-key JSON payload, UTF-8 bytes via python hashlib)
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T17:20:00Z` (UTC = issued_at + 3600s)

## Decision gate

- `decision_gate=false` (companion DEC-0123 authored Accepted in THIS phase; approach A1 locked; DQ1..DQ10 LOCKED for US-0123; 7/7 R ACCEPTED; 2 research critic NBs closed; 3 spec critic NBs closed; DC check clean; compose guards 6/6 UNCHANGED)
- `stop_conditions_met=yes`

## Next scheduled phase

- `next_scheduled_phase=/sprint-plan` (role=tech-lead per US-0069 / DEC-0051 phase→role matrix default; third canonical phase of `plan` macro per ultra_lean; research + architecture + sprint-plan merged into `plan` macro)
- `next_scheduled_role=tech-lead`
- `stop_condition=STOP after architecture completes; hand off via artifacts only to /sprint-plan in fresh tech-lead subagent (BUG-0006). Do not spawn /sprint-plan from this subagent.`

