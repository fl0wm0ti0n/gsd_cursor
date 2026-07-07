# Sprint S0115 — Tasks (US-0115)

**sprint_id**: S0115
**story_refs**: US-0115
**dec_ref**: none (companion_dec=none; US-0115 documentation-only)
**architecture_ref**: `docs/engineering/architecture.md#US-0115` (h1 section appended in architecture phase; approach_locked=A1)
**research_ref**: `docs/engineering/research.md` `R-0103`
**task_count**: 6
**within_limit**: true (6 ≤ `SPRINT_MAX_TASKS=12`)
**coverage**: AC-1..AC-8 surjective via T-001..T-006 (8 ACs, 6 tasks; multi-AC tasks T-002 (AC-2+AC-7), T-005 (AC-4+AC-6))

---

## Task-to-AC Bijection Table

| Task ID | Title | ACs Satisfied |
|---------|-------|---------------|
| T-001 | Add `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` umbrella section under `## Commands and workflow` | AC-1 |
| T-002 | Add 7 per-feature `#### US-xxxx` operator subsections nested under umbrella (US-0034 → US-0084 → US-0086 → US-0093 → US-0096 → US-0101 → US-0102; cross-link + net-new narrative + bidirectional pointers + runbook cross-links) | AC-2, AC-7 |
| T-003 | Extend `### Full scratchpad reference (detailed)` with `### Integration & observability keys (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` sub-block (net-new keys + cross-link pointers + reason-code-only entries) | AC-3 |
| T-004 | Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md` | AC-5 |
| T-005 | Run validators (`validate_readme_feature_coverage.py --enforce`, `validate_doc_profile.py`, `check-user-visible-metadata.py`) and fix any drift | AC-4, AC-6 |
| T-006 | Run regression tests (`pytest tests/scratchpad_example_parity_test.py -q`); confirm green | AC-8 |

**Total**: 6 tasks covering 8 ACs (surjective).

---

## Task Seeds

### T-001: Add `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` umbrella section

**Coverage**: AC-1
**Risk**: LOW
**Dependencies**: None
**Files to touch**:
- `its_magic/README.md` (append new `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` section under `## Commands and workflow` (L350), placed **immediately after** the closing of the US-0114 release & distribution umbrella block (which ends before L1410 `### Full scratchpad reference (detailed)`), keeping the three family umbrellas visually adjacent as siblings in release order: US-0113 sovereign-loop era (L940) → US-0114 release & distribution (L1225) → US-0115 integration & observability)

**Scope**:
- Add `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` umbrella section containing:
  - **Default-off posture callout (optional features)** — explicit statement that optional features (US-0034 cross-repo observability, US-0096 active context handoff, US-0101 model tier resolution, US-0102 role-based model catalog) are opt-in via scratchpad keys and impose zero overhead when disabled.
  - **Always-on framing (publish/QA guards)** — US-0084 (codebase map freshness gate at `npm publish`), US-0086 (handoff hygiene validator routing), US-0093 (scratchpad drift detector during `/qa` and `/verify-work`) are always-on machinery, not opt-in toggles. Frame as "automatic when running `npm publish` / `/qa` / `/verify-work`" rather than "enable to turn on".
  - **7-step recommended enable order** — dependency chain: `US-0034` (cross-repo observability master enable) → `US-0096` (delivery mode + lean memory + active context handoff) → `US-0101` (model tier default + catalog + resolver + fallback + provider mode) → `US-0102` (role-based model slug overrides, composes on US-0101) → `US-0084` (publish-time freshness gate) → `US-0086` (handoff hygiene validator) → `US-0093` (scratchpad drift detector). Order rationale: optional feature enables first (master toggles in dependency order) → always-on guards last (no enable needed — informational ordering for the operator narrative).
  - **Runbook pointer line** — single cross-link to an integration & observability runbook section (existing anchor only; no content duplication). Recommended target: `## Runtime QA autopilot contract (US-0065 / DEC-0047)` (runbook L1486) as the parent h2 umbrella covering US-0093 + the family-adjacent US-0065 contract, or per-feature anchors as appropriate.
  - **Zero-overhead-when-off contract paragraph** — mirrors the `.cursor/scratchpad.md` `# Default-off` pattern: disabled optional features incur no runtime cost, no artifact emission, no side effects. Always-on guards only fire at their triggering lifecycle event (`npm publish` / `/qa` / `/verify-work`).

**Verification step**:
- `its_magic/README.md` contains a `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` heading under `## Commands and workflow` and after the US-0114 release & distribution umbrella block (i.e., before `### Full scratchpad reference (detailed)` at L1410).
- The umbrella section names all 7 in-scope features (US-0034/US-0084/US-0086/US-0093/US-0096/US-0101/US-0102) at least once.
- The umbrella section contains the 7-step recommended enable order with all 7 features listed in order (US-0034 → US-0096 → US-0101 → US-0102 → US-0084 → US-0086 → US-0093).
- The umbrella section contains a default-off posture callout (for optional features) and an always-on framing note (for publish/QA guards) and a zero-overhead-when-off contract paragraph.
- The umbrella section contains a runbook cross-link (existing anchor; no new runbook content added to `docs/engineering/runbook.md`).

---

### T-002: Add 7 per-feature `#### US-xxxx` operator subsections nested under the umbrella

**Coverage**: AC-2, AC-7
**Risk**: LOW–MEDIUM (US-0096 net-new narrative + US-0101/US-0102 angle boundary)
**Dependencies**: T-001 (umbrella section must exist first to nest under)
**Files to touch**:
- `its_magic/README.md` (add 7 `#### US-xxxx` subsections nested under the T-001 umbrella, ordered **US-id-ascending** (deterministic — matches catalog one-liner order): US-0034 → US-0084 → US-0086 → US-0093 → US-0096 → US-0101 → US-0102)

**Scope**:
- Add 7 per-feature `#### US-xxxx` operator subsections. Each subsection contains:
  - **1–3 sentence narrative** — what the feature does (integration & observability angle), grounded in the backlog row + scratchpad keys + runbook anchor.
  - **Master enable flag + related keys with defaults** (where applicable — see per-feature shape below).
  - **Zero-overhead-when-off wording** (for optional features) OR **always-on framing** (for publish/QA guards) — mirrors `.cursor/scratchpad.md` `# Default-off` pattern.
  - **Runbook cross-link** — existing anchor only (AC-7 forbids duplication). All 7 cross-link targets already exist (R-0103 verified):
    - US-0034 → `## Optional cross-repo observability mode (US-0034)` (runbook L1167, h2).
    - US-0084 → `### Published npm installer.sh / POSIX dash (US-0084)` (runbook L1441, h3) + `### Automated checks (US-0084)` (runbook L1459, h3).
    - US-0086 → `### Manual vs automation routing (US-0086)` (runbook L1398, h3) + `### Optional deterministic CI routing recipe (US-0086)` (runbook L1471, h3).
    - US-0093 → `### Browser UAT self-test (US-0093)` (runbook L1999, h3, parent h2 = `## Runtime QA autopilot contract (US-0065 / DEC-0047)` L1486).
    - US-0096 → `### Delivery modes (US-0096 / DEC-0082)` (runbook L591, h3).
    - US-0101 → `## Model tier resolution (US-0101 / DEC-0086)` (runbook L653, h2).
    - US-0102 → `## Role-based model catalog (US-0102 / DEC-0087)` (runbook L771, h2).

- **Per-feature narrative shape (R-0103 grounded)**:
  - **US-0034 — Cross-repo compatibility observability** (cross-link only to existing L585 README section per R-0103 recommendation (a); preserves byte-stability of pre-US-0115 L585 `### Optional cross-repo observability (US-0034)` h3). Subsection = short pointer block: "See `### Optional cross-repo observability (US-0034)` above for the operator guide; this entry records the integration & observability family angle." + runbook cross-link to L1167. Master enable flag: `CROSS_REPO_OBSERVABILITY=0|1` (default `0`); related keys `COMPATIBILITY_GATE_ON_CRITICAL=0|1` (default `1`), `COMPATIBILITY_SOURCES=` (semicolon-separated `repo=/module=/contract=/docs=` declarations; default empty). Zero-overhead-when-off wording: when `CROSS_REPO_OBSERVABILITY=0` (default), the workflow adds zero required compatibility overhead — no source probing, no gate evaluation, no release block.
  - **US-0084 — Codebase map freshness gate** (always-on publish-time guard, NOT a default-off optional feature). Subsection narrates: (1) what the gate checks (POSIX `installer.sh` LF line endings + agent-driven codebase map freshness at `## Codebase map` surface); (2) when it runs (`npm publish` invocation via `guard_installer_publish.py`); (3) failure mode (`INSTALL_MANIFEST_ERROR` reason code, publish aborts); (4) runbook cross-link to L1441/L1459. No scratchpad key block to document — reference the shared `INSTALL_MANIFEST_ERROR` reason code only (also surfaced by US-0062/US-0041 per R-0102 § AC-3 reference extension).
  - **US-0086 — Handoff hygiene validator** (always-on routing guard). Subsection narrates the 3 routing modes (manual operator terminal vs automation CI vs deterministic-CI recipe) + the grouped cross-link to the remote-execution keys (`REMOTE_EXECUTION=0|1` (default `0`), `REMOTE_CONFIG`, `AUTO_REMOTE_AUTOMATION_PROFILE=off|deterministic_v1` (default `off`), `AUTO_REMOTE_ENVIRONMENT_LABEL`) — full reference rows live in the main scratchpad reference list above L1410 per byte-stability contract (mirrors US-0114's `AUTO_INSTALL_DEPS`/`AUTO_RELEASE_NOTES` grouped cross-link pattern) + runbook cross-link to L1398/L1471. Zero-overhead-when-off wording: when `REMOTE_EXECUTION=0` (default) and `AUTO_REMOTE_AUTOMATION_PROFILE=off` (default), the workflow adds zero remote-execution overhead — no Docker/SSH probing, no environment-label injection. Manual operator terminal is the default routing.
  - **US-0093 — Scratchpad drift detector** (always-on QA-time guard). Subsection narrates: (1) what it checks (scratchpad header drift + backlog status drift via `browser_smoke` probe); (2) when it runs (`/qa` and `/verify-work` invocations — no runtime cost outside those phases); (3) `probe_kind=browser_smoke` distinct from US-0109's post-deploy `two_stage` smoke probe; (4) failure modes (`SCRATCHPAD_HEADER_DRIFT`, `BACKLOG_STATUS_DRIFT` reason codes); (5) runbook cross-link to L1999 (parent h2 = US-0065 runtime QA autopilot contract L1486). No scratchpad key block to document — reference the reason codes only.
  - **US-0096 — Active context handoff** (**net-new narrative** per R-0103 CORRECTION — no pre-existing L591 README section; L591 is a runbook line). Subsection narrates: delivery modes (`standard` / `ultra_lean` / `mega_quick`) with layered per-story lean memory — `LEAN_MEMORY_READ`/`LEAN_MEMORY_WRITE` toggle the lean pack/active-context paths; `LEAN_COLD_READ_MAX_SECTIONS` / `LEAN_STATE_INDEX_ROWS` bound cold reads; `AUTO_DELIVERY_ROUTING` selects scratchpad-only vs backlog-then-scratchpad routing. Master enable flags + related keys with defaults: `DELIVERY_MODE=standard|ultra_lean|mega_quick` (documentation default = `standard` per the `.cursor/scratchpad.md` comment block L173; note this repo dogfoods `ultra_lean`), `LEAN_MEMORY_READ=0|1` (default `1` when pack/active-context paths exist), `LEAN_MEMORY_WRITE=0|1` (default `1`), `LEAN_COLD_READ_MAX_SECTIONS` (default `4`), `LEAN_STATE_INDEX_ROWS` (default `80`), `AUTO_DELIVERY_ROUTING=scratchpad_only|backlog_then_scratchpad` (default `scratchpad_only`). **Cross-link pointer to US-0114's `### Release & distribution keys` block** for the canonical `DELIVERY_MODE` row (US-0114 owns that row per byte-stability; US-0096 narrative here documents the active-context-handoff angle, not the release-workflow angle). Runbook cross-link to L591. Zero-overhead-when-off wording: when `LEAN_MEMORY_READ=0` and `LEAN_MEMORY_WRITE=0`, the lean pack/active-context paths are disabled and the workflow falls back to standard cold reads.
  - **US-0101 — Model tier resolution** (resolver mechanics angle owned by US-0115; release-workflow angle shipped in US-0114's US-0112 installer-payload subsection). Subsection narrates the model tier resolver mechanics: `MODEL_TIER_DEFAULT` (default tier), `MODEL_CATALOG` (path to catalog), `MODEL_RESOLVE` (resolution strategy), `MODEL_FALLBACK` (fallback chain), `MODEL_PROVIDER_MODE` (provider selection). Bidirectional "see US-0114 for installer-payload angle on US-0112 preset shipping" pointer (mirror US-0113/US-0114 pointer convention — US-0114's US-0112 subsection already ships the "see US-0115" pointer per S0114 RELEASED state). Runbook cross-link to L653. Zero-overhead-when-off wording: when no `MODEL_TIER_DEFAULT` is set, the resolver falls back to the framework default tier.
  - **US-0102 — Role-based model catalog** (role catalog angle owned by US-0115; release-workflow angle shipped in US-0114's US-0112 installer-payload subsection). Subsection narrates the role-based model catalog: `MODEL_SLUG_<PHASE_ID>` (per-phase role-based model slug overrides; composes on US-0101's `MODEL_CATALOG` — set the catalog path first, then per-phase slug overrides). Bidirectional "see US-0114 for installer-payload angle on US-0112 preset shipping" pointer (mirror US-0113/US-0114 pointer convention). Runbook cross-link to L771. Zero-overhead-when-off wording: when no `MODEL_SLUG_<PHASE_ID>` overrides are set, the catalog falls back to `MODEL_TIER_DEFAULT` (US-0101).

- **Bidirectional "see US-0114 for installer-payload angle" pointers**: US-0101 and US-0102 subsections MUST include explicit "see US-0114 for installer-payload angle on US-0112 preset shipping" pointers (angle-distinct narrative contract — US-0115 owns resolver mechanics + role catalog DEC-0086/DEC-0087; US-0114 owns installer payload US-0112 presets + version sync). US-0114's US-0112 subsections already ship the "see US-0115" pointer per S0114 RELEASED state.

**Verification step**:
- `its_magic/README.md` contains exactly 7 `#### US-xxxx` subsections nested under the `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` umbrella.
- Subsection order is US-id-ascending: US-0034, US-0084, US-0086, US-0093, US-0096, US-0101, US-0102.
- US-0034 subsection is a cross-link-only pointer block to the existing L585 README section + runbook cross-link to L1167 (byte-stability of L585 preserved — no edits to L585).
- US-0096 subsection is net-new narrative (R-0103 CORRECTION honored — no reference to a pre-existing L591 README section) grounded in `.cursor/scratchpad.md` L173–186 + runbook cross-link to L591.
- US-0084/US-0086/US-0093 subsections frame as always-on publish/QA guards + reason codes + runbook cross-links (no scratchpad key blocks; no "enable to turn on" wording).
- US-0101/US-0102 subsections include bidirectional "see US-0114 for installer-payload angle" pointers + runbook cross-links to L653/L771.
- Each optional-feature subsection (US-0034/US-0096/US-0101/US-0102) contains the master enable flag(s) with default value(s) + a zero-overhead-when-off statement.
- Each subsection contains a runbook cross-link to an existing anchor (no new runbook content added to `docs/engineering/runbook.md`).
- No runbook content is duplicated in the README (AC-7).

---

### T-003: Extend `### Full scratchpad reference (detailed)` with `### Integration & observability keys` sub-block

**Coverage**: AC-3
**Risk**: MEDIUM (3rd-story cumulative byte-stability surface — highest risk in this sprint)
**Dependencies**: T-002 (per-feature subsections complete first to keep narrative+reference ordering coherent)
**Files to touch**:
- `its_magic/README.md` (extend the `### Full scratchpad reference (detailed)` section, L1410, with a `### Integration & observability keys (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` sub-block as a sibling to US-0113's `### Sovereign-loop era keys (US-0103–US-0112)` (L1427) and US-0114's `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` (L1551))

**Scope**:
- Append `### Integration & observability keys (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` sub-block as a sibling to (after) US-0114's `### Release & distribution keys` block (L1551) under `### Full scratchpad reference (detailed)` (L1410).
- **Net-new key rows ONLY** (architecture lock — preserve US-0113 L1427 + US-0114 L1551 byte-stability, no duplicate rows):
  - **US-0034 net-new keys** (from `.cursor/scratchpad.md` L220–228): `CROSS_REPO_OBSERVABILITY=0|1` (default `0` — master enable), `COMPATIBILITY_GATE_ON_CRITICAL=0|1` (default `1` — gate posture when observability is on), `COMPATIBILITY_SOURCES=` (semicolon-separated `repo=/module=/contract=/docs=` declarations; default empty). Document defaults + flip guidance.
  - **US-0096 net-new keys** (from `.cursor/scratchpad.md` L173–186): `LEAN_MEMORY_READ=0|1` (default `1` when pack/active-context paths exist), `LEAN_MEMORY_WRITE=0|1` (default `1`), `LEAN_COLD_READ_MAX_SECTIONS` (default `4`), `LEAN_STATE_INDEX_ROWS` (default `80`), `AUTO_DELIVERY_ROUTING=scratchpad_only|backlog_then_scratchpad` (default `scratchpad_only`). Document defaults + flip guidance.
  - **US-0101 net-new keys** (from `.cursor/scratchpad.md` L355–374): `MODEL_TIER_DEFAULT` (default tier), `MODEL_CATALOG` (path to catalog), `MODEL_RESOLVE` (resolution strategy), `MODEL_FALLBACK` (fallback chain), `MODEL_PROVIDER_MODE` (provider selection mode). Document defaults + flip guidance.
  - **US-0102 net-new keys** (from `.cursor/scratchpad.md` L355–374 region): `MODEL_SLUG_<PHASE_ID>` (per-phase role-based model slug overrides; composition-on-US-0101 note — set `MODEL_CATALOG` first, then per-phase slug overrides). Document defaults + composition note.
- **Cross-link pointer to US-0114's `### Release & distribution keys` block** for the overlapping `DELIVERY_MODE` row (US-0114 owns that row per byte-stability contract; US-0096 narrative documents the active-context-handoff angle, not the release-workflow angle). Cross-link pointer wording: "See `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` above for the canonical `DELIVERY_MODE` row. US-0096 documents the active-context-handoff operator angle in the narrative subsection above; the canonical key row remains in the release & distribution keys block for byte-stability."
- **Grouped cross-link to main reference list above L1410** for US-0086 `REMOTE_EXECUTION` family (per R-0103 — these keys already live in the main `### Full scratchpad reference (detailed)` list above L1410 pre-US-0113; mirrors US-0114's `AUTO_INSTALL_DEPS`/`AUTO_RELEASE_NOTES` grouped cross-link pattern). Cross-link wording: "For `REMOTE_EXECUTION` / `REMOTE_CONFIG` / `AUTO_REMOTE_AUTOMATION_PROFILE` / `AUTO_REMOTE_ENVIRONMENT_LABEL`, see the main reference list above (US-0086 family — pre-US-0113 reference surface)."
- **Reason-code-only entries** (no scratchpad key blocks — always-on publish/QA guards):
  - **US-0084**: `INSTALL_MANIFEST_ERROR` reason code (also surfaced by US-0062/US-0041 per R-0102 § AC-3 reference extension). Note: "US-0084 has no dedicated scratchpad key block — its normative surface is runbook-anchored (`### Published npm installer.sh / POSIX dash (US-0084)` L1441 + `### Automated checks (US-0084)` L1459) + the shared `INSTALL_MANIFEST_ERROR` reason code."
  - **US-0093**: `SCRATCHPAD_HEADER_DRIFT`, `BACKLOG_STATUS_DRIFT` reason codes. Note: "US-0093 has no dedicated scratchpad key block — its normative surface is runbook-anchored (`### Browser UAT self-test (US-0093)` L1999) + the `SCRATCHPAD_HEADER_DRIFT` / `BACKLOG_STATUS_DRIFT` reason codes."
- **No duplicate key rows**: each key appears in exactly one canonical location (US-0113's block for sovereign-loop keys; US-0114's block for release & distribution keys + `DELIVERY_MODE` overlap; US-0115's block for integration & observability net-new keys + cross-link pointers + reason-code-only entries).
- **Default-off / zero-overhead-when-off wording** per AC-3 — mirrors the `.cursor/scratchpad.md` `# Default-off` pattern for optional features; always-on framing for publish/QA guards.

**Verification step**:
- `its_magic/README.md` `### Full scratchpad reference (detailed)` section contains a new `### Integration & observability keys (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` sub-block as a sibling to (after) US-0114's `### Release & distribution keys` block (L1551).
- The sub-block documents US-0034's `CROSS_REPO_OBSERVABILITY` / `COMPATIBILITY_GATE_ON_CRITICAL` / `COMPATIBILITY_SOURCES` with defaults + flip guidance.
- The sub-block documents US-0096's `LEAN_MEMORY_READ` / `LEAN_MEMORY_WRITE` / `LEAN_COLD_READ_MAX_SECTIONS` / `LEAN_STATE_INDEX_ROWS` / `AUTO_DELIVERY_ROUTING` with defaults + flip guidance (the 5 net-new key rows).
- The sub-block documents US-0101's `MODEL_TIER_DEFAULT` / `MODEL_CATALOG` / `MODEL_RESOLVE` / `MODEL_FALLBACK` / `MODEL_PROVIDER_MODE` with defaults + flip guidance (the 5 net-new key rows).
- The sub-block documents US-0102's `MODEL_SLUG_<PHASE_ID>` with the composition-on-US-0101 note.
- The sub-block contains a cross-link pointer to US-0114's `### Release & distribution keys` block for the canonical `DELIVERY_MODE` row (US-0096 overlap) — `DELIVERY_MODE` is NOT re-documented in US-0115's block (no duplicate row).
- The sub-block contains a grouped cross-link to the main reference list above L1410 for US-0086's `REMOTE_EXECUTION` family — those 4 keys are NOT re-documented in US-0115's block (no duplicate rows).
- The sub-block contains reason-code-only entries for US-0084 (`INSTALL_MANIFEST_ERROR`) and US-0093 (`SCRATCHPAD_HEADER_DRIFT`, `BACKLOG_STATUS_DRIFT`) — no scratchpad key rows for these two features (always-on guards).
- US-0113's `### Sovereign-loop era keys` block (L1427) is byte-stable — none of its rows are modified, reordered, or removed.
- US-0114's `### Release & distribution keys` block (L1551) is byte-stable — none of its rows are modified, reordered, or removed.
- Each net-new key row contains default-off / zero-overhead-when-off wording (for optional features) or always-on framing (for publish/QA guards).
- No duplicate key rows exist among US-0113's, US-0114's, and US-0115's blocks.
- `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1551 range (no removals/modifications to US-0113's L1427 or US-0114's L1551 blocks).

---

### T-004: Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md`

**Coverage**: AC-5
**Risk**: MEDIUM (parity lockstep — highest risk in this sprint)
**Dependencies**: T-001, T-002, T-003 (all `its_magic/README.md` edits complete first)
**Files to touch**:
- `template/its_magic/README.md` (one-way copy from `its_magic/README.md`)

**Scope**:
- One-way copy: `its_magic/README.md` → `template/its_magic/README.md` (byte-identical).
- Re-run parity gates:
  - `python -c "a=open(r'its_magic/README.md','rb').read(); b=open(r'template/its_magic/README.md','rb').read(); print('PARITY_OK' if a==b else 'PARITY_DIFF')"` → expect **`PARITY_OK`**.
  - `python scripts/check_intake_template_parity.py` → expect **`[INTAKE_TEMPLATE_PARITY_OK]`** (exit 0).

**Verification step**:
- `python -c "a=open(r'its_magic/README.md','rb').read(); b=open(r'template/its_magic/README.md','rb').read(); print('PARITY_OK' if a==b else 'PARITY_DIFF')"` reports `PARITY_OK`.
- `python scripts/check_intake_template_parity.py` emits `[INTAKE_TEMPLATE_PARITY_OK]` (exit 0).
- `template/its_magic/README.md` is byte-identical to `its_magic/README.md`.

**Note**: QA within `build+verify` must re-verify both parity gates (highest-risk mitigation per architecture).

---

### T-005: Run validators and fix any drift

**Coverage**: AC-4, AC-6
**Risk**: LOW (catalog) / MEDIUM (encoding prerequisite)
**Dependencies**: T-004 (template synced before validator runs)
**Files to touch**:
- `its_magic/README.md` and `template/its_magic/README.md` (only if drift requires prose fix; re-sync after any fix per T-004)

**Scope**:
- Run coverage validator:
  - `python scripts/validate_readme_feature_coverage.py --enforce` → expect `[README_FEATURE_COVERAGE_VALIDATE_OK]` with `coverage_missing=["US-0117"]` **unchanged** (US-0117 pre-existing gap; DC-1 + DC-2 + DC-3 out-of-scope). Catalog block L63 + US-0113/US-0114 narrative blocks treated as read-only.
  - **Encoding hygiene prerequisite:** working-tree `docs/product/backlog.md` has 185 stray `0xa7` bytes (Windows-1252 corruption flagged in R-0102 + R-0103 + architecture) that break this validator's strict UTF-8 read — orchestrator must restore encoding hygiene before execute so this gate can re-pass post-execute.
- Run audience + metadata validators:
  - `python scripts/validate_doc_profile.py` → expect PASS.
  - `python scripts/check-user-visible-metadata.py` → expect PASS.
- **Fix any drift**: if any validator fails, fix the narrative prose. **Convention**: reuse existing `(US-xxxx)` parenthetical-tag pattern; avoid `DEC-xxxx`/`R-xxxx`/reason-code families in narrative sentences. US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. If a prose fix is applied to `its_magic/README.md`, re-run T-004 one-way copy to re-sync `template/its_magic/README.md`.

**Verification step**:
- `python scripts/validate_readme_feature_coverage.py --enforce` emits `[README_FEATURE_COVERAGE_VALIDATE_OK]` (exit 0) with `coverage_missing=["US-0117"]` unchanged.
- `python scripts/validate_doc_profile.py` emits PASS (exit 0).
- `python scripts/check-user-visible-metadata.py` emits PASS (exit 0).
- No narrative prose leaks internal IDs (DEC-xxxx/R-xxxx/reason-codes) into user-visible sentences; US-IDs appear only in parenthetical catalog tags `(US-xxxx)`.
- If any prose fix was applied, `template/its_magic/README.md` re-synced and both parity gates re-confirmed green.

---

### T-006: Run regression tests and confirm green

**Coverage**: AC-8
**Risk**: LOW–MEDIUM (forbid test weakenings)
**Dependencies**: T-005 (all prose finalized before regression confirmation)
**Files to touch**: None (regression tests are read-only gates)

**Scope**:
- Run regression tests:
  - `python -m pytest tests/scratchpad_example_parity_test.py -q` → expect **4 passed**.
- **No test weakenings**: US-0115 does NOT modify `.cursor/scratchpad.md` or `template/.cursor/scratchpad.local.example.md`, so the scratchpad parity tests remain green by construction. **If a test fails, the prose is wrong, not the test** — fix prose (re-run T-005), never relax the test.

**Verification step**:
- `python -m pytest tests/scratchpad_example_parity_test.py -q` reports 4 passed (exit 0).
- No edits to `tests/scratchpad_example_parity_test.py`, `.cursor/scratchpad.md`, or `template/.cursor/scratchpad.local.example.md` (forbid test weakenings).
- If a test failed and prose was fixed, the fix is documented and the test re-run green without modification.

---

## Appendix: Task Dependencies (Visual)

```
T-001 (umbrella section)
    ↓
T-002 (7 per-feature subsections)
    ↓
T-003 (scratchpad ref extension — net-new + cross-links + reason-code-only)
    ↓
T-004 (template byte-sync)
    ↓
T-005 (validators)
    ↓
T-006 (regression tests)
```

---

**Task Execution Order**: T-001 → T-002 → T-003 → T-004 → T-005 → T-006
