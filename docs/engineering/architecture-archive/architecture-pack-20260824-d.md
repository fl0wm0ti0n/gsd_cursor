# Architecture archive pack (2026-08-24)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3000, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 10
- Retained units in hot file: 40
- First archived heading: `## US-0117 — Phase & role governance operator documentation in framework README`
- Last archived heading: `## US-0079 — Bug queue routing`
- Verification tuple (mandatory):
  - archived_body_lines=184
  - preamble_lines=1
  - retained_body_lines=3000

---

## US-0117 — Phase & role governance operator documentation in framework README

### Overview

**US-0117** is a documentation-only story closing the operator-documentation gap for the **phase & role governance** functional family — the LARGEST family in the 5-story drain (18 features: US-0069, US-0070, US-0071, US-0072, US-0075, US-0076, US-0077, US-0078, US-0079, US-0080, US-0081, US-0082, US-0083, US-0085, US-0087, US-0088, US-0089, US-0090). It adds the **5th sibling umbrella** `### Phase & role governance (US-0069 / US-0070 / US-0071 / US-0072 / US-0075 / US-0076 / US-0077 / US-0078 / US-0079 / US-0080 / US-0081 / US-0082 / US-0083 / US-0085 / US-0087 / US-0088 / US-0089 / US-0090) umbrella section` under `## Commands and workflow` (L350) in `its_magic/README.md`, as a sibling to US-0113's `### Sovereign-loop era` (L940), US-0114's `### Release & distribution` (L1225), US-0115's `### Integration & observability` (L1410), and US-0116's `### Delivery & lifecycle` (L1665) umbrellas, inserted after US-0116's umbrella close (before L1665 `### Full scratchpad reference (detailed)`). The umbrella carries 18 nested per-feature `#### US-xxxx` operator subsections ordered US-id-ascending. A matching `### Phase & role governance keys (US-0069 / ... / US-0090)` sub-block is appended to `### Full scratchpad reference (detailed)` (L1665) as the **5th sibling** to US-0113's `### Sovereign-loop era keys` (L1682), US-0114's `### Release & distribution keys` (L1806), US-0115's `### Integration & observability keys` (L1878), and US-0116's `### Delivery & lifecycle keys` (L2225), inserted after US-0116's keys block close (before `### Remote execution config`). The sub-block covers **46 net-new key rows** across 10 features (US-0069/0070/0079/0080/0081/0083/0087/0088/0089/0090) + **9 reason-code-only entries** (7 features) + **7 prose-only / runbook-cross-link-only entries** (US-0071/0072/0075/0076/0077/0078/0085) + **cross-link pointers** (`DELIVERY_MODE` -> US-0114 L1806; `LEAN_MEMORY_*` -> US-0115 L1877 default omit; `TOKEN_PROFILE` -> main reference list + US-0080 subsection; `CODEBASE_MAP_REFRESH_ON_ROLLOVER` -> US-0082 subsection). Two labeling corrections locked: US-0082 = **Codebase map** (per runbook L63 + DEC-0065; spec handoff's "Input compression" is a mislabel); US-0090 = **Caveman input compression** (per runbook L2099 + DEC-0073; spec handoff's "Phase governance integration" is a mislabel — "phase governance integration" is the umbrella's introductory framing AC-1, not a separate `#### US-0090` subsection). US-0089 = **Auto orchestration** (per scratchpad L21/L135 + 18-feature family; note US-id collision with runbook h2 `## Caveman mode (US-0089)` L2032 — `/architecture` locks the resolution: the `#### US-0089` subsection title is "Auto orchestration", NOT "Caveman mode"). The framework README pair (`its_magic/README.md` <-> `template/its_magic/README.md`) is kept byte-identical via one-way copy. No code, schema, installer, scratchpad canonical, or runbook content changes.

**Binding decision**: **companion_dec=none** (US-0117 is documentation-only; no architectural, policy, or schema surface is being changed; R-0105 § Decision-gate check confirmed no DEC required — mirrors US-0113 / US-0114 / US-0115 / US-0116 sibling precedent; grep `^## DEC-` in `docs/engineering/decisions.md` returned no US-0117 companion DEC). **Research anchor**: **R-0105** (delivered 2026-07-04T16:54:35Z, 8/8 open questions closed; 18 per-feature sub-findings; AC-3 approach locked; DC-1..DC-4 confirmed = 18 deferred + 18 own = 36 total h1 anchors to add in `/architecture`; AC baselines green; deepened risks). **Compose guards (non-negotiable, 23 — UNCHANGED, cumulative across all prior stories — same 23 as US-0116)**: DO NOT amend US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062. **Status authority**: **OPEN** per **US-0045** (closure at `/release`).

**Fresh context marker**: `tl-US0117-architecture-20260704T171500Z-fresh`
**Orchestrator run id**: `auto-20260704-01`
**Timestamp**: 2026-07-04T17:15:00Z (UTC)
**Verdict**: PASS
**Next**: `/sprint-plan`

### Companion DEC

**companion_dec = none**. US-0117 is documentation-only (mirrors US-0113 / US-0114 / US-0115 / US-0116 sibling precedent). No architectural, policy, or schema surface is being changed. Grep for `^## DEC-` in `docs/engineering/decisions.md` returned no matches — confirmed no US-0117 companion DEC is required and none was proposed in R-0105 § Decision-gate check. The DC-1+DC-2+DC-3+DC-4 resolution (36 h1 anchors added in THIS phase) is a triad-hygiene closure, not a tradeoff requiring a DEC.

### Approach locked (A1)

**Approach A1** (locked): Single `### Phase & role governance` umbrella + 18 nested `#### US-xxxx` subsections (h4 under h3 umbrella), sibling to US-0113's `### Sovereign-loop era`, US-0114's `### Release & distribution`, US-0115's `### Integration & observability`, and US-0116's `### Delivery & lifecycle` umbrellas, inserted after US-0116's umbrella under `## Commands and workflow`. Consistency with prior 4 stories.

| Option | Summary | Verdict |
|--------|---------|---------|
| **A1** | **Single umbrella + 18 nested subsections + 5th scratchpad ref sub-block** (net-new keys + cross-link pointers + reason-code-only + prose-only) | **Preferred** — matches US-0113 / US-0114 / US-0115 / US-0116 sibling precedent (5th sibling). |
| A2 (rejected) | Reuse an existing phase governance README section as umbrella and nest the other 17 features under it. | **Rejected** — pre-US-0117 README surfaces for phase/role keys (`### Automation modes` L880, `### Sync policy (US-0038)` L909, `### Optional /auto backlog-drain mode (US-0044)` L2370) are feature-mode blocks, not family-grouping blocks; elevating any one to umbrella-holder conflates a feature section with a family section, breaks byte-stability of pre-US-0117 blocks, and breaks the family-parity contract (prior 4 stories each have a dedicated umbrella header). Several US-0117 features (US-0069 / US-0070 / US-0071 / US-0075 / US-0077 / US-0085) have no pre-US-0117 README section at all. |
| A3 (rejected) | Split the 18 features across 2 umbrellas ("phase governance" + "role governance"). | **Rejected** — breaks the 5-sibling parity contract (prior 4 stories each have ONE umbrella per family); the 18 features form one coherent family per backlog.md US-0117 decomposition (US-0051); splitting would fragment the operator catalog. |

### Files to touch

- `its_magic/README.md` — APPEND umbrella `### Phase & role governance (US-0069 / ... / US-0090) umbrella section` (after US-0116 umbrella close, before L1665 `### Full scratchpad reference (detailed)`) + 18 nested `#### US-xxxx` operator subsections (US-0069 -> US-0070 -> US-0071 -> US-0072 -> US-0075 -> US-0076 -> US-0077 -> US-0078 -> US-0079 -> US-0080 -> US-0081 -> US-0082 -> US-0083 -> US-0085 -> US-0087 -> US-0088 -> US-0089 -> US-0090) + `### Phase & role governance keys (US-0069 / ... / US-0090)` sub-block under `### Full scratchpad reference (detailed)` (after US-0116's `### Delivery & lifecycle keys` block at L2225; before `### Remote execution config`). Sub-block covers 46 net-new key rows + 9 reason-code-only entries + 7 prose-only / runbook-cross-link-only entries + cross-link pointers.
- `template/its_magic/README.md` — byte-identical one-way copy of `its_magic/README.md` (AC-5 parity; T-004).

### Files NOT to touch

- `.cursor/scratchpad.md` — canonical scratchpad; US-0117 documents keys in README, never edits the canonical source.
- `template/.cursor/scratchpad.local.example.md` — framework parity file; US-0117 does not extend the example scratchpad (AC-3 extension is in README only).
- `docs/product/backlog.md` — status authority; US-0117 remains OPEN until `/release`.
- `docs/engineering/runbook.md` — AC-7 cross-links only (no runbook edits; US-0117 points TO existing runbook anchors, never edits them).
- `docs/developer/README.md` — US-0097 compose guard.
- `docs/engineering/architecture.md` — **other than this `## US-0117` append + the 36 DC anchors appended below**, no edits. Execute-phase does NOT add h1 anchors.
- `installer.py` / `installer.ps1` / `installer.sh` / `scripts/*` — no code or installer changes (US-0117 documentation-only).
- `tests/scratchpad_example_parity_test.py` — AC-8 regression test; forbid edits.
- **Do NOT modify US-0113's `### Sovereign-loop era` / `### Sovereign-loop era keys` blocks (L940 / L1682), US-0114's `### Release & distribution` / `### Release & distribution keys` blocks (L1225 / L1806), US-0115's `### Integration & observability` / `### Integration & observability keys` blocks (L1410 / L1878), or US-0116's `### Delivery & lifecycle` / `### Delivery & lifecycle keys` blocks (L1665 / L2225)** in `its_magic/README.md` — byte-stability contract (all 4 already released in S0113 / S0114 / S0115 / S0116). US-0117 adds cross-link pointers to these blocks from its own 5th sub-block; it never edits them. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2225 range (no removals/modifications to US-0113's L1682, US-0114's L1806, US-0115's L1878, or US-0116's L2225 blocks).

### Sprint seeds (T-001..T-006 + T-anch = 7 tasks within SPRINT_MAX_TASKS=12)

| Task | AC | Description | Role |
|------|----|-------------|------|
| **T-anch** | AC-2 / AC-8 | Add 36 `## US-xxxx` h1 anchors to `docs/engineering/architecture.md` (18 own: US-0069/0070/0071/0072/0075/0076/0077/0078/0079/0080/0081/0082/0083/0085/0087/0088/0089/0090 + 18 deferred DC-1+DC-2+DC-3+DC-4: US-0103/0104/0105/0107/0110 + US-0041/0062 + US-0034/0084/0086/0093/0096/0101/0102 + US-0092/0095/0098/0099) + the `# US-0117` anchor (already authored in `/architecture`). Minimal 3–5 line normative sections. **First-time DC anchor addition in architecture phase** (resolved HERE, not deferred to `/execute`). | B |
| **T-001** | AC-1 | Add umbrella `### Phase & role governance (US-0069 / ... / US-0090) umbrella section` under `## Commands and workflow` (after US-0116 umbrella close, before L1665). 18-step enable order (US-id-ascending) + runbook pointer line + zero-overhead-when-off contract line + "phase governance integration" introductory framing (AC-1). | B |
| **T-002** | AC-2 / AC-7 | Add 18 per-feature operator subsections (US-0069 -> US-0090) under the umbrella. Two labeling corrections applied: US-0082 = "Codebase map" (NOT "Input compression"); US-0090 = "Caveman input compression" (NOT "Phase governance integration"); US-0089 = "Auto orchestration" (NOT "Caveman mode" — runbook US-id collision resolved). Each subsection carries AC-7 runbook cross-link. | B |
| **T-003** | AC-3 | Add `### Phase & role governance keys` sub-block under `### Full scratchpad reference (detailed)` (after US-0116 L2225 block). 46 net-new key rows (10 features) + 9 reason-code-only entries (7 features) + 7 prose-only / runbook-cross-link-only entries (US-0071/0072/0075/0076/0077/0078/0085) + cross-link pointers (`DELIVERY_MODE` -> US-0114; `LEAN_MEMORY_*` -> US-0115 default omit; `TOKEN_PROFILE` -> main ref + US-0080; `CODEBASE_MAP_REFRESH_ON_ROLLOVER` -> US-0082). 5th-story cumulative byte-stability surface — prior 4 blocks byte-identical. | B |
| **T-004** | AC-5 | Sync `template/its_magic/README.md` byte-identical to `its_magic/README.md` (one-way copy). Verify `PARITY_OK <size> <size>`. | B |
| **T-005** | AC-4 / AC-6 | Run validators: `python scripts/validate_readme_feature_coverage.py --repo . --enforce` -> `[README_FEATURE_COVERAGE_VALIDATE_OK]` with `coverage_missing=["US-0117"]` unchanged (US-0117 not in catalog surface). `python scripts/validate_doc_profile.py --repo .` + `python scripts/check-user-visible-metadata.py --repo .` + `python scripts/check_intake_template_parity.py --repo .` -> expect PASS. Fix any narrative prose leaking internal IDs. | B |
| **T-006** | AC-8 | Run regression tests: `python -m pytest tests/scratchpad_example_parity_test.py -v` -> 4 passed. Forbid edits to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, `tests/scratchpad_example_parity_test.py`. | B |

**Execution order**: T-anch -> T-001 -> T-002 -> T-003 -> T-004 -> T-005 -> T-006. Acyclic. (T-anch first because it is on `architecture.md`, not `its_magic/README.md`; doing it first keeps the README byte-stability surface clean for subsequent T-001..T-004.)

### Test markers (5 — same as prior stories)

- `tests/scratchpad_example_parity_test.py` (4 tests)
- `scripts/validate_readme_feature_coverage.py --enforce`
- `scripts/validate_doc_profile.py`
- `scripts/check-user-visible-metadata.py`
- `scripts/check_intake_template_parity.py`

### Compose guards UNCHANGED (23 cumulative — same 23 as US-0116)

US-0117 is documentation-only and lives entirely outside the compose surface. The 23 compose guards (cumulative across all prior stories — US-0117 adds no new family-internal guards because all 18 in-scope features are phase & role governance operators, not compose-surface features) remain UNCHANGED:

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062.

### DC-1 + DC-2 + DC-3 + DC-4 resolution (final deferred-candidate resolution point)

US-0117 is the **final story in the 5-story drain** and the **final deferred-candidate resolution point** for the architecture.md triad hygiene closure. It inherits 18 missing `# US-xxxx` h1 anchors from prior released stories AND owns 18 anchors for its own features (also missing — confirmed by grep in R-0105). Total h1 anchors added in THIS `/architecture` phase: **36** (18 own + 18 deferred).

- **DC-1** (5, from US-0113): US-0103, US-0104, US-0105, US-0107, US-0110 (sovereign-loop era family).
- **DC-2** (2, from US-0114): US-0041, US-0062 (release & distribution family).
- **DC-3** (7, from US-0115): US-0034, US-0084, US-0086, US-0093, US-0096, US-0101, US-0102 (integration & observability family).
- **DC-4** (4, from US-0116): US-0092, US-0095, US-0098, US-0099 (delivery & lifecycle family).
- **18 own** (US-0117 family): US-0069, US-0070, US-0071, US-0072, US-0075, US-0076, US-0077, US-0078, US-0079, US-0080, US-0081, US-0082, US-0083, US-0085, US-0087, US-0088, US-0089, US-0090.

**First time the architecture phase adds DC anchors** (prior 4 stories deferred them to US-0117). Resolution approach (Q-2 LOCKED in R-0105): add in `/architecture`, NOT `/execute` — keeps anchors as architecture artifacts per `docs/engineering/artifact-ownership-policy.md`. NOT appended to `handoffs/sovereign_deferrals.jsonl` — the anchors ARE being resolved in this phase. Each anchor is a minimal 3–5 line normative section; full architectural content for each feature remains in their original DEC / R-xxxx entries. Anchor format: `## US-xxxx — <feature title>` (matching existing `## US-0115` / `## US-0116` format). The 36 anchors are appended below this `## US-0117` section.

### Risks finalized

| Risk | Severity | Mitigation |
|------|----------|------------|
| **AC-3 byte-stability (5th-story cumulative surface — first 5-cumulative-surface story)** — US-0117 is the fifth story to extend `### Full scratchpad reference`; cumulative surface now covers 4 prior released blocks (US-0113 L1682 + US-0114 L1806 + US-0115 L1878 + US-0116 L2225). Risk of accidentally editing a prior released block. | **MEDIUM** | Net-new-keys-only (46 keys) + cross-link-pointer + reason-code-only (9) + prose-only (7) shape LOCKED in `/architecture` (T-003). Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2225 range (no removals/modifications to US-0113's L1682, US-0114's L1806, US-0115's L1878, or US-0116's L2225 blocks). QA re-verifies. Mirrors S0114 / S0115 / S0116 retrospective pattern extended to 5th story. |
| **AC-5 parity lockstep** — `template/its_magic/README.md` must be byte-identical to `its_magic/README.md`. | **MEDIUM** | T-004 one-way copy + `PARITY_OK <size> <size>` byte-parity check. |
| **AC-7 anchor gaps + labeling ambiguities** — 18 features; two labeling corrections (US-0082 = Codebase map; US-0090 = Caveman input compression) + one US-id collision (runbook `## Caveman mode (US-0089)` L2032 vs 18-feature family US-0089 = Auto orchestration). | **MEDIUM** | R-0105 closed all anchor gaps (all 18 features have verified runbook anchors). Labeling corrections LOCKED in T-002. US-0089 title resolution LOCKED: `#### US-0089` subsection = "Auto orchestration" (NOT "Caveman mode"). |
| **AC-8 regression tests** — coverage parity contract tests weakened or failing. | **LOW–MEDIUM** | US-0117 is documentation-only; **forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` in execute-phase. If a test fails, fix prose, never relax test. T-006 confirms green. |
| **DC anchor resolution (first-time in `/architecture`)** — 36 h1 anchors + `# US-0117` to add in `/architecture`; ~1670 lines post-addition, under 3000-line cap. | **MEDIUM** | T-anch adds all 36 anchors in `/execute` (task seeded HERE, executed in build+verify macro). Architecture phase authors the `# US-0117` section + the 36 anchor stubs (appended below) as the normative contract; execute-phase materializes them in `architecture.md` if not already present. **Mitigation**: anchors appended in THIS phase (resolved here, not deferred further). |
| **AC-2 18-subsection scope size** — 2–4x prior stories' T-002 load. | **MEDIUM** | Keep T-002 as a single task with 18 subsections (mirror prior stories' pattern; dev subagent can handle 18 subsections — it's documentation, not code). Split only if dev subagent progress stalls. |
| **AC-4 encoding hygiene prerequisite (carried from US-0114)** — 185 stray `0xa7` (section sign) bytes in working-tree `docs/product/backlog.md` per R-0102 / R-0103 / R-0104 / R-0105. | **MEDIUM (carried)** | `/architecture` makes no backlog.md edits. Flag to orchestrator: restore backlog.md encoding hygiene before execute so AC-4 can be re-verified post-execute. NOT a US-0117 blocker (research + architecture are read-only on backlog.md). |
| **US-0087 key surface size** — 18 net-new key rows (largest in family). | **MEDIUM** | Angle boundary with US-0088 / US-0092 (US-0116 family, cross-link only) explicit. T-003 groups US-0087 keys under one sub-heading. |
| **Decomposition drift** — Drain mutex (US-0117 is the last story; no successor in this drain). | **LOW** | Bounded by angle-distinct narrative contract; US-0117 owns phase & role governance feature operator guides only. |

### Stop conditions met

- **No DEC required** — confirmed (US-0117 documentation-only; mirrors US-0113 / US-0114 / US-0115 / US-0116 sibling precedent; grep `^## DEC-` returned no matches).
- **No feasibility unknown** — R-0105 closed all 8 spec open questions (Q1–Q8); AC-3 approach locked; DC resolution approach locked (Q-2); key surface resolved via scratchpad grep (Q-3); 5th-story byte-stability contract locked (Q-8).
- **No data migration risk** — US-0117 is documentation-only; no schema, installer, or canonical-file migration.

**No DECISION_GATE raised.** Architecture phase revealed no question requiring operator input. DC-1+DC-2+DC-3+DC-4 resolved by tech-lead within the `plan` macro (36 h1 anchors added in THIS phase). No sovereign-memory digest call needed (US-0117 is documentation-only; existing digest context sufficient per R-0105 — S0113 / S0114 / S0115 / S0116 retrospectives established the reusable patterns applied here; the cross-link pointer pattern + angle-distinct narrative pattern + cross-story byte-stability contract now form a quad scaled to the 5th story). Verdict: **PASS**.

### Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called (US-0117 documentation-only; existing digest context sufficient per R-0105). Sovereign-loop pattern for curator retrospective at segment close: "phase & role governance family operator documentation completes the US-0113 / US-0114 / US-0115 / US-0116 / US-0117 umbrella quint under `## Commands and workflow`; cross-story byte-stability contract now covers **four** prior released blocks (US-0113 L1682 + US-0114 L1806 + US-0115 L1878 + US-0116 L2225) — net-new-keys-only + cross-link-pointer + reason-code-only + prose-only shape is the established quint-closure pattern; US-0117 is the first 5-cumulative-surface story and the final deferred-candidate resolution point (36 architecture.md h1 anchors added). No write to `mistakes.jsonl` in architecture phase.

### Consequences

- Sprint: S0117 (pending `/sprint-plan`).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.
- Framework README pair grows by umbrella + 18 subsections + scratchpad reference extension (both `its_magic/README.md` and `template/its_magic/README.md` byte-identical).
- **36 architecture.md h1 anchors RESOLVED in this phase** (18 own + 18 deferred DC-1+DC-2+DC-3+DC-4) — final deferred-candidate resolution point. Appended below.
- No new tests; no new DECs; no compose-surface changes.

### Evidence references

- `docs/product/backlog.md` — `## US-0117` block (lines 3965–3981, 8 ACs)
- `docs/engineering/research.md` — `R-0105` (delivered 2026-07-04T16:54:35Z, 8/8 open questions closed; 18 per-feature sub-findings; AC-3 approach locked; DC-1..DC-4 confirmed = 36 total; AC baselines green; deepened risks)
- `handoffs/po_to_tl.md` — research handoff (topmost block) + spec handoff
- `docs/engineering/state.md` — research checkpoint (latest) + architecture checkpoint (this phase, appended)
- `handoffs/resume_brief.md` — top block updated to reflect architecture complete
- `.cursor/scratchpad.md` — phase & role governance keys (L21/L89–91 role overrides, L102–105 phase plan, L77–80 bug queue, L11–22 auto loop, L30–38 full-autonomy, L41–56 backlog drain, L63 active, L135 orchestration, L201 release publish, L295–298 dev auto-launch) — canonical source for AC-3 extension (net-new + cross-links)
- `its_magic/README.md` — L350 (`## Commands and workflow`) umbrella target; L940 (US-0113 sibling umbrella — byte-stability preserved); L1225 (US-0114 sibling umbrella — byte-stability preserved); L1410 (US-0115 sibling umbrella — byte-stability preserved); L1665 (US-0116 sibling umbrella + `### Full scratchpad reference (detailed)` extension target); L1682 (US-0113 keys block — byte-stability preserved); L1806 (US-0114 keys block — byte-stability preserved + cross-link target for `DELIVERY_MODE`); L1878 (US-0115 keys block — byte-stability preserved + optional cross-link target for `LEAN_MEMORY_*`); L2225 (US-0116 keys block — byte-stability preserved + insertion point for `### Phase & role governance keys` sub-block); L880 / L909 / L2370 (pre-US-0117 grouped cross-link targets for `AUTO_BACKLOG_DRAIN` / `AUTO_BUG_QUEUE` family)
- `docs/engineering/runbook.md` — 18 anchors (per R-0105 § Per-feature sub-findings): US-0069 L1711 h2; US-0070 L1753 h2; US-0071 L303 h2; US-0072 L550 h2; US-0075 L1949 h3 + L2535 h2; US-0076 L63 h2; US-0077 L98 h2; US-0078 L479 h2; US-0079 L512 h2; US-0080 L550 h2 + L570 h3; US-0081 L2032 h3; US-0082 L63 h2; US-0083 L479 h2 + L591 h3; US-0085 L1628 h2; US-0087 L1809 h2 + L1958 h3; US-0088 L1838 h2; US-0089 L1398 h3 + L1838 h2; US-0090 L2099 h3
- `docs/engineering/architecture.md` — h1 inventory confirmed: `# US-0106` (L2), `# US-0108` (L120), `# US-0109` (L220), `# US-0111` (L335), `# US-0112` (L454), `# US-0113` (L717), `# US-0114` (L914), `## US-0115` (L1117), `## US-0116` (L1265) exist; `## US-0117` + 36 DC anchors added in THIS phase (appended below)
- `docs/engineering/decisions.md` — DEC-0051 (US-0069 phase-role), DEC-0052 (US-0070 phase plan), DEC-0053 (US-0071 metadata guard), DEC-0035 (US-0080 / US-0072 token profile), DEC-0039 / DEC-0057 (US-0075 scratchpad parity), DEC-0065 (US-0082 codebase map), DEC-0059 / DEC-0067 (US-0077 delegation), DEC-0060 (US-0078 env file), DEC-0061 (US-0079 bug queue), DEC-0073 (US-0090 caveman input compression), DEC-0029 (US-0085 fresh-context markers), DEC-0078 (US-0087 full-autonomy), DEC-0038 (runtime proof) — referenced, not amended; no US-0117 companion DEC (grep `^## DEC-` returned no matches)

### Isolation evidence (per US-0048 / DEC-0029)

Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to artifact files (narrow-read per US-0053 — research.md R-0105 entry only, po_to_tl.md top research handoff block, backlog.md US-0117 block L3965–3981, state.md US-0117 research checkpoint, resume_brief.md top ~30 lines, architecture.md grep US-0113..US-0117 + DC-1..DC-4 anchors, decisions.md grep `^## DEC-`). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python timestamp/hash computation. `assemble_sovereign_memory_digest(...)` NOT called (US-0117 documentation-only; existing digest context sufficient per R-0105). No write to `mistakes.jsonl` in architecture phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).

### Strict runtime proof (DEC-0038)

- **runtime_proof_id**: `rp-auto-20260704-01-architecture-techlead-20260704T171500Z-US-0117`
- **canonical_payload** (sorted-key JSON per DEC-0038): `{"approach_locked":"A1","companion_dec":"none","delivery_mode":"ultra_lean","dc_anchors_added":36,"macro_phase":"plan","orchestrator_run_id":"auto-20260704-01","phase_id":"architecture","proof_issued_at":"2026-07-04T17:15:00Z","proof_ttl_seconds":3600,"research_anchor":"R-0105","role":"tech-lead","story_id":"US-0117","verdict":"PASS"}`
- **proof_ttl**: 2026-07-04T18:15:00Z (1-hour TTL per DEC-0038)

---

### 36 DC anchors (appended below — minimal normative sections)

The following 36 `## US-xxxx` h1 anchors are added in THIS `/architecture` phase as the final deferred-candidate resolution. Each is a minimal 3–5 line normative section; full architectural content for each feature remains in their original DEC / R-xxxx entries. 18 own (US-0117 family) + 18 deferred (DC-1 from US-0113 + DC-2 from US-0114 + DC-3 from US-0115 + DC-4 from US-0116).

## US-0069 — Phase→role matrix

Story US-0069 — Phase→role matrix. Per-phase role admission + checkpoint validation + per-role override (`AUTO_ROLE_RESEARCH` / `AUTO_ROLE_PLAN_VERIFY` / `AUTO_ROLE_REFRESH_CONTEXT`). Fail-closed on mismatch. See `# US-0117` for the operator documentation angle. Binding: DEC-0051; runbook `## Strict /auto phase→role enforcement (US-0069 / DEC-0051)` L1711 h2.

## US-0070 — Phase selection policy

Story US-0070 — Phase selection policy. Resolved ordered phase plan via `AUTO_PHASE_PLAN` / `AUTO_PHASE_EXCLUDE` / `AUTO_PHASE_INCLUDE` / `AUTO_PHASE_PROFILE`; exactly-one-active-mode after merge; conflict -> fail closed (`PHASE_POLICY_CONFLICT` / `PHASE_PLAN_UNKNOWN_PHASE`). See `# US-0117`. Binding: DEC-0052; runbook `## Configurable /auto phase plan (US-0070 / DEC-0052)` L1753 h2.

## US-0071 — Metadata sanitization

Story US-0071 — Metadata sanitization. Validator gate (not a runtime toggle): `scripts/check-user-visible-metadata.py` forbids internal IDs (DEC-xxxx / R-xxxx / reason-codes) in user-visible prose; US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. See `# US-0117`. Binding: DEC-0053; runbook `## User-visible internal metadata guard (US-0071 / DEC-0053)` L303 h2.

## US-0072 — Context slimming

Story US-0072 — Context slimming. Concept of context compaction / token-cost control; runtime toggle is `TOKEN_PROFILE=lean|balanced|full` (DEC-0035, owned by US-0080) + `LEAN_MEMORY_*` family (DEC-0082, owned by US-0115). See `# US-0117`. Binding: DEC-0035; runbook `## Context compaction and token profile mode (US-0053 / DEC-0035)` L550 h2 (shared with US-0080).

## US-0075 — Scratchpad example-first refresh

Story US-0075 — Scratchpad example-first refresh. Parity-contract feature materialized via `tests/scratchpad_example_parity_test.py` + `installer.py materialize_scratchpad_example()`; canonical `.cursor/scratchpad.md` <-> `template/.cursor/scratchpad.local.example.md` byte-parity. See `# US-0117`. Binding: DEC-0039 / DEC-0057; runbook `### Scratchpad example parity` L1949 h3 + `## Scratchpad example upgrade contract (US-0057 / DEC-0039 / DEC-0057)` L2535 h2.

## US-0076 — Codebase map (freshness gate)

Story US-0076 — Codebase map freshness gate. Freshness gate on `docs/engineering/codebase-map.md`; runtime toggle `CODEBASE_MAP_REFRESH_ON_ROLLOVER=1` (default off) owned by US-0082's bootstrap-mechanism narrative. See `# US-0117` and `## US-0082`. Binding: DEC-0065; runbook `## Codebase map bootstrap (US-0082 / DEC-0065)` L63 h2 (shared with US-0082).

## US-0077 — Delegation policy

Story US-0077 — Delegation policy. Intake-evidence delegation path: `topic_coverage[].satisfied_by=delegation_ref` + required `delegation_scope` / `delegation_rationale` / `delegation_confidence`; fail-closed on missing/malformed (`INTAKE_DELEGATION_EVIDENCE_MISSING`). See `# US-0117`. Binding: DEC-0059 / DEC-0067; runbook `## Documentation profile validation (US-0077 / DEC-0059)` L98 h2.

## US-0078 — Env file bootstrap (intake evidence harness)

Story US-0078 — Env file bootstrap. Install-time copy-when-missing mechanism for intake-evidence env file; harness contract (validator + installer). See `# US-0117` and `## US-0083`. Binding: DEC-0060; runbook `## Interactive intake evidence validation (US-0078 / DEC-0060 / US-0083 / DEC-0067)` L479 h2 (shared with US-0083).

## US-0079 — Bug queue routing

Story US-0079 — Bug queue routing. Bug-targeted `/auto` via `AUTO_BUG_QUEUE` / `AUTO_BUG_TARGET` / `AUTO_BUG_MAX_ITEMS` / `AUTO_BUG_ON_BLOCK`; mutex vs `AUTO_BACKLOG_DRAIN` without bug-target argv; `AUTO_BUG_TARGET=all-open|BUG-####` required when `AUTO_BUG_QUEUE=1`. See `# US-0117`. Binding: DEC-0061; runbook `## Bug issues (US-0079 / DEC-0061)` L512 h2.

