#!/usr/bin/env python3
"""
Sovereign convergence JSON validator (US-0110 / DEC-0110).

Validates ConvergenceResult and goal_progress block shapes; optional repo artifact checks.

Exit codes:
- 0: validation passed (or --self-test OK)
- 1: fail-closed validation error (with --enforce)
- 2: usage error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, List, Optional, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

from sovereign_convergence_lib import (  # noqa: E402
    PARTIAL_DELIVERY_PATH,
    RESUME_BRIEF_PATH,
    schema_check_convergence_result,
    schema_check_goal_progress,
    self_test,
)

PARTIAL_SECTIONS = (
    "Goal",
    "Evaluated At",
    "Unmet Conditions",
    "Blocked By",
    "Completed Stories",
    "Open Stories",
    "Deferrals Summary",
    "Remediation",
)


def _load_json(path_or_dash: str) -> Tuple[Optional[Any], Optional[str]]:
    if path_or_dash == "-":
        try:
            return json.load(sys.stdin), None
        except json.JSONDecodeError as exc:
            return None, f"stdin JSON decode error: {exc}"
    p = Path(path_or_dash)
    if not p.is_file():
        return None, f"file not found: {p}"
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as exc:
        return None, f"JSON decode error in {p}: {exc}"


def validate_partial_delivery(path: Path) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if not path.is_file():
        return True, errors
    text = path.read_text(encoding="utf-8")
    for section in PARTIAL_SECTIONS:
        if f"## {section}" not in text:
            errors.append(f"partial delivery missing section: {section}")
    return len(errors) == 0, errors


def validate_resume_brief_goal_progress(path: Path) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if not path.is_file():
        return True, errors
    text = path.read_text(encoding="utf-8")
    if "### goal_progress" not in text:
        return True, errors
    m = re.search(r"### goal_progress\s+```json\s*(.*?)\s*```", text, re.DOTALL)
    if not m:
        errors.append("goal_progress heading present but fenced JSON block missing")
        return False, errors
    try:
        obj = json.loads(m.group(1))
    except json.JSONDecodeError as exc:
        errors.append(f"goal_progress JSON invalid: {exc}")
        return False, errors
    ok, err = schema_check_goal_progress(obj)
    if not ok:
        errors.append(f"goal_progress schema: {err}")
    return len(errors) == 0, errors


def run_self_test() -> bool:
    if not self_test():
        return False

    good_conv = {
        "converged": False,
        "unmet_conditions": ["test"],
        "blocked_by": ["CONVERGENCE_OPEN_STORIES_REMAIN"],
        "conjuncts": {
            name: {"status": "pass", "reason_code": None, "skipped": False}
            for name in (
                "backlog_clear",
                "zero_deferrals",
                "critic_resolved",
                "smoke_green",
                "ledger_clean",
            )
        },
        "evaluated_at": "2026-06-28T19:30:00.000Z",
        "schema_version": 1,
    }
    ok, err = schema_check_convergence_result(good_conv)
    if not ok:
        print(f"  fixture convergence: {err}", file=sys.stderr)
        return False

    bad_conv = dict(good_conv)
    del bad_conv["converged"]
    ok_b, _ = schema_check_convergence_result(bad_conv)
    if ok_b:
        print("  expected invalid convergence fixture to fail", file=sys.stderr)
        return False

    good_gp = {
        "goal_progress": {
            "goal_text": "test",
            "goal_source": "explicit",
            "mode": "goal_convergence",
            "converged": False,
            "unmet_conditions": [],
            "blocked_by": [],
            "conjuncts": {},
            "evaluated_at": "2026-06-28T19:30:00.000Z",
            "orchestrator_run_id": "auto-test",
            "schema_version": 1,
        }
    }
    ok, err = schema_check_goal_progress(good_gp)
    if not ok:
        print(f"  fixture goal_progress: {err}", file=sys.stderr)
        return False

    print("[SOVEREIGN_CONVERGENCE_VALIDATION_OK]")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Sovereign convergence validator (US-0110 / DEC-0110)")
    parser.add_argument("--convergence-json", help="Validate ConvergenceResult JSON (path or -)")
    parser.add_argument("--goal-progress-json", help="Validate goal_progress block JSON (path or -)")
    parser.add_argument("--repo", type=Path, help="Validate partial-delivery + resume_brief goal_progress when present")
    parser.add_argument("--self-test", action="store_true", help="Run lib self-test + schema fixtures")
    parser.add_argument("--enforce", action="store_true", help="Exit non-zero on validation failure")

    args = parser.parse_args()

    if args.self_test:
        return 0 if run_self_test() else 1

    errors: List[str] = []

    if args.convergence_json:
        obj, err = _load_json(args.convergence_json)
        if err:
            errors.append(err)
        elif obj is not None:
            ok, serr = schema_check_convergence_result(obj)
            if not ok:
                errors.append(f"convergence-json: {serr}")

    if args.goal_progress_json:
        obj, err = _load_json(args.goal_progress_json)
        if err:
            errors.append(err)
        elif obj is not None:
            ok, serr = schema_check_goal_progress(obj)
            if not ok:
                errors.append(f"goal-progress-json: {serr}")

    repo_root = args.repo or Path.cwd()
    if args.repo is not None or (not args.convergence_json and not args.goal_progress_json):
        ok, perrs = validate_partial_delivery(repo_root / PARTIAL_DELIVERY_PATH)
        if not ok:
            errors.extend(perrs)
        ok, rerrs = validate_resume_brief_goal_progress(repo_root / RESUME_BRIEF_PATH)
        if not ok:
            errors.extend(rerrs)

    if not args.convergence_json and not args.goal_progress_json and args.repo is None:
        parser.print_help()
        return 2

    if errors:
        print(f"\n[SOVEREIGN_CONVERGENCE_VALIDATION_FAILED] {len(errors)} error(s)", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1 if args.enforce else 1

    print("[SOVEREIGN_CONVERGENCE_VALIDATION_OK]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
