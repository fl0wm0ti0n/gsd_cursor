"""Regression fixtures for token-cost run class + AC-2 compare (US-0080 / DEC-0062)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = _ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import token_cost_lib  # noqa: E402


class TokenCostLibTest(unittest.TestCase):
    def test_run_class_hash_stable(self) -> None:
        rc = {
            "phase_policy_mode": "full",
            "requested_start_from": "",
            "resolution_source": "resume_brief",
            "resolved_phase_plan": [
                "intake",
                "discovery",
                "research",
                "architecture",
                "sprint-plan",
                "plan-verify",
                "execute",
                "qa",
                "verify-work",
                "release",
                "refresh-context",
            ],
            "resolved_start_phase": "intake",
            "SECURITY_REVIEW": "0",
            "TOKEN_PROFILE": "balanced",
            "story_id": "US-0080",
        }
        h = token_cost_lib.compute_run_class_hash(rc)
        self.assertEqual(
            h,
            "60a4694b5da8b8650b1e031b773db99b98e632b17865553eac6ef916b5992b87",
        )

    def test_strict_proof_hash_vector(self) -> None:
        h = token_cost_lib.compute_strict_proof_hash(
            "auto-20260329-02",
            "rp-auto-20260329-02-execute-dev-20260329T221500Z-US0080-S0059",
            "execute",
            "dev",
            "2026-03-29T22:15:00Z",
            3600,
        )
        self.assertEqual(
            h,
            "c98bc4a22ba34bfd0e378e1f3f9ce6540b7749550dd2787e0248c8d3367fd879",
        )

    def test_compare_ac2_ok_and_mismatch(self) -> None:
        fx = _ROOT / "tests" / "fixtures" / "token_cost"
        base = json.loads((fx / "baseline.json").read_text(encoding="utf-8"))
        ok = json.loads((fx / "target_ok.json").read_text(encoding="utf-8"))
        bad = json.loads((fx / "target_bad_hash.json").read_text(encoding="utf-8"))
        self.assertTrue(token_cost_lib.compare_cache_read_reduction(base, ok)[0])
        self.assertFalse(token_cost_lib.compare_cache_read_reduction(base, bad)[0])

    def test_validate_run_totals(self) -> None:
        errs = token_cost_lib.validate_run_totals(
            {
                "cache_read_tokens": 1,
                "input_tokens": 2,
                "output_tokens": 3,
                "metric_source": "fixture",
            }
        )
        self.assertEqual(errs, [])
        bad = token_cost_lib.validate_run_totals(
            {
                "cache_read_tokens": -1,
                "input_tokens": 0,
                "output_tokens": 0,
                "metric_source": "x",
            }
        )
        self.assertTrue(any("invalid_non_negative_int" in e for e in bad))


class TokenCostCliTest(unittest.TestCase):
    def test_compare_cli_ok(self) -> None:
        fx = _ROOT / "tests" / "fixtures" / "token_cost"
        env = dict(os.environ)
        proc = subprocess.run(
            [
                sys.executable,
                str(_ROOT / "scripts" / "token_cost_compare.py"),
                str(fx / "baseline.json"),
                str(fx / "target_ok.json"),
            ],
            cwd=str(_ROOT),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_compare_cli_bad_hash(self) -> None:
        fx = _ROOT / "tests" / "fixtures" / "token_cost"
        proc = subprocess.run(
            [
                sys.executable,
                str(_ROOT / "scripts" / "token_cost_compare.py"),
                str(fx / "baseline.json"),
                str(fx / "target_bad_hash.json"),
            ],
            cwd=str(_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)


if __name__ == "__main__":
    unittest.main()
