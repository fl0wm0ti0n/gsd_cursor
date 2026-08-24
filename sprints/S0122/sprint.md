# Sprint S0122 - Sprint Plan (US-0122)

## Metadata

| Field | Value |
|---|---|
| story_id | US-0122 |
| story_title | OpenCode role agents and Layer-1 permission table |
| sprint_id | S0122 |
| delivery_mode | ultra_lean |
| macro_phase | plan (sprint-plan — terminal canonical phase per ultra_lean; /plan-verify runs standalone per orchestrator brief, role=qa) |
| current_phase | sprint-plan |
| approach | A1 locked |
| companion_DEC | DEC-0122 (Accepted) |
| research_anchor | R-0109 (DQ1..DQ8 LOCKED for US-0122; US-0121 Q1..Q12 locks preserved) |
| orchestrator_run_id | auto-20260824-01 |
| fresh_context_marker | tl-US0122-sprint-plan-20260824T120000Z-fresh |
| timestamp | 2026-08-24T12:00:00Z (UTC) |
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

Ship the second slice of the OpenCode adapter epic: populate `template/.opencode/agents/` with **eight markdown role agents** (`po`, `tech-lead`, `dev`, `qa`, `release`, `curator`, `security`, plus orchestrator `auto`) carrying YAML frontmatter (`description`, `mode`, `permission`, short `prompt` body), and lock the **Layer-1 permission matrix** that the OpenCode host enforces. Layer 1 is the security control: a model that ignores its prompt still cannot let PO write production code when `edit` is `deny` on production paths (success test (c), AC-3). Layer 2 prompts stay short (role + allowed artifacts only); they MUST NOT paste `.cursor/commands/*.md` or `.mdc` bodies. Locked matrix in `decisions/DEC-0122.md` §2 consumed by `test_us0122_*` (8 markers). Runbook one-liner for manual `@<role>` invoke (AC-6); full runbook deferred to US-0126. `--scope=opencode-adapter` parity extended for agent inventory. No repo-root `opencode.json`. No active kit `.opencode/agents/` mirror (DQ8 YAGNI). No vendor slugs in template (AC-7).

Out of scope: US-0123 per-role `provider/slug` routing, US-0124 orchestrator plugin spawn loop + runtime permission-check hook, US-0125 thin command bodies, US-0126 full runbook, repo-root `opencode.json`, active kit `.opencode/agents/` mirror, committed `handoffs/security_findings/` directory, runtime permission-check test.

## Acceptance criteria (10) - US-0122 (status OPEN, checkboxes untouched per US-0045)

- **AC-1**: Eight agents — template ships OpenCode agents for `po`, `tech-lead`, `dev`, `qa`, `release`, `curator`, `security`, plus orchestrator `auto` (primary). File names / `opencode.json` keys are deterministic and documented.
- **AC-2**: Permission table (Layer 1) — each agent has `permission` for at least `edit`, `bash`, and `task`. Orchestrator: `edit` deny; `task` allow only for the seven role agents (allow-list + `*` deny last). `po`: `edit` allow only under `docs/product/**` and `handoffs/po_to_tl.md`; production/code paths `deny`. Exact globs locked in `/architecture` + DEC-0122 §2.
- **AC-3**: Success test (c) — contract test proves PO cannot write a production/code path via **static permission-object inspection** (frontmatter parse + deny-last ordering assertion + no-production-allow assertion), even if the agent prompt is emptied or contradictory (host permission, not prose). Optional runtime permission-check call deferred to US-0124.
- **AC-4**: Layer 2 short prompts — agent bodies state who the role is and which artifacts they may write. They must not paste `.cursor/commands/*.md` bodies. A size/grep guard fails on oversized command clones (≤ 2 KiB per file; no forbidden clone markers).
- **AC-5**: US-0003 contract — role identifiers match the kit role set; no extra product roles in v1. Security agent is findings-oriented (`edit` deny or findings-only paths).
- **AC-6**: Manual invoke — with pack installed, an operator can `@po` (or OpenCode equivalent) without the US-0124 plugin. Document the manual path in a one-liner; full runbook is US-0126.
- **AC-7**: No vendor slugs in template agents — `model:` in `template/` stays placeholder / omitted; real `provider/slug` is US-0123.
- **AC-8**: Contract tests — `test_us0122_*` cover agent inventory, permission deny-lists, success test (c), prompt-size/clone guard, and US-0003 role-id parity.
- **AC-9**: Compose, do not amend — US-0003 role semantics, US-0023 isolation, BUG-0006 spawn-only unchanged. Do not treat `.mdc` / Cursor skills as OpenCode enforcement.
- **AC-10**: Illustrative vs locked — intake table is illustrative; architecture publishes the locked permission matrix consumed by tests (DEC-0122 §2).

## Task summaries (10 - T-anch + T-001..T-009)

- **T-anch** (NO-OP / verification): Verify `# US-0122` H1 anchor present in `docs/engineering/architecture.md`; verify DEC-0122 authored Accepted at `decisions/DEC-0122.md`; verify compose guards 5/5 UNCHANGED baseline (US-0003, US-0023/BUG-0006, US-0121, US-0102/DEC-0087, US-0002/US-0004); verify 8-marker contract-test list locked in architecture; verify locked Layer-1 permission matrix in DEC-0122 §2; verify `template/.opencode/agents/` ships `.gitkeep` only (no role files yet); verify `tests/us0122_contract_test.py` does NOT yet exist. Record results to `sprints/S0122/t-anch-verification.md`. (AC-9, AC-10 baseline; NO-OP / verification only)
- **T-001** (NEW 8 markdown agent files): Create `template/.opencode/agents/{po,tech-lead,dev,qa,release,curator,security,auto}.md` with YAML frontmatter (`description`, `mode`, `permission`, short `prompt` body). One file per role; filename (minus `.md`) is the OpenCode agent name. No repo-root `opencode.json`. No active kit `.opencode/agents/` mirror (DQ8 YAGNI). No vendor slugs, no `model:` literals (AC-7, US-0102). (AC-1, AC-4)
- **T-002** (PO `edit` object form): `template/.opencode/agents/po.md` frontmatter `permission.edit` is an object (not shorthand): `docs/product/**` → `allow` + `handoffs/po_to_tl.md` → `allow` + `**` → `deny` (last key, deny-last ordering). `permission.bash: "deny"`; `permission.task: "deny"`; `mode: "subagent"`. Prompt body states role + allowed artifacts only (≤ 2 KiB; no clone markers). (AC-2, AC-3)
- **T-003** (`auto` orchestrator): `template/.opencode/agents/auto.md` frontmatter `permission.edit: "deny"` (no phase-artifact writes); `permission.bash: "deny"` (orchestrator spawns Task, not shell); `permission.task` object with 7 role names (`po`, `tech-lead`, `dev`, `qa`, `release`, `curator`, `security`) → `allow` + `*` → `deny` (last key). `mode: "primary"`. (AC-2)
- **T-004** (Security agent): `template/.opencode/agents/security.md` frontmatter `permission.edit: "deny"` (findings-oriented, no write surface in v1); `permission.bash: "ask"` (read-only grep/scan); `permission.task: "deny"`; `mode: "subagent"`. Findings return as text/Task result. (AC-5)
- **T-005** (Remaining role agents): `template/.opencode/agents/{tech-lead,dev,qa,release,curator}.md` frontmatter permission matrices per DEC-0122 §2: `tech-lead` (architecture/decisions/state/research + `decisions/DEC-*.md` + `handoffs/tl_to_dev.md` + `sprints/Sxxxx/sprint.md` + `sprints/Sxxxx/tasks.md`); `dev` (`scripts/**`, `its_magic/**`, `template/**`, `tests/**`, `sprints/Sxxxx/progress.md`, `sprints/Sxxxx/qa-findings.md`, `handoffs/dev_to_qa.md`; `bash: "ask"`); `qa` (qa-findings + plan-verify + verify-work-findings + uat.md/json + qa handoffs; `bash: "ask"`); `release` (release_queue/notes/releases + release/verify handoffs + CHANGELOG; `bash: "ask"`); `curator` (state + state-archive + decisions.md + research.md + resume_brief/portfolio_state/continuation_hygiene/archive; `bash: "deny"`). All `mode: "subagent"`; `task: "deny"`; `**` → `deny` last. **Critic NB closed**: `dev` `template/**` allow could mutate `.opencode/agents/*.md` — document mutation risk in T-005 task note; T-006 marker 1 + T-009 parity extension assert `template/.opencode/agents/*.md` byte-identical between active and template pack; drift fails `--scope=opencode-adapter` parity. (AC-2, AC-10)
- **T-006** (Contract tests): Create `tests/us0122_contract_test.py` with 8 markers per architecture AC-8 table: (1) `test_us0122_agent_inventory` [AC-1, AC-5]; (2) `test_us0122_po_permission_object_form` [AC-2]; (3) `test_us0122_po_production_code_denial` [AC-3, AC-10]; (4) `test_us0122_auto_task_allowlist` [AC-2]; (5) `test_us0122_security_edit_denied` [AC-5]; (6) `test_us0122_no_vendor_slugs_in_template` [AC-7]; (7) `test_us0122_prompt_size_clone_guard` [AC-4]; (8) `test_us0122_role_id_parity` [AC-5, AC-9]. **Critic NB closed**: do NOT add a 9th `test_us0122_compose_guards_unchanged` marker — AC-9 surjection is via T-anch compose-guards baseline + DEC-0122 §compose surface table + marker 8 (`test_us0122_role_id_parity` asserts US-0003 role-id parity). 8-marker budget locked. (AC-8)
- **T-007** (Installer manifest rows): Add `template/.opencode/agents/**` source rows under `[opencode_install_include_paths]` in `docs/engineering/context/installer-owned-paths.manifest` AND `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical). Existing rows (`.opencode/agents`, `.opencode/commands`, `.opencode/plugins`, `.opencode/.gitignore`, `.opencode/README.md`) UNCHANGED — additive `template/.opencode/agents/**` source rows only. Triple-installer (PS/Bash/Python) reads opencode sections only when `--host` includes opencode (US-0121 compose). (AC-1)
- **T-008** (Runbook cross-link): Add `## OpenCode role agents and permissions (US-0122)` h2 to `docs/engineering/runbook.md` as a **one-liner**: "With the pack installed via `--host opencode|both`, an operator can `@po` (or `@<role>` for any of the seven role agents) in the OpenCode chat to invoke that role manually, before the US-0124 plugin exists." Full OpenCode operator runbook deferred to US-0126. T-008 does NOT author a full runbook section. (AC-6)
- **T-009** (README + parity extension): Update `template/.opencode/README.md` to document the eight agent files + locked permission matrix pointer (DEC-0122 §2). Extend `scripts/check_intake_template_parity.py` `--scope=opencode-adapter` `OPENCODE_ADAPTER_PAIRS` to cover agent inventory (8 markdown files byte-identical between active `template/.opencode/agents/` and template pack — no active kit mirror; DQ8 YAGNI). Mirror parity script to `template/scripts/check_intake_template_parity.py` byte-identical. (AC-7, AC-9)

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 | T-001, T-007, T-009 |
| AC-2 | T-002, T-003, T-005 |
| AC-3 | T-002, T-006 (marker 3) |
| AC-4 | T-001, T-006 (marker 7) |
| AC-5 | T-004, T-006 (markers 1, 5, 8) |
| AC-6 | T-008 |
| AC-7 | T-001, T-006 (marker 6), T-009 |
| AC-8 | T-006 (all 8 markers) |
| AC-9 | T-anch (baseline), T-006 (marker 8), T-009 (parity extension) |
| AC-10 | T-005 (locked matrix consumed), T-006 (marker 3) |

**Surjectivity check**: 10/10 ACs covered (each AC has at least 1 task). No `PLAN_AC_COVERAGE_GAP`.

## Critic carry-ins (3 non-blocking findings from architecture sovereign-critic — not silently dropped)

- `ik_us0122_dev_template_allow_mutates_agents` → T-005 task note: `dev` `template/**` allow could mutate `.opencode/agents/*.md`. Mitigation: T-006 marker 1 (`test_us0122_agent_inventory`) + T-009 parity extension assert `template/.opencode/agents/*.md` byte-identical between active and template pack; drift would fail `--scope=opencode-adapter` parity. Risk documented in T-005 task note. No narrow deny glob added (would fragment the locked matrix; parity gate is sufficient).
- `ik_us0122_compose_guards_marker_surjection` → T-006 task note: do NOT add a 9th `test_us0122_compose_guards_unchanged` marker. AC-9 surjection is via T-anch compose-guards baseline (read-only inspection) + DEC-0122 §compose surface table + marker 8 (`test_us0122_role_id_parity` asserts US-0003 role-id parity). 8-marker budget locked in architecture AC-8 table.
- `ik_us0122_stale_compose_count_6_vs_5` → T-anch task note: architecture overview line says "compose guards 6/6 verified" (stale — carried over from research checkpoint). Architecture compose-guards table lists 5/5. T-anch verifies 5/5 (US-0003, US-0023/BUG-0006, US-0121, US-0102/DEC-0087, US-0002/US-0004). No architecture.md mutation in /execute (T-anch NO-OP); the 6/6 vs 5/5 wording discrepancy is a non-blocking documentation drift to be reconciled at /plan-verify or in a future doc-parity slice.

## Compose guards (5/5 UNCHANGED — additive only)

| Compose target | Verification | Result |
|---|---|---|
| US-0003 (role set) | inline ref — same role identifiers (`po`, `tech-lead`, `dev`, `qa`, `release`, `curator`, `security`); no extra v1 product roles; marker 8 asserts parity | ✅ read-only (additive) |
| US-0023 / BUG-0006 (spawn-only isolation) | inline ref — `auto` Task-spawns role agents; no same-session roleplay; role agents `task: "deny"` shorthand | ✅ read-only |
| US-0121 (pack path) | `# US-0121` — US-0122 consumes `template/.opencode/**`; no repo-root `opencode.json` added; default install host remains cursor-only until explicit `--host opencode\|both` | ✅ read-only (additive) |
| US-0102 / DEC-0087 (volatile-ID rule) | inline ref — no vendor slugs in `template/.opencode/agents/*.md`; `model:` omitted/placeholder; US-0123 owns real provider/slug routing | ✅ read-only |
| US-0002 / US-0004 (do-not-port Cursor rules/skills) | inline ref — markdown agents, no `.mdc`/rules/skills clone; Layer-2 prompts MUST NOT paste `.cursor/commands/*.md` bodies | ✅ NOT ported |

Contract test `test_us0122_role_id_parity` (marker 8) enforces US-0003 role-id parity at execute boundary. Compose-guards baseline verified read-only in T-anch.

## Task dependency graph

```
[T-anch] --> [T-001] (8 agent files) --> [T-002, T-003, T-004, T-005 parallel] (per-agent permission matrices)
                                  |
                                  v
                              [T-007] (manifest rows, after T-001)
                                  |
                                  v
                              [T-009] (README + parity extension, after T-001 + T-007)
                                  |
                                  v
                              [T-008] (runbook one-liner, after T-001)
                                  |
                                  v
                              [T-006] (contract tests last, assert all outputs)
                                  |
                                  v
                          Integration verification
```

**Execution order (deterministic)**: T-anch → T-001 (all 8 agent files) → {T-002, T-003, T-004, T-005 parallel (per-agent permission matrices verified)} → T-007 (manifest rows) → T-009 (README + parity) → T-008 (runbook one-liner) → T-006 (contract tests last, assert all outputs) → integration verification.

## Execute phase role (per DEC-0051 / US-0069)

| Phase | Role | Isolation |
|---|---|---|
| /plan-verify | qa (fresh per BUG-0006) | {phase_id:plan-verify, role:qa} — standalone per orchestrator brief |
| /execute | dev (fresh per BUG-0006) | {phase_id:execute, role:dev} |
| /qa | qa (fresh) | {phase_id:qa, role:qa} |
| /verify-work | qa (fresh) | {phase_id:verify-work, role:qa} |
| /release | release (fresh) | {phase_id:release, role:release} |
| /closure | qe (fresh) | {phase_id:closure, role:qe} |
| /refresh-context | curator (fresh) | {phase_id:refresh-context, role:curator} |

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

| Field | Value |
|---|---|
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0122 |
| sprint_id | S0122 |
| orchestrator_run_id | auto-20260824-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| fresh_context_marker | tl-US0122-sprint-plan-20260824T120000Z-fresh |
| timestamp | 2026-08-24T12:00:00Z (UTC) |
| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 — required) |
| evidence_ref | sprints/S0122/sprint.md, sprints/S0122/tasks.md, sprints/S0122/progress.md, sprints/S0122/summary.md, sprints/S0122/uat.json, sprints/S0122/uat.md, handoffs/tl_to_dev.md (US-0122 prepend), docs/engineering/state.md (sprint-plan checkpoint append-bottom), docs/engineering/architecture.md # US-0122, decisions/DEC-0122.md |

Prior phase proof consumed: `rp-auto-20260824-01-architecture-tech-lead-20260824T114500Z-US-0122` (proof_hash=6C636966FA3D86C026708B84EB03B91154D9C9EB511A2C794369637ACE9A402C). Sovereign-critic architecture PASS at 2026-08-24T11:52:00Z (anti_slop_aggregate=8; 0 blocking findings; 3 non-blocking carry-forwards routed to task notes above).

## Runtime proof (DEC-0038)

| Field | Value |
|---|---|
| runtime_proof_id | rp-auto-20260824-01-sprint-plan-tech-lead-20260824T120000Z-US-0122 |
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0122 |
| sprint_id | S0122 |
| orchestrator_run_id | auto-20260824-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 — required) |
| proof_issued_at | 2026-08-24T12:00:00Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-08-24T13:00:00Z (UTC) |
| proof_hash | 49D4165515F54421094D13675422D8A6CDBDDCBE9A82C6C5A3F3E5248FD1857D |
| canonical_payload | `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"sprint-plan","proof_issued_at":"2026-08-24T12:00:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260824-01-sprint-plan-tech-lead-20260824T120000Z-US-0122","sprint_id":"S0122","story_id":"US-0122"}` |

## Decision gate

| Field | Value |
|---|---|
| decision_gate | false |
| stop_conditions_met | yes |
| missing_acceptance_criteria | none (10/10 ACs covered by 8 contract-test markers + compose guards + T-008 runbook one-liner) |
| compose_guards | 5/5 UNCHANGED (additive only) |
| dc_check | clean |
| task_count | 10 (within SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1 but no split needed) |
| risks_finalized | 7/7 ACCEPTED (R1..R7 from R-0109 US-0122) + 3 critic NBs closed (C1 AC-3 static-vs-runtime harness; C2 Task `*` deny + full matrix; C3 T-008 one-liner) |
| approach | A1 locked |
| Q | DQ1..DQ8 LOCKED for US-0122; US-0121 Q1..Q12 locks preserved |
| plan-verify readiness | standalone /plan-verify next (role=qa per orchestrator brief); plan-verify.json NOT written in this spawn |
| sovereign_memory_note | `assemble_sovereign_memory_digest(...)` NOT called; no mistakes.jsonl write |

## Definition of done (sprint-plan)

- [x] 10 tasks enumerated (T-anch + T-001..T-009) — within SPRINT_MAX_TASKS=12
- [x] 10/10 ACs covered by 8 contract-test markers + compose guards + T-008 runbook one-liner (surjective)
- [x] Task dependency graph documented
- [x] Execute phase role matrix documented (including standalone /plan-verify per orchestrator brief)
- [x] Compose guards 5/5 UNCHANGED
- [x] Critic carry-ins (3) explicitly routed to task notes (not silently dropped)
- [x] Isolation evidence + runtime proof emitted (model_id=glm-5.2-high present)
- [x] Sprint-plan checkpoint appended to `docs/engineering/state.md` (append-bottom)
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
| artifacts_written | sprints/S0122/sprint.md, sprints/S0122/tasks.md, sprints/S0122/progress.md, sprints/S0122/summary.md, sprints/S0122/uat.json, sprints/S0122/uat.md, docs/engineering/state.md (sprint-plan checkpoint append-bottom), handoffs/tl_to_dev.md (US-0122 prepend), handoffs/resume_brief.md (sprint-plan PASS prepend → /plan-verify) |
