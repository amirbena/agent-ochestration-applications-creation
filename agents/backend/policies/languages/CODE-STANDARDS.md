# Language Standards — Contract

This file defines what a per-language `CODE-STANDARDS.md` covers. It is itself an
operational contract, not human-only documentation — the Backend Agent relies on it to
know what to expect from `languages/<language>/CODE-STANDARDS.md`.

A language standard covers concerns intrinsic to a programming language — not to any
particular framework built on top of it. It applies whenever the Backend Agent's
assignment names that language, regardless of which framework (if any) is also assigned.
It is loaded because the assignment names the language, not because the Backend Agent
detected or preferred it — see
[../../SKILL.md](../../SKILL.md#multi-language-architecture).

## Scope

A language standard should address the categories below where relevant to that language.
Not every category applies to every language — omit what doesn't apply rather than
forcing a rule to exist.

- Language idioms.
- Naming.
- Type-system usage.
- Nullability / optional-value handling.
- Immutability and mutation.
- Error handling.
- Resource management.
- Concurrency / async.
- Collections / data structures.
- Package/module organization.
- Dependency management.
- Code generation / language-supported boilerplate reduction.
- Logging.
- Unit testing.
- Integration testing.
- Test naming and organization.
- Test isolation.
- Mocking/faking guidance.
- Formatter/linter/static-analysis tooling.
- Performance pitfalls.
- Security-sensitive language behavior.
- Compatibility with the repository-selected language version.

## Out of scope

A language standard must **not** define framework-specific architecture — e.g. the Java
standard must not define Spring dependency-injection patterns, and the TypeScript
standard must not define NestJS decorators. That belongs in the corresponding
[framework standard](../frameworks/CODE-STANDARDS.md).

## Style

Language standards are normative, not tutorials — see
[../../SKILL.md](../../SKILL.md#normative-style). No syntax introductions, no beginner
examples, no version-specific claims beyond what the assigned project requires. Prefer
actionable rules ("prefer X when Y", "avoid Z because...", "escalate when...") over prose
explanation.

## Current standards

- [java/CODE-STANDARDS.md](java/CODE-STANDARDS.md)
- [kotlin/CODE-STANDARDS.md](kotlin/CODE-STANDARDS.md)
- [typescript/CODE-STANDARDS.md](typescript/CODE-STANDARDS.md)
- [python/CODE-STANDARDS.md](python/CODE-STANDARDS.md)
- [go/CODE-STANDARDS.md](go/CODE-STANDARDS.md)
- [rust/CODE-STANDARDS.md](rust/CODE-STANDARDS.md)

This list is not closed — additional languages may be added following the same contract.
