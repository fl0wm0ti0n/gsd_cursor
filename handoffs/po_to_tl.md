## Orchestrated discovery handoff — BUG-0010 / auto-20260606-02

### Target

- `bug_id=BUG-0010`
- `orchestrator_run_id=auto-20260606-02`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-BUG0010-discovery-20260606T141701Z-fresh`
- `next_scheduled_phase=research`
- `segment_work_item_kind=bug`
- `bug_queue_position=2` / `bug_queue_remaining=2`

### Summary

- **`/discovery`** **PASS** — root cause confirmed: `enforce-triad-hot-surface.py` `STORY_HEADING` matches only H1 `# US-xxxx`; `## US-xxxx` story sections invisible → `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS` when `architecture.md` exceeds `ARCH_HOT_MAX_LINES` with zero archivable chunks. Kit repo mixed inventory: **26** H1 + **5** H2 `## US-` (3495 lines). Operator fix (**both**, intake-locked): (A) extend archiver for `##` backward-compat rollover; (B) enforce H1 `# US-xxxx` for new `/architecture` writes.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Key findings (research inputs)

1. **Defect line**: `STORY_HEADING = re.compile(r'^# US-\d{4}\s*[:\u2014\-].+$')` — `split_arch_stories` / `rollover_architecture` lines 138–356.
2. **Failure mode**: oversize + `stories=[]` → `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS` (not `ARTIFACT_HOT_SURFACE_OVERSIZE` after failed rollover attempt).
3. **Kit vs downstream**: kit can rollover via H1 boundaries; `##`-only downstream repos cannot (operator: 3021/3000 lines).
4. **Mixed-file precedence (discovery stub)**: H1 wins when same `US-xxxx` at both levels; only `## US-\d{4}` is a story boundary (not generic `##`).
5. **Enforcement surfaces**: `.cursor/commands/architecture.md` + `template/`; optional validator script; `enforce-triad-hot-surface.py --self-test`; runbook triad section; harness + template parity.

### Research asks (extend R-0076)

1. Dual-level regex shape and merge algorithm for `split_arch_stories`.
2. Mixed-file precedence table (kit has US-0067..0070 + US-0083 at H2).
3. Validator placement and reason-code family for forward enforcement.
4. Block vs warn at `/architecture` completion boundary.
5. Self-test + harness regression matrix (`##`-only, `# US-`, mixed, idempotent rollover).
6. `BUG-xxxx` H1 pattern parity; installer/template parity scope.

### Evidence refs

- `docs/product/backlog.md` (`### BUG-0010` — `discovery_notes`)
- `docs/product/vision.md` (Intake notes + Discovery Notes — BUG-0010)
- `docs/engineering/research.md` (**`R-0076`** discovery extension)
- `handoffs/intake_evidence/BUG-0010-intake-20260606.json`
- `scripts/enforce-triad-hot-surface.py`; `decisions/DEC-0054.md` §2
- `docs/engineering/architecture.md` (mixed `# US-` / `## US-` inventory)
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (research pointer)

### Next

- **`/research`** (fresh **tech-lead** context) for **`BUG-0010`** — resolve **`R-0076`** Q1–Q6 before **`/architecture`**.

### Decision gate

- **None** — discovery satisfied; bug **OPEN**.

---

## Intake handoff — BUG-0010 / cursor-20260606-BUG0010-intake

### Target

- `bug_id=BUG-0010`
- `intake_run_id=cursor-20260606-BUG0010-intake`
- phase completed: **`intake`** (**`po`**)
- `next_scheduled_phase=discovery`
- `work_item_kind=bug` (`/intake bug`)
- `INTAKE_GUIDED_MODE=1`, `INTAKE_WORK_ITEM_KIND=bug` (argv override), `INTAKE_SUBAGENT_FALLBACK=deny`

### Summary

- **Defect**: Triad archiver (`scripts/enforce-triad-hot-surface.py`) only splits `docs/engineering/architecture.md` on H1 `# US-xxxx` headings. Repos where agents wrote story sections as `## US-xxxx` hit `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS` when the file exceeds `ARCH_HOT_MAX_LINES` — rollover finds zero chunks, `/auto` stops with non-suppressible `blocked` (operator report: discovery PASS on US-0016, then triad gate fail at 3021/3000 lines).
- **Operator fix choice (AskQuestion)**: **both** — (1) extend archiver to recognize `## US-xxxx` as story-section boundaries (backward-compatible rollover); (2) enforce H1 `# US-xxxx` for new `/architecture` writes (validator + command/template parity per **DEC-0054**).
- Distinct from **BUG-0009** (CI template leak). Related governance: **US-0072**, **DEC-0054**, **DEC-0043**.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Proposed fix direction (defer exact design to /architecture)

- Extend `STORY_HEADING` / `split_arch_stories` to treat `## US-xxxx` as archival units (oldest-first, same as `# US-xxxx`).
- Add heading-level validator or contract test; update `.cursor/commands/architecture.md` (+ `template/`) to mandate H1 `# US-xxxx` for new sections.
- Regression: `##`-only fixture rollovers when over cap; `# US-` non-regression; `enforce-triad-hot-surface.py --self-test` extended; runbook operator note for one-time `##`→`#` normalization in existing repos.

### Risks

- **Double-counting** if both `# US-` and `## US-` exist at same id — architecture must define precedence.
- **Nested `##` inside a US block** — archiver must not split on non-story `##` headings.
- **Kit repo mixed headings** — this repo already has 30 `# US-` + 5 `## US-` sections; fix must handle mixed files.

### Intake evidence (US-0078 / DEC-0060)

- `selected_pack=small-intake-pack`; `missing_topics=[]`; `assumptions_confirmed=(none)`
- `outcome_success_criteria` + `constraints_compatibility_risks` = `answer_ref` (operator chat + **both** fix choice); `impacted_components` / `required_tests_acceptance_checks` / `done_definition` = `delegation_ref` per **DEC-0067**
- Validator: `python scripts/intake_evidence_validate.py --file handoffs/intake_evidence/BUG-0010-intake-20260606.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**

### Evidence refs

- `docs/product/backlog.md` (`### BUG-0010`); `docs/product/acceptance.md` (unchecked row)
- `handoffs/intake_evidence/BUG-0010-intake-20260606.json`
- `scripts/enforce-triad-hot-surface.py` (`STORY_HEADING`, `rollover_architecture`); `decisions/DEC-0054.md`
- `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` → **`[BUG_VALIDATION_OK]`**
- `handoffs/resume_brief.md` refreshed: **`[INTAKE_BUG_RESUME_BRIEF_REFRESH_OK]`** (`bug_id=BUG-0010`, `intended_resume_phase=discovery`)

### Next

- **`/discovery`** (fresh PO context) for **BUG-0010** — confirm heading-mix inventory, archiver precedence rules, and enforcement surface for `/architecture`.

---

## Orchestrated discovery handoff — US-0091 / auto-20260606-01

### Target

- `story_id=US-0091`
- `orchestrator_run_id=auto-20260606-01`
- phase completed: **`discovery`** (**`po`**)
- `next_scheduled_phase=research`
- `fresh_context_marker=po-US0091-discovery-20260606T132027Z-fresh`
- `decomposition=single_story` (operator explicit; per `US-0051`)
- `priority=P1`
- `backlog_drain_active=true`

### Summary

- **Static-coverage gap**: `US-0030` (DONE) blocks README/runbook **deltas** when commands/flags change; it does **not** assert that every DONE user-visible feature already has a blurb. `US-0091` closes that gap with audit + backfill + a **second blocking check** in the `/release` doc-gate surface.
- **Three-file target** (audience + parity): root `README.md` (operator blurbs), `template/README.md` (byte parity per `US-0017`), `docs/developer/README.md` (`DEV_*` traceability rows per `DEC-0059`).
- **Discovery-locked predicate**: backlog block field **`user_visible: true|false`** is canonical validator input; optional acceptance row `(user_visible)` suffix is human-scan only. In-scope = **DONE** + `user_visible: true` (explicit) or migration-heuristic pass for unset fields; out-of-scope = `user_visible: false` or pure-internal surfaces. Ambiguous → `README_FEATURE_COVERAGE_INPUT_INVALID`.
- **Section placement**: backfill adds **bullets/sub-entries within existing H2s** — no new H2s; affinity map in vision/backlog discovery notes; `validate_doc_profile.py` section budgets unchanged.
- **Grandfathering**: blocking gate activates in the **same sprint/commit** as backfill — no retroactive `/release` block before catalog is populated (**AC-10**).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Acceptance pointers (discovery emphasis)

- **AC-1**: predicate + `user_visible` marker contract (backlog field canonical).
- **AC-2**: deterministic audit report (`coverage_total` / gaps list).
- **AC-3–AC-4**: three-file backfill + audience/profile compliance.
- **AC-5–AC-7**: validator script, `/release` composition on `US-0030`, idempotent `--report`.
- **AC-8–AC-9**: `US-0071` hygiene + `US-0017` template parity for new script/content.
- **AC-10**: companion `DEC-xxxx` with grandfathering + composition semantics.

### Top risks (carry to /research)

- **R1** False positives without bounded predicate — mitigation: explicit `user_visible` markers + fail-closed ambiguous.
- **R2** README bloat across ~90 DONE stories — mitigation: 1–2 sentence blurbs, existing section budgets.
- **R3** Three-file parity drift — mitigation: compose with `US-0017`, extend parity tests not duplicate logic.
- **R4** Retroactive release lock-in — mitigation: same-sprint atomic delivery + grandfathering toggle.
- **R5** `US-0071` token leakage in backfilled prose — mitigation: existing scanner stays green.
- **R6** Migration heuristic ambiguity for unset `user_visible` — mitigation: research locks deterministic rules table.

### Research asks (extend **`R-0074`**)

1. Validator placement and CLI grammar — candidate `scripts/validate_readme_feature_coverage.py` with `--self-test`, `--report`, stable JSON (`coverage_total` / `coverage_present` / `coverage_missing`).
2. Release-gate wiring point — where `/release` / `validate-and-push` invokes the second check (active + `template/`).
3. Migration heuristic table — deterministic rules for unset `user_visible` during one-time backfill pass.
4. Section-affinity manifest — `US-xxxx`/`BUG-xxxx` → root H2 + DEV H2 anchor (no new headings).
5. Grandfathering / first-activation toggle — report-only vs blocking enablement contract.
6. Template parity inventory — extend `check_intake_template_parity.py` or sibling test for new validator script paths.

### Evidence refs

- `docs/product/backlog.md` (`## US-0091` — discovery_notes appended)
- `docs/product/vision.md` (**Discovery Notes — US-0091**)
- `docs/product/acceptance.md` (`US-0091` row — unchecked)
- `handoffs/intake_evidence/US-0091-intake-20260510.json`
- `docs/engineering/research.md` (**`R-0074`** — discovery extension appended)
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/research`)
- Adjacent: `US-0030`, `US-0077`/`DEC-0059`, `US-0017`, `US-0071`, `DEC-0040`

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0091`** — deepen **`R-0074`**, lock validator/release wiring, migration heuristic, and grandfathering before **`/architecture`**.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

## Orchestrated research handoff — US-0091 / auto-20260606-01

### Target

- `story_id=US-0091`
- `orchestrator_run_id=auto-20260606-01`
- phase completed: **`research`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0091-research-20260606T140500Z-fresh`
- `next_scheduled_phase=architecture`
- `decomposition=single_story` (operator explicit; per `US-0051`)
- `priority=P1`

### Summary

- **`/research`** **PASS** — extended **`R-0074`** with implementation-ready findings: predicate Option A (`user_visible: true|false` backlog field canonical; migration heuristic H1–H8 for unset fields; H7 fail-closed); stable audit/`--report` JSON schema; validator API sketch (`scripts/validate_readme_feature_coverage.py` + `readme_feature_coverage_lib.py`); release step **3f** as second scripted check composed on **US-0030** doc-delta (unchanged); section-affinity manifest; grandfathering via `README_FEATURE_COVERAGE_ENFORCE=0|1` (default **0** until backfill); template parity `--scope=readme-feature-coverage`.
- **Repo facts**: ~90 story blocks, zero `user_visible:` markers today; root README ~52 id token hits but incomplete catalog; DEV shard sparse; US-0030 has no dedicated script — US-0091 adds first scripted static-coverage gate.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Key findings (architecture inputs)

1. **Predicate**: backlog-only input; acceptance `(user_visible)` suffix human-scan only; post-backfill explicit markers required when enforce=1.
2. **Validator**: stdlib Python; `--self-test`, `--report`, `--enforce`; reason codes per AC-5; profile budget via `doc_profile_lib` composition.
3. **Release wiring**: new step **3f** in `.cursor/commands/release.md` (+ `template/`); NOT `validate-and-push`.
4. **Grandfathering**: same-sprint flip `README_FEATURE_COVERAGE_ENFORCE` **0→1** with backfill merge (**AC-10**).
5. **Parity**: extend `check_intake_template_parity.py`; compose US-0017 README byte guard.

### Evidence refs

- `docs/engineering/research.md` (**`R-0074`** research extension)
- `docs/product/backlog.md` (`## US-0091` — `research_notes`)
- `docs/product/vision.md` (**Discovery Notes — US-0091**)
- `handoffs/intake_evidence/US-0091-intake-20260510.json`
- `docs/engineering/state.md` (Research checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/architecture`)
- Adjacent: `US-0030`, `US-0077`/`DEC-0059`, `US-0017`, `US-0071`, `scripts/validate_doc_profile.py`, `doc_profile_lib.py`

### Architecture asks (DEC-xxxx companion)

1. Lock predicate + heuristic table + enforce key in companion **DEC-xxxx** composing on **DEC-0030** + **DEC-0059**.
2. Author `docs/engineering/architecture.md` **`# US-0091`** with gate composition diagram and parity inventory.
3. Confirm lib split vs monolithic validator; lock run-tests section id.

### Next

- **`/architecture`** (fresh **tech-lead** context) for **`US-0091`** — lock **DEC-xxxx** + architecture section before **`/sprint-plan`**.

### Decision gate

- **None** — research satisfied; story **OPEN**.

---

## Orchestrated architecture handoff — US-0091 / auto-20260606-01

### Target

- `story_id=US-0091`
- `orchestrator_run_id=auto-20260606-01`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0091-architecture-20260606T143000Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `decomposition=single_story` (operator explicit; per `US-0051`)
- `priority=P1`

### Summary

- **`/architecture`** **PASS** — **`DEC-0074`** authored; **`docs/engineering/architecture.md`** **`# US-0091`** appended; predicate H1–H8 + backlog **`user_visible:`** field locked; validator **`scripts/validate_readme_feature_coverage.py`** + **`readme_feature_coverage_lib.py`**; release step **3f** composed on **US-0030** (delta gate unchanged); grandfathering via **`README_FEATURE_COVERAGE_ENFORCE=0|1`** (default **0**); section-affinity manifest; reason codes per AC-5; template parity **`--scope=readme-feature-coverage`**; harness **§27U**.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Locked decisions (DEC-0074 summary)

1. **Predicate Option A** — backlog `user_visible: true|false` canonical; heuristic H1–H8 for unset fields when enforce=0; H7 fail-closed on ambiguous stories.
2. **Validator lib split** — `validate_readme_feature_coverage.py` + `readme_feature_coverage_lib.py` (stdlib-only).
3. **Release composition** — step **3f** after **3e**, before step **4** UAT; NOT `validate-and-push`.
4. **Grandfathering** — `README_FEATURE_COVERAGE_ENFORCE=0|1` (default **0**); same-sprint flip with backfill.
5. **Reason codes** — umbrella `README_FEATURE_COVERAGE_BLOCKED` + gap/parity/input/profile sub-codes.
6. **Template parity** — 6-row inventory + `--scope=readme-feature-coverage`.

### Atomic task seeds (10; `/sprint-plan` converts to T-xxx)

See **`docs/engineering/architecture.md`** **`# US-0091`** § Atomic task seeds.

### Evidence refs

- `decisions/DEC-0074.md`
- `docs/engineering/architecture.md` (**`# US-0091`**)
- `docs/engineering/decisions.md` (index + context pack)
- `docs/product/backlog.md` (`## US-0091` `architecture_notes`)
- `docs/engineering/research.md` (**`R-0074`**)
- `docs/engineering/state.md` (Architecture checkpoint — this run)
- `handoffs/resume_brief.md` (sprint-plan pointer)

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`US-0091`** — seed sprint from 10 task seeds + AC ↔ § map.

### Decision gate

- **None** — architecture satisfied; story **OPEN**.

---

## Orchestrated sprint-plan handoff — US-0091 / S0077 / auto-20260606-01

### Target

- `story_id=US-0091`
- `sprint_id=S0077`
- `orchestrator_run_id=auto-20260606-01`
- phase completed: **`sprint-plan`** (**`tech-lead`**)
- `fresh_context_marker=tl-S0077-US0091-sprint-plan-20260606T150000Z-fresh`
- `next_scheduled_phase=plan-verify`
- `dec_id=DEC-0074`

### Summary

- **`/sprint-plan`** **PASS** — sprint **`S0077`** created; **AC-1..AC-10 ↔ T-001..T-010** strict bijection; `task_count=10`, `within_limit=true` (≤ `SPRINT_MAX_TASKS=12`); `plan-verify.json` status **PENDING**.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1 | Predicate lib (`readme_feature_coverage_lib.py`) |
| T-002 | AC-2 | Audit report (`--audit-out`, gap artifact) |
| T-003 | AC-3 | Three-file backfill + `user_visible:` markers |
| T-004 | AC-4 | Section-affinity manifest + audience boundaries |
| T-005 | AC-5 | Validator CLI + reason codes + `--self-test` |
| T-006 | AC-6 | Release step 3f + runbook delta-vs-static |
| T-007 | AC-7 | Idempotent `--report` + harness §27U |
| T-008 | AC-8 | US-0071 metadata hygiene |
| T-009 | AC-9 | Template parity + installer manifest |
| T-010 | AC-10 | Grandfathering toggle + activation + DEC linkage |

### Evidence refs

- `sprints/S0077/sprint.md`, `sprints/S0077/tasks.md`, `sprints/S0077/plan-verify.json`
- `decisions/DEC-0074.md`
- `docs/engineering/architecture.md` (**`# US-0091`**)
- `docs/product/backlog.md` (`## US-0091` `sprint_plan_notes`)
- `handoffs/tl_to_dev.md` (S0077 handoff prepended)
- `handoffs/qa_plan_verify.md` (S0077 PENDING queue)
- `docs/engineering/state.md` (Sprint-plan checkpoint — this run)

### Next

- **`/plan-verify`** (fresh **qa** context) for **`S0077`** / **`US-0091`**.

### Decision gate

- **None** — sprint plan satisfied; story **OPEN**.

---

## Orchestrated architecture handoff — BUG-0009 / auto-20260606-02

### Target

- `bug_id=BUG-0009`
- `orchestrator_run_id=auto-20260606-02`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-BUG0009-architecture-20260606T160000Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `segment_work_item_kind=bug`
- `bug_queue_position=1` / `bug_queue_remaining=3`
- `dec_id=DEC-0075`

### Summary

- **`/architecture`** **PASS** — **`DEC-0075`** authored; **`docs/engineering/architecture.md`** **`# BUG-0009`** appended; **`R-0075`** Q4 (US-0017 negative parity) resolved; template in-place job subtraction + drift guard + harness **§28B** + empty template `TEST_COMMAND` bootstrap locked.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Locked decisions (DEC-0075 summary)

1. **CI split** — template `ci.yml`: `checks`+`auto-fix` only; active: five jobs retained.
2. **US-0017 negative parity** — `ci.yml` + template runbook `TEST_COMMAND:` line exceptions; guard scripts byte-identical.
3. **Drift guard** — `check_downstream_ci_guard.py` + `downstream_ci_guard_lib.py`; **§28B**; `test_bug0009_*` contract tests.
4. **Forbidden patterns** + three reason codes (template scan + active positive inventory).
5. **checks green-by-default** — `no tests configured yet`; fail only on configured failure.
6. **Install smoke** — `installer_completeness_bug0003_test.py` job inventory (missing + upgrade).
7. **Operator docs** — upgrade remediation blurb.

### Atomic task seeds (10)

See **`docs/engineering/architecture.md`** **`# BUG-0009`** § Atomic task seeds.

### Evidence refs

- `decisions/DEC-0075.md`
- `docs/engineering/architecture.md` (**`# BUG-0009`**)
- `docs/engineering/decisions.md` (index + context pack)
- `docs/product/backlog.md` (`### BUG-0009` `architecture_notes`)
- `docs/engineering/research.md` (**`R-0075`**)
- `docs/engineering/state.md` (Architecture checkpoint — this run)
- `handoffs/tl_to_dev.md` (BUG-0009 architecture handoff)
- `handoffs/resume_brief.md` (sprint-plan pointer)

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`BUG-0009`** — seed sprint from 10 task seeds + AC ↔ § map.

### Decision gate

- **None** — architecture satisfied; bug **OPEN**.

---

## Orchestrated sprint-plan handoff — BUG-0010 / S0079 / auto-20260606-02

### Target

- `bug_id=BUG-0010`
- `sprint_id=S0079`
- `orchestrator_run_id=auto-20260606-02`
- phase completed: **`sprint-plan`** (**`tech-lead`**)
- `fresh_context_marker=tl-S0079-BUG0010-sprint-plan-20260606T170000Z-fresh`
- `next_scheduled_phase=plan-verify`
- `dec_id=DEC-0076`

### Summary

- **`/sprint-plan`** **PASS** — sprint **`S0079`** created; **AC-1..AC-8** surjective via **T-001..T-009**; `task_count=9`, `within_limit=true` (≤ `SPRINT_MAX_TASKS=12`); `plan-verify.json` status **PENDING**.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1, AC-2, AC-3, AC-7 | Dual-level archiver + H1-wins merge (+ template mirror) |
| T-002 | AC-4 | `count_h2_story_headings` + `check_arch_heading_policy` + CLI |
| T-003 | AC-1, AC-2, AC-3, AC-6 | Extended `--self-test` fixture classes |
| T-004 | AC-4, AC-5 | Architecture command H1 mandate + policy step |
| T-005 | AC-5, AC-6 | Contract tests `test_bug0010_*` |
| T-006 | AC-6 | Harness **§29A** |
| T-007 | AC-1, AC-3 | Optional `triad_arch_headings/` fixtures |
| T-008 | AC-8 | Runbook legacy `## US-` remediation blurb |
| T-009 | AC-5 | Architecture + DEC linkage assert |

### Evidence refs

- `sprints/S0079/sprint.md`, `sprints/S0079/tasks.md`, `sprints/S0079/plan-verify.json`
- `decisions/DEC-0076.md`
- `docs/engineering/architecture.md` (**`# BUG-0010`**)
- `docs/product/backlog.md` (`### BUG-0010` `sprint_plan_notes`)
- `handoffs/tl_to_dev.md` (S0079 handoff prepended)
- `handoffs/qa_plan_verify.md` (S0079 PENDING queue)
- `docs/engineering/state.md` (Sprint-plan checkpoint — this run)

### Next

- **`/plan-verify`** (fresh **qa** context) for **`S0079`** / **`BUG-0010`**.

### Decision gate

- **None** — sprint plan satisfied; bug **OPEN**.

---

## Orchestrated sprint-plan handoff — BUG-0009 / S0078 / auto-20260606-02

### Target

- `bug_id=BUG-0009`
- `sprint_id=S0078`
- `orchestrator_run_id=auto-20260606-02`
- phase completed: **`sprint-plan`** (**`tech-lead`**)
- `fresh_context_marker=tl-S0078-BUG0009-sprint-plan-20260606T140023Z-fresh`
- `next_scheduled_phase=plan-verify`
- `dec_id=DEC-0075`

### Summary

- **`/sprint-plan`** **PASS** — sprint **`S0078`** created; **AC-1..AC-8** surjective via **T-001..T-010**; `task_count=10`, `within_limit=true` (≤ `SPRINT_MAX_TASKS=12`); `plan-verify.json` status **PENDING**.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1, AC-4 | Template `ci.yml` downstream-safe + checks hardening |
| T-002 | AC-2, AC-4 | Active `ci.yml` checks hardening; five jobs preserved |
| T-003 | AC-5 | Template runbook empty `TEST_COMMAND:` |
| T-004 | AC-3, AC-7 | Drift guard lib + CLI |
| T-005 | AC-3, AC-7 | Contract tests `test_bug0009_*` |
| T-006 | AC-3 | Harness **§28B** |
| T-007 | AC-6 | Install-completeness job-inventory smoke |
| T-008 | AC-6, AC-7 | Installer manifest + parity scope |
| T-009 | AC-8 | Operator upgrade remediation docs |
| T-010 | AC-7 | Architecture linkage assert |

### Evidence refs

- `sprints/S0078/sprint.md`, `sprints/S0078/tasks.md`, `sprints/S0078/plan-verify.json`
- `decisions/DEC-0075.md`
- `docs/engineering/architecture.md` (**`# BUG-0009`**)
- `docs/product/backlog.md` (`### BUG-0009` `sprint_plan_notes`)
- `handoffs/tl_to_dev.md` (S0078 handoff prepended)
- `handoffs/qa_plan_verify.md` (S0078 PENDING queue)
- `docs/engineering/state.md` (Sprint-plan checkpoint — this run)

### Next

- **`/plan-verify`** (fresh **qa** context) for **`S0078`** / **`BUG-0009`**.

### Decision gate

- **None** — sprint plan satisfied; bug **OPEN**.

---

## Orchestrated architecture handoff — BUG-0010 / auto-20260606-02

### Target

- `bug_id=BUG-0010`
- `orchestrator_run_id=auto-20260606-02`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-BUG0010-architecture-20260606T142242Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `segment_work_item_kind=bug`
- `bug_queue_position=2` / `bug_queue_remaining=2`
- `dec_id=DEC-0076`

### Summary

- **`/architecture`** **PASS** — **`DEC-0076`** authored; **`docs/engineering/architecture.md`** **`# BUG-0010`** appended; dual-level archiver (`STORY_HEADING_H1` + `STORY_HEADING_H2`, H1-wins precedence); diff-gated `ARCH_STORY_HEADING_LEVEL_INVALID` forward enforcement; in-place `enforce-triad-hot-surface.py` extension; harness **§29A**; `test_bug0010_*` contract tests; command + runbook template parity; DEC-0054 §2 doc-only amendment.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Locked decisions (DEC-0076 summary)

1. **Dual-level regex** — two-pattern scan + H1-wins merge filter (not single alternation).
2. **Precedence table** — mixed kit file (26×H1 + 5×H2) is regression anchor.
3. **Forward enforcement** — diff-gated hard fail when H2 story-heading count increases; grandfathered `## US-` allowed.
4. **In-place script** — `count_h2_story_headings` + `check_arch_heading_policy` in `enforce-triad-hot-surface.py`.
5. **Reason codes** — `ARCH_STORY_HEADING_LEVEL_INVALID` (new); existing triad codes unchanged.
6. **Harness §29A** — additive; existing triad self-test block unchanged.
7. **Template parity** — script + architecture command + runbook (no new parity scope).
8. **BUG H1 parity** — `# BUG-xxxx` in rollover H1 family.

### Atomic task seeds (9)

See **`docs/engineering/architecture.md`** **`# BUG-0010`** § Atomic task seeds.

### Evidence refs

- `decisions/DEC-0076.md`
- `docs/engineering/architecture.md` (**`# BUG-0010`**)
- `docs/engineering/decisions.md` (index + context pack)
- `docs/product/backlog.md` (`### BUG-0010` `architecture_notes`)
- `docs/engineering/research.md` (**`R-0076`**)
- `docs/engineering/state.md` (Architecture checkpoint — this run)
- `handoffs/resume_brief.md` (sprint-plan pointer)

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`BUG-0010`** — seed sprint from 9 task seeds + AC ↔ § map.

### Decision gate

- **None** — architecture satisfied; bug **OPEN**.

---

## Orchestrated sprint-plan handoff — BUG-0010 / S0079 / auto-20260606-02

### Target

- `bug_id=BUG-0010`
- `sprint_id=S0079`
- `orchestrator_run_id=auto-20260606-02`
- phase completed: **`sprint-plan`** (**`tech-lead`**)
- `fresh_context_marker=tl-S0079-BUG0010-sprint-plan-20260606T170000Z-fresh`
- `next_scheduled_phase=plan-verify`
- `dec_id=DEC-0076`

### Summary

- **`/sprint-plan`** **PASS** — sprint **`S0079`** created; **AC-1..AC-8** surjective via **T-001..T-009**; `task_count=9`, `within_limit=true` (≤ `SPRINT_MAX_TASKS=12`); `plan-verify.json` status **PENDING**.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### AC ↔ Task map (locked)

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1, AC-2, AC-3, AC-7 | Dual-level archiver + H1-wins merge (+ template mirror) |
| T-002 | AC-4 | `count_h2_story_headings` + `check_arch_heading_policy` + CLI |
| T-003 | AC-1, AC-2, AC-3, AC-6 | Extended `--self-test` fixture classes |
| T-004 | AC-4, AC-5 | Architecture command H1 mandate + policy step |
| T-005 | AC-5, AC-6 | Contract tests `test_bug0010_*` |
| T-006 | AC-6 | Harness **§29A** |
| T-007 | AC-1, AC-3 | Optional `triad_arch_headings/` fixtures |
| T-008 | AC-8 | Runbook legacy `## US-` remediation blurb |
| T-009 | AC-5 | Architecture + DEC linkage assert |

### Evidence refs

- `sprints/S0079/sprint.md`, `sprints/S0079/tasks.md`, `sprints/S0079/plan-verify.json`
- `decisions/DEC-0076.md`
- `docs/engineering/architecture.md` (**`# BUG-0010`**)
- `docs/product/backlog.md` (`### BUG-0010` `sprint_plan_notes`)
- `handoffs/tl_to_dev.md` (S0079 handoff prepended)
- `handoffs/qa_plan_verify.md` (S0079 PENDING queue)
- `docs/engineering/state.md` (Sprint-plan checkpoint — this run)

### Next

- **`/plan-verify`** (fresh **qa** context) for **`S0079`** / **`BUG-0010`**.

### Decision gate

- **None** — sprint plan satisfied; bug **OPEN**.


---

## Intake handoff — US-0092 / cursor-20260606-US0092-intake

### Target

- `story_id=US-0092`
- `intake_run_id=cursor-20260606-US0092-intake`
- phase completed: **`intake`** (**`po`**)
- `next_scheduled_phase=discovery`
- `INTAKE_GUIDED_MODE=1`, `INTAKE_WORK_ITEM_KIND=story`

### Summary

- **Problem**: Downstream its-magic repos stop after every US/bug despite scratchpad auto flags (**US-0088** continuous `/auto` is often one Cursor turn + operator re-invoke). Operator wants **full autonomy**: build software, self-run UAT/manual steps (API/browser/tests), auto-resolve blocks until green, advance to next OPEN US/bug without waiting.
- **Operator constraint (hard)**: **`TOKEN_PROFILE`** must affect **token usage / context breadth only** — **not** automation level. Audit and fix any docs implying otherwise.
- **Proposed delivery**: opt-in **`AUTO_FLOW_MODE=full_autonomy`** (literal architecture-locked); shipped **stdlib outer-driver script**; expand **US-0065/66** self-verify for UAT; bounded block retry; drain-without-pause; default-off — **`auto_until_decision`** unchanged.
- **Decomposition**: single story (PO default); TL may split at architecture only with explicit authority.
- Status authority: **OPEN** in `docs/product/backlog.md` per **US-0045**; closure at `/release`.

### Plan areas (US-0081)

| plan_area_id | maps to |
|---|---|
| `full-autonomy-flow-mode` | US-0092 |
| `outer-driver-script` | US-0092 |
| `self-verify-uat-runtime` | US-0092 |
| `block-auto-resolve` | US-0092 |
| `drain-without-pause` | US-0092 |
| `token-profile-orthogonality` | US-0092 |
| `docs-tests-parity` | US-0092 |

### Risks (carry to /discovery)

- **R1**: Outer driver infinite loop without caps — mitigate with existing **`AUTO_LOOP_MAX_CYCLES`** / **`AUTO_BACKLOG_MAX_STORIES`** + driver exit codes.
- **R2**: Self-verify false PASS on unresolvable stacks — fail closed **`UAT_PROBE_UNRESOLVED`** (name TBD at architecture).
- **R3**: TOKEN_PROFILE doc drift reintroduced — AC-6 audit + contract tests.
- **R4**: Security — auto-remediation touching secrets or publish — hard deny-list + **`RELEASE_PUBLISH_MODE`** unchanged default.

### Intake evidence (US-0078 / DEC-0060)

- `selected_pack=first-intake-pack`
- `coverage_complete=true`
- Validator: `python scripts/intake_evidence_validate.py --file handoffs/intake_evidence/US-0092-intake-20260606.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**

### Evidence refs

- `docs/product/backlog.md` (`## US-0092`)
- `docs/product/acceptance.md` (portfolio row unchecked)
- `handoffs/intake_evidence/US-0092-intake-20260606.json`

### Next

- **`/discovery`** (fresh PO context) for **`US-0092`** — lock full_autonomy stop matrix vs **US-0088**, outer-driver invocation model, UAT probe catalog, TOKEN_PROFILE orthogonality audit scope. Research stub: **`R-0078`**.

---

## Orchestrated discovery handoff — US-0092 / auto-20260606-03

### Target

- `story_id=US-0092`
- `orchestrator_run_id=auto-20260606-03`
- phase completed: **`discovery`** (**`po`**)
- `next_scheduled_phase=research`
- `fresh_context_marker=po-US0092-discovery-20260606T183000Z-fresh`
- `decomposition=single_story` (PO default; per `US-0051`)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=3`

### Summary

- **Orchestration gap**: **US-0088** documents continuous `/auto` but Cursor often stops after one phase — operators manually re-invoke despite scratchpad auto flags. **US-0092** ships opt-in **`AUTO_FLOW_MODE=full_autonomy`** (default-off) with a **stdlib outer-driver script**, self-verify UAT/QA, bounded block auto-resolve, and drain-without-pause.
- **TOKEN_PROFILE orthogonality (hard)**: **`lean|balanced|full`** = context breadth / token cost **only** — not automation level, phase depth, drain, or driver invocation. AC-6 audit + contract tests required.
- **Six-step operator flow (discovery-locked)**: (1) enable full_autonomy + optional drain flags; (2) run outer driver once; (3) inner lifecycle + self-verify; (4) bounded block retry; (5) drain-without-pause advance; (6) deterministic stop on cap/gate/empty portfolio.
- **Spawn-only preserved**: **US-0048** / **BUG-0006** unchanged — driver loops invocations, not in-chat multi-role.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Acceptance pointers (discovery emphasis)

- **AC-1**: **`AUTO_FLOW_MODE=full_autonomy`** scratchpad key + interaction with **`PHASE_MODE`**, **`PERMISSION_MODE`**, drain/bug-queue, safety caps.
- **AC-2**: Shipped stdlib outer-driver under **`scripts/`** — not operator-manual-only.
- **AC-3**: Self-verify **`/verify-work`** + **`/qa`** — probe catalog, fail-closed on unresolvable stack.
- **AC-4**: Block auto-resolve with per-attempt ledger + caps.
- **AC-5**: Drain-without-pause + **DEC-0069** boundary refresh.
- **AC-6**: TOKEN_PROFILE orthogonality audit (grep + contract tests).
- **AC-7**: Stop matrix in **`auto.md`**, **`auto-orchestration-reference.md`**, **`architecture.md`** **`# US-0092`**.
- **AC-8–AC-9**: Contract tests + template parity.
- **AC-10**: Security deny-list (no `.env`, no intake mutation, no auto-publish).

### Top risks (carry to /research)

- **R1** Driver infinite loop — mitigate **`AUTO_LOOP_MAX_CYCLES`** / **`AUTO_BACKLOG_MAX_STORIES`** + exit codes.
- **R2** Self-verify false PASS — fail closed **`UAT_PROBE_UNRESOLVED`**.
- **R3** TOKEN_PROFILE doc drift — AC-6 audit + contract tests.
- **R4** Security (secrets/publish/intake) — hard deny-list + **`RELEASE_PUBLISH_MODE`** default.
- **R5** Partial delivery — single-story vertical contract prevents flags without driver.

### Research asks (extend **`R-0078`**)

1. Outer-driver invocation model — CLI vs Cursor hook vs **`/loop`**; argv/exit-code contract; runbook recipe.
2. Full_autonomy stop matrix — hard vs relaxable **US-0088** gates.
3. UAT probe catalog — acceptance → probe mapping; fail-closed reason codes; **US-0065/66** composition.
4. Block-retry ledger schema + **`AUTO_IMPLEMENTATION_LOOP`** cap interaction.
5. TOKEN_PROFILE orthogonality audit — grep scope + contract-test markers.
6. Contract-test + template parity inventory for touched surfaces.

### Evidence refs

- `docs/product/backlog.md` (`## US-0092` — discovery_notes appended)
- `docs/product/vision.md` (**Intake Notes — US-0092** + **Discovery Notes — US-0092**)
- `docs/product/acceptance.md` (`US-0092` row — unchecked)
- `handoffs/intake_evidence/US-0092-intake-20260606.json`
- `docs/engineering/research.md` (**`R-0078`** — discovery extension appended)
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/research`)
- Adjacent: **US-0088**, **US-0044**, **US-0065**, **US-0066**, **US-0080**, **US-0087**, **US-0048**, **US-0056**

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0092`** — deepen **`R-0078`**, lock stop matrix, outer-driver model, probe catalog, and TOKEN_PROFILE audit before **`/architecture`**.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

## Orchestrated research handoff — US-0092 / auto-20260606-03

### Target

- `story_id=US-0092`
- `orchestrator_run_id=auto-20260606-03`
- phase completed: **`research`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0092-research-20260606T190500Z-fresh`
- `next_scheduled_phase=architecture`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=3`

### Summary

- **`/research`** **PASS** — extended **`R-0078`** with Q1–Q6 resolution. **Outer driver**: stdlib **`scripts/auto_outer_driver.py`** (not manual-only, not **`/loop`**) with argv/exit-code contract and runbook recipe. **Stop matrix**: hard gates preserved; **`full_autonomy`** relaxes transient **`blocked`**/**`missing_input`** and UAT/QA fail under **`AUTO_IMPLEMENTATION_LOOP`**. **UAT probes**: catalog + fail-closed reason codes (**`UAT_PROBE_UNRESOLVED`**, etc.). **Block-retry ledger**: **`handoffs/auto_block_retry/<orchestrator_run_id>.jsonl`** with cap interaction (**`AUTO_LOOP_MAX_CYCLES`**, **`AUTO_IMPLEMENTATION_LOOP`**, **`AUTO_BLOCK_RETRY_MAX`**). **TOKEN_PROFILE audit**: grep scope + known runbook conflict flagged.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Key findings (architecture inputs)

1. **Outer driver (Q1)**: Option A stdlib script — polls **`resume_brief`**/**`state.md`**, re-invokes **`/auto`** hook; exit codes 0–6 + 124.
2. **Stop matrix (Q2)**: normative hard vs relaxable table in **`R-0078`**; **`RELEASE_PUBLISH_MODE=auto`** stays opt-in.
3. **UAT probes (Q3)**: seven probe kinds; shared resolver lib candidate **`scripts/uat_probe_lib.py`**.
4. **Ledger (Q4)**: JSONL schema + three-tier cap model.
5. **TOKEN_PROFILE (Q5)**: fix **`lowers default automation breadth`** in runbook active+template; contract-test markers.
6. **Parity (Q6)**: 9-row inventory for execute/template.

### Evidence refs

- `docs/engineering/research.md` (**`R-0078`** research extension)
- `docs/product/backlog.md` (`## US-0092` — `research_notes`)
- `docs/product/acceptance.md` (`US-0092` row — unchecked)
- `handoffs/intake_evidence/US-0092-intake-20260606.json`
- `docs/engineering/state.md` (Research checkpoint — this run)
- `handoffs/resume_brief.md` (architecture pointer)

### Architecture asks (companion DEC-xxxx)

1. Lock **`AUTO_FLOW_MODE=full_autonomy`** scratchpad contract + interaction matrix with drain/bug-queue/caps.
2. Author **`docs/engineering/architecture.md`** **`# US-0092`** with outer-driver contract, stop matrix, probe catalog, ledger schema.
3. Confirm script names, **`AUTO_BLOCK_RETRY_MAX`** default, and lib split (**`auto_outer_driver.py`** vs **`uat_probe_lib.py`**).

### Next

- **`/architecture`** (fresh **tech-lead** context) for **`US-0092`** — lock companion DEC + architecture section before **`/sprint-plan`**.

### Decision gate

- **None** — research satisfied; story **OPEN**.

