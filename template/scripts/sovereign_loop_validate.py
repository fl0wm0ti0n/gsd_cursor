#!/usr/bin/env python3
"""
Sovereign Loop deferral register validator (US-0107 / DEC-0107).

Exit codes:
- 0: validation passed (or --self-test OK)
- 1: fail-closed validation error (with --enforce)
- 2: usage error
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import uuid
from pathlib import Path
from typing import List, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

from sovereign_loop_lib import (  # noqa: E402
    build_sample_deferral,
    resolve_deferrals_path,
    schema_check_deferral,
    self_test,
)


def validate_jsonl_file(path: Path) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if not path.is_file():
        return True, errors

    for line_no, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{line_no}: JSON decode error: {exc}")
            continue
        ok, err = schema_check_deferral(obj)
        if not ok:
            errors.append(f"{path}:{line_no}: {err}")

    return len(errors) == 0, errors


def validate_repo(repo: Path) -> Tuple[bool, List[str]]:
    path = resolve_deferrals_path(repo)
    if not path.is_file():
        return True, []
    return validate_jsonl_file(path)


def run_self_test() -> bool:
    if not self_test():
        return False

    good = build_sample_deferral()
    good["deferral_id"] = str(uuid.uuid4())
    ok, err = schema_check_deferral(good)
    if not ok:
        print(f"  fixture deferral: {err}", file=sys.stderr)
        return False

    with tempfile.TemporaryDirectory() as tmp:
        bad_path = Path(tmp) / "bad.jsonl"
        bad_path.write_text('{"schema_version": 1}\n', encoding="utf-8")
        ok_file, errors = validate_jsonl_file(bad_path)
        if ok_file or not errors:
            print("  expected invalid fixture to fail", file=sys.stderr)
            return False

    print("[SOVEREIGN_LOOP_VALIDATION_OK]")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Sovereign loop deferral validator (US-0107 / DEC-0107)")
    parser.add_argument("--file", type=Path, help="Validate single JSONL file")
    parser.add_argument("--repo", type=Path, help="Validate repo deferrals path if present")
    parser.add_argument("--self-test", action="store_true", help="Run lib self-test + schema fixtures")
    parser.add_argument("--enforce", action="store_true", help="Exit non-zero on validation failure")

    args = parser.parse_args()

    if args.self_test:
        return 0 if run_self_test() else 1

    errors: List[str] = []

    if args.file is not None:
        ok, file_errors = validate_jsonl_file(args.file)
        if not ok:
            errors.extend(file_errors)

    if args.repo is not None:
        ok_repo, repo_errors = validate_repo(args.repo)
        if not ok_repo:
            errors.extend(repo_errors)

    if args.file is None and args.repo is None:
        parser.print_help()
        return 2

    if errors:
        for item in errors:
            print(item, file=sys.stderr)
        if args.enforce:
            return 1
        return 0

    print("[SOVEREIGN_LOOP_VALIDATION_OK]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
