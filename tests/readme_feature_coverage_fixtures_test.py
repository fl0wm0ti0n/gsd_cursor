"""US-0091 / DEC-0074 — README feature coverage fixtures + idempotence."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "readme_feature_coverage" / "minimal"
SCRIPT = ROOT / "scripts" / "validate_readme_feature_coverage.py"


class ReadmeFeatureCoverageFixturesTest(unittest.TestCase):
    def test_self_test_token(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--self-test"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("[README_FEATURE_COVERAGE_SELF_TEST_OK]", proc.stdout)

    def test_report_idempotent_on_fixture(self) -> None:
        cmd = [
            sys.executable,
            str(SCRIPT),
            "--repo",
            str(FIXTURE),
            "--no-template-parity",
            "--report",
        ]
        first = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        second = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, first.returncode)
        self.assertEqual(first.stdout, second.stdout)
        body = json.loads(first.stdout)
        self.assertEqual(body["coverage_missing"], [])
        self.assertEqual(body["report_schema_version"], 1)

    def test_readme_feature_coverage_architecture_linkage(self) -> None:
        arch = (ROOT / "docs" / "engineering" / "architecture.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("# US-0091", arch)
        section = arch[arch.find("# US-0091") :]
        for token in (
            "DEC-0074",
            "US-0030",
            "DEC-0059",
            "US-0017",
            "US-0071",
        ):
            with self.subTest(token=token):
                self.assertIn(token, section)


if __name__ == "__main__":
    unittest.main()
