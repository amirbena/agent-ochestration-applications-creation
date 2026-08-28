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
    ".github/ISSUE_TEMPLATE/engineering-task.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    "policies/README.md",
    "policies/repository-workflow.md",
    "policies/git-pr-merge-policy.md",
    "policies/validation-and-clean-exit.md",
    "policies/github-issue-pr-authoring.md",
    "policies/skill-development-policy.md",
]

# Root repository-development instruction paths that an Agent Skill's
# operational files must NOT depend on — see AGENTS.md ("Packaged Agent
# Skills are independent ...") and policies/skill-development-policy.md
# ("The portable-Skill boundary"). A relative Markdown link inside an
# operational Agent file that resolves to one of these (the repo-root
# AGENTS.md / CLAUDE.md / README.md, or anything under repo-root
# policies/) breaks portability: installing only agents/<agent>/ would
# leave the link dangling.
ROOT_DEV_INSTRUCTION_FILES = {"AGENTS.md", "CLAUDE.md", "README.md"}
ROOT_DEV_INSTRUCTION_DIRS = {"policies"}

# Operational Agent files are everything under agents/<agent>/ except
# human-facing README.md files, which are explanatory and may reference
# root context.
AGENT_NON_OPERATIONAL_FILENAMES = {"README.md"}

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


def is_operational_agent_file(path: Path) -> bool:
    """Return True if `path` is an operational file inside some `agents/<agent>/`.

    Operational = under `agents/<agent>/` and not a human-facing
    `README.md`. These must stay portable (see
    `validate_agent_skill_independence`).
    """
    try:
        rel_parts = path.relative_to(REPO_ROOT).parts
    except ValueError:
        return False
    if len(rel_parts) < 3 or rel_parts[0] != "agents":
        return False
    return path.name not in AGENT_NON_OPERATIONAL_FILENAMES


def links_to_root_dev_instruction(source: Path, target: str) -> bool:
    """Return True if a relative Markdown `target` from `source` resolves to a
    repository-root development-instruction file (AGENTS.md / CLAUDE.md /
    README.md) or anything under a repository-root development directory
    (`policies/`)."""
    resolved = resolve_link_target(source, target)
    try:
        rel = resolved.relative_to(REPO_ROOT)
    except ValueError:
        return False
    parts = rel.parts
    if len(parts) == 1 and parts[0] in ROOT_DEV_INSTRUCTION_FILES:
        return True
    return len(parts) >= 1 and parts[0] in ROOT_DEV_INSTRUCTION_DIRS


def validate_agent_skill_independence() -> list[Issue]:
    """Flag operational Agent files that depend on root repository-development instructions.

    An operational file under `agents/<agent>/` (anything but its
    human-facing `README.md`) must not contain a relative link that
    resolves to the repo-root `AGENTS.md` / `CLAUDE.md` / `README.md` or
    into repo-root `policies/`. Such a link means the Skill cannot be
    consumed on its own. Agent-local links (e.g. to
    `agents/<agent>/policies/...`) are legitimate and never flagged.
    """
    issues: list[Issue] = []
    agents_dir = REPO_ROOT / "agents"
    if not agents_dir.is_dir():
        return issues

    for md_file in iter_markdown_files(agents_dir):
        if not is_operational_agent_file(md_file):
            continue
        content, decode_error = read_utf8(md_file)
        if decode_error or content is None:
            continue
        for lineno, target in extract_relative_link_targets(content):
            if links_to_root_dev_instruction(md_file, target):
                issues.append(
                    Issue(
                        md_file,
                        f"line {lineno}: operational Agent file depends on a root "
                        f"repository-development instruction -> {target} "
                        f"(move the rule into agents/<agent>/ so the Skill stays portable)",
                    )
                )
    return issues


def run_validation() -> list[Issue]:
    """Run all repository checks (required files + every Markdown file) and collect Issues."""
    issues: list[Issue] = []
    issues.extend(validate_required_root_files())
    issues.extend(validate_required_agent_files())
    issues.extend(validate_agent_skill_independence())
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
