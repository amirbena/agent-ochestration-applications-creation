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

### Changed

- Strengthened `policies/github-issue-pr-authoring.md` so an Issue stays an engineering
  backlog item, not a hidden HLD/LLD: a new "Issue vs. canonical design ownership"
  section states what belongs in an Issue versus a canonical design (no full state
  machines, schema inventories, file-by-file plans, or algorithm design), and a new
  "Decision to make vs. decision already made" rule requires an unsettled behavior to be
  written as `Decide how X should work, subject to Y` rather than a specific mechanism,
  unless that mechanism is already canonical elsewhere. Research Issues and the new
  Implementation Issues subsection both link this rule instead of restating it.
  `.github/ISSUE_TEMPLATE/engineering-task.yml`'s Scope field description now points
  authors at the same rule.
  ([#50](https://github.com/amirbena/agent-ochestration-applications-creation/issues/50))

- Strengthened the Agent HLD/LLD templates
  (`docs/templates/AGENT_HLD_TEMPLATE.md`, `docs/templates/AGENT_LLD_TEMPLATE.md`) before
  Issues #12–#22 produce real design documents against them: the HLD/LLD boundary is now
  a single sharpened formula in `policies/skill-development-policy.md`
  (`HLD = ownership + authority + major decisions + system shape`,
  `LLD = contracts + states + mechanisms + failure behavior + implementation
  boundaries`), with a lightweight fact/constraint/assumption/decision/rejected-alternative
  vocabulary, required Blocking/Non-blocking tagging on every open question, diagram-usage
  guidance, and a canonical "ready for implementation" checklist. The LLD template gained
  `Failure Behavior`, `Evaluation Readiness`, and `Ready for Implementation` sections.
  `scripts/validate_repository.py` now checks that any real
  `docs/agents/<agent>/HLD.md` / `LLD.md` carries every required section from its
  template (structural only, no exact-prose test).
  ([#43](https://github.com/amirbena/agent-ochestration-applications-creation/issues/43))
- Renamed `.github/README.md` to `.github/AUTOMATION.md` so GitHub renders the intended
  root `README.md` as the repository landing page (README files under `.github/` take
  precedence over the root README). The file's role is unchanged — it stays the
  navigational map of `.github/` workflows, Issue Forms, and templates. All references
  (`README.md`, this changelog) now point at the new path.

### Added

- Bug Report and Feature Request Issue Forms: `.github/ISSUE_TEMPLATE/bug-report.yml`
  (applies `bug`) and `.github/ISSUE_TEMPLATE/feature-request.yml` (applies
  `type:feature` + `enhancement`), each short and outcome-first with an Affected-area
  dropdown reusing the Engineering Task Area taxonomy. `config.yml` now documents the
  `/issues/new/choose` chooser flow and why `blank_issues_enabled: false` stays; every
  new Issue is created from one of the three templates. `.github/AUTOMATION.md` lists the
  forms.
  ([#38](https://github.com/amirbena/agent-ochestration-applications-creation/issues/38))
- Automatic Issue-label sync: `scripts/sync_issue_labels.py` (canonical
  Form-value → label mapping, plus a deterministic add/remove plan) and a mutating
  `.github/workflows/sync-issue-labels.yml` (`issues` `opened` / `edited`,
  `permissions: issues: write`, serialized per issue). Reconciles only
  `type:*` / `area:*` / `priority:*` from the Engineering Task Form; non-Form or
  hand-edited Issues and `priority:P0` are left untouched. `.github/AUTOMATION.md` lists
  the workflow.
  ([#33](https://github.com/amirbena/agent-ochestration-applications-creation/issues/33))
- PR-description useful-content ceiling: `scripts/pr_description_length.py` (one
  authoritative `PR_BODY_USEFUL_CONTENT_LIMIT` constant and normalization) and a
  read-only `.github/workflows/pr-description-length.yml` Action on `pull_request` into
  `main`. `policies/github-issue-pr-authoring.md` "Enforcement" is now *adopted* and
  `.github/AUTOMATION.md` lists the workflow.
  ([#30](https://github.com/amirbena/agent-ochestration-applications-creation/issues/30))
- `CHANGELOG.md` and `policies/changelog-policy.md`: a `## Unreleased` changelog
  discipline with a single canonical definition of when an entry is required, plus a
  **Changelog discipline** `AGENTS.md` Global Invariant and Task Routing row routing to
  the policy, and `CHANGELOG.md` / `policies/changelog-policy.md` added to the
  `scripts/validate_repository.py` required-file set.
  ([#29](https://github.com/amirbena/agent-ochestration-applications-creation/issues/29))
