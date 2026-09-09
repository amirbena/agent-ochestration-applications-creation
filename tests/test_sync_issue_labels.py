"""Unit tests for `scripts/sync_issue_labels.py` — the one authoritative
Type / Area / Priority label sync. Stdlib/pytest only, no live GitHub calls.
"""

import json
from pathlib import Path

import pytest

import sync_issue_labels as sync

REPO_ROOT = Path(__file__).resolve().parent.parent
ISSUE_FORM = REPO_ROOT / ".github/ISSUE_TEMPLATE/engineering-task.yml"

FORM_BODY = """### Type

Infrastructure

### Area

GitHub / Workflow

### Priority

P2 — Medium

### Problem

Something needs fixing.
"""


# --- heading_value ---------------------------------------------------------

def test_heading_value_reads_next_nonblank_line():
    assert sync.heading_value(FORM_BODY, "Type") == "Infrastructure"
    assert sync.heading_value(FORM_BODY, "Area") == "GitHub / Workflow"
    assert sync.heading_value(FORM_BODY, "Priority") == "P2 — Medium"


def test_heading_value_handles_hash_level_two():
    assert sync.heading_value("## Type\n\nResearch\n", "Type") == "Research"


def test_heading_value_missing_heading_is_none():
    assert sync.heading_value("### Area\n\nOrchestration\n", "Type") is None


def test_heading_value_empty_field_is_none():
    assert sync.heading_value("### Type\n\n### Area\n\nResearch\n", "Type") is None
    assert sync.heading_value("### Type\n\n_No response_\n", "Type") is None


# --- match_label ---------------------------------------------------------

def test_match_label_exact():
    assert sync.match_label(sync.TYPE_LABELS, "Feature") == "type:feature"
    assert sync.match_label(sync.AREA_LABELS, "Quality / Testing") == "area:quality-testing"


def test_match_label_priority_lenient_on_token():
    assert sync.match_label(sync.PRIORITY_LABELS, "P2 — Medium") == "priority:P2"
    assert sync.match_label(sync.PRIORITY_LABELS, "P3 - Low") == "priority:P3"
    assert sync.match_label(sync.PRIORITY_LABELS, "P1") == "priority:P1"


def test_match_label_unknown_is_none():
    assert sync.match_label(sync.TYPE_LABELS, "Chore") is None
    assert sync.match_label(sync.PRIORITY_LABELS, "P0 — Emergency") is None


# --- mapping drift guard -------------------------------------------------

def test_mapping_covers_every_form_option_exactly():
    yaml = pytest.importorskip("yaml")
    data = yaml.safe_load(ISSUE_FORM.read_text(encoding="utf-8"))
    dropdowns = {item["id"]: item["attributes"]["options"] for item in data["body"] if item.get("type") == "dropdown"}
    assert set(dropdowns["type"]) == set(sync.TYPE_LABELS)
    assert set(dropdowns["area"]) == set(sync.AREA_LABELS)
    assert set(dropdowns["priority"]) == set(sync.PRIORITY_LABELS)


def test_every_mapped_label_uses_its_namespace_prefix():
    for label in sync.TYPE_LABELS.values():
        assert label.startswith("type:")
    for label in sync.AREA_LABELS.values():
        assert label.startswith("area:")
    for label in sync.PRIORITY_LABELS.values():
        assert label.startswith("priority:")


# --- plan --------------------------------------------------------------

def test_plan_adds_all_three_for_a_fresh_form_issue():
    add, remove = sync.plan(FORM_BODY, [])
    assert add == ["area:github-workflow", "priority:P2", "type:infrastructure"]
    assert remove == []


def test_plan_no_change_when_already_in_sync():
    add, remove = sync.plan(FORM_BODY, ["type:infrastructure", "area:github-workflow", "priority:P2"])
    assert (add, remove) == ([], [])


def test_plan_replaces_a_stale_label_in_the_same_namespace():
    add, remove = sync.plan(FORM_BODY, ["type:infrastructure", "area:github-workflow", "priority:P1"])
    assert add == ["priority:P2"]
    assert remove == ["priority:P1"]


def test_plan_leaves_non_managed_labels_untouched():
    add, remove = sync.plan(FORM_BODY, ["good first issue", "help wanted", "priority:P1"])
    assert "good first issue" not in add + remove
    assert "help wanted" not in add + remove
    assert remove == ["priority:P1"]


def test_plan_never_touches_priority_p0():
    add, remove = sync.plan(FORM_BODY, ["priority:P0"])
    assert "priority:P0" not in remove
    assert "priority:P2" in add


def test_plan_on_non_form_body_is_a_noop():
    body = "Just some free text with no Form headings.\n\n- a bullet\n"
    add, remove = sync.plan(body, ["type:feature", "area:orchestration", "priority:P1"])
    assert (add, remove) == ([], [])


def test_plan_partial_body_only_reconciles_present_fields():
    body = "### Type\n\nResearch\n\n### Problem\n\ntext\n"
    add, remove = sync.plan(body, ["type:feature", "area:orchestration", "priority:P1"])
    assert add == ["type:research"]
    assert remove == ["type:feature"]  # area:* / priority:* left alone


def test_plan_unrecognized_value_leaves_namespace_untouched():
    body = "### Type\n\nMysteryType\n"
    add, remove = sync.plan(body, ["type:feature"])
    assert (add, remove) == ([], [])


# --- compute_from_event ------------------------------------------------

def _event(body, labels, number=7, repo="owner/name"):
    return {
        "issue": {"number": number, "body": body, "labels": [{"name": n} for n in labels]},
        "repository": {"full_name": repo},
    }


def test_compute_from_event_extracts_repo_number_and_plan():
    repo, number, add, remove = sync.compute_from_event(_event(FORM_BODY, ["priority:P1"], number=42, repo="a/b"))
    assert (repo, number) == ("a/b", 42)
    assert add == ["area:github-workflow", "priority:P2", "type:infrastructure"]
    assert remove == ["priority:P1"]


def test_compute_from_event_tolerates_null_body_and_missing_labels():
    event = {"issue": {"number": 1, "body": None}, "repository": {"full_name": "a/b"}}
    repo, number, add, remove = sync.compute_from_event(event)
    assert (add, remove) == ([], [])


# --- main() -----------------------------------------------------------

def test_main_github_event_prints_plan_without_applying(tmp_path, capsys):
    event_file = tmp_path / "event.json"
    event_file.write_text(json.dumps(_event(FORM_BODY, [])), encoding="utf-8")
    assert sync.main(["--github-event", str(event_file)]) == 0
    out = capsys.readouterr().out
    assert "+ type:infrastructure" in out
    assert "Applied." not in out


def test_main_body_file_with_labels(tmp_path, capsys):
    body_file = tmp_path / "body.md"
    body_file.write_text(FORM_BODY, encoding="utf-8")
    assert sync.main(["--body-file", str(body_file), "--labels", "type:infrastructure,area:github-workflow,priority:P2"]) == 0
    assert "no change" in capsys.readouterr().out


def test_main_apply_without_token_fails(tmp_path, capsys, monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    event_file = tmp_path / "event.json"
    event_file.write_text(json.dumps(_event(FORM_BODY, [])), encoding="utf-8")
    assert sync.main(["--github-event", str(event_file), "--apply"]) == 1


def test_main_apply_invokes_api_calls_additions_before_removals(tmp_path, capsys, monkeypatch):
    calls = []
    monkeypatch.setattr(sync, "_request", lambda method, url, token, payload=None: calls.append((method, url, payload)))
    monkeypatch.setenv("GITHUB_TOKEN", "x")
    event_file = tmp_path / "event.json"
    event_file.write_text(json.dumps(_event(FORM_BODY, ["priority:P1"], number=9, repo="o/r")), encoding="utf-8")
    assert sync.main(["--github-event", str(event_file), "--apply"]) == 0
    methods = [c[0] for c in calls]
    assert methods == ["POST", "DELETE"], "additions must be applied before removals"
    assert calls[0][2] == {"labels": ["area:github-workflow", "priority:P2", "type:infrastructure"]}
    assert calls[-1][1].endswith("/issues/9/labels/priority%3AP1")
    assert "Applied." in capsys.readouterr().out


def test_main_apply_with_empty_plan_makes_no_api_calls(tmp_path, capsys, monkeypatch):
    calls = []
    monkeypatch.setattr(sync, "_request", lambda *a, **k: calls.append(a))
    monkeypatch.setenv("GITHUB_TOKEN", "x")
    event_file = tmp_path / "event.json"
    in_sync = ["type:infrastructure", "area:github-workflow", "priority:P2"]
    event_file.write_text(json.dumps(_event(FORM_BODY, in_sync)), encoding="utf-8")
    assert sync.main(["--github-event", str(event_file), "--apply"]) == 0
    assert calls == []
    assert "Applied." not in capsys.readouterr().out
