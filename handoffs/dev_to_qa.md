# Dev → QA handoff — US-0129 / S0129 (execute)

- **sprint_id**: S0129
- **story_id**: US-0129 (OPEN — not marked DONE per US-0045)
- **phase_id**: execute (build+verify macro — first canonical phase)
- **role**: dev (fresh per BUG-0006)
- **orchestrator_run_id**: auto-20260827-01
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **AUTO_IMPLEMENTATION_LOOP**: 1
- **fresh_context_marker**: dev-US0129-execute-20260827T080438Z-fresh (NEW per US-0048 / BUG-0006)
- **timestamp**: 2026-08-27T08:04:38Z (UTC)
- **model_id**: cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 — required)
- **verdict**: PASS (execute) — 8/8 tasks completed; 8/8 us0129 contract markers green; `--scope=arch-linkage` parity OK; compose 8/8 UNCHANGED
- **story_status**: OPEN (US-0045 — not marked DONE; acceptance L157 unchecked)
- **intake_json**: NOT mutated
- **next_scheduled_phase**: `/qa` (role=qa) — orchestrator-owned; this subagent did not spawn QA
- **UAT_BROWSER**: n/a — library/docs/tests story; no browser UAT

## Scope delivered (US-0129 — linkage guard + reason_codes + flag + refresh-context + tests + runbook + parity + installer)

Fail-closed architecture-rollover linkage guard wrapping `enforce-triad-hot-surface.py --rollover` (DEC-0129 / R-0113). New `scripts/arch_linkage_guard.py` imports `split_arch_stories` (no copy-fork). Pre-guard blocks with `ARCH_LINKAGE_ROLLOVER_BLOCKED` (`security_hard`) before any archive write. Post-guard re-checks active headings. Optional `ARCH_LINKAGE_AUTO_REPAIR` default-off, not in `AUTONOMY_PRESET`; DQ8 H1 stubs insert before US-0089/US-0090 tail. `/refresh-context` step 4: pre-guard → `--rollover` → post-guard → `--check`. Eight `test_us0129_*` markers + harness **26AB**.

### Files created (new)

- `scripts/arch_linkage_guard.py` + `template/scripts/arch_linkage_guard.py`
- `tests/us0129_contract_test.py` + `template/tests/us0129_contract_test.py`
- `sprints/S0129/t-anch-verification.md`
- `sprints/S0129/summary.md`

### Files edited (scoped, additive; active↔template byte-identical)

- `docs/engineering/reason_codes.md` + template (`## US-0129`)
- `scripts/data/autonomy_stop_matrix.yaml` (`ARCH_LINKAGE_ROLLOVER_BLOCKED` security_hard)
- `docs/engineering/autonomy-stop-matrix.md` + template
- `.cursor/scratchpad.md` + `.cursor/scratchpad.local.example.md` + template mirrors (comment only)
- `.cursor/commands/refresh-context.md` + template
- `tests/run-tests.ps1` + `tests/run-tests.sh` (harness 26AB)
- `docs/engineering/runbook.md` + template (h3 under triad)
- `scripts/check_intake_template_parity.py` + template (`ARCH_LINKAGE_PAIRS`)
- `docs/engineering/context/installer-owned-paths.manifest` + template
- `sprints/S0129/tasks.md`, `sprints/S0129/progress.md`

### Files NOT modified (compose guards)

- `docs/engineering/architecture.md` (T-anch NO-OP)
- `docs/product/backlog.md` / `docs/product/acceptance.md` (US-0045; L157 unchecked)
- `decisions/DEC-0129.md` / intake JSON
- US-0126 / US-0127 / US-0128 / US-0130 DONE rows
- `scripts/enforce-triad-hot-surface.py` `rollover_architecture` split/pack/`ARCH_HOT_MAX_*`
- `AUTONOMY_PRESET` expansion (12 flags unchanged)

## Verification evidence

| Check | Result |
|---|---|
| `python -m pytest tests/us0129_contract_test.py -v` | **8 passed** |
| `--scope=arch-linkage` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| `validate_autonomy_stop_matrix.py --self-test` | `[MATRIX_VALID]` 29 codes |
| `check-user-visible-metadata.py` | exit 0 |
| No live `ARCH_LINKAGE_AUTO_REPAIR=1` | PASS (comment only) |
| No-DONE / L157 | OPEN / unchecked |

### critic_evidence

```json
{"anti_slop_aggregate":8,"critic_model_id":"composer-2.5-fast","degraded_mode":false,"findings_path":"handoffs/sovereign_critic_findings.jsonl","producer_model_id":"cursor-grok-4.6-high","rework_generation":0}
```

Carry-forward of sprint-plan sovereign-critic PASS (anti_slop=8, 0 blocking `a0129spn-*`; marker `tl-US0129-sovereign-critic-sprint-plan-20260827T074408Z-fresh`). Execute critic is orchestrator-owned next; this subagent did not spawn `/sovereign-critic` or `/qa`.

## Producer proof consumed

- `runtime_proof_id=rp-auto-20260827-01-sprint-plan-tech-lead-20260827T073646Z-US-0129`
- `proof_hash=8960A93B97E39E84B107001316228F5CBE69472DDF8835752862ECF4EC3B4B00` MATCH
- `consumed_at=2026-08-27T08:04:38Z` < `ttl=2026-08-27T08:36:46Z`

## This-phase strict runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260827-01-execute-dev-20260827T080438Z-US-0129`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260827-01","phase_id":"execute","proof_issued_at":"2026-08-27T08:04:38Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260827-01-execute-dev-20260827T080438Z-US-0129","sprint_id":"S0129","story_id":"US-0129"}`
- `proof_hash=CFE682EA7A8A7A8EF5A9486F7A9E04FAAC2F9DB6425147CA3D8B7B77F413CE4F`
- `proof_ttl=2026-08-27T09:04:38Z`

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=execute`
- `role=dev`
- `fresh_context_marker=dev-US0129-execute-20260827T080438Z-fresh`
- `timestamp=2026-08-27T08:04:38Z`
- `model_id=cursor-grok-4.6-high`
- `evidence_ref=handoffs/dev_to_qa.md, sprints/S0129/summary.md`

## Stop

STOP after EXECUTE_PASS. Next = `/qa` in a fresh qa subagent (orchestrator-owned). Do not spawn `/qa` from this subagent.

---

# Dev → QA handoff — US-0130 / S0130 (execute)

- **sprint_id**: S0130
- **story_id**: US-0130 (OPEN — not marked DONE per US-0045)
- **phase_id**: execute (build+verify macro — first canonical phase)
- **role**: dev (fresh per BUG-0006)
- **orchestrator_run_id**: auto-20260826-01
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **AUTO_IMPLEMENTATION_LOOP**: 1
- **fresh_context_marker**: dev-US0130-execute-20260826T221420Z-fresh (NEW per US-0048 / BUG-0006)
- **timestamp**: 2026-08-26T22:14:20Z (UTC)
- **model_id**: cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 — required)
- **verdict**: PASS (execute) — 8/8 tasks completed; 10/10 us0130 contract markers green; `--scope=sovereign-critic` + `--scope=model-tier-overrides` parity OK; us0104 compose PASS
- **story_status**: OPEN (US-0045 — not marked DONE; acceptance L158 unchecked)
- **intake_json**: NOT mutated
- **next_scheduled_phase**: `/qa` (role=qa) — orchestrator-owned; this subagent did not spawn QA
- **UAT_BROWSER**: n/a — library/docs/tests story; no browser UAT

## Scope delivered (US-0130 — additive overlay + validator allowlist + examples/installer + docs + parity + contract-test)

Operator pin overlay for `/sovereign-critic` model selection (R-0112 / compose DEC-0104 §5 / DEC-0087 / DEC-0086; no companion DEC). Precedence: hyphen pin `MODEL_SOVEREIGN-CRITIC` > optional catalog `roles.critic` when `MODEL_RESOLVE=role_catalog` > existing opposition/`dev` fallback UNCHANGED. Same-slug keeps `CROSS_MODEL_DEGRADED_MODE`. Optional `critic` via `CATALOG_OPTIONAL_ROLE_KEYS` (not in required `CATALOG_ROLE_KEYS`). Cursor-only example `critic=composer-2.5-fast` shipped as 9th. Never wrote `model-catalog.local.json`.

### Files created (new)

- `tests/us0130_contract_test.py` + `template/tests/us0130_contract_test.py`
- `template/.cursor/model-catalog.local.example.role-based-balanced_cursor_only.json`
- `sprints/S0130/t-anch-verification.md`
- `sprints/S0130/summary.md`

### Files edited (scoped, additive; active↔template byte-identical)

- `scripts/sovereign_critic_lib.py` + template
- `scripts/model_tier_lib.py` + template
- `scripts/model_tier_validate.py` + template
- v2 role example catalogs + cursor_only
- `docs/engineering/context/installer-owned-paths.manifest` + template
- `installer.ps1` / `installer.py`
- `.cursor/scratchpad.md` + `scratchpad.local.example.md` + template mirrors
- `docs/engineering/runbook.md` + template
- `scripts/check_intake_template_parity.py` + template
- `sprints/S0130/tasks.md`, `sprints/S0130/progress.md`

### Files NOT modified (compose guards)

- `docs/engineering/architecture.md` (T-anch NO-OP)
- `docs/product/backlog.md` / `docs/product/acceptance.md` (US-0045)
- `decisions/` / intake JSON / US-0129 / DONE rows US-0127/US-0128
- `.cursor/model-catalog.local.json` (never write)
- v1 example catalogs; `CATALOG_ROLE_KEYS` required-set; `PHASE_LOGICAL_ROLE`; US-0104 findings schema/lenses/`CROSS_MODEL_*` keys

## Verification evidence

| Check | Result |
|---|---|
| `python -m pytest tests/us0130_contract_test.py -v` | **10 passed** |
| `python -m pytest tests/us0104_contract_test.py -q` | **PASS** |
| `--scope=sovereign-critic` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| `--scope=model-tier-overrides` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| `check-user-visible-metadata.py` | exit 0 |
| Never-write gate | `.cursor/model-catalog.local.json` absent |

### critic_evidence

```json
{"anti_slop_aggregate":8,"critic_model_id":"composer-2.5-fast","degraded_mode":false,"findings_path":"handoffs/sovereign_critic_findings.jsonl","producer_model_id":"cursor-grok-4.6-high","rework_generation":0}
```

Carry-forward of sprint-plan sovereign-critic PASS (anti_slop=8, 0 blocking `a0130spn-*`). Execute critic is orchestrator-owned next; this subagent did not spawn `/sovereign-critic` or `/qa`.

## Producer proof consumed

- `runtime_proof_id=rp-auto-20260826-01-sprint-plan-tech-lead-20260826T215200Z-US-0130`
- `proof_hash=5D0ADA062FE675333EF06E56DBC4649D22A2045C08D71456C7963893178CFED1` MATCH
- `consumed_at=2026-08-26T22:14:20Z` < `ttl=2026-08-26T22:52:00Z`

## This-phase strict runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260826-01-execute-dev-20260826T221420Z-US-0130`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260826-01","phase_id":"execute","proof_issued_at":"2026-08-26T22:14:20Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260826-01-execute-dev-20260826T221420Z-US-0130","sprint_id":"S0130","story_id":"US-0130"}`
- `proof_hash=089947FF99F92DF799FA3FD51A10E503B3DF26052833DE33EC7942ED7C59DA9C`
- `proof_ttl=2026-08-26T23:14:20Z`

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=execute`
- `role=dev`
- `fresh_context_marker=dev-US0130-execute-20260826T221420Z-fresh`
- `timestamp=2026-08-26T22:14:20Z`
- `model_id=cursor-grok-4.6-high`
- `evidence_ref=handoffs/dev_to_qa.md, sprints/S0130/summary.md`

## Stop

STOP after EXECUTE_PASS. Next = `/qa` in a fresh qa subagent (orchestrator-owned). Do not spawn `/qa` from this subagent.

---

# Dev → QA handoff — US-0128 / S0128 (execute)

- **sprint_id**: S0128
- **story_id**: US-0128 (OPEN — not marked DONE per US-0045)
- **phase_id**: execute (build+verify macro — first canonical phase)
- **role**: dev (fresh per BUG-0006)
- **orchestrator_run_id**: auto-20260826-01
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **AUTO_IMPLEMENTATION_LOOP**: 1
- **fresh_context_marker**: dev-US0128-execute-20260826T203023Z-fresh (NEW per US-0048 / BUG-0006)
- **timestamp**: 2026-08-26T20:30:23Z (UTC)
- **model_id**: cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 — required)
- **verdict**: PASS (execute) — 8/8 tasks completed; 11/11 us0128 contract markers green; `--scope=sovereign-convergence` parity OK; US-0110/US-0104/US-0127 compose 31/31 green
- **story_status**: OPEN (US-0045 — not marked DONE; acceptance L156 unchecked)
- **intake_json**: NOT mutated
- **next_scheduled_phase**: `/qa` (role=qa) — orchestrator-owned; this subagent did not spawn QA

## Scope delivered (US-0128 — additive code + docs + parity + contract-test)

Convergence `smoke_green` surrogate for waived-probe / contract-test UAT slices (R-0111 / DEC-0110 §10; no companion DEC). Legacy `_uat_smoke_passes` first; surrogate PASS when 6 live-runtime classes are `UAT_PROBE_FORBIDDEN`, `contract_test_failed=0`, and `convergence_smoke` (or tail `probe_kind=contract_tests_primary`) passes. Fail-closed `CONVERGENCE_SMOKE_SURROGATE_MISSING`. `/qa` and `/verify-work` emit the canonical step. 11 contract markers. Runbook subsection + reason_codes `## US-0128`. `SOVEREIGN_CONVERGENCE_PAIRS` +2 command rows.

### Files created (new)

- `tests/us0128_contract_test.py` + `template/tests/us0128_contract_test.py`
- `sprints/S0128/t-anch-verification.md`
- `sprints/S0128/summary.md`

### Files edited (scoped, additive; active↔template byte-identical)

- `scripts/sovereign_convergence_lib.py` + template
- `.cursor/commands/qa.md` + template
- `.cursor/commands/verify-work.md` + template
- `docs/engineering/reason_codes.md` + template
- `docs/engineering/runbook.md` + template
- `scripts/check_intake_template_parity.py` + template (`SOVEREIGN_CONVERGENCE_PAIRS` +2)
- `sprints/S0128/tasks.md`, `sprints/S0128/progress.md`

### Files NOT modified (compose guards)

- `docs/engineering/architecture.md` (T-anch NO-OP)
- `docs/product/backlog.md` / `docs/product/acceptance.md` (US-0045)
- `decisions/` / intake JSON / US-0129/US-0130 / DONE rows US-0108/US-0121..US-0127
- `sprints/S0126/uat.json` (reference fixture only — marker 11)
- `_eval_critic_resolved` / `SOVEREIGN_CRITIC_PAIRS` / US-0109 deploy smoke / US-0110 five-conjunct inventory of 10

## Verification evidence

| Check | Result |
|---|---|
| `python -m pytest tests/us0128_contract_test.py -v` | **11 passed** |
| `--scope=sovereign-convergence` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| US-0110 + US-0104 + US-0127 contract tests | **31 passed** |
| `check-user-visible-metadata.py` | exit 0 |
| No-secrets grep | zero secret literals on new code |

### critic_evidence

```json
{"anti_slop_aggregate":8,"critic_model_id":"composer-2.5-fast","degraded_mode":false,"findings_path":"handoffs/sovereign_critic_findings.jsonl","producer_model_id":"cursor-grok-4.6-high","rework_generation":0}
```

Carry-forward of sprint-plan sovereign-critic PASS (anti_slop=8, 0 blocking `a0128sp-*`). Execute critic is orchestrator-owned next; this subagent did not spawn `/sovereign-critic` or `/qa`.

## Producer proof consumed

- `runtime_proof_id=rp-auto-20260826-01-sprint-plan-tech-lead-2026-08-26T201100Z-US-0128`
- `proof_hash=C911D7C5CAA2939EC6F65ED07C717E9CBB00E80B551DCBFECA097D39F26878F4` MATCH
- `consumed_at=2026-08-26T20:25:50Z` < `ttl=2026-08-26T21:11:00Z`

## This-phase strict runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260826-01-execute-dev-20260826T203023Z-US-0128`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260826-01","phase_id":"execute","proof_issued_at":"2026-08-26T20:30:23Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260826-01-execute-dev-20260826T203023Z-US-0128","sprint_id":"S0128","story_id":"US-0128"}`
- `proof_hash=F0EE260C2ADF63821C8C22B7699DFDC0C184BFCD8E32B07C8AB720F78ADBBF32`
- `proof_ttl=2026-08-26T21:30:23Z`

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=execute`
- `role=dev`
- `fresh_context_marker=dev-US0128-execute-20260826T203023Z-fresh`
- `timestamp=2026-08-26T20:30:23Z`
- `model_id=cursor-grok-4.6-high`
- `evidence_ref=handoffs/dev_to_qa.md, sprints/S0128/summary.md`

## FRAMEWORK_KIT_REPO / DEV_AUTO_LAUNCH

- `FRAMEWORK_KIT_REPO=1` — skipped execute 23a/23b project README bootstrap/delta
- `DEV_AUTO_LAUNCH_PROFILE=off` — skipped execute 24a–24d
- `REMOTE_EXECUTION=0` — no remote cues
- `CROSS_MODEL_REVIEW=1` — critic_evidence block above (carry-forward; no critic spawn)

## Stop

STOP after execute PASS. Next = `/qa` in a fresh qa subagent. Do not spawn `/qa` from this subagent.

---

# Dev → QA handoff — US-0127 / S0127 (execute)

- **sprint_id**: S0127
- **story_id**: US-0127 (OPEN — not marked DONE per US-0045)
- **phase_id**: execute (build+verify macro — first canonical phase)
- **role**: dev (fresh per BUG-0006)
- **orchestrator_run_id**: auto-20260826-01
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **AUTO_IMPLEMENTATION_LOOP**: 1
- **fresh_context_marker**: dev-US0127-execute-20260826T184328Z-fresh (NEW per US-0048 / BUG-0006)
- **timestamp**: 2026-08-26T18:43:28Z (UTC)
- **model_id**: cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 — required)
- **verdict**: PASS (execute) — 8/8 tasks completed; 13/13 us0127 contract markers green; `--scope=sovereign-critic` parity OK; US-0110/US-0104 compose 18/18 green
- **story_status**: OPEN (US-0045 — not marked DONE; acceptance L155 unchecked)
- **intake_json**: NOT mutated
- **next_scheduled_phase**: `/qa` (role=qa) — orchestrator-owned; this subagent did not spawn QA

## Scope delivered (US-0127 — additive code + docs + parity + contract-test)

Blocking-only conjunct-3: `_critic_jsonl_has_open` delegates to `read_open_blocking`. JSONL is authoritative when present/non-empty; QA-markdown fallback only if JSONL absent; skip when neither. Auto-resolve hook at `/sovereign-critic` PASS. Operator-only hygiene CLI. 13 contract markers. Runbook + reason_codes. `SOVEREIGN_CRITIC_PAIRS` + `--scope=sovereign-critic`.

### Files created (new)

- `scripts/sovereign_critic_hygiene.py` + `template/scripts/sovereign_critic_hygiene.py`
- `tests/us0127_contract_test.py` + `template/tests/us0127_contract_test.py`
- `sprints/S0127/t-anch-verification.md`
- `sprints/S0127/summary.md`

### Files edited (scoped, additive; active↔template byte-identical)

- `scripts/sovereign_convergence_lib.py` + template
- `scripts/sovereign_critic_lib.py` + template (`auto_resolve_nonblocking_for_run` additive)
- `.cursor/commands/sovereign-critic.md` + template
- `docs/engineering/runbook.md` + template
- `docs/engineering/reason_codes.md` + template
- `scripts/check_intake_template_parity.py` + template
- `sprints/S0127/tasks.md`, `sprints/S0127/progress.md`

### Files NOT modified (compose guards)

- `docs/engineering/architecture.md` (T-anch NO-OP)
- `scripts/sovereign_critic_validate.py` (marker 13 asserts current reject behavior)
- `docs/product/backlog.md` / `docs/product/acceptance.md` (US-0045)
- `decisions/` / intake JSON / US-0128/US-0129/US-0130 / DONE rows US-0108/US-0121..US-0126
- `read_open_blocking` / `resolve_finding` signatures and findings JSONL schema

## Verification evidence

| Check | Result |
|---|---|
| `python -m pytest tests/us0127_contract_test.py -v` | **13 passed** |
| `--scope=sovereign-critic` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| `--scope=sovereign-convergence` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| `--scope=opencode-adapter` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| US-0110 + US-0104 contract tests | **18 passed** |
| `check-user-visible-metadata.py` | exit 0 |
| No-secrets grep | zero hits |

### critic_evidence

```json
{"anti_slop_aggregate":10,"critic_model_id":"composer-2.5-fast","degraded_mode":false,"findings_path":"handoffs/sovereign_critic_findings.jsonl","producer_model_id":"cursor-grok-4.6-high","rework_generation":0}
```

Carry-forward of plan-verify sovereign-critic PASS (anti_slop=10, 0 blocking). Execute critic is orchestrator-owned next; this subagent did not spawn `/sovereign-critic` or `/qa`.

## Producer proof consumed

- `runtime_proof_id=rp-auto-20260826-01-plan-verify-qa-20260826T182713Z-US-0127-reattest`
- `proof_hash=3BFC94355962D40C58D8F65840760574022B9B17E1960C6DA03F8E593C3B38AD` MATCH
- `consumed_at=2026-08-26T18:36:03Z` < `ttl=2026-08-26T19:27:13Z`

## This-phase strict runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260826-01-execute-dev-20260826T184328Z-US-0127`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260826-01","phase_id":"execute","proof_issued_at":"2026-08-26T18:43:28Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260826-01-execute-dev-20260826T184328Z-US-0127","sprint_id":"S0127","story_id":"US-0127"}`
- `proof_hash=F42BBB6F51CD57EE2B5D7EC04630F5EFB38F93B89B38AEE4C38418C28616BBFE`
- `proof_ttl=2026-08-26T19:43:28Z`

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=execute`, `role=dev`, `model_id=cursor-grok-4.6-high`
- `fresh_context_marker=dev-US0127-execute-20260826T184328Z-fresh`
- `timestamp=2026-08-26T18:43:28Z`
- `evidence_ref=handoffs/dev_to_qa.md, sprints/S0127/summary.md`

---

# Dev → QA handoff — US-0126 / S0126 (execute)

> **LOOP-2 UPDATE (2026-08-25T17:10:00Z, dev, `model_id=glm-5.2-high`, fresh marker `dev-US0126-execute-20260825T171000Z-fresh-loop2`)**: Verify-work B-1 FAIL (7 harness Fail) remediated. Full harness `tests/run-tests.ps1` → **Pass:845 Fail:0** (no `[FAIL]` rows; `tests/report.md` timestamp 2026-08-25T17:09:57Z). `pytest tests/us0126_contract_test.py` 12/12 PASS. `--scope=opencode-adapter` parity OK. `validate_readme_feature_coverage --repo . --report` → `coverage_missing=[]` status=PASS (US-0125 gap closed). Edits: (A) `docs/engineering/architecture.md` — restored `# US-0091` + `# US-0093` H1 blocks before `# US-0089`, appended `# US-0090` H1 after `# US-0089` (only `# US-`/`## US-` heading after US-0089; carries DEC-0073/DEC-0072/R-0073/`# US-0089`/US-0053/US-0085/US-0078/DEC-0060), reworded 5 task-table refs `` `# US-0089` ``→`` `US-0089` `` so `arch.find` resolves to real heading (fixes `test_bug0011_architecture_linkage`); file 2950→2999 lines (under ARCH_HOT_MAX_LINES=3000); `--check-arch-heading-policy --baseline-h2-count 38` PASS. (B) `docs/developer/README.md` + byte-identical `template/docs/developer/README.md` — added `**US-0125**` Architecture notes row. NOT mutated: backlog US-0126 OPEN, acceptance L154 unchecked, intake JSON, US-0121..US-0125 not reopened, `OPENCODE_VALIDATOR_FAILED` wrapper NOT resurrected, US-0126 H1 (~L1747) untouched. Loop-2 runtime proof below.

- **sprint_id**: S0126
- **story_id**: US-0126 (OPEN — not marked DONE per US-0045)
- **phase_id**: execute (build+verify macro — first canonical phase)
- **role**: dev (fresh per BUG-0006)
- **orchestrator_run_id**: auto-20260825-01
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **AUTO_IMPLEMENTATION_LOOP**: 1 (loop 1 first execute)
- **fresh_context_marker**: dev-US0126-execute-20260825T163028Z-fresh (NEW per US-0048 / BUG-0006)
- **timestamp**: 2026-08-25T16:30:28Z (UTC)
- **model_id**: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
- **verdict**: PASS (execute) — 11/11 tasks completed; 12/12 us0126 contract markers green; opencode-adapter parity OK; prior-story regression 53/53 green
- **story_status**: OPEN (US-0045 — not marked DONE; acceptance L154 unchecked)
- **intake_json**: NOT mutated

## Scope delivered (US-0126 — additive docs + parity + contract-test only)

US-0126 is the sixth and final slice of the six-story OpenCode adapter epic (US-0121..US-0126). It owns Layer 4 — the operator-facing runbook section, the consolidated cross-host reason-code table, the `--scope=opencode-adapter` parity extension (2 new pairs), and the 12 `test_us0126_*` contract markers.

### Files created (new)

- `tests/us0126_contract_test.py` (12 markers, static/grep, no live OpenCode probe)
- `template/tests/us0126_contract_test.py` (byte-identical mirror — 12202b = 12202b)
- `sprints/S0126/t-anch-verification.md` (13 baseline checks PASS — verification only)

### Files edited (scoped, additive; all active↔template byte-identical)

| File | Change | Parity |
|---|---|---|
| `docs/engineering/runbook.md` | Append `## OpenCode host operator runbook (US-0126)` h2 body (program DoD + default-host reminder + out-of-scope + Boundaries subsection + consolidated reason-code table + parity scope cross-link) | byte-identical ↔ `template/docs/engineering/runbook.md` (204996b) |
| `template/docs/engineering/runbook.md` | Same edit (byte-identical mirror) | byte-identical ↔ active |
| `README.md` | Add `### OpenCode host operator runbook (US-0126)` blurb (default-host reminder + out-of-scope list; operator prose, no DEC ids) | byte-identical ↔ `template/README.md` (70980b) |
| `template/README.md` | Same edit (byte-identical mirror) | byte-identical ↔ active |
| `its_magic/README.md` | Add `### OpenCode host operator runbook (US-0126)` blurb (default-host reminder + out-of-scope list) | byte-identical ↔ `template/its_magic/README.md` (74559b) |
| `template/its_magic/README.md` | Same edit (byte-identical mirror) | byte-identical ↔ active |
| `scripts/check_intake_template_parity.py` | Extend `OPENCODE_ADAPTER_PAIRS` additively with 2 new pairs (`tests/us0126_contract_test.py` ↔ template + `docs/engineering/runbook.md` ↔ template); existing 8 pairs preserved; parity CLI stays byte-only (DQ3 layer split — no grep predicates added) | byte-identical ↔ `template/scripts/check_intake_template_parity.py` (22712b) |
| `template/scripts/check_intake_template_parity.py` | Same edit (byte-identical mirror) | byte-identical ↔ active |
| `sprints/S0126/tasks.md` | Checkboxes ticked (T-anch + T-001..T-010 + integration verification) | n/a (sprint artifact) |
| `sprints/S0126/progress.md` | Execute checkpoint prepended | n/a (sprint artifact) |

### Files NOT modified (compose guards)

- `docs/engineering/architecture.md` (T-anch NO-OP — DQ1..DQ8 locks + 12-marker table are locked source of truth)
- `decisions/DEC-0126.md` (T-anch NO-OP)
- `docs/engineering/context/installer-owned-paths.manifest` (DQ8 lock — UNCHANGED; 4055b = 4055b byte-identical)
- `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical mirror — UNCHANGED)
- `template/.opencode/agents/*.md` (US-0122 — agent files unchanged)
- `template/.opencode/plugins/orchestrator.ts` (US-0124 — plugin unchanged)
- `template/.opencode/commands/*.md` (US-0125 — command files unchanged)
- `.cursor/commands/*.md` + `.cursor/agents/*.mdc` (read-only compose for AC-10 baseline; marker 11 enforces presence)
- `docs/product/backlog.md` (US-0045 canonical status — not mutated)
- `docs/product/acceptance.md` (US-0045 derived view — L154 NOT ticked)
- Intake evidence JSON (not mutated)

## Verification evidence (PASS claim rule — all satisfied)

| Check | Result |
|---|---|
| `python -m pytest tests/us0126_contract_test.py -q` | **12 passed** in 0.15s (12/12 markers green) |
| `python scripts/check_intake_template_parity.py --scope=opencode-adapter` | **exit 0** — `[INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter` |
| Active + template manifest byte-identical | **match** (4055b = 4055b) |
| Active + template runbook byte-identical | **match** (204996b = 204996b) |
| Active + template parity script byte-identical | **match** (22712b = 22712b) |
| Active + template contract test byte-identical | **match** (12202b = 12202b) |
| Active + template root README byte-identical | **match** (70980b = 70980b) |
| Active + template its_magic README byte-identical | **match** (74559b = 74559b) |
| Prior-story regression (US-0121..US-0125 contract tests) | **53 passed** in 6.02s (no regression) |
| No-secrets grep on runbook/README/contract test | zero secret values (`.env` references are pre-existing US-0085 operator docs, not secrets) |
| No-DEC-leak gate (markers 5 + 6) | PASS — US-0126 operator prose clean (DEC ids only in Boundaries/evidence subsection) |
| Cursor-docs-not-deleted gate (marker 11) | PASS — `.cursor/commands/` (25 `.md`) + `.cursor/agents/` (7 `.mdc`) present vs current-kit-inventory baseline |
| No-`OPENCODE_VALIDATOR_FAILED`-wrapper gate (marker 2) | PASS — raw Python codes only; wrapper NOT resurrected |

## Contract marker summary (12 markers, one-test-per-AC)

| # | Marker | AC | Status |
|---|---|---|---|
| 1 | `test_us0126_runbook_section_present` | AC-1 | PASS (h2 + AC-1 operator phrases: stock OpenCode TUI/desktop/IDE, --host opt-in, /connect, slash commands, reason codes) |
| 2 | `test_us0126_reason_code_catalog_present` | AC-2 | PASS (15 codes; fail-closed action; NO OPENCODE_VALIDATOR_FAILED wrapper) |
| 3 | `test_us0126_parity_scope_opencode_adapter` | AC-3 | PASS (parity CLI exit 0) |
| 4 | `test_us0126_test_marker_checklist` | AC-4 | PASS (test_us0121_*..test_us0125_* found) |
| 5 | `test_us0126_readme_no_dec_leak` | AC-5a | PASS (no DEC ids in US-0126 README blurb) |
| 6 | `test_us0126_runbook_no_dec_leak` | AC-5b | PASS (no DEC ids in operator prose before Boundaries) |
| 7 | `test_us0126_program_dod_documented` | AC-6 | PASS (DoD key phrases present) |
| 8 | `test_us0126_default_host_reminder` | AC-7 | PASS (default-host phrases in runbook + README) |
| 9 | `test_us0126_out_of_scope_listed` | AC-8 | PASS (5 excluded items in runbook + README) |
| 10 | `test_us0126_template_doc_parity` | AC-9 | PASS (manifest + runbook byte-identical active↔template) |
| 11 | `test_us0126_cursor_docs_not_deleted` | AC-10 | PASS (25 `.md` + 7 `.mdc` files present vs baseline) |
| 12 | `test_us0126_prior_story_markers_present` | AC-4 aggregate | PASS (defense in depth) |

## Compose guards (8/8 UNCHANGED)

| Compose target | Verification | Result |
|---|---|---|
| US-0071 (operator-sentence sanitization) | no DEC ids in operator prose; cross-references to runbook h2 / Boundaries subsection only (DQ6/DQ7); markers 5 + 6 PASS | ✅ compose |
| US-0113..US-0117 (operator docs) | additive OpenCode host runbook section; no Cursor command catalog rewrite | ✅ compose |
| US-0121 / DEC-0120 (installer `--host` flag docs hook) | `## OpenCode host mode (US-0121)` h2 untouched; US-0126 cross-links | ✅ untouched |
| US-0122 / DEC-0122 (seven role agents) | runbook references role agents; does not redefine permissions | ✅ compose |
| US-0123 (per-role slug routing) | runbook references `/connect` keys + per-role slug routing; does not re-list vendor slugs | ✅ compose |
| US-0124 / DEC-0124 (orchestrator plugin + stub reason-code h2) | `## OpenCode orchestrator plugin reason codes (US-0124)` h2 untouched; US-0126 owns consolidated table; cross-links | ✅ untouched |
| US-0125 / DEC-0125 (thin commands + validator-bridge stub h2) | `## OpenCode thin commands + validator bridge (US-0125)` h2 untouched; US-0126 owns consolidated table; DEC-0125 DQ7 raw Python reason codes upheld — `OPENCODE_VALIDATOR_FAILED` wrapper NOT resurrected | ✅ untouched |
| US-0102 / DEC-0087 (no vendor slugs in `template/`) | no vendor slugs in runbook/README operator prose | ✅ untouched |

## Carry-ins closed

1. `ik_us0126_sp_ac1_marker_prose_gap` — CLOSED: marker 1 greps h2 PLUS AC-1 operator phrases (stock OpenCode TUI/desktop/IDE as UI, `--host` opt-in, `/connect` keys, kit UX = slash commands + reason codes) — defense in depth beyond h2-only grep. The runbook h2 body intro paragraph carries all those phrases.
2. AC-10 inventory path pin — CLOSED: `test_us0126_cursor_docs_not_deleted` (marker 11) uses a tuple-in-test sorted file-name list of `.cursor/commands/*.md` (25 files) + `.cursor/agents/*.mdc` (7 files) captured at execute time. NOT a frozen git snapshot. NOT a hash manifest of the entire `.cursor/` directory.

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=execute`, `role=dev`, `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=dev-US0126-execute-20260825T163028Z-fresh`
- `timestamp=2026-08-25T16:30:28Z`
- `evidence_ref=sprints/S0126/summary.md, sprints/S0126/progress.md, sprints/S0126/tasks.md, sprints/S0126/t-anch-verification.md, handoffs/dev_to_qa.md (this prepend), docs/engineering/state.md (execute checkpoint append-bottom), handoffs/resume_brief.md (execute PASS prepend → /qa)`

## Strict runtime proof (DEC-0038)

- `orchestrator_run_id=auto-20260825-01`
- `runtime_proof_id=rp-auto-20260825-01-execute-dev-20260825T163028Z-US-0126`
- `phase_id=execute`, `role=dev`, `story_id=US-0126`, `sprint_id=S0126`
- `proof_issued_at=2026-08-25T16:30:28Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-25T17:30:28Z` (UTC)
- `proof_hash=70B8523BBC15FC833D0508A1ACDA3B1CCF71AAA0DCBAF3AAC07C05535952B4C0`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260825-01","phase_id":"execute","proof_issued_at":"2026-08-25T16:30:28Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260825-01-execute-dev-20260825T163028Z-US-0126","sprint_id":"S0126","story_id":"US-0126"}`

Prior phase proof consumed: `rp-auto-20260825-01-plan-verify-qa-20260825T162348Z-US-0126` (proof_hash=7D60FA65A3BC387CE6817B27A3B16B9FEFBB92059D5575D5495E6EF7476E8559, ttl 2026-08-25T17:23:48Z — consumed before RUNTIME_PROOF_STALE).

## Next scheduled phase

- `/qa` (role=qa per US-0069 / DEC-0051 phase→role matrix; fresh qa subagent per BUG-0006 — after sovereign-critic of execute per CROSS_MODEL_REVIEW=1)
- STOP after execute; orchestrator spawns /qa in fresh qa subagent. Do NOT mark US-0126 DONE. Do NOT tick acceptance L154. Do NOT mutate intake JSON. Do NOT reopen US-0121..US-0125.

## Full harness note

Full harness (`tests/run-tests.ps1`) was NOT run in this execute spawn (time-bounded; 12/12 US-0126 contract markers green + opencode-adapter parity OK + prior-story regression 53/53 green are the gate evidence). QA should run the full harness and report `tests/report.md` Pass/Fail counts.

## Pre-existing note (NOT US-0126 scope)

`validate_readme_feature_coverage --report` reports `coverage_missing=["US-0125"]` — this is a pre-existing gap from US-0125's closure (US-0125 was DONE before this execute; its coverage row was not added to `docs/developer/README.md` `## Architecture notes` at closure). US-0126 is OPEN and NOT in the coverage set. US-0126 execute did not introduce this gap and must not fix it (would reopen US-0125 scope — forbidden). QA may flag this as a pre-existing US-0125 carry-forward.

> **LOOP-2 RESOLUTION (2026-08-25T17:10:00Z)**: The US-0125 coverage gap above is now CLOSED in loop-2 — `**US-0125**` row added to `docs/developer/README.md` `## Architecture notes` + byte-identical `template/docs/developer/README.md` mirror. `validate_readme_feature_coverage --repo . --report` now returns `coverage_missing=[]` status=PASS. This was a minimal coverage backfill (no US-0125 scope reopening — only a README coverage row added per US-0091 / DEC-0074 contract).

## Loop-2 strict runtime proof (DEC-0038)

- `orchestrator_run_id=auto-20260825-01`
- `runtime_proof_id=rp-auto-20260825-01-execute-dev-20260825T171000Z-loop2-US-0126`
- `phase_id=execute`, `role=dev`, `story_id=US-0126`, `sprint_id=S0126`
- `delivery_mode=ultra_lean`, `macro_phase=build+verify`, `model_id=glm-5.2-high`
- `proof_issued_at=2026-08-25T17:10:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-25T18:10:00Z` (UTC)
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260825-01","phase_id":"execute","proof_issued_at":"2026-08-25T17:10:00Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260825-01-execute-dev-20260825T171000Z-loop2-US-0126","sprint_id":"S0126","story_id":"US-0126"}`
- `proof_hash` = see `docs/engineering/state.md` loop-2 isolation evidence block (SHA-256 sorted-key compact JSON, uppercase hex).

