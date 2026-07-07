# Sprint S0117

## Metadata

- **sprint_id**: S0117
- **story_refs**: US-0117
- **priority**: P3
- **effort**: 1 day
- **owner**: dev
- **goal**: Close the operator-documentation gap for the **phase & role governance family features** (18 features: US-0069, US-0070, US-0071, US-0072, US-0075, US-0076, US-0077, US-0078, US-0079, US-0080, US-0081, US-0082, US-0083, US-0085, US-0087, US-0088, US-0089, US-0090) in the framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`). Add the `### Phase & role governance (US-0069 / US-0070 / US-0071 / US-0072 / US-0075 / US-0076 / US-0077 / US-0078 / US-0079 / US-0080 / US-0081 / US-0082 / US-0083 / US-0085 / US-0087 / US-0088 / US-0089 / US-0090) umbrella section` under `## Commands and workflow` (L350), as a sibling — **5th sibling, first 5-cumulative-surface story, LARGEST family in the 5-story drain** — to US-0113's `### Sovereign-loop era` umbrella (L940), US-0114's `### Release & distribution` umbrella (L1225), US-0115's `### Integration & observability` umbrella (L1410), and US-0116's `### Delivery & lifecycle` umbrella (L1665), with 18 nested `#### US-xxxx` operator subsections ordered US-id-ascending (US-0069 → US-0070 → US-0071 → US-0072 → US-0075 → US-0076 → US-0077 → US-0078 → US-0079 → US-0080 → US-0081 → US-0082 → US-0083 → US-0085 → US-0087 → US-0088 → US-0089 → US-0090), inserted immediately after the closing of US-0116's umbrella block (before L1665 `### Full scratchpad reference (detailed)`). Extend `### Full scratchpad reference (detailed)` (L1665) with a `### Phase & role governance keys (US-0069 / ... / US-0090)` sub-block — **46 net-new key rows across 10 features** (US-0069/0070/0079/0080/0081/0083/0087/0088/0089/0090) + **9 reason-code-only entries** (7 features) + **7 prose-only / runbook-cross-link-only entries** (US-0071/0072/0075/0076/0077/0078/0085) + **cross-link pointers** (`DELIVERY_MODE` → US-0114 L1806; `LEAN_MEMORY_*` → US-0115 L1878 default omit; `TOKEN_PROFILE` → main reference list + US-0080 subsection; `CODEBASE_MAP_REFRESH_ON_ROLLOVER` → US-0082 subsection). Preserve framework README byte-parity, run validators green, and keep regression tests green. Documentation-only; default-off posture preserved for optional runtime features; bootstrap-on-install framing for install-time-only features. US-0113's L1682 sovereign-loop keys block, US-0114's L1806 release & distribution keys block, US-0115's L1878 integration & observability keys block, and US-0116's L2225 delivery & lifecycle keys block byte-stability PRESERVED (5th-story cumulative byte-stability surface — pure addition, cross-link pointers + reason-code-only entries + prose-only entries only; never edit prior released blocks).
- **status**: OPEN (per US-0045 — closure at /release)
- **created_at**: 2026-07-04T17:26:45Z
- **orchestrator_run_id**: auto-20260704-01
- **delivery_mode**: ultra_lean
- **macro_phase**: plan (sprint-plan — third canonical phase)
- **fresh_context_marker**: tl-US0117-sprint-plan-20260704T172645Z-fresh
- **resolved_phase_plan**: `["spec","plan","build+verify","ship"]` (ultra_lean macro — recomputed at story boundary per US-0044 / DEC-0022; `spec` already done via 5-story decomposition intake; `plan` = research + architecture + sprint-plan all complete; `build+verify` = `/execute` + `/qa` (merges plan-verify + execute QA + verify-work); `ship` = `/release` + `/refresh-context`)

## Scope

- **US-0117**: Phase & role governance operator documentation in framework README
- **Architecture anchor**: `docs/engineering/architecture.md#US-0117` (h1 section appended in architecture phase; approach_locked=A1)
- **Research anchor**: `docs/engineering/research.md` `R-0105` (delivered 2026-07-04T16:54:35Z — 8/8 spec open questions closed; 18 per-feature sub-findings; AC-3 approach locked; DC-1..DC-4 confirmed = 36 total; AC baselines green; deepened risks)
- **Companion DEC**: none (US-0117 is documentation-only; no architectural, policy, or schema surface changed. Mirrors US-0113 / US-0114 / US-0115 / US-0116 sibling precedent. R-0105 § Decision-gate check confirmed no DEC candidate; grep `^## DEC-` in `docs/engineering/decisions.md` returned no US-0117 companion DEC. DC-1+DC-2+DC-3+DC-4 resolution is a triad-hygiene closure, not a tradeoff requiring a DEC.)

## DC resolution note (36 anchors added in /architecture — final deferred-candidate resolution point)

US-0117 is the **5th and final story** in the 5-story drain and the **final deferred-candidate resolution point** for the architecture.md triad hygiene closure. The 36 `## US-xxxx` h1 anchors (18 own + 18 deferred DC-1+DC-2+DC-3+DC-4) plus the `## US-0117` section itself were **already added in the `/architecture` phase** (per R-0105 Q-2 LOCKED: resolve in `/architecture`, NOT `/execute` — keeps anchors as architecture artifacts per `docs/engineering/artifact-ownership-policy.md`).

**Consequence for this sprint plan**: **T-anch in this sprint is a NO-OP / verification task** — the 36 anchors already exist in `docs/engineering/architecture.md` (verified at L1568–L1708). T-anch does NOT perform a new write; it confirms the anchors exist and that `git diff HEAD -- docs/engineering/architecture.md` shows the architecture-phase append as pure addition. The dev subagent running T-anch simply re-verifies the anchor inventory (grep `^## US-` in architecture.md returns the 36 expected anchors + `## US-0117` section) and records the verification result; no architecture.md edits occur in execute-phase. This mirrors the architecture phase lock (R-0105 Q-2 + architecture § Sprint seeds T-anch note: "anchors appended in THIS phase, resolved here, not deferred further").

## Acceptance criteria (US-0117 — 8 ACs)

| AC | Description |
|----|-------------|
| AC-1 | `### Phase & role governance umbrella section` under `## Commands and workflow` |
| AC-2 | Per-feature operator subsections for US-0069/US-0070/US-0071/US-0072/US-0075/US-0076/US-0077/US-0078/US-0079/US-0080/US-0081/US-0082/US-0083/US-0085/US-0087/US-0088/US-0089/US-0090 |
| AC-3 | Full scratchpad reference extension (46 net-new key rows + 9 reason-code-only entries + 7 prose-only / runbook-cross-link-only entries + cross-link pointers) |
| AC-4 | Coverage preserved (`validate_readme_feature_coverage.py --enforce` green) |
| AC-5 | Framework README parity (`its_magic/README.md` ↔ `template/its_magic/README.md` byte-identical) |
| AC-6 | Audience + metadata hygiene |
| AC-7 | Runbook cross-links per feature (18 features → 18 anchors: US-0069 L1711 h2; US-0070 L1753 h2; US-0071 L303 h2; US-0072 L550 h2; US-0075 L1949 h3 + L2535 h2; US-0076 L63 h2; US-0077 L98 h2; US-0078 L479 h2; US-0079 L512 h2; US-0080 L550 h2 + L570 h3; US-0081 L2032 h3; US-0082 L63 h2; US-0083 L479 h2 + L591 h3; US-0085 L1628 h2; US-0087 L1809 h2 + L1958 h3; US-0088 L1838 h2; US-0089 L1398 h3 + L1838 h2; US-0090 L2099 h3) |
| AC-8 | Regression tests (coverage parity contract tests green; no test weakenings) |

## AC → task surjective coverage (7 tasks, 8 ACs)

| AC | Task(s) | Architecture anchor |
|----|---------|---------------------|
| DC resolution (36 anchors) | T-anch | § Sprint seeds T-anch (NO-OP / verification — anchors already added in /architecture) |
| AC-1 Umbrella section | T-001 | § Sprint seeds T-001 |
| AC-2 Per-feature operator subsections | T-002 | § Sprint seeds T-002 |
| AC-3 Full scratchpad reference extension | T-003 | § Sprint seeds T-003 |
| AC-4 Coverage preserved | T-005 | § Sprint seeds T-005 |
| AC-5 Framework README parity | T-004 | § Sprint seeds T-004 |
| AC-6 Audience + metadata hygiene | T-005 | § Sprint seeds T-005 |
| AC-7 Runbook cross-links per feature | T-002 | § Sprint seeds T-002 |
| AC-8 Regression tests | T-006 | § Sprint seeds T-006 |

**Surjectivity check**: AC-1..AC-8 all covered (8/8) + DC resolution covered (T-anch). Multi-AC tasks: **T-002** (AC-2+AC-7), **T-005** (AC-4+AC-6). Every AC has ≥1 task. No `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 7 (T-anch + T-001..T-006)
- **SPRINT_MAX_TASKS**: 12 (from `.cursor/scratchpad.md`)
- **Within limit**: yes (7 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **SPRINT_AUTO_SPLIT_TRIGGERED**: false

## Tasks (T-anch + T-001..T-006)

See `sprints/S0117/tasks.md` for atomic task definitions. Execution order (per architecture dependency chain):

```
T-anch (verify 36 anchors exist) → T-001 (umbrella) → T-002 (18 subsections) →
T-003 (scratchpad ref extension) → T-004 (template byte-sync) →
T-005 (validators) → T-006 (regression tests)
```

| ID | Title | ACs | Tranche | Risk |
|----|-------|-----|:--------|:-----|
| T-anch | **NO-OP / verification** — confirm the 36 `## US-xxxx` h1 anchors (18 own: US-0069/0070/0071/0072/0075/0076/0077/0078/0079/0080/0081/0082/0083/0085/0087/0088/0089/0090 + 18 deferred DC-1+DC-2+DC-3+DC-4: US-0103/0104/0105/0107/0110 + US-0041/0062 + US-0034/0084/0086/0093/0096/0101/0102 + US-0092/0095/0098/0099) plus the `## US-0117` section already exist in `docs/engineering/architecture.md` (added in `/architecture` phase per R-0105 Q-2 LOCKED; architecture.md L1568–L1708). No new write. Verify `git diff HEAD -- docs/engineering/architecture.md` shows pure addition from the architecture phase (no execute-phase edits to architecture.md). | DC resolution (AC-2 / AC-8 indirect) | A | LOW |
| T-001 | Add `### Phase & role governance (US-0069 / ... / US-0090) umbrella section` under `## Commands and workflow` (after US-0116 umbrella close, before L1665 `### Full scratchpad reference (detailed)`). 18-step enable order (US-id-ascending) + runbook pointer line + zero-overhead-when-off contract line + "phase governance integration" introductory framing (AC-1). | AC-1 | A | LOW |
| T-002 | Add 18 per-feature `#### US-xxxx` operator subsections nested under umbrella (US-0069 → US-0090). Two labeling corrections applied: **US-0082 = "Codebase map"** (NOT "Input compression"; per runbook L63 + DEC-0065); **US-0090 = "Caveman input compression"** (NOT "Phase governance integration"; per runbook L2099 + DEC-0073 — "phase governance integration" is the umbrella-level introductory framing AC-1, not a separate `#### US-0090` subsection); **US-0089 = "Auto orchestration"** (NOT "Caveman mode" — runbook US-id collision at `## Caveman mode (US-0089)` L2032 resolved in `/architecture`; `#### US-0089` subsection title = "Auto orchestration"). Each subsection carries AC-7 runbook cross-link. | AC-2, AC-7 | A | MEDIUM (18-subsection scope size — 2–4× prior stories' T-002 load) |
| T-003 | Add `### Phase & role governance keys (US-0069 / ... / US-0090)` sub-block under `### Full scratchpad reference (detailed)` (after US-0116 L2225 block; before `### Remote execution config`). 46 net-new key rows (10 features: US-0069/0070/0079/0080/0081/0083/0087/0088/0089/0090) + 9 reason-code-only entries (7 features: US-0070/0077/0081/0083/0085/0087 + US-0099-not-applicable-here) + 7 prose-only / runbook-cross-link-only entries (US-0071/0072/0075/0076/0077/0078/0085) + cross-link pointers (`DELIVERY_MODE` → US-0114; `LEAN_MEMORY_*` → US-0115 default omit; `TOKEN_PROFILE` → main ref + US-0080 subsection; `CODEBASE_MAP_REFRESH_ON_ROLLOVER` → US-0082 subsection). 5th-story cumulative byte-stability surface — prior 4 blocks byte-identical. | AC-3 | A | MEDIUM (first 5-cumulative-surface story) |
| T-004 | Sync `template/its_magic/README.md` byte-identical to `its_magic/README.md` (one-way copy). Verify `PARITY_OK <size> <size>`. | AC-5 | B | MEDIUM |
| T-005 | Run validators: `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]` with `coverage_missing=["US-0117"]` unchanged (US-0117 not in catalog surface). `python scripts/validate_doc_profile.py --repo .` + `python scripts/check-user-visible-metadata.py --repo .` + `python scripts/check_intake_template_parity.py --repo .` → expect PASS. Fix any narrative prose leaking internal IDs. | AC-4, AC-6 | B | LOW (catalog) / MEDIUM (encoding prerequisite) |
| T-006 | Run regression tests: `python -m pytest tests/scratchpad_example_parity_test.py -v` → 4 passed. Forbid edits to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, `tests/scratchpad_example_parity_test.py`. | AC-8 | B | LOW–MEDIUM |

## Test markers (5 — same as prior stories, no new tests proposed)

| Marker | File | ACs covered | Notes |
|--------|------|-------------|-------|
| `test_bug0013_parity_check` + 3 companions | `tests/scratchpad_example_parity_test.py` | AC-5 (indirect), AC-8 | US-0117 does NOT modify `.cursor/scratchpad.md` or `template/.cursor/scratchpad.local.example.md`; tests remain green by construction. |
| `validate_readme_feature_coverage.py --enforce` | `scripts/validate_readme_feature_coverage.py` | AC-4 | Coverage gate; `coverage_missing=["US-0117"]` baseline (US-0117 not in catalog surface). Catalog block L63 read-only. |
| `check_intake_template_parity.py` | `scripts/check_intake_template_parity.py` | AC-5 | Framework README byte-parity gate. |
| `validate_doc_profile.py` | `scripts/validate_doc_profile.py` | AC-6 | Audience profile gate. |
| `check-user-visible-metadata.py` | `scripts/check-user-visible-metadata.py` | AC-6 | Metadata hygiene gate. |

**No new tests proposed.** AC-8 satisfied by existing tests remaining green (read-only gates, not edit targets). R-0105 confirmed no test weakenings.

## Files to touch

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `its_magic/README.md` | `template/its_magic/README.md` | T-001, T-002, T-003, T-004 | Byte-identical via T-004 one-way copy |
| 2 | _(verification only)_ `docs/engineering/architecture.md` | — | T-anch (NO-OP / verification — no execute-phase write) | N/A |

## Files NOT to touch (non-goals — hard)

- `.cursor/scratchpad.md` — canonical source of truth (never edit in docs stories; BUG-0013 precedent; US-0117 only documents existing keys).
- `template/.cursor/scratchpad.local.example.md` — canonical example (BUG-0013 ownership); US-0117 does not extend the example scratchpad (AC-3 extension is in README only).
- `docs/product/backlog.md` — status authority (closure only at /release per US-0045). **Note:** working-tree copy has 185 stray `0xa7` bytes (encoding regression flagged in R-0102 + R-0103 + R-0104 + R-0105) — orchestrator must restore encoding hygiene before execute so AC-4 can be re-verified post-execute. **NOT a US-0117 blocker.**
- `docs/engineering/runbook.md` — AC-7 cross-links only; **no new runbook content** (AC-7 forbids duplication). All 18 runbook cross-link targets already exist (verified in R-0105).
- `docs/developer/README.md` — separate audience surface owned by US-0097 (project README parity) compose guard; AC-6 is a validator gate, not an edit mandate.
- `docs/engineering/architecture.md` — **other than the `## US-0117` section + 36 DC anchors already appended in `/architecture` phase, NO execute-phase edits**. T-anch is a NO-OP / verification task (the 36 anchors + `## US-0117` section already exist at L1568–L1708). Execute-phase does NOT add h1 anchors.
- `installer.py`, `installer.ps1`, `installer.sh` — no installer changes (US-0008/US-0018/US-0057/US-0075 + US-0062/DEC-0045 + US-0041/BUG-0003 compose guards).
- All `scripts/*` — validators are read-only gates, not edit targets.
- All phase & role governance scripts and Python/PowerShell/Shell files — US-0069/US-0070/.../US-0090 features are **documented only**, not amended.
- `tests/scratchpad_example_parity_test.py` — read-only regression gate; if it fails, fix prose not test.
- **Do NOT modify US-0113's `### Sovereign-loop era` / `### Sovereign-loop era keys` blocks (L940 / L1682), US-0114's `### Release & distribution` / `### Release & distribution keys` blocks (L1225 / L1806), US-0115's `### Integration & observability` / `### Integration & observability keys` blocks (L1410 / L1878), or US-0116's `### Delivery & lifecycle` / `### Delivery & lifecycle keys` blocks (L1665 / L2225)** in `its_magic/README.md` — byte-stability contract (all 4 already released in S0113 / S0114 / S0115 / S0116). US-0117 adds cross-link pointers to these blocks from its own 5th sub-block; it never edits them. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2225 range (no removals/modifications to US-0113's L1682, US-0114's L1806, US-0115's L1878, or US-0116's L2225 blocks).

## Compose guards UNCHANGED (23 cumulative — same 23 as US-0116)

US-0117 is documentation-only and lives entirely outside the compose surface. The 23 compose guards (cumulative across all prior stories — US-0117 adds no new family-internal guards because all 18 in-scope features are phase & role governance operators, not compose-surface features) remain UNCHANGED:

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062.

| Story | Compose rule (UNCHANGED) |
|-------|---------------------------|
| US-0091 | Feature coverage catalog anchor `<!-- readme-feature-coverage-catalog -->` (L63) + one-liners UNCHANGED — US-0117 appends narrative sections outside the catalog block. |
| US-0097 | Project README parity surface UNCHANGED — US-0117 touches framework README pair only, not project README. |
| US-0017 | Framework README parity contract UNCHANGED — US-0117 preserves byte-parity via T-004 lockstep. |
| US-0040 | Per-sprint release notes semantics UNCHANGED. |
| US-0100 | Semantic changelog UNCHANGED. |
| US-0101 | Catalog schema (DEC-0086) UNCHANGED — documented only. |
| US-0102 | Role catalog precedence (DEC-0087) UNCHANGED — documented only. |
| US-0103 | AI Decision Ledger schema/semantics UNCHANGED — documented only. |
| US-0104 | Cross-Model Adversarial Critic schema/semantics UNCHANGED — documented only. |
| US-0105 | Sovereign Memory schema/semantics UNCHANGED — documented only. |
| US-0107 | Sovereign Loop Mode schema/semantics UNCHANGED — documented only. |
| US-0108 | Parallel Instance Arbitrage schema/semantics UNCHANGED — documented only. |
| US-0109 | Self-Healing Deploy Loop schema/semantics UNCHANGED — documented only. |
| US-0110 | Goal-Based Convergence schema/semantics UNCHANGED — documented only. |
| US-0111 | Release Trigger Adapters schema/semantics UNCHANGED — documented only. |
| US-0112 | Model-Catalog Example Presets schema/semantics UNCHANGED — documented only. |
| US-0034 | Cross-repo compatibility observability schema/semantics UNCHANGED — documented only. |
| US-0084 | Codebase map freshness gate schema/semantics UNCHANGED — documented only. |
| US-0086 | Handoff hygiene validator schema/semantics UNCHANGED — documented only. |
| US-0093 | Scratchpad drift detector schema/semantics UNCHANGED — documented only. |
| US-0096 | Active context handoff schema/semantics UNCHANGED — documented only. |
| US-0041 | End-to-End Lifecycle QA schema/semantics UNCHANGED — documented only. |
| US-0062 | Installer-Owned `its_magic/` folder boundary (DEC-0045, amended by DEC-0083/US-0097) UNCHANGED — documented only. |

**23 guards UNCHANGED.**

## 5th-story cumulative byte-stability surface note

US-0117 is the **first 5-cumulative-surface story** — the cumulative byte-stability surface now covers **4 prior released blocks** (US-0113's `### Sovereign-loop era keys` L1682 + US-0114's `### Release & distribution keys` L1806 + US-0115's `### Integration & observability keys` L1878 + US-0116's `### Delivery & lifecycle keys` L2225). The cross-story byte-stability contract (S0114 retrospective — "net-new keys + cross-link pointers + reason-code-only entries + prose-only entries; never edit prior story's released block") now scales from a quad to a quint. US-0117's net-new content (46 key rows + 9 reason-code-only + 7 prose-only + cross-link pointers) is added to its own 5th sub-block; it never edits prior released blocks. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2225 range (no removals/modifications to US-0113's L1682, US-0114's L1806, US-0115's L1878, or US-0116's L2225 blocks). Pattern now established as a quint (S0113/S0114/S0115/S0116 + US-0117).

## 2 labeling corrections note (LOCKED in /architecture)

Per R-0105 § Per-feature sub-findings + architecture `## US-0117` § Approach A1, two PO-side labeling ambiguities are LOCKED to authoritative runbook + DEC labels:

- **US-0082 = "Codebase map"** (NOT "Input compression" per spec handoff). Authoritative per runbook `## Codebase map bootstrap (US-0082 / DEC-0065)` L63 h2 + DEC-0065 + architecture `## US-0082 — Codebase map (bootstrap mechanism)` L1612. The spec handoff's "US-0082 (Input compression)" is a PO-side mislabel; the input-compression surface is owned by US-0090.
- **US-0090 = "Caveman input compression"** (NOT "Phase governance integration" per spec handoff). Authoritative per runbook `### Caveman input compression (US-0090)` L2099 h3 + DEC-0073 + architecture `## US-0090 — Caveman input compression` L1636. The "phase governance integration" concept is the **umbrella-level introductory framing** (AC-1), not a separate `#### US-0090` subsection.

T-002 applies both corrections in the `#### US-0082` and `#### US-0090` subsection titles + narrative content.

## US-0089 US-id collision note (LOCKED in /architecture)

Per R-0105 § US-0081 + US-0090 findings + architecture `## US-0089 — Auto orchestration` L1632, the runbook contains a US-id collision:

- Runbook h2 `## Caveman mode (US-0089)` at L2032 — covers caveman voice/level (US-0081 family content).
- 18-feature family US-0089 = **Auto orchestration** (per scratchpad L21 `AUTO_PAUSE_REQUEST` + L135 `AUTO_REMOTE_AUTOMATION_PROFILE` + 18-feature family decomposition in backlog.md US-0117 block).

`/architecture` LOCKS the resolution: the `#### US-0089` subsection title in the US-0117 umbrella = **"Auto orchestration"** (NOT "Caveman mode"). The caveman-mode narrative is owned by `#### US-0081` (US-0081 owns `CAVEMAN_MODE` / `CAVEMAN_LEVEL` keys); US-0089 owns the auto-orchestration narrative (`AUTO_PAUSE_REQUEST` + `AUTO_REMOTE_AUTOMATION_PROFILE`). T-002 applies this resolution in the `#### US-0089` subsection title + narrative content.

## Plan-verify readiness (ultra_lean merge note)

In **ultra_lean** delivery mode, `/plan-verify` is **merged into the `build+verify` macro under QA** — the orchestrator routes; this sprint does **not** pre-create `sprints/S0117/plan-verify.json`. The sprint-plan output is plan-verify-ready (surjective AC coverage, atomic tasks, test markers aligned, T-anch NO-OP documented) so QA can verify in one spawn within `build+verify`.

`build+verify` macro canonical phases (per ultra_lean):
1. `/execute` (dev) — first canonical phase
2. `/qa` (qa) — merges plan-verify + execute QA + verify-work

## Decision gate check

**No DECISION_GATE raised.** Architecture phase resolved all 8 R-0105 carry-overs within the `plan` macro (approach A1 locked; sprint seeds T-anch + T-001..T-006; files to touch/not to touch locked; DC-1+DC-2+DC-3+DC-4 RESOLVED in `/architecture` — T-anch in this sprint is NO-OP / verification; encoding hygiene prerequisite flagged; 5th-story cumulative byte-stability surface LOCKED; 2 labeling corrections LOCKED; US-0089 US-id collision LOCKED). Sprint-plan revealed no question requiring operator input. Verdict: **PASS**.

## Sovereign memory note

Sprint-plan phase does NOT call `advance_sovereign_loop` (advance hook runs at segment boundary post `ship` macro). Sovereign-memory digest not re-assembled in sprint-plan (architecture phase already noted existing digest context sufficient per R-0105; US-0117 documentation-only). DC resolution noted in T-anch NO-OP for traceability.

Sovereign-loop pattern for curator retrospective at segment close: "phase & role governance family operator documentation completes the US-0113 / US-0114 / US-0115 / US-0116 / US-0117 umbrella quint under `## Commands and workflow`; cross-story byte-stability contract now covers **four** prior released blocks (US-0113 L1682 + US-0114 L1806 + US-0115 L1878 + US-0116 L2225) — net-new-keys-only + cross-link-pointer + reason-code-only + prose-only shape is the established quint-closure pattern; US-0117 is the first 5-cumulative-surface story and the final deferred-candidate resolution point (36 architecture.md h1 anchors RESOLVED in `/architecture`, T-anch in S0117 = NO-OP / verification)."

## Risks and mitigations (carried from architecture)

| ID | Risk | Severity | Sprint guard |
|----|------|----------|--------------|
| R1 | AC-3 byte-stability (5th-story cumulative surface — first 5-cumulative-surface story) — US-0117 is the fifth story to extend `### Full scratchpad reference`; cumulative surface now covers 4 prior released blocks (US-0113 L1682 + US-0114 L1806 + US-0115 L1878 + US-0116 L2225). Risk of accidentally editing a prior released block. | MEDIUM | T-003 mandates **net-new-keys-only (46 keys) + cross-link-pointer + reason-code-only (9) + prose-only (7) shape** (architecture lock); US-0113/US-0114/US-0115/US-0116 keys blocks byte-stability preserved. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2225 range. QA re-verifies. Mirrors S0114/S0115/S0116 retrospective pattern extended to 5th story. |
| R2 | AC-5 parity lockstep — `its_magic/README.md` edited but `template/its_magic/README.md` not synced (or vice versa) | MEDIUM | T-004 mandates one-way copy `its_magic/README.md` → `template/its_magic/README.md` after T-001/T-002/T-003 complete. Execute-phase runs `python -c "a=open(r'its_magic/README.md','rb').read(); b=open(r'template/its_magic/README.md','rb').read(); print('PARITY_OK' if a==b else 'PARITY_DIFF')"` (expect `PARITY_OK`) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`). QA re-verifies. |
| R3 | AC-7 anchor gaps + labeling ambiguities — 18 features; two labeling corrections (US-0082 = Codebase map; US-0090 = Caveman input compression) + one US-id collision (runbook `## Caveman mode (US-0089)` L2032 vs 18-feature family US-0089 = Auto orchestration) | MEDIUM | R-0105 closed all anchor gaps (all 18 features have verified runbook anchors). Labeling corrections LOCKED in T-002. US-0089 title resolution LOCKED: `#### US-0089` subsection = "Auto orchestration" (NOT "Caveman mode"). |
| R4 | AC-8 regression tests — coverage parity contract tests weakened or failing | LOW–MEDIUM | US-0117 is documentation-only; **forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` in execute-phase. If a test fails, fix prose, never relax test. T-006 confirms green. |
| R5 | DC anchor resolution (first-time in `/architecture`) — 36 h1 anchors + `## US-0117` added in `/architecture` phase; T-anch in this sprint = NO-OP / verification | LOW (mitigated by architecture-phase resolution) | T-anch NO-OP / verification task confirms the 36 anchors + `## US-0117` section already exist in `docs/engineering/architecture.md` (L1568–L1708). No execute-phase write to architecture.md. QA re-verifies via grep. |
| R6 | AC-2 18-subsection scope size — 2–4× prior stories' T-002 load | MEDIUM | Keep T-002 as a single task with 18 subsections (mirror prior stories' pattern; dev subagent can handle 18 subsections — it's documentation, not code). Split only if dev subagent progress stalls. |
| R7 | AC-4 encoding hygiene prerequisite (carried from US-0114) — 185 stray `0xa7` (section sign) bytes in working-tree `docs/product/backlog.md` per R-0102 / R-0103 / R-0104 / R-0105 | MEDIUM (carried) | Sprint-plan phase is read-only on backlog.md. Flag to orchestrator: restore backlog.md encoding hygiene before execute so AC-4 can be re-verified post-execute. NOT a US-0117 blocker. |
| R8 | US-0087 key surface size — 18 net-new key rows (largest in family) | MEDIUM | Angle boundary with US-0088 / US-0092 (US-0116 family, cross-link only) explicit. T-003 groups US-0087 keys under one sub-heading. |
| R9 | Decomposition drift — Drain mutex (US-0117 is the last story; no successor in this drain) | LOW | Bounded by angle-distinct narrative contract; US-0117 owns phase & role governance feature operator guides only. |

## Definition of done

- All 8 acceptance criteria covered surjectively (AC-1..AC-8 → T-001..T-006) + DC resolution verified (T-anch NO-OP / verification).
- T-anch + T-001..T-006 executed in dependency order; all exit criteria met.
- T-anch confirms 36 anchors + `## US-0117` section already exist in `docs/engineering/architecture.md` (no execute-phase write).
- `python -m pytest tests/scratchpad_example_parity_test.py -q` → 4 passed (no test weakenings).
- `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]` (exit 0).
- `python -c "a=open(r'its_magic/README.md','rb').read(); b=open(r'template/its_magic/README.md','rb').read(); print('PARITY_OK' if a==b else 'PARITY_DIFF')"` → `PARITY_OK`.
- `python scripts/check_intake_template_parity.py` → `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`.
- `python scripts/validate_doc_profile.py` → PASS.
- `python scripts/check-user-visible-metadata.py` → PASS.
- `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2225 range (no removals/modifications to US-0113's L1682, US-0114's L1806, US-0115's L1878, or US-0116's L2225 blocks).
- `git diff HEAD -- docs/engineering/architecture.md` shows no execute-phase edits (T-anch NO-OP — 36 anchors + `## US-0117` section already added in `/architecture` phase).
- `docs/product/backlog.md` `## US-0117` retains **OPEN** through execute / qa / verify-work; closure at `/release` (US-0045).

## Next phase

Per **ultra_lean**, the orchestrator routes to the **`build+verify` macro** — `/execute` (dev, first canonical phase of `build+verify`), which then chains to `/qa` (merges plan-verify + execute QA + verify-work). Plan-verify is NOT a standalone phase in ultra_lean.

**Handoff**: `handoffs/po_to_tl.md` (sprint-plan handoff block prepended per ultra_lean artifact convention — orchestrator reads the topmost block).

**Stop**: sprint-plan complete; do not spawn the next phase. Orchestrator Task-spawns dev for `/execute`.
