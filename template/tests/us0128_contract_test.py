"""US-0128: Convergence smoke surrogate for waived-probe UAT slices.

11 contract markers (AC-1..AC-6 + compose + R1/R3). All static/fixture-based.
No live critic spawn. Markers 4, 5, 7 (T-007) live in this file on purpose.
"""

from __future__ import annotations

import dataclasses
import hashlib
import inspect
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _scripts_dir() -> Path:
    return _repo_root() / "scripts"


def _load_convergence():
    scripts = str(_scripts_dir())
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import sovereign_convergence_lib as mod  # noqa: E402

    return mod


SIX_CLASSES = (
    "browser_smoke",
    "api_health",
    "process_health",
    "cli_smoke",
    "build",
    "manual_operator",
)

CONVERGENCE_SMOKE_STEP = {
    "id": "convergence_smoke",
    "description": "Convergence smoke surrogate — waived-probe slice with green contract-test harness",
    "result": "pass",
    "marker": "test_us0128_convergence_smoke_surrogate",
    "evidence_ref": "tests/report.md Fail:0 + uat.json waived_probes[] (6 classes, UAT_PROBE_FORBIDDEN)",
    "probe_kind": "contract_tests_primary",
}


def _six_waived(n: int = 6) -> List[dict]:
    return [
        {
            "probe_class": cls,
            "reason": "fixture waived-probe slice",
            "reason_code": "UAT_PROBE_FORBIDDEN",
        }
        for cls in SIX_CLASSES[:n]
    ]


def _write_fixture(
    repo: Path,
    *,
    report_fail: int = 0,
    waived: Optional[List[dict]] = None,
    steps: Optional[List[dict]] = None,
    contract_test_failed: Optional[int] = 0,
    extra: Optional[Dict[str, Any]] = None,
) -> Path:
    (repo / "tests").mkdir(parents=True, exist_ok=True)
    sprint = repo / "sprints" / "S0128"
    sprint.mkdir(parents=True, exist_ok=True)
    (repo / "tests" / "report.md").write_text(
        f"Pass: 1\nFail: {report_fail}\n", encoding="utf-8"
    )
    uat: Dict[str, Any] = {
        "steps": list(steps) if steps is not None else [],
        "waived_probes": list(waived) if waived is not None else [],
    }
    if contract_test_failed is not None:
        uat["contract_test_failed"] = contract_test_failed
        uat["contract_test_passed"] = 11 - int(contract_test_failed)
        uat["contract_test_total"] = 11
    if extra:
        uat.update(extra)
    path = sprint / "uat.json"
    path.write_text(json.dumps(uat), encoding="utf-8")
    return path


def _files_byte_identical(a: Path, b: Path) -> bool:
    return a.read_bytes() == b.read_bytes()


class US0128SurrogatePassesWhenAllSixWaivedAndGreen(unittest.TestCase):
    """Marker 1: test_us0128_surrogate_passes_when_all_six_waived_and_green (AC-1/AC-5)."""

    def test_us0128_surrogate_passes_when_all_six_waived_and_green(self) -> None:
        conv = _load_convergence()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _write_fixture(
                repo,
                waived=_six_waived(6),
                steps=[CONVERGENCE_SMOKE_STEP],
                contract_test_failed=0,
            )
            result = conv._eval_smoke_green(repo)
            self.assertEqual(result.name, "smoke_green")
            self.assertEqual(result.status, "pass")
            self.assertIsNone(result.reason_code)
            self.assertFalse(result.skipped)


class US0128SurrogateMissingWhenNoStep(unittest.TestCase):
    """Marker 2: test_us0128_surrogate_missing_when_no_step (AC-1/AC-3/AC-5)."""

    def test_us0128_surrogate_missing_when_no_step(self) -> None:
        conv = _load_convergence()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _write_fixture(
                repo,
                waived=_six_waived(6),
                steps=[{"id": "UAT-1", "result": "pass", "description": "docs"}],
                contract_test_failed=0,
            )
            result = conv._eval_smoke_green(repo)
            self.assertEqual(result.status, "fail")
            self.assertEqual(result.reason_code, conv.CONVERGENCE_SMOKE_SURROGATE_MISSING)


class US0128SurrogateMissingWhenHarnessFail(unittest.TestCase):
    """Marker 3: test_us0128_surrogate_missing_when_harness_fail (AC-1/AC-3/AC-5)."""

    def test_us0128_surrogate_missing_when_harness_fail(self) -> None:
        conv = _load_convergence()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _write_fixture(
                repo,
                waived=_six_waived(6),
                steps=[],
                contract_test_failed=2,
            )
            result = conv._eval_smoke_green(repo)
            self.assertEqual(result.status, "fail")
            self.assertEqual(result.reason_code, conv.CONVERGENCE_SMOKE_SURROGATE_MISSING)
            self.assertNotEqual(
                result.reason_code, conv.ReasonCode.CONVERGENCE_SMOKE_PROBE_FAIL.value
            )


class US0128SurrogateMissingWhenPartialWaivers(unittest.TestCase):
    """Marker 4: test_us0128_surrogate_missing_when_partial_waivers (AC-1/AC-3/AC-5 / T-007)."""

    def test_us0128_surrogate_missing_when_partial_waivers(self) -> None:
        conv = _load_convergence()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _write_fixture(
                repo,
                waived=_six_waived(3),
                steps=[],
                contract_test_failed=0,
            )
            result = conv._eval_smoke_green(repo)
            self.assertEqual(result.status, "fail")
            self.assertEqual(result.reason_code, conv.CONVERGENCE_SMOKE_SURROGATE_MISSING)


class US0128RealSmokeStepPassWinsOverSurrogate(unittest.TestCase):
    """Marker 5: test_us0128_real_smoke_step_pass_wins_over_surrogate (AC-1/AC-5 / T-007)."""

    def test_us0128_real_smoke_step_pass_wins_over_surrogate(self) -> None:
        conv = _load_convergence()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _write_fixture(
                repo,
                waived=[],
                steps=[
                    {
                        "id": "browser_smoke",
                        "probe_kind": "browser_smoke",
                        "result": "pass",
                    }
                ],
                contract_test_failed=0,
            )
            result = conv._eval_smoke_green(repo)
            self.assertEqual(result.status, "pass")
            self.assertIsNone(result.reason_code)
            src = inspect.getsource(conv._eval_smoke_green)
            idx_legacy = src.find("_uat_smoke_passes")
            idx_surr = src.find("_all_six_live_runtime_probes_waived")
            self.assertGreaterEqual(idx_legacy, 0)
            self.assertGreater(idx_surr, idx_legacy)


class US0128RealSmokeStepFailUsesProbeFail(unittest.TestCase):
    """Marker 6: test_us0128_real_smoke_step_fail_uses_probe_fail_not_surrogate_missing (AC-1/AC-3/AC-5)."""

    def test_us0128_real_smoke_step_fail_uses_probe_fail_not_surrogate_missing(self) -> None:
        conv = _load_convergence()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _write_fixture(
                repo,
                waived=_six_waived(6),
                steps=[
                    {
                        "id": "cli_smoke",
                        "probe_kind": "cli_smoke",
                        "result": "fail",
                    }
                ],
                contract_test_failed=0,
            )
            result = conv._eval_smoke_green(repo)
            self.assertEqual(result.status, "fail")
            self.assertEqual(
                result.reason_code, conv.ReasonCode.CONVERGENCE_SMOKE_PROBE_FAIL.value
            )
            self.assertNotEqual(result.reason_code, conv.CONVERGENCE_SMOKE_SURROGATE_MISSING)


class US0128ComposeUs0109DeploySmokeUnchanged(unittest.TestCase):
    """Marker 7: test_us0128_compose_us0109_deploy_smoke_unchanged (AC-5 / T-007)."""

    def test_us0128_compose_us0109_deploy_smoke_unchanged(self) -> None:
        root = _repo_root()
        conv_src = (root / "scripts" / "sovereign_convergence_lib.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("DEPLOY_SMOKE", conv_src)
        self.assertNotIn("self_healing_deploy", conv_src)
        deploy_lib = (root / "scripts" / "self_healing_deploy_lib.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("DEPLOY_SMOKE_PROBE_OK", deploy_lib)
        self.assertIn("AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC", deploy_lib)
        us0109 = (root / "tests" / "us0109_contract_test.py").read_text(encoding="utf-8")
        self.assertIn("def test_us0109_scratchpad_keys_and_defaults", us0109)
        self.assertIn("run_smoke_probe_chain", us0109)
        rc = (root / "docs" / "engineering" / "reason_codes.md").read_text(encoding="utf-8")
        self.assertIn("`CONVERGENCE_SMOKE_PROBE_FAIL`", rc)
        self.assertIn("US-0109 deploy smoke", rc)


class US0128TemplateParityConvergenceLibAndCommands(unittest.TestCase):
    """Marker 8: test_us0128_template_parity_convergence_lib_and_commands (AC-5/AC-6)."""

    def test_us0128_template_parity_convergence_lib_and_commands(self) -> None:
        root = _repo_root()
        pairs = (
            (
                root / "scripts" / "sovereign_convergence_lib.py",
                root / "template" / "scripts" / "sovereign_convergence_lib.py",
            ),
            (
                root / ".cursor" / "commands" / "qa.md",
                root / "template" / ".cursor" / "commands" / "qa.md",
            ),
            (
                root / ".cursor" / "commands" / "verify-work.md",
                root / "template" / ".cursor" / "commands" / "verify-work.md",
            ),
        )
        for active, template in pairs:
            self.assertTrue(active.is_file(), msg=str(active))
            self.assertTrue(template.is_file(), msg=str(template))
            self.assertTrue(
                _files_byte_identical(active, template),
                msg=f"byte mismatch: {active} vs {template}",
            )
        qa = (root / ".cursor" / "commands" / "qa.md").read_text(encoding="utf-8")
        vw = (root / ".cursor" / "commands" / "verify-work.md").read_text(encoding="utf-8")
        self.assertIn("### Convergence smoke surrogate (US-0128)", qa)
        self.assertIn("### Convergence smoke surrogate (US-0128)", vw)
        self.assertIn('"id": "convergence_smoke"', qa)
        self.assertIn("probe_kind", qa)
        parity = (root / "scripts" / "check_intake_template_parity.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('".cursor/commands/qa.md"', parity)
        self.assertIn('".cursor/commands/verify-work.md"', parity)
        idx = parity.find("SOVEREIGN_CONVERGENCE_PAIRS")
        critic_idx = parity.find("SOVEREIGN_CRITIC_PAIRS")
        self.assertGreaterEqual(idx, 0)
        conv_block = parity[idx : idx + 800]
        self.assertIn("qa.md", conv_block)
        self.assertIn("verify-work.md", conv_block)
        critic_block = parity[critic_idx : critic_idx + 400]
        self.assertNotIn("qa.md", critic_block)


class US0128ComposeUs0110FiveConjunctUnchanged(unittest.TestCase):
    """Marker 9: test_us0128_compose_us0110_five_conjunct_unchanged (AC-5)."""

    def test_us0128_compose_us0110_five_conjunct_unchanged(self) -> None:
        conv = _load_convergence()
        self.assertEqual(
            conv.CONVERGENCE_CONJUNCTS,
            (
                "backlog_clear",
                "zero_deferrals",
                "critic_resolved",
                "smoke_green",
                "ledger_clean",
            ),
        )
        fields = {f.name for f in dataclasses.fields(conv.ConjunctResult)}
        self.assertEqual(fields, {"name", "status", "reason_code", "skipped"})
        self.assertEqual(len(conv.REASON_CODES), 10)
        self.assertIn("CONVERGENCE_SMOKE_PROBE_FAIL", conv.REASON_CODES)
        self.assertNotIn(conv.CONVERGENCE_SMOKE_SURROGATE_MISSING, conv.REASON_CODES)
        src = inspect.getsource(conv._eval_smoke_green)
        self.assertIn('name="smoke_green"', src)
        self.assertIn("ConjunctResult", src)
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/us0110_contract_test.py", "-q"],
            cwd=str(_repo_root()),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        self.assertIn("passed", proc.stdout.lower() + proc.stderr.lower())


class US0128ComposeUs0127CriticConjunctUnchanged(unittest.TestCase):
    """Marker 10: test_us0128_compose_us0127_critic_conjunct_unchanged (AC-5)."""

    def test_us0128_compose_us0127_critic_conjunct_unchanged(self) -> None:
        conv = _load_convergence()
        eval_src = inspect.getsource(conv._eval_critic_resolved)
        self.assertIn("read_open_blocking", inspect.getsource(conv._critic_jsonl_has_open))
        self.assertIn("jsonl_authoritative", eval_src)
        self.assertIn("_qa_findings_has_open_critic", eval_src)
        self.assertNotIn("_eval_smoke_green", eval_src)
        parity = (_repo_root() / "scripts" / "check_intake_template_parity.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("SOVEREIGN_CRITIC_PAIRS", parity)
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/us0127_contract_test.py", "-q"],
            cwd=str(_repo_root()),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)


class US0128ComposeUs0126WaivedProbeFixtureReferenceOnly(unittest.TestCase):
    """Marker 11: test_us0128_compose_us0126_waived_probe_fixture_reference_only (AC-5)."""

    def test_us0128_compose_us0126_waived_probe_fixture_reference_only(self) -> None:
        root = _repo_root()
        fixture = root / "sprints" / "S0126" / "uat.json"
        self.assertTrue(fixture.is_file())
        before = fixture.read_bytes()
        digest = hashlib.sha256(before).hexdigest()
        data = json.loads(before.decode("utf-8"))
        waived = data.get("waived_probes") or []
        classes = {
            row.get("probe_class")
            for row in waived
            if isinstance(row, dict) and row.get("reason_code") == "UAT_PROBE_FORBIDDEN"
        }
        self.assertEqual(set(SIX_CLASSES), classes)
        self.assertEqual(len(waived), 6)
        steps = data.get("steps") or []
        self.assertFalse(any(isinstance(s, dict) and s.get("id") == "convergence_smoke" for s in steps))
        this_src = Path(__file__).read_text(encoding="utf-8")
        self.assertNotRegex(this_src, r"S0126[/\\]uat\.json[^\n]{0,120}write_")
        after = fixture.read_bytes()
        self.assertEqual(before, after)
        self.assertEqual(digest, hashlib.sha256(after).hexdigest())


if __name__ == "__main__":
    unittest.main()
