# NestJS Framework Standards

Applies when the assignment names NestJS as the framework, together with the
[TypeScript](../../languages/typescript/CODE-STANDARDS.md) language standard. This
standard adds only what NestJS itself introduces — general TypeScript rules live in the
language standard.

## Framework

- Organize code around modules/controllers/providers consistent with the repository's
  existing structure — do not restructure module boundaries without a task-justified
  reason.
- Use constructor-based dependency injection; keep providers focused on a single
  responsibility.
- Validate incoming requests with DTOs and the repository's existing validation pipeline
  (e.g. `class-validator` pipes) rather than manual validation inside handlers.
- Use pipes for transformation/validation, guards for authorization checks, interceptors
  for cross-cutting concerns, and filters for exception mapping — keep each in its
  intended role rather than mixing responsibilities.
- Respect module lifecycle hooks (`OnModuleInit`, `OnModuleDestroy`, etc.) for
  setup/teardown instead of ad hoc initialization code.
- Use async providers (`useFactory`/`async` module registration) when a dependency
  requires asynchronous setup, following the repository's existing pattern.
- Use request-scoped providers only when the task genuinely requires per-request state —
  they carry a performance cost and should not be the default scope.
- Keep persistence integration (ORM/repository pattern) consistent with the framework and
  library already used in the repository.
- Handle transactions according to the persistence library already used — NestJS itself
  does not prescribe a transaction mechanism.
- Map exceptions to HTTP responses through the repository's existing exception-filter
  setup rather than per-controller error handling.
- Avoid circular module dependencies; if one emerges, restructure providers/modules
  rather than forcing it with `forwardRef` as a first resort.
- Keep business/domain logic in services, not controllers — controllers should stay thin
  request/response adapters.

## Prefer NestJS-native decorators

Where appropriate and consistent with the repository, prefer NestJS's own decorators and
mechanisms — `@Controller`, `@Injectable`, `@Module`, `@UseGuards`, `@UseInterceptors`,
`@UsePipes`, `@Catch`, plus validation/OpenAPI decorators — instead of hand-written
infrastructure that duplicates what NestJS already provides. Do not over-decorate classes
or hide business logic inside decorators — a decorator should wire behavior, not contain
it.

## OpenAPI

Keep OpenAPI/Swagger decorators consistent with the repository's existing API
documentation setup.

## Testing

- Write unit tests for providers/services in isolation using standard testing-framework
  mocking, without booting a Nest application context.
- Write integration tests using Nest's testing module (`@nestjs/testing`,
  `Test.createTestingModule`) consistent with the repository's existing test conventions.
- Write end-to-end-style application tests only to the extent the Backend Agent's own
  implementation-level validation responsibility requires — broader E2E ownership belongs
  to the future QA Agent.
- Run the repository's existing test command for the affected module before reporting
  the implementation complete; if it cannot be run, report why, what was validated
  instead, and the remaining risk.

## Logging

Use structured logging consistent with the repository's existing logging setup — see
[../../global/CODE-STANDARDS.md](../../global/CODE-STANDARDS.md#logging) and the
TypeScript language standard's logging section.
