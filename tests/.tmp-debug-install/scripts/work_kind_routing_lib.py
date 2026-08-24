"""
Work-kind routing resolver (US-0118 / DEC-0118).

Resolves ``(delivery_mode, phase_plan, reason_code)`` from the merged
scratchpad + story signals using the **L8 precedence chain** (LOCKED):

1. **``start-from=<phase>``** — always wins (intersects with whatever
   plan is active per DEC-0052 §2.5; handled by the caller).
2. **Explicit ``DELIVERY_MODE``** (US-0096 / DEC-0082) — argv
   ``delivery-mode=`` > backlog row ``delivery_mode`` (when
   ``AUTO_DELIVERY_ROUTING=backlog_then_scratchpad``) > scratchpad
   ``DELIVERY_MODE``.
3. **Explicit ``AUTO_PHASE_*``** (US-0070 / DEC-0052) —
   ``AUTO_PHASE_PLAN`` / ``AUTO_PHASE_EXCLUDE`` / ``AUTO_PHASE_INCLUDE``
   / ``AUTO_PHASE_PROFILE``.
4. **``WORK_KIND_ROUTING``-derived ``recommended_delivery_mode``** — only
   when ``WORK_KIND_ROUTING=1`` AND the backlog row carries ``work_kind``
   AND higher-precedence keys are unset.
5. **Current default lifecycle** — full DEC-0052 chain; ``standard``
   delivery mode.

Zero-overhead-when-off (Q8 LOCKED): when ``WORK_KIND_ROUTING != "1"`` the
resolver early-returns ``(standard, full_plan, "WORK_KIND_ROUTING_OFF")``
without invoking :func:`classify_work_kind`. Existing backlog rows
without ``work_kind``/``recommended_delivery_mode`` route via current
``DELIVERY_MODE``/``AUTO_PHASE_*`` precedence (no forced reclassification,
no schema-migration).
"""

from __future__ import annotations

import os
import sys
from typing import List, Optional, Tuple

# Path bootstrap so the bare ``import work_kind_classify_lib`` resolves
# whether the script is run from the repo root or as a file path.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

import work_kind_classify_lib  # noqa: E402
from work_kind_classify_lib import (  # noqa: E402
    CODE_STANDARD_PHASE_PLAN,
    WorkKind,
    WorkKindClassification,
    WORK_KIND_DELIVERY_MODE_CONFLICT,
    WORK_KIND_ROUTING_OFF,
    classify_work_kind,
)


# Reason code emitted by this resolver when both ``WORK_KIND_ROUTING=1``
# and explicit ``DELIVERY_MODE`` are set (the explicit value wins, but the
# conflict is surfaced for diagnostics).
WORK_KIND_ROUTING_CONFLICT_INFO = "WORK_KIND_DELIVERY_MODE_CONFLICT"

# Reason code emitted when the classifier-derived delivery mode is
# actually applied (info-only).
WORK_KIND_ROUTING_APPLIED = "WORK_KIND_ROUTING_APPLIED"

FULL_STANDARD_PLAN: List[str] = list(CODE_STANDARD_PHASE_PLAN)


def _is_set(value: Optional[str]) -> bool:
    """Return True when ``value`` is a non-empty string after strip."""
    return value is not None and bool(str(value).strip())


def _has_auto_phase_keys(scratchpad: dict) -> bool:
    """Return True when any ``AUTO_PHASE_*`` key is non-empty."""
    for key in (
        "AUTO_PHASE_PLAN",
        "AUTO_PHASE_EXCLUDE",
        "AUTO_PHASE_INCLUDE",
        "AUTO_PHASE_PROFILE",
    ):
        if _is_set(scratchpad.get(key)):
            return True
    return False


def resolve_delivery_mode_with_work_kind(
    scratchpad: dict,
    story_prose: str,
    ac_set: List[str],
    touched_file_hints: List[str],
    component_scope: Optional[str] = None,
    *,
    backlog_work_kind: Optional[str] = None,
    backlog_recommended_delivery_mode: Optional[str] = None,
    has_companion_dec: bool = False,
) -> Tuple[str, List[str], Optional[str]]:
    """
    Resolve ``(delivery_mode, phase_plan, reason_code)`` from scratchpad +
    story signals per the L8 precedence chain.

    Parameters
    ----------
    scratchpad:
        Merged scratchpad dict (Model B: local > baseline > example).
    story_prose, ac_set, touched_file_hints, component_scope:
        Forwarded to :func:`classify_work_kind` when routing is enabled.
    backlog_work_kind, backlog_recommended_delivery_mode:
        Optional backlog-row fields set at intake (AC-4). When present
        and ``WORK_KIND_ROUTING=1`` the classifier is *not* re-run — the
        backlog value is trusted as the operator-accepted recommendation.
    has_companion_dec:
        Forwarded to the classifier (affects ``mini`` → ``mega_quick``
        eligibility).

    Returns
    -------
    Tuple ``(delivery_mode, phase_plan, reason_code)`` where
    ``reason_code`` is ``None`` on a clean explicit resolution, an
    info-code (``WORK_KIND_ROUTING_OFF`` / ``WORK_KIND_ROUTING_APPLIED``)
    on a derived resolution, or a fail-closed ``WORK_KIND_*`` code on
    conflict.
    """
    routing_flag = (scratchpad.get("WORK_KIND_ROUTING") or "0").strip()
    if routing_flag != "1":
        # Q8 LOCKED zero-overhead-when-off — early return WITHOUT
        # invoking the classifier. Byte-identical to pre-US-0118 behavior.
        return ("standard", list(FULL_STANDARD_PLAN), WORK_KIND_ROUTING_OFF)

    explicit_delivery_mode = (scratchpad.get("DELIVERY_MODE") or "").strip()
    explicit_auto_phase = _has_auto_phase_keys(scratchpad)

    # L8 precedence: explicit DELIVERY_MODE wins (2) > AUTO_PHASE_* (3) >
    # WORK_KIND_ROUTING-derived (4) > default (5).
    if _is_set(explicit_delivery_mode):
        # If the classifier would have recommended a different mode, emit
        # the conflict reason code (info for diagnostics; explicit still
        # wins per L8). The classifier is NOT run when the backlog row
        # already carries a recommendation — we compare against that.
        if (
            _is_set(backlog_recommended_delivery_mode)
            and backlog_recommended_delivery_mode != explicit_delivery_mode
        ):
            return (
                explicit_delivery_mode,
                _phase_plan_for_delivery_mode(explicit_delivery_mode),
                WORK_KIND_ROUTING_CONFLICT_INFO,
            )
        return (
            explicit_delivery_mode,
            _phase_plan_for_delivery_mode(explicit_delivery_mode),
            None,
        )

    if explicit_auto_phase:
        # Explicit AUTO_PHASE_* wins over work-kind-derived (L8 #3 > #4).
        # The caller materializes the actual plan via DEC-0052; we return
        # the standard delivery mode + full plan as the base.
        return ("standard", list(FULL_STANDARD_PLAN), None)

    # WORK_KIND_ROUTING-derived path (L8 #4). Use the backlog row's
    # accepted recommendation when present; otherwise classify now.
    if _is_set(backlog_recommended_delivery_mode) and _is_set(backlog_work_kind):
        delivery_mode = backlog_recommended_delivery_mode
        phase_plan = _phase_plan_for_delivery_mode(delivery_mode)
        return (delivery_mode, phase_plan, WORK_KIND_ROUTING_APPLIED)

    try:
        classification: WorkKindClassification = classify_work_kind(
            story_prose=story_prose,
            acceptance_criteria=ac_set,
            touched_file_hints=touched_file_hints,
            component_scope=component_scope,
            has_companion_dec=has_companion_dec,
        )
    except Exception:
        # WORK_KIND_CLASSIFY_FAILED — fail closed to standard lifecycle.
        return ("standard", list(FULL_STANDARD_PLAN), "WORK_KIND_CLASSIFY_FAILED")

    if not classification.recommended_phase_plan:
        return (
            "standard",
            list(FULL_STANDARD_PLAN),
            "WORK_KIND_PLAN_COVERAGE_MISSING",
        )

    return (
        classification.recommended_delivery_mode,
        list(classification.recommended_phase_plan),
        WORK_KIND_ROUTING_APPLIED,
    )


def _phase_plan_for_delivery_mode(delivery_mode: str) -> List[str]:
    """Map a delivery mode to its canonical phase plan (DEC-0082 table)."""
    if delivery_mode == "ultra_lean":
        return ["spec", "plan", "build+verify", "ship"]
    if delivery_mode == "mega_quick":
        return ["quick"]
    # standard (or unknown — fall back to standard full lifecycle).
    return list(FULL_STANDARD_PLAN)


# ---------------------------------------------------------------------------
# Self-test (AC-12)
# ---------------------------------------------------------------------------


def self_test() -> int:
    """Built-in self-test. Exits 0 on success, 1 on failure."""
    failures: List[str] = []

    # WORK_KIND_ROUTING=0 → zero overhead, no classifier call.
    mode, plan, reason = resolve_delivery_mode_with_work_kind(
        scratchpad={"WORK_KIND_ROUTING": "0"},
        story_prose="anything",
        ac_set=["AC-1"],
        touched_file_hints=["docs/foo.md"],
    )
    if mode != "standard":
        failures.append(f"routing-off mode: expected standard, got {mode}")
    if reason != WORK_KIND_ROUTING_OFF:
        failures.append(f"routing-off reason: expected {WORK_KIND_ROUTING_OFF}, got {reason}")
    if plan != FULL_STANDARD_PLAN:
        failures.append("routing-off plan: expected full standard plan")

    # Explicit DELIVERY_MODE wins over WORK_KIND_ROUTING (L8 #2 > #4).
    mode, plan, reason = resolve_delivery_mode_with_work_kind(
        scratchpad={"WORK_KIND_ROUTING": "1", "DELIVERY_MODE": "ultra_lean"},
        story_prose="code feature",
        ac_set=["AC-1", "AC-2", "AC-3", "AC-4"],
        touched_file_hints=["package.json", "src/index.ts"],
    )
    if mode != "ultra_lean":
        failures.append(f"explicit-delivery mode: expected ultra_lean, got {mode}")
    if reason is not None:
        failures.append(f"explicit-delivery reason: expected None, got {reason}")

    # Conflict — backlog recommends standard, explicit DELIVERY_MODE=ultra_lean.
    mode, plan, reason = resolve_delivery_mode_with_work_kind(
        scratchpad={"WORK_KIND_ROUTING": "1", "DELIVERY_MODE": "ultra_lean"},
        story_prose="code feature",
        ac_set=["AC-1"],
        touched_file_hints=["package.json"],
        backlog_work_kind="code",
        backlog_recommended_delivery_mode="standard",
    )
    if mode != "ultra_lean":
        failures.append(f"conflict mode: expected ultra_lean (explicit wins), got {mode}")
    if reason != WORK_KIND_ROUTING_CONFLICT_INFO:
        failures.append(
            f"conflict reason: expected {WORK_KIND_ROUTING_CONFLICT_INFO}, got {reason}"
        )

    # AUTO_PHASE_* wins over WORK_KIND_ROUTING (L8 #3 > #4).
    mode, plan, reason = resolve_delivery_mode_with_work_kind(
        scratchpad={"WORK_KIND_ROUTING": "1", "AUTO_PHASE_PLAN": '["spec","plan"]'},
        story_prose="code feature",
        ac_set=["AC-1"],
        touched_file_hints=["package.json"],
    )
    if mode != "standard":
        failures.append(f"auto-phase mode: expected standard, got {mode}")
    if reason is not None:
        failures.append(f"auto-phase reason: expected None, got {reason}")

    # WORK_KIND_ROUTING=1 + doc story → DOC route (ultra_lean + lean plan).
    mode, plan, reason = resolve_delivery_mode_with_work_kind(
        scratchpad={"WORK_KIND_ROUTING": "1"},
        story_prose="README update",
        ac_set=["AC-1"],
        touched_file_hints=["docs/engineering/runbook.md"],
    )
    if mode != "ultra_lean":
        failures.append(f"doc-derived mode: expected ultra_lean, got {mode}")
    if plan != ["intake", "execute", "release"]:
        failures.append(f"doc-derived plan: expected lean plan, got {plan}")
    if reason != WORK_KIND_ROUTING_APPLIED:
        failures.append(
            f"doc-derived reason: expected {WORK_KIND_ROUTING_APPLIED}, got {reason}"
        )

    # Backlog-row accepted recommendation is trusted (no re-classify).
    mode, plan, reason = resolve_delivery_mode_with_work_kind(
        scratchpad={"WORK_KIND_ROUTING": "1"},
        story_prose="ignored",
        ac_set=["AC-1"],
        touched_file_hints=["package.json"],
        backlog_work_kind="doc",
        backlog_recommended_delivery_mode="ultra_lean",
    )
    if mode != "ultra_lean":
        failures.append(f"backlog-accept mode: expected ultra_lean, got {mode}")
    if reason != WORK_KIND_ROUTING_APPLIED:
        failures.append(
            f"backlog-accept reason: expected {WORK_KIND_ROUTING_APPLIED}, got {reason}"
        )

    if failures:
        for f in failures:
            print(f"[WORK_KIND_ROUTING_SELF_TEST_FAIL] {f}", file=sys.stderr)
        return 1
    print("[WORK_KIND_ROUTING_SELF_TEST_OK]")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(
        description="Work-kind routing resolver (US-0118 / DEC-0118)."
    )
    p.add_argument("--self-test", action="store_true", help="Run built-in self-test.")
    args = p.parse_args(argv)
    if args.self_test:
        return self_test()
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
