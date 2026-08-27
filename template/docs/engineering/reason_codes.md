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

Note on `CONVERGENCE_SMOKE_PROBE_FAIL`: reserved for real smoke step failures and US-0109 deploy smoke; surrogate path uses `CONVERGENCE_SMOKE_SURROGATE_MISSING`. Description of `CONVERGENCE_SMOKE_PROBE_FAIL` unchanged.

## US-0127: Convergence critic conjunct hygiene (DEC-0110 §10 / DEC-0104 §11)

Blocking-only conjunct-3 plus operator hygiene for informational critic rows.
`CONVERGENCE_CROSS_REVIEWER_OPEN` now requires `blocking=true` (description
amendment only; compose amendment to description only; code semantics already
require `blocking=true` per DEC-0110 §10). No US-0110 reason-code renumbering.

| Code | Exit | Meaning |
|------|------|---------|
| **`HYGIENE_RESOLVE_CONFIRM_REQUIRED`** | 2 | `--resolve-nonblocking-for-run` without `--confirm` (and not `--dry-run`) |
| **`HYGIENE_RESOLVE_NO_CANDIDATES`** | 0 (info) | No matching open non-blocking rows for the scoped run/phase |
| **`HYGIENE_RESOLVE_PARTIAL`** | 3 | Some candidates resolved, some failed |
| **`HYGIENE_RESOLVE_FAILED`** | 4 | Resolve attempted and none succeeded |
| **`HYGIENE_REPORT_EMPTY`** | 0 (info) | `--report` found no open critic findings |
| **`HYGIENE_RESOLVE_PHASE_SCOPE_REQUIRED`** | 2 | Resolve without `--all-phases` and without `--phase-id` |
| **`SOVEREIGN_CRITIC_AUTORESOLVE_FAILED`** | info | Auto-resolve hook failed; PASS verdict stands |

## US-0128: Convergence smoke surrogate (DEC-0110 §10 smoke-green)

Additive PASS path inside the existing `smoke_green` conjunct for ultra_lean/docs/contract-test
slices. Five-conjunct name/order/`ConjunctResult` shape unchanged. `CONVERGENCE_SMOKE_PROBE_FAIL`
remains the US-0110 code for real smoke step failures and US-0109 deploy smoke.

| Code | blocked_by? | Meaning |
|------|-------------|---------|
| **`CONVERGENCE_SMOKE_SURROGATE_MISSING`** | yes | smoke green — surrogate prerequisites unmet for waived-probe slice (no smoke step + incomplete waivers or harness red) |

### Operational remediation

| Reason code | Operator action |
|-------------|-----------------|
| `CONVERGENCE_SMOKE_SURROGATE_MISSING` | Emit `convergence_smoke` in `/qa`/`/verify-work`; ensure 6 `waived_probes` with `UAT_PROBE_FORBIDDEN`; fix failing contract tests |

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

## US-0109 — Self-Healing Deploy Loop (`DEPLOY_HEALING_*` / `DEPLOY_SMOKE_*`)

Default-off post-deploy smoke probe + bounded retry loop (`AUTO_SOVEREIGN_SELF_HEALING_DEPLOY=0`) → zero
overhead, byte-identical US-0054 publish path. When enabled, after `[RELEASE_PUBLISH_OK]`, a two-stage
smoke probe (health HTTP GET + acceptance smoke runner) validates the deployed artifact. On probe FAIL,
publish PASS path re-entered idempotently up to `AUTO_SOVEREIGN_DEPLOY_RETRY_MAX`. After retry-cap
exhaustion, US-0107 `append_deferral(work_item_kind=deploy)` writes DEPLOY_DEFERRED row.
Normative: **`decisions/DEC-0109.md`** §7; architecture **`# US-0109`**.

### DEPLOY_HEALING_* / DEPLOY_SMOKE_* (8 codes)

| Reason code | Meaning | Blocking? |
|-------------|---------|-----------|
| **`DEPLOY_HEALING_DISABLED`** | `AUTO_SOVEREIGN_SELF_HEALING_DEPLOY=0` (default) — informational, zero overhead | **No** |
| **`DEPLOY_HEALING_SMOKE_HEALTH_FAIL`** | Health HTTP GET non-2xx or connection refused | **Yes** (retry or defer) |
| **`DEPLOY_HEALING_SMOKE_ACCEPTANCE_FAIL`** | Acceptance smoke pytest runner non-zero exit | **Yes** (retry or defer) |
| **`DEPLOY_HEALING_RETRY_ATTEMPT`** | Per-attempt log entry during retry loop (`retry_count` tag) | **No** (info) |
| **`DEPLOY_HEALING_RETRY_CAP_EXHAUSTED`** | `AUTO_SOVEREIGN_DEPLOY_RETRY_MAX` reached — proceed to DEPLOY_DEFERRED | **Yes** (to defer) |
| **`DEPLOY_HEALING_DEFERRED`** | DEPLOY_DEFERRED tuple written via US-0107 `append_deferral` | **No** (deferral row) |
| **`DEPLOY_HEALING_PROBE_TARGET_MISSING`** | `AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT` unresolvable from env — **fail-closed** | **Yes** (fail-closed) |
| **`DEPLOY_HEALING_TIMEOUT`** | Total bounded timeout exceeded (smoke HTTP timeout or pytest runner timeout) | **Yes** (blocking) |

`DEPLOY_DEFERRED` already reserved in US-0107 runbook — confirmed reuse.

### Operator remediation

| Reason code | Operator action |
|-------------|-----------------|
| `DEPLOY_HEALING_DISABLED` | Set `AUTO_SOVEREIGN_SELF_HEALING_DEPLOY=1` to enable self-healing deploy |
| `DEPLOY_HEALING_SMOKE_HEALTH_FAIL` | Check target health endpoint reachability; verify `AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT` env key resolves; run `self_healing_deploy_validate.py --self-test` |
| `DEPLOY_HEALING_SMOKE_ACCEPTANCE_FAIL` | Inspect smoke test logs in `SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH`; fix failing acceptance tests |
| `DEPLOY_HEALING_RETRY_ATTEMPT` | Informational per-attempt log; no action needed unless cap exhausted |
| `DEPLOY_HEALING_RETRY_CAP_EXHAUSTED` | Review `sprints/Sxxxx/summary.md` smoke probe output; raise `AUTO_SOVEREIGN_DEPLOY_RETRY_MAX` if transient; or resolve root cause |
| `DEPLOY_HEALING_DEFERRED` | Resolve DEPLOY_DEFERRED row in `handoffs/sovereign_deferrals.jsonl`; re-run `/release` after fix |
| `DEPLOY_HEALING_PROBE_TARGET_MISSING` | Set `AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT` to a valid env key name in scratchpad.local; ensure env var contains URL |
| `DEPLOY_HEALING_TIMEOUT` | Raise `AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC` for slow targets; investigate startup latency |

### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0109`
- **Decision record**: `decisions/DEC-0109.md` §7
- **Library**: `scripts/self_healing_deploy_lib.py` — `ReasonCode` enum (8 values)
- **Validator**: `scripts/self_healing_deploy_validate.py` — CLI exit codes map to reason codes
- **Contract tests**: `tests/us0109_contract_test.py` — 8 core markers + 2 compose guards

## US-0111 — Release trigger adapter family (trigger source dispatch, atomic version-file promotion)

Dispatch release flow by trigger source (GitHub webhook, npm publish, Git tag push, manual /release). Default source is `RELEASE_TRIGGER_SOURCE=manual` (zero behavior change vs pre-US-0111 /release path — byte-identical). Compose with existing release pipeline (US-0100); reuses `release_changelog_lib.compare_versions()` and `promote_unreleased()` without modification.

### RELEASE_TRIGGER_* (9 codes)

| Code | Meaning | Blocking |
|------|---------|----------|
| **`RELEASE_TRIGGER_ADAPTER_FAILED`** | Trigger adapter dispatch failed (unknown source value) — unknown adapter name in registry. | **Yes** |
| **`RELEASE_TRIGGER_TAG_MISSING`** | Trigger source is git/github but no semantic version tag was found in the repository. | **Yes** |
| **`RELEASE_TRIGGER_PREVIOUS_MISSING`** | Cannot resolve previous version tag (required for diff-based changelog derivation). | **Yes** |
| **`RELEASE_TRIGGER_PACKAGE_JSON_MISSING`** | npm trigger source selected but `package.json` is absent from repository root. | **Yes** |
| **`RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED`** | Atomic rename (mv) of temporary version file to production path failed. | **Yes** |
| **`RELEASE_TRIGGER_NOTES_WRITE_FAILED`** | Per-version release notes write to `handoffs/releases/vX.Y.Z/release-notes.md` failed. | **Yes** |
| **`RELEASE_TRIGGER_EVENT_EMIT_FAILED`** | Failed to emit canonical `version_derivation` event to sovereign decision ledger (US-0107). | **Yes** |
| **`RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED`** | Semver comparison between current and previous version failed (invalid format or equality check error). | **Yes** |
| **`RELEASE_TRIGGER_SOURCE_INVALID`** | `RELEASE_TRIGGER_SOURCE` in scratchpad is neither `auto` nor one of the four registered adapters (`github_webhook`, `npm_publish`, `git_tag_push`, `manual_release`). | **Yes** |

### Operator remediation

| Reason code | Operator action |
|-------------|------------------|
| `RELEASE_TRIGGER_ADAPTER_FAILED` | Verify scratchpad `RELEASE_TRIGGER_SOURCE`; must be one of: `auto`, `github_webhook`, `npm_publish`, `git_tag_push`, `manual_release`. If `auto`, ensure only one trigger artifact exists in environment. |
| `RELEASE_TRIGGER_TAG_MISSING` | Tag current commit with a semantic version (`git tag vX.Y.Z && git push --tags`). |
| `RELEASE_TRIGGER_PREVIOUS_MISSING` | For initial releases, explicitly set `RELEASE_TRIGGER_PREVIOUS_VERSION=` in scratchpad. For subsequent releases, ensure at least one prior version tag exists in git history. |
| `RELEASE_TRIGGER_PACKAGE_JSON_MISSING` | Restore `package.json` to repository root (npm trigger requires it for version discovery). |
| `RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED` | Check filesystem permissions on target directory; verify no concurrent hold on the file; retry after resolving lock. |
| `RELEASE_TRIGGER_NOTES_WRITE_FAILED` | Check disk quota and directory permissions for `handoffs/releases/`; ensure no concurrent hold on target file. |
| `RELEASE_TRIGGER_EVENT_EMIT_FAILED` | Check ledger file permissions; ensure `handoffs/sovereign_decisions.jsonl` is writable; verify ledger schema compatibility. |
| `RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED` | Verify both current and previous versions are valid semver (major.minor.patch); resolve any non-numeric suffixes or malformed tags. |
| `RELEASE_TRIGGER_SOURCE_INVALID` | Update scratchpad `RELEASE_TRIGGER_SOURCE` to `auto` or an explicit adapter name. Run `scripts/release_trigger_adapters.py --list` to see registered source names. |

### Exit-code mapping

All 9 codes map to exit code `1` (fail-closed) — execution halts and requires operator intervention before proceeding.

### Usage in CLI tools

- **`scripts/release_trigger_adapters.py`**: Adapter registry + dispatch logic; emits `RELEASE_TRIGGER_ADAPTER_FAILED` / `RELEASE_TRIGGER_SOURCE_INVALID` on invalid source.
- **`scripts/release_changelog_lib.py`**: Consumes `TriggerContext.version` and `TriggerContext.previous_version`; emits `RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED` / `RELEASE_TRIGGER_PREVIOUS_MISSING` when version diff fails.
- **`scripts/release_promote_atomic.py`**: Orchestrates atomic promotion; emits `RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED` on rename failure.
- **`scripts/release_notes_emit.py`**: Writes per-version notes; emits `RELEASE_TRIGGER_NOTES_WRITE_FAILED` on I/O error.
- **Ledger integration**: Emits `version_derivation` decision type via `append_decision()` in `scripts/decision_ledger_lib.py`; emits `RELEASE_TRIGGER_EVENT_EMIT_FAILED` on ledger write failure.

### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0111` (trigger adapter family + atomic version-file promotion)
- **Decision record**: `decisions/DEC-0111.md` (release trigger dispatch design)
- **Library**: `scripts/release_trigger_adapters.py` — adapter registry + `TriggerContext` dataclass
- **Contract tests**: `tests/us0111_contract_test.py` — adapter dispatch, previous-version resolution, atomic promotion, reason-code inventory

## US-0129 — Architecture hot-surface rollover linkage guard

Fail-closed pre/post wrap of `python scripts/enforce-triad-hot-surface.py --rollover` so contract-test `# US-xxxx` / `# BUG-xxxx` headings stay on the active `docs/engineering/architecture.md` hot surface (DEC-0129). Do not extend US-0110 / US-0127 / US-0128 / US-0111 tables.

### ARCH_LINKAGE_*

| Code | Meaning | Blocking |
|------|---------|----------|
| **`ARCH_LINKAGE_ROLLOVER_BLOCKED`** | Pre-hook predicted a required heading would leave the hot file, or post-hook found a required heading missing after rollover. Metadata: story/bug id, missing heading token, archive pack path (predicted or written). `ARCH_LINKAGE_REPAIR_FAILED` is message text under this same code (v1 — no sibling family). | **Yes** (`security_hard`; never skip, including `AUTONOMY_STOP_POLICY=auto_repair_then_skip`) |

### Operator remediation

| Reason code | Operator action |
|-------------|------------------|
| `ARCH_LINKAGE_ROLLOVER_BLOCKED` | `set ARCH_LINKAGE_AUTO_REPAIR=1` for stub restore, or restore H1s manually, then rerun `--rollover`. Pre-hook does not write archive pack or hot file. Post-hook packs are append-only (no pack rollback). |

### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0129`
- **Decision record**: `decisions/DEC-0129.md`
- **Library**: `scripts/arch_linkage_guard.py`
- **Contract tests**: `tests/us0129_contract_test.py` — 8 markers

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
