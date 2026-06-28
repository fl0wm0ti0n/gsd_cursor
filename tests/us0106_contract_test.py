"""US-0106: Eight `test_us0106_*` contract tests for Sovereign Role-Behavior Manifest.

DEC-0106 §3: scratchpad literals, YAML v1 schema with 6 required sections, objective
injection char cap, obligation dispatch per-phase cap, cross_model_policy ordering
modes, zero-overhead default-off, compose guards (US-0069 matrix unchanged, US-0104
critic schema unchanged), and parity scope coverage.

Default-off: SOVEREIGN_ROLE_MANIFEST=0 → zero overhead.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_role_lib():
    root = _repo_root()
    scripts_dir = str(root / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import sovereign_role_manifest_lib as mod  # noqa: E402
    return mod


def _scratchpad_text(root: Path) -> tuple[str, str]:
    a = (root / ".cursor" / "scratchpad.md").read_text(encoding="utf-8")
    b = (root / "template" / ".cursor" / "scratchpad.md").read_text(encoding="utf-8")
    return a, b


def _manifest_text(root: Path) -> tuple[str, str]:
    a = (root / ".cursor" / "sovereign-role-manifest.yaml").read_text(encoding="utf-8")
    b = (root / "template" / ".cursor" / "sovereign-role-manifest.yaml.example").read_text(encoding="utf-8")
    return a, b


class US0106ScratchpadKeysTest(unittest.TestCase):
    """test_us0106_scratchpad_keys_literals (AC-1 / T-001)."""

    def test_us0106_scratchpad_keys_literals(self) -> None:
        lib = _load_role_lib()
        self.assertEqual(lib.SOVEREIGN_ROLE_MANIFEST_VALUES, {"0", "1"})
        self.assertEqual(lib.SOVEREIGN_ROLE_MANIFEST_DEFAULT, "0")
        self.assertEqual(lib.SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS_DEFAULT, 512)
        self.assertEqual(lib.SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE_DEFAULT, 2)
        self.assertEqual(lib.SOVEREIGN_ROLE_REVIEW_REWORK_MAX_DEFAULT, 1)

        root = _repo_root()
        a_text, t_text = _scratchpad_text(root)
        for text, lbl in ((a_text, "active"), (t_text, "template")):
            for key in (
                "SOVEREIGN_ROLE_MANIFEST",
                "SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS",
                "SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE",
                "SOVEREIGN_ROLE_REVIEW_REWORK_MAX",
            ):
                self.assertIn(key, text, f"{lbl} scratchpad missing {key}")
            self.assertIn("SOVEREIGN_ROLE_MANIFEST=0", text)
            self.assertIn("SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS=512", text)
            self.assertIn("SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE=2", text)
            self.assertIn("SOVEREIGN_ROLE_REVIEW_REWORK_MAX=1", text)
            self.assertIn("US-0106", text)

        self.assertFalse(lib.is_role_manifest_enabled({}))
        self.assertFalse(lib.is_role_manifest_enabled({lib.SOVEREIGN_ROLE_MANIFEST_KEY: "0"}))
        self.assertTrue(lib.is_role_manifest_enabled({lib.SOVEREIGN_ROLE_MANIFEST_KEY: "1"}))


class US0106ManifestSchemaTest(unittest.TestCase):
    """test_us0106_manifest_schema_v1_literals (AC-2 / T-002)."""

    def test_us0106_manifest_schema_v1_literals(self) -> None:
        lib = _load_role_lib()
        root = _repo_root()
        a_text, t_text = _manifest_text(root)

        required_sections = (
            "schema_version: 1",
            "roles:",
            "review_obligations:",
            "allowed_self_overrides:",
            "cross_model_policy:",
            "escalation_rules:",
        )
        for text, name in ((a_text, "active"), (t_text, "example")):
            for sect in required_sections:
                self.assertIn(sect, text, f"{name} manifest missing {sect}")

        self.assertEqual(lib.SCHEMA_VERSION, 1)
        self.assertEqual(lib.VALID_ROLE_IDS, {"po", "tech-lead", "dev", "qa", "release", "curator"})
        self.assertEqual(lib.VALID_REVIEW_FOCI, {"user_value_drift", "testability", "buildability", "deployability"})
        self.assertEqual(lib.VALID_DEFAULT_ORDERS, {
            "role_review_first", "critic_first", "critic_only", "role_review_only",
        })
        self.assertEqual(lib.ALLOWED_SELF_OVERRIDES, {"verbosity", "detail_level", "tone"})
        self.assertEqual(lib.OBJECTIVE_FILE_MAX_CHARS, 1024)

        self.assertIn("obligation_id: O1", a_text)
        self.assertIn("obligation_id: O2", a_text)
        self.assertIn("obligation_id: O3", a_text)
        self.assertIn("obligation_id: O4", a_text)


class US0106ObjectiveInjectionTest(unittest.TestCase):
    """test_us0106_objective_injection_char_cap (AC-4 / T-004)."""

    def test_us0106_objective_injection_char_cap(self) -> None:
        lib = _load_role_lib()
        root = _repo_root()

        # Valid objective (<= 1024 file max, > 512 injection cap)
        long_obj = "x" * 1000
        manifest = {
            "schema_version": 1,
            "roles": [{"role_id": "dev", "objective_function": long_obj}],
            "review_obligations": [],
        }
        scratch = {lib.SOVEREIGN_ROLE_MANIFEST_KEY: "1", lib.SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS_KEY: "512"}

        ok, err = lib.validate_manifest(manifest)
        self.assertTrue(ok, msg=err)

        with tempfile.TemporaryDirectory() as td:
            m_path = Path(td) / ".cursor" / "sovereign-role-manifest.yaml"
            m_path.parent.mkdir(parents=True)
            m_path.write_text(
                "schema_version: 1\nroles:\n  - role_id: dev\n    objective_function: " + long_obj + "\nreview_obligations: []\n",
                encoding="utf-8",
            )
            block, err = lib.build_objective_injection_block(scratch, "dev", Path(td))
            self.assertIsNone(err)
            self.assertIsNotNone(block)
            header = "## Role objective (dev)\n\n"
            self.assertTrue(block.startswith(header))
            self.assertLessEqual(len(block), len(header) + 512)

        block_off, err_off = lib.build_objective_injection_block(
            {lib.SOVEREIGN_ROLE_MANIFEST_KEY: "0"}, "dev"
        )
        self.assertIsNone(block_off)
        self.assertEqual(err_off, lib.ReasonCode.DISABLED.value)

        block_unknown, err_unknown = lib.build_objective_injection_block(scratch, "nope-role", root)
        self.assertIsNone(block_unknown)
        self.assertEqual(err_unknown, lib.ReasonCode.UNKNOWN_ROLE.value)


class US0106ObligationDispatchTest(unittest.TestCase):
    """test_us0106_obligation_dispatch_cap (AC-5 / T-005)."""

    def test_us0106_obligation_dispatch_cap(self) -> None:
        lib = _load_role_lib()
        manifest = {
            "schema_version": 1,
            "roles": [
                {"role_id": "tech-lead", "objective_function": "Build architecture"},
            ],
            "review_obligations": [
                {"obligation_id": "A", "reviewer_role": "po", "target_role": "tech-lead",
                 "trigger_phase": "architecture", "review_focus": "user_value_drift"},
                {"obligation_id": "B", "reviewer_role": "dev", "target_role": "tech-lead",
                 "trigger_phase": "architecture", "review_focus": "buildability"},
                {"obligation_id": "C", "reviewer_role": "qa", "target_role": "tech-lead",
                 "trigger_phase": "architecture", "review_focus": "testability"},
            ],
        }
        obligations = lib.list_obligations_for_phase("architecture", "tech-lead", manifest, max_per_phase=2)
        self.assertEqual(len(obligations), 2)
        self.assertEqual(obligations[0].obligation_id, "A")
        self.assertEqual(obligations[1].obligation_id, "B")

        obligation = obligations[0]
        dispatch, err = lib.dispatch_role_review(obligation, "sprints/S0106/summary.md", "architecture", "tech-lead")
        self.assertEqual(err, "")
        self.assertIsNotNone(dispatch)
        self.assertTrue(dispatch.spawn_only)
        self.assertEqual(dispatch.boundary_token, "role_review")
        self.assertEqual(dispatch.reviewer_role, "po")
        self.assertEqual(dispatch.producer_role, "tech-lead")
        self.assertEqual(dispatch.trigger_phase, "architecture")
        self.assertEqual(dispatch.obligation_id, "A")

        dispatch_off, err_off = lib.dispatch_role_review(
            obligation, "sprints/S0106/summary.md", "architecture", "tech-lead",
            scratchpad={lib.SOVEREIGN_ROLE_MANIFEST_KEY: "0"},
        )
        self.assertIsNone(dispatch_off)
        self.assertEqual(err_off, lib.ReasonCode.DISABLED.value)


class US0106ComposeUS0069Test(unittest.TestCase):
    """test_us0106_us0069_compose_no_matrix_change (AC-8 / T-008 compose guard).

    Verifies that US-0069 phase→role matrix invariants are unchanged regardless
    of SOVEREIGN_ROLE_MANIFEST value. Review spawns are supplementary.
    """

    PHASE_ROLE_EXPECTATIONS = {
        "architecture": "tech-lead",
        "execute": "dev",
        "qa": "qa",
        "verify-work": "qa",
        "plan-verify": "qa",
        "release": "release",
        "research": "tech-lead",
    }

    def test_us0106_us0069_compose_no_matrix_change(self) -> None:
        root = _repo_root()
        ref_path = root / "docs" / "engineering" / "auto-orchestration-reference.md"
        self.assertTrue(ref_path.is_file(), "auto-orchestration-reference.md missing")
        text = ref_path.read_text(encoding="utf-8")

        import re as _re
        matrix_re = _re.compile(r"^\| (`\w[\w-]*`)[^|]*\|([^|]*)\|([^|]*)\|", _re.MULTILINE)
        matrix = {}
        for m in matrix_re.finditer(text):
            phase = m.group(1).strip("`")
            default_col = m.group(3).strip().strip("`")
            matrix[phase] = (m.group(2), default_col)

        for phase, role in self.PHASE_ROLE_EXPECTATIONS.items():
            self.assertIn(phase, matrix, f"phase {phase} missing from matrix")
            allowed, default = matrix[phase]
            self.assertIn(f"`{role}`", allowed, f"phase→role for {phase} should allow {role}")
            self.assertEqual(default, role, f"phase→role for {phase}: default should be {role}, got {default}")

        self.assertNotIn("SOVEREIGN_ROLE_MANIFEST", text)
        self.assertNotIn("sovereign_role_manifest", text)


class US0106ComposeUS0104Test(unittest.TestCase):
    """test_us0106_us0104_compose_no_critic_schema_change (AC-8 / T-009 compose guard).

    Verifies US-0104 sovereign_critic_findings.jsonl schema invariants are unchanged.
    """

    CRITIC_LENSES = {"challenger", "architect", "subtractor"}
    SEVERITY_VALUES = {"low", "medium", "high", "critical"}
    CRITIC_REQUIRED_FIELDS = {
        "ts", "orchestrator_run_id", "phase_id", "role", "producer_model_id",
        "critic_model_id", "lens", "finding_id", "severity", "confidence",
        "anti_slop_score", "finding_text", "status", "blocking", "degraded_mode",
    }

    def test_us0106_us0104_compose_no_critic_schema_change(self) -> None:
        Scripts_dir = str(_repo_root() / "scripts")
        if Scripts_dir not in sys.path:
            sys.path.insert(0, Scripts_dir)
        import sovereign_critic_lib as critic  # noqa: E402

        self.assertEqual(critic.LENS_VALUES, self.CRITIC_LENSES)
        self.assertEqual(critic.SEVERITY_VALUES, self.SEVERITY_VALUES)
        self.assertEqual(critic.FINDING_REQUIRED_FIELDS, self.CRITIC_REQUIRED_FIELDS)
        self.assertEqual(critic.SCHEMA_VERSION, 1)
        self.assertEqual(critic.CROSS_MODEL_REVIEW_DEFAULT, "0")
        self.assertEqual(critic.CROSS_MODEL_ANTISLOP_THRESHOLD_DEFAULT, 6)
        self.assertEqual(critic.CROSS_MODEL_REWORK_MAX_DEFAULT, 2)

        self.assertFalse(critic.is_cross_model_review_enabled({}))
        self.assertFalse(critic.is_cross_model_review_enabled({critic.CROSS_MODEL_REVIEW_KEY: "0"}))
        self.assertTrue(critic.is_cross_model_review_enabled({critic.CROSS_MODEL_REVIEW_KEY: "1"}))


class US0106ZeroOverheadTest(unittest.TestCase):
    """test_us0106_zero_overhead_default (AC-1 / AC-7 / T-001 / T-007).

    When SOVEREIGN_ROLE_MANIFEST=0, every entry point short-circuits to no-op
    without file I/O.
    """

    def test_us0106_zero_overhead_default(self) -> None:
        lib = _load_role_lib()

        block, err = lib.build_objective_injection_block({}, "dev")
        self.assertIsNone(block)
        self.assertEqual(err, lib.ReasonCode.DISABLED.value)

        block, err = lib.build_objective_injection_block(
            {lib.SOVEREIGN_ROLE_MANIFEST_KEY: "0"}, "po"
        )
        self.assertIsNone(block)
        self.assertEqual(err, lib.ReasonCode.DISABLED.value)

        root = _repo_root()
        manifest, err = lib.load_manifest(root, {})
        self.assertIsNone(manifest)
        self.assertEqual(err, lib.ReasonCode.DISABLED.value)

        dispatch, err = lib.dispatch_role_review(
            lib.RoleObligation("O1", "po", "tech-lead", "architecture", "user_value_drift"),
            "sprints/S0106/summary.md", "architecture", "tech-lead",
            scratchpad={},
        )
        self.assertIsNone(dispatch)
        self.assertEqual(err, lib.ReasonCode.DISABLED.value)

        obligations = lib.list_obligations_for_phase(
            "architecture", "tech-lead",
            {"review_obligations": [{"obligation_id": "O1", "reviewer_role": "po",
                                     "target_role": "tech-lead", "trigger_phase": "architecture",
                                     "review_focus": "user_value_drift"}]},
        )
        self.assertEqual(len(obligations), 1)
        self.assertEqual(lib.resolve_critic_ordering({}), "role_review_first")


class US0106ParityScopeTest(unittest.TestCase):
    """test_us0106_parity_scope (AC-7 / T-011)."""

    def test_us0106_parity_scope(self) -> None:
        root = _repo_root()
        checker = root / "scripts" / "check_intake_template_parity.py"
        self.assertTrue(checker.is_file())
        text = checker.read_text(encoding="utf-8")

        self.assertIn("sovereign-role-manifest", text)
        self.assertIn("SOVEREIGN_ROLE_MANIFEST_PAIRS", text)

        result = subprocess.run(
            [sys.executable, str(checker), "--scope=sovereign-role-manifest", "--repo", str(root)],
            capture_output=True, text=True, cwd=str(root),
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("[INTAKE_TEMPLATE_PARITY_OK]", result.stdout)


if __name__ == "__main__":
    unittest.main()
