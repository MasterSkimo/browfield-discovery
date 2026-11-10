# Compose-first Docker foundation — Discovery and E2E handoff

**Discovery must create the initial Docker setup.** The E2E agent completes and runs it. The existing developer workflow is not the deployment contract for autonomous agents.

## Discovery-owned files

- .e2e/compose.yaml — real application service definitions, supporting DB/broker services and external integration wiring
- .e2e/.env.e2e.example — non-secret variables and safe sample defaults
- .e2e/docker/<service>.Dockerfile — one per required application when no reusable Dockerfile exists
- .e2e/config/<service> — dedicated application E2E profile/config only where necessary
- .gitignore — narrowly scoped ignore of .e2e/.env.e2e.local and any generated local credentials
- .agent-context/environment-blueprint.md — source evidence, created paths, validation result, incomplete tasks

Never overwrite existing developer Compose/Dockerfiles or application configuration. Reuse them by reference if safe; keep new files under .e2e/.

## Compose rules

- Represent **all actual app executables**: frontend, backend, background workers, schedulers, message consumers. Source-build these in Compose, with actual relative build contexts, Dockerfile locations, commands and exposed ports derived from checked-out files. Do not stub application-owned code.
- Include detected databases and brokers with source-grounded engine/image versions, topology/health requirements and service DNS (not localhost for cross-container connections).
- Stub **outside-application** dependencies. Discovery creates their integration routes and can provision a configurable stub service where source-grounded; the E2E agent implements response behavior and errors. Missing stub contracts/wiring become explicit blockers; never let E2E accidentally call production.
- Core app/DB/broker services are not hidden in optional Compose profiles. Optional test runners or diagnostics may be. Compose profiles are different from Spring/application runtime profiles.
- Introduce **separate E2E-specific application profiles/files** only when required and wire them via Compose environment, env_file or supported config-loading mechanism; do not touch developer/prod profiles. Distinguish Compose --env-file interpolation from container env_file and environment overrides.
- Create safe .env.e2e.example and ignore .env.e2e.local; do not commit secrets, client data, token values or user-owned configuration.
- Record healthchecks, readiness and dependency ordering where they can be derived. Avoid inventing health endpoints or claiming a running stack.
- Do not create empty stub/fixture/test directories solely for appearances.

## Minimal handoff example — illustrative, not to be copied verbatim

A target project's Compose file should contain its own real source build declarations, e.g.:

~~~yaml
name: brownfield-e2e
services:
  api:
    build:
      context: ..
      dockerfile: .e2e/docker/api.Dockerfile
    environment:
      SPRING_PROFILES_ACTIVE: e2e
      SPRING_DATASOURCE_URL: jdbc:postgresql://db:5432/e2e
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: e2e
      POSTGRES_USER: e2e
      POSTGRES_PASSWORD: ${DB_TEST_PASSWORD:-local-e2e-only}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U e2e -d e2e"]
      interval: 5s
      timeout: 3s
      retries: 10
~~~

Versions, app variables and commands in this snippet are not assumed to match any scanned project.

## Validation boundaries

Discovery attempts the non-mutating Compose config check when Docker Compose is available, recording actual result and limitations; it performs structural validation regardless of installed Docker. A config parse is **not** proof of successful image builds, application startup, healthy services, stub correctness or coverage.

Downstream E2E agent owns complete stubs, identity, seed/reset, Playwright UI and Newman API-only scenarios, runtime build/start checks, async observations and evidence collection.

Official references: https://docs.docker.com/compose/how-tos/profiles/ ; https://docs.docker.com/reference/compose-file/services/ ; https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/
