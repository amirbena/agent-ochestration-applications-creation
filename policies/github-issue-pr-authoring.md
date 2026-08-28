# GitHub Issue / PR Authoring Policy

Canonical rules for the **content of agent-authored GitHub Issues and Pull Requests** for
this repository — how much detail belongs in the GitHub-visible body, and what belongs in
a linked document instead.

This is a repository-development policy. It is **not** packaged into any Agent Skill, and
no `agents/<agent>/` resource may depend on it. It governs the body an author writes; it
does not change the Issue Form fields in
[../.github/ISSUE_TEMPLATE/engineering-task.yml](../.github/ISSUE_TEMPLATE/engineering-task.yml)
or the checklist in
[../.github/PULL_REQUEST_TEMPLATE.md](../.github/PULL_REQUEST_TEMPLATE.md), and it never
overrides the mechanics in [git-pr-merge-policy.md](git-pr-merge-policy.md). See
[../AGENTS.md](../AGENTS.md) for global invariants and routing.

## Principle

**Agent-complete internally, human-scannable externally.** An author may reason as
deeply as the task needs; the Issue or PR body is a briefing for a human, not a
transcript of that reasoning.

## When this applies

Whenever an author **creates, updates, rewrites, or materially expands** a GitHub Issue
or Pull Request body — not only at first creation. When updating, preserve context that
is still useful but compress or replace redundant prose instead of appending another full
status report, so the body does not grow indefinitely.

## Prefer / avoid

**Prefer:** short sections; bullets; a small table where it clarifies; links to the
canonical doc / Issue / ADR / policy / research artifact; concrete evidence; explicit
decisions.

**Avoid:** long narrative; repeated context; restating repository policy; a step-by-step
execution log or implementation diary; verbose validation output; large requirement text
copied from another source.

## Engineering Task Issues

The Issue is a **Phase-1 engineering backlog item** for evolving this repository and its
Agent ecosystem — a Jira-like work item consumed by a human or a coding agent following
the repository development workflow. It is **not** a runtime-Agent assignment and **not**
a normalized requirements contract.

A normal Engineering Task Issue body (fields from the Issue Form) is usually:

| Field | Usual size |
| --- | --- |
| Problem | 1–3 short paragraphs |
| Goal | 1–2 sentences |
| Scope | 3–6 focused bullets |
| Non-Goals | 0–3 bullets |
| Acceptance Criteria | 3–6 observable checkboxes |
| Dependencies | short references (`Depends on:` / `Blocks:` / `Parent:`) |
| Validation | 2–5 concise checks |

`one Issue = one independently observable outcome` — if it has multiple independently
closable deliverables, split it.

When the task genuinely needs more, **link** a research artifact, ADR, parent Issue,
architecture document, or canonical policy — do not paste those into the Issue. Prefer
native GitHub sub-issues for parent/child relationships when available.

### Parent / Epic Issues

Shorter still: a one-paragraph goal, short context, a child-issue checklist, and the key
dependencies. Detailed requirements live in the child Issues, not the parent.

### Research Issues

A research Issue may run a little longer, but the body stays focused on the **questions**,
the **scope**, the **evidence required**, and the **expected decision / output**. The
detailed findings belong in the research/analysis artifact the Issue produces, not in the
Issue body.

## Pull Requests

The body answers four questions: **what changed**, **why**, **how it was validated**, and
**anything a reviewer should look at closely**. Fill the applicable sections of
[../.github/PULL_REQUEST_TEMPLATE.md](../.github/PULL_REQUEST_TEMPLATE.md) and mark the
rest `None` / `N/A`.

Summarize validation:

```text
repository validation passed
N tests passed
git diff reviewed — no unrelated changes
```

Do not include: a full chronology of the work; every command run; full test output; the
Issue's requirements restated; architecture already documented elsewhere; large code
already visible in the diff; filler such as "carefully reviewed all files". Link the
Issue or the document instead.

## Not a character limit

This policy targets cognitive load and scanability, not a line or character count. The
sizes above are typical ranges, not thresholds to game, and nothing here licenses
trimming a body below the point of clarity. Preserve required review and traceability
information; move detail into a linked document rather than deleting it.
