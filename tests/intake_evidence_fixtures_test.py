"""
Tier A/B regression for intake evidence validator
(US-0078 / US-0083 / DEC-0060 / DEC-0067 / R-0055 AC-8).

Invoked from tests/run-tests.ps1 and tests/run-tests.sh (§26k).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
LIB_DIR = os.path.join(ROOT, "scripts")
VALIDATOR = os.path.join(LIB_DIR, "intake_evidence_validate.py")

if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)

import intake_evidence_lib as ie  # noqa: E402


def _small_pack_bundle(*, omit_key: str | None = None) -> dict:
    rid = "fixture-p1"
    keys = list(ie.PACK_REQUIRED_KEYS["small-intake-pack"])
    rows = []
    for i, key in enumerate(keys):
        if omit_key and key == omit_key:
            continue
        txt = f"answer-{key}"
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


def _p2_assumption_bundle() -> dict:
    rid = "fixture-p2"
    keys = list(ie.PACK_REQUIRED_KEYS["small-intake-pack"])
    rows = []
    for i, key in enumerate(keys):
        if key == "done_definition":
            sat = "assumption_confirmation_ref"
            txt = "I accept the stated default for done."
        else:
            sat = "answer_ref"
            txt = f"answer-{key}"
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


def _delegated_small_pack_bundle() -> dict:
    rid = "fixture-us0083-delegated"
    keys = list(ie.PACK_REQUIRED_KEYS["small-intake-pack"])
    rows = []
    for i, key in enumerate(keys):
        if key == "done_definition":
            sat = "delegation_ref"
            txt = "Please choose a practical done definition and proceed."
        else:
            sat = "answer_ref"
            txt = f"answer-{key}"
        row = {
            "topic_key": key,
            "satisfied_by": sat,
            "quoted_user_text": txt,
            "intake_run_id": rid,
            "turn_index": i,
            "ref": ie.build_ie_ref(rid, i, key, sat, txt),
        }
        if sat == "delegation_ref":
            row["delegation_scope"] = "Acceptance wording for done criteria only"
            row["delegation_rationale"] = "User opted in to delegate this unresolved topic."
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


def _first_pack_bundle() -> dict:
    rid = "fixture-us0081"
    keys = list(ie.PACK_REQUIRED_KEYS["first-intake-pack"])
    rows = []
    for i, key in enumerate(keys):
        txt = f"answer-{key}"
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
        "selected_pack": "first-intake-pack",
        "intake_run_id": rid,
        "asked_topics": keys,
        "missing_topics": [],
        "assumptions_confirmed": "(none)",
        "topic_coverage": rows,
        "candidate_story_ids": ["US-8101", "US-8102", "US-8103"],
        "plan_area_inventory": [
            {"plan_area_id": "auth", "title": "Authentication"},
            {"plan_area_id": "billing", "title": "Billing"},
            {"plan_area_id": "reporting", "title": "Reporting"},
        ],
        "plan_area_coverage": [
            {"plan_area_id": "auth", "story_ids": ["US-8101"]},
            {"plan_area_id": "billing", "story_ids": ["US-8102"]},
            {"plan_area_id": "reporting", "story_ids": ["US-8103"]},
        ],
        "coverage_complete": True,
    }


def _assert_mode_parity(bundle: dict, *, expected_ok: bool, required_code: str | None = None) -> bool:
    r0 = ie.validate_intake_evidence(bundle, intake_guided_mode=0)
    r1 = ie.validate_intake_evidence(bundle, intake_guided_mode=1)
    if r0.ok != expected_ok or r1.ok != expected_ok:
        print(
            "mode parity outcome mismatch",
            expected_ok,
            r0.ok,
            r1.ok,
            r0.primary_codes,
            r1.primary_codes,
            file=sys.stderr,
        )
        return False
    if r0.primary_codes != r1.primary_codes:
        print("mode parity code mismatch", r0.primary_codes, r1.primary_codes, file=sys.stderr)
        return False
    if required_code and required_code not in r0.primary_codes:
        print("missing required code", required_code, r0.primary_codes, file=sys.stderr)
        return False
    return True


def run_matrix() -> int:
    # P1 — full answers
    r = ie.validate_intake_evidence(_small_pack_bundle())
    if not r.ok:
        print("P1 expected PASS", r.primary_codes, r.diagnostics, file=sys.stderr)
        return 1

    # P2 — assumption path
    r = ie.validate_intake_evidence(_p2_assumption_bundle())
    if not r.ok:
        print("P2 expected PASS", r.primary_codes, r.diagnostics, file=sys.stderr)
        return 1

    # P3 — missing topic row
    r = ie.validate_intake_evidence(_small_pack_bundle(omit_key="done_definition"))
    if r.ok or "INTAKE_REQUIRED_TOPIC_MISSING" not in r.primary_codes:
        print("P3 expected FAIL with INTAKE_REQUIRED_TOPIC_MISSING", r.primary_codes, file=sys.stderr)
        return 1
    if "INTAKE_PERSISTENCE_BLOCKED" not in r.primary_codes:
        print("P3 expected umbrella blocked", file=sys.stderr)
        return 1

    # P4 — false confirmation
    b = _small_pack_bundle()
    b["assumptions_confirmed"] = "yes"
    r = ie.validate_intake_evidence(b)
    if r.ok or "INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED" not in r.primary_codes:
        print("P4 expected ASSUMPTION_CONFIRMATION_REQUIRED", r.primary_codes, file=sys.stderr)
        return 1

    # P5 — asked drift
    b = _small_pack_bundle()
    b["asked_topics"] = [k for k in b["asked_topics"] if k != "done_definition"]
    r = ie.validate_intake_evidence(b)
    if r.ok or "INTAKE_REQUIRED_TOPIC_MISSING" not in r.primary_codes:
        print("P5 expected asked-vs-covered FAIL", r.primary_codes, file=sys.stderr)
        return 1

    # P6 — equivalent evidence accounting suppresses repetitive prompt requirement
    b = _small_pack_bundle()
    b["asked_topics"] = [k for k in b["asked_topics"] if k != "done_definition"]
    for row in b["topic_coverage"]:
        if row["topic_key"] == "done_definition":
            row["evidence_source"] = "equivalent_evidence_ref"
            row["equivalent_evidence_ref"] = "ie:prior-run-0001:7:abcdef1234567890"
            break
    r = ie.validate_intake_evidence(b)
    if not r.ok:
        print("P6 expected PASS with equivalent evidence accounting", r.primary_codes, r.diagnostics, file=sys.stderr)
        return 1

    # Unknown pack
    b = _small_pack_bundle()
    b["selected_pack"] = "unknown-pack"
    r = ie.validate_intake_evidence(b)
    if r.ok or "INTAKE_REQUIRED_PACK_INCOMPLETE" not in r.primary_codes:
        print("unknown pack expected PACK_INCOMPLETE", r.primary_codes, file=sys.stderr)
        return 1

    # US-0083 D1 — delegated unresolved required topic passes in both modes
    if not _assert_mode_parity(_delegated_small_pack_bundle(), expected_ok=True):
        print("US-0083 delegated path expected PASS", file=sys.stderr)
        return 1

    # US-0083 D2 — delegated topic missing required delegation evidence fails deterministically
    b = _delegated_small_pack_bundle()
    for row in b["topic_coverage"]:
        if row["topic_key"] == "done_definition":
            row.pop("delegation_rationale", None)
            break
    if not _assert_mode_parity(
        b,
        expected_ok=False,
        required_code="INTAKE_DELEGATION_EVIDENCE_MISSING",
    ):
        print("US-0083 delegated-missing-evidence expected FAIL", file=sys.stderr)
        return 1

    # US-0083 D3 — delegated topic with invalid delegation confidence fails deterministically
    b = _delegated_small_pack_bundle()
    for row in b["topic_coverage"]:
        if row["topic_key"] == "done_definition":
            row["delegation_confidence"] = "certain"
            break
    if not _assert_mode_parity(
        b,
        expected_ok=False,
        required_code="INTAKE_DELEGATION_EVIDENCE_INVALID",
    ):
        print("US-0083 delegated-invalid-evidence expected FAIL", file=sys.stderr)
        return 1

    # US-0083 D4 — non-delegated unresolved required topic still fails closed
    b = _small_pack_bundle(omit_key="done_definition")
    if not _assert_mode_parity(
        b,
        expected_ok=False,
        required_code="INTAKE_REQUIRED_TOPIC_MISSING",
    ):
        print("US-0083 non-delegated unresolved topic expected FAIL", file=sys.stderr)
        return 1

    # US-0081 C1 — full plan-area coverage pass in both modes
    if not _assert_mode_parity(_first_pack_bundle(), expected_ok=True):
        print("US-0081 full coverage parity expected PASS", file=sys.stderr)
        return 1

    # US-0081 C2 — justified defer pass in both modes
    b = _first_pack_bundle()
    b["plan_area_coverage"][2] = {
        "plan_area_id": "reporting",
        "deferred_ref": "DEC-0064.defer.reporting",
        "deferred_reason": "Phase 2 dependency after initial launch.",
    }
    if not _assert_mode_parity(b, expected_ok=True):
        print("US-0081 deferred coverage parity expected PASS", file=sys.stderr)
        return 1

    # US-0081 C3 — missing plan-area mapping fail-closed in both modes
    b = _first_pack_bundle()
    b["plan_area_coverage"] = [row for row in b["plan_area_coverage"] if row["plan_area_id"] != "billing"]
    b["coverage_complete"] = False
    if not _assert_mode_parity(
        b,
        expected_ok=False,
        required_code="INTAKE_PLAN_COVERAGE_MISSING",
    ):
        print("US-0081 missing mapping parity expected FAIL", file=sys.stderr)
        return 1

    return 0


def main() -> int:
    ie.self_test()
    err = run_matrix()
    if err != 0:
        return err

    if not os.path.isfile(VALIDATOR):
        print("missing intake_evidence_validate.py", file=sys.stderr)
        return 1
    st = subprocess.call([sys.executable, VALIDATOR, "--self-test"], cwd=ROOT)
    if st != 0:
        return st

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
        encoding="utf-8",
        newline="\n",
    ) as tmp:
        json.dump(_small_pack_bundle(), tmp)
        path = tmp.name
    try:
        st = subprocess.call([sys.executable, VALIDATOR, "--file", path], cwd=ROOT)
        if st != 0:
            return st
    finally:
        os.unlink(path)

    print("[INTAKE_EVIDENCE_FIXTURES_OK]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
