"""US-0110: Eight `test_us0110_*` contract tests for Goal-Based Convergence Loops.

DEC-0110 §8: scratchpad literals, five-conjunct predicate, goal authoring,
goal_progress block, partial delivery on timeout, reason-code inventory,
phase_driven zero-overhead, compose-no-stop-matrix-change.

Default-off: SOVEREIGN_GOAL_MODE=phase_driven → zero overhead.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_lib():
    root = _repo_root()
    scripts_dir = str(root / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import sovereign_convergence_lib as mod  # noqa: E402
    return mod


class US0110ScratchpadKeysTest(unittest.TestCase):
    """test_us0110_scratchpad_keys_literals (AC-1)."""

    def test_us0110_scratchpad_keys_literals(self) -> None:
        lib = _load_lib()
        self.assertEqual(lib.SOVEREIGN_GOAL_MODE_VALUES, {"phase_driven", "goal_convergence"})
        self.assertEqual(lib.SOVEREIGN_GOAL_MODE_DEFAULT, "phase_driven")
        self.assertEqual(lib.SOVEREIGN_GOAL_TOP_N_DEFAULT, 3)
        self.assertEqual(lib.SOVEREIGN_GOAL_MAX_CHARS_DEFAULT, 512)
        self.assertEqual(lib.SOVEREIGN_GOAL_TIMEOUT_MAX_DEFAULT, 0)

        root = _repo_root()
        for pad_path in (root / ".cursor" / "scratchpad.md", root / "template" / ".cursor" / "scratchpad.md"):
            text = pad_path.read_text(encoding="utf-8")
            for key in (
                "SOVEREIGN_GOAL_MODE",
                "SOVEREIGN_GOAL",
                "SOVEREIGN_GOAL_TOP_N",
                "SOVEREIGN_GOAL_MAX_CHARS",
                "SOVEREIGN_GOAL_TIMEOUT_MAX",
            ):
                self.assertIn(key, text, f"missing {key} in {pad_path}")
            self.assertIn("SOVEREIGN_GOAL_MODE=phase_driven", text)
            self.assertIn("SOVEREIGN_GOAL_TOP_N=3", text)
            self.assertIn("SOVEREIGN_GOAL_MAX_CHARS=512", text)
            self.assertIn("SOVEREIGN_GOAL_TIMEOUT_MAX=0", text)
            self.assertIn("Goal-Based Convergence (US-0110 / DEC-0110)", text)

        self.assertFalse(lib.is_goal_convergence_enabled({lib.SOVEREIGN_GOAL_MODE_KEY: "phase_driven"}))
        self.assertTrue(lib.is_goal_convergence_enabled({lib.SOVEREIGN_GOAL_MODE_KEY: "goal_convergence"}))


class US0110EvaluatorFiveConjunctTest(unittest.TestCase):
    """test_us0110_evaluator_five_conjunct_contract (AC-2)."""

    def test_us0110_evaluator_five_conjunct_contract(self) -> None:
        lib = _load_lib()
        lib.clear_eval_cache()
        RC = lib.ReasonCode

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs" / "product").mkdir(parents=True)
            (repo / "tests").mkdir()
            (repo / "sprints" / "S0001").mkdir(parents=True)
            (repo / "handoffs").mkdir()

            # Backlog with OPEN story → backlog_clear fail
            (repo / "docs" / "product" / "backlog.md").write_text(
                "## US-9999 — Test\n- Status: OPEN\n", encoding="utf-8"
            )
            (repo / "tests" / "report.md").write_text("Pass: 1\nFail: 0\n", encoding="utf-8")
            (repo / "sprints" / "S0001" / "uat.json").write_text(
                json.dumps({
                    "steps": [{"id": "smoke-1", "probe_kind": "cli_smoke", "result": "pass"}],
                }),
                encoding="utf-8",
            )

            sp = {lib.SOVEREIGN_GOAL_MODE_KEY: "goal_convergence"}
            r1 = lib.evaluate_convergence(repo, sp, orchestrator_run_id="auto-test")
            self.assertFalse(r1.converged)
            self.assertIn(RC.CONVERGENCE_OPEN_STORIES_REMAIN.value, r1.blocked_by)
            self.assertEqual(r1.conjuncts["backlog_clear"].status, "fail")
            self.assertEqual(r1.conjuncts["zero_deferrals"].status, "skip")
            self.assertIn("deferral_register_not_yet_deployed", r1.unmet_conditions)
            self.assertEqual(r1.conjuncts["critic_resolved"].status, "skip")
            self.assertIn("critic_register_not_yet_deployed", r1.unmet_conditions)

            # Clear backlog → backlog pass; deferrals file non-empty → fail
            (repo / "docs" / "product" / "backlog.md").write_text(
                "## US-9999 — Test\n- Status: DONE\n", encoding="utf-8"
            )
            (repo / "handoffs" / "sovereign_deferrals.jsonl").write_text('{"id": "d1"}\n', encoding="utf-8")
            lib.clear_eval_cache()
            r2 = lib.evaluate_convergence(repo, sp, orchestrator_run_id="auto-test")
            self.assertIn(RC.CONVERGENCE_DEFERRALS_PENDING.value, r2.blocked_by)
            self.assertEqual(r2.conjuncts["zero_deferrals"].status, "fail")

            # Empty deferrals; missing smoke → fail-closed
            (repo / "handoffs" / "sovereign_deferrals.jsonl").write_text("", encoding="utf-8")
            (repo / "tests" / "report.md").write_text("Pass: 1\nFail: 1\n", encoding="utf-8")
            lib.clear_eval_cache()
            r3 = lib.evaluate_convergence(repo, sp, orchestrator_run_id="auto-test")
            self.assertIn(RC.CONVERGENCE_SMOKE_PROBE_FAIL.value, r3.blocked_by)

            # Memoization: same mtimes → same cache_key
            k1 = r3.cache_key
            r3b = lib.evaluate_convergence(repo, sp, orchestrator_run_id="auto-test")
            self.assertEqual(r3b.cache_key, k1)

            (repo / "tests" / "report.md").write_text("Pass: 2\nFail: 0\n", encoding="utf-8")
            lib.clear_eval_cache()
            r4 = lib.evaluate_convergence(repo, sp, orchestrator_run_id="auto-test")
            self.assertNotEqual(r4.cache_key, k1)


class US0110GoalAuthoringTest(unittest.TestCase):
    """test_us0110_goal_authoring_explicit_and_derive (AC-3)."""

    def test_us0110_goal_authoring_explicit_and_derive(self) -> None:
        lib = _load_lib()
        RC = lib.ReasonCode

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs" / "product").mkdir(parents=True)

            explicit = {lib.SOVEREIGN_GOAL_KEY: "Ship convergence v1", lib.SOVEREIGN_GOAL_MODE_KEY: "goal_convergence"}
            g = lib.resolve_goal(explicit, repo)
            self.assertEqual(g.goal_source, "explicit")
            self.assertEqual(g.goal_text, "Ship convergence v1")
            self.assertIsNone(g.reason_code)

            (repo / "docs" / "product" / "vision.md").write_text(
                "# Vision\n\nFirst eligible paragraph about the product.\n\n"
                "Second paragraph with more detail.\n",
                encoding="utf-8",
            )
            derive_sp = {lib.SOVEREIGN_GOAL_MODE_KEY: "goal_convergence", lib.SOVEREIGN_GOAL_TOP_N_KEY: "2"}
            g2 = lib.resolve_goal(derive_sp, repo)
            self.assertEqual(g2.goal_source, "vision_derived")
            self.assertIn("First eligible paragraph", g2.goal_text or "")
            self.assertIn("Second paragraph", g2.goal_text or "")

            empty_repo = Path(tmp) / "empty"
            empty_repo.mkdir()
            (empty_repo / "docs" / "product").mkdir(parents=True)
            g3 = lib.resolve_goal(derive_sp, empty_repo)
            self.assertEqual(g3.reason_code, RC.SOVEREIGN_GOAL_DERIVE_FAILED)


class US0110GoalProgressBlockTest(unittest.TestCase):
    """test_us0110_goal_progress_block_shape (AC-4)."""

    def test_us0110_goal_progress_block_shape(self) -> None:
        lib = _load_lib()
        result = lib.ConvergenceResult(
            converged=False,
            unmet_conditions=["test gap"],
            blocked_by=[lib.ReasonCode.CONVERGENCE_OPEN_STORIES_REMAIN.value],
            conjuncts={
                name: lib.ConjunctResult(name=name, status="fail", reason_code="CONVERGENCE_OPEN_STORIES_REMAIN", skipped=False)
                for name in lib.CONVERGENCE_CONJUNCTS
            },
            evaluated_at="2026-06-28T19:30:00.000Z",
            orchestrator_run_id="auto-test",
        )
        block = lib.build_goal_progress_block(result, "My goal", "explicit", "auto-test")
        ok, err = lib.schema_check_goal_progress(block)
        self.assertTrue(ok, msg=err)
        gp = block["goal_progress"]
        self.assertEqual(gp["mode"], "goal_convergence")
        self.assertEqual(gp["goal_source"], "explicit")
        self.assertEqual(gp["schema_version"], 1)


class US0110PartialDeliveryTimeoutTest(unittest.TestCase):
    """test_us0110_partial_delivery_timeout (AC-5)."""

    def test_us0110_partial_delivery_timeout(self) -> None:
        lib = _load_lib()
        RC = lib.ReasonCode

        timed, code = lib.check_timeout({lib.SOVEREIGN_GOAL_TIMEOUT_MAX_KEY: "0"}, 100)
        self.assertFalse(timed)
        self.assertIsNone(code)

        timed, code = lib.check_timeout({lib.SOVEREIGN_GOAL_TIMEOUT_MAX_KEY: "5"}, 5)
        self.assertTrue(timed)
        self.assertEqual(code, RC.SOVEREIGN_GOAL_TIMEOUT)

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs" / "product").mkdir(parents=True)
            (repo / "handoffs").mkdir()
            (repo / "docs" / "product" / "backlog.md").write_text(
                "## US-0001 — A\n- Status: DONE\n\n## US-0002 — B\n- Status: OPEN\n",
                encoding="utf-8",
            )
            result = lib.ConvergenceResult(
                converged=False,
                unmet_conditions=["timeout"],
                blocked_by=[],
                conjuncts={},
                evaluated_at="2026-06-28T19:30:00.000Z",
            )
            out = lib.write_partial_delivery_report(
                repo, result, "Test goal", RC.SOVEREIGN_GOAL_TIMEOUT, "auto-test"
            )
            text = out.read_text(encoding="utf-8")
            for section in (
                "Goal", "Evaluated At", "Unmet Conditions", "Blocked By",
                "Completed Stories", "Open Stories", "Deferrals Summary", "Remediation",
            ):
                self.assertIn(f"## {section}", text)
            self.assertIn("SOVEREIGN_GOAL_TIMEOUT", text)
            self.assertIn("US-0002", text)
            self.assertIn("US-0001", text)


class US0110ReasonCodeInventoryTest(unittest.TestCase):
    """test_us0110_reason_code_inventory (AC-6)."""

    def test_us0110_reason_code_inventory(self) -> None:
        lib = _load_lib()
        expected = {
            "CONVERGENCE_OPEN_STORIES_REMAIN",
            "CONVERGENCE_DEFERRALS_PENDING",
            "CONVERGENCE_CROSS_REVIEWER_OPEN",
            "CONVERGENCE_SMOKE_PROBE_FAIL",
            "CONVERGENCE_LEDGER_EXTENSIONS_UNAPPROVED",
            "SOVEREIGN_GOAL_TIMEOUT",
            "SOVEREIGN_GOAL_MODE_INVALID",
            "SOVEREIGN_GOAL_MISSING",
            "SOVEREIGN_GOAL_DERIVE_FAILED",
            "CONVERGENCE_EVAL_FAILED",
        }
        self.assertEqual(lib.REASON_CODES, expected)
        self.assertEqual(len(lib.REASON_CODES), 10)

        rc_text = (_repo_root() / "docs" / "engineering" / "reason_codes.md").read_text(encoding="utf-8")
        self.assertIn("## US-0110:", rc_text)
        for code in expected:
            self.assertIn(f"`{code}`", rc_text, f"missing {code} in reason_codes.md")


class US0110PhaseDrivenZeroOverheadTest(unittest.TestCase):
    """test_us0110_phase_driven_zero_overhead (AC-7)."""

    def test_us0110_phase_driven_zero_overhead(self) -> None:
        lib = _load_lib()
        lib.clear_eval_cache()

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "handoffs").mkdir()
            sp = {lib.SOVEREIGN_GOAL_MODE_KEY: "phase_driven"}
            before = set(repo.rglob("*"))
            result = lib.evaluate_convergence(repo, sp, orchestrator_run_id="auto-test")
            after = set(repo.rglob("*"))
            self.assertEqual(before, after)
            self.assertFalse(result.converged)
            self.assertIn("goal_convergence_mode_disabled", result.unmet_conditions)
            self.assertFalse(lib.emit_goal_progress_to_resume_brief(repo, sp, "auto-test"))


class US0110ComposeNoStopMatrixChangeTest(unittest.TestCase):
    """test_us0110_compose_no_stop_matrix_change (AC-7 / AC-8)."""

    _MARKERS = {
        "US-0088": "Deterministic stop matrix",
        "US-0092": "Full-autonomy stop matrix (US-0092)",
        "US-0095": "Native in-chat auto-chain (US-0095",
        "US-0044": "Optional backlog-drain mode (US-0044",
    }

    def test_us0110_compose_no_stop_matrix_change(self) -> None:
        lib = _load_lib()
        root = _repo_root()

        auto_active = (root / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        auto_ref = (root / "docs" / "engineering" / "auto-orchestration-reference.md").read_text(encoding="utf-8")
        for story, marker in self._MARKERS.items():
            self.assertIn(marker, auto_active, f"{story} marker missing from auto.md")
            if story in ("US-0088", "US-0092", "US-0095"):
                self.assertIn(marker, auto_ref, f"{story} marker missing from auto-orchestration-reference.md")

        # Convergence lib must not write into composed story command surfaces
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "handoffs").mkdir()
            sp = {lib.SOVEREIGN_GOAL_MODE_KEY: "goal_convergence"}
            lib.evaluate_convergence(repo, sp)
            written = {str(p.relative_to(repo)).replace("\\", "/") for p in repo.rglob("*") if p.is_file()}
            for protected in (
                ".cursor/commands/auto.md",
                "docs/engineering/auto-orchestration-reference.md",
            ):
                self.assertNotIn(protected, written)


if __name__ == "__main__":
    unittest.main()
