# Release Notes — S0090 / US-0100 (version-scoped release changelog)

- **sprint_id**: S0090
- **story_refs**: US-0100
- **release_name**: `S0090 — US-0100 version-scoped release changelog and GitHub release-note attachment`
- **release_date**: 2026-06-15T08:00:00Z
- **orchestrator_run_id**: auto-20260615-01
- **verdict**: **PASS**
- **binding_decision**: `DEC-0085`
- **research_anchor**: `R-0087`

## Summary

Ships the **version documentation layer** composing with **US-0040** sprint-scoped notes: cumulative **`CHANGELOG.md`** (Keep a Changelog 1.1.0 + mandatory **`[Unreleased]`**), per-version **`handoffs/releases/{semver}-release-notes.md`** SOT for GitHub **`-F`**, **`/release` step 19** derivation hook (19a–19d), **`release_changelog_lib.py`** / **`release_changelog_validate.py`** / **`release_changelog_backfill.py`**, queue **`release_version`** binding, and **`release-all.sh`** fail-closed **`-F`** replace for **`--generate-notes`**.

## What's new

- **Cumulative changelog stub (AC-1)** — `CHANGELOG.md` + `template/CHANGELOG.md` with **`## [Unreleased]`** anchor.
- **Per-version doc pattern (AC-2)** — `{semver}-release-notes.md` convention + example template; sprint **`Sxxxx`** notes unchanged.
- **`/release` step 19 (AC-3, AC-4)** — derive/coalesce/promote/append + queue version binding; workflow-only releases append to **`[Unreleased]`** when semver blank.
- **`release-all.sh` `-F` (AC-5)** — fail-closed **`RELEASE_CHANGELOG_VERSION_DOC_MISSING`** unless opt-in **`--generate-notes`**.
- **Three-tier backfill (AC-6)** — Tier A/B/C + `release-version-backfill.manifest.yaml`.
- **Validator + 10 reason codes (AC-7)** — `release_changelog_validate.py` enforce/warn paths.
- **Runbook + command docs (AC-8)** — version-doc workflow in runbook + release.md step 19.
- **Contract tests + parity (AC-9)** — ten **`test_us0100_*`** subtests; **`RELEASE_CHANGELOG_PAIRS`**; harness **§26Y**.
- **Architecture + decision (AC-10)** — **`DEC-0085`** + architecture **`# US-0100`**.

## Non-goals (explicit)

- No replacement of sprint-scoped **`handoffs/releases/Sxxxx-release-notes.md`**.
- No semver bump or per-version file this boundary (workflow-only release; **`release_version`** blank → **`[Unreleased]`** append only per step 19a).
- No publish execution (`RELEASE_PUBLISH_MODE=disabled`).

## Run

- **start_command**: `pytest -k us0100 tests/auto_command_contract_test.py -v`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md` § **Version-scoped release docs (US-0100 / DEC-0085)**

## Connect

- **service_url**: N/A (release documentation layer; no app runtime)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `pytest -k us0100 tests/auto_command_contract_test.py -v` → expect **10 passed** (26 subtests).
2. `python scripts/release_changelog_validate.py --repo .` → exit **0** (warn on unreleased-only stub pre-derivation; enforce post-derivation).
3. `python scripts/check_intake_template_parity.py --scope=release-changelog` → expect `[INTAKE_TEMPLATE_PARITY_OK]`.
4. `python scripts/check-user-visible-metadata.py --repo .` → exit **0**.
5. Confirm `CHANGELOG.md` contains **`## [Unreleased]`** with **US-0100** bullet after step 19 derivation.
6. Confirm `sprints/S0090/qa-findings.md` **PASS** and `sprints/S0090/uat.json` **10/10 PASS**.
7. Confirm release-queue row **`S0090`** is **`released`** and backlog / acceptance show **`US-0100`** = **DONE** / checked.
8. Confirm `.cursor/commands/release.md` step **19** (19a–19d) present in active + template mirrors.

- **expected_health_signal**: Contract tests green; validator OK; **`US-0100`** surfaces as **DONE** in backlog and checked in acceptance; **`[Unreleased]`** changelog entry present.

## Credentials

- Env-reference-only policy in effect. No inline secrets in changelog or version-doc artifacts.

## Test evidence summary

- **Contract subtests**: `pytest -k us0100` → **10 passed**, 26 subtests (release gate re-run).
- **Template parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=release-changelog.
- **Changelog validator**: `release_changelog_validate.py` exit 0 (warn pre-enforce on fresh stub; enforce post step 19).
- **Metadata guard**: `check-user-visible-metadata.py` exit 0.
- **UAT**: **10/10 PASS** (`sprints/S0090/uat.json`); UAT-10 procedural attestation per **DEC-0085** + architecture review.

## Governance references

- **DEC-0085** — artifact paths, derivation precedence, publish compose rules.
- **`docs/engineering/architecture.md`** `# US-0100`.
- **`docs/engineering/research.md`** `R-0087`.
- **`decisions/DEC-0085.md`**.

## Known Issues

- None blocking release for in-scope **US-0100** / **DEC-0085** delivery.
- **readme_feature_coverage_3f**: post-**S0077** portfolio drift on **`its_magic/README.md`** family — kit-repo observation per **S0085**/**S0086**/**S0087**/**S0088**/**S0089** precedent (disjoint from **US-0100** closure).
- **Full harness**: 25 pre-existing failures in `tests/run-tests.ps1` (809/25 baseline @ `tests/report.md` Timestamp=2026-06-13T10:33:17Z; non-blocking per QA/verify-work).

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (us0100 10/10; metadata guard harness rows PASS) |
| qa | pass (no blockers) |
| uat | pass (10/10; UAT-10 procedural attestation) |
| isolation | pass (execute+qa+verify-work distinct markers) |
| strict_proof | pass |
| parity | pass (scope=release-changelog) |
| readme_feature_coverage_3f | observation (post-S0077 drift; kit-repo) |
| project_readme_coverage_3g | pass (kit_repo_skipped) |
| metadata_guard | pass |
| version_doc_19 | pass ([Unreleased] append; enforce validate) |
| publish | skipped (RELEASE_PUBLISH_MODE=disabled) |
| finalization | pass |

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260615-01-release-release-20260615T080000Z-S0090-US0100`
- `proof_hash=92e55de82e4089435f4a6b3229e3233bbc2a4c4fd4aca5675313b8d7638d1d85`
- `fresh_context_marker=release-S0090-US0100-release-20260615T080000Z-fresh`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=disabled`, `ALLOW_AUTO_PUSH=1`; `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`.
- **Publish**: `RELEASE_PUBLISH_MODE=disabled` → `publish_snapshot=skipped_disabled` (deterministic no-op).

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **6** remaining.
