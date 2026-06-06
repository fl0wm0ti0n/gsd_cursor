# Sprint S0077

## Metadata

- **sprint_id**: S0077
- **story_refs**: US-0091
- **goal**: Deliver README ↔ backlog/acceptance static feature-coverage backfill across the README family (root + `template/` + DEV shard), ship deterministic stdlib validator with reason-code vocabulary, wire blocking release step **3f** composing on **US-0030**, and activate grandfathering toggle — per **DEC-0074** (composes on **DEC-0059**; extends release doc-gate family without rewriting **US-0030** delta semantics).
- **status**: planned
- **created_at**: 2026-06-06T15:00:00Z
- **orchestrator_run_id**: auto-20260606-01
- **fresh_context_marker**: tl-S0077-US0091-sprint-plan-20260606T150000Z-fresh

## Scope

- **US-0091**: README ↔ backlog/acceptance feature coverage backfill + blocking drift gate
- **Architecture**: `docs/engineering/architecture.md` `# US-0091` (active-only)
- **Binding decision**: `decisions/DEC-0074.md` (Accepted 2026-06-06) — composes on `DEC-0059`; extends **US-0030** release doc-gate family
- **Research anchor**: `docs/engineering/research.md` `R-0074`

## Non-goals (hard, from DEC-0074 §10)

- No rewrite of **US-0030** delta semantics or **DEC-0059** audience profiles.
- No new H2 literals in README family.
- No mandatory per-feature user guides (`USER_GUIDE_MODE` unchanged).
- No npm / pip runtime dependency (stdlib Python only).
- No acceptance.md row format change beyond optional human-scan suffix.
- No retroactive `/release` block before backfill completes (`README_FEATURE_COVERAGE_ENFORCE=0` until flip).
- No wiring into `validate-and-push` / `sync_push_gates.py` (wrong lifecycle).
- No duplicate root↔template README diff logic inside validator (compose **US-0017** instead).
- **Status authority (US-0045)**: US-0091 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0074** (§1–§10); architecture `# US-0091`; research **R-0074**
- **Governance stack (unchanged)**: **US-0030** (delta gate — unchanged), **US-0077 / DEC-0059** (audience profiles), **US-0017** (template drift guard), **US-0071** (user-visible metadata), **US-0045** (status authority), **US-0048 / DEC-0029** (isolation), **US-0056 / DEC-0038** (strict proof), **BUG-0001 / DEC-0063** + **BUG-0003 / DEC-0066** (installer completeness precedent)

## Acceptance criteria coverage (AC-1..AC-10 → T-xxx, strict bijection)

| AC | Description (summary) | Task | DEC-0074 § |
|----|-----------------------|------|------------|
| AC-1 | Deterministic **user-visible predicate** (`user_visible:` field + H1–H8 when enforce=0) | T-001 | §1, §2 |
| AC-2 | One-time **audit report** mapping DONE items to README anchors; gaps explicit | T-002 | §5 (`--audit-out`, `--report`) |
| AC-3 | **Backfill** in root + `template/` + DEV shard; blurbs + DEV traceability rows | T-003 | §3 |
| AC-4 | **Audience boundaries** — existing `USER_*` / `DEV_*` H2s; section budgets respected | T-004 | §3, §4, §6 |
| AC-5 | **Validator** + reason-code vocabulary + `--self-test` | T-005 | §5, §6 |
| AC-6 | **Release gate** step **3f** blocking when enforce=1; composes on US-0030 | T-006 | §7 |
| AC-7 | **Idempotent `--report`** — stable JSON counts and gap list | T-007 | §5 |
| AC-8 | **US-0071 hygiene** — no planning tokens in operator blurbs | T-008 | §3 (blurb preference) |
| AC-9 | **Template parity** — scoped parity script + installer manifest + US-0017 compose | T-009 | §9 |
| AC-10 | **Grandfathering DEC** — `README_FEATURE_COVERAGE_ENFORCE` toggle + activation procedure | T-010 | §8, this record |

## Task count

- **Total**: 10
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (10 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Bijection**: **AC-1..AC-10 ↔ T-001..T-010** (1:1; no multi-AC tasks)

## Governance

- **DEC-0074** §1–§10 (binding) — each task cites governing §(s).
- **R-0074** (research anchor).
- **US-0017** template parity policy.
- **US-0045** canonical status authority (US-0091 stays OPEN through this sprint).
- **US-0030** delta gate unchanged; **US-0091** adds static-coverage scripted check only.

## Template parity plan (DEC-0074 §9)

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `scripts/readme_feature_coverage_lib.py` | `template/scripts/readme_feature_coverage_lib.py` | T-001 | Positive (byte-identical) |
| 2 | `scripts/validate_readme_feature_coverage.py` | `template/scripts/validate_readme_feature_coverage.py` | T-005 | Positive (byte-identical) |
| 3 | `docs/engineering/context/readme-section-affinity.json` | `template/docs/engineering/context/readme-section-affinity.json` | T-004 | Positive (byte-identical) |
| 4 | `.cursor/commands/release.md` (step 3f) | `template/.cursor/commands/release.md` | T-006 | Positive (full-file per US-0017) |
| 5 | `docs/engineering/runbook.md` (subsection) | `template/docs/engineering/runbook.md` | T-006 | Positive (locked strings byte-identical) |
| 6 | `docs/engineering/context/installer-owned-paths.manifest` | `template/docs/engineering/context/installer-owned-paths.manifest` | T-009 | Positive (byte-identical) |
| 7 | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` | T-009 | Positive (`--scope=readme-feature-coverage`) |
| 8 | `README.md` backfill | `template/README.md` | T-003 | Positive (byte-identical per US-0017) |

**Active-only** (no `template/` mirror):

- `docs/engineering/architecture.md` `# US-0091`
- `tests/fixtures/readme_feature_coverage/`
- `docs/engineering/context/readme-feature-coverage-audit.json` (generated)
- `docs/developer/README.md` (DEV shard — no template mirror per DEC-0059)
- `docs/product/backlog.md` (`user_visible:` markers on touched items)

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Self-test + report idempotence (T-005, T-007)

- `python scripts/validate_readme_feature_coverage.py --self-test` → `[README_FEATURE_COVERAGE_SELF_TEST_OK]`
- `--report` run twice on same inputs → identical exit code + sorted reason-code list + JSON body (no timestamps in body)
- Fixture tree: `tests/fixtures/readme_feature_coverage/` (minimal repo trees)

### Harness (T-007)

- New section **§27U** in `tests/run-tests.ps1` + `tests/run-tests.sh` — self-test + report idempotence fixture

### Parity (T-009)

- `python scripts/check_intake_template_parity.py --scope=readme-feature-coverage` exits 0 on clean tree
- Compose with existing **US-0017** README byte guard — do not duplicate inside validator

### Metadata (T-008)

- `python scripts/check-user-visible-metadata.py` passes on changed README family paths

## Risks and mitigations (DEC-0074 §Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | False positives block `/release` | T-003 explicit `user_visible:` markers; T-010 enforce flip only after `--report` shows `coverage_missing: []` |
| R2 | README bloat | T-003 1–2 sentence blurbs; T-004 profile budget check → `README_FEATURE_COVERAGE_PROFILE_VIOLATION` |
| R3 | Three-file parity drift | T-009 US-0017 + scoped parity script |
| R4 | Retroactive lock-in | T-010 `README_FEATURE_COVERAGE_ENFORCE=0` until backfill merge; flip 0→1 same commit |
| R5 | US-0071 leakage | T-008 metadata scanner; T-003 prefer command/flag tokens in root blurbs |
| R6 | Heuristic ambiguity | T-001 H7 fail-closed; T-010 enforce=1 disables heuristic |
| R7 | Delta vs static confusion | T-006 runbook remediation table (delta vs static inventory) |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 10 acceptance criteria covered 1:1 by T-001..T-010.
- `sprints/S0077/plan-verify.json` reaches **PASS** with `plan_integrity.task_ac_bijection=true`, `task_count=10`, `within_limit=true`.
- `--report` shows `coverage_missing: []` before T-010 enforce flip.
- Full positive-parity byte equality across DEC-0074 §9 inventory rows 1–7.
- `docs/product/backlog.md` **`## US-0091`** retains **`OPEN`** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0077`** / **US-0091** — verify AC-1..AC-10 ↔ T-001..T-010 bijection, task-count bound, governance alignment. Target: `sprints/S0077/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
