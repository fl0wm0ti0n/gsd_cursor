#!/usr/bin/env python3
"""
Model tier validator CLI (US-0101 / DEC-0086; US-0102 / DEC-0087; US-0123 / DEC-0123).

Validates:
- Tier enum values (cheap|balanced|strong)
- Catalog schema (v1 + v2)
- Direct MODEL_<PHASE> slug keys
- Phase key spelling (canonical phase IDs)
- Forbidden vendor slugs in template agents
- OpenCode catalog + template agents (`--scope opencode-catalog`)

Extension policy (US-0123 T-004 / DQ9): default extend-in-place in this script.
Fall back to a new `scripts/opencode_model_catalog_validate.py` ONLY if OpenCode
schema cannot share >50% of Cursor catalog helpers OR scope plumbing touches >3
unrelated `--scope` modes (DEC-0124-class follow-up).

Exit codes:
- 0: All validations passed
- 1: Validation failed (see stderr for details)
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).parent))
import host_runtime_config_lib as hrc  # noqa: E402
from model_tier_lib import (
    CANONICAL_PHASE_IDS,
    CATALOG_ROLE_KEYS,
    DEFAULT_PHASE_TIER_MATRIX,
    PRECEDENCE_CHAIN_STEPS,
    ReasonCode,
    Tier,
    catalog_validation_reason_code,
    phase_to_model_key,
    resolve_model_for_phase,
    validate_catalog_schema,
    validate_direct_slug,
)

# Reason codes used for fail-closed reporting (DEC-0086 §3 + DEC-0087 §8):
# - MODEL_TIER_INVALID: unknown tier value
# - MODEL_CATALOG_INVALID: malformed catalog JSON (v1)
# - MODEL_SLUG_UNKNOWN: tier key missing from catalog
# - MODEL_RESOLVE_FALLBACK: catalog lookup failed, using fallback
# - MODEL_OVERRIDE_SLUG_UNKNOWN: direct slug validation failure
# - MODEL_ROLE_SLUG_UNKNOWN: role catalog lookup miss
# - MODEL_CATALOG_SCHEMA_V2_INVALID: v2 schema validation failure
REASON_CODES = list(ReasonCode)

FORBIDDEN_SLUG_PATTERNS = [
    r"composer-",
    r"claude-",
    r"gpt-",
    r"opus-",
    r"glm-",
]

OPENCODE_FORBIDDEN_SLUG_PATTERNS = [
    r"deepseek",
    r"moonshot",
    r"kimi",
    r"glm",
    r"claude",
    r"gpt",
    r"sonnet",
    r"opus",
    r"haiku",
    r"o1",
    r"o3",
    r"sk-",
]

OPENCODE_ROLE_KEYS = (
    "po",
    "tech-lead",
    "dev",
    "qa",
    "release",
    "curator",
    "security",
    "auto",
)

OPENCODE_CATALOG_SCOPE = "opencode-catalog"
REASON_OPENCODE_MODEL_SLUG_UNKNOWN = "OPENCODE_MODEL_SLUG_UNKNOWN"

CANONICAL_PHASE_ID_SET = set(CANONICAL_PHASE_IDS)


def validate_tier_enum(tier_value: str) -> Tuple[bool, str]:
    """Validate tier enum value."""
    try:
        Tier(tier_value)
        return True, ""
    except ValueError:
        return False, f"Invalid tier value: {tier_value} (expected: cheap|balanced|strong)"


def validate_phase_key(phase: str) -> Tuple[bool, str]:
    """Validate phase key spelling."""
    if phase not in CANONICAL_PHASE_ID_SET:
        return False, (
            f"Unknown phase ID: {phase} "
            f"(canonical: {', '.join(sorted(CANONICAL_PHASE_ID_SET))})"
        )
    return True, ""


def check_forbidden_slugs_in_file(
    file_path: Path,
    patterns: List[str] | None = None,
) -> List[str]:
    """Check for forbidden vendor slugs in a file."""
    violations = []
    if not file_path.exists():
        return violations

    active_patterns = patterns or FORBIDDEN_SLUG_PATTERNS
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    for line_num, line in enumerate(lines, start=1):
        for pattern in active_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                violations.append(
                    f"{file_path}:{line_num}: forbidden slug pattern '{pattern}' found: {line.strip()}"
                )

    return violations


def _opencode_slug_unknown(slug: str) -> bool:
    if not slug or not str(slug).strip():
        return True
    s = str(slug).strip()
    if re.match(r"^<.*>$", s):
        return True
    if "<your-" in s:
        return True
    return False


def check_template_opencode_agents(repo_root: Path) -> List[str]:
    """US-0123: template OpenCode agents omit model: + no vendor slugs."""
    violations: List[str] = []
    agents_dir = repo_root / "template" / ".opencode" / "agents"
    if agents_dir.exists():
        for agent_file in agents_dir.glob("**/*.md"):
            content = agent_file.read_text(encoding="utf-8")
            for line_num, line in enumerate(content.split("\n"), start=1):
                if re.match(r"^\s*model\s*:", line):
                    violations.append(f"{agent_file}:{line_num}: model: must be omitted in template")
            violations.extend(
                check_forbidden_slugs_in_file(agent_file, OPENCODE_FORBIDDEN_SLUG_PATTERNS)
            )
    for cfg_name in ("opencode.json", "opencode.jsonc"):
        cfg_path = repo_root / "template" / ".opencode" / cfg_name
        if cfg_path.exists():
            violations.append(f"{cfg_path}: must not exist in template/.opencode/")
    return violations


def validate_opencode_catalog_file(catalog_path: Path) -> Tuple[bool, List[str]]:
    """Validate operator-local OpenCode catalog when present."""
    errors: List[str] = []
    try:
        data = json.loads(catalog_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, [f"[MODEL_CATALOG_INVALID] scope={OPENCODE_CATALOG_SCOPE} invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return False, [f"[MODEL_CATALOG_INVALID] scope={OPENCODE_CATALOG_SCOPE} root must be object"]

    if "schema_version" not in data:
        errors.append(f"[MODEL_CATALOG_INVALID] scope={OPENCODE_CATALOG_SCOPE} missing schema_version")
    providers = data.get("providers")
    if not isinstance(providers, dict):
        errors.append(f"[MODEL_CATALOG_INVALID] scope={OPENCODE_CATALOG_SCOPE} missing providers")
    roles = data.get("roles")
    if not isinstance(roles, dict):
        errors.append(f"[MODEL_CATALOG_INVALID] scope={OPENCODE_CATALOG_SCOPE} missing roles")
        return False, errors

    for role in OPENCODE_ROLE_KEYS:
        if role not in roles:
            errors.append(f"[MODEL_CATALOG_INVALID] scope={OPENCODE_CATALOG_SCOPE} missing role: {role}")
            continue
        value = roles[role]
        if not isinstance(value, str) or "/" not in value:
            errors.append(f"[{REASON_OPENCODE_MODEL_SLUG_UNKNOWN}] role={role} invalid assignment")
            continue
        provider, slug = value.split("/", 1)
        provider = provider.strip()
        slug = slug.strip()
        if not isinstance(providers, dict) or provider not in providers:
            errors.append(f"[{REASON_OPENCODE_MODEL_SLUG_UNKNOWN}] role={role} undeclared provider")
        elif _opencode_slug_unknown(slug):
            errors.append(f"[{REASON_OPENCODE_MODEL_SLUG_UNKNOWN}] role={role} unknown slug")

    return len(errors) == 0, errors


def check_opencode_example_catalog(repo_root: Path) -> Tuple[bool, List[str]]:
    """US-0123: example catalog placeholders only + per-role provider divergence."""
    errors: List[str] = []
    example_path = repo_root / "template" / ".opencode" / "model-catalog.local.example.json"
    if not example_path.is_file():
        errors.append(f"missing example catalog: {example_path}")
        return False, errors

    try:
        data = json.loads(example_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, [f"[MODEL_CATALOG_INVALID] scope={OPENCODE_CATALOG_SCOPE} example JSON: {exc}"]

    roles = data.get("roles", {})
    providers_seen: set[str] = set()
    placeholder_re = re.compile(r"^[^/]+/<your-[^>]+-slug>$")

    for role in OPENCODE_ROLE_KEYS:
        value = roles.get(role)
        if not isinstance(value, str) or not placeholder_re.match(value.strip()):
            errors.append(f"example catalog role {role} must use <your-*-slug> placeholder form")

    for role in OPENCODE_ROLE_KEYS:
        value = roles.get(role, "")
        if isinstance(value, str) and "/" in value:
            providers_seen.add(value.split("/", 1)[0].strip())
    if len(providers_seen) < 2:
        errors.append("example catalog must have ≥2 roles with different providers")

    return len(errors) == 0, errors


def run_opencode_catalog_scope(repo_root: Path) -> List[str]:
    """Run all checks for --scope opencode-catalog."""
    errors: List[str] = []
    print(f"[OPENCODE] Checking template/.opencode/agents...")
    errors.extend(check_template_opencode_agents(repo_root))

    catalog_path = repo_root / ".opencode" / "model-catalog.local.json"
    if catalog_path.is_file():
        print(f"[OPENCODE] Validating {catalog_path}...")
        ok, cat_errors = validate_opencode_catalog_file(catalog_path)
        if not ok:
            errors.extend(cat_errors)
    else:
        print(f"[OPENCODE] No local catalog at {catalog_path} (optional — skip)")

    print(f"[OPENCODE] Checking example catalog...")
    ok, ex_errors = check_opencode_example_catalog(repo_root)
    if not ok:
        errors.extend(ex_errors)

    return errors


def check_template_agents(repo_root: Path) -> List[str]:
    """Check template/.cursor/agents/*.mdc for forbidden slugs."""
    violations = []
    agents_dir = repo_root / "template" / ".cursor" / "agents"

    if not agents_dir.exists():
        return violations

    for agent_file in agents_dir.glob("*.mdc"):
        violations.extend(check_forbidden_slugs_in_file(agent_file))

    return violations


def parse_scratchpad_keys(scratchpad_path: Path) -> Dict[str, str]:
    """Parse key=value lines from scratchpad (skip comments)."""
    result: Dict[str, str] = {}
    if not scratchpad_path.exists():
        return result
    for line in scratchpad_path.read_text(encoding="utf-8").split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" in stripped:
            key, value = stripped.split("=", 1)
            result[key.strip()] = value.strip()
    return result


def validate_catalog(catalog_path: Path) -> Tuple[bool, List[str], ReasonCode]:
    """Validate catalog schema and return list of errors."""
    errors: List[str] = []

    if not catalog_path.exists():
        errors.append(f"Catalog file not found: {catalog_path}")
        return False, errors, ReasonCode.MODEL_CATALOG_INVALID

    is_valid, error_msg = validate_catalog_schema(catalog_path)
    if not is_valid:
        schema_version = None
        try:
            with open(catalog_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                schema_version = data.get("schema_version")
        except (json.JSONDecodeError, OSError):
            pass
        code = catalog_validation_reason_code(
            error_msg,
            {"schema_version": schema_version} if schema_version else None,
        )
        errors.append(error_msg or "Catalog validation failed")
        return False, errors, code

    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    for tier_name, slug in catalog["tiers"].items():
        if not slug.strip():
            errors.append(f"Tier '{tier_name}' has empty slug")

    if catalog.get("schema_version") == 2 and "roles" in catalog:
        for role_name in CATALOG_ROLE_KEYS:
            if role_name not in catalog["roles"]:
                errors.append(f"Missing role key: {role_name}")
            elif not catalog["roles"][role_name].strip():
                errors.append(f"Role '{role_name}' has empty slug")
        if "critic" in catalog["roles"]:
            critic_slug = catalog["roles"].get("critic")
            if not isinstance(critic_slug, str) or not critic_slug.strip():
                errors.append("Role 'critic' must have a non-empty string slug")

    code = (
        ReasonCode.MODEL_CATALOG_SCHEMA_V2_INVALID
        if catalog.get("schema_version") == 2
        else ReasonCode.MODEL_CATALOG_INVALID
    )
    return len(errors) == 0, errors, code


def validate_scratchpad_tiers(scratchpad_path: Path) -> Tuple[bool, List[str]]:
    """Validate MODEL_TIER_* keys in scratchpad file."""
    errors: List[str] = []

    if not scratchpad_path.exists():
        return True, errors

    content = scratchpad_path.read_text(encoding="utf-8")

    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("MODEL_TIER_") and "=" in line:
            key, value = line.split("=", 1)
            value = value.strip()

            if key.startswith("#"):
                continue

            if value and not value.startswith("<"):
                is_valid, error = validate_tier_enum(value)
                if not is_valid:
                    errors.append(f"{key}={value}: {error}")

    return len(errors) == 0, errors


def validate_scratchpad_direct_slugs(scratchpad_path: Path, catalog: dict | None) -> Tuple[bool, List[str]]:
    """Validate MODEL_<PHASE> direct override keys."""
    errors: List[str] = []
    pad = parse_scratchpad_keys(scratchpad_path)
    model_resolve = pad.get("MODEL_RESOLVE", "alias_only")

    for phase_id in CANONICAL_PHASE_ID_SET:
        key = phase_to_model_key(phase_id)
        if key in pad and pad[key].strip() and not pad[key].startswith("<"):
            slug = pad[key].strip()
            is_valid, error = validate_direct_slug(slug, model_resolve, catalog)
            if not is_valid:
                errors.append(f"{key}={slug}: {error} [{ReasonCode.MODEL_OVERRIDE_SLUG_UNKNOWN.value}]")

    return len(errors) == 0, errors


def run_precedence_self_test() -> List[str]:
    """Precedence self-test hook (DEC-0087)."""
    errors: List[str] = []

    if len(PRECEDENCE_CHAIN_STEPS) != 5:
        errors.append("PRECEDENCE_CHAIN_STEPS must have exactly 5 steps")

    # Step 1 wins over tier
    pad = {"MODEL_EXECUTE": "<test-slug>", "MODEL_TIER_EXECUTE": "cheap", "MODEL_RESOLVE": "alias_only"}
    result = resolve_model_for_phase("execute", pad)
    if not result.success or result.slug != "<test-slug>":
        errors.append("Precedence self-test: MODEL_EXECUTE should win step 1")

    # Tier-only backward compat: execute → strong → omit alias
    result = resolve_model_for_phase("execute", {"MODEL_RESOLVE": "alias_only"})
    if not result.success or result.tier != Tier.STRONG or result.alias is not None:
        errors.append("Precedence self-test: tier-only execute should resolve to strong/omit")

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Model tier validator (US-0101 / US-0102)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/model_tier_validate.py --repo .
  python scripts/model_tier_validate.py --catalog .cursor/model-catalog.local.json
  python scripts/model_tier_validate.py --check-template-agents
  python scripts/model_tier_validate.py --enforce
  python scripts/model_tier_validate.py --scope opencode-catalog --repo .
        """,
    )

    parser.add_argument("--repo", type=Path, help="Repository root (default: current directory)")
    parser.add_argument(
        "--scope",
        choices=("opencode-catalog",),
        help="Validation scope (US-0123 OpenCode catalog surface)",
    )
    parser.add_argument("--catalog", type=Path, help="Path to local catalog")
    parser.add_argument("--scratchpad", type=Path, help="Path to scratchpad file")
    parser.add_argument("--check-template-agents", action="store_true", help="Check template agents for forbidden slugs")
    parser.add_argument("--self-test", action="store_true", help="Run self-test (validate library contract)")
    parser.add_argument("--enforce", action="store_true", help="Exit non-zero on any fail-closed code")

    args = parser.parse_args()

    repo_root = (args.repo or Path.cwd()).resolve()
    all_errors: List[str] = []

    if args.scope == OPENCODE_CATALOG_SCOPE:
        all_errors = run_opencode_catalog_scope(repo_root)
        if all_errors:
            print(f"\n[MODEL_TIER_VALIDATION_FAILED] {len(all_errors)} error(s)", file=sys.stderr)
            for error in all_errors:
                print(f"  {error}", file=sys.stderr)
            sys.exit(1)
        print("\n[MODEL_TIER_VALIDATION_OK]")
        sys.exit(0)

    if args.self_test:
        print("[SELF-TEST] Validating model_tier_lib contract...")

        for tier in Tier:
            is_valid, error = validate_tier_enum(tier.value)
            if not is_valid:
                all_errors.append(f"Self-test failed: {error}")

        for phase in CANONICAL_PHASE_ID_SET:
            is_valid, error = validate_phase_key(phase)
            if not is_valid:
                all_errors.append(f"Self-test failed: {error}")

        test_content = "model: composer-1"
        for pattern in FORBIDDEN_SLUG_PATTERNS:
            if not re.search(pattern, test_content, re.IGNORECASE):
                all_errors.append(f"Self-test failed: pattern '{pattern}' not matching test content")

        all_errors.extend(run_precedence_self_test())

        for code in (
            ReasonCode.MODEL_OVERRIDE_SLUG_UNKNOWN,
            ReasonCode.MODEL_ROLE_SLUG_UNKNOWN,
            ReasonCode.MODEL_CATALOG_SCHEMA_V2_INVALID,
        ):
            if code not in ReasonCode:
                all_errors.append(f"Self-test failed: missing reason code {code.value}")

        if all_errors:
            print("[SELF_TEST_FAILED]")
            for error in all_errors:
                print(f"  {error}", file=sys.stderr)
            sys.exit(1)
        else:
            print("[DEV_ENVIRONMENT_SELF_TEST_OK]")
            sys.exit(0)

    catalog_dict = None

    if args.catalog:
        print(f"[CATALOG] Validating {args.catalog}...")
        is_valid, errors, code = validate_catalog(args.catalog)
        if not is_valid:
            all_errors.extend(f"[{code.value}] {e}" for e in errors)
            print(f"[CATALOG_INVALID] {args.catalog}", file=sys.stderr)
            for error in errors:
                print(f"  [{code.value}] {error}", file=sys.stderr)
        else:
            with open(args.catalog, "r", encoding="utf-8") as f:
                catalog_dict = json.load(f)

    if args.scratchpad:
        print(f"[SCRATCHPAD] Validating {args.scratchpad}...")
        is_valid, errors = validate_scratchpad_tiers(args.scratchpad)
        if not is_valid:
            all_errors.extend(errors)
        is_valid, errors = validate_scratchpad_direct_slugs(args.scratchpad, catalog_dict)
        if not is_valid:
            all_errors.extend(errors)

    if args.check_template_agents:
        print(f"[TEMPLATE] Checking {repo_root / 'template' / '.cursor' / 'agents'}...")
        violations = check_template_agents(repo_root)
        if violations:
            all_errors.extend(violations)

    if not args.catalog and not args.scratchpad and not args.check_template_agents:
        print(f"[REPO] Validating {repo_root}...")

        for example_name in (
            "model-catalog.local.example.json",
            "model-catalog.local.example.role-based-balanced.json",
            "model-catalog.local.example.role-based-highend.json",
        ):
            catalog_example = repo_root / ".cursor" / example_name
            if catalog_example.exists():
                print(f"[CATALOG] Validating {catalog_example}...")
                is_valid, errors, code = validate_catalog(catalog_example)
                if not is_valid:
                    all_errors.extend(f"[{code.value}] {e}" for e in errors)

        scratchpad = repo_root / ".cursor" / "scratchpad.md"
        # US-0131 path inject only — do not reinterpret/validate MODEL_* here (US-0132).
        _ = hrc.resolve_runtime_config(repo_root, raise_on_fatal=False)
        if scratchpad.exists():
            print(f"[SCRATCHPAD] Validating {scratchpad}...")
            is_valid, errors = validate_scratchpad_tiers(scratchpad)
            if not is_valid:
                all_errors.extend(errors)

        print(f"[TEMPLATE] Checking {repo_root / 'template' / '.cursor' / 'agents'}...")
        violations = check_template_agents(repo_root)
        if violations:
            all_errors.extend(violations)

        all_errors.extend(run_precedence_self_test())

    if all_errors:
        print(f"\n[MODEL_TIER_VALIDATION_FAILED] {len(all_errors)} error(s)", file=sys.stderr)
        for error in all_errors:
            print(f"  {error}", file=sys.stderr)
        sys.exit(1 if args.enforce or True else 0)
    else:
        print("\n[MODEL_TIER_VALIDATION_OK]")
        sys.exit(0)


if __name__ == "__main__":
    main()
