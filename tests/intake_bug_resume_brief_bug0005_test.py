"""BUG-0005 / DEC-0069: resume_brief refresh at bug-intake boundary (R-0064 matrix)."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "intake_bug_resume_brief_refresh.py"
PY = sys.executable


def _minimal_open_bug_block(bug_id: str = "BUG-0999") -> str:
    return f"""## Bug issues (canonical)

### {bug_id} — Fixture
- Status: OPEN
- environment: fixture
- steps_to_reproduce: 1. run test
- expected: refresh ok
- actual: observed in fixture run
- evidence_refs: tests/intake_bug_resume_brief_bug0005_test.py
"""


class IntakeBugResumeBriefBug0005Test(unittest.TestCase):
    def test_script_self_test_passes(self) -> None:
        self.assertTrue(SCRIPT.is_file())
        r = subprocess.run(
            [PY, str(SCRIPT), "--self-test"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)

    def test_r0064_happy_path_discovery_seed_not_intake(self) -> None:
        """R-0064 #1: post-intake brief seeds discovery (no stale intake target)."""
        import tempfile

        backlog = _minimal_open_bug_block("BUG-0999")
        with tempfile.TemporaryDirectory() as td:
            tdir = Path(td)
            bp = tdir / "backlog.md"
            rp = tdir / "resume_brief.md"
            bp.write_text(backlog + "\n", encoding="utf-8")
            rp.write_text(
                "# Resume Brief\n\n## Latest orchestration pointer — stale\n\n- stale\n\n",
                encoding="utf-8",
            )
            r = subprocess.run(
                [
                    PY,
                    str(SCRIPT),
                    "--bug-id",
                    "BUG-0999",
                    "--backlog",
                    str(bp),
                    "--resume-brief",
                    str(rp),
                    "--intake-boundary-utc",
                    "2026-04-03T21:00:00Z",
                    "--orchestrator-run-id",
                    "auto-fixture-01",
                    "--intake-evidence",
                    "handoffs/intake_evidence/BUG-0999.json",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
            text = rp.read_text(encoding="utf-8")
            self.assertIn("resolved_start_phase=discovery", text)
            self.assertIn("next_scheduled_phase=discovery", text)
            self.assertIn("`discovery`", text)
            self.assertNotIn("resolved_start_phase=intake", text)
            self.assertIn("INTAKE_BUG_RESUME_BRIEF_REFRESH_OK", r.stdout)

    def test_r0064_missing_brief_creates_file(self) -> None:
        """R-0064 #2: absent resume_brief — writer creates parseable handoff (orchestrator may use state if still absent)."""
        import tempfile

        backlog = _minimal_open_bug_block("BUG-0998")
        with tempfile.TemporaryDirectory() as td:
            tdir = Path(td)
            bp = tdir / "backlog.md"
            rp = tdir / "resume_brief.md"
            bp.write_text(backlog, encoding="utf-8")
            r = subprocess.run(
                [
                    PY,
                    str(SCRIPT),
                    "--bug-id",
                    "BUG-0998",
                    "--backlog",
                    str(bp),
                    "--resume-brief",
                    str(rp),
                    "--intake-boundary-utc",
                    "2026-04-03T21:01:00Z",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
            self.assertTrue(rp.is_file())
            self.assertIn("bug_id=BUG-0998", rp.read_text(encoding="utf-8"))

    def test_r0064_start_from_precedence_documented_contract(self) -> None:
        """R-0064 #3: explicit start-from wins over brief — contract fields use resolution_source=resume_brief when no arg."""
        import tempfile

        backlog = _minimal_open_bug_block()
        with tempfile.TemporaryDirectory() as td:
            tdir = Path(td)
            bp = tdir / "backlog.md"
            rp = tdir / "resume_brief.md"
            bp.write_text(backlog, encoding="utf-8")
            r = subprocess.run(
                [
                    PY,
                    str(SCRIPT),
                    "--bug-id",
                    "BUG-0999",
                    "--backlog",
                    str(bp),
                    "--resume-brief",
                    str(rp),
                    "--intake-boundary-utc",
                    "2026-04-03T21:02:00Z",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            text = rp.read_text(encoding="utf-8")
            self.assertIn("resolution_source=resume_brief", text)
            self.assertIn("requested_start_from=(none)", text)

    def test_r0064_backlog_contradiction_done_fails(self) -> None:
        """R-0064 #4: DONE bug cannot seed OPEN discovery continuation."""
        import tempfile

        backlog = _minimal_open_bug_block("BUG-0997").replace("OPEN", "DONE")
        with tempfile.TemporaryDirectory() as td:
            tdir = Path(td)
            bp = tdir / "backlog.md"
            rp = tdir / "resume_brief.md"
            bp.write_text(backlog, encoding="utf-8")
            r = subprocess.run(
                [
                    PY,
                    str(SCRIPT),
                    "--bug-id",
                    "BUG-0997",
                    "--backlog",
                    str(bp),
                    "--resume-brief",
                    str(rp),
                    "--intake-boundary-utc",
                    "2026-04-03T21:03:00Z",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("INTAKE_RESUME_BRIEF_BACKLOG_CONTRADICTION", r.stderr)

    def test_r0064_portfolio_switch_new_bug_id_in_brief(self) -> None:
        """R-0064 #5: refresh targets the newly persisted OPEN bug, not a prior id in tail."""
        import tempfile

        # Canonical sort: lower BUG id first
        multi = (
            "## Bug issues (canonical)\n\n### BUG-0995 — B\n- Status: OPEN\n"
            "- environment: e\n- steps_to_reproduce: s\n- expected: x\n- actual: y\n"
            "- evidence_refs: t\n\n### BUG-0996 — A\n- Status: OPEN\n"
            "- environment: e\n- steps_to_reproduce: s\n- expected: x\n- actual: y\n"
            "- evidence_refs: t\n"
        )
        with tempfile.TemporaryDirectory() as td:
            tdir = Path(td)
            bp = tdir / "backlog.md"
            rp = tdir / "resume_brief.md"
            bp.write_text(multi, encoding="utf-8")
            rp.write_text(
                "# Resume Brief\n\n## Latest orchestration pointer — old\n\n- bug_id=BUG-0996\n\n",
                encoding="utf-8",
            )
            r = subprocess.run(
                [
                    PY,
                    str(SCRIPT),
                    "--bug-id",
                    "BUG-0995",
                    "--backlog",
                    str(bp),
                    "--resume-brief",
                    str(rp),
                    "--intake-boundary-utc",
                    "2026-04-03T21:04:00Z",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
            body = rp.read_text(encoding="utf-8")
            self.assertIn("bug_id=BUG-0995", body)
            # Latest pointer block should reference new bug in resolved_start_phase context
            idx = body.index("## Latest orchestration pointer")
            head = body[idx : idx + 800]
            self.assertIn("BUG-0995", head)
            self.assertNotIn("BUG-0996", head.split("## Checkpoint")[0])


if __name__ == "__main__":
    unittest.main()
