#!/usr/bin/env python3
"""Verify active vs template/ bytes match for DEC-0062 token-cost parity manifest paths."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_PAIR_RE = re.compile(r"`([^`]+)`\s*→\s*`([^`]+)`")


def load_pairs(manifest_text: str) -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    for line in manifest_text.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        m = _PAIR_RE.search(line)
        if not m:
            continue
        pairs.append((Path(m.group(1)), Path(m.group(2))))
    return pairs


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
    manifest = root / "docs/engineering/token-cost-parity-manifest.md"
    if not manifest.is_file():
        print(f"[TOKEN_COST_PARITY_ERROR] missing manifest: {manifest}")
        return 2
    text = manifest.read_text(encoding="utf-8")
    pairs = load_pairs(text)
    if not pairs:
        print("[TOKEN_COST_PARITY_ERROR] no path pairs parsed from manifest")
        return 2
    failed = False
    for rel_active, rel_tpl in pairs:
        a = root / rel_active
        t = root / rel_tpl
        if not a.is_file() or not t.is_file():
            print(f"[TOKEN_COST_PARITY_ERROR] missing file: {rel_active} or {rel_tpl}")
            failed = True
            continue
        ba = a.read_bytes()
        bt = t.read_bytes()
        if ba != bt:
            print(
                f"[TOKEN_COST_PARITY_ERROR] mismatch: {rel_active} ({len(ba)}b) "
                f"!= {rel_tpl} ({len(bt)}b)"
            )
            failed = True
    if failed:
        return 2
    print("[TOKEN_COST_PARITY_OK]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
