# Sprint S0117 — Tasks (US-0117)

**sprint_id**: S0117
**story_refs**: US-0117
**dec_ref**: none (companion_dec=none; US-0117 documentation-only)
**architecture_ref**: `docs/engineering/architecture.md#US-0117` (h1 section appended in architecture phase; approach_locked=A1) + 36 `## US-xxxx` DC anchor stubs appended below the US-0117 section (L1568–L1708)
**research_ref**: `docs/engineering/research.md` `R-0105`
**task_count**: 7 (T-anch + T-001..T-006)
**within_limit**: true (7 ≤ `SPRINT_MAX_TASKS=12`)
**coverage**: AC-1..AC-8 surjective via T-001..T-006 + DC resolution verified via T-anch (8 ACs, 7 tasks; multi-AC tasks T-002 (AC-2+AC-7), T-005 (AC-4+AC-6); T-anch = NO-OP / verification for DC resolution)

---

## Task-to-AC Bijection Table

| Task ID | Title | ACs Satisfied |
|---------|-------|---------------|
| T-anch | **NO-OP / verification** — confirm 36 `## US-xxxx` h1 anchors + `## US-0117` section already exist in `docs/engineering/architecture.md` (added in `/architecture` phase per R-0105 Q-2 LOCKED) | DC resolution (AC-2 / AC-8 indirect) |
| T-001 | Add `### Phase & role governance (US-0069 / ... / US-0090) umbrella section` under `## Commands and workflow` | AC-1 |
| T-002 | Add 18 per-feature `#### US-xxxx` operator subsections nested under umbrella (US-0069 → US-0090; cross-link + narrative + runbook cross-links; 2 labeling corrections + 1 US-id collision LOCKED) | AC-2, AC-7 |
| T-003 | Extend `### Full scratchpad reference (detailed)` with `### Phase & role governance keys (US-0069 / ... / US-0090)` sub-block (46 net-new key rows + cross-link pointers + 9 reason-code-only entries + 7 prose-only / runbook-cross-link-only entries) | AC-3 |
| T-004 | Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md` | AC-5 |
| T-005 | Run validators (`validate_readme_feature_coverage.py --enforce`, `validate_doc_profile.py`, `check-user-visible-metadata.py`, `check_intake_template_parity.py`) and fix any drift | AC-4, AC-6 |
| T-006 | Run regression tests (`pytest tests/scratchpad_example_parity_test.py -v`); confirm green | AC-8 |

**Total**: 7 tasks covering 8 ACs (surjective) + DC resolution (T-anch NO-OP / verification).

---

## Task Seeds

### T-anch: NO-OP / verification — confirm 36 `## US-xxxx` h1 anchors + `## US-0117` section already exist in `docs/engineering/architecture.md`

**Coverage**: DC resolution (AC-2 / AC-8 indirect)
**Risk**: LOW
**Dependencies**: None (anchors already added in `/architecture` phase)
**Files to touch**: None (NO-OP / verification task — no execute-phase write to `docs/engineering/architecture.md`)

**Scope**:
- **VERIFY** (do NOT write) that the following 36 `## US-xxxx` h1 anchors + the `## US-0117` section already exist in `docs/engineering/architecture.md` (added in the `/architecture` phase per R-0105 Q-2 LOCKED — "resolve in `/architecture`, NOT `/execute`"):
  - **18 own** (US-0117 family): `## US-0069`, `## US-0070`, `## US-0071`, `## US-0072`, `## US-0075`, `## US-0076`, `## US-0077`, `## US-0078`, `## US-0079`, `## US-0080`, `## US-0081`, `## US-0082`, `## US-0083`, `## US-0085`, `## US-0087`, `## US-0088`, `## US-0089`, `## US-0090`.
  - **18 deferred**: DC-1 (5, from US-0113): `## US-0103`, `## US-0104`, `## US-0105`, `## US-0107`, `## US-0110`; DC-2 (2, from US-0114): `## US-0041`, `## US-0062`; DC-3 (7, from US-0115): `## US-0034`, `## US-0084`, `## US-0086`, `## US-0093`, `## US-0096`, `## US-0101`, `## US-0102`; DC-4 (4, from US-0116): `## US-0092`, `## US-0095`, `## US-0098`, `## US-0099`.
  - Plus the `## US-0117 — Phase & role governance operator documentation in framework README` section itself.
- Confirm `git diff HEAD -- docs/engineering/architecture.md` shows no execute-phase edits to architecture.md (any architecture-phase append was already committed at `/architecture` time; T-anch does NOT add to it).
- Record the verification result (anchor count = 36 + `## US-0117` section; pure-addition confirmation); no new write performed.

**Verification step**:
- `rg -c '^## US-' docs/engineering/architecture.md` returns the expected count (36 DC anchors + the `## US-0117` section + prior `## US-0115` / `## US-0116` sections + other historical anchors — verify the 36 expected anchor IDs are present: US-0069/0070/0071/0072/0075/0076/0077/0078/0079/0080/0081/0082/0083/0085/0087/0088/0089/0090 + US-0103/0104/0105/0107/0110 + US-0041/0062 + US-0034/0084/0086/0093/0096/0101/0102 + US-0092/0095/0098/0099).
- `git diff HEAD -- docs/engineering/architecture.md` shows no execute-phase edits (T-anch is NO-OP — the architecture-phase append is already in HEAD or staged from `/architecture`; T-anch does not modify architecture.md).

---

### T-001: Add `### Phase & role governance (US-0069 / ... / US-0090) umbrella section`

**Coverage**: AC-1
**Risk**: LOW
**Dependencies**: T-anch (verification first — keeps the README byte-stability surface clean for T-001..T-004)
**Files to touch**:
- `its_magic/README.md` (append new `### Phase & role governance (US-0069 / US-0070 / US-0071 / US-0072 / US-0075 / US-0076 / US-0077 / US-0078 / US-0079 / US-0080 / US-0081 / US-0082 / US-0083 / US-0085 / US-0087 / US-0088 / US-0089 / US-0090) umbrella section` under `## Commands and workflow` (L350), placed **immediately after** the closing of the US-0116 delivery & lifecycle umbrella block (which ends before L1665 `### Full scratchpad reference (detailed)`), keeping the five family umbrellas visually adjacent as siblings in release order: US-0113 sovereign-loop era (L940) → US-0114 release & distribution (L1225) → US-0115 integration & observability (L1410) → US-0116 delivery & lifecycle (L1665) → US-0117 phase & role governance — 5th sibling, first 5-cumulative-surface story, LARGEST family in the 5-story drain)

**Scope**:
- Add `### Phase & role governance (US-0069 / US-0070 / US-0071 / US-0072 / US-0075 / US-0076 / US-0077 / US-0078 / US-0079 / US-0080 / US-0081 / US-0082 / US-0083 / US-0085 / US-0087 / US-0088 / US-0089 / US-0090) umbrella section` umbrella section containing:
  - **"Phase governance integration" introductory framing (AC-1)** — explicit statement that this umbrella closes the operator-documentation gap for the phase & role governance family (the 5th and final family in the 5-story drain) and that the "phase governance integration" concept lives at this umbrella level (NOT a separate `#### US-0090` subsection — US-0090 = Caveman input compression per R-0105 + architecture lock).
  - **Default-off posture callout (optional runtime features)** — explicit statement that optional runtime features in this family (e.g., US-0087 full-autonomy mode via `AUTO_FLOW_MODE=full_autonomy`, US-0088 automation modes via `AUTO_BACKLOG_DRAIN` / `AUTO_EXECUTE_BULK`, US-0081 caveman mode via `CAVEMAN_MODE`, US-0090 caveman input compression via `CAVEMAN_COMPRESS_INPUT`) are opt-in with default-off; disabled features impose zero overhead.
  - **18-step recommended enable order** — US-id-ascending dependency chain: `US-0069` (phase→role matrix) → `US-0070` (phase selection policy) → `US-0071` (metadata sanitization — validator gate, always on) → `US-0072` (context slimming — concept; toggle is `TOKEN_PROFILE` owned by US-0080) → `US-0075` (scratchpad example-first refresh — install-time) → `US-0076` (codebase map freshness gate) → `US-0077` (delegation policy — validator) → `US-0078` (env file bootstrap — install-time) → `US-0079` (bug queue routing) → `US-0080` (auto quiet mode) → `US-0081` (caveman mode) → `US-0082` (codebase map bootstrap) → `US-0083` (scratchpad delivery keys) → `US-0085` (context fresh-context markers — isolation-evidence contract) → `US-0087` (full-autonomy mode) → `US-0088` (automation modes) → `US-0089` (auto orchestration) → `US-0090` (caveman input compression). Order rationale: phase-role governance + phase selection first → sanitization + slimming + example-first + codebase map + delegation + env file + bug queue + quiet mode + caveman voice + codebase map bootstrap + delivery keys + fresh-context markers + full-autonomy + automation modes + auto orchestration + caveman input compression last.
  - **Runbook pointer line** — single cross-link to phase & role governance runbook sections (existing anchors only; no content duplication). Per-feature anchors in each subsection below.
  - **Zero-overhead-when-off contract paragraph** — mirrors the `.cursor/scratchpad.md` `# Default-off` pattern: disabled optional runtime features incur no runtime cost, no artifact emission, no side effects. Validator-gate features (US-0071 metadata sanitization, US-0077 delegation policy, US-0085 fresh-context markers) are always-on (zero runtime cost — they are static validators).

**Verification step**:
- `its_magic/README.md` contains a `### Phase & role governance (US-0069 / US-0070 / US-0071 / US-0072 / US-0075 / US-0076 / US-0077 / US-0078 / US-0079 / US-0080 / US-0081 / US-0082 / US-0083 / US-0085 / US-0087 / US-0088 / US-0089 / US-0090) umbrella section` heading under `## Commands and workflow` and after the US-0116 delivery & lifecycle umbrella block (i.e., before `### Full scratchpad reference (detailed)` at L1665).
- The umbrella section names all 18 in-scope features (US-0069..US-0090) at least once.
- The umbrella section contains the 18-step recommended enable order with all 18 features listed in US-id-ascending order.
- The umbrella section contains a default-off posture callout (for optional runtime features) and a "phase governance integration" introductory framing (AC-1) and a zero-overhead-when-off contract paragraph.
- The umbrella section contains a runbook cross-link (existing anchor; no new runbook content added to `docs/engineering/runbook.md`).

---

### T-002: Add 18 per-feature `#### US-xxxx` operator subsections nested under the umbrella

**Coverage**: AC-2, AC-7
**Risk**: MEDIUM (18-subsection scope size — 2–4× prior stories' T-002 load; 2 labeling corrections + 1 US-id collision LOCKED)
**Dependencies**: T-001 (umbrella section must exist first to nest under)
**Files to touch**:
- `its_magic/README.md` (add 18 `#### US-xxxx` subsections nested under the T-001 umbrella, ordered **US-id-ascending** (deterministic — matches catalog one-liner order): US-0069 → US-0070 → US-0071 → US-0072 → US-0075 → US-0076 → US-0077 → US-0078 → US-0079 → US-0080 → US-0081 → US-0082 → US-0083 → US-0085 → US-0087 → US-0088 → US-0089 → US-0090)

**Scope**:
- Add 18 per-feature `#### US-xxxx` operator subsections. Each subsection contains:
  - **1–3 sentence narrative** — what the feature does (phase & role governance angle), grounded in the backlog row + scratchpad keys + runbook anchor.
  - **Master enable flag + related keys with defaults** (where applicable — see per-feature shape from R-0105 § Per-feature sub-findings).
  - **Zero-overhead-when-off wording** (for optional runtime features) OR **always-on validator framing** (for US-0071 / US-0077 / US-0085) OR **bootstrap-on-install framing** (for US-0075 / US-0078) — mirrors `.cursor/scratchpad.md` `# Default-off` pattern.
  - **Runbook cross-link** — existing anchor only (AC-7 forbids duplication). All 18 cross-link targets already exist (R-0105 verified):
    - US-0069 → `## Strict /auto phase→role enforcement (US-0069 / DEC-0051)` (runbook L1711, h2).
    - US-0070 → `## Configurable /auto phase plan (US-0070 / DEC-0052)` (runbook L1753, h2).
    - US-0071 → `## User-visible internal metadata guard (US-0071 / DEC-0053)` (runbook L303, h2).
    - US-0072 → `## Context compaction and token profile mode (US-0053 / DEC-0035)` (runbook L550, h2 — shared with US-0080).
    - US-0075 → `### Scratchpad example parity` (runbook L1949, h3) + `## Scratchpad example upgrade contract (US-0057 / DEC-0039 / DEC-0057)` (runbook L2535, h2).
    - US-0076 → `## Codebase map bootstrap (US-0082 / DEC-0065)` (runbook L63, h2 — shared with US-0082).
    - US-0077 → `## Documentation profile validation (US-0077 / DEC-0059)` (runbook L98, h2).
    - US-0078 → `## Interactive intake evidence validation (US-0078 / DEC-0060 / US-0083 / DEC-0067)` (runbook L479, h2 — shared with US-0083).
    - US-0079 → `## Bug issues (US-0079 / DEC-0061)` (runbook L512, h2).
    - US-0080 → `## Context compaction and token profile mode (US-0053 / DEC-0035)` (runbook L550, h2 — shared with US-0072) + `### Auto quiet mode` (runbook L570, h3).
    - US-0081 → `### Caveman mode (US-0089)` (runbook L2032, h3 — note: runbook h2 US-id collides with US-0089 in the 18-feature family; US-0081 owns the caveman voice/level narrative; US-0089 owns auto orchestration — `/architecture` LOCKS the resolution; see US-0089 below).
    - US-0082 → `## Codebase map bootstrap (US-0082 / DEC-0065)` (runbook L63, h2 — shared with US-0076; **label correction: US-0082 = "Codebase map" per runbook L63 + DEC-0065; spec handoff's "Input compression" is a mislabel**).
    - US-0083 → `## Interactive intake evidence validation (US-0078 / DEC-0060 / US-0083 / DEC-0067)` (runbook L479, h2 — shared with US-0078) + `### Scratchpad delivery keys` (runbook L591, h3).
    - US-0085 → `## Per-phase subagent isolation evidence (US-0048 / DEC-0029)` (runbook L1628, h2).
    - US-0087 → `## Targeted bug auto drain (US-0087)` (runbook L1809, h2) + `### Full-autonomy outer driver (US-0092) — fallback` (runbook L1958, h3 — cross-link to US-0092 for the outer-driver fallback angle; US-0087 owns the full-autonomy mode + hard caps narrative; US-0092 owns the security-posture + outer-driver fallback — US-0092 in US-0116's family, already released, cross-link only).
    - US-0088 → `## Continuous /auto + backlog drain (US-0088)` (runbook L1838, h2).
    - US-0089 → `### Manual vs automation routing (US-0086)` (runbook L1398, h3 — parent h2 covering remote execution / automation routing; US-0089 owns auto-orchestration; US-0086 owns manual-vs-automation routing — in US-0115's family, already released, cross-link only) + secondary anchor `## Continuous /auto + backlog drain (US-0088)` (runbook L1838, h2 — `AUTO_PAUSE_REQUEST` table at L1873). **US-id collision resolution LOCKED: `#### US-0089` subsection title = "Auto orchestration" (NOT "Caveman mode"; per scratchpad L21/L135 + 18-feature family; runbook h2 `## Caveman mode (US-0089)` L2032 is the collision — `/architecture` locks the resolution)**.
    - US-0090 → `### Caveman input compression (US-0090)` (runbook L2099, h3 — parent h2 = `## Caveman mode (US-0089)` L2032; **label correction: US-0090 = "Caveman input compression" per runbook L2099 + DEC-0073; spec handoff's "Phase governance integration" is a mislabel — "phase governance integration" is the umbrella's introductory framing AC-1, not a separate `#### US-0090` subsection**).

- **Per-feature narrative shape (R-0105 grounded)**: see R-0105 § Per-feature sub-findings (18 sub-sections, one per feature) for the authoritative narrative angle + key surface + runbook anchor + risk notes per feature. Key boundaries:
  - **US-0081 / US-0090 / US-0089 three-way angle boundary**: US-0081 owns `CAVEMAN_MODE` / `CAVEMAN_LEVEL` (voice); US-0090 owns `CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE` (input compression); US-0089 owns `AUTO_PAUSE_REQUEST` / `AUTO_REMOTE_AUTOMATION_PROFILE` (auto orchestration — NOT caveman mode).
  - **US-0072 / US-0080 / US-0115 three-way angle boundary**: US-0072 = context-slimming concept (prose-only + cross-link to US-0080 for `TOKEN_PROFILE` runtime toggle + cross-link to US-0115 L1878 for `LEAN_MEMORY_*` mechanics, default omit); US-0080 = `AUTO_QUIET` runtime toggle + `TOKEN_PROFILE` runtime toggle (DEC-0035); US-0115 (already released) owns `LEAN_MEMORY_*` family mechanics.
  - **US-0076 / US-0082 same-umbrella angle boundary**: US-0076 = codebase-map freshness gate (prose-only + cross-link to US-0082 for `CODEBASE_MAP_REFRESH_ON_ROLLOVER` toggle); US-0082 = codebase-map bootstrap mechanism (owns `CODEBASE_MAP_REFRESH_ON_ROLLOVER`).
  - **US-0078 / US-0083 same-umbrella angle boundary**: US-0078 = env file bootstrap harness (prose-only); US-0083 = scratchpad delivery keys extension (owns `AUTO_DELIVERY_ROUTING` + cross-link to US-0114 for `DELIVERY_MODE` + `DELIVERY_MODE_SWITCH_MID_STORY` reason code).
  - **US-0087 / US-0088 / US-0092 / US-0116 angle boundary**: US-0087 owns canonical key rows for `AUTO_FLOW_MODE` / `AUTO_IMPLEMENTATION_LOOP` / `AUTO_LOOP_MAX_CYCLES` / `AUTO_BLOCK_RETRY_MAX` / `CROSS_MODEL_REVIEW` family / `SOVEREIGN_MEMORY` family / `AUTO_SOVEREIGN` family / `SOVEREIGN_GOAL_MODE` / `RELEASE_PUBLISH_MODE` (18 net-new keys — largest in family); US-0088 owns `AUTO_BACKLOG_DRAIN` / `AUTO_BACKLOG_MAX_STORIES` / `AUTO_BACKLOG_ON_BLOCK` / `AUTO_STORY_SELECTION` / `AUTO_EXECUTE_BULK` / `AUTO_EXECUTE_MAX_ITEMS` / `AUTO_EXECUTE_ON_BLOCK` / `AUTO_EXECUTE_SELECTION` / `AUTO_TEAM_SCOPE_ENFORCE` (9 net-new keys); US-0092 (US-0116 family, already released) is cross-link only.

**Verification step**:
- `its_magic/README.md` contains exactly 18 `#### US-xxxx` subsections nested under the `### Phase & role governance (...) umbrella section`.
- Subsection order is US-id-ascending: US-0069, US-0070, US-0071, US-0072, US-0075, US-0076, US-0077, US-0078, US-0079, US-0080, US-0081, US-0082, US-0083, US-0085, US-0087, US-0088, US-0089, US-0090.
- `#### US-0082` subsection title = "Codebase map" (NOT "Input compression") — labeling correction applied.
- `#### US-0090` subsection title = "Caveman input compression" (NOT "Phase governance integration") — labeling correction applied.
- `#### US-0089` subsection title = "Auto orchestration" (NOT "Caveman mode") — US-id collision resolution applied.
- Each optional-runtime-feature subsection contains the master enable flag(s) with default value(s) + a zero-overhead-when-off statement.
- Each validator-gate subsection (US-0071 / US-0077 / US-0085) contains always-on validator framing.
- Each bootstrap-on-install subsection (US-0075 / US-0078) contains bootstrap-on-install framing.
- Each subsection contains a runbook cross-link to an existing anchor (no new runbook content added to `docs/engineering/runbook.md`).
- No runbook content is duplicated in the README (AC-7).

---

### T-003: Extend `### Full scratchpad reference (detailed)` with `### Phase & role governance keys` sub-block

**Coverage**: AC-3
**Risk**: MEDIUM (5th-story cumulative byte-stability surface — first 5-cumulative-surface story — highest risk in this sprint)
**Dependencies**: T-002 (per-feature subsections complete first to keep narrative+reference ordering coherent)
**Files to touch**:
- `its_magic/README.md` (extend the `### Full scratchpad reference (detailed)` section, L1665, with a `### Phase & role governance keys (US-0069 / US-0070 / US-0071 / US-0072 / US-0075 / US-0076 / US-0077 / US-0078 / US-0079 / US-0080 / US-0081 / US-0082 / US-0083 / US-0085 / US-0087 / US-0088 / US-0089 / US-0090)` sub-block as a sibling to (after) US-0116's `### Delivery & lifecycle keys` block (L2225); before `### Remote execution config`)

**Scope**:
- Append `### Phase & role governance keys (US-0069 / ... / US-0090)` sub-block as a sibling to (after) US-0116's `### Delivery & lifecycle keys` block (L2225) under `### Full scratchpad reference (detailed)` (L1665). 5th sibling sub-block in release order: US-0113 L1682 → US-0114 L1806 → US-0115 L1878 → US-0116 L2225 → US-0117 new (first 5-cumulative-surface story).
- **46 net-new key rows** (top-level scratchpad keys documented in the 5th sub-block — architecture lock; preserve US-0113 L1682 + US-0114 L1806 + US-0115 L1878 + US-0116 L2225 byte-stability, no duplicate rows):
  - **US-0069** (3 keys): `AUTO_ROLE_RESEARCH`, `AUTO_ROLE_PLAN_VERIFY`, `AUTO_ROLE_REFRESH_CONTEXT`.
  - **US-0070** (4 keys): `AUTO_PHASE_PLAN`, `AUTO_PHASE_EXCLUDE`, `AUTO_PHASE_INCLUDE`, `AUTO_PHASE_PROFILE`.
  - **US-0079** (4 keys): `AUTO_BUG_QUEUE`, `AUTO_BUG_TARGET`, `AUTO_BUG_MAX_ITEMS`, `AUTO_BUG_ON_BLOCK`.
  - **US-0080** (1 key): `AUTO_QUIET`.
  - **US-0081** (2 keys): `CAVEMAN_MODE`, `CAVEMAN_LEVEL`.
  - **US-0083** (1 key): `AUTO_DELIVERY_ROUTING` (note: `DELIVERY_MODE` is cross-link to US-0114 — NOT re-documented here).
  - **US-0087** (18 keys): `AUTO_FLOW_MODE`, `AUTO_IMPLEMENTATION_LOOP`, `AUTO_LOOP_MAX_CYCLES`, `AUTO_BLOCK_RETRY_MAX`, `RELEASE_PUBLISH_MODE`, `CROSS_MODEL_REVIEW`, `CROSS_MODEL_ANTISLOP_THRESHOLD`, `CROSS_MODEL_REWORK_MAX`, `SOVEREIGN_MEMORY`, `SOVEREIGN_MEMORY_TOP_N`, `SOVEREIGN_MEMORY_TOP_K`, `SOVEREIGN_MEMORY_MAX_CHARS`, `SOVEREIGN_MEMORY_JSONL_MAX_LINES`, `AUTO_SOVEREIGN`, `AUTO_SOVEREIGN_DEFERRAL_MAX`, `AUTO_SOVEREIGN_DRAIN_GENERATE_MAX`, `AUTO_SOVEREIGN_DEFERRAL_POLICY`, `SOVEREIGN_GOAL_MODE`.
  - **US-0088** (9 keys): `AUTO_BACKLOG_DRAIN`, `AUTO_BACKLOG_MAX_STORIES`, `AUTO_BACKLOG_ON_BLOCK`, `AUTO_STORY_SELECTION`, `AUTO_EXECUTE_BULK`, `AUTO_EXECUTE_MAX_ITEMS`, `AUTO_EXECUTE_ON_BLOCK`, `AUTO_EXECUTE_SELECTION`, `AUTO_TEAM_SCOPE_ENFORCE`.
  - **US-0089** (2 keys): `AUTO_PAUSE_REQUEST`, `AUTO_REMOTE_AUTOMATION_PROFILE`.
  - **US-0090** (2 keys): `CAVEMAN_COMPRESS_INPUT`, `CAVEMAN_FILE_SCOPE`.
  - **Total**: 46 keys across 10 features.
- **9 reason-code-only entries** (no scratchpad key block — install-time only or validator-only; mirrors US-0114's `INSTALL_MANIFEST_ERROR` and US-0115's `SCRATCHPAD_HEADER_DRIFT` / `BACKLOG_STATUS_DRIFT` reason-code-only pattern):
  - **US-0070**: `PHASE_POLICY_CONFLICT`, `PHASE_PLAN_UNKNOWN_PHASE`.
  - **US-0077**: `INTAKE_DELEGATION_EVIDENCE_MISSING`.
  - **US-0081**: `CAVEMAN_LEVEL_UNKNOWN`.
  - **US-0083**: `DELIVERY_MODE_SWITCH_MID_STORY`.
  - **US-0085**: `PHASE_CONTEXT_ISOLATION_MISSING`.
  - **US-0087**: `BLOCK_RETRY_CAP_EXHAUSTED`, `NATIVE_CHAIN_UNAVAILABLE`.
  - (US-0090: `CAVEMAN_COMPRESS_SCOPE_EMPTY` — counted within US-0090 prose; reason-code-only entry.)
- **7 prose-only / runbook-cross-link-only entries** (no key row — validator-gate or concept features):
  - **US-0071** (Metadata sanitization): prose-only; cross-link to `## User-visible internal metadata guard (US-0071 / DEC-0053)` runbook L303.
  - **US-0072** (Context slimming): prose-only + cross-link pointer to US-0080 subsection (same umbrella) for `TOKEN_PROFILE` runtime toggle + cross-link pointer to US-0115's `### Integration & observability keys` block (L1878) for `LEAN_MEMORY_*` family (default omit — angle-distinct).
  - **US-0075** (Scratchpad example-first refresh): prose-only; cross-link to runbook L1949 + L2535.
  - **US-0076** (Codebase map freshness gate): prose-only + cross-link pointer to US-0082 subsection (same umbrella) for `CODEBASE_MAP_REFRESH_ON_ROLLOVER` toggle + cross-link to runbook L63.
  - **US-0077** (Delegation policy): prose-only; cross-link to runbook L98.
  - **US-0078** (Env file bootstrap): prose-only; cross-link to runbook L479 (shared with US-0083).
  - **US-0085** (Context fresh-context markers): prose-only; cross-link to runbook L1628.
- **Cross-link pointers** (no duplicate key rows):
  - **`DELIVERY_MODE`** (US-0083) → cross-link pointer to US-0114's `### Release & distribution keys` block (L1806) which owns the canonical `DELIVERY_MODE` row (byte-stability preserved).
  - **`LEAN_MEMORY_*` family** (optional, US-0087/US-0072 angle) → cross-link pointer to US-0115's `### Integration & observability keys` block (L1878) which owns the canonical `LEAN_MEMORY_*` family rows per US-0096/DEC-0082. Default omit (angle-distinct per R-0105 — US-0087 owns full-autonomy mode; US-0115 owns memory-layer mechanics).
  - **`TOKEN_PROFILE`** (US-0072 / US-0080) → grouped cross-link to main reference list above L1665 + US-0080 subsection (same umbrella — US-0080 owns the `TOKEN_PROFILE` runtime toggle narrative).
  - **`CODEBASE_MAP_REFRESH_ON_ROLLOVER`** (US-0076 / US-0082) → cross-link to US-0082 subsection (same umbrella — US-0082 owns the bootstrap-mechanism narrative).
- **No key block for US-0071 / US-0072 / US-0075 / US-0076 / US-0077 / US-0078 / US-0085** (prose-only / runbook-cross-link-only entries — confirmed via scratchpad grep in R-0105).
- **Default-off / zero-overhead-when-off wording** per AC-3 — mirrors the `.cursor/scratchpad.md` `# Default-off` pattern for optional runtime features; always-on validator framing for US-0071 / US-0077 / US-0085; bootstrap-on-install framing for US-0075 / US-0078.

**Verification step**:
- `its_magic/README.md` `### Full scratchpad reference (detailed)` section contains a new `### Phase & role governance keys (US-0069 / ... / US-0090)` sub-block as a sibling to (after) US-0116's `### Delivery & lifecycle keys` block (L2225) and before `### Remote execution config`.
- The sub-block documents 46 net-new key rows across 10 features (US-0069/0070/0079/0080/0081/0083/0087/0088/0089/0090) with defaults + flip guidance.
- The sub-block contains 9 reason-code-only entries (7 features).
- The sub-block contains 7 prose-only / runbook-cross-link-only entries (US-0071/0072/0075/0076/0077/0078/0085) — no key rows for these features.
- The sub-block contains a cross-link pointer to US-0114's `### Release & distribution keys` block for the canonical `DELIVERY_MODE` row (US-0083 overlap) — `DELIVERY_MODE` is NOT re-documented in US-0117's block.
- The sub-block optionally contains a cross-link pointer to US-0115's `### Integration & observability keys` block for the `LEAN_MEMORY_*` family overlap (default omit — angle-distinct per R-0105).
- The sub-block contains a grouped cross-link pointer to the main reference list above + US-0080 subsection for `TOKEN_PROFILE` (US-0072 overlap) — `TOKEN_PROFILE` is NOT re-documented as a net-new row in US-0117's block (it lives in the main reference list).
- The sub-block contains a cross-link pointer to US-0082 subsection for `CODEBASE_MAP_REFRESH_ON_ROLLOVER` (US-0076 overlap) — `CODEBASE_MAP_REFRESH_ON_ROLLOVER` is NOT re-documented as a net-new row in US-0117's block (it lives in US-0082's narrative).
- US-0113's `### Sovereign-loop era keys` block (L1682) is byte-stable — none of its rows are modified, reordered, or removed.
- US-0114's `### Release & distribution keys` block (L1806) is byte-stable — none of its rows are modified, reordered, or removed.
- US-0115's `### Integration & observability keys` block (L1878) is byte-stable — none of its rows are modified, reordered, or removed.
- US-0116's `### Delivery & lifecycle keys` block (L2225) is byte-stable — none of its rows are modified, reordered, or removed.
- Each net-new key row contains default-off / zero-overhead-when-off wording (for optional runtime features) or always-on validator framing (for US-0071/0077/0085) or bootstrap-on-install framing (for US-0075/0078).
- No duplicate key rows exist among US-0113's, US-0114's, US-0115's, US-0116's, and US-0117's blocks.
- `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2225 range (no removals/modifications to US-0113's L1682, US-0114's L1806, US-0115's L1878, or US-0116's L2225 blocks).

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
  - `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → expect `[README_FEATURE_COVERAGE_VALIDATE_OK]` (exit 0) with `coverage_missing=["US-0117"]` baseline (US-0117 not in catalog surface — unchanged from baseline). Catalog block L63 + US-0113/US-0114/US-0115/US-0116 narrative blocks treated as read-only.
  - **Encoding hygiene prerequisite:** working-tree `docs/product/backlog.md` has 185 stray `0xa7` bytes (Windows-1252 corruption flagged in R-0102 + R-0103 + R-0104 + R-0105 + architecture) that break this validator's strict UTF-8 read — orchestrator must restore encoding hygiene before execute so this gate can re-pass post-execute. **NOT a US-0117 blocker.**
- Run audience + metadata validators:
  - `python scripts/validate_doc_profile.py --repo .` → expect PASS.
  - `python scripts/check-user-visible-metadata.py --repo .` → expect PASS.
- Run intake template parity:
  - `python scripts/check_intake_template_parity.py --repo .` → expect `[INTAKE_TEMPLATE_PARITY_OK] scope=intake` (exit 0).
- **Fix any drift**: if any validator fails, fix the narrative prose. **Convention**: reuse existing `(US-xxxx)` parenthetical-tag pattern; avoid `DEC-xxxx`/`R-xxxx`/reason-code families in narrative sentences. US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. If a prose fix is applied to `its_magic/README.md`, re-run T-004 one-way copy to re-sync `template/its_magic/README.md`.

**Verification step**:
- `python scripts/validate_readme_feature_coverage.py --repo . --enforce` emits `[README_FEATURE_COVERAGE_VALIDATE_OK]` (exit 0) with `coverage_missing=["US-0117"]` baseline.
- `python scripts/validate_doc_profile.py --repo .` emits PASS (exit 0).
- `python scripts/check-user-visible-metadata.py --repo .` emits PASS (exit 0).
- `python scripts/check_intake_template_parity.py --repo .` emits `[INTAKE_TEMPLATE_PARITY_OK] scope=intake` (exit 0).
- No narrative prose leaks internal IDs (DEC-xxxx/R-xxxx/reason-codes) into user-visible sentences; US-IDs appear only in parenthetical catalog tags `(US-xxxx)`.
- If any prose fix was applied, `template/its_magic/README.md` re-synced and both parity gates re-confirmed green.

---

### T-006: Run regression tests and confirm green

**Coverage**: AC-8
**Risk**: LOW–MEDIUM (forbid test weakenings — 5th-story cumulative surface)
**Dependencies**: T-005 (all prose finalized before regression confirmation)
**Files to touch**: None (regression tests are read-only gates)

**Scope**:
- Run regression tests:
  - `python -m pytest tests/scratchpad_example_parity_test.py -v` → expect **4 passed**.
- **No test weakenings**: US-0117 does NOT modify `.cursor/scratchpad.md` or `template/.cursor/scratchpad.local.example.md`, so the scratchpad parity tests remain green by construction. **If a test fails, the prose is wrong, not the test** — fix prose (re-run T-005), never relax the test.

**Verification step**:
- `python -m pytest tests/scratchpad_example_parity_test.py -v` reports 4 passed (exit 0).
- No edits to `tests/scratchpad_example_parity_test.py`, `.cursor/scratchpad.md`, or `template/.cursor/scratchpad.local.example.md` (forbid test weakenings).
- If a test failed and prose was fixed, the fix is documented and the test re-run green without modification.

---

## Appendix: Task Dependencies (Visual)

```
T-anch (NO-OP / verify 36 anchors exist in architecture.md)
    ↓
T-001 (umbrella section)
    ↓
T-002 (18 per-feature subsections)
    ↓
T-003 (scratchpad ref extension — 46 net-new + 9 reason-code + 7 prose-only + cross-links)
    ↓
T-004 (template byte-sync)
    ↓
T-005 (validators)
    ↓
T-006 (regression tests)
```

---

**Task Execution Order**: T-anch → T-001 → T-002 → T-003 → T-004 → T-005 → T-006
