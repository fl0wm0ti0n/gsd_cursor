#!/usr/bin/env python3
"""
AI Decision Ledger JSONL validator (US-0103 / DEC-0103).

Validates:
- 12-field schema v1 per JSONL line
- One-file-per-orchestrator-run path layout
- Bounded QA digest emission

Exit codes:
- 0: All validations passed (or --self-test OK)
- 1: Fail-closed code hit
- 2: Usage error
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

from decision_ledger_lib import (  # noqa: E402
    LEDGER_REQUIRED_FIELDS,
    ReasonCode,
    build_qa_findings_block,
    is_ledger_enabled,
    read_entries,
    resolve_ledger_path,
    schema_check,
    self_test,
    summary_digest,
)


def validate_single_file(ledger_path: Path, *, strict: bool = True) -> Tuple[bool, List[str], List[ReasonCode]]:
    """Validate every JSONL entry in one ledger file. Returns (ok, errors, codes)."""
    errors: List[str] = []
    codes: List[ReasonCode] = []

    if not ledger_path.exists():
        return False, [f"Ledger file not found: {ledger_path}"], [ReasonCode.LEDGER_FILE_MISSING]

    entries, reason, message = read_entries(ledger_path, strict=strict)
    if reason is not None:
        if reason in (ReasonCode.LEDGER_CORRUPT, ReasonCode.LEDGER_SCHEMA_INVALID):
            errors.append(f"[{reason.value}] {message}")
            codes.append(reason)
            return len(errors) == 0, errors, codes
        if reason == ReasonCode.LEDGER_FILE_MISSING:
            errors.append(f"[{reason.value}] {message}")
            codes.append(reason)
            return len(errors) == 0, errors, codes
        if reason == ReasonCode.LEDGER_READ_BOUND:
            pass

    if not ledger_path.name.endswith(".jsonl"):
        errors.append(f"Ledger file must end with .jsonl: {ledger_path.name}")

    if not ledger_path.parent.name == "sovereign_decisions":
        errors.append(f"Ledger must live in handoffs/sovereign_decisions/: {ledger_path}")

    return len(errors) == 0, errors, codes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Decision ledger JSONL validator (US-0103 / DEC-0103)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/ledger_validate.py --self-test
  python scripts/ledger_validate.py --file handoffs/sovereign_decisions/auto-20260628-01.jsonl
  python scripts/ledger_validate.py --repo .
  python scripts/ledger_validate.py --file handoffs/sovereign_decisions/auto-20260628-01.jsonl --enforce
  python scripts/ledger_validate.py --qa-find --orchestrator-run-id auto-20260628-01 --repo .
        """,
    )
    parser.add_argument("--file", type=Path, help="Validate single JSONL ledger file")
    parser.add_argument("--repo", type=Path, help="Validate all ledger files in handoffs/sovereign_decisions/")
    parser.add_argument("--self-test", action="store_true", help="Run library self-test")
    parser.add_argument("--enforce", action="store_true", help="Exit non-zero on any fail-closed code")
    parser.add_argument(
        "--qa-find",
        action="store_true",
        help="Build QA findings block (prints JSON) for ledger; needs --orchestrator-run-id",
    )
    parser.add_argument("--orchestrator-run-id", help="Orchestrator run id for --qa-find / --file resolution")

    args = parser.parse_args()

    if args.self_test:
        return 0 if self_test() else 1

    if args.qa_find:
        if not args.orchestrator_run_id:
            print("[USAGE] --qa-find requires --orchestrator-run-id", file=sys.stderr)
            return 2
        repo_root = Path(args.repo) if args.repo else Path.cwd()
        ledger_path = resolve_ledger_path(args.orchestrator_run_id, repo_root)
        block, blocking = build_qa_findings_block(ledger_path, args.orchestrator_run_id)
        print(json.dumps(block, indent=2, sort_keys=True))
        if blocking is not None:
            return 1 if args.enforce else 0
        return 0

    all_errors: List[str] = []
    all_codes: List[ReasonCode] = []

    if args.file:
        ok, errs, codes = validate_single_file(Path(args.file))
        all_errors.extend(errs)
        all_codes.extend(codes)
    elif args.repo:
        sovereign_dir = Path(args.repo) / "handoffs" / "sovereign_decisions"
        if sovereign_dir.exists():
            for ledger_path in sorted(sovereign_dir.glob("*.jsonl")):
                ok, errs, codes = validate_single_file(ledger_path)
                if not ok:
                    all_errors.extend([f"{ledger_path}: {e}" for e in errs])
                    all_codes.extend(codes)

    if not args.file and not args.repo:
        sovereign_dir = Path.cwd() / "handoffs" / "sovereign_decisions"
        if sovereign_dir.exists():
            for ledger_path in sorted(sovereign_dir.glob("*.jsonl")):
                ok, errs, codes = validate_single_file(ledger_path)
                if not ok:
                    all_errors.extend([f"{ledger_path}: {e}" for e in errs])
                    all_codes.extend(codes)

    if all_errors:
        print(f"\n[LEDGER_VALIDATION_FAILED] {len(all_errors)} error(s)", file=sys.stderr)
        for err in all_errors:
            print(f"  {err}", file=sys.stderr)
        if args.enforce:
            return 1
        return 1 if any(
            c in (ReasonCode.LEDGER_FILE_MISSING, ReasonCode.LEDGER_SCHEMA_INVALID, ReasonCode.LEDGER_CORRUPT)
            for c in all_codes
        ) else 0

    print("[LEDGER_VALIDATION_OK]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
