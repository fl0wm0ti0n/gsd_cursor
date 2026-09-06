# Release Findings — BUG-0015 / S0131

- sprint_id: S0131
- story_id: BUG-0015
- bug_id: BUG-0015
- phase_id: release
- role: release (fresh per BUG-0006)
- orchestrator_run_id: auto-20260906-bug0015
- delivery_mode: ultra_lean
- macro_phase: ship (release is phase 1 of 3: release → closure → refresh-context per DEC-0082)
- fresh_context_marker: release-BUG0015-release-rerun-20260906T153000Z-fresh
- timestamp: 2026-09-06T15:30:00Z (UTC)
- model_id: composer-2.5 (CROSS_MODEL_REVIEW=1 — required on isolation)
- RELEASE_PUBLISH_MODE: confirm (no publish — RELEASE_PUBLISH_AUTO_CONFIRM=0)
- RELEASE_PUBLISH_AUTO_CONFIRM: 0
- SYNC_POLICY_MODE: disabled
- release attempt: **2nd** (re-run after sovereign-critic `ik_bug0015_release_gate1_fail_nonzero` + Homebrew remediation)

## Verdict

**PASS** — all mandatory release gates (1, 2, 3, 4, 4b) green with **canonical harness Fail:0**. Queue row S0131 remains/kept `released` (idempotent). No backlog mutation (closure owns OPEN→DONE + acceptance tick per US-0120 / DEC-0082). No publish (`RELEASE_PUBLISH_MODE=confirm` + `RELEASE_PUBLISH_AUTO_CONFIRM=0` → `PUBLISH_CONFIRMATION_REQUIRED` / deterministic no-op). Critic issue_key `ik_bug0015_release_gate1_fail_nonzero` resolved via `resolve_finding` (3 rows → `status=resolved`).

## Prior attempt (superseded)

Attempt 1 @ `2026-09-06T15:15:00Z` claimed RELEASE_PASS with `tests/report.md` Pass:846 / **Fail:3** and `harness_fail_zero_claimed=false`. Sovereign-critic blocked (`ik_bug0015_release_gate1_fail_nonzero`). Dev remediation synced Homebrew formula to `0.1.3-6` and confirmed Active context surface; harness re-run → Pass:849 / Fail:0 @ `2026-09-06T15:28:42Z`.

## Gate table

| # | Gate | Result | Reason code(s) | Evidence |
|---|------|--------|----------------|----------|
| 1 | Check-in test | **PASS** | — | Live `python -m pytest tests/bug0015_contract_test.py -v` → **7 passed in 0.69s**; us0124 12/12; parity `--scope=bug-0015` OK; US-0071 metadata OK; **`tests/report.md` @ `2026-09-06T15:28:42Z` Pass:849 / Fail:0** (zero `[FAIL]` rows); Homebrew url+version match npm `0.1.3-6`; `harness_fail_zero_claimed=true` |
| 2 | QA completion | PASS | — | `sprints/S0131/qa-findings.md` verdict QA_PASS; `blocking_count=0`; NB-1..NB-3 informational |
| 3 | UAT completion | PASS | — | `sprints/S0131/uat.json` verify_work verdict=PASS, total=9, passed=9, failed=0 incl. `convergence_smoke`; `sprints/S0131/uat.md` populated 9/9 (DEC-0009) |
| 4 | Isolation compliance | PASS | — | execute + execute-remediation + qa + verify-work + sovereign-critic (release FAIL) + this release re-run; distinct `fresh_context_marker`; `model_id` set per phase |
| 4b | Strict runtime proof | PASS | — | Verify-work proof `rp-auto-20260906-bug0015-verify-work-qa-20260906T150500Z-BUG-0015` (proof_hash=`165F812E5357B9DC0BF07AC07628F96D62BB10DFA2056F7EA2C97ADE8C5A4117`, proof_ttl=`2026-09-06T16:05:00Z`) consumed at release re-run `15:30:00Z` before expiry; hash independently recomputed MATCH; NEW release proof minted (no proof_id reuse) |
| 5 | Release finalization | **PASS** | — | `handoffs/releases/S0131-release-notes.md` refreshed PASS; queue row S0131 = `released` (idempotent) |

## Doc gates

| Gate | Result | Notes |
|------|--------|-------|
| readme_feature_coverage_3f | **PASS** | `python scripts/validate_readme_feature_coverage.py --repo . --enforce` exit 0; `coverage_missing=[]`; BUG-0015 OPEN — excluded |
| project_readme_3g | skipped | `FRAMEWORK_KIT_REPO=1` per S0114..S0130 precedent |
| metadata_guard (US-0071) | PASS | `python scripts/check-user-visible-metadata.py --repo .` exit 0 |
| version_doc_17 | skipped | workflow-only release; no semver bump (`RELEASE_CHANGELOG_VALIDATE_WARN` expected without queue semver) |
| triad_regression | PASS | `enforce-triad-hot-surface.py --check` exit 0; Active context surface preamble present |

## Harness re-run decision

**Accepted post-remediation harness** @ `2026-09-06T15:28:42Z` → **`Pass: 849 / Fail: 0`**. Live contract slice re-confirmed this spawn (bug0015 7/7 @ 0.69s). Gate-1 PASS rests on **Fail:0** canonical report + slice + compose + parity + metadata.

## Critic remediation

| issue_key | finding_ids | prior status | action | new status |
|-----------|-------------|--------------|--------|------------|
| `ik_bug0015_release_gate1_fail_nonzero` | b0015rel-challenger-001, b0015rel-architect-002, b0015rel-subtractor-003 | open (blocking) | `scripts.sovereign_critic_lib.resolve_finding(..., "resolved")` after Fail:0 evidence | **resolved** |

## Compose guards (UNCHANGED)

DEC-0124 / DEC-0125 bodies UNCHANGED; `test_us0124_*` / `test_us0125_*` not amended; BUG-0016 / US-0131 / US-0132 out of scope; backlog ### BUG-0015 Status OPEN L4899; acceptance L180 unchecked; intake JSON not mutated.

## Strict runtime proof (release attempt 2)

- `runtime_proof_id=rp-auto-20260906-bug0015-release-release-20260906T153000Z-BUG-0015`
- `proof_hash=1467A9436D9012A5974AC13C269E28EDFA1D1E9821BA3C94422E1DAB4D8FAD00`
- `proof_ttl=2026-09-06T16:30:00Z`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"ship","model_id":"composer-2.5","orchestrator_run_id":"auto-20260906-bug0015","phase_id":"release","proof_issued_at":"2026-09-06T15:30:00Z","proof_ttl_seconds":3600,"role":"release","runtime_proof_id":"rp-auto-20260906-bug0015-release-release-20260906T153000Z-BUG-0015","sprint_id":"S0131","story_id":"BUG-0015"}`
- Consumed verify-work proof: `rp-auto-20260906-bug0015-verify-work-qa-20260906T150500Z-BUG-0015` (hash `165F812E5357B9DC0BF07AC07628F96D62BB10DFA2056F7EA2C97ADE8C5A4117` — recomputed MATCH; ttl `2026-09-06T16:05:00Z` — consumed at `15:30:00Z` before RUNTIME_PROOF_STALE)

### Lifecycle proofs (present)

| Phase | runtime_proof_id | proof_hash |
|-------|------------------|------------|
| execute | `rp-auto-20260906-bug0015-execute-dev-20260906T144500Z-BUG-0015` | `1E8BF77730FB73CD94657EA5A0287E8F769F31C0CCD2EF81370181AD641D9CB0` |
| execute (remediation) | `rp-auto-20260906-bug0015-execute-remediation-dev-20260906T152500Z-BUG-0015` | `A1CBD004604C473F8BAB2D6EE007CA18B31F29E316901351B30A1C6FBCAB55C1` (per summary) |
| qa | `rp-auto-20260906-bug0015-qa-qa-20260906T145500Z-BUG-0015` | `B2924E1E4F3B1E750491884C7F1226E6DA15F24C9421333914394386AA4E35FB` |
| verify-work | `rp-auto-20260906-bug0015-verify-work-qa-20260906T150500Z-BUG-0015` | `165F812E5357B9DC0BF07AC07628F96D62BB10DFA2056F7EA2C97ADE8C5A4117` |
| release (attempt 1, superseded) | `rp-auto-20260906-bug0015-release-release-20260906T151500Z-BUG-0015` | `DB3A4169B06633D5EDA241D9243744170EF259600B7C406EB629322D5D68BC00` |
| release (attempt 2) | `rp-auto-20260906-bug0015-release-release-20260906T153000Z-BUG-0015` | `1467A9436D9012A5974AC13C269E28EDFA1D1E9821BA3C94422E1DAB4D8FAD00` |

## Publish / sync snapshot

- `publish_snapshot=skipped_pending_operator_confirm` (`RELEASE_PUBLISH_MODE=confirm`, `RELEASE_PUBLISH_AUTO_CONFIRM=0` → `PUBLISH_CONFIRMATION_REQUIRED`)
- `push_decision=not_eligible` (`SYNC_POLICY_MODE=disabled` → `reason_code=SYNC_DISABLED`)

## Evidence refs

- `handoffs/releases/S0131-release-notes.md`
- `handoffs/release_queue.md` (S0131 row)
- `handoffs/release_notes.md` (legacy pointer — attempt-2 note prepended)
- `docs/engineering/state.md` (release re-run checkpoint + isolation)
- `handoffs/resume_brief.md` (prepended /closure handoff)
- `handoffs/sovereign_critic_findings.jsonl` (`ik_bug0015_release_gate1_fail_nonzero` → resolved)
- `sprints/S0131/qa-findings.md`
- `sprints/S0131/uat.json`, `sprints/S0131/uat.md`
- `sprints/S0131/summary.md` (incl. Homebrew remediation)
- `tests/report.md` (@ 2026-09-06T15:28:42Z — Fail:0)

## Next phase

`/closure` (fresh **qe** subagent) — backlog OPEN→DONE, acceptance tick L180, `sprints/S0131/closure-verification.md`. Release does NOT spawn closure.
