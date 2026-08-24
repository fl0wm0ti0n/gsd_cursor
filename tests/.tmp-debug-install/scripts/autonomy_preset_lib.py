#!/usr/bin/env python3
"""
Autonomy preset expansion library (US-0119).

Expands AUTONOMY_PRESET into per-feature autonomy flags with deterministic,
pure-stdlib logic. No LLM, no network, no .env reads.
"""
import sys
import json
from typing import Dict, Optional


# 12 per-feature autonomy flags (DEC-0119 §7)
AUTONOMY_FLAGS = {
    "INTAKE_AUTONOMY_MODE",
    "INTAKE_MINIMAL_PACK",
    "INTAKE_ASSUME_STACK_CONTEXT",
    "WORK_KIND_AUTO_ACCEPT",
    "CROSS_MODEL_REWORK_EXHAUSTED_POLICY",
    "CROSS_MODEL_SKIP_PHASES",
    "RESUME_BRIEF_AUTO_REFRESH",
    "RUNTIME_PROOF_KIND",
    "GOAL_CONVERGENCE_INTERVAL",
    "SOVEREIGN_DRAIN_AUTO_ACCEPT",
    "RELEASE_PUBLISH_AUTO_CONFIRM",
    "AUTONOMY_STOP_POLICY",
}


# Preset definitions (DEC-0119 §7)
# none: empty expansion (byte-identical pre-US-0119)
# balanced: 8 flags (moderate autonomy)
# full: all 12 flags (maximum autonomy)
PRESET_DEFINITIONS = {
    "none": {},
    "balanced": {
        "WORK_KIND_AUTO_ACCEPT": "1",
        "CROSS_MODEL_REWORK_EXHAUSTED_POLICY": "downgrade",
        "CROSS_MODEL_SKIP_PHASES": "",
        "RESUME_BRIEF_AUTO_REFRESH": "1",
        "RUNTIME_PROOF_KIND": "lightweight",
        "GOAL_CONVERGENCE_INTERVAL": "3",
        "SOVEREIGN_DRAIN_AUTO_ACCEPT": "1",
        "AUTONOMY_STOP_POLICY": "auto_repair_then_block",
    },
    "full": {
        "INTAKE_AUTONOMY_MODE": "1",
        "INTAKE_MINIMAL_PACK": "1",
        "INTAKE_ASSUME_STACK_CONTEXT": "1",
        "WORK_KIND_AUTO_ACCEPT": "1",
        "CROSS_MODEL_REWORK_EXHAUSTED_POLICY": "downgrade",
        "CROSS_MODEL_SKIP_PHASES": "",
        "RESUME_BRIEF_AUTO_REFRESH": "1",
        "RUNTIME_PROOF_KIND": "lightweight",
        "GOAL_CONVERGENCE_INTERVAL": "1",
        "SOVEREIGN_DRAIN_AUTO_ACCEPT": "1",
        "RELEASE_PUBLISH_AUTO_CONFIRM": "1",
        "AUTONOMY_STOP_POLICY": "auto_repair_then_skip",
    },
}


def expand_autonomy_preset(
    preset: str,
    overrides: Optional[Dict[str, str]] = None
) -> Dict[str, str]:
    """
    Expand AUTONOMY_PRESET into per-feature flags.

    Args:
        preset: One of {none, balanced, full}
        overrides: Explicit per-flag values that override preset defaults

    Returns:
        Dict of flag_name -> flag_value

    Raises:
        ValueError: If preset is invalid or overrides contain unknown keys

    Precedence (LOCKED): explicit per-flag > preset expansion > scratchpad defaults
    """
    if preset not in PRESET_DEFINITIONS:
        raise ValueError(
            f"Invalid AUTONOMY_PRESET='{preset}'. "
            f"Must be one of: {', '.join(PRESET_DEFINITIONS.keys())}"
        )

    # Start with preset base
    result = PRESET_DEFINITIONS[preset].copy()

    # Apply overrides (explicit per-flag values always win)
    if overrides:
        unknown_keys = set(overrides.keys()) - AUTONOMY_FLAGS
        if unknown_keys:
            raise ValueError(
                f"Unknown autonomy flag(s) in overrides: {', '.join(sorted(unknown_keys))}"
            )
        result.update(overrides)

    return result


def explain_preset(preset: str) -> Dict[str, Dict[str, str]]:
    """
    Explain preset expansion with source annotations.

    Returns:
        Dict of flag_name -> {value, source} where source is 'preset' or 'default'
    """
    expansion = PRESET_DEFINITIONS[preset]
    result = {}

    for flag in sorted(AUTONOMY_FLAGS):
        if flag in expansion:
            result[flag] = {
                "value": expansion[flag],
                "source": "preset"
            }
        else:
            result[flag] = {
                "value": "",
                "source": "default"
            }

    return result


def self_test() -> bool:
    """
    Self-test mode: verify known-key set, precedence, and preset expansions.

    Returns:
        True if all tests pass, False otherwise
    """
    tests_passed = 0
    tests_total = 0

    # Test 1: none preset is empty
    tests_total += 1
    result = expand_autonomy_preset("none")
    if result == {}:
        tests_passed += 1
        print("[PASS] Test 1: none preset is empty")
    else:
        print(f"[FAIL] Test 1: expected {{}}, got {result}")

    # Test 2: balanced preset has 8 flags
    tests_total += 1
    result = expand_autonomy_preset("balanced")
    if len(result) == 8 and all(k in AUTONOMY_FLAGS for k in result.keys()):
        tests_passed += 1
        print("[PASS] Test 2: balanced preset has 8 flags, all known keys")
    else:
        print(f"[FAIL] Test 2: expected 8 flags, got {len(result)}")

    # Test 3: full preset has 12 flags
    tests_total += 1
    result = expand_autonomy_preset("full")
    if len(result) == 12 and all(k in AUTONOMY_FLAGS for k in result.keys()):
        tests_passed += 1
        print("[PASS] Test 3: full preset has 12 flags, all known keys")
    else:
        print(f"[FAIL] Test 3: expected 12 flags, got {len(result)}")

    # Test 4: explicit override wins
    tests_total += 1
    result = expand_autonomy_preset("balanced", {"WORK_KIND_AUTO_ACCEPT": "0"})
    if result.get("WORK_KIND_AUTO_ACCEPT") == "0":
        tests_passed += 1
        print("[PASS] Test 4: explicit override wins over preset")
    else:
        print(f"[FAIL] Test 4: expected '0', got '{result.get('WORK_KIND_AUTO_ACCEPT')}'")

    # Test 5: unknown key in overrides raises ValueError
    tests_total += 1
    try:
        expand_autonomy_preset("balanced", {"UNKNOWN_FLAG": "1"})
        print("[FAIL] Test 5: should have raised ValueError for unknown key")
    except ValueError:
        tests_passed += 1
        print("[PASS] Test 5: unknown key in overrides raises ValueError")

    # Test 6: invalid preset raises ValueError
    tests_total += 1
    try:
        expand_autonomy_preset("invalid")
        print("[FAIL] Test 6: should have raised ValueError for invalid preset")
    except ValueError:
        tests_passed += 1
        print("[PASS] Test 6: invalid preset raises ValueError")

    print(f"\nSelf-test: {tests_passed}/{tests_total} tests passed")
    return tests_passed == tests_total


if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1]

        if mode == "--self-test":
            success = self_test()
            sys.exit(0 if success else 1)

        elif mode == "--explain":
            if len(sys.argv) < 3:
                print("Usage: autonomy_preset_lib.py --explain <preset>")
                sys.exit(1)

            preset = sys.argv[2]
            try:
                explanation = explain_preset(preset)
                print(json.dumps(explanation, indent=2))
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)

        else:
            print(f"Unknown mode: {mode}", file=sys.stderr)
            print("Usage: autonomy_preset_lib.py [--self-test | --explain <preset>]", file=sys.stderr)
            sys.exit(1)

    else:
        print("Autonomy Preset Library (US-0119)")
        print("Usage: python autonomy_preset_lib.py [--self-test | --explain <preset>]")
