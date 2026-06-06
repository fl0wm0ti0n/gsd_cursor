# Sprint S0080 Tasks — BUG-0011

**sprint_id**: S0080  
**bug_refs**: BUG-0011  
**dec_ref**: DEC-0077 (binding; composes on DEC-0072; US-0090 orthogonal)  
**task_count**: 8  
**within_limit**: true (8 ≤ `SPRINT_MAX_TASKS=12`); `SPRINT_AUTO_SPLIT` not triggered  
**coverage**: AC-1..AC-8 surjective via T-001..T-008 (8 ACs, 8 tasks; T-001 multi-AC per architecture seeds)

> No implementation or test code is authored in this phase — dev owns that in `/execute`.

---

## T-001 — Append voice section to `caveman.mdc` per DEC-0077 §2 — AC-1, AC-2, AC-3, AC-4

- **ac_ref**: AC-1, AC-2, AC-3, AC-4
- **dec_ref**: DEC-0077 §1 (delivery surface), §2 (voice outline), §3 (level semantics)
- **description**: Append `## Voice compression (when CAVEMAN_MODE=1)` with six subsections in normative order: `### Precedence`, `### Intensity levels` (lite/full/ultra table + kit-native examples), `### Drop rules`, `### Auto-Clarity`, `### Persistence`, `### Ultra and literal regions` (pointer stub to existing 9-zone MUST — no duplicate list). **Preserve** all pre-voice scaffolding verbatim. Ship byte-identical `template/.cursor/rules/caveman.mdc`.
- **files_affected**:
  - `.cursor/rules/caveman.mdc`
  - `template/.cursor/rules/caveman.mdc` (byte-identical)
- **parity_touchpoints**: DEC-0077 §9 row 1 (positive parity).
- **acceptance_check**:
  - Exact heading `## Voice compression (when CAVEMAN_MODE=1)` present.
  - All six subsections present in locked order; `lite`, `full`, `ultra` in intensity table.
  - `### Precedence` cites user-rule override when `CAVEMAN_MODE=1` (reply voice only).
  - `### Ultra and literal regions` defers to 9-zone MUST without duplicating zone list.
  - Pre-voice blocks (gate, 9-zone invariant, toggles, TOKEN_PROFILE non-substitution) unchanged verbatim.
  - Active / template `caveman.mdc` SHA-256 equal.
- **status**: done

---

## T-002 — Runbook `#### Voice compression levels` (2-row table + rule pointer) — AC-6

- **ac_ref**: AC-6
- **dec_ref**: DEC-0077 §7 (runbook extension)
- **description**: Under existing `### Caveman mode (US-0089)` in `docs/engineering/runbook.md` (+ `template/` mirror), add `#### Voice compression levels` with compact 2-row before/after table: (1) technical explain at `full`, (2) destructive warning at auto-clarity break. Point to `.cursor/rules/caveman.mdc` for full contract. **Do not modify** `### Caveman input compression (US-0090)` subsection.
- **files_affected**:
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md` (byte-identical Caveman subsection delta)
- **parity_touchpoints**: DEC-0077 §9 row 2 (positive parity).
- **acceptance_check**:
  - `#### Voice compression levels` present under Caveman mode subsection.
  - 2-row before/after table with `full` level example and auto-clarity destructive example.
  - Pointer to `.cursor/rules/caveman.mdc` for normative contract.
  - `### Caveman input compression (US-0090)` subsection byte-unchanged.
  - Active/template runbook Caveman delta strings byte-identical.
- **status**: done

---

## T-003 — Nine `test_caveman_voice_*` subtests — AC-5

- **ac_ref**: AC-5
- **dec_ref**: DEC-0077 §5 (contract test marker list)
- **description**: Extend `tests/auto_command_contract_test.py` **in place** with nine additive `test_caveman_voice_*` subtests per DEC-0077 §5 table: section heading, level table markers, drop filler, fragment permission, auto-clarity exceptions, persistence directive, user-rule precedence, ultra/literal boundary, template parity. Additions only — do not modify unrelated subtests or `test_caveman_default_off_*` bodies.
- **files_affected**:
  - `tests/auto_command_contract_test.py`
- **parity_touchpoints**: Active-only (tests).
- **acceptance_check**:
  - All nine `test_caveman_voice_*` subtests pass post T-001.
  - Subtests fail if voice section heading or required tokens removed.
  - `test_caveman_voice_template_parity` asserts active == template `caveman.mdc` byte-identical.
  - No modification to `test_caveman_default_off_*` assertion bodies.
- **status**: done

---

## T-004 — Bump `_CAVEMAN_RULE_BASELINE_SHA256` in byte-identity subtest — AC-5

- **ac_ref**: AC-5
- **dec_ref**: DEC-0077 §4 (SHA dual-layer strategy)
- **description**: Update `_CAVEMAN_RULE_BASELINE_SHA256` constant in `test_caveman_compress_input_rule_byte_identity` to post-voice digest. Retain active==template equality assertion. Pre-voice baseline recorded: `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`. All other `test_caveman_compress_input_*` bodies byte-unchanged except baseline constant.
- **files_affected**:
  - `tests/auto_command_contract_test.py`
- **parity_touchpoints**: Active-only (tests).
- **acceptance_check**:
  - `test_caveman_compress_input_rule_byte_identity` passes with new post-voice SHA.
  - Constant differs from pre-voice `E10EFC32…E47DE` (intentional bump documented).
  - Active / template `caveman.mdc` equality assertion still present and green.
  - Other `test_caveman_compress_input_*` bodies unchanged except SHA constant.
- **status**: done

---

## T-005 — Harness section **§30A** — AC-8

- **ac_ref**: AC-8
- **dec_ref**: DEC-0077 §6 (harness §30A)
- **description**: Add harness section **§30A** to `tests/run-tests.ps1` + `tests/run-tests.sh`: title `Voice compression rule markers (BUG-0011)`; scope runs only `test_caveman_voice_*` prefix (e.g. `pytest -k caveman_voice`). Section id locked as **§30A**. Additive — existing caveman harness blocks unchanged.
- **files_affected**:
  - `tests/run-tests.ps1` (§30A)
  - `tests/run-tests.sh` (§30A)
- **parity_touchpoints**: Active-only (harness).
- **acceptance_check**:
  - §30A present in both PS1 and SH runners with matching semantics.
  - Section green when `test_caveman_voice_*` subtests pass.
  - Section fails closed when voice section markers regressed.
  - Prior caveman harness sections unchanged (additive only).
- **status**: done

---

## T-006 — Regression guard — `test_caveman_default_off_*` bodies unchanged — AC-7

- **ac_ref**: AC-7
- **dec_ref**: DEC-0077 §4 invariants (DEC-0072 §6 preservation)
- **description**: Add or extend assert-only regression guard verifying all `test_caveman_default_off_*` subtest assertion bodies remain byte-identical to DEC-0072 §6 pinned baseline. Includes pinned `test_caveman_default_off_reference_non_substitution_paragraph` sentence. Execute must not weaken default-off invariant coverage.
- **files_affected**:
  - `tests/auto_command_contract_test.py` (assert-only guard subtest)
- **parity_touchpoints**: Active-only (tests).
- **acceptance_check**:
  - Guard subtest passes on clean tree.
  - Guard fails if any `test_caveman_default_off_*` assertion body edited.
  - `test_caveman_default_off_reference_non_substitution_paragraph` pinned sentence byte-unchanged.
  - All eight DEC-0072 §6 subtests still pass green.
- **status**: done

---

## T-007 — Sprint UAT operator voice spot-check — AC-8

- **ac_ref**: AC-8
- **dec_ref**: DEC-0077 §6, §10 (operator UAT; qualitative brevity not CI)
- **description**: Populate `sprints/S0080/uat.md` + `uat.json` with operator voice spot-check scenario: set `CAVEMAN_MODE=1` + `CAVEMAN_LEVEL=full` in scratchpad; ask technical question; verify visibly shorter prose vs default-off; confirm literals (reason codes, gate tokens, paths) remain exact. Document pass/fail per AC-8 at `/verify-work`. Qualitative brevity is operator-verified — not automated CI.
- **files_affected**:
  - `sprints/S0080/uat.md`
  - `sprints/S0080/uat.json`
- **parity_touchpoints**: Active-only (UAT docs).
- **acceptance_check**:
  - UAT scenario documents `CAVEMAN_MODE=1` + `CAVEMAN_LEVEL=full` preconditions.
  - Spot-check records visibly shorter prose under mode on (operator judgment).
  - Literal regions (9-zone tokens, reason codes) verified intact in sample reply.
  - UAT notes qualitative brevity is not CI-tested (contract markers only).
- **status**: done

---

## T-008 — Architecture + DEC linkage assert (read-only) — AC-1

- **ac_ref**: AC-1
- **dec_ref**: DEC-0077 §8, §9; architecture `# BUG-0011` § Related
- **description**: Assert-only subtest verifying `docs/engineering/architecture.md` `# BUG-0011` references **DEC-0077**, **DEC-0072**, **R-0077**, documents voice-section outline and harness **§30A**; `# US-0089` §6 cross-link amended (voice rules delivered in BUG-0011). No rewrite of architecture or DEC files.
- **files_affected**:
  - `tests/auto_command_contract_test.py` (assert-only subtest under `test_caveman_voice_*` or sibling)
- **parity_touchpoints**: Active-only (read-only assert).
- **acceptance_check**:
  - Subtest passes when required cross-refs present in `# BUG-0011`.
  - Subtest fails if voice-section outline or AC traceability table removed.
  - `# US-0089` §6 contains forward-link to BUG-0011 / DEC-0077.
  - `decisions/DEC-0077.md` exists and status Accepted (read-only assert).
- **status**: done

---

## Recommended /execute ordering

1. **T-001** — voice section append (+ template mirror)
2. **T-002** — runbook level table (+ template mirror; can parallel T-001)
3. **T-004** — SHA baseline bump (depends T-001 file change)
4. **T-003** — `test_caveman_voice_*` subtests (depends T-001, T-004)
5. **T-006** — default-off regression guard (depends T-003)
6. **T-005** — harness §30A (depends T-003)
7. **T-008** — architecture linkage assert (read-only; after T-001 stable)
8. **T-007** — operator UAT docs (verify-work phase; after execute deliverables)
