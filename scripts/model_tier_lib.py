#!/usr/bin/env python3
"""
Model tier resolver library (US-0101 / DEC-0086).

Provides:
- Tier→alias resolution (cheap→fast, balanced→inherit, strong→omit)
- Local catalog schema validation
- Resolver algorithm with 4 fail-closed reason codes

Reason codes:
- MODEL_TIER_INVALID: unknown tier value
- MODEL_CATALOG_INVALID: malformed catalog JSON
- MODEL_SLUG_UNKNOWN: tier key missing from catalog
- MODEL_RESOLVE_FALLBACK: catalog lookup failed, using fallback
"""

import json
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class Tier(str, Enum):
    """Three operator-facing tiers for LLM model strength."""
    CHEAP = "cheap"
    BALANCED = "balanced"
    STRONG = "strong"


class ReasonCode(str, Enum):
    """Fail-closed reason codes for model tier resolution."""
    MODEL_TIER_INVALID = "MODEL_TIER_INVALID"
    MODEL_CATALOG_INVALID = "MODEL_CATALOG_INVALID"
    MODEL_SLUG_UNKNOWN = "MODEL_SLUG_UNKNOWN"
    MODEL_RESOLVE_FALLBACK = "MODEL_RESOLVE_FALLBACK"


# Tier→Cursor alias mapping (DEC-0086 §2)
TIER_ALIAS_MAP = {
    Tier.CHEAP: "fast",
    Tier.BALANCED: "inherit",
    Tier.STRONG: None,  # omit model: field
}

# Default phase→tier matrix (DEC-0086 §4)
DEFAULT_PHASE_TIER_MATRIX = {
    # cheap tier
    "ask": Tier.CHEAP,
    "refresh-context": Tier.CHEAP,
    "memory-audit": Tier.CHEAP,
    "status-reconcile": Tier.CHEAP,
    "pause": Tier.CHEAP,
    # balanced tier
    "intake": Tier.BALANCED,
    "discovery": Tier.BALANCED,
    "research": Tier.BALANCED,
    "release": Tier.BALANCED,
    "plan-verify": Tier.BALANCED,
    # strong tier
    "architecture": Tier.STRONG,
    "execute": Tier.STRONG,
    "quick": Tier.STRONG,
    "qa": Tier.STRONG,
    "verify-work": Tier.STRONG,
    "security-review": Tier.STRONG,
    # auto inherits parent (no tier override)
    "auto": None,
}


@dataclass
class ResolveResult:
    """Result of model tier resolution."""
    success: bool
    alias: Optional[str]  # "fast", "inherit", or None (omit)
    reason_code: Optional[ReasonCode]
    reason_message: Optional[str]
    tier: Optional[Tier] = None
    slug: Optional[str] = None  # vendor-specific slug from catalog

    @classmethod
    def success_alias(cls, tier: Tier, alias: Optional[str]) -> "ResolveResult":
        """Successful resolution with alias."""
        return cls(
            success=True,
            alias=alias,
            reason_code=None,
            reason_message=None,
            tier=tier,
        )

    @classmethod
    def success_slug(cls, tier: Tier, slug: str) -> "ResolveResult":
        """Successful resolution with vendor slug."""
        return cls(
            success=True,
            alias=None,
            reason_code=None,
            reason_message=None,
            tier=tier,
            slug=slug,
        )

    @classmethod
    def failure(cls, reason_code: ReasonCode, message: str) -> "ResolveResult":
        """Failed resolution with reason code."""
        return cls(
            success=False,
            alias=None,
            reason_code=reason_code,
            reason_message=message,
        )


def validate_catalog_schema(catalog_path: Path) -> tuple[bool, Optional[str]]:
    """
    Validate local catalog schema (DEC-0086 §3).

    Returns:
        (is_valid, error_message)
    """
    if not catalog_path.exists():
        return False, f"Catalog file not found: {catalog_path}"

    try:
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"Malformed JSON: {e}"

    # Check schema_version
    if "schema_version" not in catalog:
        return False, "Missing required field: schema_version"
    if catalog["schema_version"] != 1:
        return False, f"Unsupported schema_version: {catalog['schema_version']} (expected 1)"

    # Check tiers object
    if "tiers" not in catalog:
        return False, "Missing required field: tiers"
    tiers = catalog["tiers"]
    if not isinstance(tiers, dict):
        return False, "Field 'tiers' must be an object"

    # Check all three tier keys present
    required_tiers = {t.value for t in Tier}
    actual_tiers = set(tiers.keys())
    missing = required_tiers - actual_tiers
    if missing:
        return False, f"Missing required tier keys: {', '.join(sorted(missing))}"

    # Check tier values are non-empty strings
    for tier_name, slug in tiers.items():
        if not isinstance(slug, str) or not slug.strip():
            return False, f"Tier '{tier_name}' must have a non-empty string slug"

    return True, None


def load_catalog(catalog_path: Path) -> tuple[Optional[dict], Optional[str]]:
    """
    Load and validate catalog.

    Returns:
        (catalog_dict, error_message)
    """
    is_valid, error = validate_catalog_schema(catalog_path)
    if not is_valid:
        return None, error

    with open(catalog_path, "r", encoding="utf-8") as f:
        return json.load(f), None


def resolve_model_tier(
    phase: str,
    model_resolve: str = "alias_only",
    model_fallback: str = "inherit",
    catalog_path: Optional[Path] = None,
    tier_override: Optional[str] = None,
) -> ResolveResult:
    """
    Resolve model tier for a given phase (DEC-0086 §3 resolver algorithm).

    Args:
        phase: Canonical phase ID (e.g., "execute", "qa")
        model_resolve: Resolution strategy ("alias_only" | "local_catalog")
        model_fallback: Fallback when catalog lookup fails ("inherit")
        catalog_path: Path to local catalog (required when model_resolve="local_catalog")
        tier_override: Explicit tier override (bypasses phase matrix lookup)

    Returns:
        ResolveResult with success/failure, alias/slug, and reason code
    """
    # Step 1: Determine tier value
    tier = None
    if tier_override:
        try:
            tier = Tier(tier_override)
        except ValueError:
            return ResolveResult.failure(
                ReasonCode.MODEL_TIER_INVALID,
                f"Unknown tier value: {tier_override} (expected: cheap|balanced|strong)",
            )
    else:
        tier = DEFAULT_PHASE_TIER_MATRIX.get(phase)
        if tier is None and phase != "auto":
            # Unknown phase, use balanced as default
            tier = Tier.BALANCED

    # Step 2: Check MODEL_RESOLVE strategy
    if model_resolve == "alias_only":
        # Use built-in tier→alias mapping
        alias = TIER_ALIAS_MAP.get(tier)
        return ResolveResult.success_alias(tier, alias)

    elif model_resolve == "local_catalog":
        # Load catalog
        if not catalog_path:
            return ResolveResult.failure(
                ReasonCode.MODEL_CATALOG_INVALID,
                "MODEL_RESOLVE=local_catalog requires catalog_path",
            )

        catalog, error = load_catalog(catalog_path)
        if error:
            # Step 7: Malformed catalog
            return ResolveResult.failure(
                ReasonCode.MODEL_CATALOG_INVALID,
                error,
            )

        # Step 3: Lookup tier key in catalog
        tier_key = tier.value
        tiers = catalog["tiers"]
        if tier_key not in tiers:
            # Step 4: Key missing
            if model_fallback == "inherit":
                # Step 5: Use fallback
                return ResolveResult(
                    success=True,
                    alias="inherit",
                    reason_code=ReasonCode.MODEL_RESOLVE_FALLBACK,
                    reason_message=f"Tier '{tier_key}' not in catalog, using fallback 'inherit'",
                    tier=tier,
                )
            else:
                return ResolveResult.failure(
                    ReasonCode.MODEL_SLUG_UNKNOWN,
                    f"Tier '{tier_key}' not found in catalog {catalog_path}",
                )

        # Success: return vendor slug
        slug = tiers[tier_key]
        return ResolveResult.success_slug(tier, slug)

    else:
        return ResolveResult.failure(
            ReasonCode.MODEL_TIER_INVALID,
            f"Unknown MODEL_RESOLVE value: {model_resolve} (expected: alias_only|local_catalog)",
        )


def get_tier_for_phase(phase: str) -> Optional[Tier]:
    """Get default tier for a phase (None for 'auto')."""
    return DEFAULT_PHASE_TIER_MATRIX.get(phase)


def get_alias_for_tier(tier: Tier) -> Optional[str]:
    """Get Cursor alias for a tier (None means omit model: field)."""
    return TIER_ALIAS_MAP.get(tier)


def self_test() -> bool:
    """Run self-test to validate library contract (US-0101 / DEC-0086)."""
    print("[SELF-TEST] Validating model_tier_lib contract...")
    errors = []

    # Test 1: Tier enum values
    expected_tiers = {"cheap", "balanced", "strong"}
    actual_tiers = {t.value for t in Tier}
    if actual_tiers != expected_tiers:
        errors.append(f"Tier enum mismatch: expected {expected_tiers}, got {actual_tiers}")

    # Test 2: Phase matrix has all expected phases
    expected_phases = {
        "ask", "refresh-context", "memory-audit", "status-reconcile", "pause",
        "intake", "discovery", "research", "release", "plan-verify",
        "architecture", "execute", "quick", "qa", "verify-work", "security-review",
        "auto"
    }
    actual_phases = set(DEFAULT_PHASE_TIER_MATRIX.keys())
    if actual_phases != expected_phases:
        errors.append(f"Phase matrix mismatch: expected {expected_phases}, got {actual_phases}")

    # Test 3: Tier→alias mapping
    if TIER_ALIAS_MAP[Tier.CHEAP] != "fast":
        errors.append(f"CHEAP alias mismatch: expected 'fast', got '{TIER_ALIAS_MAP[Tier.CHEAP]}'")
    if TIER_ALIAS_MAP[Tier.BALANCED] != "inherit":
        errors.append(f"BALANCED alias mismatch: expected 'inherit', got '{TIER_ALIAS_MAP[Tier.BALANCED]}'")
    if TIER_ALIAS_MAP[Tier.STRONG] is not None:
        errors.append(f"STRONG alias mismatch: expected None, got '{TIER_ALIAS_MAP[Tier.STRONG]}'")

    # Test 4: Reason codes
    expected_codes = {"MODEL_TIER_INVALID", "MODEL_CATALOG_INVALID", "MODEL_SLUG_UNKNOWN", "MODEL_RESOLVE_FALLBACK"}
    actual_codes = {c.value for c in ReasonCode}
    if actual_codes != expected_codes:
        errors.append(f"ReasonCode mismatch: expected {expected_codes}, got {actual_codes}")

    if errors:
        print("[SELF_TEST_FAILED]")
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return False
    else:
        print("[MODEL_TIER_SELF_TEST_OK]")
        return True


if __name__ == "__main__":
    # CLI for quick testing
    import argparse

    parser = argparse.ArgumentParser(description="Model tier resolver (US-0101)")
    parser.add_argument("--phase", help="Phase ID (e.g., execute, qa)")
    parser.add_argument("--resolve", default="alias_only", choices=["alias_only", "local_catalog"])
    parser.add_argument("--fallback", default="inherit", help="Fallback strategy")
    parser.add_argument("--catalog", type=Path, help="Path to local catalog")
    parser.add_argument("--tier-override", help="Explicit tier (cheap|balanced|strong)")
    parser.add_argument("--self-test", action="store_true", help="Run self-test")

    args = parser.parse_args()

    if args.self_test:
        success = self_test()
        sys.exit(0 if success else 1)

    if not args.phase:
        parser.error("--phase is required unless --self-test is specified")

    result = resolve_model_tier(
        phase=args.phase,
        model_resolve=args.resolve,
        model_fallback=args.fallback,
        catalog_path=args.catalog,
        tier_override=args.tier_override,
    )

    if result.success:
        print(f"[OK] phase={args.phase} tier={result.tier.value}", end="")
        if result.alias:
            print(f" alias={result.alias}")
        elif result.slug:
            print(f" slug={result.slug}")
        else:
            print(" (omit model: field)")
        if result.reason_code:
            print(f"  reason={result.reason_code.value}: {result.reason_message}")
        sys.exit(0)
    else:
        print(f"[FAIL] phase={args.phase} reason={result.reason_code.value}")
        print(f"  {result.reason_message}")
        sys.exit(1)
