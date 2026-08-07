# Framework Standards — Contract

This file defines what a per-framework `CODE-STANDARDS.md` covers. It is itself an
operational contract, not human-only documentation — the Backend Agent relies on it to
know what to expect from `frameworks/<framework>/CODE-STANDARDS.md`.

A framework standard covers behavior introduced by a specific framework or runtime
ecosystem built on top of a language — not the language itself. A framework standard may
apply to more than one language (e.g. Spring Boot applies to both Java and Kotlin); the
assignment determines which language/framework combination is actually in effect.

A framework standard is loaded because the assignment names that framework, not because
the Backend Agent detected or preferred it — see
[../../SKILL.md](../../SKILL.md#multi-language-architecture). If the assignment names a
framework that does not support the assigned language (or vice versa), that is an
assignment inconsistency — see [../../SKILL.md](../../SKILL.md#assignment-validation) —
the Backend Agent reports it rather than reinterpreting the task.

## Scope

A framework standard should address the categories below where relevant to that
framework.

- Application/module structure.
- Lifecycle.
- Dependency injection.
- Framework-native annotations/decorators/macros.
- Request/response handling.
- Validation.
- Configuration.
- Persistence integration.
- Transactions.
- Middleware / interceptors / filters.
- Exception/error mapping.
- Authentication/authorization integration.
- OpenAPI/Swagger.
- Observability.
- Logging.
- Unit testing.
- Integration testing.
- Framework-native testing facilities.
- Test application/context startup strategy.
- Framework-specific concurrency.
- Framework-specific performance concerns.
- Security concerns.
- Common anti-patterns.

Framework standards should prefer framework-native capabilities where they reduce
boilerplate or improve correctness, but must still respect repository conventions and
avoid unnecessary magic — see
[../../SKILL.md](../../SKILL.md#boilerplate-reduction-and-native-feature-usage).

## Out of scope

A framework standard must **not** redefine generic language rules unnecessarily — those
belong in the corresponding [language standard](../languages/CODE-STANDARDS.md). For
example, the Spring Boot standard should not restate general Java null-handling rules; it
should only add what Spring itself introduces.

## Style

Framework standards are normative, not tutorials — see
[../../SKILL.md](../../SKILL.md#normative-style). No framework marketing, no
version-specific claims beyond what the assigned project requires.

## Current standards

- [spring-boot/CODE-STANDARDS.md](spring-boot/CODE-STANDARDS.md) — applies to Java and
  Kotlin.
- [nestjs/CODE-STANDARDS.md](nestjs/CODE-STANDARDS.md) — applies to TypeScript.
- [fastapi/CODE-STANDARDS.md](fastapi/CODE-STANDARDS.md) — applies to Python.
- [gin/CODE-STANDARDS.md](gin/CODE-STANDARDS.md) — applies to Go.
- [axum/CODE-STANDARDS.md](axum/CODE-STANDARDS.md) — applies to Rust.
- [actix-web/CODE-STANDARDS.md](actix-web/CODE-STANDARDS.md) — applies to Rust.

This list is not closed — additional frameworks may be added following the same contract.
