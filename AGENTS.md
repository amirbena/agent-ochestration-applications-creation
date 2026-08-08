# AGENTS.md

This is the canonical, repository-wide instruction file for coding agents working in this
project. It is vendor-neutral: it must remain usable by any compatible coding runtime
(Claude Code, Codex, Cursor, or others). Runtime-specific files (e.g. `CLAUDE.md`) act only
as thin adapters that point back to this file and to the relevant Skills under `agents/`.
They must never become the canonical source of project behavior.

## What this project is

An agent orchestration system for software generation. A user describes an application or
website in natural language; the system interprets that requirement and coordinates
specialized software-engineering Agents to design, implement, test, review, secure,
package, and eventually release the resulting software.

This repository is currently in its **foundation stage**. Only repository-wide conventions
and the first Agent (Backend Agent) exist so far. Orchestration itself (the Team Lead) is
not implemented yet.

## Agent Model

- **Agent** — a stable organizational/software-engineering role in the orchestration
  system, independent of any specific runtime or implementation. Examples: Backend Agent,
  Frontend Agent, Architect Agent, QA Agent, DevOps Agent, Security Agent, Release Agent,
  Team Lead Agent.

- **Skill** — the portable definition and behavior of an Agent: instructions, policies,
  workflows, runbooks, and references required for the Agent to perform its role. Skills
  are what make an Agent portable across runtimes; they contain no runtime-specific
  assumptions.

- **Subagent / Worker** — an internal execution mechanism an Agent may use to decompose its
  own work. Subagents are an implementation detail, not a replacement for the Agent
  abstraction, and are not visible as top-level orchestration units. Example:

  ```text
  Team Lead
    -> Backend Agent
         -> API worker
         -> persistence worker
         -> test worker
  ```

  The Team Lead sees one Backend Agent, regardless of whether that Backend Agent executes
  its work sequentially or delegates internally to workers.

- **Runtime** — the environment executing a Skill (e.g. Claude Code, Codex, Cursor, or
  another compatible coding agent). Core Agent behavior, as defined in a Skill, must never
  depend on a single runtime.

## Architecture Ownership

Architecture decisions (technology stack, service decomposition, high-level contracts,
and similar) belong to the appropriate architecture authority (e.g. a future Architect
Agent), not to the Agent implementing the work. Implementation Agents execute within the
boundaries and decisions they are assigned; they do not independently choose or infer
them. Any change that is cross-Agent or architectural in nature must be escalated to the
owning Agent, or, in the future, the Team Lead — never resolved unilaterally by the
implementing Agent. See the applicable Agent's `SKILL.md` for how this applies concretely
to that Agent's role.

## Parallel Execution Rules

Parallel execution is a first-class capability of this system: multiple Agents and/or
internal subagents may work concurrently. It is an **optimization, not a correctness
requirement** — nothing may rely on parallelism to be correct, and everything must remain
correct if run sequentially.

- Parallelize independent tasks where useful.
- Do not parallelize work that mutates the same files without an explicit ownership
  strategy.
- Do not independently mutate a shared API/schema/contract from multiple workers.
- Do not parallelize tasks when one depends on the output of another.
- A shared mutable contract (API schema, shared file, shared dependency, database
  migration sequence, generated file/code) creates a synchronization boundary; work
  touching it must be serialized or explicitly coordinated.
- Database migrations are ordered and mutate shared state — do not let independent
  parallel workers generate or apply migrations concurrently without coordination.
- Generated files (e.g. generated clients, generated schema code) are derived from a
  shared source; do not let multiple workers regenerate them independently and merge
  divergent output.
- If parallel work produces conflicting assumptions, escalate to the owning Agent, or, in
  the future, to the Team Lead. Do not silently resolve conflicting assumptions.
- Agents must preserve clear file and module ownership during parallel execution.

The same invariant applies whether the parallelism is across top-level Agents (e.g.
Backend and Frontend working concurrently) or internal to one Agent's own
subagents/workers: **parallelize independent work; serialize or explicitly coordinate
shared mutable state.**

This task does not implement a parallel execution engine — only the rules that future
implementations must follow.

## Git Methodology

The full lifecycle for an implementation task:

```text
receive implementation task
    ↓
verify clean/safe base
    ↓
create dedicated task branch
    ↓
implement
    ↓
validate
    ↓
sync with target HEAD
    ↓
push
    ↓
open PR / code review
    ↓
merge
    ↓
switch to main
    ↓
sync main
    ↓
delete task branch locally + remotely
    ↓
clean final state
```

This section defines each stage. A future Release Agent will automate the
publish/merge/cleanup stages; until then, the acting Agent (or user) follows this
lifecycle manually.

### Before Starting Work

- Inspect `git status`.
- Determine the current branch and current HEAD.
- Identify the repository's default/upstream branch when available.
- Fetch the remote before starting new work when a remote exists.
- Verify work starts from the expected/latest base.
- Never silently overwrite or discard unrelated local changes — if the working tree
  contains unrelated changes, stop and report them instead of proceeding.

### Every Implementation Task Starts on a Dedicated Branch

Every implementation task must begin on a dedicated branch created from the latest safe
target branch — not directly on `main` (or another protected/default branch), unless the
user explicitly requests an exceptional workflow. This applies to any implementation
task: new features, Agent/Skill implementation, bug fixes, refactoring, test work,
infrastructure changes, and documentation changes that are part of an implementation
task.

Start-of-task flow:

```text
new implementation task
    ↓
inspect status / branch / HEAD
    ↓
fetch remote
    ↓
synchronize target branch safely
    ↓
create dedicated task branch
    ↓
perform work
```

Before creating the branch, verify: working tree state, current branch, current HEAD,
the intended base branch, the remote/default branch, remote synchronization, and the
absence of unrelated local changes (per "Before Starting Work" above). Never silently
discard work in order to create a branch — if the base isn't safe, stop and report
instead.

**One implementation scope ≈ one dedicated task branch.** Do not accumulate unrelated
tasks on the same branch; if a new request is materially separate from the current task
and the previous work is already completed/merged, start a new branch. Do not create
unnecessary branches for small edits inside the same active task.

### Branching

Preferred naming convention:

```text
feature/<clear-feature-name>
```

Other allowed prefixes:

```text
fix/<clear-fix-name>
refactor/<clear-refactor-name>
docs/<clear-docs-name>
test/<clear-test-name>
chore/<clear-chore-name>
```

Rules:

- Prefer `feature/` for most new implementation work.
- Use a short but descriptive kebab-case name that describes the work, not only an issue
  number.
- Avoid vague names such as `feature/update`, `fix/stuff`, `changes`, `work`.
- Do not reuse an old merged branch for unrelated work — see "One implementation scope"
  above.
- For a task spanning both code and documentation, prefer the prefix matching the
  primary purpose.

Examples:

```text
feature/backend-agent
feature/code-review-agent
feature/team-lead-orchestration
fix/openapi-validation
refactor/policy-loading
docs/git-workflow-post-merge-cleanup
```

Never work directly on `main`, `master`, or another protected/default branch.

### Synchronization

Before publishing work:

- Fetch the latest remote state.
- Check whether the branch is behind or diverged from its base.
- Verify the expected HEAD.
- Rebase or merge only when appropriate to the repository's workflow.
- Never hide a failed rebase or merge.

If `rebase` or `merge` fails:

- Stop the Git operation safely when required.
- Preserve the working state.
- Report the conflict to the caller/user.
- Do not guess conflict resolution when intent is ambiguous.
- Do not force-push merely to bypass the problem.

### Commits

- Keep commits focused; do not mix unrelated cleanup with feature work.
- Use meaningful commit messages.
- Validate relevant functionality before committing when practical.

### Publishing

Before push, confirm:

- Clean/expected working tree.
- Correct branch name.
- Correct HEAD.
- Synchronization with the remote/base.
- Relevant validation has been run.

If push fails because the remote moved: fetch, inspect divergence, resolve through the
normal synchronization workflow, and report failures rather than using destructive Git
commands.

### Pull Requests

A future Release Agent will eventually automate publication and code-review opening. For
now, the principle is:

```text
validated branch
    -> synchronization check
    -> push
    -> open pull request
    -> assign PR creator (when supported)
    -> code review
    -> merge
```

A failed synchronization/rebase/merge must be reported back to the orchestrating Agent
(or user), never silently treated as success. This is the one canonical PR flow for this
section — "Pull Request Assignee" and "Merge Strategy" below add detail to specific
steps in it rather than restating the whole sequence.

#### Pull Request Description

Every implementation PR must use and populate the repository's canonical PR template at
[.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) — GitHub applies it
automatically to new PRs against this repository. The template is the single source of
truth for PR body structure; do not restate or fork it here. Populating it (including
Execution Metadata) does not grant the implementing Agent authority to approve its own
review — see the applicable Agent's `SKILL.md` for review-approval boundaries.

#### Pull Request Assignee

- Determine the authenticated/current Git-hosting user creating the PR.
- When the platform supports PR assignees, assign that same user/account as the
  assignee.
- Use the authenticated platform identity when it can be resolved safely — do not guess
  a username from Git commit metadata, repository ownership, email address, or display
  name.
- If the current user cannot be resolved, or the platform does not support assignees,
  open the PR normally and report that assignment was not applied — this is not a reason
  to block opening the PR.
- Do not assign unrelated users automatically.

Being assigned to a PR is metadata, not approval. It does not mean review approval,
merge approval, or ownership of all implementation concerns raised in review — the flow
above (code review, then merge) is unchanged by who is assigned.

#### Merge Strategy

Prefer **squash merge** for normal feature/fix/task branches — the default desired
result is one focused commit on `main` per merged PR. At the merge step in the flow
above: squash merge, producing a single commit on `main`, followed by the sync and
branch-cleanup steps in "Post-Merge Cleanup" below.

Use a different merge strategy only when:

- the user explicitly requests it;
- repository rules require it;
- preserving the branch's individual commit history is intentionally important for that
  specific change.

Do not create unnecessary merge commits for ordinary task branches. When squash merge is
used, the post-merge cleanup steps below — including the squash-specific branch-deletion
handling — apply as documented in "Post-Merge Cleanup".

### Post-Merge Cleanup

After a pull request is successfully merged:

```text
merged PR
  ↓
confirm merge
  ↓
switch to main
  ↓
fetch/prune
  ↓
synchronize local main with origin/main
  ↓
verify merged content exists
  ↓
delete local task branch
  ↓
delete remote task branch
  ↓
verify clean final state
```

Concretely, the acting Agent must:

- Confirm the PR is actually in the `MERGED` state — do not assume it merged.
- Capture or verify the resulting merge/squash commit.
- Ensure it is safe to leave the feature branch (nothing below is skipped first).
- Switch to `main`.
- Fetch/prune remote state.
- Synchronize local `main` with `origin/main`, preferring fast-forward — see "Main
  Synchronization" below.
- Verify the merged work is actually present on `main`.
- Verify no work exists only on the feature branch (nothing would be lost by removing
  it).
- Delete the local task branch.
- Verify/delete the remote source branch (some hosting platforms auto-delete it on
  merge — verify it is actually gone rather than assuming).
- Prune stale remote-tracking references.
- Finish on `main`, with a clean working tree.

Never delete another Agent's active branch, an unrelated feature branch, or a branch
whose merge state is uncertain.

#### Main Synchronization

```text
fetch
    ↓
inspect local main vs origin/main
    ↓
fast-forward when possible
```

Do not create an unnecessary merge commit merely to update local `main`. If local `main`
contains unexpected local-only commits, stop and report — do not reset/discard them.
Expected successful state: `local main HEAD == origin/main HEAD`.

#### Squash-Merge Local Branch Deletion

A squash merge creates a new commit on `main` rather than preserving the feature
branch's commit ancestry. As a result, `git branch -d <branch>` may refuse to delete the
branch even though the PR was safely squash-merged — that refusal alone does not mean
the work is unmerged.

Before using forced local deletion, verify all of:

1. the PR is confirmed `MERGED`;
2. the resulting squash commit exists on `main`;
3. all intended feature content is present on `main`;
4. the task branch contains no extra work beyond what was merged;
5. the working tree is safe.

```text
safe squash merge verified
    ↓
git branch -d fails due to ancestry
    ↓
content + commit verification
    ↓
local branch force-delete allowed
```

Only after those checks may `git branch -D <merged-task-branch>` be used. This is a
narrowly scoped exception to the destructive-operations rule below (see "Safety") — it
does not generalize to permission for other destructive Git behavior, and branch
deletion must never be used to hide unmerged work.

#### Post-Merge Failure Behavior

If any cleanup step reveals: local-only commits on `main`; additional commits on the
feature/task branch beyond what was merged; uncommitted work; failed synchronization;
unexpected remote divergence; an uncertain PR merge state; missing merged content; or
branch contents that differ unexpectedly from merged `main` — stop and report instead of
deleting anything. Never make branch cleanup more important than preserving potentially
unmerged work.

#### Final State Contract

The canonical completion state for a successfully merged implementation task:

```text
PR = merged
current branch = main
local main = origin/main
task branch = absent locally
task branch = absent remotely
remote tracking reference = absent
working tree = clean
```

### Safety

Destructive Git operations must never be used merely to make the repository appear clean.
The following require explicit justification and authorization before use:

```text
git reset --hard
git clean -fd
force push
discarding unrelated changes
```

The one narrowly scoped exception is forced local deletion of an already-verified,
squash-merged task branch — see "Squash-Merge Local Branch Deletion" above. It does not
extend to any other destructive operation.

## Repository Layout

```text
AGENTS.md            canonical, vendor-neutral, repository-wide instructions (this file)
CLAUDE.md            minimal Claude Code adapter that bootstraps into AGENTS.md; not a
                      second source of rules
README.md            project overview
agents/
  backend/           Backend Agent Skill (see agents/backend/SKILL.md)
    SKILL.md
    policies/
      global/        universal backend engineering standard (CODE-STANDARDS.md)
      languages/      per-language standards (CODE-STANDARDS.md), e.g. languages/typescript/
      frameworks/     per-framework standards (CODE-STANDARDS.md), e.g. frameworks/nestjs/
    templates/        reusable backend implementation starting points
    runbooks/         repeatable backend engineering workflows
```

Future Agents (Frontend, Architect, QA, DevOps, Security, Release, Team Lead, ...) will
follow the same `agents/<agent-name>/SKILL.md` convention when they are added. A future
runtime-specific adapter (analogous to `CLAUDE.md`) must stay a thin bootstrap into
`AGENTS.md` and the applicable Skill — never a second, divergent source of rules.

## Scope of This Repository Today

Implemented: repository foundation, canonical Agent/Git rules, and the Backend Agent Skill.

Not yet implemented (may be referenced in documentation, but do not exist as working
functionality): Team Lead orchestration, Requirements Agent, Product Agent, Architect
Agent, Frontend Agent, QA Agent, DevOps Agent, Security Agent, Code Review Agent, Release
Agent, LLM routing, a runtime execution engine, queues, databases, or APIs for the
orchestration platform itself.
