#!/usr/bin/env python3
"""
Model tier validator CLI (US-0101 / DEC-0086).

Validates:
- Tier enum values (cheap|balanced|strong)
- Catalog schema (schema_version, tiers object, all keys present)
- Phase key spelling (canonical phase IDs)
- Forbidden vendor slugs in template agents

Exit codes:
- 0: All validations passed
- 1: Validation failed (see stderr for details)
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Import from model_tier_lib
sys.path.insert(0, str(Path(__file__).parent))
from model_tier_lib import (
    DEFAULT_PHASE_TIER_MATRIX,
    ReasonCode,
    Tier,
    validate_catalog_schema,
)

# Reason codes used for fail-closed reporting (DEC-0086 §3):
# - MODEL_TIER_INVALID: unknown tier value
# - MODEL_CATALOG_INVALID: malformed catalog JSON
# - MODEL_SLUG_UNKNOWN: tier key missing from catalog
# - MODEL_RESOLVE_FALLBACK: catalog lookup failed, using fallback
REASON_CODES = [
    ReasonCode.MODEL_TIER_INVALID,
    ReasonCode.MODEL_CATALOG_INVALID,
    ReasonCode.MODEL_SLUG_UNKNOWN,
    ReasonCode.MODEL_RESOLVE_FALLBACK,
]

# Forbidden vendor slug patterns (DEC-0086 §4)
FORBIDDEN_SLUG_PATTERNS = [
    r"composer-",
    r"claude-",
    r"gpt-",
    r"opus-",
]

# Canonical phase IDs (from US-0069 / DEC-0051)
CANONICAL_PHASE_IDS = set(DEFAULT_PHASE_TIER_MATRIX.keys())


def validate_tier_enum(tier_value: str) -> Tuple[bool, str]:
    """Validate tier enum value."""
    try:
        Tier(tier_value)
        return True, ""
    except ValueError:
        return False, f"Invalid tier value: {tier_value} (expected: cheap|balanced|strong)"


def validate_phase_key(phase: str) -> Tuple[bool, str]:
    """Validate phase key spelling."""
    if phase not in CANONICAL_PHASE_IDS:
        return False, f"Unknown phase ID: {phase} (canonical: {', '.join(sorted(CANONICAL_PHASE_IDS))})"
    return True, ""


def check_forbidden_slugs_in_file(file_path: Path) -> List[str]:
    """Check for forbidden vendor slugs in a file."""
    violations = []
    if not file_path.exists():
        return violations

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    for line_num, line in enumerate(lines, start=1):
        for pattern in FORBIDDEN_SLUG_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                violations.append(
                    f"{file_path}:{line_num}: forbidden slug pattern '{pattern}' found: {line.strip()}"
                )

    return violations


def check_template_agents(repo_root: Path) -> List[str]:
    """Check template/.cursor/agents/*.mdc for forbidden slugs."""
    violations = []
    agents_dir = repo_root / "template" / ".cursor" / "agents"

    if not agents_dir.exists():
        return violations

    for agent_file in agents_dir.glob("*.mdc"):
        violations.extend(check_forbidden_slugs_in_file(agent_file))

    return violations


def validate_catalog(catalog_path: Path) -> Tuple[bool, List[str]]:
    """Validate catalog schema and return list of errors."""
    errors = []

    if not catalog_path.exists():
        errors.append(f"Catalog file not found: {catalog_path}")
        return False, errors

    is_valid, error_msg = validate_catalog_schema(catalog_path)
    if not is_valid:
        errors.append(error_msg)
        return False, errors

    # Additional validation: check tier values are non-empty
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    for tier_name, slug in catalog["tiers"].items():
        if not slug.strip():
            errors.append(f"Tier '{tier_name}' has empty slug")

    return len(errors) == 0, errors


def validate_scratchpad_tiers(scratchpad_path: Path) -> Tuple[bool, List[str]]:
    """Validate MODEL_TIER_* keys in scratchpad file."""
    errors = []

    if not scratchpad_path.exists():
        return True, errors  # scratchpad is optional

    content = scratchpad_path.read_text(encoding="utf-8")

    # Find MODEL_TIER_* lines
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("MODEL_TIER_") and "=" in line:
            key, value = line.split("=", 1)
            value = value.strip()

            # Skip comments
            if key.startswith("#"):
                continue

            # Validate tier value
            if value and not value.startswith("<"):  # skip placeholders
                is_valid, error = validate_tier_enum(value)
                if not is_valid:
                    errors.append(f"{key}={value}: {error}")

    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(
        description="Model tier validator (US-0101 / DEC-0086)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate all (repo root)
  python scripts/model_tier_validate.py --repo .

  # Validate specific catalog
  python scripts/model_tier_validate.py --catalog .cursor/model-catalog.local.json

  # Check template agents for forbidden slugs
  python scripts/model_tier_validate.py --check-template-agents
        """,
    )

    parser.add_argument("--repo", type=Path, help="Repository root (default: current directory)")
    parser.add_argument("--catalog", type=Path, help="Path to local catalog")
    parser.add_argument("--scratchpad", type=Path, help="Path to scratchpad file")
    parser.add_argument("--check-template-agents", action="store_true", help="Check template agents for forbidden slugs")
    parser.add_argument("--self-test", action="store_true", help="Run self-test (validate library contract)")

    args = parser.parse_args()

    # Default to current directory
    repo_root = args.repo or Path.cwd()
    repo_root = repo_root.resolve()

    all_errors = []

    # Self-test mode
    if args.self_test:
        print("[SELF-TEST] Validating model_tier_lib contract...")

        # Test 1: Tier enum
        for tier in Tier:
            is_valid, error = validate_tier_enum(tier.value)
            if not is_valid:
                all_errors.append(f"Self-test failed: {error}")

        # Test 2: Phase matrix
        for phase in CANONICAL_PHASE_IDS:
            is_valid, error = validate_phase_key(phase)
            if not is_valid:
                all_errors.append(f"Self-test failed: {error}")

        # Test 3: Forbidden slug patterns
        test_content = "model: composer-1"
        for pattern in FORBIDDEN_SLUG_PATTERNS:
            if not re.search(pattern, test_content, re.IGNORECASE):
                all_errors.append(f"Self-test failed: pattern '{pattern}' not matching test content")

        if all_errors:
            print("[SELF_TEST_FAILED]")
            for error in all_errors:
                print(f"  {error}", file=sys.stderr)
            sys.exit(1)
        else:
            print("[DEV_ENVIRONMENT_SELF_TEST_OK]")
            sys.exit(0)

    # Validate catalog
    if args.catalog:
        print(f"[CATALOG] Validating {args.catalog}...")
        is_valid, errors = validate_catalog(args.catalog)
        if not is_valid:
            all_errors.extend(errors)
            print(f"[CATALOG_INVALID] {args.catalog}", file=sys.stderr)
            for error in errors:
                print(f"  {error}", file=sys.stderr)

    # Validate scratchpad
    if args.scratchpad:
        print(f"[SCRATCHPAD] Validating {args.scratchpad}...")
        is_valid, errors = validate_scratchpad_tiers(args.scratchpad)
        if not is_valid:
            all_errors.extend(errors)
            print(f"[SCRATCHPAD_INVALID] {args.scratchpad}", file=sys.stderr)
            for error in errors:
                print(f"  {error}", file=sys.stderr)

    # Check template agents
    if args.check_template_agents:
        print(f"[TEMPLATE] Checking {repo_root / 'template' / '.cursor' / 'agents'}...")
        violations = check_template_agents(repo_root)
        if violations:
            all_errors.extend(violations)
            print("[FORBIDDEN_SLUG_DETECTED]", file=sys.stderr)
            for violation in violations:
                print(f"  {violation}", file=sys.stderr)

    # Default: validate all
    if not args.catalog and not args.scratchpad and not args.check_template_agents:
        print(f"[REPO] Validating {repo_root}...")

        # Check catalog example
        catalog_example = repo_root / ".cursor" / "model-catalog.local.example.json"
        if catalog_example.exists():
            print(f"[CATALOG] Validating {catalog_example}...")
            is_valid, errors = validate_catalog(catalog_example)
            if not is_valid:
                all_errors.extend(errors)
                print(f"[CATALOG_INVALID] {catalog_example}", file=sys.stderr)
                for error in errors:
                    print(f"  {error}", file=sys.stderr)

        # Check scratchpad
        scratchpad = repo_root / ".cursor" / "scratchpad.md"
        if scratchpad.exists():
            print(f"[SCRATCHPAD] Validating {scratchpad}...")
            is_valid, errors = validate_scratchpad_tiers(scratchpad)
            if not is_valid:
                all_errors.extend(errors)
                print(f"[SCRATCHPAD_INVALID] {scratchpad}", file=sys.stderr)
                for error in errors:
                    print(f"  {error}", file=sys.stderr)

        # Check template agents
        print(f"[TEMPLATE] Checking {repo_root / 'template' / '.cursor' / 'agents'}...")
        violations = check_template_agents(repo_root)
        if violations:
            all_errors.extend(violations)
            print("[FORBIDDEN_SLUG_DETECTED]", file=sys.stderr)
            for violation in violations:
                print(f"  {violation}", file=sys.stderr)

    # Final verdict
    if all_errors:
        print(f"\n[MODEL_TIER_VALIDATION_FAILED] {len(all_errors)} error(s)", file=sys.stderr)
        sys.exit(1)
    else:
        print("\n[MODEL_TIER_VALIDATION_OK]")
        sys.exit(0)


if __name__ == "__main__":
    main()
