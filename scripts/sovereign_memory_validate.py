#!/usr/bin/env python3
"""
Sovereign Memory JSONL validator (US-0105 / DEC-0105).

Validates docs/engineering/sovereign-memory/*.jsonl entries against v1 family schemas.

Exit codes:
- 0: validation passed (or --self-test OK)
- 1: fail-closed validation error (with --enforce)
- 2: usage error
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

from sovereign_memory_lib import (  # noqa: E402
    JSONL_FAMILIES,
    JSONL_FILENAMES,
    ReasonCode,
    resolve_jsonl_path,
    schema_check,
    self_test,
)


def validate_jsonl_file(path: Path, family: str) -> Tuple[bool, List[str], List[str]]:
    errors: List[str] = []
    codes: List[str] = []
    if not path.is_file():
        return True, errors, codes

    for line_no, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{line_no}: JSON decode error: {exc}")
            codes.append(ReasonCode.SOVEREIGN_MEMORY_SCHEMA_INVALID.value)
            continue
        ok, err = schema_check(obj, family)
        if not ok:
            errors.append(f"{path}:{line_no}: {err}")
            codes.append(ReasonCode.SOVEREIGN_MEMORY_SCHEMA_INVALID.value)

    return len(errors) == 0, errors, codes


def validate_repo(repo: Path, family: str) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    families = JSONL_FAMILIES if family == "all" else {family}

    for fam in sorted(families):
        path = resolve_jsonl_path(fam, repo)
        if not path.is_file():
            continue
        ok, file_errors, _ = validate_jsonl_file(path, fam)
        if not ok:
            errors.extend(file_errors)
    return len(errors) == 0, errors


def run_self_test() -> bool:
    if not self_test():
        return False

    import tempfile
    import uuid

    from sovereign_memory_lib import build_sample_decision  # noqa: WPS433

    good = build_sample_decision()
    good["entry_id"] = str(uuid.uuid4())
    ok, err = schema_check(good, "decisions")
    if not ok:
        print(f"  fixture decision: {err}", file=sys.stderr)
        return False

    with tempfile.TemporaryDirectory() as tmp:
        bad_path = Path(tmp) / "bad.jsonl"
        bad_path.write_text('{"schema_version": 1}\n', encoding="utf-8")
        ok_file, errors, _ = validate_jsonl_file(bad_path, "decisions")
        if ok_file or not errors:
            print("  expected invalid fixture to fail", file=sys.stderr)
            return False

    print("[SOVEREIGN_MEMORY_VALIDATION_OK]")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Sovereign memory validator (US-0105 / DEC-0105)")
    parser.add_argument("--file", type=Path, help="Validate single JSONL file")
    parser.add_argument("--repo", type=Path, help="Validate sovereign-memory JSONL if present")
    parser.add_argument(
        "--family",
        choices=sorted(JSONL_FAMILIES | {"all"}),
        default="all",
        help="JSONL family to validate (default all)",
    )
    parser.add_argument("--self-test", action="store_true", help="Run lib self-test + schema fixtures")
    parser.add_argument("--enforce", action="store_true", help="Exit non-zero on validation failure")

    args = parser.parse_args()

    if args.self_test:
        return 0 if run_self_test() else 1

    errors: List[str] = []

    if args.file is not None:
        family = args.family if args.family != "all" else "decisions"
        if args.family == "all":
            matched = None
            for fam, name in JSONL_FILENAMES.items():
                if args.file.name == name:
                    matched = fam
                    break
            family = matched or "decisions"
        ok, file_errors, _ = validate_jsonl_file(args.file, family)
        if not ok:
            errors.extend(file_errors)

    if args.repo is not None:
        ok_repo, repo_errors = validate_repo(args.repo, args.family)
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

    print("[SOVEREIGN_MEMORY_VALIDATION_OK]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
