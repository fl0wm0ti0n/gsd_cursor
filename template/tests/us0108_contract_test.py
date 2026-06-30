"""US-0108: Eight contract tests for Parallel Instance Arbitrage.

DEC-0108 §10: scratchpad keys, worktree isolation, selection predicate,
merge policy, resource guard, execute steps 25-28, backward compat, parity scope.

Default-off: SOVEREIGN_PARALLEL_DEV=0 → zero overhead.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_arbiter():
    root = _repo_root()
    scripts_dir = str(root / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import parallel_dev_arbiter as mod  # noqa: E402
    return mod


def _enabled_scratchpad(scratchpad_path: Path) -> None:
    """Write scratchpad with US-0108 enabled."""
    scratchpad_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# US-0108 parallel dev enabled\n",
        "SOVEREIGN_PARALLEL_DEV=1\n",
        "AUTO_SOVEREIGN_PARALLEL_N=3\n",
        "AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL=6\n",
        "AUTO_SOVEREIGN_MERGE_RESOLVE=first_pass_wins\n",
        "AUTO_SOVEREIGN_WORKTREE_KEEP=0\n",
        "AUTO_SOVEREIGN_PARALLEL_QA=0\n",
        "AUTO_SOVEREIGN_PARALLEL_QA_ARBITER=critic_first_pass\n",
        "AUTO_SOVEREIGN_PARALLEL_ANTI_SLOP_THRESHOLD=6\n",
        "AUTO_SOVEREIGN_PARALLEL_REWORK_MAX=2\n",
        "AUTO_SOVEREIGN_PARALLEL_MERGE_TIMEOUT_SEC=60\n",
    ]
    scratchpad_path.write_text("".join(lines), encoding="utf-8")


class TestUS0108ScratchpadKeys(unittest.TestCase):
    """test_us0108_scratchpad_keys_literals (AC-1)."""

    def test_scratchpad_key_literals(self) -> None:
        mod = _load_arbiter()
        required_keys = {
            "SOVEREIGN_PARALLEL_DEV",
            "AUTO_SOVEREIGN_PARALLEL_N",
            "AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL",
            "AUTO_SOVEREIGN_MERGE_RESOLVE",
            "AUTO_SOVEREIGN_WORKTREE_KEEP",
            "AUTO_SOVEREIGN_PARALLEL_QA",
            "AUTO_SOVEREIGN_PARALLEL_QA_ARBITER",
            "AUTO_SOVEREIGN_PARALLEL_ANTI_SLOP_THRESHOLD",
            "AUTO_SOVEREIGN_PARALLEL_REWORK_MAX",
            "AUTO_SOVEREIGN_PARALLEL_MERGE_TIMEOUT_SEC",
        }
        for key in required_keys:
            self.assertIn(key, mod.SCRATCHPAD_KEY_DEFAULTS,
                          f"{key} missing from SCRATCHPAD_KEY_DEFAULTS")
        self.assertEqual(mod.SCRATCHPAD_KEY_DEFAULTS["SOVEREIGN_PARALLEL_DEV"], "0")
        self.assertEqual(mod.SCRATCHPAD_KEY_DEFAULTS["AUTO_SOVEREIGN_PARALLEL_N"], "3")
        self.assertEqual(mod.SCRATCHPAD_KEY_DEFAULTS["AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL"], "6")


class TestUS0108WorktreeIsolation(unittest.TestCase):
    """test_us0108_worktree_isolation (AC-2)."""

    def test_worktree_creation_pattern(self) -> None:
        mod = _load_arbiter()
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / ".git").mkdir()
            wt = mod.create_worktree("US-0108", 0, "main", repo_root)
            self.assertEqual(wt.instance_id, "US-0108-inst0")
            self.assertEqual(wt.branch, "us0108-US-0108-0")
            expected_path = repo_root / ".git" / "worktrees" / "us0108-US-0108-0"
            self.assertEqual(wt.path, str(expected_path))


class TestUS0108SelectionDeterminism(unittest.TestCase):
    """test_us0108_selection_determinism (AC-3)."""

    def test_selection_logic(self) -> None:
        mod = _load_arbiter()
        results = [
            {"qa_verdict": "pass", "anti_slop_score": 5, "proof_issued_at": "2026-06-29T22:00:00Z", "instance_id": "A"},
            {"qa_verdict": "pass", "anti_slop_score": 8, "proof_issued_at": "2026-06-29T22:01:00Z", "instance_id": "B"},
            {"qa_verdict": "fail", "anti_slop_score": 10, "proof_issued_at": "2026-06-29T22:00:30Z", "instance_id": "C"},
        ]
        winner = mod.select_winner(results)
        self.assertIsNotNone(winner)
        self.assertEqual(winner["instance_id"], "B")  # highest anti_slop among passing

    def test_tie_break_earliest(self) -> None:
        mod = _load_arbiter()
        results = [
            {"qa_verdict": "pass", "anti_slop_score": 7, "proof_issued_at": "2026-06-29T22:05:00Z", "instance_id": "X"},
            {"qa_verdict": "pass", "anti_slop_score": 7, "proof_issued_at": "2026-06-29T22:01:00Z", "instance_id": "Y"},
        ]
        winner = mod.select_winner(results)
        self.assertIsNotNone(winner)
        self.assertEqual(winner["instance_id"], "Y")  # earliest proof_issued_at


class TestUS0108MergeAndPickSchema(unittest.TestCase):
    """test_us0108_merge_and_pick_schema (AC-4)."""

    def test_pick_record_schema(self) -> None:
        mod = _load_arbiter()
        with tempfile.TemporaryDirectory() as td:
            pick_path = Path(td) / "pick.json"
            rec = mod.build_pick_record(
                story_id="US-0108",
                winner_id="inst0",
                winner_path="/tmp/wt0",
                qa_verdict="pass",
                anti_slop_score=8,
                merge_policy="first_pass_wins",
                loser_ids=["inst1", "inst2"],
                orchestrator_run_id="test-001",
            )
            ok, msg = mod.write_pick_record(rec, pick_path)
            self.assertTrue(ok, msg)
            self.assertTrue(pick_path.exists())
            loaded = json.loads(pick_path.read_text(encoding="utf-8"))
            vok, vmsg = mod.validate_pick_record(loaded)
            self.assertTrue(vok, vmsg)
            self.assertEqual(loaded["schema_version"], 1)
            self.assertEqual(loaded["story_id"], "US-0108")
            self.assertIn("loser_instance_ids", loaded)


class TestUS0108ResourceCap(unittest.TestCase):
    """test_us0108_resource_cap (AC-5)."""

    def test_lockfile_acquire_release(self) -> None:
        mod = _load_arbiter()
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / ".git").mkdir()
            ok1, msg1 = mod.acquire_parallel_slot("slot1", repo_root, max_total=2)
            self.assertTrue(ok1, msg1)
            ok2, msg2 = mod.acquire_parallel_slot("slot2", repo_root, max_total=2)
            self.assertTrue(ok2, msg2)
            ok3, msg3 = mod.acquire_parallel_slot("slot3", repo_root, max_total=2)
            self.assertFalse(ok3)
            self.assertEqual(msg3, mod.ReasonCode.PARALLEL_DEV_RESOURCE_CAP_EXHAUSTED)
            mod.release_parallel_slot("slot1", repo_root)
            ok4, msg4 = mod.acquire_parallel_slot("slot4", repo_root, max_total=2)
            self.assertTrue(ok4, msg4)


class TestUS0108ExecuteSteps(unittest.TestCase):
    """test_us0108_execute_steps_25_28 (AC-6)."""

    def test_execute_disabled_by_default(self) -> None:
        mod = _load_arbiter()
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / ".git").mkdir()
            (repo_root / ".cursor").mkdir()
            scratchpad = repo_root / ".cursor" / "scratchpad.md"
            scratchpad.write_text("SOVEREIGN_PARALLEL_DEV=0\n", encoding="utf-8")
            result = mod.execute_parallel_dev("US-0108", "main", 3, scratchpad, repo_root)
            self.assertIsNone(result.winner_worktree)
            self.assertEqual(result.merge_result.conflicts, [mod.ReasonCode.PARALLEL_DEV_DISABLED])


class TestUS0108BackwardCompat(unittest.TestCase):
    """test_us0108_backward_compat_single_dev_unchanged (AC-7)."""

    def test_disabled_zero_overhead(self) -> None:
        mod = _load_arbiter()
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / ".git").mkdir()
            (repo_root / ".cursor").mkdir()
            scratchpad = repo_root / ".cursor" / "scratchpad.md"
            scratchpad.write_text("# no US-0108 keys\n", encoding="utf-8")
            self.assertFalse(mod.is_parallel_enabled(scratchpad))
            result = mod.execute_parallel_dev("US-0108", "main", 3, scratchpad, repo_root)
            self.assertIsNone(result.winner_worktree)
            self.assertEqual(result.merge_result.conflicts, [mod.ReasonCode.PARALLEL_DEV_DISABLED])


class TestUS0108ParityScope(unittest.TestCase):
    """test_us0108_parity_scope (AC-8)."""

    def test_parity_scope_registered(self) -> None:
        from check_intake_template_parity import SCOPES
        self.assertIn("sovereign-parallel-dev", SCOPES)
        pairs = SCOPES["sovereign-parallel-dev"]
        self.assertGreater(len(pairs), 0)


if __name__ == "__main__":
    unittest.main()
