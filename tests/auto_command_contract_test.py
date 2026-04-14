"""Ensure slim `/auto` command retains DEC-0029/0038/0051/0052 contract markers (US-0080 / BUG-0006 / R-0065 / US-0088)."""

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
            "Automation remote routing contract (US-0086)",
            "start container <target_id>",
            "REMOTE_AUTOMATION_MODE_OFF",
            "REMOTE_TARGET_UNKNOWN",
            "REMOTE_TARGET_DISABLED",
            "REMOTE_TARGET_UNROUTABLE",
            "AUTO_REMOTE_AUTOMATION_PROFILE",
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
            "Automation remote routing contract (US-0086)",
            "AUTO_REMOTE_AUTOMATION_PROFILE",
            "start container <target_id>",
            "REMOTE_AUTOMATION_MODE_OFF",
            "REMOTE_TARGET_UNKNOWN",
            "REMOTE_TARGET_DISABLED",
            "REMOTE_TARGET_UNROUTABLE",
            "secret_surface=names_only",
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

    # --- US-0088: continuation, reference Step 5, drain advance, AUTO_QUIET ---

    def test_slim_auto_references_step5_and_continuation(self) -> None:
        """US-0088 / AC-4: compact auto.md points unambiguously to reference Step 5."""
        root = Path(__file__).resolve().parents[1]
        text = (root / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        for token in (
            "reference Step 5",
            "Multi-phase continuation",
            "deterministic stop condition",
            "Outer-driver equivalence",
            "recomputing",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_reference_step5_continuation_markers(self) -> None:
        """US-0088 / AC-4: reference doc contains normative multi-phase continuation phrases."""
        root = Path(__file__).resolve().parents[1]
        ref = (
            root / "docs" / "engineering" / "auto-orchestration-reference.md"
        ).read_text(encoding="utf-8")
        for token in (
            "reference Step 5",
            "intersected resolved schedule order",
            "advance through all subsequent phases",
            "deterministic stop condition",
            "Outer-driver equivalence (AC-1, Option B)",
            "Deterministic stop matrix (US-0088)",
        ):
            with self.subTest(token=token):
                self.assertIn(token, ref)

    def test_reference_drain_advance_markers(self) -> None:
        """US-0088 / AC-3: reference doc contains normative drain advance phrases."""
        root = Path(__file__).resolve().parents[1]
        ref = (
            root / "docs" / "engineering" / "auto-orchestration-reference.md"
        ).read_text(encoding="utf-8")
        for token in (
            "next eligible OPEN story",
            "recompute the materialized phase plan",
            "reloading merged",
            "story boundary",
            "BACKLOG_MAX_STORIES_REACHED",
        ):
            with self.subTest(token=token):
                self.assertIn(token, ref)

    def test_reference_auto_quiet_markers(self) -> None:
        """US-0088 / AC-2: reference doc documents AUTO_QUIET and TOKEN_PROFILE orthogonality."""
        root = Path(__file__).resolve().parents[1]
        ref = (
            root / "docs" / "engineering" / "auto-orchestration-reference.md"
        ).read_text(encoding="utf-8")
        for token in (
            "AUTO_QUIET",
            "TOKEN_PROFILE",
            "non-suppressible",
            "routine per-phase success chatter",
        ):
            with self.subTest(token=token):
                self.assertIn(token, ref)

    def test_slim_auto_spawn_only_regression(self) -> None:
        """BUG-0006 / US-0088: spawn-only contract unchanged after US-0088 edits."""
        root = Path(__file__).resolve().parents[1]
        text = (root / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        lower = text.lower()
        forbidden = (
            "orchestrator may run the",
            "orchestrator can run the",
            "orchestrator should run the",
            "orchestrator executes the phase",
            "orchestrator performs the phase",
        )
        for fragment in forbidden:
            with self.subTest(fragment=fragment):
                self.assertNotIn(fragment, lower)

    def test_active_scratchpad_documents_auto_quiet(self) -> None:
        """US-0088 / AC-2: active scratchpad documents AUTO_QUIET key."""
        root = Path(__file__).resolve().parents[1]
        text = (root / ".cursor" / "scratchpad.md").read_text(encoding="utf-8")
        self.assertIn("AUTO_QUIET", text)

    def test_template_scratchpad_example_documents_auto_quiet(self) -> None:
        """US-0088 / AC-2: template scratchpad example documents AUTO_QUIET key."""
        root = Path(__file__).resolve().parents[1]
        text = (
            root / "template" / ".cursor" / "scratchpad.local.example.md"
        ).read_text(encoding="utf-8")
        self.assertIn("AUTO_QUIET", text)

    def test_template_runbook_literal_parity_active(self) -> None:
        """US-0088 / AC-5: template mirrors active runbook.md byte-for-byte."""
        root = Path(__file__).resolve().parents[1]
        active = (root / "docs" / "engineering" / "runbook.md").read_text(
            encoding="utf-8"
        )
        template = (
            root / "template" / "docs" / "engineering" / "runbook.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(active, template)

    def test_template_scratchpad_baseline_literal_parity_active(self) -> None:
        """US-0088 / AC-5: template scratchpad.md mirrors active scratchpad.md."""
        root = Path(__file__).resolve().parents[1]
        active = (root / ".cursor" / "scratchpad.md").read_text(encoding="utf-8")
        template = (root / "template" / ".cursor" / "scratchpad.md").read_text(
            encoding="utf-8"
        )
        self.assertEqual(active, template)

    def test_template_scratchpad_example_literal_parity_active(self) -> None:
        """US-0088 / AC-5: template scratchpad example mirrors active example."""
        root = Path(__file__).resolve().parents[1]
        active = (root / ".cursor" / "scratchpad.local.example.md").read_text(
            encoding="utf-8"
        )
        template = (
            root / "template" / ".cursor" / "scratchpad.local.example.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(active, template)

    def test_remote_automation_profile_keys_exist_in_scratchpads(self) -> None:
        """US-0086 / AC-1: automation profile keys exist in active and template scratchpads."""
        root = Path(__file__).resolve().parents[1]
        active = (root / ".cursor" / "scratchpad.md").read_text(encoding="utf-8")
        active_example = (root / ".cursor" / "scratchpad.local.example.md").read_text(
            encoding="utf-8"
        )
        template = (root / "template" / ".cursor" / "scratchpad.md").read_text(
            encoding="utf-8"
        )
        template_example = (
            root / "template" / ".cursor" / "scratchpad.local.example.md"
        ).read_text(encoding="utf-8")
        for key in (
            "AUTO_REMOTE_AUTOMATION_PROFILE",
            "AUTO_REMOTE_ENVIRONMENT_LABEL",
        ):
            for text in (active, active_example, template, template_example):
                with self.subTest(key=key):
                    self.assertIn(key, text)

    def test_runbook_and_handoff_document_remote_evidence_tuple(self) -> None:
        """US-0086 / AC-5: runbook and QA handoff include names-only routing tuple guidance."""
        root = Path(__file__).resolve().parents[1]
        runbook = (root / "docs" / "engineering" / "runbook.md").read_text(
            encoding="utf-8"
        )
        handoff = (root / "handoffs" / "qa_to_verify_work.md").read_text(
            encoding="utf-8"
        )
        for token in (
            "target_id",
            "environment_label",
            "automation_profile",
            "routing_source",
            "secret_surface=names_only",
        ):
            with self.subTest(token=token):
                self.assertIn(token, runbook)
                self.assertIn(token, handoff)


if __name__ == "__main__":
    unittest.main()
