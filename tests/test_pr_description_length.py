"""Unit tests for `scripts/pr_description_length.py` — the one authoritative
PR-description useful-content gate. Stdlib/pytest only, no LLM/API calls.
"""

import json
from pathlib import Path

import pr_description_length as gate

REPO_ROOT = Path(__file__).resolve().parent.parent


# --- normalize -----------------------------------------------------------------

def test_normalize_drops_html_comments():
    assert gate.normalize("before <!-- template hint\nmultiline --> after") == "before after"


def test_normalize_keeps_link_text_drops_target():
    assert gate.normalize("see [the policy](../policies/x.md) now") == "see the policy now"
    assert gate.normalize("![a diagram](x.png)") == "a diagram"


def test_normalize_drops_autolink_urls():
    assert gate.normalize("ref <https://example.com/very/long/path> done") == "ref done"


def test_normalize_strips_line_markers():
    body = "# Heading\n\n- bullet one\n- [ ] task\n- [x] done\n> quoted\n1. first"
    assert gate.normalize(body) == "Heading bullet one task done quoted first"


def test_normalize_strips_table_syntax():
    body = "| Col A | Col B |\n| --- | --- |\n| v1 | v2 |"
    assert gate.normalize(body) == "Col A Col B v1 v2"


def test_normalize_strips_emphasis_and_inline_code_markers():
    assert gate.normalize("**bold** _em_ `code` ~~strike~~") == "bold em code strike"


def test_normalize_drops_fence_lines_but_keeps_code_content():
    body = "text\n```python\nx = 1\n```\nmore"
    assert gate.normalize(body) == "text x = 1 more"


def test_normalize_collapses_whitespace_runs():
    assert gate.normalize("a\n\n\n   b\t\tc") == "a b c"


def test_normalize_is_idempotent_on_plain_text():
    plain = "one short sentence of plain prose"
    assert gate.normalize(plain) == plain


# --- measure / evaluate ------------------------------------------------------

def test_measure_counts_normalized_code_points():
    assert gate.measure("**hello** [world](x)") == len("hello world")


def test_evaluate_pass_at_and_below_limit():
    ok, evidence = gate.evaluate("x" * 10, limit=10)
    assert ok is True
    assert evidence["useful_content_code_points"] == 10
    assert evidence["overage"] == 0


def test_evaluate_fail_one_over_limit():
    ok, evidence = gate.evaluate("x" * 11, limit=10)
    assert ok is False
    assert evidence["overage"] == 1
    assert evidence["limit"] == 10


def test_evaluate_evidence_reports_raw_and_useful_separately():
    body = "<!-- a long template comment that is not content -->\nreal text here"
    ok, evidence = gate.evaluate(body, limit=6000)
    assert evidence["raw_code_points"] == len(body)
    assert evidence["useful_content_code_points"] == len("real text here")
    assert evidence["useful_content_code_points"] < evidence["raw_code_points"]


def test_default_limit_is_a_single_constant():
    ok, evidence = gate.evaluate("short")
    assert evidence["limit"] == gate.PR_BODY_USEFUL_CONTENT_LIMIT


# --- main() I/O paths --------------------------------------------------------

def test_main_body_file_pass(tmp_path, capsys):
    f = tmp_path / "body.md"
    f.write_text("a concise review delta", encoding="utf-8")
    assert gate.main(["--body-file", str(f)]) == 0
    assert "PASS" in capsys.readouterr().out


def test_main_body_file_fail(tmp_path, capsys):
    f = tmp_path / "body.md"
    f.write_text("x" * 20, encoding="utf-8")
    assert gate.main(["--body-file", str(f), "--limit", "10"]) == 1
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "overage" in out


def test_main_github_event_reads_pull_request_body(tmp_path, capsys):
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"pull_request": {"body": "x" * 50}}), encoding="utf-8")
    assert gate.main(["--github-event", str(event), "--limit", "10"]) == 1


def test_main_github_event_without_pull_request_fails(tmp_path, capsys):
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"issue": {"body": "hi"}}), encoding="utf-8")
    assert gate.main(["--github-event", str(event)]) == 1


def test_main_github_event_null_body_passes(tmp_path):
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"pull_request": {"body": None}}), encoding="utf-8")
    assert gate.main(["--github-event", str(event)]) == 0


def test_main_stdin(monkeypatch, capsys):
    import io

    monkeypatch.setattr("sys.stdin", io.StringIO("a short body"))
    assert gate.main(["--stdin"]) == 0


# --- realistic inputs ------------------------------------------------------

def test_repository_pr_template_is_well_within_limit():
    body = (REPO_ROOT / ".github/PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
    ok, evidence = gate.evaluate(body)
    assert ok, evidence
    # The template is almost entirely HTML comments, so useful content is tiny.
    assert evidence["useful_content_code_points"] < 400
