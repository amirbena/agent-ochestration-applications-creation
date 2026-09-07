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

- `CHANGELOG.md` and `policies/changelog-policy.md`: a `## Unreleased` changelog
  discipline with a single canonical definition of when an entry is required, plus a
  **Changelog discipline** `AGENTS.md` Global Invariant and Task Routing row routing to
  the policy, and `CHANGELOG.md` / `policies/changelog-policy.md` added to the
  `scripts/validate_repository.py` required-file set.
  ([#29](https://github.com/amirbena/agent-ochestration-applications-creation/issues/29))
