#!/usr/bin/env python3
"""
AI Decision Ledger helper library (US-0103 / DEC-0103).

Provides:
- Append-only JSONL ledger operations (append / read / schema_check / summary_digest)
- Plan-fidelity deviation classifier per AUTO_PLAN_FIDELITY mode
- QA cross-check ledger_findings block builder
- Fail-closed reason codes for ledger + plan-fidelity families

Reason codes (DEC-0103 §8):
  PLAN_FIDELITY_VIOLATION, PLAN_FIDELITY_OVERRIDE, PLAN_FIDELITY_SCOPE_GATE,
  PLAN_FIDELITY_EXTENSION, PLAN_FIDELITY_REORDER,
  LEDGER_FILE_MISSING, LEDGER_SCHEMA_INVALID, LEDGER_APPEND_FAILED,
  LEDGER_CORRUPT, LEDGER_READ_BOUND, LEDGER_DISABLED

Default-off: AI_DECISION_LEDGER=0 → zero overhead (no reads, no writes).
"""

from __future__ import annotations

import json
import os
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# --- Scratchpad key contracts (DEC-0103 §1) -----------------------------------

AI_DECISION_LEDGER_KEY = "AI_DECISION_LEDGER"
AUTO_PLAN_FIDELITY_KEY = "AUTO_PLAN_FIDELITY"

AI_DECISION_LEDGER_VALUES = frozenset({"0", "1"})
AI_DECISION_LEDGER_DEFAULT = "0"

AUTO_PLAN_FIDELITY_VALUES = frozenset({"strict", "relaxed", "extended"})
AUTO_PLAN_FIDELITY_DEFAULT = "strict"


# --- Enums --------------------------------------------------------------------


class PlanFidelity(str, Enum):
    STRICT = "strict"
    RELAXED = "relaxed"
    EXTENDED = "extended"


class RiskTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DecisionType(str, Enum):
    PLAN_FIDELITY_VIOLATION = "PLAN_FIDELITY_VIOLATION"
    PLAN_FIDELITY_OVERRIDE = "PLAN_FIDELITY_OVERRIDE"
    PLAN_FIDELITY_SCOPE_GATE = "PLAN_FIDELITY_SCOPE_GATE"
    PLAN_FIDELITY_EXTENSION = "PLAN_FIDELITY_EXTENSION"
    PLAN_FIDELITY_REORDER = "PLAN_FIDELITY_REORDER"
    LEDGER_DECISION = "LEDGER_DECISION"
    LEDGER_DERIVATION = "LEDGER_DERIVATION"
    LEDGER_PHASE_TRANSITION = "LEDGER_PHASE_TRANSITION"
    LEDGER_DELEGATION = "LEDGER_DELEGATION"


class ReasonCode(str, Enum):
    PLAN_FIDELITY_VIOLATION = "PLAN_FIDELITY_VIOLATION"
    PLAN_FIDELITY_OVERRIDE = "PLAN_FIDELITY_OVERRIDE"
    PLAN_FIDELITY_SCOPE_GATE = "PLAN_FIDELITY_SCOPE_GATE"
    PLAN_FIDELITY_EXTENSION = "PLAN_FIDELITY_EXTENSION"
    PLAN_FIDELITY_REORDER = "PLAN_FIDELITY_REORDER"
    LEDGER_FILE_MISSING = "LEDGER_FILE_MISSING"
    LEDGER_SCHEMA_INVALID = "LEDGER_SCHEMA_INVALID"
    LEDGER_APPEND_FAILED = "LEDGER_APPEND_FAILED"
    LEDGER_CORRUPT = "LEDGER_CORRUPT"
    LEDGER_READ_BOUND = "LEDGER_READ_BOUND"
    LEDGER_DISABLED = "LEDGER_DISABLED"


# --- Canonical phase ids (DEC-0086 / DEC-0087) --------------------------------

CANONICAL_PHASE_IDS = frozenset({
    "ask", "refresh-context", "memory-audit", "status-reconcile", "pause",
    "intake", "discovery", "research", "release", "plan-verify",
    "architecture", "execute", "quick", "qa", "verify-work", "security-review",
    "auto",
})

CANONICAL_ROLES = frozenset({
    "po", "tech-lead", "dev", "qa", "security", "release", "curator",
})


# --- Deviation kind → decision_type mapping (DEC-0103 §3) --------------------

DEVIATION_KINDS = frozenset({
    "drop_ac", "reorder_ac", "add_scope", "generic", "derivation",
    "phase_transition", "delegation", "operator_override",
})


def _deviation_table(mode: PlanFidelity, deviation_kind: str) -> Tuple[DecisionType, ReasonCode, bool]:
    """
    §3 decision table. Returns (decision_type, reason_code, blocking).
    """
    if deviation_kind == "operator_override":
        return (
            DecisionType.PLAN_FIDELITY_OVERRIDE,
            ReasonCode.PLAN_FIDELITY_OVERRIDE,
            False,
        )

    if mode == PlanFidelity.STRICT:
        if deviation_kind in ("drop_ac", "reorder_ac"):
            return (
                DecisionType.PLAN_FIDELITY_VIOLATION,
                ReasonCode.PLAN_FIDELITY_VIOLATION,
                True,
            )
        if deviation_kind == "add_scope":
            return (
                DecisionType.PLAN_FIDELITY_SCOPE_GATE,
                ReasonCode.PLAN_FIDELITY_SCOPE_GATE,
                True,
            )

    if mode == PlanFidelity.RELAXED:
        if deviation_kind in ("drop_ac", "reorder_ac"):
            return (
                DecisionType.PLAN_FIDELITY_REORDER,
                ReasonCode.PLAN_FIDELITY_REORDER,
                False,
            )
        if deviation_kind == "add_scope":
            return (
                DecisionType.PLAN_FIDELITY_SCOPE_GATE,
                ReasonCode.PLAN_FIDELITY_SCOPE_GATE,
                True,
            )

    if mode == PlanFidelity.EXTENDED:
        if deviation_kind == "add_scope":
            return (
                DecisionType.PLAN_FIDELITY_EXTENSION,
                ReasonCode.PLAN_FIDELITY_EXTENSION,
                False,
            )
        if deviation_kind in ("drop_ac", "reorder_ac"):
            return (
                DecisionType.PLAN_FIDELITY_REORDER,
                ReasonCode.PLAN_FIDELITY_REORDER,
                False,
            )

    return (DecisionType.LEDGER_DECISION, ReasonCode.PLAN_FIDELITY_REORDER, False)


# Deviation kind → DecisionType for non-fidelity generic kinds:

_GENERIC_DECISION_TYPE = {
    "generic": DecisionType.LEDGER_DECISION,
    "derivation": DecisionType.LEDGER_DERIVATION,
    "phase_transition": DecisionType.LEDGER_PHASE_TRANSITION,
    "delegation": DecisionType.LEDGER_DELEGATION,
}


# --- Schema v1 (DEC-0103 §2) --------------------------------------------------

LEDGER_SCHEMA_FIELDS = (
    "ts", "orchestrator_run_id", "phase_id", "role",
    "decision_id", "decision_type", "from_artifact", "to_artifact",
    "rationale", "plan_fidelity", "cross_model_reviewed", "risk_tier",
)

LEDGER_REQUIRED_FIELDS = frozenset(LEDGER_SCHEMA_FIELDS)

ARTIFACT_NONE_SENTINEL = "(none)"


def _is_iso8601_utc(value: str) -> bool:
    if not isinstance(value, str):
        return False
    if not value.endswith("Z"):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def _is_uuidv4(value: str) -> bool:
    if not isinstance(value, str):
        return False
    try:
        u = uuid.UUID(value, version=4)
        return str(u) == value.lower()
    except ValueError:
        return False


def schema_check(entry: dict) -> Tuple[bool, Optional[str]]:
    """Validate one JSONL entry against DEC-0103 schema v1 (12-field)."""
    if not isinstance(entry, dict):
        return False, "Entry must be a JSON object"

    missing = [k for k in LEDGER_REQUIRED_FIELDS if k not in entry]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    extra = [k for k in entry.keys() if k not in LEDGER_REQUIRED_FIELDS]
    if extra:
        return False, f"Unknown fields: {', '.join(extra)}"

    if not _is_iso8601_utc(entry["ts"]):
        return False, f"Field 'ts' is not an ISO 8601 UTC timestamp: {entry['ts']!r}"

    if not isinstance(entry["orchestrator_run_id"], str) or not entry["orchestrator_run_id"].strip():
        return False, "Field 'orchestrator_run_id' must be non-empty string"

    if entry["phase_id"] not in CANONICAL_PHASE_IDS:
        return False, f"Field 'phase_id' unknown: {entry['phase_id']!r}"

    if entry["role"] not in CANONICAL_ROLES:
        return False, f"Field 'role' unknown: {entry['role']!r}"

    if not _is_uuidv4(entry["decision_id"]):
        return False, f"Field 'decision_id' is not a valid UUIDv4: {entry['decision_id']!r}"

    try:
        DecisionType(entry["decision_type"])
    except ValueError:
        return False, f"Field 'decision_type' unknown: {entry['decision_type']!r}"

    for path_field in ("from_artifact", "to_artifact"):
        value = entry[path_field]
        if not isinstance(value, str):
            return False, f"Field '{path_field}' must be a string"

    if not isinstance(entry["rationale"], str) or not entry["rationale"].strip():
        return False, "Field 'rationale' must be a non-empty string"

    try:
        PlanFidelity(entry["plan_fidelity"])
    except ValueError:
        return False, f"Field 'plan_fidelity' unknown: {entry['plan_fidelity']!r}"

    if not isinstance(entry["cross_model_reviewed"], bool):
        return False, "Field 'cross_model_reviewed' must be a boolean"

    try:
        RiskTier(entry["risk_tier"])
    except ValueError:
        return False, f"Field 'risk_tier' unknown: {entry['risk_tier']!r}"

    return True, None


# --- Path + enabled checks ----------------------------------------------------


def is_ledger_enabled(scratchpad: Optional[Dict[str, str]] = None) -> bool:
    """AI_DECISION_LEDGER=1 check. Default off."""
    if not scratchpad:
        return False
    value = (scratchpad.get(AI_DECISION_LEDGER_KEY) or AI_DECISION_LEDGER_DEFAULT).strip()
    return value == "1"


def resolve_plan_fidelity(scratchpad: Optional[Dict[str, str]] = None) -> PlanFidelity:
    """AUTO_PLAN_FIDELITY value. Default strict."""
    if not scratchpad:
        return PlanFidelity.STRICT
    value = (scratchpad.get(AUTO_PLAN_FIDELITY_KEY) or AUTO_PLAN_FIDELITY_DEFAULT).strip()
    if value not in AUTO_PLAN_FIDELITY_VALUES:
        return PlanFidelity.STRICT
    return PlanFidelity(value)


def resolve_ledger_path(
    orchestrator_run_id: str,
    repo_root: Optional[Path] = None,
) -> Path:
    """Canonical ledger path per orchestrator run (DEC-0103 §2)."""
    if not orchestrator_run_id or not orchestrator_run_id.strip():
        raise ValueError("orchestrator_run_id must be a non-empty string")
    base = Path(repo_root) if repo_root else Path.cwd()
    return base / "handoffs" / "sovereign_decisions" / f"{orchestrator_run_id.strip()}.jsonl"


# --- Core operations ----------------------------------------------------------


def _fsync_file(path: Path) -> None:
    """fsync a file; best-effort on Windows where some handles reject it."""
    try:
        fd = os.open(str(path), os.O_RDONLY)
        try:
            os.fsync(fd)
        except OSError:
            pass
        finally:
            os.close(fd)
    except OSError:
        pass


@dataclass
class AppendResult:
    success: bool
    reason_code: Optional[ReasonCode] = None
    reason_message: Optional[str] = None
    decision_id: Optional[str] = None


def _ensure_parent_dir(path: Path) -> Tuple[bool, Optional[ReasonCode], Optional[str]]:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        return True, None, None
    except OSError as exc:
        return False, ReasonCode.LEDGER_APPEND_FAILED, f"Cannot create {path.parent}: {exc}"


def append_entry(
    ledger_path: Path,
    entry: dict,
    *,
    scratchpad: Optional[Dict[str, str]] = None,
) -> AppendResult:
    """
    Append one JSONL entry with fsync semantics.

    Default-off: when AI_DECISION_LEDGER=0 (default), returns success with LEDGER_DISABLED
    reason code (informational) and does NOT touch the filesystem.
    """
    if not is_ledger_enabled(scratchpad):
        return AppendResult(
            success=True,
            reason_code=ReasonCode.LEDGER_DISABLED,
            reason_message="AI_DECISION_LEDGER=0 (default); zero overhead; no file written",
        )

    ok, err = schema_check(entry)
    if not ok:
        return AppendResult(
            success=False,
            reason_code=ReasonCode.LEDGER_SCHEMA_INVALID,
            reason_message=err or "Schema validation failed",
            decision_id=entry.get("decision_id"),
        )

    ok_dir, rc_dir, msg_dir = _ensure_parent_dir(ledger_path)
    if not ok_dir:
        return AppendResult(success=False, reason_code=rc_dir, reason_message=msg_dir)

    try:
        line = json.dumps(entry, separators=(",", ":"), sort_keys=False, ensure_ascii=False) + "\n"
        with open(ledger_path, "a", encoding="utf-8") as fh:
            fh.write(line)
            fh.flush()
        _fsync_file(ledger_path)
        return AppendResult(success=True, decision_id=entry.get("decision_id"))
    except OSError as exc:
        return AppendResult(
            success=False,
            reason_code=ReasonCode.LEDGER_APPEND_FAILED,
            reason_message=f"Append failed: {exc}",
            decision_id=entry.get("decision_id"),
        )


def read_entries(
    ledger_path: Path,
    *,
    last_n: Optional[int] = None,
    strict: bool = True,
) -> Tuple[List[dict], Optional[ReasonCode], Optional[str]]:
    """
    Read JSONL ledger entries. Returns (entries, reason_code, message).

    `last_n` bounds the tail returned (default None = all when ledger present).
    When `strict=True`, any schema-invalid line hard-stops and emits LEDGER_SCHEMA_INVALID.
    When `strict=False`, invalid lines are skipped and reason code reflects LEDGER_READ_BOUND.
    """
    if not ledger_path.exists():
        return [], ReasonCode.LEDGER_FILE_MISSING, f"Ledger file not found: {ledger_path}"

    try:
        text = ledger_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return [], ReasonCode.LEDGER_CORRUPT, f"UTF-8 decode failed: {exc}"
    except OSError as exc:
        return [], ReasonCode.LEDGER_CORRUPT, f"Read failed: {exc}"

    raw_lines = [ln for ln in text.split("\n") if ln.strip()]
    parsed: List[dict] = []
    for idx, raw in enumerate(raw_lines, start=1):
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            if strict:
                return [], ReasonCode.LEDGER_CORRUPT, f"Line {idx}: JSON decode error: {exc}"
            continue
        ok, err = schema_check(obj)
        if not ok:
            if strict:
                return [], ReasonCode.LEDGER_SCHEMA_INVALID, f"Line {idx}: {err}"
            continue
        parsed.append(obj)

    if last_n is not None and last_n > 0:
        parsed = parsed[-last_n:]

    warn = None
    if last_n is not None and len(raw_lines) > last_n:
        warn = ReasonCode.LEDGER_READ_BOUND

    return parsed, warn, f"Bounded to last {last_n} of {len(raw_lines)} lines" if warn else None


def classify_deviation(
    mode: PlanFidelity,
    deviation_kind: str,
) -> Tuple[DecisionType, ReasonCode, bool]:
    """
    DEC-0103 §3 deviation classifier. Single source of truth.

    Returns (decision_type, reason_code, blocking).
    """
    if deviation_kind not in DEVIATION_KINDS:
        return (
            DecisionType.LEDGER_DECISION,
            ReasonCode.PLAN_FIDELITY_VIOLATION,
            False,
        )

    if deviation_kind in _GENERIC_DECISION_TYPE:
        dt = _GENERIC_DECISION_TYPE[deviation_kind]
        return (dt, ReasonCode.PLAN_FIDELITY_OVERRIDE, False)

    return _deviation_table(mode, deviation_kind)


# --- Summary digest (DEC-0103 §6) --------------------------------------------

_DECISION_TYPE_ZERO_MAP = {dt.value: 0 for dt in DecisionType}
_RISK_TIER_ZERO_MAP = {rt.value: 0 for rt in RiskTier}


def summary_digest(entries: List[dict]) -> dict:
    """
    Build bounded QA digest — DEC-0103 §6 shape.
    """
    digest = {
        "total_decisions": 0,
        "by_type": dict(_DECISION_TYPE_ZERO_MAP),
        "by_risk_tier": dict(_RISK_TIER_ZERO_MAP),
        "violation_count": 0,
        "override_count": 0,
        "scope_gate_count": 0,
        "extension_count": 0,
    }
    for entry in entries:
        digest["total_decisions"] += 1
        dt = entry.get("decision_type")
        rt = entry.get("risk_tier")
        if dt in digest["by_type"]:
            digest["by_type"][dt] += 1
        if rt in digest["by_risk_tier"]:
            digest["by_risk_tier"][rt] += 1
        if dt == DecisionType.PLAN_FIDELITY_VIOLATION.value:
            digest["violation_count"] += 1
        elif dt == DecisionType.PLAN_FIDELITY_OVERRIDE.value:
            digest["override_count"] += 1
        elif dt == DecisionType.PLAN_FIDELITY_SCOPE_GATE.value:
            digest["scope_gate_count"] += 1
        elif dt == DecisionType.PLAN_FIDELITY_EXTENSION.value:
            digest["extension_count"] += 1
    return digest


def build_qa_findings_block(
    ledger_path: Path,
    orchestrator_run_id: str,
    *,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Tuple[dict, Optional[ReasonCode]]:
    """
    Build `ledger_findings` block for QA emission (DEC-0103 §6).
    Returns (block_dict, blocking_reason_code_or_None).
    """
    if not is_ledger_enabled(scratchpad):
        return {
            "ledger_findings": [],
            "ledger_summary_digest": summary_digest([]),
            "ledger_source": str(ledger_path),
            "ledger_orchestrator_run_id": orchestrator_run_id,
            "ledger_status": "disabled",
        }, ReasonCode.LEDGER_DISABLED

    entries, reason, message = read_entries(ledger_path, last_n=100)
    if reason == ReasonCode.LEDGER_FILE_MISSING:
        return {
            "ledger_findings": [],
            "ledger_summary_digest": summary_digest([]),
            "ledger_source": str(ledger_path),
            "ledger_orchestrator_run_id": orchestrator_run_id,
            "ledger_status": "file_missing",
            "ledger_error": message or "Ledger file does not exist",
        }, ReasonCode.LEDGER_FILE_MISSING

    if reason in (ReasonCode.LEDGER_SCHEMA_INVALID, ReasonCode.LEDGER_CORRUPT):
        return {
            "ledger_findings": [],
            "ledger_summary_digest": summary_digest([]),
            "ledger_source": str(ledger_path),
            "ledger_orchestrator_run_id": orchestrator_run_id,
            "ledger_status": "schema_invalid",
            "ledger_error": message or "Ledger lines failed schema_check",
        }, reason

    findings: List[dict] = []
    for entry in entries:
        rationale = (entry.get("rationale") or "").strip()
        findings.append({
            "decision_id": entry["decision_id"],
            "decision_type": entry["decision_type"],
            "phase_id": entry["phase_id"],
            "rationale_summary": rationale[:200],
            "risk_tier": entry["risk_tier"],
            "plan_fidelity_mode": entry["plan_fidelity"],
            "cross_model_reviewed": bool(entry.get("cross_model_reviewed", False)),
        })

    return {
        "ledger_findings": findings,
        "ledger_summary_digest": summary_digest(entries),
        "ledger_source": str(ledger_path),
        "ledger_orchestrator_run_id": orchestrator_run_id,
        "ledger_status": "ok",
    }, None


# --- Builder convenience ------------------------------------------------------


def build_new_entry(
    *,
    orchestrator_run_id: str,
    phase_id: str,
    role: str,
    decision_type: str,
    rationale: str,
    plan_fidelity: str,
    risk_tier: str = "medium",
    from_artifact: str = ARTIFACT_NONE_SENTINEL,
    to_artifact: str = ARTIFACT_NONE_SENTINEL,
    cross_model_reviewed: bool = False,
    decision_id: Optional[str] = None,
    ts: Optional[str] = None,
) -> dict:
    """Build a valid ledger entry dict. Raises ValueError on invalid inputs."""
    ts_value = ts or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    did = decision_id or str(uuid.uuid4())
    return {
        "ts": ts_value,
        "orchestrator_run_id": orchestrator_run_id,
        "phase_id": phase_id,
        "role": role,
        "decision_id": did,
        "decision_type": decision_type,
        "from_artifact": from_artifact,
        "to_artifact": to_artifact,
        "rationale": rationale,
        "plan_fidelity": plan_fidelity,
        "cross_model_reviewed": bool(cross_model_reviewed),
        "risk_tier": risk_tier,
    }


# --- Self-test ----------------------------------------------------------------


def self_test() -> bool:
    """Run self-test to validate library contract (US-0103 / DEC-0103)."""
    print("[SELF-TEST] Validating decision_ledger_lib contract...")
    errors: List[str] = []

    # Scratchpad literals
    if AI_DECISION_LEDGER_VALUES != {"0", "1"}:
        errors.append(f"AI_DECISION_LEDGER_VALUES mismatch: {AI_DECISION_LEDGER_VALUES}")
    if AI_DECISION_LEDGER_DEFAULT != "0":
        errors.append(f"AI_DECISION_LEDGER_DEFAULT mismatch: {AI_DECISION_LEDGER_DEFAULT}")
    if AUTO_PLAN_FIDELITY_VALUES != {"strict", "relaxed", "extended"}:
        errors.append(f"AUTO_PLAN_FIDELITY_VALUES mismatch: {AUTO_PLAN_FIDELITY_VALUES}")
    if AUTO_PLAN_FIDELITY_DEFAULT != "strict":
        errors.append(f"AUTO_PLAN_FIDELITY_DEFAULT mismatch: {AUTO_PLAN_FIDELITY_DEFAULT}")

    # Enum cardinalities (DEC-0103 §8 — 5 + 6 = 11 reason codes; 3+4+9 = 16 decisions)
    if len(ReasonCode) != 11:
        errors.append(f"ReasonCode count: expected 11, got {len(ReasonCode)}")
    plan_fidelity_codes = {c for c in ReasonCode if c.value.startswith("PLAN_FIDELITY_")}
    ledger_codes = {c for c in ReasonCode if c.value.startswith("LEDGER_")}
    if len(plan_fidelity_codes) != 5:
        errors.append(f"PLAN_FIDELITY_* codes expected 5, got {len(plan_fidelity_codes)}")
    if len(ledger_codes) != 6:
        errors.append(f"LEDGER_* codes expected 6, got {len(ledger_codes)}")

    # is_ledger_enabled / is_ledger_enabled default
    if is_ledger_enabled(None) or is_ledger_enabled({}) or is_ledger_enabled({"AI_DECISION_LEDGER": "0"}):
        errors.append("is_ledger_enabled should be False by default")
    if not is_ledger_enabled({"AI_DECISION_LEDGER": "1"}):
        errors.append("is_ledger_enabled should be True when key=1")

    # resolve_plan_fidelity default path
    if resolve_plan_fidelity(None) != PlanFidelity.STRICT:
        errors.append("resolve_plan_fidelity default should be strict")

    # schema_check + append round-trip
    good = build_new_entry(
        orchestrator_run_id="self-test-run-1",
        phase_id="research",
        role="tech-lead",
        decision_type=DecisionType.LEDGER_DECISION.value,
        rationale="Self-test rationale.",
        plan_fidelity=PlanFidelity.STRICT.value,
        risk_tier=RiskTier.LOW.value,
    )
    ok, err = schema_check(good)
    if not ok:
        errors.append(f"schema_check should accept valid entry: {err}")

    bad = dict(good)
    bad["decision_id"] = "not-a-uuid"
    ok_b, err_b = schema_check(bad)
    if ok_b:
        errors.append("schema_check should reject invalid decision_id")
    if err_b is None:
        errors.append("schema_check error message must be non-None on failure")

    bad2 = dict(good)
    bad2["phase_id"] = "not-a-phase"
    ok_b2, err_b2 = schema_check(bad2)
    if ok_b2:
        errors.append("schema_check should reject unknown phase_id")

    # classify_deviation strict + drop_ac → blocking
    dt, rc, blocking = classify_deviation(PlanFidelity.STRICT, "drop_ac")
    if not blocking or dt != DecisionType.PLAN_FIDELITY_VIOLATION:
        errors.append(f"strict+drop_ac should be blocking PLAN_FIDELITY_VIOLATION (got {dt}, {blocking})")

    # relaxed+reorder_ac → non-blocking
    dt, rc, blocking = classify_deviation(PlanFidelity.RELAXED, "reorder_ac")
    if blocking or dt != DecisionType.PLAN_FIDELITY_REORDER:
        errors.append(f"relaxed+reorder_ac should be non-blocking PLAN_FIDELITY_REORDER (got {dt}, {blocking})")

    # extended+add_scope → non-blocking extension
    dt, rc, blocking = classify_deviation(PlanFidelity.EXTENDED, "add_scope")
    if blocking or dt != DecisionType.PLAN_FIDELITY_EXTENSION:
        errors.append(f"extended+add_scope should be non-blocking PLAN_FIDELITY_EXTENSION (got {dt}, {blocking})")

    # summary_digest shape
    digest = summary_digest([good])
    if digest["total_decisions"] != 1:
        errors.append("summary_digest total_decisions != 1")
    if "violation_count" not in digest or "by_type" not in digest or "by_risk_tier" not in digest:
        errors.append("summary_digest shape missing required keys")

    if errors:
        print("[SELF_TEST_FAILED]")
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return False

    print("[DECISION_LEDGER_SELF_TEST_OK]")
    return True


# --- CLI ----------------------------------------------------------------------


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Decision ledger library (US-0103 / DEC-0103)")
    parser.add_argument("--self-test", action="store_true", help="Run self-test")
    parser.add_argument("--append-json", help="JSON string of entry to append")
    parser.add_argument("--ledger", type=Path, help="Ledger path for --append-json")
    parser.add_argument("--orchestrator-run-id", help="Resolve path for --append-json")
    parser.add_argument("--dump-digest", type=Path, help="Print summary_digest for ledger path")
    parser.add_argument("--repo", type=Path, default=None, help="Repo root for ledger path resolution")

    args = parser.parse_args()

    if args.self_test:
        sys.exit(0 if self_test() else 1)

    if args.dump_digest:
        entries, reason, message = read_entries(args.dump_digest, strict=True)
        if reason in (ReasonCode.LEDGER_FILE_MISSING, ReasonCode.LEDGER_SCHEMA_INVALID, ReasonCode.LEDGER_CORRUPT):
            print(f"[LEDGER_READ_FAIL] {reason.value}: {message}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(summary_digest(entries), indent=2, sort_keys=True))
        sys.exit(0)

    if args.append_json:
        if not args.ledger and not args.orchestrator_run_id:
            print("[USAGE] --ledger or --orchestrator-run-id required", file=sys.stderr)
            sys.exit(2)
        path = args.ledger or resolve_ledger_path(args.orchestrator_run_id, args.repo)
        try:
            entry = json.loads(args.append_json)
        except json.JSONDecodeError as exc:
            print(f"[USAGE] invalid --append-json: {exc}", file=sys.stderr)
            sys.exit(2)
        res = append_entry(path, entry)
        if res.success:
            print(f"[OK] decision_id={res.decision_id} reason={res.reason_code.value if res.reason_code else 'appended'}")
            sys.exit(0)
        print(f"[FAIL] {res.reason_code.value if res.reason_code else 'append_failed'}: {res.reason_message}", file=sys.stderr)
        sys.exit(1)

    parser.print_help()
    sys.exit(0)
