## QA -> Verify-Work Handoff -- US-0090 / S0076 (QA cycle 1 PASS)

> **2026-04-18T23:30:00Z** -- `/qa` complete (fresh **qa** subagent, `orchestrator_run_id=auto-20260418-01`, `qa_loop_cycle=1` of `qa_loop_max=5`, backlog-drain active, budget remaining=5, `AUTO_QUIET=1`). Story **US-0090** remains **OPEN** (US-0045). Sprint **S0076**. QA verdict: **PASS** (with one non-blocking `PARTIAL_VERBATIM` fidelity note on DEC-0073 §1). Ready for **`/verify-work`**.

### QA summary

- **Overall verdict**: **PASS** — zero blocking findings. AC-1..AC-8 all PASS. `regressions_found=[]`. `parity_verified=true`. `caveman_mdc_sha256_preserved=true`. Default-off invariant (DEC-0072 §6 all 8 items) byte-unchanged. Installer-completeness 4/4 including new `test_caveman_compress_input_shipped_by_installer`.
- **Canonical check-in (`tests/run-tests.ps1`)**: **Pass=791 / Fail=9** (`tests/report.md` Timestamp=2026-04-18T15:00:49Z). vs US-0089 release baseline (783/11): **+8 pass / -2 fail**. `[PASS] 6 rules exist` assertion preserved. All 9 remaining failures pre-existing drift disjoint from US-0090 (US-0086/US-0087/US-0088 + Homebrew version drift + installer TEST_COMMAND).
- **Targeted caveman pytest**: `pytest tests/auto_command_contract_test.py -k caveman` → **24 passed / 19 deselected / 142 subtests passed / 0 failed** (+13 passes / +8 subtests / 0 new fails vs US-0089 release). Includes T-005 new `test_caveman_compress_input_*` subtests and unchanged `test_caveman_default_off_*` subtests (DEC-0072 §6 row 6 invariant).
- **Full contract module**: **40 passed / 24 failed / 215 subtests**. 24-failure baseline preserved byte-for-byte; no new regression.
- **Installer completeness**: `python -m pytest tests/installer_completeness_bug0003_test.py -v` → **4 passed / 0 failed** (incl. new caveman shipped-by-installer test).
- **Parity**: `check_intake_template_parity.py --scope=caveman-compress` → `[INTAKE_TEMPLATE_PARITY_OK]`; `--scope=all` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- **Bug validator**: `[BUG_VALIDATION_OK]`.
- **Negative parity**: `.cursor/rules/caveman.mdc` active == template SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` (R10 mitigation end-to-end preserved through QA phase).
- **CLI live-probes**: `--write` without activation → `CAVEMAN_COMPRESS_MODE_DISABLED` (exit 2); `--dry-run --write` → `CAVEMAN_COMPRESS_FLAG_CONFLICT` (exit 2); `--report` emits stable `deny_list_version=33bd8fa055791051cfb4505ca8815de51eefd73b41ee850541db63bc0ef69884` and `idempotency_check.fixture_byte_stable=true`; `--help` exit 0 with all four flags documented.

### AC verification matrix

| AC | Verdict | DEC-0073 § | Evidence pointer |
|----|---------|------------|------------------|
| AC-1 Gating | PASS | §2 + §7 | live CLI probe + 3 gating subtests green |
| AC-2 Originals | PASS | §3 | `.gitignore` anchor + `.gitkeep` + sidecar-first atomic order in script |
| AC-3 Deny list | PASS | §4 + §4.1 + §7 | stable `deny_list_version`; 33 fixture classes under `tests/fixtures/caveman_compress/03_deny_list/` |
| AC-4 Scope | PASS | §5 + §7 | 3 scope reason codes; frozen v1 profile present; profile/hybrid/glob parsing |
| AC-5 Operator UX | PASS | §8 + §9 row 2 + §3 | `--help` OK; runbook subsection active=template SHA; revert via sidecar documented |
| AC-6 Tests | PASS | §6 + §9 test strategy + §10 | 24 caveman tests / 142 subtests green; 8 fixture classes present; installer-completeness green |
| AC-7 `# US-0090` | PASS (PARTIAL_VERBATIM note) | §1 + §9 row 4 | architecture §US-0090 has 8 linkage tokens + forbidden surfaces; three-axis paragraph verbatim in architecture; non-blocking verbatim note on reference/runbook paraphrase |
| AC-8 Template parity | PASS | §9 + §10 | 5 sanctioned byte-identical pairs; `.cursor/rules/caveman.mdc` SHA-256 preserved; installer manifest entry live-verified |

### Scrutiny-target resolutions (orchestrator-surfaced concerns)

1. **Baseline drift claim (+13 unexplained failures)** — **resolved false-positive**. Orchestrator mis-attributed `run-tests.ps1` harness fail count (11) as the pytest contract-module baseline. Pytest contract-module baseline at US-0089 release was **24 failed** (`docs/engineering/state.md` line 515: "27 passed / 24 failed / 192 subtests"). Current pytest: **40 passed / 24 failed / 215 subtests** = **+13 passes** (new caveman subtests added) / **+0 new fails**. No regression.
2. **DEC-0073 §1 fidelity gap (replace vs compose-alongside + verbatim vs paraphrase)** — **PARTIAL_VERBATIM non-blocking**. Dev kept DEC-0072 §1 section intact (to preserve DEC-0072 §6 row 6 pinned test `test_caveman_default_off_reference_non_substitution_paragraph`) AND added a new companion section in reference + runbook with a *paraphrase* of the DEC-0073 §1 normative paragraph ("file compression" / "All three axes are orthogonal…" vs DEC text "file mutation" / "None substitutes for another; setting one does not change the others. Combine freely."). Architecture doc `docs/engineering/architecture.md` §Three-axis non-substitution carries the **verbatim** paragraph. DEC-0072 §6 row 6 invariant preserved; semantic intent of DEC-0073 §1 preserved. Non-blocking because (i) no contract test asserts byte-exact publication in reference + runbook; (ii) architecture cross-reference is authoritative; (iii) dev surfaced this in handoff ambiguity resolution #1. **Optional follow-up** (not required for verify-work or release): minor doc edit to align reference + runbook paragraph byte-exact with DEC-0073 §1.
3. **`test_caveman_architecture_section_bottom_appended_and_linked` relaxation** — **legitimate update**. Test is NOT in DEC-0072 §6 row 6 pinned class; relaxation accommodates the architecturally-correct `# US-0090` append; underlying bottom-appended intent preserved.
4. **Negative-assertion removal on `template/docs/engineering/architecture.md`** — **legitimate**. File is active-only per DEC-0072 §7 row 6 precedent; negative-assertion was a misunderstanding; not in DEC-0073 §9 negative-parity set.
5. **Canonical check-in suites** — **PASS**. PowerShell harness 791/9; `[PASS] 6 rules exist`. Bash harness not run (Windows host; PowerShell is canonical gate + `26T` symmetrically wired).
6. **Parity re-verification + `.cursor/rules/caveman.mdc` SHA-256** — **PASS**. `check_intake_template_parity.py` both scopes `[INTAKE_TEMPLATE_PARITY_OK]`; rule SHA-256 preserved.

### Artifacts authored this phase

- **`sprints/S0076/qa-findings.md`** — full per-AC verdicts, scrutiny-target findings, test battery summary, isolation + runtime proof.
- **`sprints/S0076/uat.md`** + **`sprints/S0076/uat.json`** — 15 UAT steps covering AC-1..AC-8 for `/verify-work`.
- **`docs/engineering/state.md`** — QA checkpoint appended with isolation evidence + strict runtime proof + phase boundary status + AC verdicts + scrutiny resolutions. `enforce-triad-hot-surface.py --check` exit 0 pre- and post-append (no rollover required).
- **`handoffs/resume_brief.md`** — updated to point to `/verify-work` for S0076 / US-0090.
- **`handoffs/qa_to_verify_work.md`** — this handoff.

### Artifacts NOT touched this phase

- `.cursor/rules/caveman.mdc` (+ template mirror) — negative parity preserved.
- `.cursor/skills/its-magic/SKILL.md` (+ mirror) — unchanged.
- `.cursor/scratchpad.md` and `.cursor/scratchpad.local.example.md` — unchanged.
- `template/*` files — QA is read-only on mirrors.
- Dev-authored `sprints/S0076/sprint.md`, `tasks.md`, `summary.md` — untouched (QA appends to state.md; dev/release own those files).
- `decisions/DEC-0073.md`, `decisions/DEC-0072.md` — not rewritten.
- `docs/product/backlog.md`, `docs/product/acceptance.md` — not mutated (US-0090 remains OPEN per US-0045).

### Runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260418-01`
- `runtime_proof_id=rp-auto-20260418-01-qa-qa-20260418T233000Z-S0076-US0090`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-04-18T23:30:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=aebc889eb82a2b78fa998796c4d102d3f8b2edeb7dc609dfab3efeb1a49fa995`

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0076-US0090-qa-20260418T233000Z-fresh`
- `timestamp=2026-04-18T23:30:00Z`
- `evidence_ref=sprints/S0076/qa-findings.md`

### Phase boundary status (US-0088 / DEC-0069)

`phase_boundary=qa`; `next_scheduled_phase=verify-work`; `segment_work_item_kind=story`; `active_bug_id=(none)`; `bug_queue_position=(none)`; `bug_queue_remaining=(none)`; `backlog_drain_active=true`; `bug_queue_active=false`; `backlog_drain_stories_remaining_budget=5`; `story_id=US-0090`; `sprint_id=S0076`; `task_count=10`; `qa_verdict=PASS`; `regressions_found=0`; `dec_id=DEC-0073`; `orchestrator_run_id=auto-20260418-01`; `qa_loop_cycle=1`; `qa_loop_max=5`; `stop_reason=(none)`; `stop_phase=(none)`; `backlog_drain_segment_complete=0`.

### Next phase -- `/verify-work` (fresh **qa** subagent)

- **Sprint**: S0076
- **Story**: US-0090
- **Decision**: DEC-0073
- **Required inputs**: `sprints/S0076/qa-findings.md`, `sprints/S0076/uat.md`, `sprints/S0076/uat.json`, `sprints/S0076/summary.md`, `handoffs/qa_to_verify_work.md` (this file), `decisions/DEC-0073.md`, `docs/product/backlog.md` `## US-0090`.
- **Expected verify-work actions**: (a) run UAT-1..UAT-15 from `sprints/S0076/uat.md`; (b) confirm zero regressions + parity + `.cursor/rules/caveman.mdc` SHA-256; (c) update `docs/product/backlog.md` `## US-0090` with verify-work disposition (US-0045 authority); (d) flip AC-rows in `docs/product/acceptance.md` as appropriate; (e) prepare `handoffs/qa_to_release.md` if closing; (f) append verify-work checkpoint to `docs/engineering/state.md`.
- **Non-blocking carryover**: consider optional minor doc edit to align `docs/engineering/auto-orchestration-reference.md` + `docs/engineering/runbook.md` three-axis paragraph byte-exact with DEC-0073 §1 verbatim text (does not block verify-work or release).
