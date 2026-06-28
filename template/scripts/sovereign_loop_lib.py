#!/usr/bin/env python3
"""
Sovereign Loop Mode helper library (US-0107 / DEC-0107).

Deferral register, drain-generate gate, notification dispatch, and convergence
hooks composing US-0088/US-0092/US-0095/US-0103/US-0105/US-0110.

Sidecar schema v1 — ``handoffs/sovereign_loop_state.json`` (create-on-first-write):

    {"schema_version": 1, "drain_generate_iterations": {"<orchestrator_run_id>": <int>}}

Reason codes (DEC-0107 §9):
  SOVEREIGN_LOOP_DISABLED, SOVEREIGN_LOOP_GOAL_MODE_REQUIRED,
  SOVEREIGN_DEFERRAL_CAP_EXCEEDED, SOVEREIGN_DEFERRAL_SCHEMA_INVALID,
  SOVEREIGN_DEFERRAL_APPEND_FAILED, SOVEREIGN_DRAIN_GENERATE_CAP,
  SOVEREIGN_DRAIN_GENERATE_BLOCKED, SOVEREIGN_NOTIFY_DISPATCH_FAILED,
  SOVEREIGN_NOTIFY_TARGET_INVALID, SOVEREIGN_NOTIFY_CONFIG_MISSING,
  SOVEREIGN_LOOP_ADVANCE_BLOCKED, DEPLOY_DEFERRED

Default-off: AUTO_SOVEREIGN=0 → zero overhead (no reads, no writes, no advance).
Requires SOVEREIGN_GOAL_MODE=goal_convergence when enabled (fail-closed).
"""

from __future__ import annotations

import json
import re
import sys
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
from urllib import error as urllib_error
from urllib import request as urllib_request

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from sovereign_convergence_lib import (  # noqa: E402
    SOVEREIGN_GOAL_MODE_KEY,
    check_timeout,
    evaluate_convergence,
    is_goal_convergence_enabled,
    resolve_goal,
    write_partial_delivery_report,
)

SCHEMA_VERSION = 1
DEFERRALS_PATH = Path("handoffs/sovereign_deferrals.jsonl")
LOOP_STATE_PATH = Path("handoffs/sovereign_loop_state.json")

AUTO_SOVEREIGN_KEY = "AUTO_SOVEREIGN"
AUTO_SOVEREIGN_DEFERRAL_MAX_KEY = "AUTO_SOVEREIGN_DEFERRAL_MAX"
AUTO_SOVEREIGN_DRAIN_GENERATE_MAX_KEY = "AUTO_SOVEREIGN_DRAIN_GENERATE_MAX"
AUTO_SOVEREIGN_DEFERRAL_POLICY_KEY = "AUTO_SOVEREIGN_DEFERRAL_POLICY"
SOVEREIGN_NOTIFY_TARGET_KEY = "SOVEREIGN_NOTIFY_TARGET"
SOVEREIGN_NOTIFY_NTFY_TOPIC_KEY = "SOVEREIGN_NOTIFY_NTFY_TOPIC"
SOVEREIGN_NOTIFY_NTFY_BASE_KEY = "SOVEREIGN_NOTIFY_NTFY_BASE"
SOVEREIGN_NOTIFY_HOOK_URL_KEY = "SOVEREIGN_NOTIFY_HOOK_URL"
SOVEREIGN_NOTIFY_EMAIL_TO_KEY = "SOVEREIGN_NOTIFY_EMAIL_TO"

AUTO_SOVEREIGN_DEFAULT = "0"
AUTO_SOVEREIGN_DEFERRAL_MAX_DEFAULT = 50
AUTO_SOVEREIGN_DRAIN_GENERATE_MAX_DEFAULT = 3
AUTO_SOVEREIGN_DEFERRAL_POLICY_DEFAULT = "resolve_first"
SOVEREIGN_NOTIFY_TARGET_DEFAULT = "off"

AUTO_SOVEREIGN_VALUES = frozenset({"0", "1"})
DEFERRAL_POLICY_VALUES = frozenset({"stop", "skip", "resolve_first"})
NOTIFY_TARGET_VALUES = frozenset({"off", "ntfy", "email", "hook"})
WORK_ITEM_KIND_VALUES = frozenset({"story", "bug", "deploy", "block"})
DEFERRAL_STATE_VALUES = frozenset({"open", "resolved", "superseded"})
STEP_ACTION_VALUES = frozenset({
    "noop",
    "continue",
    "defer",
    "drain_generate",
    "terminal_converged",
    "terminal_timeout",
    "terminal_cap",
    "blocked",
})
NOTIFY_EVENT_VALUES = frozenset({
    "convergence",
    "timeout",
    "deferral_cap",
    "drain_generate_cap",
})
PROVENANCE_VALUES = frozenset({"vision", "memory", "both"})

REMEDIATION_HINT_MAX = 512
WORK_ITEM_REF_MAX = 128
TITLE_MAX = 120
SUMMARY_MAX = 512
AC_SKETCH_MAX_ITEMS = 8
AC_SKETCH_ITEM_MAX = 256
MAX_CANDIDATES_PER_ITERATION = 3

REQUIRED_DEFERRAL_FIELDS = frozenset({
    "schema_version",
    "deferral_id",
    "ts",
    "reason_code",
    "work_item_kind",
    "work_item_ref",
    "state",
    "source_orchestrator_run_id",
    "remediation_hint",
})

_SECRET_PATTERNS = (
    re.compile(r"api_key\s*=", re.I),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9]{8,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
)


class ReasonCode(str, Enum):
    SOVEREIGN_LOOP_DISABLED = "SOVEREIGN_LOOP_DISABLED"
    SOVEREIGN_LOOP_GOAL_MODE_REQUIRED = "SOVEREIGN_LOOP_GOAL_MODE_REQUIRED"
    SOVEREIGN_DEFERRAL_CAP_EXCEEDED = "SOVEREIGN_DEFERRAL_CAP_EXCEEDED"
    SOVEREIGN_DEFERRAL_SCHEMA_INVALID = "SOVEREIGN_DEFERRAL_SCHEMA_INVALID"
    SOVEREIGN_DEFERRAL_APPEND_FAILED = "SOVEREIGN_DEFERRAL_APPEND_FAILED"
    SOVEREIGN_DRAIN_GENERATE_CAP = "SOVEREIGN_DRAIN_GENERATE_CAP"
    SOVEREIGN_DRAIN_GENERATE_BLOCKED = "SOVEREIGN_DRAIN_GENERATE_BLOCKED"
    SOVEREIGN_NOTIFY_DISPATCH_FAILED = "SOVEREIGN_NOTIFY_DISPATCH_FAILED"
    SOVEREIGN_NOTIFY_TARGET_INVALID = "SOVEREIGN_NOTIFY_TARGET_INVALID"
    SOVEREIGN_NOTIFY_CONFIG_MISSING = "SOVEREIGN_NOTIFY_CONFIG_MISSING"
    SOVEREIGN_LOOP_ADVANCE_BLOCKED = "SOVEREIGN_LOOP_ADVANCE_BLOCKED"
    DEPLOY_DEFERRED = "DEPLOY_DEFERRED"


REASON_CODES = frozenset(code.value for code in ReasonCode)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _scratchpad_int(scratchpad: Dict[str, str], key: str, default: int) -> int:
    raw = scratchpad.get(key, str(default)).strip()
    try:
        return max(0, int(raw))
    except ValueError:
        return default


def scan_secrets(text: str) -> Optional[ReasonCode]:
    for pattern in _SECRET_PATTERNS:
        if pattern.search(text or ""):
            return ReasonCode.SOVEREIGN_DEFERRAL_SCHEMA_INVALID
    return None


def is_sovereign_loop_enabled(scratchpad: Dict[str, str]) -> bool:
    if scratchpad.get(AUTO_SOVEREIGN_KEY, AUTO_SOVEREIGN_DEFAULT).strip() != "1":
        return False
    return is_goal_convergence_enabled(scratchpad)


def resolve_deferrals_path(repo_root: Path) -> Path:
    return repo_root / DEFERRALS_PATH


def schema_check_deferral(entry: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    if not isinstance(entry, dict):
        return False, "entry must be object"

    missing = REQUIRED_DEFERRAL_FIELDS - set(entry.keys())
    if missing:
        return False, f"missing required fields: {sorted(missing)}"

    if entry.get("schema_version") != SCHEMA_VERSION:
        return False, "schema_version must be 1"

    if entry.get("work_item_kind") not in WORK_ITEM_KIND_VALUES:
        return False, "invalid work_item_kind"

    if entry.get("state") not in DEFERRAL_STATE_VALUES:
        return False, "invalid state"

    hint = str(entry.get("remediation_hint", ""))
    if not hint or len(hint) > REMEDIATION_HINT_MAX:
        return False, "remediation_hint length invalid"

    ref = str(entry.get("work_item_ref", ""))
    if not ref or len(ref) > WORK_ITEM_REF_MAX:
        return False, "work_item_ref length invalid"

    for field_name in ("remediation_hint", "work_item_ref"):
        if scan_secrets(str(entry.get(field_name, ""))):
            return False, ReasonCode.SOVEREIGN_DEFERRAL_SCHEMA_INVALID.value

    return True, None


def schema_check_drain_generate_candidate(candidate: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    if not isinstance(candidate, dict):
        return False, "candidate must be object"
    title = str(candidate.get("title", ""))
    summary = str(candidate.get("summary", ""))
    if not title or len(title) > TITLE_MAX:
        return False, "title length invalid"
    if not summary or len(summary) > SUMMARY_MAX:
        return False, "summary length invalid"
    ac_sketch = candidate.get("ac_sketch", [])
    if not isinstance(ac_sketch, list) or len(ac_sketch) > AC_SKETCH_MAX_ITEMS:
        return False, "ac_sketch invalid"
    for item in ac_sketch:
        if len(str(item)) > AC_SKETCH_ITEM_MAX:
            return False, "ac_sketch item too long"
    provenance = candidate.get("provenance", "vision")
    if provenance not in PROVENANCE_VALUES:
        return False, "invalid provenance"
    return True, None


def schema_check_drain_generate_bundle(bundle: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    if not isinstance(bundle, dict):
        return False, "bundle must be object"
    if bundle.get("schema_version") != SCHEMA_VERSION:
        return False, "schema_version must be 1"
    candidates = bundle.get("candidates", [])
    if not isinstance(candidates, list):
        return False, "candidates must be list"
    if len(candidates) > MAX_CANDIDATES_PER_ITERATION:
        return False, "candidate cap exceeded"
    for candidate in candidates:
        ok, err = schema_check_drain_generate_candidate(candidate)
        if not ok:
            return False, err
    return True, None


def _read_deferral_rows(path: Path) -> List[Dict[str, Any]]:
    if not path.is_file():
        return []
    rows: List[Dict[str, Any]] = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            rows.append(obj)
    return rows


def list_open_deferrals(
    repo: Path,
    *,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    if scratchpad is not None and not is_sovereign_loop_enabled(scratchpad):
        return [], ReasonCode.SOVEREIGN_LOOP_DISABLED.value

    latest: Dict[str, Dict[str, Any]] = {}
    for row in _read_deferral_rows(resolve_deferrals_path(repo)):
        deferral_id = str(row.get("deferral_id", "")).strip()
        if not deferral_id:
            continue
        latest[deferral_id] = row

    open_rows = [
        row for row in latest.values()
        if str(row.get("state", "")).lower() == "open"
    ]
    open_rows.sort(key=lambda r: (str(r.get("ts", "")), str(r.get("deferral_id", ""))))
    return open_rows, None


def build_sample_deferral() -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "deferral_id": str(uuid.uuid4()),
        "ts": _utc_now_iso(),
        "reason_code": ReasonCode.DEPLOY_DEFERRED.value,
        "work_item_kind": "deploy",
        "work_item_ref": "release-target:staging",
        "state": "open",
        "source_orchestrator_run_id": "auto-research-stub",
        "remediation_hint": "Retry deploy smoke after US-0109 ships bounded repair loop.",
        "blocked_by_phase": "release",
        "retry_count": 0,
    }


@dataclass
class DrainGenerateCandidate:
    candidate_id: str
    title: str
    summary: str
    ac_sketch: List[str] = field(default_factory=list)
    plan_area_id: Optional[str] = None
    priority: str = "P2"
    provenance: str = "vision"


@dataclass
class DrainGenerateCandidateBundle:
    schema_version: int = SCHEMA_VERSION
    orchestrator_run_id: str = ""
    iteration: int = 0
    generated_at: str = ""
    candidates: List[DrainGenerateCandidate] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["candidates"] = [asdict(c) for c in self.candidates]
        return payload


@dataclass
class SovereignLoopStepResult:
    schema_version: int = SCHEMA_VERSION
    action: str = "noop"
    reason_code: Optional[str] = None
    stop_reason: Optional[str] = None
    orchestrator_run_id: str = ""
    evaluated_at: str = ""
    deferral_id: Optional[str] = None
    drain_generate_bundle: Optional[Dict[str, Any]] = None
    notification_dispatched: bool = False
    convergence: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def append_deferral(
    repo: Path,
    scratchpad: Dict[str, str],
    *,
    reason_code: str,
    work_item_kind: str,
    work_item_ref: str,
    source_orchestrator_run_id: str,
    remediation_hint: str,
    blocked_by_phase: Optional[str] = None,
    retry_count: Optional[int] = None,
    ledger_decision_id: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str]]:
    if not is_sovereign_loop_enabled(scratchpad):
        return None, ReasonCode.SOVEREIGN_LOOP_DISABLED.value

    cap = _scratchpad_int(scratchpad, AUTO_SOVEREIGN_DEFERRAL_MAX_KEY, AUTO_SOVEREIGN_DEFERRAL_MAX_DEFAULT)
    open_rows, _ = list_open_deferrals(repo, scratchpad=scratchpad)
    if len(open_rows) >= cap:
        return None, ReasonCode.SOVEREIGN_DEFERRAL_CAP_EXCEEDED.value

    entry: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "deferral_id": str(uuid.uuid4()),
        "ts": _utc_now_iso(),
        "reason_code": reason_code,
        "work_item_kind": work_item_kind,
        "work_item_ref": work_item_ref,
        "state": "open",
        "source_orchestrator_run_id": source_orchestrator_run_id,
        "remediation_hint": remediation_hint,
    }
    if blocked_by_phase:
        entry["blocked_by_phase"] = blocked_by_phase
    if retry_count is not None:
        entry["retry_count"] = retry_count
    if ledger_decision_id:
        entry["ledger_decision_id"] = ledger_decision_id

    ok, err = schema_check_deferral(entry)
    if not ok:
        return None, err or ReasonCode.SOVEREIGN_DEFERRAL_SCHEMA_INVALID.value

    path = resolve_deferrals_path(repo)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        return None, ReasonCode.SOVEREIGN_DEFERRAL_APPEND_FAILED.value

    return str(entry["deferral_id"]), None


def resolve_deferral(
    repo: Path,
    deferral_id: str,
    *,
    orchestrator_run_id: str,
) -> Tuple[bool, Optional[str]]:
    rows = _read_deferral_rows(resolve_deferrals_path(repo))
    latest = None
    for row in rows:
        if str(row.get("deferral_id", "")) == deferral_id:
            latest = row
    if latest is None:
        return False, "deferral_id not found"
    if str(latest.get("state", "")).lower() != "open":
        return False, "deferral not open"

    resolved = dict(latest)
    resolved["ts"] = _utc_now_iso()
    resolved["state"] = "resolved"
    resolved["source_orchestrator_run_id"] = orchestrator_run_id

    ok, err = schema_check_deferral(resolved)
    if not ok:
        return False, err

    path = resolve_deferrals_path(repo)
    try:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(resolved, ensure_ascii=False) + "\n")
    except OSError:
        return False, ReasonCode.SOVEREIGN_DEFERRAL_APPEND_FAILED.value
    return True, None


def _read_loop_state(repo: Path) -> Dict[str, Any]:
    state_path = repo / LOOP_STATE_PATH
    if not state_path.is_file():
        return {"schema_version": SCHEMA_VERSION, "drain_generate_iterations": {}}
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"schema_version": SCHEMA_VERSION, "drain_generate_iterations": {}}
    if not isinstance(data, dict):
        return {"schema_version": SCHEMA_VERSION, "drain_generate_iterations": {}}
    runs = data.get("drain_generate_iterations", {})
    if not isinstance(runs, dict):
        runs = {}
    return {"schema_version": SCHEMA_VERSION, "drain_generate_iterations": runs}


def _write_loop_state(repo: Path, state: Dict[str, Any]) -> None:
    state_path = repo / LOOP_STATE_PATH
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def count_drain_generate_iterations(repo: Path, orchestrator_run_id: str) -> int:
    runs = _read_loop_state(repo).get("drain_generate_iterations", {})
    try:
        return int(runs.get(orchestrator_run_id, 0))
    except (TypeError, ValueError):
        return 0


def increment_drain_generate_iterations(repo: Path, orchestrator_run_id: str) -> int:
    state = _read_loop_state(repo)
    runs = state.setdefault("drain_generate_iterations", {})
    current = count_drain_generate_iterations(repo, orchestrator_run_id)
    new_count = current + 1
    runs[orchestrator_run_id] = new_count
    _write_loop_state(repo, state)
    return new_count


def build_drain_generate_spawn_inputs(
    repo: Path,
    scratchpad: Dict[str, str],
    convergence: Any,
) -> Dict[str, Any]:
    goal = resolve_goal(scratchpad, repo)
    inputs: Dict[str, Any] = {
        "vision_path": "docs/product/vision.md",
        "unmet_conditions": getattr(convergence, "unmet_conditions", []),
        "blocked_by": getattr(convergence, "blocked_by", []),
        "goal_text": goal.goal_text or "",
    }
    if scratchpad.get("SOVEREIGN_MEMORY", "0").strip() == "1":
        try:
            from sovereign_memory_lib import build_injection_digest_block  # noqa: WPS433

            block = build_injection_digest_block(scratchpad=scratchpad, repo_root=repo)
            if block:
                inputs["sovereign_memory_digest"] = block
        except ImportError:
            inputs["sovereign_memory_digest"] = None
    return inputs


def build_drain_generate_ephemeral_id(orchestrator_run_id: str, iteration: int) -> str:
    return f"drain-gen-{orchestrator_run_id}-{iteration}"


def _build_notification_payload(
    *,
    event_type: str,
    orchestrator_run_id: str,
    reason_code: Optional[str],
    convergence: Any = None,
) -> Dict[str, Any]:
    goal_progress = None
    unmet: List[str] = []
    blocked: List[str] = []
    if convergence is not None:
        if hasattr(convergence, "to_dict"):
            goal_progress = convergence.to_dict()
            unmet = list(getattr(convergence, "unmet_conditions", []))
            blocked = list(getattr(convergence, "blocked_by", []))
        elif isinstance(convergence, dict):
            goal_progress = convergence
            unmet = list(convergence.get("unmet_conditions", []))
            blocked = list(convergence.get("blocked_by", []))
    return {
        "schema_version": SCHEMA_VERSION,
        "event_type": event_type,
        "ts": _utc_now_iso(),
        "orchestrator_run_id": orchestrator_run_id,
        "reason_code": reason_code,
        "unmet_conditions": unmet,
        "blocked_by": blocked,
        "goal_progress": goal_progress,
    }


def dispatch_notification(
    scratchpad: Dict[str, str],
    event_type: str,
    payload: Dict[str, Any],
) -> Tuple[bool, Optional[str]]:
    target = scratchpad.get(SOVEREIGN_NOTIFY_TARGET_KEY, SOVEREIGN_NOTIFY_TARGET_DEFAULT).strip().lower()
    if target == "off":
        return True, None
    if event_type not in NOTIFY_EVENT_VALUES:
        return False, ReasonCode.SOVEREIGN_NOTIFY_TARGET_INVALID.value
    if target == "email":
        return False, ReasonCode.SOVEREIGN_NOTIFY_TARGET_INVALID.value
    if target == "ntfy" and not scratchpad.get(SOVEREIGN_NOTIFY_NTFY_TOPIC_KEY, "").strip():
        return True, ReasonCode.SOVEREIGN_NOTIFY_CONFIG_MISSING.value
    if target == "hook" and not scratchpad.get(SOVEREIGN_NOTIFY_HOOK_URL_KEY, "").strip():
        return True, ReasonCode.SOVEREIGN_NOTIFY_CONFIG_MISSING.value

    try:
        if target == "ntfy":
            topic = scratchpad.get(SOVEREIGN_NOTIFY_NTFY_TOPIC_KEY, "").strip()
            base = scratchpad.get(SOVEREIGN_NOTIFY_NTFY_BASE_KEY, "").strip() or "https://ntfy.sh"
            url = f"{base.rstrip('/')}/{topic}"
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            req = urllib_request.Request(url, data=body, method="POST")
            req.add_header("Title", f"Sovereign {event_type}")
            priority = "4" if event_type in ("timeout", "deferral_cap", "drain_generate_cap") else "3"
            req.add_header("Priority", priority)
            req.add_header("Tags", "sovereign,auto")
            urllib_request.urlopen(req, timeout=10)
        elif target == "hook":
            hook_url = scratchpad.get(SOVEREIGN_NOTIFY_HOOK_URL_KEY, "").strip()
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            req = urllib_request.Request(hook_url, data=body, method="POST")
            req.add_header("Content-Type", "application/json")
            urllib_request.urlopen(req, timeout=10)
    except (OSError, urllib_error.URLError, urllib_error.HTTPError, ValueError):
        print(
            f"[{ReasonCode.SOVEREIGN_NOTIFY_DISPATCH_FAILED.value}] adapter error for {event_type}",
            file=sys.stderr,
        )
        return True, None

    return True, None


def advance_sovereign_loop(
    repo: Path,
    scratchpad: Dict[str, str],
    *,
    orchestrator_run_id: str,
    iteration: Optional[int] = None,
) -> SovereignLoopStepResult:
    evaluated_at = _utc_now_iso()
    if scratchpad.get(AUTO_SOVEREIGN_KEY, AUTO_SOVEREIGN_DEFAULT).strip() != "1":
        return SovereignLoopStepResult(
            action="noop",
            orchestrator_run_id=orchestrator_run_id,
            evaluated_at=evaluated_at,
        )

    if not is_goal_convergence_enabled(scratchpad):
        return SovereignLoopStepResult(
            action="blocked",
            reason_code=ReasonCode.SOVEREIGN_LOOP_GOAL_MODE_REQUIRED.value,
            stop_reason=ReasonCode.SOVEREIGN_LOOP_GOAL_MODE_REQUIRED.value,
            orchestrator_run_id=orchestrator_run_id,
            evaluated_at=evaluated_at,
        )

    iter_count = iteration if iteration is not None else 0
    convergence = evaluate_convergence(
        repo,
        scratchpad,
        orchestrator_run_id=orchestrator_run_id,
        iteration=iteration,
    )
    conv_dict = convergence.to_dict()

    if convergence.converged:
        payload = _build_notification_payload(
            event_type="convergence",
            orchestrator_run_id=orchestrator_run_id,
            reason_code="converged",
            convergence=convergence,
        )
        _, _ = dispatch_notification(scratchpad, "convergence", payload)
        return SovereignLoopStepResult(
            action="terminal_converged",
            stop_reason="converged",
            orchestrator_run_id=orchestrator_run_id,
            evaluated_at=evaluated_at,
            notification_dispatched=True,
            convergence=conv_dict,
        )

    timed_out, timeout_reason = check_timeout(scratchpad, iter_count)
    if timed_out and timeout_reason is not None:
        goal = resolve_goal(scratchpad, repo)
        write_partial_delivery_report(
            repo,
            convergence,
            goal.goal_text or "",
            timeout_reason.value,
            orchestrator_run_id,
        )
        payload = _build_notification_payload(
            event_type="timeout",
            orchestrator_run_id=orchestrator_run_id,
            reason_code=timeout_reason.value,
            convergence=convergence,
        )
        _, _ = dispatch_notification(scratchpad, "timeout", payload)
        return SovereignLoopStepResult(
            action="terminal_timeout",
            reason_code=timeout_reason.value,
            stop_reason=timeout_reason.value,
            orchestrator_run_id=orchestrator_run_id,
            evaluated_at=evaluated_at,
            notification_dispatched=True,
            convergence=conv_dict,
        )

    open_deferrals, _ = list_open_deferrals(repo, scratchpad=scratchpad)
    policy = scratchpad.get(
        AUTO_SOVEREIGN_DEFERRAL_POLICY_KEY,
        AUTO_SOVEREIGN_DEFERRAL_POLICY_DEFAULT,
    ).strip()

    deferral_cap = _scratchpad_int(
        scratchpad,
        AUTO_SOVEREIGN_DEFERRAL_MAX_KEY,
        AUTO_SOVEREIGN_DEFERRAL_MAX_DEFAULT,
    )
    if len(open_deferrals) >= deferral_cap:
        payload = _build_notification_payload(
            event_type="deferral_cap",
            orchestrator_run_id=orchestrator_run_id,
            reason_code=ReasonCode.SOVEREIGN_DEFERRAL_CAP_EXCEEDED.value,
            convergence=convergence,
        )
        _, _ = dispatch_notification(scratchpad, "deferral_cap", payload)
        return SovereignLoopStepResult(
            action="terminal_cap",
            reason_code=ReasonCode.SOVEREIGN_DEFERRAL_CAP_EXCEEDED.value,
            stop_reason=ReasonCode.SOVEREIGN_DEFERRAL_CAP_EXCEEDED.value,
            orchestrator_run_id=orchestrator_run_id,
            evaluated_at=evaluated_at,
            notification_dispatched=True,
            convergence=conv_dict,
        )

    if open_deferrals and policy == "stop":
        return SovereignLoopStepResult(
            action="defer",
            reason_code=ReasonCode.SOVEREIGN_LOOP_ADVANCE_BLOCKED.value,
            deferral_id=str(open_deferrals[0].get("deferral_id", "")),
            orchestrator_run_id=orchestrator_run_id,
            evaluated_at=evaluated_at,
            convergence=conv_dict,
        )

    if open_deferrals and policy == "resolve_first":
        return SovereignLoopStepResult(
            action="blocked",
            reason_code=ReasonCode.SOVEREIGN_LOOP_ADVANCE_BLOCKED.value,
            stop_reason=ReasonCode.SOVEREIGN_LOOP_ADVANCE_BLOCKED.value,
            orchestrator_run_id=orchestrator_run_id,
            evaluated_at=evaluated_at,
            convergence=conv_dict,
        )

    backlog_conj = convergence.conjuncts.get("backlog_clear")
    if backlog_conj and backlog_conj.status == "fail":
        return SovereignLoopStepResult(
            action="continue",
            orchestrator_run_id=orchestrator_run_id,
            evaluated_at=evaluated_at,
            convergence=conv_dict,
        )

    drain_max = _scratchpad_int(
        scratchpad,
        AUTO_SOVEREIGN_DRAIN_GENERATE_MAX_KEY,
        AUTO_SOVEREIGN_DRAIN_GENERATE_MAX_DEFAULT,
    )
    current_iter = count_drain_generate_iterations(repo, orchestrator_run_id)
    if current_iter < drain_max:
        new_iter = increment_drain_generate_iterations(repo, orchestrator_run_id)
        bundle = DrainGenerateCandidateBundle(
            orchestrator_run_id=orchestrator_run_id,
            iteration=new_iter,
            generated_at=evaluated_at,
            candidates=[],
        )
        return SovereignLoopStepResult(
            action="drain_generate",
            orchestrator_run_id=orchestrator_run_id,
            evaluated_at=evaluated_at,
            drain_generate_bundle=bundle.to_dict(),
            convergence=conv_dict,
        )

    payload = _build_notification_payload(
        event_type="drain_generate_cap",
        orchestrator_run_id=orchestrator_run_id,
        reason_code=ReasonCode.SOVEREIGN_DRAIN_GENERATE_CAP.value,
        convergence=convergence,
    )
    _, _ = dispatch_notification(scratchpad, "drain_generate_cap", payload)
    return SovereignLoopStepResult(
        action="terminal_cap",
        reason_code=ReasonCode.SOVEREIGN_DRAIN_GENERATE_CAP.value,
        stop_reason=ReasonCode.SOVEREIGN_DRAIN_GENERATE_CAP.value,
        orchestrator_run_id=orchestrator_run_id,
        evaluated_at=evaluated_at,
        notification_dispatched=True,
        convergence=conv_dict,
    )


def self_test() -> bool:
    errors: List[str] = []

    if is_sovereign_loop_enabled({AUTO_SOVEREIGN_KEY: "0", SOVEREIGN_GOAL_MODE_KEY: "goal_convergence"}):
        errors.append("AUTO_SOVEREIGN=0 must disable even with goal_convergence")

    if not is_sovereign_loop_enabled({AUTO_SOVEREIGN_KEY: "1", SOVEREIGN_GOAL_MODE_KEY: "goal_convergence"}):
        errors.append("AUTO_SOVEREIGN=1 + goal_convergence must enable")

    if is_sovereign_loop_enabled({AUTO_SOVEREIGN_KEY: "1", SOVEREIGN_GOAL_MODE_KEY: "phase_driven"}):
        errors.append("phase_driven must fail-closed for sovereign loop")

    sample = build_sample_deferral()
    ok, err = schema_check_deferral(sample)
    if not ok:
        errors.append(f"sample deferral invalid: {err}")

    bad_secret = build_sample_deferral()
    bad_secret["remediation_hint"] = "api_key=leaked"
    bad_ok, bad_err = schema_check_deferral(bad_secret)
    if bad_ok:
        errors.append("secret scan must reject api_key patterns")

    step = advance_sovereign_loop(
        Path("."),
        {AUTO_SOVEREIGN_KEY: "0"},
        orchestrator_run_id="self-test",
    )
    if step.action != "noop":
        errors.append("disabled advance must noop")

    blocked = advance_sovereign_loop(
        Path("."),
        {AUTO_SOVEREIGN_KEY: "1", SOVEREIGN_GOAL_MODE_KEY: "phase_driven"},
        orchestrator_run_id="self-test",
    )
    if blocked.action != "blocked" or blocked.reason_code != ReasonCode.SOVEREIGN_LOOP_GOAL_MODE_REQUIRED.value:
        errors.append("goal mode coupling must fail-closed")

    notify_ok, _ = dispatch_notification(
        {SOVEREIGN_NOTIFY_TARGET_KEY: "off"},
        "convergence",
        {"schema_version": 1},
    )
    if not notify_ok:
        errors.append("off target must fail-open success")

    email_ok, email_code = dispatch_notification(
        {SOVEREIGN_NOTIFY_TARGET_KEY: "email"},
        "convergence",
        {"schema_version": 1},
    )
    if email_ok or email_code != ReasonCode.SOVEREIGN_NOTIFY_TARGET_INVALID.value:
        errors.append("email target must return SOVEREIGN_NOTIFY_TARGET_INVALID")

    bundle = DrainGenerateCandidateBundle(
        orchestrator_run_id="self-test",
        iteration=1,
        generated_at=_utc_now_iso(),
        candidates=[
            DrainGenerateCandidate(
                candidate_id=str(uuid.uuid4()),
                title="Example follow-on story",
                summary="Bounded drain-generate candidate for self-test.",
                ac_sketch=["AC-1: example"],
            ),
        ],
    )
    bundle_ok, bundle_err = schema_check_drain_generate_bundle(bundle.to_dict())
    if not bundle_ok:
        errors.append(f"bundle schema failed: {bundle_err}")

    if len(REASON_CODES) != 12:
        errors.append("reason code inventory must be 12 codes")

    if errors:
        for msg in errors:
            print(f"[SOVEREIGN_LOOP_SELF_TEST_FAIL] {msg}", file=sys.stderr)
        return False

    print("[SOVEREIGN_LOOP_SELF_TEST_OK]")
    return True


if __name__ == "__main__":
    raise SystemExit(0 if self_test() else 1)
