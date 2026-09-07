"""US-0131 host-neutral runtime config contract — 10 markers (DEC-0131 / R-0116 DQ9).

Static/fixture only — no live OpenCode CI probe.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import host_runtime_config_lib as hrc  # noqa: E402

RUNBOOK = REPO_ROOT / "docs" / "engineering" / "runbook.md"
RUNBOOK_TEMPLATE = REPO_ROOT / "template" / "docs" / "engineering" / "runbook.md"
INSTALLER = REPO_ROOT / "installer.py"
MANIFEST = REPO_ROOT / "docs" / "engineering" / "context" / "installer-owned-paths.manifest"
LIB = REPO_ROOT / "scripts" / "host_runtime_config_lib.py"
LIB_TEMPLATE = REPO_ROOT / "template" / "scripts" / "host_runtime_config_lib.py"
EXAMPLE = REPO_ROOT / ".its-magic" / "config.example.json"
EXAMPLE_TEMPLATE = REPO_ROOT / "template" / ".its-magic" / "config.example.json"

MARKERS = (
    "test_us0131_neutral_path_no_cursor_required",
    "test_us0131_cursor_adapter_preserves_dec0055_precedence",
    "test_us0131_opencode_only_resolves_shared_from_its_magic",
    "test_us0131_both_host_precedence_table",
    "test_us0131_rejects_opencode_json_governance_dump",
    "test_us0131_schema_fail_closed_codes",
    "test_us0131_installer_preserves_local_config",
    "test_us0131_shared_kernel_uses_resolver_not_hardcode",
    "test_us0131_model_keys_ignored_us0132_boundary",
    "test_us0131_capability_matrix_reason_codes_documented",
)

SHARED_KERNEL = hrc.shared_kernel_modules()


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_scratchpad(path: Path, mapping: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{k}={v}" for k, v in mapping.items()]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _kit_payload(shared: dict[str, str]) -> dict:
    return {
        "schema_version": 1,
        "shared": shared,
        "host_overlays": {"cursor": {}, "opencode": {}},
    }


def test_us0131_neutral_path_no_cursor_required(tmp_path: Path) -> None:
    """OpenCode-only / kit-only repo resolves without requiring .cursor/."""
    kit = tmp_path / ".its-magic"
    _write_json(kit / "config.example.json", _kit_payload({"AUTO_FLOW_MODE": "full_autonomy"}))
    (tmp_path / ".opencode").mkdir()
    assert not (tmp_path / ".cursor").exists()
    resolved = hrc.resolve_runtime_config(tmp_path, host_mode="opencode")
    assert resolved.ok
    assert resolved.values.get("AUTO_FLOW_MODE") == "full_autonomy"
    assert resolved.host_mode_resolved == "opencode"


def test_us0131_cursor_adapter_preserves_dec0055_precedence(tmp_path: Path) -> None:
    """Within Cursor layers: local > baseline > example (DEC-0055 Model B)."""
    _write_scratchpad(
        tmp_path / ".cursor" / "scratchpad.local.example.md",
        {"AUTO_QUIET": "0", "DONE": "0"},
    )
    _write_scratchpad(tmp_path / ".cursor" / "scratchpad.md", {"AUTO_QUIET": "1", "DONE": "0"})
    _write_scratchpad(tmp_path / ".cursor" / "scratchpad.local.md", {"AUTO_QUIET": "1", "DONE": "1"})
    adapted = hrc.legacy_scratchpad_adapter(tmp_path)
    assert adapted["AUTO_QUIET"] == "1"
    assert adapted["DONE"] == "1"
    resolved = hrc.resolve_runtime_config(tmp_path, host_mode="cursor")
    assert resolved.values["DONE"] == "1"
    assert resolved.provenance.get("DONE") == "cursor_local"


def test_us0131_opencode_only_resolves_shared_from_its_magic(tmp_path: Path) -> None:
    """OpenCode-only ignores Cursor scratchpad even if present on disk."""
    (tmp_path / ".opencode").mkdir()
    _write_json(
        tmp_path / ".its-magic" / "config.json",
        _kit_payload({"TOKEN_PROFILE": "lean"}),
    )
    _write_scratchpad(tmp_path / ".cursor" / "scratchpad.md", {"TOKEN_PROFILE": "standard"})
    # Detected as both because .cursor exists — force opencode mode.
    resolved = hrc.resolve_runtime_config(tmp_path, host_mode="opencode")
    assert resolved.values.get("TOKEN_PROFILE") == "lean"
    assert "cursor_baseline" not in resolved.provenance.get("TOKEN_PROFILE", "")


def test_us0131_both_host_precedence_table(tmp_path: Path) -> None:
    """DQ6: kit-local > cursor-local > kit-baseline > cursor-baseline > example > defaults."""
    (tmp_path / ".cursor").mkdir()
    (tmp_path / ".opencode").mkdir()
    _write_json(
        tmp_path / ".its-magic" / "config.example.json",
        _kit_payload({"DELIVERY_MODE": "from_example"}),
    )
    _write_scratchpad(tmp_path / ".cursor" / "scratchpad.md", {"DELIVERY_MODE": "from_cursor_base"})
    _write_json(
        tmp_path / ".its-magic" / "config.json",
        _kit_payload({"DELIVERY_MODE": "from_kit_base"}),
    )
    _write_scratchpad(tmp_path / ".cursor" / "scratchpad.local.md", {"DELIVERY_MODE": "from_cursor_local"})
    _write_json(
        tmp_path / ".its-magic" / "config.local.json",
        _kit_payload({"DELIVERY_MODE": "from_kit_local"}),
    )
    resolved = hrc.resolve_runtime_config(tmp_path, host_mode="both")
    assert resolved.values["DELIVERY_MODE"] == "from_kit_local"
    assert resolved.provenance["DELIVERY_MODE"] == "kit_local"
    # Shadow diagnostic when kit local and cursor local disagree.
    assert any(hrc.HOST_CONFIG_KEY_SHADOWED in d for d in resolved.diagnostics)


def test_us0131_rejects_opencode_json_governance_dump(tmp_path: Path) -> None:
    path = tmp_path / "opencode.json"
    path.write_text(
        json.dumps({"model": "placeholder", "AUTO_FLOW_MODE": "full_autonomy"}),
        encoding="utf-8",
    )
    with pytest.raises(hrc.HostConfigError) as exc:
        hrc.reject_opencode_json_governance_dump(path)
    assert exc.value.code == hrc.HOST_CONFIG_PATH_FORBIDDEN


def test_us0131_schema_fail_closed_codes(tmp_path: Path) -> None:
    bad = tmp_path / ".its-magic" / "config.json"
    _write_json(bad, {"schema_version": 99, "shared": {}})
    with pytest.raises(hrc.HostConfigError) as exc:
        hrc.resolve_runtime_config(tmp_path)
    assert exc.value.code == hrc.HOST_CONFIG_SCHEMA_UNSUPPORTED

    _write_json(bad, {"schema_version": 1, "shared": {"X": 1}})
    with pytest.raises(hrc.HostConfigError) as exc2:
        hrc.resolve_runtime_config(tmp_path)
    assert exc2.value.code == hrc.HOST_CONFIG_INVALID

    _write_json(bad, _kit_payload({}))
    with pytest.raises(hrc.HostConfigError) as exc3:
        hrc.resolve_runtime_config(tmp_path, required_keys=["MUST_EXIST_KEY"])
    assert exc3.value.code == hrc.HOST_CONFIG_MISSING_REQUIRED

    # PATH_FORBIDDEN only when OpenCode-only + cursor_as_sole_sot.
    (tmp_path / ".opencode").mkdir(exist_ok=True)
    with pytest.raises(hrc.HostConfigError) as exc4:
        hrc.resolve_runtime_config(
            tmp_path, host_mode="opencode", cursor_as_sole_sot=True
        )
    assert exc4.value.code == hrc.HOST_CONFIG_PATH_FORBIDDEN

    # host_mode=None must auto-detect — not treat as OpenCode-only PATH_FORBIDDEN alone.
    resolved = hrc.resolve_runtime_config(tmp_path, host_mode=None, cursor_as_sole_sot=False)
    assert resolved.ok


def test_us0131_installer_preserves_local_config(tmp_path: Path) -> None:
    src = REPO_ROOT
    example_src = src / ".its-magic" / "config.example.json"
    assert example_src.is_file()
    # Seed local that must never be overwritten.
    local = tmp_path / ".its-magic" / "config.local.json"
    _write_json(local, _kit_payload({"DONE": "1"}))
    local_bytes = local.read_bytes()

    sys.path.insert(0, str(REPO_ROOT))
    import installer  # noqa: E402

    assert installer.run_kit_config_postinstall(str(tmp_path), str(src), "missing", print_ok=False)
    assert local.read_bytes() == local_bytes
    assert (tmp_path / ".its-magic" / "config.example.json").is_file()
    assert (tmp_path / ".its-magic" / "config.json").is_file()

    # Upgrade must still preserve local.
    assert installer.run_kit_config_postinstall(str(tmp_path), str(src), "upgrade", print_ok=False)
    assert local.read_bytes() == local_bytes
    assert "config.local.json" in Path(REPO_ROOT / ".gitignore").read_text(encoding="utf-8")


def test_us0131_shared_kernel_uses_resolver_not_hardcode() -> None:
    for rel in SHARED_KERNEL:
        path = REPO_ROOT / rel
        assert path.is_file(), rel
        text = path.read_text(encoding="utf-8")
        assert "host_runtime_config_lib" in text or "resolve_runtime_config" in text, rel
        # Template mirror when present.
        tmpl = REPO_ROOT / "template" / rel
        if tmpl.is_file():
            assert "host_runtime_config_lib" in tmpl.read_text(encoding="utf-8") or (
                "resolve_runtime_config" in tmpl.read_text(encoding="utf-8")
            )


def test_us0131_model_keys_ignored_us0132_boundary(tmp_path: Path) -> None:
    _write_json(
        tmp_path / ".its-magic" / "config.json",
        _kit_payload(
            {
                "AUTO_FLOW_MODE": "manual",
                "MODEL_TIER_EXECUTE": "high",
                "MODEL_PO": "should-ignore",
            }
        ),
    )
    _write_scratchpad(
        tmp_path / ".cursor" / "scratchpad.md",
        {"MODEL_TIER_QA": "medium", "DONE": "0"},
    )
    resolved = hrc.resolve_runtime_config(tmp_path, host_mode="both")
    assert "MODEL_TIER_EXECUTE" not in resolved.values
    assert "MODEL_PO" not in resolved.values
    assert "MODEL_TIER_QA" not in resolved.values
    assert resolved.values.get("AUTO_FLOW_MODE") == "manual"
    assert resolved.values.get("DONE") == "0"


def test_us0131_capability_matrix_reason_codes_documented() -> None:
    assert set(hrc.CAPABILITY_MATRIX) == {
        hrc.CAP_SHARED,
        hrc.CAP_CURSOR_ONLY,
        hrc.CAP_OPENCODE_ONLY,
        hrc.CAP_US0132_OWNED,
    }
    for code in hrc.HOST_CONFIG_CODES:
        assert code.startswith("HOST_CONFIG_")

    runbook = RUNBOOK.read_text(encoding="utf-8")
    assert "## Cross-host runtime configuration (US-0131)" in runbook
    for code in hrc.HOST_CONFIG_CODES:
        assert code in runbook
    # US-0126 additive rows only.
    us0126 = runbook.split("## OpenCode host operator runbook (US-0126)", 1)[1]
    for code in (
        "HOST_CONFIG_SCHEMA_UNSUPPORTED",
        "HOST_CONFIG_INVALID",
        "HOST_CONFIG_MISSING_REQUIRED",
        "HOST_CONFIG_PATH_FORBIDDEN",
        "HOST_CONFIG_SECRET_REJECTED",
        "HOST_CONFIG_KEY_SHADOWED",
    ):
        assert code in us0126

    assert hrc.unsupported_capability_reason(hrc.CAP_CURSOR_ONLY, "opencode") == (
        hrc.CURSOR_CAPABILITY_UNAVAILABLE
    )
    assert hrc.unsupported_capability_reason(hrc.CAP_US0132_OWNED, "both") == (
        hrc.US0132_CAPABILITY_OUT_OF_SCOPE
    )

    # Parity of core surfaces.
    assert LIB.read_bytes() == LIB_TEMPLATE.read_bytes()
    assert EXAMPLE.read_bytes() == EXAMPLE_TEMPLATE.read_bytes()
    assert ".its-magic/config.example.json" in MANIFEST.read_text(encoding="utf-8")
    assert "run_kit_config_postinstall" in INSTALLER.read_text(encoding="utf-8")

    # Exactly 10 markers defined in this module.
    names = [n for n in globals() if n.startswith("test_us0131_")]
    assert sorted(names) == sorted(MARKERS)
    assert len(MARKERS) == 10
