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
those templates. Per [git-pr-merge-policy.md](git-pr-merge-policy.md), the PR template is
the single source of truth for PR body structure; this policy never forks or restates it,
and never overrides that file's Git/PR mechanics.

This file is the canonical home of the **Concise, layered Issue and PR descriptions**
Global Invariant; [../AGENTS.md](../AGENTS.md) carries only its one-line summary. See
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

Write it in plain, natural language an engineer with no prior repository context could
follow: what is wrong, what should be true once the Issue is done, what is
included/excluded, what must already exist for the work to make sense, and how completion
is checked. This is not a prompt written for an LLM to execute, and not a second design
document — the canonical design lives in the linked HLD/LLD/policy (see
[Information density](#information-density)), and the Issue only explains and scopes the
work.

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
architecture document, or canonical policy — do not paste those into the Issue. See
[Native GitHub relationships](#native-github-relationships) for how `Parent`/`Depends
on`/`Blocks` map to GitHub's native sub-issue and issue-dependency relationships.

### Information density

An Issue carries enough to **understand, scope, and implement** the work — not a full
implementation transcript or a speculative design document. The layered model that
governs PR bodies applies here too: the Issue states intent and desired outcome and
links the canonical detail rather than reproducing it.

- **State the problem and the desired outcome.** Keep Scope and Acceptance Criteria on
  observable results, not on the steps taken to reach them.
- **Link, don't reproduce.** Reference canonical policies, ADRs, architecture documents,
  and related Issues instead of restating context that already lives in them.
- **Name implementation detail only when it is a genuine constraint** — a required
  interface, a compatibility boundary, a fixed sequence. Do not enumerate a
  file-by-file change plan; deciding where a change lands is implementation work.
- **Don't repeat one requirement** across Problem, Goal, Scope, and Acceptance Criteria.
  Each field should add something the others do not.
- **Move substantial extra detail out of the Issue** — into a follow-up Issue or a
  canonical design document — rather than growing the body to hold it.

This is density, not a cap: a larger Issue is fine when the work genuinely needs it (see
[Not a character limit](#not-a-character-limit)).

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
instead of embedding their structure or rules in the Issue. A follow-up implementation
Issue is only opened once the LLD's own *Ready for Implementation* section says so, per
the canonical criteria in that same policy section — do not restate those criteria here.

This canonical-detail boundary matters most for research Issues, since a research Issue's
natural output — questions, findings, a recommendation — is easy to let grow into a
second design document inside the Issue body. Issues #12–#22 are the main place this
could drift: keep the questions, scope, and decision in the Issue, and put the actual
design in the HLD/LLD the research produces.

### Native GitHub relationships

The `Dependencies` field's `Depends on:` / `Blocks:` / `Parent:` text is the
**human-readable summary** of a relationship — not the completed state of it. Each has a
distinct meaning:

| Relationship | Meaning |
| --- | --- |
| `Parent` | This work belongs structurally under that work (a child of an epic or a larger task). |
| `Depends on` / `Blocked by` | This Issue cannot correctly proceed until the referenced Issue is complete. |
| `Blocks` | Another Issue should not proceed until this one is complete. |
| `Related` | Useful context for the reader — no execution ordering, no structural relationship. |

GitHub has two **native** relationship primitives: the parent/sub-issue relationship, and
the issue-dependency relationship (`blocked by` / `blocking`). When a `Parent` or
`Depends on`/`Blocked by`/`Blocks` reference is genuine, the matching native relationship
is the **authoritative graph** and must be created **in the same operation** as the prose
— not left as prose only, and not added later as cleanup. The two primitives are never
conflated: a structural `Parent` relationship is a sub-issue link, never an
issue-dependency, and a `Depends on`/`Blocks` ordering is an issue-dependency, never a
sub-issue link.

`Related` is always prose-only. Never create a native relationship for a `Related`
reference, and never add a `Parent` or a dependency merely because two Issues share a
subject or a label — a relationship is created only when it is genuinely structural
(`Parent`) or genuinely blocking (`Depends on`/`Blocks`).

#### Issue-creation workflow for coding agents

When an agent creates or restructures an Issue's relationships:

1. Inspect repository conventions (this policy, the Issue Form, recent Issues) for shape
   and terminology.
2. Search existing Issues for duplicates or an Issue this one should extend instead.
3. Identify the canonical docs to link (policy, HLD/LLD, template, related Issue) —
   see [Internal linking](#internal-linking).
4. Write a concise Issue following [Information density](#information-density).
5. Create the Issue.
6. If a genuine parent/child relationship exists, create the matching native sub-issue
   relationship.
7. If a genuine dependency exists, create the matching native issue-dependency
   (`blocked by` / `blocking`) relationship.
8. Verify the resulting Issue body and relationship state (e.g. via the GitHub UI or
   `gh api`) — do not assume step 6/7 succeeded silently.

Do not infer a `Parent`, `Depends on`, or `Blocks` relationship from an Issue's title or
subject alone; only record and create a relationship the author can point to a concrete
reason for.

### Internal linking

Link directly to the canonical source — the HLD/LLD, policy, template, Agent contract, or
related Issue — instead of a vague pointer such as "see the architecture document". A
reader should be able to follow one link to the authoritative source, not search for it.
The Issue should still make sense on its own without the reader following every link;
linking replaces reproducing detail, not explaining what the work is.

### Link and reference integrity

[`scripts/validate_repository.py`](../scripts/validate_repository.py) already resolves
every relative Markdown link in the repository against the filesystem and fails on a
broken one, which catches the common case of a stale file reference (a renamed or moved
policy, template, or doc). It does not, and this policy does not add tooling to, validate
`#fragment` anchor targets or bare `#123`-style Issue-number references — checking that an
anchor still names an existing heading, or that a referenced Issue number still exists and
still means what the prose says it means, would require either a live GitHub API call
during validation or a heading/graph model well beyond a stdlib link check. Given the
current backlog's size, this is not worth automating now: a broken anchor or a stale
Issue reference is rare enough to catch in review. Revisit this if repeated stale
references start passing review unnoticed.

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

This policy targets cognitive load and scanability for both Issue and PR bodies. The
per-field sizes above are typical ranges, not thresholds to game, and nothing here — the
enforced ceiling below included — licenses trimming a body below the point of clarity: an
Issue or PR a human or a coding agent cannot act on has been cut too far. Preserve
required review and traceability information; move detail into a linked document rather
than deleting it.

### Enforcement: adopted (PR descriptions only)

A single mechanically enforced ceiling on a PR description's **useful content** is in
place:

- **One authoritative implementation.** [`scripts/pr_description_length.py`](../scripts/pr_description_length.py)
  owns the constant `PR_BODY_USEFUL_CONTENT_LIMIT` and the normalization that defines
  "useful content" — raw text with HTML/template comments, code-fence lines, link and
  image *targets* (visible text kept), list / task / heading / block-quote / table
  syntax, and emphasis markers removed, then whitespace runs collapsed. No second
  body-measurement implementation may be added anywhere.
- **One dedicated Action.** [`.github/workflows/pr-description-length.yml`](../.github/workflows/pr-description-length.yml)
  runs only this check on `pull_request` (`opened` / `edited` / `reopened`) into `main`.
  It is read-only — `permissions: {}`, no token, no PR mutation — and reads the body from
  the event payload rather than the API. A failed status check, with an evidence
  breakdown in the log, is the only signal.
- **A ceiling, not the guidance.** The limit sits far above every real PR body in this
  repository's history, so exceeding it almost always means the body restates the Issue,
  the diff, or validation logs — which this policy already says to link, not reproduce.
  It is a backstop against extreme bloat, not a substitute for the density guidance
  above, and it does not apply to Issue bodies.

Structure stays single-sourced in [../.github/PULL_REQUEST_TEMPLATE.md](../.github/PULL_REQUEST_TEMPLATE.md)
per [git-pr-merge-policy.md](git-pr-merge-policy.md); this gate measures length only.
