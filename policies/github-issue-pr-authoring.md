# GitHub Issue / PR Authoring Policy

Canonical rules for the **content of agent-authored GitHub Issues and Pull Requests** for
this repository — how much detail belongs in the GitHub-visible body, and what belongs in
a linked document instead.

This is a repository-development policy. It is **not** packaged into any Agent Skill, and
no `agents/<agent>/` resource may depend on it. It governs the body an author writes, not
the field or section structure of the templates: the Issue Form fields in
[../.github/ISSUE_TEMPLATE/engineering-task.yml](../.github/ISSUE_TEMPLATE/engineering-task.yml)
and the sections of
[../.github/PULL_REQUEST_TEMPLATE.md](../.github/PULL_REQUEST_TEMPLATE.md) are owned by
those templates. The PR template is the single source of truth for PR body structure;
this policy never forks or restates it, and it never overrides the Git/PR mechanics in
[git-pr-merge-policy.md](git-pr-merge-policy.md).

This file is the canonical home of the **Concise, layered PR descriptions** Global
Invariant; [../AGENTS.md](../AGENTS.md) carries only its one-line summary. See
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

When the research designs an Agent, state the applicable deliverables as
`docs/agents/<agent-name>/HLD.md` and `docs/agents/<agent-name>/LLD.md`. Link the
[canonical HLD template](../docs/templates/AGENT_HLD_TEMPLATE.md),
[canonical LLD template](../docs/templates/AGENT_LLD_TEMPLATE.md), and the
[Skill-development policy](skill-development-policy.md#agent-research-and-design-documents)
instead of embedding their structure or rules in the Issue.

## Pull Requests

### The layered model

The Issue and the canonical documents own the detail; the Pull Request owns the delta.

- **Issue / canonical docs** (policy, ADR, HLD/LLD, parent Issue, commit history, the diff
  itself) own detailed requirements, design rationale, normative rules, and history.
- **The PR body** owns a concise **review delta**: what changed and why, where the
  canonical detail lives, how it was validated, what risk remains, and anything a
  reviewer specifically needs to know. It is a change summary and a navigation surface —
  **not a second specification** and not a re-derivation of anything above.

Fill the applicable sections of
[../.github/PULL_REQUEST_TEMPLATE.md](../.github/PULL_REQUEST_TEMPLATE.md) and mark the
rest `None` / `N/A`.

### Concrete preferences

- **"What changed": 2–5 high-value bullets**, grouped by behavior or intent. Add a
  labeled sub-bullet (behavior / contract, governance / policy, portability / packaging)
  only for a dimension that actually changed.
- **No mechanical changed-file or changed-surface inventory.** The diff already lists the
  files and the surfaces touched; do not restate them section by section.
- **Link, don't reproduce.** Reference the Issue, canonical policy, ADR, or design doc
  instead of copying requirements, design history, or policy text into the body. If a
  reviewer needs the "why" in depth, the link is the answer.
- **Summarize validation; never paste logs.** State the checks run and their outcome, for
  example:

  ```text
  repository validation passed
  N tests passed
  git diff reviewed — no unrelated changes
  ```

  Omit a full chronology of the work, every command run, and full command or test output.
- **Reviewer notes are for the non-obvious only** — decisions a reviewer could not infer
  from the diff, subtle behavior, deliberate trade-offs, and where to focus. Write
  `None.` when there is nothing to flag; do not narrate routine work.
- **Keep Risk / Impact when it materially helps review** — a short `Low / Medium / High`
  line plus a sentence or two on breaking, runtime, migration, contract, or security
  impact. Drop it to `None.` when the change carries no meaningful risk rather than
  padding it.
- **Specialized impact stays optional and collapsed.** Governance-surface and
  agent/orchestration metadata (e.g. which Agent produced the change) go in the
  template's collapsible block and only where they add genuine repository value — never
  as always-filled ceremony. Execution participation recorded there is metadata, never
  review approval (see [git-pr-merge-policy.md](git-pr-merge-policy.md)).

Do not include: filler such as "carefully reviewed all files"; architecture already
documented elsewhere; large code already visible in the diff; the Issue's requirements
restated.

## Not a character limit

This policy targets cognitive load and scanability, not a line or character count. The
sizes above are typical ranges, not thresholds to game, and nothing here licenses
trimming a body below the point of clarity. Preserve required review and traceability
information; move detail into a linked document rather than deleting it.

### Enforcement: evaluated, not adopted

A mechanically enforced useful-content limit (a `pull_request` workflow running a
`scripts/pr_description_length.py` with a single authoritative code-point constant, a
defined normalization algorithm, and an evidence table — as the sibling
`amirbena/code-review-skill` repository does) was considered and **is not adopted now**:

- Simplifying the template removes the structural driver of oversized PR bodies — the
  mechanical changed-surface inventory and the always-filled specialized blocks — so the
  concrete problem is addressed without a numeric gate.
- A byte gate adds a second body-measurement concern plus a normalization spec and an
  evidence table to maintain, against this repository's deliberately minimal,
  stdlib-only validation surface at foundation stage.
- A number invites gaming (splitting content across links purely to duck the counter)
  without improving scanability, which is what this section already optimizes for.

Revisit this decision if, after the template change, PR bodies still trend long in
practice; that would provide the evidence needed to size a limit. If it is later adopted,
reuse one authoritative constant and add no second body-measurement implementation.
