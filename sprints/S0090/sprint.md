# Sprint S0090

## Metadata

- **sprint_id**: S0090
- **story_refs**: US-0100
- **goal**: Ship **version-scoped release changelog** and **GitHub `-F` release-note attachment** — **`CHANGELOG.md`**, per-version **`{semver}-release-notes.md`**, **`release_changelog_lib.py`** API, **`/release`** step **19**, **`release-all.sh`** **`-F`** replace **`--generate-notes`**, three-tier backfill manifest, **`RELEASE_CHANGELOG_*`** validators, ten **`test_us0100_*`** contract markers, harness **§26Y**, and **`RELEASE_CHANGELOG_PAIRS`** parity — per **DEC-0085** (composes **US-0040** / **US-0054** / **US-0067** / **US-0008**; research **R-0087**).
- **status**: planned
- **created_at**: 2026-06-15T04:00:00Z
- **orchestrator_run_id**: auto-20260615-01
- **fresh_context_marker**: tl-S0090-US0100-sprint-plan-20260615T040000Z-fresh

## Scope

- **US-0100**: Version-scoped release changelog and GitHub release-note attachment
- **Architecture**: `docs/engineering/architecture.md` `# US-0100`
- **Binding decision**: `decisions/DEC-0085.md`
- **Research anchor**: `docs/engineering/research.md` `R-0087`

## Non-goals (hard, from DEC-0085 / architecture `# US-0100`)

- No replacement or overwrite of non-target **`Sxxxx-release-notes.md`** (**US-0040**).
- No passing sprint notes to **`gh -F`** — per-version semver file only.
- No bypass of **`RELEASE_PUBLISH_MODE`** confirmation (**US-0054**).
- No default **`--generate-notes`** — fail-closed unless **`RELEASE_CHANGELOG_ALLOW_GENERATE_NOTES=1`**.
- No removal of **US-0067** Run/Connect/Verify operator hints from sprint notes.
- No runtime **`CHANGELOG.md`** parsing for **`gh`** attach — explicit per-version SOT only.
- **Status authority (US-0045)**: US-0100 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0085**; architecture `# US-0100`; research **R-0087**
- **Governance stack**: **US-0040** (sprint notes + queue), **US-0054** / **DEC-0036** (publish confirmation), **US-0067** (operator hints in sprint notes), **US-0008** (`release-all.sh`), **US-0017** (template parity), **US-0045** (status authority), **US-0048** / **DEC-0029** (isolation), **US-0056** / **DEC-0038** (strict proof), **DEC-0080** / **DEC-0081** (native chain compose)

## Acceptance criteria coverage (AC-1..AC-10 → T-xxx; surjective, 12 tasks / 10 ACs)

| AC | Description (summary) | Task(s) | Architecture anchor |
|----|-----------------------|---------|---------------------|
| AC-1 | Canonical cumulative **`CHANGELOG.md`** (Keep a Changelog 1.1.0) | T-002 | § Artifact paths; § `[Unreleased]` promotion |
| AC-2 | Per-version **`{semver}-release-notes.md`** + example pattern | T-003 | § Artifact paths |
| AC-3 | **`/release`** derivation hook + **`[Unreleased]`** promotion | T-001, T-004 | § Derivation precedence; § `/release` step 19 |
| AC-4 | Queue **`release_version`** binding + cross-refs | T-004, T-005 | § Derivation precedence; § Coalesce + backfill |
| AC-5 | **`release-all.sh`** **`gh -F`** replace **`--generate-notes`** | T-009 | § `release-all.sh` touchpoint |
| AC-6 | Three-tier backfill A/B/C + operator manifest | T-007, T-008 | § Coalesce + backfill |
| AC-7 | **`release_changelog_validate.py`** + 10 reason codes | T-001, T-006 | § Reason codes; § `release_changelog_lib.py` API |
| AC-8 | Runbook + **`release.md`** step **19** docs | T-004, T-010 | § `/release` touchpoint; § Scratchpad keys |
| AC-9 | Ten **`test_us0100_*`** + parity + harness | T-011, T-012 | § Contract tests + parity |
| AC-10 | Architecture + decision anchor | *(pre-satisfied at `/architecture`)* | **`DEC-0085`**; `# US-0100`; plan-verify attestation |

**Multi-AC tasks** (justified by architecture `# US-0100` § Atomic task seeds): **T-001** (AC-3+AC-7), **T-004** (AC-3+AC-4+AC-8), **T-007** (AC-6), **T-008** (AC-6), **T-011** (AC-9), **T-012** (AC-9+AC-10 parity/harness). Every AC has ≥1 task or architecture-phase attestation; no `PLAN_AC_COVERAGE_GAP`. **AC-10** pre-satisfied at architecture — no dev task seed per architecture § AC traceability.

## Task count

- **Total**: 12
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (12 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-10 coverage; **strict 1:1 task-to-seed** (12 architecture seeds → T-001..T-012); **not** strict AC bijection (multi-AC tasks above; AC-10 architecture-phase only)

## Governance

- **DEC-0085** (binding) — each task cites governing architecture §(s) and DEC §(s).
- **R-0087** (research anchor).
- **US-0040** compose — sprint notes remain canonical workflow evidence; version docs are additive layer.
- **US-0045** canonical status authority (US-0100 stays OPEN through this sprint).

## Edit surfaces and parity plan

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `scripts/release_changelog_lib.py` | `template/scripts/release_changelog_lib.py` | T-001 | Positive |
| 2 | `CHANGELOG.md` | `template/CHANGELOG.md` | T-002 | Positive |
| 3 | `template/handoffs/releases/vX.Y.Z-release-notes.md.example` | (template-only) | T-003 | N/A |
| 4 | `.cursor/commands/release.md` | `template/.cursor/commands/release.md` | T-004 | Positive |
| 5 | `handoffs/release_queue.md` | (active-only — lib binding) | T-005 | N/A |
| 6 | `scripts/release_changelog_validate.py` | `template/scripts/release_changelog_validate.py` | T-006 | Positive |
| 7 | `scripts/release_changelog_backfill.py` | `template/scripts/release_changelog_backfill.py` | T-007 | Positive |
| 8 | `docs/engineering/context/release-version-backfill.manifest.yaml` | (active-only) | T-008 | N/A |
| 9 | `scripts/release-all.sh` | (active-only — contract literals) | T-009 | N/A |
| 10 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-010 | Positive |
| 11 | `tests/auto_command_contract_test.py` | (active-only) | T-011 | N/A |
| 12 | `tests/run-tests.ps1` / `tests/run-tests.sh` | (active-only) | T-012 | Harness **§26Y** |
| 13 | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` | T-012 | Positive |

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** replace or overwrite non-target **`Sxxxx-release-notes.md`**.
- Do **not** pass sprint notes to **`gh -F`**.
- Do **not** bypass **`RELEASE_PUBLISH_MODE`** confirmation.
- Do **not** default **`--generate-notes`** without **`RELEASE_CHANGELOG_ALLOW_GENERATE_NOTES=1`**.
- Do **not** remove **US-0067** operator hints from sprint notes.

## Post-edit gate sequence (architecture § Contract tests)

1. `pytest -k us0100 tests/auto_command_contract_test.py` → all ten subtests green
2. `python scripts/check_intake_template_parity.py --scope=release-changelog` → PASS (**`RELEASE_CHANGELOG_PAIRS`**)

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Tranche A — lib + stubs (T-001..T-003)

- **`release_changelog_lib.py`** API surface, coalesce, fingerprint idempotency
- **`CHANGELOG.md`** + **`template/CHANGELOG.md`** stub with **`[Unreleased]`**
- Per-version path convention + **`vX.Y.Z-release-notes.md.example`**

### Tranche B — `/release` hook + queue binding (T-004..T-005)

- Step **19** (19a–19d) in active + template **`release.md`**
- **`bind_queue_release_version`** target-scoped queue mutation

### Tranche C — validator + backfill (T-006..T-008)

- **`release_changelog_validate.py`** + 10 **`RELEASE_CHANGELOG_*`** codes
- **`release_changelog_backfill.py`** Tier A/B/C idempotent seed
- Backfill manifest + runbook operator guidance

### Tranche D — publish integration (T-009)

- **`release-all.sh`** **`-F`** replace **`--generate-notes`** + enforce preflight

### Tranche E — docs + tests + parity (T-010..T-012)

- Runbook version-doc workflow (active + template)
- Ten **`test_us0100_*`** contract subtests; harness **§26Y**; **`RELEASE_CHANGELOG_PAIRS`** parity sweep

## Risks and mitigations (architecture § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Synthetic semver noise | T-008 Tier B manifest + remediation labels |
| R2 | **`[Unreleased]`** promotion race | T-001 fingerprint idempotency per semver |
| R3 | Pre-release filename edge cases | T-003 semver stem without **`v`**; **`test_us0100_changelog_artifact_paths_literals`** |
| R4 | **`--generate-notes`** fallback misuse | T-009 fail-closed; **`RELEASE_CHANGELOG_ALLOW_GENERATE_NOTES=0`** default |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 10 acceptance criteria covered surjectively (AC-10 attested at plan-verify from architecture phase).
- `sprints/S0090/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_surjective=true`, `task_count=12`, `within_limit=true`.
- `pytest -k us0100` green; parity **`--scope=release-changelog`** PASS.
- `docs/product/backlog.md` **`## US-0100`** retains **OPEN** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0090`** / **US-0100** — verify AC-1..AC-10 ↔ T-001..T-012 surjective coverage, task-seed bijection (12 seeds → 12 tasks), task-count bound, governance alignment. Target: `sprints/S0090/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
