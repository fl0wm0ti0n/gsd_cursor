"""Regression: codebase map materializer (US-0082 / DEC-0065)."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "materialize_codebase_map.py"
TEMPLATE_SCRIPT = ROOT / "template" / "scripts" / "materialize_codebase_map.py"


def _run_script(repo: Path, *extra: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(repo), *extra],
        capture_output=True,
        text=True,
        check=False,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out


class CodebaseMapMaterializeTest(unittest.TestCase):
    def test_active_template_script_bytes_match(self) -> None:
        self.assertTrue(SCRIPT.is_file(), str(SCRIPT))
        self.assertTrue(TEMPLATE_SCRIPT.is_file(), str(TEMPLATE_SCRIPT))
        self.assertEqual(SCRIPT.read_bytes(), TEMPLATE_SCRIPT.read_bytes())

    def test_fresh_repo_creates_bootstrap_and_idempotent_rerun(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            c1, o1 = _run_script(repo, "--trigger", "architecture")
            self.assertEqual(c1, 0, o1)
            self.assertIn("[CODEBASE_MAP_OK] created", o1)
            mp = repo / "docs" / "engineering" / "codebase-map.md"
            self.assertTrue(mp.is_file())
            first = mp.read_text(encoding="utf-8")
            c2, o2 = _run_script(repo, "--trigger", "architecture")
            self.assertEqual(c2, 0, o2)
            self.assertIn("noop", o2)
            self.assertEqual(mp.read_text(encoding="utf-8"), first)

    def test_existing_custom_map_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            eng = repo / "docs" / "engineering"
            eng.mkdir(parents=True)
            custom = "# Codebase Map\n\n## Custom\n\nOperator-owned content.\n"
            mp = eng / "codebase-map.md"
            mp.write_text(custom, encoding="utf-8")
            c, o = _run_script(repo, "--trigger", "architecture")
            self.assertEqual(c, 0, o)
            self.assertIn("preserved_existing", o)
            self.assertEqual(mp.read_text(encoding="utf-8"), custom)

    def test_simulate_block_emits_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            c, o = _run_script(
                Path(tmp),
                "--trigger",
                "architecture",
                "--simulate-block",
                "fixture_denial",
            )
            self.assertEqual(c, 2)
            self.assertIn("[CODEBASE_MAP_BLOCKED:fixture_denial]", o)
            self.assertIn("Remediation:", o)

    def test_policy_skip_env_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["CODEBASE_MAP_LIFECYCLE_SKIP"] = "1"
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--repo", tmp, "--trigger", "architecture"],
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )
            out = (proc.stdout or "") + (proc.stderr or "")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("[CODEBASE_MAP_BLOCKED:policy_skip]", out)

    def test_check_present_missing_and_ok(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            c1, o1 = _run_script(repo, "--check-present")
            self.assertEqual(c1, 2)
            self.assertIn("[CODEBASE_MAP_MISSING]", o1)
            c2, o2 = _run_script(repo, "--trigger", "architecture")
            self.assertEqual(c2, 0, o2)
            c3, o3 = _run_script(repo, "--check-present")
            self.assertEqual(c3, 0, o3)
            self.assertIn("check_present", o3)


if __name__ == "__main__":
    unittest.main()
