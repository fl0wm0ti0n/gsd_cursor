# PO to TL archive pack (2026-06-28)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 5
- Retained units in hot file: 10
- First archived heading: `## --- ##`
- Last archived heading: `## PO intake handoff — US-0111 / cursor-20260628-US0111-intake`
- Verification tuple (mandatory):
  - archived_body_lines=281
  - retained_body_lines=635

---

## --- ##

## Orchestrated architecture handoff — US-0103 / `auto-20260628-01`

### Target

- `story_id=US-0103`
- `orchestrator_run_id=auto-20260628-01`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0103-architecture-20260628T133000Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `decomposition=single_story` (per **US-0051**)
- `priority=P0`
- `delivery_mode=standard`
- `sprint_id_target=S0103` (TBD in `/sprint-plan`)
- `sovereign_loop_foundation=true`

### Summary

**`/architecture`** **PASS** — **`DEC-0103`** already accepted in research phase; **`# US-0103`** appended to `docs/engineering/architecture.md` with comprehensive section (overview, scratchpad keys, ledger artifact, helper library contract, validator CLI contract, deviation classification table, QA cross-check contract, contract tests + parity, reason codes, integration points, backward compatibility, atomic task seeds, definition of done, decision linkage). 11 task seeds prepared in `sprints/S0103/tasks.md` covering 8 ACs surjectively (within `SPRINT_MAX_TASKS=12`). Status authority (US-0045): US-0103 remains **OPEN** through `/sprint-plan`, `/plan-verify`, `/execute`, `/qa`, `/verify-work`; closure at `/release`.

### Architecture locks (sprint-plan inputs)

| Lock | Decision |
|------|----------|
| **S1 Scratchpad keys** | `AI_DECISION_LEDGER` ∈ {0, 1}, default `0`; `AUTO_PLAN_FIDELITY` ∈ {strict, relaxed, extended}, default `strict`. Zero-overhead when LEDGER=0. |
| **S2 Ledger artifact** | One file per orchestrator run at `handoffs/sovereign_decisions/<orchestrator_run_id>.jsonl`. 12-field JSONL schema v1 (all required): `ts`, `orchestrator_run_id`, `phase_id`, `role`, `decision_id`, `decision_type`, `from_artifact`, `to_artifact`, `rationale`, `plan_fidelity`, `cross_model_reviewed`, `risk_tier`. Append-only semantics with fsync-style guard. UTF-8 encoding, no BOM. |
| **S3 Helper library contract** | `scripts/decision_ledger_lib.py` with 10 functions: `resolve_ledger_path`, `append_entry`, `read_entries`, `schema_check`, `summary_digest`, `is_ledger_enabled`, `resolve_plan_fidelity`, `classify_deviation`, `build_qa_findings_block`, `build_new_entry`, `self_test`. CLI with `--self-test`, `--append-json`, `--dump-digest`. Byte-parity with `template/scripts/decision_ledger_lib.py`. |
| **S4 Validator CLI contract** | `scripts/ledger_validate.py` with flags: `--file <path>`, `--validate-all`, `--verify-integrity`, `--report`. Exit codes: 0 (success), 1 (validation failed), 2 (usage error). Byte-parity with `template/scripts/ledger_validate.py`. |
| **S5 Plan-fidelity deviation classifier** | `classify_deviation(mode, deviation_kind)` with mode ∈ {strict, relaxed, extended}, deviation_kind ∈ {drop_ac, reorder_ac, add_scope, operator_override, generic, phase_transition, delegation, derivation}. Returns (decision_type, reason_code, blocking) triple. Frozen table from DEC-0103 §3. |
| **S6 QA cross-check block builder** | `build_qa_findings_block(ledger_path, orchestrator_run_id, scratchpad)` returns dict with keys: `ledger_source` (path), `ledger_orchestrator_run_id` (string), `ledger_findings` (list of finding dicts), `ledger_summary_digest` (total/violation/override/scope_gate/extension counts + by_type dict + by_risk_tier dict), `ledger_status` (ok\|disabled\|file_missing\|schema_invalid\|corrupt), `ledger_error` (optional error message). Fail-closed on schema invalid + corrupt + file missing. |
| **S7 Reason codes inventory** | 11 codes total: `PLAN_FIDELITY_VIOLATION`, `PLAN_FIDELITY_OVERRIDE`, `PLAN_FIDELITY_SCOPE_GATE`, `PLAN_FIDELITY_EXTENSION`, `PLAN_FIDELITY_REORDER`, `LEDGER_FILE_MISSING`, `LEDGER_SCHEMA_INVALID`, `LEDGER_APPEND_FAILED`, `LEDGER_CORRUPT`, `LEDGER_READ_BOUND`, `LEDGER_DISABLED`. |
| **S8 Contract tests** | 8 `test_us0103_*` markers: `scratchpad_keys_literals`, `ledger_jsonl_schema_contract`, `strict_mode_hard_stop`, `relaxed_mode_reorder_with_ledger`, `extended_mode_nonblocking`, `qa_crosscheck_ledger_findings`, `reason_code_inventory`, `us0070_compose_no_schema_change`. Parity scope: `--scope=sovereign-ledger` with `SOVEREIGN_LEDGER_PAIRS` manifest (3 pairs). |
| **S9 Composition rules** | US-0070 (phase selection), US-0069 (role enforcement), US-0048 (isolation evidence), US-0092 (full-autonomy outer driver) are **UNCHANGED** — US-0103 writes on top. Regression guard: `test_us0103_us0070_compose_no_schema_change`. US-0111 is consumer (writes `derivation_decisions[]` to ledger as `decision_type=LEDGER_DERIVATION`). US-0104..US-0110 depend on v1 schema stability. |
| **S10 Backward compatibility** | `AI_DECISION_LEDGER=0` (default) → zero overhead, no file writes, no reads, no schema enforcement. Existing `/auto` lifecycle fully unchanged. Schema v1 architecture-locked; US-0104..US-0110 depend on v1 contract stability. `LEDGER_READ_BOUND` is warn-only, never fail-closed. |

### Integration points (carry to sprint-plan)

| Story | Compose rule |
|-------|--------------|
| **US-0070** (phase selection) | Ledger respects phase selection policy — no ledger write during skipped phases. |
| **US-0069** (role enforcement) | Ledger entries include role verification (field `role` ∈ canonical roles). |
| **US-0048** (isolation evidence) | Ledger reads bounded (`last_n=100` default for QA) to prevent token abuse. |
| **US-0092** (full autonomy) | Ledger supports full autonomy mode with operator override recording. |
| **US-0111** (consumer) | Writes `derivation_decisions[]` to ledger with `decision_type=LEDGER_DERIVATION`. |

### Security boundaries

- Ledger is append-only — no .env reads, no mutation of prior entries
- No cross-run file access (one file per orchestrator run)
- `rationale` field must contain no secrets (no tokens, passwords, API keys)
- `.cursorignore` no-op for `handoffs/sovereign_decisions/` — ledger is git-tracked (auditable decisions)
- US-0085 4-layer audit inherits: `.gitignore` + `.cursorignore` + Cursor rules + operator discipline

### Reason codes summary (11 total)

**`PLAN_FIDELITY_*`** (5 codes):
- `PLAN_FIDELITY_VIOLATION` — strict-mode unapproved deviation (hard stop)
- `PLAN_FIDELITY_OVERRIDE` — operator-approved relaxation (non-blocking, recorded)
- `PLAN_FIDELITY_SCOPE_GATE` — new scope request (hard stop)
- `PLAN_FIDELITY_EXTENSION` — extended-mode scope extension (non-blocking)
- `PLAN_FIDELITY_REORDER` — relaxed/extended AC drop/reorder (non-blocking)

**`LEDGER_*`** (6 codes):
- `LEDGER_FILE_MISSING` — ledger enabled but file missing (QA hard stop)
- `LEDGER_SCHEMA_INVALID` — JSONL line fails schema (fail-closed)
- `LEDGER_APPEND_FAILED` — append/fsync failed (fail-closed)
- `LEDGER_CORRUPT` — file non-UTF-8 or broken JSON (QA hard stop)
- `LEDGER_READ_BOUND` — bounded read truncation (warn only)
- `LEDGER_DISABLED` — `AI_DECISION_LEDGER=0` (informational, zero overhead)

**Informational**: `LEDGER_FILE_EMPTY` (emit at QA only, warn)

### Risks (carry to sprint-plan)

| Risk | Mitigation |
|------|------------|
| **R1** Ledger contention under concurrent writes | One file per run + append-only + fsync; orchestrator enforces single-writer-per-run invariant |
| **R2** Token budget on ledger reads | `summary_digest` + `last_n=100` bounded reads default; 10K lines/run cap |
| **R3** Deviation classification ambiguity | §3 deviation table architecture-locked; `classify_deviation()` single source of truth |
| **R4** Ledger corruption | `schema_check` fail-closed per line; recoverable append on next valid line; `LEDGER_CORRUPT` hard stop requires operator remediation |
| **R5** Sovereign-loop composition stability | `test_us0103_us0070_compose_no_schema_change` regression guard; §3 table frozen; US-0104..US-0110 contract depends on v1 schema |

### Sprint plan input (for `/sprint-plan` phase)

| # | Task seed | AC | Risk | Dependencies |
|---|-----------|-----|------|--------------|
| T-001 | Scratchpad keys declaration (`.cursor/scratchpad.md` + template) | AC-1 | LOW | None |
| T-002 | Ledger directory structure (`handoffs/sovereign_decisions/.gitkeep` + template; `.gitignore`) | AC-2 | LOW | None |
| T-003 | Helper library contract (`scripts/decision_ledger_lib.py` + template byte-parity) | AC-1, AC-2 | HIGH | T-001, T-002 |
| T-004 | Validator CLI contract (`scripts/ledger_validate.py` + template byte-parity) | AC-2, AC-8 | HIGH | T-003 |
| T-005 | Plan-fidelity deviation classification implementation (strict/relaxed/extended branching) | AC-3, AC-4, AC-5 | HIGH | T-003 |
| T-006 | QA cross-check block builder integration (dev_to_qa pipeline) | AC-6, AC-8 | MEDIUM | T-003 |
| T-007 | Runbook operator recipe (`docs/engineering/runbook.md` §AI Decision Ledger + template) | AC-8 | LOW | T-003, T-004 |
| T-008 | Eight `test_us0103_*` contract markers (`tests/auto_command_contract_test.py`) | AC-7 | HIGH | T-003..T-006 |
| T-009 | `SOVEREIGN_LEDGER_PAIRS` parity scope (`check_intake_template_parity.py` + template) | AC-7, AC-8 | MEDIUM | T-003, T-004 |
| T-010 | Harness section `§S103` (`tests/run-tests.ps1` + `tests/run-tests.sh`) | AC-7 | MEDIUM | T-008, T-009 |
| T-011 | Architecture `# US-0103` pre-satisfaction + US-0070 regression guard | AC-8 | LOW | T-003 |

**Total**: 11 tasks (≤12 limit). 8 AC covered surjectively. Tranche order: A (T-001, T-002) → B (T-003) → C (T-004, T-005, T-006) → D (T-007, T-011) → E (T-008, T-009, T-010).

**Multi-AC tasks** (justified by architecture): T-003 (AC-1+AC-2), T-004 (AC-2+AC-8), T-006 (AC-6+AC-8), T-009 (AC-7+AC-8), T-011 (AC-8 pre-satisfied at architecture).

### Evidence refs

- `decisions/DEC-0103.md` (research-phase companion decision — accepted)
- `docs/engineering/architecture.md` (`# US-0103` section appended)
- `docs/engineering/research.md` (`R-0089` resolved Q1–Q7)
- `docs/product/backlog.md` (`## US-0103` — architecture_notes appended)
- `sprints/S0103/tasks.md` (11 task seeds written)
- `handoffs/resume_brief.md` (latest orchestration pointer → sprint-plan)
- `scripts/decision_ledger_lib.py` (+ `template/scripts/` mirror, byte-parity) — research-phase artifact
- `scripts/ledger_validate.py` (+ `template/scripts/` mirror, byte-parity) — research-phase artifact
- `handoffs/po_to_tl.md` (US-0103 discovery handoff — `sovereign-loop-001`)
- `handoffs/intake_evidence/intake-sovereign-20260627-01.json`
- Adjacent stories: **US-0070**, **US-0069**, **US-0048**, **US-0092**, **US-0104..US-0110**, **US-0111**, **US-0045**

### Next

- **`/sprint-plan`** (fresh **tech-lead**) for **`US-0103`** — materialize sprint `S0103` from 11 architecture seeds; lock sprint.md + sprint.json + tasks.md; verify AC-1..AC-8 surjective coverage. Target sprint ID: **S0103**.

### Decision gate

- **None** — architecture satisfied; sprint-plan readiness explicit.

---

## Orchestrated discovery handoff — US-0103 / sovereign-loop-001


--- ##

## Orchestrated discovery handoff — US-0103 / sovereign-loop-001

### Target

- `story_id=US-0103`
- `orchestrator_run_id=sovereign-loop-001`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0103-discovery-20260628T120000Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (per **US-0051**)
- `priority=P0`
- `delivery_mode=standard`
- `sovereign_loop_foundation=true`

### Summary

**`/discovery`** **PASS** — sovereign-loop foundation layer locked: append-only JSONL decision ledger per orchestrator run + plan-fidelity tri-state governance (strict/relaxed/extended) + QA cross-check contract. All overhead gated behind `AI_DECISION_LEDGER=0|1` (default 0, zero overhead). **Compose do NOT amend** US-0070/US-0069/US-0048/US-0092 — US-0103 operates ON TOP of `resolved_phase_plan` / isolation evidence. Foundation for US-0104..US-0110. Status: **OPEN** (US-0045).

### Discovery locks (research inputs)

| Lock | Decision |
|------|----------|
| **L1 Scratchpad keys** | `AI_DECISION_LEDGER=0\|1` (default `0`); `AUTO_PLAN_FIDELITY=strict\|relaxed\|extended` (default `strict`); when ledger `0`, zero overhead — no file writes, no checks. |
| **L2 Ledger path** | `handoffs/sovereign_decisions/<orchestrator_run_id>.jsonl` — one file per orchestrator run. |
| **L3 JSONL schema** | 12 fields: `{ts, orchestrator_run_id, phase_id, role, decision_id (UUIDv4), decision_type, from_artifact, to_artifact, rationale, plan_fidelity, cross_model_reviewed, risk_tier}`. Append-only; fsync semantics. |
| **L4 strict mode** | ANY unapproved deviation → `PLAN_FIDELITY_VIOLATION` hard stop; operator-approved relaxations via scratchpad recorded as `plan_fidelity_override`. |
| **L5 relaxed mode** | AI may drop/reorder ACs with ledger entry; new scope → `PLAN_FIDELITY_SCOPE_GATE` decision gate. |
| **L6 extended mode** | AI may extend scope non-blocking; QA still cross-checks; operator sees extension report at convergence. |
| **L7 QA cross-check** | `/qa` reads ledger → `ledger_findings` in `qa-findings.md`; `LEDGER_FILE_MISSING` fail-closed when `AI_DECISION_LEDGER=1`. |
| **L8 Contract tests** | Eight `test_us0103_*` markers; parity scope `--scope=sovereign-ledger` (`SOVEREIGN_LEDGER_PAIRS`). |
| **L9 Reason codes** | `PLAN_FIDELITY_*` (5 codes) + `LEDGER_*` (6 codes). |
| **L10 Backward compat** | `AI_DECISION_LEDGER=0` (default): zero overhead. US-0070/US-0069/US-0048/US-0092 UNCHANGED. US-0103 composes ON TOP. US-0111 writes `derivation_decisions[]` to ledger. |

### Acceptance pointers (discovery emphasis)

- AC-1: Scratchpad keys `AI_DECISION_LEDGER` + `AUTO_PLAN_FIDELITY` enum literals + defaults.
- AC-2: Ledger JSONL path + 12-field schema + append-only + template parity.
- AC-3: strict mode hard stop on unapproved deviation; ledger `plan_fidelity_override` for operator-approved relaxations.
- AC-4: relaxed mode drops/reorders with ledger entry; new scope → `PLAN_FIDELITY_SCOPE_GATE` stop.
- AC-5: extended mode non-blocking extension report; QA still cross-checks.
- AC-6: QA cross-check → `ledger_findings` in `qa-findings.md`; `LEDGER_FILE_MISSING` fail-closed.
- AC-7: Eight `test_us0103_*` contract markers + parity `--scope=sovereign-ledger`.
- AC-8: Architecture `# US-0103`; runbook recipe; reason codes inventory; template byte-parity.

### Top risks (carry to /research)

- R1: Ledger file contention under concurrent writes — one-file-per-run + append-only with fsync.
- R2: Token budget — ledger reads should be bounded (last N or summary digest for QA).
- R3: Deviation classification ambiguity — need clear deviation table in architecture.
- R4: Ledger corruption → `LEDGER_SCHEMA_INVALID` fail-closed + recoverable append.
- R5: Sovereign-loop composition stability — US-0104..US-0110 depend on US-0103 contract.

### Research asks (extend R-0089)

1. **Q1**: Ledger JSONL exact schema + validator `scripts/ledger_validate.py` CLI.
2. **Q2**: Helper library `scripts/decision_ledger_lib.py` API — append/read/schema_check/summary_digest.
3. **Q3**: Plan-fidelity deviation classification table (decision_type families per mode).
4. **Q4**: QA cross-check `ledger_findings` schema + bounded digest.
5. **Q5**: Contract-test inventory `test_us0103_*` (8 markers) + parity file list.
6. **Q6**: Reason-code enumeration complete inventory.
7. **Q7**: Companion `DEC-xxxx` necessity — new decision or discovery locks suffice?

### Evidence refs

- `docs/product/backlog.md` (`## US-0103` — `discovery_notes` appended)
- `docs/product/vision.md` (Discovery Notes — US-0103 appended)
- `docs/engineering/research.md` (**R-0089** appended)
- `handoffs/intake_evidence/intake-sovereign-20260627-01.json`
- `docs/engineering/state.md` (Discovery checkpoint — this run; orchestrator manages state)
- `handoffs/resume_brief.md` (top pointer → `/research`)
- Adjacent: **US-0070**, **US-0069**, **US-0048**, **US-0092**, **US-0104**, **US-0105**, **US-0107**, **US-0109**, **US-0111**

### Next

- **`/research`** (fresh **tech-lead**) for **`US-0103`** — close **R-0089** Q1–Q7; ledger schema + helper lib + deviation table + contract tests inventory.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

## PO intake handoff — US-0111 / cursor-20260628-US0111-intake

### Target

- `story_id=US-0111`
- `intake_run_id=cursor-20260628-US0111-intake`
- `selected_pack=small-intake-pack` (pre-scoped US-0100 follow-up)
- `priority=P1`
- `decomposition=single_story` (per **US-0051**)
- `next_scheduled_phase=discovery`

### Summary

Operator request: Extend US-0100 version-scoped changelog to support **automatic version changelog generation** from multiple release trigger sources (GitHub webhook, npm publish, git tag push, manual **`/release`**) — currently US-0100 only supports the manual **`/release`** command flow.

### Scope (12 ACs)

1. Trigger adapter registry (`scripts/release_trigger_adapters.py`) with four concrete adapters returning standardized **`TriggerContext`**.
2. GitHub release adapter (webhook payload → tag + previous version via API).
3. npm publish adapter (`package.json` version + registry previous).
4. Git tag push adapter (tag name → semver + tag ordering previous).
5. Manual backward compatibility (`RELEASE_TRIGGER_SOURCE=manual` preserves existing `/release`).
6. `release_changelog_lib.compare_versions()` extended to accept TriggerContext for diff computation.
7. Atomic `[Unreleased] → [semver]` promotion in **`CHANGELOG.md`** with rollback on failure.
8. Per-version notes at **`handoffs/releases/{semver}-release-notes.md`** (atomic write).
9. Sovereign loop US-0103 integration — emit `(semver, previous_semver, timestamp, derivation_decisions[])` event.
10. `RELEASE_TRIGGER_*` fail-closed reason code family.
11. `test_us0111_*` contract tests + `check_intake_template_parity.py --scope=release-trigger` parity.
12. Runbook + **`.cursor/commands/release.md`** + template parity documentation.

### Overlap / duplicate check

- **US-0100** (version-scoped changelog, DONE) — **composes**: US-0111 adds trigger adapters on top; does not amend US-0100 derivation semantics.
- **US-0103** (AI Decision Ledger, OPEN) — **composes**: US-0111 writes derivation decisions to ledger; ledger schema unchanged.
- **US-0054** (publish confirmation, DONE) — **composes unchanged**: trigger-driven generation still respects RELEASE_PUBLISH_MODE.
- **US-0008** (release-all.sh, DONE) — **composes**: may invoke trigger logic when applicable; publish target execution unchanged.
- **US-0040** (release artifacts, DONE) — **composes**: same sprint-scoped notes + queue structures.

### Intake evidence

- `handoffs/intake_evidence/US-0111-intake-20260627.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**
- `asked_topics`: all five small-pack keys covered
- `missing_topics`: (none)
- `assumptions_confirmed`: (none)

### Risks (PO)

- **R1**: GitHub webhook payload shape stability — adapter schema validation + fail-closed.
- **R2**: Atomic [Unreleased] promotion idempotence under concurrent/manually rerun triggers — file-lock + SHA guard.
- **R3**: US-0103 ledger tuple stability (ledger still OPEN) — freeze minimal tuple now.
- **R4**: Semver extraction from heterogeneous tag namespaces — adapter-specific regex + reject-on-ambiguous.

### Research anchor

- Extend **`R-0087`** (US-0100 research) with trigger detection specifics, adapter interface contract, and sovereign-loop ledger tuple shape.

### Status authority

- **OPEN** per **US-0045** until QA/release closure chain.
- **Next**: **`/discovery`** (fresh **PO**) for **`US-0111`**.

### Decision gate

- **None** — intake satisfied; no assumptions, no decomposition split, no decision gate triggered.

---

