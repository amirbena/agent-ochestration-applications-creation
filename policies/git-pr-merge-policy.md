# Git / PR / Merge Policy

Canonical rules for **commits, pushes, Pull Requests, merges, post-merge cleanup, and
destructive-Git prohibitions** in development of this repository.

This is a repository-development policy. It is **not** packaged into any Agent Skill, and
no `agents/<agent>/` resource may depend on it. It governs development of *this*
repository only — it is distinct from how an Agent works inside a target repository it
was assigned (see that Agent's `SKILL.md`). See
[repository-workflow.md](repository-workflow.md) for task-branch creation and base
synchronization, [validation-and-clean-exit.md](validation-and-clean-exit.md) for the
clean end state, and [../AGENTS.md](../AGENTS.md) for global invariants and routing.

## Lifecycle (publication onward)

```text
task branch
    ↓
validate
    ↓
synchronize with target HEAD
    ↓
push
    ↓
open PR
    ↓
assign authenticated PR creator (when supported)
    ↓
code review
    ↓
squash merge by default
    ↓
switch to main
    ↓
sync main with origin/main
    ↓
delete task branch locally + remotely
    ↓
prune
    ↓
clean final state
```

## Commit discipline

- Keep commits focused; do not mix unrelated cleanup with feature work.
- Use meaningful commit messages that describe intent, not a file list.
- Split a task into focused commits when that aids review; do not rewrite history merely
  for aesthetics.
- Validate relevant functionality before committing when practical (see
  [validation-and-clean-exit.md](validation-and-clean-exit.md)).

## Before push

Confirm:

- clean, expected working tree;
- correct branch name;
- correct HEAD;
- synchronization with the remote/base (fetch, inspect divergence);
- relevant validation has been run.

If push fails because the remote moved: fetch, inspect divergence, resolve through the
normal synchronization workflow in [repository-workflow.md](repository-workflow.md), and
report failures rather than using destructive Git commands.

## Pull Request creation

- Open the PR from the dedicated task branch against `main`.
- Populate the repository's canonical PR template at
  [../.github/PULL_REQUEST_TEMPLATE.md](../.github/PULL_REQUEST_TEMPLATE.md) — GitHub
  applies it automatically. The three sources do not overlap: the **template** is the
  single source of truth for PR body *structure* (do not restate or fork it),
  [github-issue-pr-authoring.md](github-issue-pr-authoring.md) owns PR body *content*
  guidance, and the **Concise, layered PR descriptions** Global Invariant in
  [../AGENTS.md](../AGENTS.md) is the one-line summary that routes to that policy.

### PR assignee

- Resolve the authenticated Git-hosting identity creating the PR.
- When the platform supports assignees, assign that same account.
- Never infer the assignee from Git commit metadata, email, repository ownership, or
  display name.
- If assignment cannot be resolved, or the platform has no assignees, open the PR
  normally and report that assignment was not applied — this never blocks opening the PR.
- Do not assign unrelated users automatically.

**PR assignment is metadata, not approval.** It is not review approval, merge approval,
or ownership of every concern raised in review. Execution participation recorded in the
PR template (such as a "Produced by" note in the specialized-impact block) likewise does
not grant self-review authority — review approval follows the applicable Agent's
`SKILL.md` review-approval boundaries.

## Merge strategy

Default: **squash merge** — one focused commit on `main` per merged PR.

```text
task branch commits  →  one focused squash commit  →  main
```

Use another strategy only when the user explicitly requests it, repository rules require
it, or preserving the branch's individual commit history is intentionally necessary for
that specific change. Do not create unnecessary merge commits for ordinary task branches.

## Merge safety

Before merge:

- re-fetch;
- verify PR state;
- verify the reviewed HEAD matches the current HEAD — no new unreviewed commits appeared;
- inspect checks;
- inspect reviews;
- inspect unresolved comments;
- inspect mergeability.

Attempt a normal squash merge first. Administrative privileges may be used **only** when
the PR is otherwise safe and a normal merge is blocked solely by an
administrative/protection gate. Never use admin privileges to bypass conflicts, failing
validation, requested changes, blocking review findings, or correctness/safety problems.

## Post-merge cleanup

```text
confirm PR is MERGED
    ↓
capture the resulting squash/merge commit
    ↓
switch to main
    ↓
fetch / prune
    ↓
synchronize local main with origin/main (prefer fast-forward)
    ↓
verify merged content is present on main
    ↓
verify nothing exists only on the task branch
    ↓
delete the local task branch
    ↓
delete the remote task branch (verify auto-delete actually happened)
    ↓
prune stale remote-tracking refs
    ↓
finish on main with a clean working tree
```

Never delete another Agent's active branch, an unrelated feature branch, or a branch
whose merge state is uncertain.

### Main synchronization

```text
fetch  →  inspect local main vs origin/main  →  fast-forward when possible
```

Do not create an unnecessary merge commit merely to update local `main`. If local `main`
carries unexpected local-only commits, stop and report — do not reset or discard them.
Expected successful state: `local main HEAD == origin/main HEAD`.

### Squash-merge local branch deletion (verified exception)

A squash merge creates a new commit on `main` rather than preserving the task branch's
ancestry, so `git branch -d <branch>` may refuse to delete a safely squash-merged
branch. That refusal alone does not mean the work is unmerged.

Before using the forced form, verify all of:

1. the PR is confirmed `MERGED`;
2. the resulting squash commit exists on `main`;
3. all intended task content is present on `main`;
4. the task branch contains no extra work beyond what was merged;
5. the working tree is safe.

```text
safe squash merge verified
    ↓
git branch -d fails due to ancestry
    ↓
content + commit verification
    ↓
git branch -D <merged-task-branch> allowed
```

This is a narrow post-merge cleanup exception only. Branch deletion must never be used to
hide unmerged work, and this exception does not generalize to any other destructive Git
behavior.

### Post-merge failure behavior

If any cleanup step reveals local-only commits on `main`, extra commits on the task
branch beyond what was merged, uncommitted work, failed synchronization, unexpected
remote divergence, an uncertain PR merge state, missing merged content, or branch
contents that differ unexpectedly from merged `main` — stop and report instead of
deleting anything. Never make branch cleanup more important than preserving potentially
unmerged work.

### Final state contract

```text
PR = merged
current branch = main
local main = origin/main
task branch = absent locally
task branch = absent remotely
remote tracking reference = absent
working tree = clean
```

## Git safety

Destructive Git operations must never be used merely to make the repository appear clean.
The following require explicit justification and authorization before use:

```text
git reset --hard
git clean -fd
force push
branch deletion used to hide divergence or unmerged work
history rewriting merely to simplify review
```

The one narrowly scoped exception is the verified forced local deletion of an
already-squash-merged task branch, above.

If the repository contains unexpected local commits, divergence, ambiguous conflicts,
unrelated uncommitted work, or an uncertain merge state:

```text
preserve state  →  inspect  →  report  →  do not guess
```
