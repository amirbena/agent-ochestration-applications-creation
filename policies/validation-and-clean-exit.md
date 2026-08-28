# Validation and Clean-Exit Policy

Canonical rules for how a task on this repository **finishes**: the validation it runs,
how it inspects its own diff, and the known clean end state it leaves behind.

This is a repository-development policy. It is **not** packaged into any Agent Skill, and
no `agents/<agent>/` resource may depend on it. It governs the exit of a repository task
— it does not define any Agent's own runtime testing behavior (for example, the Backend
Agent's unit/integration testing workflow lives in
[../agents/backend/SKILL.md](../agents/backend/SKILL.md) and its policies/runbooks). See
[../AGENTS.md](../AGENTS.md) for global invariants and routing,
[repository-workflow.md](repository-workflow.md) for task-branch creation, and
[git-pr-merge-policy.md](git-pr-merge-policy.md) for commit/push/PR/merge rules.

## Run the applicable validation

Before committing and before reporting a task complete, run the repository's
deterministic checks from the repository root:

```bash
python3 scripts/validate_repository.py
python3 -m pytest tests -q
```

These are stdlib/pytest only and call no LLM or external API. They check Markdown
integrity (UTF-8, trailing whitespace, tabs, resolvable relative links), required
repository and Agent files, portable-Skill boundaries, and structural Agent contracts.
Also run any additional check a repository instruction file names for the area you
changed.

Validate changed artifacts according to what the change touched:

- Markdown / policy / documentation change → repository validator + tests, and confirm
  links and anchors resolve.
- Issue Form / PR template / workflow YAML change → confirm the YAML parses and the
  repository validator still passes.
- `scripts/` or `tests/` change → run `pytest tests -q` and exercise the new check
  against both a passing and a failing input where practical.

If a check genuinely cannot be run in the environment, report explicitly what could not
be run, why, what was verified instead, and the remaining risk. Never claim a check
passed if it was not run.

## Review the final diff

Before committing:

- read the complete `git diff` (staged and unstaged);
- confirm every change is intended and in scope for this task;
- confirm no unrelated file was modified;
- confirm no debugging scaffolding, scratch file, or editor artifact was left behind;
- confirm no generated or cache artifact is staged or newly tracked — at minimum
  `__pycache__/` directories, `*.pyc` files, and `.pytest_cache/` (these are
  `.gitignore`d; verify none slipped in).

Never delete a file merely because its name resembles a cache artifact — only remove
artifacts confirmed to be generated, untracked build byproducts.

## Clean end state

**A task that ends before merge** finishes with:

- current branch = the dedicated task branch;
- intended work committed;
- working tree clean;
- no unrelated modifications;
- no stray generated or cache artifacts;
- no destructive cleanup used to manufacture that state.

**A task that includes merge and cleanup** finishes per the Final State Contract in
[git-pr-merge-policy.md](git-pr-merge-policy.md): on `main`, `local main == origin/main`,
task branch absent locally and remotely, tracking ref pruned, working tree clean.

Never sacrifice unmerged or unrelated work merely to reach a visually clean status.

## Final reporting

On completion, report:

- the branch worked on and its base;
- files added / modified / deleted, grouped by purpose;
- validation commands run and their results (summarized — e.g. "repository validation
  passed; N tests passed");
- the final HEAD and the final `git status`;
- anything intentionally left for follow-up.

## Unexpected state

If validation, the diff review, or the Git state reveals something unexpected —
local-only commits, divergence, unrelated uncommitted work, an ambiguous conflict, a
missing expected file — **preserve it, inspect it, and report it. Do not delete or
"clean" it to make the task look finished.**
