"""
US-0118 contract tests (R-0106 Q4 LOCKED — 12 `test_us0118_*` markers).

Covers:
    - Each work-kind classification (DOC / MINI / CODE).
    - Each recommended phase plan.
    - Default-off zero-overhead behavior.
    - L8 precedence vs explicit DELIVERY_MODE / AUTO_PHASE_*.
    - Operator override path (backlog-row accepted recommendation).
    - Each fail-closed reason code in the WORK_KIND_* family.
    - --explain rule_trace emission.
    - classify_touched_files reuse boundary (Q9 LOCKED import contract).

Pure stdlib pytest — no external deps. Active + `template/` parity.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS_DIR = _REPO_ROOT / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import work_kind_classify_lib as wkc  # noqa: E402
import work_kind_routing_lib as wkr  # noqa: E402
from work_kind_classify_lib import (  # noqa: E402
    WorkKind,
    classify_work_kind,
)
from work_kind_routing_lib import resolve_delivery_mode_with_work_kind  # noqa: E402

# Also import dev_environment_lib to verify the reuse boundary.
import dev_environment_lib  # noqa: E402


# ---------------------------------------------------------------------------
# AC-1, AC-2 — work-kind classification + phase plans
# ---------------------------------------------------------------------------


def test_us0118_doc_kind_routes_to_lean_plan():
    """DOC kind → `[intake, execute, release]` (skip discovery/research/
    architecture/sprint-plan/plan-verify/qa/verify-work)."""
    result = classify_work_kind(
        story_prose="Update README",
        acceptance_criteria=["AC-1 README updated"],
        touched_file_hints=["docs/engineering/runbook.md", "docs/product/backlog.md"],
    )
    assert result.work_kind is WorkKind.DOC
    assert result.recommended_phase_plan == ["intake", "execute", "release"]
    assert result.recommended_delivery_mode == "ultra_lean"


def test_us0118_mini_kind_routes_to_ultra_lean():
    """MINI kind → ultra_lean when mega_quick ineligible (AC count > 3)."""
    result = classify_work_kind(
        story_prose="Tweak nginx config",
        acceptance_criteria=["AC-1", "AC-2", "AC-3", "AC-4"],  # 4 > 3
        touched_file_hints=[".env.example"],
        component_scope="web",
    )
    assert result.work_kind is WorkKind.MINI
    assert result.recommended_delivery_mode == "ultra_lean"
    assert result.recommended_phase_plan == ["spec", "plan", "build+verify", "ship"]


def test_us0118_mini_kind_routes_to_mega_quick_when_eligible():
    """MINI kind + US-0096 eligibility (≤3 ACs, single component, no DEC)
    → mega_quick."""
    result = classify_work_kind(
        story_prose="Tiny fix",
        acceptance_criteria=["AC-1", "AC-2"],  # 2 ≤ 3
        touched_file_hints=[".env.example"],
        component_scope="web",
        has_companion_dec=False,
    )
    assert result.work_kind is WorkKind.MINI
    assert result.recommended_delivery_mode == "mega_quick"
    assert result.recommended_phase_plan == ["quick"]


def test_us0118_code_kind_routes_to_standard():
    """CODE kind (tier A — package.json, or any non-skip source path) →
    standard full lifecycle."""
    result = classify_work_kind(
        story_prose="New feature",
        acceptance_criteria=["AC-1", "AC-2", "AC-3", "AC-4"],
        touched_file_hints=["package.json", "src/index.ts"],
    )
    assert result.work_kind is WorkKind.CODE
    assert result.recommended_delivery_mode == "standard"
    assert result.recommended_phase_plan == [
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
    ]


# ---------------------------------------------------------------------------
# AC-6 — L8 precedence chain
# ---------------------------------------------------------------------------


def test_us0118_explicit_delivery_mode_wins_over_work_kind():
    """L8 precedence: explicit DELIVERY_MODE wins over WORK_KIND_ROUTING-
    derived recommendation even when the story is CODE."""
    mode, plan, reason = resolve_delivery_mode_with_work_kind(
        scratchpad={"WORK_KIND_ROUTING": "1", "DELIVERY_MODE": "ultra_lean"},
        story_prose="code feature",
        ac_set=["AC-1", "AC-2", "AC-3", "AC-4"],
        touched_file_hints=["package.json", "src/index.ts"],
    )
    assert mode == "ultra_lean"
    # Explicit resolution → reason is None (no conflict because no
    # backlog recommendation was supplied to compare against).
    assert reason is None
    assert plan == ["spec", "plan", "build+verify", "ship"]


def test_us0118_auto_phase_wins_over_work_kind():
    """L8 precedence: explicit AUTO_PHASE_* wins over WORK_KIND_ROUTING-
    derived recommendation."""
    mode, plan, reason = resolve_delivery_mode_with_work_kind(
        scratchpad={
            "WORK_KIND_ROUTING": "1",
            "AUTO_PHASE_PLAN": '["spec","plan"]',
        },
        story_prose="code feature",
        ac_set=["AC-1"],
        touched_file_hints=["package.json"],
    )
    assert mode == "standard"
    # Explicit AUTO_PHASE_* resolution → reason is None.
    assert reason is None


# ---------------------------------------------------------------------------
# AC-3, AC-8 — default-off zero-overhead + backward compat
# ---------------------------------------------------------------------------


def test_us0118_routing_off_is_noop():
    """WORK_KIND_ROUTING=0 → zero overhead: returns standard + full plan +
    WORK_KIND_ROUTING_OFF; classifier NOT invoked."""
    mode, plan, reason = resolve_delivery_mode_with_work_kind(
        scratchpad={"WORK_KIND_ROUTING": "0"},
        story_prose="anything",
        ac_set=["AC-1"],
        touched_file_hints=["docs/foo.md"],
    )
    assert mode == "standard"
    assert reason == wkc.WORK_KIND_ROUTING_OFF
    assert plan == wkr.FULL_STANDARD_PLAN


def test_us0118_default_off_zero_overhead():
    """WORK_KIND_ROUTING=0 behavior byte-identical to pre-US-0118
    (standard delivery mode + full canonical phase plan)."""
    # Absent key → treated as "0" (default-off).
    mode1, plan1, reason1 = resolve_delivery_mode_with_work_kind(
        scratchpad={},
        story_prose="anything",
        ac_set=["AC-1"],
        touched_file_hints=["docs/foo.md"],
    )
    mode2, plan2, reason2 = resolve_delivery_mode_with_work_kind(
        scratchpad={"WORK_KIND_ROUTING": "0"},
        story_prose="different",
        ac_set=["AC-99"],
        touched_file_hints=["src/x.ts"],
    )
    assert (mode1, plan1, reason1) == (mode2, plan2, reason2)
    assert mode1 == "standard"
    assert reason1 == wkc.WORK_KIND_ROUTING_OFF


# ---------------------------------------------------------------------------
# AC-8 — reuse boundary (Q9 LOCKED import contract)
# ---------------------------------------------------------------------------


def test_us0118_classify_touched_files_reuse():
    """classify_touched_files imported from dev_environment_lib — NOT
    reimplemented in work_kind_classify_lib (Q9 LOCKED)."""
    # The classifier module must reference the same function object.
    assert wkc.classify_touched_files is dev_environment_lib.classify_touched_files
    assert wkc.TIER_C_SKIP_PREFIXES is dev_environment_lib.TIER_C_SKIP_PREFIXES
    # And the classifier produces tier-consistent results.
    assert wkc.classify_touched_files(["package.json"]) == "A"
    assert wkc.classify_touched_files([".env.example"]) == "B"
    assert wkc.classify_touched_files(["docs/foo.md"]) is None


# ---------------------------------------------------------------------------
# AC-5, AC-9 — intake evidence schema extension
# ---------------------------------------------------------------------------


def test_us0118_intake_evidence_records_work_kind():
    """The classifier output carries the intake-evidence schema extension
    fields (work_kind, recommended_delivery_mode, work_kind_operator_decision)
    so /intake step 5 can persist them directly."""
    result = classify_work_kind(
        story_prose="README update",
        acceptance_criteria=["AC-1"],
        touched_file_hints=["docs/foo.md"],
    )
    out = result.as_dict()
    # work_kind is a string in the serialized form.
    assert out["work_kind"] == "doc"
    assert out["recommended_delivery_mode"] in ("standard", "ultra_lean", "mega_quick")
    # work_kind_operator_decision defaults to None until the operator
    # accept/override gate records a value.
    assert "work_kind_operator_decision" in out


# ---------------------------------------------------------------------------
# AC-7 — fail-closed reason codes (R-0106 Q2 LOCKED)
# ---------------------------------------------------------------------------


def test_us0118_reason_codes_preserved():
    """All WORK_KIND_* reason codes are emitted by the appropriate failure
    modes (R-0106 Q2 LOCKED)."""
    # WORK_KIND_ROUTING_OFF — info-only when flag off.
    _, _, reason = resolve_delivery_mode_with_work_kind(
        scratchpad={"WORK_KIND_ROUTING": "0"},
        story_prose="x",
        ac_set=["AC-1"],
        touched_file_hints=["docs/foo.md"],
    )
    assert reason == wkc.WORK_KIND_ROUTING_OFF

    # WORK_KIND_DELIVERY_MODE_CONFLICT — explicit DELIVERY_MODE conflicts
    # with backlog-row recommendation.
    _, _, reason = resolve_delivery_mode_with_work_kind(
        scratchpad={"WORK_KIND_ROUTING": "1", "DELIVERY_MODE": "ultra_lean"},
        story_prose="x",
        ac_set=["AC-1"],
        touched_file_hints=["package.json"],
        backlog_work_kind="code",
        backlog_recommended_delivery_mode="standard",
    )
    assert reason == wkc.WORK_KIND_DELIVERY_MODE_CONFLICT

    # WORK_KIND_CLASSIFY_FAILED — classifier raises → fail-closed standard.
    _, _, reason = resolve_delivery_mode_with_work_kind(
        scratchpad={"WORK_KIND_ROUTING": "1"},
        story_prose="x",
        ac_set=["AC-1"],
        touched_file_hints=None,  # type: ignore[arg-type]  # provokes TypeError
    )
    assert reason == "WORK_KIND_CLASSIFY_FAILED"

    # All reason codes are present in the WORK_KIND_REASON_CODES tuple.
    expected = {
        "WORK_KIND_ROUTING_OFF",
        "WORK_KIND_DELIVERY_MODE_CONFLICT",
        "WORK_KIND_CLASSIFY_FAILED",
        "WORK_KIND_UNKNOWN_ROUTE",
        "WORK_KIND_PLAN_COVERAGE_MISSING",
        "WORK_KIND_TIE_BREAK_APPLIED",
    }
    assert set(wkc.WORK_KIND_REASON_CODES) == expected
    # Every reason code has remediation guidance.
    for code in wkc.WORK_KIND_REASON_CODES:
        assert code in wkc.REASON_CODE_REMEDIATION
        assert wkc.REASON_CODE_REMEDIATION[code]


# ---------------------------------------------------------------------------
# AC-1 — --explain flag emits rule_trace (Q3 LOCKED)
# ---------------------------------------------------------------------------


def test_us0118_explain_emits_rule_trace():
    """--explain flag (explain=True) emits a non-empty rule_trace list of
    (rule_id, matched_signal, contribution) tuples."""
    result = classify_work_kind(
        story_prose="code feature",
        acceptance_criteria=["AC-1"],
        touched_file_hints=["package.json"],
        explain=True,
    )
    assert result.rule_trace
    for entry in result.rule_trace:
        assert isinstance(entry, tuple)
        assert len(entry) == 3
        rule_id, matched_signal, contribution = entry
        assert isinstance(rule_id, str) and rule_id
        assert isinstance(matched_signal, str) and matched_signal
        assert isinstance(contribution, str) and contribution

    # Without explain, rule_trace is empty.
    no_explain = classify_work_kind(
        story_prose="code feature",
        acceptance_criteria=["AC-1"],
        touched_file_hints=["package.json"],
    )
    assert no_explain.rule_trace == []


# ---------------------------------------------------------------------------
# Q1 LOCKED — tie-break (highest tier wins)
# ---------------------------------------------------------------------------


def test_us0118_tie_break_code_wins():
    """Story touching both docs/ and src/ (mixed tier) → CODE (highest
    tier wins per Q1 LOCKED)."""
    result = classify_work_kind(
        story_prose="Feature + docs",
        acceptance_criteria=["AC-1"],
        touched_file_hints=["docs/foo.md", "package.json"],
    )
    assert result.work_kind is WorkKind.CODE
