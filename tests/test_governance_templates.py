"""Deterministic checks for the GitHub Issue Form, PR template, and the
portable-Agent-Skill independence boundary. No LLM/API calls.

The YAML-parse checks use `pytest.importorskip("yaml")` so they run wherever
PyYAML is available (locally and in CI, which installs it) and skip cleanly
otherwise — the string-level checks below always run.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
ISSUE_FORM = REPO_ROOT / ".github/ISSUE_TEMPLATE/engineering-task.yml"
ISSUE_CONFIG = REPO_ROOT / ".github/ISSUE_TEMPLATE/config.yml"
PR_TEMPLATE = REPO_ROOT / ".github/PULL_REQUEST_TEMPLATE.md"
WORKFLOWS_DIR = REPO_ROOT / ".github/workflows"

EXPECTED_ISSUE_FIELDS = [
    "Type",
    "Area",
    "Priority",
    "Problem",
    "Goal",
    "Scope",
    "Non-Goals",
    "Acceptance Criteria",
    "Dependencies",
    "Validation",
]

FORBIDDEN_ISSUE_FIELDS = ["Agent / Owner", "Architecture prerequisite", "Owner", "Architecture Prerequisite"]

EXPECTED_AREA_OPTIONS = [
    "Agent Skills",
    "Orchestration",
    "Agent Contracts",
    "Repository Governance",
    "GitHub / Workflow",
    "Quality / Testing",
    "Infrastructure",
    "Documentation",
    "Research",
]

EXPECTED_VISIBLE_PR_SECTIONS = [
    "## Summary",
    "## What changed",
    "## Validation",
    "## Reviewer notes",
    "## Risk / Impact",
]


def test_issue_template_files_exist():
    assert ISSUE_FORM.is_file()
    assert ISSUE_CONFIG.is_file()


def test_blank_issues_are_disabled():
    assert "blank_issues_enabled: false" in ISSUE_CONFIG.read_text(encoding="utf-8")


def test_issue_form_parses_as_yaml_with_exactly_ten_fields():
    yaml = pytest.importorskip("yaml")
    data = yaml.safe_load(ISSUE_FORM.read_text(encoding="utf-8"))
    labels = [
        item["attributes"]["label"]
        for item in data["body"]
        if item.get("type") in {"input", "textarea", "dropdown", "checkboxes"}
    ]
    assert labels == EXPECTED_ISSUE_FIELDS, f"Issue Form fields drifted: {labels}"


def test_every_workflow_file_parses_as_yaml_with_jobs():
    yaml = pytest.importorskip("yaml")
    workflow_files = sorted(WORKFLOWS_DIR.glob("*.yml")) + sorted(WORKFLOWS_DIR.glob("*.yaml"))
    assert workflow_files, "expected at least one workflow under .github/workflows/"
    for path in workflow_files:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert isinstance(data, dict), f"{path.name} did not parse to a mapping"
        assert isinstance(data.get("jobs"), dict) and data["jobs"], f"{path.name} has no jobs"


def test_pr_description_length_workflow_is_read_only():
    text = (WORKFLOWS_DIR / "pr-description-length.yml").read_text(encoding="utf-8")
    assert "permissions: {}" in text, "the PR-description-length workflow must declare no token permissions"
    assert "pr_description_length.py" in text


def test_sync_issue_labels_workflow_is_least_privilege_and_serialized():
    yaml = pytest.importorskip("yaml")
    data = yaml.safe_load((WORKFLOWS_DIR / "sync-issue-labels.yml").read_text(encoding="utf-8"))
    assert data["permissions"] == {"issues": "write"}, "label sync must request only issues:write"
    assert data["concurrency"]["cancel-in-progress"] is False, "label mutations must not be cancelled mid-run"
    assert "sync_issue_labels.py" in (WORKFLOWS_DIR / "sync-issue-labels.yml").read_text(encoding="utf-8")


def test_issue_form_has_no_routing_or_architecture_fields():
    text = ISSUE_FORM.read_text(encoding="utf-8")
    for forbidden in FORBIDDEN_ISSUE_FIELDS:
        assert forbidden not in text, f"deferred field present in Issue Form: {forbidden}"


def test_issue_form_priority_dropdown_has_no_p0_option():
    yaml = pytest.importorskip("yaml")
    data = yaml.safe_load(ISSUE_FORM.read_text(encoding="utf-8"))
    priority = next(i for i in data["body"] if i.get("id") == "priority")
    options = priority["attributes"]["options"]
    assert options == ["P1 — High", "P2 — Medium", "P3 — Low"], options
    assert not any("P0" in o for o in options), "P0 must not be a selectable Priority option"


def test_issue_form_area_taxonomy_is_stable_and_not_per_agent():
    yaml = pytest.importorskip("yaml")
    data = yaml.safe_load(ISSUE_FORM.read_text(encoding="utf-8"))
    area = next(i for i in data["body"] if i.get("id") == "area")
    options = area["attributes"]["options"]
    assert options == EXPECTED_AREA_OPTIONS, f"Area taxonomy drifted: {options}"
    # Must not mirror the Agent list.
    for agent_name in ["Backend", "Frontend", "DevOps", "Architect", "QA", "Release", "Security", "Team Lead"]:
        assert agent_name not in options, f"Area taxonomy must not name individual Agent '{agent_name}'"


def test_pr_template_sections_present_and_reviewer_oriented():
    text = PR_TEMPLATE.read_text(encoding="utf-8")
    for section in EXPECTED_VISIBLE_PR_SECTIONS:
        assert section in text, f"PR template missing section: {section}"
    assert text.index("## Summary") < text.index("## What changed")
    assert text.index("## What changed") < text.index("## Validation")
    assert text.index("## Validation") < text.index("## Reviewer notes")
    assert text.index("## Reviewer notes") < text.index("## Risk / Impact")

    # The PR body is a concise review delta, not a re-derivation of the diff.
    assert "2–5 high-value bullets" in text
    assert "do not restate them" in text
    assert "Summarize results" in text and "do not paste test logs" in text
    assert "non-obvious" in text

    # Specialized traceability stays available in one optional, collapsed block.
    assert text.count("<details>") >= 1
    for semantic_marker in [
        "Specialized impact",
        "Produced by:",
        "Governance surface:",
        "Behavior or contract change:",
        "Execution participation is metadata, never review approval",
        "None",
        "N/A",
    ]:
        assert semantic_marker in text, f"PR template lost required semantics: {semantic_marker}"

    # The mechanical changed-file / changed-surface inventory is gone (the diff covers it),
    # and Related / Remaining Work is folded into an optional one-line link, not a section.
    for removed in [
        "### Change surface",
        "- [ ] Agent Skill behavior",
        "## Related / Remaining Work",
        "<summary>Execution metadata",
    ]:
        assert removed not in text, f"PR template still carries removed ceremony: {removed}"
    assert "follow-up Issue" in text

    # Code-Review-specific global governance must not leak in.
    for leak in ["Self-review prevention", "SHA / delta review", "Approve / Request Changes"]:
        assert leak not in text, f"Code-Review-specific item leaked into PR template: {leak}"


def test_claude_md_remains_thin():
    claude = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    assert "AGENTS.md" in claude
    assert len(claude.splitlines()) <= 20, "CLAUDE.md should stay a thin adapter"
    # It must not restate policy content.
    assert "squash merge" not in claude.lower()
