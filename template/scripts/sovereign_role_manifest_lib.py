#!/usr/bin/env python3
"""
Sovereign Role-Behavior Manifest helper library (US-0106 / DEC-0106).

Additive per-role objective + inter-role review obligations layer on top of
US-0069 spawn machinery. Review spawns are supplementary post-phase hooks —
they never substitute for the US-0069 producer role.

Reason codes (DEC-0106 §10):
  SOVEREIGN_ROLE_MANIFEST_DISABLED, SOVEREIGN_ROLE_MANIFEST_SCHEMA_INVALID,
  SOVEREIGN_ROLE_UNKNOWN_ROLE, SOVEREIGN_ROLE_UNKNOWN_PHASE,
  SOVEREIGN_ROLE_SECRET_DETECTED, SOVEREIGN_ROLE_OBJECTIVE_OVERFLOW,
  ROLE_REVIEW_DISPATCH_FAILED, ROLE_REVIEW_SPAWN_FAILED,
  ROLE_REVIEW_BLOCKED, ROLE_REVIEW_DEFERRAL_FAILED,
  ROLE_REVIEW_REWORK_CAP

Default-off: SOVEREIGN_ROLE_MANIFEST=0 → zero overhead.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

SCHEMA_VERSION = 1
MANIFEST_REL = ".cursor/sovereign-role-manifest.yaml"
REVIEWS_JSONL_REL = "handoffs/sovereign_role_reviews.jsonl"

SOVEREIGN_ROLE_MANIFEST_KEY = "SOVEREIGN_ROLE_MANIFEST"
SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS_KEY = "SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS"
SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE_KEY = "SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE"
SOVEREIGN_ROLE_REVIEW_REWORK_MAX_KEY = "SOVEREIGN_ROLE_REVIEW_REWORK_MAX"

SOVEREIGN_ROLE_MANIFEST_VALUES = frozenset({"0", "1"})
SOVEREIGN_ROLE_MANIFEST_DEFAULT = "0"
SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS_DEFAULT = 512
SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE_DEFAULT = 2
SOVEREIGN_ROLE_REVIEW_REWORK_MAX_DEFAULT = 1

OBJECTIVE_FILE_MAX_CHARS = 1024

VALID_ROLE_IDS = frozenset({"po", "tech-lead", "dev", "qa", "release", "curator"})

VALID_REVIEW_FOCI = frozenset({
    "user_value_drift",
    "testability",
    "buildability",
    "deployability",
})

VALID_DEFAULT_ORDERS = frozenset({
    "role_review_first",
    "critic_first",
    "critic_only",
    "role_review_only",
})

ALLOWED_SELF_OVERRIDES = frozenset({"verbosity", "detail_level", "tone"})

VALID_TRIGGER_PHASES = frozenset({
    "intake",
    "discovery",
    "research",
    "architecture",
    "plan-verify",
    "execute",
    "qa",
    "verify-work",
    "release",
    "refresh-context",
    "pause",
    "security-review",
})


class ReasonCode(str, Enum):
    DISABLED = "SOVEREIGN_ROLE_MANIFEST_DISABLED"
    SCHEMA_INVALID = "SOVEREIGN_ROLE_MANIFEST_SCHEMA_INVALID"
    UNKNOWN_ROLE = "SOVEREIGN_ROLE_UNKNOWN_ROLE"
    UNKNOWN_PHASE = "SOVEREIGN_ROLE_UNKNOWN_PHASE"
    SECRET_DETECTED = "SOVEREIGN_ROLE_SECRET_DETECTED"
    OBJECTIVE_OVERFLOW = "SOVEREIGN_ROLE_OBJECTIVE_OVERFLOW"
    REVIEW_DISPATCH_FAILED = "ROLE_REVIEW_DISPATCH_FAILED"
    REVIEW_SPAWN_FAILED = "ROLE_REVIEW_SPAWN_FAILED"
    REVIEW_BLOCKED = "ROLE_REVIEW_BLOCKED"
    REVIEW_DEFERRAL_FAILED = "ROLE_REVIEW_DEFERRAL_FAILED"
    REVIEW_REWORK_CAP = "ROLE_REVIEW_REWORK_CAP"


SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|password|secret|private[_-]?key)\s*[:=]\s*\S+"),
    re.compile(r"sk-[a-zA-Z0-9]{16,}"),
    re.compile(r"ghp_[a-zA-Z0-9]{36}"),
    re.compile(r"(?i)bearer\s+[a-zA-Z0-9\-._~+/]+=*"),
]


def is_role_manifest_enabled(scratchpad: Dict[str, Any]) -> bool:
    return str(scratchpad.get(SOVEREIGN_ROLE_MANIFEST_KEY, SOVEREIGN_ROLE_MANIFEST_DEFAULT)) == "1"


def get_objective_max_chars(scratchpad: Dict[str, Any]) -> int:
    raw = scratchpad.get(SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS_KEY, SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS_DEFAULT)
    try:
        v = int(raw)
        return v if v >= 1 else SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS_DEFAULT
    except (ValueError, TypeError):
        return SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS_DEFAULT


def get_review_max_per_phase(scratchpad: Dict[str, Any]) -> int:
    raw = scratchpad.get(SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE_KEY, SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE_DEFAULT)
    try:
        v = int(raw)
        return v if v >= 0 else SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE_DEFAULT
    except (ValueError, TypeError):
        return SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE_DEFAULT


def get_review_rework_max(scratchpad: Dict[str, Any]) -> int:
    raw = scratchpad.get(SOVEREIGN_ROLE_REVIEW_REWORK_MAX_KEY, SOVEREIGN_ROLE_REVIEW_REWORK_MAX_DEFAULT)
    try:
        v = int(raw)
        return v if v >= 0 else SOVEREIGN_ROLE_REVIEW_REWORK_MAX_DEFAULT
    except (ValueError, TypeError):
        return SOVEREIGN_ROLE_REVIEW_REWORK_MAX_DEFAULT


def scan_secret_literals(text: str) -> List[str]:
    hits: List[str] = []
    for pat in SECRET_PATTERNS:
        m = pat.search(text)
        if m:
            hits.append(m.group(0))
    return hits


def _parse_yaml_minimal(text: str) -> Dict[str, Any]:
    """Minimal YAML-subset parser for the sovereign role manifest.

    Supports the v1 schema: top-level scalars, sequences of mappings
    (roles[], review_obligations[]), simple inline lists, and nested
    scalar mappings (cross_model_policy, escalation_rules, allowed_self_overrides).
    """
    import re as _re
    result: Dict[str, Any] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()
        if not stripped or stripped.lstrip().startswith("#"):
            i += 1
            continue
        if not line.startswith(" ") and not line.startswith("\t"):
            m = _re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)", stripped)
            if m:
                key = m.group(1)
                val = m.group(2).strip()
                if val.startswith("[") and val.endswith("]"):
                    inner = val[1:-1]
                    result[key] = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
                elif val:
                    result[key] = val.strip('"').strip("'")
                else:
                    seq, next_i = _parse_block(lines, i + 1)
                    result[key] = seq
                    i = next_i
                    continue
        i += 1
    return result


def _parse_block(lines: List[str], start: int) -> Tuple[Any, int]:
    """Parse a YAML block starting after a key: line."""
    i = start
    if i >= len(lines):
        return None, i
    first = lines[i]
    indent = len(first) - len(first.lstrip())
    if first.strip().startswith("- "):
        items: List[Any] = []
        while i < len(lines):
            line = lines[i]
            if not line.strip() or line.strip().startswith("#"):
                i += 1
                continue
            cur_indent = len(line) - len(line.lstrip())
            if cur_indent < indent:
                break
            if cur_indent == indent and line.strip().startswith("- "):
                item, i = _parse_mapping(lines, i, indent)
                items.append(item)
            else:
                break
        return items, i
    else:
        mapping: Dict[str, Any] = {}
        while i < len(lines):
            line = lines[i]
            if not line.strip() or line.strip().startswith("#"):
                i += 1
                continue
            cur_indent = len(line) - len(line.lstrip())
            if cur_indent < indent:
                break
            m = re.match(r"^\s+([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)", line)
            if m:
                key = m.group(1)
                val = m.group(2).strip()
                if val.startswith("[") and val.endswith("]"):
                    inner = val[1:-1]
                    mapping[key] = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
                elif val:
                    mapping[key] = val.strip('"').strip("'")
                else:
                    mapping[key] = None
                i += 1
            else:
                i += 1
        return mapping, i


def _parse_mapping(lines: List[str], start: int, base_indent: int) -> Tuple[Dict[str, Any], int]:
    """Parse a single mapping item (- key: val ...) inside a sequence."""
    result: Dict[str, Any] = {}
    first = lines[start]
    content = first.strip()[2:].strip()
    m = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)", content)
    if m:
        result[m.group(1)] = _coerce(m.group(2).strip())
    i = start + 1
    child_indent = base_indent + 2
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        cur_indent = len(line) - len(line.lstrip())
        if cur_indent < child_indent:
            break
        m2 = re.match(r"^\s+([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)", line)
        if m2:
            key = m2.group(1)
            val = m2.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1]
                result[key] = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
            elif val:
                result[key] = _coerce(val)
            else:
                result[key] = None
        i += 1
    return result, i


def _coerce(val: str) -> Any:
    v = val.strip().strip('"').strip("'")
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    try:
        return int(v)
    except ValueError:
        pass
    return v


def load_manifest(repo_root: Path, scratchpad: Optional[Dict[str, Any]] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Load and return the parsed manifest, or (None, reason_code) when disabled/missing."""
    if scratchpad is not None and not is_role_manifest_enabled(scratchpad):
        return None, ReasonCode.DISABLED.value
    manifest_path = repo_root / MANIFEST_REL
    if not manifest_path.is_file():
        return None, ReasonCode.SCHEMA_INVALID.value
    try:
        text = manifest_path.read_text(encoding="utf-8")
    except Exception:
        return None, ReasonCode.SCHEMA_INVALID.value
    parsed = _parse_yaml_minimal(text)
    return parsed, None


def validate_manifest(parsed: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Validate parsed manifest against v1 schema."""
    if parsed.get("schema_version") not in (1, "1"):
        return False, f"schema_version must be 1, got {parsed.get('schema_version')}"
    roles = parsed.get("roles")
    if not isinstance(roles, list) or not roles:
        return False, "roles[] missing or empty"
    seen_roles = set()
    for r in roles:
        if not isinstance(r, dict):
            return False, "roles[] entry not a mapping"
        rid = r.get("role_id")
        if rid not in VALID_ROLE_IDS:
            return False, f"unknown role_id: {rid}"
        if rid in seen_roles:
            return False, f"duplicate role_id: {rid}"
        seen_roles.add(rid)
        obj = r.get("objective_function", "")
        if not obj or len(str(obj)) == 0:
            return False, f"empty objective_function for role {rid}"
        if len(str(obj)) > OBJECTIVE_FILE_MAX_CHARS:
            return False, f"objective_function > {OBJECTIVE_FILE_MAX_CHARS} chars for role {rid}"
        secrets = scan_secret_literals(str(obj))
        if secrets:
            return False, f"secret-shaped literal in objective_function for role {rid}: {secrets[0]}"
    obligations = parsed.get("review_obligations", [])
    if not isinstance(obligations, list):
        return False, "review_obligations must be a list"
    seen_obl_ids = set()
    for obl in obligations:
        if not isinstance(obl, dict):
            return False, "review_obligations[] entry not a mapping"
        oid = obl.get("obligation_id")
        if not oid:
            return False, "missing obligation_id"
        if oid in seen_obl_ids:
            return False, f"duplicate obligation_id: {oid}"
        seen_obl_ids.add(oid)
        rr = obl.get("reviewer_role")
        tr = obl.get("target_role")
        if rr not in VALID_ROLE_IDS:
            return False, f"unknown reviewer_role: {rr}"
        if tr not in VALID_ROLE_IDS:
            return False, f"unknown target_role: {tr}"
        tp = obl.get("trigger_phase")
        if tp not in VALID_TRIGGER_PHASES:
            return False, f"unknown trigger_phase: {tp}"
        rf = obl.get("review_focus")
        if rf not in VALID_REVIEW_FOCI:
            return False, f"unknown review_focus: {rf}"
    cmp = parsed.get("cross_model_policy")
    if cmp and isinstance(cmp, dict):
        do = cmp.get("default_order")
        if do and do not in VALID_DEFAULT_ORDERS:
            return False, f"unknown cross_model_policy.default_order: {do}"
    return True, None


@dataclass
class RoleObligation:
    obligation_id: str
    reviewer_role: str
    target_role: str
    trigger_phase: str
    review_focus: str
    artifact_refs: List[str] = field(default_factory=list)
    blocking: bool = False


def list_obligations_for_phase(
    phase_id: str,
    target_role: str,
    manifest: Dict[str, Any],
    max_per_phase: Optional[int] = None,
) -> List[RoleObligation]:
    if max_per_phase is None:
        max_per_phase = SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE_DEFAULT
    obligations = manifest.get("review_obligations", [])
    result: List[RoleObligation] = []
    for obl in obligations:
        if not isinstance(obl, dict):
            continue
        if obl.get("trigger_phase") == phase_id and obl.get("target_role") == target_role:
            result.append(RoleObligation(
                obligation_id=str(obl.get("obligation_id", "")),
                reviewer_role=str(obl.get("reviewer_role", "")),
                target_role=str(obl.get("target_role", "")),
                trigger_phase=str(obl.get("trigger_phase", "")),
                review_focus=str(obl.get("review_focus", "")),
                artifact_refs=list(obl.get("artifact_refs", [])) if isinstance(obl.get("artifact_refs"), list) else [],
                blocking=bool(obl.get("blocking", False)),
            ))
            if len(result) >= max_per_phase:
                break
    return result


def resolve_role_objective(role_id: str, manifest: Dict[str, Any]) -> Optional[str]:
    roles = manifest.get("roles", [])
    for r in roles:
        if isinstance(r, dict) and r.get("role_id") == role_id:
            return str(r.get("objective_function", ""))
    return None


def build_objective_injection_block(
    scratchpad: Dict[str, Any],
    role_id: str,
    repo_root: Optional[Path] = None,
) -> Tuple[Optional[str], Optional[str]]:
    if not is_role_manifest_enabled(scratchpad):
        return None, ReasonCode.DISABLED.value
    if repo_root is None:
        repo_root = Path.cwd()
    manifest, err = load_manifest(repo_root, scratchpad)
    if manifest is None:
        return None, err
    objective = resolve_role_objective(role_id, manifest)
    if objective is None:
        return None, ReasonCode.UNKNOWN_ROLE.value
    max_chars = get_objective_max_chars(scratchpad)
    truncated = objective[:max_chars]
    block = f"## Role objective ({role_id})\n\n{truncated}"
    return block, None


def resolve_critic_ordering(
    manifest: Dict[str, Any],
    obligation_id: Optional[str] = None,
) -> str:
    cmp_section = manifest.get("cross_model_policy", {})
    if not isinstance(cmp_section, dict):
        return "role_review_first"
    default_order = str(cmp_section.get("default_order", "role_review_first"))
    if obligation_id:
        overrides = cmp_section.get("per_obligation_overrides", {})
        if isinstance(overrides, dict) and obligation_id in overrides:
            return str(overrides[obligation_id])
    if default_order in VALID_DEFAULT_ORDERS:
        return default_order
    return "role_review_first"


def build_review_row(
    obligation: RoleObligation,
    producer_evidence_ref: str,
    orchestrator_run_id: str,
    verdict: str = "pending",
    findings_ref: str = "",
) -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "obligation_id": obligation.obligation_id,
        "reviewer_role": obligation.reviewer_role,
        "target_role": obligation.target_role,
        "trigger_phase": obligation.trigger_phase,
        "review_focus": obligation.review_focus,
        "producer_evidence_ref": producer_evidence_ref,
        "orchestrator_run_id": orchestrator_run_id,
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "verdict": verdict,
        "blocking": obligation.blocking,
        "findings_ref": findings_ref,
    }


def append_review_row(repo_root: Path, row: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    jsonl_path = repo_root / REVIEWS_JSONL_REL
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        return True, None
    except Exception as exc:
        return False, f"{ReasonCode.REVIEW_DISPATCH_FAILED.value}: {exc}"


@dataclass
class RoleReviewDispatch:
    trigger_phase: str
    producer_role: str
    reviewer_role: str
    obligation_id: str
    boundary_token: str
    artifact_refs: List[str]
    producer_evidence_ref: str
    spawn_only: bool = True


def dispatch_role_review(
    obligation: RoleObligation,
    producer_evidence_ref: str,
    trigger_phase: str,
    producer_role: str,
    scratchpad: Optional[Dict[str, Any]] = None,
) -> Tuple[Optional[RoleReviewDispatch], str]:
    """Build a spawn-only review dispatch descriptor (BUG-0006).

    Returns (dispatch, reason_code). The dispatch describes the supplementary
    fresh-reviewer subagent to spawn — the orchestrator spawns, never
    substitutes the producer phase role.
    """
    if scratchpad is not None and not is_role_manifest_enabled(scratchpad):
        return None, ReasonCode.DISABLED.value
    dispatch = RoleReviewDispatch(
        trigger_phase=trigger_phase,
        producer_role=producer_role,
        reviewer_role=obligation.reviewer_role,
        obligation_id=obligation.obligation_id,
        boundary_token="role_review",
        artifact_refs=list(obligation.artifact_refs),
        producer_evidence_ref=producer_evidence_ref,
        spawn_only=True,
    )
    return dispatch, ""


def self_test() -> bool:
    ok, _ = validate_manifest({
        "schema_version": 1,
        "roles": [
            {"role_id": "po", "objective_function": "Maximize user value delivery"},
        ],
        "review_obligations": [
            {
                "obligation_id": "O1",
                "reviewer_role": "po",
                "target_role": "tech-lead",
                "trigger_phase": "architecture",
                "review_focus": "user_value_drift",
                "artifact_refs": ["docs/engineering/architecture.md"],
                "blocking": False,
            },
        ],
        "allowed_self_overrides": ["verbosity", "detail_level", "tone"],
        "cross_model_policy": {"default_order": "role_review_first"},
        "escalation_rules": {"rework_max": 1},
    })
    return ok


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        ok = self_test()
        print("[SOVEREIGN_ROLE_MANIFEST_SELF_TEST_OK]" if ok else "[SOVEREIGN_ROLE_MANIFEST_SELF_TEST_FAIL]")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
