# QA -> Dev handoff - US-0125 / S0125 (BLOCKING - FAIL)

- **sprint_id**: S0125
- **story_id**: US-0125 (OPEN - not marked DONE per US-0045)
- **phase_id**: qa (build+verify macro)
- **role**: qa (fresh per BUG-0006)
- **orchestrator_run_id**: auto-20260824-02
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **AUTO_IMPLEMENTATION_LOOP**: 1 (cycle: qa FAIL -> dev fix -> /qa re-run)
- **fresh_context_marker**: qa-US0125-qa-20260824T213000Z-fresh
- **timestamp**: 2026-08-24T21:30:00Z (UTC)
- **model_id**: glm-5.2-high (CROSS_MODEL_REVIEW=1 - required)
- **verdict**: **FAIL** - full harness Pass:841 / Fail:4 (hard gate violation; 2 blocking root causes)
- **story_status**: OPEN (US-0045 - not marked DONE; acceptance checkboxes unchecked)
- **intake_json**: NOT mutated

## Blocking findings (2 root causes -> 4 [FAIL] rows)

### B-1: architecture.md `# US-0090` section missing `US-0085` linkage

- **[FAIL] rows**: `slim auto command contract markers pass` (report L784); `US-0090 caveman-compress contract subtests pass` (report L805).
- **Failing test**: `tests/auto_command_contract_test.py::AutoCommandContractTest::test_caveman_compress_input_architecture_linkage (token='US-0085')` (line 1078).
- **Root cause**: `docs/engineering/architecture.md` `# US-0090` h2 section (L34) does not reference `US-0085`. 7 of 8 required linkages present; only `US-0085` missing.
- **Fix**: Add a `US-0085` reference in `arch` at or after L34 (`# US-0090` heading). Minimal additive sentence: append `See \`# US-0085\` for context fresh-context markers.` to the US-0090 section body. Do NOT alter other sections.
- **Attribution**: Pre-existing gap (US-0125 did not touch architecture.md; `git diff` confirms no US-0090/US-0085 changes). architecture.md is a US-0125 compose-guard (T-anch NO-OP) - record this as pre-existing-bug remediation in the loop-2 execute summary, not US-0125 scope expansion.

### B-2: US-0124 missing from root README `## Commands and workflow` + developer README `## Quality gates`

- **[FAIL] rows**: `validate_readme_feature_coverage repo --report passes` (report L814); `validate_readme_feature_coverage report idempotent` (report L815).
- **Failing validator**: `python scripts/validate_readme_feature_coverage.py --repo . --report` -> exit 1; `coverage_missing=["US-0124"]`, `coverage_present=["US-0121","US-0122","US-0123"]`.
- **Root cause**: US-0124 is `user_visible: true` (backlog L4283) and `Status: DONE` (backlog L4287; acceptance L152 `[x]`). US-0124 execute loop-2 added US-0123 to developer README `## Quality gates` but never added US-0124 to root README `## Commands and workflow` or developer README `## Quality gates`. Gap surfaced after US-0124 release ticked acceptance -> DONE -> entered coverage set.
- **Fix**:
  1. Add to `docs/developer/README.md` `## Quality gates` after the US-0123 bullet (L27-28), before US-0122 (L32):
     `- **US-0124** - OpenCode orchestrator plugin spawn-only \`/auto\` (Task-spawns US-0069 roles, never executes phase work in-session); traceability: runbook \`## OpenCode orchestrator plugin reason codes (US-0124)\`, architecture \`# US-0124\`, \`decisions/DEC-0124.md\`.`
  2. Add a user-facing bullet containing `\bUS-0124\b` to root `README.md` under `## Commands and workflow` (L349) or `### Feature coverage catalog (US-0091)` (L1178/L1378).
  3. Re-run `python scripts/validate_readme_feature_coverage.py --repo . --report` -> confirm `status: PASS`, `coverage_missing: []`.
  4. Re-run `python scripts/check-user-visible-metadata.py --repo .` (step 20/23c).
- **Attribution**: Pre-existing US-0124 release-gate backfill (US-0125 did not touch root README, developer README, or backlog). Record as backfill, not US-0125 scope expansion.

## US-0125 own-contract evidence (all PASS - unaffected by blockers)

- `python -m pytest tests/us0125_contract_test.py -v` -> 11/11 PASS (markers 1-11)
- `check_intake_template_parity --scope opencode-adapter` -> OK
- Byte-identical pairs (5/5) -> MATCH (runbook, its_magic/README.md, manifest, parity script, contract test)
- 15 command files <= 20 lines; auto.md dispatch-only (no spawn literals)
- `.cursor/commands` zero US-0125 refs; orchestrator.ts zero US-0125 refs
- Architecture `# US-0125` (L1836) before `# US-0089` (L2103)
- Triad --check exit 0; metadata guard exit 0

## Verification commands for dev loop-2

```powershell
# After applying B-1 and B-2 fixes:
python -m pytest tests/us0125_contract_test.py -v          # expect 11/11 PASS
python -m pytest tests/auto_command_contract_test.py -v     # expect 151/151 PASS (B-1 fixed)
python scripts/validate_readme_feature_coverage.py --repo . --report   # expect status: PASS (B-2 fixed)
python scripts/check_intake_template_parity.py --repo . --scope opencode-adapter  # expect OK
python scripts/enforce-triad-hot-surface.py --check          # expect exit 0
python scripts/check-user-visible-metadata.py --repo .      # expect exit 0
powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1 # expect exit 0; Pass:845 (or higher) / Fail: 0; zero [FAIL] rows
```

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=qa`, `role=qa`, `model_id=glm-5.2-high`
- `fresh_context_marker=qa-US0125-qa-20260824T213000Z-fresh` (NEW)
- `timestamp=2026-08-24T21:30:00Z`
- `evidence_ref=sprints/S0125/qa-findings.md, handoffs/qa_to_dev.md (this prepend), tests/report.md (Pass:841 Fail:4 @ 2026-08-24T20:51:58Z), docs/engineering/state.md (qa checkpoint append-bottom)`

## Strict runtime proof (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-02-qa-qa-20260824T213000Z-US-0125`
- `proof_issued_at=2026-08-24T21:30:00Z`, `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T22:30:00Z`
- `proof_hash=65A96BF541C856A2E74EE96573D7C77CE4E47D2F7D91C3634DE31F2E55F98358`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-02","phase_id":"qa","proof_issued_at":"2026-08-24T21:30:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-02-qa-qa-20260824T213000Z-US-0125","sprint_id":"S0125","story_id":"US-0125"}`

Prior phase proof consumed: `rp-auto-20260824-02-execute-dev-20260824T210000Z-US-0125` (hash=3A45F2563E0533E1D4558150FEC8F3723C95285331F007B4AF70B35D960B69C7, ttl 2026-08-24T22:00:00Z).

## Next phase

- `/execute` (role=dev per US-0069 / DEC-0051; fresh dev subagent per BUG-0006) to remediate B-1 and B-2.
- STOP after qa; orchestrator spawns `/execute` in fresh dev subagent. Do NOT mark US-0125 DONE. Do NOT tick acceptance. Do NOT mutate intake JSON.

---
# QA → Dev handoff — US-0124 / S0124 (BLOCKING — FAIL)

- **sprint_id**: S0124
- **story_id**: US-0124 (OPEN — not marked DONE per US-0045; acceptance unchecked)
- **phase_id**: qa
- **role**: qa (fresh per BUG-0006)
- **orchestrator_run_id**: auto-20260824-02
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **AUTO_IMPLEMENTATION_LOOP**: 1 (cycle: dev fix → /qa re-run)
- **fresh_context_marker**: qa-US0124-qa-20260824T191000Z-fresh
- **timestamp**: 2026-08-24T19:10:00Z (UTC)
- **model_id**: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
- **verdict**: **FAIL (blocking)** — US-0124 scope gates green (12/12 contract markers, opencode-adapter parity, 6/6 byte-identical pairs, plugin hygiene, heading order); canonical harness `tests/report.md` reports `Pass:843 Fail:2` due to pre-existing US-0123 README coverage gap. HARD test gate forbids claiming Fail=0. Not rubber-stamped.
- **story_status**: OPEN (US-0045 — not marked DONE)
- **next_scheduled_phase**: /execute (fresh dev subagent per BUG-0006)
- **stop_condition**: STOP after qa; orchestrator spawns /execute in fresh dev subagent. Do NOT spawn /execute from this qa subagent. Do NOT mark US-0124 DONE.

## Blocking finding

### B-1: `validate_readme_feature_coverage` FAIL — US-0123 missing from `docs/developer/README.md` `## Quality gates` section

- **Severity**: blocking (release-gate US-0039 / US-0091 / DEC-0074).
- **Evidence**:
  - `tests/report.md` L4 `Fail: 2`; L814–815 `[FAIL] validate_readme_feature_coverage repo --report passes` + `[FAIL] validate_readme_feature_coverage report idempotent`.
  - `python scripts/validate_readme_feature_coverage.py --repo . --report` → `{"coverage_missing":["US-0123"],"coverage_present":["US-0121","US-0122"],"coverage_total":3,"gaps":[{"dev_h2":"Quality gates","id":"US-0123","kind":"US","predicate_source":"explicit:true","root_h2":"Commands and workflow","user_visible":true}],"status":"FAIL"}` + stderr `README_FEATURE_COVERAGE_BLOCKED` / `README_FEATURE_COVERAGE_GAP:US-0123`.
- **Root cause**: US-0123 (DONE, `user_visible: true` in `docs/product/backlog.md` L4243–4248) is present in `its_magic/README.md` `## Commands and workflow` (L380) so `root_ok=True`, but **absent** from `docs/developer/README.md` `## Quality gates` (only `**US-0121**` at L25–26; `**US-0122**` sits under `## Architecture notes` L30–31). `has_dev_coverage` needs `**US-0123**` (bold) or `traceability:` + `US-0123` on a line in `Quality gates`.
- **Pre-existing (NOT a US-0124 regression)**:
  1. Gap names **US-0123**, not US-0124. US-0124 is OPEN → `classify_item` returns `not in_scope` → not in coverage set (`coverage_total: 3`).
  2. US-0124 execute scope did not touch `docs/developer/README.md` (git diff shows only US-0121/US-0122 additions).
  3. US-0123 execute (under `FRAMEWORK_KIT_REPO=1`) skipped `/execute` step 23b per execute command contract.
- **Why blocking despite pre-existing**: HARD test gate (US-0045 / US-0039) forbids `Fail:0` claim when `tests/report.md` has `Fail: 2` + non-empty `[FAIL]` rows. `/release` requires `Fail:0`. QA does not rubber-stamp. Fix is small, dev-owned.

## Precise fix for dev (B-1)

Add a `**US-0123**` + `traceability:` bullet to the `## Quality gates` section of **both** `docs/developer/README.md` **and** `template/docs/developer/README.md` (byte-identical mirror). Suggested wording (mirror the US-0121 pattern at L25–26):

```
- **US-0123** — OpenCode per-role/per-phase model slug routing (multi-provider, no vendor IDs in template); traceability:
  runbook `## OpenCode model slug routing (US-0123)`, architecture `# US-0123`, `decisions/DEC-0123.md`.
```

Place immediately after the `**US-0121**` bullet (L25–26) so `## Quality gates` stays grouped. Do **not** add US-0124 — US-0124 is OPEN and not in the coverage set; its bullet belongs in a future US-0124 closure execute when US-0124 flips DONE.

After the edit, dev must re-run:
1. `python scripts/validate_readme_feature_coverage.py --repo . --report` → expect `status:PASS`, `coverage_missing:[]`.
2. `python scripts/check_intake_template_parity.py --scope=readme-feature-coverage` → expect exit 0.
3. `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1` → expect `Pass:845 Fail:0`, zero `[FAIL]` rows, exit 0.
4. Confirm `docs/developer/README.md` ↔ `template/docs/developer/README.md` byte-identical.

## US-0124 scope (clean — no dev action required on US-0124 deliverables)

- 12/12 contract-test markers PASS (`tests/us0124_contract_test.py`).
- opencode-adapter parity PASS (`[INTAKE_TEMPLATE_PARITY_OK]`).
- 6/6 byte-identical pairs (active ↔ template): runbook, its_magic/README.md, installer-owned-paths.manifest, auto_outer_driver.py, check_intake_template_parity.py, us0124_contract_test.py.
- Architecture `# US-0124` (L1816) before `# US-0089` (L2021) — DEC-0073 §11.
- Plugin hygiene: spawn-only (no auto.md clone), `OPENCODE_DRIVER_INVOKE_FAILED` distinct from `OPENCODE_HEADLESS_UNSUPPORTED`, zero secrets/env refs.
- Compose guards 9/9 UNCHANGED; backlog L4287 OPEN; acceptance unchecked; intake JSON not mutated.

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=qa`, `role=qa`, `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=qa-US0124-qa-20260824T191000Z-fresh`, `timestamp=2026-08-24T19:10:00Z`
- `evidence_ref=sprints/S0124/qa-findings.md + handoffs/qa_to_dev.md (this file) + docs/engineering/state.md (qa checkpoint) + handoffs/resume_brief.md (FAIL → /execute prepend)`

## Strict runtime proof (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-02-qa-qa-20260824T191000Z-US-0124`
- `proof_issued_at=2026-08-24T19:10:00Z`, `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T20:10:00Z`
- `proof_hash=3953643135F290CE4A0B2F0317C4187F3AA8446EE6C927E4678A62F24F02CF82`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build_verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-02","phase_id":"qa","proof_issued_at":"2026-08-24T19:10:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-02-qa-qa-20260824T191000Z-US-0124","sprint_id":"S0124","story_id":"US-0124"}`

## Next phase

Spawn fresh **dev** subagent for **`/execute`** on **S0124 / US-0124** (fix B-1, re-run harness to Fail:0). Do NOT mark US-0124 DONE. Do NOT tick acceptance. Do NOT mutate intake JSON.

---

# QA → Dev handoff — US-0121 / S0121 (BLOCKING)

- sprint_id: S0121
- story_id: US-0121
- phase_id: qa
- role: qa (fresh per BUG-0006)
- orchestrator_run_id: auto-20260823-01
- delivery_mode: ultra_lean
- macro_phase: build+verify
- fresh_context_marker: qa-US0121-qa-20260823T114000Z-fresh
- timestamp: 2026-08-23T11:40:00Z (UTC)
- model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
- verdict: **FAIL** (1 blocking finding)
- blocking_findings: 1
- non_blocking_findings: 4
- tests_run: 0 (python_not_on_path — static review fallback)
- next_scheduled_phase: /execute (auto-implementation loop; AUTO_IMPLEMENTATION_LOOP=1)
- stop_condition: STOP after qa; do not spawn /execute from this QA subagent. Orchestrator reroutes.

## Blocking finding

### B-1: marker 12 false-positive — README prose contains `apiKey` (AC-10 / AC-7)

- severity: blocking
- ac_mapping: AC-10, AC-7
- marker: 12 (test_us0121_no_secrets_in_pack)
- issue_key: ik_us0121_marker12_apikey_prose_false_positive (execute-critic row 16, escalated by QA to blocking)

#### Reproduction

1. Install python 3 on PATH.
2. `python -m pytest tests/us0121_host_mode_test.py::test_us0121_no_secrets_in_pack -v`
3. Observe failure: `AssertionError: secret-like patterns found in template/.opencode/: ['template/.opencode/README.md']`

#### Root cause

- `tests/us0121_host_mode_test.py` L243: `pattern = re.compile(r"apiKey|api_key|sk-|MODEL=")` — substring search, no word-boundary, no README exclusion.
- `template/.opencode/README.md` L45: prose `ships no opencode.json (a consumer repo may add one with provider/apiKey` contains the literal substring `apiKey`.
- The regex matches prose documenting a forbidden pattern, not an actual secret.

#### Remediation options (dev picks one; QA does not implement)

- **Option A (test fix — preferred, smallest surface)**: tighten the regex to match assignments, not prose. Use `re.compile(r"\bapiKey\s*[:=]|api_key\s*[:=]|sk-[A-Za-z0-9]{8,}|MODEL\s*=")` or exclude `README.md` from the walk. This keeps the README documentation intact and fixes the false-positive.
- **Option B (product fix)**: rephrase `template/.opencode/README.md` L45 to avoid the literal `apiKey` token (e.g., "a consumer repo may add one with provider credentials and must not commit it"). Keeps the naive regex.
- **Option C (both)**: combine A + B for defense-in-depth.

QA recommendation: **Option A** — the README is documenting a forbidden pattern, which is valuable operator guidance; the test should distinguish prose from assignments.

#### Compose guard impact

- None. README is template-only; not a US-0008 / DEC-0045 / US-0102 / US-0001 / US-0018 surface. Fixing this does not touch compose guards.

#### Files to edit (dev discretion)

- `tests/us0121_host_mode_test.py` (Option A) — and `template/tests/us0121_host_mode_test.py` byte-identical mirror (parity pair).
- OR `template/.opencode/README.md` (Option B).
- OR both (Option C).

## Non-blocking findings (carry forward; do not block /execute)

- NB-1: tests_not_run=python_not_on_path (environmental; orchestrator should rerun /qa in a python-on-PATH env before /release).
- NB-2: AC-6 parity scope grep-only (marker 13 does not subprocess-invoke the parity CLI; pack files excluded from OPENCODE_ADAPTER_PAIRS). issue_key=ik_us0121_ac6_parity_scope_pack_gap.
- NB-3: triple-installer behavioral parity grep-only (marker 14; PS/sh runtime not exercised). issue_key=ik_us0121_py_only_behavioral_triple_grep.
- NB-4: symmetric CURSOR_* shrink diagnostics grep-only (markers 8-9 cover opencode-shrink only; CURSOR_* shrink-to-opencode is grep-only in marker 14).

## Compose guards (5/5 UNCHANGED — verified read-only)

| Compose target | Verification | Result |
|---|---|---|
| US-0008 (CLI installer) | additive --host only; missing/overwrite/clean/upgrade semantics UNCHANGED | read-only |
| DEC-0045 (its_magic/ ownership) | its_magic/ ownership unchanged | read-only |
| US-0102 (volatile-ID rule) | template ships no vendor slugs; *.local.json{,c} gitignore mirrors kit convention | read-only |
| US-0001 (phase names) | placeholders only; no command body clone | read-only |
| US-0018 (packaging delivery) | installer delivery path unchanged except additive --host forward | read-only |

## What dev should do next

1. Pick a remediation option for B-1 (Option A recommended).
2. Edit the chosen file(s); keep `tests/us0121_host_mode_test.py` ↔ `template/tests/us0121_host_mode_test.py` byte-identical if Option A (parity pair).
3. If python becomes available on PATH, run `python -m pytest tests/us0121_host_mode_test.py -v` and confirm 14/14 PASS.
4. Update `sprints/S0121/progress.md` with the fix cycle.
5. Re-handoff to QA via `handoffs/dev_to_qa.md` with a new `fresh_context_marker`.

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- phase_id=qa
- role=qa
- fresh_context_marker=qa-US0121-qa-20260823T114000Z-fresh
- timestamp=2026-08-23T11:40:00Z
- model_id=glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
- evidence_ref=sprints/S0121/qa-findings.md + handoffs/qa_to_dev.md (this file)
- next_scheduled_phase=/execute (blocking finding open; AUTO_IMPLEMENTATION_LOOP=1)
- stop_condition=STOP after qa; do not spawn next phase. Orchestrator reroutes to /execute in a fresh dev subagent.

## Strict runtime proof (US-0056 / DEC-0038)

- runtime_proof_id=rp-auto-20260823-01-qa-qa-20260823T114000Z-US-0121
- proof_hash=457664171B3FF0771957E71785576B14B39C66F3F988066A82904BFB177BAB78
- proof_ttl=2026-08-23T12:40:00Z
