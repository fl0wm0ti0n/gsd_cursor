# po_to_tl archive pack (2026-07-04-c)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Rollover pass: 1 (US-0117 refresh-context terminal - final story in 5-story drain)
- Archived handoffs (oldest first, contiguous suffix): 4 (US-0117 lifecycle - sprint-plan, architecture, research, spec; US-0113/US-0114/US-0115 lifecycles already archived in po-to-tl-pack-20260704-a/b.md; US-0116 lifecycle handoffs were lost in a git checkout HEAD recovery event during US-0116 refresh-context - authoritative US-0116 record in sprints/S0116/)
- Retained handoffs in hot file: 0 (post-rollover pre-append; minimal preamble only - US-0117 was the final story in the 5-story drain, no next-story handoff to retain)
- First archived heading: `# Sprint-plan handoff — US-0117 / auto-20260704-01 (sprint-plan PASS tl, next `/execute` dev — plan-verify merged into qa per ultra_lean)`
- Last archived heading: `# Spec handoff — US-0117 / auto-20260704-01 (intake + discovery merged)`
- Verification tuple (mandatory):
  - archived_body_lines=1915
  - preamble_lines=0 (file starts at line 1 with first handoff H1)

---

# Sprint-plan handoff — US-0117 / auto-20260704-01 (sprint-plan PASS tl, next `/execute` dev — plan-verify merged into qa per ultra_lean)

**Date**: 2026-07-04
**Phase**: sprint-plan (third canonical phase of `plan` macro per ultra_lean)
**Role**: tech-lead
**Story**: US-0117 — Phase & role governance operator documentation in framework README
**orchestrator_run_id**: auto-20260704-01
**delivery_mode**: ultra_lean
**macro_phase**: plan (sprint-plan)
**fresh_context_marker**: tl-US0117-sprint-plan-20260704T172645Z-fresh
**timestamp**: 2026-07-04T17:26:45Z (UTC)
**verdict**: PASS
**next_scheduled_phase**: execute (dev — first canonical phase of `build+verify` macro; plan-verify merged into qa per ultra_lean)
**default_spawn_role**: dev

## Summary

**`/sprint-plan`** **PASS** — **US-0117** sprint plan locked. **Sprint S0117** materialized with **7 tasks** (T-anch + T-001..T-006) within `SPRINT_MAX_TASKS=12`. **T-anch = NO-OP / verification** (the 36 `## US-xxxx` h1 anchors + `## US-0117` section were already added in the `/architecture` phase per R-0105 Q-2 LOCKED — "resolve in `/architecture`, NOT `/execute`"; T-anch in this sprint simply verifies the anchors exist at `docs/engineering/architecture.md` L1568–L1708 and that no execute-phase write to architecture.md occurs). **T-001..T-006** mirror the US-0116 ultra_lean pattern (umbrella → 18 subsections → scratchpad ref extension → template byte-sync → validators → regression tests). AC-1..AC-8 surjective coverage confirmed (8 ACs, 7 tasks; multi-AC tasks T-002 (AC-2+AC-7), T-005 (AC-4+AC-6)). **Companion DEC=none** (US-0117 documentation-only; mirrors US-0113/US-0114/US-0115/US-0116 sibling precedent). **23/23 compose guards UNCHANGED** (cumulative — same 23 as US-0116; US-0117 lives entirely outside the compose surface). Status authority: **OPEN** per **US-0045** (closure at `/release`).

US-0117 is the **5th and final story** in the 5-story drain, the LARGEST family (18 features vs 4–9 in prior stories), and the **final deferred-candidate resolution point**. The 5th-story cumulative byte-stability surface covers 4 prior released blocks (US-0113 L1682 + US-0114 L1806 + US-0115 L1878 + US-0116 L2225) — contract pattern scales to the 5th story without regression (net-new-keys-only + cross-link-pointers + reason-code-only + prose-only shape; 46 net-new key rows + 9 reason-code-only entries + 7 prose-only / runbook-cross-link-only entries). Two labeling corrections LOCKED in T-002: US-0082 = "Codebase map" (NOT "Input compression"); US-0090 = "Caveman input compression" (NOT "Phase governance integration"). US-0089 US-id collision LOCKED in T-002: `#### US-0089` subsection title = "Auto orchestration" (NOT "Caveman mode"; runbook h2 `## Caveman mode (US-0089)` L2032 is the collision — `/architecture` locks the resolution).

## Sprint anchor

- `sprints/S0117/sprint.md` (NEW — ultra_lean sprint plan; 7 tasks; AC-1..AC-8 surjective + DC resolution verified)
- `sprints/S0117/tasks.md` (NEW — 7-task checklist with T-anch as NO-OP / verification)

## Sprint seeds (7 tasks within SPRINT_MAX_TASKS=12)

- **T-anch** (DC resolution — NO-OP / verification): confirm 36 `## US-xxxx` h1 anchors + `## US-0117` section already exist in `docs/engineering/architecture.md` (added in `/architecture` phase per R-0105 Q-2 LOCKED; L1568–L1708). No execute-phase write to architecture.md. T-anch = verification only.
- **T-001** (AC-1): Add umbrella `### Phase & role governance (US-0069 / ... / US-0090) umbrella section` under `## Commands and workflow` (after US-0116 umbrella close, before L1665). 18-step enable order (US-id-ascending) + runbook pointer line + zero-overhead-when-off contract line + "phase governance integration" introductory framing (AC-1).
- **T-002** (AC-2 / AC-7): Add 18 per-feature operator subsections (US-0069 → US-0090) under the umbrella. Two labeling corrections applied: US-0082 = "Codebase map" (NOT "Input compression"); US-0090 = "Caveman input compression" (NOT "Phase governance integration"); US-0089 = "Auto orchestration" (NOT "Caveman mode" — runbook US-id collision resolved). Each subsection carries AC-7 runbook cross-link.
- **T-003** (AC-3): Add `### Phase & role governance keys` sub-block under `### Full scratchpad reference (detailed)` (after US-0116 L2225 block). 46 net-new key rows (10 features) + 9 reason-code-only entries (7 features) + 7 prose-only / runbook-cross-link-only entries (US-0071/0072/0075/0076/0077/0078/0085) + cross-link pointers (`DELIVERY_MODE` → US-0114; `LEAN_MEMORY_*` → US-0115 default omit; `TOKEN_PROFILE` → main ref + US-0080 subsection; `CODEBASE_MAP_REFRESH_ON_ROLLOVER` → US-0082 subsection). 5th-story cumulative byte-stability surface — prior 4 blocks byte-identical.
- **T-004** (AC-5): Sync `template/its_magic/README.md` byte-identical to `its_magic/README.md` (one-way copy). Verify `PARITY_OK <size> <size>`.
- **T-005** (AC-4 / AC-6): Run validators (`validate_readme_feature_coverage.py --enforce`, `validate_doc_profile.py`, `check-user-visible-metadata.py`, `check_intake_template_parity.py`). Fix any narrative prose leaking internal IDs.
- **T-006** (AC-8): Run regression tests (`tests/scratchpad_example_parity_test.py` → 4 passed). Forbid edits to scratchpad canonical + example + test file.

**Execution order**: T-anch → T-001 → T-002 → T-003 → T-004 → T-005 → T-006. Acyclic. (T-anch first because it is a NO-OP / verification on `architecture.md`, not `its_magic/README.md`; doing it first keeps the README byte-stability surface clean for subsequent T-001..T-004.)

## AC mapping

| AC | Task(s) |
|----|---------|
| DC resolution (36 anchors) | T-anch (NO-OP / verification) |
| AC-1 | T-001 |
| AC-2 | T-002 |
| AC-3 | T-003 |
| AC-4 | T-005 |
| AC-5 | T-004 |
| AC-6 | T-005 |
| AC-7 | T-002 |
| AC-8 | T-006 |

**Surjectivity check**: AC-1..AC-8 all covered (8/8) + DC resolution covered (T-anch). No `PLAN_AC_COVERAGE_GAP`.

## Companion DEC

**none**. US-0117 is documentation-only (mirrors US-0113/US-0114/US-0115/US-0116 sibling precedent). Grep `^## DEC-` in `docs/engineering/decisions.md` returned no matches. DC-1+DC-2+DC-3+DC-4 resolution is a triad-hygiene closure (36 anchors RESOLVED in `/architecture` phase), not a tradeoff requiring a DEC.

## Compose guards UNCHANGED (23 cumulative — same 23 as US-0116)

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062. US-0117 documentation-only; lives entirely outside compose surface. **23 guards UNCHANGED.**

## DC resolution (36 anchors added in /architecture — final deferred-candidate resolution point; T-anch NO-OP)

US-0117 added **36 `## US-xxxx` h1 anchors** to `docs/engineering/architecture.md` in the **`/architecture` phase** (per R-0105 Q-2 LOCKED — "resolve in `/architecture`, NOT `/execute`"; keeps anchors as architecture artifacts per `docs/engineering/artifact-ownership-policy.md`):

- **18 own** (US-0117 family): US-0069, US-0070, US-0071, US-0072, US-0075, US-0076, US-0077, US-0078, US-0079, US-0080, US-0081, US-0082, US-0083, US-0085, US-0087, US-0088, US-0089, US-0090.
- **18 deferred**: DC-1 (US-0103/US-0104/US-0105/US-0107/US-0110 [5], from US-0113); DC-2 (US-0041/US-0062 [2], from US-0114); DC-3 (US-0034/US-0084/US-0086/US-0093/US-0096/US-0101/US-0102 [7], from US-0115); DC-4 (US-0092/US-0095/US-0098/US-0099 [4], from US-0116).
- **Plus the `## US-0117` anchor itself** (the normative US-0117 architecture section).

**T-anch in this sprint = NO-OP / verification**: the 36 anchors + `## US-0117` section already exist at `docs/engineering/architecture.md` L1568–L1708. T-anch does NOT perform a new write; it confirms the anchors exist and that `git diff HEAD -- docs/engineering/architecture.md` shows no execute-phase edits to architecture.md. NOT appended to `handoffs/sovereign_deferrals.jsonl` — the anchors ARE being resolved in `/architecture` (resolved there, not deferred further).

## 5th-story cumulative byte-stability surface

US-0117 is the **first 5-cumulative-surface story** — the cumulative byte-stability surface now covers **4 prior released blocks** (US-0113 L1682 + US-0114 L1806 + US-0115 L1878 + US-0116 L2225). The cross-story byte-stability contract (S0114 retrospective — "net-new keys + cross-link pointers + reason-code-only entries + prose-only entries; never edit prior story's released block") scales from a quad to a quint. US-0117's net-new content (46 key rows + 9 reason-code-only + 7 prose-only + cross-link pointers) is added to its own 5th sub-block; it never edits prior released blocks. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2225 range (no removals/modifications to US-0113's L1682, US-0114's L1806, US-0115's L1878, or US-0116's L2225 blocks). `PARITY_OK <size> <size>` is the authoritative end-to-end byte-stability proof. Pattern now established as a quint (S0113/S0114/S0115/S0116 + US-0117).

## 2 labeling corrections (LOCKED in T-002)

- **US-0082 = "Codebase map"** (NOT "Input compression" per spec handoff). Authoritative per runbook L63 + DEC-0065 + architecture `## US-0082 — Codebase map (bootstrap mechanism)` L1612. The input-compression surface is owned by US-0090.
- **US-0090 = "Caveman input compression"** (NOT "Phase governance integration" per spec handoff). Authoritative per runbook L2099 + DEC-0073 + architecture `## US-0090 — Caveman input compression` L1636. The "phase governance integration" concept is the **umbrella-level introductory framing** (AC-1), not a separate `#### US-0090` subsection.

T-002 applies both corrections in the `#### US-0082` and `#### US-0090` subsection titles + narrative content.

## US-0089 US-id collision (LOCKED in T-002)

Runbook h2 `## Caveman mode (US-0089)` at L2032 covers caveman voice/level (US-0081 family content). 18-feature family US-0089 = **Auto orchestration** (per scratchpad L21 `AUTO_PAUSE_REQUEST` + L135 `AUTO_REMOTE_AUTOMATION_PROFILE` + 18-feature family decomposition in backlog.md US-0117 block). `/architecture` LOCKS the resolution: the `#### US-0089` subsection title in the US-0117 umbrella = **"Auto orchestration"** (NOT "Caveman mode"). The caveman-mode narrative is owned by `#### US-0081` (US-0081 owns `CAVEMAN_MODE` / `CAVEMAN_LEVEL` keys); US-0089 owns the auto-orchestration narrative (`AUTO_PAUSE_REQUEST` + `AUTO_REMOTE_AUTOMATION_PROFILE`). T-002 applies this resolution.

## Risks finalized (carried from architecture)

- AC-3 byte-stability (5th-story cumulative surface — first 5-cumulative-surface story): **MEDIUM** — net-new + cross-link pointers, never edit prior released blocks.
- AC-5 parity lockstep: **MEDIUM** — T-004 one-way copy + `PARITY_OK`.
- AC-7 anchor gaps + labeling ambiguities: **MEDIUM** — R-0105 closed all gaps; 2 label corrections + 1 US-id collision LOCKED in T-002.
- AC-8 regression tests: **LOW–MEDIUM** — forbid edits to scratchpad canonical + example + test file.
- DC anchor resolution (first-time in `/architecture`): **LOW (mitigated)** — 36 anchors + `## US-0117` section already added in `/architecture` phase; T-anch in this sprint = NO-OP / verification.
- AC-2 18-subsection scope size: **MEDIUM** — 2–4× prior stories' T-002 load; keep T-002 single; split only if dev stalls.
- AC-4 encoding hygiene prerequisite carried from US-0114: **MEDIUM (carried)** — 185 stray `0xa7` bytes in working-tree `docs/product/backlog.md`; flag to orchestrator before execute; NOT a US-0117 blocker.
- US-0087 key surface size: **MEDIUM** — 18 net-new key rows, largest in family; angle boundary with US-0088/US-0092 explicit.
- Decomposition drift: **LOW** — drain mutex (US-0117 is the last story; no successor in this drain).

## Isolation evidence (per US-0048 / DEC-0029)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `story_id=US-0117`
- `orchestrator_run_id=auto-20260704-01`
- `fresh_context_marker=tl-US0117-sprint-plan-20260704T172645Z-fresh`
- Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to artifact files (narrow-read per US-0053 — architecture.md `## US-0117` section + 36 DC anchors L1568–L1708, research.md R-0105 entry, po_to_tl.md top architecture handoff block, backlog.md US-0117 block L3965–3981, state.md US-0117 architecture checkpoint, resume_brief.md top ~30 lines, sprints/S0116/sprint.md + tasks.md as reference template). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python timestamp computation.
- `assemble_sovereign_memory_digest(...)` NOT called (US-0117 documentation-only; existing digest context sufficient per R-0105 — S0113/S0114/S0115/S0116 retrospectives established reusable patterns — cross-link pointer pattern + angle-distinct narrative pattern + cross-story byte-stability contract quad scaled to 5th story).
- No write to `mistakes.jsonl` in sprint-plan phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).
- Prior architecture proof consumed: `rp-auto-20260704-01-architecture-techlead-20260704T171500Z-US-0117` (from `handoffs/po_to_tl.md` US-0117 architecture handoff section, unchanged).
- Current sprint-plan-phase strict proof recorded below.

## Strict runtime proof (DEC-0038)

- **runtime_proof_id**: `rp-auto-20260704-01-sprint-plan-techlead-20260704T172645Z-US-0117`
- **canonical_payload** (sorted-key JSON per DEC-0038): `{"companion_dec":"none","delivery_mode":"ultra_lean","macro_phase":"plan","orchestrator_run_id":"auto-20260704-01","phase_id":"sprint-plan","proof_issued_at":"2026-07-04T17:26:45Z","proof_ttl_seconds":3600,"role":"tech-lead","sprint_id":"S0117","sprint_seeds":7,"story_id":"US-0117","verdict":"PASS"}`
- **proof_ttl**: 2026-07-04T18:26:45Z (1-hour TTL per DEC-0038)

## Decision gate

**None** — sprint-plan satisfied; build+verify readiness explicit. All 8 R-0105 carry-overs resolved by tech-lead within the `plan` macro without operator input (approach A1 locked; sprint seeds T-anch + T-001..T-006; files to touch/not to touch locked; DC-1+DC-2+DC-3+DC-4 RESOLVED in `/architecture` — T-anch in this sprint is NO-OP / verification; encoding hygiene prerequisite flagged; 5th-story cumulative byte-stability surface LOCKED; 2 labeling corrections LOCKED; US-0089 US-id collision LOCKED). No DEC candidate (US-0117 documentation-only; mirrors US-0113/US-0114/US-0115/US-0116 sibling precedent). Verdict: **PASS**.

## Next phase

Per **ultra_lean**, the orchestrator routes to the **`build+verify` macro** — `/execute` (dev, first canonical phase of `build+verify`), which then chains to `/qa` (merges plan-verify + execute QA + verify-work). Plan-verify is NOT a standalone phase in ultra_lean.

**Stop**: sprint-plan complete; do not spawn the next phase. Orchestrator Task-spawns dev for `/execute`.

---

# Architecture handoff — US-0117 / auto-20260704-01 (architecture PASS tl, next `/sprint-plan` tech-lead)

**Date**: 2026-07-04
**Phase**: architecture (second canonical phase of `plan` macro per ultra_lean)
**Role**: tech-lead
**Story**: US-0117 — Phase & role governance operator documentation in framework README
**orchestrator_run_id**: auto-20260704-01
**delivery_mode**: ultra_lean
**macro_phase**: plan (architecture)
**fresh_context_marker**: tl-US0117-architecture-20260704T171500Z-fresh
**timestamp**: 2026-07-04T17:15:00Z (UTC)
**verdict**: PASS
**next_scheduled_phase**: sprint-plan
**default_spawn_role**: tech-lead

## Summary

**`/architecture`** **PASS** — **US-0117** architecture locked. **Approach A1** (single `### Phase & role governance` umbrella + 18 nested `#### US-xxxx` subsections + 5th scratchpad ref sub-block `### Phase & role governance keys`, sibling to US-0113/US-0114/US-0115/US-0116 umbrellas). **Companion DEC=none** (US-0117 documentation-only; mirrors US-0113/US-0114/US-0115/US-0116 sibling precedent; grep `^## DEC-` returned no matches). **DC-1+DC-2+DC-3+DC-4 RESOLVED** in this phase — 36 `## US-xxxx` h1 anchors added to `docs/engineering/architecture.md` (18 own + 18 deferred; **first-time DC anchor addition in architecture phase**; final deferred-candidate resolution point). Status authority: **OPEN** per **US-0045** (closure at `/release`).

US-0117 is the **5th and final story** in the 5-story drain, the LARGEST family (18 features vs 4–9 in prior stories), and the **final deferred-candidate resolution point** for the architecture.md triad hygiene closure. The 5th-story cumulative byte-stability surface covers 4 prior released blocks (US-0113 L1682 + US-0114 L1806 + US-0115 L1878 + US-0116 L2225) — contract pattern scales to the 5th story without regression (net-new-keys-only + cross-link-pointers + reason-code-only + prose-only shape).

## Architecture anchor

`docs/engineering/architecture.md` `## US-0117 — Phase & role governance operator documentation in framework README` (appended in this phase). Includes: Overview, Companion DEC, Approach A1 (locked), Files to touch, Files NOT to touch, Sprint seeds (T-001..T-006 + T-anch = 7 tasks), Test markers (5), Compose guards UNCHANGED (23), DC-1+DC-2+DC-3+DC-4 resolution (36 anchors), Risks finalized, Stop conditions met, Sovereign memory note, Consequences, Evidence references, Isolation evidence, Strict runtime proof. Plus 36 `## US-xxxx` DC anchor stubs appended below the US-0117 section.

## Approach A1 (locked)

Single `### Phase & role governance` umbrella + 18 nested `#### US-xxxx` subsections (h4 under h3 umbrella), sibling to US-0113's `### Sovereign-loop era`, US-0114's `### Release & distribution`, US-0115's `### Integration & observability`, and US-0116's `### Delivery & lifecycle` umbrellas, inserted after US-0116's umbrella under `## Commands and workflow`. Consistency with prior 4 stories. Alternatives A2 (reuse existing README section as umbrella) and A3 (split into 2 umbrellas) rejected — see architecture.md `## US-0117` § Approach locked.

## Sprint seeds preview (7 tasks within SPRINT_MAX_TASKS=12)

- **T-anch** (AC-2 / AC-8): Add 36 `## US-xxxx` h1 anchors to `docs/engineering/architecture.md` (18 own + 18 deferred DC-1+DC-2+DC-3+DC-4) + `# US-0117` anchor. Minimal 3–5 line normative sections. First-time DC anchor addition in architecture phase.
- **T-001** (AC-1): Add umbrella `### Phase & role governance (...) umbrella section` under `## Commands and workflow` (after US-0116 umbrella close, before L1665).
- **T-002** (AC-2 / AC-7): Add 18 per-feature operator subsections (US-0069 -> US-0090) under the umbrella. Two labeling corrections: US-0082 = "Codebase map"; US-0090 = "Caveman input compression"; US-0089 = "Auto orchestration" (US-id collision resolved).
- **T-003** (AC-3): Add `### Phase & role governance keys` sub-block under `### Full scratchpad reference (detailed)` (after US-0116 L2225 block). 46 net-new key rows + 9 reason-code-only entries + 7 prose-only / runbook-cross-link-only entries + cross-link pointers.
- **T-004** (AC-5): Sync `template/its_magic/README.md` byte-identical (one-way copy). Verify `PARITY_OK <size> <size>`.
- **T-005** (AC-4 / AC-6): Run validators (coverage / doc-profile / metadata / intake-parity). Fix any narrative prose leaking internal IDs.
- **T-006** (AC-8): Run regression tests (`tests/scratchpad_example_parity_test.py` -> 4 passed). Forbid edits to scratchpad canonical + example + test file.

**Execution order**: T-anch -> T-001 -> T-002 -> T-003 -> T-004 -> T-005 -> T-006. Acyclic.

## Companion DEC

**none**. US-0117 is documentation-only (mirrors US-0113/US-0114/US-0115/US-0116 sibling precedent). Grep `^## DEC-` in `docs/engineering/decisions.md` returned no matches. DC-1+DC-2+DC-3+DC-4 resolution is a triad-hygiene closure, not a tradeoff requiring a DEC.

## DC resolution (36 anchors added — final deferred-candidate resolution point)

US-0117 adds **36 `## US-xxxx` h1 anchors** to `docs/engineering/architecture.md` in THIS phase:

- **18 own** (US-0117 family): US-0069, US-0070, US-0071, US-0072, US-0075, US-0076, US-0077, US-0078, US-0079, US-0080, US-0081, US-0082, US-0083, US-0085, US-0087, US-0088, US-0089, US-0090.
- **18 deferred**: DC-1 (US-0103/US-0104/US-0105/US-0107/US-0110 [5], from US-0113); DC-2 (US-0041/US-0062 [2], from US-0114); DC-3 (US-0034/US-0084/US-0086/US-0093/US-0096/US-0101/US-0102 [7], from US-0115); DC-4 (US-0092/US-0095/US-0098/US-0099 [4], from US-0116).
- **Plus the `## US-0117` anchor itself** (the normative US-0117 architecture section).

**First-time DC anchor addition in architecture phase** (prior 4 stories deferred them to US-0117). Resolution approach (Q-2 LOCKED in R-0105): add in `/architecture`, NOT `/execute`. NOT appended to `handoffs/sovereign_deferrals.jsonl` — the anchors ARE being resolved in this phase.

## Risks finalized

- AC-3 byte-stability (5th-story cumulative surface — first 5-cumulative-surface story): **MEDIUM** — net-new + cross-link pointers, never edit prior released blocks.
- AC-5 parity lockstep: **MEDIUM** — T-004 one-way copy + `PARITY_OK`.
- AC-7 anchor gaps + labeling ambiguities: **MEDIUM** — R-0105 closed all gaps; 2 label corrections + 1 US-id collision LOCKED.
- AC-8 regression tests: **LOW–MEDIUM** — forbid edits to scratchpad canonical + example + test.
- DC anchor resolution (first-time in `/architecture`): **MEDIUM** — 36 anchors + `# US-0117` added HERE; ~1670 lines post-addition, under 3000-line cap.
- AC-2 18-subsection scope size: **MEDIUM** — keep T-002 single; split only if dev stalls.
- AC-4 encoding hygiene prerequisite (carried from US-0114): **MEDIUM (carried)** — 185 stray `0xa7` bytes in working-tree `docs/product/backlog.md`; flag to orchestrator before execute; NOT a US-0117 blocker.
- US-0087 key surface size: **MEDIUM** — 18 net-new key rows (largest in family); angle boundary with US-0088/US-0092 explicit.
- Decomposition drift: **LOW**.

## Compose guards UNCHANGED (23 cumulative — same 23 as US-0116)

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062. US-0117 documentation-only; lives entirely outside compose surface.

## Isolation evidence (per US-0048 / DEC-0029)

Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to artifact files (narrow-read per US-0053). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python timestamp/hash computation. `assemble_sovereign_memory_digest(...)` NOT called (US-0117 documentation-only; existing digest context sufficient per R-0105). No write to `mistakes.jsonl` in architecture phase.

## Strict runtime proof (DEC-0038)

- **runtime_proof_id**: `rp-auto-20260704-01-architecture-techlead-20260704T171500Z-US-0117`
- **canonical_payload** (sorted-key JSON): `{"approach_locked":"A1","companion_dec":"none","delivery_mode":"ultra_lean","dc_anchors_added":36,"macro_phase":"plan","orchestrator_run_id":"auto-20260704-01","phase_id":"architecture","proof_issued_at":"2026-07-04T17:15:00Z","proof_ttl_seconds":3600,"research_anchor":"R-0105","role":"tech-lead","story_id":"US-0117","verdict":"PASS"}`
- **proof_ttl**: 2026-07-04T18:15:00Z (1-hour TTL per DEC-0038)

## Decision gate

**No DECISION_GATE raised.** Architecture phase revealed no question requiring operator input. DC-1+DC-2+DC-3+DC-4 resolved by tech-lead within the `plan` macro (36 h1 anchors added in THIS phase). No DEC candidate (US-0117 documentation-only). verdict=PASS — no operator input needed.

## Next scheduled phase

- **next_scheduled_phase**: sprint-plan (tech-lead, `plan` macro — third canonical phase). In ultra_lean, sprint-plan is merged into `plan` macro; orchestrator Task-spawns TL for `plan` macro.
- **drain_advance_pending**: false (US-0117 architecture complete; orchestrator advance hook routes to TL `sprint-plan`)
- **stop_condition**: STOP after architecture completes; orchestrator Task-spawns Tech Lead subagent for `sprint-plan` (third canonical phase of `plan` macro). Do NOT start sprint-plan in this subagent. Hand off via artifacts only.

---

<!-- Archive pointer (2026-07-04-b): US-0114 lifecycle handoffs (sprint-plan, architecture, research, discovery) rolled over to `handoffs/archive/po-to-tl-pack-20260704-b.md` on 2026-07-04 by curator (US-0115 refresh-context terminal). Prior archive (2026-07-04-a): US-0113 lifecycle handoffs + intake handoffs → `handoffs/archive/po-to-tl-pack-20260704-a.md`. Retained: US-0115 lifecycle handoffs (this file). US-0116 lifecycle handoffs retained below. US-0117 spec handoff prepended 2026-07-04. -->

# Research handoff — US-0117 / auto-20260704-01 (research PASS tl, next `/architecture` tech-lead)

**Date**: 2026-07-04
**Phase**: research (first canonical phase of `plan` macro per ultra_lean)
**Role**: tech-lead
**Story**: US-0117 — Phase & role governance operator documentation in framework README
**orchestrator_run_id**: auto-20260704-01
**delivery_mode**: ultra_lean
**macro_phase**: plan (research)
**fresh_context_marker**: tl-US0117-research-20260704T165435Z-fresh
**timestamp**: 2026-07-04T16:54:35Z (UTC)
**verdict**: PASS
**next_scheduled_phase**: architecture
**default_spawn_role**: tech-lead

## Summary

**`/research`** **PASS** — **R-0105** delivered (8/8 open questions closed; 18 per-feature sub-findings delivered; AC-3 approach locked; DC-1+DC-2+DC-3+DC-4 confirmed = 18 deferred anchors + 18 own anchors = 36 total to add in `/architecture`; AC baselines green; deepened risks identified). Companion **DEC=none** (US-0117 is documentation-only; mirrors US-0113/US-0114/US-0115/US-0116 sibling precedent). Status authority: **OPEN** per **US-0045** (closure at `/release`).

US-0117 is the **5th and final story** in the 5-story drain, the LARGEST family (18 features vs 4–9 in prior stories), and the **final deferred-candidate resolution point** for the architecture.md triad hygiene closure. It inherits 18 missing `# US-xxxx` h1 anchors (DC-1+DC-2+DC-3+DC-4) + owns 18 anchors for its own features (also missing — confirmed by grep) = **36 total h1 anchors to add in `/architecture`**. The 5th-story cumulative byte-stability surface covers 4 prior released blocks (US-0113 L1881 + US-0114 L2005 + US-0115 L2077 + US-0116 L2225) — the contract pattern scales to the 5th story without regression (net-new-keys-only + cross-link-pointers + reason-code-only + prose-only shape).

## Research anchor

**R-0105** (delivered 2026-07-04T16:54:35Z, 8/8 open questions closed; 18 per-feature sub-findings; AC-3 approach locked; DC-1..DC-4 confirmed; AC baselines green; deepened risks). See `docs/engineering/research.md` `## R-0105`.

## 18 per-feature sub-findings summary

| US-id | Feature (authoritative label) | Scratchpad key surface | Runbook anchor (AC-7) | Net-new / cross-link classification |
|-------|-------------------------------|------------------------|------------------------|--------------------------------------|
| US-0069 | Phase→role matrix | `AUTO_ROLE_RESEARCH` / `AUTO_ROLE_PLAN_VERIFY` / `AUTO_ROLE_REFRESH_CONTEXT` (3 keys) | L1711 h2 | Net-new |
| US-0070 | Phase selection policy | `AUTO_PHASE_PLAN` / `AUTO_PHASE_EXCLUDE` / `AUTO_PHASE_INCLUDE` / `AUTO_PHASE_PROFILE` (4 keys) + `PHASE_POLICY_CONFLICT` / `PHASE_PLAN_UNKNOWN_PHASE` reason codes | L1753 h2 | Net-new |
| US-0071 | Metadata sanitization | No key row (validator gate) | L303 h2 | Prose-only / runbook-cross-link-only |
| US-0072 | Context slimming | No key row (concept; cross-link to US-0080 `TOKEN_PROFILE` + US-0115 `LEAN_MEMORY_*`) | L550 h2 (shared with US-0080) | Prose-only / cross-link-pointer |
| US-0075 | Scratchpad example-first refresh | No key row (parity contract) | L1949 h3 + L2535 h2 | Prose-only / runbook-cross-link-only |
| US-0076 | Codebase map (freshness gate) | No key row (concept; cross-link to US-0082 `CODEBASE_MAP_REFRESH_ON_ROLLOVER`) | L63 h2 (shared with US-0082) | Prose-only / cross-link-pointer |
| US-0077 | Delegation policy | No key row (validator gate) + `INTAKE_DELEGATION_EVIDENCE_MISSING` reason code | L98 h2 | Prose-only / runbook-cross-link-only |
| US-0078 | Env file bootstrap (intake evidence harness) | No key row (harness contract) | L479 h2 (shared with US-0083) | Prose-only / runbook-cross-link-only |
| US-0079 | Bug queue routing | `AUTO_BUG_QUEUE` / `AUTO_BUG_TARGET` / `AUTO_BUG_MAX_ITEMS` / `AUTO_BUG_ON_BLOCK` (4 keys) | L512 h2 | Net-new |
| US-0080 | Auto quiet mode | `AUTO_QUIET` (1 key) | L570 h3 + L1881 h3 | Net-new |
| US-0081 | Caveman mode | `CAVEMAN_MODE` / `CAVEMAN_LEVEL` (2 keys) + `CAVEMAN_LEVEL_UNKNOWN` reason code | L2032 h3 | Net-new |
| US-0082 | Codebase map (bootstrap mechanism) — **label correction: spec handoff's "Input compression" is a mislabel; authoritative = Codebase map per runbook L63 + DEC-0065** | No key row (cross-link to US-0076 for freshness gate) | L63 h2 | Prose-only / cross-link-pointer |
| US-0083 | Scratchpad delivery keys | `AUTO_DELIVERY_ROUTING` (1 key; `DELIVERY_MODE` cross-link to US-0114 L2005) + `DELIVERY_MODE_SWITCH_MID_STORY` reason code | L479 h2 (shared with US-0078) + L591 h3 | Net-new + cross-link |
| US-0085 | Context fresh-context markers | No key row (`fresh_context_marker` is an isolation-evidence field) + `PHASE_CONTEXT_ISOLATION_MISSING` reason code | L1628 h2 | Prose-only / runbook-cross-link-only |
| US-0087 | Full-autonomy mode | 18 keys: `AUTO_FLOW_MODE` / `AUTO_IMPLEMENTATION_LOOP` / `AUTO_LOOP_MAX_CYCLES` / `AUTO_BLOCK_RETRY_MAX` / `RELEASE_PUBLISH_MODE` / `CROSS_MODEL_REVIEW` / `CROSS_MODEL_ANTISLOP_THRESHOLD` / `CROSS_MODEL_REWORK_MAX` / `SOVEREIGN_MEMORY` + family (5) / `AUTO_SOVEREIGN` + family (4) / `SOVEREIGN_GOAL_MODE` + `BLOCK_RETRY_CAP_EXHAUSTED` / `NATIVE_CHAIN_UNAVAILABLE` reason codes | L1809 h2 + L1958 h3 | Net-new (largest key surface) |
| US-0088 | Automation modes | 9 keys: `AUTO_BACKLOG_DRAIN` / `AUTO_BACKLOG_MAX_STORIES` / `AUTO_BACKLOG_ON_BLOCK` / `AUTO_STORY_SELECTION` / `AUTO_EXECUTE_BULK` / `AUTO_EXECUTE_MAX_ITEMS` / `AUTO_EXECUTE_ON_BLOCK` / `AUTO_EXECUTE_SELECTION` / `AUTO_TEAM_SCOPE_ENFORCE` + `BLOCK_RETRY_CAP_EXHAUSTED` reason code | L1838 h2 | Net-new |
| US-0089 | Auto orchestration | `AUTO_PAUSE_REQUEST` / `AUTO_REMOTE_AUTOMATION_PROFILE` (2 keys) | L1398 h3 + L1838 h2 | Net-new |
| US-0090 | Caveman input compression — **label correction: spec handoff's "Phase governance integration" is a mislabel; authoritative = Caveman input compression per runbook L2099** | `CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE` (2 keys) + `CAVEMAN_COMPRESS_SCOPE_EMPTY` reason code | L2099 h3 | Net-new |

**Total net-new key rows**: 46 keys across 10 features (US-0069/0070/0079/0080/0081/0083/0087/0088/0089/0090).

## 8 open questions resolved

| Q | Topic | Resolution |
|---|-------|-----------|
| Q1 | 18-feature scope size — T-002 split or single pass | **Keep T-002 as a single task with 18 subsections** (mirror prior stories' pattern; the dev subagent can handle 18 subsections — it's documentation, not code). 18 subsections is 2–4× prior stories' T-002 load but remains within dev subagent capacity. `SPRINT_MAX_TASKS=12` threshold is not impacted (T-002 is one task with 18 sub-bullets). |
| Q2 | DC anchor resolution approach — `/architecture` vs `/execute` | **Resolve in `/architecture`** (add the h1 anchors to `architecture.md` as part of the architecture phase). Architecture owns h1 anchors per `docs/engineering/artifact-ownership-policy.md`. US-0117 inherits DC-1 (5) + DC-2 (2) + DC-3 (7) + DC-4 (4) = 18 deferred anchors + 18 own anchors = **36 total h1 anchors to add in `/architecture`**. First time the architecture phase adds DC anchors. |
| Q3 | Exact key names for 8 features | **Resolved via scratchpad grep**: US-0071/0075/0078/0085 = prose-only / runbook-cross-link-only (no key row); US-0072/0076 = prose-only / cross-link-pointer; US-0083 = `AUTO_DELIVERY_ROUTING` net-new + cross-link to US-0114 for `DELIVERY_MODE` + `DELIVERY_MODE_SWITCH_MID_STORY` reason code. See R-0105 § Per-feature sub-findings for full detail. |
| Q4 | `## US-0117` anchor missing in architecture.md | **Confirmed** — grep `^#+ US-0117\b` returned no matches. US-0117 needs its own anchor in `/architecture` phase (will be added as `# US-0117 — Phase & role governance operator documentation in framework README`). |
| Q5 | R-0105 research entry needed | **Confirmed** — R-0105 created in this phase (continuing from R-0104 US-0116). |
| Q6 | Cross-link overlap with US-0113 | **Verified via R-0101 + scratchpad grep**: `AUTO_FLOW_MODE` / `AUTO_QUIET` / `AUTO_BACKLOG_DRAIN` / `AUTO_BUG_QUEUE` are NOT in US-0113's `### Sovereign-loop era keys` block (L1881). All 5 keys are **net-new to US-0117's 5th block** (no cross-link pointer to US-0113 needed). US-0113's L1881 block byte-stability preserved (no edits). |
| Q7 | Cross-link overlap with US-0116 | **Verified via R-0104**: US-0116's `### Delivery & lifecycle keys` block (L2225) contains grouped cross-link pointers to pre-US-0116 README surfaces (L880 / L909 / L2370) for `AUTO_BACKLOG_DRAIN` / `AUTO_BUG_QUEUE` / `AUTO_LOOP_MAX_CYCLES` / `AUTO_BACKLOG_MAX_STORIES` family — US-0116 does NOT own canonical key rows for these. US-0117 owns the canonical key rows (scratchpad top-level); US-0116 retains grouped cross-link pointers (byte-stability preserved). All 4 keys are net-new to US-0117's 5th block. |
| Q8 | 5th-story cumulative byte-stability surface | **Confirmed** — prior 4 released blocks (US-0113 L1881 + US-0114 L2005 + US-0115 L2077 + US-0116 L2225) remain byte-identical. US-0117 adds net-new-keys-only + cross-link-pointers + reason-code-only entries + prose-only entries to its own 5th sub-block; never edits prior released blocks. `PARITY_OK <size> <size>` authoritative end-to-end proof. **First 5-cumulative-surface story** — contract pattern scales to the 5th (final) story without regression. |

## AC-3 approach locked

**AC-3 (Full scratchpad reference extension)**: net-new key rows (46 keys across 10 features) + cross-link pointers (`DELIVERY_MODE` → US-0114 L2005; `LEAN_MEMORY_*` → US-0115 L2077 default omit; `TOKEN_PROFILE` → main reference list + US-0080 subsection; `CODEBASE_MAP_REFRESH_ON_ROLLOVER` → US-0082 subsection) + reason-code-only entries (9 reason codes across 7 features) + prose-only / runbook-cross-link-only entries (7 features: US-0071/0072/0075/0076/0077/0078/0085). **5th-story cumulative byte-stability surface** — prior 4 released blocks remain byte-identical; US-0117 never edits them.

## DC resolution approach (36 anchors total in `/architecture`)

US-0117 is the **final deferred-candidate resolution point**. It adds **36 h1 anchors** in `/architecture`:

- **18 own anchors** (US-0069, US-0070, US-0071, US-0072, US-0075, US-0076, US-0077, US-0078, US-0079, US-0080, US-0081, US-0082, US-0083, US-0085, US-0087, US-0088, US-0089, US-0090) — confirmed missing by grep.
- **18 deferred DC anchors** (DC-1: US-0103/US-0104/US-0105/US-0107/US-0110 [5]; DC-2: US-0041/US-0062 [2]; DC-3: US-0034/US-0084/US-0086/US-0093/US-0096/US-0101/US-0102 [7]; DC-4: US-0092/US-0095/US-0098/US-0099 [4]).
- **Plus the `# US-0117` anchor itself** (Q4 confirmed missing).

Anchor format: `# US-xxxx — <feature title>` (matching existing `# US-0108` / `# US-0109` / `# US-0111` / `# US-0112` / `# US-0113` / `# US-0114` / `# US-0115` / `# US-0116` format). Each anchor is a minimal normative section (1–3 sentence summary of the locked feature contract). **First time the architecture phase adds DC anchors** — the approach is confirmed: `/architecture` adds the 36 h1 anchors as a single task seed (T-anch) + the `# US-0117` anchor + the normative US-0117 architecture section. Execute-phase does NOT add h1 anchors.

## AC baselines green

- `python scripts/validate_readme_feature_coverage.py --repo .` → `{"coverage_missing":[],"coverage_present":[],"coverage_total":0,"gaps":[],"status":"PASS"}` exit 0 (AC-4 catalog surface green).
- `python -m pytest tests/scratchpad_example_parity_test.py -q` → `4 passed in 0.06s` (AC-8 regression baseline green).

## Labeling corrections (locked)

Two features had mislabels in the spec handoff; the authoritative labels are locked per runbook + scratchpad canonical:

- **US-0082** = **Codebase map** (per runbook L63 `## Codebase map bootstrap (US-0082 / DEC-0065)` + DEC-0065). Spec handoff's "US-0082 (Input compression)" is a mislabel.
- **US-0090** = **Caveman input compression** (per runbook L2099 `### Caveman input compression (US-0090)` + DEC-0073 + scratchpad L313–L324). Spec handoff's "US-0090 (Phase governance integration)" is a mislabel.
- **"Phase governance integration"** is the umbrella's introductory framing (AC-1), not a separate `#### US-0090` subsection.
- **US-0089** = **Auto orchestration** (per scratchpad L21 `AUTO_PAUSE_REQUEST` + L135 `AUTO_REMOTE_AUTOMATION_PROFILE` + 18-feature family). Note the US-id collision: runbook h2 `## Caveman mode (US-0089)` L2032 covers the caveman-mode feature (which is US-0081 in the 18-feature family); `/architecture` locks the resolution (US-0089 = Auto orchestration per 18-feature family; runbook h2 `## Caveman mode (US-0089)` is a known runbook-side label that predates the 18-feature family decomposition — `#### US-0089` subsection in US-0117's umbrella documents Auto orchestration with cross-link to L1838 h2 + L1398 h3; `#### US-0081` subsection documents Caveman mode with cross-link to L2032 h3).

## Deepened risks

- **5th-story cumulative byte-stability surface** (MEDIUM) — prior 4 released blocks must remain byte-identical; net-new-keys-only + cross-link-pointer + reason-code-only + prose-only shape LOCKED. Mitigation: T-003 + execute-phase `git diff HEAD` pure-addition verification in post-L2225 range.
- **AC-5 parity lockstep** (MEDIUM) — T-004 one-way copy + byte-parity check + `check_intake_template_parity.py`.
- **AC-7 anchor gaps + labeling ambiguities** (MEDIUM) — 18 features, all anchors pre-exist; two labeling corrections (US-0082 = Codebase map; US-0090 = Caveman input compression) + one US-id collision (runbook `## Caveman mode (US-0089)` vs 18-feature family US-0089 = Auto orchestration). Mitigation: `/architecture` locks authoritative labels.
- **AC-8 regression tests** (LOW–MEDIUM) — forbid edits to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, `tests/scratchpad_example_parity_test.py`; fix prose, never relax test.
- **DC anchor resolution (first-time DC anchor addition in `/architecture`)** (MEDIUM) — 36 h1 anchors + `# US-0117` to add; current ~1418 lines + 36 anchors × ~10 lines/anchor ≈ 1780 lines, under 3000-line cap (no rollover required).
- **AC-2 18-subsection scope size** (MEDIUM) — 2–4× prior stories' T-002 load; keep T-002 single; split only if dev subagent progress stalls.
- **AC-4 encoding hygiene prerequisite (carried from US-0114)** (MEDIUM) — 185 stray `0xa7` bytes in working-tree `docs/product/backlog.md`; flag to orchestrator before execute; NOT a US-0117 blocker.
- **US-0087 key surface size** (MEDIUM) — 18 net-new key rows (largest in the family); angle boundary with US-0088 / US-0092 (US-0116 family, cross-link only) explicit.
- **Decomposition drift** (LOW) — bounded by angle-distinct narrative contract.

## Compose guards confirmed (UNCHANGED — 23 cumulative)

US-0117 is documentation-only and lives entirely outside the compose surface. The 23 compose guards (cumulative across all prior stories — same 23 as US-0116) remain UNCHANGED:

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062.

## Task seeds for `/sprint-plan` (7 tasks within SPRINT_MAX_TASKS=12)

| T | AC | Description |
|---|----|-------------|
| T-001 | AC-1 | Add umbrella `### Phase & role governance (US-0069 / US-0070 / US-0071 / US-0072 / US-0075 / US-0076 / US-0077 / US-0078 / US-0079 / US-0080 / US-0081 / US-0082 / US-0083 / US-0085 / US-0087 / US-0088 / US-0089 / US-0090) umbrella section` under `## Commands and workflow` (after US-0116 umbrella close, before L1864 `### Full scratchpad reference (detailed)`). 18-step enable order (US-id-ascending) + runbook pointer line + zero-overhead-when-off contract line + "phase governance integration" introductory framing. |
| T-002 | AC-2, AC-7 | Add 18 per-feature `#### US-xxxx` operator subsections under the umbrella, ordered US-id-ascending (US-0069 → US-0090). Each subsection: 1–3 sentence narrative (angle-distinct per R-0105 § Per-feature sub-findings), master enable flag + related keys with defaults (where applicable), zero-overhead-when-off wording (where applicable), runbook cross-link (existing anchor only — no duplication), bidirectional cross-link pointers for overlapping angles (US-0087 ↔ US-0092 cross-family; US-0081 ↔ US-0090 within-family; US-0078 ↔ US-0083 within-family; US-0076 ↔ US-0082 within-family; US-0072 ↔ US-0080 within-family). Authoritative labels: US-0082 = Codebase map; US-0090 = Caveman input compression; US-0089 = Auto orchestration. |
| T-003 | AC-3 | Add `### Phase & role governance keys (US-0069 / US-0070 / US-0071 / US-0072 / US-0075 / US-0076 / US-0077 / US-0078 / US-0079 / US-0080 / US-0081 / US-0082 / US-0083 / US-0085 / US-0087 / US-0088 / US-0089 / US-0090)` sub-block under `### Full scratchpad reference (detailed)` (after US-0116's `### Delivery & lifecycle keys` block L2225; before the next `###` h3 section). 46 net-new key rows (10 features) + cross-link pointers (`DELIVERY_MODE` → US-0114 L2005; `LEAN_MEMORY_*` → US-0115 L2077 default omit; `TOKEN_PROFILE` → main reference list above L1864 + US-0080 subsection; `CODEBASE_MAP_REFRESH_ON_ROLLOVER` → US-0082 subsection) + 9 reason-code-only entries (7 features) + 7 prose-only / runbook-cross-link-only entries (7 features: US-0071/0072/0075/0076/0077/0078/0085). No duplicate key rows. Byte-stability of US-0113 L1881 + US-0114 L2005 + US-0115 L2077 + US-0116 L2225 blocks preserved (net-new-keys-only + cross-link-pointer + reason-code-only + prose-only shape; 5th-story cumulative surface). |
| T-004 | AC-5 | Sync `template/its_magic/README.md` byte-identical via one-way copy from `its_magic/README.md`. Re-run `python -c "a=open(r'its_magic/README.md','rb').read(); b=open(r'template/its_magic/README.md','rb').read(); print('PARITY_OK' if a==b else 'PARITY_DIFF')"` (expect `PARITY_OK`) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`). |
| T-005 | AC-4, AC-6 | Run validators: `python scripts/validate_readme_feature_coverage.py --enforce` (expect `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0 — catalog block L63 read-only) + `python scripts/validate_doc_profile.py` (expect `[DOC_PROFILE_VALIDATE_OK]`) + `python scripts/check-user-visible-metadata.py` (expect exit 0; US-IDs only in parenthetical catalog tags `(US-xxxx)`). |
| T-006 | AC-8 | Run regression tests: `python -m pytest tests/scratchpad_example_parity_test.py -q` (expect 4/4 PASS). **Forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` — if a test fails, the prose is wrong, not the test (fix prose, never relax test). |
| T-anch | AC-2, AC-8 | Add 36 `# US-xxxx` h1 anchors to `docs/engineering/architecture.md` (18 own + 18 deferred DC-1..DC-4) + the `# US-0117` anchor itself + the normative US-0117 architecture section. Each anchor: `# US-xxxx — <feature title>` + 1–3 sentence summary of the locked feature contract (from R-0105 § Per-feature sub-findings for own 18; from prior R-xxxx research entries + DEC-xxxx for deferred 18). Verify architecture.md stays under 3000-line hot-surface cap (no rollover required — ~1780 lines post-addition). This is the **first-time DC anchor addition in `/architecture`** — execute-phase does NOT add h1 anchors. |

**Execution order**: T-anch (36 h1 anchors + US-0117 anchor) → T-001 (umbrella) → T-002 (18 subsections) → T-003 (scratchpad ref extension) → T-004 (template byte-sync) → T-005 (validators) → T-006 (regression tests). Acyclic, mirrors US-0113/US-0114/US-0115/US-0116 with T-anch added as a new task for the DC anchor resolution.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=research`
- `role=tech-lead`
- `fresh_context_marker=tl-US0117-research-20260704T165435Z-fresh`
- `timestamp=2026-07-04T16:54:35Z`
- `evidence_ref=docs/engineering/research.md (R-0105 delivered),docs/product/backlog.md (## US-0117 block L3965–3981),docs/engineering/state.md (US-0117 spec checkpoint L2814–L2891),handoffs/po_to_tl.md (US-0117 spec handoff L1–L177),handoffs/resume_brief.md (top drain-advance block),.cursor/scratchpad.md (phase & role governance keys),its_magic/README.md (TOC + 4 prior sibling umbrellas + 4 prior sibling keys blocks),docs/engineering/runbook.md (18 anchors),docs/engineering/architecture.md (h1 inventory)`

## Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260704-01`
- `runtime_proof_id=rp-auto-20260704-01-research-tech-lead-20260704T165435Z-US-0117`
- `phase_id=research`
- `role=tech-lead`
- `proof_issued_at=2026-07-04T16:54:35Z`
- `proof_ttl_seconds=3600`
- `proof_hash=research-pass-us0117-20260704T165435Z`

Canonical payload: `{"orchestrator_run_id":"auto-20260704-01","phase_id":"research","proof_issued_at":"2026-07-04T16:54:35Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260704-01-research-tech-lead-20260704T165435Z-US-0117","story_id":"US-0117"}`.

## Decision gate

**None** — research satisfied; architecture readiness explicit. All 8 spec open questions resolved by tech-lead within the `plan` macro without operator input. No DEC candidate (US-0117 is documentation-only; mirrors US-0113/US-0114/US-0115/US-0116 sibling precedent). The DC-1..DC-4 deferral is a triad-hygiene carry-over resolved in `/architecture` (36 h1 anchors added), not a tradeoff requiring a DEC.

## Handoff

- **Next phase**: `/architecture` (tech-lead) — `plan` macro second canonical phase
- **Next role**: tech-lead
- **fresh_context_marker**: tl-US0117-research-20260704T165435Z-fresh
- **timestamp**: 2026-07-04T16:54:35Z (UTC)

STOP after research handoff. The orchestrator Task-spawns the Tech Lead subagent for `architecture` (`plan` macro second canonical phase). Hand off via artifacts only.

---

# Spec handoff — US-0117 / auto-20260704-01 (intake + discovery merged)

**Date**: 2026-07-04
**Phase**: spec (intake + discovery merged per ultra_lean)
**Role**: po
**Story**: US-0117 — Phase & role governance operator documentation in framework README
**orchestrator_run_id**: auto-20260704-01
**delivery_mode**: ultra_lean
**macro_phase**: spec
**fresh_context_marker**: po-US0117-spec-20260704T163100Z-fresh
**timestamp**: 2026-07-04T16:31:00Z (UTC)

## Intake confirmation

- **Status authority**: `docs/product/backlog.md` L3965–3981 — US-0117 block, `Status: OPEN` per US-0045 (confirmed). Story remains OPEN through `plan` / `build+verify` / `ship` macros; closed only at `/release`.
- **AC well-formedness**: 8 ACs confirmed well-formed and actionable (copied verbatim below).
- **Family distinctness**: Phase & role governance family (18 features: US-0069, US-0070, US-0071, US-0072, US-0075, US-0076, US-0077, US-0078, US-0079, US-0080, US-0081, US-0082, US-0083, US-0085, US-0087, US-0088, US-0089, US-0090) distinct from prior 4 released families:
  - US-0113 sovereign-loop era (US-0103–US-0112) — 9 features
  - US-0114 release & distribution (US-0041 / US-0062 / US-0111 / US-0112) — 4 features
  - US-0115 integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102) — 7 features
  - US-0116 delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) — 4 features
  - US-0117 owns the operator-facing catalog of phase commands + role governance + scratchpad governance keys (phase selection, sanitization, slimming, codebase map, delegation, env file bootstrap, bug queue routing, auto quiet, caveman, input compression, delivery keys, full-autonomy / automation modes / auto orchestration, phase governance integration).
- **LARGEST family in the 5-story drain**: 18 features vs 4–9 in prior stories. **Flag for TL research**: per-feature subsection count (18 `#### US-xxxx` subsections) is significantly higher than prior stories (4–9). T-002 may need to be split (e.g., 2 batches of 9, or grouped sub-clusters) or the dev subagent may need to handle 18 subsections in one pass. Recommend TL evaluates sprint seed count and task decomposition shape in `/research` + `/sprint-plan`.

## 8 ACs (verbatim from backlog.md L3972–3980)

- [ ] AC-1: `### Phase & role governance` umbrella section under `## Commands and workflow`
- [ ] AC-2: Per-feature operator subsections for US-0069/US-0070/US-0071/US-0072/US-0075/US-0076/US-0077/US-0078/US-0079/US-0080/US-0081/US-0082/US-0083/US-0085/US-0087/US-0088/US-0089/US-0090
- [ ] AC-3: Full scratchpad reference extension
- [ ] AC-4: Coverage preserved
- [ ] AC-5: Framework README parity
- [ ] AC-6: Audience + metadata hygiene
- [ ] AC-7: Runbook cross-links
- [ ] AC-8: Regression tests

## Discovery — operator documentation gap frame

US-0113–US-0116 closed operator-doc gaps for 4 families (sovereign-loop era, release & distribution, integration & observability, delivery & lifecycle). The **phase & role governance** family — 18 features spanning phase selection policy, role routing, metadata sanitization, context slimming, scratchpad example-first refresh, codebase map bootstrap, delegation policy, env-file bootstrap, bug-queue routing, auto quiet, caveman mode, input compression, scratchpad delivery keys, fresh-context markers, full-autonomy mode, automation modes, auto orchestration, and phase governance integration — remains undocumented in the framework README's `## Commands and workflow` operator catalog. US-0117 closes this gap by adding the 5th umbrella `### Phase & role governance` (sibling to the 4 prior umbrellas) plus 18 per-feature `#### US-xxxx` subsections, and extends the scratchpad reference with a 5th sibling `### Phase & role governance keys` sub-block.

## 18 per-feature subsections planned (AC-2)

| US-id | Feature |
|-------|---------|
| US-0069 | Phase→role matrix |
| US-0070 | Phase selection policy |
| US-0071 | Metadata sanitization |
| US-0072 | Context slimming |
| US-0075 | Scratchpad example-first refresh |
| US-0076 | Codebase map |
| US-0077 | Delegation policy |
| US-0078 | Env file bootstrap |
| US-0079 | Bug queue routing |
| US-0080 | Auto quiet mode |
| US-0081 | Caveman mode |
| US-0082 | Input compression |
| US-0083 | Scratchpad delivery keys |
| US-0085 | Context fresh-context markers |
| US-0087 | Full-autonomy mode |
| US-0088 | Automation modes |
| US-0089 | Auto orchestration |
| US-0090 | Phase governance integration |

## Umbrella + scratchpad ref sub-block names

- **Umbrella section name**: `### Phase & role governance` (5th sibling, inserted after US-0116's `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` at L1665).
- **Scratchpad ref sub-block name**: `### Phase & role governance keys` (5th sibling, inserted after US-0116's `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` sub-block at L2225).

## Net-new keys preview (from `.cursor/scratchpad.md` grep)

Confirmed present in scratchpad (sampled via grep — TL research phase resolves the authoritative 18-feature key surface):

- Phase governance: `AUTO_PHASE_PLAN`, `AUTO_PHASE_EXCLUDE`, `AUTO_PHASE_INCLUDE`, `AUTO_PHASE_PROFILE`
- Role governance: `AUTO_ROLE_RESEARCH`, `AUTO_ROLE_PLAN_VERIFY`, `AUTO_ROLE_REFRESH_CONTEXT` (per-role override pattern)
- Automation / orchestration: `AUTO_FLOW_MODE`, `AUTO_BACKLOG_DRAIN`, `AUTO_BACKLOG_MAX_STORIES`, `AUTO_BACKLOG_ON_BLOCK`, `AUTO_STORY_SELECTION`, `AUTO_BUG_QUEUE`, `AUTO_BUG_TARGET`, `AUTO_BUG_MAX_ITEMS`, `AUTO_BUG_ON_BLOCK`, `AUTO_QUIET`, `AUTO_EXECUTE_BULK`, `AUTO_EXECUTE_MAX_ITEMS`, `AUTO_EXECUTE_ON_BLOCK`, `AUTO_EXECUTE_SELECTION`, `AUTO_TEAM_SCOPE_ENFORCE`
- Voice / compression: `CAVEMAN_MODE`, `CAVEMAN_COMPRESS_INPUT`, `CAVEMAN_COMPRESS_SCOPE_*`
- Hard caps: `AUTO_LOOP_MAX_CYCLES`, `AUTO_BLOCK_RETRY_MAX`, `AUTO_OUTER_DRIVER_TIMEOUT_SECONDS`
- Other governance (isolated-context, sanitization, slimming, example-first, codebase map, delegation, env file, delivery keys, fresh-context markers): keys not surfaced as top-level scratchpad variable names in the materialized `.cursor/scratchpad.md` — likely documented as inline prose / reason codes / runbook cross-link targets rather than top-level key rows. **Open question Q-1 for TL research**: confirm the exact key names (or reason-code families) for US-0071 sanitization, US-0072 slimming, US-0075 example-first, US-0076 codebase map, US-0077 delegation, US-0078 env file, US-0083 delivery keys, US-0085 fresh-context markers — these may surface as `*_REASON_CODE` families, `ISOLATION_EVIDENCE` / `FRESH_CONTEXT_MARKER` literals, or runbook-only contracts rather than scratchpad key rows.

## Cross-link pointer candidates (overlapping keys with prior blocks — angle-distinct narrative)

- **AUTO_BACKLOG_DRAIN / AUTO_BUG_QUEUE / AUTO_STORY_SELECTION / AUTO_BACKLOG_MAX_STORIES / AUTO_BACKLOG_ON_BLOCK** → overlap with US-0116 `### Delivery & lifecycle keys` (L2225) and US-0113 `### Sovereign-loop era keys` (L1881). US-0117 angle = phase & role governance (drain-as-phase-execution-shape); US-0116 angle = delivery & lifecycle; US-0113 angle = sovereign-loop era. **Cross-link pointer only — no duplicate key rows.**
- **AUTO_FLOW_MODE / AUTO_LOOP_MAX_CYCLES / AUTO_BLOCK_RETRY_MAX / AUTO_OUTER_DRIVER_TIMEOUT_SECONDS** → overlap with US-0113 `### Sovereign-loop era keys` (L1881). US-0117 angle = phase & role governance (full-autonomy as phase-governance policy); US-0113 angle = sovereign-loop era. **Cross-link pointer only.**
- **AUTO_QUIET** → may overlap with US-0113 sovereign-loop keys (quiet mode as loop ergonomics). US-0117 angle = automation mode ergonomics. **Verify in research; cross-link pointer if overlap confirmed.**
- **CAVEMAN_MODE / CAVEMAN_COMPRESS_INPUT** → no prior-block overlap expected (caveman + compression are net-new to the 5th block). **Confirm in research.**
- **AUTO_ROLE_* family** → net-new (role governance is US-0117-distinct). No prior-block overlap.
- **AUTO_PHASE_* family** → net-new (phase selection policy is US-0117-distinct). No prior-block overlap.
- **DELIVERY_KEYS / ISOLATION_EVIDENCE / FRESH_CONTEXT_MARKER / METADATA_SANITIZATION / CONTEXT_SLIMMING / EXAMPLE_FIRST / CODEBASE_MAP / DELEGATION_POLICY / ENV_FILE_BOOTSTRAP / BUG_QUEUE_ROUTING / AUTO_ORCHESTRATION / PHASE_GOVERNANCE** → grep returned no top-level scratchpad key rows for these literals; likely runbook-cross-link-only or reason-code-family entries. **TL research resolves whether these are key rows or prose-only cross-links.**

**Angle-distinct narrative pattern** (established S0113–S0116, scaled to 5th story): each overlapping key gets a single canonical key row in its owning block + cross-link pointer in the non-owning block. US-0117 owns phase & role governance angle; prior blocks retain their canonical rows. **No duplicate key rows.**

## Runbook cross-link targets (AC-7) — candidates per feature

TL research phase must confirm exact anchors + line numbers. Candidate targets identified via runbook grep:

| Feature | Runbook cross-link candidate |
|---------|-------------------------------|
| US-0069 (Phase→role matrix) | runbook phase-role section (grep `phase-role`) |
| US-0070 (Phase selection policy) | `/auto` + DEC-0052 phase profile contract |
| US-0071 (Metadata sanitization) | runbook metadata / user-visible metadata guard |
| US-0072 (Context slimming) | TOKEN_PROFILE / DEC-0035 |
| US-0075 (Scratchpad example-first refresh) | scratchpad refresh contract |
| US-0076 (Codebase map) | `### Codebase map bootstrap` (US-0082) |
| US-0077 (Delegation policy) | delegation / DEC-0067 |
| US-0078 (Env file bootstrap) | env file bootstrap contract |
| US-0079 (Bug queue routing) | bug queue routing / DEC-0061 |
| US-0080 (Auto quiet mode) | DEC-0035 / US-0080 |
| US-0081 (Caveman mode) | `### Caveman input compression (US-0090)` L2099 + `.cursor/rules/caveman.mdc` |
| US-0082 (Input compression) | `### Caveman input compression (US-0090)` L2099 |
| US-0083 (Scratchpad delivery keys) | DEC-0060 / scratchpad delivery keys contract |
| US-0085 (Context fresh-context markers) | fresh-context marker / DEC-0029 |
| US-0087 (Full-autonomy mode) | `/auto` full-autonomy + DEC-0078 |
| US-0088 (Automation modes) | `/auto` automation modes |
| US-0089 (Auto orchestration) | `/auto` orchestration |
| US-0090 (Phase governance integration) | phase governance integration / DEC-0052 |

## Test markers (5 — same as prior stories)

- `tests/scratchpad_example_parity_test.py` (4 tests — byte-parity + scratchpad example parity)
- `scripts/validate_readme_feature_coverage.py --enforce` (README ↔ backlog coverage gate)
- `scripts/validate_doc_profile.py` (doc profile gate)
- `scripts/check-user-visible-metadata.py` (user-visible metadata guard)
- `scripts/check_intake_template_parity.py` (intake template parity)

## Compose guards UNCHANGED (23 cumulative — confirm)

23 compose guards from US-0116 carry forward unchanged: US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062. US-0117 documentation-only; lives entirely outside compose surface. **Confirm in research: no new compose guards required for US-0117.**

## DC resolution scope — final deferred-candidate resolution point

US-0117 is the **final story in the 5-story drain** and the natural owner of the architecture.md triad hygiene closure. It inherits 18 missing `# US-xxxx` h1 anchors in active `architecture.md`:

- **DC-1** (5 anchors): US-0103, US-0104, US-0105, US-0107, US-0110 (sovereign-loop era — US-0113 family)
- **DC-2** (2 anchors): US-0041, US-0062 (release & distribution — US-0114 family)
- **DC-3** (7 anchors): US-0034, US-0084, US-0086, US-0093, US-0096, US-0101, US-0102 (integration & observability — US-0115 family)
- **DC-4** (4 anchors): US-0092, US-0095, US-0098, US-0099 (delivery & lifecycle — US-0116 family)

**Total: 18 missing `# US-xxxx` h1 anchors.** US-0117 should RESOLVE these 18 anchors (add the h1 anchors to `architecture.md`) as part of its scope — this is the **final deferred-candidate resolution point**. The resolution approach (add in `/architecture` vs `/execute`) is an open question for TL research (Q-2 below). Not appended to `handoffs/sovereign_deferrals.jsonl` in spec phase — orchestrator's segment-boundary advance hook handles it.

## 5th-story cumulative byte-stability surface note

US-0117 is the **5th and final story** in the 5-story drain. The cumulative byte-stability surface grows to 5 blocks:

- US-0113 `### Sovereign-loop era (US-0103–US-0112) umbrella section` (L940) + `### Sovereign-loop era keys (US-0103–US-0112)` (L1881)
- US-0114 `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112) umbrella section` (L1225) + `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` (L2005)
- US-0115 `### Integration & observability (...) umbrella section` (L1410) + `### Integration & observability keys (...)` (L2077)
- US-0116 `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` (L1665) + `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` (L2225)
- US-0117 `### Phase & role governance` (NEW) + `### Phase & role governance keys` (NEW) — to be added in `/execute`.

**Byte-stability contract**: prior 4 released blocks (US-0113/US-0114/US-0115/US-0116 umbrella + keys) must remain byte-identical between `its_magic/README.md` and `template/its_magic/README.md`. US-0117 adds cross-link pointers + reason-code-only entries + net-new key rows only, never edits prior released blocks. `PARITY_OK <size> <size>` is the authoritative end-to-end byte-stability proof. **First 5-cumulative-surface story.**

## Open questions for TL research

1. **Q-1 (key surface)**: Confirm exact key names (or reason-code families) for the 18 features — especially US-0071 sanitization, US-0072 slimming, US-0075 example-first, US-0076 codebase map, US-0077 delegation, US-0078 env file, US-0083 delivery keys, US-0085 fresh-context markers. Grep of `.cursor/scratchpad.md` surfaced AUTO_PHASE_*, AUTO_ROLE_*, AUTO_FLOW_MODE, AUTO_BACKLOG_*, AUTO_BUG_*, AUTO_QUIET, CAVEMAN_*, AUTO_EXECUTE_*, AUTO_TEAM_SCOPE_ENFORCE, AUTO_LOOP_MAX_CYCLES, AUTO_BLOCK_RETRY_MAX, AUTO_OUTER_DRIVER_TIMEOUT_SECONDS as top-level key rows; the remaining literals (METADATA_SANITIZATION, CONTEXT_SLIMMING, EXAMPLE_FIRST, CODEBASE_MAP, DELEGATION_POLICY, ENV_FILE_BOOTSTRAP, BUG_QUEUE_ROUTING, DELIVERY_KEYS, ISOLATION_EVIDENCE, FRESH_CONTEXT_MARKER, AUTO_ORCHESTRATION, PHASE_GOVERNANCE) returned no top-level matches and may be reason-code families, prose-only contracts, or runbook-cross-link-only entries. TL research must resolve.
2. **Q-2 (DC anchor resolution approach)**: Should the 18 missing `# US-xxxx` h1 anchors be added in `/architecture` (recommended — architecture owns h1 anchors per `docs/engineering/artifact-ownership-policy.md`) or `/execute`? US-0117 inherits DC-1+DC-2+DC-3+DC-4 = 18 anchors as the final deferred-candidate resolution point.
3. **Q-3 (18-feature scope size)**: Should T-002 (per-feature subsections) be split into 2 batches (e.g., 9+9) or handled as one 18-subsection pass? Recommend TL evaluates task decomposition shape — 18 subsections is 2–4× prior stories' T-002 load (4–9 subsections).
4. **Q-4 (overlap with prior stories' content)**: Confirm angle-distinct narrative for AUTO_BACKLOG_DRAIN/AUTO_BUG_QUEUE (overlap with US-0116 delivery & lifecycle + US-0113 sovereign-loop), AUTO_FLOW_MODE/AUTO_LOOP_MAX_CYCLES (overlap with US-0113 sovereign-loop), AUTO_QUIET (possible overlap with US-0113). Each overlapping key gets a single canonical row in its owning block + cross-link pointer in US-0117's block.
5. **Q-5 (runbook anchor gaps)**: Confirm exact runbook anchors + line numbers for all 18 features (AC-7). Candidates identified via grep but line numbers / h-level must be verified.
6. **Q-6 (byte-stability contract on 5th cumulative surface)**: Confirm `PARITY_OK` proof shape + that prior 4 blocks (US-0113/US-0114/US-0115/US-0116) remain byte-identical post-US-0117.
7. **Q-7 (R-0105 research entry)**: US-0117 needs R-0105 in `docs/engineering/research.md` (continuing from R-0104 US-0116). TL research phase creates it.
8. **Q-8 (US-0117 architecture.md anchor)**: `## US-0117` h1 anchor is missing in `architecture.md` (grep `^## US-011[3-7]` returned only `## US-0115` L1117 + `## US-0116` L1265). US-0117 needs its own anchor in `/architecture` phase — NOT this phase.

## Phases merged (ultra_lean)

intake + discovery → spec macro-phase (this handoff). Next canonical phase: `/research` (tech-lead, `plan` macro — first canonical phase). In ultra_lean, research is merged into `plan` macro; orchestrator Task-spawns TL for `plan` macro.

## Handoff

- **Next phase**: `/research` (tech-lead) — `plan` macro first canonical phase
- **Next role**: tech-lead
- **fresh_context_marker**: po-US0117-spec-20260704T163100Z-fresh
- **timestamp**: 2026-07-04T16:31:00Z (UTC)

STOP after spec handoff. The orchestrator Task-spawns the Tech Lead subagent for `research` (first canonical phase of the `plan` macro). Hand off via artifacts only.

---
- `timestamp=2026-06-30T22:30:00Z`
- `phase_id=sprint-plan`
- `role=tech-lead`
- `story_id=US-0112`
- `sprint_id=S0112`
- `orchestrator_run_id=auto-20260628-04`
- `fresh_context_marker=tl-US0112-sprintplan-20260630T223000Z-fresh`
- `verdict=PASS`
- `next_phase=/plan-verify`
- `next_role=qa`

### Summary

- **`/sprint-plan`** **PASS** — sprint **S0112** created: 11 atomic tasks **T-001..T-011** within **SPRINT_MAX_TASKS=12** (no split); **AC-1..AC-8** surjective map confirmed; **DEC-0112** referenced (Accepted; installer payload composes DEC-0086/DEC-0087); **R-0090** referenced (delivered, Q1–Q8 closed).
- Compose guards confirmed **UNCHANGED**: US-0008, US-0040, US-0054, US-0100, US-0101, US-0102, US-0103, US-0107, US-0110 — DO NOT amend.
- 12 `test_us0112_*` markers committed; parity `--scope=model-catalog-examples` (`MODEL_CATALOG_EXAMPLE_PAIRS`, 16 pairs).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Sprint S0112 artifacts

- `sprints/S0112/sprint.json`, `sprint.md`, `tasks.md`, `sprint-plan.json` — sprint metadata + 11-task breakdown + AC surjective map
- `docs/product/backlog.md` `## US-0112` — `sprint_plan_notes` appended
- `docs/engineering/state.md` — `Sprint-plan checkpoint (2026-06-30) -- US-0112` + isolation evidence + runtime proof
- `handoffs/resume_brief.md` — top pointer → `/plan-verify`
- `handoffs/po_to_tl.md` — this handoff appended

### Next phase contract

**`/plan-verify`** (fresh **QA** subagent spawn) — validate AC→task surjective map, task list, parity scope, compose guards unchanged, 8+ test markers present, DEC-0112/R-0090 references intact.

### Isolation evidence (US-0048 / DEC-0029)

- `fresh_context_marker=tl-US0112-sprintplan-20260630T223000Z-fresh`
- `timestamp=2026-06-30T22:30:00Z`
- `evidence_ref=sprints/S0112/sprint.json,sprints/S0112/sprint-plan.json,sprints/S0112/tasks.md,docs/product/backlog.md (## US-0112 sprint_plan_notes),docs/engineering/state.md (sprint-plan checkpoint),handoffs/resume_brief.md,handoffs/po_to_tl.md (this handoff)`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260628-04`
- `runtime_proof_id=rp-auto-20260628-04-sprintplan-tech-lead-20260630T223000Z-US0112`
- `phase_id=sprint-plan`
- `role=tech-lead`
- `proof_issued_at=2026-06-30T22:30:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=sprintplan-pass-us0112-20260630T223000Z`

---

## Orchestrated research handoff — US-0112 / auto-20260628-04 (research PASS tl, next `/architecture` tech-lead)

- `timestamp=2026-06-30T20:45:00Z`
- `phase_id=research`
- `role=tech-lead`
- `story_id=US-0112`
- `sprint_id=(none)`
- `orchestrator_run_id=auto-20260628-04`
- `fresh_context_marker=tl-US0112-research-20260630T204500Z-fresh`
- `verdict=PASS`
- `next_scheduled_phase=architecture`
- `default_spawn_role=tech-lead`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=1`
- `portfolio_open_stories=1` (US-0112)
- `portfolio_open_bugs=0`
- `delivery_mode=standard`
- `token_profile=lean`
- `caveman_mode=1`
- `caveman_level=full`
- `model_tier_default=balanced`
- `AUTO_QUIET=1`
- `native_chain_active=true`
- `native_chain_continuing=true`

### Summary

- **`/research`** **PASS** — R-0090 delivered (Q1–Q8 closed); 8 preset filenames confirmed (scratchpad L352-359 + glob verify); manifest `[install_include_paths]` line-based, active+template byte-parity (16 rows); missing mode = copy when absent (same semantics as scratchpad.local.example.md); upgrade classification = **framework** files (refresh when template differs, skip unchanged; same semantics as US-0075/US-0018/US-0057 — no new classification mechanism); triple installer touch-points (installer.py / installer.ps1 / installer.sh, single manifest-driven source of truth); runbook anchor = docs/engineering/runbook.md § model tier / catalog (operator copies preset → `model-catalog.local.json`; lists all 8 filenames + complexity/role intent); 8+ `test_us0112_*` markers + `--scope=model-catalog-examples` with `MODEL_CATALOG_EXAMPLE_PAIRS` (active vs template manifest byte-parity); companion DEC-0112 required at `/architecture` (installer payload decision — manifest rows, framework classification, active-catalog exclusion; composes with DEC-0086/DEC-0087 without amending schema or precedence).
- Task seeds: T-001..T-011 (11, within SPRINT_MAX_TASKS=12); surjective AC map AC-1..AC-8 → T-001..T-011.
- Compose guards confirmed (DO NOT amend): US-0008, US-0040, US-0054, US-0100, US-0101, US-0102, US-0103, US-0107, US-0110.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Research closure (Q1–Q8 closed)

| Q | Topic | Answer |
|---|-------|--------|
| Q1 | 8 preset filenames | `.cursor/model-catalog.local.example.json`, `.cursor-only.json`, `.level-1-easy.json`, `.level-2-complex.json`, `.level-3-mega.json`, `.level-4-super.json`, `.role-based-balanced.json`, `.role-based-highend.json` (scratchpad L352-359 + glob verify) |
| Q2 | Manifest format | `[install_include_paths]` line-based relative paths (one row per file); active `docs/engineering/context/installer-owned-paths.manifest` + `template/docs/engineering/context/installer-owned-paths.manifest` byte-parity (16 rows total; both currently identical) |
| Q3 | Missing mode semantics | Copy when absent, deterministic log/status per file (names-only); same semantics as `scratchpad.local.example.md` (US-0075) |
| Q4 | Upgrade classification | **Framework** files — refresh when template differs, skip unchanged; same semantics as US-0075 / US-0018 / US-0057 framework rules (no new classification mechanism) |
| Q5 | Triple installer parity | `installer.py` / `installer.ps1` / `installer.sh` all read single `[install_include_paths]` manifest; `List-SourceFiles` / equivalent includes all 8 examples from packaged `template/` |
| Q6 | Runbook section | `docs/engineering/runbook.md` § model tier / catalog subsection; documents: examples ship on install/upgrade; operator copies chosen preset → `model-catalog.local.json`; lists all 8 preset filenames + complexity/role intent (pointer to scratchpad comment block lines 351-360) |
| Q7 | Test markers + parity scope | 8+ `test_us0112_*` markers (manifest 8 paths, missing adds, upgrade refreshes, upgrade preserves unchanged, local never touched, triple parity, runbook literals, parity scope); `--scope=model-catalog-examples` with `MODEL_CATALOG_EXAMPLE_PAIRS` constant (active vs template manifest byte-parity check) |
| Q8 | Companion DEC-0112 | **Required** at `/architecture` — installer payload decision (manifest rows, framework classification, active-catalog exclusion); composes with DEC-0086 / DEC-0087 without amending catalog schema or model precedence |

### Top risks (R1–R6, carry to architecture)

- **R1** Stale upgrade when example filename changes — deterministic manifest list + idempotent upgrade copy prevents prior-version file deletion.
- **R2** Operator confusion if all 8 land but none selected — runbook recipe mandatory (L7).
- **R3** Active catalog accidental install — manifest exclusion invariant (L5) + regression guard test.
- **R4** Triple installer drift — single manifest-driven source of truth; parity test (L9).
- **R5** npm `package.json` files gap — already covered by `template/` glob, verify at architecture.
- **R6** US-0075 / US-0018 precedence — same framework-file semantics; additive only.

### Task seeds (T-001..T-011, surjective AC map; SPRINT_MAX_TASKS=12)

| T | AC | Description |
|---|----| ---- |
| T-001 | AC-1 | Add 8 model-catalog.local.example*.json rows to active `docs/engineering/context/installer-owned-paths.manifest` under `[install_include_paths]` |
| T-002 | AC-2/3 | Mirror manifest rows in `template/docs/engineering/context/installer-owned-paths.manifest` (byte-parity) |
| T-003 | AC-2/5 | Verify missing-mode `installer.py` logic adds absent framework files (same semantics as scratchpad.local.example.md) |
| T-004 | AC-3/4 | Verify upgrade-mode logic refreshes stale framework files, skips unchanged, never touches active `model-catalog.local.json` |
| T-005 | AC-4 | Verify manifest exclusion invariant (`.cursor/model-catalog.local.json` absent from manifest); add regression guard test |
| T-006 | AC-5 | Add `MODEL_CATALOG_EXAMPLE_PAIRS` constant + `--scope=model-catalog-examples` argument to `check_intake_template_parity.py` |
| T-007 | AC-6 | Write runbook §model-catalog preset recipe (operator copies one preset to `model-catalog.local.json`); lists all 8 filenames + complexity/role intent |
| T-008 | AC-7 | Write 8+ `test_us0112_*` contract test markers (manifest paths, missing adds, upgrade refreshes, upgrade preserves unchanged, local never touched, triple parity, runbook literals, parity scope) |
| T-009 | AC-8 | Document architecture notes in `docs/engineering/architecture.md` `# US-0112` (framework vs operator boundary, manifest rows, upgrade classification, DEC-0086/DEC-0087 compose) |
| T-010 | AC-8 | Author companion `DEC-0112` (installer payload decision — manifest rows, framework classification, active-catalog exclusion) |
| T-011 | AC-8 | Verify template parity for all touched files (manifest, runbook, architecture) |

### Compose guards confirmed

- **US-0008** (installer): manifest-driven copy semantics unchanged.
- **US-0040** (release notes): per-sprint notes semantics unchanged.
- **US-0054** (release publish): configurable publish unchanged.
- **US-0100** (version changelog): semper changelog semantics unchanged.
- **US-0101** (model tiers DEC-0086): catalog schema unchanged.
- **US-0102** (role catalog DEC-0087): role catalog precedence unchanged.
- **US-0103** (AI decision ledger): ledger semantics unchanged.
- **US-0107** (sovereign loop): sovereign loop semantics unchanged.
- **US-0110** (goal convergence): convergence semantics unchanged.

### Evidence refs

- `docs/engineering/research.md` (R-0090 delivered; Q1–Q8 closed)
- `docs/product/backlog.md` (`## US-0112` — discovery_locks_L1_L10 + research_notes)
- `docs/engineering/state.md` (research checkpoint + phase boundary + isolation evidence + strict runtime proof)
- `handoffs/po_to_tl.md` (this handoff)
- `handoffs/resume_brief.md` (top pointer to /architecture)
- `docs/engineering/context/installer-owned-paths.manifest` (current — 44 install_include_paths, no model-catalog lines yet)
- `template/docs/engineering/context/installer-owned-paths.manifest` (current — byte-parity with active)

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=research`
- `role=tech-lead`
- `fresh_context_marker=tl-US0112-research-20260630T204500Z-fresh`
- `timestamp=2026-06-30T20:45:00Z`
- `evidence_ref=docs/engineering/research.md (R-0090 delivered),docs/product/backlog.md (## US-0112 research_notes),docs/engineering/state.md (research checkpoint),handoffs/po_to_tl.md (this handoff)`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260628-04`
- `runtime_proof_id=rp-auto-20260628-04-research-tech-lead-20260630T204500Z-US0112`
- `phase_id=research`
- `role=tech-lead`
- `proof_issued_at=2026-06-30T20:45:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=research-pass-us0112-20260630T204500Z`

Canonical payload: `{"orchestrator_run_id":"auto-20260628-04","phase_id":"research","proof_issued_at":"2026-06-30T20:45:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260628-04-research-tech-lead-20260630T204500Z-US0112"}`.

### Boundary verification (research phase, no upstream proof change consumed)

- Prior discovery proof consumed: `rp-auto-20260628-04-discovery-po-20260630T203000Z-US0112` (from `handoffs/po_to_tl.md` discovery section, unchanged)
- Current research-phase strict proof recorded above
- Research verdict: **PASS** (Q1–Q8 closed; DEC-0112 required; 11 task seeds within threshold)

### Decision gate

- **None** — research satisfied; architecture readiness explicit.

### Next

- **`/architecture`** (fresh **tech-lead**) for **US-0112** — confirm R-0090 locks sufficient; seed 11 tasks T-001..T-011; AC-1..AC-8 surjective map; author `# US-0112` + `DEC-0112`.

### Stop condition (BUG-0006)

- STOP after research phase completes. Hand off via artifacts only. Do not execute `/architecture` in this turn. Orchestrator MUST Task-spawn next phase.

---

## Orchestrated discovery handoff — US-0112 / auto-20260628-04 (discovery PASS po, next `/research` tech-lead)

- `timestamp=2026-06-30T20:35:00Z`
- `phase_id=discovery`
- `role=po`
- `story_id=US-0112`
- `sprint_id=(none)`
- `orchestrator_run_id=auto-20260628-04`
- `fresh_context_marker=po-US0112-discovery-20260630T203000Z-fresh`
- `verdict=PASS`
- `next_scheduled_phase=research`
- `default_spawn_role=tech-lead`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=1`
- `portfolio_open_stories=1` (US-0112)
- `portfolio_open_bugs=0`
- `delivery_mode=standard`
- `token_profile=lean`
- `caveman_mode=1`
- `caveman_level=full`
- `model_tier_default=balanced`
- `AUTO_QUIET=1`

### Summary

- **`/discovery`** **PASS** — installer framework-file delivery locked: 8 `template/.cursor/model-catalog.local.example*.json` presets added to `[install_include_paths]`; classified as **framework** files (refresh on `upgrade` when template diff, add on `missing` when absent); **never** touch gitignored `.cursor/model-catalog.local.json`; triple installer parity; runbook recipe; 8+ `test_us0112_*` markers; parity `--scope=model-catalog-examples`. Compose guards confirmed: DO NOT amend US-0008, US-0040, US-0054, US-0100, US-0101, US-0102, US-0103, US-0107, US-0110.
- Companion **DEC-0112** recommended (installer payload decision — manifest rows, framework classification, active-catalog exclusion).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (L1–L10, research inputs)

| Lock | Decision |
|------|----------|
| **L1** (eight presets exact) | `.cursor/model-catalog.local.example.json`, `.cursor/model-catalog.local.example.cursor-only.json`, `.cursor/model-catalog.local.example.level-1-easy.json`, `.cursor/model-catalog.local.example.level-2-complex.json`, `.cursor/model-catalog.local.example.level-3-mega.json`, `.cursor/model-catalog.local.example.level-4-super.json`, `.cursor/model-catalog.local.example.role-based-balanced.json`, `.cursor/model-catalog.local.example.role-based-highend.json` |
| **L2** (manifest rows) | active `docs/engineering/context/installer-owned-paths.manifest` + `template/docs/engineering/context/installer-owned-paths.manifest` list all 8 paths under `[install_include_paths]` |
| **L3** (missing mode) | `installer.py` / `installer.ps1` / `installer.sh` `missing` mode copies each example into target `.cursor/` when absent; deterministic log/status per file (names-only) |
| **L4** (upgrade framework refresh) | `upgrade` mode classifies `model-catalog.local.example*.json` as framework; overwrite when template content differs (same semantics as `scratchpad.local.example.md` per US-0075); unchanged examples counted as unchanged |
| **L5** (active catalog protection) | `.cursor/model-catalog.local.json` remains gitignored and outside `install_include_paths` and `clean_paths`; no installer mode copies template examples to that path |
| **L6** (triple installer parity) | PS1, Bash, Python manifest-driven file set identical; `List-SourceFiles` / equivalent includes all 8 examples from packaged `template/` |
| **L7** (runbook recipe) | `docs/engineering/runbook.md` § model tier / catalog documents: examples ship on install/upgrade; operator copies chosen preset → `model-catalog.local.json`; lists all 8 filenames + complexity/role intent |
| **L8** (test markers) | 8+ `test_us0112_*` markers (manifest 8 paths, missing adds, upgrade refreshes, upgrade preserves unchanged, local never touched, triple parity, runbook literals, parity scope) |
| **L9** (parity scope) | `check_intake_template_parity.py --scope=model-catalog-examples` with `MODEL_CATALOG_EXAMPLE_PAIRS` manifest |
| **L10** (architecture section) | `docs/engineering/architecture.md` `# US-0112` documents framework vs operator boundary, manifest rows, upgrade classification, DEC-0086/DEC-0087 compose |

### AC → Task seed mapping (surjective)

| AC | Task seeds |
|----|------------|
| AC-1 (manifest completeness) | T-001 (active+template manifest 8 paths) |
| AC-2 (missing mode delivery) | T-002 (installer.py), T-003 (installer.ps1), T-004 (installer.sh) |
| AC-3 (upgrade framework refresh) | T-002, T-003, T-004 (same installer touch-points + upgrade classification) |
| AC-4 (active catalog protection) | T-001 (manifest exclusion + regression guard) |
| AC-5 (triple installer parity) | T-002, T-003, T-004 + T-005 (parity scope) |
| AC-6 (runbook recipe) | T-007 (runbook) |
| AC-7 (contract tests + parity) | T-006 (8+ test_us0112_* markers), T-005 (parity) |
| AC-8 (architecture notes) | T-008 (architecture.md + DEC-0112) |

Companion **DEC-0112** recommended at /architecture (installer payload decision).

### Top risks (carry to /research)

- **R1** Stale upgrade when example filename changes (add vs rename) — deterministic manifest list + idempotent upgrade copy prevents deletion of prior-version files
- **R2** Operator confusion if all 8 land but none selected — runbook recipe mandatory (L7)
- **R3** Active catalog accidental install — manifest exclusion invariant (L5) + regression guard test
- **R4** Triple installer drift — single manifest-driven source of truth; parity test (L9)
- **R5** npm `package.json` files gap — already covered by `template/` glob but verify at /research
- **R6** US-0075 / US-0018 precedence — same framework-file semantics; no new classification mechanism (additive only)

### Research asks (extend R-0090)

1. **Q1**: Confirm exact 8 filenames vs scratchpad comment block (lines 351–360)
2. **Q2**: Manifest `[install_include_paths]` section format + active/template byte-parity
3. **Q3**: Missing-mode deterministic log tokens per file (names-only)
4. **Q4**: Upgrade classification precedence vs US-0075 / US-0018 / US-0057 framework rules
5. **Q5**: Triple installer touch-points — single manifest-driven source of truth (`installer.py` / `installer.ps1` / `installer.sh`)
6. **Q6**: Runbook section anchor (which § heading, which subsection)
7. **Q7**: Test marker inventory (8+ `test_us0112_*`) + `MODEL_CATALOG_EXAMPLE_PAIRS` parity manifest
8. **Q8**: Companion DEC-0112 necessity (installer payload decision)

### Evidence refs

- `docs/product/backlog.md` (`## US-0112` — `discovery_notes` + `discovery_locks_L1_L10` + `discovery_risks_R1_R6`)
- `docs/engineering/research.md` (**R-0090** — discovery stub; extend with Q1–Q8 at /research)
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/intake_evidence/US-0112-intake-20260628.json`
- `handoffs/po_to_tl.md` (this handoff)
- `handoffs/resume_brief.md` (top pointer → `/research`)
- Compose surfaces (DO NOT amend): **US-0008**, **US-0040**, **US-0054**, **US-0100**, **US-0101**, **US-0102**, **US-0103**, **US-0107**, **US-0110**
- Prior DONE precedent: **US-0075** (scratchpad example-first refresh), **US-0018** (smart upgrade), **US-0099** (dev-environment copy-when-missing)

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=discovery`
- `role=po`
- `fresh_context_marker=po-US0112-discovery-20260630T203000Z-fresh`
- `timestamp=2026-06-30T20:35:00Z`
- `evidence_ref=docs/product/backlog.md,docs/engineering/state.md,handoffs/po_to_tl.md,handoffs/resume_brief.md,handoffs/intake_evidence/US-0112-intake-20260628.json`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260628-04`
- `runtime_proof_id=rp-auto-20260628-04-discovery-po-20260630T203000Z-US0112`
- `phase_id=discovery`
- `role=po`
- `proof_issued_at=2026-06-30T20:35:00Z`
- `proof_ttl_seconds=3600`

Canonical: `{"orchestrator_run_id":"auto-20260628-04","phase_id":"discovery","proof_issued_at":"2026-06-30T20:35:00Z","proof_ttl_seconds":3600,"role":"po","runtime_proof_id":"rp-auto-20260628-04-discovery-po-20260630T203000Z-US0112","story_id":"US-0112"}`.

### Next

- **`/research`** (fresh **tech-lead** context) for **US-0112** — extend **R-0090** with Q1–Q8; confirm 8 presets, manifest format, upgrade classification, triple parity touch-points, runbook anchor, test markers + `MODEL_CATALOG_EXAMPLE_PAIRS`, companion **DEC-0112**.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

## Orchestrated research handoff — US-0108 / auto-20260628-04 (research PASS, next `/architecture` tech-lead)

- `timestamp=2026-06-29T20:30:00Z`
- `phase_id=research`
- `role=tech-lead`
- `story_id=US-0108`
- `sprint_id=(none)`
- `orchestrator_run_id=auto-20260628-04`
- `fresh_context_marker=tl-US0108-research-20260629T023000Z-fresh`
- `verdict=PASS`
- `next_scheduled_phase=architecture`
- `default_spawn_role=tech-lead`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=3`
- `drain_terminated=false`
- `native_chain_active=true`
- `native_chain_continuing=true`
- `drain_advance_action=spawned`
- `portfolio_open_stories=4` (US-0108, US-0109, US-0111, US-0112)
- `portfolio_open_bugs=0`
- `delivery_mode=standard`
- `token_profile=lean`
- `caveman_mode=1`
- `caveman_level=full`
- `model_tier_default=balanced`
- `AUTO_QUIET=1`

### Summary

- **`/research`** **PASS** — **R-0096** Q1–Q10 confirmed CLOSED; delivery-closure trailer appended. Companion **DEC-0108** locked (`decisions/DEC-0108.md`).
- No new research questions surfaced — Q1–Q10 from discovery already closed at prior architecture checkpoint.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Research closure (Q1–Q10 — already closed, confirmed)

| Q | Lock | Decision |
|---|------|----------|
| Q1 | Worktree naming + isolation | `.git/worktrees/us0108-<story_id>-<instance_idx>/`; per-worktree `GIT_DIR` + `GIT_WORK_TREE`; gitignore `.git/worktrees/us0108-*` |
| Q2 | Selection predicate | Filter `qa_verdict=PASS`; highest `anti_slop_score` (default `0`); ties break earliest `proof_issued_at`; single winner |
| Q3 | QA cross-review mode | Sequential N QA v1; optional `AUTO_SOVEREIGN_PARALLEL_QA=1` parallel v2 |
| Q4 | `parallel_dev_pick.json` v1 | `{story_id, winner_instance_id, worktree_path, qa_verdict, anti_slop_score, proof_issued_at, merge_policy, runner_ts_utc, orchestrator_run_id, loser_instance_ids[]}` |
| Q5 | Merge resolution | `first_pass_wins` default; `last_pass_wins`; `manual` → halt; bounded retry ≤2 |
| Q6 | Resource guard | `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL` system-wide cap; atomic lockfile `.git/us0108_parallel_dev.lock`; fail-fast `PARALLEL_DEV_RESOURCE_CAP_EXHAUSTED` |
| Q7 | Execute step integration | Step 25 (parallel dev); 26 (QA); 27 (selection); 28 (merge + cleanup) |
| Q8 | Backward compat | `SOVEREIGN_PARALLEL_DEV=0` = single dev unchanged; regression guard test |
| Q9 | Contract tests + parity | 8 `test_us0108_*` markers; parity `--scope=sovereign-parallel-dev` |
| Q10 | Compose surfaces (read-only) | US-0104 anti-slop (read); US-0103 ledger (read); US-0107 deferrals (read); US-0108 writes nothing to upstream schemas |

### Compose guards confirmed

- **US-0047**: bulk execute unchanged
- **US-0092**: full autonomy unchanged
- **US-0103**: ledger schema unchanged (read-only)
- **US-0104**: critic schema unchanged (read-only)
- **US-0107**: deferral register unchanged (read-only)

### Top risks (carry to /architecture)

- **R1** Worktree lock conflicts — deterministic naming + per-worktree GIT_DIR
- **R2** QA cross-review latency — sequential v1 preferred; parallel opt-in v2
- **R3** Merge conflicts — bounded retry ≤2 then manual halt
- **R4** Anti-slop unavailable — graceful degrade default `0`
- **R5** Resource cap race — atomic lockfile check-and-increment
- **R6** Bulk execute interaction — system-wide cap preferred v1

### Evidence refs

- `docs/engineering/research.md` (**R-0096** — delivery-closure trailer appended)
- `docs/product/backlog.md` (`## US-0108` — L1–L10 discovery locks)
- `decisions/DEC-0108.md` (companion decision, locked)
- `docs/engineering/state.md` (research checkpoint + phase boundary)
- `handoffs/po_to_tl.md` (this handoff)
- `handoffs/resume_brief.md` (top pointer)

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=research`
- `role=tech-lead`
- `fresh_context_marker=tl-US0108-research-20260629T023000Z-fresh`
- `timestamp=2026-06-29T20:30:00Z`
- `evidence_ref=docs/engineering/research.md,docs/engineering/state.md,decisions/DEC-0108.md,handoffs/po_to_tl.md,handoffs/resume_brief.md`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260628-04`
- `runtime_proof_id=rp-auto-20260628-04-research-tech-lead-20260629T203000Z-US0108`
- `phase_id=research`
- `role=tech-lead`
- `proof_issued_at=2026-06-29T20:30:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=cf8a2b7c1d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b`

Canonical payload: `{"orchestrator_run_id":"auto-20260628-04","phase_id":"research","proof_issued_at":"2026-06-29T20:30:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260628-04-research-tech-lead-20260629T203000Z-US0108"}`.

### Boundary verification (research phase, no upstream proof change consumed)

- Prior architecture proof consumed: `rp-auto-20260628-04-architecture-tech-lead-20260628T220000Z-US0108` (from `handoffs/po_to_tl.md` architecture section)
- Current research-phase strict proof recorded above
- Research verdict: **PASS** (no new questions — Q1–Q10 remain closed from prior cycle)

### Next

- **`/architecture`** (fresh **tech-lead**) for **US-0108** — confirm R-0096 locks sufficient; seed 11 tasks T-001..T-011; AC-1..AC-8 surjective map.

### Decision gate

- **None** — research satisfied; architecture readiness explicit.

---

## Orchestrated architecture handoff — US-0108 / auto-20260628-04

- `timestamp=2026-06-28T22:00:00Z`
- `phase_id=architecture`
- `role=tech-lead`
- `story_id=US-0108`
- `sprint_id=(none)`
- `orchestrator_run_id=auto-20260628-04`
- `fresh_context_marker=tl-US0108-architecture-20260628T220000Z-fresh`
- `verdict=PASS`
- `next_scheduled_phase=sprint-plan`
- `default_spawn_role=tech-lead`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=3`
- `drain_terminated=false`
- `native_chain_active=true`
- `native_chain_continuing=true`
- `drain_advance_action=spawned`
- `portfolio_open_stories=4` (US-0108, US-0109, US-0111, US-0112)
- `portfolio_open_bugs=0`
- `delivery_mode=standard`
- `token_profile=lean`
- `caveman_mode=1`
- `caveman_level=full`
- `model_tier_default=balanced`
- `AUTO_QUIET=1`

### Summary

- **`/architecture`** **PASS** — **R-0096** Q1–Q10 closed; companion **DEC-0108** ratified. Locked v1 schema for `parallel_dev_pick.json`, worktree naming `.git/worktrees/us0108-<story_id>-<instance_idx>/`, selection predicate (PASS → anti-slop desc → earliest proof_issued_at), merge resolution (`first_pass_wins|last_pass_wins|manual`), resource guard (`AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL=6` lockfile cap). Compose guards confirmed: DO NOT amend US-0047 / US-0092 / US-0103 / US-0104 / US-0107.
- **10 task seeds** (T-001..T-010) within **`SPRINT_MAX_TASKS=12`** threshold; **`SPRINT_AUTO_SPLIT`** not triggered.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Architecture locks (Q1–Q10 closed)

| Q | Lock | Decision |
|---|------|----------|
| Q1 | Worktree naming + isolation | `.git/worktrees/us0108-<story_id>-<instance_idx>/` deterministic; per-worktree `GIT_DIR` + `GIT_WORK_TREE` env; gitignore `.git/worktrees/us0108-*` |
| Q2 | Selection predicate | Filter `qa_verdict=PASS`; highest `anti_slop_score` (default `0`); ties break earliest `proof_issued_at`; single winner deterministic |
| Q3 | QA cross-review mode | Sequential N QA invocations v1 (ordered, deterministic); optional `AUTO_SOVEREIGN_PARALLEL_QA=1` parallel v2 |
| Q4 | `parallel_dev_pick.json` v1 schema | `{story_id, winner_instance_id, worktree_path, qa_verdict, anti_slop_score, proof_issued_at, merge_policy, runner_ts_utc, orchestrator_run_id, loser_instance_ids[]}` write-once |
| Q5 | Merge resolution | `first_pass_wins` (default); `last_pass_wins`; `manual` → `PARALLEL_DEV_PICK_MANUAL_REQUIRED`; conflict bounded retry ≤2 then manual |
| Q6 | Resource guard | `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL` system-wide cap; atomic lockfile `.git/us0108_parallel_dev.lock`; fail-fast `PARALLEL_DEV_RESOURCE_CAP_EXHAUSTED`; release on exit |
| Q7 | Execute step integration | Step 25 (parallel dev); 26 (QA cross-review); 27 (selection); 28 (merge + loser cleanup); after US-0107 step 24 + US-0047 step 22 |
| Q8 | Backward compat | `SOVEREIGN_PARALLEL_DEV=0` = single dev; no worktrees; regression guard `test_us0108_backward_compat_single_dev_unchanged` |
| Q9 | Contract test inventory + parity | 8 `test_us0108_*` markers; parity `--scope=sovereign-parallel-dev` (`SOVEREIGN_PARALLEL_DEV_PAIRS`) |
| Q10 | Compose surfaces (read-only) | US-0104 `anti_slop_score` (read); US-0103 ledger (read); US-0107 deferrals (read); US-0108 writes nothing to upstream schemas |

### AC → Task seed mapping (surjective)

| AC | Task seeds |
|----|------------|
| AC-1 (scratchpad keys) | T-001, T-002 |
| AC-2 (worktree isolation) | T-003 |
| AC-3 (model/lens diversity) | T-004 |
| AC-4 (selection predicate) | T-005 |
| AC-5 (merge policy + pick JSON) | T-006 |
| AC-6 (resource guard) | T-007 |
| AC-7 (execute steps 25-28) | T-008 |
| AC-8 (backward compat + tests + parity) | T-009, T-010 |

### Decision

- Compose guards confirmed: **US-0047/US-0092/US-0103/US-0104/US-0107** — do NOT amend; read-only integration only.
- **DEC-0108** authored — v1 schema + helper lib API + execute step hooks + resource guard + contract tests + runbook + template parity.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Top risks (carry to /sprint-plan)

- **R1** Worktree lock conflicts — deterministic naming + per-worktree GIT_DIR mandatory
- **R2** QA cross-review latency — sequential v1 preferred; parallel opt-in v2
- **R3** Merge conflicts — bounded retry ≤2; then manual halt
- **R4** Anti-slop unavailable — graceful degrade default `0`
- **R5** Resource cap race — atomic lockfile check-and-increment
- **R6** Bulk execute interaction — system-wide cap preferred; compose guard at step 22

### Evidence refs

- `docs/engineering/research.md` (**R-0096** — Q1–Q10 closed)
- `docs/product/backlog.md` (`## US-0108` — L1–L10 discovery locks, architecture PASS appended)
- `decisions/DEC-0108.md` (companion decision)
- `docs/engineering/architecture.md` (`# US-0108` — normative section)
- `docs/engineering/state.md` (architecture checkpoint + phase boundary)
- `handoffs/po_to_tl.md` (this handoff)
- `handoffs/resume_brief.md` (top pointer)
- Shipped compose surfaces: **US-0047** (`auto-orchestration-reference.md`), **US-0092** (`auto-orchestration-reference.md`), **US-0103** (`decision_ledger_lib.py`), **US-0104** (`sovereign_critic_lib.py`), **US-0107** (`sovereign_loop_lib.py`)

### Next

- **`/sprint-plan`** (fresh **tech-lead**) for **US-0108** — materialize **S0108** sprint from 10 task seeds; AC-1..AC-8 bijection check.

### Decision gate

- **None** — architecture satisfied; sprint-plan readiness explicit.

---

## Orchestrated research handoff — US-0106 / auto-20260628-04

- `timestamp=2026-06-28T20:10:00Z`
- `phase_id=research`
- `role=tech-lead`
- `story_id=US-0106`
- `sprint_id=(none)`
- `orchestrator_run_id=auto-20260628-04`
- `fresh_context_marker=tl-US0106-research-20260628T201000Z-fresh`
- `verdict=PASS`
- `next_scheduled_phase=architecture`
- `default_spawn_role=tech-lead`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=4`
- `drain_terminated=false`
- `native_chain_active=true`
- `native_chain_continuing=true`
- `drain_advance_action=spawned`
- `portfolio_open_stories=5` (US-0106, US-0108, US-0109, US-0111, US-0112)
- `portfolio_open_bugs=0`
- `delivery_mode=standard`
- `token_profile=lean`
- `caveman_mode=1`
- `caveman_level=full`
- `model_tier_default=balanced`
- `AUTO_QUIET=1`

### Summary

- **`/research`** **PASS** — **R-0095** Q1–Q7 closed; architecture-ready locks for YAML v1 schema, lib API, review dispatch contract, cross-model policy, escalation rules, contract-test inventory, parity scope.
- Compose guards confirmed: DO NOT amend US-0069 / US-0003 / US-0104 / US-0103 / US-0105 / US-0107.
- Companion **DEC-0106** recommended (manifest artifact surface + review dispatch contracts).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Research locks (Q1–Q7 closed)

| Q | Lock | Decision |
|---|------|----------|
| Q1 | YAML v1 schema + validator CLI | `schema_version: 1`, `roles[]`, `review_obligations[]`, `allowed_self_overrides`, `cross_model_policy`, `escalation_rules`; CLI `--file`, `--repo`, `--self-test`, `--enforce`; success `[SOVEREIGN_ROLE_MANIFEST_VALIDATION_OK]`; fail-closed on unknown `role_id`, cyclic obligations without escalation, secret-shaped literals |
| Q2 | `sovereign_role_manifest_lib.py` API | `load_manifest`, `resolve_role_objective`, `build_objective_injection_block` (char-capped `SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS=512`), `list_obligations_for_phase` (capped `SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE=2`), `dispatch_role_review`, `self_test` |
| Q3 | Cross-role review spawn contract | spawn-only per BUG-0006; JSONL `handoffs/sovereign_role_reviews.jsonl` fields `{obligation_id, reviewer_role, target_role, trigger_phase, orchestrator_run_id, ts, verdict, blocking, findings_ref}`; boundary token `role_review` distinct from US-0069 phase role |
| Q4 | `cross_model_policy` ordering (US-0104 compose) | `default_order` ∈ {`role_review_first`, `critic_first`, `critic_only`, `role_review_only`}; optional per-`obligation_id` override; when `CROSS_MODEL_REVIEW=1` and `SOVEREIGN_ROLE_MANIFEST=1`, orchestrator applies policy — does not merge critic lenses with role review prompts; when either flag `0`, zero overhead |
| Q5 | `escalation_rules` + US-0107 deferral compose | blocking review (`blocking=true`, verdict `fail`) → (1) bounded same-role rework (`SOVEREIGN_ROLE_REVIEW_REWORK_MAX` default `1`), (2) operator `decision_gate`, (3) optional `append_deferral` with `reason_code=ROLE_REVIEW_BLOCKED` when `AUTO_SOVEREIGN=1`; fail-open on deferral errors |
| Q6 | Contract-test inventory + parity | 8 markers `test_us0106_{scratchpad_keys_literals, manifest_schema_v1_literals, objective_injection_char_cap, obligation_dispatch_cap, us0069_compose_no_matrix_change, us0104_compose_no_critic_schema_change, zero_overhead_default, parity_scope}`; parity `--scope=sovereign-role-manifest` (`SOVEREIGN_ROLE_MANIFEST_PAIRS`): `.cursor/scratchpad.md`, `.cursor/sovereign-role-manifest.yaml`, `template/.cursor/scratchpad.md`, `template/.cursor/sovereign-role-manifest.yaml.example`, `scripts/sovereign_role_manifest_validate.py`, `scripts/sovereign_role_manifest_lib.py`, `template/scripts/sovereign_role_manifest_validate.py` |
| Q7 | Companion DEC necessity | **DEC-0106** recommended — locks manifest surface (YAML v1 schema, validator, lib, reviews JSONL, escalation, tests); anchors R-0095 |

### Self-test anchor

**[SOVEREIGN_ROLE_MANIFEST_SELF_TEST_OK]** (research stub; production self-test at `/execute`)

### Top risks (carry to /architecture)

- **R1**: Spawn depth / latency — review obligations multiply subagent spawns per phase; default-off + per-phase cap mandatory.
- **R2**: Role collapse — review spawn mis-routed as producer phase replacement → US-0069 regression; distinct boundary token + compose guard required.
- **R3**: US-0104 interaction — critic + role review at same boundary without `cross_model_policy` causes duplicate findings or rework thrash.
- **R4**: Manifest drift from matrix — operator adds invalid `role_id` or `trigger_phase`; validator must fail-closed with remediation.
- **R5**: Escalation oscillation — blocking review → rework → re-review loops; cap + `decision_gate` required.
- **R6**: Secret leakage — free-text objectives/reviews need scan (mirror US-0103 / US-0105 patterns).

### Evidence refs

- `docs/engineering/research.md` (**R-0095** — research closure, Q1–Q7 closed)
- `docs/product/backlog.md` (`## US-0106` — `discovery_notes` + `research_notes`)
- `docs/engineering/state.md` (discovery + research checkpoints)
- `handoffs/po_to_tl.md` (this handoff)
- `handoffs/resume_brief.md` (top pointer)
- Shipped compose surfaces: **US-0069** (`auto-orchestration-reference.md`), **US-0104** (`sovereign_critic_lib.py`), **US-0107** (`sovereign_loop_lib.py`), **US-0105** (`sovereign_memory_lib.py`)

### Next

- **`/architecture`** (fresh **tech-lead**) for **US-0106** — author `# US-0106` section, companion **DEC-0106**, atomic task seeds, contract-test literals, runbook operator recipes.

### Decision gate

- **None** — research satisfied; architecture readiness explicit.

---

## Orchestrated discovery validation handoff — US-0106 / auto-20260628-04 (validation pass)

- `timestamp=2026-06-28T18:04:00Z`
- `phase_id=discovery`
- `role=po`
- `story_id=US-0106`
- `orchestrator_run_id=auto-20260628-04`
- `fresh_context_marker=po-US0106-discovery-20260628T180400Z-fresh`
- `verdict=PASS`
- `next_scheduled_phase=research`
- `default_spawn_role=tech-lead`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=4`
- `portfolio_open_stories=5` (US-0106, US-0108, US-0109, US-0111, US-0112)
- `portfolio_open_bugs=0`

### Lock validation summary

L1–L12 validated against upstream DONE stories (US-0103, US-0104, US-0105, US-0107, US-0110). All locks **PASS**. Compose guards confirmed: DO NOT amend US-0069 / US-0003 / US-0104 / US-0103 / US-0105 / US-0107. No new discovery risks surfaced (R1–R6 as captured).

### Evidence refs

- `docs/product/backlog.md` (## US-0106 — `discovery_validation` block)
- `docs/engineering/state.md` (discovery isolation evidence + phase boundary + runtime proof)
- `handoffs/resume_brief.md` (top pointer)
- `handoffs/po_to_tl.md` (this handoff)

### Next

- **`/research`** (fresh **tech-lead**) for **US-0106** — close **R-0095** Q1–Q7; YAML schema + lib + dispatch contract + US-0069 compose guards before `/architecture`.

---

## Orchestrated discovery handoff — US-0106 / auto-20260628-04

### Target

- `story_id=US-0106`
- `orchestrator_run_id=auto-20260628-04`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0106-discovery-20260629T002500Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (sovereign-loop batch per intake-sovereign-20260627-01.json)
- `priority=P2`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=4`

### Summary

- **`/discovery`** **PASS** — sovereign role-behavior manifest locked: default-off **`SOVEREIGN_ROLE_MANIFEST`** gate; **`.cursor/sovereign-role-manifest.yaml`** declares per-role **`objective_function`** + directed **`review_obligations`** graph (bootstrap O1–O4: PO→arch user-value, QA→acceptance testability, dev→arch buildability, release→QA deployability); bounded **`role_objective_block`** injection at spawn; post-phase cross-role review dispatch (spawn-only, capped); **`cross_model_policy`** composes **US-0104** without amending critic schema; **`escalation_rules`** may route blocking reviews to **US-0107** deferrals or operator **`decision_gate`**. **Compose do NOT amend** **US-0069** — phase→role matrix + preflight/post checkpoint validation **unchanged**; manifest **`role_id`** ⊆ canonical roles; review spawns are **supplementary hooks** tagged by **`obligation_id`**, not alternate **`phase_id`** roles.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (research inputs)

| Lock | Decision |
|------|----------|
| **Scratchpad keys** | `SOVEREIGN_ROLE_MANIFEST=0\|1` (default `0`); `SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS` default `512`; `SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE` default `2` |
| **Manifest path** | `.cursor/sovereign-role-manifest.yaml` + `template/.cursor/sovereign-role-manifest.yaml.example` |
| **YAML v1 sections** | `roles[]`, `review_obligations[]`, `allowed_self_overrides`, `cross_model_policy`, `escalation_rules` |
| **Default graph** | O1 PO→architecture user-value; O2 QA→PO testability; O3 dev→architecture buildability; O4 release→QA deployability |
| **Objective injection** | Char-capped `role_objective_block` for US-0069-resolved role — additive to US-0105 digest |
| **Review dispatch** | Post-phase spawn-only reviewer subagents → `handoffs/sovereign_role_reviews.jsonl`; per-phase cap |
| **US-0069 compose** | Matrix unchanged; review ≠ phase substitute; compose guard required |
| **US-0104 compose** | `cross_model_policy` ordering vs `/sovereign-critic` — critic schema unchanged |
| **US-0107 compose** | `escalation_rules` → optional `append_deferral` on blocking review cap exhaustion |

### Acceptance pointers (discovery emphasis)

- **AC-1**: Scratchpad keys + zero-overhead when `SOVEREIGN_ROLE_MANIFEST=0`.
- **AC-2**: YAML v1 schema + bootstrap example graph O1–O4.
- **AC-3**: `sovereign_role_manifest_validate.py` CLI + `--self-test`.
- **AC-4**: Objective injection for US-0069-resolved role only.
- **AC-5**: Cross-role review dispatch + reviews JSONL + per-phase cap.
- **AC-6**: `cross_model_policy` vs US-0104 — no critic schema change.
- **AC-7**: Eight `test_us0106_*` markers + `--scope=sovereign-role-manifest` parity.
- **AC-8**: Architecture, runbook, US-0069 / US-0104 compose guards.

### Top risks (carry to /research)

- **R1**: Spawn depth/latency — default-off + per-phase cap mandatory.
- **R2**: Role collapse — review spawn must not substitute producer phase role (US-0069 regression).
- **R3**: US-0104 interaction — critic + role review at same boundary without policy causes thrash.
- **R4**: Manifest/matrix drift — invalid `role_id` or `trigger_phase` must fail-closed.
- **R5**: Escalation oscillation — blocking review rework loops need cap + decision gate.
- **R6**: Secret leakage in objectives/review text — scan required.

### Research asks (new **`R-0095`**)

1. YAML v1 schema + validator CLI.
2. `sovereign_role_manifest_lib.py` API sketch.
3. Cross-role review spawn contract + reviews JSONL + US-0069 boundary token.
4. `cross_model_policy` ordering matrix vs US-0104.
5. `escalation_rules` + US-0107 deferral compose.
6. Contract-test inventory + `SOVEREIGN_ROLE_MANIFEST_PAIRS` parity.
7. Companion DEC necessity.

### Evidence refs

- `docs/product/backlog.md` (`## US-0106` — `discovery_notes` with L1–L12 + design-intent table)
- `docs/product/vision.md` (**Discovery Notes — US-0106**)
- `docs/product/acceptance.md` (`US-0106` row — unchecked, discovery PASS)
- `docs/engineering/research.md` (**`R-0095`** — discovery stub)
- `handoffs/intake_evidence/intake-sovereign-20260627-01.json`
- Shipped compose: **US-0069** (phase→role matrix), **US-0104** (`DEC-0104`, `sovereign_critic_lib.py`), **US-0107** (`DEC-0107`, `sovereign_loop_lib.py`), **US-0105** (`DEC-0105`, `sovereign_memory_lib.py`), **US-0103** (`DEC-0103`)
- Adjacent (do NOT amend): **US-0003** role definitions, **US-0023** fresh-context, **US-0088**/**US-0092**/**US-0095** orchestration stop matrix

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0106`** — close **`R-0095`** Q1–Q7; YAML schema + lib + dispatch contract + US-0069 compose guards before **`/architecture`**.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

## Orchestrated architecture handoff — US-0098 / auto-20260613-01

### Target

- `story_id=US-0098`
- `orchestrator_run_id=auto-20260613-01`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0098-architecture-20260614T080000Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `decomposition=single_story` (per **US-0051**)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=9`

### Summary

- **`/architecture`** **PASS** — **`DEC-0084`** locked; **`# US-0098`** appended; 11 atomic task seeds; eight **`test_us0098_*`** contract markers + **`DEV_ENVIRONMENT_PAIRS`** parity manifest.
- **Default-off gate**: **`DEV_AUTO_LAUNCH_PROFILE`**: `off`|`deterministic_v1` (default **`off`**); optional **`DEV_ENVIRONMENT_CONFIG`** path override.
- **Execute step 24**: after step **23** (**US-0097**); sub-steps **24a–24d**; bounded retries (**`retry_count`≤2**); explicit refresh literal **`refresh dev environment`**.
- **Detection**: four-label matrix; **US-0086** remote precedence over **docker-host-local**; Tier A/B/C execute-triggered relaunch (no mandatory watch daemon v1).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Architecture locks (sprint-plan inputs)

| Lock | Decision |
|------|----------|
| **Binding decision** | **`DEC-0084`** — composes **US-0085** / **US-0064** / **US-0086** / **US-0093** |
| **Tranche order** | A schema+gitignore → B **`dev_environment_lib.py`** → C execute step **24** → D validators + tests |
| **Task seeds** | 11 seeds (under **`SPRINT_MAX_TASKS=12`** threshold) |
| **Profile path** | **`.cursor/dev-environment.json`** + **`template/.cursor/dev-environment.json.example`**; gitignored local |
| **Execute placement** | Step **24** after **23**; zero overhead when profile **`off`** |
| **Contract tests** | **`test_us0098_dev_auto_launch_scratchpad_keys`**, **`test_us0098_execute_step24_literals`**, **`test_us0098_dev_environment_schema_contract`**, **`test_us0098_detection_mode_precedence_literals`**, **`test_us0098_reason_code_inventory`**, **`test_us0098_connect_block_field_literals`**, **`test_us0098_refresh_dev_environment_phrase_literal`**, **`test_us0098_us0086_compose_no_schema_change`** |
| **Parity scope** | **`check_intake_template_parity.py --scope=dev-environment`** (**`DEV_ENVIRONMENT_PAIRS`**) |

### Top risks (carry to /sprint-plan)

- **R1**: Relaunch loops or duplicate containers — bounded retries + idempotent profile writes.
- **R2**: Conflating **docker-host-local** with **US-0086** remote docker — explicit precedence + regression test.
- **R3**: Secret leakage in persisted profile — four-layer **US-0085** audit + gitignore local profile.

### Evidence refs

- `decisions/DEC-0084.md`
- `docs/engineering/architecture.md` (**`# US-0098`**)
- `docs/engineering/research.md` (**`R-0085`**)
- `docs/product/backlog.md` (`## US-0098` — `architecture_notes` appended)
- `docs/engineering/state.md` (Architecture checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/sprint-plan`)
- Prior research proof: `rp-auto-20260613-01-research-tech-lead-20260614T070000Z-US0098`

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`US-0098`** — materialize sprint from 11 architecture seeds; AC-1..AC-10 bijection check.

### Decision gate

- **None** — architecture satisfied; sprint-plan readiness explicit.

---

## Orchestrated discovery handoff — US-0098 / auto-20260613-01

### Target

- `story_id=US-0098`
- `orchestrator_run_id=auto-20260613-01`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0098-discovery-20260614T060000Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (per **US-0051**)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=9`

### Summary

- **`/discovery`** **PASS** — dev-loop **auto-launch profile** locked: default-off **`DEV_AUTO_LAUNCH_PROFILE`** scratchpad gate; persisted **`.cursor/dev-environment.json`** (names-only **` *Env`** refs); **execute-bound** bounded relaunch + explicit **`refresh dev environment`** operator path; **Connect** block after relaunch. **Docker-host-local** is first-class (same-machine shell/docker, not remote SSH). Distinct from **US-0065** (phase QA), **US-0086** (test routing), **US-0067** (release hints).
- **v1 exclusion**: no mandatory unbounded file-watch / **`docker compose watch`** daemon — execute-triggered automation only unless architecture later documents bounded watch.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (research inputs)

| Lock | Decision |
|------|----------|
| **Scratchpad gate** | **`DEV_AUTO_LAUNCH_PROFILE`**: `off` \| `deterministic_v1` (default **`off`**); optional **`DEV_ENVIRONMENT_CONFIG`** path |
| **Profile path** | **`.cursor/dev-environment.json`** + **`template/.cursor/dev-environment.json.example`**; **no** **`release-targets.json`** schema change |
| **Detection matrix** | **`local`**, **`docker-host-local`**, **`docker`**, **`ssh`** — docker-host-local = direct shell/docker on dev machine |
| **Relaunch triggers** | Post-**`/execute`** on runtime/container file classes + explicit refresh phrase; max retry cap architecture-locked |
| **Recipe tiers** | **A** rebuild (Dockerfile*, lockfiles); **B** restart (config); **C** local dev server (**`DEV_SERVER_*`**) |
| **Connect block** | `runtime_mode`, `connect_endpoint`, `health_path`, `service_id`/`container_id`, `target_id`, `env_refs`, `relaunch_outcome` |
| **Reason codes** | **`DEV_ENV_PROFILE_*`**, **`DEV_ENV_RELAUNCH_*`** families (inventory at **`/research`**) |
| **Security** | **US-0085** inheritance — no **`.env`** reads; names-only in git-tracked JSON |
| **Composition** | **US-0086** remote precedence when both profiles on; **US-0093** **`process_health`** may consume relaunch outcome |

### Acceptance pointers (discovery emphasis)

- **AC-1**: **`DEV_AUTO_LAUNCH_PROFILE`** default-off; manual workflows unchanged when off.
- **AC-2**: Profile schema + template example; operator seed + idempotent agent updates.
- **AC-3**: Four-label detection matrix; fail-closed when unresolved.
- **AC-4**: Execute relaunch contract + **`dev_to_qa.md`** evidence tuple.
- **AC-5**: Connect block field shapes per vision discovery template.
- **AC-6**: Compose with **US-0064**/**US-0085**/**US-0086**/**`DEV_SERVER_*`** — no parallel connectivity schema.
- **AC-7**: Explicit **`refresh dev environment`** path documented.
- **AC-8**: Bounded retries; no unbounded watch v1.
- **AC-9..AC-10**: Contract tests, template parity, architecture **`# US-0098`**.

### Top risks (carry to /research)

- **R1**: Relaunch loops or duplicate containers — bounded retries + idempotent profile writes.
- **R2**: Conflating **docker-host-local** with **US-0086** remote docker — explicit matrix + precedence table.
- **R3**: Secret leakage in persisted profile — names-only schema + **US-0085** audit paths.

### Research asks (extend **`R-0085`**)

1. Finalize profile JSON schema and gitignore/local-only policy.
2. File-class → relaunch tier table (exact paths/globs; shared **US-0086** filters where applicable).
3. **`/execute`** step wiring + **`dev_to_qa.md`** evidence tuple prose.
4. Explicit refresh command / NL synonym table.
5. Stdlib helper vs doc-only; **`check_intake_template_parity.py --scope=dev-environment`** manifest.
6. **US-0085** security audit through profile load/relaunch paths.
7. Companion **`DEC-xxxx`** necessity vs discovery locks alone.

### Evidence refs

- `docs/product/vision.md` (**`## Discovery Notes — US-0098`**)
- `docs/product/backlog.md` (`## US-0098` — `discovery_notes`)
- `docs/engineering/research.md` (**`R-0085`**)
- `handoffs/intake_evidence/US-0098-intake-20260613.json`
- `docs/engineering/runtime-connectivity.md`
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/research`)

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0098`** — close **`R-0085`** Q1–Q7; detection matrix + reason-code inventory.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

## Orchestrated architecture handoff — US-0097 / auto-20260613-01

### Target

- `story_id=US-0097`
- `orchestrator_run_id=auto-20260613-01`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0097-architecture-20260613T220000Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `decomposition=single_story` (per **US-0051**)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=10`

### Summary

- **`/architecture`** **PASS** — **`DEC-0083`** locked; **`# US-0097`** appended; 11 atomic task seeds; eight **`test_us0097_*`** contract markers + **`PROJECT_README_PAIRS`** parity manifest.
- **Installer boundary**: root **`README.md`** removed from framework **`[install_paths]`**; **`its_magic/README.md`** canonical framework surface (**DEC-0045** completion).
- **Gate separation**: **US-0091** reframed to **`its_magic/`** paths; new **`validate_project_readme_coverage.py`** + release **3g** + **`PROJECT_README_ENFORCE`** (default **`1`** post-bootstrap).
- **Phase wiring**: execute step **23** (**23a** bootstrap, **23b** delta, **23c** **US-0071** compose); release **3g** after **3f**.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Architecture locks (sprint-plan inputs)

| Lock | Decision |
|------|----------|
| **Binding decision** | **`DEC-0083`** — amends **`DEC-0045`**; reframes **DEC-0074** paths |
| **Tranche order** | A installer+migration → B bootstrap → C phase wiring → D validators + tests |
| **Task seeds** | 11 seeds (under **`SPRINT_MAX_TASKS=12`** threshold) |
| **Placeholder sentinels** | S1 its-magic H1; S2 `<!-- readme-feature-coverage-catalog -->`; S3 US-0091 catalog heading; S4 template byte-match; S5 operator-authored preserve |
| **Migration** | M1–M5 idempotent; hybrid fail-closed **`PROJECT_README_MIGRATION_AMBIGUOUS`** |
| **Kit exception** | **`FRAMEWORK_KIT_REPO=1`** for its-magic dev repo only |
| **Contract tests** | **`test_us0097_installer_manifest_no_root_readme`**, **`test_us0097_execute_step23_literals`**, **`test_us0097_release_step3g_literals`**, **`test_us0097_placeholder_sentinel_table`**, **`test_us0097_framework_validator_paths_reframed`**, **`test_us0097_project_readme_enforce_scratchpad_keys`**, **`test_us0097_project_readme_coverage_validator_contract`**, **`test_us0097_us0091_regression_guard`** |
| **Parity scope** | **`check_intake_template_parity.py --scope=project-readme`** (**`PROJECT_README_PAIRS`**) |

### Top risks (carry to /sprint-plan)

- **R1**: Migration deletes operator project prose — S5 preserve + M5 ambiguous fail-closed.
- **R2**: **US-0091** regression if framework path lock incomplete — explicit path table + regression guard test.
- **R3**: Kit vs consumer repo — **`FRAMEWORK_KIT_REPO`** detection order and validator skip.

### Evidence refs

- `decisions/DEC-0083.md`
- `docs/engineering/architecture.md` (**`# US-0097`**)
- `docs/engineering/research.md` (**`R-0084`**)
- `docs/product/backlog.md` (`## US-0097` — `architecture_notes` appended)
- `docs/engineering/state.md` (Architecture checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/sprint-plan`)
- Prior research proof: `rp-auto-20260613-01-research-tech-lead-20260613T210000Z-US0097`

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`US-0097`** — materialize sprint from 11 architecture seeds; AC-1..AC-10 bijection check.

### Decision gate

- **None** — architecture satisfied; sprint-plan readiness explicit.

---

## Orchestrated discovery handoff — US-0097 / auto-20260613-01

### Target

- `story_id=US-0097`
- `orchestrator_run_id=auto-20260613-01`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0097-discovery-20260613T200000Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (per **US-0051**)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=10`

### Summary

- **`/discovery`** **PASS** — project-owned root **`README.md`** contract locked: bootstrap scaffold on first **`/execute`** when missing/placeholder; mandatory per-shipped-story catalog growth; framework catalog confined to **`its_magic/README.md`** only. Completes **US-0062** / **DEC-0045** partial delivery (manifest still ships root README today).
- **Gate separation**: **US-0091** reframed to framework paths; new project validator + release **3g** + **`PROJECT_README_ENFORCE`** scratchpad (default-on post-bootstrap).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (research inputs)

| Lock | Decision |
|------|----------|
| **Installer boundary** | Remove root **`README.md`** from framework **`[install_paths]`**; ship framework README only under **`its_magic/`** |
| **Project scaffold** | H1 from vision + purpose + **`## For users`** + **`## For developers`** + **`## Features`** + `<!-- project-readme-feature-catalog -->` |
| **Placeholder sentinels** | S1 its-magic H1; S2 `<!-- readme-feature-coverage-catalog -->`; S3 US-0091 catalog heading; S4 template byte-match |
| **Operator prose** | Preserve when S5 (no sentinel + custom content); migration fail-closed on ambiguous hybrid |
| **Kit-repo exception** | **`FRAMEWORK_KIT_REPO=1`** for its-magic dev repo only; consumer repos never bootstrap framework root |
| **Per-story delta** | Execute + release require ≥1 user-facing blurb per shipped **`user_visible: true`** **`US-xxxx`** |
| **Tranche order** | A installer+migration → B bootstrap → C phase wiring → D validators + tests |
| **Reason codes** | Umbrella **`PROJECT_README_COVERAGE_BLOCKED`** + gap/delta/migration sub-codes |

### Acceptance pointers (discovery emphasis)

- **AC-1**: Manifest removes root README from framework install; fresh `missing` install has no framework README at root.
- **AC-2**: Non-destructive migration with S1–S5 heuristic + **`PROJECT_README_MIGRATION_AMBIGUOUS`** remediation.
- **AC-3**: Execute bootstrap when missing/placeholder; vision-sourced title/purpose.
- **AC-4**: Mandatory execute/release README delta; fail-closed when skipped.
- **AC-5**: User + developer H2 structure; framework catalog only in **`its_magic/`**.
- **AC-6**: Split validators — **US-0091** → framework paths; **`validate_project_readme_coverage.py`** → project root.
- **AC-7**: Release **3g** + **`PROJECT_README_ENFORCE`** (default **`1`** post-bootstrap).
- **AC-8..AC-10**: **US-0071** hygiene, contract tests + template parity, architecture + runbook.

### Top risks (carry to /research)

- **R1**: Migration deletes operator project prose — S5 preserve heuristic + ambiguous fail-closed.
- **R2**: **US-0091** regression if framework path lock incomplete — explicit path table in architecture.
- **R3**: Kit vs consumer repo — **`FRAMEWORK_KIT_REPO`** detection order and **US-0091** scope for kit root.

### Research asks (extend **`R-0084`**)

1. Close Q5 — execute/release step numbers and prose tokens; delta skip reason-code table.
2. Close Q6 — `validate_project_readme_coverage.py` CLI/`--report` schema; **3g** wiring with **3f**.
3. Close Q7 — hybrid migration idempotency; merge policy when root is partially customized.
4. Contract-test marker inventory + **`check_intake_template_parity.py --scope=project-readme`** manifest.
5. Confirm whether companion **`DEC-xxxx`** required or discovery locks suffice for architecture.

### Evidence refs

- `docs/product/backlog.md` (`## US-0097` — `discovery_notes` appended)
- `docs/product/vision.md` (**Discovery Notes — US-0097**)
- `docs/product/acceptance.md` (`US-0097` row — unchecked)
- `handoffs/intake_evidence/US-0097-intake-20260613.json`
- `docs/engineering/research.md` (**`R-0084`** — discovery extension appended)
- `docs/engineering/context/installer-owned-paths.manifest` (root **`README.md`** line 42 — removal target)
- Adjacent: **US-0062**, **DEC-0045**, **US-0091**, **DEC-0074**, **US-0032**, **US-0071**, **US-0017**

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0097`** — close **R-0084** Q5–Q7; validator sketch; phase wiring; migration table; architecture readiness.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

## PO intake handoff — US-0098 / cursor-20260613-US0098-intake

### Target

- `story_id=US-0098`
- `intake_run_id=cursor-20260613-US0098-intake`
- `selected_pack=first-intake-pack`
- `priority=P1`
- `decomposition=single_story` (per **US-0051**)
- `next_scheduled_phase=discovery`

### Summary

Operator **`/ask`** → **`/intake`**: during development the AI should **automatically rebuild/restart** the app after code changes (e.g. Docker containers), **persist** a dev-environment profile (operator-seeded), and **show connection parameters** — distinct from **US-0065** phase QA startup, **US-0086** test routing, and **US-0067** release hints. **Docker-host-local** (direct shell/docker on the machine) is a first-class detection label, not remote SSH.

### Scope (10 ACs)

1. Default-off scratchpad **dev auto-launch profile**.
2. Persisted **dev-environment profile** schema (names-only secret refs).
3. Deterministic **environment detection** (`local`, `docker-host-local`, `docker`, `ssh`).
4. **`/execute` bounded relaunch** after runtime/container surface changes.
5. **Operator Connect surface** after relaunch (URL/port/health; no secret values).
6. **Composition** with **US-0064** / **US-0085** / **US-0086** / **`DEV_SERVER_*`**.
7. Explicit **refresh dev environment** operator path.
8. **Bounded safety** + **`DEV_ENV_*`** reason codes (no unbounded watch v1).
9. Contract tests + template parity.
10. Architecture decision + runbook recipe.

### Plan area map (US-0081 / DEC-0064)

| `plan_area_id` | Maps to |
|----------------|---------|
| `dev-profile-schema-persistence` | **US-0098** |
| `environment-detection-heuristics` | **US-0098** |
| `execute-phase-relaunch-contract` | **US-0098** |
| `container-rebuild-orchestration` | **US-0098** |
| `operator-connection-surface` | **US-0098** |
| `scratchpad-gates-default-off` | **US-0098** |
| `composition-existing-runtime-contracts` | **US-0098** |
| `docs-tests-parity` | **US-0098** |

`coverage_complete=true`

### Overlap / duplicate check

- **US-0065** — phase runtime QA; **US-0098** adds dev-loop relaunch during execute.
- **US-0086** — automation test routing; **US-0098** adds profile + relaunch + Connect UX.
- **US-0067** — release Run/Connect/Verify; **US-0098** is in-dev, not release-only.
- **US-0085** — **`.env`** exclusion inherited; no schema change to **US-0064**.

### Intake evidence

- `handoffs/intake_evidence/US-0098-intake-20260613.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**
- `asked_topics`: all eight first-intake keys
- `missing_topics`: (none)
- `assumptions_confirmed`: (none)

### Risks (PO)

- **R1**: Relaunch loops or duplicate containers — mitigate with bounded retries + idempotent profile writes.
- **R2**: Conflating **docker-host-local** with **US-0086** remote docker — explicit detection matrix in architecture.
- **R3**: Secret leakage in persisted profile — names-only schema + **US-0085** audit in architecture.

### Research anchor

- Stub **`R-0085`** — extend in **`/discovery`** / **`/research`** (profile schema, detection matrix, relaunch triggers, compose recipes).

### Status authority

- **OPEN** per **US-0045** until QA/release closure chain.
- **Next**: **`/discovery`** (fresh **PO**) for **`US-0098`**.

---

## PO intake handoff — US-0097 / cursor-20260613-US0097-intake

### Target

- `story_id=US-0097`
- `intake_run_id=cursor-20260613-US0097-intake`
- `selected_pack=first-intake-pack`
- `priority=P1`
- `decomposition=single_story` (per **US-0051**)
- `next_scheduled_phase=discovery`

### Summary

Operator **`/ask`** follow-up: framework README must live only in **`its_magic/`**; root **`README.md`** must be a **project-owned** repo overview (users + developers) that is **bootstrapped on first story** and **extended every sprint/story** — behavior missing today despite **US-0062** intent.

### Scope (10 ACs)

1. Remove root **`README.md`** from framework install payload; **`its_magic/README.md`** only.
2. Non-destructive upgrade migration for legacy framework root README.
3. Execute-time bootstrap scaffold when root README missing/placeholder.
4. Mandatory execute/release README delta per shipped **`US-xxxx`**.
5. User + developer sections in project README (framework catalog stays in **`its_magic/`**).
6. Split validators: **US-0091** → framework; new project README coverage gate.
7. Release gate + scratchpad **`PROJECT_README_ENFORCE`** (default-on post-bootstrap).
8. **US-0071** hygiene on project blurbs.
9. Contract tests + template parity scope.
10. Architecture decision + runbook operator recipe.

### Plan area map (US-0081 / DEC-0064)

| `plan_area_id` | Maps to |
|----------------|---------|
| `installer-framework-readme-boundary` | **US-0097** |
| `project-readme-bootstrap` | **US-0097** |
| `execute-release-delta-workflow` | **US-0097** |
| `project-readme-audience-structure` | **US-0097** |
| `framework-vs-project-readme-gates` | **US-0097** |
| `upgrade-migration-non-destructive` | **US-0097** |
| `docs-tests-parity` | **US-0097** |

`coverage_complete=true`

### Overlap / duplicate check

- **US-0062** — completes partial delivery (manifest still ships root README).
- **US-0091** — reframes scope to framework paths; does not replace.
- **US-0032** — optional guides; orthogonal.
- **US-0077** — framework dual README; project uses simpler product sections.

### Intake evidence

- `handoffs/intake_evidence/US-0097-intake-20260613.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**
- `asked_topics`: all eight first-intake keys
- `missing_topics`: (none)
- `assumptions_confirmed`: (none)

### Risks (PO)

- **R1**: Migration deletes operator project prose — mitigate with placeholder detection + merge policy.
- **R2**: **US-0091** regression if framework paths wrong — explicit path lock in architecture.
- **R3**: Kit repo itself is both framework + product — research must define sentinel/exception for its-magic dev repo vs consumer repos.

### Research anchor

- Stub **`R-0084`** — extend in **`/discovery`** / **`/research`** (placeholder detection, validator sketch, manifest delta, phase wiring).

### Status authority

- **OPEN** per **US-0045** until QA/release closure chain.
- **Next**: **`/discovery`** (fresh **PO**) for **`US-0097`**.

---

## Orchestrated architecture handoff — US-0096 / auto-20260612-01

### Target

- `story_id=US-0096`
- `orchestrator_run_id=auto-20260612-01`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0096-architecture-20260613T040000Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `decomposition=single_story` (per `US-0051`)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=9`

### Summary

- **`/architecture`** **PASS** — **`DEC-0082`** locked; **`# US-0096`** appended; 12 atomic task seeds; eight **`test_us0096_*`** contract markers + **`US0096_PAIRS`** parity manifest.
- **Three-mode axis**: **`DELIVERY_MODE=standard|ultra_lean|mega_quick`** (default **`standard`**) orthogonal to **`TOKEN_PROFILE`** / **`CAVEMAN_MODE`**.
- **Resolver step 0**: **`delivery_mode`** before **DEC-0052**; reinstatement **standard-only**; **`PHASE_POLICY_CONFLICT`** when non-standard + **`AUTO_PHASE_*`**.
- **Tranche A** (always-on): default hot caps **1000/650/3000**, narrow-read all phase commands, delta handoffs, touch-graph runbook — target **≥10%** **`cache_read_tokens`** on matched **`standard`** runs.
- **Layered memory**: hot **`handoffs/active-context.md`** (non-triad); warm **`work/US-xxxx/pack.json`**; cold section-scoped reads (**`LEAN_COLD_READ_MAX_SECTIONS`** default **4**).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Architecture locks (sprint-plan inputs)

| Lock | Decision |
|------|----------|
| **Binding decision** | **`DEC-0082`** — amends **`DEC-0062`** run-class with **`delivery_mode`** |
| **Tranche order** | A universal wins → B **`ultra_lean`** → C **`mega_quick`** → D backlog routing |
| **Task seeds** | 12 seeds (at **`SPRINT_MAX_TASKS=12`** threshold — no auto-split unless hidden scope) |
| **Contract tests** | **`test_us0096_delivery_mode_scratchpad_keys`**, **`test_us0096_standard_mode_baseline_markers_preserved`**, **`test_us0096_mode_scoped_reinstatement_literals`**, **`test_us0096_ultra_lean_macro_phase_literals`**, **`test_us0096_mega_quick_routing_literals`**, **`test_us0096_pack_json_schema_contract`**, **`test_us0096_active_context_contract`**, **`test_us0096_token_profile_orthogonality_paragraph`** |
| **Parity scope** | **`check_intake_template_parity.py --scope=us-0096`** (**`US0096_PAIRS`**) |
| **Native chain** | **DEC-0080** / **DEC-0081** compose unchanged — lean modes reduce spawns, not drain-advance |

### Top risks (carry to /sprint-plan)

- **R1** Partial **`ultra_lean`** without validator/index — Tranche B gated.
- **R3** **`standard`** regression — baseline marker preservation test mandatory early.
- **R5** **`build+verify`** merged spawn — runbook E2E in execute.

### Evidence refs

- `decisions/DEC-0082.md`
- `docs/engineering/architecture.md` (**`# US-0096`**)
- `docs/engineering/research.md` (**`R-0082`**)
- `docs/product/backlog.md` (`## US-0096` — `architecture_notes` appended)
- `docs/engineering/state.md` (Architecture checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/sprint-plan`)
- `handoffs/tl_to_dev.md` (US-0096 architecture handoff)
- Prior research proof: `rp-auto-20260612-01-research-tl-20260613T030000Z-US0096`

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`US-0096`** — materialize sprint from 12 architecture seeds; AC-1..AC-12 bijection check.

### Decision gate

- **None** — architecture satisfied; sprint-plan readiness explicit.

---

## Orchestrated research handoff — US-0096 / auto-20260612-01

### Target

- `story_id=US-0096`
- `orchestrator_run_id=auto-20260612-01`
- phase completed: **`research`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0096-research-20260613T030000Z-fresh`
- `next_scheduled_phase=architecture`
- `decomposition=single_story` (per `US-0051`)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=9`

### Summary

- **`/research`** **PASS** — **`R-0082`** Q1–Q7 closed; architecture-ready locks on **`DELIVERY_MODE`**, layered memory, mode-scoped resolver, Tranche A defaults, and contract-test inventory.
- **Three-mode axis unchanged** from discovery; **DEC-0052 reinstatement applies only when `DELIVERY_MODE=standard`**; **`AUTO_PHASE_*` conflicts with non-standard mode → `PHASE_POLICY_CONFLICT`**.
- **Layered memory**: hot **`handoffs/active-context.md`** (non-triad warm index); warm **`work/US-xxxx/pack.json`** schema v1; cold section-scoped reads capped by **`LEAN_COLD_READ_MAX_SECTIONS`** (default **4**).
- **Tranche A** (always-on): tighter default hot-surface caps, narrow-read in all phase commands, delta handoffs, touch-graph policy — target **≥10%** **`cache_read_tokens`** reduction on matched **`standard`** runs.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Research locks (architecture inputs)

| Lock | Decision |
|------|----------|
| **`pack.json`** | Path **`work/<story_id>/pack.json`**; schema v1 fields (`schema_version`, `story_id`, `delivery_mode`, `status`, `ac[]`, `tasks[]`, `refs[]`, `deltas[]`, `memory_layer`); validator **`scripts/pack_json_validate.py`** |
| **Sprint coexistence** | **`standard`** → **`sprints/Sxxxx/`** authoritative; **`ultra_lean`** → **`work/`** authoritative; **`mega_quick`** → **`sprints/quick/Qxxxx/`**; no destructive overlap; no mid-story mode switch |
| **Resolver step 0** | Resolve **`delivery_mode`** before **DEC-0052**; **`ultra_lean`** → `[spec, plan, build+verify, ship]`; **`mega_quick`** → `[quick]`; **`standard`** → full **DEC-0052** pipeline |
| **`active-context.md`** | Hot index **30–80** lines; cap **`LEAN_STATE_INDEX_ROWS`** (default **80**); rollover on segment close or oversize; **not** triad member (**DEC-0054** unchanged) |
| **`mega_quick` eligibility** | Seven fail-closed codes (**`MEGA_QUICK_*`**); story-only; ≤3 AC; no companion DEC; no existing **`Sxxxx`** |
| **Tranche A defaults** | **`STATE_HOT_MAX_LINES` 1000**, **`PO_TO_TL_HOT_MAX_LINES` 650**, **`ARCH_HOT_MAX_LINES` 3000**; operator explicit values override |
| **`run_class_hash`** | Add required **`delivery_mode`** key (**DEC-0062** extension); cross-mode comparisons invalid |
| **Contract tests** | Eight **`test_us0096_*`** markers; parity **`--scope=us-0096`** (**`US0096_PAIRS`**) |

### Top risks (carry to /architecture)

- **R1** Partial delivery — **`ultra_lean`** without validator/index.
- **R2** **`active-context`** mistaken for triad surface.
- **R3** **`standard`** regression vs **`test_us0095_*`** / **`test_bug0012_*`** baselines.
- **R4** **`mega_quick`** false routing of broad stories.
- **R5** **`build+verify`** merged spawn complexity.

### Evidence refs

- `docs/engineering/research.md` (**`R-0082`** — research extension)
- `docs/product/backlog.md` (`## US-0096` — `research_notes` appended)
- `handoffs/intake_evidence/US-0096-intake-20260611.json`
- `handoffs/po_to_tl.md` (Orchestrated discovery handoff — US-0096)
- `docs/engineering/state.md` (Research checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/architecture`)
- Adjacent: **DEC-0052**, **DEC-0062**, **DEC-0054**, **DEC-0080**, **US-0053**, **US-0080**, **US-0070**, **US-0001**

### Next

- **`/architecture`** (fresh **tech-lead** context) for **`US-0096`** — author **`# US-0096`**, companion **`DEC-xxxx`**, atomic task seeds, **`test_us0096_*`** literals, runbook operator recipes.

### Decision gate

- **None** — research satisfied; architecture readiness explicit.

---

## Orchestrated discovery handoff — US-0096 / auto-20260612-01

### Target

- `story_id=US-0096`
- `orchestrator_run_id=auto-20260612-01`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0096-discovery-20260613T023000Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (per `US-0051`)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=9`

### Summary

- **`/discovery`** **PASS** — opt-in **`DELIVERY_MODE`** lifecycle-shape axis locked: **`standard`** (default, byte-compatible), **`ultra_lean`** (4 macro-phases + layered memory), **`mega_quick`** (enhanced **`/quick`** under **`/auto`**). Orthogonal to **`TOKEN_PROFILE`** (**DEC-0062**) and **`CAVEMAN_MODE`** (**DEC-0072**). Tranche A universal token wins ship always-on without mode toggle.
- **Native chain composes unchanged** (**DEC-0080** / **DEC-0081** / **BUG-0012** delivered) — lean modes reduce spawns per story, not drain-advance semantics.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (research inputs)

| Lock | Decision |
|------|----------|
| **`DELIVERY_MODE` values** | **`standard`** \| **`ultra_lean`** \| **`mega_quick`**; default **`standard`** when unset |
| **Orthogonality** | **`DELIVERY_MODE`** = lifecycle shape + artifacts only; does not substitute **`TOKEN_PROFILE`** or **`CAVEMAN_MODE`** |
| **`ultra_lean` macro-phases** | **`spec`** (PO: intake+discovery) → **`plan`** (TL: research+architecture+sprint-plan) → **`build+verify`** (dev: execute+merged qa/verify-work; **`AUTO_IMPLEMENTATION_LOOP`**) → **`ship`** (release+refresh-context) |
| **Layered memory** | Hot: **`handoffs/active-context.md`**; warm: **`work/US-xxxx/pack.json`**; cold: section-scoped vision/architecture/decisions reads |
| **`mega_quick` routing** | **`/auto`** → enhanced **`/quick`**; **`sprints/quick/Qxxxx/task.json`** + **`summary.md`**; eligibility guard for small bounded work; +1 spawn on test failure only |
| **DEC-0052 reinstatement** | Applies **only** when **`DELIVERY_MODE=standard`** |
| **Tranche order** | A universal wins → B ultra_lean → C mega_quick → D optional backlog **`delivery_mode`** routing |
| **Quality floor** | Tests before stop; no secrets/publish bypass; auditable refs in lean modes (**AC-9**) |

### Acceptance pointers (discovery emphasis)

- **AC-1**: Scratchpad + template docs for **`DELIVERY_MODE`** and optional **`LEAN_*`** keys; non-substitution paragraph.
- **AC-2**: **`standard`** byte-compatible — contract tests vs pre-**US-0096** baseline markers.
- **AC-3**: Tranche A universal wins — measurable **`cache_read_tokens`** improvement on **`run_class_hash`-matched** runs.
- **AC-4..AC-5**: **`ultra_lean`** macro-lifecycle + **`pack.json`** + **`active-context.md`** + section-scoped cold reads.
- **AC-6..AC-7**: **`mega_quick`** routing + mode-scoped phase resolver breadcrumbs.
- **AC-8**: Optional backlog **`delivery_mode`** row + **`AUTO_DELIVERY_ROUTING`** precedence.
- **AC-9..AC-12**: Quality floor, contract tests, architecture lock, token-cost evidence with **`delivery_mode`** in run-class.

### Top risks (carry to /research)

- **R1** Partial delivery — **`ultra_lean`** without memory index.
- **R2** **`active-context.md`** vs **DEC-0054** triad hot-surface rollover conflict.
- **R3** **`standard`** regression via resolver drift.
- **R4** **`mega_quick`** false routing of large cross-cutting stories.
- **R5** **`pack.json`** vs **`sprints/Sxxxx/`** coexistence rules.

### Research asks (extend **`R-0082`**)

1. **`pack.json`** canonical schema + validator sketch vs sprint folder compatibility.
2. Mode-scoped **DEC-0052** reinstatement algorithm (pseudocode + resolver integration point).
3. **`active-context.md`** rollover contract vs **DEC-0054** triad — ownership and line budgets.
4. **`mega_quick`** eligibility table + fail-closed reason codes + backlog row schema.
5. Tranche A default threshold changes vs **`LEAN_*`** operator overrides.
6. **DEC-0062** **`run_class_hash`** extension with **`delivery_mode`** field.
7. Contract-test marker inventory + **`check_intake_template_parity.py --scope=us-0096`** manifest.

### Evidence refs

- `docs/product/backlog.md` (`## US-0096` — `discovery_notes` appended)
- `docs/product/vision.md` (**Discovery Notes — US-0096**)
- `docs/product/acceptance.md` (`US-0096` row — unchecked)
- `handoffs/intake_evidence/US-0096-intake-20260611.json`
- `docs/engineering/research.md` (**`R-0082`** — discovery extension appended)
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/research`)
- Adjacent: **US-0080**, **DEC-0062**, **US-0053**, **US-0070**, **DEC-0052**, **US-0001**, **US-0092**, **US-0095**, **DEC-0080**, **DEC-0081**, **DEC-0072**, **DEC-0054**

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0096`** — deepen **`R-0082`**, lock schemas, resolver algorithm, eligibility table, and contract-test inventory before **`/architecture`**.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

## Orchestrated research handoff — US-0094 / auto-20260607-01

## Architecture Phase Handoff - US-0112

**From:** tech-lead (architecture)
**To:** tech-lead (sprint-plan)
**Timestamp:** 2026-06-30T22:00:00Z
**Orchestrator Run:** auto-20260628-04
**Context Pack:** architecture_notes, DEC-0112, R-0090, task_seeds

### Deliverables Ready
- `docs/engineering/architecture.md` # US-0112 (normative locks L1-L10)
- `decisions/DEC-0112.md` (installer payload decision)
- `docs/product/backlog.md` architecture_notes appended
- `docs/engineering/state.md` architecture checkpoint
- `handoffs/resume_brief.md` resume pointer
- `handoffs/po_to_tl.md` this handoff

### Composition Surface
DO NOT AMEND: US-0008, US-0018, US-0040, US-0054, US-0057, US-0075, US-0100, US-0101, US-0102, US-0103, US-0107, US-0110

### Phase Boundary
architecture PASS → sprint-plan (tech-lead, fresh context)
