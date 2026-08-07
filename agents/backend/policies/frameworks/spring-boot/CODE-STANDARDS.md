# Spring Boot Framework Standards

Applies when the assignment names Spring Boot as the framework, together with either the
[Java](../../languages/java/CODE-STANDARDS.md) or
[Kotlin](../../languages/kotlin/CODE-STANDARDS.md) language standard depending on the
assigned language. This standard adds only what Spring itself introduces — general
language rules live in the applicable language standard.

## Framework

- Use constructor injection for required dependencies; avoid field injection.
- Keep controller/service/repository boundaries consistent with the repository's existing
  layering — do not introduce a different layering scheme mid-task.
- Prefer typed configuration properties (`@ConfigurationProperties` or equivalent) over
  scattering raw `@Value` lookups for related settings.
- Be aware of bean lifecycle and scope (singleton by default) — avoid hidden mutable
  state in singleton beans that would not be safe under concurrent requests.
- Validate incoming requests at the boundary (`@Valid`/`@Validated` with Bean Validation
  annotations) rather than deep inside service logic.
- Map exceptions to responses consistently through the repository's existing mechanism
  (e.g. `@ControllerAdvice`/`@ExceptionHandler`) rather than ad hoc per-controller
  handling.
- Keep transaction boundaries (`@Transactional`) explicit and no wider than necessary; be
  aware of proxy-based self-invocation limits (a `@Transactional` method called from
  within the same class does not go through the proxy).
- Do not perform long-running external calls (HTTP, messaging) inside a database
  transaction — keep the transactional scope limited to persistence work.
- Follow the repository's existing Spring Data (or other persistence) patterns for
  queries and repositories rather than introducing a parallel data-access style.
- Run asynchronous work only through Spring-managed mechanisms (`@Async` with a
  configured executor, or the repository's existing async infrastructure) — do not spawn
  unmanaged threads inside a Spring-managed component.
- Respect existing security integration boundaries (e.g. Spring Security configuration)
  — do not bypass or duplicate authentication/authorization logic.

## Prefer Spring-native annotations

When Spring provides a relevant annotation or mechanism and the repository follows that
pattern, prefer it over manual boilerplate — for example `@Service`, `@Component`,
`@Repository`, `@RestController`, `@ControllerAdvice`, `@Configuration`,
`@ConfigurationProperties`, `@Validated`, `@Valid`, `@Transactional`. Use annotations
based on semantics, not decoration:

- do not annotate classes unnecessarily;
- do not create framework-managed behavior manually (manual bean wiring, manual
  transaction management) when Spring already provides the correct lifecycle/mechanism;
- avoid annotation-driven "magic" that obscures what the code actually does when a more
  explicit approach would be just as maintainable.

## OpenAPI / observability

- Keep OpenAPI/Swagger annotations/config consistent with the repository's existing
  documentation setup.
- Use Actuator/observability endpoints already configured in the repository rather than
  introducing a parallel health/metrics mechanism.

## Testing

- Write integration tests using the repository's existing Spring test tooling (e.g.
  `@SpringBootTest`, `@WebMvcTest`/`@DataJpaTest` slice tests) rather than introducing a
  different test harness.
- Do not start a full Spring application context for a unit test that does not need it —
  use a narrower test slice, or a plain unit test with the collaborators mocked/faked,
  wherever the test does not genuinely need Spring's wiring.
- Use Testcontainers for integration tests only where the repository already uses it, or
  where the task justifies introducing it.
- Run the repository's existing build/test command (Maven or Gradle) for the affected
  module before reporting the implementation complete; if it cannot be run, report why,
  what was validated instead, and the remaining risk.

## Logging

Use structured logging with correlation/trace identifiers consistent with the
repository's existing logging setup — see
[../../global/CODE-STANDARDS.md](../../global/CODE-STANDARDS.md#logging) and the
applicable language standard's logging section.
