#!/usr/bin/env python3
"""Host-neutral Its-Magic runtime configuration (US-0131 / DEC-0131).

Canonical SOT: `.its-magic/config{,.local,.example}.json`.
Cursor `.cursor/scratchpad*` is a DEC-0055 Model B compatibility adapter into
the same `shared` KEY namespace. OpenCode-only resolves from `.its-magic/` +
code defaults without requiring `.cursor/`.

US-0132 boundary: `MODEL_*` / `MODEL_TIER_*` keys are ignored (not validated).
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

SCHEMA_VERSION_SUPPORTED = 1

KIT_DIR_NAME = ".its-magic"
CONFIG_EXAMPLE_REL = f"{KIT_DIR_NAME}/config.example.json"
CONFIG_BASELINE_REL = f"{KIT_DIR_NAME}/config.json"
CONFIG_LOCAL_REL = f"{KIT_DIR_NAME}/config.local.json"

CURSOR_EXAMPLE_REL = ".cursor/scratchpad.local.example.md"
CURSOR_BASELINE_REL = ".cursor/scratchpad.md"
CURSOR_LOCAL_REL = ".cursor/scratchpad.local.md"

HOST_CONFIG_SCHEMA_UNSUPPORTED = "HOST_CONFIG_SCHEMA_UNSUPPORTED"
HOST_CONFIG_INVALID = "HOST_CONFIG_INVALID"
HOST_CONFIG_MISSING_REQUIRED = "HOST_CONFIG_MISSING_REQUIRED"
HOST_CONFIG_PATH_FORBIDDEN = "HOST_CONFIG_PATH_FORBIDDEN"
HOST_CONFIG_SECRET_REJECTED = "HOST_CONFIG_SECRET_REJECTED"
HOST_CONFIG_KEY_SHADOWED = "HOST_CONFIG_KEY_SHADOWED"

HOST_CONFIG_CODES = (
    HOST_CONFIG_SCHEMA_UNSUPPORTED,
    HOST_CONFIG_INVALID,
    HOST_CONFIG_MISSING_REQUIRED,
    HOST_CONFIG_PATH_FORBIDDEN,
    HOST_CONFIG_SECRET_REJECTED,
    HOST_CONFIG_KEY_SHADOWED,
)

# Capability classes (R-0116 DQ7 / DEC-0131).
CAP_SHARED = "shared"
CAP_CURSOR_ONLY = "cursor_only"
CAP_OPENCODE_ONLY = "opencode_only"
CAP_US0132_OWNED = "us0132_owned"

CURSOR_CAPABILITY_UNAVAILABLE = "CURSOR_CAPABILITY_UNAVAILABLE"
OPENCODE_CAPABILITY_UNAVAILABLE = "OPENCODE_CAPABILITY_UNAVAILABLE"
US0132_CAPABILITY_OUT_OF_SCOPE = "US0132_CAPABILITY_OUT_OF_SCOPE"

CAPABILITY_MATRIX: Dict[str, Dict[str, str]] = {
    CAP_SHARED: {
        "examples": "DELIVERY_MODE, TOKEN_PROFILE, AUTO_*, intake/work-kind, triad thresholds",
        "unavailable": "HOST_CONFIG_* fail-closed or defaults",
    },
    CAP_CURSOR_ONLY: {
        "examples": ".cursor/rules/*.mdc, Cursor browser MCP UAT, pair-parity validators",
        "unavailable": CURSOR_CAPABILITY_UNAVAILABLE,
    },
    CAP_OPENCODE_ONLY: {
        "examples": ".opencode/agents Layer-1, orchestrator plugin, OPENCODE_* codes",
        "unavailable": "OPENCODE_* (US-0124/0126) unchanged",
    },
    CAP_US0132_OWNED: {
        "examples": "model catalogs, MODEL_*, materializers",
        "unavailable": US0132_CAPABILITY_OUT_OF_SCOPE,
    },
}

# Illustrative built-in defaults for governance keys used by shared-kernel scripts.
CODE_DEFAULTS: Dict[str, str] = {
    "AUTO_FLOW_MODE": "manual",
    "PHASE_MODE": "interactive",
    "PERMISSION_MODE": "interactive",
    "AUTO_LOOP_MAX_CYCLES": "32",
    "DONE": "0",
    "AUTO_BACKLOG_DRAIN": "0",
    "AUTO_BUG_QUEUE": "0",
    "CAVEMAN_COMPRESS_INPUT": "0",
    "SOVEREIGN_PARALLEL_DEV": "0",
    "UAT_BROWSER_PROBE_MODE": "cursor",
    "UAT_BROWSER_FALLBACK_CHAIN": "1",
    "STATE_HOT_MAX_LINES": "1200",
    "STATE_HOT_MAX_CHECKPOINTS": "80",
    "PO_TO_TL_HOT_MAX_LINES": "800",
    "PO_TO_TL_HOT_MAX_SECTIONS": "60",
    "ARCH_HOT_MAX_LINES": "3500",
    "ARCH_HOT_MAX_STORY_SECTIONS": "120",
}

_MODEL_KEY_RE = re.compile(r"^(MODEL_|MODEL_TIER_)")
_SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|secret|password|token|passwd)\s*[:=]"),
    re.compile(r"(?i)\b(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|xox[baprs]-)"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9\-._~+/]+=*"),
)

_ALLOWED_TOP_KEYS = frozenset({"schema_version", "shared", "host_overlays"})


class HostConfigError(Exception):
    """Fatal host-config resolution error."""

    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


@dataclass
class ResolvedRuntimeConfig:
    values: Dict[str, str] = field(default_factory=dict)
    provenance: Dict[str, str] = field(default_factory=dict)
    diagnostics: List[str] = field(default_factory=list)
    ok: bool = True
    fatal_code: Optional[str] = None
    host_mode_resolved: str = "both"


def _norm_root(repo_root: Path | str) -> Path:
    return Path(repo_root).resolve()


def config_root_override() -> Optional[Path]:
    raw = os.environ.get("ITS_MAGIC_CONFIG_ROOT", "").strip()
    if not raw:
        return None
    return Path(raw).resolve()


def kit_paths(repo_root: Path | str, *, config_root: Optional[Path] = None) -> Dict[str, Path]:
    root = _norm_root(repo_root)
    kit = (config_root or config_root_override() or (root / KIT_DIR_NAME)).resolve()
    if config_root is not None or config_root_override() is not None:
        # Test override: treat override dir as the kit directory itself.
        return {
            "example": kit / "config.example.json",
            "baseline": kit / "config.json",
            "local": kit / "config.local.json",
            "kit_dir": kit,
        }
    return {
        "example": root / CONFIG_EXAMPLE_REL,
        "baseline": root / CONFIG_BASELINE_REL,
        "local": root / CONFIG_LOCAL_REL,
        "kit_dir": root / KIT_DIR_NAME,
    }


def cursor_paths(repo_root: Path | str) -> Dict[str, Path]:
    root = _norm_root(repo_root)
    return {
        "example": root / CURSOR_EXAMPLE_REL,
        "baseline": root / CURSOR_BASELINE_REL,
        "local": root / CURSOR_LOCAL_REL,
    }


def detect_host_mode(repo_root: Path | str) -> str:
    """Auto-detect install surface. None callers must use this — never equate None with opencode."""
    root = _norm_root(repo_root)
    has_cursor = (root / ".cursor").is_dir()
    has_opencode = (root / ".opencode").is_dir()
    if has_opencode and not has_cursor:
        return "opencode"
    if has_cursor and not has_opencode:
        return "cursor"
    if has_cursor and has_opencode:
        return "both"
    # Neither surface present: treat as host-neutral kit-only (both semantics without Cursor adapter).
    return "both"


def is_model_key(key: str) -> bool:
    return bool(_MODEL_KEY_RE.match(key or ""))


def looks_like_secret(value: str) -> bool:
    text = value or ""
    return any(p.search(text) for p in _SECRET_PATTERNS)


def filter_model_keys(mapping: Mapping[str, str]) -> Dict[str, str]:
    """US-0132 boundary: drop MODEL_* / MODEL_TIER_* from shared resolve output."""
    return {k: v for k, v in mapping.items() if not is_model_key(k)}


def parse_scratchpad_text(text: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("- ") or line.startswith("<!--"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        if key:
            out[key] = val.strip()
    return out


def parse_scratchpad_file(path: Path) -> Dict[str, str]:
    if not path.is_file():
        return {}
    try:
        return parse_scratchpad_text(path.read_text(encoding="utf-8"))
    except OSError:
        return {}


def legacy_scratchpad_layers(repo_root: Path | str) -> Tuple[Dict[str, str], Dict[str, str], Dict[str, str]]:
    """Return (example, baseline, local) Cursor KEY maps (unmerged)."""
    paths = cursor_paths(repo_root)
    return (
        parse_scratchpad_file(paths["example"]),
        parse_scratchpad_file(paths["baseline"]),
        parse_scratchpad_file(paths["local"]),
    )


def legacy_scratchpad_adapter(repo_root: Path | str) -> Dict[str, str]:
    """DEC-0055 Model B pre-merge within Cursor layers: local > baseline > example."""
    example, baseline, local = legacy_scratchpad_layers(repo_root)
    merged: Dict[str, str] = {}
    for key in set(example) | set(baseline) | set(local):
        if key in local:
            merged[key] = local[key]
        elif key in baseline:
            merged[key] = baseline[key]
        else:
            merged[key] = example[key]
    return filter_model_keys(merged)


def _load_kit_json(path: Path, diagnostics: List[str]) -> Optional[Dict]:
    if not path.is_file():
        return None
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        diagnostics.append(f"{HOST_CONFIG_INVALID}: malformed JSON at {path}: {exc}")
        raise HostConfigError(HOST_CONFIG_INVALID, f"malformed JSON at {path}") from exc
    except OSError as exc:
        diagnostics.append(f"{HOST_CONFIG_INVALID}: unreadable {path}: {exc}")
        raise HostConfigError(HOST_CONFIG_INVALID, f"unreadable {path}") from exc

    if not isinstance(data, dict):
        raise HostConfigError(HOST_CONFIG_INVALID, f"root must be object at {path}")

    unknown = set(data.keys()) - _ALLOWED_TOP_KEYS
    if unknown:
        raise HostConfigError(
            HOST_CONFIG_INVALID,
            f"unknown top-level keys at {path}: {sorted(unknown)}",
        )

    if "schema_version" not in data:
        raise HostConfigError(HOST_CONFIG_INVALID, f"missing schema_version at {path}")
    ver = data["schema_version"]
    if not isinstance(ver, int) or isinstance(ver, bool):
        raise HostConfigError(HOST_CONFIG_INVALID, f"schema_version must be int at {path}")
    if ver != SCHEMA_VERSION_SUPPORTED:
        raise HostConfigError(
            HOST_CONFIG_SCHEMA_UNSUPPORTED,
            f"schema_version={ver} unsupported (supported={SCHEMA_VERSION_SUPPORTED})",
        )

    shared = data.get("shared", {})
    if shared is None:
        shared = {}
    if not isinstance(shared, dict):
        raise HostConfigError(HOST_CONFIG_INVALID, f"shared must be object at {path}")
    for k, v in shared.items():
        if not isinstance(k, str) or not isinstance(v, str):
            raise HostConfigError(
                HOST_CONFIG_INVALID,
                f"shared values must be string KEY→string at {path} key={k!r}",
            )
        if looks_like_secret(v):
            raise HostConfigError(
                HOST_CONFIG_SECRET_REJECTED,
                f"secret-shaped value rejected at {path} key={k}",
            )

    overlays = data.get("host_overlays", {})
    if overlays is None:
        overlays = {}
    if not isinstance(overlays, dict):
        raise HostConfigError(HOST_CONFIG_INVALID, f"host_overlays must be object at {path}")
    for host_name, overlay in overlays.items():
        if overlay is None:
            continue
        if not isinstance(overlay, dict):
            raise HostConfigError(
                HOST_CONFIG_INVALID,
                f"host_overlays.{host_name} must be object at {path}",
            )

    return data


def _shared_from_kit(data: Optional[Dict]) -> Dict[str, str]:
    if not data:
        return {}
    shared = data.get("shared") or {}
    return filter_model_keys({str(k): str(v) for k, v in shared.items()})


def classify_capability(key_or_surface: str) -> str:
    """Classify a key/surface into the capability matrix."""
    token = (key_or_surface or "").strip()
    if is_model_key(token) or token in ("model_catalog", "opencode_model_catalog", "materializer"):
        return CAP_US0132_OWNED
    if token.startswith(".cursor/") or token in (
        "cursor_rules",
        "cursor_browser_uat",
        "cursor_pair_parity",
        "cursor_remote",
        "cursor_task_spawn",
    ):
        return CAP_CURSOR_ONLY
    if token.startswith(".opencode/") or token.startswith("OPENCODE_") or token in (
        "opencode_agents",
        "opencode_plugin",
        "opencode_connect",
    ):
        return CAP_OPENCODE_ONLY
    return CAP_SHARED


def unsupported_capability_reason(cap_class: str, host_mode: str) -> Optional[str]:
    """Return deterministic skip/fail reason when a capability class is unavailable."""
    mode = (host_mode or "both").strip().lower()
    if cap_class == CAP_SHARED:
        return None
    if cap_class == CAP_US0132_OWNED:
        return US0132_CAPABILITY_OUT_OF_SCOPE
    if cap_class == CAP_CURSOR_ONLY and mode == "opencode":
        return CURSOR_CAPABILITY_UNAVAILABLE
    if cap_class == CAP_OPENCODE_ONLY and mode == "cursor":
        return OPENCODE_CAPABILITY_UNAVAILABLE
    return None


def reject_opencode_json_governance_dump(
    opencode_json_path: Path | str,
    kit_keys: Optional[Iterable[str]] = None,
) -> None:
    """Fail closed if kit governance keys are dumped into opencode.json{,c}."""
    path = Path(opencode_json_path)
    if not path.is_file():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HostConfigError(HOST_CONFIG_INVALID, f"cannot parse {path}: {exc}") from exc

    keys_to_check = set(kit_keys or CODE_DEFAULTS.keys())
    # Also scan common automation prefixes.
    found: List[str] = []

    def walk(obj, prefix: str = "") -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                key = str(k)
                path_key = f"{prefix}.{key}" if prefix else key
                if key in keys_to_check or key.startswith("AUTO_") or key.startswith("MAGIC_"):
                    found.append(path_key)
                walk(v, path_key)

    walk(data)
    if found:
        raise HostConfigError(
            HOST_CONFIG_PATH_FORBIDDEN,
            f"kit governance keys must not be dumped into {path}: {sorted(found)[:20]}",
        )


def resolve_runtime_config(
    repo_root: Path | str,
    *,
    host_mode: Optional[str] = None,
    required_keys: Optional[Iterable[str]] = None,
    config_root: Optional[Path] = None,
    cursor_as_sole_sot: bool = False,
    raise_on_fatal: bool = True,
) -> ResolvedRuntimeConfig:
    """Resolve shared runtime/governance keys (DEC-0131 §4 / R-0116 DQ6).

    Precedence (highest wins):
      1. (reserved) explicit one-run CLI/env — ITS_MAGIC_CONFIG_ROOT is test path only
      2. .its-magic/config.local.json shared.*
      3. Cursor local (adapter)
      4. .its-magic/config.json shared.*
      5. Cursor baseline (adapter)
      6. .its-magic/config.example.json
      7. Built-in code defaults

    host_mode=None means auto-detect (never treat None as OpenCode-only).
    HOST_CONFIG_PATH_FORBIDDEN only when OpenCode-only AND cursor_as_sole_sot=True.
    """
    root = _norm_root(repo_root)
    diagnostics: List[str] = []
    result = ResolvedRuntimeConfig(diagnostics=diagnostics)

    resolved_mode = (host_mode or detect_host_mode(root)).strip().lower()
    if resolved_mode not in ("cursor", "opencode", "both"):
        result.ok = False
        result.fatal_code = HOST_CONFIG_INVALID
        diagnostics.append(f"{HOST_CONFIG_INVALID}: unknown host_mode={resolved_mode!r}")
        if raise_on_fatal:
            raise HostConfigError(HOST_CONFIG_INVALID, f"unknown host_mode={resolved_mode!r}")
        return result
    result.host_mode_resolved = resolved_mode

    opencode_only = resolved_mode == "opencode"
    if cursor_as_sole_sot and opencode_only:
        result.ok = False
        result.fatal_code = HOST_CONFIG_PATH_FORBIDDEN
        diagnostics.append(
            f"{HOST_CONFIG_PATH_FORBIDDEN}: .cursor/ cannot be sole SOT on OpenCode-only"
        )
        if raise_on_fatal:
            raise HostConfigError(
                HOST_CONFIG_PATH_FORBIDDEN,
                ".cursor/ cannot be sole SOT on OpenCode-only",
            )
        return result

    paths = kit_paths(root, config_root=config_root)
    try:
        kit_local = _shared_from_kit(_load_kit_json(paths["local"], diagnostics))
        kit_base = _shared_from_kit(_load_kit_json(paths["baseline"], diagnostics))
        kit_example = _shared_from_kit(_load_kit_json(paths["example"], diagnostics))
    except HostConfigError as exc:
        result.ok = False
        result.fatal_code = exc.code
        diagnostics.append(str(exc))
        if raise_on_fatal:
            raise
        return result

    cursor_example: Dict[str, str] = {}
    cursor_baseline: Dict[str, str] = {}
    cursor_local: Dict[str, str] = {}
    if not opencode_only:
        cursor_example, cursor_baseline, cursor_local = legacy_scratchpad_layers(root)
        cursor_example = filter_model_keys(cursor_example)
        cursor_baseline = filter_model_keys(cursor_baseline)
        cursor_local = filter_model_keys(cursor_local)

    # Shadow diagnostic: kit local vs cursor local disagreement.
    strict = os.environ.get("HOST_CONFIG_STRICT", "0").strip() == "1"
    for key in set(kit_local) & set(cursor_local):
        if kit_local[key] != cursor_local[key]:
            msg = (
                f"{HOST_CONFIG_KEY_SHADOWED}: key={key} kit_local wins "
                f"(cursor_local ignored for shared namespace)"
            )
            diagnostics.append(msg)
            if strict:
                result.ok = False
                result.fatal_code = HOST_CONFIG_KEY_SHADOWED
                if raise_on_fatal:
                    raise HostConfigError(HOST_CONFIG_KEY_SHADOWED, f"key={key}")
                return result

    # Apply layers lowest → highest so highest wins.
    values: Dict[str, str] = {}
    provenance: Dict[str, str] = {}

    def apply(layer: Mapping[str, str], label: str) -> None:
        for k, v in layer.items():
            if is_model_key(k):
                continue
            if looks_like_secret(v):
                result.ok = False
                result.fatal_code = HOST_CONFIG_SECRET_REJECTED
                diagnostics.append(f"{HOST_CONFIG_SECRET_REJECTED}: key={k} layer={label}")
                if raise_on_fatal:
                    raise HostConfigError(HOST_CONFIG_SECRET_REJECTED, f"key={k} layer={label}")
                return
            values[k] = v
            provenance[k] = label

    apply(CODE_DEFAULTS, "code_defaults")
    apply(kit_example, "kit_example")
    if not opencode_only:
        apply(cursor_baseline, "cursor_baseline")
    apply(kit_base, "kit_baseline")
    if not opencode_only:
        apply(cursor_local, "cursor_local")
    apply(kit_local, "kit_local")

    if result.fatal_code:
        return result

    result.values = values
    result.provenance = provenance

    if required_keys:
        missing = []
        for key in required_keys:
            if is_model_key(key):
                continue
            val = values.get(key)
            if val is None or str(val).strip() == "":
                missing.append(key)
        if missing:
            result.ok = False
            result.fatal_code = HOST_CONFIG_MISSING_REQUIRED
            diagnostics.append(
                f"{HOST_CONFIG_MISSING_REQUIRED}: keys={','.join(missing)}"
            )
            if raise_on_fatal:
                raise HostConfigError(
                    HOST_CONFIG_MISSING_REQUIRED,
                    f"keys={','.join(missing)}",
                )
    return result


def materialize_kit_config_baseline(
    target_root: Path | str,
    source_example: Optional[Path] = None,
    *,
    mode: str = "missing",
) -> Tuple[bool, str]:
    """Materialize `.its-magic/config.json` from example when missing (Model B semantics).

    Never overwrites `.its-magic/config.local.json`.
    Never overwrites existing baseline unless mode == 'overwrite'.
    """
    root = _norm_root(target_root)
    kit_dir = root / KIT_DIR_NAME
    example = source_example or (kit_dir / "config.example.json")
    baseline = kit_dir / "config.json"
    local = kit_dir / "config.local.json"

    # Explicit never-overwrite local (even if somehow targeted).
    if local.is_file() and mode == "overwrite":
        # Local remains untouched; only baseline may overwrite.
        pass

    if not example.is_file():
        return False, f"HOST_CONFIG_INVALID: missing example at {example}"

    kit_dir.mkdir(parents=True, exist_ok=True)
    if baseline.is_file() and mode != "overwrite":
        return True, "baseline_skip: config.json already present"
    baseline.write_text(example.read_text(encoding="utf-8"), encoding="utf-8")
    return True, "baseline_materialize: wrote config.json from example"


def shared_kernel_modules() -> Sequence[str]:
    """Exhaustive R-0116 / T-004 migration inventory (marker 8)."""
    return (
        "scripts/auto_outer_driver.py",
        "scripts/opencode_auto_bridge.py",
        "scripts/enforce-triad-hot-surface.py",
        "scripts/dev_environment_lib.py",
        "scripts/caveman_compress_input.py",
        "scripts/parallel_dev_arbiter.py",
        "scripts/uat_probe_lib.py",
        "scripts/validate_autonomy_stop_matrix.py",
        "scripts/model_tier_validate.py",
    )


__all__ = [
    "CAPABILITY_MATRIX",
    "CODE_DEFAULTS",
    "HOST_CONFIG_CODES",
    "HOST_CONFIG_INVALID",
    "HOST_CONFIG_KEY_SHADOWED",
    "HOST_CONFIG_MISSING_REQUIRED",
    "HOST_CONFIG_PATH_FORBIDDEN",
    "HOST_CONFIG_SCHEMA_UNSUPPORTED",
    "HOST_CONFIG_SECRET_REJECTED",
    "HostConfigError",
    "ResolvedRuntimeConfig",
    "classify_capability",
    "detect_host_mode",
    "filter_model_keys",
    "is_model_key",
    "kit_paths",
    "legacy_scratchpad_adapter",
    "materialize_kit_config_baseline",
    "reject_opencode_json_governance_dump",
    "resolve_runtime_config",
    "shared_kernel_modules",
    "unsupported_capability_reason",
]
