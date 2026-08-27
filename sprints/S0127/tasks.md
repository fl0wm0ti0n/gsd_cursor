# Sprint S0127 - Task checklist (US-0127)

Total tasks: 8 (T-anch + T-001..T-007). SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1; no split needed.

## Task execution order

1. T-anch (NO-OP / verification)
2. T-001 (Convergence lib fix `scripts/sovereign_convergence_lib.py` `_critic_jsonl_has_open` -> delegate to `read_open_blocking` + `_eval_critic_resolved` JSONL-authoritative dispatch per DQ6; + template mirror)
3. T-002 (`.cursor/commands/sovereign-critic.md` auto-resolve hook at PASS + `sovereign_critic_lib.auto_resolve_nonblocking_for_run` helper; + template mirror)
4. T-003 (NEW `scripts/sovereign_critic_hygiene.py` + `template/scripts/sovereign_critic_hygiene.py` with `--report` / `--resolve-nonblocking-for-run` / `--dry-run` / `--confirm` / `--self-test` / `--all-phases` / `--phase-id` + 6 reason codes)
5. T-004 (NEW `tests/us0127_contract_test.py` + `template/tests/us0127_contract_test.py` byte-identical — 13 markers shell, includes T-007 marker 13)
6. T-005 (runbook `### Blocking-only conjunct-3 semantics (US-0127)` + `### Hygiene CLI (US-0127)` subsections + `reason_codes.md` `## US-0127` section; active + template byte-identical)
7. T-006 (`SOVEREIGN_CRITIC_PAIRS` additive row + `check_intake_template_parity.py --scope=sovereign-critic` extension + template mirror)
8. T-007 (R2 validator regression guard marker 13 `test_us0127_validate_rejects_missing_blocking` authored inside T-004 file)
9. Integration verification

## Task checklist

- [x] **T-anch**: Verify `# US-0127` H1 anchor present in `docs/engineering/architecture.md` at L1852 (added in /architecture phase per DEC-0073 §11 / BUG-0010 heading policy; AFTER `# US-0126` and BEFORE `# US-0091`); verify approach A1 locked + R-0110 DQ1–DQ8 LOCKED; verify compose-do-not-amend 8/8 baseline (US-0104, US-0110, US-0107, US-0045, US-0048/BUG-0006, US-0053/DEC-0035, US-0103/DEC-0103, US-0056); verify 13-marker contract-test list locked in architecture AC-4 table; verify runbook subsection placement anchors (`### Evaluate convergence` L2792, `### Interpret goal_progress block` L2811, `#### Parity enforcement` L2915, `#### Related artifacts` L2923) + `reason_codes.md` `## US-0110` section at L77–L107; verify `SOVEREIGN_CRITIC_PAIRS` does NOT yet exist in `scripts/check_intake_template_parity.py`; verify `scripts/sovereign_critic_hygiene.py` + `template/scripts/sovereign_critic_hygiene.py` do NOT yet exist; verify `tests/us0127_contract_test.py` + `template/tests/us0127_contract_test.py` do NOT yet exist; verify `_critic_jsonl_has_open` root cause at `scripts/sovereign_convergence_lib.py` L318–331 still present (short-circuits on `status in ("open","blocking","fail")` AND defaults `blocking=True` when key absent); verify `read_open_blocking` predicate at `scripts/sovereign_critic_lib.py` L386–400 (`obj.get("blocking") and obj.get("status") == "open"`); verify `resolve_finding` at `scripts/sovereign_critic_lib.py` L403 (read-all + rewrite-all, idempotent). Record results to `sprints/S0127/t-anch-verification.md`. T-anch is NO-OP / verification only — NO mutation to `docs/engineering/architecture.md` in /execute; T-anch records baseline observations only (mirrors US-0126 T-anch ceremony). (AC-1, AC-2 baseline; NO-OP / verification only)

- [x] **T-001**: Edit `scripts/sovereign_convergence_lib.py` AND `template/scripts/sovereign_convergence_lib.py` (byte-identical active↔template) per architecture DQ1+DQ6 LOCKED. Replace `_critic_jsonl_has_open` body (L318–331) with a delegate to `sovereign_critic_lib.read_open_blocking(repo)` (import; do not redefine — compose read-only on US-0104 DQ7). Change `_eval_critic_resolved` dispatch (L372–404): when `handoffs/sovereign_critic_findings.jsonl` exists and is non-empty, the JSONL blocking-only predicate is authoritative and `_qa_findings_has_open_critic` is NOT consulted; when JSONL absent, fall back to the unchanged QA-markdown grep heuristic (`_qa_findings_has_open_critic`); when neither deployed, informational skip per US-0110 L3 degrade matrix. `_qa_findings_has_open_critic` and `_qa_has_cross_reviewer_section` predicates unchanged (compose read-only on US-0104 derived surfaces). MUST keep `scripts/sovereign_convergence_lib.py` byte-identical with `template/scripts/sovereign_convergence_lib.py` after edit. Tests: markers 1 (`test_us0127_open_nonblocking_passes_convergence`), 2 (`test_us0127_open_blocking_fails_convergence`), 11 (`test_us0127_compose_us0104_read_open_blocking_unchanged`), 12 (`test_us0127_compose_us0110_conjunct3_contract`), 13 (`test_us0127_validate_rejects_missing_blocking`). (AC-1)

- [x] **T-002**: Edit `.cursor/commands/sovereign-critic.md` AND `template/.cursor/commands/sovereign-critic.md` (byte-identical active↔template) per architecture DQ1 LOCKED. Add a single conditional call at the end of the command after `reconcile_findings` + JSONL append + isolation evidence, before `## Stop conditions`: `if read_open_blocking(repo) == []: auto_resolve_nonblocking_for_run(repo, orchestrator_run_id, phase_id)`. Add `auto_resolve_nonblocking_for_run(repo, orchestrator_run_id, phase_id)` helper to `scripts/sovereign_critic_lib.py` AND `template/scripts/sovereign_critic_lib.py` (byte-identical) — additive; does NOT amend `read_open_blocking`/`resolve_finding` signatures (DQ7 compose read-only). Scope key = `(orchestrator_run_id, phase_id)` pair on the finding row. Idempotent re-run via `resolve_finding` no-op. `SOVEREIGN_CRITIC_AUTORESOLVE_FAILED` is non-blocking informational (PASS verdict stands). MUST keep active ↔ template byte-identical after edit. Tests: markers 3 (`test_us0127_autoresolve_idempotent_on_rerun`), 4 (`test_us0127_autoresolve_preserves_audit_trail`), 5 (`test_us0127_autoresolve_skips_when_blocking_open`). (AC-2)

- [x] **T-003**: Create NEW `scripts/sovereign_critic_hygiene.py` AND `template/scripts/sovereign_critic_hygiene.py` (byte-identical active↔template) per architecture DQ2+DQ5 LOCKED. Surface inventory: `--report`, `--resolve-nonblocking-for-run <orchestrator_run_id>`, `--dry-run`, `--confirm`, `--self-test`, `--all-phases`, `--phase-id <phase_id>`. 6 reason codes: `HYGIENE_RESOLVE_CONFIRM_REQUIRED` (exit 2), `HYGIENE_RESOLVE_NO_CANDIDATES` (exit 0 info), `HYGIENE_RESOLVE_PARTIAL` (exit 3), `HYGIENE_RESOLVE_FAILED` (exit 4), `HYGIENE_REPORT_EMPTY` (exit 0 info), `HYGIENE_RESOLVE_PHASE_SCOPE_REQUIRED` (exit 2). Operator-only posture — `/auto` orchestrator does NOT call it during a run (document operator-only-when-quiet contract in runbook `### Hygiene CLI (US-0127)` subsection — Q3 accepted: no advisory lock; `/auto` is single-threaded per repo; `resolve_finding` already uses read-all + rewrite-all). MUST keep `scripts/sovereign_critic_hygiene.py` byte-identical with `template/scripts/sovereign_critic_hygiene.py` after edit. Tests: markers 6 (`test_us0127_hygiene_report`), 7 (`test_us0127_hygiene_dry_run`), 8 (`test_us0127_hygiene_confirm_required`), 9 (`test_us0127_hygiene_self_test`), 10 (`test_us0127_hygiene_phase_scope_required`). (AC-3)

- [x] **T-004**: Create `tests/us0127_contract_test.py` with 13 markers per architecture DQ3 LOCKED + R-0110 R2 (marker 13 validator guard). Markers:
  1. `test_us0127_open_nonblocking_passes_convergence` — fixture JSONL with `status=open, blocking=false` row; assert `_eval_critic_resolved` returns pass/skip (not fail) (AC-1/AC-4).
  2. `test_us0127_open_blocking_fails_convergence` — fixture JSONL with `status=open, blocking=true` row; assert `_eval_critic_resolved` returns fail with `CONVERGENCE_CROSS_REVIEWER_OPEN` (AC-1/AC-4).
  3. `test_us0127_autoresolve_idempotent_on_rerun` — call `auto_resolve_nonblocking_for_run` twice on same fixture; assert second call is a no-op (status already `resolved`) (AC-2/AC-4).
  4. `test_us0127_autoresolve_preserves_audit_trail` — after auto-resolve, assert original finding rows still present (status changed to `resolved`; no rows deleted; finding_id + lens + timestamp preserved) (AC-2/AC-4).
  5. `test_us0127_autoresolve_skips_when_blocking_open` — fixture JSONL with at least one `blocking=true, status=open` row; assert `auto_resolve_nonblocking_for_run` is NOT called (hook conditional on `read_open_blocking(repo) == []`) (AC-2/AC-4).
  6. `test_us0127_hygiene_report` — run `scripts/sovereign_critic_hygiene.py --report` on fixture; assert exit 0 + report output (AC-3).
  7. `test_us0127_hygiene_dry_run` — run `--resolve-nonblocking-for-run <id> --dry-run`; assert no JSONL mutation + candidate list printed (AC-3).
  8. `test_us0127_hygiene_confirm_required` — run `--resolve-nonblocking-for-run <id>` WITHOUT `--confirm`; assert exit 2 + `HYGIENE_RESOLVE_CONFIRM_REQUIRED` (AC-3).
  9. `test_us0127_hygiene_self_test` — run `--self-test`; assert exit 0 (AC-3).
  10. `test_us0127_hygiene_phase_scope_required` — run `--resolve-nonblocking-for-run <id>` WITHOUT `--all-phases` and WITHOUT `--phase-id`; assert exit 2 + `HYGIENE_RESOLVE_PHASE_SCOPE_REQUIRED` (AC-3).
  11. `test_us0127_compose_us0104_read_open_blocking_unchanged` — compose regression guard: assert `sovereign_critic_lib.read_open_blocking` signature + predicate unchanged (`obj.get("blocking") and obj.get("status") == "open"`) (DQ7).
  12. `test_us0127_compose_us0110_conjunct3_contract` — compose regression guard: assert five-conjunct structure + degrade matrix + `CONVERGENCE_CROSS_REVIEWER_OPEN` reason code unchanged (DQ8).
  13. `test_us0127_validate_rejects_missing_blocking` — R2 validator regression guard: fixture JSONL row with `status=open` but NO `blocking` key; assert `sovereign_critic_validate.py --enforce` rejects it (non-zero exit + clear error) (R2 — supports AC-1/AC-4).
  All markers static/fixture-based; no live critic spawn. Mirror to `template/tests/us0127_contract_test.py` byte-identical for parity pairing. (AC-4)

- [x] **T-005**: Edit `docs/engineering/runbook.md` AND `template/docs/engineering/runbook.md` (byte-identical active↔template) per architecture DQ4 LOCKED. New `### Blocking-only conjunct-3 semantics (US-0127)` subsection after `### Evaluate convergence` (L2792) and before `### Interpret goal_progress block` (L2811) — documents that `CONVERGENCE_CROSS_REVIEWER_OPEN` now requires `blocking=true` per US-0110 L3 conjunct-3 / DEC-0110 §10, and that informational `status=open, blocking=false` PASS concurrence rows no longer block convergence. New `### Hygiene CLI (US-0127)` subsection after `#### Parity enforcement` (L2915) and before `#### Related artifacts` (L2923) — documents the `scripts/sovereign_critic_hygiene.py` inventory (`--report`, `--resolve-nonblocking-for-run`, `--dry-run`, `--confirm`, `--self-test`, `--all-phases`, `--phase-id`), the 6 reason codes, and the operator-only-when-quiet contract (no advisory lock; `/auto` is single-threaded per repo; `resolve_finding` already uses read-all + rewrite-all). Edit `docs/engineering/reason_codes.md` AND `template/docs/engineering/reason_codes.md` (byte-identical): new `## US-0127: Convergence critic conjunct hygiene (DEC-0110 §10 / DEC-0104 §11)` section after the US-0110 section (L77–L107) with the 6 hygiene reason codes + `SOVEREIGN_CRITIC_AUTORESOLVE_FAILED` (info) + clarifying note that `CONVERGENCE_CROSS_REVIEWER_OPEN` now requires `blocking=true` (description amendment only; no US-0110 reason-code renumbering). MUST keep active ↔ template byte-identical after edit. (AC-5)

- [x] **T-006**: Edit `scripts/check_intake_template_parity.py` AND `template/scripts/check_intake_template_parity.py` (byte-identical active↔template) per architecture DQ5 LOCKED. Add NEW `SOVEREIGN_CRITIC_PAIRS: tuple[tuple[str, str], ...]` tuple table with the hygiene script pair: `("scripts/sovereign_critic_hygiene.py", "template/scripts/sovereign_critic_hygiene.py")`. Add NEW `"sovereign-critic": SOVEREIGN_CRITIC_PAIRS` entry to `SCOPES` dict. Add `SOVEREIGN_CRITIC_PAIRS` to the `all` union tuple. Add `"--scope=sovereign-critic"` to the docstring help. Existing scopes unchanged (additive only). `SOVEREIGN_CONVERGENCE_PAIRS` existing rows confirmed (no new row — convergence lib mirror already present per architecture DQ5; if `SOVEREIGN_CONVERGENCE_PAIRS` does not yet exist, execute may add it with the convergence lib pair `scripts/sovereign_convergence_lib.py` ↔ `template/scripts/sovereign_convergence_lib.py` per DQ5, but architecture DQ5 says "existing rows confirmed" — execute verifies and adds only if missing). MUST keep `scripts/check_intake_template_parity.py` byte-identical with `template/scripts/check_intake_template_parity.py` after edit. Tests: marker 11/12 (compose regression guards) + `python scripts/check_intake_template_parity.py --scope=sovereign-critic` exit 0. (AC-6)

- [x] **T-007**: Author `test_us0127_validate_rejects_missing_blocking` (marker 13) inside `tests/us0127_contract_test.py` per architecture R2 + R-0110 R2 LOCKED. Marker 13 builds a fixture findings JSONL row with `status=open` but NO `blocking` key and asserts `sovereign_critic_validate.py --enforce` rejects it (non-zero exit + clear error). This is the R2 mitigation: prevent a future regression where `blocking` key is absent from a finding row (which would mask the `_critic_jsonl_has_open` narrowing — if `blocking` defaults to `True` when absent, then a missing-key row would be treated as blocking and fail convergence even though it is informational). Mirror to `template/tests/us0127_contract_test.py` byte-identical. (R2 — supports AC-1/AC-4 regression guard)

## Integration verification (post T-007 + T-004)

- [x] Test gate: `python -m pytest tests/us0127_contract_test.py -v` → 13/13 PASS
- [x] Parity gate: `check_intake_template_parity.py --scope=sovereign-critic` PASS
- [x] Parity gate: active + template sovereign_convergence_lib.py byte-identical
- [x] Parity gate: active + template sovereign_critic_lib.py byte-identical
- [x] Parity gate: active + template sovereign_critic_hygiene.py byte-identical
- [x] Parity gate: active + template sovereign-critic.md byte-identical
- [x] Parity gate: active + template runbook.md byte-identical
- [x] Parity gate: active + template reason_codes.md byte-identical
- [x] Parity gate: active + template check_intake_template_parity.py byte-identical
- [x] Parity gate: active + template us0127_contract_test.py byte-identical
- [x] Compose gate: 8/8 UNCHANGED
- [x] Validator gate: `sovereign_critic_validate.py --enforce` rejects missing `blocking` key (marker 13)
- [x] No-secrets gate: `api_key`/`apikey`/`sk-`/`auth.json`/`.env` grep zero hits on edited files

## Files to touch (scope)

### New (create)

- `scripts/sovereign_critic_hygiene.py`
- `template/scripts/sovereign_critic_hygiene.py` (byte-identical mirror for parity)
- `tests/us0127_contract_test.py`
- `template/tests/us0127_contract_test.py` (byte-identical mirror for parity)
- `sprints/S0127/t-anch-verification.md`

### Edit (scoped, additive only)

- `scripts/sovereign_convergence_lib.py` (replace `_critic_jsonl_has_open` body + change `_eval_critic_resolved` dispatch per DQ6)
- `template/scripts/sovereign_convergence_lib.py` (byte-identical mirror)
- `scripts/sovereign_critic_lib.py` (additive `auto_resolve_nonblocking_for_run` helper)
- `template/scripts/sovereign_critic_lib.py` (byte-identical mirror)
- `.cursor/commands/sovereign-critic.md` (add auto-resolve hook at PASS)
- `template/.cursor/commands/sovereign-critic.md` (byte-identical mirror)
- `docs/engineering/runbook.md` (append `### Blocking-only conjunct-3 semantics (US-0127)` + `### Hygiene CLI (US-0127)` subsections)
- `template/docs/engineering/runbook.md` (byte-identical mirror)
- `docs/engineering/reason_codes.md` (append `## US-0127` section)
- `template/docs/engineering/reason_codes.md` (byte-identical mirror)
- `scripts/check_intake_template_parity.py` (add `SOVEREIGN_CRITIC_PAIRS` + `--scope=sovereign-critic`)
- `template/scripts/check_intake_template_parity.py` (byte-identical mirror)

### Verify read-only (no mutation)

- `docs/engineering/architecture.md # US-0127` (T-anch NO-OP; DQ1..DQ8 locks + 13-marker table are the locked source of truth — execute ships the runbook/reason_codes body, NOT architecture.md)
- `docs/product/backlog.md ## US-0127` (read-only — US-0045 canonical status)
- `docs/product/acceptance.md` US-0127 row (read-only — US-0045 derived view)
- `handoffs/intake_evidence/US-0127-intake-20260825.json` (read-only — never mutate prior intake evidence)
- `scripts/sovereign_critic_validate.py` (read-only — marker 13 asserts its behavior; do not amend)

### Compose-guard UNCHANGED (DO NOT TOUCH)

| File | Reason |
|---|---|
| `docs/product/backlog.md` | US-0045 canonical status — `/closure` mutates ONLY at execution time |
| `docs/product/acceptance.md` | US-0045 derived view — same |
| `decisions/` | No new DEC (per R-0110 §Companion DEC recommendation) |
| US-0104 surfaces (`sovereign_critic_lib.read_open_blocking` / `resolve_finding` / findings JSONL schema / `build_qa_cross_reviewer_block` / `sovereign_critic_validate.py`) | compose read-only — DQ7 |
| US-0110 surfaces (five-conjunct structure / degrade matrix / `CONVERGENCE_CROSS_REVIEWER_OPEN` reason code) | compose read-only — DQ8 |
| US-0107 surfaces (deferral register / drain-generate / sovereign loop stop matrix) | compose read-only — DQ8 |
| US-0121..US-0126 DONE rows | do not reopen |

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (Blocking-only check) | T-001, T-004 (markers 1, 2, 11, 12, 13), T-007 (marker 13) |
| AC-2 (Auto-resolve non-blocking) | T-002, T-004 (markers 3, 4, 5) |
| AC-3 (Hygiene CLI) | T-003, T-004 (markers 6, 7, 8, 9, 10) |
| AC-4 (Contract tests) | T-004 (all 13 markers), T-007 (marker 13) |
| AC-5 (Operator docs) | T-005 (runbook subsections + reason_codes.md section) |
| AC-6 (Template parity) | T-006 (SOVEREIGN_CRITIC_PAIRS + --scope=sovereign-critic) |

**Surjectivity check**: 6/6 ACs covered (AC-1..AC-6 each have at least 1 task). No `PLAN_AC_COVERAGE_GAP`.
