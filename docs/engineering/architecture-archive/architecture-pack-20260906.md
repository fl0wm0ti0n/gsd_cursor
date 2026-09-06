# Architecture archive pack (2026-09-06)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3000, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 19
- First archived heading: `# US-0122 — OpenCode role agents and Layer-1 permission table`
- Last archived heading: `# US-0122 — OpenCode role agents and Layer-1 permission table`
- Verification tuple (mandatory):
  - archived_body_lines=219
  - preamble_lines=1
  - retained_body_lines=2879

---

# US-0122 — OpenCode role agents and Layer-1 permission table

## Overview

**US-0122** is the second slice of the six-story OpenCode adapter epic (US-0121..US-0126). US-0121 shipped an empty-but-valid `template/.opencode/` pack + the `--host` installer switch. US-0122 populates that pack with **eight OpenCode role agents** (`po`, `tech-lead`, `dev`, `qa`, `release`, `curator`, `security`, plus orchestrator `auto`) as markdown files under `template/.opencode/agents/<role>.md`, and locks the **Layer-1 permission matrix** that the OpenCode host enforces. Layer 1 is the security control: a model that ignores its prompt still cannot let PO write production code when `edit` is `deny` on production paths (success test (c), AC-3). Layer 2 prompts stay short (role + allowed artifacts only); they MUST NOT paste `.cursor/commands/*.md` or `.mdc` bodies.

This is a **pack-population + permission-contract** change: eight new template files, a locked permission matrix consumed by `test_us0122_*`, a runbook one-liner for manual `@<role>` invoke (AC-6), and a contract-test list. The compose surface (US-0003 role identifiers, US-0023/BUG-0006 spawn-only isolation, US-0121 pack path, US-0102 volatile-ID rule, US-0002/US-0004 do-not-port) remains UNCHANGED — US-0122 adds the role agents and their permission table only.

**Research anchor**: **R-0109** US-0122 deepened findings (DQ1..DQ8 LOCKED for `/architecture`; US-0121 Q1..Q12 locks preserved, not wiped; 7 risks R1..R7 ACCEPTED; approach A1 locked; compose guards 6/6 verified). **Companion DEC**: **DEC-0122** (authored Accepted in THIS phase — captures the locked permission matrix + Task subagent ID contract + static success-test-(c) harness so US-0123..US-0126 inherit without re-deriving).

**Fresh context marker**: `tl-US0122-architecture-20260824T114500Z-fresh`
**Orchestrator run id**: `auto-20260824-01`
**Timestamp**: 2026-08-24T11:45:00Z (UTC)
**Verdict**: PASS
**Next**: `/sprint-plan`

## Approach locked (A1 — from R-0109 DQ1..DQ8)

**Approach A1** (locked): Ship eight markdown agents at `template/.opencode/agents/{po,tech-lead,dev,qa,release,curator,security,auto}.md` with YAML frontmatter (`description`, `mode`, `permission`, short `prompt` body). No repo-root `opencode.json` (R-0109 Q6 US-0121 lock preserved). `permission.edit` uses the object form with deny-last ordering (DQ2+DQ3); `permission.bash` uses shorthand; `permission.task` uses the object form for `auto` (7-role allow + `*` deny last) and `task: "deny"` shorthand for role agents (DQ4). `auto` = primary; seven role agents = subagent (not hidden) (DQ5). Security default `edit: "deny"` (DQ6 YAGNI). Success test (c) = static permission-object inspection (DQ7); runtime permission-check call deferred to US-0124. No active kit `.opencode/agents/` mirror (DQ8 YAGNI inherits R-0109 Q9 US-0121).

| Option | Summary | Verdict |
|--------|---------|---------|
| **A1** | **Markdown agents + object-form permission matrix with deny-last ordering + static success-test-(c) harness + 7-role Task allow-list + `*` deny last on `auto`** | **Preferred** — additive only; composes with US-0003/US-0023/BUG-0006/US-0121/US-0102; AC-3 provable via static inspection; critic NBs closed. |
| A2 (rejected) | JSON `agent` table at `opencode.json` / `.opencode/opencode.json` | **Rejected** — prematurely locks US-0123 provider config; separates prompts from permissions (DQ1). |
| A3 (rejected) | Runtime-only success test (c) via `permission.ask` hook | **Rejected** — depends on a host API US-0124 owns; static layer is sufficient and host-agnostic (DQ7). |
| A4 (rejected) | Committed `handoffs/security_findings/` directory + narrow glob for security | **Rejected** — YAGNI for v1; findings return as text/Task result; deferred to US-0126 (DQ6). |

## Components

### Agent file layout (DQ1 LOCKED)

```
template/.opencode/agents/
  po.md
  tech-lead.md
  dev.md
  qa.md
  release.md
  curator.md
  security.md
  auto.md
```

- One markdown file per role; filename (minus `.md`) is the OpenCode agent name.
- YAML frontmatter: `description`, `mode`, `permission` (the Layer-1 table), short `prompt` body (Layer 2).
- No repo-root `opencode.json` (R-0109 Q6 US-0121 lock preserved).
- No active kit `.opencode/agents/` mirror (DQ8 YAGNI).

### Locked Layer-1 permission matrix (DQ2+DQ3+DQ4+DQ5+DQ6 LOCKED — AC-2, AC-5, AC-10)

See `decisions/DEC-0122.md` §2 for the full eight-agent matrix table. Summary:

- **`auto`** (primary): `edit: "deny"`, `bash: "deny"`, `task` object with 7 role names → `allow` + `*` → `deny` (last). No phase-artifact writes; Task-spawns role agents only; built-in and non-kit subagents denied by `*` deny last.
- **`po`** (subagent): `edit` object — `docs/product/**` + `handoffs/po_to_tl.md` → `allow`, `**` → `deny` (last); `bash: "deny"`; `task: "deny"`.
- **`tech-lead`** (subagent): `edit` object — architecture/decisions/state/research + `decisions/DEC-*.md` + `handoffs/tl_to_dev.md` + `sprints/Sxxxx/sprint.md` + `sprints/Sxxxx/tasks.md` → `allow`, `**` → `deny` (last); `bash: "deny"`; `task: "deny"`.
- **`dev`** (subagent): `edit` object — `scripts/**`, `its_magic/**`, `template/**`, `tests/**`, `sprints/Sxxxx/progress.md`, `sprints/Sxxxx/qa-findings.md`, `handoffs/dev_to_qa.md` → `allow`, `**` → `deny` (last); `bash: "ask"`; `task: "deny"`.
- **`qa`** (subagent): `edit` object — `sprints/Sxxxx/qa-findings.md`, `plan-verify.json`, `verify-work-findings.md`, `uat.md`, `uat.json` + `handoffs/qa_to_dev.md`, `qa_to_verify.md`, `qa_to_verify_work.md` → `allow`, `**` → `deny` (last); `bash: "ask"`; `task: "deny"`.
- **`release`** (subagent): `edit` object — `handoffs/release_queue.md`, `release_notes.md`, `releases/*.md`, `release_to_dev.md`, `verify_to_release.md`, `CHANGELOG.md`, `template/CHANGELOG.md` → `allow`, `**` → `deny` (last); `bash: "ask"`; `task: "deny"`.
- **`curator`** (subagent): `edit` object — `docs/engineering/state.md`, `state-archive/**`, `decisions.md`, `research.md` + `handoffs/resume_brief.md`, `portfolio_state.md`, `continuation_hygiene.md`, `archive/**` → `allow`, `**` → `deny` (last); `bash: "deny"`; `task: "deny"`.
- **`security`** (subagent): `edit: "deny"` (findings-oriented, no write surface in v1); `bash: "ask"` (read-only grep/scan); `task: "deny"`. Findings return as text/Task result.

#### Ordering contract (DQ3 — last-match-wins, order-sensitive)

For every object-form `permission.edit`, the broad `**` → `deny` glob MUST be the **last key**. Tests assert key order, not just set membership. For `auto` `permission.task`, the `*` → `deny` glob MUST be the last key. This is the success-test-(c) anchor.

#### Task subagent ID contract (DQ4 — critic NB closed)

`auto` `permission.task` object: 7 role names as `allow` keys + `*` → `deny` last. The `*` deny denies all non-kit subagents including OpenCode built-ins and any future US-0124 plugin-internal helpers. US-0124 may add helpers as `allow` keys above the `*` deny, never remove the `*` deny last. Role agents carry `task: "deny"` shorthand (BUG-0006 spawn-only via orchestrator).

### Static success-test-(c) harness (DQ7 LOCKED — AC-3, AC-8 — critic NB closed)

Success test (c) MUST NOT depend on the model obeying the prompt. The minimum harness is a **static permission-object inspection** (required, US-0122); the optional runtime permission-check call is deferred to US-0124. AC-3 wording locked in DEC-0122 §3.

### Layer-2 short prompts + clone guard (AC-4)

Agent prompt bodies state only who the role is and which artifacts they may write. Each `template/.opencode/agents/<role>.md` file MUST be ≤ 2 KiB total AND MUST NOT contain forbidden clone markers (`/auto`, `/intake`, `/discovery`, `/research`, `/architecture`, `/sprint-plan`, `/execute`, `/qa`, `/release`, `/closure`, `/refresh-context` command-body prose; `.cursor/commands/` path literals; `---` MDC frontmatter delimiters).

### Manual invoke one-liner (AC-6 — T-008, critic NB closed)

T-008 ships a **one-liner** in `docs/engineering/runbook.md` under a new `## OpenCode role agents and permissions (US-0122)` h2. Full runbook deferred to US-0126. T-008 does NOT author a full runbook section.

### No vendor slugs in template (AC-7 — US-0102 / US-0123 compose)

`template/.opencode/agents/*.md` frontmatter MUST NOT contain a `model:` key with a real vendor slug. `test_us0122_no_vendor_slugs_in_template` greps for known vendor slug patterns and fails on any hit.

### AC-8 contract-test list (locked)

`tests/us0122_contract_test.py` — markers:

| # | Marker | AC |
|---|--------|-----|
| 1 | `test_us0122_agent_inventory` (8 markdown files present; names match US-0003 role set + `auto`) | AC-1, AC-5 |
| 2 | `test_us0122_po_permission_object_form` (`edit` is an object, not shorthand) | AC-2 |
| 3 | `test_us0122_po_production_code_denial` (deny-last ordering; no production allow; success test (c) static) | AC-3, AC-10 |
| 4 | `test_us0122_auto_task_allowlist` (exact 7-role set + `*` deny last; built-in subagents denied) | AC-2 |
| 5 | `test_us0122_security_edit_denied` (`edit: "deny"`; findings-oriented) | AC-5 |
| 6 | `test_us0122_no_vendor_slugs_in_template` (grep `deepseek|moonshot|kimi|glm|claude|gpt|sonnet|opus|haiku|o1|o3|sk-` → zero hits) | AC-7 |
| 7 | `test_us0122_prompt_size_clone_guard` (≤ 2 KiB per file; no forbidden clone markers) | AC-4 |
| 8 | `test_us0122_role_id_parity` (role identifiers match US-0003; no extra v1 product roles) | AC-5, AC-9 |

Surjective AC coverage: AC-1 (marker 1), AC-2 (markers 2, 4), AC-3 (marker 3), AC-4 (marker 7), AC-5 (markers 1, 5, 8), AC-6 (T-008 runbook one-liner), AC-7 (marker 6), AC-8 (full set), AC-9 (compose guards verified separately + marker 8), AC-10 (marker 3 + the locked matrix in DEC-0122). Every AC has ≥1 marker.

## Risks mitigated

All 7 risks from R-0109 US-0122 ACCEPTED, plus 3 critic NBs closed:

| Risk | Severity | Mitigation |
|------|----------|------------|
| R1: Permission glob ordering drift | MEDIUM → LOW | DQ3 deny-last ordering locked; markers 2, 3 assert key order. |
| R2: PO `edit` shorthand vs object form regression | MEDIUM → LOW | DQ2 object form locked; marker 2 asserts non-shorthand. |
| R3: Orchestrator Task allow-list leak | MEDIUM → LOW | DQ4 7-role allow + `*` deny last; marker 4 asserts exact set + `*` deny. |
| R4: Security findings-only surface leak | LOW–MEDIUM → LOW | DQ6 default `edit: "deny"`; marker 5 asserts deny. |
| R5: Vendor slug leakage | LOW | marker 6 (US-0102 family). |
| R6: Prompt-body bloat / clone drift | LOW | T-001 short prompts; marker 7 (grep + 2 KiB cap). |
| R7: Active kit mirror accidentally created | LOW | DQ8 YAGNI; T-009 parity validator asserts no active mirror. |
| C1 (critic NB): AC-3 static-vs-runtime harness wording | → closed | AC-3 locked as static permission-object inspection; runtime deferred to US-0124 (DEC-0122 §3). |
| C2 (critic NB): Task deny for non-kit subagents | → closed | DQ4 `*` deny last denies all non-kit subagents including built-ins (DEC-0122 §2 Task subagent ID contract). |
| C3 (critic NB): T-008 one-liner not full runbook | → closed | T-008 ships one runbook h2 one-liner; full runbook deferred to US-0126 (DEC-0122 §5). |

## Non-goals (this slice)

- **US-0123** (per-role `provider/slug` routing) — `model:` omitted/placeholder; no real slugs.
- **US-0124** (orchestrator plugin spawn loop) — no plugin body; runtime permission-check harness deferred; v1/v2 plugin choice deferred.
- **US-0125** (thin command bodies) — `template/.opencode/commands/` ships `.gitkeep` only (US-0121 pack).
- **US-0126** (full runbook) — T-008 one-liner only.
- **Repo-root `opencode.json`** — not shipped (R-0109 Q6 US-0121 lock preserved).
- **Active kit `.opencode/agents/` mirror** — YAGNI (DQ8 inherits R-0109 Q9 US-0121).
- **Committed `handoffs/security_findings/` directory** — YAGNI (DQ6).
- **Runtime permission-check test** — deferred to US-0124 (DQ7).

## Compose guards (UNCHANGED — additive only)

| Compose target | Verification | Result |
|---|---|---|
| US-0003 (role set) | inline ref — same role identifiers; no extra v1 product roles | ✅ read-only (additive) |
| US-0023 / BUG-0006 (spawn-only isolation) | inline ref — `auto` Task-spawns role agents; no same-session roleplay | ✅ read-only |
| US-0121 (pack path) | `# US-0121` — US-0122 consumes `template/.opencode/**`; no repo-root `opencode.json` added | ✅ read-only (additive) |
| US-0102 / DEC-0087 (volatile-ID rule) | inline ref — no vendor slugs in `template/.opencode/agents/*.md` | ✅ read-only |
| US-0002 / US-0004 (do-not-port Cursor rules/skills) | inline ref — markdown agents, no `.mdc`/rules/skills clone | ✅ NOT ported |

Contract test `test_us0122_compose_guards_unchanged` enforces at execute boundary.

## Sprint seeds preview (within SPRINT_MAX_TASKS=12)

| Seed | Description | AC |
|------|-------------|-----|
| **T-anch** | Verify `# US-0122` H1 anchor present; DEC-0122 Accepted; compose guards 5/5; 8-marker list locked; locked matrix in DEC-0122 §2. | AC-9, AC-10 |
| **T-001** | NEW 8 markdown agent files `template/.opencode/agents/{po,tech-lead,dev,qa,release,curator,security,auto}.md` with frontmatter `description`, `mode`, `permission`, short prompt body. | AC-1, AC-4 |
| **T-002** | PO `edit` object form: `docs/product/**` + `handoffs/po_to_tl.md` allow + `**` deny last; `bash: "deny"`; `task: "deny"`. | AC-2, AC-3 |
| **T-003** | `auto` orchestrator `edit: "deny"`; `task` object with 7 role allow + `*` deny last; `mode: "primary"`; `bash: "deny"`. | AC-2 |
| **T-004** | Security agent `edit: "deny"` findings-oriented; `bash: "ask"`; `task: "deny"`; `mode: "subagent"`. | AC-5 |
| **T-005** | Remaining role agents `tech-lead`, `dev`, `qa`, `release`, `curator` permission matrices per DEC-0122 §2; `mode: "subagent"`; `task: "deny"`. | AC-2, AC-10 |
| **T-006** | Contract tests `tests/us0122_contract_test.py` — 8 markers. | AC-8 |
| **T-007** | Installer manifest rows for `template/.opencode/agents/**` under `[opencode_install_include_paths]` + triple-installer parity (US-0121 compose). | AC-1 |
| **T-008** | Runbook cross-link `## OpenCode role agents and permissions (US-0122)` h2 one-liner for AC-6 (full runbook deferred to US-0126). | AC-6 |
| **T-009** | README + template parity + `check_intake_template_parity.py --scope=opencode-adapter` extension for agent inventory; no active mirror. | AC-7, AC-9 |

**Total: 10 tasks (T-anch + T-001..T-009) — within `SPRINT_MAX_TASKS=12`.** `/sprint-plan` may merge or split within the 12-task budget.

## DC check

`dc_check=clean`. No `# US-0122` or `## US-0122` existed prior to THIS write. H1 anchor added per DEC-0076 / BUG-0010 heading policy. Deferral register clean.

## Stop conditions

- `decision_gate=false`
- `missing_acceptance_criteria=none` (10/10 ACs covered by 8 contract-test markers + compose guards + T-008 runbook one-liner)
- `compose_guards=5/5 UNCHANGED (additive only)`
- `dc_check=clean`
- DQ1..DQ8 LOCKED for US-0122; 7/7 R ACCEPTED; A1 locked; 3 critic NBs closed
- Triad baseline `baseline_h2_count` preserved (H1 used, not H2)
- `validator_skipped=python_not_on_path` (Windows Store stub; `py -3` and `python` both missing — exit 9009); H2 count verified via PowerShell `Select-String -Pattern '^## US-'` (unchanged from US-0121 baseline)
- `enforce-triad-hot-surface.py --rollover/--check` skipped (python missing); `materialize_codebase_map.py --trigger architecture` skipped (python missing); not blocking per orchestrator brief

## Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called. No write to `mistakes.jsonl`.

## Consequences

- **Positive**: Operators can `@<role>` invoke any of the seven role agents with host-enforced permissions before the US-0124 plugin exists; success test (c) is provable via static permission-object inspection; epic US-0123..US-0126 inherits the locked matrix via DEC-0122 without re-deriving; US-0003 role identifiers and US-0023/BUG-0006 spawn-only isolation compose unchanged.
- **Negative**: Eight new template files; new contract test file (8 markers); `--scope=opencode-adapter` parity extension; runbook h2 one-liner.
- **Neutral**: US-0121 pack path consumed (additive); US-0102 volatile-ID rule respected; US-0002/US-0004 do-not-port rule respected.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=architecture`, `role=tech-lead`, `story_id=US-0122`, `sprint_id=(pending — created at sprint-plan)`
- `orchestrator_run_id=auto-20260824-01`
- `delivery_mode=ultra_lean`, `macro_phase=plan` (architecture — second canonical phase of `plan` macro per US-0096 / DEC-0082)
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required; this spawn's producer model)
- `fresh_context_marker=tl-US0122-architecture-20260824T114500Z-fresh`, `timestamp=2026-08-24T11:45:00Z` (UTC)
- `evidence_ref=docs/engineering/architecture.md # US-0122 (this section), decisions/DEC-0122.md (companion DEC), docs/engineering/research.md ## R-0109 (US-0122 deepened findings DQ1..DQ8 LOCKED), docs/product/backlog.md ## US-0122 (D1..D10 + 10 ACs + DQ1..DQ8, status OPEN untouched, AC checkboxes untouched), docs/product/acceptance.md US-0122 row L150 (unchecked), docs/product/vision.md ## Discovery Notes — US-0122, handoffs/po_to_tl.md US-0122 top section, handoffs/sovereign_critic_findings.jsonl US-0122 research rows (3 non-blocking carry-forwards closed here), docs/engineering/architecture.md # US-0121 (format template), docs/engineering/decisions.md ## DEC-0120 (last DEC id), decisions/DEC-0120.md (full read as DEC-0122 template), handoffs/resume_brief.md (US-0122 sovereign-critic PASS prepend)`
- Fresh tech-lead subagent per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to narrow-read files (US-0053). No `.env` reads, no credentials access, no intake-evidence mutation, no backlog status/AC mutation.
- Prior proof consumed: `rp-auto-20260824-01-research-techlead-20260824T113700Z-US-0122` (from `docs/engineering/state.md` research checkpoint, unchanged).
- Triad baseline `baseline_h2_count` preserved via H1 anchor (no new H2 `## US-` headings added).

## Strict runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-architecture-tech-lead-20260824T114500Z-US-0122`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"architecture","proof_issued_at":"2026-08-24T11:45:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260824-01-architecture-tech-lead-20260824T114500Z-US-0122","sprint_id":"(pending)","story_id":"US-0122"}`
- `proof_hash=6C636966FA3D86C026708B84EB03B91154D9C9EB511A2C794369637ACE9A402C` (SHA-256, UTF-8 bytes via PowerShell — python missing on PATH)
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T12:45:00Z` (UTC)

## Decision gate

- `decision_gate=false` (companion DEC-0122 authored Accepted in THIS phase; approach A1 locked; DQ1..DQ8 LOCKED for US-0122; 7/7 R ACCEPTED; 3 critic NBs closed; DC check clean; compose guards 5/5 UNCHANGED)
- `stop_conditions_met=yes`

## Next scheduled phase

- `next_scheduled_phase=/sprint-plan` (role=tech-lead per US-0069 / DEC-0051 phase→role matrix default; third canonical phase of `plan` macro per ultra_lean; research + architecture + sprint-plan merged into `plan` macro)
- `next_scheduled_role=tech-lead`
- `stop_condition=STOP after architecture completes; hand off via artifacts only to /sprint-plan in fresh tech-lead subagent (BUG-0006). Do not spawn /sprint-plan from this subagent.`






