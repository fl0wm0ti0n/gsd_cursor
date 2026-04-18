# Tasks — S0075 / US-0089

All tasks are atomic, testable, and scoped to **DEC-0072** / `docs/engineering/architecture.md` `# US-0089`. Status starts **planned** and advances at **`/execute`**.

## T-001 — Add Caveman scratchpad keys (active + template example) — AC-1

- **AC**: AC-1
- **Description**: Insert the four architecture-locked Caveman scratchpad keys (`CAVEMAN_MODE=0`, `CAVEMAN_LEVEL=`, `CAVEMAN_COMPRESS_INPUT=0`, `CAVEMAN_FILE_SCOPE=`) plus a `## Caveman mode (US-0089)` comment block into the active operator scratchpad and both example surfaces. Active/template example lines must be byte-identical (contract subtest #2 asserts parity).
- **Files**:
  - `.cursor/scratchpad.md` (active — keys + `## Caveman mode (US-0089)` comment block, **DEC-0055** example-only install path means no `template/.cursor/scratchpad.md` mirror)
  - `.cursor/scratchpad.local.example.md` (active)
  - `template/.cursor/scratchpad.local.example.md` (template mirror — byte-identical to active)
- **Governance**: **DEC-0072 §3**, architecture.md `# US-0089` §3, **US-0017**, **US-0045**.
- **Status**: done
- **Acceptance**: All four keys present with locked default values; comment block identifies US-0089 and `default-off` semantics; example files byte-parity verified; no behavior change implied by key presence alone (consumed only by `caveman.mdc` rule in T-003).

## T-002 — Lock default-off invariant assertions (spawn-only / gate / tokens) — AC-2

- **AC**: AC-2
- **Description**: Author the three default-off invariant subtests that guarantee byte-equivalence with pre-US-0089 behavior under `CAVEMAN_MODE=0`: (a) existing `required` token list in contract tests intact (only additive); (b) `AUTO_QUIET` non-suppressible gate vocabulary preserved in `auto.md` + reference; (c) no `npx skills add` token leak anywhere under `.cursor/` or `docs/engineering/`. These three subtests are the canonical #6 / #7 / #8 of the DEC-0072 §6 set.
- **Files**:
  - `tests/auto_command_contract_test.py` (add `test_caveman_default_off_existing_contract_tokens_intact`, `test_caveman_default_off_non_suppressible_gate_vocab_preserved`, `test_caveman_default_off_no_vendor_install_leak`)
- **Governance**: **DEC-0072 §6** (items 6–8), **US-0088** (`AUTO_QUIET` vocabulary), **US-0048 / DEC-0029**, **US-0056 / DEC-0038**, **BUG-0006** (spawn-only).
- **Status**: done
- **Acceptance**: Three subtests present, runnable, and fail-closed on any regression of existing tokens / gate vocabulary / vendor-install leakage; `CAVEMAN_MODE=0` byte-equivalence invariant is enforced by assertion.

## T-003 — Create `.cursor/rules/caveman.mdc` (active + template) — AC-3

- **AC**: AC-3
- **Description**: Create the new Caveman composition rule in both active and template paths (byte-identical bodies). Rule MUST contain: (a) `CAVEMAN_MODE` / `CAVEMAN_LEVEL` gate logic (default-off narrative); (b) the 9-zone literal-region invariant list phrased as hard `MUST` (fenced code, file paths, AC checklists, `ALL_CAPS_WITH_UNDERSCORES` reason codes, IDs — `US-xxxx`/`DEC-xxxx`/`R-xxxx`/`BUG-####`/`S0xxx`/`T-xxx` — contract markers like `[BUG_VALIDATION_OK]`/`[INTAKE_EVIDENCE_VALIDATION_OK]`, strict-proof tuple fields, isolation-evidence fields, git/commit refs); (c) the five canonical operator phrases verbatim; (d) non-suppressible gate list (decision gate, errors, evidence, `AUTO_QUIET` non-suppressibles); (e) single-line external attribution only — no `npx skills add` token. Contract subtest #3 asserts presence of `CAVEMAN_MODE`, the literal token `literal`, and all five phrases in each body.
- **Files**:
  - `.cursor/rules/caveman.mdc` (new)
  - `template/.cursor/rules/caveman.mdc` (new — byte-identical to active)
- **Governance**: **DEC-0072 §2 / §4 / §5**, architecture.md `# US-0089` §2 / §4 / §5, **US-0017**, **US-0021**, **US-0071**.
- **Status**: done
- **Acceptance**: Rule file exists on both paths with byte-identical bodies; 9-zone list, five phrases, non-suppressible list all present; no vendor-install token; contract subtest #3 passes.

## T-004 — Publish TOKEN_PROFILE non-substitution paragraph in reference — AC-4

- **AC**: AC-4
- **Description**: Insert the verbatim non-substitution paragraph (locked by DEC-0072 §1) into `docs/engineering/auto-orchestration-reference.md` near the existing `TOKEN_PROFILE` / `AUTO_QUIET` discussion, and mirror byte-identically into `template/` counterpart. The paragraph establishes Option A (orthogonal axes) — `TOKEN_PROFILE` controls context breadth, `CAVEMAN_*` controls reply voice; neither substitutes for the other. Contract subtest #4 asserts the exact sentence present in both files.
- **Files**:
  - `docs/engineering/auto-orchestration-reference.md` (active)
  - `template/docs/engineering/auto-orchestration-reference.md` (template mirror — byte-identical paragraph)
- **Governance**: **DEC-0072 §1**, architecture.md `# US-0089` §1, **US-0080 / DEC-0062** (`TOKEN_PROFILE`), **US-0088** (`AUTO_QUIET`), **US-0017**, **US-0058 / DEC-0040**.
- **Status**: done
- **Acceptance**: Exact paragraph present in both active and template paths (byte-identical); placement adjacent to existing `TOKEN_PROFILE` / `AUTO_QUIET` context; contract subtest #4 passes.

## T-005 — Add `### Caveman mode (US-0089)` runbook subsection — AC-5

- **AC**: AC-5
- **Description**: Append the operator-facing Caveman subsection to `docs/engineering/runbook.md` (active + template). Subsection MUST include: (a) scratchpad key table showing the four locked keys with defaults; (b) the five canonical operator phrases verbatim (`caveman on`, `caveman off`, `stop caveman`, `normal mode`, `caveman: lite|full|ultra`); (c) the non-substitution paragraph (identical text to T-004); (d) scratchpad-authoritative-across-spawn semantics; (e) session phrases-as-next-turn-overlay semantics. Contract subtest #5 asserts all five phrases + the non-substitution sentence present in both active + template.
- **Files**:
  - `docs/engineering/runbook.md` (active)
  - `template/docs/engineering/runbook.md` (template mirror — byte-identical for the locked strings)
- **Governance**: **DEC-0072 §5**, architecture.md `# US-0089` §5, **US-0017**, **US-0058 / DEC-0040**.
- **Status**: done
- **Acceptance**: Subsection present in both paths; five phrases + non-substitution sentence are byte-identical across active/template and identical to the reference-doc paragraph from T-004; contract subtest #5 passes.

## T-006 — Extend `tests/auto_command_contract_test.py` in place (subtests 1–5) — AC-6

- **AC**: AC-6
- **Description**: Add the remaining five `test_caveman_default_off_*` subtests (the active-surface presence / template-parity / non-substitution / runbook-phrases half of the DEC-0072 §6 eight-test set, i.e. items 1–5): (1) `test_caveman_default_off_scratchpad_keys_active` — four exact lines present in `.cursor/scratchpad.md`; (2) `test_caveman_default_off_scratchpad_keys_example_parity` — identical four lines present in both active + template example; (3) `test_caveman_default_off_rule_file_present_active_template` — `caveman.mdc` present in both paths, containing tokens `CAVEMAN_MODE`, `literal`, and all five phrases; (4) `test_caveman_default_off_reference_non_substitution_paragraph` — exact paragraph present in reference doc (active + template); (5) `test_caveman_default_off_runbook_operator_phrases` — five phrases + non-substitution paragraph present in runbook (active + template). File extension is in place (no new test module).
- **Files**:
  - `tests/auto_command_contract_test.py` (active-only — no `template/` mirror, consistent with row 7 of DEC-0072 §7)
- **Governance**: **DEC-0072 §6** (items 1–5), **US-0017** (negative-parity for tests), **US-0088** (test-surface policy).
- **Status**: done
- **Acceptance**: Five subtests added (combined with the three from T-002 totals 8 `test_caveman_default_off_*` subtests — matching DEC-0072 §6 cardinality exactly); all subtests PASS; no new test module created.

## T-007 — Verify `architecture.md # US-0089` linkage and append-bottom integrity — AC-7

- **AC**: AC-7
- **Description**: Assertion-only task. Architecture section `# US-0089` was written at `/architecture` (2026-04-18); this task confirms the section persists on the `docs/engineering/architecture.md` hot surface (post-rollover), follows **DEC-0040** append-bottom ordering, is cross-referenced from `docs/engineering/decisions.md` (index + context pack + full record of DEC-0072), and remains linked from `docs/product/backlog.md` `## US-0089` `architecture_notes`. No rewrite of the section body; no edit of `decisions.md` body. Task output is a plan-verify evidence bullet in `sprints/S0075/summary.md` at `/execute` time.
- **Files** (read-only verification — no writes in T-007):
  - `docs/engineering/architecture.md` (section `# US-0089`)
  - `docs/engineering/decisions.md` (DEC-0072 entry + context pack)
  - `docs/product/backlog.md` (`## US-0089` `architecture_notes`)
- **Governance**: **DEC-0072**, **DEC-0040** (append-bottom artifact-ordering), **US-0045** (canonical status), **US-0058 / DEC-0040**.
- **Status**: done
- **Acceptance**: Section present, append-bottom position honored, cross-references intact; evidence recorded in `sprints/S0075/summary.md` and verified at QA.

## T-008 — Template parity sweep + negative-parity assertion — AC-8

- **AC**: AC-8
- **Description**: Final parity pass across the DEC-0072 §7 inventory. Confirm: rows 2 / 3 / 4 / 5 have byte-identical active + template counterparts for the locked strings (scratchpad example, new rule, reference paragraph, runbook subsection); row 1 follows **DEC-0055** example-only install (active only); row 6 is active-only architecture (no mirror); row 7 is active-only tests (no mirror); row 8 negative-parity — both `.cursor/skills/its-magic/SKILL.md` (active) and `template/.cursor/skills/its-magic/SKILL.md` (template) remain **unchanged** from their pre-US-0089 bodies. Any parity slip triggers a fail-closed reason code and blocks QA.
- **Files** (verification + explicit no-edit discipline):
  - Rows 2–5 active + template pairs (byte-equality check for locked strings)
  - Row 8: `.cursor/skills/its-magic/SKILL.md` + `template/.cursor/skills/its-magic/SKILL.md` (explicit no-edit assertion)
- **Governance**: **DEC-0072 §7**, architecture.md `# US-0089` §7, **US-0017**, **DEC-0055** (scratchpad install surface).
- **Status**: done
- **Acceptance**: All eight rows of DEC-0072 §7 accounted for; parity rows match byte-for-byte where required; negative-parity row untouched; sweep evidence captured in `sprints/S0075/summary.md`.
