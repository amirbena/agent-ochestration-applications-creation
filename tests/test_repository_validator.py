"""Runs the deterministic repository validator itself as a pytest check.

This ties `scripts/validate_repository.py` into the pytest suite so a single
`pytest tests` invocation covers both repository integrity and Agent
contracts. It does not call any external LLM/API.
"""

import validate_repository as validator


def test_repository_validation_has_no_issues():
    issues = validator.run_validation()
    assert issues == [], "\n".join(str(issue) for issue in issues)


def test_markdown_files_are_discovered():
    files = validator.iter_markdown_files(validator.REPO_ROOT)
    assert files, "expected at least one Markdown file in the repository"


def test_trailing_whitespace_detection():
    content = "line one\nline two \nline three"
    assert validator.check_trailing_whitespace(content) == [2]


def test_tab_detection():
    content = "line one\n\tline two\nline three"
    assert validator.check_tabs(content) == [2]


def test_broken_relative_link_is_flagged(tmp_path):
    target_dir = tmp_path
    md_file = target_dir / "doc.md"
    md_file.write_text("[missing](./does-not-exist.md)\n", encoding="utf-8")

    issues = validator.validate_markdown_file(md_file)
    assert any("broken relative link" in issue.message for issue in issues)


def test_valid_relative_link_is_not_flagged(tmp_path):
    other = tmp_path / "other.md"
    other.write_text("content\n", encoding="utf-8")
    md_file = tmp_path / "doc.md"
    md_file.write_text("[ok](./other.md)\n", encoding="utf-8")

    issues = validator.validate_markdown_file(md_file)
    assert issues == []


def test_external_and_anchor_links_are_ignored(tmp_path):
    md_file = tmp_path / "doc.md"
    md_file.write_text(
        "[external](https://example.com)\n[anchor](#section)\n", encoding="utf-8"
    )

    issues = validator.validate_markdown_file(md_file)
    assert issues == []


# --- Portable-Agent-Skill independence -------------------------------------

def test_agent_skill_independence_check_passes_on_the_real_repo():
    issues = validator.validate_agent_skill_independence()
    assert issues == [], "\n".join(str(issue) for issue in issues)


def test_operational_agent_file_linking_root_agents_md_is_flagged():
    src = validator.REPO_ROOT / "agents" / "sample" / "SKILL.md"
    assert validator.is_operational_agent_file(src)
    assert validator.links_to_root_dev_instruction(src, "../../AGENTS.md#x")
    assert validator.links_to_root_dev_instruction(src, "../../policies/git-pr-merge-policy.md")
    assert validator.links_to_root_dev_instruction(src, "../../CLAUDE.md")


def test_agent_local_links_are_not_flagged():
    src = validator.REPO_ROOT / "agents" / "sample" / "runbooks" / "x" / "RUNBOOK.md"
    assert not validator.links_to_root_dev_instruction(src, "../../policies/global/CODE-STANDARDS.md")
    assert not validator.links_to_root_dev_instruction(src, "../../SKILL.md")


def test_agent_readme_is_not_an_operational_file():
    readme = validator.REPO_ROOT / "agents" / "sample" / "README.md"
    assert not validator.is_operational_agent_file(readme)


def test_required_root_files_include_policies_and_issue_template():
    for rel in [
        "CHANGELOG.md",
        "policies/README.md",
        "policies/repository-workflow.md",
        "policies/git-pr-merge-policy.md",
        "policies/validation-and-clean-exit.md",
        "policies/github-issue-pr-authoring.md",
        "policies/skill-development-policy.md",
        "policies/changelog-policy.md",
        ".github/ISSUE_TEMPLATE/engineering-task.yml",
        ".github/ISSUE_TEMPLATE/config.yml",
    ]:
        assert rel in validator.REQUIRED_ROOT_FILES
