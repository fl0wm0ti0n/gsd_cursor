"""US-0084 remote_config_summary.py exit-code fixtures (AC-10 / H3–H5)."""

from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "remote_config_summary.py"
FIX = ROOT / "tests" / "fixtures"


def _run(env: dict[str, str], extra_args: list[str] | None = None) -> subprocess.CompletedProcess[str]:
    merged = {**os.environ, **env}
    cmd = ["python", str(SCRIPT)]
    if extra_args:
        cmd.extend(extra_args)
    return subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=merged,
        check=False,
    )


@unittest.skipUnless(SCRIPT.is_file(), "remote_config_summary.py missing")
class RemoteConfigSummaryTest(unittest.TestCase):
    def test_remote_execution_zero_skips_with_exit_zero(self) -> None:
        r = _run({"REMOTE_EXECUTION": "0"})
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertEqual("", r.stdout.strip())

    def test_fixture_valid_exits_zero(self) -> None:
        r = _run(
            {"REMOTE_EXECUTION": "1"},
            ["--config", str(FIX / "remote_config_valid.json")],
        )
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertIn("defaultTarget=local-docker", r.stdout)
        self.assertIn("tokenEnv=REMOTE_DOCKER_TOKEN", r.stdout)

    def test_fixture_invalid_json_exits_three(self) -> None:
        r = _run(
            {"REMOTE_EXECUTION": "1"},
            ["--config", str(FIX / "remote_config_invalid.json")],
        )
        self.assertEqual(3, r.returncode, r.stderr)

    def test_fixture_schema_bad_exits_four(self) -> None:
        r = _run(
            {"REMOTE_EXECUTION": "1"},
            ["--config", str(FIX / "remote_config_schema_bad.json")],
        )
        self.assertEqual(4, r.returncode, r.stderr)


if __name__ == "__main__":
    unittest.main()
