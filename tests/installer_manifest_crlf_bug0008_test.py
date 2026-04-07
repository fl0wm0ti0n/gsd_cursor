"""BUG-0008: CRLF in installer-owned-paths.manifest must not empty POSIX awk section parse."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_MANIFEST = ROOT / "template" / "docs" / "engineering" / "context" / "installer-owned-paths.manifest"

# Keep in sync with installer.sh `get_manifest_paths` awk body (after BUG-0008).
_AWK_MANIFEST_SECTION = r"""
BEGIN { in_section=0 }
{
  sub(/\r$/, "")
}
/^[[:space:]]*#/ { next }
/^[[:space:]]*$/ { next }
/^\[/ {
  in_section = ($0 == "[" s "]")
  next
}
{ if (in_section) print $0 }
"""


@unittest.skipUnless(shutil.which("awk"), "awk not on PATH")
@unittest.skipUnless(TEMPLATE_MANIFEST.is_file(), "template manifest missing")
class InstallerManifestCrlfBug0008Test(unittest.TestCase):
    def _awk_section(self, manifest: Path, section: str) -> str:
        run = subprocess.run(
            ["awk", "-v", f"s={section}", _AWK_MANIFEST_SECTION, str(manifest)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        self.assertEqual(0, run.returncode, run.stderr or run.stdout)
        return run.stdout

    def test_crlf_manifest_install_include_paths_nonempty(self) -> None:
        lf = TEMPLATE_MANIFEST.read_bytes()
        crlf = lf.replace(b"\n", b"\r\n")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".manifest") as tmp:
            tmp.write(crlf)
            path = Path(tmp.name)
        try:
            out = self._awk_section(path, "install_include_paths")
            self.assertIn(".cursor/commands", out)
            self.assertIn("docs", out)
            clean = self._awk_section(path, "clean_paths")
            self.assertIn(".cursor", clean)
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
