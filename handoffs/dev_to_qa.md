## Dev -> QA Handoff — S0076 / US-0090 (2026-04-18T12:00:00Z)

> **2026-04-18T12:00:00Z** — `/execute` (fresh **dev**, `orchestrator_run_id=auto-20260418-01`, backlog-drain segment, `AUTO_QUIET=1`) for **US-0090** / **`S0076`**. All **10 / 10** tasks (T-001..T-010) flipped `todo -> done` in `sprints/S0076/tasks.md`. Story **US-0090** remains **OPEN** (US-0045). Ready for `/qa` acceptance verification.

### Runtime proof (DEC-0038)

- `runtime_proof_id=rp-execute-S0076-US-0090-dev`
- `proof_hash=321739b3b8ec3a16ada461c41b37c81e93bf853f51153bb7223d85d304ca5107` (sha256 of canonical JSON tuple `{"orchestrator_run_id":"auto-20260418-01","phase_id":"execute","proof_issued_at":"2026-04-18T12:00:00Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-execute-S0076-US-0090-dev"}`)
- `proof_issued_at=2026-04-18T12:00:00Z`, `proof_ttl_seconds=3600`, `phase_id=execute`, `role=dev`

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=execute`, `role=dev`, `fresh_context_marker=true`, `fresh_context_marker_value=dev-S0076-US0090-execute-20260418T120000Z-fresh`, `timestamp=2026-04-18T12:00:00Z`, `evidence_ref=sprints/S0076/summary.md#execute-phase-S0076-US0090-2026-04-18`.

### Scope delivered (AC-1..AC-8 surface)

| Task | ACs | DEC-0073 § | Surface | Status |
|------|-----|-----------|---------|--------|
| T-001 | AC-1..AC-5 | §2/§3/§4/§5/§6/§7/§8 | `scripts/caveman_compress_input.py` + `template/` mirror | done |
| T-002 | AC-5 | §8 + §9 row 2 | `docs/engineering/runbook.md` **`### Caveman input compression (US-0090)`** + template mirror | done |
| T-003 | AC-7 | §1 + §9 row 3 | `docs/engineering/auto-orchestration-reference.md` new companion section + template mirror | done |
| T-004 | AC-2 | §3 | `.gitignore` sidecar anchor + `docs/.caveman-originals/.gitkeep` (active-only) | done |
| T-005 | AC-6 + AC-8 | §6 + §9 | 13 new `test_caveman_compress_input_*` subtests in `tests/auto_command_contract_test.py` | done |
| T-006 | AC-6 | §9 fixture classes 1-8 | `tests/fixtures/caveman_compress/` 8 classes, 51 fixture files (class 2 × 9 zones; class 3 × 33 deny classes) | done |
| T-007 | AC-8 | §10 | `scripts/caveman_compress_input.py` added to `installer-owned-paths.manifest` (`[install_include_paths]` + `[clean_paths]` + `[required_install_script_paths]`) + template mirror | done |
| T-008 | AC-8 | §10 | `scripts/check_intake_template_parity.py` `--scope=caveman-compress` / `--scope=all` + template mirror | done |
| T-009 | AC-6 + AC-8 | §10 | `test_caveman_compress_input_shipped_by_installer` class in `tests/installer_completeness_bug0003_test.py` + harness section **26T** in both `tests/run-tests.ps1` / `tests/run-tests.sh` | done |
| T-010 | AC-7 | §9 row 4 | `test_caveman_compress_input_architecture_linkage` assert-only subtest (8 linkage tokens: DEC-0073, DEC-0072, R-0073, `# US-0089`, US-0053, US-0085, US-0078, DEC-0060) | done |

### Key invariants preserved (DEC-0072 + DEC-0073)

- **Default off**: mutation requires `CAVEMAN_COMPRESS_INPUT=1` + non-empty `CAVEMAN_FILE_SCOPE` + `--write`; empty scope fails closed with `CAVEMAN_COMPRESS_SCOPE_EMPTY`; flag conflicts fail closed with `CAVEMAN_COMPRESS_FLAG_CONFLICT`.
- **Deny always wins over allow**: evaluation order hard-coded baseline → `.gitignore` secret merge → optional `.cursorignore` overlay (`CAVEMAN_COMPRESS_INGEST_CURSORIGNORE=1`) → allow-list → literal-region scan → write.
- **Sidecar-first atomic write** at `docs/.caveman-originals/<relative/path>/<file>`.
- **9-zone literal-region invariant** (DEC-0072 §4) reused verbatim — pre-write + post-transform byte-equality scan on zones.
- **Safe-mode algorithm only in v1**: duplicate-blank collapse + trailing-whitespace trim + LF normalize + EOF-newline preserve — strictly idempotent by construction; aggressive mode deferred (R8).
- **9-code reason vocabulary** across 3 families (Gating / Scope / Integrity); `deny_list_version` SHA-256 stable across consecutive `--report` invocations; no new codes authored beyond the 9.
- **Negative parity**: `.cursor/rules/caveman.mdc` SHA-256 **`E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`** **unchanged end-to-end** (R10 mitigation); `.cursor/skills/its-magic/SKILL.md` unchanged; `.cursor/scratchpad.md` unchanged; `template/.cursor/scratchpad.local.example.md` unchanged.
- **No new runtime deps** (stdlib-only Python); no `--mode` / `--purge-orphans` flags in v1; no `npx skills add` leak.
- **Existing `test_caveman_default_off_*` subtests** (DEC-0072 §6 row 6 pinned class) **byte-unchanged** — only additions.

### Test evidence

- `python -m pytest tests/auto_command_contract_test.py -q -k caveman` -> exit 0, **23 passed / 134 subtests / 0 failed**.
- `python -m pytest tests/installer_completeness_bug0003_test.py -q` -> exit 0, **4 passed / 0 failed** (including new `test_caveman_compress_input_shipped_by_installer`).
- `python scripts/check_intake_template_parity.py --scope=caveman-compress` -> **`[INTAKE_TEMPLATE_PARITY_OK]`** (exit 0).
- `python scripts/check_intake_template_parity.py --scope=all` -> **`[INTAKE_TEMPLATE_PARITY_OK]`** (exit 0).
- `python scripts/enforce-triad-hot-surface.py --check` post-rollover -> exit 0.
- `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` -> **`[BUG_VALIDATION_OK]`** (exit 0, pre- and post-execute).
- `scripts/caveman_compress_input.py --help` exits 0 with flags `--dry-run`, `--write`, `--verify-originals`, `--report`; unknown flags fail closed.

### Template parity (US-0017)

All four sanctioned pairs byte-identical at handoff:
- `scripts/caveman_compress_input.py` ↔ `template/scripts/caveman_compress_input.py` (SHA-256 `CA5F6FDF276FBD1BC9B212BE723E83661503FE2CA9D27D721B67CA4D4DA1C231`).
- `docs/engineering/context/installer-owned-paths.manifest` ↔ template mirror (SHA-256 `D99EB4B674FAD57299BEE360172B00F22E51035E52FC4558F03E8CACD1937212`).
- `docs/engineering/runbook.md` ↔ `template/docs/engineering/runbook.md` (SHA-256 `B7ED93F224809A24D18763DCB7EB556FDDACEF0ED039113EA603A4B1BA6A6DA7`).
- `docs/engineering/auto-orchestration-reference.md` ↔ template mirror (SHA-256 `86952E631B908AE7169C8FDE86516C6C523CD55C987272CF2BF5A098A3A7224C`).
- `scripts/check_intake_template_parity.py` ↔ template mirror (byte-identical).

No new `template/` files beyond the sanctioned mirrors. `template/docs/engineering/architecture.md` pre-existed from prior work and is **not** touched by US-0090 (active-only precedent per DEC-0072 §7 row 6).

### Triad hot-surface rollover (DEC-0054)

Post-append `state.md` `--check` flagged `STATE_ARCHIVE_REQUIRED` at 1207 / 1200 lines; `--rollover` produced `docs/engineering/state-archive/state-pack-20260418-k.md` (`moved=1 unit`); final `--check` exit 0.

### Ambiguity resolutions surfaced (AUTO_QUIET=1)

1. **DEC-0073 §1 "replace" vs DEC-0072 §6 row 6 byte-unchanged**: DEC-0073 §1 calls for replacing the existing two-sentence non-substitution paragraph with a three-sentence version; DEC-0072 §6 row 6 pins `test_caveman_default_off_reference_non_substitution_paragraph` byte-unchanged (it asserts the exact two-sentence string). Conservative resolution: **preserve** the two-sentence original AND **append** the new three-sentence paragraph as a distinct companion block (new `### TOKEN_PROFILE × CAVEMAN_MODE × CAVEMAN_COMPRESS_INPUT non-substitution (US-0090 / DEC-0073 §1)` section in reference + new runbook subsection) in both active and `template/`. QA should confirm both paragraphs coexist in all four files.
2. **`test_caveman_architecture_section_bottom_appended_and_linked`**: this test (authored at `/architecture`) asserted `# US-0089` is the last `# US-xxxx` heading in `architecture.md`, but `/architecture` also appended `# US-0090` below it. Since this test is **not** in the DEC-0072 §6 row 6 pinned class, its final assertion was relaxed to accept `# US-0090` as the **single permissible successor** heading after `# US-0089`, preserving the "bottom-appended and linked" intent.
3. **`test_caveman_compress_input_architecture_linkage` (T-010)**: initial draft asserted `template/docs/engineering/architecture.md` does not exist; that file already exists from prior work unrelated to US-0090. Removed the negative assertion; the test now verifies only active-file linkage.

### Pre-existing failure baseline (not regressions)

24 pre-existing failures in `tests/auto_command_contract_test.py` (`test_slim_auto_retains_gate_markers`, `test_template_*_literal_parity_active`, remote-automation profile keys, etc.) were captured via `git stash` pre-execute and compared post-execute. Failure set is **identical** save for the one deliberate relaxation documented in Ambiguity resolution #2. QA should treat these 24 as out-of-scope for US-0090 (they predate the sprint and do not touch Caveman input compression surfaces).

### Verdict ready for QA verification

- All 10 tasks done; all 10 AC-level acceptance checks satisfied on `sprints/S0076/tasks.md`.
- `sprints/S0076/plan-verify.json` remains `status=PASS` (not mutated by execute).
- Backlog `## US-0090` `execute_notes (2026-04-18, Dev, auto-20260418-01)` appended; **US-0090 remains OPEN** per US-0045 (closure remains a `/release` responsibility).
- Ready for **`/qa`** (fresh **qa** context) for **`S0076`** / **US-0090** — expected outputs: `sprints/S0076/qa-findings.md` populated, AC-1..AC-8 verdicts, UAT rehearsal notes, runtime proof + isolation evidence appended to `docs/engineering/state.md`.

---

## Dev -> QA Handoff — US-0089 / S0075 — QA-loop cycle 2 (2026-04-18T16:00:00Z) -- superseded by **S0076 / US-0090** above

> **2026-04-18T16:00:00Z** — `/execute` re-run (fresh **dev**, `orchestrator_run_id=auto-20260418-01`, **QA-loop cycle 2 of 5**) for **US-0089** / **S0075**. Surgical remediation of the prior `/qa` FAIL (`runtime_proof_id=rp-auto-20260418-01-qa-qa-20260418T150000Z-S0075-US0089`, `proof_hash=3bef1259f94c6c5d79cf30a45efbbd28765da263a6ef6ef4918010992fc809ca`, 2026-04-18T15:00:00Z). Story **US-0089** remains **OPEN** (US-0045). T-001..T-008 still **done**. Ready for `/qa` re-verification.

### Scope (cycle 2 -- surgical only)

Single blocking finding from prior `/qa` cleared: `tests/run-tests.ps1` rule-count assertion was stale at `"5 rules exist"` / `-eq 5`. **DEC-0072 §7 row 3** legitimately added `.cursor/rules/caveman.mdc` + `template/.cursor/rules/caveman.mdc`, raising the count to **6**. Bumped both POSIX-parity check-in runners. No DEC / architecture / backlog AC / rule-file edit performed. AC-1..AC-8 surface untouched.

### Files touched (cycle 2)

| File | Line | Before | After |
|------|------|--------|-------|
| `tests/run-tests.ps1` | 77 | `Assert-True "5 rules exist" ((Count-Files (Join-Path $tpl ".cursor\rules") "*.mdc") -eq 5)` | `Assert-True "6 rules exist" ((Count-Files (Join-Path $tpl ".cursor\rules") "*.mdc") -eq 6)` |
| `tests/run-tests.sh` | 87 | `assert_true "5 rules exist" "[ $rule_count -eq 5 ]"` | `assert_true "6 rules exist" "[ $rule_count -eq 6 ]"` |

Template parity (US-0017): no `template/tests/run-tests.*` mirror exists (test runners are active-only, consistent with row 7 of DEC-0072 §7); no template edit required.

### Verified rule-file count

`.cursor/rules/` contains exactly **6** `.mdc` files: `caveman.mdc`, `coding-standards.mdc`, `core.mdc`, `escalation.mdc`, `handoffs.mdc`, `quality.mdc`. `template/.cursor/rules/` mirrors the same six files. Assertion bump matches reality.

### Test evidence (post-fix, pre-fix in parens)

- Canonical check-in: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` -> `tests/report.md` `Timestamp=2026-04-18T12:32:24Z`, **Pass=783 / Fail=11** (pre-fix: Pass=782 / Fail=12). Specifically the failing `5 rules exist` assertion is now `[PASS] 6 rules exist`. Remaining 11 failures are pre-existing US-0086 / US-0087 / US-0088 drift (observational, disjoint from US-0089), exactly matching QA's stated post-fix expectation.
- Targeted Caveman pytest: `python -m pytest tests/auto_command_contract_test.py -q -k caveman` -> exit 0, **11 passed / 19 deselected / 119 subtests / 0 failed** (unchanged from cycle 1 baseline).
- Full contract module: `python -m pytest tests/auto_command_contract_test.py -q` -> exit 1, **27 passed / 24 failed / 192 subtests** (24 pre-existing failures unchanged; no new regression).
- Bug validator: `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` -> `[BUG_VALIDATION_OK]` (exit 0).

### Verdict ready for QA re-verification

DONE -- single blocking finding cleared with minimal scope; AC-1..AC-8 surface and default-off invariant untouched; template parity rows 2-5 + negative parity row 8 still UPHELD byte-for-byte; pre-existing observational failures untouched (out of US-0089 scope).

### Strict runtime proof (DEC-0038, cycle 2)

- `orchestrator_run_id=auto-20260418-01`
- `runtime_proof_id=rp-auto-20260418-01-execute-dev-20260418T160000Z-S0075-US0089-loop2`
- `phase_id=execute`, `role=dev`
- `proof_issued_at=2026-04-18T16:00:00Z`, `proof_ttl_seconds=3600`
- `proof_hash=c43fc4471e31d838f492fcd4054fedd80d11300588290f51801189cb0654e937`

Canonical payload (sorted-key JSON): `{"orchestrator_run_id":"auto-20260418-01","phase_id":"execute","proof_issued_at":"2026-04-18T16:00:00Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260418-01-execute-dev-20260418T160000Z-S0075-US0089-loop2"}`.

### Isolation evidence (US-0048 / DEC-0029, cycle 2)

- `phase_id=execute`, `role=dev`
- `fresh_context_marker=dev-US0089-execute-20260418T160000Z-S0075-loop2-fresh`
- `timestamp=2026-04-18T16:00:00Z`
- `evidence_ref=tests/run-tests.ps1,tests/run-tests.sh,sprints/S0075/summary.md,handoffs/dev_to_qa.md,handoffs/resume_brief.md,docs/engineering/state.md,tests/report.md`

### Next

- `/qa` (fresh **qa** context) for **S0075 / US-0089** -- QA-loop cycle 2 re-verification (`AUTO_LOOP_MAX_CYCLES=5`, current cycle 2/5).

---

## Dev -> QA Handoff — US-0089 / S0075

> **2026-04-18T14:00:00Z** — `/execute` complete (dev, `orchestrator_run_id=auto-20260418-01`). Story **US-0089** remains **OPEN** (US-0045). Sprint **S0075**. All 8 tasks (T-001..T-008) done. Ready for `/qa`.

### Scope delivered

Implemented Caveman mode (US-0089) as a **response-side** optional terse/imperative voice overlay, default off. Every change preserves the DEC-0072 default-off byte-for-byte invariant (with `CAVEMAN_MODE=0` or absent, pre-US-0089 behavior is unchanged).

| Task | AC | What landed |
|------|----|-------------|
| T-001 | AC-1 | Four locked scratchpad key lines + `## Caveman mode (US-0089)` comment block in active baseline scratchpad and active + template example. |
| T-002 | AC-2 | Default-off invariant subtests items **6–8** of DEC-0072 §6 (existing tokens intact, AUTO_QUIET gate vocabulary preserved, no vendor install leak). |
| T-003 | AC-3 | New `.cursor/rules/caveman.mdc` + `template/` mirror with 9-zone literal-region invariant and 5 canonical operator toggle phrases. |
| T-004 | AC-4 | `TOKEN_PROFILE × CAVEMAN_MODE` non-substitution paragraph in `auto-orchestration-reference.md` (active + template). |
| T-005 | AC-5 | `### Caveman mode (US-0089)` subsection in runbook (active + template) with key table, phrase catalog, non-substitution paragraph, determinism semantics. |
| T-006 | AC-6 | Default-off invariant subtests items **1–5** of DEC-0072 §6 (scratchpad keys active, scratchpad keys parity, rule file present active/template, reference non-substitution paragraph, runbook operator phrases). |
| T-007 | AC-7 | Assertion-only test verifying `# US-0089` is bottom-appended in `architecture.md` and linked from `backlog.md` + `decisions.md`. No rewrite. |
| T-008 | AC-8 | Template parity sweep test across the four touched pairs + negative-parity test guarding `.cursor/skills/its-magic/SKILL.md`. |

### Tests added (all in `tests/auto_command_contract_test.py`)

1. `test_caveman_default_off_scratchpad_keys_active`
2. `test_caveman_default_off_scratchpad_keys_example_parity`
3. `test_caveman_default_off_rule_file_present_active_template`
4. `test_caveman_default_off_reference_non_substitution_paragraph`
5. `test_caveman_default_off_runbook_operator_phrases`
6. `test_caveman_default_off_existing_contract_tokens_intact`
7. `test_caveman_default_off_non_suppressible_gate_vocab_preserved`
8. `test_caveman_default_off_no_vendor_install_leak`
9. `test_caveman_architecture_section_bottom_appended_and_linked`
10. `test_caveman_template_parity_sweep`
11. `test_caveman_skill_file_negative_parity`

### File touchpoints (grouped)

**Active**:

- `.cursor/scratchpad.md`
- `.cursor/scratchpad.local.example.md`
- `.cursor/rules/caveman.mdc` (**new**)
- `docs/engineering/auto-orchestration-reference.md`
- `docs/engineering/runbook.md`
- `tests/auto_command_contract_test.py`

**Template parity**:

- `template/.cursor/scratchpad.local.example.md`
- `template/.cursor/rules/caveman.mdc` (**new**)
- `template/docs/engineering/auto-orchestration-reference.md`
- `template/docs/engineering/runbook.md`

**Explicit non-touches** (per DEC-0072 §8 / negative parity):

- `.cursor/skills/its-magic/SKILL.md`
- `decisions/DEC-0072.md`
- `docs/engineering/architecture.md` (bottom-appended by `/architecture`; assertion-only verification by T-007)
- `docs/product/backlog.md` acceptance rows
- `template/.cursor/scratchpad.md` (baseline scratchpad n/a per US-0073 / DEC-0055)

### Test command (TEST_COMMAND)

```
python -m pytest tests/auto_command_contract_test.py -k caveman --tb=short -q
```

Expected: **11 passed, 19 deselected, 119 subtests passed**.

Broader coverage (all Caveman + all pre-existing contract tests):

```
python -m pytest tests/auto_command_contract_test.py --tb=no -q
python -m pytest -q --tb=no
python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance
```

### Test results (as of 2026-04-18T14:00:00Z)

- Targeted (Caveman only): **11 passed**, 0 failed.
- Full `auto_command_contract_test.py` module: **27 passed**, **24 failed** — **all 24 failures are pre-existing** (US-0086/US-0087/US-0088 drift in `.cursor/commands/auto.md` and scratchpad baseline/template parity). Verified via git-stash baseline measurement: removing US-0089 changes yields **24 failed / 16 passed**; adding US-0089 yields **24 failed / 27 passed**. Net change: **+11 passes, +0 failures**.
- Full repo suite: **66 passed**, **24 failed** (pre-existing), **4 skipped**, 192 subtests passed.
- **`[BUG_VALIDATION_OK]`**.

### Known findings (for QA awareness)

- **Pre-existing failures** out of US-0089 scope (documented above). Recommend QA verdict **PASS** for US-0089 based on the 11 targeted Caveman subtests and the default-off invariant guarantee; the 24 pre-existing failures should be triaged separately (likely candidates for a drift-repair story or new BUG issues; not US-0089's regression surface).
- **No DEC authored** — decision rights stay with `/architecture` (DEC-0072 already locked).
- **No story status change** — US-0089 remains OPEN per US-0045 (flips at `/verify-work` or `/release`).
- **No vendor install** — JuliusBrussee/caveman (MIT) referenced in documentation only; no package-manager install recipe surfaced anywhere.
- **`CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE`** are reserved for **US-0090** and remain documented no-ops in US-0089.

### Contract-test status

- Caveman contract tests: **GREEN**.
- Default-off invariant (DEC-0072 §6 all 8 items): **GREEN**.
- Template parity (DEC-0072 §7, rows 1–7): **GREEN**.
- Negative parity (DEC-0072 §7 row 8 / §8): **GREEN** (`.cursor/skills/its-magic/SKILL.md` free of US-0089 tokens).

### Strict runtime proof

- `orchestrator_run_id=auto-20260418-01`
- `runtime_proof_id=rp-auto-20260418-01-execute-dev-20260418T140000Z-S0075-US0089`
- `phase_id=execute`
- `role=dev`
- `proof_issued_at=2026-04-18T14:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=8a9f9ecc8dce7e31806f5dad53d205e40d9e5e325ecd7ce74b0a64ec42262482`

### Next

- `/qa` (fresh qa subagent) for S0075 / US-0089.

---

## Dev -> QA Handoff — US-0086 / S0074

> **2026-04-13T21:05:00Z** — `/execute` complete (dev, `orchestrator_run_id=auto-20260405-01`). Story **US-0086** remains **OPEN** (US-0045). Sprint **S0074**. All 10 tasks (T-001..T-010) done. Ready for `/qa`.

### What changed

1. **Scratchpad automation profile keys** (AC-1):
   - `.cursor/scratchpad.md`
   - `template/.cursor/scratchpad.md`
   - `.cursor/scratchpad.local.example.md`
   - `template/.cursor/scratchpad.local.example.md`
   Added `AUTO_REMOTE_AUTOMATION_PROFILE` and `AUTO_REMOTE_ENVIRONMENT_LABEL`
   with default-off/manual-safe values.

2. **Manual vs automation mode docs** (AC-2, AC-6, AC-7):
   - `docs/engineering/runbook.md`
   - `template/docs/engineering/runbook.md`
   - `docs/engineering/runtime-connectivity.md`
   - `template/docs/engineering/runtime-connectivity.md`
   Added deterministic mode split, fail-closed reason codes, names-only tuple
   contract, and optional deterministic CI routing recipe.

3. **Deterministic routing contract updates** (AC-3, AC-4):
   - `.cursor/commands/auto.md`
   - `template/.cursor/commands/auto.md`
   - `docs/engineering/auto-orchestration-reference.md`
   - `template/docs/engineering/auto-orchestration-reference.md`
   Added `start container <target_id>` literal, mode-off no-reroute guardrail,
   and locked reason-code vocabulary.

4. **Security/rule guidance** (AC-7):
   - `.cursor/rules/coding-standards.mdc`
   - `template/.cursor/rules/coding-standards.mdc`
   Added explicit US-0086 guardrail for no silent remote reroute when profile
   is off, plus fail-closed unknown/disabled target handling.

5. **Evidence tuple handoff guidance** (AC-5):
   - `handoffs/qa_to_verify_work.md`
   Added required names-only routing tuple fields.

6. **Execute artifact updates**:
   - `sprints/S0074/tasks.md` -> all statuses set to `done`
   - `sprints/S0074/summary.md` -> execute checkpoint and next phase pointer
   - `docs/engineering/state.md` -> execute checkpoint + strict proof + phase boundary
   - `handoffs/resume_brief.md` -> top pointer moved to `intended_resume_phase=qa`

7. **Contract tests** (AC-8, AC-10):
   - `tests/auto_command_contract_test.py`
   Added US-0086 token assertions for command/reference docs, scratchpad keys,
   and runbook/handoff tuple guidance.

### Remote-routing evidence tuple for this execute run

- `target_id=local-default`
- `environment_label=local`
- `automation_profile=off`
- `routing_source=local_default`
- `secret_surface=names_only`

### Test evidence

- `python -m pytest tests/auto_command_contract_test.py -q` -> PASS
- `python -m pytest tests/remote_config_summary_test.py -q` -> PASS

### Strict runtime proof

- `orchestrator_run_id=auto-20260405-01`
- `runtime_proof_id=rp-auto-20260405-01-execute-dev-20260413T210500Z-S0074-US0086`
- `phase_id=execute`
- `role=dev`
- `proof_issued_at=2026-04-13T21:05:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=672482884dfa858726a194e3eb07f77ca7f3eb077b3d58c24c096fe6cefafc41`

### Next

- `/qa` (fresh qa subagent) for S0074 / US-0086

## Dev -> QA Handoff — US-0085 / S0073

> **2026-04-13T14:00:00Z** — `/execute` complete (dev, `orchestrator_run_id=auto-20260405-01`). Story **US-0085** remains **OPEN** (US-0045). Sprint **S0073**. All 10 tasks (T-001..T-010) done. Ready for `/qa`.

### What changed

1. **`.gitignore` + `template/.gitignore`** (AC-1): Added `.env`, `.env.local`, `.env.*` exclusion patterns with `!.env.example` negation to keep the example tracked.

2. **`.cursorignore` + `template/.cursorignore`** (AC-2): New files blocking agent file tools from `.env*` files, with `!.env.example` negation.

3. **`.env.example` + `template/.env.example`** (AC-3): 20 `*Env` variable names grouped by source config (3 from `remote.json`, 17 from `release-targets.json`). Names only, no values.

4. **`docs/engineering/runbook.md`** + template (AC-4): New "Operator `.env` setup" section with copy/source recipe, forbidden actions (committing `.env`, agents reading `.env`), and allowed actions.

5. **`docs/engineering/runtime-connectivity.md`** + template (AC-5): Added "`*Env` variable sourcing" section referencing `.env` pattern.

6. **`docs/engineering/us-0084-remote-e2e.md`** + template (AC-6): Path B and C updated to reference `.env`/`.env.example` for operator env var setup.

7. **`.cursor/rules/coding-standards.mdc`** + template (AC-7): Added `.env` exclusion rule bullet after DEC-0016 remote config security bullet.

8. **`scripts/print_remote_env_hint.py`** (AC-8): Names-only parity helper. Reads `.env.example` and JSON configs, validates 20-name parity. Exit 0 on PASS, exit 1 on mismatch. Never reads `.env`.

9. **`tests/test_env_gitignore.py`** (AC-9): 4 regression tests — `.env` gitignored, `.env.example` NOT gitignored, `.cursorignore` exists with pattern, `.env.example` has 20 names.

10. **Existing tests** (AC-10): `remote_config_summary.py` exit 0; full suite 56/0 passed/failed.

### Test evidence

- New tests: **4 passed** (`tests/test_env_gitignore.py`)
- Parity script: **Parity PASS** (20/20 names)
- Full test suite: **56 passed**, 4 skipped, 66 subtests passed, **0 failed**
- Triad hot surface: `--check` PASS
- User-visible metadata: PASS

### Environment

- Platform: Windows 10 (local)
- Tests ran locally via `python -m pytest tests/ -q`
- `REMOTE_EXECUTION` not set (skip mode — remote_config_summary exit 0)

### Files for QA review

| Path | Change type |
|------|------------|
| `.gitignore` | Modified — `.env*` patterns + `!.env.example` negation |
| `template/.gitignore` | New — `.env*` patterns + `!.env.example` negation |
| `.cursorignore` | New — agent exclusion patterns |
| `template/.cursorignore` | New — agent exclusion patterns |
| `.env.example` | New — 20 env var names, grouped, no values |
| `template/.env.example` | New — parity copy |
| `docs/engineering/runbook.md` | Modified — `.env` setup section |
| `template/docs/engineering/runbook.md` | Modified — parity copy |
| `docs/engineering/runtime-connectivity.md` | Modified — `*Env` sourcing note |
| `template/docs/engineering/runtime-connectivity.md` | Modified — parity copy |
| `docs/engineering/us-0084-remote-e2e.md` | Modified — `.env` refs in Path B/C |
| `template/docs/engineering/us-0084-remote-e2e.md` | Modified — parity copy |
| `.cursor/rules/coding-standards.mdc` | Modified — `.env` exclusion rule |
| `template/.cursor/rules/coding-standards.mdc` | Modified — parity copy |
| `scripts/print_remote_env_hint.py` | New — parity helper |
| `tests/test_env_gitignore.py` | New — regression tests |

### Strict runtime proof

- `orchestrator_run_id=auto-20260405-01`
- `runtime_proof_id=rp-auto-20260405-01-execute-dev-20260413T140000Z-S0073-US0085`
- `phase_id=execute`
- `role=dev`
- `proof_issued_at=2026-04-13T14:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=f0590356f1ae4922a5bd235db44a0213e63f96d57288ccfee86de5e2a56835bb`

### Next

- `/qa` (fresh qa subagent) for S0073 / US-0085
