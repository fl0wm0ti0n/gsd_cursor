"""BUG-0004 shell-startup compatibility regressions (DEC-0068)."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER_SH = ROOT / "installer.sh"
CLI = ROOT / "bin" / "its-magic.js"


def write_bootstrap_package_json(target: Path) -> None:
    payload = {
        "name": "tmp-bug0004-fixture",
        "version": "0.0.0",
        "scripts": {"test": "echo ok"},
    }
    (target / "package.json").write_text(json.dumps(payload), encoding="utf-8")


@unittest.skipUnless(INSTALLER_SH.is_file(), "installer.sh missing")
class InstallerShellBug0004Test(unittest.TestCase):
    def test_startup_does_not_use_bash_only_set_bundle(self) -> None:
        text = INSTALLER_SH.read_text(encoding="utf-8")
        # Guard against accidental reintroduction of non-POSIX startup bundles.
        forbidden_tokens = ("set -euo", "set -o pipefail", "set -eu -o pipefail")
        for token in forbidden_tokens:
            self.assertNotIn(token, text, f"forbidden startup token found: {token}")

    @unittest.skipUnless(shutil.which("sh"), "sh not available")
    def test_direct_sh_missing_mode_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            write_bootstrap_package_json(target)
            run = subprocess.run(
                ["sh", str(INSTALLER_SH), "--target", str(target), "--mode", "missing", "--create"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            self.assertEqual(0, run.returncode, run.stdout + run.stderr)

    @unittest.skipUnless(shutil.which("sh") and shutil.which("node"), "sh/node not available")
    def test_cli_unix_path_missing_mode_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            write_bootstrap_package_json(target)
            run = subprocess.run(
                ["node", str(CLI), "--target", str(target), "--mode", "missing", "--create"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            self.assertEqual(0, run.returncode, run.stdout + run.stderr)


if __name__ == "__main__":
    unittest.main()
