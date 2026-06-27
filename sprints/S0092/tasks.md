# Sprint S0092 Tasks — US-0102

**sprint_id**: S0092  
**story_refs**: US-0102  
**dec_ref**: DEC-0087 (binding; composes DEC-0086/US-0101 — do not amend)  
**task_count**: 11  
**within_limit**: true (11 ≤ `SPRINT_MAX_TASKS=12`; `SPRINT_AUTO_SPLIT` not triggered)  
**coverage**: AC-1..AC-10 surjective via T-001..T-011 (10 ACs, 11 tasks; architecture seeds 1:1; multi-AC tasks T-001, T-003, T-005, T-006, T-009/T-010/T-011)

> No implementation or test code is authored in this phase — dev owns delivery in `/execute`.

---

## T-001 — **`MODEL_<PHASE>`** scratchpad keys (active + template + local example) — AC-1, AC-5

- **ac_ref**: AC-1, AC-5
- **dec_ref**: DEC-0087 §3, §7; architecture `# US-0102` § Scratchpad keys; § `/ask` phase
- **description**: Document **`MODEL_<PHASE>=<vendor-slug>`** keys for all canonical phase ids (same list as **DEC-0086**, including **`ask`**, **`architecture`**, **`execute`**, …) in active scratchpad comment block + **`template/.cursor/scratchpad.md`** + **`template/.cursor/scratchpad.local.example.md`**. Use **`<your-vendor-slug>`** placeholders only — **no real vendor slugs**. Document merge precedence: **`MODEL_<PHASE>`** > **`MODEL_TIER_<PHASE>`** > **`MODEL_TIER_DEFAULT`** > Cursor alias. Include **`MODEL_ASK`** example.
- **files_affected**:
  - `.cursor/scratchpad.md` (comment block only)
  - `template/.cursor/scratchpad.md`
  - `template/.cursor/scratchpad.local.example.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 1; **`MODEL_TIER_OVERRIDES_PAIRS`** scratchpad pairs; **`test_us0102_direct_override_keys`**, **`test_us0102_ask_phase_reinforcement`**.
- **acceptance_check**:
  - All canonical phase ids documented for **`MODEL_<PHASE>`** keys.
  - Precedence chain comment block present in active + template scratchpad.
  - **`MODEL_ASK`** documented same as other phases.
  - No vendor slugs in template files — placeholders only.
  - Contract subtests **`test_us0102_direct_override_keys`** + **`test_us0102_ask_phase_reinforcement`** pass (after T-009).
- **status**: done

---

## T-002 — **`MODEL_RESOLVE=role_catalog`** enum extension + precedence comment block — AC-10

- **ac_ref**: AC-10
- **dec_ref**: DEC-0087 §3; architecture `# US-0102` § Scratchpad keys; § Precedence chain
- **description**: Extend **`MODEL_RESOLVE`** documented enum to **`alias_only`** | **`local_catalog`** | **`role_catalog`** (default **`alias_only`**) in active + template scratchpad. Add precedence comment block showing 5-step chain including optional step 3 role lookup when **`role_catalog`**.
- **files_affected**:
  - `.cursor/scratchpad.md` (comment block only)
  - `template/.cursor/scratchpad.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 2; **`MODEL_TIER_OVERRIDES_PAIRS`** scratchpad pairs.
- **acceptance_check**:
  - **`role_catalog`** value documented with opt-in semantics.
  - 5-step precedence chain visible in scratchpad comments.
  - Default remains **`alias_only`** — tier-only configs unchanged.
  - Active/template scratchpad parity for touched sections.
- **status**: done

---

## T-003 — Catalog schema **v2** role-based example JSON files (active + template) — AC-3, AC-7

- **ac_ref**: AC-3, AC-7
- **dec_ref**: DEC-0087 §5; architecture `# US-0102` § Catalog schema v2
- **description**: Add **`.cursor/model-catalog.local.example.role-based-balanced.json`** and **`.cursor/model-catalog.local.example.role-based-highend.json`** (+ template mirrors) with **`schema_version: 2`**, required **`tiers`** (cheap/balanced/strong), optional **`roles`** (po, sa, dev, dev_difficult, qa, security, release). All slug values use placeholders (**`<your-po-model-slug>`**, not real vendor ids).
- **files_affected**:
  - `.cursor/model-catalog.local.example.role-based-balanced.json` (new)
  - `.cursor/model-catalog.local.example.role-based-highend.json` (new)
  - `template/.cursor/model-catalog.local.example.role-based-balanced.json` (new)
  - `template/.cursor/model-catalog.local.example.role-based-highend.json` (new)
- **parity_touchpoints**: architecture § Atomic task seeds row 3; **`MODEL_TIER_OVERRIDES_PAIRS`** catalog example pairs; **`test_us0102_catalog_schema_v2`**.
- **acceptance_check**:
  - Both example files validate against v2 schema shape in DEC-0087 §5.
  - All seven role keys present when **`roles`** section included.
  - Placeholder slugs only — no **`glm-*`**, **`claude-*`**, **`composer-*`**, etc.
  - Active/template example files byte-identical.
  - Contract subtest **`test_us0102_catalog_schema_v2`** passes (after T-009).
- **status**: done

---

## T-004 — Template stability — tier-only examples; no vendor slugs in template catalog — AC-7

- **ac_ref**: AC-7
- **dec_ref**: DEC-0087 §3; architecture `# US-0102` § Template policy
- **description**: Ensure **`template/.cursor/scratchpad.md`** shows **`MODEL_TIER_*`** keys as primary examples; **`MODEL_<PHASE>`** documented in comments with placeholders only. Audit **`template/.cursor/model-catalog.local.example.json`** and new role-based examples — no hardcoded vendor slugs. Operator slugs live in **`.cursor/scratchpad.local.md`** and **`.cursor/model-catalog.local.json`** only (gitignored).
- **files_affected**:
  - `template/.cursor/scratchpad.md`
  - `template/.cursor/model-catalog.local.example.json`
  - `template/.cursor/model-catalog.local.example.role-based-balanced.json`
  - `template/.cursor/model-catalog.local.example.role-based-highend.json`
- **parity_touchpoints**: architecture § Atomic task seeds row 4; **`test_us0102_no_vendor_slugs_in_template`**.
- **acceptance_check**:
  - Grep under **`template/`** finds no known vendor slug patterns.
  - Tier-only examples remain primary visible configuration path.
  - Contract subtest **`test_us0102_no_vendor_slugs_in_template`** passes (after T-009).
- **status**: done

---

## T-005 — **`model_tier_lib.py`** unified resolver — 5-step precedence + phase→role mapping — AC-2, AC-4, AC-6

- **ac_ref**: AC-2, AC-4, AC-6
- **dec_ref**: DEC-0087 §2, §4, §6; architecture `# US-0102` § Precedence chain; § Role catalog resolver; § Backward compatibility
- **description**: Extend **`scripts/model_tier_lib.py`** (+ template mirror) with **`resolve_model_for_phase(phase_id, scratchpad, catalog)`** implementing deterministic 5-step precedence: (1) **`MODEL_<PHASE>`** → slug or **`MODEL_OVERRIDE_SLUG_UNKNOWN`**; (2) **DEC-0086** tier chain; (3) role catalog lookup when **`MODEL_RESOLVE=role_catalog`** → **`MODEL_ROLE_SLUG_UNKNOWN`** fall through; (4) **`MODEL_TIER_DEFAULT`**; (5) Cursor alias. Add phase→logical role constants per architecture table (**DEC-0051** + policy keys). v1/v2 catalog load unchanged for tier-only path.
- **files_affected**:
  - `scripts/model_tier_lib.py`
  - `template/scripts/model_tier_lib.py`
- **parity_touchpoints**: architecture § Atomic task seeds row 5; **`test_us0102_precedence_chain`**, **`test_us0102_role_catalog_resolver`**, **`test_us0102_tier_only_backward_compat`**.
- **acceptance_check**:
  - **`resolve_model_for_phase()`** exported and callable.
  - 5-step precedence matches DEC-0087 §2 table.
  - Tier-only configs (no **`MODEL_<PHASE>`**, **`MODEL_RESOLVE=alias_only`**, v1 catalog) produce identical results to pre-US-0102 baseline.
  - Role lookup active only when **`MODEL_RESOLVE=role_catalog`**.
  - Active/template lib byte-identical for touched symbols.
  - Contract subtests **`test_us0102_precedence_chain`**, **`test_us0102_role_catalog_resolver`**, **`test_us0102_tier_only_backward_compat`** pass (after T-009).
- **status**: done

---

## T-006 — Catalog **v2** validation — accept v1; **`MODEL_CATALOG_SCHEMA_V2_INVALID`** — AC-3, AC-8

- **ac_ref**: AC-3, AC-8
- **dec_ref**: DEC-0087 §5, §8; architecture `# US-0102` § Catalog schema v2; § Reason codes
- **description**: Extend catalog validation in **`model_tier_lib.py`** to accept **v1** unchanged and **v2** with optional **`roles`** section. When **`roles`** present, all seven keys required with non-empty slugs. Malformed v2 → **`MODEL_CATALOG_SCHEMA_V2_INVALID`** (distinct from v1 **`MODEL_CATALOG_INVALID`**).
- **files_affected**:
  - `scripts/model_tier_lib.py`
  - `template/scripts/model_tier_lib.py`
- **parity_touchpoints**: architecture § Atomic task seeds row 6; **`test_us0102_catalog_schema_v2`**, **`test_us0102_reason_codes`**.
- **acceptance_check**:
  - v1 catalogs (no **`roles`**) validate as today.
  - v2 with complete **`roles`** validates.
  - Incomplete **`roles`** → **`MODEL_CATALOG_SCHEMA_V2_INVALID`** with remediation text.
  - Contract subtests **`test_us0102_catalog_schema_v2`** + reason-code portion pass.
  - Active/template lib parity maintained.
- **status**: done

---

## T-007 — **`model_tier_validate.py`** extensions — direct slug keys + three new reason codes — AC-8

- **ac_ref**: AC-8
- **dec_ref**: DEC-0087 §4, §8; architecture `# US-0102` § Direct slug validation; § Reason codes
- **description**: Extend **`scripts/model_tier_validate.py`** (+ template mirror) to validate: (1) **`MODEL_<PHASE>`** keys for valid phase ids and non-empty slugs; (2) catalog schema v2 rules; (3) precedence self-test hook. Emit three new fail-closed codes: **`MODEL_OVERRIDE_SLUG_UNKNOWN`**, **`MODEL_ROLE_SLUG_UNKNOWN`**, **`MODEL_CATALOG_SCHEMA_V2_INVALID`**. Extend existing **`MODEL_TIER_*`** validators for v2 catalogs.
- **files_affected**:
  - `scripts/model_tier_validate.py`
  - `template/scripts/model_tier_validate.py`
- **parity_touchpoints**: architecture § Atomic task seeds row 7; **`test_us0102_reason_codes`**; **`MODEL_TIER_OVERRIDES_PAIRS`** validator pair.
- **acceptance_check**:
  - All three new reason codes grep-able in validator + lib.
  - Direct slug validation respects **`MODEL_RESOLVE`** mode table (§4).
  - CLI **`--enforce`** exits non-zero on fail codes.
  - Active/template validator byte-identical.
  - Contract subtest **`test_us0102_reason_codes`** passes (after T-009).
- **status**: done

---

## T-008 — Runbook subsection — direct override + role catalog operator recipe — AC-10

- **ac_ref**: AC-10
- **dec_ref**: DEC-0087 §11; architecture `# US-0102` § Runbook (implied); § Risks
- **description**: Update **`docs/engineering/runbook.md`** (+ template mirror) with US-0102 operator subsection: 5-step precedence chain, **`MODEL_RESOLVE=role_catalog`** enablement recipe, backward-compat note for tier-only operators, reference to **`ai_modell_auslegung_cursor_highend.md`** as non-normative role recommendations, **`dev_difficult`** via direct override or tier **`strong`**.
- **files_affected**:
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 8; **`MODEL_TIER_OVERRIDES_PAIRS`** runbook pair.
- **acceptance_check**:
  - Precedence chain documented with deterministic step order.
  - Role catalog opt-in path documented with fall-through behavior on miss.
  - **`TOKEN_PROFILE`** non-substitution paragraph preserved.
  - Active/template runbook parity for touched sections.
- **status**: done

---

## T-009 — Eight **`test_us0102_*`** contract subtests — AC-9

- **ac_ref**: AC-9
- **dec_ref**: DEC-0087 §9; architecture `# US-0102` § Contract tests + parity
- **description**: Add eight contract subtests in **`tests/auto_command_contract_test.py`**: **`test_us0102_direct_override_keys`**, **`test_us0102_precedence_chain`**, **`test_us0102_catalog_schema_v2`**, **`test_us0102_role_catalog_resolver`**, **`test_us0102_tier_only_backward_compat`**, **`test_us0102_no_vendor_slugs_in_template`**, **`test_us0102_reason_codes`**, **`test_us0102_ask_phase_reinforcement`**. Run `pytest -k us0102` → all eight green.
- **files_affected**:
  - `tests/auto_command_contract_test.py`
- **parity_touchpoints**: architecture § Contract tests table; active-only.
- **acceptance_check**:
  - All eight **`test_us0102_*`** function names present with assertions per architecture table.
  - `pytest -k us0102 tests/auto_command_contract_test.py` exits 0 after T-001..T-008 edits.
  - Tier-only backward compat asserts pre-US-0102 resolution paths unchanged.
- **status**: done

---

## T-010 — **`MODEL_TIER_OVERRIDES_PAIRS`** parity — **`--scope=model-tier-overrides`** — AC-9

- **ac_ref**: AC-9
- **dec_ref**: DEC-0087 §9; architecture `# US-0102` § Contract tests + parity
- **description**: Register **`MODEL_TIER_OVERRIDES_PAIRS`** in **`scripts/check_intake_template_parity.py`** (+ template mirror) with **`--scope=model-tier-overrides`** extending **`--scope=model-tier`** family. Cover scratchpad override docs, v2 catalog examples, resolver literals, runbook subsection.
- **files_affected**:
  - `scripts/check_intake_template_parity.py`
  - `template/scripts/check_intake_template_parity.py`
- **parity_touchpoints**: architecture § Atomic task seeds row 10; **`test_us0102_template_parity_scope`** (if added) or parity script self-check.
- **acceptance_check**:
  - **`MODEL_TIER_OVERRIDES_PAIRS`** table covers scratchpad, catalog examples, lib, validator, runbook pairs.
  - `python scripts/check_intake_template_parity.py --scope=model-tier-overrides` → **`[INTAKE_TEMPLATE_PARITY_OK]`**.
  - Active/template parity script byte-identical for new scope.
- **status**: done

---

## T-011 — Harness section **§26AA** — AC-9

- **ac_ref**: AC-9
- **dec_ref**: DEC-0087 §9; architecture `# US-0102` § Atomic task seeds row 11
- **description**: Register harness section **§26AA** (next after **§26Z**) in **`tests/run-tests.ps1`** + **`tests/run-tests.sh`** covering `pytest -k us0102` and `python scripts/check_intake_template_parity.py --scope=model-tier-overrides`.
- **files_affected**:
  - `tests/run-tests.ps1`
  - `tests/run-tests.sh`
- **parity_touchpoints**: architecture § Atomic task seeds row 11; harness **§26AA**.
- **acceptance_check**:
  - Harness **§26AA** registered in both run-tests scripts after **§26Z**.
  - Section runs `pytest -k us0102` and parity scope command.
  - Both harness scripts include identical section label and commands.
- **status**: done

---

## Recommended /execute ordering

1. **T-001** → **T-002** — Tranche A (scratchpad keys + MODEL_RESOLVE docs)
2. **T-003** → **T-004** — Tranche B (catalog v2 examples + template stability)
3. **T-005** → **T-006** → **T-007** — Tranche C (resolver + catalog validation + CLI validator)
4. **T-008** — Tranche D (runbook)
5. **T-009** — contract subtests (after scripts/docs)
6. **T-010** → **T-011** — parity scope + harness (last)
