# Sprint S0120 — Task checklist (US-0120)

Total tasks: 10 (T-anch + T-001..T-010). SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1; no split needed.

## Task execution order

1. T-anch (NO-OP / verification)
2. T-001 (NEW `.cursor/commands/closure.md` — active)
3. T-003 (DEC-0052 phase→role matrix + AUTO_ROLE_CLOSURE scratchpad key) — parallel with T-004
4. T-004 (DEC-0082 ship macro + auto.md phase plan + closure spawn) — parallel with T-003
5. T-002 (NEW `template/.cursor/commands/closure.md` — byte-identical) — parallel with T-005, T-006
6. T-005 (release.md step 10-12 removal + renumbering — active + template) — parallel with T-002, T-006
7. T-006 (NEW `scripts/validate_closure_verification.py`) — parallel with T-002, T-005
8. T-007 (closure.md isolation evidence + runtime proof contract)
9. T-008 (NEW `tests/us0120_closure_phase_test.py` — 10 markers)
10. T-009 (drain hook + installer manifest rows)
11. T-010 (runbook `## Story closure (US-0120)` h2 + documentation)
12. Integration verification

## Task checklist

- [ ] **T-anch**: Verify `# US-0120` H1 anchor present at `docs/engineering/architecture.md` L2125; verify DEC-0052 phase→role matrix exists; verify DEC-0082 delivery mode table exists; verify `## Story closure (US-0120)` NOT YET in runbook.md; verify `.cursor/commands/closure.md` does NOT exist. Record results to `sprints/S0120/t-anch-verification.md`. (AC-11, AC-12 baseline; NO-OP / verification only)

- [ ] **T-001**: Create `.cursor/commands/closure.md` (active) with structure: Subagents:qe, Execution model (fresh qe subagent per BUG-0006), Isolation evidence write (US-0048/DEC-0029), Inputs (narrow-read US-0053), Outputs (4 mandatory: backlog.md flip, acceptance.md check, state.md closure checkpoint, closure-verification.md), Stop conditions, Input prerequisites (release_queue.md status=released + release-notes EXISTS + qa-findings EXISTS — fail CLOSURE_RELEASE_EVIDENCE_MISSING), Backlog reconciliation contract (US-0043/DEC-0021), Canonical status source (US-0045/DEC-0025), Orchestrator post-closure rg verification, Fail-safe reason codes, Artifact ordering (backlog→acceptance→state→closure-verification), Cross-phase ownership guard. (AC-1, AC-5, AC-7, AC-8, AC-10)

- [ ] **T-002**: Copy `.cursor/commands/closure.md` → `template/.cursor/commands/closure.md` (byte-identical). Extend `scripts/check_intake_template_parity.py` with closure scope. Verify PARITY_OK. (AC-1, AC-12)

- [ ] **T-003**: Edit `decisions/DEC-0052.md` — ADDITIVE only: (i) §1 canonical phase→role matrix row `closure \| qe \| AUTO_ROLE_CLOSURE override to curator`; (ii) §2 override contract row `AUTO_ROLE_CLOSURE \| values: qe, curator \| default: qe \| curator must not write qa-owned surfaces`; (iii) §3 preflight capability gate row `closure \| capability: role:qe or override \| fail-closed: PHASE_CAPABILITY_MISSING`. Add AUTO_ROLE_CLOSURE scratchpad key to `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md`. Existing 12 phase→role mappings UNTOUCHED. (AC-2, AC-12)

- [ ] **T-004**: Edit `decisions/DEC-0082.md` — scoped ship macro change `[release, refresh-context]` (2) → `[release, closure, refresh-context]` (3). Edit `.cursor/commands/auto.md` + `template/.cursor/commands/auto.md` — add closure to phase plan arrays in all 3 delivery modes (standard, ultra_lean, mega_quick); after /release completes → spawn closure subagent (fresh per BUG-0006); add AUTO_ROLE_CLOSURE scratchpad pointer. Other macro definitions UNTOUCHED. (AC-3, AC-4, AC-12)

- [ ] **T-005**: `.cursor/commands/release.md` + `template/.cursor/commands/release.md` (byte-identical) — remove original steps 10, 11, 12 (backlog reconciliation, derived views reconciliation, normalization report); replace with new step 10 pointer to `/closure`. Old step 13 → new step 10, old 14 → new 11, ..., sequential renumbering. Release subagent post-US-0120 focuses on release artifacts only. (AC-5, AC-12)

- [ ] **T-006**: Create `scripts/validate_closure_verification.py` — pure-stdlib validator for `closure-verification.md` schema. Required fields: `story_id`, `closure_date` (ISO-8601 UTC), `closure_role` (qe|curator), `pre_closure_status` (OPEN), `post_closure_status` (DONE), `release_evidence_refs[]`, `isolation_evidence{}`, `runtime_proof{}`. Optional: `normalization_notes`, `backward_compat_note` (extensible — R7 ACCEPTED). CLI `--file <path>` + `--self-test`. Exit 0 valid; exit 1 invalid with `CLOSURE_VERIFICATION_SCHEMA_INVALID`. (AC-6, AC-8)

- [ ] **T-007**: Extend `.cursor/commands/closure.md` + `template/.cursor/commands/closure.md` (byte-identical) with concrete isolation evidence contract + runtime proof contract sections: state.md closure checkpoint {phase_id:closure, role:qe, fresh_context_marker, timestamp, evidence_ref} per US-0048/DEC-0029; sorted-key JSON payload {delivery_mode, macro_phase:ship, orchestrator_run_id, phase_id:closure, proof_issued_at, proof_ttl_seconds:3600, role:qe, runtime_proof_id, sprint_id, story_id} per DEC-0038; fail codes RUNTIME_PROOF_MISSING/INVALID/REUSED/STALE/AMBIGUOUS_LINK. (AC-7, AC-8)

- [ ] **T-008**: Create `tests/us0120_closure_phase_test.py` with 10 contract test markers:
  - `test_us0120_closure_command_file_exists_active` (AC-1)
  - `test_us0120_closure_command_file_exists_template` (AC-1)
  - `test_us0120_closure_command_file_parity` (AC-1)
  - `test_us0120_dec_0052_phase_role_matrix_includes_closure` (AC-2)
  - `test_us0120_dec_0082_ship_macro_includes_closure` (AC-3)
  - `test_us0120_auto_phase_plan_includes_closure` (AC-4)
  - `test_us0120_release_md_steps_10_12_removed` (AC-5)
  - `test_us0120_closure_verification_schema_defined` (AC-6)
  - `test_us0120_compose_guards_unchanged` (AC-12)
  - `test_us0120_backward_compat_drain_hook` (AC-10)

  Surjective AC coverage: 1-3→AC-1, 4→AC-2, 5→AC-3, 6→AC-4, 7→AC-5, 8→AC-6, 9→AC-12, 10→AC-10; AC-7/8/9/11 indirect. (AC-9)

- [ ] **T-009**: Drain hook 3-signal detection in `/auto`: (i) `handoffs/release_queue.md` row status=released; (ii) `docs/product/backlog.md` status=OPEN; (iii) `docs/product/acceptance.md` `[ ]` unchecked → spawn `/closure` backfill (post-US-0120); pre-US-0120 → `CLOSURE_LEGACY_DRIFT` (no retroactive closure-verification.md per R8). SKIP Status:DONE stories. Extend `docs/engineering/context/installer-owned-paths.manifest` `[install_include_paths]` rows for `scripts/validate_closure_verification.py`, `.cursor/commands/closure.md`, `template/.cursor/commands/closure.md`. (AC-10, AC-12)

- [ ] **T-010**: Add `## Story closure (US-0120)` h2 to `docs/engineering/runbook.md`. Content: overview of `/closure` phase operator recipe; when to run (after /release PASS + before /refresh-context); how to verify (state.md closure checkpoint + runtime proof); how to manually trigger (for in-flight stories spawn /closure subagent); troubleshooting (CLOSURE_RELEASE_EVIDENCE_MISSING, CLOSURE_VERIFICATION_FAILED, CANONICAL_STATUS_CONFLICT, BACKLOG_STATUS_DRIFT). architecture.md `# US-0120` H1 section at L2125 verified present (NO-OP on architecture.md). (AC-11, AC-12)

## Integration verification (post T-010)

- [ ] Test gate: `python -m pytest tests/us0120_closure_phase_test.py -v` → 10/10 PASS
- [ ] Parity gate: `check_intake_template_parity.py --scope=closure-phase` PASS
- [ ] Parity gate: `.cursor/commands/closure.md` ↔ `template/.cursor/commands/closure.md` PARITY_OK
- [ ] Parity gate: `.cursor/commands/release.md` ↔ `template/.cursor/commands/release.md` PARITY_OK
- [ ] Compose gate: 6/6 UNCHANGED (US-0043/US-0045/US-0040/US-0048/US-0056/US-0096)
- [ ] Schema gate: `scripts/validate_closure_verification.py --self-test` PASS
- [ ] Drain hook smoke: `test_us0120_backward_compat_drain_hook` PASS

## Files to touch (scope)

### New (create)

- `.cursor/commands/closure.md`
- `template/.cursor/commands/closure.md` (byte-identical)
- `scripts/validate_closure_verification.py`
- `tests/us0120_closure_phase_test.py`

### Edit (scoped)

- `decisions/DEC-0052.md` (ADDITIVE rows)
- `decisions/DEC-0082.md` (ship macro 2→3)
- `.cursor/commands/auto.md` + `template/.cursor/commands/auto.md` (closure phase plan)
- `.cursor/commands/release.md` + `template/.cursor/commands/release.md` (remove steps 10-12 + pointer + renumber)
- `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` (AUTO_ROLE_CLOSURE key)
- `scripts/check_intake_template_parity.py` (add closure scope)
- `docs/engineering/runbook.md` (add `## Story closure (US-0120)` h2)
- `docs/engineering/context/installer-owned-paths.manifest` (add closure paths)

### Verify read-only (no mutation)

- `docs/engineering/architecture.md` L2125 (H1 anchor verified; NO execute-mutation)

### Compose-guard UNCHANGED (DO NOT TOUCH)

| File | Reason |
|---|---|
| `docs/product/backlog.md` | US-0045 canonical status — `/closure` mutates ONLY at execution time |
| `docs/product/acceptance.md` | US-0045 derived view — same |
| Compose-guard story surfaces (US-0043, US-0045, US-0040, US-0048, US-0056, US-0096) | 6/6 UNCHANGED — `/closure` EXECUTES their existing contracts |

## AC → Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (closure command file active+template) | T-001, T-002 |
| AC-2 (DEC-0052 phase→role matrix) | T-003 |
| AC-3 (DEC-0082 ship macro) | T-004 |
| AC-4 (/auto orchestration) | T-004 |
| AC-5 (release.md step 10-12 removal) | T-005 |
| AC-6 (closure-verification.md schema) | T-006 |
| AC-7 (closure isolation evidence) | T-001, T-007 |
| AC-8 (closure runtime proof) | T-001, T-007 |
| AC-9 (contract tests 10 markers) | T-008 |
| AC-10 (drain hook backward compat) | T-001, T-007, T-009 |
| AC-11 (documentation runbook + architecture) | T-anch (NO-OP baseline), T-010 |
| AC-12 (compose 6/6 UNCHANGED) | T-anch, T-002..T-005, T-009, T-010 (all gated) |

**Surjectivity check**: 12/12 ACs covered (AC-1..AC-12 each have ≥1 task). No `PLAN_AC_COVERAGE_GAP`.
