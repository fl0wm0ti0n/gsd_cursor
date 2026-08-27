# Architecture archive pack (2026-08-25)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3000, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 28
- Retained units in hot file: 13
- First archived heading: `## US-0080 — Auto quiet mode`
- Last archived heading: `## US-0118 — Work-kind classification + tiered delivery routing per story`
- Verification tuple (mandatory):
  - archived_body_lines=355
  - preamble_lines=1
  - retained_body_lines=2950

---

## US-0080 — Auto quiet mode

Story US-0080 — Auto quiet mode. `AUTO_QUIET=1` suppresses non-essential stdout; angle-distinct from `TOKEN_PROFILE` (US-0072 / US-0080 shared runbook anchor). See `# US-0117`. Binding: DEC-0035; runbook `## Context compaction and token profile mode (US-0053 / DEC-0035)` L550 h2 + `### Auto quiet mode` L570 h3.

## US-0081 — Caveman mode

Story US-0081 — Caveman mode. `CAVEMAN_MODE=1` / `CAVEMAN_LEVEL=<n>` engages compressed-output operator mode; `CAVEMAN_LEVEL_UNKNOWN` reason code on invalid level. See `# US-0117`. Binding: DEC-0073; runbook `## Caveman mode (US-0089)` L2032 h3 (note: runbook h2 uses US-0089 id colliding with US-0081 family — US-0081 owns the caveman-mode feature; US-0089 owns auto orchestration; `/architecture` locks the resolution).

## US-0082 — Codebase map (bootstrap mechanism)

Story US-0082 — Codebase map bootstrap mechanism. **Label correction**: authoritative label = "Codebase map" (per runbook L63 + DEC-0065; spec handoff's "Input compression" is a mislabel). `CODEBASE_MAP_REFRESH_ON_ROLLOVER=1` (default off) triggers `scripts/materialize_codebase_map.py` on rollover. See `# US-0117` and `## US-0076`. Binding: DEC-0065; runbook `## Codebase map bootstrap (US-0082 / DEC-0065)` L63 h2.

## US-0083 — Scratchpad delivery keys

Story US-0083 — Scratchpad delivery keys. `AUTO_DELIVERY_ROUTING` net-new key + cross-link to US-0114 for `DELIVERY_MODE` + `DELIVERY_MODE_SWITCH_MID_STORY` reason code. See `# US-0117` and `## US-0078`. Binding: DEC-0067 / DEC-0060; runbook `## Interactive intake evidence validation (US-0078 / DEC-0060 / US-0083 / DEC-0067)` L479 h2 + `### Scratchpad delivery keys` L591 h3.

## US-0085 — Context fresh-context markers

Story US-0085 — Context fresh-context markers. `fresh_context_marker` is an isolation-evidence field (not a runtime toggle); `PHASE_CONTEXT_ISOLATION_MISSING` reason code on missing marker. See `# US-0117`. Binding: DEC-0029; runbook `## Phase-context isolation (US-0048 / DEC-0029)` L1628 h2.

## US-0087 — Full-autonomy mode

Story US-0087 — Full-autonomy mode. 18 net-new key rows (largest in family): `AUTO_FLOW_MODE` / `AUTO_IMPLEMENTATION_LOOP` / `AUTO_LOOP_MAX_CYCLES` / `AUTO_BLOCK_RETRY_MAX` / `RELEASE_PUBLISH_MODE` / `CROSS_MODEL_REVIEW` / `CROSS_MODEL_ANTISLOP_THRESHOLD` / `CROSS_MODEL_REWORK_MAX` / `SOVEREIGN_MEMORY` + family (5) / `AUTO_SOVEREIGN` + family (4) / `SOVEREIGN_GOAL_MODE` + `BLOCK_RETRY_CAP_EXHAUSTED` / `NATIVE_CHAIN_UNAVAILABLE` reason codes. See `# US-0117`. Binding: DEC-0078; runbook `## Full-autonomy mode (US-0087 / DEC-0078)` L1809 h2 + `### Full-autonomy interaction` L1958 h3.

## US-0088 — Automation modes

Story US-0088 — Automation modes. 9 net-new keys: `AUTO_BACKLOG_DRAIN` / `AUTO_BACKLOG_MAX_STORIES` / `AUTO_BACKLOG_ON_BLOCK` / `AUTO_STORY_SELECTION` / `AUTO_EXECUTE_BULK` / `AUTO_EXECUTE_MAX_ITEMS` / `AUTO_EXECUTE_ON_BLOCK` / `AUTO_EXECUTE_SELECTION` / `AUTO_TEAM_SCOPE_ENFORCE` + `BLOCK_RETRY_CAP_EXHAUSTED` reason code. See `# US-0117`. Binding: DEC-0078; runbook `## Automation modes (US-0088)` L1838 h2.

## US-0089 — Auto orchestration

Story US-0089 — Auto orchestration. **US-id collision resolution**: authoritative label = "Auto orchestration" (per scratchpad L21/L135 + 18-feature family; runbook h2 `## Caveman mode (US-0089)` L2032 is a US-id collision — US-0089 in the 18-feature family is Auto orchestration, NOT Caveman mode). 2 net-new keys: `AUTO_PAUSE_REQUEST` / `AUTO_REMOTE_AUTOMATION_PROFILE`. See `# US-0117`. Forward-link **`BUG-0011`** / **`DEC-0077`** (Caveman voice-compression delivery; see `# US-0089` §6 below). Binding: DEC-0078; runbook `### Auto orchestration` L1398 h3 + `## Automation modes (US-0088)` L1838 h2.

## US-0090 — Caveman input compression

Story US-0090 — Caveman input compression. **Label correction**: authoritative label = "Caveman input compression" (per runbook L2099 + DEC-0073; spec handoff's "Phase governance integration" is a mislabel — "phase governance integration" is the umbrella's introductory framing AC-1, not a separate `#### US-0090` subsection). 2 net-new keys: `CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE` + `CAVEMAN_COMPRESS_SCOPE_EMPTY` reason code. See `# US-0117`. Binding: DEC-0073; runbook `### Caveman input compression` L2099 h3. See `# US-0085` for context fresh-context markers.

## US-0103 — Sovereign loop ledger (DC-1, from US-0113)

Story US-0103 — Sovereign loop ledger. Append-only sovereign-loop event log (`sovereign_loop_lib.py` advance/drain-generate/notification); default-off `AUTO_SOVEREIGN` (US-0107) composes on this. See `# US-0113`. Binding: DEC-0103; research R-0089.

## US-0104 — Cross-model critic (DC-1, from US-0113)

Story US-0104 — Cross-model critic. `CROSS_MODEL_REVIEW` / `CROSS_MODEL_ANTISLOP_THRESHOLD` / `CROSS_MODEL_REWORK_MAX` keys; cross-model review dispatch with antislop threshold + bounded rework. See `# US-0113`. Binding: DEC-0104; research R-0092.

## US-0105 — Convergence gate (DC-1, from US-0113)

Story US-0105 — Convergence gate. `evaluate_convergence` five-conjunct gate + `goal_progress` emission; composes on US-0103 ledger. See `# US-0113`. Binding: DEC-0105; research R-0093.

## US-0107 — Sovereign loop mode (DC-1, from US-0113)

Story US-0107 — Sovereign loop mode. Default-off `AUTO_SOVEREIGN` orchestrates sovereign-loop advance/drain-generate/notification; fail-closed goal-mode coupling; deferral JSONL v1 + validator. See `# US-0113`. Binding: DEC-0107; research R-0094.

## US-0110 — Goal-based convergence loops (DC-1, from US-0113)

Story US-0110 — Goal-based convergence loops. Five-conjunct `evaluate_convergence`, `goal_progress` emission, partial-delivery report; composes on US-0103 / US-0105. See `# US-0113`. Binding: DEC-0110; research R-0091.

## US-0041 — Release notes derivation (DC-2, from US-0114)

Story US-0041 — Release notes derivation. Atomic `[Unreleased] -> [semver]` promotion via `release_changelog_lib.promote_unreleased()`; release-trigger-driven changelog derivation. See `# US-0114`. Binding: DEC-0041.

## US-0062 — Sync policy + auto-push allowlist (DC-2, from US-0114)

Story US-0062 — Sync policy + auto-push allowlist. `SYNC_POLICY_MODE=disabled` (DEC-0018 default); `AUTO_PUSH_BRANCH_ALLOWLIST` gated sync; release-publish-mode contract. See `# US-0114`. Binding: DEC-0062 / DEC-0018.

## US-0034 — Cross-repo compatibility observability (DC-3, from US-0115)

Story US-0034 — Cross-repo compatibility observability. Monitored sources, manifest contract boundaries, compatibility signal taxonomy, critical-gate policy (`COMPATIBILITY_GATE_ON_CRITICAL`). Default-off (`CROSS_REPO_OBSERVABILITY=0`). See `# US-0115`. Binding: DEC-0034.

## US-0084 — Codebase map freshness gate (DC-3, from US-0115)

Story US-0084 — Codebase map freshness gate. Freshness gate on `docs/engineering/codebase-map.md`; `CODEBASE_MAP_REFRESH_ON_ROLLOVER` default off. See `# US-0115` and `## US-0082`. Binding: DEC-0065.

## US-0086 — Handoff hygiene validator (DC-3, from US-0115)

Story US-0086 — Handoff hygiene validator. `scripts/check_handoff_hygiene.py` validates handoff files against schema; fail-closed on missing/malformed. See `# US-0115`. Binding: DEC-0086.

# US-0091: README ↔ backlog feature coverage backfill + blocking drift gate

## Overview

**Composes on `# US-0077`** (dual-README audience — **`DEC-0059`**) and **extends the
release doc-gate family** alongside **US-0030** (delta-driven command/flag documentation
gate). Binding decision: **`DEC-0074`**. Composes on **`US-0017`** template drift guard and
**`US-0071`** installer parity surfaces. Release changelog artifacts include
`{semver}-release-notes.md` and **`CHANGELOG.md`** per **`DEC-0085`**.

## Decision linkage

- Decision: **`DEC-0074`**
- Composed: **`US-0030`**, **`DEC-0059`**, **`US-0017`**, **`US-0071`**

# US-0093: Cursor browser-integrated UAT self-test

## Overview

**`US-0093`** closes the execution gap left by **`US-0092`** / **`DEC-0078`**: stdlib
**`scripts/uat_probe_lib.py`** classifies browser steps but Tier 2 agent execution owns
Cursor built-in browser MCP. Binding decision: **`DEC-0079`**. Research anchor:
**`R-0041`**. Composes on **`# US-0092`** / **`DEC-0078`**, **`US-0065`**, **`US-0066`**
— spawn-only (**`BUG-0006`**) unchanged; stdlib never invokes browser MCP directly.

## Agent-browser evidence contract

Normative verify-work / qa / execute subsections require agents to write
**`browser_evidence_refs`** after MCP probes. Scratchpad key **`UAT_BROWSER_PROBE_MODE`**
selects primary path (`cursor` | `http_fallback` | `playwright_fallback`); fail closed on
**`UAT_BROWSER_UNAVAILABLE`** when MCP is missing.

## Decision linkage

- Decision: **`DEC-0079`**
- Composed: **`DEC-0078`**, **`US-0092`**, **`US-0065`**
- Research: **`R-0041`**

## US-0096 — Active context handoff / lean memory (DC-3, from US-0115)

Story US-0096 — Active context handoff. `LEAN_MEMORY_*` family (DEC-0082) for memory-layer mechanics; delivery-mode-aware handoff shape. See `# US-0115`. Binding: DEC-0082.

## US-0101 — Model tier resolution (DC-3, from US-0115)

Story US-0101 — Model tier resolution. Resolves model tier per role + delivery mode; composes on US-0102 catalog. See `# US-0115`. Binding: DEC-0101.

## US-0102 — Role-based model catalog (DC-3, from US-0115)

Story US-0102 — Role-based model catalog. Role-based model catalog presets shipped on install/upgrade (US-0112); `model-catalog.local.example.*.json` framework files. See `# US-0115`. Binding: DEC-0102.

## US-0092 — Delivery confirmation gate / full-autonomy outer driver (DC-4, from US-0116)

Story US-0092 — Delivery confirmation gate. Full-autonomy outer driver + security posture; delivery confirmation gate at end of drain. See `# US-0116`. Binding: DEC-0078.

## US-0095 — Native in-chat auto-chain (DC-4, from US-0116)

Story US-0095 — Native in-chat auto-chain. Native in-chat auto-chain continuation; orchestrator continuation contract. See `# US-0116`. Binding: DEC-0080 / DEC-0081.

## US-0098 — Dev environment auto-launch (DC-4, from US-0116)

Story US-0098 — Dev environment auto-launch. `DEV_AUTO_LAUNCH_PROFILE` / `DEV_ENVIRONMENT_CONFIG` keys; execute-phase runtime gate (default-off). See `# US-0116`. Binding: DEC-0084.

## US-0099 — Dev-environment copy-when-missing bootstrap (DC-4, from US-0116)

Story US-0099 — Dev-environment copy-when-missing bootstrap. Install-time bootstrap (copy-when-missing, runs only on `missing` / `upgrade` / `postinstall`); `DEV_ENV_BOOTSTRAP_*` family + `DEV_ENV_PROFILE_MISSING` reason codes. See `# US-0116`. Binding: DEC-0084.


## US-0118 — Work-kind classification + tiered delivery routing per story

### Overview

**US-0118** is the first **code-bearing** story in the new drain (US-0113..US-0117 were documentation-only). It introduces a deterministic **per-story work-kind classifier** `scripts/work_kind_classify_lib.py:classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope) -> WorkKindClassification` returning `work_kind ∈ {doc, mini, code}` + `recommended_delivery_mode ∈ {standard, ultra_lean, mega_quick}` + `recommended_phase_plan` (list of canonical phase ids) + `rationale` + `evidence_refs` (+ optional `rule_trace` via `--explain`). Gated by a new default-off scratchpad flag `WORK_KIND_ROUTING=0|1` (zero overhead when off — early-return in `/auto` `resolve_delivery_mode` step 0 + `/intake` step 5 skip when `WORK_KIND_ROUTING != "1"`). Backlog rows gain optional `work_kind` + `recommended_delivery_mode` fields set at intake (operator accept/override; recorded in intake evidence bundle per US-0078 / DEC-0060). `/auto` `resolve_delivery_mode` step 0 consumes them when `DELIVERY_MODE`/`AUTO_PHASE_*` are unset (L8 precedence: explicit `DELIVERY_MODE` > explicit `AUTO_PHASE_*` > `WORK_KIND_ROUTING`-derived > current default; `start-from` always wins). `doc` → `[intake, execute, release]`; `mini` → `ultra_lean` or `mega_quick` (US-0096 eligibility); `code` → `standard`. Reuses `scripts/dev_environment_lib.py:classify_touched_files()` (tier A/B/C + `TIER_C_SKIP_PREFIXES`) — import, do not reinvent (Q9 LOCKED). Deterministic pure-stdlib, no LLM, no network, no `.env` reads (Q3 LOCKED). Four `WORK_KIND_*` reason codes (Q2 LOCKED). 12 `test_us0118_*` contract test markers (Q4 LOCKED). New `### Work-kind routing keys (US-0118)` README sub-block (Q5 LOCKED — 6th sibling; README edits happen in `/execute`, NOT here) + new `## Work-kind routing (US-0118)` runbook h2 (Q7 LOCKED). Triple-installer parity (Q10/installer manifest).

**Binding decision**: **companion_dec=DEC-0118** (Required → Accepted; authored in THIS phase). US-0118 introduces a new routing primitive — DEC-0118 locks: (a) the work-kind enumeration decision (`doc`/`mini`/`code` 3-tier; alternatives: 2-tier doc/non-doc collapsed — rejected as too coarse; 4-tier doc/mini/standard/extended — rejected as over-engineered), (b) the L8 precedence chain (explicit operator flags always win; classifier fills only the unset case), (c) the `dev_environment_lib.classify_touched_files` reuse boundary (import, not rewrite — Q9 LOCKED), (d) the zero-overhead-when-off contract (default `WORK_KIND_ROUTING=0`). Mirrors DEC-0082 (US-0096 delivery modes) / DEC-0052 (US-0070 phase selection) precedent. **Research anchor**: **R-0106** (delivered 2026-07-04T20:00:00Z, 10/10 open questions Q1..Q10 closed LOCKED; architecture seeds T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; AC baselines green; risks R1..R8 finalized). **Compose guards (non-negotiable, 23 — UNCHANGED, cumulative across all prior stories — same 23 as US-0117)**: US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062. **Status authority**: **OPEN** per **US-0045** (closure at `/release`).

**Fresh context marker**: `tl-US0118-architecture-20260704T203000Z-fresh`
**Orchestrator run id**: `auto-20260704-01`
**Timestamp**: 2026-07-04T20:30:00Z (UTC)
**Verdict**: PASS
**Next**: `/sprint-plan`


### Companion DEC

**companion_dec = DEC-0118** (Required → Accepted; authored in THIS phase at `decisions/DEC-0118.md`). US-0118 introduces a new routing primitive (per-story work-kind classifier) with a precedence-chain tradeoff (L8: explicit `DELIVERY_MODE` > explicit `AUTO_PHASE_*` > `WORK_KIND_ROUTING`-derived > current default) and a work-kind enumeration tradeoff (`doc`/`mini`/`code` 3-tier vs alternative 2-tier or 4-tier schemes). Mirrors DEC-0082 (US-0096 delivery modes) / DEC-0052 (US-0070 phase selection) precedent: a new routing primitive gets a companion DEC locking the precedence chain + enumeration choice + reuse boundary + zero-overhead-when-off contract. The DC-1+DC-2+DC-3+DC-4 resolution (36 h1 anchors) was already performed in US-0117's `/architecture` phase (final deferred-candidate resolution point) — US-0118 inherits a clean deferral register. See `decisions/DEC-0118.md` for the decision body.

### Approach locked (A1)

**Approach A1** (locked): Single `### Work-kind routing (US-0118)` umbrella section + per-feature subsections + 6th scratchpad ref sub-block `### Work-kind routing keys (US-0118)` as a sibling to the US-0113..US-0117 sub-blocks (US-0113 L2421, US-0114 L2545, US-0115 L2617, US-0116 L2765, US-0117 L2856). US-0118 is the **6th-story cumulative byte-stability surface** — first 6-cumulative-surface story. Prior 5 released blocks (US-0113..US-0117) must remain byte-identical between `its_magic/README.md` and `template/its_magic/README.md`; US-0118 adds net-new-keys-only + cross-link-pointers + reason-code-only entries to its own 6th sub-block, never edits prior released blocks. README edits happen in `/execute` (build+verify macro), NOT here — this phase only PROPOSES the sub-block name + cross-link targets in prose.

| Option | Summary | Verdict |
|--------|---------|---------|
| **A1** | **Single `### Work-kind routing (US-0118)` umbrella + per-feature subsections + 6th scratchpad ref sub-block** (net-new keys + cross-link pointers + reason-code-only) | **Preferred** — matches US-0113 / US-0114 / US-0115 / US-0116 / US-0117 sibling precedent (6th sibling); preserves byte-stability of prior 5 released blocks. |
| A2 (rejected) | Extend `### Delivery & lifecycle keys` (US-0116) sub-block with `WORK_KIND_ROUTING` key. | **Rejected** — breaks US-0116's byte-stability (released block in S0116); Q5 LOCKED rejected this alternative explicitly. |
| A3 (rejected) | 2-tier work-kind enumeration (`doc`/`non-doc`) collapsed; or 4-tier (`doc`/`mini`/`standard`/`extended`). | **Rejected** — 2-tier too coarse (conflates `mini` and `code`); 4-tier over-engineered (no operator demand for `extended`); 3-tier mirrors `dev_environment_lib.classify_touched_files` tier A/B/C precedent. |


### Files to touch

- `scripts/work_kind_classify_lib.py` — **NEW**. Pure-stdlib classifier exposing `classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope) -> WorkKindClassification` dataclass (Q10 LOCKED signature). Implements doc/mini/code rules per L5/L6/L7 + Q1 tie-break (highest tier wins). `--explain` flag emits `rule_trace` (Q3). `--self-test` exits 0 (AC-12). Imports `TIER_C_SKIP_PREFIXES` + `classify_touched_files` from `dev_environment_lib` (Q9 LOCKED import contract — no duplication).
- `scripts/installer.py` (or `/auto` orchestrator) — `resolve_delivery_mode` step 0 minimal hook (early-return when `WORK_KIND_ROUTING != "1"`; precedence clause per L8). T-004.
- `its_magic/README.md` — **NEW** `### Work-kind routing (US-0118)` umbrella section + per-feature subsections + `### Work-kind routing keys (US-0118)` 6th scratchpad ref sub-block (Q5 LOCKED — 6th sibling; net-new keys + cross-link pointers + reason-code-only; never edits prior US-0113..US-0117 blocks). T-007. (Edits happen in `/execute`, NOT here.)
- `template/its_magic/README.md` — one-way byte-sync of `its_magic/README.md`. T-007/T-004.
- `tests/us0118_contract_test.py` (or `tests/work_kind_classify_test.py` per R-0106) — **NEW**. 12 `test_us0118_*` markers (Q4 LOCKED). T-006.
- `docs/engineering/runbook.md` — **NEW** `## Work-kind routing (US-0118)` h2 cross-link section (Q7 LOCKED). Content: `WORK_KIND_ROUTING` flag, L8 precedence, operator recipe (force full lifecycle on `doc` story via `DELIVERY_MODE=standard`), `--explain` usage, four `WORK_KIND_*` reason codes. T-008.
- `template/docs/engineering/runbook.md` — parity one-way copy of runbook h2.
- `.cursor/scratchpad.md` — **NEW** `WORK_KIND_ROUTING=0` key (default off) + `WORK_KIND_*` reason-code family (example scratchpad only — canonical scratchpad edits deferred to `/execute`). T-002.
- `template/.cursor/scratchpad.local.example.md` — mirror of `WORK_KIND_ROUTING` row.
- `.cursor/commands/auto.md` — `resolve_delivery_mode` step-0 precedence clause (L8 chain). T-002/T-004.
- `.cursor/commands/intake.md` — step-5 classifier hook (after ACs drafted, after US-0051 decomposition evaluator, before persistence). T-003.
- `template/.cursor/commands/auto.md` + `template/.cursor/commands/intake.md` — parity one-way copy (when template mirrors commands).
- `handoffs/intake_evidence/*.json` — schema extension: 3 new optional fields `work_kind`, `recommended_delivery_mode`, `work_kind_operator_decision ∈ {accept, override}` (Q9 LOCKED). T-003.
- `installer-owned-paths.manifest` — `[install_include_paths]` rows for `scripts/work_kind_classify_lib.py` + `template/scripts/work_kind_classify_lib.py`. T-009.
- `scripts/check_intake_template_parity.py` — `WORK_KIND_ROUTING_PAIRS` manifest constant + `--scope=work-kind-routing` flag (Q6 LOCKED). T-009.
- `decisions/DEC-0118.md` — **NEW** companion DEC (authored in THIS phase).
- `docs/engineering/architecture.md` — **this `## US-0118` section** (T-anch; authored in THIS phase).

### Files NOT to touch

- `docs/product/backlog.md` — US-0045 status authority; release-only. (US-0118 remains OPEN until `/release`. Backlog row fields `work_kind` / `recommended_delivery_mode` are added per-story at intake time only when `WORK_KIND_ROUTING=1` and operator accepts — this is a schema extension, NOT a bulk edit of existing rows. No forced reclassification of existing rows.)
- `docs/product/acceptance.md` — release-only.
- Prior-released US-0113..US-0117 README blocks (`### Sovereign-loop era` L940 + `### Sovereign-loop era keys` L2421 / `### Release & distribution` L1225 + `### Release & distribution keys` L2545 / `### Integration & observability` L1410 + `### Integration & observability keys` L2617 / `### Delivery & lifecycle` L1665 + `### Delivery & lifecycle keys` L2765 / `### Phase & role governance` + `### Phase & role governance keys` L2856) in `its_magic/README.md` — **byte-stability contract** (all 5 already released in S0113..S0117). US-0118 adds cross-link pointers to these blocks from its own 6th sub-block; it never edits them. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2856 range (no removals/modifications to US-0113's L2421, US-0114's L2545, US-0115's L2617, US-0116's L2765, or US-0117's L2856 blocks).
- `scripts/sovereign_loop_lib.py` — compose-do-not-amend (US-0103 read-only consumer).
- `scripts/sovereign_convergence_lib.py` — compose-do-not-amend (US-0105 read-only consumer).
- `scripts/dev_environment_lib.py` — **REUSE only — do not modify**. Import `classify_touched_files` + `TIER_C_SKIP_PREFIXES` from `dev_environment_lib` (Q9 LOCKED import contract). Contract test `test_us0118_classify_touched_files_reuse` enforces the import boundary.
- `tests/scratchpad_example_parity_test.py` — AC-8 regression baseline; forbid edits.
- Compose-guard stories (23 — US-0091, US-0097, US-0017, US-0040, US-0100..US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062) — read-only consumers; additive-only.


### Sprint seeds (T-anch + T-001..T-009 — 10 tasks within SPRINT_MAX_TASKS=12)

| Task | AC | Description | Role |
|------|----|-------------|------|
| **T-anch** | AC-10 | Add `## US-0118` h1 anchor to `docs/engineering/architecture.md` (per US-0118 h1-anchor policy; mirrors `## US-0113`..`## US-0117` format). Verify compose-do-not-amend: US-0096, US-0070, US-0078, US-0051, US-0069, US-0103 surfaces remain read-only (no edits to their architecture sections). Lock the import contract for `dev_environment_lib.classify_touched_files` reuse (Q9 boundary). | B |
| **T-001** | AC-1 / AC-2 | Create `scripts/work_kind_classify_lib.py` exposing `classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope) -> WorkKindClassification` per Q10 signature. Pure stdlib; import `TIER_C_SKIP_PREFIXES` + `classify_touched_files` from `dev_environment_lib` (no duplication — Q9). Implement the three rules (doc/mini/code) per L5/L6/L7 + Q1 tie-break (highest tier wins). Implement `--explain` flag emitting `rule_trace` (Q3). Implement `--self-test` (AC-12) exiting 0. | B |
| **T-002** | AC-3 / AC-6 | Add `WORK_KIND_ROUTING=0` (default off) to `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` with merge-precedence note (US-0078 model B: local > materialized baseline > example). Document the L8 precedence chain in `.cursor/commands/auto.md` `resolve_delivery_mode` step 0. (README scratchpad reference sub-block `### Work-kind routing keys (US-0118)` is added in T-007, not here.) | B |
| **T-003** | AC-4 / AC-5 | Extend `/intake` step 5 to run the classifier when `WORK_KIND_ROUTING=1` (after ACs drafted, after US-0051 decomposition evaluator, before persistence). Present `work_kind` + `recommended_delivery_mode` to operator for accept/override (Q9). Persist choice in backlog row (`- work_kind`, `- recommended_delivery_mode`) + intake evidence bundle (`work_kind`, `recommended_delivery_mode`, `work_kind_operator_decision`). US-0078 evidence gate still runs before any backlog/acceptance write. | B |
| **T-004** | AC-6 | `/auto` `resolve_delivery_mode` step-0 integration: add precedence clause to `.cursor/commands/auto.md`: when `WORK_KIND_ROUTING=1` AND backlog row carries `work_kind` AND `DELIVERY_MODE` unset AND `AUTO_PHASE_*` unset → derive `resolved_phase_plan` from `recommended_delivery_mode`. Explicit `DELIVERY_MODE` / `AUTO_PHASE_*` / `start-from` always win (L8). Early-return when `WORK_KIND_ROUTING != "1"` (zero overhead — Q8). | B |
| **T-005** | AC-7 | Emit the four `WORK_KIND_*` reason codes (Q2) with remediation prose in `sprints/Sxxxx/qa-findings.md` / `release-findings.md`. `WORK_KIND_ROUTING_DISABLED` is info-only (not fail-closed); the other three are fail-closed. | B |
| **T-006** | AC-9 | Create `tests/work_kind_classify_test.py` (or `tests/us0118_contract_test.py`) with the 12 `test_us0118_*` markers enumerated in Q4. Active + `template/` parity for the new script + scratchpad lines. | B |
| **T-007** | AC-3 | Add `### Work-kind routing keys (US-0118)` sub-block to `its_magic/README.md` `### Full scratchpad reference (detailed)` (after the US-0117 `### Phase & role governance keys` block L2856) — documents `WORK_KIND_ROUTING` key + four reason codes + cross-link pointer to `### Release & distribution keys` for `DELIVERY_MODE` precedence. One-way copy to `template/its_magic/README.md`. Verify `PARITY_OK <size> <size>`. (README edits happen in `/execute`, not `/architecture`.) | B |
| **T-008** | AC-11 | Append `## Work-kind routing (US-0118)` h2 to `docs/engineering/runbook.md` (Q7) + `template/docs/engineering/runbook.md` parity. Content: `WORK_KIND_ROUTING` flag, L8 precedence, operator recipe (force full lifecycle on `doc` story via `DELIVERY_MODE=standard`), `--explain` usage, four reason codes. | B |
| **T-009** | AC-9 / AC-12 | Add `tests/work_kind_classify_test.py` to the active test suite; verify 4-prior pytest still green. Add `scripts/work_kind_classify_lib.py` + `template/scripts/work_kind_classify_lib.py` to `installer-owned-paths.manifest` `[install_include_paths]` (Q10/installer parity — triple-installer PS1/Bash/Python ships the new script). Add `WORK_KIND_ROUTING_PAIRS` to `scripts/check_intake_template_parity.py` + `--scope=work-kind-routing` flag (Q6). | B |

**Execution order**: T-anch → T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 → T-008 → T-009. Acyclic. (T-anch first because it is on `architecture.md`, not `its_magic/README.md` — keeps the README byte-stability surface clean for T-001..T-007.)

**Total task seeds: 10 (T-anch + T-001..T-009) — within `SPRINT_MAX_TASKS=12`.** `/sprint-plan` may merge or split within the 12-task budget.


### Test markers (12 — from R-0106 Q4 LOCKED)

`test_us0118_doc_kind_routes_to_lean_plan`, `test_us0118_mini_kind_routes_to_ultra_lean`, `test_us0118_mini_kind_routes_to_mega_quick_when_eligible`, `test_us0118_code_kind_routes_to_standard`, `test_us0118_explicit_delivery_mode_wins_over_work_kind`, `test_us0118_auto_phase_wins_over_work_kind`, `test_us0118_routing_off_is_noop`, `test_us0118_classify_touched_files_reuse`, `test_us0118_intake_evidence_records_work_kind`, `test_us0118_reason_codes_preserved`, `test_us0118_default_off_zero_overhead`, `test_us0118_explain_emits_rule_trace` (in `tests/work_kind_classify_test.py` per R-0106 Q4; or `tests/us0118_contract_test.py` — name finalized in `/sprint-plan`).

Plus the regression baseline marker: `tests/scratchpad_example_parity_test.py` (4 tests — BUG-0013 parity baseline; do not weaken).

### Compose guards UNCHANGED (23 cumulative — same 23 as US-0117)

US-0118 is a code-bearing story but lives entirely **additive** to the compose surface — it adds a new flag (`WORK_KIND_ROUTING`), a new lib (`work_kind_classify_lib.py`), new backlog row fields, a new precedence clause, a new README sub-block, and a new runbook h2. It does **not** amend any existing compose-surface feature. The 23 compose guards (cumulative across all prior stories — US-0118 adds no new family-internal guards because US-0118 is itself a single-feature story, not a family umbrella) remain UNCHANGED:

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062.

**Does US-0118 itself become a NEW compose guard?** **NO.** US-0118 is a **routing primitive**, not a compose-surface guard. The 6 read-only compose consumers (US-0096 / US-0070 / US-0078 / US-0051 / US-0069 / US-0103) consume US-0118's output; they are not amended by it. Adding US-0118 to the compose-guard list would conflate a routing primitive with a guard — rejected. US-0118's contract is enforced by its own 12 `test_us0118_*` markers + the `WORK_KIND_ROUTING=0` zero-overhead-when-off contract (test `test_us0118_default_off_zero_overhead`).

### DC (deferred-candidate) resolution

`dc_check=clean`. `grep "^## US-0118" docs/engineering/architecture.md` prior to this phase → **no matches**. The `## US-0118` h1 anchor is **added in THIS `/architecture` phase** (per R-0105 Q-2 LOCKED pattern — architecture artifacts live in `architecture.md`, not in `/execute`; T-anch in the sprint seeds is the resolution point). 

Cross-check against the full US-xxxx list in `docs/product/backlog.md`: no OTHER deferred `## US-xxxx` anchors remain unresolved. US-0117 was the **final deferred-candidate resolution point** (36 `## US-xxxx` h1 anchors added in US-0117's `/architecture` phase — 18 own + 18 deferred DC-1..DC-4); the deferral register is clean. US-0118 inherits no DC candidates from prior stories. No new DC candidates are created by US-0118 (its own `## US-0118` anchor is resolved HERE, not deferred). Deferral register remains clean — no carry-over to a successor story.

### Compose, do not amend (verification — read-only consumers of US-0118)

| Story | README anchor | architecture.md anchor | Verification |
|-------|---------------|------------------------|--------------|
| US-0096 / DEC-0082 (delivery modes) | L2617 `### Integration & observability keys` (DELIVERY_MODE cross-link) + L2670 inline ref | `## US-0096` L1684 | ✓ exists — explicit `DELIVERY_MODE` still wins (L8); US-0118 only fills the unset case |
| US-0070 / DEC-0052 (phase selection) | L2856 `### Phase & role governance keys` (AUTO_PHASE_* canonical) | `## US-0070` L1572 | ✓ exists — `AUTO_PHASE_*` remains explicit override; classifier only fills the unset case |
| US-0078 / DEC-0060 (intake evidence) | L479 runbook `## Interactive intake evidence validation` | `## US-0078` L1596 | ✓ exists — evidence gate still runs before any write (L10); classifier proposal + operator decision recorded in evidence bundle |
| US-0051 (decomposition) | L371 runbook `## Intake decomposition and risk-aware questioning` | (no h1 anchor) | ✓ exists — classifier runs after the decomposition evaluator (L10) |
| US-0069 / DEC-0051 (phase→role matrix) | L2856 `### Phase & role governance keys` | `## US-0069` L1568 | ✓ exists — classifier only selects which phases run, not who runs them |
| US-0103 (AI decision ledger) | L2421 `### Sovereign-loop era keys` | `## US-0103` L1640 | ✓ exists — read-only consumer for audit trail |

All 6 compose targets verified present (read-only consumers of US-0118 — their architectural surfaces are NOT edited by US-0118; additive-only: new flag, new lib, new row fields, new precedence clause, new sub-block, new runbook h2).


### Risks finalized (R1..R8 — promoted from R-0106)

| Risk | Severity | Mitigation |
|------|----------|------------|
| **R1** Classification ambiguity (mixed `docs/` + `src/` tiers) | **MEDIUM** | Q1 LOCKED: highest tier wins (`code` > `mini` > `doc`) per `classify_touched_files` tier_rank A>B>C. Single-pass deterministic. Contract test `test_us0118_code_kind_routes_to_standard` covers the mixed-tier case. |
| **R2** Precedence conflicts (`WORK_KIND_ROUTING=1` + `DELIVERY_MODE` set) | **MEDIUM** | L8 precedence chain LOCKED + `WORK_KIND_DELIVERY_MODE_CONFLICT` reason code (Q2). Explicit operator flags always win; classifier fills only the unset case. Contract test `test_us0118_explicit_delivery_mode_wins_over_work_kind` + `test_us0118_auto_phase_wins_over_work_kind`. |
| **R3** `mega_quick` eligibility overlap with `mini` | **LOW–MEDIUM** | L6 LOCKED: classifier recommends `mega_quick` only when US-0096 eligibility passes (AC≤3, no DEC, single component), else falls back to `ultra_lean`. Contract test `test_us0118_mini_kind_routes_to_mega_quick_when_eligible` + `test_us0118_mini_kind_routes_to_ultra_lean`. |
| **R4** Backward compatibility (existing backlog rows without `work_kind`) | **MEDIUM** | Q8 LOCKED: `WORK_KIND_ROUTING=0` default-off + early-return in `/auto` step 0 + `/intake` step 5 skip. No forced reclassification, no schema-migration. Contract test `test_us0118_default_off_zero_overhead`. |
| **R5** Operator trust (deterministic + inspectable) | **LOW–MEDIUM** | Q3 LOCKED: deterministic pure-stdlib + `--explain` flag emitting `rule_trace` (Q10). Contract test `test_us0118_explain_emits_rule_trace`. Operators can override with confidence. |
| **R6** Reuse boundary drift (`dev_environment_lib.classify_touched_files` rewritten vs imported) | **LOW** | Q9 LOCKED (in T-001): `work_kind_classify_lib.py` imports `TIER_C_SKIP_PREFIXES` + `classify_touched_files` from `dev_environment_lib` — no duplication. Contract test `test_us0118_classify_touched_files_reuse`. |
| **R7** Installer parity drift (triple-installer must ship new script) | **LOW** | T-009 adds both `scripts/work_kind_classify_lib.py` + `template/scripts/work_kind_classify_lib.py` to `installer-owned-paths.manifest` `[install_include_paths]`. Manifest-driven single source of truth. |
| **R8** Cross-story byte-stability surface (6th sub-block) — US-0118 is the first NEW story after the US-0113..US-0117 quint; it adds a 6th sub-block to `### Full scratchpad reference (detailed)`. Risk of accidentally editing a prior released block (US-0113 L2421 / US-0114 L2545 / US-0115 L2617 / US-0116 L2765 / US-0117 L2856). | **MEDIUM** | T-007 mandates net-new-keys-only + cross-link-pointer + reason-code-only shape; never edits prior released blocks. Execute-phase verifies `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2856 range (no removals/modifications to US-0113..US-0117 blocks). QA re-verifies. `PARITY_OK <size> <size>` authoritative end-to-end proof. Pattern now scales from quint to 6th story. |

### Stop conditions met

- **No DEC required beyond DEC-0118** — DEC-0118 authored in THIS phase (Required → Accepted; mirrors DEC-0082 / DEC-0052 precedent).
- **No feasibility unknown** — R-0106 closed all 10 discovery open questions Q1..Q10; approach A1 locked; sprint seeds T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; risks R1..R8 finalized; DC check clean.
- **No data migration risk** — `WORK_KIND_ROUTING=0` default-off + no forced reclassification of existing backlog rows (Q8 LOCKED). New `work_kind` / `recommended_delivery_mode` fields are optional; absence is valid.
- **Compose-do-not-amend verified** — all 6 compose targets (US-0096 / US-0070 / US-0078 / US-0051 / US-0069 / US-0103) verified present with existing `## US-xxxx` h1 anchors in `architecture.md`; US-0118 is additive-only.

**No DECISION_GATE raised.** Architecture phase revealed no question requiring operator input. DC check clean (no new DC candidates). Verdict: **PASS**.

### Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called (US-0118 documentation-only so far — architecture phase writes prose + DEC only; existing digest context sufficient per R-0106 — S0113..S0117 retrospectives established the reusable patterns applied here: cross-link pointer pattern scales to 6th story; angle-distinct narrative pattern extends to the routing-primitive angle (distinct from prior 5 documentation-family angles); cross-story byte-stability contract now scales from quint to 6th story; DC anchor resolution pattern proven (US-0117 was the final deferred-candidate resolution point — US-0118 inherits a clean deferral register). No write to `mistakes.jsonl` in architecture phase.

### Consequences

- Sprint: S0118 (pending `/sprint-plan`).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.
- New code surface: `scripts/work_kind_classify_lib.py` (NEW) + `tests/work_kind_classify_test.py` (NEW) + installer manifest rows.
- New doc surface: `## US-0118` h1 anchor in `architecture.md` (this section) + `### Work-kind routing keys (US-0118)` README sub-block (in `/execute`) + `## Work-kind routing (US-0118)` runbook h2 (in `/execute`).
- New scratchpad surface: `WORK_KIND_ROUTING=0` key + `WORK_KIND_*` reason-code family (in `/execute`).
- New command surface: `.cursor/commands/auto.md` precedence clause + `.cursor/commands/intake.md` step-5 hook (in `/execute`).
- New evidence schema: `work_kind` / `recommended_delivery_mode` / `work_kind_operator_decision` fields in `handoffs/intake_evidence/*.json` (in `/execute`).
- **`WORK_KIND_ROUTING=0` (default)**: zero overhead — `/auto` `resolve_delivery_mode` + `/intake` step 5 skip classifier entirely; existing backlog rows without `work_kind` route via current `DELIVERY_MODE`/`AUTO_PHASE_*` precedence (no forced reclassification).
- **`WORK_KIND_ROUTING=1`**: classifier runs at intake (after ACs) and at `/auto` step 0; `recommended_delivery_mode` derived from `work_kind` fills the unset case (L8 precedence); explicit operator flags always win.
- **23/23 compose guards UNCHANGED** (additive-only). 6 read-only compose consumers (US-0096 / US-0070 / US-0078 / US-0051 / US-0069 / US-0103) consume US-0118 output; not amended.
- DC resolution: `## US-0118` h1 anchor added in THIS phase (per R-0105 Q-2 LOCKED pattern); deferral register clean — no carry-over.

### Evidence references

- `docs/product/backlog.md` — `## US-0118` block (L3983–L4025, 12 ACs)
- `docs/product/acceptance.md` — US-0118 row L145 (12 ACs, OPEN)
- `docs/engineering/research.md` — `## R-0106` (delivered 2026-07-04T20:00:00Z, 10/10 open questions Q1..Q10 closed LOCKED; architecture seeds T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; companion DEC-0118 required; AC baselines green; risks R1..R8 finalized)
- `handoffs/po_to_tl.md` — research handoff (topmost block) + discovery handoff + intake handoff
- `docs/engineering/state.md` — research checkpoint (latest) + architecture checkpoint (this phase, appended)
- `handoffs/resume_brief.md` — top block updated to reflect architecture complete
- `scripts/dev_environment_lib.py` — `TIER_C_SKIP_PREFIXES` (L117–L125: `docs/`, `handoffs/`, `sprints/`, `decisions/`, `tests/`, `.cursor/commands/`, `template/docs/`) + `classify_touched_files` (L321–L339: tier A/B/C with `tier_rank={"A":3,"B":2,"C":1}`, highest matching tier wins) — reuse anchor (Q9 LOCKED import contract)
- `its_magic/README.md` — L2421 (US-0113 keys block — byte-stability preserved); L2545 (US-0114 keys block — byte-stability preserved); L2617 (US-0115 keys block — byte-stability preserved); L2765 (US-0116 keys block — byte-stability preserved); L2856 (US-0117 keys block — byte-stability preserved + insertion point for `### Work-kind routing keys (US-0118)` 6th sub-block in `/execute`)
- `docs/engineering/architecture.md` — h1 inventory confirmed: `## US-0069` L1568, `## US-0070` L1572, `## US-0078` L1596, `## US-0103` L1640, `## US-0096` L1684 exist (read-only consumers of US-0118); `## US-0118` added in THIS phase (appended below the existing `## US-0099` section)
- `decisions/DEC-0118.md` — companion DEC (authored in THIS phase)
- `.cursor/scratchpad.md` — `WORK_KIND_ROUTING` (new key, added in `/execute`); `DELIVERY_MODE` / `AUTO_PHASE_*` / `SPRINT_MAX_TASKS` (existing — grep anchors only)
- `.cursor/commands/auto.md` — `resolve_delivery_mode` step 0 (precedence clause added in `/execute`)
- `.cursor/commands/intake.md` — step 5 (classifier hook added in `/execute`)


### Isolation evidence (per US-0048 / DEC-0029)

- `phase_id=architecture`
- `role=tech-lead`
- `story_id=US-0118`
- `sprint_id=(pending — created at sprint-plan)`
- `orchestrator_run_id=auto-20260704-01`
- `delivery_mode=ultra_lean`, `macro_phase=plan` (architecture — second canonical phase of `plan` macro per US-0096 / DEC-0082; research + architecture + sprint-plan merged)
- `fresh_context_marker=tl-US0118-architecture-20260704T203000Z-fresh`
- `timestamp=2026-07-04T20:30:00Z` (UTC)
- `evidence_ref=docs/product/backlog.md (## US-0118 block L3983–L4025 narrow-read), docs/product/acceptance.md (US-0118 row L145 narrow-read), handoffs/intake_evidence/US-0118-intake.json (cross-reference only — not read this phase), handoffs/po_to_tl.md (US-0118 research handoff L5–L93 + discovery handoff L95–L193 + intake handoff L196–L231 narrow-read), docs/engineering/state.md (research checkpoint L197–L297 + discovery checkpoint L102–L196 + drain-advance breadcrumb L84–L101 narrow-read), docs/engineering/research.md (R-0106 entry L8754–L8904 full read), docs/engineering/architecture.md (grep ^## US- anchors + US-0117 section L1420–L1566 read as template + DC anchor verification L1568–L1710 + US-0099 last line L1710), scripts/dev_environment_lib.py (TIER_C_SKIP_PREFIXES L117–L125 + classify_touched_files L321–L339 narrow-read for Q9 import-contract lock), its_magic/README.md (grep ### .*keys anchors only — no full-read), decisions/DEC-0082.md (full read as DEC-0118 template), decisions/DEC-0052.md (full read as DEC-0118 template), docs/product/backlog.md (grep ^## US- anchors for DC cross-check), handoffs/resume_brief.md (top ~30 lines narrow-read for drain-advance prose shape)`
- Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the narrow-read files listed above (US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python SHA-256 computation for the strict runtime proof + powershell line-count computations + the artifact writes listed in this phase (architecture.md `## US-0118` section append, decisions/DEC-0118.md NEW, po_to_tl.md architecture handoff prepend, state.md architecture checkpoint append, resume_brief.md drain-advance append). No `.env` reads, no credentials access, no intake-evidence mutation (read-only for this phase).
- `assemble_sovereign_memory_digest(...)` NOT called (US-0118 documentation-only so far — architecture phase writes prose + DEC only; existing digest context sufficient per R-0106 — S0113..S0117 retrospectives established reusable patterns; classifier code is built in `/execute`, not here).
- No write to `mistakes.jsonl` in architecture phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).
- Prior phase strict proof consumed: `rp-auto-20260704-01-research-techlead-20260704T200000Z-US-0118` (from `docs/engineering/state.md` research checkpoint L281–L285, unchanged).
- Current architecture-phase strict proof recorded below.

### Strict runtime proof (DEC-0038)

- **runtime_proof_id**: `rp-auto-20260704-01-architecture-techlead-20260704T203000Z-US-0118`
- **canonical_payload** (sorted-key JSON per DEC-0038): `{"orchestrator_run_id":"auto-20260704-01","phase_id":"architecture","proof_issued_at":"2026-07-04T20:30:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260704-01-architecture-techlead-20260704T203000Z-US-0118","sprint_id":"(pending)","story_id":"US-0118"}`
- **proof_hash**: `fd72d56bd8e8450cf830e3a4fa6164d5e3b98595c00fafa166ffd00669b1d3db` (SHA-256 of the sorted-key JSON payload above, computed via python `hashlib.sha256`)
- **proof_ttl_seconds**: 3600
- **proof_ttl**: 2026-07-04T21:30:00Z (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

### Decision gate

- `decision_gate=false` (no DECISION_GATE; no hard stop; companion DEC-0118 authored Accepted in THIS phase; approach A1 locked; sprint seeds T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; risks R1..R8 finalized; DC check clean; compose-do-not-amend verified 6/6)
- `stop_conditions_met=yes` (no missing references — all 6 compose targets verified; no decision gate triggered; AC baselines green: `validate_readme_feature_coverage.py` PASS + `pytest tests/scratchpad_example_parity_test.py` 4 passed)

### Next scheduled phase

- `next_scheduled_phase=/sprint-plan` (role=tech-lead per US-0069 / DEC-0051 phase→role matrix default; third canonical phase of `plan` macro per ultra_lean; research + architecture + sprint-plan merged into `plan` macro)
- `next_scheduled_role=tech-lead`
- `next_scheduled_sprint_macro=plan`
- `stop_condition=STOP after architecture completes; hand off via artifacts only to /sprint-plan in fresh tech-lead subagent (BUG-0006)`

---

