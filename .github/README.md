# `.github/` — Automation Map

Explanatory map of this repository's GitHub automation: what each workflow triggers on,
what it is responsible for, what it is allowed to change, and which canonical policy or
script owns its contract. This file is **navigational** — it never defines a rule. Every
normative contract lives in the linked policy or script; this README only points at it.

See [../AGENTS.md](../AGENTS.md) for global invariants and routing, and
[../policies/README.md](../policies/README.md) for the repository-development policies.

## Workflows

| Workflow | Trigger | Responsibility | Mutation boundary | Canonical contract |
| --- | --- | --- | --- | --- |
| [`repository-validation.yml`](workflows/repository-validation.yml) | `pull_request` → `main` | Run the deterministic repository validator and the `tests/` suite (Markdown integrity, required files, portable-Skill boundary, Agent contracts). | **Read-only.** Reports a pass/fail status check; changes nothing. | [`scripts/validate_repository.py`](../scripts/validate_repository.py), [`tests/`](../tests) |

Mutating automation from [#28](https://github.com/amirbena/agent-ochestration-applications-creation/issues/28)
(PR-description length enforcement, `/claim` + `/unclaim`, Issue-label sync) will be added
here as its child PRs land, each with its trigger, least-privilege `permissions:`,
mutation boundary, and canonical script/policy link.

## Issue and Pull Request templates

| File | Purpose | Canonical contract |
| --- | --- | --- |
| [`ISSUE_TEMPLATE/engineering-task.yml`](ISSUE_TEMPLATE/engineering-task.yml) | The Phase-1 Engineering Task Issue Form (Type / Area / Priority dropdowns plus Problem / Goal / Scope / Non-Goals / Acceptance Criteria / Dependencies / Validation). | [github-issue-pr-authoring.md](../policies/github-issue-pr-authoring.md) owns body **content**; the Form owns field **structure**. |
| [`ISSUE_TEMPLATE/config.yml`](ISSUE_TEMPLATE/config.yml) | Disables blank Issues so every Issue uses the Form. | — |
| [`PULL_REQUEST_TEMPLATE.md`](PULL_REQUEST_TEMPLATE.md) | Applied by GitHub to every PR body. Single source of truth for PR body **structure**. | [git-pr-merge-policy.md](../policies/git-pr-merge-policy.md) (structure ownership), [github-issue-pr-authoring.md](../policies/github-issue-pr-authoring.md) (content guidance). |

## Keeping this file accurate

Any change under `.github/` that adds, removes, or repurposes a workflow updates this map
in the same PR. The **Workflows** table must match the actual contents of
[`workflows/`](workflows/) at merge time.
