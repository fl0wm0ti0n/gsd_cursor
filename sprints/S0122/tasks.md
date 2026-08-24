# Sprint S0122 - Task checklist (US-0122)

Total tasks: 10 (T-anch + T-001..T-009). SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1; no split needed.

## Task execution order

1. T-anch (NO-OP / verification)
2. T-001 (NEW 8 markdown agent files `template/.opencode/agents/*.md`)
3. T-002 (PO `edit` object form + deny-last ordering) - parallel with T-003, T-004, T-005
4. T-003 (`auto` orchestrator `task` object + 7-role allow + `*` deny last) - parallel with T-002, T-004, T-005
5. T-004 (Security agent `edit: "deny"` findings-oriented) - parallel with T-002, T-003, T-005
6. T-005 (Remaining role agents `tech-lead`, `dev`, `qa`, `release`, `curator` permission matrices) - parallel with T-002, T-003, T-004
7. T-007 (Manifest rows `template/.opencode/agents/**` under `[opencode_install_include_paths]`)
8. T-009 (README + `--scope=opencode-adapter` parity extension for agent inventory)
9. T-008 (Runbook `## OpenCode role agents and permissions (US-0122)` h2 one-liner)
10. T-006 (NEW `tests/us0122_contract_test.py` — 8 markers; tests last, assert all outputs)
11. Integration verification

## Task checklist

- [x] **T-anch**: Verify `# US-0122` H1 anchor present in `docs/engineering/architecture.md` (added in /architecture phase per DEC-0076 / BUG-0010); verify DEC-0122 authored Accepted at `decisions/DEC-0122.md` (§1 markdown agents, §2 locked eight-agent matrix, §3 static success-test-(c) harness, §4 Layer-2 short prompts + clone guard, §5 manual invoke one-liner, §6 no vendor slugs, §7 contract tests + parity, §8 non-goals); verify compose guards 5/5 UNCHANGED baseline (US-0003, US-0023/BUG-0006, US-0121, US-0102/DEC-0087, US-0002/US-0004); verify 8-marker contract-test list locked in architecture AC-8 table; verify locked Layer-1 permission matrix in DEC-0122 §2 (8 agents: `auto`, `po`, `tech-lead`, `dev`, `qa`, `release`, `curator`, `security`); verify `template/.opencode/agents/` ships `.gitkeep` only (no role files yet); verify `tests/us0122_contract_test.py` does NOT yet exist; verify `[opencode_install_include_paths]` section exists in active + template manifest (US-0121) but does NOT yet list `template/.opencode/agents/**` source rows. Record results to `sprints/S0122/t-anch-verification.md`. **Critic NB `ik_us0122_stale_compose_count_6_vs_5`**: architecture overview line says "compose guards 6/6 verified" (stale — carried over from research checkpoint); architecture compose-guards table lists 5/5. T-anch verifies 5/5 (US-0003, US-0023/BUG-0006, US-0121, US-0102/DEC-0087, US-0002/US-0004). No architecture.md mutation in /execute (T-anch NO-OP); the 6/6 vs 5/5 wording discrepancy is a non-blocking documentation drift to be reconciled at /plan-verify or in a future doc-parity slice. (AC-9, AC-10 baseline; NO-OP / verification only)

- [x] **T-001**: Create 8 markdown agent files `template/.opencode/agents/{po,tech-lead,dev,qa,release,curator,security,auto}.md` per architecture DQ1 LOCKED + DEC-0122 §1. Each file: YAML frontmatter (`description`, `mode`, `permission`, short `prompt` body). Filename (minus `.md`) is the OpenCode agent name. No repo-root `opencode.json` (R-0109 Q6 US-0121 lock preserved). No active kit `.opencode/agents/` mirror (DQ8 YAGNI inherits R-0109 Q9 US-0121). No vendor slugs, no `model:` literals (AC-7, US-0102). Each file ≤ 2 KiB total (AC-4 size cap). No forbidden clone markers (`/auto`, `/intake`, `/discovery`, `/research`, `/architecture`, `/sprint-plan`, `/execute`, `/qa`, `/release`, `/closure`, `/refresh-context` command-body prose; `.cursor/commands/` path literals; `---` MDC frontmatter delimiters). (AC-1, AC-4)

- [x] **T-002**: `template/.opencode/agents/po.md` frontmatter `permission.edit` is an object (not shorthand) per DQ2+DQ3 LOCKED + DEC-0122 §2: keys in order — `docs/product/**` → `allow`, `handoffs/po_to_tl.md` → `allow`, `**` → `deny` (last key, deny-last ordering). `permission.bash: "deny"`; `permission.task: "deny"` (DQ4 — role agents do not spawn sub-tasks; BUG-0006 spawn-only via orchestrator); `mode: "subagent"` (DQ5). Prompt body states role + allowed artifacts only (≤ 2 KiB; no clone markers). Tests: marker 2 (`test_us0122_po_permission_object_form`) asserts non-shorthand; marker 3 (`test_us0122_po_production_code_denial`) asserts deny-last ordering + no production allow. (AC-2, AC-3)

- [x] **T-003**: `template/.opencode/agents/auto.md` frontmatter per DQ4+DQ5 LOCKED + DEC-0122 §2: `permission.edit: "deny"` (no phase-artifact writes); `permission.bash: "deny"` (orchestrator spawns Task, not shell); `permission.task` object with 7 role names (`po`, `tech-lead`, `dev`, `qa`, `release`, `curator`, `security`) → `allow` + `*` → `deny` (last key — denies all non-kit subagents including OpenCode built-ins and any future US-0124 plugin-internal helpers); `mode: "primary"`. Prompt body states orchestrator role + Task-spawns role agents only. Test: marker 4 (`test_us0122_auto_task_allowlist`) asserts exact 7-role set + `*` deny last. (AC-2)

- [x] **T-004**: `template/.opencode/agents/security.md` frontmatter per DQ6 LOCKED + DEC-0122 §2: `permission.edit: "deny"` (findings-oriented, no write surface in v1); `permission.bash: "ask"` (read-only grep/scan); `permission.task: "deny"`; `mode: "subagent"`. Findings return as conversation turn text or Task result back to the orchestrator. No committed `handoffs/security_findings/` directory (YAGNI; deferred to US-0126 if persisted findings needed). Test: marker 5 (`test_us0122_security_edit_denied`) asserts `edit: "deny"`. (AC-5)

- [x] **T-005**: `template/.opencode/agents/{tech-lead,dev,qa,release,curator}.md` frontmatter permission matrices per DEC-0122 §2 (locked matrix):
  - `tech-lead`: `edit` object — `docs/engineering/architecture.md`, `docs/engineering/decisions.md`, `docs/engineering/state.md`, `docs/engineering/research.md`, `decisions/DEC-*.md`, `handoffs/tl_to_dev.md`, `sprints/Sxxxx/sprint.md`, `sprints/Sxxxx/tasks.md` → `allow`, `**` → `deny` (last); `bash: "deny"`; `task: "deny"`; `mode: "subagent"`.
  - `dev`: `edit` object — `scripts/**`, `its_magic/**`, `template/**`, `tests/**`, `sprints/Sxxxx/progress.md`, `sprints/Sxxxx/qa-findings.md`, `handoffs/dev_to_qa.md` → `allow`, `**` → `deny` (last); `bash: "ask"` (dev runs build/test; host prompts operator); `task: "deny"`; `mode: "subagent"`.
  - `qa`: `edit` object — `sprints/Sxxxx/qa-findings.md`, `sprints/Sxxxx/plan-verify.json`, `sprints/Sxxxx/verify-work-findings.md`, `sprints/Sxxxx/uat.md`, `sprints/Sxxxx/uat.json`, `handoffs/qa_to_dev.md`, `handoffs/qa_to_verify.md`, `handoffs/qa_to_verify_work.md` → `allow`, `**` → `deny` (last); `bash: "ask"` (qa runs pytest/validators); `task: "deny"`; `mode: "subagent"`.
  - `release`: `edit` object — `handoffs/release_queue.md`, `handoffs/release_notes.md`, `handoffs/releases/*.md`, `handoffs/release_to_dev.md`, `handoffs/verify_to_release.md`, `CHANGELOG.md`, `template/CHANGELOG.md` → `allow`, `**` → `deny` (last); `bash: "ask"` (release runs git/publish probes); `task: "deny"`; `mode: "subagent"`.
  - `curator`: `edit` object — `docs/engineering/state.md`, `docs/engineering/state-archive/**`, `docs/engineering/decisions.md`, `docs/engineering/research.md`, `handoffs/resume_brief.md`, `handoffs/portfolio_state.md`, `handoffs/continuation_hygiene.md`, `handoffs/archive/**` → `allow`, `**` → `deny` (last); `bash: "deny"`; `task: "deny"`; `mode: "subagent"`.
  - **Critic NB `ik_us0122_dev_template_allow_mutates_agents` closed**: `dev` `template/**` allow could mutate `.opencode/agents/*.md` (since `template/.opencode/agents/` lives under `template/**`). Mitigation: T-006 marker 1 (`test_us0122_agent_inventory`) + T-009 parity extension assert `template/.opencode/agents/*.md` byte-identical between active and template pack; drift would fail `--scope=opencode-adapter` parity. Risk documented here. No narrow deny glob added (would fragment the locked matrix; parity gate is sufficient). (AC-2, AC-10)

- [x] **T-006**: Create `tests/us0122_contract_test.py` with 8 markers per architecture AC-8 table:
  1. `test_us0122_agent_inventory` — 8 markdown files present in `template/.opencode/agents/`; names match US-0003 role set + `auto` (AC-1, AC-5).
  2. `test_us0122_po_permission_object_form` — `po.md` `permission.edit` is an object (not shorthand) (AC-2).
  3. `test_us0122_po_production_code_denial` — deny-last ordering; no production allow (`scripts/**`, `its_magic/**`, `**/*.py`, `installer.*`, `template/scripts/**`, `template/its_magic/**`); success test (c) static (AC-3, AC-10).
  4. `test_us0122_auto_task_allowlist` — `auto.md` `permission.task` exact 7-role set + `*` deny last; built-in subagents denied by `*` (AC-2).
  5. `test_us0122_security_edit_denied` — `security.md` `permission.edit: "deny"`; findings-oriented (AC-5).
  6. `test_us0122_no_vendor_slugs_in_template` — grep `deepseek|moonshot|kimi|glm|claude|gpt|sonnet|opus|haiku|o1|o3|sk-` in `template/.opencode/agents/*.md` → zero hits (AC-7).
  7. `test_us0122_prompt_size_clone_guard` — each `template/.opencode/agents/<role>.md` ≤ 2 KiB total; no forbidden clone markers (AC-4).
  8. `test_us0122_role_id_parity` — role identifiers match US-0003 (`po`, `tech-lead`, `dev`, `qa`, `release`, `curator`, `security`); no extra v1 product roles; `auto` is orchestrator (AC-5, AC-9).
  **Critic NB `ik_us0122_compose_guards_marker_surjection` closed**: do NOT add a 9th `test_us0122_compose_guards_unchanged` marker. AC-9 surjection is via T-anch compose-guards baseline (read-only inspection of US-0003/US-0023/BUG-0006/US-0002/US-0004 surfaces) + DEC-0122 §compose surface table + marker 8 (`test_us0122_role_id_parity` asserts US-0003 role-id parity). 8-marker budget locked in architecture AC-8 table. Mirror to `template/tests/us0122_contract_test.py` byte-identical for parity pairing. (AC-8)

- [x] **T-007**: Add `template/.opencode/agents/**` source rows under `[opencode_install_include_paths]` in `docs/engineering/context/installer-owned-paths.manifest` AND `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical). Existing rows (`.opencode/agents`, `.opencode/commands`, `.opencode/plugins`, `.opencode/.gitignore`, `.opencode/README.md`) UNCHANGED — additive `template/.opencode/agents/**` source rows only. Triple-installer (PS/Bash/Python) reads opencode sections only when `--host` includes opencode (US-0121 compose; `host_gates_cursor_row` predicate). (AC-1)

- [x] **T-008**: Add `## OpenCode role agents and permissions (US-0122)` h2 to `docs/engineering/runbook.md` as a **one-liner** per DEC-0122 §5: "With the pack installed via `--host opencode|both`, an operator can `@po` (or `@<role>` for any of the seven role agents) in the OpenCode chat to invoke that role manually, before the US-0124 plugin exists." Full OpenCode operator runbook deferred to US-0126. T-008 does NOT author a full runbook section. **Critic NB C3 closed**: T-008 ships one runbook h2 one-liner only. (AC-6)

- [x] **T-009**: Update `template/.opencode/README.md` to document the eight agent files (`po`, `tech-lead`, `dev`, `qa`, `release`, `curator`, `security`, `auto`) + locked permission matrix pointer (DEC-0122 §2). Extend `scripts/check_intake_template_parity.py` `--scope=opencode-adapter` `OPENCODE_ADAPTER_PAIRS` to cover agent inventory (8 markdown files byte-identical between active `template/.opencode/agents/` and template pack — no active kit mirror; DQ8 YAGNI inherits R-0109 Q9 US-0121). Mirror parity script to `template/scripts/check_intake_template_parity.py` byte-identical. **Critic NB `ik_us0122_dev_template_allow_mutates_agents` closed**: parity extension asserts `template/.opencode/agents/*.md` byte-identical; drift fails `--scope=opencode-adapter` parity. (AC-7, AC-9)

## Integration verification (post T-009 + T-006)

- [x] Test gate: `python -m pytest tests/us0122_contract_test.py -v` → 8/8 PASS
- [x] Parity gate: `check_intake_template_parity.py --scope=opencode-adapter` PASS
- [x] Parity gate: active + template manifest byte-identical
- [x] Compose gate: 5/5 UNCHANGED
- [x] No-secrets gate: vendor slug grep zero hits on agents
- [x] Size gate: each agent file ≤ 2 KiB
- [x] Clone-marker gate: zero hits in agent prompt bodies

## Files to touch (scope)

### New (create)

- `template/.opencode/agents/po.md`
- `template/.opencode/agents/tech-lead.md`
- `template/.opencode/agents/dev.md`
- `template/.opencode/agents/qa.md`
- `template/.opencode/agents/release.md`
- `template/.opencode/agents/curator.md`
- `template/.opencode/agents/security.md`
- `template/.opencode/agents/auto.md`
- `tests/us0122_contract_test.py`
- `template/tests/us0122_contract_test.py` (byte-identical mirror for parity)
- `sprints/S0122/t-anch-verification.md`

### Edit (scoped, additive only)

- `docs/engineering/context/installer-owned-paths.manifest` (add `template/.opencode/agents/**` source rows under `[opencode_install_include_paths]`)
- `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical)
- `scripts/check_intake_template_parity.py` (extend `OPENCODE_ADAPTER_PAIRS` for agent inventory)
- `template/scripts/check_intake_template_parity.py` (byte-identical mirror)
- `docs/engineering/runbook.md` (append `## OpenCode role agents and permissions (US-0122)` h2 one-liner)
- `template/.opencode/README.md` (document 8 agent files + locked matrix pointer)

### Verify read-only (no mutation)

- `docs/engineering/architecture.md # US-0122` (T-anch NO-OP)
- `decisions/DEC-0122.md` (T-anch NO-OP)

### Compose-guard UNCHANGED (DO NOT TOUCH)

| File | Reason |
|---|---|
| `docs/product/backlog.md` | US-0045 canonical status — `/closure` mutates ONLY at execution time |
| `docs/product/acceptance.md` | US-0045 derived view — same |
| Compose-guard story surfaces (US-0003, US-0023/BUG-0006, US-0121, US-0102/DEC-0087, US-0002/US-0004) | 5/5 UNCHANGED — US-0122 adds additive role agents + permission matrix only |

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (eight agents) | T-001, T-007, T-009 |
| AC-2 (permission table Layer 1) | T-002, T-003, T-005 |
| AC-3 (success test (c) static) | T-002, T-006 (marker 3) |
| AC-4 (Layer 2 short prompts + clone guard) | T-001, T-006 (marker 7) |
| AC-5 (US-0003 contract + security findings) | T-004, T-006 (markers 1, 5, 8) |
| AC-6 (manual invoke one-liner) | T-008 |
| AC-7 (no vendor slugs in template) | T-001, T-006 (marker 6), T-009 |
| AC-8 (contract tests 8 markers) | T-006 (all 8 markers) |
| AC-9 (compose, do not amend) | T-anch (baseline), T-006 (marker 8), T-009 (parity extension) |
| AC-10 (illustrative vs locked) | T-005 (locked matrix consumed), T-006 (marker 3) |

**Surjectivity check**: 10/10 ACs covered (AC-1..AC-10 each have at least 1 task). No `PLAN_AC_COVERAGE_GAP`.
