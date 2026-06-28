"""US-0104: Eight `test_us0104_*` contract tests for Cross-Model Adversarial Critic.

DEC-0104 §12: scratchpad literals, sovereign-critic command, three-lens enum,
findings JSONL schema, reconciliation branches, model_id isolation extension,
anti-slop rework cap, degraded fallback zero-overhead.

Default-off: CROSS_MODEL_REVIEW=0 → zero overhead.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
import uuid
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_critic_lib():
    root = _repo_root()
    scripts_dir = str(root / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import sovereign_critic_lib as mod  # noqa: E402
    return mod


def _load_convergence_lib():
    root = _repo_root()
    scripts_dir = str(root / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import sovereign_convergence_lib as mod  # noqa: E402
    return mod


class US0104ScratchpadKeysTest(unittest.TestCase):
    """test_us0104_scratchpad_keys_literals (AC-1)."""

    def test_us0104_scratchpad_keys_literals(self) -> None:
        lib = _load_critic_lib()
        self.assertEqual(lib.CROSS_MODEL_REVIEW_VALUES, {"0", "1"})
        self.assertEqual(lib.CROSS_MODEL_REVIEW_DEFAULT, "0")
        self.assertEqual(lib.CROSS_MODEL_ANTISLOP_THRESHOLD_DEFAULT, 6)
        self.assertEqual(lib.CROSS_MODEL_REWORK_MAX_DEFAULT, 2)

        root = _repo_root()
        for pad_path in (root / ".cursor" / "scratchpad.md", root / "template" / ".cursor" / "scratchpad.md"):
            text = pad_path.read_text(encoding="utf-8")
            for key in (
                "CROSS_MODEL_REVIEW",
                "CROSS_MODEL_ANTISLOP_THRESHOLD",
                "CROSS_MODEL_REWORK_MAX",
            ):
                self.assertIn(key, text, f"missing {key} in {pad_path}")
            self.assertIn("CROSS_MODEL_REVIEW=0", text)
            self.assertIn("CROSS_MODEL_ANTISLOP_THRESHOLD=6", text)
            self.assertIn("CROSS_MODEL_REWORK_MAX=2", text)
            self.assertIn("Cross-Model Adversarial Critic (US-0104 / DEC-0104)", text)

        self.assertFalse(lib.is_cross_model_review_enabled({}))
        self.assertFalse(lib.is_cross_model_review_enabled({lib.CROSS_MODEL_REVIEW_KEY: "0"}))
        self.assertTrue(lib.is_cross_model_review_enabled({lib.CROSS_MODEL_REVIEW_KEY: "1"}))


class US0104SovereignCriticCommandTest(unittest.TestCase):
    """test_us0104_sovereign_critic_command_literals (AC-2)."""

    def test_us0104_sovereign_critic_command_literals(self) -> None:
        root = _repo_root()
        for rel in (
            ".cursor/commands/sovereign-critic.md",
            "template/.cursor/commands/sovereign-critic.md",
        ):
            text = (root / rel).read_text(encoding="utf-8")
            self.assertIn("# /sovereign-critic", text)
            self.assertIn("phase_id", text)
            self.assertIn("producer_model_id", text)
            self.assertIn("evidence_ref", text)
            self.assertIn("handoffs/sovereign_critic_findings.jsonl", text)
            self.assertIn("cross_reviewer_findings", text)
            self.assertIn("CROSS_MODEL_REVIEW=1", text)

        auto_text = (root / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        self.assertIn("Cross-model adversarial critic post-phase hook (US-0104 / DEC-0104)", auto_text)
        self.assertIn("/sovereign-critic", auto_text)
        self.assertIn("CROSS_MODEL_ANTISLOP_FAIL", auto_text)
        self.assertIn("CROSS_MODEL_REWORK_CAP_EXHAUSTED", auto_text)


class US0104ThreeLensEnumTest(unittest.TestCase):
    """test_us0104_three_lens_enum_contract (AC-3)."""

    def test_us0104_three_lens_enum_contract(self) -> None:
        lib = _load_critic_lib()
        self.assertEqual(lib.LENS_VALUES, {"challenger", "architect", "subtractor"})
        self.assertEqual(len(lib.LENS_CHECKLIST_KEYS), 3)
        for lens in lib.LENS_VALUES:
            self.assertIn(lens, lib.LENS_CHECKLIST_KEYS)
            self.assertEqual(len(lib.LENS_CHECKLIST_KEYS[lens]), 4)

        cmd = (_repo_root() / ".cursor" / "commands" / "sovereign-critic.md").read_text(encoding="utf-8")
        for lens in lib.LENS_VALUES:
            self.assertIn(f"**`{lens}`**", cmd)
        self.assertIn("all three lenses", cmd.lower())


class US0104FindingsJsonlSchemaTest(unittest.TestCase):
    """test_us0104_findings_jsonl_schema_contract (AC-5)."""

    def test_us0104_findings_jsonl_schema_contract(self) -> None:
        lib = _load_critic_lib()
        self.assertEqual(len(lib.FINDING_REQUIRED_FIELDS), 15)

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "handoffs").mkdir(parents=True)
            findings = repo / "handoffs" / "sovereign_critic_findings.jsonl"
            sample = lib.build_sample_finding(finding_id=str(uuid.uuid4()))
            ok, code = lib.append_finding(
                findings,
                sample,
                scratchpad={lib.CROSS_MODEL_REVIEW_KEY: "1"},
            )
            self.assertTrue(ok, msg=str(code))
            self.assertIsNone(code)

            rows = lib.read_open_blocking(repo)
            self.assertEqual(len(rows), 0)  # non-blocking sample

            blocking = lib.build_sample_finding(
                finding_id=str(uuid.uuid4()),
                blocking=True,
                finding_text="Blocking race on concurrent append path",
            )
            lib.append_finding(
                findings,
                blocking,
                scratchpad={lib.CROSS_MODEL_REVIEW_KEY: "1"},
            )
            open_rows = lib.read_open_blocking(repo)
            self.assertEqual(len(open_rows), 1)

            resolved = lib.resolve_finding(findings, blocking["finding_id"], "resolved")
            self.assertTrue(resolved)
            self.assertEqual(len(lib.read_open_blocking(repo)), 0)


class US0104ReconciliationTest(unittest.TestCase):
    """test_us0104_reconciliation_agreement_branches (AC-3 / AC-5)."""

    def test_us0104_reconciliation_agreement_branches(self) -> None:
        lib = _load_critic_lib()
        shared_text = "Shared coupling risk at module boundary"
        raw = [
            lib.build_sample_finding(lens="challenger", finding_text=shared_text),
            lib.build_sample_finding(lens="architect", finding_text=shared_text),
            lib.build_sample_finding(lens="subtractor", finding_text="Unique over abstraction in helper"),
        ]
        result = lib.reconcile_findings(raw)
        self.assertEqual(len(result.agreement_groups), 1)
        self.assertEqual(len(result.single_finder_flags), 1)
        high = [f for f in result.findings if f.get("confidence") == "high"]
        medium = [f for f in result.findings if f.get("confidence") == "medium"]
        self.assertEqual(len(high), 1)
        self.assertEqual(len(medium), 1)
        self.assertFalse(high[0]["single_finder"])
        self.assertTrue(medium[0]["single_finder"])


class US0104ModelIdIsolationTest(unittest.TestCase):
    """test_us0104_model_id_isolation_evidence_extension (AC-4)."""

    def test_us0104_model_id_isolation_evidence_extension(self) -> None:
        lib = _load_critic_lib()
        self.assertEqual(
            lib.ISOLATION_EVIDENCE_BASE_FIELDS,
            {"phase_id", "role", "fresh_context_marker", "timestamp", "evidence_ref"},
        )

        execute = (_repo_root() / ".cursor" / "commands" / "execute.md").read_text(encoding="utf-8")
        self.assertIn("model_id=", execute)
        self.assertIn("ISOLATION_EVIDENCE_MODEL_ID_MISSING", execute)
        self.assertIn("CROSS_MODEL_REVIEW=1", execute)

        critic_cmd = (_repo_root() / ".cursor" / "commands" / "sovereign-critic.md").read_text(encoding="utf-8")
        self.assertIn("model_id=", critic_cmd)

        ok, code = lib.check_isolation_model_id(
            {"phase_id": "execute", "role": "dev", "model_id": "inherit"},
            {lib.CROSS_MODEL_REVIEW_KEY: "1"},
        )
        self.assertTrue(ok)
        self.assertIsNone(code)

        bad, bad_code = lib.check_isolation_model_id({}, {lib.CROSS_MODEL_REVIEW_KEY: "1"})
        self.assertFalse(bad)
        self.assertEqual(bad_code.value, "ISOLATION_EVIDENCE_MODEL_ID_MISSING")


class US0104AntislopReworkCapTest(unittest.TestCase):
    """test_us0104_antislop_rework_cap_literals (AC-6)."""

    def test_us0104_antislop_rework_cap_literals(self) -> None:
        lib = _load_critic_lib()
        self.assertEqual(lib.compute_anti_slop_aggregate([7, 9, 6]), 6)
        self.assertEqual(lib.parse_scratchpad_threshold({}), 6)
        self.assertEqual(lib.parse_scratchpad_rework_max({}), 2)

        auto = (_repo_root() / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        for token in (
            "CROSS_MODEL_ANTISLOP_THRESHOLD",
            "CROSS_MODEL_REWORK_MAX",
            "CROSS_MODEL_ANTISLOP_FAIL",
            "CROSS_MODEL_REWORK_CAP_EXHAUSTED",
            "compute_anti_slop_aggregate",
        ):
            self.assertIn(token, auto)

        execute = (_repo_root() / ".cursor" / "commands" / "execute.md").read_text(encoding="utf-8")
        self.assertIn("critic_evidence", execute)
        self.assertIn("build_critic_evidence_block", execute)

        block = lib.build_critic_evidence_block(
            scratchpad={lib.CROSS_MODEL_REVIEW_KEY: "1"},
            producer_model_id="inherit",
            critic_model_id="fast",
            anti_slop_aggregate=7,
        )
        self.assertIsNotNone(block)
        self.assertEqual(block["findings_path"], "handoffs/sovereign_critic_findings.jsonl")
        self.assertIsNone(
            lib.build_critic_evidence_block(
                scratchpad={lib.CROSS_MODEL_REVIEW_KEY: "0"},
                producer_model_id="inherit",
                critic_model_id="fast",
                anti_slop_aggregate=7,
            )
        )


class US0104DegradedFallbackTest(unittest.TestCase):
    """test_us0104_degraded_fallback_zero_overhead (AC-7)."""

    def test_us0104_degraded_fallback_zero_overhead(self) -> None:
        lib = _load_critic_lib()

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "findings.jsonl"
            sample = lib.build_sample_finding(finding_id=str(uuid.uuid4()))
            ok, code = lib.append_finding(path, sample, scratchpad={lib.CROSS_MODEL_REVIEW_KEY: "0"})
            self.assertFalse(ok)
            self.assertEqual(code.value, "CROSS_MODEL_REVIEW_DISABLED")
            self.assertFalse(path.exists())

        auto = (_repo_root() / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        self.assertIn("CROSS_MODEL_DEGRADED_MODE", auto)
        self.assertIn("degraded_mode", auto)
        self.assertIn("CROSS_MODEL_REVIEW=0", auto)

        result = lib.select_critic_model("fast", {lib.CROSS_MODEL_REVIEW_KEY: "1"}, "execute")
        if result.degraded:
            self.assertEqual(result.reason_code.value, "CROSS_MODEL_DEGRADED_MODE")


class US0104US0048ComposeTest(unittest.TestCase):
    """test_us0104_us0048_compose_no_base_schema_change (AC-4 / AC-8)."""

    def test_us0104_us0048_compose_no_base_schema_change(self) -> None:
        lib = _load_critic_lib()
        self.assertEqual(len(lib.ISOLATION_EVIDENCE_BASE_FIELDS), 5)

        execute = (_repo_root() / ".cursor" / "commands" / "execute.md").read_text(encoding="utf-8")
        for field in lib.ISOLATION_EVIDENCE_BASE_FIELDS:
            self.assertIn(field, execute)

        dec = (_repo_root() / "decisions" / "DEC-0029.md").read_text(encoding="utf-8")
        self.assertIn("phase_id, role, fresh_context_marker, timestamp, evidence_ref", dec)


class US0104US0110CriticPathTest(unittest.TestCase):
    """test_us0104_us0110_critic_path_unchanged (AC-8 compose guard)."""

    def test_us0104_us0110_critic_path_unchanged(self) -> None:
        critic = _load_critic_lib()
        conv = _load_convergence_lib()
        self.assertEqual(str(critic.FINDINGS_PATH).replace("\\", "/"), "handoffs/sovereign_critic_findings.jsonl")
        self.assertEqual(str(conv.CRITIC_PATH).replace("\\", "/"), "handoffs/sovereign_critic_findings.jsonl")
        self.assertEqual(critic.FINDINGS_PATH, conv.CRITIC_PATH)


if __name__ == "__main__":
    unittest.main()
