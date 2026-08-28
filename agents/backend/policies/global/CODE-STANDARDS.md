# Global Backend Standards

Universal backend engineering expectations that apply regardless of language or
framework. Language and framework standards (sibling `policies/languages/<language>/` and
`policies/frameworks/<framework>/` directories) refine or override this baseline per the
precedence model in [../../SKILL.md](../../SKILL.md#precedence); they must not contradict
it without a documented reason tied to that language/framework.

## General engineering

- Preserve existing architecture unless the task explicitly changes it.
- Prefer small, scoped changes over broad rewrites.
- Validate inputs at appropriate boundaries (e.g. API entry points, external integrations).
- Propagate errors intentionally — do not swallow failures silently.
- Maintain backward compatibility when required by the task or contract.
- Avoid leaking secrets (credentials, tokens, keys) into code, logs, or committed files.
- Maintain API-contract consistency; do not silently change a shared contract (see
  [../../SKILL.md](../../SKILL.md#contract-ownership)).
- Avoid unnecessary dependencies.
- Follow the repository's existing tooling rather than replacing it unnecessarily.
- Prefer idiomatic language/framework features that reduce boilerplate over hand-written
  equivalents, but do not add a new dependency solely to save a few lines — see
  [../../SKILL.md](../../SKILL.md#boilerplate-reduction-and-native-feature-usage).

## Concurrency and parallel work

This standard is self-contained: it does not depend on any repository-level instruction
file to be understood or applied.

- Parallel execution is an optimization, never a correctness requirement. Every change
  the Backend Agent produces must remain correct if its work is run sequentially.
- Parallelize only genuinely independent work. Do not parallelize a step that depends on
  the output of another step.
- A shared mutable contract — an API/schema/event contract, a shared source or config
  file, a shared dependency, an ordered database-migration sequence, or generated
  code/clients — is a synchronization boundary. Work touching it is serialized or
  explicitly coordinated, never mutated independently by multiple workers.
- Preserve clear file and module ownership while parallel work is in flight; never let
  two workers write the same file without an explicit ownership split.
- Do not let independent workers generate or apply migrations concurrently, and do not
  let multiple workers regenerate a derived/generated artifact independently and merge
  divergent output.
- If parallel work produces conflicting assumptions, stop and escalate (see
  [../../SKILL.md](../../SKILL.md#stop-conditions)) — never silently pick one.

This governs concurrency within the Backend Agent's own implementation work, including
its internal workers (see [../../SKILL.md](../../SKILL.md#parallel-internal-work)).

## Testing

Testing is a first-class part of implementation, not optional follow-up work — see
[../../SKILL.md](../../SKILL.md#test-execution-as-part-of-the-work-plan).

- Every behavioral change requires tests.
- Write unit tests for the change; add or update integration tests when the change
  crosses a real implementation boundary (persistence, HTTP, messaging, framework
  wiring) — see the applicable language/framework standard for ecosystem-specific detail.
- Run targeted tests for the affected area before considering an implementation done;
  expand to broader validation when the change's risk warrants it.
- Do not report an implementation complete without having run the appropriate tests,
  unless execution is genuinely impossible in the environment. If so, report explicitly
  what could not be run, why, what validation was performed instead, and the remaining
  risk.

## Logging

- Use structured logging via the repository's or framework's standard logging
  abstraction — do not use ad hoc stdout/print statements for production logging.
- Log meaningful operational events; avoid noisy logging inside tight loops or
  high-throughput paths.
- Use levels intentionally: trace/debug for diagnostic detail, info for meaningful
  lifecycle/business events, warn for recoverable abnormal situations, error for failures
  requiring attention.
- Preserve correlation/request/trace identifiers when available, and prefer structured
  contextual fields over concatenated opaque strings.
- Never log secrets, credentials, or tokens; avoid logging unnecessary personal or
  sensitive data, and avoid logging full request/response bodies by default.
- Avoid logging the same failure repeatedly across multiple layers without reason.
- Preserve exception/error context (type, message, stack) where the logging mechanism
  supports it, rather than logging a flattened string.

Language/framework standards specify the idiomatic logging mechanism for that ecosystem.

## Comments

This applies to all supported languages/frameworks unless an explicit repository-local
convention requires otherwise.

- Prefer self-explanatory code over comments — clear naming and structure first.
- Do not comment obvious syntax or restate what the code already says.
- Add a comment only when it provides useful context that cannot be expressed clearly
  through naming or structure. A comment should primarily explain:
  - why a non-obvious decision exists;
  - an important constraint;
  - an external-system limitation;
  - a compatibility/workaround reason;
  - a subtle concurrency, transaction, or lifecycle concern.
- Keep normal implementation comments short — as a default, a contextual comment should
  not exceed approximately 3 lines. If explaining ordinary implementation code needs
  more than that, first consider whether the code should be simplified, naming improved,
  logic extracted, or the explanation belongs in an ADR, runbook, API documentation, or
  another higher-level document instead. Avoid comment blocks that become mini design
  documents inside source files.
- Remove stale comments when behavior changes.
- Do not leave commented-out code.
- Do not use a comment to explain around unclear or overly complex implementation —
  simplify the implementation instead.

Undesirable:

```java
// Increment the counter
counter++;
```

Useful — communicates context the code itself cannot:

```java
// Provider retries duplicate requests after network timeouts.
// Preserve the idempotency key so repeated attempts resolve to the same operation.
```

**Documentation exception**: the ~3-line guidance applies to ordinary inline/block
implementation comments. It does not prohibit longer documentation where the ecosystem
genuinely requires it — public API documentation, Javadoc/KDoc/docstrings, generated
OpenAPI descriptions, or complex protocol documentation. Even there, keep documentation
focused and avoid unnecessary verbosity.

## Adding language/framework standards

Language and framework standards are independent, sibling categories under
`agents/backend/policies/`:

```text
policies/
  global/                          this directory — universal backend standards
  languages/
    CODE-STANDARDS.md               language-standard contract
    java/CODE-STANDARDS.md
    kotlin/CODE-STANDARDS.md
    typescript/CODE-STANDARDS.md
    python/CODE-STANDARDS.md
    go/CODE-STANDARDS.md
    rust/CODE-STANDARDS.md
  frameworks/
    CODE-STANDARDS.md               framework-standard contract
    spring-boot/CODE-STANDARDS.md
    nestjs/CODE-STANDARDS.md
    fastapi/CODE-STANDARDS.md
    gin/CODE-STANDARDS.md
    axum/CODE-STANDARDS.md
    actix-web/CODE-STANDARDS.md
```

This set is not closed. Each language or framework standard should document only what is
specific to it — anything already covered here does not need to be repeated. A framework
standard is not nested under its language standard, since a language can host multiple
unrelated frameworks and both categories should be extensible independently.
