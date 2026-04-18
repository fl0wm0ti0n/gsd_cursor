# Sprint S0076

## Metadata

- **sprint_id**: S0076
- **story_refs**: US-0090
- **goal**: Deliver input-side Caveman-style file compression — default-off, opt-in gate (`CAVEMAN_COMPRESS_INPUT=1` + non-empty `CAVEMAN_FILE_SCOPE`), sidecar-first atomic write under `docs/.caveman-originals/`, hard deny-list (deny always wins over allow), strictly-idempotent safe-mode minifier, 9-code reason-code vocabulary in 3 families, and full `active` + `template/` parity on every mirrored surface per **DEC-0073** §1–§11 (composes on **DEC-0072** via forward-link; **DEC-0072** not rewritten).
- **status**: planned
- **created_at**: 2026-04-18T22:30:00Z
- **orchestrator_run_id**: auto-20260418-01
- **fresh_context_marker**: tl-US0090-sprint-plan-20260418T223000Z-fresh

## Scope

- **US-0090**: Optional Caveman-style input compression (safe file scope)
- **Architecture**: `docs/engineering/architecture.md` `# US-0090` (active-only per DEC-0072 §7 row 6 precedent)
- **Binding decision**: `decisions/DEC-0073.md` (Accepted 2026-04-18) — composes on `decisions/DEC-0072.md` via forward-link; **does not rewrite** DEC-0072
- **Research anchor**: `docs/engineering/research.md` `R-0073` (shared anchor; Q9–Q19 resolution pass dated 2026-04-18)

## Non-goals (hard, from DEC-0073 §11 + DEC-0072 §8 carried)

- **No rewrite of `DEC-0072`** (forward-link only). No rewrite of `DEC-0073`.
- **No aggressive compression in v1** (DEC-0073 §6 — Option B safe-mode only). No filler-word list, no prose rewriter, no `--mode` flag, no `--purge-orphans` flag.
- **No LLM-assisted compression** ever (violates AC-6 by construction).
- **No `TOKEN_PROFILE` change** (US-0080 / DEC-0062 / DEC-0035 unchanged).
- **No change to strict runtime proof (DEC-0038) or isolation evidence (DEC-0029) tuple fields, or AC-10 phase-boundary block.**
- **No change to `AUTO_QUIET` non-suppressible vocabulary** (US-0088) or `US-0071` user-visible metadata sanitization.
- **No change to the 9-zone literal-region invariant** (DEC-0072 §4 reused verbatim; may grow in a future DEC, never narrow).
- **No change to DEC-0072 §5 operator phrase catalog** (input-side is script-invoked, not voice-toggled).
- **No mandatory auto-compress in `/auto`** (script is operator-run out-of-band).
- **No new npm / pip runtime dep** (stdlib Python only — `argparse`, `hashlib`, `json`, `os`, `pathlib`, `re`, `sys`).
- **No `npx skills add`** token anywhere in kit docs / rules / scripts / manifests (DEC-0072 §8 carried).
- **No rewrite of canonical workflow artifacts** — `docs/product/backlog.md` (outside `sprint_plan_notes` append), `docs/product/acceptance.md`, `docs/engineering/state.md` schema, `handoffs/intake_evidence/*.json`, `decisions/DEC-*.md`, `sprints/*/*` all structurally deny-listed (DEC-0073 §4.1).
- **No edit of `.cursor/rules/caveman.mdc`** or its `template/` mirror (R10 negative parity; pre-US-0090 SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` preserved end-to-end).
- **No edit of `.cursor/scratchpad.md`** or either `.cursor/scratchpad.local.example.md` surface (DEC-0072 §3 key byte strings preserved; no key added / renamed — `CAVEMAN_COMPRESS_INPUT` and `CAVEMAN_FILE_SCOPE` already exist as reserved no-ops).
- **No modification of existing `test_caveman_default_off_*` subtests** (DEC-0072 §6 row 6 invariant — additions only).
- **No new reason codes, no new CLI flags, no new allow-list profiles, no new fixture classes beyond DEC-0073 §9** (would require a subsequent DEC).
- **No `.cursorignore` mutation** (operator-owned per US-0085 / DEC-0071).
- **Status authority (US-0045)**: US-0090 stays **OPEN** throughout this sprint; closure happens at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0073** (binding decision; §1–§11); **DEC-0072** (substrate; forward-linked); architecture section `# US-0090`; research anchor `R-0073` (2026-04-18 resolution pass).
- **Governance stack (unchanged)**: **US-0017** (active / template parity), **US-0045** (canonical status authority), **US-0048 / DEC-0029** (isolation evidence), **US-0056 / DEC-0038** (strict runtime proof), **US-0058 / DEC-0040** (artifact ordering), **US-0069 / DEC-0051** (phase-role matrix), **US-0080 / DEC-0062** (`TOKEN_PROFILE`), **US-0088** (`AUTO_QUIET` non-suppressible list), **US-0085 / DEC-0071** (`.env` defense-in-depth), **US-0078 / DEC-0060** (intake-evidence integrity — deny-list anchor), **BUG-0001 / DEC-0063** + **BUG-0003 / DEC-0066** (installer-completeness precedent for §10).
- **Downstream**: None in this sprint. Future aggressive-mode, additional profiles, and additional reason-code families require new DECs forward-linking §6, §5.1, and §7 respectively.

## Acceptance criteria coverage (AC-1..AC-8 → T-xxx, DEC-0073 §)

| AC | Description (summary) | Task(s) | DEC-0073 § |
|----|-----------------------|---------|------------|
| AC-1 | **Gating** — compression inactive unless `CAVEMAN_COMPRESS_INPUT=1` + explicit `CAVEMAN_FILE_SCOPE` + `--write`; default off. | T-001 | §2, §7 (`CAVEMAN_COMPRESS_MODE_DISABLED`, `CAVEMAN_COMPRESS_SCOPE_EMPTY`, `CAVEMAN_COMPRESS_FLAG_CONFLICT`) |
| AC-2 | **Originals** — every `--write` creates/refreshes a sidecar at `docs/.caveman-originals/<relative/path>/<file>` before target mutation; sidecar-first atomic order. | T-001, T-004 | §3 |
| AC-3 | **Deny list** — hard refusals for `.env*`, intake evidence, canonical product/engineering docs, DEC files, sprint evidence, contract surfaces, binaries, vendor-install leaks; deny always wins over allow. | T-001 | §4 + §4.1 + §7 (`CAVEMAN_COMPRESS_DENY_HIT`) |
| AC-4 | **Scope** — `CAVEMAN_FILE_SCOPE` grammar (named profile / raw globs / hybrid); frozen v1 `docs-prose-only` profile; unknown profile and scope violation fail closed with reason codes. | T-001 | §5 + §5.1 + §7 (`CAVEMAN_COMPRESS_SCOPE_VIOLATION`, `CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE`) |
| AC-5 | **Operator UX** — `scripts/caveman_compress_input.py` CLI (`--dry-run` default, `--write`, `--verify-originals`, `--report`); runbook subsection documents 3-step dry-run → verify → write; revert via sidecar restore. | T-001, T-002 | §8 + §9 row 2 + §3 |
| AC-6 | **Tests** — path guards, scope parser, idempotency, literal-region preservation, deny/allow evaluation, flag-conflict handling; byte-idempotent safe-mode by construction. | T-005, T-006, T-009 | §6 + §9 test strategy (fixture classes 1–8) + §10 install-completeness extension |
| AC-7 | **`architecture.md` `# US-0090`** — linkage to `# US-0089`, US-0053, US-0085, US-0078 / DEC-0060; documents forbidden surfaces; three-axis non-substitution paragraph published in reference + runbook (active + `template/`). | T-003, T-010 | §1 + §9 row 3 + §9 row 4 + §11 non-goals |
| AC-8 | **Template parity** — script + runbook + reference paragraph + manifest + parity-script mirrored byte-identically; negative parity enforced for rule file (R10) and canonical artifacts; installer-owned-paths manifest updated. | T-005 (guards), T-007, T-008 | §9 rows 1 / 2 / 3 + §10 |

## Task count

- **Total**: 10
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (10 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Grouping rationale**: Architecture Addendum (`handoffs/po_to_tl.md` `## Architecture Addendum — US-0090`) hinted seeds 5 & 7 may be grouped (same test file `tests/auto_command_contract_test.py`); grouped into **T-005**. Seeds 1 & 4 stay separate (different file classes — script vs `.gitignore` / `.gitkeep` — atomic-write contract lives in the script, tree materialization is config). All other seeds stay atomic.

## Governance

- **DEC-0073** §1–§11 (binding) — each task cites the governing §(s).
- **DEC-0072** (substrate) — scratchpad contract §3 (reserved no-op keys activated), 9-zone literal-region invariant §4 (reused verbatim), default-off invariant §6 (preserved byte-unchanged), 8-row template parity inventory §7 (row 6 active-only precedent applied to §9 row 4).
- **R-0073** (research anchor — Q9–Q19 resolution pass, 2026-04-18).
- **US-0017** template parity policy.
- **US-0045** canonical status authority (US-0090 stays OPEN through this sprint).
- **US-0048 / DEC-0029** isolation evidence; **US-0056 / DEC-0038** strict runtime proof; **US-0069 / DEC-0051** phase-role matrix (sprint-plan = tech-lead default).
- **US-0088** `AUTO_QUIET` non-suppressible vocabulary; **US-0071** user-visible metadata.
- **US-0085 / DEC-0071** `.env` defense-in-depth (baseline deny includes `.env*`; `.cursorignore` left operator-owned).
- **US-0078 / DEC-0060** intake-evidence integrity (baseline deny includes `handoffs/intake_evidence/*.json`).
- **BUG-0001 / DEC-0063** + **BUG-0003 / DEC-0066** installer-completeness precedent for §10 (manifest entry + install-completeness fixture non-negotiable — R11).

## Template parity plan (DEC-0073 §9 — 8 positive rows + negative-parity set)

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `scripts/caveman_compress_input.py` (**new**) | `template/scripts/caveman_compress_input.py` (**new**) | T-001 | Positive (byte-identical) |
| 2 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-002 | Positive (locked strings byte-identical) |
| 3 | `docs/engineering/auto-orchestration-reference.md` | `template/docs/engineering/auto-orchestration-reference.md` | T-003 | Positive (three-sentence paragraph byte-identical) |
| 4 | `docs/engineering/architecture.md` `# US-0090` | active-only (per DEC-0072 §7 row 6 precedent) | T-010 | Active-only (assert-only linkage check) |
| 5 | `tests/auto_command_contract_test.py` (extended) | active-only (tests do not mirror) | T-005 | Active-only |
| 6 | `tests/fixtures/caveman_compress/` (**new**) | active-only (fixtures do not mirror) | T-006 | Active-only |
| 7 | `.gitignore` (repo-root) + `docs/.caveman-originals/.gitkeep` (**new**) | n/a (installer does not own repo `.gitignore`; sidecar root is repo-local) | T-004 | Active-only |
| 8 | `docs/engineering/context/installer-owned-paths.manifest` | `template/docs/engineering/context/installer-owned-paths.manifest` | T-007 | Positive (byte-identical entry) |
| 9 | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` | T-008 | Positive (byte-identical `--scope=caveman-compress` mode) |
| 10 | `tests/installer_completeness_bug0003_test.py` + `tests/run-tests.ps1` + `tests/run-tests.sh` | n/a (tests + harness active-only) | T-009 | Active-only |

**NEGATIVE parity (MUST NOT be edited in this sprint; guarded by T-005 subtests)**:

- `.cursor/rules/caveman.mdc` + `template/.cursor/rules/caveman.mdc` — SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` preserved end-to-end (R10).
- `.cursor/scratchpad.md`, `.cursor/scratchpad.local.example.md`, `template/.cursor/scratchpad.local.example.md` — DEC-0072 §3 key byte strings unchanged; `CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE` already exist as reserved no-ops (activated by this DEC without byte-string change).
- `.cursor/skills/its-magic/SKILL.md` + mirror — DEC-0072 §7 row 9 negative-parity invariant preserved.
- `decisions/DEC-0072.md`, `decisions/DEC-0073.md` — no rewrite.
- `.cursorignore` — operator-owned (US-0085 / DEC-0071).
- All files in DEC-0073 §4.1 deny baseline — structurally unreachable by script (script self-protects).

## Test strategy summary (no test code written in sprint-plan; strategy locked for /execute)

### Contract tests (`tests/auto_command_contract_test.py`, in-place extension — T-005)

New `test_caveman_compress_input_*` subtests covering:

1. Script presence active + template (byte-identical SHA-256 assertion; positive parity row 1).
2. `--dry-run` default behavior (no mutation when no mode flag supplied).
3. `--write` requires `CAVEMAN_COMPRESS_INPUT=1` (fail closed `CAVEMAN_COMPRESS_MODE_DISABLED` otherwise).
4. `--write` requires non-empty `CAVEMAN_FILE_SCOPE` (fail closed `CAVEMAN_COMPRESS_SCOPE_EMPTY` otherwise).
5. Unknown profile in `CAVEMAN_FILE_SCOPE` → `CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE`.
6. Flag conflict detection (`--dry-run --write`, `--write --verify-originals`, `--write --report`, unknown flags) → `CAVEMAN_COMPRESS_FLAG_CONFLICT`.
7. Deny-list evaluation precedes allow-list (deny always wins) — `CAVEMAN_COMPRESS_DENY_HIT` on baseline entry.
8. Sidecar tree materialization (`.gitkeep` presence, `.gitignore` anchor entry).
9. **Rule byte-identity guard** (seed 7a) — `.cursor/rules/caveman.mdc` active vs `template/` SHA-256 equality (R10; baseline `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` preserved).
10. **Deny-list version guard** (seed 7b) — `scripts/caveman_compress_input.py --report` emits stable `deny_list_version` SHA-256 (drift detection per §4.2).
11. Reason-code vocabulary completeness — exactly 9 codes, grouped in 3 families (Gating / Scope / Integrity) per §7; no extras.

**Invariant**: existing `test_caveman_default_off_*` subtests from S0075 MUST remain byte-unchanged (DEC-0072 §6 row 6). Additions only.

### Fixtures (`tests/fixtures/caveman_compress/`, active-only — T-006)

Eight fixture classes per DEC-0073 §9 test-strategy block:

1. Whitespace baseline (Option B safe-mode output — byte-idempotent).
2. Literal-region preservation (one fixture per DEC-0072 §4 zone; 9 total).
3. Deny-list refusal (one fixture per §4.1 entry class).
4. Scope violation (empty / outside allow / unknown profile).
5. Idempotency (AC-6) — `compress(compress(f)) == compress(f)` byte-for-byte.
6. Mode-disabled (`CAVEMAN_COMPRESS_INPUT=0`).
7. Original-missing (`--verify-originals` orphan detection).
8. Flag-conflict (`--dry-run --write`, `--write --verify-originals`, unknown flag).

### Install-completeness fixture extension (`tests/installer_completeness_bug0003_test.py` — T-009)

New assertion class verifying `--mode missing` + `--mode upgrade` deliver `template/scripts/caveman_compress_input.py` across `installer.sh`, `installer.ps1`, `installer.py` (R11 mitigation — BUG-0003 class non-regression).

### Run-tests harness (`tests/run-tests.ps1` + `tests/run-tests.sh` — T-009)

New section (candidate `§26S`; dev to lock exact number matching last assigned) wiring both contract subtests and install-completeness fixture.

## Risks and mitigations (R8–R11 carried from DEC-0073)

- **R8 — Filler-word drift** → **Neutralized**: aggressive mode deferred entirely (§6 Option B only). No `--mode` flag in v1. **Sprint guard**: T-001 implements safe-mode minifier only; adding aggressive-mode code is out-of-scope.
- **R9 — Reason-code proliferation** → **Mitigated**: vocabulary locked at 9 codes grouped in 3 families (Gating / Scope / Integrity). **Sprint guard**: T-005 subtest #11 asserts exactly 9 codes; DEC required for any addition.
- **R10 — Rule-subsection byte-identity** → **Mitigated**: no rule edit in v1 (§9 negative parity). **Sprint guard**: T-005 subtest #9 asserts SHA-256 equality active vs template `.cursor/rules/caveman.mdc`; baseline `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` preserved.
- **R11 — Install-completeness omission (BUG-0003 class)** → **Mitigated**: install-completeness fixture extension is **non-negotiable**. **Sprint guard**: T-007 (manifest entry), T-009 (completeness fixture + harness row) — `/release` MUST NOT ship without both green.

## Additional sprint risks

- **R-S1 — Atomic-write partial state**: mid-operation failure between sidecar write and target write could produce inconsistent state. **Mitigation**: DEC-0073 §3 locks sidecar-first atomic write order (temp + replace each step); T-001 acceptance asserts rollback on any step failure (no partial state).
- **R-S2 — Literal-region scan false negative**: safe-mode minifier affecting a byte inside a fenced code block would violate DEC-0072 §4. **Mitigation**: DEC-0073 §6 mandates pre-write and post-transform 9-zone scan with byte-for-byte equality check; fails closed with `CAVEMAN_COMPRESS_LITERAL_REGION_DAMAGED` (T-006 fixture class 2 covers every zone).
- **R-S3 — Deny-list baseline drift between releases**: adding / removing entries in §4.1 without a DEC is a contract violation. **Mitigation**: `--report deny_list_version` SHA-256 emission (T-001); T-005 subtest #10 asserts stable hash.
- **R-S4 — Scratchpad semantic activation without byte change**: activating `CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE` semantics without editing their byte strings must not break S0075 parity subtests. **Mitigation**: keys already exist from DEC-0072 §3; T-001 reads them; no scratchpad edit; existing S0075 subtests remain green.
- **R-S5 — `.cursorignore` operator-owned regression**: accidentally adding sidecar-related `.cursorignore` entry would cross DEC-0071 boundary. **Mitigation**: DEC-0073 §3 explicitly forbids kit-level parity entry; runbook subsection (T-002) documents operator-owned policy; no task touches `.cursorignore`.
- **R-S6 — `test_caveman_default_off_*` drift**: modifying existing S0075 subtests would violate DEC-0072 §6 row 6. **Mitigation**: T-005 additions only; linter-class review in plan-verify; QA regression against baseline subtest count + bodies.

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release exit criteria)

- All 8 acceptance criteria covered by their mapped tasks (see table above); AC-6 and AC-8 have multi-task coverage justified by Addendum.
- `sprints/S0076/plan-verify.json` reaches **PASS** with `plan_integrity.task_ac_bijection=true` (multi-AC task `ac_ref` fields cite Addendum justification) and `task_count=10`, `within_limit=true`, `sprint_auto_split_triggered=false`.
- No drift in existing `test_caveman_default_off_*` subtests (byte-unchanged invariant asserted).
- `.cursor/rules/caveman.mdc` SHA-256 unchanged end-to-end (R10 guard subtest green).
- 9-code reason-code vocabulary locked (no additions; R9 guard subtest green).
- Sidecar tree materializes (`.gitignore` anchor + `.gitkeep` + `docs/.caveman-originals/` root).
- `template/scripts/caveman_compress_input.py` delivered by all three installer entrypoints in `--mode missing` + `--mode upgrade` (R11 install-completeness fixture green).
- Full positive-parity byte equality across rows 1 / 2 / 3 / 8 / 9 of DEC-0073 §9 inventory; active-only surfaces for rows 4 / 5 / 6 / 7 / 10.
- `docs/product/backlog.md` **`## US-0090`** retains **`OPEN`** status (**US-0045**) through plan-verify / execute / qa / verify-work; closure flips `OPEN` → `DONE` at `/release`.

## Parity matrix summary (at-a-glance for dev + QA)

| Row | Surface | Active | Template | Enforcement |
|-----|---------|--------|----------|-------------|
| 1 | Script (`caveman_compress_input.py`) | new | new (byte-identical) | T-008 parity script + T-005 SHA-256 subtest |
| 2 | Runbook (Caveman input subsection) | append | append (locked strings byte-identical) | T-005 presence subtest |
| 3 | Reference (three-sentence paragraph) | replace two-sentence paragraph | mirror replace | T-005 presence subtest |
| 4 | Architecture section `# US-0090` | append | (active-only) | T-010 linkage subtest |
| 5 | Contract tests | extend in place | (active-only) | Self |
| 6 | Fixture directory | new | (active-only) | T-005 / T-006 |
| 7 | `.gitignore` + `.gitkeep` | new anchor + empty file | (active-only; installer does not own repo `.gitignore`) | T-005 subtest #8 |
| 8 | Installer manifest | add entry | mirror add | T-007 |
| 9 | Parity script (`--scope=caveman-compress`) | extend | mirror extend | T-008 |
| 10 | Install-completeness + harness | extend + §26S-class row | (active-only) | T-009 |
| negative | `.cursor/rules/caveman.mdc` (+ mirror) | **unchanged** | **unchanged** | T-005 subtest #9 (SHA-256 equality) |
| negative | `.cursor/scratchpad*` (three files) | **unchanged** | **unchanged** | DEC-0072 §6 S0075 subtests (byte-unchanged invariant) |
| negative | `.cursor/skills/its-magic/SKILL.md` (+ mirror) | **unchanged** | **unchanged** | DEC-0072 §7 row 9 |
| negative | `decisions/DEC-*.md` | **unchanged** (new DEC-0073 already authored at /architecture) | n/a | Self |
| negative | canonical artifacts (DEC-0073 §4.1) | **unreachable** | n/a | Script deny-list |

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0076`** / **US-0090** — verify AC-1..AC-8 coverage, AC-to-task mapping (including Addendum-justified multi-AC cases), task-count bound, governance alignment, and non-goals preserved. Target: `sprints/S0076/plan-verify.json` `status` flip **`PENDING`** → **`PASS`**.
