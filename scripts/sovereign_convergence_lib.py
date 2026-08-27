#!/usr/bin/env python3
"""
Goal-based convergence helper library (US-0110 / DEC-0110).

Reason codes (DEC-0110 §10):
  CONVERGENCE_OPEN_STORIES_REMAIN, CONVERGENCE_DEFERRALS_PENDING,
  CONVERGENCE_CROSS_REVIEWER_OPEN, CONVERGENCE_SMOKE_PROBE_FAIL,
  CONVERGENCE_LEDGER_EXTENSIONS_UNAPPROVED, SOVEREIGN_GOAL_TIMEOUT,
  SOVEREIGN_GOAL_MODE_INVALID, SOVEREIGN_GOAL_MISSING,
  SOVEREIGN_GOAL_DERIVE_FAILED, CONVERGENCE_EVAL_FAILED

US-0128 additive (not in the DEC-0110 §10 inventory of 10):
  CONVERGENCE_SMOKE_SURROGATE_MISSING

Default-off: SOVEREIGN_GOAL_MODE=phase_driven → zero overhead.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from decision_ledger_lib import (  # noqa: E402
    ReasonCode as LedgerReasonCode,
    is_ledger_enabled,
    read_entries,
    resolve_ledger_path,
)
from sovereign_critic_lib import read_open_blocking  # noqa: E402


# --- Scratchpad key contracts (DEC-0110 §1) -----------------------------------

SOVEREIGN_GOAL_MODE_KEY = "SOVEREIGN_GOAL_MODE"
SOVEREIGN_GOAL_KEY = "SOVEREIGN_GOAL"
SOVEREIGN_GOAL_TOP_N_KEY = "SOVEREIGN_GOAL_TOP_N"
SOVEREIGN_GOAL_MAX_CHARS_KEY = "SOVEREIGN_GOAL_MAX_CHARS"
SOVEREIGN_GOAL_TIMEOUT_MAX_KEY = "SOVEREIGN_GOAL_TIMEOUT_MAX"

SOVEREIGN_GOAL_MODE_VALUES = frozenset({"phase_driven", "goal_convergence"})
SOVEREIGN_GOAL_MODE_DEFAULT = "phase_driven"
SOVEREIGN_GOAL_TOP_N_DEFAULT = 3
SOVEREIGN_GOAL_MAX_CHARS_DEFAULT = 512
SOVEREIGN_GOAL_TIMEOUT_MAX_DEFAULT = 0

CONVERGENCE_CONJUNCTS = (
    "backlog_clear",
    "zero_deferrals",
    "critic_resolved",
    "smoke_green",
    "ledger_clean",
)

CONJUNCT_STATUS_VALUES = frozenset({"pass", "fail", "skip"})
GOAL_SOURCE_VALUES = frozenset({"explicit", "vision_derived"})
SCHEMA_VERSION = 1

VISION_PATH = Path("docs/product/vision.md")
BACKLOG_PATH = Path("docs/product/backlog.md")
DEFERRALS_PATH = Path("handoffs/sovereign_deferrals.jsonl")
CRITIC_PATH = Path("handoffs/sovereign_critic_findings.jsonl")
REPORT_PATH = Path("tests/report.md")
PARTIAL_DELIVERY_PATH = Path("handoffs/sovereign_partial_delivery.md")
RESUME_BRIEF_PATH = Path("handoffs/resume_brief.md")
SPRINTS_DIR = Path("sprints")

_SKIP_SECTION_RE = re.compile(r"^## (Discovery Notes —|Intake Notes —)")
_HEADING_RE = re.compile(r"^#{1,6}\s")
_LIST_RE = re.compile(r"^(\s*[-*+]|\s*\d+\.)\s")
_BLOCKQUOTE_RE = re.compile(r"^>\s?")
_US_STORY_RE = re.compile(r"^## (US-\d{4})\b")
_STATUS_OPEN_RE = re.compile(r"^-\s+Status:\s+OPEN\b")
_STATUS_DONE_RE = re.compile(r"^-\s+Status:\s+DONE\b")
_SPRINT_ID_RE = re.compile(r"\b(S\d{4})\b")

_EVAL_CACHE: Dict[str, ConvergenceResult] = {}


class ReasonCode(str, Enum):
    CONVERGENCE_OPEN_STORIES_REMAIN = "CONVERGENCE_OPEN_STORIES_REMAIN"
    CONVERGENCE_DEFERRALS_PENDING = "CONVERGENCE_DEFERRALS_PENDING"
    CONVERGENCE_CROSS_REVIEWER_OPEN = "CONVERGENCE_CROSS_REVIEWER_OPEN"
    CONVERGENCE_SMOKE_PROBE_FAIL = "CONVERGENCE_SMOKE_PROBE_FAIL"
    CONVERGENCE_LEDGER_EXTENSIONS_UNAPPROVED = "CONVERGENCE_LEDGER_EXTENSIONS_UNAPPROVED"
    SOVEREIGN_GOAL_TIMEOUT = "SOVEREIGN_GOAL_TIMEOUT"
    SOVEREIGN_GOAL_MODE_INVALID = "SOVEREIGN_GOAL_MODE_INVALID"
    SOVEREIGN_GOAL_MISSING = "SOVEREIGN_GOAL_MISSING"
    SOVEREIGN_GOAL_DERIVE_FAILED = "SOVEREIGN_GOAL_DERIVE_FAILED"
    CONVERGENCE_EVAL_FAILED = "CONVERGENCE_EVAL_FAILED"


REASON_CODES = frozenset(code.value for code in ReasonCode)

# US-0128 additive fail-closed code — not part of DEC-0110 §10 REASON_CODES (must remain 10).
CONVERGENCE_SMOKE_SURROGATE_MISSING = "CONVERGENCE_SMOKE_SURROGATE_MISSING"

_CANONICAL_LIVE_RUNTIME_PROBE_CLASSES = frozenset(
    {
        "browser_smoke",
        "api_health",
        "process_health",
        "cli_smoke",
        "build",
        "manual_operator",
    }
)
_SMOKE_PASS_RESULTS = frozenset({"pass", "passed", "ok"})
_SURROGATE_WAIVER_REASON = "UAT_PROBE_FORBIDDEN"

_UNAPPROVED_LEDGER_TYPES = frozenset({
    "PLAN_FIDELITY_EXTENSION",
    "PLAN_FIDELITY_SCOPE_GATE",
})


@dataclass
class GoalResolveResult:
    goal_text: Optional[str]
    goal_source: Optional[str]
    reason_code: Optional[ReasonCode]


@dataclass
class ConjunctResult:
    name: str
    status: str
    reason_code: Optional[str] = None
    skipped: bool = False


@dataclass
class ConvergenceResult:
    converged: bool
    unmet_conditions: List[str] = field(default_factory=list)
    blocked_by: List[str] = field(default_factory=list)
    conjuncts: Dict[str, ConjunctResult] = field(default_factory=dict)
    evaluated_at: str = ""
    orchestrator_run_id: Optional[str] = None
    cache_key: Optional[str] = None
    schema_version: int = SCHEMA_VERSION

    def to_dict(self) -> dict:
        return {
            "converged": self.converged,
            "unmet_conditions": list(self.unmet_conditions),
            "blocked_by": list(self.blocked_by),
            "conjuncts": {
                name: {
                    "status": c.status,
                    "reason_code": c.reason_code,
                    "skipped": c.skipped,
                }
                for name, c in self.conjuncts.items()
            },
            "evaluated_at": self.evaluated_at,
            "orchestrator_run_id": self.orchestrator_run_id,
            "cache_key": self.cache_key,
            "schema_version": self.schema_version,
        }


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def parse_scratchpad(scratchpad: Dict[str, str]) -> Dict[str, str]:
    """Normalize scratchpad dict access."""
    return {k: str(v).strip() for k, v in scratchpad.items()}


def is_goal_convergence_enabled(scratchpad: Dict[str, str]) -> bool:
    sp = parse_scratchpad(scratchpad)
    return sp.get(SOVEREIGN_GOAL_MODE_KEY, SOVEREIGN_GOAL_MODE_DEFAULT) == "goal_convergence"


def clear_eval_cache() -> None:
    """Test helper — invalidate memoization cache."""
    _EVAL_CACHE.clear()


def _mtime_ns(path: Path) -> int:
    if path.is_file():
        return path.stat().st_mtime_ns
    return 0


def _resolve_active_uat_path(repo: Path) -> Optional[Path]:
    brief = repo / RESUME_BRIEF_PATH
    if brief.is_file():
        text = brief.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines()[:40]:
            m = _SPRINT_ID_RE.search(line)
            if m:
                candidate = repo / SPRINTS_DIR / m.group(1) / "uat.json"
                if candidate.is_file():
                    return candidate
    sprints_root = repo / SPRINTS_DIR
    if not sprints_root.is_dir():
        return None
    candidates = sorted(
        sprints_root.glob("S*/uat.json"),
        key=lambda p: p.stat().st_mtime_ns,
        reverse=True,
    )
    return candidates[0] if candidates else None


def _build_cache_key(
    repo: Path,
    scratchpad: Dict[str, str],
    orchestrator_run_id: Optional[str],
) -> str:
    backlog = repo / BACKLOG_PATH
    deferrals = repo / DEFERRALS_PATH
    critic = repo / CRITIC_PATH
    report = repo / REPORT_PATH
    uat = _resolve_active_uat_path(repo)
    ledger = Path("0")
    if orchestrator_run_id and is_ledger_enabled(scratchpad):
        ledger = resolve_ledger_path(orchestrator_run_id, repo)
    uat_mtime = _mtime_ns(uat) if uat else 0
    return (
        f"{_mtime_ns(backlog)}:{_mtime_ns(deferrals)}:{_mtime_ns(critic)}:"
        f"{_mtime_ns(report)}:{uat_mtime}:{_mtime_ns(ledger)}"
    )


def _scan_story_statuses(backlog_path: Path) -> Tuple[List[str], List[str]]:
    open_stories: List[str] = []
    done_stories: List[str] = []
    if not backlog_path.is_file():
        return open_stories, done_stories
    current_us: Optional[str] = None
    for line in backlog_path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = _US_STORY_RE.match(line)
        if m:
            current_us = m.group(1)
            continue
        if current_us is None:
            continue
        if line.startswith("## ") and not _US_STORY_RE.match(line):
            current_us = None
            continue
        if _STATUS_OPEN_RE.match(line):
            open_stories.append(current_us)
        elif _STATUS_DONE_RE.match(line):
            done_stories.append(current_us)
    return open_stories, done_stories


def _eval_backlog_clear(repo: Path) -> ConjunctResult:
    backlog = repo / BACKLOG_PATH
    if not backlog.is_file():
        return ConjunctResult(
            name="backlog_clear",
            status="fail",
            reason_code=ReasonCode.CONVERGENCE_EVAL_FAILED.value,
            skipped=False,
        )
    open_stories, _ = _scan_story_statuses(backlog)
    if open_stories:
        return ConjunctResult(
            name="backlog_clear",
            status="fail",
            reason_code=ReasonCode.CONVERGENCE_OPEN_STORIES_REMAIN.value,
            skipped=False,
        )
    return ConjunctResult(name="backlog_clear", status="pass", reason_code=None, skipped=False)


def _eval_zero_deferrals(
    repo: Path,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Tuple[ConjunctResult, Optional[str]]:
    if scratchpad is not None:
        try:
            from sovereign_loop_lib import is_sovereign_loop_enabled, list_open_deferrals

            if is_sovereign_loop_enabled(scratchpad):
                open_rows, _ = list_open_deferrals(repo, scratchpad=scratchpad)
                if open_rows:
                    return (
                        ConjunctResult(
                            name="zero_deferrals",
                            status="fail",
                            reason_code=ReasonCode.CONVERGENCE_DEFERRALS_PENDING.value,
                            skipped=False,
                        ),
                        None,
                    )
                return (
                    ConjunctResult(
                        name="zero_deferrals",
                        status="pass",
                        reason_code=None,
                        skipped=False,
                    ),
                    None,
                )
        except ImportError:
            pass

    path = repo / DEFERRALS_PATH
    if not path.is_file():
        return (
            ConjunctResult(
                name="zero_deferrals",
                status="skip",
                reason_code=None,
                skipped=True,
            ),
            "deferral_register_not_yet_deployed",
        )
    lines = [ln for ln in path.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()]
    if lines:
        return (
            ConjunctResult(
                name="zero_deferrals",
                status="fail",
                reason_code=ReasonCode.CONVERGENCE_DEFERRALS_PENDING.value,
                skipped=False,
            ),
            None,
        )
    return ConjunctResult(name="zero_deferrals", status="pass", reason_code=None, skipped=False), None


def _jsonl_file_nonempty(path: Path) -> bool:
    """True when findings JSONL exists and has at least one non-blank line (US-0127 DQ6)."""
    if not path.is_file():
        return False
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if raw.strip():
            return True
    return False


def _critic_jsonl_has_open(repo: Path) -> bool:
    """Blocking-only open check — delegates to US-0104 read_open_blocking (US-0127 AC-1).

    Do not redefine read_open_blocking. Informational status=open, blocking=false rows
    must not fail CONVERGENCE_CROSS_REVIEWER_OPEN.
    """
    return bool(read_open_blocking(repo))


def _qa_findings_has_open_critic(repo: Path) -> bool:
    sprints_root = repo / SPRINTS_DIR
    if not sprints_root.is_dir():
        return False
    qa_files = sorted(
        sprints_root.glob("S*/qa-findings.md"),
        key=lambda p: p.stat().st_mtime_ns,
        reverse=True,
    )
    for qa_path in qa_files:
        text = qa_path.read_text(encoding="utf-8", errors="replace")
        if "cross_reviewer_findings" not in text.lower():
            continue
        in_section = False
        for line in text.splitlines():
            lower = line.lower()
            if "cross_reviewer_findings" in lower and line.startswith("#"):
                in_section = True
                continue
            if in_section and line.startswith("#"):
                break
            if in_section and re.search(r"\b(open|blocking|fail|critical)\b", lower):
                if "none" not in lower and "no open" not in lower and "0 open" not in lower:
                    return True
        return False
    return False


def _qa_has_cross_reviewer_section(repo: Path) -> bool:
    sprints_root = repo / SPRINTS_DIR
    if not sprints_root.is_dir():
        return False
    for qa_path in sprints_root.glob("S*/qa-findings.md"):
        if "cross_reviewer_findings" in qa_path.read_text(encoding="utf-8", errors="replace").lower():
            return True
    return False


def _eval_critic_resolved(repo: Path) -> Tuple[ConjunctResult, Optional[str]]:
    """US-0110 L3 conjunct-3 with US-0127 DQ6 dispatch.

    When handoffs/sovereign_critic_findings.jsonl exists and is non-empty, the JSONL
    blocking-only predicate is authoritative and _qa_findings_has_open_critic is NOT
    consulted. When JSONL is absent, fall back to the unchanged QA-markdown grep.
    When neither is deployed, informational skip (US-0110 L3 degrade matrix).
    """
    critic_path = repo / CRITIC_PATH
    jsonl_authoritative = _jsonl_file_nonempty(critic_path)
    has_qa_section = _qa_has_cross_reviewer_section(repo)

    if jsonl_authoritative:
        if _critic_jsonl_has_open(repo):
            return (
                ConjunctResult(
                    name="critic_resolved",
                    status="fail",
                    reason_code=ReasonCode.CONVERGENCE_CROSS_REVIEWER_OPEN.value,
                    skipped=False,
                ),
                None,
            )
        return ConjunctResult(name="critic_resolved", status="pass", reason_code=None, skipped=False), None

    if has_qa_section:
        if _qa_findings_has_open_critic(repo):
            return (
                ConjunctResult(
                    name="critic_resolved",
                    status="fail",
                    reason_code=ReasonCode.CONVERGENCE_CROSS_REVIEWER_OPEN.value,
                    skipped=False,
                ),
                None,
            )
        return ConjunctResult(name="critic_resolved", status="pass", reason_code=None, skipped=False), None

    return (
        ConjunctResult(
            name="critic_resolved",
            status="skip",
            reason_code=None,
            skipped=True,
        ),
        "critic_register_not_yet_deployed",
    )


def _report_passes(report_path: Path) -> bool:
    if not report_path.is_file():
        return False
    head = report_path.read_text(encoding="utf-8", errors="replace")[:2000]
    m = re.search(r"^Fail:\s*(\d+)", head, re.MULTILINE)
    if m:
        return int(m.group(1)) == 0
    return "Fail: 0" in head or re.search(r"Overall:\s*PASS", head, re.IGNORECASE) is not None


def _step_is_smoke(step: dict) -> bool:
    for key in ("probe_kind", "probe_type", "id", "expected"):
        val = str(step.get(key, "")).lower()
        if "smoke" in val:
            return True
    return False


def _uat_smoke_passes(uat_path: Path) -> bool:
    if not uat_path.is_file():
        return False
    try:
        data = json.loads(uat_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    steps = data.get("steps") or []
    smoke_steps = [s for s in steps if isinstance(s, dict) and _step_is_smoke(s)]
    if not smoke_steps:
        return False
    latest = smoke_steps[-1]
    result = str(latest.get("result", "")).lower()
    return result in ("pass", "passed", "ok")


def _load_uat_data(uat_path: Optional[Path]) -> Optional[dict]:
    if uat_path is None or not uat_path.is_file():
        return None
    try:
        data = json.loads(uat_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def _uat_has_smoke_step(data: dict) -> bool:
    steps = data.get("steps") or []
    return any(isinstance(s, dict) and _step_is_smoke(s) for s in steps)


def _all_six_live_runtime_probes_waived(data: dict) -> bool:
    waived = data.get("waived_probes") or []
    present = set()
    for row in waived:
        if not isinstance(row, dict):
            continue
        if str(row.get("reason_code", "")) != _SURROGATE_WAIVER_REASON:
            continue
        cls = str(row.get("probe_class", "")).strip()
        if cls:
            present.add(cls)
    return _CANONICAL_LIVE_RUNTIME_PROBE_CLASSES.issubset(present)


def _contract_test_failed_count(data: dict) -> Optional[int]:
    if "contract_test_failed" in data:
        try:
            return int(data.get("contract_test_failed"))
        except (TypeError, ValueError):
            return None
    passed = data.get("contract_test_passed")
    total = data.get("contract_test_total")
    if passed is None or total is None:
        return None
    try:
        p = int(passed)
        t = int(total)
    except (TypeError, ValueError):
        return None
    return 0 if p == t else max(0, t - p)


def _surrogate_step_passes(data: dict) -> bool:
    steps = [s for s in (data.get("steps") or []) if isinstance(s, dict)]
    for step in steps:
        if str(step.get("id", "")) == "convergence_smoke":
            return str(step.get("result", "")).lower() in _SMOKE_PASS_RESULTS
    if not steps:
        return False
    tail = steps[-1]
    if str(tail.get("probe_kind", "")) == "contract_tests_primary":
        return str(tail.get("result", "")).lower() in _SMOKE_PASS_RESULTS
    return False


def _eval_smoke_green(repo: Path) -> ConjunctResult:
    report_ok = _report_passes(repo / REPORT_PATH)
    uat = _resolve_active_uat_path(repo)
    # Legacy path first (US-0128 critic NB / R6): real smoke-named step wins.
    uat_ok = _uat_smoke_passes(uat) if uat else False
    if report_ok and uat_ok:
        return ConjunctResult(name="smoke_green", status="pass", reason_code=None, skipped=False)

    data = _load_uat_data(uat)
    if data is not None and _uat_has_smoke_step(data):
        return ConjunctResult(
            name="smoke_green",
            status="fail",
            reason_code=ReasonCode.CONVERGENCE_SMOKE_PROBE_FAIL.value,
            skipped=False,
        )

    failed_count = _contract_test_failed_count(data) if data is not None else None
    surrogate_ok = (
        report_ok
        and data is not None
        and _all_six_live_runtime_probes_waived(data)
        and failed_count == 0
        and _surrogate_step_passes(data)
    )
    if surrogate_ok:
        return ConjunctResult(name="smoke_green", status="pass", reason_code=None, skipped=False)
    return ConjunctResult(
        name="smoke_green",
        status="fail",
        reason_code=CONVERGENCE_SMOKE_SURROGATE_MISSING,
        skipped=False,
    )


def _ledger_has_unapproved(entries: List[dict]) -> bool:
    pending = 0
    for entry in entries:
        dt = entry.get("decision_type")
        if dt in _UNAPPROVED_LEDGER_TYPES:
            pending += 1
        elif dt == "PLAN_FIDELITY_OVERRIDE":
            pending = max(0, pending - 1)
    return pending > 0


def _eval_ledger_clean(
    repo: Path,
    scratchpad: Dict[str, str],
    orchestrator_run_id: Optional[str],
) -> Tuple[ConjunctResult, Optional[str]]:
    if not is_ledger_enabled(scratchpad):
        return (
            ConjunctResult(
                name="ledger_clean",
                status="skip",
                reason_code=None,
                skipped=True,
            ),
            "ledger_disabled_skip",
        )
    if not orchestrator_run_id:
        return (
            ConjunctResult(
                name="ledger_clean",
                status="fail",
                reason_code=ReasonCode.CONVERGENCE_EVAL_FAILED.value,
                skipped=False,
            ),
            None,
        )
    ledger_path = resolve_ledger_path(orchestrator_run_id, repo)
    entries, reason, _ = read_entries(ledger_path, last_n=100, strict=False)
    if reason == LedgerReasonCode.LEDGER_FILE_MISSING:
        return ConjunctResult(name="ledger_clean", status="pass", reason_code=None, skipped=False), None
    if _ledger_has_unapproved(entries):
        return (
            ConjunctResult(
                name="ledger_clean",
                status="fail",
                reason_code=ReasonCode.CONVERGENCE_LEDGER_EXTENSIONS_UNAPPROVED.value,
                skipped=False,
            ),
            None,
        )
    return ConjunctResult(name="ledger_clean", status="pass", reason_code=None, skipped=False), None


def evaluate_convergence(
    repo: Path,
    scratchpad: Dict[str, str],
    *,
    orchestrator_run_id: Optional[str] = None,
    iteration: Optional[int] = None,
) -> ConvergenceResult:
    """Five-conjunct convergence predicate with mtime memoization (DEC-0110 §4)."""
    sp = parse_scratchpad(scratchpad)
    mode = sp.get(SOVEREIGN_GOAL_MODE_KEY, SOVEREIGN_GOAL_MODE_DEFAULT)
    if mode not in SOVEREIGN_GOAL_MODE_VALUES:
        return ConvergenceResult(
            converged=False,
            unmet_conditions=["invalid_sovereign_goal_mode"],
            blocked_by=[ReasonCode.SOVEREIGN_GOAL_MODE_INVALID.value],
            conjuncts={
                name: ConjunctResult(name=name, status="skip", skipped=True)
                for name in CONVERGENCE_CONJUNCTS
            },
            evaluated_at=_utc_now_iso(),
            orchestrator_run_id=orchestrator_run_id,
        )

    if not is_goal_convergence_enabled(scratchpad):
        return ConvergenceResult(
            converged=False,
            unmet_conditions=["goal_convergence_mode_disabled"],
            blocked_by=[],
            conjuncts={
                name: ConjunctResult(name=name, status="skip", skipped=True)
                for name in CONVERGENCE_CONJUNCTS
            },
            evaluated_at=_utc_now_iso(),
            orchestrator_run_id=orchestrator_run_id,
        )

    cache_key = _build_cache_key(repo, scratchpad, orchestrator_run_id)
    if cache_key in _EVAL_CACHE:
        cached = _EVAL_CACHE[cache_key]
        cached.orchestrator_run_id = orchestrator_run_id
        return cached

    unmet: List[str] = []
    blocked: List[str] = []
    conjuncts: Dict[str, ConjunctResult] = {}

    try:
        c1 = _eval_backlog_clear(repo)
        conjuncts["backlog_clear"] = c1
        if c1.status == "fail" and c1.reason_code:
            blocked.append(c1.reason_code)
            unmet.append("backlog has open stories")

        c2, skip_note = _eval_zero_deferrals(repo, scratchpad)
        conjuncts["zero_deferrals"] = c2
        if skip_note:
            unmet.append(skip_note)
        elif c2.status == "fail" and c2.reason_code:
            blocked.append(c2.reason_code)
            unmet.append("deferrals pending")

        c3, skip_note = _eval_critic_resolved(repo)
        conjuncts["critic_resolved"] = c3
        if skip_note:
            unmet.append(skip_note)
        elif c3.status == "fail" and c3.reason_code:
            blocked.append(c3.reason_code)
            unmet.append("cross-reviewer findings open")

        c4 = _eval_smoke_green(repo)
        conjuncts["smoke_green"] = c4
        if c4.status == "fail" and c4.reason_code:
            blocked.append(c4.reason_code)
            unmet.append("smoke probe not green")

        c5, skip_note = _eval_ledger_clean(repo, scratchpad, orchestrator_run_id)
        conjuncts["ledger_clean"] = c5
        if skip_note:
            unmet.append(skip_note)
        elif c5.status == "fail" and c5.reason_code:
            blocked.append(c5.reason_code)
            unmet.append("ledger has unapproved extensions")

        active_conjuncts = [c for c in conjuncts.values() if not c.skipped]
        converged = bool(active_conjuncts) and all(c.status == "pass" for c in active_conjuncts)

        result = ConvergenceResult(
            converged=converged,
            unmet_conditions=unmet,
            blocked_by=blocked,
            conjuncts=conjuncts,
            evaluated_at=_utc_now_iso(),
            orchestrator_run_id=orchestrator_run_id,
            cache_key=cache_key,
        )
        _EVAL_CACHE[cache_key] = result
        return result
    except Exception:
        return ConvergenceResult(
            converged=False,
            unmet_conditions=["evaluator_internal_error"],
            blocked_by=[ReasonCode.CONVERGENCE_EVAL_FAILED.value],
            conjuncts={
                name: ConjunctResult(name=name, status="skip", skipped=True)
                for name in CONVERGENCE_CONJUNCTS
            },
            evaluated_at=_utc_now_iso(),
            orchestrator_run_id=orchestrator_run_id,
        )


def _truncate_goal(text: str, max_chars: int) -> str:
    text = " ".join(text.split())
    if len(text) <= max_chars:
        return text
    cut = text[: max_chars - 1]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut + "…"


def _eligible_vision_paragraphs(lines: List[str]) -> List[str]:
    paragraphs: List[str] = []
    current: List[str] = []
    in_skip_section = False
    in_code_fence = False

    def flush() -> None:
        nonlocal current
        if current:
            paragraphs.append(" ".join(current))
            current = []

    for line in lines:
        stripped = line.rstrip("\n")
        if stripped.strip().startswith("```"):
            flush()
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue
        if _SKIP_SECTION_RE.match(stripped):
            flush()
            in_skip_section = True
            continue
        if in_skip_section:
            if _HEADING_RE.match(stripped) and not _SKIP_SECTION_RE.match(stripped):
                in_skip_section = False
            else:
                continue
        if (
            not stripped.strip()
            or _HEADING_RE.match(stripped)
            or _LIST_RE.match(stripped)
            or _BLOCKQUOTE_RE.match(stripped)
            or stripped.strip().startswith("<!--")
        ):
            flush()
            continue
        current.append(stripped.strip())

    flush()
    return paragraphs


def resolve_goal(scratchpad: Dict[str, str], repo: Path) -> GoalResolveResult:
    sp = parse_scratchpad(scratchpad)
    mode = sp.get(SOVEREIGN_GOAL_MODE_KEY, SOVEREIGN_GOAL_MODE_DEFAULT)
    if mode not in SOVEREIGN_GOAL_MODE_VALUES:
        return GoalResolveResult(None, None, ReasonCode.SOVEREIGN_GOAL_MODE_INVALID)

    explicit = sp.get(SOVEREIGN_GOAL_KEY, "").strip()
    max_chars = int(sp.get(SOVEREIGN_GOAL_MAX_CHARS_KEY, SOVEREIGN_GOAL_MAX_CHARS_DEFAULT))

    if explicit:
        return GoalResolveResult(_truncate_goal(explicit, max_chars), "explicit", None)

    top_n = int(sp.get(SOVEREIGN_GOAL_TOP_N_KEY, SOVEREIGN_GOAL_TOP_N_DEFAULT))
    vision_file = repo / VISION_PATH
    if not vision_file.is_file():
        return GoalResolveResult(None, None, ReasonCode.SOVEREIGN_GOAL_DERIVE_FAILED)

    try:
        lines = vision_file.read_text(encoding="utf-8").splitlines(keepends=True)
    except OSError:
        return GoalResolveResult(None, None, ReasonCode.SOVEREIGN_GOAL_DERIVE_FAILED)

    eligible = _eligible_vision_paragraphs(lines)
    if not eligible:
        return GoalResolveResult(None, None, ReasonCode.SOVEREIGN_GOAL_DERIVE_FAILED)

    joined = " — ".join(eligible[:top_n])
    return GoalResolveResult(_truncate_goal(joined, max_chars), "vision_derived", None)


def schema_check_convergence_result(obj: Any) -> Tuple[bool, Optional[str]]:
    if not isinstance(obj, dict):
        return False, "root must be object"
    required = {
        "converged": bool,
        "unmet_conditions": list,
        "blocked_by": list,
        "conjuncts": dict,
        "evaluated_at": str,
        "schema_version": int,
    }
    for key, typ in required.items():
        if key not in obj:
            return False, f"missing field: {key}"
        if not isinstance(obj[key], typ):
            return False, f"field {key} wrong type"
    if obj["schema_version"] != SCHEMA_VERSION:
        return False, "schema_version must be 1"
    for name in CONVERGENCE_CONJUNCTS:
        if name not in obj["conjuncts"]:
            return False, f"missing conjunct: {name}"
        c = obj["conjuncts"][name]
        if not isinstance(c, dict):
            return False, f"conjunct {name} must be object"
        if c.get("status") not in CONJUNCT_STATUS_VALUES:
            return False, f"conjunct {name} invalid status"
        if not isinstance(c.get("skipped"), bool):
            return False, f"conjunct {name} skipped must be bool"
    return True, None


def schema_check_goal_progress(obj: Any) -> Tuple[bool, Optional[str]]:
    if not isinstance(obj, dict):
        return False, "root must be object"
    if "goal_progress" not in obj:
        return False, "missing goal_progress wrapper"
    gp = obj["goal_progress"]
    if not isinstance(gp, dict):
        return False, "goal_progress must be object"
    required_str = ("goal_text", "goal_source", "mode", "evaluated_at")
    for key in required_str:
        if key not in gp or not isinstance(gp[key], str):
            return False, f"goal_progress.{key} must be non-empty string"
    if gp.get("goal_source") not in GOAL_SOURCE_VALUES:
        return False, "goal_source invalid"
    if gp.get("mode") != "goal_convergence":
        return False, "mode must be goal_convergence"
    if not isinstance(gp.get("converged"), bool):
        return False, "converged must be bool"
    for key in ("unmet_conditions", "blocked_by"):
        if not isinstance(gp.get(key), list):
            return False, f"{key} must be list"
    if gp.get("schema_version") != SCHEMA_VERSION:
        return False, "schema_version must be 1"
    if not isinstance(gp.get("conjuncts"), dict):
        return False, "conjuncts must be object"
    return True, None


def build_goal_progress_block(
    result: ConvergenceResult,
    goal_text: str,
    goal_source: str,
    orchestrator_run_id: Optional[str],
) -> dict:
    return {
        "goal_progress": {
            "goal_text": goal_text,
            "goal_source": goal_source,
            "mode": "goal_convergence",
            "converged": result.converged,
            "unmet_conditions": list(result.unmet_conditions),
            "blocked_by": list(result.blocked_by),
            "conjuncts": {
                name: {
                    "status": c.status,
                    "reason_code": c.reason_code,
                    "skipped": c.skipped,
                }
                for name, c in result.conjuncts.items()
            },
            "evaluated_at": result.evaluated_at or _utc_now_iso(),
            "orchestrator_run_id": orchestrator_run_id,
            "schema_version": SCHEMA_VERSION,
        }
    }


def _deferrals_summary(repo: Path) -> str:
    path = repo / DEFERRALS_PATH
    if not path.is_file():
        return "Deferral register not deployed (US-0107)."
    lines = [ln for ln in path.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()]
    if not lines:
        return "No pending deferrals."
    return f"{len(lines)} deferral record(s) in register."


def write_partial_delivery_report(
    repo: Path,
    result: ConvergenceResult,
    goal_text: str,
    timeout_reason: ReasonCode,
    orchestrator_run_id: Optional[str],
) -> Path:
    """Write idempotent partial-delivery report (DEC-0110 §6 / AC-5)."""
    out = repo / PARTIAL_DELIVERY_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    open_stories, done_stories = _scan_story_statuses(repo / BACKLOG_PATH)
    blocked = list(result.blocked_by)
    if timeout_reason.value not in blocked:
        blocked.append(timeout_reason.value)

    body = (
        "# Sovereign Partial Delivery\n\n"
        f"## Goal\n\n{goal_text}\n\n"
        f"## Evaluated At\n\n{result.evaluated_at}\n\n"
        "## Unmet Conditions\n\n"
        + ("\n".join(f"- {u}" for u in result.unmet_conditions) or "- (none)")
        + "\n\n## Blocked By\n\n"
        + ("\n".join(f"- {b}" for b in blocked) or "- (none)")
        + "\n\n## Completed Stories\n\n"
        + ("\n".join(f"- {s}" for s in done_stories) or "- (none)")
        + "\n\n## Open Stories\n\n"
        + ("\n".join(f"- {s}" for s in open_stories) or "- (none)")
        + "\n\n## Deferrals Summary\n\n"
        + _deferrals_summary(repo)
        + "\n\n## Remediation\n\n"
        + "- Review blocked reason codes in `docs/engineering/reason_codes.md` § US-0110.\n"
        + "- Resolve unmet conjuncts and re-run convergence evaluation.\n"
        + f"- Orchestrator run: `{orchestrator_run_id or '(none)'}`.\n"
    )
    out.write_text(body, encoding="utf-8")
    return out


def check_timeout(scratchpad: Dict[str, str], iteration_count: int) -> Tuple[bool, Optional[ReasonCode]]:
    sp = parse_scratchpad(scratchpad)
    try:
        max_iter = int(sp.get(SOVEREIGN_GOAL_TIMEOUT_MAX_KEY, SOVEREIGN_GOAL_TIMEOUT_MAX_DEFAULT))
    except ValueError:
        return True, ReasonCode.SOVEREIGN_GOAL_MODE_INVALID
    if max_iter <= 0:
        return False, None
    if iteration_count >= max_iter:
        return True, ReasonCode.SOVEREIGN_GOAL_TIMEOUT
    return False, None


def emit_goal_progress_to_resume_brief(
    repo: Path,
    scratchpad: Dict[str, str],
    orchestrator_run_id: Optional[str],
) -> bool:
    """
    Insert ### goal_progress fenced JSON after latest orchestration pointer in resume_brief.md.
    Returns True when block was written; False when skipped (phase_driven or inactive).
    """
    if not is_goal_convergence_enabled(scratchpad):
        return False
    result = evaluate_convergence(repo, scratchpad, orchestrator_run_id=orchestrator_run_id)
    goal = resolve_goal(scratchpad, repo)
    if goal.reason_code == ReasonCode.SOVEREIGN_GOAL_DERIVE_FAILED:
        goal_text = "(derive failed)"
        goal_source = "explicit"
    else:
        goal_text = goal.goal_text or "(unset)"
        goal_source = goal.goal_source or "explicit"
    block = build_goal_progress_block(result, goal_text, goal_source, orchestrator_run_id)
    fenced = (
        "### goal_progress\n\n"
        "```json\n"
        + json.dumps(block, indent=2, sort_keys=True)
        + "\n```\n"
    )
    brief_path = repo / RESUME_BRIEF_PATH
    if not brief_path.is_file():
        brief_path.parent.mkdir(parents=True, exist_ok=True)
        brief_path.write_text(f"# Resume Brief\n\n{fenced}", encoding="utf-8")
        return True

    text = brief_path.read_text(encoding="utf-8")
    marker = "## Latest orchestration pointer"
    if marker not in text:
        brief_path.write_text(text.rstrip() + "\n\n" + fenced, encoding="utf-8")
        return True

    parts = text.split(marker, 1)
    after = parts[1]
    next_header = re.search(r"\n## Prior orchestration pointer", after)
    if next_header:
        insert_at = len(parts[0]) + len(marker) + next_header.start()
        new_text = text[:insert_at] + "\n\n" + fenced + text[insert_at:]
    else:
        new_text = text.rstrip() + "\n\n" + fenced
    brief_path.write_text(new_text, encoding="utf-8")
    return True


def self_test() -> bool:
    errors: List[str] = []

    if len(REASON_CODES) != 10:
        errors.append(f"expected 10 reason codes, got {len(REASON_CODES)}")

    sample = ConvergenceResult(
        converged=False,
        unmet_conditions=["test"],
        blocked_by=[ReasonCode.CONVERGENCE_OPEN_STORIES_REMAIN.value],
        conjuncts={
            name: ConjunctResult(name=name, status="pass", skipped=False)
            for name in CONVERGENCE_CONJUNCTS
        },
        evaluated_at=_utc_now_iso(),
        schema_version=SCHEMA_VERSION,
    )
    ok, err = schema_check_convergence_result(sample.to_dict())
    if not ok:
        errors.append(f"schema_check_convergence_result: {err}")

    gp = build_goal_progress_block(sample, "test goal", "explicit", "auto-test")
    ok, err = schema_check_goal_progress(gp)
    if not ok:
        errors.append(f"schema_check_goal_progress: {err}")

    if not is_goal_convergence_enabled({SOVEREIGN_GOAL_MODE_KEY: "goal_convergence"}):
        errors.append("is_goal_convergence_enabled should be true for goal_convergence")

    if is_goal_convergence_enabled({SOVEREIGN_GOAL_MODE_KEY: "phase_driven"}):
        errors.append("is_goal_convergence_enabled should be false for phase_driven")

    timed, code = check_timeout({SOVEREIGN_GOAL_TIMEOUT_MAX_KEY: "0"}, 99)
    if timed:
        errors.append("timeout should be disabled when max=0")

    timed, code = check_timeout({SOVEREIGN_GOAL_TIMEOUT_MAX_KEY: "3"}, 3)
    if not timed or code != ReasonCode.SOVEREIGN_GOAL_TIMEOUT:
        errors.append("timeout should fire at iteration cap")

    if errors:
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        print("[SELF_TEST_FAILED]", file=sys.stderr)
        return False

    print("[SOVEREIGN_CONVERGENCE_SELF_TEST_OK]")
    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sovereign convergence library (US-0110 / DEC-0110)")
    parser.add_argument("--self-test", action="store_true", help="Run self-test")
    parser.add_argument("--evaluate", action="store_true", help="Evaluate convergence")
    parser.add_argument("--dump-progress", action="store_true", help="Dump goal_progress block JSON")
    parser.add_argument("--emit-resume-brief", action="store_true", help="Emit goal_progress to resume_brief.md")
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Repo root")
    parser.add_argument("--orchestrator-run-id", default=None, help="Orchestrator run id")

    args = parser.parse_args()

    if args.self_test:
        sys.exit(0 if self_test() else 1)

    scratchpad: Dict[str, str] = {SOVEREIGN_GOAL_MODE_KEY: "goal_convergence"}

    if args.evaluate:
        result = evaluate_convergence(args.repo, scratchpad, orchestrator_run_id=args.orchestrator_run_id)
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        sys.exit(0)

    if args.dump_progress:
        result = evaluate_convergence(args.repo, scratchpad, orchestrator_run_id=args.orchestrator_run_id)
        goal = resolve_goal(scratchpad, args.repo)
        block = build_goal_progress_block(
            result,
            goal.goal_text or "(unset)",
            goal.goal_source or "explicit",
            args.orchestrator_run_id,
        )
        print(json.dumps(block, indent=2, sort_keys=True))
        sys.exit(0)

    if args.emit_resume_brief:
        ok = emit_goal_progress_to_resume_brief(args.repo, scratchpad, args.orchestrator_run_id)
        sys.exit(0 if ok else 1)

    parser.print_help()
    sys.exit(0)
