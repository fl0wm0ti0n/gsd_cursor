#!/usr/bin/env python3
"""Validate work/<story_id>/pack.json schema v1 (US-0096 / DEC-0082)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = (
    "schema_version",
    "story_id",
    "delivery_mode",
    "status",
    "ac",
    "tasks",
    "refs",
    "deltas",
    "memory_layer",
)

VALID_DELIVERY_MODES = frozenset({"standard", "ultra_lean", "mega_quick"})
VALID_MEMORY_LAYER = "pack"


def validate_pack(data: Any, *, expected_story_id: str | None = None) -> list[str]:
    """Return PACK_* reason codes; empty list means valid."""
    codes: list[str] = []
    if not isinstance(data, dict):
        return ["PACK_INVALID_ROOT"]

    for field in REQUIRED_FIELDS:
        if field not in data:
            codes.append(f"PACK_MISSING_REQUIRED_FIELD:{field}")

    if codes:
        return codes

    if data.get("schema_version") != "1":
        codes.append("PACK_SCHEMA_VERSION_INVALID")

    story_id = data.get("story_id")
    if not isinstance(story_id, str) or not story_id.strip():
        codes.append("PACK_STORY_ID_INVALID")
    elif expected_story_id and story_id != expected_story_id:
        codes.append("PACK_STORY_ID_MISMATCH")

    delivery_mode = data.get("delivery_mode")
    if delivery_mode not in VALID_DELIVERY_MODES:
        codes.append("PACK_DELIVERY_MODE_INVALID")

    if not isinstance(data.get("status"), str) or not str(data["status"]).strip():
        codes.append("PACK_STATUS_INVALID")

    for list_field in ("ac", "tasks", "refs", "deltas"):
        if not isinstance(data.get(list_field), list):
            codes.append(f"PACK_INVALID_FIELD_TYPE:{list_field}")

    if data.get("memory_layer") != VALID_MEMORY_LAYER:
        codes.append("PACK_MEMORY_LAYER_INVALID")

    return codes


def main() -> int:
    p = argparse.ArgumentParser(description="Validate pack.json schema v1 (US-0096).")
    p.add_argument("--file", type=Path, help="Path to pack.json")
    p.add_argument(
        "--story-id",
        help="Expected story_id (e.g. US-0096); mismatch → PACK_STORY_ID_MISMATCH",
    )
    p.add_argument(
        "--self-test",
        action="store_true",
        help="Run built-in fixture checks and exit.",
    )
    args = p.parse_args()

    if args.self_test:
        valid = {
            "schema_version": "1",
            "story_id": "US-0096",
            "delivery_mode": "ultra_lean",
            "status": "OPEN",
            "ac": ["AC-1"],
            "tasks": [{"id": "T-001", "status": "pending"}],
            "refs": ["decisions/DEC-0082.md"],
            "deltas": [],
            "memory_layer": "pack",
        }
        if validate_pack(valid):
            print("PACK_SELF_TEST_FAIL: valid fixture rejected", file=sys.stderr)
            return 1
        invalid = dict(valid)
        del invalid["story_id"]
        if "PACK_MISSING_REQUIRED_FIELD:story_id" not in validate_pack(invalid):
            print("PACK_SELF_TEST_FAIL: missing field not detected", file=sys.stderr)
            return 1
        print("[PACK_JSON_SELF_TEST_OK]")
        return 0

    if not args.file:
        print("error: specify --file or --self-test", file=sys.stderr)
        return 2

    path = args.file.resolve()
    if not path.is_file():
        print(f"PACK_FILE_NOT_FOUND: {path}", file=sys.stderr)
        return 2

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"PACK_INVALID_JSON: {exc}", file=sys.stderr)
        return 1

    codes = validate_pack(data, expected_story_id=args.story_id)
    if codes:
        for code in codes:
            print(code, file=sys.stderr)
        return 1

    print("[PACK_JSON_VALIDATION_OK]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
