# `.github/` — Automation Map

Explanatory map of this repository's GitHub automation: what each workflow triggers on,
what it is responsible for, what it is allowed to change, and which canonical policy or
script owns its contract. This file is **navigational** — it never defines a rule. Every
normative contract lives in the linked policy or script; this file only points at it.

See [../AGENTS.md](../AGENTS.md) for global invariants and routing, and
[../policies/README.md](../policies/README.md) for the repository-development policies.

## Workflows

| Workflow | Trigger | Responsibility | Mutation boundary | Canonical contract |
| --- | --- | --- | --- | --- |
| [`repository-validation.yml`](workflows/repository-validation.yml) | `pull_request` → `main` | Run the deterministic repository validator and the `tests/` suite (Markdown integrity, required files, portable-Skill boundary, Agent contracts). | **Read-only.** Reports a pass/fail status check; changes nothing. | [`scripts/validate_repository.py`](../scripts/validate_repository.py), [`tests/`](../tests) |
| [`pr-description-length.yml`](workflows/pr-description-length.yml) | `pull_request` (`opened` / `edited` / `reopened`) → `main` | Enforce the single useful-content ceiling on the PR description. | **Read-only.** `permissions: {}`, no token; reads the body from the event payload; a failed status check with an evidence log is the only signal. | [`scripts/pr_description_length.py`](../scripts/pr_description_length.py), [github-issue-pr-authoring.md](../policies/github-issue-pr-authoring.md) ("Enforcement: adopted") |
| [`sync-issue-labels.yml`](workflows/sync-issue-labels.yml) | `issues` (`opened` / `edited`) | Reconcile an Issue's managed labels with its Engineering Task Form fields. | **Mutating**, `permissions: issues: write`. Adds/removes **only** `type:*` / `area:*` / `priority:*` labels the Form can produce; never touches other labels or `priority:P0`. Serialized per issue. | [`scripts/sync_issue_labels.py`](../scripts/sync_issue_labels.py) (canonical Form-value → label mapping) |

Mutating automation from [#28](https://github.com/amirbena/agent-ochestration-applications-creation/issues/28)
(`/claim` + `/unclaim`) will be added here as its child PRs land, each with its trigger,
least-privilege `permissions:`, mutation boundary, and canonical script/policy link.

## Issue and Pull Request templates

Opening **New issue** lands on the chooser at `/issues/new/choose` — **Bug Report |
Feature Request | Engineering Task** — with no blank-issue option, so every Issue is
created from one of these forms.

| File | Purpose | Canonical contract |
| --- | --- | --- |
| [`ISSUE_TEMPLATE/bug-report.yml`](ISSUE_TEMPLATE/bug-report.yml) | Lightweight "something is broken" report — required *what happened*, an Affected-area dropdown reusing the Engineering Task Area taxonomy, optional context. Applies `bug` (the repository's existing label; the `type:*` scheme has no `type:bug`). | [github-issue-pr-authoring.md](../policies/github-issue-pr-authoring.md) owns body **content**; the Form owns field **structure**. |
| [`ISSUE_TEMPLATE/feature-request.yml`](ISSUE_TEMPLATE/feature-request.yml) | Lightweight "I want this to behave differently" report — required desired-outcome field, optional area/context. Applies `type:feature` + `enhancement`. | [github-issue-pr-authoring.md](../policies/github-issue-pr-authoring.md) owns body **content**; the Form owns field **structure**. |
| [`ISSUE_TEMPLATE/engineering-task.yml`](ISSUE_TEMPLATE/engineering-task.yml) | The Phase-1 Engineering Task Issue Form (Type / Area / Priority dropdowns plus Problem / Goal / Scope / Non-Goals / Acceptance Criteria / Dependencies / Validation). | [github-issue-pr-authoring.md](../policies/github-issue-pr-authoring.md) owns body **content**; the Form owns field **structure**. |
| [`ISSUE_TEMPLATE/config.yml`](ISSUE_TEMPLATE/config.yml) | Documents the chooser flow and keeps `blank_issues_enabled: false` so every Issue uses a Form; no `contact_links`. | — |
| [`PULL_REQUEST_TEMPLATE.md`](PULL_REQUEST_TEMPLATE.md) | Applied by GitHub to every PR body. Single source of truth for PR body **structure**. | [git-pr-merge-policy.md](../policies/git-pr-merge-policy.md) (structure ownership), [github-issue-pr-authoring.md](../policies/github-issue-pr-authoring.md) (content guidance). |

## Keeping this file accurate

Any change under `.github/` that adds, removes, or repurposes a workflow updates this map
in the same PR. The **Workflows** table must match the actual contents of
[`workflows/`](workflows/) at merge time.
