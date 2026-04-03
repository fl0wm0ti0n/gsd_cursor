"""
BUG-0007 / R-0066 regression matrix rows 1–5 for answer_ref topic distinctness.

Invoked from tests/run-tests.ps1 and tests/run-tests.sh (section 26R).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
LIB_DIR = os.path.join(ROOT, "scripts")
VALIDATOR = os.path.join(LIB_DIR, "intake_evidence_validate.py")
BUG0007_FIXTURE = os.path.join(ROOT, "handoffs", "intake_evidence", "BUG-0007-intake-20260403.json")

if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)

import intake_evidence_lib as ie  # noqa: E402


def _small_pack_distinct_answers() -> dict:
    rid = "r0066-row2"
    keys = list(ie.PACK_REQUIRED_KEYS["small-intake-pack"])
    rows = []
    for i, key in enumerate(keys):
        txt = f"short-{key}-{i}"
        rows.append(
            {
                "topic_key": key,
                "satisfied_by": "answer_ref",
                "quoted_user_text": txt,
                "intake_run_id": rid,
                "turn_index": i,
                "ref": ie.build_ie_ref(rid, i, key, "answer_ref", txt),
            }
        )
    return {
        "selected_pack": "small-intake-pack",
        "intake_run_id": rid,
        "asked_topics": keys,
        "missing_topics": [],
        "assumptions_confirmed": "(none)",
        "topic_coverage": rows,
    }


def _delegated_row3() -> dict:
    rid = "r0066-row3"
    keys = list(ie.PACK_REQUIRED_KEYS["small-intake-pack"])
    rows = []
    for i, key in enumerate(keys):
        if key == "done_definition":
            sat = "delegation_ref"
            txt = "Delegate done wording to PO defaults."
        else:
            sat = "answer_ref"
            txt = f"a-{key}"
        row: dict = {
            "topic_key": key,
            "satisfied_by": sat,
            "quoted_user_text": txt,
            "intake_run_id": rid,
            "turn_index": i,
            "ref": ie.build_ie_ref(rid, i, key, sat, txt),
        }
        if sat == "delegation_ref":
            row["delegation_scope"] = "Done criteria wording"
            row["delegation_rationale"] = "User delegated this topic."
            row["delegation_confidence"] = "medium"
        rows.append(row)
    return {
        "selected_pack": "small-intake-pack",
        "intake_run_id": rid,
        "asked_topics": keys,
        "missing_topics": [],
        "assumptions_confirmed": "(none)",
        "topic_coverage": rows,
    }


def _equivalent_evidence_row4() -> dict:
    rid = "r0066-row4"
    keys = list(ie.PACK_REQUIRED_KEYS["small-intake-pack"])
    rows = []
    for i, key in enumerate(keys):
        txt = f"ev-{key}"
        rows.append(
            {
                "topic_key": key,
                "satisfied_by": "answer_ref",
                "quoted_user_text": txt,
                "intake_run_id": rid,
                "turn_index": i,
                "ref": ie.build_ie_ref(rid, i, key, "answer_ref", txt),
            }
        )
    asked = [k for k in keys if k != "done_definition"]
    for row in rows:
        if row["topic_key"] == "done_definition":
            row["evidence_source"] = "equivalent_evidence_ref"
            row["equivalent_evidence_ref"] = "ie:prior-run-0001:7:abcdef1234567890"
            break
    return {
        "selected_pack": "small-intake-pack",
        "intake_run_id": rid,
        "asked_topics": asked,
        "missing_topics": [],
        "assumptions_confirmed": "(none)",
        "topic_coverage": rows,
    }


def _assumption_confirmation_row5() -> dict:
    rid = "r0066-row5"
    keys = list(ie.PACK_REQUIRED_KEYS["small-intake-pack"])
    rows = []
    for i, key in enumerate(keys):
        if key == "done_definition":
            sat = "assumption_confirmation_ref"
            txt = "I accept the stated default for done."
        else:
            sat = "answer_ref"
            txt = f"x-{key}"
        rows.append(
            {
                "topic_key": key,
                "satisfied_by": sat,
                "quoted_user_text": txt,
                "intake_run_id": rid,
                "turn_index": i,
                "ref": ie.build_ie_ref(rid, i, key, sat, txt),
            }
        )
    aquote = "Yes, I confirm the documented assumptions."
    aref = ie.build_ie_ref(
        rid,
        99,
        ie.ASSUMPTIONS_TOPIC_KEY,
        "assumption_confirmation_ref",
        aquote,
    )
    return {
        "selected_pack": "small-intake-pack",
        "intake_run_id": rid,
        "asked_topics": keys,
        "missing_topics": [],
        "assumptions_confirmed": "User confirmed documented assumptions",
        "assumption_confirmation_ref": aref,
        "assumption_confirmation_intake_run_id": rid,
        "assumption_confirmation_turn_index": 99,
        "assumption_confirmation_quoted": aquote,
        "topic_coverage": rows,
    }


def _assert_mode_parity(bundle: dict, *, expected_ok: bool, required_code: str | None = None) -> bool:
    r0 = ie.validate_intake_evidence(bundle, intake_guided_mode=0)
    r1 = ie.validate_intake_evidence(bundle, intake_guided_mode=1)
    if r0.ok != expected_ok or r1.ok != expected_ok:
        print("mode parity outcome mismatch", r0.ok, r1.ok, r0.primary_codes, file=sys.stderr)
        return False
    if r0.primary_codes != r1.primary_codes:
        print("mode parity code mismatch", r0.primary_codes, r1.primary_codes, file=sys.stderr)
        return False
    if required_code and required_code not in r0.primary_codes:
        print("missing required code", required_code, r0.primary_codes, file=sys.stderr)
        return False
    return True


def run_matrix() -> int:
    # Row 1 — BUG-0007 exemplar fixture fails (lib + CLI)
    if not os.path.isfile(BUG0007_FIXTURE):
        print("missing fixture", BUG0007_FIXTURE, file=sys.stderr)
        return 1
    with open(BUG0007_FIXTURE, encoding="utf-8") as f:
        bug_bundle = json.load(f)
    r = ie.validate_intake_evidence(bug_bundle)
    if r.ok or "INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT" not in r.primary_codes:
        print("row1 expected FAIL with INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT", r.primary_codes, file=sys.stderr)
        return 1
    proc = subprocess.run(
        [sys.executable, VALIDATOR, "--file", BUG0007_FIXTURE],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        print("row1 CLI expected non-zero", proc.stdout, proc.stderr, file=sys.stderr)
        return 1
    if "INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT" not in (proc.stderr or ""):
        print("row1 CLI stderr missing code", proc.stderr, file=sys.stderr)
        return 1

    # Row 2 — five distinct short answers
    if not _assert_mode_parity(_small_pack_distinct_answers(), expected_ok=True):
        return 1

    # Row 3 — delegation_ref
    if not _assert_mode_parity(_delegated_row3(), expected_ok=True):
        return 1

    # Row 4 — equivalent_evidence_ref; topic omitted from asked_topics
    if not _assert_mode_parity(_equivalent_evidence_row4(), expected_ok=True):
        return 1

    # Row 5 — assumption_confirmation_ref on a topic row + bundle assumption binding
    if not _assert_mode_parity(_assumption_confirmation_row5(), expected_ok=True):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(run_matrix())
