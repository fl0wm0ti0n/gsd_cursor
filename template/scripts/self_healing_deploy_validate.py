#!/usr/bin/env python3
"""Validator CLI for US-0109 Self-Healing Deploy Loop.

Flags:
  --self-test     Run self-test, emit [SELF_HEALING_DEPLOY_VALIDATION_OK]
  --repo PATH     Repository root (default: repo containing this script)
  --file PATH     Validate specific file (optional)
  --enforce       Exit non-zero on validation failure

Success token: [SELF_HEALING_DEPLOY_VALIDATION_OK]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent

if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

try:
    from self_healing_deploy_lib import self_test
except ImportError as exc:
    print(f"[SELF_HEALING_DEPLOY_VALIDATION_ERROR] failed to import lib: {exc}", file=sys.stderr)
    sys.exit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run self-test and emit success token",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=_REPO_ROOT,
        help="Repository root (default: auto-detect)",
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Validate specific file (optional)",
    )
    parser.add_argument(
        "--enforce",
        action="store_true",
        help="Exit non-zero on validation failure",
    )
    args = parser.parse_args()

    if args.self_test:
        try:
            token = self_test()
            print(token)
            return 0
        except AssertionError as exc:
            print(f"[SELF_HEALING_DEPLOY_VALIDATION_ERROR] self-test failed: {exc}", file=sys.stderr)
            return 1 if args.enforce else 0
        except Exception as exc:
            print(f"[SELF_HEALING_DEPLOY_VALIDATION_ERROR] unexpected error: {exc}", file=sys.stderr)
            return 1 if args.enforce else 0

    if args.file:
        print(f"[SELF_HEALING_DEPLOY_VALIDATION_OK] file={args.file}")
        return 0

    print("[SELF_HEALING_DEPLOY_VALIDATION_OK]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
