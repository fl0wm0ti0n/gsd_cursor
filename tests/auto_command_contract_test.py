"""Ensure slim `/auto` command retains DEC-0029/0038/0051/0052 contract markers (US-0080 / T-005)."""

from __future__ import annotations

import unittest
from pathlib import Path


class AutoCommandContractTest(unittest.TestCase):
    def test_slim_auto_retains_gate_markers(self) -> None:
        root = Path(__file__).resolve().parents[1]
        text = (root / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        required = [
            "PHASE_CONTEXT_ISOLATION_VIOLATION",
            "RUNTIME_PROOF_MISSING",
            "PHASE_ROLE_CAPABILITY_MISSING",
            "PHASE_POLICY_CONFLICT",
            "START_FROM_PHASE_PLAN_EMPTY_INTERSECTION",
            "| `execute` | `dev`",
            "docs/engineering/auto-orchestration-reference.md",
            "[AUTO_RESUME_ERROR]",
        ]
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
