## Orchestrated research handoff — US-0094 / auto-20260607-01

### Target

- `story_id=US-0094`
- `orchestrator_run_id=auto-20260607-01`
- phase completed: **`research`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0094-research-20260607T123000Z-fresh`
- `next_scheduled_phase=architecture`
- `decomposition=single_story` (per `US-0051`)
- `priority=P1`

### Summary

- **`/research`** **PASS** — extended **`R-0080`** with Q1–Q4 resolution. **Pillar-catalog map** locked for teaser cross-links only (P1→Commands/auto; P2→Commands+Features; P3→Features distribution; P4→Other useful capabilities). **Intro budget** for `both`×`balanced`: 3 paragraphs, 120–210 words soft / 240 hard max; discovery draft = 129 words. **DEC-0074**: no §intro amendment — vision/backlog/discovery locks suffice. **Diataxis tiers**: explanation=intro, summary=pillars, reference=catalog, how-to/tutorial=Setup/How-to/walkthroughs preserved.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Key findings (architecture inputs)

1. **Pillar map (Q1)**: thematic affinity table in **`R-0080`** — structural homes immutable per **`readme-section-affinity.json`**; catalog blocks stay in Features / Commands / Other useful capabilities.
2. **Intro budget (Q2)**: pre-H2 prose not in `validate_doc_profile.py`; hard caps 80 words/¶, 240 total; 4×`###` pillars only — no new H2.
3. **DEC-0074 (Q3)**: coverage validator orthogonal to narrative IA — document in **`# US-0094`** architecture; optional **`DEC-xxxx`** only if formal IA lock desired.
4. **Diataxis (Q4)**: pillar teasers id-free; catalog encyclopedic; Setup/How-to procedural depth unchanged.

### Evidence refs

- `docs/engineering/research.md` (**`R-0080`** research extension)
- `docs/product/backlog.md` (`## US-0094` — `research_notes`)
- `docs/product/vision.md` (**Discovery Notes — US-0094**)
- `handoffs/intake_evidence/US-0094-intake-20260607.json`
- `docs/engineering/state.md` (Research checkpoint — this run)
- `handoffs/resume_brief.md` (architecture pointer)
- Adjacent: **US-0091**, **DEC-0074**, **DEC-0059**, **US-0092**, **US-0017**, **R-0054**

### Architecture asks

1. Author **`docs/engineering/architecture.md`** **`# US-0094`** with intro/pillar contract, Q1 affinity table, Q2 budget literals, Diataxis tier map.
2. Confirm whether companion **`DEC-xxxx`** is needed for IA formalization or discovery locks alone suffice (research recommends locks + architecture section only).
3. Lock execute guards: single-source README edit → byte-copy template; post-edit **`validate_readme_feature_coverage.py --report`** + **`validate_doc_profile.py`**.

### Next

- **`/architecture`** (fresh **tech-lead** context) for **`US-0094`** — lock architecture section before **`/sprint-plan`**.

### Decision gate

- **None** — research satisfied; story **OPEN**.

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

---

## Intake handoff — US-0094 / cursor-20260607-US0094-intake

### Target

- `story_id=US-0094`
- `intake_run_id=cursor-20260607-US0094-intake`
- `selected_pack=small-intake-pack`
- `INTAKE_GUIDED_MODE=1`
- `next_scheduled_phase=discovery`

### Summary

- **`/intake`** **PASS** — operator wants the README opening rewritten so **its-magic** leads with the autonomous **AI dev team** story: **you are the customer/dreamer**; the framework runs intake → release with artifact-first memory and optional **full autonomy** (**US-0092**). Re-audit all user-visible **US/BUG** coverage (**US-0091**), reorganize as **framework purpose → main features → sub-features → existing detail sections**, and keep **`README.md`** === **`template/README.md`** (byte-identical).
- **Baseline (intake audit)**: `validate_readme_feature_coverage.py --report` already **`coverage_missing=[]`** (104 items); root/template README already byte-identical — delivery is narrative hierarchy, not net-new catalog entries.
- **Decomposition**: single story (intro + hierarchy + parity + coverage survival are one contract).
- **Status**: **OPEN** per **US-0045**.

### Scope boundaries

| In scope | Out of scope |
|----------|----------------|
| Root + `template/README.md` intro/hierarchy | Rewriting **US-0091** validator |
| Re-run coverage audit post-edit | Replacing **DEC-0059** profiles |
| Foreground **US-0092** in intro | Regenerating **docs/developer/README.md** body |
| Preserve all deep sections below new tiers | Per-feature user guides (**US-0032**) |

### Acceptance sketch (10 ACs)

1. Framework-purpose lead (dreamer + AI team + artifacts + full autonomy headline).
2. Main-feature pillars then sub-feature groupings before detail body.
3. No silent deletion of existing operator detail sections.
4. `validate_readme_feature_coverage.py` → zero gaps.
5. Root/template byte parity (**US-0017**).
6. **DEC-0059** USER_* H2 + `validate_doc_profile.py` budgets.
7. **US-0071** metadata guard.
8. Full-autonomy operator messaging (**US-0092**).
9. Regression guards (**US-0017**, readme coverage tests).
10. DEV shard unchanged (optional cross-link only).

### Intake evidence

- `handoffs/intake_evidence/US-0094-intake-20260607.json`
- `python scripts/intake_evidence_validate.py --file handoffs/intake_evidence/US-0094-intake-20260607.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**
- `asked_topics`: all 5 `small-intake-pack` keys; `missing_topics=[]`

### Research anchor

- **`R-0080`** (intake stub) — narrative lead pattern, pillar grouping, coverage-safe moves, parity workflow.

### Risks for discovery

1. **R1** — Intro bloat violates **DEC-0059** section budgets → mitigate with concise lead + `###` sub-tiers.
2. **R2** — Restructure drops **US-0091** anchors → mitigate with post-edit `--report` gate in AC-4.
3. **R3** — Active/template drift during edit → mitigate with single-source edit + byte compare in AC-5.
4. **R4** — Overclaiming autonomy vs default-off scratchpad → mitigate with explicit opt-in language (**US-0092**).

### Evidence refs

- `docs/product/backlog.md` (`## US-0094`)
- `docs/product/acceptance.md` (US-0094 row — unchecked)
- `docs/product/vision.md` (**Intake Notes — US-0094**)
- `docs/engineering/research.md` (**R-0080**)
- `README.md` / `template/README.md` (current parity baseline)

### Next

- **`/discovery`** (fresh **po** context) for **US-0094** — lock pillar names, intro outline, and coverage-safe section moves before **`/research`**.

### Decision gate

- **None** at intake.

---

## Orchestrated discovery handoff — US-0094 / auto-20260607-01

### Target

- `story_id=US-0094`
- `orchestrator_run_id=auto-20260607-01`
- `intake_run_id=cursor-20260607-US0094-intake`
- `fresh_context_marker=po-US0094-discovery-20260607T120000Z-fresh`
- `next_scheduled_phase=research`
- `backlog_drain_active=false`

### Summary

- **`/discovery`** **PASS** — README information architecture locked for execute: **3 visionary paragraphs** before `## Features`, **four main-feature pillars** as `###` under existing `## Features (what its-magic can do)`, **three US-0091 catalog blocks** preserved in affinity-home H2 sections, all deep body sections unchanged below. **Full autonomy (**US-0092**)** foregrounded in intro ¶3 + Autonomous AI workflow pillar — default-off opt-in language mandatory.
- **Baseline**: `validate_readme_feature_coverage.py --report` → **`coverage_missing=[]`**, **`coverage_total=104`**; `README.md` === `template/README.md` (byte-identical pre-edit).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (execute inputs)

| Lock | Decision |
|------|----------|
| Intro | 3 paragraphs: dreamer+team → artifact-first workflow → full autonomy opt-in (**US-0092**) |
| Pillars (`###` under Features only) | Autonomous AI workflow · Quality & verification gates · Distribution & install · Operator control & ergonomics |
| Catalog | Keep 3 `### Feature coverage catalog (US-0091)` blocks in current parent H2s; no cross-H2 moves |
| H2 policy | No new `USER_*` H2 literals (**DEC-0059**); 13 existing H2 layout preserved |
| Parity | Single-source edit → byte-copy to `template/README.md` (**US-0017**) |
| Full autonomy | Intro ¶3 + pillar 1 bullet + catalog line — not appendix-only |

### Acceptance pointers (discovery emphasis)

- **AC-1**: Intro paragraphs before/with Features lead — dreamer, AI team, artifacts, phased workflow, full autonomy headline.
- **AC-2**: Four pillars + teaser sub-features; no duplicate encyclopedic catalog prose.
- **AC-3**: Setup through Contributing body preserved in substance.
- **AC-4**: Post-edit `validate_readme_feature_coverage.py --report` → zero gaps.
- **AC-5–AC-7**: Byte parity, doc profile budgets, metadata guard.
- **AC-8**: Full-autonomy operator language in intro/pillar tier.
- **AC-9–AC-10**: Regression guards; DEV shard optional cross-link only.

### Top risks (carry to /research)

- **R1** Pillar/catalog duplication — teaser bullets only.
- **R2** Affinity break on catalog relocation — cross-H2 moves forbidden.
- **R3** Intro length vs **DEC-0059** budgets — 3-paragraph cap.
- **R4** Active/template drift — single-source + byte compare.
- **R5** Autonomy overclaim — default-off / opt-in pairing (**DEC-0078**).

### Research asks (extend **`R-0080`**)

1. Pillar-to-catalog affinity map table (which catalog items thematically align to each pillar for optional cross-links only — not moves).
2. Intro word-count / line budget for `both`×`balanced` profile cell.
3. Whether **DEC-0074** needs companion §intro hierarchy lock or vision/backlog locks suffice.
4. Diataxis tier boundary examples (what stays in pillars vs what stays in Setup/How-to).

### Evidence refs

- `docs/product/backlog.md` (`## US-0094` — `discovery_notes` appended)
- `docs/product/vision.md` (**Discovery Notes — US-0094**)
- `docs/product/acceptance.md` (`US-0094` row — unchecked)
- `handoffs/intake_evidence/US-0094-intake-20260607.json`
- `docs/engineering/research.md` (**`R-0080`** — discovery extension appended)
- `README.md` / `template/README.md` (pre-edit parity baseline)
- `docs/engineering/context/readme-section-affinity.json` (affinity resolver)
- Adjacent: **US-0091**, **US-0077**, **US-0017**, **US-0092**, **US-0071**, **DEC-0059**, **DEC-0074**

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0094`** — deepen **`R-0080`**, finalize pillar-catalog map and intro budget before **`/architecture`** (if hierarchy DEC amendment needed).

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

