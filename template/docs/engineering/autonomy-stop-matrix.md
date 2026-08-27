# Autonomy Stop Matrix (US-0119 / DEC-0119)

**Owner**: `DEC-0119` (Accepted 2026-07-05)
**Story**: `US-0119` — Autonomous-autonomy presets and configurable hard-stop relaxation
**Consumer**: `scripts/validate_autonomy_stop_matrix.py` (validator)
**Template parity**: `template/docs/engineering/autonomy-stop-matrix.md` (byte-identical)

## Purpose

Classifies all fail-closed reason codes into two stop classes to support `AUTONOMY_STOP_POLICY` dispatch:

- **`security_hard`**: NEVER auto-repaired under any preset/policy. Block immediately.
- **`autonomy_resolvable`**: Bounded auto-repair permitted when `AUTONOMY_STOP_POLICY != block`. Cap per (run, reason_code) from matrix `cap` column (default 3 per R-0107 Q3).

## Stop class rules

| Stop class | `auto_repair_kind` | `cap` | Rationale |
|------------|--------------------|----|-----------|
| `security_hard` | `n/a` (MUST) | `0` (MUST) | Security boundary — never softened |
| `autonomy_resolvable` | one of 9 taxonomy values (MUST) | `>= 1` or `0` for terminal stops (MUST) | Bounded repair with audit trail |

## `auto_repair_kind` taxonomy (9 values — R-0107 Q2)

| auto_repair_kind | Description |
|------------------|-------------|
| `reorder_anchors` | Sort H1s by story ID |
| `fix_timestamp` | Replace stale timestamp with `now()` |
| `truncate_hot_surface` | Archive rollover |
| `reset_retry_counter` | Reset to 0 |
| `disambiguate_state` | Pick last-known phase |
| `auto_refresh_brief` | Regenerate from state.md |
| `approve_plan_deviation` | Ledger waiver |
| `regenerate_isolation_evidence` | Re-run context-refresh |
| `skip_confirmation_gate` | Allowlist-gated skip |

## Security-hard gates (19 codes)

Reason codes that are NEVER auto-repaired. Violation of any triggers terminal `AUTONOMY_REPAIR_CAP_EXHAUSTED` escalation.

| Reason code | Rationale |
|-------------|-----------|
| `PHASE_CONTEXT_ISOLATION_VIOLATION` | Context isolation is a fundamental security boundary |
| `PHASE_CONTEXT_ISOLATION_MISSING` | Missing isolation evidence = untrusted context |
| `ISOLATION_EVIDENCE_STALE` | Stale evidence = untrusted context |
| `RUNTIME_PROOF_MISSING` | Proof absence = unverifiable execution |
| `RUNTIME_PROOF_REUSED` | Proof reuse = unverifiable execution |
| `RUNTIME_PROOF_STALE` | Stale proof = unverifiable execution |
| `RUNTIME_PROOF_AMBIGUOUS_LINK` | Ambiguous link = unverifiable execution |
| `PHASE_ROLE_CAPABILITY_MISSING` | Role capability is a security boundary |
| `PHASE_ROLE_MISMATCH` | Role mismatch is a security boundary |
| `PHASE_OWNERSHIP_VIOLATION` | Ownership is a security boundary |
| `PHASE_OVERRIDE_EVIDENCE_MISSING` | Override evidence is a security boundary |
| `INTAKE_BUG_ROUTING_REQUIRED` | Bug routing is a structural gate |
| `INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT` | Topic distinctness is a truthfulness boundary |
| `INTAKE_REQUIRED_TOPIC_MISSING` | Required topic absence blocks intake |
| `INTAKE_PERSISTENCE_BLOCKED` | Persistence failure = unreliable state |
| `AUTO_SCHEDULER_CONFLICT` | Scheduler conflict = unreliable sequencing |
| `RESUME_BRIEF_STALE` (when `RESUME_BRIEF_AUTO_REFRESH != 1`) | Stale brief = unreliable context (when auto-refresh not enabled) |
| `SECURITY_REVIEW_CRITICAL_FINDING` | Security review critical = security boundary |
| `ARCH_LINKAGE_ROLLOVER_BLOCKED` | Architecture rollover would drop headings still required by contract tests (US-0129); never skip, including under `AUTONOMY_STOP_POLICY=auto_repair_then_skip` |

## Autonomy-resolvable gates (9 codes)

Reason codes that may be auto-repaired when `AUTONOMY_STOP_POLICY` allows. Cap per (run, reason_code) from matrix `cap` column.

| Reason code | `auto_repair_kind` | `cap` | Rationale |
|-------------|---------------------|-------|-----------|
| `ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS` | `reorder_anchors` | `3` | Sort H1s by story ID (mechanical fix) |
| `STATE_TIMESTAMP_NON_MONOTONIC` | `fix_timestamp` | `3` | Replace stale timestamp (mechanical fix) |
| `ARTIFACT_HOT_SURFACE_OVERSIZE` | `truncate_hot_surface` | `3` | Archive rollover (mechanical fix) |
| `BLOCK_RETRY_CAP_EXHAUSTED` | `reset_retry_counter` | `3` | Reset to 0 (ledger entry) |
| `STATE_PHASE_AMBIGUOUS` | `disambiguate_state` | `3` | Pick last-known phase (unambiguous selection) |
| `RESUME_BRIEF_MISSING` | `auto_refresh_brief` | `3` | Regenerate brief from state.md (when `RESUME_BRIEF_AUTO_REFRESH=1`) |
| `PLAN_FIDELITY_VIOLATION` | `approve_plan_deviation` | `3` | Ledger waiver (bounded audit trail) |
| `ISOLATION_EVIDENCE_INVALID` | `regenerate_isolation_evidence` | `3` | Re-run context-refresh (mechanical fix) |
| `RELEASE_PUBLISH_MODE` | `skip_confirmation_gate` | `3` | Allowlist-gated skip (when target in `RELEASE_TARGETS_ALLOWLIST`) |

## Terminal stop reasons

Reason codes emitted by the bounded auto-repair ledger when cap is exhausted.

| Reason code | `auto_repair_kind` | `cap` | Rationale |
|-------------|---------------------|-------|-----------|
| `AUTONOMY_REPAIR_CAP_EXHAUSTED` | `n/a` | `0` | Terminal stop — cap exhaustion escalates to operator (distinct from `BLOCK_RETRY_CAP_EXHAUSTED` per R-0107 Q9) |

## Matrix validator

`scripts/validate_autonomy_stop_matrix.py --self-test` enforces:
- No orphan reason codes in scripts (grep `scripts/*.py` for codes not in YAML → fail)
- `security_hard` rows carry `auto_repair_kind=n/a`
- `autonomy_resolvable` rows carry finite `cap` (default 3)
- Every reason code in `.cursor/commands/*.md` is in YAML (grep-based cross-check per R-0107 Q8)

Exit 0 = matrix valid. Exit non-zero = matrix invalid (list of violations on stderr).

## YAML single source of truth

`scripts/data/autonomy_stop_matrix.yaml` is the machine-readable companion. Validator reads YAML, not this markdown file. Markdown is operator-facing documentation; YAML is the contract.

## Compose guards

US-0119 composes read-only with US-0092 / US-0095 / US-0056 / US-0068 / US-0096 / BUG-0007. This matrix does NOT amend their architectural surfaces. Stop classification is additive only.
