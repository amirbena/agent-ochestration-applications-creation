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
