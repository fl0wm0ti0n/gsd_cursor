#!/usr/bin/env python3
"""Compare two token-cost run JSON records for AC-2 (same run_class_hash, 50% cache read)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

import token_cost_lib  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("baseline", type=Path, help="JSON file with run_class_hash + totals")
    p.add_argument("target", type=Path, help="JSON file with run_class_hash + totals")
    p.add_argument(
        "--reduction-fraction",
        type=float,
        default=0.5,
        help="Required fractional reduction in cache_read_tokens (default 0.5)",
    )
    args = p.parse_args()
    base = json.loads(args.baseline.read_text(encoding="utf-8"))
    tgt = json.loads(args.target.read_text(encoding="utf-8"))
    ok, msg = token_cost_lib.compare_cache_read_reduction(
        base, tgt, reduction_fraction=args.reduction_fraction
    )
    print(msg)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
