# Repository Workflow Policy

Canonical rules for **task branches** in development of this repository: which branch a
task runs on, how the base is synchronized, how unrelated local work is preserved, how a
task branch is named, and what to do when synchronization fails.

This is a repository-development policy. It is **not** packaged into any Agent Skill, and
no `agents/<agent>/` resource may depend on it. It is distinct from how an Agent (e.g.
the Backend Agent) works inside a *target* repository it was assigned — that behavior is
defined in the Agent's own `SKILL.md`. See [../AGENTS.md](../AGENTS.md) for the global
invariants and instruction precedence, and
[git-pr-merge-policy.md](git-pr-merge-policy.md) for commit, push, PR, and merge rules.

## Canonical task lifecycle

```text
receive implementation task
    ↓
inspect repository state (branch / status / HEAD)
    ↓
identify and synchronize the base branch
    ↓
preserve any unrelated local work
    ↓
create a dedicated task branch
    ↓
switch to it
    ↓
implement  →  validate  →  commit  →  push  →  open PR
```

The commit/push/PR/merge stages are owned by
[git-pr-merge-policy.md](git-pr-merge-policy.md); the clean end state is owned by
[validation-and-clean-exit.md](validation-and-clean-exit.md). Until a future Release Agent
automates the publish/merge/cleanup stages, the acting Agent (or user) follows this
lifecycle manually.

## Before starting work

- Inspect `git status`.
- Determine the current branch and current HEAD.
- Identify the repository's default/upstream branch (`main`).
- Fetch/prune the remote before starting new work when a remote exists.
- Verify work starts from the expected, latest base — compare local `main` against
  `origin/main`.
- Never silently overwrite or discard unrelated local changes. If the working tree
  contains unrelated changes, stop and report them instead of proceeding.

## Every materially separate task starts on a dedicated branch

Every materially separate implementation or documentation task begins on a dedicated
branch created from the latest safe base — never directly on `main` (or another
protected/default branch), unless the user explicitly requests an exceptional workflow.
This applies to features, Agent/Skill work, bug fixes, refactoring, test work,
infrastructure changes, governance/policy changes, and documentation changes that are
part of a task.

**Required order — no implementation or documentation file may be modified before step 5
completes:**

1. inspect repository state (current branch, working-tree status, local HEAD);
2. identify the base branch, fetch/prune if a remote exists, and compare against
   `origin/main`;
3. ensure the working tree is clean, or safely preserve unrelated work (see below);
4. create a new task-specific branch from the synchronized base;
5. switch to that branch;
6. only then modify implementation or documentation files.

Creating the branch after edits have already started does not satisfy this rule. If work
began before switching: stop, stash the premature edits, create the branch properly, then
reapply the work.

An acting Agent must never:

- modify files directly on `main` (or another protected/default branch);
- begin implementation before switching to the dedicated task branch;
- continue a new, materially separate task on a branch created for a previous task —
  including a branch that already carries a previous task's commits or an open PR;
- reuse an already-open PR branch for unrelated work;
- mix unrelated tasks on the same implementation branch.

### One implementation scope per task branch

One implementation scope maps to one dedicated task branch. Do not accumulate unrelated
tasks on the same branch: if a new request is materially separate from the current task
and the previous work is completed or merged, start a new branch. Do not create
unnecessary branches for small edits inside the same active task.

### Resuming an already-correct task branch

If the current branch is already clearly the branch for the task at hand — for example an
Agent resuming its own in-progress task — do **not** create a nested or replacement
branch. "Dedicated task branch" means one branch per task, not one branch per work
session on that task. Continue on the existing branch.

### Preserving unrelated local changes when switching (stash discipline)

When the current branch is unrelated to the task at hand and the working tree is not
clean:

1. inspect the local changes before doing anything else — never assume what they are;
2. never discard them (`git reset --hard`, `git checkout .`, `git clean -fd`, or
   equivalent) merely to reach a clean state for the switch;
3. `git stash` them (including untracked content via `-u` when relevant) before
   creating/switching to the task branch;
4. create/switch to the branch that belongs to the current task;
5. `git stash pop` only when the stashed changes are determined to belong to the current
   task — never automatically, and never merely because a stash exists.

If the stashed changes belong to a different task, leave them stashed, report that a
stash exists and what it contains, and do not mix it into the current task branch. Branch
hygiene is never a reason to discard or blend unrelated working-tree changes.

## Branch naming

Preferred:

```text
feature/<clear-description>
```

Supported alternatives:

```text
fix/<clear-fix-name>
refactor/<clear-refactor-name>
docs/<clear-docs-name>
test/<clear-test-name>
chore/<clear-chore-name>
```

A research task may use `research/<clear-topic>` when its output is a research/analysis
artifact rather than an implementation change.

Rules:

- Prefer `feature/` for most new implementation work.
- Use a short, descriptive kebab-case name that describes the work, not only an issue
  number.
- Avoid vague names such as `feature/update`, `fix/stuff`, `changes`, `work`.
- For a task spanning code and documentation, prefer the prefix matching the primary
  purpose.
- Do not reuse an already-merged branch for unrelated work.

Examples:

```text
feature/backend-agent
feature/team-lead-orchestration
fix/openapi-validation
refactor/policy-loading
docs/git-workflow-post-merge-cleanup
research/code-review-repo-governance-adaptation
```

Never work directly on `main`, `master`, or another protected/default branch.

## Synchronization and failed synchronization

Before publishing work:

- fetch the latest remote state;
- check whether the branch is behind or diverged from its base;
- verify the expected HEAD;
- rebase or merge only when appropriate to the repository's workflow;
- never hide a failed rebase or merge.

If a rebase or merge fails:

- stop the Git operation safely when required;
- preserve the working state;
- report the conflict to the caller/user;
- do not guess conflict resolution when intent is ambiguous;
- do not force-push merely to bypass the problem.

A failed synchronization, rebase, or merge is reported back to the orchestrating Agent or
user — never silently treated as success.
