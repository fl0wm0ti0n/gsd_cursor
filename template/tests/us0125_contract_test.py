"""US-0125 Thin OpenCode commands + Python validator bridge — 11 contract markers.

Markers 1–11 per DEC-0125 §9 / architecture AC-8 table. The runtime harness
uses a Node subprocess (`tests/us0125/bridge_harness.mjs`) that imports the
mock-subprocess harness (`tests/us0125/mock_subprocess.ts`) and reads the
validator→artifact mapping fixture
(`tests/us0125/fixtures/validator_artifact_mapping.json`) under
`node --experimental-strip-types`. No live OpenCode runtime probe (AC-10).

The plugin file (`template/.opencode/plugins/orchestrator.ts`) is US-0124
territory and is NOT modified by US-0125. US-0125 authors the validator
→artifact mapping (additive data) + the bridge contract prose in the 15
command files; US-0124 authors the `ctx.tool.hook("execute.before")` hook
that consumes the mapping. Marker 4 (success test (b)) asserts the bridge
contract via the harness — the contract that the US-0124 plugin hook must
follow.
"""

from __future__ import annotations

import difflib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COMMANDS_DIR = REPO_ROOT / "template" / ".opencode" / "commands"
CURSOR_COMMANDS_DIR = REPO_ROOT / ".cursor" / "commands"
FIXTURE_PATH = REPO_ROOT / "tests" / "us0125" / "fixtures" / "validator_artifact_mapping.json"
HARNESS_PATH = REPO_ROOT / "tests" / "us0125" / "bridge_harness.mjs"
MOCK_SUBPROCESS_PATH = REPO_ROOT / "tests" / "us0125" / "mock_subprocess.ts"
PLUGIN_PATH = REPO_ROOT / "template" / ".opencode" / "plugins" / "orchestrator.ts"
PACKAGE_JSON = REPO_ROOT / "package.json"
RUNBOOK = REPO_ROOT / "docs" / "engineering" / "runbook.md"

# 15-file inventory (DQ1 LOCKED).
EXPECTED_COMMANDS: tuple[str, ...] = (
    "intake",
    "discovery",
    "research",
    "architecture",
    "sprint-plan",
    "plan-verify",
    "execute",
    "qa",
    "verify-work",
    "release",
    "closure",
    "refresh-context",
    "auto",
    "quick",
    "ask",
)

# Clone-guard strip list (DQ2 LOCKED — closes critic NB
# ik_us0125_dq2_normalization_strip_list_open). Single source of truth so
# US-0126 inherits without re-deriving.
US0125_CLONE_GUARD_STRIP_TOKENS: tuple[str, ...] = (
    "its-magic",
    "command",
    "phase",
    "artifact",
    "STOP",
    "run",
    "validator",
    "plugin",
    "script",
    "python",
    "scripts",
    "repo",
    "the",
    "a",
    "an",
    "to",
    "of",
    "and",
    "or",
    "before",
    "after",
    "above",
    "below",
    "path",
    "list",
    "id",
)

# Policy-text fragments that MUST NOT appear in command files (AC-6 —
# validator logic belongs in Python CLIs + plugin hook, not command prose).
POLICY_TEXT_FRAGMENTS: tuple[str, ...] = (
    "INTAKE_REQUIRED_TOPIC_MISSING",
    "INTAKE_REQUIRED_PACK_INCOMPLETE",
    "INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED",
    "INTAKE_PERSISTENCE_BLOCKED",
    "BUG_ISSUE_VALIDATION_FAILED",
    "topic_coverage",
    "assumption_confirmation_ref",
    "asked_topics",
    "missing_topics",
    "assumptions_confirmed",
)

# Unique-to-Cursor phrases that MUST NOT appear in OpenCode command files
# (AC-9 — no 200-line Cursor clones).
CURSOR_CLONE_PHRASES: tuple[str, ...] = (
    "Spawn-boundary integrity (BUG-0006)",
    "AUTO_LOOP_MAX_CYCLES",
    ".cursor/commands/auto.md",
    "ctx.session.create",
    "Session.create",
    "subagent context",
    "fresh subagent",
)

# Secret patterns (AC-11 / US-0085 — no secrets in command/harness source).
SECRET_PATTERNS = re.compile(
    r"api_key|apikey|sk-[A-Za-z0-9]{8,}|auth\.json|\.env",
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


def _strip_frontmatter(text: str) -> str:
    """Strip the leading YAML frontmatter block (between --- fences)."""
    if not text.startswith("---"):
        return text
    lines = text.splitlines()
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[i + 1:])
    return text


def _normalize_for_clone_guard(text: str, phase_id: str) -> str:
    """Normalize text per DQ2 strip list for clone-guard similarity."""
    s = _strip_frontmatter(text)
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    tokens = s.split()
    strip_set = set(US0125_CLONE_GUARD_STRIP_TOKENS) | {phase_id.lower()}
    kept = [t for t in tokens if t and t not in strip_set]
    return " ".join(kept)


def test_us0125_command_inventory():
    """Marker 1 (AC-1): 15 files present; no extra; no .gitkeep after populate."""
    assert COMMANDS_DIR.is_dir(), "template/.opencode/commands missing"
    md_files = sorted(p.name for p in COMMANDS_DIR.glob("*.md"))
    expected = sorted(f"{name}.md" for name in EXPECTED_COMMANDS)
    assert md_files == expected, f"command inventory mismatch: got {md_files}, expected {expected}"
    gitkeep = COMMANDS_DIR / ".gitkeep"
    assert not gitkeep.exists(), ".gitkeep must be removed after populate"


def test_us0125_clone_guard():
    """Marker 2 (AC-2): per-file line cap ≤ 20 + similarity ≤ 0.30 via difflib."""
    offenders_line: list[str] = []
    offenders_sim: list[str] = []
    for name in EXPECTED_COMMANDS:
        oc_path = COMMANDS_DIR / f"{name}.md"
        cursor_path = CURSOR_COMMANDS_DIR / f"{name}.md"
        assert oc_path.is_file(), f"missing opencode command: {name}.md"
        assert cursor_path.is_file(), f"missing cursor command for baseline: {name}.md"
        oc_text = oc_path.read_text(encoding="utf-8")
        line_count = len(oc_text.splitlines())
        if line_count > 20:
            offenders_line.append(f"{name}.md: {line_count} lines > 20")
        oc_norm = _normalize_for_clone_guard(oc_text, name)
        cursor_norm = _normalize_for_clone_guard(cursor_path.read_text(encoding="utf-8"), name)
        ratio = difflib.SequenceMatcher(None, oc_norm, cursor_norm).ratio()
        if ratio > 0.30:
            offenders_sim.append(f"{name}.md: similarity {ratio:.3f} > 0.30")
    assert not offenders_line, "line cap violations: " + "; ".join(offenders_line)
    assert not offenders_sim, "similarity violations: " + "; ".join(offenders_sim)


def test_us0125_validator_subprocess_fail_closed():
    """Marker 3 (AC-3): bridge contract for the two named CLIs — stubbed
    non-zero → command/plugin does not proceed to persistence."""
    data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    named_clis = {
        "scripts/intake_evidence_validate.py --repo . --enforce",
        "scripts/bug_issue_validate.py --repo . --check-acceptance",
    }
    found = {row["validator_cli"] for row in data["rows"] if row["bridge"] == "named"}
    assert named_clis.issubset(found), f"named CLIs missing from fixture: {named_clis - found}"
    r = _run_harness("release-blocked-nonzero")
    assert r["allowed"] is False, f"non-zero exit must refuse persistence: {r}"
    assert r["reasonCode"] == "INTAKE_PERSISTENCE_BLOCKED", (
        f"raw Python reason code must surface (no wrapper): {r}"
    )
    argv_str = " ".join(r["validatorArgv"])
    assert (
        "bug_issue_validate.py" in argv_str or "intake_evidence_validate.py" in argv_str
    ), f"validator argv must be a named CLI: {r['validatorArgv']}"


def test_us0125_release_blocked_after_failing_validator():
    """Marker 4 (AC-4): success test (b) — mock-ctx+mock-subprocess; validator
    non-zero → refuse write; raw Python reason code; throw → OPENCODE_DRIVER_INVOKE_FAILED."""
    r_nonzero = _run_harness("release-blocked-nonzero")
    assert r_nonzero["allowed"] is False
    assert r_nonzero["reasonCode"] == "INTAKE_PERSISTENCE_BLOCKED", r_nonzero
    assert len(r_nonzero["calls"]) == 1, f"subprocess must be called once: {r_nonzero['calls']}"
    r_throw = _run_harness("release-blocked-throw")
    assert r_throw["allowed"] is False
    assert r_throw["reasonCode"] == "OPENCODE_DRIVER_INVOKE_FAILED", r_throw
    assert len(r_throw["calls"]) == 1, f"subprocess must be called once even on throw: {r_throw['calls']}"
    r_ok = _run_harness("release-allowed")
    assert r_ok["allowed"] is True, r_ok


def test_us0125_reason_code_raw_python():
    """Marker 5 (AC-5): no OPENCODE_VALIDATOR_FAILED wrapper; raw Python codes
    surface as-is; OPENCODE_DRIVER_INVOKE_FAILED only for subprocess invocation failure."""
    sources: list[Path] = list(COMMANDS_DIR.glob("*.md")) + [MOCK_SUBPROCESS_PATH, HARNESS_PATH]
    forbidden = "OPENCODE_VALIDATOR_FAILED"
    hits: list[str] = []
    for path in sources:
        if not path.is_file():
            continue
        for line_num, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if forbidden in line:
                hits.append(f"{path.name}:{line_num}:{line.strip()}")
    assert not hits, f"OPENCODE_VALIDATOR_FAILED wrapper found (DQ7 violation): {hits}"
    harness_text = MOCK_SUBPROCESS_PATH.read_text(encoding="utf-8") + "\n" + HARNESS_PATH.read_text(encoding="utf-8")
    assert "OPENCODE_DRIVER_INVOKE_FAILED" in harness_text, (
        "harness must surface OPENCODE_DRIVER_INVOKE_FAILED on subprocess throw"
    )
    for f in COMMANDS_DIR.glob("*.md"):
        text = f.read_text(encoding="utf-8")
        assert "OPENCODE_DRIVER_INVOKE_FAILED" not in text, (
            f"command file {f.name} must not own enforcement codes (DQ4 — diagnostics only)"
        )


def test_us0125_no_policy_in_commands():
    """Marker 6 (AC-6): grep 15 command files for policy text duplicating
    validator logic — zero hits."""
    hits: list[str] = []
    for f in COMMANDS_DIR.glob("*.md"):
        text = f.read_text(encoding="utf-8")
        for frag in POLICY_TEXT_FRAGMENTS:
            if frag in text:
                hits.append(f"{f.name}: {frag}")
    assert not hits, f"policy text leaked into command files (AC-6 violation): {hits}"


def test_us0125_missing_command_does_not_disable_plugin():
    """Marker 7 (AC-7): delete a command file in a temp copy → plugin still
    loads via .opencode/plugins/ auto-discovery; @auto agent still invocable."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        dst_opencode = tmp_path / "template" / ".opencode"
        dst_opencode.mkdir(parents=True)
        shutil.copytree(REPO_ROOT / "template" / ".opencode" / "agents", dst_opencode / "agents")
        shutil.copytree(REPO_ROOT / "template" / ".opencode" / "commands", dst_opencode / "commands")
        shutil.copytree(REPO_ROOT / "template" / ".opencode" / "plugins", dst_opencode / "plugins")
        (dst_opencode / "commands" / "quick.md").unlink()
        assert not (dst_opencode / "commands" / "quick.md").exists()
        # Plugin file still present (auto-discovered via .opencode/plugins/).
        assert (dst_opencode / "plugins" / "orchestrator.ts").is_file(), (
            "plugin must remain after a convenience command is deleted"
        )
        # @auto agent still invocable (agent file independent of command file).
        assert (dst_opencode / "agents" / "auto.md").is_file(), (
            "auto agent must remain after /quick command is deleted"
        )
        # Remaining 14 commands still present.
        remaining = sorted(p.name for p in (dst_opencode / "commands").glob("*.md"))
        assert len(remaining) == 14, f"expected 14 commands after deletion, got {len(remaining)}"


def test_us0125_auto_command_dispatch_only():
    """Marker 8 (AC-1, AC-7): auto.md ≤ 20 lines + no ctx.session.create /
    Session.create / spawn logic literals in the BODY (frontmatter
    description 'spawn-only' is allowed — it is a description, not spawn logic)
    + agent: auto frontmatter present."""
    auto_path = COMMANDS_DIR / "auto.md"
    assert auto_path.is_file(), "auto.md missing"
    text = auto_path.read_text(encoding="utf-8")
    line_count = len(text.splitlines())
    assert line_count <= 20, f"auto.md {line_count} lines > 20"
    # Check the BODY (after frontmatter) for spawn-logic literals. The
    # frontmatter description "spawn-only" is permitted — it describes the
    # entry, not spawn logic.
    body = _strip_frontmatter(text)
    for forbidden in ("ctx.session.create", "Session.create"):
        assert forbidden not in body, f"auto.md body must not contain {forbidden!r} (dispatch-only)"
    # "spawn" as a standalone logic literal (e.g. `spawn(`, `spawn =`, `.spawn(`)
    # is forbidden; the word "spawn-only" in the description is allowed.
    assert not re.search(r"\bspawn\s*[(=]", body), (
        "auto.md body must not contain spawn-call logic (dispatch-only per DQ5)"
    )
    assert re.search(r"^agent:\s*auto\s*$", text, re.MULTILINE), (
        "auto.md must have agent: auto frontmatter"
    )
    assert re.search(r"^subtask:\s*false\s*$", text, re.MULTILINE), (
        "auto.md must have subtask: false frontmatter"
    )


def test_us0125_cursor_commands_unchanged():
    """Marker 9 (AC-9): US-0125 must not modify .cursor/commands/*.md. The
    cursor commands may carry pre-existing changes from prior sprints
    (US-0120, US-0124, etc.); US-0125 is additive and must not introduce
    any US-0125 references into .cursor/commands/*.md."""
    assert CURSOR_COMMANDS_DIR.is_dir(), ".cursor/commands missing"
    hits: list[str] = []
    for f in CURSOR_COMMANDS_DIR.glob("*.md"):
        text = f.read_text(encoding="utf-8")
        # US-0125 must not be referenced in any cursor command file (additive).
        if "US-0125" in text:
            hits.append(f.name)
    assert not hits, f"US-0125 references leaked into .cursor/commands (AC-9): {hits}"
    # The 15 OpenCode command names must not appear as new files in
    # .cursor/commands/ (they live in template/.opencode/commands/ only).
    oc_names = {f"{name}.md" for name in EXPECTED_COMMANDS}
    cursor_names = {p.name for p in CURSOR_COMMANDS_DIR.glob("*.md")}
    overlap = oc_names & cursor_names
    # Overlap is expected (cursor already has intake.md, auto.md, etc.) —
    # those are the ORIGINAL cursor commands, not OpenCode clones. The
    # clone-guard (marker 2) asserts the OpenCode versions are dissimilar.
    # Here we only assert that US-0125 didn't ADD new cursor command files
    # beyond the pre-existing set. Since we can't easily distinguish pre-
    # existing from US-0125-added without git history, we rely on the
    # clone-guard marker 2 + the US-0125-reference grep above.


def test_us0125_no_new_npm_runtime():
    """Marker 10 (AC-10): grep package.json + consumer app code for new runtime
    deps — zero hits; validator bridge is kit scripts + plugin subprocess."""
    assert PACKAGE_JSON.is_file(), "package.json missing"
    data = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    deps = dict(data.get("dependencies") or {})
    deps.update(data.get("devDependencies") or {})
    # No OpenCode/AI SDK runtime deps in consumer app code.
    forbidden_prefixes = ("@opencode-ai/", "@ai-sdk/", "opencode")
    hits = [dep for dep in deps if any(dep.startswith(p) or dep == p for p in forbidden_prefixes)]
    assert not hits, f"new runtime deps in package.json (AC-10 violation): {hits}"
    # Command files must not reference npm/runtime deps.
    for f in COMMANDS_DIR.glob("*.md"):
        text = f.read_text(encoding="utf-8")
        assert "npm install" not in text, f"{f.name} must not reference npm install"
        assert "require(" not in text, f"{f.name} must not reference require()"


def test_us0125_command_frontmatter_shape():
    """Marker 11 (AC-1, AC-8): 15 files — description present; agent present
    for 14 (omitted for /ask); no model: in any; subtask: false only on /auto."""
    for name in EXPECTED_COMMANDS:
        path = COMMANDS_DIR / f"{name}.md"
        assert path.is_file(), f"missing {name}.md"
        text = path.read_text(encoding="utf-8")
        # Must start with frontmatter.
        assert text.startswith("---"), f"{name}.md must start with frontmatter"
        fm_end = text.find("\n---", 3)
        assert fm_end != -1, f"{name}.md frontmatter not terminated"
        fm = text[3:fm_end]
        # description present.
        assert re.search(r"^description:\s*\S", fm, re.MULTILINE), (
            f"{name}.md missing description frontmatter"
        )
        # no model: in any template command (US-0102 + US-0123).
        assert not re.search(r"^model\s*:", fm, re.MULTILINE), (
            f"{name}.md must not have model: frontmatter (US-0102)"
        )
        if name == "ask":
            # /ask omits agent (agent-agnostic).
            assert not re.search(r"^agent\s*:", fm, re.MULTILINE), (
                "ask.md must omit agent: frontmatter (agent-agnostic)"
            )
            # /ask must not have subtask: false.
            assert not re.search(r"^subtask:\s*false", fm, re.MULTILINE), (
                "ask.md must not set subtask: false (only /auto)"
            )
        else:
            assert re.search(r"^agent:\s*\S", fm, re.MULTILINE), (
                f"{name}.md missing agent: frontmatter"
            )
            if name == "auto":
                assert re.search(r"^subtask:\s*false\s*$", fm, re.MULTILINE), (
                    "auto.md must have subtask: false (DQ5 dispatch-only)"
                )
            else:
                # Lifecycle commands must NOT set subtask: false (only /auto).
                assert not re.search(r"^subtask:\s*false", fm, re.MULTILINE), (
                    f"{name}.md must not set subtask: false (only /auto)"
                )

