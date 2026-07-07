# Sprint S0116 — Tasks (US-0116)

**sprint_id**: S0116
**story_refs**: US-0116
**dec_ref**: none (companion_dec=none; US-0116 documentation-only)
**architecture_ref**: `docs/engineering/architecture.md#US-0116` (h1 section appended in architecture phase; approach_locked=A1)
**research_ref**: `docs/engineering/research.md` `R-0104`
**task_count**: 6
**within_limit**: true (6 ≤ `SPRINT_MAX_TASKS=12`)
**coverage**: AC-1..AC-8 surjective via T-001..T-006 (8 ACs, 6 tasks; multi-AC tasks T-002 (AC-2+AC-7), T-005 (AC-4+AC-6))

---

## Task-to-AC Bijection Table

| Task ID | Title | ACs Satisfied |
|---------|-------|---------------|
| T-001 | Add `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` under `## Commands and workflow` | AC-1 |
| T-002 | Add 4 per-feature `#### US-xxxx` operator subsections nested under umbrella (US-0092 → US-0095 → US-0098 → US-0099; cross-link + narrative + runbook cross-links) | AC-2, AC-7 |
| T-003 | Extend `### Full scratchpad reference (detailed)` with `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` sub-block (true net-new keys + cross-link pointers + reason-code-only entries) | AC-3 |
| T-004 | Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md` | AC-5 |
| T-005 | Run validators (`validate_readme_feature_coverage.py --enforce`, `validate_doc_profile.py`, `check-user-visible-metadata.py`) and fix any drift | AC-4, AC-6 |
| T-006 | Run regression tests (`pytest tests/scratchpad_example_parity_test.py -q`); confirm green | AC-8 |

**Total**: 6 tasks covering 8 ACs (surjective).

---

## Task Seeds

### T-001: Add `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section`

**Coverage**: AC-1
**Risk**: LOW
**Dependencies**: None
**Files to touch**:
- `its_magic/README.md` (append new `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` under `## Commands and workflow` (L350), placed **immediately after** the closing of the US-0115 integration & observability umbrella block (which ends before L1665 `### Full scratchpad reference (detailed)`), keeping the four family umbrellas visually adjacent as siblings in release order: US-0113 sovereign-loop era (L940) → US-0114 release & distribution (L1225) → US-0115 integration & observability (L1410) → US-0116 delivery & lifecycle — 4th sibling, first 4-cumulative-surface story)

**Scope**:
- Add `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` umbrella section containing:
  - **Default-off posture callout (optional runtime features)** — explicit statement that optional runtime features (US-0092 full-autonomy outer driver + US-0095 native in-chat auto-chain) are opt-in via `AUTO_FLOW_MODE=full_autonomy` (default `manual`), and US-0098 dev environment auto-launch is opt-in via `DEV_AUTO_LAUNCH_PROFILE` (default `off`). Disabled features impose zero overhead.
  - **Bootstrap-on-install framing (US-0099)** — US-0099 is install-time only (runs on `missing` / `upgrade` / npm `postinstall`); zero runtime cost. Frame as "automatic at install time" rather than "enable to turn on".
  - **4-step recommended enable order** — dependency chain: `US-0099` (install-time bootstrap baseline) → `US-0098` (execute-phase auto-launch layered on bootstrap baseline) → `US-0095` (native in-chat auto-chain primary) → `US-0092` (outer-driver fallback for headless/CI or `NATIVE_CHAIN_UNAVAILABLE`). Order rationale: install-time baseline first → runtime auto-launch layered on top → primary IDE recipe → optional fallback last.
  - **Runbook pointer line** — single cross-link to delivery & lifecycle runbook sections (existing anchors only; no content duplication). Per-feature anchors in each subsection below.
  - **Zero-overhead-when-off contract paragraph** — mirrors the `.cursor/scratchpad.md` `# Default-off` pattern: disabled optional runtime features incur no runtime cost, no artifact emission, no side effects. US-0099 bootstrap runs only at install/upgrade/postinstall — zero runtime cost.

**Verification step**:
- `its_magic/README.md` contains a `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` heading under `## Commands and workflow` and after the US-0115 integration & observability umbrella block (i.e., before `### Full scratchpad reference (detailed)` at L1665).
- The umbrella section names all 4 in-scope features (US-0092/US-0095/US-0098/US-0099) at least once.
- The umbrella section contains the 4-step recommended enable order with all 4 features listed in order (US-0099 → US-0098 → US-0095 → US-0092).
- The umbrella section contains a default-off posture callout (for optional runtime features) and a bootstrap-on-install framing note (for US-0099) and a zero-overhead-when-off contract paragraph.
- The umbrella section contains a runbook cross-link (existing anchor; no new runbook content added to `docs/engineering/runbook.md`).

---

### T-002: Add 4 per-feature `#### US-xxxx` operator subsections nested under the umbrella

**Coverage**: AC-2, AC-7
**Risk**: LOW–MEDIUM (US-0092/US-0095 angle overlap + US-0098/US-0099 angle boundary)
**Dependencies**: T-001 (umbrella section must exist first to nest under)
**Files to touch**:
- `its_magic/README.md` (add 4 `#### US-xxxx` subsections nested under the T-001 umbrella, ordered **US-id-ascending** (deterministic — matches catalog one-liner order): US-0092 → US-0095 → US-0098 → US-0099)

**Scope**:
- Add 4 per-feature `#### US-xxxx` operator subsections. Each subsection contains:
  - **1–3 sentence narrative** — what the feature does (delivery & lifecycle angle), grounded in the backlog row + scratchpad keys + runbook anchor.
  - **Master enable flag + related keys with defaults** (where applicable — see per-feature shape below).
  - **Zero-overhead-when-off wording** (for optional runtime features) OR **bootstrap-on-install framing** (for US-0099) — mirrors `.cursor/scratchpad.md` `# Default-off` pattern.
  - **Runbook cross-link** — existing anchor only (AC-7 forbids duplication). All 4 cross-link targets already exist (R-0104 verified):
    - US-0092 → `### Full-autonomy outer driver (US-0092) — fallback` (runbook L1958, h3, parent h2 = `## Auto continuation resume contract` L1587) + secondary pointer to `#### Security (US-0092 / DEC-0078)` (L1989, h4 under the L1958 h3).
    - US-0095 → `### Native in-chat auto-chain (US-0095)` (runbook L1900, h3, parent h2 = `## Auto continuation resume contract` L1587).
    - US-0098 → `## Dev environment auto-launch (US-0098 / DEC-0084)` (runbook L244, h2 — top-level runbook section).
    - US-0099 → `## Dev environment auto-launch (US-0098 / DEC-0084)` (runbook L244, parent h2) with secondary pointers to L250 (`**Install-time bootstrap (US-0099):**` paragraph inside the L244 h2) and L301 (normative contract anchor `# US-0098` / `# US-0099` (bootstrap posture)).

- **Per-feature narrative shape (R-0104 grounded)**:
  - **US-0092 — Full-autonomy outer driver + security posture**: opt-in `AUTO_FLOW_MODE=full_autonomy` (default-off per US-0092 / DEC-0078) enables the shipped stdlib outer driver as **optional** / **fallback** for headless/CI or when the native in-chat chain (US-0095) is unavailable. The driver loops hook invocations; it never performs phase-role work (spawn-only). Security posture (DEC-0078): no auto-read `.env`/secret paths; no intake evidence mutation under automation; no publish without explicit `RELEASE_PUBLISH_MODE=auto` opt-in (default-off); block-retry ledger is names-only. Hard caps: `AUTO_LOOP_MAX_CYCLES` (loop safety guard, default `5`), `AUTO_BACKLOG_MAX_STORIES` (drain cap, default `10`), `AUTO_BLOCK_RETRY_MAX` (default `3`). Relationship to native in-chat chain: US-0095 primary (IDE); US-0092 fallback (headless/CI or `NATIVE_CHAIN_UNAVAILABLE`). Grouped cross-link pointer to the main reference list for `AUTO_FLOW_MODE` / `ALLOW_AUTO_PUSH` / `AUTO_PUSH_BRANCH_ALLOWLIST` / `AUTO_LOOP_MAX_CYCLES` / `AUTO_BACKLOG_MAX_STORIES` (no duplicate rows in the delivery & lifecycle keys sub-block — these keys are already in `### Automation modes` L880 + `### Sync policy (US-0038)` L909 + `### Optional /auto backlog-drain mode (US-0044)` L2370 + main reference list). Runbook cross-link to L1958 + L1989.
  - **US-0095 — Native in-chat auto-chain**: primary IDE recipe for hands-off delivery when `AUTO_FLOW_MODE=full_autonomy` (default-off): run `/auto` once in Cursor — orchestrator self-chains in-chat across phases and drain segments via foreground sequential Task loop in the same `/auto` orchestrator session. Distinct from US-0092 (outer-driver fallback): US-0095 is **primary** in the Cursor IDE; US-0092 is **optional fallback** for headless/CI or when the native chain is unavailable (`NATIVE_CHAIN_UNAVAILABLE`). Compose-on-US-0044: `AUTO_BACKLOG_DRAIN=1` enables drain (cross-link pointer to `### Optional /auto backlog-drain mode (US-0044)` README section L2370 — grouped cross-link, no duplicate rows). Drain-advance suppression: `AUTO_QUIET=1`. `AUTO_IMPLEMENTATION_LOOP` + `AUTO_PAUSE_REQUEST` / `AUTO_PAUSE_POLICY` interaction (grouped cross-link to main reference list — no duplicate rows). Native chain vs outer-driver fallback routing table (mirrors runbook L1921–L1926). Optional `LEAN_MEMORY_*` cross-link to US-0115's `### Integration & observability keys` block (L1878) — default omit (angle-distinct per R-0104 open question #2; auto-chain drain angle owned by US-0044's `AUTO_BACKLOG_DRAIN` family; lean-memory angle owned by US-0096/US-0115); add only a brief single-sentence pointer if the composition narrative is essential ("composes with `LEAN_MEMORY_*` family documented in `### Integration & observability keys` above"). Runbook cross-link to L1900.
  - **US-0098 — Dev environment auto-launch**: execute-phase bounded rebuild/relaunch of dev stacks plus Connect surfacing after implementation changes. Default-off scratchpad gate (`DEV_AUTO_LAUNCH_PROFILE=off|deterministic_v1`, default `off`; zero-overhead-when-off). `DEV_ENVIRONMENT_CONFIG=repo-relative path` (default `.cursor/dev-environment.json`). Orthogonality to US-0065 phase QA / US-0086 test routing / US-0067 release hints / `AUTO_REMOTE_AUTOMATION_PROFILE` (remote execution) is explicit (runbook L247–L248). Detection precedence: US-0086 remote wins over docker-host-local per DEC-0084 §3. Compose-with-US-0099 (install-time bootstrap baseline → US-0098 auto-launch layered on top). `DEV_ENV_*` reason-code family pointer (profile/relaunch families — runbook L280–L286; reason-code-only entries, no scratchpad key rows for these — they live in the runbook). Runbook cross-link to L244.
  - **US-0099 — Dev-environment copy-when-missing bootstrap**: install-time bootstrap on `missing` / `upgrade` / npm `postinstall`: copies `template/.cursor/dev-environment.json.example` → resolved profile path (`.cursor/dev-environment.json` by default) **only when the target file is absent** — never overwrites operator-customized profiles. Customize-after-bootstrap contract. `DEV_ENV_BOOTSTRAP_*` reason-code family (5 codes — net-new reason-code-only entries in the delivery & lifecycle keys sub-block). `DEV_ENV_PROFILE_MISSING` remediation (re-run install/upgrade or `python scripts/dev_environment_lib.py --bootstrap --target <repo>` then customize). Compose-with-US-0098 (bootstrap baseline → US-0098 auto-launch layered on top). Runbook cross-link to L244 (parent h2) with secondary pointers to L250 (the bootstrap paragraph) and L301 (normative contract anchor `# US-0098` / `# US-0099` (bootstrap posture)).

- **US-0092/US-0095 angle boundary (R-002 / R3)**: Both share `AUTO_FLOW_MODE=full_autonomy` opt-in. Primary/fallback boundary table mirrors runbook L1921–L1926 (US-0095 primary IDE; US-0092 fallback headless/CI or `NATIVE_CHAIN_UNAVAILABLE`). Angle-distinct narrative contract — US-0095 owns process angle (orchestrator self-chain mechanism); US-0092 owns security posture + outer-driver fallback.
- **US-0098/US-0099 angle boundary (R-004 / R4)**: Both share the `## Dev environment auto-launch (US-0098 / DEC-0084)` h2 at runbook L244. US-0098 = execute-phase runtime gate (default-off `DEV_AUTO_LAUNCH_PROFILE`); US-0099 = install-time bootstrap (copy-when-missing, runs only on `missing` / `upgrade` / `postinstall`). Distinct narrative angles — no overlap.

**Verification step**:
- `its_magic/README.md` contains exactly 4 `#### US-xxxx` subsections nested under the `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section`.
- Subsection order is US-id-ascending: US-0092, US-0095, US-0098, US-0099.
- US-0092 subsection narrates the full-autonomy outer driver + DEC-0078 security posture + hard caps + native-chain-vs-outer-driver routing (US-0095 primary, US-0092 fallback) + grouped cross-link to main reference list + runbook cross-link to L1958 + L1989.
- US-0095 subsection narrates the native in-chat auto-chain primary + compose-on-US-0044 + drain-advance suppression + grouped cross-link to main reference list + optional `LEAN_MEMORY_*` cross-link to US-0115 L1878 (default omit) + runbook cross-link to L1900.
- US-0098 subsection narrates `DEV_AUTO_LAUNCH_PROFILE` default-off + `DEV_ENVIRONMENT_CONFIG` path + orthogonality + DEC-0084 §3 detection precedence + compose-with-US-0099 + runbook cross-link to L244.
- US-0099 subsection narrates install-time copy-when-missing bootstrap + customize-after-bootstrap contract + `DEV_ENV_BOOTSTRAP_*` reason-code family (5 codes) + `DEV_ENV_PROFILE_MISSING` remediation + compose-with-US-0098 + runbook cross-link to L244/L250/L301.
- Each optional-runtime-feature subsection (US-0092/US-0095/US-0098) contains the master enable flag(s) with default value(s) + a zero-overhead-when-off statement.
- US-0099 subsection contains bootstrap-on-install framing (install-time only, zero runtime cost).
- Each subsection contains a runbook cross-link to an existing anchor (no new runbook content added to `docs/engineering/runbook.md`).
- No runbook content is duplicated in the README (AC-7).

---

### T-003: Extend `### Full scratchpad reference (detailed)` with `### Delivery & lifecycle keys` sub-block

**Coverage**: AC-3
**Risk**: MEDIUM (4th-story cumulative byte-stability surface — first 4-cumulative-surface story — highest risk in this sprint)
**Dependencies**: T-002 (per-feature subsections complete first to keep narrative+reference ordering coherent)
**Files to touch**:
- `its_magic/README.md` (extend the `### Full scratchpad reference (detailed)` section, L1665, with a `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` sub-block as a sibling to (after) US-0115's `### Integration & observability keys` block at L1878; before L2026 `### Remote execution config` — confirmed insertion point in R-0104)

**Scope**:
- Append `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` sub-block as a sibling to (after) US-0115's `### Integration & observability keys` block (L1878) under `### Full scratchpad reference (detailed)` (L1665). 4th sibling sub-block in release order: US-0113 L1682 → US-0114 L1806 → US-0115 L1878 → US-0116 new (first 4-cumulative-surface story).
- **True net-new key rows ONLY** (architecture lock — preserve US-0113 L1682 + US-0114 L1806 + US-0115 L1878 byte-stability, no duplicate rows):
  - **US-0098 net-new keys** (from `.cursor/scratchpad.md` L295–298): `DEV_AUTO_LAUNCH_PROFILE=off|deterministic_v1` (default `off`; zero-overhead-when-off), `DEV_ENVIRONMENT_CONFIG=repo-relative path` (default `.cursor/dev-environment.json`). Document defaults + flip guidance. **These are the ONLY true net-new scratchpad key rows** in the delivery & lifecycle keys sub-block — confirmed via grep (no pre-US-0116 README documentation of these keys per R-0104).
- **Reason-code-only entries** (no scratchpad key block — install-time only, distinct from runtime opt-in toggles owned by US-0098; mirrors US-0114's `INSTALL_MANIFEST_ERROR` and US-0115's `SCRATCHPAD_HEADER_DRIFT` / `BACKLOG_STATUS_DRIFT` reason-code-only pattern):
  - **US-0099 reason codes** (5 codes — from runbook L276–L282; confirmed NOT in any pre-US-0116 README section per R-0104 grep): `DEV_ENV_BOOTSTRAP_COPIED`, `DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`, `DEV_ENV_BOOTSTRAP_PATH_INVALID`, `DEV_ENV_BOOTSTRAP_SOURCE_MISSING`, `DEV_ENV_PROFILE_MISSING`. Note: "US-0099 has no dedicated scratchpad key block — its normative surface is runbook-anchored (`## Dev environment auto-launch (US-0098 / DEC-0084)` L244 § Install-time bootstrap (US-0099) L250 + normative contract anchor L301) + the `DEV_ENV_BOOTSTRAP_*` reason-code family + `DEV_ENV_PROFILE_MISSING`."
- **Grouped cross-link pointers** (overlap keys — byte-stability; no duplicate rows):
  - **`AUTO_FLOW_MODE` / `AUTO_IMPLEMENTATION_LOOP` / `AUTO_PAUSE_REQUEST` / `AUTO_PAUSE_POLICY` / `AUTO_LOOP_MAX_CYCLES` / `AUTO_BACKLOG_MAX_STORIES`** (US-0092/US-0095) → grouped cross-link pointer to the main reference list above (these keys pre-date US-0113/US-0114/US-0115 and are already in the main `### Automation modes` block at L880 and the main `### Full scratchpad reference (detailed)` list). Mirrors US-0114's `AUTO_INSTALL_DEPS`/`AUTO_RELEASE_NOTES` grouped cross-link pattern and US-0115's `REMOTE_EXECUTION` family grouped cross-link pattern. **`AUTO_LOOP_MAX_CYCLES` / `AUTO_BACKLOG_MAX_STORIES` are exact key names** (verified via scratchpad per R-0104 open question #8); both are already in the main reference list — grouped cross-link only, no net-new rows.
  - **`ALLOW_AUTO_PUSH` / `AUTO_PUSH_BRANCH_ALLOWLIST`** (US-0092 security posture) → grouped cross-link pointer to the main `### Sync policy (US-0038)` block (L909) and the main reference list above (these keys pre-date US-0113 and are already documented there). No net-new rows.
  - **`AUTO_BACKLOG_DRAIN` / `AUTO_BUG_QUEUE` / `AUTO_BACKLOG_MAX_STORIES` / `AUTO_STORY_SELECTION` / `AUTO_BACKLOG_ON_BLOCK` / `AUTO_BUG_TARGET` / `AUTO_BUG_MAX_ITEMS` / `AUTO_BUG_ON_BLOCK`** (US-0092/US-0095 compose-on-US-0044/US-0087/US-0088) → grouped cross-link pointer to the `### Optional /auto backlog-drain mode (US-0044)` README section (L2370) and the US-0087/US-0088 catalog one-liners (L2261/L2263). **NOT a cross-link to US-0113's `### Sovereign-loop era keys` block** (L1682) — those keys are NOT there (confirmed in R-0104 open question #1).
  - **`DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES`** (US-0096/US-0114 + US-0041/US-0062 overlap) → cross-link pointer to US-0114's `### Release & distribution keys` block (L1806) which owns these rows. Cross-link wording: "See `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` above for the canonical `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` rows. US-0116 documents the auto-chain lifecycle-shape / enablement angle in the narrative subsections above; the canonical key rows remain in the release & distribution keys block for byte-stability."
  - **`LEAN_MEMORY_READ` / `LEAN_MEMORY_WRITE` / `LEAN_COLD_READ_MAX_SECTIONS` / `LEAN_STATE_INDEX_ROWS` / `AUTO_DELIVERY_ROUTING`** (US-0096/US-0115 overlap) → optional cross-link pointer to US-0115's `### Integration & observability keys` block (L1878) which owns the canonical `LEAN_MEMORY_*` family rows per US-0096/DEC-0082. **Default omit** (angle-distinct per R-0104 open question #2 — US-0095 is angle-distinct from US-0096's `LEAN_MEMORY_*` family: process angle vs memory angle). If US-0095's subsection narrative references lean-memory composition, add a brief single-sentence pointer ("composes with `LEAN_MEMORY_*` family documented in `### Integration & observability keys` above") — no key row duplication.
- **No key block for US-0092 / US-0095 (true scratchpad key rows)**: US-0092/US-0095's scratchpad keys (`AUTO_FLOW_MODE`, `AUTO_IMPLEMENTATION_LOOP`, `AUTO_PAUSE_*`, `AUTO_LOOP_MAX_CYCLES`, `AUTO_BACKLOG_MAX_STORIES`, `ALLOW_AUTO_PUSH`, `AUTO_PUSH_BRANCH_ALLOWLIST`, `AUTO_BACKLOG_DRAIN`, `AUTO_BUG_QUEUE`, etc.) are ALL already documented in pre-US-0116 README surfaces. Per byte-stability contract, US-0116's `### Delivery & lifecycle keys` sub-block adds **grouped cross-link pointers** to these pre-US-0116 surfaces (no duplicate key rows). The ONLY true net-new key rows in the delivery & lifecycle keys sub-block are US-0098's `DEV_AUTO_LAUNCH_PROFILE` / `DEV_ENVIRONMENT_CONFIG` (2 keys) + US-0099's reason-code-only entries (5 reason codes).
- **Default-off / zero-overhead-when-off wording** per AC-3 — mirrors the `.cursor/scratchpad.md` `# Default-off` pattern for optional runtime features (US-0092/US-0095/US-0098); bootstrap-on-install framing for US-0099 (install-time only, zero runtime cost).

**Verification step**:
- `its_magic/README.md` `### Full scratchpad reference (detailed)` section contains a new `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` sub-block as a sibling to (after) US-0115's `### Integration & observability keys` block (L1878) and before L2026 `### Remote execution config`.
- The sub-block documents US-0098's `DEV_AUTO_LAUNCH_PROFILE` / `DEV_ENVIRONMENT_CONFIG` with defaults + flip guidance (the 2 true net-new key rows).
- The sub-block contains reason-code-only entries for US-0099 (5 codes: `DEV_ENV_BOOTSTRAP_COPIED`, `DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`, `DEV_ENV_BOOTSTRAP_PATH_INVALID`, `DEV_ENV_BOOTSTRAP_SOURCE_MISSING`, `DEV_ENV_PROFILE_MISSING`) — no scratchpad key rows for US-0099 (install-time only).
- The sub-block contains a grouped cross-link pointer to the main reference list above for US-0092/US-0095's `AUTO_FLOW_MODE` / `AUTO_IMPLEMENTATION_LOOP` / `AUTO_PAUSE_*` / `AUTO_LOOP_MAX_CYCLES` / `AUTO_BACKLOG_MAX_STORIES` / `ALLOW_AUTO_PUSH` / `AUTO_PUSH_BRANCH_ALLOWLIST` — those keys are NOT re-documented in US-0116's block (no duplicate rows).
- The sub-block contains a grouped cross-link pointer to `### Optional /auto backlog-drain mode (US-0044)` (L2370) + US-0087/US-0088 catalog one-liners (L2261/L2263) for `AUTO_BACKLOG_DRAIN` / `AUTO_BUG_QUEUE` family — those keys are NOT re-documented in US-0116's block.
- The sub-block contains a cross-link pointer to US-0114's `### Release & distribution keys` block for the canonical `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` rows (US-0096/US-0114 overlap) — those keys are NOT re-documented in US-0116's block.
- The sub-block optionally contains a cross-link pointer to US-0115's `### Integration & observability keys` block for the `LEAN_MEMORY_*` family overlap (default omit — angle-distinct per R-0104).
- US-0113's `### Sovereign-loop era keys` block (L1682) is byte-stable — none of its rows are modified, reordered, or removed.
- US-0114's `### Release & distribution keys` block (L1806) is byte-stable — none of its rows are modified, reordered, or removed.
- US-0115's `### Integration & observability keys` block (L1878) is byte-stable — none of its rows are modified, reordered, or removed.
- Each net-new key row contains default-off / zero-overhead-when-off wording (for optional runtime features) or bootstrap-on-install framing (for US-0099).
- No duplicate key rows exist among US-0113's, US-0114's, US-0115's, and US-0116's blocks.
- `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1878 range (no removals/modifications to US-0113's L1682, US-0114's L1806, or US-0115's L1878 blocks).

---

### T-004: Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md`

**Coverage**: AC-5
**Risk**: MEDIUM (parity lockstep — highest parity risk in this sprint)
**Dependencies**: T-001, T-002, T-003 (all `its_magic/README.md` edits complete first)
**Files to touch**:
- `template/its_magic/README.md` (one-way copy from `its_magic/README.md`)

**Scope**:
- One-way copy: `its_magic/README.md` → `template/its_magic/README.md` (byte-identical).
- Re-run parity gates:
  - `python -c "a=open(r'its_magic/README.md','rb').read(); b=open(r'template/its_magic/README.md','rb').read(); print('PARITY_OK' if a==b else 'PARITY_DIFF')"` → expect **`PARITY_OK`**.
  - `python scripts/check_intake_template_parity.py` → expect **`[INTAKE_TEMPLATE_PARITY_OK] scope=intake`** (exit 0).

**Verification step**:
- `python -c "a=open(r'its_magic/README.md','rb').read(); b=open(r'template/its_magic/README.md','rb').read(); print('PARITY_OK' if a==b else 'PARITY_DIFF')"` reports `PARITY_OK`.
- `python scripts/check_intake_template_parity.py` emits `[INTAKE_TEMPLATE_PARITY_OK] scope=intake` (exit 0).
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
  - `python scripts/validate_readme_feature_coverage.py --enforce` → expect `[README_FEATURE_COVERAGE_VALIDATE_OK]` (exit 0) with `coverage_missing=[]` baseline (US-0117 not yet OPEN in-scope). Catalog block L63 + US-0113/US-0114/US-0115 narrative blocks treated as read-only.
  - **Encoding hygiene prerequisite:** working-tree `docs/product/backlog.md` has 185 stray `0xa7` bytes (Windows-1252 corruption flagged in R-0102 + R-0103 + R-0104 + architecture) that break this validator's strict UTF-8 read — orchestrator must restore encoding hygiene before execute so this gate can re-pass post-execute. **NOT a US-0116 blocker.**
- Run audience + metadata validators:
  - `python scripts/validate_doc_profile.py` → expect PASS.
  - `python scripts/check-user-visible-metadata.py` → expect PASS.
- **Fix any drift**: if any validator fails, fix the narrative prose. **Convention**: reuse existing `(US-xxxx)` parenthetical-tag pattern; avoid `DEC-xxxx`/`R-xxxx`/reason-code families in narrative sentences. US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. If a prose fix is applied to `its_magic/README.md`, re-run T-004 one-way copy to re-sync `template/its_magic/README.md`.

**Verification step**:
- `python scripts/validate_readme_feature_coverage.py --enforce` emits `[README_FEATURE_COVERAGE_VALIDATE_OK]` (exit 0) with `coverage_missing=[]` baseline.
- `python scripts/validate_doc_profile.py` emits PASS (exit 0).
- `python scripts/check-user-visible-metadata.py` emits PASS (exit 0).
- No narrative prose leaks internal IDs (DEC-xxxx/R-xxxx/reason-codes) into user-visible sentences; US-IDs appear only in parenthetical catalog tags `(US-xxxx)`.
- If any prose fix was applied, `template/its_magic/README.md` re-synced and both parity gates re-confirmed green.

---

### T-006: Run regression tests and confirm green

**Coverage**: AC-8
**Risk**: LOW–MEDIUM (forbid test weakenings — 4th-story cumulative surface)
**Dependencies**: T-005 (all prose finalized before regression confirmation)
**Files to touch**: None (regression tests are read-only gates)

**Scope**:
- Run regression tests:
  - `python -m pytest tests/scratchpad_example_parity_test.py -q` → expect **4 passed**.
- **No test weakenings**: US-0116 does NOT modify `.cursor/scratchpad.md` or `template/.cursor/scratchpad.local.example.md`, so the scratchpad parity tests remain green by construction. **If a test fails, the prose is wrong, not the test** — fix prose (re-run T-005), never relax the test.

**Verification step**:
- `python -m pytest tests/scratchpad_example_parity_test.py -q` reports 4 passed (exit 0).
- No edits to `tests/scratchpad_example_parity_test.py`, `.cursor/scratchpad.md`, or `template/.cursor/scratchpad.local.example.md` (forbid test weakenings).
- If a test failed and prose was fixed, the fix is documented and the test re-run green without modification.

---

## Appendix: Task Dependencies (Visual)

```
T-001 (umbrella section)
    ↓
T-002 (4 per-feature subsections)
    ↓
T-003 (scratchpad ref extension — true net-new + cross-links + reason-code-only)
    ↓
T-004 (template byte-sync)
    ↓
T-005 (validators)
    ↓
T-006 (regression tests)
```

---

**Task Execution Order**: T-001 → T-002 → T-003 → T-004 → T-005 → T-006
