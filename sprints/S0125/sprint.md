# Sprint S0125 - Sprint Plan (US-0125)

## Metadata

| Field | Value |
|---|---|
| story_id | US-0125 |
| story_title | Thin OpenCode commands and Python validator bridge — dispatch-only named commands, no Cursor command clones, Python CLIs remain fail-closed source of truth |
| sprint_id | S0125 |
| delivery_mode | ultra_lean |
| macro_phase | plan (sprint-plan — terminal canonical phase per ultra_lean; /plan-verify runs standalone per orchestrator brief, role=qa) |
| current_phase | sprint-plan |
| approach | A1 locked |
| companion_DEC | DEC-0125 (Accepted) |
| research_anchor | R-0109 (DQ1..DQ8 LOCKED for US-0125; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 + US-0124 DQ1..DQ8 locks preserved) |
| orchestrator_run_id | auto-20260824-02 |
| fresh_context_marker | tl-US0125-sprint-plan-20260824T204500Z-fresh |
| timestamp | 2026-08-24T20:45:00Z (UTC) |
| verdict | PASS |
| decision_gate | false |
| SPRINT_MAX_TASKS | 12 |
| SPRINT_AUTO_SPLIT | 1 |
| task_count | 10 (T-anch + T-001..T-009; within 12; no split) |
| CROSS_MODEL_REVIEW | 1 (model_id=glm-5.2-high required) |
| COMPONENT_SCOPE_MODE | 0 |
| USER_GUIDE_MODE | 0 |
| plan-verify | standalone /plan-verify next (role=qa per orchestrator brief); plan-verify.json NOT written in this spawn |
| backlog_status | OPEN (US-0045 — not mutated) |
| ac_checkboxes | unchecked (US-0045 — not mutated) |

## Scope summary

Ship the fifth slice of the OpenCode adapter epic (US-0121..US-0126): **Layer 3** — the named slash-command entry points (`/intake`, `/discovery`, `/research`, `/architecture`, `/sprint-plan`, `/plan-verify`, `/execute`, `/qa`, `/verify-work`, `/release`, `/closure`, `/refresh-context`, `/auto`, `/quick`, `/ask`) as **dispatch-only** markdown files at `template/.opencode/commands/<name>.md`, plus the **Python validator bridge contract** that keeps `scripts/*_validate.py` the single source of truth for persistence-blocking gates.

The commands **are** dispatch-only (do **not** clone Cursor 200-line command bodies per AC-1/AC-9). Success test (b) lives here: a model that ignores its prompt still cannot run `/release` (or any release persistence path) after a failing validator — the US-0124 plugin's `ctx.tool.hook("execute.before")` is the enforcement layer that a prompt-ignoring model cannot bypass (DQ4 defense in depth). The command prose is the *invitation* (diagnostics); the plugin is the *enforcement* (persistence).

This is an **additive commands + bridge-contract + stub-harness** change. US-0125 adds: (a) 15 new template command files (`template/.opencode/commands/<name>.md`); (b) one validator→artifact mapping table authored in the US-0125 architecture section (consumed read-only by the US-0124 plugin — T-003 is verify-or-extract-to-test-fixture, NOT a rewrite of architecture.md in execute); (c) one mock-subprocess harness extension on the US-0124 `MockCtx`; (d) one new contract test file `tests/us0125_contract_test.py` (11 markers); (e) one stub runbook h2 one-liner per code; (f) installer manifest rows for the 15 command files; (g) `--scope=opencode-adapter` parity extension; (h) README cross-link. Template agent files (`template/.opencode/agents/*.md`) and the orchestrator plugin (`template/.opencode/plugins/orchestrator.ts`) are NOT edited by US-0125 — the commands compose with the US-0122 `auto.md` agent (DQ5/DQ8 — independent surfaces, defense in depth) and the US-0124 plugin (DQ4 — command = invitation, plugin = enforcement).

Reason codes: raw Python reason codes for validator non-zero exit (`INTAKE_PERSISTENCE_BLOCKED`, `INTAKE_REQUIRED_TOPIC_MISSING`, `BUG_ISSUE_VALIDATION_FAILED`, ...); `OPENCODE_DRIVER_INVOKE_FAILED` (DEC-0124 DQ6) for subprocess invocation failure; no new `OPENCODE_*` wrapper (DQ7). US-0126 owns the full reason-code table; US-0125 ships a stub reason-code reference in `docs/engineering/runbook.md` h2 `## OpenCode thin commands + validator bridge (US-0125)` only.

Out of scope: US-0126 (full runbook + reason-code table + `--scope=opencode-adapter` parity text), enumerating every kit validator (US-0125 ships the bridge contract; US-0126 owns the full enumeration), editing `template/.opencode/agents/*.md` (US-0122 owns agent files), editing `template/.opencode/plugins/orchestrator.ts` (US-0124 owns the plugin; US-0125 authors the validator→artifact mapping that the plugin consumes — additive data, not plugin code change), repo-root `opencode.json`, new npm runtime in consumer app code (AC-10), porting `.cursor/commands/*.md` 200-line bodies (forbidden — AC-1, AC-9), new validator script (default rejected — extend contract tests; only add `scripts/opencode_command_validate.py` if US-0125 command files need static validation beyond contract tests).

## Acceptance criteria (10) - US-0125 (status OPEN, checkboxes untouched per US-0045)

- **AC-1**: Dispatch-only commands — each named OpenCode command selects role + phase id + artifact path list and stops. No embedded 200-line Cursor procedure.
- **AC-2**: Clone guard — contract test fails if `.opencode/commands/` copies `.cursor/commands/` bodies above a documented size/similarity threshold.
- **AC-3**: Validator source of truth — persistence-blocking gates remain existing Python CLIs (`intake_evidence_validate.py`, `bug_issue_validate.py`, and other fail-closed validators already in the kit). Plugin/command may subprocess them; must not reimplement rules.
- **AC-4**: Success test (b) — `/release` (or release persistence path) after a failing validator is blocked even if the command/agent prompt says to continue.
- **AC-5**: Fail-closed reason codes — validator non-zero exit surfaces existing kit reason codes (or documented `OPENCODE_*` wrapper that still names the Python code). No silent skip.
- **AC-6**: If a rule can be a plugin check or Python CLI, it must not live in a command file — grep/test for policy text that duplicates validator logic in commands.
- **AC-7**: Optional commands — missing a convenience command must not disable plugin spawn (US-0124) or Python CLIs. Commands are Layer 3.
- **AC-8**: Contract tests — `test_us0125_*` cover thin-command inventory, clone guard, validator subprocess fail-closed, and success test (b).
- **AC-9**: Compose US-0001 — Cursor command files unchanged. OpenCode commands are additive.
- **AC-10**: No new npm runtime in consumer app code — validator bridge is kit scripts + plugin subprocess, not a dependency of the operator's application.
- **AC-10**: No new npm runtime in consumer app code — validator bridge is kit scripts + plugin subprocess, not a dependency of the operator's application.

## Task summaries (10 - T-anch + T-001..T-009)

- **T-anch** (NO-OP / verification): Verify `# US-0125` H1 anchor in `docs/engineering/architecture.md` AFTER `# US-0124` (L1632) and BEFORE `# US-0089` (L2103) per DEC-0073 §11 / BUG-0010 heading policy (verified at L1836); verify DEC-0125 Accepted at `decisions/DEC-0125.md` (§1–§8); verify compose guards 7/7 UNCHANGED baseline (US-0001, US-0078/DEC-0060, US-0121/DEC-0120, US-0122/DEC-0122, US-0124/DEC-0124, US-0126, US-0102/DEC-0087); verify 11-marker contract-test list locked in architecture AC-8 table; verify command inventory (15 files) + clone-guard (line ≤ 20 + similarity ≤ 0.30 via difflib) + validator-bridge (two named CLIs + generic bridge) + defense-in-depth (command prose = diagnostics; plugin = enforcement) + `/auto` dispatch-only (`agent: auto` + `subtask: false` + no spawn logic) + frontmatter shape (`description` + `agent`; `/ask` omits `agent`; no `model:`; `subtask: false` only on `/auto`) + reason-code boundary (raw Python codes + `OPENCODE_DRIVER_INVOKE_FAILED` for subprocess failure; no `OPENCODE_*` wrapper) + stub-harness (mock-ctx + mock-subprocess reusing US-0124 `MockCtx`) locked in DEC-0125 §1–§8; verify `template/.opencode/commands/` exists with only `.gitkeep` (US-0121 reserved slot — US-0125 owns directory body); verify `tests/us0125/` directory does NOT yet exist; verify `tests/us0125_contract_test.py` does NOT yet exist; verify `docs/engineering/runbook.md` does NOT yet have `## OpenCode thin commands + validator bridge (US-0125)` h2; verify `[opencode_install_include_paths]` exists but does NOT yet list `template/.opencode/commands/**`. Record to `sprints/S0125/t-anch-verification.md`. T-anch is NO-OP / verification only — NO mutation to `architecture.md` or `DEC-0125.md` in /execute (mirrors US-0122 / US-0123 / US-0124 T-anch ceremony). (AC-9, AC-10 baseline; NO-OP / verification only)
- **T-001** (NEW 15 command files): Create 15 dispatch-only markdown command files at `template/.opencode/commands/<name>.md` per architecture DQ1 + DQ6 LOCKED + DEC-0125 §1, §6. Inventory: 12 lifecycle phases (`intake.md`→`po`, `discovery.md`→`po`, `research.md`→`tech-lead`, `architecture.md`→`tech-lead`, `sprint-plan.md`→`tech-lead`, `plan-verify.md`→`qa`, `execute.md`→`dev`, `qa.md`→`qa`, `verify-work.md`→`qa`, `release.md`→`release`, `closure.md`→`qa` with prompt `role=qe` per DEC-0051 / US-0120, `refresh-context.md`→`curator`) + `auto.md` (`agent: auto` + `subtask: false` — dispatch-only, no spawn logic per DQ5) + `quick.md` (`agent: tech-lead` — mega_quick delivery-mode entry per US-0096 / DEC-0082) + `ask.md` (omits `agent:` — agent-agnostic, read-only). Each file: frontmatter (`description` + `agent: <role>`; `/auto` adds `subtask: false`; `/ask` omits `agent`) + dispatch-only body (≤ ~12 lines) naming the phase_id + artifact path list + STOP. No `model:` in any template command (US-0102 + US-0123). No `$ARGUMENTS`, no shell injection, no `@file` inclusion. Each file ≤ 20 lines (DQ2 line cap). No 200-line Cursor command clones (AC-1, AC-9). Tests: marker 1 (`test_us0125_command_inventory`) asserts 15 files present + no extra + no `.gitkeep` after populate; marker 11 (`test_us0125_command_frontmatter_shape`) asserts frontmatter shape; marker 8 (`test_us0125_auto_command_dispatch_only`) asserts `/auto` dispatch-only. (AC-1)
- **T-002** (Clone-guard contract test): Create `test_us0125_clone_guard` marker inside `tests/us0125_contract_test.py` per architecture DQ2 LOCKED + DEC-0125 §2. Two metrics, defense in depth: (i) per-file line cap ≤ 20 (including frontmatter + body); (ii) normalized-text similarity ≤ 0.30 vs `.cursor/commands/<name>.md` via stdlib `difflib.SequenceMatcher` (no new test dependency). **Normalization strip list LOCKED** (critic NB `ik_us0125_dq2_normalization_strip_list_open` closed here): strip frontmatter (between `---` fences) + lowercase + strip punctuation + strip the shared phase-name vocabulary (the canonical phase id token + the words "its-magic", "command", "phase", "artifact", "STOP", "run", "validator", "plugin", "script", "python", "scripts", "repo", "the", "a", "an", "to", "of", "and", "or", "before", "after", "above", "below", "path", "list", "id"). The strip list is documented as a constant in the test file so US-0126 inherits it without re-deriving. `test_us0125_clone_guard` iterates over the 15 shipped `.opencode/commands/*.md` files; for each, asserts (i) line count ≤ 20, (ii) normalized similarity vs `.cursor/commands/<name>.md` ≤ 0.30. Fails on either violation. (AC-2)
- **T-003** (Validator→artifact mapping table — verify-or-extract-to-test-fixture): The mapping table already lives in the US-0125 architecture section (architecture.md L1939-L1945 — authored in /architecture phase; consumed read-only by the US-0124 plugin `ctx.tool.hook("execute.before")`). T-003 in /execute is **verify-or-extract-to-test-fixture**, NOT a rewrite of architecture.md. /execute work: (a) verify the mapping table is present in `docs/engineering/architecture.md # US-0125` (3 rows: `handoffs/intake_evidence/*.json` → `intake_evidence_validate.py --enforce`; `docs/product/backlog.md` + `docs/product/acceptance.md` bug rows → `bug_issue_validate.py --check-acceptance`; other persistence-blocking artifacts → generic bridge contract); (b) extract the mapping into a test fixture consumed by `test_us0125_validator_subprocess_fail_closed` (marker 3) and `test_us0125_release_blocked_after_failing_validator` (marker 4) so the contract tests do not re-parse architecture.md prose at runtime; (c) assert the mapping is additive data (US-0125-owned, US-0124-consumed) — no plugin code change. T-003 does NOT mutate `architecture.md` (T-anch NO-OP ceremony preserves the architecture mapping table as the locked source of truth). (AC-3, AC-4)
- **T-004** (Validator subprocess bridge — command prose line shape): Author the validator-subprocess bridge line shape in the 12 lifecycle phase command bodies + `/auto` + `/quick` + `/ask` per architecture DQ3 + DQ4 + DQ7 LOCKED + DEC-0125 §3, §4, §7. Each lifecycle command body that owns a persistence-blocking artifact includes a short line: "Before writing to `<artifact>`, run `python scripts/<validator>.py --repo .` and surface any non-zero exit reason code to the operator. The orchestrator plugin enforces persistence." This is *informational* (DQ4 — diagnostics, not enforcement). The plugin `ctx.tool.hook("execute.before")` enforcement is US-0124 territory — US-0125 authors the contract prose, US-0124 authors the hook. Reason codes: raw Python reason codes for validator non-zero exit (e.g. `INTAKE_PERSISTENCE_BLOCKED`, `BUG_ISSUE_VALIDATION_FAILED`); `OPENCODE_DRIVER_INVOKE_FAILED` (DEC-0124 DQ6) for subprocess invocation failure (missing Python, missing script, timeout); no new `OPENCODE_*` wrapper (DQ7). No silent skip (AC-5). Tests: marker 3 (`test_us0125_validator_subprocess_fail_closed`) asserts bridge contract for the two named CLIs — stubbed non-zero → command/plugin does not proceed to persistence; marker 5 (`test_us0125_reason_code_raw_python`) asserts no `OPENCODE_VALIDATOR_FAILED` wrapper; marker 6 (`test_us0125_no_policy_in_commands`) asserts no policy text duplicating validator logic. (AC-3, AC-5)
- **T-005** (Mock-subprocess harness extension): Extend the US-0124 `MockCtx` harness (`tests/us0124/mock_ctx.ts`) with a `mockSubprocess` field OR add a sibling `tests/us0125/mock_subprocess.ts` imported by the US-0125 test, per architecture DQ8 LOCKED + DEC-0125 §8. The mock subprocess accepts a scripted `nextExitCode` (0 or non-zero) + `nextStderr` (the raw Python reason code) + `nextThrow` (for `OPENCODE_DRIVER_INVOKE_FAILED` simulation). The plugin's `ctx.tool.hook("execute.before")` calls the mock subprocess; tests assert the hook refuses the write on non-zero. No OpenCode runtime dependency — CI runs pure Node/Bun (same as US-0124). **Runner: Node** (consistent with US-0124 DQ3). Tests: marker 4 (`test_us0125_release_blocked_after_failing_validator`) — success test (b); marker 10 (`test_us0125_no_new_npm_runtime`) asserts no new runtime deps. (AC-4, AC-8, AC-10)
- **T-006** (Contract tests `tests/us0125_contract_test.py` — 11 markers): Create `tests/us0125_contract_test.py` with 11 markers per architecture AC-8 table + DEC-0125 §9. Markers: (1) `test_us0125_command_inventory` [AC-1]; (2) `test_us0125_clone_guard` [AC-2]; (3) `test_us0125_validator_subprocess_fail_closed` [AC-3]; (4) `test_us0125_release_blocked_after_failing_validator` [AC-4] — success test (b); (5) `test_us0125_reason_code_raw_python` [AC-5]; (6) `test_us0125_no_policy_in_commands` [AC-6]; (7) `test_us0125_missing_command_does_not_disable_plugin` [AC-7]; (8) `test_us0125_auto_command_dispatch_only` [AC-1, AC-7]; (9) `test_us0125_cursor_commands_unchanged` [AC-9]; (10) `test_us0125_no_new_npm_runtime` [AC-10]; (11) `test_us0125_command_frontmatter_shape` [AC-1, AC-8]. Surjective AC coverage: AC-1 (markers 1, 8, 11), AC-2 (marker 2), AC-3 (markers 3, 4), AC-4 (marker 4), AC-5 (marker 5), AC-6 (marker 6), AC-7 (markers 7, 8), AC-8 (marker 11), AC-9 (marker 9), AC-10 (marker 10). Mirror to `template/tests/us0125_contract_test.py` byte-identical for parity pairing. (AC-8)
- **T-007** (Installer manifest rows): Add `template/.opencode/commands/**` source row under `[opencode_install_include_paths]` in `docs/engineering/context/installer-owned-paths.manifest` AND `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical). Existing rows UNCHANGED — additive row only. Triple-installer (PS/Bash/Python) reads opencode sections only when `--host` includes opencode (US-0121 compose; `host_gates_cursor_row` predicate). (AC-1)
- **T-008** (README + parity + runbook stub): Extend `scripts/check_intake_template_parity.py` `--scope=opencode-adapter` `OPENCODE_ADAPTER_PAIRS` to cover the 15 command files + mock-subprocess harness + contract-test surface (byte-identical active ↔ template pairs where applicable). Update `its_magic/README.md` to cross-link the OpenCode thin commands + validator bridge capability + pointer to DEC-0125. Add `## OpenCode thin commands + validator bridge (US-0125)` h2 stub to `docs/engineering/runbook.md` as a **stub one-liner per code** per DEC-0125 §7 — list the two named validator CLIs (`intake_evidence_validate.py`, `bug_issue_validate.py`) + their canonical Python reason codes + cross-link to US-0126 for the full reason-code table. US-0126 owns the full runbook section text; US-0125 ships the stub only — no duplication of remediation text. **MUST keep `docs/engineering/runbook.md` byte-identical with `template/docs/engineering/runbook.md` after edit** — edit both files identically. Mirror parity script to `template/scripts/check_intake_template_parity.py` byte-identical. (AC-8)
- **T-009** (Validator extension — default no new script): Default = extend contract tests (T-006) + reuse `scripts/model_tier_validate.py --scope opencode-catalog` from US-0123; do NOT create a new `scripts/opencode_command_validate.py`. Fall back to a new validator script ONLY if US-0125 command files need static validation beyond contract tests AND coupling forces a separate validator class (trigger: command-specific checks cannot reuse >50% of existing `--scope opencode-catalog` helpers, OR scope-tag plumbing requires touching >3 unrelated `--scope` modes). If fallback triggers, raise a DEC follow-up; do NOT silently split. (AC-8)

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (dispatch-only commands) | T-001, T-006 (markers 1, 8, 11), T-007 |
| AC-2 (clone guard) | T-002, T-006 (marker 2) |
| AC-3 (validator source of truth) | T-003, T-004, T-006 (markers 3, 4) |
| AC-4 (success test b) | T-003, T-005, T-006 (marker 4) |
| AC-5 (fail-closed reason codes) | T-004, T-006 (marker 5) |
| AC-6 (no policy in commands) | T-006 (marker 6) |
| AC-7 (optional commands) | T-006 (markers 7, 8) |
| AC-8 (contract tests) | T-006 (all 11 markers), T-008 (parity + runbook stub) |
| AC-9 (compose US-0001) | T-anch (baseline), T-006 (marker 9) |
| AC-10 (no new npm runtime) | T-005, T-006 (marker 10) |

**Surjectivity check**: 10/10 ACs covered (each AC has at least 1 task). No `PLAN_AC_COVERAGE_GAP`.

## Critic carry-ins (1 non-blocking finding — closed in /execute T-002)

- `ik_us0125_dq2_normalization_strip_list_open` → T-002 task note: lock the token-strip manifest as a documented constant in `test_us0125_clone_guard` so the normalization strip list is explicit, version-controlled, and inherited by US-0126 without re-derivation. The strip list is: frontmatter fence block + lowercase + punctuation + the canonical phase id token + the shared vocabulary words listed in T-002.

## Compose guards (7/7 UNCHANGED — additive commands + bridge contract + stub harness only)

| Compose target | Verification | Result |
|---|---|---|
| US-0001 (phase names + artifact outputs) | 15 command files use phase names + artifact paths; no 200-line clones (AC-9) | ✅ compose |
| US-0078 / DEC-0060 (`intake_evidence_validate.py` persistence gate) | validator remains Python SOT; thin commands subprocess, do not reimplement | ✅ compose |
| US-0121 / DEC-0120 (host default cursor-only + reserved `template/.opencode/commands/` slot) | commands live in reserved slot; `.gitkeep` replaced by 15 files | ✅ consumed |
| US-0122 / DEC-0122 (seven role agents) | commands bind via `agent: <role>`; agents unchanged | ✅ compose |
| US-0124 / DEC-0124 (plugin owns spawn + `ctx.tool.hook` enforcement) | `/auto` is dispatch-only; plugin owns spawn + `ctx.tool.hook` enforcement; no spawn logic in commands; missing command must not disable plugin (US-0124 AC-7 ↔ US-0125 AC-7) | ✅ compose |
| US-0126 (full runbook + reason-code table + `--scope=opencode-adapter` parity) | US-0125 ships stub reason-code reference only; US-0126 owns full text | ✅ boundary |
| US-0102 / DEC-0087 (no vendor slugs in `template/`) | no `model:` literals in any command frontmatter | ✅ untouched |

Contract test `test_us0125_cursor_commands_unchanged` (marker 9) + `test_us0125_no_new_npm_runtime` (marker 10) + `test_us0125_command_frontmatter_shape` (marker 11) enforce at execute boundary.

## Task dependency graph

```
[T-anch] --> [T-001] (15 command files) --> [T-002] (clone-guard marker, after T-001)
                                          |
                                          v
                                      [T-004] (validator subprocess bridge prose, after T-001) - parallel with T-002/T-003/T-007
                                          |
                                          v
                                      [T-007] (manifest rows, after T-001) - parallel with T-008
                                          |
                                          v
                                      [T-008] (README + parity + runbook stub, after T-001 + T-007)
                                          |
                                          v
                                      [T-003] (verify-or-extract mapping fixture, after T-001)
                                          |
                                          v
                                      [T-005] (mock-subprocess harness, after T-003)
                                          |
                                          v
                                  [T-006] (contract tests last, assert all outputs)
                                          |
                                          v
                                  [T-009] (validator extension decision, after T-006)
                                          |
                                          v
                                  Integration verification
```

**Execution order (deterministic)**: T-anch → T-001 (15 command files) → {T-002, T-003, T-004, T-007 parallel (clone-guard marker, mapping fixture, bridge prose, manifest rows)} → T-008 (README + parity + runbook stub) → T-005 (mock-subprocess harness) → T-006 (contract tests last) → T-009 (validator decision) → integration verification.

## Execute phase role (per DEC-0051 / US-0069)

| Phase | Role | Isolation |
|---|---|---|
| /plan-verify | qa (fresh per BUG-0006) | {phase_id:plan-verify, role:qa} — standalone per orchestrator brief |
| /execute | dev (fresh per BUG-0006) | {phase_id:execute, role:dev} |
| /qa | qa (fresh) | {phase_id:qa, role:qa} |
| /verify-work | qa (fresh) | {phase_id:verify-work, role:qa} |
| /release | release (fresh) | {phase_id:release,role:release} |
| /closure | qe (fresh) | {phase_id:closure, role:qe} |
| /refresh-context | curator (fresh) | {phase_id:refresh-context, role:curator} |

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

| Field | Value |
|---|---|
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0125 |
| sprint_id | S0125 |
| orchestrator_run_id | auto-20260824-02 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| fresh_context_marker | tl-US0125-sprint-plan-20260824T204500Z-fresh |
| timestamp | 2026-08-24T20:45:00Z (UTC) |
| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 — required) |
| evidence_ref | sprints/S0125/sprint.md, sprints/S0125/tasks.md, sprints/S0125/progress.md, sprints/S0125/uat.json, sprints/S0125/uat.md, sprints/S0125/t-anch-verification.md, handoffs/tl_to_dev.md (US-0125 prepend), docs/engineering/state.md (sprint-plan checkpoint append-bottom), docs/engineering/architecture.md # US-0125, decisions/DEC-0125.md |

Prior phase proof consumed: `rp-auto-20260824-02-architecture-tech-lead-20260824T203000Z-US-0125` (proof_hash=9405B4A1DD1A66B7112C8C594CDF319DA93ACC6E095F640068FEEB10AB02C525, ttl 2026-08-24T21:30:00Z — consumed before RUNTIME_PROOF_STALE). Sovereign-critic architecture PASS at 2026-08-24T20:35:00Z (anti_slop_aggregate=8; 0 blocking findings; 3 research critic NBs + 1 architecture-prompt carry-forward closed in architecture phase; 1 non-blocking carry-forward `ik_us0125_dq2_normalization_strip_list_open` routed to /execute T-002).

## Runtime proof (DEC-0038)

| Field | Value |
|---|---|
| runtime_proof_id | rp-auto-20260824-02-sprint-plan-tech-lead-20260824T204500Z-US-0125 |
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0125 |
| sprint_id | S0125 |
| orchestrator_run_id | auto-20260824-02 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 — required) |
| proof_issued_at | 2026-08-24T20:45:00Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-08-24T21:45:00Z (UTC) |
| proof_hash | 2FF3A63387C7337D5EC02802253D251CC2636831A6369B7A121F6135AC51E234 |
| canonical_payload | `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-02","phase_id":"sprint-plan","proof_issued_at":"2026-08-24T20:45:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260824-02-sprint-plan-tech-lead-20260824T204500Z-US-0125","sprint_id":"S0125","story_id":"US-0125"}` |

## Decision gate

| Field | Value |
|---|---|
| decision_gate | false |
| stop_conditions_met | yes |
| missing_acceptance_criteria | none (10/10 ACs covered by 11 contract-test markers + compose guards + T-008 runbook stub) |
| compose_guards | 7/7 UNCHANGED (additive commands + bridge contract + stub harness only) |
| dc_check | clean |
| task_count | 10 (within SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1 but no split needed) |
| risks_finalized | 6/6 ACCEPTED (R1..R6 from R-0109 US-0125) + 3 research critic NBs closed (ik_us0125_dq5_auto_plugin_overlap; ik_us0125_dq3_validator_scope_boundary; ik_us0125_spec_scope_minimal_pass) + 1 architecture-prompt carry-forward closed (ik_us0125_dq4_plugin_mapping_coupling) + 1 non-blocking carry-forward routed to /execute T-002 (ik_us0125_dq2_normalization_strip_list_open) |
| approach | A1 locked |
| Q | DQ1..DQ8 LOCKED for US-0125; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 + US-0124 DQ1..DQ8 locks preserved |
| plan-verify readiness | standalone /plan-verify next (role=qa per orchestrator brief); plan-verify.json NOT written in this spawn |
| sovereign_memory_note | `assemble_sovereign_memory_digest(...)` NOT called; no mistakes.jsonl write |

## Definition of done (sprint-plan)

- [x] 10 tasks enumerated (T-anch + T-001..T-009) — within SPRINT_MAX_TASKS=12
- [x] 10/10 ACs covered by 11 contract-test markers + compose guards + T-008 runbook stub (surjective)
- [x] Task dependency graph documented
- [x] Execute phase role matrix documented (including standalone /plan-verify per orchestrator brief)
- [x] Compose guards 7/7 UNCHANGED (additive commands + bridge contract + stub harness only)
- [x] Critic carry-ins (1 non-blocking) explicitly closed in T-002 (not silently dropped)
- [x] Isolation evidence + runtime proof emitted (model_id=glm-5.2-high present)
- [x] Sprint-plan checkpoint appended to `docs/engineering/state.md` (append-bottom; never truncate)
- [x] Sprint-plan handoff prepended to `handoffs/tl_to_dev.md`
- [x] Sprint-plan PASS prepended to `handoffs/resume_brief.md` (→ /plan-verify, role=qa)
- [x] UAT placeholders written (`uat.json` empty steps, `uat.md` ACs no results)
- [x] Backlog status OPEN (US-0045 — not mutated); AC checkboxes untouched

## Next scheduled phase

| Field | Value |
|---|---|
| next_scheduled_phase | `/plan-verify` (role=qa per orchestrator brief; fresh qa subagent per BUG-0006) |
| next_scheduled_role | qa |
| next_sprint_macro | plan (terminal — /plan-verify is the verification gate before build+verify macro) |
| stop_condition | STOP after sprint-plan completes; hand off via artifacts only to /plan-verify in fresh qa subagent per BUG-0006. Do not spawn /plan-verify from this subagent. |
| artifacts_written | sprints/S0125/sprint.md, sprints/S0125/tasks.md, sprints/S0125/progress.md, sprints/S0125/uat.json, sprints/S0125/uat.md, sprints/S0125/t-anch-verification.md, docs/engineering/state.md (sprint-plan checkpoint append-bottom), handoffs/tl_to_dev.md (US-0125 prepend), handoffs/resume_brief.md (sprint-plan PASS prepend → /plan-verify) |
