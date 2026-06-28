#!/usr/bin/env python3
"""
Cross-model adversarial critic helper library (US-0104 / DEC-0104).

Reason codes (DEC-0104 §11):
  CROSS_MODEL_REVIEW_DISABLED, CROSS_MODEL_CRITIC_SPAWN_FAILED,
  CROSS_MODEL_MODEL_COLLISION, CROSS_MODEL_ANTISLOP_FAIL,
  CROSS_MODEL_REWORK_CAP_EXHAUSTED, CROSS_MODEL_FINDINGS_INVALID,
  CROSS_MODEL_RECONCILE_FAILED, CROSS_MODEL_DEGRADED_MODE,
  CROSS_MODEL_CRITIC_MODEL_UNAVAILABLE, ISOLATION_EVIDENCE_MODEL_ID_MISSING

Default-off: CROSS_MODEL_REVIEW=0 → zero overhead.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import string
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from model_tier_lib import Tier, resolve_model_for_phase  # noqa: E402


# --- Scratchpad key contracts (DEC-0104 §1) ------------------------------------

CROSS_MODEL_REVIEW_KEY = "CROSS_MODEL_REVIEW"
CROSS_MODEL_ANTISLOP_THRESHOLD_KEY = "CROSS_MODEL_ANTISLOP_THRESHOLD"
CROSS_MODEL_REWORK_MAX_KEY = "CROSS_MODEL_REWORK_MAX"

CROSS_MODEL_REVIEW_VALUES = frozenset({"0", "1"})
CROSS_MODEL_REVIEW_DEFAULT = "0"
CROSS_MODEL_ANTISLOP_THRESHOLD_DEFAULT = 6
CROSS_MODEL_REWORK_MAX_DEFAULT = 2

LENS_VALUES = frozenset({"challenger", "architect", "subtractor"})
SEVERITY_VALUES = frozenset({"low", "medium", "high", "critical"})
CONFIDENCE_VALUES = frozenset({"low", "medium", "high"})
STATUS_VALUES = frozenset({"open", "resolved", "waived"})

FINDINGS_REL = "handoffs/sovereign_critic_findings.jsonl"
FINDINGS_PATH = Path(FINDINGS_REL)
SCHEMA_VERSION = 1
ISSUE_KEY_MAX_CHARS = 80
ISSUE_KEY_HEX_LEN = 16

FINDING_REQUIRED_FIELDS = frozenset({
    "ts",
    "orchestrator_run_id",
    "phase_id",
    "role",
    "producer_model_id",
    "critic_model_id",
    "lens",
    "finding_id",
    "severity",
    "confidence",
    "anti_slop_score",
    "finding_text",
    "status",
    "blocking",
    "degraded_mode",
})

ISOLATION_EVIDENCE_BASE_FIELDS = frozenset({
    "phase_id",
    "role",
    "fresh_context_marker",
    "timestamp",
    "evidence_ref",
})

LENS_CHECKLIST_KEYS = {
    "challenger": (
        "edge_case_cited",
        "failure_mode_named",
        "concurrency_considered",
        "input_boundary_tested",
    ),
    "architect": (
        "coupling_named",
        "layer_boundary_stated",
        "dependency_direction_explicit",
        "interface_contract_mentioned",
    ),
    "subtractor": (
        "unnecessary_abstraction_flagged",
        "yagni_applied",
        "premature_generalization_challenged",
        "scope_creep_identified",
    ),
}

CRITIC_TIER_OPPOSITION = {
    Tier.STRONG: Tier.CHEAP,
    Tier.BALANCED: Tier.CHEAP,
    Tier.CHEAP: Tier.STRONG,
}


class ReasonCode(str, Enum):
    CROSS_MODEL_REVIEW_DISABLED = "CROSS_MODEL_REVIEW_DISABLED"
    CROSS_MODEL_CRITIC_SPAWN_FAILED = "CROSS_MODEL_CRITIC_SPAWN_FAILED"
    CROSS_MODEL_MODEL_COLLISION = "CROSS_MODEL_MODEL_COLLISION"
    CROSS_MODEL_ANTISLOP_FAIL = "CROSS_MODEL_ANTISLOP_FAIL"
    CROSS_MODEL_REWORK_CAP_EXHAUSTED = "CROSS_MODEL_REWORK_CAP_EXHAUSTED"
    CROSS_MODEL_FINDINGS_INVALID = "CROSS_MODEL_FINDINGS_INVALID"
    CROSS_MODEL_RECONCILE_FAILED = "CROSS_MODEL_RECONCILE_FAILED"
    CROSS_MODEL_DEGRADED_MODE = "CROSS_MODEL_DEGRADED_MODE"
    CROSS_MODEL_CRITIC_MODEL_UNAVAILABLE = "CROSS_MODEL_CRITIC_MODEL_UNAVAILABLE"
    ISOLATION_EVIDENCE_MODEL_ID_MISSING = "ISOLATION_EVIDENCE_MODEL_ID_MISSING"


REASON_CODES = frozenset(code.value for code in ReasonCode)


@dataclass
class SelectCriticResult:
    critic_model_id: str
    degraded: bool
    reason_code: Optional[ReasonCode] = None
    producer_model_id: str = ""


@dataclass
class ReconciliationResult:
    findings: List[dict] = field(default_factory=list)
    agreement_groups: List[List[str]] = field(default_factory=list)
    single_finder_flags: List[str] = field(default_factory=list)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


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


def parse_scratchpad_threshold(scratchpad: Optional[Dict[str, str]]) -> int:
    pad = scratchpad or {}
    raw = pad.get(CROSS_MODEL_ANTISLOP_THRESHOLD_KEY, str(CROSS_MODEL_ANTISLOP_THRESHOLD_DEFAULT))
    try:
        value = int(str(raw).strip())
    except (TypeError, ValueError):
        return CROSS_MODEL_ANTISLOP_THRESHOLD_DEFAULT
    return max(0, min(10, value))


def parse_scratchpad_rework_max(scratchpad: Optional[Dict[str, str]]) -> int:
    pad = scratchpad or {}
    raw = pad.get(CROSS_MODEL_REWORK_MAX_KEY, str(CROSS_MODEL_REWORK_MAX_DEFAULT))
    try:
        value = int(str(raw).strip())
    except (TypeError, ValueError):
        return CROSS_MODEL_REWORK_MAX_DEFAULT
    return max(0, value)


def check_isolation_model_id(
    evidence: dict,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Tuple[bool, Optional[ReasonCode]]:
    """Fail-closed when critic enabled and model_id absent on isolation evidence."""
    if not is_cross_model_review_enabled(scratchpad):
        return True, None
    model_id = evidence.get("model_id") if isinstance(evidence, dict) else None
    if model_id is not None and str(model_id).strip():
        return True, None
    return False, ReasonCode.ISOLATION_EVIDENCE_MODEL_ID_MISSING


def is_cross_model_review_enabled(scratchpad: Optional[Dict[str, str]]) -> bool:
    if not scratchpad:
        return False
    return scratchpad.get(CROSS_MODEL_REVIEW_KEY, CROSS_MODEL_REVIEW_DEFAULT).strip() == "1"


def _normalize_model_token(model_id: str) -> str:
    token = (model_id or "").strip().lower()
    if token in ("", "inherit", "none", "omit"):
        return "inherit"
    if token == "fast":
        return "fast"
    return token


def _infer_producer_tier(producer_model_id: str) -> Tier:
    norm = _normalize_model_token(producer_model_id)
    if norm == "fast":
        return Tier.CHEAP
    if norm == "inherit":
        return Tier.BALANCED
    return Tier.STRONG


def _resolve_slug_for_tier(phase_id: str, tier: Tier, scratchpad: Dict[str, str]) -> str:
    tier_key = f"MODEL_TIER_{phase_id.upper().replace('-', '_')}"
    pad = dict(scratchpad)
    pad[tier_key] = tier.value
    pad.setdefault("MODEL_TIER_DEFAULT", tier.value)
    result = resolve_model_for_phase(phase_id, pad)
    if result.success:
        if result.slug:
            return result.slug
        if result.alias:
            return result.alias
    return "inherit"


def select_critic_model(
    producer_model_id: str,
    scratchpad: Optional[Dict[str, str]],
    phase_id: str,
) -> SelectCriticResult:
    pad = scratchpad or {}
    producer = producer_model_id.strip()
    if not producer:
        resolved = resolve_model_for_phase(phase_id, pad)
        if resolved.success:
            producer = resolved.slug or resolved.alias or "inherit"
        else:
            producer = "inherit"

    producer_tier = _infer_producer_tier(producer)
    critic_tier = CRITIC_TIER_OPPOSITION.get(producer_tier, Tier.CHEAP)
    critic = _resolve_slug_for_tier("sovereign-critic", critic_tier, pad)

    if _normalize_model_token(critic) == _normalize_model_token(producer):
        return SelectCriticResult(
            critic_model_id=producer,
            degraded=True,
            reason_code=ReasonCode.CROSS_MODEL_DEGRADED_MODE,
            producer_model_id=producer,
        )

    return SelectCriticResult(
        critic_model_id=critic,
        degraded=False,
        reason_code=None,
        producer_model_id=producer,
    )


def compute_issue_key(finding_text: str) -> str:
    lowered = finding_text.lower()
    table = str.maketrans("", "", string.punctuation)
    cleaned = lowered.translate(table)
    collapsed = re.sub(r"\s+", " ", cleaned).strip()
    if len(collapsed) > ISSUE_KEY_MAX_CHARS:
        truncated = collapsed[:ISSUE_KEY_MAX_CHARS]
        if " " in truncated:
            truncated = truncated.rsplit(" ", 1)[0]
        collapsed = truncated
    digest = hashlib.sha256(collapsed.encode("utf-8")).hexdigest()[:ISSUE_KEY_HEX_LEN]
    return f"ik_{digest}"


def score_lens_antislop(lens: str, checklist_hits: Dict[str, bool]) -> int:
    if lens not in LENS_CHECKLIST_KEYS:
        return 0
    keys = LENS_CHECKLIST_KEYS[lens]
    hits = sum(1 for key in keys if checklist_hits.get(key))
    score = int(round(hits * 2.5))
    return max(0, min(10, score))


def compute_anti_slop_aggregate(lens_scores: List[int]) -> int:
    if not lens_scores:
        return 0
    return min(int(s) for s in lens_scores)


def reconcile_findings(raw_findings: List[dict]) -> ReconciliationResult:
    if not raw_findings:
        return ReconciliationResult()

    keyed: Dict[str, List[dict]] = {}
    for item in raw_findings:
        text = str(item.get("finding_text", ""))
        key = item.get("issue_key") or compute_issue_key(text)
        keyed.setdefault(key, []).append({**item, "issue_key": key})

    merged: List[dict] = []
    agreement_groups: List[List[str]] = []
    single_finder_flags: List[str] = []

    for key, group in keyed.items():
        lenses = {str(g.get("lens", "")) for g in group}
        finding_ids = [str(g.get("finding_id", "")) for g in group if g.get("finding_id")]
        if len(lenses) >= 2:
            confidence = "high"
            single_finder = False
            agreement_groups.append(finding_ids)
        else:
            confidence = "medium"
            single_finder = True
            single_finder_flags.extend(finding_ids)

        base = dict(group[0])
        base["confidence"] = confidence
        base["single_finder"] = single_finder
        base["issue_key"] = key
        merged.append(base)

    return ReconciliationResult(
        findings=merged,
        agreement_groups=agreement_groups,
        single_finder_flags=single_finder_flags,
    )


def schema_check(entry: dict) -> Tuple[bool, Optional[str]]:
    if not isinstance(entry, dict):
        return False, "entry must be object"
    missing = FINDING_REQUIRED_FIELDS - set(entry.keys())
    if missing:
        return False, f"missing fields: {sorted(missing)}"
    extra = set(entry.keys()) - FINDING_REQUIRED_FIELDS - {"issue_key", "single_finder", "rework_generation", "schema_version"}
    if extra:
        return False, f"unknown fields: {sorted(extra)}"
    if entry["lens"] not in LENS_VALUES:
        return False, f"invalid lens: {entry['lens']}"
    if entry["severity"] not in SEVERITY_VALUES:
        return False, f"invalid severity: {entry['severity']}"
    if entry["confidence"] not in CONFIDENCE_VALUES:
        return False, f"invalid confidence: {entry['confidence']}"
    if entry["status"] not in STATUS_VALUES:
        return False, f"invalid status: {entry['status']}"
    score = entry["anti_slop_score"]
    if not isinstance(score, int) or score < 0 or score > 10:
        return False, "anti_slop_score must be int 0-10"
    for bool_field in ("blocking", "degraded_mode"):
        if not isinstance(entry[bool_field], bool):
            return False, f"{bool_field} must be bool"
    if not str(entry["finding_text"]).strip():
        return False, "finding_text must be non-empty"
    return True, None


def append_finding(
    path: Path,
    entry: dict,
    *,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Tuple[bool, Optional[ReasonCode]]:
    if not is_cross_model_review_enabled(scratchpad):
        return False, ReasonCode.CROSS_MODEL_REVIEW_DISABLED
    ok, err = schema_check(entry)
    if not ok:
        return False, ReasonCode.CROSS_MODEL_FINDINGS_INVALID
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(entry, ensure_ascii=False) + "\n"
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(line)
        handle.flush()
        try:
            os.fsync(handle.fileno())
        except OSError:
            _fsync_file(path)
    return True, None


def read_open_blocking(repo: Path) -> List[dict]:
    path = repo / FINDINGS_PATH
    if not path.is_file():
        return []
    open_rows: List[dict] = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if obj.get("blocking") and obj.get("status") == "open":
            open_rows.append(obj)
    return open_rows


def resolve_finding(path: Path, finding_id: str, status: str) -> bool:
    if status not in ("resolved", "waived"):
        return False
    if not path.is_file():
        return False
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    changed = False
    out: List[str] = []
    for raw in lines:
        if not raw.strip():
            out.append(raw)
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            out.append(raw)
            continue
        if str(obj.get("finding_id")) == finding_id:
            obj["status"] = status
            changed = True
            out.append(json.dumps(obj, ensure_ascii=False) + "\n")
        else:
            out.append(raw)
    if changed:
        path.write_text("".join(out), encoding="utf-8")
    return changed


def build_qa_cross_reviewer_block(repo: Path) -> dict:
    rows = read_open_blocking(repo)
    return {
        "cross_reviewer_findings": [
            {
                "finding_id": row.get("finding_id"),
                "lens": row.get("lens"),
                "severity": row.get("severity"),
                "confidence": row.get("confidence"),
                "finding_text": str(row.get("finding_text", ""))[:200],
                "blocking": row.get("blocking", False),
                "degraded_mode": row.get("degraded_mode", False),
            }
            for row in rows
        ],
        "open_blocking_count": len(rows),
        "findings_path": FINDINGS_REL,
    }


def build_critic_evidence_block(
    *,
    scratchpad: Optional[Dict[str, str]] = None,
    producer_model_id: str,
    critic_model_id: str,
    anti_slop_aggregate: int,
    rework_generation: int = 0,
    degraded_mode: bool = False,
) -> Optional[dict]:
    """Additive dev_to_qa evidence tuple when CROSS_MODEL_REVIEW=1."""
    if not is_cross_model_review_enabled(scratchpad):
        return None
    return {
        "producer_model_id": producer_model_id,
        "critic_model_id": critic_model_id,
        "anti_slop_aggregate": int(anti_slop_aggregate),
        "rework_generation": int(rework_generation),
        "degraded_mode": bool(degraded_mode),
        "findings_path": FINDINGS_REL,
    }


def patch_ledger_cross_model_reviewed(
    repo: Path,
    orchestrator_run_id: str,
    phase_id: str,
    role: str,
    *,
    scratchpad: Optional[Dict[str, str]] = None,
    producer_model_id: str = "",
    critic_model_id: str = "",
) -> Tuple[bool, Optional[ReasonCode]]:
    """Append ledger entry with cross_model_reviewed=True when ledger enabled."""
    from decision_ledger_lib import (  # noqa: WPS433
        append_entry,
        build_new_entry,
        is_ledger_enabled,
        resolve_ledger_path,
        resolve_plan_fidelity,
    )

    if not is_ledger_enabled(scratchpad):
        return True, None

    ledger_path = resolve_ledger_path(orchestrator_run_id, repo)
    fidelity = resolve_plan_fidelity(scratchpad).value
    rationale = (
        f"Cross-model critic review completed for {phase_id}/{role} "
        f"(producer={producer_model_id or 'inherit'}, critic={critic_model_id or 'inherit'})."
    )
    entry = build_new_entry(
        orchestrator_run_id=orchestrator_run_id,
        phase_id=phase_id,
        role=role,
        decision_type="CROSS_MODEL_REVIEW",
        rationale=rationale,
        plan_fidelity=fidelity,
        cross_model_reviewed=True,
        risk_tier="medium",
    )
    result = append_entry(ledger_path, entry, scratchpad=scratchpad)
    if not result.success:
        return False, ReasonCode.CROSS_MODEL_FINDINGS_INVALID
    return True, None


def build_sample_finding(**overrides: Any) -> dict:
    base = {
        "ts": _utc_now_iso(),
        "orchestrator_run_id": "self-test-run",
        "phase_id": "research",
        "role": "tech-lead",
        "producer_model_id": "inherit",
        "critic_model_id": "fast",
        "lens": "challenger",
        "finding_id": str(uuid.uuid4()),
        "severity": "medium",
        "confidence": "medium",
        "anti_slop_score": 8,
        "finding_text": "Missing null guard on boundary input path.",
        "status": "open",
        "blocking": False,
        "degraded_mode": False,
    }
    base.update(overrides)
    return base


def self_test() -> bool:
    errors: List[str] = []

    if len(REASON_CODES) != 10:
        errors.append(f"expected 10 reason codes, got {len(REASON_CODES)}")

    if CROSS_MODEL_REVIEW_DEFAULT != "0":
        errors.append("CROSS_MODEL_REVIEW_DEFAULT must be 0")

    if is_cross_model_review_enabled({}) or is_cross_model_review_enabled(None):
        errors.append("default scratchpad must disable critic")

    if not is_cross_model_review_enabled({CROSS_MODEL_REVIEW_KEY: "1"}):
        errors.append("CROSS_MODEL_REVIEW=1 must enable critic")

    key_a = compute_issue_key("Race on concurrent append!")
    key_b = compute_issue_key("race on concurrent append")
    if key_a != key_b:
        errors.append("issue_key normalization mismatch")

    scores = [7, 9, 6]
    if compute_anti_slop_aggregate(scores) != 6:
        errors.append("aggregate must be min(lens_scores)")

    rubric = score_lens_antislop(
        "challenger",
        {
            "edge_case_cited": True,
            "failure_mode_named": True,
            "concurrency_considered": False,
            "input_boundary_tested": False,
        },
    )
    if rubric != 5:
        errors.append(f"challenger rubric expected 5, got {rubric}")

    raw = [
        build_sample_finding(lens="challenger", finding_text="Shared coupling risk in module boundary"),
        build_sample_finding(lens="architect", finding_text="Shared coupling risk in module boundary"),
        build_sample_finding(lens="subtractor", finding_text="Unique over abstraction in helper layer"),
    ]
    reconciled = reconcile_findings(raw)
    if len(reconciled.agreement_groups) != 1:
        errors.append("expected one agreement group")
    if len(reconciled.single_finder_flags) != 1:
        errors.append("expected one single-finder flag")

    sample = build_sample_finding()
    ok, err = schema_check(sample)
    if not ok:
        errors.append(f"schema_check valid sample failed: {err}")

    bad, err = schema_check({"lens": "challenger"})
    if bad:
        errors.append("schema_check should reject incomplete entry")

    select = select_critic_model("inherit", {CROSS_MODEL_REVIEW_KEY: "1"}, "execute")
    if not select.critic_model_id:
        errors.append("select_critic_model must return critic_model_id")

    ok_model, code = check_isolation_model_id({"phase_id": "execute"}, {CROSS_MODEL_REVIEW_KEY: "0"})
    if not ok_model or code is not None:
        errors.append("model_id check must pass when critic disabled")

    bad_model, bad_code = check_isolation_model_id({}, {CROSS_MODEL_REVIEW_KEY: "1"})
    if bad_model or bad_code != ReasonCode.ISOLATION_EVIDENCE_MODEL_ID_MISSING:
        errors.append("model_id check must fail-closed when critic enabled and model_id missing")

    if len(ISOLATION_EVIDENCE_BASE_FIELDS) != 5:
        errors.append("ISOLATION_EVIDENCE_BASE_FIELDS must have 5 base fields")

    if errors:
        for item in errors:
            print(f"  {item}", file=sys.stderr)
        print("[SELF_TEST_FAILED]", file=sys.stderr)
        return False

    print("[SOVEREIGN_CRITIC_SELF_TEST_OK]")
    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sovereign critic library (US-0104 / DEC-0104)")
    parser.add_argument("--self-test", action="store_true", help="Run self-test")
    args = parser.parse_args()
    if args.self_test:
        sys.exit(0 if self_test() else 1)
    parser.print_help()
    sys.exit(2)
