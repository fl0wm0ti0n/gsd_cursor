#!/usr/bin/env python3
"""
Cross-model adversarial critic JSONL validator (US-0104 / DEC-0104).

Validates handoffs/sovereign_critic_findings.jsonl entries against 15-field v1 schema.

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

from sovereign_critic_lib import (  # noqa: E402
    FINDINGS_PATH,
    ReasonCode,
    read_open_blocking,
    schema_check,
    self_test,
)


def validate_jsonl_file(path: Path) -> Tuple[bool, List[str], List[str]]:
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
            codes.append(ReasonCode.CROSS_MODEL_FINDINGS_INVALID.value)
            continue
        ok, err = schema_check(obj)
        if not ok:
            errors.append(f"{path}:{line_no}: {err}")
            codes.append(ReasonCode.CROSS_MODEL_FINDINGS_INVALID.value)

    return len(errors) == 0, errors, codes


def run_self_test() -> bool:
    if not self_test():
        return False

    import tempfile
    import uuid

    from sovereign_critic_lib import build_sample_finding  # noqa: WPS433

    good = build_sample_finding(finding_id=str(uuid.uuid4()))
    ok, err = schema_check(good)
    if not ok:
        print(f"  fixture finding: {err}", file=sys.stderr)
        return False

    with tempfile.TemporaryDirectory() as tmp:
        bad_path = Path(tmp) / "bad.jsonl"
        bad_path.write_text('{"lens": "challenger"}\n', encoding="utf-8")
        ok_file, errors, _ = validate_jsonl_file(bad_path)
        if ok_file or not errors:
            print("  expected invalid fixture to fail", file=sys.stderr)
            return False

    print("[SOVEREIGN_CRITIC_VALIDATION_OK]")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Sovereign critic validator (US-0104 / DEC-0104)")
    parser.add_argument("--file", type=Path, help="Validate single JSONL file")
    parser.add_argument("--repo", type=Path, help="Validate handoffs/sovereign_critic_findings.jsonl if present")
    parser.add_argument("--self-test", action="store_true", help="Run lib self-test + schema fixtures")
    parser.add_argument("--enforce", action="store_true", help="Exit non-zero on validation failure")
    parser.add_argument("--open-blocking", action="store_true", help="List open blocking findings (stdout JSON)")

    args = parser.parse_args()

    if args.self_test:
        return 0 if run_self_test() else 1

    if args.open_blocking:
        repo = args.repo or Path.cwd()
        rows = read_open_blocking(repo)
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0

    errors: List[str] = []

    if args.file is not None:
        ok, file_errors, _ = validate_jsonl_file(args.file)
        if not ok:
            errors.extend(file_errors)

    if args.repo is not None:
        target = args.repo / FINDINGS_PATH
        if target.is_file():
            ok, repo_errors, _ = validate_jsonl_file(target)
            if not ok:
                errors.extend(repo_errors)

    if args.file is None and args.repo is None:
        parser.print_help()
        return 2

    if errors:
        print(f"\n[SOVEREIGN_CRITIC_VALIDATION_FAILED] {len(errors)} error(s)", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1 if args.enforce else 1

    print("[SOVEREIGN_CRITIC_VALIDATION_OK]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
