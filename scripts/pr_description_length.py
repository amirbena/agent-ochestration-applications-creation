#!/usr/bin/env python3
"""Enforce a generous ceiling on a Pull Request description's *useful content*.

Stdlib-only (no third-party dependencies) so it runs in CI or locally with no
setup beyond a Python interpreter. This is the **one authoritative
implementation** of the PR-description length gate referenced by
`policies/github-issue-pr-authoring.md` ("Enforcement: adopted"). Do not add a
second body-measurement implementation anywhere.

What it measures
----------------
Not raw bytes and not raw code points: the body is first put through `normalize`,
which removes the parts that are scaffolding rather than content a reviewer
reads — HTML/template comments, code-fence lines, link and image *targets*
(the visible text is kept), list / task / heading / block-quote / table syntax,
and emphasis markers — then collapses every whitespace run to one space. The
Unicode code-point length of that result is the "useful content" figure.

The limit
---------
`PR_BODY_USEFUL_CONTENT_LIMIT` is a single constant. It is a *ceiling*, not the
per-field size guidance in the policy: it sits far above every real PR body in
this repository's history (the largest was ~3,500 raw code points as of #35), so
a body that exceeds it is almost always restating the Issue, the diff, or
validation logs — which the policy says to link, not reproduce. It must never be
tightened to a point where it forces trimming a body below clarity; see the
policy's "Not a character limit" section.

Usage
-----
    python3 scripts/pr_description_length.py --github-event "$GITHUB_EVENT_PATH"
    python3 scripts/pr_description_length.py --body-file body.md
    printf '%s' "$PR_BODY" | python3 scripts/pr_description_length.py --stdin

Exit code 0 = within the ceiling, 1 = over it (or the body could not be read).
"""

from __future__ import annotations

import argparse
import json
import re
import sys

# The single authoritative limit: useful-content Unicode code points (see
# `normalize`) strictly greater than this fail the check. Sized as a generous
# ceiling from this repository's own history, with ample room for a genuinely
# complex change. Change this in one place only.
PR_BODY_USEFUL_CONTENT_LIMIT = 6000

_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_FENCE_LINE_RE = re.compile(r"^[ \t]*```[^\n]*$", re.MULTILINE)
_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_AUTOLINK_RE = re.compile(r"<https?://[^>\s]+>")
_TABLE_SEP_RE = re.compile(r"^[ \t]*\|?[ \t]*:?-{3,}[-\s|:]*$", re.MULTILINE)
_LIST_MARKER_RE = re.compile(r"^[ \t]*(?:[-*+]|\d+\.)[ \t]+(?:\[[ xX]\][ \t]+)?", re.MULTILINE)
_HEADING_RE = re.compile(r"^[ \t]*#{1,6}[ \t]+", re.MULTILINE)
_QUOTE_RE = re.compile(r"^[ \t]*>[ \t]?", re.MULTILINE)
_EMPHASIS_RE = re.compile(r"\*\*|__|~~|[*_`]")
_WS_RE = re.compile(r"\s+")


def normalize(body: str) -> str:
    """Reduce a raw PR-description body to its reviewer-facing text.

    Deterministic and order-dependent. The steps, in order: normalize line
    endings; drop HTML/template comments; drop code-fence lines (```` ``` ````,
    keeping any content between them); reduce ``![alt](src)`` to ``alt`` and
    ``[text](target)`` to ``text``; drop ``<autolink>`` URLs; drop Markdown
    table separator rows and pipe characters; strip leading list / task /
    heading / block-quote markers; strip emphasis / inline-code markers; collapse
    every whitespace run to a single space and trim.
    """
    s = body.replace("\r\n", "\n").replace("\r", "\n")
    s = _HTML_COMMENT_RE.sub(" ", s)
    s = _FENCE_LINE_RE.sub(" ", s)
    s = _IMAGE_RE.sub(r"\1", s)
    s = _LINK_RE.sub(r"\1", s)
    s = _AUTOLINK_RE.sub(" ", s)
    s = _TABLE_SEP_RE.sub(" ", s)
    s = s.replace("|", " ")
    s = _LIST_MARKER_RE.sub("", s)
    s = _HEADING_RE.sub("", s)
    s = _QUOTE_RE.sub("", s)
    s = _EMPHASIS_RE.sub("", s)
    s = _WS_RE.sub(" ", s).strip()
    return s


def measure(body: str) -> int:
    """Return the useful-content code-point count of `body` (see `normalize`)."""
    return len(normalize(body))


def evaluate(body: str, limit: int = PR_BODY_USEFUL_CONTENT_LIMIT) -> tuple[bool, dict]:
    """Return `(ok, evidence)` for `body` against `limit`.

    `ok` is True when the useful-content count is `<= limit`. `evidence` carries
    `raw_code_points`, `useful_content_code_points`, `limit`, and `overage`.
    """
    raw = len(body)
    useful = measure(body)
    overage = max(0, useful - limit)
    return overage == 0, {
        "raw_code_points": raw,
        "useful_content_code_points": useful,
        "limit": limit,
        "overage": overage,
    }


_NORMALIZATION_NOTE = (
    "(HTML comments, link targets, list/heading/table syntax, and whitespace runs removed)"
)


def format_evidence(ok: bool, evidence: dict) -> str:
    """Render the human-readable evidence block printed to the check log."""
    verdict = "PASS" if ok else "FAIL"
    lines = [
        f"PR description useful-content check: {verdict}",
        "",
        f"  raw code points ............. {evidence['raw_code_points']}",
        f"  useful content code points .. {evidence['useful_content_code_points']}",
        f"      {_NORMALIZATION_NOTE}",
        f"  limit ...................... {evidence['limit']}",
        f"  overage ................... {evidence['overage']}",
    ]
    if not ok:
        lines += [
            "",
            "The limit is a generous ceiling, not the per-field size guidance in",
            "policies/github-issue-pr-authoring.md. A body over it usually restates the",
            "Issue, the diff, or validation logs — link those instead of reproducing them.",
        ]
    return "\n".join(lines)


def _body_from_args(args: argparse.Namespace) -> str | None:
    """Resolve the PR body from the one source selected on the command line.

    `main()` passes these through a `required=True` mutually exclusive group, so
    exactly one of `--github-event` / `--body-file` / `--stdin` is always set.
    Returns `None` only when `--github-event` points at a payload with no
    `pull_request` object.
    """
    if args.github_event is not None:
        with open(args.github_event, encoding="utf-8") as handle:
            event = json.load(handle)
        pull_request = event.get("pull_request")
        if not isinstance(pull_request, dict):
            print("error: event payload has no 'pull_request' object", file=sys.stderr)
            return None
        return pull_request.get("body") or ""
    if args.body_file is not None:
        with open(args.body_file, encoding="utf-8") as handle:
            return handle.read()
    return sys.stdin.read()


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, evaluate the body, print the evidence, return 0/1."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--github-event", metavar="PATH", help="path to the GitHub event payload JSON ($GITHUB_EVENT_PATH)")
    source.add_argument("--body-file", metavar="PATH", help="path to a file containing the PR body")
    source.add_argument("--stdin", action="store_true", help="read the PR body from stdin")
    parser.add_argument(
        "--limit",
        type=int,
        default=PR_BODY_USEFUL_CONTENT_LIMIT,
        help=f"override the ceiling (default {PR_BODY_USEFUL_CONTENT_LIMIT}); for testing / local use",
    )
    args = parser.parse_args(argv)

    body = _body_from_args(args)
    if body is None:
        return 1

    ok, evidence = evaluate(body, args.limit)
    print(format_evidence(ok, evidence))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
