#!/usr/bin/env python3
"""
Deterministic scratchpad paired-file parity (US-0075 / DEC-0057 / AC-11).

Verifies each (baseline, example) pair under the repo root and template/ has:
  - identical sets of automation KEY= names (values may differ)
  - identical sets of structural section headers from the catalog anchor
    (# Core behavior) through EOF (single-line # headers that are not doc bullets)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_CATALOG_ANCHOR = "# Core behavior"

# Lines like "KEY=value" (installer-style automation keys)
_KEY_LINE = re.compile(r"^([A-Z][A-Z0-9_]*)=")

# Structural header: "# " then a non-whitespace, non- comment-bullet start
_HEADER_LINE = re.compile(r"^# ([^-#\s].*)$")


def parse_keys(path: Path) -> set[str]:
    keys: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("- "):
            continue
        if "=" not in line:
            continue
        m = _KEY_LINE.match(line)
        if m:
            keys.add(m.group(1))
    return keys


def parse_catalog_headers(path: Path) -> set[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        start = next(i for i, ln in enumerate(lines) if ln.rstrip("\r") == _CATALOG_ANCHOR)
    except StopIteration:
        raise ValueError(f"missing catalog anchor {_CATALOG_ANCHOR!r} in {path}") from None
    headers: set[str] = set()
    for ln in lines[start:]:
        if _HEADER_LINE.match(ln):
            headers.add(ln.strip())
    return headers


def check_pair(repo: Path, baseline_rel: str, example_rel: str, label: str) -> list[str]:
    a = repo / baseline_rel
    b = repo / example_rel
    errs: list[str] = []
    if not a.is_file():
        errs.append(f"[SCRATCHPAD_PAIR_ERROR] {label}: missing {baseline_rel}")
        return errs
    if not b.is_file():
        errs.append(f"[SCRATCHPAD_PAIR_ERROR] {label}: missing {example_rel}")
        return errs

    try:
        ka, kb = parse_keys(a), parse_keys(b)
    except OSError as exc:
        return [f"[SCRATCHPAD_PAIR_ERROR] {label}: read failure: {exc}"]
    if ka != kb:
        only_a = sorted(ka - kb)
        only_b = sorted(kb - ka)
        errs.append(
            f"[SCRATCHPAD_PAIR_ERROR] {label}: KEY set mismatch "
            f"only_in_baseline={only_a} only_in_example={only_b}"
        )

    try:
        ha, hb = parse_catalog_headers(a), parse_catalog_headers(b)
    except ValueError as exc:
        errs.append(f"[SCRATCHPAD_PAIR_ERROR] {label}: {exc}")
        return errs
    if ha != hb:
        only_a = sorted(ha - hb)
        only_b = sorted(hb - ha)
        errs.append(
            f"[SCRATCHPAD_PAIR_ERROR] {label}: catalog section header mismatch "
            f"only_in_baseline={only_a} only_in_example={only_b}"
        )
    return errs


def main() -> int:
    p = argparse.ArgumentParser(description="Check scratchpad baseline/example pair parity.")
    p.add_argument("--repo", default=".", help="Repository root (default: .)")
    args = p.parse_args()
    repo = Path(args.repo).resolve()

    pairs: list[tuple[str, str, str]] = [
        (".cursor/scratchpad.md", ".cursor/scratchpad.local.example.md", "active_pair"),
        ("template/.cursor/scratchpad.md", "template/.cursor/scratchpad.local.example.md", "template_pair"),
    ]
    all_errs: list[str] = []
    for bl, ex, lab in pairs:
        all_errs.extend(check_pair(repo, bl, ex, lab))

    if all_errs:
        print("\n".join(all_errs))
        print(
            "[SCRATCHPAD_PAIR_ERROR] Fix: align keys and catalog # headers between "
            "each baseline file and its scratchpad.local.example.md peer "
            "(see DEC-0057 / US-0075 AC-11)."
        )
        return 1
    print(
        "[SCRATCHPAD_PAIR_OK] baseline/example KEY sets and catalog headers match "
        "for active and template pairs."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
