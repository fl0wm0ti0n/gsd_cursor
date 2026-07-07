"""
Work-kind classification + tiered delivery routing per story (US-0118 / DEC-0118).

Deterministic pure-stdlib per-story work-kind classifier that returns
``work_kind ∈ {doc, mini, code}`` plus a recommended delivery mode and phase
plan. Reuses ``dev_environment_lib.classify_touched_files`` (tier A/B/C +
``TIER_C_SKIP_PREFIXES``) via import — never duplicates the tier rules.

The classifier is gated by the ``WORK_KIND_ROUTING`` scratchpad flag
(default ``0`` — zero overhead when off). When ``1`` the classifier is
consulted by ``/intake`` step 5 and ``/auto`` ``resolve_delivery_mode``
step 0 per the L8 precedence chain (explicit ``DELIVERY_MODE`` >
``AUTO_PHASE_*`` > ``WORK_KIND_ROUTING``-derived > current default).

Reason codes (``WORK_KIND_*`` family, R-0106 Q2 LOCKED):
    - ``WORK_KIND_ROUTING_OFF`` — info-only; ``WORK_KIND_ROUTING != "1"``.
    - ``WORK_KIND_DELIVERY_MODE_CONFLICT`` — explicit ``DELIVERY_MODE`` set
      and conflicts with the classifier recommendation.
    - ``WORK_KIND_CLASSIFY_FAILED`` — classifier raised / returned malformed.
    - ``WORK_KIND_UNKNOWN_ROUTE`` — work_kind value not in {doc, mini, code}.
    - ``WORK_KIND_PLAN_COVERAGE_MISSING`` — empty/invalid phase plan.
    - ``WORK_KIND_TIE_BREAK_APPLIED`` — info-only; mixed tiers resolved by
      the highest-tier-wins tie-break (Q1 LOCKED).

Intake evidence schema extension (AC-9 / R-0106 Q9): the intake evidence
JSON gains three optional fields when the classifier runs at ``/intake``
step 5 — ``work_kind``, ``recommended_delivery_mode``,
``work_kind_operator_decision ∈ {accept, override}``. Existing intake
evidence files are NOT modified; only the schema contract is documented
here.
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

# Path bootstrap so the bare ``import dev_environment_lib`` resolves
# whether the script is run from the repo root or as a file path.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

# Q9 LOCKED import contract — import, do NOT duplicate. The tier A/B/C
# classification + skip-prefix single source of truth lives in
# ``dev_environment_lib`` so that drift between the two rule engines is
# impossible by construction.
import dev_environment_lib  # noqa: E402
from dev_environment_lib import (  # noqa: E402
    TIER_C_SKIP_PREFIXES,
    classify_touched_files,
)


# ---------------------------------------------------------------------------
# Enumeration + dataclass (R-0106 Q10 LOCKED signature)
# ---------------------------------------------------------------------------


class WorkKind(str, Enum):
    """Three-tier work-kind enumeration (DEC-0118 §1)."""

    DOC = "doc"
    MINI = "mini"
    CODE = "code"


@dataclass
class WorkKindClassification:
    """
    Result of :func:`classify_work_kind`.

    Fields mirror R-0106 Q10 LOCKED signature. ``rule_trace`` is populated
    only when ``explain=True`` (Q3 LOCKED — ``--explain`` flag).
    """

    work_kind: WorkKind
    recommended_delivery_mode: str
    recommended_phase_plan: List[str]
    rationale: str
    evidence_refs: List[str] = field(default_factory=list)
    rule_trace: List[Tuple[str, str, str]] = field(default_factory=list)
    # Intake-evidence schema extension fields (AC-9). Populated so that
    # consumers (e.g. ``/intake`` step 5) can persist them directly into
    # the intake evidence bundle without re-deriving.
    work_kind_operator_decision: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        """Serialize to a JSON-friendly dict (enum → string)."""
        d = asdict(self)
        d["work_kind"] = self.work_kind.value
        d["rule_trace"] = [list(t) for t in self.rule_trace]
        return d


# ---------------------------------------------------------------------------
# Constants — phase plans + reason codes (R-0106 Q2 LOCKED)
# ---------------------------------------------------------------------------


DOC_PHASE_PLAN: Tuple[str, ...] = ("intake", "execute", "release")
MINI_ULTRA_LEAN_PHASE_PLAN: Tuple[str, ...] = (
    "spec",
    "plan",
    "build+verify",
    "ship",
)
MINI_MEGA_QUICK_PHASE_PLAN: Tuple[str, ...] = ("quick",)
CODE_STANDARD_PHASE_PLAN: Tuple[str, ...] = (
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
)

# Reason-code family (R-0106 Q2 LOCKED + AC-7). ``WORK_KIND_ROUTING_OFF``
# and ``WORK_KIND_TIE_BREAK_APPLIED`` are info-only (not fail-closed); the
# other four are fail-closed and emit remediation guidance in
# ``sprints/Sxxxx/qa-findings.md`` / ``release-findings.md``.
WORK_KIND_ROUTING_OFF = "WORK_KIND_ROUTING_OFF"
WORK_KIND_DELIVERY_MODE_CONFLICT = "WORK_KIND_DELIVERY_MODE_CONFLICT"
WORK_KIND_CLASSIFY_FAILED = "WORK_KIND_CLASSIFY_FAILED"
WORK_KIND_UNKNOWN_ROUTE = "WORK_KIND_UNKNOWN_ROUTE"
WORK_KIND_PLAN_COVERAGE_MISSING = "WORK_KIND_PLAN_COVERAGE_MISSING"
WORK_KIND_TIE_BREAK_APPLIED = "WORK_KIND_TIE_BREAK_APPLIED"

WORK_KIND_REASON_CODES: Tuple[str, ...] = (
    WORK_KIND_ROUTING_OFF,
    WORK_KIND_DELIVERY_MODE_CONFLICT,
    WORK_KIND_CLASSIFY_FAILED,
    WORK_KIND_UNKNOWN_ROUTE,
    WORK_KIND_PLAN_COVERAGE_MISSING,
    WORK_KIND_TIE_BREAK_APPLIED,
)

REASON_CODE_REMEDIATION: Dict[str, str] = {
    WORK_KIND_ROUTING_OFF: (
        "Set WORK_KIND_ROUTING=1 to enable per-story routing; current "
        "behavior unchanged."
    ),
    WORK_KIND_DELIVERY_MODE_CONFLICT: (
        "Explicit DELIVERY_MODE wins per L8 precedence; either unset "
        "DELIVERY_MODE to allow work-kind routing or update the backlog "
        "row; mid-story switch forbidden (DELIVERY_MODE_SWITCH_MID_STORY)."
    ),
    WORK_KIND_CLASSIFY_FAILED: (
        "Re-run /intake with explicit work_kind override; inspect "
        "--explain trace; file bug if rule engine is at fault."
    ),
    WORK_KIND_UNKNOWN_ROUTE: (
        "Re-run classifier; if persistent, set DELIVERY_MODE explicitly "
        "or add AUTO_PHASE_* override; default to standard lifecycle."
    ),
    WORK_KIND_PLAN_COVERAGE_MISSING: (
        "Re-run classifier; if persistent, set DELIVERY_MODE explicitly "
        "or add AUTO_PHASE_* override; default to standard lifecycle."
    ),
    WORK_KIND_TIE_BREAK_APPLIED: (
        "Mixed-tier story resolved by highest-tier-wins tie-break "
        "(code > mini > doc). Inspect --explain trace to override."
    ),
}

# Tier → work_kind mapping (Q1 LOCKED). Mirrors
# ``classify_touched_files`` tier_rank A>B>C where A=code, B=mini, C=doc.
TIER_TO_WORK_KIND: Dict[str, WorkKind] = {
    "A": WorkKind.CODE,
    "B": WorkKind.MINI,
    "C": WorkKind.DOC,
}

# US-0096 mega_quick eligibility signals (L6 LOCKED). The classifier
# recommends ``mega_quick`` only when all of these hold; otherwise it
# falls back to ``ultra_lean`` for the ``mini`` route.
MEGA_QUICK_MAX_AC = 3


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _looks_like_markdown_under_skip_prefix(rel: str) -> bool:
    """Return True for ``*.md`` / ``README*`` under a skip prefix (L5)."""
    norm = rel.replace("\\", "/")
    if not any(norm.startswith(p) for p in TIER_C_SKIP_PREFIXES):
        return False
    base = norm.rsplit("/", 1)[-1]
    return base.lower().endswith(".md") or base.lower().startswith("readme")


def _resolve_work_kind_from_tier(
    tier: Optional[str],
    touched_file_hints: List[str],
    explain: bool,
) -> Tuple[WorkKind, List[Tuple[str, str, str]]]:
    """
    Map the highest matched tier to a work_kind (Q1 LOCKED tie-break).

    ``classify_touched_files`` already returns the *highest* matching tier
    (A>B>C). When the story touches both ``docs/`` and ``src/`` paths the
    highest tier wins — ``code`` > ``mini`` > ``doc``.
    """
    trace: List[Tuple[str, str, str]] = []
    if tier is None:
        # No matched source path. If every touched file is a doc/markdown
        # under a skip prefix → DOC; otherwise fall back to DOC as the
        # conservative default (no runtime surface detected).
        all_doc = bool(touched_file_hints) and all(
            _looks_like_markdown_under_skip_prefix(h) or any(
                h.replace("\\", "/").startswith(p) for p in TIER_C_SKIP_PREFIXES
            )
            for h in touched_file_hints
        )
        if explain:
            trace.append((
                "rule.doc.no_runtime_surface",
                f"tier={tier}, hints={len(touched_file_hints)}",
                "doc" if all_doc else "doc (conservative default)",
            ))
        return WorkKind.DOC, trace

    work_kind = TIER_TO_WORK_KIND.get(tier, WorkKind.DOC)
    if explain:
        trace.append((
            "rule.tier.highest_wins",
            f"tier={tier}",
            work_kind.value,
        ))
        # Tie-break signal: when any touched file is under a skip prefix
        # AND the highest tier is A or B, the highest-tier-wins rule
        # resolved a mixed-tier story (Q1 LOCKED).
        has_skip_prefix = any(
            any(h.replace("\\", "/").startswith(p) for p in TIER_C_SKIP_PREFIXES)
            for h in touched_file_hints
        )
        if has_skip_prefix and tier in ("A", "B"):
            trace.append((
                "rule.tie_break.highest_tier_wins",
                f"tier={tier} + skip-prefix files present",
                work_kind.value,
            ))
    return work_kind, trace


def _resolve_mini_delivery_mode(
    ac_set: List[str],
    component_scope: Optional[str],
    has_companion_dec: bool,
    explain: bool,
) -> Tuple[str, List[Tuple[str, str, str]]]:
    """
    Resolve ``mini`` → ``ultra_lean`` or ``mega_quick`` per US-0096
    eligibility (L6 LOCKED).
    """
    trace: List[Tuple[str, str, str]] = []
    ac_count = len(ac_set)
    single_component = component_scope is not None and "," not in str(component_scope)
    eligible_mega_quick = (
        ac_count <= MEGA_QUICK_MAX_AC
        and not has_companion_dec
        and single_component
    )
    if eligible_mega_quick:
        if explain:
            trace.append((
                "rule.mini.mega_quick_eligible",
                f"ac_count={ac_count}, dec={has_companion_dec}, "
                f"component_scope={component_scope!r}",
                "mega_quick",
            ))
        return "mega_quick", trace
    if explain:
        trace.append((
            "rule.mini.ultra_lean_fallback",
            f"ac_count={ac_count}, dec={has_companion_dec}, "
            f"single_component={single_component}",
            "ultra_lean",
        ))
    return "ultra_lean", trace


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def classify_work_kind(
    story_prose: str,
    acceptance_criteria: List[str],
    touched_file_hints: List[str],
    component_scope: Optional[str] = None,
    *,
    has_companion_dec: bool = False,
    explain: bool = False,
) -> WorkKindClassification:
    """
    Classify a story into ``{doc, mini, code}`` and derive a recommended
    delivery mode + phase plan.

    Inputs are prose + AC set + touched-file hints (names-only, no content
    reads) + component_scope string. Pure stdlib, no network, no ``.env``
    reads, no LLM calls (Q3 LOCKED).

    Parameters mirror R-0106 Q10 LOCKED signature. ``has_companion_dec``
    and ``explain`` are keyword-only extensions surfaced for the
    ``--explain`` CLI trace + the ``mini`` → ``mega_quick`` eligibility
    check.
    """
    if not isinstance(touched_file_hints, list):
        raise TypeError("touched_file_hints must be a list[str]")

    # Reuse the canonical tier classifier (Q9 LOCKED import contract).
    tier = classify_touched_files(touched_file_hints)
    work_kind, trace = _resolve_work_kind_from_tier(
        tier, touched_file_hints, explain
    )

    # Derive delivery mode + phase plan (DEC-0118 §1 mapping table).
    if work_kind is WorkKind.DOC:
        recommended_delivery_mode = "ultra_lean"
        recommended_phase_plan = list(DOC_PHASE_PLAN)
        if explain:
            trace.append((
                "rule.doc.lean_plan",
                f"work_kind={work_kind.value}",
                "ultra_lean + [intake, execute, release]",
            ))
    elif work_kind is WorkKind.MINI:
        recommended_delivery_mode, mini_trace = _resolve_mini_delivery_mode(
            acceptance_criteria, component_scope, has_companion_dec, explain
        )
        trace.extend(mini_trace)
        if recommended_delivery_mode == "mega_quick":
            recommended_phase_plan = list(MINI_MEGA_QUICK_PHASE_PLAN)
        else:
            recommended_phase_plan = list(MINI_ULTRA_LEAN_PHASE_PLAN)
    else:  # WorkKind.CODE
        recommended_delivery_mode = "standard"
        recommended_phase_plan = list(CODE_STANDARD_PHASE_PLAN)
        if explain:
            trace.append((
                "rule.code.standard",
                f"work_kind={work_kind.value}",
                "standard + full canonical lifecycle",
            ))

    rationale = (
        f"work_kind={work_kind.value} derived from "
        f"classify_touched_files tier={tier}; "
        f"recommended_delivery_mode={recommended_delivery_mode}; "
        f"phase_plan={recommended_phase_plan}"
    )

    return WorkKindClassification(
        work_kind=work_kind,
        recommended_delivery_mode=recommended_delivery_mode,
        recommended_phase_plan=recommended_phase_plan,
        rationale=rationale,
        evidence_refs=[],  # names-only; populated by caller if needed
        rule_trace=trace,
    )


# ---------------------------------------------------------------------------
# Self-test (AC-12) — exits 0 on success
# ---------------------------------------------------------------------------


def self_test() -> int:
    """Built-in self-test (AC-12). Exits 0 on success, 1 on failure."""
    failures: List[str] = []

    # DOC route — only docs/ touched files → tier None → DOC → lean plan.
    doc = classify_work_kind(
        "Update README",
        ["AC-1 README updated"],
        ["docs/engineering/runbook.md", "docs/product/backlog.md"],
    )
    if doc.work_kind is not WorkKind.DOC:
        failures.append(f"doc work_kind: expected DOC, got {doc.work_kind}")
    if doc.recommended_phase_plan != list(DOC_PHASE_PLAN):
        failures.append(
            f"doc phase_plan: expected {DOC_PHASE_PLAN}, got {doc.recommended_phase_plan}"
        )
    if doc.recommended_delivery_mode != "ultra_lean":
        failures.append(
            f"doc delivery_mode: expected ultra_lean, got {doc.recommended_delivery_mode}"
        )

    # MINI route — single env.example (tier B) → MINI → ultra_lean fallback
    # (AC count > MEGA_QUICK_MAX_AC).
    mini = classify_work_kind(
        "Tweak nginx config",
        [f"AC-{i}" for i in range(1, 5)],  # 4 ACs > 3 → ultra_lean
        [".env.example"],
        component_scope="web",
    )
    if mini.work_kind is not WorkKind.MINI:
        failures.append(f"mini work_kind: expected MINI, got {mini.work_kind}")
    if mini.recommended_delivery_mode != "ultra_lean":
        failures.append(
            f"mini delivery_mode: expected ultra_lean, got {mini.recommended_delivery_mode}"
        )

    # MINI → mega_quick when eligible (≤3 ACs, single component, no DEC).
    mini_mq = classify_work_kind(
        "Tiny fix",
        ["AC-1", "AC-2"],
        [".env.example"],
        component_scope="web",
    )
    if mini_mq.recommended_delivery_mode != "mega_quick":
        failures.append(
            f"mini mega_quick: expected mega_quick, got {mini_mq.recommended_delivery_mode}"
        )

    # CODE route — package.json (tier A) → CODE → standard.
    code = classify_work_kind(
        "New feature",
        ["AC-1", "AC-2", "AC-3", "AC-4"],
        ["package.json", "src/index.ts"],
    )
    if code.work_kind is not WorkKind.CODE:
        failures.append(f"code work_kind: expected CODE, got {code.work_kind}")
    if code.recommended_delivery_mode != "standard":
        failures.append(
            f"code delivery_mode: expected standard, got {code.recommended_delivery_mode}"
        )

    # Tie-break — mixed docs/ + src/ → CODE (highest tier wins, Q1 LOCKED).
    mixed = classify_work_kind(
        "Feature + docs",
        ["AC-1"],
        ["docs/foo.md", "package.json"],
    )
    if mixed.work_kind is not WorkKind.CODE:
        failures.append(
            f"tie-break: expected CODE (highest tier wins), got {mixed.work_kind}"
        )

    # --explain emits rule_trace.
    explained = classify_work_kind(
        "Tiny fix",
        ["AC-1"],
        [".env.example"],
        component_scope="web",
        explain=True,
    )
    if not explained.rule_trace:
        failures.append("explain=True: rule_trace must be non-empty")

    # Import boundary — classify_touched_files must be imported, not copied.
    from work_kind_classify_lib import classify_touched_files as imported
    if imported is not classify_touched_files:
        failures.append("import boundary: classify_touched_files not reused")

    if failures:
        for f in failures:
            print(f"[WORK_KIND_CLASSIFY_SELF_TEST_FAIL] {f}", file=sys.stderr)
        return 1
    print("[WORK_KIND_CLASSIFY_SELF_TEST_OK]")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description="Work-kind classifier (US-0118 / DEC-0118)."
    )
    p.add_argument(
        "--self-test",
        action="store_true",
        help="Run built-in self-test (AC-12).",
    )
    p.add_argument(
        "--explain",
        action="store_true",
        help="Emit rule_trace in the JSON output (Q3 LOCKED).",
    )
    p.add_argument(
        "--story-prose",
        default="",
        help="Story prose (names-only, no content reads).",
    )
    p.add_argument(
        "--ac",
        nargs="*",
        default=[],
        help="Acceptance criteria list.",
    )
    p.add_argument(
        "--touched",
        nargs="*",
        default=[],
        help="Touched file hints (names-only).",
    )
    p.add_argument(
        "--component-scope",
        default=None,
        help="Component scope string (single component when set without comma).",
    )
    p.add_argument(
        "--has-companion-dec",
        action="store_true",
        help="Story has a companion DEC (disables mega_quick eligibility).",
    )
    args = p.parse_args(argv)

    if args.self_test:
        return self_test()

    result = classify_work_kind(
        story_prose=args.story_prose,
        acceptance_criteria=args.ac,
        touched_file_hints=args.touched,
        component_scope=args.component_scope,
        has_companion_dec=args.has_companion_dec,
        explain=args.explain,
    )
    import json

    print(json.dumps(result.as_dict(), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
