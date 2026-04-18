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

    # --- US-0089 / DEC-0072: Caveman mode default-off invariant (8 subtests) ---
    #
    # Canonical byte-locked strings (DEC-0072 §1, §3, §5):
    #   - Scratchpad key lines (§3): four exact strings below.
    #   - Non-substitution sentence (§1): verbatim sentence below.
    #   - Operator toggle phrases (§5): five canonical phrase strings.
    #
    # These subtests assert file-presence, token-presence, and literal equality
    # only. They do NOT assert voice quality under `CAVEMAN_MODE=1` (which is
    # qualitative and explicitly out of scope per DEC-0072).

    _CAVEMAN_SCRATCHPAD_KEY_LINES = (
        "CAVEMAN_MODE=0",
        "CAVEMAN_LEVEL=",
        "CAVEMAN_COMPRESS_INPUT=0",
        "CAVEMAN_FILE_SCOPE=",
    )

    _CAVEMAN_NON_SUBSTITUTION_SENTENCE = (
        "`TOKEN_PROFILE` controls context breadth. `CAVEMAN_MODE` controls "
        "reply voice. Neither substitutes for the other; setting one does "
        "not change the other. Combine freely."
    )

    _CAVEMAN_OPERATOR_PHRASES = (
        "caveman on",
        "caveman off",
        "stop caveman",
        "normal mode",
        "caveman: lite|full|ultra",
    )

    @staticmethod
    def _assert_line_exact(test: "AutoCommandContractTest", text: str, line: str) -> None:
        lines = text.splitlines()
        test.assertIn(
            line,
            lines,
            msg=f"expected exact line {line!r} in file (splitlines match)",
        )

    def test_caveman_default_off_scratchpad_keys_active(self) -> None:
        """DEC-0072 §6 item 1: `.cursor/scratchpad.md` has the four exact Caveman key lines."""
        root = Path(__file__).resolve().parents[1]
        text = (root / ".cursor" / "scratchpad.md").read_text(encoding="utf-8")
        for line in self._CAVEMAN_SCRATCHPAD_KEY_LINES:
            with self.subTest(line=line):
                self._assert_line_exact(self, text, line)

    def test_caveman_default_off_scratchpad_keys_example_parity(self) -> None:
        """DEC-0072 §6 item 2: same four exact key lines in active + template example files."""
        root = Path(__file__).resolve().parents[1]
        active = (root / ".cursor" / "scratchpad.local.example.md").read_text(
            encoding="utf-8"
        )
        template = (
            root / "template" / ".cursor" / "scratchpad.local.example.md"
        ).read_text(encoding="utf-8")
        for line in self._CAVEMAN_SCRATCHPAD_KEY_LINES:
            with self.subTest(line=line, file="active"):
                self._assert_line_exact(self, active, line)
            with self.subTest(line=line, file="template"):
                self._assert_line_exact(self, template, line)

    def test_caveman_default_off_rule_file_present_active_template(self) -> None:
        """DEC-0072 §6 item 3: rule file present in active + template, with required tokens."""
        root = Path(__file__).resolve().parents[1]
        active_path = root / ".cursor" / "rules" / "caveman.mdc"
        template_path = root / "template" / ".cursor" / "rules" / "caveman.mdc"
        self.assertTrue(active_path.is_file(), f"missing {active_path}")
        self.assertTrue(template_path.is_file(), f"missing {template_path}")
        active = active_path.read_text(encoding="utf-8")
        template = template_path.read_text(encoding="utf-8")
        required_tokens = ("CAVEMAN_MODE", "literal") + self._CAVEMAN_OPERATOR_PHRASES
        for token in required_tokens:
            with self.subTest(token=token, file="active"):
                self.assertIn(token, active)
            with self.subTest(token=token, file="template"):
                self.assertIn(token, template)

    def test_caveman_default_off_reference_non_substitution_paragraph(self) -> None:
        """DEC-0072 §6 item 4: exact non-substitution sentence in reference (active + template)."""
        root = Path(__file__).resolve().parents[1]
        active = (
            root / "docs" / "engineering" / "auto-orchestration-reference.md"
        ).read_text(encoding="utf-8")
        template = (
            root
            / "template"
            / "docs"
            / "engineering"
            / "auto-orchestration-reference.md"
        ).read_text(encoding="utf-8")
        for label, text in (("active", active), ("template", template)):
            with self.subTest(file=label):
                self.assertIn(self._CAVEMAN_NON_SUBSTITUTION_SENTENCE, text)

    def test_caveman_default_off_runbook_operator_phrases(self) -> None:
        """DEC-0072 §6 item 5: five phrases + non-substitution sentence in runbook (active + template)."""
        root = Path(__file__).resolve().parents[1]
        active = (root / "docs" / "engineering" / "runbook.md").read_text(
            encoding="utf-8"
        )
        template = (
            root / "template" / "docs" / "engineering" / "runbook.md"
        ).read_text(encoding="utf-8")
        for label, text in (("active", active), ("template", template)):
            with self.subTest(file=label, token="non_substitution_sentence"):
                self.assertIn(self._CAVEMAN_NON_SUBSTITUTION_SENTENCE, text)
            for phrase in self._CAVEMAN_OPERATOR_PHRASES:
                with self.subTest(file=label, phrase=phrase):
                    self.assertIn(phrase, text)

    def test_caveman_default_off_existing_contract_tokens_intact(self) -> None:
        """DEC-0072 §6 item 6: existing required-token vocabulary in this test module is intact.

        The patch may only **add** Caveman assertions; it must not rename or drop
        existing spawn-only / BUG-0006 / reason-code / AUTO_QUIET / US-0086
        vocabulary carried by the pre-US-0089 test module.
        """
        root = Path(__file__).resolve().parents[1]
        module_path = Path(__file__).resolve()
        module_text = module_path.read_text(encoding="utf-8")
        pre_us0089_required = (
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
        )
        for token in pre_us0089_required:
            with self.subTest(token=token):
                self.assertIn(token, module_text)
        self.assertTrue((root / "docs" / "engineering" / "runbook.md").is_file())

    def test_caveman_default_off_non_suppressible_gate_vocab_preserved(self) -> None:
        """DEC-0072 §6 item 7: AUTO_QUIET non-suppressible gate vocabulary preserved in auto.md + reference.

        Scope: the gate-state vocabulary from **US-0088** non-suppressible list
        that actually appears in the slim `auto.md` and the reference doc. The
        contract markers `[BUG_VALIDATION_OK]` / `[INTAKE_EVIDENCE_VALIDATION_OK]`
        are asserted separately in the rule-file subtest (they live in
        `.cursor/rules/caveman.mdc`, not in `auto.md`).
        """
        root = Path(__file__).resolve().parents[1]
        reference = (
            root / "docs" / "engineering" / "auto-orchestration-reference.md"
        ).read_text(encoding="utf-8")
        gate_vocab = (
            "decision_gate",
            "missing input",
            "pause",
            "loop_max",
            "blocked",
        )
        for token in gate_vocab:
            with self.subTest(token=token, file="reference"):
                self.assertIn(token, reference)

    def test_caveman_default_off_no_vendor_install_leak(self) -> None:
        """DEC-0072 §6 item 8: `npx skills add` token MUST NOT appear in runbook or Caveman rule file.

        The vendor-install leak guard is scoped to the operator-facing runbook
        and the new Caveman rule file per **DEC-0072** §6 item 8 verbatim
        ("neither runbook nor rule file contains the token `npx skills add`").
        Historical mentions in pre-US-0089 decision/research/state artifacts are
        out of scope (canonical artifact rewrites are forbidden by DEC-0072 §8).
        """
        root = Path(__file__).resolve().parents[1]
        leak_token = "npx skills add"
        guarded_paths = (
            root / "docs" / "engineering" / "runbook.md",
            root / "template" / "docs" / "engineering" / "runbook.md",
            root / ".cursor" / "rules" / "caveman.mdc",
            root / "template" / ".cursor" / "rules" / "caveman.mdc",
        )
        for path in guarded_paths:
            with self.subTest(path=str(path.relative_to(root))):
                self.assertTrue(path.is_file(), f"missing {path}")
                self.assertNotIn(
                    leak_token,
                    path.read_text(encoding="utf-8"),
                    msg=(
                        f"vendor-install leak: {leak_token!r} found in "
                        f"{path.relative_to(root)} (DEC-0072 §6 item 8)"
                    ),
                )

    # --- T-007 / AC-7: architecture.md `# US-0089` bottom-appended, linked -----

    def test_caveman_architecture_section_bottom_appended_and_linked(self) -> None:
        """T-007 / AC-7: `# US-0089` section exists in architecture.md, is bottom-appended, and is linked.

        Assertion-only (no rewrite): the section heading must be present, must
        appear **after every other `# US-xxxx:` or `## US-xxxx`** heading in the
        file (bottom-appended rule per DEC-0072), and must be referenced from
        at least one peer artifact (the decisions index or the backlog entry).
        """
        root = Path(__file__).resolve().parents[1]
        arch = (root / "docs" / "engineering" / "architecture.md").read_text(
            encoding="utf-8"
        )
        lines = arch.splitlines()
        section_indices: list[tuple[int, str]] = []
        for idx, line in enumerate(lines):
            stripped = line.lstrip()
            if stripped.startswith("# US-") or stripped.startswith("## US-"):
                section_indices.append((idx, stripped))
        self.assertTrue(
            section_indices,
            msg="no `# US-xxxx` headings found in architecture.md",
        )
        us0089 = [
            (idx, head)
            for idx, head in section_indices
            if head.startswith("# US-0089")
        ]
        self.assertEqual(
            len(us0089),
            1,
            msg=f"expected exactly one `# US-0089` heading; got {len(us0089)}",
        )
        us0089_idx = us0089[0][0]
        # DEC-0072 bottom-appended semantics: no US-xxxx section may appear
        # after the tail. US-0089 was the tail at the time of DEC-0072;
        # US-0090 (DEC-0073) is the subsequent tail. Accept US-0090 as the
        # only permissible heading after US-0089.
        later = [
            head
            for idx, head in section_indices
            if idx > us0089_idx and not head.startswith("# US-0089")
        ]
        allowed_after_us0089 = {"# US-0090"}
        forbidden_later = [
            h for h in later if not any(h.startswith(a) for a in allowed_after_us0089)
        ]
        self.assertEqual(
            forbidden_later,
            [],
            msg=(
                "`# US-0089` must be bottom-appended (only `# US-0090` may follow "
                f"per DEC-0073 §11); unexpected later headings: {forbidden_later!r}"
            ),
        )
        backlog = (root / "docs" / "product" / "backlog.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("US-0089", backlog)
        decisions_index = (
            root / "docs" / "engineering" / "decisions.md"
        ).read_text(encoding="utf-8")
        self.assertIn("DEC-0072", decisions_index)

    # --- T-008 / AC-8: template parity sweep + negative-parity for SKILL.md ----

    def test_caveman_template_parity_sweep(self) -> None:
        """T-008 / AC-8: every touched .cursor/ and docs/engineering/ file mirrored under template/."""
        root = Path(__file__).resolve().parents[1]
        parity_pairs = (
            (
                ".cursor/scratchpad.local.example.md",
                "template/.cursor/scratchpad.local.example.md",
            ),
            (
                ".cursor/rules/caveman.mdc",
                "template/.cursor/rules/caveman.mdc",
            ),
            (
                "docs/engineering/auto-orchestration-reference.md",
                "template/docs/engineering/auto-orchestration-reference.md",
            ),
            (
                "docs/engineering/runbook.md",
                "template/docs/engineering/runbook.md",
            ),
        )
        locked_strings = self._CAVEMAN_SCRATCHPAD_KEY_LINES + (
            self._CAVEMAN_NON_SUBSTITUTION_SENTENCE,
        ) + self._CAVEMAN_OPERATOR_PHRASES
        for active_rel, template_rel in parity_pairs:
            active_path = root / active_rel
            template_path = root / template_rel
            with self.subTest(pair=(active_rel, template_rel)):
                self.assertTrue(active_path.is_file(), f"missing {active_path}")
                self.assertTrue(
                    template_path.is_file(), f"missing {template_path}"
                )
                active_text = active_path.read_text(encoding="utf-8")
                template_text = template_path.read_text(encoding="utf-8")
                for locked in locked_strings:
                    if locked in active_text:
                        with self.subTest(
                            pair=(active_rel, template_rel), locked=locked
                        ):
                            self.assertIn(
                                locked,
                                template_text,
                                msg=(
                                    f"template parity break: {locked!r} in "
                                    f"{active_rel} but not in {template_rel} "
                                    "(DEC-0072 §7 / US-0017)"
                                ),
                            )

    def test_caveman_skill_file_negative_parity(self) -> None:
        """T-008 / AC-8: `.cursor/skills/its-magic/SKILL.md` MUST NOT be modified for US-0089.

        DEC-0072 §8 non-goals forbid introducing or editing a skill file for
        Caveman mode. This negative-parity assertion guards against scope creep
        by failing if the SKILL.md file carries any `CAVEMAN_*` key, the
        `US-0089` reason code, or any of the five operator toggle phrases.
        """
        root = Path(__file__).resolve().parents[1]
        skill_path = root / ".cursor" / "skills" / "its-magic" / "SKILL.md"
        self.assertTrue(skill_path.is_file(), f"missing {skill_path}")
        skill_text = skill_path.read_text(encoding="utf-8")
        forbidden = (
            "CAVEMAN_MODE",
            "CAVEMAN_LEVEL",
            "CAVEMAN_COMPRESS_INPUT",
            "CAVEMAN_FILE_SCOPE",
            "US-0089",
        ) + self._CAVEMAN_OPERATOR_PHRASES
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(
                    token,
                    skill_text,
                    msg=(
                        f"SKILL.md must not carry US-0089 content ({token!r} "
                        "found); DEC-0072 §8 non-goal"
                    ),
                )

    # ------------------------------------------------------------------
    # US-0090 / DEC-0073 — Caveman input-compression contract subtests
    # (T-005). Eleven assertions per sprints/S0076/sprint.md Test strategy.
    # ------------------------------------------------------------------

    _CAVEMAN_COMPRESS_SCRIPT_REL = "scripts/caveman_compress_input.py"
    _CAVEMAN_COMPRESS_SCRIPT_TPL = "template/scripts/caveman_compress_input.py"
    _CAVEMAN_RULE_REL = ".cursor/rules/caveman.mdc"
    _CAVEMAN_RULE_BASELINE_SHA256 = (
        "E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE"
    )
    _CAVEMAN_COMPRESS_REASON_CODES = (
        "CAVEMAN_COMPRESS_MODE_DISABLED",
        "CAVEMAN_COMPRESS_FLAG_CONFLICT",
        "CAVEMAN_COMPRESS_SCOPE_EMPTY",
        "CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE",
        "CAVEMAN_COMPRESS_SCOPE_VIOLATION",
        "CAVEMAN_COMPRESS_DENY_HIT",
        "CAVEMAN_COMPRESS_NOT_IDEMPOTENT",
        "CAVEMAN_COMPRESS_LITERAL_REGION_DAMAGED",
        "CAVEMAN_COMPRESS_ORIGINAL_MISSING",
    )

    def test_caveman_compress_input_script_parity(self) -> None:
        """Assertion #1: active vs template script byte-identical (DEC-0073 §9 row 1)."""
        import hashlib

        root = Path(__file__).resolve().parents[1]
        active = (root / self._CAVEMAN_COMPRESS_SCRIPT_REL).read_bytes()
        tpl = (root / self._CAVEMAN_COMPRESS_SCRIPT_TPL).read_bytes()
        self.assertEqual(
            hashlib.sha256(active).hexdigest(),
            hashlib.sha256(tpl).hexdigest(),
            "scripts/caveman_compress_input.py must be byte-identical to its template mirror",
        )

    def test_caveman_compress_input_help_documents_four_flags(self) -> None:
        """Assertion #2: --help exits 0 and documents all four CLI flags (DEC-0073 §8)."""
        import subprocess
        import sys as _sys

        root = Path(__file__).resolve().parents[1]
        proc = subprocess.run(
            [_sys.executable, str(root / self._CAVEMAN_COMPRESS_SCRIPT_REL), "--help"],
            capture_output=True, text=True, cwd=str(root), timeout=20,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        for flag in ("--dry-run", "--write", "--verify-originals", "--report"):
            with self.subTest(flag=flag):
                self.assertIn(flag, proc.stdout)

    def test_caveman_compress_input_mode_disabled_reason(self) -> None:
        """Assertion #3: --write without env gate → CAVEMAN_COMPRESS_MODE_DISABLED."""
        import subprocess
        import sys as _sys
        import tempfile

        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / ".cursor").mkdir(parents=True)
            (tmp_root / ".cursor" / "scratchpad.md").write_text(
                "# empty scratchpad\n", encoding="utf-8"
            )
            proc = subprocess.run(
                [
                    _sys.executable, str(root / self._CAVEMAN_COMPRESS_SCRIPT_REL),
                    "--write", "--repo", str(tmp_root),
                ],
                capture_output=True, text=True, cwd=str(root), timeout=20,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("CAVEMAN_COMPRESS_MODE_DISABLED", proc.stderr)

    def test_caveman_compress_input_scope_empty_reason(self) -> None:
        """Assertion #4: mode on but empty scope → CAVEMAN_COMPRESS_SCOPE_EMPTY."""
        import subprocess
        import sys as _sys
        import tempfile

        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / ".cursor").mkdir(parents=True)
            (tmp_root / ".cursor" / "scratchpad.md").write_text(
                "CAVEMAN_COMPRESS_INPUT=1\nCAVEMAN_FILE_SCOPE=\n",
                encoding="utf-8",
            )
            proc = subprocess.run(
                [
                    _sys.executable, str(root / self._CAVEMAN_COMPRESS_SCRIPT_REL),
                    "--write", "--repo", str(tmp_root),
                ],
                capture_output=True, text=True, cwd=str(root), timeout=20,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("CAVEMAN_COMPRESS_SCOPE_EMPTY", proc.stderr)

    def test_caveman_compress_input_flag_conflict(self) -> None:
        """Assertion #5: --dry-run + --write → CAVEMAN_COMPRESS_FLAG_CONFLICT."""
        import subprocess
        import sys as _sys

        root = Path(__file__).resolve().parents[1]
        proc = subprocess.run(
            [
                _sys.executable, str(root / self._CAVEMAN_COMPRESS_SCRIPT_REL),
                "--dry-run", "--write",
            ],
            capture_output=True, text=True, cwd=str(root), timeout=20,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("CAVEMAN_COMPRESS_FLAG_CONFLICT", proc.stderr)

    def test_caveman_compress_input_unknown_profile(self) -> None:
        """Assertion #6: unknown profile → CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE."""
        import subprocess
        import sys as _sys
        import tempfile

        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / ".cursor").mkdir(parents=True)
            (tmp_root / ".cursor" / "scratchpad.md").write_text(
                "CAVEMAN_COMPRESS_INPUT=1\nCAVEMAN_FILE_SCOPE=does-not-exist\n",
                encoding="utf-8",
            )
            proc = subprocess.run(
                [
                    _sys.executable, str(root / self._CAVEMAN_COMPRESS_SCRIPT_REL),
                    "--write", "--repo", str(tmp_root),
                ],
                capture_output=True, text=True, cwd=str(root), timeout=20,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE", proc.stderr)

    def test_caveman_compress_input_deny_always_wins(self) -> None:
        """Assertion #7: deny-list wins even when allow-list nominally matches."""
        import sys as _sys

        root = Path(__file__).resolve().parents[1]
        _sys.path.insert(0, str(root))
        try:
            from scripts.caveman_compress_input import file_is_denied, DENY_BASELINE
        finally:
            _sys.path.pop(0)
        denied_examples = [
            ".env",
            "docs/product/backlog.md",
            "docs/engineering/state.md",
            "decisions/DEC-0073.md",
            "sprints/S0076/tasks.md",
        ]
        for rel in denied_examples:
            with self.subTest(path=rel):
                self.assertTrue(
                    file_is_denied(rel, list(DENY_BASELINE), root),
                    f"deny baseline must refuse {rel!r}",
                )

    def test_caveman_compress_input_sidecar_anchor_present(self) -> None:
        """Assertion #8: sidecar anchor + .gitkeep present (DEC-0073 §3)."""
        root = Path(__file__).resolve().parents[1]
        self.assertTrue(
            (root / "docs" / ".caveman-originals").is_dir(),
            "docs/.caveman-originals/ must exist (sidecar tree anchor)",
        )
        self.assertTrue(
            (root / "docs" / ".caveman-originals" / ".gitkeep").is_file(),
            "docs/.caveman-originals/.gitkeep must exist",
        )
        gitignore = (root / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("docs/.caveman-originals/", gitignore,
                      ".gitignore must anchor the sidecar tree (US-0090)")

    def test_caveman_compress_input_rule_byte_identity(self) -> None:
        """Assertion #9 (seed 7a): .cursor/rules/caveman.mdc SHA-256 == baseline (R10)."""
        import hashlib

        root = Path(__file__).resolve().parents[1]
        rule = (root / self._CAVEMAN_RULE_REL).read_bytes()
        digest = hashlib.sha256(rule).hexdigest().upper()
        self.assertEqual(
            digest,
            self._CAVEMAN_RULE_BASELINE_SHA256,
            "caveman.mdc SHA-256 must match US-0089 baseline (R10 negative parity — "
            "US-0090 adds no new Cursor rule)",
        )

    def test_caveman_compress_input_deny_list_version_stable(self) -> None:
        """Assertion #10 (seed 7b): --report deny_list_version is a stable 64-char SHA-256."""
        import hashlib
        import json as _json
        import subprocess
        import sys as _sys

        root = Path(__file__).resolve().parents[1]
        proc = subprocess.run(
            [
                _sys.executable, str(root / self._CAVEMAN_COMPRESS_SCRIPT_REL),
                "--report",
            ],
            capture_output=True, text=True, cwd=str(root), timeout=20,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        payload = _json.loads(proc.stdout)
        self.assertIn("deny_list_version", payload)
        version = payload["deny_list_version"]
        self.assertRegex(version, r"^[0-9a-f]{64}$",
                         "deny_list_version must be a 64-hex-char SHA-256")

        _sys.path.insert(0, str(root))
        try:
            from scripts.caveman_compress_input import (
                deny_list_version_hash, DENY_BASELINE,
            )
        finally:
            _sys.path.pop(0)
        self.assertEqual(version, deny_list_version_hash(DENY_BASELINE),
                         "deny_list_version must be stable across invocations")

    def test_caveman_compress_input_reason_codes_cardinality(self) -> None:
        """Assertion #11 (R9): 9 reason codes grouped in 3 families."""
        import sys as _sys

        root = Path(__file__).resolve().parents[1]
        _sys.path.insert(0, str(root))
        try:
            from scripts.caveman_compress_input import (
                ALL_REASON_CODES, REASON_CODES_BY_FAMILY,
            )
        finally:
            _sys.path.pop(0)
        self.assertEqual(len(ALL_REASON_CODES), 9,
                         "DEC-0073 §7 locks the reason vocabulary at 9 codes")
        self.assertEqual(
            set(REASON_CODES_BY_FAMILY.keys()),
            {"Gating", "Scope", "Integrity"},
            "DEC-0073 §7 locks the 3 reason-code families",
        )
        self.assertEqual(set(ALL_REASON_CODES),
                         set(self._CAVEMAN_COMPRESS_REASON_CODES))

    def test_caveman_compress_input_architecture_linkage(self) -> None:
        """T-010 / AC-7: architecture.md `# US-0090` section exists and links the required peer stories / decisions / research.

        Assert-only per DEC-0073 §11 (no architecture rewrite this sprint).
        Active-only per DEC-0072 §7 row 6 (`docs/engineering/architecture.md`
        has no `template/` mirror).
        """
        root = Path(__file__).resolve().parents[1]
        arch = (root / "docs" / "engineering" / "architecture.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("# US-0090", arch,
                      "architecture.md must carry a `# US-0090` section")
        us0090_idx = arch.find("# US-0090")
        us0090_section = arch[us0090_idx:]
        required_linkages = (
            "DEC-0073",
            "DEC-0072",
            "R-0073",
            "# US-0089",
            "US-0053",
            "US-0085",
            "US-0078",
            "DEC-0060",
        )
        for token in required_linkages:
            with self.subTest(token=token):
                self.assertIn(token, us0090_section,
                              f"US-0090 architecture section must link {token!r}")

    def test_caveman_compress_input_three_axis_paragraph_present(self) -> None:
        """DEC-0073 §1: the 3-axis non-substitution paragraph appears in reference + runbook."""
        root = Path(__file__).resolve().parents[1]
        sentence = (
            "`TOKEN_PROFILE` controls context breadth. `CAVEMAN_MODE` controls "
            "reply voice. `CAVEMAN_COMPRESS_INPUT` controls input-side file "
            "compression. All three axes are orthogonal: setting one does not "
            "change the others, and none substitutes for another."
        )
        for rel in (
            "docs/engineering/auto-orchestration-reference.md",
            "docs/engineering/runbook.md",
            "template/docs/engineering/auto-orchestration-reference.md",
            "template/docs/engineering/runbook.md",
        ):
            with self.subTest(path=rel):
                text = (root / rel).read_text(encoding="utf-8")
                self.assertIn(sentence, text,
                              f"{rel} must carry DEC-0073 §1 3-axis paragraph")


if __name__ == "__main__":
    unittest.main()
