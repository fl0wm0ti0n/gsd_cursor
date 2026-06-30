#!/usr/bin/env python3
"""
Self-Healing Deploy Loop helper library (US-0109 / DEC-0109).

Post-deploy smoke probe + bounded retry loop on US-0054 publish chain.
After the post-publish PASS point, two-stage probe validates deployed artifact.
On probe FAIL, re-enter publish PASS path (not execute re-entry) up to
`AUTO_SOVEREIGN_DEPLOY_RETRY_MAX`. After retry-cap exhaustion, emit
DEPLOY_DEFERRED tuple via US-0107 `append_deferral(work_item_kind=deploy)`.

Default-off: `AUTO_SOVEREIGN_SELF_HEALING_DEPLOY=0` → zero overhead, byte-identical
US-0054 publish path — no probe, no retry, no deferral, no execute steps 29-31.

Reason codes (DEC-0109 §7):
  DEPLOY_HEALING_DISABLED (info), DEPLOY_HEALING_SMOKE_HEALTH_FAIL,
  DEPLOY_HEALING_SMOKE_ACCEPTANCE_FAIL, DEPLOY_HEALING_RETRY_ATTEMPT,
  DEPLOY_HEALING_RETRY_CAP_EXHAUSTED, DEPLOY_HEALING_DEFERRED,
  DEPLOY_HEALING_PROBE_TARGET_MISSING, DEPLOY_HEALING_TIMEOUT.

Compose guards (non-negotiable): DO NOT amend US-0054, US-0100, US-0103, US-0107, US-0110.
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

try:
    from sovereign_loop_lib import append_deferral, is_sovereign_loop_enabled  # type: ignore
except ImportError:
    append_deferral = None  # type: ignore
    is_sovereign_loop_enabled = None  # type: ignore


SCHEMA_VERSION = 1


class ProbeKind(Enum):
    HEALTH_ENDPOINT = "health_endpoint"
    ACCEPTANCE_SMOKE = "acceptance_smoke"
    BOTH = "both"


class ReasonCode(Enum):
    DEPLOY_HEALING_DISABLED = "DEPLOY_HEALING_DISABLED"
    DEPLOY_HEALING_SMOKE_HEALTH_FAIL = "DEPLOY_HEALING_SMOKE_HEALTH_FAIL"
    DEPLOY_HEALING_SMOKE_ACCEPTANCE_FAIL = "DEPLOY_HEALING_SMOKE_ACCEPTANCE_FAIL"
    DEPLOY_HEALING_RETRY_ATTEMPT = "DEPLOY_HEALING_RETRY_ATTEMPT"
    DEPLOY_HEALING_RETRY_CAP_EXHAUSTED = "DEPLOY_HEALING_RETRY_CAP_EXHAUSTED"
    DEPLOY_HEALING_DEFERRED = "DEPLOY_HEALING_DEFERRED"
    DEPLOY_HEALING_PROBE_TARGET_MISSING = "DEPLOY_HEALING_PROBE_TARGET_MISSING"
    DEPLOY_HEALING_TIMEOUT = "DEPLOY_HEALING_TIMEOUT"


# Scratchpad keys (DEC-0109 §1)
AUTO_SOVEREIGN_SELF_HEALING_DEPLOY_KEY = "AUTO_SOVEREIGN_SELF_HEALING_DEPLOY"
AUTO_SOVEREIGN_DEPLOY_RETRY_MAX_KEY = "AUTO_SOVEREIGN_DEPLOY_RETRY_MAX"
AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC_KEY = "AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC"
AUTO_SOVEREIGN_DEPLOY_PROBE_KIND_KEY = "AUTO_SOVEREIGN_DEPLOY_PROBE_KIND"
SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH_KEY = "SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH"
AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT_KEY = "AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT"

# Defaults (DEC-0109 §1)
DEFAULT_RETRY_MAX = 3
DEFAULT_SMOKE_TIMEOUT_SEC = 30
DEFAULT_PROBE_KIND = "both"
DEFAULT_ACCEPTANCE_SMOKE_PATH = "tests/deploy_smoke/"
DEFAULT_SELF_HEALING_ENABLED = "0"


@dataclass
class ProbeResult:
    probe_kind: str
    health_status: Optional[str] = None
    health_status_code: Optional[str] = None
    acceptance_status: Optional[str] = None
    acceptance_tests_run: Optional[int] = None
    acceptance_tests_failed: Optional[int] = None
    overall: str = "fail"
    reason_code: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HealingLoopResult:
    enabled: bool
    probe_result: Optional[Dict[str, Any]] = None
    retry_count: int = 0
    retry_max: int = DEFAULT_RETRY_MAX
    deferred: bool = False
    deferral_id: Optional[str] = None
    reason_code: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def is_self_healing_deploy_enabled(scratchpad: Dict[str, str]) -> bool:
    """Return True when AUTO_SOVEREIGN_SELF_HEALING_DEPLOY=1 (default 0 = disabled)."""
    value = scratchpad.get(AUTO_SOVEREIGN_SELF_HEALING_DEPLOY_KEY, DEFAULT_SELF_HEALING_ENABLED)
    return value.strip() == "1"


def get_retry_max(scratchpad: Dict[str, str]) -> int:
    """Return AUTO_SOVEREIGN_DEPLOY_RETRY_MAX (default 3; int >= 1)."""
    raw = scratchpad.get(AUTO_SOVEREIGN_DEPLOY_RETRY_MAX_KEY, str(DEFAULT_RETRY_MAX))
    try:
        parsed = int(raw.strip())
        return max(1, parsed)
    except (ValueError, AttributeError):
        return DEFAULT_RETRY_MAX


def get_smoke_timeout_sec(scratchpad: Dict[str, str]) -> int:
    """Return AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC (default 30; int >= 1)."""
    raw = scratchpad.get(AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC_KEY, str(DEFAULT_SMOKE_TIMEOUT_SEC))
    try:
        parsed = int(raw.strip())
        return max(1, parsed)
    except (ValueError, AttributeError):
        return DEFAULT_SMOKE_TIMEOUT_SEC


def get_probe_kind(scratchpad: Dict[str, str]) -> ProbeKind:
    """Return AUTO_SOVEREIGN_DEPLOY_PROBE_KIND (default both)."""
    raw = scratchpad.get(AUTO_SOVEREIGN_DEPLOY_PROBE_KIND_KEY, DEFAULT_PROBE_KIND)
    try:
        return ProbeKind(raw.strip().lower())
    except (ValueError, AttributeError):
        return ProbeKind.BOTH


def get_acceptance_smoke_path(scratchpad: Dict[str, str]) -> str:
    """Return SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH (default tests/deploy_smoke/)."""
    return scratchpad.get(SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH_KEY, DEFAULT_ACCEPTANCE_SMOKE_PATH)


def resolve_health_endpoint_url(scratchpad: Dict[str, str]) -> Optional[str]:
    """Return health endpoint URL from names-only env ref (US-0085 compose).

    `AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT` is a KEY NAME in `os.environ` — NOT a URL literal.
    Fail-closed `DEPLOY_HEALING_PROBE_TARGET_MISSING` when absent or unresolvable.
    No secret values leaked from `.env` (US-0085 / US-0093 compose).
    """
    env_key_name = scratchpad.get(AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT_KEY, "").strip()
    if not env_key_name:
        return None
    url = os.environ.get(env_key_name, "").strip()
    if not url:
        return None
    return url


def _scan_for_secret_candidate(url: str) -> bool:
    """Best-effort secret scan — reject URLs carrying inline credentials (US-0085)."""
    forbidden_patterns = ["password=", "token=", "key=", "secret=", "Bearer ", "Basic "]
    lower = url.lower()
    return any(p in lower for p in forbidden_patterns)


def run_health_probe(scratchpad: Dict[str, str]) -> ProbeResult:
    """Stage (a): health HTTP GET to names-only env ref resolved URL.

    Success: HTTP 2xx. Fail: timeout / non-2xx / unresolvable target.
    """
    timeout_sec = get_smoke_timeout_sec(scratchpad)
    url = resolve_health_endpoint_url(scratchpad)
    result = ProbeResult(probe_kind="health_endpoint")

    if url is None:
        result.health_status = "fail"
        result.reason_code = ReasonCode.DEPLOY_HEALING_PROBE_TARGET_MISSING.value
        result.overall = "fail"
        return result

    if _scan_for_secret_candidate(url):
        result.health_status = "fail"
        result.reason_code = f"{ReasonCode.DEPLOY_HEALING_PROBE_TARGET_MISSING.value}_SECRET_SCAN"
        result.overall = "fail"
        return result

    try:
        import urllib.request
        import urllib.error
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            status = resp.status
            result.health_status_code = str(status)
            if 200 <= status < 300:
                result.health_status = "pass"
                result.overall = "pass"
                result.reason_code = "DEPLOY_SMOKE_PROBE_OK"
            else:
                result.health_status = "fail"
                result.overall = "fail"
                result.reason_code = ReasonCode.DEPLOY_HEALING_SMOKE_HEALTH_FAIL.value
    except socket.timeout:
        result.health_status = "fail"
        result.health_status_code = "timeout"
        result.overall = "fail"
        result.reason_code = ReasonCode.DEPLOY_HEALING_TIMEOUT.value
    except urllib.error.URLError as exc:
        result.health_status = "fail"
        result.health_status_code = "url_error"
        result.overall = "fail"
        result.reason_code = ReasonCode.DEPLOY_HEALING_SMOKE_HEALTH_FAIL.value
    except Exception:
        result.health_status = "fail"
        result.health_status_code = "unknown"
        result.overall = "fail"
        result.reason_code = ReasonCode.DEPLOY_HEALING_SMOKE_HEALTH_FAIL.value

    return result


def run_acceptance_smoke(scratchpad: Dict[str, str], repo: Optional[Path] = None) -> ProbeResult:
    """Stage (b): bounded pytest runner on acceptance smoke path.

    Path: SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH (default tests/deploy_smoke/).
    Runner: `pytest -x --timeout=30 -q <path>`. Success: exit 0.
    """
    timeout_sec = get_smoke_timeout_sec(scratchpad)
    smoke_path = get_acceptance_smoke_path(scratchpad)
    result = ProbeResult(probe_kind="acceptance_smoke")

    target = Path(repo / smoke_path) if repo else Path(smoke_path)
    if not target.exists():
        result.acceptance_status = "skip"
        result.acceptance_tests_run = 0
        result.acceptance_tests_failed = 0
        result.overall = "pass"
        result.reason_code = "DEPLOY_ACCEPTANCE_SMOKE_SKIP_NO_PATH"
        return result

    cmd = [
        sys.executable, "-m", "pytest",
        "-x",
        f"--timeout={timeout_sec}",
        "-q",
        str(target),
    ]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_sec + 10,
            cwd=str(repo) if repo else None,
        )
    except subprocess.TimeoutExpired:
        result.acceptance_status = "fail"
        result.overall = "fail"
        result.reason_code = ReasonCode.DEPLOY_HEALING_TIMEOUT.value
        return result
    except Exception:
        result.acceptance_status = "fail"
        result.overall = "fail"
        result.reason_code = ReasonCode.DEPLOY_HEALING_SMOKE_ACCEPTANCE_FAIL.value
        return result

    failed_count = 0
    passed_count = 0
    for line in (proc.stdout or "").splitlines():
        if " passed" in line:
            try:
                passed_count = int(line.split(" passed")[0].split()[-1])
            except (ValueError, IndexError):
                passed_count = 0
        if " failed" in line:
            try:
                failed_count = int(line.split(" failed")[0].split()[-1])
            except (ValueError, IndexError):
                failed_count = 0

    result.acceptance_tests_run = passed_count + failed_count
    result.acceptance_tests_failed = failed_count

    if proc.returncode == 0:
        result.acceptance_status = "pass"
        result.overall = "pass"
        result.reason_code = "DEPLOY_SMOKE_PROBE_OK"
    else:
        result.acceptance_status = "fail"
        result.overall = "fail"
        result.reason_code = ReasonCode.DEPLOY_HEALING_SMOKE_ACCEPTANCE_FAIL.value

    return result


def run_smoke_probe_chain(scratchpad: Dict[str, str]) -> ProbeResult:
    """Two-stage probe chain executed sequentially at post-publish stage.

    When PROBE_KIND != BOTH, only the named stage runs.
    Both stages MUST pass to emit `[DEPLOY_SMOKE_PROBE_OK]`.
    """
    if not is_self_healing_deploy_enabled(scratchpad):
        result = ProbeResult(probe_kind="disabled")
        result.overall = "pass"
        result.reason_code = ReasonCode.DEPLOY_HEALING_DISABLED.value
        result.health_status = "skip"
        result.acceptance_status = "skip"
        return result

    probe_kind = get_probe_kind(scratchpad)
    result = ProbeResult(probe_kind=probe_kind.value)

    if probe_kind in (ProbeKind.HEALTH_ENDPOINT, ProbeKind.BOTH):
        health = run_health_probe(scratchpad)
        result.health_status = health.health_status
        result.health_status_code = health.health_status_code
        if health.overall != "pass":
            result.overall = "fail"
            result.reason_code = health.reason_code
            result.acceptance_status = "skip"
            return result

    if probe_kind in (ProbeKind.ACCEPTANCE_SMOKE, ProbeKind.BOTH):
        acceptance = run_acceptance_smoke(scratchpad)
        result.acceptance_status = acceptance.acceptance_status
        result.acceptance_tests_run = acceptance.acceptance_tests_run
        result.acceptance_tests_failed = acceptance.acceptance_tests_failed
        if acceptance.overall != "pass":
            result.overall = "fail"
            result.reason_code = acceptance.reason_code
            return result

    result.overall = "pass"
    result.reason_code = "DEPLOY_SMOKE_PROBE_OK"
    return result


def run_deploy_healing_loop(
    repo: Path,
    scratchpad: Dict[str, str],
    publish_handler: Callable[[str], bool],
    *,
    story_id: str = "",
    orchestrator_run_id: str = "",
) -> HealingLoopResult:
    """Bounded retry loop re-entering US-0054 publish PASS path on probe FAIL.

    publish_handler: callable that re-runs publish PASS path; returns True on success.
    Retries up to AUTO_SOVEREIGN_DEPLOY_RETRY_MAX. Idempotency invariant: no duplicate
    ledger rows (US-0103 `retry_count` field); deploy target overwrite safe.
    """
    result = HealingLoopResult(enabled=False)
    if not is_self_healing_deploy_enabled(scratchpad):
        result.reason_code = ReasonCode.DEPLOY_HEALING_DISABLED.value
        return result

    result.enabled = True
    retry_max = get_retry_max(scratchpad)
    result.retry_max = retry_max

    probe = run_smoke_probe_chain(scratchpad)
    result.probe_result = probe.to_dict()

    if probe.overall == "pass":
        result.reason_code = probe.reason_code
        return result

    for attempt in range(1, retry_max + 1):
        result.retry_count = attempt
        reason_log = f"{ReasonCode.DEPLOY_HEALING_RETRY_ATTEMPT.value} attempt={attempt}/{retry_max}"
        try:
            publish_ok = publish_handler(reason_log)
        except Exception:
            publish_ok = False

        if not publish_ok:
            result.reason_code = ReasonCode.DEPLOY_HEALING_RETRY_CAP_EXHAUSTED.value
            break

        probe = run_smoke_probe_chain(scratchpad)
        result.probe_result = probe.to_dict()

        if probe.overall == "pass":
            result.reason_code = probe.reason_code
            return result

    result.reason_code = ReasonCode.DEPLOY_HEALING_RETRY_CAP_EXHAUSTED.value
    return result


def emit_deploy_deferral(
    repo: Path,
    scratchpad: Dict[str, str],
    *,
    story_id: str = "",
    orchestrator_run_id: str = "",
    smoke_summary: str = "",
    retry_max: Optional[int] = None,
) -> Tuple[Optional[str], str]:
    """Emit DEPLOY_DEFERRED tuple after retry-cap exhaustion.

    Calls US-0107 `append_deferral(work_item_kind=deploy)`. Orchestrator continues
    per `AUTO_SOVEREIGN_DEFERRAL_POLICY` — does NOT halt.
    """
    if append_deferral is None or not is_sovereign_loop_enabled:
        return None, ReasonCode.DEPLOY_HEALING_DISABLED.value

    if not is_sovereign_loop_enabled(scratchpad):
        return None, "SOVEREIGN_LOOP_DISABLED"

    if retry_max is None:
        retry_max = get_retry_max(scratchpad)

    remediation = smoke_summary[:512] if smoke_summary else "deploy smoke probe failed; retry cap exhausted"

    deferral_id, reason = append_deferral(
        repo,
        scratchpad,
        reason_code="DEPLOY_DEFERRED",
        work_item_kind="deploy",
        work_item_ref=story_id,
        source_orchestrator_run_id=orchestrator_run_id,
        remediation_hint=remediation,
        blocked_by_phase="release",
        retry_count=retry_max,
    )
    return deferral_id, reason


def self_test() -> str:
    """Emit `[SELF_HEALING_DEPLOY_VALIDATION_OK]` when lib loads and defaults resolve."""
    defaults = {
        AUTO_SOVEREIGN_SELF_HEALING_DEPLOY_KEY: "0",
        AUTO_SOVEREIGN_DEPLOY_RETRY_MAX_KEY: str(DEFAULT_RETRY_MAX),
        AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC_KEY: str(DEFAULT_SMOKE_TIMEOUT_SEC),
        AUTO_SOVEREIGN_DEPLOY_PROBE_KIND_KEY: DEFAULT_PROBE_KIND,
        SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH_KEY: DEFAULT_ACCEPTANCE_SMOKE_PATH,
        AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT_KEY: "",
    }
    assert not is_self_healing_deploy_enabled(defaults)
    assert get_retry_max(defaults) == DEFAULT_RETRY_MAX
    assert get_smoke_timeout_sec(defaults) == DEFAULT_SMOKE_TIMEOUT_SEC
    assert get_probe_kind(defaults) == ProbeKind.BOTH
    assert get_acceptance_smoke_path(defaults) == DEFAULT_ACCEPTANCE_SMOKE_PATH
    assert resolve_health_endpoint_url(defaults) is None
    probe = run_smoke_probe_chain(defaults)
    assert probe.overall == "pass"
    return "[SELF_HEALING_DEPLOY_VALIDATION_OK]"


if __name__ == "__main__":
    print(self_test())
