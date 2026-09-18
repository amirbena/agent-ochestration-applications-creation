# Skill Development Policy

Canonical rules for **authoring Agent Skills in this repository**: the `agents/<agent>/`
layout, runtime neutrality, the portable-Skill boundary, the independence of Agent Skills
from root repository-development instructions, and why a `shared/` layer is not
introduced yet.

This is a repository-development policy. It is **not** packaged into any Agent Skill, and
no `agents/<agent>/` resource may depend on it. See [../AGENTS.md](../AGENTS.md) for the
global invariants, instruction precedence, and task routing.

## Agent via Skill

```text
Agent   = a stable software-engineering role in the orchestration system
          (Backend, Frontend, Architect, QA, DevOps, Security, Release, Team Lead, …)
Skill   = the portable operational definition of that Agent
          (SKILL.md + metadata + policies + runbooks + templates)
```

Each Agent lives under `agents/<agent>/` and is defined by its own `SKILL.md`. Do **not**
rename `agents/` to `skills/`: the repository models *Agents* (roles), each *defined by*
a Skill.

```text
agents/
  backend/
  frontend/        (future)
  architect/       (future)
  ...
```

An Agent may internally use subagents/workers to decompose its own work; that is an
execution detail and never redefines the Agent or its external contract.

## Runtime neutrality

Canonical Agent resources — `SKILL.md`, `metadata/`, `policies/`, `runbooks/`,
`templates/` — must not depend on a specific runtime: no Claude-, Anthropic-, Codex-, or
Cursor-specific tool names, APIs, or subagent-orchestration syntax. Express external
dependencies as capabilities (e.g. "a test runner the repository configures"), not as a
required vendor implementation.

Runtime-specific adapter files (e.g. the repository-root `CLAUDE.md`) may improve
discovery or presentation for one consumer, but they remain **thin**: they bootstrap a
runtime into reading `AGENTS.md`, its routed policies, and the applicable Agent Skill.
They never duplicate or override a canonical rule.

## The portable-Skill boundary

A portable Agent directory may contain:

```text
agents/<agent>/
  SKILL.md      canonical operational definition of the Agent
  metadata/     declarative, machine-readable identity / capabilities / contract shape
  policies/     portable engineering standards the Agent applies while performing its role
  runbooks/     repeatable execution workflows for classes of the Agent's work
  templates/    reusable structured artifacts / contracts
  README.md     human-facing overview — explanatory only, never a source of canonical behavior
```

**Operational files** are everything under `agents/<agent>/` except `README.md`. They
must remain fully correct and executable with the repository-root `AGENTS.md`,
`CLAUDE.md`, `README.md`, and `policies/` **removed from the environment entirely**. A
consumer that installs only `agents/<agent>/` must not need any root
repository-development file to run the Skill.

Concretely, an operational file must not link to or require, as a runtime dependency:

```text
/AGENTS.md
/CLAUDE.md
/README.md
/policies/**
```

If a rule an Agent needs at runtime must survive being consumed on its own, its canonical
home is inside the Skill, using the resource type that best fits it:

```text
normative reusable engineering rule   → agents/<agent>/policies/…
operational procedure                 → agents/<agent>/runbooks/…
reusable output / content shape       → agents/<agent>/templates/…
Agent-level responsibility / boundary → agents/<agent>/SKILL.md
machine-readable identity / contract  → agents/<agent>/metadata/…
```

A human-facing `README.md` under `agents/<agent>/` **may** link to a root file for
explanatory context, but only when the link is genuinely explanatory and nothing
operational depends on it.

This boundary is narrowly about *this repository's own* development instructions. It does
not restrict an Agent from discovering and following the conventions of a **target
repository** it was assigned to work in — reading that target repo's own `AGENTS.md` /
`CLAUDE.md` / linter config is legitimate, portable Agent behavior.

The repository validator enforces this boundary — see
[validation-and-clean-exit.md](validation-and-clean-exit.md).

## Repository policy vs. Agent policy

```text
/policies/                 rules for developing THIS repository (never packaged)
/agents/<agent>/policies/   portable behavior of an Agent performing its role
```

Repository-level Git/PR/validation policy must not migrate into `agents/<agent>/` and
become part of an Agent's portable runtime behavior. Conversely, an Agent's engineering
standards must not migrate into `/policies/` merely to centralize them — they belong with
the Agent.

## Agent research and design documents

Research for a new Agent, or a material redesign of an Agent's role or Skill contract,
produces human-reviewed design documents before implementation when the work needs both
architecture and implementation design:

```text
research
  -> HLD
  -> approved high-level boundaries
  -> LLD
  -> implementation task
```

The preferred locations are:

```text
docs/agents/<agent-name>/HLD.md
docs/agents/<agent-name>/LLD.md
```

Use [the canonical HLD template](../docs/templates/AGENT_HLD_TEMPLATE.md) and
[the canonical LLD template](../docs/templates/AGENT_LLD_TEMPLATE.md). Do not create an
Agent design directory until it has a real document.

**The HLD/LLD boundary, stated once:**

```text
HLD = ownership + authority + major decisions + system shape
LLD = contracts + states + mechanisms + failure behavior + implementation boundaries
```

The LLD links to and stays consistent with its HLD without duplicating it. If LLD work
changes a high-level assumption, update the HLD rather than silently contradicting it.
Neither document implements the Agent, creates runtime behavior, or substitutes for the
future implementation task. This is the canonical statement of the boundary; the
templates link here instead of restating it.

HLDs and LLDs are engineering documents for humans first and Agents second. Optimize for
fast scanning, explicit decisions, clear ownership, concise diagrams, useful tables,
bullets, and links to canonical rules. Avoid walls of prose, copied research or Issue
bodies, duplicated policy, and implementation diaries. Sections may be brief, and
`None` / `N/A` is valid when a concept genuinely does not apply.

### Distinguishing claims

An HLD or LLD mixes several kinds of statement. Tag the kind when it is not obvious from
context, so a reader never has to guess whether something is settled or assumed:

| Kind | Meaning |
| --- | --- |
| Fact / evidence | Observed or verifiable (existing code, a prior Issue, a measured result) |
| Constraint | A boundary the design must respect but did not choose (portability, an existing contract, a Global Invariant) |
| Assumption | Treated as true for this design but not verified; note what would invalidate it |
| Decision | A choice actually made, with its rationale |
| Rejected alternative | An option considered and not chosen, with why |
| Open question | Unresolved; see below |

This is a vocabulary for prose and table cells, not a new mandatory document type or an
ADR process — use it inline (e.g. in a **Rationale** or **Why it matters** cell) wherever
it removes ambiguity about what kind of claim is being made.

### Open questions and blocking status

Every open question (an HLD's *Open Questions* table, an LLD's *Remaining Implementation
Questions* table) must be marked **Blocking** or **Non-blocking**. A **Blocking**
question means implementation cannot correctly start until it is resolved; leaving it
unmarked is not a valid substitute for marking it non-blocking. "Undecided" must be
visible in this column, never left to hide inside prose.

### Diagram usage

A diagram earns its place when it clarifies something a table or bullets cannot: a
multi-Agent interaction, a dependency graph, a state machine, concurrency, an authority
flow, or a multi-stage lifecycle. Otherwise, prefer tables and bullets. Diagrams are
never mandatory for template symmetry — a section with no useful diagram simply has none.

### Evaluation readiness

An LLD should expose what a future benchmark/evaluation harness would need, without
designing that harness: observable success, failure states, contract violations,
authority violations, expected outputs, which decisions are deterministic versus
LLM-made, and what evidence artifacts (logs, diffs, validation output) a harness could
inspect. `N/A` is valid for an Agent where a property genuinely does not apply yet.

### Ready for implementation

A piece of Agent research becomes an implementation Issue only once:

- authority is clear (the HLD's Authority and Decision Boundaries has no unresolved gap);
- contracts are clear (the LLD's Assignment/Result Contract is stable);
- lifecycle is clear (the LLD's Workflow/State Model, or `N/A`, is settled);
- important failure behavior is clear (the LLD's Failure Behavior is settled);
- every **Blocking** open question is resolved (a **Non-blocking** one may remain open);
- implementation can be split into roughly 3–8 bounded, ordered steps (the LLD's
  Implementation Sequence).

Until all of these hold, the work stays research/design — do not open an implementation
Issue against it. This is the canonical criteria list; the LLD template's *Ready for
Implementation* section applies it per-Agent and links here rather than restating it.

## No premature `shared/`

Do not create a `shared/` layer in this repository yet. Extract a cross-Agent shared
resource only when a **genuine repeated cross-Agent contract or policy exists** — that
is, when two or more Agent Skills need the *same* rule or artifact verbatim at runtime.
Until then, each Agent owns its own copy of what it needs. Likely first candidates, when
the time comes: the assignment/result status vocabulary, cross-Agent contract
conventions, and the parallel-work invariant.
