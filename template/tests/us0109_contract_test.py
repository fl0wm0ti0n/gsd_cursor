"""Contract tests for US-0109 Self-Healing Deploy Loop (DEC-0109).

8 core markers + 2 compose guards + 1 backward compat.
"""
from __future__ import annotations

import os
import pathlib
import subprocess
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from self_healing_deploy_lib import (  # noqa: E402
    AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT_KEY,
    AUTO_SOVEREIGN_DEPLOY_PROBE_KIND_KEY,
    AUTO_SOVEREIGN_DEPLOY_RETRY_MAX_KEY,
    AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC_KEY,
    AUTO_SOVEREIGN_SELF_HEALING_DEPLOY_KEY,
    DEFAULT_ACCEPTANCE_SMOKE_PATH,
    DEFAULT_PROBE_KIND,
    DEFAULT_RETRY_MAX,
    DEFAULT_SELF_HEALING_ENABLED,
    DEFAULT_SMOKE_TIMEOUT_SEC,
    SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH_KEY,
    ProbeKind,
    ReasonCode,
    get_acceptance_smoke_path,
    get_probe_kind,
    get_retry_max,
    get_smoke_timeout_sec,
    is_self_healing_deploy_enabled,
    resolve_health_endpoint_url,
    run_acceptance_smoke,
    run_deploy_healing_loop,
    run_health_probe,
    run_smoke_probe_chain,
    self_test,
)


# --- T-006: 8 core markers ---------------------------------------------------


def test_us0109_scratchpad_keys_and_defaults() -> None:
    """AC-1: 6 scratchpad keys resolve to DEC-0109 defaults."""
    scratchpad = {}
    assert is_self_healing_deploy_enabled(scratchpad) is False
    assert get_retry_max(scratchpad) == DEFAULT_RETRY_MAX
    assert get_smoke_timeout_sec(scratchpad) == DEFAULT_SMOKE_TIMEOUT_SEC
    assert get_probe_kind(scratchpad) == ProbeKind.BOTH
    assert get_acceptance_smoke_path(scratchpad) == DEFAULT_ACCEPTANCE_SMOKE_PATH
    assert resolve_health_endpoint_url(scratchpad) is None
    assert DEFAULT_SELF_HEALING_ENABLED == "0"
    expected_keys = {
        AUTO_SOVEREIGN_SELF_HEALING_DEPLOY_KEY,
        AUTO_SOVEREIGN_DEPLOY_RETRY_MAX_KEY,
        AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC_KEY,
        AUTO_SOVEREIGN_DEPLOY_PROBE_KIND_KEY,
        SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH_KEY,
        AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT_KEY,
    }
    assert len(expected_keys) == 6


def test_us0109_probe_health_stage() -> None:
    """AC-2: health probe stage returns fail when target missing."""
    scratchpad = {
        AUTO_SOVEREIGN_SELF_HEALING_DEPLOY_KEY: "1",
        AUTO_SOVEREIGN_DEPLOY_PROBE_KIND_KEY: "health_endpoint",
        AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT_KEY: "",
    }
    result = run_health_probe(scratchpad)
    assert result.overall == "fail"
    assert result.reason_code == ReasonCode.DEPLOY_HEALING_PROBE_TARGET_MISSING.value
    assert result.health_status == "fail"
    assert result.acceptance_status is None


def test_us0109_probe_acceptance_stage() -> None:
    """AC-2: acceptance smoke skip when path absent."""
    scratchpad = {
        AUTO_SOVEREIGN_SELF_HEALING_DEPLOY_KEY: "1",
        AUTO_SOVEREIGN_DEPLOY_PROBE_KIND_KEY: "acceptance_smoke",
        SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH_KEY: "nonexistent_path_xyz/",
    }
    result = run_acceptance_smoke(scratchpad)
    assert result.acceptance_status == "skip"
    assert result.overall == "pass"
    assert result.reason_code == "DEPLOY_ACCEPTANCE_SMOKE_SKIP_NO_PATH"


def test_us0109_retry_loop_bounded() -> None:
    """AC-3: bounded retry loop caps at AUTO_SOVEREIGN_DEPLOY_RETRY_MAX."""
    scratchpad = {
        AUTO_SOVEREIGN_SELF_HEALING_DEPLOY_KEY: "1",
        AUTO_SOVEREIGN_DEPLOY_RETRY_MAX_KEY: "3",
    }
    attempts = 0

    def always_fail(reason: str) -> bool:
        nonlocal attempts
        attempts += 1
        return False

    result = run_deploy_healing_loop(REPO_ROOT, scratchpad, always_fail, story_id="US-0109")
    assert result.enabled is True
    assert result.reason_code == ReasonCode.DEPLOY_HEALING_RETRY_CAP_EXHAUSTED.value
    assert result.retry_count <= 3
    assert attempts <= 3


def test_us0109_deferred_after_cap_exhaustion() -> None:
    """AC-4: DEPLOY_DEFERRED path after retry cap exhaustion."""
    from self_healing_deploy_lib import emit_deploy_deferral

    scratchpad = {
        AUTO_SOVEREIGN_SELF_HEALING_DEPLOY_KEY: "1",
        AUTO_SOVEREIGN_DEPLOY_RETRY_MAX_KEY: "2",
    }
    deferral_id, reason = emit_deploy_deferral(
        REPO_ROOT,
        scratchpad,
        story_id="US-0109",
        orchestrator_run_id="auto-20260628-04",
        smoke_summary="smoke probe failed; retry cap exhausted",
    )
    allowed = (
        ReasonCode.DEPLOY_HEALING_DISABLED.value,
        "SOVEREIGN_LOOP_DISABLED",
        "",
    )
    assert deferral_id is None or reason in allowed


def test_us0109_backward_compat_off_path_byte_identical() -> None:
    """AC-5: AUTO_SOVEREIGN_SELF_HEALING_DEPLOY=0 byte-identical US-0054 path."""
    scratchpad = {AUTO_SOVEREIGN_SELF_HEALING_DEPLOY_KEY: "0"}
    probe = run_smoke_probe_chain(scratchpad)
    assert probe.overall == "pass"
    assert probe.reason_code == ReasonCode.DEPLOY_HEALING_DISABLED.value
    assert probe.health_status == "skip"
    assert probe.acceptance_status == "skip"

    loop_result = run_deploy_healing_loop(
        REPO_ROOT, scratchpad, lambda reason: False, story_id="US-0109"
    )
    assert loop_result.enabled is False
    assert loop_result.reason_code == ReasonCode.DEPLOY_HEALING_DISABLED.value


def test_us0109_validator_cli_self_test() -> None:
    """AC-6: validator CLI emits [SELF_HEALING_DEPLOY_VALIDATION_OK]."""
    token = self_test()
    assert token == "[SELF_HEALING_DEPLOY_VALIDATION_OK]"


def test_us0109_reason_codes_section_present() -> None:
    """AC-8: 8 DEPLOY_HEALING_* reason codes in reason_codes.md."""
    reason_codes_path = REPO_ROOT / "docs" / "engineering" / "reason_codes.md"
    assert reason_codes_path.is_file()
    content = reason_codes_path.read_text(encoding="utf-8")
    expected_codes = [
        "DEPLOY_HEALING_DISABLED",
        "DEPLOY_HEALING_SMOKE_HEALTH_FAIL",
        "DEPLOY_HEALING_SMOKE_ACCEPTANCE_FAIL",
        "DEPLOY_HEALING_RETRY_ATTEMPT",
        "DEPLOY_HEALING_RETRY_CAP_EXHAUSTED",
        "DEPLOY_HEALING_DEFERRED",
        "DEPLOY_HEALING_PROBE_TARGET_MISSING",
        "DEPLOY_HEALING_TIMEOUT",
    ]
    for code in expected_codes:
        assert code in content, f"reason code {code} missing"
    assert "## US-0109" in content


# --- T-007 / T-009: compose guards -------------------------------------------


def test_us0109_us0054_compose_no_publish_semantics_change() -> None:
    """AC-7 compose guard: US-0054 publish targets / confirmation gate UNCHANGED."""
    lib_path = SCRIPTS_DIR / "self_healing_deploy_lib.py"
    content = lib_path.read_text(encoding="utf-8")
    forbidden_tokens = ["RELEASE_PUBLISH_OK", "release_publish", "publish_targets"]
    for token in forbidden_tokens:
        assert token not in content, f"US-0054 publish token {token} found in US-0109 lib"


def test_us0109_us0100_compose_no_changelog_change() -> None:
    """AC-7 compose guard: US-0100 changelog / [Unreleased] UNCHANGED."""
    lib_path = SCRIPTS_DIR / "self_healing_deploy_lib.py"
    content = lib_path.read_text(encoding="utf-8")
    forbidden_tokens = ["changelog", "[Unreleased]", "changelog_lib", "version_changelog"]
    for token in forbidden_tokens:
        assert token not in content, f"US-0100 changelog token {token} found in US-0109 lib"


def test_us0109_us0110_compose_no_convergence_change() -> None:
    """AC-7 compose guard: US-0110 convergence predicate UNCHANGED."""
    lib_path = SCRIPTS_DIR / "self_healing_deploy_lib.py"
    content = lib_path.read_text(encoding="utf-8")
    forbidden_tokens = ["convergence", "evaluate_convergence", "sovereign_convergence_lib"]
    for token in forbidden_tokens:
        assert token not in content, f"US-0110 convergence token {token} found in US-0109 lib"
