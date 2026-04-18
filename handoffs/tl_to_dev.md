## Sprint Plan — **S0076** / **US-0090** — post-**`/sprint-plan`** -> **`/plan-verify`** (**qa**)

> **2026-04-18T22:30:00Z** — **`/sprint-plan`** authored in fresh **tech-lead** context (`orchestrator_run_id=auto-20260418-01`, `fresh_context_marker=tl-US0090-sprint-plan-20260418T223000Z-fresh`, `runtime_proof_id=rp-auto-20260418-01-sprint-plan-tech-lead-20260418T223000Z-US0090`, `proof_hash=df27d039db0eb77e35ae140483338045c8a5a980f866b68ff683aa80bc3e8197`). Sprint **`S0076`** created; binding decision **`DEC-0073`** (composes on **`DEC-0072`** — forward-link, no rewrite). Task count **10 / 12** (`within_limit=true`; `SPRINT_AUTO_SPLIT` not triggered); AC coverage **AC-1..AC-8 all >=1 task** (no `PLAN_AC_COVERAGE_GAP`). Story **`US-0090`** remains **OPEN** (**US-0045**). No execution started yet — next phase is **`/plan-verify`** (fresh **qa**) -> then **`/execute`** (fresh **dev**).

### Sprint anchor

- **Sprint overview**: `sprints/S0076/sprint.md`
- **Atomic tasks**: `sprints/S0076/tasks.md` (T-001..T-010)
- **Plan-verify (qa)**: `sprints/S0076/plan-verify.json` (`status=PENDING`; flip to `PASS` at `/plan-verify`)
- **Summary stub**: `sprints/S0076/summary.md`
- **Binding decision**: `decisions/DEC-0073.md` (§1–§11)
- **Substrate decision (unchanged; forward-linked)**: `decisions/DEC-0072.md`
- **Architecture**: `docs/engineering/architecture.md` **`# US-0090`** (active-only per DEC-0072 §7 row 6 precedent)
- **Research**: `docs/engineering/research.md` **`R-0073`** (shared anchor; Q9–Q19 resolution pass 2026-04-18)
- **State checkpoint**: `docs/engineering/state.md` — **Sprint-plan checkpoint (2026-04-18) — US-0090 / S0076 / `auto-20260418-01`**

### Task → AC → DEC-0073 § mapping (locked)

| Task | AC | Summary | DEC-0073 § | Parity |
|------|----|---------|------------|--------|
| T-001 | AC-1..AC-5 | `scripts/caveman_compress_input.py` (+ `template/`) — CLI binary hosting gating / sidecar atomic-write ordering / deny eval / allow grammar / safe-mode algorithm / 9-code reason vocab | §2, §3, §4 + §4.1, §5 + §5.1, §6, §7, §8 | Positive (row 1) |
| T-002 | AC-5 | `docs/engineering/runbook.md` (+ `template/`) — Caveman input compression subsection (3-step operator flow + revert + three-axis reminder + `.cursorignore` operator-owned note) | §8, §9 row 2 | Positive (row 2) |
| T-003 | AC-7 | `docs/engineering/auto-orchestration-reference.md` (+ `template/`) — replace 2-sentence paragraph with 3-sentence three-axis non-substitution paragraph | §1, §9 row 3 | Positive (row 3) |
| T-004 | AC-2 | `.gitignore` anchor + `docs/.caveman-originals/.gitkeep` | §3 | Active-only |
| T-005 | AC-6, AC-8 | `tests/auto_command_contract_test.py` — new `test_caveman_compress_input_*` subtest class (11 assertions; includes seed-7 rule byte-identity R10 guard + deny_list_version drift guard; preserves existing `test_caveman_default_off_*` byte-unchanged) | §6, §7, §9 row 1 + negative-parity | Active-only |
| T-006 | AC-6 | `tests/fixtures/caveman_compress/` — 8 fixture classes (whitespace baseline / literal-region 9 zones / deny-list / scope violation / idempotency / mode-disabled / original-missing / flag-conflict) | §9 test-strategy block | Active-only |
| T-007 | AC-8 | `docs/engineering/context/installer-owned-paths.manifest` (+ `template/`) — add `scripts/caveman_compress_input.py` row | §10, §9 row 8 | Positive (row 8) |
| T-008 | AC-8 | `scripts/check_intake_template_parity.py` (+ `template/`) — new `--scope=caveman-compress` mode | §9 row 9 | Positive (row 9) |
| T-009 | AC-6, AC-8 | `tests/installer_completeness_bug0003_test.py` extension + `tests/run-tests.ps1` / `tests/run-tests.sh` new section (candidate §26S; lock during /execute) | §10 | Active-only |
| T-010 | AC-7 | Architecture `# US-0090` linkage assert-only subtest (no rewrite) | §1, §11 + DEC-0072 §7 row 6 | Active-only |

### Multi-AC task justification (Architecture Addendum-anchored)

- **T-001 → AC-1..AC-5**: Architecture Addendum seed #1 — "script is the CLI contract; five ACs land inside one binary by design" (gating / sidecar ordering / deny eval / allow grammar / CLI contract all implemented in `scripts/caveman_compress_input.py`).
- **T-005 → AC-6 + AC-8**: Addendum seeds 5 + 7 grouped — "same test file; grouping to minimize test-file churn while keeping rule byte-identity (R10) and deny-list version (§4.2) drift-detection guards in the same subtest class".
- **T-009 → AC-6 + AC-8**: Addendum seed 10 — "tests live under AC-6; installer / harness surface is AC-8 — single fixture + harness row lands both".

### Dev entry conditions (blocking; enforced by `/plan-verify`)

- `/plan-verify` must flip `sprints/S0076/plan-verify.json` `status` from **`PENDING`** → **`PASS`** before `/execute`.
- Fresh **dev** context required (US-0048 / DEC-0029 isolation); strict runtime proof (DEC-0038) at `/execute` entry and exit.
- Dev MUST edit active + `template/` in the same commit for parity rows 1 / 2 / 3 / 8 / 9 of DEC-0073 §9.
- Dev MUST NOT edit `.cursor/rules/caveman.mdc` or its `template/` counterpart (**negative parity; R10 byte-identity**). Baseline SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` preserved.
- Dev MUST NOT modify `test_caveman_default_off_*` subtests (DEC-0072 §6 row 6 invariant — additions only in `test_caveman_compress_input_*`).
- Dev MUST NOT add new reason codes, new CLI flags (no `--mode`, no `--purge-orphans`), new allow-list profiles, or new fixture classes beyond `DEC-0073` §9 without a subsequent DEC.
- Dev MUST NOT author / reference `npx skills add` anywhere (DEC-0072 §8 carried).
- Dev MUST NOT mutate `.cursorignore` (operator-owned per US-0085 / DEC-0071); script only reads it as optional overlay.
- Dev MUST NOT rewrite / edit `.cursor/scratchpad*` files — `CAVEMAN_COMPRESS_INPUT` and `CAVEMAN_FILE_SCOPE` already exist as reserved no-ops (DEC-0072 §3); activation is semantic (script reads them), not a byte change.

### File-by-file plan (ordering for /execute; pre-implementation gotchas)

Recommended implementation order (smallest blast radius first → highest leverage):

1. **T-004** — anchor the sidecar tree (`.gitignore` + `.gitkeep`) before any script can write sidecars. Cheap, unblocks T-001 acceptance test.
2. **T-001** — author the CLI binary (active + `template/` byte-identical). Largest single task; all downstream tests depend on its interface + reason codes. Gotcha: stdlib only (no `requests` / `pyyaml` / third-party); canonical JSON output (sort_keys=True, separators=(',',':')) for stable hashes in `--report`.
3. **T-007** — installer manifest row (active + `template/`). Unblocks T-009 fixture assertion.
4. **T-008** — parity-script `--scope=caveman-compress` mode (active + `template/`). Exercises T-001 output; gives a CI hook for positive-parity drift.
5. **T-002** — runbook subsection (active + `template/`). Locked strings (three-axis paragraph + four CLI flags).
6. **T-003** — reference-doc three-sentence paragraph (active + `template/`). Replace, do not append — the existing two-sentence paragraph is the target.
7. **T-006** — fixture tree (active-only). 8 classes; literal-region class needs 9 sub-fixtures (one per DEC-0072 §4 zone).
8. **T-005** — contract-test extension (active-only, tests do not mirror). Additions only; preserve S0075 subtest bodies byte-unchanged. Lock reason-code cardinality at 9 and rule SHA-256 at baseline.
9. **T-009** — install-completeness fixture + harness section (active-only). Pick next unassigned §26-series number (candidate §26S) during /execute by inspecting last-assigned in `run-tests.ps1` / `run-tests.sh`.
10. **T-010** — assert-only architecture linkage subtest (active-only). No edit of `docs/engineering/architecture.md`.

### Parity checklist at a glance (for dev + QA cross-check)

- **Positive (active + `template/` byte-identical)**: T-001 script, T-002 runbook append, T-003 reference paragraph, T-007 manifest row, T-008 parity script `--scope=caveman-compress` mode.
- **Active-only**: T-004 `.gitignore` / `.gitkeep`, T-005 contract-tests, T-006 fixtures, T-009 install-completeness + harness section, T-010 architecture linkage subtest, `docs/engineering/architecture.md` `# US-0090` (per DEC-0072 §7 row 6 precedent).
- **NEGATIVE (MUST NOT be edited)**: `.cursor/rules/caveman.mdc` (+ mirror) baseline SHA-256 preserved; `.cursor/scratchpad*` byte strings unchanged; `.cursor/skills/its-magic/SKILL.md` (+ mirror); `.cursorignore`; `decisions/DEC-0072.md` (forward-linked only); `decisions/DEC-0073.md` (already authored at /architecture); canonical artifacts in DEC-0073 §4.1 (script self-protects).

### DEC-0073 anchors

- **§1** three-axis non-substitution (T-003, T-002) — `TOKEN_PROFILE × CAVEMAN_MODE × CAVEMAN_COMPRESS_INPUT` orthogonal.
- **§2** activation gate (T-001) — `CAVEMAN_COMPRESS_INPUT=1` + non-empty `CAVEMAN_FILE_SCOPE` + explicit `--write`.
- **§3** sidecar originals (T-001, T-004) — parallel tree under `docs/.caveman-originals/<relative/path>/<file>`; `.gitignore` anchor + `.gitkeep`.
- **§4 + §4.1** deny-list source of truth (T-001) — layered precedence: baseline → `.gitignore` merge → `.cursorignore` overlay; deny always wins.
- **§5 + §5.1** allow-list grammar (T-001) — hybrid (named profile / raw globs) + frozen `docs-prose-only` v1 profile.
- **§6** safe-mode algorithm (T-001, T-006 class 5) — strictly idempotent; aggressive deferred.
- **§7** 9-code reason vocabulary (T-001, T-005 subtest #11) — 3 families (Gating / Scope / Integrity).
- **§8** CLI contract (T-001, T-002) — `--dry-run` default / `--write` / `--verify-originals` / `--report`; conflict fails closed `CAVEMAN_COMPRESS_FLAG_CONFLICT`.
- **§9** template parity inventory (T-001, T-002, T-003, T-005, T-006, T-007, T-008) — 8 positive rows + negative-parity set.
- **§10** installer / publish (T-007, T-008, T-009) — manifest entry + parity script extension + install-completeness fixture (R11 non-negotiable).
- **§11** non-goals / cross-cutting absorbed per-task (T-002 runbook, T-005 negative-parity subtests, T-001 deny-self-protection, T-010 architecture-linkage assert-only).

### Risks (locked at architecture; sprint-plan preserves)

- **R8** aggressive filler-word drift → neutralized (§6 Option B only; no `--mode` flag ships).
- **R9** reason-code proliferation → mitigated (9 codes in 3 families locked; T-005 subtest asserts cardinality).
- **R10** rule-subsection byte-identity → mitigated (no rule edit in v1; T-005 asserts baseline SHA-256).
- **R11** install-completeness omission (BUG-0003 class) → mitigated (T-007 + T-009 non-negotiable).
- **R-S1..R-S6** (sprint-phase risks — literal-region scan false negative, deny-list baseline drift, scratchpad byte-string preservation, `.cursorignore` boundary, existing subtest byte-unchanged) → per-task acceptance checks (see `sprints/S0076/sprint.md` § Additional sprint risks).

### Governance

- **DEC-0073**, **DEC-0072**, **R-0073**, architecture `# US-0090`.
- **US-0017**, **US-0045**, **US-0048 / DEC-0029**, **US-0056 / DEC-0038**, **US-0058 / DEC-0040**, **US-0069 / DEC-0051**, **US-0080 / DEC-0062**, **US-0088**, **US-0071**, **US-0085 / DEC-0071**, **US-0078 / DEC-0060**, **BUG-0001 / DEC-0063**, **BUG-0003 / DEC-0066**, **BUG-0006**.

---

## TL -> Dev Handoff — **US-0090** (post-architecture; pre-sprint) — post-**`/architecture`** -> **`/sprint-plan`** (**tech-lead**) — **superseded** by `## Sprint Plan — S0076 / US-0090` above

> **2026-04-18T22:00:00Z** — **`/architecture`** authored in fresh **tech-lead** context (`orchestrator_run_id=auto-20260418-01`, `fresh_context_marker=tl-US0090-architecture-20260418T220000Z-fresh`, `runtime_proof_id=rp-auto-20260418-01-architecture-tech-lead-20260418T220000Z-US0090`). Binding decision **`DEC-0073`** (composes on **`DEC-0072`** — forward-link, no rewrite); architecture section **`docs/engineering/architecture.md`** **`# US-0090`** appended. No sprint created yet — next phase is **`/sprint-plan`** (fresh **tech-lead**) -> then **`/plan-verify`** (fresh **qa**) -> then **`/execute`** (fresh **dev**). Story **`US-0090`** remains **OPEN** (**US-0045**). Dev entry is blocked until `/sprint-plan` authors `sprints/SXXXX/*` and `/plan-verify` moves the plan to **PASS**.

### Architecture anchors

- **Companion DEC**: `decisions/DEC-0073.md` (§1–§11 map 1:1 to the eleven research-phase architecture-asks)
- **Architecture section**: `docs/engineering/architecture.md` **`# US-0090`** (active-only per DEC-0072 §7 row 6 precedent)
- **Substrate DEC (unchanged)**: `decisions/DEC-0072.md` (binding for US-0089; forward-linked, not rewritten, by DEC-0073)
- **Research**: `docs/engineering/research.md` **`R-0073`** (shared anchor; Q9–Q19 resolution pass dated 2026-04-18)
- **State checkpoint**: `docs/engineering/state.md` — **Architecture checkpoint (2026-04-18) — US-0090 / `auto-20260418-01`**
- **PO→TL sprint-plan brief**: `handoffs/po_to_tl.md` **`## Architecture Addendum — US-0090`** (11 atomic task seeds + test surfaces + parity touchpoints + release gates + risks)

### Atomic task seed → AC → DEC-0073 § (sprint-plan locks exact `T-xxx` identifiers)

| Seed | Summary | AC | DEC-0073 § |
|------|---------|----|-----------|
| 1 | `scripts/caveman_compress_input.py` + `template/` mirror (CLI §8; activation §2; deny §4; allow §5; algorithm §6; reason codes §7; sidecar §3) | AC-1..AC-5 | §2, §3, §4, §5, §6, §7, §8 |
| 2 | `docs/engineering/runbook.md` (+ `template/`) — `### Caveman input compression (US-0090)` subsection | AC-5, AC-7 | §9 row 2 |
| 3 | `docs/engineering/auto-orchestration-reference.md` (+ `template/`) — three-sentence non-substitution paragraph | AC-7 | §1 + §9 row 3 |
| 4 | `.gitignore` anchor `docs/.caveman-originals/` + `docs/.caveman-originals/.gitkeep` | AC-2 | §3 + §9 rows 7–8 |
| 5 | `tests/auto_command_contract_test.py` extension — `test_caveman_compress_input_*` subtests | AC-6 | §9 test strategy |
| 6 | `tests/fixtures/caveman_compress/` — 8 fixture classes | AC-6 | §9 test strategy |
| 7 | Rule byte-identity guard + deny-list version guard subtests | AC-6, AC-8 | §9 + §4.2 |
| 8 | `installer-owned-paths.manifest` (+ `template/`) — `template/scripts/caveman_compress_input.py` under `install_include_paths` | AC-8 | §10 |
| 9 | `scripts/check_intake_template_parity.py` (+ `template/`) — `--scope=caveman-compress` mode | AC-8 | §10 Option A |
| 10 | `tests/installer_completeness_bug0003_test.py` extension + new `run-tests` section (candidate `§26S`) | AC-6, AC-8 | §10 Option A + §9 |
| 11 | Architecture `# US-0090` linkage check (assert-only; no rewrite) | AC-7 | §9 row 4 |

### Dev entry conditions (blocking; enforced by `/plan-verify`)

- `/sprint-plan` must author `sprints/SXXXX/sprint.md` + `sprints/SXXXX/tasks.md` + `sprints/SXXXX/plan-verify.json` (`status=PENDING`, `reason=AWAITING_QA_PLAN_VERIFY`).
- `/plan-verify` must move `plan-verify.json` `status` from **`PENDING`** to **`PASS`** before `/execute`.
- Fresh **dev** context required (US-0048 / DEC-0029 isolation); strict runtime proof (DEC-0038) required at `/execute`.
- Dev MUST edit active + `template/` in the same commit for parity rows 1 / 2 / 3 / 8 / 9 of DEC-0073 §9.
- Dev MUST NOT edit `.cursor/rules/caveman.mdc` or its `template/` counterpart (**negative parity; R10 byte-identity**). Pre-US-0090 SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` preserved.
- Dev MUST NOT modify `test_caveman_default_off_*` subtests (DEC-0072 §6 row 6 invariant — additions only, never modifications of existing).
- Dev MUST NOT add new reason codes, new CLI flags (`--mode`, `--purge-orphans`), new allow-list profiles, or new fixture classes beyond `DEC-0073` §9 without a subsequent DEC.
- Dev MUST NOT author or reference `npx skills add` in any rule / doc / command / scratchpad / script (DEC-0072 §8 carried).

### Parity touchpoints at a glance

- **Positive (active + `template/` byte-identical)**: rows 1, 2, 3, 4, 5 of DEC-0073 §9 + installer-owned-paths manifest (§10) + `check_intake_template_parity.py` (§10).
- **Active-only (no mirror; per DEC-0072 §7 precedent)**: architecture section, contract-tests, fixtures, `.gitignore`, `.gitkeep`.
- **NEGATIVE parity (MUST NOT be edited)**: `.cursor/rules/caveman.mdc` + mirror, scratchpad byte strings, `.cursor/skills/its-magic/SKILL.md` + mirror, `.cursorignore`, all canonical-artifact / contract-surface files in DEC-0073 §4.1.

### Risks and their architecture mitigations (sprint-plan must preserve)

- **R8** (aggressive filler-word drift): **aggressive mode deferred** in v1 (§6 Option B only). No `--mode` flag ships. Sprint-plan MUST NOT reopen.
- **R9** (reason-code proliferation): 9 codes locked into 3 families (Gating / Scope / Integrity). No new codes without DEC revising §7.
- **R10** (rule-subsection byte-identity): **no rule edit** in v1 (§9 NEGATIVE parity). Byte-identity guard subtest (seed 7) is a hard requirement.
- **R11** (install-completeness omission / BUG-0003 class): install-completeness fixture extension (seed 10) is **non-negotiable**; `/release` MUST NOT ship without it.

### Scope guards for `/sprint-plan` (non-negotiables)

- Do not rewrite `DEC-0072` or `DEC-0073`. Do not re-open architecture decisions.
- Do not advance backlog status (US-0090 stays **OPEN** per **US-0045**; closure at `/release`).
- Do not seed tasks outside the 11 seeds above without explicit justification tied to a specific AC.
- Do not change `TOKEN_PROFILE` / `CAVEMAN_MODE` / strict-proof / isolation-evidence / `AUTO_QUIET` / US-0071 contracts.

---

## TL -> Dev Handoff — **S0075** / **US-0089** (post-sprint-plan) — post-**`/sprint-plan`** -> **`/plan-verify`** (**qa**) — **superseded** by US-0090 architecture handoff above

> **2026-04-18T12:45:00Z** — **`/sprint-plan`** authored in fresh **tech-lead** context (`orchestrator_run_id=auto-20260418-01`, `fresh_context_marker=tl-US0089-sprint-plan-20260418T124500Z-fresh`). Sprint **`S0075`** created; **AC-1..AC-8** map **1:1** to **`T-001..T-008`** (`plan_integrity.task_ac_bijection=true`, `task_count=8`, `SPRINT_MAX_TASKS=12`, `within_limit=true`, `SPRINT_AUTO_SPLIT` not triggered). Story **`US-0089`** remains **OPEN** (**US-0045**). No execution started yet — next phase is **`/plan-verify`** (fresh **qa**) -> then **`/execute`** (fresh **dev**).

### Sprint anchor

- **Sprint overview**: `sprints/S0075/sprint.md`
- **Atomic tasks**: `sprints/S0075/tasks.md`
- **Plan-verify (qa)**: `sprints/S0075/plan-verify.json` (`status=PENDING`, `reason=AWAITING_QA_PLAN_VERIFY`)
- **Architecture lock**: `decisions/DEC-0072.md` + `docs/engineering/architecture.md` `# US-0089`
- **Research**: `docs/engineering/research.md` `R-0073` (discovery + research extensions)
- **State checkpoint**: `docs/engineering/state.md` — **Sprint-plan checkpoint (2026-04-18) — US-0089 / S0075 / `auto-20260418-01`**

### Task -> AC bijection

| Task | AC | Locked scope (DEC-0072 anchors) |
|------|----|---------------------------------|
| T-001 | AC-1 | Scratchpad keys in `.cursor/scratchpad.md` + active/template `.cursor/scratchpad.local.example.md` (DEC-0072 §3) |
| T-002 | AC-2 | Default-off invariant subtests (DEC-0072 §6 items 6–8: existing tokens, gate vocabulary, no vendor install leak) |
| T-003 | AC-3 | `.cursor/rules/caveman.mdc` (active + `template/`) — 9-zone literal-region invariant + 5 phrases (DEC-0072 §2 / §4 / §5) |
| T-004 | AC-4 | Non-substitution paragraph in `docs/engineering/auto-orchestration-reference.md` (active + `template/`) (DEC-0072 §1) |
| T-005 | AC-5 | `### Caveman mode (US-0089)` subsection in `docs/engineering/runbook.md` (active + `template/`) (DEC-0072 §5) |
| T-006 | AC-6 | 5 remaining `test_caveman_default_off_*` subtests (DEC-0072 §6 items 1–5) |
| T-007 | AC-7 | Architecture section `# US-0089` linkage + append-bottom integrity (assertion-only; no rewrite) |
| T-008 | AC-8 | Template parity sweep + `.cursor/skills/its-magic/SKILL.md` negative-parity (DEC-0072 §7 row 8) |

### Dev entry conditions (blocking)

- `/plan-verify` must move `sprints/S0075/plan-verify.json` `status` from **`PENDING`** to **`PASS`** before `/execute`.
- Fresh **dev** context required (US-0048 / DEC-0029 isolation) and strict runtime proof (DEC-0038) for `/execute`.
- Dev MUST edit active + `template/` in the same commit for rows 2 / 3 / 4 / 5 of DEC-0072 §7.
- Dev MUST NOT edit `.cursor/skills/its-magic/SKILL.md` or its `template/` counterpart (row 8 negative-parity).
- Dev MUST NOT author or reference `npx skills add` in any rule / doc / command / scratchpad (contract subtest #8).

### Carry-forward from pre-sprint architecture handoff

The pre-sprint architecture handoff body (scope, locked decisions, file touchpoints, non-goals, test expectations, parity checklist, scope pointers) stays canonical below; sprint-plan adds task identifiers and ordering only.

---

## TL -> Dev Handoff — **US-0089** (pre-sprint architecture) — post-**`/architecture`** -> **`/sprint-plan`** (**tech-lead**)

> **2026-04-18T12:30:00Z** — **`/architecture`** **PASS** (**tech-lead**, `orchestrator_run_id=auto-20260418-01`, `fresh_context_marker=tl-US0089-architecture-20260418T123000Z-fresh`). **`DEC-0072`** locked. Story **`US-0089`** remains **OPEN** (**US-0045**). No sprint created yet — next phase is **`/sprint-plan`** (fresh **tech-lead**).

### Scope (locked by DEC-0072)

Deliver **response-side** Cursor Caveman voice mode, **default off**, with:

- **Option A orthogonal composition** — `TOKEN_PROFILE` (US-0080 / DEC-0062) and `CAVEMAN_*` are independent axes; neither substitutes for the other.
- **Option A rule-only surface** — single new `.cursor/rules/caveman.mdc` active + `template/` mirror; NO new skill.
- **Four scratchpad keys** with exact byte-literal test strings (see DEC-0072 §3).
- **9-zone literal-region invariant** preserved under `CAVEMAN_MODE=1` (DEC-0072 §4).
- **5 canonical operator toggle phrases** (DEC-0072 §5).
- **8 `test_caveman_default_off_*` subtests** extending `tests/auto_command_contract_test.py` in place (DEC-0072 §6).

### Locked decisions (summary)

| # | Decision | Lock |
|---|----------|------|
| 1 | TOKEN_PROFILE × CAVEMAN | Option A (orthogonal, non-substitution); verbatim paragraph in reference + runbook. |
| 2 | Composition surface | Option A rule-only — `.cursor/rules/caveman.mdc` active + `template/`. No skill. |
| 3 | Scratchpad keys | `CAVEMAN_MODE=0\|1` default `0`; `CAVEMAN_LEVEL=lite\|full\|ultra` default empty; reserved no-ops `CAVEMAN_COMPRESS_INPUT=0\|1` default `0`, `CAVEMAN_FILE_SCOPE=` empty. |
| 4 | Literal-region invariant | 9-zone MUST list (fenced code, paths, AC checklists, reason codes, IDs, contract markers, strict-proof fields, isolation fields, git refs). |
| 5 | Operator phrases | `caveman on`, `caveman off`, `stop caveman`, `normal mode`, `caveman: lite\|full\|ultra`. |
| 6 | Default-off tests | Extend `tests/auto_command_contract_test.py` in place — 8 subtests; no new module. |
| 7 | Template parity | 8-row inventory (DEC-0072 §7; architecture `# US-0089` §7). |
| 8 | Non-goals | No input-side compression (US-0090), no TOKEN_PROFILE change, no canonical artifact rewrites, no new deps, no vendor install path. |

### File touchpoints for `/execute`

| # | Active path | Template path | Action |
|---|-------------|---------------|--------|
| 1 | `.cursor/scratchpad.md` | n/a (example-only install, DEC-0055) | Add 4 Caveman key lines + `## Caveman mode (US-0089)` comment block. |
| 2 | `.cursor/scratchpad.local.example.md` | `template/.cursor/scratchpad.local.example.md` | Add identical 4 key lines + comment block (literal parity). |
| 3 | `.cursor/rules/caveman.mdc` (**new**) | `template/.cursor/rules/caveman.mdc` (**new**) | Create rule per DEC-0072 §2 / §4 / §5. |
| 4 | `docs/engineering/auto-orchestration-reference.md` | `template/docs/engineering/auto-orchestration-reference.md` | Insert non-substitution paragraph near `TOKEN_PROFILE` / `AUTO_QUIET` discussion. |
| 5 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | Add `### Caveman mode (US-0089)` subsection (key table, phrase catalog, non-substitution paragraph). |
| 6 | `docs/engineering/architecture.md` `# US-0089` | active-only | Already written (this phase). |
| 7 | `tests/auto_command_contract_test.py` | active-only | Extend in place (8 subtests). |
| 8 | `.cursor/skills/its-magic/SKILL.md` | `template/.cursor/skills/its-magic/SKILL.md` | **No change** — negative parity assertion. |

### Non-goals (hard)

- No input-side file compression; `CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE` remain **documented no-ops**. No script, no installer change, no file mutator. US-0090 owns that vertical.
- No change to `TOKEN_PROFILE` semantics, context packs, archive policy, or phase-context slimming.
- No rewrite of `docs/product/backlog.md` outside the `## US-0089` `architecture_notes` append, `docs/product/acceptance.md`, `docs/engineering/state.md` schema, `handoffs/intake_evidence/*.json`, or DEC files.
- No new npm / Python dependencies. No `package.json` edit.
- No `npx skills add` surfaced in runbook or rule (contract test #8 guards this).
- No modification of `.cursor/skills/its-magic/SKILL.md` (row 8 negative parity).
- No change to spawn-only orchestration (US-0048 / DEC-0029 / BUG-0006), strict runtime proof (DEC-0038), `AUTO_QUIET` non-suppressible list (US-0088), or US-0071 visible-metadata rules.
- No unit test of voice quality under `CAVEMAN_MODE=1`.

### Test expectations for `/qa`

`tests/auto_command_contract_test.py` gains 8 subtests, all file-presence / token-presence / literal-equality:

1. `test_caveman_default_off_scratchpad_keys_active` — 4 exact lines in `.cursor/scratchpad.md`.
2. `test_caveman_default_off_scratchpad_keys_example_parity` — same 4 lines in both active and template example files (byte parity).
3. `test_caveman_default_off_rule_file_present_active_template` — rule file exists active + `template/`, contains tokens `CAVEMAN_MODE`, `literal`, and all five canonical phrases.
4. `test_caveman_default_off_reference_non_substitution_paragraph` — exact non-substitution sentence in reference doc (active + `template/`).
5. `test_caveman_default_off_runbook_operator_phrases` — five phrases + non-substitution sentence in runbook (active + `template/`).
6. `test_caveman_default_off_existing_contract_tokens_intact` — existing `required` token list unchanged (may only add).
7. `test_caveman_default_off_non_suppressible_gate_vocab_preserved` — gate vocabulary intact in `auto.md` + reference.
8. `test_caveman_default_off_no_vendor_install_leak` — no `npx skills add` token anywhere.

QA must also confirm the 9-zone literal-region list is present verbatim in `.cursor/rules/caveman.mdc` (both active and `template/`).

### Template parity checklist (US-0017)

For each "active + template" row above, parity is asserted via contract subtests #2, #3, #4, #5. Dev MUST:

- Edit both surfaces in the same commit.
- Preserve byte-identical text for the non-substitution paragraph across reference + runbook + template mirrors.
- Preserve byte-identical scratchpad key lines across `.cursor/scratchpad.local.example.md` and `template/.cursor/scratchpad.local.example.md`.
- Leave `.cursor/skills/its-magic/SKILL.md` and `template/.cursor/skills/its-magic/SKILL.md` untouched.

### Scope pointers

- **`docs/engineering/architecture.md`** **`# US-0089`** — full contract.
- **`decisions/DEC-0072.md`** — Accepted decision record (exact test strings in §3 and §6).
- **`docs/engineering/research.md`** **`R-0073`** (research extension 2026-04-18) — rationale for Option A choices and 9-zone list origin.
- **`handoffs/po_to_tl.md`** — Architecture Addendum — US-0089 (tail mirror).

### Governance

- **DEC-0072** (this story).
- **DEC-0062** / **US-0080** — TOKEN_PROFILE semantics unchanged.
- **DEC-0035** / **US-0053** — tiered profile unchanged.
- **US-0088** — `AUTO_QUIET` non-suppressible gate list inherited verbatim.
- **US-0071** — visible ID metadata preserved (9-zone list zone 5).
- **US-0048** / **DEC-0029**, **US-0056** / **DEC-0038**, **BUG-0006** — spawn-only / isolation / strict-proof untouched.
- **US-0017** — active/`template/` parity.
- **DEC-0055** — scratchpad example-only install policy (row 1 has no `template/` mirror of `.cursor/scratchpad.md` itself).
- **DEC-0040** — artifact-ordering policy respected (architecture section appended at bottom).
- **US-0045** — backlog status authority stays in `docs/product/backlog.md`.

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **US-0089** — atomize DEC-0072 §7 parity inventory into tasks against AC-1..AC-8 (story has 8 ACs). Recommended mapping: 1 task per template-parity row + 1 task per test-subtest cluster + 1 task for the architecture-notes / parity sweep, all within `SPRINT_MAX_TASKS=12`. Or **`/auto start-from=sprint-plan`**.

---

## TL -> Dev Handoff — **US-0086** / **S0074** — post-**`/sprint-plan`** -> **`/plan-verify`** (**tech-lead**)

> **2026-04-13T19:45:00Z** - **`/sprint-plan`** **PASS** (**tech-lead**, **`orchestrator_run_id=auto-20260405-01`**). Story **`US-0086`** remains **OPEN** (**US-0045**). Sprint **`S0074`** created. Plan-verify **`PENDING`** (**`AWAITING_QA_PLAN_VERIFY`**) - proceed to **`/plan-verify`** (fresh **qa** context).

### Sprint S0074 summary

- **story_refs**: US-0086
- **goal**: Deliver automation-only remote execution selection with deterministic NL target resolution, fail-closed reason codes, remote-routing evidence tuple capture, US-0085 security continuity, and active/template parity.
- **task_count**: 10 (within SPRINT_MAX_TASKS=12)

### Task map (AC -> Task)

| Task | AC | Summary |
|------|----|---------|
| T-001 | AC-1 | Add automation profile keys to scratchpad surfaces (active + template), default-off/manual unchanged |
| T-002 | AC-2 | Document manual vs automation mode in runbook (active + template) |
| T-003 | AC-3 | Add deterministic mode-on routing guidance and mode-off no-reroute guardrails (commands/rules + template) |
| T-004 | AC-4 | Document/lock `start container <target_id>` resolution and fail-closed unknown/disabled behavior |
| T-005 | AC-5 | Define remote-routing evidence tuple for execute/qa handoffs |
| T-006 | AC-6 | Add deterministic optional CI recipe for remote routing |
| T-007 | AC-7 | Enforce security continuity (no `.env` reads, names-only secret posture) |
| T-008 | AC-8 | Add/extend target-resolution pass/fail tests and mode-off non-regression |
| T-009 | AC-9 | Reconcile architecture lock consistency (`# US-0086`, reason codes, key names, compatibility) |
| T-010 | AC-10 | Perform active/template parity sweep for all touched surfaces |

### Scope pointers

- **`docs/engineering/architecture.md`** **`# US-0086`** — routing precedence, reason codes, evidence tuple, compatibility boundaries
- **`docs/engineering/research.md`** **`R-0068`** — routing matrix and evidence rationale
- **`sprints/S0074/sprint.md`** — sprint metadata + AC coverage matrix
- **`sprints/S0074/tasks.md`** — atomic task definitions
- **`sprints/S0074/plan-verify.json`** — seeded **`PENDING`** for QA

### Governance

- **US-0064 / DEC-0070**: remote schema compatibility unchanged
- **US-0085 / DEC-0071**: no `.env` reads; names-only secret posture
- **US-0045**: backlog status authority remains in `docs/product/backlog.md`

### Next

- **`/plan-verify`** (fresh **qa** context) for **`S0074`** / **`US-0086`**, or **`/auto start-from=plan-verify`**.

## TL -> Dev Handoff — **US-0085** / **S0073** — post-**`/sprint-plan`** → **`/plan-verify`** (**tech-lead**)

> **2026-04-13T12:45:00Z** — **`/sprint-plan`** **PASS** (**tech-lead**, **`orchestrator_run_id=auto-20260405-01`**). Story **`US-0085`** remains **OPEN** (**US-0045**). Sprint **`S0073`** created. Plan-verify **`PENDING`** (**`AWAITING_QA_PLAN_VERIFY`**) — proceed to **`/plan-verify`** (fresh **qa** context).

### Sprint S0073 summary

- **story_refs**: US-0085
- **goal**: Deliver gitignored `.env` for remote and release connectivity with 4-layer defense-in-depth exclusion (DEC-0071), committed `.env.example`, agent/IDE exclusion, operator documentation, optional parity helper, regression tests, and template parity.
- **task_count**: 10 (within SPRINT_MAX_TASKS=12)

### Task map (AC -> Task)

| Task | AC | Summary |
|------|----|---------|
| T-001 | AC-1 | Update `.gitignore` (active) + create `template/.gitignore` with `.env`/`.env.local` |
| T-002 | AC-2 | Create `.cursorignore` (active + template) with `.env*` exclusion |
| T-003 | AC-3 | Create `.env.example` (active + template) — 20 `*Env` names, grouped |
| T-004 | AC-4 | Update `docs/engineering/runbook.md` (active + template) — `.env` recipe |
| T-005 | AC-5 | Update `docs/engineering/runtime-connectivity.md` (active + template) — `*Env` sourcing |
| T-006 | AC-6 | Update `docs/engineering/us-0084-remote-e2e.md` (active + template) — `.env` refs |
| T-007 | AC-7 | Append `.env` exclusion rule to `coding-standards.mdc` (active + template) |
| T-008 | AC-8 | Create `scripts/print_remote_env_hint.py` — names-only parity helper |
| T-009 | AC-9 | Create `tests/test_env_gitignore.py` — regression test |
| T-010 | AC-10 | Verify `remote_config_summary.py` + tests remain PASS |

### Scope pointers

- **`docs/engineering/architecture.md`** **`# US-0085`** — file layout, `.env.example` contract, defense-in-depth layers, template parity, risks
- **`decisions/DEC-0071.md`** — 4-layer `.env` exclusion contract
- **`docs/engineering/research.md`** **`R-0072`** — `*Env` inventory, `.cursorignore` semantics
- **`sprints/S0073/sprint.md`** — sprint metadata + AC coverage matrix
- **`sprints/S0073/tasks.md`** — atomic task definitions

### Governance

- **DEC-0071**: 4-layer defense-in-depth locked — `.gitignore` + `.cursorignore` + Cursor rules + operator discipline
- **US-0064** / **DEC-0070**: JSON schema unchanged; `.env` supplies values locally
- **US-0086** (OPEN): must compose with DEC-0071

### Template parity (7 touchpoints)

| # | Active path | Template path | Action |
|---|-------------|---------------|--------|
| 1 | `.gitignore` | `template/.gitignore` (**new**) | Create with `.env`/`.env.local` |
| 2 | `.cursorignore` (**new**) | `template/.cursorignore` (**new**) | Create with `.env*` patterns |
| 3 | `.env.example` (**new**) | `template/.env.example` (**new**) | 20 names, grouped |
| 4 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | `.env` copy/source recipe |
| 5 | `docs/engineering/runtime-connectivity.md` | `template/docs/engineering/runtime-connectivity.md` | `*Env` sourcing note |
| 6 | `docs/engineering/us-0084-remote-e2e.md` | `template/docs/engineering/us-0084-remote-e2e.md` | `.env`/`.env.example` refs |
| 7 | `.cursor/rules/coding-standards.mdc` | `template/.cursor/rules/coding-standards.mdc` | `.env` exclusion bullet |

### Next

- **`/plan-verify`** (fresh **qa** context) for **`S0073`** / **`US-0085`**, or **`/auto start-from=plan-verify`**.
