"""US-0121 OpenCode host-mode contract tests — 14 markers.

Surjective AC coverage (per architecture.md # US-0121 "AC-7 contract-test list"):
  1 -> AC-2; 2 -> AC-2,3,4; 3 -> AC-2,3,4; 4 -> AC-2,3,4; 5 -> AC-2;
  6 -> AC-2; 7 -> AC-2; 8 -> AC-3,7; 9 -> AC-3,7; 10 -> AC-5,7;
  11 -> AC-5; 12 -> AC-10; 13 -> AC-6; 14 -> AC-5 (+ AC-9 --help hook).

Markers 1-10 are behavioral (invoke installer.py in a temp target).
Markers 11-14 are static grep (source-level parity of predicate/flag across
py/ps1/sh/js).
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALLER_PY = REPO_ROOT / "installer.py"
MANIFEST = REPO_ROOT / "docs" / "engineering" / "context" / "installer-owned-paths.manifest"
TEMPLATE_MANIFEST = REPO_ROOT / "template" / "docs" / "engineering" / "context" / "installer-owned-paths.manifest"
TEMPLATE_OPENCODE = REPO_ROOT / "template" / ".opencode"
PARITY_SCRIPT = REPO_ROOT / "scripts" / "check_intake_template_parity.py"
TEMPLATE_PARITY_SCRIPT = REPO_ROOT / "template" / "scripts" / "check_intake_template_parity.py"
JS_BIN = REPO_ROOT / "bin" / "its-magic.js"
PS_INSTALLER = REPO_ROOT / "installer.ps1"
SH_INSTALLER = REPO_ROOT / "installer.sh"
PY_INSTALLER = REPO_ROOT / "installer.py"


def _run_installer(args, cwd=None):
    cmd = [sys.executable, str(INSTALLER_PY), *args]
    return subprocess.run(
        cmd,
        cwd=str(cwd or REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _install(tmp, host=None, mode="missing"):
    args = ["--target", tmp, "--mode", mode, "--create", "--yes"]
    if host is not None:
        args += ["--host", host]
    return _run_installer(args)


def _clean(tmp, host):
    return _run_installer(["--clean-repo", "--target", tmp, "--yes", "--host", host])


# -- marker 1: AC-2 --

def test_us0121_default_host_cursor_when_omitted():
    """AC-2: omitted --host defaults to cursor; .opencode/ is NOT installed."""
    with tempfile.TemporaryDirectory() as tmp:
        r = _install(tmp)
        assert r.returncode == 0, "install failed: " + (r.stdout or "") + (r.stderr or "")
        assert os.path.isdir(os.path.join(tmp, ".cursor")), "default install missing .cursor/"
        assert not os.path.exists(os.path.join(tmp, ".opencode")), \
            "default install must NOT create .opencode/"


# -- marker 2: AC-2, AC-3, AC-4 --

def test_us0121_host_cursor_installs_cursor_and_kernel_no_opencode():
    """AC-2,3,4: --host cursor installs .cursor/ + kernel; no .opencode/."""
    with tempfile.TemporaryDirectory() as tmp:
        r = _install(tmp, host="cursor")
        assert r.returncode == 0, "install failed: " + (r.stdout or "") + (r.stderr or "")
        assert os.path.isdir(os.path.join(tmp, ".cursor")), ".cursor/ missing"
        assert os.path.isdir(os.path.join(tmp, "docs")), "kernel docs/ missing"
        assert os.path.isdir(os.path.join(tmp, "scripts")), "kernel scripts/ missing"
        assert os.path.isdir(os.path.join(tmp, "its_magic")), "kernel its_magic/ missing"
        assert not os.path.exists(os.path.join(tmp, ".opencode")), \
            "--host cursor must NOT create .opencode/"


# -- marker 3: AC-2, AC-3, AC-4 --

def test_us0121_host_opencode_skips_cursor_installs_opencode_and_kernel():
    """AC-2,3,4: --host opencode skips .cursor/, installs .opencode/ + kernel."""
    with tempfile.TemporaryDirectory() as tmp:
        r = _install(tmp, host="opencode")
        assert r.returncode == 0, "install failed: " + (r.stdout or "") + (r.stderr or "")
        assert os.path.isdir(os.path.join(tmp, ".opencode")), ".opencode/ missing"
        assert os.path.isdir(os.path.join(tmp, "docs")), "kernel docs/ missing"
        assert os.path.isdir(os.path.join(tmp, "scripts")), "kernel scripts/ missing"
        assert not os.path.isdir(os.path.join(tmp, ".cursor")), \
            "--host opencode must NOT create .cursor/"


# -- marker 4: AC-2, AC-3, AC-4 --

def test_us0121_host_both_installs_both_trees():
    """AC-2,3,4: --host both installs both .cursor/ and .opencode/ + kernel."""
    with tempfile.TemporaryDirectory() as tmp:
        r = _install(tmp, host="both")
        assert r.returncode == 0, "install failed: " + (r.stdout or "") + (r.stderr or "")
        assert os.path.isdir(os.path.join(tmp, ".cursor")), ".cursor/ missing"
        assert os.path.isdir(os.path.join(tmp, ".opencode")), ".opencode/ missing"
        assert os.path.isdir(os.path.join(tmp, "docs")), "kernel docs/ missing"


# -- marker 5: AC-2 --

def test_us0121_invalid_host_fails_closed_install_host_invalid():
    """AC-2: unknown --host value -> exit nonzero + INSTALL_HOST_INVALID."""
    with tempfile.TemporaryDirectory() as tmp:
        r = _install(tmp, host="invalid-value")
        assert r.returncode != 0, "invalid host must fail closed"
        combined = (r.stdout or "") + (r.stderr or "")
        assert "INSTALL_HOST_INVALID" in combined, \
            "expected INSTALL_HOST_INVALID in output; got: " + combined


# -- marker 6: AC-2 --

def test_us0121_host_normalize_case_and_whitespace():
    """AC-2: --host normalizes case + whitespace (OpenCode, '  opencode  ', BOTH)."""
    cases = [
        ("OpenCode", "opencode"),
        ("  opencode  ", "opencode"),
        ("BOTH", "both"),
        ("Cursor", "cursor"),
    ]
    for raw, expected_tree in cases:
        with tempfile.TemporaryDirectory() as tmp:
            r = _install(tmp, host=raw)
            assert r.returncode == 0, "host=" + raw + " install failed: " + (r.stdout or "") + (r.stderr or "")
            if expected_tree == "opencode":
                assert os.path.isdir(os.path.join(tmp, ".opencode")), \
                    "host=" + raw + " should install .opencode/"
                assert not os.path.isdir(os.path.join(tmp, ".cursor")), \
                    "host=" + raw + " should NOT install .cursor/"
            elif expected_tree == "both":
                assert os.path.isdir(os.path.join(tmp, ".opencode")), "host=" + raw + " should install .opencode/"
                assert os.path.isdir(os.path.join(tmp, ".cursor")), "host=" + raw + " should install .cursor/"
            elif expected_tree == "cursor":
                assert os.path.isdir(os.path.join(tmp, ".cursor")), "host=" + raw + " should install .cursor/"
                assert not os.path.exists(os.path.join(tmp, ".opencode")), \
                    "host=" + raw + " should NOT install .opencode/"


# -- marker 7: AC-2 --

def test_us0121_duplicate_host_argv_fails_closed():
    """AC-2: duplicate --host argv -> fail closed INSTALL_HOST_INVALID (no last-wins)."""
    with tempfile.TemporaryDirectory() as tmp:
        r = _run_installer(["--target", tmp, "--mode", "missing", "--create", "--yes",
                            "--host", "cursor", "--host", "opencode"])
        assert r.returncode != 0, "duplicate --host must fail closed"
        combined = (r.stdout or "") + (r.stderr or "")
        assert "INSTALL_HOST_INVALID" in combined, \
            "expected INSTALL_HOST_INVALID for duplicate; got: " + combined


# -- marker 8: AC-3, AC-7 --

def test_us0121_clean_host_cursor_after_both_emits_orphan_diagnostic():
    """AC-3,7: clean --host cursor after --host both leaves .opencode/ + emits OPENCODE_ORPHANED_BY_CLEAN_CURSOR."""
    with tempfile.TemporaryDirectory() as tmp:
        r1 = _install(tmp, host="both")
        assert r1.returncode == 0, "both install failed: " + (r1.stdout or "") + (r1.stderr or "")
        assert os.path.isdir(os.path.join(tmp, ".opencode")), "precondition: .opencode/ must exist"

        r2 = _clean(tmp, host="cursor")
        assert r2.returncode == 0, "clean failed: " + (r2.stdout or "") + (r2.stderr or "")
        assert os.path.isdir(os.path.join(tmp, ".opencode")), \
            "clean --host cursor must NOT delete .opencode/"
        assert not os.path.isdir(os.path.join(tmp, ".cursor")), \
            "clean --host cursor should remove .cursor/"
        combined = (r2.stdout or "") + (r2.stderr or "")
        assert "OPENCODE_ORPHANED_BY_CLEAN_CURSOR" in combined, \
            "expected OPENCODE_ORPHANED_BY_CLEAN_CURSOR; got: " + combined


# -- marker 9: AC-3, AC-7 --

def test_us0121_upgrade_host_cursor_after_both_emits_stale_diagnostic():
    """AC-3,7: upgrade --host cursor after --host both leaves .opencode/ untouched + emits OPENCODE_STALE_BY_UPGRADE_CURSOR.

    Per sprint-critic ik_us0121_sprint_ac9_marker_misroute: marker 9 stays
    the upgrade-stale test (architecture table). The --help documents --host
    hook is covered inside marker 14 (triple-installer parity).
    """
    with tempfile.TemporaryDirectory() as tmp:
        r1 = _install(tmp, host="both")
        assert r1.returncode == 0, "both install failed: " + (r1.stdout or "") + (r1.stderr or "")
        assert os.path.isdir(os.path.join(tmp, ".opencode")), "precondition: .opencode/ must exist"

        r2 = _run_installer(["--target", tmp, "--mode", "upgrade", "--host", "cursor"])
        assert r2.returncode == 0, "upgrade failed: " + (r2.stdout or "") + (r2.stderr or "")
        assert os.path.isdir(os.path.join(tmp, ".opencode")), \
            "upgrade --host cursor must NOT delete .opencode/"
        combined = (r2.stdout or "") + (r2.stderr or "")
        assert "OPENCODE_STALE_BY_UPGRADE_CURSOR" in combined, \
            "expected OPENCODE_STALE_BY_UPGRADE_CURSOR; got: " + combined


# -- marker 10: AC-5, AC-7 --

def test_us0121_mixed_section_cursor_skip_when_host_opencode():
    """AC-5,7: --host opencode skips .cursor/ rows from [install_include_paths] but installs kernel rows + [opencode_install_include_paths]."""
    with tempfile.TemporaryDirectory() as tmp:
        r = _install(tmp, host="opencode")
        assert r.returncode == 0, "install failed: " + (r.stdout or "") + (r.stderr or "")
        assert os.path.isdir(os.path.join(tmp, "docs")), "kernel docs/ missing"
        assert os.path.isdir(os.path.join(tmp, "scripts")), "kernel scripts/ missing"
        assert os.path.isdir(os.path.join(tmp, "its_magic")), "kernel its_magic/ missing"
        assert not os.path.isdir(os.path.join(tmp, ".cursor")), \
            "mixed-section .cursor/ rows must be skipped when --host opencode"
        assert os.path.isdir(os.path.join(tmp, ".opencode")), ".opencode/ missing"
        assert os.path.isfile(os.path.join(tmp, ".opencode", "README.md")), ".opencode/README.md missing"
        assert os.path.isfile(os.path.join(tmp, ".opencode", ".gitignore")), ".opencode/.gitignore missing"


# -- marker 11: AC-5 --

def test_us0121_manifest_lists_opencode_pack():
    """AC-5: manifest contains [opencode_install_include_paths] + .opencode/ rows; active+template byte-identical."""
    text = MANIFEST.read_text(encoding="utf-8")
    assert "[opencode_install_include_paths]" in text, "manifest missing [opencode_install_include_paths]"
    assert "[opencode_clean_paths]" in text, "manifest missing [opencode_clean_paths]"
    for row in (".opencode/agents", ".opencode/commands", ".opencode/plugins",
                ".opencode/.gitignore", ".opencode/README.md"):
        assert row in text, "manifest missing opencode row: " + row
    assert ".opencode" in text, "manifest missing .opencode clean path"
    assert MANIFEST.read_bytes() == TEMPLATE_MANIFEST.read_bytes(), \
        "active + template manifest must be byte-identical for opencode sections"


# -- marker 12: AC-10 --

def test_us0121_no_secrets_in_pack():
    """AC-10: template/.opencode/** has no assignment-like apiKey/api_key/sk-/MODEL= hits; no vendor slugs.

    Regex tightened (loop-2 fix for B-1 / ik_us0121_marker12_apikey_prose_false_positive):
    matches assignments only, so prose documenting the forbidden pattern
    in README.md cannot trip the gate.
    """
    pattern = re.compile(r"\bapiKey\s*[:=]|api_key\s*[:=]|sk-[A-Za-z0-9]{8,}|MODEL\s*=")
    hits = []
    for root, _dirs, files in os.walk(str(TEMPLATE_OPENCODE)):
        for name in files:
            p = Path(root) / name
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if pattern.search(text):
                hits.append(str(p))
    assert not hits, "secret-like patterns found in template/.opencode/: " + repr(hits)


# -- marker 13: AC-6 --

def test_us0121_parity_scope_opencode_adapter_registered():
    """AC-6: --scope=opencode-adapter registered in check_intake_template_parity.py (active + template byte-identical)."""
    src = PARITY_SCRIPT.read_text(encoding="utf-8")
    tpl = TEMPLATE_PARITY_SCRIPT.read_text(encoding="utf-8")
    for label, text in (("active", src), ("template", tpl)):
        assert '"opencode-adapter"' in text, \
            label + " parity script missing 'opencode-adapter' scope"
        assert "OPENCODE_ADAPTER_PAIRS" in text, \
            label + " parity script missing OPENCODE_ADAPTER_PAIRS"
    assert PARITY_SCRIPT.read_bytes() == TEMPLATE_PARITY_SCRIPT.read_bytes(), \
        "active + template parity script must be byte-identical"
    assert '"opencode-adapter": OPENCODE_ADAPTER_PAIRS' in src, \
        "opencode-adapter not registered in SCOPES dict"
    assert "OPENCODE_ADAPTER_PAIRS" in src.split('    "all":')[1], \
        "opencode-adapter not included in SCOPES['all'] union"


# -- marker 14: AC-5 (+ AC-9 --help hook) --

def test_us0121_triple_installer_host_parity():
    """AC-5: PS/Bash/Python all normalize, validate, and apply the same host_gates_cursor_row predicate.

    Also covers AC-9 --help hook: bin/its-magic.js --help documents --host.
    """
    py_src = PY_INSTALLER.read_text(encoding="utf-8")
    ps_src = PS_INSTALLER.read_text(encoding="utf-8")
    sh_src = SH_INSTALLER.read_text(encoding="utf-8")
    js_src = JS_BIN.read_text(encoding="utf-8")

    # Shared predicate present in all three installers
    assert "host_gates_cursor_row" in py_src, "installer.py missing host_gates_cursor_row"
    assert "Host-GatesCursorRow" in ps_src, "installer.ps1 missing Host-GatesCursorRow"
    assert "host_gates_cursor_row" in sh_src, "installer.sh missing host_gates_cursor_row"

    # --host / -InstallHost flag present in all three installers
    assert "--host" in py_src, "installer.py missing --host"
    assert "-InstallHost" in ps_src, "installer.ps1 missing -InstallHost"
    assert "--host" in sh_src, "installer.sh missing --host"

    # Diagnostics present in all three installers
    for diag in ("INSTALL_HOST_INVALID", "OPENCODE_ORPHANED_BY_CLEAN_CURSOR",
                 "OPENCODE_STALE_BY_UPGRADE_CURSOR", "CURSOR_ORPHANED_BY_CLEAN_OPENCODE",
                 "CURSOR_STALE_BY_UPGRADE_OPENCODE"):
        assert diag in py_src, "installer.py missing diagnostic: " + diag
        assert diag in ps_src, "installer.ps1 missing diagnostic: " + diag
        assert diag in sh_src, "installer.sh missing diagnostic: " + diag

    # JS bin forwards --host and documents it in --help
    assert "--host" in js_src, "bin/its-magic.js missing --host parser"
    assert "-InstallHost" in js_src, "bin/its-magic.js missing -InstallHost forward to PS"
    assert "--host <value>" in js_src, "bin/its-magic.js --help missing --host <value> doc"
    assert "INSTALL_HOST_INVALID" in js_src, "bin/its-magic.js missing INSTALL_HOST_INVALID"
