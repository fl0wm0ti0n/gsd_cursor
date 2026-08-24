# S0122 / US-0122 — QA findings (build+verify macro) — loop 2

- **sprint_id**: S0122
- **story_id**: US-0122
- **phase_id**: qa
- **role**: qa (fresh per BUG-0006)
- **orchestrator_run_id**: auto-20260824-01
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **AUTO_IMPLEMENTATION_LOOP**: cycle 2 (post-`RELEASE_TEST_FAILED` remediation)
- **fresh_context_marker**: qa-US0122-qa-loop2-20260824T131000Z-fresh
- **timestamp**: 2026-08-24T13:10:00Z (UTC)
- **model_id**: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required on isolation)
- **producer_model_id**: composer-2.5
- **producer_runtime_proof_id**: rp-auto-20260824-01-execute-dev-20260824T125912Z-US-0122
- **producer_proof_hash**: 47B79B125A6D2EA8E331F988BAC00785762825DA2EDC4B406072EB78D6F14A6A
- **producer_proof_ttl**: 2026-08-24T13:59:12Z (consumed before expiry — OK)
- **verdict**: PASS
- **story_status**: OPEN (not marked DONE — US-0045; closure owns the flip)
- **next_scheduled_phase**: /verify-work (fresh qa subagent per BUG-0006)
- **stop_condition**: STOP after /qa loop-2. Hand off via artifacts only to /verify-work. Do NOT spawn /verify-work from this QA subagent.

## Loop-2 remediations under test (from dev_to_qa.md)

| Remediation | Result |
|---|---|
| Runbook byte-identical mirror (`docs` -> `template`) | PASS (sha256 `97e1c0cc...a4a8` both sides; 196549 bytes both sides) |
| Architecture `# US-0122` (L1835) before `# US-0089` (L2056) — DEC-0073 §11 | PASS |
| `state.md` `## Active context surface (US-0053 / DEC-0035)` restored at L7 | PASS |
| Triad rollover `--rollover` + `--check` | PASS (units=9,2 per producer) |
| README US-0121 feature coverage | PASS (per producer) |
| `tests/run-tests.ps1` consolidated harness | **Pass:845 / Fail:0** (exit 0) |

## Test plan (independent re-run — not trusting execute)

1. **Contract gate** — `python -m pytest tests/us0122_contract_test.py -v` — require 8/8 PASS.
2. **Parity gate** — `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` — require INTAKE_TEMPLATE_PARITY_OK.
3. **Harness report freshness** — `tests/report.md` must show literal `Fail: 0` AND zero `[FAIL]` rows AND timestamp at/after execute loop-2 (`2026-08-24T12:59:12Z`). Producer timestamp `2026-08-24T13:02:49Z` qualifies.
4. **Architecture ordering** — `# US-0122` H1 (L1835) appears before `# US-0089` H1 (L2056).
5. **Runbook byte-identical** — `docs/engineering/runbook.md` vs `template/docs/engineering/runbook.md` SHA-256 match.
6. **State heading** — `## Active context surface (US-0053 / DEC-0035)` present in `docs/engineering/state.md`.
7. **AC checklist 10/10** still holds; compose 5/5 unchanged (backlog/acceptance/architecture/DEC-0122 not mutated by US-0122 execute).
8. **UAT probes** — static contract-test mapping (pack/contract story, no web UI). No fake browser PASS.

## Verification evidence

### 1. Contract gate — 8/8 PASS (independent re-run)

Command: `python -m pytest tests/us0122_contract_test.py -v`

Output:

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: G:\workdir\github\sonstiges\gsd_cursor
collecting ... collected 8 items

tests/us0122_contract_test.py::test_us0122_agent_inventory PASSED        [ 12%]
tests/us0122_contract_test.py::test_us0122_po_permission_object_form PASSED [ 25%]
tests/us0122_contract_test.py::test_us0122_po_production_code_denial PASSED [ 37%]
tests/us0122_contract_test.py::test_us0122_auto_task_allowlist PASSED    [ 50%]
tests/us0122_contract_test.py::test_us0122_security_edit_denied PASSED   [ 62%]
tests/us0122_contract_test.py::test_us0122_no_vendor_slugs_in_template PASSED [ 75%]
tests/us0122_contract_test.py::test_us0122_prompt_size_clone_guard PASSED [ 87%]
tests/us0122_contract_test.py::test_us0122_role_id_parity PASSED         [100%]

============================== 8 passed in 0.03s ==============================
```

Exit code: 0. **8/8 PASS** — independent re-run confirms producer claim.

### 2. Parity gate — PASS

Command: `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter`

Output: `[INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter`

Exit code: 0.

### 3. Harness report freshness — PASS

`tests/report.md` L1–L5:

```
# its-magic Test Report

Timestamp: 2026-08-24T13:02:49Z
Pass: 845
Fail: 0
```

- Literal `Fail: 0` — PASS.
- `rg "\[FAIL\]" tests/report.md` — **0 matches** (no `[FAIL]` rows).
- Timestamp `2026-08-24T13:02:49Z` is at/after execute loop-2 producer timestamp `2026-08-24T12:59:12Z` — fresh.
- No full-harness re-run performed (report not missing, not contradicting; per orchestrator brief).

### 4. Architecture ordering — PASS

`docs/engineering/architecture.md`:

- `# US-0122` H1 at **L1835** — `# US-0122 — OpenCode role agents and Layer-1 permission table`
- `# US-0089` H1 at **L2056** — `# US-0089: Cursor Caveman mode (scratchpad-configurable terse responses)`

L1835 < L2056 -> `# US-0122` H1 appears before `# US-0089` H1. DEC-0073 §11 honored.

(Note: `## US-0089 — Auto orchestration` at L720 is an H2 anchor under the US-0117 family umbrella, not the H1 `# US-0089` Caveman-mode section; the ordering check targets the H1 anchors per the brief.)

### 5. Runbook byte-identical — PASS

SHA-256 comparison:

| File | SHA-256 | Size |
|------|---------|------|
| `docs/engineering/runbook.md` | `97e1c0cc3e9d2f6016159c929f27c283283132ae5ac4ea4c5e4e03b3ff2ca4a8` | 196549 bytes |
| `template/docs/engineering/runbook.md` | `97e1c0cc3e9d2f6016159c929f27c283283132ae5ac4ea4c5e4e03b3ff2ca4a8` | 196549 bytes |

Byte-identical. Loop-2 runbook mirror remediation confirmed.

### 6. State heading — PASS

`docs/engineering/state.md` L7: `## Active context surface (US-0053 / DEC-0035)` — present.

### 7. Compose 5/5 UNCHANGED + AC checklist 10/10 — PASS

| Compose target | Surface | US-0122 mutation? |
|----------------|---------|-------------------|
| US-0003 | role identifiers in `template/.opencode/agents/*.md` stems | additive only — no backlog/acceptance mutation |
| US-0023 / BUG-0006 | `auto` Task-spawns role agents (no same-session roleplay) | additive only — `auto.md` `task` object 7-role allow + `*` deny last |
| US-0121 | `template/.opencode/**` pack path; no repo-root `opencode.json` | additive only — `agents/` populated; no `opencode.json` added |
| US-0102 / DEC-0087 | no vendor slugs in `template/.opencode/agents/*.md` | honored — marker 6 zero hits |
| US-0002 / US-0004 | do NOT port Cursor rules/skills as OpenCode enforcement | honored — markdown agents, no `.mdc` clone (marker 7 zero clone markers) |

- `docs/product/backlog.md` `## US-0122` L4191 — untouched (read-only). Status: OPEN. 10 ACs all `- [ ]` (unchecked).
- `docs/product/acceptance.md` US-0122 row L150 — still `- [ ]` (unchecked).
- `docs/engineering/architecture.md` `# US-0122` L1835 — not mutated by /execute loop-2 (T-anch NO-OP; only ordering remediation moved it ahead of `# US-0089`).
- `decisions/DEC-0122.md` — not mutated by /execute (T-anch NO-OP; Status: Accepted unchanged).

### 8. Byte-identical mirrors — PASS

SHA-256 comparison (active vs template):

| Pair | Result |
|------|--------|
| `docs/engineering/context/installer-owned-paths.manifest` vs `template/docs/engineering/context/installer-owned-paths.manifest` | IDENTICAL |
| `tests/us0122_contract_test.py` vs `template/tests/us0122_contract_test.py` | IDENTICAL |
| `scripts/check_intake_template_parity.py` vs `template/scripts/check_intake_template_parity.py` | IDENTICAL |

### 9. UAT probes — static contract-test mapping (no browser)

This is a pack/contract story, not a web UI. No browser probe maps. Per `/qa` step 6 (US-0092 / DEC-0078) and the orchestrator brief, ACs are mapped to pytest markers as stack-profile probes with evidence (command + output above). No `.env` read. No intake evidence mutation. No `UAT_PROBE_UNRESOLVED` — static contract-test mapping is justified by story type (code/contract, not browser/UI). **No fake browser PASS** — `browser_probe_used=false` recorded.

| AC | Probe kind | Probe ID | Evidence | Result |
|----|-----------|----------|----------|--------|
| AC-1 | pytest | `test_us0122_agent_inventory` | marker 1 PASS | PASS |
| AC-2 | pytest | `test_us0122_po_permission_object_form` + `test_us0122_auto_task_allowlist` | markers 2, 4 PASS | PASS |
| AC-3 | pytest | `test_us0122_po_production_code_denial` | marker 3 PASS | PASS |
| AC-4 | pytest | `test_us0122_prompt_size_clone_guard` | marker 7 PASS | PASS |
| AC-5 | pytest | `test_us0122_agent_inventory` + `test_us0122_security_edit_denied` + `test_us0122_role_id_parity` | markers 1, 5, 8 PASS | PASS |
| AC-6 | static | runbook h2 one-liner at `docs/engineering/runbook.md` L3987 | grep + read | PASS |
| AC-7 | pytest | `test_us0122_no_vendor_slugs_in_template` | marker 6 PASS | PASS |
| AC-8 | pytest | 8/8 markers | contract gate §1 above | PASS |
| AC-9 | static | compose 5/5 UNCHANGED + marker 8 role-id parity | §7 above | PASS |
| AC-10 | pytest | `test_us0122_po_production_code_denial` (locked matrix consumed) | marker 3 PASS | PASS |

## AC checklist

- [x] AC-1 — eight markdown agents present in `template/.opencode/agents/` (po, tech-lead, dev, qa, release, curator, security, auto).
- [x] AC-2 — Layer-1 permission matrix locked per DEC-0122 §2 (po object+deny-last; auto 7-role allow + `*` deny last).
- [x] AC-3 — success test (c) static: marker 3 proves PO cannot write production paths via deny-last + no-production-allow (host permission, not prose).
- [x] AC-4 — Layer-2 short prompts: each agent <= 2 KiB; no clone markers (marker 7).
- [x] AC-5 — US-0003 role-id parity; security `edit: deny` findings-oriented (markers 1, 5, 8).
- [x] AC-6 — runbook `## OpenCode role agents and permissions (US-0122)` h2 one-liner present (L3987).
- [x] AC-7 — no vendor slugs in `template/.opencode/agents/*.md` (marker 6 zero hits).
- [x] AC-8 — 8 contract-test markers, 8/8 PASS.
- [x] AC-9 — compose 5/5 UNCHANGED (US-0003, US-0023/BUG-0006, US-0121, US-0102/DEC-0087, US-0002/US-0004).
- [x] AC-10 — locked matrix consumed by tests (marker 3 asserts po production-code denial).

## Generated test evidence (US-0066 / DEC-0048)

- `generated_test_stack_profile`: python (pytest 9.1.1, Python 3.12.10)
- `generated_test_command`: `python -m pytest tests/us0122_contract_test.py -v`
- `generated_test_result`: pass (8/8)
- `generated_test_output_ref`: `sprints/S0122/qa-findings.md` §1 (this file)
- `generated_test_paths_ref`: `tests/us0122_contract_test.py`, `template/tests/us0122_contract_test.py`
- `generated_test_reason_code`: n/a (PASS)

## Runtime autopilot (US-0065 / DEC-0047) — N/A

This is a pack/contract story with no runtime app surface. No `runtime_startup_command`, no endpoint, no log scan. Stack profile = `static-contract` (not `node|python|go|java|dotnet` runtime). No `RUNTIME_STACK_PROFILE_UNRESOLVED` — story type is contract/static, not runtime-app. Runtime autopilot does not apply.

## Blocking findings

None. All gates green; compose 5/5 UNCHANGED; mirrors byte-identical; ACs 10/10 covered; harness `Fail: 0` literal with zero `[FAIL]` rows; architecture ordering correct; runbook mirror byte-identical; state.md active-context surface present.

## Non-blocking observations (carried forward, not blocking)

- `ik_us0122_stale_compose_count_6_vs_5` — architecture overview line "compose guards 6/6 verified" remains stale drift vs the 5/5 T-anch count. Non-blocking; doc-parity slice deferred (not US-0122 scope).
- `ik_us0122_sxxxx_literal_glob_runtime` — `sprints/Sxxxx/*` globs in DEC-0122 §2 locked matrix are runtime pattern globs (Sxxxx = sprint placeholder). Closed at plan-verify; non-blocking runtime gap.
- `ik_us0122_dev_template_agent_permission_escalation` — `dev` `template/**` allow could in principle mutate `.opencode/agents/*.md`. Closed via parity gate (byte-identical mirrors). Non-blocking; parity gate sufficient.

## Strict runtime proof (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-qa-qa-loop2-20260824T131000Z-US-0122`
- `proof_issued_at=2026-08-24T13:10:00Z`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-08-24T14:10:00Z` (UTC = issued_at + 3600s)
- `proof_hash=94B1960081A51EF41401934B5D3A386DB8C90EFADCF0149C60695DAC7A33F143`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"qa","proof_issued_at":"2026-08-24T13:10:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-01-qa-qa-loop2-20260824T131000Z-US-0122","sprint_id":"S0122","story_id":"US-0122"}`

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-US0122-qa-loop2-20260824T131000Z-fresh`
- `timestamp=2026-08-24T13:10:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required on isolation)
- `evidence_ref=sprints/S0122/qa-findings.md, handoffs/qa_to_verify.md, sprints/S0122/uat.json, sprints/S0122/uat.md`

## Next phase

`/verify-work` (fresh qa subagent per BUG-0006). STOP
