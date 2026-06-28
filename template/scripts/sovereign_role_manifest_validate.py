#!/usr/bin/env python3
"""Sovereign Role-Behavior Manifest validator CLI (US-0106 / DEC-0106).

CLI contract:
  --file <path>        validate a single YAML manifest
  --repo <root>        validate repo root active + template pair
  --self-test          run lib self-test
  --enforce            exit non-zero on validation failure

Success: [SOVEREIGN_ROLE_MANIFEST_VALIDATION_OK]
Fail:    reason codes SOVEREIGN_ROLE_* (SCHEMA_INVALID / UNKNOWN_ROLE / UNKNOWN_PHASE /
         SECRET_DETECTED / OBJECTIVE_OVERFLOW)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from sovereign_role_manifest_lib import (  # noqa: E402
    MANIFEST_REL,
    ReasonCode,
    is_role_manifest_enabled,
    load_manifest,
    self_test,
    validate_manifest,
)

TEMPLATE_MANIFEST_REL = "template/.cursor/sovereign-role-manifest.yaml.example"


def _load_yaml_text(path: Path) -> Tuple[str, str | None]:
    try:
        return path.read_text(encoding="utf-8"), None
    except Exception as exc:
        return "", f"{ReasonCode.SCHEMA_INVALID.value}: cannot read {path}: {exc}"


def _validate_file(path: Path) -> Tuple[bool, List[str]]:
    text, err = _load_yaml_text(path)
    if err:
        return False, [err]
    from sovereign_role_manifest_lib import _parse_yaml_minimal
    parsed = _parse_yaml_minimal(text)
    ok, reason = validate_manifest(parsed)
    if not ok:
        return False, [f"{ReasonCode.SCHEMA_INVALID.value}: {reason}"]
    return True, []


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--file", type=Path, help="Validate a single manifest YAML")
    p.add_argument("--repo", type=Path, help="Repo root to validate active + template pair")
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--enforce", action="store_true", help="Exit non-zero on validation failure")
    args = p.parse_args()

    if args.self_test:
        ok = self_test()
        print("[SOVEREIGN_ROLE_MANIFEST_SELF_TEST_OK]" if ok else "[SOVEREIGN_ROLE_MANIFEST_SELF_TEST_FAIL]")
        return 0 if ok else 2

    if args.file:
        ok, errs = _validate_file(args.file)
        if ok:
            print(f"[SOVEREIGN_ROLE_MANIFEST_VALIDATION_OK] file={args.file}")
            return 0
        for e in errs:
            print(f"[SOVEREIGN_ROLE_MANIFEST_VALIDATION_ERROR] {e}")
        return 1 if args.enforce else 0

    if args.repo:
        root = args.repo
        active = root / MANIFEST_REL
        template = root / TEMPLATE_MANIFEST_REL
        errors: List[str] = []
        if not active.is_file():
            errors.append(f"{ReasonCode.SCHEMA_INVALID.value}: missing active manifest {active}")
        else:
            ok, errs = _validate_file(active)
            errors.extend(errs)
        if not template.is_file():
            errors.append(f"{ReasonCode.SCHEMA_INVALID.value}: missing template example {template}")
        else:
            ok, errs = _validate_file(template)
            errors.extend(errs)
        if errors:
            for e in errors:
                print(f"[SOVEREIGN_ROLE_MANIFEST_VALIDATION_ERROR] {e}")
            return 1 if args.enforce else 0
        print(f"[SOVEREIGN_ROLE_MANIFEST_VALIDATION_OK] repo={root}")
        return 0

    p.error("one of --file, --repo, --self-test is required")
    return 2


if __name__ == "__main__":
    sys.exit(main())
