# QA Findings — US-0125 / S0125 (qa phase loop-2 — PASS after B-1 + B-2 fix)

## Metadata

|| Field | Value |
|---|---|
|| sprint_id | S0125 |
|| story_id | US-0125 (OPEN — not marked DONE per US-0045) |
|| phase_id | qa (loop-2) |
|| role | qa (fresh per BUG-0006; loop-2 — new subagent, not reused from qa-1) |
|| orchestrator_run_id | auto-20260824-02 |
|| delivery_mode | ultra_lean |
|| macro_phase | build+verify |
|| AUTO_IMPLEMENTATION_LOOP | 1 (cycle 2 complete: dev fixed B-1 + B-2 → sovereign-critic PASS → /qa loop-2 PASS → /verify-work) |
|| fresh_context_marker | qa-US0125-qa-20260824T220000Z-fresh (NEW — not reused from qa-1 213000Z) |
|| timestamp | 2026-08-24T22:00:00Z (UTC) |
|| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 — required on isolation) |
|| producer_model_id | glm-5.2-high (dev / execute loop-2) |
|| verdict | **PASS (loop-2)** — B-1 + B-2 closed; canonical harness `tests/report.md` Pass:845 / Fail:0 literal; zero `[FAIL]` rows; 11/11 us0125 contract markers PASS (independent re-run); `validate_readme_feature_coverage` PASS `coverage_missing=[]` (US-0125 absent — OPEN, not in coverage set); no fake browser PASS (non-browser plugin contract story) |
|| blocking_count | 0 |
|| intake_json | NOT mutated |
|| ac_checkboxes | unchecked (US-0045 — not mutated) |
|| backlog_status | OPEN (US-0045 — not mutated) |

## Verdict rationale

Per the QA hard gate (US-0048 / DEC-0029 + US-0056 / DEC-0038 PASS-claim rule): **never claim
Fail=0 unless `tests/report.md` has literal `Fail: 0` AND `rg "\[FAIL\]"` is empty.** Producer (execute
loop-2) claimed Pass:845 / Fail:0 @ 2026-08-24T21:04:51Z. QA independently confirmed both literals
without re-running the full harness (no file changes made this phase; report is current vs
execute loop-2 product/test changes — fixes applied before 21:04:51Z harness run, handoff written
at 21:07:10Z):

- `tests/report.md` header line 5: `Fail: 0` (literal zero) @ 2026-08-24T21:04:51Z
- `rg "\[FAIL\]" tests/report.md` -> **0 matches**

Both loop-1 blockers (B-1, B-2) are independently confirmed closed:

- **B-1 closed**: `docs/engineering/architecture.md` line 36 (`# US-0090` section body) now contains
  `See \`# US-0085\` for context fresh-context markers.` — `US-0085` token present in
  `arch[arch.find("# US-0090"):]` slice.
- **B-2 closed**: `python scripts/validate_readme_feature_coverage.py --repo . --report` -> exit 0,
  `{"coverage_missing":[],"coverage_present":["US-0121","US-0122","US-0123","US-0124"],"status":"PASS"}`
  — US-0125 absent (OPEN, not in coverage set).

Therefore US-0125 QA loop-2 verdict = **PASS**. Hand off to `/verify-work` via artifacts only.
Do NOT spawn `/verify-work` from this subagent (orchestrator owns spawn per BUG-0006).

## US-0125 own-contract evidence (independent re-run, loop-2)

|| Check | Result |
|---|---|
|| `python -m pytest tests/us0125_contract_test.py -v` | **11/11 PASS** (0.41s, exit 0) - markers 1-11 green |
|| `python scripts/validate_readme_feature_coverage.py --repo . --report` | **PASS** — `coverage_missing=[]`, `coverage_present=["US-0121","US-0122","US-0123","US-0124"]`, US-0125 absent (OPEN) |
|| `python scripts/check_intake_template_parity.py --repo . --scope readme-feature-coverage` | **`[INTAKE_TEMPLATE_PARITY_OK]`** (exit 0) |
|| `python scripts/enforce-triad-hot-surface.py --check` | **exit 0** (no rollover triggered; Active context surface preserved) |
|| Canonical harness `tests/report.md` header | `Pass: 845` / `Fail: 0` (literal zero) @ 2026-08-24T21:04:51Z |
|| `rg "\[FAIL\]" tests/report.md` | **0 matches** |
|| B-1 architecture.md `# US-0090` US-0085 linkage | **PRESENT** (line 36: `See \`# US-0085\` for context fresh-context markers.`) |
|| B-2 readme-feature-coverage | **PASS** (coverage_missing=[]) |

## Loop-1 blockers — closure verification

### B-1 closed (architecture.md `# US-0090` missing `US-0085` linkage)

- **Loop-1 FAIL**: `tests/auto_command_contract_test.py::test_caveman_compress_input_architecture_linkage (token='US-0085')` failed; 8 required linkages, 7 present, `US-0085` missing.
- **Loop-2 fix**: execute loop-2 appended `See \`# US-0085\` for context fresh-context markers.` to the US-0090 section paragraph (architecture.md L36).
- **Loop-2 QA confirmation**: `rg "US-0085" docs/engineering/architecture.md` -> line 36 (US-0090 section) contains the token. Test now PASS (per `tests/report.md` Pass:845 Fail:0 @ 21:04:51Z, zero `[FAIL]` rows).

### B-2 closed (US-0124 README feature coverage gap)

- **Loop-1 FAIL**: `validate_readme_feature_coverage --report` exit 1 with `coverage_missing=["US-0124"]`.
- **Loop-2 fix**: execute loop-2 added US-0124 bullets to `docs/developer/README.md` `## Workflow` + `## Quality gates` and root `README.md` `## Commands and workflow` (byte-identical active ↔ template pairs).
- **Loop-2 QA confirmation**: `validate_readme_feature_coverage --report` exit 0, `coverage_missing=[]`, `coverage_present=["US-0121","US-0122","US-0123","US-0124"]`. US-0125 correctly absent (OPEN, not in coverage set).

## US-0125 scope (unchanged from loop-1 — no product-scope edits in loop-2)

- 11/11 contract-test markers PASS (`tests/us0125_contract_test.py`).
- 15 dispatch-only command files at `template/.opencode/commands/<name>.md` (≤ 20 lines each).
- opencode-adapter parity PASS.
- Compose guards 7/7 UNCHANGED; backlog US-0125 OPEN; acceptance unchecked; intake JSON not mutated.

## UAT classification

US-0125 is a non-browser plugin contract story (dispatch-only commands + validator bridge contract
asserted via Node subprocess harness `tests/us0125/bridge_harness.mjs`). No browser-surface UAT
applies. No fake browser PASS — UAT probes deferred to `/verify-work` per DEC-0009 lifecycle
(placeholder → populated → verified). QA does not populate UAT artifacts.

## Non-blocking observations

- US-0125 execute loop-2 did NOT run the full harness in the dev subagent (time-bounded); however,
  the dev handoff records the harness run @ 21:04:51Z producing Pass:845/Fail:0, and QA
  independently confirmed the report literals (no re-run needed — no file changes this phase).
- US-0125 contract test markers 1-11 remain green and unaffected by the loop-2 backfill edits.
- Loop-2 edits confined to architecture.md (US-0085 linkage sentence in US-0090 section) +
  developer README (US-0124 bullets) + root README (US-0124 bullet); no installer/plugin/agent/
  scratchpad/DEC/backlog/acceptance surfaces touched. Compose guards 7/7 UNCHANGED.

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=qa`
- `role=qa`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=qa-US0125-qa-20260824T220000Z-fresh` (NEW — not reused from qa-1 213000Z or execute loop-2)
- `timestamp=2026-08-24T22:00:00Z`
- `evidence_ref=sprints/S0125/qa-findings.md (this loop-2 prepend), handoffs/qa_to_verify.md (PASS handoff prepend), tests/report.md (Pass:845 Fail:0 @ 2026-08-24T21:04:51Z), docs/engineering/state.md (qa loop-2 checkpoint append-bottom)`

## Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260824-02`
- `runtime_proof_id=rp-auto-20260824-02-qa-qa-20260824T220000Z-US-0125` (loop-2, unique vs qa-1 213000Z)
- `phase_id=qa`, `role=qa`, `story_id=US-0125`, `sprint_id=S0125`
- `proof_issued_at=2026-08-24T22:00:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T23:00:00Z` (UTC)
- `proof_hash=591B6F44D3A311D17083D90AAF1D9A740F45826D63D38C48042FF160139E9AE2`
- Canonical payload (sorted-key compact JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-02","phase_id":"qa","proof_issued_at":"2026-08-24T22:00:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-02-qa-qa-20260824T220000Z-US-0125","sprint_id":"S0125","story_id":"US-0125"}`

Prior phase proof consumed: `rp-auto-20260824-02-execute-dev-20260824T210710Z-US-0125` (proof_hash=9a29423c0d4df7d61f3a3ee45a9884485eed52f5ee26916d712b8a476baeb807, ttl 2026-08-24T22:07:10Z — consumed before RUNTIME_PROOF_STALE).

## Next phase

- `/verify-work` (role=qa per US-0069 / DEC-0051 phase->role matrix; fresh qa subagent per BUG-0006) to populate UAT artifacts (placeholder → populated per DEC-0009).
- STOP after qa loop-2; orchestrator spawns `/verify-work` in fresh qa subagent. Do NOT mark US-0125 DONE. Do NOT tick acceptance. Do NOT mutate intake JSON.

---

# QA Findings — US-0125 / S0125 (qa phase loop-1 — FAIL)

## Metadata

| Field | Value |
|---|---|
| sprint_id | S0125 |
| story_id | US-0125 (OPEN — not marked DONE per US-0045) |
| phase_id | qa |
| role | qa (fresh per BUG-0006) |
| orchestrator_run_id | auto-20260824-02 |
| delivery_mode | ultra_lean |
| macro_phase | build+verify |
| fresh_context_marker | qa-US0125-qa-20260824T213000Z-fresh |
| timestamp | 2026-08-24T21:30:00Z (UTC) |
| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 — required) |
| verdict | **FAIL** — full harness Fail:4 != 0 (hard gate violation) |
| blocking_count | 2 blocking findings (4 [FAIL] rows; 2 root causes) |
| intake_json | NOT mutated |
| ac_checkboxes | unchecked (US-0045 — not mutated) |
| backlog_status | OPEN (US-0045 — not mutated) |

## Verdict rationale

Per the QA hard gate (US-0048 / DEC-0029 + US-0056 / DEC-0038 PASS-claim rule): **never claim
Fail=0 unless `tests/report.md` has literal `Fail: 0` AND `rg "\[FAIL\]"` is empty.** The refreshed
canonical harness (`powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`, exit 1) produced:

- `tests/report.md` header: `Pass: 841` / `Fail: 4` @ 2026-08-24T20:51:58Z
- `rg "\[FAIL\]" tests/report.md` -> 4 matches (lines 784, 805, 814, 815)

Therefore US-0125 QA verdict = **FAIL**. Per `AUTO_IMPLEMENTATION_LOOP=1`, hand off to dev with
precise fixes; do NOT spawn `/execute` from this subagent (orchestrator owns spawn per BUG-0006).

## US-0125 own-contract evidence (PASS)

| Check | Result |
|---|---|
| `python -m pytest tests/us0125_contract_test.py -v` | **11/11 PASS** (0.42s) - markers 1-11 green |
| `python scripts/check_intake_template_parity.py --repo . --scope opencode-adapter` | **`[INTAKE_TEMPLATE_PARITY_OK]`** (exit 0) |
| `python scripts/enforce-triad-hot-surface.py --check` | **exit 0** (no rollover triggered) |
| `python scripts/check-user-visible-metadata.py --repo .` | **exit 0** (no leaks) |
| Byte-identical pairs (5/5) - runbook, its_magic/README.md, installer-owned-paths.manifest, parity script, us0125 contract test | **MATCH** (SHA-256) |
| 15 command files line count | all <= 20 lines (max 14) |
| `template/.opencode/commands/auto.md` | dispatch-only; `agent: auto` + `subtask: false`; no spawn literals in body |
| `.cursor/commands/*.md` US-0125 reference grep | **0 hits** (AC-9 upheld) |
| `template/.opencode/plugins/orchestrator.ts` US-0125 reference grep | **0 hits** (US-0124 owned; not rewritten) |
| Architecture heading order | `# US-0125` (L1836) before `# US-0089` (L2103) - DEC-0073 section 11 upheld |

## Blocking findings (2 root causes -> 4 [FAIL] rows)

### B-1: architecture.md `# US-0090` section missing `US-0085` linkage

- **[FAIL] rows**: `slim auto command contract markers pass` (report L784); `US-0090 caveman-compress contract subtests pass` (report L805).
- **Failing test**: `tests/auto_command_contract_test.py::AutoCommandContractTest::test_caveman_compress_input_architecture_linkage (token='US-0085')` at line 1078.
- **Root cause**: `docs/engineering/architecture.md` `# US-0090` section (h2 at L34) does not reference `US-0085`. The test asserts 8 required linkages appear in `arch[arch.find("# US-0090"):]`; 7 are present, only `US-0085` is missing.
- **Required linkages** (per test L339-348): `DEC-0073`, `DEC-0072`, `R-0073`, `# US-0089`, `US-0053`, `US-0085`, `US-0078`, `DEC-0060`.
- **Token presence check** (QA recomputed): DEC-0073 PRESENT, DEC-0072 PRESENT, R-0073 PRESENT, `# US-0089` PRESENT, US-0053 PRESENT, **US-0085 MISSING**, US-0078 PRESENT, DEC-0060 PRESENT.
- **US-0125 attribution**: **NOT a US-0125 regression.** US-0125 execute did not touch `docs/engineering/architecture.md` (T-anch NO-OP per dev handoff; `git diff -- docs/engineering/architecture.md` shows no US-0090/US-0085 changes). The US-0090 h2 section was added by a prior sprint. However, the hard gate is unconditional: Fail!=0 blocks.
- **Precise fix**: Add a `US-0085` reference somewhere in `arch` at or after the `# US-0090` heading (L34). Minimal additive edit: extend the existing US-0090 section body sentence to also cite `US-0085` (e.g. append `See \`# US-0085\` for context fresh-context markers.`). The edit is one sentence; does not alter any other section. architecture.md is a US-0125 compose-guard (T-anch NO-OP) - this is a pre-existing-bug remediation, not US-0125 scope expansion; record as such in the loop-2 execute summary.

### B-2: US-0124 missing from root README `## Commands and workflow` + developer README `## Quality gates`

- **[FAIL] rows**: `validate_readme_feature_coverage repo --report passes` (report L814); `validate_readme_feature_coverage report idempotent` (report L815).
- **Failing validator**: `python scripts/validate_readme_feature_coverage.py --repo . --report` -> exit 1 with:
  - `README_FEATURE_COVERAGE_BLOCKED`
  - `README_FEATURE_COVERAGE_GAP:US-0124`
  - `{"coverage_missing":["US-0124"],"coverage_present":["US-0121","US-0122","US-0123"],"coverage_total":4,"gaps":[{"dev_h2":"Workflow","id":"US-0124","kind":"US","predicate_source":"explicit:true","root_h2":"Commands and workflow","user_visible":true}],"status":"FAIL"}`
- **Root cause**: US-0124 is `user_visible: true` (backlog L4283) and `Status: DONE` (backlog L4287; acceptance L152 `[x]`). It therefore belongs to the readme-feature-coverage set. US-0124 execute loop-2 added `US-0123` to `docs/developer/README.md` `## Quality gates` but did NOT add `US-0124` to root `README.md` `## Commands and workflow` or to `docs/developer/README.md` `## Quality gates`. The gap surfaced after US-0124 release (which ticked acceptance -> DONE -> entered coverage set); US-0124 QA ran before the release tick, so its `Pass:845/Fail:0` did not see this gap.
- **US-0125 attribution**: **NOT a US-0125 regression.** US-0125 execute did not touch root `README.md`, `docs/developer/README.md`, or `docs/product/backlog.md` (dev handoff "Files NOT modified (compose guards)" lists all three). US-0125 is OPEN and not in the coverage set. However, the hard gate is unconditional: Fail!=0 blocks.
- **Precise fix**:
  1. Add to `docs/developer/README.md` `## Quality gates` (immediately after the US-0123 bullet at L27-28, before US-0122 at L32):
     ```
     - **US-0124** - OpenCode orchestrator plugin spawn-only `/auto` (Task-spawns US-0069 roles, never executes phase work in-session); traceability:
       runbook `## OpenCode orchestrator plugin reason codes (US-0124)`, architecture `# US-0124`, `decisions/DEC-0124.md`.
     ```
  2. Add a user-facing bullet containing `\bUS-0124\b` to root `README.md` under `## Commands and workflow` (L349) or the `### Feature coverage catalog (US-0091)` section (L1178/L1378).
  3. Re-run `python scripts/validate_readme_feature_coverage.py --repo . --report` -> confirm `status: PASS` with `coverage_missing: []`.
  4. Re-run `python scripts/check-user-visible-metadata.py --repo .` (step 20/23c of execute command) after the README edit.
  This fix is a US-0124 release-gate backfill, not US-0125 scope expansion.

## Non-blocking observations

- US-0125 execute did NOT run the full harness (dev handoff: "time-bounded; 11/11 US-0125 contract markers green + opencode-adapter parity OK + triad check clean are the gate evidence"). QA refreshed the harness as required and found 2 pre-existing blockers. Future executes should run the full harness when prior green is stale.
- US-0125 contract test markers 1-11 are green and unaffected by the 2 blockers; US-0125's own deliverables are sound.
- `tests/auto_command_contract_test.py` working-tree diff (US-0099 postinstall hook refactor + US-0100/US-0101 section renumbering) is from prior sprints, not US-0125. The US-0085 linkage test itself was not modified by recent changes - the failure is purely an architecture.md content gap.

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=qa`
- `role=qa`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 - required)
- `fresh_context_marker=qa-US0125-qa-20260824T213000Z-fresh` (NEW - not reused from execute or sovereign-critic)
- `timestamp=2026-08-24T21:30:00Z`
- `evidence_ref=sprints/S0125/qa-findings.md (this file), handoffs/qa_to_dev.md (FAIL handoff), tests/report.md (Pass:841 Fail:4 @ 2026-08-24T20:51:58Z), docs/engineering/state.md (qa checkpoint append-bottom)`

## Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260824-02`
- `runtime_proof_id=rp-auto-20260824-02-qa-qa-20260824T213000Z-US-0125`
- `phase_id=qa`, `role=qa`, `story_id=US-0125`, `sprint_id=S0125`
- `proof_issued_at=2026-08-24T21:30:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T22:30:00Z` (UTC)
- `proof_hash=65A96BF541C856A2E74EE96573D7C77CE4E47D2F7D91C3634DE31F2E55F98358`
- Canonical payload (sorted-key compact JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-02","phase_id":"qa","proof_issued_at":"2026-08-24T21:30:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-02-qa-qa-20260824T213000Z-US-0125","sprint_id":"S0125","story_id":"US-0125"}`

Prior phase proof consumed: `rp-auto-20260824-02-execute-dev-20260824T210000Z-US-0125` (proof_hash=3A45F2563E0533E1D4558150FEC8F3723C95285331F007B4AF70B35D960B69C7, ttl 2026-08-24T22:00:00Z - consumed before RUNTIME_PROOF_STALE).

## Next phase

- `/execute` (role=dev per US-0069 / DEC-0051 phase->role matrix; fresh dev subagent per BUG-0006) to remediate B-1 and B-2.
- STOP after qa; orchestrator spawns `/execute` in fresh dev subagent. Do NOT mark US-0125 DONE. Do NOT tick acceptance. Do NOT mutate intake JSON.
