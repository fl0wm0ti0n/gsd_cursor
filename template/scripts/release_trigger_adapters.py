"""
Release trigger adapters — dispatch release flow by trigger source (US-0111 / DEC-0111).

Four adapters:
  - github:  GitHub webhook release event → resolve tag + find previous via API
  - npm:     npm publish event → read package version + query registry
  - git_tag: Git tag push → parse GITHUB_REF or local git describe
  - manual:  Legacy /release command → byte-identical to pre-US-0111

All adapters produce TriggerContext(version, previous_version, source, metadata).
Downstream reuse release_changelog_lib.compare_versions() and promote_unreleased()
without modification (compose — US-0100 read-only).

Reason codes (DEC-0111 §7):
  RELEASE_TRIGGER_ADAPTER_FAILED
  RELEASE_TRIGGER_TAG_MISSING
  RELEASE_TRIGGER_PREVIOUS_MISSING
  RELEASE_TRIGGER_PACKAGE_JSON_MISSING
  RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED
  RELEASE_TRIGGER_NOTES_WRITE_FAILED
  RELEASE_TRIGGER_EVENT_EMIT_FAILED
  RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED
  RELEASE_TRIGGER_SOURCE_INVALID

Default source: RELEASE_TRIGGER_SOURCE=manual (zero behavior change vs pre-US-0111).
"""

from __future__ import annotations

import abc
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

# Semantic version pattern
SEMVER_RE = re.compile(
    r"^v?([0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?)$"
)

# --- Scratchpad key contracts (DEC-0111 §1) ----------------------------------

RELEASE_TRIGGER_SOURCE_KEY = "RELEASE_TRIGGER_SOURCE"
RELEASE_TRIGGER_SOURCE_VALUES = frozenset({"manual", "github", "npm", "git_tag", "auto"})
RELEASE_TRIGGER_SOURCE_DEFAULT = "manual"

RELEASE_TRIGGER_TIMEOUT_SEC_KEY = "RELEASE_TRIGGER_TIMEOUT_SEC"
RELEASE_TRIGGER_TIMEOUT_SEC_DEFAULT = 10

RELEASE_TRIGGER_FALLBACK_TO_LOCAL_KEY = "RELEASE_TRIGGER_FALLBACK_TO_LOCAL"
RELEASE_TRIGGER_FALLBACK_TO_LOCAL_DEFAULT = "0"

# --- Reason codes (DEC-0111 §7, 9 codes) -------------------------------------

RELEASE_TRIGGER_ADAPTER_FAILED = "RELEASE_TRIGGER_ADAPTER_FAILED"
RELEASE_TRIGGER_TAG_MISSING = "RELEASE_TRIGGER_TAG_MISSING"
RELEASE_TRIGGER_PREVIOUS_MISSING = "RELEASE_TRIGGER_PREVIOUS_MISSING"
RELEASE_TRIGGER_PACKAGE_JSON_MISSING = "RELEASE_TRIGGER_PACKAGE_JSON_MISSING"
RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED = "RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED"
RELEASE_TRIGGER_NOTES_WRITE_FAILED = "RELEASE_TRIGGER_NOTES_WRITE_FAILED"
RELEASE_TRIGGER_EVENT_EMIT_FAILED = "RELEASE_TRIGGER_EVENT_EMIT_FAILED"
RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED = "RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED"
RELEASE_TRIGGER_SOURCE_INVALID = "RELEASE_TRIGGER_SOURCE_INVALID"

FAIL_CODES: Tuple[str, ...] = (
    RELEASE_TRIGGER_ADAPTER_FAILED,
    RELEASE_TRIGGER_TAG_MISSING,
    RELEASE_TRIGGER_PREVIOUS_MISSING,
    RELEASE_TRIGGER_PACKAGE_JSON_MISSING,
    RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED,
    RELEASE_TRIGGER_NOTES_WRITE_FAILED,
    RELEASE_TRIGGER_EVENT_EMIT_FAILED,
    RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED,
    RELEASE_TRIGGER_SOURCE_INVALID,
)

FAIL_CODES_COUNT = 9

# --- TriggerContext dataclass ------------------------------------------------


@dataclass
class TriggerContext:
    version: str
    previous_version: Optional[str]
    source: str  # manual | github | npm | git_tag
    metadata: Dict[str, Any] = field(default_factory=dict)


# --- Abstract base class ------------------------------------------------------


class ReleaseAdapter(abc.ABC):
    """Abstract base class for release trigger adapters."""

    source_name: str = "unknown"

    @abc.abstractmethod
    def detect(self, env_vars: Optional[Dict[str, str]] = None) -> Optional[TriggerContext]:
        """Return TriggerContext when this adapter matches, None otherwise."""

    @abc.abstractmethod
    def get_version_info(self) -> TriggerContext:
        """Resolve version + previous; fail-closed on missing data."""


# --- GitHub webhook adapter ---------------------------------------------------


def _strip_v(tag: str) -> str:
    return tag.lstrip("v").lstrip("V")


def _is_semver(tag: str) -> bool:
    return bool(SEMVER_RE.match(tag.strip()))


def _semver_sort_key(tag: str) -> Tuple[int, ...]:
    base = _strip_v(tag).split("-", 1)[0]
    parts = base.split(".")
    out: List[int] = []
    for p in parts:
        try:
            out.append(int(p))
        except ValueError:
            out.append(0)
    while len(out) < 3:
        out.append(0)
    return tuple(out)


class GithubReleaseAdapter(ReleaseAdapter):
    """GitHub webhook release event adapter (AC-2).

    Parse release.tag_name from webhook payload; query GitHub API to find
    previous tag (sorted by created_at desc, skip current). Fallback:
    git ls-remote --tags origin filtered for semver.
    """

    source_name = "github"

    def __init__(
        self,
        env_vars: Optional[Dict[str, str]] = None,
        payload: Optional[Dict[str, Any]] = None,
        timeout_sec: int = RELEASE_TRIGGER_TIMEOUT_SEC_DEFAULT,
    ) -> None:
        self.env = env_vars or dict(os.environ)
        self.payload = payload or {}
        self.timeout_sec = timeout_sec

    def detect(self, env_vars: Optional[Dict[str, str]] = None) -> Optional[TriggerContext]:
        env = env_vars or self.env
        if env.get("GITHUB_EVENT_NAME") == "release" and env.get("GITHUB_EVENT_PATH"):
            try:
                with open(env["GITHUB_EVENT_PATH"], "r", encoding="utf-8") as f:
                    payload = json.load(f)
                tag = payload.get("release", {}).get("tag_name", "")
                if tag and _is_semver(tag):
                    return self._resolve(tag, env)
            except (OSError, json.JSONDecodeError):
                return None
        return None

    def get_version_info(self) -> TriggerContext:
        tag = self.payload.get("release", {}).get("tag_name", "")
        if not tag or not _is_semver(tag):
            raise ReleaseTriggerError(
                RELEASE_TRIGGER_TAG_MISSING, "GitHub payload missing release.tag_name"
            )
        return self._resolve(tag, self.env)

    def _resolve(self, tag: str, env: Dict[str, str]) -> TriggerContext:
        version = _strip_v(tag)
        previous = self._find_previous(env, version)
        return TriggerContext(
            version=version,
            previous_version=previous,
            source=self.source_name,
            metadata={"tag_name": tag, "token_env_ref": "GITHUB_TOKEN"},
        )

    def _find_previous(self, env: Dict[str, str], current_version: str) -> Optional[str]:
        token = env.get("GITHUB_TOKEN", "")
        repo_slug = env.get("GITHUB_REPOSITORY", "")
        if token and repo_slug:
            tags = self._api_tags(token, repo_slug, env)
            if tags is not None:
                for t in tags:
                    if _is_semver(t) and _strip_v(t) != current_version:
                        return _strip_v(t)
                return None
        tags = self._ls_remote_tags(env)
        for t in tags:
            if _is_semver(t) and _strip_v(t) != current_version:
                return _strip_v(t)
        return None

    def _api_tags(
        self, token: str, repo_slug: str, env: Dict[str, str]
    ) -> Optional[List[str]]:
        import urllib.request
        import urllib.error

        url = f"https://api.github.com/repos/{repo_slug}/releases?per_page=100"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"token {token}")
        req.add_header("Accept", "application/vnd.github.v3+json")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            releases = [(r["tag_name"], r.get("created_at", "")) for r in data if "tag_name" in r]
            releases.sort(key=lambda x: x[1], reverse=True)
            return [r[0] for r in releases]
        except Exception:
            return None

    def _ls_remote_tags(self, env: Dict[str, str]) -> List[str]:
        try:
            result = subprocess.run(
                ["git", "ls-remote", "--tags", "origin"],
                capture_output=True,
                text=True,
                timeout=self.timeout_sec,
                cwd=env.get("GIT_WORK_DIR", None),
            )
            if result.returncode != 0:
                return []
            tags: List[str] = []
            for line in result.stdout.splitlines():
                parts = line.split("\t")
                if len(parts) >= 2 and parts[1].startswith("refs/tags/"):
                    tag = parts[1][len("refs/tags/") :]
                    if not tag.endswith("^{}") and _is_semver(tag):
                        tags.append(tag)
            tags.sort(key=_semver_sort_key, reverse=True)
            return tags
        except Exception:
            return []


# --- npm publish adapter ------------------------------------------------------


class NpmPublishAdapter(ReleaseAdapter):
    """npm publish event adapter (AC-3).

    Read npm_package_version env var; query npm registry for previous version.
    Offline fallback: package-lock.json when RELEASE_TRIGGER_FALLBACK_TO_LOCAL=1.
    """

    source_name = "npm"

    def __init__(
        self,
        env_vars: Optional[Dict[str, str]] = None,
        timeout_sec: int = RELEASE_TRIGGER_TIMEOUT_SEC_DEFAULT,
        fallback_to_local: bool = False,
        repo_root: Optional[str] = None,
    ) -> None:
        self.env = env_vars or dict(os.environ)
        self.timeout_sec = timeout_sec
        self.fallback_to_local = fallback_to_local
        self.repo_root = repo_root or "."

    def detect(self, env_vars: Optional[Dict[str, str]] = None) -> Optional[TriggerContext]:
        env = env_vars or self.env
        pkg_version = env.get("npm_package_version", "")
        if pkg_version and _is_semver(pkg_version):
            return self._resolve(pkg_version, env)
        return None

    def get_version_info(self) -> TriggerContext:
        pkg_version = self.env.get("npm_package_version", "")
        if not pkg_version or not _is_semver(pkg_version):
            pkg_lock = self._read_package_lock()
            if pkg_lock:
                return TriggerContext(
                    version=pkg_lock,
                    previous_version=None,
                    source=self.source_name,
                    metadata={"fallback": "package-lock.json"},
                )
            raise ReleaseTriggerError(
                RELEASE_TRIGGER_PACKAGE_JSON_MISSING,
                "npm_package_version env var missing and package-lock.json unreadable",
            )
        return self._resolve(pkg_version, self.env)

    def _resolve(self, version: str, env: Dict[str, str]) -> TriggerContext:
        previous = self._find_previous(env, version)
        return TriggerContext(
            version=version,
            previous_version=previous,
            source=self.source_name,
            metadata={"npm_package_version": version},
        )

    def _find_previous(self, env: Dict[str, str], current: str) -> Optional[str]:
        versions = self._registry_versions(env)
        if versions is not None:
            sv_versions = [v for v in versions if _is_semver(v)]
            sv_versions.sort(key=_semver_sort_key, reverse=True)
            for v in sv_versions:
                if v != current and v != _strip_v(current):
                    return v
            return None
        if self.fallback_to_local:
            return self._read_package_lock()
        return None

    def _registry_versions(self, env: Dict[str, str]) -> Optional[List[str]]:
        pkg_name = env.get("npm_package_name", "")
        if not pkg_name:
            return None
        try:
            result = subprocess.run(
                ["npm", "view", pkg_name, "versions", "--json"],
                capture_output=True,
                text=True,
                timeout=self.timeout_sec,
            )
            if result.returncode != 0:
                return None
            data = json.loads(result.stdout)
            if isinstance(data, list):
                return data
            return None
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            return None

    def _read_package_lock(self) -> Optional[str]:
        lock_path = os.path.join(self.repo_root, "package-lock.json")
        if not os.path.isfile(lock_path):
            return None
        try:
            with open(lock_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            version = data.get("version", "")
            if version and _is_semver(version):
                return version
        except (OSError, json.JSONDecodeError):
            pass
        return None


# --- Git tag push adapter -----------------------------------------------------


class GitTagAdapter(ReleaseAdapter):
    """Git tag push adapter (AC-4).

    Parse GITHUB_REF (CI) or local git describe --tags --abbrev=0.
    Compute previous_version via git for-each-ref --sort=-version:refname refs/tags.
    """

    source_name = "git_tag"

    def __init__(
        self,
        env_vars: Optional[Dict[str, str]] = None,
        repo_root: Optional[str] = None,
    ) -> None:
        self.env = env_vars or dict(os.environ)
        self.repo_root = repo_root or "."

    def detect(self, env_vars: Optional[Dict[str, str]] = None) -> Optional[TriggerContext]:
        env = env_vars or self.env
        ref = env.get("GITHUB_REF", "")
        if ref.startswith("refs/tags/"):
            tag = ref[len("refs/tags/") :]
            if _is_semver(tag):
                return self._resolve(tag)
        try:
            tag = self._git_describe_tag()
            if tag and _is_semver(tag):
                return self._resolve(tag)
        except Exception:
            pass
        return None

    def get_version_info(self) -> TriggerContext:
        ref = self.env.get("GITHUB_REF", "")
        if ref.startswith("refs/tags/"):
            tag = ref[len("refs/tags/") :]
            if _is_semver(tag):
                return self._resolve(tag)
            raise ReleaseTriggerError(
                RELEASE_TRIGGER_TAG_MISSING, f"GITHUB_REF tag is not semver: {ref!r}"
            )
        tag = self._git_describe_tag()
        if tag and _is_semver(tag):
            return self._resolve(tag)
        raise ReleaseTriggerError(
            RELEASE_TRIGGER_TAG_MISSING, "Cannot resolve current tag from GITHUB_REF or git describe"
        )

    def _resolve(self, tag: str) -> TriggerContext:
        version = _strip_v(tag)
        previous = self._find_previous()
        return TriggerContext(
            version=version,
            previous_version=previous,
            source=self.source_name,
            metadata={"tag_name": tag},
        )

    def _git_describe_tag(self) -> Optional[str]:
        try:
            result = subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return None

    def _find_previous(self) -> Optional[str]:
        try:
            result = subprocess.run(
                ["git", "for-each-ref", "--sort=-version:refname", "refs/tags"],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
            )
            if result.returncode != 0:
                return None
            current = None
            ref = self.env.get("GITHUB_REF", "")
            if ref.startswith("refs/tags/"):
                current = _strip_v(ref[len("refs/tags/") :])
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 3:
                    refname = parts[2]
                    if refname.startswith("refs/tags/"):
                        tag = refname[len("refs/tags/") :]
                        if _is_semver(tag):
                            v = _strip_v(tag)
                            if current is not None and v == current:
                                continue
                            return v
        except Exception:
            pass
        return None


# --- Manual adapter (backward compatibility) ----------------------------------


class ManualReleaseAdapter(ReleaseAdapter):
    """Manual /release adapter (AC-5).

    Byte-identical to pre-US-0111 /release behavior.
    source=manual, version=current, previous_version=None.
    """

    source_name = "manual"

    def __init__(
        self,
        current_version: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None,
        repo_root: Optional[str] = None,
    ) -> None:
        self.current_version = current_version
        self.env = env_vars or dict(os.environ)
        self.repo_root = repo_root or "."

    def detect(self, env_vars: Optional[Dict[str, str]] = None) -> Optional[TriggerContext]:
        return TriggerContext(
            version=self.current_version or "0.0.0",
            previous_version=None,
            source=self.source_name,
            metadata={"manual": True},
        )

    def get_version_info(self) -> TriggerContext:
        return TriggerContext(
            version=self.current_version or "0.0.0",
            previous_version=None,
            source=self.source_name,
            metadata={"manual": True},
        )


# --- Adapter registry ---------------------------------------------------------

_ADAPTER_MAP: Dict[str, type] = {
    "github": GithubReleaseAdapter,
    "npm": NpmPublishAdapter,
    "git_tag": GitTagAdapter,
    "manual": ManualReleaseAdapter,
}

# Auto-detection priority order
_AUTO_PRIORITY: Tuple[str, ...] = ("github", "npm", "git_tag", "manual")


class ReleaseTriggerError(Exception):
    def __init__(self, code: str, message: str = "") -> None:
        self.code = code
        super().__init__(message or code)


def dispatch_to_adapter(
    source: str,
    env_vars: Optional[Dict[str, str]] = None,
    *,
    current_version: Optional[str] = None,
    repo_root: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
) -> TriggerContext:
    """
    Resolve source and dispatch to the matching adapter. Returns TriggerContext.

    source values: manual, github, npm, git_tag, auto
    Invalid source → RELEASE_TRIGGER_SOURCE_INVALID (fail-closed).
    """
    if source not in RELEASE_TRIGGER_SOURCE_VALUES:
        raise ReleaseTriggerError(
            RELEASE_TRIGGER_SOURCE_INVALID,
            f"Unknown RELEASE_TRIGGER_SOURCE={source!r}; "
            f"allowed: {sorted(RELEASE_TRIGGER_SOURCE_VALUES)}",
        )

    env = env_vars or dict(os.environ)

    if source == "auto":
        return _auto_dispatch(env, current_version=current_version, repo_root=repo_root, payload=payload)

    adapter = _instantiate(source, env, current_version, repo_root, payload)
    return adapter.get_version_info()


def _auto_dispatch(
    env: Dict[str, str],
    *,
    current_version: Optional[str] = None,
    repo_root: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
) -> TriggerContext:
    for source_name in _AUTO_PRIORITY:
        if source_name == "manual":
            continue
        adapter = _instantiate(source_name, env, current_version, repo_root, payload)
        ctx = adapter.detect(env)
        if ctx is not None:
            return ctx
    return ManualReleaseAdapter(
        current_version=current_version,
        env_vars=env,
        repo_root=repo_root,
    ).get_version_info()


def _instantiate(
    source: str,
    env: Dict[str, str],
    current_version: Optional[str],
    repo_root: Optional[str],
    payload: Optional[Dict[str, Any]],
) -> ReleaseAdapter:
    cls = _ADAPTER_MAP[source]
    if source == "github":
        return cls(env_vars=env, payload=payload or {})
    if source == "npm":
        return cls(env_vars=env, repo_root=repo_root)
    if source == "git_tag":
        return cls(env_vars=env, repo_root=repo_root)
    if source == "manual":
        return cls(current_version=current_version, env_vars=env, repo_root=repo_root)
    return cls()


# --- Version comparison integration (T-006 / AC-6) ---------------------------


def compare_versions_from_trigger(trigger: TriggerContext) -> Tuple[str, Optional[str]]:
    """
    Compute semver diff from TriggerContext.
    Uses release_changelog_lib.normalize_semver for validation.
    Fail-closed: RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED.
    """
    try:
        from release_changelog_lib import normalize_semver, ReleaseChangelogError
    except ImportError:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from release_changelog_lib import normalize_semver, ReleaseChangelogError

    try:
        norm_current = normalize_semver(trigger.version)
    except ReleaseChangelogError as exc:
        raise ReleaseTriggerError(
            RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED,
            f"Cannot normalize current version: {exc}",
        )

    norm_previous: Optional[str] = None
    if trigger.previous_version:
        try:
            norm_previous = normalize_semver(trigger.previous_version)
        except ReleaseChangelogError as exc:
            raise ReleaseTriggerError(
                RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED,
                f"Cannot normalize previous version: {exc}",
            )

    return norm_current, norm_previous


# --- Atomic file write (T-007, T-008 / AC-7, AC-8) ---------------------------

_ATOMIC_RETRY_DELAY = 0.1
_ATOMIC_RETRY_COUNT = 2


def atomic_write_file(target_path: str, content: str) -> None:
    """
    Write content to target_path atomically via os.replace(temp, target).
    Best-effort on Windows: catch PermissionError, retry 0.1s.
    Fail-closed: RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED.
    """
    target_dir = os.path.dirname(target_path) or "."
    os.makedirs(target_dir, exist_ok=True)

    for attempt in range(_ATOMIC_RETRY_COUNT + 1):
        try:
            fd, tmp_path = tempfile.mkstemp(
                dir=target_dir, suffix=".tmp", prefix=".atomic_"
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
                    f.write(content)
                os.replace(tmp_path, target_path)
                return
            except Exception:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
                raise
        except PermissionError:
            if attempt < _ATOMIC_RETRY_COUNT:
                time.sleep(_ATOMIC_RETRY_DELAY)
                continue
            raise ReleaseTriggerError(
                RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED,
                f"Atomic write failed (PermissionError after retries): {target_path}",
            )
        except ReleaseTriggerError:
            raise
        except Exception as exc:
            raise ReleaseTriggerError(
                RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED,
                f"Atomic write failed: {target_path}: {exc}",
            )


def promote_changelog_version(
    semver: str,
    sprint_ids: Sequence[str],
    repo_root: str,
    release_date: Optional[str] = None,
) -> str:
    """
    Promote [Unreleased] → [X.Y.Z] atomically + generate per-version doc.
    Reuses release_changelog_lib.promote_unreleased() without modification.
    Fail-closed: RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED.
    """
    from release_changelog_lib import (
        promote_unreleased,
        ensure_changelog_stub,
        changelog_path,
        read_utf8,
    )

    try:
        ensure_changelog_stub(repo_root)
        changelog = changelog_path(repo_root)
        old_text = read_utf8(changelog)

        promote_unreleased(semver, sprint_ids, repo_root, release_date)

        new_text = read_utf8(changelog)
        if new_text != old_text:
            atomic_write_file(changelog, new_text)

        return changelog
    except ReleaseTriggerError:
        raise
    except Exception as exc:
        raise ReleaseTriggerError(
            RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED,
            f"CHANGELOG promotion failed: {exc}",
        )


def write_per_version_notes(
    semver: str,
    sprint_ids: Sequence[str],
    repo_root: str,
) -> str:
    """
    Write handoffs/releases/vX.Y.Z-release-notes.md atomically.
    Reuses release_changelog_lib.build_version_doc() read-only compose.
    Fail-closed: RELEASE_TRIGGER_NOTES_WRITE_FAILED.
    """
    from release_changelog_lib import (
        build_version_doc,
        version_doc_path,
        normalize_semver,
        derive_work_items,
        version_fingerprint,
        ReleaseChangelogError,
    )

    try:
        norm = normalize_semver(semver)
        work_items = derive_work_items(sprint_ids, repo_root)
        fp = version_fingerprint(norm, [w.item_id for w in work_items])
        target_path = version_doc_path(repo_root, norm)

        content_lines = [
            f"# Release notes — {norm}",
            "",
            f"<!-- release_changelog_fingerprint: {fp} -->",
            "",
            "> Per-version GitHub `-F` SOT (US-0100). Sprint-scoped evidence in "
            "`handoffs/releases/Sxxxx-release-notes.md`.",
            "",
            "## Work items",
            "",
        ]
        for wi in work_items:
            content_lines.append(f"- **{wi.item_id}** — {wi.summary}")
        content_lines.extend(["", "## Sprint evidence", ""])
        for sid in sorted(set(sprint_ids)):
            content_lines.append(f"- [`{sid}`](handoffs/releases/{sid}-release-notes.md)")
        content_lines.append("")
        content = "\n".join(content_lines)

        atomic_write_file(target_path, content)
        return target_path
    except ReleaseTriggerError:
        raise
    except Exception as exc:
        raise ReleaseTriggerError(
            RELEASE_TRIGGER_NOTES_WRITE_FAILED,
            f"Per-version notes write failed for {semver}: {exc}",
        )


# --- Ledger event emit (T-009 / AC-9) -----------------------------------------


def emit_version_derivation_event(
    trigger: TriggerContext,
    norm_version: str,
    norm_previous: Optional[str],
    repo_root: str,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Emit (semver, previous_semver, timestamp, derivation_decisions[]) event
    to US-0103 ledger via append_entry(decision_type='version_derivation').
    Also write handoffs/release_events/{iso-timestamp}-{semver}.json.
    Ledger schema unchanged (consumer-only append compose).
    Fail-closed: RELEASE_TRIGGER_EVENT_EMIT_FAILED.
    """
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    iso_compact = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    derivation_decisions: List[str] = []
    if trigger.source != "manual":
        derivation_decisions.append(f"trigger_source={trigger.source}")
    if norm_previous:
        derivation_decisions.append(f"previous={norm_previous}")

    event_payload = {
        "semver": norm_version,
        "previous_semver": norm_previous,
        "timestamp_iso": ts,
        "derivation_decisions": derivation_decisions,
        "source": trigger.source,
        "metadata": trigger.metadata,
    }

    event_dir = os.path.join(repo_root, "handoffs", "release_events")
    os.makedirs(event_dir, exist_ok=True)
    event_filename = f"{iso_compact}-{norm_version}.json"
    event_path = os.path.join(event_dir, event_filename)

    try:
        atomic_write_file(event_path, json.dumps(event_payload, indent=2, sort_keys=True) + "\n")
    except ReleaseTriggerError:
        raise
    except Exception as exc:
        raise ReleaseTriggerError(
            RELEASE_TRIGGER_EVENT_EMIT_FAILED,
            f"Failed to write release event file: {exc}",
        )

    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import decision_ledger_lib as ledger

        ledger_path = Path(repo_root) / "handoffs" / "sovereign_decisions" / "decisions.jsonl"
        ledger_entry = {
            "ts": ts,
            "orchestrator_run_id": (scratchpad or {}).get("ORCHESTRATOR_RUN_ID", "manual"),
            "phase_id": "release",
            "role": "dev",
            "decision_id": f"version-derivation-{iso_compact}-{norm_version}",
            "decision_type": "version_derivation",
            "from_artifact": f"trigger:{trigger.source}",
            "to_artifact": event_path,
            "rationale": json.dumps(event_payload, sort_keys=True),
            "plan_fidelity": (scratchpad or {}).get("AUTO_PLAN_FIDELITY", "strict"),
            "cross_model_reviewed": False,
            "risk_tier": "low",
        }
        result = ledger.append_entry(ledger_path, ledger_entry, scratchpad=scratchpad)
    except ReleaseTriggerError:
        raise
    except Exception as exc:
        raise ReleaseTriggerError(
            RELEASE_TRIGGER_EVENT_EMIT_FAILED,
            f"Failed to append ledger entry: {exc}",
        )

    return {"event_path": event_path, "ledger_result": result, "payload": event_payload}
