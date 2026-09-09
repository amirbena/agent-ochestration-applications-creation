# Changelog

All notable changes to this repository's conventions, automation, and Agent Skills are
recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
entries are grouped under **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**,
or **Security**.

**When an entry is required, and when it is not, is defined once in
[policies/changelog-policy.md](policies/changelog-policy.md).** That policy also owns the
`## Unreleased` workflow summarized below. This file never restates those rules.

Accumulate changes under `## Unreleased` as they merge. This repository has no release,
version-tag, or SemVer process yet (see the policy's *Relationship to release
automation*), so there are no dated release sections below `## Unreleased` — only that
section, until a Release process is introduced.

## Unreleased

### Added

- Bug Report and Feature Request Issue Forms: `.github/ISSUE_TEMPLATE/bug-report.yml`
  (applies `bug`) and `.github/ISSUE_TEMPLATE/feature-request.yml` (applies
  `type:feature` + `enhancement`), each short and outcome-first with an Affected-area
  dropdown reusing the Engineering Task Area taxonomy. `config.yml` now documents the
  `/issues/new/choose` chooser flow and why `blank_issues_enabled: false` stays; every
  new Issue is created from one of the three templates. `.github/README.md` lists the
  forms.
  ([#38](https://github.com/amirbena/agent-ochestration-applications-creation/issues/38))
- Automatic Issue-label sync: `scripts/sync_issue_labels.py` (canonical
  Form-value → label mapping, plus a deterministic add/remove plan) and a mutating
  `.github/workflows/sync-issue-labels.yml` (`issues` `opened` / `edited`,
  `permissions: issues: write`, serialized per issue). Reconciles only
  `type:*` / `area:*` / `priority:*` from the Engineering Task Form; non-Form or
  hand-edited Issues and `priority:P0` are left untouched. `.github/README.md` lists
  the workflow.
  ([#33](https://github.com/amirbena/agent-ochestration-applications-creation/issues/33))
- PR-description useful-content ceiling: `scripts/pr_description_length.py` (one
  authoritative `PR_BODY_USEFUL_CONTENT_LIMIT` constant and normalization) and a
  read-only `.github/workflows/pr-description-length.yml` Action on `pull_request` into
  `main`. `policies/github-issue-pr-authoring.md` "Enforcement" is now *adopted* and
  `.github/README.md` lists the workflow.
  ([#30](https://github.com/amirbena/agent-ochestration-applications-creation/issues/30))
- `CHANGELOG.md` and `policies/changelog-policy.md`: a `## Unreleased` changelog
  discipline with a single canonical definition of when an entry is required, plus a
  **Changelog discipline** `AGENTS.md` Global Invariant and Task Routing row routing to
  the policy, and `CHANGELOG.md` / `policies/changelog-policy.md` added to the
  `scripts/validate_repository.py` required-file set.
  ([#29](https://github.com/amirbena/agent-ochestration-applications-creation/issues/29))
