# Repository Policies

These policies govern **development and maintenance of this repository itself** —
branching, commits, pull requests, merges, validation, task exit, and how Agent Skills
are authored. They are the routed targets of the **Task routing** table in
[../AGENTS.md](../AGENTS.md); the normative rules live in the individual policy files, not
in this README.

## Start here

[../AGENTS.md](../AGENTS.md) is the repository-wide entrypoint. Read its **Global
Invariants** and **Instruction Precedence** first, then follow its **Task routing** table
to the one policy below that owns your task.

## Repository policy vs. Agent Skill policy

This distinction is deliberate and must stay explicit.

```text
/policies/                     rules for developing THIS repository
                               (branching, PRs, merges, validation, Skill authoring).
                               Never packaged with an Agent Skill. Never consumed by an
                               Agent performing its role.

/agents/<agent>/policies/      portable behavior / engineering rules used by that Agent
                               while it performs its role. Consumed wherever the Skill
                               runs. Independent of this directory and of /AGENTS.md.
```

If a rule is needed by an Agent Skill at runtime, its canonical home is inside that
Skill (`agents/<agent>/SKILL.md`, `.../policies/`, `.../runbooks/`, `.../templates/`,
`.../metadata/`) — never a file in this directory.

## Policy map

| Policy | Purpose (short) |
| --- | --- |
| [repository-workflow.md](repository-workflow.md) | Start-of-task inspection, base synchronization, preserving unrelated work, dedicated task branch before editing, one scope per branch, resuming an active task branch, branch naming, failed-synchronization behavior. |
| [git-pr-merge-policy.md](git-pr-merge-policy.md) | Commit discipline, pre-push synchronization, push safety, PR creation and authenticated-creator assignment, squash-merge default, merge-safety checks, admin fallback, post-merge cleanup, verified squash `-D` exception, destructive-Git prohibitions. |
| [validation-and-clean-exit.md](validation-and-clean-exit.md) | Running the applicable validators/tests, validating changed artifacts by scope, reviewing the final diff, cache/artifact hygiene, the clean-working-tree end state, final branch/HEAD reporting, and preserving unexpected state instead of deleting it. |
| [github-issue-pr-authoring.md](github-issue-pr-authoring.md) | Content and shape of agent-authored GitHub Issues and Pull Requests: human-scannable bodies, per-field size guidance, linking canonical docs instead of embedding them, and the PR what/why/validation/reviewer-focus shape. |
| [skill-development-policy.md](skill-development-policy.md) | Authoring Agent Skills: the `agents/<agent>/` layout, runtime neutrality, the portable-Skill boundary, independence of packaged Skills from root repository-development instructions, and why `shared/` is not introduced yet. |

## Ownership rule

**One normative rule has one canonical home.** [../AGENTS.md](../AGENTS.md) keeps only a
short invariant plus a routing link; the routed policy owns the detailed rule. Do not
create a second normative copy of a rule in `../AGENTS.md`, in another policy, in
`docs/`, or in a README.

## Adding or changing a policy

1. If the rule applies to **every** repository task and is short, state it as an
   invariant in `../AGENTS.md` and stop.
2. If it is a substantial, independently ownable domain, add or extend a focused file
   here and add a row to the `../AGENTS.md` **Task routing** table. Prefer a small number
   of meaningful domains over many tiny files.
3. If the rule is needed by an Agent Skill at runtime, put it under
   `../agents/<agent>/` — never here.
4. Keep cross-references as relative Markdown links and run repository validation
   (`python3 scripts/validate_repository.py`, `python3 -m pytest tests -q`).
