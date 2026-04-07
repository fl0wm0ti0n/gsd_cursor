"""Ensure slim `/auto` command retains DEC-0029/0038/0051/0052 contract markers (US-0080 / BUG-0006 / R-0065)."""

from __future__ import annotations

import unittest
from pathlib import Path


class AutoCommandContractTest(unittest.TestCase):
    def test_slim_auto_retains_gate_markers(self) -> None:
        root = Path(__file__).resolve().parents[1]
        text = (root / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        required = [
            "spawn-only orchestrator",
            "spawn a fresh subagent",
            "phase deliverables",
            "AUTO_ORCHESTRATOR_PHASE_EXECUTION",
            "PHASE_CONTEXT_ISOLATION_VIOLATION",
            "RUNTIME_PROOF_MISSING",
            "PHASE_ROLE_CAPABILITY_MISSING",
            "PHASE_POLICY_CONFLICT",
            "START_FROM_PHASE_PLAN_EMPTY_INTERSECTION",
            "| `execute` | `dev`",
            "docs/engineering/auto-orchestration-reference.md",
            "[AUTO_RESUME_ERROR]",
            "bug-target=BUG-####",
            "bug-target=all-open",
            "AUTO_SCHEDULER_CONFLICT",
            "AUTO_BUG_QUEUE_EMPTY",
            "AUTO_BUG_TARGET_UNKNOWN",
            "AUTO_BUG_TARGET_NOT_OPEN",
            "US-0087",
            "US-0069",
        ]
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_slim_auto_no_affirmative_in_process_phase_run(self) -> None:
        """R-0065 matrix row 4: no wording that implies the orchestrator may run phases in-turn."""
        root = Path(__file__).resolve().parents[1]
        text = (root / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        lower = text.lower()
        misleading = (
            "orchestrator may run the",
            "orchestrator can run the",
            "orchestrator should run the",
        )
        for fragment in misleading:
            with self.subTest(fragment=fragment):
                self.assertNotIn(fragment, lower)

    def test_template_auto_literal_parity_active(self) -> None:
        """BUG-0006 / AC-2: template mirrors active `.cursor/commands/auto.md` byte-for-byte."""
        root = Path(__file__).resolve().parents[1]
        active = (root / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        template = (root / "template" / ".cursor" / "commands" / "auto.md").read_text(
            encoding="utf-8"
        )
        self.assertEqual(active, template)

    def test_reference_documents_spawn_boundary_and_links(self) -> None:
        root = Path(__file__).resolve().parents[1]
        ref = (
            root / "docs" / "engineering" / "auto-orchestration-reference.md"
        ).read_text(encoding="utf-8")
        for token in (
            "spawn-only orchestrator",
            "AUTO_ORCHESTRATOR_PHASE_EXECUTION",
            "decisions/DEC-0029.md",
            "decisions/DEC-0038.md",
            "Optional bug-queue mode (US-0087)",
            "bug-target=BUG-####",
            "bug-target=all-open",
            "AUTO_SCHEDULER_CONFLICT",
            "AUTO_BUG_QUEUE_EMPTY",
            "DEC-0069",
        ):
            with self.subTest(token=token):
                self.assertIn(token, ref)

    def test_template_auto_orchestration_reference_literal_parity_active(self) -> None:
        """US-0087 / AC-10: template mirrors active auto-orchestration-reference."""
        root = Path(__file__).resolve().parents[1]
        active = (
            root / "docs" / "engineering" / "auto-orchestration-reference.md"
        ).read_text(encoding="utf-8")
        template = (
            root / "template" / "docs" / "engineering" / "auto-orchestration-reference.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(active, template)

    def test_active_scratchpad_documents_auto_bug_keys(self) -> None:
        root = Path(__file__).resolve().parents[1]
        text = (root / ".cursor" / "scratchpad.md").read_text(encoding="utf-8")
        for key in (
            "AUTO_BUG_QUEUE",
            "AUTO_BUG_TARGET",
            "AUTO_BUG_MAX_ITEMS",
            "AUTO_BUG_ON_BLOCK",
        ):
            with self.subTest(key=key):
                self.assertIn(key, text)

    def test_template_scratchpad_example_documents_auto_bug_keys(self) -> None:
        root = Path(__file__).resolve().parents[1]
        text = (
            root / "template" / ".cursor" / "scratchpad.local.example.md"
        ).read_text(encoding="utf-8")
        for key in (
            "AUTO_BUG_QUEUE",
            "AUTO_BUG_TARGET",
            "AUTO_BUG_MAX_ITEMS",
            "AUTO_BUG_ON_BLOCK",
        ):
            with self.subTest(key=key):
                self.assertIn(key, text)


if __name__ == "__main__":
    unittest.main()
