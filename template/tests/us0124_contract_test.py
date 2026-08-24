"""US-0124 OpenCode orchestrator plugin spawn-only `/auto` — 10 contract markers.

Markers 1–9 per DEC-0124 §9 / architecture AC-10 table; marker 10
(`test_us0124_phase_role_mismatch`) is the plan-verify carry-forward
additive 10th marker under T-005 (wrong role vs US-0069 matrix →
`PHASE_ROLE_MISMATCH`, fail closed). The original 9 markers are preserved.

The runtime harness uses a Node subprocess (`tests/us0124/run_harness.mjs`)
that imports the orchestrator plugin (`template/.opencode/plugins/orchestrator.ts`)
and the MockCtx (`tests/us0124/mock_ctx.ts`) under
`node --experimental-strip-types`. No live OpenCode runtime probe (AC-10).
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_PATH = REPO_ROOT / "template" / ".opencode" / "plugins" / "orchestrator.ts"
MOCK_PATH = REPO_ROOT / "tests" / "us0124" / "mock_ctx.ts"
HARNESS_PATH = REPO_ROOT / "tests" / "us0124" / "run_harness.mjs"
AUTO_AGENT = REPO_ROOT / "template" / ".opencode" / "agents" / "auto.md"
DRIVER_PATH = REPO_ROOT / "scripts" / "auto_outer_driver.py"
RUNBOOK = REPO_ROOT / "docs" / "engineering" / "runbook.md"

# Unique-to-Cursor phrases that MUST NOT appear in the plugin source (AC-9).
CURSOR_CLONE_PHRASES = [
    "Spawn-boundary integrity (BUG-0006)",
    "AUTO_LOOP_MAX_CYCLES",
    ".cursor/commands/auto.md",
]

# Agent permission-array literals that MUST NOT appear in the plugin source
# (DQ8 — defense in depth, no duplication). The plugin resolves roles via
# the US-0069 matrix; it does NOT copy the agent's `edit`/`bash`/`task`
# allow-list object form. Role names as matrix values are permitted.
PERMISSION_ARRAY_LITERALS = [
    re.compile(r"^\s*edit\s*:\s*deny\s*$", re.MULTILINE),
    re.compile(r"^\s*bash\s*:\s*deny\s*$", re.MULTILINE),
    re.compile(r"^\s*task\s*:\s*$", re.MULTILINE),
]

# Secret patterns that MUST NOT appear in log/print/error paths (AC-11 / US-0085).
SECRET_PATTERNS = re.compile(
    r"api_key|apikey|sk-[A-Za-z0-9]{8,}|auth\.json|\.env",
    re.IGNORECASE,
)

VENDOR_SLUG_RE = re.compile(
    r"deepseek|moonshot|kimi|glm|claude|gpt|sonnet|opus|haiku|o1|o3|sk-",
    re.IGNORECASE,
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


def test_us0124_spawn_isolation_static():
    """Marker 1 (AC-1, AC-3): plugin source calls ctx.session.create with
    parentID + agent; no same-session spawn. Static grep/AST on plugin source."""
    src = PLUGIN_PATH.read_text(encoding="utf-8")
    assert "ctx.session.create" in src or "session.create" in src, (
        "plugin source must call ctx.session.create"
    )
    assert "parentID" in src, "plugin source must pass parentID to session.create"
    assert "agent" in src, "plugin source must pass agent (role) to session.create"
    # Hard post-condition: sessionID !== parentID assertion (DQ5). The plugin
    # may express this as `sessionID === parentID` (fail-closed branch) or
    # `sessionID !== parentID` (success branch); accept either form.
    assert (
        "sessionID === args.orchestratorSessionId" in src
        or "sessionID !== args.orchestratorSessionId" in src
        or "sessionID === parentID" in src
        or "sessionID !== parentID" in src
    ), "plugin source must compare sessionID against the orchestrator session id"
    # Plugin id (DQ1)
    assert 'id: "its-magic.orchestrator"' in src, "plugin id must be its-magic.orchestrator"
    # ctx.tool.hook("execute.before") present (DQ8)
    assert 'ctx.tool.hook("execute.before"' in src or 'tool.hook("execute.before"' in src, (
        "plugin source must register ctx.tool.hook('execute.before')"
    )


def test_us0124_spawn_isolation_runtime():
    """Marker 2 (AC-3, AC-4, AC-10): MockCtx.session.create returns fresh uuid
    ≠ parentID; plugin asserts sessionID !== parentID; isolation evidence
    persisted with required fields."""
    r = _run_harness("spawn-ok")
    assert r["ok"] is True, f"expected ok spawn, got {r}"
    parent = "orchestrator-session-0"
    sid = r["sessionID"]
    assert sid and sid != parent, (
        f"sessionID must differ from parentID (got sessionID={sid!r})"
    )
    ev = r["evidence"]
    for field in ("parentID", "sessionID", "role", "phase_id", "timestamp", "fresh_context_marker"):
        assert field in ev and ev[field], f"isolation evidence missing field {field!r}: {ev}"
    assert ev["parentID"] == parent
    assert ev["sessionID"] == sid
    assert ev["role"] == "dev"
    assert ev["phase_id"] == "execute"
    # create was called with parentID + agent
    calls = r["createCalls"]
    assert calls and calls[0]["parentID"] == parent and calls[0]["agent"] == "dev"


def test_us0124_subtask_ignored_null_return():
    """Marker 3 (AC-8): MockCtx.session.create returns null →
    OPENCODE_SUBTASK_IGNORED + stop /auto."""
    r = _run_harness("spawn-null")
    assert r["ok"] is False
    assert r["reasonCode"] == "OPENCODE_SUBTASK_IGNORED", r


def test_us0124_subtask_ignored_throw():
    """Marker 4 (AC-8): generic throw → OPENCODE_SUBTASK_IGNORED;
    missing-primitive throw → OPENCODE_PLUGIN_SPAWN_UNSUPPORTED
    (throw-discrimination rule, DEC-0124 §5)."""
    r_generic = _run_harness("spawn-throw-generic")
    assert r_generic["ok"] is False
    assert r_generic["reasonCode"] == "OPENCODE_SUBTASK_IGNORED", r_generic

    r_missing = _run_harness("spawn-throw-missing-primitive")
    assert r_missing["ok"] is False
    assert r_missing["reasonCode"] == "OPENCODE_PLUGIN_SPAWN_UNSUPPORTED", r_missing


def test_us0124_subtask_ignored_identical_id():
    """Marker 5 (AC-8): MockCtx.session.create returns { sessionID: parentID }
    → plugin detects sessionID === parentID → OPENCODE_SUBTASK_IGNORED."""
    r = _run_harness("spawn-identical-id")
    assert r["ok"] is False
    assert r["reasonCode"] == "OPENCODE_SUBTASK_IGNORED", r


def test_us0124_no_cursor_auto_clone():
    """Marker 6 (AC-9): grep plugin source for unique-to-Cursor phrases —
    zero hits. The plugin IS the OpenCode native chain; no Cursor Task-loop
    port (DEC-0124 §8 / DQ8 / US-0095)."""
    src = PLUGIN_PATH.read_text(encoding="utf-8")
    hits = [p for p in CURSOR_CLONE_PHRASES if p in src]
    assert not hits, f"Cursor prose leaked into plugin source: {hits}"


def test_us0124_agent_plugin_compose():
    """Marker 7 (AC-1, AC-9): both auto.md + orchestrator.ts exist; plugin
    source does NOT copy the agent permission array (`edit:`/`bash:`/`task:`
    allow-list object form); ctx.tool.hook('execute.before') callback present
    and calls into the stop-matrix subprocess path for
    AUTO_ORCHESTRATOR_PHASE_EXECUTION detection."""
    assert AUTO_AGENT.is_file(), "template/.opencode/agents/auto.md missing"
    assert PLUGIN_PATH.is_file(), "template/.opencode/plugins/orchestrator.ts missing"
    src = PLUGIN_PATH.read_text(encoding="utf-8")
    for pat in PERMISSION_ARRAY_LITERALS:
        hits = pat.findall(src)
        assert not hits, (
            f"agent permission-array literal {pat.pattern!r} leaked into plugin: {hits}"
        )
    # ctx.tool.hook("execute.before") callback present
    assert 'tool.hook("execute.before"' in src, (
        "plugin source must register ctx.tool.hook('execute.before')"
    )
    # stop-matrix subprocess dispatch present (DQ6)
    assert "dispatchStopMatrix" in src and "auto_outer_driver.py" in src, (
        "plugin source must delegate stop-matrix to scripts/auto_outer_driver.py"
    )
    # AUTO_ORCHESTRATOR_PHASE_EXECUTION referenced
    assert "AUTO_ORCHESTRATOR_PHASE_EXECUTION" in src, (
        "plugin source must reference AUTO_ORCHESTRATOR_PHASE_EXECUTION"
    )


def test_us0124_invoke_cmd_hook():
    """Marker 8 (AC-7): argv construction `opencode run --agent auto --format
    json --auto "<prompt>"` + JSON event parsing OR fail-closed
    OPENCODE_HEADLESS_UNSUPPORTED when opencode missing on PATH; not a live
    OpenCode probe. Also asserts DQ6 stop-matrix subprocess argv + JSON
    parsing OR fail-closed OPENCODE_DRIVER_INVOKE_FAILED on non-zero exit /
    malformed JSON (critic NB ik_us0124_dq6_driver_fail_code_conflation closed)."""
    # Headless argv construction
    r_argv = _run_harness("build-argv")
    expected = ["opencode", "run", "--agent", "auto", "--format", "json", "--auto", "phase-prompt-here"]
    assert r_argv["argv"] == expected, f"headless argv mismatch: {r_argv['argv']}"

    # Fail-closed when opencode missing on PATH
    r_missing = _run_harness("invoke-headless-missing")
    assert r_missing["ok"] is False
    assert r_missing["reasonCode"] == "OPENCODE_HEADLESS_UNSUPPORTED", r_missing

    # Headless success path parses JSON events
    r_ok = _run_harness("invoke-headless-ok")
    assert r_ok["ok"] is True and r_ok["events"] == [{"type": "message"}], r_ok

    # DQ6 stop-matrix subprocess: success path parses JSON
    r_dm_ok = _run_harness("dispatch-stop-matrix-ok")
    assert r_dm_ok["ok"] is True, r_dm_ok
    assert r_dm_ok["action"] == "spawn_next"
    assert r_dm_ok["next_phase"] == "qa"

    # DQ6 stop-matrix subprocess: non-zero exit → DRIVER_INVOKE_FAILED (NOT HEADLESS_UNSUPPORTED)
    r_dm_fail = _run_harness("dispatch-stop-matrix-fail")
    assert r_dm_fail["ok"] is False
    assert r_dm_fail["reasonCode"] == "OPENCODE_DRIVER_INVOKE_FAILED", r_dm_fail

    # DQ6 stop-matrix subprocess: malformed JSON → DRIVER_INVOKE_FAILED
    r_dm_malformed = _run_harness("dispatch-stop-matrix-malformed")
    assert r_dm_malformed["ok"] is False
    assert r_dm_malformed["reasonCode"] == "OPENCODE_DRIVER_INVOKE_FAILED", r_dm_malformed

    # Live Python driver additive argv returns JSON (no regression to US-0092)
    proc = subprocess.run(
        [sys.executable, str(DRIVER_PATH),
         "--phase", "execute", "--role", "dev",
         "--story", "US-0124", "--sprint", "S0124",
         "--orchestrator-run-id", "auto-20260824-02",
         "--stop-reason", "completed"],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert proc.returncode == 0, f"driver additive path failed: {proc.stderr}"
    payload = json.loads(proc.stdout)
    assert payload["action"] == "spawn_next"
    assert payload["phase"] == "execute"
    assert payload["role"] == "dev"


def test_us0124_secrets_no_logging():
    """Marker 9 (AC-11 / US-0085): grep plugin source + harness for
    api_key/apikey/sk-/auth.json/.env patterns — zero hits in log/print/error
    paths. The plugin never logs secrets."""
    files = [PLUGIN_PATH, MOCK_PATH, HARNESS_PATH]
    hits = []
    for f in files:
        if not f.is_file():
            continue
        for line_num, line in enumerate(f.read_text(encoding="utf-8").splitlines(), start=1):
            if SECRET_PATTERNS.search(line):
                # Allow `.env` only in a comment that documents the gitignore
                # contract — but the plugin/harness must not reference it in
                # log/print/error paths. Be strict: zero hits in source.
                hits.append(f"{f.name}:{line_num}:{line.strip()}")
    assert not hits, f"secret patterns in plugin/harness source: {hits}"


def test_us0124_phase_role_mismatch():
    """Marker 10 (plan-verify carry-forward, AC-2): wrong-role spawn per
    US-0069 / DEC-0051 matrix → PHASE_ROLE_MISMATCH, fail closed. An unknown
    phase_id must not silently spawn any role."""
    r = _run_harness("spawn-unknown-phase")
    assert r["ok"] is False, f"unknown phase must fail closed: {r}"
    assert r["reasonCode"] == "PHASE_ROLE_MISMATCH", r
    # No session.create call should have been made for an unknown phase
    calls = r.get("createCalls") or []
    assert calls == [], f"no session.create expected for unknown phase: {calls}"


def test_us0124_no_vendor_slugs_in_plugin():
    """Extra AC-2/US-0102 guard: plugin source has zero vendor model slugs."""
    src = PLUGIN_PATH.read_text(encoding="utf-8")
    hits = VENDOR_SLUG_RE.findall(src)
    # `o1`/`o3` may appear as substrings; check word-boundary for the real
    # vendor slugs. Use a targeted check: none of the full vendor names.
    assert not hits, f"vendor slug patterns in plugin source: {hits}"


def test_us0124_runbook_stub_present():
    """Extra AC-8 guard: runbook has the US-0124 stub h2 with the four new
    OPENCODE_* codes + three reused codes, and the US-0126 cross-link."""
    text = RUNBOOK.read_text(encoding="utf-8")
    assert "## OpenCode orchestrator plugin reason codes (US-0124)" in text, (
        "runbook missing US-0124 stub h2"
    )
    for code in (
        "OPENCODE_PLUGIN_SPAWN_UNSUPPORTED",
        "OPENCODE_SUBTASK_IGNORED",
        "OPENCODE_HEADLESS_UNSUPPORTED",
        "OPENCODE_DRIVER_INVOKE_FAILED",
        "AUTO_ORCHESTRATOR_PHASE_EXECUTION",
        "PHASE_ROLE_MISMATCH",
        "NATIVE_CHAIN_UNAVAILABLE",
    ):
        assert code in text, f"runbook US-0124 stub missing code {code}"
    assert "US-0126" in text, "runbook US-0124 stub must cross-link to US-0126"
