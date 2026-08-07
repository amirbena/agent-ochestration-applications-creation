# OpenAPI Runbook

- The Backend Agent is responsible for API implementation and its documentation.
- Keep OpenAPI/Swagger definitions consistent with the actual implementation.
- Shared contract changes (request/response shapes, endpoints, error formats) must be
  surfaced to the owning Agent rather than silently changed — see
  [../SKILL.md](../SKILL.md#boundaries).
- If the repository is already contract-first (OpenAPI spec drives implementation), that
  workflow must be preserved; do not switch it to code-first.
