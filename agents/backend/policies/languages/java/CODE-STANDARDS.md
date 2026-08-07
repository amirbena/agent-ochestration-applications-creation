# Java Language Standards

Applies whenever the assignment names Java, regardless of framework. Framework-specific
concerns (e.g. Spring) belong in the corresponding
[framework standard](../../frameworks/CODE-STANDARDS.md), not here.

## Language

- Give each class a single, clear responsibility; avoid god classes.
- Prefer immutability where practical — final fields, immutable collections, defensive
  copies at boundaries.
- Use records for simple value objects/DTOs where the project's Java version supports
  them; do not force records where identity or mutability is genuinely required.
- Avoid returning or accepting `null` for values that can instead be absent-by-design;
  prefer explicit signaling (e.g. `Optional`, a sentinel type) at API boundaries.
- Reserve `Optional` for return types signaling optional results — do not use it for
  fields, method parameters, or collections.
- Follow the repository's existing checked-vs-unchecked exception convention; do not
  introduce a new discipline unilaterally.
- Never swallow exceptions silently — catch only what you can handle, and either recover
  meaningfully or rethrow/wrap with context.
- Use try-with-resources (or equivalent) for anything implementing `AutoCloseable`.
- Prefer the standard collections framework; choose the narrowest useful interface
  (`List`, `Set`, `Map`) over concrete implementations in signatures.
- Use streams where they improve clarity over an equivalent loop; do not chain streams
  purely to appear concise when it reduces readability.
- Preserve type safety — avoid raw types and unchecked casts; do not suppress generics
  warnings without a documented reason.
- For concurrency, prefer `ExecutorService`/`CompletableFuture` and structured
  submission over manual `Thread` creation; use explicit synchronization primitives
  (`java.util.concurrent`) rather than ad hoc locking; do not spawn unmanaged threads.
- Use modern Java language features (e.g. pattern matching, sealed types, records) when
  they are available in the assigned/repository-configured Java version — do not use
  features the project's target version does not support.
- Avoid reflection unless it is the only way to satisfy a requirement — it bypasses type
  safety and complicates maintenance.
- Preserve backward compatibility with the assigned/repository-configured Java version;
  do not assume a newer version is available.

## Boilerplate reduction and code generation

- Prefer native Java features (records, `var`, pattern matching) over manual boilerplate
  when they fit and the project's Java version supports them.
- If the repository already uses a well-established boilerplate-reduction solution such
  as Lombok, and the assigned architecture permits it, prefer the appropriate annotation
  over hand-written repetitive code (e.g. `@Getter`, `@Setter`, `@Builder`,
  `@NoArgsConstructor`, `@AllArgsConstructor`, `@RequiredArgsConstructor`, `@Value`) —
  but apply them intentionally, not by default:
  - prefer `@RequiredArgsConstructor` for dependency-oriented constructor generation
    when appropriate;
  - prefer immutable/value-oriented models when mutation is not required;
  - do not add setters automatically to immutable/domain objects;
  - do not apply `@Data` blindly to every class;
  - avoid generated `equals`/`hashCode`/`toString` where they create problematic
    semantics — recursive references, lazy-loading traps (e.g. JPA entities), or
    sensitive-data exposure.
- Do not introduce Lombok (or an equivalent) into a repository that intentionally does
  not already use it, without architectural justification — this is a dependency
  decision, not a routine implementation choice.

## Dependency/build tooling

Respect the repository's build tool (Maven or Gradle) and its existing module/dependency
layout rather than introducing a second one.

## Testing

- Follow the JUnit ecosystem conventions already used in the repository (JUnit 4 or 5)
  for test structure, lifecycle annotations, and naming.
- Use the repository's existing assertion library (e.g. JUnit assertions, AssertJ,
  Hamcrest) rather than introducing a second one.
- Organize unit tests to mirror the production package structure, one test class per
  unit under test unless the repository's convention differs.
- Keep unit tests isolated and independently runnable — do not depend on execution
  order or shared mutable static state between tests.
- Mock external boundaries (persistence, HTTP clients, messaging) rather than internal
  collaborators; excessive mocking of internal classes is a signal the design should be
  reconsidered, not a testing goal.
- Use parameterized tests for boundary/validation cases with multiple inputs, following
  the repository's existing convention (e.g. JUnit 5 `@ParameterizedTest`).
- Add integration tests when the change touches persistence, HTTP boundaries, or
  framework wiring — see the applicable framework standard for the mechanism (e.g.
  Testcontainers, `@SpringBootTest`).
- Run the repository's existing test command for the affected module before reporting
  the implementation complete; if it cannot be run, report why, what was validated
  instead, and the remaining risk.

## Logging

- Use the repository's existing logging abstraction (e.g. SLF4J) rather than
  `System.out`/`System.err` or a competing logging library.
- Follow the global logging levels and content rules in
  [../../global/CODE-STANDARDS.md](../../global/CODE-STANDARDS.md#logging).

## Tooling

Follow the repository's configured formatter and static-analysis tooling rather than
introducing a personal style.
