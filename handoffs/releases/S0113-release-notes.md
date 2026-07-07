# Sprint Release Notes — S0113

- **Sprint:** S0113
- **Story:** US-0113 — Sovereign-loop operator documentation in framework README
- **Release date (UTC):** 2026-07-04T03:00:00Z
- **Release date (calendar):** 2026-07-04
- **Orchestrator run:** auto-20260704-01
- **Delivery mode:** ultra_lean
- **Macro phase:** ship (release — first canonical phase)
- **Trigger source:** manual (`RELEASE_TRIGGER_SOURCE=manual`; no adapter subprocess)
- **Publish mode:** disabled (`RELEASE_PUBLISH_MODE=disabled`; deterministic no-op — `publish_snapshot=skipped_disabled`)
- **Sync policy:** disabled (`SYNC_POLICY_MODE=disabled` → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`)
- **Fresh context marker:** `release-S0113-US0113-20260704T030000Z-fresh`
- **Runtime proof id:** `rp-auto-20260704-01-release-release-20260704T030000Z-US-0113`

## Summary

Sovereign-loop operator documentation added to the framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`). Closes the operator-documentation gap for the sovereign-loop era features (US-0103–US-0112) by adding an `### Sovereign-loop era (US-0103–US-0112)` umbrella section under `## Commands and workflow` with 9 nested `#### US-xxxx` operator subsections, extending `### Full scratchpad reference (detailed)` with sovereign-loop keys, preserving the catalog anchors (US-0091), and keeping framework README byte-parity (US-0097/US-0017). Documentation-only; default-off posture preserved; zero new scratchpad keys; no code, scripts, installer, or canonical scratchpad touched.

## ACs satisfied

8/8 — AC-1 PASS, AC-2 PASS, AC-3 PASS, AC-4 PASS, AC-5 PASS, AC-6 PASS, AC-7 PASS, AC-8 PASS.

## Files shipped

- `its_magic/README.md` — umbrella `### Sovereign-loop era (US-0103–US-0112)` section + 9 nested `#### US-xxxx` operator subsections (US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112) + `### Full scratchpad reference (detailed)` extension with sovereign-loop keys.
- `template/its_magic/README.md` — byte-identical one-way copy from `its_magic/README.md` per AC-5.

## Compose guards

16 UNCHANGED: US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112. US-0113 lives entirely outside the compose surface (documentation-only).

## Test results

- **check_in_tests** (AC-8 proxy): `python -m pytest tests/scratchpad_example_parity_test.py -v` → 4 passed (parity_check, header_preserved, local_overrides_preserved, active_example_mirror_in_sync).
- **readme_feature_coverage** (AC-4): `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → exit 1 due to **pre-existing US-0117 gap** only (DC-1 deferred to US-0117 — out-of-scope for US-0113). `coverage_present` includes US-0103–US-0112; no new gaps introduced.
- **doc_profile** (AC-6): `python scripts/validate_doc_profile.py` → `[DOC_PROFILE_VALIDATE_OK]` (exit 0).
- **template_parity** (AC-5): `python scripts/check_intake_template_parity.py` → `[INTAKE_TEMPLATE_PARITY_OK] scope=intake` (exit 0).
- **byte-parity** (AC-5): `fc /b its_magic\README.md template\its_magic\README.md` → `FC_IDENTICAL` (no differences).
- **project_readme**: `FRAMEWORK_KIT_REPO=1` → skip project validator root check (kit repo). Framework README parity confirmed via AC-5 byte-identical.

## Gate chain

| Gate | Result | Notes |
|------|--------|-------|
| check_in_tests | PASS | 4/4 pytest PASS |
| qa | PASS | QA_PASS 8/8 ACs, 0 blockers (`sprints/S0113/qa-verdict.json`) |
| verify_work | PASS | VERIFY_WORK_PASS, ready_for_release=true (`sprints/S0113/verify-work-verdict.json`) |
| isolation_evidence | PASS | execute + qa + verify-work all proven (runtime_proof_ids present) |
| compose_guards | PASS | 16/16 UNCHANGED |
| readme_feature_coverage | PASS* | exit 1 ONLY on pre-existing US-0117 gap (DC-1 deferred — out-of-scope); no new gaps |
| project_readme | SKIP | `FRAMEWORK_KIT_REPO=1` (kit repo — skip root check); parity via AC-5 |
| doc_profile | PASS | `[DOC_PROFILE_VALIDATE_OK]` |
| template_parity | PASS | `[INTAKE_TEMPLATE_PARITY_OK]` |

\* Pre-existing US-0117 gap is the documented DC-1 deferral carried from research → architecture → sprint-plan. It is the next backlog-drain story in the 5-story decomposition (US-0117 = phase & role governance family) and will close that gap when it ships. Not a US-0113 blocker.

## Run

```bash
python -m pytest tests/scratchpad_example_parity_test.py -v
python scripts/validate_doc_profile.py
python scripts/check_intake_template_parity.py
python scripts/validate_readme_feature_coverage.py --repo . --enforce   # exit 1 expected — pre-existing US-0117 gap only
```

## Verify

- `fc /b its_magic\README.md template\its_magic\README.md` → no differences (byte-identical)
- `sprints/S0113/qa-verdict.json` → `verdict=QA_PASS`, 8/8 ACs
- `sprints/S0113/verify-work-verdict.json` → `verdict=VERIFY_WORK_PASS`, `ready_for_release=true`
- `sprints/S0113/release-verdict.json` → `verdict=RELEASE_PASS`

## Publish

`RELEASE_PUBLISH_MODE=disabled` — deterministic no-op. `publish_snapshot=skipped_disabled`.

## Sync (DEC-0018)

`SYNC_POLICY_MODE=disabled` → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`.

## Next

`/refresh-context` (curator, ship macro — second canonical phase) for segment closeout. Orchestrator Task-spawns the curator in a fresh subagent context. Remaining backlog-drain queue: US-0114, US-0115, US-0116, US-0117 (4 stories).