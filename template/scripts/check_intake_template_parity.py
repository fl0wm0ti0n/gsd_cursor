#!/usr/bin/env python3
"""Verify active vs template/scripts/ bytes match for DEC-0063 intake gate modules (BUG-0001)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Normative pairs: repo scripts/ (canonical dev) → template/scripts/ (packaged ship path).
INTAKE_TEMPLATE_PAIRS: tuple[tuple[str, str], ...] = (
    ("scripts/intake_evidence_validate.py", "template/scripts/intake_evidence_validate.py"),
    ("scripts/intake_evidence_lib.py", "template/scripts/intake_evidence_lib.py"),
    ("scripts/intake_bug_routing_guard.py", "template/scripts/intake_bug_routing_guard.py"),
    ("scripts/check_intake_template_parity.py", "template/scripts/check_intake_template_parity.py"),
)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root",
    )
    args = p.parse_args()
    root: Path = args.repo
    failed = False
    for rel_active, rel_tpl in INTAKE_TEMPLATE_PAIRS:
        a = root / rel_active
        t = root / rel_tpl
        if not a.is_file() or not t.is_file():
            print(f"[INTAKE_TEMPLATE_PARITY_ERROR] missing file: {rel_active} or {rel_tpl}")
            failed = True
            continue
        ba = a.read_bytes()
        bt = t.read_bytes()
        if ba != bt:
            print(
                f"[INTAKE_TEMPLATE_PARITY_ERROR] mismatch: {rel_active} ({len(ba)}b) "
                f"!= {rel_tpl} ({len(bt)}b)"
            )
            failed = True
    if failed:
        return 2
    print("[INTAKE_TEMPLATE_PARITY_OK]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
