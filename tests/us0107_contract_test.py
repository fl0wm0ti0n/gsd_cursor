"""US-0107: Eight `test_us0107_*` contract tests for Sovereign Loop Mode.

DEC-0107 §10: scratchpad literals, deferral JSONL schema, advance deferral policy,
drain-generate gate, notification fail-open, goal-mode coupling, zero-overhead default,
compose-no-stop-matrix-change.

Default-off: AUTO_SOVEREIGN=0 → zero overhead.
"""

from __future__ import annotations

import inspect
import json
import sys
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest import mock


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_loop_lib():
    root = _repo_root()
    scripts_dir = str(root / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import sovereign_loop_lib as mod  # noqa: E402
    return mod


def _load_convergence_lib():
    root = _repo_root()
    scripts_dir = str(root / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import sovereign_convergence_lib as mod  # noqa: E402
    return mod


def _enabled_scratchpad(lib) -> dict:
    return {
        lib.AUTO_SOVEREIGN_KEY: "1",
        "SOVEREIGN_GOAL_MODE": "goal_convergence",
    }


def _minimal_converged_repo(repo: Path) -> None:
    (repo / "docs" / "product").mkdir(parents=True)
    (repo / "tests").mkdir()
    (repo / "sprints" / "S0001").mkdir(parents=True)
    (repo / "handoffs").mkdir()
    (repo / "docs" / "product" / "backlog.md").write_text(
        "## US-9999 — Test\n- Status: DONE\n",
        encoding="utf-8",
    )
    (repo / "tests" / "report.md").write_text("Pass: 1\nFail: 0\n", encoding="utf-8")
    (repo / "sprints" / "S0001" / "uat.json").write_text(
        json.dumps({"steps": [{"id": "smoke-1", "probe_kind": "cli_smoke", "result": "pass"}]}),
        encoding="utf-8",
    )


class US0107ScratchpadKeysTest(unittest.TestCase):
    """test_us0107_scratchpad_keys_literals (AC-1)."""

    def test_us0107_scratchpad_keys_literals(self) -> None:
        lib = _load_loop_lib()
        self.assertEqual(lib.AUTO_SOVEREIGN_VALUES, {"0", "1"})
        self.assertEqual(lib.AUTO_SOVEREIGN_DEFAULT, "0")
        self.assertEqual(lib.AUTO_SOVEREIGN_DEFERRAL_MAX_DEFAULT, 50)
        self.assertEqual(lib.AUTO_SOVEREIGN_DRAIN_GENERATE_MAX_DEFAULT, 3)
        self.assertEqual(lib.AUTO_SOVEREIGN_DEFERRAL_POLICY_DEFAULT, "resolve_first")
        self.assertEqual(lib.SOVEREIGN_NOTIFY_TARGET_DEFAULT, "off")

        root = _repo_root()
        for pad_path in (root / ".cursor" / "scratchpad.md", root / "template" / ".cursor" / "scratchpad.md"):
            text = pad_path.read_text(encoding="utf-8")
            for key in (
                "AUTO_SOVEREIGN",
                "AUTO_SOVEREIGN_DEFERRAL_MAX",
                "AUTO_SOVEREIGN_DRAIN_GENERATE_MAX",
                "AUTO_SOVEREIGN_DEFERRAL_POLICY",
                "SOVEREIGN_NOTIFY_TARGET",
                "SOVEREIGN_NOTIFY_NTFY_TOPIC",
                "SOVEREIGN_NOTIFY_NTFY_BASE",
                "SOVEREIGN_NOTIFY_HOOK_URL",
                "SOVEREIGN_NOTIFY_EMAIL_TO",
            ):
                self.assertIn(key, text, f"missing {key} in {pad_path}")
            self.assertIn("AUTO_SOVEREIGN=0", text)
            self.assertIn("AUTO_SOVEREIGN_DEFERRAL_MAX=50", text)
            self.assertIn("AUTO_SOVEREIGN_DRAIN_GENERATE_MAX=3", text)
            self.assertIn("AUTO_SOVEREIGN_DEFERRAL_POLICY=resolve_first", text)
            self.assertIn("SOVEREIGN_NOTIFY_TARGET=off", text)
            self.assertIn("Sovereign Loop Mode (US-0107 / DEC-0107)", text)


class US0107DeferralJsonlSchemaTest(unittest.TestCase):
    """test_us0107_deferral_jsonl_schema_contract (AC-2)."""

    def test_us0107_deferral_jsonl_schema_contract(self) -> None:
        lib = _load_loop_lib()
        root = _repo_root()
        self.assertTrue((root / "handoffs" / "sovereign_deferrals" / ".gitkeep").is_file())
        self.assertTrue((root / "template" / "handoffs" / "sovereign_deferrals" / ".gitkeep").is_file())

        sample = lib.build_sample_deferral()
        ok, err = lib.schema_check_deferral(sample)
        self.assertTrue(ok, msg=err)

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            sp = _enabled_scratchpad(lib)
            deferral_id, reason = lib.append_deferral(
                repo,
                sp,
                reason_code=lib.ReasonCode.DEPLOY_DEFERRED.value,
                work_item_kind="deploy",
                work_item_ref="release-target:staging",
                source_orchestrator_run_id="auto-test",
                remediation_hint="Retry deploy smoke after cap exhaustion.",
            )
            self.assertIsNone(reason)
            self.assertIsNotNone(deferral_id)

            open_rows, _ = lib.list_open_deferrals(repo, scratchpad=sp)
            self.assertEqual(len(open_rows), 1)

            resolved, resolve_err = lib.resolve_deferral(
                repo,
                str(deferral_id),
                orchestrator_run_id="auto-test-resolve",
            )
            self.assertTrue(resolved, msg=resolve_err)
            open_after, _ = lib.list_open_deferrals(repo, scratchpad=sp)
            self.assertEqual(len(open_after), 0)


class US0107AdvanceDeferralPolicyTest(unittest.TestCase):
    """test_us0107_advance_deferral_policy_literals (AC-3)."""

    def test_us0107_advance_deferral_policy_literals(self) -> None:
        lib = _load_loop_lib()

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _minimal_converged_repo(repo)
            sp_base = _enabled_scratchpad(lib)

            sp_stop = dict(sp_base)
            sp_stop[lib.AUTO_SOVEREIGN_DEFERRAL_POLICY_KEY] = "stop"
            lib.append_deferral(
                repo,
                sp_stop,
                reason_code=lib.ReasonCode.DEPLOY_DEFERRED.value,
                work_item_kind="block",
                work_item_ref="phase:release",
                source_orchestrator_run_id="auto-test",
                remediation_hint="Blocked by open deferral under stop policy.",
            )
            stop_result = lib.advance_sovereign_loop(repo, sp_stop, orchestrator_run_id="auto-test")
            self.assertEqual(stop_result.action, "defer")
            self.assertEqual(stop_result.reason_code, lib.ReasonCode.SOVEREIGN_LOOP_ADVANCE_BLOCKED.value)

            sp_resolve = dict(sp_base)
            sp_resolve[lib.AUTO_SOVEREIGN_DEFERRAL_POLICY_KEY] = "resolve_first"
            resolve_result = lib.advance_sovereign_loop(repo, sp_resolve, orchestrator_run_id="auto-test")
            self.assertEqual(resolve_result.action, "blocked")
            self.assertEqual(resolve_result.reason_code, lib.ReasonCode.SOVEREIGN_LOOP_ADVANCE_BLOCKED.value)

            sp_skip = dict(sp_base)
            sp_skip[lib.AUTO_SOVEREIGN_DEFERRAL_POLICY_KEY] = "skip"
            skip_result = lib.advance_sovereign_loop(repo, sp_skip, orchestrator_run_id="auto-test")
            self.assertIn(skip_result.action, ("drain_generate", "terminal_cap"))


class US0107DrainGenerateGateTest(unittest.TestCase):
    """test_us0107_drain_generate_gate_contract (AC-4)."""

    def test_us0107_drain_generate_gate_contract(self) -> None:
        lib = _load_loop_lib()
        self.assertEqual(lib.MAX_CANDIDATES_PER_ITERATION, 3)
        eph = lib.build_drain_generate_ephemeral_id("auto-run-1", 2)
        self.assertEqual(eph, "drain-gen-auto-run-1-2")

        candidates = [
            {
                "candidate_id": str(uuid.uuid4()),
                "title": f"Candidate {idx}",
                "summary": "Summary text.",
                "ac_sketch": ["AC-1: example"],
                "priority": "P2",
                "provenance": "vision",
            }
            for idx in range(4)
        ]
        bundle = {
            "schema_version": 1,
            "orchestrator_run_id": "auto-test",
            "iteration": 1,
            "generated_at": "2026-06-29T00:00:00Z",
            "candidates": candidates,
        }
        ok, err = lib.schema_check_drain_generate_bundle(bundle)
        self.assertFalse(ok)
        self.assertIn("cap", (err or "").lower())

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _minimal_converged_repo(repo)
            conv = _load_convergence_lib()
            conv.clear_eval_cache()
            result = conv.evaluate_convergence(repo, _enabled_scratchpad(lib), orchestrator_run_id="auto-test")
            inputs = lib.build_drain_generate_spawn_inputs(repo, _enabled_scratchpad(lib), result)
            self.assertEqual(inputs["vision_path"], "docs/product/vision.md")
            self.assertIn("unmet_conditions", inputs)
            self.assertIn("blocked_by", inputs)
            self.assertIn("goal_text", inputs)

        auto_text = (_repo_root() / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        self.assertIn("Decision gate (mandatory per candidate)", auto_text)
        self.assertIn("drain-gen-{orchestrator_run_id}-{iteration}", auto_text)


class US0107NotificationFailOpenTest(unittest.TestCase):
    """test_us0107_notification_fail_open_literals (AC-5)."""

    def test_us0107_notification_fail_open_literals(self) -> None:
        lib = _load_loop_lib()
        payload = {"schema_version": 1, "event_type": "convergence"}

        ok_off, code_off = lib.dispatch_notification(
            {lib.SOVEREIGN_NOTIFY_TARGET_KEY: "off"},
            "convergence",
            payload,
        )
        self.assertTrue(ok_off)
        self.assertIsNone(code_off)

        ok_email, code_email = lib.dispatch_notification(
            {lib.SOVEREIGN_NOTIFY_TARGET_KEY: "email"},
            "convergence",
            payload,
        )
        self.assertFalse(ok_email)
        self.assertEqual(code_email, lib.ReasonCode.SOVEREIGN_NOTIFY_TARGET_INVALID.value)

        ok_missing, code_missing = lib.dispatch_notification(
            {
                lib.SOVEREIGN_NOTIFY_TARGET_KEY: "ntfy",
                lib.SOVEREIGN_NOTIFY_NTFY_TOPIC_KEY: "",
            },
            "convergence",
            payload,
        )
        self.assertTrue(ok_missing)
        self.assertEqual(code_missing, lib.ReasonCode.SOVEREIGN_NOTIFY_CONFIG_MISSING.value)

        with mock.patch("sovereign_loop_lib.urllib_request.urlopen", side_effect=OSError("network down")):
            ok_fail, code_fail = lib.dispatch_notification(
                {
                    lib.SOVEREIGN_NOTIFY_TARGET_KEY: "hook",
                    lib.SOVEREIGN_NOTIFY_HOOK_URL_KEY: "https://example.invalid/hook",
                },
                "timeout",
                payload,
            )
        self.assertTrue(ok_fail)
        self.assertIsNone(code_fail)


class US0107GoalModeCouplingTest(unittest.TestCase):
    """test_us0107_goal_mode_coupling_fail_closed (AC-1 / AC-3)."""

    def test_us0107_goal_mode_coupling_fail_closed(self) -> None:
        lib = _load_loop_lib()
        self.assertFalse(lib.is_sovereign_loop_enabled({lib.AUTO_SOVEREIGN_KEY: "1", "SOVEREIGN_GOAL_MODE": "phase_driven"}))

        result = lib.advance_sovereign_loop(
            Path("."),
            {lib.AUTO_SOVEREIGN_KEY: "1", "SOVEREIGN_GOAL_MODE": "phase_driven"},
            orchestrator_run_id="auto-test",
        )
        self.assertEqual(result.action, "blocked")
        self.assertEqual(result.reason_code, lib.ReasonCode.SOVEREIGN_LOOP_GOAL_MODE_REQUIRED.value)


class US0107ZeroOverheadDefaultTest(unittest.TestCase):
    """test_us0107_zero_overhead_default (AC-1)."""

    def test_us0107_zero_overhead_default(self) -> None:
        lib = _load_loop_lib()

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            before = set(repo.rglob("*"))
            rows, reason = lib.list_open_deferrals(repo, scratchpad={lib.AUTO_SOVEREIGN_KEY: "0"})
            step = lib.advance_sovereign_loop(repo, {lib.AUTO_SOVEREIGN_KEY: "0"}, orchestrator_run_id="auto-test")
            after = set(repo.rglob("*"))
            self.assertEqual(before, after)
            self.assertEqual(rows, [])
            self.assertEqual(reason, lib.ReasonCode.SOVEREIGN_LOOP_DISABLED.value)
            self.assertEqual(step.action, "noop")


class US0107ComposeNoStopMatrixChangeTest(unittest.TestCase):
    """test_us0107_compose_no_stop_matrix_change (AC-8)."""

    _MARKERS = {
        "US-0088": "Deterministic stop matrix",
        "US-0092": "Full-autonomy stop matrix (US-0092)",
        "US-0095": "Native in-chat auto-chain (US-0095",
        "US-0044": "Optional backlog-drain mode (US-0044",
    }

    def test_us0107_compose_no_stop_matrix_change(self) -> None:
        root = _repo_root()
        auto_active = (root / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        auto_ref = (root / "docs" / "engineering" / "auto-orchestration-reference.md").read_text(encoding="utf-8")
        for story, marker in self._MARKERS.items():
            self.assertIn(marker, auto_active, f"{story} marker missing from auto.md")
            if story in ("US-0088", "US-0092", "US-0095"):
                self.assertIn(marker, auto_ref, f"{story} marker missing from auto-orchestration-reference.md")

        self.assertIn("Sovereign Loop Mode (US-0107", auto_active)
        self.assertIn("additive", auto_active.lower())


class US0107US0110ConvergenceImportTest(unittest.TestCase):
    """test_us0107_us0110_convergence_import_contract (AC-6 / AC-8)."""

    def test_us0107_us0110_convergence_import_contract(self) -> None:
        conv = _load_convergence_lib()
        source = inspect.getsource(conv._eval_zero_deferrals)
        self.assertIn("sovereign_loop_lib", source)
        self.assertIn("list_open_deferrals", source)

        loop = _load_loop_lib()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _minimal_converged_repo(repo)
            sp = _enabled_scratchpad(loop)
            deferral_id, _ = loop.append_deferral(
                repo,
                sp,
                reason_code=loop.ReasonCode.DEPLOY_DEFERRED.value,
                work_item_kind="deploy",
                work_item_ref="staging",
                source_orchestrator_run_id="auto-test",
                remediation_hint="Open deploy deferral blocks convergence.",
            )
            self.assertIsNotNone(deferral_id)
            conv.clear_eval_cache()
            result = conv.evaluate_convergence(repo, sp, orchestrator_run_id="auto-test")
            self.assertFalse(result.converged)
            self.assertEqual(result.conjuncts["zero_deferrals"].status, "fail")


class US0107US0095SpawnOnlyRegressionTest(unittest.TestCase):
    """test_us0107_us0095_spawn_only_regression_guard (AC-4 / AC-8)."""

    def test_us0107_us0095_spawn_only_regression_guard(self) -> None:
        auto_text = (_repo_root() / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        self.assertIn("MUST Task-spawn", auto_text)
        self.assertIn("spawn-only", auto_text.lower())
        self.assertIn("US-0095", auto_text)
        self.assertIn("drain-generate", auto_text.lower())
        self.assertIn("No auto-append", auto_text)


if __name__ == "__main__":
    unittest.main()
