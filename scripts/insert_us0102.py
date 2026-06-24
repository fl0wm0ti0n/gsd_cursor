"""Insert US-0102 story block into backlog.md before the Bug issues section."""
import sys
import re

backlog_path = r'c:\flowGit\sonstiges\gsd_cursor\docs\product\backlog.md'

# Read file in binary to preserve line endings
with open(backlog_path, 'rb') as f:
    data = f.read()

content = data.decode('utf-8')

# Find the Bug issues canonical section (line-level)
lines = content.split('\n')
target_idx = None
for i, line in enumerate(lines):
    if line.rstrip('\r') == '## Bug issues (canonical)':
        target_idx = i
        break

if target_idx is None:
    print("ERROR: Could not find '## Bug issues (canonical)' line", file=sys.stderr)
    sys.exit(1)

# Check if US-0102 is already present
if any('## US-0102' in line for line in lines):
    print("US-0102 already present; skipping insert", file=sys.stderr)
    sys.exit(0)

# US-0102 story block with CRLF line endings to match file
# (we use explicit \r\n to match the file's Windows line endings)
CRLF = '\r\n'
us0102_lines = [
    '## US-0102 — Direct per-phase model slug override and role-based catalog presets (US-0101 extension)',
    '- user_visible: true',
    '- Title: Extend US-0101 tier-based model selection with direct per-phase slug override and role-based catalog presets, while retaining 3-tier baseline',
    '- Summary: US-0101 delivered per-phase `MODEL_TIER_<PHASE>` (cheap/balanced/strong) → Cursor alias mapping (fast/inherit) with optional local catalog for vendor slugs. Operators now request a second axis: **direct per-phase model slug assignment** (`MODEL_<PHASE>=<vendor-slug>`) that bypasses the tier indirection layer, plus **role-based catalog presets** (PO/SA/DEV/QA model profiles per `ai_modell_auslegung_cursor_highend.md`) for operators who want curated model sets without manual tier mapping. The 3-tier system remains as the default/fallback layer: **precedence** `MODEL_<PHASE>` > `MODEL_TIER_<PHASE>` > `MODEL_TIER_DEFAULT` > Cursor alias (local catalog or stable alias). The `/ask` phase (already in US-0101 default matrix as `cheap`) is reinforced with direct override support. **Compose with US-0101/DEC-0086** (do not amend — US-0101 stays DONE). **Backward compatible**: tier-only configurations continue to work unchanged. **No volatile vendor IDs in template files** — direct slug keys and role-based presets live in local catalog JSON (gitignored) only; templates keep Cursor-stable identifiers. New catalog schema v2 extends v1 with optional `roles` section. New contract tests `test_us0102_*` validate precedence, schema, backward compatibility.',
    '- Priority: P2',
    '- Status: OPEN',
    '- Decomposition (US-0051):',
    '  - **Single story** — direct override scratchpad keys, precedence logic, catalog schema v2, role-based presets, backward compatibility, validator updates, contract tests ship as one vertical slice; splitting would ship override logic without catalog integration or reverse.',
    '  - **Rationale**: "tier system stays default; advanced operators can assign exact models per phase or pick a role-based preset" without breaking US-0101 DONE status or forcing tier users to migrate.',
    '- Overlap / duplicate evaluation:',
    '  - **US-0101 / DEC-0086 (DONE)**: per-phase tier selection — **compose, do not amend**: US-0101 stays DONE; US-0102 adds a second overlay axis (direct slug override + role-based catalog). Precedence documented: `MODEL_<PHASE>` > `MODEL_TIER_<PHASE>` > `MODEL_TIER_DEFAULT` > Cursor alias. No changes to US-0101 ACs or DEC-0086 locks.',
    '  - **US-0080 / DEC-0062 (DONE)**: `TOKEN_PROFILE` — **orthogonal**: direct slug override still selects LLM identity (not context breadth); non-substitution paragraph in runbook.',
    '  - **US-0003 (DONE)**: subagent definitions — **unchanged**: template agents keep Cursor-stable aliases; direct slugs and role presets live in local catalog only (no volatile vendor IDs in templates).',
    '  - **US-0092 / DEC-0078 (DONE)**: outer driver / SDK agents — **distinct**: document optional per-send `model` for programmatic paths; out of scope for mandatory IDE resolver v1.',
    '  - **US-0023 / US-0048 (DONE)**: fresh subagent isolation — **unchanged**: direct slug override must not weaken spawn-only or isolation evidence gates.',
    '- Intake pack evidence (**small-intake-pack**):',
    '  - `selected_pack=small-intake-pack` (bounded refinement of US-0101; clear scope expansion)',
    '  - `asked_topics=` all five small-pack keys covered',
    '  - `missing_topics=(none)`',
    '  - `assumptions_confirmed=(none)`',
    '  - `intake_evidence_ref=handoffs/intake_evidence/US-0102-intake-20260624.json`',
    '- Acceptance:',
    '  - [ ] AC-1: **Direct per-phase slug override scratchpad keys** — document `MODEL_<PHASE>=<vendor-slug>` keys (canonical phase ids: same as US-0101 list, including `ask`). Values are direct vendor model slugs (e.g. `MODEL_EXECUTE=kimi-k2.7-code`). **Forbidden** in `template/.cursor/scratchpad.md`: hardcoded vendor slugs (document only in `.cursor/scratchpad.local.md` examples). Merge precedence for model resolution: `MODEL_<PHASE>` > `MODEL_TIER_<PHASE>` > `MODEL_TIER_DEFAULT` > Cursor alias (local catalog or stable alias).',
    '  - [ ] AC-2: **Precedence validation and resolution logic** — `scripts/model_tier_lib.py` (or new `scripts/model_overrides_lib.py`) implements deterministic resolution: (1) check `MODEL_<PHASE>` scratchpad key → return slug or fail-closed `MODEL_OVERRIDE_SLUG_UNKNOWN`; (2) fall back to `MODEL_TIER_<PHASE>` tier → resolve via US-0101 chain; (3) fall back to `MODEL_TIER_DEFAULT` tier → resolve; (4) fall back to Cursor stable alias per US-0101 AC-3. Unknown slug in step (1) → `MODEL_OVERRIDE_SLUG_UNKNOWN` reason code with remediation text.',
    '  - [ ] AC-3: **Local catalog schema v2 with role-based presets** — extend `.cursor/model-catalog.local.json` schema from v1 to v2: add optional `roles` section alongside existing `tiers`. Schema: `{schema_version: 2, tiers: {cheap, balanced, strong}, roles: {po, sa, dev, dev_difficult, qa, security, release}, notes}`. Role slugs follow `ai_modell_auslegung_cursor_highend.md` recommendations. **Backward compatible**: v1 catalogs (no `roles`) still work; v2 catalogs are opt-in. New example catalogs: `.cursor/model-catalog.local.example.role-based-balanced.json`, `.cursor/model-catalog.local.example.role-based-highend.json` (placeholder slugs only).',
    '  - [ ] AC-4: **Role-based resolver (opt-in)** — scratchpad flag `MODEL_RESOLVE=alias_only|local_catalog|role_catalog` (default `alias_only`). When `role_catalog`, resolver looks up phase → role mapping (from `AUTO_ROLE_RESEARCH`, `AUTO_ROLE_PLAN_VERIFY`, or phase→role defaults per `US-0069 / DEC-0051`) → role slug from catalog. Precedence: `MODEL_<PHASE>` > `MODEL_TIER_<PHASE>` > `role_catalog` role lookup > `MODEL_TIER_DEFAULT` > Cursor alias. Role lookup fails → `MODEL_ROLE_SLUG_UNKNOWN` → fall back to tier or alias.',
    '  - [ ] AC-5: **/ask phase reinforcement** — `/ask` phase already in US-0101 default matrix as `cheap` tier; reinforce with direct override support: `MODEL_ASK=<slug>` scratchpad key works same as other phases. No change to default matrix (keep `ask: cheap`); no change to US-0101 AC-1 (phase list already includes `ask`).',
    '  - [ ] AC-6: **Backward compatibility** — existing US-0101 configurations (tier-only, no direct overrides, v1 catalogs) continue to work unchanged. No migration required. Validator accepts both v1 and v2 catalog schemas. Contract tests verify tier-only resolution still produces correct aliases without direct override keys present.',
    '  - [ ] AC-7: **Template stability and volatile-ID protection** — `template/.cursor/scratchpad.md` examples show only `MODEL_TIER_*` keys (no `MODEL_<PHASE>` vendor slugs). `template/.cursor/model-catalog.local.example.json` and role-based examples use placeholder slugs (`<your-po-model-slug>`, not `glm-5.2` directly). Operator configures slugs in `.cursor/scratchpad.local.md` and `.cursor/model-catalog.local.json` only (gitignored). Forbidden: hardcoded vendor slugs in `template/` files (grep check in contract tests).',
    '  - [ ] AC-8: **Validator + reason codes** — `scripts/model_tier_lib.py` extends to validate: (1) direct slug keys (`MODEL_<PHASE>=<slug>`) for valid phase ids and non-empty slugs; (2) catalog schema v2 (roles section optional, but when present must have valid slugs); (3) precedence resolution logic; (4) backward compatibility (v1 catalogs). New fail-closed reason codes: `MODEL_OVERRIDE_SLUG_UNKNOWN` (direct slug not recognized), `MODEL_ROLE_SLUG_UNKNOWN` (role catalog lookup failed), `MODEL_CATALOG_SCHEMA_V2_INVALID` (v2 schema validation failure). Extend existing `MODEL_TIER_*` reason codes to handle v2 catalogs.',
    '  - [ ] AC-9: **Contract tests + template parity** — `test_us0102_*` markers validate: (1) direct slug scratchpad keys (`test_us0102_direct_override_keys`), (2) precedence resolution (`test_us0102_precedence_chain`), (3) catalog schema v2 (`test_us0102_catalog_schema_v2`), (4) role-based resolver (`test_us0102_role_catalog_resolver`), (5) backward compatibility (`test_us0102_tier_only_backward_compat`), (6) template stability (`test_us0102_no_vendor_slugs_in_template`), (7) reason code inventory (`test_us0102_reason_codes`), (8) `/ask` phase reinforcement (`test_us0102_ask_phase_reinforcement`). **`check_intake_template_parity.py --scope=model-tier-overrides`** added to existing `--scope=model-tier` family.',
    '  - [ ] AC-10: **Documentation + runbook** — `.cursor/scratchpad.md` documents `MODEL_<PHASE>` keys with examples in comments (no vendor slugs). Runbook and architecture `# US-0102` documents direct override precedence, role-based resolution, backward compatibility. `ai_modell_auslegung_cursor_highend.md` referenced in runbook as role-based recommendation source (not normative).',
    '- Boundaries:',
    '  - In scope: direct per-phase model slug scratchpad keys, role-based catalog presets, `/ask` phase reinforcement, backward compatibility for tier system.',
    '  - Out of scope: changing US-0101 DONE status or DEC-0086 locks; requiring migration from tier-based to direct override; forcing operators to use role-based catalogs; modifying Cursor billing-plan enforcement; fixing Cursor subagent BYOK bugs (document only); changing mandatory QA/release gate semantics; TOKEN_PROFILE behavior changes.',
    '- related_us: US-0101, US-0003, US-0023, US-0048, US-0069, US-0080, US-0092',
    '- intake_evidence_ref: handoffs/intake_evidence/US-0102-intake-20260624.json',
    '- intake_notes (2026-06-24, PO, `cursor-20260624-US0102-intake`, `INTAKE_GUIDED_MODE=1`, `INTAKE_WORK_ITEM_KIND=story`): **`/intake`** **PASS** — operator (German/English): extend US-0101 with direct per-phase model slug assignment (bypass tier indirection) + role-based catalog presets (PO/SA/DEV/QA profiles from `ai_modell_auslegung_cursor_highend.md`); retain 3-tier system as default/fallback; include `/ask` phase; backward compatible; no volatile vendor IDs in template files; compose with US-0101/DEC-0086 (do not amend). **small-intake-pack**; all 5 topics covered; validator **`[INTAKE_EVIDENCE_VALIDATION_OK]`**. Decomposition evaluator → single story. Overlap vs US-0101 confirms composition (not amendment). Research stub deferred (small refinement of existing US-0101). **Status: OPEN** per **US-0045**. **Next**: **`/architecture`** (fresh **tech-lead**) for **US-0102** — no `/discovery` needed (clear scope, no new problem framing).',
    '',
]

# Build the US-0102 block as bytes with CRLF endings
us0102_block = CRLF.join(us0102_lines)
# Insert with leading blank line (so there's a blank line between US-0101 release_notes and US-0102 start)
# target_idx is the line "## Bug issues (canonical)"; we want to insert before the blank line before it
# Find the blank line before target_idx (should be target_idx - 1 if it's empty)
insert_idx = target_idx
# Walk back to find the first non-empty line; insert after that
while insert_idx > 0 and lines[insert_idx - 1].strip() == '':
    insert_idx -= 1

# Insert blank line + US-0102 block + blank line before Bug issues section
to_insert = [CRLF] + [line + CRLF for line in us0102_lines[:-1]] + [CRLF]
new_lines = lines[:insert_idx+1] + [l.rstrip(CRLF) for l in to_insert] + lines[insert_idx+1:]

new_content = '\n'.join(new_lines)
new_data = new_content.encode('utf-8')
with open(backlog_path, 'wb') as f:
    f.write(new_data)
print(f"OK: US-0102 block inserted at line {insert_idx+1} (before '## Bug issues (canonical)')")
