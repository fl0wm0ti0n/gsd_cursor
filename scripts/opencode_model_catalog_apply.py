#!/usr/bin/env python3
"""
OpenCode model catalog materializer (US-0123 / DEC-0123).

Reads `.opencode/model-catalog.local.json` at the install target and injects
`model: <provider/slug>` into installed `.opencode/agents/<role>.md` YAML
frontmatter only. Never writes to `template/` or reads `.cursor/` catalogs.

Exit codes:
  0 — success or catalog absent (no-op)
  1 — validation failure (see reason codes on stderr)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

OPENCODE_ROLE_KEYS = (
    "po",
    "tech-lead",
    "dev",
    "qa",
    "release",
    "curator",
    "security",
    "auto",
)

REASON_OPENCODE_MODEL_SLUG_UNKNOWN = "OPENCODE_MODEL_SLUG_UNKNOWN"
REASON_MODEL_CATALOG_INVALID = "MODEL_CATALOG_INVALID"
SCOPE_TAG = "opencode-catalog"

PLACEHOLDER_SLUG_RE = re.compile(r"^<.*>$")


def is_unknown_slug(slug: str) -> bool:
    if not slug or not str(slug).strip():
        return True
    s = str(slug).strip()
    if PLACEHOLDER_SLUG_RE.match(s):
        return True
    if "<your-" in s:
        return True
    return False


def validate_opencode_catalog_data(data: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["catalog root must be a JSON object"]
    if "schema_version" not in data:
        errors.append("missing schema_version")
    providers = data.get("providers")
    if not isinstance(providers, dict):
        errors.append("missing or invalid providers object")
    roles = data.get("roles")
    if not isinstance(roles, dict):
        errors.append("missing or invalid roles object")
    else:
        for role in OPENCODE_ROLE_KEYS:
            if role not in roles:
                errors.append(f"missing role key: {role}")
    return errors


def parse_role_assignment(value: str, providers: dict) -> tuple[str | None, str | None, str | None]:
    """Return (provider, slug, error_reason) — error_reason set when fail-closed."""
    if not isinstance(value, str):
        return None, None, REASON_OPENCODE_MODEL_SLUG_UNKNOWN
    text = value.strip()
    if "/" not in text:
        return None, None, REASON_OPENCODE_MODEL_SLUG_UNKNOWN
    provider, slug = text.split("/", 1)
    provider = provider.strip()
    slug = slug.strip()
    if not provider or not isinstance(providers, dict) or provider not in providers:
        return None, None, REASON_OPENCODE_MODEL_SLUG_UNKNOWN
    if is_unknown_slug(slug):
        return None, None, REASON_OPENCODE_MODEL_SLUG_UNKNOWN
    return provider, slug, None


def inject_model_frontmatter(content: str, model_value: str) -> str:
    if not content.startswith("---"):
        raise ValueError("agent file missing opening frontmatter fence")
    rest = content[3:]
    if rest.startswith("\r\n"):
        rest = rest[2:]
    elif rest.startswith("\n"):
        rest = rest[1:]
    close_idx = rest.find("\n---")
    if close_idx < 0:
        raise ValueError("agent file missing closing frontmatter fence")
    fm = rest[:close_idx]
    body = rest[close_idx + 4:]
    if body.startswith("\r\n"):
        body = body[2:]
    elif body.startswith("\n"):
        body = body[1:]

    lines = fm.splitlines()
    out: list[str] = []
    replaced = False
    for line in lines:
        if line.strip().startswith("model:"):
            out.append(f"model: {model_value}")
            replaced = True
        else:
            out.append(line)
    if not replaced:
        inserted = False
        new_out: list[str] = []
        for line in out:
            new_out.append(line)
            if not inserted and line.strip().startswith("description:"):
                new_out.append(f"model: {model_value}")
                inserted = True
        if not inserted:
            new_out.insert(0, f"model: {model_value}")
        out = new_out

    return "---\n" + "\n".join(out) + "\n---" + (("\n" + body) if body else "")


def apply_catalog(target_root: Path) -> int:
    catalog_path = target_root / ".opencode" / "model-catalog.local.json"
    if not catalog_path.is_file():
        return 0

    try:
        raw = catalog_path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"[{REASON_MODEL_CATALOG_INVALID}] scope={SCOPE_TAG} invalid JSON: {exc}", file=sys.stderr)
        return 1

    schema_errors = validate_opencode_catalog_data(data)
    if schema_errors:
        for err in schema_errors:
            print(f"[{REASON_MODEL_CATALOG_INVALID}] scope={SCOPE_TAG} {err}", file=sys.stderr)
        return 1

    providers = data.get("providers", {})
    roles = data.get("roles", {})
    agents_dir = target_root / ".opencode" / "agents"

    for role in OPENCODE_ROLE_KEYS:
        provider, slug, reason = parse_role_assignment(roles.get(role, ""), providers)
        if reason:
            print(f"[{REASON_OPENCODE_MODEL_SLUG_UNKNOWN}] role={role}", file=sys.stderr)
            return 1
        model_value = f"{provider}/{slug}"
        agent_path = agents_dir / f"{role}.md"
        if not agent_path.is_file():
            print(
                f"[{REASON_OPENCODE_MODEL_SLUG_UNKNOWN}] missing installed agent: {agent_path}",
                file=sys.stderr,
            )
            return 1
        try:
            updated = inject_model_frontmatter(agent_path.read_text(encoding="utf-8"), model_value)
        except ValueError as exc:
            print(f"[{REASON_MODEL_CATALOG_INVALID}] scope={SCOPE_TAG} {exc}", file=sys.stderr)
            return 1
        agent_path.write_text(updated, encoding="utf-8", newline="\n")

    print("[OPENCODE_MODEL_CATALOG_APPLY_OK]")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenCode model catalog materializer (US-0123)")
    parser.add_argument("--target", type=Path, help="Install target repository root")
    parser.add_argument("--repo", type=Path, help="Alias for --target")
    args = parser.parse_args()
    target = args.target or args.repo
    if not target:
        print("error: --target or --repo required", file=sys.stderr)
        return 1
    return apply_catalog(target.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
