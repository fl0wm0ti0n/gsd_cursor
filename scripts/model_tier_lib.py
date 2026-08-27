#!/usr/bin/env python3
"""
Model tier resolver library (US-0101 / DEC-0086; US-0102 / DEC-0087).

Provides:
- Tier→alias resolution (cheap→fast, balanced→inherit, strong→omit)
- Local catalog schema validation (v1 + v2)
- Unified 5-step precedence resolver (US-0102)
- Resolver algorithm with fail-closed reason codes

Reason codes (DEC-0086):
- MODEL_TIER_INVALID: unknown tier value
- MODEL_CATALOG_INVALID: malformed catalog JSON (v1)
- MODEL_SLUG_UNKNOWN: tier key missing from catalog
- MODEL_RESOLVE_FALLBACK: catalog lookup failed, using fallback

Reason codes (DEC-0087):
- MODEL_OVERRIDE_SLUG_UNKNOWN: direct slug validation failure
- MODEL_ROLE_SLUG_UNKNOWN: role catalog lookup miss (fall through)
- MODEL_CATALOG_SCHEMA_V2_INVALID: v2 schema validation failure
"""

import json
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, Optional


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
    MODEL_OVERRIDE_SLUG_UNKNOWN = "MODEL_OVERRIDE_SLUG_UNKNOWN"
    MODEL_ROLE_SLUG_UNKNOWN = "MODEL_ROLE_SLUG_UNKNOWN"
    MODEL_CATALOG_SCHEMA_V2_INVALID = "MODEL_CATALOG_SCHEMA_V2_INVALID"


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

# Canonical phase ids for MODEL_<PHASE> keys (DEC-0086 + DEC-0087)
CANONICAL_PHASE_IDS = frozenset(DEFAULT_PHASE_TIER_MATRIX.keys())

# Catalog v2 role keys (DEC-0087 §5)
CATALOG_ROLE_KEYS = frozenset({
    "po", "sa", "dev", "dev_difficult", "qa", "security", "release",
})

# US-0130 optional overlay — not in the required set (DQ1).
CATALOG_OPTIONAL_ROLE_KEYS = frozenset({"critic"})

# Phase→logical role (DEC-0051 + DEC-0087 §6)
PHASE_LOGICAL_ROLE: Dict[str, Optional[str]] = {
    "intake": "po",
    "discovery": "po",
    "research": "tech-lead",
    "architecture": "tech-lead",
    "plan-verify": "qa",
    "execute": "dev",
    "quick": "dev",
    "qa": "qa",
    "verify-work": "qa",
    "security-review": "security",
    "release": "release",
    "refresh-context": "curator",
    "ask": "dev",
    "memory-audit": "dev",
    "status-reconcile": "dev",
    "pause": "dev",
    "auto": None,
}

# Logical role → catalog roles key (DEC-0087 §6)
LOGICAL_ROLE_TO_CATALOG_KEY = {
    "po": "po",
    "tech-lead": "sa",
    "dev": "dev",
    "qa": "qa",
    "security": "security",
    "release": "release",
    "curator": "dev",
}

# 5-step precedence chain labels (DEC-0087 §2) — for contract tests / docs
PRECEDENCE_CHAIN_STEPS = (
    "MODEL_<PHASE>",
    "MODEL_TIER_<PHASE>",
    "role_catalog_lookup",
    "MODEL_TIER_DEFAULT",
    "cursor_alias",
)


def phase_to_model_key(phase_id: str) -> str:
    """Scratchpad key for direct slug override: MODEL_<PHASE>."""
    return f"MODEL_{phase_id.upper()}"


def phase_to_tier_key(phase_id: str) -> str:
    """Scratchpad key for tier override: MODEL_TIER_<PHASE>."""
    return f"MODEL_TIER_{phase_id.upper()}"


@dataclass
class ResolveResult:
    """Result of model tier resolution."""
    success: bool
    alias: Optional[str]  # "fast", "inherit", or None (omit)
    reason_code: Optional[ReasonCode]
    reason_message: Optional[str]
    tier: Optional[Tier] = None
    slug: Optional[str] = None  # vendor-specific slug from catalog or direct override

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
    def success_slug(cls, tier: Optional[Tier], slug: str) -> "ResolveResult":
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

    @classmethod
    def fallthrough(
        cls,
        reason_code: ReasonCode,
        message: str,
    ) -> "ResolveResult":
        """Emit reason code but signal fall-through (role catalog miss)."""
        return cls(
            success=False,
            alias=None,
            reason_code=reason_code,
            reason_message=message,
        )


def _validate_tiers_object(tiers: object) -> Optional[str]:
    """Validate tiers object; return error message or None."""
    if not isinstance(tiers, dict):
        return "Field 'tiers' must be an object"
    required_tiers = {t.value for t in Tier}
    actual_tiers = set(tiers.keys())
    missing = required_tiers - actual_tiers
    if missing:
        return f"Missing required tier keys: {', '.join(sorted(missing))}"
    for tier_name, slug in tiers.items():
        if not isinstance(slug, str) or not slug.strip():
            return f"Tier '{tier_name}' must have a non-empty string slug"
    return None


def _validate_roles_object(roles: object) -> Optional[str]:
    """Validate v2 roles object; return error message or None."""
    if not isinstance(roles, dict):
        return "Field 'roles' must be an object"
    actual_keys = set(roles.keys())
    missing = CATALOG_ROLE_KEYS - actual_keys
    extra = actual_keys - CATALOG_ROLE_KEYS - CATALOG_OPTIONAL_ROLE_KEYS
    if missing:
        return f"Missing required role keys: {', '.join(sorted(missing))}"
    if extra:
        return f"Unknown role keys: {', '.join(sorted(extra))}"
    for role_name, slug in roles.items():
        if not isinstance(slug, str) or not slug.strip():
            return f"Role '{role_name}' must have a non-empty string slug"
    return None


def validate_catalog_schema(catalog_path: Path) -> tuple[bool, Optional[str]]:
    """
    Validate local catalog schema (DEC-0086 v1 + DEC-0087 v2).

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

    if "schema_version" not in catalog:
        return False, "Missing required field: schema_version"

    schema_version = catalog["schema_version"]
    if schema_version not in (1, 2):
        return False, f"Unsupported schema_version: {schema_version} (expected 1 or 2)"

    if "tiers" not in catalog:
        return False, "Missing required field: tiers"

    tiers_error = _validate_tiers_object(catalog["tiers"])
    if tiers_error:
        if schema_version == 2:
            return False, f"v2 schema error: {tiers_error}"
        return False, tiers_error

    if schema_version == 2 and "roles" in catalog:
        roles_error = _validate_roles_object(catalog["roles"])
        if roles_error:
            return False, f"v2 schema error: {roles_error}"

    return True, None


def catalog_validation_reason_code(error_message: Optional[str], catalog: Optional[dict]) -> ReasonCode:
    """Pick fail-closed reason code for catalog validation failure."""
    if catalog and catalog.get("schema_version") == 2:
        return ReasonCode.MODEL_CATALOG_SCHEMA_V2_INVALID
    if error_message and "v2 schema error" in error_message:
        return ReasonCode.MODEL_CATALOG_SCHEMA_V2_INVALID
    return ReasonCode.MODEL_CATALOG_INVALID


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


def _catalog_contains_slug(catalog: dict, slug: str) -> bool:
    """Check whether slug appears in catalog tiers or roles values."""
    tiers = catalog.get("tiers", {})
    if slug in tiers.values():
        return True
    roles = catalog.get("roles", {})
    if isinstance(roles, dict) and slug in roles.values():
        return True
    return False


def validate_direct_slug(
    slug: str,
    model_resolve: str,
    catalog: Optional[dict],
) -> tuple[bool, Optional[str]]:
    """
    Validate direct MODEL_<PHASE> slug per DEC-0087 §4.

    Returns:
        (is_valid, error_message)
    """
    if not slug or not slug.strip():
        return False, "Direct slug override must be a non-empty string"

    if model_resolve == "alias_only":
        return True, None

    if model_resolve in ("local_catalog", "role_catalog"):
        if not catalog:
            return False, "Direct slug validation requires catalog when MODEL_RESOLVE is local_catalog or role_catalog"
        if not _catalog_contains_slug(catalog, slug):
            return False, f"Slug '{slug}' not found in catalog tiers or roles"
        return True, None

    return False, f"Unknown MODEL_RESOLVE value: {model_resolve}"


def resolve_logical_role(phase_id: str, scratchpad: Dict[str, str]) -> Optional[str]:
    """Resolve phase to logical role with AUTO_ROLE_* policy overrides."""
    if phase_id == "auto":
        return None

    base_role = PHASE_LOGICAL_ROLE.get(phase_id)
    if base_role is None:
        return "dev"

    if phase_id == "research":
        override = scratchpad.get("AUTO_ROLE_RESEARCH", "").strip()
        if override in ("po", "tech-lead"):
            return override
        return base_role

    if phase_id == "plan-verify":
        override = scratchpad.get("AUTO_ROLE_PLAN_VERIFY", "").strip()
        if override in ("qa", "tech-lead"):
            return override
        return base_role

    if phase_id == "refresh-context":
        override = scratchpad.get("AUTO_ROLE_REFRESH_CONTEXT", "").strip()
        if override in ("curator", "po"):
            return override
        return base_role

    return base_role


def _resolve_tier_chain(
    phase_id: str,
    tier: Optional[Tier],
    model_resolve: str,
    model_fallback: str,
    catalog: Optional[dict],
) -> ResolveResult:
    """DEC-0086 tier→alias / local_catalog chain for a resolved tier."""
    if tier is None:
        return ResolveResult.success_alias(None, None)

    if model_resolve == "alias_only":
        alias = TIER_ALIAS_MAP.get(tier)
        return ResolveResult.success_alias(tier, alias)

    if model_resolve == "local_catalog" or model_resolve == "role_catalog":
        if not catalog:
            return ResolveResult.failure(
                ReasonCode.MODEL_CATALOG_INVALID,
                "MODEL_RESOLVE=local_catalog requires catalog",
            )

        tier_key = tier.value
        tiers = catalog.get("tiers", {})
        if tier_key not in tiers:
            if model_fallback == "inherit":
                return ResolveResult(
                    success=True,
                    alias="inherit",
                    reason_code=ReasonCode.MODEL_RESOLVE_FALLBACK,
                    reason_message=f"Tier '{tier_key}' not in catalog, using fallback 'inherit'",
                    tier=tier,
                )
            return ResolveResult.failure(
                ReasonCode.MODEL_SLUG_UNKNOWN,
                f"Tier '{tier_key}' not found in catalog",
            )

        slug = tiers[tier_key]
        return ResolveResult.success_slug(tier, slug)

    return ResolveResult.failure(
        ReasonCode.MODEL_TIER_INVALID,
        f"Unknown MODEL_RESOLVE value: {model_resolve} (expected: alias_only|local_catalog|role_catalog)",
    )


def _resolve_tier_for_phase(
    phase_id: str,
    scratchpad: Dict[str, str],
    use_default_only: bool = False,
) -> Optional[Tier]:
    """Resolve tier from MODEL_TIER_<PHASE> or phase matrix / default."""
    if use_default_only:
        default = scratchpad.get("MODEL_TIER_DEFAULT", "balanced").strip()
        try:
            return Tier(default)
        except ValueError:
            return Tier.BALANCED

    tier_key = phase_to_tier_key(phase_id)
    if tier_key in scratchpad and scratchpad[tier_key].strip():
        try:
            return Tier(scratchpad[tier_key].strip())
        except ValueError:
            return None

    tier = DEFAULT_PHASE_TIER_MATRIX.get(phase_id)
    if tier is not None:
        return tier

    if phase_id == "auto":
        return None

    default = scratchpad.get("MODEL_TIER_DEFAULT", "balanced").strip()
    try:
        return Tier(default)
    except ValueError:
        return Tier.BALANCED


def resolve_model_for_phase(
    phase_id: str,
    scratchpad: Optional[Dict[str, str]] = None,
    catalog: Optional[dict] = None,
    catalog_path: Optional[Path] = None,
) -> ResolveResult:
    """
    Unified 5-step precedence resolver (DEC-0087 §2).

    Precedence:
    1. MODEL_<PHASE> direct slug
    2. MODEL_TIER_<PHASE> → DEC-0086 tier chain
    3. MODEL_RESOLVE=role_catalog → phase→role→catalog slug (fall through on miss)
    4. MODEL_TIER_DEFAULT → DEC-0086 tier chain
    5. Cursor stable alias
    """
    pad = scratchpad or {}
    model_resolve = pad.get("MODEL_RESOLVE", "alias_only").strip() or "alias_only"
    model_fallback = pad.get("MODEL_FALLBACK", "inherit").strip() or "inherit"

    if catalog is None and catalog_path is not None:
        catalog, catalog_error = load_catalog(catalog_path)
        if catalog_error:
            code = catalog_validation_reason_code(catalog_error, None)
            return ResolveResult.failure(code, catalog_error)

    # Step 1: MODEL_<PHASE> direct slug override
    model_key = phase_to_model_key(phase_id)
    if model_key in pad and pad[model_key].strip():
        slug = pad[model_key].strip()
        is_valid, error = validate_direct_slug(slug, model_resolve, catalog)
        if not is_valid:
            return ResolveResult.failure(
                ReasonCode.MODEL_OVERRIDE_SLUG_UNKNOWN,
                error or "Direct slug validation failed",
            )
        return ResolveResult.success_slug(None, slug)

    # Step 2: MODEL_TIER_<PHASE> tier chain (skipped when role_catalog — step 3 handles slug)
    if model_resolve in ("alias_only", "local_catalog"):
        tier = _resolve_tier_for_phase(phase_id, pad, use_default_only=False)
        if tier is not None:
            result = _resolve_tier_chain(phase_id, tier, model_resolve, model_fallback, catalog)
            if result.success:
                return result
            if result.reason_code != ReasonCode.MODEL_RESOLVE_FALLBACK:
                return result

    # Step 3: role catalog lookup (opt-in)
    if model_resolve == "role_catalog" and phase_id != "auto":
        logical_role = resolve_logical_role(phase_id, pad)
        if logical_role:
            catalog_role_key = LOGICAL_ROLE_TO_CATALOG_KEY.get(logical_role)
            if catalog and catalog_role_key:
                roles = catalog.get("roles")
                if isinstance(roles, dict) and catalog_role_key in roles:
                    slug = roles[catalog_role_key]
                    if slug and slug.strip():
                        return ResolveResult.success_slug(None, slug.strip())
            # Miss → fall through with reason (not hard stop)
            # Continue to step 4; reason emitted via optional metadata on result path

    # Step 4: MODEL_TIER_DEFAULT tier chain
    default_tier = _resolve_tier_for_phase(phase_id, pad, use_default_only=True)
    if default_tier is not None:
        result = _resolve_tier_chain(phase_id, default_tier, model_resolve, model_fallback, catalog)
        if result.success:
            return result

    # Step 5: Cursor alias from phase matrix tier or balanced default
    fallback_tier = DEFAULT_PHASE_TIER_MATRIX.get(phase_id, Tier.BALANCED)
    if fallback_tier is None:
        fallback_tier = Tier.BALANCED
    alias = TIER_ALIAS_MAP.get(fallback_tier)
    return ResolveResult.success_alias(fallback_tier, alias)


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
        model_resolve: Resolution strategy ("alias_only" | "local_catalog" | "role_catalog")
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
            tier = Tier.BALANCED

    catalog = None
    if catalog_path and model_resolve in ("local_catalog", "role_catalog"):
        catalog, error = load_catalog(catalog_path)
        if error:
            code = catalog_validation_reason_code(error, None)
            return ResolveResult.failure(code, error)

    return _resolve_tier_chain(phase, tier, model_resolve, model_fallback, catalog)


def get_tier_for_phase(phase: str) -> Optional[Tier]:
    """Get default tier for a phase (None for 'auto')."""
    return DEFAULT_PHASE_TIER_MATRIX.get(phase)


def get_alias_for_tier(tier: Tier) -> Optional[str]:
    """Get Cursor alias for a tier (None means omit model: field)."""
    return TIER_ALIAS_MAP.get(tier)


def self_test() -> bool:
    """Run self-test to validate library contract (US-0101 / DEC-0086; US-0102 / DEC-0087)."""
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
    expected_codes = {
        "MODEL_TIER_INVALID", "MODEL_CATALOG_INVALID", "MODEL_SLUG_UNKNOWN",
        "MODEL_RESOLVE_FALLBACK", "MODEL_OVERRIDE_SLUG_UNKNOWN",
        "MODEL_ROLE_SLUG_UNKNOWN", "MODEL_CATALOG_SCHEMA_V2_INVALID",
    }
    actual_codes = {c.value for c in ReasonCode}
    if actual_codes != expected_codes:
        errors.append(f"ReasonCode mismatch: expected {expected_codes}, got {actual_codes}")

    # Test 5: Precedence chain
    if len(PRECEDENCE_CHAIN_STEPS) != 5:
        errors.append(f"Precedence chain must have 5 steps, got {len(PRECEDENCE_CHAIN_STEPS)}")

    # Test 6: resolve_model_for_phase exported
    if not callable(resolve_model_for_phase):
        errors.append("resolve_model_for_phase is not callable")

    if errors:
        print("[SELF_TEST_FAILED]")
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return False
    else:
        print("[MODEL_TIER_SELF_TEST_OK]")
        return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Model tier resolver (US-0101 / US-0102)")
    parser.add_argument("--phase", help="Phase ID (e.g., execute, qa)")
    parser.add_argument(
        "--resolve",
        default="alias_only",
        choices=["alias_only", "local_catalog", "role_catalog"],
    )
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
        print(f"[OK] phase={args.phase} tier={result.tier.value if result.tier else 'n/a'}", end="")
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
