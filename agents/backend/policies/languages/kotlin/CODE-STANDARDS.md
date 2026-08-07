# Kotlin Language Standards

Applies whenever the assignment names Kotlin, regardless of framework. Framework-specific
concerns (e.g. Spring) belong in the corresponding
[framework standard](../../frameworks/CODE-STANDARDS.md), not here.

## Language

- Treat Kotlin's null safety as the primary defense against null-related failures — model
  optionality in the type system rather than working around it.
- Avoid the not-null assertion (`!!`); prefer safe calls, `?:`, `requireNotNull`, or
  restructuring so nullability is handled explicitly at the point it's introduced.
- Use data classes for value-holding types; do not use them for types with significant
  behavior or identity semantics.
- Use sealed classes/interfaces to model closed sets of domain states or outcomes instead
  of open class hierarchies or stringly-typed state.
- Use value classes to give primitive-like values type safety when doing so meaningfully
  prevents mistakes (e.g. distinguishing IDs); do not overuse them for trivial wrappers.
- Use extension functions to add focused, readable behavior — not to accumulate an
  unbounded ad hoc API surface over unrelated types.
- Favor an expression-oriented style (`when`, expression bodies) where it improves
  clarity over an imperative equivalent; do not force it where a straightforward
  statement is clearer.
- Prefer immutable collections and `val` by default; use mutable collections/`var` only
  where mutation is intentional and localized.
- Use scope functions (`let`, `run`, `apply`, `also`, `with`) deliberately for the
  semantic they express — not as a default habit that obscures control flow.
- Use coroutines with structured concurrency (`coroutineScope`, structured builders) —
  avoid `GlobalScope` and unscoped coroutine launches.
- Keep `suspend` boundaries explicit and intentional; do not mark functions `suspend`
  without a real suspension point, and do not silently drop suspension in wrapper code.
- Propagate cancellation correctly — cooperate with `CancellationException` rather than
  catching and swallowing it.
- Handle exceptions raised inside coroutines explicitly (structured `try`/`catch`,
  `CoroutineExceptionHandler` where appropriate) — do not let coroutine failures fail
  silently.
- When interoperating with Java code/libraries, respect Java nullability annotations (or
  their absence) and validate assumptions at the boundary rather than trusting them
  blindly.
- Avoid excessive DSL/abstraction cleverness that trades readability for elegance —
  prefer the simplest construct that is clear to the next reader.

## Boilerplate reduction

- Prefer Kotlin-native constructs (data classes, default/named arguments, destructuring,
  extension functions, sealed types) over mechanically reproducing Java patterns (manual
  getters/setters, builder classes for simple values, utility classes for what an
  extension function expresses).
- Reach for a third-party code-generation library only when Kotlin's own language
  features do not already solve the problem — Kotlin removes most of the boilerplate
  Lombok-style tools exist to solve in Java.

## Dependency/build tooling

Respect the repository's existing Gradle (or other build tool) conventions rather than
introducing a new structure.

## Testing

- Follow the testing ecosystem conventions already used in the repository (e.g.
  `kotlin.test`, JUnit 5 with Kotlin extensions, Kotest) for structure and naming.
- Keep unit tests isolated and independently runnable — no dependence on execution order
  or shared mutable state.
- Mock external boundaries (persistence, HTTP clients, messaging) rather than internal
  collaborators; prefer fakes over deep mock chains where they produce clearer tests.
- Test coroutine code using the repository's existing coroutine-testing tooling (e.g.
  `kotlinx-coroutines-test`, `runTest`) — do not test suspend functions with real
  `Thread.sleep`/timing-based waits.
- Verify cancellation and failure paths for coroutine-based code, not only the success
  path.
- Add integration tests when the change touches persistence, HTTP boundaries, or
  framework wiring — see the applicable framework standard.
- Run the repository's existing test command for the affected module before reporting
  the implementation complete; if it cannot be run, report why, what was validated
  instead, and the remaining risk.

## Logging

- Use the repository's existing logging abstraction (e.g. SLF4J via a Kotlin-friendly
  wrapper) rather than `println` or a competing logging library.
- Follow the global logging levels and content rules in
  [../../global/CODE-STANDARDS.md](../../global/CODE-STANDARDS.md#logging).
