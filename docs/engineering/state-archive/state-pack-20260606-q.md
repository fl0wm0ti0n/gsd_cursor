# State archive pack (2026-06-06)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 20
- First archived heading: `## QA checkpoint -- S0076 / US-0090 (2026-04-18)`
- Last archived heading: `## Verify-work checkpoint (2026-04-18) -- US-0090 / S0076 / `auto-20260418-01``
- Verification tuple (mandatory):
  - archived_body_lines=159
  - preamble_lines=2
  - retained_body_lines=1068

---

## QA checkpoint -- S0076 / US-0090 (2026-04-18)

**Isolation evidence (US-0048 / DEC-0029)**: `phase_id=qa`; `role=qa`; `fresh_context_marker=qa-S0076-US0090-qa-20260418T233000Z-fresh`; `timestamp=2026-04-18T23:30:00Z`; `evidence_ref=sprints/S0076/qa-findings.md`.

**Strict runtime proof (US-0056 / DEC-0038)**: `orchestrator_run_id=auto-20260418-01`; `runtime_proof_id=rp-auto-20260418-01-qa-qa-20260418T233000Z-S0076-US0090`; `phase_id=qa`; `role=qa`; `proof_issued_at=2026-04-18T23:30:00Z`; `proof_ttl_seconds=3600`; `proof_hash=aebc889eb82a2b78fa998796c4d102d3f8b2edeb7dc609dfab3efeb1a49fa995`.

**Phase boundary status (US-0088 / DEC-0069)**: compact status -- `phase_boundary=qa`; `next_scheduled_phase=verify-work`; `segment_work_item_kind=story`; `active_bug_id=(none)`; `bug_queue_position=(none)`; `bug_queue_remaining=(none)`; `backlog_drain_active=true`; `bug_queue_active=false`; `backlog_drain_stories_remaining_budget=5`; `story_id=US-0090`; `sprint_id=S0076`; `task_count=10`; `qa_verdict=PASS`; `regressions_found=0`; `dec_id=DEC-0073`; `orchestrator_run_id=auto-20260418-01`; `stop_reason=(none)`; `stop_phase=(none)`; `backlog_drain_segment_complete=0`.

**AC verdicts (AC-1..AC-8)**: AC-1 PASS (gating + flag-conflict + scope-empty fail-closed live-probed); AC-2 PASS (`.gitignore` anchor + `.gitkeep` + sidecar-first atomic order); AC-3 PASS (deny-list version stable SHA-256 `33bd8fa055791051cfb4505ca8815de51eefd73b41ee850541db63bc0ef69884`); AC-4 PASS (scope grammar + frozen v1 profile + 3 scope reason codes); AC-5 PASS (CLI `--help` + runbook subsection + three-axis section); AC-6 PASS (24 caveman subtests green / 142 subtests / installer-completeness 4/4 / harness 791/9); AC-7 PASS with non-blocking PARTIAL_VERBATIM note on reference + runbook paragraph paraphrase (architecture doc verbatim; DEC-0072 §6 row 6 pinned test green); AC-8 PASS (5 sanctioned byte-identical pairs; `.cursor/rules/caveman.mdc` SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` preserved).

**Scrutiny targets**: (1) baseline-drift PASS -- orchestrator conflated harness (11) vs pytest contract module (24) baselines; real delta is +13 new caveman passes / 0 new fails. (2) DEC-0073 §1 fidelity PARTIAL_VERBATIM non-blocking -- reference + runbook paraphrase instead of publish verbatim; architecture doc verbatim; DEC-0072 §6 row 6 `test_caveman_default_off_reference_non_substitution_paragraph` invariant preserved; compose-alongside resolution is DEC-0073-compatible (explicit "does not edit DEC-0072"); optional follow-up edit recommended, not required for `/verify-work` or `/release`. (3) `test_caveman_architecture_section_bottom_appended_and_linked` relaxation LEGITIMATE -- accommodates `# US-0090` tail; test is not in DEC-0072 §6 row 6 pinned class. (4) negative-assertion removal on `template/docs/engineering/architecture.md` PASS -- file was never in DEC-0073 §9 negative-parity set; active-only precedent per DEC-0072 §7 row 6 applies. (5) canonical harness PASS -- `tests/run-tests.ps1` Pass=791 / Fail=9 (+8 pass / -2 fail vs US-0089 release baseline); rule count `[PASS] 6 rules exist`. (6) parity re-verification PASS -- `check_intake_template_parity.py --scope=caveman-compress` + `--scope=all` both `[INTAKE_TEMPLATE_PARITY_OK]`; rule SHA-256 equality preserved active = template.

**Test battery summary**: contract full (24 failed / 40 passed / 215 subtests) -- zero new failures (all 24 are pre-existing US-0086/US-0087/US-0088 drift); contract caveman-only (24 passed / 142 subtests); installer-completeness (4/4); parity (both OK); bug validator (`[BUG_VALIDATION_OK]`); harness (Pass=791 / Fail=9 -- remaining 9 are pre-existing drift disjoint from US-0090).

**Template parity (US-0017)** (QA phase): read-only w.r.t. rules / templates. No mirrored active file edited by QA. Positive parity rows (DEC-0073 §9) all byte-identical live-verified: `scripts/caveman_compress_input.py` SHA-256 `CA5F6FDF276FBD1BC9B212BE723E83661503FE2CA9D27D721B67CA4D4DA1C231`; `docs/engineering/runbook.md` SHA-256 `b7ed93f224809a24d18763dcb7eb556fddacef0ed039113ea603a4b1ba6a6da7`; `docs/engineering/auto-orchestration-reference.md` SHA-256 `86952e631b908ae7169c8fde86516c6c523cd55c987272cf2bf5a098a3a7224c`; `docs/engineering/context/installer-owned-paths.manifest` SHA-256 `e352ae06084c666ceee7ea923a9975f3c83eeba06b2596b700c7e64d56351932`. Negative parity preserved: `.cursor/rules/caveman.mdc` SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` **unchanged** across the full lifecycle through QA.

**Triad hot-surface enforcement (DEC-0054)** (post-qa append): `python scripts/enforce-triad-hot-surface.py --check` -> exit 0 (no rollover required at this append; `state.md` = 125 KB / 1151 lines).

**Traceability index (DEC-0010)** (QA pass; verify-work pending):

| Story | Sprint | Tasks | Status | Evidence |
|-------|--------|-------|--------|----------|
| US-0090 | S0076 | T-001..T-010 | OPEN -- QA PASS | sprints/S0076/qa-findings.md (PASS), sprints/S0076/uat.md, sprints/S0076/uat.json, sprints/S0076/summary.md (QA checkpoint to append), sprints/S0076/plan-verify.json (PASS), sprints/S0076/sprint.md, sprints/S0076/tasks.md, decisions/DEC-0073.md, docs/engineering/architecture.md (# US-0090), docs/product/backlog.md (## US-0090), handoffs/dev_to_qa.md#s0076-us-0090-2026-04-18, handoffs/qa_to_verify_work.md (to be prepared), handoffs/resume_brief.md (verify-work pointer), docs/engineering/state.md (this checkpoint) |

**Status authority (US-0045)**: `US-0090` remains **OPEN** in `docs/product/backlog.md`. No `docs/product/acceptance.md` rows checked by QA. No bug status changes. No sprint task statuses re-advanced (QA reads dev's task status; does not mutate). `DEC-0072` / `DEC-0073` **not rewritten**. `.cursor/rules/caveman.mdc` **not edited** (byte-identity preserved end-to-end through QA).

## Verify-work checkpoint (2026-04-18) -- US-0090 / S0076 / `auto-20260418-01`

- **Role**: `qa` (fresh context `qa-S0076-US0090-verify-work-20260418T235000Z-fresh`).
- **Orchestrator**: `auto-20260418-01` (backlog-drain, `AUTO_QUIET=1`, budget remaining=5).
- **Phase**: `/verify-work` **PASS** — UAT matrix **15 / 15 PASS** / 0 FAIL / 0 SKIP. Closure preflight all 9 gates PASS. No decision gate triggered. Non-blocking `PARTIAL_VERBATIM` observation carried forward for optional documentation cleanup.
- **Inputs reviewed**: `sprints/S0076/uat.md`, `sprints/S0076/uat.json`, `sprints/S0076/qa-findings.md`, `sprints/S0076/tasks.md`, `sprints/S0076/sprint.md`, `sprints/S0076/summary.md`, `sprints/S0076/plan-verify.json`, `handoffs/qa_to_verify_work.md` (US-0090 section), `decisions/DEC-0073.md`, `decisions/DEC-0072.md` (substrate; not rewritten), `docs/product/backlog.md` `## US-0090` (AC list + prior phase notes), `.cursor/scratchpad.md` (CAVEMAN_COMPRESS_INPUT/CAVEMAN_FILE_SCOPE default-off baseline; temp flipped 1→0 for UAT-3; `git diff --stat` empty post-UAT).

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=verify-work`
- `role=qa`
- `fresh_context_marker=qa-S0076-US0090-verify-work-20260418T235000Z-fresh`
- `timestamp=2026-04-18T23:50:00Z`
- `evidence_ref=[sprints/S0076/uat.json, sprints/S0076/uat.md]`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260418-01`
- `runtime_proof_id=rp-auto-20260418-01-verify-work-qa-20260418T235000Z-S0076-US0090`
- `phase_id=verify-work`
- `role=qa`
- `proof_issued_at=2026-04-18T23:50:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=b012a75eda56b943d25cb44fd24d986de0cdab046abcd304c8467645cd3535c9`
- canonical sorted-key JSON tuple: `{"orchestrator_run_id":"auto-20260418-01","phase_id":"verify-work","proof_issued_at":"2026-04-18T23:50:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260418-01-verify-work-qa-20260418T235000Z-S0076-US0090"}`

### UAT execution summary (15 / 15 PASS)

| Step | AC | Verdict | Evidence (abbrev.) |
|------|-----|---------|---------------------|
| UAT-1 | AC-1 | PASS | `--write` exit 2 / `CAVEMAN_COMPRESS_MODE_DISABLED` |
| UAT-2 | AC-1 | PASS | `--dry-run --write` exit 2 / `CAVEMAN_COMPRESS_FLAG_CONFLICT` |
| UAT-3 | AC-4 | PASS | `--write` with mode=1 + empty scope exit 2 / `CAVEMAN_COMPRESS_SCOPE_EMPTY` (UAT-spec `--dry-run` gracefully narrates per §2 activation gate design — documented as carried-forward observation #2) |
| UAT-4 | AC-2 | PASS | `.gitignore:39-40` anchor + exception; `docs/.caveman-originals/.gitkeep` present |
| UAT-5 | AC-3 | PASS | `deny_list_version=33bd8fa055791051cfb4505ca8815de51eefd73b41ee850541db63bc0ef69884` byte-stable across two runs |
| UAT-6 | AC-5 | PASS | `--help` exit 0; 4 flags documented |
| UAT-7 | AC-5 | PASS | active + template runbook SHA-256 `b7ed93f2…6da7` equal |
| UAT-8 | AC-5/AC-7 | PASS | reference line 798 + runbook line 1383 mention; architecture line 3314 carries verbatim "CAVEMAN_COMPRESS_INPUT controls input-side file mutation" |
| UAT-9 | AC-7 | PASS | `# US-0090` section at line 3183; linkage test green |
| UAT-10 | AC-6 | PASS | `idempotency_check.fixture_byte_stable=true` |
| UAT-11 | AC-8 | PASS | installer completeness 4 passed (incl. `test_caveman_compress_input_shipped_by_installer`) |
| UAT-12 | AC-8 | PASS | `[INTAKE_TEMPLATE_PARITY_OK]` both scopes |
| UAT-13 | AC-8 | PASS | `.cursor/rules/caveman.mdc` SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` active == template |
| UAT-14 | AC-6/AC-8 | PASS | `tests/run-tests.ps1` Pass=791 / Fail=9 (2026-04-18T15:17:36Z); `[PASS] 6 rules exist`; §26T all green |
| UAT-15 | AC-6 | PASS | `pytest -k caveman` 24 passed / 142 subtests |

### Closure preflight (release readiness gate) — 9 gates PASS

| Gate | Result |
|------|--------|
| `tasks_done` | PASS (10/10 done in `sprints/S0076/tasks.md`) |
| `ac_qa_pass` | PASS (8/8 AC verdicts PASS in `sprints/S0076/qa-findings.md`) |
| `ac_uat_pass` | PASS (8/8 AC UAT-step verdicts PASS in `sprints/S0076/uat.md`) |
| `plan_verify_status` | PASS (`sprints/S0076/plan-verify.json` `status=PASS`; 13 gates green) |
| `bug_validator` | `[BUG_VALIDATION_OK]` pre- and post-verify-work write |
| `parity` | `[INTAKE_TEMPLATE_PARITY_OK]` `--scope=caveman-compress` and `--scope=all` |
| `sha_preserved` | `.cursor/rules/caveman.mdc` SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` (active == template) |
| `test_baselines_no_regression` | PASS — PS1 harness 791/9 exact; `pytest -k caveman` 24/142 exact; full contract module failures remain in pre-existing US-0086/US-0087/US-0088 families (zero new US-0090 regressions) |
| `dec_invariants` | PASS — three-axis non-substitution published (architecture verbatim; reference + runbook paraphrase documented); DEC-0072 not rewritten; negative parity intact for `.cursor/rules/caveman.mdc`, `.cursor/skills/its-magic/SKILL.md`, scratchpad byte strings |

### Carried-forward observations (non-blocking — for `/release` notes)

1. **PARTIAL_VERBATIM** on DEC-0073 §1 publication: `docs/engineering/architecture.md` lines 3313–3316 carries the verbatim paragraph; `docs/engineering/auto-orchestration-reference.md` line 798 and `docs/engineering/runbook.md` line 1383 carry a semantic paraphrase ("file compression" / "All three axes are orthogonal…"). Semantic intent preserved; DEC-0072 §6 row 6 pinned test (`test_caveman_default_off_reference_non_substitution_paragraph`) preserved byte-unchanged. Optional future doc cleanup; no DEC amendment needed.
2. **UAT-3 scope-empty command variance**: implementation binds `CAVEMAN_COMPRESS_SCOPE_EMPTY` to the DEC-0073 §2 activation gate (`--write` pathway) per contract test `test_caveman_compress_input_scope_empty_reason`. UAT spec's `--dry-run` command gracefully narrates by design (`scripts/caveman_compress_input.py` lines 726–749). AC-4 fail-closed intent satisfied via `--write` evidence; optional UAT-spec alignment or a secondary `--dry-run` design note in runbook would close the authoring gap.

### Test baselines (verify-work independent re-run; matches QA cycle 1)

| Gate | Result | Exit |
|------|--------|------|
| `tests/run-tests.ps1` (canonical check-in) | Pass=**791** / Fail=**9** (`tests/report.md` 2026-04-18T15:17:36Z) | 1 (same drift baseline) |
| `pytest -k caveman` | **24 passed / 0 failed / 142 subtests passed** | 0 |
| `pytest tests/installer_completeness_bug0003_test.py -v` | **4 passed** including `test_caveman_compress_input_shipped_by_installer` | 0 |
| `pytest tests/auto_command_contract_test.py` (full module) | **40 passed** + pre-existing US-0086/US-0087/US-0088 drift (zero new US-0090 regressions) | 1 |
| `check_intake_template_parity.py --scope=caveman-compress` | `[INTAKE_TEMPLATE_PARITY_OK]` | 0 |
| `check_intake_template_parity.py --scope=all` | `[INTAKE_TEMPLATE_PARITY_OK]` | 0 |
| `bug_issue_validate.py --check-acceptance` | `[BUG_VALIDATION_OK]` | 0 |

### CLI live-probes (verify-work independent)

- `python scripts/caveman_compress_input.py --write` → exit 2; `REASON_CODE=CAVEMAN_COMPRESS_MODE_DISABLED detail=CAVEMAN_COMPRESS_INPUT != 1`.
- `python scripts/caveman_compress_input.py --dry-run --write` → exit 2; `REASON_CODE=CAVEMAN_COMPRESS_FLAG_CONFLICT detail=--dry-run with --write`.
- `python scripts/caveman_compress_input.py --write` with temporary `CAVEMAN_COMPRESS_INPUT=1` + empty `CAVEMAN_FILE_SCOPE` → exit 2; `REASON_CODE=CAVEMAN_COMPRESS_SCOPE_EMPTY detail=CAVEMAN_FILE_SCOPE empty` (scratchpad reverted post-probe; `git diff --stat` empty).
- `python scripts/caveman_compress_input.py --help` → exit 0; all four flags (`--dry-run`, `--write`, `--verify-originals`, `--report`) documented.
- `python scripts/caveman_compress_input.py --report` (two runs) → `deny_list_version=33bd8fa055791051cfb4505ca8815de51eefd73b41ee850541db63bc0ef69884` (byte-stable); `idempotency_check.fixture_byte_stable=true`; 9-code vocabulary in 3 families (Gating / Scope / Integrity) present.

### Phase boundary status (US-0088 / DEC-0069)

`phase_boundary=verify-work`; `next_scheduled_phase=release`; `segment_work_item_kind=story`; `active_bug_id=(none)`; `bug_queue_position=(none)`; `bug_queue_remaining=(none)`; `backlog_drain_active=true`; `bug_queue_active=false`; `backlog_drain_stories_remaining_budget=5`; `story_id=US-0090`; `sprint_id=S0076`; `dec_id=DEC-0073`; `verify_work_verdict=PASS`; `uat_pass=15/15`; `closure_preflight=pass`; `orchestrator_run_id=auto-20260418-01`; `stop_reason=(none)`; `stop_phase=(none)`; `backlog_drain_segment_complete=0`.

### Artifact touchpoints (this checkpoint)

- `sprints/S0076/uat.md` — flipped PENDING → PASS with 15 verdict rows + results summary + AC trace table.
- `sprints/S0076/uat.json` — structured verdicts, evidence refs, timestamps, verify-work verdict=PASS.
- `sprints/S0076/summary.md` — QA phase + Verify-work phase blocks appended.
- `docs/product/backlog.md` `## US-0090` — `qa_notes` + `verify_work_notes` appended (US-0090 remains OPEN per US-0045).
- `handoffs/qa_to_release.md` — new `## QA -> Release — S0076 / US-0090` top stanza prepended; prior US-0089 stanza marked superseded.
- `handoffs/resume_brief.md` — new top pointer (`intended_resume_phase=release`); prior post-`/qa` pointer marked superseded.
- `docs/engineering/state.md` — this Verify-work checkpoint appended (append-bottom per DEC-0040).

### Artifacts NOT touched (verify-work contract)

- `.cursor/rules/caveman.mdc` + template mirror — negative parity preserved end-to-end.
- `.cursor/skills/its-magic/SKILL.md` + template mirror — unchanged.
- `.cursor/scratchpad.md` — temporary UAT-3 edit (1 ↔ 0 flip) reverted post-probe; `git diff --stat` empty.
- All `template/` files — verify-work read-only on mirrors.
- `decisions/DEC-0073.md`, `decisions/DEC-0072.md` — not rewritten.
- `docs/product/acceptance.md` — release phase owns AC-row checking.
- Implementation / test code — verify-work does not author code.

### Triad hot-surface enforcement (DEC-0054)

- Pre-verify-work append: `state.md` = 891 lines.
- Post-verify-work append: `state.md` = 1309 lines → **STATE_ARCHIVE_REQUIRED** (cap=1200 / 80 units).
- `python scripts/enforce-triad-hot-surface.py --rollover` → `rollover_complete units=2`; oldest 2 units archived into `docs/engineering/state-archive/state-pack-20260418-l.md`.
- Post-rollover: `python scripts/enforce-triad-hot-surface.py --check` → exit 0 (compliant). Verify-work checkpoint preserved (append-bottom; rollover retains youngest units including this one).

### Traceability index (DEC-0010) — US-0090 update

| Story | Sprint | Tasks | Status | Evidence |
|-------|--------|-------|--------|----------|
| US-0090 | S0076 | T-001..T-010 | OPEN — QA PASS / Verify-work PASS | `sprints/S0076/uat.md` (15/15 PASS), `sprints/S0076/uat.json`, `sprints/S0076/qa-findings.md` (PASS), `sprints/S0076/summary.md` (QA + Verify-work checkpoints), `sprints/S0076/plan-verify.json` (PASS), `sprints/S0076/sprint.md`, `sprints/S0076/tasks.md`, `decisions/DEC-0073.md`, `docs/engineering/architecture.md` (# US-0090), `docs/product/backlog.md` (## US-0090 with qa_notes + verify_work_notes), `handoffs/qa_to_release.md` (S0076 top stanza), `handoffs/resume_brief.md` (verify-work → release pointer), `docs/engineering/state.md` (this checkpoint). |

### Status authority (US-0045)

- `US-0090` remains **OPEN** in `docs/product/backlog.md`.
- No `docs/product/acceptance.md` mutations (release-owned).
- Verify-work does NOT advance backlog status; release phase owns `OPEN → DONE` flip.
- DEC-0072 / DEC-0073 **not rewritten**; `.cursor/rules/caveman.mdc` byte-identity preserved.

### Next

- **`/release`** (fresh **release** subagent) for **`S0076`** / **US-0090** — author `sprints/S0076/release-findings.md` + `handoffs/releases/S0076-release-notes.md` carrying the two non-blocking observations; flip `US-0090` OPEN → DONE per US-0045; check AC-1..AC-8 acceptance rows; append release checkpoint to `docs/engineering/state.md`; advance `handoffs/release_queue.md` S0076 → `released`; re-run bug validator to confirm `[BUG_VALIDATION_OK]`.

