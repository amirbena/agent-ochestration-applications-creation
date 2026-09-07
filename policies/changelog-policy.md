# Changelog Policy

Canonical rules for **`CHANGELOG.md`** in development of this repository: the
`## Unreleased` workflow, when a change requires an entry and when it does not, and the
entry format.

This is a repository-development policy. It is **not** packaged into any Agent Skill, and
no `agents/<agent>/` resource may depend on it. It governs the changelog for *this*
repository — it is distinct from any changelog an Agent maintains inside a target
repository it was assigned. See [../AGENTS.md](../AGENTS.md) for global invariants and
routing, [repository-workflow.md](repository-workflow.md) for task-branch creation, and
[validation-and-clean-exit.md](validation-and-clean-exit.md) for the clean end state a
task finishes in.

This file is the canonical home of the **Changelog discipline** Global Invariant;
[../AGENTS.md](../AGENTS.md) carries only its one-line summary. [../CHANGELOG.md](../CHANGELOG.md)
holds the entries and links here; it never restates these rules.

## The `## Unreleased` workflow

- [../CHANGELOG.md](../CHANGELOG.md) has exactly one working section, `## Unreleased`, at
  the top. Every qualifying change adds its entry there **in the same Pull Request** that
  makes the change.
- Entries accumulate under `## Unreleased` between releases. This repository has no
  release, version-derivation, tag, or SemVer process yet, so nothing moves out of
  `## Unreleased` today — there are no dated release sections.
- When a Release process is later introduced, it — not this policy and not an author
  mid-task — owns cutting `## Unreleased` into a dated, versioned section. Adding that
  mechanism is out of scope here (see *Relationship to release automation*).

## When an entry is required

Add an `## Unreleased` entry when a merged change alters something a **consumer of this
repository** — a human contributor, a coding agent following the workflow, or a runtime
consuming an Agent Skill — would need to know about without reading the diff:

- a normative rule change: `AGENTS.md` invariants or precedence, any file under
  `policies/`, or an Agent's canonical Skill sources
  (`agents/<agent>/SKILL.md`, `.../policies/`, `.../runbooks/`, `.../templates/`,
  `.../metadata/`);
- a change to repository automation an author interacts with: GitHub workflow triggers or
  behavior, the Issue Form, the Pull Request template, or the label set;
- a change to the validation contract: what `scripts/validate_repository.py` or `tests/`
  enforces, or the commands used to run them;
- adding, removing, or renaming an Agent, a policy, a template, or a runbook;
- any change that moves a canonical home or changes a documented contract.

## When an entry is not required

Skip the changelog when the change does not affect any consumer-visible contract:

- internal refactoring of `scripts/` or `tests/` with no behavior or contract change;
- test-only additions that do not change what is enforced;
- fixes to typos, formatting, links, or wording that do not change meaning;
- work-in-progress commits on a task branch (the entry is required by merge time, not per
  commit);
- changes fully contained in explanatory files (`README.md`, `docs/`, navigational
  READMEs) that do not document a new or changed contract.

If a change is genuinely borderline, add the entry — a redundant line is cheaper than a
silent contract change.

## Entry format

- Group entries under the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
  headings: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security**.
- One entry per change: a single sentence in the imperative or descriptive present,
  naming the affected file, policy, or Agent, and linking the Issue or PR.
- State the consumer-visible effect, not the implementation steps. Link the canonical
  document for detail rather than reproducing it — the changelog is a pointer, not a
  second specification.

## Relationship to release automation

This policy covers changelog **discipline** only. Release packaging, version derivation,
SemVer, Git tags, and moving `## Unreleased` into a dated section are a future Release
concern and are deliberately not defined here or anywhere else in the repository yet.
