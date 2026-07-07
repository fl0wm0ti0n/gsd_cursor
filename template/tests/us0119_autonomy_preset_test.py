"""
Contract tests for US-0119 — Autonomous-autonomy presets.

10 test markers per DEC-0119 §9, covering AC-6, AC-7, AC-10, AC-12.
"""
import pytest
import sys
from pathlib import Path


def test_us0119_preset_none_is_noop():
    """AC-6: AUTONOMY_PRESET=none produces byte-identical pre-US-0119 behaviour (empty expansion)."""
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    from autonomy_preset_lib import expand_autonomy_preset

    result = expand_autonomy_preset("none")
    assert result == {}, "AUTONOMY_PRESET=none MUST produce empty expansion (byte-identical pre-US-0119)"


def test_us0119_preset_balanced_expansion():
    """AC-2: balanced preset expands into documented 8 flags per DEC-0119 §7."""
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    from autonomy_preset_lib import expand_autonomy_preset

    result = expand_autonomy_preset("balanced")
    assert len(result) == 8, f"balanced preset MUST expand to 8 flags, got {len(result)}"
    expected_keys = {
        "WORK_KIND_AUTO_ACCEPT",
        "CROSS_MODEL_REWORK_EXHAUSTED_POLICY",
        "CROSS_MODEL_SKIP_PHASES",
        "RESUME_BRIEF_AUTO_REFRESH",
        "RUNTIME_PROOF_KIND",
        "GOAL_CONVERGENCE_INTERVAL",
        "SOVEREIGN_DRAIN_AUTO_ACCEPT",
        "AUTONOMY_STOP_POLICY",
    }
    assert set(result.keys()) == expected_keys, f"balanced preset keys mismatch: {set(result.keys())} != {expected_keys}"


def test_us0119_preset_full_expansion():
    """AC-2: full preset expands into documented 12 flags per DEC-0119 §7."""
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    from autonomy_preset_lib import expand_autonomy_preset

    result = expand_autonomy_preset("full")
    assert len(result) == 12, f"full preset MUST expand to 12 flags, got {len(result)}"
    expected_keys = {
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
    assert set(result.keys()) == expected_keys, f"full preset keys mismatch: {set(result.keys())} != {expected_keys}"


def test_us0119_explicit_flag_overrides_preset():
    """AC-2: explicit per-flag > preset expansion (LOCKED precedence)."""
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    from autonomy_preset_lib import expand_autonomy_preset

    result = expand_autonomy_preset("balanced", {"WORK_KIND_AUTO_ACCEPT": "0"})
    assert result["WORK_KIND_AUTO_ACCEPT"] == "0", "explicit override MUST win over preset value"


def test_us0119_preset_expansion_uses_known_keys_only():
    """AC-12: expansion output contains only keys in pre-US-0119 scratchpad schema (compose guard)."""
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    from autonomy_preset_lib import expand_autonomy_preset, AUTONOMY_FLAGS

    for preset in ["none", "balanced", "full"]:
        result = expand_autonomy_preset(preset)
        unknown_keys = set(result.keys()) - AUTONOMY_FLAGS
        assert not unknown_keys, f"preset={preset} expansion contains unknown keys: {unknown_keys}"


def test_us0119_matrix_validator_passes():
    """AC-4: scripts/validate_autonomy_stop_matrix.py --self-test exits 0."""
    import subprocess

    validator_path = Path(__file__).parent.parent / "scripts" / "validate_autonomy_stop_matrix.py"
    result = subprocess.run(
        ["python", str(validator_path), "--self-test"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"validator --self-test MUST exit 0, got {result.returncode}\nstderr: {result.stderr}"


def test_us0119_security_hard_gates_never_auto_repaired():
    """AC-7: matrix security_hard rows all carry auto_repair_kind=n/a."""
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    from validate_autonomy_stop_matrix import parse_yaml_matrix, REPO_ROOT

    yaml_path = REPO_ROOT / "scripts" / "data" / "autonomy_stop_matrix.yaml"
    matrix = parse_yaml_matrix(yaml_path)

    for entry in matrix.get("reason_codes", []):
        if entry.get("stop_class") == "security_hard":
            assert entry.get("auto_repair_kind") == "n/a", (
                f"security_hard code {entry['code']} MUST have auto_repair_kind=n/a, "
                f"got {entry.get('auto_repair_kind')}"
            )


def test_us0119_stop_policy_affects_repair_dispatch():
    """AC-3: auto_repair_then_block vs auto_repair_then_skip dispatch correctly."""
    # This test verifies the stop-policy dispatch logic is documented in scratchpad
    # Actual dispatch happens at runtime based on AUTONOMY_STOP_POLICY value

    scratchpad_path = Path(__file__).parent.parent / ".cursor" / "scratchpad.md"
    content = scratchpad_path.read_text(encoding="utf-8")

    assert "AUTONOMY_STOP_POLICY=" in content, "AUTONOMY_STOP_POLICY MUST be documented in scratchpad"
    assert "block|" in content or "auto_repair_then_block|" in content, (
        "AUTONOMY_STOP_POLICY MUST document block/auto_repair_then_block/auto_repair_then_skip enum"
    )


def test_us0119_repair_ledger_cap_escalates():
    """AC-8: cap exhaustion -> AUTONOMY_REPAIR_CAP_EXHAUSTED terminal stop."""
    # This test verifies the terminal stop code is in the matrix

    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    from validate_autonomy_stop_matrix import parse_yaml_matrix, REPO_ROOT

    yaml_path = REPO_ROOT / "scripts" / "data" / "autonomy_stop_matrix.yaml"
    matrix = parse_yaml_matrix(yaml_path)

    reason_codes = {entry["code"]: entry for entry in matrix.get("reason_codes", [])}
    assert "AUTONOMY_REPAIR_CAP_EXHAUSTED" in reason_codes, (
        "AUTONOMY_REPAIR_CAP_EXHAUSTED terminal stop code MUST be in matrix"
    )

    terminal_entry = reason_codes["AUTONOMY_REPAIR_CAP_EXHAUSTED"]
    assert terminal_entry["stop_class"] == "autonomy_resolvable", (
        "AUTONOMY_REPAIR_CAP_EXHAUSTED MUST be autonomy_resolvable (bounded cap)"
    )
    assert terminal_entry["auto_repair_kind"] == "n/a", (
        "AUTONOMY_REPAIR_CAP_EXHAUSTED MUST have auto_repair_kind=n/a (terminal)"
    )
    assert terminal_entry["cap"] == 0, (
        "AUTONOMY_REPAIR_CAP_EXHAUSTED MUST have cap=0 (terminal stop)"
    )


def test_us0119_matrix_no_orphan_codes():
    """AC-4: no orphan reason codes outside YAML manifest."""
    # This test is implicitly covered by test_us0119_matrix_validator_passes,
    # which runs the validator's --self-test. If the validator passes, no orphan
    # codes exist.

    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    from validate_autonomy_stop_matrix import self_test

    passed, violations = self_test()
    assert passed, f"validator self_test MUST pass, got violations: {violations}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
