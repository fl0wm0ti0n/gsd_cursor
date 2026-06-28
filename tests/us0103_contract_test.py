"""US-0103: Eight `test_us0103_*` contract tests for AI Decision Ledger + Plan Fidelity.

DEC-0103 §7: scratchpad literals, JSONL schema v1, tri-state deviation classifier,
QA cross-check `ledger_findings` block, reason-code inventory, backward composition.

Default-off: `AI_DECISION_LEDGER=0` → zero overhead (no reads/writes).
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
import uuid
from datetime import datetime, timezone
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_lib():
    root = _repo_root()
    scripts_dir = str(root / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import decision_ledger_lib as mod  # noqa: E402
    return mod


def _good_entry(lib, *, phase_id: str = "research", role: str = "tech-lead",
                decision_type: str = "LEDGER_DECISION", plan_fidelity: str = "strict",
                risk_tier: str = "medium") -> dict:
    return {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "orchestrator_run_id": "self-test-run-contract",
        "phase_id": phase_id,
        "role": role,
        "decision_id": str(uuid.uuid4()),
        "decision_type": decision_type,
        "from_artifact": "(none)",
        "to_artifact": "(none)",
        "rationale": "Contract-test rationale.",
        "plan_fidelity": plan_fidelity,
        "cross_model_reviewed": False,
        "risk_tier": risk_tier,
    }


class US0103ScratchpadKeysTest(unittest.TestCase):
    """test_us0103_scratchpad_keys_literals (AC-1)."""

    def test_us0103_scratchpad_keys_literals(self) -> None:
        lib = _load_lib()
        self.assertEqual(lib.AI_DECISION_LEDGER_VALUES, {"0", "1"})
        self.assertEqual(lib.AI_DECISION_LEDGER_DEFAULT, "0")
        self.assertEqual(lib.AUTO_PLAN_FIDELITY_VALUES, {"strict", "relaxed", "extended"})
        self.assertEqual(lib.AUTO_PLAN_FIDELITY_DEFAULT, "strict")

        # Scratchpad files must declare both keys with the correct defaults
        root = _repo_root()
        for pad_path in (root / ".cursor" / "scratchpad.md",
                         root / "template" / ".cursor" / "scratchpad.md"):
            text = pad_path.read_text(encoding="utf-8")
            self.assertIn("AI_DECISION_LEDGER", text, f"missing key in {pad_path}")
            self.assertIn("AUTO_PLAN_FIDELITY", text, f"missing key in {pad_path}")
            self.assertIn("AI_DECISION_LEDGER=0", text, f"default 0 required in {pad_path}")
            self.assertIn("AUTO_PLAN_FIDELITY=strict", text, f"default strict required in {pad_path}")

        # Default-off behavior
        self.assertFalse(lib.is_ledger_enabled(None))
        self.assertFalse(lib.is_ledger_enabled({}))
        self.assertFalse(lib.is_ledger_enabled({"AI_DECISION_LEDGER": "0"}))
        self.assertTrue(lib.is_ledger_enabled({"AI_DECISION_LEDGER": "1"}))

        # resolve_plan_fidelity default path
        self.assertEqual(lib.resolve_plan_fidelity(None).value, "strict")
        self.assertEqual(lib.resolve_plan_fidelity({"AUTO_PLAN_FIDELITY": "relaxed"}).value, "relaxed")
        self.assertEqual(lib.resolve_plan_fidelity({"AUTO_PLAN_FIDELITY": "garbage"}).value, "strict")


class US0103LedgerJsonlSchemaContractTest(unittest.TestCase):
    """test_us0103_ledger_jsonl_schema_contract (AC-2)."""

    def test_us0103_ledger_jsonl_schema_contract(self) -> None:
        lib = _load_lib()
        self.assertEqual(len(lib.LEDGER_SCHEMA_FIELDS), 12)
        for field in ("ts", "orchestrator_run_id", "phase_id", "role",
                      "decision_id", "decision_type", "from_artifact", "to_artifact",
                      "rationale", "plan_fidelity", "cross_model_reviewed", "risk_tier"):
            self.assertIn(field, lib.LEDGER_SCHEMA_FIELDS)

        good = _good_entry(lib)
        ok, err = lib.schema_check(good)
        self.assertTrue(ok, msg=err)
        self.assertIsNone(err)

        # Missing field
        bad = dict(good); del bad["ts"]
        ok_b, err_b = lib.schema_check(bad)
        self.assertFalse(ok_b)
        self.assertIn("ts", err_b)

        # Extra field
        extra = dict(good); extra["unknown"] = "nope"
        ok_e, err_e = lib.schema_check(extra)
        self.assertFalse(ok_e)
        self.assertIn("Unknown fields", err_e)

        # Invalid phase_id
        bad_phase = dict(good); bad_phase["phase_id"] = "not-a-phase"
        ok_p, err_p = lib.schema_check(bad_phase)
        self.assertFalse(ok_p)
        self.assertIn("phase_id", err_p)

        # Invalid UUID
        bad_uuid = dict(good); bad_uuid["decision_id"] = "not-a-uuid"
        ok_u, err_u = lib.schema_check(bad_uuid)
        self.assertFalse(ok_u)

        # Invalid timestamp (no Z)
        bad_ts = dict(good); bad_ts["ts"] = "2026-06-28T10:00:00+00:00"
        ok_t, err_t = lib.schema_check(bad_ts)
        self.assertFalse(ok_t)

        # Invalid enum values
        bad_type = dict(good); bad_type["decision_type"] = "NOT_A_TYPE"
        ok_d, _ = lib.schema_check(bad_type)
        self.assertFalse(ok_d)

        bad_pf = dict(good); bad_pf["plan_fidelity"] = "bogus"
        ok_f, _ = lib.schema_check(bad_pf)
        self.assertFalse(ok_f)


class US0103StrictModeHardStopTest(unittest.TestCase):
    """test_us0103_strict_mode_hard_stop (AC-3)."""

    def test_us0103_strict_mode_hard_stop(self) -> None:
        lib = _load_lib()
        PF = lib.PlanFidelity
        DT = lib.DecisionType

        for kind in ("drop_ac", "reorder_ac"):
            dt, rc, blocking = lib.classify_deviation(PF.STRICT, kind)
            self.assertTrue(blocking, f"strict+{kind} must block")
            self.assertEqual(dt, DT.PLAN_FIDELITY_VIOLATION)
            self.assertEqual(rc, lib.ReasonCode.PLAN_FIDELITY_VIOLATION)

        dt, rc, blocking = lib.classify_deviation(PF.STRICT, "add_scope")
        self.assertTrue(blocking)
        self.assertEqual(dt, DT.PLAN_FIDELITY_SCOPE_GATE)
        self.assertEqual(rc, lib.ReasonCode.PLAN_FIDELITY_SCOPE_GATE)

        # Operator override — non-blocking override recorded in strict
        dt, rc, blocking = lib.classify_deviation(PF.STRICT, "operator_override")
        self.assertFalse(blocking)
        self.assertEqual(dt, DT.PLAN_FIDELITY_OVERRIDE)


class US0103RelaxedModeReorderTest(unittest.TestCase):
    """test_us0103_relaxed_mode_reorder_with_ledger (AC-4)."""

    def test_us0103_relaxed_mode_reorder_with_ledger(self) -> None:
        lib = _load_lib()
        PF = lib.PlanFidelity
        DT = lib.DecisionType

        for kind in ("drop_ac", "reorder_ac"):
            dt, rc, blocking = lib.classify_deviation(PF.RELAXED, kind)
            self.assertFalse(blocking, f"relaxed+{kind} must not block")
            self.assertEqual(dt, DT.PLAN_FIDELITY_REORDER)
            self.assertEqual(rc, lib.ReasonCode.PLAN_FIDELITY_REORDER)

        # relaxed+add_scope still hard-stops (scope gate)
        dt, rc, blocking = lib.classify_deviation(PF.RELAXED, "add_scope")
        self.assertTrue(blocking)
        self.assertEqual(dt, DT.PLAN_FIDELITY_SCOPE_GATE)


class US0103ExtendedModeNonblockingTest(unittest.TestCase):
    """test_us0103_extended_mode_nonblocking (AC-5)."""

    def test_us0103_extended_mode_nonblocking(self) -> None:
        lib = _load_lib()
        PF = lib.PlanFidelity
        DT = lib.DecisionType

        dt, rc, blocking = lib.classify_deviation(PF.EXTENDED, "add_scope")
        self.assertFalse(blocking, "extended+add_scope must not block")
        self.assertEqual(dt, DT.PLAN_FIDELITY_EXTENSION)
        self.assertEqual(rc, lib.ReasonCode.PLAN_FIDELITY_EXTENSION)

        for kind in ("drop_ac", "reorder_ac"):
            dt, rc, blocking = lib.classify_deviation(PF.EXTENDED, kind)
            self.assertFalse(blocking)
            self.assertEqual(dt, DT.PLAN_FIDELITY_REORDER)


class US0103QACrosscheckTest(unittest.TestCase):
    """test_us0103_qa_crosscheck_ledger_findings (AC-6)."""

    def test_us0103_qa_crosscheck_ledger_findings(self) -> None:
        lib = _load_lib()

        # Disabled path → no file read, LEDGER_DISABLED
        block, blocking = lib.build_qa_findings_block(
            Path("handoffs/sovereign_decisions/auto-X.jsonl"), "auto-X",
            scratchpad={"AI_DECISION_LEDGER": "0"},
        )
        self.assertEqual(blocking, lib.ReasonCode.LEDGER_DISABLED)
        self.assertEqual(block["ledger_status"], "disabled")

        with tempfile.TemporaryDirectory() as tmp:
            ledger_path = Path(tmp) / "auto-enabled.jsonl"
            # File missing + ledger enabled → LEDGER_FILE_MISSING
            block2, blocking2 = lib.build_qa_findings_block(
                ledger_path, "auto-enabled",
                scratchpad={"AI_DECISION_LEDGER": "1"},
            )
            self.assertEqual(blocking2, lib.ReasonCode.LEDGER_FILE_MISSING)
            self.assertEqual(block2["ledger_status"], "file_missing")

            # Write a valid entry, read back via build_qa_findings_block
            good = _good_entry(lib, phase_id="execute", role="dev", decision_type="LEDGER_DECISION")
            res = lib.append_entry(ledger_path, good, scratchpad={"AI_DECISION_LEDGER": "1"})
            self.assertTrue(res.success, msg=res.reason_message)
            self.assertTrue(ledger_path.exists())

            block3, blocking3 = lib.build_qa_findings_block(
                ledger_path, "auto-enabled",
                scratchpad={"AI_DECISION_LEDGER": "1"},
            )
            self.assertIsNone(blocking3)
            self.assertEqual(block3["ledger_status"], "ok")
            self.assertEqual(len(block3["ledger_findings"]), 1)
            self.assertEqual(block3["ledger_findings"][0]["decision_id"], good["decision_id"])
            self.assertEqual(block3["ledger_orchestrator_run_id"], "auto-enabled")
            digest = block3["ledger_summary_digest"]
            self.assertIn("violation_count", digest)
            self.assertIn("by_type", digest)
            self.assertIn("by_risk_tier", digest)
            self.assertEqual(digest["total_decisions"], 1)

            # Write a corrupt entry, strict mode → LEDGER_SCHEMA_INVALID
            ledger_path.write_text("not-json\n", encoding="utf-8")
            block4, blocking4 = lib.build_qa_findings_block(
                ledger_path, "auto-enabled",
                scratchpad={"AI_DECISION_LEDGER": "1"},
            )
            self.assertIn(blocking4, (lib.ReasonCode.LEDGER_SCHEMA_INVALID,
                                      lib.ReasonCode.LEDGER_CORRUPT))


class US0103ReasonCodeInventoryTest(unittest.TestCase):
    """test_us0103_reason_code_inventory (AC-8)."""

    def test_us0103_reason_code_inventory(self) -> None:
        lib = _load_lib()
        RC = lib.ReasonCode

        pf_codes = sorted(c.value for c in RC if c.value.startswith("PLAN_FIDELITY_"))
        ledger_codes = sorted(c.value for c in RC if c.value.startswith("LEDGER_"))
        self.assertEqual(pf_codes, [
            "PLAN_FIDELITY_EXTENSION",
            "PLAN_FIDELITY_OVERRIDE",
            "PLAN_FIDELITY_REORDER",
            "PLAN_FIDELITY_SCOPE_GATE",
            "PLAN_FIDELITY_VIOLATION",
        ])
        self.assertEqual(sorted(ledger_codes), [
            "LEDGER_APPEND_FAILED",
            "LEDGER_CORRUPT",
            "LEDGER_DISABLED",
            "LEDGER_FILE_MISSING",
            "LEDGER_READ_BOUND",
            "LEDGER_SCHEMA_INVALID",
        ])
        self.assertEqual(len(RC), 11)

        DT = lib.DecisionType
        self.assertEqual(len(DT), 9)


class US0103US0070ComposeNoSchemaChangeTest(unittest.TestCase):
    """test_us0103_us0070_compose_no_schema_change (AC-7 / DEC-0103 §9).

    US-0103 must NOT mutate the following artifacts:
    - `handoffs/resolved_phase_plan.json` (US-0070)
    - `sprints/*/phase-role-transition.json` (US-0069)
    - `sprints/*/phase-isolation.json` (US-0048)
    It must only append to `handoffs/sovereign_decisions/<run>.jsonl`.
    """

    _PROTECTED_FILES = {
        "handoffs/resolved_phase_plan.json": ("Phase selection policy — US-0070"),
        "sprints/S0001/phase-role-transition.json": ("Phase role enforcement — US-0069"),
        "sprints/S0001/phase-isolation.json": ("Isolation evidence — US-0048"),
        "sprints/S0001/phase-context.json": ("Phase context — US-0048"),
    }

    def test_us0103_us0070_compose_no_schema_change(self) -> None:
        lib = _load_lib()
        root = _repo_root()

        # 1. Library contract invariant: all paths built by the lib live under
        #    handoffs/sovereign_decisions/<run>.jsonl — never under phase-plan,
        #    phase-role-transition, phase-isolation, or phase-context files.
        canonical = lib.resolve_ledger_path("auto-20260628-01", root)
        self.assertEqual(canonical.parent.name, "sovereign_decisions")
        self.assertEqual(canonical.parent.parent.name, "handoffs")

        # 2. `append_entry` when enabled only writes to handoffs/sovereign_decisions/
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            ledger_path = tmp_root / "handoffs" / "sovereign_decisions" / "auto-x.jsonl"
            good = _good_entry(lib, phase_id="execute", role="dev")
            res = lib.append_entry(ledger_path, good, scratchpad={"AI_DECISION_LEDGER": "1"})
            self.assertTrue(res.success, msg=res.reason_message)
            # No protected file written under the tmp root
            rels = {str(p.relative_to(tmp_root)).replace("\\", "/")
                    for p in tmp_root.rglob("*") if p.is_file()}
            for protected in self._PROTECTED_FILES:
                self.assertNotIn(protected, rels, f"US-0103 wrote into {protected}")
            self.assertIn("handoffs/sovereign_decisions/auto-x.jsonl", rels)

        # 3. schema v1 field inventory frozen: 12 fields, no `plan_integrity_v2` additions.
        #    plan_integrity table lives in plan-verify.json (US-0070), NOT in ledger schema.
        self.assertNotIn("plan_integrity", lib.LEDGER_SCHEMA_FIELDS)
        self.assertNotIn("plan_integrity_v2", lib.LEDGER_SCHEMA_FIELDS)

        # 4. Phase selection policy (US-0070) fields untouched:
        #    CANONICAL_PHASE_IDS + CANONICAL_ROLES match DEC-0086 / DEC-0051.
        self.assertIn("execute", lib.CANONICAL_PHASE_IDS)
        self.assertIn("qa", lib.CANONICAL_PHASE_IDS)
        self.assertIn("architecture", lib.CANONICAL_PHASE_IDS)
        self.assertIn("dev", lib.CANONICAL_ROLES)
        self.assertIn("qa", lib.CANONICAL_ROLES)


if __name__ == "__main__":
    unittest.main()
