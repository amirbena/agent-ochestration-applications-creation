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

### Before Starting Work

- Inspect `git status`.
- Determine the current branch and current HEAD.
- Identify the repository's default/upstream branch when available.
- Fetch the remote before starting new work when a remote exists.
- Verify work starts from the expected/latest base.
- Never silently overwrite or discard unrelated local changes — if the working tree
  contains unrelated changes, stop and report them instead of proceeding.

### Branching

Preferred naming convention:

```text
feature/<clear-feature-name>
```

Other allowed prefixes:

```text
fix/
refactor/
docs/
chore/
test/
```

Prefer a clear, semantic branch name over an issue-number-only or vague name. Examples:

```text
feature/backend-agent
feature/team-lead-orchestration
fix/openapi-validation
refactor/agent-runtime-boundary
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
    -> open code review / pull request
```

A failed synchronization/rebase/merge must be reported back to the orchestrating Agent
(or user), never silently treated as success.

### Safety

Destructive Git operations must never be used merely to make the repository appear clean.
The following require explicit justification and authorization before use:

```text
git reset --hard
git clean -fd
force push
discarding unrelated changes
```

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
