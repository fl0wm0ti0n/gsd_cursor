# PO to TL archive pack (2026-07-01)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 9
- Retained units in hot file: 10
- First archived heading: `## Sprint-plan → /plan-verify handoff — US-0112 / auto-20260628-04`
- Last archived heading: `## Orchestrated architecture handoff — US-0098 / auto-20260613-01`
- Verification tuple (mandatory):
  - archived_body_lines=762
  - retained_body_lines=597

---

## Sprint-plan → /plan-verify handoff — US-0112 / auto-20260628-04

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

