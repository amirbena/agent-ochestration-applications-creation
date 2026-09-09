#!/usr/bin/env python3
"""Synchronize an Issue's managed labels with its Engineering Task Form fields.

Stdlib-only (no third-party dependencies). This is the **one authoritative
implementation** of the Type / Area / Priority label sync wired to
`.github/workflows/sync-issue-labels.yml`. The Form → label mapping below is the
single canonical place that mapping lives; `tests/test_sync_issue_labels.py`
cross-checks it against `.github/ISSUE_TEMPLATE/engineering-task.yml` so the two
cannot drift.

What it does
------------
For each of the three managed fields (`Type`, `Area`, `Priority`), if the Issue
body has that Form heading with a value this script recognizes, it ensures the
one implied label is present and removes any *other* label the same field could
have produced. A field that is absent or carries an unrecognized value leaves its
namespace completely untouched — so a non-Form Issue, or a partially hand-edited
body, is never stripped of labels.

`priority:P0` is deliberately outside the managed Priority set: it is a manual
escalation (see the Issue Form — P0 is not a selectable option), so this script
never adds or removes it.

Usage
-----
    python3 scripts/sync_issue_labels.py --github-event "$GITHUB_EVENT_PATH" [--apply]
    python3 scripts/sync_issue_labels.py --body-file b.md --labels type:bug,area:x

Without `--apply` the computed plan is printed and nothing is mutated. With
`--apply` (used by the workflow) the add/remove calls are made against the GitHub
REST API using `GITHUB_TOKEN`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

_HTTP_TIMEOUT_SECONDS = 30

# --- The canonical Form-value -> label mapping ------------------------------
# Keys are the exact dropdown option strings in
# .github/ISSUE_TEMPLATE/engineering-task.yml. Covered by a drift test.

TYPE_LABELS = {
    "Feature": "type:feature",
    "Refactor": "type:refactor",
    "Quality": "type:quality",
    "Research": "type:research",
    "Documentation": "type:documentation",
    "Infrastructure": "type:infrastructure",
}

AREA_LABELS = {
    "Agent Skills": "area:agent-skills",
    "Orchestration": "area:orchestration",
    "Agent Contracts": "area:agent-contracts",
    "Repository Governance": "area:repository-governance",
    "GitHub / Workflow": "area:github-workflow",
    "Quality / Testing": "area:quality-testing",
    "Infrastructure": "area:infrastructure",
    "Documentation": "area:documentation",
    "Research": "area:research",
}

PRIORITY_LABELS = {
    "P1 — High": "priority:P1",
    "P2 — Medium": "priority:P2",
    "P3 — Low": "priority:P3",
}

# (Form heading, mapping). Order is the order changes are reported in.
FIELDS = (
    ("Type", TYPE_LABELS),
    ("Area", AREA_LABELS),
    ("Priority", PRIORITY_LABELS),
)

_HEADING_RE = re.compile(r"^#{1,6}[ \t]+(.+?)[ \t]*$")
_PRIORITY_TOKEN_RE = re.compile(r"^(P[0-9]+)\b")
_NO_RESPONSE = {"_no response_", "_none_", "none", ""}


def heading_value(body: str, heading: str) -> str | None:
    """Return the first non-blank line after the `## <heading>` line, or None.

    Handles any heading level (`#`..`######`). Stops at the next heading, so an
    empty field (or a `_No response_` placeholder) yields None.
    """
    lines = body.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    for index, line in enumerate(lines):
        match = _HEADING_RE.match(line.strip())
        if not match or match.group(1) != heading:
            continue
        for following in lines[index + 1:]:
            stripped = following.strip()
            if _HEADING_RE.match(stripped):
                return None
            if stripped and stripped.lower() not in _NO_RESPONSE:
                return stripped
        return None
    return None


def match_label(mapping: dict[str, str], raw_value: str) -> str | None:
    """Map a raw field value to its label, or None if unrecognized.

    Exact match first; then, for Priority-style values, a lenient match on the
    leading `Pn` token so `P2 — Medium` still resolves if the dash or suffix
    render differently.
    """
    value = raw_value.strip()
    if value in mapping:
        return mapping[value]
    token = _PRIORITY_TOKEN_RE.match(value)
    if token:
        for option, label in mapping.items():
            if option == token.group(1) or option.startswith(token.group(1) + " "):
                return label
    return None


def plan(body: str, current_labels: list[str]) -> tuple[list[str], list[str]]:
    """Return `(labels_to_add, labels_to_remove)` for `body` given `current_labels`.

    Pure and deterministic. Only labels a managed field could itself produce are
    ever removed; everything else on the Issue is left alone.
    """
    current = set(current_labels)
    add: set[str] = set()
    remove: set[str] = set()
    for heading, mapping in FIELDS:
        raw = heading_value(body, heading)
        if raw is None:
            continue
        label = match_label(mapping, raw)
        if label is None:
            continue
        field_labels = set(mapping.values())
        if label not in current:
            add.add(label)
        remove |= {other for other in current if other in field_labels and other != label}
    return sorted(add), sorted(remove)


def format_plan(add: list[str], remove: list[str]) -> str:
    """Render the plan for the workflow log."""
    if not add and not remove:
        return "Issue labels: already in sync with the Form (no change)."
    parts = ["Issue label sync plan:"]
    parts += [f"  + {label}" for label in add]
    parts += [f"  - {label}" for label in remove]
    return "\n".join(parts)


# --- GitHub REST calls (thin; not part of the deterministic core) -----------

_API_ROOT = "https://api.github.com"


def _request(method: str, url: str, token: str, payload: dict | None = None) -> None:
    """Perform one authenticated GitHub REST call, raising on HTTP >= 400."""
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    request.add_header("User-Agent", "sync-issue-labels-script")
    if data is not None:
        request.add_header("Content-Type", "application/json")
    # URL is always the fixed api.github.com host built from _API_ROOT.
    with urllib.request.urlopen(request, timeout=_HTTP_TIMEOUT_SECONDS) as response:
        response.read()


def apply_changes(repo: str, issue_number: int, add: list[str], remove: list[str], token: str) -> None:
    """Apply the plan via the GitHub REST API.

    Additions first, then removals: if a call fails partway, the Issue is left
    transiently over-labelled (recoverable, and re-corrected on the next
    ``edited`` event) rather than stripped of a namespace.
    """
    if add:
        _request("POST", f"{_API_ROOT}/repos/{repo}/issues/{issue_number}/labels", token, {"labels": add})
    for label in remove:
        encoded = urllib.parse.quote(label, safe="")
        _request("DELETE", f"{_API_ROOT}/repos/{repo}/issues/{issue_number}/labels/{encoded}", token)


def compute_from_event(event: dict) -> tuple[str, int, list[str], list[str]]:
    """Extract `(repo, issue_number, add, remove)` from a GitHub `issues` event."""
    issue = event["issue"]
    body = issue.get("body") or ""
    current = [label["name"] for label in issue.get("labels", []) if isinstance(label, dict) and "name" in label]
    repo = event["repository"]["full_name"]
    add, remove = plan(body, current)
    return repo, int(issue["number"]), add, remove


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, compute the plan, print it, and optionally apply it."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--github-event", metavar="PATH", help="GitHub event payload JSON ($GITHUB_EVENT_PATH)")
    source.add_argument("--body-file", metavar="PATH", help="file containing the Issue body (with --labels)")
    parser.add_argument("--labels", default="", help="comma-separated current labels, for use with --body-file")
    parser.add_argument("--repo", help="owner/name, for use with --body-file --apply")
    parser.add_argument("--issue", type=int, help="issue number, for use with --body-file --apply")
    parser.add_argument("--apply", action="store_true", help="apply the plan via the GitHub API (needs GITHUB_TOKEN)")
    args = parser.parse_args(argv)

    if args.github_event is not None:
        with open(args.github_event, encoding="utf-8") as handle:
            event = json.load(handle)
        repo, issue_number, add, remove = compute_from_event(event)
    else:
        with open(args.body_file, encoding="utf-8") as handle:
            body = handle.read()
        current = [label.strip() for label in args.labels.split(",") if label.strip()]
        add, remove = plan(body, current)
        repo, issue_number = args.repo, args.issue

    print(format_plan(add, remove))

    if not args.apply or (not add and not remove):
        return 0

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("error: --apply needs GITHUB_TOKEN in the environment", file=sys.stderr)
        return 1
    if not repo or issue_number is None:
        print("error: --apply needs a resolvable repo and issue number", file=sys.stderr)
        return 1
    try:
        apply_changes(repo, issue_number, add, remove, token)
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"error: GitHub API call failed: {exc}", file=sys.stderr)
        return 1
    print("Applied.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
