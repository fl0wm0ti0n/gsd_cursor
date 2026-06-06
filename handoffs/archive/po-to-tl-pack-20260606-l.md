# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 14
- First archived heading: `## Architecture Addendum — US-0090 (companion DEC authored; ready for `/sprint-plan`)`
- Last archived heading: `## Intake handoff — US-0091 / cursor-20260510-US0091-intake`
- Verification tuple (mandatory):
  - archived_body_lines=179
  - retained_body_lines=754

---

## Architecture Addendum — US-0090 (companion DEC authored; ready for `/sprint-plan`)

- **From**: **tech-lead** (**`/architecture`** phase for US-0090, `auto-20260418-01`, `fresh_context_marker=tl-US0090-architecture-20260418T220000Z-fresh`)
- **To**: **tech-lead** (fresh **`/sprint-plan`** subagent, next phase; **do not reuse this phase's context**). Parallel handoff at top of `handoffs/tl_to_dev.md` (`## TL -> Dev Handoff — US-0090 (post-architecture)`).
- **Binding decision**: **`DEC-0073`** (**composes on** **`DEC-0072`** via forward-link; does **NOT** rewrite `DEC-0072`). `§1`–`§11` map 1:1 to the eleven research-phase architecture-asks above.
- **Architecture section**: **`docs/engineering/architecture.md`** **`# US-0090`** appended (active-only — story-scoped architecture sections do not mirror to `template/`; DEC-0072 §7 row 6 precedent).
- **Research closure**: all eight deferred questions resolved (Q9 — safe-mode minifier only / aggressive deferred; Q10 — Option B parallel tree; Q11 — Option C hybrid; Q12 — Option C hybrid with frozen `docs-prose-only` profile; Q15 — 9-code vocab grouped in three families; Q16 — three parallel sentences extending DEC-0072 §1 in place; Q17 — 8-row parity inventory + rule-subsection decided **NO** in v1; Q19 — manifest entry + extend existing parity script + extend existing completeness test). Three concrete questions (Q13/Q14/Q18) ratified verbatim. Four risks (R8/R9/R10/R11) resolved by architectural means.

### Atomic task seeds (one per AC; `/sprint-plan` converts to `T-xxx` and may split/group)

| # | Seed | AC | DEC-0073 § | Active surface(s) | Template surface(s) |
|---|------|----|-----------|-------------------|---------------------|
| 1 | **`scripts/caveman_compress_input.py`** — implement CLI (`--dry-run` default, `--write`, `--verify-originals`, `--report`), activation gate (§2), deny-list layered eval (§4), allow-list grammar (§5), safe-mode minifier (§6), reason-code emission (§7), atomic sidecar write order (§3). Stdlib Python only. | AC-1, AC-2, AC-3, AC-4, AC-5 (CLI) | §2, §3, §4, §5, §6, §7, §8 | `scripts/caveman_compress_input.py` | `template/scripts/caveman_compress_input.py` (byte-identical) |
| 2 | **Runbook subsection** — `### Caveman input compression (US-0090)` with 3-step dry-run → verify → write procedure, deny summary, `.cursorignore` operator-owned note, sidecar explanation. | AC-5, AC-7 | §1 three-sentence paragraph + §9 row 2 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` |
| 3 | **Three-axis non-substitution paragraph** — replace DEC-0072 §1 paragraph with three parallel sentences (`TOKEN_PROFILE` / `CAVEMAN_MODE` / `CAVEMAN_COMPRESS_INPUT`). | AC-7 | §1 + §9 row 3 | `docs/engineering/auto-orchestration-reference.md` | `template/docs/engineering/auto-orchestration-reference.md` |
| 4 | **Sidecar tree anchor** — `docs/.caveman-originals/.gitkeep` (new; empty file) + repo-root `.gitignore` anchor `docs/.caveman-originals/`. | AC-2 | §3 + §9 rows 7 & 8 | `.gitignore`, `docs/.caveman-originals/.gitkeep` | n/a (installer does not own repo `.gitignore`; sidecar root is repo-local state) |
| 5 | **Contract-test extension** — extend `tests/auto_command_contract_test.py` in place with `test_caveman_compress_input_*` prefix. **Must not** modify existing `test_caveman_default_off_*` subtests (DEC-0072 §6 row 6 invariant). | AC-6 | §9 test strategy | `tests/auto_command_contract_test.py` | n/a (tests do not mirror) |
| 6 | **Fixture directory** — `tests/fixtures/caveman_compress/` with 8 fixture classes (whitespace / literal-region / deny-list / scope / idempotency / mode-disabled / original-missing / flag-conflict). | AC-6 | §9 test strategy classes 1–8 | `tests/fixtures/caveman_compress/` | n/a |
| 7 | **Rule byte-identity guard + deny-list version guard** — add two subtests under (5): (a) SHA-256 equality of `.cursor/rules/caveman.mdc` active vs `template/`; (b) stable `--report deny_list_version` hash. | AC-6, AC-8 | §9 test strategy + §4.2 | `tests/auto_command_contract_test.py` (same file as seed 5) | n/a |
| 8 | **Installer manifest entry** — add `template/scripts/caveman_compress_input.py` under `install_include_paths` (active + `template/`). | AC-8 | §10 | `docs/engineering/context/installer-owned-paths.manifest` | `template/docs/engineering/context/installer-owned-paths.manifest` |
| 9 | **Parity-test extension** — extend `scripts/check_intake_template_parity.py` with `--scope=caveman-compress` mode asserting script byte-identity. | AC-8 | §10 Option A | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` |
| 10 | **Install-completeness fixture extension** — extend `tests/installer_completeness_bug0003_test.py` to verify `--mode missing` + `--mode upgrade` deliver `template/scripts/caveman_compress_input.py` across all three installer entrypoints (`installer.sh`, `installer.ps1`, `installer.py`). Add new `run-tests` section (candidate `§26S`; sprint-plan locks exact number) in `tests/run-tests.ps1` + `tests/run-tests.sh`. | AC-8, AC-6 | §10 Option A + §9 test strategy | `tests/installer_completeness_bug0003_test.py`, `tests/run-tests.ps1`, `tests/run-tests.sh` | n/a (tests + harness active-only) |
| 11 | **Architecture section linkage check** — assert-only task verifying `docs/engineering/architecture.md` **`# US-0090`** references `# US-0089`, US-0053, US-0085, US-0078 / DEC-0060 and enumerates forbidden surfaces. No rewrite. | AC-7 | §9 row 4 | `docs/engineering/architecture.md` (read-only check) | n/a |

**Task count**: 11 candidate seeds. `SPRINT_MAX_TASKS=12` (default). Sprint-plan may group seeds 5 & 7 (same test file) and/or 1 & 4 (one commit pair) to land at `T-001..T-009` or `T-001..T-010`. `SPRINT_AUTO_SPLIT` NOT expected to trigger.

### Test surfaces (no implementation here; sprint-plan + execute own code)

- **`tests/auto_command_contract_test.py`** — extend **in place** with `test_caveman_compress_input_*` subtests (mandatory). Existing `test_caveman_default_off_*` UNCHANGED byte-for-byte (DEC-0072 §6 row 6 invariant).
- **`tests/fixtures/caveman_compress/`** — 8 fixture classes (see DEC-0073 §9).
- **`tests/installer_completeness_bug0003_test.py`** — extend with caveman-script delivery assertion (R11; non-negotiable).
- **`tests/run-tests.ps1` + `tests/run-tests.sh`** — new section (candidate `§26S`; sprint-plan locks).
- **No new pytest module** in v1 (follow DEC-0072 / US-0089 precedent — in-place extension).

### Template parity touchpoints (8-row positive + 4-class negative)

**Positive parity (active + `template/` byte-identical)**:

1. `scripts/caveman_compress_input.py` ↔ `template/scripts/caveman_compress_input.py`
2. `docs/engineering/runbook.md` ↔ `template/docs/engineering/runbook.md` (caveman-compression subsection)
3. `docs/engineering/auto-orchestration-reference.md` ↔ `template/docs/engineering/auto-orchestration-reference.md` (three-sentence paragraph)
4. `docs/engineering/context/installer-owned-paths.manifest` ↔ `template/docs/engineering/context/installer-owned-paths.manifest` (caveman script entry)
5. `scripts/check_intake_template_parity.py` ↔ `template/scripts/check_intake_template_parity.py` (scope extension)

**Active-only (no mirror; per DEC-0072 §7 precedent)**:

6. `docs/engineering/architecture.md` `# US-0090` section
7. `tests/auto_command_contract_test.py` + `tests/fixtures/caveman_compress/`
8. `.gitignore` + `docs/.caveman-originals/.gitkeep`

**NEGATIVE parity (MUST NOT be edited in v1)**:

- `.cursor/rules/caveman.mdc` + `template/.cursor/rules/caveman.mdc` (SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` preserved; rule byte-identity guard subtest enforces).
- `.cursor/scratchpad.md`, `.cursor/scratchpad.local.example.md`, `template/.cursor/scratchpad.local.example.md` (key byte-strings from DEC-0072 §3 preserved; semantics activate without rename).
- `.cursor/skills/its-magic/SKILL.md` + mirror (DEC-0072 §7 row 9 preserved).
- `.cursorignore` (operator-owned per US-0085 / DEC-0071).
- All canonical-artifact / contract-surface files listed in DEC-0073 §4.1.

### Release / verify gates

- **`/plan-verify`**: AC-1..AC-8 ↔ `T-xxx` 1:1 bijection; governance anchors verified (`DEC-0073`, `DEC-0072` composition, `# US-0090`, `R-0073`).
- **`/execute`**: dev MUST commit active + `template/` pairs atomically for parity rows 1–5; MUST NOT edit any NEGATIVE-parity file; MUST keep `test_caveman_default_off_*` byte-unchanged.
- **`/qa`**: canonical `tests/run-tests.ps1` (+ `run-tests.sh`) green for the new `§26S` + all existing sections; targeted pytest — all `test_caveman_compress_input_*` + `test_caveman_default_off_*` pass; `bug_issue_validate.py` `[BUG_VALIDATION_OK]`; rule byte-identity guard green; deny-list version guard green; install-completeness fixture green for `--mode missing` + `--mode upgrade` across all three entrypoints.
- **`/verify-work`**: UAT 8/8 on AC-1..AC-8; isolation evidence + strict-proof tuples present for every phase in `docs/engineering/state.md`; `handoffs/release_queue.md` → `ready`.
- **`/release`**: flip backlog `OPEN` → `DONE`; check AC-1..AC-8 in `docs/product/backlog.md` + portfolio row in `docs/product/acceptance.md`; author `sprints/SXXXX/release-findings.md` + `handoffs/releases/SXXXX-release-notes.md`; release-queue `ready` → `released`; publish mode: per existing `RELEASE_PUBLISH_MODE` operator default (no new publish flag).

### Risks carried (architecture-resolved; sprint-plan should preserve mitigations)

- **R8** — filler-word drift → neutralized in v1 by **deferring aggressive mode** (DEC-0073 §6). Sprint-plan must NOT reopen.
- **R9** — reason-code proliferation → locked 9-code set grouped into three families (DEC-0073 §7). Sprint-plan must NOT add codes.
- **R10** — rule-subsection byte-identity → **no rule edit in v1** (DEC-0073 §9 NEGATIVE parity). Sprint-plan must NOT seed a rule-subsection task. Byte-identity guard subtest (seed 7) is a hard requirement.
- **R11** — install-completeness omission (BUG-0003 class) → install-completeness fixture extension (seed 10) is **non-negotiable**. Sprint-plan MUST seed it regardless of sprint-size pressure. `/release` MUST NOT ship without it.

### Scope guards for `/sprint-plan` (non-negotiables; do not cross)

- **Do not re-open** any architecture-locked decision in DEC-0073 §§1–11.
- **Do not rewrite** `DEC-0072` or `DEC-0073`. Sprint-plan authors `sprints/SXXXX/*`, not DECs.
- **Do not edit** `.cursor/rules/caveman.mdc` (byte-identity preserved — seed 7 guard asserts).
- **Do not add** new reason codes, new CLI flags (e.g. `--mode`, `--purge-orphans`), new profiles, new fixture classes beyond §9, or new deny-list entries without a subsequent DEC.
- **Do not change** `TOKEN_PROFILE` / `CAVEMAN_MODE` / strict-proof (DEC-0038) / isolation-evidence (DEC-0029) / `AUTO_QUIET` (US-0088) / US-0071 contracts.
- **Do not advance** backlog status. US-0090 stays **OPEN** per **US-0045** (closure at `/release`).
- **Do not seed tasks** outside the 11 seeds above without explicit justification tied to a specific AC.

### Mandatory `/sprint-plan` deliverables (next phase)

1. `sprints/SXXXX/sprint.md` with summary, AC table, locked DEC anchors (`DEC-0073` + `DEC-0072` composition), research anchor (`R-0073`), success gate.
2. `sprints/SXXXX/tasks.md` with `T-001..T-Nxx` atomic tasks + AC map + DEC-0073 § locks per row.
3. `sprints/SXXXX/plan-verify.json` `status=PENDING`, `reason=AWAITING_QA_PLAN_VERIFY`.
4. Empty-stub scaffold: `sprints/SXXXX/summary.md`, `sprints/SXXXX/qa-findings.md`, `sprints/SXXXX/uat.json`, `sprints/SXXXX/uat.md`, `sprints/SXXXX/release-findings.md`.
5. `handoffs/tl_to_dev.md` sprint-plan stanza prepended; prior architecture stanza preserved as lineage.
6. `handoffs/qa_plan_verify.md` QA entrypoint pointer.
7. `handoffs/resume_brief.md` new top pointer post-`/sprint-plan`; intended_resume_phase=`plan-verify`.
8. `docs/engineering/state.md` Sprint-plan checkpoint (isolation + strict proof + phase boundary block + AC-10 compact line + `[BUG_VALIDATION_OK]`).
9. `docs/product/backlog.md` **`## US-0090`** `sprint_plan_notes` appended (US-0090 remains **OPEN** per **US-0045**).

### Artifact refs (architecture phase materializations)

- `decisions/DEC-0073.md` (new; composes on `DEC-0072`).
- `docs/engineering/decisions.md` — `## Current context pack` header refreshed + `DEC-0073` entry appended to "Compact decision index".
- `docs/engineering/architecture.md` `# US-0090` (new section appended at bottom).
- `docs/product/backlog.md` `## US-0090` `architecture_notes (2026-04-18, TL, auto-20260418-01)` appended.
- `docs/engineering/state.md` — Architecture checkpoint (2026-04-18) — US-0090 / `auto-20260418-01` (isolation + strict proof + phase boundary block + AC-10 line).
- `handoffs/tl_to_dev.md` — **US-0090 architecture** stanza prepended at top; prior US-0089 stanza preserved.
- `handoffs/resume_brief.md` — new top pointer post-`/architecture` US-0090 (prior post-`/research` US-0090 pointer marked superseded).
- `handoffs/po_to_tl.md` — this `## Architecture Addendum — US-0090` section appended.

### Next phase

- **`/sprint-plan`** (fresh **tech-lead**) for **US-0090** — seed `sprints/SXXXX/*` from the 11 task seeds above + the AC ↔ § map.
- **Decision-gate posture**: **none** expected — architecture phase IS the decision gate; sprint-plan translates decisions into atomic tasks.
- **Status authority**: **US-0090** stays **OPEN** per **US-0045**. No acceptance rows checked by architecture.

---

## Intake handoff — US-0091 / cursor-20260510-US0091-intake

### Target

- `story_id=US-0091`
- `intake_run_id=cursor-20260510-US0091-intake`
- phase completed: **`intake`** (**`po`**)
- `next_scheduled_phase=discovery`
- `decomposition=single_story` (operator explicit; per `US-0051`)
- `priority=P1`
- `INTAKE_GUIDED_MODE=1`, `INTAKE_WORK_ITEM_KIND=story`, `INTAKE_SUBAGENT_FALLBACK=deny`

### Summary

- One-time audit of `README.md` against `docs/product/backlog.md` + `docs/product/acceptance.md` to identify and backfill **user-visible** feature descriptions (commands, flags, operator-affecting bug fixes), then ship a **blocking** release-gate extension so feature coverage cannot drift again.
- Three target files keep audience semantics (`DEC-0059`) and template parity (`US-0017`):
  - root `README.md` — `USER_*` H2 blurbs (operator audience),
  - `template/README.md` — byte parity with active root,
  - `docs/developer/README.md` — `DEV_*` H2 rows linking each feature to its US/DEC and scratchpad flags.
- Composition (no rewrites):
  - **`US-0030`** (DONE) provides the existing release doc-delta gate (delta-driven). `US-0091` adds a **second check** for static-coverage gaps inside the same gate surface and shares remediation vocabulary.
  - **`US-0077`** / `DEC-0059` (DONE) provide the audience profile contract. `US-0091` populates it for currently undocumented user-visible features without inventing new H2s.
  - **`US-0017`** template-drift guard absorbs new validator parity touchpoints.
  - **`US-0071`** wording sanitization remains in force on backfilled blurbs.
- Operator-confirmed scope (AskQuestion 2026-05-10): `scope_files=both` (root + template), `audience_focus=both_profiles` (USER_* + DEV_*), `feature_set=user_visible` (skip pure-internal guards / refactors), `drift_guard=blocking`, `story_split=single`, `priority=P1`.
- Status authority: **OPEN** in `docs/product/backlog.md` per `US-0045`; closure flips at `/release`.

### Risks (carry to /discovery and /research)

- **False positives** if the user-visible feature predicate is not bounded deterministically (would block `/release` retroactively) — mitigation: per-story `user_visible` marker authored explicitly; ambiguous inputs fail closed with `README_FEATURE_COVERAGE_INPUT_INVALID`.
- **README bloat** if 90+ stories all backfill simultaneously across both audience profiles — mitigation: short blurbs (1-2 sentences) bounded by existing `validate_doc_profile.py` section budgets per audience cell.
- **Three-file parity drift** (root + `template/` + `docs/developer/README.md`) — mitigation: extend or compose with existing `US-0017` template-drift guard + `scripts/check_intake_template_parity.py`; do not duplicate parity logic.
- **Retroactive release lock-in** when the new blocking gate ships before the backfill is complete — mitigation: same-sprint delivery + grandfathering / migration policy locked in the new architecture decision (`AC-10`).

### Adaptive questioning evidence (US-0051)

- 6-question `AskQuestion` round (single round, bounded): `scope_files`, `audience_focus`, `feature_set`, `drift_guard`, `story_split`, `priority`.
- Each question presented options/alternatives before recommendation; user authority preserved (`US-0021`).
- Decomposition evaluator → single story (operator explicit; consistent with bounded-refinement breadth/risk score).

### Intake evidence (US-0078 / DEC-0060)

- `selected_pack=small-intake-pack`
- `asked_topics=outcome_success_criteria, impacted_components, constraints_compatibility_risks, required_tests_acceptance_checks, done_definition`
- `missing_topics=[]`
- `assumptions_confirmed=(none)`
- Validator: `python scripts/intake_evidence_validate.py --file handoffs/intake_evidence/US-0091-intake-20260510.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**.
- Truthfulness: each `topic_coverage` row carries a distinct `quoted_user_text` derived from the operator's AskQuestion answers — no shared blob across topic keys (per `BUG-0007` / `R-0066`).

### Evidence refs

- `docs/product/backlog.md` (`## US-0091` block — full acceptance criteria, decomposition, overlap evaluation, intake notes)
- `docs/product/acceptance.md` (`US-0091` row — unchecked)
- `handoffs/intake_evidence/US-0091-intake-20260510.json` (canonical `ie:` refs per `DEC-0060`)
- `docs/engineering/research.md` (`## R-0074` — intake-time research; per `DEC-0011` / `EARLY_RESEARCH=1`)
- Adjacent governance: `US-0030` (release doc-delta gate), `US-0077` / `DEC-0059` (dual-README audience), `US-0017` (template-drift parity), `US-0071` (user-visible metadata sanitization), `DEC-0040` (artifact ordering)

### Next

- **`/discovery`** (fresh PO context) for `US-0091` — lock the user-visible feature predicate, the per-story `user_visible` marker location (acceptance row vs backlog block field), and section-budget posture per audience profile cell.
- Deferred to `/research` (tech-lead): validator placement and CLI grammar (candidate `scripts/validate_readme_feature_coverage.py`), reason-code vocabulary lock, release-gate wiring point (active + `template/`), grandfathering / migration options.
- Deferred to `/architecture` (tech-lead): companion `DEC-xxxx` composing on `DEC-0030` + `DEC-0059`; final template parity inventory; first-activation policy.

---

