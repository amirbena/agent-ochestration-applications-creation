# AGENTS.md

This is the **canonical, runtime-neutral, repository-wide entrypoint** for development of
this repository. Every task starts here — read the **Global Invariants** and
**Instruction Precedence** below, then follow the **Task Routing** table into the one
focused policy that owns your task's detailed rules.

It must remain usable by any compatible coding runtime (Claude Code, Codex, Cursor, or
others). Runtime-specific files (e.g. [CLAUDE.md](CLAUDE.md)) are thin adapters that
bootstrap a runtime into reading this file, its routed policies, and the applicable Agent
Skill — they never become the canonical source of behavior.

This file, and the [policies/](policies/) it routes to, govern **development of this
repository itself**. How an Agent behaves when performing its role is defined by that
Agent's own `SKILL.md` under [agents/](agents/).

## Repository Purpose

An agent orchestration system for software generation. A user describes an application or
website in natural language; the system interprets that requirement and coordinates
specialized software-engineering Agents to design, implement, test, review, secure,
package, and eventually release the resulting software.

The repository is in its **foundation stage**: only repository-wide conventions and the
first Agent (the Backend Agent) exist. Orchestration (the Team Lead) is not implemented
yet. See [Scope of This Repository Today](#scope-of-this-repository-today).

## Core Vocabulary: Agent via Skill

```text
Agent
= a stable software-engineering role in the orchestration system,
  independent of any runtime (Backend, Frontend, Architect, QA, DevOps,
  Security, Release, Team Lead, …). Defined by responsibility and scope.

Skill
= the portable operational definition of an Agent — instructions,
  policies, runbooks, templates — authored once, consumed by any runtime.

Subagent / Worker
= an optional internal execution mechanism an Agent uses to decompose its
  own work. An implementation detail, never the definition of the Agent,
  and never a top-level orchestration unit.

Runtime
= the environment consuming/executing a Skill (Claude Code, Codex,
  Cursor, or any other compatible coding agent).
```

**Canonical principle:**

```text
Agent via Skill
```

Each Agent is defined by its own `SKILL.md`, not by a runtime-specific worker syntax.
Runtime adapters (e.g. `CLAUDE.md`) may exist separately but never redefine an Agent.

## Global Invariants

These apply to **every** task. Each is a short invariant here; the detailed rule lives in
the routed policy named after it.

- **Runtime neutrality.** Canonical repository behavior — this file, `policies/`, and
  each Agent's `SKILL.md` and its `policies/`, `runbooks/`, `templates/`, `metadata/` —
  must not depend on runtime-specific tools, APIs, or subagent-orchestration syntax.
  Adapters may exist separately but never fork these rules. Canonical:
  [policies/skill-development-policy.md](policies/skill-development-policy.md).
- **Dedicated task branch.** Every materially separate task runs on a freshly created
  task branch off synchronized `main`; never implement directly on `main` or continue on
  a previous task's branch, and never discard or blend unrelated local work to get
  there. Canonical: [policies/repository-workflow.md](policies/repository-workflow.md).
- **Safe Git behavior.** Destructive Git shortcuts (`git reset --hard`, `git clean -fd`,
  force push, ancestry-hiding branch deletion, history rewriting for convenience) are
  prohibited; on unexpected state — preserve, inspect, report, do not guess. Canonical:
  [policies/git-pr-merge-policy.md](policies/git-pr-merge-policy.md).
- **Clean task exit.** Every task finishes in a known clean state — the right branch,
  intended work committed, no unrelated modifications, no stray generated or cache
  artifacts, no destructive cleanup used to manufacture that state. Canonical:
  [policies/validation-and-clean-exit.md](policies/validation-and-clean-exit.md).
- **Packaged Agent Skills are independent of root repository-development instructions.**
  No operational file under `agents/<agent>/` (`SKILL.md`, `metadata/`, `policies/`,
  `runbooks/`, `templates/`) may depend on this repository's `AGENTS.md`, `CLAUDE.md`,
  `README.md`, or `policies/`; the Skill must stay correct if consumed on its own.
  Canonical: [policies/skill-development-policy.md](policies/skill-development-policy.md).
- **Architecture authority belongs to the owning Agent.** Architecture decisions
  (technology stack, service decomposition, high-level contracts) belong to the
  appropriate architecture authority (a future Architect Agent), not to the Agent
  implementing the work. Any cross-Agent or architectural change is escalated to the
  owning Agent — or, in the future, the Team Lead — never resolved unilaterally by the
  implementing Agent. How this applies to a specific role is in that Agent's `SKILL.md`.
- **Parallelize independent work; serialize shared mutable state.** Parallel execution is
  an optimization, never a correctness requirement — everything must remain correct run
  sequentially. Independent tasks may run concurrently; a shared mutable contract (API
  schema, shared file, shared dependency, migration sequence, generated code) is a
  synchronization boundary and must be serialized or explicitly coordinated. Conflicting
  parallel assumptions are escalated, never silently resolved. This applies equally
  across top-level Agents and within one Agent's own workers. This repository does not
  implement a parallel execution engine — only the rule.
- **One canonical home per normative rule.** A normative rule has exactly one canonical
  location. Other files — this one included — summarize and link; they never restate a
  rule in a way that can drift independently.
- **Concise, layered PR descriptions.** A Pull Request body is a concise review delta —
  what changed and why, where the canonical detail lives, how it was validated, and what a
  reviewer needs to know — not a second specification. Detailed requirements, design
  rationale, policy text, and history stay in the Issue and canonical documents and are
  linked, not reproduced; the diff is not restated. Canonical:
  [policies/github-issue-pr-authoring.md](policies/github-issue-pr-authoring.md).

## Instruction Precedence

When instructions overlap, the more specific and more authoritative source wins, in this
order:

1. **The user's / calling task's explicit instructions** for the task at hand.
2. **This file's Global Invariants**, and the canonical `policies/` file the task routes
   to. Where a Global Invariant above is only a summary, the routed policy's full text is
   authoritative.
3. **The applicable Agent's canonical Skill sources** — that Agent's `SKILL.md` and its
   own `policies/`, `runbooks/`, `templates/`, and `metadata/` — for how that Agent
   performs its role.
4. **Explanatory documentation** — `README.md`, `docs/`, each Agent's `README.md`, and
   navigational READMEs — which describes and navigates but never overrides a canonical
   source.

Architecture-authority semantics are unchanged by this ordering: an implementing Agent
never overrides an architecture decision it does not own, regardless of where an
instruction appears (see the Global Invariant above and the Agent's `SKILL.md`).

## Canonical vs. Explanatory

**Canonical** (defines behavior):

```text
AGENTS.md
policies/
agents/<agent>/SKILL.md
agents/<agent>/policies/
agents/<agent>/runbooks/
agents/<agent>/templates/
```

**Explanatory** (describes and navigates, never overrides):

```text
README.md
docs/
agents/<agent>/README.md
navigational READMEs (e.g. policies/README.md, agents/backend/runbooks/README.md)
```

An explanatory file that appears to conflict with a canonical one is a documentation bug
to fix, not a competing rule.

## Task Routing

Read this file's Global Invariants and Instruction Precedence for **any** task. Then read
the one policy that owns your task. For a directory map of the routed policies, see
[policies/README.md](policies/README.md) (navigational only).

| Task / concern | Canonical instruction source |
| --- | --- |
| Any repository task | this file — **Global Invariants** + **Instruction Precedence** |
| Start-of-task inspection, base synchronization, preserving unrelated work, dedicated task branch before editing, one scope per branch, resuming an active task branch, branch naming, failed-synchronization behavior | [policies/repository-workflow.md](policies/repository-workflow.md) |
| Commit discipline, pre-push synchronization, push safety, PR creation and authenticated-creator assignment, squash-merge default, merge safety, admin fallback, post-merge cleanup, verified squash `-D` exception, destructive-Git prohibitions | [policies/git-pr-merge-policy.md](policies/git-pr-merge-policy.md) |
| Running the applicable validators/tests, validating changed artifacts by scope, reviewing the final diff, cache/artifact hygiene, the clean end state, final branch/HEAD reporting, preserving unexpected state | [policies/validation-and-clean-exit.md](policies/validation-and-clean-exit.md) |
| Content and shape of agent-authored GitHub Issues and Pull Requests — per-field size guidance, linking canonical docs instead of embedding them, the PR what/why/validation/reviewer-focus shape | [policies/github-issue-pr-authoring.md](policies/github-issue-pr-authoring.md) |
| Authoring Agent Skills — the `agents/<agent>/` layout, runtime neutrality, the portable-Skill boundary, packaged-Skill independence, repository-vs-Agent policy, no premature `shared/` | [policies/skill-development-policy.md](policies/skill-development-policy.md) |

If a task is not covered by a row above, it is governed by the Global Invariants alone,
and a new focused policy should be added (see [Maintainability](#maintainability)) rather
than expanding this file with detailed procedure.

## Repository Layout

```text
AGENTS.md            this file — global invariants, precedence, routing (canonical)
CLAUDE.md            thin Claude Code adapter that bootstraps into AGENTS.md (not a second source of rules)
README.md            project overview (explanatory)
policies/            repository-development policy domains, routed from this file
  README.md          navigational map
  repository-workflow.md
  git-pr-merge-policy.md
  validation-and-clean-exit.md
  github-issue-pr-authoring.md
  skill-development-policy.md
.github/
  ISSUE_TEMPLATE/
    engineering-task.yml   the Phase-1 engineering-backlog Issue Form
    config.yml             blank issues disabled
  PULL_REQUEST_TEMPLATE.md
agents/
  backend/           Backend Agent Skill (see agents/backend/SKILL.md)
    SKILL.md         canonical Backend Agent definition
    metadata/        declarative Skill identity/capabilities/contract shape
    policies/
      global/        universal backend engineering standard (CODE-STANDARDS.md)
      languages/     per-language standards (CODE-STANDARDS.md), e.g. languages/typescript/
      frameworks/    per-framework standards (CODE-STANDARDS.md), e.g. frameworks/nestjs/
    templates/       reusable backend implementation starting points / contracts
    runbooks/        repeatable backend engineering workflows
scripts/             deterministic repository validation tooling
tests/               deterministic repository + Agent-contract tests
```

Future Agents (Frontend, Architect, QA, DevOps, Security, Release, Team Lead, …) follow
the same `agents/<agent-name>/SKILL.md` convention. There is no `shared/` layer — see
[policies/skill-development-policy.md](policies/skill-development-policy.md), "No premature
`shared/`".

## Maintainability

**One normative rule has one canonical home.** `AGENTS.md` is a routing layer, not a
procedural monolith: it keeps only genuinely global material — repository-wide safety
invariants, instruction precedence, the canonical-vs-explanatory distinction, the task
routing table, the packaged-Skill independence boundary, and this rule.

- Put a **substantial, independently ownable policy domain** in its own focused file
  under `policies/`, and add a routing row above. Prefer a small number of meaningful
  domains over many tiny files.
- Add a rule to the Global Invariants only when it truly applies to *every* repository
  task and is short enough to state as an invariant. Otherwise it belongs in a routed
  policy.
- Never create a second normative copy of a rule. When a concise invariant must appear
  here, phrase it as a summary and route to the canonical policy.
- The criterion is **not** a line count — it is responsibility and discoverability. A new
  coding agent should read this file first and immediately know the global invariants,
  which policy to read next, what is canonical, and what is explanatory.

## Scope of This Repository Today

Implemented: repository foundation, canonical Agent/Git rules, the routed
repository-development policies, the Backend Agent Skill, and the deterministic
repository-validation tooling.

Not yet implemented (may be referenced for context, but do not exist as working
functionality): Team Lead orchestration, Requirements Agent intake, Product Agent,
Architect Agent, Frontend Agent, QA Agent, DevOps Agent, Security Agent, Code Review
Agent, Release Agent, LLM routing, a runtime execution engine, queues, databases, or APIs
for the orchestration platform itself.
