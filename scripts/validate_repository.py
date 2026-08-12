#!/usr/bin/env python3
"""Deterministic repository/Markdown integrity validator.

Stdlib-only (no third-party dependencies) so it can run in CI or locally with
no setup beyond a Python interpreter. See README.md ("Repository Validation")
for what this checks and how it relates to `tests/`.

Usage:
    python scripts/validate_repository.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

EXCLUDED_DIR_NAMES = {".git"}

# Root files every clone of this repository must have — see AGENTS.md
# ("Repository Layout") and README.md.
REQUIRED_ROOT_FILES = [
    "AGENTS.md",
    "README.md",
    "CLAUDE.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
]

# Per-Agent required files, matching the "Structure" section documented in
# each Agent's own SKILL.md. Extend this map when a new Agent is added.
REQUIRED_AGENT_FILES: dict[str, list[str]] = {
    "backend": [
        "SKILL.md",
        "README.md",
        "metadata/skill.yaml",
        "policies/global/CODE-STANDARDS.md",
        "policies/languages/CODE-STANDARDS.md",
        "policies/frameworks/CODE-STANDARDS.md",
        "templates/README.md",
        "templates/backend-assignment.yaml",
        "templates/backend-result.yaml",
        "runbooks/README.md",
    ],
}

MARKDOWN_LINK_RE = re.compile(r"\[[^\]\n]*\]\(([^)\s]+)\)")


class Issue:
    """A single validation problem found at a specific repository path."""

    def __init__(self, path: Path, message: str) -> None:
        """Store the offending `path` and a human-readable `message`."""
        self.path = path
        self.message = message

    def __str__(self) -> str:
        """Render as `<path relative to REPO_ROOT>: <message>` for reporting."""
        try:
            rel = self.path.relative_to(REPO_ROOT)
        except ValueError:
            rel = self.path
        return f"{rel}: {self.message}"


def iter_markdown_files(root: Path) -> list[Path]:
    """Return all `*.md` files under `root`, sorted, excluding EXCLUDED_DIR_NAMES."""
    files = []
    for path in root.rglob("*.md"):
        if any(part in EXCLUDED_DIR_NAMES for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def read_utf8(path: Path) -> tuple[str | None, str | None]:
    """Read `path` as UTF-8 text.

    Returns a `(content, error)` tuple: `content` is the decoded text (or
    `None` on failure), and `error` is a description of the decode failure
    (or `None` on success).
    """
    try:
        return path.read_bytes().decode("utf-8"), None
    except UnicodeDecodeError as exc:
        return None, f"not valid UTF-8 ({exc})"


def check_non_empty(content: str) -> bool:
    """Return `True` if `content` has any non-whitespace text."""
    return content.strip() != ""


def check_trailing_whitespace(content: str) -> list[int]:
    """Return the 1-based line numbers in `content` that end in a space or tab."""
    lines = content.splitlines()
    return [i + 1 for i, line in enumerate(lines) if line != line.rstrip(" \t")]


def check_tabs(content: str) -> list[int]:
    """Return the 1-based line numbers in `content` that contain a tab character."""
    lines = content.splitlines()
    return [i + 1 for i, line in enumerate(lines) if "\t" in line]


def extract_relative_link_targets(content: str) -> list[tuple[int, str]]:
    """Find Markdown link targets in `content`, excluding external/anchor links.

    Returns a list of `(1-based line number, link target)` pairs for every
    Markdown link whose target is not an `http(s)://`, `mailto:`, or `#`
    (in-page anchor) link, i.e. the relative links that should be checked
    against the filesystem.
    """
    targets = []
    for lineno, line in enumerate(content.splitlines(), start=1):
        for match in MARKDOWN_LINK_RE.finditer(line):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            targets.append((lineno, target))
    return targets


def resolve_link_target(path: Path, target: str) -> Path:
    """Resolve a Markdown `target` (from the file at `path`) to an absolute filesystem path.

    Strips any `#fragment` suffix before resolving relative to `path`'s
    parent directory.
    """
    target_path = target.split("#", 1)[0]
    return (path.parent / target_path).resolve()


def validate_markdown_file(path: Path) -> list[Issue]:
    """Validate a single Markdown file at `path`.

    Checks UTF-8 decodability, non-emptiness, trailing whitespace, tab
    characters, and broken relative links. Returns the list of `Issue`s
    found; an empty list means the file passed all checks.
    """
    issues: list[Issue] = []

    content, decode_error = read_utf8(path)
    if decode_error:
        issues.append(Issue(path, decode_error))
        return issues
    assert content is not None

    if not check_non_empty(content):
        issues.append(Issue(path, "file is empty"))
        return issues

    trailing = check_trailing_whitespace(content)
    if trailing:
        lines = ", ".join(str(n) for n in trailing[:10])
        suffix = "..." if len(trailing) > 10 else ""
        issues.append(Issue(path, f"trailing whitespace on line(s) {lines}{suffix}"))

    tabs = check_tabs(content)
    if tabs:
        lines = ", ".join(str(n) for n in tabs[:10])
        suffix = "..." if len(tabs) > 10 else ""
        issues.append(Issue(path, f"tab character(s) on line(s) {lines}{suffix}"))

    for lineno, target in extract_relative_link_targets(content):
        resolved = resolve_link_target(path, target)
        if not resolved.exists():
            issues.append(
                Issue(path, f"line {lineno}: broken relative link -> {target}")
            )

    return issues


def validate_required_root_files() -> list[Issue]:
    """Check that every path in REQUIRED_ROOT_FILES exists as a file in the repo root."""
    issues = []
    for rel in REQUIRED_ROOT_FILES:
        if not (REPO_ROOT / rel).is_file():
            issues.append(Issue(REPO_ROOT / rel, "required repository file is missing"))
    return issues


def validate_required_agent_files() -> list[Issue]:
    """Check each `agents/<name>/` directory for its required Agent files.

    Every Agent directory must contain `SKILL.md`. Agents listed in
    REQUIRED_AGENT_FILES are additionally checked for their full set of
    required relative paths.
    """
    issues = []
    agents_dir = REPO_ROOT / "agents"
    if not agents_dir.is_dir():
        return issues

    for agent_dir in sorted(p for p in agents_dir.iterdir() if p.is_dir()):
        skill_md = agent_dir / "SKILL.md"
        if not skill_md.is_file():
            issues.append(Issue(skill_md, "Agent directory is missing SKILL.md"))

        required = REQUIRED_AGENT_FILES.get(agent_dir.name)
        if required is None:
            continue
        for rel in required:
            if not (agent_dir / rel).is_file():
                issues.append(
                    Issue(agent_dir / rel, "required Agent file is missing")
                )

    return issues


def run_validation() -> list[Issue]:
    """Run all repository checks (required files + every Markdown file) and collect Issues."""
    issues: list[Issue] = []
    issues.extend(validate_required_root_files())
    issues.extend(validate_required_agent_files())
    for md_file in iter_markdown_files(REPO_ROOT):
        issues.extend(validate_markdown_file(md_file))
    return issues


def main() -> int:
    """Run validation, print the results, and return the process exit code (0 or 1)."""
    issues = run_validation()
    if not issues:
        print("Repository validation passed: no issues found.")
        return 0

    print(f"Repository validation failed: {len(issues)} issue(s) found.\n")
    for issue in issues:
        print(f"  - {issue}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
