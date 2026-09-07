"""
Dev environment auto-launch profile: load, detect, classify, relaunch, connect (US-0098 / DEC-0084).
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
import host_runtime_config_lib as hrc  # noqa: E402

SCHEMA_VERSION = 1
DEFAULT_PROFILE_PATH = ".cursor/dev-environment.json"
MAX_RETRY_COUNT = 2
RETRY_DELAYS_SECONDS = (5, 15)

VALID_DETECTED_MODES = frozenset({"local", "docker-host-local", "docker", "ssh"})
VALID_TIERS = frozenset({"A", "B", "C"})
CONNECT_STANDARD_KEYS = frozenset({"endpoint", "health_path"})
SECRET_LIKE_PATTERN = re.compile(
    r"(?i)(password|secret|token|api[_-]?key|private[_-]?key)\s*[:=]\s*['\"]?[^'\"]{8,}"
)

# DEV_ENV_PROFILE_* reason codes (DEC-0084 §10)
DEV_ENV_PROFILE_DISABLED = "DEV_ENV_PROFILE_DISABLED"
DEV_ENV_PROFILE_INVALID = "DEV_ENV_PROFILE_INVALID"
DEV_ENV_PROFILE_MISSING = "DEV_ENV_PROFILE_MISSING"
DEV_ENV_DETECT_AMBIGUOUS = "DEV_ENV_DETECT_AMBIGUOUS"
DEV_ENV_COMPOSE_UNRESOLVED = "DEV_ENV_COMPOSE_UNRESOLVED"
DEV_ENV_TARGET_DISABLED = "DEV_ENV_TARGET_DISABLED"
DEV_ENV_SECRET_SURFACE_VIOLATION = "DEV_ENV_SECRET_SURFACE_VIOLATION"

# DEV_ENV_RELAUNCH_* reason codes (DEC-0084 §10)
DEV_ENV_RELAUNCH_SKIPPED_NO_SURFACE = "DEV_ENV_RELAUNCH_SKIPPED_NO_SURFACE"
DEV_ENV_RELAUNCH_SKIPPED_PROFILE_OFF = "DEV_ENV_RELAUNCH_SKIPPED_PROFILE_OFF"
DEV_ENV_RELAUNCH_FAILED = "DEV_ENV_RELAUNCH_FAILED"
DEV_ENV_RELAUNCH_RETRY_EXHAUSTED = "DEV_ENV_RELAUNCH_RETRY_EXHAUSTED"
DEV_ENV_RELAUNCH_TIMEOUT = "DEV_ENV_RELAUNCH_TIMEOUT"
DEV_ENV_CONNECT_UNAVAILABLE = "DEV_ENV_CONNECT_UNAVAILABLE"

PROFILE_REASON_CODES = (
    DEV_ENV_PROFILE_DISABLED,
    DEV_ENV_PROFILE_INVALID,
    DEV_ENV_PROFILE_MISSING,
    DEV_ENV_DETECT_AMBIGUOUS,
    DEV_ENV_COMPOSE_UNRESOLVED,
    DEV_ENV_TARGET_DISABLED,
    DEV_ENV_SECRET_SURFACE_VIOLATION,
)

RELAUNCH_REASON_CODES = (
    DEV_ENV_RELAUNCH_SKIPPED_NO_SURFACE,
    DEV_ENV_RELAUNCH_SKIPPED_PROFILE_OFF,
    DEV_ENV_RELAUNCH_FAILED,
    DEV_ENV_RELAUNCH_RETRY_EXHAUSTED,
    DEV_ENV_RELAUNCH_TIMEOUT,
    DEV_ENV_CONNECT_UNAVAILABLE,
)

# DEV_ENV_BOOTSTRAP_* reason codes (DEC-0084 § bootstrap posture / US-0099)
DEV_ENV_BOOTSTRAP_COPIED = "DEV_ENV_BOOTSTRAP_COPIED"
DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS = "DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS"
DEV_ENV_BOOTSTRAP_PATH_INVALID = "DEV_ENV_BOOTSTRAP_PATH_INVALID"
DEV_ENV_BOOTSTRAP_SOURCE_MISSING = "DEV_ENV_BOOTSTRAP_SOURCE_MISSING"

BOOTSTRAP_REASON_CODES = (
    DEV_ENV_BOOTSTRAP_COPIED,
    DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS,
    DEV_ENV_BOOTSTRAP_PATH_INVALID,
    DEV_ENV_BOOTSTRAP_SOURCE_MISSING,
)

SCRATCHPAD_EXAMPLE_REL = ".cursor/scratchpad.local.example.md"
SCRATCHPAD_BASELINE_REL = ".cursor/scratchpad.md"
SCRATCHPAD_LOCAL_REL = ".cursor/scratchpad.local.md"
DEV_ENV_EXAMPLE_REL = ".cursor/dev-environment.json.example"

TIER_A_PATTERNS = (
    "Dockerfile",
    "Dockerfile.*",
    "*Dockerfile",
    "docker-compose*.yml",
    "docker-compose*.yaml",
    "compose.y*ml",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "Pipfile.lock",
    "poetry.lock",
    "go.sum",
    "Cargo.lock",
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "Gemfile.lock",
)

TIER_B_PATTERNS = (
    "*.env.example",
    "nginx*.conf",
    "traefik*.yml",
    "traefik*.yaml",
    "traefik*.toml",
    "application.y*ml",
    "application.y*aml",
    "scripts/docker/**",
    "docker/**/entrypoint*",
    "docker/**/Dockerfile*",
)

TIER_C_SKIP_PREFIXES = (
    "docs/",
    "handoffs/",
    "sprints/",
    "decisions/",
    "tests/",
    ".cursor/commands/",
    "template/docs/",
)


def _normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def read_merged_scratchpad(target_root: Path) -> Dict[str, str]:
    """Resolve shared governance keys via host-neutral config (US-0131 / DEC-0131)."""
    resolved = hrc.resolve_runtime_config(target_root, raise_on_fatal=False)
    return dict(resolved.values)


def resolve_profile_path(
    target_root: Path | str,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Tuple[Optional[Path], Optional[str]]:
    """Resolve profile path from scratchpad override or default; fail closed on invalid override."""
    root = Path(target_root).resolve()
    pad = scratchpad or {}
    override = (pad.get("DEV_ENVIRONMENT_CONFIG") or "").strip()
    rel = override if override else DEFAULT_PROFILE_PATH
    norm = _normalize_path(rel)

    if os.path.isabs(rel) or (len(rel) > 1 and rel[1] == ":"):
        return None, DEV_ENV_BOOTSTRAP_PATH_INVALID
    if ".." in norm.split("/"):
        return None, DEV_ENV_BOOTSTRAP_PATH_INVALID
    if not norm.endswith(".json"):
        return None, DEV_ENV_BOOTSTRAP_PATH_INVALID

    resolved = (root / norm).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return None, DEV_ENV_BOOTSTRAP_PATH_INVALID
    return resolved, None


def bootstrap_dev_environment_profile(
    target_root: Path | str,
    source_root: Optional[Path | str] = None,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Tuple[str, str]:
    """
    Copy example profile when target absent (non-destructive).
    Returns (reason_code, log_channel) where log_channel is stdout or stderr.
    """
    root = Path(target_root).resolve()
    if source_root is None:
        src_root = Path(__file__).resolve().parent.parent / "template"
    else:
        src_root = Path(source_root).resolve()

    profile_path, path_err = resolve_profile_path(root, scratchpad)
    if path_err:
        print(f"[DEV_ENV_BOOTSTRAP_ERROR] {path_err}", file=sys.stderr)
        return path_err, "stderr"

    source_path = src_root / DEV_ENV_EXAMPLE_REL
    if not source_path.is_file():
        print(f"[DEV_ENV_BOOTSTRAP_ERROR] {DEV_ENV_BOOTSTRAP_SOURCE_MISSING}", file=sys.stderr)
        return DEV_ENV_BOOTSTRAP_SOURCE_MISSING, "stderr"

    rel_target = profile_path.relative_to(root).as_posix()
    if profile_path.is_file():
        print(f"[DEV_ENV_BOOTSTRAP_OK] skipped: profile exists at {rel_target}")
        return DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS, "stdout"

    profile_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, profile_path)
    print(f"[DEV_ENV_BOOTSTRAP_OK] copied: {rel_target}")
    return DEV_ENV_BOOTSTRAP_COPIED, "stdout"


def run_bootstrap_cli(target: Path, source_root: Path) -> int:
    scratchpad = read_merged_scratchpad(target)
    reason, _channel = bootstrap_dev_environment_profile(target, source_root, scratchpad)
    if reason in (DEV_ENV_BOOTSTRAP_PATH_INVALID, DEV_ENV_BOOTSTRAP_SOURCE_MISSING):
        return 1
    return 0


def _check_secret_literals(obj: Any, path: str = "") -> Optional[str]:
    if isinstance(obj, dict):
        for key, value in obj.items():
            full = f"{path}.{key}" if path else key
            if key == "connect" and isinstance(value, dict):
                for ck, cv in value.items():
                    if ck not in CONNECT_STANDARD_KEYS and not ck.endswith("Env"):
                        return f"connect key must be *Env or standard: {ck}"
                    if isinstance(cv, str) and SECRET_LIKE_PATTERN.search(cv):
                        return DEV_ENV_SECRET_SURFACE_VIOLATION
            child = _check_secret_literals(value, full)
            if child:
                return child
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            child = _check_secret_literals(item, f"{path}[{i}]")
            if child:
                return child
    elif isinstance(obj, str):
        if SECRET_LIKE_PATTERN.search(obj):
            return DEV_ENV_SECRET_SURFACE_VIOLATION
    return None


def validate_profile_schema(data: Any) -> List[str]:
    codes: List[str] = []
    if not isinstance(data, dict):
        return [DEV_ENV_PROFILE_INVALID]

    if data.get("schema_version") != SCHEMA_VERSION:
        codes.append(DEV_ENV_PROFILE_INVALID)

    mode = data.get("detected_mode")
    if mode is not None and mode not in VALID_DETECTED_MODES:
        codes.append(DEV_ENV_PROFILE_INVALID)

    connect = data.get("connect")
    if connect is not None:
        if not isinstance(connect, dict):
            codes.append(DEV_ENV_PROFILE_INVALID)
        else:
            for ck in connect:
                if ck not in CONNECT_STANDARD_KEYS and not ck.endswith("Env"):
                    codes.append(DEV_ENV_SECRET_SURFACE_VIOLATION)

    env_refs = data.get("env_refs")
    if env_refs is not None and not isinstance(env_refs, list):
        codes.append(DEV_ENV_PROFILE_INVALID)

    secret_violation = _check_secret_literals(data)
    if secret_violation == DEV_ENV_SECRET_SURFACE_VIOLATION:
        codes.append(DEV_ENV_SECRET_SURFACE_VIOLATION)

    return codes


def load_profile(path: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Parse JSON profile; reject inline secrets; names-only schema validation."""
    if not os.path.isfile(path):
        return None, DEV_ENV_PROFILE_MISSING
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None, DEV_ENV_PROFILE_INVALID

    codes = validate_profile_schema(data)
    if codes:
        return None, codes[0]
    return data, None


def _match_tier_patterns(rel_path: str, patterns: Tuple[str, ...]) -> bool:
    norm = _normalize_path(rel_path)
    base = os.path.basename(norm)
    for pat in patterns:
        if fnmatch.fnmatch(norm, pat) or fnmatch.fnmatch(base, pat):
            return True
        if "**" in pat:
            prefix = pat.split("**")[0]
            if norm.startswith(prefix) and fnmatch.fnmatch(norm, pat):
                return True
    return False


def classify_touched_files(paths: List[str]) -> Optional[str]:
    """Return highest matching tier A/B/C or None when no runtime surface matched."""
    highest: Optional[str] = None
    tier_rank = {"A": 3, "B": 2, "C": 1}
    for raw in paths:
        rel = _normalize_path(raw)
        if any(rel.startswith(p) for p in TIER_C_SKIP_PREFIXES):
            if not (_match_tier_patterns(rel, TIER_A_PATTERNS) or _match_tier_patterns(rel, TIER_B_PATTERNS)):
                continue
        if _match_tier_patterns(rel, TIER_A_PATTERNS):
            if highest is None or tier_rank["A"] > tier_rank.get(highest, 0):
                highest = "A"
        elif _match_tier_patterns(rel, TIER_B_PATTERNS):
            if highest is None or tier_rank["B"] > tier_rank.get(highest, 0):
                highest = "B"
        elif not any(rel.startswith(p) for p in TIER_C_SKIP_PREFIXES):
            if highest is None:
                highest = "C"
    return highest


def _read_remote_config(repo: Path) -> Optional[Dict[str, Any]]:
    remote_path = repo / ".cursor" / "remote.json"
    if not remote_path.is_file():
        return None
    try:
        with open(remote_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _resolve_us0086_remote_target(
    repo: Path, scratchpad: Dict[str, str]
) -> Optional[Tuple[str, Optional[str]]]:
    """US-0086 precedence: remote docker/ssh wins over docker-host-local."""
    if scratchpad.get("AUTO_REMOTE_AUTOMATION_PROFILE", "off") != "deterministic_v1":
        return None
    remote = _read_remote_config(repo)
    if not remote:
        return None
    default_id = remote.get("defaultTarget")
    targets = remote.get("targets") or []
    for target in targets:
        if not isinstance(target, dict):
            continue
        tid = target.get("id")
        if tid != default_id:
            continue
        if not target.get("enabled", False):
            return None, DEV_ENV_TARGET_DISABLED
        ttype = target.get("type")
        if ttype == "docker":
            return "docker", None
        if ttype == "ssh":
            return "ssh", None
    return None


def _compose_resolvable(repo: Path, profile: Optional[Dict[str, Any]]) -> bool:
    candidates: List[Path] = []
    if profile and profile.get("compose_file"):
        candidates.append(repo / profile["compose_file"])
    candidates.extend(
        [
            repo / "docker-compose.yml",
            repo / "docker-compose.yaml",
            repo / "compose.yml",
            repo / "compose.yaml",
        ]
    )
    return any(p.is_file() for p in candidates)


def _local_docker_cli_succeeds() -> bool:
    try:
        proc = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        return proc.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def _dev_server_inferable(scratchpad: Dict[str, str]) -> bool:
    cmd = (scratchpad.get("DEV_SERVER_COMMAND") or "").strip()
    port = (scratchpad.get("DEV_SERVER_PORT") or "").strip()
    return bool(cmd or port)


def detect_mode(
    repo: Path,
    profile: Optional[Dict[str, Any]],
    scratchpad: Dict[str, str],
) -> Tuple[Optional[str], Optional[str]]:
    """
    Detection precedence (DEC-0084 §3):
    profile off -> skip; US-0086 remote wins; compose+local docker -> docker-host-local;
    DEV_SERVER_* -> local; else DEV_ENV_DETECT_AMBIGUOUS.
    """
    if scratchpad.get("DEV_AUTO_LAUNCH_PROFILE", "off") == "off":
        return None, DEV_ENV_PROFILE_DISABLED

    remote_result = _resolve_us0086_remote_target(repo, scratchpad)
    if remote_result is not None:
        if isinstance(remote_result, tuple) and len(remote_result) == 2:
            mode, reason = remote_result
            if mode:
                return mode, reason
            if reason:
                return None, reason

    if _compose_resolvable(repo, profile) and _local_docker_cli_succeeds():
        return "docker-host-local", None

    if _dev_server_inferable(scratchpad):
        return "local", None

    if profile and profile.get("detected_mode") in VALID_DETECTED_MODES:
        return profile["detected_mode"], None

    return None, DEV_ENV_DETECT_AMBIGUOUS


def build_relaunch_plan(
    mode: str,
    tier: Optional[str],
    profile: Dict[str, Any],
) -> List[str]:
    """Command list for tier recipe; no .env reads; retry_count max 2 enforced by caller."""
    if tier is None:
        return []
    service = profile.get("service") or "app"
    compose_file = profile.get("compose_file") or "docker-compose.yml"
    commands: List[str] = []
    if tier == "A":
        if mode in ("docker-host-local", "docker"):
            commands = [
                f"docker compose -f {compose_file} build {service}",
                f"docker compose -f {compose_file} up -d {service}",
            ]
        elif mode == "local":
            cmd = profile.get("rebuild_recipe", {}).get("local_build_command")
            if cmd:
                commands = [cmd]
    elif tier == "B":
        if mode in ("docker-host-local", "docker"):
            commands = [f"docker compose -f {compose_file} restart {service}"]
        elif mode == "local":
            cmd = profile.get("rebuild_recipe", {}).get("restart_command")
            if cmd:
                commands = [cmd]
    elif tier == "C":
        if mode == "local":
            cmd = profile.get("rebuild_recipe", {}).get("dev_server_command")
            if not cmd:
                cmd = os.environ.get("DEV_SERVER_COMMAND", "").strip()
            if cmd:
                commands = [cmd]
        elif mode == "docker-host-local":
            restart_on_change = profile.get("rebuild_recipe", {}).get(
                "restart_on_source_change", False
            )
            if restart_on_change:
                commands = [f"docker compose -f {compose_file} restart {service}"]
    return commands


def format_connect_block(profile: Dict[str, Any], outcome: str) -> str:
    """Markdown Connect block with mandatory names-only fields."""
    connect = profile.get("connect") or {}
    env_refs = sorted(set(profile.get("env_refs") or []))
    lines = [
        "## Connect",
        "",
        f"- **runtime_mode**: {profile.get('detected_mode', 'unknown')}",
        f"- **connect_endpoint**: {connect.get('endpoint', '(unset)')}",
        f"- **health_path**: {connect.get('health_path', '/')}",
        f"- **service_id**: {profile.get('service', '')}",
        f"- **container_id**: (resolve via operator shell)",
        f"- **target_id**: {profile.get('target_id', '')}",
        f"- **env_refs**: {', '.join(env_refs) if env_refs else '(none)'}",
        f"- **relaunch_outcome**: {outcome}",
        "",
    ]
    return "\n".join(lines)


def run_self_test() -> int:
    fixture_path = Path(__file__).resolve().parent.parent / "template" / ".cursor" / "dev-environment.json.example"
    data, err = load_profile(str(fixture_path))
    if err or not data:
        print(f"DEV_ENV_SELF_TEST_FAIL: load_profile {err}", file=sys.stderr)
        return 1

    tier_a = classify_touched_files(["docker-compose.yml", "docs/foo.md"])
    if tier_a != "A":
        print(f"DEV_ENV_SELF_TEST_FAIL: tier A expected, got {tier_a}", file=sys.stderr)
        return 1

    tier_none = classify_touched_files(["docs/engineering/runbook.md"])
    if tier_none is not None:
        print(f"DEV_ENV_SELF_TEST_FAIL: docs should skip, got {tier_none}", file=sys.stderr)
        return 1

    scratchpad = {"DEV_AUTO_LAUNCH_PROFILE": "off"}
    mode, reason = detect_mode(Path("."), data, scratchpad)
    if mode is not None or reason != DEV_ENV_PROFILE_DISABLED:
        print(f"DEV_ENV_SELF_TEST_FAIL: off gate {mode}/{reason}", file=sys.stderr)
        return 1

    block = format_connect_block(data, "success")
    for field in (
        "runtime_mode",
        "connect_endpoint",
        "health_path",
        "service_id",
        "container_id",
        "target_id",
        "env_refs",
        "relaunch_outcome",
    ):
        if field not in block:
            print(f"DEV_ENV_SELF_TEST_FAIL: missing {field}", file=sys.stderr)
            return 1

    plan = build_relaunch_plan("docker-host-local", "A", data)
    if not plan or "docker compose" not in plan[0]:
        print("DEV_ENV_SELF_TEST_FAIL: relaunch plan", file=sys.stderr)
        return 1

    if MAX_RETRY_COUNT != 2:
        print("DEV_ENV_SELF_TEST_FAIL: retry_count", file=sys.stderr)
        return 1

    print("[DEV_ENVIRONMENT_SELF_TEST_OK]")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Dev environment profile helper (US-0098).")
    p.add_argument("--self-test", action="store_true", help="Run built-in checks.")
    p.add_argument("--load", metavar="PATH", help="Load and validate profile path.")
    p.add_argument("--bootstrap", action="store_true", help="Bootstrap dev-environment profile (US-0099).")
    p.add_argument("--target", metavar="PATH", help="Consumer repository root (default: cwd).")
    p.add_argument(
        "--source-root",
        metavar="PATH",
        help="Packaged template root (default: <pkg>/template).",
    )
    args = p.parse_args()

    if args.self_test:
        return run_self_test()

    if args.bootstrap:
        target = Path(args.target or ".").resolve()
        if args.source_root:
            source_root = Path(args.source_root).resolve()
        else:
            source_root = Path(__file__).resolve().parent.parent / "template"
        return run_bootstrap_cli(target, source_root)

    if args.load:
        _, err = load_profile(args.load)
        if err:
            print(err, file=sys.stderr)
            return 1
        print("[DEV_ENVIRONMENT_LOAD_OK]")
        return 0

    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
