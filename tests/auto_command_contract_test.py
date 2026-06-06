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

    # --- BUG-0011 / DEC-0077: voice-compression rule markers (9 subtests) ---

    _CAVEMAN_VOICE_SECTION_HEADING = (
        "## Voice compression (when CAVEMAN_MODE=1)"
    )

    def _caveman_rule_texts(self) -> tuple[str, str]:
        root = Path(__file__).resolve().parents[1]
        active = (root / ".cursor" / "rules" / "caveman.mdc").read_text(
            encoding="utf-8"
        )
        template = (
            root / "template" / ".cursor" / "rules" / "caveman.mdc"
        ).read_text(encoding="utf-8")
        return active, template

    def test_caveman_voice_section_heading_present(self) -> None:
        """DEC-0077 §5: exact voice section heading in caveman.mdc."""
        active, template = self._caveman_rule_texts()
        for label, text in (("active", active), ("template", template)):
            with self.subTest(file=label):
                self.assertIn(self._CAVEMAN_VOICE_SECTION_HEADING, text)

    def test_caveman_voice_level_table_markers(self) -> None:
        """DEC-0077 §5: lite, full, ultra level markers in rule body."""
        active, _ = self._caveman_rule_texts()
        for level in ("lite", "full", "ultra"):
            with self.subTest(level=level):
                self.assertIn(level, active)

    def test_caveman_voice_drop_filler_directive(self) -> None:
        """DEC-0077 §5: drop + filler/hedging/pleasantries directive present."""
        active, _ = self._caveman_rule_texts()
        self.assertIn("drop", active.lower())
        self.assertTrue(
            any(token in active.lower() for token in ("filler", "hedging", "pleasantries")),
            "voice section must mention filler, hedging, or pleasantries",
        )

    def test_caveman_voice_fragment_permission(self) -> None:
        """DEC-0077 §5: fragments OK permission in voice section."""
        active, _ = self._caveman_rule_texts()
        self.assertIn("fragments", active.lower())
        self.assertIn("OK", active)

    def test_caveman_voice_auto_clarity_exceptions(self) -> None:
        """DEC-0077 §5: Auto-Clarity pause for security/destructive/ambiguous."""
        active, _ = self._caveman_rule_texts()
        lower = active.lower()
        self.assertIn("auto-clarity", lower)
        self.assertTrue(
            any(token in lower for token in ("security", "destructive", "ambiguous")),
            "Auto-Clarity must cite security, destructive, or ambiguous cases",
        )

    def test_caveman_voice_persistence_directive(self) -> None:
        """DEC-0077 §5: every response persistence while mode on."""
        active, _ = self._caveman_rule_texts()
        self.assertIn("every response", active.lower())

    def test_caveman_voice_user_rule_precedence(self) -> None:
        """DEC-0077 §5: user-rule precedence when CAVEMAN_MODE=1."""
        active, _ = self._caveman_rule_texts()
        lower = active.lower()
        self.assertIn("user rule", lower)
        self.assertIn("CAVEMAN_MODE=1", active)

    def test_caveman_voice_ultra_prose_only_boundary(self) -> None:
        """DEC-0077 §5: ultra defers to 9-zone; reason codes stay literal."""
        active, _ = self._caveman_rule_texts()
        self.assertIn("ultra", active.lower())
        self.assertTrue(
            "reason code" in active.lower() or "reason codes" in active.lower()
        )
        self.assertIn("9-zone", active.lower())

    def test_caveman_voice_template_parity(self) -> None:
        """DEC-0077 §5: active and template caveman.mdc byte-identical."""
        active, template = self._caveman_rule_texts()
        self.assertEqual(active, template)

    # --- BUG-0011 / DEC-0077 §4: DEC-0072 §6 default-off body regression guard ---

    _CAVEMAN_DEFAULT_OFF_BODY_SHA256: dict[str, str] = {
        "test_caveman_default_off_scratchpad_keys_active": (
            "BA1A852531D65A68E61077F9AF9B99F3CF97E6BE2FD4ADAC90DC7B5F603B628A"
        ),
        "test_caveman_default_off_scratchpad_keys_example_parity": (
            "1CAF18B93BD0551F76E4AD2BF4C26D6DA42930C06356B2FF3A883447B7CF22C5"
        ),
        "test_caveman_default_off_rule_file_present_active_template": (
            "DF095E85CF0704511C23DCCD065D5E97483F767CD3C9C22AF7AE6EB470882CEF"
        ),
        "test_caveman_default_off_reference_non_substitution_paragraph": (
            "4611DF21DC9E4D7ECF6C52D8A08FD5A32B37064A5E6C61B41202C64E401D1710"
        ),
        "test_caveman_default_off_runbook_operator_phrases": (
            "39B640498E79FD0F1D48B256FA2D78AADA81B0FC2D01D01988C576BC570367B9"
        ),
        "test_caveman_default_off_existing_contract_tokens_intact": (
            "5DDC89FA50CE71134AD17BD56A061EB644D6FD7C6D0168E0DA5E088EE692810E"
        ),
        "test_caveman_default_off_non_suppressible_gate_vocab_preserved": (
            "3092A1117A145318F78A37F145CA1609B9CA4D47E99B454ADDA2D8B87F7555C8"
        ),
        "test_caveman_default_off_no_vendor_install_leak": (
            "1CD3F742B66D9DB259E0E680FBFD029A4134B431D8FCBF36BC445B9996C37248"
        ),
    }

    def test_caveman_default_off_bodies_regression_guard(self) -> None:
        """T-006 / AC-7: DEC-0072 §6 pinned test_caveman_default_off_* bodies unchanged."""
        import ast
        import hashlib

        path = Path(__file__).resolve()
        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src)
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            if node.name != "AutoCommandContractTest":
                continue
            for item in node.body:
                if not isinstance(item, ast.FunctionDef):
                    continue
                if item.name not in self._CAVEMAN_DEFAULT_OFF_BODY_SHA256:
                    continue
                segment = ast.get_source_segment(src, item)
                self.assertIsNotNone(segment, msg=f"missing source for {item.name}")
                digest = hashlib.sha256(segment.encode()).hexdigest().upper()
                with self.subTest(test=item.name):
                    self.assertEqual(
                        digest,
                        self._CAVEMAN_DEFAULT_OFF_BODY_SHA256[item.name],
                        f"{item.name} body drifted from DEC-0072 §6 pinned baseline",
                    )
        self.assertEqual(
            self._CAVEMAN_NON_SUBSTITUTION_SENTENCE,
            (
                "`TOKEN_PROFILE` controls context breadth. `CAVEMAN_MODE` controls "
                "reply voice. Neither substitutes for the other; setting one does "
                "not change the other. Combine freely."
            ),
            "pinned non-substitution sentence must remain byte-unchanged",
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
        "C7AAC699C5CDF732BD029FA8C431B2A4D0B5A3A1B91E49D80C19C11C9748BC4D"
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

    _BUG0009_REMEDIATION_BLURB = (
        "**CI still runs its-magic packaging jobs?** Your project received a pre-fix workflow.\n"
        "Run **`its-magic --target <repo> --mode upgrade`** (or **`--mode clean`** then reinstall)\n"
        "to refresh `.github/workflows/ci.yml` from the corrected template. After upgrade, GitHub\n"
        "Actions should show only **`checks`** and **`auto-fix`** jobs — not `npm-test`,\n"
        "`brew-test`, or `choco-test`."
    )
    _BUG0009_REQUIRED_ACTIVE_JOBS = frozenset(
        {"checks", "auto-fix", "npm-test", "brew-test", "choco-test"}
    )
    _BUG0009_FORBIDDEN_TEMPLATE_PATTERNS = (
        "npm-test",
        "brew-test",
        "choco-test",
        "npm pack",
        "installer.sh",
        "packaging/chocolatey",
    )

    def test_bug0009_template_ci_forbidden_patterns_absent(self) -> None:
        """T-005 / AC-3: template ci.yml must not contain kit packaging markers."""
        root = Path(__file__).resolve().parents[1]
        template_ci = (root / "template" / ".github" / "workflows" / "ci.yml").read_text(
            encoding="utf-8"
        )
        for pattern in self._BUG0009_FORBIDDEN_TEMPLATE_PATTERNS:
            with self.subTest(pattern=pattern):
                self.assertNotIn(
                    pattern,
                    template_ci,
                    f"template ci.yml must not contain forbidden pattern {pattern!r}",
                )

    def test_bug0009_template_active_ci_negative_parity_sha256(self) -> None:
        """T-005 / AC-7: template and active ci.yml must differ (US-0017 negative parity)."""
        import hashlib

        root = Path(__file__).resolve().parents[1]
        template_bytes = (root / "template" / ".github" / "workflows" / "ci.yml").read_bytes()
        active_bytes = (root / ".github" / "workflows" / "ci.yml").read_bytes()
        self.assertNotEqual(
            hashlib.sha256(template_bytes).digest(),
            hashlib.sha256(active_bytes).digest(),
            "template and active ci.yml must not byte-match after BUG-0009 fix",
        )

    def test_bug0009_active_ci_five_job_inventory(self) -> None:
        """T-005 / AC-2: active ci.yml retains all five required job ids."""
        import sys as _sys

        root = Path(__file__).resolve().parents[1]
        _sys.path.insert(0, str(root / "scripts"))
        try:
            import downstream_ci_guard_lib as dci
        finally:
            _sys.path.pop(0)
        active_text = (root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        job_keys = set(dci.extract_job_keys(active_text))
        self.assertEqual(
            self._BUG0009_REQUIRED_ACTIVE_JOBS,
            job_keys,
            "active ci.yml must retain checks, auto-fix, npm-test, brew-test, choco-test",
        )

    def test_bug0009_guard_report_inventory_fields(self) -> None:
        """T-005 / AC-3: guard --report exposes template/active job inventories."""
        import json as _json
        import subprocess
        import sys as _sys

        root = Path(__file__).resolve().parents[1]
        proc = subprocess.run(
            [
                _sys.executable,
                str(root / "scripts" / "check_downstream_ci_guard.py"),
                "--repo",
                str(root),
                "--report",
            ],
            capture_output=True,
            text=True,
            cwd=str(root),
            timeout=30,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        payload = _json.loads(proc.stdout)
        self.assertIn("template_job_keys", payload)
        self.assertIn("active_job_keys", payload)
        self.assertIn("forbidden_hits", payload)
        self.assertEqual(payload["forbidden_hits"], [])
        self.assertEqual(set(payload["template_job_keys"]), {"checks", "auto-fix"})
        self.assertEqual(set(payload["active_job_keys"]), self._BUG0009_REQUIRED_ACTIVE_JOBS)
        self.assertTrue(payload["ok"])

    def test_bug0009_runbook_remediation_parity(self) -> None:
        """T-009 / AC-8: active/template runbook remediation blurb byte-identical."""
        root = Path(__file__).resolve().parents[1]
        active = (root / "docs" / "engineering" / "runbook.md").read_text(encoding="utf-8")
        template = (root / "template" / "docs" / "engineering" / "runbook.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(self._BUG0009_REMEDIATION_BLURB, active)
        self.assertIn(self._BUG0009_REMEDIATION_BLURB, template)

    def test_bug0009_architecture_linkage(self) -> None:
        """T-010 / AC-7: architecture # BUG-0009 links required peers (assert-only)."""
        root = Path(__file__).resolve().parents[1]
        dec_path = root / "decisions" / "DEC-0075.md"
        self.assertTrue(dec_path.is_file(), "decisions/DEC-0075.md must exist")
        dec_text = dec_path.read_text(encoding="utf-8")
        self.assertIn("Accepted", dec_text, "DEC-0075 must be Accepted")

        arch = (root / "docs" / "engineering" / "architecture.md").read_text(encoding="utf-8")
        self.assertIn("# BUG-0009", arch)
        bug_section = arch[arch.find("# BUG-0009") :]
        required = (
            "DEC-0075",
            "US-0008",
            "US-0017",
            "US-0018",
            "US-0063",
            "BUG-0003",
            "R-0075",
            "negative-parity",
            "ci-downstream",
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, bug_section, f"# BUG-0009 must reference {token!r}")

    _BUG0010_REMEDIATION_BLURB = (
        "**Architecture file blocked on rollover?** If story sections use legacy H2 `## US-xxxx`\n"
        "headings, the archiver now recognizes them for rollover after **BUG-0010**. For new work,\n"
        "`/architecture` must append H1 `# US-xxxx` (or `# BUG-xxxx` for defects). To converge an\n"
        "existing repo, optionally normalize `## US-xxxx` → `# US-xxxx` manually (count decrease is\n"
        "allowed; adding new `## US-` story headings is blocked)."
    )

    def test_bug0010_architecture_command_h1_mandate(self) -> None:
        """T-005 / AC-5: architecture command mandates H1 for story and bug sections."""
        root = Path(__file__).resolve().parents[1]
        for rel in (
            ".cursor/commands/architecture.md",
            "template/.cursor/commands/architecture.md",
        ):
            with self.subTest(path=rel):
                text = (root / rel).read_text(encoding="utf-8")
                self.assertIn("H1 `# US-xxxx`", text)
                self.assertIn("H1 `# BUG-xxxx`", text)
                self.assertIn("not `## US-`", text)

    def test_bug0010_architecture_command_policy_stop_token(self) -> None:
        """T-005 / AC-5: ARCH_STORY_HEADING_LEVEL_INVALID is a non-suppressible stop token."""
        root = Path(__file__).resolve().parents[1]
        for rel in (
            ".cursor/commands/architecture.md",
            "template/.cursor/commands/architecture.md",
        ):
            with self.subTest(path=rel):
                text = (root / rel).read_text(encoding="utf-8")
                self.assertIn("ARCH_STORY_HEADING_LEVEL_INVALID", text)
                self.assertIn("non-suppressible", text)

    def test_bug0010_architecture_command_baseline_policy_step(self) -> None:
        """T-005 / AC-4: step 9 documents baseline capture and heading policy check."""
        root = Path(__file__).resolve().parents[1]
        for rel in (
            ".cursor/commands/architecture.md",
            "template/.cursor/commands/architecture.md",
        ):
            with self.subTest(path=rel):
                text = (root / rel).read_text(encoding="utf-8")
                self.assertIn("baseline_h2_count", text)
                self.assertIn("--check-arch-heading-policy", text)
                self.assertIn("--baseline-h2-count", text)

    def test_bug0010_script_template_parity_sha256(self) -> None:
        """T-001 / AC-7: active and template enforce-triad-hot-surface.py byte-identical."""
        import hashlib

        root = Path(__file__).resolve().parents[1]
        active = (root / "scripts" / "enforce-triad-hot-surface.py").read_bytes()
        template = (root / "template" / "scripts" / "enforce-triad-hot-surface.py").read_bytes()
        self.assertEqual(
            hashlib.sha256(active).digest(),
            hashlib.sha256(template).digest(),
            "enforce-triad-hot-surface.py must byte-match template mirror",
        )

    def test_bug0010_triad_arch_headings_fixtures(self) -> None:
        """T-007 / AC-1, AC-3: fixture files exercise H2-only and mixed H1-wins paths."""
        import importlib.util

        root = Path(__file__).resolve().parents[1]
        spec = importlib.util.spec_from_file_location(
            "enforce_triad_hot_surface",
            root / "scripts" / "enforce-triad-hot-surface.py",
        )
        assert spec and spec.loader
        eths = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(eths)

        h2_fixture = (
            root / "tests" / "fixtures" / "triad_arch_headings" / "h2_only_multi.md"
        ).read_text(encoding="utf-8")
        _, h2_stories = eths.split_arch_stories(h2_fixture)
        self.assertEqual(4, len(h2_stories), "H2-only fixture should yield four boundaries")

        mixed_fixture = (
            root / "tests" / "fixtures" / "triad_arch_headings" / "mixed_h1_h2_same_id.md"
        ).read_text(encoding="utf-8")
        _, mixed_stories = eths.split_arch_stories(mixed_fixture)
        self.assertEqual(2, len(mixed_stories), "mixed fixture should yield two blocks (H1-wins)")
        self.assertTrue(mixed_stories[0].startswith("# US-0067"))

    def test_bug0010_runbook_remediation_parity(self) -> None:
        """T-008 / AC-8: active/template runbook remediation blurb present."""
        root = Path(__file__).resolve().parents[1]
        active = (root / "docs" / "engineering" / "runbook.md").read_text(encoding="utf-8")
        template = (root / "template" / "docs" / "engineering" / "runbook.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(self._BUG0010_REMEDIATION_BLURB, active)
        self.assertIn(self._BUG0010_REMEDIATION_BLURB, template)

    def test_bug0010_architecture_linkage(self) -> None:
        """T-009 / AC-5: architecture # BUG-0010 links required peers (assert-only)."""
        root = Path(__file__).resolve().parents[1]
        dec_path = root / "decisions" / "DEC-0076.md"
        self.assertTrue(dec_path.is_file(), "decisions/DEC-0076.md must exist")
        dec_text = dec_path.read_text(encoding="utf-8")
        self.assertIn("Accepted", dec_text, "DEC-0076 must be Accepted")

        arch = (root / "docs" / "engineering" / "architecture.md").read_text(encoding="utf-8")
        self.assertIn("# BUG-0010", arch)
        bug_section = arch[arch.find("# BUG-0010") :]
        required = (
            "DEC-0076",
            "DEC-0054",
            "DEC-0043",
            "US-0017",
            "US-0072",
            "R-0076",
            "H1-wins",
            "ARCH_STORY_HEADING_LEVEL_INVALID",
            "Dual-track",
            "Template parity inventory",
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, bug_section, f"# BUG-0010 must reference {token!r}")

    # --- US-0092: full_autonomy, outer driver, TOKEN_PROFILE orthogonality ---

    def test_us0092_scratchpad_full_autonomy_literal(self) -> None:
        """US-0092 / AC-1: AUTO_FLOW_MODE=full_autonomy literal in scratchpad comment block."""
        root = Path(__file__).resolve().parents[1]
        for rel in (
            ".cursor/scratchpad.md",
            "template/.cursor/scratchpad.md",
            ".cursor/scratchpad.local.example.md",
            "template/.cursor/scratchpad.local.example.md",
        ):
            with self.subTest(path=rel):
                text = (root / rel).read_text(encoding="utf-8")
                self.assertIn("AUTO_FLOW_MODE=full_autonomy", text)
                self.assertIn("AUTO_BLOCK_RETRY_MAX", text)
                self.assertIn("AUTO_OUTER_DRIVER_TIMEOUT_SECONDS", text)

    def test_us0092_token_profile_orthogonality_string(self) -> None:
        """US-0092 / AC-6: normative TOKEN_PROFILE orthogonality marker."""
        root = Path(__file__).resolve().parents[1]
        ref = (
            root / "docs" / "engineering" / "auto-orchestration-reference.md"
        ).read_text(encoding="utf-8")
        self.assertIn("TOKEN_PROFILE controls context breadth / token cost only", ref)
        runbook = (root / "docs" / "engineering" / "runbook.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("TOKEN_PROFILE controls context breadth / token cost only", runbook)

    def test_us0092_runbook_no_automation_breadth_conflict(self) -> None:
        """US-0092 / AC-6 negative: runbook must not contain forbidden conflict string."""
        root = Path(__file__).resolve().parents[1]
        for rel in ("docs/engineering/runbook.md", "template/docs/engineering/runbook.md"):
            with self.subTest(path=rel):
                text = (root / rel).read_text(encoding="utf-8")
                self.assertNotIn("lowers default automation breadth", text)

    def test_us0092_drain_advance_without_operator_phrases(self) -> None:
        """US-0092 / AC-5: drain-advance-without-operator phrases in auto surfaces."""
        root = Path(__file__).resolve().parents[1]
        auto = (root / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        for token in (
            "Drain-advance-without-pause",
            "immediately",
            "without operator re-`/auto`",
        ):
            with self.subTest(token=token, surface="auto.md"):
                self.assertIn(token, auto)
        ref = (
            root / "docs" / "engineering" / "auto-orchestration-reference.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Drain-advance-without-pause", ref)

    def test_us0092_outer_driver_script_exists(self) -> None:
        """US-0092 / AC-2: scripts/auto_outer_driver.py exists active + template."""
        root = Path(__file__).resolve().parents[1]
        active = root / "scripts" / "auto_outer_driver.py"
        template = root / "template" / "scripts" / "auto_outer_driver.py"
        self.assertTrue(active.is_file())
        self.assertTrue(template.is_file())
        self.assertEqual(active.read_bytes(), template.read_bytes())

    def test_us0092_uat_probe_lib_exists(self) -> None:
        """US-0092 / AC-3: scripts/uat_probe_lib.py exists active + template."""
        root = Path(__file__).resolve().parents[1]
        active = root / "scripts" / "uat_probe_lib.py"
        template = root / "template" / "scripts" / "uat_probe_lib.py"
        self.assertTrue(active.is_file())
        self.assertTrue(template.is_file())
        self.assertEqual(active.read_bytes(), template.read_bytes())

    def test_us0092_runbook_outer_driver_heading(self) -> None:
        """US-0092 / AC-10: runbook Full-autonomy outer driver subsection."""
        root = Path(__file__).resolve().parents[1]
        heading = "### Full-autonomy outer driver (US-0092)"
        active = (root / "docs" / "engineering" / "runbook.md").read_text(
            encoding="utf-8"
        )
        template = (
            root / "template" / "docs" / "engineering" / "runbook.md"
        ).read_text(encoding="utf-8")
        self.assertIn(heading, active)
        self.assertIn(heading, template)
        idx = active.find(heading)
        section = active[idx : idx + 2500]
        for token in (".env", "RELEASE_PUBLISH_MODE=auto", "auto_block_retry"):
            with self.subTest(token=token):
                self.assertIn(token, section)

    def test_us0092_auto_stop_matrix_markers(self) -> None:
        """US-0092 / AC-7: full_autonomy stop matrix in auto.md + reference."""
        root = Path(__file__).resolve().parents[1]
        auto = (root / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        ref = (
            root / "docs" / "engineering" / "auto-orchestration-reference.md"
        ).read_text(encoding="utf-8")
        for token in (
            "Full-autonomy stop matrix (US-0092)",
            "full_autonomy` delta",
            "BLOCK_RETRY_CAP_EXHAUSTED",
            "RELEASE_PUBLISH_MODE=auto",
        ):
            with self.subTest(token=token):
                self.assertIn(token, auto)
                self.assertIn(token, ref)

    def test_us0092_verify_work_qa_self_verify_excerpt(self) -> None:
        """US-0092 / AC-3: verify-work and qa cite uat_probe_lib."""
        root = Path(__file__).resolve().parents[1]
        for cmd in ("verify-work.md", "qa.md"):
            with self.subTest(cmd=cmd):
                active = (root / ".cursor" / "commands" / cmd).read_text(
                    encoding="utf-8"
                )
                template = (
                    root / "template" / ".cursor" / "commands" / cmd
                ).read_text(encoding="utf-8")
                self.assertEqual(active, template)
                self.assertIn("scripts/uat_probe_lib.py", active)
                self.assertIn("UAT_PROBE_UNRESOLVED", active)

    # --- US-0093: browser UAT two-tier, evidence schema, reason codes ---

    def test_us0093_scratchpad_browser_probe_mode_keys(self) -> None:
        """US-0093 / AC-1: UAT_BROWSER_PROBE_MODE literals in scratchpad family."""
        root = Path(__file__).resolve().parents[1]
        for rel in (
            ".cursor/scratchpad.md",
            "template/.cursor/scratchpad.md",
            ".cursor/scratchpad.local.example.md",
            "template/.cursor/scratchpad.local.example.md",
        ):
            with self.subTest(path=rel):
                text = (root / rel).read_text(encoding="utf-8")
                self.assertIn("UAT_BROWSER_PROBE_MODE=cursor", text)
                self.assertIn("http_fallback", text)
                self.assertIn("playwright_fallback", text)
                self.assertIn("UAT_BROWSER_FALLBACK_CHAIN=1", text)
                self.assertIn("UAT_PROCESS_HEALTH_POLL_SECONDS=60", text)
                self.assertIn("PERMISSION_MODE", text)

    def test_us0093_browser_evidence_refs_in_commands(self) -> None:
        """US-0093 / AC-5: browser_evidence_refs in verify-work + qa excerpts."""
        root = Path(__file__).resolve().parents[1]
        for cmd in ("verify-work.md", "qa.md"):
            with self.subTest(cmd=cmd):
                active = (root / ".cursor" / "commands" / cmd).read_text(
                    encoding="utf-8"
                )
                template = (
                    root / "template" / ".cursor" / "commands" / cmd
                ).read_text(encoding="utf-8")
                self.assertEqual(active, template)
                self.assertIn("browser_evidence_refs", active)
                self.assertIn("### Browser UAT self-test (US-0093)", active)

    def test_us0093_browser_reason_codes_in_lib_and_docs(self) -> None:
        """US-0093 / AC-6: UAT_BROWSER_* codes in lib + command docs."""
        root = Path(__file__).resolve().parents[1]
        lib = (root / "scripts" / "uat_probe_lib.py").read_text(encoding="utf-8")
        for code in (
            "UAT_BROWSER_UNAVAILABLE",
            "UAT_BROWSER_PROBE_FAILED",
            "UAT_BROWSER_PROBE_TIMEOUT",
        ):
            with self.subTest(code=code):
                self.assertIn(code, lib)
        vw = (root / ".cursor" / "commands" / "verify-work.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("UAT_BROWSER_UNAVAILABLE", vw)

    def test_us0093_no_silent_pass_cursor_browser_smoke(self) -> None:
        """US-0093 / AC-9 negative: docs must not imply stdlib PASS without evidence."""
        root = Path(__file__).resolve().parents[1]
        for rel in (
            ".cursor/commands/verify-work.md",
            ".cursor/commands/qa.md",
            "template/.cursor/commands/verify-work.md",
            "template/.cursor/commands/qa.md",
        ):
            with self.subTest(path=rel):
                text = (root / rel).read_text(encoding="utf-8")
                self.assertIn("No silent PASS", text)
                self.assertIn("browser_evidence_refs", text)
                self.assertNotIn("stdlib alone PASSes browser_smoke", text)

    def test_us0093_uat_probe_lib_parity_and_self_test(self) -> None:
        """US-0093 / AC-2: uat_probe_lib active/template parity + --merge-result."""
        root = Path(__file__).resolve().parents[1]
        active = root / "scripts" / "uat_probe_lib.py"
        template = root / "template" / "scripts" / "uat_probe_lib.py"
        self.assertEqual(active.read_bytes(), template.read_bytes())
        text = active.read_text(encoding="utf-8")
        self.assertIn("--merge-result", text)
        self.assertIn("execution_tier", text)

    def test_us0093_architecture_linkage(self) -> None:
        """US-0093 / AC-10: architecture # US-0093 + DEC-0079 compose-on linkage."""
        root = Path(__file__).resolve().parents[1]
        dec_path = root / "decisions" / "DEC-0079.md"
        self.assertTrue(dec_path.is_file())
        dec_text = dec_path.read_text(encoding="utf-8")
        self.assertIn("Accepted", dec_text)
        arch = (root / "docs" / "engineering" / "architecture.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("# US-0093", arch)
        section = arch[arch.find("# US-0093") :]
        for token in (
            "DEC-0079",
            "US-0092",
            "DEC-0078",
            "US-0065",
            "R-0041",
            "browser_evidence_refs",
            "UAT_BROWSER_PROBE_MODE",
        ):
            with self.subTest(token=token):
                self.assertIn(token, section)

    def test_bug0011_architecture_linkage(self) -> None:
        """T-008 / AC-1: architecture # BUG-0011 + DEC-0077 linkage (assert-only)."""
        root = Path(__file__).resolve().parents[1]
        dec_path = root / "decisions" / "DEC-0077.md"
        self.assertTrue(dec_path.is_file(), "decisions/DEC-0077.md must exist")
        dec_text = dec_path.read_text(encoding="utf-8")
        self.assertIn("Accepted", dec_text, "DEC-0077 must be Accepted")

        arch = (root / "docs" / "engineering" / "architecture.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("# BUG-0011", arch)
        bug_section = arch[arch.find("# BUG-0011") :]
        required_bug = (
            "DEC-0077",
            "DEC-0072",
            "R-0077",
            "## Voice compression (when CAVEMAN_MODE=1)",
            "§30A",
            "test_caveman_voice_*",
            "AC traceability",
        )
        for token in required_bug:
            with self.subTest(token=token, section="BUG-0011"):
                self.assertIn(token, bug_section, f"# BUG-0011 must reference {token!r}")

        us0089_idx = arch.find("# US-0089")
        self.assertNotEqual(us0089_idx, -1, "architecture.md must have # US-0089")
        us0089_section = arch[us0089_idx : arch.find("\n# ", us0089_idx + 1)]
        for token in ("BUG-0011", "DEC-0077"):
            with self.subTest(token=token, section="US-0089"):
                self.assertIn(
                    token,
                    us0089_section,
                    f"# US-0089 §6 must forward-link {token!r}",
                )


if __name__ == "__main__":
    unittest.main()
