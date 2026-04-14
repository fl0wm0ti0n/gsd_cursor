#!/usr/bin/env python3
"""
Print required env var names from .env.example and validate parity with
*Env fields in template/.cursor/remote.json and
docs/engineering/release-targets.json (US-0085 / DEC-0071).

Never opens, reads, or prints from .env — values stay local.

Exit codes:
  0  parity OK (or warnings only)
  1  ENV_EXAMPLE_PARITY_MISMATCH — JSON *Env names missing from .env.example
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ENV_FIELD_RE = re.compile(r"(?:Env|ENV)$")
ENV_EXAMPLE_LINE = re.compile(r"^([A-Z][A-Z0-9_]*)=")

REMOTE_JSON = Path("template/.cursor/remote.json")
RELEASE_JSON = Path("docs/engineering/release-targets.json")
ENV_EXAMPLE = Path(".env.example")


def _collect_env_fields(data: object, out: set[str], path: str = "") -> None:
    if isinstance(data, dict):
        for k, v in data.items():
            if ENV_FIELD_RE.search(k) and isinstance(v, str) and v:
                out.add(v)
            else:
                _collect_env_fields(v, out, f"{path}.{k}")
    elif isinstance(data, list):
        for i, item in enumerate(data):
            _collect_env_fields(item, out, f"{path}[{i}]")


def _load_json(p: Path) -> object:
    return json.loads(p.read_text(encoding="utf-8"))


def _load_env_example_names(p: Path) -> set[str]:
    names: set[str] = set()
    for line in p.read_text(encoding="utf-8").splitlines():
        m = ENV_EXAMPLE_LINE.match(line.strip())
        if m:
            names.add(m.group(1))
    return names


def main() -> int:
    errors: list[str] = []

    if not ENV_EXAMPLE.is_file():
        print(f"[ENV_EXAMPLE_PARITY_MISMATCH] {ENV_EXAMPLE} not found.", file=sys.stderr)
        return 1

    example_names = _load_env_example_names(ENV_EXAMPLE)

    json_names: set[str] = set()
    for jp in [REMOTE_JSON, RELEASE_JSON]:
        if not jp.is_file():
            print(f"[WARN] {jp} not found; skipping.", file=sys.stderr)
            continue
        _collect_env_fields(_load_json(jp), json_names)

    missing_from_example = json_names - example_names
    extra_in_example = example_names - json_names

    print("# Required env var names (from .env.example)")
    for name in sorted(example_names):
        print(name)

    if missing_from_example:
        for name in sorted(missing_from_example):
            errors.append(f"[ENV_EXAMPLE_PARITY_MISMATCH] {name} in JSON *Env but missing from .env.example")
        for e in errors:
            print(e, file=sys.stderr)
        return 1

    if extra_in_example:
        for name in sorted(extra_in_example):
            print(f"[WARN] {name} in .env.example but not in JSON *Env sources", file=sys.stderr)

    print(f"\nParity PASS: {len(example_names)} names in .env.example, "
          f"{len(json_names)} *Env fields in JSON sources.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
