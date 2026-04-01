"""Token-cost run class, metrics, and AC-2 comparability helpers (US-0080 / DEC-0062)."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

# Canonical metric keys (DEC-0062 §1) — totals / per-phase rows
METRIC_KEYS = (
    "cache_read_tokens",
    "input_tokens",
    "output_tokens",
    "phase_call_count",
    "cache_creation_tokens",
    "orchestrator_call_estimate",
)

REQUIRED_TOTAL_KEYS = (
    "cache_read_tokens",
    "input_tokens",
    "output_tokens",
)


def canonical_json_dumps(obj: Mapping[str, Any]) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def compute_run_class_hash(run_class: Mapping[str, Any]) -> str:
    """SHA-256 hex (lowercase) of canonical JSON for DEC-0062 §2 tuple."""
    payload = canonical_json_dumps(run_class)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def compute_strict_proof_hash(
    orchestrator_run_id: str,
    runtime_proof_id: str,
    phase_id: str,
    role: str,
    proof_issued_at: str,
    proof_ttl_seconds: int,
) -> str:
    """DEC-0038-style sorted-key JSON SHA-256 over the strict-proof tuple fields."""
    obj = {
        "orchestrator_run_id": orchestrator_run_id,
        "runtime_proof_id": runtime_proof_id,
        "phase_id": phase_id,
        "role": role,
        "proof_issued_at": proof_issued_at,
        "proof_ttl_seconds": int(proof_ttl_seconds),
    }
    return hashlib.sha256(canonical_json_dumps(obj).encode("utf-8")).hexdigest()


def validate_run_totals(row: Mapping[str, Any]) -> list[str]:
    """Return diagnostic strings for invalid totals; empty if OK."""
    errs: list[str] = []
    for k in REQUIRED_TOTAL_KEYS:
        if k not in row:
            errs.append(f"missing_metric:{k}")
            continue
        v = row[k]
        if not isinstance(v, int) or v < 0:
            errs.append(f"invalid_non_negative_int:{k}")
    if "metric_source" not in row or not str(row.get("metric_source", "")).strip():
        errs.append("missing_metric_source")
    return errs


def compare_cache_read_reduction(
    baseline: Mapping[str, Any],
    target: Mapping[str, Any],
    *,
    reduction_fraction: float = 0.5,
) -> tuple[bool, str]:
    """
    AC-2: target must achieve >= reduction_fraction lower cache_read_tokens
    vs baseline when run_class_hash matches. Otherwise TOKEN_COST_RUN_CLASS_MISMATCH.
    """
    hb = baseline.get("run_class_hash")
    ht = target.get("run_class_hash")
    if not isinstance(hb, str) or not isinstance(ht, str) or hb != ht:
        return False, "TOKEN_COST_RUN_CLASS_MISMATCH: run_class_hash differs or missing"

    tb = baseline.get("totals") or {}
    tt = target.get("totals") or {}
    if not isinstance(tb, Mapping) or not isinstance(tt, Mapping):
        return False, "TOKEN_COST_RUN_CLASS_MISMATCH: totals object missing"

    br = tb.get("cache_read_tokens")
    tr = tt.get("cache_read_tokens")
    if not isinstance(br, int) or not isinstance(tr, int) or br < 0 or tr < 0:
        return False, "TOKEN_COST_RUN_CLASS_MISMATCH: invalid cache_read_tokens"

    if br == 0:
        if tr == 0:
            return True, "ok: baseline and target zero cache_read_tokens"
        return False, "TOKEN_COST_RUN_CLASS_MISMATCH: baseline zero but target non-zero"

    max_target = int(br * (1.0 - reduction_fraction))
    if tr > max_target:
        return (
            False,
            f"TOKEN_COST_RUN_CLASS_MISMATCH: cache_read_tokens {tr} exceeds "
            f"50% reduction threshold (baseline {br}, max_target {max_target})",
        )
    return True, "ok: cache_read_tokens meets 50% reduction vs baseline"
