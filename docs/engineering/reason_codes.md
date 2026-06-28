# Reason Codes Index

Canonical inventory of fail-closed reason codes used across the its-magic framework.

Each code maps to a deterministic exit code or blocking behavior. Operators read this
document to interpret error messages, triage failures, and decide remediation steps.

---

## US-0103: AI Decision Ledger + Plan Fidelity (DEC-0103 §8)

Sovereign-loop foundation layer. Default-off (`AI_DECISION_LEDGER=0`) → zero overhead.
When enabled, every autonomous AI decision writes to an append-only JSONL ledger.
Plan fidelity tri-state (`strict|relaxed|extended`) governs deviation tolerance.

### PLAN_FIDELITY_* (5 codes)

| Code | Meaning | Blocking |
|------|---------|----------|
| **`PLAN_FIDELITY_VIOLATION`** | Unapproved deviation under `strict` mode (drop/reorder AC) — **hard stop** | **Yes** — operator must approve override or revert |
| **`PLAN_FIDELITY_OVERRIDE`** | Operator-approved relaxation recorded in ledger | **No** — informational, ledger entry appended |
| **`PLAN_FIDELITY_SCOPE_GATE`** | New scope request (add story/feature) under `strict` or `relaxed` — **hard stop** | **Yes** — decision gate requires explicit scope acceptance |
| **`PLAN_FIDELITY_EXTENSION`** | Extended-mode non-blocking scope extension | **No** — recorded in extension report, QA cross-checks |
| **`PLAN_FIDELITY_REORDER`** | Relaxed/extended-mode AC drop/reorder recorded | **No** — ledger entry appended, QA cross-checks |

### LEDGER_* (6 codes)

| Code | Meaning | Blocking |
|------|---------|----------|
| **`LEDGER_FILE_MISSING`** | `AI_DECISION_LEDGER=1` but no ledger file for current orchestrator run — **fail-closed** | **Yes** — QA hard stop, operator must create or disable |
| **`LEDGER_SCHEMA_INVALID`** | JSONL line fails 12-field schema v1 validation — **fail-closed** | **Yes** — QA hard stop, operator must remediate ledger |
| **`LEDGER_APPEND_FAILED`** | Append/fsync failed (permission error, I/O error, disk full) | **Yes** — execute phase cannot continue without ledger write |
| **`LEDGER_CORRUPT`** | Whole file fails UTF-8 decode or JSON parse — **fail-closed** | **Yes** — operator must manually repair or truncate ledger |
| **`LEDGER_READ_BOUND`** | Bounded read truncated (`last_n=100` for QA) | **No** — warning only, digest still emitted |
| **`LEDGER_DISABLED`** | `AI_DECISION_LEDGER=0` (default) — informational, zero overhead | **No** — no-op, no ledger reads/writes |

**Informational (not fail)**: `LEDGER_FILE_EMPTY` when ledger file exists but contains
zero parseable lines (emit at QA only, warn — not a hard stop unless `LEDGER_FILE_MISSING`
logic also triggers).

### Exit-code mapping

| Code | Exit code (CLI) |
|------|-----------------|
| `PLAN_FIDELITY_VIOLATION`, `PLAN_FIDELITY_SCOPE_GATE`, `LEDGER_FILE_MISSING`, `LEDGER_SCHEMA_INVALID`, `LEDGER_CORRUPT`, `LEDGER_APPEND_FAILED` | `1` (fail-closed) |
| `PLAN_FIDELITY_OVERRIDE`, `PLAN_FIDELITY_EXTENSION`, `PLAN_FIDELITY_REORDER`, `LEDGER_READ_BOUND`, `LEDGER_DISABLED` | `0` (success / informational) |

### Usage in CLI tools

- **`scripts/decision_ledger_lib.py`**: `append_entry()` returns `AppendResult(success, reason_code, reason_message)`.
- **`scripts/ledger_validate.py`**: `--file <path>` validates schema, emits `LEDGER_SCHEMA_INVALID` on first invalid line, `LEDGER_FILE_MISSING` if file absent.
- **`tests/us0103_contract_test.py`**: 8 contract tests assert enum cardinalities, default-off behavior, schema v1 invariants, tri-state deviation classifier, QA cross-check block shape, backward composition with US-0070/US-0069/US-0048.

### Operational remediation

| Reason code | Operator action |
|-------------|-----------------|
| `PLAN_FIDELITY_VIOLATION` | Review `handoffs/sovereign_decisions/<run>.jsonl` last entry; if deviation justified, set `AUTO_PLAN_FIDELITY=relaxed` in `.cursor/scratchpad.local.md` and re-run `/execute`; otherwise revert AC changes |
| `PLAN_FIDELITY_SCOPE_GATE` | If scope-add is intentional, switch to `AUTO_PLAN_FIDELITY=extended` and document in `sprints/Sxxxx/extension-report.md`; otherwise drop new scope |
| `LEDGER_FILE_MISSING` | Ensure `handoffs/sovereign_decisions/` directory exists (create `.gitkeep` if missing); or set `AI_DECISION_LEDGER=0` to disable |
| `LEDGER_SCHEMA_INVALID` | Open ledger file, locate invalid line (validator prints line number), fix JSON syntax or missing field; if unrecoverable, truncate file to last valid line |
| `LEDGER_CORRUPT` | Ledger file contains non-UTF-8 bytes or malformed JSON throughout — manual repair required; consider `git restore` from prior commit or truncate to known-good prefix |
| `LEDGER_APPEND_FAILED` | Check disk space (`df -h`), file permissions (`ls -la handoffs/sovereign_decisions/`), and filesystem mount status; retry after remediation |
| `LEDGER_READ_BOUND` | No action required — QA digest still emitted; full file read available via `read_entries(ledger_path, last_n=None)` in library call |
| `LEDGER_DISABLED` | No action required — zero overhead when `AI_DECISION_LEDGER=0`; opt-in via `.cursor/scratchpad.local.md` if ledger auditing desired |

### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0103` §8 (reason code inventory)
- **Decision record**: `decisions/DEC-0103.md` §8
- **Library**: `scripts/decision_ledger_lib.py` — `ReasonCode` enum (11 values total)
- **Validator**: `scripts/ledger_validate.py` — CLI exit codes map to reason codes
- **Contract tests**: `tests/us0103_contract_test.py` — `test_us0103_reason_code_inventory` asserts 5 `PLAN_FIDELITY_*` + 6 `LEDGER_*` parity

---

## US-0110: Goal-Based Convergence Loops (DEC-0110 §10)

Sovereign-loop terminal predicate. Default-off (`SOVEREIGN_GOAL_MODE=phase_driven`) → zero
overhead. When `goal_convergence`, `evaluate_convergence` reads composed surfaces only.

| Code | blocked_by? | Conjunct / trigger |
|------|-------------|-------------------|
| **`CONVERGENCE_OPEN_STORIES_REMAIN`** | yes | backlog clear — OPEN stories remain in `docs/product/backlog.md` |
| **`CONVERGENCE_DEFERRALS_PENDING`** | yes | zero deferrals — non-empty `handoffs/sovereign_deferrals.jsonl` |
| **`CONVERGENCE_CROSS_REVIEWER_OPEN`** | yes | critic resolved — open blocking cross-reviewer finding |
| **`CONVERGENCE_SMOKE_PROBE_FAIL`** | yes | smoke green — `tests/report.md` and/or active sprint UAT smoke step not PASS |
| **`CONVERGENCE_LEDGER_EXTENSIONS_UNAPPROVED`** | yes | ledger clean — unapproved extension/scope-gate without override |
| **`SOVEREIGN_GOAL_TIMEOUT`** | yes | iteration cap exhausted (`SOVEREIGN_GOAL_TIMEOUT_MAX`) |
| **`SOVEREIGN_GOAL_MODE_INVALID`** | yes | invalid `SOVEREIGN_GOAL_MODE` scratchpad enum |
| **`SOVEREIGN_GOAL_MISSING`** | no (warn) | empty goal under `phase_driven` — informational only |
| **`SOVEREIGN_GOAL_DERIVE_FAILED`** | yes | vision auto-derive failed (missing/empty vision) |
| **`CONVERGENCE_EVAL_FAILED`** | yes | evaluator internal error |

### Operational remediation

| Reason code | Operator action |
|-------------|-----------------|
| `CONVERGENCE_OPEN_STORIES_REMAIN` | Complete or defer remaining OPEN stories; re-run drain loop |
| `CONVERGENCE_DEFERRALS_PENDING` | Resolve deferrals in register or drain-generate (US-0107) |
| `CONVERGENCE_CROSS_REVIEWER_OPEN` | Resolve critic findings; re-run `/qa` |
| `CONVERGENCE_SMOKE_PROBE_FAIL` | Fix failing tests/UAT smoke; refresh `tests/report.md` |
| `CONVERGENCE_LEDGER_EXTENSIONS_UNAPPROVED` | Add `PLAN_FIDELITY_OVERRIDE` or revert scope changes |
| `SOVEREIGN_GOAL_TIMEOUT` | Read `handoffs/sovereign_partial_delivery.md`; adjust goal or cap |
| `SOVEREIGN_GOAL_MODE_INVALID` | Set `SOVEREIGN_GOAL_MODE=phase_driven` or `goal_convergence` |
| `SOVEREIGN_GOAL_DERIVE_FAILED` | Set explicit `SOVEREIGN_GOAL` or populate `docs/product/vision.md` |
| `CONVERGENCE_EVAL_FAILED` | Check evaluator logs; re-run with `--self-test` |

## US-0104: Cross-Model Adversarial Critic (DEC-0104 §11)

Default-off cross-model review (`CROSS_MODEL_REVIEW=0`) → zero overhead. When enabled,
`/auto` spawns `/sovereign-critic` after producer phases; findings append to
`handoffs/sovereign_critic_findings.jsonl`.

| Code | Blocking? | Surface |
|------|-----------|---------|
| **`CROSS_MODEL_REVIEW_DISABLED`** | no (info) | scratchpad gate off |
| **`CROSS_MODEL_CRITIC_SPAWN_FAILED`** | yes | orchestrator hook |
| **`CROSS_MODEL_MODEL_COLLISION`** | no → degraded | same slug resolved |
| **`CROSS_MODEL_ANTISLOP_FAIL`** | yes (rework) | score below threshold |
| **`CROSS_MODEL_REWORK_CAP_EXHAUSTED`** | yes (gate) | rework max hit |
| **`CROSS_MODEL_FINDINGS_INVALID`** | yes | schema validation |
| **`CROSS_MODEL_RECONCILE_FAILED`** | yes | jury merge error |
| **`CROSS_MODEL_DEGRADED_MODE`** | no (info) | single-model fallback |
| **`CROSS_MODEL_CRITIC_MODEL_UNAVAILABLE`** | yes → degraded | catalog miss |
| **`ISOLATION_EVIDENCE_MODEL_ID_MISSING`** | yes | critic enabled, evidence incomplete |

### Operational remediation

| Reason code | Operator action |
|-------------|-----------------|
| `CROSS_MODEL_REVIEW_DISABLED` | Set `CROSS_MODEL_REVIEW=1` to enable critic |
| `CROSS_MODEL_CRITIC_SPAWN_FAILED` | Retry spawn; check Task tool availability |
| `CROSS_MODEL_ANTISLOP_FAIL` | Address critic findings; producer re-spawn (bounded) |
| `CROSS_MODEL_REWORK_CAP_EXHAUSTED` | Waive findings or abort; adjust `CROSS_MODEL_REWORK_MAX` |
| `CROSS_MODEL_FINDINGS_INVALID` | Fix JSONL schema; run `sovereign_critic_validate.py --enforce` |
| `CROSS_MODEL_DEGRADED_MODE` | Informational — single-model multi-lens fallback active |
| `ISOLATION_EVIDENCE_MODEL_ID_MISSING` | Add `model_id` to producer and critic isolation rows |

### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0110`
- **Decision record**: `decisions/DEC-0110.md` §10
- **Library**: `scripts/sovereign_convergence_lib.py`
- **Validator**: `scripts/sovereign_convergence_validate.py`
- **Contract tests**: `tests/us0110_contract_test.py`

---

## US-0105 — Sovereign Memory (`SOVEREIGN_MEMORY_*`)

Default-off institutional memory (`SOVEREIGN_MEMORY=0`) → zero overhead. When enabled,
bounded JSONL learnings inject into phase spawns via `sovereign_memory_lib.py`.
Normative: **`decisions/DEC-0105.md`** §9; architecture **`# US-0105`**.

### SOVEREIGN_MEMORY_* (8 codes)

| Reason code | Meaning | Blocking? |
|-------------|---------|-----------|
| **`SOVEREIGN_MEMORY_DISABLED`** | `SOVEREIGN_MEMORY=0` (default) — informational, zero overhead | **No** |
| **`SOVEREIGN_MEMORY_SCHEMA_INVALID`** | JSONL line fails v1 family schema — **fail-closed** | **Yes** |
| **`SOVEREIGN_MEMORY_APPEND_FAILED`** | Append/fsync failed (permission / I/O) | **Yes** |
| **`SOVEREIGN_MEMORY_DECISION_DUPLICATE`** | `decision_key` already present — skip append | **No** (skip) |
| **`SOVEREIGN_MEMORY_SECRET_DETECTED`** | Free-text field matches secret heuristics — **fail-closed** | **Yes** |
| **`SOVEREIGN_MEMORY_ARCHIVE_REQUIRED`** | JSONL rollover I/O failure — block append | **Yes** |
| **`SOVEREIGN_MEMORY_READ_BOUND`** | Tail read truncated during digest assembly | **No** (warning) |
| **`SOVEREIGN_MEMORY_PROMOTION_SKIPPED`** | Ledger off or promotion filter empty | **No** (info) |

### Operator remediation

| Reason code | Operator action |
|-------------|-----------------|
| `SOVEREIGN_MEMORY_DISABLED` | Set `SOVEREIGN_MEMORY=1` to enable memory |
| `SOVEREIGN_MEMORY_SCHEMA_INVALID` | Fix JSONL line; run `sovereign_memory_validate.py --enforce` |
| `SOVEREIGN_MEMORY_APPEND_FAILED` | Check disk space and file permissions |
| `SOVEREIGN_MEMORY_DECISION_DUPLICATE` | No action — dedup skip is expected |
| `SOVEREIGN_MEMORY_SECRET_DETECTED` | Remove secret-shaped literals from entry text |
| `SOVEREIGN_MEMORY_ARCHIVE_REQUIRED` | Remediate archive I/O; check `sovereign-memory-archive/` permissions |
| `SOVEREIGN_MEMORY_READ_BOUND` | No action — digest still emitted within char cap |
| `SOVEREIGN_MEMORY_PROMOTION_SKIPPED` | Enable `AI_DECISION_LEDGER=1` or adjust promotion filter |

### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0105`
- **Decision record**: `decisions/DEC-0105.md` §9
- **Library**: `scripts/sovereign_memory_lib.py`
- **Validator**: `scripts/sovereign_memory_validate.py`
- **Contract tests**: `tests/us0105_contract_test.py`

---

## US-0106 — Sovereign Role-Behavior Manifest (`SOVEREIGN_ROLE_*` / `ROLE_REVIEW_*`)

Default-off per-role objective + inter-role review obligations (`SOVEREIGN_ROLE_MANIFEST=0`) → zero
overhead. When enabled, orchestrator reads `.cursor/sovereign-role-manifest.yaml`, injects role-specific
objective blocks into subagent spawn context, and dispatches supplementary cross-role reviews after
phase completion (spawn-only per BUG-0006; distinct boundary_token `role_review`).

Normative: **`decisions/DEC-0106.md`** §2; architecture **`# US-0106`**.

### SOVEREIGN_ROLE_* (6 codes)

| Reason code | Meaning | Blocking? |
|-------------|---------|-----------|
| **`SOVEREIGN_ROLE_MANIFEST_DISABLED`** | `SOVEREIGN_ROLE_MANIFEST=0` (default) — informational, zero overhead | **No** |
| **`SOVEREIGN_ROLE_MANIFEST_SCHEMA_INVALID`** | Manifest YAML parse or schema validation failed — **fail-closed** | **Yes** |
| **`SOVEREIGN_ROLE_UNKNOWN_ROLE`** | Manifest references `role_id` not in canonical set (`po`, `tech-lead`, `dev`, `qa`, `release`, `curator`) — **fail-closed** | **Yes** |
| **`SOVEREIGN_ROLE_UNKNOWN_PHASE`** | Manifest references `trigger_phase` not in canonical phase set — **fail-closed** | **Yes** |
| **`SOVEREIGN_ROLE_SECRET_DETECTED`** | Manifest `objective_function` contains secret-shaped literal (API key, token, password) — **fail-closed** | **Yes** |
| **`SOVEREIGN_ROLE_OBJECTIVE_OVERFLOW`** | `objective_function` exceeds 1024 chars at file load — **fail-closed** | **Yes** |

### ROLE_REVIEW_* (5 codes)

| Reason code | Meaning | Blocking? |
|-------------|---------|-----------|
| **`ROLE_REVIEW_DISPATCH_FAILED`** | Append to `handoffs/sovereign_role_reviews.jsonl` failed (I/O, permissions) | **Yes** |
| **`ROLE_REVIEW_SPAWN_FAILED`** | Task tool spawn error for supplementary review subagent | **Yes** |
| **`ROLE_REVIEW_BLOCKED`** | Supplementary review verdict `fail` with `blocking=true`; producer phase cannot proceed | **Yes** (operator decision gate) |
| **`ROLE_REVIEW_DEFERRAL_FAILED`** | US-0107 deferral append failed during review escalation | **No** (fail-open log) |
| **`ROLE_REVIEW_REWORK_CAP`** | Rework cap exhausted (`SOVEREIGN_ROLE_REVIEW_REWORK_MAX`); operator decision gate required | **Yes** (operator decision gate) |

### Operational remediation

| Reason code | Operator action |
|-------------|-----------------|
| `SOVEREIGN_ROLE_MANIFEST_DISABLED` | Set `SOVEREIGN_ROLE_MANIFEST=1` to enable role manifest |
| `SOVEREIGN_ROLE_MANIFEST_SCHEMA_INVALID` | Re-create manifest from `.cursor/sovereign-role-manifest.yaml.example`; re-run `scripts/sovereign_role_manifest_validate.py --file .cursor/sovereign-role-manifest.yaml` |
| `SOVEREIGN_ROLE_UNKNOWN_ROLE` | Edit manifest; replace `role_id` with canonical role (`po`, `tech-lead`, `dev`, `qa`, `release`, `curator`) |
| `SOVEREIGN_ROLE_UNKNOWN_PHASE` | Edit manifest; replace `trigger_phase` with canonical phase_id (see `/architecture` canonical phases) |
| `SOVEREIGN_ROLE_SECRET_DETECTED` | Replace secret-shaped literal in `objective_function` with placeholder; never commit real credentials |
| `SOVEREIGN_ROLE_OBJECTIVE_OVERFLOW` | Truncate or split `objective_function` (file max 1024 chars; validator hard caps) |
| `ROLE_REVIEW_DISPATCH_FAILED` | Retry dispatch; check file permissions on `handoffs/` directory |
| `ROLE_REVIEW_SPAWN_FAILED` | Retry spawn; if persistent, check Task tool availability or disable `SOVEREIGN_ROLE_MANIFEST` |
| `ROLE_REVIEW_BLOCKED` | Operator decision gate: waive review (set `blocking=false`), rework producer output, or disable manifest |
| `ROLE_REVIEW_DEFERRAL_FAILED` | Check `handoffs/sovereign_deferrals.jsonl` permissions; fail-open logged but not blocking |
| `ROLE_REVIEW_REWORK_CAP` | Operator decision: waive review, escalate to human reviewer, or disable manifest |

### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0106`
- **Decision record**: `decisions/DEC-0106.md`
- **Library**: `scripts/sovereign_role_manifest_lib.py` — `ReasonCode` enum (11 values total)
- **Validator**: `scripts/sovereign_role_manifest_validate.py` — CLI exit codes map to reason codes
- **Contract tests**: `tests/us0106_contract_test.py` — 8 tests + 2 compose guards

---

## US-0107 — Sovereign Loop Mode (`SOVEREIGN_*` / `DEPLOY_DEFERRED`)

Default-off sovereign loop orchestration (`AUTO_SOVEREIGN=0`) → zero overhead. When enabled
with `SOVEREIGN_GOAL_MODE=goal_convergence`, manages deferral register, drain-generate,
notification dispatch, and convergence hooks via `sovereign_loop_lib.py`.
Normative: **`decisions/DEC-0107.md`** §9; architecture **`# US-0107`**.

### SOVEREIGN_LOOP_* / SOVEREIGN_DEFERRAL_* / SOVEREIGN_DRAIN_* / SOVEREIGN_NOTIFY_* (12 codes)

| Reason code | Meaning | Blocking? |
|-------------|---------|-----------|
| **`SOVEREIGN_LOOP_DISABLED`** | `AUTO_SOVEREIGN=0` (default) — informational, zero overhead | **No** |
| **`SOVEREIGN_LOOP_GOAL_MODE_REQUIRED`** | `AUTO_SOVEREIGN=1` without `SOVEREIGN_GOAL_MODE=goal_convergence` — **fail-closed** | **Yes** |
| **`SOVEREIGN_DEFERRAL_CAP_EXCEEDED`** | Open deferral rows ≥ `AUTO_SOVEREIGN_DEFERRAL_MAX` — append rejected / sovereign terminal | **Yes** |
| **`SOVEREIGN_DEFERRAL_SCHEMA_INVALID`** | Deferral JSONL line fails v1 schema — **fail-closed** | **Yes** |
| **`SOVEREIGN_DEFERRAL_APPEND_FAILED`** | Deferral append/fsync failed (permission / I/O) | **Yes** |
| **`SOVEREIGN_DRAIN_GENERATE_CAP`** | Drain-generate iterations exhausted for run — sovereign terminal | **Yes** |
| **`SOVEREIGN_DRAIN_GENERATE_BLOCKED`** | Deferral policy or gate blocks drain-generate spawn | **Yes** |
| **`SOVEREIGN_NOTIFY_DISPATCH_FAILED`** | Notification adapter error — logged, loop continues (fail-open) | **No** (fail-open log) |
| **`SOVEREIGN_NOTIFY_TARGET_INVALID`** | Unknown notify target or email v1 deferred | **No** |
| **`SOVEREIGN_NOTIFY_CONFIG_MISSING`** | Notify target on but topic/URL absent — skip dispatch | **No** (skip) |
| **`SOVEREIGN_LOOP_ADVANCE_BLOCKED`** | Deferral policy `stop` or `resolve_first` blocks advance | **Yes** |
| **`DEPLOY_DEFERRED`** | Deploy smoke cap exhaustion — deferral row for **US-0109** writer | **No** (deferral row) |

### Operator remediation

| Reason code | Operator action |
|-------------|-----------------|
| `SOVEREIGN_LOOP_DISABLED` | Set `AUTO_SOVEREIGN=1` and `SOVEREIGN_GOAL_MODE=goal_convergence` to enable |
| `SOVEREIGN_LOOP_GOAL_MODE_REQUIRED` | Set both `AUTO_SOVEREIGN=1` and `SOVEREIGN_GOAL_MODE=goal_convergence` in scratchpad.local |
| `SOVEREIGN_DEFERRAL_CAP_EXCEEDED` | Resolve open deferrals or raise `AUTO_SOVEREIGN_DEFERRAL_MAX` |
| `SOVEREIGN_DEFERRAL_SCHEMA_INVALID` | Fix JSONL line; run `sovereign_loop_validate.py --enforce` |
| `SOVEREIGN_DEFERRAL_APPEND_FAILED` | Check disk space and file permissions on `handoffs/sovereign_deferrals.jsonl` |
| `SOVEREIGN_DRAIN_GENERATE_CAP` | Review drain-generate proposals; adjust goal or raise cap; read partial-delivery report |
| `SOVEREIGN_DRAIN_GENERATE_BLOCKED` | Resolve open deferrals or change `AUTO_SOVEREIGN_DEFERRAL_POLICY` |
| `SOVEREIGN_NOTIFY_DISPATCH_FAILED` | Check ntfy/hook connectivity; notification failure does not block loop |
| `SOVEREIGN_NOTIFY_TARGET_INVALID` | Set valid `SOVEREIGN_NOTIFY_TARGET`; email deferred to v1.1 |
| `SOVEREIGN_NOTIFY_CONFIG_MISSING` | Set topic/URL in scratchpad.local or set `SOVEREIGN_NOTIFY_TARGET=off` |
| `SOVEREIGN_LOOP_ADVANCE_BLOCKED` | Resolve deferrals via `resolve_deferral` or change policy to `skip` |
| `DEPLOY_DEFERRED` | **US-0109** scope — resolve deploy deferral or retry smoke |

### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0107`
- **Decision record**: `decisions/DEC-0107.md` §9
- **Library**: `scripts/sovereign_loop_lib.py`
- **Validator**: `scripts/sovereign_loop_validate.py`
- **Contract tests**: `tests/us0107_contract_test.py`

---

## Other stories

Reason codes for other stories live in their respective architecture sections:

- **US-0018** (installer upgrade): `UPGRADE_FILE_CLASSIFICATION_*`, `UPGRADE_VERSION_TRACKING_*`
- **US-0063** (runbook bootstrap): `RUNBOOK_BOOTSTRAP_ERROR`
- **US-0070** (phase selection): `PHASE_POLICY_CONFLICT`, `START_FROM_PHASE_PLAN_EMPTY_INTERSECTION`
- **US-0069** (phase role): `PHASE_ROLE_CAPABILITY_MISSING`
- **US-0048** (isolation): `PHASE_CONTEXT_ISOLATION_VIOLATION`
- **US-0087** (bug queue): `AUTO_BUG_QUEUE_EMPTY`, `AUTO_BUG_TARGET_*`
- **US-0086** (remote automation): `REMOTE_TARGET_*`, `REMOTE_AUTOMATION_MODE_OFF`
- **US-0092** (full autonomy): `AUTO_FLOW_MODE_CONFLICT`, `AUTO_OUTER_DRIVER_*`
- **US-0096** (delivery modes): `DELIVERY_MODE_UNKNOWN`, `LEAN_MEMORY_*`

See `docs/engineering/architecture.md` for normative definitions.
