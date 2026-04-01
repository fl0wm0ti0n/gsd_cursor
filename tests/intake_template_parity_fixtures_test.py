"""Regression for DEC-0063 intake script active/template parity (BUG-0001 / S0060)."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]


class IntakeTemplateParityTest(unittest.TestCase):
    def test_parity_script_exits_ok_on_repo(self) -> None:
        script = _ROOT / "scripts" / "check_intake_template_parity.py"
        self.assertTrue(script.is_file())
        r = subprocess.run(
            [sys.executable, str(script), "--repo", str(_ROOT)],
            cwd=_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
