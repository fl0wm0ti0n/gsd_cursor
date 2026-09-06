"""BUG-0015 OpenCode `/auto` plugin dispatch attach — 7 contract markers.

Markers per architecture.md # BUG-0015 / R-0114 DQ6. Additive only — do NOT
amend test_us0124_* / test_us0125_* bodies. Mock-ctx / static only; no live
OpenCode runtime probe.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_PATH = REPO_ROOT / "template" / ".opencode" / "plugins" / "orchestrator.ts"
ACTIVE_PLUGIN = REPO_ROOT / ".opencode" / "plugins" / "orchestrator.ts"
MOCK_PATH = REPO_ROOT / "tests" / "us0124" / "mock_ctx.ts"
HARNESS_PATH = REPO_ROOT / "tests" / "bug0015" / "run_harness.mjs"
AUTO_MD = REPO_ROOT / "template" / ".opencode" / "commands" / "auto.md"
ACTIVE_AUTO_MD = REPO_ROOT / ".opencode" / "commands" / "auto.md"
BRIDGE_PATH = REPO_ROOT / "scripts" / "opencode_auto_bridge.py"

SPAWN_LITERALS = (
    "ctx.session.create",
    "Session.create",
    "session.create(",
)


def _node_bin() -> str:
    node = shutil.which("node")
    if not node:
        raise AssertionError("node not on PATH — run tests/run-tests.ps1 Ensure-NodeOnPath")
    return node


def _run_harness(scenario: str) -> dict:
    proc = subprocess.run(
        [_node_bin(), "--experimental-strip-types", str(HARNESS_PATH), scenario],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    if proc.returncode != 0:
        raise AssertionError(
            f"harness scenario {scenario!r} failed rc={proc.returncode}: "
            f"stdout={proc.stdout!r} stderr={proc.stderr!r}"
        )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"harness scenario {scenario!r} produced non-JSON stdout: "
            f"{proc.stdout!r} (stderr={proc.stderr!r})"
        ) from exc


def test_bug0015_command_transform_registers_auto():
    """Marker 1 (AC-1): setup registers transform / editor.add({ name: "auto" })."""
    src = PLUGIN_PATH.read_text(encoding="utf-8")
    assert "command.transform" in src or "ctx.command.transform" in src
    assert 'name: "auto"' in src or "name: 'auto'" in src
    assert "editor.add" in src
    r = _run_harness("attach-registers-auto")
    assert r["attachSupported"] is True
    assert "auto" in r["editorAddNames"]
    assert r["hasExecute"] is True
    assert r["transformRegistered"] is True


def test_bug0015_auto_execute_invokes_spawn_phase():
    """Marker 2 (AC-1): mock execute → session.create with parentID/agent."""
    r = _run_harness("execute-invokes-spawn")
    assert r["ok"] is True, r
    calls = r["createCalls"]
    assert calls, "expected session.create call"
    assert calls[0]["parentID"] == "orchestrator-session-0"
    assert calls[0]["agent"] == "dev"
    assert r["sessionID"] and r["sessionID"] != calls[0]["parentID"]
    ev = r["evidence"]
    for field in (
        "parentID",
        "sessionID",
        "role",
        "phase_id",
        "timestamp",
        "fresh_context_marker",
    ):
        assert field in ev and ev[field], f"missing isolation field {field}: {ev}"


def test_bug0015_missing_attach_fail_closed():
    """Marker 3 (AC-2): no attach → OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED."""
    r = _run_harness("missing-attach")
    assert r["attachSupported"] is False
    assert r["attachReasonCode"] == "OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED"
    assert r["ok"] is False
    assert r["reasonCode"] == "OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED"


def test_bug0015_missing_session_create_fail_closed():
    """Marker 4 (AC-3): attach ok, create missing → OPENCODE_PLUGIN_SPAWN_UNSUPPORTED."""
    r = _run_harness("missing-session-create")
    assert r["attachSupported"] is True
    assert r["ok"] is False
    assert r["reasonCode"] == "OPENCODE_PLUGIN_SPAWN_UNSUPPORTED"


def test_bug0015_concurrent_reentry_fail_closed():
    """Marker 5 (AC-5): second `/auto` / dual-fire → OPENCODE_AUTO_ALREADY_RUNNING."""
    r = _run_harness("concurrent-reentry")
    assert r["secondOk"] is False
    assert r["secondReasonCode"] == "OPENCODE_AUTO_ALREADY_RUNNING"
    # Dual-fire secondary path (command.executed) also mutex-gated when present
    if r.get("eventReasonCode") is not None:
        assert r["eventReasonCode"] == "OPENCODE_AUTO_ALREADY_RUNNING"
    src = PLUGIN_PATH.read_text(encoding="utf-8")
    assert "7200" in src
    assert "Date.now()" in src
    assert "clearAutoMutex" in src or "autoMutex = null" in src


def test_bug0015_auto_md_dispatch_only_static():
    """Marker 6 (AC-6): auto.md ≤20 lines; no spawn literals (active + template)."""
    for path in (AUTO_MD, ACTIVE_AUTO_MD):
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        assert len(lines) <= 20, f"{path} has {len(lines)} lines > 20"
        assert "STOP" in text
        # Body after frontmatter
        parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.MULTILINE)
        body = parts[-1] if len(parts) >= 3 else text
        for forbidden in SPAWN_LITERALS:
            assert forbidden not in body, f"{path} body contains {forbidden!r}"
        assert not re.search(r"\bspawn\s*[(=]", body), f"{path} has spawn-call logic"
        assert re.search(r"^agent:\s*auto\s*$", text, re.MULTILINE)


def test_bug0015_compose_us0124_spawn_api_unchanged():
    """Marker 7 (AC-7): existing spawnPhase / reason-code exports present (read-only)."""
    src = PLUGIN_PATH.read_text(encoding="utf-8")
    assert "export async function spawnPhase" in src
    assert "OPENCODE_PLUGIN_SPAWN_UNSUPPORTED" in src
    assert "OPENCODE_SUBTASK_IGNORED" in src
    assert 'ctx.tool.hook("execute.before"' in src or 'tool.hook("execute.before"' in src
    assert "export function dispatchStopMatrix" in src
    assert "export function invokeHeadless" in src
    # Active ↔ template byte-identical for plugin
    assert ACTIVE_PLUGIN.read_bytes() == PLUGIN_PATH.read_bytes()
    r = _run_harness("static-info")
    assert r["hasSpawnPhase"] is True
    assert r["hasRunAutoLifecycle"] is True
    assert r["reasonCodes"]["PLUGIN_SPAWN_UNSUPPORTED"] == "OPENCODE_PLUGIN_SPAWN_UNSUPPORTED"
    assert (
        r["reasonCodes"]["PLUGIN_DISPATCH_ATTACH_UNSUPPORTED"]
        == "OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED"
    )
    assert r["reasonCodes"]["AUTO_ALREADY_RUNNING"] == "OPENCODE_AUTO_ALREADY_RUNNING"
    assert r["mutexTtlMs"] == 7200 * 1000
    assert BRIDGE_PATH.is_file(), "Python IsolationEvidence bridge missing"
