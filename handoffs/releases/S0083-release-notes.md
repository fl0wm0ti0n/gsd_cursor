# Release Notes — S0083 / US-0094 (README visionary intro + tiered feature hierarchy)

- **sprint_id**: S0083
- **story_refs**: US-0094
- **release_name**: `S0083 — US-0094 README visionary intro + tiered feature hierarchy (root/template parity)`
- **release_date**: 2026-06-07T16:30:00Z
- **orchestrator_run_id**: auto-20260607-01
- **verdict**: **PASS**
- **binding_decision**: none (architecture `# US-0094` + **R-0080**; composes **DEC-0074**, **DEC-0059**, **DEC-0078**)
- **research_anchor**: `R-0080`

## Summary

Rewrites the root README opening for autonomous AI dev team positioning: three discovery-locked intro paragraphs (dreamer + role-based team; artifact-first `/intake`→`/release` workflow; opt-in **`AUTO_FLOW_MODE=full_autonomy`** default-off + outer driver + `/auto` drain), four pillar `###` teaser sections under **`## Features`**, and preserved deep-detail body (`Setup`, `How-to`, `Commands and workflow`, walkthroughs, etc.). Three **`<!-- readme-feature-coverage-catalog -->`** blocks unchanged in affinity homes; **`coverage_missing=[]`**, **`coverage_total=104`**. **`README.md`** byte-copied to **`template/README.md`** (**US-0017**). **`docs/developer/README.md`** body unchanged (optional root cross-link only).

## What's new

- **Intro contract (AC-1)** — 3 paragraphs before `## Features`; 136 words; operator-as-dreamer + AI team roles; phased workflow + decision gates; full-autonomy opt-in headline with default-off pairing.
- **Tiered pillars (AC-2)** — Autonomous AI workflow | Quality & verification gates | Distribution & install | Operator control & ergonomics — id-free teaser bullets only; catalog blocks remain reference tier.
- **Detail preservation (AC-3)** — All deep body H2s retained below hierarchy; no silent operator-facing deletion.
- **Coverage re-audit (AC-4)** — `validate_readme_feature_coverage.py --report` and `--enforce` green post-edit.
- **Root/template parity (AC-5)** — SHA-256 `67EF3482A2D4A6FFDBD054DFA9AA854F76B8A739012E617615D9A51844E75918` both files.
- **Profile + metadata (AC-6, AC-7)** — `[DOC_PROFILE_VALIDATE_OK]`; metadata scanner exit 0 on changed surfaces.
- **Full-autonomy placement (AC-8)** — intro ¶3 primary; P1 pillar secondary; US-0092 catalog line tertiary.
- **Regression guards (AC-9)** — fixtures 3/3 OK; `--scope=readme-feature-coverage` parity OK; US-0030 delta gate unchanged.
- **DEV shard boundary (AC-10)** — no visionary intro in `docs/developer/README.md`; single-sentence root cross-link only.

## Non-goals (explicit)

- No **US-0091** validator semantic changes.
- No **DEC-0059** profile or USER_* H2 vocabulary changes.
- No **docs/developer/README.md** body rewrite.
- No release-gate wiring changes.

## Run

- **start_command**: `python scripts/validate_readme_feature_coverage.py --repo . --report`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md` (README feature coverage validation)

## Connect

- **service_url**: N/A (framework/toolkit repository; no running service)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `python scripts/validate_readme_feature_coverage.py --repo . --enforce`
   → expect `[README_FEATURE_COVERAGE_VALIDATE_OK]`; `coverage_missing=[]`, `coverage_total=104`.
2. `python scripts/validate_doc_profile.py --repo .`
   → expect `[DOC_PROFILE_VALIDATE_OK]`.
3. `python scripts/check-user-visible-metadata.py --repo .`
   → expect exit 0.
4. `python scripts/check_intake_template_parity.py --repo . --scope=readme-feature-coverage`
   → expect `[INTAKE_TEMPLATE_PARITY_OK]`.
5. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance`
   → expect `[BUG_VALIDATION_OK]`.
6. Confirm `sprints/S0083/qa-findings.md` PASS and `sprints/S0083/uat.json` 10/10 PASS.
7. Confirm release-queue row `S0083` is `released` and backlog / acceptance show `US-0094` = DONE / checked.

- **expected_health_signal**: All artifact checks above pass; `US-0094` surfaces as `DONE` in backlog and checked in acceptance.

## Credentials

- Env-reference-only policy in effect. No inline secrets in release artifacts.

## Test evidence summary

- **Canonical `tests/run-tests.ps1`**: Pass=**811** / Fail=**14** (`tests/report.md` Timestamp=2026-06-07T08:24:40Z). Fail=14 pre-existing disjoint.
- **readme_feature_coverage_3f**: `[README_FEATURE_COVERAGE_VALIDATE_OK]` live `--enforce` (release re-run).
- **Doc profile**: `[DOC_PROFILE_VALIDATE_OK]`.
- **Metadata guard**: exit 0.
- **Fixtures**: `readme_feature_coverage_fixtures_test.py` 3/3 OK.
- **Parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=readme-feature-coverage.
- **Bug validator**: `[BUG_VALIDATION_OK]` pre- and post-release-write.
- **UAT**: 10/10 PASS (`sprints/S0083/uat.json`, `sprints/S0083/uat.md`).

## Governance references

- **`docs/engineering/architecture.md`** `# US-0094`.
- **`docs/engineering/research.md`** `R-0080`.
- **DEC-0074** — feature coverage catalog (composed; not amended).
- **DEC-0059** — doc profile / USER_* H2 vocabulary.
- **US-0017** — root/template byte parity.

## Known Issues

- None blocking release. Pre-existing harness Fail=14 remains for separate triage.
- Prior `/release` attempt blocked on placeholder UAT — remediated by verify-work 10/10 PASS.

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (811/14; 14 pre-existing disjoint) |
| qa | pass (cycle 1) |
| uat | pass (10/10) |
| isolation | pass |
| strict_proof | pass |
| readme_feature_coverage_3f | pass (enforce=1; coverage_missing=[]) |
| bug_validate | pass |
| triad_check | pass (post-release rollover; pack_ref=docs/engineering/state-archive/state-pack-20260607-a.md) |
| finalization | pass |

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260607-01-release-release-20260607T163000Z-S0083-US0094`
- `proof_hash=1a245b9025a2d1acf19f5993e4ac7febfb8abc5c1bd75ad88a18e296c7c4dd00`
- `fresh_context_marker=release-S0083-US0094-release-20260607T163000Z-fresh`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=by_phase`, `ALLOW_AUTO_PUSH=1`, branch `main`; `push_decision=blocked`, `reason_code=TEST_FAILED` (canonical harness Fail=14; disjoint from US-0094).
- **Publish**: `RELEASE_PUBLISH_MODE=confirm` → `skipped_pending_operator_confirm`.

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories after US-0094 closure.
